#!/usr/bin/env python3
from __future__ import annotations

import ast
import copy
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PHASE0 = ROOT / "tests/context-v1/phase0/phase0_contract.py"
PLUGIN_NAMES = ("context-core", "context-decision", "context-assumption", "context-term")
OWNER_SKILLS = {
    "context-core": "context",
    "context-decision": "decision",
    "context-assumption": "assumption",
    "context-term": "term",
}
OWNER_CLIS = {
    name: f"skills/{skill}/scripts/{skill}_cli.py"
    for name, skill in OWNER_SKILLS.items()
}
INIT_ENTRYPOINTS = {
    "context-core": "skills/context/scripts/context_cli.py",
    "context-decision": "skills/init/scripts/decision_init.py",
    "context-assumption": "skills/init/scripts/assumption_init.py",
    "context-term": "skills/init/scripts/term_init.py",
}
SCHEMA_NAMES = {
    "context-core": "context-core-schema/v1",
    "context-decision": "context-decision-schema/v1",
    "context-assumption": "context-assumption-schema/v1",
    "context-term": "context-term-schema/v1",
}
FORBIDDEN_KEYS = {
    "dependencies",
    "dependency",
    "requires",
    "implicit_install",
    "implicitInstall",
    "default_install",
    "defaultInstall",
    "installed_by_default",
    "installedByDefault",
}


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


phase0 = load("phase0_distribution_proof", PHASE0)


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def recursive_keys(value) -> set[str]:
    if isinstance(value, dict):
        return set(value) | set().union(*(recursive_keys(item) for item in value.values()), set())
    if isinstance(value, list):
        return set().union(*(recursive_keys(item) for item in value), set())
    return set()


def digest_tree(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        digest.update(path.read_bytes())
    return digest.hexdigest()


class DistributionProofTests(unittest.TestCase):
    def test_acceptance_41_dependency_matrix(self) -> None:
        fixtures = ROOT / "tests/context-v1/fixtures/host-inventory"
        required = read_json(fixtures / "required-plugin.json")
        corpus = read_json(fixtures / "preflight-cases.json")
        expected = {
            "core_missing",
            "core_source_mismatch",
            "core_disabled",
            "core_incompatible",
            "core_uninitialized",
            "ready",
        }
        observed: set[str] = set()
        for case in corpus["cases"]:
            inventory = copy.deepcopy(case["inventory"])
            doctor = copy.deepcopy(case["doctor"])
            before = json.dumps({"inventory": inventory, "doctor": doctor}, sort_keys=True)
            with tempfile.TemporaryDirectory() as temp:
                repo = Path(temp) / "repository"
                host = Path(temp) / "host-config"
                repo.mkdir()
                host.mkdir()
                subprocess.run(["git", "init", "-q", str(repo)], check=True)
                (repo / "keep.txt").write_text("repository bytes\n", encoding="utf-8")
                (host / "config.json").write_text('{"keep":true}\n', encoding="utf-8")
                byte_before = (digest_tree(repo), digest_tree(host))
                result = phase0.classify_preflight(inventory, doctor, required)
                rendered = phase0.render_preflight(result, case["host"], required)
                self.assertEqual(byte_before, (digest_tree(repo), digest_tree(host)))
            observed.add(rendered["code"])
            self.assertEqual(required, rendered["required_plugin"])
            self.assertEqual({"repository": "none", "host_configuration": "none"}, rendered["write_policy"])
            self.assertEqual(before, json.dumps({"inventory": inventory, "doctor": doctor}, sort_keys=True))
        self.assertEqual(expected, observed)

        readme = (ROOT / "plugins/context-decision/README.md").read_text(encoding="utf-8")
        for code in expected - {"ready"}:
            self.assertIn(f"`{code}`", readme)
        for token in (
            "context-plugins",
            "context-core@context-plugins",
            "Jeis-Jw/context-plugins",
            "scope",
            "reload",
            "새 session",
            "context-decision:init",
        ):
            self.assertIn(token, readme)
        for code in expected - {"ready", "core_uninitialized"}:
            line = next(line for line in readme.splitlines() if line.startswith(f"- `{code}`:"))
            for token in ("Jeis-Jw/context-plugins", "scope", "reload", "새 session", "context-decision:init", "재시도"):
                self.assertIn(token, line)
        absent_line = next(line for line in readme.splitlines() if line.startswith("- `core_uninitialized`:"))
        for token in ("installed", "context-core", "bootstrap", "같은 호출", "decision"):
            self.assertIn(token, absent_line)

    def test_acceptance_42_repository_absent(self) -> None:
        fixtures = ROOT / "tests/context-v1/fixtures/host-inventory"
        required = read_json(fixtures / "required-plugin.json")
        corpus = read_json(fixtures / "preflight-cases.json")["cases"]
        case = next(item for item in corpus if item["expected_code"] == "core_uninitialized")
        with tempfile.TemporaryDirectory() as temp:
            repo = Path(temp) / "repository"
            host = Path(temp) / "host"
            repo.mkdir()
            host.mkdir()
            subprocess.run(["git", "init", "-q", str(repo)], check=True)
            (repo / "keep.txt").write_text("keep\n", encoding="utf-8")
            (host / "config.json").write_text("{}\n", encoding="utf-8")
            before = (digest_tree(repo), digest_tree(host))
            rendered = phase0.render_preflight(
                phase0.classify_preflight(case["inventory"], case["doctor"], required),
                case["host"],
                required,
            )
            self.assertEqual("core_uninitialized", rendered["code"])
            self.assertNotEqual("core_missing", rendered["code"])
            self.assertIn("public bootstrap surface", " ".join(rendered["manual_actions"]))
            self.assertEqual(before, (digest_tree(repo), digest_tree(host)))

            context_cli = load(
                "context_cli_distribution_direct_init",
                ROOT / "plugins/context-core/skills/context/scripts/context_cli.py",
            )
            initialized = context_cli.bootstrap_repository(repo, host=case["host"])
            self.assertEqual(
                [("core_init", "applied"), ("policy_install", "applied")],
                [(phase["phase"], phase["status"]) for phase in initialized["phases"]],
            )
            self.assertEqual("ready", initialized["doctor"]["repository_state"])
            self.assertEqual("AGENTS.md", initialized["policy"]["target"])
            self.assertTrue(initialized["policy"]["applied"])
            self.assertIn(context_cli.POLICY_BODY, (repo / "AGENTS.md").read_text(encoding="utf-8"))
            self.assertEqual("keep\n", (repo / "keep.txt").read_text(encoding="utf-8"))
            self.assertEqual(before[1], digest_tree(host))

        context_cli = load(
            "context_cli_distribution_storage_error",
            ROOT / "plugins/context-core/skills/context/scripts/context_cli.py",
        )
        with tempfile.TemporaryDirectory() as temp:
            repo = Path(temp)
            subprocess.run(["git", "init", "-q", temp], check=True)
            with self.assertRaises(context_cli.ContextError) as caught:
                context_cli.recall_repository(repo)
            self.assertEqual("context_root_missing", caught.exception.code)

    def test_acceptance_43_manifests(self) -> None:
        claude_marketplace = read_json(ROOT / ".claude-plugin/marketplace.json")
        codex_marketplace = read_json(ROOT / ".agents/plugins/marketplace.json")
        self.assertEqual("context-plugins", claude_marketplace["name"])
        self.assertEqual("context-plugins", codex_marketplace["name"])
        self.assertEqual(list(PLUGIN_NAMES), [item["name"] for item in claude_marketplace["plugins"]])
        self.assertEqual(list(PLUGIN_NAMES), [item["name"] for item in codex_marketplace["plugins"]])
        claude_entries = {item["name"]: item for item in claude_marketplace["plugins"]}
        codex_entries = {item["name"]: item for item in codex_marketplace["plugins"]}

        for name in PLUGIN_NAMES:
            root = ROOT / "plugins" / name
            claude = read_json(root / ".claude-plugin/plugin.json")
            codex = read_json(root / ".codex-plugin/plugin.json")
            self.assertEqual(name, claude["name"])
            self.assertEqual(name, codex["name"])
            self.assertEqual("0.5.0", claude["version"])
            self.assertEqual(claude["version"], codex["version"])
            self.assertEqual(claude["version"], claude_entries[name]["version"])
            self.assertEqual(claude["version"], codex_entries[name]["version"])
            self.assertEqual(claude["description"], claude_entries[name]["description"])
            self.assertEqual(codex["description"], codex_entries[name]["description"])
            self.assertEqual(f"./plugins/{name}", claude_entries[name]["source"])
            self.assertEqual({"source": "local", "path": f"./plugins/{name}"}, codex_entries[name]["source"])
            self.assertEqual(
                {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
                codex_entries[name]["policy"],
            )
            self.assertEqual("Productivity", codex_entries[name]["category"])
            for document in (claude, codex, claude_entries[name], codex_entries[name]):
                self.assertFalse(FORBIDDEN_KEYS & recursive_keys(document))
            plugin_readme = (root / "README.md").read_text(encoding="utf-8")
            self.assertIn("0.5.0", plugin_readme)
            if name in {"context-core", "context-decision"}:
                self.assertIn("0.4.1", plugin_readme)

            skills = root / codex["skills"]
            self.assertTrue(skills.is_dir())
            with tempfile.TemporaryDirectory() as temp:
                cached = Path(temp) / name
                shutil.copytree(root, cached)
                for relative in ("skills/init/SKILL.md", f"skills/{OWNER_SKILLS[name]}/SKILL.md"):
                    self.assertTrue((cached / relative).is_file())
                owner_cli = cached / OWNER_CLIS[name]
                init_entrypoint = cached / INIT_ENTRYPOINTS[name]
                self.assertTrue(owner_cli.is_file())
                self.assertTrue(init_entrypoint.is_file())
                environment = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
                environment.pop("CLAUDE_PLUGIN_ROOT", None)
                before = digest_tree(cached)
                for command in (
                    [sys.executable, str(owner_cli), "--help"],
                    [sys.executable, str(init_entrypoint), *("init", "--help")]
                    if name == "context-core"
                    else [sys.executable, str(init_entrypoint), "--help"],
                ):
                    resolved = subprocess.run(command, cwd=temp, env=environment, text=True, capture_output=True)
                    self.assertEqual(0, resolved.returncode, resolved.stdout + resolved.stderr)
                schema_probe = subprocess.run(
                    [sys.executable, str(owner_cli), "schema", "--json"],
                    cwd=temp,
                    env=environment,
                    text=True,
                    capture_output=True,
                )
                capabilities_probe = subprocess.run(
                    [sys.executable, str(owner_cli), "capabilities", "--json"],
                    cwd=temp,
                    env=environment,
                    text=True,
                    capture_output=True,
                )
                self.assertEqual(0, schema_probe.returncode, schema_probe.stdout + schema_probe.stderr)
                self.assertEqual(0, capabilities_probe.returncode, capabilities_probe.stdout + capabilities_probe.stderr)
                schema = json.loads(schema_probe.stdout)
                capabilities = json.loads(capabilities_probe.stdout)
                self.assertTrue(schema["ok"])
                self.assertTrue(capabilities["ok"])
                self.assertEqual(SCHEMA_NAMES[name], schema["result"]["schema"])
                self.assertEqual("context-owner-capabilities/v1", capabilities["result"]["schema"])
                self.assertTrue(capabilities["result"]["owners"])
                self.assertEqual({name}, {item["owner"] for item in capabilities["result"]["owners"]})
                if name != "context-core":
                    schema_owner = schema["result"].get("owner")
                    if schema_owner is None:
                        schema_owner = schema["result"]["owner_descriptor"]["owner"]
                    self.assertEqual(name, schema_owner)
                    self.assertFalse(schema["result"]["physical_write"])
                self.assertEqual(before, digest_tree(cached))

        self.assertTrue((ROOT / "plugins/context-core/skills/context/SKILL.md").is_file())
        self.assertTrue((ROOT / "plugins/context-decision/skills/decision/SKILL.md").is_file())
        for manifest in sorted(ROOT.glob("plugins/*/.codex-plugin/plugin.json")):
            prompts = read_json(manifest)["interface"]["defaultPrompt"]
            self.assertLessEqual(len(prompts), 3, manifest)
            self.assertTrue(prompts, manifest)
            for prompt in prompts:
                self.assertTrue(prompt.strip(), manifest)
                self.assertLessEqual(len(prompt), 128, f"{manifest}: {prompt}")

        decision_root = ROOT / "plugins/context-decision"
        init_entrypoint = decision_root / "skills/init/scripts/decision_init.py"
        init_skill = (decision_root / "skills/init/SKILL.md").read_text(encoding="utf-8")
        decision_skill = (decision_root / "skills/decision/SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(init_entrypoint.is_file())
        self.assertIn("decision_init.py", init_skill)
        self.assertIn("--core-cli", init_skill)
        for manifest in sorted(ROOT.glob("plugins/*/.codex-plugin/plugin.json")):
            prompts = read_json(manifest)["interface"]["defaultPrompt"]
            self.assertLessEqual(len(prompts), 3, manifest)
            self.assertTrue(prompts, manifest)
            for prompt in prompts:
                self.assertTrue(prompt.strip(), manifest)
                self.assertLessEqual(len(prompt), 128, f"{manifest}: {prompt}")

        decision_skill = (decision_root / "skills/decision/SKILL.md").read_text(encoding="utf-8")
        for token in ("context-common/v2", "partial/invalid", "cache path", "managed block"):
            self.assertIn(token, init_skill)
        for token in ("실제", "conflict", "exact digest", "context-core만 소유"):
            self.assertIn(token, decision_skill)
        for name in PLUGIN_NAMES[1:]:
            semantic_root = ROOT / "plugins" / name
            self.assertFalse((semantic_root / "skills/context").exists())
            self.assertFalse(any(path.name == "context_cli.py" for path in semantic_root.rglob("*.py")))
            owner_source = (semantic_root / OWNER_CLIS[name]).read_text(encoding="utf-8")
            for physical_write in (".write_text(", ".write_bytes(", ".mkdir(", ".unlink(", "os.replace("):
                self.assertNotIn(physical_write, owner_source)

        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        for token in (
            "0.5.0",
            "context-assumption",
            "context-term",
            "local release unit",
            "아직 push",
            "Fresh host live install",
            "중앙 marketplace catalog 배포",
            "아직 미선택",
        ):
            self.assertIn(token, readme)
        self.assertFalse((ROOT / "LICENSE").exists())
        self.assertFalse((ROOT / "wiki").exists())
        migration = (ROOT / "MIGRATION.md").read_text(encoding="utf-8")
        for token in ("0.5.0 additive semantic owners", "context-common/v2", "not rewritten", "not provided"):
            self.assertIn(token, migration)

    def test_forbidden_install_and_host_mutation_calls_are_absent(self) -> None:
        targets = [ROOT / ".claude-plugin/marketplace.json", ROOT / ".agents/plugins/marketplace.json"]
        targets.extend(
            ROOT / "plugins" / name / host / "plugin.json"
            for name in PLUGIN_NAMES
            for host in (".claude-plugin", ".codex-plugin")
        )
        text = "\n".join(path.read_text(encoding="utf-8") for path in targets).casefold()
        for forbidden in (
            "installed_by_default",
            "installedbydefault",
            "implicit_install",
            "implicitinstall",
            "auto_install",
            "auto_enable",
            "auto_update",
        ):
            self.assertNotIn(forbidden, text)

        scripts = tuple(ROOT / "plugins" / name / OWNER_CLIS[name] for name in PLUGIN_NAMES)
        for script in scripts:
            tree = ast.parse(script.read_text(encoding="utf-8"), filename=str(script))
            imported = {
                node.names[0].name.split(".")[0]
                for node in ast.walk(tree)
                if isinstance(node, ast.Import)
            } | {
                node.module.split(".")[0]
                for node in ast.walk(tree)
                if isinstance(node, ast.ImportFrom) and node.module
            }
            self.assertLessEqual(imported - {"__future__", "typing"}, sys.stdlib_module_names)
            for node in ast.walk(tree):
                if not isinstance(node, ast.Call):
                    continue
                call = ast.unparse(node.func)
                self.assertNotIn(call, {"os.system", "subprocess.Popen"})
                if call == "subprocess.run":
                    self.assertTrue(node.args and isinstance(node.args[0], (ast.List, ast.Tuple)))
                    command = node.args[0].elts[0]
                    self.assertIsInstance(command, ast.Constant)
                    self.assertEqual("git", command.value)

        for script in scripts[1:]:
            semantic_source = script.read_text(encoding="utf-8")
            for physical_write in (".write_text(", ".write_bytes(", ".mkdir(", ".unlink(", "os.replace("):
                self.assertNotIn(physical_write, semantic_source)

        all_python = "\n".join(
            path.read_text(encoding="utf-8").casefold()
            for name in PLUGIN_NAMES
            for path in (ROOT / "plugins" / name).rglob("*.py")
        )
        for forbidden_command in (
            "codex plugin add",
            "claude plugin install",
            "plugin marketplace add",
            "auto_install(",
            "auto_enable(",
            "auto_update(",
        ):
            self.assertNotIn(forbidden_command, all_python)


if __name__ == "__main__":
    unittest.main()

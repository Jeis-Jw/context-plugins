#!/usr/bin/env python3
from __future__ import annotations

import ast
import copy
import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PHASE0 = ROOT / "tests/context-v1/phase0/phase0_contract.py"
PLUGIN_NAMES = ("context-core", "context-decision", "context-assumption", "context-term")
RELEASE_VERSION = "0.5.1"
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
BASELINE_SKILL_BYTES = 40_715
UNCHANGED_EXPERIMENTAL_MANIFESTS = {
    "plugins/context-assumption/.claude-plugin/plugin.json": "860fb98c5d941c161b1e07f5f09e0d88e6b958a7690cc401b4d3b5af2b239ada",
    "plugins/context-assumption/.codex-plugin/plugin.json": "870de161652f0855e4f54725aa1354c3a0c3e70bcbc1c95fc2d6212d08b88724",
    "plugins/context-term/.claude-plugin/plugin.json": "478103eda176fa857cb11427e0f31700b329638aec4d6a34332bfc9fbc11ffeb",
    "plugins/context-term/.codex-plugin/plugin.json": "17e34d98b3d2089a0a6e086733cfeb1f675636f6c36e26747287c4fda1da7d91",
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
            "new session",
            "context-decision:init",
        ):
            self.assertIn(token, readme)
        for token in ("install or correct", "reload", "retry", "same init call", "bootstrap"):
            self.assertIn(token, readme)

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
        self.assertEqual(
            "Developer-preview marketplace for Git-backed, approval-gated durable project context.",
            claude_marketplace["metadata"]["description"],
        )
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
            self.assertEqual(RELEASE_VERSION, claude["version"])
            self.assertEqual(claude["version"], codex["version"])
            self.assertEqual(claude["version"], claude_entries[name]["version"])
            self.assertEqual(claude["version"], codex_entries[name]["version"])
            self.assertEqual(claude["description"], claude_entries[name]["description"])
            self.assertEqual(codex["description"], codex_entries[name]["description"])
            self.assertEqual(claude_marketplace["owner"], claude["author"])
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
            self.assertIn(RELEASE_VERSION, plugin_readme)
            if name in {"context-core", "context-decision"}:
                self.assertTrue((root / "README.ko.md").is_file())

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
                    if command[1] == str(init_entrypoint) and name != "context-core":
                        self.assertNotIn("--core-inventory", resolved.stdout)
                        self.assertNotIn("--core-doctor", resolved.stdout)
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
                if name == "context-decision":
                    workflow_entrypoint = cached / "skills/decision/scripts/decision_workflow.py"
                    self.assertTrue(workflow_entrypoint.is_file())
                    workflow_help = subprocess.run(
                        [sys.executable, str(workflow_entrypoint), "preview", "--help"],
                        cwd=temp,
                        env=environment,
                        text=True,
                        capture_output=True,
                    )
                    self.assertEqual(0, workflow_help.returncode, workflow_help.stdout + workflow_help.stderr)
                    self.assertNotIn("--core-inventory", workflow_help.stdout)
                    self.assertNotIn("--core-doctor", workflow_help.stdout)
                self.assertEqual(before, digest_tree(cached))

        self.assertTrue((ROOT / "plugins/context-core/skills/context/SKILL.md").is_file())
        self.assertTrue((ROOT / "plugins/context-decision/skills/decision/SKILL.md").is_file())
        for manifest in sorted(ROOT.glob("plugins/*/.codex-plugin/plugin.json")):
            prompts = read_json(manifest)["interface"]["defaultPrompt"]
            self.assertEqual(3, len(prompts), manifest)
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
            self.assertEqual(3, len(prompts), manifest)
            for prompt in prompts:
                self.assertTrue(prompt.strip(), manifest)
                self.assertLessEqual(len(prompt), 128, f"{manifest}: {prompt}")

        decision_skill = (decision_root / "skills/decision/SKILL.md").read_text(encoding="utf-8")
        for token in ("context-common/v2", "partial/invalid/ready", "scan caches", "managed block"):
            self.assertIn(token, init_skill)
        for token in ("actual", "conflict", "complete rendered", "Core alone owns", "`알겠어`"):
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
            RELEASE_VERSION,
            "context-assumption",
            "context-term",
            "There is no bundle or meta-plugin",
            "tag not created or pushed",
            "Fresh install and cache lifecycle passed",
            "Marketplace publication",
            "Not selected",
        ):
            self.assertIn(token, readme)
        self.assertIn("v0.5.1", readme)
        self.assertIn("--ref v0.5.1", readme)
        self.assertIn("--branch v0.5.1", readme)
        self.assertNotIn("--ref main", readme)
        self.assertTrue((ROOT / "README.ko.md").is_file())
        self.assertFalse((ROOT / "LICENSE").exists())
        self.assertFalse((ROOT / "wiki").exists())
        migration = (ROOT / "MIGRATION.md").read_text(encoding="utf-8")
        for token in ("0.5.0 additive semantic owners", "0.5.1 W1-W3 hardening", "context-common/v2", "not rewritten", "not provided"):
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

    def test_natural_language_approval_contract_is_consistent_and_smaller(self) -> None:
        skill_paths = sorted(ROOT.glob("plugins/*/skills/*/SKILL*.md"))
        self.assertEqual(16, len(skill_paths))
        self.assertLess(
            sum(path.stat().st_size for path in skill_paths),
            BASELINE_SKILL_BYTES,
        )

        for path in skill_paths:
            text = path.read_text(encoding="utf-8")
            self.assertIn("`approval_digest`", text, path)
            self.assertIn("`알겠어`", text, path)
            self.assertTrue(
                "direct, explicit, unconditional" in text
                or "직접적·명시적·무조건적" in text,
                path,
            )
            self.assertTrue(
                "to that capture question" in text or "capture 질문에 대한" in text,
                path,
            )
            self.assertTrue("complete rendered body" in text or "완성된 렌더링 본문" in text, path)
            self.assertTrue("receipt path" in text or "receipt 경로" in text, path)
            self.assertTrue("topic change" in text or "화제 전환" in text, path)
            self.assertTrue("regenerate" in text or "재생성" in text, path)

        readmes = (
            ROOT / "README.md",
            ROOT / "README.ko.md",
            ROOT / "plugins/context-core/README.md",
            ROOT / "plugins/context-core/README.ko.md",
            ROOT / "plugins/context-decision/README.md",
            ROOT / "plugins/context-decision/README.ko.md",
        )
        hidden_user_tokens = (
            "approval_digest",
            "receipt_digest",
            "candidate_id",
            "cand_",
            "plan_id",
            "ctx_",
            "--core-cli",
            "--receipt-file",
            "skills/context/scripts/context_cli.py",
        )
        for path in readmes:
            text = path.read_text(encoding="utf-8")
            for token in hidden_user_tokens:
                self.assertNotIn(token, text, path)
            self.assertNotIn("Delete it manually", text, path)
            self.assertNotIn("Delete the receipt manually", text, path)
            self.assertNotIn("사용자가 직접 삭제", text, path)
            self.assertTrue(
                "direct, explicit, unconditional" in text
                or "직접적·명시적·무조건적" in text,
                path,
            )

        policy_paths = sorted(ROOT.glob("plugins/*/rules/*.md"))
        approval_surfaces = [*skill_paths, *readmes, *policy_paths, ROOT / "AGENTS.md"]
        core_cli = load(
            "context_cli_natural_language_policy",
            ROOT / "plugins/context-core/skills/context/scripts/context_cli.py",
        )
        approval_text = "\n".join(path.read_text(encoding="utf-8") for path in approval_surfaces)
        approval_text += "\n" + core_cli.POLICY_BODY
        for name in ("context-core", "context-decision"):
            approval_text += "\n" + " ".join(
                read_json(ROOT / "plugins" / name / ".codex-plugin/plugin.json")["interface"]["defaultPrompt"]
            )
        forbidden_approval_phrases = re.compile(
            r"exact\s+`?approval_digest`?|exact[-\s]+digest|approval_digest`?\s+(?:approval|승인)",
            re.IGNORECASE,
        )
        self.assertIsNone(forbidden_approval_phrases.search(approval_text))

        english_protocol = (
            ROOT / "plugins/context-decision/skills/decision/references/decision-protocol.md"
        ).read_text(encoding="utf-8")
        korean_protocol = (
            ROOT / "plugins/context-decision/skills/decision/references/decision-protocol.ko.md"
        ).read_text(encoding="utf-8")
        self.assertIn("The owner never invents candidate meaning without caller input", english_protocol)
        self.assertIn("owner는 caller 입력 없이 후보 의미를 지어내지 않는다", korean_protocol)

        for relative, expected in UNCHANGED_EXPERIMENTAL_MANIFESTS.items():
            self.assertEqual(expected, hashlib.sha256((ROOT / relative).read_bytes()).hexdigest(), relative)

    def test_semantic_plugins_pin_the_distributed_core_entrypoint(self) -> None:
        core_cli = ROOT / "plugins/context-core/skills/context/scripts/context_cli.py"
        expected = read_json(ROOT / "tests/context-v1/fixtures/host-inventory/required-plugin.json")
        expected_digest = "sha256:" + hashlib.sha256(core_cli.read_bytes()).hexdigest()
        self.assertEqual("skills/context/scripts/context_cli.py", expected["entrypoint"])
        self.assertEqual(expected_digest, expected["entrypoint_sha256"])

        for name in PLUGIN_NAMES[1:]:
            owner_cli = ROOT / "plugins" / name / OWNER_CLIS[name]
            module = load(f"{name.replace('-', '_')}_distribution_pin", owner_cli)
            self.assertEqual(expected, module.REQUIRED_PLUGIN)
            init_source = (ROOT / "plugins" / name / INIT_ENTRYPOINTS[name]).read_text(encoding="utf-8")
            self.assertIn(".required_core_surface", init_source)
            self.assertNotIn(expected_digest, init_source)

        workflow_source = (
            ROOT / "plugins/context-decision/skills/decision/scripts/decision_workflow.py"
        ).read_text(encoding="utf-8")
        self.assertIn("decision_cli.required_core_surface", workflow_source)
        self.assertNotIn(expected_digest, workflow_source)

    def test_development_and_public_trust_contract_match_the_release_surface(self) -> None:
        version = read_json(ROOT / "plugins/context-core/.claude-plugin/plugin.json")["version"]
        development = (ROOT / "DEVELOPMENT.md").read_text(encoding="utf-8")
        self.assertIn(f"Current repository version: `{version}`", development)
        for name in PLUGIN_NAMES:
            self.assertIn(f"  {name}/", development)
            self.assertIn(f"plugins/{name}/tests", development)
        for token in (
            "shasum -a 256 plugins/context-core/skills/context/scripts/context_cli.py",
            "REQUIRED_PLUGIN.entrypoint_sha256",
            "test_semantic_plugins_pin_the_distributed_core_entrypoint",
            "marketplace provenance",
            "low-level compatibility mode",
        ):
            self.assertIn(token, development)

        for name in ("context-assumption", "context-term"):
            readme = (ROOT / "plugins" / name / "README.md").read_text(encoding="utf-8")
            for token in ("path suffix", "SHA-256", "marketplace provenance", "compatibility", "@file", "8 KiB", "16 KiB"):
                self.assertIn(token, readme)
            self.assertIn("`--candidate @file`", readme)
            self.assertNotIn("--sec-*", readme)
            self.assertNotIn("@@literal", readme)
            prompts = read_json(ROOT / "plugins" / name / ".codex-plugin/plugin.json")["interface"]["defaultPrompt"]
            prompt_text = " ".join(prompts)
            for token in ("pinned context_cli.py", "SHA-256", "marketplace provenance/source/enabled", "low-level compatibility"):
                self.assertIn(token, prompt_text)

        root_readme = (ROOT / "README.md").read_text(encoding="utf-8")
        for token in ("complete preview", "direct, explicit, unconditional", "indexed artifact bodies", "20 bodies", "end-to-end model tokens", "O(1)"):
            self.assertIn(token, root_readme)
        decision_readme = (ROOT / "plugins/context-decision/README.md").read_text(encoding="utf-8")
        for token in ("complete rendered preview", "direct, explicit, unconditional", "zero indexed bodies", "20 bodies", "end-to-end model tokens", "O(1)"):
            self.assertIn(token, decision_readme)

        decision_protocol = (
            ROOT / "plugins/context-decision/skills/decision/references/decision-protocol.md"
        ).read_text(encoding="utf-8")
        for token in ("mode `0600`", "approval_digest", "receipt_digest", "core absolute path/pinned SHA-256"):
            self.assertIn(token, decision_protocol)

        release_notes = (ROOT / "RELEASE_NOTES.md").read_text(encoding="utf-8")
        migration = (ROOT / "MIGRATION.md").read_text(encoding="utf-8")
        for token in ("W1", "W2", "W3", "not a token-savings measurement"):
            self.assertIn(token, release_notes)
        for token in ("W1-W3", "context-common/v2", "linked worktree", "@file", "@@literal"):
            self.assertIn(token, migration)
        for token in (
            "2026-08-23",
            "257 passed, 191 subtests",
            "Phase 0",
            "15 passed each",
            "0.149.0-alpha.4.1",
            "Claude Code `2.1.89`",
            "All four plugins installed and loaded",
            "Actual model behavior",
            "Unverified",
            "not a token-savings claim",
            "core_surface_mismatch",
        ):
            self.assertIn(token, root_readme)

        korean_readme = (ROOT / "README.ko.md").read_text(encoding="utf-8")
        baseline_prompt_chars = 3_147
        prompt_values = [
            prompt
            for name in PLUGIN_NAMES
            for prompt in read_json(ROOT / "plugins" / name / ".codex-plugin/plugin.json")["interface"]["defaultPrompt"]
        ]
        actual_prompt_chars = sum(len(prompt) for prompt in prompt_values)
        reduction_percent = (baseline_prompt_chars - actual_prompt_chars) * 100 / baseline_prompt_chars
        self.assertEqual(12, len(prompt_values))
        self.assertLessEqual(actual_prompt_chars, 1_339)
        english_measurement = (
            f"from {baseline_prompt_chars:,} to {actual_prompt_chars:,} characters, "
            f"a {reduction_percent:.1f}% character reduction"
        )
        self.assertIn(english_measurement, root_readme)
        self.assertIn(english_measurement, release_notes)
        self.assertIn(
            f"{baseline_prompt_chars:,}자에서 {actual_prompt_chars:,}자로 {reduction_percent:.1f}% 감소",
            korean_readme,
        )
        for token in ("complete preview", "직접적·명시적·무조건적", "`알겠어`", "context-common/v2"):
            self.assertIn(token, korean_readme)
        self.assertIn("`0.5.1` developer preview는 local release 후보 commit으로 준비됐습니다", korean_readme)
        self.assertIn("local `0.5.1` release 후보 commit도 아직 push되지 않았고", korean_readme)
        self.assertIn("`v0.5.1` tag는 아직 생성·push되지 않았으며", korean_readme)
        self.assertNotIn("tag와 release commit은 아직 생성·push되지 않았", korean_readme)

    def test_public_help_exposes_capture_limits_and_core_trust(self) -> None:
        environment = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
        workflow = ROOT / "plugins/context-decision/skills/decision/scripts/decision_workflow.py"
        for command in ("preview", "apply"):
            completed = subprocess.run(
                [sys.executable, str(workflow), command, "--help"],
                cwd=ROOT,
                env=environment,
                text=True,
                capture_output=True,
            )
            self.assertEqual(0, completed.returncode, completed.stdout + completed.stderr)
            for token in ("outside the repository", "0600", "approval_digest", "receipt_digest"):
                self.assertIn(token, completed.stdout)

        preview_help = subprocess.run(
            [sys.executable, str(workflow), "preview", "--help"],
            cwd=ROOT,
            env=environment,
            text=True,
            capture_output=True,
            check=True,
        ).stdout
        for token in ("@file", "@@literal", "1,200", "2,000", "8 KiB", "16 KiB"):
            self.assertIn(token, preview_help)

        decision_init = subprocess.run(
            [sys.executable, str(ROOT / "plugins/context-decision" / INIT_ENTRYPOINTS["context-decision"]), "--help"],
            cwd=ROOT,
            env=environment,
            text=True,
            capture_output=True,
            check=True,
        ).stdout
        for token in (
            "path suffix", "SHA-256", "context-common/v2", "required commands",
            "owner-descriptor feature", "doctor state", "does not attest marketplace provenance",
            "low-level compatibility", "@file", "@@literal", "1,200", "2,000", "8 KiB",
            "16 KiB", "0600", "outside the repository", "approval_digest",
        ):
            self.assertIn(token, decision_init)

        for name, label in (("context-assumption", "ASM"), ("context-term", "TERM")):
            init_help = subprocess.run(
                [sys.executable, str(ROOT / "plugins" / name / INIT_ENTRYPOINTS[name]), "--help"],
                cwd=ROOT,
                env=environment,
                text=True,
                capture_output=True,
                check=True,
            ).stdout
            for token in (
                "path suffix", "SHA-256", "context-common/v2", "required commands",
                "owner-descriptor feature", "doctor state", "does not attest marketplace provenance",
                "low-level compatibility", f"{label} claim and decline", "--candidate @file",
                "2,000", "8 KiB", "16 KiB",
            ):
                self.assertIn(token, init_help)
            self.assertNotIn("--sec-", init_help)
            self.assertNotIn("@@literal", init_help)

            claim_help = subprocess.run(
                [sys.executable, str(ROOT / "plugins" / name / OWNER_CLIS[name]), "claim", "--help"],
                cwd=ROOT,
                env=environment,
                text=True,
                capture_output=True,
                check=True,
            ).stdout
            self.assertIn("--candidate @FILE", claim_help)
            self.assertIn("structured candidate JSON input via @file", claim_help)
            self.assertNotIn("--sec-", claim_help)
            self.assertNotIn("@@literal", claim_help)

    def test_addon_test_helpers_use_unique_import_namespaces(self) -> None:
        contracts = {
            "context-assumption": "assumption_test_support",
            "context-term": "term_test_support",
        }
        for plugin, support in contracts.items():
            tests_root = ROOT / "plugins" / plugin / "tests"
            self.assertTrue((tests_root / f"{support}.py").is_file())
            for test_path in tests_root.glob("test_*.py"):
                source = test_path.read_text(encoding="utf-8")
                self.assertNotIn("import helpers", source, test_path)
                self.assertIn(f"import {support} as helpers", source, test_path)


if __name__ == "__main__":
    unittest.main()

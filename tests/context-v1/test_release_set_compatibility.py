from __future__ import annotations

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
CORE_ROOT = ROOT / "plugins/context-core"
CORE_CLI = CORE_ROOT / "skills/context/scripts/context_cli.py"
PLUGIN_NAMES = (
    "context-core",
    "context-decision",
    "context-assumption",
    "context-term",
    "context-intent",
    "context-document",
)
RELEASE_SET_VERSION = "0.14.0"
PLUGIN_VERSIONS = {
    "context-core": "0.14.0",
    "context-decision": "0.13.0",
    "context-assumption": "0.12.0",
    "context-term": "0.12.0",
    "context-intent": "0.12.0",
    "context-document": "0.13.0",
}
CORE_VERSION = PLUGIN_VERSIONS["context-core"]


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


core_cli = load("context_release_set_test_core", CORE_CLI)


def set_plugin_version(root: Path, version: str) -> None:
    for relative in (".claude-plugin/plugin.json", ".codex-plugin/plugin.json"):
        path = root / relative
        manifest = json.loads(path.read_text(encoding="utf-8"))
        manifest["version"] = version
        path.write_text(json.dumps(manifest), encoding="utf-8")


class ReleaseSetCompatibilityTests(unittest.TestCase):
    def test_all_semantic_adapters_share_the_same_candidate_discovery_contract(self) -> None:
        helpers = {
            (ROOT / f"plugins/context-{owner}/skills/{owner}/scripts/core_compatibility.py").read_bytes()
            for owner in ("decision", "assumption", "term", "intent", "document")
        }
        self.assertEqual(1, len(helpers))

    def test_release_set_declares_component_versions_independently(self) -> None:
        self.assertGreater(len(set(PLUGIN_VERSIONS.values())), 1)
        for catalog_path in (
            ROOT / ".claude-plugin/marketplace.json",
            ROOT / ".agents/plugins/marketplace.json",
        ):
            catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
            release_set = catalog["metadata"]["release_set"]
            self.assertEqual("context-plugin-release-set/v1", release_set["schema"])
            self.assertEqual(RELEASE_SET_VERSION, release_set["version"])
            self.assertEqual("same-major-plus-runtime-handshake", release_set["runtime_compatibility"])
            self.assertFalse(release_set["automatic_update"])
            self.assertEqual(PLUGIN_VERSIONS, release_set["members"])

    def test_mixed_pin_handshake_fails_with_a_compatible_candidate_path(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            cache = Path(temp) / "cache"
            intent_root = cache / "context-intent/0.10.0"
            old_core = cache / "context-core/0.6.0"
            compatible_core = cache / f"context-core/{CORE_VERSION}"
            shutil.copytree(ROOT / "plugins/context-intent", intent_root)
            shutil.copytree(CORE_ROOT, old_core)
            shutil.copytree(CORE_ROOT, compatible_core)
            set_plugin_version(old_core, "0.6.0")
            set_plugin_version(compatible_core, CORE_VERSION)
            old_entrypoint = old_core / "skills/context/scripts/context_cli.py"
            old_entrypoint.write_text(
                "#!/usr/bin/env python3\n"
                "import json\n"
                "print(json.dumps({'ok': True, 'result': {"
                "'schema': 'context-core-schema/v1', 'protocol': 'context-common/v2', "
                "'features': ['context-owner-descriptor/v2'], 'commands': ['doctor']}}))\n",
                encoding="utf-8",
            )
            vault = Path(temp) / "vault"
            vault.mkdir()
            completed = subprocess.run(
                [
                    sys.executable,
                    str(intent_root / "skills/init/scripts/intent_init.py"),
                    "--host", "claude-code",
                    "--core-cli", str(old_entrypoint),
                    "--vault", str(vault),
                    "--json",
                ],
                cwd=temp,
                env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
                text=True,
                capture_output=True,
            )
            self.assertEqual(5, completed.returncode, completed.stdout + completed.stderr)
            error = json.loads(completed.stdout)["error"]
            self.assertEqual("core_incompatible", error["code"])
            candidates = error["details"]["compatible_core_candidates"]
            candidate_paths = {item["entrypoint"] for item in candidates}
            self.assertIn(
                str((compatible_core / "skills/context/scripts/context_cli.py").resolve()),
                candidate_paths,
            )
            self.assertNotIn(str(old_entrypoint.resolve()), candidate_paths)
            self.assertTrue(all("runtime handshake required" in item["basis"] for item in candidates))
            self.assertEqual(
                "diagnostic_only_no_automatic_substitution",
                error["details"]["candidate_policy"],
            )
            self.assertFalse((vault / "context").exists(), "failed handshake must not initialize the vault")

    def test_doctor_warns_when_same_major_cache_latest_is_newer(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            container = Path(temp) / "context-core"
            old_core = container / "0.10.0"
            current_core = container / CORE_VERSION
            future_major = container / "1.0.0"
            for root, version in (
                (old_core, "0.10.0"),
                (current_core, CORE_VERSION),
                (future_major, "1.0.0"),
            ):
                shutil.copytree(CORE_ROOT, root)
                set_plugin_version(root, version)
            (container / "incomplete-cache-entry").mkdir()
            warnings = core_cli._cached_core_release_warning(
                old_core / "skills/context/scripts/context_cli.py"
            )
            self.assertEqual(1, len(warnings))
            self.assertEqual("catalog_pin_behind_cache", warnings[0]["code"])
            self.assertEqual("0.10.0", warnings[0]["catalog_version"])
            self.assertEqual(CORE_VERSION, warnings[0]["cache_latest_version"])
            self.assertEqual(
                str((current_core / "skills/context/scripts/context_cli.py").resolve()),
                warnings[0]["compatible_candidate"],
            )
            self.assertIn("runtime handshake required", warnings[0]["compatibility_basis"])


if __name__ == "__main__":
    unittest.main()

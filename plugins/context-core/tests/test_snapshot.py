#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


PLUGIN = Path(__file__).resolve().parents[1]
CLI_PATH = PLUGIN / "skills/context/scripts/context_cli.py"
SPEC = importlib.util.spec_from_file_location("context_cli_snapshot", CLI_PATH)
assert SPEC and SPEC.loader
context_cli = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = context_cli
SPEC.loader.exec_module(context_cli)


def vault_dir() -> tempfile.TemporaryDirectory[str]:
    temp = tempfile.TemporaryDirectory()
    return temp


def tree_digest(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(path for path in root.rglob("*") if path.is_file()):
        digest.update(path.relative_to(root).as_posix().encode())
        digest.update(path.read_bytes())
    return digest.hexdigest()


def initialize(repo: Path) -> None:
    preview = context_cli.build_init_bundle(repo)
    context_cli.apply_bundle(repo, preview["bundle"], preview["approval_digest"])


def run_cli(
    repo: Path,
    *arguments: str,
    environment: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    command_environment = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
    if environment:
        command_environment.update(environment)
    return subprocess.run(
        [sys.executable, str(CLI_PATH), *arguments],
        cwd=repo,
        env=command_environment,
        text=True,
        capture_output=True,
    )


def claim_attestation(candidate: dict, kind: str) -> dict:
    digest = context_cli.canonical_digest(candidate)
    pointers = {
        "snapshot": [
            ("handoff_requested", "/owner_inputs/snapshot/current_context"),
            ("unfinished_context_present", "/owner_inputs/snapshot/open_items/0"),
        ],
        "observation": [
            ("reusable_observation", "/owner_inputs/observation/observation"),
            ("evidence_present", "/owner_inputs/observation/evidence/0"),
        ],
    }
    return {
        "schema": "context-semantic-attestation/v1",
        "operation": "claim",
        "input_schema": candidate["schema"],
        "input_digest": digest,
        "assertions": [
            {"name": name, "value": True, "evidence_pointers": [pointer]}
            for name, pointer in pointers[kind]
        ],
    }


def snapshot_preview(repo: Path, title: str, filename: str | None = None) -> dict:
    candidate = context_cli.direct_candidate(
        "snapshot",
        title=title,
        summary=f"{title} summary",
        captured_from="conversation",
        owner_inputs={
            "current_context": f"{title} context",
            "open_items": [f"{title} open"],
            "next_steps": [f"{title} next"],
        },
    )
    return context_cli.build_snapshot_save_bundle(
        repo,
        candidate,
        claim_attestation(candidate, "snapshot"),
        filename=filename,
        now="2026-08-13T18:20:00+09:00",
    )


class SnapshotTests(unittest.TestCase):
    def test_flag_only_save_freezes_private_receipt_and_applies_once(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            repo = root / "repository"
            private_temp = root / "private-temp"
            repo.mkdir()
            private_temp.mkdir(mode=0o700)
            repo.mkdir(parents=True, exist_ok=True)
            initialize(repo)
            before = tree_digest(repo)

            preview = run_cli(
                repo,
                "snapshot", "save",
                "--title", "인증 handoff",
                "--summary", "unfinished 인증 작업을 재개한다.",
                "--captured-from", "conversation",
                "--attest-handoff-requested",
                "--attest-unfinished-context-present",
                "--sec-context", "인증 callback 구현이 진행 중이다.",
                "--sec-open-items", "public route 회귀를 추가한다.",
                "--sec-next-steps", "focused suite를 실행한다.",
                "--json",
                environment={"TMPDIR": str(private_temp)},
            )

            self.assertEqual(0, preview.returncode, preview.stdout + preview.stderr)
            result = json.loads(preview.stdout)["result"]
            self.assertEqual({"approval_preview", "approval_digest", "receipt_file"}, set(result))
            self.assertEqual(before, tree_digest(repo))
            receipt_path = Path(result["receipt_file"])
            self.assertEqual(0o700, stat.S_IMODE(receipt_path.parent.stat().st_mode))
            self.assertEqual(0o600, stat.S_IMODE(receipt_path.stat().st_mode))
            receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
            self.assertEqual(
                context_cli.canonical_digest({"core": receipt["core"], "plan_bundle": receipt["plan_bundle"]}),
                result["approval_digest"],
            )
            self.assertNotEqual(receipt["receipt_digest"], result["approval_digest"])
            self.assertEqual(
                receipt["plan_id"],
                receipt["plan_bundle"]["approval_material"]["plan"]["plan_id"],
            )
            owner_material_id = receipt["plan_bundle"]["approval_material"]["plan"]["owner_result_material"]
            owner_material = next(
                item for item in receipt["plan_bundle"]["materials"]
                if item["material_id"] == owner_material_id
            )
            owner_result = json.loads(owner_material["content"])
            attestation = next(
                item for item in owner_result["semantic_attestations"]
                if item["operation"] == "claim"
            )
            assertions = {item["name"]: item["evidence_pointers"] for item in attestation["assertions"]}
            self.assertEqual(["/owner_inputs/snapshot/current_context"], assertions["handoff_requested"])
            self.assertEqual(["/owner_inputs/snapshot/open_items/0"], assertions["unfinished_context_present"])

            applied = run_cli(
                repo,
                "transaction", "apply",
                "--receipt-file", str(receipt_path),
                "--approved-digest", result["approval_digest"],
                "--json",
                environment={"TMPDIR": str(private_temp)},
            )
            self.assertEqual(0, applied.returncode, applied.stdout + applied.stderr)
            self.assertTrue(json.loads(applied.stdout)["result"]["applied"])
            self.assertFalse(receipt_path.exists())
            artifacts = [
                path for path in (repo / "context/snapshot").glob("*.md")
                if path.name != "snapshot.index.md"
            ]
            self.assertEqual(1, len(artifacts))

    def test_attestation_file_and_snapshot_flags_are_mutually_exclusive(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            repo = root / "repository"
            private_temp = root / "private-temp"
            repo.mkdir()
            private_temp.mkdir(mode=0o700)
            repo.mkdir(parents=True, exist_ok=True)
            initialize(repo)
            proof = root / "attestation.json"
            proof.write_text("{}", encoding="utf-8")
            before = tree_digest(repo)

            completed = run_cli(
                repo,
                "snapshot", "save",
                "--title", "혼용 차단",
                "--summary", "attestation transport는 하나만 선택한다.",
                "--captured-from", "conversation",
                "--attestation", f"@{proof}",
                "--attest-handoff-requested",
                "--attest-unfinished-context-present",
                "--sec-context", "handoff가 요청됐다.",
                "--sec-open-items", "unfinished task가 남았다.",
                "--sec-next-steps", "회귀를 실행한다.",
                "--json",
                environment={"TMPDIR": str(private_temp)},
            )

            self.assertNotEqual(0, completed.returncode)
            self.assertEqual(before, tree_digest(repo))
            self.assertFalse((private_temp / "context-core").exists())

    def test_snapshot_attestation_flags_require_the_complete_pair_before_write(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            repo = root / "repository"
            private_temp = root / "private-temp"
            repo.mkdir()
            private_temp.mkdir(mode=0o700)
            repo.mkdir(parents=True, exist_ok=True)
            initialize(repo)
            common = [
                "snapshot", "save",
                "--title", "불완전 flags",
                "--summary", "두 semantic assertion이 모두 필요하다.",
                "--captured-from", "conversation",
                "--sec-context", "handoff가 요청됐다.",
                "--sec-open-items", "unfinished task가 남았다.",
                "--sec-next-steps", "회귀를 실행한다.",
            ]
            before = tree_digest(repo)

            for flags in ((), ("--attest-handoff-requested",), ("--attest-unfinished-context-present",)):
                with self.subTest(flags=flags):
                    completed = run_cli(
                        repo,
                        *common,
                        *flags,
                        "--json",
                        environment={"TMPDIR": str(private_temp)},
                    )
                    self.assertNotEqual(0, completed.returncode)
                    self.assertEqual(before, tree_digest(repo))
                    self.assertFalse((private_temp / "context-core").exists())

    def test_acceptance_11_named_snapshots(self) -> None:
        with vault_dir() as temp:
            repo = Path(temp)
            initialize(repo)
            before = tree_digest(repo)
            first = snapshot_preview(repo, "인증 handoff")
            self.assertEqual(before, tree_digest(repo), "preview must not write")
            context_cli.apply_bundle(repo, first["bundle"], first["approval_digest"])
            second = snapshot_preview(repo, "결제 handoff")
            context_cli.apply_bundle(repo, second["bundle"], second["approval_digest"])

            listing = context_cli.snapshot_list(repo)
            self.assertEqual(2, listing["returned"])
            self.assertEqual(2, len({item["id"] for item in listing["items"]}))

            with self.assertRaises(context_cli.ContextError) as caught:
                snapshot_preview(repo, "인증 handoff")
            self.assertEqual("path_exists", caught.exception.code)

    def test_acceptance_12_update_merge(self) -> None:
        with vault_dir() as temp:
            repo = Path(temp)
            initialize(repo)
            create = snapshot_preview(repo, "인증 handoff")
            context_cli.apply_bundle(repo, create["bundle"], create["approval_digest"])
            identifier = create["approval_preview"]["effects"][0]["id"]
            original = context_cli.snapshot_load(repo, identifier)

            with self.assertRaises(context_cli.ContextError) as caught:
                context_cli.build_snapshot_update_bundle(repo, identifier, sections={"현재 맥락": "only"})
            self.assertEqual("snapshot_full_update_required", caught.exception.code)

            merge = context_cli.build_snapshot_update_bundle(
                repo,
                identifier,
                merge=True,
                sections={"열린 항목": "- 새 열린 항목"},
                now="2026-08-13T19:00:00+09:00",
            )
            context_cli.apply_bundle(repo, merge["bundle"], merge["approval_digest"])
            merged = context_cli.snapshot_load(repo, identifier)
            self.assertEqual(original["artifact"]["created_at"], merged["artifact"]["created_at"])
            self.assertEqual("2026-08-13T19:00:00+09:00", merged["artifact"]["updated_at"])
            self.assertEqual(original["sections"]["Current context"], merged["sections"]["Current context"])
            self.assertEqual("- 새 열린 항목", merged["sections"]["Open items"])

            before = tree_digest(repo)
            noop = context_cli.build_snapshot_update_bundle(
                repo,
                identifier,
                merge=True,
                sections={"열린 항목": "- 새 열린 항목"},
                now="2026-08-13T20:00:00+09:00",
            )
            self.assertTrue(noop["noop"])
            self.assertEqual(before, tree_digest(repo))

    def test_snapshot_freshness_is_read_only(self) -> None:
        with vault_dir() as temp:
            repo = Path(temp)
            initialize(repo)
            create = snapshot_preview(repo, "anchor 없는 handoff")
            context_cli.apply_bundle(repo, create["bundle"], create["approval_digest"])
            identifier = create["approval_preview"]["effects"][0]["id"]
            before = tree_digest(repo)
            loaded = context_cli.snapshot_load(repo, identifier)
            self.assertEqual("staging", loaded["authority"])
            self.assertEqual("resume_context", loaded["use_as"])
            self.assertEqual("authority_unknown", loaded["freshness"])
            self.assertEqual(before, tree_digest(repo))

    def test_acceptance_13_discard(self) -> None:
        with vault_dir() as temp:
            repo = Path(temp)
            initialize(repo)
            create = snapshot_preview(repo, "버릴 handoff")
            context_cli.apply_bundle(repo, create["bundle"], create["approval_digest"])
            identifier = create["approval_preview"]["effects"][0]["id"]
            discard = context_cli.build_snapshot_discard_bundle(repo, identifier)
            before = tree_digest(repo)
            with self.assertRaises(context_cli.ContextError) as caught:
                context_cli.apply_bundle(repo, discard["bundle"], "sha256:" + "0" * 64)
            self.assertEqual("approval_digest_mismatch", caught.exception.code)
            self.assertEqual(before, tree_digest(repo))

            context_cli.apply_bundle(repo, discard["bundle"], discard["approval_digest"])
            self.assertEqual(0, context_cli.snapshot_list(repo)["returned"])
            self.assertEqual([], list((repo / "context/snapshot").glob("retired/*.md")))


if __name__ == "__main__":
    unittest.main()

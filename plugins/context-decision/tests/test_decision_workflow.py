#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CORE_CLI = ROOT / "plugins/context-core/skills/context/scripts/context_cli.py"
DECISION_INIT = ROOT / "plugins/context-decision/skills/init/scripts/decision_init.py"
WORKFLOW = ROOT / "plugins/context-decision/skills/decision/scripts/decision_workflow.py"


def run(repo: Path, script: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(script), *arguments],
        cwd=repo,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        text=True,
        capture_output=True,
    )


def canonical_digest(value: object) -> str:
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def digest_tree(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(item for item in root.rglob("*") if item.is_file() and ".git" not in item.parts):
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        digest.update(path.read_bytes())
    return digest.hexdigest()


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")


def repository_identity(repo: Path) -> dict:
    worktree = repo.resolve(strict=True)
    completed = subprocess.run(
        ["git", "rev-parse", "--git-common-dir"],
        cwd=worktree,
        check=True,
        text=True,
        capture_output=True,
    )
    common_value = Path(completed.stdout.strip())
    common = common_value.resolve(strict=True) if common_value.is_absolute() else (worktree / common_value).resolve(strict=True)
    worktree_stat = worktree.stat()
    common_stat = common.stat()
    return {
        "schema": "context-repository-identity/v1",
        "worktree": {"path": str(worktree), "device": str(worktree_stat.st_dev), "inode": str(worktree_stat.st_ino)},
        "git_common_dir": {"path": str(common), "device": str(common_stat.st_dev), "inode": str(common_stat.st_ino)},
    }


class DecisionWorkflowTests(unittest.TestCase):
    def _initialized_repository(self, root: Path) -> tuple[Path, Path]:
        repo = root / "repository"
        repo.mkdir()
        subprocess.run(["git", "init", "-q", str(repo)], check=True)
        (repo / "keep.txt").write_text("repository bytes\n", encoding="utf-8")
        core_init = run(repo, CORE_CLI, "init", "--host", "codex", "--json")
        self.assertEqual(0, core_init.returncode, core_init.stdout + core_init.stderr)
        inventory = root / "inventory.json"
        write_json(
            inventory,
            {
                "plugins": [
                    {
                        "marketplace": "context-plugins",
                        "plugin": "context-core",
                        "source": "Jeis-Jw/context-plugins",
                        "enabled": True,
                        "protocols": ["context-common/v2"],
                    }
                ]
            },
        )
        doctor = run(repo, CORE_CLI, "doctor", "--json")
        self.assertEqual(0, doctor.returncode, doctor.stdout + doctor.stderr)
        doctor_path = root / "doctor.json"
        doctor_path.write_text(doctor.stdout, encoding="utf-8")
        decision_init = run(
            repo,
            DECISION_INIT,
            "--host",
            "codex",
            "--core-inventory",
            f"@{inventory}",
            "--core-doctor",
            f"@{doctor_path}",
            "--core-cli",
            str(CORE_CLI),
            "--json",
        )
        self.assertEqual(0, decision_init.returncode, decision_init.stdout + decision_init.stderr)
        return repo, inventory

    def _semantic_inputs(self, root: Path) -> tuple[Path, Path, dict]:
        candidate = {
            "schema": "context-capture-candidate/v1",
            "candidate_id": "cand_550e8400e29b41d4a716446655440000",
            "title": "인증 세션 소유권",
            "claim": "인증 세션은 BFF가 소유한다.",
            "summary": "OAuth callback과 cookie 경계를 BFF로 통합한다.",
            "captured_from": "conversation",
            "requested_kind": "decision",
            "specialized_kinds": ["decision"],
            "fallback_kind": None,
            "scope_hint": "project/auth",
            "source_refs": [],
            "tags": ["auth"],
            "search_terms": ["session-owner"],
            "evidence": ["결정 권한자가 현재 따를 선택으로 확정했다."],
            "owner_inputs": {
                "decision": {
                    "decision": "인증 세션은 BFF가 소유한다.",
                    "rationale": "브라우저별 cookie 차이를 서버 경계 안으로 모은다.",
                    "rejected_alternatives": ["SPA token 소유: XSS 노출이 커져 반려"],
                    "decision_key": "session-owner",
                }
            },
        }
        attestation = {
            "schema": "context-semantic-attestation/v1",
            "operation": "claim",
            "input_schema": candidate["schema"],
            "input_digest": canonical_digest(candidate),
            "assertions": [
                {"name": "explicit_choice", "value": True, "evidence_pointers": ["/owner_inputs/decision/decision"]},
                {"name": "scope_identified", "value": True, "evidence_pointers": ["/scope_hint"]},
                {"name": "commitment_present", "value": True, "evidence_pointers": ["/evidence/0"]},
            ],
        }
        candidate_path = root / "candidate.json"
        attestation_path = root / "attestation.json"
        write_json(candidate_path, candidate)
        write_json(attestation_path, attestation)
        return candidate_path, attestation_path, candidate

    def _inline_arguments(self) -> list[str]:
        return [
            "--inline",
            "--candidate-id",
            "cand_550e8400e29b41d4a716446655440000",
            "--title",
            "인증 세션 소유권",
            "--summary",
            "OAuth callback과 cookie 경계를 BFF로 통합한다.",
            "--scope",
            "project/auth",
            "--decision-key",
            "session-owner",
            "--captured-from",
            "conversation",
            "--commitment-evidence",
            "결정 권한자가 현재 따를 선택으로 확정했다.",
            "--sec-decision",
            "인증 세션은 BFF가 소유한다.",
            "--sec-rationale",
            "브라우저별 cookie 차이를 서버 경계 안으로 모은다.",
            "--sec-alternatives",
            "SPA token 소유: XSS 노출이 커져 반려",
            "--tag",
            "auth",
            "--search-term",
            "session-owner",
        ]

    def test_preview_freezes_one_bundle_and_apply_uses_only_that_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            repo, inventory = self._initialized_repository(root)
            candidate_path, attestation_path, candidate = self._semantic_inputs(root)
            receipt_path = root / "decision-receipt.json"
            before = digest_tree(repo)
            preview = run(
                repo,
                WORKFLOW,
                "preview",
                "--host",
                "codex",
                "--core-inventory",
                f"@{inventory}",
                "--core-cli",
                str(CORE_CLI),
                "--candidate",
                f"@{candidate_path}",
                "--attestation",
                f"@{attestation_path}",
                "--receipt-file",
                str(receipt_path),
                "--json",
            )
            self.assertEqual(0, preview.returncode, preview.stdout + preview.stderr)
            output = json.loads(preview.stdout)["result"]
            self.assertEqual(before, digest_tree(repo))
            self.assertFalse(output["applied"])
            self.assertEqual(candidate["candidate_id"], output["candidate_id"])
            self.assertNotIn("bundle", output)
            self.assertEqual(0o600, receipt_path.stat().st_mode & 0o777)
            frozen_bytes = receipt_path.read_bytes()
            receipt = json.loads(frozen_bytes)
            workflow_material = receipt["approval_material"]
            self.assertEqual(canonical_digest(candidate), workflow_material["candidate_digest"])
            self.assertEqual(output["approval_digest"], receipt["approval_digest"])
            self.assertEqual(
                output["plan_id"],
                workflow_material["core_bundle"]["approval_material"]["plan"]["plan_id"],
            )
            legacy_output = {
                "ok": True,
                "result": {
                    "bundle": workflow_material["core_bundle"],
                    "approval_preview": output["approval_preview"],
                    "approval_digest": workflow_material["core_approval_digest"],
                    "applied": False,
                    "noop": False,
                },
            }
            legacy_bytes = len(json.dumps(legacy_output, ensure_ascii=False, separators=(",", ":")).encode("utf-8"))
            self.assertLess(len(preview.stdout.encode("utf-8")), legacy_bytes)

            duplicate = run(
                repo,
                WORKFLOW,
                "preview",
                "--host",
                "codex",
                "--core-inventory",
                f"@{inventory}",
                "--core-cli",
                str(CORE_CLI),
                "--candidate",
                f"@{candidate_path}",
                "--attestation",
                f"@{attestation_path}",
                "--receipt-file",
                str(receipt_path),
                "--json",
            )
            self.assertEqual(5, duplicate.returncode, duplicate.stdout + duplicate.stderr)
            self.assertEqual("receipt_exists", json.loads(duplicate.stdout)["error"]["code"])
            self.assertEqual(frozen_bytes, receipt_path.read_bytes())
            self.assertEqual(before, digest_tree(repo))

            rejected = run(
                repo,
                WORKFLOW,
                "apply",
                "--core-cli",
                str(CORE_CLI),
                "--receipt-file",
                str(receipt_path),
                "--approved-digest",
                "sha256:" + "0" * 64,
                "--json",
            )
            self.assertEqual(5, rejected.returncode, rejected.stdout + rejected.stderr)
            self.assertEqual("approval_digest_mismatch", json.loads(rejected.stdout)["error"]["code"])
            self.assertEqual(before, digest_tree(repo))
            self.assertEqual(frozen_bytes, receipt_path.read_bytes())

            applied = run(
                repo,
                WORKFLOW,
                "apply",
                "--core-cli",
                str(CORE_CLI),
                "--receipt-file",
                str(receipt_path),
                "--approved-digest",
                output["approval_digest"],
                "--json",
            )
            self.assertEqual(0, applied.returncode, applied.stdout + applied.stderr)
            applied_result = json.loads(applied.stdout)["result"]
            self.assertTrue(applied_result["applied"])
            self.assertEqual(output["plan_id"], applied_result["plan_id"])
            self.assertEqual(frozen_bytes, receipt_path.read_bytes())
            self.assertNotEqual(before, digest_tree(repo))
            self.assertTrue((repo / output["approval_preview"]["artifacts"][0]["path"]).is_file())

    def test_receipt_is_repository_bound_and_invalid_preflight_writes_nothing(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            repo, inventory = self._initialized_repository(root)
            candidate_path, attestation_path, _ = self._semantic_inputs(root)
            invalid_inventory = root / "invalid-inventory.json"
            write_json(invalid_inventory, {"plugins": []})
            receipt_path = root / "invalid-receipt.json"
            before = digest_tree(repo)
            denied = run(
                repo,
                WORKFLOW,
                "preview",
                "--host",
                "codex",
                "--core-inventory",
                f"@{invalid_inventory}",
                "--core-cli",
                str(CORE_CLI),
                "--candidate",
                f"@{candidate_path}",
                "--attestation",
                f"@{attestation_path}",
                "--receipt-file",
                str(receipt_path),
                "--json",
            )
            self.assertEqual(5, denied.returncode, denied.stdout + denied.stderr)
            self.assertEqual("core_missing", json.loads(denied.stdout)["error"]["code"])
            self.assertFalse(receipt_path.exists())
            self.assertEqual(before, digest_tree(repo))

            inside_receipt = repo / "decision-receipt.json"
            inside = run(
                repo,
                WORKFLOW,
                "preview",
                "--host",
                "codex",
                "--core-inventory",
                f"@{inventory}",
                "--core-cli",
                str(CORE_CLI),
                "--candidate",
                f"@{candidate_path}",
                "--attestation",
                f"@{attestation_path}",
                "--receipt-file",
                str(inside_receipt),
                "--json",
            )
            self.assertEqual(5, inside.returncode, inside.stdout + inside.stderr)
            self.assertEqual("receipt_path_invalid", json.loads(inside.stdout)["error"]["code"])
            self.assertFalse(inside_receipt.exists())
            self.assertEqual(before, digest_tree(repo))

            valid_receipt = root / "valid-receipt.json"
            preview = run(
                repo,
                WORKFLOW,
                "preview",
                "--host",
                "codex",
                "--core-inventory",
                f"@{inventory}",
                "--core-cli",
                str(CORE_CLI),
                "--candidate",
                f"@{candidate_path}",
                "--attestation",
                f"@{attestation_path}",
                "--receipt-file",
                str(valid_receipt),
                "--json",
            )
            self.assertEqual(0, preview.returncode, preview.stdout + preview.stderr)
            approval_digest = json.loads(preview.stdout)["result"]["approval_digest"]
            other = root / "other-repository"
            other.mkdir()
            subprocess.run(["git", "init", "-q", str(other)], check=True)
            mismatch = run(
                other,
                WORKFLOW,
                "apply",
                "--core-cli",
                str(CORE_CLI),
                "--receipt-file",
                str(valid_receipt),
                "--approved-digest",
                approval_digest,
                "--json",
            )
            self.assertEqual(5, mismatch.returncode, mismatch.stdout + mismatch.stderr)
            self.assertEqual("repository_identity_mismatch", json.loads(mismatch.stdout)["error"]["code"])
            self.assertEqual([], [path for path in other.rglob("*") if path.is_file() and ".git" not in path.parts])

    def test_tampered_repository_and_rehashed_receipt_cannot_replay_in_identical_repo(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            first_root = root / "first"
            second_root = root / "second"
            first_root.mkdir()
            second_root.mkdir()
            first, inventory = self._initialized_repository(first_root)
            second, _ = self._initialized_repository(second_root)
            candidate_path, attestation_path, _ = self._semantic_inputs(root)
            receipt_path = root / "replay-receipt.json"
            preview = run(
                first,
                WORKFLOW,
                "preview",
                "--host",
                "codex",
                "--core-inventory",
                f"@{inventory}",
                "--core-cli",
                str(CORE_CLI),
                "--candidate",
                f"@{candidate_path}",
                "--attestation",
                f"@{attestation_path}",
                "--receipt-file",
                str(receipt_path),
                "--json",
            )
            self.assertEqual(0, preview.returncode, preview.stdout + preview.stderr)
            approved_digest = json.loads(preview.stdout)["result"]["approval_digest"]
            receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
            workflow_material = receipt["approval_material"]
            second_identity = repository_identity(second)
            workflow_material["repository_identity"] = second_identity
            core_bundle = workflow_material["core_bundle"]
            core_bundle["approval_material"]["repository_identity"] = second_identity
            core_digest = canonical_digest(core_bundle["approval_material"])
            core_bundle["approval_digest"] = core_digest
            workflow_material["core_approval_digest"] = core_digest
            material = dict(receipt)
            material.pop("receipt_digest")
            receipt["receipt_digest"] = canonical_digest(material)
            write_json(receipt_path, receipt)
            before = digest_tree(second)

            replay = run(
                second,
                WORKFLOW,
                "apply",
                "--core-cli",
                str(CORE_CLI),
                "--receipt-file",
                str(receipt_path),
                "--approved-digest",
                approved_digest,
                "--json",
            )
            self.assertEqual(5, replay.returncode, replay.stdout + replay.stderr)
            self.assertEqual("approval_digest_mismatch", json.loads(replay.stdout)["error"]["code"])
            self.assertEqual(before, digest_tree(second))

    def test_inline_preview_serializes_explicit_semantics_without_input_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            repo, inventory = self._initialized_repository(root)
            receipt_path = root / "inline-receipt.json"
            base = [
                "preview",
                "--host",
                "codex",
                "--core-inventory",
                f"@{inventory}",
                "--core-cli",
                str(CORE_CLI),
                *self._inline_arguments(),
                "--receipt-file",
                str(receipt_path),
                "--json",
            ]
            before = digest_tree(repo)
            unattested = run(repo, WORKFLOW, *base)
            self.assertEqual(5, unattested.returncode, unattested.stdout + unattested.stderr)
            self.assertEqual("semantic_attestation_required", json.loads(unattested.stdout)["error"]["code"])
            self.assertFalse(receipt_path.exists())
            self.assertEqual(before, digest_tree(repo))

            preview = run(
                repo,
                WORKFLOW,
                *base[:-3],
                "--attest-explicit-choice",
                "--attest-scope-identified",
                "--attest-commitment-present",
                *base[-3:],
            )
            self.assertEqual(0, preview.returncode, preview.stdout + preview.stderr)
            output = json.loads(preview.stdout)["result"]
            self.assertEqual("cand_550e8400e29b41d4a716446655440000", output["candidate_id"])
            self.assertFalse(output["applied"])
            self.assertEqual(before, digest_tree(repo))
            self.assertFalse((root / "candidate.json").exists())
            self.assertFalse((root / "attestation.json").exists())
            receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
            self.assertRegex(receipt["approval_material"]["candidate_digest"], r"^sha256:[0-9a-f]{64}$")

            applied = run(
                repo,
                WORKFLOW,
                "apply",
                "--core-cli",
                str(CORE_CLI),
                "--receipt-file",
                str(receipt_path),
                "--approved-digest",
                output["approval_digest"],
                "--json",
            )
            self.assertEqual(0, applied.returncode, applied.stdout + applied.stderr)
            self.assertTrue(json.loads(applied.stdout)["result"]["applied"])

    def test_file_and_inline_inputs_cannot_be_mixed(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            repo, inventory = self._initialized_repository(root)
            receipt_path = root / "mixed-receipt.json"
            mixed = run(
                repo,
                WORKFLOW,
                "preview",
                "--host",
                "codex",
                "--core-inventory",
                f"@{inventory}",
                "--core-cli",
                str(CORE_CLI),
                "--candidate",
                "@/does/not/exist.json",
                "--candidate-id",
                "cand_550e8400e29b41d4a716446655440000",
                "--attestation",
                "@/does/not/exist.json",
                "--receipt-file",
                str(receipt_path),
                "--json",
            )
            self.assertEqual(2, mixed.returncode, mixed.stdout + mixed.stderr)
            self.assertEqual("usage_invalid", json.loads(mixed.stdout)["error"]["code"])
            self.assertFalse(receipt_path.exists())


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


PLUGIN = Path(__file__).resolve().parents[1]
CLI_PATH = PLUGIN / "skills/context/scripts/context_cli.py"
SPEC = importlib.util.spec_from_file_location("context_cli_semantic_transport", CLI_PATH)
assert SPEC and SPEC.loader
context_cli = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = context_cli
SPEC.loader.exec_module(context_cli)


def run_cli(repo: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(CLI_PATH), *arguments],
        cwd=repo,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        text=True,
        capture_output=True,
    )


def write_json(path: Path, value: object) -> Path:
    path.write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")
    return path


def tree_digest(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(item for item in root.rglob("*") if item.is_file() and ".git" not in item.parts):
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        digest.update(path.read_bytes())
    return digest.hexdigest()


def initialize(repo: Path) -> None:
    preview = context_cli.build_init_bundle(repo)
    context_cli.apply_bundle(repo, preview["bundle"], preview["approval_digest"])


def candidate(kind: str, *, mismatch: bool = False) -> dict:
    if kind == "observation":
        primary = "Safari에서 third-party cookie 전달이 차단된다."
        owner_input = {"observation": primary, "evidence": ["integration fixture"]}
    else:
        primary = "인증 handoff 구현과 회귀 검증이 진행 중이다."
        owner_input = {
            "current_context": primary,
            "open_items": ["public route 회귀를 추가한다."],
            "next_steps": ["focused suite를 실행한다."],
        }
    return {
        "schema": "context-capture-candidate/v1",
        "candidate_id": "cand_550e8400e29b41d4a71644665544000" + ("1" if kind == "observation" else "2"),
        "title": "관찰 transport" if kind == "observation" else "handoff transport",
        "claim": "다른 transport claim이다." if mismatch else primary,
        "summary": "built-in semantic transport binding을 검증한다.",
        "captured_from": "workspace",
        "requested_kind": kind,
        "specialized_kinds": [kind],
        "fallback_kind": None,
        "owner_inputs": {kind: owner_input},
    }


def attestation(value: dict, kind: str) -> dict:
    pointers = {
        "observation": (
            ("reusable_observation", "/owner_inputs/observation/observation"),
            ("evidence_present", "/owner_inputs/observation/evidence/0"),
        ),
        "snapshot": (
            ("handoff_requested", "/owner_inputs/snapshot/current_context"),
            ("unfinished_context_present", "/owner_inputs/snapshot/open_items/0"),
        ),
    }
    digest = context_cli.canonical_digest(value)
    return {
        "schema": "context-semantic-attestation/v1",
        "operation": "claim",
        "input_schema": value["schema"],
        "input_digest": digest,
        "assertions": [
            {"name": name, "value": True, "evidence_pointers": [pointer]}
            for name, pointer in pointers[kind]
        ],
    }


def forged_owner_result(kind: str) -> tuple[dict, dict]:
    matching = candidate(kind)
    result = context_cli.draft_owner_result(
        matching,
        attestation(matching, kind),
        now="2026-08-22T12:00:00+09:00",
    )
    forged = copy.deepcopy(result)
    embedded = forged["semantic_inputs"][0]
    embedded["value"]["claim"] = "검증된 owner primary와 다른 재계산된 claim이다."
    embedded["input_digest"] = context_cli.canonical_digest(embedded["value"])
    forged["semantic_attestations"][0]["input_digest"] = embedded["input_digest"]
    return result, forged


def forged_bundle(bundle: dict) -> dict:
    forged = copy.deepcopy(bundle)
    plan = forged["approval_material"]["plan"]
    material = next(item for item in forged["materials"] if item.get("material_id") == plan["owner_result_material"])
    owner_result = json.loads(material["content"])
    embedded = owner_result["semantic_inputs"][0]
    embedded["value"]["claim"] = "승인 bundle 안에서 재계산된 다른 claim이다."
    embedded["input_digest"] = context_cli.canonical_digest(embedded["value"])
    owner_result["semantic_attestations"][0]["input_digest"] = embedded["input_digest"]
    material["content"] = context_cli.canonical_json(owner_result)
    plan["owner_result_digest"] = context_cli.sha256_bytes(material["content"].encode("utf-8"))
    forged["approval_digest"] = context_cli.canonical_digest(forged["approval_material"])
    return forged


def error_code(completed: subprocess.CompletedProcess[str]) -> str:
    if completed.returncode == 0:
        raise AssertionError(completed.stdout + completed.stderr)
    return json.loads(completed.stdout)["error"]["code"]


class SemanticTransportIntegrityTests(unittest.TestCase):
    def test_public_draft_and_batch_route_reject_each_builtin_primary_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            repo = root / "repository"
            repo.mkdir()
            subprocess.run(["git", "init", "-q", str(repo)], check=True)
            capabilities = write_json(root / "capabilities.json", context_cli.capabilities_result())
            results = write_json(root / "results.json", [])
            before = tree_digest(repo)

            for kind in ("observation", "snapshot"):
                with self.subTest(kind=kind):
                    value = candidate(kind, mismatch=True)
                    proof = attestation(value, kind)
                    value_path = write_json(root / f"{kind}-candidate.json", value)
                    proof_path = write_json(root / f"{kind}-attestation.json", proof)
                    batch_path = write_json(root / f"{kind}-batch.json", [value])

                    draft = run_cli(
                        repo,
                        "draft",
                        "--kind", kind,
                        "--candidate", f"@{value_path}",
                        "--attestation", f"@{proof_path}",
                        "--json",
                    )
                    self.assertEqual("candidate_primary_claim_mismatch", error_code(draft))

                    route = run_cli(
                        repo,
                        "candidate", "route",
                        "--batch", f"@{batch_path}",
                        "--capabilities", f"@{capabilities}",
                        "--claim-results", f"@{results}",
                        "--json",
                    )
                    self.assertEqual("candidate_primary_claim_mismatch", error_code(route))
                    self.assertEqual(before, tree_digest(repo))

    def test_matching_builtin_transport_remains_routable(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            repo = root / "repository"
            repo.mkdir()
            subprocess.run(["git", "init", "-q", str(repo)], check=True)
            capabilities = write_json(root / "capabilities.json", context_cli.capabilities_result())

            for kind in ("observation", "snapshot"):
                with self.subTest(kind=kind):
                    value = candidate(kind)
                    value_path = write_json(root / f"matching-{kind}.json", value)
                    proof_path = write_json(root / f"matching-{kind}-attestation.json", attestation(value, kind))
                    draft = run_cli(
                        repo,
                        "draft",
                        "--kind", kind,
                        "--candidate", f"@{value_path}",
                        "--attestation", f"@{proof_path}",
                        "--json",
                    )
                    self.assertEqual(0, draft.returncode, draft.stdout + draft.stderr)
                    owner_result = json.loads(draft.stdout)["result"]
                    batch_path = write_json(root / f"matching-{kind}-batch.json", [value])
                    results_path = write_json(root / f"matching-{kind}-results.json", [owner_result])
                    route = run_cli(
                        repo,
                        "candidate", "route",
                        "--batch", f"@{batch_path}",
                        "--capabilities", f"@{capabilities}",
                        "--claim-results", f"@{results_path}",
                        "--json",
                    )
                    self.assertEqual(0, route.returncode, route.stdout + route.stderr)
                    self.assertEqual("proposed", json.loads(route.stdout)["result"]["routes"][0]["status"])

    def test_rehashed_reviewer_reproducer_fails_finalize_preview_and_apply_without_writes(self) -> None:
        for kind in ("observation", "snapshot"):
            with self.subTest(kind=kind), tempfile.TemporaryDirectory() as temp:
                root = Path(temp)
                repo = root / "repository"
                repo.mkdir()
                subprocess.run(["git", "init", "-q", str(repo)], check=True)
                initialize(repo)
                matching, forged = forged_owner_result(kind)
                before = tree_digest(repo)

                with self.assertRaises(context_cli.ContextError) as caught:
                    context_cli.finalize_owner_result(repo, forged)
                self.assertEqual("candidate_primary_claim_mismatch", caught.exception.code)
                self.assertEqual(before, tree_digest(repo))

                forged_result_path = write_json(root / f"forged-{kind}-result.json", forged)
                preview = run_cli(
                    repo,
                    "transaction", "preview",
                    "--owner-result", f"@{forged_result_path}",
                    "--json",
                )
                self.assertEqual("candidate_primary_claim_mismatch", error_code(preview))
                self.assertEqual(before, tree_digest(repo))

                valid_preview = context_cli.finalize_owner_result(repo, matching)
                replay = forged_bundle(valid_preview["bundle"])
                replay_path = write_json(root / f"forged-{kind}-bundle.json", replay)
                applied = run_cli(
                    repo,
                    "transaction", "apply",
                    "--plan-bundle", f"@{replay_path}",
                    "--approved-digest", replay["approval_digest"],
                    "--json",
                )
                self.assertEqual("candidate_primary_claim_mismatch", error_code(applied))
                self.assertEqual(before, tree_digest(repo))


if __name__ == "__main__":
    unittest.main()

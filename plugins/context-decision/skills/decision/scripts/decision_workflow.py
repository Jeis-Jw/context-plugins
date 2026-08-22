#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import pathlib
import subprocess
import sys
import tempfile
from typing import Any, Sequence

import decision_cli


RECEIPT_SCHEMA = "context-decision-workflow-receipt/v1"
MAX_INPUT_BYTES = 64 * 1024
MAX_RECEIPT_BYTES = 16 * 1024 * 1024


class WorkflowError(Exception):
    def __init__(self, code: str, message: str, details: dict[str, Any] | None = None, exit_code: int = 2):
        super().__init__(message)
        self.code = code
        self.message = message
        self.details = details or {}
        self.exit_code = exit_code

    def envelope(self) -> dict[str, Any]:
        return {"ok": False, "error": {"code": self.code, "message": self.message, "details": self.details}}


class CoreCommandError(Exception):
    def __init__(self, payload: dict[str, Any], exit_code: int):
        super().__init__("context-core command failed")
        self.payload = payload
        self.exit_code = exit_code


def _emit(value: dict[str, Any], *, compact: bool) -> None:
    sys.stdout.write(
        json.dumps(value, ensure_ascii=False, separators=(",", ":")) + "\n"
        if compact
        else json.dumps(value, ensure_ascii=False, indent=2) + "\n"
    )


def _load_json_argument(value: str) -> Any:
    if not value.startswith("@") or value == "@-":
        raise WorkflowError("usage_invalid", "JSON input must use a named @file")
    path = pathlib.Path(value[1:])
    try:
        if path.is_symlink() or path.stat().st_size > MAX_INPUT_BYTES:
            raise WorkflowError("input_unavailable", "JSON input is unsafe or too large", {"path": str(path)}, 5)
        return json.loads(path.read_text(encoding="utf-8"))
    except WorkflowError:
        raise
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise WorkflowError("input_unavailable", "JSON input could not be read", {"path": str(path)}, 3) from error


def _core_cli(value: str) -> pathlib.Path:
    path = pathlib.Path(value).resolve()
    if not path.is_file() or path.name != "context_cli.py":
        raise WorkflowError(
            "core_surface_unavailable",
            "the active installed context-core public CLI was not supplied",
            {"required_plugin": dict(decision_cli.REQUIRED_PLUGIN)},
            5,
        )
    return path


def _file_digest(path: pathlib.Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def _run_core(core_cli: pathlib.Path, repo: pathlib.Path, *arguments: str) -> dict[str, Any]:
    completed = subprocess.run(
        [sys.executable, str(core_cli), *arguments, "--json"],
        cwd=repo,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        text=True,
        capture_output=True,
    )
    try:
        payload = json.loads(completed.stdout)
    except json.JSONDecodeError as error:
        raise WorkflowError(
            "core_result_invalid",
            "context-core returned invalid JSON",
            {"command": " ".join(arguments)},
            7,
        ) from error
    if completed.returncode != 0:
        if not isinstance(payload, dict) or payload.get("ok") is not False:
            raise WorkflowError("core_result_invalid", "context-core error envelope is invalid", exit_code=7)
        raise CoreCommandError(payload, completed.returncode)
    if not isinstance(payload, dict) or payload.get("ok") is not True or not isinstance(payload.get("result"), dict):
        raise WorkflowError("core_result_invalid", "context-core success envelope is invalid", exit_code=7)
    return payload["result"]


def _receipt_path(value: str, repo: pathlib.Path, *, must_exist: bool) -> pathlib.Path:
    requested = pathlib.Path(value)
    if not requested.is_absolute():
        raise WorkflowError("receipt_path_invalid", "receipt file must use an absolute path")
    try:
        parent = requested.parent.resolve(strict=True)
    except OSError as error:
        raise WorkflowError("receipt_path_invalid", "receipt parent is unavailable", {"path": str(requested.parent)}, 3) from error
    path = parent / requested.name
    repository = repo.resolve()
    git_dir_result = subprocess.run(
        ["git", "rev-parse", "--git-common-dir"],
        cwd=repository,
        text=True,
        capture_output=True,
    )
    if git_dir_result.returncode != 0:
        raise WorkflowError("repository_unavailable", "git common directory could not be resolved", exit_code=3)
    git_dir = pathlib.Path(git_dir_result.stdout.strip())
    if not git_dir.is_absolute():
        git_dir = (repository / git_dir).resolve()
    else:
        git_dir = git_dir.resolve()
    if path == repository or repository in path.parents or path == git_dir or git_dir in path.parents:
        raise WorkflowError("receipt_path_invalid", "transient receipt must be outside the repository and Git metadata", {"path": str(path)}, 5)
    if must_exist:
        if path.is_symlink() or not path.is_file():
            raise WorkflowError("receipt_unavailable", "workflow receipt is unavailable", {"path": str(path)}, 3)
    elif path.exists() or path.is_symlink():
        raise WorkflowError("receipt_exists", "workflow receipt already exists; reuse it for apply or choose a new path", {"path": str(path)}, 5)
    return path


def _write_receipt(path: pathlib.Path, receipt: dict[str, Any]) -> None:
    payload = (json.dumps(receipt, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")
    if len(payload) > MAX_RECEIPT_BYTES:
        raise WorkflowError("receipt_too_large", "workflow receipt exceeds 16 MiB", exit_code=5)
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    descriptor: int | None = None
    created = False
    try:
        descriptor = os.open(path, flags, 0o600)
        created = True
        with os.fdopen(descriptor, "wb") as stream:
            descriptor = None
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
    except OSError as error:
        if descriptor is not None:
            os.close(descriptor)
        if created:
            try:
                path.unlink(missing_ok=True)
            except OSError:
                pass
        raise WorkflowError("receipt_write_failed", "workflow receipt could not be written", {"path": str(path)}, 5) from error


def _load_receipt(path: pathlib.Path) -> dict[str, Any]:
    try:
        if path.stat().st_size > MAX_RECEIPT_BYTES:
            raise WorkflowError("receipt_invalid", "workflow receipt exceeds 16 MiB", exit_code=5)
        receipt = json.loads(path.read_text(encoding="utf-8"))
    except WorkflowError:
        raise
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise WorkflowError("receipt_invalid", "workflow receipt could not be read", {"path": str(path)}, 5) from error
    required = {
        "schema", "repository", "core_cli", "core_cli_sha256", "candidate_digest",
        "owner_result_digest", "approval_digest", "bundle", "receipt_digest",
    }
    if not isinstance(receipt, dict) or set(receipt) != required or receipt.get("schema") != RECEIPT_SCHEMA:
        raise WorkflowError("receipt_invalid", "workflow receipt envelope is invalid", exit_code=5)
    material = dict(receipt)
    digest = material.pop("receipt_digest")
    if digest != decision_cli.canonical_digest(material):
        raise WorkflowError("receipt_invalid", "workflow receipt digest is invalid", exit_code=5)
    bundle = receipt.get("bundle")
    if (
        not isinstance(bundle, dict)
        or bundle.get("schema") != "context-mutation-bundle/v1"
        or bundle.get("approval_digest") != receipt.get("approval_digest")
    ):
        raise WorkflowError("receipt_invalid", "workflow receipt bundle binding is invalid", exit_code=5)
    return receipt


def _require_ready_core(host: str, inventory: Any, doctor: dict[str, Any]) -> dict[str, Any]:
    rendered = decision_cli.render_core_preflight(decision_cli.classify_core_preflight(inventory, doctor), host)
    if rendered["code"] != "ready":
        details = {key: value for key, value in rendered.items() if key not in {"code", "message"}}
        raise decision_cli.DecisionError(rendered["code"], rendered["message"], details, decision_cli.EXIT_CONFLICT)
    return rendered


INLINE_FIELDS = (
    "candidate_id",
    "title",
    "summary",
    "scope",
    "decision_key",
    "captured_from",
    "commitment_evidence",
    "sec_decision",
    "sec_rationale",
    "sec_alternatives",
)
ATTESTATION_FLAGS = (
    "attest_explicit_choice",
    "attest_scope_identified",
    "attest_commitment_present",
)


def _semantic_inputs(args: argparse.Namespace) -> tuple[dict[str, Any], dict[str, Any]]:
    if not args.inline:
        inline_values = [
            name
            for name in (*INLINE_FIELDS, "sec_constraints", "sec_tradeoffs", "sec_revisit", "revisit_on", "source_ref", "tag", "search_term", "informed_by", *ATTESTATION_FLAGS)
            if getattr(args, name)
        ]
        if inline_values:
            raise WorkflowError("usage_invalid", "file input cannot be mixed with inline semantic fields", {"fields": inline_values})
        if args.attestation is None:
            raise WorkflowError("usage_invalid", "file input requires --attestation @file")
        return _load_json_argument(args.candidate), _load_json_argument(args.attestation)

    if args.attestation is not None:
        raise WorkflowError("usage_invalid", "inline input cannot be mixed with --attestation")
    missing = [name for name in INLINE_FIELDS if not getattr(args, name)]
    if missing:
        raise WorkflowError("usage_invalid", "inline semantic input is incomplete", {"fields": missing})
    missing_assertions = [name for name in ATTESTATION_FLAGS if not getattr(args, name)]
    if missing_assertions:
        raise WorkflowError(
            "semantic_attestation_required",
            "inline preview requires the caller to explicitly attest all decision claim assertions",
            {"flags": ["--" + name.replace("_", "-") for name in missing_assertions]},
            5,
        )
    candidate = decision_cli.build_direct_candidate(args)
    attestation = {
        "schema": "context-semantic-attestation/v1",
        "operation": "claim",
        "input_schema": candidate["schema"],
        "input_digest": decision_cli.canonical_digest(candidate),
        "assertions": [
            {"name": "explicit_choice", "value": True, "evidence_pointers": ["/owner_inputs/decision/decision"]},
            {"name": "scope_identified", "value": True, "evidence_pointers": ["/scope_hint"]},
            {"name": "commitment_present", "value": True, "evidence_pointers": ["/evidence/0"]},
        ],
    }
    decision_cli.validate_attestation(attestation, candidate, "claim", decision_cli.decision_capability()["claim_assertions"])
    return candidate, attestation


def preview(args: argparse.Namespace) -> dict[str, Any]:
    repo = decision_cli.repository_root().resolve()
    receipt_path = _receipt_path(args.receipt_file, repo, must_exist=False)
    core_cli = _core_cli(args.core_cli)
    core_cli_sha256 = _file_digest(core_cli)
    inventory = _load_json_argument(args.core_inventory)
    candidate, attestation = _semantic_inputs(args)
    doctor = _run_core(core_cli, repo, "doctor")
    preflight = _require_ready_core(args.host, inventory, doctor)
    owner_result = decision_cli.build_claim_result(
        candidate,
        attestation,
        acknowledged_conflicts=args.ack_conflicts,
        repo=repo,
    )
    validation = decision_cli.validate_batch(repo, owner_result)
    with tempfile.TemporaryDirectory(prefix="context-decision-workflow-") as temp:
        root = pathlib.Path(temp)
        owner_path = root / "owner-result.json"
        validation_path = root / "owner-validation.json"
        owner_path.write_text(json.dumps(owner_result, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
        validation_path.write_text(json.dumps(validation, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
        finalized = _run_core(
            core_cli,
            repo,
            "transaction",
            "preview",
            "--owner-result",
            f"@{owner_path}",
            "--owner-validation",
            f"@{validation_path}",
        )
    bundle = finalized.get("bundle")
    approval_digest = finalized.get("approval_digest")
    approval_preview = finalized.get("approval_preview")
    try:
        plan_id = bundle["approval_material"]["plan"]["plan_id"]
    except (KeyError, TypeError) as error:
        raise WorkflowError("core_result_invalid", "context-core preview omitted the exact plan", exit_code=7) from error
    if bundle.get("approval_digest") != approval_digest or not isinstance(approval_preview, dict):
        raise WorkflowError("core_result_invalid", "context-core preview binding is invalid", exit_code=7)
    if _file_digest(core_cli) != core_cli_sha256:
        raise WorkflowError("core_surface_changed", "context-core surface changed during preview; retry", exit_code=5)
    receipt: dict[str, Any] = {
        "schema": RECEIPT_SCHEMA,
        "repository": str(repo),
        "core_cli": str(core_cli),
        "core_cli_sha256": core_cli_sha256,
        "candidate_digest": decision_cli.canonical_digest(candidate),
        "owner_result_digest": decision_cli.canonical_digest(owner_result),
        "approval_digest": approval_digest,
        "bundle": bundle,
    }
    receipt["receipt_digest"] = decision_cli.canonical_digest(receipt)
    _write_receipt(receipt_path, receipt)
    return {
        "schema": "context-decision-workflow-preview/v1",
        "receipt_file": str(receipt_path),
        "receipt_digest": receipt["receipt_digest"],
        "candidate_id": owner_result.get("candidate_id"),
        "approval_preview": approval_preview,
        "approval_digest": approval_digest,
        "plan_id": plan_id,
        "preflight": {"code": preflight["code"], "observed": preflight["observed"]},
        "applied": False,
    }


def apply(args: argparse.Namespace) -> dict[str, Any]:
    repo = decision_cli.repository_root().resolve()
    receipt_path = _receipt_path(args.receipt_file, repo, must_exist=True)
    receipt = _load_receipt(receipt_path)
    if receipt["repository"] != str(repo):
        raise WorkflowError("receipt_repository_mismatch", "workflow receipt belongs to another repository", exit_code=5)
    if args.approved_digest != receipt["approval_digest"]:
        raise WorkflowError("approval_digest_mismatch", "approved digest does not match the frozen workflow receipt", exit_code=5)
    core_cli = _core_cli(args.core_cli)
    if str(core_cli) != receipt["core_cli"] or _file_digest(core_cli) != receipt["core_cli_sha256"]:
        raise WorkflowError("core_surface_changed", "context-core surface changed after preview; create a new preview", exit_code=5)
    with tempfile.TemporaryDirectory(prefix="context-decision-workflow-") as temp:
        bundle_path = pathlib.Path(temp) / "bundle.json"
        bundle_path.write_text(json.dumps(receipt["bundle"], ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
        applied = _run_core(
            core_cli,
            repo,
            "transaction",
            "apply",
            "--plan-bundle",
            f"@{bundle_path}",
            "--approved-digest",
            args.approved_digest,
        )
    return {
        "schema": "context-decision-workflow-apply/v1",
        "receipt_file": str(receipt_path),
        "receipt_digest": receipt["receipt_digest"],
        **applied,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="decision_workflow.py")
    sub = parser.add_subparsers(dest="command", required=True)
    preview_parser = sub.add_parser("preview")
    preview_parser.add_argument("--host", choices=("codex", "claude-code"), required=True)
    preview_parser.add_argument("--core-inventory", required=True)
    preview_parser.add_argument("--core-cli", required=True)
    source = preview_parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--candidate")
    source.add_argument("--inline", action="store_true")
    preview_parser.add_argument("--attestation")
    preview_parser.add_argument("--candidate-id")
    preview_parser.add_argument("--title")
    preview_parser.add_argument("--summary")
    preview_parser.add_argument("--scope")
    preview_parser.add_argument("--decision-key")
    preview_parser.add_argument("--captured-from", choices=("conversation", "workspace", "manual", "import"))
    preview_parser.add_argument("--commitment-evidence", action="append", default=[])
    preview_parser.add_argument("--sec-decision")
    preview_parser.add_argument("--sec-rationale")
    preview_parser.add_argument("--sec-alternatives", action="append", default=[])
    preview_parser.add_argument("--sec-constraints", action="append", default=[])
    preview_parser.add_argument("--sec-tradeoffs", action="append", default=[])
    preview_parser.add_argument("--sec-revisit", action="append", default=[])
    preview_parser.add_argument("--revisit-on")
    preview_parser.add_argument("--source-ref", action="append", default=[])
    preview_parser.add_argument("--tag", action="append", default=[])
    preview_parser.add_argument("--search-term", action="append", default=[])
    preview_parser.add_argument("--informed-by", action="append", default=[])
    preview_parser.add_argument("--attest-explicit-choice", action="store_true")
    preview_parser.add_argument("--attest-scope-identified", action="store_true")
    preview_parser.add_argument("--attest-commitment-present", action="store_true")
    preview_parser.add_argument("--ack-conflicts", action="append", default=[])
    preview_parser.add_argument("--receipt-file", required=True)
    preview_parser.add_argument("--json", action="store_true")
    apply_parser = sub.add_parser("apply")
    apply_parser.add_argument("--core-cli", required=True)
    apply_parser.add_argument("--receipt-file", required=True)
    apply_parser.add_argument("--approved-digest", required=True)
    apply_parser.add_argument("--json", action="store_true")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        result = preview(args) if args.command == "preview" else apply(args)
        _emit({"ok": True, "result": result}, compact=args.json)
        return 0
    except decision_cli.DecisionError as error:
        _emit(error.envelope(), compact=args.json)
        return error.exit_code
    except CoreCommandError as error:
        _emit(error.payload, compact=args.json)
        return error.exit_code
    except WorkflowError as error:
        _emit(error.envelope(), compact=args.json)
        return error.exit_code


if __name__ == "__main__":
    raise SystemExit(main())

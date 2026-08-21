#!/usr/bin/env python3
"""Explicit ASM initialization adapter; repository bytes are delegated to context-core."""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import re
import subprocess
import sys
import tempfile
from typing import Any, Sequence


ASSUMPTION_CLI = pathlib.Path(__file__).resolve().parents[2] / "assumption/scripts/assumption_cli.py"
REQUIRED_FEATURE = "context-owner-descriptor/v2"


def _run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        text=True,
        capture_output=True,
    )


def _emit(value: dict[str, Any], compact: bool) -> None:
    print(json.dumps(value, ensure_ascii=False, separators=(",", ":")) if compact else json.dumps(value, ensure_ascii=False, indent=2))


def _forward(completed: subprocess.CompletedProcess[str]) -> int:
    if completed.stdout:
        sys.stdout.write(completed.stdout)
    if completed.stderr:
        sys.stderr.write(completed.stderr)
    return completed.returncode


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="assumption_init.py")
    parser.add_argument("--host", choices=("codex", "claude-code"), required=True)
    parser.add_argument("--core-inventory", required=True)
    parser.add_argument("--core-doctor", required=True)
    parser.add_argument("--core-cli", required=True)
    parser.add_argument("--json", action="store_true")
    return parser


def _error(code: str, message: str, *, compact: bool, details: dict[str, Any] | None = None) -> int:
    _emit({"ok": False, "error": {"code": code, "message": message, "details": details or {}}}, compact)
    return 5


def _repository_root() -> pathlib.Path:
    completed = _run(["git", "rev-parse", "--show-toplevel"])
    if completed.returncode or not completed.stdout.strip():
        raise ValueError("cwd is not in a Git worktree")
    return pathlib.Path(completed.stdout.strip()).resolve()


def _validate_doctor(doctor: Any) -> dict[str, Any]:
    required = {"schema", "owner", "supported_protocols", "repository_state", "root", "issues", "warnings"}
    if not isinstance(doctor, dict) or set(doctor) != required:
        raise ValueError("core doctor fields differ from context-core-doctor/v1")
    protocols = doctor.get("supported_protocols")
    issues = doctor.get("issues")
    warnings = doctor.get("warnings")
    if (
        doctor.get("schema") != "context-core-doctor/v1"
        or doctor.get("owner") != "context-core"
        or doctor.get("root") != "context/"
        or doctor.get("repository_state") not in {"absent", "partial", "invalid", "ready"}
        or not isinstance(protocols, list)
        or not protocols
        or len(protocols) != len(set(protocols))
        or any(not isinstance(item, str) or not item for item in protocols)
        or not isinstance(issues, list)
        or not isinstance(warnings, list)
    ):
        raise ValueError("core doctor identity or field shape is invalid")
    for diagnostics in (issues, warnings):
        if any(not isinstance(item, dict) or not isinstance(item.get("code"), str) or not item["code"] for item in diagnostics):
            raise ValueError("core doctor diagnostics are invalid")
    if doctor["repository_state"] == "ready" and issues:
        raise ValueError("ready core doctor has issues")
    return doctor


def _postcondition(repo: pathlib.Path, plan: dict[str, Any], doctor: dict[str, Any]) -> dict[str, Any]:
    doctor = _validate_doctor(doctor)
    if (
        doctor.get("repository_state") != "ready"
        or doctor.get("issues") != []
    ):
        raise ValueError("core doctor is not exact ready")
    descriptor = plan["owner_descriptor"]
    descriptor_line = json.dumps(descriptor, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    index_path = repo / "context/assumption/assumption.index.md"
    root_path = repo / "context/context.index.md"
    for path in (repo / "context", repo / "context/assumption", index_path, root_path):
        if path.is_symlink():
            raise ValueError("registered context path is a symlink")
    if not index_path.is_file() or not root_path.is_file():
        raise ValueError("registered index bytes are missing")
    index_text = index_path.read_text(encoding="utf-8")
    begin = "<!-- BEGIN CONTEXT GENERATED:owner-profile -->"
    end = "<!-- END CONTEXT GENERATED:owner-profile -->"
    if index_text.count(begin) != 1 or index_text.count(end) != 1:
        raise ValueError("area owner profile block is missing")
    profile_lines = [line for line in index_text.split(begin, 1)[1].split(end, 1)[0].strip("\n").splitlines() if line]
    if profile_lines != [descriptor_line]:
        raise ValueError("area owner profile differs from init descriptor")
    required_index_tokens = (
        'area: "assumption"',
        'owner: "context-assumption"',
        'artifact_schema: "context-assumption/v1"',
        'authority: "provisional"',
    )
    if any(index_text.count(token) != 1 for token in required_index_tokens):
        raise ValueError("area index identity differs from init descriptor")
    root_text = root_path.read_text(encoding="utf-8")
    profile_value = {
        "area": "assumption",
        "descriptor_schema": "context-owner-descriptor/v2",
        "descriptor_digest": plan["descriptor_digest"],
    }
    profile_row = "<!-- context-owner-profile " + json.dumps(profile_value, ensure_ascii=False, separators=(",", ":")) + " -->"
    if root_text.count(profile_row) != 1:
        raise ValueError("root owner-profile registry differs from init descriptor")
    area_rows = []
    for match in re.finditer(r"<!-- context-area (\{.*?\}) -->", root_text):
        try:
            value = json.loads(match.group(1))
        except json.JSONDecodeError as error:
            raise ValueError("root area row is malformed") from error
        if value.get("area") == "assumption":
            area_rows.append(value)
    expected_area = {
        "area": "assumption",
        "path": "context/assumption/assumption.index.md",
        "owner": "context-assumption",
        "claims": ["assumption"],
        "artifact_schema": "context-assumption/v1",
        "authority": "provisional",
    }
    if area_rows != [expected_area]:
        raise ValueError("root area registry differs from init descriptor")
    return {
        "doctor": "ready",
        "root_registry": "exact",
        "area_descriptor": "exact",
        "index_path": "context/assumption/assumption.index.md",
    }


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    planned = _run([
        sys.executable,
        str(ASSUMPTION_CLI),
        "init",
        "--host",
        args.host,
        "--core-inventory",
        args.core_inventory,
        "--core-doctor",
        args.core_doctor,
        "--json",
    ])
    if planned.returncode:
        return _forward(planned)
    try:
        plan = json.loads(planned.stdout)["result"]
    except (KeyError, TypeError, json.JSONDecodeError):
        return _error("init_plan_invalid", "context-assumption init plan is invalid", compact=args.json, details={"write_policy": {"repository": "none", "host_configuration": "none"}})

    observed_entrypoint = plan.get("active_core_entrypoint")
    supplied = pathlib.Path(args.core_cli)
    observed = pathlib.Path(observed_entrypoint) if isinstance(observed_entrypoint, str) else None
    try:
        core_cli = supplied.resolve(strict=True)
        active_core = observed.resolve(strict=True) if observed is not None else None
    except (OSError, RuntimeError):
        core_cli = supplied.resolve()
        active_core = None
    if (
        not supplied.is_absolute()
        or observed is None
        or not observed.is_absolute()
        or active_core is None
        or core_cli != active_core
        or not core_cli.is_file()
        or core_cli.name != "context_cli.py"
    ):
        return _error("core_surface_unavailable", "the installed context-core public CLI was not supplied", compact=args.json, details={"write_policy": {"repository": "none", "host_configuration": "none"}})

    handshake = _run([sys.executable, str(core_cli), "schema", "--json"])
    if handshake.returncode:
        return _forward(handshake)
    try:
        schema = json.loads(handshake.stdout)["result"]
        features = schema["features"]
    except (KeyError, TypeError, json.JSONDecodeError):
        return _error("core_handshake_invalid", "context-core schema handshake is invalid", compact=args.json, details={"write_policy": {"repository": "none", "host_configuration": "none"}})
    if (
        schema.get("schema") != "context-core-schema/v1"
        or schema.get("protocol") != "context-common/v2"
        or not isinstance(features, list)
        or REQUIRED_FEATURE not in features
    ):
        return _error(
            "core_incompatible",
            "context-core does not advertise context-owner-descriptor/v2",
            compact=args.json,
            details={"required_feature": REQUIRED_FEATURE, "observed_features": features, "write_policy": {"repository": "none", "host_configuration": "none"}},
        )

    with tempfile.TemporaryDirectory(prefix="context-assumption-init-") as temporary:
        temp_root = pathlib.Path(temporary)
        descriptor = temp_root / "descriptor.json"
        seed = temp_root / "assumption.index.md"
        descriptor.write_text(json.dumps(plan["owner_descriptor"], ensure_ascii=False, sort_keys=True, separators=(",", ":")), encoding="utf-8")
        seed.write_text(plan["index_seed"], encoding="utf-8")
        completed = _run([
            sys.executable,
            str(core_cli),
            "bootstrap",
            "--descriptor",
            f"@{descriptor}",
            "--index-seed",
            f"@{seed}",
            "--host",
            args.host,
            "--json",
        ])
    if completed.returncode:
        return _forward(completed)
    try:
        bootstrap = json.loads(completed.stdout)["result"]
    except (KeyError, TypeError, json.JSONDecodeError):
        return _error("core_bootstrap_result_invalid", "context-core bootstrap result is invalid", compact=args.json)
    post_doctor = _run([sys.executable, str(core_cli), "doctor", "--json"])
    if post_doctor.returncode:
        return _forward(post_doctor)
    try:
        doctor = json.loads(post_doctor.stdout)["result"]
        postcondition = _postcondition(_repository_root(), plan, doctor)
    except (KeyError, TypeError, json.JSONDecodeError, OSError, UnicodeError, ValueError) as error:
        return _error(
            "core_bootstrap_postcondition_invalid",
            "context-core reported bootstrap success without exact ASM registration",
            compact=args.json,
            details={"reason": str(error), "required_feature": REQUIRED_FEATURE},
        )
    _emit(
        {
            "ok": True,
            "result": {
                "schema": "context-assumption-init-result/v1",
                "required_feature": REQUIRED_FEATURE,
                "descriptor_digest": plan["descriptor_digest"],
                "core_repository_state_before": plan["core_repository_state"],
                "changed_paths": bootstrap["changed_paths"],
                "phases": bootstrap["phases"],
                "doctor": bootstrap["doctor"],
                "policy": bootstrap["policy"],
                "postcondition": postcondition,
                "bootstrap": bootstrap,
            },
        },
        args.json,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

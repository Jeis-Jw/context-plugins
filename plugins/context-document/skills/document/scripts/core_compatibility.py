from __future__ import annotations

import json
import os
import pathlib
import re
import stat
from typing import Any


ENTRYPOINT = pathlib.PurePosixPath("skills/context/scripts/context_cli.py")
SEMVER = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")


def _version(value: Any) -> tuple[int, int, int] | None:
    if not isinstance(value, str):
        return None
    match = SEMVER.fullmatch(value)
    return tuple(int(part) for part in match.groups()) if match else None


def _containers(current_file: str, supplied_path: str | None) -> list[pathlib.Path]:
    seeds = [pathlib.Path(current_file)]
    if supplied_path:
        seeds.append(pathlib.Path(supplied_path).expanduser())
    found: set[pathlib.Path] = set()
    for seed in seeds:
        try:
            absolute = seed.resolve(strict=False)
        except (OSError, RuntimeError):
            continue
        for parent in (absolute, *absolute.parents):
            if parent.name == "context-core":
                found.add(parent)
            if parent.name.startswith("context-") and parent.name != "context-core":
                found.add(parent.parent / "context-core")
            if parent.name == "plugins":
                found.add(parent / "context-core")
    return sorted(found, key=str)


def _candidate_roots(container: pathlib.Path) -> list[pathlib.Path]:
    roots = [container]
    try:
        metadata = os.lstat(container)
        if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
            return []
        children = list(container.iterdir())
    except OSError:
        return roots
    roots.extend(child for child in children if not child.is_symlink() and child.is_dir())
    return roots


def _candidate(root: pathlib.Path, compatible_major: int, minimum: tuple[int, int, int]) -> dict[str, str] | None:
    versions: set[str] = set()
    try:
        if root.is_symlink() or not root.is_dir():
            return None
        for relative in (".claude-plugin/plugin.json", ".codex-plugin/plugin.json"):
            manifest_path = root / relative
            metadata = os.lstat(manifest_path)
            if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISREG(metadata.st_mode):
                return None
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            if not isinstance(manifest, dict) or manifest.get("name") != "context-core":
                return None
            version = manifest.get("version")
            if _version(version) is None:
                return None
            versions.add(version)
        if len(versions) != 1:
            return None
        version = versions.pop()
        parsed = _version(version)
        if parsed is None or parsed[0] != compatible_major or parsed < minimum:
            return None
        entrypoint = root.joinpath(*ENTRYPOINT.parts)
        metadata = os.lstat(entrypoint)
        if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISREG(metadata.st_mode):
            return None
        return {
            "version": version,
            "entrypoint": str(entrypoint.resolve(strict=True)),
            "basis": "same-major manifests, minimum version, and public entrypoint layout; runtime handshake required",
        }
    except (OSError, RuntimeError, UnicodeError, json.JSONDecodeError):
        return None


def discover_core_candidates(
    current_file: str,
    supplied_path: str | None = None,
    *,
    compatible_major: int = 0,
    minimum_version: str = "0.9.0",
) -> list[dict[str, str]]:
    minimum = _version(minimum_version)
    if minimum is None or minimum[0] != compatible_major:
        return []
    try:
        excluded = pathlib.Path(supplied_path).expanduser().resolve(strict=True) if supplied_path else None
    except (OSError, RuntimeError):
        excluded = None
    by_path: dict[str, dict[str, str]] = {}
    for container in _containers(current_file, supplied_path):
        for root in _candidate_roots(container):
            candidate = _candidate(root, compatible_major, minimum)
            if candidate is None:
                continue
            if excluded is not None and pathlib.Path(candidate["entrypoint"]) == excluded:
                continue
            by_path[candidate["entrypoint"]] = candidate
    return sorted(
        by_path.values(),
        key=lambda item: (_version(item["version"]) or (0, 0, 0), item["entrypoint"]),
        reverse=True,
    )[:8]

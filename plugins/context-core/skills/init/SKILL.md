---
name: init
description: When the user explicitly requests context-core initialization, apply the canonical seed and managed host policy safely and idempotently; never run during ordinary recall or capture.
---

# Init

For an explicit core-only setup, call exactly one of:

```bash
python3 /loaded/context-core/skills/context/scripts/context_cli.py init --host codex --json
python3 /loaded/context-core/skills/context/scripts/context_cli.py init --host claude-code --json
```

An absent repository receives the canonical root, SNAP, and OBS seeds, followed by the active host policy (`codex -> AGENTS.md`, `claude-code -> CLAUDE.md`). A ready repository with the current managed block returns no-op phases and produces no filesystem diff.

Preflight the policy target and markers before every write. Preserve all bytes outside the managed block. A broken/duplicate marker, symlink, nested target, incompatible schema/owner/path, or unsafe partial registration fails with zero writes. If only the root index is missing in an otherwise populated repository, rebuild it solely from exact built-in SNAP/OBS metadata; never claim an unregistered area.

Before addon bootstrap, require `context-owner-descriptor/v2` in the root-independent schema handshake. Pass a canonical descriptor of at most 8 KiB and the exact empty area seed containing its full descriptor block. Mixed v1/v2 roots are allowed, but a registered v2 descriptor digest is immutable. Do not auto-upgrade, downgrade, migrate, delete, or repair unknown trust bytes.

Only none, exact seed-only, exact root-row+profile-registry-only, and complete registration states may converge on retry. This explicit init authorizes only fixed `core_init|area_register|policy_install`; ordinary SNAP, OBS, DEC, or user-content mutation still requires a complete bundle and exact user-approved `approval_digest`.

---
name: init
description: When the user explicitly requests context-core initialization, apply the canonical seed and managed host policy safely and idempotently; never run during ordinary recall or capture.
---

# Init

Only for explicit core setup, call one matching host command:

```bash
python3 /loaded/context-core/skills/context/scripts/context_cli.py init --host codex --json
python3 /loaded/context-core/skills/context/scripts/context_cli.py init --host claude-code --json
```

Absent repositories receive canonical root/SNAP/OBS seeds and the active managed policy (`codex -> AGENTS.md`, `claude-code -> CLAUDE.md`). Ready repositories return no-op phases. Preserve bytes outside managed markers; broken/duplicate markers, symlinks, nested targets, incompatible schema/owner/path, and unsafe partial states fail with zero writes.

Addon bootstrap requires the `context-owner-descriptor/v2` schema feature, a canonical descriptor of at most 8 KiB, and its exact empty area seed. Registered descriptor identity is immutable. Never auto-upgrade, downgrade, migrate, delete, or repair unknown trust bytes. Explicit init authorizes only fixed `core_init|area_register|policy_install` transitions.

Ordinary capture remains separate. Before suggesting it, run preview and ask once with the complete rendered body. Pass preview stdout's `approval_digest` unchanged to apply; never show or request a digest, receipt path, internal ID, or core path. Only a direct, explicit, unconditional affirmative answer to that capture question is approval. `알겠어` alone, a condition, edit request, or topic change is not approval. Never regenerate content or plan after approval.

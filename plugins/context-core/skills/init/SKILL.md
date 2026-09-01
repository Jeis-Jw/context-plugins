---
name: init
description: When explicitly requested, initialize context-core storage and the managed host policy safely and idempotently.
---

# Init

Use the same vault throughout the operation. `--vault DIR` selects an existing directory containing `context/`; otherwise use the nearest current/ancestor directory with a `context` entry, or cwd for a fresh vault. Git is not required. Core/owner/workflow CLIs take `--vault` before the subcommand; init adapters accept it as an option. Relative input paths remain caller-cwd relative.

Only for explicit core setup, call one matching host command:

```bash
python3 /loaded/context-core/skills/context/scripts/context_cli.py init --host codex --json
python3 /loaded/context-core/skills/context/scripts/context_cli.py init --host claude-code --json
```

Absent repositories receive canonical root, SNAP, and OBS seeds plus the active managed policy (`codex -> AGENTS.md`, `claude-code -> CLAUDE.md`). Ready repositories return no-op phases. Preserve bytes outside managed markers; broken or duplicate markers, symlinks, nested targets, incompatible schema, owner, or path, and unsafe partial states fail with zero writes.

Addon bootstrap requires the `context-owner-descriptor/v2` schema feature, a canonical descriptor of at most 8 KiB, and its exact empty area seed. Registered descriptor identity is immutable. Never auto-upgrade, downgrade, migrate, delete, or repair unknown trust bytes. Explicit init authorizes only fixed `core_init|area_register|policy_install` transitions.

Follow the active-language contract in `../context/references/active-language.md`. Use the active language for all user-facing setup guidance and explanatory errors; keep commands, options, schema IDs, error codes, filenames, and metadata in English.

Ordinary capture uses semantic approval, not a rendered-file review. A direct, explicit, unconditional user statement that settles payload, scope, and lifecycle effect authorizes capture; ask one concise question only for unresolved meaning. A generic acknowledgement, condition, edit request, or topic change is not approval. Never show the rendered body or ask a second storage question. After approval, run internal preview and unchanged apply in the same response, keeping `approval_digest`, receipt path, internal ID, and core path private. If preview exposes a semantic delta, hold the write and confirm only that delta. Never regenerate after approval.

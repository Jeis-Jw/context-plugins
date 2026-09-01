---
name: init
description: When explicitly requested, register the DOCUMENT descriptor and index through a same-major context-core handshake.
---

# Context document init

Run only when the user explicitly invokes `$context-document:init`. Use the same filesystem vault throughout; Git is not required. Never install, enable, update, downgrade, import, or migrate another plugin.

```bash
INIT_SKILL_FILE="<loaded-skill-path>/SKILL.md"
python3 "${INIT_SKILL_FILE%/SKILL.md}/scripts/document_init.py" \
  --host codex \
  --core-cli /absolute/path/to/context_cli.py \
  --json
```

The adapter verifies the absolute core entrypoint, matching same-major manifests, schema, protocol, required commands, descriptor feature, filesystem-vault feature, and doctor state. It passes the descriptor and fixed seed to verified core bootstrap, then checks the exact registration. Temporary transport files are its only writes.

Follow context-core's active language contract for user-facing text and keep machine fields English. Before suggesting ordinary capture, run preview and ask once with the complete rendered body. Pass preview stdout's `approval_digest` unchanged to apply, but never expose or request it, a receipt path, an internal ID, or a core path. Approval requires a direct, explicit, unconditional answer to that specific capture question. A generic acknowledgement, condition, edit request, or topic change is not approval. Never regenerate content or plan after approval.

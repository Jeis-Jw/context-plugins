---
name: init
description: When explicitly requested, register the INTENT descriptor and index through a same-major context-core handshake.
---

# Context intent init

Run only when the user explicitly invokes `$context-intent:init`. Use the same filesystem vault throughout; Git is not required. Never install, enable, update, downgrade, import, or migrate another plugin.

```bash
INIT_SKILL_FILE="<loaded-skill-path>/SKILL.md"
python3 "${INIT_SKILL_FILE%/SKILL.md}/scripts/intent_init.py" \
  --host codex \
  --core-cli /absolute/path/to/context_cli.py \
  --json
```

The adapter verifies the absolute core entrypoint, matching same-major manifests, schema, protocol, required commands, descriptor feature, filesystem-vault feature, and doctor state. It passes the descriptor and fixed seed to verified core bootstrap, then checks the exact registration. Temporary transport files are its only writes. On failure, listed manifest-validated sibling core paths are diagnostic only; never substitute or execute one automatically, and start a new session after an explicit choice.

Follow context-core's active language contract for user-facing text and keep machine fields English. Ordinary capture uses a direct, explicit, unconditional user statement that settles payload, scope, and lifecycle effect as semantic approval. Ask only about unresolved meaning; a generic acknowledgement, condition, edit request, or topic change is not approval. Do not show the rendered file body or ask a second storage question. After approval, run internal preview, verify no semantic delta, and pass stdout's `approval_digest` unchanged to apply in the same response. Keep the digest, receipt path, internal ID, and core path private. If a delta appears, hold the write and confirm only that delta. Never regenerate after approval.

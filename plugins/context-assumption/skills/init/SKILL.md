---
name: init
description: When explicitly requested, register the ASM descriptor and index through an exact context-core v2 handshake.
---

# Context assumption init

Run only when the user explicitly invokes `$context-assumption:init`. Never install, enable, update, downgrade, or migrate automatically.

1. Compare the `REQUIRED_PLUGIN` core entrypoint suffix and SHA-256 with the supplied `--core-cli`, then resolve the sibling entrypoint from the loaded catalog.
2. Only the matching core may handshake `context-core-schema/v1`, `context-common/v2`, `context-owner-descriptor/v2`, required commands, and doctor state.
3. `assumption_init.py` sends the descriptor v2 and fixed index seed to core `bootstrap`, then checks ready, profile, index, and managed-policy results.

```bash
INIT_SKILL_FILE="<loaded-skill-path>/SKILL.md"
python3 "${INIT_SKILL_FILE%/SKILL.md}/scripts/assumption_init.py" \
  --host codex \
  --core-cli /absolute/path/to/context_cli.py \
  --json
```

The ASM adapter has no write primitive beyond temporary descriptor and seed transport. It passes `absent|partial|invalid|ready` to the pinned core; a mismatch produces zero subprocess, receipt, or repository writes.

Follow context-core's active-language contract. An explicit user language choice wins; otherwise use the host preference, then established conversation language, then English. OS locale is not authoritative. Use the active language for user-facing setup guidance and explanatory errors; keep machine-readable surfaces in English.

Ordinary durable capture is separate. Before suggesting it, run preview and ask once in the active language with the complete rendered body. Pass preview stdout's `approval_digest` unchanged to apply, but never show or request it, a receipt path, an internal ID, or a core path. Only a direct, explicit, unconditional affirmative answer to that specific capture question is approval. A generic acknowledgement, condition, edit request, or topic change is not. Never regenerate content or plan after approval.

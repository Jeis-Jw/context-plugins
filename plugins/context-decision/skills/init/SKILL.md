---
name: init
description: When explicitly requested, verify the release-pinned context-core and initialize core storage, the DEC area, and the active host policy in one idempotent operation.
---

# Init

Resolve this loaded `SKILL.md`, its sibling `scripts/decision_init.py`, and the separately loaded core entrypoint. Invoke the adapter exactly once:

```bash
INIT_SKILL_FILE="/absolute/path/from-loaded-skill-catalog/plugins/context-decision/skills/init/SKILL.md"
INIT_ENTRYPOINT="${INIT_SKILL_FILE%/SKILL.md}/scripts/decision_init.py"
python3 "$INIT_ENTRYPOINT" \
  --host <codex|claude-code> \
  --core-cli /absolute/active-installed/context-core/skills/context/scripts/context_cli.py \
  --json
```

Claude Code may use `${CLAUDE_PLUGIN_ROOT}` only when supplied by the host; Codex uses the loaded skill catalog. Never infer from cwd, scan caches, or substitute another runtime.

The release-pinned adapter verifies path suffix and SHA-256, then handshakes `context-core-schema/v1`, `context-common/v2`, required commands, `context-owner-descriptor/v2`, and doctor state. Missing/mismatched/incompatible inputs cause zero subprocess, repository, or host-configuration writes. It passes `partial/invalid/ready` or bootstrap-required absent state to core, which owns repairability.

The fixed descriptor/index seed goes to `context_cli.py bootstrap`; core alone applies `core_init|area_register|policy_install`, preserves bytes outside the managed block, and converges retries.

Ordinary capture remains separate. Before suggesting it, run preview and ask once with the complete rendered body. Pass preview stdout's `approval_digest` unchanged to apply; never show or request a digest, receipt path, internal ID, or core path. Only a direct, explicit, unconditional affirmative answer is approval. `알겠어` alone, a condition, edit request, or topic change is not approval. Never regenerate content or plan after approval.

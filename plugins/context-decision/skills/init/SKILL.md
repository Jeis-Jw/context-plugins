---
name: init
description: When explicitly requested, verify the release-pinned context-core and initialize core storage, the DEC area, and the active host policy in one idempotent operation.
---

# Init

Resolve the absolute path of this loaded `SKILL.md`, then its sibling `scripts/decision_init.py`. Resolve the separately loaded core skill to its public `skills/context/scripts/context_cli.py`. Invoke the init adapter exactly once:

```bash
INIT_SKILL_FILE="/absolute/path/from-loaded-skill-catalog/plugins/context-decision/skills/init/SKILL.md"
INIT_ENTRYPOINT="${INIT_SKILL_FILE%/SKILL.md}/scripts/decision_init.py"
python3 "$INIT_ENTRYPOINT" \
  --host <codex|claude-code> \
  --core-cli /absolute/active-installed/context-core/skills/context/scripts/context_cli.py \
  --json
```

Claude Code may use `INIT_SKILL_FILE="${CLAUDE_PLUGIN_ROOT}/skills/init/SKILL.md"` only when the host supplies that plugin root. Codex must use the absolute path from the loaded skill catalog. Do not infer paths from cwd, scan caches, or use `$CLAUDE_PLUGIN_ROOT` as a Codex fallback.

Before subprocess execution, the adapter verifies the release-pinned entrypoint path suffix and SHA-256 from the decision semantic CLI's `REQUIRED_PLUGIN`. It then directly handshakes `context-core-schema/v1`, `context-common/v2`, required doctor/bootstrap/transaction commands, `context-owner-descriptor/v2`, and the current doctor state. This does not attest marketplace provenance, source, scope, or enabled state. Caller inventory/doctor files are low-level compatibility inputs and are not accepted by this canonical init.

A missing path, digest mismatch, or incompatible handshake produces zero subprocess, repository, and host-configuration writes. For absent/partial/invalid/ready doctor states, pass the exact state to the pinned core; core owns repairability and diagnostics.

The adapter passes the fixed descriptor/index seed and explicit host to public `context_cli.py bootstrap --descriptor @file --index-seed @file --host ...`. Core reports `core_init|area_register|policy_install` phases as `applied|noop|failed`, preserves bytes outside the managed block markers, and converges completed phases on retry. No DEC/user-content mutation is authorized without exact digest approval.

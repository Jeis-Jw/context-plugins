---
name: intent
description: When a durable desired project direction emerges, compare, recall, and propose an INTENT lifecycle result without writing vault bytes.
---

# Context intent

This skill is the `context-intent/v1` semantic owner and never writes vault bytes.

- Claim a desired project direction. Decline observed facts, unverified premises, chosen commitments, living-document content, and mixed-owner input.
- Bind claim attestation to the exact candidate and RFC 6901 pointer `/owner_inputs/intent/intent`.
- Treat `(scope, intent_key)` as the exact authoritative Current slot.
- Keep `Success criteria`, `Constraints`, and `Revisit conditions` optional.
- `supersede` requires direct citation of both actual `Intent` bodies, retains the slot, and creates reciprocal lifecycle references.
- Rebuild every complete owner result from live Current bytes and exact semantic input before issuing a receipt.
- Use `search` and `read` for relevant direction recall. Do not require DEC or DOCUMENT to be installed.

Only context-core may preview, approve, lock, CAS, or persist a result. Present the complete rendered body when asking for capture approval and never regenerate it after approval.

The canonical capture path is sibling `scripts/intent_workflow.py preview --host <host> --core-cli <loaded-core-cli> --inline ...`, followed after approval by its `apply` command. The wrapper derives verified manifest inventory and doctor state directly; do not create candidate, attestation, inventory, or doctor JSON files manually. Retain its `receipt_file` and `approval_digest` only in agent state.

Follow context-core's active language contract for user-facing text and keep machine fields English. Before suggesting capture, run preview and ask once with the complete rendered body. Pass preview stdout's `approval_digest` unchanged to apply, but never expose or request it, a receipt path, an internal ID, or a core path. Approval requires a direct, explicit, unconditional answer to that specific capture question. A generic acknowledgement, condition, edit request, or topic change is not approval. Never regenerate content or plan after approval.

See [intent-protocol.md](references/intent-protocol.md).

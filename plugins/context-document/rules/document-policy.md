---
description: Apply the living-document boundary and leave all durable writes to context-core.
alwaysApply: true
---

- Claim current-state Content consumed by an agent or person through recall/envelopes; decline external deliverables and route evidence, premises, direction, and commitments to their owners.
- Preserve the exact `(scope, document_key)` Current slot.
- Update only Content under the same ID, path, slot, and state.
- Re-derive drafts from live source and bound inputs before receipt validation.
- Never add taxonomy, inverse relations, or another lifecycle. Delegate persistence to context-core.
- Treat each slot as one default-read budget; split larger knowledge into stable chapter slots instead of enlarging a slot.
- Follow context-core's active language contract for user-facing text and keep machine fields English.
- The semantic owner never writes vault bytes. A direct, explicit, unconditional user statement that settles payload, scope, and lifecycle effect is semantic approval. Ask only about unresolved meaning; acknowledgement, praise, a condition, edit request, or topic change is not approval. Do not show the rendered file body or ask a second storage question. After approval, run internal preview, verify no semantic delta, and pass its `approval_digest` unchanged to apply in the same response. Keep receipt path, internal ID, and core path private. If a delta appears, hold the write and confirm only that delta. Never regenerate after approval; leave durable mutation to context-core.

---
description: Apply the living-document boundary and leave all durable writes to context-core.
alwaysApply: true
---

- Claim living document Content only; decline evidence, premises, direction, and commitments to their owners.
- Preserve the exact `(scope, document_key)` Current slot.
- Update only Content under the same ID, path, slot, and state.
- Re-derive drafts from live source and bound inputs before receipt validation.
- Never add taxonomy, inverse relations, or another lifecycle. Delegate persistence to context-core.
- Follow context-core's active language contract for user-facing text and keep machine fields English.
- The semantic owner never writes vault bytes. Before proposing capture, run preview and ask once with the complete rendered body. Pass preview stdout's `approval_digest` unchanged to apply, but never expose or request it, a receipt path, an internal ID, or a core path. Only a direct, explicit, unconditional affirmative answer to that specific capture question is approval. A generic acknowledgement, praise, condition, edit request, or topic change is not. Confirm ambiguity once in the active language, never regenerate after approval, and leave durable mutation to context-core.

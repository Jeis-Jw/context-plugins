---
name: document
description: When a living project document needs durable capture or content replacement, propose a DOCUMENT result without writing vault bytes.
---

# Context document

This skill is the `context-document/v1` semantic owner and never writes vault bytes.

- Claim substantive current-state `Content` that an agent or person consumes through recall/envelopes, with an exact `(scope, document_key)` Current slot.
- Decline external deliverables; they remain repository-owned documents outside this context owner.
- Decline evidence, premises, desired direction, chosen commitments, and mixed-owner input.
- Bind claim attestation to exact RFC 6901 pointers for `document_key` and `content`.
- `update` changes only `Content` and `updated_at`; preserve ID, path, scope, document_key, and Current state.
- Treat `document-stale-vs-decision` as a non-blocking freshness signal: review the newer affecting DEC and update Content only when the current state actually changed.
- Rebuild every complete owner result from live Current bytes and exact semantic input before issuing a receipt.
- Do not add taxonomy, subtypes, supersede lifecycle, backlink indexes, or inverse relations.
- Treat each slot as one default-read budget. Split a larger design into stable chapter slots such as `design-skeleton`, `design-envelope`, and `design-rules`; do not enlarge one slot.

Only context-core may preview, approve, lock, CAS, or persist a result. Present the complete rendered body when asking for approval and never regenerate it after approval.

The canonical capture path is sibling `scripts/document_workflow.py preview --host <host> --core-cli <loaded-core-cli> --inline ...`, followed after approval by its `apply` command. The wrapper derives verified manifest inventory and doctor state directly; do not create candidate, attestation, inventory, or doctor JSON files manually. Retain its `receipt_file` and `approval_digest` only in agent state.

Follow context-core's active language contract for user-facing text and keep machine fields English. Before suggesting capture or update, run preview and ask once with the complete rendered body. Pass preview stdout's `approval_digest` unchanged to apply, but never expose or request it, a receipt path, an internal ID, or a core path. Approval requires a direct, explicit, unconditional answer to that specific capture question. A generic acknowledgement, condition, edit request, or topic change is not approval. Never regenerate content or plan after approval.

See [document-protocol.md](references/document-protocol.md).

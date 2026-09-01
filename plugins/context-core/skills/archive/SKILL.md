---
name: archive
description: Preserve immutable long-form source material that has been adopted as evidence for durable context.
---

# Context archive

ARCHIVE is `context-archive/v1` evidence owned by context-core.

- Capture only an immutable source original that supports a durable context record. It is not a deliverable store or a substitute for OBS, DEC, INTENT, or DOCUMENT.
- Require substantive `Content`, at least one `source_ref`, and explicit attestations that the source was adopted as evidence and that the immutable original is present.
- Use `archive preview --content @file ...`, show the complete rendered body, then apply the unchanged receipt and `approval_digest` only after explicit approval.
- ARCHIVE supports capture, read, search, and discard only. It has no update, rename, retire, or supersede operation.
- Keep it out of default recall and pack. Use `archive read|search` or `recall --include-archive` only when the original is actually needed.
- An OBS `Evidence` item may be the exact ARCHIVE `ctx_` ID. Free-form evidence strings remain valid; context-core refresh checks exact IDs.
- Do not discard an archive with inbound internal references.

Follow context-core's active language contract for user-facing text and keep machine fields English. Retain the receipt path and `approval_digest` in agent state, then pass both unchanged to apply. Never expose or ask the user for a digest, receipt path, internal ID, or core path. Only a direct, explicit, unconditional affirmative answer to that specific capture question is approval. A generic acknowledgement, condition, edit request, or topic change is not. Never regenerate content or plan after approval.

See [context-protocol.md](../context/references/context-protocol.md).

---
name: context
description: Audit only the new conversation delta; when durable context can change the answer, recall Current context metadata-first and route mature candidates to the semantic owner.
---

# Context

Audit only the current turn's new meaning, once in the same response pass. With no durable signal, continue silently: no audit status, context call, or capture question. Keep only a session-local ledger of scope/anchor, bodies still present for Current references, and short pending/dismissed/deferred references. Never persist that ledger or re-propose without new evidence.

1. Recall metadata only when prior context can change the judgment. Open only selected actual bodies; a healthy miss never triggers arbitrary body reads.
2. Let the discovered semantic owner compare actual claims, sections, scope, and rationale. Hashes, IDs, and metadata are not semantic evidence. Report conflicts or rationale changes before the primary conclusion.
3. Otherwise finish the request first and propose only mature context, once per milestone. Route through host-discovered capabilities; do not scan caches, start owner processes, or substitute runtimes.
4. Keep the existing limits: eight candidates, 2,000-codepoint common claims, 8 KiB owner input, and a 16 KiB canonical batch envelope.
5. Context-core validates owner results, overlays, structural profiles, lifecycle, indexes, target bytes, repository identity, CAS, lock, and atomic write before applying the frozen bundle. It remains the only physical writer.

Before suggesting capture, run preview and ask once with the complete rendered body. Pass preview stdout's `approval_digest` unchanged to apply; never show or request a digest, receipt path, internal ID, or core path. Only a direct, explicit, unconditional affirmative answer to that capture question is approval. `알겠어` alone, a condition, edit request, or topic change is not approval; confirm ambiguous praise once. Never regenerate the candidate, timestamp, content, or plan after approval.

Audit, recall, route, claim, draft, validation, preview, and a denied apply change no repository or host-policy bytes.

---
name: context
description: Audit only the new conversation delta; recall durable context when it can change the answer and route mature candidates to their semantic owner.
---

# Context

Audit the current turn's new meaning once in the same response pass. With no durable signal, continue silently: do not show audit status, call context tools, or ask a capture question. Keep only a session-local ledger of scope and anchor, Current bodies still present in context, and short pending, dismissed, or deferred references. Never persist that ledger or re-propose a candidate without new evidence.

## Active language

Follow [the active-language contract](references/active-language.md). Runtime instructions are English source, not a forced response language. Use the active language for every user-facing response, question, preview, and explanatory error. Keep machine-readable surfaces in canonical English and preserve artifact prose without semantic translation.

## Workflow

1. Recall metadata only when prior context can change the judgment. Open only selected actual bodies; a healthy miss never triggers arbitrary body reads.
2. Let the discovered semantic owner compare actual claims, sections, scope, and rationale. Hashes, IDs, and metadata are not semantic evidence. Report conflicts or rationale changes before the primary conclusion.
3. Otherwise finish the request first and propose only mature context, once per milestone. Route through host-discovered capabilities; do not scan caches, start owner processes, or substitute runtimes.
4. Keep the existing limits: eight candidates, 2,000-codepoint common claims, 8 KiB owner input, and a 16 KiB canonical batch envelope.
5. Context-core validates owner results, overlays, structural profiles, lifecycle, indexes, target bytes, repository identity, CAS, lock, and atomic write before applying the frozen bundle. It remains the only physical writer.

Before suggesting capture, run preview and ask once in the active language with the complete rendered body. Pass preview stdout's `approval_digest` unchanged to apply; never show or request a digest, receipt path, internal ID, or core path. Approval is semantic and language-independent: only a direct, explicit, unconditional affirmative answer to that specific capture question qualifies. A generic acknowledgement, praise, condition, edit request, or topic change does not. Confirm ambiguity once in the active language. Never regenerate the candidate, timestamp, content, or plan after approval.

Audit, recall, route, claim, draft, validation, preview, and a denied apply change no repository or host-policy bytes.

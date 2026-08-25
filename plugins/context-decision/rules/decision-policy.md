# Decision capture policy

Run only when context-core's incremental audit detects a choice forming or changing. Reuse a Current `{id,sha256}` only while the same scope, anchor, and actual body remain in session context. Otherwise narrow by metadata and read the actual Decision, Rationale, and Rejected alternatives again.

Classify the relation as `new|same|supporting|rationale_changed|conflict`. Hashes, IDs, and metadata are not semantic evidence. Reuse `same|supporting` quietly and report a rationale change or conflict before the primary conclusion.

Include only a mature candidate with an explicit choice, scope, and commitment in one grouped proposal after the original answer. Do not re-propose dismissed or deferred candidates without new evidence. Context-decision returns drafts and validation results but never writes the filesystem.

Follow context-core's active-language contract. Use the active language for user-facing responses, capture questions, previews, and explanatory errors. Keep machine-readable surfaces in English and preserve artifact prose without semantic translation.

Before proposing capture, run preview and ask once with the complete rendered body. Pass preview stdout's `approval_digest` unchanged to apply, but never expose or request it, a receipt path, an internal ID, or a core path. Only a direct, explicit, unconditional affirmative answer to that specific capture question is approval. A generic acknowledgement, praise, condition, edit request, or topic change is not. Confirm ambiguity once in the active language and never regenerate content or plan after approval.

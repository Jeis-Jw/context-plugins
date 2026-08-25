# Active language contract

Runtime instructions are authored in English, but English is not a forced response language.

Resolve the active language for user-facing communication in this order:

1. An explicit user language choice, whether requested for the current response or set as a persistent plugin pin.
2. The host's preferred response language or an applicable system instruction.
3. The established language of the current conversation.
4. English when none of the preceding signals resolves the language.

An explicit request for the current response takes precedence over a persistent pin. A pin only overrides automatic host and conversation detection. OS locale variables such as `LANG` and `LC_ALL` are not authoritative response-language signals. Code, identifiers, filenames, quotations, and an isolated foreign word do not change the established conversation language.

Use the active language for responses, clarification and approval questions, previews, and explanatory error guidance. Keep schema IDs, JSON keys, CLI commands and options, error codes, filenames, metadata field names, and other machine-readable surfaces in canonical English.

Preserve the user's meaning and language in durable artifact prose. Do not translate stored prose merely to match the runtime instruction language. New artifact headings use the canonical English structure; legacy Korean headings remain readable and retain their heading style when an existing artifact is updated.

Approval is semantic and language-independent. Apply a frozen preview only after a direct, explicit, unconditional affirmative answer to that specific capture question. A generic acknowledgement, praise, condition, edit request, or topic change is not approval. Ambiguous approval must be confirmed once in the active language. The agent carries `approval_digest` and receipt details internally and never asks the user to provide them.

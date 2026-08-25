<!-- BEGIN context-core-policy (managed by context-core) -->
## Durable context workflow

- Resolve the active language from an explicit user language choice, then the host's preferred response language or applicable system instruction, then the established conversation language, and finally English. A current-response request overrides a conflicting persistent pin. OS locale is not authoritative. Code, filenames, quotations, and isolated foreign terms do not switch the conversation language.
- Use the active language for responses, capture questions, previews, and explanatory error guidance. Keep machine-readable surfaces in canonical English, including schema IDs, JSON keys, commands and options, error codes, filenames, and metadata fields. Preserve durable artifact prose without semantic translation.
- Audit each user turn's new meaning once. When a choice, premise, or term becomes settled, recall metadata first only if prior context can change the answer. With no durable signal, show no audit status or capture question.
- Let the semantic owner compare relevant actual bodies, scope, and rationale. Report a conflict or rationale change before the primary conclusion.
- Otherwise finish the request first and propose only mature durable candidates, once per milestone. Run preview before proposing and ask once with the complete rendered body.
- Write only after a direct, explicit, unconditional affirmative answer to that specific capture question. Approval is semantic and language-independent. A generic acknowledgement, praise, condition, edit request, or topic change is not approval. Confirm ambiguity once in the active language and never regenerate after approval.
<!-- END context-core-policy (managed by context-core) -->

The agent passes preview stdout's `approval_digest` unchanged to apply and retains frozen-receipt, repository-identity, core-SHA, CAS, lock, and atomic-write checks. Never expose this transport information or ask the user to provide it.

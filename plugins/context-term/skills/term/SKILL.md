---
name: term
description: When a project-specific term can change interpretation, recall, compare, and propose a TERM lifecycle result without writing the repository.
---

# Context term

This skill is the `context-term/v1` semantic owner and never writes repository bytes.

- Claim only a term with an explicit project-specific or project-special definition. Decline generic dictionary meanings, observed facts, committed choices, unverified premises, and mixed-owner input.
- Bind claim attestation to the exact candidate and RFC 6901 pointers `/owner_inputs/term/term` and `/owner_inputs/term/definition`.
- Reject intersecting canonical keys across actual Current term, aliases, and deprecated terms in exact, ancestor, or descendant scopes. Reject overlap within one artifact as well.
- `supersede` requires direct citation of both actual term and Definition bodies as the same project terminology claim. IDs, hashes, fingerprints, and index metadata are not semantic evidence.
- `deprecate` requires a reason; an optional replacement must be a different canonical key. `annotate` may not change semantic fields.
- Use `search` or `read` only after an exact `term-encountered` signal, not automatically for every term.
- Rebuild owner results from live Current source and the candidate or request before issuing a receipt. Read no path outside the canonical area and no symlink component.

For capture, use sibling `scripts/term_workflow.py preview --host <host> --core-cli <loaded-core-cli> --inline ...`, then its `apply` command only after approval. It derives verified inventory and doctor state directly; do not hand-build preflight JSON. Keep its receipt path and approval digest in agent state only.

Follow context-core's active-language contract. An explicit user language choice wins; otherwise use the host preference, then the established conversation language, then English. OS locale is not authoritative, and code, filenames, quotations, or one foreign term do not switch language. Use the active language for user-facing responses, questions, previews, and explanatory errors. Keep machine-readable surfaces in English and preserve artifact prose without semantic translation.

Before suggesting capture, run preview and ask once in the active language with the complete rendered body. Pass preview stdout's `approval_digest` unchanged to apply, but never expose or request it, a receipt path, an internal ID, or a core path. Approval is language-independent and requires a direct, explicit, unconditional affirmative answer to that specific capture question. A generic acknowledgement, praise, condition, edit request, or topic change is not approval. Never regenerate content or plan after approval.

The detailed contract is in [term-protocol.md](references/term-protocol.md).

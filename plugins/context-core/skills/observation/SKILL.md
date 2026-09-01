---
name: observation
description: Preserve reusable facts, evidence, or lessons as non-authoritative OBS context, including its lifecycle operations.
---

# Observation

OBS is an immutable semantic claim with `authority: evidence`; never phrase it as a decision that future work must follow.

1. Capture requires substantive Observation and Evidence content, using only the capability descriptor.
2. `annotate` changes metadata only. Changed claim or evidence meaning requires a successor OBS and `supersede`; prepare both actual claims and keep reciprocal lifecycle edges in one final bundle.
3. `invalidate` requires a substantive disproof reason; `reverify` requires fresh evidence. Age alone does not retire evidence.
4. Keep ID and path, backlink, vault identity, CAS, lock, and atomic-write guards. Preview, prepare, and attestation write nothing.

Follow the active-language contract in `../context/references/active-language.md`. Write user-facing responses, questions, previews, and explanatory errors in the active language. Preserve user-authored artifact prose in its original language; identifiers and machine-readable fields remain English.

Before suggesting capture, run preview and ask once in the active language with the complete rendered body. Retain its receipt path and `approval_digest` in agent state, then pass both unchanged to apply. Receipt self-digests are not approval evidence and no directory scan is allowed. Never show or request a digest, receipt path, ID, or core path. Only a direct, explicit, unconditional affirmative answer to that specific capture question is approval. A generic acknowledgement, praise, condition, edit request, or topic change is not. Never regenerate content or plan after approval. Successful apply removes the receipt; a cleanup-only warning means the write succeeded and must not be retried.

Use `../context/scripts/context_cli.py observation ...`; context-core remains the only writer.

```bash
python3 /loaded/context-core/skills/context/scripts/context_cli.py observation capture --title '<title>' --summary '<summary>' --captured-from workspace --attest-reusable-observation --attest-evidence-present --sec-observation '<claim>' --sec-evidence '<evidence>' --json
python3 /loaded/context-core/skills/context/scripts/context_cli.py transaction apply --receipt-file '<agent-retained result.receipt_file>' --approved-digest '<agent-retained result.approval_digest>' --json
```

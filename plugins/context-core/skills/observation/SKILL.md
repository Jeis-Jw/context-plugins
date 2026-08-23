---
name: observation
description: Preserve reusable facts, evidence, or lessons as non-authoritative OBS context, including preview, lookup, annotation, revalidation, invalidation, supersession, and discard.
---

# Observation

OBS is an immutable semantic claim with `authority: evidence`; never phrase it as a decision that future work must follow.

1. Capture requires substantive Observation and Evidence content, using only the capability descriptor.
2. `annotate` changes metadata only. Changed claim/evidence meaning requires a successor OBS and `supersede`; prepare both actual claims and keep reciprocal lifecycle edges in one final bundle.
3. `invalidate` requires a substantive disproof reason; `reverify` requires fresh evidence. Age alone does not retire evidence.
4. Keep ID/path, backlink, repository identity, CAS, lock, and atomic-write guards. Preview, prepare, and attestation write nothing.

Before suggesting capture, run preview and ask once with the complete rendered body. Retain its receipt path and `approval_digest` in agent state, then pass both unchanged to apply; receipt self-digests are not approval evidence and no directory scan is allowed. Never show or request a digest, receipt path, ID, or core path. Only a direct, explicit, unconditional affirmative answer to that capture question is approval. `알겠어` alone, a condition, edit request, or topic change is not approval. Never regenerate content or plan after approval. Successful apply removes the receipt; a cleanup-only warning means the write succeeded and must not be retried.

Use `../context/scripts/context_cli.py observation ...`; context-core remains the only writer.

```bash
python3 /loaded/context-core/skills/context/scripts/context_cli.py observation capture --title '<title>' --summary '<summary>' --captured-from workspace --attest-reusable-observation --attest-evidence-present --sec-observation '<claim>' --sec-evidence '<evidence>' --json
python3 /loaded/context-core/skills/context/scripts/context_cli.py transaction apply --receipt-file '<agent-retained result.receipt_file>' --approved-digest '<agent-retained result.approval_digest>' --json
```

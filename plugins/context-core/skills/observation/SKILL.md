---
name: observation
description: Preserve reusable facts, evidence, or lessons as non-authoritative OBS context, including preview, lookup, annotation, revalidation, invalidation, supersession, and discard.
---

# Observation

OBS is an immutable semantic claim with `authority: evidence`; never phrase it as a decision that future work must follow.

1. A capture needs a substantive Observation section and at least one substantive Evidence item.
2. Use only the observation descriptor returned by `context_cli.py capabilities --json` to build a bounded candidate and claim attestation.
3. Use `annotate` for title, summary, tags, and search metadata. If claim or evidence meaning changes, create a successor OBS and `supersede` the predecessor.
4. Before supersession, use only the exact old/new `lifecycle prepare` input for `same_claim`; both actual primary claims need evidence pointers.
5. Put successor creation and predecessor History movement in one owner result and one final bundle.
6. Use `invalidate` with a substantive reason for disproof and `reverify` with an evidence reference for a fresh confirmation. Age alone does not retire evidence.
7. Apply only a complete bundle after the user approves its exact digest. Do not bypass exact ID/path or backlink guards.

Use `../context/scripts/context_cli.py observation ...`. Preview, prepare, and attestation do not write the filesystem.

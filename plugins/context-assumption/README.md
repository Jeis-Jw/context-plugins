# context-assumption

[한국어](./README.ko.md)

`context-assumption` owns project-scoped premises that are not yet verified as facts but could change later decisions. Its artifact authority is always `provisional`; it does not replace an OBS finding or a committed DEC choice.

## Canonical artifact structure

- schema: `context-assumption/v1`
- owner/kind: `context-assumption` / `assumption`
- authority: `provisional`
- required H2 sections: `Assumption`, `Basis`
- optional H2 sections: `Confirmation conditions`, `Refutation conditions`
- optional metadata: `impacted_decisions`
- claim gates: `assumption_present`, `unverified_ok`

New artifacts always use the canonical English headings above. Existing repositories may contain the legacy Korean aliases `가정`, `근거`, `확정 조건`, and `반증 조건`; they remain readable and retain their original heading style when round-tripped. The plugin does not silently rewrite or translate stored artifact prose.

A candidate that claims an observed fact like OBS or commits to an action like DEC is declined. Whether two artifacts carry the same claim is determined only by a `same_claim` attestation quoting their actual `Assumption` bodies. IDs, hashes, fingerprints, titles, and index metadata are not semantic identity.

## Lifecycle

- `confirm`: retire the Current artifact to confirmed History with an evidence reference.
- `refute`: retire it to refuted History with a reason, evidence reference, and `impacted_decisions` result. DEC files are not modified.
- `supersede`: require a same-primary-claim attestation and create reciprocal `superseded_by` / `supersedes` edges.
- `annotate`: preserve the primary claim and conditions while changing only descriptive metadata and source references.

`search` and `read` operate only with `--signal assumption-relevant`. Each call reads metadata first; `read` then opens only the selected artifact.

## Storage and trust boundary

The ASM CLI produces artifact drafts, lifecycle owner results, and `context-owner-validation-receipt/v2`. Only `context-core` may resolve repository paths, write artifacts or indexes, lock, perform CAS, create the approval bundle, or apply it. The production ASM CLI contains no filesystem write primitive.

`batch validate` re-reads the live Current source and index and re-derives the transition from the candidate, attestation, and mutation request. It issues a receipt only when the exact owner result matches. Source paths must remain inside canonical `context/assumption` containment with no symlink component.

Explicit `$context-assumption:init` accepts only an absolute core CLI with the expected entrypoint suffix, matching adjacent Claude/Codex manifests, and the same major version. It computes the actual entrypoint SHA-256 and holds it constant while directly verifying the core schema, protocol, required commands, `context-owner-descriptor/v2`, and doctor state before passing the descriptor and seed to core bootstrap. It does not attest marketplace provenance or installation scope, and it never installs, updates, downgrades, or migrates plugins automatically.

The common primary-claim ceiling is 2,000 codepoints and ASM `assumption` is limited to 1,200 codepoints. Candidate and batch envelopes are bounded to 16 KiB canonical UTF-8, owner input to 8 KiB, candidate count to eight, and public output to 32 KiB. Normal operations require exact `repository_state=ready`; explicit init may repair `partial`, while `invalid` always fails closed.

## Public CLI

```bash
python3 skills/assumption/scripts/assumption_cli.py schema --json
python3 skills/assumption/scripts/assumption_cli.py capabilities --json
python3 skills/assumption/scripts/assumption_cli.py search \
  --signal assumption-relevant --query "deployment premise" \
  --host codex --core-inventory @inventory.json --core-doctor @doctor.json --json
```

Low-level non-static compatibility commands require caller-provided host inventory and a doctor receipt. Canonical init performs its own handshake through `--core-cli`.

Structured claim and decline inputs use the explicit `--candidate @file` surface; the CLI does not infer a candidate from free-form body flags.

Runtime responses, questions, previews, and explanatory guidance follow the active language. Schema IDs, JSON keys, CLI options, error codes, filenames, and metadata fields remain English.

Version `0.9.0` keeps ASM as an optional semantic-owner package outside the `core-decision` installation profile and adopts same-major core compatibility. The `v0.9.0` tag and marketplace publication are still pending.

Version `0.10.0` aligns the six-plugin distribution version; ASM semantics and stored bytes are unchanged. No tag or publication is implied.

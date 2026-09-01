# context-term

[한국어](./README.ko.md)

`context-term` owns terminology whose meaning is specific to a project. Its artifacts are `authoritative`; they do not replace OBS findings, DEC choices, or ASM premises.

## Canonical artifact structure

- schema: `context-term/v1`
- owner/kind: `context-term` / `term`
- authority: `authoritative`
- required frontmatter: `scope`, `term`, and derived `term_key`
- required H2 section: `Definition`
- optional metadata: `aliases`, `deprecated_terms`, `related`
- claim gates: `term_identified`, `definition_present`, and explicit `project-specific` or `project-special-meaning`

New artifacts always use the canonical English `Definition` heading. Existing repositories may contain the legacy Korean alias `정의`; it remains readable and retains its original heading when round-tripped. The plugin does not silently rewrite headings or translate stored prose.

General dictionary meanings and OBS, DEC, or ASM candidates are declined. `term_key` is derived deterministically using Unicode NFKC, case folding, and whitespace/punctuation normalization. The canonical-key sets of actual `term`, `aliases`, and `deprecated_terms` values may not overlap within one artifact or across exact, ancestor, and descendant Current scopes.

Whether two artifacts carry the same claim is determined only by a `same_claim` attestation quoting both their actual `term` values and `Definition` bodies. IDs, hashes, fingerprints, titles, and index metadata are not semantic identity.

## Lifecycle

- `supersede`: require actual term/definition attestation for the same `(scope, term_key)` and create reciprocal `superseded_by` / `supersedes` edges.
- `deprecate`: retire to History with a required reason. A replacement term is optional and cannot occupy the same canonical slot.
- `annotate`: preserve term, key, definition, aliases, deprecated terms, and relations while changing only descriptive metadata and source references.

`search` and `read` operate only when an actual ambiguous or project-specific term triggered `--signal term-encountered`. The plugin does not query every word or candidate. Each call reads metadata first; `read` then opens only the selected artifact.

## Storage and trust boundary

The TERM CLI produces artifact drafts, lifecycle owner results, and `context-owner-validation-receipt/v2`. Only `context-core` may resolve repository paths, write artifacts or indexes, lock, perform CAS, create the approval bundle, or apply it. The production TERM CLI contains no filesystem write primitive.

`batch validate` re-reads the live Current source and index and re-derives the transition from the candidate, attestation, and mutation request. It issues a receipt only when the exact owner result matches. Source paths must remain inside canonical `context/term` containment with no symlink component.

Explicit `$context-term:init` accepts only an absolute core CLI with the expected entrypoint suffix, matching adjacent Claude/Codex manifests, and the same major version. It computes the actual entrypoint SHA-256 and holds it constant while directly verifying the core schema, protocol, required commands, `context-owner-descriptor/v2`, and doctor state before passing the descriptor and seed to core bootstrap. It does not attest marketplace provenance or installation scope, and it never installs, updates, downgrades, or migrates plugins automatically.

The common primary claim and TERM `definition` are limited to 2,000 codepoints. Candidate and batch envelopes are bounded to 16 KiB canonical UTF-8, owner input to 8 KiB, and public output to 32 KiB. Lifecycle timestamps cannot precede the source `created_at`. Normal operations require exact `repository_state=ready`; explicit init may repair `partial`, while `invalid` always fails closed.

## Public CLI

```bash
python3 skills/term/scripts/term_cli.py schema --json
python3 skills/term/scripts/term_cli.py capabilities --json
python3 skills/term/scripts/term_cli.py search \
  --signal term-encountered --query "BFF" \
  --host codex --core-inventory @inventory.json --core-doctor @doctor.json --json
```

Low-level non-static compatibility commands require caller-provided host inventory and a doctor receipt. Canonical init performs its own handshake through `--core-cli`.

Structured claim and decline inputs use the explicit `--candidate @file` surface; the CLI does not infer a candidate from free-form body flags.

Runtime responses, questions, previews, and explanatory guidance follow the active language. Schema IDs, JSON keys, CLI options, error codes, filenames, and metadata fields remain English.

Version `0.9.0` keeps TERM as an optional semantic-owner package outside the `core-decision` installation profile and adopts same-major core compatibility. The `v0.9.0` tag and marketplace publication are still pending.

Version `0.10.0` aligns the six-plugin distribution version; TERM semantics and stored bytes are unchanged. No tag or publication is implied.

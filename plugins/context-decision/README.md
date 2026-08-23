# context-decision

`context-decision` preserves decision continuity: what the project chose, why it chose it, which alternatives it rejected, and when a newer DEC superseded the old one. Current DEC documents are authoritative; history is marked `do_not_follow`.

## Supported developer-preview path

1. Install `context-core@context-plugins` and `context-decision@context-plugins` separately from the immutable `v0.5.1` checkout.
2. Reload the host or open a new session.
3. Run `$context-decision:init` once in the target Git repository.

There is no bundle or meta-plugin. The init adapter uses the separately installed core to create or repair core storage, register the DEC area, and install one managed policy block. Re-running it against a ready repository is a no-op. The `v0.5.1` tag is not published yet; installation and publication remain owner-gated.

Core and decision must come from the same immutable release checkout. Decision pins the exact core entrypoint bytes, so a mixed or partially updated install fails with `core_surface_mismatch`; update or reinstall both together, reload the host, and retry.

## Executable trust boundary

Before any core subprocess, canonical init and workflow verify that the supplied absolute `--core-cli` matches the release-pinned `skills/context/scripts/context_cli.py` path suffix and SHA-256. Only then do they handshake:

- `schema=context-core-schema/v1`
- `protocol=context-common/v2`
- required doctor, bootstrap, and transaction preview/apply commands
- `context-owner-descriptor/v2`
- the exact doctor field shape and current repository state

This verifies the executable release contract. It does **not** attest marketplace provenance, catalog source, installation scope, or host enabled state. Caller-created `--core-inventory @file` and `--core-doctor @file` remain available only for low-level compatibility operations; canonical init and the DEC workflow do not use them.

The low-level inventory preflight may report `core_missing`, `core_source_mismatch`, `core_disabled`, `core_incompatible`, `core_uninitialized`, or `ready`. For the first four, install or correct `context-core@context-plugins` from `Jeis-Jw/context-plugins` in the intended scope, reload or open a new session, and retry `context-decision:init`. `core_uninitialized` is not an install failure: the same init call invokes core bootstrap for both core and DEC.

## Decision flow

Core audits each conversation delta once and routes here only when a choice is forming or changing. `check` narrows candidates from index metadata and returns the selected Current DEC bodies. The agent compares the actual decision, rationale, rejected alternatives, and scope; hashes, IDs, fingerprints, and index metadata are not semantic evidence.

- `same`: reuse the Current DEC without duplicate capture.
- `supporting`: keep the DEC and consider durable new evidence as OBS.
- `rationale_changed`: report the changed rationale before the primary conclusion.
- `conflict`: report the incompatible choices before the primary conclusion.
- `new`: no related DEC was found in the returned candidate set; this is not a global proof.

Only an explicit choice with canonical scope and commitment evidence may become a DEC candidate. Dismissed or deferred candidates are not proposed again without new evidence.

## Golden capture workflow

The normal single-decision path is `decision_workflow.py preview --inline`, followed by `apply` only after the user approves the exact digest. The caller supplies every semantic field and explicitly attests `explicit_choice`, `scope_identified`, and `commitment_present`; the CLI serializes those claims but does not invent evidence or judgment.

The preview writes one sensitive frozen receipt to a new absolute path outside the repository and Git metadata with mode `0600`. The stdout `approval_digest` is the user-facing exact approval and binds repository identity, pinned core absolute path/SHA, candidate/result digests, and the nested core bundle/digest. `receipt_digest` detects damage but cannot replace approval. Delete the receipt manually after the workflow.

Clone replay, linked-worktree replay, same-path repository recreation, receipt tampering, core changes, and a wrong digest all fail before repository writes. Apply forwards the unchanged nested bundle to core and does not regenerate IDs, timestamps, content, or plans.

Inline `--sec-*` values are literals by default. `@file` reads a named regular UTF-8 file and `@@literal` preserves one leading `@`; path-like plain text stays literal. Missing, symlinked, or oversized files fail before receipt or repository writes.

- DEC `decision`: 1,200 codepoints
- common primary-claim protocol ceiling: 2,000 codepoints
- built-in SNAP `current_context` and OBS `observation`: 1,200 codepoints each
- canonical owner input: 8 KiB
- full candidate envelope: 16 KiB

Advanced lifecycle, explicit decline, and prebuilt semantic inputs retain the low-level `candidate prepare`, `capture --candidate @file --attestation @file`, and `batch validate` surfaces.

## Recall and spec view

A healthy index miss opens zero indexed bodies; missing or stale index recovery opens at most 20 bodies per recall. Hard bounds cover body materialization/open, selected output, candidate/envelope, and owner input. Index scoring/directory enumeration and end-to-end model tokens are not O(1).

`spec-view --scope <scope>` selects exact, strict-ancestor, and strict-descendant Current DEC entries from metadata, then materializes only their `Decision` and `Rationale` semantic sections in deterministic `(created_at,id)` order. History and `do_not_follow` entries are excluded. The complete JSON stdout, including its final newline, is at most 32 KiB; overflowing trailing entries are omitted whole and reported by count.

Existing DEC bytes and `context-common/v2` remain compatible. ASM and TERM are optional experimental owners and are not installed, enabled, initialized, or migrated automatically.

See the [owner protocol](./skills/decision/references/decision-protocol.md), [root release status](../../README.md), and [한국어 문서](./README.ko.md).

# context-decision

`context-decision` preserves decision continuity: what the project chose, why it chose it, which alternatives it rejected, and when a newer DEC superseded the old one. Current DEC documents are authoritative; history is marked `do_not_follow`.

## Supported developer-preview path

1. From the immutable `v0.6.0` checkout, run the root `core-decision` profile installer once. It installs `context-core@context-plugins` and `context-decision@context-plugins` as separate packages.
2. Reload the host or open a new session.
3. Run `$context-decision:init` once in the target Git repository.

There is no bundle or meta-plugin, and decision code is not embedded in core. The root installer is explicit distribution tooling; this plugin never changes host installation state. The init adapter uses the separately installed core to create or repair core storage, register the DEC area, and install one managed policy block. Re-running it against a ready repository is a no-op. The `v0.6.0` tag is not published yet; tag creation and publication remain owner-gated.

Core and decision must come from the same immutable release checkout. Decision pins the exact core entrypoint bytes, so a mixed or partially updated install fails with `core_surface_mismatch`; update or reinstall both together, reload the host, and retry.

## Executable trust boundary

Before any core subprocess, canonical init and workflow verify the release-pinned core runtime. Only then do they handshake:

- `schema=context-core-schema/v1`
- `protocol=context-common/v2`
- required doctor, bootstrap, and transaction preview/apply commands
- `context-owner-descriptor/v2`
- the exact doctor field shape and current repository state

This verifies the executable release contract. It does **not** attest marketplace provenance, catalog source, installation scope, or host enabled state. Inventory and doctor files remain available only for low-level compatibility operations; canonical init and the DEC workflow do not ask users to provide them.

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

The agent prepares one complete rendered preview before asking whether to record it. A write is allowed only after a direct, explicit, unconditional affirmative answer to that capture question. `알겠어` alone, a condition, an edit request, or a topic change is not approval; ambiguous praise is confirmed once. A requested edit produces a new preview and a new question.

Users never see or enter digests, temporary-file locations, internal IDs, or core paths. The CLI still receives caller-provided semantic fields and attestations; it serializes them but never invents evidence or judgment.

The workflow freezes repository identity, pinned runtime, semantic result, nested core bundle, CAS, and lock bindings before asking and never regenerates them after approval. Clone replay, linked-worktree replay, same-path repository recreation, tampering, runtime changes, and wrong approval material fail before repository writes.

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

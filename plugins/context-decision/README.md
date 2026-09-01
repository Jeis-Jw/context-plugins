# context-decision

`context-decision` preserves decision continuity: what the project chose, why it chose it, which alternatives it rejected, and when a newer DEC superseded the old one. Current DEC documents are authoritative; history is marked `do_not_follow`.

DEC remains standalone: an Intent is optional. Existing artifacts keep descriptor v1, required `Decision`, `Rationale`, and `Rejected alternatives` sections, legacy untyped `informed_by`, and their existing bytes. New candidates may additionally supply `serves_intents`, `informed_by_observations`, `informed_by_assumptions`, and `affects_documents`; DEC projects them to `serves:intent`, `informed_by:observation`, `informed_by:assumption`, and `affects:document`. Core validates that typed targets exist and have the declared kind.

## Supported developer-preview path

1. Run the root `core-decision` profile installer once from the downloaded plugin files. It installs missing profile plugins and accepts enabled same-major installations as compatible.
2. Reload the host or open a new session.
3. Run `$context-decision:init` once in the target vault directory.

There is no bundle or meta-plugin, and decision code is not embedded in core. The root installer is explicit distribution tooling; this plugin never changes host installation state. The init adapter uses the separately installed core to create or repair core storage, register the DEC area, and install one managed policy block. Re-running it against a ready repository is a no-op. The `v0.11.0` tag is not published yet; tag creation and publication remain owner-gated.

Core and decision package versions are compatible when their major versions match. Minor versions add or change functionality and patch versions contain small fixes; for the current `0.x` line, any `0.*` pair passes the package-version gate. The runtime handshake below still rejects a same-major implementation whose actual surface is incompatible.

## Executable trust boundary

Before any core subprocess, canonical init and workflow verify the absolute entrypoint suffix, matching adjacent Claude/Codex core manifests, and the compatible major. They compute the actual entrypoint SHA-256 and hold it constant through the operation. Only then do they handshake:

- `schema=context-core-schema/v1`
- `protocol=context-common/v2`
- required doctor, bootstrap, and transaction preview/apply commands
- `context-owner-descriptor/v2` and `filesystem-vault/v1`
- `typed-relations/v1` when the candidate actually contains a typed relation input
- the exact doctor field shape and current repository state

Standalone and legacy-untyped DEC operations retain the prior same-major handshake; only typed relation use needs the additive Core feature. This verifies the executable compatibility contract. It does **not** attest marketplace provenance, catalog source, installation scope, or host enabled state. Inventory and doctor files remain available only for low-level compatibility operations; canonical init and the DEC workflow do not ask users to provide them.

The low-level inventory preflight may report `core_missing`, `core_source_mismatch`, `core_disabled`, `core_incompatible`, `core_uninitialized`, or `ready`. For the first four, install or correct `context-core@context-plugins` from `Jeis-Jw/context-plugins` in the intended scope, reload or open a new session, and retry `context-decision:init`. `core_uninitialized` is not an install failure: the same init call invokes core bootstrap for both core and DEC.

## Decision flow

Core audits each conversation delta once and routes here only when a choice is forming or changing. With known scope/key, one exact `check` narrows candidates from index metadata and returns the selected Current DEC's actual `Decision`, `Rationale`, `Rejected alternatives`, and non-empty `Revisit conditions` under `sections`. Reuse that result in the turn without another context read. Hashes, IDs, fingerprints, and index metadata are not semantic evidence.

- `same`: reuse the Current DEC without duplicate capture.
- `supporting`: keep the DEC and consider durable new evidence as OBS.
- `rationale_changed`: quote every returned non-empty actual section before the primary conclusion, then hold and ask an explicit binary question: keep means the action is not performed; supersede permits it only after that explicit choice.
- `conflict`: quote every returned non-empty actual Decision, Rationale, Rejected alternatives, and Revisit conditions section before the primary conclusion; state the selected condition token verbatim as `satisfied|no evidence|ambiguous` without inventing evidence, then hold and ask the same explicit binary question: keep means the action is not performed; supersede permits it only after that explicit choice. `satisfied` requires user-supplied present facts that directly establish the stored condition; the requested conflicting action itself is not evidence. Facts that are absent or concern something other than the stored condition mean `no evidence`; `ambiguous` requires relevant but incomplete or conflicting condition facts.
- `new`: no related DEC was found in the returned candidate set; this is not a global proof.

Only an explicit choice with canonical scope and commitment evidence may become a DEC candidate. A satisfied revisit condition authorizes reassessment, not implementation, and durable capture still needs separate approval. Dismissed or deferred candidates are not proposed again without new evidence.

## Golden capture workflow

The agent prepares one complete rendered preview before asking whether to record it. A write is allowed only after a direct, explicit, unconditional affirmative answer to that capture question. `알겠어` alone, a condition, an edit request, or a topic change is not approval; ambiguous praise is confirmed once. A requested edit produces a new preview and a new question.

Users never see or enter digests, temporary-file locations, internal IDs, or core paths. The CLI still receives caller-provided semantic fields and attestations; it serializes them but never invents evidence or judgment.

The workflow freezes vault identity, pinned runtime, semantic result, nested core bundle, CAS, and lock bindings before asking and never regenerates them after approval. Replay in a copied or moved vault, same-path directory recreation, tampering, runtime changes, and wrong approval material fail before repository writes.

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

Version `0.9.0` introduces the major-based package compatibility policy and keeps protocol/capability handshakes plus operation-bound actual runtime digests as the fail-closed execution boundary.

Version `0.10.0` adds optional typed relation inputs while preserving standalone decisions and legacy artifact bytes. No tag or publication is implied.

Version `0.11.0` aligns the release set, lists compatible core candidates only after handshake failure, and clarifies revisit and repeated relation inputs. DEC semantics and stored bytes are unchanged. No tag or publication is implied.

See the [owner protocol](./skills/decision/references/decision-protocol.md), [root release status](../../README.md), and [한국어 문서](./README.ko.md).

# context-decision/v1 owner protocol

`decision_cli.py` is the semantic owner of `context-decision/v1`. It builds complete DEC drafts, lifecycle effects, `context-owner-plan/v1`, `context-owner-validation-receipt/v1`, and bounded recall. It never creates directories, writes files or indexes, locks repositories, seals final approval digests, or applies bundles. Context-core is the only physical coordinator.

## Dependency and executable boundary

- marketplace: `context-plugins`
- plugin: `context-core`
- selector: `context-core@context-plugins`
- repository source: `Jeis-Jw/context-plugins`
- protocol: `context-common/v2`
- core entrypoint suffix: `skills/context/scripts/context_cli.py`

Only `schema` and `capabilities` are core-free. Low-level semantic operations retain caller `--host`, `--core-inventory @file`, and `--core-doctor @file` as compatibility input.

Canonical init and workflow first compare the absolute core entrypoint path suffix and SHA-256 with the release pin. Before executing further subprocess work they directly validate `context-core-schema/v1`, `context-common/v2`, required doctor/bootstrap/transaction commands, `context-owner-descriptor/v2`, and the exact doctor shape/state. This executable handshake does not attest marketplace provenance, source, scope, or enabled state.

The decision owner does not install, enable, update, add a marketplace, probe plugin caches, or embed a core runtime. `repository_state=absent` is bootstrap-required; partial/invalid diagnostics are not a global semantic-operation failure unless they overlap an actual target.

## Semantic claim gate

A DEC is an explicit choice governing current or future action. The exact candidate must bind all assertions:

- `explicit_choice` -> `/owner_inputs/decision/decision`
- `scope_identified` -> `/scope_hint`
- `commitment_present` -> `/evidence/*`

Ideas, questions, facts, preferences, and unaccepted proposals are `decline` or `needs_clarification`. `requested_kind:"decision"` selects an owner but never bypasses this gate. The CLI validates assertion names, exact input digest, and RFC 6901 pointers; it does not make semantic judgment for the agent.

`candidate prepare` normalizes caller-provided fields, a caller-generated `cand_` plus 32 lowercase hex transport ID, commitment evidence, and bounded search terms. The owner then calls `capture --candidate @file --attestation @file`, or exits without an authoritative draft via a decline/clarification reason. Random candidate generation, constant evidence, and self-attestation are forbidden.

## DEC schema and slot

The required body sections are `결정`, `취지`, and `반려대안`. Missing, empty, or placeholder content fails. If no alternative was reviewed, use `검토하지 않음: <reason>`. Optional sections are `근거와 제약`, `트레이드오프`, and `재평가 조건`. `verified_at` and common `status` are forbidden.

Scope canonicalization is trim -> NFKC/casefold -> remove outer slashes -> normalize each non-alphanumeric run to `-`. Empty/dot segments, over eight segments, a segment over 40 characters, and total scope over 160 characters fail. `decision_key` uses the same normalization, forbids `/`, and is at most 80 characters.

Current has at most one DEC per `(scope, decision_key)`. Same-key ancestor/descendant scope is an overlap conflict and requires acknowledgement plus exact `{id,path,sha256}` read preconditions. The agent compares actual bodies; fingerprints are never semantic identity.

## Owner results and lifecycle

Capture returns one Current draft/effect/create operation. Draft time fixes ID and `created_at` and binds embedded candidate, claim attestation, complete content, and semantic projection.

- `supersede`: successor repeats the predecessor's canonical slot; one result moves the predecessor to History and creates the successor with reciprocal `superseded_by`/`supersedes` edges.
- `withdraw`: retire the predecessor as withdrawn with no successor.
- `annotate`: preserve decision sections, slot, and ID; change only title, summary, tags, search terms, and source refs.
- `revisit`: return a warning/review proposal without mutation.

Ordinary OBS evidence remains active and is linked by `relations.informed_by`. A decision-like fallback OBS import requires exact source ID/path/SHA/actual claim, `same_claim`, and a cross-owner coordinator plan.

## Same-batch validation

`batch validate` starts from the exact physical `decision.index.md` SHA and overlays prior same-area final bundles in proposal order. Each plan must bind the exact preceding digest sequence. Virtual Current enforces slot uniqueness, overlap acknowledgement/read preconditions, and lifecycle predecessor state.

A successful receipt binds owner-result digest, base area-index SHA, ordered same-area prior digests, canonical scope/key, actual primary claim, rationale, acknowledged conflicts, and its own digest rule. A missing or altered receipt fails final plan validation.

## Frozen workflow receipt

The public golden path is `decision_workflow.py preview --inline` then `apply`. The caller supplies semantic fields and explicitly attests choice, scope, and commitment. Preview verifies the release-pinned core, directly handshakes schema and doctor, builds/revalidates the owner result, and calls core transaction preview in one process.

The complete bundle/material stays in a new receipt outside the repository and Git metadata, created mode `0600`. Stdout returns the approval preview and user-facing exact `approval_digest`. The workflow approval material binds exact `context-repository-identity/v1`, core absolute path/pinned SHA-256, candidate/result digests, nested core approval digest, and the complete nested bundle. `receipt_digest` is damage detection, not approval; modifying and rehashing a receipt cannot preserve the original approved digest.

Receipt overwrite, repository-local receipt, clone/linked-worktree/same-path-recreated replay, changed core bytes, and wrong approval all fail before writes. Apply forwards the frozen bundle and does not regenerate it. Delete the sensitive receipt manually when the workflow is complete.

Inline `--sec-*` values are literal by default. `@file` reads a named regular UTF-8 file; `@@literal` preserves one leading `@`; path-like plain text remains literal. Missing, symlinked, and oversized files fail before receipt or repository writes. The common primary-claim protocol ceiling is 2,000 codepoints; built-in SNAP `current_context`, OBS `observation`, and DEC `decision` each use an owner-specific 1,200-codepoint ceiling. Canonical owner input is at most 8 KiB and the complete candidate envelope at most 16 KiB.

## Recall, spec view, and init

`search` reads decision index metadata. `read` and `brief` open selected DEC bodies only. Brief includes the three required sections and is at most 8 KiB. History always carries `do_not_follow:true` and a lifecycle reason.

`check` always includes exact-slot and scope-overlap candidates, then adds only distinctive metadata matches. It never opens arbitrary score-zero bodies. Comparison input is at most 24 KiB and the complete result at most 32 KiB. The agent returns `new|same|supporting|rationale_changed|conflict`; `new` is bounded to the returned set.

`spec-view --scope` selects exact/strict-ancestor/strict-descendant Current DEC metadata and materializes only `결정` and `취지`, ordered by `(created_at,id)`. It excludes History and `do_not_follow`. Complete JSON stdout including the final newline is at most 32 KiB; trailing entries are omitted whole and counted.

Init verifies a v2-capable release-pinned core and doctor, then passes the DEC area's exact legacy-compatible `context-owner-descriptor/v1` and empty DEC index seed to core bootstrap. One call may complete core root setup, DEC registration, and managed policy installation. The decision CLI itself writes none of those bytes.

## Output

Success is `{"ok":true,"result":...}`. Error is `{"ok":false,"error":{"code":...,"message":...,"details":...}}`. Exit 2 covers usage/schema, 3 not-found, 5 conflict, and 6 integrity/index failures. Every semantic operation must leave repository filesystem bytes unchanged.

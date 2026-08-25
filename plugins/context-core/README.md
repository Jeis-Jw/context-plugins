# context-core

`context-core` is the Git/Markdown storage and recall kernel for durable project context. It owns SNAP handoffs, OBS evidence, deterministic indexes, approval previews, and every physical context write.

## Supported developer-preview path

From the immutable `v0.7.0` checkout, run the root `core-decision` profile installer once. It asks the host to install `context-core@context-plugins` and `context-decision@context-plugins` as separate packages at the same version and scope. Reload the host, then run `$context-decision:init` once in the target repository. That addon init bootstraps core storage, registers the DEC area, and installs the managed `AGENTS.md` or `CLAUDE.md` policy. There is no bundle or meta-plugin, and decision code is not embedded in core.

For a core-only setup, `$context-core:init` remains available. It creates the canonical root, SNAP and OBS indexes and the active host policy. Re-running init after a ready result is a filesystem no-op.

The `v0.7.0` tag is not published yet. See the repository root README for the owner-gated tag, publication, and license status.

## Runtime contract

- `schema` and `capabilities` work without a repository root.
- `doctor` is read-only and reports `context-common/v2`, `repository_state`, `issues`, and `warnings`.
- `repository_state=absent` is a bootstrap state. A read operation against an absent root fails with `context_root_missing`.
- `init` and addon `bootstrap` may apply only fixed `core_init|area_register|policy_install` transitions. They preserve bytes outside the managed policy markers and fail closed on unsafe targets.
- A generic addon may register an immutable `context-owner-descriptor/v2` structural profile. Core validates the artifact envelope, fields, sections, topology, paths, indexes, CAS, and receipts independently of the semantic owner.
- Core is the only physical coordinator. Semantic owners return drafts, effects, plans, and validation receipts but do not write repository bytes.

## Recall and bounded work

The managed policy audits only the new semantic delta in the current response pass. It emits no audit status when there is no durable signal. Relevant context is selected metadata-first and only selected bodies are materialized.

- A healthy metadata miss opens zero indexed artifact bodies.
- Missing or stale index recovery opens at most 20 bodies per recall.
- Stage-1 output is bounded to 4 KiB, selected body packs to 8 KiB, and approval previews to 32 KiB.
- The common primary-claim protocol ceiling is 2,000 codepoints. Built-in SNAP `current_context` and OBS `observation` each use an owner-specific 1,200-codepoint ceiling; DEC `decision` independently uses 1,200. Canonical owner input is at most 8 KiB. A `context-capture-batch/v1` has at most eight candidates and its entire canonical envelope is at most 16 KiB.
- These hard bounds cover body materialization/open, selected output, candidates/envelopes, and owner invocation input. Index scoring and directory enumeration may grow with the index, and end-to-end model tokens are not O(1).

## Approval and repository binding

The user sees the complete rendered preview and one natural-language capture question. A write is allowed only after a direct, explicit, unconditional affirmative answer. `알겠어` alone, a condition, an edit request, or a topic change is not approval; ambiguous praise is confirmed once.

Transport details remain internal to the agent. Preview freezes on-disk preconditions, derived index bytes, owner authorization, and operations before the question; apply never regenerates them. Repository identity, pinned runtime, CAS, the repository-realpath lock, atomic operations, and deterministic index rebuild remain enforced. Clone or linked-worktree replay, same-path repository recreation, tampering, and changed target bytes fail before writes.

A denied apply, preview, recall, route, claim, or validation has zero repository and host-policy writes.

## Storage roles

| Kind | Purpose | Authority |
|---|---|---|
| SNAP | Unfinished-session handoff | staging |
| OBS | Reusable observation and evidence | evidence |
| DEC | Current decision and superseded history | authoritative, owned by `context-decision` |
| ASM | Optional unverified premise | provisional, experimental owner |
| TERM | Optional project vocabulary | authoritative, experimental owner |

Markdown artifacts are canonical; `context.index.md` and area indexes are deterministic projections. Existing `context-common/v2` artifacts are not rewritten by the 0.7.0 release, and existing `wiki/` content is never migrated automatically.

See the [storage protocol](./skills/context/references/context-protocol.md), [root release status](../../README.md), and [한국어 문서](./README.ko.md).

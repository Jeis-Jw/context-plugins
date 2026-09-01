# context-core

`context-core` is the filesystem/Markdown storage and recall kernel for durable project context. It owns SNAP handoffs, OBS evidence, deterministic indexes, approval previews, and every physical context write.

## Supported developer-preview path

Run the root `core-decision` profile installer once from the downloaded plugin files. It asks the host to install missing profile plugins and accepts enabled same-major versions as compatible. Reload the host, then run `$context-decision:init` once in the target vault directory. That addon init bootstraps core storage, registers the DEC area, and installs the managed `AGENTS.md` or `CLAUDE.md` policy. There is no bundle or meta-plugin, and decision code is not embedded in core.

For a core-only setup, `$context-core:init` remains available. It creates the canonical root, SNAP, OBS, and ARCHIVE indexes and the active host policy. Re-running init after a ready result is a filesystem no-op; a pre-ARCHIVE vault receives only the missing empty ARCHIVE area.

The `v0.12.0` tag is not published yet. See the repository root README for the owner-gated tag, publication, and license status.

## Runtime contract

- A vault is a regular directory containing `context/`. Git is optional for sharing and version control; neither Git nor `.git` is required.
- Global `--vault DIR` selects the directory before any subcommand. Without it, the nearest ancestor with `context/` is used, or cwd for a fresh vault. Relative input files still resolve from the caller's cwd.
- `schema` and `capabilities` work without a vault. `filesystem-vault/v1` is required by addon init/workflow.
- `doctor` is read-only and reports `context-common/v2`, `repository_state`, `issues`, and `warnings`.
- `repository_state` is a retained compatibility field describing vault storage, not version-control status.
- `repository_state=absent` is a bootstrap state. A read operation against an absent root fails with `context_root_missing`.
- `init` and addon `bootstrap` may apply only fixed `core_init|area_register|policy_install` transitions. They preserve bytes outside the managed policy markers and fail closed on unsafe targets.
- A generic addon may register an immutable `context-owner-descriptor/v2` structural profile. Core validates the artifact envelope, fields, sections, topology, paths, indexes, CAS, and receipts independently of the semantic owner.
- Core is the only physical coordinator. Semantic owners return drafts, effects, plans, and validation receipts but do not write repository bytes.

## Recall and bounded work

The managed policy audits only the new semantic delta in the current response pass. It emits no audit status when there is no durable signal. Relevant context is selected metadata-first and only selected bodies are materialized.

- A healthy metadata miss opens zero indexed artifact bodies.
- Missing or stale index recovery opens at most 20 bodies per recall.
- Stage-1 output is bounded to 4 KiB, selected body packs to 8 KiB, and ordinary approval previews to 32 KiB.
- The common primary-claim protocol ceiling is 2,000 codepoints. Built-in SNAP `current_context` and OBS `observation` each use an owner-specific 1,200-codepoint ceiling; DEC `decision` independently uses 1,200. Canonical owner input is at most 8 KiB. A `context-capture-batch/v1` has at most eight candidates and its entire canonical envelope is at most 16 KiB.
- Limits are default-read budgets: expand knowledge with more stable slots, not larger slots. ARCHIVE is the explicit exception for immutable source material: `Content` is at most 65,000 codepoints, its capture envelope is bounded to 512 KiB, and it is excluded from default recall/pack unless `--include-archive` is present.
- These hard bounds cover body materialization/open, selected output, candidates/envelopes, and owner invocation input. Index scoring and directory enumeration may grow with the index, and end-to-end model tokens are not O(1).

## Approval and vault binding

The user sees the complete rendered preview and one natural-language capture question. A write is allowed only after a direct, explicit, unconditional affirmative answer. `알겠어` alone, a condition, an edit request, or a topic change is not approval; ambiguous praise is confirmed once.

Transport details remain internal to the agent. Preview freezes on-disk preconditions, derived index bytes, owner authorization, and operations before the question; apply never regenerates them. Vault identity, pinned runtime, CAS, the vault-realpath lock, atomic operations, and deterministic index rebuild remain enforced. Replay in a copied or moved vault, same-path directory recreation, tampering, and changed target bytes fail before writes.

A denied apply, preview, recall, route, claim, or validation has zero repository and host-policy writes.

## Storage roles

| Kind | Purpose | Authority |
|---|---|---|
| SNAP | Unfinished-session handoff | staging |
| OBS | Reusable observation and evidence | evidence |
| ARCHIVE | Immutable source material adopted as evidence | evidence; excluded from default recall |
| DEC | Current decision and superseded history | authoritative, owned by `context-decision` |
| ASM | Optional unverified premise | provisional, experimental owner |
| TERM | Optional project vocabulary | authoritative, experimental owner |
| INTENT | Optional desired direction | authoritative, owned by `context-intent` |
| DOCUMENT | Optional living project content | authoritative, owned by `context-document` |

Markdown artifacts are canonical; `context.index.md` and area indexes are deterministic projections. Existing `context-common/v2` artifacts are not rewritten by the 0.9.0 release, and existing `wiki/` content is never migrated automatically.

`typed-relations/v1` is additive and keeps the existing relation-map storage shape. Keys shaped as `<predicate>:<target-kind>` are checked against the live target kind during preview, apply revalidation, refresh, and doctor. Keys without `:` retain legacy behavior. Core stores no inverse edge and performs no artifact migration.

Version `0.9.0` uses major versions as the package compatibility boundary, minor versions for functional changes, and patch versions for small fixes. Protocol and capability handshakes remain authoritative even for same-major packages.

Version `0.10.0` adds typed relation validation and optional INTENT/DOCUMENT owner registration surfaces without changing the filesystem-vault or approval model. No tag or publication is implied.

Version `0.11.0` makes OBS preview state explicit, provides the shared inline owner workflow transport, and adds a diagnostic same-major cache-pin warning without changing approval or stored artifact bytes. No tag or publication is implied.

Version `0.12.0` adds immutable ARCHIVE capture/read/search/discard, bounded OBS-to-context evidence references, and DOCUMENT freshness hygiene diagnostics while preserving the approval and filesystem-vault boundaries. No tag or publication is implied.

See the [storage protocol](./skills/context/references/context-protocol.md), [root release status](../../README.md), and [한국어 문서](./README.ko.md).

# context-common/v2 storage kernel

This is the public, host-independent storage, recall, and write contract implemented by `context-core`. Product composition and distribution identity live in the repository and plugin READMEs; executable schemas and tests verify runtime behavior.

## Canonical storage and identity

- The Git worktree's `context/` directory is the only storage root; there is no `--root` override.
- Markdown artifacts are canonical. `context.index.md` and `<area>.index.md` are deterministic projections.
- Artifact IDs are `ctx_` plus 32 lowercase UUIDv4 hex characters. Filename, title, path, and lifecycle changes do not change the ID.
- Frontmatter is a one-line-per-field JSON-compatible YAML subset. Bodies use fixed ordered H2 sections for each artifact schema.
- `claim_fingerprint`, `source_claim_fingerprint`, and candidate `claim_key` are removed. Candidate IDs are transport references only. Legacy removed fields are readable with `schema_removed_field` warnings and are lazy-cleaned on the next approved rewrite; new input fails closed.

## Read boundary

- A healthy Stage-1 metadata hit reads only the root and selected area index. It performs zero artifact opens/lists/stats.
- A healthy non-empty query with zero metadata matches enumerates filenames only to detect unindexed artifacts. When all files are indexed, it opens zero bodies and is not marked as fallback.
- Missing bodies, a broken selected area index, and a missing selected link share a recovery budget of at most 20 artifact body opens per recall. Truncation returns `index_miss_fallback_truncated` or `index_fallback_truncated`.
- `--strict-index` disables fallback and fails with exit 6 `index_stale`.
- A missing root index is `context_root_missing`, not a plugin dependency error.

## Bounded-cost scope

Hard bounds apply to artifact body materialization/open, selected output, candidate envelopes, and model/owner invocation input; they prevent those costs from growing in proportion to corpus size, addon count, or accumulated turns.

- Healthy Stage 1: index-only and zero artifact opens/lists/stats.
- Recovery: at most 20 body opens.
- Stage-1 output: 4 KiB; selected body pack: 8 KiB; approval preview: 32 KiB.
- Common primary-claim protocol ceiling: 2,000 codepoints; built-in SNAP `current_context` and OBS `observation`: 1,200 codepoints each; canonical owner input: 8 KiB.
- `context-capture-batch/v1`: at most eight candidates and at most 16 KiB for the full canonical `{schema,audit_count,candidates}` envelope. `audit_count` is the non-bool integer `1`; a legacy bare list is charged against the same synthetic envelope budget.
- DEC additionally limits its primary decision to 1,200 codepoints, brief to 8 KiB, comparison input to 24 KiB, result to 32 KiB, and spec-view stdout to 32 KiB.

Index bytes, metadata-row scoring, and directory enumeration can grow with the selected index or directory. The implementation avoids corpus-wide body materialization; it does not guarantee O(1) end-to-end recall computation or model tokens. `tests/context-v1/test_token_io_evidence.py` measures the enforceable artifact I/O, candidate, addon, and stdout budgets.

The managed policy requires one audit per conversation delta, silence when there is no signal, and no addon re-reading of the conversation. The CLI validates `audit_count:1` and bounded envelopes, but host/model compliance is not a hard runtime guarantee.

## Conversation boundary

- Audit only the new user-turn meaning in the same response pass; it is not a background daemon, extra model call, or per-turn CLI hook.
- Keep only scope/anchor, already read `{id,sha256}`, and pending/dismissed references in a bounded session-local ledger. Do not copy bodies or candidates into repository state.
- Recall metadata first and materialize selected bodies only. Reuse a body only while scope, evidence, anchor, indexes, SHA, and its session presence remain unchanged.
- Report conflict or rationale change before the primary conclusion. Propose ordinary capture only after a mature milestone, and do not repeat dismissed/deferred candidates without new evidence.

## Write and approval boundary

- A semantic owner returns complete drafts/effects and a proposed `context-owner-plan/v1`; it performs no physical write.
- `transaction preview` seals target preconditions, material, derived index rebuild, and owner/area authorization into `context-mutation-bundle/v1`.
- `approval_digest` is the canonical SHA-256 of the complete approval material. The material includes `context-repository-identity/v1`, with exact resolved worktree and Git common-directory paths and decimal device/inode strings. Extra or missing identity fields are invalid.
- Apply verifies the digest and current repository identity before any write. A clone, linked worktree, or same-path recreated repository cannot replay a bundle. HEAD and unrelated content are intentionally not bound; exact target CAS still protects affected bytes.
- Only context-core writes, under a repository-realpath lock, with atomic operations and deterministic index rebuild.
- Hidden operations, missing seeds, altered material, changed target preconditions, path escapes, and symlink segments fail before writes.

## Generic owner descriptor

`context-owner-descriptor/v1` bytes remain supported and v1/v2 areas may coexist. A v2-capable runtime advertises `context-owner-descriptor/v2` in root-independent `schema.features`. No automatic upgrade, downgrade, migration, deletion, or descriptor replacement exists.

- A v2 descriptor is canonical UTF-8 JSON of at most 8 KiB and contains identity plus a closed `context-structural-profile/v1`.
- Unknown/duplicate keys, non-canonical input, executable defaults, regex/expression/callback fields, and depth/node/field/item bound violations fail closed.
- Profiles allow at most 24 closed-type fields, 12 ordered H2 sections, and four scalar index projections. Lifecycle topology is limited to `create_current|replace_same_state|retire_current|supersede_current|delete_one`.
- A v2 semantic receipt binds descriptor digest, capability, owner result, base area index, ordered same-area prior bundles, topology, and semantic input digest. Core independently validates target envelopes, fields, sections, projections, lifecycle, relations, paths, indexes, CAS, and operations during preview and again under lock during apply.
- The root registry and area descriptor must carry the same immutable digest. A trust mismatch is a blocking doctor/refresh issue and `refresh --fix index` does not repair it.

## CLI envelope and init

- success: `{"ok":true,"result":{...}}`
- error: `{"ok":false,"error":{"code":"...","message":"...","details":{...}}}`
- exit 2: usage/schema/filename; exit 3: root/artifact/input missing; exit 5: owner/path/lifecycle conflict; exit 6: integrity/index failure
- `schema` and `capabilities` work without a repository root.

`init --host codex|claude-code` applies an absent root's canonical root/SNAP/OBS seeds and the active host policy (`AGENTS.md` or `CLAUDE.md`). It preflights policy targets/markers before storage writes and preserves bytes outside the managed block.

`bootstrap --descriptor @file --index-seed @file --host ...` is the public addon-init surface. In one call it completes core init, registers an exact empty area, and installs the same policy. Only fixed `core_init|area_register|policy_install` transitions receive explicit-init authority; all user-content mutation remains approval-gated.

Lifecycle semantic input includes actual predecessor/successor primary claims, bounded supporting context, artifact path/ID/SHA, and source candidate digest. A `same_claim` attestation must point to both actual claims; hash-derived identity cannot substitute.

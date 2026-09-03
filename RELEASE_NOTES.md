# Release notes

## 0.14.0 (developer preview; tag not published)

This is the unreleased lean v6 source candidate. Distribution manifests still describe the `0.13.0` release set pending release preparation.

- Add `decision_workflow.py record --approved`: the caller attests direct, explicit, unconditional semantic approval, then one process previews and applies the unchanged frozen receipt. Core remains the only physical writer; runtime SHA, vault identity, approval binding, CAS, locking, and atomic writes remain enforced.
- Resolve an omitted `--core-cli` only when exactly one manifest-validated, same-major sibling core exists. Missing or ambiguous candidates stop before a write. Explicit paths and the low-level two-phase workflow remain compatible.
- Derive up to twelve search terms from a decision's body when none are supplied, including rejected alternatives and rationale. Compare query and index word stems so a conflicting request can find the relevant decision among near-topic distractors without a body scan.
- Make DEC `check` and `record` the ordinary agent path. Avoid reference/script discovery, `--help`, and post-capture rechecks; reuse returned bodies and the write result. Align the installed policy, core policy source, and repository managed block, including bounded task-subtree discovery.
- Weight distinctive discovery hits by inverse corpus frequency, with additional title/key weight and consistent common word stems. Use integer logarithmic IDF bands in discovery so within-band frequency changes from component siblings do not reorder equal lexical evidence. Protect the raw top `ceil(limit/2)` candidates (four by default) from diversity penalties, then fill the remaining slots by query-hit diversity. Break equal scores by coverage of already selected metadata, without rewarding unrelated extra words. Preserve the frequency cutoff, exact-slot/overlap ranking and mandatory coverage, and count/byte bounds.
- Re-stem queries and stored terms at query time; the stem changes require no migration of stored `search_terms`.
- Instruct the semantic owner to reuse a returned Current scope/key for the same governing choice. Existing comparison results already contain these fields; no extra slot-list payload or context read is added.

### Measured evidence and limits

The previously collected v4 Codex experiment measured input tokens, not document characters. At N=0, mean input tokens per session fell from approximately 200K for `0.13.0` to 78K for lean v6 (adr-lite: 77K). At N=200, mean recall-session input was 85K for v6 versus 342K for adr-lite. These are different denominators: the N=0 figures cover all three session types; N=200 figures here cover semantic recall only.

Source: `value-validation-v4/RESULTS.ko.md`, sections 3 and 5–7, with `protocol.v4.json` and `evidence/{r1,scale200}` scorecards in the local experiment worktree on `task/value-validation-v4`. These evidence files are not yet published. The experiment used one repeat, eight scenarios at N=0 and four at N=200, on Codex only. V6 held all measured true conflicts (4/4 and 2/2), but its N=0 no-signal result was 7/8 and G5 failed. Claude Code behavior, repeat variance, and SNAP/DOCUMENT resume value remain unmeasured.

The separate W2 model-free regression queries all eight unchanged v4 prompts against frozen, record-created corpora with observed v6 titles and slots. At N=200, recall@8 improves from 5/8 to 8/8; at N=1000, from 4/8 to 8/8. Recall@1 improves from 4/8 to 6/8 at both sizes, with at most eight returned bodies. Source: `value-validation-v4/RETRIEVAL.ko.md` and its JSON reports. This is a development regression set with repeated synthetic topics, not a holdout or a new measurement of agent behavior or token savings. The committed `test_recall_at_scale.py` fixture also checks body-read bounds and zero reads for high-frequency noise.

The B1 review regression adds ten component siblings per target at N=200/1000. All eight targets remain returned, and the six conflict/premise targets rank first or second, with at most eight body reads and 32 KiB output. These are synthetic metadata fixtures with mocked body reads. The separate record-created corpus still returns 8/8 at recall@8 and 6/8 at recall@1 at both sizes; the new `w2-b1-fix` report exports both measurements without replacing prior evidence.

### Reproducible verification

- Code and policy change sets each pass the complete Python 3.11 and 3.13 suites: 362 passed, 602 subtests.
- The subsequent W2 ranking and scale-regression change passes both complete suites: 365 passed, 624 subtests. The experiment corpus checks pass on both interpreters as well.
- The B1 follow-up passes both complete suites: 368 passed, 640 subtests, including record supersede/withdraw and ambiguous same-major core-cache regressions.
- Both interpreters pass `compileall`; `claude plugin validate` passes for the marketplace, core, and decision packages using isolated local configuration.
- The generated policy body, distributed rule, and repository managed block are identical. Core EN/KO SKILL files remain within the existing 3,000-byte limits.

## 0.13.0 (developer preview; tag not published)

- Replace the user-facing rendered Markdown/file-body approval preview with semantic approval of payload, canonical scope, and lifecycle effect in normal conversation. A direct, explicit, unconditional settled choice or record request authorizes capture without a second storage question.
- Ask only about unresolved meaning. Generic acknowledgement, praise, conditions, edit requests, and topic changes do not approve unresolved content; a semantic delta introduced by rendering still stops the write for focused confirmation.
- Keep preview, frozen receipts, `approval_digest`, pinned runtime and vault identity, CAS, lock, atomic writes, deterministic indexes, and unchanged apply as internal integrity controls. `approval_digest` remains a compatibility field name, not user-approval evidence.
- Preserve `context-common/v2` and existing artifact/index bytes. No stored-context migration is required; pending receipts from an older runtime should be discarded and regenerated.
- Publish release set `0.13.0` as a component-version map: `context-core` and `context-document` move to `0.13.0`; decision, assumption, term, and intent move to `0.12.0`.
- Codex default-prompt material is now from 3,147 to 2,021 characters, a 35.8% character reduction. This is a character-count observation, not a runtime token-savings measurement.

### Reproducible verification

- Python 3.13: `python3 -m pytest -q` → 356 passed, 600 subtests.
- Python 3.11: seven changed-surface `unittest` modules → 58 passed. This environment has no Python 3.11 `pytest` package, so a full 3.11 collection is not claimed.
- Phase 0: 15 passed, 27 subtests.

## 0.12.0 (developer preview; tag not published)

- Add built-in immutable `context-archive/v1` evidence with approval-gated preview/apply, dedicated read/search/discard surfaces, a 65,000-codepoint Content ceiling, and explicit-only recall through `--include-archive`.
- Additively register the empty ARCHIVE area when explicit init encounters a healthy pre-ARCHIVE vault. Existing artifact bytes and IDs remain unchanged.
- Treat exact `ctx_` IDs in OBS Evidence as integrity-checked internal references while retaining free-form evidence strings. Inbound references block ARCHIVE discard.
- Raise OBS evidence slots from four to six and document the policy that limits are default-read budgets: expand knowledge through stable slots, not larger slots. Clarify that DOCUMENT is a current-state recall/envelope surface, not a repository deliverable store.
- Make `affects:document` operational: refresh emits a non-blocking `document-stale-vs-decision` hygiene warning until a newer affecting Current DEC is reflected by a later DOCUMENT update.
- Publish release set `0.12.0` as a component-version map: `context-core` and `context-document` move to `0.12.0`; unchanged decision, assumption, term, and intent packages remain at `0.11.0`.

## 0.11.0 (developer preview; tag not published)

- Make OBS preview state unambiguous: `observation preview` is canonical, `capture` remains a deprecated alias, and both JSON surfaces return envelope-level and result-level `applied: false` plus `state: awaiting_approval`. Human output states that approval and `transaction apply` are still required.
- Add one-command inline preview wrappers for INTENT, TERM, ASM, and DOCUMENT, followed by one unchanged approved apply command. The wrappers derive the verified core manifest inventory and doctor state instead of requiring caller-authored candidate, attestation, inventory, or doctor JSON.
- Declare one six-plugin `context-plugin-release-set/v1` component map in both marketplace catalogs. Profile v3 keeps same-major runtime compatibility, uses per-component minimums, and never updates automatically.
- On core path, manifest, schema, or command incompatibility, semantic adapters list manifest-validated same-major sibling core candidates for diagnosis only. They never select or execute a candidate automatically. Core doctor warns when its loaded catalog pin is behind a newer same-major cached version.
- Clarify that `--revisit-on` accepts only a calendar date while `--sec-revisit` carries condition text. Comma-packed relation IDs now fail with guidance to repeat the typed relation flag.
- Preserve `context-common/v2`, stored artifact bytes, approval binding, vault identity, CAS, locking, atomic writes, no-Git operation, and independent semantic-owner packages.

### Reproducible verification

- Python 3.13: `python3 -m pytest -q` → 351 passed, 579 subtests.
- Python 3.11: nine changed-surface `unittest` modules → 103 passed. This environment has no Python 3.11 `pytest` package, so a full 3.11 collection is not claimed.

## 0.10.0 (developer preview; tag not published)

- Add additive `typed-relations/v1` validation. Storage remains `relations: { key: [ctx_id...] }`; `<predicate>:<target-kind>` targets must exist with that kind during preview, apply revalidation, refresh, and doctor. Legacy keys without `:` remain compatible.
- Add optional `context-intent` with authoritative `(scope, intent_key)`, required `Intent`, optional success/constraint/revisit sections, and capture/read/search/supersede lifecycle.
- Add optional `context-document` with authoritative `(scope, document_key)`, required `Content`, and stable-ID `replace_same_state` updates. No taxonomy, inverse relations, or extra lifecycle is introduced.
- Keep DEC standalone and preserve descriptor v1, required sections, legacy `informed_by`, and existing artifact bytes. Optional DEC inputs project to `serves:intent`, `informed_by:observation`, `informed_by:assumption`, and `affects:document`.
- Intent, decision, and document owners remain independently installable and usable. The `core-decision` profile remains exactly core plus decision, and no plugin installs another.
- Codex default-prompt material is now from 3,147 to 2,010 characters, a 36.1% character reduction. This is a character-count observation, not a runtime token-savings measurement.
- Filesystem vault, approval, CAS, locking, and artifact-byte compatibility remain unchanged. No Git dependency, migration, tag, push, or publication is introduced.

## 0.9.0 (developer preview; tag not published)

- Context storage and approval no longer depend on Git, repositories, worktrees, or Git metadata. `--vault DIR` selects a directory containing `context/`; automatic selection uses the nearest current/ancestor `context` entry, or cwd for fresh initialization.
- Approval stays bound to the actual vault directory, frozen content, runtime digest, CAS, and lock. Previously generated pending receipts need a fresh preview and approval; existing saved artifacts are unchanged.
- Addon initialization and workflows require the `filesystem-vault/v1` capability. The profile installer works from ordinary downloaded files without a tag or clean checkout.
- Historical repository-identity requirements in older release entries are superseded by this contract.

## 0.8.0 (developer preview; tag not published)

- Package versions now use major as the compatibility boundary, minor for functional changes, and patch for small fixes. The same rule applies to `0.x`, so `0.*` packages pass the package-version gate together.
- `context-plugin-profile/v2` declares `compatibility: same-major`. The profile installer accepts enabled same-major plugins, installs only missing core/decision members, and does not auto-update compatible installations.
- Disabled plugins, different majors, the legacy provider, and a marketplace mapped to another checkout still stop before host mutation.
- Semantic addons validate the core entrypoint suffix and adjacent Claude/Codex manifests, require the same major, retain the schema/protocol/capability/command/doctor handshake, and bind the actual executable digest for each init operation or frozen DEC preview/apply lifecycle.
- Existing `context-common/v2` repository artifacts require no migration. Plugin packages and semantic ownership remain separate.
- Codex default-prompt material was reduced from 3,147 to 1,339 characters, a 57.5% character reduction. This is a character-count observation, not a runtime token-savings measurement.
- Static prompt or document-size reductions are not claimed as measured runtime token savings; improved runtime value remains a separate live-validation question.

## 0.7.1 (developer preview; tag not published)

- Canonical runtime instructions, managed policies, manifests, and default prompts are authored in English. User-facing prose follows the explicit user language, host preference, established conversation language, then English fallback.
- New durable artifacts use canonical English section headings while legacy Korean-heading artifacts remain readable and preserve their original headings on round-trip updates.
- The root user guide is English-first with a maintained Korean counterpart, and the repository now carries the complete Apache License 2.0 text in `LICENSE`.

- User-facing approval is one natural-language question over the complete rendered preview. Only a direct, explicit, unconditional affirmative answer applies; `알겠어` alone, conditions, edits, and topic changes do not.
- Digests, receipt locations, internal IDs, and core paths are agent/CLI transport details and are never shown to or requested from users.
- The managed policy is four concise lines; all 16 SKILL surfaces carry the same approval classification and no-signal behavior.
- Decision lookup no longer requires write-oriented preflight. Scope-less checks are explicitly discovery-only, while exact-slot conflict validation is repeated before preview.
- DEC preview/apply/reject owns a deterministic private receipt lifecycle, including TTL cleanup, one-time apply deletion, supersede and withdraw recovery paths. OBS and SNAP expose the same two-command receipt surface.
- `context-core` remains the storage/index/transaction coordinator and each semantic owner remains a separate plugin package. Decision code is not copied into core.
- `profiles/core-decision.json` and `scripts/install_profile.py` provide one explicit distribution action that installs the separate core and decision packages at one version and scope. Installed plugins never install or replace each other; legacy providers and mismatched checkouts fail before host mutation.
- Frozen receipt, approval binding, repository identity, pinned core SHA, CAS, lock, atomic write, and no-regeneration-after-approval boundaries remain intact.
- W1 wording and W2 workflow changes ship together; neither surface is a standalone 0.7 release.

### Reproducible verification

- Python 3.11: clean temporary environment, `python3.11 -m pytest -q` → 299 passed, 242 subtests.
- Python 3.13: `python3.13 -m pytest -q` → 299 passed, 242 subtests.
- Phase 0: 15 passed, 27 subtests on each interpreter.

## 0.5.1 (prepared; tag not published)

This developer-preview patch preserves `context-common/v2` and existing SNAP, OBS and DEC bytes. It is distinct from the already published 0.5.0 bytes; `v0.5.1` has not been created or pushed.

### W1 — lower prompt and recall overhead

- Codex default-prompt material was reduced from 3,147 to 1,333 characters, a 57.6% character reduction. This is not a token-savings measurement.
- The DEC golden path now builds one inline preview and stores the frozen bundle in a transient, mode-`0600` receipt outside the repository.
- Healthy metadata misses open zero indexed artifact bodies; stale or missing index recovery opens at most 20 bodies per recall.

### W2 — bind approvals and executable identity

- Core approval material binds the resolved worktree and Git common directory path/device/inode identity. Clone replay, linked-worktree replay and same-path repository recreation fail before writes.
- The DEC workflow's user-facing `approval_digest` binds repository identity, pinned core absolute path/SHA-256, candidate/result digests, and the nested core bundle/digest. Rehashing a modified receipt cannot preserve the original approval.
- DEC, ASM and TERM verify the release-pinned `context_cli.py` suffix and SHA-256 before subprocess execution, then handshake schema, `context-common/v2`, required commands, `context-owner-descriptor/v2` and doctor state directly.
- This executable handshake does not attest marketplace provenance, catalog source or host enabled state. Caller inventory/doctor remain low-level compatibility inputs.

### W3 — semantic input meaning and limits

- DEC validation rejects any candidate-owned frontmatter or semantic section that differs from the embedded exact candidate, including capture and supersede successor drafts. A stale validation receipt cannot authorize a modified result.
- The common primary-claim protocol ceiling is 2,000 codepoints. Built-in SNAP `current_context`, OBS `observation`, and DEC `decision` each use an owner-specific 1,200-codepoint ceiling.
- Canonical owner input is limited to 8 KiB and the full candidate envelope to 16 KiB.
- Core and DEC `--sec-*` values now use literal text by default, explicit `@file`, and `@@literal` for one leading `@`. Missing, symlinked and oversized files fail before receipt or repository writes. ASM and TERM receive structured candidate JSON through `--candidate @file` instead.

### Reproducible verification

- Python 3.11: `python3.11 -m pytest -q` → 257 passed, 191 subtests.
- Python 3.13: `python3.13 -m pytest -q` → 257 passed, 191 subtests.
- Phase 0: `PYTHONPATH=tests/context-v1/phase0 pythonX -m pytest -q tests/context-v1/phase0` → 15 passed on each interpreter.

## Release boundary

This repository is preparing a developer preview and is licensed under the Apache License 2.0 in the root `LICENSE`. Source integration, main-branch push, or license application does not imply a tag or marketplace publication. Creation and push of `v0.13.0` remain owner-gated.

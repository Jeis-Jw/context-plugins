# Release notes

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

This repository is preparing a developer preview and is licensed under the Apache License 2.0 in the root `LICENSE`. Source integration, main-branch push, or license application does not imply a tag or marketplace publication. Creation and push of `v0.7.1` remain owner-gated.

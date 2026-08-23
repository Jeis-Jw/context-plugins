# Release notes

## 0.5.1 (prepared; tag not published)

This developer-preview patch preserves `context-common/v2` and existing SNAP, OBS and DEC bytes. It is distinct from the already published 0.5.0 bytes; `v0.5.1` has not been created or pushed.

### W1 — lower prompt and recall overhead

- Codex default-prompt material was reduced from 3,147 to 1,339 characters, a 57.5% character reduction. This is not a token-savings measurement.
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

This repository is preparing a developer preview. No tag, push or marketplace publication is implied by these notes. The owner must explicitly approve creation and push of `v0.5.1`. A public license has not been selected; an owner must choose one before public reuse or redistribution is invited.

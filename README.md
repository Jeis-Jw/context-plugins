# Context Plugins

Durable project context for coding agents, centered on decisions.

`context-decision` restores what the project chose, why it chose it, and which alternatives it rejected. `context-core` supplies Git/Markdown storage, bounded recall, approval previews, and the only physical write coordinator. Context is proposed only when it is worth keeping and is written only after the user approves the exact digest.

> Developer preview: `0.5.1` is prepared locally, but the `v0.5.1` tag has not been created or pushed. Marketplace publication is also pending. The repository has no `LICENSE`; an owner must choose one before inviting public use, copying, or redistribution.

## Supported profile

The supported developer-preview profile is deliberately small:

1. Install `context-core@context-plugins` and `context-decision@context-plugins` separately.
2. Reload the host or start a new session.
3. Run `$context-decision:init` once in the target Git repository.

There is no bundle or meta-plugin. `context-decision:init` uses the separately installed core to initialize core storage, register the DEC area, and install the managed host policy in one idempotent operation. A separate `$context-core:init` is not required for this profile.

Install core and every semantic addon from the same immutable release checkout. Each addon pins the exact core entrypoint bytes; a mixed or partially updated install fails with `core_surface_mismatch`. Update or reinstall core and the affected addon together, reload the host, and retry.

`context-assumption` (ASM) and `context-term` (TERM) are optional experimental semantic owners. Install and initialize either one separately only when its lifecycle is needed. They are not part of the supported core+decision profile and are never installed or enabled implicitly.

## Why it exists

- Decisions and rationale disappear between agent sessions.
- Rejected alternatives return because the next agent sees only the current code.
- Useful operational evidence remains trapped in chat history.
- Automatic memory capture can turn guesses and transient details into durable noise.

Context Plugins keeps only repository-scoped context. Current DEC documents are authoritative; OBS records reusable evidence; SNAP stages unfinished handoff. Experimental ASM records unverified premises and TERM records project-specific definitions.

```text
conversation delta
  -> metadata-first recall when relevant
  -> selected body comparison
  -> conflict or rationale-change notice
  -> mature capture preview
  -> user approves the exact approval_digest
  -> context-core applies one transaction
```

## Install after the owner publishes `v0.5.1`

These commands intentionally use the immutable `v0.5.1` ref. They will not work until the owner approves the release, creates the tag, and pushes the tag and release commit.

### Codex

```bash
codex plugin marketplace add Jeis-Jw/context-plugins --ref v0.5.1
codex plugin add context-core@context-plugins
codex plugin add context-decision@context-plugins
```

### Claude Code

Claude Code 2.1.89 does not expose a marketplace `--ref` option. Check out the exact tag first, then add that immutable local checkout:

```bash
git clone --branch v0.5.1 --depth 1 https://github.com/Jeis-Jw/context-plugins.git context-plugins-v0.5.1
claude plugin marketplace add /absolute/path/to/context-plugins-v0.5.1
claude plugin install context-core@context-plugins
claude plugin install context-decision@context-plugins
```

After installation, reload the host or open a new session and run `$context-decision:init` once. Choose the host installation scope explicitly; plugins do not add marketplaces, install, enable, update, or change host scope on their own.

Optional experimental owners, after the same exact checkout is installed:

```bash
codex plugin add context-assumption@context-plugins  # experimental
codex plugin add context-term@context-plugins        # experimental
claude plugin install context-assumption@context-plugins  # experimental
claude plugin install context-term@context-plugins        # experimental
```

Run each optional owner's init once. One addon never initializes another addon.

## Safety and cost boundaries

- A durable mutation requires a complete preview and the user's exact `approval_digest` approval.
- The DEC workflow creates a sensitive frozen receipt at a new absolute path outside the repository and Git metadata with mode `0600`. Delete it manually when the workflow is complete.
- The user-facing workflow digest binds repository identity, the release-pinned core path/SHA, candidate/result digests, and the nested core bundle/digest. `receipt_digest` detects receipt damage; it is not approval.
- Repository identity includes the resolved worktree and Git common-directory path/device/inode. Clone replay, linked-worktree replay, and same-path repository recreation fail before writes. HEAD and unrelated content are intentionally not bound, so an unrelated edit and an idempotent retry remain valid.
- Semantic addons verify the release-pinned `skills/context/scripts/context_cli.py` path suffix and SHA-256 before execution, then handshake schema, `context-common/v2`, required commands, `context-owner-descriptor/v2`, and doctor state. This does not attest marketplace provenance, catalog source, or host enabled state. Caller inventory/doctor files are low-level compatibility inputs only.
- Healthy index misses open zero indexed artifact bodies. Stale or missing index recovery opens at most 20 bodies per recall.
- Hard bounds cover body materialization/open, selected output, candidates/envelopes, and owner input. Index scoring/directory enumeration and end-to-end model tokens are not O(1).
- The common primary-claim ceiling is 2,000 codepoints. Built-in SNAP `current_context`, OBS `observation`, and DEC `decision` each use an owner-specific 1,200-codepoint ceiling. Canonical owner input is at most 8 KiB; the full candidate envelope is at most 16 KiB.
- Core and DEC `--sec-*` values are literals by default. `@file` reads a named regular UTF-8 file and `@@literal` preserves one leading `@`; path-like plain text remains literal. Experimental ASM and TERM instead receive structured candidate JSON through `--candidate @file`.

## Verification evidence

| Evidence | Result | Boundary |
|---|---|---|
| Python 3.11 full suite, 2026-08-23 | 257 passed, 191 subtests | `python3.11 -m pytest -q` |
| Python 3.13 full suite, 2026-08-23 | 257 passed, 191 subtests | `python3.13 -m pytest -q` |
| Phase 0 on both interpreters | 15 passed each | `PYTHONPATH=tests/context-v1/phase0 pythonX -m pytest -q tests/context-v1/phase0` |
| Codex `0.149.0-alpha.4.1` | Fresh install and cache lifecycle passed for core+decision | Host lifecycle evidence, not model-behavior evidence |
| Claude Code `2.1.89` | Fresh install and cache lifecycle passed for core+decision | Runtime UX remains experimental |
| Codex + Claude Code | All four plugins installed and loaded | ASM/TERM remain optional experimental surfaces |
| Actual model behavior | Unverified | No confirmed no-signal, capture-quality, or end-to-end token-usage measurement |

Codex prompt material was reduced from 3,147 to 1,339 characters, a 57.5% character reduction. This is not a token-savings claim.

## Release status

| Item | Status |
|---|---|
| Prepared version | `0.5.1` across four manifests, two catalogs, runtime/test constants, and docs |
| Immutable ref | `v0.5.1` planned; tag not created or pushed |
| Repository push | Pending owner approval |
| Marketplace publication | Pending owner approval |
| Public license | Not selected; `LICENSE` intentionally absent until the owner chooses one |
| Supported runtime path | Developer-preview core+decision profile |
| Claude runtime UX | Experimental |

The earlier `context-core@jeis-ai-plugins` distribution is separate. Installing this marketplace does not migrate an old installation or existing context corpus.

## Documentation

- [context-core](./plugins/context-core/README.md)
- [context-decision](./plugins/context-decision/README.md)
- [Migration boundaries](./MIGRATION.md)
- [Release notes](./RELEASE_NOTES.md)
- [Development and verification](./DEVELOPMENT.md)
- [한국어 안내](./README.ko.md)

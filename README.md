# Context Plugins

Durable project context for coding agents, centered on decisions.

`context-decision` restores what the project chose, why it chose it, and which alternatives it rejected. `context-core` supplies Git/Markdown storage, bounded recall, approval previews, and the only physical write coordinator. Context is proposed only when worth keeping and written only after the user sees the complete preview and answers the capture question directly.

> Developer preview: the `0.6.0` release candidate is prepared, but the `v0.6.0` tag has not been created or pushed. Marketplace publication is also pending. The repository has no `LICENSE`; an owner must choose one before inviting public use, copying, or redistribution.

## Supported profile

The supported developer-preview profile is deliberately small:

1. Run the release checkout's profile installer once. It installs `context-core@context-plugins` and `context-decision@context-plugins` as two separate packages at the same version and scope.
2. Reload the host or start a new session.
3. Run `$context-decision:init` once in the target Git repository.

There is no bundle or meta-plugin, and decision code is not embedded in core. The root profile manifest and installer are distribution tooling only; installed plugins never install, enable, update, or replace another plugin. `context-decision:init` uses the separately installed core to initialize core storage, register the DEC area, and install the managed host policy in one idempotent operation. A separate `$context-core:init` is not required for this profile.

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
  -> complete rendered capture preview
  -> one natural-language confirmation
  -> context-core applies one transaction
```

## Install after the owner publishes `v0.6.0`

These commands intentionally use the immutable `v0.6.0` ref. They will not work until the owner approves and pushes that tag. First create one exact local checkout:

```bash
git clone --branch v0.6.0 --depth 1 https://github.com/Jeis-Jw/context-plugins.git context-plugins-v0.6.0
cd context-plugins-v0.6.0
```

### Codex

```bash
python3 scripts/install_profile.py --host codex
```

### Claude Code

Choose the explicit Claude Code installation scope for the same checkout:

```bash
python3 scripts/install_profile.py --host claude-code --scope user
```

The installer validates the exact release surface, rejects an enabled legacy provider or a marketplace pointing at another checkout, then asks the host to install core before decision. It never removes, migrates, or rolls back host state automatically. After installation, reload the host or open a new session and run `$context-decision:init` once. The installed plugins themselves do not add marketplaces, install, enable, update, or change host scope.

Optional experimental owners, after the same exact checkout is installed:

```bash
codex plugin add context-assumption@context-plugins  # experimental
codex plugin add context-term@context-plugins        # experimental
claude plugin install context-assumption@context-plugins  # experimental
claude plugin install context-term@context-plugins        # experimental
```

Run each optional owner's init once. One addon never initializes another addon.

## Safety and cost boundaries

- A durable mutation requires the complete preview and a direct, explicit, unconditional affirmative answer to its capture question. `알겠어` alone, a condition, an edit request, or a topic change is not approval; ambiguous praise is confirmed once.
- The agent keeps transport details internal. Users never see or enter digests, temporary-file locations, internal IDs, or runtime paths.
- The workflow freezes the preview before asking and does not regenerate it after approval. Repository identity, pinned runtime, CAS, lock, and atomic-write bindings remain enforced; tampering, clone/linked-worktree replay, and same-path repository recreation fail before writes.
- Semantic addons verify the release-pinned core runtime and handshake schema, `context-common/v2`, required commands, `context-owner-descriptor/v2`, and doctor state. This does not attest marketplace provenance, catalog source, or host enabled state. Low-level compatibility inputs remain available for external orchestration.
- Healthy index misses open zero indexed artifact bodies. Stale or missing index recovery opens at most 20 bodies per recall.
- Hard bounds cover body materialization/open, selected output, candidates/envelopes, and owner input. Index scoring/directory enumeration and end-to-end model tokens are not O(1).
- The common primary-claim ceiling is 2,000 codepoints. Built-in SNAP `current_context`, OBS `observation`, and DEC `decision` each use an owner-specific 1,200-codepoint ceiling. Canonical owner input is at most 8 KiB; the full candidate envelope is at most 16 KiB.
- Core and DEC `--sec-*` values are literals by default. `@file` reads a named regular UTF-8 file and `@@literal` preserves one leading `@`; path-like plain text remains literal. Experimental ASM and TERM instead receive structured candidate JSON through `--candidate @file`.

## Verification evidence

| Evidence | Result | Boundary |
|---|---|---|
| Python 3.11 full suite, 2026-08-24 | 292 passed, 220 subtests | `python3.11 -m pytest -q` |
| Python 3.13 full suite, 2026-08-24 | 292 passed, 220 subtests | `python3.13 -m pytest -q` |
| Phase 0 on both interpreters | 15 passed each | `PYTHONPATH=tests/context-v1/phase0 pythonX -m pytest -q tests/context-v1/phase0` |
| Codex `0.149.0-alpha.4.1` | Fresh install and cache lifecycle passed for core+decision | Host lifecycle evidence, not model-behavior evidence |
| Claude Code `2.1.89` | Fresh install and cache lifecycle passed for core+decision | Runtime UX remains experimental |
| Codex + Claude Code | All four plugins installed and loaded | ASM/TERM remain optional experimental surfaces |
| Actual model behavior | Unverified | No confirmed no-signal, capture-quality, or end-to-end token-usage measurement |

Codex prompt material was reduced from 3,147 to 1,331 characters, a 57.7% character reduction. This is not a token-savings claim.

## Release status

| Item | Status |
|---|---|
| Prepared version | `0.6.0` across four manifests, two catalogs, runtime/test constants, profile, and docs |
| Immutable ref | `v0.6.0` planned; tag not created or pushed |
| Repository source | Release candidate prepared on `main`; tag and publication remain separate |
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

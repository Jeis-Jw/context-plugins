# Context Plugins

[한국어](./README.ko.md)

Context Plugins gives coding agents durable, repository-owned project memory without silently turning every conversation into permanent state. The supported profile combines `context-core`, which recalls and safely writes Git/Markdown context, with `context-decision`, which preserves decisions, rationale, and rejected alternatives across sessions. The agent proposes only context worth keeping, shows the complete preview, and writes only after direct user approval.

> **Developer preview:** version `0.7.0` is prepared on `main`. The `v0.7.0` tag has not been created or pushed, and marketplace publication is also pending. The installation commands below intentionally target that immutable tag and will work only after it is published. Source availability, tests, and host lifecycle checks do not imply a tag, GitHub Release, marketplace publication, or retained user value.

## Why Context Plugins?

- A new agent session should know why the project chose its current architecture.
- Rejected alternatives should not return as if they were new ideas.
- Useful operational evidence should survive chat history without becoming authoritative by accident.
- Unverified premises should remain visibly provisional.
- Durable writes should remain reviewable, reversible Git changes owned by the repository.

Context Plugins stores selected project context, not transcripts. It first narrows candidates through indexes and metadata, then reads actual artifact bodies only when they can affect the current answer.

## Plugins

| Plugin | Purpose | Status |
|---|---|---|
| `context-core` | Scoped recall; `OBS` evidence; `SNAP` handoff; complete preview and coordinated physical writes | Required |
| `context-decision` | `DEC` decisions, rationale, rejected alternatives, conflict and rationale-change detection | Required in the supported profile |
| `context-assumption` | `ASM` records for explicitly unverified premises and their confirm/refute lifecycle | Optional, experimental |
| `context-term` | `TERM` records for project-specific canonical definitions and aliases | Optional, experimental |

There is no bundle or meta-plugin. Core and decision remain separate packages, and no plugin installs, enables, updates, or initializes another plugin implicitly. Install core and every semantic addon from the same immutable checkout; mixed or partial updates fail closed with `core_surface_mismatch`.

## Requirements and support

| Surface | Requirement or verified boundary |
|---|---|
| Python | Python 3.11+; runtime uses the standard library |
| Repository | A Git repository on macOS or Linux; the write coordinator uses POSIX `fcntl` locking |
| Codex | Plugin marketplace CLI; fresh install and cache lifecycle verified on `0.149.0-alpha.4.1` |
| Claude Code | Plugin marketplace CLI; fresh install and cache lifecycle verified on `2.1.89`; runtime UX remains experimental |
| Supported profile | `context-core@context-plugins` + `context-decision@context-plugins`, both version `0.7.0` |
| Optional surface | `context-assumption` and `context-term` are installable but experimental |
| Language | English is the canonical runtime and documentation language. User-facing responses follow an explicit user choice, then the host's preferred response language, then the established conversation language; unresolved cases fall back to English. Identifiers and machine-readable fields remain English. |

Windows is not currently supported. Exact versions above are evidence snapshots, not permanent minimum or compatibility guarantees.

## Install

The supported path starts from one clean, immutable release checkout:

```bash
git clone --branch v0.7.0 --depth 1 https://github.com/Jeis-Jw/context-plugins.git context-plugins-v0.7.0
cd context-plugins-v0.7.0
```

### Codex

```bash
python3 scripts/install_profile.py --host codex
```

### Claude Code

Choose the installation scope explicitly. The examples in this guide use user scope:

```bash
python3 scripts/install_profile.py --host claude-code --scope user
```

The installer validates release parity, registers this checkout as the `context-plugins` marketplace if needed, and installs core before decision. It stops on legacy-provider, mixed-version, disabled-plugin, or marketplace-path conflicts. It does not migrate existing context or automatically roll back a partially completed host installation.

Reload the host or start a new session after installation.

### Optional experimental owners

Install only the lifecycle you actually need, from the same checkout:

```bash
codex plugin add context-assumption@context-plugins
codex plugin add context-term@context-plugins

claude plugin install context-assumption@context-plugins --scope user
claude plugin install context-term@context-plugins --scope user
```

## Initialize a project

In the Git repository that should own the context, run:

```text
$context-decision:init
```

This one idempotent action initializes core storage, registers the DEC area, and installs the managed host policy in `AGENTS.md` for Codex or `CLAUDE.md` for Claude Code. A separate `$context-core:init` is not required for the supported profile.

If you installed an optional owner, initialize it separately:

```text
$context-assumption:init
$context-term:init
```

## First value in a few minutes

After initialization, use ordinary language; there is no command to run on every turn.

1. Give the agent a real project decision:

   > We chose HTTP-only cookies for session tokens because browser storage would expose them to injected scripts. Compare this with existing project decisions and propose a durable decision only if it should guide future work.

2. Review the complete preview. Approve only if the proposed scope, decision, rationale, and rejected alternatives are correct.
3. In a later session, ask:

   > Before changing authentication, recall the relevant project decisions and flag any conflict.

The first durable write proves the storage and approval path. Whether recall improves real work must be established separately through actual-model, repeated-use value validation.

## Daily use

| Goal | Example request |
|---|---|
| Resume with prior context | “Check the relevant project decisions and observations before continuing this task.” |
| Detect a conflict | “Before we adopt this queue, compare it with Current decisions and explain any conflict.” |
| Preserve evidence | “Propose this production result as a reusable observation, without treating it as a decision.” |
| Hand off unfinished work | “Prepare a snapshot with the current state, blockers, and next action.” |
| Change a decision | “Compare the new rationale with the Current decision and tell me whether it should be superseded.” |
| Track an unverified premise | “Record the 5-second IdP response assumption with confirmation and refutation conditions.” |
| Define a project term | “Capture what BFF means in this repository and include its accepted aliases.” |

The managed policy audits only new meaning. With no durable signal, it stays silent. When prior context can change the answer, recall happens metadata-first and selected actual bodies are compared before the response.

## Approval and safety

```text
conversation delta
  -> relevant metadata-first recall
  -> selected actual-body comparison
  -> conflict or rationale-change notice
  -> complete preview
  -> one natural-language capture question
  -> direct, explicit, unconditional approval
  -> one context-core transaction
```

- A preview, acknowledgment, praise, edit request, condition, or topic change is not approval. `Okay` or `알겠어` alone does not authorize a write. Ambiguous approval is confirmed once.
- The preview is frozen before the capture question and is never regenerated after approval.
- Internal digests, receipt locations, runtime paths, and transport IDs stay internal to the agent.
- Repository identity, pinned runtime bytes, compare-and-swap checks, lock ownership, and atomic writes are revalidated before mutation.
- `context-core` is the only physical writer. Semantic owners return validated meaning; they do not write repository files directly.
- A healthy index miss opens zero indexed artifact bodies. Stale or missing index recovery opens at most 20 bodies per recall.
- Body materialization, selected output, owner input, and candidate envelopes have hard bounds. Directory enumeration, index scoring, and end-to-end model tokens are not guaranteed to be O(1).
- Semantic owners and core validate the `context-common/v2` runtime contract. This handshake does not attest marketplace provenance or host enabled state.

## Stored artifacts

All durable context is plain Markdown under the target repository:

```text
context/
  context.index.md
  decision/       # DEC: authoritative Current decisions and superseded history
  observation/    # OBS: reusable, non-authoritative evidence
  snapshot/       # SNAP: temporary resume and handoff state
  assumption/     # ASM: provisional premises (optional)
  term/           # TERM: project-specific definitions (optional)
```

Artifacts participate in normal Git diff, review, branching, and rollback. No database, vector store, SaaS account, background transcript collector, or Obsidian installation is required.

## Remove or roll back

Uninstall optional owners first if you installed them, then remove decision before core.

### Codex

```bash
codex plugin remove context-decision@context-plugins --json
codex plugin remove context-core@context-plugins --json
codex plugin marketplace remove context-plugins --json
```

### Claude Code

Use the same scope selected during installation:

```bash
claude plugin uninstall context-decision@context-plugins --scope user
claude plugin uninstall context-core@context-plugins --scope user
claude plugin marketplace remove context-plugins
```

Host uninstall does not alter the target repository. Existing `context/` artifacts and the managed policy block remain reviewable Git content. There is no automated corpus deletion, managed-policy removal, downgrade, or storage migration command; retire or revert that repository content only through a deliberate Git-reviewed change.

The earlier `context-core@jeis-ai-plugins` coordinate is a separate distribution. This profile does not replace it or migrate its corpus automatically. See [MIGRATION.md](./MIGRATION.md).

## Verified status and limitations

| Evidence | Result | Boundary |
|---|---|---|
| Python 3.11 full suite, 2026-08-26 | 299 passed, 242 subtests | Clean temporary environment; `python3.11 -m pytest -q` |
| Python 3.13 full suite, 2026-08-26 | 299 passed, 242 subtests | `python3.13 -m pytest -q` |
| Phase 0 on both interpreters | 15 passed, 27 subtests each | Filesystem and host-inventory contract probes |
| Codex `0.149.0-alpha.4.1` | Fresh install and cache lifecycle passed for core+decision | Host lifecycle evidence, not model-behavior evidence |
| Claude Code `2.1.89` | Fresh install and cache lifecycle passed for core+decision | Runtime UX remains experimental |
| Codex + Claude Code | All four plugins installed and loaded | ASM/TERM remain optional experimental surfaces |
| Actual model behavior | Unverified | No confirmed no-signal rate, capture quality, task outcome, retained use, or end-to-end token measurement |

Codex prompt material was reduced from 3,147 to 1,333 characters, a 57.6% character reduction. This is not a token-savings claim.

Prepared manifests, local catalogs, tests, source on `main`, or an installer dry run are not evidence of a `v0.7.0` tag, GitHub Release, marketplace publication, or real-user adoption. Those remain separate publication and value gates.

## License

Context Plugins is licensed under the [Apache License 2.0](./LICENSE).

## Documentation

- [한국어 사용자 안내](./README.ko.md)
- [`context-core`](./plugins/context-core/README.md)
- [`context-decision`](./plugins/context-decision/README.md)
- [`context-assumption`](./plugins/context-assumption/README.md)
- [`context-term`](./plugins/context-term/README.md)
- [Migration boundaries](./MIGRATION.md)
- [Release notes](./RELEASE_NOTES.md)
- [Development and verification](./DEVELOPMENT.md)

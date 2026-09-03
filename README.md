# Context Plugins

[한국어](./README.ko.md)

Context Plugins gives AI coding agents a small, project-owned memory. It keeps important decisions and useful context with your project, recalls them when they matter, and saves only meaning you explicitly settle or ask it to remember.

## What the numbers say

Every claim below comes from a pre-registered, arm-blind experiment (`value-validation-v4` on the `task/value-validation-v4` branch). Three setups ran the same scenarios as fresh agent sessions with N prior decisions already stored, and two independent scorers from a different model family graded the transcripts without knowing which setup produced them.

| Prior decisions | Setup | Held true conflicts | Compatible work not blocked | Unrelated edits left alone | Mean tokens per recall session |
|---:|---|---|---|---|---:|
| 0 | No tooling | 2/4 | 2/2 | 4/8 | 72K |
| 0 | 8-line AGENTS.md convention + docs/adr | 4/4 | 2/2 | 5/8 | 103K |
| 0 | Context Plugins | 4/4 | 2/2 | 7/8 | 93K |
| 200 | No tooling | 1/2 | 1/1 | 2/4 | 255K |
| 200 | 8-line AGENTS.md convention + docs/adr | 1/2 | 0/1 | 2/4 | 342K |
| 200 | Context Plugins | 2/2 | 1/1 | 4/4 | 85K |

Codex host (gpt-5.6-sol), one repeat, eight scenarios at N=0 and four at N=200; every setup saved a stated decision faithfully (8/8). On Claude Code (Opus 5, N=0) the plugin and the convention both held 4/4 conflicts and saved 8/8; the plugin left 7/8 unrelated edits alone versus 4/8 and used about 1.4x the tokens (130K versus 93K per session).

With a handful of decisions, an eight-line convention is as good as the plugin. With two hundred, the convention and the bare agent read most of the store on every question (255K to 342K tokens) and each implemented one conflicting request anyway, while the plugin answered from its index in 85K tokens and held every conflict. That scale result exists because of a defect found on the way: at N=200 the first lean build's lexical index returned only near-topic distractors and the agent went ahead with a conflicting migration. Indexing terms from the decision body (rejected alternatives and rationale, not just the title) and matching word stems fixed that lane; on the frozen corpus, recall@8 went from 5/8 to 8/8 at N=200 and from 4/8 to 8/8 at N=1000.

## What is it?

AI coding agents are helpful, but a new conversation may forget why your project was built a certain way. Context Plugins keeps the parts that should survive between conversations:

- **Decisions** — what you chose, why you chose it, and which alternatives you rejected
- **Intents** — which durable direction the project is trying to serve
- **Observations** — test results, incidents, and other facts worth reusing
- **Archives** — immutable long-form source material adopted as evidence
- **Documents** — living project guidance whose content stays current under one stable identity
- **Snapshots** — where unfinished work stopped and what should happen next

Saved context is plain Markdown inside a filesystem vault’s `context/` folder. It can be reviewed and edited directly, then shared through any file-sharing or version-control workflow you already use. Git is optional and is never a runtime requirement.

Context Plugins does not automatically save your entire conversation. When the meaning, scope, or lifecycle effect is unresolved, the agent asks about that semantic detail; it does not show the storage file as an approval preview.

## Why use it?

- Start a new conversation without explaining the same project decisions again.
- Stop rejected ideas from returning as if they were new.
- Let the agent warn you before new work conflicts with an existing decision.
- Keep useful results and unfinished-work notes with the project instead of in one chat window.
- Stay in control: only content you explicitly settle or ask the agent to remember is permanently saved.

## Install

You need Codex or Claude Code, a project folder on macOS or Linux, and Python 3.11 or newer. You do not need to download this repository manually.

### Codex

Run these commands in a terminal:

```bash
codex plugin marketplace add Jeis-Jw/context-plugins
codex plugin add context-core@context-plugins
codex plugin add context-decision@context-plugins
```

### Claude Code

Run these commands in a terminal:

```bash
claude plugin marketplace add Jeis-Jw/context-plugins --scope user
claude plugin install context-core@context-plugins --scope user
claude plugin install context-decision@context-plugins --scope user
```

If the marketplace is already registered, skip the first command. After installation, restart the agent or open a new session.

`context-core` and `context-decision` are all you need to get started. Every semantic owner requires `context-core`, but semantic owners do not require one another. Install and initialize only the optional owners you want; installing one never installs or initializes another.

| Optional owner | Codex install | Claude Code install | Initialize in agent chat |
| --- | --- | --- | --- |
| Intent | `codex plugin add context-intent@context-plugins` | `claude plugin install context-intent@context-plugins --scope user` | `$context-intent:init` |
| Document | `codex plugin add context-document@context-plugins` | `claude plugin install context-document@context-plugins --scope user` | `$context-document:init` |
| Assumption | `codex plugin add context-assumption@context-plugins` | `claude plugin install context-assumption@context-plugins --scope user` | `$context-assumption:init` |
| Terminology | `codex plugin add context-term@context-plugins` | `claude plugin install context-term@context-plugins --scope user` | `$context-term:init` |

### How the context types relate

- **Intent** is a desired direction.
- **Observation** and **Assumption** are evidence and premises.
- **Archive** is immutable source evidence and stays out of default recall unless explicitly included.
- **Decision** is a chosen commitment.
- **Rationale** explains why the decision follows from its grounds and serves the intent.
- **Document** is living content that can be updated without changing its identity.

You can use intent-only, decision-only, or document-only storage. When the relevant artifacts coexist, a decision can record `serves:intent`, `informed_by:observation`, `informed_by:assumption`, and `affects:document` references. These links do not create inverse records or make any plugin mandatory.

Artifact limits are default-read budgets. Expand knowledge by adding stable slots, not by enlarging one slot. For example, split one design into `design-skeleton`, `design-envelope`, and `design-rules`. Keep frozen long-form originals in ARCHIVE and include them only on an explicit read.

## How to use it

### 1. Initialize your project

Open the project in Codex or Claude Code and send this message in the agent chat, not in the terminal:

```text
$context-decision:init
```

Run it once for each project. The plugin prepares the project’s `context/` folder and the instructions the agent needs.

### 2. Talk to the agent normally

You do not need special commands for everyday use. For example:

- “We decided to use Supabase because it gives us authentication and a database in one service. Remember this decision.”
- “Before changing the login flow, check whether we already made a related decision.”
- “Save this deployment result so another session can use it later.”
- “Save where we stopped and what should be done next.”

### 3. Confirm the meaning

You approve the substance in the conversation, not a generated Markdown file.

- A clear decision or explicit request to remember settled content authorizes saving it; there is no second document-preview question.
- If meaning, scope, or replacement effect is unclear, the agent asks only about that unresolved point.
- A simple acknowledgment does not approve unresolved content.
- After saving, the agent reports the result without showing the storage document.

### 4. Continue in a later conversation

When saved context is relevant, the agent can recall it automatically. You can also ask directly:

> Check the project’s saved decisions before continuing this work.

Because the context lives with the project, it can also help another agent or teammate understand the choices already made.

### 5. Branches, merges, and CI

The Markdown files under `context/` are the source of truth. The `*.index.md` files next to them are generated projections used for fast lookup; they are committed so a fresh clone works without a build step.

- When the project is a Git repository, `init` adds a managed block to `.gitattributes` so generated indexes merge as a union instead of conflicting when two branches each record a decision. If the vault sits outside a Git checkout, add `context/**/*.index.md merge=union` yourself; `doctor` reminds you with `merge_attributes_missing`.
- After a merge, the next context write re-derives the index. To do it immediately, run `context_cli.py refresh --fix index`; `context_cli.py` is the `context-core` entrypoint inside the installed plugin directory (see [DEVELOPMENT.md](./DEVELOPMENT.md)).
- If two branches recorded different decisions for the same scope and key, `doctor` reports `duplicate_current_slot`. Writes to that slot hold until one record is withdrawn or superseded; other slots keep working, and nothing is picked automatically.
- In CI, run `context_cli.py refresh --check --json` from the project root. It exits non-zero when an index drifted from the artifacts or an integrity issue exists.

Only the decision text you approved is bound to a write. If another branch merged in the meantime, the write still lands and the index is regenerated under the lock. It stops only when the target record itself changed, or a competing decision landed in the same or an overlapping scope and key.

Context Plugins is available under the [Apache License 2.0](./LICENSE).

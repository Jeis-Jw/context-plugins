# Context Plugins

[한국어](./README.ko.md)

Context Plugins gives AI coding agents a small, project-owned memory. It keeps important decisions and useful context with your project, recalls them when they matter, and asks before saving anything.

## What is it?

AI coding agents are helpful, but a new conversation may forget why your project was built a certain way. Context Plugins keeps the parts that should survive between conversations:

- **Decisions** — what you chose, why you chose it, and which alternatives you rejected
- **Intents** — which durable direction the project is trying to serve
- **Observations** — test results, incidents, and other facts worth reusing
- **Archives** — immutable long-form source material adopted as evidence
- **Documents** — living project guidance whose content stays current under one stable identity
- **Snapshots** — where unfinished work stopped and what should happen next

Saved context is plain Markdown inside a filesystem vault’s `context/` folder. It can be reviewed and edited directly, then shared through any file-sharing or version-control workflow you already use. Git is optional and is never a runtime requirement.

Context Plugins does not automatically save your entire conversation. When the agent finds something worth keeping, it shows you a preview and asks first.

## Why use it?

- Start a new conversation without explaining the same project decisions again.
- Stop rejected ideas from returning as if they were new.
- Let the agent warn you before new work conflicts with an existing decision.
- Keep useful results and unfinished-work notes with the project instead of in one chat window.
- Stay in control: nothing is permanently saved until you approve the preview.

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

### 3. Review before saving

When something is worth keeping, the agent shows the complete proposed content and asks whether to save it.

- Only a clear, direct approval of that preview saves it.
- If something is wrong, ask the agent to edit the preview.
- A simple acknowledgment does not save anything.

### 4. Continue in a later conversation

When saved context is relevant, the agent can recall it automatically. You can also ask directly:

> Check the project’s saved decisions before continuing this work.

Because the context lives with the project, it can also help another agent or teammate understand the choices already made.

Context Plugins is available under the [Apache License 2.0](./LICENSE).

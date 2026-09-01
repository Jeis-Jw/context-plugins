# Context Plugins

[한국어](./README.ko.md)

Context Plugins gives AI coding agents a small, project-owned memory. It keeps important decisions and useful context with your project, recalls them when they matter, and asks before saving anything.

## What is it?

AI coding agents are helpful, but a new conversation may forget why your project was built a certain way. Context Plugins keeps the parts that should survive between conversations:

- **Decisions** — what you chose, why you chose it, and which alternatives you rejected
- **Observations** — test results, incidents, and other facts worth reusing
- **Snapshots** — where unfinished work stopped and what should happen next

Saved context is plain Markdown inside your project’s `context/` folder. It can be reviewed, edited, and shared through Git like the rest of your project.

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

`context-core` and `context-decision` are all you need to get started. The marketplace also includes optional assumption and terminology plugins for more specialized workflows.

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

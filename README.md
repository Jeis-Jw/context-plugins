# Context Plugins

[한국어](./README.ko.md)

Context Plugins helps Codex and Claude Code remember your project. It keeps the choices you've made, the reasons behind them, and where you left off, so you can carry them into a new conversation.

## What is it?

When you build with AI, a new conversation can mean explaining your project all over again. Context Plugins keeps the important parts with your project:

- **Decisions** — what you chose and why
- **Project direction** — who you're building for and what you want to achieve
- **Lessons learned** — what worked and how you solved a problem
- **Reference material** — original documents you may want to revisit
- **Project documents** — plans and guides you update as the project grows
- **Work in progress** — where you stopped and what to do next

By default, saved notes live in your project's `context/` folder as readable Markdown documents. You can open them yourself or share them with someone working on the project.

Context Plugins does not automatically save your entire conversation. It saves only content you clearly confirm or ask it to remember.

## Why use it?

- Spend less time explaining the same decisions in every new conversation.
- Reduce repeated suggestions of ideas you've already ruled out.
- Help the AI check with you when a new request conflicts with an earlier decision.
- Pick up unfinished work using the results and next steps you've saved.

## Install

You need Codex or Claude Code, a project folder on macOS or Linux, and Python 3.11 or newer.

Choose your tool below. Paste each command into a terminal and run it one line at a time.

### Codex

```bash
codex plugin marketplace add Jeis-Jw/context-plugins
codex plugin add context-core@context-plugins
codex plugin add context-decision@context-plugins
```

### Claude Code

```bash
claude plugin marketplace add Jeis-Jw/context-plugins --scope user
claude plugin install context-core@context-plugins --scope user
claude plugin install context-decision@context-plugins --scope user
```

If you've already added this marketplace, skip the first command. After installation, restart Codex or Claude Code, or open a new session.

`context-core` and `context-decision` are all you need to get started.

<details>
<summary>Optional: remember project direction, documents, assumptions, and terminology</summary>

Choose only the features you need. Each optional feature requires `context-core`, but optional features do not require one another. Install a feature using the command for your tool, then send the command in the last column in the AI chat.

| What to remember | Codex install | Claude Code install | Set up once in the AI chat |
| --- | --- | --- | --- |
| Project direction | `codex plugin add context-intent@context-plugins` | `claude plugin install context-intent@context-plugins --scope user` | `$context-intent:init` |
| Plans and guides | `codex plugin add context-document@context-plugins` | `claude plugin install context-document@context-plugins --scope user` | `$context-document:init` |
| Assumptions to check | `codex plugin add context-assumption@context-plugins` | `claude plugin install context-assumption@context-plugins --scope user` | `$context-assumption:init` |
| Project terminology | `codex plugin add context-term@context-plugins` | `claude plugin install context-term@context-plugins --scope user` | `$context-term:init` |

</details>

## How to use it

### 1. Set up your project

Open your project in Codex or Claude Code and send this message in the AI chat:

```text
$context-decision:init
```

Run it once for each project. The plugin prepares the folders and instructions the AI needs.

### 2. Talk to the AI normally

You don't need to memorize commands for everyday use. Just ask:

- “We've decided people can use the first version without signing up. Remember this decision.”
- “Before adding a login feature, check whether we've already made a related decision.”
- “Save the problem we just solved and how we fixed it, so we can refer to it later.”
- “Save where we stopped and what should be done next.”

### 3. Confirm what to remember

When you clearly confirm a decision or say “remember this,” the AI saves it and lets you know. You don't need to approve the same content again just to save it.

If something is unclear, such as where a decision applies or whether it replaces an earlier one, the AI asks about that point first. A casual “got it” does not confirm content you haven't settled yet.

### 4. Continue in a later conversation

When saved notes are relevant to your work, the AI can refer to them in a new conversation. You can also ask directly:

> Check the project’s saved decisions before continuing this work.

Sharing the project lets another AI or someone working with you refer to the same notes.

Context Plugins is available under the [Apache License 2.0](./LICENSE).

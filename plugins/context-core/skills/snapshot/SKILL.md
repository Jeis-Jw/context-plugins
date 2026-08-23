---
name: snapshot
description: When explicitly requested, preview, save, update, load, or discard one of several named SNAP handoffs for unfinished work.
---

# Snapshot

SNAP is mutable resume context with `authority: staging`; it is not authoritative decision or evidence history.

1. Require both unfinished context and explicit handoff intent.
2. Use only the snapshot capability descriptor. `save` is create-only and fills Current context, Open items, and Next steps.
3. `update` is full replacement unless deliberate `--merge`; `load.freshness` is only a warning.
4. `discard` targets one SNAP. SNAP has no archive, history, or retired state.

Before suggesting capture, run preview and ask once with the complete rendered body. Pass preview stdout's `approval_digest` unchanged to apply; never show or request a digest, receipt path, internal ID, or core path. Only a direct, explicit, unconditional affirmative answer to that capture question is approval. `알겠어` alone, a condition, edit request, or topic change is not approval. Never regenerate the candidate, timestamp, content, or plan after approval.

Use `../context/scripts/context_cli.py snapshot ...`; preview writes nothing and context-core keeps all ID/path, repository identity, CAS, lock, and atomic-write guards.

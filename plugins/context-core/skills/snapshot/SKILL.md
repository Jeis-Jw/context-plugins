---
name: snapshot
description: When explicitly requested, preview, save, update, load, or discard one of several named SNAP handoffs for unfinished work.
---

# Snapshot

SNAP is mutable resume context with `authority: staging`; it is not authoritative decision or evidence history.

1. Require both unfinished context and explicit handoff intent.
2. Use only the snapshot descriptor from `context_cli.py capabilities --json` to build a bounded candidate and claim attestation.
3. `save` is create-only and must fill Current context, Open items, and Next steps.
4. `update` is full replacement by default; use `--merge` only for a deliberate partial update.
5. Show the complete returned bundle and call `transaction apply` only after exact `approval_digest` approval.
6. `load.freshness` is a warning label and never changes lifecycle state.
7. `discard` accepts an exact SNAP ID. SNAP has no archive, history, or retired state.

Use `../context/scripts/context_cli.py snapshot ...`. Prefer `@file` for bodies and never regenerate a candidate, timestamp, or bundle after approval.

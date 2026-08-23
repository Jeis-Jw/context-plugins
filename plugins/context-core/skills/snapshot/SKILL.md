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

Before suggesting capture, run preview and ask once with the complete rendered body. Retain its receipt path and `approval_digest` in agent state, then pass both unchanged to apply; receipt self-digests are not approval evidence and no directory scan is allowed. Never show or request a digest, receipt path, ID, or core path. Only a direct, explicit, unconditional affirmative answer to that capture question is approval. `알겠어` alone, a condition, edit request, or topic change is not approval. Never regenerate the candidate, timestamp, content, or plan after approval. Successful apply removes the receipt; a cleanup-only warning means the write succeeded and must not be retried.

Use `../context/scripts/context_cli.py snapshot ...`; preview writes nothing and context-core keeps ID/path, repository identity, CAS, lock, and atomic-write guards.

```bash
python3 /loaded/context-core/skills/context/scripts/context_cli.py snapshot save --title '<title>' --summary '<summary>' --captured-from conversation --attest-handoff-requested --attest-unfinished-context-present --sec-context '<context>' --sec-open-items '<open item>' --sec-next-steps '<next step>' --json
python3 /loaded/context-core/skills/context/scripts/context_cli.py transaction apply --receipt-file '<agent-retained result.receipt_file>' --approved-digest '<agent-retained result.approval_digest>' --json
```

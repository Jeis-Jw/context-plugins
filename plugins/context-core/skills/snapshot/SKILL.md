---
name: snapshot
description: When explicitly requested, preview, save, update, load, or discard a named SNAP handoff for unfinished work.
---

# Snapshot

SNAP is mutable resume context with `authority: staging`; it is not authoritative decision or evidence history.

1. Require both unfinished context and explicit handoff intent.
2. Use only the snapshot capability descriptor. `save` is create-only and fills Current context, Open items, and Next steps.
3. `update` is full replacement unless deliberate `--merge`; `load.freshness` is only a warning.
4. `discard` targets one SNAP. SNAP has no archive, history, or retired state.

Follow the active-language contract in `../context/references/active-language.md`. Write user-facing responses, questions, previews, and explanatory errors in the active language. Preserve user-authored artifact prose in its original language; identifiers and machine-readable fields remain English.

Treat a direct, explicit, unconditional handoff request that settles the snapshot content and scope as semantic approval. If meaning is unresolved, ask one concise semantic question; acknowledgement, praise, a condition, edit request, or topic change is not approval. Do not show the rendered file body or ask a second storage question. After approval, run internal preview, verify it adds no semantic delta, and pass its receipt path and `approval_digest` unchanged to apply in the same response. Keep all transport details private. If a delta appears, hold the write and confirm only that delta. Never regenerate the candidate, timestamp, content, or plan after approval. Receipt self-digests are damage checks, not approval evidence, and no directory scan is allowed. Successful apply removes the receipt; a cleanup-only warning means the write succeeded and must not be retried.

Use `../context/scripts/context_cli.py snapshot ...`; preview writes nothing and context-core keeps ID and path, vault identity, CAS, lock, and atomic-write guards.

```bash
python3 /loaded/context-core/skills/context/scripts/context_cli.py snapshot save --title '<title>' --summary '<summary>' --captured-from conversation --attest-handoff-requested --attest-unfinished-context-present --sec-context '<context>' --sec-open-items '<open item>' --sec-next-steps '<next step>' --json
python3 /loaded/context-core/skills/context/scripts/context_cli.py transaction apply --receipt-file '<agent-retained result.receipt_file>' --approved-digest '<agent-retained result.approval_digest>' --json
```

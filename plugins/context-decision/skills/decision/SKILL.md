---
name: decision
description: When the incremental audit detects a forming or changing choice, compare Current DEC bodies and prepare only explicit approved choices.
---

# Decision

Use this semantic owner only with a separately installed context-core. It does not audit the whole conversation again and never writes repository bytes. Read-only operations need no host inventory. Canonical init and capture verify the release-pinned core executable and handshake its schema and doctor directly; low-level calls retain caller inventory arguments only for compatibility.

1. Run only when core's incremental audit detects a choice forming or changing. Reuse a Current `{id,sha256}` only while the same scope, anchor, and actual body remain in session context. Otherwise run `check --statement ...`; its result is `coverage:discovery_only` until exact `--scope` and `--decision-key` are known. Never infer global absence of conflict from discovery-only, and repeat the exact-slot check before preview.
2. Compare actual Decision, Rationale, and Rejected alternatives. Classify `new|same|supporting|rationale_changed|conflict`; sentence similarity, hashes, IDs, and metadata are not semantic evidence.
3. Reuse `same` silently. Keep the DEC for `supporting` and consider durable new evidence as OBS. Report `rationale_changed|conflict` before the primary conclusion and ask whether to keep or supersede. `new` applies only to the returned set.
4. Claim only a caller-provided explicit choice that governs present or future action and has canonical scope plus commitment evidence. Never invent meaning or evidence. Finish the user's request before one grouped mature proposal. Do not re-propose dismissed or deferred candidates without new evidence.
5. For a normal capture, call sibling `scripts/decision_workflow.py preview --inline`. Supply semantic fields and all three `--attest-*` judgments. Candidate ID and `captured_from:conversation` are automatic; the CLI invents no semantic field, evidence, or judgment.
6. Use the loaded core skill's sibling `scripts/context_cli.py` for `--core-cli`. Canonical preview creates one private frozen receipt below `tempdir/context-decision`; never expose its path, candidate ID, or digest.
7. Before suggesting capture, run preview and ask once in the active language with the complete rendered body. Retain preview stdout's `approval_digest` in session-local agent state; never show or request it, a receipt path, internal ID, or core path. Approval is semantic and language-independent: only a direct, explicit, unconditional affirmative answer to that specific capture question qualifies. A generic acknowledgement, praise, condition, edit request, or topic change does not. Confirm ambiguity once in the active language. Apply the unchanged digest and never regenerate the capture, IDs, timestamps, plan, or content after approval.
8. For a changed slot, use `preview --supersede <current-id>`. Use `preview --withdraw <current-id> --reason <text>` to retire without a successor. History remains `do_not_follow`.
9. Use locator-free `reject --core-cli ...` to discard the current pending receipt without repository writes. Explicit receipt controls remain low-level compatibility surfaces, not canonical user inputs.
10. Use low-level `batch validate` for ordered prior-bundle composition. Core alone owns the complete final bundle, index rebuild, approval-binding gate, CAS and lock, and physical write.
11. Use `spec-view --scope ...` for a read-only projection of actual Decision and Rationale sections from exact, ancestor, and descendant Current DEC entries. Exclude History and `do_not_follow`.

Follow context-core's active-language contract. An explicit user language choice wins; otherwise use the host's preferred response language or applicable system instruction, then the established conversation language, then English. OS locale is not authoritative. Code, identifiers, filenames, quotations, and an isolated foreign term do not switch language. Use the active language for every user-facing response, question, preview, and explanatory error. Keep schema IDs, JSON keys, commands, options, error codes, filenames, and metadata in English. Preserve artifact prose without semantic translation.

```bash
python3 /loaded/context-decision/skills/decision/scripts/decision_workflow.py preview \
  --host <codex|claude-code> \
  --core-cli /loaded/context-core/skills/context/scripts/context_cli.py \
  --inline \
  --title '<title>' --summary '<summary>' --scope '<scope>' \
  --decision-key '<key>' \
  --commitment-evidence '<caller-provided evidence>' \
  --sec-decision '<decision>' --sec-rationale '<rationale>' \
  --sec-alternatives '<rejected alternative>' \
  --attest-explicit-choice --attest-scope-identified --attest-commitment-present \
  --json

python3 /loaded/context-decision/skills/decision/scripts/decision_workflow.py apply \
  --core-cli /loaded/context-core/skills/context/scripts/context_cli.py \
  --approved-digest '<agent-retained preview stdout result.approval_digest>' \
  --json
```

Inline `--sec-*` values are literal by default. `@file` reads one named regular UTF-8 file and `@@literal` preserves one leading `@`. Missing, symlinked, or oversized files fail before receipt or repository writes. Limits are 1,200 codepoints for the DEC decision, 2,000 for a common primary claim, 8 KiB for canonical owner input, and 16 KiB for the full candidate envelope.

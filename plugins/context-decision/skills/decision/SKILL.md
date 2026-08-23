---
name: decision
description: When the incremental audit detects a forming or changing choice, compare relevant Current DEC bodies, report rationale changes or conflicts, and prepare only explicit approved choices.
---

# Decision

Use this semantic owner only with a separately installed context-core. It does not audit the whole conversation again and never writes repository bytes. `check`, `search`, `read`, `brief`, `spec-view`, `conflicts`, and `revisit` are read-only and need no host inventory. Low-level write-pipeline calls retain caller `--host`, `--core-inventory @file`, and `--core-doctor @file` for compatibility. Canonical init and capture instead verify the release-pinned core executable and handshake its schema and doctor directly.

1. Run only when core's incremental audit detects a choice forming or changing. Reuse a Current `{id,sha256}` only while the same scope/anchor and actual body remain in session context. Otherwise run `check --statement ...`; this is `coverage:discovery_only` until both exact `--scope` and `--decision-key` are known. Never conclude no conflict from discovery-only, and repeat the exact-slot check before preview.
2. Compare the returned actual Decision, Rationale, and Rejected alternatives. Classify `new|same|supporting|rationale_changed|conflict`; sentence similarity, hashes, IDs, and metadata are not semantic evidence.
3. Reuse `same` silently. Keep the DEC for `supporting` and consider durable new evidence as OBS. Report `rationale_changed|conflict` before the primary conclusion and ask whether to keep or supersede. `new` applies only to the returned set.
4. Claim only a caller-provided explicit choice that governs present or future action and has canonical scope plus commitment evidence. The owner never invents meaning or evidence. Finish the user's original request before one grouped mature proposal. Do not re-propose dismissed/deferred candidates without new evidence.
5. For a normal single capture, use the loaded decision skill's sibling `scripts/decision_workflow.py preview --inline`. Supply semantic fields and all three `--attest-*` judgments; candidate ID and `captured_from:conversation` are automatic defaults, while the CLI invents no semantic field, evidence, or judgment.
6. Use the loaded core skill's sibling `scripts/context_cli.py` for `--core-cli`. Canonical preview creates one private frozen receipt below `tempdir/context-decision`; do not show or request its path, candidate ID, or digest.
7. Before suggesting capture, run preview and ask once with the complete rendered approval body. Retain preview stdout's `result.approval_digest` in session-local agent state, but never show or request the digest, receipt path, internal ID, or core path. Only a direct, explicit, unconditional affirmative answer to that capture question is approval. `알겠어` alone, a condition, edit request, or topic change is not approval; confirm ambiguous praise once. After approval, call receipt-locator-free `apply` with that exact digest through internal `--approved-digest`. Receipt self-digests are not approval evidence. Never regenerate capture, IDs, timestamps, plans, or content after approval.
8. For a changed slot, use `preview --supersede <current-id>` with the successor semantics. Use `preview --withdraw <current-id> --reason <text>` to retire without a successor. Both use the same frozen receipt and apply path; History remains `do_not_follow`.
9. Use locator-free `reject --core-cli ...` to discard the one current pending receipt without repository writes. Explicit `--candidate-id`, `--receipt-file`, and `--keep-receipt` remain low-level compatibility controls, not canonical user inputs. The public `--approved-digest` option remains because the agent, not the user, must carry the independent preview result into every apply.
10. Use low-level `batch validate` for ordered prior-bundle composition. Core alone owns the complete final bundle, index rebuild, exact-digest gate, CAS/lock, and physical write.
11. Use `spec-view --scope ...` for a read-only projection of actual Decision and Rationale sections from exact/ancestor/descendant Current DEC entries. Exclude History and `do_not_follow`.

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

Add `--supersede <current-id>` to the preview command for replacement, or use `preview --withdraw <current-id> --reason '<reason>'` for withdrawal. Use `candidate prepare`/`capture` or workflow `--candidate @file --attestation @file` only for advanced lifecycle, explicit decline, or already-frozen inputs. Inline `--sec-*` is literal by default; `@file` reads a named regular UTF-8 file and `@@literal` preserves one leading `@`. Missing, symlinked, or oversized files fail before receipt or repository writes. Limits are DEC decision 1,200 codepoints, common primary claim 2,000 codepoints, canonical owner input 8 KiB, and full candidate envelope 16 KiB.

---
name: decision
description: When the incremental audit detects a forming or changing choice, compare relevant Current DEC bodies, report rationale changes or conflicts, and prepare only explicit approved choices.
---

# Decision

Use this semantic owner only with a separately installed context-core. It does not audit the whole conversation again and never writes repository bytes. Low-level non-static CLI calls accept caller `--host`, `--core-inventory @file`, and `--core-doctor @file` for compatibility. Canonical init and capture instead verify the release-pinned core executable and handshake its schema and doctor directly.

1. Run only when core's incremental audit detects a choice forming or changing. Reuse a Current `{id,sha256}` only while the same scope/anchor and actual body remain in session context. Otherwise run `check --statement ... --scope ... --decision-key ...` before concluding or proposing capture.
2. Compare the returned actual Decision, Rationale, and Rejected alternatives. Classify `new|same|supporting|rationale_changed|conflict`; sentence similarity, hashes, IDs, and metadata are not semantic evidence.
3. Reuse `same` silently. Keep the DEC for `supporting` and consider durable new evidence as OBS. Report `rationale_changed|conflict` before the primary conclusion and ask whether to keep or supersede. `new` applies only to the returned set.
4. Claim only an explicit choice that governs present or future action and has canonical scope plus commitment evidence. Finish the user's original request before one grouped mature proposal. Do not re-propose dismissed/deferred candidates without new evidence.
5. For a normal single capture, use the loaded decision skill's sibling `scripts/decision_workflow.py preview --inline`. The caller supplies semantic fields and all three `--attest-*` judgments; the CLI serializes them but invents no evidence or judgment.
6. Use the loaded core skill's sibling `scripts/context_cli.py` for `--core-cli` and a new absolute path outside the repository for `--receipt-file`. Preview writes the exact bundle once to a sensitive mode-0600 frozen receipt.
7. The stdout user-facing `approval_digest` binds repository identity, core absolute path/SHA, candidate/result digests, and nested core bundle/digest. After the user approves that exact digest, call the same workflow's `apply`; do not regenerate capture, IDs, timestamps, plans, or content.
8. Use low-level `batch validate` for lifecycle and ordered prior-bundle composition. Core alone owns the complete final bundle, index rebuild, exact-digest gate, and physical write.
9. Use `spec-view --scope ...` for a read-only projection of actual Decision and Rationale sections from exact/ancestor/descendant Current DEC entries. Exclude History and `do_not_follow`.

```bash
python3 /loaded/context-decision/skills/decision/scripts/decision_workflow.py preview \
  --host <codex|claude-code> \
  --core-cli /loaded/context-core/skills/context/scripts/context_cli.py \
  --inline --candidate-id cand_0123456789abcdef0123456789abcdef \
  --title '<title>' --summary '<summary>' --scope '<scope>' \
  --decision-key '<key>' --captured-from conversation \
  --commitment-evidence '<caller-provided evidence>' \
  --sec-decision '<decision>' --sec-rationale '<rationale>' \
  --sec-alternatives '<rejected alternative>' \
  --attest-explicit-choice --attest-scope-identified --attest-commitment-present \
  --receipt-file /absolute/path/outside/repository/decision-receipt.json --json

python3 /loaded/context-decision/skills/decision/scripts/decision_workflow.py apply \
  --core-cli /loaded/context-core/skills/context/scripts/context_cli.py \
  --receipt-file /absolute/path/outside/repository/decision-receipt.json \
  --approved-digest sha256:<exact> --json
```

Use `candidate prepare`/`capture` or workflow `--candidate @file --attestation @file` only for advanced lifecycle, explicit decline, or already-frozen inputs. Inline `--sec-*` is literal by default; `@file` reads a named regular UTF-8 file and `@@literal` preserves one leading `@`. Missing, symlinked, or oversized files fail before receipt or repository writes. Limits are DEC decision 1,200 codepoints, common primary claim 2,000 codepoints, canonical owner input 8 KiB, and full candidate envelope 16 KiB. Delete the transient receipt manually after the workflow.

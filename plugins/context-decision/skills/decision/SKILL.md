---
name: decision
description: When the incremental audit detects a forming or changing choice, compare relevant Current DEC bodies, report rationale changes or conflicts, and prepare only explicit approved choices.
---

# Decision

Use this semantic owner only with the separately installed release-pinned context-core. It does not repeat the conversation audit or write repository bytes. Low-level calls keep `--host`, `--core-inventory @file`, and `--core-doctor @file`; canonical init and capture handshake the pinned core directly.

1. Run only for a forming or changing choice. Reuse a Current body only while its scope/anchor and bytes remain in session; otherwise run `check --statement ... --scope ... --decision-key ...` before concluding or proposing capture.
2. Compare actual Decision, Rationale, and Rejected alternatives. Classify `new|same|supporting|rationale_changed|conflict`; hashes, IDs, and metadata are not semantic evidence. Reuse `same` silently, keep supporting evidence as OBS, and report changes/conflicts before the primary conclusion.
3. Claim only a caller-provided explicit choice with canonical scope and commitment evidence. The owner never invents meaning or evidence. Finish the original request before one mature proposal; do not re-propose dismissed/deferred candidates without new evidence.
4. Normal capture uses the loaded decision skill's `scripts/decision_workflow.py preview --inline`. The agent supplies the semantic fields and three `--attest-*` judgments. Resolve sibling decision/core entrypoints internally; preview writes the bundle once to an out-of-repository frozen receipt.
5. Use low-level `batch validate` for lifecycle/ordered overlays and `spec-view --scope ...` for actual Current Decision/Rationale projection. Core alone owns final validation, repository identity, CAS, lock, index rebuild, and physical write.

Before suggesting capture, run preview and ask once with the complete rendered body. Pass preview stdout's `approval_digest` unchanged to apply; never show or request a digest, receipt path, internal ID, or core path. Only a direct, explicit, unconditional affirmative answer to that capture question is approval. `알겠어` alone, a condition, edit request, or topic change is not approval; confirm ambiguous praise once. Never regenerate capture, IDs, timestamps, plans, or content after approval.

The following command shape is agent-internal compatibility input, never user input:

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

Use `candidate prepare`/`capture` or `--candidate @file --attestation @file` only for advanced lifecycle, decline, or frozen inputs. Inline values are literal; explicit `@file` and `@@literal` remain supported. Missing, symlinked, or oversized inputs fail before receipt or repository writes. Limits remain DEC 1,200 codepoints, common claim 2,000 codepoints, owner input 8 KiB, and candidate envelope 16 KiB.

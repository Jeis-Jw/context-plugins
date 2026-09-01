---
name: decision
description: Compare Current DEC bodies on a choice signal; prepare only explicit choices.
---

# Decision

Same-major core only; Core alone writes. Init/capture bind the Core digest and validate manifests/schema/doctor; reads skip inventory.

## Recall and decide

1. Run only on core's choice signal. Reuse Current `{id,sha256}` only while its scope, anchor, and actual body remain in context. When exact `--scope` and `--decision-key` are known, run one exact-slot `decision_cli.py check`; use discovery only when either value is unknown. `coverage:discovery_only` cannot prove global absence, so check the exact slot before preview.
2. Reuse sections returned by `check` in the same turn; do not call `read`, `spec-view`, or another context read unless a section is absent or the body changed. Compare actual `Decision`, `Rationale`, `Rejected alternatives`, and non-empty `Revisit conditions`. Classify `new|same|supporting|rationale_changed|conflict`; similarity, hashes, IDs, and metadata are not evidence.
3. Reuse `same` silently; for `supporting`, keep the DEC and consider durable new evidence as OBS. Before the primary conclusion, report `rationale_changed|conflict` by quoting every returned non-empty actual section: Decision, Rationale, Rejected alternatives, and Revisit conditions. State the selected revisit token verbatim as `satisfied|no evidence|ambiguous` without invention. `satisfied` needs facts establishing the condition; the requested conflicting action is not evidence. `no evidence`: no facts or facts about another concern; `ambiguous`: relevant facts incomplete/conflicting.
4. Hold the affected action: make no code, file, or command change that performs or advances it until the user answers. Ask one explicit binary question offering both choices. Keep means the action is not performed; supersede permits it only after that explicit choice. A satisfied revisit authorizes reassessment, not implementation. The explicit choice settles that decision payload and authorizes its capture without a second storage question. `new` covers returned results only.
5. Claim only a caller-provided explicit choice governing action, with canonical scope and commitment evidence. Finish the request before one grouped mature proposal; re-propose dismissed/deferred candidates only with new evidence. If payload, scope, or lifecycle effect remains unresolved, ask only about that semantic delta.

DEC standalone; Intent optional. Relations: `serves:intent`, `informed_by:observation`, `informed_by:assumption`, and `affects:document`; Core checks kinds. Legacy `informed_by` bytes remain.

## Capture

Run sibling `scripts/decision_workflow.py preview --inline` with semantic fields and three `--attest-*` flags. ID/source are automatic. Do not pre-run host inventory or core doctor. Failure candidate paths are diagnostic only; never auto-execute or substitute. Call documented entrypoints; inspect script source only after an unexplained interface failure.

A direct, explicit, unconditional choice settling decision, scope, and lifecycle effect is semantic approval. Do not show the rendered file body or ask a second capture question. Then run internal preview, ensure its frozen receipt adds no semantic delta, and pass `approval_digest` unchanged to apply in the same response; never expose or request transport details. Acknowledgement, praise, condition, edit request, or topic change is not approval. On delta, hold and confirm it; never regenerate after approval.

Replace with `preview --supersede <current-id>`, retire with `preview --withdraw <current-id> --reason <text>`, and discard with locator-free `reject --core-cli ...`. History is `do_not_follow`. `batch validate` composes prior bundles; Core alone owns final validation and writes. Use `spec-view --scope ...` only for requested Decision/Rationale.

Follow core's active-language contract: active language for user text, English machine fields, and no semantic translation of artifact prose.

```bash
python3 /loaded/context-decision/skills/decision/scripts/decision_cli.py check \
  --statement '<forming or changing choice>' \
  --scope '<scope>' --decision-key '<key>' --json

python3 /loaded/context-decision/skills/decision/scripts/decision_workflow.py preview \
  --host <codex|claude-code> \
  --core-cli /loaded/context-core/skills/context/scripts/context_cli.py \
  --inline \
  --title '<title>' --summary '<summary>' --scope '<scope>' \
  --decision-key '<key>' --commitment-evidence '<evidence>' \
  --sec-decision '<decision>' --sec-rationale '<rationale>' \
  --sec-alternatives '<rejected alternative>' \
  --attest-explicit-choice --attest-scope-identified --attest-commitment-present \
  --json

python3 /loaded/context-decision/skills/decision/scripts/decision_workflow.py apply \
  --core-cli /loaded/context-core/skills/context/scripts/context_cli.py \
  --approved-digest '<agent-retained preview stdout result.approval_digest>' --json
```

Inline `--sec-*` is literal; `@file` reads UTF-8 and `@@literal` preserves `@`. Invalid or oversized files fail before writes. Limits: decision 1,200 codepoints, claim 2,000, input 8 KiB, envelope 16 KiB.

# Benchmarks and evidence

These measurements cover bytes and tool I/O bounds; they are not end-to-end model token measurements.

## Reproducible model-free checks

Run the committed token-I/O fixture from the repository root:

```bash
python -m pytest -q -s tests/context-v1/test_token_io_evidence.py
```

On the 0.15.0 development worktree with Python 3.13, the command emitted the following model-free observations. The fixture itself defines the corpus and assertions, so future results should be attributed to the exact commit and interpreter that produced them.

| Contract | Observed result | Committed source |
| --- | --- | --- |
| Healthy metadata miss | 2,000 Current OBS rows; 0 returned artifact bodies and 0 artifact opens | `test_identifier_like_query_is_precise_and_healthy_miss_opens_no_bodies` |
| Default stage 1 | 3,813-byte serialized result, below the 4 KiB contract | `test_stage1_pack_and_section_use_independent_byte_budgets` |
| Selected body pack | 7,803 bytes; 13 returned and 13 opened from a 5,100-record Current+History corpus | same test |
| Narrow selected body pack | 686 bytes; 1 returned and 1 opened under a caller-provided 1 KiB budget | same test |
| Candidate batch | 8 candidates accepted at 3,444 canonical bytes; 9 candidates rejected with `candidate_batch_too_large` | `test_candidate_0_1_8_9_and_exact_owner_input_boundaries` |
| Owner input | 8,192 bytes accepted and 8,193 bytes rejected | same test |
| Approval preview | 27,268-byte envelope containing 27,076 semantic-content bytes, below 32 KiB | `test_grouped_preview_accepts_complete_32k_or_less_without_semantic_truncation` |
| Addon routing | 0, 1, and 8 registered addons each retain one audit and zero router-owner subprocess invocations for an empty batch | `test_addon_count_does_not_multiply_audit_or_router_process_work` |

This command checks deterministic Python behavior, serialized byte ceilings, and instrumented file I/O. It does not measure host prompt assembly, model input tokens, latency, answer quality, or cost.

Run the committed decision-ranking regression separately:

```bash
python -m pytest -q tests/context-v1/test_recall_at_scale.py
```

That fixture checks eight frozen queries at corpus sizes 200 and 1,000. Every target must remain within eight returned bodies, at least six of eight targets must rank first at each size, non-compatible conflict/premise targets with ten component siblings must rank first or second, and high-frequency or unknown terms must open zero bodies. The corpus is synthetic and model-free; this is not a token-savings measurement or a holdout-quality claim.

## Static prompt-character check

`tests/context-v1/test_distribution_proof.py` computes this observation from all committed Codex plugin manifests:

```bash
python -m pytest -q tests/context-v1/test_distribution_proof.py::DistributionProofTests::test_public_trust_contract_matches_the_release_surface
```

For release set 0.13.0, the recorded static prompt material moved from 3,147 to 2,021 characters, a 35.8% character reduction. This is a character-count observation and not a token-savings measurement.

## Historical host experiment

Historical, one-repeat Codex experiment; raw evidence is not published in this repository. The original local sources were `value-validation-v4/RESULTS.ko.md`, `protocol.v4.json`, and the `evidence/{r1,scale200}` scorecards on the former `task/value-validation-v4` worktree. Because the corpus and raw runs are unavailable here, these figures are context, not independently reproducible release claims.

- At N=0, mean input tokens across three session types were approximately 200K for 0.13.0, 78K for lean v6, and 77K for the adr-lite comparison.
- At N=200, mean input tokens for semantic-recall sessions were 85K for lean v6 and 342K for adr-lite.
- The denominators differ: the N=0 figures cover all three session types, while the N=200 figures cover semantic recall only.
- The experiment used one repeat, eight scenarios at N=0, and four scenarios at N=200 on Codex. Lean v6 held all measured true conflicts, while its N=0 no-signal result was seven of eight.
- Claude Code behavior, repeat variance, and SNAP/DOCUMENT resume value were not measured.

The safe public conclusion is narrower than “always saves tokens”: Context Plugins pays a bounded static-instruction cost, avoids extra context calls and body reads on a healthy no-signal path, and has shown a cost and retrieval advantage as context grew in one historical experiment. Repetition and current-host generalization remain unverified.

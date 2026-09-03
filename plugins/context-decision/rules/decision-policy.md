# Decision capture policy

Run only on core's choice signal. Reuse Current while scope, anchor, and actual body remain. With known scope/key, run one exact-slot `check`; otherwise discover. Reuse returned actual Decision, Rationale, Rejected alternatives, and non-empty Revisit conditions that turn without another context read.

Classify `new|same|supporting|rationale_changed|conflict` by meaning, not hash/ID/metadata. Reuse `same|supporting` quietly. Before conclusion, quote each returned non-empty actual Decision, Rationale, Rejected alternatives, and Revisit conditions section. State the revisit token verbatim: `satisfied|no evidence|ambiguous`. `satisfied` needs facts establishing the stored condition; the requested conflicting action is not evidence. `no evidence` means no facts or another concern; `ambiguous` means relevant facts incomplete/conflicting.

Hold the affected action: no code, file, or command change may advance it before the answer. Ask one explicit binary question. Keep means the action is not performed; supersede permits it only after that explicit choice. A satisfied revisit authorizes reassessment, not implementation. The explicit choice settles that decision payload and authorizes capture without a second storage question.

Then propose one mature choice per milestone with scope/commitment. Do not re-propose dismissed/deferred without new evidence. Context-decision drafts; core writes.

Use core's active language. A direct, explicit, unconditional choice settling decision, scope, and lifecycle effect is semantic approval. Ask only unresolved meaning; acknowledgement, praise, condition, edit request, or topic change is not approval. Do not show the rendered file body or ask a second storage question. Then run one `record --approved` in the same response: internal preview, no semantic delta, unchanged apply with `approval_digest` bound internally. Keep digest, receipt path, internal ID, and core path private. On delta, confirm only that delta. Never regenerate after approval.

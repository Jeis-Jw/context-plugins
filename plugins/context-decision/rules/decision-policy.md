# Decision capture policy

Run only on core's choice signal. Reuse Current only while scope, anchor, and actual body remain in context. With known scope/key, run one exact-slot `check`; otherwise use discovery. Reuse returned actual Decision, Rationale, Rejected alternatives, and non-empty Revisit conditions that turn without another context read.

Classify `new|same|supporting|rationale_changed|conflict` by actual meaning, not hash/ID/metadata. Reuse `same|supporting` quietly. Before conclusion, quote every returned non-empty actual Decision, Rationale, Rejected alternatives, and Revisit conditions section. State the revisit token verbatim: `satisfied|no evidence|ambiguous`; invent nothing. `satisfied` needs facts establishing the stored condition; the requested conflicting action is not evidence. `no evidence`: no facts or facts about another concern. `ambiguous`: relevant facts incomplete/conflicting.

Then hold the affected action: make no code, file, or command change that performs or advances it until the user answers. Ask one explicit binary question. Keep means the action is not performed; supersede permits it only after that explicit choice. A satisfied revisit authorizes reassessment, not implementation; durable capture requires separate approval.

After the original answer, propose one mature explicit choice per milestone with scope and commitment. Do not re-propose dismissed/deferred without new evidence. Context-decision drafts; context-core alone writes.

Follow core's active language contract for user text. Before capture, preview and ask once with the complete rendered body. Pass preview stdout's `approval_digest` unchanged to apply; never expose or request the digest, receipt path, internal ID, core path, or other transport details. Only a direct, explicit, unconditional affirmative to that specific capture question is approval; acknowledgement, praise, a condition, edit request, or topic change is not. Confirm ambiguity once; never regenerate after approval.

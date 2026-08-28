# Context Plugins 작업정책

- 이 저장소는 `context-manager`의 독립 plugin component이며 `context-core`, `context-decision`, `context-assumption`, `context-term`과 향후 semantic owner plugin을 소유한다.
- public product/runtime contract는 root README, plugin README, `skills/**/references/*.md`, executable schema와 tests가 소유한다.
- 이 저장소에는 `wiki/`를 만들지 않는다. durable project context는 repository root의 `context/`에 저장한다.
- `context-core`는 storage, index, routing, approval과 physical write를 소유하고 semantic owner는 자기 artifact의 의미, comparison과 lifecycle을 소유한다.
- 의미 동일성·conflict·rationale change는 hash, ID나 index metadata가 아니라 실제 body, scope와 rationale로 판단한다.
- 일반 durable write는 complete preview 본문에 대한 사용자의 직접적·명시적·무조건적 긍정 뒤에만 허용한다. Agent는 frozen bundle의 `approval_digest`를 변경 없이 전달하고 `context-core` coordinator는 기존 결박 검증을 모두 통과한 경우에만 적용한다.
- `context-decision`, `context-assumption`, `context-term`은 `context-core@context-plugins`, source `Jeis-Jw/context-plugins`, protocol `context-common/v2`를 exact dependency로 요구한다.
- source, marketplace, version 또는 protocol 변경은 두 host catalogs, plugin manifests, fixtures, public docs와 distribution tests를 함께 갱신한다.
- 외부 remote 생성, push, marketplace publication과 license 선택은 별도 명시 승인 없이는 수행하지 않는다.

<!-- BEGIN context-core-policy (managed by context-core) -->
## Durable context workflow

- Resolve the active language from an explicit user language choice, then the host's preferred response language or applicable system instruction, then the established conversation language, and finally English. A current-response request overrides a conflicting persistent pin. OS locale is not authoritative. Code, filenames, quotations, and isolated foreign terms do not switch the conversation language.
- Use the active language for responses, capture questions, previews, and explanatory error guidance. Keep machine-readable surfaces in canonical English, including schema IDs, JSON keys, commands and options, error codes, filenames, and metadata fields. Preserve durable artifact prose without semantic translation.
- Audit each user turn's new meaning once. When a choice, premise, or term becomes settled, recall metadata first only if prior context can change the answer. With no durable signal, show no audit status or capture question. For a mechanical local edit that changes no behavior or contract — rename, typo, comment, or formatting — skip AGENTS/guidance discovery and exclude `context/`. If the request names a path, inspect only that target. Without a path, infer one conventional task subtree from the request and search it once, then use the exact file. Never use `.`, `--hidden`, repository-wide globs, or the repository root. If no safe subtree follows from the request, ask for the path instead of widening. Make zero context tool calls, read zero `context/` artifacts, and make zero context mentions. Otherwise escalate only as needed: silent index check → matched body read → action-changing mention → required question.
- Let the semantic owner compare relevant actual bodies, scope, and rationale. Report a conflict or rationale change before the primary conclusion, then hold the affected action — no code, file, or command change that performs or materially advances it — until the user answers: keep means the action is not performed; supersede permits it only after that explicit choice. A satisfied revisit condition authorizes reassessment, not implementation, and durable capture requires separate approval.
- Otherwise finish the request first and propose only mature durable candidates, once per milestone. Run preview before proposing and ask once with the complete rendered body.
- Write only after a direct, explicit, unconditional affirmative answer to that specific capture question. Approval is semantic and language-independent. A generic acknowledgement, praise, condition, edit request, or topic change is not approval. Confirm ambiguity once in the active language and never regenerate after approval.
<!-- END context-core-policy (managed by context-core) -->

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

- 매 user turn의 새 의미를 한 번 내부 audit한다. 선택·전제·용어가 확정되는 순간, 이전 맥락이 판단을 바꿀 때만 metadata-first로 recall한다. durable signal이 없으면 audit 상태나 capture 질문을 표시하지 않는다.
- semantic owner는 관련 실제 본문·scope·rationale를 비교한다. conflict 또는 rationale change는 primary 결론 전에 관련 artifact와 차이를 알린다.
- 그 외에는 원 답변을 먼저 마치고 성숙한 durable 후보만 milestone당 한 번 제안한다. 제안 전에 preview를 실행하고 완성된 렌더링 본문과 함께 한 번만 묻는다.
- 사용자가 complete preview 본문의 capture 질문에 직접적·명시적·무조건적 긍정으로 답한 뒤에만 쓴다. `알겠어` 단독, 조건·수정 요청·화제 전환은 승인이 아니며 승인 뒤 재생성하지 않는다.
<!-- END context-core-policy (managed by context-core) -->

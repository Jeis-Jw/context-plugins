# Context Plugins 작업정책

- 이 저장소는 `context-manager`의 독립 plugin component이며 `context-core`, `context-decision`, `context-assumption`, `context-term`과 향후 semantic owner plugin을 소유한다.
- public product/runtime contract는 root README, plugin README, `skills/**/references/*.md`, executable schema와 tests가 소유한다.
- 이 저장소에는 `wiki/`를 만들지 않는다. durable project context는 repository root의 `context/`에 저장한다.
- `context-core`는 storage, index, routing, approval과 physical write를 소유하고 semantic owner는 자기 artifact의 의미, comparison과 lifecycle을 소유한다.
- 의미 동일성·conflict·rationale change는 hash, ID나 index metadata가 아니라 실제 body, scope와 rationale로 판단한다.
- 일반 durable write는 complete preview의 exact approval digest를 사용하며 `context-core` coordinator만 적용한다.
- `context-decision`, `context-assumption`, `context-term`은 `context-core@context-plugins`, source `Jeis-Jw/context-plugins`, protocol `context-common/v2`를 exact dependency로 요구한다.
- source, marketplace, version 또는 protocol 변경은 두 host catalogs, plugin manifests, fixtures, public docs와 distribution tests를 함께 갱신한다.
- 외부 remote 생성, push, marketplace publication과 license 선택은 별도 명시 승인 없이는 수행하지 않는다.

<!-- BEGIN context-core-policy (managed by context-core) -->
## Durable context workflow

- 매 user turn에서 새로 추가된 의미만 같은 response pass에서 별도 model·tool 호출 없이 내부 audit한다. durable signal이 없으면 audit 상태나 capture 질문을 표시하지 않는다.
- audit은 context-core가 대화 delta당 한 번만 수행하고 addon은 신호가 자기 의미와 맞을 때만 판정한다. addon별로 대화를 다시 audit하지 않는다.
- scope·anchor, 이미 읽은 Current `{id,sha256}`, pending·dismissed 후보 참조만 session-local ephemeral ledger로 유지한다. 실제 본문을 복제하거나 repository에 쓰지 않는다.
- 이전 맥락이 판단을 바꿀 신호가 있을 때만 index metadata 먼저 recall하고 관련 실제 본문만 읽는다. 본문이 session context에 있고 scope·evidence·anchor·index와 artifact SHA가 그대로일 때만 재사용한다.
- semantic owner는 실제 본문·scope·rationale를 비교한다. hash, fingerprint, ID와 index metadata는 의미 동일성 또는 충돌의 근거가 아니다.
- conflict 또는 rationale change는 primary 결론 전에 관련 artifact와 차이를 알린다. 그 외에는 primary 요청을 먼저 끝내고, 성숙한 durable 후보만 milestone당 한 번 grouped capture로 제안한다.
- dismissed·deferred 후보는 새 근거가 생기기 전에는 다시 제안하지 않는다. Current DEC는 authoritative, OBS는 evidence, SNAP은 resume staging이다.
- context artifact와 index write는 사용자가 exact `approval_digest`를 명시 승인한 final bundle에만 허용한다.
<!-- END context-core-policy (managed by context-core) -->

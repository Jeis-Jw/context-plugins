---
name: context
description: 중앙 대화 audit에서 durable-context 신호가 생겼거나 이전 맥락이 판단을 바꿀 때, Current context를 metadata-first로 recall하고 성숙한 후보를 owner capability에 route한다.
---

# Context (한국어)

각 user turn의 새 의미만 같은 응답 pass에서 한 번 내부 audit한다. durable signal이 없으면 audit 상태, context 호출, capture 질문 없이 원래 대화를 계속한다. scope·anchor, session에 본문이 남은 Current 참조와 짧은 pending·dismissed·deferred 참조만 session-local ledger로 유지하며 저장하거나 새 근거 없이 재제안하지 않는다.

1. 이전 맥락이 판단을 바꿀 때만 metadata-first로 recall하고 선택한 실제 본문만 읽는다. healthy miss에서 임의의 body를 열지 않는다.
2. host가 발견한 semantic owner가 실제 claim·section·scope·rationale를 비교한다. hash, ID와 metadata는 의미 근거가 아니다. conflict 또는 rationale change는 primary 결론 전에 알린다.
3. 그 외에는 원 요청을 먼저 마치고 성숙한 후보만 milestone당 한 번 제안한다. plugin cache·owner process·대체 runtime을 탐색하지 않는다.
4. 최대 8개 candidate, common claim 2,000 codepoint, owner input 8 KiB, canonical batch 16 KiB 상한을 유지한다.
5. context-core는 owner result, overlay, structural profile, lifecycle, index, target bytes, repository identity, CAS, lock, atomic write를 검증한 뒤 frozen bundle만 적용하는 유일한 physical writer다.

기록 제안 전에 preview를 실행하고 완성된 렌더링 본문과 함께 한 번만 묻는다. preview stdout의 `approval_digest`는 agent가 그대로 apply에 전달하되 digest·receipt 경로·내부 ID·core 경로를 사용자에게 보이거나 요구하지 않는다. capture 질문에 대한 직접적·명시적·무조건적 긍정만 승인이다. `알겠어` 단독, 조건, 수정 요청, 화제 전환은 승인이 아니며 모호한 평가는 한 줄로 한 번만 재확인한다. 승인 뒤 candidate·timestamp·content·plan을 재생성하지 않는다.

audit, route, claim, draft, validation, preview와 거절된 apply는 repository와 host policy bytes를 변경하지 않는다.

---
name: context
description: 새 대화 delta를 audit하고 답을 바꿀 맥락만 recall해 성숙한 후보를 semantic owner로 route한다.
---

# Context (한국어)

전역 옵션: `--vault DIR`.

각 user turn의 새 의미만 한 번 audit한다. durable signal이 없으면 context tool call 0이고 audit 표시·capture 질문도 없다. 행동·계약 중립인 기계적 편집은 AGENTS/guidance 탐색을 생략하고 `context/`를 제외한다. 요청에 path가 있으면 그 target만 확인한다. 아니면 요청의 task noun으로 subtree 하나를 정해 한 번만 탐색하고 exact file만 쓴다. `.`, `--hidden`, repository-wide glob, repository root는 쓰지 않는다. 안전하지 않으면 범위를 넓히지 말고 path를 묻는다. `context/` artifact read 0, context 언급 0이다. scope·anchor, 본문이 남은 Current `{id,sha256}`, pending·dismissed·deferred 참조만 session ledger에 두고 저장·재제안하지 않는다.

1. 이전 맥락이 판단을 바꿀 때만 metadata-first로 recall한다. 필요할 때만 조용한 index 확인→match일 때 선택 본문 읽기→행동 변경 시 사용자 언급→답이 필요할 때 질문한다. healthy miss는 body를 읽지 않는다.
2. semantic owner가 실제 claim·section·scope·rationale를 비교한다. hash·ID·metadata는 의미 근거가 아니다. conflict나 rationale change를 먼저 알리고 행동을 보류한다. keep이면 수행하지 않고 supersede면 그 명시적 선택 뒤에만 진행한다. 조건 충족은 재평가 권한이지 구현 권한이 아니다. 그 선택이 decision payload를 확정하므로 별도 저장 승인을 묻지 않는다.
3. 원 요청을 먼저 마치고 성숙한 후보만 milestone당 제안한다. sibling entrypoint를 쓰고 cache scan·runtime 대체를 하지 않는다. doctor는 cache version만 나열한다. 설명되지 않는 interface failure 뒤에만 구현을 읽는다.
4. candidate 8개, common claim 2,000 codepoint, owner input 8 KiB, batch 16 KiB 상한을 유지한다.
5. core만 owner result, lifecycle, index, target bytes, vault identity, CAS, lock과 frozen bundle을 검증한 뒤 실제로 쓴다.

semantic payload·scope·lifecycle effect를 직접적·명시적·무조건적으로 확정하면 승인이다. 미확정 부분만 짧게 묻는다. 단순 확인·칭찬·조건·수정 요청·화제 전환은 승인이 아니다. 저장 파일의 렌더링 본문을 보여주거나 별도 저장 승인을 묻지 않는다. 승인 뒤 내부 preview에 semantic delta가 없음을 확인하고 `approval_digest`를 그대로 같은 응답의 apply에 전달한다. transport detail은 비공개다. delta면 write를 보류하고 그 차이만 확인한다. 승인 뒤 재생성하지 않는다.

audit, recall, routing, claiming, drafting, validation, preview와 거절된 apply는 repository와 host policy bytes를 바꾸지 않는다.

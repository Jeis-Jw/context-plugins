---
description: Apply the provisional assumption owner boundary and keep all persistence in context-core.
alwaysApply: true
---

- ASM은 검증되지 않았음을 명시한 project-scoped 전제만 claim한다.
- 관찰된 사실·근거는 OBS, 현재 따를 선택은 DEC가 소유하므로 ASM은 decline한다.
- claim attestation은 exact candidate digest와 RFC 6901 `/owner_inputs/assumption/assumption`, `/owner_inputs/assumption/unverified_ok`를 결박한다.
- confirm/refute에는 evidence ref가 필요하고 refute는 explicit impacted_decisions 결과를 남기되 DEC를 수정하지 않는다.
- supersede의 same_claim은 predecessor/successor의 실제 primary claim을 모두 직접 인용한다. ID·hash·fingerprint·index metadata는 의미 근거가 아니다.
- search/read는 assumption-relevant signal이 있을 때만 사용한다.
- receipt 발급 전 live Current source와 candidate/request에서 owner-result를 다시 생성한다. canonical area 밖 path와 symlink component는 읽지 않는다.
- 일반 operation은 exact ready doctor에서만 실행한다. partial은 명시적 init에만, invalid는 어떤 operation에도 허용하지 않는다.
- semantic owner는 repository write를 수행하지 않는다. 기록 제안 전에 preview를 실행하고 완성된 렌더링 본문과 함께 한 번만 묻는다. preview stdout의 `approval_digest`는 agent가 변경 없이 apply에 전달하되 digest·receipt 경로·내부 ID·core 경로를 사용자에게 보이거나 요구하지 않는다. capture 질문에 대한 직접적·명시적·무조건적 긍정만 승인이고 `알겠어` 단독, 조건, 수정 요청, 화제 전환에는 적용하지 않는다. 승인 뒤에는 재생성하지 않으며 durable mutation은 context-core coordinator만 적용한다.

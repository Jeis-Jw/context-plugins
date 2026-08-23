---
description: Apply the authoritative project terminology boundary and keep all persistence in context-core.
alwaysApply: true
---

- TERM은 project-specific 또는 project-special meaning이 명시된 term/definition만 claim한다. 범용 사전 의미는 decline한다.
- 관찰된 사실은 OBS, 현재 따를 선택은 DEC, 미검증 전제는 ASM이 소유하므로 TERM은 decline한다. mixed owner input도 claim하지 않는다.
- claim attestation은 exact candidate digest와 RFC 6901 `/owner_inputs/term/term`, `/owner_inputs/term/definition`을 결박한다.
- exact·ancestor·descendant scope의 Current 사이에서 실제 term, aliases, deprecated_terms canonical key 집합이 하나라도 교차하면 거부한다. 한 artifact 안의 overlap도 허용하지 않는다.
- supersede의 same_claim은 predecessor/successor의 실제 term과 definition을 모두 직접 인용한다. ID·hash·fingerprint·index metadata는 의미 근거가 아니다.
- deprecate는 이유가 필수이며 optional replacement는 다른 canonical key여야 한다. annotate는 의미 필드를 바꾸지 않는다.
- updated_at과 retired_at은 source created_at보다 빠를 수 없고, tags/search_terms item은 core common limit인 40자를 넘을 수 없다.
- search/read는 실제 용어를 만났다는 exact `term-encountered` signal이 있을 때만 사용하고, 매 term 자동 조회를 금지한다.
- receipt 발급 전 live Current source와 candidate/request에서 owner-result를 다시 생성한다. canonical area 밖 path와 symlink component는 읽지 않는다.
- 일반 operation은 exact ready doctor에서만 실행한다. partial은 명시적 init에만, invalid는 어떤 operation에도 허용하지 않는다.
- semantic owner는 repository write를 수행하지 않는다. 기록 제안 전에 preview를 실행하고 완성된 렌더링 본문과 함께 한 번만 묻는다. preview stdout의 `approval_digest`는 agent가 변경 없이 apply에 전달하되 digest·receipt 경로·내부 ID·core 경로를 사용자에게 보이거나 요구하지 않는다. capture 질문에 대한 직접적·명시적·무조건적 긍정만 승인이고 `알겠어` 단독, 조건, 수정 요청, 화제 전환에는 적용하지 않는다. 승인 뒤에는 재생성하지 않으며 durable mutation은 context-core coordinator만 적용한다.

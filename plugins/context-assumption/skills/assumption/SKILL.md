---
name: assumption
description: 중앙 audit에서 아직 검증되지 않은 project-scoped 전제가 후속 판단을 바꿀 신호가 있을 때만 ASM을 조회·비교·제안하고, 승인된 가정 lifecycle owner-result를 준비한다.
---

# Context assumption

이 skill은 `context-assumption/v1` semantic owner이며 repository를 쓰지 않는다.

- 관찰된 사실이나 확정 선택이 아닌 미검증 전제, project scope, basis가 모두 있을 때만 claim한다. 실제 claim은 `owner_inputs.assumption.assumption`과 같고 `unverified_ok=true`여야 한다.
- Attestation은 candidate에 결박된 `assumption_present → /owner_inputs/assumption/assumption`, `unverified_ok → /owner_inputs/assumption/unverified_ok`만 사용한다. OBS/DEC claim과 requested-kind-only 입력은 decline한다.
- 새 assumption·검증·반증·변경이 현재 답을 바꿀 때만 metadata-first `search --signal assumption-relevant`, 선택된 실제 본문 `read`를 사용한다.
- `confirm`은 evidence ref, `refute`는 reason/evidence/explicit impacted decisions가 필요하다. `supersede`는 양쪽 실제 `가정`의 same semantic claim일 때만, `annotate`는 의미를 보존하는 metadata에만 허용한다.
- 최대 8개, canonical batch 16 KiB를 유지하고 v2 `batch validate` 뒤 context-core preview로 넘긴다. Frozen receipt, repository identity, core SHA, CAS, lock, atomic write 검증은 그대로다.

기록 제안 전에 preview를 실행하고 완성된 렌더링 본문과 함께 한 번만 묻는다. preview stdout의 `approval_digest`는 agent가 그대로 apply에 전달하되 digest·receipt 경로·내부 ID·core 경로를 사용자에게 보이거나 요구하지 않는다. capture 질문에 대한 직접적·명시적·무조건적 긍정만 승인이다. `알겠어` 단독, 조건, 수정 요청, 화제 전환은 승인이 아니며 승인 뒤 candidate·content·plan을 재생성하지 않는다.

상세 계약은 [assumption-protocol.md](references/assumption-protocol.md)를 따른다.

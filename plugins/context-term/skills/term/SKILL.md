---
name: term
description: 중앙 audit에서 project-specific 용어와 정의 신호가 있을 때만 TERM을 claim하고, 실제 모호하거나 고유한 용어를 만났을 때 조회하며, 승인용 terminology lifecycle owner-result를 준비한다.
---

# Context term

이 skill은 `context-term/v1` semantic owner이며 repository를 쓰지 않는다.

- `project-specific|project-special-meaning` signal, substantive term/definition, canonical scope와 겹치지 않는 vocabulary key가 모두 있을 때만 claim한다. OBS·DEC·ASM mixed input, 범용 사전 정의와 requested-kind-only 입력은 decline한다.
- Attestation은 candidate에 결박된 `term_identified → /owner_inputs/term/term`, `definition_present → /owner_inputs/term/definition`만 사용한다.
- 실제 모호하거나 프로젝트 고유한 용어가 현재 답을 바꿀 때만 `search --signal term-encountered` 후 선택된 실제 본문을 `read`한다. 모든 단어·candidate·turn을 자동 조회하지 않는다.
- `supersede`는 같은 slot 양쪽 실제 term/definition이 same semantic claim일 때만, `deprecate`는 이유와 다른 optional replacement가 있을 때만, `annotate`는 의미를 보존하는 metadata에만 허용한다.
- v2 `batch validate` 뒤 context-core preview로 전달한다. Frozen receipt, repository identity, core SHA, CAS, lock, atomic write 검증은 그대로다.

기록 제안 전에 preview를 실행하고 완성된 렌더링 본문과 함께 한 번만 묻는다. preview stdout의 `approval_digest`는 agent가 그대로 apply에 전달하되 digest·receipt 경로·내부 ID·core 경로를 사용자에게 보이거나 요구하지 않는다. capture 질문에 대한 직접적·명시적·무조건적 긍정만 승인이다. `알겠어` 단독, 조건, 수정 요청, 화제 전환은 승인이 아니며 승인 뒤 candidate·content·plan을 재생성하지 않는다.

상세 계약은 [term-protocol.md](references/term-protocol.md)를 따른다.

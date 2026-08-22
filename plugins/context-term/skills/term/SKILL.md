---
name: term
description: 중앙 audit에서 project-specific 용어와 정의 신호가 있을 때만 TERM을 claim하고, 실제 모호하거나 고유한 용어를 만났을 때 조회하며, 승인용 terminology lifecycle owner-result를 준비한다.
---

# Context term

이 skill은 `context-term/v1`의 semantic owner다. 실제 persistence는 하지 않는다.

## claim

다음 조건을 모두 만족할 때만 claim한다.

1. `owner_inputs.term.project_signal`이 `project-specific` 또는 `project-special-meaning`이다.
2. `owner_inputs.term.term`과 `definition`이 substantive하며 `candidate.claim`은 실제 definition과 같다.
3. canonical project scope가 있고 term/aliases/deprecated_terms key가 서로 겹치지 않는다.
4. candidate가 OBS·DEC·ASM 경계를 함께 제안하거나 structured input으로 섞지 않는다.

attestation은 exact candidate digest에 결박하고 다음 RFC 6901 pointer를 정확히 쓴다.

- `term_identified` → `/owner_inputs/term/term`
- `definition_present` → `/owner_inputs/term/definition`

OBS의 observed/evidence claim, DEC의 explicit choice/commitment claim, ASM의 unverified premise는 이유와 함께 decline한다. 범용 사전 정의도 decline하며 requested kind만으로 claim하지 않는다.

## recall

대화·코드·문서에서 실제 모호하거나 프로젝트 고유한 용어를 만났고 정의가 현재 답을 바꿀 때만 `search --signal term-encountered`를 호출한다. metadata 결과에서 관련 ID를 고른 뒤에만 같은 signal로 `read --id ...`를 호출한다. 자연어의 모든 단어, 모든 candidate 또는 매 turn마다 자동 조회하지 않는다.

## lifecycle

- supersede: 같은 scope/term_key에서 `same-claim-input`으로 양쪽 실제 term과 definition을 읽고, 별도 model semantic 판정이 `same_semantic_claim`을 attest한 경우에만 실행한다.
- deprecate: substantive reason을 필수로 하고 optional replacement term은 다른 canonical slot만 허용한다.
- annotate: term, definition, term_key와 vocabulary를 보존하는 metadata 변경만 허용한다.

항상 `batch validate`로 descriptor/capability/result/index digest가 결박된 v2 receipt를 만든 후 context-core preview에 전달한다. 사용자의 exact `approval_digest` 승인 전에는 apply를 요청하지 않는다.

상세 계약은 [term-protocol.md](references/term-protocol.md)를 따른다.

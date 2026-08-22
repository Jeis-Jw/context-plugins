---
name: assumption
description: 중앙 audit에서 아직 검증되지 않은 project-scoped 전제가 후속 판단을 바꿀 신호가 있을 때만 ASM을 조회·비교·제안하고, 승인된 가정 lifecycle owner-result를 준비한다.
---

# Context assumption

이 skill은 `context-assumption/v1`의 semantic owner다. 실제 persistence는 하지 않는다.

## claim

다음 조건을 모두 만족할 때만 claim한다.

1. candidate가 관찰된 사실이나 확정 선택이 아니라 아직 검증되지 않은 전제다.
2. `owner_inputs.assumption.assumption`에 실제 primary claim이 있고 `candidate.claim`과 같다.
3. `owner_inputs.assumption.unverified_ok`가 `true`다.
4. project scope와 최소 한 개의 basis가 있다.

attestation은 exact candidate digest에 결박하고 다음 RFC 6901 pointer를 정확히 쓴다.

- `assumption_present` → `/owner_inputs/assumption/assumption`
- `unverified_ok` → `/owner_inputs/assumption/unverified_ok`

OBS의 observed/evidence claim과 DEC의 explicit choice/commitment claim은 이유와 함께 decline한다. requested kind만으로 claim하지 않는다.

## recall

새 assumption, 검증 신호, 반증, 같은 전제의 변경이 현재 답을 바꿀 때만 `search --signal assumption-relevant`를 호출한다. metadata 결과에서 관련 ID를 고른 뒤에만 `read --signal assumption-relevant --id ...`로 실제 본문을 읽는다. 매 turn 또는 모든 candidate마다 자동 조회하지 않는다.

## lifecycle

- confirm: evidence ref가 실제 검증 근거를 가리킬 때 `confirm` owner-result를 만든다.
- refute: reason, evidence ref와 explicit `impacted_decisions` 결과를 전달한다. DEC 변경은 별도 DEC owner flow다.
- supersede: `same-claim-input`으로 양쪽 실제 `가정`을 읽고, 별도 model semantic 판정이 `same_semantic_claim`을 attest한 경우에만 `supersede`한다.
- annotate: 의미 본문을 보존하는 metadata 변경만 허용한다.

candidate batch는 최대 8개이며 `context-capture-batch/v1` schema·audit_count·candidates 전체 canonical UTF-8 envelope가 16 KiB 이하여야 한다. 항상 `batch validate`로 descriptor/capability/result/index digest가 결박된 v2 receipt를 만든 후 context-core preview에 전달한다. 사용자의 exact `approval_digest` 승인 전에는 apply를 요청하지 않는다.

상세 계약은 [assumption-protocol.md](references/assumption-protocol.md)를 따른다.

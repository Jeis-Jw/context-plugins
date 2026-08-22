# Term protocol

## artifact

`context-term/v1`은 common frontmatter와 descriptor v2 profile을 따른다.

| 위치 | 필드 | 계약 |
|---|---|---|
| frontmatter | `scope` | required, 1..160 chars |
| frontmatter | `term` | required, 1..120 chars |
| frontmatter | `term_key` | required, term에서 결정론적으로 파생 |
| frontmatter | `aliases` | optional, 최대 12개 |
| frontmatter | `deprecated_terms` | optional, 최대 12개 |
| frontmatter | `related` | optional, 최대 12개 |
| H2 | `정의` | required primary claim |

Current authority는 `authoritative`다. `term_key`는 NFKC/case-fold 뒤 whitespace와 punctuation을 단일 `-`로 normalize한다. 각 Current의 실제 `{term, aliases, deprecated_terms}` canonical key 집합은 exact 및 ancestor/descendant scope의 다른 Current 집합과 교차할 수 없다. artifact 안에서도 세 필드의 canonical key overlap을 거부한다.

History에는 `retired_at`, `retired_reason`과 reason recipe가 요구하는 deprecation 또는 reciprocal supersession payload가 추가된다.

## claim boundary

candidate transport ID나 artifact ID는 의미 근거가 아니다. semantic attestation은 candidate canonical digest와 exact RFC 6901 pointer에 결박된다. TERM은 다음을 decline한다.

- 이미 관찰된 사실 또는 증거 자체: OBS boundary
- 받아들여 현재 따를 선택: DEC boundary
- 검증되지 않은 전제: ASM boundary
- 범용 사전 정의 또는 project-specific signal이 없는 단어

claim assertions는 `term_identified` → `/owner_inputs/term/term`, `definition_present` → `/owner_inputs/term/definition`이다. mixed owner kind와 structured foreign input은 decline한다.

## lifecycle and recall

- supersede는 같은 scope/term_key와 predecessor/successor의 실제 `{term, definition}` primary claim을 요구한다.
- deprecate는 이유가 필수고 optional replacement term은 다른 canonical key여야 한다.
- annotate는 term, definition, term_key, aliases, deprecated_terms, related를 변경할 수 없다.
- updated_at과 retired_at은 source created_at보다 빠를 수 없다.
- search/read는 실제 ambiguous 또는 project-specific term을 만났다는 exact `term-encountered` signal이 있을 때만 허용한다. 매 단어 자동 조회는 금지한다.

## owner result and persistence

TERM CLI는 `context-owner-result/v1`과 `context-owner-validation-receipt/v2`를 생성한다. receipt는 descriptor digest, capability digest, owner-result digest, physical area-index digest, same-area prior bundle 순서, generic topology와 semantic input digest를 결박한다.

receipt 발급 시 live source path/id/SHA, 실제 primary claim, exact candidate와 attestation, transition별 mutation request를 다시 읽는다. 그 입력에서 artifact drafts/effects/operations를 재생성한 결과가 제출 owner-result 전체와 같지 않으면 fail-closed한다. absolute path, `..`, `context/term` 밖 target과 symlink component는 receipt·search·read 전에 거부한다.

core는 target bytes를 descriptor로 다시 검증하고 preview/apply/lock 후 CAS를 수행한다. TERM은 repository/index 파일을 쓰지 않는다.

## init handshake

`schema`와 `capabilities`만 core 없이 호출할 수 있다. 저수준 compatibility operation은 exact host inventory와 core doctor receipt를 요구한다. 일반 operation은 ready만 허용하고, partial/invalid는 fail-closed한다. canonical init adapter는 caller-created inventory/doctor를 받지 않는다. semantic CLI의 release pin과 supplied core CLI의 absolute path suffix·SHA-256을 먼저 대조하고, 일치한 core의 schema·protocol·feature·필수 command·doctor state를 직접 handshake한다. bootstrap 뒤 public doctor와 registry/descriptor/index bytes를 사후 검증한다.

canonical byte budget은 owner input 2 KiB, candidate와 전체 candidate batch envelope 각각 16 KiB, 실제 public output 32 KiB다. common tags/search_terms item은 최대 40자다.

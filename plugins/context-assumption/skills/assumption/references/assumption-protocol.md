# Assumption protocol

## artifact

`context-assumption/v1`은 common frontmatter와 descriptor v2 profile을 따른다.

| 위치 | 필드 | 계약 |
|---|---|---|
| frontmatter | `scope` | required, 1..160 chars |
| frontmatter | `impacted_decisions` | optional, 최대 12 context IDs |
| H2 | `가정` | required primary claim |
| H2 | `근거` | required basis |
| H2 | `확정 조건` | optional |
| H2 | `반증 조건` | optional |

Current authority는 `provisional`이다. History에는 `retired_at`, `retired_reason`과 reason recipe가 요구하는 evidence/reference payload가 추가된다.

## claim boundary

candidate transport ID나 artifact ID는 의미 근거가 아니다. semantic attestation은 candidate canonical digest와 exact RFC 6901 pointer에 결박된다. ASM은 다음을 decline한다.

- 이미 관찰된 사실 또는 증거 자체: OBS boundary
- 받아들여 현재 따를 선택: DEC boundary
- 단순 질문·아이디어·희망·선호
- unverified 상태를 명시하지 않은 주장

## owner result and persistence

ASM CLI는 `context-owner-result/v1`과 `context-owner-validation-receipt/v2`를 생성한다. receipt는 descriptor digest, capability digest, owner-result digest, physical area-index digest, same-area prior bundle 순서, generic topology와 semantic input digest를 결박한다.

receipt 발급 시 live source path/id/SHA, 실제 primary claim, exact candidate와 attestation, transition별 mutation request를 다시 읽는다. 그 입력에서 artifact drafts/effects/operations를 재생성한 결과가 제출 owner-result 전체와 같지 않으면 fail-closed한다. absolute path, `..`, `context/assumption` 밖 target과 symlink component는 receipt·search·read 전에 거부한다.

core는 target bytes를 descriptor로 다시 검증하고 preview/apply/lock 후 CAS를 수행한다. ASM은 repository/index 파일을 쓰지 않는다.

## init handshake

`schema`와 `capabilities`만 core 없이 호출할 수 있다. 나머지 명령은 exact host inventory와 core doctor receipt를 요구한다. 일반 operation은 ready만 허용하고, partial은 init repair에만 허용하며 invalid는 항상 거부한다. init adapter는 inventory의 active entrypoint realpath와 supplied core CLI를 결박하고, public `schema --json`에 `context-owner-descriptor/v2`가 없으면 repository byte-noop으로 거부한다. bootstrap 뒤 public doctor와 registry/descriptor/index bytes를 사후 검증한다.

canonical byte budget은 owner input 2 KiB, candidate 16 KiB, 실제 public output 32 KiB다. candidate batch는 최대 8개이며 `context-capture-batch/v1`의 schema·audit_count·candidates 전체 canonical UTF-8 envelope가 16 KiB 이하여야 한다.

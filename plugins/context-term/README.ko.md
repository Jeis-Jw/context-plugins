# context-term (한국어)

[English](./README.md)

`context-term`은 프로젝트 안에서만 성립하는 용어와 정의의 semantic owner입니다. artifact authority는 `authoritative`이며 OBS의 관찰, DEC의 선택, ASM의 미검증 전제를 대신하지 않습니다.

## Canonical artifact 구조

- schema: `context-term/v1`
- owner/kind: `context-term` / `term`
- authority: `authoritative`
- 필수 frontmatter: `scope`, `term`, derived `term_key`
- 필수 H2 section: `Definition`
- 선택 metadata: `aliases`, `deprecated_terms`, `related`
- claim gate: `term_identified`, `definition_present`, explicit `project-specific` 또는 `project-special-meaning`

신규 artifact는 canonical 영어 `Definition` heading을 사용합니다. 기존 repository의 `정의`는 legacy 한국어 read/round-trip alias로 계속 지원하며, 기존 문서를 갱신할 때 heading과 본문 언어를 자동 변경하거나 번역하지 않습니다.

범용 사전 의미와 OBS·DEC·ASM candidate는 decline합니다. `term_key`는 Unicode NFKC, case folding, whitespace/punctuation normalization으로 결정론적으로 생성합니다. 실제 `term`, `aliases`, `deprecated_terms`의 canonical key 집합은 한 artifact 안에서나 exact·ancestor·descendant Current scope 사이에서 겹칠 수 없습니다.

같은 claim 여부는 predecessor와 successor의 실제 `term`과 `Definition` 본문을 모두 직접 인용한 `same_claim` attestation으로만 판정합니다. ID, SHA, fingerprint, title과 index metadata는 의미 동일성의 근거가 아닙니다.

## Lifecycle

- `supersede`: 같은 `(scope, term_key)`의 실제 term/definition attestation을 요구하고 reciprocal `superseded_by` / `supersedes` edge를 만듭니다.
- `deprecate`: 필수 reason과 함께 History로 retire합니다. replacement term은 선택 사항이며 같은 canonical slot을 차지할 수 없습니다.
- `annotate`: term, key, definition, aliases, deprecated terms, relation을 유지하고 descriptive metadata와 source ref만 바꿉니다.

`search`와 `read`는 실제 모호하거나 project-specific term을 만난 경우의 `--signal term-encountered`가 있을 때만 동작합니다. 모든 단어나 candidate를 자동 조회하지 않습니다. 호출마다 metadata index를 먼저 읽고 `read`는 선택한 artifact만 엽니다.

## Storage와 신뢰 경계

TERM CLI는 artifact draft, lifecycle owner result와 `context-owner-validation-receipt/v2`만 산출합니다. repository path resolution, artifact/index write, lock, CAS, approval bundle 생성과 apply는 `context-core`만 수행합니다. production TERM CLI에는 filesystem write primitive가 없습니다.

`batch validate`는 live Current source와 index를 다시 읽고 candidate·attestation·mutation request에서 transition을 재생성합니다. exact owner result가 일치할 때만 receipt를 발급하며 source path에는 canonical `context/term` containment와 symlink-free component가 필요합니다.

명시적 `$context-term:init`은 expected entrypoint suffix, 인접한 Claude/Codex manifest의 name·version, 같은 major를 만족하는 absolute core CLI만 사용합니다. 실제 entrypoint SHA-256을 계산해 operation 동안 고정하고 core schema, protocol, 필수 command, `context-owner-descriptor/v2`, doctor state를 직접 확인한 뒤 descriptor와 seed를 core bootstrap에 전달합니다. marketplace provenance나 설치 scope를 attestation하지 않으며 plugin install, update, downgrade, migration을 자동 수행하지 않습니다.

common primary claim과 TERM `definition`은 2,000 codepoint입니다. candidate와 batch envelope는 canonical UTF-8 16 KiB, owner input은 8 KiB, public output은 32 KiB입니다. lifecycle timestamp는 source `created_at`보다 빠를 수 없습니다. 일반 operation은 exact `repository_state=ready`에서만 동작하고 명시적 init은 `partial`만 수리할 수 있으며 `invalid`는 항상 fail-closed입니다.

## Public CLI

```bash
python3 skills/term/scripts/term_cli.py schema --json
python3 skills/term/scripts/term_cli.py capabilities --json
python3 skills/term/scripts/term_cli.py search \
  --signal term-encountered --query "BFF" \
  --host codex --core-inventory @inventory.json --core-doctor @doctor.json --json
```

저수준 non-static compatibility command는 caller가 제공한 host inventory와 doctor receipt가 필요합니다. canonical init은 `--core-cli`를 통해 직접 handshake합니다.

runtime 응답, 질문, preview와 설명형 안내는 active language를 따릅니다. schema ID, JSON key, CLI option, error code, filename과 metadata field는 영어로 유지합니다.

`0.9.0`에서 TERM은 `core-decision` 설치 profile 밖의 optional semantic-owner package이며 same-major core 호환성을 사용합니다. `v0.9.0` tag와 marketplace publication은 아직 완료되지 않았습니다.

`0.10.0`은 six-plugin distribution version을 맞추며 TERM semantics와 저장 bytes는 변경하지 않습니다. tag나 publication을 의미하지 않습니다.

`0.11.0`은 canonical inline preview/apply workflow와 진단용 호환 core 후보 안내를 추가합니다. TERM semantics와 저장 bytes는 변경하지 않으며 tag나 publication을 의미하지 않습니다.

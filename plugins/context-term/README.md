# context-term

`context-term`은 프로젝트 안에서만 성립하는 용어와 canonical 정의의 semantic owner다. artifact authority는 `authoritative`이며 OBS의 관찰, DEC의 선택, ASM의 미검증 전제를 대신하지 않는다.

## 소유 경계

- schema: `context-term/v1`
- owner/kind: `context-term` / `term`
- authority: `authoritative`
- required: frontmatter `scope`, `term`, derived `term_key`; H2 `정의`
- optional: `aliases`, `deprecated_terms`, `related`
- claim gates: `term_identified`, `definition_present`, explicit `project-specific` 또는 `project-special-meaning`

범용 사전 의미와 OBS·DEC·ASM candidate는 `decline`한다. `term_key`는 Unicode NFKC, case-fold, whitespace/punctuation normalization으로 결정론적으로 생성한다. 각 Current의 실제 `{term, aliases, deprecated_terms}` canonical key 집합은 exact·ancestor·descendant scope의 다른 Current 집합과 하나도 겹칠 수 없다. artifact 내부에서도 세 필드의 canonical key overlap을 거부한다.

같은 claim 여부는 predecessor와 successor의 실제 `term`과 `정의`를 모두 직접 인용한 `same_claim` attestation으로만 판정한다. ID, SHA, fingerprint, 제목과 index metadata는 의미 동일성 근거가 아니다.

## lifecycle

- `supersede`: 같은 `(scope, term_key)`의 실제 term/definition attestation을 요구하고 reciprocal `superseded_by`/`supersedes` edge를 만든다.
- `deprecate`: 이유를 필수로 기록해 History로 retire한다. replacement term은 선택 사항이며 같은 canonical slot일 수 없다.
- `annotate`: term, term_key, definition, aliases, deprecated_terms, related를 유지하고 title, summary, tags, search terms, source refs만 바꾼다.

`search`와 `read`는 대화나 작업에서 실제 모호하거나 고유한 용어를 만난 경우의 exact `--signal term-encountered`가 있을 때만 동작한다. 모든 단어 또는 모든 candidate마다 자동 조회하지 않는다. 호출 시 metadata index를 먼저 읽고 `read`는 선택된 실제 artifact 한 건만 연다.

## storage 경계

TERM CLI는 artifact draft, lifecycle owner-result와 `context-owner-validation-receipt/v2`만 산출한다. repository/index write, lock, CAS, path resolution, approval bundle 생성과 apply는 모두 `context-core`가 수행한다. TERM production CLI에는 filesystem write primitive가 없다.

`batch validate`는 embedded result를 신뢰하지 않는다. live Current source와 index를 다시 읽고 candidate·attestation·mutation request에서 transition 결과를 재생성한 뒤 exact owner-result가 일치할 때만 receipt를 발급한다. source path는 canonical `context/term` containment와 symlink-free component를 요구한다.

명시적 `$context-term:init`은 release contract가 고정한 core entrypoint path suffix와 SHA-256이 제공된 absolute `--core-cli`와 같을 때만 실행한다. 일치한 core의 schema·protocol·필수 command·`context-owner-descriptor/v2` feature와 doctor state를 직접 확인한 뒤 descriptor/seed를 core `bootstrap`에 전달하고, 실제 doctor ready와 root registry·area descriptor·index bytes를 다시 확인한다. 이 executable handshake는 marketplace provenance, catalog source 또는 host enabled state를 attestation하지 않는다. Caller-created inventory/doctor는 저수준 compatibility mode 입력일 뿐 canonical init의 신뢰 근거가 아니다. 자동 설치, update, downgrade, migration은 하지 않는다.

common primary claim과 TERM `definition`은 2,000 codepoint다. `claim`과 `decline`은 structured candidate JSON을 `--candidate @file`로 받는다. candidate와 전체 candidate batch envelope는 각각 canonical UTF-8 16 KiB, owner input은 8 KiB, public output은 실제 canonical UTF-8 32 KiB로 제한한다. common `tags`와 `search_terms` item은 core와 동일하게 40자까지 허용한다. lifecycle clock은 `updated_at`과 `retired_at`이 source `created_at`보다 빠르면 거부한다. 일반 operation은 exact `repository_state=ready`에서만 동작한다. `partial`은 명시적 init repair에만 허용하고 `invalid`는 init을 포함해 항상 거부한다.

## public CLI

```bash
python3 skills/term/scripts/term_cli.py schema --json
python3 skills/term/scripts/term_cli.py capabilities --json
python3 skills/term/scripts/term_cli.py search --signal term-encountered --query "BFF" \
  --host codex --core-inventory @inventory.json --core-doctor @doctor.json --json
```

모든 저수준 non-static compatibility 명령에는 caller-provided core host inventory와 doctor receipt가 필요하다. Canonical init은 `--core-cli`에서 직접 handshake한다.

0.5.0은 `context-term/v1` authoritative semantic owner의 첫 distribution release다. TERM은 optional addon이며 설치·활성화·init·기존 용어 문서 변환을 자동 수행하지 않고, exact core handshake와 승인형 transaction 경계를 그대로 따른다.

0.5.1은 release-pinned core path/SHA와 direct handshake, repository-bound approval, actual semantic input limits와 structured `--candidate @file` 계약을 추가한 developer-preview patch다.

0.6.0은 같은 승인 문구와 release identity를 적용하지만 TERM은 `core-decision` 설치 profile에 포함하지 않는다. 별도 semantic owner package와 optional experimental surface 경계를 유지하며 `v0.6.0` tag와 publication은 아직 완료되지 않았다.

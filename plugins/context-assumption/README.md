# context-assumption

`context-assumption`은 아직 사실로 확인되지 않았지만 이후 판단을 바꿀 수 있는 project-scoped 전제의 semantic owner다. artifact authority는 항상 `provisional`이며 OBS의 관찰·근거와 DEC의 확정 선택을 대신하지 않는다.

## 소유 경계

- schema: `context-assumption/v1`
- owner/kind: `context-assumption` / `assumption`
- authority: `provisional`
- required body: `가정`, `근거`
- optional body/metadata: `확정 조건`, `반증 조건`, `impacted_decisions`
- claim gates: `assumption_present`, `unverified_ok`

OBS처럼 관찰된 사실을 주장하거나 DEC처럼 따를 선택을 확정한 candidate는 `decline`한다. 같은 claim 여부는 predecessor와 successor의 실제 `가정` 본문을 직접 인용한 `same_claim` attestation으로만 판정한다. ID, SHA, fingerprint, 제목과 index metadata는 의미 동일성 근거가 아니다.

## lifecycle

- `confirm`: evidence ref를 남기고 `confirmed` History로 retire한다.
- `refute`: reason, evidence ref, `impacted_decisions` 결과를 남기고 `refuted` History로 retire한다. DEC 파일은 수정하지 않는다.
- `supersede`: 같은 실제 primary claim attestation을 요구하고 reciprocal `superseded_by`/`supersedes` edge를 만든다.
- `annotate`: primary claim과 조건은 유지하고 title, summary, tags, search terms, source refs만 바꾼다.

`search`와 `read`는 `--signal assumption-relevant`가 있을 때만 동작한다. 호출마다 metadata index를 먼저 읽고, `read`는 선택된 실제 artifact 한 건만 연다.

## storage 경계

ASM CLI는 artifact draft, lifecycle owner-result와 `context-owner-validation-receipt/v2`만 산출한다. repository/index write, lock, CAS, path resolution, approval bundle 생성과 apply는 모두 `context-core`가 수행한다. ASM production CLI에는 filesystem write primitive가 없다.

`batch validate`는 embedded result를 신뢰하지 않는다. live Current source와 index를 다시 읽고 candidate·attestation·mutation request에서 transition 결과를 재생성한 뒤 exact owner-result가 일치할 때만 receipt를 발급한다. source path는 canonical `context/assumption` containment와 symlink-free component를 요구한다.

명시적 `$context-assumption:init`은 release contract가 고정한 active core entrypoint suffix와 SHA-256이 제공된 absolute `--core-cli`와 같을 때만 실행한다. 일치한 core의 schema·protocol·필수 command·`context-owner-descriptor/v2` feature와 doctor state를 직접 확인한 뒤 descriptor/seed를 core `bootstrap`에 전달하고, 실제 doctor ready와 root registry·area descriptor·index bytes를 다시 확인한다. 자동 설치, update, downgrade, migration은 하지 않는다.

common primary claim은 2,000 codepoint, ASM `assumption`은 1,200 codepoint다. candidate와 candidate batch는 canonical UTF-8 16 KiB로 제한하며, batch budget은 `context-capture-batch/v1`의 schema·audit_count·candidates 전체 envelope에 적용한다. count 상한은 최대 8개다. owner input은 8 KiB, public output은 실제 canonical UTF-8 32 KiB로 제한한다. 일반 operation은 exact `repository_state=ready`에서만 동작한다. `partial`은 명시적 init repair에만 허용하고 `invalid`는 init을 포함해 항상 거부한다.

## public CLI

```bash
python3 skills/assumption/scripts/assumption_cli.py schema --json
python3 skills/assumption/scripts/assumption_cli.py capabilities --json
python3 skills/assumption/scripts/assumption_cli.py search --signal assumption-relevant --query "전제" \
  --host codex --core-inventory @inventory.json --core-doctor @doctor.json --json
```

모든 non-static 명령에는 exact core host inventory와 doctor receipt가 필요하다.

0.5.0은 `context-assumption/v1` provisional semantic owner의 첫 distribution release다. ASM은 optional addon이며 설치·활성화·init·기존 맥락 변환을 자동 수행하지 않고, exact core handshake와 승인형 transaction 경계를 그대로 따른다.

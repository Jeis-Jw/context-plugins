---
name: observation
description: 작업 중 발견한 사실·근거·시행착오가 이후에도 재사용될 가치가 있지만 authoritative decision은 아닐 때 비권위 OBS로 preview, 조회, 교정, 재검증, 무효화, supersede 또는 폐기한다.
---

# Observation (한국어)

OBS는 `authority: evidence`인 immutable semantic claim이다. DEC처럼 따를 결정으로 표현하지 않는다.

1. capture에는 substantive `관찰`과 최소 한 개의 substantive `근거`가 필요하며 capability descriptor만 사용한다.
2. `annotate`는 metadata만 바꾼다. claim/evidence 의미가 달라지면 양쪽 실제 claim을 준비해 successor OBS와 predecessor History를 한 final bundle로 `supersede`한다.
3. 반증은 이유가 있는 `invalidate`, 실제 재확인은 evidence ref가 있는 `reverify`다. 오래됨만으로 retire하지 않는다.
4. ID/path, backlink, vault identity, CAS, lock, atomic-write guard를 유지한다. preview·prepare·attestation은 write 0이다.

기록 제안 전에 preview를 실행하고 완성된 렌더링 본문과 함께 한 번만 묻는다. receipt 경로와 `approval_digest`는 agent state에만 보존해 apply에 그대로 전달한다. receipt self-digest는 승인 근거가 아니며 directory scan도 하지 않는다. digest·receipt 경로·ID·core 경로를 사용자에게 보이거나 요구하지 않는다. capture 질문에 대한 직접적·명시적·무조건적 긍정만 승인이다. `알겠어` 단독, 조건, 수정 요청, 화제 전환은 승인이 아니며 승인 뒤 content·plan을 재생성하지 않는다. 성공 시 receipt를 지우고 cleanup-only warning이면 이미 기록됐으므로 재시도하지 않는다.

CLI는 `../context/scripts/context_cli.py observation ...`을 사용하고 물리 write는 context-core만 수행한다.

```bash
python3 /loaded/context-core/skills/context/scripts/context_cli.py observation capture --title '<제목>' --summary '<요약>' --captured-from workspace --attest-reusable-observation --attest-evidence-present --sec-observation '<관찰>' --sec-evidence '<근거>' --json
python3 /loaded/context-core/skills/context/scripts/context_cli.py transaction apply --receipt-file '<agent가 유지한 result.receipt_file>' --approved-digest '<agent가 유지한 result.approval_digest>' --json
```

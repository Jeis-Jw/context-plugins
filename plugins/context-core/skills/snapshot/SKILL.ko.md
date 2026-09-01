---
name: snapshot
description: 명시적으로 요청된 unfinished session handoff를 여러 named SNAP 중 하나로 preview, 갱신, 조회 또는 폐기한다.
---

# Snapshot (한국어)

SNAP은 `authority: staging`인 mutable resume context다. 결정·관찰의 권위 기록으로 취급하지 않는다.

1. 저장 요청에 unfinished context와 handoff 의도가 모두 있는지 확인한다.
2. snapshot capability descriptor만 사용한다. `save`는 create-only이며 `현재 맥락`, `열린 항목`, `다음 단계`를 채운다.
3. `update`는 기본 full replacement이고 일부만 바꿀 때만 `--merge`다. `load.freshness`는 warning일 뿐이다.
4. `discard`는 SNAP 하나를 대상으로 한다. archive/history/retired 상태는 없다.

기록 제안 전에 preview를 실행하고 완성된 렌더링 본문과 함께 한 번만 묻는다. receipt 경로와 `approval_digest`는 agent state에만 보존해 apply에 그대로 전달한다. receipt self-digest는 승인 근거가 아니며 directory scan도 하지 않는다. digest·receipt 경로·ID·core 경로를 사용자에게 보이거나 요구하지 않는다. capture 질문에 대한 직접적·명시적·무조건적 긍정만 승인이다. `알겠어` 단독, 조건, 수정 요청, 화제 전환은 승인이 아니며 승인 뒤 candidate·timestamp·content·plan을 재생성하지 않는다. 성공 시 receipt를 지우고 cleanup-only warning이면 이미 기록됐으므로 재시도하지 않는다.

CLI는 `../context/scripts/context_cli.py snapshot ...`을 사용한다. preview는 write 0이고 context-core의 ID/path, vault identity, CAS, lock, atomic-write guard를 유지한다.

```bash
python3 /loaded/context-core/skills/context/scripts/context_cli.py snapshot save --title '<제목>' --summary '<요약>' --captured-from conversation --attest-handoff-requested --attest-unfinished-context-present --sec-context '<현재 맥락>' --sec-open-items '<열린 항목>' --sec-next-steps '<다음 단계>' --json
python3 /loaded/context-core/skills/context/scripts/context_cli.py transaction apply --receipt-file '<agent가 유지한 result.receipt_file>' --approved-digest '<agent가 유지한 result.approval_digest>' --json
```

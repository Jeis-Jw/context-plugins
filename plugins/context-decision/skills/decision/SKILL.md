---
name: decision
description: 대화의 증분 audit에서 선택 신호가 생길 때만 관련 Current DEC 실제 본문을 비교해 동일·보강·취지 변경·충돌을 알리고, 확정·승인된 선택만 DEC owner result로 만든다.
---

# Decision

context-decision은 직접 설치된 context-core가 활성 상태일 때만 사용한다. 이 skill은 대화 전체를 따로 audit하지 않는 semantic owner이며 filesystem을 쓰지 않는다. `schema`/`capabilities`를 제외한 CLI 호출은 host의 `--host`, `--core-inventory @file`, `--core-doctor @file`을 먼저 검증한다.

1. context-core의 증분 audit이 선택의 형성·변경 신호를 감지한 경우에만 동작한다. ledger의 같은 scope·anchor와 Current `{id,sha256}` 본문이 session context에도 남아 있으면 재사용한다. 본문이 없거나 scope·evidence·anchor·index 또는 artifact SHA가 바뀌었으면 결론·기록 제안 전에 `check --statement ... --scope ... --decision-key ...`를 실행한다.
2. `check`는 metadata로 후보를 줄인 뒤 관련 Current DEC의 실제 `결정`·`취지`·`반려대안`만 반환한다. 이를 읽고 `new|same|supporting|rationale_changed|conflict` 중 하나로 판정한다. 문장 유사도, hash, ID와 metadata는 의미 판정 근거가 아니다.
3. `same`은 기존 DEC를 조용히 재사용한다. `supporting`은 DEC를 유지하고 오래 재사용될 새 근거만 OBS 후보로 본다. `rationale_changed|conflict`는 primary 결론 전에 차이를 알리고 유지·변경·supersede 의도를 확인한다. `new`는 조회 범위 안의 판정일 뿐 전역 무충돌 증명이 아니다.
4. 현재 또는 미래 행동을 지배하는 명시적 선택, canonical scope와 commitment evidence가 모두 있을 때만 DEC를 claim한다. 원래 답을 먼저 마친 뒤 성숙한 후보를 grouped proposal에 한 번 포함한다. dismissed·deferred 후보는 새 evidence 전까지 다시 제안하지 않는다.
5. 일반 단일 capture는 loaded decision skill의 sibling `scripts/decision_workflow.py preview --inline`을 사용한다. caller가 semantic field와 세 `--attest-*` 판단을 명시하면 CLI는 그 값을 exact candidate·attestation으로 기계적으로 직렬화할 뿐 evidence나 판단을 발명하지 않는다.
6. `--core-cli`는 loaded core skill의 sibling `scripts/context_cli.py`, `--receipt-file`은 repository 밖의 새 절대경로다. 이 한 호출이 core doctor, owner-result 생성, `batch validate`, core preview를 수행하고 exact bundle을 frozen receipt에 한 번만 저장한다. 이 경로에서는 별도 help, schema, doctor, candidate, draft, capture 호출을 하지 않는다.
7. 사용자가 그 exact `approval_digest`를 승인한 뒤 같은 entrypoint의 `apply --receipt-file ... --approved-digest ...`를 호출한다. capture, timestamp, ID, plan 또는 content를 다시 만들지 않는다. receipt의 repository binding, core CLI SHA와 digest가 달라지면 새 preview가 필요하다.
8. 저수준 `batch validate`는 lifecycle·ordered prior bundle 조합에 사용한다. exact slot, scope overlap, acknowledgement와 ordered overlay를 구조적으로 검증하며 ordinary evidence OBS는 DEC의 `relations.informed_by`로 유지한다.
9. complete final bundle, exact digest 승인, index rebuild와 physical write는 context-core만 소유한다. decision CLI의 write 수는 항상 0이고 workflow receipt는 repository 밖의 명시적 transient 파일뿐이다.
10. 사용자가 scope의 현재 결정을 읽기용 명세로 요청하면 `spec-view --scope ...`를 사용한다. exact·ancestor·descendant Current DEC의 실제 `결정`·`취지`만 조립하며 History, 승인과 저장은 포함하지 않는다.

일반 capture의 명령 형태는 다음으로 고정한다. host/plugin cache를 탐색하지 말고 loaded skill catalog가 준 두 경로를 사용한다. `candidate-id` 예시는 실제 호출마다 caller가 새 32자리 lowercase hex 값으로 바꾼다.

```bash
python3 /loaded/context-decision/skills/decision/scripts/decision_workflow.py preview \
  --host <codex|claude-code> --core-inventory @inventory.json \
  --core-cli /loaded/context-core/skills/context/scripts/context_cli.py \
  --inline --candidate-id cand_0123456789abcdef0123456789abcdef \
  --title '<title>' --summary '<summary>' --scope '<scope>' \
  --decision-key '<key>' --captured-from conversation \
  --commitment-evidence '<caller-provided evidence>' \
  --sec-decision '<decision>' --sec-rationale '<rationale>' \
  --sec-alternatives '<rejected alternative>' \
  --attest-explicit-choice --attest-scope-identified --attest-commitment-present \
  --receipt-file /absolute/path/outside/repository/decision-receipt.json --json

python3 /loaded/context-decision/skills/decision/scripts/decision_workflow.py apply \
  --core-cli /loaded/context-core/skills/context/scripts/context_cli.py \
  --receipt-file /absolute/path/outside/repository/decision-receipt.json \
  --approved-digest sha256:<exact> --json
```

고급 lifecycle·decline 또는 이미 고정한 input을 재사용할 때만 `candidate prepare`/`capture`나 workflow의 `--candidate @file --attestation @file` mode를 사용한다.

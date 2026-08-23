---
name: decision
description: 대화의 증분 audit에서 선택 신호가 생길 때만 관련 Current DEC 실제 본문을 비교해 동일·보강·취지 변경·충돌을 알리고, 확정·승인된 선택만 DEC owner result로 만든다.
---

# Decision (한국어)

context-decision은 직접 설치된 context-core가 활성 상태일 때만 사용한다. 이 skill은 대화 전체를 따로 audit하지 않는 semantic owner이며 filesystem을 쓰지 않는다. `check`, `search`, `read`, `brief`, `spec-view`, `conflicts`, `revisit`는 read-only라 host inventory가 필요 없다. 저수준 write pipeline은 compatibility mode의 `--host`, `--core-inventory @file`, `--core-doctor @file`을 유지한다. 일반 capture workflow와 init은 caller가 만든 inventory/doctor를 받지 않고 release-pinned core CLI에서 schema와 doctor를 직접 handshake한다.

1. context-core의 증분 audit이 선택의 형성·변경 신호를 감지한 경우에만 동작한다. ledger의 같은 scope·anchor와 Current `{id,sha256}` 본문이 session context에도 남아 있으면 재사용한다. 그 외에는 먼저 `check --statement ...`를 실행한다. 정확한 `--scope`와 `--decision-key`를 둘 다 주기 전 결과는 `coverage:discovery_only`이므로 무충돌을 확정하지 않고, preview 전 exact-slot check를 다시 실행한다.
2. `check`는 metadata로 후보를 줄인 뒤 관련 Current DEC의 실제 `결정`·`취지`·`반려대안`만 반환한다. 이를 읽고 `new|same|supporting|rationale_changed|conflict` 중 하나로 판정한다. 문장 유사도, hash, ID와 metadata는 의미 판정 근거가 아니다.
3. `same`은 기존 DEC를 조용히 재사용한다. `supporting`은 DEC를 유지하고 오래 재사용될 새 근거만 OBS 후보로 본다. `rationale_changed|conflict`는 primary 결론 전에 차이를 알리고 유지·변경·supersede 의도를 확인한다. `new`는 조회 범위 안의 판정일 뿐 전역 무충돌 증명이 아니다.
4. caller가 제공한 현재 또는 미래 행동을 지배하는 명시적 선택, canonical scope와 commitment evidence가 모두 있을 때만 DEC를 claim한다. owner는 의미나 evidence를 지어내지 않는다. 원래 답을 먼저 마친 뒤 성숙한 후보를 grouped proposal에 한 번 포함한다. dismissed·deferred 후보는 새 evidence 전까지 다시 제안하지 않는다.
5. 일반 단일 capture는 loaded decision skill의 sibling `scripts/decision_workflow.py preview --inline`을 사용한다. caller가 semantic field와 세 `--attest-*` 판단을 명시하면 candidate ID와 `captured_from:conversation`은 자동 기본값이 되고, CLI는 semantic field, evidence나 판단을 발명하지 않는다.
6. `--core-cli`는 loaded core skill의 sibling `scripts/context_cli.py`를 사용한다. canonical preview는 `tempdir/context-decision` 아래 private frozen receipt 한 개를 자동 생성한다. receipt 경로, candidate ID와 digest를 사용자에게 보이거나 요구하지 않는다.
7. 기록 제안 전에 preview를 실행하고 완성된 렌더링 본문과 함께 한 번만 묻는다. preview stdout의 `approval_digest` 결과는 session-local agent state에 유지하되 digest·receipt 경로·내부 ID·core 경로를 사용자에게 보이거나 요구하지 않는다. capture 질문에 대한 직접적·명시적·무조건적 긍정만 승인이다. `알겠어` 단독, 조건, 수정 요청, 화제 전환은 승인이 아니며 모호한 평가는 한 줄로 한 번만 재확인한다. 승인 뒤 receipt locator 없는 `apply`에 그 값을 내부 `--approved-digest`로 그대로 전달한다. receipt self-digest는 승인 근거가 아니다. 승인 뒤 capture·ID·timestamp·plan·content를 재생성하지 않는다.
8. 같은 slot의 변경은 successor semantic field와 `preview --supersede <current-id>`를 사용한다. successor 없이 물리려면 `preview --withdraw <current-id> --reason <text>`를 사용한다. 둘 다 같은 frozen receipt/apply 경로를 거치고 predecessor는 History `do_not_follow`가 된다.
9. 현재 repository/core에 결박된 fresh pending receipt가 정확히 한 개일 때 locator 없는 `reject --core-cli ...`로 repository write 없이 폐기한다. `--candidate-id`, `--receipt-file`, `--keep-receipt`는 저수준 compatibility control로만 유지한다. public `--approved-digest` option은 사용자 입력이 아니라 agent가 receipt 밖 preview 결과를 모든 apply에 전달하기 위해 유지한다.
10. 저수준 `batch validate`는 ordered prior bundle 조합에 사용한다. complete final bundle, approval-binding gate, index rebuild, CAS/lock과 physical write는 context-core만 소유한다.
11. 사용자가 scope의 현재 결정을 읽기용 명세로 요청하면 `spec-view --scope ...`를 사용한다. exact·ancestor·descendant Current DEC의 실제 `결정`·`취지`만 조립하며 History, 승인과 저장은 포함하지 않는다.

일반 capture의 명령 형태는 다음으로 고정한다. host/plugin cache를 탐색하지 말고 loaded skill catalog가 준 두 경로를 사용한다.

```bash
python3 /loaded/context-decision/skills/decision/scripts/decision_workflow.py preview \
  --host <codex|claude-code> \
  --core-cli /loaded/context-core/skills/context/scripts/context_cli.py \
  --inline \
  --title '<title>' --summary '<summary>' --scope '<scope>' \
  --decision-key '<key>' \
  --commitment-evidence '<caller-provided evidence>' \
  --sec-decision '<decision>' --sec-rationale '<rationale>' \
  --sec-alternatives '<rejected alternative>' \
  --attest-explicit-choice --attest-scope-identified --attest-commitment-present \
  --json

python3 /loaded/context-decision/skills/decision/scripts/decision_workflow.py apply \
  --core-cli /loaded/context-core/skills/context/scripts/context_cli.py \
  --approved-digest '<agent가 유지한 preview stdout result.approval_digest>' \
  --json
```

replacement는 위 preview에 `--supersede <current-id>`를 더하고, withdrawal은 `preview --withdraw <current-id> --reason '<reason>'`을 사용한다. 고급 lifecycle·decline 또는 이미 고정한 input을 재사용할 때만 `candidate prepare`/`capture`나 workflow의 `--candidate @file --attestation @file` mode를 사용한다.

inline `--sec-*` 값은 plain text가 기본이다. `@file`만 named regular UTF-8 file을 읽고 `@@text`는 leading `@`를 보존한 literal이다. 일반 path-like text는 file로 추측하지 않는다. missing·symlink·8 KiB 초과 file은 receipt와 repository write 전에 실패한다. common primary claim은 2,000 codepoint, DEC `decision`은 1,200 codepoint, owner input은 canonical UTF-8 8 KiB, candidate envelope는 16 KiB다.

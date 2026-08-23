---
name: decision
description: 대화의 증분 audit에서 선택 신호가 생길 때만 관련 Current DEC 실제 본문을 비교해 동일·보강·취지 변경·충돌을 알리고, 확정·승인된 선택만 DEC owner result로 만든다.
---

# Decision (한국어)

context-decision은 별도 설치된 release-pinned context-core와 함께 사용하는 semantic owner다. 대화 audit을 반복하지 않고 repository를 쓰지 않는다. 저수준 호출은 `--host`, `--core-inventory @file`, `--core-doctor @file` compatibility 입력을 유지하며 일반 init/capture는 pinned core를 직접 handshake한다.

1. 선택의 형성·변경 신호가 있을 때만 동작한다. Current 본문을 같은 scope·anchor와 session bytes가 유지될 때만 재사용하고, 아니면 결론·기록 제안 전에 `check --statement ... --scope ... --decision-key ...`를 실행한다.
2. 실제 `결정`·`취지`·`반려대안`을 비교해 `new|same|supporting|rationale_changed|conflict`로 판정한다. hash, ID와 metadata는 의미 근거가 아니다. `same`은 조용히 재사용하고 supporting evidence는 OBS로 두며 변화·conflict는 primary 결론 전에 알린다.
3. caller가 제공한 명시적 선택·canonical scope·commitment evidence가 모두 있을 때만 claim한다. owner는 의미나 evidence를 지어내지 않는다. 원래 답을 먼저 마치고 성숙한 후보만 한 번 제안하며 새 근거 없이 dismissed·deferred 후보를 반복하지 않는다.
4. 일반 capture는 loaded decision skill의 `scripts/decision_workflow.py preview --inline`을 사용한다. agent가 semantic field와 세 `--attest-*` 판단을 제공한다. sibling decision/core entrypoint와 repository 밖 receipt는 내부에서 resolve하고 preview가 bundle을 한 번만 고정한다.
5. lifecycle/ordered overlay는 저수준 `batch validate`, 실제 Current `결정`·`취지` projection은 `spec-view --scope ...`다. complete validation, repository identity, CAS, lock, index와 physical write는 core만 소유한다.

기록 제안 전에 preview를 실행하고 완성된 렌더링 본문과 함께 한 번만 묻는다. preview stdout의 `approval_digest`는 agent가 그대로 apply에 전달하되 digest·receipt 경로·내부 ID·core 경로를 사용자에게 보이거나 요구하지 않는다. capture 질문에 대한 직접적·명시적·무조건적 긍정만 승인이다. `알겠어` 단독, 조건, 수정 요청, 화제 전환은 승인이 아니며 모호한 평가는 한 줄로 한 번만 재확인한다. 승인 뒤 capture·ID·timestamp·plan·content를 재생성하지 않는다.

다음 명령 형태는 agent 내부 compatibility 입력이며 사용자 입력이 아니다.

```bash
python3 /loaded/context-decision/skills/decision/scripts/decision_workflow.py preview \
  --host <codex|claude-code> \
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

고급 lifecycle·decline·frozen input에만 `candidate prepare`/`capture` 또는 `--candidate @file --attestation @file`을 사용한다. Inline은 literal이며 explicit `@file`과 `@@text`를 유지한다. missing·symlink·oversized input은 write 전에 실패한다. DEC 1,200 codepoint, common claim 2,000 codepoint, owner input 8 KiB, candidate envelope 16 KiB 상한을 유지한다.

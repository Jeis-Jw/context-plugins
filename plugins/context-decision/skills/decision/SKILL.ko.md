---
name: decision
description: 선택 신호가 있을 때 Current DEC 실제 본문을 비교하고 명시적으로 승인된 선택만 준비한다.
---

# Decision (한국어)

별도 설치된 같은-major context-core와 함께만 사용한다. 이 semantic owner는 대화를 재-audit하거나 repository를 쓰지 않으며 core만 실제로 쓴다. Read-only command에는 host inventory가 필요 없다. Canonical init/capture는 인접 manifest를 검증하고 actual core digest를 operation에 결박한 뒤 schema/doctor를 직접 handshake한다. Caller inventory argument는 low-level compatibility에서만 유지한다.

## 조회와 판정

1. core가 선택 신호를 낼 때만 동작한다. 같은 scope·anchor의 Current `{id,sha256}`와 실제 본문이 session context에 남아 있을 때만 재사용한다. 정확한 `--scope`와 `--decision-key`를 알면 exact-slot `decision_cli.py check`를 한 번만 실행한다. 둘 중 하나를 모를 때만 discovery를 사용한다. `coverage:discovery_only`는 전역 무충돌 증명이 아니므로 preview 전에는 exact check가 필요하다.
2. 같은 턴에서는 `check`가 반환한 section을 재사용한다. section이 없거나 본문이 바뀐 경우가 아니면 `read`, `spec-view` 또는 다른 context read를 다시 호출하지 않는다. 실제 `Decision`, `Rationale`, `Rejected alternatives`와 비어 있지 않은 `Revisit conditions`를 비교해 `new|same|supporting|rationale_changed|conflict`로 판정한다. 유사도·hash·ID·metadata는 의미 근거가 아니다.
3. `same`은 조용히 재사용하고 `supporting`은 DEC를 유지하며 오래 갈 새 근거만 OBS 후보로 본다. `rationale_changed|conflict`는 primary 결론 전에 반환된 비어 있지 않은 실제 Decision, Rationale, Rejected alternatives, Revisit conditions를 모두 원문 인용한다. 선택한 revisit token을 `satisfied|no evidence|ambiguous` 중 하나로 user response에 그대로 쓰며 근거를 발명하지 않는다. `satisfied`는 사용자가 저장 조건을 직접 성립시키는 현재 사실을 제공할 때만 쓴다. 요청된 충돌 행동 자체는 근거가 아니다. 사실이 없거나 저장 조건이 아닌 다른 쟁점에 관한 사실이면 `no evidence`, 관련 조건 사실이 불완전하거나 충돌하면 `ambiguous`다.
4. 사용자의 답까지 영향받는 행동을 보류하고 이를 수행·진행하는 code·file·command 변경을 하지 않는다. 두 선택지를 모두 제시해 하나의 명시적 양자 질문을 한다. keep이면 수행하지 않고 supersede면 그 명시적 선택 뒤에만 진행한다. 조건 충족은 재평가 권한이지 구현 권한이 아니며 durable capture 승인은 별도다. `new`는 반환 범위뿐이다.
5. 현재·미래 행동을 지배하는 명시적 선택, canonical scope, commitment evidence가 모두 caller에게서 왔을 때만 claim한다. 원래 요청을 먼저 끝내고 성숙한 후보를 한 번 묶어 제안한다. 새 근거 없이 dismissed/deferred 후보를 재제안하지 않는다.

신규 canonical section은 `Decision`, `Rationale`, `Rejected alternatives`이며 기존 한국어 heading은 legacy read/round-trip alias다.

## Capture

일반 capture는 sibling `scripts/decision_workflow.py preview --inline`에 semantic field와 세 `--attest-*` 판단을 준다. Candidate ID와 `captured_from:conversation`은 자동이다. Loaded core의 sibling `scripts/context_cli.py`를 쓰고 cache를 탐색하지 않는다. Host inventory나 core doctor를 미리 실행하지 않는다. Preview가 직접 handshake한다. 문서화된 entrypoint를 바로 호출하고 설명되지 않는 interface failure 뒤에만 script source를 읽는다.

Preview는 private frozen receipt 하나를 만든다. Active language로 완성된 렌더링 본문을 보여주며 한 번만 묻는다. preview stdout의 `approval_digest`를 session에 보관해 그대로 전달하고 digest·receipt 경로·내부 ID·core 경로 등 transport detail은 노출하거나 요구하지 않는다. 해당 질문에 대한 직접적·명시적·무조건적 긍정만 승인이다. 단순 확인·칭찬·조건·수정 요청·화제 전환은 승인이 아니다. 모호하면 한 번만 확인하며 승인 뒤 재생성하지 않는다.

교체는 `preview --supersede <current-id>`, 후속 없이 종료는 `preview --withdraw <current-id> --reason <text>`, pending 폐기는 locator 없는 `reject --core-cli ...`를 사용한다. History는 `do_not_follow`다. `batch validate`는 prior bundle을 조합하고 최종 검증과 write는 Core alone owns. 읽기용 Decision/Rationale 투영을 요청받았을 때만 `spec-view --scope ...`를 쓴다.

Context-core의 active-language contract를 따른다. 사용자용 텍스트는 active language, machine-readable surface는 English를 쓰고 artifact prose는 의미 번역하지 않는다.

```bash
python3 /loaded/context-decision/skills/decision/scripts/decision_cli.py check \
  --statement '<형성되거나 바뀌는 선택>' \
  --scope '<scope>' --decision-key '<key>' --json

python3 /loaded/context-decision/skills/decision/scripts/decision_workflow.py preview \
  --host <codex|claude-code> \
  --core-cli /loaded/context-core/skills/context/scripts/context_cli.py \
  --inline \
  --title '<title>' --summary '<summary>' --scope '<scope>' \
  --decision-key '<key>' --commitment-evidence '<evidence>' \
  --sec-decision '<decision>' --sec-rationale '<rationale>' \
  --sec-alternatives '<rejected alternative>' \
  --attest-explicit-choice --attest-scope-identified --attest-commitment-present \
  --json

python3 /loaded/context-decision/skills/decision/scripts/decision_workflow.py apply \
  --core-cli /loaded/context-core/skills/context/scripts/context_cli.py \
  --approved-digest '<agent가 보관한 preview stdout result.approval_digest>' --json
```

Inline `--sec-*`는 literal이다. `@file`만 UTF-8 file을 읽고 `@@literal`은 `@`를 보존한다. 잘못되거나 너무 큰 file은 write 전에 실패한다. 제한: DEC decision 1,200 codepoint, common claim 2,000, owner input 8 KiB, envelope 16 KiB.

---
name: decision
description: 선택 신호가 있을 때 Current DEC 실제 본문을 비교하고 명시적으로 승인된 선택만 준비한다.
---

# Decision (한국어)

같은-major context-core와 함께 쓴다. semantic owner는 대화를 재-audit하거나 쓰지 않고 core만 쓴다. `references/`, plugin manifest, `context/*.index.md`는 읽지 않는다. `check`가 index 확인이다. `--help`를 실행하지 않고 plugin script를 읽거나 grep하지 않는다. 아래 명령이 전부다. usage 오류면 명령을 그대로 다시 실행한다. 설명되지 않는 interface failure 뒤에만 script source를 읽는다.

## 조회와 판정

1. core가 선택 신호를 낼 때만 동작한다. 신호는 사용자의 확정·변경 선택이다. 호환 요청 수행은 선택이 아니므로 그 뒤 `check`를 실행하지 않는다. 같은 scope·anchor의 Current `{id,sha256}`와 실제 본문이 session context에 남아 있을 때만 재사용한다. 정확한 `--scope`와 `--decision-key`를 알면 exact-slot `decision_cli.py check`를 한 번만 실행한다. 모르면 `--statement`만으로 discovery `check`를 한 번 실행한다. `coverage:discovery_only`는 전역 무충돌 증명이 아니므로 `record` 전에 exact slot을 한 번 확인한다.
2. 같은 턴에서는 `check`가 반환한 section을 재사용한다. section이 없거나 본문이 바뀐 경우가 아니면 `read`, `spec-view` 또는 다른 context read를 다시 호출하지 않는다. 실제 `Decision`, `Rationale`, `Rejected alternatives`와 비어 있지 않은 `Revisit conditions`를 비교해 `new|same|supporting|rationale_changed|conflict`로 판정한다. 유사도·hash·ID·metadata는 의미 근거가 아니다.
3. `same`은 조용히 재사용하고 `supporting`은 DEC를 유지하며 오래 갈 새 근거만 OBS 후보로 본다. `rationale_changed|conflict`는 primary 결론 전에 반환된 비어 있지 않은 실제 Decision, Rationale, Rejected alternatives, Revisit conditions를 모두 원문 인용한다. 선택한 revisit token을 `satisfied|no evidence|ambiguous` 중 하나로 user response에 그대로 쓰며 근거를 발명하지 않는다. `satisfied`는 사용자가 저장 조건을 직접 성립시키는 현재 사실을 제공할 때만 쓴다. 요청된 충돌 행동 자체는 근거가 아니다. 사실이 없거나 저장 조건이 아닌 다른 쟁점에 관한 사실이면 `no evidence`, 관련 조건 사실이 불완전하거나 충돌하면 `ambiguous`다.
4. 사용자의 답까지 영향받는 행동을 보류하고 이를 수행·진행하는 code·file·command 변경을 하지 않는다. 두 선택지를 모두 제시해 하나의 명시적 양자 질문을 한다. keep이면 수행하지 않고 supersede면 그 명시적 선택 뒤에만 진행한다. 조건 충족은 재평가 권한이지 구현 권한이 아니다. 명시적 선택이 해당 decision payload를 확정하고 별도 저장 질문 없이 capture를 승인한다. `new`는 반환 범위뿐이다.
5. 현재·미래 행동을 지배하는 명시적 선택, canonical scope, commitment evidence가 모두 caller에게서 왔을 때만 claim한다. 원래 요청을 먼저 끝내고 성숙한 후보를 한 번 묶어 제안한다. 새 근거 없이 dismissed/deferred 후보를 재제안하지 않는다. payload·scope·lifecycle effect가 미확정이면 그 semantic delta만 묻는다.

신규 canonical section은 `Decision`, `Rationale`, `Rejected alternatives`이며 기존 한국어 heading은 legacy read/round-trip alias다.

## Capture

decision·scope·lifecycle effect를 직접적·명시적·무조건적으로 확정한 선택이나 기억 요청은 semantic approval이다. 단순 확인·칭찬·조건·수정 요청·화제 전환은 승인이 아니다. 저장 파일의 렌더링 본문을 보여주거나 별도 capture 질문을 하지 않는다. Host inventory나 core doctor를 미리 실행하지 않는다. 승인 뒤 같은 응답에서 `record --approved`를 한 번 실행한다. record는 internal preview로 frozen receipt를 만들고 `approval_digest`를 내부에서 결박해 그대로 apply한다. transport detail은 노출하거나 요구하지 않는다. record가 semantic delta나 slot conflict를 보고하면 write를 보류하고 그 차이만 확인한다. 승인 뒤 재생성하지 않는다. record 출력이 확인이며 이후 `check`를 다시 실행하거나 파일을 읽지 않는다.

교체는 `record --supersede <current-id>`, 후속 없이 종료는 `record --withdraw <current-id> --reason <text>`, pending low-level receipt 폐기는 locator 없는 `reject --core-cli ...`를 사용한다. History는 `do_not_follow`다. orchestration용 low-level 2단계 capture는 유지된다: `decision_workflow.py preview`(frozen receipt, preview stdout의 `approval_digest`) 뒤 `apply --approved-digest`.

Context-core의 active-language contract를 따른다. 사용자용 텍스트는 active language, machine-readable surface는 English를 쓰고 artifact prose는 의미 번역하지 않는다.

```bash
python3 /loaded/context-decision/skills/decision/scripts/decision_cli.py check \
  --statement '<형성되거나 바뀌는 선택>' \
  --scope '<scope>' --decision-key '<key>' --json

python3 /loaded/context-decision/skills/decision/scripts/decision_workflow.py record \
  --host <codex|claude-code> --inline --approved \
  --title '<title>' --summary '<summary>' --scope '<scope>' \
  --decision-key '<key>' --commitment-evidence '<evidence>' \
  --sec-decision '<decision>' --sec-rationale '<rationale>' \
  --sec-alternatives '<rejected alternative>' --sec-revisit '<revisit condition>' \
  --attest-explicit-choice --attest-scope-identified --attest-commitment-present \
  --json
```

`/loaded/...`는 이 파일의 skill catalog 경로에서 푼다. sibling core는 자동으로 찾는다(`core_cli_required` 오류 뒤에만 `--core-cli <path>`를 추가한다). Inline `--sec-*`는 literal이다. `@file`만 UTF-8 file을 읽고 `@@literal`은 `@`를 보존한다. 제한: DEC decision 1,200 codepoint, common claim 2,000, owner input 8 KiB, envelope 16 KiB.

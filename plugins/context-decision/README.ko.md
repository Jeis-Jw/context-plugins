# context-decision (한국어)

`context-decision`은 “무엇을 결정했고, 왜 그 결정을 따르며, 어떤 대안을 반려했는가”를 다음 agent와 session에서 바로 복원하는 decision continuity plugin입니다. 현재 DEC는 authoritative하며 superseded history는 `do_not_follow`로 표시됩니다.

## Manual hard dependency

요구 좌표는 marketplace `context-plugins`, plugin `context-core`, selector `context-core@context-plugins`, source `Jeis-Jw/context-plugins`, protocol `context-common/v2`입니다. 동명 plugin이나 다른 marketplace source는 대체하지 못합니다.

1. 지원 profile은 immutable `v0.7.0` checkout의 root installer를 사용자가 한 번 실행해 exact core와 decision을 같은 version·scope의 독립 package로 설치합니다.
2. host를 reload하거나 새 session을 엽니다.
3. `$context-decision:init`을 한 번 호출합니다.
4. installed core public bootstrap이 필요한 core seed와 decision area를 적용하고, 현재 host의 `AGENTS.md` 또는 `CLAUDE.md`에 context 운영지침 managed block을 설치합니다. ready 재호출은 모두 noop입니다.

Root installer는 명시적으로 실행하는 배포 도구일 뿐 bundle/meta-plugin이 아닙니다. `context-decision` 자체는 marketplace add, install, enable, update 또는 host configuration 변경을 자동 실행하지 않습니다. Manifest에도 dependency나 implicit/default install metadata가 없고 core 구현을 내장하지 않습니다. Canonical init과 workflow는 subprocess 전에 release-pinned core runtime을 확인하고, 일치한 executable에서 `context-core-schema/v1`, `context-common/v2`, required doctor/transaction/bootstrap command, `context-owner-descriptor/v2` feature와 doctor state를 직접 handshake합니다. 이 검사는 marketplace provenance, catalog source 또는 host enabled state를 attestation하지 않습니다. Caller-created inventory/doctor는 저수준 compatibility mode의 입력일 뿐 canonical 경로의 신뢰 근거가 아닙니다.

core와 decision은 같은 immutable release checkout에서 함께 설치·update해야 합니다. Decision이 exact core entrypoint bytes를 고정하므로 혼합 설치나 일부만 update한 상태는 `core_surface_mismatch`로 중단됩니다. core와 decision을 같은 release로 맞추고 host reload 뒤 재시도합니다.

## Exact failure UX

- `core_missing`: source `Jeis-Jw/context-plugins`의 `context-core@context-plugins`를 사용자가 선택한 scope에 직접 설치하고 reload 또는 새 session 뒤 `context-decision:init`을 재시도합니다.
- `core_source_mismatch`: source `Jeis-Jw/context-plugins`의 exact selector를 사용자가 선택한 scope에 직접 설치하고 다른 marketplace의 동명 plugin을 사용하지 않습니다. reload 또는 새 session 뒤 `context-decision:init`을 재시도합니다.
- `core_disabled`: source `Jeis-Jw/context-plugins`의 exact core를 사용자가 선택한 올바른 scope에서 직접 활성화하고 reload 또는 새 session 뒤 `context-decision:init`을 재시도합니다.
- `core_incompatible`: source `Jeis-Jw/context-plugins`의 exact core를 사용자가 선택한 scope에서 `context-common/v2` 호환 버전으로 직접 업데이트하고 reload 또는 새 session 뒤 `context-decision:init`을 재시도합니다.
- `core_uninitialized`: plugin 설치 문제가 아닙니다. installed `context-core` public `bootstrap` surface가 같은 호출에서 core seed와 decision area를 순서대로 적용합니다. 별도 core init 호출은 필요하지 않습니다.
이 failure UX는 host inventory와 doctor receipt를 caller가 제공하는 저수준 compatibility mode에 적용됩니다. missing/source mismatch/disabled/incompatible 실패는 exact source와 manual action을 표시하며 repository와 host configuration bytes를 바꾸지 않습니다. Storage-level `context_root_missing`은 core read surface의 별도 오류이며 addon preflight에서는 installed core의 bootstrap-required `core_uninitialized`로 분류합니다. doctor의 partial/invalid `issues|warnings`는 성공 preflight의 diagnostics로 전달합니다.

Host는 `schema`/`capabilities`를 제외한 모든 저수준 compatibility CLI 호출에 `--host`, `--core-inventory @file`, `--core-doctor @file`을 전달합니다. canonical init과 일반 `decision_workflow.py preview --inline`은 caller-created inventory/doctor 대신 release-pinned core CLI의 schema와 doctor를 직접 handshake합니다. workflow는 caller가 명시한 semantic field와 세 attestation을 exact input에 결박해 approval preview를 만들며 evidence나 판단을 발명하지 않습니다. 고급 lifecycle·decline에는 `candidate prepare`와 `capture`를 사용하며 fact/idea는 draft 없이 종료합니다.

inline `--sec-*`는 plain text가 기본이며 explicit `@file`과 leading `@` literal용 `@@literal`을 지원합니다. 일반 path-like text는 file로 추측하지 않습니다. common primary-claim protocol 상한은 2,000 codepoint이고 built-in SNAP `current_context`, OBS `observation`, DEC `decision`은 각각 owner-specific 1,200 codepoint입니다. owner input은 canonical UTF-8 8 KiB, candidate envelope는 16 KiB입니다. missing·symlink·oversized body file과 limit 초과는 receipt/repository write 전에 실제 크기 진단과 함께 실패합니다.

Agent는 기록 제안 전에 complete preview의 완성된 렌더링 본문을 만들고 한 번만 묻습니다. 그 capture 질문에 대한 직접적·명시적·무조건적 긍정만 승인입니다. `알겠어` 단독, 조건, 수정 요청, 화제 전환은 승인이 아니며 모호한 평가는 한 줄로 한 번만 재확인합니다. 수정 요청은 새 preview와 새 질문으로 처리합니다.

사용자는 digest, 임시 파일 위치, 내부 ID나 core 경로를 보거나 입력하지 않습니다. Workflow는 질문 전에 repository identity, pinned runtime, semantic result, nested core bundle, CAS와 lock 결박을 고정하고 승인 뒤 재생성하지 않습니다. Tampering, clone·linked-worktree·same-path replay, runtime 변경과 잘못된 승인 material은 repository write 전에 실패합니다.

## Product flow

context-core가 각 대화 delta를 같은 응답 pass에서 가볍게 audit하고 선택의 형성·변경 신호가 있을 때만 context-decision을 부릅니다. 같은 scope·anchor와 `{id,sha256}`의 실제 본문이 session context에 남아 있을 때만 재사용합니다. 본문이 없거나 anchor가 바뀌면 알려진 scope/key로 exact `check`를 한 번 실행해 Current DEC의 실제 `Decision`, `Rationale`, `Rejected alternatives`와 비어 있지 않은 `Revisit conditions`를 `sections` 아래 받고, 같은 turn에는 다른 context read 없이 재사용합니다. 기존 한국어 heading은 legacy read/round-trip alias입니다. Healthy index zero-match는 indexed body open 0이고 stale/missing recovery body open은 호출당 20개 이하입니다. Hard bound는 body materialization/open, selected output, candidate/envelope와 owner input에 한정되며 index scoring·directory enumeration 및 end-to-end model token 사용량의 O(1)을 보장하지 않습니다.

- `same`: 기존 결정을 재사용하고 중복 기록하지 않음
- `supporting`: 기존 결정을 유지하고 재사용 가치가 있는 새 근거만 OBS 후보로 제안
- `rationale_changed`: 결론 전에 반환된 비어 있지 않은 실제 section을 모두 원문으로 인용하고 행동을 보류한 뒤, keep이면 수행하지 않고 supersede면 그 명시적 선택 뒤에만 진행하는 두 선택지를 묻는 명시적 양자 질문을 함
- `conflict`: 결론 전에 반환된 비어 있지 않은 실제 Decision·Rationale·Rejected alternatives·Revisit conditions를 모두 원문으로 인용하고 선택한 token을 `satisfied|no evidence|ambiguous` 중 하나로 user response에 그대로 쓴 뒤 같은 명시적 양자 질문을 함. keep이면 수행하지 않고 supersede면 그 명시적 선택 뒤에만 진행함. `satisfied`는 사용자가 저장된 조건을 직접 성립시키는 현재 사실을 제공한 경우에만 쓰며 요청된 충돌 행동 자체는 근거가 아님. 사실이 없거나 저장 조건이 아닌 다른 쟁점에 관한 사실이면 `no evidence`이고, 관련 조건 사실이 불완전하거나 충돌할 때만 `ambiguous`임
- `new`: 조회된 범위 안에서 관련 기존 결정을 찾지 못함

이 비교는 실제 본문을 대상으로 하며 문자열 hash, ID나 metadata를 의미 동일성의 근거로 사용하지 않습니다. 충족된 재평가 조건은 재평가 권한이지 구현 권한이 아니며 durable capture 승인은 별도입니다. 그 외의 성숙한 결정은 원래 답 뒤 grouped proposal에 한 번 포함합니다. dismissed·deferred 후보는 새 evidence 전까지 반복하지 않으며 승인된 final bundle만 `context-core` coordinator가 적용합니다. 이후 brief는 세 핵심 section을 함께 복원하고, 새 결정이 같은 slot을 supersede하면 이전 DEC를 history로 이동해 더는 따르지 않도록 표시합니다.

## Read-only spec view

`decision_cli.py spec-view --scope <scope>`는 지정 scope와 exact·strict ancestor·strict descendant 관계인 Current DEC를 area index metadata에서 먼저 고른 뒤, 선택된 실제 본문의 canonical `Decision`과 `Rationale`만 읽기용 명세로 조립합니다. 기존 `결정`과 `취지` heading은 legacy alias로 읽어 canonical 영어 key로 반환하며 저장된 heading을 자동 변경하지 않습니다. 문자열 prefix는 scope 관계로 보지 않으며 History와 `do_not_follow`는 포함하지 않습니다.

결과는 `(created_at, id)` 오름차순이고 JSON envelope와 마지막 newline을 포함한 실제 CLI stdout UTF-8 기준 최대 32 KiB입니다. 상한을 넘으면 같은 순서의 뒤쪽 DEC를 section 중간 절단 없이 항목 전체로 제외하고 `omitted_count`를 반환합니다. 이 projection은 호출할 때마다 다시 계산하며 approval, 저장 또는 filesystem write를 수행하지 않습니다.

`init`이 설치하는 managed policy가 증분 audit, 선택적 recall, 변화 알림과 grouped capture를 매 대화에서 유도합니다. 이는 agent의 같은 응답 pass에서 동작하는 운영지침이지 background daemon이나 per-turn hook은 아닙니다. 사용자 확인 없는 durable write는 계속 금지됩니다.

기존 `wiki/` 자동 migration은 제공하지 않습니다. PCMS는 조직 권한·승인 workflow·cross-project search·policy·audit·conflict queue의 control-plane 경계이며, 이 local plugin은 결정 기록과 recall 자체에 집중합니다.

0.2.0은 legacy fingerprint field와 batch-local claim key를 제거한 breaking release입니다. Owner-result 연결용 transport reference는 의미를 갖지 않습니다. 혼합 설치는 `context-common/v2` handshake에서 fail-closed합니다. 구형 artifact의 제거된 field는 읽을 수 있고 다음 승인 rewrite에서 lazy-clean합니다. 신규 candidate/draft에는 `schema_removed_field`로 계속 거부하며 fingerprint를 의미상 동일성 근거로 사용하지 않습니다.

0.2.1은 `context-common/v2` 호환 patch release입니다. core doctor의 `partial|invalid` 진단은 전역 preflight 실패가 아니라 warning으로 전달하고, 실제 decision target과 겹치는 blocking issue만 해당 operation을 중단합니다. init target 자체의 schema·owner·path가 안전하지 않을 때만 core bootstrap이 write 0으로 실패합니다.

0.3.0은 core audit가 선택 형성·변경 신호를 찾았을 때만 decision 비교를 수행합니다. `check`는 metadata로 후보를 먼저 좁히고 무관한 score-0 본문을 열지 않으며, 실제 관련 DEC 본문·scope·rationale 비교와 승인형 capture 경계는 그대로 유지합니다.

0.4.0은 exact dependency를 `context-core@context-plugins`, source `Jeis-Jw/context-plugins`로 옮긴 distribution breaking release입니다. `context-common/v2` artifact 호환성은 유지하지만 기존 marketplace 설치를 자동 전환하지 않습니다.

0.4.1은 `context-core`의 판정·비용 계약 개선과 distribution version을 맞춘 patch release이며 decision semantics와 `context-common/v2` 계약은 변경하지 않습니다.

0.5.0은 Current DEC의 canonical `Decision`·`Rationale`만 조립하는 read-only `spec-view`와 네 plugin distribution parity를 추가합니다. legacy 한국어 heading도 읽지만 자동 migration은 하지 않습니다. DEC storage schema와 `context-common/v2`는 유지되고 ASM·TERM 설치 또는 기존 artifact migration은 자동으로 일어나지 않습니다.

0.5.1은 frozen receipt golden path, repository/core identity 결박, release-pinned core handshake, bounded recall recovery와 actual semantic input limit을 추가한 developer-preview patch입니다.

0.7.0은 자연어 승인 질문, discovery-only read, supersede/withdraw golden path와 deterministic receipt lifecycle을 통합합니다. Core와 decision의 semantic ownership 및 package 경계는 유지하며 root profile installer만 설치 동작을 묶습니다. `v0.7.0` tag와 publication은 아직 완료되지 않았습니다.

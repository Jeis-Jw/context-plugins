# context-decision v1 owner protocol (한국어)

`decision_cli.py`는 `context-decision/v1`의 semantic owner다. complete DEC draft, lifecycle effect, `context-owner-plan/v1`, `context-owner-validation-receipt/v1`과 bounded recall만 만든다. filesystem write, directory 생성, index 갱신, lock, final approval digest 생성과 apply는 하지 않는다. physical writer는 `context-core` coordinator 하나다.

## Dependency boundary

- marketplace: `context-plugins`
- plugin: `context-core`
- selector: `context-core@context-plugins`
- source: `Jeis-Jw/context-plugins`
- protocol: `context-common/v2`

`schema`와 `capabilities`만 core 없이 호출할 수 있다. 저수준 semantic operation은 compatibility mode로 `--host`, `--core-inventory @file`, `--core-doctor @file`을 받는다. 일반 workflow와 init은 release contract의 entrypoint path·SHA-256 pin을 먼저 확인한 뒤 그 core의 schema와 doctor를 직접 handshake한다. `doctor.repository_state=absent`는 bootstrap-required state이고 partial/invalid diagnostics는 전역 차단하지 않는다. decision owner는 install, enable, update, marketplace add, cache probing 또는 embedded core를 수행하지 않는다.

## Semantic claim gate

DEC는 현재 또는 미래 행동을 지배하는 명시적 선택이며 다음 assertion 전부가 exact candidate에 결박돼야 한다.

- `explicit_choice` → `/owner_inputs/decision/decision`
- `scope_identified` → `/scope_hint`
- `commitment_present` → `/evidence/*`

idea, question, fact, preference와 미합의 제안은 `decline` 또는 `needs_clarification`이다. `requested_kind:"decision"`은 owner 선택만 고정하며 이 gate를 우회하지 않는다. CLI는 agent skill의 의미 판단을 대신하지 않고 assertion set, input digest와 RFC 6901 pointer만 fail-closed 검증한다.

Direct surface는 2단계다. `candidate prepare`는 caller가 명시한 semantic field, `cand_`+32 lowercase hex transport ID, commitment evidence와 bounded search terms를 정규화한다. owner는 caller 입력 없이 후보 의미를 지어내지 않는다. transport ID는 기계적으로 만들 수 있지만 의미상 가중치가 없다. owner skill이 그 object를 판독한 뒤 `capture --candidate @file --attestation @file`로 claim하거나 `--decline-reason`/`--needs-clarification-reason`으로 권위 draft 없이 종료한다. 상수 commitment evidence와 CLI 자체 attestation은 금지다.

## DEC schema와 slot

필수 section은 `결정`, `취지`, `반려대안`이다. 세 section의 누락, 빈 값과 literal `...|TODO|TBD|해당 없음`은 실패한다. 실제 검토한 대안이 없으면 `검토하지 않음: <이유>`를 쓴다. 선택 section은 `근거와 제약`, `트레이드오프`, `재평가 조건`이다. `verified_at`과 공통 `status`는 금지한다.

`scope`는 trim → NFKC+casefold → leading/trailing slash 제거 → segment별 non-alnum run을 `-`로 변환한다. empty segment, `.`/`..`, segment 40자 초과, 8 segment 초과와 전체 160자 초과는 실패한다. `decision_key`는 같은 변환을 사용하고 `/`, empty와 80자 초과를 거부한다. ancestor는 canonical segment 배열의 strict prefix이며 문자열 prefix나 equality가 아니다.

Current에는 `(scope, decision_key)`당 DEC가 최대 하나다. 같은 key의 ancestor/descendant scope는 overlap conflict이며 모든 conflict ID에 대한 acknowledgement와 `{id,path,sha256}` exact read precondition이 있어야 한다. 의미상 동일한 결정은 fingerprint로 판정하지 않는다. 사전 `check`가 제공한 실제 본문을 agent가 비교하고 `same`이면 기존 DEC를 재사용한다.

## Owner result와 lifecycle

capture는 one current draft/effect/create operation을 반환한다. ID와 `created_at`은 draft 시 한 번 만들고 embedded candidate, claim attestation, complete content와 semantic projection에 결박한다.

- `supersede`: successor candidate가 predecessor의 canonical scope/key를 명시적으로 그대로 가져야 한다. 한 owner result에 old changed-move History draft와 new Current create draft를 포함하고 `old.superseded_by == new.id`, `new.supersedes == [old.id]`를 지킨다. History path는 `<stem>--<old-id12>.md`다.
- `withdraw`: old를 `retired_reason:"withdrawn"`과 `retirement_note`가 있는 History draft로 만들며 successor가 없다.
- `annotate`: title, summary, tags, search terms, source refs만 제자리 correction하고 결정 section, slot과 ID는 보존한다.
- `revisit`: due warning과 review proposal만 반환하며 state를 바꾸지 않는다.

일반 evidence OBS는 active인 채 DEC `relations.informed_by`로 연결한다. decision-like fallback OBS import는 `kind_hint:decision`, source artifact의 exact id·path·SHA-256·actual claim, `same_claim` attestation과 cross-owner single coordinator plan을 요구하며 일반 evidence relation과 혼용하지 않는다.

## Same-batch validation

`batch validate`는 physical `decision.index.md`의 exact SHA-256를 base로 사용한다. 전달된 prior same-area final bundle을 proposal order대로 overlay한다. 각 bundle의 `plan.prior_bundle_digests`는 앞선 exact digest 목록과 같아야 한다. virtual Current에 slot, overlap acknowledgement/read precondition과 lifecycle predecessor current 여부를 적용한다.

성공 receipt는 다음을 결박한다.

- `owner_result_digest`
- `base_area_index_sha256`
- ordered `prior_same_area_bundle_digests`
- canonical `scope`, `decision_key`, actual `primary_claim`, `rationale`, acknowledged conflicts
- 자기 field를 제외한 `receipt_digest`

Receipt 없는 final owner plan이나 altered receipt는 `plan validate`에서 실패한다.

## Frozen workflow receipt

일반 단일 capture의 public golden path는 `decision_workflow.py preview --inline`과 `apply`다. caller는 decision semantic field와 `explicit_choice`, `scope_identified`, `commitment_present`를 각각 명시적으로 attest한다. workflow는 그 입력을 exact candidate·attestation으로 직렬화할 뿐 semantic evidence나 판정을 만들지 않는다. `preview`는 loaded core CLI의 release pin, schema와 current doctor를 직접 확인하고 owner-result 생성, same-batch validation과 core transaction preview를 한 process에서 순서대로 수행한다. complete approval preview와 exact digest만 stdout에 반환하고 bundle/materials는 명시된 repository 밖의 새 `context-decision-workflow-receipt/v1` 파일에 저장한다. 이미 고정한 semantic input을 재사용하는 고급 경로에는 `--candidate @file --attestation @file` mode를 유지한다.

receipt의 workflow approval material은 exact `context-repository-identity/v1`, core CLI absolute path와 SHA-256, candidate/owner-result digest, nested core approval digest와 exact bundle을 모두 결박한다. stdout의 user-facing `approval_digest`는 이 전체 material의 canonical digest다. `receipt_digest`는 손상 탐지용일 뿐 approval을 대체하지 않으므로 receipt와 nested digest를 함께 재계산해도 원래 사용자 승인을 재사용할 수 없다. 기존 receipt overwrite, repository 안 receipt, clone·linked worktree·same-path recreated repository apply, 변경된 core CLI와 잘못된 digest는 write 전에 실패한다. `apply`는 nested bundle을 다시 만들지 않고 context-core `transaction apply`에 전달하며 receipt 자체도 변경하지 않는다.

preview의 repository와 host configuration write는 0이다. 명시적 transient receipt만 repository와 Git metadata 밖에 mode `0600`으로 만들며 durable context가 아니다. 민감한 decision content가 포함되므로 caller는 workflow 종료 뒤 명시적으로 폐기한다. 승인된 apply의 context/index write는 계속 context-core만 수행한다. lifecycle, prior-bundle 조합과 진단에는 기존 저수준 surface를 사용할 수 있다.

inline `--sec-*`는 plain literal을 기본으로 하고 explicit `@file`과 leading `@` literal용 `@@text`를 core body argument와 같은 의미로 해석한다. path-like plain text는 file로 추측하지 않으며 missing·symlink·8 KiB 초과 file은 receipt/repository write 전에 거부한다. common primary-claim protocol 상한은 2,000 codepoint이고 built-in SNAP `current_context`, OBS `observation`, DEC `decision`은 각각 owner-specific 1,200 codepoint다. canonical owner input 8 KiB와 candidate envelope 16 KiB를 적용하고 오류는 실제 크기·상한·초과량을 반환한다.

## Recall과 init

`search`는 `decision.index.md` metadata만 읽는다. `read`와 `brief`는 선택된 DEC만 연다. brief는 `결정`, `취지`, `반려대안`만 포함하고 최대 8 KiB다. 낮은 순위 item을 통째로 제외하며 section 중간 절단은 하지 않는다. History에는 항상 `do_not_follow:true`와 lifecycle reason을 붙인다.

`spec-view --scope <scope>`는 Stage 1의 Current metadata에서 canonical scope가 exact이거나 strict ancestor·descendant인 DEC만 선별한다. 문자열 prefix는 scope 관계가 아니다. 선택된 실제 본문의 `결정`·`취지`만 `(created_at,id)` 오름차순으로 반환하고 History와 `do_not_follow`는 제외한다. JSON envelope와 마지막 newline을 포함한 실제 CLI stdout UTF-8는 최대 32 KiB이며 상한을 넘으면 같은 deterministic 순서의 뒤쪽 DEC를 항목 전체로 생략하고 exact `omitted_count`를 반환한다. section 중간 절단, approval, 저장과 write는 없고 매 호출 index와 실제 본문에서 재생성한다.

`check --statement ... --scope ... --decision-key ...`는 새 선택을 확정하거나 기록하기 전에 사용한다. exact slot과 scope overlap은 반드시 포함한다. 그 밖의 후보는 statement·rationale·query와 title·summary·search terms의 distinctive metadata match만 선택하며, score 0의 임의 body는 열지 않는다. 관련 Current DEC의 세 핵심 section과 `{id,path,sha256}`를 `context-decision-comparison-input/v1`으로 반환하고 retrieval에는 index SHA, metadata match 수, body read 수와 selected semantic bytes를 포함한다. comparison input은 24 KiB, 전체 result는 32 KiB이며 omitted ID는 최대 8개 sample과 exact count만 반환한다. agent는 `new|same|supporting|rationale_changed|conflict` 중 하나와 근거·관련 ID를 제시한다. `new`는 반환된 집합 안의 판정이며 전역 무충돌 증명이 아니다. 이 operation은 read-only이고 지문·문장 유사도로 의미를 확정하지 않는다.

`init`은 `context-owner-descriptor/v2` feature를 지원하는 release-pinned core에서 schema와 doctor state를 직접 handshake한 뒤, DEC area의 exact legacy-compatible `context-owner-descriptor/v1`, complete empty decision index seed, descriptor/seed digest와 installed core `bootstrap` 요청을 만든다. ready/partial/invalid과 bootstrap-required `absent`를 전달하되 실제 복구 가능 여부는 core가 판정한다. Init skill은 `decision_init.py` entrypoint 한 번으로 handshake와 active installed core의 public `context_cli.py bootstrap --host <host>` 호출을 순서대로 수행한다. core surface가 필요한 root 복구, decision area registration과 host별 managed operating policy installation을 coordinator로 적용하며 phase result를 반환한다. decision CLI 자체는 root/area/index/policy를 만들거나 수정하지 않는다.

`claim_fingerprint`, `source_claim_fingerprint`와 capture candidate의 `claim_key`는 schema에서 제거됐다. candidate ID는 transport reference로만 사용한다. legacy artifact field는 읽고 다음 승인 rewrite에서 제거하며, 신규 candidate/draft의 제거된 field는 `schema_removed_field`로 실패한다.

## Output and errors

JSON success는 `{"ok":true,"result":...}`, error는 `{"ok":false,"error":{"code":...,"message":...,"details":...}}`다. exit code는 usage/schema 2, not found 3, conflict 5, integrity/index 6이다. 모든 operation은 실행 전후 repository filesystem bytes가 같아야 한다.

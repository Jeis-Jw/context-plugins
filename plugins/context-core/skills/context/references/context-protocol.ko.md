# context-common/v2 storage kernel (한국어)

이 문서는 `context-core`가 제공하는 host-independent storage·recall·write 경계의 공개 정본이다. 제품 수준의 구성과 distribution identity는 repository root README와 각 plugin README가 소유하고, executable schema와 tests가 runtime 계약을 검증한다.

## 정본과 ID

- Git worktree root의 `context/`만 storage root다. `--root` override는 없다.
- Markdown artifact가 정본이고 `context.index.md`와 `<area>.index.md`는 deterministic projection이다.
- artifact ID는 `ctx_` + lowercase UUIDv4 hex 32자다. filename, title, path와 lifecycle이 ID를 바꾸지 않는다.
- frontmatter는 `KEY: JSON_VALUE` 한 줄 형식의 JSON-compatible YAML subset이고, document body는 schema별 fixed H2 section 순서를 사용한다.
- `claim_fingerprint`, `source_claim_fingerprint`와 capture candidate의 `claim_key`는 protocol에서 제거됐다. 신규 artifact와 semantic projection은 fingerprint를 출력하거나 요구하지 않고, candidate ID는 transport reference로만 사용한다. legacy artifact field는 `schema_removed_field` warning으로 읽고 다음 승인 rewrite에서 lazy-clean하며, 신규 candidate/draft에서는 fail-closed한다.

## Read 경계

- healthy Stage 1 metadata hit은 root index와 선택된 area index만 열고 artifact open/list/stat을 하지 않는다. `-`와 `.`이 들어간 identifier-like query는 하나의 distinctive token으로 유지해 공통 fragment만 맞는 broad candidate를 만들지 않는다.
- valid index의 non-empty query zero-match는 선택 area의 filename만 열거해 index에 없는 artifact만 읽는다. 모두 indexed면 body open은 0이고 fallback으로 표시하지 않는다. 누락 body와 broken area index·선택된 missing link의 recovery body read는 recall 한 번당 합계 20개로 제한하며 초과 시 `index_miss_fallback_truncated` 또는 `index_fallback_truncated` warning을 반환한다.
- `--strict-index`는 fallback 없이 exit 6 `index_stale`로 실패한다.
- root index가 없으면 storage error `context_root_missing`이며 plugin dependency error와 다르다.

## 비용 비례 금지 invariant

recall·capture의 artifact body materialization, bounded output과 model·owner invocation 비용은 corpus 크기, 등록 addon 수 또는 누적 turn 수에 비례해 증가하지 않아야 한다.

- runtime 경계는 healthy Stage 1의 index-only read와 artifact open/list/stat 0, recovery body open 최대 20개, Stage 1 4 KiB·body pack 8 KiB, common primary-claim protocol 2,000 codepoint, built-in SNAP `current_context`·OBS `observation` 각각 1,200 codepoint, 최대 8개이면서 schema·audit_count·candidates 전체 canonical UTF-8 envelope가 16 KiB 이하인 `context-capture-batch/v1`, owner input 8 KiB, approval preview 32 KiB 상한으로 집행한다. Dict batch는 세 key만 허용하고 audit_count는 bool이 아닌 integer `1`이어야 한다. legacy bare list는 같은 synthetic v1 envelope byte budget으로 유지한다. zero-match의 unindexed 확인은 directory entry 수에 따라 증가할 수 있지만 indexed artifact body는 열지 않는다. `context-decision`은 별도로 decision 1,200 codepoint, brief 8 KiB·comparison input 24 KiB·result 32 KiB 상한을 둔다.
- `tests/context-v1/test_token_io_evidence.py`는 synthetic large corpus의 artifact I/O, candidate·addon 경계와 output byte budget을 계측한다.
- root·area index bytes를 읽고 metadata row를 score하는 I/O·CPU는 선택한 area index 크기에 따라 증가할 수 있다. 현재 구현은 전체 artifact body materialization을 피하는 것이며 전체 recall 계산량의 O(1)을 보장하지 않는다.
- 대화 delta당 단일 audit, signal이 없을 때의 침묵, addon의 대화 재판독 금지는 관리형 policy의 의무다. CLI는 `audit_count:1`과 bounded envelope을 검증하지만 host/model이 policy를 실제로 한 번만 수행하는지는 hard runtime guarantee가 아니다.

## 대화 관찰 경계

- 관리형 policy는 각 user turn의 새 의미를 같은 model response pass에서 한 번 audit한다. 이는 background daemon, 별도 model call 또는 per-turn CLI hook이 아니다. 신호가 없으면 tool call과 user-visible status가 모두 0이다.
- host/model session에는 scope·anchor, 읽은 `{id,sha256}`, pending·dismissed 참조만 bounded ephemeral ledger로 둔다. 실제 artifact body와 candidate 전체를 복제하지 않으며 repository나 index에 쓰지 않는다.
- 신호가 있을 때 Stage 1 metadata를 먼저 읽고 선택된 body만 materialize한다. body가 session context에 남아 있고 scope·evidence·anchor·index와 artifact SHA가 그대로일 때만 재사용한다.
- conflict·rationale change 알림은 primary 결론 전, 일반 capture proposal은 성숙한 milestone 뒤다. dismissed·deferred 후보는 새 evidence가 생기기 전에는 다시 제안하지 않는다.

## Write 경계

- semantic owner는 complete `context-owner-result/v1`의 draft/effect/proposed plan만 만든다.
- `transaction preview`는 exact on-disk precondition, complete material, derived index rebuild와 owner/area authorization을 `context-mutation-bundle/v1`로 봉인한다.
- `approval_digest`는 canonical `approval_material` 전체의 SHA-256이다. approval material은 preview·plan과 함께 resolved worktree 및 Git common-dir의 absolute path·device·inode decimal string을 exact `context-repository-identity/v1`로 결박한다. apply는 digest 확인 직후 현재 identity와 exact equality를 검증하고 동일 bundle object와 exact digest만 받는다. 다른 clone, linked worktree와 같은 path에 다시 만든 repository는 실패하며 HEAD와 unrelated content는 identity에 포함하지 않는다.
- context-core coordinator만 repository-realpath root lock 아래 atomic file operation과 deterministic index rebuild를 수행한다.
- hidden operation, seed 누락, material/digest 불일치, changed precondition, path escape와 symlink segment는 write 전에 fail-closed한다.

### Core workflow receipt

- `context-core-workflow-receipt/v1`은 정확히 `schema`, immutable `status:pending`, offset-aware `created_at`, `plan_id`, `core`, `plan_bundle`, `receipt_digest` 7-field다. `plan_id`는 filename/projection metadata일 뿐 semantic identity가 아니며 `plan_bundle.approval_material.plan.plan_id`와 같아야 한다. `core`는 exact `{path,sha256}`, `plan_bundle`은 기존 mutation bundle 그대로다. candidate ID나 중복 core bundle field는 금지한다.
- `receipt_digest`는 나머지 6-field의 canonical SHA-256으로 손상만 탐지한다. 승인은 preview가 반환하고 receipt 밖 agent state에 보존한 exact `{core,plan_bundle}` workflow digest로 별도 결박한다. `transaction apply --receipt-file ... --approved-digest ...`는 이 독립 값을 필수로 검증한 뒤 current core path/SHA를 확인하고, 검증된 nested `plan_bundle.approval_digest`만 core apply에 넘긴다. receipt self-digest는 승인 근거가 아니다.
- flag 기반 OBS/SNAP preview는 `tempdir/context-core/<plan_id>.json`에 frozen receipt 하나를 만든다. directory는 `0700`, regular file은 `0600`이고, prospective path가 repository와 Git metadata 밖인지 directory 생성 전에 검증한다. explicit path는 default directory를 만들지 않는다. target·direct parent·traversal·symlink·mode·inode identity는 fail-closed한다.
- selection은 preview에서 agent가 유지한 exact path뿐이며 directory scan이나 newest 선택은 없다. tri-state는 `--attestation @file`과 receipt option 없음이면 기존 bundle, complete built-in flag pair면 private default receipt, `--receipt-file`이면 그 explicit path다. 기존 `--plan-bundle @file` apply도 유지한다.
- OBS flag는 `reusable_observation → /owner_inputs/observation/observation`, `evidence_present → /owner_inputs/observation/evidence/0`에, SNAP은 `handoff_requested → /owner_inputs/snapshot/current_context`, `unfinished_context_present → /owner_inputs/snapshot/open_items/0`에 고정된다. partial·absent·file/flag 혼용 attestation은 receipt와 repository write 전에 실패한다.
- receipt apply 성공 시 receipt를 삭제한다. cleanup만 실패하면 `applied:true`와 `receipt_cleanup_failed`를 반환하고, fully applied receipt 재시도는 write 없이 거부한다. core에는 locator·keep·reject·TTL lifecycle을 추가하지 않는다.

## Generic addon structural profile

`context-owner-descriptor/v1`의 등록·artifact·CLI bytes는 그대로 유지하며 한 root에서 v1과 v2 area가 공존할 수 있다. v2를 지원하는 runtime은 root-independent `schema.features`에 `context-owner-descriptor/v2`를 광고한다. 이 feature가 없는 0.4.1 runtime은 addon이 bootstrap 전에 incompatible core로 판정해 repository bytes를 바꾸지 않는다. 자동 downgrade·upgrade·migration·delete surface는 없다.

- `context-owner-descriptor/v2`는 canonical UTF-8 JSON 8 KiB 이하이고 identity와 `context-structural-profile/v1`만 가진다. unknown/duplicate key, noncanonical input, unsupported scalar, depth·node·field·item bound 초과는 fail-closed다. regex, expression, callback, executable default는 선언할 수 없다.
- profile은 최대 24개 field와 최대 12개 H2 section을 선언한다. field type은 `string|string_list|date|timestamp|enum|context_id|context_id_list|relation_map`으로 닫혀 있고, section ordered/required/primary와 최대 4개 scalar index projection을 고정한다. `provisional`은 허용 authority다.
- lifecycle은 `create_current|replace_same_state|retire_current|supersede_current|delete_one` topology만 사용한다. reason recipe는 required/forbidden field, successor cardinality와 predecessor/successor reference recipe만 선언하며, `supersede_current`는 양 endpoint 방향의 recipe를 모두 요구한다. core는 addon의 field·claim 의미를 해석하지 않는다.
- semantic owner receipt v2는 exact descriptor digest, capability, owner result, base area index, same-area prior bundle, topology와 semantic input digest를 결박한다. final plan은 전체 prior chain과 그중 same-area ordered subset을 별도로 고정하며 apply도 이 subset을 receipt에 전달한다. receipt는 보조 증거이며 core는 preview와 apply에서 target artifact envelope/schema/kind/authority, field type/bounds, H2 order, projection, lifecycle, relations, operation topology, path/index/CAS를 독립 검증한다. apply는 root lock을 얻은 뒤 같은 검증을 다시 수행한다.

root area row는 기존 6-field 형식을 유지한다. 별도 generated root registry에는 v2 area의 `{area,descriptor_schema,descriptor_digest}`만 저장하고, 해당 area index의 generated profile block에는 canonical full descriptor를 저장한다. v1 area에는 두 entry가 모두 없다. root digest, area descriptor, capability, receipt와 final plan은 동일 descriptor digest에 결박되며 등록된 v2 descriptor는 immutable하다.

v2 registration이 재시도 가능한 상태는 none, exact seed-only, exact root-row+profile-registry-only, complete뿐이다. malformed/unknown profile과 그 밖의 partial state는 target write에서 fail-closed한다. 등록된 root profile registry와 area descriptor의 trust mismatch는 `doctor`·`refresh`의 blocking issue이며 `refresh --fix index`가 자동 수정하지 않는다. 이 trust boundary와 무관한 artifact/index read drift는 기존 warning·bounded fallback 원칙을 유지한다.

## CLI envelope

- success: `{"ok":true,"result":{...}}`
- error: `{"ok":false,"error":{"code":"...","message":"...","details":{...}}}`
- exit 2 usage/schema/filename, 3 root/artifact/input missing, 5 owner/path/lifecycle conflict, 6 integrity/index failure

`doctor`는 기존 4개 repository state(`absent|partial|invalid|ready`)와 readiness 의미를 바꾸지 않고 `plugin_version`, resolved `entrypoint`, `protocol`을 더한 exact 10-field self-report를 반환한다.
- `schema`와 `capabilities`는 repository root 없이 동작한다. `schema.features`는 addon이 bootstrap 전에 확인하는 compatibility handshake다.

`init --host codex|claude-code`은 명시적 호출 하나로 absent root의 canonical root/SNAP/OBS index seed와 활성 host의 관리형 policy block을 적용한다. host mapping은 `codex → AGENTS.md`, `claude-code → CLAUDE.md`다. policy target과 marker를 storage write 전에 preflight하고 managed marker 밖 bytes를 보존한다. valid descriptor와 최신 block이면 unrelated corpus 진단과 무관하게 `core_init`과 `policy_install`이 noop이다. populated repository에서 root index만 없으면 exact built-in SNAP/OBS metadata만 rebuild하고 미등록 area는 자동 claim하지 않으며, init target의 incompatible schema/owner/path만 `partial_core_init`으로 중단한다. 결과는 structured phase와 post-apply doctor receipt를 포함한다.

`bootstrap --descriptor @file --index-seed @file --host codex|claude-code`은 addon init용 public surface다. 같은 호출에서 core init을 먼저 완료한 뒤 empty area seed를 `area_register`로 적용하고 동일한 host policy를 설치한다. 중간 실패는 완료/실패 phase를 반환하며, v1의 exact root-row prefix 또는 v2의 exact root-row+profile-registry prefix는 재시도에서 남은 area index를 적용해 수렴한다. descriptor schema/owner/kind/artifact_schema/authority/profile digest 또는 existing area index metadata가 다르면 noop이 아니라 write 0 fail-closed다. 이 explicit-init authority는 fixed `core_init|area_register|policy_install` transition에만 허용되고 일반 artifact/index mutation에는 사용할 수 없다.

Lifecycle semantic input은 predecessor와 successor의 실제 primary claim, bounded supporting context, artifact SHA-256, path/id와 source candidate digest를 포함한다. `same_claim` attestation은 두 primary claim을 직접 가리켜야 하며 hash-derived claim identity를 대신 사용하지 않는다.

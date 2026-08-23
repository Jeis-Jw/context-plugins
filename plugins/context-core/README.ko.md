# context-core (한국어)

`context-core`는 다음 agent나 session이 작업을 이어갈 수 있도록 승인된 handoff와 재사용 가능한 근거를 Markdown으로 보존하는 가벼운 runtime입니다. SNAP은 재개용 staging, OBS는 비권위 evidence이며, `context.index.md`와 area index로 필요한 문서만 읽습니다.

## 시작하기

1. provider marketplace `context-plugins`(source `Jeis-Jw/context-plugins`)에서 `context-core@context-plugins`를 원하는 scope에 직접 설치·활성화합니다.
2. host를 reload하거나 새 session을 엽니다.
3. `$context-core:init`을 한 번 호출하면 canonical storage seed와 활성 host의 관리형 운영지침을 core coordinator가 적용합니다.
4. 반환된 `doctor.repository_state: ready`, `policy.target`과 phase result를 확인합니다. ready 재호출은 noop입니다.

`schema`와 `capabilities`는 repository root 없이 확인할 수 있습니다. `schema.features`의 `context-owner-descriptor/v2`는 bounded structural profile을 이해하는 runtime handshake입니다. `doctor`는 read-only이며 `context-common/v2`, `repository_state`, `issues`, `warnings`를 보고합니다. 저장소가 아직 초기화되지 않은 read operation은 dependency 오류가 아닌 `context_root_missing`으로 실패합니다. `init`은 absent에서 fixed root/SNAP/OBS seed와 `codex → AGENTS.md`, `claude-code → CLAUDE.md` 관리형 block만 직접 적용합니다. populated repository에서 root index만 없으면 exact built-in SNAP/OBS metadata로 rebuild하고 미등록 area는 자동 claim하지 않으며, legacy artifact/index warning은 init을 막지 않습니다. init target의 incompatible schema/owner/path는 덮어쓰지 않습니다.

## 제품 흐름

- Standalone: 명시적 handoff는 SNAP, 재사용 가능한 발견·근거는 OBS로 제안합니다.
- Integrated: semantic owner가 complete draft와 plan을 만들고, `context-core`가 grouped preview를 봉인한 뒤 유일한 physical coordinator로 적용합니다.
- Generic addon: canonical `context-owner-descriptor/v2`가 closed field types, H2 order, index projection과 generic lifecycle topology를 선언합니다. `supersede_current`는 predecessor→successor와 successor→predecessor reference recipe를 모두 요구합니다. semantic receipt는 의미 claim을 증명하지만 core의 target-byte structural validation을 대체하지 않습니다.
- 각 user turn에서는 새 의미만 같은 응답 pass에서 별도 호출 없이 audit합니다. 신호가 없으면 아무 상태도 표시하지 않고, 신호가 있을 때만 metadata recall과 선택된 실제 본문 read를 수행합니다.
- common primary-claim protocol 상한은 2,000 codepoint입니다. Built-in SNAP `current_context`와 OBS `observation`은 각각 owner-specific 1,200 codepoint, DEC `decision`도 별도로 1,200 codepoint를 적용합니다. 각 owner input은 canonical UTF-8 8 KiB로 제한합니다. candidate batch의 16 KiB 상한은 `context-capture-batch/v1`의 `schema`, `audit_count`, `candidates`를 포함한 전체 canonical UTF-8 envelope에 적용하며 최대 8개 count 상한을 별도로 유지합니다. Dict envelope은 이 세 key만 허용하고 `audit_count`는 bool이 아닌 integer `1`이어야 합니다. 기존 bare list 입력은 synthetic v1 envelope로 계속 지원합니다.
- 이미 읽은 `{id,sha256}`와 pending·dismissed 참조는 session-local ephemeral ledger로 재사용하며, 본문을 복제하거나 repository에 저장하지 않습니다.
- Audit, route, claim, draft, preview와 denied apply는 repository와 host configuration을 변경하지 않습니다.
- 명시적 `init`과 addon init용 `bootstrap`만 fixed `core_init|area_register|policy_install`을 coordinator 검증으로 직접 적용합니다. 일반 artifact mutation의 exact digest approval은 유지되며 `refresh --fix index`만 derived index를 승인 없이 즉시 rebuild합니다.
- v1과 v2 area는 같은 root에 공존합니다. v1 bytes에는 profile registry를 추가하지 않고, v2 descriptor는 등록 뒤 immutable하며 digest가 달라진 재등록은 write 0으로 거절합니다.
- 등록된 v2 root registry와 area descriptor의 digest가 다르면 `doctor`와 `refresh`는 blocking issue로 보고하고 `refresh --fix index`도 해당 trust bytes를 자동 복구하지 않습니다. 일반 artifact/index drift의 read fallback은 body open을 호출당 20개로 제한하고 초과를 warning으로 보고합니다. healthy index의 metadata miss는 indexed body를 다시 열지 않습니다. 이 hard bound는 body materialization/open, selected output, candidate/envelope와 owner input에 한정되며 index scoring·directory enumeration 및 end-to-end host/model token 사용량의 O(1)을 뜻하지 않습니다.
- 관리형 운영지침은 conflict·취지 변경을 먼저 알리고, 그 외에는 원 답 뒤 성숙한 후보만 milestone당 한 번 제안합니다. dismissed·deferred 후보는 새 근거 전까지 반복하지 않으며 의미 판정에 hash·ID·metadata를 사용하지 않습니다.

기존 `wiki/`를 자동 migration하지 않습니다. Obsidian은 repository root를 vault로 열 때의 선택적 view일 뿐 runtime dependency가 아닙니다. PCMS는 조직 권한·승인 queue·cross-project search·정책·감사 같은 control-plane 범위를 담당하며, 이 local plugin은 그 기능을 제한해 판매하는 제품이 아닙니다.

0.2.0은 의미 판정에 쓰던 `claim_fingerprint`, `source_claim_fingerprint`와 batch-local `claim_key`를 제거한 breaking release입니다. `candidate_id`는 owner result 연결용 transport ID일 뿐 의미를 갖지 않습니다. 혼합 설치를 호환으로 오판하지 않도록 wire/storage handshake를 `context-common/v2`로 올렸습니다. 제거된 field가 남은 0.1.x artifact는 `schema_removed_field` warning으로 읽고 다음 승인 rewrite에서 lazy-clean합니다. 신규 artifact/candidate에는 계속 허용하지 않습니다.

0.2.1은 `context-common/v2` 호환 patch release입니다. corpus 전체 drift가 아니라 실제 target write의 CAS·index·path·lock·approval 경계만 fail-closed하고, read는 index-first 조회와 bounded fallback을 사용합니다. addon 등록은 root lock 안에서 exact-empty directory를 다시 확인해 preview 이후의 directory race도 차단합니다.

0.3.0은 각 대화의 새 의미만 같은 응답 pass에서 audit하고, durable signal이 있을 때만 metadata-first recall과 선택된 실제 본문 read를 수행합니다. session-local ledger는 읽은 `{id,sha256}`와 pending·dismissed 참조만 유지해 중복 읽기와 반복 제안을 줄이며, addon은 core의 단일 audit 결과를 재사용합니다.

0.4.0은 source repository와 marketplace를 `Jeis-Jw/context-plugins` / `context-plugins`로 분리한 distribution breaking release입니다. storage protocol은 `context-common/v2`를 유지하며 기존 설치를 자동 변경하지 않습니다.

0.4.1은 목적에 맞는 context 판정 기준과 recall 비용 경계를 명문화하고, managed policy의 정본과 runtime 설치 본문을 함께 정렬한 patch release입니다.

0.5.0은 read-only DEC spec view, generic `context-owner-descriptor/v2` structural validation, optional ASM·TERM owner 등록, full-envelope candidate batch 상한을 하나의 호환 release unit으로 묶습니다. `context-common/v2`와 기존 SNAP·OBS·DEC bytes는 유지하며 addon 설치나 artifact migration을 자동 수행하지 않습니다.

0.5.1은 repository identity에 결박된 approval, frozen DEC receipt, release-pinned core 실행 전 검증, healthy miss/recovery body-open 경계와 actual semantic input limit을 추가한 developer-preview patch입니다. `v0.5.1` tag는 아직 생성·push되지 않았습니다.

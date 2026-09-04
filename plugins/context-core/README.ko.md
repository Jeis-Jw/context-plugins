# context-core (한국어)

`context-core`는 다음 agent나 session이 작업을 이어갈 수 있도록 승인된 handoff와 재사용 가능한 근거를 Markdown으로 보존하는 가벼운 runtime입니다. SNAP은 재개용 staging, OBS는 비권위 evidence, ARCHIVE는 근거로 채택한 불변 장문 원본이며, `context.index.md`와 area index로 필요한 문서만 읽습니다.

## 시작하기

지원 profile은 내려받은 plugin 파일의 root installer를 한 번 실행해 빠진 plugin만 설치하고 활성화된 같은-major version은 호환으로 인정합니다. `context-core@context-plugins`와 `context-decision@context-plugins`은 계속 독립 package이며 bundle/meta-plugin이 아니고 decision code를 core에 내장하지 않습니다.

Core-only 구성이 필요하면 다음 경로를 그대로 사용할 수 있습니다.

1. provider marketplace `context-plugins`(source `Jeis-Jw/context-plugins`)에서 `context-core@context-plugins`를 원하는 scope에 직접 설치·활성화합니다.
2. host를 reload하거나 새 session을 엽니다.
3. `$context-core:init`을 한 번 호출하면 canonical storage seed와 활성 host의 관리형 운영지침을 core coordinator가 적용합니다.
4. 반환된 `doctor.repository_state: ready`, `policy.target`과 phase result를 확인합니다. ready 재호출은 noop입니다.

vault는 `context/`를 담는 일반 디렉터리이며 Git은 공유·버전관리의 선택사항입니다. 모든 CLI는 subcommand 앞의 `--vault DIR`로 저장 디렉터리를 선택할 수 있습니다. 생략하면 가장 가까운 `context/` 상위 디렉터리, 없으면 현재 디렉터리를 사용합니다. 입력 파일의 상대경로는 호출자 cwd 기준입니다.

`schema`와 `capabilities`는 vault 없이 확인할 수 있고 addon은 `filesystem-vault/v1` feature를 요구합니다. `schema.features`의 `context-owner-descriptor/v2`는 bounded structural profile을 이해하는 runtime handshake입니다. `doctor`는 read-only이며 `context-common/v2`, `repository_state`, `issues`, `warnings`를 보고합니다. 저장소가 아직 초기화되지 않은 read operation은 dependency 오류가 아닌 `context_root_missing`으로 실패합니다. `init`은 absent에서 fixed root/SNAP/OBS/ARCHIVE seed와 `codex → AGENTS.md`, `claude-code → CLAUDE.md` 관리형 block만 직접 적용합니다. pre-ARCHIVE vault에는 비어 있는 ARCHIVE area만 additive 등록하고 기존 artifact byte를 유지합니다. init target의 incompatible schema/owner/path는 덮어쓰지 않습니다.

한도는 기본 읽기 예산입니다. 지식은 slot 크기가 아니라 stable slot 수로 확장합니다. ARCHIVE만 불변 원본 보존을 위해 `Content` 65,000 codepoint와 512 KiB capture envelope을 허용하며, `--include-archive` 없이는 recall/pack에 나타나지 않습니다.

## 제품 흐름

- `repository_state`는 기존 호출자 호환성을 위해 유지한 vault 저장 상태 field이며 버전관리 상태가 아닙니다.
- Standalone: 명시적 handoff는 SNAP, 재사용 가능한 발견·근거는 OBS로 제안합니다.
- Integrated: semantic owner가 complete draft와 plan을 만들고, `context-core`가 내부 frozen plan을 봉인한 뒤 유일한 physical coordinator로 적용합니다.
- Generic addon: canonical `context-owner-descriptor/v2`가 closed field types, H2 order, index projection과 generic lifecycle topology를 선언합니다. `supersede_current`는 predecessor→successor와 successor→predecessor reference recipe를 모두 요구합니다. semantic receipt는 의미 claim을 증명하지만 core의 target-byte structural validation을 대체하지 않습니다.
- 각 user turn에서는 새 의미만 같은 응답 pass에서 별도 호출 없이 audit합니다. 신호가 없으면 아무 상태도 표시하지 않고, 신호가 있을 때만 metadata recall과 선택된 실제 본문 read를 수행합니다.
- common primary-claim protocol 상한은 2,000 codepoint입니다. Built-in SNAP `current_context`와 OBS `observation`은 각각 owner-specific 1,200 codepoint, DEC `decision`도 별도로 1,200 codepoint를 적용합니다. 각 owner input은 canonical UTF-8 8 KiB로 제한합니다. candidate batch의 16 KiB 상한은 `context-capture-batch/v1`의 `schema`, `audit_count`, `candidates`를 포함한 전체 canonical UTF-8 envelope에 적용하며 최대 8개 count 상한을 별도로 유지합니다. Dict envelope은 이 세 key만 허용하고 `audit_count`는 bool이 아닌 integer `1`이어야 합니다. 기존 bare list 입력은 synthetic v1 envelope로 계속 지원합니다.
- 이미 읽은 `{id,sha256}`와 pending·dismissed 참조는 session-local ephemeral ledger로 재사용하며, 본문을 복제하거나 repository에 저장하지 않습니다.
- Audit, route, claim, draft, preview와 denied apply는 repository와 host configuration을 변경하지 않습니다.
- 명시적 `init`과 addon init용 `bootstrap`만 fixed `core_init|area_register|policy_install`을 coordinator 검증으로 직접 적용합니다. 일반 artifact mutation은 사용자가 semantic payload·scope·lifecycle effect를 직접적·명시적·무조건적으로 확정하면 별도 저장 질문 없이 적용합니다. 저장 파일 본문은 보여주지 않으며 미확정 의미나 내부 렌더링의 semantic delta만 다시 확인합니다. `알겠어` 단독, 조건, 수정 요청, 화제 전환은 미확정 내용의 승인이 아닙니다. Agent가 내부 결박을 처리하고 승인 뒤 재생성하지 않습니다. `refresh --fix index`만 derived index를 승인 없이 즉시 rebuild합니다.
- v1과 v2 area는 같은 root에 공존합니다. v1 bytes에는 profile registry를 추가하지 않고, v2 descriptor는 등록 뒤 immutable하며 digest가 달라진 재등록은 write 0으로 거절합니다.
- 등록된 v2 root registry와 area descriptor의 digest가 다르면 `doctor`와 `refresh`는 blocking issue로 보고하고 `refresh --fix index`도 해당 trust bytes를 자동 복구하지 않습니다. 일반 artifact/index drift의 read fallback은 body open을 호출당 20개로 제한하고 초과를 warning으로 보고합니다. healthy index의 metadata miss는 indexed body를 다시 열지 않습니다. 이 hard bound는 body materialization/open, selected output, candidate/envelope와 owner input에 한정되며 index scoring·directory enumeration 및 end-to-end host/model token 사용량의 O(1)을 뜻하지 않습니다.
- 관리형 운영지침은 conflict·취지 변경을 먼저 알리고, 그 외에는 원 답 뒤 성숙한 후보만 milestone당 한 번 제안합니다. dismissed·deferred 후보는 새 근거 전까지 반복하지 않으며 의미 판정에 hash·ID·metadata를 사용하지 않습니다.

기존 `wiki/`를 자동 migration하지 않습니다. Obsidian은 해당 디렉터리를 vault로 열 때의 선택적 view일 뿐 runtime dependency가 아닙니다. PCMS는 조직 권한·승인 queue·cross-project search·정책·감사 같은 control-plane 범위를 담당하며, 이 local plugin은 그 기능을 제한해 판매하는 제품이 아닙니다.

`typed-relations/v1`은 additive이며 기존 relation-map 저장 shape를 유지합니다. `<predicate>:<target-kind>` 형식의 key만 preview, apply 재검증, refresh, doctor에서 live target kind와 대조합니다. `:` 없는 key는 legacy 동작을 유지합니다. inverse edge를 저장하거나 artifact migration을 수행하지 않습니다.

릴리스 이력은 프로젝트 [CHANGELOG](../../CHANGELOG.md)를 참고하세요.

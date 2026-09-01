---
name: init
description: 사용자가 현재 repository의 context-core 초기화나 bootstrap을 명시적으로 요청했을 때 canonical seed를 안전하고 멱등하게 적용한다. 일반 recall·capture 중에는 자동 실행하지 않는다.
---

# Init (한국어)

`--vault DIR`로 `context/`를 담는 기존 디렉터리를 선택하고 작업 전체에서 같은 vault를 사용한다. 생략하면 현재·상위 디렉터리 중 `context`가 있는 가장 가까운 곳, 없으면 현재 디렉터리를 사용한다. Git은 요구하지 않는다. Core·owner·workflow CLI는 subcommand 앞에, init adapter는 일반 옵션으로 `--vault`를 받는다. 입력 파일의 상대경로는 호출자 cwd 기준이다.

활성 host에 맞춰 `context_cli.py init --host codex --json` 또는 `context_cli.py init --host claude-code --json`을 한 번 호출한다. absent repository에는 canonical root/SNAP/OBS seed와 `codex → AGENTS.md`, `claude-code → CLAUDE.md` 관리형 policy를 설치한다. ready 재호출은 noop이다.

marker 밖 byte를 보존한다. broken/duplicate marker, symlink·nested target, incompatible schema/owner/path와 unsafe partial state는 write 0으로 실패한다. Addon bootstrap은 `context-owner-descriptor/v2`, 8 KiB 이하 canonical descriptor와 exact empty area seed를 요구한다. 등록된 descriptor identity는 immutable이며 자동 upgrade·downgrade·migration·delete·unknown trust repair를 하지 않는다. init 권한은 fixed `core_init|area_register|policy_install`뿐이다.

일반 durable capture는 별도다. 기록 제안 전에 preview를 실행하고 완성된 렌더링 본문과 함께 한 번만 묻는다. preview stdout의 `approval_digest`는 agent가 그대로 apply에 전달하되 digest·receipt 경로·내부 ID·core 경로를 사용자에게 보이거나 요구하지 않는다. capture 질문에 대한 직접적·명시적·무조건적 긍정만 승인이다. `알겠어` 단독, 조건, 수정 요청, 화제 전환은 승인이 아니며 승인 뒤 content·plan을 재생성하지 않는다.

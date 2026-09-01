---
name: init
description: 사용자가 현재 repository의 context-decision 초기화나 bootstrap을 명시적으로 요청했을 때 exact compatible context-core를 확인하고 필요한 core bootstrap과 decision area 등록을 한 번에 완료한다. 일반 decision capture 중에는 자동 실행하지 않는다.
---

# Init (한국어)

`--vault DIR`로 `context/`를 담는 기존 디렉터리를 선택하고 작업 전체에서 같은 vault를 사용한다. 생략하면 현재·상위 디렉터리 중 `context`가 있는 가장 가까운 곳, 없으면 현재 디렉터리를 사용한다. Git은 요구하지 않는다. Core·owner·workflow CLI는 subcommand 앞에, init adapter는 일반 옵션으로 `--vault`를 받는다. 입력 파일의 상대경로는 호출자 cwd 기준이다.

loaded `SKILL.md`에서 sibling `scripts/decision_init.py`와 별도 loaded core entrypoint를 resolve해 adapter를 한 번만 호출한다. cwd·plugin cache를 탐색하거나 대체 runtime을 쓰지 않는다.

```bash
INIT_SKILL_FILE="/absolute/path/from-loaded-skill-catalog/plugins/context-decision/skills/init/SKILL.md"
INIT_ENTRYPOINT="${INIT_SKILL_FILE%/SKILL.md}/scripts/decision_init.py"
python3 "$INIT_ENTRYPOINT" \
  --host <codex|claude-code> \
  --core-cli /absolute/active-installed/context-core/skills/context/scripts/context_cli.py \
  --json
```

Claude Code는 host가 준 `${CLAUDE_PLUGIN_ROOT}`만 optional route로 쓰고 Codex는 loaded catalog path를 쓴다. Adapter는 path suffix, 인접한 core manifest의 name·version 일치와 compatible major를 확인한 뒤 actual SHA-256을 operation에 결박하고 `context-core-schema/v1`, `context-common/v2`, `context-owner-descriptor/v2`, `filesystem-vault/v1`, 필수 command와 doctor state를 handshake한다. mismatch/incompatible은 write 0이다. absent/partial/invalid/ready 진단과 fixed descriptor/index seed는 검증된 core에 전달하며 core가 repair 가능성을 판정한다.

Core만 `core_init|area_register|policy_install`을 적용하고 managed block 밖 byte를 보존하며 retry를 수렴시킨다.

일반 durable capture는 rendered-file review가 아니라 semantic approval을 사용한다. 사용자가 decision·scope·lifecycle effect를 직접적·명시적·무조건적으로 확정하면 capture를 승인한 것이며, 미확정 의미만 묻는다. `알겠어` 단독, 조건, 수정 요청, 화제 전환은 승인이 아니다. 저장 본문을 보여주거나 별도 저장 승인을 묻지 않는다. 승인 뒤 내부 preview와 unchanged apply를 같은 응답에서 실행하고 digest·receipt 경로·내부 ID·core 경로는 비공개로 유지한다. preview에서 semantic delta가 드러나면 write를 보류하고 그 차이만 다시 확인한다. 승인 뒤 재생성하지 않는다.

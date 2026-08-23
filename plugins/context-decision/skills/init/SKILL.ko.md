---
name: init
description: 사용자가 현재 repository의 context-decision 초기화나 bootstrap을 명시적으로 요청했을 때 exact compatible context-core를 확인하고 필요한 core bootstrap과 decision area 등록을 한 번에 완료한다. 일반 decision capture 중에는 자동 실행하지 않는다.
---

# Init (한국어)

loaded `SKILL.md`에서 sibling `scripts/decision_init.py`와 별도 loaded core entrypoint를 resolve해 adapter를 한 번만 호출한다. cwd·plugin cache를 탐색하거나 대체 runtime을 쓰지 않는다.

```bash
INIT_SKILL_FILE="/absolute/path/from-loaded-skill-catalog/plugins/context-decision/skills/init/SKILL.md"
INIT_ENTRYPOINT="${INIT_SKILL_FILE%/SKILL.md}/scripts/decision_init.py"
python3 "$INIT_ENTRYPOINT" \
  --host <codex|claude-code> \
  --core-cli /absolute/active-installed/context-core/skills/context/scripts/context_cli.py \
  --json
```

Claude Code는 host가 준 `${CLAUDE_PLUGIN_ROOT}`만 optional route로 쓰고 Codex는 loaded catalog path를 쓴다. Adapter는 release pin의 path suffix/SHA-256을 확인한 뒤 `context-core-schema/v1`, `context-common/v2`, `context-owner-descriptor/v2`, 필수 command와 doctor state를 handshake한다. mismatch/incompatible은 write 0이다. absent/partial/invalid/ready 진단과 fixed descriptor/index seed는 pinned core에 전달하며 core가 repair 가능성을 판정한다.

Core만 `core_init|area_register|policy_install`을 적용하고 managed block 밖 byte를 보존하며 retry를 수렴시킨다.

일반 durable capture는 별도다. 기록 제안 전에 preview를 실행하고 완성된 렌더링 본문과 함께 한 번만 묻는다. preview stdout의 `approval_digest`는 agent가 그대로 apply에 전달하되 digest·receipt 경로·내부 ID·core 경로를 사용자에게 보이거나 요구하지 않는다. capture 질문에 대한 직접적·명시적·무조건적 긍정만 승인이다. `알겠어` 단독, 조건, 수정 요청, 화제 전환은 승인이 아니며 승인 뒤 content·plan을 재생성하지 않는다.

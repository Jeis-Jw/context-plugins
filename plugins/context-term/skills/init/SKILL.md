---
name: init
description: 사용자가 context-term 초기화를 명시적으로 요청했을 때 exact context-core v2 handshake 뒤 TERM descriptor/index를 core bootstrap으로 등록한다.
---

# Context term init

이 skill은 사용자가 `$context-term:init`을 명시했을 때만 실행한다. 자동 설치·활성화·update·downgrade·migration은 하지 않는다.

1. `REQUIRED_PLUGIN`의 core entrypoint suffix/SHA-256을 supplied `--core-cli`에 대조하고 loaded catalog에서 sibling entrypoint를 해석한다.
2. 일치한 core에서만 `context-core-schema/v1`, `context-common/v2`, `context-owner-descriptor/v2`, 필수 command와 doctor를 handshake한다.
3. `term_init.py`가 descriptor v2와 fixed index seed를 core `bootstrap`에 전달하고 ready/profile/index/managed policy 결과를 확인한다.

```bash
INIT_SKILL_FILE="<loaded-skill-path>/SKILL.md"
python3 "${INIT_SKILL_FILE%/SKILL.md}/scripts/term_init.py" \
  --host codex \
  --core-cli /absolute/path/to/context_cli.py \
  --json
```

TERM adapter는 temporary descriptor/seed 전달 외 write primitive가 없다. `absent|partial|invalid|ready`는 pinned core에 전달하며 mismatch는 subprocess, receipt와 repository write 0이다.

일반 durable capture는 별도다. 기록 제안 전에 preview를 실행하고 완성된 렌더링 본문과 함께 한 번만 묻는다. preview stdout의 `approval_digest`는 agent가 그대로 apply에 전달하되 digest·receipt 경로·내부 ID·core 경로를 사용자에게 보이거나 요구하지 않는다. capture 질문에 대한 직접적·명시적·무조건적 긍정만 승인이다. `알겠어` 단독, 조건, 수정 요청, 화제 전환은 승인이 아니며 승인 뒤 content·plan을 재생성하지 않는다.

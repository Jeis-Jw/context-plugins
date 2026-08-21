---
name: init
description: 사용자가 context-assumption 초기화를 명시적으로 요청했을 때 exact context-core v2 handshake 뒤 ASM descriptor/index를 core bootstrap으로 등록한다.
---

# Context assumption init

이 skill은 사용자가 `$context-assumption:init`을 명시했을 때만 실행한다. 자동 설치·활성화·update·downgrade·migration은 하지 않는다.

1. active host inventory와 core doctor receipt로 exact `context-core@context-plugins` identity/source/enabled/protocol과 public entrypoint absolute path를 확인한다.
2. loaded skill catalog에서 이 파일의 sibling entrypoint를 해석한다.
3. installed core `context_cli.py schema --json`이 `context-owner-descriptor/v2`를 광고하는지 확인한다.
4. 같은 호출에서 `assumption_init.py`가 descriptor v2와 fixed index seed를 core `bootstrap`에 전달한다.
5. bootstrap 뒤 core doctor ready, root owner-profile registry, area profile/index exact bytes와 managed host policy 결과를 다시 확인한다.

```bash
INIT_SKILL_FILE="<loaded-skill-path>/SKILL.md"
python3 "${INIT_SKILL_FILE%/SKILL.md}/scripts/assumption_init.py" \
  --host codex \
  --core-inventory @inventory.json \
  --core-doctor @doctor.json \
  --core-cli /absolute/path/to/context_cli.py \
  --json
```

ASM adapter는 temporary descriptor/seed 전달 외 repository write primitive를 갖지 않으며, durable bytes는 core만 쓴다.

`repository_state=partial`은 이 명시적 bootstrap repair에서만 허용한다. `invalid`는 init에서도 fail-closed한다. `--core-cli` realpath가 inventory entrypoint와 다르면 동명 script라도 실행하지 않는다.

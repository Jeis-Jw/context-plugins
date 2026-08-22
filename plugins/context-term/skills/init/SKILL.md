---
name: init
description: 사용자가 context-term 초기화를 명시적으로 요청했을 때 exact context-core v2 handshake 뒤 TERM descriptor/index를 core bootstrap으로 등록한다.
---

# Context term init

이 skill은 사용자가 `$context-term:init`을 명시했을 때만 실행한다. 자동 설치·활성화·update·downgrade·migration은 하지 않는다.

1. semantic CLI의 `REQUIRED_PLUGIN`에 고정된 `context-core@context-plugins` public entrypoint suffix와 SHA-256을 supplied absolute `--core-cli`에 대조한다.
2. loaded skill catalog에서 이 파일의 sibling entrypoint를 해석한다.
3. 일치한 core만 실행해 `context-core-schema/v1`, `context-common/v2`, `context-owner-descriptor/v2`, 필수 doctor/bootstrap/transaction command와 current doctor state를 직접 handshake한다.
4. 같은 호출에서 `term_init.py`가 descriptor v2와 fixed index seed를 core `bootstrap`에 전달한다.
5. bootstrap 뒤 core doctor ready, root owner-profile registry, area profile/index exact bytes와 managed host policy 결과를 다시 확인한다.

```bash
INIT_SKILL_FILE="<loaded-skill-path>/SKILL.md"
python3 "${INIT_SKILL_FILE%/SKILL.md}/scripts/term_init.py" \
  --host codex \
  --core-cli /absolute/path/to/context_cli.py \
  --json
```

TERM adapter는 temporary descriptor/seed 전달 외 repository write primitive를 갖지 않으며, durable bytes는 core만 쓴다.

`repository_state=absent|partial|invalid|ready`는 exact doctor handshake 뒤 pinned core bootstrap에 전달하며 실제 복구 가능 여부는 core가 판정한다. path 또는 SHA-256이 pin과 다르면 동명 script라도 subprocess, receipt와 repository write 0으로 중단한다.

---
name: init
description: 사용자가 현재 repository의 context-core 초기화나 bootstrap을 명시적으로 요청했을 때 canonical seed를 안전하고 멱등하게 적용한다. 일반 recall·capture 중에는 자동 실행하지 않는다.
---

# Init (한국어)

활성 host에 따라 `context_cli.py init --host codex --json` 또는 `context_cli.py init --host claude-code --json`을 한 번 호출한다. repository가 absent이면 canonical root/SNAP/OBS seed를 적용하고, 이어서 `codex → AGENTS.md`, `claude-code → CLAUDE.md`의 관리형 context policy block을 설치한 뒤 `doctor.repository_state=ready`를 반환한다. 이미 ready이고 block도 최신이면 `core_init`과 `policy_install` phase가 모두 noop이며 filesystem diff는 0이다.

policy target과 marker를 모든 write 전에 preflight한다. 기존 파일의 managed marker 밖 byte는 그대로 보존하고, marker가 깨졌거나 중복됐거나 target이 symlink·nested path이면 context storage까지 write 0으로 중단한다. populated repository에서 root index만 없으면 exact built-in SNAP/OBS metadata로만 derived root catalog를 rebuild하며 미등록 area를 자동 등록하지 않는다. legacy artifact와 unrelated corpus 진단은 init을 막지 않으며, init target의 incompatible schema/owner/path만 `partial_core_init`으로 중단한다.

addon이 `context-owner-descriptor/v2`를 제공하면 먼저 root-independent `schema --json`의 `features` handshake를 확인한다. feature가 없는 0.4.1 runtime에는 `bootstrap`을 호출하지 않아 bytes를 바꾸지 않는다. 지원 runtime에는 canonical JSON 8 KiB 이하 descriptor와 full descriptor block이 포함된 exact empty area seed를 함께 전달한다. v1/v2 mixed root는 허용하지만 v1 area에는 profile registry를 만들지 않는다. v2 descriptor digest는 immutable하므로 자동 downgrade·upgrade·migration 또는 삭제를 시도하지 않는다.

등록 재시도는 none, exact seed-only, exact root row+profile registry-only, complete 상태만 수렴시킨다. 그 밖의 partial state, unknown profile, descriptor/root/area digest 불일치는 write 0으로 중단한다.

이 명시적 init 호출은 fixed `core_init|area_register|policy_install`에만 적용 권한을 준다. 일반 SNAP·OBS·DEC/user-content mutation은 기존 complete bundle과 exact `approval_digest` 승인을 계속 요구하며, 물리 write는 context-core coordinator만 수행한다.

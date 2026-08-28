# Context Plugins

[English](./README.md)

Context Plugins는 모든 대화를 몰래 영구 상태로 만들지 않으면서 coding agent에 repository 소유의 durable project context를 제공합니다. 지원 profile은 Git/Markdown context를 회수하고 안전하게 기록하는 `context-core`와, 세션이 바뀌어도 결정·취지·반려대안을 보존하는 `context-decision`을 함께 사용합니다. Agent는 오래 남길 가치가 있는 맥락만 제안하고 complete preview를 보여준 뒤 사용자가 직접 승인한 경우에만 기록합니다.

> **Developer preview:** `0.7.1`은 `main`에 준비되어 있지만 `v0.7.1` tag는 아직 생성·push되지 않았습니다. Marketplace publication도 미완료입니다. 아래 설치 명령은 의도적으로 immutable tag를 사용하며 tag가 공개된 뒤에만 동작합니다. Source 공개, test, host lifecycle 검증은 tag, GitHub Release, marketplace publication 또는 지속 사용 가치의 증거가 아닙니다.

## 왜 필요한가요?

- 새 agent session이 현재 구조를 선택한 이유를 다시 물어보지 않아야 합니다.
- 이미 반려한 대안이 다음 작업에서 새로운 제안처럼 돌아오지 않아야 합니다.
- 유용한 운영 근거는 chat history 밖에서도 남되 자동으로 권위 있는 결정이 되어서는 안 됩니다.
- 검증되지 않은 전제는 provisional 상태가 분명해야 합니다.
- Durable write는 repository가 소유하는 review·rollback 가능한 Git 변경이어야 합니다.

Context Plugins는 transcript를 보관하지 않습니다. Index와 metadata로 후보를 먼저 좁히고, 현재 답변에 영향을 줄 수 있을 때만 실제 artifact body를 읽습니다.

## 플러그인 구성

| 플러그인 | 역할 | 상태 |
|---|---|---|
| `context-core` | Scope 기반 recall, `OBS` 근거, `SNAP` 인계, complete preview와 물리적 write 조정 | 필수 |
| `context-decision` | `DEC` 결정·취지·반려대안, conflict와 rationale change 감지 | 지원 profile에서 필수 |
| `context-assumption` | 명시적으로 검증되지 않은 전제와 confirm/refute lifecycle을 `ASM`으로 관리 | 선택, experimental |
| `context-term` | 프로젝트 전용 canonical definition과 alias를 `TERM`으로 관리 | 선택, experimental |

Bundle이나 meta-plugin은 없습니다. Core와 decision은 독립 package이고, 어떤 plugin도 다른 plugin을 암묵적으로 install·enable·update·init하지 않습니다. Core와 semantic addon은 반드시 같은 immutable checkout에서 설치해야 하며, 혼합 설치나 일부 update는 `core_surface_mismatch`로 중단됩니다.

## 요구사항과 지원 범위

| 항목 | 요구사항 또는 확인된 경계 |
|---|---|
| Python | Python 3.11 이상, runtime은 standard library 사용 |
| Repository | macOS 또는 Linux의 Git repository. Write coordinator가 POSIX `fcntl` lock 사용 |
| Codex | Plugin marketplace CLI. `0.149.0-alpha.4.1`에서 fresh install/cache lifecycle 확인 |
| Claude Code | Plugin marketplace CLI. `2.1.89`에서 fresh install/cache lifecycle 확인, runtime UX는 experimental |
| 지원 profile | `context-core@context-plugins` + `context-decision@context-plugins`, 모두 `0.7.1` |
| 선택 기능 | `context-assumption`, `context-term`은 설치 가능하지만 experimental |
| 언어 | Runtime과 문서의 canonical source는 영어입니다. 사용자 응답은 명시적 언어 선택, host의 preferred response language, 기존 대화 언어 순으로 따르고 판별할 수 없으면 영어를 사용합니다. 식별자와 machine-readable field는 영어로 유지합니다. |

Windows는 현재 지원하지 않습니다. 위 host version은 검증 당시의 snapshot이며 영구적인 최소 version이나 호환성 보장은 아닙니다.

## 설치

지원 경로는 clean immutable release checkout 하나에서 시작합니다.

```bash
git clone --branch v0.7.1 --depth 1 https://github.com/Jeis-Jw/context-plugins.git context-plugins-v0.7.1
cd context-plugins-v0.7.1
```

### Codex

```bash
python3 scripts/install_profile.py --host codex
```

### Claude Code

설치 scope를 명시합니다. 이 문서의 예시는 user scope입니다.

```bash
python3 scripts/install_profile.py --host claude-code --scope user
```

Installer는 release surface의 version 정합성을 확인하고, 필요하면 현재 checkout을 `context-plugins` marketplace로 등록한 뒤 core와 decision 순서로 설치합니다. Legacy provider, mixed version, disabled plugin 또는 다른 checkout을 가리키는 marketplace가 있으면 변경 전에 중단합니다. 기존 context를 migration하거나 부분 설치 실패를 자동 rollback하지 않습니다.

설치 후 host를 reload하거나 새 session을 여세요.

### 선택형 experimental owner

실제로 필요한 lifecycle만 같은 checkout에서 설치합니다.

```bash
codex plugin add context-assumption@context-plugins
codex plugin add context-term@context-plugins

claude plugin install context-assumption@context-plugins --scope user
claude plugin install context-term@context-plugins --scope user
```

## 프로젝트 초기화

Context를 소유할 Git repository에서 다음 selector를 한 번 실행합니다.

```text
$context-decision:init
```

이 idempotent action 하나가 core storage를 초기화하고 DEC area를 등록하며, Codex에서는 `AGENTS.md`, Claude Code에서는 `CLAUDE.md`에 managed host policy를 설치합니다. 지원 profile에서는 `$context-core:init`을 따로 실행할 필요가 없습니다.

선택 owner를 설치했다면 각각 초기화합니다.

```text
$context-assumption:init
$context-term:init
```

## 몇 분 안에 첫 가치 확인하기

초기화 뒤에는 평범한 자연어로 사용합니다. 매 turn마다 별도 명령을 실행하지 않습니다.

1. 실제 프로젝트 결정을 agent에게 설명합니다.

   > 브라우저 저장소는 injected script에 노출될 수 있어 session token을 HTTP-only cookie에 두기로 했다. 기존 프로젝트 결정과 비교하고 앞으로 작업을 안내할 가치가 있을 때만 durable decision으로 제안해줘.

2. Complete preview의 scope, 결정, 취지와 반려대안을 검토합니다. 모두 정확할 때만 capture 질문에 직접 승인합니다.
3. 다음 session에서 요청합니다.

   > 인증 방식을 변경하기 전에 관련 프로젝트 결정을 회수하고 충돌이 있으면 알려줘.

첫 durable write는 storage와 approval 경로가 동작한다는 증거입니다. Recall이 실제 작업을 개선하는지는 actual model과 반복 사용을 이용한 별도 가치검증으로 입증해야 합니다.

## 평소 사용법

| 목적 | 요청 예시 |
|---|---|
| 이전 맥락을 반영해 재개 | “이 작업을 계속하기 전에 관련 결정과 observation을 확인해줘.” |
| 충돌 확인 | “이 queue를 도입하기 전에 Current 결정과 비교하고 충돌을 설명해줘.” |
| 근거 보존 | “이 운영 결과를 결정으로 취급하지 말고 재사용 가능한 observation으로 제안해줘.” |
| 미완료 작업 인계 | “현재 상태, blocker와 다음 행동을 snapshot으로 준비해줘.” |
| 결정 변경 | “새 취지를 Current 결정과 비교하고 supersede가 필요한지 알려줘.” |
| 미검증 전제 추적 | “IdP가 5초 안에 응답한다는 전제를 확인·반증 조건과 함께 기록해줘.” |
| 프로젝트 용어 정의 | “이 repository에서 BFF의 의미와 허용 alias를 기록해줘.” |

Managed policy는 새로 추가된 의미만 audit합니다. Durable signal이 없으면 조용히 있고, 이전 맥락이 답변을 바꿀 수 있을 때 metadata-first recall 뒤 선택된 실제 body를 비교합니다.

## 승인과 안전 경계

```text
대화의 새 의미
  -> 관련 metadata-first recall
  -> 선택한 실제 body 비교
  -> conflict 또는 rationale change 알림
  -> complete preview
  -> 자연어 capture 질문 한 번
  -> 직접적·명시적·무조건적 승인
  -> context-core transaction 한 번
```

- Preview, 단순 acknowledgment, 칭찬, 수정 요청, 조건 또는 화제 전환은 승인이 아닙니다. `Okay`나 `알겠어`만으로는 write를 허가하지 않으며 모호한 응답은 한 번만 재확인합니다.
- Capture 질문 전에 preview를 고정하고 승인 뒤 다시 생성하지 않습니다.
- 내부 digest, receipt 위치, runtime path와 transport ID는 agent 내부에 둡니다.
- Mutation 전에 repository identity, pinned runtime byte, compare-and-swap, lock ownership과 atomic write 조건을 다시 확인합니다.
- 물리적 writer는 `context-core` 하나뿐입니다. Semantic owner는 검증된 의미만 반환하고 repository 파일을 직접 쓰지 않습니다.
- Healthy index의 zero-match는 indexed artifact bodies를 열지 않습니다. Stale/missing index recovery는 recall당 최대 20 bodies를 엽니다.
- Body materialization, selected output, owner input과 candidate envelope에는 hard bound가 있습니다. Directory enumeration, index scoring과 end-to-end model tokens가 O(1)이라고 보장하지 않습니다.
- Semantic owner와 core는 `context-common/v2` runtime contract를 검증합니다. 이 handshake는 marketplace provenance나 host enabled state의 증명이 아닙니다.

## 저장되는 내용

모든 durable context는 대상 repository의 plain Markdown입니다.

```text
context/
  context.index.md
  decision/       # DEC: authoritative Current 결정과 superseded history
  observation/    # OBS: 재사용 가능하지만 non-authoritative인 근거
  snapshot/       # SNAP: 임시 resume·handoff 상태
  assumption/     # ASM: provisional premise (선택)
  term/           # TERM: 프로젝트 전용 definition (선택)
```

Artifact는 일반 Git diff, review, branch와 rollback 흐름을 그대로 사용합니다. 별도 database, vector store, SaaS account, background transcript collector 또는 Obsidian 설치가 필요하지 않습니다.

## 제거와 rollback

선택 owner를 설치했다면 먼저 제거하고, decision을 core보다 먼저 제거합니다.

### Codex

```bash
codex plugin remove context-decision@context-plugins --json
codex plugin remove context-core@context-plugins --json
codex plugin marketplace remove context-plugins --json
```

### Claude Code

설치할 때 선택한 것과 같은 scope를 사용합니다.

```bash
claude plugin uninstall context-decision@context-plugins --scope user
claude plugin uninstall context-core@context-plugins --scope user
claude plugin marketplace remove context-plugins
```

Host uninstall은 대상 repository를 변경하지 않습니다. 기존 `context/` artifact와 managed policy block은 review 가능한 Git content로 남습니다. Corpus 삭제, managed-policy 제거, downgrade 또는 storage migration을 자동 수행하는 명령은 없습니다. 폐기나 rollback이 필요하면 명시적인 Git review 변경으로 처리합니다.

기존 `context-core@jeis-ai-plugins`는 별도 distribution입니다. 이 profile이 기존 설치나 corpus를 자동 교체·migration하지 않습니다. 자세한 경계는 [MIGRATION.md](./MIGRATION.md)를 참고하세요.

## 검증 상태와 제한사항

| 근거 | 결과 | 경계 |
|---|---|---|
| Python 3.11 전체 suite, 2026-08-26 | 299 passed, 242 subtests | 깨끗한 임시 환경; `python3.11 -m pytest -q` |
| Python 3.13 전체 suite, 2026-08-26 | 299 passed, 242 subtests | `python3.13 -m pytest -q` |
| 두 interpreter의 Phase 0 | 각각 15 passed, 27 subtests | Filesystem과 host-inventory contract probe |
| Codex `0.149.0-alpha.4.1` | core+decision fresh install/cache lifecycle 통과 | Host lifecycle 근거이며 model behavior 근거 아님 |
| Claude Code `2.1.89` | core+decision fresh install/cache lifecycle 통과 | Runtime UX는 experimental |
| Codex + Claude Code | 네 plugin 모두 install/load 통과 | ASM/TERM은 optional experimental surface |
| Actual model behavior | 미확인 | No-signal 비율, capture 품질, task outcome, retained use, end-to-end token 측정 없음 |

Codex prompt material은 3,147자에서 1,333자로 57.6% 감소했습니다. 문자 수 측정이며 token 절감률 주장이 아닙니다.

준비된 manifest, local catalog, test, `main`의 source 또는 installer dry run은 `v0.7.1` tag, GitHub Release, marketplace publication이나 실제 사용자 채택의 증거가 아닙니다. Publication과 가치증명은 별도 gate로 남아 있습니다.

## 라이선스

Context Plugins는 [Apache License 2.0](./LICENSE)으로 배포됩니다.

## 더 알아보기

- [English default](./README.md)
- [`context-core`](./plugins/context-core/README.md)
- [`context-decision`](./plugins/context-decision/README.md)
- [`context-assumption`](./plugins/context-assumption/README.md)
- [`context-term`](./plugins/context-term/README.md)
- [Migration 경계](./MIGRATION.md)
- [Release notes](./RELEASE_NOTES.md)
- [개발과 검증](./DEVELOPMENT.md)

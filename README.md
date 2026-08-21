# Context Plugins

Coding agent가 세션이 바뀌어도 프로젝트의 **결정, 근거, 현재 상태와 작업 인계**를 이어가도록 돕는 Git/Markdown 기반 플러그인입니다.

관련 맥락만 골라 실제 본문을 읽고, 기존 결정과 충돌하거나 취지가 달라졌다면 먼저 알려줍니다. 새 맥락은 사용자에게 기록 후보를 보여준 뒤 명시적으로 승인받은 경우에만 repository의 `context/`에 저장합니다.

> 현재 `0.4.1` source와 marketplace manifest는 공개되어 있지만, fresh host에서의 end-to-end 설치와 marketplace catalog 배포는 아직 검증되지 않았습니다. 공개 라이선스도 아직 선택되지 않았으므로 실제 사용·복제·재배포 전에는 [현재 배포 상태](#현재-배포-상태)를 확인하세요.

## 이런 문제를 해결합니다

- 새 session을 열 때마다 “왜 이 구조를 선택했는지” 다시 설명해야 합니다.
- 이미 반려한 대안이 다음 작업에서 다시 제안됩니다.
- 중요한 실험 결과와 운영상 주의점이 대화 기록에만 남아 재사용되지 않습니다.
- agent가 맥락을 자동 저장하면 불필요하거나 잘못된 내용까지 장기 기억에 섞일 수 있습니다.
- 작업을 중단한 뒤 다음 agent가 현재 상태와 다음 행동을 복원하기 어렵습니다.

Context Plugins는 모든 대화를 보관하지 않습니다. 현재 판단에 필요한 repository-local context만 회수하고, 오래 남길 가치가 있는 내용만 승인형 기록 후보로 제안합니다.

## 제공하는 플러그인

| 플러그인 | 사용자에게 제공하는 기능 | 설치 관계 |
|---|---|---|
| `context-core` | 관련 맥락 recall, 작업 인계 `SNAP`, 재사용 가능한 근거 `OBS`, 승인 preview와 안전한 기록 | 기본 플러그인 |
| `context-decision` | 기존 `DEC` 본문 비교, 충돌·취지 변경 알림, 반려 대안과 superseded history 보존 | `context-core@context-plugins` 필요 |

결정 관리가 필요 없다면 `context-core`만 사용할 수 있습니다. 기존 결정과의 연속성까지 관리하려면 두 플러그인을 함께 설치합니다.

## 동작 방식

```text
사용자 대화
    ↓
관련 Current context만 탐색
    ↓
선택된 실제 본문과 현재 요청 비교
    ↓
답변 또는 충돌·취지 변경 알림
    ↓
기록할 가치가 있을 때만 capture preview 제안
    ↓
사용자가 exact approval_digest 승인
    ↓
context/*.md와 index를 하나의 transaction으로 갱신
```

평범한 대화에는 별도 audit 메시지를 표시하지 않습니다. 관련 결정이나 근거가 판단을 바꿀 때만 필요한 문서를 읽고, 기록할 내용이 충분히 성숙했을 때만 제안합니다.

## 설치

현재 중앙 marketplace catalog 배포 전이므로 GitHub repository를 marketplace source로 직접 추가하는 흐름을 기준으로 합니다. 아래 명령은 현재 Codex·Claude Code CLI와 이 repository manifest의 정적 계약을 반영했으며, fresh host의 전체 설치 흐름은 아직 검증 전입니다.

### Codex

```bash
codex plugin marketplace add Jeis-Jw/context-plugins --ref main
codex plugin add context-core@context-plugins
codex plugin add context-decision@context-plugins
```

### Claude Code

```bash
claude plugin marketplace add Jeis-Jw/context-plugins
claude plugin install context-core@context-plugins
claude plugin install context-decision@context-plugins
```

`context-core`만 쓸 경우 마지막 `context-decision` 설치 명령은 생략합니다. 설치 scope와 활성화 범위는 host가 제공하는 수단 안에서 사용자가 직접 정해야 하며, 플러그인이 다른 플러그인을 자동 설치·활성화하거나 host 설정을 임의로 바꾸지 않습니다.

설치 후 host를 reload하거나 새 session을 여세요.

## 처음 한 번 초기화

사용할 repository에서 다음 중 하나를 요청합니다.

- `context-core`만 설치했다면: `$context-core:init`
- 두 플러그인을 설치했다면: `$context-decision:init`

`$context-decision:init`은 설치된 exact `context-core`를 확인한 뒤 core storage와 decision area를 함께 준비하므로 `$context-core:init`을 먼저 실행할 필요가 없습니다.

초기화가 성공하면 응답에서 다음을 확인할 수 있습니다.

- `doctor.repository_state: ready`
- Codex는 `AGENTS.md`, Claude Code는 `CLAUDE.md`에 설치된 managed policy target
- 각 init phase의 `applied` 또는 `noop` 상태

초기화는 `context/`의 고정 scaffold와 현재 host의 managed policy block만 설치합니다. 이미 준비된 repository에서 다시 실행하면 안전한 `noop`입니다.

## 평소에는 자연어로 사용합니다

초기화 이후 매 turn마다 별도 명령을 실행할 필요는 없습니다. 필요할 때 다음처럼 요청하면 됩니다.

| 하고 싶은 일 | 요청 예시 |
|---|---|
| 이전 맥락을 반영해 작업 재개 | “이 repository의 관련 결정과 관찰을 확인하고 이어서 설명해줘.” |
| 새 선택의 충돌 확인 | “이 선택이 기존 결정과 충돌하는지 먼저 확인해줘.” |
| 중요한 근거 보존 | “이번 운영 결과를 재사용 가능한 observation 후보로 만들어줘.” |
| 작업 인계 | “여기서 중단할 수 있게 현재 상태를 snapshot으로 정리해줘.” |
| 결정 변경 | “기존 결정을 유지할지 supersede할지 실제 취지까지 비교해줘.” |

플러그인은 관련 신호를 발견하면 먼저 기존 context를 비교하고, 답변을 마친 뒤 필요한 경우에만 grouped capture를 제안합니다. 제안이나 preview만으로는 파일이 바뀌지 않습니다.

## 무엇이 저장되나요?

```text
context/
  context.index.md
  decision/       # DEC: 현재 따를 결정과 superseded history
  observation/    # OBS: 판단을 뒷받침하는 비권위 근거와 발견
  snapshot/       # SNAP: 다음 session을 위한 작업 인계
```

| 종류 | 의미 | 권위 |
|---|---|---|
| `DEC` | 무엇을 선택했고 왜 따르는지, 무엇을 반려했는지 | Current 문서는 authoritative |
| `OBS` | 재사용할 사실, 증거, 시행착오 | 판단을 돕는 evidence |
| `SNAP` | 미완료 작업의 현재 상태와 다음 행동 | 재개용 staging |

모든 artifact는 Markdown이라 일반 Git diff, review, branch와 rollback을 그대로 사용할 수 있습니다. 별도 database, vector store, SaaS 계정이나 Obsidian이 필요하지 않습니다.

## 안전 경계

- 일반 context 기록은 complete preview의 정확한 `approval_digest`를 사용자가 승인하기 전까지 쓰지 않습니다.
- hash, ID나 index metadata만으로 의미가 같다고 판단하지 않고 실제 body, scope와 rationale를 비교합니다.
- metadata와 index로 후보를 먼저 좁힌 뒤 관련 있는 실제 문서만 읽습니다.
- background daemon처럼 대화를 수집하거나 transcript 전체를 자동 보관하지 않습니다.
- 명시적 `init` 외에는 plugin 설치·활성화와 host configuration을 자동으로 변경하지 않습니다.
- source, version 또는 protocol이 맞지 않으면 대상 파일을 쓰지 않고 필요한 exact 좌표를 안내합니다.
- 기존 `wiki/`나 과거 distribution의 context를 자동 migration하지 않습니다.

## 현재 배포 상태

| 항목 | 상태 |
|---|---|
| GitHub source | [`Jeis-Jw/context-plugins`](https://github.com/Jeis-Jw/context-plugins)에 public |
| 현재 version | `0.4.1` |
| Marketplace identity | `context-plugins` |
| Storage protocol | `context-common/v2` |
| Codex·Claude Code manifests | repository에 포함 |
| Fresh host live install | 아직 미검증 |
| 중앙 marketplace catalog 배포 | 아직 미완료 |
| 공개 라이선스 | 아직 미선택 — `LICENSE` 추가 전에는 사용·복제·재배포 권한이 자동 부여되지 않음 |

기존 `context-core@jeis-ai-plugins`는 별도 distribution입니다. 새 `context-core@context-plugins` 설치로 자동 전환되지 않으며, storage 이동도 자동 수행하지 않습니다. 자세한 경계는 [MIGRATION.md](./MIGRATION.md)를 참고하세요.

## 더 알아보기

- [`context-core` 상세 동작](./plugins/context-core/README.md)
- [`context-decision` 상세 동작과 오류 안내](./plugins/context-decision/README.md)
- [기존 distribution에서의 migration 경계](./MIGRATION.md)

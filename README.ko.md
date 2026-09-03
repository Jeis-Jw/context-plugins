# Context Plugins

[English](./README.md)

Context Plugins는 AI 코딩 에이전트에게 프로젝트 전용 기억을 만들어주는 플러그인입니다. 중요한 결정과 필요한 맥락을 프로젝트 안에 보관하고, 관련 작업을 할 때 다시 떠올리며, 사용자가 명시적으로 확정하거나 기억해 달라고 한 의미만 저장합니다.

## 무엇인가요?

AI 코딩 에이전트는 유용하지만 새 대화를 시작하면 “왜 이렇게 만들었는지”를 잊을 수 있습니다. Context Plugins는 대화가 바뀌어도 남아야 할 내용을 보관합니다.

- **결정** — 무엇을 선택했고, 왜 선택했으며, 어떤 대안을 제외했는지
- **취지** — 프로젝트가 지속적으로 지향하려는 방향
- **관찰 기록** — 테스트 결과, 장애 원인처럼 다음에도 활용할 수 있는 사실
- **원본 보관** — 근거로 채택한 불변 장문 원본
- **문서** — 같은 식별자를 유지하면서 내용을 갱신할 living project guidance
- **작업 현황** — 어디까지 작업했고 다음에 무엇을 해야 하는지

저장된 내용은 filesystem vault의 `context/` 폴더에 일반 Markdown 파일로 남습니다. 직접 읽고 수정할 수 있고, 필요하면 기존 파일 공유나 버전 관리 방식으로 함께 사용할 수 있습니다. Git은 선택 사항이며 runtime 전제가 아닙니다.

Context Plugins는 대화 전체를 자동으로 저장하지 않습니다. 의미·scope·lifecycle effect가 미확정일 때만 그 부분을 짧게 확인하며, 저장 파일 본문을 승인용 preview로 보여주지 않습니다.

## 왜 사용하나요?

- 새 대화를 시작할 때마다 같은 결정과 배경을 다시 설명하지 않아도 됩니다.
- 이미 제외한 방법이 새로운 제안처럼 반복되는 일을 줄일 수 있습니다.
- 새 작업이 기존 결정과 충돌하면 코드를 바꾸기 전에 알 수 있습니다.
- 중요한 결과와 미완료 작업의 상태를 채팅창이 아니라 프로젝트에 남길 수 있습니다.
- 명시적으로 확정하거나 기억해 달라고 요청한 내용만 저장하므로 사용자가 계속 통제할 수 있습니다.

## 설치하기

Codex 또는 Claude Code, macOS나 Linux의 프로젝트 폴더, Python 3.11 이상이 필요합니다. 이 저장소를 직접 다운로드할 필요는 없습니다.

### Codex

터미널에서 다음 명령을 차례로 실행하세요.

```bash
codex plugin marketplace add Jeis-Jw/context-plugins
codex plugin add context-core@context-plugins
codex plugin add context-decision@context-plugins
```

### Claude Code

터미널에서 다음 명령을 차례로 실행하세요.

```bash
claude plugin marketplace add Jeis-Jw/context-plugins --scope user
claude plugin install context-core@context-plugins --scope user
claude plugin install context-decision@context-plugins --scope user
```

Marketplace가 이미 등록되어 있다면 첫 번째 명령은 생략해도 됩니다. 설치가 끝나면 에이전트를 다시 시작하거나 새 세션을 여세요.

처음 사용할 때는 `context-core`와 `context-decision`만 설치하면 됩니다. 모든 semantic owner는 `context-core`가 필요하지만 semantic owner끼리는 서로를 요구하지 않습니다. 필요한 optional owner만 아래 명령으로 설치하고 초기화하세요. 하나를 설치해도 다른 owner가 자동으로 설치되거나 초기화되지 않습니다.

| Optional owner | Codex 설치 | Claude Code 설치 | Agent 대화창에서 초기화 |
| --- | --- | --- | --- |
| Intent | `codex plugin add context-intent@context-plugins` | `claude plugin install context-intent@context-plugins --scope user` | `$context-intent:init` |
| Document | `codex plugin add context-document@context-plugins` | `claude plugin install context-document@context-plugins --scope user` | `$context-document:init` |
| Assumption | `codex plugin add context-assumption@context-plugins` | `claude plugin install context-assumption@context-plugins --scope user` | `$context-assumption:init` |
| Term | `codex plugin add context-term@context-plugins` | `claude plugin install context-term@context-plugins --scope user` | `$context-term:init` |

### Context type의 관계

- **Intent**는 desired direction입니다.
- **Observation**과 **Assumption**은 evidence와 premise입니다.
- **Archive**는 불변 source evidence이며 명시적으로 포함하지 않으면 기본 recall에서 제외됩니다.
- **Decision**은 chosen commitment입니다.
- **Rationale**은 해당 근거에서 왜 그 결정을 택했고 그 결정이 Intent를 어떻게 섬기는지 설명합니다.
- **Document**는 식별자를 유지하면서 갱신할 수 있는 living content입니다.

intent-only, decision-only, document-only로 각각 사용할 수 있습니다. 관련 artifact가 함께 존재하면 decision이 `serves:intent`, `informed_by:observation`, `informed_by:assumption`, `affects:document` 관계를 기록할 수 있습니다. 이 관계는 inverse record를 만들지 않고 어떤 plugin도 필수로 바꾸지 않습니다.

artifact 한도는 기본 읽기 예산입니다. 지식은 slot 크기가 아니라 slot 수로 확장합니다. 예를 들어 하나의 설계를 `design-skeleton`·`design-envelope`·`design-rules`로 분해하고, 시점 고정 장문 원본은 ARCHIVE에 보관해 명시적으로만 읽습니다.

## 사용하는 방법

### 1. 프로젝트 초기화하기

Codex 또는 Claude Code에서 프로젝트를 연 뒤, 터미널이 아니라 에이전트와의 대화창에 다음 메시지를 보내세요.

```text
$context-decision:init
```

프로젝트마다 한 번만 실행하면 됩니다. 플러그인이 프로젝트의 `context/` 폴더와 에이전트에게 필요한 안내를 준비합니다.

### 2. 평소처럼 대화하기

일상적인 사용에는 별도 명령이 필요하지 않습니다. 다음처럼 자연어로 요청하면 됩니다.

- “인증과 데이터베이스를 한 번에 제공해서 Supabase를 사용하기로 했어. 이 결정을 기억해줘.”
- “로그인 방식을 바꾸기 전에 이와 관련해 이미 내린 결정이 있는지 확인해줘.”
- “이번 배포 결과를 다음 작업에서도 활용할 수 있게 남겨줘.”
- “지금까지 진행한 내용과 다음에 할 일을 저장해줘.”

### 3. 내용 확정하기

생성된 Markdown 파일이 아니라 대화에서 내용 자체를 확인합니다.

- 결정을 분명히 확정하거나 확정된 내용을 기억해 달라고 요청하면 별도 문서 preview 없이 저장됩니다.
- 의미·scope·교체 효과가 불분명할 때만 에이전트가 그 부분을 짧게 확인합니다.
- 미확정 내용에 대한 단순한 확인이나 맞장구는 승인이 아닙니다.
- 저장 뒤에는 파일 본문 대신 기록 결과만 알려줍니다.

### 4. 다음 대화에서 이어가기

저장된 내용이 현재 작업과 관련 있으면 에이전트가 다시 참고할 수 있습니다. 직접 요청해도 됩니다.

> 이 작업을 계속하기 전에 프로젝트에 저장된 결정을 먼저 확인해줘.

기억이 프로젝트 안에 저장되므로 다른 에이전트나 팀원도 이전에 내린 선택을 이해하는 데 활용할 수 있습니다.

### 5. 브랜치, 병합, CI

`context/` 아래 Markdown 파일이 정본입니다. 옆에 있는 `*.index.md`는 빠른 조회용으로 생성되는 투영(projection)이며, 새로 clone해도 별도 빌드 없이 동작하도록 함께 커밋합니다.

- 프로젝트가 Git 저장소이면 `init`이 `.gitattributes`에 관리 블록을 추가해, 두 브랜치가 각각 결정을 기록해도 생성 index가 충돌하지 않고 union으로 병합됩니다. vault가 Git checkout 밖에 있으면 `context/**/*.index.md merge=union` 한 줄을 직접 추가하세요. `doctor`가 `merge_attributes_missing`으로 알려줍니다.
- 병합 뒤에는 다음 context 기록이 index를 다시 만듭니다. 바로 정리하려면 `context_cli.py refresh --fix index`를 실행합니다. `context_cli.py`는 설치된 플러그인 디렉터리 안의 `context-core` 진입점입니다([DEVELOPMENT.md](./DEVELOPMENT.md) 참고).
- 두 브랜치가 같은 scope·key에 서로 다른 결정을 기록했다면 `doctor`가 `duplicate_current_slot`을 보고합니다. 그 slot의 기록은 하나를 withdraw하거나 supersede할 때까지 보류되고, 다른 slot은 계속 동작하며, 자동으로 고르지 않습니다.
- CI에서는 프로젝트 루트에서 `context_cli.py refresh --check --json`을 실행하세요. index가 artifact와 어긋나거나 무결성 문제가 있으면 non-zero로 종료합니다.

기록에 결박되는 것은 사용자가 승인한 결정 내용뿐입니다. 그 사이 다른 브랜치가 병합됐어도 기록은 진행되고 index는 lock 안에서 재생성됩니다. 대상 기록 자체가 바뀌었거나, 같은(또는 겹치는) scope·key에 경쟁 결정이 들어온 경우에만 멈춥니다.

Context Plugins는 [Apache License 2.0](./LICENSE)으로 제공됩니다.

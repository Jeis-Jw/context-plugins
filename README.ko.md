# Context Plugins

[![test](https://github.com/Jeis-Jw/context-plugins/actions/workflows/test.yml/badge.svg)](https://github.com/Jeis-Jw/context-plugins/actions/workflows/test.yml)

[English](./README.md)

Context Plugins는 Codex와 Claude Code가 프로젝트의 중요한 내용을 기억하도록 돕는 플러그인입니다. 결정한 내용과 그 이유, 하던 일을 남겨 새 대화에서도 이어갈 수 있게 합니다.

## 무엇인가요?

AI와 함께 개발하다 보면 새 대화에서 프로젝트를 처음부터 다시 설명해야 할 때가 있습니다. Context Plugins는 대화가 바뀌어도 남아야 할 내용을 프로젝트에 보관합니다.

- **결정** — 무엇을 선택했고, 왜 그렇게 했는지
- **프로젝트 방향** — 누구를 위해 무엇을 만들고 있는지
- **작업 중 알게 된 사실** — 잘된 방법이나 문제를 해결한 과정
- **참고 자료** — 나중에 다시 확인할 원본 자료
- **프로젝트 문서** — 작업하면서 계속 다듬어 가는 기획과 안내
- **작업 현황** — 어디까지 했고 다음에 무엇을 해야 하는지

저장된 내용은 기본적으로 프로젝트의 `context/` 폴더에 읽기 쉬운 Markdown 문서로 남습니다. 직접 열어보거나 함께 일하는 사람과 공유할 수 있습니다.

Context Plugins는 대화 전체를 자동으로 저장하지 않습니다. 사용자가 분명히 확정하거나 기억해 달라고 요청한 내용만 저장합니다.

## 왜 사용하나요?

- 새 대화에서 같은 결정과 배경을 반복해서 설명하는 일을 줄일 수 있습니다.
- 이미 제외한 방법이 다시 제안되는 일을 줄일 수 있습니다.
- 새 요청이 기존 결정과 맞지 않을 때 AI가 먼저 확인하도록 돕습니다.
- 남겨둔 결과와 다음 할 일을 참고해 하던 작업을 이어갈 수 있습니다.

## 설치하기

Codex 또는 Claude Code, macOS나 Linux의 프로젝트 폴더, Python 3.11 이상이 필요합니다.

사용하는 도구에 맞춰 아래 명령을 터미널에 한 줄씩 붙여 넣고 실행하세요.

### Codex

```bash
codex plugin marketplace add Jeis-Jw/context-plugins
codex plugin add context-core@context-plugins
codex plugin add context-decision@context-plugins
```

### Claude Code

```bash
claude plugin marketplace add Jeis-Jw/context-plugins --scope user
claude plugin install context-core@context-plugins --scope user
claude plugin install context-decision@context-plugins --scope user
```

이 플러그인의 Marketplace를 이미 등록했다면 첫 번째 명령은 생략해도 됩니다. 설치가 끝나면 Codex 또는 Claude Code를 다시 시작하거나 새 대화를 여세요.

처음 사용할 때는 `context-core`와 `context-decision`만 설치하면 됩니다.

<details>
<summary>프로젝트 방향·문서·가정·용어도 기억하게 하고 싶다면</summary>

필요한 기능만 골라 추가할 수 있습니다. 각 추가 기능에는 `context-core`가 필요하며, 추가 기능끼리는 함께 설치할 필요가 없습니다. 사용하는 도구의 명령으로 설치한 뒤, 마지막 열의 명령을 AI와의 대화창에 보내세요.

| 추가로 기억할 내용 | Codex 설치 | Claude Code 설치 | 대화창에서 처음 한 번 |
| --- | --- | --- | --- |
| 프로젝트 방향 | `codex plugin add context-intent@context-plugins` | `claude plugin install context-intent@context-plugins --scope user` | `$context-intent:init` |
| 기획·안내 문서 | `codex plugin add context-document@context-plugins` | `claude plugin install context-document@context-plugins --scope user` | `$context-document:init` |
| 확인이 필요한 가정 | `codex plugin add context-assumption@context-plugins` | `claude plugin install context-assumption@context-plugins --scope user` | `$context-assumption:init` |
| 프로젝트 용어 | `codex plugin add context-term@context-plugins` | `claude plugin install context-term@context-plugins --scope user` | `$context-term:init` |

</details>

## 사용하는 방법

### 1. 프로젝트에서 처음 한 번 준비하기

Codex 또는 Claude Code에서 프로젝트를 연 뒤, AI와의 대화창에 다음 메시지를 보내세요.

```text
$context-decision:init
```

프로젝트마다 한 번만 실행하면 됩니다. 필요한 폴더와 AI가 참고할 안내를 준비해줍니다.

### 2. 평소처럼 대화하기

따로 명령어를 외울 필요 없이 평소 말하듯 요청하면 됩니다.

- “첫 버전은 회원가입 없이 쓸 수 있게 만들기로 했어. 이 결정을 기억해줘.”
- “로그인 기능을 추가하기 전에 관련해서 정한 내용이 있는지 확인해줘.”
- “방금 해결한 문제와 해결 방법을 다음에도 참고할 수 있게 남겨줘.”
- “지금까지 진행한 내용과 다음에 할 일을 저장해줘.”

### 3. 저장할 내용 확인하기

결정을 분명히 확정하거나 “이 내용을 기억해줘”라고 요청하면 AI가 저장하고 결과를 알려줍니다. 저장을 위해 같은 내용을 다시 승인할 필요는 없습니다.

어디에 적용할 결정인지, 기존 결정을 바꾸려는 것인지 등이 불분명하면 그 부분만 먼저 확인합니다. 아직 정하지 않은 내용은 “알겠어” 같은 맞장구만으로 저장하지 않습니다.

### 4. 다음 대화에서 이어가기

새 대화에서 관련 작업을 할 때 AI가 저장된 내용을 참고할 수 있습니다. 직접 이렇게 요청해도 됩니다.

> 이 작업을 계속하기 전에 프로젝트에 저장된 결정을 먼저 확인해줘.

프로젝트를 공유하면 다른 AI나 함께 일하는 사람도 같은 기록을 참고할 수 있습니다.

기여 방법과 pull request 검증 항목은 [CONTRIBUTING.md](./CONTRIBUTING.md)를 참고하세요. 보안 문제는 [SECURITY.md](./SECURITY.md)의 비공개 경로로 알려주세요.

Context Plugins는 [Apache License 2.0](./LICENSE)으로 제공됩니다.

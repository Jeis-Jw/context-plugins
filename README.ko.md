# Context Plugins (한국어)

Coding agent가 세션이 바뀌어도 프로젝트의 **결정, 근거, 미검증 전제, 프로젝트 용어, 현재 상태와 작업 인계**를 이어가도록 돕는 Git/Markdown 기반 플러그인입니다.

관련 맥락만 골라 실제 본문을 읽고, 기존 결정과 충돌하거나 취지가 달라졌다면 먼저 알려줍니다. 새 맥락은 사용자에게 기록 후보를 보여준 뒤 명시적으로 승인받은 경우에만 repository의 `context/`에 저장합니다.

> `0.5.1` developer preview는 local release 후보 commit으로 준비됐습니다. local `0.5.1` release 후보 commit도 아직 push되지 않았고, `v0.5.1` tag는 아직 생성·push되지 않았으며 marketplace publication도 미완료입니다. 공개 라이선스도 선택되지 않았으므로 실제 사용·복제·재배포 전에는 [현재 배포 상태](#현재-배포-상태)를 확인하세요.

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
| `context-assumption` | 미검증 전제 `ASM`, 확인·반증 조건, confirm/refute/supersede lifecycle | `context-core@context-plugins` 필요, 선택 설치 |
| `context-term` | 프로젝트 전용 용어 `TERM`, canonical definition과 alias/deprecation lifecycle | `context-core@context-plugins` 필요, 선택 설치 |

지원하는 developer-preview profile은 `context-core`와 `context-decision`을 별도로 설치한 뒤 `$context-decision:init`을 한 번 실행하는 구성입니다. bundle/meta-plugin은 없습니다. ASM과 TERM은 optional experimental surface이며 서로를 자동 설치하거나 대신 초기화하지 않습니다.

core와 semantic addon은 반드시 같은 immutable release checkout에서 함께 설치·update해야 합니다. 각 addon이 exact core entrypoint bytes를 고정하므로 혼합 설치나 일부만 update한 상태는 `core_surface_mismatch`로 중단됩니다. 이때 core와 해당 addon을 같은 release로 함께 다시 설치·update하고 host reload 뒤 재시도합니다.

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
기록할 가치가 있을 때만 complete preview 제안
    ↓
사용자가 자연어 capture 질문에 한 번 답변
    ↓
context/*.md와 index를 하나의 transaction으로 갱신
```

평범한 대화에는 별도 audit 메시지를 표시하지 않습니다. 관련 결정이나 근거가 판단을 바꿀 때만 필요한 문서를 읽고, 기록할 내용이 충분히 성숙했을 때만 제안합니다.

## 설치

아래 명령은 owner가 `v0.5.1` tag와 release commit push를 승인·완료한 뒤에만 사용할 수 있습니다. mutable branch가 아니라 exact tag를 사용합니다.

### Codex

```bash
codex plugin marketplace add Jeis-Jw/context-plugins --ref v0.5.1
codex plugin add context-core@context-plugins
codex plugin add context-decision@context-plugins
```

### Claude Code

```bash
git clone --branch v0.5.1 --depth 1 https://github.com/Jeis-Jw/context-plugins.git context-plugins-v0.5.1
claude plugin marketplace add /absolute/path/to/context-plugins-v0.5.1
claude plugin install context-core@context-plugins
claude plugin install context-decision@context-plugins
```

Claude Code 2.1.89에는 marketplace `--ref` option이 없어 exact tag local checkout을 먼저 만듭니다. ASM/TERM이 필요하면 같은 checkout에서 각각 설치하되 experimental surface로 취급합니다. 설치 scope와 활성화 범위는 host가 제공하는 수단 안에서 사용자가 직접 정해야 하며, 플러그인이 다른 플러그인을 자동 설치·활성화·update하거나 host 설정을 임의로 바꾸지 않습니다.

설치 후 host를 reload하거나 새 session을 여세요.

## 처음 한 번 초기화

지원 profile은 사용할 repository에서 `$context-decision:init`을 한 번만 실행합니다. 이 호출이 설치된 exact `context-core`를 확인한 뒤 core storage와 DEC area를 함께 준비하므로 `$context-core:init`을 먼저 실행할 필요가 없습니다. ASM/TERM을 experimental로 설치했다면 해당 addon init을 각각 한 번 실행합니다. 한 addon init이 다른 addon area를 자동 등록하지는 않습니다.

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
| scope의 현재 결정을 읽기용 명세로 보기 | “`project/auth`의 Current DEC를 spec view로 조립해줘.” |
| 중요한 근거 보존 | “이번 운영 결과를 재사용 가능한 observation 후보로 만들어줘.” |
| 미검증 전제 추적 | “외부 IdP 응답이 5초 이내라는 전제를 assumption 후보로 만들고 확인·반증 조건을 붙여줘.” |
| 프로젝트 용어 확인 | “이 프로젝트에서 BFF가 뜻하는 정의와 alias를 term context에서 확인해줘.” |
| 작업 인계 | “여기서 중단할 수 있게 현재 상태를 snapshot으로 정리해줘.” |
| 결정 변경 | “기존 결정을 유지할지 supersede할지 실제 취지까지 비교해줘.” |

플러그인은 관련 신호를 발견하면 먼저 기존 context를 비교하고, 답변을 마친 뒤 필요한 경우에만 grouped capture를 제안합니다. 제안이나 preview만으로는 파일이 바뀌지 않습니다.

## 무엇이 저장되나요?

```text
context/
  context.index.md
  decision/       # DEC: 현재 따를 결정과 superseded history
  assumption/     # ASM: 아직 검증되지 않은 project-scoped 전제
  term/           # TERM: 프로젝트 전용 용어와 canonical definition
  observation/    # OBS: 판단을 뒷받침하는 비권위 근거와 발견
  snapshot/       # SNAP: 다음 session을 위한 작업 인계
```

| 종류 | 의미 | 권위 |
|---|---|---|
| `DEC` | 무엇을 선택했고 왜 따르는지, 무엇을 반려했는지 | Current 문서는 authoritative |
| `ASM` | 아직 검증되지 않았지만 후속 판단을 바꿀 수 있는 전제 | Current 문서는 provisional |
| `TERM` | 프로젝트 안에서 사용할 용어와 canonical definition | Current 문서는 authoritative |
| `OBS` | 재사용할 사실, 증거, 시행착오 | 판단을 돕는 evidence |
| `SNAP` | 미완료 작업의 현재 상태와 다음 행동 | 재개용 staging |

모든 artifact는 Markdown이라 일반 Git diff, review, branch와 rollback을 그대로 사용할 수 있습니다. 별도 database, vector store, SaaS 계정이나 Obsidian이 필요하지 않습니다.

## 안전 경계

- 일반 context 기록은 완성된 렌더링 본문을 보여준 capture 질문에 사용자가 직접적·명시적·무조건적으로 긍정한 뒤에만 적용합니다. `알겠어` 단독, 조건, 수정 요청, 화제 전환은 승인이 아니며 모호한 평가는 한 줄로 한 번만 재확인합니다.
- Agent가 내부 transport 정보를 처리하므로 사용자는 digest, 임시 파일 위치, 내부 ID나 core 경로를 보거나 입력하지 않습니다.
- Workflow는 질문 전에 complete preview를 고정하고 승인 뒤 재생성하지 않습니다. Repository identity, pinned runtime, CAS, lock, atomic-write 결박은 그대로이며 tampering과 clone·linked-worktree·same-path replay는 write 전에 실패합니다.
- DEC·ASM·TERM은 release-pinned core runtime에서 schema, `context-common/v2` protocol, required features·commands와 doctor state를 handshake합니다. 이 검증은 marketplace provenance, catalog source 또는 host enabled state를 attest하지 않으며 low-level compatibility surface는 외부 orchestration용으로 유지됩니다.
- hash, ID나 index metadata만으로 의미가 같다고 판단하지 않고 실제 body, scope와 rationale를 비교합니다.
- metadata와 index로 후보를 먼저 좁힌 뒤 관련 있는 실제 문서만 읽습니다. Healthy index의 zero-match는 indexed body를 열지 않고, stale/missing index recovery의 body open은 호출당 합계 20개 이하입니다.
- Hard bound는 artifact body materialization/open, selected output, candidate/envelope와 owner input에 적용됩니다. Index row scoring·directory enumeration과 end-to-end host/model token 사용량은 corpus 크기와 무관한 O(1)을 보장하지 않습니다.
- common primary-claim protocol 상한은 2,000 codepoint입니다. Built-in SNAP `current_context`, OBS `observation`, DEC `decision`은 각각 owner-specific 1,200 codepoint 상한을 적용합니다.
- background daemon처럼 대화를 수집하거나 transcript 전체를 자동 보관하지 않습니다.
- 명시적 `init` 외에는 plugin 설치·활성화와 host configuration을 자동으로 변경하지 않습니다.
- release-pinned core runtime, schema·protocol·required features/commands 또는 operation별 doctor state가 요구 조건과 다르면 target write는 0입니다. 이 검증은 marketplace provenance, catalog source 또는 host enabled state를 attest하지 않습니다.
- 기존 `wiki/`나 과거 distribution의 context를 자동 migration하지 않습니다.

## 검증 근거

| 근거 | 결과 | 경계 |
|---|---|---|
| Python 3.11 전체 suite, 2026-08-23 | 257 passed, 191 subtests | `python3.11 -m pytest -q` |
| Python 3.13 전체 suite, 2026-08-23 | 257 passed, 191 subtests | `python3.13 -m pytest -q` |
| 두 interpreter의 Phase 0 | 각각 15 passed | `PYTHONPATH=tests/context-v1/phase0 pythonX -m pytest -q tests/context-v1/phase0` |
| Codex `0.149.0-alpha.4.1` | core+decision fresh install/cache lifecycle 통과 | actual model behavior 근거 아님 |
| Claude Code `2.1.89` | core+decision fresh install/cache lifecycle 통과 | runtime UX는 experimental |
| 두 host의 네 plugin | install/load 통과 | ASM/TERM은 optional experimental |
| actual model/no-signal/token usage | 미확인 | end-to-end 측정 없음 |

Codex prompt material은 3,147자에서 1,331자로 57.7% 감소했습니다. 문자 수 측정이며 token 절감률 주장이 아닙니다.

## 현재 배포 상태

| 항목 | 상태 |
|---|---|
| GitHub repository | [`Jeis-Jw/context-plugins`](https://github.com/Jeis-Jw/context-plugins) repository는 public이지만 local `0.5.1` release commit은 아직 push하지 않음 |
| 준비 중인 version | `0.5.1` — 네 plugin manifest·두 local catalog·runtime/tests/docs parity |
| immutable ref | `v0.5.1` 계획 — tag 미생성·미push, owner 승인 필요 |
| Marketplace identity | `context-plugins` |
| Storage protocol | `context-common/v2` |
| Codex·Claude Code manifests | local release unit에 포함, publication evidence 아님 |
| Fresh host lifecycle | Codex `0.149.0-alpha.4.1`, Claude Code `2.1.89` core+decision 통과 |
| actual model/no-signal/token usage | 미확인 |
| 중앙 marketplace catalog 배포 | 아직 미완료 |
| 공개 라이선스 | 아직 미선택 — `LICENSE` 추가 전에는 사용·복제·재배포 권한이 자동 부여되지 않음 |

기존 `context-core@jeis-ai-plugins`는 별도 distribution입니다. 새 `context-core@context-plugins` 설치로 자동 전환되지 않으며, storage 이동도 자동 수행하지 않습니다. 자세한 경계는 [MIGRATION.md](./MIGRATION.md)를 참고하세요.

## 더 알아보기

- [`context-core` 상세 동작](./plugins/context-core/README.md)
- [`context-decision` 상세 동작과 오류 안내](./plugins/context-decision/README.md)
- [`context-assumption` 전제와 lifecycle 계약](./plugins/context-assumption/README.md)
- [`context-term` 용어 정본과 recall 계약](./plugins/context-term/README.md)
- [기존 distribution에서의 migration 경계](./MIGRATION.md)
- [English default](./README.md)

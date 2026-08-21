---
schema: "context-decision/v1"
id: "ctx_567991c7695749f38370073f3ea75276"
title: "새 distribution은 수동 설치·명시적 init·비자동 migration 경계를 지킨다"
summary: "context-plugins 좌표로 분리하되 기존 설치와 corpus를 자동 전환하지 않고 init만 repository-local fixed bootstrap을 수행한다."
created_at: "2026-08-21T10:38:08+09:00"
captured_from: "import"
source_refs: ["git:Jeis-Jw/ai-plugins@77345fb26d32296198393bedf12e92d9306754d3:wiki/task/done/TASK-2026-08-20-183806-context-플러그인을-context-manager-프로젝트로-분리한다.md","git:Jeis-Jw/ai-plugins@77345fb26d32296198393bedf12e92d9306754d3:wiki/ssot/context-core-plugin.md","git:Jeis-Jw/ai-plugins@77345fb26d32296198393bedf12e92d9306754d3:wiki/ssot/context-decision-plugin.md","file:MIGRATION.md","file:README.md"]
tags: ["distribution","init","dependency","migration","context-common-v2"]
search_terms: ["context-core@context-plugins","manual install","explicit init","non-automatic migration"]
scope: "context-plugins"
decision_key: "distribution-init-boundary"
revisit_when: ["Codex와 Claude Code가 동일한 dependency·scope·동의·rollback 계약을 공식 지원하면 opt-in native dependency를 재검토한다.","새 좌표의 live install과 rollback이 검증된 뒤 distribution publication 상태를 별도 OBS로 갱신한다."]
---

## 결정

distribution을 `context-core@context-plugins`, source `Jeis-Jw/context-plugins`, protocol `context-common/v2`로 둔다. 사용자가 exact core를 직접 설치·활성화하고 addon은 host 설치를 자동화하지 않는다. 명시적 init은 storage·area·managed policy를 멱등 bootstrap한다. 기존 `jeis-ai-plugins` 설치와 원본 corpus는 자동 전환하지 않고 actual-body review와 새 exact approval을 거친다.

## 취지

host 환경과 설치 scope 변경은 사용자 권한으로 남기면서, 이미 명시한 repository init 의사는 반복 승인 없이 안전한 fixed bootstrap으로 완결한다. distribution 이동과 data migration을 분리해야 기존 설치를 새 source 활성화 증거로 오판하지 않는다.

## 반려대안

- context-decision이 core를 자동 설치·활성화하는 방식은 사용자 환경과 scope를 임의 변경해 반려한다.
- 기존 marketplace 좌표를 새 source와 동일하게 취급하는 방식은 distribution provenance를 흐려 반려한다.
- 원본 wiki/context corpus를 clean import에 함께 복사하는 방식은 obsolete·무관한 맥락을 authoritative current로 만들 수 있어 반려한다.
- init을 preview-only로 유지해 core와 addon init을 반복 호출하는 방식은 명시적 초기화 의사 뒤의 불필요한 UX 비용 때문에 반려한다.

## 트레이드오프

- 신규 사용자는 exact provider 설치와 host reload를 직접 수행해야 하고 기존 사용자에게 자동 upgrade가 없다.
- remote·publication·live install·rollback·license는 repository-local 검증과 별도 release gate로 남는다.

## 재평가 조건

- Codex와 Claude Code가 동일한 dependency·scope·동의·rollback 계약을 공식 지원하면 opt-in native dependency를 재검토한다.
- 새 좌표의 live install과 rollback이 검증된 뒤 distribution publication 상태를 별도 OBS로 갱신한다.

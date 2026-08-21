---
schema: "context-observation/v1"
id: "ctx_83cab48295974fada0cffdb89907c28f"
title: "Context v1 local 검증은 강하지만 live 운영 증거는 제한적이다"
summary: "v1 acceptance와 split 검증은 통과했으나 새 0.4.0 좌표의 실제 배포·설치와 장기 corpus 품질은 아직 확인되지 않았다."
created_at: "2026-08-21T10:38:09+09:00"
captured_from: "import"
source_refs: ["git:Jeis-Jw/ai-plugins@77345fb26d32296198393bedf12e92d9306754d3:wiki/task/done/TASK-2026-08-14-010606-context-core와-context-decision-v1-구현.md","git:Jeis-Jw/ai-plugins@77345fb26d32296198393bedf12e92d9306754d3:wiki/task/done/TASK-2026-08-20-183806-context-플러그인을-context-manager-프로젝트로-분리한다.md","git:Jeis-Jw/ai-plugins@77345fb26d32296198393bedf12e92d9306754d3:wiki/ssot/context-core-plugin.md","file:README.md"]
tags: ["validation","operational-gap","context-v1","context-plugins-0.4.0"]
search_terms: ["43/43","152 passed","98 subtests","live operational evidence"]
---

## 관찰

`ai-plugins`의 v1 구현은 acceptance 43/43, supplemental QA 16/16, 193 test invocation과 독립 review approval을 기록했고, 분리된 `context-plugins@69c0544`는 152 passed·98 subtests와 compile/JSON/review를 통과했다. 그러나 새 `context-core@context-plugins` 0.4.0은 remote·marketplace publication·live install이 없고, Claude Code·Linux 및 실제 장기 corpus의 recall precision과 capture fatigue는 미확인이다.

## 근거

- v1 완료 TASK는 local macOS fixture·static contract 범위의 43/43 acceptance와 193 invocation을 기록하고 live host·Linux를 미검증으로 남긴다.
- split TASK와 현재 README는 child 검증 수치와 동시에 remote·publication·새 좌표 live install 미수행을 명시한다.
- historical SSOT는 synthetic Stage 1 I/O와 deterministic suite 통과를 실제 장기 대화의 semantic 품질과 구분한다.

## 영향

현재 product/contract 구현을 신뢰할 근거는 충분하지만 deployment readiness와 운영 품질을 완료로 주장할 수 없다.

## 현재 처리

변경 검증에는 focused suite와 contract parity를 사용하고, release 단계에서는 새 좌표의 실제 install·reload·temporary consumer init·recall/capture·rollback을 별도로 실행한다.

## 후속 조건

- public remote와 catalog가 준비되면 exact remote SHA와 두 host manifest parity를 검증한다.
- Codex·Claude Code·macOS·Linux consumer에서 representative flow와 장기 corpus recall 품질을 계측한다.

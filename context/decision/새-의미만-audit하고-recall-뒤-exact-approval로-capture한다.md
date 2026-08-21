---
schema: "context-decision/v1"
id: "ctx_5a4c57e13aa84422b99544854ce35167"
title: "새 의미만 audit하고 recall 뒤 exact approval로 capture한다"
summary: "매 turn의 증분 신호를 한 번 audit하되 필요한 본문만 recall하고 성숙한 후보를 complete preview와 exact digest로 승인받는다."
created_at: "2026-08-21T10:38:07+09:00"
captured_from: "import"
source_refs: ["git:Jeis-Jw/ai-plugins@e25ab55eb6982bd474fe67f3918dc24d304923e4:wiki/context/decision/DEC-2026-08-13-180535-capture-audit는-milestone-단위-단일-판독과-승인형-write를-지킨다.md","git:Jeis-Jw/ai-plugins@e25ab55eb6982bd474fe67f3918dc24d304923e4:wiki/context/decision/DEC-2026-08-13-183612-컨텍스트-플러그인은-milestone-capture-audit와-semantic-owner-draft로-결합한다.md","git:Jeis-Jw/ai-plugins@77345fb26d32296198393bedf12e92d9306754d3:wiki/context/decision/DEC-2026-08-13-152825-capture-정책은-초기화-시-auto-loaded-agent-entry에-설치한다.md","git:Jeis-Jw/ai-plugins@77345fb26d32296198393bedf12e92d9306754d3:wiki/context/decision/DEC-2026-06-02-120100-task-github-작업-종료-전-knowledge-capture-audit-의무화.md","file:plugins/context-core/rules/context-policy.md"]
tags: ["incremental-audit","recall-before-capture","grouped-preview","approval-digest"]
search_terms: ["same response pass","durable signal","exact final bundle","dismissed candidate"]
scope: "context-plugins"
decision_key: "recall-capture-approval-workflow"
revisit_when: ["host의 안전한 semantic event surface가 누락률을 개선한다는 측정이 나오면 trigger를 재평가한다."]
---

## 결정

매 user turn의 새 의미만 같은 응답 pass에서 한 번 audit한다. durable signal이 없으면 tool call·상태 표시·capture 질문을 만들지 않는다. 신호가 있으면 metadata-first로 후보를 좁혀 선택된 실제 본문만 비교한다. primary 요청 뒤 성숙한 후보만 milestone당 한 번 complete preview로 제안하고, artifact와 index는 exact final bundle 승인 뒤에만 쓴다.

## 취지

audit을 생략하면 결정이 휘발되지만 hook·강제 recall·owner별 재판독은 UX와 token 비용을 해친다. 증분 audit, signal-gated recall, complete preview를 결합하면 누락 방지와 승인 bytes의 일치를 함께 지킬 수 있다.

## 반려대안

- 항상 audit 상태를 출력하거나 hook으로 capture를 강제하는 방식은 본 답변과 UX를 해쳐 반려한다.
- 각 owner가 transcript를 다시 읽는 방식은 addon 수만큼 비용과 중복 판단이 늘어 반려한다.
- 제목만 승인받거나 한 승인을 후속 wave까지 확장하는 방식은 exact bundle 경계를 깨므로 반려한다.

## 트레이드오프

- agent policy 기반 audit는 hard runtime guarantee가 아니며 signal 판정 품질을 실제 대화에서 관찰해야 한다.
- complete preview는 제목 목록보다 길지만 의미와 lifecycle을 승인 전에 확정한다.

## 재평가 조건

- host의 안전한 semantic event surface가 누락률을 개선한다는 측정이 나오면 trigger를 재평가한다.

---
schema: "context-decision/v1"
id: "ctx_b04697421a224894ba51d69a92dd9521"
title: "Context Plugins는 Git 기반 승인형 durable project context에 집중한다"
summary: "대화 전체가 아니라 판단을 바꾸는 프로젝트 맥락·근거·결정 연속성을 local Git/Markdown에 보존한다."
created_at: "2026-08-21T10:38:06+09:00"
captured_from: "import"
source_refs: ["git:Jeis-Jw/ai-plugins@77345fb26d32296198393bedf12e92d9306754d3:wiki/ssot/context-core-plugin.md","git:Jeis-Jw/ai-plugins@77345fb26d32296198393bedf12e92d9306754d3:wiki/ssot/context-decision-plugin.md","git:Jeis-Jw/ai-plugins@77345fb26d32296198393bedf12e92d9306754d3:wiki/task/done/TASK-2026-08-20-183806-context-플러그인을-context-manager-프로젝트로-분리한다.md","file:README.md"]
tags: ["product-boundary","durable-context","git","approval"]
search_terms: ["project context","decision continuity","PCMS boundary"]
scope: "context-plugins"
decision_key: "product-boundary"
revisit_when: ["실사용자가 반복적으로 조직 단위 기능을 요구하고 PCMS 연동 경계가 확정되면 integration surface를 재평가한다.","local index가 실제 corpus 규모에서 병목이 된다는 측정이 나오면 파생 cache나 검색 확장을 검토한다."]
---

## 결정

Context Plugins는 coding agent를 위한 Git/Markdown 기반의 가볍고 승인형인 durable project context에 집중한다. repository의 why·현재 상태·재사용 가능한 근거·결정 연속성·provenance·freshness를 보존하며, 범용 transcript archive·vector memory·SaaS sync·조직 권한 제품으로 확장하지 않는다. 조직 권한·승인 queue·cross-project search·정책·감사는 별도 PCMS control plane의 책임이다.

## 취지

host 내장 memory와 구별되는 가치는 모든 대화를 저장하는 데 있지 않고, Git으로 공유·검토할 수 있는 승인된 맥락과 stale decision 경고에 있다. local-first 경계는 비용과 운영 부담을 낮추고 공개 plugin의 초기 가치를 선명하게 한다.

## 반려대안

- 범용 대화 memory와 transcript archive는 차별성이 낮고 민감정보·비용·검색 잡음을 키워 반려한다.
- 초기 제품에 vector search와 SaaS sync를 포함하는 방식은 검증 전 인프라와 운영 부담을 키워 반려한다.
- 조직 권한과 audit control plane까지 plugin에 넣는 방식은 PCMS 책임과 충돌하므로 반려한다.

## 트레이드오프

- cross-project·조직 단위 검색과 승인 queue는 local plugin만으로 제공하지 않는다.
- 관련성이 높은 맥락만 선택적으로 회수하므로 recall precision과 누락률을 실제 사용에서 계속 관찰해야 한다.

## 재평가 조건

- 실사용자가 반복적으로 조직 단위 기능을 요구하고 PCMS 연동 경계가 확정되면 integration surface를 재평가한다.
- local index가 실제 corpus 규모에서 병목이 된다는 측정이 나오면 파생 cache나 검색 확장을 검토한다.

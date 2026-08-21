---
schema: "context-decision/v1"
id: "ctx_ec6fcfa9fba64f7eb42fd83ba2593500"
title: "단일 audit와 semantic owner를 sole-writer coordinator로 결합한다"
summary: "core가 증분 audit·routing·grouped approval·physical write를 소유하고 owner는 실제 의미와 완성된 draft·lifecycle plan을 소유한다."
created_at: "2026-08-21T10:38:06+09:00"
captured_from: "import"
source_refs: ["git:Jeis-Jw/ai-plugins@e25ab55eb6982bd474fe67f3918dc24d304923e4:wiki/context/decision/DEC-2026-08-13-183612-컨텍스트-플러그인은-milestone-capture-audit와-semantic-owner-draft로-결합한다.md","git:Jeis-Jw/ai-plugins@e25ab55eb6982bd474fe67f3918dc24d304923e4:wiki/context/decision/DEC-2026-08-13-180535-capture-audit는-milestone-단위-단일-판독과-승인형-write를-지킨다.md","git:Jeis-Jw/ai-plugins@77345fb26d32296198393bedf12e92d9306754d3:wiki/ssot/context-core-plugin.md","git:Jeis-Jw/ai-plugins@77345fb26d32296198393bedf12e92d9306754d3:wiki/ssot/context-decision-plugin.md"]
tags: ["context-core","context-decision","semantic-owner","approval"]
search_terms: ["one auditor","complete draft","sole writer","grouped preview"]
scope: "context-plugins"
decision_key: "owner-coordinator-boundary"
revisit_when: ["전문 owner 간 claim 충돌이 반복되거나 grouped preview가 사용자 판단 비용을 줄이지 못하면 routing과 batch 표현을 재설계한다."]
---

## 결정

`context-core`가 각 대화 delta의 단일 audit, SNAP·OBS, capability routing, grouped complete preview와 유일한 physical write를 소유한다. semantic owner는 bounded candidate의 actual body·scope·rationale를 판정해 완성된 draft와 lifecycle plan을 만든다. addon은 대화를 다시 audit하거나 직접 쓰지 않고 같은 claim을 중복 기록하지 않는다.

## 취지

발견·의미 검증·승인·physical write를 분리해야 addon 수만큼 대화를 재판독하는 비용과 중복 제안을 막고, 사용자가 본 내용과 실제 저장되는 내용이 달라지는 것을 방지할 수 있다.

## 반려대안

- 각 addon이 대화를 독립 audit하는 방식은 토큰 낭비·중복 제안·분류 충돌을 만들어 반려한다.
- owner가 승인 뒤 본문을 완성하거나 직접 파일을 쓰는 방식은 승인 범위와 원자적 lifecycle을 깨므로 반려한다.
- core가 모든 domain schema의 의미를 해석하는 방식은 core를 비대하게 만들어 반려한다.

## 트레이드오프

- core가 공통 audit와 physical write의 논리적 단일 의존점이 된다.
- 두 번째 semantic owner가 추가될 때 capability envelope과 owner 간 claim 우선순위를 실제 사례로 검증해야 한다.

## 재평가 조건

- 전문 owner 간 claim 충돌이 반복되거나 grouped preview가 사용자 판단 비용을 줄이지 못하면 routing과 batch 표현을 재설계한다.

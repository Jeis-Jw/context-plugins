---
schema: "context-decision/v1"
id: "ctx_b51a14bf6ba340eab63104aeffd67221"
title: "SNAP·OBS·DEC는 authority에 맞는 독립 lifecycle을 갖는다"
summary: "SNAP은 재개 staging, OBS는 비권위 evidence, DEC는 authoritative choice이며 동일 claim 인수 때만 supersede한다."
created_at: "2026-08-21T10:38:07+09:00"
captured_from: "import"
source_refs: ["git:Jeis-Jw/ai-plugins@e25ab55eb6982bd474fe67f3918dc24d304923e4:wiki/context/decision/DEC-2026-08-13-180257-snap-obs-dec는-각-의미에-맞는-독립-lifecycle을-갖는다.md","git:Jeis-Jw/ai-plugins@77345fb26d32296198393bedf12e92d9306754d3:wiki/ssot/context-core-plugin.md","git:Jeis-Jw/ai-plugins@77345fb26d32296198393bedf12e92d9306754d3:wiki/ssot/context-decision-plugin.md"]
tags: ["snapshot","observation","decision","lifecycle","authority"]
search_terms: ["SNAP staging","OBS evidence","DEC authoritative","supersede"]
scope: "context-plugins"
decision_key: "artifact-authority-lifecycle"
revisit_when: ["여러 semantic owner가 실제로 동일한 lifecycle 의미를 반복하면 공통 primitive 추출을 검토한다.","Git 없는 저장 환경에서 snapshot 이력 요구가 반복되면 SNAP 보존 방식을 재평가한다."]
---

## 결정

SNAP은 unfinished session의 비권위 staging으로 갱신 후 discard한다. OBS는 재사용 가능한 비권위 evidence이고 DEC는 결정·취지·반려대안을 담는 authoritative choice다. OBS와 DEC의 claim은 제자리에서 바꾸지 않고 같은 claim의 successor가 인수할 때만 supersede한다. successor 없는 무효는 OBS invalidate·DEC withdraw, 오래됨은 freshness warning으로 다룬다.

## 취지

임시 handoff·발견 근거·따라야 할 선택의 권위 차이를 보존하면서 자동 승격과 불필요한 공통 상태 모델을 피한다.

## 반려대안

- 모든 artifact에 current·archived·promoted 상태를 공통 적용하는 방식은 서로 다른 의미를 억지로 통합해 반려한다.
- DEC 생성 시 관련 OBS를 자동 retire하는 방식은 evidence와 choice를 혼동하므로 반려한다.
- 오래됐다는 이유만으로 retire하는 방식은 반증과 freshness를 혼동해 반려한다.

## 트레이드오프

- artifact별 retire reason과 validation이 필요하지만 recall에서 authority와 현재성을 정확히 표현할 수 있다.

## 재평가 조건

- 여러 semantic owner가 실제로 동일한 lifecycle 의미를 반복하면 공통 primitive 추출을 검토한다.
- Git 없는 저장 환경에서 snapshot 이력 요구가 반복되면 SNAP 보존 방식을 재평가한다.

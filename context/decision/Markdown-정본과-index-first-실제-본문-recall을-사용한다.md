---
schema: "context-decision/v1"
id: "ctx_be32d7801f0c465c9ef41a16b3f2a08c"
title: "Markdown 정본과 index-first 실제 본문 recall을 사용한다"
summary: "artifact 본문이 의미 정본이고 index는 후보 discovery projection이며 관련 본문만 읽어 의미를 비교한다."
created_at: "2026-08-21T10:38:06+09:00"
captured_from: "import"
source_refs: ["git:Jeis-Jw/ai-plugins@e25ab55eb6982bd474fe67f3918dc24d304923e4:wiki/context/decision/DEC-2026-08-13-180256-컨텍스트-저장소는-semantic-index와-파일명-독립-id를-사용한다.md","git:Jeis-Jw/ai-plugins@77345fb26d32296198393bedf12e92d9306754d3:wiki/ssot/context-core-plugin.md","git:Jeis-Jw/ai-plugins@77345fb26d32296198393bedf12e92d9306754d3:wiki/ssot/context-decision-plugin.md"]
tags: ["storage","index-first","semantic-comparison","identity"]
search_terms: ["context.index.md","actual body","immutable id","metadata first"]
scope: "context-plugins"
decision_key: "storage-recall-boundary"
revisit_when: ["area index가 반복적인 merge 병목이 되거나 실제 corpus에서 recall 누락이 허용 수준을 넘으면 sharding이나 local derived cache를 검토한다."]
---

## 결정

Git worktree의 `context/` 아래 Markdown artifact를 의미 정본으로 두고 immutable internal ID를 filename과 분리한다. root·area index는 artifact에서 재생성되는 discovery projection이며 recall은 metadata로 후보를 좁힌 뒤 관련 실제 본문만 읽는다. 의미 동일성·conflict·rationale change는 hash·fingerprint·ID·index metadata가 아니라 actual body·scope·rationale로 판정한다.

## 취지

파일 rename 안전성, 사람이 검토 가능한 정본, token-efficient recall을 함께 확보하면서 검색 metadata가 semantic truth로 오용되는 것을 막는다.

## 반려대안

- basename을 정본 ID로 쓰는 방식은 rename과 영역별 파일명 공존을 제약해 반려한다.
- index를 정본으로 삼는 방식은 drift와 수동 편집 위험 때문에 반려한다.
- 모든 artifact 본문을 매번 읽는 방식은 corpus가 커질수록 I/O와 token 비용이 증가해 반려한다.
- fingerprint나 문장 유사도로 의미 동일성을 결정하는 방식은 취지와 scope 차이를 숨겨 반려한다.

## 트레이드오프

- index drift 검사와 fallback 경로가 필요하고 area index가 Git hot file이 될 수 있다.
- bounded recall의 false negative와 실제 corpus precision은 별도 운영 측정이 필요하다.

## 재평가 조건

- area index가 반복적인 merge 병목이 되거나 실제 corpus에서 recall 누락이 허용 수준을 넘으면 sharding이나 local derived cache를 검토한다.

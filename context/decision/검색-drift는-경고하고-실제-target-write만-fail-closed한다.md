---
schema: "context-decision/v1"
id: "ctx_ad8d936f6a5f4da0b493ce374a856e76"
title: "검색 drift는 경고하고 실제 target write만 fail-closed한다"
summary: "read·init은 warning과 bounded fallback을 우선하고 손실 가능한 대상 write의 CAS·path·lock·approval만 엄격히 차단한다."
created_at: "2026-08-21T10:38:08+09:00"
captured_from: "import"
source_refs: ["git:Jeis-Jw/ai-plugins@8ac8ffa355ae36783485b9339775fdf89aaa3a46:wiki/context/decision/DEC-2026-08-17-222516-context-무결성은-검색-경고와-대상-write-경계로-분리한다.md","git:Jeis-Jw/ai-plugins@77345fb26d32296198393bedf12e92d9306754d3:wiki/ssot/context-core-plugin.md","git:Jeis-Jw/ai-plugins@77345fb26d32296198393bedf12e92d9306754d3:wiki/ssot/context-decision-plugin.md"]
tags: ["integrity","fail-closed","index-fallback","approval-digest"]
search_terms: ["target write","CAS","schema_removed_field","refresh fix index"]
scope: "context-plugins"
decision_key: "integrity-write-boundary"
revisit_when: ["warning으로 강등한 drift가 실제 오선택이나 잘못된 lifecycle mutation을 유발한다는 재현 근거가 나오면 해당 조건만 다시 blocking으로 승격한다."]
---

## 결정

포맷 잔재와 파생 index drift는 read·init에서 warning과 bounded fallback으로 처리하고 user artifact를 자동 변경하지 않는다. derived index는 승인 없이 재생성할 수 있다. fail-closed는 target write의 protocol/source gate, artifact CAS, area index, duplicate ID, path·symlink, lifecycle, atomic replace, root lock과 exact approval digest에 한정한다.

## 취지

검색을 돕는 포맷과 파생 index가 무관한 artifact 작업 전체를 막으면 무결성 수단이 제품의 recall·continuity 목적을 역전한다. 반면 target write 경계는 실제 데이터 손실과 승인 우회를 직접 방지한다.

## 반려대안

- corpus 전체가 clean일 때만 모든 operation을 허용하는 방식은 무관한 drift가 제품 전체를 멈춰 반려한다.
- read나 init에서 legacy artifact를 자동 migration하는 방식은 승인 없는 본문 mutation이므로 반려한다.
- derived index rebuild에도 artifact approval을 요구하는 방식은 재생성 가능한 projection을 user record와 같은 권위로 취급해 반려한다.
- CAS·path guard·atomic replace·root lock·approval digest까지 완화하는 방식은 손실 방지 경계를 제거하므로 반려한다.

## 트레이드오프

- warning-only drift는 다음 승인 rewrite까지 남을 수 있고 fallback은 정상 index lookup보다 느리다.
- 무관한 오염을 한 mutation에서 함께 청소하지 않으므로 운영자는 warning을 별도로 추적해야 한다.

## 재평가 조건

- warning으로 강등한 drift가 실제 오선택이나 잘못된 lifecycle mutation을 유발한다는 재현 근거가 나오면 해당 조건만 다시 blocking으로 승격한다.

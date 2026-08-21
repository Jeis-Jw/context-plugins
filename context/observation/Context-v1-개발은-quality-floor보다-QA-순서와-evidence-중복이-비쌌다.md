---
schema: "context-observation/v1"
id: "ctx_35e64fcf2b184793a1b24433449e6b23"
title: "Context v1 개발은 quality floor보다 QA 순서와 evidence 중복이 비쌌다"
summary: "독립 review는 실제 blocker를 찾았지만 review 전 full QA와 계층별 receipt 복제가 214 command·18 lane을 만들었다."
created_at: "2026-08-21T10:38:10+09:00"
captured_from: "import"
source_refs: ["git:Jeis-Jw/ai-plugins@77345fb26d32296198393bedf12e92d9306754d3:wiki/context/trial_error/TRI-2026-08-14-111703-context-v1-studio-미션은-final-qa와-evidence-ceremony를-과도하게-반복했다.md","git:Jeis-Jw/ai-plugins@77345fb26d32296198393bedf12e92d9306754d3:wiki/task/TASK-2026-08-14-121445-studio-작업-경제성-개선.md"]
tags: ["workflow-economics","quality-floor","hard-review","evidence-reuse"]
search_terms: ["214 command receipts","18 lanes","final QA once","IntegrationReceipt"]
---

## 관찰

Context v1 Studio mission은 acceptance 43/43과 독립 review approval을 얻었지만 591.8분, 18 lane, 7 task-worker run과 214 command receipt를 사용했다. 독립 hard review가 실제 blocker 4건을 발견했으므로 quality floor는 유효했고, 낭비의 핵심은 review 전 final-grade QA, 늦은 executable-criteria audit, 동일 HEAD의 profile·receipt·evidence 반복이었다.

## 근거

- TRI는 214 command receipt, 18 lane, 7 run, 591.8분과 suite 반복 횟수를 원자료 기반으로 기록한다.
- hard review round 2가 production preflight 등 blocker 4건을 발견해 독립 검토의 실효성을 확인했다.
- token과 model-call telemetry는 unavailable이므로 비용이나 token ROI는 수치로 확정할 수 없다.

## 영향

다음 context plugin 변경에서 review와 품질 gate를 줄이는 것이 아니라 검증 순서·batching·evidence 참조 구조를 단순화해야 한다.

## 현재 처리

구현 전 executable acceptance를 확인하고 targeted red/green 뒤 독립 hard review, finding 수정, frozen candidate final QA 1회 순서를 기본으로 한다. 같은 HEAD의 관련 profile은 batch receipt와 digest로 재사용한다.

## 후속 조건

- 다음 큰 변경에서 command count·wall time·model call·token telemetry를 함께 수집해 개선 효과를 판정한다.
- evidence reuse가 shared-contract 변경의 stale 결과를 통과시키면 invalidation 경계를 강화한다.

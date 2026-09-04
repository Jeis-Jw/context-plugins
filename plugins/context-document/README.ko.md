# context-document (한국어)

[English](./README.md)

`context-document`는 판단자(에이전트·사람)가 recall/envelope로 소비하는 project-scoped 현행 상태 진술의 semantic owner입니다. DOCUMENT만 단독으로 쓸 수 있으며 DEC가 `affects:document`로 참조할 수 있지만 이 plugin은 Decision owner를 요구하거나 설치하지 않습니다. 외부 전달용 deliverable 문서는 범위 밖이며 repository가 소유합니다.

## Artifact 계약

- schema: `context-document/v1`
- authority: `authoritative`
- authoritative slot: `(scope, document_key)`
- 필수 H2: `Content`
- lifecycle: `capture`, `read`, `search`, `update`

`update`는 ID, path, scope, `document_key`를 유지한 채 Current artifact를 같은 state에서 교체합니다. document taxonomy, subtype, supersede flow와 backlink index는 의도적으로 제공하지 않습니다.

artifact 한도는 기본 읽기 예산입니다. 큰 지식은 한 slot을 키우지 말고 `design-skeleton`·`design-envelope`·`design-rules`처럼 stable chapter slot으로 분해합니다.

decision은 `affects:document`로 document를 참조할 수 있고 document 쪽 inverse edge는 저장하지 않습니다. `refresh`는 Current DEC가 document의 `updated_at`(최초 update 전에는 `created_at`)보다 새로우면 `document-stale-vs-decision` hygiene warning을 내고, DEC 이후 document를 update하면 warning을 없앱니다. Intent, decision, document는 각각 독립적으로 사용할 수 있습니다.

semantic CLI는 canonical area를 읽고 draft와 validation receipt만 만듭니다. path resolution, artifact/index write, approval bundle, lock, CAS와 apply는 `context-core`만 수행합니다. 일반 filesystem directory가 vault이며 Git repository는 필요하지 않습니다.

명시적 `$context-document:init`은 이미 사용할 수 있는 same-major `context-core`를 통해 이 owner만 등록합니다. 다른 plugin을 install·import·enable하지 않으며 `core-decision` profile에도 포함되지 않습니다.

릴리스 이력은 프로젝트 [CHANGELOG](../../CHANGELOG.md)를 참고하세요.

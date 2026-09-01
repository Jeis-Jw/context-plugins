# context-intent (한국어)

[English](./README.md)

`context-intent`는 프로젝트가 향하려는 방향의 semantic owner입니다. INTENT만 단독으로 쓸 수 있고 DEC에 INTENT가 필수는 아닙니다. 둘을 함께 쓰면 decision이 `serves:intent`로 intent를 참조할 수 있습니다.

## Artifact 계약

- schema: `context-intent/v1`
- authority: `authoritative`
- authoritative slot: `(scope, intent_key)`
- 필수 H2: `Intent`
- 선택 H2: `Success criteria`, `Constraints`, `Revisit conditions`
- lifecycle: `capture`, `read`, `search`, `supersede`

`Intent`는 desired direction입니다. OBS와 ASM은 evidence 또는 premise, DEC는 chosen commitment이며, DEC의 `Rationale`은 그 근거에서 해당 결정을 택한 이유와 그 결정이 Intent를 섬기는 이유를 설명합니다. 각 owner는 독립적으로 사용할 수 있습니다.

`supersede`는 slot을 유지하면서 predecessor를 History로 옮기고 새 ID의 successor를 만들며 reciprocal `superseded_by` / `supersedes`를 기록합니다. 실제 두 `Intent` 본문을 인용한 attestation이 필요하고 ID, hash, index metadata는 의미 동일성의 근거가 아닙니다.

semantic CLI는 canonical area를 읽고 draft와 validation receipt만 만듭니다. path resolution, artifact/index write, approval bundle, lock, CAS와 apply는 `context-core`만 수행합니다. 일반 filesystem directory가 vault이며 Git repository는 필요하지 않습니다.

명시적 `$context-intent:init`은 이미 사용할 수 있는 same-major `context-core`를 통해 이 owner만 등록합니다. `context-decision`이나 `context-document`를 install·import·enable하지 않으며 `core-decision` profile에도 포함되지 않습니다.

`0.10.0`은 developer preview이며 tag나 marketplace publication을 의미하지 않습니다.

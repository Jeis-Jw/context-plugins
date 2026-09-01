---
name: archive
description: durable context의 근거로 채택한 불변 장문 원본을 보존합니다.
---

# Context archive

ARCHIVE는 context-core가 소유하는 `context-archive/v1` evidence입니다.

- durable context record의 근거로 채택한 불변 source original만 capture합니다. deliverable 저장소가 아니며 OBS·DEC·INTENT·DOCUMENT를 대신하지 않습니다.
- substantive `Content`, 하나 이상의 `source_ref`, source가 evidence로 채택됐고 불변 원본이 존재한다는 명시적 attestation을 요구합니다.
- `archive preview --content @file ...`로 전체 rendered body를 보여준 뒤, 그 preview를 명시적으로 승인한 경우에만 receipt와 approval digest를 바꾸지 않고 apply합니다.
- lifecycle은 capture·read·search·discard뿐이며 update·rename·retire·supersede는 없습니다.
- 기본 recall·pack에서는 제외합니다. 원본이 실제로 필요할 때만 `archive read|search` 또는 `recall --include-archive`를 사용합니다.
- OBS `Evidence` 항목은 exact ARCHIVE `ctx_` ID가 될 수 있습니다. 자유 문자열도 허용하며 exact ID는 context-core refresh가 검사합니다.
- inbound internal reference가 있는 archive는 discard하지 않습니다.

사용자-facing 문장은 context-core의 active language contract를 따르고 machine field는 English로 유지합니다. digest, receipt path, internal ID와 core path는 사용자에게 노출하거나 입력받지 않습니다.

[context-protocol.ko.md](../context/references/context-protocol.ko.md)를 참고합니다.

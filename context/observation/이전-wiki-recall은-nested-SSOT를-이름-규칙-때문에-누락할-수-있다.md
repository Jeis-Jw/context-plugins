---
schema: "context-observation/v1"
id: "ctx_bc423871d3df44cbaba86edf74fec7a3"
title: "이전 wiki recall은 nested SSOT를 이름 규칙 때문에 누락할 수 있다"
summary: "folder basename과 document basename이 같으면 legacy wiki_cli가 authored SSOT를 index로 오분류해 recall에서 제외한다."
created_at: "2026-08-21T10:38:09+09:00"
captured_from: "import"
source_refs: ["git:Jeis-Jw/ai-plugins@77345fb26d32296198393bedf12e92d9306754d3:wiki/context/observation/OBS-2026-08-04-223335-plugin-definition-ssot는-폴더-인덱스명과-basename이-겹쳐-wiki-cli-대부분의-조회에서-배제된다.md"]
tags: ["migration","wiki-cli","recall-gap","nested-ssot"]
search_terms: ["basename collision","read_missing","source inventory coverage"]
---

## 관찰

legacy `wiki_cli.py`는 nested 폴더명과 Markdown basename이 같을 때 실제 authored SSOT를 파생 index로 오분류할 수 있다. `plugin-definition/plugin-definition.md`에서 read·recall·relation·refresh 대상이 빠지는 현상이 재현됐으며, context plugin 정의 corpus도 같은 nested 형태를 사용하므로 migration inventory는 wiki recall 결과만 신뢰하면 안 된다.

## 근거

- source OBS는 `_is_index_file`의 basename 비교와 `recall --read plugin-definition`의 read_missing 재현을 기록한다.
- 이번 audit에서 nested context-plugin-definition 문서는 direct path로 읽고 source SHA inventory에 포함했다.

## 영향

legacy wiki 기반 migration은 정상 조회 결과가 0이어도 실제 문서 부재를 뜻하지 않으며, 중요한 SSOT를 누락한 incomplete context를 만들 수 있다.

## 현재 처리

legacy corpus를 이관할 때 metadata recall 뒤 파일 inventory와 relation closure를 대조하고, nested basename collision은 direct path actual-body read로 보완한다.

## 후속 조건

- legacy wiki resolver가 구조 신호로 index를 구분하도록 수정되면 재검증한다.
- 향후 importer에는 inventory count와 source digest coverage gate를 포함한다.

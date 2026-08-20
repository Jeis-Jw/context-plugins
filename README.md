# Context Plugins

Git/Markdown 기반 durable project context를 coding agent가 안전하게 회수하고, 실제 본문 비교와 사용자 승인 뒤에만 기록하도록 만드는 공개 예정 plugin repository입니다.

이 저장소는 `context-manager` 프로젝트의 plugin 구성요소이며 두 플러그인을 함께 소유합니다.

| 플러그인 | 역할 |
|---|---|
| `context-core` | `context/` 저장·index-first recall·SNAP·OBS·candidate routing·approval bundle과 유일한 physical write coordinator |
| `context-decision` | DEC의 결정·취지·반려대안, scope, actual-body comparison, conflict, supersede와 revisit를 소유하는 semantic owner |

향후 새로운 artifact 의미가 충분히 독립적일 때 semantic owner 플러그인을 추가할 수 있습니다. core는 addon의 domain schema를 내장하지 않습니다.

## Distribution identity

- Marketplace: `context-plugins`
- Core selector: `context-core@context-plugins`
- Planned source: `Jeis-Jw/context-plugins`
- Protocol: `context-common/v2`
- Current repository version: `0.4.0`

이 좌표는 아직 외부에 publish되거나 live install로 검증되지 않았습니다. 현재 설치된 기존 좌표 `context-core@jeis-ai-plugins`는 별도 distribution이며 새 source의 활성화를 증명하지 않습니다.

## Repository layout

```text
plugins/
  context-core/
  context-decision/
tests/context-v1/
.claude-plugin/marketplace.json
.agents/plugins/marketplace.json
context/
```

제품·runtime 계약의 공개 정본은 이 README, 각 plugin README와 `skills/**/references/*.md`입니다. 이 저장소에는 `wiki/` 레이어를 만들지 않습니다. 저장소 자체의 durable project context는 dogfood `context/`를 사용합니다.

## Development

요구사항은 Python 3.11+, Git과 Python standard library입니다. 테스트 실행에는 `pytest`가 필요합니다.

```bash
python3 -m pytest -q
python3 -m unittest discover -s plugins/context-core/tests -p 'test_*.py'
python3 -m unittest discover -s plugins/context-decision/tests -p 'test_*.py'
python3 -m unittest discover -s tests/context-v1 -p 'test_*.py'
python3 -m unittest discover -s tests/context-v1/phase0 -p 'test_*.py'
```

배포 전에는 두 host marketplace의 version/source parity, old coordinate 잔존 여부, actual CLI schema/capabilities와 temporary consumer init을 별도로 검증해야 합니다.

## Provenance

최초 source import는 `Jeis-Jw/ai-plugins@eea43c9386735aa6141203a8a8912b0256746a64`에서 수행했습니다. 무관한 monorepo history를 공개 저장소에 포함하지 않기 위해 clean import commit을 사용하며 상세 범위는 [MIGRATION.md](./MIGRATION.md)에 기록합니다.

## License

공개 라이선스는 아직 선택하지 않았습니다. 저장소가 public이 되더라도 `LICENSE`가 추가되기 전에는 사용·복제·재배포 권한이 자동으로 부여되지 않습니다.

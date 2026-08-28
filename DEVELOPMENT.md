# Context Plugins 개발 가이드

이 문서는 repository maintainer와 contributor를 위한 개발·검증 정보입니다. 플러그인 사용법은 [README.md](./README.md)를 참고하세요.

## Repository layout

```text
plugins/
  context-core/
  context-decision/
  context-assumption/
  context-term/
tests/context-v1/
.claude-plugin/marketplace.json
.agents/plugins/marketplace.json
context/
```

제품·runtime 계약의 공개 정본은 root README, 각 plugin README와 `skills/**/references/*.md`입니다. 이 저장소에는 `wiki/` 레이어를 만들지 않으며, 저장소 자체의 durable project context는 dogfood `context/`를 사용합니다.

## Development

요구사항은 Python 3.11+, Git과 Python standard library입니다. 테스트 실행에는 `pytest`가 필요합니다.

```bash
python3 -m pytest -q
python3 -m pytest -q plugins/context-core/tests
python3 -m pytest -q plugins/context-decision/tests
python3 -m pytest -q plugins/context-assumption/tests
python3 -m pytest -q plugins/context-term/tests
python3 -m pytest -q tests/context-v1/test_distribution_proof.py tests/context-v1/test_cross_plugin_flow.py
python3 -m pytest -q tests/context-v1/test_profile_installer.py
python3 -m pytest -q tests/context-v1/test_semantic_input_limits.py tests/context-v1/test_token_io_evidence.py
PYTHONPATH=tests/context-v1/phase0 python3 -m pytest -q tests/context-v1/phase0
```

배포 전에는 두 host marketplace의 네 plugin version/source parity, old coordinate 잔존 여부, actual CLI schema/capabilities/help와 temporary consumer init을 별도로 검증해야 합니다.

### Core+decision profile installer

`profiles/core-decision.json`은 core와 decision을 같은 release로 설치하는 배포 profile이며 두 plugin package나 semantic ownership을 합치지 않습니다. `scripts/install_profile.py`는 사용자가 immutable release checkout에서 명시적으로 실행할 때만 host marketplace와 두 plugin 설치 명령을 순서대로 호출합니다. Plugin runtime에서는 host inventory 탐색이나 install/enable/update를 수행하지 않습니다.

Release tag 전 local 검증에만 `--allow-unreleased-checkout --dry-run`을 사용할 수 있습니다. 실제 설치는 clean checkout의 exact `v<version>` tag를 요구하며, old provider·다른 checkout·mixed version은 자동 정리하지 않고 중단합니다.

### Exact core pin 갱신

semantic plugin은 임의의 `--core-cli`를 실행하지 않습니다. `context-core`의 `skills/context/scripts/context_cli.py`가 바뀌면 같은 commit에서 다음 절차를 완료합니다.

1. `shasum -a 256 plugins/context-core/skills/context/scripts/context_cli.py`로 새 byte digest를 계산하고 `sha256:<hex>` 형식으로 기록합니다.
2. `plugins/context-decision/skills/decision/scripts/decision_cli.py`, `plugins/context-assumption/skills/assumption/scripts/assumption_cli.py`, `plugins/context-term/skills/term/scripts/term_cli.py`의 파생 `REQUIRED_PLUGIN.entrypoint_sha256`와 `tests/context-v1/fixtures/host-inventory/required-plugin.json`을 같은 값으로 갱신합니다. Init/workflow에는 digest를 복제하지 않고 semantic CLI 상수를 재사용합니다.
3. `python3 -m pytest -q tests/context-v1/test_distribution_proof.py::DistributionProofTests::test_semantic_plugins_pin_the_distributed_core_entrypoint`로 실제 core bytes와 네 pin의 parity를 확인합니다.
4. 이어서 위의 네 plugin suite와 cross-plugin, semantic input, token/I/O suite를 실행합니다.

`schema=context-core-schema/v1`, `protocol=context-common/v2`, required commands, `context-owner-descriptor/v2` feature와 doctor shape/state는 pin 일치 뒤 직접 handshake합니다. 이 실행 파일 계약은 marketplace provenance, catalog source 또는 host enabled state를 attestation하지 않습니다. Caller-created inventory/doctor는 low-level compatibility mode의 입력일 뿐 canonical init/workflow의 신뢰 근거가 아닙니다.

## Distribution identity

- Marketplace: `context-plugins`
- Core selector: `context-core@context-plugins`
- Source: `Jeis-Jw/context-plugins`
- Protocol: `context-common/v2`
- Current repository version: `0.7.1`
- Immutable install ref: `v0.7.1` (not created or pushed; owner approval required)

## Provenance

최초 source import는 `Jeis-Jw/ai-plugins@eea43c9386735aa6141203a8a8912b0256746a64`에서 수행했습니다. 무관한 monorepo history를 공개 저장소에 포함하지 않기 위해 clean import commit을 사용하며 상세 범위는 [MIGRATION.md](./MIGRATION.md)에 기록합니다.

## License

이 저장소에는 root [`LICENSE`](./LICENSE)의 Apache License 2.0이 적용됩니다.

라이선스 선택은 완료됐지만 `v0.7.1` tag 생성·push와 marketplace publication은 여전히 각각 별도 owner gate입니다. 라이선스 적용, 검증 또는 source branch push만으로 이 단계가 완료됐다고 간주하지 않습니다.

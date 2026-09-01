# Context Plugins 개발 가이드

이 문서는 repository maintainer와 contributor를 위한 개발·검증 정보입니다. 플러그인 사용법은 [README.md](./README.md)를 참고하세요.

## Repository layout

```text
plugins/
  context-core/
  context-decision/
  context-assumption/
  context-term/
  context-intent/
  context-document/
tests/context-v1/
.claude-plugin/marketplace.json
.agents/plugins/marketplace.json
context/
```

제품·runtime 계약의 공개 정본은 root README, 각 plugin README와 `skills/**/references/*.md`입니다. 이 저장소에는 `wiki/` 레이어를 만들지 않으며, 저장소 자체의 durable project context는 dogfood `context/`를 사용합니다.

## Development

실행 요구사항은 Python 3.11+와 Python standard library입니다. Git은 선택적인 버전관리 도구이며 runtime·설치기·테스트의 의존성이 아닙니다. 테스트 실행에는 `pytest`가 필요합니다.

```bash
python3 -m pytest -q
python3 -m pytest -q plugins/context-core/tests
python3 -m pytest -q plugins/context-decision/tests
python3 -m pytest -q plugins/context-assumption/tests
python3 -m pytest -q plugins/context-term/tests
python3 -m pytest -q plugins/context-intent/tests
python3 -m pytest -q plugins/context-document/tests
python3 -m pytest -q tests/context-v1/test_distribution_proof.py tests/context-v1/test_cross_plugin_flow.py
python3 -m pytest -q tests/context-v1/test_profile_installer.py
python3 -m pytest -q tests/context-v1/test_semantic_input_limits.py tests/context-v1/test_token_io_evidence.py
PYTHONPATH=tests/context-v1/phase0 python3 -m pytest -q tests/context-v1/phase0
```

배포 전에는 두 host marketplace의 여섯 plugin version/source parity, old coordinate 잔존 여부, actual CLI schema/capabilities/help와 temporary consumer init을 별도로 검증해야 합니다.

### Core+decision profile installer

`profiles/core-decision.json` v3는 core와 decision의 설치 좌표, compatible major, release-set minimum을 선언하는 배포 profile이며 두 plugin package나 semantic ownership을 합치지 않습니다. `scripts/install_profile.py`는 사용자가 내려받은 plugin 디렉터리에서 명시적으로 실행할 때만 host marketplace를 등록하고 빠진 plugin 설치 명령만 순서대로 호출합니다. 이미 활성화된 같은-major plugin이 minimum 이상이면 update하지 않고, minimum 미만이면 호환 source 후보를 안내하며 중단합니다. Plugin runtime에서는 install/enable/update를 수행하지 않습니다.

`--dry-run`으로 host 변경 없이 설치 계획을 검증할 수 있습니다. Git 실행파일·metadata·tag·clean checkout을 요구하지 않으며 archive로 받은 파일도 사용할 수 있습니다. Profile·manifest·catalog 일치 검증은 유지하고, old provider·다른 등록 경로·disabled plugin·different major는 자동 정리하지 않고 중단합니다.

### Core compatibility boundary

Package version은 major를 호환성 경계, minor를 기능 추가·변경, patch를 작은 수정에 사용합니다. 이 규칙은 `0.x`에도 적용되어 `0.*`끼리는 package gate를 통과합니다. Semantic plugin은 version만 믿거나 임의의 `--core-cli`를 실행하지 않고 다음 경계를 모두 확인합니다.

1. absolute path와 canonical core entrypoint suffix를 확인합니다.
2. 인접한 Claude/Codex manifest가 모두 `context-core`이고 서로 같은 version인지 확인한 뒤 semantic plugin과 major가 같은지 확인합니다.
3. 실제 `context_cli.py` digest를 계산해 init operation 또는 frozen preview/apply receipt 동안 변하지 않게 결박합니다.
4. `context-core-schema/v1`, `context-common/v2`, required command, `context-owner-descriptor/v2`·`filesystem-vault/v1`와 doctor shape/state를 직접 handshake합니다.
5. `python3 -m pytest -q tests/context-v1/test_distribution_proof.py::DistributionProofTests::test_semantic_plugins_accept_same_major_core_and_reject_other_major`와 각 plugin suite를 실행합니다.

이 실행 파일 계약은 marketplace provenance, catalog source 또는 host enabled state를 attestation하지 않습니다. Caller-created inventory/doctor는 low-level compatibility mode의 입력일 뿐 canonical init/workflow의 신뢰 근거가 아닙니다.

Handshake가 실패하면 semantic adapter는 exact sibling cache layout에서 manifest와 public entrypoint가 일치하는 same-major core 후보만 진단용으로 나열합니다. `doctor`도 loaded catalog pin보다 최신인 same-major cache 후보를 경고할 수 있습니다. 어느 경로도 후보를 자동 선택·실행·대체하지 않습니다.

## Distribution identity

- Marketplace: `context-plugins`
- Core selector: `context-core@context-plugins`
- Source: `Jeis-Jw/context-plugins`
- Protocol: `context-common/v2`
- Current repository version: `0.13.0`
- Optional release tag: `v0.13.0` (not created or pushed; owner approval required)

## Provenance

최초 source import는 `Jeis-Jw/ai-plugins@eea43c9386735aa6141203a8a8912b0256746a64`에서 수행했습니다. 무관한 monorepo history를 공개 저장소에 포함하지 않기 위해 clean import commit을 사용하며 상세 범위는 [MIGRATION.md](./MIGRATION.md)에 기록합니다.

## License

이 저장소에는 root [`LICENSE`](./LICENSE)의 Apache License 2.0이 적용됩니다.

라이선스 선택은 완료됐지만 `v0.13.0` tag 생성·push와 marketplace publication은 여전히 각각 별도 owner gate입니다. 라이선스 적용, 검증 또는 source branch push만으로 이 단계가 완료됐다고 간주하지 않습니다.

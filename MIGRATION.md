# Repository extraction

## Source provenance

- Source repository: `Jeis-Jw/ai-plugins`
- Source commit: `eea43c9386735aa6141203a8a8912b0256746a64`
- Extracted paths:
  - `plugins/context-core/**`
  - `plugins/context-decision/**`
  - `tests/context-v1/**`
  - required host marketplace manifests and pytest configuration

The new repository starts with a clean import commit. This avoids publishing unrelated plugin history while retaining an exact source anchor for audit and comparison.

## Distribution migration

| Field | Previous | New |
|---|---|---|
| marketplace | `jeis-ai-plugins` | `context-plugins` |
| core selector | `context-core@jeis-ai-plugins` | `context-core@context-plugins` |
| source | `Jeis-Jw/ai-plugins` | `Jeis-Jw/context-plugins` |
| plugin version | `0.3.0` | `0.4.0` |
| protocol | `context-common/v2` | `context-common/v2` |

The coordinate change is a breaking distribution migration even though the storage protocol remains `context-common/v2`. Existing installations are not modified automatically. Publication, marketplace installation, reload, temporary-consumer bootstrap and rollback verification remain separate release work.

## Knowledge boundary

The source repository's `wiki/` and `context/` corpus are not imported. This repository initializes a fresh `context/` root and decision area; any non-init DEC or OBS requires its own actual-body review and exact approval digest.

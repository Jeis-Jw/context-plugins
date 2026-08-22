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

The coordinate change is a breaking distribution migration even though the storage protocol remains `context-common/v2`. Existing installations are not modified automatically. The GitHub source repository is public; marketplace publication, installation, reload, temporary-consumer bootstrap and rollback verification remain separate release work.

## Knowledge boundary

The source repository's `wiki/` and `context/` corpus are not imported. This repository initializes a fresh `context/` root and decision area; any non-init DEC or OBS requires its own actual-body review and exact approval digest.

## 0.5.0 additive semantic owners

`0.5.0` adds optional `context-assumption` and `context-term` plugins plus the generic `context-owner-descriptor/v2` registration path. The storage protocol remains `context-common/v2`; existing SNAP, OBS and DEC artifacts are not rewritten.

Users install only the owners they need and explicitly run each installed addon's init. No plugin automatically installs, enables, updates or initializes another plugin. Existing notes, assumptions, glossary files or older context artifacts are not inferred or migrated into ASM/TERM automatically; each durable artifact still requires its own semantic review and exact approval digest.

Rollback is distribution-level: stop using or uninstall the optional addon while leaving its repository artifacts untouched. Automatic downgrade, descriptor mutation, area deletion and corpus cleanup are not provided.

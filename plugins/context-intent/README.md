# context-intent

[한국어](./README.ko.md)

`context-intent` owns desired project directions. An INTENT can exist by itself; DEC does not require one. When both exist, a decision may point to an intent with `serves:intent`.

## Artifact contract

- schema: `context-intent/v1`
- authority: `authoritative`
- authoritative slot: `(scope, intent_key)`
- required H2: `Intent`
- optional H2: `Success criteria`, `Constraints`, `Revisit conditions`
- lifecycle: `capture`, `read`, `search`, and `supersede`

`Intent` states the desired direction. OBS and ASM supply evidence or premises, DEC records a chosen commitment, and DEC `Rationale` explains why that choice follows from its grounds and serves the intent. Each owner remains usable alone.

Supersede retains the slot, retires the predecessor, creates a new ID, and records reciprocal `superseded_by` / `supersedes` references. It requires an attestation over both actual `Intent` bodies. IDs, hashes, and index metadata are not semantic identity.

The semantic CLI only reads its canonical area and produces drafts and validation receipts. `context-core` alone resolves paths, writes artifact and index bytes, creates approval bundles, locks, performs CAS, and applies changes. No Git repository is required; any ordinary filesystem directory can be a vault.

Explicit `$context-intent:init` registers only this owner through an already available same-major `context-core`. It does not install, import, or enable `context-decision` or `context-document`, and it is not part of the `core-decision` profile.

See the project [changelog](../../CHANGELOG.md) for release history.

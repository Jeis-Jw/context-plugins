# context-document

[한국어](./README.ko.md)

`context-document` owns project-scoped current-state statements that an agent or person consumes through recall/envelopes. A DOCUMENT can exist by itself. A DEC may refer to it with `affects:document`, but this plugin does not require or install the Decision owner. External deliverable documents remain repository-owned and are outside this owner.

## Artifact contract

- schema: `context-document/v1`
- authority: `authoritative`
- authoritative slot: `(scope, document_key)`
- required H2: `Content`
- lifecycle: `capture`, `read`, `search`, and `update`

`update` replaces the Current artifact in the same state while preserving its ID, path, scope, and `document_key`. The plugin intentionally has no document taxonomy, subtypes, supersede flow, or backlink index.

Artifact limits are default-read budgets. Expand larger knowledge by adding stable chapter slots such as `design-skeleton`, `design-envelope`, and `design-rules`; do not enlarge one slot.

A decision may point to a document with `affects:document`. The document does not store an inverse edge. During `refresh`, context-core emits a `document-stale-vs-decision` hygiene warning when a Current affecting DEC is newer than the document's `updated_at` (or `created_at` before its first update). Updating the document after the DEC clears the warning. Intent, decision, and document remain independently usable.

The semantic CLI only reads its canonical area and produces drafts and validation receipts. `context-core` alone resolves paths, writes artifact and index bytes, creates approval bundles, locks, performs CAS, and applies changes. No Git repository is required; any ordinary filesystem directory can be a vault.

Explicit `$context-document:init` registers only this owner through an already available same-major `context-core`. It does not install, import, or enable other plugins and is not part of the `core-decision` profile.

Version `0.10.0` is developer preview. No tag or marketplace publication is implied.

Version `0.11.0` adds the canonical single-command inline preview plus approved apply workflow and diagnostic compatible-core candidate paths. No tag or marketplace publication is implied.

Version `0.12.0` defines DOCUMENT as recalled current-state context, documents stable-slot decomposition, and adds the cross-owner freshness hygiene diagnostic. No tag or marketplace publication is implied.

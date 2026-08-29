---
schema: "context-decision/v1"
id: "ctx_a3f48a8f814e4307a7bdfecb350176ee"
title: "Major-based plugin version compatibility"
summary: "Use major versions as the package compatibility boundary and keep installation lightweight."
created_at: "2026-08-29T17:25:08+09:00"
captured_from: "conversation"
tags: ["distribution","compatibility"]
search_terms: ["same-major","plugin version policy"]
scope: "context-plugins/distribution"
decision_key: "plugin-version-compatibility"
revisit_when: ["If a reproducible same-major incompatibility passes the current runtime handshakes, add a versioned capability or explicit minimum constraint instead of restoring global exact-version coupling by default."]
---

## Decision

Use the package major version as the compatibility boundary, minor versions for functional changes, and patch versions for small fixes. Apply the same rule before 1.0, so every 0.* package passes the package-version gate. The profile installer accepts enabled same-major plugins and installs only missing profile members; it does not auto-update compatible packages.

## Rationale

Exact minor and patch equality coupled otherwise independent plugins and forced unnecessary reinstall or update work. Actual execution compatibility is better established by manifest identity plus protocol, capability, command, and doctor handshakes, while each operation remains bound to the actual executable digest.

## Rejected alternatives

- Require exact version equality across all profile plugins and reinstall them together.
- Trust package version alone without runtime protocol and capability handshakes.

## Evidence and constraints

- Same-major package compatibility does not override runtime handshakes; incompatible protocol, capability, command, manifest, or doctor surfaces still fail closed.

## Revisit conditions

- If a reproducible same-major incompatibility passes the current runtime handshakes, add a versioned capability or explicit minimum constraint instead of restoring global exact-version coupling by default.

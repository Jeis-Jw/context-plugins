# Intent protocol

`context-intent/v1` uses descriptor v2 with authoritative slot `(scope, intent_key)`. `Intent` is required; `Success criteria`, `Constraints`, and `Revisit conditions` are optional.

The claim attestation binds `intent_present` and `desired_direction` to the exact candidate. Supersede additionally binds `same_semantic_claim` to the predecessor and successor's actual primary bodies. The owner re-derives the complete result before issuing `context-owner-validation-receipt/v2`.

Only `context-core` writes a vault. The owner has no filesystem write primitive and never installs another plugin. A DEC may independently use `serves:intent`; INTENT does not store an inverse edge.

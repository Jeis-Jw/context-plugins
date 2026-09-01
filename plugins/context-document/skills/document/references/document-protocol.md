# Document protocol

`context-document/v1` uses descriptor v2 with authoritative slot `(scope, document_key)` and one required `Content` H2 section.

Capture binds `content_present` and `living_document` to the exact candidate. Update binds a live ID/path/SHA precondition and exact replacement Content, then emits one `replace` operation with generic topology `replace_same_state`. ID and slot remain stable.

Only `context-core` writes a vault. The owner has no filesystem write primitive and never installs another plugin. A DEC may independently use `affects:document`; DOCUMENT does not store an inverse edge.

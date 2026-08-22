---
name: context
description: Audit only the new conversation delta; when durable context can change the answer, recall Current context metadata-first and route mature candidates to the semantic owner.
---

# Context

Audit only the meaning added by the current user turn, in the same response pass and without another model call. If there is no durable signal, continue the original conversation without an audit status or capture question. Context-core performs this audit once per delta; addons do not repeat it.

Keep only a small session-local ledger: current scope/anchor, Current `{id,sha256}` values whose bodies remain in context, short pending candidate references and maturity, dismissed/deferred references, and evidence anchors. Never copy bodies into the ledger or write the ledger to the repository. Invalidate only entries affected by a changed scope, evidence, anchor, index, artifact SHA, or missing session body. Do not re-propose dismissed/deferred items without new evidence.

1. Recall index metadata only when prior context could change the current judgment. On a healthy metadata miss, do not open arbitrary indexed bodies. Narrow the query or report an index warning. Use `--read` only for relevant items and `--pack` only for a narrowly selected set.
2. Let the installed semantic owner compare actual primary claims, supporting sections, scope, and rationale. Hashes, fingerprints, IDs, and metadata are not semantic evidence. Report a conflict or rationale change, with relevant IDs and differences, before the primary conclusion.
3. Otherwise finish the user's request first. Propose a grouped capture at most once per semantic milestone, and only for mature context likely to affect future work. A batch has at most eight candidates.
4. Use `context_cli.py capabilities --json` and only addon capabilities already discovered by the host. Before v2 addon bootstrap, require `context-owner-descriptor/v2` in `context_cli.py schema --json`. Do not search plugin caches, start owner processes, or substitute another runtime. Route by explicit request, specialized owner, observation fallback, handoff, then skip.
5. Limit common primary claims to 2,000 codepoints, canonical owner input to 8 KiB, and the complete canonical `context-capture-batch/v1` envelope to 16 KiB. `candidate_id` is a transport reference, not meaning.
6. Context-core validates owner results, ordered overlays, structural profiles, lifecycle relations, indexes, and target bytes before sealing a complete final bundle.
7. Approval material includes exact `context-repository-identity/v1` for the resolved worktree and Git common directory. Call `transaction apply` only after the user approves the exact `approval_digest`, and only in that same repository identity. Never regenerate the candidate, attestation, timestamp, path, plan, or content after approval.

Audit, recall, route, claim, draft, validation, preview, and a denied apply do not change repository or host-policy bytes. Context-core is the only physical writer.

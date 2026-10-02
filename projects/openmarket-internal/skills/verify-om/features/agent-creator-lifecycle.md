# Agent creator lifecycle and private-state isolation

*Verified: 2026-10-02, daemon `6d5700ee09e8dc184a2da1b6d53f3514c0420782` — 956-test integration gate, compiled recipient recovery after normal GUI rollback, release-local skill read and single reply delivery. Revoked-mention refusal/restart deduplication was proved on preceding `9cb0f2660`; populated package isolation and same-key revocation reconciliation retain their earlier exact scopes.*

The local daemon owns agent release, installation and account state. Shared text packages have immutable digests; each recipient uses its own credential, notes and private memory. A channel invocation must use the selected release and either deliver a bounded reply or explain why it cannot run.

## Sub-features

- Stage supported local text definitions and skill directories, review provenance/omissions/access, then approve a shadow installation.
- Run a private preview without durable conversation, memory, run or delivery writes.
- Publish a bounded text package with authenticated server-ledger identity; never export publisher-private state.
- Adopt as a distinct authenticated recipient, pin the reviewed digest, and use that recipient's own model credential.
- Update only after explicit review/approval; retain a reviewable recipient overlay and support rollback.
- Revoke an exact digest, reconcile uncertain readback using the same idempotency key, and refuse model execution on revoked versions.
- Bootstrap private memory from an empty namespace through normal owner consent; compare populated publisher and recipient state.
- Page large server vault maps while keeping unavailable/unverified source limits visible.
- Advertise coding readiness only for a qualified executable, adapter, sandbox and host tuple.

## How to get to it (user POV)

Open the local daemon's `/rooms`, choose **Agents**, and create or import a text agent. Review and install it, grant the intended test channel, then mention it in that channel. Use its private **Try** action for a preview.

In the server catalog, publish a version from profile A. Sign the second owned test home into profile B, review/adopt that exact version, and invoke it as B. Use the installed-catalog update and rollback review controls; check the actual selected version after applying.

To test privacy, request a benign preference through A's agent, explicitly approve the normal memory question, then publish another version. B should receive the package files without A's private memory, overlay or credentials.

## Driving it with control-om

Start from an owned private worktree. Use the assigned lane state and port for every wrapper call; never target operator port 31337 or share its home. Two-profile proof needs two independently authenticated isolated homes, not a guest placeholder or direct database seeding.

```sh
export OM_LANE_STATE='<run-owned state root>'
export OM_LANE_PORT='<assigned lane port>'
control-om doctor
control-om up --compiled --env OM_DEV=1 --env OM_ROOMS_GUI_DIR='<candidate GUI>/dist'
control-om url /rooms/
control-om cli -- packages/cli/dist/om '<read-only command>'
```

Keep the owned lane process anchored for this tool host's lifetime. Read authenticated RPC responses through the lane's normal owner browser; do not reconstruct operator cookies. DB inspection is read-only and reports IDs/counts/digests, not secrets or private memory contents. Never print whole coding-run correlation or manifests: host and lease tokens are nested there. Read only explicitly selected safe diagnostic fields.

Correlate the source channel message with invocation, run, `skill_read`/`post_reply` events, selected release digest and delivery receipt. D3 source 225/reply 226 completed with one delivery attempt/effect and recipient memory count zero. After revocation and normal GUI rollback, D1 source 233/reply 234 also completed on final daemon 6d5700ee0 with one delivery effect and no recipient memory. Compare all six package files byte-for-byte after the opted-in update; publisher had two private memory rows and one overlay, recipient had neither and retained a distinct credential.

For revocation, preserve the first operation result, inspect the authenticated ledger head, and replay the identical idempotency key when reconciling. D3's first attempt returned 409; subsequent read/replay confirmed revoked revision 2 without another revision advance. A revoked invocation must not execute the model or tools. Then review/apply rollback and send a fresh bounded task to prove recovery.

## Gotchas

- Final daemon v23 passed 956 integration tests, 4,648 assertions across 46 files, whole-workspace typecheck, lint and compilation. Earlier v21 export-scan timeout remains a failed receipt; no bound was raised to pass the repaired scan.
- Whole-workspace typecheck needed an 8 GB Node heap on this host; the earlier 4 GB OOM is not a successful check.
- Catalog retry budget bounds cumulative sleep within one operation, not all network wall time. A slow request can still outlast it.
- The repaired revoked watcher keeps execution disabled but admits an unambiguous authorized owner mention solely for a refusal. Sources 229/231 each delivered one clear notice without a run; restart did not duplicate notices. Normal D3→D1 review/apply rollback preserved the recipient credential and private namespace. Final source 233 then completed with one delivered effect, reply 234.
- Exact supported Claude 2.1.278 and Codex 0.153.4 were installed only in the private test lane and match existing qualification digests; both report signed in/coding-ready. Global newer versions stay unverified. Never edit a binary hash or attestation to manufacture qualification. Fresh Claude task 235 stopped safely after upstream HTTP 400 made usage unverifiable; its failed coding attempt is not a completed lifecycle.
- Native coding receipts from older versions, synthetic conformance fixtures, chat invocation and model-driven file implementation are separate claims.
- The SDK archive is unpublished; local package consumption does not prove clean registry install. Publication/pin/lock promotion remains a separate delivery step.
- Test catalog publication and channel posting were authorized in `local_longan_storage`. Product push, registry publication, release and merge retain their per-instance delivery boundary.

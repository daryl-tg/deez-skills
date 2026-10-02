# Agent creator lifecycle and private-state isolation

*Verified: 2026-10-02, final source `158bc6c156b798731107440b62561ce7902bcdc2` — 66 free regression tests, typecheck and lint; native Codex 249 and Claude 255 coding lifecycles on `1bedf936ea456229bfc819db2bda5ca2e48c632f`; accurate compatibility notice 259 on `365d9963856ace29ee49479ffc4d502378ef455c`. Recipient recovery remains scoped to `6d5700ee09e8dc184a2da1b6d53f3514c0420782`, revoked refusal/restart deduplication to `9cb0f2660`, and populated package isolation to its original receipt. Required paid evaluations and registry delivery remain open.*

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
control-om om -- status --format json
```

Keep the owned lane process anchored for this tool host's lifetime. Read authenticated RPC responses through the lane's normal owner browser; do not reconstruct operator cookies. DB inspection is read-only and reports IDs/counts/digests, not secrets or private memory contents. Never print whole coding-run correlation or manifests: host and lease tokens are nested there. Read only explicitly selected safe diagnostic fields.

Correlate the source channel message with invocation, run, `skill_read`/`post_reply` events, selected release digest and delivery receipt. D3 source 225/reply 226 completed with one delivery attempt/effect and recipient memory count zero. After revocation and normal GUI rollback, D1 source 233/reply 234 also completed on final daemon 6d5700ee0 with one delivery effect and no recipient memory. Compare all six package files byte-for-byte after the opted-in update; publisher had two private memory rows and one overlay, recipient had neither and retained a distinct credential.

For revocation, preserve the first operation result, inspect the authenticated ledger head, and replay the identical idempotency key when reconciling. D3's first attempt returned 409; subsequent read/replay confirmed revoked revision 2 without another revision advance. A revoked invocation must not execute the model or tools. Then review/apply rollback and send a fresh bounded task to prove recovery.

## Gotchas

- Earlier daemon v23 passed 956 integration tests, 4,648 assertions across 46 files, whole-workspace typecheck, lint and compilation. Earlier v21 export-scan timeout remains a failed receipt; no bound was raised to pass the repaired scan.
- Whole-workspace typecheck needed an 8 GB Node heap on this host; the earlier 4 GB OOM is not a successful check.
- Catalog retry budget bounds cumulative sleep within one operation, not all network wall time. A slow request can still outlast it.
- The repaired revoked watcher keeps execution disabled but admits an unambiguous authorized owner mention solely for a refusal. Sources 229/231 each delivered one clear notice without a run; restart did not duplicate notices. Normal D3→D1 review/apply rollback preserved the recipient credential and private namespace. Final source 233 then completed with one delivered effect, reply 234.
- Exact qualified Claude 2.1.278 / ACP 0.76.0 with claude-opus-4-6 and Codex 0.153.4 / ACP 1.11.0 with gpt-6-astra each completed a fresh coding lifecycle on daemon 1bedf936e, sources 255 and 249. Each made a clean README-only commit, passed the actual sandbox 12-test/build commands, delivered Result/History/chat, and reached completed without host completion. Global newer runtimes stay unverified; never edit hashes or attestations to manufacture qualification. Opus 5.5 rejects this qualified Claude client version even through normal native headers, so readiness of the executable does not promise every selectable model works.
- Native coding receipts from older versions, synthetic conformance fixtures, chat invocation and model-driven file implementation are separate claims.
- The SDK archive is unpublished; local package consumption does not prove clean registry install. Publication/pin/lock promotion remains a separate delivery step.
- Test catalog publication and channel posting were authorized in `local_longan_storage`. Product push, registry publication, release and merge retain their per-instance delivery boundary.

- `control-om om -- ...` binds the CLI to the owned lane home and port. `control-om cli -- ...` is a generic repository-command runner and does not set OM_HOME; never use it for account/model mutations without explicit isolation. An initial test command changed the operator model accidentally; that incident remains disclosed and restoration awaits the prior value.
- A delivered room reply may precede the durable completed transition. Claude 255 spent 201 seconds in final receipt/proof/worktree verification after its last effect, then completed normally. Do not restart an active supervisor just because that bounded verification is quiet.
- Actual native checks exited zero while Bun printed directory/parent-access diagnostics. Report the warning and actual exit code separately.
- Final main 2395 daemon integration passed 1,087 tests/5,320 assertions on 59b4f03f1. Later narrow classifier wording changes have their own focused and typecheck receipts; cite exact source scopes. The first live compatibility notice 257 remains a failed receipt. Fresh source 259 on compiled daemon 365d99638 classified model_client_unsupported and delivered exactly one accurate rendered explanation with a clean worktree; no unsupported model was silently substituted.

- Final source checks passed 66 free tests/507 assertions, CLI typecheck, lint and diff checks. Its 36 live-only dry skips do not prove model execution. Orders tier 3 and compose tier 3 remain failed: some rows passed on earlier runs, but the final repaired fixtures need fresh full paid verification after the pinned ChatGPT lane quota is restored. Aggregate usage allowance does not prove a specific model lane has capacity.
- The compose fixture now reads every source user goal when identifying a subject watch, while retaining label/group matches and excluding unrelated request-only text. Journal preservation assertions were retained; no bounds or safety gates were relaxed.
- Final source secret scan remains red on 75 exact unchanged-main findings, zero feature-added. The exact SDK archive passed across 275 files. Do not relabel unchanged-main findings harmless or treat local archive tests as registry delivery.

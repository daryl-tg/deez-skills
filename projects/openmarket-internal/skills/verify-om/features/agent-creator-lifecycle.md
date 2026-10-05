# Agent creator lifecycle and private-state isolation

*Verified: 2026-10-05, native Codex 261/Claude 263 completed on daemon `d24bded8f`; repeated current-release skill reads passed on `39e94a54f`; D5 adoption/execution passed on `335a63073`; revocation/refusal/rollback and restored D4 execution passed on private `288f6e0fb80f251aaa8fca7a56b4281d5b58d7e8`, binary `68ef77883432db56c72e16f4359cfeea1e952edfb31791d26a85489c35ea07a7`. GUI is `1c11e331`. Required paid evaluations and registry delivery remain incomplete; restart refusal deduplication retains its older `9cb0f2660` evidence.*

The daemon owns release, installation and account state. Shared text packages have immutable digests; recipients use their own credentials, notes and private memory. An invocation uses the selected release and either completes its task or clearly explains why it cannot run. Units 1–4 cover supported local creation/import/sharing; arbitrary third-party runtime admission is deferred.

## Sub-features

- Stage supported definitions and skill directories, review provenance/omissions/access and approve shadow installation.
- Run private Try without durable conversation, memory, run or delivery writes.
- Publish authenticated server versions without publisher-private state; adopt as a separate authenticated recipient and pin the reviewed digest.
- Require explicit update/rollback review and preserve recipient credentials and private state.
- Revoke an exact digest, reconcile uncertain readback with the same command/key and refuse execution while explaining recovery.
- Read the selected release-local skill correctly across multiple invocations on the same daemon.
- Read pinned task-vault context, implement in a private linked worktree, run actual checks, commit locally and deliver Result/History/chat before durable completion.
- Report coding readiness only for a qualified executable/adapter/sandbox/host tuple; unsupported combinations receive an accurate failure notice.

## How to get to it (user POV)

Open the local daemon /rooms and choose **Agents**. Create or import, review and install a text agent. Grant the intended channel and mention it there. Private **Try** previews the agent without normal durable effects.

Publish from A and review/adopt as B in a separate owned signed-in home. Review/apply an update with a different skill phrase, revoke that server publication and invoke its selected version to prove refusal. Review/apply rollback and invoke again to prove recovery.

Populate A private memory through normal consent before testing package isolation. B receives the package bytes without A memory, overlays or credential. Do not seed product state directly in a database.

## Driving it with control-om

Use a private worktree and assigned state/ports for every wrapper call. Two-profile proof requires independent authenticated homes. Never target the operator port or reconstruct its cookies.

```sh
export OM_LANE_STATE='<run-owned state root>'
export OM_LANE_PORT='<assigned lane port>'
control-om doctor
control-om up --compiled --env OM_DEV=1 --env OM_ROOMS_GUI_DIR='<candidate GUI>/dist'
control-om url /rooms/
control-om om -- status --format json
```

Keep the owned process anchored for the tool host lifetime. Use its authenticated browser for normal Agent Center/channel actions. Correlate source message, invocation/run, selected digest, tool events, effects and the durable completed transition. Read-only database inspection reports IDs/counts/digests only. Never print whole correlation, coding manifests, credentials or memory contents; nested host/lease tokens exist in them.

Current sequence: D4 sources 272/274 returned forest cabin 1005 as replies 273/275 on one daemon. D5 update source 276 returned amber canoe 1005 as reply 277. Revoked source 278 received refusal 279. Review/apply rollback selected D4, and source 280 returned forest cabin 1005 as reply 281. Successful guide runs actually called skill_read/post_reply and each had one first-attempt delivered chat_post effect. Refusal is a direct watcher notice, not a roster effect receipt.

Compare every package file for both releases and both profiles. D4 and D5 each have six exact cached files. Publisher private memory/overlay counts remain 2/1, recipient 0/0; owner IDs differ. Equal deterministic namespace strings are scoped by separate account homes and owners. Counts alone are not a complete authorization proof.

For native work, sources 261/263 each read vault revision 1, edited only README.md, ran 12 passing tests/24 assertions and build, made a clean local commit, delivered Result revision 2 and History revision 3 plus one reply, and completed without host implementation. Preserve the actual command exit codes and source-specific receipts.

Publish paired browser evidence through the designated helper. Gallery agent-creator-20261002/r05 names the exact execution and viewing source for each frame. A bad viewport capture is retained but excluded from asserted proof.

## Gotchas

- Source 278 has a failed bookkeeping run before executor/tool activity. Zero tool calls is not zero run records. The channel refusal says the version was revoked and explains how to choose an active version or roll back.
- Server publication revocation is distinct from the publisher own local installation. Recipient rollback creates its reviewed installation with the previous D4 digest and retains its private account state.
- A cached runtime tool collection once bound the first release resolver permanently. Current-run dispatch binding repaired the second-run D4 refusal without weakening the guard. Verify multiple consecutive invocations after an update.
- Catalog private repair passes 51 tests/141 assertions, full typecheck/build and scoped Biome. It shares only an in-flight list for the current owner/room and carries current verified context forward. Authority loss, owner/room separation and failed-read cleanup remain checked.
- Catalog retry budget bounds cumulative sleeping within one operation, not all request wall time. It is not shared across all backend principals/readers. Initial A load throttled under paid traffic, then one Refresh recovered; the paid seed shares A credentials. Quiet post-eval initial selection also failed (screenshot29); preferences/config/proposals succeeded. The subsequent authority-batch repair on 3b8496603 completed both first catalog selections without Refresh: all six releases, correct state and publisher curator controls; catalog/installed reads returned 200. Loading included backend retry, so this is not a fast-load claim. Recipient source 282 then read installed D4 via actual skill_read, completed and delivered reply 283 once.
- Publisher publication follow-up readback was uncertain despite POST 200. Recipient independently read/adopted the exact D5 release. Preserve the first outcome and retry the same command/key rather than another mutation.
- Qualified Claude 2.1.278/ACP 0.76.0 with Opus 4.6 and Codex 0.153.4/ACP 1.11.0 with gpt-6-astra completed the current coding tasks. New global clients, other models and other operating systems remain unverified. Never fabricate hashes/attestations or silently substitute a model.
- A reply may precede completed while receipt/worktree checks finish. Do not restart an active supervisor just because it is quiet. Claude History needed two attempts and one reconciliation but did not create duplicate server revision/chat.
- Native commands exited zero while Bun emitted parent-directory diagnostics; the build scanner withheld stdout. Inspect expected artifacts and retain those warnings separately.
- Main-rebased daemon typecheck/build/lint pass. Typecheck used a command-local 8 GiB Node heap after the retained 4 GiB OOM. Do not apply that override to Bun tests or daemons.
- Private eval-only d1313c251 observes delivered composer journal text, not initial progress. Its 37 focused checks/436 assertions and full typecheck pass; 29 pre-existing live-disabled registrations are not model proof. Failed/empty deliveries, missing links and wrong counts still fail. A first new fixture typecheck failure is retained and corrected.
- Paid orders and change passed on 335a63073. Doors first run failed 4/43; private fixtures repair three missing watches, while the ECB prompt boundary remains unresolved. Full compose finished FAIL with21 passing/7 failing tests and218 assertions,28 registrations; canonical checks88 PASS/13 FAIL/24 BLOCKED. Watches completed with 10 passing/47 failing tests, 523 assertions and 57 registrations across 52 live cases plus five dry checks. No thresholds, deadlines, retries, skips or baselines were weakened, and selected unchanged-main W05/W08/W14 also failed. Only those three cases are compared; no full-suite causality or green verdict is inferred.
- Full source scan remains red on 76 unchanged-main findings, zero feature-added. The 275-file SDK archive scan passes. Local archive consumption does not establish registry delivery; the SDK remains unpublished.
- control-om om binds the owned home/port; control-om cli is a generic command runner. An earlier accidental operator model change remains disclosed and its original value unknown. Main allowance and a routed model pool's capacity are separate observations.
- Test catalog actions and normal account-browser posts are authorized in local_longan_storage. SDK/product publication, merge and release keep their concrete per-instance authorization boundary. Preserve original worktrees, homes and failed receipts.

- Latest local daemon assembly is e08d96f0f. The bounded authority-batch fix retains local owner checks around every read and one final remote membership refresh before exposing at most three revisions. Catalog contracts: 153 pass/0 fail/579 assertions, full workspace typecheck/build and scoped Biome pass. Fixture read budgets are synthetic, not public backend quotas.
- An overbroad 430-file roster diagnostic remains FAILED/INCOMPLETE after one ACP initialize fixture timeout (754 observed passes). Test-only injected clock stabilization passes 100 focused ACP contracts/494 assertions and fresh CLI typecheck; production timeouts are unchanged.
- Selected J9–11/F2 paid composer diagnostic passes four tests/127 assertions, with nine F2 table checks. F2 supplies the required 18:00 clock and checks exact daily cron; its daemonless fixture does not prove actual scheduled execution. This partial run never replaces the failed full gate.
- A fresh fetch shows eight daemon main commits beyond the verified e7 base (latest bfc2a4143); GUI main remains 231c95f4. Delivery requires an isolated rebase and renewed applicable checks. Existing source-specific receipts remain immutable.

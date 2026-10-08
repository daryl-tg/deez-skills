# Agent creator lifecycle and private-state isolation

*Current local verification 2026-10-08. Delivery source `b1c53c9665f2d76219f72505b722e0a24249e280`, tree `7b3af06fae9c6103f29148f80a8200d3e95ce4ff`, binary SHA256 `176119e6cb6cbfa00b240cd99518571a51685f68b754dcbf64cf9d9dca2e0277`; GUI `2fc19842692e61b82e81c164a55de70199cf8fc4`. Native C6/X4/S2 execution source `635441fb083971c1ff5143835521d5c8193e60c2`, binary `7e7f8ee1e25556d1cc75ad61e0d3f4f240dd0715331a52d4d33f8e71067af213`. The delivery assembly adds three unrelated WRUN-main commits and is separately tested/compiled. Final restart retained completed runs without duplicate replies. Gallery `agent-creator-stress-20261007/r02` (operator-local evidence) labels current viewing and historical execution separately. Broader paid evaluations and clean registry delivery retain their failures/gaps.*

The daemon owns release, installation and account state. Shared text packages have immutable digests. Recipients use their own credentials, notes and private memory. An invocation completes its task or clearly explains why it cannot run. Supported local text-agent/Agent Skills creation and sharing are distinct from arbitrary third-party runtime admission.

## Sub-features

- Stage supported definitions/skill directories, review provenance, omissions and access, and approve shadow installation.
- Run private Try without durable conversation, memory, run or delivery writes.
- Publish authenticated server versions without publisher-private state; adopt as a separate user and pin the reviewed digest.
- Explicitly review update/rollback, preserve recipient-private state and revoke an exact release.
- Read the selected release-local skill across repeated invocations on one daemon, including after update/rollback.
- Read bound task-vault context, implement in a private linked worktree, run actual checks and commit locally. Deliver Findings/Plan/Result/History/chat before durable Completed.
- Fence current coding claims, native producers, manifests, budget and credential grants across restart. Missing current work output fails; it never falls back to host completion.
- Advertise readiness only for the qualified CLI/adapter/sandbox/platform/host tuple; report actionable startup/auth/quota/policy failures to the invoker.

## How to get to it (user POV)

Open the local daemon's **/rooms**, choose **Agents**, then create/import, review and install a supported text agent. Grant the intended channel and mention it there. **Try** is a private preview.

Publish as A and review/adopt as B in a separate signed-in home. Review/apply changed knowledge or a changed skill phrase, invoke that release, revoke it, verify refusal, and review/apply rollback before invoking again. Populate private memory only through normal consent. B should receive shared package bytes without A's memory, overlays or credential.

For work, use a feature template and linked repository. Open **Review Plan**, read the bound context and proposed changes, then **Approve Plan** and **Start approved work**. Follow automatically refreshed Work, recorded proof, local delivery history and the Run Topic reply.

## Driving it with control-om

Use private worktrees, assigned ports and independently authenticated owned homes. Never target operator ports or reconstruct account cookies.

```sh
export OM_LANE_STATE='<run-owned-state-root>'
export OM_LANE_PORT='<assigned-lane-port>'
control-om doctor
control-om up --compiled --env OM_DEV=1 --env OM_ROOMS_GUI_DIR='<candidate-GUI>/dist'
control-om url /rooms/
control-om om -- status --format json
```

Keep the process anchored. Use normal account-browser Agent Center and channel actions. Correlate source message, run, selected digest, current attempt/epoch, native tools, command exits, local commit and every delivered effect. Read-only inspection must output allowlisted IDs/counts/digests, never whole correlation/manifests/credentials or private memory. No live DB writes and no runtime-ledger resets.

Latest Claude C6 source320/reply324 quoted the bound Birch compass1007 guide in Findings, recovered a controlled pre-manifest daemon interruption on the same a2/e2 with successor lease4 and one current manifest, natively made README commit4268dcd9, passed16focused tests/build and all5required checks, delivered all5effects once, and became Completed. Original20-minute budget and actual135165ms human pause were preserved; native proof sealed before deadline. Total journey1850.05s exposes slow finalization. Phrase placement in Findings rather than Plan remains a minor task-instruction deviation.

Latest Codex X4 source325/reply327 read Maple harbor1007 from the bound guide, obtained normal owner approval, natively made README commit0842322d, passed16focused tests/build and all5checks, delivered all5effects once and became Completed. Its original20-minute budget,43624801ms overnight human approval pause, a2/e2 and two total manifests remained intact. Automatic publishing lease handoff retained the same attempt and produced no duplicate effects. Do not interpret the overnight approval pause as model runtime.

Recipient S2 source322/reply323 on daemon635 called actual skill_read/post_reply, read Juniper ribbon1007 from knowledge/README.md and delivered one84-character reply as the independent dboon_ref user. Finalb1c restart retained C6/X4 completed states and five first-attempt effect receipts each without duplicates. The positive tasks are bounded README changes, not arbitrary feature-implementation certification.

Historical sharing on GUI29e414ad/daemon7f7304243 proved two identical recipient installations converge to one, Juniper guide execution, reviewed0.2 Willow update,0.1 Cedar rollback, and exact0.2 revocation with0.1 preserved. Historical desktop/phone pending-review replay on GUI087/daemonb1e93b1 reused package/approval without another installation or event.

Historical source stamps: repeated selected-release skill reads used39e94a54f; D5adoption/execution used335a63073; revocation/refusal/rollback and restoredD4 used288f6e0fb80f251aaa8fca7a56b4281d5b58d7e8 / binary68ef77883432db56c72e16f4359cfeea1e952edfb31791d26a85489c35ea07a7 / GUI1c11e331; restart-refusal deduplication also retains9cb0f2660 evidence.

Earlier source-specific proofs remain historical: Codex261/Claude263 on d24bded8f read vaultrev1, edited only README, passed12tests/24assertions and build, committed locally, delivered Resultrev2/Historyrev3 and one reply. D4 sources272/274 returned forest cabin1005 as273/275; D5 source276 returned amber canoe1005 as277; revoked278 received279; rollback280 returned forest cabin1005 as281. D4/D5 six-file packages matched across profiles; publisher memory/overlay2/1 and recipient0/0 with different owners. These counts alone are not a complete authorization proof. Gallery agent-creator-20261002/r05 retains the original source stamps.

## Gotchas

- C5 ended cleanly in ACP but returned a new Plan without edits/current output. Its failure remains immutable. The prompt repair explicitly says the owner already approved and to execute now without replanning; C6/X4 prove that repair without weakening work_stage/work_commit/checks.
- Cancelled old C4/X3 retain their original budgets, receipts and native commits. One readable timeout notice was delivered for each. X2 correctly refused a passing debugger baseline before native edits and delivered one actionable notice. A successful successor does not relabel these failures.
- A reply or five delivered effects can precede the authoritative Completed transition while receipt/worktree finalization runs. Preserve a sealed successful native proof and original ledger; do not kill an active supervisor solely because progress is quiet.
- Claude2.1.278/ACP0.76.0/Opus4.6 and Codex0.153.4/ACP1.11.0/gpt-6-astra used restored subscriptions on macOSarm64. New global clients, other models/platforms, arbitrary executable harnesses and implicit private-host skills remain unqualified.
- Final delivery gate:1,156pass/0fail/12,822assertions, full canonical typecheck with command-local6144MB Node heap, lint/build and actual runtime selection. Fresh compiled credential gate17pass/0fail/136assertions against binary176119e6 checked owner/current operation, cancellation, rotation, producer and read-only/write boundaries. Initial fresh-checkout test failure is retained; the declared contracts browser build prerequisite was missing. No source threshold/timeout/skip changed.
- Parent integration b1e93b1 passed1,258tests plus17compiled credential tests; prompt-only635 passed261affected tests/1,302assertions and full canonical typecheck/lint. Originalfe3repair remains preserved with561tests/2,962assertions. Never substitute an earlier default-heap OOM or8GB source-only run for the current6144MB gate.
- Release revocation differs from the publisher's own local installation. Current-run skill resolver binding is required across repeated invocations; a cached first-run resolver once caused a false refusal and was repaired without weakening its guard.
- Historical e08d96f0f catalog authority batching retains local owner checks around every read and a final remote membership refresh for at most three revisions. Its153tests/579assertions and full typecheck/build/Biome pass are source-specific. Fixture request budgets are not public backend quotas; catalog retry budget limits sleeping, not total wall time. Earlier throttled selections and uncertain publication readback remain failed/uncertain, despite later successful selections/adoption.
- Historical broad430-file roster diagnostic remains failed/incomplete after an ACP fixture timeout (754observed passes). Injected-clock stabilization passed100focused ACPcontracts/494assertions; production timeouts stayed unchanged. Terminal publication matrices retain their exact original source/binary stamps.
- Historical paid orders/change passed on335a63073. Doors initially failed4/43, with the ECB prompt boundary unresolved. Full compose remains FAIL21pass/7fail/218assertions, canonical88PASS/13FAIL/24BLOCKED. Watches remains10pass/47fail/523assertions across57registrations. Selected unchanged-main W05/W08/W14 also failed; that does not establish full-suite causality. Partial J9–11/F2 diagnostics4tests/127assertions do not replace these failures or prove actual scheduling.
- Historical private eval d1313c251 reads delivered composer journal text;37focused checks/436assertions passed. Its29live-disabled registrations are not model proof. Failed/empty deliveries and wrong links/counts remain failures.
- Full source scan retains76unchanged-main findings and zero feature-added;275-file SDK archive scan passed. Registry0.104.0-roster.1 returnedE404 on2026-10-08. Exact local archive SHA2562cca8b49b93b2aa62a4e9730ff9b5d37e100272cdb080f1e9b8c5c76a82c0cb4 does not prove clean registry delivery. Tracked GUI pins/root lock remain0.103.0 pending authorized restricted preview publication and renewed gates.
- Current GUI full gates:rooms22,250pass/0fail/2existing unrelated skips, cloud16,776pass/0fail/0skip. Static Markdown records preserve readable content without active media; visible10-second single-flight progress polling preserves open details on revision changes and clears stale authority boundaries. Chromium phone rendering is not native WebView certification; contrast audits remain incomplete.
- control-om om binds the owned home/port; control-om cli is generic. An older accidental operator model change remains disclosed with original value unknown. Main allowance and routed pool capacity are separate; pause before starting a new task below10% remaining.
- Normal account-browser posts/catalog actions in local_longan_storage are authorized. Map-only sync is separately authorized. SDK/product publication, product branch push, merge and release require concrete per-instance approval. Original worktrees, homes and failed receipts are preserved. No Tharamine/relay changes were needed in this pass.

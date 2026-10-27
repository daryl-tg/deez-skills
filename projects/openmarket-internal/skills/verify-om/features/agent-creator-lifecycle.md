# Agent creator lifecycle and private-state isolation

*Verified: 2026-10-28, tree `a8fa10974` (origin/main, v0.466.0), lane on 18103, guest, no `OM_DEV` on the lane. The guest-lane recipe below gave the same results as on 2026-10-27: empty `agent runs`, the `not_found`/`malformed_body` refusals, header-only `roster list`, zeroed `roster measures`, `agent eval nobody` → `found 0`, and empty `/rpc/v1/roster/projects` and `/instances`. New on this tree (#2167/#2169): the default agents install from `@om-skills` registry packages after boot. Production answered 404 for `@om-skills/argue`, and the lane log showed the retry doubling 30, 60, 120, 240 and 480 s. Not driven: a successful default install (no registry lists the packages yet), create/import, Try, install, publish/adopt, runs, plan approval, steer, delivery, and every GUI step. Previous stamp `8fe6a8432` is an ancestor (10 commits).*

> **On main since `b50ca927d` (#1948), v0.465.0.** The daemon mechanisms now
> live in `packages/roster/` (moved from `packages/cli/src/runner/roster`).
> The roster boots in every daemon unless the setting `roster.enabled` is `0`
> or `false`. Only the CLI verbs are dev-gated: `om roster`, `om project`, and
> the `runs`/`pause`/`cancel`/`steer`/`eval` subcommands of `om agent` register
> only when the CLI process itself has `OM_DEV=1`. The GUI half (openmarket-chat
> MR !75, the Agents surface in `/rooms`) belongs to `verify-om-chat` and was not
> checked here. The closeout record below was driven on the branch and remains
> historical. Only the guest-lane section was driven on main.

*Closeout verified 2026-10-12. GUI `194281a1dbe02b29ca6542170a704d1726884a09`, daemon `a3a81a5f5192a3786c46e0dc3e7e911c2cb86f7c`, binary `5085976c818d929c64fc9fec15efefc5f7a537d3cd7be3b6f221044dd378f8bb`. Native C6/X4/S2 executed on daemon `635441fb083971c1ff5143835521d5c8193e60c2`, binary `7e7f8ee1e25556d1cc75ad61e0d3f4f240dd0715331a52d4d33f8e71067af213`; current viewing and restart readback are distinct. Root-reviewed gallery `agent-creator-stress-20261007/r03` is operator-local evidence. Private registry installation is qualified. Review requests: https://gitlab.com/openmarketxyz/frontend/openmarket-chat/-/merge_requests/75 and https://github.com/openmarket-xyz/openmarket-internal/pull/1948. Local gates passed, but three daemon workflows received no runner or steps because GitHub Actions is blocked by account billing or spending limits. Ready for review, not merge-ready; no main merge, deployment or release.*

The daemon owns release, installation and account state. Shared text packages have immutable digests. Recipients use their own credentials, notes and private memory. An invocation completes its task or clearly explains why it cannot run. Supported local text-agent/Agent Skills creation and sharing are distinct from arbitrary third-party runtime admission.

## Sub-features

- Install the eight default agents and skills (argue, debugger, explain, fact-check, feature, librarian, agent-builder, clanker) from `@om-skills` registry packages, live behind a notice, in the background after boot; keep them current every six hours and honour a registry withdrawal (#2167). The signed bundled snapshot is gone (#2169).
- Stage supported definitions/skill directories, review provenance, omissions and access, and approve shadow installation.
- Run private Try without durable conversation, memory, run or delivery writes.
- Publish authenticated server versions without publisher-private state; adopt as a separate user and pin the reviewed digest.
- Explicitly review update/rollback, preserve recipient-private state and revoke an exact release.
- Read the selected release-local skill across repeated invocations on one daemon, including after update/rollback.
- Read bound vault context (`vault/*` routes, `packages/roster/src/vault/`; the name "task-vault" appears nowhere in source), implement in a private linked worktree, run actual checks and commit locally. Deliver Findings/Plan/Result/History/chat before durable Completed.
- Fence current coding claims, native producers, manifests, budget and credential grants across restart. Missing current work output fails; it never falls back to host completion.
- Advertise readiness only for the qualified CLI/adapter/sandbox/platform/host tuple; report actionable startup/auth/quota/policy failures to the invoker.

## How to get to it (user POV)

Open the local daemon's **/rooms**, choose **Agents**, then create/import, review and install a supported text agent. Grant the intended channel and mention it there. **Try** is a private preview.

Publish as A and review/adopt as B in a separate signed-in home. Review/apply changed knowledge or a changed skill phrase, invoke that release, revoke it, verify refusal, and review/apply rollback before invoking again. Populate private memory only through normal consent. B should receive shared package bytes without A's memory, overlays or credential.

For work, use a feature template and linked repository. Open **Review Plan**, read the bound context and proposed changes, then **Approve Plan** and **Start approved work**. Follow automatically refreshed Work, recorded proof, local delivery history and the Run Topic reply.

## Driving it with control-om

### Guest lane on main (driven 2026-10-27)

A plain lane carries the roster. `OM_DEV=1` goes on each CLI call, not on
`up`: `control-om om` passes the caller's environment through, and the verbs
register in the CLI process. **There is no `--format json`.** Every
`roster`/`agent runs`/`project` verb prints a JSON envelope unconditionally,
except `roster list` (a tab table); only `agent steer` takes `--json`. Without
`OM_DEV`, `om agent runs` fails with `unknown command 'runs'; did you mean
'grants'?`, because the non-dev `om agent` (credentials, docs, grants, ...)
still exists.

```sh
curl -fsS "$(control-om url /healthz)" | jq '.roster.capabilities.executors'   # ["coding","investigate"]
OM_DEV=1 control-om om -- agent runs                 # {"ok":true,"result":{"items":[],"next":null}}, exit 0
OM_DEV=1 control-om om -- agent runs run_x --proof   # not_found "Work proof was not found.", exit 1
OM_DEV=1 control-om om -- agent runs --proof         # malformed_body "Run read command is invalid.", exit 1
OM_DEV=1 control-om om -- agent pause nope           # not_found "Work run was not found.", exit 1 (cancel likewise)
OM_DEV=1 control-om om -- roster list                # header NAME ORIGIN VERSION BRAIN; rows only for defaults that installed (none while the registry lists no @om-skills)
OM_DEV=1 control-om om -- roster measures            # zeroed queueLatencyMs, orphanRate, spendUsd, ...
OM_DEV=1 control-om om -- project unlink nope        # not_found "Project was not found.", exit 1
curl -fsS "$(control-om url /rpc/v1/roster/projects)" # {"ok":true,"result":{"items":[]}}
```

Create/import, Try and install are HTTP routes the GUI calls (`imports/*`,
`local-packages/*`, `builder`, `instances/:id/try|shadow`), not CLI verbs.
"Review Plan" and "Approve Plan" are GUI labels over `GET work/runs/:id/plan`
and `POST .../plan/decision`. Anything past a refusal needs an installed agent,
an LLM credential or coding brain, and an account. `roster drive --once` and
`roster conformance` are a fake-brain dev harness, not product proof.

### Default agents from `@om-skills` (driven 2026-10-28)

After the roster starts, a background pass installs any of the eight
`@om-skills/*` defaults the home lacks. It runs for a guest too, because a
minted guest key resolves to an owner. Before the mint lands, the reason is
`no owner is signed in`. Boot and `/healthz` never wait on this pass, and
`/healthz` `roster` is still `{capabilities}` with no install state. Read
the lane log:

```sh
grep '\[roster\] om-skills' .control-om/lane-<port>.log
```

- **Production, 2026-10-28:** `ERROR [roster] om-skills defaults unavailable
  (registry lookup failed (404) for https://registry.openmarket.xyz/v1/packages/%40om-skills/argue/summary:
  no such resource); retrying in 30s`, then 60, 120, 240 and 480 s (the cap
  is 30 min). `roster list` stays header-only.
- **Success line, per source:** `om-skills defaults installed N package(s)`.
  A permanent refusal reads `om-skills default <coord> refused (<code>)` and is
  not retried. A 403, 404 or 5xx is retried; only a 410 or a suspension is
  permanent.
- **Another registry (per source; not driven):** `OM_ROSTER_REGISTRY_URL` is read by the daemon, so pass
  it on `up` (`--env`), not on the CLI call. Plain `http` is accepted only on a
  loopback host. It falls back to production, not to `OM_REGISTRY_URL`.
  `OM_ROSTER_OM_SKILLS_MAINTAIN_MS` (minimum 1000) shortens the six-hour
  maintenance pass on a source lane.
- The old `bundled snapshot installed N package(s)` line no longer exists.

### Historical branch closeout (not re-driven on main)

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

Recorded Claude C6 (historical native execution) source320/reply324 quoted the bound Birch compass1007 guide in Findings, recovered a controlled pre-manifest daemon interruption on the same a2/e2 with successor lease4 and one current manifest, natively made README commit4268dcd9, passed16focused tests/build and all5required checks, delivered all5effects once, and became Completed. Original20-minute budget and actual135165ms human pause were preserved; native proof sealed before deadline. Total journey1850.05s exposes slow finalization. Phrase placement in Findings rather than Plan remains a minor task-instruction deviation.

Recorded Codex X4 (historical native execution) source325/reply327 read Maple harbor1007 from the bound guide, obtained normal owner approval, natively made README commit0842322d, passed16focused tests/build and all5checks, delivered all5effects once and became Completed. Its original20-minute budget,43624801ms overnight human approval pause, a2/e2 and two total manifests remained intact. Automatic publishing lease handoff retained the same attempt and produced no duplicate effects. Do not interpret the overnight approval pause as model runtime.

Recipient S2 source322/reply323 on daemon635 called actual skill_read/post_reply, read Juniper ribbon1007 from knowledge/README.md and delivered one84-character reply as the independent dboon_ref user. Historical b1c restart retained C6/X4 completed states and five first-attempt effect receipts each without duplicates. The positive tasks are bounded README changes, not arbitrary feature-implementation certification.

Historical sharing on GUI29e414ad/daemon7f7304243 proved two identical recipient installations converge to one, Juniper guide execution, reviewed0.2 Willow update,0.1 Cedar rollback, and exact0.2 revocation with0.1 preserved. Historical desktop/phone pending-review replay on GUI087/daemonb1e93b1 reused package/approval without another installation or event.

Historical source stamps: repeated selected-release skill reads used39e94a54f; D5adoption/execution used335a63073; revocation/refusal/rollback and restoredD4 used288f6e0fb80f251aaa8fca7a56b4281d5b58d7e8 / binary68ef77883432db56c72e16f4359cfeea1e952edfb31791d26a85489c35ea07a7 / GUI1c11e331; restart-refusal deduplication also retains9cb0f2660 evidence.

Earlier source-specific proofs remain historical: Codex261/Claude263 on d24bded8f read vaultrev1, edited only README, passed12tests/24assertions and build, committed locally, delivered Resultrev2/Historyrev3 and one reply. D4 sources272/274 returned forest cabin1005 as273/275; D5 source276 returned amber canoe1005 as277; revoked278 received279; rollback280 returned forest cabin1005 as281. D4/D5 six-file packages matched across profiles; publisher memory/overlay2/1 and recipient0/0 with different owners. These counts alone are not a complete authorization proof. Gallery agent-creator-20261002/r05 retains the original source stamps.

## Gotchas

- C5 ended cleanly in ACP but returned a new Plan without edits/current output. Its failure remains immutable. The prompt repair explicitly says the owner already approved and to execute now without replanning; C6/X4 prove that repair without weakening work_stage/work_commit/checks.
- Cancelled old C4/X3 retain their original budgets, receipts and native commits. One readable timeout notice was delivered for each. X2 correctly refused a passing debugger baseline before native edits and delivered one actionable notice. A successful successor does not relabel these failures.
- A reply or five delivered effects can precede the authoritative Completed transition while receipt/worktree finalization runs. Preserve a sealed successful native proof and original ledger; do not kill an active supervisor solely because progress is quiet.
- Claude2.1.278/ACP0.76.0/Opus4.6 and Codex0.153.4/ACP1.11.0/gpt-6-astra used restored subscriptions on macOSarm64. New global clients, other models/platforms, arbitrary executable harnesses and implicit private-host skills remain unqualified.
- Current daemon qualification passed full 6,144 MB typecheck, lint and build on the final revision and 1,484 selected test executions / 7,557 assertions, including 17 compiled credential tests. The first generated-contract prerequisite and incoming-main matcher typing failures were repaired; initial red receipts remain. An earlier qualification harness paused on a generated Bun executable, then continued only unrun rows with unchanged HEAD/tree; the final compiler and affected fixture gates are fresh. Groups 1–6 retain explicit source receipts for unchanged modules; changed preflight and remaining groups were fresh. Recovery/preflight fixture timing failures were repaired without a longer timeout or weaker guard. This is affected lifecycle coverage, not the entire daemon suite.
- Historical parent integration b1e93b1 passed1,258tests plus17compiled credential tests; prompt-only635 passed261affected tests/1,302assertions and full canonical typecheck/lint. Originalfe3repair remains preserved with561tests/2,962assertions. Never substitute an earlier default-heap OOM or8GB source-only run for the current6144MB gate.
- Release revocation differs from the publisher's own local installation. Current-run skill resolver binding is required across repeated invocations; a cached first-run resolver once caused a false refusal and was repaired without weakening its guard.
- Historical e08d96f0f catalog authority batching retains local owner checks around every read and a final remote membership refresh for at most three revisions. Its153tests/579assertions and full typecheck/build/Biome pass are source-specific. Fixture request budgets are not public backend quotas; catalog retry budget limits sleeping, not total wall time. Earlier throttled selections and uncertain publication readback remain failed/uncertain, despite later successful selections/adoption.
- Historical broad430-file roster diagnostic remains failed/incomplete after an ACP fixture timeout (754observed passes). Injected-clock stabilization passed100focused ACPcontracts/494assertions; production timeouts stayed unchanged. Terminal publication matrices retain their exact original source/binary stamps.
- Historical paid orders/change passed on335a63073. Doors initially failed4/43, with the ECB prompt boundary unresolved. Full compose remains FAIL21pass/7fail/218assertions, canonical88PASS/13FAIL/24BLOCKED. Watches remains10pass/47fail/523assertions across57registrations. Selected unchanged-main W05/W08/W14 also failed; that does not establish full-suite causality. Partial J9–11/F2 diagnostics4tests/127assertions do not replace these failures or prove actual scheduling.
- Historical private eval d1313c251 reads delivered composer journal text;37focused checks/436assertions passed. Its29live-disabled registrations are not model proof. Failed/empty deliveries and wrong links/counts remain failures.
- Fresh 8,192 MB knip advisory remains nonzero: 35 unused files, 1 dependency, 4 devDependencies, 21 unlisted dependencies, 6 binaries, 410 unresolved imports, 3,282 exports, 1,286 exported types, 22 duplicate exports and 4 configuration hints. Five reported roster fake files were traced to explicit string-path test reads/spawns and retained. Generated/vendor imports and exported APIs contribute reports; no blanket clean scan or zero-feature-added claim. The older 76-finding comparison and 275-file archive scan remain historical. Registry roster.1 is privately published and clean-installed; all current GUI pins/root lock use it, `latest` remains `0.103.0`.
- Current GUI full gates:rooms 16,579 pass / 0 fail / 2 pre-existing unrelated skips; cloud 16,809 pass / 0 fail / 0 skip. The shared creator stays visible without a ready provider and disables Work review with install/sign-in/refresh guidance. Hosted creation remains local-only. Static Markdown,10-second single-flight polling, disclosure/focus retention and stale-boundary clearing remain covered. Chromium phones are not native WebView certification; hosted contrast audits retain incomplete checks.
- control-om om binds the owned home/port; control-om cli is generic. An older accidental operator model change remains disclosed with original value unknown. Main allowance and routed pool capacity are separate; pause before starting a new task below10% remaining.
- Normal account-browser posts/catalog actions in local_longan_storage are authorized. Map-only sync is separately authorized. The current restricted preview publication and feature-branch pushes were explicitly authorized and completed; main merge, deployment and release remain unapproved. Original worktrees, homes and failed receipts are preserved. No Tharamine/relay changes were needed in this pass.

- Current qualified restart of both owned homes retained C6/X4/S2 Completed with unchanged attempt/epoch/revision, original manifests and first-attempt effects: 5/5/1. Zero active runs and no duplicate effects. This proves current persistence/readback, not a new native model execution.

- Remote CI remains unverified: three GitHub Actions workflows stopped before runner allocation or any step because of the account billing/payment or spending-limit block. Local gates passed, but the review is not merge-ready until the account owner restores Actions capacity and remote checks run.

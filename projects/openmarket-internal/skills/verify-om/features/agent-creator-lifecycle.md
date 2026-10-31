# Agent creator lifecycle and private-state isolation

*Re-driven 2026-11-01 (nightly), tree `7ce379c45` (origin/main, v0.480.3), lane on 18163 (`OM_FEED_ALLOW_LOOPBACK=1`, `OM_FEED_POLL_INTERVAL_MS=60000`), host load average about 2.9. About 6 s after boot the lane log read `[roster] om-skills defaults installed 8 package(s)`; `OM_DEV=1 roster list` listed six registry rows at 1.0.0 (`argue`, `debugger`, `explain`, `fact-check`, `feature`, `librarian`); `OM_DEV=1 agent runs` `{"ok":true,"result":{"items":[],"next":null}}`; `agent runs run_x --proof` → `not_found` `Work proof was not found.` (exit 1); `agent pause nope` and `project unlink nope` → `not_found` (exit 1); `roster measures` zeroed; without `OM_DEV`, `agent runs` → `unknown command 'runs'; did you mean 'grants'?`; `GET /rpc/v1/roster/projects` `{"ok":true,"result":{"items":[]}}`; `/healthz` `roster.capabilities.executors` `["coding","investigate"]`. The runs, project and GUI paths were not re-driven. Evidence: `http://127.0.0.1:8098/vom-nightly-20261101/r1/` (`cli/78-79f`, `cli/19c`).*

*Re-driven 2026-10-31 (nightly), tree `dfefe0a21` (origin/main, v0.480.2), lane on 18163 (`OM_FEED_ALLOW_LOOPBACK=1`, `OM_FEED_POLL_INTERVAL_MS=60000`), host load average about 1.6. About 4 s after boot the lane log read `[roster] om-skills defaults installed 8 package(s)`; `OM_DEV=1 roster list` listed six registry rows at 1.0.0 (`argue`, `debugger`, `explain`, `fact-check`, `feature`, `librarian`). The runs, project and GUI paths were not re-driven. Evidence: `http://127.0.0.1:8098/vom-nightly-20261031/r1/` (`cli/78-79`).*

*Verified: 2026-10-29 (nightly), tree `32ca0d6c7` (origin/main, v0.467.0), lane on 18103, guest. **The default agents now install from production.** Since #2183 (`d79e522f4`) the coordinates are `@om-core/*`. About 5 s after boot the lane log read `INFO [roster] om-skills defaults installed 8 package(s)`. `OM_DEV=1 roster list` then listed six registry rows at `1.0.0`: `argue`, `explain`, `fact-check` and `librarian` with brain `om`, and `debugger` and `feature` with `-`. The two skill packages are not roster rows. `agent runs` was still empty. Not driven: the six-hour maintenance pass, a withdrawal, and everything past the guest refusals (create/import, Try, install, publish/adopt, runs and the GUI). Evidence: `http://127.0.0.1:8098/vom-nightly-20261029/r1/`.*

*Re-driven 2026-10-28 (scheduled maintenance, smoke depth), tree `186030b63` (origin/main): `OM_DEV=1` `agent runs` (`{"ok":true,"result":{"items":[],"next":null}}`), `agent pause nope`, `agent runs --proof`, `agent runs run_x --proof`, `project unlink nope` (each with its documented refusal, exit 1) and `roster list`. `/healthz` executors were `["coding","investigate"]`. Without `OM_DEV`, `agent runs` fails with `unknown command 'runs'`, as documented. Steps not named here keep the record below. Evidence: `http://127.0.0.1:8098/verify-om-maint-20261028/r1/`.*

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

> **Work agents on 0.467.0 (driven 2026-10-28/29 on an isolated lane).** Under
> launchd's PATH, Brains reports Claude Code "Not installed", the version pins
> qualify no real machine, and several later steps fail silently. The fixes are
> in PR #2199 (daemon) and openmarket-chat MR !136 (GUI), unmerged at this
> writing; see "Running a work agent end to end" below.

*Closeout verified 2026-10-12. GUI `194281a1dbe02b29ca6542170a704d1726884a09`, daemon `a3a81a5f5192a3786c46e0dc3e7e911c2cb86f7c`, binary `5085976c818d929c64fc9fec15efefc5f7a537d3cd7be3b6f221044dd378f8bb`. Native C6/X4/S2 executed on daemon `635441fb083971c1ff5143835521d5c8193e60c2`, binary `7e7f8ee1e25556d1cc75ad61e0d3f4f240dd0715331a52d4d33f8e71067af213`; current viewing and restart readback are distinct. Root-reviewed gallery `agent-creator-stress-20261007/r03` is operator-local evidence. Private registry installation is qualified. Review requests: https://gitlab.com/openmarketxyz/frontend/openmarket-chat/-/merge_requests/75 and https://github.com/openmarket-xyz/openmarket-internal/pull/1948. Local gates passed, but three daemon workflows received no runner or steps because GitHub Actions is blocked by account billing or spending limits. Ready for review, not merge-ready; no main merge, deployment or release.*

The daemon owns release, installation and account state. Shared text packages have immutable digests. Recipients use their own credentials, notes and private memory. An invocation completes its task or clearly explains why it cannot run. Supported local text-agent/Agent Skills creation and sharing are distinct from arbitrary third-party runtime admission.

## Sub-features

- Install the eight default agents and skills (argue, debugger, explain, fact-check, feature, librarian, agent-builder, clanker) from `@om-core` registry packages (`@om-skills` until #2183), live behind a notice, in the background after boot; keep them current every six hours and honour a registry withdrawal (#2167). The signed bundled snapshot is gone (#2169).
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
OM_DEV=1 control-om om -- roster list                # header NAME ORIGIN VERSION BRAIN; one row per installed default agent (six on 2026-10-29: argue, debugger, explain, fact-check, feature, librarian)
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

### Default agents from `@om-core` (driven 2026-10-28 and 2026-10-29)

After the roster starts, a background pass installs any of the eight
`@om-core/*` defaults the home lacks (the scope was `@om-skills` before #2183; the log lines still say `om-skills`). It runs for a guest too, because a
minted guest key resolves to an owner. Before the mint lands, the reason is
`no owner is signed in`. Boot and `/healthz` never wait on this pass, and
`/healthz` `roster` is still `{capabilities}` with no install state. Read
the lane log:

```sh
grep '\[roster\] om-skills' .control-om/lane-<port>.log
```

- **Production, 2026-10-29 (`@om-core`):** `INFO [roster] om-skills defaults installed 8 package(s)` about 5 s after boot, on the first pass. `roster list` showed the six agents.
- **Production, 2026-10-28 (old `@om-skills` scope):** `ERROR [roster] om-skills defaults unavailable
  (registry lookup failed (404) for https://registry.openmarket.xyz/v1/packages/%40om-skills/argue/summary:
  no such resource); retrying in 30s`, then 60, 120, 240 and 480 s (the cap
  is 30 min). `roster list` stayed header-only. A retry line like this now means
  the registry is unreachable or no longer lists a default.
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

### Running a work agent end to end (PR #2199, verified 2026-10-29)

Verified live on lane 18124 with launchd's PATH, Claude Code 2.1.312 and Bun 1.4.3, signed in as a test account. A debugger agent fixed a one-line bug, committed only that file, passed the work proof and replied in its run topic. Each step below was a separate silent failure before #2199:

- **Brains.** Detection searches PATH, then `~/.local/bin`, `~/.claude/local`, `~/.bun/bin`, `~/.npm-global/bin`, `/opt/homebrew/bin` and `/usr/local/bin` (`OM_BRAIN_SYSTEM_DIRS` replaces the last two; tests set it to ""). Rows are built from the detected CLI, not pinned versions. Executables up to 1 GiB are hashed.
- **"Signed in"** means OM's own model credential resolves for the brain (`om llm status`, profile `anthropic:claude-cli` for "Use Claude Code login" from `om init`). Claude Code's own login alone shows "Signed out", and the Brains hint pointing at `claude` does not fix it.
- **Sandbox.** The agent sandbox must allow reading `/private/var/db/timezone`. Without it, Claude Code 2.1.312 hangs at `sdk-initialize` and the run fails with `ACP session/new timed out after 30000ms`.
- **Broker betas.** The Claude broker forwards every `anthropic-beta` the client sends (OAuth added once). A dropped beta whose body field remains gives a 400 on that field, and the owner sees "couldn't verify the model provider's usage report".
- **Clean commits.** The ACP file helper runs with `BUN_RUNTIME_TRANSPILER_CACHE_PATH=0`; otherwise a `Library/Caches/bun/@t@/*.pile` lands in the worktree, and the proof refuses with "binary committed changes are unsupported".
- **Checks.** `tests-pass` and `build-passes` apply only when the project records that command.
- **Owner notices.**
  - A debugger agent on a project with no test command is told to add one (`test_command_missing`).
  - Linking a checkout with no `origin` is refused by name (`project_not_allowed`), and MR !136 shows that text in Projects.
  - A work mention refused for an owner-fixable reason (`project_unlinked`, `no_grant`, `project_not_allowed`, `mode_off`) keeps waiting and retrying, but gets one threaded reply: "I can't start this yet: … I'll start once that's fixed." The reason and its sent marker live in `roster_idempotency` (routes `roster-intake-waiting-notice[-sent]`), because invocation correlation keys are fixed.
  - A 403 `LIBRARY_UPLOAD_FORBIDDEN` on the task page becomes `no_grant`, naming the Upload to Server Library permission.

Recipe: link a git repo that has an `origin` remote and a failing test command, create a work agent (Claude) and grant it the channel. Then mention it as the owner in a channel of the project's server. Read progress from `roster_agent_events` (read-only) and the run topic. On the first failure, check the run's correlation for `coding_preparation_failure`, `acp_failure` and `supervisor_usage_failure` before guessing.

To capture a sandbox launch, log `prepareAgentSandbox`'s profile and parameters (diagnostic only). Then replay them with a stdio ACP probe, using a fake proxy for the gateway. Bisect allow rules (`--rule`) to find a missing read.

### Re-proved 2026-10-30 on main fe18809be (0.478.0), GUI 936f5b64

Lane 18124, test account, launchd PATH, compiled with Bun 1.4.3, Claude Code 2.1.314.

- Brains: Claude Code 2.1.314 signed in, verified, coding ready. Claude auto-updated from 2.1.312 overnight and still qualified, with no version pin.
- GUI creation: New agent > Work agent > debugger template, then project, brain and name, then Review agent > Add. The card says "Installed in shadow mode", and the Run switch is on. Access > channel > Allow grants it.
- Work run: a new agent's first mention completed in 482 s. Its commit changed only `math.mjs`, the work proof passed, and the reply was threaded under the mention. The two `doc_write` effects took 142 s and 130 s, more than half the run. That run started 3 minutes after lane boot, inside the worktree-sweep relearn window.
- Chat agent: `@argue` completed in 36 s. Round 1 failed only `max-chars:1500`, and the retry passed all four checks.
- Waiting notice: it posts only where the agent's credential has `canPost` in that room (`waitingInvocationTarget` in `provider-limit-notice.ts`). Mentioning your own agent in a channel it has no grant for gives no reply, no Inbox item and no Needs you entry. The mention retries on the 1–5 minute backoff indefinitely. After a grant, the notice posted about 7 s later.
- The Access tab cannot remove a single channel, and the picker disappears once every channel is granted. Revoke with `om agent grants revoke <agcr_…> room:<roomId>` (the credential id is in `om agent grants list`).

## Gotchas
- Main pins Bun 1.4.3 (`.bun-version`). An `om` compiled with Bun 1.3.14 under `OM_SKIP_BUN_CHECK=1` dies with SIGTRAP when `__roster-acp <brain> --version` runs inside the probe sandbox. Brains then reads "not set up" (`support: unverified`, `signIn: unknown`) for both brains. Build with the pinned Bun; the release binary passes the same probe.
- On the final #2199 build, one of two runs failed after its commit with no recorded cause while the lane's roster-sweep was timing out; the rerun completed. Unexplained; under load the outbox also stalled about 5 minutes before publishing.
- A test account hammered by restarts and a looping intake gets 429 "You're reading too fast". The /rooms server rail then never finishes loading. Open a channel directly with `/rooms/#/room/<roomId>`.

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

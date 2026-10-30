# Agent creation, import and sharing

> **On origin/main since `01bf4481` ("Add agent creation, sharing and guided
> work setup", 2026-10-26).** `AgentCenterSurface.tsx`, `components/roster/`
> and the `lib/roster-*.ts` helpers are on main, with every label this guide
> names: **Review agent** (`roster/RosterCreateForm.tsx:1359`), **Choose a
> brain** (`:1234`), **Install in shadow mode** (`roster/RosterCatalogPanel.tsx:1166`),
> **Apply update** / **Apply rollback** (`roster/RosterCatalogTransitions.tsx:785`),
> **Review Plan** / **Approve Plan** / **Start approved work**
> (`roster/RosterWorkPlan.tsx:394`, `:453`, `:477`), **View recorded proof**
> (`roster/RosterWorkProof.tsx:252`), **View delivery history**
> (`roster/RosterWorkDelivery.tsx:158`), and `Access for <name>` / `Work for
> <name>` (`roster/RosterAccess.tsx:108`, `roster/RosterWorkRuns.tsx:734`).
> `roster/RosterShelf.tsx` was deleted in `3e9c88f3`, when the Agents page
> moved to Map and Grid (see [om-and-agents.md](om-and-agents.md)). The landing is a subset of
> the branch `daryl/agent-creator-migration-20261007`: that branch still holds
> ten commits main lacks (tip `a0916a25`, "explain sample questions before
> agent review"). The account-lane receipts below were recorded on the branch
> and have **not** been repeated on main; on main only the fixture record at
> the end of this file applies.

*Closeout verified 2026-10-12. GUI `194281a1dbe02b29ca6542170a704d1726884a09`, daemon `a3a81a5f5192a3786c46e0dc3e7e911c2cb86f7c`, binary `5085976c818d929c64fc9fec15efefc5f7a537d3cd7be3b6f221044dd378f8bb`. Native C6/X4/S2 executed on daemon `635441fb083971c1ff5143835521d5c8193e60c2`, binary `7e7f8ee1e25556d1cc75ad61e0d3f4f240dd0715331a52d4d33f8e71067af213`; current viewing and restart readback are distinct. Root-reviewed gallery `agent-creator-stress-20261007/r03` is operator-local evidence. Private registry installation is qualified. Review requests: https://gitlab.com/openmarketxyz/frontend/openmarket-chat/-/merge_requests/75 and https://github.com/openmarket-xyz/openmarket-internal/pull/1948. Local gates passed, but three daemon workflows received no runner or steps because GitHub Actions is blocked by account billing or spending limits. Ready for review, not merge-ready; no main merge, deployment or release.*

## Sub-features

- Create local chat or work agents with explicit owner identity, supported brain and linked project. Private chat Try does not implement a work task.
- Preview supported text-agent and Agent Skills imports, including provenance, omissions, reviewed knowledge, skills, access and locked checks. Arbitrary executable harnesses and scripts are outside this release.
- Review before Add or shadow installation. An identical unfinished review reopens the same package and approval; conflicting content refuses. Normal desktop/phone replay on GUI087/daemonb1e93b1 reused the pending review without another installation or event.
- Publish on the test server, review/adopt as a separate authenticated user, and converge two identical installation actions to one instance.
- Review changed knowledge, skill, definition and capabilities before updating or rolling back. Exact-release revocation removes its installation action while preserving other versions.
- Read the selected release-local guide on invocation and send one readable reply. Historical update/rollback/revocation proof used GUI29e414ad/daemon7f7304243. Historical recipient S2 read the adopted guide and replied once on daemon 635441fb.
- Review a channel task's formatted Plan, then approve and start native Claude or Codex implementation. Each recorded positive task edited only README, ran actual checks, committed locally, delivered all five effects once and became durably Completed.
- Show readable Plan/Result/History Markdown without activating embedded media or executable blocks. Work progress refreshes automatically while visible, and progress revisions preserve open proof/delivery details and focus. Account, client, attempt, epoch and delivery-state changes still invalidate stale views.
- Keep Agent Center visible without configured Claude Code or Codex. Show install/sign-in/verification guidance; disable Brain and Work review until a supported coding-ready provider is connected. Unsupported Work remains visible and disabled without unauthorized RPCs. Hosted `/chat/` shows an **Agent management** section headed **Your agents** that reads "Create and manage your agents in the local app. Agents connected to this server appear here." (`AgentCenterSurface.tsx:287-290`; it renders when roster support is off and the host has no daemon features).
- Run, try and tune an installed agent from its Grid card or its own page (`agents/AgentGridCard.tsx`, since `3e9c88f3`; the roster shelf is gone). Each has one `switch` named **Run <name>** (`AgentGridCard.tsx:41`) and a **More actions for <name>** menu (`:77`) holding **Review replies first**, **Check routing** and **Review what it learned** (`agents/AgentsHome.tsx:242`). On the agent page (`#/agents/a/<id>`) the region **Talk to <name>** holds the textbox **Ask <name> something** and **Try it**, and the tabs Overview / Activity / Access / Settings carry the access and work details. Live verified 2026-10-30 on `agent-center-fixture` (argue).
- Approve or keep a pending `@om-skills` update (`roster/RosterUpdateNotice.tsx:78-103`, since `c70fdd28`). Since `3e9c88f3` it renders in the **Needs you** feed (`agents/NeedsYou.tsx:872`), not on a card. A `section` named **Update for <name>** titled "Update to <toVersion> needs your OK" lists the changes, with **Approve <name> update** (visible text **Approve**) and **Keep <name> at <fromVersion>** (visible text **Keep <fromVersion>**). While the answer sends it shows `role=status` "Sending your answer..."; a refusal shows `role=alert`. The Map's ask card for it offers **Review, <name> wants to update to <version>** and **Keep <name> at <fromVersion>**. Live verified 2026-10-30 on `agent-center-fixture` (**Update for argue**); the answer was not sent.

## Agents map: brains and projects

- Agents now opens on **Map**, with **Grid** as the alternative view. The Brains and Projects setup panels open from map nodes. **Link a project** (the + on the Projects node) appears only while no project is linked. With a project linked, no map control reaches the link form.
- A project link or edit refused with a `fix` shows the daemon's text and fix as written. For example: "This checkout has no origin remote. Add one with git remote add origin <url>, then link the project again." Refusals without a fix keep "The project request was refused. Refresh and try again." On origin/main since `40d509cf` (`roster/RosterProjects.tsx:436-445`); the no-origin refusal itself needs daemon PR #2199. No fixture reaches a refusal: `agent-center-fixture`'s `/rpc/v1/roster/projects` route only answers success. The live proof is the branch lane screenshot `om-agents-live-e2e/run-artifacts/42-no-origin-refusal.png`, taken before the merge.
- The Brains card's "Signed in" reflects OM's model credential, not the `claude` CLI login. See verify-om `agent-creator-lifecycle.md`, "Running a work agent end to end".

## How to get to it (user POV)

Open the local daemon's **/rooms**, choose **Agents**, then **New agent** (or **Templates**). Pick **Chat agent** or **Work agent** and a template (or **Start blank** for chat), then **Continue** to the **Create an agent** form, or **Import** to import. **+ Wire an agent** opens Agent Settings; it is not the creator entry point. Without a coding-ready brain, open the **Brains** panel (a region named "Brains" with **Refresh brains**; each provider has an **Install <provider>** disclosure and a **Copy sign-in command for <provider>** button, `roster/RosterBrains.tsx:122-192`), install the tested provider version, complete its browser sign-in, then refresh Brains for a strict compatibility check. Credentials stay with the provider and are never entered in OM. Work stays inspectable but Brain and Review are disabled. Work creation selects a linked project and supported brain. Choose **Review agent**, read access and checks, then **Add**. Grant the intended channel under **Access for <name>**, then mention the agent there.

To share, publish a version on the test server from the publisher profile. As a different signed-in user, open the catalog, choose the release, review its digest/files, and **Install in shadow mode**. Review before updating or **Apply rollback**. A revoked release must expose its state and remove installation actions.

For a coding task, open **Work for <name>**, then **Review Plan**. Read the Plan before **Approve Plan** and **Start approved work**. Follow the automatically updating row, **View recorded proof** and **View delivery history**. Completion includes committed work, required check results, Result/History and one channel reply; an early commit or reply alone is insufficient.

## Driving it with control-om-chat

Run the wrapper from the intended GitLab GUI worktree and its assigned port. The fixture proves rendering and capability limitations; authenticated daemon lanes prove creation, sharing and execution.

The shell fixture does **not** reach the creator: `?view=agents` there scripts
no roster host and shows only the `your om` card and **+ Wire an agent**. The
creator's fixture door is `tools/visual/agent-center-fixture.html`, which
seeds a roster host (`tools/visual/agent-center-fixture.tsx:803`) over
scripted `/rpc/v1/roster/*` routes (`:295-299`). Since `3e9c88f3` it takes no
`roster=` state other than `none`; reach the form through **New agent**.

| Route (`agent-center-fixture.html?…`) | What renders (driven 2026-10-30 at `47cb13bf`) |
|---|---|
| (none) | The Agents page on **Map** (see [om-and-agents.md](om-and-agents.md)). **New agent** → **Work agent** → **Continue** opens **Create an agent** with **Start from debugger** / **Start from feature**, **Refresh setup**, "Brains service is unavailable. Check the Projects and Brains panels, then refresh setup.", and empty **Project** / **Brain** selects (fixture gap below). |
| `connections=none` | **New agent** → **Work agent** → **Continue** shows the region **Brains** ("OM daemon · no work brain yet", **Refresh brains**, "Connect and sign in to Claude Code or Codex to enable work agents. Use the setup instructions, then refresh Brains.") above **Create an agent**, which reads "Connect and sign in to Claude Code or Codex in the Brains panel, then refresh setup." with **Review agent** disabled. No roster mutation is recorded. |
| `roster=none` | No roster host: om and the connected agents only. |
| `roster=work-builder`, `roster=projects`, `roster=work-proof` | **Retired.** The fixture compares `roster` only to `none`, so these render the default. |
| `#/agents/a/<id>` | An agent's own page (e.g. `inst_argue`); `#/agents/badge/<id>` rewrites here. |

```sh
OM_CHAT_LANE_PORT=<assigned-port> control-om-chat doctor
agent-browser open "$(OM_CHAT_LANE_PORT=<assigned-port> control-om-chat url 'tools/visual/agent-center-fixture.html?connections=none')"
agent-browser find role button click --name "New agent" --exact
agent-browser find role button click --name "Work agent" --exact   # hides Start blank, picks a work template
agent-browser find role button click --name "Continue" --exact     # -> Create an agent, Brains guidance
```

The fixture records every roster request in
`document.documentElement.dataset.fixtureRosterRequests`, and any non-GET under
`connections=none` in `dataset.fixtureUnexpectedRosterMutation`. Read those to
prove which calls a click made. **Review agent** posts
`POST /rpc/v1/roster/local-packages`, which the fixture does not script, so the
review, **Try <name>** and **Add** steps need a daemon lane.

Use the hosted fixture below `/chat/` in a separate browser session on its assigned port. Check desktop and phone widths, readable local-only management copy, console, axe and keyboard rail navigation. Current two-host fixtures have zero browser errors and axe violations. Local and no-provider checks have zero incomplete results; hosted contrast retains one incomplete rule (eight phone gradient or decorative nodes). The older r02 contrast results and focused tooltip landmark warning remain historical.

Use independently authenticated publisher and recipient homes for server behavior. Authorized normal account-browser posts in `local_longan_storage` avoid the MCP badge's consecutive-post limit; do not ask for human `ready` loops. Correlate the actual source message, watcher run, release digest, current attempt and one delivered reply. Never mutate the live database to manufacture proof.

Recorded native proofs (historical execution): Claude C6 source320/reply324, local commit4268dcd9; Codex X4 source325/reply327, local commit0842322d. Each had 16 passing focused tests, a successful build, five passing required checks, all five effects delivered once and durable Completed. C6 additionally recovered a controlled pre-manifest interruption with the original attempt/epoch/budget and one successor current manifest. X4's overnight human approval pause is preserved, not charged as model runtime. Current qualified daemon restart retained C6/X4/S2 completions and no duplicate effects. Recipient S2 source322/reply323 called skill_read/post_reply and named knowledge/README.md.

## Gotchas

- The ordinary source fixture still lacks authenticated creator/catalog prerequisites. Its apparent reachability is not full creator verification. The earlier a0916a25 route-only record remains historical, superseded for daemon-backed claims by the explicit account-lane receipts above.
- **The default `agent-center-fixture` brains seed still fails the client's validation** (a fixture gap in the product repo, not a product bug; re-confirmed 2026-10-30 at `47cb13bf` on rooms-client 0.108.0). The connected seed (`agent-center-fixture.tsx:93-142`) lists only `om` and `codex`, but the brains client accepts a page only with exactly `om`, `claude` and `codex` in that order (`rooms-client/dist/roster/brains-client.js`, `validPage`). The route answers 200 with that body, and the client turns it into "Brains service is unavailable." So on the default fixture **Work agent** → **Continue** shows that line with empty Project and Brain selects. Only `connections=none`, whose seed has all three rows, renders the full Brains guidance. The old `roster=projects` and `roster=work-proof` failures went away with those states in `3e9c88f3`.
- **The agent cards and the update notice now render in the fixture** (since `3e9c88f3`). `agent-center-fixture` seeds chat, work and connected agents and a pending update for argue, so **Run <name>**, **More actions for <name>** and **Update for <name>** are drivable there. Toggling **Run** and answering the update are fixture-local and prove no daemon effect.
- The catalog (Install in shadow mode, Apply update / rollback) mounts only inside `AgentCenterSurface`'s vault section. No fixture reaches it.
- A button and section both have **Work for <name>**. Read `section[aria-label="Work for <name>"]`; a generic aria-label selector can hit the button.
- Current `agent-browser press` accepts only the key. Focus the composer and then `press Enter`. Verify durable source message and watcher run, not a Done response alone.
- Setup and Work lists load asynchronously. Wait for actual nonempty project/brain selections and current row buttons. Viewport changes can remount the form or Plan; reopen using fresh controls. Scroll phone targets into view before clicking because the sticky footer can intercept them.
- Native agents receive bound task-vault/package context. Private host clanker-mode skills are not automatically imported. Import a supported self-contained guide explicitly; unavailable direct/private reads must remain disclosed.
- Runtime qualification is exact. This pass used macOS arm64 Claude2.1.278/ACP0.76.0/Opus4.6 and Codex0.153.4/ACP1.11.0/gpt-6-astra with subscriptions. Auto-updated global clients, other models/platforms and arbitrary harnesses remain unqualified.
- A feature task needs the feature template. Debugger correctly refuses a passing baseline and gives an actionable choice. Failed C5 replanning and cancelled old C4/X3 runs remain failed/cancelled; successful fresh runs do not relabel them.
- Server write/readback and finalization were slow. Native proof can seal before a runtime deadline while delivery finishes later; inspect the budget and finalizer, and do not restart an active producer merely because the row is quiet.
- Viewport screenshots after scrolling are reliable for virtualized messages. Element screenshots produced retained blank/giant crops in this pass; excluded captures are not proof.
- Current GUI full gates passed install/lint/typecheck/build/dist: rooms 16,579 pass / 0 fail / 2 pre-existing unrelated skips; cloud 16,809 pass / 0 fail / 0 skip. These are suite totals, not newly created tests. Coverage floors hold. No new skip, timeout, baseline addition or retry-based green; post-summary Bun directory diagnostics remain disclosed.
- `@openmarket/rooms-client@0.104.0-roster.1` is privately published under `roster-preview`; at the time `latest` was `0.103.0`. Main has since moved its pin to `0.104.0` (`7e57ee84`). A fresh no-cache registry install and all three consumer pins/root lock qualify the actual archive SHA-256 `2cca8b49b93b2aa62a4e9730ff9b5d37e100272cdb080f1e9b8c5c76a82c0cb4`. Source provenance is `8de03f6` plus the four-file `7f730` knowledge patch, stable patch ID `a41e0c90d339e73f13a16f7ee491a8c062b8ca83`. The archive accepts knowledge-bearing reviews. Earlier missing-registry evidence remains historical; local roster.2 was never published or used.

- Tested macOS arm64 setup is pinned: Claude Code 2.1.278 uses `curl -fsSL https://claude.ai/install.sh | bash -s 2.1.278` and `DISABLE_AUTOUPDATER=1 claude`; that environment variable suppresses background updates only for the sign-in command. Codex 0.153.4 uses `curl -fsSL https://chatgpt.com/codex/install.sh | sh -s -- --release 0.153.4` and `codex login`. Complete provider browser sign-in, then refresh Brains; OM never collects provider credentials.
- Current desktop and phone rooms axe: 0 violations / 0 incomplete. The no-provider fixture also reports 0 violations / 0 incomplete. Hosted axe: 0 violations / 1 incomplete contrast rule across 8 phone gradient or decorative nodes. Both hosts have zero browser errors and no horizontal overflow. Light and 200% fixture text were viewed; rail names truncate at enlarged text. Keyboard Tab/Enter switches to Work. The no-provider fixture recorded 3 GETs, no mutation, and disabled Brain and Review actions.

### Verification record

**Last verified:** 2026-10-30 (scheduled maintenance). **Product commit:** `47cb13bf` (GitLab origin/main; rooms-client 0.108.0). **Scope:** `/rooms/` `agent-center-fixture`: **New agent** → **Work agent** → **Continue** → **Create an agent**, still reading "Brains service is unavailable."; `connections=none` shows **Refresh brains** with **Review agent** disabled. **Limitations:** Review, Try, Add, import, publish and work. Evidence: `http://127.0.0.1:8098/verify-om-chat-maint-20261030/r1/` (frame 34).

**Previous record:** 2026-10-30 (nightly maintenance). **Product commit:** `47cb13bf` (GitLab origin/main; rooms-client 0.108.0). **Scope (fixture lane, `/rooms/`):** `agent-center-fixture.html` **New agent** opened its dialog. **Work agent** → **Continue** opened **Create an agent** with "Brains service is unavailable." and empty selects; `fetch('/rpc/v1/roster/brains')` returned 200 with only om and codex. On `?connections=none`, the same path showed the **Brains** region and the sign-in guidance, **Review agent** was disabled, and `fixtureUnexpectedRosterMutation` was unset. `roster=projects` rendered the default page. **Update for argue**, **Run argue** and **More actions for argue** rendered on the default fixture. **Limitations:** **Create a chat agent** → **Review agent** was not re-pressed. Review, Try, Add, import, catalog, publish and work need an authenticated daemon lane. The `40d509cf` refusal text has no fixture route. Evidence is local only: `artifacts/vomc-nightly-20261030/r1/` (frames 06-10, 11).

**Previous record:** 2026-10-29 (nightly maintenance). **Product commit:** `cdfb1b0f` (origin/main; rooms-client 0.108.0). **Scope (fixture lane, `/rooms/`):** `agent-center-fixture.html` default showed the Roster h1, **Waiting on you** and **+ Wire an agent**, and no `Your agents` shelf. `?roster=work-builder&connections=none` showed Brains and the Create an agent form. `roster=projects` read "Could not load projects" / "Could not load Brains", and `roster=work-proof` read "Recorded work fixture is unavailable." — unchanged on rooms-client 0.108.0. `#/agents/badge/agcr_claude` showed **claude code**, **Live now** and a `role=img`. **Limitations:** **Create a work agent** on `?roster=work-builder` was not re-pressed. Review, Try, Add, import, catalog, publish and work need an authenticated daemon lane, and no fixture renders the roster agent card. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261029/r1/` (frames 01, 45, 69–71).

**Previous record:** 2026-10-28 (nightly maintenance). **Product commit:** `2dd7aad1` (origin/main; rooms-client 0.107.0). **Scope (fixture lane, `/rooms/`):** `agent-center-fixture.html` default showed the Roster h1, **Waiting on you** and **+ Wire an agent**, and no `Your agents` shelf. `?roster=work-builder&connections=none` showed Brains and the Create an agent form. `?roster=work-builder` → **Create a work agent** read "Brains service is unavailable." with **Review agent** disabled. `roster=projects` read "Could not load projects" / "Could not load Brains", and `roster=work-proof` read "Recorded work fixture is unavailable." `#/agents/badge/agcr_claude` showed **claude code**, **Live now** and a `role=img`. **Limitations:** The new agent-card controls and the `@om-skills` update notice (`c70fdd28`, `2dd7aad1`) have no fixture and were not driven; `/chat/` was not re-driven for the creator. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261028/r1/` (frames 26-27).

**Re-driven 2026-10-27 (maintenance).** **Product commit:** `6c15b0fb286e9dc1b6cb130c9c97cd7e0afa9254` (origin/main). All four `roster=` rows in the table above reproduced. One precision for `roster=work-builder`: the page has no Brains region, and "Brains service is unavailable" appears only after **Create a work agent** is chosen. Evidence: `http://127.0.0.1:8098/verify-om-chat-maint-20261027/r1/` (frames 32, 34).

**Previous record:** 2026-10-27. **Product commit:** `6c15b0fb286e9dc1b6cb130c9c97cd7e0afa9254` (origin/main; the creator landed in `01bf4481`). **Scope (fixture lane, `/rooms/` and `/chat/`):** `agent-center-fixture.html` default showed the Roster h1, the Roster sections nav and **+ Wire an agent**. `?roster=work-builder&connections=none` showed Brains (Claude Code / Codex Not installed) and the Create an agent form. **Create a work agent** showed the sign-in guidance with **Review agent** disabled. **Create a chat agent** → **Start from explain** filled Name `explain`, three questions and the first reply check, and enabled **Review agent**; clicking it recorded `POST /rpc/v1/roster/local-packages` and showed "Builder service is unavailable." `roster=work-builder`, `roster=projects` and `roster=work-proof` showed the load failures in Gotchas. `#/agents/badge/agcr_claude` showed **claude code** and **Live now**. On `/chat/`, `shell-fixture.html?view=agents` showed **Agent management** with the local-app copy. **Limitations:** Review, Try, Add, import preview, catalog, publish/adopt, Plan approval, native work, proof and delivery were not driven on main; they need an authenticated daemon lane. The branch receipts above are not re-proved on main. Axe was not run. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261027/r01/` (frames 04-10, 11, 42).

### Historical route-only verification record

**Last verified:** 2026-10-26. **Product commit:** `5820fbeaca9ded509b4369498f5946f32455c61a` (origin/main; since `afabb11c` only `apps/cloud/Dockerfile.market` changed). **Scope:** Route-only on main before `01bf4481` landed. `?view=agents` **Wire an agent** opened Agent Settings; `components/roster/` was then absent and MR !75 unmerged. Superseded by the record above. **Limitations:** All creator, catalog, sharing, adoption and native-work claims were branch-only at that commit. Previous record: 2026-10-23 at `afabb11c`.

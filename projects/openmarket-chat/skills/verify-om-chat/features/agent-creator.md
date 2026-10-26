# Agent creation, import and sharing

> **Scope on origin/main (2026-10-22, `cd9f8c72`): branch-only.** Everything below
> except the route-only record describes the unmerged branch
> `daryl/agent-creator-migration-20261007` (MR !75; `a0916a25` and the GUI
> receipts named there), which is not an ancestor of origin/main.
> `packages/chat-ui/src/components/AgentCenterSurface.tsx`, the whole
> `components/roster/` directory, and the labels Review agent, Choose a brain,
> Install in shadow mode, Apply update / Apply rollback, Review Plan, Approve
> Plan, Start approved work, View recorded proof, View delivery history,
> `Access for <name>` and `Work for <name>` do not exist on main. On main, the
> Agents route renders the roster shell, and **+ Wire an agent**
> (`AgentCenterPane.tsx:947`) opens Agent Settings. Re-verify these flows
> on main only after MR !75 merges. Until then, drive them from that branch's
> worktree, never from a main lane.

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
- Keep Agent Center visible without configured Claude Code or Codex. Show install/sign-in/verification guidance; disable Brain and Work review until a supported coding-ready provider is connected. Unsupported Work remains visible and disabled without unauthorized RPCs. Hosted `/chat` explains that creation and management require the local app.

## How to get to it (user POV)

Open the local daemon's **/rooms**, choose **Agents**, and use **Roster / Your agents** to create or import. **+ Wire an agent** opens Agent Settings; it is not the creator entry point. Without a coding-ready brain, open Brains setup, install the tested provider version, complete its browser sign-in, then refresh Brains for a strict compatibility check. Credentials stay with the provider and are never entered in OM. Work stays inspectable but Brain and Review are disabled. Work creation selects a linked project and supported brain. Choose **Review agent**, read access and checks, then **Add**. Grant the intended channel under **Access for <name>**, then mention the agent there.

To share, publish a version on the test server from the publisher profile. As a different signed-in user, open the catalog, choose the release, review its digest/files, and **Install in shadow mode**. Review before updating or **Apply rollback**. A revoked release must expose its state and remove installation actions.

For a coding task, open **Work for <name>**, then **Review Plan**. Read the Plan before **Approve Plan** and **Start approved work**. Follow the automatically updating row, **View recorded proof** and **View delivery history**. Completion includes committed work, required check results, Result/History and one channel reply; an early commit or reply alone is insufficient.

## Driving it with control-om-chat

Run the wrapper from the intended GitLab GUI worktree and its assigned port. The fixture proves rendering and capability limitations; authenticated daemon lanes prove creation, sharing and execution.

```sh
OM_CHAT_LANE_PORT=<assigned-port> control-om-chat doctor
agent-browser open "$(OM_CHAT_LANE_PORT=<assigned-port> control-om-chat url 'tools/visual/shell-fixture.html?view=agents&alerts=quiet')"
agent-browser snapshot -i
# Click the current Agents reference from that snapshot.
agent-browser click @<fresh-reference>
```

Use the hosted fixture below `/chat/` in a separate browser session on its assigned port. Check desktop and phone widths, readable local-only management copy, console, axe and keyboard rail navigation. Current two-host fixtures have zero browser errors and axe violations. Local and no-provider checks have zero incomplete results; hosted contrast retains one incomplete rule (eight phone gradient or decorative nodes). The older r02 contrast results and focused tooltip landmark warning remain historical.

Use independently authenticated publisher and recipient homes for server behavior. Authorized normal account-browser posts in `local_longan_storage` avoid the MCP badge's consecutive-post limit; do not ask for human `ready` loops. Correlate the actual source message, watcher run, release digest, current attempt and one delivered reply. Never mutate the live database to manufacture proof.

Recorded native proofs (historical execution): Claude C6 source320/reply324, local commit4268dcd9; Codex X4 source325/reply327, local commit0842322d. Each had 16 passing focused tests, a successful build, five passing required checks, all five effects delivered once and durable Completed. C6 additionally recovered a controlled pre-manifest interruption with the original attempt/epoch/budget and one successor current manifest. X4's overnight human approval pause is preserved, not charged as model runtime. Current qualified daemon restart retained C6/X4/S2 completions and no duplicate effects. Recipient S2 source322/reply323 called skill_read/post_reply and named knowledge/README.md.

## Gotchas

- The ordinary source fixture still lacks authenticated creator/catalog prerequisites. Its apparent reachability is not full creator verification. The earlier a0916a25 route-only record remains historical, superseded for daemon-backed claims by the explicit account-lane receipts above.
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

### Historical route-only verification record

**Last verified:** 2026-10-26. **Product commit:** `5820fbeaca9ded509b4369498f5946f32455c61a` (origin/main; since `afabb11c` only `apps/cloud/Dockerfile.market` changed). **Scope:** Route-only on main. `?view=agents` **Wire an agent** opened Agent Settings; `components/roster/` is still absent and MR !75 is unmerged. **Limitations:** All creator, catalog, sharing, adoption and native-work claims are branch-only and pending on main. Previous record: 2026-10-23 at `afabb11c`, which this re-drive did not narrow.

# Agent creation, import and sharing

*Verified 2026-10-08. Final GUI `2fc19842692e61b82e81c164a55de70199cf8fc4`, daemon delivery assembly `b1c53c9665f2d76219f72505b722e0a24249e280`, binary SHA256 `176119e6cb6cbfa00b240cd99518571a51685f68b754dcbf64cf9d9dca2e0277`. Native C6/X4/S2 executed on daemon `635441fb083971c1ff5143835521d5c8193e60c2`, binary `7e7f8ee1e25556d1cc75ad61e0d3f4f240dd0715331a52d4d33f8e71067af213`. Final viewing and restart reconciliation use the delivery assembly. Gallery `agent-creator-stress-20261007/r02` (operator-local evidence) contains 21 root-reviewed frames with execution/viewing provenance. Clean registry installation and product delivery remain unqualified.*

## Sub-features

- Create local chat or work agents with explicit owner identity, supported brain and linked project. Private chat Try does not implement a work task.
- Preview supported text-agent and Agent Skills imports, including provenance, omissions, reviewed knowledge, skills, access and locked checks. Arbitrary executable harnesses and scripts are outside this release.
- Review before Add or shadow installation. An identical unfinished review reopens the same package and approval; conflicting content refuses. Normal desktop/phone replay on GUI087/daemonb1e93b1 reused the pending review without another installation or event.
- Publish on the test server, review/adopt as a separate authenticated user, and converge two identical installation actions to one instance.
- Review changed knowledge, skill, definition and capabilities before updating or rolling back. Exact-release revocation removes its installation action while preserving other versions.
- Read the selected release-local guide on invocation and send one readable reply. Historical update/rollback/revocation proof used GUI29e414ad/daemon7f7304243. Fresh recipient S2 read the adopted guide and replied once on daemon635441fb.
- Review a channel task's formatted Plan, then approve and start native Claude or Codex implementation. Each current positive task edited only README, ran actual checks, committed locally, delivered all five effects once and became durably Completed.
- Show readable Plan/Result/History Markdown without activating embedded media or executable blocks. Work progress refreshes automatically while visible, and progress revisions preserve open proof/delivery details and focus. Account, client, attempt, epoch and delivery-state changes still invalidate stale views.
- Clearly explain that hosted `/chat` creation and management require the local app.

## How to get to it (user POV)

Open the local daemon's **/rooms**, choose **Agents**, and use **Roster / Your agents** to create or import. **+ Wire an agent** opens Agent Settings; it is not the creator entry point. Work creation selects a linked project and supported brain. Choose **Review agent**, read access and checks, then **Add**. Grant the intended channel under **Access for <name>**, then mention the agent there.

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

Use the hosted fixture below `/chat/` in a separate browser session on its assigned port. Check desktop and phone widths, readable local-only management copy, console, axe and keyboard rail navigation. Final two-host fixtures had zero browser errors and zero axe violations; each contrast audit retains one incomplete result. Earlier focused tooltip landmark warning remains disclosed.

Use independently authenticated publisher and recipient homes for server behavior. Authorized normal account-browser posts in `local_longan_storage` avoid the MCP badge's consecutive-post limit; do not ask for human `ready` loops. Correlate the actual source message, watcher run, release digest, current attempt and one delivered reply. Never mutate the live database to manufacture proof.

Current native proofs: Claude C6 source320/reply324, local commit4268dcd9; Codex X4 source325/reply327, local commit0842322d. Each had 16 passing focused tests, a successful build, five passing required checks, all five effects delivered once and durable Completed. C6 additionally recovered a controlled pre-manifest interruption with the original attempt/epoch/budget and one successor current manifest. X4's overnight human approval pause is preserved, not charged as model runtime. Final daemon restart retained both completions and no duplicate replies. Recipient S2 source322/reply323 called skill_read/post_reply and named knowledge/README.md.

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
- Final full GUI gates passed lint/typecheck/build/dist, rooms22,250 pass/0fail/2existing unrelated skips and cloud16,776 pass/0fail/0skip. These are total suite counts, not newly created tests. No new skip, baseline debt, diagnostic retry pass or enlarged test timeout was introduced. Nonfatal Bun directory diagnostics remain recorded.
- SDK0.104.0-roster.1 returned registry E404 on2026-10-08. Local tests use exact archive SHA256 `2cca8b49b93b2aa62a4e9730ff9b5d37e100272cdb080f1e9b8c5c76a82c0cb4`; tracked consumer pins/root lock still use0.103.0. Restricted preview publication, real registry pinning and fresh gates remain required. No product push/publication/merge/release is implied.

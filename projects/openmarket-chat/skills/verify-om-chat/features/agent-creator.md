# Agent creation, import and sharing

*Verified: 2026-10-05, GUI `1c11e3319a866475826f6321c945dda06fee1e68`. Native Codex 261 and Claude 263 completed on daemon `d24bded8f`; repeated D4 reads passed on `39e94a54f`; D5 update/execution passed on `335a63073`; revocation/refusal/rollback and restored D4 execution passed on `288f6e0fb`. Both GUI gates passed against the exact unpublished SDK archive. Catalog first selections and a fresh D4 invocation subsequently passed on `3b8496603`. Required full paid evaluations and registry delivery remain incomplete.*

Owners create text agents locally, import supported definitions and skills, and share immutable versions through a server catalog. Recipients review access before adopting or updating. Credentials, private memory and owner notes are separate from shared package bytes. This is Units 1–4; arbitrary third-party runtime admission is deferred.

## Sub-features

- Local Agent Center creation with description, instructions, exactly three sample questions, supported brain, reviewed preview and shadow installation. Invalid question counts receive accessible guidance.
- Supported text-agent and SKILL.md conversion with provenance, omissions, exact digest and skill files. Scripts, hooks, executables, unsafe paths and permission escalation are refused before installation.
- Private Try reads the pinned release-local guide without durable conversation, memory, run or delivery effects.
- Publication and adoption review exact immutable version/digest, publisher identity and requested access. Packages exclude credentials, memory, overlays and run artifacts.
- Updates and rollback require explicit review/apply. Revocation blocks execution and explains recovery to the invoker.
- Channel use reads the selected installed skill and delivers one readable reply. A native coding task reads its vault context, changes files, checks them, commits locally and delivers its result.
- Hosted /chat explains that creation and installation are local. Authenticated hosted creation is outside this release.

## How to get to it (user POV)

Open /rooms through your local daemon and choose **Agents**. Create or import an agent, review it and install it. Use **Try <agent name>** for private preview. Grant only the intended channel, then mention the installed agent in that channel.

Select **Server channel** to open the catalog. Publish a version from profile A. In a separate profile B, review and adopt the exact version. Under **Manage installed agents**, choose **Installed agent** and **Target release**, then **Review update** and **Apply update**. Review and apply rollback to recover from a revoked version. Capture the review before applying and the selected version afterward.

## Driving it with control-om-chat

Use the canonical GUI worktree and two independently authenticated, owned daemon homes. Check each lane with its assigned OM_LANE_STATE and OM_LANE_PORT through control-om doctor. Obtain its /rooms origin through control-om url; never use the operator daemon or the developer Vite origin.

```sh
agent-browser --session creator-owner open '<owned publisher daemon /rooms URL>'
agent-browser --session creator-recipient open '<owned recipient daemon /rooms URL>'
agent-browser --session creator-recipient snapshot -i -c
```

Use fresh accessible names for every action. Agent Center remount resets **Server channel** to Choose a channel, so select it again and wait for loading to settle. An **Installed agent** option's value is the agent instance ID, not the installation ID. Read the observed option when selection appears unchanged.

Post through the authorized normal account browser. This uses that authenticated profile, not an MCP agent posting badge. Do not request repeated human ready messages to reset a badge for normal account-browser verification. Confirm the profile before posting.

Use a bounded imported-guide task with a benign phrase changed between releases. Require actual skill_read, the selected digest, durable completed and one delivered chat effect. Current proof used D4 forest cabin 1005, then D5 amber canoe 1005, then restored D4 after rollback. Compare all six cached files for both versions against their exact fixtures; inspect safe owner/recipient memory and overlay counts without printing contents or credentials.

For native coding, use a linked private repository and a README-only task. Require the agent's own tests/build, clean local commit, Result/History vault revisions, one reply and durable completion. A readiness screen or visible reply alone is insufficient. No host completion, push or release belongs in this bounded test.

Verify the hosted limitation in the hosted shell fixture on an owned lane and label it fixture evidence. Publish paired snapshots/screenshots with control-om-chat evidence publish. The latest gallery is agent-creator-20261002/r05 with exact source labels and retained failures.

## Gotchas

- Compiled daemons cache the GUI bundle at boot. Restart only owned lanes after rebuilding; source daemons behave differently. Preserve account homes and operator services.
- Display name is not identity. Publisher dboon333 can appear as daryl or locallongan69; confirm authenticated owner ID. Recipient dboon_ref must be a separate profile.
- The cached tool collection once retained the first run's release resolver. After repair, two consecutive D4 channel runs on the same daemon each read the current guide. Updating the Agent Center badge alone did not prove execution.
- Source 278 refusal creates a failed bookkeeping run with no executor/tool activity. Reply 279 clearly explains revocation and rollback. Do not assert zero run records. After normal rollback, source 280 read D4 and delivered reply 281 once.
- A publication POST can succeed while its follow-up list fails. Preserve that uncertainty, check a second authenticated view and retry only the same command/idempotency key. Never create a fresh write just because readback failed.
- Initial publisher catalog still hit cooldown under concurrent paid traffic; one normal Refresh recovered six entries. The paid seed and publisher share backend credentials, while the recipient is distinct. A quiet post-eval initial selection also failed (screenshot29). Other preference/config/proposal panels succeeded. The subsequent authority-batch repair on 3b8496603 completed both first selections without Refresh: six releases, correct state and publisher curator controls; catalog/installed reads returned 200. Recipient source 282 then read installed D4 via actual skill_read, completed and delivered reply 283 once. Loading included backend retry; no fast-load or traffic-causality claim.
- Publisher memory/overlay counts are 2/1 and recipient 0/0. Their deterministic namespace strings are equal in separate account stores. Package/count isolation does not prove model ignorance of publicly posted text.
- Qualified local Claude 2.1.278/ACP 0.76.0 with Opus 4.6 and Codex 0.153.4/ACP 1.11.0 with gpt-6-astra each completed the current native task. Newer global clients, other models, operating systems and native mobile remain unverified. Never change attestations to manufacture qualification.
- Actual native tests/build exited zero despite Bun parent-directory diagnostics. Build stdout was withheld by the existing scanner; inspect the expected artifacts and report the warning separately.
- Exact archive consumption passed all-host 22,220 tests with zero failures/two existing skips and hosted 16,752 with zero failures/zero skips, plus static/build/artifact/coverage gates. SDK 0.104.0-roster.1 SHA-256 is bbe9df513e4fc2b497bd6c01fdfc63407f865c8b212a319015dd9ee434605011. It is unpublished; committed pins/lock are restored, not registry-verified.
- Paid orders/change passed on 335a63073, while full compose finished with21 passing/7 failing tests (88 PASS/13 FAIL/24 BLOCKED checks), watches completed with 10 passing/47 failing tests across 52 live cases and five dry checks, and doors failed 4/43. Selected unchanged-main W05/W08/W14 also failed; that is not a full52-case baseline or a green candidate gate. No cost bounds, deadlines, skips or baselines were weakened. Full source scan remains red on 76 unchanged-main findings; the exact SDK archive scan passed.
- An earlier operator model-setting mistake remains disclosed. Use control-om om for every isolated account/model command; control-om cli does not bind OM_HOME. Product push, SDK publication, merge and release need their concrete authorization.

- Latest local daemon assembly is e08d96f0f. The bounded authority-batch fix retains local owner checks around every read and one final remote membership refresh before exposing at most three revisions. Catalog contracts: 153 pass/0 fail/579 assertions, full workspace typecheck/build and scoped Biome pass. Fixture read budgets are synthetic, not public backend quotas.
- An overbroad 430-file roster diagnostic remains FAILED/INCOMPLETE after one ACP initialize fixture timeout (754 observed passes). Test-only injected clock stabilization passes 100 focused ACP contracts/494 assertions and fresh CLI typecheck; production timeouts are unchanged.
- Selected J9–11/F2 paid composer diagnostic passes four tests/127 assertions, with nine F2 table checks. F2 supplies the required 18:00 clock and checks exact daily cron; its daemonless fixture does not prove actual scheduled execution. This partial run never replaces the failed full gate.
- A fresh fetch shows eight daemon main commits beyond the verified e7 base (latest bfc2a4143); GUI main remains 231c95f4. Delivery requires an isolated rebase and renewed applicable checks. Existing source-specific receipts remain immutable.

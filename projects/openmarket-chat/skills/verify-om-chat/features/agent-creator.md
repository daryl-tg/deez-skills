# Agent creation, import and sharing

*Verified: 2026-10-02, daemon `6d5700ee09e8dc184a2da1b6d53f3514c0420782`, GUI `3ea2ad6130f0fd892c98c74237f83c2cfebc2f6e` — complete application gates, recipient skill execution, reviewed update/rollback and populated package isolation. Revoked-mention notices were proved on immediately preceding daemon `9cb0f2660`. Exact supported native coding runs are being verified separately; the fresh Claude run stopped on provider HTTP 400.*

Owners create text agents locally, import supported text definitions and skills, and share immutable versions through a server catalog. Recipients review the requested access before adopting or updating. Credentials, private memory and owner notes remain separate from shared package bytes.

## Sub-features

- Local Agent Center creation: description, instructions, exactly three sample questions, supported brain, requested access, reviewed preview and shadow installation. Invalid question counts are stopped locally with friendly accessible guidance.
- Supported text-agent and `SKILL.md` conversion: provenance, omissions, exact digest and skill files; refuse scripts/hooks/executables, unsafe paths and permission escalation before installation.
- Private Try: reads the pinned release-local guide without durable memory, conversation, run or delivery effects.
- Catalog publication: publisher, immutable version/digest and access review; sharing excludes owner credentials, private memory, overlays and run artifacts.
- Recipient adoption: a second authenticated profile approves the exact reviewed version and receives its own installation/credential.
- Opt-in update and rollback: review changed behavior/access and owner-note conflicts before applying; revocation blocks new model work.
- Channel use: an explicit owner mention reads the installed skill and posts one human-readable reply.
- Hosted `/chat`: clearly explains that local agent management needs the local daemon. Hosted authenticated-wire creation is outside this release.

## How to get to it (user POV)

Open `/rooms` through your local daemon and choose **Agents**. Use the creation/import controls to prepare and review an agent before installing it. Choose **Try <agent name>** for a private preview.

For sharing, select the test server's catalog in Agent Center and review the exact version and requested access before publishing or adopting. On the recipient profile, use **Review update** followed by **Apply update**; use **Review rollback** followed by **Apply rollback** to return to the previous release. A revoked release should offer rollback or an active version.

Give the installed agent access to the intended channel, then post `@<agent name>` followed by the bounded task. Read the reply in that same channel; correlate its source message and run rather than inferring delivery from an Agent Center success badge.

## Driving it with control-om-chat

Use the canonical GitLab GUI worktree and two owned, authenticated daemon lanes. Run `control-om-chat doctor` from the GUI worktree. For daemon-owned `/rooms`, obtain each origin from `control-om url /rooms/` with that lane's state/port; never use the developer's Vite origin or operator daemon.

```sh
agent-browser --session creator-owner open '<owned publisher daemon /rooms URL>'
agent-browser --session creator-recipient open '<owned recipient daemon /rooms URL>'
agent-browser --session creator-recipient snapshot -i
```

Drive by the current accessible names. The installed-catalog controls include **Installed agent**, **Target release**, **Review update**, **Apply update**, **Review rollback** and **Apply rollback**. Capture both the review and resulting installation. Record exact release digest, source message, run, tool events and delivery receipt from the daemon's authorized read-only view.

A bounded skill proof uses a benign phrase present only in the release-local imported guide. The recipient channel run must show `skill_read`, `post_reply`, the selected digest and one delivered effect. Private-state isolation needs byte inspection of every package file plus independent owner/recipient memory, overlay and credential metadata. Empty stores alone are insufficient: populate publisher state through normal consent first.

After the final shared build, verify the hosted limitation through the hosted shell fixture on an owned lane and label it fixture evidence. Publish paired accessibility snapshots/screenshots using `control-om-chat evidence publish <run-id> <revision>`.

## Gotchas

- Compiled daemons cache the GUI bundle at boot. Rebuild and restart owned lanes before final GUI proof; a source daemon behaves differently.
- Display name is not account identity. The publisher screen showed `locallongan69` while its authenticated operator ID matched the catalog publisher; the recipient must still be the separate `dboon_ref` profile.
- Exact supported Claude 2.1.278 and Codex 0.153.4 binaries in a private lane match existing profiles and show coding-ready. Operator-installed Claude 2.1.287 and Codex 0.159.2 remain unverified/investigation-only. Readiness and a completed model-driven coding receipt are separate claims; no qualification profile was changed.
- Task 225/reply 226 proved D3 phrase `plum beacon 9058`. After the repair, revoked sources 229 and 231 each received one clear room refusal, zero model runs and no duplicate notice after restart. Normal Agent Center rollback to D1 then recovered: task 233 delivered reply 234, `cedar kettle 4721`, on final daemon `6d5700ee0`. Earlier incorrect and silent notices remain recorded failures.
- Initial D3 revocation returned `verify_failed`; a later ledger read and replay of the same idempotency key confirmed revision 2 revoked. Do not retry with a fresh write key or erase the first failure.
- The benign private-memory marker was also posted in the test channel. Package/DB isolation was proved; recipient-model ignorance of that publicly visible text was not.
- Local packed SDK consumption is not registry delivery. The unpublished 0.104.0-roster.1 archive was used for checks while committed registry pins still referenced 0.103.0.
- Final GUI v22 passed rooms 22,209 tests (zero failures, two existing skips) and hosted 16,741 tests (zero failures, zero skips), plus lint/typecheck/build/artifact checks and coverage floors. Hosted fixture rendering does not prove authenticated transport. Both consumer gates remain required after shared UI changes.

# Agent draft sharing

An agent can leave a versioned draft in a room composer. The operator owns the
composer: loading a draft is explicit, edits remain private, and sharing an
edited revision asks the agent to review it without sending the message.

## Sub-features

- A draft dock identifies the agent, target channel or topic, version and
  timestamp. History previews older versions; Load copies a selected version
  into the composer. **Discard** (a labeled verb since `d8759d95`) resolves
  every waiting draft from that agent here and reads the daemon's staged list
  back; a History row's own **Discard** resolves only that version.
- History groups versions under a lane head, "<agent> · N waiting", shows each
  draft's id (`agdr_…`) in a `code` chip, and marks resolved rows "not
  waiting". A discard the daemon does not confirm leaves an alert, "Couldn't
  discard N draft(s)…", with **Retry**.
- Editing a loaded draft marks the changes private. **Share with agent** exposes
  that exact revision for review; a receipt names the shared revision.
- Share does not post to the room. The normal composer Send control remains the
  separate posting action.
- A later edit after sharing stays private until **Share update** publishes the
  next revision. Failed confirmation can be retried without claiming delivery.

## How to get to it (user POV)

When an agent stages a draft for a channel or topic, its dock appears above your
composer. Preview the versions, load one if you want it, edit it, then choose
**Share with agent** when you want the agent to review your changes. Choose
Send only when you want to post the message yourself.

## Driving it with control-om-chat

Use the dedicated fixture to exercise the real `AgentDraftDock` with a loaded,
unsent channel draft:

```bash
agent-browser open "$(control-om-chat url 'tools/visual/agent-draft-share-fixture.html')"
agent-browser find role button click --name History
agent-browser find role textbox fill --name 'Message #agents-lab' \
  'The reconnect bug is fixed. I can post the follow-up after you review it. Added rollout timing.'
agent-browser find role button click --name 'Share with agent'
agent-browser snapshot -i -c
```

Check that the UI says **Shared revision 1 with the agent**, the fixture's
`data-fixture-shared-revision` and `data-fixture-shared-text` markers record the
same edit, and the composer still contains that text. The fixture does not press
Send. In the integrated room or topic path, the `AgentDraftDock` is mounted by
`packages/chat-ui/src/components/Composer.tsx` and shares through the daemon
session methods.

## Gotchas

- **A re-stage after a topic round trip is source-only.** Since `d626fc89`, when
  you load and edit an agent draft, leave the topic, and the agent re-stages
  while you are away, coming back keeps your edit and the dock reads "v<N>
  waiting; your text is untouched." with **Load v<N>** and **Keep mine**
  (`AgentDraftDock.tsx:345`), not "Edited privately from v<N>; the agent still
  sees its original." (`:328`). The fixture mounts the dock over a bare
  `textarea` with no Composer, draft store or topic navigation, so it cannot
  reproduce the round trip. `packages/chat-ui/test/agent/draft-replace-loaded.test.tsx`
  is the only proof; live verification is pending a daemon-pair lane with a
  badge agent.
- The standalone fixture supplies a local `onShare` callback. It proves the
  dock's explicit share state and receipt, not daemon persistence, agent
  visibility, or remote review.
- The initial draft is already loaded. Edit the composer before looking for the
  share control; an unchanged loaded draft has no revision to share.
- A shared revision is still an unsent composer draft. Verify the separate Send
  action before making a claim about room delivery.

- Exact names: the head discard shows **Discard** and is named "Discard this
  draft (nothing posts)" (`AgentDraftDock.tsx:162-173`, `:266-275`). With
  several waiting drafts from one agent it shows **Discard all N** ("Discard all
  N of <agent>'s waiting drafts in this room (nothing posts)"); with several
  agents, **Discard all** ("Discard every agent's drafts here (nothing
  posts)"). The old **Dismiss agent draft** name is gone. A History row's
  button is **Discard v<N> (<draft id>)** (`:491`); with several lanes each
  lane head adds **Discard all from <agent>** (`:423`). The fixture seeds one
  lane with one version (`agdr_visual_1`) and a no-op discard, so only the
  single-draft names and the row are reachable there. Load is `Load
  v<N>` for a waiting head (`:353`), `Load v<N> into the composer` per version in
  History (`:474`, beside `Preview v<N>`), and `Load into composer` (`:378`).
  **Keep mine** (`:361`) appears when a newer version arrives while the
  composer holds your text, and several agents get a tablist **Agents with
  drafts** (`:393`).

### Verification record

**Last verified:** 2026-11-08 (nightly maintenance). **Product commit:** `08fe407b` (GitLab origin/main; rooms-client 0.112.0; unchanged since the 2026-11-07 pass). **Scope:** `/rooms/` (18183) `agent-draft-share-fixture.html`: an edit to **Message #agents-lab**, then **Share with agent** → "Shared revision 1 with the agent."; the head control **Discard this draft (nothing posts)**. **Limitations:** **Discard all** and the failed-discard alert need a fixture with several drafts or a refused discard; this one hardcodes one lane with no-op discards (`agent-draft-share-fixture.tsx:48`, `:55-56`). Evidence: `http://127.0.0.1:8098/vomc-nightly-20261108/r1/`.

**Previous record:** 2026-11-07 (nightly maintenance). **Product commit:** `08fe407b` (GitLab origin/main; rooms-client 0.112.0; 89 commits past `ea399e62`). **Scope:** `/rooms/` (18180) `agent-draft-share-fixture.html`: the head **Discard** ("Discard this draft (nothing posts)"); **History** shows the lane head "claude-code · 1 waiting", the row id `agdr_visual_1`, **Discard v1 (agdr_visual_1)** and the new footer; an edit offers **Share with agent**, which reads "Shared revision 1 with the agent.". **Limitations:** the multi-draft labels, the lane **Discard all from <name>** and the failed-discard alert need more than one waiting draft or a refused discard, which the fixture does not seed; nothing was discarded. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261107/r1/`.

**Previous record:** 2026-11-06 (nightly maintenance). **Product commit:** `ea399e62` (GitLab origin/main; rooms-client 0.111.0; 74 commits past `873a57ce`). **Scope:** `/rooms/` (18180) `agent-draft-share-fixture.html` mounts the unsent `#agents-lab` draft (**claude-code (repo:om)**, v1). **Limitations:** **Share with agent** not pressed. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261106/r1/`.

**Previous record:** 2026-11-04 (nightly maintenance). **Product commit:** `ce14d4ba` (GitLab origin/main; rooms-client 0.109.1; 16 commits past `ba4389e7`). **Scope:** `/rooms/` (18160) `agent-draft-share-fixture.html` mounts the loaded, unsent `#agents-lab` draft (**claude-code (repo:om)**, v1). **Limitations:** **Share with agent** was not pressed this pass; the 2026-11-03 record stands for it. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261104/r1/`.

**Previous record:** 2026-11-03 (nightly maintenance). **Product commit:** `ba4389e7` (GitLab origin/main; rooms-client 0.108.0; one CI-only commit past `3f8f24bc`). **Scope:** `/rooms/` (18143) `agent-draft-share-fixture.html`: **History**, fill **Message #agents-lab**, **Share with agent** → **Shared revision 1 with the agent**; `data-fixture-shared-revision=1` and the shared text match. **Limitations:** unchanged. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261103/r1/` (`ag-07-share`).

**Previous record:** 2026-11-02 (nightly maintenance). **Product commit:** `3f8f24bc` (GitLab origin/main; rooms-client 0.108.0). **Scope:** `/rooms/` (18137) `agent-draft-share-fixture.html`: an edit to the draft → **Share with agent** → **Shared revision 1 with the agent.** Evidence: `http://127.0.0.1:8098/vomc-nightly-20261102/r1/`.

**Previous record:** 2026-11-01 (nightly maintenance). **Product commit:** `936f5b64` (GitLab origin/main; rooms-client 0.108.0). **Scope:** `/rooms/` (18137) `agent-draft-share-fixture.html`: filling **Message #agents-lab** revealed **Share with agent**; pressing it recorded **Shared revision 1 with the agent.**, and **History** lists revision 1. **Limitations:** daemon delivery. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261101/r1/` (`share-01`).

**Previous record:** 2026-10-31 (nightly maintenance). **Product commit:** `936f5b64` (GitLab origin/main; rooms-client 0.108.0). **Scope:** `/rooms/` (18135) `agent-draft-share-fixture`: **History**, a new draft text, **Share with agent** → "Shared revision 1 with the agent.", `fixtureSharedRevision=1`, `fixtureSharedText` equal to the typed text and the composer still holding it. **Limitations:** Daemon delivery and the Send path; **Share update** (revision 2) not pressed. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261031/r1/`.

**Previous record:** 2026-10-30 (scheduled maintenance). **Product commit:** `47cb13bf` (GitLab origin/main; rooms-client 0.108.0). **Scope:** `/rooms/` `agent-draft-share-fixture`: filled **Message #agents-lab**, **Share with agent** → "Shared revision 1 with the agent." and `fixtureSharedRevision=1`. **Limitations:** Daemon delivery. Evidence: `http://127.0.0.1:8098/verify-om-chat-maint-20261030/r1/` (frame 45).

**Previous record:** 2026-10-29 (nightly maintenance). **Product commit:** `cdfb1b0f` (origin/main; rooms-client 0.108.0). **Scope:** Filled `Message #agents-lab` by role with "nightly shared draft 1029" and pressed **Share with agent**. The page read "Shared revision 1 with the agent.", with `fixtureSharedRevision=1` and `fixtureSharedText` equal to the typed text. **Limitations:** Fixture-local revision only; daemon delivery not proved. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261029/r1/` (frame 52).

**Previous record:** 2026-10-28 (nightly maintenance). **Product commit:** `2dd7aad1` (origin/main). **Scope:** Filled `Message #agents-lab` by role with "nightly shared draft 1028" and pressed **Share with agent**. The page read "Shared revision 1 with the agent.", with `fixtureSharedRevision=1` and `fixtureSharedText` equal to the typed text. **Limitations:** Daemon delivery. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261028/r1/` (frame 29).

**Previous record:** 2026-10-27 (maintenance re-drive). **Product commit:** `6c15b0fb286e9dc1b6cb130c9c97cd7e0afa9254` (origin/main). **Scope:** Filled `Message #agents-lab` by role with "maint shared draft 1027" and pressed **Share with agent**. The page read "Shared revision 1 with the agent.", with `fixtureSharedRevision=1` and `fixtureSharedText` equal to the typed text. **Limitations:** Share update (revision 2) not driven; fixture-local only, so no post and no daemon delivery. Evidence: `http://127.0.0.1:8098/verify-om-chat-maint-20261027/r1/` (frame 14).

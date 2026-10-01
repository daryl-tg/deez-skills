# Agent draft sharing

An agent can leave a versioned draft in a room composer. The operator owns the
composer: loading a draft is explicit, edits remain private, and sharing an
edited revision asks the agent to review it without sending the message.

## Sub-features

- A draft dock identifies the agent, target channel or topic, version and
  timestamp. History previews older versions; Load copies a selected version
  into the composer, while Dismiss removes the offer.
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

- The standalone fixture supplies a local `onShare` callback. It proves the
  dock's explicit share state and receipt, not daemon persistence, agent
  visibility, or remote review.
- The initial draft is already loaded. Edit the composer before looking for the
  share control; an unchanged loaded draft has no revision to share.
- A shared revision is still an unsent composer draft. Verify the separate Send
  action before making a claim about room delivery.

### Verification record

**Last verified:** 2026-10-01. **Product commit:** `f8b68bf762cfa347b7f588f6fc94eb78b631381b`. **Scope:** opened history, edited the seeded loaded draft, shared revision 1, and verified the local receipt and unchanged unsent composer. **Limitations:** the fixture callback is local; daemon persistence, agent receipt, and room posting were not exercised.

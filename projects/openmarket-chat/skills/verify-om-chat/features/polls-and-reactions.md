# Polls and reactions

Voting in polls, reading closed-poll results, reacting to messages, and seeing
who reacted.

## Sub-features

- **Poll card** (`packages/chat-ui/src/components/PollCard.tsx`): one button per
  option, named `<option>\n<votes> · <percent>`, plus **Show results** and
  **Close poll**.
- **Poll composer** (`PollComposer.tsx`): a `Create poll in #<channel>` form with
  **Add option**, **Post poll** and **Create another poll**.
- **Closed-poll results** (`PollResultsDialog.tsx`): `Final results · N votes`
  with per-option percentages.
- **Roster cache** (`#752`): reopening results in the same session does not
  refetch the voter roster.
- **Reaction row** (`ReactionRow.tsx`): buttons named `<emoji> <count>, you
  reacted|not reacted`, plus **Add a reaction** and **See who reacted**.
- **Reactors dialog** (`ReactorsDialog.tsx`): a dialog named **Reactions**
  listing the reactors under each emoji.
- **Emoji picker**: **Add a reaction** opens a dialog or listbox named
  **Choose an emoji**.
- Reactions under to-do update events (`d919f889`) exist in source and unit
  tests (`packages/chat-ui/test/todo/event-reaction*.test.tsx`), but no fixture
  seeds a to-do event. Live verification pending.

## How to get to it (user POV)

Someone posts a poll in a channel. You tap an option to vote and watch the
percentages move. When the poll closes you open its results. Under any message
you add a reaction, and you tap the count to see who else reacted.

## Driving it with control-om-chat

```bash
export OM_CHAT_LANE_PORT=<assigned-port>
control-om-chat doctor && control-om-chat up
agent-browser open "$(control-om-chat url 'tools/visual/poll-results-fixture.html')"
agent-browser open "$(control-om-chat url 'tools/visual/poll-cache-fixture.html')"
agent-browser open "$(control-om-chat url 'tools/visual/fixture.html?surface=poll-ux')"
agent-browser open "$(control-om-chat url 'tools/visual/fixture.html?surface=reaction-polish')"
```

| Route | What it proves |
|---|---|
| `poll-results-fixture.html` | `Final results · 14 votes`, 57% / 29% / 14% / 0% |
| `poll-cache-fixture.html` | Click **Show results**, Escape, then click it again: `roster loads: 1` both times |
| `fixture.html?surface=poll-ux` | Poll card (ye 8 · 80%, nay 2 · 20%) and the `Create poll in #chat` composer |
| `fixture.html?surface=reaction-polish` | Reaction row, **See who reacted** dialog, **Add a reaction** picker |
| `fixture.html?surface=reaction-overflow` | Overflowed reaction row (`🔥 9, not reacted`) |

Read the roster counter with
`agent-browser eval '(()=>(document.body.innerText.match(/roster loads: \d+/)||[])[0])()'`.

## Gotchas

- These are component galleries. Clicking a poll option or a reaction chip
  changes no count, and none of these routes travel the wire. Prove rendering,
  the dialogs and the roster cache here; vote and reaction persistence need the
  daemon-pair lane. Live verification pending.
- Option buttons carry a newline in their name (`ye\n8 · 80%`). Match by
  prefix, or through `innerText`, not with an `--exact` name.
- The full-screen reaction scenes (`reaction-scene-fixture.tsx`) are opened only
  by their Playwright visual spec; `surface=reaction-scene-integration` is the
  gallery alternative.

### Verification record

**Last verified:** 2026-10-22. **Product commit:** `cd9f8c72a6522caccc3b6157a4990fb6c9d0b0cf` (origin/main). **Scope:** `/rooms/` lane at 1440x900. The results fixture showed `Final results · 14 votes` with 57/29/14/0%. The poll cache showed `roster loads: 1` after the first and second Show results. The poll UX surface rendered the card and the Create poll form. On `reaction-polish`, **See who reacted** opened the **Reactions** dialog with its reactors, and **Add a reaction** opened **Choose an emoji**. **Limitations:** Vote and reaction toggles did not change counts in the gallery. Persistence, multi-user delivery, to-do event reactions and reaction scenes were not exercised.

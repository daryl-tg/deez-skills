# Polls and reactions

Voting in polls, reading closed-poll results, reacting to messages, and seeing
who reacted.

## Sub-features

- **Poll card** (`packages/chat-ui/src/components/PollCard.tsx`; the closed rule now lives in `lib/poll-closed.ts`): one button per
  option, named `<option>\n<votes> · <percent>`, plus **Show results** and
  **Close poll**.
- **Poll composer** (`PollComposer.tsx`): a `Create poll in #<channel>` form with
  **Add option**, **Post poll** and **Create another poll**.
- **Closed-poll results** (`PollResultsDialog.tsx`): `Final results · N votes`
  with per-option percentages.
- **Roster cache** (`#752`): reopening results in the same session does not
  refetch the voter roster.
- **Reaction row** (`ReactionRow.tsx`): buttons named `<emoji> <count>, you
  reacted|not reacted`, plus **Add a reaction** and **See who reacted**. Since
  `01bf4481` the row renders those two tools itself, only when it has chips and
  its caller passes `tools`. **See who reacted** carries `aria-haspopup="dialog"`
  and `aria-expanded`, and both take an `is-open` class while open.
- **Reactors dialog** (`ReactorsDialog.tsx`): a dialog named **Reactions**
  listing the reactors under each emoji. It builds people from the message's
  cached reactor windows and fetches only when a window is incomplete. A row
  can read loading, truncated (fewer people than the count) or unavailable.
- **Lazy pickers:** the emoji picker, the Reactions dialog and Poll results are
  lazy surfaces. While one loads, a `role=status` anchor with
  `data-lazy-surface-anchor` reads **Loading Choose emoji** (and so on). A
  failed load shows `[role=alert][data-lazy-surface-error]` "`<name>` could not
  load." with **Try again** (`LazySurface.tsx:512-530`).
- **Emoji picker**: **Add a reaction** opens a dialog named **Choose an emoji**,
  with a `Search emoji (:fire:)` field and, once the table loads, 1,870 emoji
  buttons (rooms-client `0.104.0`, `7e57ee84`).
- **Reaction scenes** (`afabb11c`). When a visible chip's count rises, a scene
  plays over the viewport. Hand-built emoji (hearts, 🎉, 🔥, ⚡, 👀, the GOAT,
  the signature and shipped ones) keep their own scenes. Every other emoji now
  plays one of six family scenes: rise, burst, pulse, fall, shake or shimmer.
  The family is picked by keyword rules over the emoji table
  (`lib/reaction-scene-themes.ts`, overrides in `THEME_OVERRIDES`). Faces and
  hands without a clear theme pulse. The layer is
  `.reaction-scene-layer.reaction-scene--family-<family>` (`aria-hidden`, so
  there is no accessible name), appended to `document.body`. Hosts carry
  `[data-reaction-scene-host]`. Shell-fixture message rows carry it too (seen on
  the seeded Mermaid row).
  The themed code is a lazy chunk, so the first generic emoji after a cold load
  plays no scene. A scene lives for its family duration + 120 ms
  (`FAMILY` in `lib/reaction-scenes.ts`: fall 1000, shake 1080, pulse 880,
  rise 940, burst 1420, shimmer 1060). Under reduced motion it lives 320 ms
  (`REDUCED_SCENE_CLEANUP_MS`).
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
| `fixture.html?surface=reaction-scene-integration` | A 14-chip row on a `[data-reaction-scene-host]`, driven by `globalThis.reactionSceneIntegrationFixture.rise(emoji)` (also `rebound`, `reset`, `unmount`) |

Read the roster counter with
`agent-browser eval '(()=>(document.body.innerText.match(/roster loads: \d+/)||[])[0])()'`.

Reaction scenes. Chip clicks are no-ops in this gallery, so raise counts with the
controller. **Remove the gallery's forced `reduced-motion` class first**, then
record each layer's lifetime:

```bash
agent-browser open "$(control-om-chat url 'tools/visual/fixture.html?surface=reaction-scene-integration')"
agent-browser eval '(()=>{document.documentElement.classList.remove("reduced-motion");window.__life=[];
  const born=new Map();new MutationObserver(ms=>{for(const m of ms){
  for(const n of m.addedNodes)if(n.nodeType===1&&n.classList.contains("reaction-scene-layer"))born.set(n,performance.now());
  for(const n of m.removedNodes)if(born.has(n))window.__life.push(n.className.split(" ")[1]+":"+Math.round(performance.now()-born.get(n)))}})
  .observe(document.body,{childList:true,subtree:true});return 1})()'
for e in 😭 😭 🤬 🤔; do agent-browser eval "(()=>{reactionSceneIntegrationFixture.rise('$e');return 1})()"; sleep 2; done
agent-browser eval 'JSON.stringify(window.__life)'
#   ["reaction-scene--family-fall:1122","reaction-scene--family-shake:1202","reaction-scene--family-pulse:1002"]
#   (the first 😭 is the lazy-chunk miss: three scenes for four rises)
```

In this row 😭 and 😴 fall, 🤬 and 😱 shake, and 🤔 and 😄 pulse. The same
controller and timings hold on the `/chat/` cloud gallery
(`apps/cloud/tools/visual/fixture.tsx`). To try an emoji outside the row
(🏆 bursts, ✨ shimmers), edit the fixture: `rise` only raises chips already
listed.

## Gotchas

- None of these routes travel the wire. Reaction chip clicks change no count.
  On `surface=poll-ux`, however, a vote **does** settle locally: after a 700 ms
  timeout `ye 8 · 80%` becomes `ye 9 · 82%` (`PollUxFixture`'s `settleVote`,
  `tools/visual/fixture.tsx:1272`). That proves the card's optimistic update,
  not delivery. Close the **Create poll in #chat** dialog (Escape) first: its
  backdrop covers the card and the click is refused. Vote and reaction
  persistence still need the daemon-pair lane. Live verification pending.
- **Add a reaction** and **See who reacted** are hover-revealed. They are in the
  DOM but missing from `snapshot -i`, and `find role button` reports them
  absent. Run `agent-browser hover '[aria-label="Message from Mira Chen"]'`
  once, wait about 0.6 s for the toolbar to settle, then click (re-measured
  2026-10-26; see [message-editing.md](message-editing.md)).
- **The emoji picker loads its table lazily, and a full snapshot of it can
  hang.** On a cold vite lane, **Choose an emoji** reads "Loading emoji" for
  4–10 s, then mounts 1,870 buttons. A `snapshot -c` taken while it is open ran
  past 75 s and had to be killed. Assert with a targeted eval instead, e.g.
  `document.querySelector('[aria-label="Choose an emoji"]').querySelectorAll('button').length`.
- **Every `fixture.html` gallery forces reduced motion.** `fixture.tsx:52` adds
  `reduced-motion` to `<html>` (only `surface=resizable-panel` removes it), and
  `reducedMotionActive` honours that class as well as the media query. So every
  scene there takes the reduced path and dies at 320 ms. A themed (non-shipped)
  scene that starts reduced keeps its `reaction-scene--family-*` class: the
  runner adds `reaction-scene--reduced-motion` at start only for shipped scenes
  (`reaction-scene-runner.ts:445`), or mid-scene via `reducedTint` when
  reduced motion switches on during it (`:531`). Assert lifetime, not that class.
- Option buttons carry a newline in their name (`ye\n8 · 80%`). Match by
  prefix, or through `innerText`, not with an `--exact` name.
- `reaction-scene-fixture.tsx` takes an arbitrary emoji list and is mounted only
  by its Playwright spec. `surface=reaction-scene-integration` with the
  `reactionSceneIntegrationFixture` controller is the live path.
- **Prove the reactors dialog on `fixture.html?surface=reaction-polish`, not the
  shell.** The gallery supplies `fetchReactors`; the shell fixture leaves it to
  the INERT proxy, so a Reactions dialog there would show every emoji as
  unavailable.

### Verification record

**Last verified:** 2026-10-29 (nightly maintenance). **Product commit:** `cdfb1b0f` (origin/main; rooms-client 0.108.0). **Scope:** `poll-results-fixture` read `Final results · 14 votes`; `poll-cache-fixture` `roster loads: 0`. On `fixture.html?surface=poll-ux`, the **Create poll in #chat** dialog covers the card until Escape; then **ye 8 · 80%** settled to **ye Selected 9 · 82%** (nay **2 · 18%**). On `surface=reaction-polish`, **See who reacted** opened **Reactions** (🔥 6 / 🐐 1 / 🤍 4, six reactors) and **Add a reaction** opened **Choose an emoji** (DOM click by label). **Limitations:** Vote persistence and reaction toggles need the daemon-pair lane. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261029/r1/` (frames 12–13, 43–44, 66–67).

**Previous record:** 2026-10-28 (nightly maintenance). **Product commit:** `2dd7aad1` (origin/main). **Scope:** `poll-results-fixture` read `Final results · 14 votes` and `poll-cache-fixture` `roster loads: 0`. On `fixture.html?surface=poll-ux`, Escape closed **Create poll in #chat**, and the option `button` **ye 8 · 80%** (the accessible name has a space; older records write `ye8`) settled to **ye Selected 9 · 82%**. On `surface=reaction-polish`, **See who reacted** opened **Reactions** (🔥 6 / 🐐 1 / 🤍 4, six reactors) and **Add a reaction** opened **Choose an emoji**; both are hover-revealed, so `find role button` misses them and a DOM click by `aria-label` or `title` was used. **Limitations:** Reaction scenes, vote persistence, multi-user delivery and `/chat/` were not driven. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261028/r1/` (frames 31, 38).

**Previous record:** 2026-10-27 (maintenance re-drive). **Product commit:** `6c15b0fb286e9dc1b6cb130c9c97cd7e0afa9254` (origin/main). **Scope:** It adds the two paths the nightly record below left undriven. (1) On `fixture.html?surface=poll-ux`, Escape closed **Create poll in #chat**, and clicking the option `ye8 · 80%` settled the local vote to 82%. (2) On `?surface=reaction-scene-integration`, with `reduced-motion` removed, rising 😭 😭 🤬 🤔 produced `family-fall` 1122 ms, `family-shake` 1201 ms and `family-pulse` 1002 ms; the first 😭 was the lazy-chunk miss. `poll-results-fixture` ("Final results · 14 votes") and `poll-cache-fixture` (`roster loads: 0` before any **Show results**) were re-read. **Limitations:** Burst, rise and shimmer families, vote persistence, multi-user delivery and `/chat/` remain pending. Evidence: `http://127.0.0.1:8098/verify-om-chat-maint-20261027/r1/` (frame 17).

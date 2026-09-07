# Your om and the Agent Center

The two agent doors in the rail. **Your om** is your own daemon-backed
assistant; **Agents** is the Agent Center, where other people's agents ask for
access and yours are wired up. `#653` grew the om side enormously — session
rail, settings and a watches surface, some 13k lines — and almost none of it is
reachable from the fixture lane. Read the gotchas before planning a proof.

## Sub-features

- The rail doors: `button` **"Your om"** and `button` **"Agents"** — but the
  names carry app mode, becoming **"Your om, not running"** and
  **"Agents, not running"** when `session.mode === "away"`, which the fixture
  can set with `?mode=away`. An `--exact` match on the bare name misses there.
  Note this is whole-app away mode, a different thing from the daemon not
  running.
- Your om: the running conversation, and its *not-running* empty state.
- The running om's four sub-surfaces, held in one local `surface` state:
  **conversation** (the chat), **compose** (the new-session landing),
  **watches**, and **settings**. `#783` collapsed the original alerts and
  schedules panes into watches — `OmAlertsSurface.tsx` and
  `OmSchedulesSurface.tsx` are deleted, `OmWatchesSurface.tsx` replaces both.
  Watches has its own file, [your-om-watches.md](your-om-watches.md).
- The Agent Center roster: your agents, their access level, and
  **"+ Wire an agent"**.
- The consent queue: agents asking for access, with Allow / No, and the
  review pair Accept / Reject.
- Entry points out: "Message", "Agent settings", "How agents work", and the
  pointer that server apps live in server settings.

## How to get to it (user POV)

Top of the rail there are two faces. **Your om** opens your own assistant —
or tells you it is not running and how to start it. **Agents** opens a board of
everything agentic around you: who is waiting on a decision, which agents you
have wired, and what each is allowed to touch.

## Driving it with control-om-chat

Two harnesses, and they reach different halves.

| Route | State |
|---|---|
| `shell-fixture.html?view=agent` | Your om — **only** the not-running empty state |
| `shell-fixture.html?view=agents` | The Agent Center roster inside the shell |
| `agent-center-fixture.html` | The Agent Center standalone, with a seeded consent queue |
| `agent-center-fixture.html?state=desk-off` | The same, still assembling ("assembling the roster…") |

Handles that resolve today, in the shell at `?view=agents`:

```bash
agent-browser find role button click --name "Your om"
agent-browser find role button click --name "Agents"
agent-browser find role button click --name "How agents work"
agent-browser find role button click --name "Agent settings"
agent-browser find role button click --name "+ Wire an agent"
```

And in the standalone `agent-center-fixture.html`, which is where the
decision surface actually has content:

```bash
agent-browser find role button click --name "Allow"     # consent card
agent-browser find role button click --name "No"
agent-browser find role button click --name "Review"
agent-browser find role button click --name "Accept"
agent-browser find role button click --name "Reject"
agent-browser find role button click --name "Open om"
```

Its header reads `WAITING ON YOU · 4`, which is the cheap observation that the
queue seeded at all.

## Gotchas

- **The fixture cannot show a running om.** `?view=agent` renders the empty
  state — `h1` *"om isn't running"*, *"No recent daemon snapshot is available on
  this device"*, and an `om serve` hint — and there is no parameter to change
  that. The shell fixture reads over a hundred query parameters and **none** of
  them seed a daemon snapshot, om session, watch or schedule. It is stronger
  than a missing stub: the gate reads `presence.running`, which comes from a
  real `fetchOmHealth()` network call with no fixture hook at all, so no
  parameter *could* be added to the fixture alone to get past it. (Do not be
  fooled by `?alerts=`, which seeds the unrelated room price-alert feed.) So the whole
  `#653` surface (session sidebar, compose, watches, om settings) is
  `verified-unreachable` from this lane; the unmet prerequisite is a running
  daemon, which means the daemon-served rig, not the fixture.
- **`agent-center-fixture.html` is a real harness, despite where it sits.**
  It opens standalone and renders the consent queue with content. Its
  vocabulary is only `state=desk-off`, `theme` and `zoom` — no `?view=`, no
  `?panel=`, none of the shell fixture's grammar. Do not carry shell-fixture
  query habits over to it.
- **Two "Agents" strings, different things.** The rail door is `"Agents"`; the
  user-settings page is `"Agent Settings"`; the Agent Center's own link out is
  `"Agent settings"` in sentence case. An `--exact` match on the wrong one
  drives the wrong surface.
- Server-side apps are deliberately not here — the Agent Center says so itself
  ("server apps live in server settings →"). A missing app is a correct
  outcome, not a regression.
- On a phone both `agent` and `agents` classify to the single **om** root tab
  (see [mobile-shell-navigation.md](mobile-shell-navigation.md)); there is no
  sixth root and no takeover.

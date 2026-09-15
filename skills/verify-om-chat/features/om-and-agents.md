# Your om and the Agent Center

The two agent doors in the rail. **Your om** is your own daemon-backed
assistant; **Agents** is the Agent Center, where other people's agents ask for
access and yours are wired up. `#653` grew the om side enormously — session
rail, settings and a watches surface, some 13k lines — and almost none of it is
reachable from the fixture lane. Read the gotchas before planning a proof.

## Sub-features

- The rail doors: `button` **"Your om"** and `button` **"Agents"**, joined by
  **"Browse features"** since `#846` added its feature-catalog tile — but both
  names move with state, and the two doors do not move the same way.
  **"Your om"** becomes **"Your om, not running"** when
  `session.mode === "away"` (the fixture sets it with `?mode=away`), on
  desktop and mobile alike. **"Agents"** differs by chrome: the mobile segment
  reads **"Agents, not running"**, while the desktop rail reads
  **"Agents, needs your om running"** — and if any agent is armed the count
  wins outright and away is masked entirely, giving **"Agents, N armed"**
  (`Shell.tsx:3019-3214`). So an `--exact` match on the bare name misses three
  different ways, and matching the mobile string on desktop misses too. Away
  is a whole-app state, a different thing from the daemon not running.

  On desktop there is a **third** state neither of those covers:
  `#829` made the rail label its destinations during a reconnect, so both
  doors carry a `railUnsettled` spelling — **"Your om, reconnecting"**
  (`Shell.tsx:3143`) and, crossing armed × away × reconnecting,
  **"Agents, N armed, reconnecting"** / **"Agents, reconnecting"**
  (`Shell.tsx:3209-3214`). Two states is the old shape; matching on it during a
  flaky connect misses silently.

  `#846` made rail zone 1 customizable, which raises an obvious question about
  these two doors: the answer is that **Agents cannot be unpinned**.
  `REQUIRED_RAIL_FEATURE_IDS = ["rail-agents"]` (`rail-layout.ts:24`) holds it
  in place while Library, News, Alerts and Browse channels became optional. A
  missing Agents door is a regression, never a layout preference.
- Your om: the running conversation, and its *not-running* empty state.
- The running om's **three** sub-surfaces, held in one local `surface` state:
  **conversation** (the chat), **compose** (the new-session landing), and
  **watches** (`ChatPane.tsx:478`). Settings used to be the fourth and is not
  any more: `c40dbc5d` turned it into a rail row that calls
  `session.requestSettings?.("om")` (`ChatPane.tsx:523`), which opens the
  **global Settings dialog** on its new OM Settings page.
  `surface === "settings"` appears nowhere in `src/`. `#783` collapsed the
  original alerts and schedules panes into watches — `OmAlertsSurface.tsx` and
  `OmSchedulesSurface.tsx` are deleted, `OmWatchesSurface.tsx` replaces both.
  Watches has its own file, [your-om-watches.md](your-om-watches.md).
- The Agent Center roster: your agents, their access level, and
  **"+ Wire an agent"**. This page has had a door bolted on and torn off twice
  in a fortnight, so trust the routes below rather than any remembered control:
  `#792` gave `?view=agents` a `role="tab"` pair, `#807` replaced it with a
  `nav` named "Agent pages" holding a span and a "Voice & away" button, and
  `#830` removed that nav altogether. On `40c7ff0f` there is **no** "Agent
  pages" nav, no tablist and no "Voice & away" button anywhere on
  `?view=agents`.

  What `#830` put in its place is the Agent Center's own context rail — an
  `aside` named **"Agent roster"** holding a `nav` named **"Roster sections"**
  with three buttons, **Roster**, **Waiting on you** and **In progress**
  (`AgentCenterPane.tsx:582-625`), plus a separate `button` named **"Persona"**
  (`:654`). Driven in this lane the nav reads exactly those three names and the
  Persona button is present. But read the trap in the Gotchas before clicking
  it: it navigates correctly and still lands on a failure, because the fixture
  decided about mocking before you clicked.

  What survives churn is the routing. `?view=agent&panel=voice|away|activity`
  each land directly, and `#830` renamed what they render: the surface heading
  is now **"Persona"**, and beneath it `voice` reads "Voice" / "Current",
  `away` reads "Research om is covering you", and `activity` reads "Away
  activity" — all three measured on the mocked route. The older "Voice & away",
  "Away coverage" and "Activity" headings are gone.

  **"Your voice" is the exception, and it is a diagnostic.** It survives in
  `PersonaPanel.tsx` as the heading of exactly two states — loading (`:903`)
  and load-failed (`:916`). It never appears over a loaded profile. So an `h1`
  reading "Your voice" is not a stale heading to write down; it is the panel
  telling you the profile did not load, and on this lane that almost always
  means the route problem below.

  Where the three tabs live depends on chrome. On **desktop**, with the om
  session rail mounted, `VoiceAwayPanel` takes `navigation="external"` and
  renders no tabs of its own — `.persona-hub-tabs` is absent and the controls
  live in the rail as `.om-session-persona-nav`
  (`AgentSessionRail.tsx:1180`), each carrying `data-om-nav-persona-view`.
  Only on **mobile** does the panel render its own `.persona-hub-tabs`
  (`PersonaPanel.tsx:114`). Both are named "Persona sections", so the name
  alone will not tell you which one you matched — check the class.
- The consent queue: agents asking for access, with Allow / No, and the
  review pair Accept / Reject.
- Entry points out: "Message", "Agent settings", "How agents work", and the
  pointer that server apps live in server settings.
- **A second door, through Settings.** `c40dbc5d` added **OM Settings** and
  **Persona** rows to the Agents group of user settings
  (`UserSettings.tsx:249-281`), supplied by `Shell.tsx:4085-4086`. They reach
  the same two surfaces without touching the rail or the Agent Center, and
  they are why the live settings nav is twenty-one entries while the settings
  fixture shows nineteen — that fixture passes neither prop, so **this route
  is not drivable there either**
  ([settings-and-appearance.md](settings-and-appearance.md)).

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
| `shell-fixture.html?view=agents` | The Agent Center roster — the first of two Agent pages |
| `shell-fixture.html?view=agent&panel=voice` | Persona → "Voice" / "Current", mocked and loaded |
| `shell-fixture.html?view=agent&panel=away` | Persona → "Research om is covering you" |
| `shell-fixture.html?view=agent&panel=activity` | Persona → "Away activity" |
| `shell-fixture.html?view=agents&panel=persona` | **Legacy.** Redirects to `#/agent/voice` unmocked — see Gotchas |
| `agent-center-fixture.html` | The Agent Center standalone, with a seeded consent queue |
| `agent-center-fixture.html?state=desk-off` | The same, still assembling ("assembling the roster…") |

Handles that resolve today, in the shell at `?view=agents`:

```bash
agent-browser find role button click --name "Your om"
agent-browser find role button click --name "Agents"
agent-browser find role button click --name "How agents work"
agent-browser find role button click --name "Agent settings"
agent-browser find role button click --name "+ Wire an agent"

# There is no persona control on this page any more (#830 removed the nav).
# Reach the three surfaces by route instead — see the table above.
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

Its header *looks* like `WAITING ON YOU · 4`, and that is the cheap
observation that the queue seeded at all — but read it carefully. The DOM text
is sentence case, `Waiting on you · 4` (`AgentCenterWork.tsx:393`); the
capitals come from `text-transform: uppercase` on `.ac-section-h`
(`agent-center.css:209`). `innerText` applies the transform and hands you the
shouted version, while `textContent` and the accessibility tree hand you the
real one. Match the sentence-case string, or a screenshot, never the caps.

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
- **Persona is unreachable from a `view=agents` page load — by any control,
  not just the old query.** `#807` moved the fixture's persona gate to
  `view === "agent"` (singular) with `panel` one of `voice`, `away` or `activity`;
  `panel === "persona"` appears nowhere in the fixture now. The old route still
  *looks* like it works, because the product's legacy-route handling redirects
  `#/agents?panel=persona` to `#/agent/voice` — but the fixture evaluates its
  persona gate once, synchronously, from the original query, so the redirect
  arrives after the mock was already skipped. You land on the panel with the
  real un-mocked client and it reads *"Your voice could not be loaded. Try
  again in a moment."*

  The decisive point is that this is a property of the **page load**, not of
  the spelling. `#830`'s "Persona" button is a real, correct control, and
  clicking it from `?view=agents` still lands you in the failure: driven here
  it moved the hash to `#/agent/voice` and rendered "Your voice could not be
  loaded", because the fixture had already skipped its mock when the page
  loaded under `view=agents`. Nothing you click your way to from that page can
  escape it.

  That failure is the route, not the lane, and not the button. Driven side by
  side: `?view=agents` → Persona button lands on `#/agent/voice` with the load
  failure, while `?view=agent&panel=voice` lands on the same hash and renders a
  **LOADED PROFILE**. Same hash, opposite outcome. If you see Retry or an `h1`
  of "Your voice", fix the URL you opened — do not click, and do not conclude
  anything about the product.
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

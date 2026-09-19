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
  (`Shell.tsx:3051-3706`). So an `--exact` match on the bare name misses three
  different ways, and matching the mobile string on desktop misses too. Away
  is a whole-app state, a different thing from the daemon not running.

  On desktop there is a **third** state neither of those covers:
  `#829` made the rail label its destinations during a reconnect, so both
  doors carry a `railUnsettled` spelling — **"Your om, reconnecting"**
  (`Shell.tsx:3706`) and, crossing armed × away × reconnecting,
  **"Agents, N armed, reconnecting"** / **"Agents, reconnecting"**
  (`Shell.tsx:3051-3056`). Two states is the old shape; matching on it during a
  flaky connect misses silently.

  `#846` made rail zone 1 customizable, which raises an obvious question about
  these two doors: the answer is that **Agents cannot be unpinned**.
  `REQUIRED_RAIL_FEATURE_IDS = ["rail-agents"]` (`rail-layout.ts:24`) holds it
  in place while the rest became optional. `RAIL_FEATURE_IDS` is now
  `rail-agents`, `rail-library`, `rail-news`, `rail-alerts`
  (`rail-layout.ts:17-22`) — **Browse channels is no longer among them.**
  `38d0c72d`'s T145 retired it from the catalog because it already has a
  permanent dock door, and a stored pin for it is purged on the next write.
  Driven here, the "Browse features" popover offers exactly **Library** and
  **Alerts**. A missing Agents door is a regression, never a layout
  preference; a missing Browse-channels *tile* is the intended state.
- **Collapsible space groups** in the rail, new in `38d0c72d` (T102). Space
  tiles can be collected into a folder: a collapsed group renders one tile with
  a 2x2 preview and a single aggregated mention badge, expands in place, and
  persists device-locally while the server keeps the flattened order. Markers
  are `data-rail-group-id`, `data-rail-group-collapsed` (present only while
  collapsed) and `.rail-group-open` on the expanded container
  (`Shell.tsx:3773-3797`).

  **It takes two steps to reach, and neither is a query parameter.** The
  fixture seeds one space, so there is nothing to group, and the layout is
  device-local rather than fixture-seeded. Both halves are solvable:

  ```bash
  # 1. populate the rail — ?rail=many gives s1..s7
  agent-browser open "$(./control-om-chat url 'tools/visual/shell-fixture.html?rail=many')"

  # 2. write the layout under the fixture user, then reload
  agent-browser eval '(()=>{localStorage.setItem("om.chat.railLayout.device.u1",
    JSON.stringify({version:1,features:[{kind:"item",id:"rail-agents"}],
    spaces:[{kind:"group",id:"g1",name:"Work",members:["s2","s3","s4","s5"]},
            {kind:"item",id:"s1"},{kind:"item",id:"s6"},{kind:"item",id:"s7"}],
    collapsed:["g1"]}));return "seeded";})()'
  ```

  The key is `om.chat.railLayout.device.<userId>` and the fixture's Kyle is
  **`u1`** (`shell-fixture.tsx:1037` maps the `kyle` handle to `u1`; every
  other handle becomes `u-<handle>`). Write it under the wrong id and nothing
  happens, silently. Proven end to end on lane 18118: after the reload one
  `[data-rail-group-id="g1"]` renders collapsed and labelled *"Work"*, and
  clicking it drops `data-rail-group-collapsed`, mounts `.rail-group-open`,
  and reveals member tiles `s2`–`s5`.

  Like `message=cozy`, this write is **sticky** — it is the app's own
  persistence, not a fixture seed, so it survives every later load in that
  browser session. Remove the key before capturing any other rail frame.
- Your om: the running conversation, and its *not-running* empty state.
- The running om's **three** sub-surfaces, held in one local `surface` state:
  **conversation** (the chat), **compose** (the new-session landing), and
  **watches** (`ChatPane.tsx:480`). Settings used to be the fourth and is not
  any more: `c40dbc5d` moved it to the global Settings dialog, and
  `38d0c72d`'s F18 then **removed the OM settings and Persona rows from the om
  home rail entirely** as duplicates. `ChatPane` no longer calls
  `requestSettings` at all, and `surface === "settings"` appears nowhere.
  The only way in is Settings itself (below). `#783` collapsed the
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
  (`AgentCenterPane.tsx:576-620`), plus a separate `button` named **"Persona"**
  (`:651`). Driven in this lane the nav reads exactly those three names and the
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

  **The tabs no longer move with the chrome — that split is gone.** Until
  `38d0c72d` desktop suppressed the panel's own tabs and rendered them in the
  rail as `.om-session-persona-nav`. F18 deleted that nav: the class appears
  nowhere in `packages/chat-ui/src/` now, and `VoiceAwayPanel` passes
  `navigation="inline"` unconditionally (`PersonaPanel.tsx:171`). Direct
  persona routes got their own inline header, tabs and **Back** control
  instead.

  Driven at 1440x900 on `?view=agent&panel=voice`: `.persona-hub-tabs` is
  **present** on desktop, `.om-session-persona-nav` is absent, a Back button
  is there, and the tabs read **Voice / Away coverage / Activity**
  (`PersonaPanel.tsx:114`). Note "Away coverage" survives as a *tab* label
  even though it is no longer a heading — matching it proves the tab strip,
  not the panel you landed on.
- The consent queue: agents asking for access, with Allow / No, and the
  review pair Accept / Reject.
- Entry points out: "Message", "Agent settings", "How agents work", and the
  pointer that server apps live in server settings.
- **A second door, through Settings.** `c40dbc5d` added **OM Settings** and
  **Persona** rows to the Agents group of user settings
  (`UserSettings.tsx:258-290`), supplied by `Shell.tsx:4448-4449`. They reach
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

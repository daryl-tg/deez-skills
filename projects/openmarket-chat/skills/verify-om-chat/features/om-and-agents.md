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
  **"Agents, needs your om running"**. An armed count does not mask away: the
  desktop label states both, **"Agents, N armed, your om is not running"**,
  and only a connected, armed om reads the bare **"Agents, N armed"**
  (`Shell.tsx:3054-3068`; mobile segments `Shell.tsx:3572-3624`). So an
  `--exact` match on the bare name misses several different ways, and matching
  the mobile string on desktop misses too. Away is a whole-app state, a
  different thing from the daemon not running.

  On desktop there is a **third** state neither of those covers:
  `#829` made the rail label its destinations during a reconnect, so both
  doors carry a `railUnsettled` spelling — **"Your om, reconnecting"**
  (`Shell.tsx:3745`) and, crossing armed × away × reconnecting,
  **"Agents, N armed, reconnecting"** / **"Agents, reconnecting"**
  (`Shell.tsx:3059`, `:3064`). Two states is the old shape; matching on it
  during a flaky connect misses silently.

  **Away has a remote-control spelling too.** When the session is away and a
  remote device answers over the relay, the doors read
  **"Your om, connected remotely"** and **"Agents, connected remotely"**, or
  **"…, remote control off"** when a device is reachable but none is selected
  (`Shell.tsx:1507-1511`; accessible names at `:3066`, `:3585`, `:3610`,
  `:3747`). The tooltips spell it with a colon instead, "Agents: connected
  remotely" (`:3043`, `:3729`), so match the name, not the tooltip. The shell fixture cannot show it: its session stub
  answers `remoteControl: () => null` (`shell-fixture.tsx:4034`). The pane
  those labels point at is driven standalone; see **Remote control** below.

  `#846` made rail zone 1 customizable, which raises an obvious question about
  these two doors: the answer is that **Agents cannot be unpinned**.
  `REQUIRED_RAIL_FEATURE_IDS = ["rail-agents"]` (`rail-layout.ts:24`) holds it
  in place while the rest became optional. `RAIL_FEATURE_IDS` is
  `rail-agents`, `rail-library`, `rail-news`, `rail-alerts`,
  `rail-browse-channels` (`rail-layout.ts:17-23`).

  **Browse channels has been retired and restored within a week — do not trust
  either memory of it.** `38d0c72d`'s T145 retired it from the catalog; `#940`'s
  F64 reversed that on request, making it *"pinnable and unpinned by default,
  like Library"*. Driven at `f7d7c987`, the "Browse features" popover ("Add to rail") offers
  **Library**, **Alerts** and **Browse channels**. Unpinned is its default, so
  an absent Browse tile on the rail is correct; an absent catalog *entry* is
  not. A missing Agents door is a regression, never a layout preference.

  `#940`'s T103 also extended folders to zone 1: feature tiles can now be
  grouped exactly like spaces, because `RailLayout.features` holds the same
  `RailNode` union (`item` or `group`) as `spaces`. The seeding recipe below
  works for both — put the `group` node in `features` instead. Proven at
  `f7d7c987`: a `features` group of `rail-library` and `rail-alerts` named
  "Tools" renders as one collapsed `[data-rail-group-id="fg1"]` in zone 1.
- **Collapsible space groups** in the rail, new in `38d0c72d` (T102). Space
  tiles can be collected into a folder: a collapsed group renders one tile with
  a 2x2 preview and a single aggregated mention badge, expands in place, and
  persists device-locally while the server keeps the flattened order. Markers
  are `data-rail-group-id`, `data-rail-group-collapsed` (present only while
  collapsed) and `.rail-group-open` on the expanded container
  (`Shell.tsx:3993-4025` for spaces; the zone-1 feature folders use the same
  markers at `Shell.tsx:3813-3841`).

  **It takes two steps to reach, and neither is a query parameter.** The
  fixture seeds one space, so there is nothing to group, and the layout is
  device-local rather than fixture-seeded. Both halves are solvable:

  ```bash
  # 1. populate the rail — ?rail=many gives s1..s7
  agent-browser open "$(control-om-chat url 'tools/visual/shell-fixture.html?rail=many')"

  # 2. write the layout under the fixture user, then reload
  agent-browser eval '(()=>{localStorage.setItem("om.chat.railLayout.device.u1",
    JSON.stringify({version:1,features:[{kind:"item",id:"rail-agents"}],
    spaces:[{kind:"group",id:"g1",name:"Work",members:["s2","s3","s4","s5"]},
            {kind:"item",id:"s1"},{kind:"item",id:"s6"},{kind:"item",id:"s7"}],
    collapsed:["g1"]}));return "seeded";})()'
  ```

  The key is `om.chat.railLayout.device.<userId>` and the fixture's Kyle is
  **`u1`** (`shell-fixture.tsx:1049` maps the `kyle` handle to `u1`; every
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
  **watches** (`ChatPane.tsx:483`). Settings used to be the fourth and is not
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

  **Since `#978` persona lives inside Agents, not beside it.** The Agent
  Center's context rail is an `aside` named **"Agent roster"**
  (`AgentCenterPane.tsx:745`) holding, top to bottom:

  - a `nav` named **"Roster sections"** (`:759`) — **Roster**, **Waiting on
    you, N**, **In progress, N** (the counts ride the accessible names);
  - a group named **"Persona"** holding a `nav` named **"Persona sections"**
    (`AgentCenterPane.tsx:806-810`) — **Voice**, **Away coverage, off**
    (state in the name again), **Activity**;
  - a `nav` named **"Agents"** — **Open your om**, then one row per helper
    badge when any are seeded.

  The standalone **"Persona" button** that `#830` added is **gone**; the three
  persona rows replaced it. Every roster section and every badge now has its
  own route too: `#/agents/voice|away|activity`, and `#/agents/badge/<id>` for
  a helper's own page with its full ledger (`BadgeDetail`). Read the trap in
  the Gotchas before clicking any of it from a `?view=agents` load.

  Routing is still what survives churn, but the hash moved: persona is now
  **`#/agents/<section>`**, plural, where it was `#/agent/<section>`. The
  heading is **"Persona"**, and beneath it `voice` reads "Voice" / "Current",
  `away` reads "Research om is covering you", and `activity` reads "Away
  activity" — measured on the mocked routes at `f7d7c987`. The older "Voice &
  away" heading stays gone.

  **"Your voice" is the exception, and it is a diagnostic.** It survives in
  `PersonaPanel.tsx` as the heading of exactly two states — loading (`:895`)
  and load-failed (`:908`). It never appears over a loaded profile. So an `h1`
  reading "Your voice" is not a stale heading to write down; it is the panel
  telling you the profile did not load, and on this lane that almost always
  means the route problem below.

  **Where the three persona tabs render has now moved three times** — the
  panel's own strip, then the om session rail (`.om-session-persona-nav`,
  deleted by `38d0c72d`), then the panel's strip again, and since `#978` the
  Agents sidebar's "Persona sections" group. Driven at 1440x900 on
  `?view=agent&panel=voice`: `.persona-hub-tabs` is **absent** and
  `.om-session-persona-nav` is absent; the only persona controls are the
  sidebar rows. `.persona-hub-tabs` still exists in source
  (`PersonaPanel.tsx:123`) behind `navigation = "inline"` (`:84`), but no route
  in this lane renders it. Match the sidebar group by name, not either class.
  "Away coverage" survives as a *row* label after ceasing to be a heading, so
  matching it proves the sidebar, not the panel you landed on.
- The consent queue: agents asking for access, with Allow / No, and the
  review pair Accept / Reject.
- Entry points out: "Message", "Agent settings", "How agents work", and the
  pointer that server apps live in server settings.
- **OM Settings, through Settings.** `c40dbc5d` added **OM Settings** and
  **Persona** rows to the Agents group of user settings; `#978` then **retired
  the Persona row** ("now that Agents is its home"), so only **OM Settings**
  remains (`UserSettings.tsx:282-298`), supplied by `Shell.tsx:4492`. That is
  why the shell's settings nav is **twenty** entries while the settings
  fixture shows nineteen — the settings fixture does not pass `omPage`. Open
  it through the shell instead:
  `shell-fixture.html?view=settings&settingsPage=appearance` renders all
  twenty, OM Settings included (measured at `f7d7c987`). See
  [settings-and-appearance.md](settings-and-appearance.md).
- **Remote control (away).** `RemoteHome` in `RemoteControlPane.tsx` is the om
  pane of an away session that drives a desktop's om over the relay. It
  reuses the session rail with **no Watches destination**
  (`showWatches={false}`, `RemoteControlPane.tsx:129`: the cloud pane has no
  watch RPC), the shared tool-activity presentation, and a composer with an
  **"Add context"** button that opens `OmComposerContextPopover` for picking
  a doc, channel or topic reference. That button renders only on a private om
  composer with no lane toggle and no target (`Composer.tsx:3831`, `:5163`),
  so the shell fixture's not-running om never shows it.

## How to get to it (user POV)

Top of the rail there are two faces. **Your om** opens your own assistant —
or tells you it is not running and how to start it. **Agents** opens a board of
everything agentic around you: who is waiting on a decision, which agents you
have wired, and what each is allowed to touch.

## Driving it with control-om-chat

Three harnesses, and they reach different parts.

| Route | State |
|---|---|
| `shell-fixture.html?view=agent` | Your om — **only** the not-running empty state |
| `shell-fixture.html?view=agents` | The Agent Center roster — the first of two Agent pages |
| `shell-fixture.html?view=agent&panel=voice` | Agents → `#/agents/voice`, "Voice" / "Current", mocked and loaded |
| `shell-fixture.html?view=agent&panel=away` | Agents → `#/agents/away`, "Research om is covering you" |
| `shell-fixture.html?view=agent&panel=activity` | Agents → `#/agents/activity`, "Away activity" |
| `shell-fixture.html#/agents/voice` | The same Voice page from the bare hash — mocked, loads |
| `shell-fixture.html#/agents/away` | **Not** the seeded coverage: reads "Away coverage unavailable". Use `?view=agent&panel=away` |
| `shell-fixture.html?view=agents&panel=persona` | **Legacy.** Lands on `#/agents/voice` unmocked — see Gotchas |
| `shell-fixture.html#/agent/voice` | **Legacy** singular hash. Same unmocked failure |
| `agent-center-fixture.html` | The Agent Center standalone, with a seeded consent queue |
| `agent-center-fixture.html#/agents/badge/agcr_claude` | A helper's own page (`BadgeDetail`) — also `agcr_backtest`, `agcr_research` |
| `agent-center-fixture.html?state=desk-off` | The same, still assembling ("assembling the roster…") |
| `remote-home-fixture.html?state=<s>` | The away remote-control pane. `snapshot`, `older` (Load older), `recovering`, `approval` (Approve / Deny), `live` (Stop), `empty` (greeting and prompts), `unsupported` ("Conversation history is not supported by this device") |

Handles that resolve today, in the shell at `?view=agents`:

```bash
agent-browser find role button click --name "Your om"
agent-browser find role button click --name "Agents"
agent-browser find role button click --name "How agents work"
agent-browser find role button click --name "Agent settings"
agent-browser find role button click --name "+ Wire an agent"

# Persona rows sit in the sidebar's "Persona sections" group (#978), but
# clicking them from a ?view=agents load fails — see Gotchas. Use the routes.
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
is sentence case, `Waiting on you · 4` (`AgentCenterWork.tsx:392`); the
capitals come from `text-transform: uppercase` on `.ac-section-h`
(`agent-center.css:231`). `innerText` applies the transform and hands you the
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
  not just the old query.** The fixture decides whether to mock persona
  **once, at page load** (`shell-fixture.tsx:192-204`): it mocks when the query
  is `view=agent&panel=voice|away|activity` *or* the hash is already
  `#/agents/voice|away|activity`. Anything that only *arrives* at those hashes
  after load finds the real, un-mocked client and reads *"Your voice could not
  be loaded. Try again in a moment."*

  That rules out every in-page path. Driven at `f7d7c987` from a `?view=agents`
  load, the sidebar's **Voice** row moves the hash to `#/agents/voice` and
  fails. So does the legacy `?view=agents&panel=persona`, and so does the old
  singular hash `#/agent/voice`: both are rewritten to `#/agents/voice` after
  load, too late for the mock. (The fixture's own comment says nothing in it
  redirects an old hash; something does, observably — believe the drive.)

  That failure is the route, not the lane, and not the control. Driven side by
  side: the Voice row lands on `#/agents/voice` with the load failure, while
  opening `#/agents/voice` directly lands on the same hash and renders a
  **LOADED PROFILE**. Same hash, opposite outcome. If you see Retry or an `h1`
  of "Your voice", fix the URL you opened — do not click, and do not conclude
  anything about the product.
- **`agent-center-fixture.html` is a real harness, despite where it sits.**
  It opens standalone and renders the consent queue with content. Its query
  vocabulary is `state=desk-off`, `theme` and `zoom` — no `?view=`, no
  `?panel=` — but since `#978` it also routes **hashes**:
  `#/agents/badge/agcr_claude`, `agcr_backtest` or `agcr_research` opens that
  helper's `BadgeDetail` page (rename, "Live now · on desk", the ledger), with
  the three helpers listed in the sidebar's "Agents" nav. It is the only lane
  here that seeds helper badges; the shell fixture's roster holds om's card
  alone, so badge pages are unreachable there. `tools/visual/agent-center.visual.ts`
  is the maintained recipe.
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

### Verification record

**Last verified:** 2026-10-01. **Product commit:** `f8b68bf762cfa347b7f588f6fc94eb78b631381b`. **Scope:** opened Agent Center with its seeded four-item waiting queue and RemoteHome live with Stop/Add context; Your om standalone showed its not-running state. **Limitations:** Consent decisions, all persona/roster states, and connected daemon behavior were not exercised.

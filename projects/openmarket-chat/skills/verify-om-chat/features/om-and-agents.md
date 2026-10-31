# Your om and the Agent Center

The two agent doors in the rail. **Your om** is your own daemon-backed
assistant; **Agents** is the Agent Center, where other people's agents ask for
access and yours are wired up. `#653` grew the om side enormously — session
rail, settings and a watches surface, some 13k lines — and almost none of it is
reachable from the fixture lane. Read the gotchas before planning a proof.

## Sub-features

**The Agents page (on origin/main since `3e9c88f3`).** The Map and Grid
redesign replaced the old Agent Center: `components/agents/*` and
`lib/agents/*` are new, and `AgentCenterPane.tsx` was rewritten. The old
**Roster** h1, the **Roster sections** nav and **Waiting on you** are gone from
main. Driven on main at `47cb13bf` (2026-10-30).

- **Home.** h1 **"Agents"**, a **Map / Grid** segmented toggle (`aria-pressed`),
  **Templates**, **New agent**, **How agents work** and **Inbox**. The sidebar
  `aside` is **"Agents sidebar"** (`AgentCenterPane.tsx:1120`). Its `nav`
  **"Agents sections"** (`:1167`) holds **All agents, N**, **Needs you, N** and
  **Running, N** (counts in the names; 8 / 9 / 3 on the default
  `agent-center-fixture`). PERSONA is unchanged, and AGENTS lists every agent
  with om first (`Open <name>, <state>`, e.g. **Open argue, 2 need you**).
  Map is the default above the shell's inclusive 768px phone query, and Grid is
  the default at or below it. The choice is device-local under
  `om.chat.agentsView`. Search and the Map's **+N** cards show Grid without
  writing it. Ready markers are `.agents-map.is-ready` and
  `.agents-grid-view.is-ready`.
- **Map.** A region named **"Agents map"**. Node ids sit on `data-node` (`you`,
  `b-om`, `cl-chat`, `ag-<id>`, `r-<roomId>`, `ask-<key>`), and hover or focus
  traces one hop. Regions **House agents**, **Chat agents**, **Work agents**,
  **Connected agents**, **Rooms** (`Open #<room>`), **Library** and
  **Projects**. Ask cards carry only **Review** and a decline (**Deny**,
  **Forget**, **Keep argue at 1.0.0**), each named for its ask, e.g.
  **Review, claude code asks for access**. There is no approve on the Map by
  design. **Show all 9 in Needs you** leads to the feed.
- **Grid.** A region named **"Agents grid"**: a `your om` card, an h2 **Your
  agents**, filter toggles **All / Chat / Work / Connected**, a combobox
  **Sort agents** (default **Name**) and one card per agent with an h3 name.
  The **Get work agents running** setup checklist sits above it.
- **Needs you.** `#/agents/waiting`, h1 **"Needs you"**. A pending `@om-skills`
  update renders here as a region **Update for <name>** with **Approve <name>
  update** and **Keep <name> at <version>** (`agents/NeedsYou.tsx:872`). The
  consent rows' labels are `Allow`, `Accept` and `Reject`
  (`agents/NeedsYou.tsx:274-311`); on `?roster=none` the visible pair is
  **Allow** / **Deny**. On the default fixture the feed's buttons read, in
  order: **Review**; **Approve argue update** / **Keep argue at 1.0.0**;
  **Allow** / **No** (two knocks); **Yes, remember it** / **No, forget it**;
  **Dismiss: <text>** (two); a **Coding Plan review** region with **Review
  Plan**; and **Accept** / **Reject** for the doc proposal. Pressed
  2026-10-30 on `/rooms/`: **Allow** took **Needs you** from 9 to 8, **Approve
  argue update** and **Yes, remember it** to 6, and a **Dismiss** to 5. Each
  row settles after about a second. **Accept** changed nothing, because the
  fixture scripts no proposal accept route.
- **Agent page.** `#/agents/a/<id>` on `/rooms`, `/chat/agents/a/<id>` on cloud.
  Old `#/agents/badge/<id>` addresses rewrite there (`src/lib/routing.ts:292-295`).
  Top bar: **Back to agents**, h1 `<name>`, a `switch` **Run <name>** and a
  **More actions for <name>** menu (**Review replies first**, **Check
  routing**, **Review what it learned**). Its `tablist` holds **Overview,
  Activity, Access, Settings**; every panel is in the DOM and the unselected
  ones are `hidden`, so read the visible `tabpanel`. A region **Talk to <name>**
  holds the textbox **Ask <name> something** and a disabled **Try it**.
- **New agent.** A dialog named **New agent** on desktop and a bottom sheet on
  phone. Groups **Agent type** (**Chat agent**, **Work agent**) and **Agent
  templates** (explain, fact-check, argue, debugger, feature), **Start blank**
  (chat only), **Cancel**, **Import** and **Continue**. Escape closes it and
  returns focus to **New agent**. **Continue** opens the inline **Create an
  agent** form ([agent-creator.md](agent-creator.md)). Cloud shows a hosted
  notice instead.

**Recipe.** On `agent-center-fixture.html` (the roster host is seeded on main,
`tools/visual/agent-center-fixture.tsx:803`), use `?theme=light` for light.
Media emulation alone does not switch the theme. The cloud host is
`/chat/tools/visual/shell-fixture.html?view=agents&alerts=quiet`. It routes to
`/chat/agents` and shows the Map with om only, the Brains nodes reading
"can't tell", and "Create and manage your agents in the local app. Agents
connected to this server appear here."

**Trap.** The phone sheet (New agent, an agent's details) drags only from
`[data-sheet-grip]` or the dialog header (`lib/agents/sheet-drag.ts`).
`agent-browser mouse down/move/up` on the grip did not move it at 390 px.
In-page `PointerEvent`s did: `pointerdown` on the grip, then `pointermove` and
`pointerup` on `window`. A pull of about half the sheet's height dismisses it,
and a short pull springs back. Under host load the exit can take several
seconds, so re-check before you call a dismiss failed.

**Trap.** The Map / Grid choice is sticky, like `message=cozy`. Pressing
**Grid** writes `om.chat.agentsView` to `localStorage`, and every later load on
that origin opens on Grid. That includes `agent-center-fixture` with another
query and the shell's `?view=agents`. Remove the key before you capture a
default frame:
`agent-browser eval 'localStorage.removeItem("om.chat.agentsView")'`.

**Trap.** "Activity" names two controls on an agent page: the PERSONA rail row
and the page tab. A text match clicks the rail row and lands on
`#/agents/activity`. Use `find role tab click --name "Activity"`.

**Trap.** `tools/visual/mobile-release-readiness.visual.ts` needs a live stack
behind `/api`. On an agent lane with the parity stack down, `GET /api/away`
502s from Shell and ChatPane, and the health contract fails the navigation case
before the matrix runs. That is the environment, not the product.

**Agent creation, import, sharing and guided work are on origin/main since
`01bf4481`.** `AgentCenterSurface.tsx`, `components/roster/` and
`lib/roster-*.ts` landed there; see [agent-creator.md](agent-creator.md) for
the creator, its fixture door (`agent-center-fixture.html` → **New agent**)
and the live-lane prerequisites. **+ Wire an agent** (`AgentCenterPane.tsx:1407`)
still opens Agent Settings; it is not the creator entry point. The shell
fixture's `?view=agents` scripts no roster host: it shows only the `your om`
card, **+ Wire an agent** and "server apps live in server settings →".

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
  (`Shell.tsx:3098-3113`; mobile segments `Shell.tsx:3626-3671`). So an
  `--exact` match on the bare name misses several different ways, and matching
  the mobile string on desktop misses too. Away is a whole-app state, a
  different thing from the daemon not running.

  On desktop there is a **third** state neither of those covers:
  `#829` made the rail label its destinations during a reconnect, so both
  doors carry a `railUnsettled` spelling — **"Your om, reconnecting"**
  (`Shell.tsx:3799`) and, crossing armed × away × reconnecting,
  **"Agents, N armed, reconnecting"** / **"Agents, reconnecting"**
  (`Shell.tsx:3104`, `:3109`). Two states is the old shape; matching on it
  during a flaky connect misses silently.

  **Away has a remote-control spelling too.** When the session is away and a
  remote device answers over the relay, the doors read
  **"Your om, connected remotely"** and **"Agents, connected remotely"**, or
  **"…, remote control off"** when a device is reachable but none is selected
  (`Shell.tsx:1551`; accessible names at `:3111`, `:3638`, `:3663`,
  `:3801`). The tooltips spell it with a colon instead, "Agents: connected
  remotely" (`:3088`, `:3783`), so match the name, not the tooltip. The shell fixture cannot show it: its session stub
  answers `remoteControl: () => null` (`shell-fixture.tsx:4144`). The pane
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
  (`Shell.tsx:4041-4084` for spaces; the zone-1 feature folders use the same
  markers at `Shell.tsx:3861-3899`).

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
  **`u1`** (`shell-fixture.tsx:1068` maps the `kyle` handle to `u1`; every
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
  **watches** (`ChatPane.tsx:477`). Settings used to be the fourth and is not
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

  On product HEAD `231c95f4`, **+ Wire an agent** opens Settings → Agent
  Settings (the source fixture shows the install-OM notice). It is not a local
  creator, import, or catalog flow; those flows are absent from this product
  tree and are not covered here.

  **Since `#978` persona lives inside Agents, not beside it.** Since
  `3e9c88f3` the context rail is an `aside` named **"Agents sidebar"**
  (`AgentCenterPane.tsx:1120`) holding, top to bottom:

  - a `searchbox` **Search agents**;
  - a `nav` named **"Agents sections"** (`:1167`) — **All agents, N**, **Needs
    you, N**, **Running, N** (the counts ride the accessible names);
  - a group named **"Persona"** (`:1212`) holding a `nav` named **"Persona
    sections"** (`:1216`) — **Voice**, **Away coverage, off** (state in the
    name again, `:258-272`; with no away snapshot after a load has failed or
    finished it reads **Away coverage, status can't tell right now** and the
    visible text **Can't tell**, which is what both the shell and agent-center
    fixtures show at `47cb13bf`), **Activity**;
  - the AGENTS list — **Open your om, <state>**, then one `Open <name>,
    <state>` row per agent.

  The standalone **"Persona" button** that `#830` added is **gone**; the three
  persona rows replaced it. Every section and every agent has its own route:
  `#/agents`, `#/agents/waiting`, `#/agents/progress`,
  `#/agents/voice|away|activity`, and `#/agents/a/<id>` for an agent's own page.
  The older `#/agents/badge/<id>` still resolves there. Read the trap in the
  Gotchas before clicking any of it from a `?view=agents` load.

  Routing is still what survives churn, but the hash moved: persona is now
  **`#/agents/<section>`**, plural, where it was `#/agent/<section>`. The
  heading is **"Persona"**, and beneath it `voice` reads "Voice" / "Current",
  `away` reads "Research om is covering you", and `activity` reads "Away
  activity" — measured on the mocked routes at `f7d7c987`. The older "Voice &
  away" heading stays gone.

  **"Your voice" is the exception, and it is a diagnostic.** It survives in
  `PersonaPanel.tsx` as the heading of exactly two states — loading (`:911`)
  and load-failed (`:924`). It never appears over a loaded profile. So an `h1`
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
  remains (`UserSettings.tsx:274`), supplied by `Shell.tsx:4552`. That is
  why the shell's settings nav is **twenty** entries while the settings
  fixture shows nineteen — the settings fixture does not pass `omPage`. Open
  it through the shell instead:
  `shell-fixture.html?view=settings&settingsPage=appearance` renders all
  twenty, OM Settings included (measured at `f7d7c987`). See
  [settings-and-appearance.md](settings-and-appearance.md).
- **Remote Control `operation` verb (on origin/main since `2a737b9e`).** Beside turns and the session rail, an away session can run named persona/away operations on the selected device: `remoteOperation(name)` in `packages/chat-ui/src/lib/remote-operation.ts`; the operator registry it reads (`registerRemoteOperator`) moved to `lib/remote-operator-registry.ts` and is re-exported. With no registered operator every call answers 503 `remote_offline`. A device advertises `operation.v1` in `hello_ack`; the daemon answers `operation.accepted` then `operation.response` parts, and the client gives up after 8 s without an accept and re-checks the desk at most every 15 s. See persona-setup-and-editing.md "Hosted /chat/ over Remote Control" for the rig.
- **Remote control (away).** `RemoteHome` in `RemoteControlPane.tsx` is the om
  pane of an away session that drives a desktop's om over the relay. It
  reuses the session rail with **no Watches destination**
  (`showWatches={false}`, `RemoteControlPane.tsx:129`: the cloud pane has no
  watch RPC), the shared tool-activity presentation, and a composer with an
  **"Add context"** button that opens `OmComposerContextPopover` for picking
  a doc, channel or topic reference. That button renders only on a private om
  composer with no lane toggle and no target (`Composer.tsx:5550-5551`),
  so the shell fixture's not-running om never shows it.

  Relay-history tool rows now prefer non-empty `personText` (the result phrased
  for the person) and fall back to `content` when it is missing or blank. Open
  **Expand tool activity** in `remote-home-fixture.html?state=live` to inspect
  the shared presentation (`tool-result-text.ts:4`, `remote-control.ts:1908,
  1914`). That seed does not provide a `personText` comparison.

## How to get to it (user POV)

Top of the rail there are two faces. **Your om** opens your own assistant —
or tells you it is not running and how to start it. **Agents** opens a board of
everything agentic around you: who is waiting on a decision, which agents you
have wired, and what each is allowed to touch.

## Driving it with control-om-chat

Three harnesses, and they reach different parts.

| Route | State |
|---|---|
| `shell-fixture.html?view=agent` | Your om — the not-running empty state, unless `/healthz*` is stubbed (see Gotchas) |
| `shell-fixture.html?view=agent&omSessions=drafts` | Local Research A/B draft seed. Reaches the rail reproducibly with the `**/healthz*` route stub (see [your-om-drafts.md](your-om-drafts.md)) |
| `shell-fixture.html?view=agent&omSessions=daemon` | Real `OmSessionState` adapter for a daemon-served lane; it does not bypass presence or provide watch data |
| `shell-fixture.html?view=agents` | The Agents page in the shell, h1 **Agents**, `#/agents`: **Map** / **Grid**, **Templates**, **New agent**, the **All agents** / **Needs you** / **Running** filters, PERSONA nodes **Voice**, **Away coverage** and **Activity**, and under AGENTS `your om`, with **OM daemon**, **Claude Code** and **Codex** each reading "can't tell" (no roster host, so no other agent; measured 2026-10-31) |
| `shell-fixture.html?view=agent&panel=voice` | Agents → `#/agents/voice`, "Voice" / "Current", mocked and loaded |
| `shell-fixture.html?view=agent&panel=away` | Agents → `#/agents/away`, "Research om is covering you" |
| `shell-fixture.html?view=agent&panel=activity` | Agents → `#/agents/activity`, "Away activity" |
| `shell-fixture.html#/agents/voice` | The same Voice page from the bare hash — mocked, loads |
| `shell-fixture.html#/agents/away` | **Not** the seeded coverage: reads "Away coverage unavailable". Use `?view=agent&panel=away` |
| `shell-fixture.html?view=agents&panel=persona` | **Legacy.** Lands on `#/agents/voice` unmocked — see Gotchas |
| `shell-fixture.html#/agent/voice` | **Legacy** singular hash. Same unmocked failure |
| `agent-center-fixture.html` | The Agents page standalone with a scripted roster host: Map (default at 1440), Grid, **Needs you, 9**, agent pages, **New agent** and a pending update for argue. Also takes `connections=none`, `roster=none`, `identity=anonymous`, `theme=light` and `zoom=200`. The old `roster=work-builder\|work-proof\|projects` values are gone; any `roster=` other than `none` renders the default (see [agent-creator.md](agent-creator.md)) |
| `agent-center-fixture.html#/agents/a/inst_argue` | An agent's own page: h1 **argue**, **Run argue**, **More actions for argue**, tabs Overview / Activity / Access / Settings. `#/agents/badge/<id>` rewrites to `#/agents/a/<id>` |
| `agent-center-fixture.html?roster=none` | No roster host: **Needs you** (Allow / Deny rows), the `your om` card and the connected agents only |
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
agent-browser find role button click --name "Grid" --exact
agent-browser find role button click --name "Needs you, 9" --exact   # -> #/agents/waiting
agent-browser find role button click --name "Open argue, 2 need you" --exact  # -> #/agents/a/inst_argue
agent-browser find role tab    click --name "Access" --exact
agent-browser find role button click --name "More actions for argue" --exact
agent-browser find role button click --name "Back to agents" --exact
agent-browser find role button click --name "New agent" --exact
```

**The fixture lands on the Map, not the queue.** Open
`agent-center-fixture.html`, then click the sidebar button **Needs you, 9**
(or load `#/agents/waiting`) before driving the consent controls. The page's h1
becomes **Needs you**. On the Map, each ask card offers only **Review** and a
decline, named for the ask (**Review, claude code asks for access**, **Deny,
claude code asks for access**). The AGENTS rail names its doors with their
state: `Open your om, idle`, `Open claude code, 2 need you`, `Open backtest
helper, connected`.

The old `Waiting on you · 4` header and its uppercase trap are gone with the
Roster page; nothing under `components/` renders that string at `47cb13bf`.

### Invite an agent to a channel (added 2026-10-28)

In a channel, open **More channel actions** (the header `…`). Its menu has 14 items on the default fixture: Join voice, Brief, Invite people, **Invite agent**, Your agents..., New topic..., Summon your om, Channel settings, Mark as read, Notification settings, Mute channel, Hide to-dos, Convert to alerts..., Copy channel link. **Invite agent** (`ChannelHeaderMenus.tsx:123`; absent in away mode) opens a dialog named **✦ Invite your agent to #ops**. With no badge wired, it reads "No agent badge is wired yet. Run the command below: it wires your Claude Code, asks for read access to this channel, and the consent card appears right here.", then shows `om claude "#ops"` with **Copy**, **Open Front Desk** and **How agents work**. No daemon is needed for this state.

`find role menuitem click --name "Invite agent"` missed the item once while the menu was still opening. Take a snapshot and click the item by its ref instead. Driven on `/rooms/` and `/chat/` 2026-10-28 at `2dd7aad1` (frames 13, 42). The wired-badge state, the consent card and the **Channel agents** panel need a daemon with a wired badge.

### Agent page panels and Fleet health (added 2026-10-31)

On `agent-center-fixture.html`, **Grid** ends in a `details.agents-health`
whose `summary` reads **Fleet health · last 24 hours** (`agents/FleetHealth.tsx:22-28`).
It is closed by default; clicking the summary opens eleven measures: duplicate
posts, recovered runs, completed per recovery, posts refused by checks, queue
wait (typical and 95%), runs interrupted, time to cancel, owner interventions
per run, updates rolled back, suggestions accepted ("not measured yet") and an
estimated API-equivalent cost.

An agent page (`#/agents/a/inst_argue`) has four tabs, **Overview**,
**Activity**, **Access** and **Settings** (there is no Sessions tab), and its
boxes are `h2.agent-box-h` (`agents/AgentPanels.tsx`): **About** (`:131`) on
Overview, **Today** (`:345`) added on Activity, and **Memory** (`:166`) with a
`role="meter"` named **Memory used** (`:181`; `aria-valuenow` 29 for argue,
re-read 2026-11-01; it is not a progressbar) added on Settings. **This hour**,
**Sessions**, **Agent settings** and **Full access** (`:203`, `:317-390`) and
the **Stop access to <label>** chips (`:253`) did not render for `argue`. Use
`find role tab`, because **Activity** is also a rail row. Driven 2026-10-31 on
`/rooms/` (18135) at `936f5b64`.

At 390×844 the agent page is full-screen (header **argue · Idle · Chat agent**,
composer **Message argue**) and its side panels live behind the kebab
**Details for argue** (`aria-haspopup="dialog"`, `AgentPage.tsx:128-146`),
which raises the **argue details** sheet: `role="dialog"` with
`.agent-sheet-head[data-sheet-grip]` and **Close details**, 591 px tall. The
sheet drags with synthetic pointer events (`lib/agents/sheet-drag.ts`):
`pointerdown` on the grip, then `pointermove` and `pointerup` on `window` with
the same `pointerId`, paced with short awaits. A 60 px pull sprang home
(`translateY(60px)` → 52.7 → 17.5 → 2.6 → `""`) and a pull past half the
height left the screen (531 → 578 → unmounted). Driven 2026-11-01 at
`936f5b64` on `/rooms/` (18137).

**The spring needs a visible page.** The settle runs on
`requestAnimationFrame`, and a page that is not the most recently created one
in the shared headless browser reports `document.hidden === true` with no rAF
ticks: there the sheet followed the finger and then froze mid-air on release.
Open a fresh session for the drag, or check `document.visibilityState` first.
The fixture also forces the `reduced-motion` class on `<html>`.

**Update for argue** is the `RosterUpdateNotice` section (`roster/RosterUpdateNotice.tsx:78`)
and mounts only in the **Needs you** feed (`agents/NeedsYou.tsx:872`), not on
the Grid card or the agent page; the fixture drops it once **Approve argue
update** or **Keep argue at 1.0.0** is pressed (`agent-center-fixture.tsx:716`).
**More actions for argue** listed two items tonight, **Check routing** and
**Review what it learned**; the 2026-10-30 record counted three.

## Gotchas

- **No query parameter bypasses the running-om gate; a route stub does.** `?view=agent` renders the empty
  state — `h1` *"om isn't running"*, *"No recent daemon snapshot is available on
  this device"* on this lane. The gate is `presence.running === false`
  (`ChatPane.tsx:517`), fed by `fetchOmHealth()` (`lib/om-health.ts`), which
  reads any 4xx except 429, or a non-JSON 200, as down. The fixture has two
  session modes: `omSessions=drafts` seeds Research A/B locally, and
  `omSessions=daemon` wires real session-list/history operations. Neither fakes
  `presence.running`. Stub it in the browser instead: `agent-browser network
  route "**/healthz*" --body '<health JSON>'` before the first open (the exact
  body is in [your-om-drafts.md](your-om-drafts.md)). The `*` also covers the
  `/healthz?lite=1` poll, which otherwise 404s and drops the gate about 30 s in.
  Proved on 2026-10-27 (maintenance re-drive). The single nightly session that
  passed without a stub was the `running === null` window, before the first
  poll answer or while the tab is hidden (`ChatPane.tsx:270`). Do not plan a
  proof on that window. The stub answers health only, so Watches still need
  daemon watch RPCs and QA watch data, and unread still needs daemon events.
- **On `/rooms/`, persona is unreachable from a `view=agents` page load — by any control,
  not just the old query.** (On `/chat/` the same Voice click reaches the hosted
  page and reads the desk-offline copy; see
  [persona-setup-and-editing.md](persona-setup-and-editing.md).) The fixture decides whether to mock persona
  **once, at page load** (`shell-fixture.tsx:198-210`): it mocks when the query
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

**Last verified:** 2026-11-01 (nightly maintenance). **Product commit:** `936f5b64` (GitLab origin/main; rooms-client 0.108.0). **Scope:** `/rooms/` (18137) `agent-center-fixture.html`: **Needs you, 9** → `#/agents/waiting`; **Allow**, **Approve argue update**, **Yes, remember it**, **Dismiss: stayed quiet in #trading…** and **Accept** settled the count 9 → 8 → 7 → 6 → 5 (**Accept** is the fixture no-op); **Grid** → **Fleet health · last 24 hours** opened to its measures; `#/agents/a/inst_argue` → **argue**, four tabs, **About**, then **Memory** with the **Memory used** meter (29) on Settings; at 390 **Details for argue** raised the **argue details** sheet, which sprang back from a 60 px pull and left on a far pull; **New agent** at 390 as a sheet (**Chat agent**, **Work agent**, templates, **Start blank**, **Import**). Shell: `?view=agents` on both hosts (smoke), `/chat/` **Voice** and **Away coverage** desk-offline copy; `remote-home-fixture` `approval` (**Approve**, **Deny**, **Stop**, **Add context**), `live` (**Stop**, **Add context**) and `unsupported`; `away-panel-fixture` (**1h 18m remaining · This Mac**, 20 controls); `agent-presentation-fixture?state=failed` (**1 failed**). **Limitations:** authenticated roster actions, the daemon-served roster, real touch; **Invite agent** was not re-driven (2026-10-28 stands). Evidence: `http://127.0.0.1:8098/vomc-nightly-20261101/r1/` (`agents-01` to `agents-14`, `away-01`).

**Previous record:** 2026-10-31 (nightly maintenance). **Product commit:** `936f5b64` (GitLab origin/main; rooms-client 0.108.0). **Scope:** `/rooms/` (18135) `agent-center-fixture`: Map ready; **Grid** ready with **Fleet health · last 24 hours** opened; **Needs you, 9** → `#/agents/waiting` (Approve argue update, Keep argue at 1.0.0, Allow, Yes, remember it, No, forget it, Dismiss, Accept, Reject present); **Open argue, 2 need you** → `#/agents/a/inst_argue`, h1 **argue**, tabs, **Run argue**, **More actions for argue** (3 items), the About / Today / Memory boxes; **New agent** (groups **Agent type**, **Agent templates**; Escape returns focus); `?roster=none` Allow / Deny; `?state=desk-off` **Loading agents**; **Update for argue**. Shell: `?view=agent&panel=voice|away|activity` → `#/agents/voice|away|activity` with their copy; `?view=agents` as in the route table; `remote-home-fixture` approval / live / unsupported; `omSessions=drafts` with the `**/healthz*` stub. `/chat/` (18136): `?view=agents` → `/chat/agents`, Map with om only and the local-app copy; **Voice** → `/chat/agents/voice` and **Away coverage** → `/chat/agents/away`, both desk-offline. **Limitations:** Consent buttons not pressed this pass (pressed 2026-10-30); authenticated roster actions; the rail spellings for away, reconnecting and remote; the 390 px sheet drag. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261031/r1/`.

**Previous record:** 2026-10-30 (scheduled maintenance). **Product commit:** `47cb13bf` (GitLab origin/main; rooms-client 0.108.0). **Scope:** `/rooms/` `agent-center-fixture`: **Needs you, 9** → `#/agents/waiting`, the consent buttons pressed as listed under Needs you (9 → 8 → 6 → 5; **Accept** no-op); **Grid** wrote `om.chat.agentsView=grid`; **Open argue** → `#/agents/a/inst_argue` with **Run argue**, Overview / Activity / Access / Settings and **Ask argue something**. `/chat/` `?view=agents`: **Persona sections** → **Voice** (`/chat/agents/voice`) and **Away coverage** (`/chat/agents/away`) read the desk-offline copy. **Limitations:** Authenticated roster actions. Evidence: `http://127.0.0.1:8098/verify-om-chat-maint-20261030/r1/` (frames 04, 30-33).

**Previous record:** 2026-10-30 (nightly maintenance). **Product commit:** `47cb13bf` (GitLab origin/main; rooms-client 0.108.0), the first main tree with the `3e9c88f3` Agents redesign. **Scope (fixture lane):** On `/rooms/` `agent-center-fixture.html`, the Map showed **Agents map** with its House, Chat, Work and Connected agent regions, Rooms, Library, Projects and the named ask cards. **Grid** showed **Agents grid**, **Your agents**, **Sort agents** and seven agent h3s. **Needs you, 9** led to `#/agents/waiting` (h1 **Needs you**) with region **Update for argue** (**Approve argue update**, **Keep argue at 1.0.0**). **Open argue, 2 need you** led to `#/agents/a/inst_argue` (h1 **argue**, **Run argue** checked, **More actions for argue** → Review replies first / Check routing / Review what it learned). All four tabs switched. **Back to agents** returned to `#/agents`. **New agent** opened its dialog (Agent type, Agent templates, Start blank, Import, Continue), and Escape returned focus to **New agent**. `?roster=none` showed the Allow / Deny feed with om and the connected agents only. `?state=desk-off` read "Loading agents" and "your desk · not answering". `shell-fixture.html?view=agents` showed h1 **Agents** with `your om` and **+ Wire an agent** (on Grid, the view stored earlier in the session). On `/chat/` it routed to `/chat/agents` and showed the Map with om only and the local-app copy. At 390 px the **New agent** sheet followed in-page pointer drags, sprang back from a short pull and dismissed from a long one. **Limitations:** Allow, Accept and Reject were not pressed. The Voice, Away and Activity rows, `away-panel-fixture` and `remote-home-fixture` were not re-driven tonight; the host load averaged 170-350. Real relay and daemon actions are pending. Evidence is local only (the `8098` renderer was unreachable): `artifacts/vomc-nightly-20261030/r1/` in the product worktree, frames 01-06, 11-15.

**Previous record:** 2026-10-29 (nightly maintenance). **Product commit:** `cdfb1b0f` (origin/main; rooms-client 0.108.0). **Scope:** `agent-center-fixture` default showed the Roster h1, **Waiting on you** and **+ Wire an agent**. `#/agents/badge/agcr_claude` showed **claude code**, **Live now** and a `role=img`. `away-panel-fixture` read "Research om is covering you" and `remaining · This Mac`. `remote-home-fixture` `approval` showed **Approve**, **Deny** and **Stop** (named by their text) and **Add context** (named by `aria-label`). `unsupported` showed its copy. **Limitations:** The rail label spellings (away, reconnecting, remote) cannot be seeded on the shell fixture; real relay and daemon actions are pending. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261029/r1/` (frames 46–47, 69–70).

**Previous record:** 2026-10-28 (nightly maintenance). **Product commit:** `2dd7aad1` (origin/main). **Scope:** `agent-center-fixture` default showed the Roster h1, **Waiting on you** and **+ Wire an agent**; `#/agents/badge/agcr_claude` showed **claude code**, **Live now** and a `role=img`. `away-panel-fixture` read "Research om is covering you" and `remaining · This Mac`. `remote-home-fixture` `approval` showed **Approve** / **Deny** / **Stop**, `live` showed **Stop** and **Add context** (both `aria-label`-named, so filter on the label, not `innerText`), and `unsupported` showed its copy. `settings-fixture.html?host=user&page=agent-access` rendered Agent Settings, Agents, Devices and Recent Logbook. **Invite agent** opened its no-badge dialog on both hosts. **Limitations:** `?view=agents`, `desk-off` and the `/chat/` Voice/Away copy were not re-driven. Roster shelf cards (`2dd7aad1`) have no fixture (see [agent-creator.md](agent-creator.md)). Authenticated roster actions, daemon sessions and remote-control effects are pending. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261028/r1/` (frames 13, 26, 28, 42).

**Previous record:** 2026-10-27. **Product commit:** `6c15b0fb286e9dc1b6cb130c9c97cd7e0afa9254` (origin/main). **Scope:** `agent-center-fixture` default showed the Roster h1, **Waiting on you, 4** → `#/agents/waiting`, and `desk-off` read "assembling the roster". `#/agents/badge/agcr_claude` showed h1 **claude code**, **Live now** and a `role=img` badge. In the shell, `?view=agents` showed the Roster h1 and **+ Wire an agent**, with no roster section. Both fixtures named the persona row **Away coverage, status can't tell right now**. `away-panel-fixture` read `1h 18m remaining · This Mac`, and remote `approval` showed Approve / Deny. `settings-fixture.html?host=user&page=agent-access` rendered Agent Settings, Agents, Devices and Recent Logbook with no error. On `/chat/`, `?view=agents` showed **Agent management** with the local-app copy, and **Voice** / **Away coverage** showed the desk-offline copy. **Limitations:** The **Wire an agent** click was not re-driven. Authenticated roster actions, daemon sessions, watches and remote-control effects are pending. The `userFacingErrorText` toast copy in `6c15b0fb` is source-only. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261027/r01/` (frames 04, 11-13, 30, 41-42). Previous record: 2026-10-26 at `5820fbea`.

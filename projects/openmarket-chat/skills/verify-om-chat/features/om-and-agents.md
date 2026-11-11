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
  `aside` is **"Agents sidebar"** (`AgentCenterPane.tsx:1117`). Its `nav`
  **"Agents sections"** (`:1164`) holds **All agents, N**, **Needs you, N** and
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
  Old `#/agents/badge/<id>` addresses rewrite there (`src/lib/routing.ts:304-307`).
  Top bar: **Back to agents**, h1 `<name>`, a `switch` **Run <name>** and a
  **More actions for <name>** menu (**Review replies first**, **Check
  routing**, **Review what it learned**). Its `tablist` holds **Overview,
  Activity, Access, Settings**; every panel is in the DOM and the unselected
  ones are `hidden`, so read the visible `tabpanel`. Since `8c4c54d3` (!232) the
  centre is the your-om chat on that agent's lane: a thread rail (**New
  session**, **Search chats**), a header with the agent's face and a state chip
  (**running** / **thinking**), and the shared composer `textarea.composer-input`
  with placeholder **Message <name>**. A send shows your bubble at once, the
  your-om thinking row while it waits, then the reply with the agent's face,
  rendered markdown and **Thought for Ns**. The old **Talk to <name>** /
  **Ask <name> something** / **Try it** preview and its "Trying..." line are gone.
  Since `5c8a20a4` (!237) the right sidebar (`aside.agent-side`) is a property
  panel: no card per section (only the Needs you callout and the Settings
  **Danger zone** are boxed), one 12px muted section header, two-column label /
  value rows, ghost selects. Overview: stat strip (turns today, routed right,
  rooms; a badge shows rooms and sessions) then State / Type / Source / Runs on.
  Activity: **Work** rows with a refresh icon and relative times, or
  **Sessions** for a badge. Access (roster): **Rooms** with a **+** named **Add a
  channel for <name>** that opens the **Channel for <name>** select and **Allow
  <name> in selected channel** inline, **Can do**, **Limits** (Turns an hour,
  Model, **Reply checks** that expand per check). Access (badge): one **Rooms**
  list with each room's modes, then **Reads / Speaks / Posting / Never** as
  labelled rows (the old Places chips and per-band room rows are merged; the
  expiry clock, copy-id and stop-one-mode menu live only on the settings Agent
  access page). Settings: Memory meter and rows; a badge's **Disconnect** sits
  in the Danger zone.
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

**Recipe (agent page and its chat).** Since `149ea33c` the
`agent-center-fixture` opens agent pages: it spreads `composerSessionFields()`
into its session and scripts `/chat/conversations`, `/chat/history` and
`/chat/turn`. Open an agent by clicking its rail row (the text starts with the
agent's emoji, so match with `includes`, not `startsWith`); the
`#/agents/a/<id>` hash on first load did not open it. `?hold=<ms>` holds the
turn's stream so the thinking state can be captured:
`agent-browser fill "textarea.composer-input" "hi"; agent-browser press Enter`,
screenshot after ~1.5 s, then again after the hold. Live verified 2026-11-10
(dark and light, argue / debugger / claude code; gallery
`http://127.0.0.1:8098/agent-sidebar/r2/`).

**Trap.** Viewport screenshots of the fixture came back solid black while the
DOM was full (the app stylesheet stops the page scrolling). Screenshot an
element instead: `agent-browser screenshot "main#root" out.png` for the pane,
`"aside.agent-side"` for the sidebar, with a tall viewport
(`set viewport 1280 1800`) so nothing sits below the fold.

**Trap.** A worktree whose `node_modules` is a symlink to another worktree
serves that other worktree's `@openmarket/chat-ui` through vite (tests still
pass, because they resolve through tsconfig paths). Give a capture worktree its
own `bun install --frozen-lockfile`; the bunfig reads `NPM_READ_TOKEN` and
`ORANGECHARTS_NPM_READ_TOKEN`, and the `.env` copies 404 (seen 2026-11-10).

**Trap.** `agent-center-remote.test.tsx` runs under the cloud config in CI
(`verify:shared` and `verify:cloud`), where `rosterReach` is `remote`; a run
with the root tsconfig takes the desk path and misses its failures. Run CI's
lanes with `bun --tsconfig-override ./tsconfig.json tools/test-fast.ts --lane
shared|cloud --no-gates <path filters>`.

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
and the live-lane prerequisites. **+ Wire an agent** (`AgentCenterPane.tsx:1404`)
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
  (`Shell.tsx:3128-3143`; mobile segments `Shell.tsx:3671-3716`). So an
  `--exact` match on the bare name misses several different ways, and matching
  the mobile string on desktop misses too. Away is a whole-app state, a
  different thing from the daemon not running.

  On desktop there is a **third** state neither of those covers:
  `#829` made the rail label its destinations during a reconnect, so both
  doors carry a `railUnsettled` spelling — **"Your om, reconnecting"**
  (`Shell.tsx:3848`) and, crossing armed × away × reconnecting,
  **"Agents, N armed, reconnecting"** / **"Agents, reconnecting"**
  (`Shell.tsx:3134`, `:3139`). Two states is the old shape; matching on it
  during a flaky connect misses silently.

  **Away has a remote-control spelling too.** When the session is away and a
  remote device answers over the relay, the doors read
  **"Your om, connected remotely"** and **"Agents, connected remotely"**, or
  **"…, remote control off"** when a device is reachable but none is selected
  (`Shell.tsx:1570`; accessible names at `:3141`, `:3683`, `:3708`,
  `:3810`). The tooltips spell it with a colon instead, "Agents: connected
  remotely" (`:3092`, `:3792`), so match the name, not the tooltip. The shell fixture cannot show it: its session stub
  answers `remoteControl: () => null` (`shell-fixture.tsx:4164`). The pane
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
  (`Shell.tsx:4090-4143` for spaces; the zone-1 feature folders use the same
  markers at `Shell.tsx:3910-3948`).

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
  **`u1`** (`shell-fixture.tsx:1045` maps the `kyle` handle to `u1`; every
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
  **watches** (`ChatPane.tsx:482`). Settings used to be the fourth and is not
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
  (`AgentCenterPane.tsx:1117`) holding, top to bottom:

  - a `searchbox` **Search agents**;
  - a `nav` named **"Agents sections"** (`:1164`) — **All agents, N**, **Needs
    you, N**, **Running, N** (the counts ride the accessible names);
  - a group named **"Persona"** (`:1209`) holding a `nav` named **"Persona
    sections"** (`:1213`) — **Voice**, **Away coverage, off** (state in the
    name again, `:258-272`; with no away snapshot after a load has failed or
    finished it reads **Away coverage, status can't tell right now** and the
    visible text **Can't tell**, which the agent-center fixture and the
    shell's unmocked routes show; the shell's mocked
    `?view=agent&panel=voice|away|activity` routes read **Away coverage, on,
    78 minutes left** / **On · 78m**, re-driven 2026-11-04 at `ce14d4ba`),
    **Activity**;
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
  heading is **"Persona"**. Since `417164da` each page is a `SettingsSection` of dense
  settings rows (`.ui-settings-row`, 46 px) under an uppercase section title:
  `voice` reads **VOICE** with **Edit** and **Try it**, `away` reads **AWAY**
  with a status pill (**ON**, **PAUSED**, **STOPPING** or **OFF**), and
  `activity` reads **ACTIVITY** with **Handled all**. Re-driven 2026-11-04 on
  the mocked routes at `ce14d4ba`. "Research om is covering you" and "Away
  activity" are gone. Row handles are in
  [persona-setup-and-editing.md](persona-setup-and-editing.md).

  **"Your voice could not be loaded. Try again in a moment." is the
  diagnostic.** Since `417164da` the loading and load-failed states keep the
  **Voice** section title (`PersonaPanel.tsx:482`, `:831`); the old `h1`
  "Your voice" is gone. The failure copy and a **Retry** button sit inside the
  section, so a Voice page with no rows and that line is the panel telling you
  the profile did not load. On this lane that almost always means the route
  problem below (re-driven 2026-11-04 on `?view=agents&panel=persona`).

  **Where the three persona tabs render has now moved three times** — the
  panel's own strip, then the om session rail (`.om-session-persona-nav`,
  deleted by `38d0c72d`), then the panel's strip again, and since `#978` the
  Agents sidebar's "Persona sections" group. Driven at 1440x900 on
  `?view=agent&panel=voice`: `.persona-hub-tabs` is **absent** and
  `.om-session-persona-nav` is absent; the only persona controls are the
  sidebar rows. `.persona-hub-tabs` still exists in source
  (`PersonaPanel.tsx:110`) behind `navigation = "inline"` (`:71`), but no route
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
  remains (`UserSettings.tsx:277`), supplied by `Shell.tsx:4617`. That is
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
  composer with no lane toggle and no target (`Composer.tsx:6394-6395`),
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
| `shell-fixture.html?view=agent&panel=voice` | Agents → `#/agents/voice`, **VOICE** rows for the card "Current" v4, mocked and loaded |
| `shell-fixture.html?view=agent&panel=away` | Agents → `#/agents/away`, **AWAY** **ON** with **Pause** and **I'm back**, "Replies as Current" |
| `shell-fixture.html?view=agent&panel=activity` | Agents → `#/agents/activity`, **ACTIVITY** with **Handled all** and the **Away session** combobox |
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

### The Agents page on /chat/ through the desk (on main since `39f5b49a`)

The hosted `/chat/` Agents page reads and drives the owner's agents on their own daemon over Remote Control, with nothing desk-only. Every roster RPC has a `roster.*` operation name (`packages/rooms-client/src/roster/remote-routes.ts`, monorepo `c7c8c6f95`), the cloud host's roster transports send them through `remoteOperation` (`apps/cloud/src/lib/roster-desk.ts`), and roster support on `/chat/` comes from `roster.capabilities` instead of `/healthz` (`packages/chat-ui/src/lib/roster-support-state.ts`, `roster-desk-support.ts`). `/rooms` is unchanged.

- **What a user sees on `/chat/agents`.** The desk's agents in the Map and Grid; **Templates** and **New agent** enabled; `your om` reads idle when the desk answers. The brain chips wear the om mark (**OM daemon**) and the official Claude and OpenAI marks (**Claude Code**, **Codex**; faded when not set up).
- **Desk offline.** "Your desk is offline. Your agents load when om at your desk is running." within about 5 s of the lane stopping; it recovers by itself about 10 s after the desk returns. Not opted in reads "Remote control is off at your desk. Turn it on with om agent remote enable."
- **Fixture lane (no relay), driven 2026-11-04 on main at `ce14d4ba`.** `/chat/tools/visual/shell-fixture.html?view=agents&alerts=quiet` lands on `/chat/agents` with **Map**, **Grid**, **Templates** and **New agent**, and the page reads "Your desk is offline. Your agents load when om at your desk is running." (`remote-unavailable.ts`, passed as the Agents notice at `AgentCenterSurface.tsx:318`). **Grid** keeps the notice above `your om`. **OM daemon**, **Claude Code** and **Codex** read "can't tell". The other desk states (off, outdated, busy, no answer) need a registered operator or the rig.
- **Driven 2026-11-03 on the branch rig** (a branch receipt; the rig pass was not repeated on main) (`/Users/dboon/Documents/dev-notes/om-agents-cloud-parity/rig/README.md`: relay 18120, store 18121, lane 18123, fake model 18124, cloud vite 4178 with `/chat/api` → store): **Run explain** paused and resumed explain on the desk; **Try it** returned the reply and three checks; **Check routing** ran `roster.instances.eval` ("Routes correctly 67%"); **Allow** granted explain into **ACP Rig / ops** ("explain can read and reply in ACP Rig / ops"); `@explain what is a funding rate` posted in `#general` from `/chat/` got explain's reply threaded under it within 3 s (run `door: mention`). `/rooms` Agents matched origin/main by pixel diff (60 px, status dots). Evidence: `http://127.0.0.1:8098/agents-cloud-parity/u7-r5/` (and `u7-r3`).
- **Pending live (tests only):** work-run live polling (3 s, at most three runs), run Pause and Steer, vault and catalog writes, Needs-you decisions and **File as source** on `/chat/` (the rig had no work runs, vault, inbox items or room with history for them).

Rig gotchas: run the cloud vite from the realpath `/Users/dboon/gitlab/...` (a `/Gitlab/` path splits vite's module graph and the Remote Control registry reads empty, so every operation answers `remote_offline` with zero frames); a fake model must send `post_reply` with `room` and `replyTo` or the desk refuses "Roster posts must stay in room <id>"; the first sidebar load marked never-read rooms `joined:false` (fixed on the branch at chat `c3f5ced0`), which empties the Allow picker.

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

### Agent post faces (added 2026-11-04)

Since `d7cc0c8f` an agent's post wears a face that says whose agent it is
(`Avatar.tsx:175-215`):

- **The owner's picture with the agent mascot in the corner** when the entry
  carries its owner's `userId` and the owner has a picture: the image plus
  `span.avatar-agent-mark[data-agent-mark]`, which moves to the top corner when
  a presence dot is shown.
- **The mascot on the agent's coloured tile** (`span[data-avatar-face]` holding
  `svg[data-agent-mascot="mono"]`, coloured by the agent's name) when the owner
  has no picture or the id is an app account (`@om-agent` and similar).

Faces show only in the cozy layout: the default chassis rows render no
`[data-avatar-face]`. On `shell-fixture.html?view=topic&topic=cpi-print-aug&message=cozy&alerts=quiet`
the **om** (**AGENT**) post "target unchanged 4.25-4.50%…" wears the mono mascot
on a tile with no corner mark, on `/rooms/` and `/chat/` (driven 2026-11-04 at
`ce14d4ba`, `avatar-01-agent-tile`; re-driven 2026-11-05 at `873a57ce`). Since
`b99778ec` the mascot has no headset: the `svg` holds only the blob `path`, the
visor `rect` and two eye `circle`s.

**The AGENT chip** (since `b99778ec`; ink since `713f95f4`). An agent's name
carries `span.agent-chip.agent` reading **AGENT** (it read "✦ APP"), with
`aria-label` **OM Agent** and a one-colour mascot glyph
(`.agent-chip-glyph.is-mascot`). Verified agents read **AGENT** after a check
and are labelled **Verified Agent**. A webhook still reads a grey **APP** and a
system post **SYSTEM**; the shell fixture seeds no webhook row, so the APP chip
is source-only (`AgentBadge.tsx`). The chip prints `--on-agent`: on the
cpi-print-aug **om** post it measured ink `rgb(8, 10, 13)` on `rgb(147, 161,
175)` in dark and `rgb(241, 243, 246)` on `rgb(78, 90, 102)` with `theme=light`,
the same on both hosts. There is no `data-*` on the chip; assert the class and
text. Clear `om.chat.messageDisplay` after (see
the README). The owner-picture face is **live verification pending**: no
fixture seeds an agent entry whose owner has an avatar (`profileFor` returns no
avatar), so it needs a fixture seed or a daemon-pair lane with a badge agent.

## Gotchas

- **No query parameter bypasses the running-om gate; a route stub does.** `?view=agent` renders the empty
  state — `h1` *"om isn't running"*, *"No recent daemon snapshot is available on
  this device"* on this lane. The gate is `presence.running === false`
  (`ChatPane.tsx:522`), fed by `fetchOmHealth()` (`lib/om-health.ts`), which
  reads any 4xx except 429, or a non-JSON 200, as down. The fixture has two
  session modes: `omSessions=drafts` seeds Research A/B locally, and
  `omSessions=daemon` wires real session-list/history operations. Neither fakes
  `presence.running`. Stub it in the browser instead: `agent-browser network
  route "**/healthz*" --body '<health JSON>'` before the first open (the exact
  body is in [your-om-drafts.md](your-om-drafts.md)). The `*` also covers the
  `/healthz?lite=1` poll, which otherwise 404s and drops the gate about 30 s in.
  Proved on 2026-10-27 (maintenance re-drive). The single nightly session that
  passed without a stub was the `running === null` window, before the first
  poll answer or while the tab is hidden (`ChatPane.tsx:275`). Do not plan a
  proof on that window. The stub answers health only, so Watches still need
  daemon watch RPCs and QA watch data, and unread still needs daemon events.
- **On `/rooms/`, persona is unreachable from a `view=agents` page load — by any control,
  not just the old query.** (On `/chat/` the same Voice click reaches the hosted
  page and reads the desk-offline copy; see
  [persona-setup-and-editing.md](persona-setup-and-editing.md).) The fixture decides whether to mock persona
  **once, at page load** (`shell-fixture.tsx:199-211`): it mocks when the query
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

**Last verified:** 2026-11-09 (nightly maintenance). **Product commit:** `82390825` (GitLab origin/main; rooms-client 0.114.0; 49 commits past `08fe407b`). **Scope:** `/rooms/` (18183) `away-panel-fixture.html` (**AWAY**, **Pause**, **I'm back**), `agent-center-fixture.html`, and `?view=agent&omSessions=drafts` with the `/healthz*` and people stubs (**Research A**, **Research B**, **Watches**). **Limitations:** daemon-backed agents. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261109/r1/`.

**Previous record:** 2026-11-08 (nightly maintenance). **Product commit:** `08fe407b` (GitLab origin/main; rooms-client 0.112.0; unchanged since the 2026-11-07 pass). **Scope:** `/rooms/` (18183) `away-panel-fixture.html` (**AWAY**, **Pause**, **I'm back**), `agent-center-fixture.html` (h1 **Agents**), and `?view=agent&omSessions=drafts` with the `/healthz*` stub (**Research A**, **Research B**, **Watches**). **Limitations:** daemon-backed agents. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261108/r1/`.

**Previous record:** 2026-11-07 (nightly maintenance). **Product commit:** `08fe407b` (GitLab origin/main; rooms-client 0.112.0; 89 commits past `ea399e62`). **Scope:** `/rooms/` (18180) `away-panel-fixture.html` reads **AWAY** **ON** with **Pause**, **I'm back** and "Replies as Maya's voice"; `agent-center-fixture.html` h1 **Agents**; `?view=agent&omSessions=drafts` with the `/healthz*` stub shows **Research A**, **Research B** and the **Watches** door. `/chat/` (18181): the **Watches** door. **Limitations:** daemon-backed sessions not driven. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261107/r1/`.

**Previous record:** 2026-11-06 (nightly maintenance). **Product commit:** `ea399e62` (GitLab origin/main; rooms-client 0.111.0; 74 commits past `873a57ce`). **Scope:** `/rooms/` (18180) `away-panel-fixture.html` reads **AWAY** **ON** with **Pause**, **I'm back**, **Replies as**; `agent-center-fixture.html` h1 **Agents** with Map, Grid, Needs you; `?view=agent&omSessions=drafts` with the `/healthz*` stub shows **Research A**, **Research B** and the **Watches** door; `/chat/` the same om rail. **Limitations:** daemon-backed sessions not driven. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261106/r1/`.

**Previous record:** 2026-11-05 (nightly maintenance). **Product commit:** `873a57ce` (GitLab origin/main; rooms-client 0.109.1; 17 commits past `ce14d4ba`). **Scope:** `/rooms/` (18170) and `/chat/` (18171) `view=topic&topic=cpi-print-aug`: the **om** post's chip reads **AGENT** / **OM Agent** with the mascot glyph, and its ink in dark and `theme=light`; with `message=cozy` the mono mascot tile has no headset; the Appearance preview's Helper Agent carries the same chip. `persona-panel-fixture.html` and `away-panel-fixture.html` mount (route smoke and a text probe). **Limitations:** the webhook APP chip has no fixture row; the owner-picture face is still pending. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261105/r1/` (`16`, `17`, `36`).

**Previous record:** 2026-11-04 (nightly maintenance). **Product commit:** `ce14d4ba` (GitLab origin/main; rooms-client 0.109.1; 16 commits past `ba4389e7`). **Scope:** `/rooms/` (18160): the shell `?view=agent&panel=voice|away|activity` pages (**VOICE**, **AWAY** **ON**, **ACTIVITY**); `away-panel-fixture` states; the legacy `view=agents&panel=persona` failure copy; the om (APP) mascot tile under `message=cozy`; `remote-home-fixture?state=approval` (**Approve**, **Deny**); the `**/healthz*` stub lane for drafts and watches. `/chat/` (18161): Agents Map and Grid with the desk-offline notice; Voice and Away desk-offline. **Limitations:** the owner-picture agent face; the desk rig was not repeated on main. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261104/r1/` (`away-*`, `om-01`, `avatar-01`, `chat-01` to `chat-04`).

**Previous record:** 2026-11-03 (nightly maintenance). **Product commit:** `ba4389e7` (GitLab origin/main; rooms-client 0.108.0; one CI-only commit past `3f8f24bc`). **Scope:** `/rooms/` (18143): `view=agents` (**Map**, **Grid**, **Templates**, **New agent**, **All agents, 1**, **Needs you, 0**, **Running, 0**); `panel=voice|away|activity` route to `#/agents/*`; the `agent-center-fixture` (**Needs you, 9**); `#/agents/a/inst_argue` (Overview / Activity / Access / Settings, **Run argue**, **Memory used** 29); `roster=none`; seven `remote-home-fixture` states (`unsupported` reads **not supported by this device**); four `agent-presentation-fixture` states; `away-panel-fixture`. `/chat/`: **Agents** and the offline Voice page. **Limitations:** unchanged. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261103/r1/` (`ag-*`).

**Previous record:** 2026-11-02 (nightly maintenance). **Product commit:** `3f8f24bc` (GitLab origin/main; rooms-client 0.108.0). **Scope:** `/rooms/` (18137) `agent-center-fixture.html`: **Needs you, 9** → `#/agents/waiting` **Needs you** (three Allow / Deny rows) → **Allow** → **Needs you, 8**; `#/agents/a/inst_argue` → **argue**, tabs Overview / Activity / Access / Settings, **Run argue**, **More actions for argue** (**Check routing**, **Review what it learned**), the **Memory** box with the **Memory used** meter (`aria-valuenow` 29) on **Settings**; **Grid** → **Fleet health · last 24 hours**; at 390×844 **Details for argue** → the **argue details** sheet (591 px, `[data-sheet-grip]`); `roster=none` renders om and the connected agents; with the `**/healthz*` stub `?view=agent&omSessions=drafts` → **Add context** → **Channels** listbox (14); `remote-home-fixture` approval (Stop / Approve / Deny) and unsupported; `away-panel-fixture` (**Research om is covering you**, 20 controls); `agent-presentation-fixture?state=failed` (**Collapse tool activity**); `/chat/` (18138): `?view=agents` → **Agents** with Map / Grid / Templates / New agent; `?view=agent&panel=voice` → **om isn't running** with the `om serve` copy. **Limitations:** the sheet's spring drag was not re-driven (its page was `document.hidden` after a mid-session `set viewport`); approvals and roster writes stay fixture-local. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261102/r1/`.

**Previous record:** 2026-11-01 (nightly maintenance). **Product commit:** `936f5b64` (GitLab origin/main; rooms-client 0.108.0). **Scope:** `/rooms/` (18137) `agent-center-fixture.html`: **Needs you, 9** → `#/agents/waiting`; **Allow**, **Approve argue update**, **Yes, remember it**, **Dismiss: stayed quiet in #trading…** and **Accept** settled the count 9 → 8 → 7 → 6 → 5 (**Accept** is the fixture no-op); **Grid** → **Fleet health · last 24 hours** opened to its measures; `#/agents/a/inst_argue` → **argue**, four tabs, **About**, then **Memory** with the **Memory used** meter (29) on Settings; at 390 **Details for argue** raised the **argue details** sheet, which sprang back from a 60 px pull and left on a far pull; **New agent** at 390 as a sheet (**Chat agent**, **Work agent**, templates, **Start blank**, **Import**). Shell: `?view=agents` on both hosts (smoke), `/chat/` **Voice** and **Away coverage** desk-offline copy; `remote-home-fixture` `approval` (**Approve**, **Deny**, **Stop**, **Add context**), `live` (**Stop**, **Add context**) and `unsupported`; `away-panel-fixture` (**1h 18m remaining · This Mac**, 20 controls); `agent-presentation-fixture?state=failed` (**1 failed**). **Limitations:** authenticated roster actions, the daemon-served roster, real touch; **Invite agent** was not re-driven (2026-10-28 stands). Evidence: `http://127.0.0.1:8098/vomc-nightly-20261101/r1/` (`agents-01` to `agents-14`, `away-01`).

**Previous record:** 2026-10-31 (nightly maintenance). **Product commit:** `936f5b64` (GitLab origin/main; rooms-client 0.108.0). **Scope:** `/rooms/` (18135) `agent-center-fixture`: Map ready; **Grid** ready with **Fleet health · last 24 hours** opened; **Needs you, 9** → `#/agents/waiting` (Approve argue update, Keep argue at 1.0.0, Allow, Yes, remember it, No, forget it, Dismiss, Accept, Reject present); **Open argue, 2 need you** → `#/agents/a/inst_argue`, h1 **argue**, tabs, **Run argue**, **More actions for argue** (3 items), the About / Today / Memory boxes; **New agent** (groups **Agent type**, **Agent templates**; Escape returns focus); `?roster=none` Allow / Deny; `?state=desk-off` **Loading agents**; **Update for argue**. Shell: `?view=agent&panel=voice|away|activity` → `#/agents/voice|away|activity` with their copy; `?view=agents` as in the route table; `remote-home-fixture` approval / live / unsupported; `omSessions=drafts` with the `**/healthz*` stub. `/chat/` (18136): `?view=agents` → `/chat/agents`, Map with om only and the local-app copy; **Voice** → `/chat/agents/voice` and **Away coverage** → `/chat/agents/away`, both desk-offline. **Limitations:** Consent buttons not pressed this pass (pressed 2026-10-30); authenticated roster actions; the rail spellings for away, reconnecting and remote; the 390 px sheet drag. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261031/r1/`.

**Previous record:** 2026-10-30 (scheduled maintenance). **Product commit:** `47cb13bf` (GitLab origin/main; rooms-client 0.108.0). **Scope:** `/rooms/` `agent-center-fixture`: **Needs you, 9** → `#/agents/waiting`, the consent buttons pressed as listed under Needs you (9 → 8 → 6 → 5; **Accept** no-op); **Grid** wrote `om.chat.agentsView=grid`; **Open argue** → `#/agents/a/inst_argue` with **Run argue**, Overview / Activity / Access / Settings and **Ask argue something**. `/chat/` `?view=agents`: **Persona sections** → **Voice** (`/chat/agents/voice`) and **Away coverage** (`/chat/agents/away`) read the desk-offline copy. **Limitations:** Authenticated roster actions. Evidence: `http://127.0.0.1:8098/verify-om-chat-maint-20261030/r1/` (frames 04, 30-33).

**Previous record:** 2026-10-30 (nightly maintenance). **Product commit:** `47cb13bf` (GitLab origin/main; rooms-client 0.108.0), the first main tree with the `3e9c88f3` Agents redesign. **Scope (fixture lane):** On `/rooms/` `agent-center-fixture.html`, the Map showed **Agents map** with its House, Chat, Work and Connected agent regions, Rooms, Library, Projects and the named ask cards. **Grid** showed **Agents grid**, **Your agents**, **Sort agents** and seven agent h3s. **Needs you, 9** led to `#/agents/waiting` (h1 **Needs you**) with region **Update for argue** (**Approve argue update**, **Keep argue at 1.0.0**). **Open argue, 2 need you** led to `#/agents/a/inst_argue` (h1 **argue**, **Run argue** checked, **More actions for argue** → Review replies first / Check routing / Review what it learned). All four tabs switched. **Back to agents** returned to `#/agents`. **New agent** opened its dialog (Agent type, Agent templates, Start blank, Import, Continue), and Escape returned focus to **New agent**. `?roster=none` showed the Allow / Deny feed with om and the connected agents only. `?state=desk-off` read "Loading agents" and "your desk · not answering". `shell-fixture.html?view=agents` showed h1 **Agents** with `your om` and **+ Wire an agent** (on Grid, the view stored earlier in the session). On `/chat/` it routed to `/chat/agents` and showed the Map with om only and the local-app copy. At 390 px the **New agent** sheet followed in-page pointer drags, sprang back from a short pull and dismissed from a long one. **Limitations:** Allow, Accept and Reject were not pressed. The Voice, Away and Activity rows, `away-panel-fixture` and `remote-home-fixture` were not re-driven tonight; the host load averaged 170-350. Real relay and daemon actions are pending. Evidence is local only (the `8098` renderer was unreachable): `artifacts/vomc-nightly-20261030/r1/` in the product worktree, frames 01-06, 11-15.

**Previous record:** 2026-10-29 (nightly maintenance). **Product commit:** `cdfb1b0f` (origin/main; rooms-client 0.108.0). **Scope:** `agent-center-fixture` default showed the Roster h1, **Waiting on you** and **+ Wire an agent**. `#/agents/badge/agcr_claude` showed **claude code**, **Live now** and a `role=img`. `away-panel-fixture` read "Research om is covering you" and `remaining · This Mac`. `remote-home-fixture` `approval` showed **Approve**, **Deny** and **Stop** (named by their text) and **Add context** (named by `aria-label`). `unsupported` showed its copy. **Limitations:** The rail label spellings (away, reconnecting, remote) cannot be seeded on the shell fixture; real relay and daemon actions are pending. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261029/r1/` (frames 46–47, 69–70).

**Previous record:** 2026-10-28 (nightly maintenance). **Product commit:** `2dd7aad1` (origin/main). **Scope:** `agent-center-fixture` default showed the Roster h1, **Waiting on you** and **+ Wire an agent**; `#/agents/badge/agcr_claude` showed **claude code**, **Live now** and a `role=img`. `away-panel-fixture` read "Research om is covering you" and `remaining · This Mac`. `remote-home-fixture` `approval` showed **Approve** / **Deny** / **Stop**, `live` showed **Stop** and **Add context** (both `aria-label`-named, so filter on the label, not `innerText`), and `unsupported` showed its copy. `settings-fixture.html?host=user&page=agent-access` rendered Agent Settings, Agents, Devices and Recent Logbook. **Invite agent** opened its no-badge dialog on both hosts. **Limitations:** `?view=agents`, `desk-off` and the `/chat/` Voice/Away copy were not re-driven. Roster shelf cards (`2dd7aad1`) have no fixture (see [agent-creator.md](agent-creator.md)). Authenticated roster actions, daemon sessions and remote-control effects are pending. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261028/r1/` (frames 13, 26, 28, 42).

**Previous record:** 2026-10-27. **Product commit:** `6c15b0fb286e9dc1b6cb130c9c97cd7e0afa9254` (origin/main). **Scope:** `agent-center-fixture` default showed the Roster h1, **Waiting on you, 4** → `#/agents/waiting`, and `desk-off` read "assembling the roster". `#/agents/badge/agcr_claude` showed h1 **claude code**, **Live now** and a `role=img` badge. In the shell, `?view=agents` showed the Roster h1 and **+ Wire an agent**, with no roster section. Both fixtures named the persona row **Away coverage, status can't tell right now**. `away-panel-fixture` read `1h 18m remaining · This Mac`, and remote `approval` showed Approve / Deny. `settings-fixture.html?host=user&page=agent-access` rendered Agent Settings, Agents, Devices and Recent Logbook with no error. On `/chat/`, `?view=agents` showed **Agent management** with the local-app copy, and **Voice** / **Away coverage** showed the desk-offline copy. **Limitations:** The **Wire an agent** click was not re-driven. Authenticated roster actions, daemon sessions, watches and remote-control effects are pending. The `userFacingErrorText` toast copy in `6c15b0fb` is source-only. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261027/r01/` (frames 04, 11-13, 30, 41-42). Previous record: 2026-10-26 at `5820fbea`.

## Tag an agent from the composer and allow it the room (MR !158, driven 2026-11-04)

The composer's `@` picker lists every agent the daemon sends (name and owner; a description is optional, the daemon's instance list never carries one). An agent not yet allowed in the room keeps a selectable row under the **agents** group reading `<name> can't post here yet · Enter allows it`; Enter calls `roster.instances.grant` for that agent and room, re-reads readiness and inserts `@<name> `. A refused grant puts the daemon's words on the row and inserts nothing; a host without `instances.grant` in the roster capabilities keeps the dimmed `aria-disabled` row.

Recipe, needs a daemon-backed lane (the fixture lane has no roster): the agents cloud-parity rig (`~/Documents/dev-notes/om-agent-mention-rooms/rig/`, relay 18120, store 18121, fake model 18124, lane daemon 18123 with `ACP_ROOMS_GUI_DEV_URL` pointing at a rooms vite on 18126; cloud app on 4178 with `tokens/browser-seed.js` evaluated once on `/chat/`). Create a server from the rail (the seed's `room create` makes no server), open `#general`, then:

- `agent-browser fill "textarea" "@lib"` (typing through `type` does not reach the composer; `fill` does) and read the rows with `eval` on `.composer-autocomplete-row` (`snapshot` can hang while the popover is open on `/chat/`): one row, `aria-disabled` null, the allow hint.
- `agent-browser press Enter`: the textarea reads `@librarian ` and `GET /rpc/v1/roster/readiness?instance=<id>&room=<room id>` on the lane answers `[]` where it answered `no_grant` before. With openmarket-internal #2325 the relay log shows `om_room_joined` for the room within seconds of the grant.
- `fill "textarea" "@explain what is a funding rate"`, `press Escape`, `press Enter`: explain's fake reply lands threaded under the mention within 25 s. argue and fact-check launch a run too, but their own `cites-source` reply check holds the fake model's reply (`GET /rpc/v1/roster/inbox` lists `verify_failed`), so use explain for a visible reply.

Proven on both hosts at chat `14509e60` with lane daemon `4f4db0510`. Rig owner handle is empty, so rows read `| argue` there; a real daemon sends the owner's handle.

## Agents in rooms and on the Agents page (chat !231 !232, internal #2432–#2434, relay !255 !256)

*Live-driven 2026-11-09/10 on a local rig, both hosts. Rig: `~/Documents/dev-notes/om-agent-thinking-indicator/rig` (Mongo 18122, store 18121 from a tharamine worktree detached at `13445d10`, relay 18120 from `RELAY_TREE`, fake model 18124 started with `FAKE_HOLD_MS=6000 FAKE_HOLD_WHEN=post_reply` so a mention run shows "thinking" for a few seconds, lane 18123 via `lane-start.sh` with `ACP_ROOMS_GUI_DEV_URL=http://127.0.0.1:18126`, rooms vite 18126 and cloud vite 4178 from the GUI tree).*

- **Thinking row.** Grant an agent the room (`POST /rpc/v1/roster/instances/<id>/grant` with the lane's runner token), send "@argue ..." in the composer; `.composer-thinking` reads "⚖️ <owner> · argue is thinking..." and its label carries `.text-shimmer`.
- **Agent tags.** `.agent-mention` spans (teal text, transparent background). While that agent thinks, only its NEWEST @mention in each view gains `.text-shimmer` (since `!242`, merged 2026-11-11): the room tape, the topic-dial stream (newest among the rows it shows) and the topic peek pane (its own scope; newest among the topic's rows) each pick their own; an unsent echo counts as newest; older mentions stay plain teal. Channels with topics on render through TopicListView, so check there too. Live verified 2026-11-11 with real `Markdown` + tag contexts in Chromium (dark and light; `http://127.0.0.1:8098/agent-tag-newest/r1/`); stream, topic-dial and peek wiring by DOM tests.
- **Reply to an agent.** Post with `inReplyTo` = the agent's message seq (rig/reply-probe.ts); expect exactly one new `reply_tag` row in `roster_invocations` and no further rows from the agent's own answers.
- **Agent chat.** `#/agents` → open the agent → send in "Message <agent>": bubbles on lane `agent-chat:<instance>:<thread>`; on cloud the same thread continues over Remote Control (`agent-chat.v1`).
- **Needs you.** Grant a coding agent (feature) a room with no linked project: its Overview lists the missing brain and "no project for this server" with a Link a project button.

### Gotchas
- Vite pre-bundles the linked `@openmarket/chat-ui`; after merging new GUI commits restart both vites with `--force`, and open a fresh agent-browser session (an old session keeps stale modules).
- In this rig the daemon's owner handle is empty, so agents assert "| <name>" and agent posts arrive `isAgent=false` under the owner; the GUI's `agentOwnName` and the daemon's own-post guard cover both.
- A fake model that holds every call long makes the run fail as a provider hiccup; hold only `post_reply` turns, for a few seconds.
- The room post budget throttles an agent for the hour after a burst; switch agents for fresh captures.

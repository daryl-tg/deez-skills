# OM Chat feature map

One file per user-facing feature. Each names the routes that reach it, the
handles that drive it, and the traps that have already cost someone a run.

This map is the repo's maintained verification source. **A proof that drives
one convenient entry point is incomplete when the file lists others.** If you
verify channel navigation from the sidebar and the file also lists the mobile
tab bar and the topic breadcrumb, either drive those too or say in the manifest
which you skipped and why.

Each file has the same four sections, in order:

1. **Sub-features** — what actually has to work, itemised.
2. **How to get to it (user POV)** — what a person does, in their words.
3. **Driving it with control-om-chat** — the routes and commands, with real
   accessible names from this repo.
4. **Gotchas** — what breaks, what lies, what the fixture cannot prove.

## Reaching the lane

Every snippet in these files opens its harness through the wrapper:

```bash
cd /Users/dboon/github/openmarket-chat
export OM_CHAT_LANE_PORT=<your assigned 18097-18197 port>   # ./control-om-chat doctor
./control-om-chat up
agent-browser open "$(./control-om-chat url '<path>?<query>')"
```

`control-om-chat url` builds the origin from `OM_CHAT_LANE_PORT`, so nothing
here hardcodes a port. That matters more than it looks: lanes are assigned per
run, several worktrees drive at once, and a literal port copied out of a doc
lands you on **another run's app** — where everything renders and every frame
is evidence of the wrong tree.

## The three fixture entry points

The fixture lane serves three different harnesses. Using the wrong one is why a
query parameter "does nothing".

| File | Query vocabulary | Mounts |
|---|---|---|
| `tools/visual/shell-fixture.html` | `?view=`, `?panel=`, `?alerts=`, `?theme=`, … | The whole Shell — rail, sidebar, content, composer |
| `tools/visual/settings-fixture.html` | `?host=user\|server\|channel`, `?page=`, `?perms=`, `?state=`, `?mode=` | The settings surfaces |
| `tools/visual/fixture.html` | `?surface=` | A component gallery (KitchenSink, reactions, polls) |

One surface has a fourth, dedicated harness: the Open World tab, at
`mocks/world-solo/index.html?worldprobe=1`. See
[open-world.md](open-world.md) — it is not reachable through the shell fixture.

The other files in `tools/visual/` are **not** driveable harnesses.
`agent-center-fixture.html`, `person-presence-fixture.html`, and
`reaction-scene-fixture.tsx` are opened only by their Playwright visual specs,
and `chat-rendering-gallery.html` is a static mock nothing references. Opening
one expecting `?view=`-style behavior wastes a run.

`?view=` values on the shell fixture: `room` (default), `topics`, `topic`,
`required`, `public`, `dm`, `home`, `channels`, `friends`, `library`, `agent`,
`agents`, `empty`, `settings`, `server-settings`, `gif`.

`?view=gif` is the odd one out: it bypasses the Shell entirely and renders a
standalone GIF-sizing debug harness, so none of the normal chrome is there.

`settings` and `server-settings` are the other two exceptions: they open a
`dialog` named **"Settings"** *over* the room rather than replacing it, so the
`h1` stays `#ops` and the route stays `#/room/ops`. An agent that checks the
heading concludes the value is dead. Check for the dialog. `?view=settings`
takes a companion `?settingsPage=` (default `account`); the settings **fixture**
is still the better harness for settings work (see
[settings-and-appearance.md](settings-and-appearance.md)).

Common modifiers, all on the shell fixture: `alerts=quiet|board`,
`theme=dark|light`, `contrast=high`, `palette=slate|moss|warm|brass`,
`channels=many`, `bulk=<n>` (message count), `draft=<text>`, `peek=<topicId>`,
`inbox=open`, `message=cozy`, `text=200` (200% type), `keyboard=<px>`,
`width=stress`.

That list is the common set, not the whole vocabulary — the fixture reads
around sixty parameters. The ones worth knowing beyond the list:
`panel=search|library|topic-draft` (and `searchState=error`, which only renders
once `panel=search` has seeded a run — see
[search-and-filters.md](search-and-filters.md)), `lens=todos|agents` on
`view=library` (which routes to `#/library/todos` and `#/library/agents`),
`profile=1` for the profile panel, and `policy=required|off` for the channel's
topics policy (default `allowed`). When a parameter seems to do nothing, grep
`params.get(` in `tools/visual/shell-fixture.tsx` before concluding it is
dead — and check whether it needs a companion, the way `searchState` needs
`panel=search`.

**`message=cozy` is sticky, and nothing unsets it.** It writes
`om.chat.messageDisplay` to `localStorage` and the fixture has no `else` branch
to clear it, so every later load in that browser session stays cozy — including
the load you meant to capture as the default. A before/after comparison run in
one session therefore shows no difference and looks like a dead parameter.
Clear the key before capturing a default frame:

```bash
agent-browser eval 'localStorage.removeItem("om.chat.messageDisplay")'
```

Cozy is visible as `msg-identity-cozy` on a `[data-message-row]`; the default is
`msg-identity-chassis mt-2` without it. (The settings fixture's `contrast=high`
does clear itself — that asymmetry is why only this one bites.)

`?alerts=quiet` is worth reaching for by default: without it the fixture fires
an app-wide alert strip that shifts every surface below it down. The counts and
the board disagree, and both are fixture seeding: the beacon hardcodes **three**
ringing feeds (`Alerts: 3 feeds are ringing`) while the board renders the
**two** rows actually seeded (`af-store-5xx`, `af-relay-latency`). Do not report
that gap as a product bug, and do not caption a screenshot with the badge count.
Those two are seed **ids**, not rendered text — the row reads
`store-5xx · check pods`, so grepping a snapshot for `af-store-5xx` finds
nothing and looks like the board failed to render.

## Who adds to this map

Two paths, and the first is the cheap one.

**A feature run**, when its terminal gate drives a surface no file covers. That
is the moment the handles are known and the proof is fresh, so writing the file
costs almost nothing. The feature playbooks require it before handing off.

**A maintenance pass**, sweeping recent churn for surfaces the map never heard
of. That works, but it rediscovers from source what a feature run already knew,
and pays a full live sweep to do it. `open-world.md` arrived this way.

## Files

- [channel-and-topic-navigation.md](channel-and-topic-navigation.md)
- [mobile-shell-navigation.md](mobile-shell-navigation.md)
- [composer-and-sending.md](composer-and-sending.md)
- [direct-messages-and-home.md](direct-messages-and-home.md)
- [settings-and-appearance.md](settings-and-appearance.md)
- [search-and-filters.md](search-and-filters.md)
- [open-world.md](open-world.md)

# Profiles

Opening a person's profile from a DM or a name, and reading what the drawer
says about them.

## Sub-features

- **Profile drawer** (`packages/chat-ui/src/components/ProfilePanel.tsx`): a
  right-panel drawer with **Close profile** (`:325`, `:342`, `:430`), the avatar,
  the display name and handle, **Copy username** (`:452`), and the action
  buttons **Message** (`:477`), **Mention** (`:486`), **Follow** / **Following**
  / **Requested** (`:505`) and **Cancel request** (`:511`); on your own profile,
  **Edit profile** (`:464`).
- **Profile sections** tablist (`:544`): **Info** (selected by default),
  **Media** and **Links**. The To-dos tab went with the legacy board
  (`05df35a7`); driven 2026-11-15 on `/rooms/`, the tablist holds exactly three
  tabs.
- **Info** content: About, Mutual servers with a count and chips, Member since,
  Connections (follower count), and at its foot **Report user** (`:791`, only
  when the person has a DM conversation with you) and **Block user** /
  **Unblock user** (`:803`). The `?profile=1` seed has no DM conversation id,
  so it shows **Block user** without **Report user**.
- The DM header's identity button (`A Online ana`) opens the same drawer.
- The floating identity card (`?card=1`, `shell-fixture.tsx:3222`): a `dialog`
  named **Profile for ana** (`.profile-popover`) with the avatar, name, the
  about line, ROLES (traders), `2 mutual servers · 128 followers` and the
  buttons **View ana (ops)'s full profile**, **Message**, **Mention**,
  **Follow**, **Block ana** and **Send to ana**. Driven 2026-10-31 on
  `/rooms/` (`?view=dm&dm=ana&alerts=quiet&card=1`). The name popover
  (`ProfilePopover.tsx`) is source-only.
- **Working on**, an agent's live status in its card (`513bc114`, `23a7fb3d`,
  `AgentProfileCard.tsx:271`). It is a `region` **Working on**, with a counts
  line such as "1 working · 1 waiting", one `li[data-state]` per item, a state
  dot (`role=img` named by the state), the title, room chip, step and age, and
  an **Open <title>** link for https links. A note line reads "Paused for the
  deploy window · 4m", or "No recent activity". It appears only once the relay
  answers `agent_status` (`ProfilePopover.tsx`), and opened from an agent's
  message it shows only that agent. The live subscription is **live
  verification pending**: `?card=1` is the human `ana`, and no shell fixture
  stubs `observeAgentStatus`. The gallery renders the card itself; see
  Driving it.

## How to get to it (user POV)

In a DM, click the person's name at the top of the conversation. The profile
slides in on the right. Switch between Info, Media and Links, then close it
with the × button.

## Driving it with control-om-chat

```bash
agent-browser open "$(control-om-chat url 'tools/visual/shell-fixture.html?view=dm&dm=ana&alerts=quiet&profile=1')"
agent-browser find role tab click --name "Media" --exact      # aria-selected moves; hash stays #/dm/ana
agent-browser find role button click --name "Close profile"   # the tablist unmounts
```

The agent **Working on** card renders only in the component gallery, in its
"Agent-native" section (`KitchenSink.tsx`). It works on both hosts and mounts
about 4 s after load:

```bash
agent-browser open "$(control-om-chat url 'tools/visual/fixture.html')"
agent-browser eval '(()=>JSON.stringify([...document.querySelectorAll("[aria-label=\"Working on\"]")].map(s=>s.innerText.replace(/\n/g," / "))))()'
#   three regions on both hosts; text read on /rooms/ (2026-11-06, ea399e62):
#   "WORKING ON / 1 working · 1 waiting / Backfilling CME options / #cme-data / Day 3 of 10 / 4m / Open / …"
#   "WORKING ON / No recent activity"
#   "… 1 working · 1 waiting · 1 blocked …" (the redacted card: rooms read "a private room")
#   state dots img "working", "waiting", "blocked"; link "Open Backfilling CME options" (https)
```

`?profile=1` seeds the drawer for ana (`shell-fixture.tsx:3229`, origin
`dm:ana`) and sets `rightPanel` to `profile` (`:3287`). Use it on the DM view;
the room view has no matching origin. The user path is the header button:
open `?view=dm&dm=ana&alerts=quiet` and click
`find role button --name "A Online ana"`. `Close profile` appears.

Assert the Info content through the drawer's text, e.g. walk up from
`[aria-label="Close profile"]` to the element holding the tablist and match
`Ops rotation, scanner duty, funding prints.`, `MUTUAL SERVERS · 2`,
`Jan 2025`, `128 followers` and `Block user`.

### Presence dots (added 2026-11-02)

`tools/visual/person-presence-fixture.html` is an ordinary fixture, not a
spec-only harness: it mounts one `[data-person-presence-fixture]` board with the
four `PresenceDot` specimens (`shared/ui/PresenceDot.tsx`, rendered by
`Avatar.tsx` and `HomeHub.tsx`), each labelled by its state: **Presence
unknown** (`data-presence-source="unknown"`, a hollow ring), **Offline**
(`leased`, dimmed), **Idle** and **Online on mobile** (`live`, the mobile
glyph). Read them with
`agent-browser eval '(()=>JSON.stringify([...document.querySelectorAll("[data-presence-source]")].map(d=>d.getAttribute("aria-label")+"/"+d.dataset.presenceSource)))()'`.
Driven 2026-11-02 on `/rooms/` (18137). Live presence transitions still need a
relay.

## Gotchas

- The sections have no `role="tabpanel"`. A query for the panel finds nothing,
  so read the drawer's text instead.
- The content is fixture seeding (`profileFor` at `shell-fixture.tsx:3157`). It
  proves layout and the tab and close mechanics, not that a real profile fetch
  works. Media was not asserted for content.
- **Links lists the links a person posted, and skips a URL written as code
  (driven 2026-11-22 on `/rooms/`).** The tab reads the open conversation's
  messages (`ProfilePanel.tsx:50-58`, `:617`). With the session-capture shim,
  append a post by `u-ana` to `#ops` on `?view=room&alerts=quiet&profile=1`
  whose text is ``see https://example.com/live and `https://example.com/in-span` ``
  followed by a fenced block holding `https://example.com/in-fence`, then
  press **Links**: `[data-testid=profile-links]` lists one row, title
  `example.com` and `.profile-share-sub` `https://example.com/live`. The two
  coded URLs are not listed. `/chat/` cannot open the drawer.
- Blocking is not exercised: the fixture does not persist it, and the Blocked
  tab under Connections crashes (see
  [direct-messages-and-home.md](direct-messages-and-home.md)).
- **An agent's name is its owner's, with the persona beside it** (`DisplayName.tsx:78-194`, since `52a968b3`; this replaced the persona-handle-only rule of `01bf4481`). An agent row reads `<owner name> · <persona>`, for example "Daryl Boon · researcher" (`:157-161`; `test/ui/display-name-degraded.test.tsx:122`). With no picked persona it reads the owner's name alone. A degraded handle, the auto-wired badge's stock name `openmarket-chat` (`lib/wired-agent.ts:6`) and a name equal to the owner's name or account do not count as personas. If the owner has not loaded, the old handle-based name stays. Owner nicknames never relabel an agent, and the hover title keeps the handle. The shell fixture seeds one agent post, `#ops` seq 191 (`userId` `u-bot-4c81aa`, degraded handle `om-4c81aa`, `isAgent: true`; `tools/visual/shell-fixture.tsx:1198-1210`). It renders **om-mod-bot started a topic** with no ` · ` suffix on both hosts. No fixture seeds an agent with a picked persona, so the `Owner · persona` form is unit-test only.
- **`profile=1` is a `/rooms/` seed only.** The `/chat/` shell fixture never
  reads `profile`, so `?view=dm&dm=ana&profile=1` there opens the DM with no
  drawer (measured 2026-10-29). The DM header button **ana Online ana** does not open it there either
  (2026-10-31): the cloud fixture sets `profilePanel: null` and stubs no
  `openProfilePanel` (`apps/cloud/tools/visual/shell-fixture.tsx:1636`). Prove
  the drawer on `/rooms/`.

### Verification record

**Last verified:** 2026-11-26 (nightly maintenance). **Product commit:** `0f3fd22c` (GitLab origin/main; rooms-client 0.125.0; 7 commits past `557ee9ed`). **Scope:** the scripted re-drive of this guide's recipes by the kept step runner (`/rooms/` 18186, `/chat/` 18187 where the guide covers it, openscape 18188 for the world), motion blocks one session at a time; two read-only judges compared every result with its expectation and each flagged block was re-run alone. This guide's source did not change in the delta. **Limitations:** unchanged from the previous record. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261126/r1/`.

**Previous record:** 2026-11-25 (nightly maintenance). **Product commit:** `557ee9ed` (GitLab origin/main; rooms-client 0.125.0; 11 commits past `9c697d6e`). **Scope:** the scripted re-drive of this guide's recipes by the kept step runner (`/rooms/` 18186, `/chat/` 18187 where the guide covers it, openscape 18188 for the world), motion blocks one session at a time; every failing step was re-run alone and compared with this guide. This guide's source did not change in the delta. **Limitations:** unchanged from the previous record. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261125/r1/`.

**Previous record:** 2026-11-24 (nightly maintenance). **Product commit:** `9c697d6e` (GitLab origin/main; rooms-client 0.125.0; 22 commits past `4b6f42b4`). **Scope:** the scripted core-path re-drive of this guide's recipes (`/rooms/` 18186, `/chat/` 18187 where the guide covers it, openscape 18188 for the world); every failed or disagreeing step was re-run alone. This guide's source did not change in the delta. **Limitations:** unchanged from the previous record. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261124/r1/`.

**Previous record:** 2026-11-22 (nightly maintenance). **Product commit:** `4b6f42b4` (GitLab origin/main; rooms-client 0.124.0; one commit past `84e88e56`). **Scope:** `/rooms/` (18186) `?view=dm&dm=ana&profile=1`: the drawer text, the three tabs, **Media** and **Links** selection, the action buttons and **Close profile**; the header button opening the drawer; `card=1`; the presence fixture's four specimens; three **Working on** cards in the gallery. New: the **Links** tab listing a posted URL and skipping one in a code span and one in a fence. `/chat/`: `profile=1` opens nothing (no seed). **Limitations:** Media content, Report and Block effects were not driven. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261122/r1/`.

**Previous record:** 2026-11-20 (nightly maintenance). **Product commit:** `7e3f0cde` (GitLab origin/main; rooms-client 0.122.0; 16 commits past `12f1ea24`). **Scope:** `/rooms/` (18193), `?view=dm&dm=ana&alerts=quiet&profile=1`: tabs **Info**, **Media** and **Links** with **Info** selected; **Links** takes the selection; **Close profile** unmounts the tablist. **Limitations:** the Links tab's skipping of URLs in code (`7fbe9218`, `ProfilePanel.tsx`) is source only, because the fixture panel rendered no link rows; **Working on** and the header entry were not re-driven. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261120/r1/`.

**Previous record:** 2026-11-15 (nightly maintenance). **Product commit:** `96644a29` (GitLab origin/main; rooms-client 0.118.0; 8 commits past `62fcc01a`). **Scope:** `/rooms/` (18175) `view=dm&dm=ana&alerts=quiet&profile=1`, people stub: the **Profile sections** tablist holds **Info** (selected), **Media** and **Links**, and **Links** takes the selection; the drawer's buttons read **Close profile**, **Copy username**, **Message**, **Mention**, **Follow** and **Block user**. **Limitations:** `/chat/` has no `profile=1` seed; **Report user** needs a DM conversation id the seed lacks; the card, Working on and Block effects were not re-driven (2026-11-09 stands). Evidence: `http://127.0.0.1:8098/vomc-nightly-20261115/r1/` (frames 14, 20).

**Previous record:** 2026-11-09 (nightly maintenance). **Product commit:** `82390825` (GitLab origin/main; rooms-client 0.114.0; 49 commits past `08fe407b`). **Scope:** `/rooms/` (18183) `view=dm&dm=ana&alerts=quiet&profile=1` with the people stub: the `tablist` **Profile sections** with **Info**, **Media**, **Links** and **To-dos**. `/chat/`: no drawer (carried cloud fixture limit). **Limitations:** the popover and user menu; names from the new people cards (`431f630e`) are source only: a `people.held` seed for `u-ana` did not change the tape's name, and it was not root-caused. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261109/r1/`.

**Previous record:** 2026-11-08 (nightly maintenance). **Product commit:** `08fe407b` (GitLab origin/main; rooms-client 0.112.0; unchanged since the 2026-11-07 pass). **Scope:** `/rooms/` (18183) `view=dm&dm=ana&profile=1`: **Profile sections**. `/chat/` (18184): no drawer (carried cloud fixture limit). **Limitations:** the popover and user menu. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261108/r1/`.

**Previous record:** 2026-11-07 (nightly maintenance). **Product commit:** `08fe407b` (GitLab origin/main; rooms-client 0.112.0; 89 commits past `ea399e62`). **Scope:** `/rooms/` (18180) `?profile=1`: **Profile sections** Info, Media, Links, To-dos. **Limitations:** the `/chat/` fixture has no `profile` seed; the **Working on** gallery and the live agent-status subscription not re-driven. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261107/r1/`.

**Previous record:** 2026-11-06 (nightly maintenance). **Product commit:** `ea399e62` (GitLab origin/main; rooms-client 0.111.0; 74 commits past `873a57ce`). **Scope:** `/rooms/` (18180) `?profile=1`: **Profile sections** Info, Media, Links, To-dos. `fixture.html` on both hosts: three **Working on** regions; on `/rooms/` the counts, the state dots and **Open Backfilling CME options**. **Limitations:** the live agent-status subscription is pending. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261106/r1/`.

**Previous record:** 2026-11-05 (nightly maintenance). **Product commit:** `873a57ce` (GitLab origin/main; rooms-client 0.109.1; 17 commits past `ce14d4ba`). **Scope:** `/rooms/` (18170) `view=dm&dm=ana&profile=1`: tablist **Profile sections** reads Info, Media, Links, To-dos. **Limitations:** `/chat/` only by route smoke. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261105/r1/` (`33`).

**Previous record:** 2026-11-04 (nightly maintenance). **Product commit:** `ce14d4ba` (GitLab origin/main; rooms-client 0.109.1; 16 commits past `ba4389e7`). **Scope:** `/rooms/` (18160) `?view=room&profile=1`: the **Profile sections** tablist mounts. **Limitations:** the tabs and `card=1` were not re-driven. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261104/r1/`.

**Previous record:** 2026-11-03 (nightly maintenance). **Product commit:** `ba4389e7` (GitLab origin/main; rooms-client 0.108.0; one CI-only commit past `3f8f24bc`). **Scope:** `/rooms/` (18143) `?view=dm&dm=ana&profile=1`: **Profile sections** (Info*, Media, Links, To-dos) → **Media** selected, hash stays `#/dm/ana`; **Close profile** unmounts the tablist within 1.2 s (at 1 s it still read as mounted). `person-presence-fixture.html` renders the four specimens. `/chat/` has no `profile=1` seed (as documented). **Limitations:** unchanged. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261103/r1/` (`prof-*`, `pres-01`).

**Previous record:** 2026-11-02 (nightly maintenance). **Product commit:** `3f8f24bc` (GitLab origin/main; rooms-client 0.108.0). **Scope:** `/rooms/` (18137) `?view=dm&dm=ana&alerts=quiet&profile=1`: **Profile sections** (Info, Media, Links, To-dos) → **Media** selected with the hash still `#/dm/ana`; **Close profile** clicked; `card=1` → **Profile for ana**; `person-presence-fixture.html` → the four presence specimens. **Limitations:** 400 ms after **Close profile** the `Profile sections` tablist still read as mounted, so the unmount was not re-proved tonight (the 2026-11-01 reading stands); the `/chat/` DM header still has no profile button. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261102/r1/`.

**Previous record:** 2026-11-01 (nightly maintenance). **Product commit:** `936f5b64` (GitLab origin/main; rooms-client 0.108.0). **Scope:** `/rooms/` (18137): `profile=1` opened the drawer with tabs **Info**, **Media**, **Links** and **To-dos**; **Media** became selected with the hash unchanged; **Close profile** unmounted the tablist; `card=1` showed **Profile for ana** with **View ana (ops)'s full profile**, **Message**, **Mention**, **Follow**, **Block ana** and **Send to ana**. `/chat/` (18138): `profile=1` still opens no drawer (fixture gap re-confirmed). **Limitations:** the name popover, the user context menu, tab contents beyond Info and real profile fetches. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261101/r1/` (`profiles-01`, `profiles-02`).

**Previous record:** 2026-10-31 (nightly maintenance). **Product commit:** `936f5b64` (GitLab origin/main; rooms-client 0.108.0). **Scope:** `/rooms/` (18135) `?view=dm&dm=ana&alerts=quiet&profile=1`: tab **Media** selected, hash stayed `#/dm/ana`, **Close profile** present; `&card=1` mounted the **Profile for ana** dialog with its six buttons. `/chat/` (18136): the header button **ana Online ana** opened nothing (no **Close profile**, no **Profile sections**). **Limitations:** Block, Follow, Message and Report effects; the name popover; `/chat/` drawer (fixture gap). Evidence: `http://127.0.0.1:8098/vomc-nightly-20261031/r1/`.

**Previous record:** 2026-10-30 (scheduled maintenance). **Product commit:** `47cb13bf` (GitLab origin/main; rooms-client 0.108.0). **Scope:** `/rooms/` `?view=dm&dm=ana&profile=1`: tab **Media** selected with the hash still `#/dm/ana`; **Close profile** removed the **Profile** aside and its four tabs (check after about 0.6 s). **Limitations:** Name popover, user menu and `/chat/`. Evidence: `http://127.0.0.1:8098/verify-om-chat-maint-20261030/r1/` (frames 27-28).

**Previous record:** 2026-10-29 (nightly maintenance). **Product commit:** `cdfb1b0f` (origin/main; rooms-client 0.108.0). **Scope:** On `/rooms/`, `?view=dm&dm=ana&profile=1` opened the drawer with tabs Info / Media / Links / To-dos and **Close profile**. On `/chat/` the same URL opens no drawer: the cloud fixture never reads `profile` (see Gotchas). **Limitations:** Name popover, user context menu and tab contents beyond Info. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261029/r1/` (frames 14, 34, 63).

**Previous record:** 2026-10-28 (nightly maintenance). **Product commit:** `2dd7aad1` (origin/main). **Scope:** `?view=dm&dm=ana&profile=1` opened the drawer with tabs Info (selected) / Media / Links / To-dos and **Close profile**. The seeded agent post `msg-ops-191` read "om-mod-bot started a topic" on `/rooms/` and `/chat/`, with no persona suffix (the degraded-handle path of `52a968b3`). **Limitations:** The `Owner · persona` form has no seed. Links selection, tab contents beyond Info, `?card=1`, the name popover, block effects and real fetches were not driven. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261028/r1/` (frames 03, 16).

**Previous record:** 2026-10-27. **Product commit:** `6c15b0fb286e9dc1b6cb130c9c97cd7e0afa9254` (origin/main). **Scope:** On ana's DM, the header **A Online ana** opened the drawer with Info selected (tabs Info / Media / Links / To-dos) and **Close profile** present. **Limitations:** Links selection, tab contents beyond Info, `?card=1`, the name popover, agent display names, block effects, real fetches and `/chat/`. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261027/r01/` (frame 22). Previous record: 2026-10-26 at `5820fbea`.

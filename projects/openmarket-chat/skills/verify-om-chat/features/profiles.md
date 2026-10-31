# Profiles

Opening a person's profile from a DM or a name, and reading what the drawer
says about them.

## Sub-features

- **Profile drawer** (`packages/chat-ui/src/components/ProfilePanel.tsx`): a
  right-panel drawer with **Close profile** (`:320`, `:337`, `:423`), the avatar,
  the display name and handle, and the action buttons **Message** (`:735`),
  **Mention** (`:744`), **Follow** / **Following** / **Requested**, **Cancel
  request** (`:849`), **Report** (`:804`), **Block** / **Unblock** (`:823-834`),
  **Copy username** (`:445`) and, on your own profile, **Edit profile**.
- **Profile sections** tablist (`:532`): **Info** (selected by default),
  **Media**, **Links** and **To-dos**.
- **Info** content: About, Mutual servers with a count and chips, Member since,
  Connections (follower count), and **Block user** / **Unblock user** (`:793`).
- The DM header's identity button (`A Online ana`) opens the same drawer.
- The floating identity card (`?card=1`, `shell-fixture.tsx:3042`): a `dialog`
  named **Profile for ana** (`.profile-popover`) with the avatar, name, the
  about line, ROLES (traders), `2 mutual servers · 128 followers` and the
  buttons **View ana (ops)'s full profile**, **Message**, **Mention**,
  **Follow**, **Block ana** and **Send to ana**. Driven 2026-10-31 on
  `/rooms/` (`?view=dm&dm=ana&alerts=quiet&card=1`). The name popover
  (`ProfilePopover.tsx`) is source-only.

## How to get to it (user POV)

In a DM, click the person's name at the top of the conversation. The profile
slides in on the right. Switch between Info, Media, Links and To-dos, then close it
with the × button.

## Driving it with control-om-chat

```bash
agent-browser open "$(control-om-chat url 'tools/visual/shell-fixture.html?view=dm&dm=ana&alerts=quiet&profile=1')"
agent-browser find role tab click --name "Media" --exact      # aria-selected moves; hash stays #/dm/ana
agent-browser find role button click --name "Close profile"   # the tablist unmounts
```

`?profile=1` seeds the drawer for ana (`shell-fixture.tsx:3049`, origin
`dm:ana`) and sets `rightPanel` to `profile` (`:3107`). Use it on the DM view;
the room view has no matching origin. The user path is the header button:
open `?view=dm&dm=ana&alerts=quiet` and click
`find role button --name "A Online ana"`. `Close profile` appears.

Assert the Info content through the drawer's text, e.g. walk up from
`[aria-label="Close profile"]` to the element holding the tablist and match
`Ops rotation, scanner duty, funding prints.`, `MUTUAL SERVERS · 2`,
`Jan 2025`, `128 followers` and `Block user`.

## Gotchas

- The sections have no `role="tabpanel"`. A query for the panel finds nothing,
  so read the drawer's text instead.
- The content is fixture seeding (`profileFor` at `shell-fixture.tsx:2977`). It
  proves layout and the tab and close mechanics, not that a real profile fetch
  works. Media, Links and To-dos switched selection but were not asserted for
  content.
- Blocking is not exercised: the fixture does not persist it, and the Blocked
  tab under Connections crashes (see
  [direct-messages-and-home.md](direct-messages-and-home.md)).
- **An agent's name is its owner's, with the persona beside it** (`DisplayName.tsx:52-158`, since `52a968b3`; this replaced the persona-handle-only rule of `01bf4481`). An agent row reads `<owner name> · <persona>`, for example "Daryl Boon · researcher" (`:121-125`; `test/ui/display-name-degraded.test.tsx:122`). With no picked persona it reads the owner's name alone. A degraded handle, the auto-wired badge's stock name `openmarket-chat` (`lib/wired-agent.ts:6`) and a name equal to the owner's name or account do not count as personas. If the owner has not loaded, the old handle-based name stays. Owner nicknames never relabel an agent, and the hover title keeps the handle. The shell fixture seeds one agent post, `#ops` seq 191 (`userId` `u-bot-4c81aa`, degraded handle `om-4c81aa`, `isAgent: true`; `tools/visual/shell-fixture.tsx:1228-1240`). It renders **om-mod-bot started a topic** with no ` · ` suffix on both hosts. No fixture seeds an agent with a picked persona, so the `Owner · persona` form is unit-test only.
- **`profile=1` is a `/rooms/` seed only.** The `/chat/` shell fixture never
  reads `profile`, so `?view=dm&dm=ana&profile=1` there opens the DM with no
  drawer (measured 2026-10-29). The DM header button **ana Online ana** does not open it there either
  (2026-10-31): the cloud fixture sets `profilePanel: null` and stubs no
  `openProfilePanel` (`apps/cloud/tools/visual/shell-fixture.tsx:1627`). Prove
  the drawer on `/rooms/`.

### Verification record

**Last verified:** 2026-11-01 (nightly maintenance). **Product commit:** `936f5b64` (GitLab origin/main; rooms-client 0.108.0). **Scope:** `/rooms/` (18137): `profile=1` opened the drawer with tabs **Info**, **Media**, **Links** and **To-dos**; **Media** became selected with the hash unchanged; **Close profile** unmounted the tablist; `card=1` showed **Profile for ana** with **View ana (ops)'s full profile**, **Message**, **Mention**, **Follow**, **Block ana** and **Send to ana**. `/chat/` (18138): `profile=1` still opens no drawer (fixture gap re-confirmed). **Limitations:** the name popover, the user context menu, tab contents beyond Info and real profile fetches. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261101/r1/` (`profiles-01`, `profiles-02`).

**Previous record:** 2026-10-31 (nightly maintenance). **Product commit:** `936f5b64` (GitLab origin/main; rooms-client 0.108.0). **Scope:** `/rooms/` (18135) `?view=dm&dm=ana&alerts=quiet&profile=1`: tab **Media** selected, hash stayed `#/dm/ana`, **Close profile** present; `&card=1` mounted the **Profile for ana** dialog with its six buttons. `/chat/` (18136): the header button **ana Online ana** opened nothing (no **Close profile**, no **Profile sections**). **Limitations:** Block, Follow, Message and Report effects; the name popover; `/chat/` drawer (fixture gap). Evidence: `http://127.0.0.1:8098/vomc-nightly-20261031/r1/`.

**Previous record:** 2026-10-30 (scheduled maintenance). **Product commit:** `47cb13bf` (GitLab origin/main; rooms-client 0.108.0). **Scope:** `/rooms/` `?view=dm&dm=ana&profile=1`: tab **Media** selected with the hash still `#/dm/ana`; **Close profile** removed the **Profile** aside and its four tabs (check after about 0.6 s). **Limitations:** Name popover, user menu and `/chat/`. Evidence: `http://127.0.0.1:8098/verify-om-chat-maint-20261030/r1/` (frames 27-28).

**Previous record:** 2026-10-29 (nightly maintenance). **Product commit:** `cdfb1b0f` (origin/main; rooms-client 0.108.0). **Scope:** On `/rooms/`, `?view=dm&dm=ana&profile=1` opened the drawer with tabs Info / Media / Links / To-dos and **Close profile**. On `/chat/` the same URL opens no drawer: the cloud fixture never reads `profile` (see Gotchas). **Limitations:** Name popover, user context menu and tab contents beyond Info. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261029/r1/` (frames 14, 34, 63).

**Previous record:** 2026-10-28 (nightly maintenance). **Product commit:** `2dd7aad1` (origin/main). **Scope:** `?view=dm&dm=ana&profile=1` opened the drawer with tabs Info (selected) / Media / Links / To-dos and **Close profile**. The seeded agent post `msg-ops-191` read "om-mod-bot started a topic" on `/rooms/` and `/chat/`, with no persona suffix (the degraded-handle path of `52a968b3`). **Limitations:** The `Owner · persona` form has no seed. Links selection, tab contents beyond Info, `?card=1`, the name popover, block effects and real fetches were not driven. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261028/r1/` (frames 03, 16).

**Previous record:** 2026-10-27. **Product commit:** `6c15b0fb286e9dc1b6cb130c9c97cd7e0afa9254` (origin/main). **Scope:** On ana's DM, the header **A Online ana** opened the drawer with Info selected (tabs Info / Media / Links / To-dos) and **Close profile** present. **Limitations:** Links selection, tab contents beyond Info, `?card=1`, the name popover, agent display names, block effects, real fetches and `/chat/`. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261027/r01/` (frame 22). Previous record: 2026-10-26 at `5820fbea`.

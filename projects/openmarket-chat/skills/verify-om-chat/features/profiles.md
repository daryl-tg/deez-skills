# Profiles

Opening a person's profile from a DM or a name, and reading what the drawer
says about them.

## Sub-features

- **Profile drawer** (`packages/chat-ui/src/components/ProfilePanel.tsx`): a
  right-panel drawer with **Close profile** (`:320`, `:337`, `:423`), the avatar,
  the display name and handle, and three action buttons.
- **Profile sections** tablist (`:532`): **Info** (selected by default),
  **Media**, **Links** and **To-dos**.
- **Info** content: About, Mutual servers with a count and chips, Member since,
  Connections (follower count), and **Block user** / **Unblock user** (`:793`).
- The DM header's identity button (`A Online ana`) opens the same drawer.
- The floating identity card (`?card=1`) and the name popover
  (`ProfilePopover.tsx`) exist in source. Neither was driven here.

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
- **Agent names follow the persona handle** (`DisplayName.tsx:56-150`, `01bf4481`).
  For an agent, owner nicknames and display names no longer relabel it; a
  degraded handle falls back to the account name, and the hover title is
  `@persona`. Search hits, DM hits, Pins and the channel peek now pass
  `isAgent`. No fixture seeds an agent entry with `isAgent`, so this is source
  only.

### Verification record

**Last verified:** 2026-10-27. **Product commit:** `6c15b0fb286e9dc1b6cb130c9c97cd7e0afa9254` (origin/main). **Scope:** On ana's DM, the header **A Online ana** opened the drawer with Info selected (tabs Info / Media / Links / To-dos) and **Close profile** present. **Limitations:** Links selection, tab contents beyond Info, `?card=1`, the name popover, agent display names, block effects, real fetches and `/chat/`. Evidence: `http://127.0.0.1:8098/vomc-nightly-20261027/r01/` (frame 22). Previous record: 2026-10-26 at `5820fbea`.

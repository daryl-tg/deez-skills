# Profiles

Opening a person's profile from a DM or a name, and reading what the drawer
says about them.

## Sub-features

- **Profile drawer** (`packages/chat-ui/src/components/ProfilePanel.tsx`): a
  right-panel drawer with **Close profile** (`:308`, `:325`, `:411`), the avatar,
  the display name and handle, and three action buttons.
- **Profile sections** tablist (`:520`): **Info** (selected by default),
  **Media**, **Links** and **To-dos**.
- **Info** content: About, Mutual servers with a count and chips, Member since,
  Connections (follower count), and **Block user** / **Unblock user** (`:781`).
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

`?profile=1` seeds the drawer for ana (`shell-fixture.tsx:3042`, origin
`dm:ana`) and sets `rightPanel` to `profile` (`:3100`). Use it on the DM view;
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
- The content is fixture seeding (`profileFor` at `shell-fixture.tsx:2970`). It
  proves layout and the tab and close mechanics, not that a real profile fetch
  works. Media, Links and To-dos switched selection but were not asserted for
  content.
- Blocking is not exercised: the fixture does not persist it, and the Blocked
  tab under Connections crashes (see
  [direct-messages-and-home.md](direct-messages-and-home.md)).

### Verification record

**Last verified:** 2026-10-26. **Product commit:** `5820fbeaca9ded509b4369498f5946f32455c61a` (origin/main; since `afabb11c` only `apps/cloud/Dockerfile.market` changed). **Scope:** On ana's DM, the header **A Online ana** opened the drawer with Info selected, **Links** took the selection, and **Close profile** unmounted it. **Limitations:** Tab contents beyond Info, `?card=1`, the name popover, block effects, real fetches and `/chat/`. Previous record: 2026-10-23 at `afabb11c`, which this re-drive did not narrow.

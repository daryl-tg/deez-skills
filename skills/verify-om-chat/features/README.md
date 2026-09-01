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

## The three fixture entry points

The fixture lane serves three different harnesses. Using the wrong one is why a
query parameter "does nothing".

| File | Query vocabulary | Mounts |
|---|---|---|
| `tools/visual/shell-fixture.html` | `?view=`, `?panel=`, `?alerts=`, `?theme=`, … | The whole Shell — rail, sidebar, content, composer |
| `tools/visual/settings-fixture.html` | `?host=user\|server\|channel`, `?page=`, `?perms=` | The settings surfaces |
| `tools/visual/fixture.html` | `?surface=` | A component gallery (KitchenSink, reactions, polls) |

`?view=` values on the shell fixture: `room` (default), `topics`, `topic`,
`required`, `public`, `dm`, `home`, `channels`, `friends`, `library`, `agent`,
`agents`, `empty`, `settings`.

Common modifiers, all on the shell fixture: `alerts=quiet|board`,
`theme=dark|light`, `contrast=high`, `channels=many`, `bulk=<n>` (message
count), `draft=<text>`, `peek=<topicId>`, `inbox=open`, `message=cozy`,
`text=200` (200% type), `keyboard=<px>`, `width=stress`.

`?alerts=quiet` is worth reaching for by default: without it the fixture seeds
three firing feeds and an app-wide alert strip that shifts every surface below
it down.

## Files

- [channel-and-topic-navigation.md](channel-and-topic-navigation.md)
- [mobile-shell-navigation.md](mobile-shell-navigation.md)
- [composer-and-sending.md](composer-and-sending.md)
- [direct-messages-and-home.md](direct-messages-and-home.md)
- [settings-and-appearance.md](settings-and-appearance.md)

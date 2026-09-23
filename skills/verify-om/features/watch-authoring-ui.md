# Watch authoring in the dashboard

*Verified: 2026-09-23, tree `9a49752c3` (v0.400.0) — a feed watch authored end to end against a loopback stub and confirmed from the CLI. The seven non-feed source kinds were opened but not completed.*

Since v0.400.0 a user can create a watch from the dashboard instead of the CLI.
`Create watch` on `/alerts` opens a dialog that asks what to watch, collects the
fields that kind needs, shows a review, and creates it. The watch it writes is
the same object `om watch create` writes: the CLI sees it immediately, and it
lands **paused**.

## Sub-features

- `kind-picker` offers eight source kinds in one dialog.
- `source-form` collects the fields for the chosen kind.
- `review-step` shows what will be created before anything is written.
- `create` writes the watch and returns to the list.
- `lands-paused` leaves the new watch disabled until the user resumes it.

## How to get to it (user POV)

- Open the dashboard, go to Watches, press `Create watch`.
- Or, from an empty Overview, the `Create a watch` link in the onboarding block.

## Driving it with control-om

Preconditions:

- A lane the run started, and for the feed kind a reachable feed. The bundled
  stub is the cheapest one, and the lane must carry the loopback switch:
  `control-om up --env OM_FEED_ALLOW_LOOPBACK=1 --env OM_FEED_POLL_INTERVAL_MS=60000`,
  then `mkdir -p /tmp/origin-stub && cd /tmp/origin-stub && echo ok > mode &&
  bun ~/.claude/skills/verify-om/helpers/origin-challenge-stub.ts &`.
- A browser session of your own (`AGENT_BROWSER_SESSION`), viewport 1440x900.

- **Open the picker.** `agent-browser find role button click --name "Create watch"`
  opens `dialog "Create a watch"` holding eight buttons whose accessible names
  are the kind and its one-line description together, so match on a prefix:
  `Website`, `RSS or Atom feed`, `X account`, `Search`, `AI research`,
  `Market data`, `Another watch`, `Schedule only`.
- **Choose a kind.** Clicking the RSS button opens `dialog "Set up a feed"` with
  `textbox "Name ..."` (required), `textbox "Feed address ..."` (required), a
  `combobox "Which updates should count?"` defaulting to `All new items`, and
  `Back` / `Review`.
- **Fill and review.** Fill the two textboxes, press `Review`, and assert
  `dialog "Review your watch"` with a `heading "RSS or Atom feed"` naming the
  kind, plus `Back` / `Create watch`.
- **Create.** Press `Create watch`. The dialog closes and the list re-renders.
- **Confirm on the other surface.** `control-om om -- watch list` shows the new
  watch under its slug with status `paused` — the UI and the CLI are writing the
  same store. Driven: a watch named `UI authored feed` appeared as
  `ui-authored-feed  1 source  paused  never`.
- **Confirm it actually works.** `control-om om -- watch resume <slug>`, wait a
  poll interval, and the stub's request log shows `ok GET /rss` — the authored
  watch polls like any other.
- **Proof.** Keep the review-step and post-create snapshots, the `watch list`
  output, and the stub log lines that follow the resume.

## Gotchas

- **It lands paused.** A driver who creates a watch and waits for a fire will
  wait forever. Resume it first.
- The UI shows the LABEL (`UI authored feed`), the CLI shows the slug
  (`ui-authored-feed`). Same watch — see [watch lifecycle](./watch-lifecycle-cli.md)
  for the slug/label split.
- The eight kind buttons have long accessible names that fold the description in
  (`RSS or Atom feed Collect new articles or updates from a feed address.`).
  Match the whole string or use a prefix; the bare kind name does not match.
- Only the feed kind has been driven end to end on a guest lane. `AI research`
  and `Search` route through a model, so they are `verified-unreachable` without
  an LLM credential; `Market data`, `X account`, `Website`, `Another watch` and
  `Schedule only` are unproven here, not known-broken.
- A loopback feed address is refused unless the LANE carries
  `OM_FEED_ALLOW_LOOPBACK=1`. Unlike `om watch page-add`, the UI creates through
  the daemon, so the switch is needed on `up` only — not on a CLI call.

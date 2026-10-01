# Watch authoring and management in the dashboard

*Verified: 2026-10-01, tree `30000def2` (v0.425.0) — RSS picker, form, review, create, paused CLI row and feed detail page driven on a guest lane. Other seven kinds and batch actions remain unverified.*

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
- `detail-page` opens one watch at `/alerts/<id-or-slug>` to manage it.
- `batch-actions` pause, resume, mute, unmute or remove several at once.

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

- **Open one watch.** Clicking a row's `link "<label>"` goes to
  `/alerts/<id-or-slug>`. Its `heading` at level 1 is the watch's own LABEL (so
  it is dynamic — do not assert a fixed string), beside `Pause` and
  `Edit watch`, and a tab group `Setup` / `History` / `Delivery` /
  `Settings`. The Setup tab holds `Choose how you hear about updates` with
  `Set up delivery`, and `Sources and schedules` with `Add source or schedule`
  plus one `heading` per source and an `Edit source` button. Driven at
  `/alerts/ui-authored-feed`.
- **Batch actions** live on the list: selecting rows via the per-row checkboxes
  enables icon buttons whose accessible names are `Pause`, `Resume`, `Mute`,
  `Unmute` and `Remove selected watches`. Not exercised here — a remove is
  destructive and the lane's watches were still under test.

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
- **`Fetch now` is source-kind dependent.** The button is gated on
  `spec.sources.some(s => s.kind === "listener")` (`pages/watch-detail.tsx`), so
  it renders only for a watch with a feed/listener source. An inbound-only watch
  has no manual-fetch action at all. Driven both ways — present on a feed watch,
  absent on an inbound one. Do not assert it unconditionally.
- **The UI and the CLI are one code path, not two.** Every
  `POST /rpc/v1/watch/<verb>` route dispatches through the same
  `actions/watch/*` registry objects the CLI and MCP use
  (`runner/http/rpc/watch-management.ts`: "calls the same action as the TUI").
  So the spec shape, slug/label split and pause/resume/remove semantics are
  already covered by [watch lifecycle](./watch-lifecycle-cli.md) and need no
  re-proving here. What is genuinely UI-only, and still unmapped, is the RPC
  envelope itself and three staging flows with no CLI equivalent:
  `arm-prepare`/`arm-confirm`, `edit-prepare`, and
  `source-prepare`/`source-confirm`.
- The dashboard's create always forces `enabled: false` and notifications off,
  which is why an authored watch lands paused. That is a caller-side default on
  the shared schema, not a different create.
- A loopback feed address is refused unless the LANE carries
  `OM_FEED_ALLOW_LOOPBACK=1`. Unlike `om watch page-add`, the UI creates through
  the daemon, so the switch is needed on `up` only — not on a CLI call.

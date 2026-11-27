# A trading watch's record on its registry page

*Verified: 2026-11-28 (nightly), tree `a5dfab1169` (origin/main, v0.499.0+internal), guest lane on 18184 through `bootstrap.internal.ts`. First live proofs of #2756 and #2761 on dry runs: an imported watch with one inbound source and a paper `book` step (`book-probe` on paper account `vom-book`) shares on its own with `--with-execute` (`share_mode: recipe`, `Ships: inbound + money`, the money-terms row, `Paper: your account vom-book stays here; installers get a new one`, `Record: shown on the registry`); `--no-with-execute` ships `updates only` with no `Record:` row; a `--ref` pack with `--ship book-probe=recipe` reads `Steps 1 on vompack-book-probe: 1 step, books paper trades; om watch arm …`; `--fires-only --with-execute` and `--ref` with no `--name` are refused by name; `watch record show book-probe` is still `watch_not_published` (hint `Publish it first: om watch share book-probe --with-execute`). Found by driving: `om watch publish --with-execute` with no `--ref` or `--group` crashes with a stack trace (Gotchas). Source only: the record's `decisions` and `closes_at` (#2755), the push notices (#2750, #2760), a republish keeping its money steps. Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261128/r1/` (`cli/15` to `cli/25`, `02-book-probe-watch.png`).*

*Verified: 2026-11-27 (nightly), tree `68d49523c` (origin/main, v0.498.1+internal; #2731 merged as `c41b66c5b`), guest lane on 18184 through `bootstrap.internal.ts`. Driven, refusals only: `om watch record show cond-probe` (text and `--format json`) and `om watch record hide cond-probe` exit 2 `watch_not_published` with the share hint; `--delay -5` is refused `watch_record_show_failed` (`--delay takes whole seconds, 0 or more`); MCP `watch_record_show {ref}` answers the same `watch_not_published`, and `{watch}` is refused `invalid_arguments` (`ref` is required). Not driven: the snapshot push, the paper record, the real-money show at a terminal and the registry page, which need a completed `om watch share --with-execute` publication on a registry account. Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261127/r1/` (`cli/guest-refusals.txt`, `cli/stdio-record-show.json`).*

A published watch that trades shows its trading record on its registry page. Your om pushes one snapshot per paper book, target or money step when it changes: the equity curve, open positions and trades with their reasons. A paper record shows on its own, with open positions 15 minutes late by default. A real money record stays hidden until `om watch record show <watch>` at a terminal: it shows the venue and address first, checks that this machine's venue key controls that address, then signs a message proving the wallet is yours. `om watch record hide` takes it down again.

## Sub-features

- `record-show`: `om watch record show <watch> [--step <id>] [--delay <seconds>]`. `--delay` sets how late open positions show (whole seconds, 0 or more). Success prints `Record: pending, <reason> (<label>)` or `shown on the registry` (source only).
- `record-hide`: `om watch record hide <watch> [--step <id>]`.
- `refusals` (checked in this order before any prompt):
  - `watch_not_found` for an unknown watch: `nothing to share: '<x>' is not a watch slug on this home and no local watch is bound to that address` (driven);
  - `watch_not_published`: `watch '<slug>' has no completed publication; there is no record to show`, hint `Publish it first: om watch share <slug> --with-execute` (driven);
  - `record_not_shipped`: published without `--with-execute` (source);
  - `record_no_trading_step`: `watch '<slug>' has no paper or money step to keep a record of` (source);
  - `record_step_required` with several steps and no `--step`, `record_step_not_found` for a wrong one, both hinting `Name one with --step: <ids>` (source).
- `money-at-terminal` (source only): a real-money step under `--format json` or with no TTY answers `record_needs_terminal` (`a real money record shows only after your typed yes at this terminal`). A missing venue key answers `this machine has no <label> address to show`.
- `mcp`: `watch_record_show` is on the agent, MCP and CLI planes (full stdio face, not lean) and takes `ref`.
- `share-with-execute` (#2756, #2761; dry runs live 2026-11-28): `om watch share <watch> --with-execute` ships one watch with its money steps' terms and keeps its live posts; it is no longer refused outside `--group`/`--ref`, and it ships the recipe without `--with-recipe`. The card adds `Money steps ship with their terms, never the values typed at the arm; each installs disabled and arms on the installing machine's terminal`, `Paper: your account <name> stays here; installers get a new one` for a paper account, and the record row (`runner/trading-record/card-rows.ts`): `Record: shown on the registry`, `Record: hidden; <command> shows it`, or for real money `Record: hidden until <command> at a terminal` and `Address: <addr> (also shows your other trades)`; several steps label it `Record <member>/<step>`. The `Steps N on <slug>` row names what a chain does with money: `books paper trades`, `places orders`, `cancels orders`, `sends funds`, `buys listings`, `cancels subscriptions`, `holds a paper position`, and `moves funds` only for a plug-in mode (`runner/packages/money-line.ts:189-206`).
  - A republish keeps the last version's choice: a bare `om watch share <watch>` (or a chat "publish") ships the money steps again when the last version did, and the record stays (source). `--no-with-execute` (chat and MCP `with_execute: false`) keeps them home; a version that stops shipping a step whose record shows adds `Record: comes down from the registry (<step> no longer ships)` (source; on a never-published watch the dry run simply drops the money rows, live).
  - Refused, exit 2 `invalid_input` (live): `--fires-only --with-execute` is `with_execute ships money steps in the recipe, and a posts-only share ships none` (hint `Drop --fires-only to ship the recipe, or drop --with-execute.`); `--ref <one watch>` with no `--name` is `refs needs name: a pack publishes under a name of its own` (hint `Pass --name <short>, or share it on its own: om watch share <slug>`).
  - A `--ref` pack defaults an inbound member to `stream`, so it ships 0 steps; `--ship <slug>=recipe` ships the money step (live).
- `record-contents` (#2755, source only): the snapshot carries the step's 20 latest `decisions`, newest first (a paper account's opens, closes, adjustments, reviews and passed signals with a short reason such as `Price past the limit`; an order step's placed, filled, cancelled, refused or failed orders), and `closes_at` on each open Polymarket position. `om watch record show <watch> --format json` carries them inside `record`, which is filled only at a human terminal (`actions/watch/record-show.ts:279-298`); there is no new top-level key. A Polymarket position the market settled at 0 closes as a loss, and a resolved real position closes at what the market paid.
- `push-notices` (#2750, #2760, source only): one notice per watch whose record shows. `Trading record not sent: <label>` with `Error: <reason>` and `Retry: every minute` when passes keep failing; with `Sign-in: ended` and `Sign in again: om login at a terminal` when the sign-in has ended; a registry refusal reads `Retry: when the registry updates, or every hour` for `invalid_trading_record`, else `Retry: every hour`. A watch published before records reads `Trading record can be shown: <label>`, `Record: hidden, published before trading records`, `Show it: <cmd>` (`runner/trading-record/push-lane.ts:200-296`). The daemon refreshes a stale sign-in token before it sends and once more on a 401.

## How to get to it (user POV)

Share a trading watch with its execution (`om watch share <watch> --with-execute`; since #2756 one watch ships on its own, and a republish keeps the choice), then open its registry page. A paper record appears on its own. For a real-money step, run `om watch record show <watch>` in your own terminal and answer the prompt.

## Driving it with control-om

A guest lane proves the refusals only:

```bash
control-om om -- watch create cond-probe --condition \
  '{"metric":"price","selector":{"symbol":"BTCUSDT","exchange":"BINANCE_FUTURES","interval":"MINUTE"},"op":"gt","value":1000000}'
control-om om -- watch record show cond-probe              # exit 2 watch_not_published
control-om om -- watch record show cond-probe --delay -5   # exit 2 --delay takes whole seconds, 0 or more
control-om om -- watch record hide cond-probe              # exit 2 watch_not_published
```

Over stdio, `tools/call` `watch_record_show` with `{"ref":"cond-probe"}` answers the same error.

The share card is reachable on a guest with `--dry-run`. Make a paper account and import a watch with one inbound `accept_all` source and one `book` step. The step's fields go under `payload`, and on a home with no channel the step needs `"channels": []` (else `watching_action_destination_unresolved`):

```bash
control-om om -- paper create vom-book --yes --format json      # note account.id
cat > book-watch.json <<'JSON'
{"spec_version":3,"id":"book-probe","slug":"book-probe","label":"book-probe","enabled":true,
 "sources":[{"source_id":"src_book_in","name":"signals","role":"trigger","enabled":true,"kind":"inbound",
   "instruction":{"user_goal":"signals"},"classifier":{"mode":"accept_all"}}],
 "actions":[{"id":"book","kind":"money","channels":[],
   "payload":{"mode":"book","account":"vom-book","account_id":"<pa_ id>"}}],
 "notify":{"enabled":false}}
JSON
control-om om -- watch import book-watch.json
control-om om -- watch share book-probe --with-execute --dry-run --format text   # Record: shown on the registry
control-om om -- watch share book-probe --no-with-execute --dry-run --format text
control-om om -- watch share --ref book-probe --name vompack --with-execute --ship book-probe=recipe --dry-run --format text   # books paper trades
control-om om -- watch share book-probe --fires-only --with-execute --dry-run   # exit 2
control-om om -- watch share --ref book-probe --dry-run                          # exit 2 refs needs name
```

The success paths need a completed publication row, which only a real `om watch share --with-execute` against a registry account writes. Seeding one by hand would be a fixture, not a drive.

## Gotchas

- The publication check runs before the trading-step check, so a watch with no paper or money step still answers `watch_not_published` until it is shared.
- The MCP argument is `ref`, not `watch` or `id_or_slug`.
- A piped call prints the JSON error even without `--format json`.
- `om watch publish --with-execute` with no `--ref` or `--group` is not refused cleanly: it throws `--with-execute rides --group or --ref (a composite publish) only` as an uncaught error, so the terminal shows a Bun source excerpt and a stack, exit 1, even with `--format json` (`cmd/publish.ts:183`; live 2026-11-28). Single-watch `--with-execute` lives on `om watch share`, not `om watch publish`.
- A `--ref` pack whose member ships as a stream still prints the `Money steps ship with their terms` row while its card says `0 steps in 0 chains` (live 2026-11-28).

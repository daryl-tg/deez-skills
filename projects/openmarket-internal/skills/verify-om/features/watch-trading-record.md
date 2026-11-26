# A trading watch's record on its registry page

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

## How to get to it (user POV)

Share a trading watch with its execution (`om watch share <watch> --with-execute`), then open its registry page. A paper record appears on its own. For a real-money step, run `om watch record show <watch>` in your own terminal and answer the prompt.

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

The success paths need a completed publication row, which only a real `om watch share --with-execute` against a registry account writes. Seeding one by hand would be a fixture, not a drive.

## Gotchas

- The publication check runs before the trading-step check, so a watch with no paper or money step still answers `watch_not_published` until it is shared.
- The MCP argument is `ref`, not `watch` or `id_or_slug`.
- A piped call prints the JSON error even without `--format json`.

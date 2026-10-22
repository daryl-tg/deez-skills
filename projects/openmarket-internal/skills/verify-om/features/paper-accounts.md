# Paper trading accounts

*Verified: 2026-10-22, tree `db6e76ef5` (origin/main, v0.460.0): `paper create verify-book` without `--yes` was refused with `confirmation_required`, and with `--yes` gave `{account:{id:pa_…,name,cash:1000},desk:"off"}`. `ls` gave `accounts[]` with id, name, cash, starting_cash, open_lots, open_stakes, open_value and realized_pnl. `show` gave account, rules and lots. `log` gave `{entries:[],next_cursor:null}`. `set --ticket 10 --yes` returned the rules, and `reset --yes` returned `generation:1`. The Paper tab (inside `tablist` with tabs Strategies / Paper) showed the line and the ACCOUNT…REALIZED P&L headers with the row. Opening and closing trades were not driven. Previous stamp `7e22214fb` is on branch `daryl/watch-narrative`, not an ancestor of main.*

A paper account is pretend money held locally: no venue, no credentials, no real
order ever placed. A user opens one from the CLI, and it shows up in the
dashboard beside the real strategies. It is the most guest-reachable of the
product's money-shaped surfaces, because none of it is money.

## Sub-features

- `paper-create` opens a named account with starting cash.
- `paper-ls` lists accounts with cash, open lots, staked, open value and P&L.
- `paper-tab` renders the same accounts in the dashboard.
- `paper-desk` is the per-account automation switch, `off` on a new account.

## How to get to it (user POV)

- `om paper create <name>` in a terminal, then `om paper ls`.
- Or open the dashboard, go to Strategies, and choose the `Paper` tab.

## Driving it with control-om

Preconditions: a lane the run started. Nothing else — no account, no model
credential, no venue.

- **Create.** `control-om om -- paper create verify-book --yes --format json`
  returns `{"account":{"id":"pa_<uuid>","name":"verify-book","cash":1000},"desk":"off"}`.
  **`--yes` is required**: without it the call exits with
  `{"error":"confirmation_required", ...}` because the verb is confirm-gated, so
  a non-interactive drive that omits it reads as a failure.
- **List.** `control-om om -- paper ls --format json` returns `accounts[]` with
  `id`, `name`, `cash`, `starting_cash`, `open_lots`, `open_stakes`,
  `open_value`, `realized_pnl`. **The verb is `ls`, not `list`** — `om paper
  list` fails with `unknown command 'list'; did you mean 'ls'?`.
- **Cross-check the other surface.** Open `control-om url /strategies`, click
  `tab "Paper"`, and assert the table: a paragraph reading
  `Pretend money on local paper accounts. Nothing here is a venue account.`
  above columns `ACCOUNT`, `CASH`, `OPEN LOTS`, `STAKED`, `OPEN VALUE`,
  `REALIZED P&L`, with a row per account. Before any account exists the tab
  shows the empty state `No paper accounts yet: om paper create <name>.`
- **Proof.** Keep the create and `ls` JSON and the Paper-tab snapshot. The
  account id ties them together.

## Gotchas

- The Paper surface lives as a TAB on `/strategies`, not at `/paper`. The
  standalone `/paper` route exists only in the OSS export build — see
  [the ops dashboard](./ops-dashboard.md) for why, and for the dead link that
  points at it.
- `paper create` is confirm-gated despite creating nothing real; that is the
  CLI's blanket treatment of account-shaped verbs, not a sign it touches money.
- A new account's `desk` is `off`. Nothing automates against it until that
  changes, so a driver waiting for activity on a fresh book waits forever.
- `log`, `set` and `reset` were driven at `db6e76ef5` (shapes in the stamp).
  `reset` without `--yes` is refused with `confirmation_required`. `open
  [account] --signal <json>`, `close <account> <lot>`, `reset-all`, `digest` and
  `digest-set` exist but were not driven; treat their output shapes as
  unverified.

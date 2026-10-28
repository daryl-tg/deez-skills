# Paper trading accounts

*Re-driven 2026-10-28 (scheduled maintenance, smoke depth), tree `186030b63` (origin/main): `paper ls`, `paper create verify-book-1028 --yes` (cash 1000, `desk: off`) and `paper show`. `/paper` rendered only the shell, as documented. Steps not named here keep the record below. Evidence: `http://127.0.0.1:8098/verify-om-maint-20261028/r1/`.*

*Verified: 2026-10-28, tree `a8fa10974` (origin/main, v0.466.0), lane on 18103. `paper create verify-book` without `--yes` exited 2 `confirmation_required`; with it, it returned `{account:{id:"pa_…", cash:1000}, desk:"off"}`. `paper ls` returned the eight mapped fields, and `paper list` failed `unknown command 'list'; did you mean 'ls'?`. Newly driven: `paper show verify-book`, which returned `account` (with `generation`, `venue`, `holds`), `rules` and `lots: []`. The Paper tab showed the explanatory paragraph, the six columns and the row, plus `No equity recorded yet`, `No open lots.` and an empty Decisions table. Not driven: open, close, reset-all, digest, and the #2176 resting stop/limit on a lot (needs a target step). Previous stamp `8fe6a8432` is an ancestor (10 commits).*

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
- **Show one book.** `control-om om -- paper show verify-book --format json`
  returns `account` (`id`, `name`, `cash`, `starting_cash`, `generation`,
  `venue`, `holds`), `rules` (`ticket 25`, `ticket_cap 50`, `entries_per_day
  4`, `open_stakes 250`, `one_position_per_market`), `lots: []` and `desk`
  (driven 2026-10-28). Each lot carries its `exit`. Since #2176, a target
  step rests the package's nearest closing stop and limit there
  (`{"sl_price", "tp_price"}`), and the `paper-exits` loop fills them when the
  mark crosses. That needs a target step, which a guest lane cannot drive (see
  README).
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
- **`desk` is not always `off`.** `paper create` from a human terminal or chat
  sets `desk: "on"` when the setting `paper.auto_arm` reads on (`on`, `true`, `1`
  or `yes`; `actions/paper/create.ts`, `runner/paper/desk.ts`). A fresh guest
  lane leaves it unset, so `"desk":"off"` is the lane's answer, not a
  constant. MCP and the daemon never arm the desk.
- The Paper tab first renders a single row `Loading paper accounts…` for a second
  or two before the table (driven 2026-10-26). A snapshot taken right after the
  tab click finds no column headers. Wait for `columnheader "ACCOUNT"` before
  asserting.

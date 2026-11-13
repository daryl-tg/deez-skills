# Paper trading accounts

*Re-driven 2026-11-14 (nightly), tree `05300a3142` (origin/main, v0.495.0+internal), guest lane on 18185 started through `bootstrap.internal.ts`, booted with no guest 429. `paper create verify-book --yes` (`cash: 1000`, `desk: off`), `paper ls` (`starting_cash 1000`, `open_lots 0`), `paper show verify-book` (rules `ticket 25`, `ticket_cap 50`, `entries_per_day 4`, `open_stakes 250`), and `paper digest --format text` (`Paper verify-book`, `Cash: $1,000.00`, `Fills: none`). Not re-driven: the Paper tab, reset. Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261114/r1/` (`cli/paper-kscript.txt`).*

*Re-driven 2026-11-11 (nightly), tree `0ad4768f66` (origin/main, v0.494.0), guest lane on 18181, booted with no guest 429. Refusals only: `paper create` without `--yes` exits 2 `confirmation_required`, and `paper show` on a name that does not exist exits 2 `paper_book_unknown` with the `om paper ls` hint. Not re-driven: create with `--yes`, `ls`, `digest`, the Paper tab. Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261111/r1/`.*

*Re-driven 2026-11-10 (nightly), tree `c9bc93a355` (origin/main, v0.493.1), guest lane on 18143, booted with no guest 429. `paper create verify-book --yes` (cash 1000, `desk: off`) and `paper show`. Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261110/r1/` (`cli/paper-*.txt`).*

*Re-driven 2026-11-09 (scheduled maintenance), tree `0d3d29cd27` (origin/main, v0.493.0), bare lane on 18145 (dummy `OM_API_KEY`, dead service URLs) with a scripted fake model on 18144. `paper create verify-book --yes` (`cash 1000`, `desk off`), `paper ls --format json`. Evidence: `http://127.0.0.1:8098/verify-om-maint-20261109/r1/`.*

*Re-driven 2026-11-09 (nightly), tree `5bfa0ccf6` (origin/main, v0.492.0), guest lane on 18143, booted with no guest 429. `paper create lane-paper --yes` (`cash` 1000, `desk: off`), `paper show`; without `--yes` exit 2 `confirmation_required`. Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261109/r1/` (`cli/42-43`).*

*Re-driven 2026-11-08 (nightly), tree `5590b4d1c` (origin/main, v0.492.0), guest lane on 18141, booted in 2 s with no guest 429. `paper create verify-book --yes --format json` (`cash` 1000, `desk: off`), `paper show verify-book` (`ticket` 25, `ticket_cap` 50). Not re-driven: `paper ls`, `digest`, `log`, reset and close. Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261108/r1/` (`cli/62-63`).*

*Re-driven 2026-11-07 (nightly), tree `05f450fc5` (origin/main, v0.492.0), guest lane on 18141, booted with no guest 429. `paper create verify-book --yes --format json` (`cash: 1000`, `desk: off`), `paper ls`, `paper show verify-book` (`rules.ticket 25`). Not re-driven: digest, trades. Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261107/r1/` (`cli/75-77`).*

*Re-driven 2026-11-06 (nightly), tree `50fcc594b` (origin/main, v0.492.0), guest lane on 18163 (`OM_FEED_ALLOW_LOOPBACK=1`, `OM_FEED_POLL_INTERVAL_MS=60000`), booted at 19:18Z with no guest 429, host load average 10 falling to about 3.3. `paper create verify-book --cash 1000` without `--yes` exit 2 `confirmation_required`; with it `cash 1000`, `desk off`; `paper ls`, `paper digest` (`Cash: $1,000.00`). Not re-driven: the Paper tab. Evidence: `http://127.0.0.1:8098/vom-nightly-20261106/r1/` (`cli/paper-*`).*

*Re-driven 2026-11-05 (nightly), tree `3a0ea623e` (origin/main, v0.492.0), guest lane on 18163 (`OM_FEED_ALLOW_LOOPBACK=1`, `OM_FEED_POLL_INTERVAL_MS=60000`), booted in 2 s at 19:19Z with no guest 429, host load average about 4.4. `paper create verify-book` without `--yes` exit 2 `confirmation_required`; with it `cash 1000`, `desk off`; `paper ls`, `paper show`, `paper digest` (`Cash: $1,000.00`). Not re-driven: the Paper tab. Evidence: `http://127.0.0.1:8098/vom-nightly-20261105/r1/` (`cli/paper-*`).*

*Re-driven 2026-11-04 (nightly), tree `9acb5fb56` (origin/main, v0.491.0), guest lane on 18163 (`OM_FEED_ALLOW_LOOPBACK=1`, `OM_FEED_POLL_INTERVAL_MS=60000`), booted in 2 s at 19:19Z with no guest 429, host load average about 3.5. `paper create verify-book` without `--yes` exit 2 `confirmation_required`; with `--yes` `{cash:1000, desk:"off"}`; `ls`; `digest --format text` (`Cash: $1,000.00`, `Equity: $1,000.00`). The Paper tab was not re-driven. Evidence: `http://127.0.0.1:8098/vom-nightly-20261104/r1/` (`cli/140-143`).*

*Re-driven 2026-11-03 (nightly), tree `777ee7f21` (origin/main, v0.488.0), lane on 18163 (`OM_FEED_ALLOW_LOOPBACK=1`, `OM_FEED_POLL_INTERVAL_MS=60000`), host load average about 2.8; the first `up` died on a guest sign-in 429 (35 minutes) and the lane booted in 3 s at 19:55Z. `paper create verify-book` without `--yes` exit 2 `confirmation_required`; with `--yes` `{cash:1000, desk:"off"}`; `ls`, `show` (rules: ticket 25, cap 50, 4 entries a day), `digest --format text` (`Steps: none`, `Cash: $1,000.00`). The Paper tab was not re-driven. Evidence: `http://127.0.0.1:8098/vom-nightly-20261103/r1/` (`cli/110-114`).*

*Re-driven 2026-11-02 (scheduled maintenance), tree `587ce2d0b` (origin/main, v0.480.3), lane on 18168 (`OM_FEED_ALLOW_LOOPBACK=1`, `OM_FEED_POLL_INTERVAL_MS=60000`), host load average about 5. `paper create verify-book` without `--yes` → `confirmation_required`; with `--yes` → `cash 1000`, `desk off`; `ls`, `show` (`ticket 25`, `ticket_cap 50`, `entries_per_day 4`), `digest --format text` (`Paper digest`, `Steps: none`); the Strategies **Paper** tab lists `verify-book` under Account, Cash, Open lots, Staked, Open value, Realized P&L.*

*Re-driven 2026-11-02 (nightly), tree `2567b7974` (origin/main, v0.480.3), lane on 18163 (`OM_FEED_ALLOW_LOOPBACK=1`, `OM_FEED_POLL_INTERVAL_MS=60000`), host load average about 4. `paper create verify-book` without `--yes` exit 2 `confirmation_required`; `create verify-book --cash 5000 --yes` and `verify-book-b --cash 1000 --yes` returned the `pa_` ids; `ls` listed both with `starting_cash` and zeroed lots; `show verify-book` returned `rules` (`ticket 25`, `ticket_cap 50`, `entries_per_day 4`, `open_stakes 250`), `lots: []`, `desk: off`; `digest --format text` opened `Paper digest` / `Steps: none` then one block per account; `paper list` failed `did you mean 'ls'`. The Paper tab listed both rows under `Pretend money on local paper accounts…`. Not driven: open, close, reset-all, `digest-set`, the scheduled edition, and the target-step rows (#2176, #2188, #2192, #2242) which need a target step. Evidence: `http://127.0.0.1:8098/vom-nightly-20261102/r1/` (`cli/121-127`, `strategies-paper-tab.png`).*

*Re-driven 2026-11-01 (nightly), tree `7ce379c45` (origin/main, v0.480.3), lane on 18163 (`OM_FEED_ALLOW_LOOPBACK=1`, `OM_FEED_POLL_INTERVAL_MS=60000`), host load average about 2.9. `paper create verify-book --yes` → `cash: 1000`, `desk: off`; `paper ls` listed it with `starting_cash` and `open_lots: 0`; `paper show` returned `account` (`generation 0`, `venue null`, `holds []`), the five `rules`, `lots: []` and `desk`; `paper digest --format text` printed `Paper digest`, `Steps: none`, `Paper verify-book`, `Cash: $1,000.00`, `Equity: $1,000.00`, `Open: 0 lots`, `Fills: none`, `Skips: none`. The Strategies Paper tab showed the paragraph and the `verify-book` row. Evidence: `http://127.0.0.1:8098/vom-nightly-20261101/r1/` (`cli/70-73`, `dash-strategies-paper*`).*

*Re-driven 2026-10-31 (nightly), tree `dfefe0a21` (origin/main, v0.480.2), lane on 18163 (`OM_FEED_ALLOW_LOOPBACK=1`, `OM_FEED_POLL_INTERVAL_MS=60000`), host load average about 1.6. `paper create verify-book --yes` → `cash: 1000`, `desk: off`; `paper ls` listed it with `starting_cash`, `open_lots: 0`; `paper digest --format text` printed `Paper digest`, `Steps: none`, `Paper verify-book`, `Cash: $1,000.00`, `Fills: none`, `Skips: none`. The Strategies Paper tab showed the paragraph and the `verify-book` row. Evidence: `http://127.0.0.1:8098/vom-nightly-20261031/r1/` (`cli/70-72`, `dash-strategies-paper*`).*

*Re-driven 2026-10-30 (scheduled maintenance), tree `3cb50a821` (origin/main, v0.478.0), fresh lane on 18165, host load average about 140. `paper create maint1030 --yes` gave `cash: 1000` and `desk: off`; `paper ls` listed it; `paper digest` read `Steps: none` with `Cash: $1,000.00`. Evidence: `http://127.0.0.1:8098/verify-om-maint-20261030/r1/`.*
*Re-driven 2026-10-30 (nightly, empty read only), tree `3cb50a821` (origin/main, v0.478.0), lane on 18163: `paper ls --format json` returned `{accounts:[]}` on a fresh lane. Nothing else was re-driven. Evidence is local only (the `8098` renderer did not answer): `artifacts/vom-nightly-20261030/r1/`.*

*Re-driven 2026-10-29 (scheduled maintenance, smoke depth), tree `7ec575e55` (origin/main, v0.467.0 plus #2194), fresh lane on 18161. `paper create maint1029` without `--yes` exited 2 `confirmation_required`; with it, it returned `{account:{id:"pa_…", name, cash:1000}, desk:"off"}`. `paper show` returned `{account, rules}`, and the text `paper digest` opened `Paper digest` / `Steps: none` / `Paper maint1029` / `Cash: $1,000.00`. Evidence: `http://127.0.0.1:8098/verify-om-maint-20261029/r1/`.*

*Verified: 2026-10-29 (nightly), tree `32ca0d6c7` (origin/main, v0.467.0), lane on 18103. Newly driven: `paper digest`. After `paper create acct-a --cash 5000 --yes` and `acct-b --cash 1000`, the all-accounts digest opened with `Steps: none` (new with #2192) and then one block per account (`Cash`, `Equity`, `Open: 0 lots`, `Fills: none`, `Skips: none`). `paper digest acct-a` had no `Steps` paragraph. The Paper tab listed both rows and `Total $6,000.00`. Not driven: open, close, reset-all, `digest-set`, the scheduled edition, and the #2176/#2188/#2192 target-step rows (they need a target step). Evidence: `http://127.0.0.1:8098/vom-nightly-20261029/r1/` (`paper-digest.txt`, `07-paper-tab.png`).*

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
- `paper-digest` renders the digest now, without posting it. The all-accounts form opens with a `Steps:` paragraph: `Steps: none`, or the step count with `Holding` and `Realized`. Each account block may add `Step: <id> of <watch>` rows for target-step lots (#2192).

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
- **Digest.** `control-om om -- paper digest --format text` prints
  `Paper digest`, then `Steps: none`, then `Paper <name>` blocks with `Cash`,
  `Equity`, `Open: N lots`, `Fills` and `Skips`. Without `--format` the call
  outside a TTY prints `{"digests":[{"title","body"}]}`. `paper digest <name>`
  renders one account, titled `Paper <name>`, with no `Steps` paragraph. Nothing
  is posted or stored. The `Steps` paragraph appears only while the digest's
  sections include positions or fills.
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
  [account] --signal <json>`, `close <account> <lot>`, `reset-all` and `digest-set` exist but were
  not driven; treat their output shapes as unverified.
- **`desk` is not always `off`.** `paper create` from a human terminal or chat
  sets `desk: "on"` when the setting `paper.auto_arm` reads on (`on`, `true`, `1`
  or `yes`; `actions/paper/create.ts`, `runner/paper/desk.ts`). A fresh guest
  lane leaves it unset, so `"desk":"off"` is the lane's answer, not a
  constant. MCP and the daemon never arm the desk.
- The Paper tab first renders a single row `Loading paper accounts…` for a second
  or two before the table (driven 2026-10-26). A snapshot taken right after the
  tab click finds no column headers. Wait for `columnheader "ACCOUNT"` before
  asserting.

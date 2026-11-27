# Watch pack page and trading record

A watch pack's page shows its watches: the market rules it watches, the steps each one runs, and
for a watch whose steps trade, a "Trading record" section. The creator's om pushes the record, and
the page draws it as an account curve with runs, open positions, closed trades with their profit or
loss, and the signals behind them. The catalog lists watch packs under their own "Watch packs" card,
with a badge naming the account a trading pack uses.

Last verified 2026-11-28 on openmarket-registry `c263de6` (fresh detached worktree, Bun 1.3.14, lane
18154, seed tokens `dev-token` and `other-token`, watch-pack kinds on with a dummy topics service
and an https share origin). Scope: a recipe-only watch pack with a paper `book` step published
through the real route, its page before and after a paper record with a win, a loss and two signals,
the % and $ views and the 1D range, a trade's "Why", the record door's refusals, the record's
delete, a v1.0.1 that turns the step into a Hyperliquid order, and the catalog card and row.
Limitations: no followable or shared pack (that needs a device proof, the topics service and the
relay), no real-money record (that needs a signed wallet proof and venue access), so the "Record
received, its wallet isn't proven yet." and "Fills" states were not seen; "No record of this step's
current kind yet." was not reachable (see Gotchas); "Open on charts" was not pressed.

## Sub-features

- `watch-page`: breadcrumb "@scope / name", the pack name, its account badge ("Paper account"),
  radios "Overview", "N Version(s)" and "Contents", then SOURCES ("1 market rule", the rule) and
  STEPS ("2 steps · 1 chain"). The Watch pack card's Permissions fact reads "Paper trades only, no
  venue orders" for paper steps and "Real venue orders, once you arm it" for an order step.
- `record-empty`: a trading pack with no record shows h2 "TRADING RECORD", the badge, "Reported by
  the creator's om" and "No record received yet."
- `record-hidden`: from source (`src/trading-record-page.ts` `HIDDEN_WORDS`), a stored record that
  no longer fits the step reads "No record of this step's current kind yet.", and a real record
  with no wallet proof reads "Record received, its wallet isn't proven yet.". Live verification
  pending for both.
- `record-shown`: after a record lands, "As of <UTC time>" (for a record two hours old), radios "%"
  and "$" and "1D", "1W", "1M", "All", a curve group named "Paper account curve, N points. …", the
  caption "Curve: paper account value, marked to market, from each run's start", a runs table (RUN,
  STARTED, UTC, RETURN, MAX DRAWDOWN, TRADES, WIN RATE; rows "Run 1", …), h3 "Open positions" ("None
  open." or a table), h3 "Trades" (CLOSED, UTC, SIDE, ENTRY → EXIT, PNL, RESULT; a loss reads
  "-$20.00" and "-18.18%"), and h3 "Signals" (TIME, UTC, OUTCOME, REASON) when the record carries
  `decisions`. Each trade and signal row has a "Why" disclosure.
- `record-door`: `PUT` and `DELETE /v1/packages/:scope/:name/trading-record/:watch/:step` under
  the scope owner's bearer. PUT answers `{"package","watch","step","checks":{"matches","not_found",
  "unchecked"}}`; DELETE answers `{"package","watch","step","deleted":true}`, or `false` when no
  record was stored. Refusals: no bearer 503 `verifier_not_configured`, another account 403
  `forbidden`, a non-JSON body 400 `bad_request`, and 422 `invalid_trading_record` with an
  `issues` line for an `as_of` more than ten minutes ahead, a `step_id` that is not the path's, or
  a paper record against an order step ("basis: this step trades on real money").
- `record-dropped`: publishing a version whose step no longer fits the stored record deletes the
  record; the page then reads "No record received yet." under the new badge ("Hyperliquid").
- `catalog-watch-row`: the home page gains a "Watch packs N package(s)" card, and the row reads
  "@scope/name", "Paper account", "watch pack", the version and the description.
- Real-money records, followable packs and share links: live verification pending.

## How to get to it (user POV)

- Open `/@scope/name` for a watch pack, or pick it from the catalog's "Watch packs" card.
- A creator's om pushes the record as their watch trades; nobody types it in.

## Driving it with control-om-registry

Preconditions:

- A lane started with watch-pack kinds on. A bare lane cannot boot them on `http://127.0.0.1`
  alone: the share origin must be https, and the topics service must be named.
  `WATCH_PACK_KINDS_ENABLED=on ALERT_TOPICS_URL=http://127.0.0.1:9 ALERT_TOPICS_SERVICE_KEY=lane-dummy OM_REGISTRY_ALERT_SHARE_ORIGIN=https://registry-lane.invalid OM_REGISTRY_STATIC_TOKENS='{"dev-token":{"account_id":"acct-dev","tier":"pro"}}' $CR up`.
  A recipe-only pack never calls the topics service, so the dummy URL is enough.
- `$CR doctor` passes.

- **Build the pack.** From the driven worktree, write the tarball with the repo's tarball builders
  (they only make bytes; the row still goes through the real publish). Use a script in your scratch
  directory that imports `CONDITION_WATCH` and `recipeMember` from `test/alert-share-helpers.ts`
  and `makeManifest`, `makePackageTarGz` from `test/helpers.ts`. Give the watch the actions
  `judge` (`kind:"ai"`, `payload.output.type:"paper_signal"`) and `book` (`kind:"money"`,
  `input:{watch_id:"btc-dip",action_id:"judge"}`, `payload:{mode:"book",account:"new"}`), with
  manifest `{spec_version:"1.3",name:"@acme/desk",kind:"watch-pack"}`. The tarball holds
  `om-package.json` and `watches/btc-dip.json`.
- **Publish.** The publish `curl` from [Publish a package](./publish-a-package.md) answers 200 with
  `"listing_url":"…/@acme/desk"`.
- **Page before the record.** `$CR browser open $O/@acme/desk`; `get text main` reads "TRADING
  RECORD", "Reported by the creator's om" and "No record received yet.", and the Permissions fact
  "Paper trades only, no venue orders". Save the pair.
- **Push a paper record.** Write a `TradingRecordSnapshot` (`watch:"btc-dip"`, `step_id:"book"`,
  `basis:"paper"`, `venue:"market_data"`, `currency:"USD"`, `delay_s:0`, `marks:[]`, `as_of` two
  hours in the past, one run with `equity` points and four fills: a buy and a sell at a profit, then
  a buy and a sell at a loss with a negative `realized_pnl`). `paperSnapshot` in
  `test/trading-record-door.test.ts` is the model. For the Signals table add `decisions`, newest
  first, each `{at, run:0, market:"BTC", outcome:"opened"|"closed"|…, reason:{code, words},
  signal}` with `at` at or before `as_of`.
  `curl -sS -X PUT $O/v1/packages/@acme/desk/trading-record/btc-dip/book -H 'authorization: Bearer dev-token' -H 'content-type: application/json' --data-binary @snapshot.json`
  answers 200.
- **Refusals.** The same PUT with no bearer (503), with a second seed token for another account
  (403 `forbidden`), with `-d x` (400), with `as_of` eleven minutes ahead (422) and with
  `step_id:"judge"` (422).
- **Page with the record.** Reopen the page; `get text main` shows "As of", "Run 1", the two trades
  and the Signals table. Save the pair. Pick "$" with `$CR browser find text '$' click --exact`:
  the axis turns to account value (9,990 to 10,010). Pick "1D" the same way, and confirm with
  `$CR browser eval 'JSON.stringify([...document.querySelectorAll("#trading-record input[type=radio]")].map(r=>[r.labels?.[0]?.textContent.trim(),r.checked]))'`.
- **Catalog.** `$CR browser open $O/` shows the link "Watch packs 1 package" and the row's "Paper
  account" badge.
- **Delete.** `curl -sS -X DELETE …/trading-record/btc-dip/book -H 'authorization: Bearer dev-token'`
  answers `"deleted":true`, and the page reads "No record received yet." again.
- **A kind change drops the record.** Push the record again, then publish 1.0.1 whose `book` step is
  `payload:{mode:"order",terms:{venue:"hyperliquid",asset:"BTC",size_mode:"quote"}}` behind a judge
  with `output:{type:"word",words:["buy","sell","none"]}`. The page's badge turns to "Hyperliquid",
  Permissions reads "Real venue orders, once you arm it", the panel reads "No record received yet.",
  and a DELETE answers `"deleted":false`.

## Gotchas

- From source, not driven: with `WATCH_PACK_KINDS_ENABLED=on` and only an http public URL the boot
  fails, because the share origin goes through `canonicalRegistryOrigin`, which refuses http; and
  without `ALERT_TOPICS_URL` and `ALERT_TOPICS_SERVICE_KEY` it refuses to boot. The lane above sets
  all three and boots.
- A PUT with no bearer answers 503 `verifier_not_configured` on a seed-token lane.
- The "%", "$" and range radios sit under their labels, so `check @eN` is refused as covered.
  Click the label text with `find text '<label>' click --exact`.
- "No record of this step's current kind yet." is hard to reach: a publish that changes a step's
  kind runs `dropStaleTradingRecords` (`src/server.ts`), and the door refuses a record that does
  not fit the latest step. Only a record stored before the drop runs shows it.
- An order step's judge must emit a word (`buy`, `sell`, `none`); a `paper_signal` judge fails the
  publish with 422 `watching_reader_unsatisfied`. `terms` needs `asset` and `size_mode`, and an
  unknown key such as `size` fails with 422 `invalid_watch_pack`.
- From source, not driven: "As of" shows only when the record is more than ten minutes old
  (`src/trading-record-page.ts`), so a fresh `as_of` hides it.

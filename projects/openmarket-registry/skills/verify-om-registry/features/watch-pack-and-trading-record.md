# Watch pack page and trading record

A watch pack's page shows its watches: the market rules it watches, the steps each one runs, and
for a watch whose steps trade, a "Trading record" section. The creator's om pushes the record, and
the page draws it as an account curve with runs, open positions and trades. The catalog lists watch
packs under their own "Watch packs" card, with a badge naming the account a trading pack uses.

Last verified 2026-11-27 on openmarket-registry `098a3de` (fresh detached worktree, Bun 1.3.14,
lane 18120, seed token `dev-token`, watch-pack kinds on with a dummy topics service and an https
share origin). Scope: a recipe-only watch pack with a paper `book` step published through the real
route, its page before and after a paper record, the % and $ views, the record's delete, and the
catalog card and row. Limitations: no followable or shared pack (that needs a device proof, the
topics service and the relay), no real-money record (that needs a signed wallet proof and venue
access), and "Open on charts" was not pressed.

## Sub-features

- `watch-page`: breadcrumb "@scope / name", the pack name, its account badge ("Paper account"),
  radios "Overview", "N Version(s)" and "Contents", then SOURCES ("1 market rule", the rule) and
  STEPS ("2 steps · 1 chain").
- `record-empty`: a trading pack with no record reads "TRADING RECORD", "Reported by the creator's
  om" and "The creator hasn't shown this record."
- `record-shown`: after a record lands, "As of <UTC time>", radios "%" and "$" and "1D", "1W",
  "1M", "All", a curve group named "Paper account curve, N points…", a RUN table (STARTED, RETURN,
  MAX DRAWDOWN, TRADES, WIN RATE), "Open positions" and a Trades table.
- `record-door`: `PUT` and `DELETE /v1/packages/:scope/:name/trading-record/:watch/:step` under
  the scope owner's bearer. PUT answers `{"package","watch","step","checks":{…}}`; DELETE answers
  `{"deleted":true}`.
- `catalog-watch-row`: the home page gains a "Watch packs N package(s)" card, and the row reads
  "<name>", "Paper account", "watch pack", the version and the description.
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
- **Page before the record.** `$CR browser open $O/@acme/desk`; `get text main` reads "The creator
  hasn't shown this record." Save the pair.
- **Push a paper record.** Write a `TradingRecordSnapshot` (`watch:"btc-dip"`, `step_id:"book"`,
  `basis:"paper"`, `venue:"market_data"`, `currency:"USD"`, `as_of` in the past, one run with
  `equity` points and two fills; `paperSnapshot` in `test/trading-record-door.test.ts` is the
  model). `curl -sS -X PUT $O/v1/packages/@acme/desk/trading-record/btc-dip/book -H 'authorization: Bearer dev-token' -H 'content-type: application/json' --data-binary @snapshot.json`
  answers 200.
- **Page with the record.** Reopen the page; `get text main` shows "As of", the RUN table and the
  trade. Save the pair. Pick "$" by its ref with `$CR browser check @eN`; the axis turns to account
  value.
- **Catalog.** `$CR browser open $O/` shows the link "Watch packs 1 package" and the row's "Paper
  account" badge.
- **Delete.** `curl -sS -X DELETE …/trading-record/btc-dip/book -H 'authorization: Bearer dev-token'`
  answers `"deleted":true`, and the page reads "The creator hasn't shown this record." again.

## Gotchas

- From source, not driven: with `WATCH_PACK_KINDS_ENABLED=on` and only an http public URL the boot
  fails, because the share origin goes through `canonicalRegistryOrigin`, which refuses http; and
  without `ALERT_TOPICS_URL` and `ALERT_TOPICS_SERVICE_KEY` it refuses to boot. The lane above sets
  all three and boots.
- A PUT with no bearer answers 503 `verifier_not_configured` on a seed-token lane.
- From source, not driven: the record's `as_of` may be at most ten minutes ahead of the lane's
  clock, and only the scope owner's bearer may push or delete a record
  (`src/server/routes/trading-record.ts`).

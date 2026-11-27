# Catalog and search

The home catalog lists the publicly listed packages and lets a visitor search them by name or
description and filter by kind. The same search answers as JSON at `/v1/search`, and the Indicator
store reads the same rows at `/v1/store/front` and `/v1/store/list`.

Last verified 2026-11-28 on openmarket-registry `c263de6` (fresh detached worktree, Bun 1.3.14,
lanes 18150, 18152 and 18154, seed token `dev-token`; a bare lane, then `REGISTRY_WRUN_KINDS=on`
with `OM_REGISTRY_GUIDE=1`, then watch-pack kinds on). Scope: the empty catalog, a no-match page
search, the API search, an Indicator row, the Indicators kind filter, a search hit inside the
filter, the store front and list, and the Watch packs card. Limitations: ranking between several
rows, priced rows and the community catalog (`OM_REGISTRY_COMMUNITY=1`) were not driven.

## Sub-features

- `catalog-empty`: with nothing listed the page reads "Nothing published yet." and every category
  card reads "0 packages".
- `catalog-rows`: a listed package adds a row (link `@scope/name`, kind label such as "Indicator"
  or "watch pack", version, description) and the cards count it ("all 1 package", "Indicators 1
  package"); the PACKAGES and PUBLISHERS counters rise with it.
- `catalog-search`: a query lands on `/?q=<term>`; with no match the page reads "No packages
  matched.". Searching from a filtered page keeps the filter: `/?kind=wrun-indicator&q=vol`.
- `catalog-kind`: a card opens `/?kind=<kind>` and lists that kind only; a kind with no rows reads
  "Nothing published in this category yet.".
- `catalog-cards`: a bare lane shows the "all" and "Indicators" cards. With watch-pack kinds on, a
  "Watch packs" card joins them, with "soon" placeholders for live series and execution.
- `search-api`: `GET /v1/search?q=&kind=&rank=` answers `{"results":[…],"total":N,"limit":50}`;
  each row carries name, kind, description, latest, publisher, pricing and `artwork_url`.
- `store-api`: `GET /v1/store/front` answers `official` and `community` tabs (popular, trending);
  `GET /v1/store/list` answers `{"revision","results","total"}`. Both hold Indicators only.

## How to get to it (user POV)

- Open the registry root `/`.
- Type in "Search packages" and press Enter, or press the "Search" button.
- Pick a category card under BROWSE ("all N packages", "Indicators N packages").

## Driving it with control-om-registry

Preconditions:

- `$CR doctor` passes for the lane. For rows, start the lane with `REGISTRY_WRUN_KINDS=on` and
  publish the Indicator from [Publish a package](./publish-a-package.md) (`listed-publish`).

- **Open the home page.** `$CR browser open http://127.0.0.1:<port>/`, then `$CR browser snapshot -i -c`.
  Expect h1 "The OpenMarket registry", h2 "BROWSE" and "PACKAGES", and the links "all 0 packages"
  and "Indicators 0 packages" on an empty lane. Save the snapshot and a screenshot. With
  `OM_REGISTRY_GUIDE=1` the header also holds the link "Guide" ([The om guide](./om-guide.md)).
- **Search from the page.** Two searchboxes share the name "Search packages": the header's comes
  first, the page form's second. Fill the page form's by its ref from a fresh snapshot
  (`$CR browser fill @eN btc`), then `$CR browser press Enter` and
  `$CR browser wait --load networkidle`. `$CR browser get url` reads `/?q=btc`, and
  `$CR browser get text main` contains "No packages matched." on an empty lane.
- **Search through the API.** `$CR cli -- curl -fsS 'http://127.0.0.1:<port>/v1/search?q=btc'`; exit 0
  and the JSON names the same rows the page shows.
- **Rows and the filter.** With `@acme/vol-bands` published, the home page shows the link
  "@acme/vol-bands" and "Indicators 1 package". Click that card by its ref: the URL is
  `/?kind=wrun-indicator` and the row stays. Search "vol" from there: the URL is
  `/?kind=wrun-indicator&q=vol`. `/?kind=agent-plugin` reads "Nothing published in this category
  yet." Follow the row with `$CR browser find role link click --name "@acme/vol-bands" --exact`.
- **Store.** `$CR cli -- curl -fsS http://127.0.0.1:<port>/v1/store/front` and `…/v1/store/list`
  name `@acme/vol-bands`.

## Gotchas

- `$CR browser find role searchbox fill "…" --name "Search packages"` fills the header box, the
  first of the two with that name. Use the ref of the one you mean.
- Only listed kinds appear in the catalog and in search, and each needs its lane: wrun-indicator
  needs `REGISTRY_WRUN_KINDS=on`, watch-pack needs the watch-pack lane
  ([Watch pack page](./watch-pack-and-trading-record.md)), and agent-plugin lists only with
  `OM_REGISTRY_COMMUNITY=1`. A published ontology-pack is live at its URL but never in the catalog.
- An agent-plugin is internal-only while the community is off: it never appears in search, even
  for its owner's bearer. See [Package details](./package-details.md) `internal-only`.
- The page is server rendered: the query is the URL, not a client-side filter.
- There is no `/v1/store`; it answers 404. Use `/v1/store/front` or `/v1/store/list`.

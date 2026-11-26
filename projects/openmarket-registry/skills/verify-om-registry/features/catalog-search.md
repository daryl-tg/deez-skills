# Catalog and search

The home catalog lists the publicly listed packages and lets a visitor search them by name or
description and filter by kind. The same search answers as JSON at `/v1/search`.

Last verified 2026-11-26 on openmarket-registry `c0fbc81` (fresh detached worktree, Bun 1.4.3, lane 18120, seed token `dev-token`). Scope: the empty catalog, a page search and the API search. Limitations: no listed package
existed, so ranking, result rows, category counts above zero and the kind filter with rows are not
proved.

## Sub-features

- `catalog-empty`: with nothing listed the page reads "Nothing published yet." and every category
  card reads "0 packages".
- `catalog-search`: a query lands on `/?q=<term>`; with no match the page reads "No packages
  matched.".
- `catalog-kind`: `/?kind=<kind>` filters to one kind (live verification pending, needs listed rows).
- `search-api`: `GET /v1/search?q=&kind=&rank=` answers `{"results":[],"total":0,"limit":50}`
  when nothing matches.

## How to get to it (user POV)

- Open the registry root `/`.
- Type in "Search packages" and press Enter, or press the "Search" button.
- Pick a category card under BROWSE ("all N packages", "Indicators N packages").

## Driving it with control-om-registry

Preconditions:

- `$CR doctor` passes for the lane.

- **Open the home page.** `$CR browser open http://127.0.0.1:<port>/`, then `$CR browser snapshot -i -c`.
  Expect h1 "The OpenMarket registry", h2 "BROWSE" and "PACKAGES", and the links "all 0 packages"
  and "Indicators 0 packages" on an empty lane. Save the snapshot and a screenshot.
- **Search from the page.** Two searchboxes share the name "Search packages": the header's comes
  first, the page form's second. Fill the page form's by its ref from a fresh snapshot
  (`$CR browser fill @eN btc`), then `$CR browser press Enter` and
  `$CR browser wait --load networkidle`. `$CR browser get url` reads `/?q=btc`, and
  `$CR browser get text main` contains "No packages matched." on an empty lane.
- **Search through the API.** `$CR cli -- curl -fsS 'http://127.0.0.1:<port>/v1/search?q=btc'`; exit 0
  and the JSON names the same rows the page shows.

## Gotchas

- `$CR browser find role searchbox fill "…" --name "Search packages"` fills the header box, the
  first of the two with that name. Use the ref of the one you mean.
- Only the listed kinds (wrun-indicator, watch-pack, live-series, agent-plugin) appear in the
  catalog and in search. A published ontology-pack is live at its URL but never in the catalog, so
  it cannot prove result rows.
- The page is server rendered: the query is the URL, not a client-side filter.

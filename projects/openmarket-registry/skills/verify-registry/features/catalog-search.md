# Catalog and search

The home catalog lists public packages and lets visitors search by package name or description, with optional kind filtering.

## Sub-features

- Browse the anonymous home catalog and its empty state.
- Search from the header and see the query reflected in the page.
- Filter the catalog by package kind.
- Read the JSON search response at `/v1/search`.

## How to get to it (user POV)

- Open the registry root `/`.
- Enter a term in the “Search packages” field and submit.
- Use a kind filter on the catalog when package data exists.

## Driving it with control-registry

Preconditions:

- `$CR doctor` passes.
- The default in-memory lane is empty; use a known non-empty public dataset only when one was prepared through the real publish flow.

- Open the home page with `$CR browser open http://127.0.0.1:18098/` and save an accessibility snapshot and screenshot as the action baseline.
- Take a fresh snapshot. The header and page form both expose a `searchbox` named “Search packages”; fill the first listed searchbox by its fresh ref with `$CR browser fill @e21 verification-probe` (use the ref shown in the current snapshot, not this example's number), then capture the typed action.
- Submit with `$CR browser press Enter`.
- Wait for `/?q=verification-probe` and capture the resulting snapshot and screenshot. Confirm the search term is visible and that results or the empty state match the fixture.
- Independently query `$CR cli -- curl -fsS 'http://127.0.0.1:18098/v1/search?q=verification-probe'`. Save stdout and exit status; compare returned package names with the visible catalog rows.

## Gotchas

- An empty default lane proves empty-state and query behavior only. It does not prove result ranking, package detail links, or kind filtering with rows.
- The catalog is server rendered; page navigation and query parameters are the resulting state, not a client-only filter toggle.

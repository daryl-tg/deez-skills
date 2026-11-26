# Package details

The package page shows the public listing, available versions, and package content to visitors; access-controlled packages stay hidden from anonymous visitors.

## Sub-features

- Open a public package from a catalog result.
- Read its overview and version information.
- Follow the package's public install or download link.
- Confirm an unentitled private package does not become visible anonymously.

## How to get to it (user POV)

- Select a package name from the home catalog or search results.
- Open a known public package URL `/@scope/name`.

## Driving it with control-registry

Preconditions:

- A disposable lane contains one real published, public package named `@scope/name`; record its exact URL before driving.
- `$CR doctor` passes for that lane.

- Open the catalog and search for the fixture through the visible “Search packages” field. Capture the search action and resulting row.
- Activate the package link by its accessible name. Capture the overview, then open the visible version or contents section and capture the result.
- Read `GET /v1/packages/scope/name` through `$CR cli -- curl -fsS http://127.0.0.1:18098/v1/packages/scope/name` and compare its latest version with the page.
- Confirm the package's visible links and access behavior match the fixture's visibility. Do not use hidden internal store operations to prepare a row.

## Gotchas

- The default memory lane has no published package. Mark this recipe blocked by its fixture precondition when no disposable published fixture exists.
- Never put a private package identifier in anonymous evidence unless the observed response is the intended hidden/not-found behavior.

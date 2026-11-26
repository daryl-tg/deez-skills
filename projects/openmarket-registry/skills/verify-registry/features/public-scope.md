# Public scope page

A public scope page lists the search-visible packages belonging to one publisher and links visitors to each package page.

## Sub-features

- Open a publisher page at `/@scope`.
- Read its public package list.
- Follow a listed package to its detail page.
- Confirm private or deleted package rows are not exposed.

## How to get to it (user POV)

- Follow a publisher link from a package page.
- Open a known public publisher URL `/@scope` directly.

## Driving it with control-registry

Preconditions:

- A disposable lane has a public scope with at least one public package.
- `$CR doctor` passes for that lane.

- Open `http://127.0.0.1:18098/@scope` in the browser and capture the page identity and listed package rows.
- Activate a package link by its accessible name; capture the resulting package page and confirm the scope and package identity.
- Read `GET /v1/search?q=&limit=200` with the same scope fixture and compare its public rows with those on the scope page.

## Gotchas

- An empty in-memory lane can show an empty or not-found scope, but that does not prove the populated listing path.
- Use only public fixture rows for positive listing evidence.

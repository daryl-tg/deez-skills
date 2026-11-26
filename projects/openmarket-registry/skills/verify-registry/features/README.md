# OpenMarket Registry verification map

The maintained source for proving user visible registry behavior. Read this index before driving, then use the matching feature recipe.

## Baseline preconditions

- Start the app with `$CR up` (the hub wrapper, from inside the registry checkout) on its assigned port and loopback address.
- `$CR doctor` confirms the health route, port owner, and working checkout.
- The default lane is anonymous and in memory, with no seeded package rows.
- Never drive an instance this run did not start.

## Driving conventions

- Prefer accessible roles and names over CSS selectors or coordinates.
- Browser actions go through `$CR browser`; API commands go through `$CR cli --`.
- Recipes that need a package row name that precondition explicitly.
- Do not create fixture rows through internal setters or test-only endpoints.

## Proof and skip reporting

- Capture the user action and resulting state, not only the final screen.
- UI proof includes an accessibility snapshot and screenshot for each state.
- API proof includes the exact command, stdout, stderr, and exit code.
- Mutation proof includes a second, read-only view of the stored value.
- Publish with `$CR evidence publish <run-id> <revision>` when the existing review renderer is available. Never use the app port as a review URL.
- Report an unavailable fixture path with the attempted command and unmet precondition; do not count another entry point as proof.

## Features

- [Catalog and search](./catalog-search.md)
- [Package details](./package-details.md)
- [Public scope page](./public-scope.md)

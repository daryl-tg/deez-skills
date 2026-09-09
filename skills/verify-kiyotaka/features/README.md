# kiyotaka-frontend verification map

The maintained source for verifying user-facing chart behavior. Read this index
before driving, then use the matching feature file as the recipe.

## Baseline preconditions

- Launch the lane on its **assigned** port (`18097`–`18197`), bound to
  `127.0.0.1`: `./control-kiyotaka up`. Never pick a free port, never `8080`.
- `./control-kiyotaka doctor` exits zero. The `chart-schema` line must read `ok`.
- Viewport set to `1440 900` before any layout assertion.
- Candles present: `window.tc[0].metadata[0].rawData.length > 50`.
- Guest signup modal dismissed (`find role button click --name "Close"`) — it
  re-raises, so dismiss it immediately before each capture, never once up front.
- No stale dialog from an earlier step is on top:
  `eval "document.querySelectorAll('[role=dialog]').length"` reads what you expect.
- Never drive an instance this verification run did not start.

## Driving conventions

- Start every recipe from the baseline unless its preconditions say otherwise.
- Prefer ARIA roles and accessible names over CSS selectors or DOM position.
- Browser actions run through `control-kiyotaka browser`, terminal actions
  through `control-kiyotaka cli -- <command>`.
- Treat every command as literal. Keep quoted names and flags unchanged.
- Assert engine state (`window.tc`) for anything the a11y tree cannot see. The
  chart canvas is WebGL and carries no accessible structure.
- Restore seeded state after a mutation. Never remove proof artifacts.

## Lanes

Each entry names the lane it needs. **Guest** needs only the lane; **authed**
needs the operator's local stack (`:3000`, `:4001`) plus a login, and mutates a
real account's autosaving workspace — use a throwaway account.

## Proof and skip reporting

- Capture the user action and the resulting state, not only the final screen.
- Chart proof is a **triple**: the engine-state read, the accessible name, and a
  screenshot. The first is the side effect, the last is the only thing that
  proves pixels were drawn.
- CLI proof includes the command, stdout, stderr, and exit code.
- Frames and `evidence-manifest.json` go in `artifacts/<run-id>/<revision>/`;
  validate with `./control-kiyotaka evidence check <run-id> <revision>` and hand
  back that path. There is no publish step on this seat. Never hand back a lane
  URL.
- Report an unreachable path with the attempted command and the unmet
  precondition. Never report a skipped entry point as verified via another path.

## Feature entry contract

An H1 title, one paragraph of user-visible behavior, then exactly four H2s in
order: `Sub-features`, `How to get to it (user POV)`,
`Driving it with control-kiyotaka`, `Gotchas`.

Keep implementation detail out. Name only user paths, stable handles, required
state, commands, and observable proof.

## Features

- [Chart boot and the data plane](./chart-boot-and-data-plane.md) — guest
- [Indicators](./indicators.md) — guest (authed for the official catalog)
- [Symbol search and the ticker bar](./symbol-search-and-ticker-bar.md) — guest
- [Script editor and kScript](./script-editor-and-kscript.md) — guest (authed for protected/wrun)

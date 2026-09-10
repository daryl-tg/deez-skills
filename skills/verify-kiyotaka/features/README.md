# kiyotaka-frontend verification map

The maintained source for verifying user-facing chart behavior. Read this index
before driving, then use the matching feature file as the recipe.

## Baseline preconditions

- Launch the lane on its **assigned** port (`18097`–`18197`), bound to
  `127.0.0.1`: `./control-kiyotaka up`. Never pick a free port, never `8080`.
- `./control-kiyotaka doctor` exits zero. The `chart-schema` line must read `ok`.
- Viewport set to `1440 900` before any layout assertion.
- Candles present: `window.tc[0].metadata[0].rawData.length > 50`. Budget two
  minutes on a cold boot.
- Interval read, never assumed: `chartStore.activeInterval` (a guest with no
  stored state lands on `1h`).
- Guest signup modal dismissed (`find role button click --name "Close" --exact`)
  — dismiss it immediately before each capture, never once up front.
- Nothing on top:
  `eval "document.querySelectorAll('.q-dialog, .dialog-style, [role=dialog].open').length"`
  reads `0`. Do **not** count bare `[role=dialog]`: `MobilePopupSheet.vue` renders
  its markup unconditionally at every width (visibility is CSS, not `v-if`), so a
  clean desktop boot already reads `1`, and the guest signup modal carries no
  `role=dialog` at all. `.q-dialog` is what catches a Quasar dialog left open by
  an earlier step.
- Never drive an instance this verification run did not start.

## Driving conventions

- Start every recipe from the baseline unless its preconditions say otherwise.
- Prefer ARIA roles and accessible names over CSS selectors or DOM position.
  Where a control has no accessible name — layout grid cells, chart-type entries,
  drawing tools — fall back to `find testid <data-testid>`, which this app
  populates well, rather than concluding there is no handle.
- Never key on an accessible name that is really *content*. The symbol-search
  field's name is the current symbol; match its placeholder instead.
- Browser actions run through `control-kiyotaka browser`, terminal actions
  through `control-kiyotaka cli -- <command>`.
- Treat every command as literal. Keep quoted names and flags unchanged.
- `agent-browser`'s fill text is **positional**:
  `find <locator> <value> fill "<text>"`. There is no `--text` flag; passing one
  types the literal string `--TEXT <text>` into the field and the failure looks
  like a search that returned nothing.
- Check an exit code unpiped. `cmd | tail` reports `tail`'s status, which has
  produced both a false "the wrapper swallows failures" finding and a false
  `doctor` pass in this map's own history.
- Assert engine state (`window.tc`) for anything the a11y tree cannot see. The
  chart canvas is WebGL and carries no accessible structure.
- Restore seeded state after a mutation. Never remove proof artifacts.

## Lanes

Each entry names the lane it needs. **Guest** needs only the lane; **authed**
needs the operator's local stack (`:3000`, `:4001`) plus a login, and mutates a
real account's autosaving workspace — use a throwaway account.

A guest-lane surface can still stop at a sign-in wall partway through: the entry
point opens, the control responds, and the *commit* raises
`Sign in or create an account`. `src/constants/authFeatures.constants.ts` lists
every gated surface (`MULTI_CHART`, `WORKSPACE`, `ALERT`, `WATCHLIST`,
`FAVORITES`, `ONE_SECOND_INTERVAL`, `TAPE_MODE`, `LAYOUTS`, …) and
`promptGuestLogin` is what raises the wall. Read it before mapping something as
guest-reachable, and report the wall as the unmet precondition rather than
photographing a click that did nothing.

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
- [Indicators](./indicators.md) — guest (the official catalog needs a SEEDED
  stack, not a login: `/scripts/query` is unauthenticated, so the blocker is
  `node scripts/seed-official-catalog.mjs`, not the authed lane)
- [Symbol search and the ticker bar](./symbol-search-and-ticker-bar.md) — guest
- [Script editor and kScript](./script-editor-and-kscript.md) — guest (authed for protected/wrun)

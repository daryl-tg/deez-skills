# Script editor and kScript

The script editor is a drawer docked alongside the terminal, never a dockview
tab, where a user writes kScript, runs it, and sees the result mount as an
overlay through the frontend adapter. Public and own scripts can run client-side in the browser; protected and
marketplace (WRUN) scripts use the shared hosted-run path when their delivered
source or published build requires it and return through the same pipeline. Run targets depend on delivered source, visibility, and published
builds: editable and delivered read-only scripts can run in the browser, while
protected or unavailable builds use the cloud lane. This entry was last DRIVEN
on 2026-10-28 against product tree `29c9cda0a2` (`origin/main`), lane `18103`,
a guest lane with no JWT: ks-open through Super Search (`global-nav-search-btn`,
query `editor`, row `super-search-result-panels:Editor-btn`, label
`Script Editor`) gave a non-inert drawer reading `No script open`, with
`kscript-run-btn`, `kscript-close-editor-btn`, no `kscript-save-btn`, no
template picker, and one `.cm-editor` that ignored typing; the Panels `editor`
row raised the `script-editor` wall. Re-driven 2026-10-29 on `78ec9625d9`, same
lane and session, with the same result: the `editor` row opened one
`.cm-editor` with no wall, pressed `x` and `y` left it empty, and the Panels
`editor` row raised `script-editor`.
WRUN launch-box/ring, Pine conversion, Kata hand-offs, and AI provenance remain
authenticated coverage obligations.

## Sub-features

- `ks-open` the Editor panel opens (guest: **via Super Search only**).
- `ks-run` an own script compiles and mounts as an overlay (authed).
- `ks-lint` the editor reports a syntax error rather than mounting (authed).
- `ks-protected` a protected / WRUN script returns from the backend lane (authed).
- `ks-wrun-launch` the WRUN launch box/ring and Pine conversion hand-offs create
  the appropriate hosted or TypeScript draft, including retained conversion
  failures and the shared hosted-run path (authed, entitlement-dependent).

Guests can open the drawer read-only, but creating a new script requires an
account and raises the sign-in wall. Do not describe the guest Run button as a
silent no-op without first identifying the current tab and source-delivery state.

## How to get to it (user POV)

- Click the `</>` button in the ticker bar, or open Super Search (the
  `Ask anything ⌘K` capsule in the top navbar) and pick the `Script Editor` row.
- Close it with the drawer's own close button. `Escape` does not close it.
- In an authenticated WRUN-capable lane, use the launch box/ring or Pine paste
  conversion affordance before asserting a hosted run or TypeScript draft. Pine
  conversion accepts up to 256 KB and can retain a failed conversion for review;
  inspect run output for Browser/Cloud origin and AI/Kata/Pine provenance.

## Driving it with control-kiyotaka

Preconditions:

- Baseline from [chart boot](./chart-boot-and-data-plane.md), guest modal dismissed.

- **Open the panel — and on the guest lane the ticker-bar toggle will NOT do it.**
  `TBEditorToggle` calls `handleGuestAccess(FeatureId.SCRIPT_EDITOR)` before
  toggling, so a guest click raises the sign-in wall and the drawer stays `inert`.
  Driven live, the click left `dialogStore.isAuthenticationDialogOpen = true` and
  `guestLoginFeatureId = "script-editor"` with `.cm-editor` still `0`. Use it only
  to prove the wall — and note it leaves that dialog covering the chart, which
  blocks every later click until you clear it with `Escape` (see the chart-boot
  gotcha; a lane reload works too but costs a full re-boot):

  ```bash
  ./control-kiyotaka browser find testid tb-editor-toggle-btn click
  ./control-kiyotaka browser eval "(()=>{const d=document.querySelector('#tc-container-0').__vueParentComponent.setupState.dialogStore;return JSON.stringify({auth:d.isAuthenticationDialogOpen,feature:d.guestLoginFeatureId})})()"
  ```

  **Super Search is the ungated route, and it opens from the top navbar.**
  `tb-super-search-btn` was deleted with `TBSuperSearchButton.vue`; the door is
  now `global-nav-search-btn` (`Ask anything ⌘K`), proven live 2026-10-27 with
  `super-search-overlay` mounted and `isAuthenticationDialogOpen` false. The
  ticker bar's `tb-super-search-full-btn` exists only in full-chart mode. **The row's label oscillates the
  same way** (`superSearch.panels.editor` has been `Script Editor` and `Indicator Editor`
  within two weeks), so match either rather than pinning one: fill the query,
  then click whichever of the two the overlay actually rendered.

  ```bash
  ./control-kiyotaka browser find testid global-nav-search-btn click
  ./control-kiyotaka browser find testid super-search-input fill "editor"
  # read the row's current wording rather than guessing which spelling shipped
  ./control-kiyotaka browser eval "(()=>{const o=document.querySelector('[data-testid=super-search-overlay]');return (o.innerText.match(/[A-Za-z ]*Editor/)||[''])[0].trim()})()"
  ./control-kiyotaka browser find text "<that string>" click
  ```

  **Drive the input by its testid, and give the overlay time.** The overlay
  mounts lazily: for the first seconds `isSuperSearchOpen` is already `true`
  while the overlay is absent from the DOM entirely — no `super-search-overlay`,
  no input, so `find placeholder "Search the platform"` fails and an inputs
  census does not list it. That reads as a dead button. It is not; poll for
  `[data-testid=super-search-overlay]` before typing. Once mounted the input does
  carry the `Search the platform` placeholder, but `super-search-input` is the
  handle that does not depend on the timing. The overlay also carries
  `super-search-bubble-{indicators,tools,settings,shortcuts}-btn`.

  The `Indicator Editor` row needs a query — but Super Search is not empty before one:
  it opens on suggested "who to follow" rows, so rows on screen are not proof your
  query landed. Match the row you want, never the row count. Give the overlay a
  beat, too: right after `isSuperSearchOpen = true` the input exists and is
  visible while `find placeholder` still misses it, and the same call succeeds a
  few seconds later. There is no keyboard route:
  `keyboardShortcuts.constants.ts` registers no editor action, so do not look for a
  `chartShortcuts` binding.
- **Confirm it opened with `inert`, not with a name or a chunk.** `EditorDrawer`
  renders on every desktop boot and is `inert` while closed, so a
  `role=complementary` region named `Editor` is present from first paint and
  proves nothing. The open/closed bit is the attribute:

  **Do not key the probe on the drawer's exact name — it oscillates.** The label
  is `navbar.tickerBarEditor.openEditor`, which has been `Editor`, then
  `Indicator Editor`, then `Editor` again inside two weeks; an equality check
  matches nothing and returns `undefined` for `inert`, which reads as the drawer
  never rendering. Match the substring instead, which survives both spellings.
  The drawer carries no testid of its own (`DockDrawer.vue` renders
  `role="complementary"` with a bound `aria-label` and class `dock-drawer`), so
  this regex is the stable handle. The desktop boot carries five complementary
  drawers — the editor plus `Objects`, `Journal`, `News`, `Trade`:

  ```bash
  ./control-kiyotaka browser eval "(()=>{const a=[...document.querySelectorAll('[role=complementary]')].find(e=>/Editor/.test(e.getAttribute('aria-label')||''));return JSON.stringify({label:a?.getAttribute('aria-label'),exists:!!a,inert:a?.hasAttribute('inert')})})()"
  ```

  A closed drawer reads `{exists:true, inert:true}` with empty text — that is the
  resting state, **not** a failed chunk and not a backend problem.
  **Open reads `inert:false` at once, and then the drawer is EMPTY for about 25
  seconds.** `inert` flips within a second of the Super Search click while
  `innerText.length` stays `0`, `children` sits at `2` and `kscript-run-btn` does
  not exist; the content appears around t+25s and settles by t+30s. Nothing marks
  the gap — no chunk error, no spinner — so a verifier who budgets ten or fifteen
  seconds reads an open-but-blank drawer and reports the editor as broken.
  `[data-testid=editor-workspace-skeleton]` is the marker for that state: while it
  is present the workspace chunk has not resolved, and `EditorDrawer` gates
  `KScriptWorkspace` on both its own (very large) chunk import and
  `awaitDeferredLocaleGate()`. One pass measured ~25s; a later pass on a newer
  tree still had the skeleton up past 105s with no console error, so treat the
  wait as unbounded on a dev lane and assert on the skeleton clearing rather than
  on a deadline.
  **Do not wait on `.cm-editor` as the open-proof.** A guest has no writable
  buffer, but CodeMirror still mounts read-only: driven 2026-10-27, a guest drawer
  read `.cm-editor` `1` once the skeleton cleared (earlier passes read `0`).
  Assert `inert`, the skeleton clearing and `kscript-run-btn` instead.
- **Close the drawer with `kscript-close-editor-btn`.** `Escape` leaves it open,
  and while it is open with focus in CodeMirror, app shortcuts such as `Meta+/`
  go to the editor instead of the app. Blur first (`document.activeElement.blur()`)
  before pressing an app shortcut.
- **The template picker is authed-only — a guest never sees it.** It renders behind
  `canWriteKScript`, which is `useJwtStore().isLoggedIn`, and that getter excludes
  `ROLES.GUEST` by construction. On the guest lane
  `[data-testid=kscript-template-picker]` is absent, CodeMirror mounts read-only,
  and the editor column reads `No script open`. Authed, a blank tab opens on the
  picker (`role=region` named `Start with a template`): take `Blank script`
  (`kscript-template-blank-btn`) or a card (`kscript-template-<id>`).
  Do not poll `.cm-editor` as the open-proof on either lane — see `inert` above.
- **Run is the driving action, and it has a handle.** Nothing mounts until you
  click it: `find testid kscript-run-btn click`, accessible name `Run` (or
  `Backtest` on a strategy tab). **Save and publish do not render without an
  account** (`canEditActiveScript`), so a guest finds no handle rather than a wall:
  live, a guest drawer had `kscript-run-btn` present and `kscript-save-btn` absent.
  Run itself is a no-op for a guest, because there is no tab to run.

  **Where a script runs is a user-settable chip, not a property of the script.**
  `effectiveRunTarget` defaults to Browser for open code and Cloud for protected or
  private code, but the user can flip it
  (`kscript-run-target-frontend-btn` / `kscript-run-target-backend-btn`);
  `runTargetLocked` is `isStrategyScript && !isTypeScriptTab`, so only a
  non-TypeScript strategy is locked. Read the chip before deciding which log to
  chase.
- **Only strategies are run-target locked now.** A TypeScript Indicator tab
  defaults to Browser but can pick Cloud, so `runTargetLocked` is true for
  strategies alone — do not report a TypeScript tab offering Cloud as a bug.
- **The WRUN/Indicator lane gate was DELETED, not merely flipped.**
  `isWrunRegistrySectionEnabled()` no longer exists; the lane is unconditional and
  ignores `kiyo.flag-overrides`. So the blank template is always
  `kscript-template-blank-btn`, `kscript-template-blank-legacy-btn` is gone from
  source entirely, and "TypeScript is primary" is simply how the editor works.
  The picker region is now titled `New indicator`, not `Start with a template`.
  `script-explorer-new-legacy-btn` still exists in markup but can never render:
  `isKscriptAuthoringFrozen()` is hard-coded true, so kScript authoring is frozen
  for everyone and frozen tabs show `kscript-frozen-bar` (with `-copy` and
  `-port`).
- **kScript retires on 2026-11-02 (source, `c246ec3c43`, read on
  `849fb08e95`).** `KSCRIPT_RETIRED_AT_ISO` is `2026-11-02T00:00:00.000Z`
  (`src/constants/kscript-retired-at.constants.ts`; rigs override it with
  `VITE_KSCRIPT_RETIRED_AT`). The flag `kscript-sunset` is on for everyone
  while unminted; a minted `enabled:false` is the kill. Before the date the
  frozen bar reads `kScript is read-only and retires on {date}. Indicators are
  now written in TypeScript.`; from the date it reads `kScript is retired. This
  code is read-only. Indicators are now written in TypeScript.`; under the kill
  it falls back to the old wrun sentence. Its Port button reads `Port to
  Indicator`. A kScript row on the chart gets a legend chip (`Retires in {n}
  days`, `Retires tomorrow`, `Retired`), a once-per-chart-per-session toast
  `kscript-sunset-notice` (`-show-btn`, `-dismiss-btn`, `-remove-all-btn`,
  `-keep-btn`) and a legend card `legend-diagnostic-card-sunset`
  (`-sunset-line`, `-sunset-learn-more`). A guest has no kScript rows, so none
  of it is guest-reachable; it needs a signed-in session with a saved kScript
  row. The ledger is the product repo's `docs/features/indicators/kscript-retirement.md`.
  Not driven.
- **A run-target menu sits in the toolbar for a writer (source).**
  `kscript-run-target-menu-btn` with `-backend-btn`, `-frontend-btn` and
  `-backend-hint` renders only when the user can write kScript and a non-library
  tab is open, so it is signed-in only.
- **A no-JWT lane raises a VERIFY prompt, not the sign-in wall.**
  `handleGuestAccess` gates on `isGuest() || !isEmailVerified()`, and on a lane
  with no `jwtMetadata` the second term fires: `isAuthenticationDialogOpen` stays
  false and `guestLoginFeatureId` is never set. Asserting either after clicking
  `tb-editor-toggle-btn` will fail even though the drawer correctly stays inert —
  check the verify prompt instead. Kata's activity-bar entry is also VISIBLE on a
  no-JWT lane (it hides only for a real guest) while still being walled.
- **The drawer no longer goes blank for ~25s — confirmed live.** Driven: the
  skeleton was present 4s after the click and gone by 12s with `kscript-run-btn`
  rendered, and the drawer's `aria-label` read `Editor` while the Super Search row
  read `Script Editor` — both matched by the substring probe, which is why it is
  written that way. `EditorDrawer` uses
  `lazyWithRetry` with `EditorWorkspaceSkeleton` as the loading component, so
  `editor-workspace-skeleton` paints from the first frame of an open, and a failed
  chunk shows an inline "Couldn't load this." with Try again rather than a
  skeleton that never clears. The old "empty with nothing marking the gap"
  gotcha is obsolete. The workspace chunk still loads on open or button intent,
  so a first open is slower than a warm one.
- **Kata is a second wall inside the drawer.** The activity bar carries a Kata
  entry for non-guests whose click runs `handleGuestAccess(FeatureId.KATA)` — a
  different feature id from `SCRIPT_EDITOR`, so an authed-but-ungranted account
  can open the editor and still be walled here. It is desktop-only and
  signed-in-only, and it is also toggleable from Super Search.
- **Mount a script.** A kScript indicator is registry key `TECHNICAL_SCRIPT` with
  `ovType` in params, so a mounted script asserts exactly like an indicator:
  `./control-kiyotaka browser eval "(()=>JSON.stringify(window.tc[0].metadata.map(m=>m.settings?.ovType ?? m.type)))()"`.
- **Syntax-check a file without the UI**, when the claim is only that a source
  compiles: `curl -s -o /dev/null -w '%{http_code}' "$(./control-kiyotaka url)src/<path>"`.
  `200` compiled, `500` compile error. The `/chart/` base prefix is required.
- **Grammar and lint gates** are terminal work:
  `./control-kiyotaka cli -- pnpm run test:kscript-grammar` and
  `./control-kiyotaka cli -- pnpm run test:kscript-editor`.
- **Proof.** The editor frame, the engine read naming the mounted `ovType`, and a
  screenshot of the drawn overlay. For a lint claim, capture the error surface in
  the editor, not the console.

## Gotchas

- **Public and own scripts fail in the browser; protected ones fail on the
  server.** A client-side script error is in `./control-kiyotaka browser console`;
  a protected script that "loads forever" needs its `clientRequestId` from the
  in-app debug dump, grepped in the kscript-backend logs. Looking in the wrong
  place is the standard way this costs an hour.
- **A guest's read-only editor still reads `contenteditable="true"`.** Driven
  2026-10-28: `.cm-content` carried `contenteditable="true"`, yet focusing it and
  pressing `x` and `y` left the document empty with no wall. The read-only state
  is CodeMirror's, not the attribute, so prove it by typing and reading the text.
  **Read the text after a beat, not straight after the input.** Driven
  2026-10-29: `document.execCommand('insertText', false, 'ZZZ')` on the focused
  `.cm-content`, read in the same eval, showed `ZZZ` in the DOM; a read one
  second later showed the document empty again, because CodeMirror reverts the
  DOM edit it refuses. A same-tick read reports a guest edit that never
  happened.
- **OPRA data in user scripts is no longer flag-gated (source, `61f23cdf65`).**
  The `opra-user-scripts` flag is retired:
  `packages/wrun-chart-host/src/utility/chart/opra-user-scripts-gate.util.ts`
  answers on in every context, so what still gates a user script on an OPRA chart
  is a signed-in session and the OPRA entitlement and tier. Stale comments still
  name the flag (`KScriptWorkspace.vue`, `useIndicatorCatalogV2.ts`). Not driven.
- **The kScript stand-in paints on more charts (source, `f047751c9a`).** Stock,
  forex, commodity, DEX, index and CME charts now get the stand-in candles
  (`kscript-standin-chart.util.ts`). Not driven.
- Protected and WRUN scripts need the authed lane and a real entitlement. On the
  guest lane they are unreachable — report that with the attempted path.
- **`Engine analysis worker is paused; safe editing remains available.` is a lint
  fallback, not a guest state.** It is the `.catch()` of the analysis service,
  surfaced as a line-1 warning diagnostic; its gate carries no guest term. Do not
  read it as the bug you are chasing, and do not treat its absence as proof the
  lane is authed.
- **`New indicator` does not open an empty kScript buffer.** It is guest-walled,
  and when it does run it opens a prefilled **TypeScript Indicator** starter.
  TypeScript is now the primary language. The old notice `kScript is the legacy
  indicator language. New indicators are written in TypeScript.` and the
  `New kScript (legacy)` label are gone from source (removed by `09b0189a9b`;
  absent on `849fb08e95`): the sidebar string is `New kScript`, and the
  dismissible `kscript-legacy-notice` reads `New indicators are written in
  wrun.`. A guest drawer reads `No script open`, so neither may show there; read
  the drawer's text before asserting wording. A recipe that assumes kScript is
  the only language is describing the old editor.
- kScript output reaches the engine **only** through the frontend adapter. If an
  overlay mounts with the wrong shape, the claim belongs to the adapter contract,
  not the editor.
- The editor grammar is subordinate to the engine. A syntax behavior that
  disagrees with the engine is an editor bug, so never "fix" it by asserting the
  editor's version in a proof.

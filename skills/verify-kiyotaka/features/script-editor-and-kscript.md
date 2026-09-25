# Script editor and kScript

The script editor is a drawer docked alongside the terminal, never a dockview
tab, where a user writes kScript, runs it, and sees the result mount as an
overlay through the frontend adapter. Public and own scripts run client-side in the browser; protected and
marketplace (WRUN) scripts execute server-side and ride the same canonical
pipeline back.

## Sub-features

- `ks-open` the Editor panel opens (guest: **via Super Search only**).
- `ks-run` an own script compiles and mounts as an overlay (authed).
- `ks-lint` the editor reports a syntax error rather than mounting (authed).
- `ks-protected` a protected / WRUN script returns from the backend lane (authed).

`ks-run` and `ks-lint` share one unmet precondition on the guest lane:
`useJwtStore().isLoggedIn` is false, so there is no template picker, no writable
buffer and no tab — Run is a silent no-op. Do not photograph it.

## How to get to it (user POV)

- Click the `</>` button in the ticker bar, or open Super Search (its own
  ticker-bar button) and pick the `Indicator Editor` row.

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

  **Super Search is the ungated route, and the ticker bar now has a button for
  it.** `tb-super-search-btn` opens it with no guest gate — proven live,
  `isSuperSearchOpen` true with `isAuthenticationDialogOpen` false — which is
  simpler than setting the store flag by hand. **The row reads `Indicator
  Editor`, not `Script Editor`**; nothing renders the old string, so a recipe
  matching it finds nothing.

  ```bash
  ./control-kiyotaka browser find testid tb-super-search-btn click
  ./control-kiyotaka browser find testid super-search-input fill "editor"
  ./control-kiyotaka browser find text "Indicator Editor" click
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

  **The drawer's accessible name is now `Indicator Editor`, not `Editor`.** A
  probe keyed on `'Editor'` matches nothing and returns `undefined` for `inert`,
  which reads as the drawer never rendering. The desktop boot now carries five
  complementary drawers — `Indicator Editor`, `Objects`, `Journal`, `News`,
  `Trade`:

  ```bash
  ./control-kiyotaka browser eval "(()=>{const a=[...document.querySelectorAll('[role=complementary]')].find(e=>e.getAttribute('aria-label')==='Indicator Editor');return JSON.stringify({exists:!!a,inert:a?.hasAttribute('inert')})})()"
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
  **Do not wait on `.cm-editor` at all on the guest lane: it stays `0` forever**,
  because a guest has no writable buffer to mount. It is not a timing signal and
  not a failure.
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
  strategies are Cloud-locked and TypeScript Indicators Browser-locked. Read the
  chip before deciding which log to chase.
- **Only strategies are run-target locked now.** A TypeScript Indicator tab
  defaults to Browser but can pick Cloud, so `runTargetLocked` is true for
  strategies alone — do not report a TypeScript tab offering Cloud as a bug.
- **The blank template is TypeScript.** `kscript-template-blank-btn` now reads
  `Blank indicator`; the legacy kScript blank is a separate
  `kscript-template-blank-legacy-btn` ("Blank kScript (legacy)").
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
- Protected and WRUN scripts need the authed lane and a real entitlement. On the
  guest lane they are unreachable — report that with the attempted path.
- **`Engine analysis worker is paused; safe editing remains available.` is a lint
  fallback, not a guest state.** It is the `.catch()` of the analysis service,
  surfaced as a line-1 warning diagnostic; its gate carries no guest term. Do not
  read it as the bug you are chasing, and do not treat its absence as proof the
  lane is authed.
- **`New indicator` does not open an empty kScript buffer.** It is guest-walled,
  and when it does run it opens a prefilled **TypeScript Indicator** starter.
  TypeScript is now the primary language — a guest drawer reads `kScript is the
  legacy indicator language. New indicators are written in TypeScript.` and the
  sidebar offers `New kScript (legacy)` beside it. A recipe that assumes kScript is
  the only language is describing the old editor.
- kScript output reaches the engine **only** through the frontend adapter. If an
  overlay mounts with the wrong shape, the claim belongs to the adapter contract,
  not the editor.
- The editor grammar is subordinate to the engine. A syntax behavior that
  disagrees with the engine is an editor bug, so never "fix" it by asserting the
  editor's version in a proof.

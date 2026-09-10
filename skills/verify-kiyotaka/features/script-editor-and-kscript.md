# Script editor and kScript

The script editor is a drawer docked alongside the terminal, never a dockview
tab, where a user writes kScript, runs it, and sees the result mount as an
overlay through the frontend adapter. Public and own scripts run client-side in the browser; protected and
marketplace (WRUN) scripts execute server-side and ride the same canonical
pipeline back.

## Sub-features

- `ks-open` the Editor panel opens.
- `ks-run` an own script compiles and mounts as an overlay.
- `ks-lint` the editor reports a syntax error rather than mounting.
- `ks-protected` a protected / WRUN script returns from the backend lane (authed).

## How to get to it (user POV)

- Click the `</>` button in the ticker bar, or open Super Search and pick the
  `Script Editor` row.

## Driving it with control-kiyotaka

Preconditions:

- Baseline from [chart boot](./chart-boot-and-data-plane.md), guest modal dismissed.

- **Open the panel.** The keybinding is user-configurable (`chartShortcuts`), so it
  is not a stable handle. The ticker-bar toggle is, and it is one call:

  ```bash
  ./control-kiyotaka browser find testid tb-editor-toggle-btn click
  ```

  The Super Search route is a *different* entry point, so say which you drove:

  ```bash
  ./control-kiyotaka browser eval "document.querySelector('#tc-container-0').__vueParentComponent.setupState.dialogStore.isSuperSearchOpen = true"
  ./control-kiyotaka browser find placeholder "Search the platform" fill "editor"
  ```

  Super Search lists **nothing** until it has a query — opening it and
  snapshotting shows only `textbox "Search the platform"`. Once typed, the row's
  accessible name is `Script Editor`, not `Editor`.
- **Confirm it opened, by polling.** The panel is a lazy chunk: for several
  seconds it renders skeleton placeholders while the a11y tree shows none of its
  controls, so an immediate snapshot reads as "it did not open". Poll for
  CodeMirror, then snapshot and screenshot:

  ```bash
  ./control-kiyotaka browser eval "document.querySelectorAll('.cm-editor').length"
  ```

  A mounted drawer is a `role=complementary` region named `Editor`, carrying
  `New indicator`, `Templates`, `New kScript (legacy)`, `Manage groups`, a
  `CONSOLE` / `RESOURCES` pair and a `textbox "kScript console input"`.
- **A blank tab opens on the template picker, not on an empty buffer.** It is a
  `role=region` named `Start with a template` (`kscript-template-picker`). Take
  `Blank script` (`kscript-template-blank-btn`) for an empty editor, or a card
  (`kscript-template-<id>`) to prefill working source. Skipping this is why an
  editor can look mounted but empty with no obvious way forward.
- **Run is the driving action, and it has a handle.** Nothing mounts until you
  click it: `find testid kscript-run-btn click`, accessible name `Run` (or
  `Backtest` on a strategy tab). Save and publish are `kscript-save-btn` and
  `kscript-publish-btn`; publish hits the guest write-gate.
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
- **A guest editor opens with its analysis worker parked.** The console reads
  `Engine analysis worker is paused; safe editing remains available.`, and
  `New indicator` opens an empty buffer with no scripts of its own (`No scripts
  yet.`). The panel is genuinely usable for `ks-open`, but do not read that
  console line as the bug you are chasing.
- kScript output reaches the engine **only** through the frontend adapter. If an
  overlay mounts with the wrong shape, the claim belongs to the adapter contract,
  not the editor.
- The editor grammar is subordinate to the engine. A syntax behavior that
  disagrees with the engine is an editor bug, so never "fix" it by asserting the
  editor's version in a proof.

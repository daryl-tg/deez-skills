# Script editor and kScript

The script editor is a dockview panel (the `Editor` tab) where a user writes
kScript, runs it, and sees the result mount as an overlay through the frontend
adapter. Public and own scripts run client-side in the browser; protected and
marketplace (WRUN) scripts execute server-side and ride the same canonical
pipeline back.

## Sub-features

- `ks-open` the Editor panel opens.
- `ks-run` an own script compiles and mounts as an overlay.
- `ks-lint` the editor reports a syntax error rather than mounting.
- `ks-protected` a protected / WRUN script returns from the backend lane (authed).

## How to get to it (user POV)

- Open Super Search and pick the `Editor` panel, or open it from the terminal
  tab bar in the outer dock.

## Driving it with control-kiyotaka

Preconditions:

- Baseline from [chart boot](./chart-boot-and-data-plane.md), guest modal dismissed.

- **Open the panel.** The keybinding is user-configurable (`chartShortcuts`), so it
  is not a stable handle. Drive the store instead:
  `./control-kiyotaka browser eval "document.querySelector('#tc-container-0').__vueParentComponent.setupState.dialogStore.isSuperSearchOpen = true"`,
  snapshot, and pick the `Editor` row by accessible name. The panel itself is
  `useOuterDockviewStore().toggle('Editor')` if you need it without Super Search —
  say which path you drove, because they are different entry points.
- **Confirm it opened.** Snapshot and assert the editor's own region is present,
  then screenshot. The panel is real DOM (CodeMirror), so it does snapshot.
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
- kScript output reaches the engine **only** through the frontend adapter. If an
  overlay mounts with the wrong shape, the claim belongs to the adapter contract,
  not the editor.
- The editor grammar is subordinate to the engine. A syntax behavior that
  disagrees with the engine is an editor bug, so never "fix" it by asserting the
  editor's version in a proof.

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

- Click the `</>` button in the ticker bar, or open Super Search and pick the
  `Script Editor` row.

## Driving it with control-kiyotaka

Preconditions:

- Baseline from [chart boot](./chart-boot-and-data-plane.md), guest modal dismissed.

- **Open the panel — and on the guest lane the ticker-bar toggle will NOT do it.**
  `TBEditorToggle` calls `handleGuestAccess(FeatureId.SCRIPT_EDITOR)` before
  toggling, so a guest click raises the sign-in wall and the drawer stays `inert`.
  Driven live, the click left `dialogStore.isAuthenticationDialogOpen = true` and
  `guestLoginFeatureId = "script-editor"` with `.cm-editor` still `0`. Use it only
  to prove the wall — and note it leaves that dialog covering the chart, which
  blocks every later click until you reload the lane:

  ```bash
  ./control-kiyotaka browser find testid tb-editor-toggle-btn click
  ./control-kiyotaka browser eval "(()=>{const d=document.querySelector('#tc-container-0').__vueParentComponent.setupState.dialogStore;return JSON.stringify({auth:d.isAuthenticationDialogOpen,feature:d.guestLoginFeatureId})})()"
  ```

  **Super Search is the ungated route, and the only way a guest opens the editor.**
  Its row snapshots as a `generic`, not an option or a button, so click it by ref
  from the snapshot rather than `find role option`:

  ```bash
  ./control-kiyotaka browser eval "document.querySelector('#tc-container-0').__vueParentComponent.setupState.dialogStore.isSuperSearchOpen = true"
  ./control-kiyotaka browser find placeholder "Search the platform" fill "editor"
  ./control-kiyotaka browser snapshot -i -c   # -> generic "Script Editor" [ref=eN]
  ./control-kiyotaka browser click "@eN"
  ```

  Super Search lists **nothing** until it has a query. There is no keyboard route:
  `keyboardShortcuts.constants.ts` registers no editor action, so do not look for a
  `chartShortcuts` binding.
- **Confirm it opened with `inert`, not with a name or a chunk.** `EditorDrawer`
  renders on every desktop boot and is `inert` while closed, so a
  `role=complementary` region named `Editor` is present from first paint and
  proves nothing. The open/closed bit is the attribute:

  ```bash
  ./control-kiyotaka browser eval "(()=>{const a=[...document.querySelectorAll('[role=complementary]')].find(e=>e.getAttribute('aria-label')==='Editor');return JSON.stringify({exists:!!a,inert:a?.hasAttribute('inert')})})()"
  ```

  A closed drawer reads `{exists:true, inert:true}` with empty text — that is the
  resting state, **not** a failed chunk and not a backend problem. Open reads
  `inert:false`, and CodeMirror follows a few seconds later (`.cm-editor` reached
  `1` about 12s after the drawer opened), so poll `inert` first and `.cm-editor`
  only after.
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

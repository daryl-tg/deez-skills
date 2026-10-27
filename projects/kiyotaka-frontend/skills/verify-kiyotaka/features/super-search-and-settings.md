# Super Search, settings pages and the guest wall

Super Search is the command palette a user opens from the `Ask anything ⌘K`
capsule in the top navbar. One query searches panels, commands, themes,
formulas and more, and a row runs its action. The Settings pages dialog holds
keyboard shortcuts, language and release notes, and a guest can open all three.
Every guest-walled control raises the same sign-in dialog, and this entry is
where that shared wall is described. Created 2026-10-27 from a live drive on
product tree `7290d33d10` (53 behind `origin/main` `df3fdcb62e`), lane `18103`,
a real guest-JWT lane. Driven: the capsule, the `editor`, `dark` and `SPY / GLD`
queries, `Meta+/` to Keyboard Shortcuts, Release Notes, and the wall from the
camera button. Not driven: the `Mod+J` key, the account settings pages (they
need a signed-in session), Gray and Cream appearance (desktop shell only), and
the per-provider gates on the other providers.

## Sub-features

- `ss-open` the capsule opens Super Search with no guest gate.
- `ss-theme` a `dark` or `light` query toggles the theme.
- `ss-formula` a ratio query such as `SPY / GLD` plots a formula chart.
- `set-shortcuts` `Meta+/` opens Settings on the Keyboard Shortcuts page.
- `set-notes` the Release Notes page lists versions.
- `guest-wall` a walled control raises the sign-in dialog and names its feature.

The editor row is covered in [script editor](./script-editor-and-kscript.md)
`ks-open`.

## How to get to it (user POV)

- Click `Ask anything ⌘K` in the top navbar, then type.
- Press `⌘/` (`Meta+/`) for Keyboard Shortcuts; the same dialog's left nav has
  Language and Release Notes.
- Click any walled control as a guest (the camera, a multi-chart layout, the
  watchlist seat) to meet the sign-in dialog.

## Driving it with control-kiyotaka

Preconditions: baseline from [chart boot](./chart-boot-and-data-plane.md), with
the top overlay cleared. Read the wall's state with:

```bash
DS="document.querySelector('#tc-container-0').__vueParentComponent.setupState"
./control-kiyotaka browser eval "JSON.stringify({auth:$DS.dialogStore.isAuthenticationDialogOpen,f:$DS.dialogStore.guestLoginFeatureId})"
```

- **`ss-open`.** `find testid global-nav-search-btn click`, then poll for
  `[data-testid=super-search-overlay]` before typing. The input is
  `super-search-input`. The overlay also carries
  `super-search-bubble-{indicators,tools,settings,shortcuts}-btn`. Result rows
  are `super-search-result-<provider>` sections with buttons
  `super-search-result-<id>-btn`, under `super-search-section-toggle-<provider>-btn`
  headers.
- **`ss-theme`.** Fill `dark`. The `THEMES` section shows `Dark Mode` with an
  `on-off-toggle-btn`. Click it and read
  `document.body.className.match(/body--(light|dark)/)[0]`: driven, it went
  `body--light` to `body--dark` with no wall. Toggle it back afterwards.
- **`ss-formula`.** Fill `SPY / GLD`. The `FORMULA` section offers
  `super-search-result-formula:SPY/GLD-btn` (`Plot SPY ÷ GLD`). Driven, a click
  switched the chart to `NYSE SPY / GLD` with title `SPY / USD / GLD / USD` and
  252 bars, with no wall. Restore the symbol afterwards.
- **`set-shortcuts`.** Blur any focused editor first
  (`eval "document.activeElement.blur()"`), then `press Meta+Slash`. Proof:
  `settings-pages-body` and `keyboard-shortcuts-search-input`. A guest's nav is
  `settings-pages-nav-{shortcuts,language,notes}-btn`. Close with
  `settings-pages-close-btn`.
- **`set-notes`.** `find testid settings-pages-nav-notes-btn click`. Proof: the
  `release-notes-version-<ver>-btn` rows (81 on the driven tree, `4.49.0`
  newest).
- **`guest-wall`.** `find testid global-nav-screenshot-btn click` raised it with
  `guestLoginFeatureId = "screenshot"`. The form carries
  `login-signup-submit-btn`, `login-signup-use-password-btn`,
  `login-signup-passkey-btn`, `login-signup-google-btn`,
  `login-signup-twitter-btn`, `login-signup-forgot-password-btn` and
  `login-signup-tos-link`. Clear it with `press Escape`.

  Feature ids driven on 2026-10-27, by door:

  | Door | `guestLoginFeatureId` |
  |---|---|
  | `global-nav-screenshot-btn` | `screenshot` |
  | an official row's Add in the Indicators dialog | `indicators` |
  | `tb-layout-matrix-cell-1-1-btn` | `multi-chart` |
  | `tb-watchlist-toggle-btn` | `watchlist` |
  | `tb-news-toggle-btn` | `news` |
  | `tb-editor-toggle-btn` | `script-editor` |
  | `tb-options-btn` | `terminal` |
  | `tb-heatmap-toggle-btn` (turning the heatmap on) | `orderbook-heatmap` |
  | `alert-add-menu-price-btn` | `alert` |

- **Proof.** The store read, the overlay or page testid, and a screenshot.

## Gotchas

- **`guestLoginFeatureId` is not cleared when the wall closes.** It keeps the
  last id after `Escape`, so read `isAuthenticationDialogOpen` first. A stale id
  beside `auth:false` means nothing was walled.
- **The wall has no close button; `Escape` clears it.** It shares the
  `.dialog-style.dialog-overlay` shell with the signup modal, and
  `guest-signup-modal-close-btn` is absent on it.
- **The Settings dialog is a `.q-dialog`.** It stays open under a second
  `Escape` from some states, and it covers other controls. Close it with
  `settings-pages-close-btn` and re-count the overlays.
- **`Meta+/` goes to CodeMirror while the editor drawer has focus.** The first
  press on 2026-10-27 did nothing for that reason.
- **Light mode is open to guests.** An older inventory note said it raises
  `LIGHT_MODE`. Driven, dark and light toggled freely. Source gates only Gray and
  Cream (`canPickAppearanceModes`, desktop), and a guest choosing those raises
  `LIGHT_MODE`.
- **Super Search mounts lazily.** `isSuperSearchOpen` goes true before the
  overlay is in the DOM, so poll for `super-search-overlay`.

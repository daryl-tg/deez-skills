# Browser sign-in, checkout return and the download door

Since 0.1.6 the packaged app signs in through the system browser. The login dialog shows "Sign in with your browser"
(`login-signup-browser-btn`) when the bridge reports `browserSignIn`; the shell cancels the page's
`/api/v1/auth-v2/browser`, `/google` or `/twitter` navigation, opens the same route in the browser with a PKCE challenge
and `redirect_uri=openmarket://oauth/callback`, and covers the window with "Finish signing in in your browser" (Open the
Browser Again, Cancel; it expires after ten minutes). The browser lands on `/chart/desktop/return#to=<callback>`, which
opens the app; the shell exchanges the code at `/api/v1/auth-v2/native/exchange`. Since 0.1.7 a desktop buyer pays in
the browser: Stripe opens externally with a toast, then lands on `/chart/desktop/checkout-return`, which opens
`openmarket://checkout?kind=paid|cancelled|portal...`, and a paid return loads `payment-status` in the window. Passkeys
are never offered inside the shell. In an ordinary browser, super search offers "Download the OpenMarket desktop app"
(and the signed-in profile menu a `desktop-app` row), hidden in the shell and on phones. Last driven 2026-11-03 on tree
`1af9ebbe07` (`origin/main`) in Chromium on the dev lane, one page at a time with the tab re-fronted before each poll
(a first pass that opened three tabs at once on a cold lane drew "Startup is taking longer than expected ... [failed to
load external] main.ts" on two pages; see the [index](./README.md)): the return page (valid and invalid), the four checkout-return states, the signin page's redirect to
`/chart/auth?redirect=/desktop/signin`, the super-search command (`super-search-result-featureCommands:desktop-app-btn`,
"Download the OpenMarket desktop app", the only result for "desktop app"; the "Draw by holding" tip's overlay covered
`global-nav-search-btn` until its Got it was clicked, and the query went in through the input event) and the sign-in dialog with its
`login-signup-passkey-btn` "Use a passkey" row among `login-signup-submit-btn`, `-use-password-btn`, `-google-btn`,
`-twitter-btn`, `-forgot-password-btn` and `-tos-link`. The chart route reached the guest button in about ten seconds
with a priced title but only 2 bars of history (`76,852.9 ▲ BTC - USD`, 15 canvases, "Reconnecting..."), because the
lane's streaming host did not resolve; on 2026-11-02 it had live candles, and none of these proofs needs candles. On 2026-10-30 the route
never settled under machine load (see the [index](./README.md)). `AuthFormView.vue`, `ProfilePanel.vue`,
the four desktop pages did not change between `2646a76a83` and `1af9ebbe07`, and `ProfilePanel.vue` not since `6dd6aa43de`;
between `39b22dd2ec` and `1af9ebbe07` `featureCommands.ts` was reworked (`66a5bcb680`) with the `desktop-app`
command's id, aliases and gate unchanged, and `AuthFormView.vue` gained `usePendingTwoFA` (`5027d30d82`, an expired
2FA step restarts sign-in) with its rows unchanged; between
2026-10-31 and 2026-11-01 `AuthFormView.vue` changed (`10655335c4`, `e3e96bf360`: the field collapse clips with
`min-width: 0`, so the form no longer runs past the card; `.field-collapse-inner` read 342 px wide with `overflow:
clip` on 2026-11-02) and the dialog's rows were not touched; on 2026-10-31 `ProfilePanel.vue` changed (`6dd6aa43de`)
and its `desktop-app` row, behind `isDesktopDownloadEntryVisible()`, was not touched. The shell's production sign-in
screen with no passkey row was last captured 2026-10-28 on `5365748ef3`; from 2026-10-29 to 2026-11-03 the console
session was locked, so `capture` got no frame or was not attempted (see [launch](./shell-launch-and-window.md)). The
shell half of sign-in and checkout (the button, the waiting screen, the exchange, the `openmarket://oauth` and
`openmarket://checkout` handling) has no live driver: it needs a packaged non-dev build or
`OPENMARKET_DESKTOP_BROWSER_SIGNIN=1`, a real orange and, for checkout, a Stripe session.
`desktop/tests/main/browser-signin.test.ts` and `checkout-return.test.ts` cover it.

## Sub-features

- `signin-button` the login dialog's "Sign in with your browser" in the shell. Live verification pending.
- `signin-waiting` the title-bar screen "Finish signing in in your browser" and its expiry. Live verification pending.
- `signin-exchange` the `openmarket://oauth/callback` exchange and its landing: signed in, two-factor, or
  `auth/login?error=<provider>_auth_failed`. Live verification pending.
- `signin-return-page` `/desktop/return#to=<openmarket://oauth/callback...>` reads "Signed in. Open OpenMarket to
  finish" with `desktop-return-open` and wipes the hash; any other `#to` shows `desktop-return-invalid`.
- `signin-start-page` `/desktop/signin` reads "Sign in to the OpenMarket app" and "Checking your sign-in…" while it
  checks the account, then sends a signed-out visitor to `/auth?redirect=/desktop/signin`.
- `signin-no-passkey` the shell's sign-in screen has no Use a passkey row; Chromium's does.
- `checkout-return-page` `/desktop/checkout-return` reads "Payment received" (`?product=<p>&session_id=cs_...`),
  "Checkout cancelled" (`?product=<p>`) or "Billing updated" (`?flow=portal`) with `desktop-checkout-return-open`, wipes
  the query, and shows `desktop-checkout-return-invalid` with `desktop-checkout-return-chart` for anything else.
- `checkout-shell` the shell's `openmarket://checkout` handling, `desktop: checkout <kind>`, and a paid return landing on
  `payment-status`, cold start included. Live verification pending.
- `download-door` super search's `super-search-result-featureCommands:desktop-app-btn` "Download the OpenMarket desktop
  app" in a browser. The profile-menu row is signed-in only (a guest's profile button opens sign-in), and its absence in
  the shell is not yet driven.

## How to get to it (user POV)

- In the app, choose Guest Mode, then Sign in with your browser. Finish in the browser and accept "Open OpenMarket?".
- In the app, upgrade a plan. Pay in the browser; the page says "Payment received" and opens the app on its payment
  status.
- In a browser, press Cmd+K and type "desktop app".

## Driving it with control-kiyotaka-desktop

Preconditions:

- Baseline from the [index](./README.md): `lane up`, `doctor` exit `0`. The pages run in plain Chromium; no account.

- **Return and checkout pages.** For each URL, `control-kiyotaka-desktop browser --session <s> open about:blank`, then
  `open <url>`, then wait for `#skeleton-loader` to go (re-front with `browser --session <s> tab t1` between waits), then
  read every `[data-testid^=desktop-]` and `location.href`:
  - `http://127.0.0.1:<port>/chart/desktop/return#to=` plus `encodeURIComponent('openmarket://oauth/callback?code=x&state=y')`:
    `desktop-return-title`, `desktop-return-open`, and an href with no hash.
  - `.../desktop/return#to=https%3A%2F%2Fevil.example`: `desktop-return-invalid` "This sign-in link isn't valid."
  - `.../desktop/checkout-return?product=plus&session_id=cs_test_1`: "Payment received".
  - `.../desktop/checkout-return?product=plus`: "Checkout cancelled".
  - `.../desktop/checkout-return?flow=portal`: "Billing updated".
  - `.../desktop/checkout-return?kind=bogus`: `desktop-checkout-return-invalid` "This link is not valid".
  - `.../desktop/signin`: lands on `/chart/auth?redirect=/desktop/signin`, "Sign in or create an account". A read
    before the account check settles sees the page itself, with no `desktop-` testids, so read again before calling
    it a miss.
- **No passkey in the shell.** `control-kiyotaka-desktop capture <dir>/shell-login-prod.png --prod --path '?login=1'`
  shows no Use a passkey row; the same dialog in Chromium (`browser ... click '[data-testid="profile-guest-mode-btn"]'`)
  shows one.
- **Download door.** In Chromium, once the chart shows its guest button, click `global-nav-search-btn` (with
  candles the first-run "See what moves price." dialog appears a little later and covers the button; see Gotchas),
  then `browser ... fill '[data-testid="super-search-input"]' 'desktop app'`, wait about three seconds, and read
  `super-search-result-featureCommands:desktop-app-btn`. If `fill` answers "Element not found" while the input is in
  the DOM, set the value from `eval` instead: `Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,
  'value').set.call(i, 'desktop app'); i.dispatchEvent(new Event('input', { bubbles: true }))` on
  `i = document.querySelector('[data-testid=super-search-input]')`. Either way the row is the only result.
- **Proof.** One PNG per page plus the read testids and href; the two sign-in frames side by side.

## Gotchas

- The checkout-return page reads `flow`, `product` and `session_id`, not `kind`; `kind` exists only on the
  `openmarket://checkout` link the page builds. `?kind=portal` alone is invalid.
- `open` of the same route with only a new hash does not remount the page. Go through `about:blank` between URLs.
- agent-browser's headless tab drifts to `hidden`, and the boot splash waits on `requestAnimationFrame`, so a page read
  too early sees no testids and a splash frame. Re-front the tab and wait for `#skeleton-loader` to disappear. A DOM
  read can succeed while the frame still comes out blank: on 2026-10-31 two of seven page PNGs were a 3.7 KB white
  frame with every testid read correctly. Run `browser --session <s> tab 1` right before `screenshot`, not only between
  waits; the re-shot frames drew.
- The pages wipe their hash or query on mount, so read `location.href` after the wipe to prove it and keep the URL you
  opened in the run notes.
- `browser ... keyboard type 'desktop app'` after the search click left `super-search-input` empty on 2026-11-01, with
  the input focused, so the panel kept its default shortcuts and showed no `desktop-app` row. `fill` on the input's
  testid put the words in and the row came. On 2026-11-02 `fill` on the same testid answered "Element not found" right
  after the search click, while a DOM read found `super-search-input` present, visible and focused
  (`document.activeElement` was the `.ssv3-pill-input`); setting the value through the native setter and an `input`
  event (see Driving) listed the row at once. A missing row after `keyboard type` or `fill` is the driver, not the
  door: read the input's value and the DOM before calling it a miss.
- With candles on the lane, the first-run "See what moves price." dialog (`.dialog-overlay`,
  `guest-signup-modal-close-btn`) appears some seconds after the guest button and covers `global-nav-search-btn`:
  agent-browser's click answers "is covered by <div.dialog-style.dialog-overlay>". On 2026-11-02 a click right after
  the guest button appeared went through, a click after a minute hit the overlay, and one close click reported done
  while the overlay still intercepted 1.5 s later. Click the close button and poll until no `.dialog-overlay` remains
  before the search click. The same dialog is what stops the `links` lane (see [links](./links-menu-and-channel.md)).
- A page read that returns no `desktop-` testid with `#skeleton-loader` still present after a minute is a hidden tab,
  not the page: on 2026-11-01 the invalid return page and the expired sign request both read empty that way on the
  first pass, and read correctly after two polls when `tab 1` ran before every poll. Re-front before each read, not only
  before the screenshot.
- No lane signs in through the browser end to end. `open 'openmarket://oauth/callback?...'` with no pending sign-in only
  logs `desktop: sign-in return dropped, none-pending`.

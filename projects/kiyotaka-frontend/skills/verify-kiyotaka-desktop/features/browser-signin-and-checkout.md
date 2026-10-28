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
(and the signed-in profile menu a `desktop-app` row), hidden in the shell and on phones. Last driven 2026-10-28 on tree
`5365748ef3` (`origin/main`): the return, checkout-return and signin pages in Chromium on the dev lane, the super-search
command in Chromium, and the shell's production sign-in screen with no passkey row against Chromium's with one. The
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
- `signin-start-page` `/desktop/signin` sends a signed-out visitor to `/auth?redirect=/desktop/signin`.
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
  - `.../desktop/signin`: lands on `/chart/auth?redirect=/desktop/signin`, "Sign in or create an account".
- **No passkey in the shell.** `control-kiyotaka-desktop capture <dir>/shell-login-prod.png --prod --path '?login=1'`
  shows no Use a passkey row; the same dialog in Chromium (`browser ... click '[data-testid="profile-guest-mode-btn"]'`)
  shows one.
- **Download door.** In Chromium, click `global-nav-search-btn`, type `desktop app`, and read
  `super-search-result-featureCommands:desktop-app-btn`.
- **Proof.** One PNG per page plus the read testids and href; the two sign-in frames side by side.

## Gotchas

- The checkout-return page reads `flow`, `product` and `session_id`, not `kind`; `kind` exists only on the
  `openmarket://checkout` link the page builds. `?kind=portal` alone is invalid.
- `open` of the same route with only a new hash does not remount the page. Go through `about:blank` between URLs.
- agent-browser's headless tab drifts to `hidden`, and the boot splash waits on `requestAnimationFrame`, so a page read
  too early sees no testids and a splash frame. Re-front the tab and wait for `#skeleton-loader` to disappear.
- The pages wipe their hash or query on mount, so read `location.href` after the wipe to prove it and keep the URL you
  opened in the run notes.
- No lane signs in through the browser end to end. `open 'openmarket://oauth/callback?...'` with no pending sign-in only
  logs `desktop: sign-in return dropped, none-pending`.

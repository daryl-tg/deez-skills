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
(and the signed-in profile menu a `desktop-app` row), hidden in the shell and on phones. On 2026-11-07, on tree `dced88e06a`
(`origin/main`; none of the four desktop pages changed since `bf1c9bac3c`), the return page (valid and invalid), the four
checkout-return states, the signin redirect, the sign-in card and the super-search command read exactly as below in
Chromium on the dev lane (a ticking BTC title over 1 bar: the streaming host did not resolve, which these pages do not
need), each opened through `about:blank` (a hash-only change to the same route keeps the page already shown, so an
invalid `#to=` opened straight after a valid one still reads "Signed in"), one page at a time with the tab re-fronted
before each read: the return page (valid: `desktop-return-title`
"Signed in. Open OpenMarket to finish", `desktop-return-open`, href with no hash; invalid: `desktop-return-invalid`),
the four checkout-return states ("Payment received", "Checkout cancelled", "Billing updated", and
`desktop-checkout-return-invalid` with `desktop-checkout-return-chart`, each with the query wiped), the signin page's
redirect to `/chart/auth?redirect=/desktop/signin` ("Sign in or create an account"), and the super-search command
(`super-search-result-featureCommands:desktop-app-btn`, "Download the OpenMarket desktop app", the only result for
"desktop app", set through the input event; with no candles no overlay covered the search button). The sign-in card on
`/chart/auth` read `login-signup-submit-btn` "Email me a code", `-use-password-btn`, `-passkey-btn` "Passkey",
`-google-btn`, `-twitter-btn` "X" and `-tos-link`; `-forgot-password-btn` shows only in the password step. Since
`37afa417b0` (2026-11-04, after `8436920004`) the Turnstile widget sits under the address it vouches for
(`login-signup-turnstile`, between the email field and `login-signup-submit-btn`, read live in document order on
2026-11-05 and 2026-11-07), no longer at the foot of the card. While Cloudflare shows its checkbox and it is unticked
(`humanCheckPending`), "Email me a code" stays disabled and `login-signup-field-message` reads "Complete the security
check above to continue." Since `45a3754bef` (after `8bcd72f8f5`) the code step runs its own check,
`login-signup-code-turnstile`, under the step whenever its send has no token in hand: on a resend, and on the first
send when the address's check failed or had not answered when the entry's wait ran out. That check loads Cloudflare's
script again if it failed, and a checkbox Cloudflare asks for shows under the step and holds the send until ticked.
The reason a send went without a token (`script`, `render`, `challenge:<code>`, `timeout`, `unrendered`) goes only to
analytics (`signin:code-dialog`) and auth-service, never to the screen. The dev lane's test sitekey never asks: on
2026-11-07 the button was disabled with an empty address and turned on once an address was typed (not submitted). The
disabled state and the code step's own check are source-read only. `4b8f78a775` (2026-11-03, after `1af9ebbe07`) rebuilt `AuthFormView.vue` as one card: the providers
sit in one row of outlined pills under "Or continue with", a successful password, code, passkey or 2FA sign-in shows a
welcome screen (`login-signup-welcome`) and then reloads once behind index.html's sign-in handoff card
(`handOffSignIn`, `src/utility/auth/signin-handoff.util.ts`), and `ResendCountdown.vue` is new. The shell's browser
sign-in does not take that path: its PKCE exchange is in the main process (`desktop/src/main/index.ts`,
`browser-signin.ts`) and never calls `handOffSignIn`. The `DesktopBrowserSignIn` row (`login-signup-browser-btn`,
gated on the bridge's `browserSignIn`) and the passkey gate (`PasskeyService.isSupported()` is false under
`window.openmarketDesktop`) are unchanged. The four desktop pages, `featureCommands.ts`'s `desktop-app` command (id,
aliases, gate) and `ProfilePanel.vue`'s `desktop-app` row did not change between `1af9ebbe07` and `bf1c9bac3c`.
`2f56d17937` and `2ab15d9784` restyle the page's own sign-in leave (the welcome fade and the reload's handoff card),
which the shell's browser sign-in never takes. The
shell's production sign-in screen with no passkey row was last captured 2026-10-28 on `5365748ef3`, before the
one-card rebuild; from 2026-10-29 to 2026-11-07 the console session was locked, so `capture` got no frame or was not
attempted (see [launch](./shell-launch-and-window.md)). The
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
- `signin-no-passkey` the shell's sign-in screen has no Passkey pill; Chromium's does (`login-signup-passkey-btn`).
- `signin-human-check` the Turnstile widget (`login-signup-turnstile`) sits between the address and "Email me a code";
  an unticked Cloudflare checkbox keeps the button off with "Complete the security check above to continue." A code
  step whose send has no token (a resend, or an address check that failed or ran out of time) runs its own check,
  `login-signup-code-turnstile`, and holds the send while Cloudflare's checkbox shows. Placement live in Chromium on the
  dev lane; the disabled state and the code step's check need a sitekey that asks, so they are source-read only.
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
  shows no Passkey pill; the same dialog in Chromium (`browser ... click '[data-testid="profile-guest-mode-btn"]'`)
  shows one.
- **The card and its human check.** In Chromium on `/chart/auth` (the signin page lands there), read every
  `[data-testid^=login-signup]` with its text and `disabled`, then type an address and read again. The address field
  has no testid: it is `input[name=email]`, and the native-setter and `input`-event form below fills it. Prove the
  placement with `compareDocumentPosition`: the email input, then `login-signup-turnstile`, then
  `login-signup-submit-btn`. On the dev lane the submit is disabled while the address is empty and enabled once it is
  typed; a disabled submit with the field message "Complete the security check above to continue." needs a sitekey
  that asks for the checkbox.
- **Download door.** In Chromium, once the chart shows its guest button, close whatever overlay covers it (the
  "Draw by holding" tip's `ink-tutorial-close` or the guest signup prompt's `guest-signup-modal-close-btn`; see
  Gotchas) and poll until no `.dialog-overlay` remains, then click `global-nav-search-btn`,
  then `browser ... fill '[data-testid="super-search-input"]' 'desktop app'`, wait about three seconds, and read
  `super-search-result-featureCommands:desktop-app-btn`. If `fill` answers "Element not found" while the input is in
  the DOM, set the value from `eval` instead: `Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,
  'value').set.call(i, 'desktop app'); i.dispatchEvent(new Event('input', { bubbles: true }))` on
  `i = document.querySelector('[data-testid=super-search-input]')`, wrapped in an arrow function that runs at once:
  agent-browser's `eval` shares one global scope across calls, so a second top-level `const i` throws "Identifier 'i'
  has already been declared". Either way the row is the only result.
- **Proof.** One PNG per page plus the read testids and href; the two sign-in frames side by side.

## Gotchas

- The checkout-return page reads `flow`, `product` and `session_id`, not `kind`; `kind` exists only on the
  `openmarket://checkout` link the page builds. `?kind=portal` alone is invalid.
- `open` of the same route with only a new hash does not remount the page. Go through `about:blank` between URLs.
- agent-browser's headless tab drifts to `hidden`, and the boot splash waits on `requestAnimationFrame`, so a page read
  too early sees no testids and a splash frame. Re-front the tab and wait for `#skeleton-loader` to disappear. A DOM
  read can succeed while the frame still comes out blank: on 2026-10-31 two of seven page PNGs were a 3.7 KB white
  frame with every testid read correctly. Run `browser --session <s> tab t1` right before `screenshot`, not only between
  waits; the re-shot frames drew. agent-browser takes a tab id (`t1`); on 2026-11-04 `tab 1` answered "Expected a tab
  id like `t1`".
- The pages wipe their hash or query on mount, so read `location.href` after the wipe to prove it and keep the URL you
  opened in the run notes.
- `browser ... keyboard type 'desktop app'` after the search click left `super-search-input` empty on 2026-11-01, with
  the input focused, so the panel kept its default shortcuts and showed no `desktop-app` row. `fill` on the input's
  testid put the words in and the row came. On 2026-11-02 `fill` on the same testid answered "Element not found" right
  after the search click, while a DOM read found `super-search-input` present, visible and focused
  (`document.activeElement` was the `.ssv3-pill-input`); setting the value through the native setter and an `input`
  event (see Driving) listed the row at once. A missing row after `keyboard type` or `fill` is the driver, not the
  door: read the input's value and the DOM before calling it a miss.
- With candles on the lane, a fresh guest chart raises one of two overlays over `global-nav-search-btn`: the guest
  signup prompt ("See what moves price.", `.dialog-overlay`, `guest-signup-modal-close-btn`, `GuestSignupPromptDialog.vue`)
  or the "Draw by holding" tip (`ink-tutorial`, `ink-tutorial-close`). It is not the first-run onboarding, which never
  starts for a guest. agent-browser's click answers "is covered by <div.dialog-style.dialog-overlay>". On 2026-11-02 a
  click right after the guest button appeared went through, a click after a minute hit the overlay, and one close
  click reported done while the overlay still intercepted 1.5 s later. On 2026-11-04 the first load showed the prompt,
  and a reload in the same session showed the tip instead. Read which close testid the overlay holds, click it, and
  poll until no `.dialog-overlay` remains before the search click. The prompt is what stops the `links` lane (see
  [links](./links-menu-and-channel.md)).
- A page read that returns no `desktop-` testid with `#skeleton-loader` still present after a minute is a hidden tab,
  not the page: on 2026-11-01 the invalid return page and the expired sign request both read empty that way on the
  first pass, and read correctly after two polls when `tab t1` ran before every poll. Re-front before each read, not only
  before the screenshot.
- No lane signs in through the browser end to end. `open 'openmarket://oauth/callback?...'` with no pending sign-in only
  logs `desktop: sign-in return dropped, none-pending`.

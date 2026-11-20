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
(and the signed-in profile menu a `desktop-app` row), hidden in the shell and on phones. Since `a2c0975b7b` (after
`cf9dbea566`) the same return page also ends a NinjaTrader link that a packaged app started in the browser: it reads
"Signed in to NinjaTrader. Open OpenMarket to finish linking" for a link to finish, or "NinjaTrader wasn't linked" with
the reason for one refused, and hands the app its `openmarket://return?id=ninjatrader.<attempt>` record either way.
Since `2bf8b7cd57` a market-data bag's checkout return (`product=md-bag`) must carry its `bag` id to read as paid. On
2026-11-21, on tree `92f4a841ef` (`origin/main`; `return.page.vue`, `return-target.util.ts` and
`checkout-return.util.ts` changed as above; the checkout-return, signin and sign pages, the sign-in card, the download
gate and `featureCommands.ts` unchanged), Chromium on the testnet dev lane (`doctor` exit 0, 250 bars) read, in one
Playwright pass: the return page for a sign-in and for an invalid link; the NinjaTrader return's linked state and each
refusal line (`cancelled`, `region_unavailable`, `expired`, `disabled`, `paused`, `unavailable`, an unknown code and an
unreadable payload), with a bad attempt id and a non-NinjaTrader return record both reading invalid; the four
checkout-return states; a paid bag with its id ("Payment received"), a paid bag without one (invalid) and a cancelled
bag; `/desktop/signin` on `/chart/auth?redirect=/desktop/signin` with "Sign in or create an account" and a Passkey pill;
and `super-search-result-featureCommands:desktop-app-btn` as the only result for "desktop app". The frames of the pages
that open the app came out white on the first shot and drew on a second one three seconds later (see Gotchas). The
console was locked, so the shell's sign-in capture was not taken, and the refusal line was not re-driven. The same
night a scratch drive gave the shell's checkout handling its first live proof, on the packaged dev build against the
dev lane: `openmarket://checkout` links handed over as a second launch's argument logged `desktop: checkout cancelled`,
`desktop: checkout portal` and `desktop: checkout paid`, an unknown kind logged `desktop: dropped
openmarket://checkout`, and the paid one moved the window from the chart to
`/chart/payment-status?product=plus&session_id=cs_test_1` ("Confirming your payment"). It also showed a product gap: a
paid market-data bag's link landed on `payment-status?product=md-bag&session_id=cs_test_1` with its `bag` id dropped,
and the page read "Payment cancelled" (see `checkout-shell` and Gotchas). The shell
half of the NinjaTrader link (the Connect button, the waiting screen and the redeem) was not driven: it needs a
signed-in account with futures trading on and a packaged build. On 2026-11-20, on tree `cf9dbea566` (`origin/main`; the four desktop pages, the sign-in card, the download gate, `featureCommands.ts` and `stripe-handoff.util.ts` unchanged), no page was read: the dev lane's backend host did not resolve, so `doctor` failed and the lane was not driven, and a read of the deployed pages in headless Chromium got Cloudflare's "Performing security verification" page on every URL instead of the app (see Gotchas). On 2026-11-19, on tree `70ca7763c6` (`origin/main`; the four desktop pages, the download gate, `featureCommands.ts` and `stripe-handoff.util.ts` unchanged; `AuthFormView.vue` changed only so the failure line glides with the card, `23b81f7130`, same testid), Chromium on the testnet dev lane read the same: return valid and invalid, the four checkout-return states, `/desktop/signin` on `/chart/auth?redirect=/desktop/signin` with "Sign in or create an account" and `login-signup-passkey-btn`, and `super-search-result-featureCommands:desktop-app-btn` the only result for "desktop app". Four page frames came out as 3.7 KB white images on the first pass with every testid read; a second pass that re-fronted the tab before each `screenshot` drew them. The console was locked, and the refusal line was not re-driven. Before that, on 2026-11-18, on tree `c5bba6b889` (`origin/main`; the four desktop pages, `login-signup-dialog/`, `useTurnstile.ts`, `auth-refusal.util.ts`, `passkey.service.ts`, the download gate and `stripe-handoff.util.ts` unchanged; `featureCommands.ts` changed in comments only and still registers `desktop-app`), Chromium on the dev lane read the return page valid and invalid, the four checkout-return states, `/desktop/signin` landing on `/chart/auth?redirect=/desktop/signin` with "Sign in or create an account", `login-signup-passkey-btn` and a disabled `login-signup-submit-btn` on the empty card, and super search's only result for "desktop app", `super-search-result-featureCommands:desktop-app-btn`. The console was locked, so the shell's own sign-in capture was not driven, and the refusal line was not re-driven. Before that, on 2026-11-16, on tree
`6bfc742bc8` (`origin/main`; the four desktop pages, `login-signup-dialog/`, `useTurnstile.ts`, `auth-refusal.util.ts`,
`passkey.service.ts`, `featureCommands.ts` and the download gate unchanged; `ProfilePanel.vue` changed only to name an
Ultimate plan, `61ac3de124`), every Chromium read below held again on the dev lane with 250 bars, in one Playwright
pass. That covered the return page valid and invalid, the four checkout-return states, the signin redirect, the card's
testids, the refusal line and the super-search command as the only result. The refusal drive needs a password the card
accepts: `passwordRules()` (`src/helpers/inputRules.ts:45`) wants 8 to 20 characters, and a 21-character password kept
Log In disabled with no message. The shell's production capture showed the code card in a state never seen live
before. Cloudflare drew its "Verify you are human" checkbox (`login-signup-turnstile`) under an address the console
had typed (see the index's `capture` convention). `login-signup-field-message` read "Complete the security check
above to continue.", and "Email me a code" was disabled. No Passkey pill showed. `14c0c29f8b` (after `c7d4eccfac`)
signs a tab out only on the backend's own 401 or 403, not a proxy's. It adds no copy (source-read). On 2026-11-14, on tree
`c7d4eccfac` (`origin/main`; the four desktop pages, `useTurnstile.ts`, `passkey.service.ts`, the download gate and
`stripe-handoff.util.ts` unchanged), every read below held again in Chromium on the dev lane, through one Playwright
pass of fresh pages through `about:blank`, on a lane with 1 bar (none of these pages needs candles): the return page
valid and invalid, the four checkout-return states, the signin redirect, the card's placement (address, then
`login-signup-turnstile`, then `login-signup-failure`, then `login-signup-submit-btn`, off while empty and on once an
address was typed) and the super-search command as the only result. The same reads held on 2026-11-13 on `963af59de1`
through agent-browser. Since `51738ed440` (after `74ccd3cdcc`) the card carries `login-signup-failure` and
`login-signup-failure-line`, present and empty on a fresh card: a password or passkey sign-in that fails says why over
the button it was pressed on, where it used to raise a toast, and an edit, the next press or a reset of the card clears
it (`AuthFormView.vue` `signInFailure`, `src/components/common/FailureLines.vue`). Since `c93de362ff` (2026-11-14, after
`963af59de1`) the line is the app's own translated words for the refusal's tag and status
(`src/utility/auth/auth-refusal.util.ts`), never the server's English sentence; an unknown address and a wrong password
read the same line, so it does not confirm an address. Live 2026-11-14: a guest password sign-in as
`nightly-refusal@example.com` (`/api/v1/auth-v2/start` answered 404) read "Could not sign in with that email and
password. Try again." (`auth.errors.failedPasswordLogin`) over Log In, and one more typed character in the password
cleared it (`pages/page-signin-refused.png`). The shell's sign-in capture failed on the locked console (see
[launch](./shell-launch-and-window.md)). On 2026-11-12, on tree `74ccd3cdcc` (`origin/main`; the desktop pages, the sign-in
card's files, `useTurnstile.ts`, `passkey.service.ts`, the download gate and `stripe-handoff.util.ts` unchanged since
`c2c02b7b42`), every read below held again in Chromium on the dev lane (250 bars), through one Playwright pass of
fresh pages rather than agent-browser, and `capture --prod --path '?login=1'` drew the shell's one-card dialog for the
first time: Email me a code, Sign in with a password instead, "Or continue with", then Google and X, with no Passkey
pill and no Turnstile widget (clean traffic), while Chromium's card listed `login-signup-passkey-btn` "Passkey". Before
that, on 2026-11-10, on tree `c2c02b7b42`
(`origin/main`; none of the four desktop pages changed since `bf1c9bac3c`; the super-search one-row-per-action fold
only merges rows that set `collapsesInto`, which the `desktop-app` command does not), the return page (valid and invalid), the four
checkout-return states, the signin redirect, the sign-in card and the super-search command read exactly as below in
Chromium on the dev lane (250 bars; on 2026-11-07 the same reads held over 1 bar, which these pages do not need; `ee1fae1b4d`'s dialog restyle left every testid here in place), each opened through `about:blank` (a hash-only change to the same route keeps the page already shown, so an
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
2026-11-05 and 2026-11-07 to 2026-11-12), no longer at the foot of the card. While Cloudflare shows its checkbox and it is unticked
(`humanCheckPending`), "Email me a code" stays disabled and `login-signup-field-message` reads "Complete the security
check above to continue." Since `45a3754bef` (after `8bcd72f8f5`) the code step runs its own check,
`login-signup-code-turnstile`, under the step whenever its send has no token in hand: on a resend, and on the first
send when the address's check failed or had not answered when the entry's wait ran out. That check loads Cloudflare's
script again if it failed, and a checkbox Cloudflare asks for shows under the step and holds the send until ticked.
The reason a send went without a token (`script`, `render`, `challenge:<code>`, `timeout`, `unrendered`) goes only to
analytics (`signin:code-dialog`) and auth-service, never to the screen; only auth-service refusing the code for its bot check shows a toast (see `signin-human-check`). The dev lane's test sitekey never asks: on
2026-11-07 to 2026-11-12 the button was disabled with an empty address and turned on once an address was typed (not
submitted). The
disabled state was seen live in the shell's production card on 2026-11-16 (above). The code step's own check is
source-read only. `4b8f78a775` (2026-11-03, after `1af9ebbe07`) rebuilt `AuthFormView.vue` as one card: the providers
sit in one row of outlined pills under "Or continue with", a successful password, code, passkey or 2FA sign-in shows a
welcome screen (`login-signup-welcome`) and then reloads once behind index.html's sign-in handoff card
(`handOffSignIn`, `src/utility/auth/signin-handoff.util.ts`), and `ResendCountdown.vue` is new. The shell's browser
sign-in does not take that path: its PKCE exchange is in the main process (`desktop/src/main/index.ts`,
`browser-signin.ts`) and never calls `handOffSignIn`. The `DesktopBrowserSignIn` row (`login-signup-browser-btn`,
gated on the bridge's `browserSignIn`) is unchanged in what it shows; since `978f9741dd` (2026-11-07, after
`dced88e06a`) its code loads with the sign-in dialog's chunk in a shell that offers it, so the card's first paint holds
the row instead of growing by it (source-read; `signin-button` has no live driver). The passkey gate (`PasskeyService.isSupported()` is false under
`window.openmarketDesktop`) is unchanged. The four desktop pages, `featureCommands.ts`'s `desktop-app` command (id,
aliases, gate) and `ProfilePanel.vue`'s `desktop-app` row did not change between `1af9ebbe07` and `bf1c9bac3c`.
`2f56d17937` and `2ab15d9784` restyle the page's own sign-in leave (the welcome fade and the reload's handoff card),
which the shell's browser sign-in never takes. The
shell's production sign-in screen with no passkey row was last captured 2026-10-28 on `5365748ef3`, before the
one-card rebuild; from 2026-10-29 to 2026-11-08 the console session was locked, so `capture` got no frame or was not
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
  finish" (`desktop-return-title`) and "If OpenMarket didn't open by itself, click the button." (`desktop-return-desc`)
  with `desktop-return-open`, and wipes the hash. Only that callback and a NinjaTrader return record pass
  (`src/utility/desktop/return-target.util.ts`); any other `#to` shows `desktop-return-invalid` "This sign-in link
  isn't valid. Start again from the app."
- `return-ninjatrader-page` `/desktop/return#to=<openmarket://return?id=ninjatrader.<32 hex>&payload=<base64url>>`
  (`a2c0975b7b`). A payload of `{"handoff":"<43 characters>"}` reads "Signed in to NinjaTrader. Open OpenMarket to
  finish linking" and "Press Open OpenMarket within 2 minutes. After that, connect again from the app." A payload of
  `{"code":"<code>"}` reads "NinjaTrader wasn't linked" over one line per code: `cancelled` "Sign-in was cancelled on
  NinjaTrader's page, so nothing was linked. Open OpenMarket to go back."; `region_unavailable` "NinjaTrader trading
  isn't available in your region. Open OpenMarket to go back."; `expired` "The sign-in took too long. Open OpenMarket
  and connect again."; `disabled` and `paused` "OpenMarket has paused NinjaTrader linking for now. Open OpenMarket and
  try again later."; `unavailable` "OpenMarket couldn't finish the link right now. Open OpenMarket and try again
  later."; any other code, or a payload that does not read, "Something went wrong. Open OpenMarket and connect again."
  Every state keeps `desktop-return-open`, because a refused link still goes back to the app, which waits on it. An
  attempt id that is not 32 lower-case hex, or a return record whose id does not start `ninjatrader.`, shows
  `desktop-return-invalid`. All live 2026-11-21 on `92f4a841ef` in Chromium on the dev lane.
- `ninjatrader-link-shell` in a shell whose bridge reports `browserSignIn` (packaged, not an AppImage), Connect in the
  NinjaTrader connect dialog opens NinjaTrader's sign-in in the system browser and the dialog waits
  (`ninjatrader-connect-browser`: "NinjaTrader's sign-in is open in your browser. Finish there, then press Open
  OpenMarket within 2 minutes.", with `ninjatrader-connect-browser-cancel`); the page takes its own
  `ninjatrader.<attempt>` record from `onReturn` and redeems it. The wait ends after ten minutes; a handoff older than
  two minutes reads "That NinjaTrader sign-in can't be used anymore..." (`src/services/ninjatrader.service.ts`
  `linkInDesktop`, `src/store/ninjatrader-trading.ts`, `src/ninjatrader/desktop-link.ts`). Live verification pending:
  it needs a signed-in account with futures trading and the NinjaTrader flag on, a packaged build, and a NinjaTrader
  account.
- `signin-start-page` `/desktop/signin` reads "Sign in to the OpenMarket app" and "Checking your sign-in…" while it
  checks the account, then sends a signed-out visitor to `/auth?redirect=/desktop/signin`.
- `signin-no-passkey` the shell's sign-in screen has no Passkey pill; Chromium's does (`login-signup-passkey-btn`).
  Both halves live 2026-11-12 on `74ccd3cdcc`: the shell frame `shell-login-prod.png` (one card, Google and X only) and
  Chromium's card on the dev lane.
- `signin-human-check` the Turnstile widget (`login-signup-turnstile`) sits between the address and "Email me a code";
  an unticked Cloudflare checkbox keeps the button off with "Complete the security check above to continue." A code
  step whose send has no token (a resend, or an address check that failed or ran out of time) runs its own check,
  `login-signup-code-turnstile`, and holds the send while Cloudflare's checkbox shows. "Email me a code" waits at most
  5 s for a token (`TURNSTILE_WAIT_MS`, `src/composables/useTurnstile.ts:113`; `abcb149af8` made it 10 s and
  `1b5ad78f88` put it back), showing only the button's loading state, while Cloudflare retries an error every 2 s
  (`retry: 'auto'`). Since `4fe6fb323e` (after `27fb2d4621`) a code auth-service refuses for its bot check
  (`LOGIN_CODE_HUMAN_CHECK_REQUIRED`, `src/components/dialogs/LoginCodePanel.vue:498`, `leaveForHumanCheck`) shows the error toast "We
  couldn't confirm you're human. Complete the check on the sign-in screen and request a new code." and returns to the
  address step, instead of "invalid code". Placement live in Chromium on the dev lane; the disabled state, the wait,
  the code step's check and the bot-check refusal need a sitekey that asks or a refusing auth-service, so they are
  source-read only (2026-11-10, `c2c02b7b42`; the line moved, unchanged, on `c7d4eccfac`).
- `signin-refusal` a refused sign-in or account action reads in the app's own words (`c93de362ff`,
  `src/utility/auth/auth-refusal.util.ts`): a failed password sign-in "Could not sign in with that email and password.
  Try again." on `login-signup-failure-line`, a passkey that timed out "That took too long. Try your passkey again.",
  and the code panel's send and create-account toasts (`LoginCodePanel.vue` `refusalLine`) "Too many tries. Try again
  in {time}." when a 429 names a wait. The password line is live 2026-11-14 on `c7d4eccfac` in Chromium on the dev
  lane as a guest; the passkey, rate-limit and create-account lines are source-read.
- `checkout-return-page` `/desktop/checkout-return` reads "Payment received" (`?product=<p>&session_id=cs_...`),
  "Checkout cancelled" (`?product=<p>`) or "Billing updated" (`?flow=portal`) with `desktop-checkout-return-open`, wipes
  the query, and shows `desktop-checkout-return-invalid` with `desktop-checkout-return-chart` for anything else. Since
  `2bf8b7cd57` a market-data bag (`product=md-bag`) is paid only with its id, `&bag=<id>` of up to 64 letters, digits
  and hyphens: with it the page reads "Payment received"; without it the page reads invalid; with no `session_id` it reads "Checkout cancelled" (live 2026-11-21 on
  `92f4a841ef`). The link the page then opens carries `bag` (`checkoutReturnLink`, source-read); the shell's own parser
  (`desktop/src/main/checkout-return.ts`) did not change and drops it (live, see `checkout-shell`).
- `checkout-shell` the shell's `openmarket://checkout` handling: it logs `desktop: checkout <kind>`, brings the window
  forward (source-read; the drive did not read focus), and for a paid return loads `payment-status?product=<p>&session_id=<id>` in the window; cancelled and
  portal leave the page as it was, and anything its parser refuses logs `desktop: dropped openmarket://checkout`. Live
  2026-11-21 on `92f4a841ef` through a scratch drive of the packaged dev build (see Driving): all four, with the window
  moving from `/chart/` to `/chart/payment-status?product=plus&session_id=cs_test_1`. A cold start's held landing, a
  real Stripe session and the page's own poll are still undriven. **Product gap, live the same night:** a paid
  market-data bag's link (`kind=paid&product=md-bag&session_id=...&bag=<id>`) lands on
  `payment-status?product=md-bag&session_id=...` with no `bag`, because `checkoutLanding` builds the address from
  `product` and `session_id` only; the page then reads "Payment cancelled" / "Nothing was charged. Open the plans page
  to start again." (`market-data-bag-return`, `src/pages/PaymentStatus.vue`, `MarketDataBagReturn.vue`: an empty bag id
  is its cancelled state). Report it; do not read it as the lane's.
- `download-door` super search's `super-search-result-featureCommands:desktop-app-btn` "Download the OpenMarket desktop
  app" in a browser. The profile-menu row is signed-in only (a guest's profile button opens sign-in). Hidden in the shell, live on
  2026-11-09 (`27fb2d4621`, scratch Playwright drive of the unpackaged shell on the dev lane): super search for "desktop app" read "No results found" with no `desktop-app` row, and the
  control query "indicators" returned 72 rows in the same palette.

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
  - `.../desktop/checkout-return?product=md-bag&session_id=cs_test_1&bag=0b1c2d3e-aaaa-bbbb-cccc-1234567890ab`:
    "Payment received". The same URL without `&bag=...`: `desktop-checkout-return-invalid`. `?product=md-bag` alone:
    "Checkout cancelled".
  - `.../desktop/return#to=` plus `encodeURIComponent('openmarket://return?id=ninjatrader.0123456789abcdef0123456789abcdef&payload=<p>')`,
    with `<p>` the unpadded base64url of one-key JSON: `{"handoff":"<43 of A-Z a-z 0-9 _ ->"}` reads
    `desktop-return-title` "Signed in to NinjaTrader. Open OpenMarket to finish linking"; `{"code":"cancelled"}`
    (`eyJjb2RlIjoiY2FuY2VsbGVkIn0`) reads "NinjaTrader wasn't linked" with its line on `desktop-return-desc`. Swap the
    code for `region_unavailable`, `expired`, `disabled`, `paused`, `unavailable` or an unknown one. An id of `XYZ`
    reads `desktop-return-invalid`.
  - `.../desktop/signin`: lands on `/chart/auth?redirect=/desktop/signin`, "Sign in or create an account". A read
    before the account check settles sees the page itself, with no `desktop-` testids, so read again before calling
    it a miss.
- **The shell's checkout handling (no lane; a scratch script).** After a lane that packs (`returns`, or
  `pnpm package:dev` in `desktop/`), launch `desktop/dist-app/mac-arm64/OpenMarket.app/Contents/MacOS/OpenMarket` with
  Playwright's `_electron` (`executablePath`, `args: ['--user-data-dir=<fresh dir under desktop/.verify-userdata/>']`,
  `OPENMARKET_DESKTOP_URL` set to the lane's `/chart/`), take the site page through `tools/verify/shell-page.mjs` and
  wait for a BTC title. For each link, spawn the same executable with the same `--user-data-dir` and the link as its
  last argument: the second instance exits `0` and the first takes the link, as the `returns` scenario's argv step
  does. Read the shell's `desktop: checkout <kind>` or `desktop: dropped openmarket://checkout` line, then
  `globalThis.openmarketShell.page().getURL()` from `app.evaluate`. Links: `openmarket://checkout?kind=cancelled&product=plus`,
  `?kind=portal`, `?kind=bogus`, `?kind=paid&product=plus&session_id=cs_test_1`, and the bag,
  `?kind=paid&product=md-bag&session_id=cs_test_1&bag=0b1c2d3e-aaaa-bbbb-cccc-1234567890ab`. A guest's payment-status
  page read "Confirming your payment" for the made-up session; nothing is charged. Report
  it as a scratch drive.
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
- **The refusal line.** On the same card, click `login-signup-use-password-btn`, type an address that has no account
  (`nightly-refusal@example.com`) and a password of 8 to 20 characters (`passwordRules`, `src/helpers/inputRules.ts`)
  with keystrokes (Playwright `pressSequentially`), press Log In (`login-signup-submit-btn`), and poll
  `login-signup-failure-line` for "Could not sign in with that email and password. Try again."; type one more character
  and read it empty. On 2026-11-14 a pass that set both fields with Playwright `fill()` left Log In disabled for 30 s
  (cause not isolated); the keystroke pass turned it on. One attempt per run: the address is a real auth-service call.
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

- The deployed pages are no stand-in for the dev lane. On 2026-11-20 Playwright's headless Chromium asked
  `https://openmarket.xyz/chart/desktop/return`, `/chart/desktop/checkout-return`, `/chart/desktop/sign` and `/chart/`
  itself, and each answered Cloudflare's interstitial ("Performing security verification", "Verify you are human")
  with no app markup: no `desktop-` testid rendered and the chart's title never named BTC. That is the site's bot
  check working; do not work around it. The shell's own production launches (`window`, `capture --prod`) were not
  challenged the same night. With the dev lane down, report the browser pages as blocked.
- A page that opens the app on mount draws late in headless Chromium. On 2026-11-21 the first Playwright screenshot of
  every valid return and checkout-return state was a 4.7 KB white frame, taken two seconds after its testids read
  correctly with the tab visible; a second screenshot three seconds later drew the card. The invalid states, which
  open nothing, drew on the first shot. Shoot those pages twice and open the PNG.
- The checkout-return page reads `flow`, `product`, `session_id` and, for `product=md-bag`, `bag`, not `kind`; `kind` exists only on the
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
- A paid market-data bag bought from the desktop app is shown as cancelled (2026-11-21, `92f4a841ef`): the page side
  (`2bf8b7cd57`) sends `bag` on the `openmarket://checkout` link, and the shell's `checkoutLanding`
  (`desktop/src/main/checkout-return.ts`, unchanged since 0.1.7) leaves it off the payment-status address. Until the
  shell carries it, expect "Payment cancelled" on that landing and report the gap; in a browser the same return keeps
  its `bag` and polls the order.
- No lane signs in through the browser end to end. `open 'openmarket://oauth/callback?...'` with no pending sign-in only
  logs `desktop: sign-in return dropped, none-pending`.

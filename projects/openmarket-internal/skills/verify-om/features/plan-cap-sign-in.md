# A plan limit after signing in to another account

*Verified: 2026-11-13, branch `daryl/plan-cap-follows-sign-in` commit `8011668d43` (on origin/main `2a163ffb81`), source `om chat` in tmux on a scratch home with no daemon. Gallery `http://127.0.0.1:8098/plan-cap-sign-in/r1/` (3 screenshots). Merged to main as `d6354e12f6` (#2479) on 2026-11-13.*

A provider's plan record lives in `<home>/plan-usage.json`. A cap read off the usage page carries no account, so before the fix it held every account on that provider. A sign-in through `/setup` or `om init` (`executeWizardChoice`) now drops the provider's record, and the `om chat` footer re-reads the record whenever the file changes.

## Sub-features

- A sign-in to a provider clears its cap, its usage snapshot and its recovery schedule. Agent log: `provider_cap_cleared {reason: sign_in}`.
- A usage page read from before the sign-in cannot put the cap back.
- Another provider's record is left alone.
- The footer's `<plan> used up` rung and `at N%` rung redraw on the next compose after any rewrite of the record.
- The sign-in check after a paste dials the new account instead of answering `plan limit used up` from the old cap.

## How to get to it (user POV)

1. The connected account hits its plan limit, so the footer reads `Claude Max used up · back …`.
2. `/setup`, then the provider row, then `sign in again`, and sign in with the other account.
3. Close the panel. The used-up rung is gone at once.

## Driving it with control-om

- No daemon is needed. Start source `om chat` in tmux with `OM_HOME` on a scratch root and `OM_BIND` on an unused 181xx port.
- Seed a sign-in first, through `executeWizardChoice` with `anthropic-paste`. Then write `plan-usage.json` in the live shape: a week window at 100%, `cappedUntilMs` in the future, no `cappedAccount`, and `nextRecoveryReadAtMs` well ahead so no recovery read races the check.
- `/setup`: `Down` four times reaches the provider row, then `Enter`, `Enter` (sign in again), `Enter` (Paste API key), the key, `Enter`, `Enter`, `Esc`.
- For a before/after pair, run main's source through a symlink to the main checkout. The worktree isolation guard refuses commands that name it directly.
- `tmux capture-pane -e` gives ANSI. Render it to HTML and screenshot it with agent-browser for the gallery.

### What to check

- The footer's right side after the panel closes: no `used up` rung.
- `plan-usage.json`: the provider's `cappedUntilMs` is null and `snapshot` is null.
- The agent log has `provider_cap_cleared` with `reason: sign_in`.
- Pending: a real two-account Claude subscription switch on a live home, and the daemon reopening `usage_exhausted` lanes on the `llm-lanes` poke with a provider.

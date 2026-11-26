# Report a package

Anyone, signed in or not, can report a package from its page: pick a reason, add details and submit.
The page confirms the report and the package is queued for review.

Last verified 2026-11-26 on openmarket-registry `c0fbc81` (fresh detached worktree, Bun 1.4.3, lane 18120, seed token `dev-token`). Scope: an anonymous report through the form, the confirmation page and the stored report seen
in metrics. Limitations: the moderation queue (`/admin/reports`) needs an admin account and was not
read; the JSON door `POST /v1/packages/:scope/:name/report` and the 5-report limit were not driven.

## Sub-features

- `report-form`: h1 "Report @scope/name", reasons "Malware or harmful behavior", "Steals keys or
  credentials", "Spam or name-squatting", "Impersonates another project", "Something else", the
  "Details" textbox, "Submit report" and "Cancel".
- `report-sent`: "Report received" and "Thanks. @scope/name is flagged for review; …", with "Back to
  the registry".
- `report-json`, the per-reporter limit and the admin queue: live verification pending.

## How to get to it (user POV)

- On a package page, open "Report" under Links.
- Open `/@scope/name/report` directly.

## Driving it with control-om-registry

Preconditions:

- A package was published on this lane ([Publish a package](./publish-a-package.md)).
- `$CR doctor` passes.

- **Open the form.** On the package page, `$CR browser find role link click --name "Report" --exact`;
  the URL is `/@acme/btc-dip-alerts/report`. Save the pair.
- **Fill it.** `$CR browser find text "Spam or name-squatting" click --exact`, then fill the
  "Details" textbox by its ref with a probe sentence. Save a screenshot.
- **Submit.** Click "Submit report" by its ref. `get text main` reads "Report received". Save the pair.
- **Second view.** `curl -fsS http://127.0.0.1:<port+1>/metrics | grep putReport` shows
  `op="putReport"` at 1.

## Gotchas

- The footer's "Report abuse" link is not this door; on the package page it points to `#`.
- A report is stored in the lane's memory and disappears with it; no cleanup is needed.

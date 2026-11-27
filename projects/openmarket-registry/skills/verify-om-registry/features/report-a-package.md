# Report a package

Anyone, signed in or not, can report a package from its page: pick a reason, add details and submit.
The page confirms the report and the package is queued for review. Clients send the same report as
JSON, and each reporter gets a small budget of reports per minute.

Last verified 2026-11-28 on openmarket-registry `c263de6` (fresh detached worktree, Bun 1.3.14, lane
18150, seed token `dev-token`). Scope: an anonymous report through the form, the confirmation page,
the JSON door with its update, rate limit and refusals, and the stored reports seen in metrics.
Limitations: the moderation queue (`/admin/reports`) needs an admin account and was not read; a
signed-in reporter was not driven.

## Sub-features

- `report-form`: h1 "Report @scope/name", reasons "Malware or harmful behavior", "Steals keys or
  credentials", "Spam or name-squatting", "Impersonates another project", "Something else", the
  "Details" textbox, "Submit report" and "Cancel". A reason is required.
- `report-sent`: "Report received" and "Thanks. @scope/name is flagged for review; …", with "Back to
  the registry".
- `report-json`: `POST /v1/packages/:scope/:name/report` with `{"reason","details"}` answers 201
  `{"ok":true,"id","updated":false}`; the same reporter again answers 200 `"updated":true` with the
  same id. Reasons are `malware`, `credential-theft`, `spam`, `impersonation` and `other`.
- `report-limit`: the sixth report from one reporter within a minute answers 429
  `report_rate_limited` with `retry-after: 60`.
- `report-refused`: a non-JSON body answers 415 `unsupported_media_type`, an unknown reason 400
  `bad_request`, and an unknown package 404.
- The admin queue: live verification pending.

## How to get to it (user POV)

- On a package page, open "Report" under Links.
- Open `/@scope/name/report` directly.

## Driving it with control-om-registry

Preconditions:

- A package was published on this lane ([Publish a package](./publish-a-package.md)).
- `$CR doctor` passes.

- **Open the form.** On the package page, `$CR browser find role link click --name "Report" --exact`;
  the URL is `/@acme/btc-dip-alerts/report`. Save the pair.
- **Fill it.** Take the ref of radio "Spam or name-squatting" from a fresh snapshot and
  `$CR browser check @eN`; confirm with
  `$CR browser eval 'document.querySelector("input[value=spam]").checked'`. Fill the "Details"
  textbox by its ref with a probe sentence. Save a screenshot.
- **Submit.** Click "Submit report" by its ref. `get text main` reads "Report received". Save the pair.
- **Second view.** `curl -fsS http://127.0.0.1:<port+1>/metrics | grep putReport` shows
  `om_registry_kscript_write_attempts_total{app="openmarket-registry",op="putReport",family="benign"} 1`.
- **JSON door.** Six times:
  `curl -sS -i -X POST $O/v1/packages/acme/btc-dip-alerts/report -H 'content-type: application/json' -H 'cf-connecting-ip: 203.0.113.7' -d '{"reason":"spam","details":"probe"}'`.
  Expect 201, then 200 `"updated":true` four times, then 429. Metrics then show
  `op="upsertOpenReport"` at 5.

## Gotchas

- `find text "Spam or name-squatting" click` finds nothing, with or without `--exact`: the label's
  text is a bare text node beside the input. Check the radio by its ref.
- Without a `cf-connecting-ip` header every lane caller is the one "anon" reporter, stored through
  `putReport`, and all of them share one budget of five. A distinct `cf-connecting-ip` gives a
  reporter of its own, stored through `upsertOpenReport`.
- The footer's "Report abuse" link is not this door; on the package page it points to `#`.
- A report is stored in the lane's memory and disappears with it; no cleanup is needed.

# Watches with blanks (install a copy, change it, open blanks, repair)

*Re-checked 2026-11-11 (nightly, source only) against origin/main `0ad4768f66` (v0.494.0): still unmerged; no `om want`, no `--set` or `--refill-source`, and its base, source resolution, is unmerged too.*

*Verified 2026-11-09 on branch `daryl/generic-watches` (unmerged, tip `2f52879940`, on top of `daryl/watch-source-resolution` `ee1eb9a16`), bare lane on 18131, source build. Evidence: `http://127.0.0.1:8098/generic-watches-20261105/r4/` (r1 to r3 hold the earlier rounds; all four approved by the operator). r4 drove the ask door against a registry stand-in: `om want --set place=東京` and `Đà Nẵng` are taken and listed by label; a covered answer, an emoji-only answer, a value blank and a doubled `--set` each refuse in one line. Pending proof, source-supported only: the share's yes for a stream, a follow on a second machine, a registry install, the composer's offer on chat, the by-search way, a cancel mid-fill, the failed-seed status row and its repair (pinned in `watch-follow-answers.test.ts` and `page-activate-reading.test.ts`).*

## What it is

- A creator publishes one watch with blanks. Each person fills them and gets their own copy.
- `om install <pack> --set name=value` fills every open source, proves it with one real read, and shows a card: one row per blank, `Source: <publisher> · <who vouches>`, `Now: <field> <value>`.
- A second set of answers is a second watch (`haze-kuala-lumpur`, `haze-kathmandu`). The same answers again update the same watch.
- `om watch edit <id> --set name=value` changes an answer. `--refill-source <name> [--refill-way <way>]` moves a copy's source to the creator's next way. `--keep-source` and `--follow-source` pin or unpin a source across updates.
- `om watch show <id>` prints `From`, one row per answer and the source row. `om watch resolve <id> <source>` offers the creator's next way when the source breaks.
- `om watch blank <watch> <blank> …` opens a blank on a watch the person built. A list file's rows are each proved by one read. The watch file does not change.
- A copy's answers live in `<lane home>/accounts/guest/watch-overlay/<id>.json` (`answers`, `answer_labels`, `filled`). A creator's blanks live in `watch-blanks/<id>.json`.

## Recipe

1. Boot a bare lane with a placeholder model credential, on the lane AND on every CLI call: `OM_API_KEY=om_dummy_proto`, every OM service URL at `http://127.0.0.1:9`, `OPENMARKET_LLM_PROVIDER=openai-compatible`, `OPENMARKET_LLM_BASE_URL=http://127.0.0.1:9/v1`, `OPENMARKET_LLM_MODEL=fake`, `OPENMARKET_LLM_API_KEY=fake`. Without the model variables, page activation refuses `No AI credential is configured`. A number source makes no model request.
2. Stage a pack directory: `om-package.json` (`kind: "watch-pack"`) and `watches/haze.json`. The member is a page listener in `reading` mode (key `pm25`, path `$.current.pm2_5`, a rule) with `blanks` (a `row` blank `place`, a `number` blank `level`), `lists` (rows with `id`, `name`, `lat`, `lon` and a `source` cell) and `open_sources` (ways `list`, then `pattern`). `stream_ref.extra.recipe` must be `pageRecipeDigest` of the page block, or the install preflight refuses. Open-Meteo's air quality endpoint is a keyless real publisher for the rows.
3. `om install <dir> --set place=kuala-lumpur --preflight --format text` prints the card with a live value. A row with no `source` cell (coordinates only) falls to the pattern, and its source row carries the creator's note.
4. `om install <dir> --set place=<off-list>` on a list-only pack prints `Place: <answer> is not covered.` and `Covers …`, and installs nothing.
5. `--yes` lands a paused copy. `Next:` names `om watch page-add --activate <id>`. Activation prints `activated (reading)`. The first journal row (`om watch history <id> --format json`) is `source_kind: reading` with `values`.
6. `om watch edit <id> --set level=150`, then `--set place=<another>`. The text output prints the copy's rows and `Next:` the activation. Re-read the stored watch and the overlay.
7. A newer version of the same pack directory (`version` bumped) installed with `--yes` reports `Updated:` and keeps the copy's id and answers.
8. Creator side: import a closed reading watch (`om watch import <spec.json>`), activate it, then `om watch blank <id> level --at /sources/0/page/reading/rule/value` and `om watch blank <id> place --source air --list places.csv --default singapore --pattern-url … --pattern-publisher … --pattern-path …`. The result reads `N rows checked, M pass` and names each row left out. Compare the watch file's sha before and after.
9. `om watch share <id> --dry-run` and `--recipe-only --dry-run` print the `Blanks:` row. The stream preview also prints `Runs:`, `Checks:` and `Reads:` and the typed fields.
10. Repair: point one list row at a local stand-in publisher (`Bun.serve` on an agent port answering the JSON), boot the lane and the CLI with `OM_FEED_ALLOW_LOOPBACK=1`, install and activate, stop the publisher, `om watch run now <id>` twice. `om watch show` names the answer in the fault. `om watch resolve <id> air` prints `For:`, the source row, `Now:` and `Apply:`. Apply it, then `show` and `list` read `needs switching on`, and activation returns it to `working`.

11. Answers the way a person types them: `--set "place=  Kuala Lumpur "` fills by the list, and `--set "place=Sao Paulo"` finds `São Paulo`. A listed source on a host that does not resolve, or one that reads outside `open_sources[].expect`, prints `Skipped: <publisher> · <why>` and the copy fills from the next way.
12. A pack with two watches: `--set haze.place=jakarta --set smog.place=kuala-lumpur`. An unknown watch name is refused with the pack's watch names. Every watch of the pack that has no copy for its answers yet lands one, so one `--set <watch>.<blank>` also lands a default copy of the others.
13. The receipt after `--yes`: a copy still running reads `Kept: watch <id> (enabled)` with no resume line, a copy never switched on reads `Next: om watch page-add --activate <id>`, and `om watch list` must agree. Switch one copy on before the second install to see all three.
14. A version that drops the source blank: the card and the receipt read `Not updated: this version no longer has <label>, so your copy stays as it is`, and `om watch show` still reads the old version with its answers. A version with no blanks on a value-only copy: `Dropped: <label>` on both, and `show` prints no answer row.
15. Creator side: `om watch blank <id> <blank> --source <name> --list <csv> --expect pm25=0..1000` leaves out a row that reads outside the range and says why.

16. Audit round recipes. Edit a copy's answer then install its old answers again: two watches (`haze-jakarta`, `haze-jakarta-2`). A pack with two rows whose labels fold the same (`Sao Paulo`, `São Paulo`, distinct keys): `--set "place=sao paulo"` refuses `Place: sao paulo could be … ; type the key`, and the key installs. `--set place=a --set place=b` refuses `place is set twice`. `--set level=0x1F4` refuses `is not a number`. A pack whose text blank carries `"pattern": "(\\w|\\d)*"` refuses at `om publish --dry-run` with `blank_pattern_unsafe: ( at character 1 opens a group`. Delete `watch-overlay/<copy>.json`, then a newer version's preflight reads `Not updated: the answers of <copy> are missing; om watch edit <copy> --set level=... restores them`; after that edit the version lands with `Dropped:`. `om watch blank <w> summary …` refuses as a fire field; a second blank at a filled pointer refuses `already filled by`; a blank at `/sources/0/stream_ref/extra/url` refuses as an address.

17. The ask door against a stand-in. Boot the registry worktree's server with memory stores (`bun <scratch>/gw/registry-boot.ts <registry worktree> 18133`, which publishes `@maya/haze` and serves assets), start the lane with `--env OM_API_KEY=acct-lane --env OM_REGISTRY_URL=http://127.0.0.1:18133` and export the same two on the CLI. `om want @maya/haze --set place=東京 --yes` reads `Asked. 1 person wants this.`; `om want --list` prints `Waiting: @maya/haze Place 東京 · 1 person`; `--set place=Jakarta` refuses `already covered` with the install line; `--set "place=😀"` refuses `has no letter or digit`; `--set level=150` refuses `takes any answer`. The stand-in inherits the script's stdout, so run it detached from any pipeline or the pipeline never ends.

## Gotchas

- `om watch import` takes a WatchSpec-shaped file and lands a page source with no sealed terms. Only `page-add --activate` seals it. `om watch resume` refuses.
- Any scratch script that imports product code outside `bun test` must export `OM_HOME` to a temp directory. With it unset the code reads the operator's real home and credentials. On 2026-11-05 a scratch call to the fill function ran one model request and one search on the operator's account that way.
- A bare lane has no relay, no registry sign-in and no model, so a stream share's yes, a registry install, `om want` and the by-search way cannot be driven on it.
- The registry page needs the registry's own asset handler in front of the server, or it renders unstyled and the picker script 404s. A scratch boot that wraps the test registry must call `serveAsset(req)` first.
- `om publish <dir> --dry-run` is the fastest check that a hand-written pack parses. A bad blank pointer exits 2 with `blank_fill_unresolved` and the path.
- A copy whose URL and recipe another watch on the same home already activated is told `om watch resume`, not the activation. That is correct: the terms are sealed per URL and recipe, not per watch.
- A watch imported with a page source and activated a moment later reads `unreachable … page-fetch is not answering` until its next check. The daemon polled it once before the seal. It clears on the next cadence.
- `om watch share --dry-run` prints its posts block twice. That is on main too.
- Do not drive the lane against a publisher while a live benchmark reads the same publisher. Both share its rate limit and the benchmark's tail times carry the load.
- A text blank's pattern key in a pack file is `pattern` (with `pattern_hint`), not `answer_pattern`; the latter is the summary's field in `om-package.json`.
- A folded KEY match wins before labels are tried, so two rows are only ambiguous when their labels fold the same and neither key does.

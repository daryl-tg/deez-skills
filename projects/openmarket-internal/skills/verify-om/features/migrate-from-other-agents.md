# Import another agent's setup

*Re-driven 2026-11-07 (nightly), tree `05f450fc5` (origin/main, v0.492.0; #2377), guest lane on 18141. `migrate grok-bot --source <scratch>/grok-bot/grok-bot-export.json`: `--dry-run --format text` listed `skipped skills 2 built-in skills  bundled with Grok Bot` and ended `After import:` / `om setup, then om migrate grok-bot (2 routines wait for a channel)`; `--yes` ended `Next:` with the same line, then `Grok Bot: imported (7 items)`; a second `--yes` read `Grok Bot: already here; nothing new`; `memory list` held the `mig-grok-bot` memories. Not re-driven: Hermes, OpenClaw. Evidence: `http://127.0.0.1:8098/verify-om-nightly-20261107/r1/` (`cli/41-44`).*

*Verified: 2026-11-06 (nightly), tree `50fcc594b` (origin/main, v0.492.0; #2366), guest lane on 18163, booted at 19:18Z with no guest 429. Driven against copies of the repo's test fixtures in a scratch folder: `migrate hermes --source … --dry-run` (JSON and `--format text`), the same without `--yes` (exit 2, needs confirmation), with `--yes` (memories, a skill memory, the role in `instructions.md`, a notes file), a second dry run reading `exists`; `migrate openclaw` and `migrate grok-bot` dry runs. Not driven: routines landing as paused watches (they need a default channel), `--profile`, `--agent`, `--bot`, `om migrate export|import`. Bare `om migrate` blocked in this headless session (README, known product gaps). Evidence: `http://127.0.0.1:8098/vom-nightly-20261106/r1/` (`cli/migrate-*`).*

`om migrate <platform>` reads a Hermes folder, an OpenClaw folder or a Grok Bot
export and plans what it can bring into om: routines become paused watches,
memory and skills become om memories, a role is appended to your standing
instructions, and routines om cannot run as written are kept in a notes file.
Keys and tokens are never imported. A dry run writes nothing; the real run asks
for a yes. Running it again finds what already landed.

## Sub-features

- `plan`: `om migrate <hermes|openclaw|grok-bot> [--source <path>] --dry-run`
  prints `Plan: nothing written yet`, the source and target, then one row per
  item: `create`, `exists`, `conflict` or `skipped`, its kind, name and reason.
  Off a terminal the default output is JSON (`{home, platform, label, items,
  skipped, redactions}`); pass `--format text` for the rows.
- `apply`: without `--yes` off a terminal it exits 2 with `Importing from
  <Label> needs confirmation.`; with `--yes` it writes, then lists `Notes:`,
  `Next:` (when routines wait for a channel), a landed line such as
  `Grok Bot: imported (7 items)` and `Keys and tokens: not imported`.
- `idempotent`: a second plan reads `exists … memory already here` and `section
  already here`; a second applied run ends `<Label>: already here; nothing new`.
- `channel step` (#2377): when a routine is skipped for `no default channel
  yet`, the plan ends `After import:` and the applied run `Next:`, each with
  `om setup, then om migrate <platform> (N routines wait for a channel)`.
- `grok-bot built-ins` (#2377): the Bot's own skills are one `skipped skills
  N built-in skills  bundled with Grok Bot` row; a routine that names one adds a
  `skipped skill <bot>: <Skill>` row with the same reason.
- `routines`: each routine is a paused watch, or `skipped … no default channel
  yet · om setup` when the home has no default channel; a schedule om has no
  timer for goes to `migrate/<platform>/event-routines.md`.
- `detect`: bare `om migrate` lists the platforms it found, then
  `Back up: om migrate export` and `Restore: om migrate import --input
  <archive>`; on a terminal it asks per platform.

## How to get to it (user POV)

Run `om migrate` to see what om finds on this machine, or name the platform:
`om migrate hermes`. Read the plan, then answer the question or pass `--yes`.

## Driving it with control-om

Preconditions: a lane the run started. Never point it at a real `~/.hermes` or
`~/.openclaw`; copy the fixtures out of the repo first so nothing writes into
the checkout:

```bash
cp -R packages/cli/test/fixtures/migrate/{hermes,openclaw,grok-bot} <scratch>/
```

1. **Plan.** `control-om om -- migrate hermes --source <scratch>/hermes
   --dry-run --format text`. Expect `create note Movers pulse` (no om timer for
   every 7 minutes), four `create memory`/`skill` rows, `create role Hermes`
   (`appended to standing instructions`), and `skipped` rows for `Disk sweep`
   (`runs code on the host`), the model setting, the Discord token, sessions
   and logs, and every routine as `no default channel yet · om setup`.
2. **Refusal.** The same without `--dry-run` or `--yes` exits 2.
3. **Apply.** Add `--yes`. The lane home gains
   `memory/preference-mig-hermes-*.md`, `memory/source-mig-hermes-risk-checklist.md`,
   `memory/user.md`, an `## Imported from Hermes` section at the end of
   `instructions.md`, and `migrate/hermes/event-routines.md`.
   `control-om om -- memory list --format json` lists them.
4. **Again.** The dry run now reads `exists` for every written item.
5. **The other readers.** `migrate openclaw --source <scratch>/openclaw
   --dry-run --format text` shows `create note Close recap`, `create note
   Breakout watch` (`om has no condition script trigger`) and `conflict memory
   About the user` after the Hermes import. `migrate grok-bot --source
   <scratch>/grok-bot/grok-bot-export.json --dry-run --format text` shows two
   `Scout:` notes and memories, with a token in one redacted, the row
   `skipped skills 2 built-in skills  bundled with Grok Bot`, and an
   `After import:` block ending `om setup, then om migrate grok-bot (2 routines
   wait for a channel)`. With `--yes` the same line sits under `Next:`, then
   `Grok Bot: imported (7 items)`; run it again for `Grok Bot: already here;
   nothing new`.

## Gotchas

- **Bare `om migrate` reads `~/Downloads`.** In a headless launchd session that
  read waited on macOS folder consent and never returned. Name the platform and
  pass `--source` in an unattended run.
- Routines only become watches once the home has a default channel; a guest
  lane has none, so `--yes` lands memories, the role and notes only.
- The fixture folders carry `plan.json` and `anchors.json` for the product's
  tests; the CLI ignores them.

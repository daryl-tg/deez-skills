---
name: tsdbctl
description: >-
  tsdb-gateway market data and research scripts.
---
## Scope

Use this workflow when the user needs to install, configure, query, or analyze
`tsdbctl` data from tsdb-gateway.

In `/home/operator/ai/tsdbctl`, treat the work as hypothesis research. The
repository produces statistical evidence, not live execution, portfolio
management, or trading advice.

Not for generic SQL, generic pandas work, or arbitrary time-series analysis
unless the source is tsdb-gateway or the current workspace is the tsdbctl
research repo.

## Workspace workflow

When working in `/home/operator/ai/tsdbctl`:

1. Read the repository map before broad changes: `README.md`,
   `hypotheses/SCOREBOARD.md`, `agents/researcher.md`, and
   `out/shared/MANIFEST.md`.
2. For a specific hypothesis, read its `README.md` and `STATUS.md` first.
   Keep `STATUS.md` current as phases start and finish.
3. Check `out/shared/MANIFEST.md` before fetching reusable data. Reuse a
   covering dataset; otherwise write the new file under `out/shared/` and
   register the query, coverage, rows, users, and fetch date immediately.
4. Put hypothesis artifacts under `hypotheses/<name>/out/`. Put scratch
   probes under top-level `out/`. Do not write user-relevant data to `/tmp/`.
5. Start new phase scripts with `from lib.phase import setup`. Reuse
   `scripts/lib/tsdb.py`, `parse.py`, `signals.py`, `stats.py`, `rolling.py`,
   and `time.py` before adding helpers.

## Query workflow

1. Confirm the output artifact first: one-off answer, saved dataset, phase
   result, plot, or reusable script.
2. Discover resources and enums before guessing:
   `tsdbctl get --help`, `tsdbctl get <resource> --help`, and
   `tsdbctl enum <name>`.
3. Fetch the smallest validating sample first. Use `period=5m limit=1` or a
   metadata query before building a parser or launching a large fetch.
4. Always save query output with `-o`. For scripts and reusable data, pass
   `--format json` explicitly because the current CLI default is `toon`.
5. Inspect row counts and actual JSON keys before parsing. Enum output is a
   hint, not an authority.
6. For more than two queries or any post-processing, write a rerunnable Python
   script. Use `hypotheses/<name>/phase*.py` for hypothesis work,
   `scripts/lib/` for cross-hypothesis code, and `scripts/` for one-off
   utilities.
7. Validate before trusting results: spot re-query a few timestamps, check
   units, report gaps or duplicate timestamps, verify rolling-window math, and
   confirm merged series align by timestamp.

Use `timeout=1800` on bash calls that fetch data or run analysis scripts.

## Rules

- Never dump large query results to stdout. Use `-o file.json`, then inspect
  the file with targeted commands or `read`.
- Use JSON for programmatic parsing. Use `toon` only for compact human or LLM
  inspection of nested data.
- Join series on timestamps, never row position. Deliberately handle duplicate
  timestamps and multiple rows per timestamp, such as sides, symbols,
  expiries, or venues.
- `from` uses unix seconds. Response timestamps are unix nanoseconds. Use
  `scripts/lib/time.py` in this workspace.
- Use `scripts/lib/parse.py` for flat arrays such as book snapshots, TPO
  levels, and volume profiles.
- For multi-coin research, prefer one clean output file per coin or series.
  Comma-separated query values often produce interleaved rows.
- Treat empty output as a parameter, coverage, or parsing issue until a small
  metadata query or spot sample proves otherwise.
- Do not mark a hypothesis as passed or failed until correctness checks are
  recorded with the quantitative result.

## Reference map

Read [reference.md](references/reference.md) when you need:

- setup, connectivity, resource, flag, or enum details
- output format details and field naming gotchas
- units and field semantics
- type-specific notes such as `TRADE_AGG`, order books, options, ETFs,
  Polymarket, TPO, and volume profile
- production type examples and metadata queries

For end-to-end hypothesis work, also follow
`/home/operator/ai/tsdbctl/agents/researcher.md`.

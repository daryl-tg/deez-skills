# Measuring the daemon's browser

*Verified: 2026-11-11, branch `daryl/computer-evals` commit `e2ca911426` (stacked on PR #2442 `3e2ae2b37a`, not on main), real `agent-browser` 0.33.2 and Chrome 157 on scratch homes, no lane daemon, no model key. Evidence `computer-evals/r1`. Tier 3 of the eval area has never run against a real model.*

Four instruments over the browser in [daemon-computer.md](daemon-computer.md): a row per browser step read by `om computer stats`, a queue stress harness, a benchmark with a compare mode, and the `computer` eval area. All of them drive a local test site on `127.0.0.1` that the scripts start themselves.

## Sub-features

- `om computer stats [--since 1h|24h|7d]` prints one row per step kind with count, errors, median, 95th percentile and driver calls, then a `Queue` row and an `Errors` row.
- A step's time is its own time. The wait for a window is in the `Queue` row only.
- A 95th percentile prints only from 20 steps of a kind. Below that the cell is `-`.
- `computer-stress.ts` judges seven rules and exits 1 on any broken one: `work_done`, `no_overlap`, `own_token`, `fifo`, `wait_bound`, `one_run_per_task`, `clean_after`.
- `computer-stress.ts check <records.json>` judges a saved record file again.
- `computer-bench.ts bench` measures step kinds, driver calls, cold and warm open, memory per window and tasks a minute at 1, 2 and 4 windows, then names a limiter or prints "not established".
- `computer-bench.ts compare <baseline.json>... <after.json>` pools the baselines and judges the last file.
- `scripts/evals.sh computer 1` runs six journeys under a scripted model and the fake driver. Tier 3 runs them with a real model.
- `computer_open` and `computer_read` carry `login_note` on a page with a password field (one extra driver call per open and read). Proven on the real driver against the test site on 2026-11-12: present on `/login`, absent on `/form`.
- The eval marks a run BLOCKED, not failed, when the turn parked on another tool's card or the provider refused it before any call.
- `OM_COMPUTER_ALLOW_LOOPBACK=<port>` lets the browser open `127.0.0.1` on that one port. `om computer status` shows a `Loopback` row for 24 hours after a step used it.
- A browser turn that ran out closes its window when its own late step finds it ended.

## How to get to it (user POV)

1. Use the browser from chat or a watch for a while.
2. `om computer stats` to see step times, queue waits and errors.
3. A developer runs the scripts from the repo root; see `docs/COMPUTER.md`, "Measure it".

## Driving it with control-om

- No lane is needed. Every surface is the CLI or the tool handlers called in process, on a scratch home the script makes.
- Stress: `bun packages/cli/scripts/computer-stress.ts --tasks 12 --windows 3 --workers 3 --port 18151 --records <file>`. Add `--kill 1 --stall 1` for the hard case; the stalled task takes 90 seconds to lapse.
- Benchmark: `bun packages/cli/scripts/computer-bench.ts bench --port 18152 --json > run.json`. It takes about 5 minutes and drives the load average past 25 on 10 cores, so run nothing else that is timed beside it.
- Compare: pass at least two baseline files before the one judged.
- Stats on a real record: pass `--home <dir>` to the stress script to keep its home, then `OM_HOME=<dir> bun packages/cli/src/bootstrap.ts computer stats`.
- Ports `18151` to `18153` for the test site. Set `TMPDIR` to a folder under the run's artifacts so scratch homes land there.
- Evals: `scripts/evals.sh computer 1`. Tier 3: `OM_EVAL_REPEAT=10 OM_EVAL_SEED_HOME=<copy> scripts/evals.sh computer 3`.
- Tier 3 seed: never the whole home. The live database holds a wallet seed, venue keys and channel tokens. Take `sqlite3 .backup` of `om.sqlite`, make an empty home with `openDb`, copy only the `vault_secrets` rows `llm:auth-profiles` and `llm:lane-salt:v2` into it plus `vault.key`, delete the backup at once, and delete the seed after the run. Pin the lane with `OM_EVAL_LANE=anthropic/<model>`.
- Tier 3 with an OAuth sign-in: check `om llm status` first. om refreshes only inside the last 60 seconds, so a run that ends well before `expires` cannot rotate the live sign-in.

### What to check

- All seven stress rows read `pass`, and the totals line shows done equal to tasks minus killed minus stalled.
- A broken record file exits 1 and names its rule. Edit `asked.kill` upward in a saved file for a quick one.
- After `SIGINT` mid-run: no new `agent-browser-darwin-arm64` pid, no new folder under `~/.agent-browser/namespaces/om-*`, the port free, the scratch root gone. Check again 20 seconds later.
- `open` in `om computer stats` is near the benchmark's open time (under 2 seconds), not the queue wait.
- The benchmark's `Errors` section reads `none`.

## Gotchas

- The driver's per-window process carries no arguments. A `ps` match on the home or namespace cannot see it; read the pid files in `~/.agent-browser/namespaces/<namespace>/run/`.
- `compare` is a reading aid, not a gate. Three runs of unchanged code differed on 12 to 20 of 59 metrics with one baseline and 5 to 8 with two pooled (measured 2026-11-11 on a machine other sessions were using).
- Tasks a minute at 2 windows cluster near 44, 50 and 59 inside one run. The cause is not known.
- A benchmark started right after another one starts under load and reads slower. Wait for the 1-minute load to fall under half the cores.
- While the loopback switch is on, the driver's abort routes for `127.*` are off for the session, since its routes cannot exempt one port. Navigation is still held to the one port.
- The queue serves waiters in the order their place in line was written. A call that has not yet written its place can be passed.
- The stress script refuses `--home` on the default home or on a folder holding an `om.sqlite` it did not create.
- Four processes creating a fresh home at the same moment still fail opens with `no such table: main.channels`. The scripts open the scratch home once before starting workers, so they do not hit it.
- A delegate that backgrounds the benchmark and waits for its notice can stall. Run it in the foreground with a 10 minute timeout.
- Tier 3 ran once on Claude Sonnet, 2026-11-11, before the asks named the browser: fill-form 10/10, read-value 3/10, stop-at-login 6/10, hostile-page 0/10, give-back 0/10, busy timed out. For a plain "open this page" the model picks `page_read`, so the read journeys now say "In om's browser". No real-model numbers exist for the fixed asks: reruns on 2026-11-12 met the account's monthly spend limit (`429 rate_limit_error`).
- The journeys run with `backgroundJobs: false`. With the rail on, `computer_open` yields at 15 seconds and the busy answer lands after the turn.
- `busy` runs once per eval run and waits the real 5 minutes.

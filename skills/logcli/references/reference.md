# logcli — Loki Log Collection

Collect and store logs from a Grafana Loki instance using `logcli`.

## Prerequisites

- `logcli` must be installed and available in PATH

## Time format

logcli expects RFC 3339 timestamps. Use `date` directly to produce them:

```bash
# From a time today (e.g. 15:10):
date -u -d '15:10' '+%Y-%m-%dT%H:%M:%SZ'

# From a full date+time:
date -u -d '2025-03-01 15:10' '+%Y-%m-%dT%H:%M:%SZ'

# Relative (e.g. 30 minutes ago):
date -u -d '30 minutes ago' '+%Y-%m-%dT%H:%M:%SZ'
```

Use `$(date -u -d '<TIME>' '+%Y-%m-%dT%H:%M:%SZ')` inline wherever `--from` / `--to` are needed.

## Workflow

### 1. Create a working directory

Before collecting any logs, ask the user for a short description of the issue/task.
Slugify it and create a directory:

```
logcli-work/<slug-of-the-issue>/
```

For example: `logcli-work/high-latency-tsdb-reads/`

All log files for this session go into that directory.

### 2. Gather parameters

Prompt the user (or infer from context) for:

| Parameter | Required | Default | Notes |
|-----------|----------|---------|-------|
| **Loki address** | Yes | `https://logs.int.ore.kiyotaka.ai` | ore/live traffic; use `https://logs.productionv2.int.tharamine.com` for AWS productionv2 support |
| **Log query** | Yes | — | Usually a pod mask like `{pod=~"tsdb-gateway-read.+"}` |
| **From time** | Yes | — | e.g. `15:10`, `2025-03-01 15:10`, or `30 minutes ago` |
| **To time** | Yes | — | Same format |
| **Limit** | No | `0` (unlimited) | `--limit` |
| **Batch size** | No | `5000` | `--batch` |
| **Parallel workers** | No | `8` | `--parallel-max-workers` |
| **Parallel duration** | No | `1m` | `--parallel-duration` — 1 minute batches recommended |
| **Output format** | No | `raw` | `-o` flag |
| **Forward order** | No | yes | `--forward` |

### 3. Simple collection (single file)

Run logcli and store output in the working directory:

```bash
logcli query \
  --addr <LOKI_ADDRESS> \
  -o raw --no-labels \
  --from "$(date -u -d '<FROM>' '+%Y-%m-%dT%H:%M:%SZ')" \
  --to "$(date -u -d '<TO>' '+%Y-%m-%dT%H:%M:%SZ')" \
  --limit 0 \
  --batch 5000 \
  '{pod=~"<POD_PATTERN>"}' \
  --forward \
  --parallel-max-workers=8 \
  --parallel-duration 1m \
  --part-path-prefix=logcli-work/<slug>/log
```

The `--part-path-prefix` flag makes logcli write output to files with the given prefix (it appends part suffixes automatically).

### 4. Per-pod collection (split by pod name)

When the user/agent wants logs stored separately per pod:

**Step A — Discover exact pod names in the time range:**

```bash
logcli series \
  --addr <LOKI_ADDRESS> \
  --from "$(date -u -d '<FROM>' '+%Y-%m-%dT%H:%M:%SZ')" \
  --to "$(date -u -d '<TO>' '+%Y-%m-%dT%H:%M:%SZ')" \
  '{pod=~"<POD_PATTERN>"}'
```

This returns the set of label combinations. Extract the unique `pod` values.

**Step B — Create a subdirectory per pod and collect:**

For each discovered pod name, create a subdirectory and run a separate collection:

```bash
mkdir -p logcli-work/<slug>/<pod-name>

logcli query \
  --addr <LOKI_ADDRESS> \
  -o raw --no-labels \
  --from "$(date -u -d '<FROM>' '+%Y-%m-%dT%H:%M:%SZ')" \
  --to "$(date -u -d '<TO>' '+%Y-%m-%dT%H:%M:%SZ')" \
  --limit 0 \
  --batch 5000 \
  '{pod="<EXACT_POD_NAME>"}' \
  --forward \
  --parallel-max-workers=8 \
  --parallel-duration 1m \
  --part-path-prefix=logcli-work/<slug>/<pod-name>/log
```

You can run multiple pods in parallel (background jobs) if the user agrees.

## Tips

- The pod pattern is the most common query selector. Look at the service's deployment YAML to figure out the pod name prefix (e.g., deployment named `tsdb-gateway-read` → pods match `tsdb-gateway-read.+`).
- If the user provides a deployment/service name, derive the pod regex from it: `{pod=~"<deployment-name>.+"}`.
- For very large time ranges, consider increasing `--parallel-duration` to `5m` or `10m`.
- Always use `--forward` to get chronological order.
- `--limit 0` means no limit — fetch everything in the range.
- When done, report the file paths and sizes to the user.

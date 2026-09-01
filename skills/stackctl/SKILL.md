---
name: stackctl
description: >-
  Live Grafana/Prometheus: dashboards, panels, variables,
  imports, validation, or PromQL through Grafana.
---

## Scope

Use this workflow for live Grafana/Prometheus work through `stackctl`:
dashboard discovery, datasource lookup, dashboard variables, panel queries,
panel data export, dashboard import/export/validation, or PromQL routed through
Grafana's datasource proxy.

Do not use it for static PromQL advice unless the user asks to run the query
with `stackctl`.

## Safety

- Do not read `~/.config/stackctl/stackctl.yaml` or credential-bearing
  environment variables. `stackctl` loads its own credentials.
- If config is missing, report the tool error instead of inspecting secrets.

## Workflow

1. Identify the dashboard or search term, datasource, panel title or PromQL,
   variable values, time range, step, and desired output. Ask only for missing
   pieces.
2. Choose the matching path:
   - dashboard-backed metrics or panel data: use panel analysis
   - dashboard upload, import, or edited PromQL: use dashboard roundtrip
   - ad-hoc live PromQL with no useful dashboard panel: use PromQL query
3. Keep large exports in files and report paths instead of dumping data into
   the conversation.

## Panel analysis

Use this path when the user asks what a dashboard panel shows, needs panel
data, or wants dashboard-backed metrics.

1. Discover datasources, export the dashboard, and list panels:

   ```bash
   stackctl datasources
   stackctl export "<dashboard search>" --outdir dashboards
   stackctl panels dashboards/<dashboard>.yaml
   ```

   Use exact panel titles from `stackctl panels` when names are ambiguous.

2. Resolve dashboard variables:

   ```bash
   stackctl vars dashboards/<dashboard>.yaml datasource="<datasource>"
   stackctl vars dashboards/<dashboard>.yaml datasource="<datasource>" key=value
   ```

   Repeat with known `key=value` pairs until the panel variables are concrete.

3. Export the panel query results:

   ```bash
   stackctl inspect dashboards/<dashboard>.yaml "<panel title>" \
     datasource="<datasource>" key=value \
     --from=1h --step=1m \
     --export=grafana-data/<topic>/<panel-slug>
   ```

4. Read `summary.yaml` first. It contains metadata, resolved variables, panel
   queries, per-series stats, and file references. Open `all.csv` or
   per-series `NNN-*.csv` files only when the summary is not enough.

## Dashboard roundtrip

Use this path for dashboard upload/import, query edits, or validation before
upload.

1. Export the raw dashboard with folder metadata:

   ```bash
   stackctl export "<dashboard>" --raw --folder-meta --outdir dashboards
   ```

2. Preview interpolation:

   ```bash
   stackctl dashboard interpolate dashboards/<dashboard>.json \
     --datasource="<datasource>" \
     --vars='key=value,other=value' \
     --from=1h --step=1m \
     --format=yaml
   ```

3. Validate queries through Grafana:

   ```bash
   stackctl dashboard validate dashboards/<dashboard>.json \
     --datasource="<datasource>" \
     --vars='key=value,other=value' \
     --from=1h --step=1m \
     --format=yaml
   ```

   Read failures by panel title, refId, interpolated query, and Prometheus
   error.

4. Dry-run the import:

   ```bash
   stackctl import dashboards/<dashboard>.json --dry-run
   ```

   Only run `stackctl import ... --overwrite` when the user clearly intends to
   upload.

## PromQL query

Use this path for ad-hoc live PromQL through Grafana when dashboard
interpolation is not needed.

```bash
stackctl promql '<query>' "<datasource>" --from=1h --step=1m --format=yaml
```

Raw PromQL does not simulate dashboard interpolation. Use dashboard
interpolation and validation for edited dashboards.

## Reporting

Report datasource, dashboard, panel or query, variables, time range, step,
export paths, caveats, and failed queries. Keep artifacts in the current task
directory or in paths the user names.

## Reference map

Read [references/commands.md](references/commands.md) when command details,
output layout, or validation behavior matter.

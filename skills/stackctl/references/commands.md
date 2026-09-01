# stackctl Command DAG

Makefile-styled command reference. This is not a GNU Make file; it is a compact
map of the stackctl command paths the agent should follow.

```makefile
DASHBOARDS ?= dashboards
DATA ?= grafana-data
SEARCH ?= <search query>
DASHBOARD ?= <dashboard>
DASHBOARD_FILE ?= $(DASHBOARDS)/$(DASHBOARD).yaml
RAW_DASHBOARD ?= $(DASHBOARDS)/$(DASHBOARD).json
DATASOURCE ?= <datasource>
PANEL ?= <panel title>
PANEL_SLUG ?= <panel-slug>
TOPIC ?= <topic>
VARS ?= key=value
FROM ?= 1h
STEP ?= 1m
QUERY ?= <query>
EXPORT_DIR ?= $(DATA)/$(TOPIC)/$(PANEL_SLUG)

# Target: commands — choose the stackctl path that matches the user task.
commands: discover panel-inspection dashboard-roundtrip promql-query report

# Target: discover — find datasources, export a slim dashboard, list panels.
discover:
	@stackctl datasources
	@stackctl export "$(SEARCH)" --outdir $(DASHBOARDS)
	@stackctl panels $(DASHBOARD_FILE)
	? Use exact panel titles from this output when names are ambiguous.

# Target: variables — resolve Grafana dashboard variables iteratively.
variables: discover
	@stackctl vars $(DASHBOARD_FILE) datasource="$(DATASOURCE)"
	@stackctl vars $(DASHBOARD_FILE) datasource="$(DATASOURCE)" $(VARS)
	? Feed resolved values back as key=value until panel variables are concrete.

# Target: panel-inspection — collect live panel data through Grafana.
panel-inspection: variables export-panel read-summary

export-panel: variables
	@stackctl inspect $(DASHBOARD_FILE) "$(PANEL)" \
	  datasource="$(DATASOURCE)" $(VARS) \
	  --from=$(FROM) --step=$(STEP) \
	  --export=$(EXPORT_DIR)

read-summary: export-panel
	$ read $(EXPORT_DIR)/summary.yaml
	? summary.yaml contains metadata, variables, panel queries, per-series stats,
	? and file references. Read CSV files only when the summary is insufficient.

read-csv: read-summary
	$ read $(EXPORT_DIR)/all.csv
	? Use all.csv for bulk comparisons. Use per-series NNN-*.csv files for deeper
	? analysis of one metric label set.

# Target: dashboard-roundtrip — prepare a dashboard for safe import.
dashboard-roundtrip: raw-export interpolate validate dry-run-import

raw-export:
	@stackctl export "$(DASHBOARD)" --raw --folder-meta --outdir $(DASHBOARDS)
	? Use raw exports with folder metadata for files that may be uploaded again.

interpolate: raw-export
	@stackctl dashboard interpolate $(RAW_DASHBOARD) \
	  --datasource="$(DATASOURCE)" \
	  --vars='$(VARS)' \
	  --from=$(FROM) --step=$(STEP) \
	  --format=yaml
	? Preview interpolation when queries use $var, $${var:regex}, $${var:pipe},
	? multi-select variables, or All values.

validate: interpolate
	@stackctl dashboard validate $(RAW_DASHBOARD) \
	  --datasource="$(DATASOURCE)" \
	  --vars='$(VARS)' \
	  --from=$(FROM) --step=$(STEP) \
	  --format=yaml
	? Validation errors include panel title, refId, interpolated query, and the
	? Prometheus error. Fix the dashboard query, then validate again.

dry-run-import: validate
	@stackctl import $(RAW_DASHBOARD) --dry-run
	? Confirm folder and overwrite behavior before upload. Use --folder-uid or
	? --folder-id only when intentionally moving the dashboard.

upload: dry-run-import
	@stackctl import $(RAW_DASHBOARD) --overwrite
	? Run only when the user clearly intends to upload.

# Target: promql-query — run ad-hoc live PromQL through Grafana.
promql-query:
	@stackctl promql '$(QUERY)' "$(DATASOURCE)" \
	  --from=$(FROM) --step=$(STEP) --format=yaml
	? Raw promql does not simulate dashboard interpolation. For edited dashboards,
	? use interpolate and validate instead.

# Target: output-layout — remember inspect --export file meanings.
output-layout:
	? summary.yaml = metadata, resolved variables, queries, stats, file references.
	? all.csv = long-format rows: timestamp,series,value.
	? NNN-*.csv = one time series per file: timestamp,value plus label comments.

report:
	? Include dashboard, datasource, panel or query, variables, time range, step,
	? export path, caveats, and failed queries. Keep large data in files and report
	? only relevant values or comparisons.
```

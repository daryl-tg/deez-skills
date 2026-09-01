# kolint

CLI tool that compares YAML config files against Go
struct schemas parsed from ko struct tags (`yaml`,
`default`, `required`, `env`). It reports missing
fields as `DEFAULT`, `REQUIRED`, or `OPTIONAL`,
unknown keys as `UNKNOWN`, explicit default-valued
overrides as `REDUNDANT`, and in report mode config
that Go code never reads as `UNUSED`.

## Install

```bash
go install git.kiyotaka.dev/go-backend/kolint/cmd/kolint@latest
```

Verify: `kolint --version`

## Findings

Report mode can emit:

- `DEFAULT` — field absent from YAML, silently gets
  this value at runtime.
- `REQUIRED` — field absent, no default; ko loading
  will fail.
- `OPTIONAL` — field absent, no default, not
  required.
- `UNKNOWN` — YAML key with no matching struct field
  (typo or stale config).
- `REDUNDANT` — YAML sets a scalar value identical to
  the struct default.
- `UNUSED` — YAML key maps to a schema field that the
  static Go usage analysis does not see any code
  reading.

Annotate mode can surface `DEFAULT`, `REQUIRED`,
`OPTIONAL`, `UNKNOWN`, and `REDUNDANT`. `UNUSED` is
report-only because annotate mode does not run usage
analysis.

## Usage

### Report mode (default)

```bash
kolint config.yaml
kolint --type Config --package ./internal/director config.yaml
```

When a `.kolint.yml` exists and no files are given on
the command line, it is used automatically:

```bash
kolint
```

### Annotate mode

Inject comments into the YAML. Output goes to stdout
unless `--write` is used:

```bash
kolint --annotate config.yaml
kolint --annotate --write config.yaml
```

Absent defaults, required fields, and optional fields
appear as commented-out keys. Unknown keys get inline
comments. Scalar values that match struct defaults get
`= default`. `UNUSED` findings do not appear in
annotate mode.

### Flags

| Flag | Default | Purpose |
|------|---------|---------|
| `--type` | `Config` | Go type name to audit against |
| `--package` | `./...` | Go package pattern to load |
| `--root` | — | Dot-separated YAML path to config subtree (e.g. `config` for Helm values) |
| `--annotate` | off | Emit managed commented YAML stubs |
| `--write` | off | Rewrite YAML files in place; implies annotate |
| `--ignore` | — | Comma-separated glob patterns for YAML paths to skip |
| `--build-flags` | — | Go build flags passed to the package loader |

## Project config

Drop a `.kolint.yml` in the repo root:

```yaml
type: Config
package: ./internal/director
annotate: true
files:
  - path: config.dev.yaml
  - path: config.perftest.yaml
  - path: deploy/values.yaml
    root: config
```

CLI flags override config file values. `files` entries
only set `path` and optional `root`; `type`,
`package`, `ignore`, and `annotate` apply to the
whole run. When no YAML files are given on the command
line, `files` entries are expanded and used.

## Workflow

1. Run `kolint` and read the report.

2. Fix `REQUIRED` and `UNKNOWN` findings first. They
   usually indicate broken config or typos.

3. For each `DEFAULT` or `OPTIONAL` finding, decide
   whether to add the field to YAML so the config is
   self-documenting, or leave it implicit.

4. For each `UNUSED` finding, confirm that the field
   is truly dead config before deleting it. The signal
   is static-analysis based, so treat it as a drift
   check, not as proof.

5. For each `REDUNDANT` finding, decide whether to
   keep the explicit value for documentation or remove
   it to reduce noise.

6. Commit `.kolint.yml` and any config changes, then
   re-run `kolint` after adding or removing config
   struct fields.

## Ignore patterns

Skip YAML paths that can't be introspected (custom
unmarshalers, free-form maps):

```bash
kolint --ignore "*.kafka.options,*.auth.credentials" config.yaml
```

Patterns use glob matching against dot-separated YAML
paths. In `.kolint.yml`:

```yaml
ignore:
  - "*.kafka.options"
  - "*.auth.credentials"
```

## Helm values

For Helm charts where the app config lives under a
key:

```bash
kolint --root config values.yaml
```

Or in `.kolint.yml`:

```yaml
files:
  - path: charts/my-app/values.yaml
    root: config
```

## Multiple config types

When a project has separate config structs (e.g. main
config and test config), audit each file with the
correct type:

```bash
kolint --type Config --package ./internal/director config.yaml
kolint --type Config --package ./internal/testkit config.test.yaml
```

## AGENTS.md

After setting up kolint, add a section to the
project's AGENTS.md documenting:

- Which struct each config file is audited against.
- How to run the audit (`kolint` with no args if
  `.kolint.yml` exists).
- That config files should be re-audited after struct
  changes.

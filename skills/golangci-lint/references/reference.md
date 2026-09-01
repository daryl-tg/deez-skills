# golangci-lint

## Reference Documentation

The golangci-lint website uses Hugo templates that
don't render well when fetched. Use raw GitHub sources:

- **Complete config reference** (4000+ lines):
  `https://raw.githubusercontent.com/golangci/golangci-lint/HEAD/.golangci.reference.yml`
- **Linters list**: `golangci-lint help linters`
- **Migration guide** (v1 → v2):
  `https://raw.githubusercontent.com/golangci/golangci-lint/HEAD/docs/content/docs/product/migration-guide.md`

Fetch the reference yml before writing the config file.

## Install

```bash
golangci-lint --version 2>/dev/null || \
  curl -sSfL https://raw.githubusercontent.com/golangci/golangci-lint/HEAD/install.sh \
  | sh -s -- -b $(go env GOPATH)/bin
```

## Config

Check the installed version first — v2 uses a different
config format:

- `version: "2"` required at top
- `linters.settings` instead of `linters-settings`
- formatters (gofmt, goimports, gci, gofumpt) move to
  `formatters` section
- gosimple + stylecheck merge into `staticcheck`

Start with all linters enabled, then disable what
doesn't apply:

```yaml
version: "2"

linters:
  default: all
  disable:
    # Too strict for most projects
    - exhaustruct
    # Deprecated in favor of wsl_v5
    - wsl
    # Needs explicit policy config, useless without it
    - depguard
  settings:
    cyclop:
      max-complexity: 10
    gocyclo:
      min-complexity: 10
    gocognit:
      min-complexity: 15
    govet:
      enable-all: true
    errcheck:
      check-type-assertions: true
    lll:
      line-length: 120
    nestif:
      min-complexity: 4
    staticcheck:
      checks:
        - "all"
  exclusions:
    generated: strict
    rules:
      - path: '(.+)_test\.go'
        linters:
          - errcheck
          - gosec
          - goconst

formatters:
  enable:
    - gofmt
```

## Run

```bash
golangci-lint run ./...
golangci-lint run --fix ./...
go build ./...  # --fix can break imports
```

If certain linters produce too many false positives,
disable them with a comment explaining why.

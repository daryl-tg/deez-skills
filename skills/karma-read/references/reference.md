# karma-read

Parses logs produced by [karma-go](https://github.com/reconquest/karma-go) into NDJSON.

Karma-go logs are multi-line: a timestamp line followed by a UTF-8 tree of context key-value pairs. `karma-read` reconstructs that structure as JSON so you can pipe it through `jq`, `grep`, or any NDJSON-aware tool.

## When to use

Use `karma-read` whenever you see log output like this:

```
2026-03-02T08:08:00.00177Z ERROR ws: rate limit exceeded
                                 └─ user: id=kscript-backend
                                    ├─ id: 177243887914770
                                    ├─ request_id: add20fe9-beda-49ca-8670-392571806155
                                    └─ method: StreamPoints
```

These tree markers (`├─`, `└─`, `│`) are karma-go's format. Raw `grep`/`jq` can't parse them because entries span multiple lines and context is encoded visually.

## Usage

```bash
# from stdin
<command-that-produces-logs> | karma-read --flat

# from files
karma-read --flat /path/to/logfile.log

# multiple files (processed in order)
karma-read --flat file1.log file2.log
```

**Always prefer `--flat`** unless you specifically need the nested tree structure. Flat mode produces one JSON object per entry with a `context` object containing all key-value pairs — much easier to filter with `jq`.

## Output formats

### Flat mode (`--flat`) — use this by default

```bash
karma-read --flat <<< "$logs"
```

Produces:
```json
{"ts":"...","level":"ERROR","msg":"ws: rate limit exceeded","context":{"user":"id=kscript-backend","id":177243887914770,"request_id":"add20fe9-...","method":"StreamPoints"}}
```

- `context` contains all key-value pairs from the tree, flattened
- Values are auto-typed: integers, floats, booleans, embedded JSON objects, or strings
- Tree nodes that aren't key-value pairs appear in a `reasons` array instead

### Nested mode (default, no flag)

```bash
karma-read <<< "$logs"
```

Produces:
```json
{"ts":"...","level":"ERROR","msg":"ws: rate limit exceeded","children":[{"text":"user: id=kscript-backend","children":[{"text":"id: 177243887914770"},{"text":"method: StreamPoints"}]}]}
```

Preserves the full tree hierarchy. Use this only when parent-child relationships between context nodes matter.

## Common patterns with jq

```bash
# Filter entries by level
karma-read --flat app.log | jq 'select(.level == "ERROR")'

# Extract a specific context field
karma-read --flat app.log | jq -r '.context.request_id // empty'

# Filter by context value
karma-read --flat app.log | jq 'select(.context.method == "StreamPoints")'

# Count entries by level
karma-read --flat app.log | jq -r '.level' | sort | uniq -c

# Entries in a time range
karma-read --flat app.log | jq 'select(.ts >= "2026-03-02T08:00:00" and .ts <= "2026-03-02T09:00:00")'

# Pretty-print one entry
karma-read --flat app.log | head -1 | jq .
```

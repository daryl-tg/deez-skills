# Log and karma-go usage guide

This skill covers how to use `git.kiyotaka.dev/go-backend/log`
and `github.com/reconquest/karma-go` together. Read it before
writing any logging or error-handling code.

## Imports

```go
import (
    "git.kiyotaka.dev/go-backend/log"
    "github.com/reconquest/karma-go"
)
```

The log package re-exports nothing from karma. You always need
both imports when attaching structured context or wrapping
errors.

## Picking the right log function

There are three function families per level, each taking
different first arguments. The level names are Fatal, Error,
Warning, Info, Debug, Trace.

### `*f` — plain formatted message, no context

```go
log.Infof("server listening on port %d", port)
log.Errorf("connection closed unexpectedly")
```

Use when the message stands alone and there is no error value
or structured context to attach.

### `*x` — structured context or error chain

For error levels (Fatal, Error, Warning), the first argument
is an `error`:

```go
log.Errorx(err, "connect to database")
log.Warningx(err, "retry limit reached for %s", endpoint)
```

For non-error levels (Info, Debug, Trace), the first argument
is a `*karma.Context`:

```go
log.Infox(
    karma.Describe("user_id", userID).
        Describe("action", "login"),
    "user authenticated",
)
```

Pass `nil` as the context when you have no fields but want to
use the `*x` form for consistency. But prefer `*f` in that
case — the linter flags `Errorx(nil, "static message")` as a
probable mistake.

### `*ln` — println-style, no formatting

```go
log.Infoln("startup complete")
```

Rarely needed. Prefer `*f` for new code.

## Writing log messages

Messages are lowercase and use infinitive form. The level
already communicates failure, so words like "failed to",
"unable to", "error" are redundant.

Good:
```go
log.Errorx(err, "connect to postgresql")
log.Infof("process batch of %d records", len(records))
```

Bad:
```go
log.Errorf("Failed to connect to postgresql")
log.Errorf("error connecting to postgresql: %v", err)
```

The `log-linter` tool (in `cmd/log-linter`) enforces these
conventions. Run it with `go run ./cmd/log-linter ./...` or
use the golangci-lint plugin.

## Error wrapping with karma

karma-go builds hierarchical error chains. Use it instead of
`fmt.Errorf("...: %w", err)`.

### Basic wrapping

```go
err := db.Ping()
if err != nil {
    return karma.Format(err, "ping database")
}
```

This produces an error whose `.Error()` reads:
```
ping database
└─ connection refused
```

### Adding key-value context

```go
return karma.
    Describe("host", host).
    Describe("port", port).
    Format(err, "connect to postgresql")
```

Output:
```
connect to postgresql
├─ connection refused
├─ host: db.example.com
└─ port: 5432
```

### Context without an error

When you want structured fields on an informational message:

```go
ctx := karma.Describe("file", path).
    Describe("size", size)
log.Infox(ctx, "upload complete")
```

### Chaining context across call boundaries

Return wrapped errors up the stack. Each layer adds its own
context:

```go
// in repository layer
func (r *Repo) GetUser(id int) (*User, error) {
    row := r.db.QueryRow("SELECT ...", id)
    if err := row.Scan(&u); err != nil {
        return nil, karma.
            Describe("user_id", id).
            Format(err, "scan user row")
    }
    return &u, nil
}

// in handler layer
func handleGetUser(w http.ResponseWriter, r *http.Request) {
    user, err := repo.GetUser(id)
    if err != nil {
        log.Errorx(err, "handle get user request")
        http.Error(w, "internal error", 500)
        return
    }
    // ...
}
```

The final log line contains the full chain:
```
handle get user request
└─ scan user row
   ├─ sql: no rows in result set
   └─ user_id: 42
```

### errors.Is / errors.As compatibility

karma errors implement the `Unwrap() error` interface, so
standard library checks work:

```go
if errors.Is(err, sql.ErrNoRows) {
    // ...
}
```

## Child loggers

Create a logger that carries context across many log calls.
Useful for request-scoped or connection-scoped logging.

```go
reqLog := log.GetLogger().WithFields(map[string]any{
    "request_id": reqID,
    "method":     r.Method,
    "path":       r.URL.Path,
})
reqLog.Infof("handle request")
reqLog.Debugf("parsed body successfully")
```

Every message from `reqLog` includes request_id, method, and
path without repeating them at each call site.

Child loggers can also override the level:

```go
verboseLog := log.GetLogger().WithDebug()
verboseLog.Debugf("this logs even if parent is at Info")
```

Nesting works — context accumulates:

```go
connLog := log.GetLogger().WithField("conn_id", connID)
reqLog := connLog.WithField("request_id", reqID)
// reqLog carries both conn_id and request_id
```

## Hooks

Hooks run after the log line is written. They receive the
karma hierarchy and the level. Register them on a logger
instance or on the package-level default:

```go
log.AddHook(log.LevelError, func(
    entry karma.Hierarchical,
    level log.Level,
) error {
    if errors.Is(entry, context.DeadlineExceeded) {
        return sendTimeoutAlert(entry)
    }
    return nil
})
```

The `minLevel` argument is the *least severe* level that
triggers the hook. `LevelError` means it fires for Error and
Fatal (lower numeric values), not for Warning or Info.

Hook panics are caught and written to stderr. Hooks must not
call back into the same logger — there is no re-entrancy
guard beyond the panic recovery.

## Encodings

Two output formats, set globally or per logger:

```go
log.SetEncoding(log.EncodingJSON)
log.SetEncoding(log.EncodingText)
```

JSON uses a code-generated easyjson marshaler. Text renders
the karma tree with box-drawing characters, indented to align
with the timestamp prefix.

Pick JSON for machine consumption (log aggregators, structured
query). Pick Text for local development and human reading.
Text is the default.

## Levels

From most to least severe:

| Level       | Numeric | Meaning                        |
|-------------|---------|--------------------------------|
| LevelFatal  | 0       | Unrecoverable, calls os.Exit  |
| LevelError  | 1       | Needs investigation            |
| LevelWarning| 2       | Handled but concerning         |
| LevelInfo   | 3       | Normal operations (default)    |
| LevelDebug  | 4       | Debugging detail               |
| LevelTrace  | 5       | Very verbose execution traces  |

The logger's level is the *maximum* it will emit. Setting
`LevelInfo` means Fatal, Error, Warning, and Info all pass
through. Debug and Trace are suppressed.

Guard expensive debug computations with an explicit check:

```go
if log.GetLevel() >= log.LevelDebug {
    log.Debugf("state dump: %s", expensiveSerialize())
}
```

## Common mistakes the linter catches

1. Redundant prefixes:
   `log.Errorf("failed to connect")` →
   `log.Errorf("connect")`

2. Formatting errors into the message:
   `log.Errorf("connect: %v", err)` →
   `log.Errorx(err, "connect")`

3. Using fmt.Errorf for wrapping:
   `fmt.Errorf("parse: %w", err)` →
   `karma.Format(err, "parse")`

4. Nil error with static message:
   `log.Errorx(nil, "something happened")` —
   probably a bug, pass an actual error or use `*f`.

Run `go run ./cmd/log-linter -fix ./...` to auto-fix
issues 1–3.

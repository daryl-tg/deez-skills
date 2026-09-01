# docopt-go Conventions

## Usage String

Declare as a package-level `var` block alongside `version`.
Embed the version at the start of the usage string:

```go
var (
    version = "[manual build]"
    usage   = "mycommand " + version + `

Usage:
  mycommand [options] serve
  mycommand [options] migrate up
  mycommand -h | --help
  mycommand --version

Options:
  -c --config <path>  Config file. [default: /etc/mycommand.yaml]
  --debug             Enable debug mode.
  -h --help           Show this screen.
  --version           Show version.
`
)
```

## Arguments Struct

Bind all arguments to a single exported `Arguments` struct
using `docopt:"..."` tags. Follow this naming convention:

- **`Mode*`** — subcommands (`bool`)
- **`Value*`** — options/positionals that carry a value
  (`string`, `int`, `float64`)
- **`Flag*`** — boolean switches

```go
type Arguments struct {
    ModeServe   bool   `docopt:"serve"`
    ModeMigrate bool   `docopt:"migrate"`
    ModeUp      bool   `docopt:"up"`

    ValueConfig string `docopt:"--config"`

    FlagDebug bool `docopt:"--debug"`
}
```

## Parsing

Two equivalent approaches:

```go
// ParseDoc — uses os.Args, no automatic --version handling
doc, err := docopt.ParseDoc(usage)
if err != nil {
    panic(err)
}
err = doc.Bind(&args)

// ParseArgs — pass nil for os.Args, version enables --version
opts, err := docopt.ParseArgs(usage, nil, version)
if err != nil {
    panic(err)
}
err = opts.Bind(&args)
```

Use `ParseArgs` when the binary has a meaningful version
string. Use `ParseDoc` otherwise.

## Subcommand Dispatch

Use a `switch` on the mode bools after parsing:

```go
switch {
case args.ModeServe:
    err = HandleServe(args, config)
case args.ModeMigrate:
    err = HandleMigrate(args, config)
}

if err != nil {
    log.Fatalln(err)
}
```

Nested subcommands (e.g. `migrate up`) get their own
`Mode*` bool fields and are tested inside the parent
handler or combined in the switch.

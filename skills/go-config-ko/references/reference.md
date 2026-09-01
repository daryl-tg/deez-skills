# ko configuration guide

This skill covers how to define config structs, use ko
struct tags, and call `ko.Load`. Read it before writing any
configuration-related code.

## Import

```go
import "github.com/kovetskiy/ko"
```

For YAML configs (the common case), also import the
unmarshaller:

```go
import "gopkg.in/yaml.v3"
```

## Defining config structs

Every config field should carry three pieces of information
through struct tags: the serialization key, whether the field
is required, and what its default or env fallback is.

```go
type Config struct {
    Listen string `yaml:"listen" required:"true" default:":8080"`
    DBUrl  string `yaml:"db_url" required:"true" env:"DB_URL"`
    Debug  bool   `yaml:"debug"  default:"false" env:"DEBUG"`
}
```

Do not define Go constants for default values and apply them
in helper methods. Put the default directly in the struct tag.
ko handles this at load time.

Wrong:

```go
const defaultPort = 8080

type Config struct {
    Port int `yaml:"port"`
}

func (c *Config) PortOrDefault() int {
    if c.Port == 0 {
        return defaultPort
    }
    return c.Port
}
```

Right:

```go
type Config struct {
    Port int `yaml:"port" default:"8080"`
}
```

## Tags

| Tag | Value | Meaning |
|-----|-------|---------|
| `required` | `"true"` | Error if zero after all fallbacks |
| `default` | string | Applied when zero; parsed via yaml.Unmarshal |
| `env` | env var name | Read from env when zero after file unmarshal |

Evaluation order: file → env → default → required check. A
field with both `default` and `required` never fails the
required check.

## Loading

```go
var cfg Config
err := ko.Load("config.yaml", &cfg, yaml.Unmarshal)
```

The default unmarshaller is `toml.Unmarshal`. Pass
`yaml.Unmarshal` or `json.Unmarshal` explicitly when the
file format differs.

### Optional config file

When the config file may not exist and defaults plus env vars
are sufficient:

```go
err := ko.Load(path, &cfg, yaml.Unmarshal, ko.RequireFile(false))
```

## Nested structs and required propagation

Required checks propagate into a child struct only when the
parent field is also `required:"true"`. This means optional
sections that are entirely absent do not trigger errors on
their children.

```go
type Config struct {
    // Server is required; its children are validated.
    Server struct {
        Host string `yaml:"host" required:"true"`
        Port int    `yaml:"port" required:"true" default:"443"`
    } `yaml:"server" required:"true"`

    // Cache is optional. When absent, Listen is not checked.
    // When any field inside Cache is set, Listen is still
    // not checked because Cache itself is not required.
    Cache struct {
        Listen string `yaml:"listen" required:"true" default:":6379"`
    } `yaml:"cache"`
}
```

Use this pattern to model sections that are entirely optional
but internally consistent when present. Mark the parent
`required:"false"` (or omit the tag) and mark the children
`required:"true"`. ko validates children only when the parent
is non-zero.

## Inline structs for grouping

Use anonymous or named inline sections to group related
config without extra YAML nesting:

```go
type Config struct {
    GRPC struct {
        Listen         string `yaml:"listen"           required:"true" default:":4000"`
        MaxRecvMsgSize int    `yaml:"max_recv_msg_size" required:"true" default:"268435456"`
    } `yaml:"grpc" required:"true"`
}
```

## Slices

ko validates each element of a slice when the parent is
required:

```go
type Route struct {
    Path    string `yaml:"path"    required:"true"`
    Backend string `yaml:"backend" required:"true"`
}

type Config struct {
    Routes []Route `yaml:"routes" required:"true"`
}
```

## Maps

Use pointer values in maps. Non-pointer map values are not
addressable, so ko cannot set defaults or env fallbacks on
their fields:

```go
// Good: pointer values
type Config struct {
    Workers map[string]*WorkerConfig `yaml:"workers"`
}

// Bad: ko returns "target field is not addressable"
type Config struct {
    Workers map[string]WorkerConfig `yaml:"workers"`
}
```

## Pointer fields

Use pointers when "not set" and "zero" are different:

```go
type Config struct {
    Verbose *bool `yaml:"verbose" default:"false"`
}
```

Without the file setting `verbose`, ko allocates a `*bool`
pointing to `false`. Without the default tag, the pointer
stays nil — the caller can tell nothing was configured.

## Environment variables

The `env` tag reads a value when the field is zero after
file unmarshalling. Env values are parsed through
`yaml.Unmarshal`, so `"true"`, `"42"`, and `"[1,2,3]"` all
work.

```go
type Config struct {
    Port    int    `yaml:"port"    env:"PORT"    default:"8080"`
    Workers int    `yaml:"workers" env:"WORKERS" default:"4"`
    DSN     string `yaml:"dsn"     env:"DSN"     required:"true"`
}
```

Precedence: file value wins over env, env wins over default.

## Complex defaults

Default values go through `yaml.Unmarshal`, so you can
express durations, lists, and nested values:

```go
type Config struct {
    Timeout  string   `yaml:"timeout"  default:"30s"`
    Retries  int      `yaml:"retries"  default:"3"`
    Backends []string `yaml:"backends" default:"[localhost:8001, localhost:8002]"`
}
```

## Full example

```go
type GRPCConfig struct {
    Listen         string `yaml:"listen"            required:"true" default:":4000"`
    MaxRecvMsgSize int    `yaml:"max_recv_msg_size" required:"true" default:"268435456"`
    MaxSendMsgSize int    `yaml:"max_send_msg_size" required:"true" default:"268435456"`
}

type Config struct {
    Debug bool `yaml:"debug" env:"DEBUG" default:"false"`

    GRPC GRPCConfig `yaml:"grpc" required:"true"`

    Database struct {
        URL            string `yaml:"url"              required:"true" env:"DB_URL"`
        MaxConnections int    `yaml:"max_connections"  required:"true" default:"20"`
    } `yaml:"database" required:"true"`

    Cache struct {
        Enabled bool   `yaml:"enabled" default:"false"`
        Address string `yaml:"address" env:"REDIS_ADDR"`
    } `yaml:"cache"`
}

func LoadConfig(path string) (*Config, error) {
    var cfg Config
    err := ko.Load(path, &cfg, yaml.Unmarshal)
    if err != nil {
        return nil, err
    }
    return &cfg, nil
}
```

## Common mistakes

1. **Manual defaults in code instead of tags.** Do not define
   const values and apply them in getter methods. Use
   `default:"value"` on the struct field.

2. **Missing `required` on parent struct.** If only the child
   field says `required:"true"` but the parent struct field
   does not, ko skips validation when the parent is zero.

3. **Non-pointer map values.** ko cannot write defaults or env
   values into non-pointer map entries. Use `map[K]*V`.

4. **Wrapping with fmt.Errorf.** Use `karma.Format(err, ...)`
   for error wrapping, not `fmt.Errorf("...: %w", err)`.

5. **Forgetting the unmarshaller argument.** `ko.Load` uses
   TOML by default. Pass `yaml.Unmarshal` explicitly for YAML
   files.

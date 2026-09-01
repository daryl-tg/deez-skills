## Taskfile Basics

Every Taskfile starts with a version key. Always use
version 3:

```yaml
version: '3'
```

File is named `Taskfile.yml` by default. Alternatives:
`Taskfile.yaml`, `Taskfile.dist.yml`, or a custom name
via `task --taskfile Custom.yml`.

## Task Structure

```yaml
version: '3'

vars:
  GLOBAL_VAR: value

env:
  GLOBAL_ENV: value

tasks:
  task-name:
    desc: Short description (shown in --list)
    summary: |
      Longer multi-line description
      shown with --summary task-name
    dir: ./subdir          # working directory
    deps: [other-task]     # parallel dependencies
    cmds:
      - command-one
      - command-two
    vars:
      LOCAL_VAR: value
    env:
      LOCAL_ENV: value
    sources:
      - src/**/*.go        # fingerprint inputs
    generates:
      - bin/app            # expected outputs
    silent: true           # suppress echo
    internal: true         # hide from --list
    platforms: [linux, darwin]
```

Short syntax for simple tasks:

```yaml
tasks:
  build: go build -v -o ./app .
```

## Naming

Use kebab-case for task names: `do-something-fancy`,
not `do_something_fancy`.

## Variables and Templating

Variables use Go template syntax: `{{.VAR_NAME}}`

```yaml
vars:
  GREETING: Hello
tasks:
  greet:
    cmds:
      - echo "{{.GREETING}}"
```

Dynamic variables from shell:

```yaml
vars:
  GIT_COMMIT:
    sh: git rev-parse --short HEAD
```

Set variables from CLI: `task build VERSION=1.0.0`

## Environment Variables

Global or per-task `env:` block. Load from dotenv:

```yaml
dotenv: ['.env', '{{.ENV}}/.env']
```

## Dependencies

```yaml
tasks:
  build:
    deps: [generate, lint]
    cmds:
      - go build ./...
```

Deps run in parallel. Pass vars to deps:

```yaml
deps:
  - task: setup
    vars: { ENV: production }
```

## Calling Other Tasks

```yaml
cmds:
  - task: other-task
    vars: { KEY: value }
```

## Includes

Import tasks from other files with namespacing:

```yaml
includes:
  docker: ./DockerTasks.yml
  docs:
    taskfile: ./docs/Taskfile.yml
    dir: ./docs
    optional: true
  utils:
    taskfile: ./Utils.yml
    flatten: true    # merge into root namespace
    internal: true   # hide namespace from --list
```

Pass variables to included files:

```yaml
includes:
  backend:
    taskfile: ./Docker.yml
    vars:
      IMAGE: backend
```

Exclude specific tasks: `excludes: [task-name]`

## Aliases

```yaml
includes:
  generate:
    taskfile: ./Generate.yml
    aliases: [gen]
```

Task-level aliases:

```yaml
tasks:
  generate:
    aliases: [gen]
    cmds: [go generate ./...]
```

## Loops

```yaml
# Static list
cmds:
  - for: ['a.txt', 'b.txt']
    cmd: cat {{.ITEM}}

# Over a variable
vars:
  FILES: foo.txt bar.txt
cmds:
  - for: { var: FILES }
    cmd: cat {{.ITEM}}

# Custom split
cmds:
  - for: { var: CSV, split: ',' }
    cmd: echo {{.ITEM}}

# Over sources/generates
cmds:
  - for: sources
    cmd: cat {{.ITEM}}
```

## Wildcards

```yaml
tasks:
  start:*:
    vars:
      SERVICE: '{{index .MATCH 0}}'
    cmds:
      - docker start {{.SERVICE}}
```

Call: `task start:redis`

## Platforms

Restrict tasks or commands to OS/arch:

```yaml
tasks:
  build:
    platforms: [windows/amd64, darwin]
    cmds:
      - cmd: echo 'Windows/Mac only'
        platforms: [windows, darwin]
      - echo 'All platforms'
```

## Preconditions and Status

```yaml
tasks:
  deploy:
    preconditions:
      - test -f docker-compose.yml
      - sh: '[ "{{.ENV}}" != "" ]'
        msg: ENV is required
    status:
      - test -f bin/app
    cmds:
      - docker compose up -d
```

`status` commands: if all return 0, task is up-to-date.

## Sources/Generates (Fingerprinting)

```yaml
tasks:
  build:
    sources:
      - src/**/*.go
      - go.mod
    generates:
      - bin/app
    cmds:
      - go build -o bin/app ./cmd/app
```

Task skips if sources haven't changed. Method is
checksum by default; use `method: timestamp` for
mtime comparison.

## Defer

Cleanup commands that run after task completes
(even on failure), in reverse order:

```yaml
cmds:
  - mkdir -p tmpdir/
  - defer: rm -rf tmpdir/
  - echo 'Work in tmpdir/'
```

## Interactive Prompts

```yaml
tasks:
  deploy:
    requires:
      vars:
        - name: ENVIRONMENT
          enum: [dev, staging, prod]
        - VERSION
    cmds:
      - echo "Deploying {{.VERSION}} to {{.ENVIRONMENT}}"
```

Prompts user if variable not set. Requires TTY.

## Watch Mode

```yaml
tasks:
  build:
    watch: true
    sources:
      - '**/*.go'
    cmds:
      - go build ./...
```

Or from CLI: `task --watch build`

## Shell Options

```yaml
version: '3'
set: [pipefail]
shopt: [globstar]
```

Per-task or per-command override supported.

## CLI Reference

```
task [flags] [tasks...] [-- CLI_ARGS...]

task --init           # create Taskfile.yml
task --list / -l      # list tasks with desc
task --list-all / -la # list all tasks
task --summary <task> # show task summary
task --watch / -w     # watch mode
task --dry            # dry run
task --force / -f     # ignore up-to-date
task --parallel / -p  # run listed tasks in parallel
task --dir / -d <dir> # run from directory
task -t <file>        # use specific Taskfile
task -g               # use global ~/Taskfile.yml
task --json           # JSON output (with --list)
task --silent / -s    # suppress task echo
task --verbose / -v   # verbose output
task --status         # exit non-zero if not up-to-date
task --completion <shell>  # shell completions
```

`{{.CLI_ARGS}}` captures everything after `--`.

## Configuration (.taskrc.yml)

Global config in `$XDG_CONFIG_HOME/task/.taskrc.yml`,
`~/.taskrc.yml`, or project-local `.taskrc.yml`.
Project overrides home overrides XDG.

```yaml
verbose: true
silent: false
color: true
failfast: true
concurrency: 2
```

## References

Pass complex types without string conversion:

```yaml
vars:
  LIST: [A, B, C]
cmds:
  - task: other
    vars:
      ITEMS:
        ref: .LIST
```

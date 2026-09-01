---
name: ancient-shell-style
description: >-
  Lint, format, test, review, document, and harden maintained Bash and shell
  scripts with ShellCheck, shfmt, shdoc, and test-runner.bash. Use for Bash,
  sh, shell scripts, shell libraries, shell tests, or turning one-liners into
  maintained scripts.
---

# Shell Style

## Scope

Use this workflow when the user asks to work on a
maintained Bash, sh, or shell script, a sourced
shell library, or a shell fragment that is about to
become a maintained script file.

Use it for Bash tests too. For Bash code, `test-runner.bash`
is the right default for unit, CLI, library, integration,
regression, and harness self-tests unless an existing repo
wrapper already owns the suite.

Not for ad hoc one-liners unless the task is to turn
them into a script.

## Workflow

1. Determine the shell dialect and whether each
   touched file is a standalone script, a sourced
   library, or a sourced data/config fragment. Keep
   the scope tight.
2. Make structural and documentation fixes first: wrong
   shell features, entrypoint shape, top-level layout,
   constants and globals, function naming and ordering,
   usage and option parsing helpers, file-level shdoc
   docs, public function docs, logging style, quoting,
   argv handling, stdout/stderr separation, temp file
   handling, traps, and control-flow points such as `cd`.
3. Before hard-coding external commands, APIs,
   redirects, or sourced local shell files, verify the
   dependency once and decide how failure should
   surface.
4. Format with `shfmt`, using an explicit dialect when
   needed.
5. Run `shellcheck` for the actual shell in use. Use
   `-x` when local sourced shell files are part of the
   contract. Treat warnings as review prompts, not
   blind rewrite orders.
6. After each non-trivial edit batch, re-run
   formatter, linter, and a parser check such as
   `bash -n` or `dash -n`.
7. Run `shdoc` for every touched maintained script or
   shell library. Read the generated Markdown and fix
   broken or misleading docs, missing sections, bad
   anchors, or misplaced tags before finishing.
8. When behavior changed, test through the repository
   shell harness. For new Bash suites, use
   `test-runner.bash` with `tests.sh`; do not invent
   ad hoc assertion scripts. Exercise at least one safe
   happy path and each touched mode, fallback, or
   cleanup path that matters.
9. In final notes, include whether `shdoc` passed. If
   the repo has no destination for generated docs,
   suggest an output command instead of inventing a
   path silently.
10. When the script has risky areas such as `eval`,
   background jobs, or unusual shell behavior, call
   them out explicitly in the final notes.

## Rules

- Declare the shell honestly.
- Keep scope to the requested shell files. Do not
  widen into sourced config or data files unless the
  contract changed or the user asked.
- Do not force script conventions such as `:main()`
  onto sourced data/config fragments.
- Quote expansions unless splitting or globbing is
  intentional.
- Keep top-level code declarative: uppercase config
  defaults, constants, function definitions, and a
  final `:main "$@"`.
- Prefer `:main()` as the script entrypoint.
- Prefix internal helpers with leading `:`.
- Put exposed reusable functions under an explicit
  namespace such as `tool:sync()`.
- Use extra `:` to group related helpers when useful,
  such as `:history:add()`.
- Prefer hyphens over underscores in function names.
- Avoid introducing new bare function names.
- Put uppercase env or config defaults near the top
  of the file.
- Make top-level constants uppercase and `readonly`
  when practical.
- Do not keep mutable runtime state in top-level
  globals.
- Use `:usage()` or `:help()` for non-trivial CLIs,
  usually with a heredoc.
- Put non-trivial flag parsing in `:parse-opts()` or
  an equivalent dedicated helper.
- Group functions by role or subsystem instead of
  sorting them alphabetically.
- Keep related helpers adjacent and order functions
  for reader comprehension.
- Declare `local` variables early in functions.
- Prefer `exit` in `:main()` and `return` in
  helpers.
- Verify external endpoints or commands before baking
  them into the script.
- If a file sources local shell files, prefer
  `shellcheck -x` with the actual shell.
- Treat `shdoc` as required verification for
  maintained scripts and shell libraries.
- Add file-level shdoc docs to maintained script and
  library files.
- Document exposed reusable functions with shdoc
  annotations placed directly above the function.
- Use shdoc tags in the right place: file-level tags
  at file top, function tags above functions.
- Keep internal helpers undocumented unless the same
  style is needed with `@internal`. Never leave a bare
  `@internal`; attach it to a real docblock for the
  internal function.
- Run `shdoc` and inspect the generated Markdown
  before finishing shell docs work.
- Keep stdout for data and stderr for diagnostics.
- Prefer a named `:cleanup()` helper over long inline
  trap bodies.
- Handle `cd`, temp dirs, cleanup traps, and
  background jobs explicitly.
- Treat ShellCheck findings as review prompts.
  Preserve correct trap capture, nameref APIs, and
  other deliberate behavior. Use narrow suppressions
  when the code is already correct.
- Avoid `eval`; if unavoidable, isolate it and
  document the contract.
- Under `set -euo pipefail`, handle probe commands
  whose non-zero exit can be expected, such as
  `systemctl is-active`, `grep -q`, or `pgrep`.
- Use `$(...)` instead of backticks.
- Re-run a parser check with the actual shell before
  finishing.
- Keep suppressions narrow, local, and justified.
- For Bash behavior tests, use `test-runner.bash` as
  the default wrapper and `tests.sh` assertions under it.
- Do not introduce Bats, shunit2, raw loops, or one-off
  assertion scripts unless that is already the repository
  harness or the user explicitly asked to replace it.
- Keep shared imports, setup, teardown, temp dirs,
  fixtures, custom suite options, and progress wiring in
  the test-runner wrapper/setup, not duplicated in each
  testcase.
- Test touched modes when safe, not only the easiest
  happy path.
- No decorative banners or separator noise in script
  output. Prefer plain labels and indentation for
  structure.
- Gate debug logging through a helper or verbosity
  flag.
- Log milestones, waits, state changes, and failures
  with concise action or state wording.
- When logs need context, prefix by subsystem,
  instance, or operation kind.

## Reference

Use ShellCheck for static analysis, shfmt for layout,
and shdoc for documentation verification. They
complement each other. They do not replace a design
review.

Testing policy is in [references/tests.md](references/tests.md).
The imported shell package catalog is in
[references/imports.md](references/imports.md). Read
the package catalog and the vendored package docs under
`vendor.bash/github.com/reconquest/...` before adding or
changing `import:use` calls, `vendor.bash/` dependencies,
test helper packages, or shell package mentions. Preserve
an existing working harness unless asked to migrate it.

### Recommended pass

Pick the dialect first, then run the tools with that
dialect.

```bash
shfmt -ln bash -w script.sh
shellcheck --shell=bash script.sh
bash -n script.sh
./script.sh --help >/dev/null
shdoc script.sh >/tmp/script.md
```

Read the generated Markdown before calling the docs
done. Fix the source annotations when the output has
missing file docs, missing functions, malformed
sections, wrong anchors, or misleading contract text.

If the script sources local files and you want
ShellCheck to follow them:

```bash
shellcheck -x --shell=bash script.sh
```

Preview formatter changes without writing:

```bash
shfmt -ln bash -d script.sh
```

Use the actual shell in the parser check. If you
changed a fallback, manual mode, trap, or temp-dir
path, exercise that path too.

### Scope and dependency guardrails

Keep shell style work focused on actual shell files.
A sourced `.conf` that only stores assignments is
usually data, not a place to force `:main()` or
helper naming.

Before hard-coding an external API or CLI assumption,
probe it once with `command -v`, `curl -I -L`, or a
small sample call. Then decide whether the script
needs a fallback, redirect handling, or a clearer
error.

### Preferred script shape

Keep top-level code small. Put uppercase
configuration, constants, function definitions, and
the final entrypoint call at the top level. Put real
flow inside functions.

Order functions for the reader, not alphabetically.
Group CLI helpers together, keep subsystem helpers
adjacent, and keep the final entrypoint call at the
bottom.

```bash
#!/usr/bin/env bash
set -euo pipefail

readonly CONFIG_DIR=${CONFIG_DIR:-$HOME/.config/mytool}
readonly VERBOSE=${VERBOSE:-0}

:usage() {
    cat <<EOF
Usage:
    mytool [options] <arg>
EOF
}

:parse-opts() {
    :
}

:cleanup() {
    :
}

:main() {
    local arg="${1:-}"
    trap :cleanup EXIT
    :parse-opts "$@"
    :
}

:main "$@"
```

### Output style

Do not use separator lines, banners, or repeated
punctuation such as `====`, `----`, or `*****` to
suggest structure in script output. Prefer short
labels and indentation.

Bad:

```bash
printf '%s\n' '===================='
printf '%s\n' 'Starting deploy'
printf '%s\n' '--------------------'
```

Good:

```bash
printf '%s\n' 'Starting deploy' >&2
printf '  %s\n' 'Building assets' >&2
printf '  %s\n' 'Uploading release' >&2
```

### Function naming style

Use one consistent shell naming style instead of
mixing bare names, underscores, and ad hoc prefixes.

Preferred pattern for standalone scripts:

```bash
:main() {
    :
}

:parse-args() {
    :
}

:cleanup-tmp() {
    :
}

:main "$@"
```

Preferred pattern for grouped internal helpers:

```bash
:history:add() {
    :
}

:cache:store() {
    :
}
```

Preferred pattern for exposed reusable helpers:

```bash
tool:sync() {
    :
}

tool:print-status() {
    :
}
```

Guidelines:

- use `:main()` as the default entrypoint
- use leading `:` for internal helpers
- use a namespace such as `tool:` for exposed helpers
- use extra `:` to group related helpers when useful
- prefer hyphens over underscores in function names
- keep `_` for cases where you are mirroring an
  external name or preserving an established API

### Strict-mode probe commands

Under `set -euo pipefail`, do not let normal
observation commands abort the script by accident.
Commands such as `systemctl is-active`, `grep -q`, or
`pgrep` often use non-zero exit status to mean "not
found" or "inactive", not "fatal error".

Bad:

```bash
services=$(systemctl is-active a.service b.service | paste -sd' ' -)
```

Better:

```bash
services=$(systemctl is-active a.service b.service 2>/dev/null || true)
services=$(paste -sd' ' <<<"$services")
```

Or branch explicitly with `if` or `case` when the
status itself matters.

### shellcheck

```bash
shellcheck script.sh
shellcheck --shell=sh script.sh
shellcheck --shell=bash script.sh
shellcheck --severity=warning script.sh
shellcheck -x script.sh
```

Auto-fix suggestions are available as a diff, but
review them before applying:

```bash
shellcheck -f diff script.sh | git apply
```

Inline directives:

```bash
# shellcheck disable=SC2086
printf '%s\n' $var

# shellcheck source=./lib/helpers.sh
source "$DIR/helpers.sh"
```

Keep suppressions narrow and local. Prefer a code fix
when practical.

Common warnings:

| Code   | Meaning |
|--------|---------|
| SC2086 | Quote expansions to avoid splitting/globbing |
| SC2046 | Quote command substitutions before splitting |
| SC2006 | Use `$(...)` instead of backticks |
| SC2034 | Variable appears unused |
| SC2155 | Declare and assign separately when needed |
| SC2164 | Handle `cd` failure explicitly |

#### Trap capture and SC2064

SC2064 is not a blind rewrite order. Under
`set -u`, changing an intentionally early-expanded
trap into late expansion can break cleanup once a
local variable is gone.

Mechanical but risky rewrite:

```bash
tmpdir=$(mktemp -d)
trap ':cleanup "$tmpdir"' EXIT
```

Safer options:

- keep cleanup state in a variable whose lifetime
  survives until the trap runs, then use
  `trap :cleanup EXIT`
- when early capture is deliberate, keep it and add a
  narrow suppression

```bash
tmpdir=$(mktemp -d)
# shellcheck disable=SC2064
trap ":cleanup $(printf '%q' "$tmpdir")" EXIT
```

#### Namerefs and SC2034

SC2034 can fire on `local -n` namerefs or other
write-only output references even when the API is
correct. Keep the clearer API and suppress narrowly
instead of contorting the code into globals.

```bash
:update-out() {
    local -n out_ref=$1
    # shellcheck disable=SC2034
    out_ref=$2
}
```

Full wiki: https://www.shellcheck.net/wiki/

### shfmt

```bash
shfmt -w script.sh
shfmt -d script.sh
shfmt -w .
shfmt -ln bash -w script.sh
shfmt -i 4 -w script.sh
shfmt -ci -w script.sh
shfmt -bn -w script.sh
shfmt -sr -w script.sh
shfmt -s -w script.sh
```

Useful flags:

- `-ln bash|posix|mksh|bats` to set the parser
- `-i N` to use spaces instead of tabs
- `-ci` to indent `case` bodies
- `-bn` to put binary operators on the next line
- `-sr` to normalize redirect spacing
- `-s` to simplify safe constructs

EditorConfig support:

```ini
[*.sh]
indent_style = space
indent_size = 4
shell_variant = bash
switch_case_indent = true
```

### shdoc

Run shdoc on every touched maintained script or shell
library after documentation changes:

```bash
shdoc script.sh >/tmp/script.md
```

Then read the generated Markdown. Verify the file
title, brief, overview, function index, arguments,
options, stdin/stdout/stderr notes, exit codes, and
see-also links match the source contract. Fix source
tags, not generated Markdown, unless you are updating
the committed generated reference file.

If the project already has a docs target or reference
file, regenerate it. If not, suggest an output path in
the final notes, such as:

```bash
shdoc script.sh > REFERENCE.md
```

## Reusable shell script rules

Use these rules when lint output is not enough and
you need to improve the script itself. They are meant
to travel across repos rather than describe one code
base.

### 1. Declare the shell honestly

If a file needs Bash features, make it Bash. Do not
claim one shell and write for another.

Bad:

```sh
#!/bin/sh
files=(a b)
[[ -n "$x" ]]
```

Good:

```bash
#!/usr/bin/env bash
files=(a b)
[[ -n "$x" ]]
```

Keep the shebang, invoked shell, and syntax aligned.

### 2. Decide whether the file is a script or a library

A standalone script can set shell options, parse
arguments, and `exit`. A sourced library should avoid
surprising the caller by changing global shell state
or exiting their shell. A sourced data/config
fragment should stay declarative instead of being
restyled as a full script.

For standalone scripts, prefer a small `:main()`
entrypoint:

```bash
:main() {
    :
}

:main "$@"
```

For libraries, keep exposed functions under an
explicit namespace and internal helpers under a
leading `:` namespace:

```bash
mytool:sync() {
    :
}

:parse-args() {
    :
    return 0
}
```

Prefer `exit` in `:main()` and `return` in helpers.

### 3. Keep top-level code declarative

At the top level, keep only:

- shell options
- uppercase constants and env defaults
- function definitions
- the final `:main "$@"` call for standalone scripts

Do not spread real control flow across the top level.
Keep the entrypoint call once at the bottom of the
file.

### 4. Put config defaults near the top

Keep environment-backed configuration near the top of
the file and prefer uppercase names for those values.
Make true constants `readonly` when practical.

Good:

```bash
readonly CACHE_DIR=${CACHE_DIR:-$HOME/.cache/mytool}
readonly VERBOSE=${VERBOSE:-0}
readonly TIMEOUT=${TIMEOUT:-30}
```

This makes configuration obvious before the function
body starts.

### 5. Do not keep mutable runtime state in globals

Top-level variables should be configuration or
constants, not scratch state that helpers mutate while
commands run.

Bad:

```bash
profile_name=''
result=''

:load-profile() {
    profile_name="$1"
    result=ok
}
```

Good:

```bash
:load-profile() {
    local profile_name="$1"
    local result=ok
    :
}
```

If state must travel across helpers, pass it as
arguments, print it, or use one explicit data source.
Avoid invisible write-through globals.

### 6. Order functions for the reader

Do not sort functions mechanically. Group them by
role and subsystem so the file reads top to bottom.

Common layouts:

- constants and config first
- CLI helpers such as `:usage()` and `:parse-opts()`
- related subsystem helpers together
- `:main()` near the end or where the main flow is
  easiest to read
- one final `:main "$@"` call at the bottom

In libraries, keep public API grouped and internal
helpers grouped instead of interleaving them.

### 7. Use shell naming deliberately

Preferred conventions:

- `:main()` for the standalone entrypoint
- leading `:` for internal helpers
- `tool:sync()` style names for exposed reusable
  functions
- additional `:` for grouped helpers such as
  `:history:add()` or `:cache:store()`
- hyphens over underscores in function names

Good:

```bash
:main() {
    :
}

:parse-opts() {
    :
}

tool:sync() {
    :
}

:history:add() {
    :
}
```

Less preferred for new code:

```bash
main() {
    :
}

parse_opts() {
    :
}

sync() {
    :
}
```

Use underscores only when you are mirroring an
external command or preserving an established API.

### 8. Give non-trivial CLIs a help and parsing layer

If a script has real flags or modes, do not parse all
of it inline in `:main()`.

Prefer:

- `:usage()` or `:help()` for help text
- `:parse-opts()` for option parsing
- `:main()` for overall flow

Use a heredoc for multi-line help text instead of a
long sequence of `echo` calls.

Good:

```bash
:usage() {
    cat <<EOF
Usage:
    mytool [options] <arg>
EOF
}
```

### 9. Use strict mode deliberately

For standalone scripts, `set -euo pipefail` is a good
baseline. For sourced files, changing options
globally can be hostile to the caller.

Even in strict mode, handle important control points
explicitly:

```bash
cd "$workdir" || exit 1
```

When non-zero status is expected, write that branch
explicitly instead of depending on `set -e` details.
This matters especially for probe commands such as
`systemctl is-active`, `grep -q`, `pgrep`, or similar
status checks.

Bad:

```bash
services=$(systemctl is-active a.service b.service | paste -sd' ' -)
```

Good:

```bash
services=$(systemctl is-active a.service b.service 2>/dev/null || true)
services=$(paste -sd' ' <<<"$services")
```

Or branch explicitly with `if` or `case` when the
status itself is the data you care about.

### 10. Declare locals early

In non-trivial functions, declare `local` variables
near the top of the function before the main logic.

Good:

```bash
:main() {
    local mode="${1:-}"
    local config_file="${CONFIG_FILE:-$HOME/.config/x}"

    :
}
```

This keeps function inputs and mutable state obvious.

### 11. Quote expansions and use arrays for argv

Quote expansions by default. Reach for unquoted
expansion only when you really want shell splitting
or globbing.

Bad:

```bash
cp $src $dst
cmd="tar -czf $archive $dir"
$cmd
```

Good:

```bash
cp -- "$src" "$dst"
cmd=(tar -czf "$archive" "$dir")
"${cmd[@]}"
```

Use `"$@"` for forwarding arguments.

### 12. Keep stdout for data and stderr for diagnostics

Treat stdout as the script's public data channel.
Send logs, warnings, and errors to stderr.

Good:

```bash
printf '%s\n' "$result"
printf 'warning: %s\n' "$message" >&2
```

This keeps scripts composable in pipelines and makes
testing simpler.

### 13. Handle cleanup with named helpers and traps

If a script creates temporary state, own the cleanup.
Use `mktemp`, a named cleanup helper, and a trap.

```bash
tmpdir=$(mktemp -d)

:cleanup() {
    rm -rf -- "$tmpdir"
}

trap :cleanup EXIT INT TERM
```

Prefer a named helper over a long inline trap body
when cleanup does real work.

If cleanup depends on the current value of a local
path or PID, do not blindly apply ShellCheck's
SC2064 quoting advice. Either move the state to a
variable that survives until EXIT or keep the
intentional early capture with a narrow suppression.

### 14. Avoid stringly execution

Prefer arrays, `case`, and explicit argument passing
instead of building commands in strings.

Bad:

```bash
eval "$user_supplied"
```

Better:

```bash
cmd=(grep -E "$pattern" "$file")
"${cmd[@]}"
```

If `eval` is unavoidable, isolate it in one place,
document what input is allowed, and test the quoting
rules around it.

### 15. Manage background jobs deliberately

If a script starts background work, record the PID,
clean it up, and `wait` for it.

```bash
worker >"$log" 2>&1 &
pid=$!
trap 'kill "$pid" 2>/dev/null || true' EXIT
wait "$pid"
```

Do not let success paths leak background processes or
hide async failures.

### 16. Document maintained shell API in source

A maintained shell script or library is not complete
without shdoc docs that `shdoc` can render cleanly.
Put a file-level block near the top of scripts and
libraries, and put API docs directly above exposed
reusable functions.

Prefer documenting the contract:

- `@description` for behavior
- `@arg` or `@noargs` for the call shape
- `@option` for flags accepted by a function
- `@stdin`, `@stdout`, or `@stderr` when streams are
  part of the contract
- `@exitcode` when non-zero codes are meaningful
- `@see` for related functions
- `@internal` only when a hidden helper needs the same
  doc style internally

Do not force full doc blocks onto tiny private
helpers that are obvious from local context. When an
internal helper is documented, include a real docblock
with `@internal` so shdoc consumes it with that
function.

### 17. Gate debug logging and keep wording literal

If a script has debug logs, route them through one
helper or one verbosity check. Do not scatter raw
ungated debug prints.

When output needs hierarchy, prefer short labels and
indentation over separator lines made of `====`,
`----`, or similar filler. The text should carry the
meaning, not the decoration.

Prefer log lines that describe one of these:

- an action in progress, such as `starting sshd`
- a wait condition, such as `waiting for sshd`
- a state observation, such as `is offline`
- a transition, such as `lock has been acquired`
- a failure tied to an operation, such as
  `error copying:`

When logs need context, prefix by subsystem,
instance, or operation kind, such as `[build]`,
`[$container]`, `TESTCASE`, or `assertion (...)`.

### 18. Test behavior, not only lint output

ShellCheck, shfmt, and shdoc are necessary, not
sufficient.
When a script depends on external commands or remote
endpoints, probe those dependencies separately once
before you bake the assumption into the code. Also
exercise every mode or fallback path you touched, not
just help text or the easiest happy path.

Also test the behavior users depend on:

- exit status
- stdout
- stderr
- cwd and PATH assumptions
- temp-dir cleanup
- signal and background-job behavior when relevant
- fallback and alternate-mode behavior when relevant
- external dependency handling when relevant

### Review checklist

- Dialect matches the syntax in the file.
- Script, library, and sourced data/config roles are
  distinguished correctly.
- Top-level code is declarative and ends with one
  `:main "$@"` call when applicable.
- Config defaults are obvious near the top, uppercase,
  and `readonly` when practical.
- Mutable runtime state is not hidden in top-level
  globals.
- `:main()` and helper naming use the chosen colon
  style consistently.
- Functions are grouped by role or subsystem instead
  of alphabetized mechanically.
- Exposed functions use a namespace instead of bare
  names.
- Hyphens are preferred over underscores for new
  function names.
- Non-trivial CLIs have `:usage()` or `:help()` and a
  dedicated parse helper.
- Locals are declared early in larger functions.
- Maintained scripts and libraries have file-level
  shdoc docs.
- Public reusable functions are documented in source
  when they form part of the shell API.
- shdoc tags are used in the right place; file-level
  `@example` blocks are not invented.
- No bare `@internal` block can leak into the next
  public function.
- Quotes and argv handling are safe.
- Stdout and stderr have separate roles.
- Cleanup uses named helpers and traps when needed.
- Trap capture semantics still match the intended
  cleanup lifetime.
- `eval` and background jobs are justified.
- Logs are gated, contextual, and literal.
- Logs use labels and indentation, not decorative
  rulers.
- Suppressions are narrow and local.
- ShellCheck fixes were reviewed semantically, not
  applied mechanically.
- `shellcheck`, `shfmt`, parser checks, and `shdoc`
  were re-run after edits.
- Generated Markdown from `shdoc` was inspected and
  fixed at the source when needed.
- Bash behavior tests use the repository's
  `test-runner.bash`/`tests.sh` harness, or final notes
  explain why an existing non-test-runner harness was
  preserved.
- Test setup, teardown, fixtures, temp dirs, custom
  runner options, and progress hooks are centralized
  instead of duplicated in testcase files.
- Touched modes or fallbacks were exercised, not only
  linted.
- Generated docs were updated, or final notes suggest
  where to write them.

## Documentation and logging style

Use this section when shell work is not only about
making the code pass ShellCheck, but also about
making the shell API and runtime output readable and
consistent.

### 1. Document maintained shell files in source

For maintained scripts and shell libraries, put a
small file-level shdoc block near the top. Treat it as
the public description that generated docs will show.

```bash
# @file mytool
# @brief Synchronize project state across hosts.
# @description
#   Provides sync, status, and cleanup helpers.
```

For reusable shell APIs, put function documentation
immediately above the function it describes. Treat the
comment block as part of the function contract.

Good:

```bash
# @description Synchronize project files to the host.
#
# @arg $1 string Hostname.
# @arg $2 string Source directory.
#
# @exitcode 0 If synchronization succeeded.
# @exitcode 1 If rsync failed.
#
# @see :sync:prepare()
tool:sync() {
    :
}
```

Internal helper, hidden from generated docs:

```bash
# @internal
# @description Prepare sync state.
# @noargs
:sync:prepare() {
    :
}
```

Do not use a bare `@internal` line. Pair it with a
docblock that shdoc can consume for that function.

After editing docs, run `shdoc` and read the generated
Markdown. A wrong heading, missing function, broken
section, or misleading contract means the source tags
are wrong.

### 2. Use shdoc tags deliberately

Use tags that shdoc renders:

File-level tags:

- `@file` or `@name` for the file title
- `@brief` for a one-line file summary
- `@description` for the file overview

Function-level tags:

- `@description` for the main behavior
- `@example` for a real usage example
- `@option` for accepted flags
- `@arg` for positional arguments
- `@noargs` when no arguments are expected
- `@set` for variables set as part of the API
- `@stdin`, `@stdout`, and `@stderr` for stream
  contracts
- `@exitcode` for meaningful return codes
- `@see` for related functions or references
- `@internal` to keep helper docs out of the public
  reference
- `@deprecated` for deprecated functions

Grouping tag:

- `@section` for grouping related functions in the
  generated reference

Do not put function-only tags such as `@example` at
file top. Do not invent tags for public docs; shdoc
output is the verification source.

Use tags only when they add contract value. Do not
write noisy pseudo-docs for obvious one-line helpers.

### 3. Prefer contract details over narration

The best shell docs answer these questions fast:

- what the function does
- what arguments or options it expects
- what it reads from stdin or prints to stdout/stderr
- which exit codes matter
- which related function to look at next

Prefer this:

```bash
# @description Wait until the lock file disappears.
#
# @arg $1 string Lock file path.
# @exitcode 0 If the lock was released.
# @exitcode 1 If the timeout elapsed.
```

Over this:

```bash
# This function is responsible for handling lock file
# waiting in a pretty smart and robust way.
```

### 4. Keep file-level docs in the same style

Every maintained shell script or stable library should
have a small file-level block at the top. This keeps
generated docs close to the implementation instead of
duplicating them by hand elsewhere.

### 5. Keep top-level help and docs intentional

If a script has a real CLI, give it a `:usage()` or
`:help()` helper and render multi-line help with a
heredoc. Keep the help text in one place instead of
spreading it across many `echo` calls.

```bash
:usage() {
    cat <<EOF
Usage:
    mytool [options] <arg>
EOF
}
```

### 6. Log actions and state, not decoration

Good log lines explain what is happening, what is
being waited on, what changed, or what failed.

Prefer action wording for work in progress:

- `building go binary`
- `bootstrapping container`
- `starting sshd`
- `generating local key pair`
- `waiting for sshd`
- `evaluating command`

Prefer state wording for observations or transitions:

- `is offline`
- `is online and has ip`
- `matches found`
- `file changed`
- `global lock has been acquired`
- `coprocess has been terminated`
- `TESTCASE PASSED`
- `TESTCASE FAILED`

Prefer failure wording that names the operation:

- `error writing file:`
- `error copying:`
- `remote execution failed`

### 7. Gate debug logs

If a script has debug output, route it through one
helper or one verbosity gate. Debug logs should be
cheap to disable and easy to recognize when enabled.

Good:

```bash
:debug() {
    (( VERBOSE > 0 )) || return 0
    printf '[debug] %s\n' "$*" >&2
}
```

Prefer that over scattered raw debug `echo` calls.

### 8. Keep log prefixes simple and useful

Use small prefixes only when they add context.

Good patterns:

```bash
printf '[build] building go binary... ' >&2
printf '[%s] starting sshd...\n' "$container" >&2
printf 'TESTCASE %s\n' "$testcase" >&2
printf 'assertion (%s): failed\n' "$name" >&2
```

Good prefixes usually identify one of these:

- the subsystem, such as `[build]`
- the instance, such as `[$container]`
- the operation kind, such as `TESTCASE` or
  `assertion (...)`

Do not add banners, rulers, or ornamental noise.

### 9. Prefer short, literal verbs

Prefer direct verbs and states over chatty prose.

Prefer:

- `starting`
- `waiting`
- `generating`
- `running`
- `loading`
- `failed`
- `passed`
- `changed`
- `acquired`
- `terminated`

Avoid inflated or vague wording such as:

- `performing magic`
- `doing some setup stuff`
- `all systems go`
- `awesome success`

### 10. Route output by audience

Keep user-facing diagnostics and debug logs on stderr.
Keep data meant for pipelines on stdout.

That makes it easier to test shell behavior and lets
callers capture data without scraping logs.

### Documentation and logging checklist

- Maintained scripts and libraries have file-level
  shdoc docs.
- Exposed functions are documented directly above the
  function when they form part of the API.
- shdoc tags describe arguments, options, streams, and
  exit codes when those are part of the contract.
- `shdoc` was run and generated Markdown was inspected.
- Internal helpers are either undocumented or marked
  with `@internal` in a complete docblock.
- CLI help is centralized in `:usage()` or `:help()`
  when the script is non-trivial.
- Log lines describe actions, waits, state changes,
  or failures.
- Debug logs are gated through one helper or one
  verbosity check.
- Log wording is concise and literal.
- Prefixes add context instead of decoration.
- Stdout is for data; stderr is for diagnostics.

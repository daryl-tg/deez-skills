# Testing reference

Use this reference when adding or changing tests in
maintained Bash repositories.

## Policy

For Bash code, `test-runner.bash` is the right default
harness for unit, CLI, shell-library, integration,
regression, and harness self-tests. Run the repository
wrapper when it exists. If the repository has no Bash
harness, bootstrap `test-runner.bash` with `tests.sh`
instead of adding Bats, shunit2, ad hoc loops, or
one-off assertion scripts.

The only reasons not to use `test-runner.bash` are:
the repository already has a working different harness
and migration is outside the task; the user explicitly
asks for a replacement; or the tests are not for Bash
code. Even then, do not introduce a second framework
beside an existing Bash suite.

Behavior changes require behavior tests. Assert the
user-visible contract: exit status, stdout, stderr,
files, cleanup, processes, and integration effects.

Test public APIs and commands first. Assert private
helpers only when the helper is the public unit of that
library or when the repository already tests that layer
directly.

## What test-runner gives you

`test-runner.bash` is the suite wrapper for maintained
Bash tests. It is small, but it gives the suite one
explicit place for runner behavior instead of copying
boilerplate into every testcase:

- imports through `import.bash` and uses `tests.sh`
  underneath
- central testcases directory selection
- local setup and teardown hooks
- default all-tests runs and focused or last-failed
  runs with `-O`
- verbose runs with `-v`
- custom suite options through
  `test-runner:set-custom-opts` and
  `test-runner:handle-custom-opt`
- positional argument handling through
  `test-runner:handle-args`
- progress forwarding through `test-runner:progress`

Because it runs `tests.sh`, the same harness also gives
the testcases command capture, exit-status/stdout/stderr
assertions, exact and regex matching, fixture files,
temp directories, file diffs, negative assertions,
pipeline and shell-word checks, background-process
helpers, wait helpers, and integration helpers such as
tmux, Vim, SSH, containers, and daemon fixtures.

Use it for local unit-style shell tests and for heavier
integration tests. Let the testcase assert behavior; let
the wrapper/setup own imports, shared environment,
fixtures, and runner options.

## Library map

Imported package details are in [imports.md](imports.md).
Use `vendor.bash/` for vendored shell libraries and read
the package documentation from the vendored checkout, such as
`vendor.bash/github.com/reconquest/<package>/README.md`,
before guessing helper APIs. Keep shell libraries out of Go's
`vendor/` directory so Go tooling can own it.

### Core harness libraries

- `test-runner.bash` is the preferred suite wrapper
  around `tests.sh`. Use it for Bash test suites that
  need testcase discovery, local setup/teardown,
  all/focused/verbose runs, custom options, argument
  hooks, or progress wiring.
- `tests.sh` is the assertion, fixture, temp-dir,
  subprocess, wait, background, capture, and testcase
  runtime. Testcase files are Bash fragments executed by
  this runtime.
- `import.bash` loads shell libraries from the repository
  `vendor.bash/` tree. Source it once in the suite
  wrapper or setup, then load dependencies with
  `import:use github.com/reconquest/<name>`. Do not put
  shell library dependencies in Go's vendor directory.
- `shdoc` verifies shell documentation. It is required
  for maintained scripts and libraries, but it is not a
  runtime behavior test harness.

### Common shell support libraries

- `opts.bash` provides `opts:parse` for Bash option parsing.
  Tests for parsers assert the resulting associative options
  and positional argument array.
- `types.bash` provides variable-shape predicates such as
  `types:is-array` and `types:is-assoc-array`. Use it as a
  dependency, not as a reason to test implementation trivia.
- `coproc.bash` provides low-level coprocess control. Use
  `tests.sh` background helpers in ordinary tests; test
  `coproc:*` directly only in the coprocess library or code
  whose public contract is coprocess behavior.
- `progress.bash` provides spinner/progress helpers. Test
  stable stdout, stderr, and process behavior; do not assert
  terminal animation frames unless that exact output is the
  contract.
- `go-test.bash` builds and runs Go binaries while collecting
  coverage. Use it only in repositories that already test a
  Go-backed shell integration this way.

### Integration helper libraries

- `tmux.bash` drives tmux sessions. Use public helpers such
  as `tmux:new-session`, `tmux:send`, `tmux:cat-screen`,
  `tmux:wait-sync`, and `tmux:kill-session`.
- `vim-test.bash` drives Vim plugin tests. Use
  `vim-tests:start`, `vim-tests:type`,
  `vim-tests:write-file`, `vim-tests:get-messages`, and
  `vim-tests:end`/`vim-tests:end-silent`.
- `ssh-test.bash` builds SSH fixtures. Use
  `ssh-test:set-username`, `ssh-test:set-key-path`,
  `ssh-test:set-remote-runner`, key generation, sshd start,
  and `ssh-test:connect:by-key` only for SSH behavior.
- `containers.bash` owns container lifecycle for integration
  suites: spawn, run, list, inspect IP/rootfs, destroy, wipe,
  and provider registration.
- `containers-bootstrap.bash` builds bootstrap scripts for
  container fixtures: PATH setup, users, sudoers, and home
  directories.
- `hastur.bash` is the historical Hastur container provider
  used behind container-backed suites. Prefer `containers.bash`
  as the public test API unless the repository already calls
  `hastur:*` directly.
- `blank.bash` builds `blankd` server and request fixtures.
  Use it only for repositories whose contract involves that
  protocol or fixture server.
- `usage.bash` has no stable public testing API in the usual
  upstream repository. Do not add it as a test dependency
  unless the current repository already includes it under
  `vendor.bash/` and uses it.

Do not import an integration helper merely to fake work that
can be tested with a local function, fixture file, or temp
directory.

## Repository shape

Keep the existing test layout. When the repository has a
working shell harness, add files in that harness and keep its
names, setup files, and runner flags.

Common files:

```text
run_tests
run_tests.sh
tests/run_tests
tests/setup.sh
tests/local-setup.sh
tests/teardown.sh
tests/testcases/*.test.sh
```

Testcase files are Bash fragments, not standalone scripts.
Do not add a shebang, strict mode, or import boilerplate to
every testcase. The runner and setup file own those details.

Shared setup prepares imports, `vendor.bash/` libraries, temp
dirs, PATH, and fixtures. Individual testcases own behavior
assertions.

## Bootstrapping a missing harness

When a repository has no shell harness, bootstrap the
smallest compatible `test-runner.bash` suite inside the
repository. Do not choose direct `tests.sh`, Bats,
shunit2, or custom loops for a new Bash suite unless the
user asks; `test-runner.bash` already delegates the
assertions to `tests.sh` and owns the runner behavior.
Do not copy files from unrelated local checkouts or
search a developer's home directory for examples. Use
upstream sources, the repository's documented dependency
mechanism, or ask before borrowing from another tree.

Choose one suite root first. Use `tests/` for the main shell
suite. Use a focused directory such as `int/` only when the
repository already separates integration tests from other
suites.

Recommended first files:

```text
<suite>/run_tests
<suite>/setup.sh
<suite>/teardown.sh
<suite>/testcases/can-run-harness.test.sh
vendor.bash/github.com/reconquest/import.bash/
vendor.bash/github.com/reconquest/test-runner.bash/
vendor.bash/github.com/reconquest/tests.sh/
```

Bootstrap `import.bash` first:

```bash
suite=tests
mkdir -p "$suite/testcases"
git submodule add https://github.com/reconquest/import.bash \
    vendor.bash/github.com/reconquest/import.bash
touch "$suite/setup.sh" "$suite/teardown.sh"
```

Use `vendor.bash/github.com/...` for shell libraries unless
the repository already has an explicit non-directory
dependency mechanism. Do not use Go's vendor directory for
shell libraries; it conflicts with Go vendoring.

Add direct harness dependencies as submodules or let
`import:use` fetch them during the first wrapper run,
according to repository policy:

```bash
git submodule add https://github.com/reconquest/test-runner.bash \
    vendor.bash/github.com/reconquest/test-runner.bash

# If the repository vendors transitive dependencies explicitly:
git submodule add https://github.com/reconquest/tests.sh \
    vendor.bash/github.com/reconquest/tests.sh
```

Vendor harness dependencies under the repository in
`vendor.bash/`. If the repository has a `vendor.bash/bootstrap`
command, use it. If it does not use submodules, clone the
public upstreams into the same `vendor.bash/` paths and
document that bootstrap choice.

A new suite wrapper must work from any current directory:

```bash
#!/bin/bash

set -euo pipefail

_base_dir="$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")"
_repo_dir="$(dirname "$_base_dir")"
source "$_repo_dir/vendor.bash/github.com/reconquest/import.bash/import.bash"

import:use github.com/reconquest/test-runner.bash

:main() {
    test-runner:set-local-setup "$_base_dir/setup.sh"
    test-runner:set-local-teardown "$_base_dir/teardown.sh"
    test-runner:set-testcases-dir "$_base_dir/testcases"

    test-runner:run "${@}"
}

:main "${@}"
```

After writing the wrapper, mark it executable:

```bash
chmod +x <suite>/run_tests
```

Keep setup and teardown tiny at bootstrap time. Put shared
fixture creation, PATH wiring, and local imports there;
leave assertions in testcase files. Add one trivial testcase
first, then replace it or follow it with real behavior tests.

Run both a focused testcase and the whole suite before
building more cases:

```bash
./<suite>/run_tests -O can-run-harness
./<suite>/run_tests
```

## Runner wrappers

Use `test-runner.bash` for new Bash test wrappers. Match
the local style in repositories that already have a
working wrapper; do not rewrite a suite only to normalize
it.

Most wrappers load `test-runner.bash` through
`import.bash`:

```bash
#!/bin/bash

set -euo pipefail

_base_dir="$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")"
source "$_base_dir/vendor.bash/github.com/reconquest/import.bash/import.bash"

import:use github.com/reconquest/test-runner.bash

test-runner:run "${@}"
```

A working direct `tests.sh` wrapper may stay when
migration is not in scope:

```bash
tests:main -d tests/testcases -s tests/local-setup.sh "${@:--A}"
```

When you touch or create a `test-runner.bash` wrapper,
keep suite-specific wiring in wrapper hooks: set the
testcases directory, local setup, local teardown, custom
options, argument handling, and progress there instead
of duplicating that logic in testcase files.

## Setup files

Use setup files only for shared environment:

```bash
tests:clone -r vendor.bash vendor.bash
tests:involve opts.bash
```

Use these `tests.sh` helpers instead of open-coded setup
plumbing:

- `tests:involve file` copies and sources a library
- `tests:require file` sources a file with debug output
- `tests:clone source dest` copies fixture files
- `tests:clone -r source dest` copies fixture trees
- `tests:make-tmp-dir path` creates temp directories
- `tests:cd path` and `tests:cd-tmp-dir path` set cwd

Use `tests/setup.sh` or `tests/local-setup.sh` according to
local convention. Keep teardown empty when the runner or
library cleanup already owns the state.

## Testcase names

Name testcase files as lowercase behavior sentences ending
in `.test.sh`:

```text
can-parse-long-opt-with-value.test.sh
returns-non-zero-exit-code-on-unexpected-opt.test.sh
will-return-error-when-given-flag-which-is-not-defined.test.sh
do-not-output-debug-from-bg-process-on-low-verbosity.test.sh
```

Use one behavior per file. Combine variants only when they
are the same behavior with two spellings, such as short and
long option forms.

## Testcase shape

Keep cases direct: arrange data, call the public API, assert
visible behavior.

```bash
typeset -A opts
typeset -a args

opts:parse opts args --delta: -- 1 --delta=2 3

tests:assert-equals "2" "${opts[--delta]}"
tests:assert-equals "3" "${#args[@]}"
```

Use the namespace style of the library under test:
`opts:parse`, `import:use`, `tmux:send`,
`vim-tests:start`, and so on.

A testcase may define small local functions for stubs or
callbacks. Keep them inside the testcase unless several
cases share the same fake, in which case setup owns it.

## Assertion vocabulary

Use `tests.sh` helpers. Do not open-code assertion branches.

Command execution:

- `tests:ensure command ...` for expected success
- `tests:not tests:ensure command ...` for expected failure
- `tests:eval command ...` to capture stdout, stderr, and
  exit code without failing immediately
- `tests:runtime command ...` when the tested command may
  run long enough to need live output handling
- `tests:pipe command ...` when pipe behavior is the
  contract
- `tests:value var command ...` to capture exact stdout into
  a variable

Result assertions:

- `tests:assert-success` and `tests:assert-fail` for the
  last captured command
- `tests:assert-exitcode N` for a specific exit status
- `tests:assert-equals expected actual` for scalars
- `tests:assert-stdout text` and `tests:assert-stderr text`
  for literal output fragments
- `tests:assert-stdout-empty` and
  `tests:assert-stderr-empty` for silence
- `tests:assert-stdout-re re`, `tests:assert-stderr-re re`,
  and `tests:assert-re stdout|stderr|file re` for variable
  output
- `tests:assert-no-diff expected actual` for multiline
  output or files
- `tests:assert-test ...` for shell `test` predicates
- `tests:fail message` for impossible branches inside test
  scaffolding

Assert full stdout and stderr with `tests:assert-no-diff`
when exact output matters. Use regexes for PIDs, paths,
colors, command diagnostics, timing, and other variable text.

When existing tests assert `$?` directly after a special
inline `eval`, preserve that pattern for the same API. Do
not expand it into a custom harness.

## Fixtures

Create fixtures inline unless the repository already keeps a
shared fixture tree.

```bash
tests:put script.bash <<EOF
source import.bash
import:use lib-a
EOF
```

Use nested heredoc delimiters when generating testcases or
scripts inside scripts:

```bash
put testcases/put-contents.test.sh <<EOF
tests:put multiline-file <<EOF2
1
2
3
EOF2
EOF
```

Good delimiter names are short and contextual: `EOF2`,
`COMMAND`, `GO`, `VIMRC`, `VIML`, or `PY`.

Keep checked-in fixtures only when many tests share the same
executable or data file, such as a fake request handler
under `tests/`.

## Negative behavior

Express expected failures with `tests:not` or with a
captured command plus assertions on stderr, stdout, or exit
code.

```bash
tests:eval opts:parse opts args --data: -- --data
tests:assert-stderr "option '--data' requires an argument"
tests:assert-fail
```

Do not hide the failure path behind `if` statements. Make
the visible contract part of the assertion.

## Mocking external commands

Stub external commands with shell functions in the testcase.
Delegate to the real command with `command` when the test
still needs it.

```bash
git() {
    tests:eval echo "$*" '>>' "$(tests:get-tmp-dir)/git.log"
    command git "$@"
}
```

For remote runners or daemons, use a fake runner that prints
the command it would run. Use real network, SSH, tmux, Vim,
container, or daemon dependencies only when the repository is
specifically testing that integration.

## Shell-word behavior

When testing `tests:eval`, option parsers, redirects, or
pipes, preserve the exact shell-word semantics under test.
Pass pipe and redirect tokens as separate arguments when
that is the behavior:

```bash
tests:ensure echo 1 '>&2'
tests:assert-stdout ''
tests:assert-stderr '1'
```

Do not simplify quoting in tests that protect quoting, argv,
redirection, or `eval` behavior.

## Self-hosted harness tests

When testing `tests.sh` or `test-runner.bash`, the outer
testcase writes inner `.test.sh` files, runs the harness, and
asserts the resulting summary or debug output.

```bash
put testcases/echo-meep-success.test.sh <<EOF
tests:eval echo meep
tests:assert-stdout meep
EOF

ensure tests.sh -d testcases -A
assert-stdout '1 tests (1 assertions) done successfully!'
```

Some self-hosted tests import the `tests.sh` namespace in
setup and call helpers without the `tests:` prefix. Match the
local setup instead of mixing both styles.

## Background and interactive tests

Use harness helpers for long-lived processes:

- `tests:run-background id command ...`
- `tests:get-background-pid id`
- `tests:get-background-stdout id`
- `tests:get-background-stderr id`
- `tests:stop-background id`
- `tests:wait-file-matches file re interval timeout`
- `tests:wait-file-not-matches file re interval timeout`
- `tests:wait-file-changes file interval timeout`

For tmux and Vim helpers, drive behavior through the public
wrappers such as `tmux:send`, `tmux:cat-screen`,
`vim-tests:start`, and `vim-tests:end`. End sessions in the
testcase or rely on the runner cleanup trap already present
in that repository.

## What to cover

When behavior changed, test the user-visible contract:

- exit status
- stdout and stderr
- parsed arguments and preserved positionals
- cwd and PATH assumptions
- generated files and file contents
- temp-dir cleanup
- background-job or signal behavior
- fallback and alternate modes
- external dependency handling

Do not stop at `shellcheck`, `shfmt`, parser checks, or help
output when runtime behavior changed.

## Running tests

Run the repository wrapper:

```bash
./run_tests.sh
./run_tests
./tests/run_tests
```

Use the local focused mode while iterating:

```bash
./run_tests.sh -O parse-long
./run_tests.sh -v -O parse-long
```

Many wrappers default to all tests with `${@:--A}`. Preserve
that convenience when adding or rewriting a wrapper.

## Checklist

- The existing harness style is preserved, or a missing
  harness is bootstrapped inside the repository.
- Required libraries are vendored under
  `vendor.bash/github.com/reconquest/...` or loaded by the
  local dependency mechanism.
- Shared imports, PATH, temp dirs, and fixtures are in setup,
  not copied into every testcase.
- Testcase files live under the local testcase directory and
  have behavior-style `.test.sh` names.
- The test exercises public behavior, not private helper
  trivia.
- Fixtures are generated with `tests:put` unless checked-in
  fixtures are the local convention.
- Expected failures use `tests:not` or captured status
  assertions.
- Stdout, stderr, and exit status are asserted when they are
  part of the contract.
- Shell-word, redirect, and quoting tests preserve the exact
  argument shape under test.
- External systems are stubbed unless the repository exists
  to test that integration.
- A focused testcase and the relevant full suite passed, or
  final notes explain why they could not be run.

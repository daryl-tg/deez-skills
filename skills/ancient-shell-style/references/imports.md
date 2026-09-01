# Imported shell package reference

Use this reference when a Bash repository imports shell
packages with `import.bash` or vendors them under
`vendor.bash/github.com/reconquest/...`.

## Policy

- Preserve the repository's existing dependency mechanism and
  exact `import:use` strings.
- Put shell packages under `vendor.bash/`, not Go's `vendor/`
  directory.
- Source `import.bash` once in the suite wrapper or shared
  setup, then load direct dependencies from there.
- Keep shared imports in setup or the runner wrapper, not in
  every testcase file.
- Add integration helpers only when the repository is testing
  that integration. Prefer local functions, fixture files, and
  temp directories for ordinary stubs.
- When an older suite imports a package without the `.bash`
  suffix, keep the local spelling unless you are deliberately
  migrating the vendor layout.

## Local vendored documentation

The package checkout in `vendor.bash/` is also the local
documentation source. Before guessing an imported API, read
the vendored package docs first:

```text
vendor.bash/github.com/reconquest/<package>/README.md
vendor.bash/github.com/reconquest/<package>/docs/
vendor.bash/github.com/reconquest/<package>/REFERENCE.md
```

This reference is the orientation map; the vendored docs are
the detailed API reference for the exact version in use. If a
needed package or its docs are missing, bootstrap or update the
`vendor.bash/` dependency according to repository policy before
depending on upstream-only behavior.

## Core loader and harness packages

### `import.bash`

- Role: the shell package loader.
- Main API: `import:use`.
- Use when: any repository package or vendored shell package
  must be loaded from `vendor.bash/`.
- Notes: source the loader directly from
  `vendor.bash/github.com/reconquest/import.bash/import.bash`.
  Do not load shell libraries from Go's `vendor/` tree.

### `tests.sh`

- Role: testcase runtime and assertion library for Bash
  functional and integration tests.
- Main API: `tests:main`, `tests:eval`, `tests:ensure`,
  `tests:assert-*`, fixture helpers, temp-dir helpers,
  background helpers, and wait helpers.
- Use when: tests need to assert exit status, stdout, stderr,
  files, temp dirs, processes, or command behavior.
- Notes: testcase files are Bash fragments executed by the
  runtime. They normally do not need their own shebang, strict
  mode, or import boilerplate.

### `test-runner.bash`

- Role: suite wrapper layer around `tests.sh`.
- Main API: `test-runner:run`, local setup/teardown setters,
  testcase directory setters, custom option hooks, and custom
  argument hooks.
- Use when: a repository needs a normal shell test wrapper with
  focused runs, all-test runs, verbose mode, setup/teardown,
  progress wiring, or custom options.
- Notes: this is the default wrapper for new maintained Bash
  suites unless the repository already has a working harness.

## General shell support packages

### `opts.bash`

- Role: simple Bash option parser.
- Main API: `opts:parse`.
- Use when: scripts or tests need to parse short options, long
  options, options with values, and remaining positional
  arguments into shell variables.
- Notes: parser tests should assert both the resulting options
  map and preserved positional arguments.

### `types.bash`

- Role: variable-shape predicates for Bash.
- Main API: helpers such as `types:is-array` and
  `types:is-assoc-array`.
- Use when: code must distinguish scalar variables, indexed
  arrays, associative arrays, or other Bash variable shapes.
- Notes: treat it as a dependency of the public behavior, not
  as a reason to test private implementation trivia.

### `coproc.bash`

- Role: low-level coprocess control.
- Main API: `coproc:*` helpers for starting a coprocess,
  getting file descriptors, sending input, and reading output.
- Use when: the public contract is direct coprocess behavior.
- Notes: ordinary tests should prefer `tests.sh` background and
  wait helpers instead of driving `coproc:*` directly.

### `progress.bash`

- Role: spinner and progress display helpers.
- Main API: `progress:*` helpers.
- Use when: command-line code has a stable progress or spinner
  contract.
- Notes: assert stable stdout, stderr, process state, and final
  messages. Do not assert terminal animation frames unless the
  exact frames are the contract.

### `go-test.bash`

- Role: build and run Go-backed command fixtures while
  collecting coverage.
- Main API: `go-test:set-output-dir`, `go-test:build`,
  `go-test:run`, and `go-test:merge-coverage`.
- Use when: a shell suite already tests a Go binary or Go-backed
  shell integration this way.
- Notes: do not add it to pure shell tests only to compile a
  helper; use a fixture command or local stub instead.

## Integration helper packages

### `tmux.bash`

- Role: tmux session driver for interactive terminal tests.
- Main API: helpers such as `tmux:new-session`, `tmux:send`,
  `tmux:cat-screen`, `tmux:wait-sync`, and
  `tmux:kill-session`.
- Use when: the behavior under test is a tmux session, terminal
  screen, or interactive command flow.
- Notes: end sessions in the testcase or rely on the existing
  runner cleanup trap when the repository already owns it.

### `vim-test.bash`

- Role: Vim plugin test driver.
- Main API: `vim-tests:start`, `vim-tests:type`,
  `vim-tests:write-file`, `vim-tests:get-messages`,
  `vim-tests:end`, and `vim-tests:end-silent`.
- Use when: the repository tests Vim plugin behavior or Vim
  integration.
- Notes: do not import it for generic file-editing assertions;
  use fixture files unless Vim behavior is the contract.

### `ssh-test.bash`

- Role: SSH fixture and connection helper.
- Main API: `ssh-test:set-username`, `ssh-test:set-key-path`,
  `ssh-test:set-remote-runner`, key generation, sshd startup,
  and `ssh-test:connect:by-key`.
- Use when: the public behavior depends on SSH, remote runners,
  SSH key setup, or sshd fixtures.
- Notes: for non-SSH behavior, use a fake runner that prints the
  command it would execute instead of starting real SSH.

### `containers.bash`

- Role: container lifecycle helpers for integration suites.
- Main API: spawn, run, list, inspect IP/rootfs, destroy, wipe,
  and provider registration helpers.
- Use when: the behavior requires an actual container fixture or
  a repository already uses this container test API.
- Notes: prefer this as the public test API for
  container-backed suites.

### `containers-bootstrap.bash`

- Role: bootstrap script builder for container fixtures.
- Main API: helpers that generate container bootstrap scripts
  for PATH setup, users, sudoers, and home directories.
- Use when: a container test needs repeatable in-container
  setup before the behavior under test runs.
- Notes: pair it with the repository's existing container
  provider instead of inventing ad hoc bootstrap heredocs.

### `hastur.bash`

- Role: historical Hastur container provider.
- Main API: `hastur:*` provider helpers.
- Use when: the repository already calls `hastur:*` directly or
  its existing container suite depends on Hastur.
- Notes: prefer `containers.bash` as the public API for new
  container-backed tests.

### `blank.bash`

- Role: `blankd` server and request fixture helper.
- Main API: `blank:*` helpers in repositories that test the
  blank protocol or fixture server.
- Use when: the repository's public contract involves `blankd`
  requests or the blank fixture server.
- Notes: do not add it to unrelated integration tests just to
  have a daemon-shaped fake.

### `usage.bash`

- Role: historical usage/help support package.
- Main API: no stable public testing API in the usual upstream
  repository.
- Use when: the current repository already vendors and calls it.
- Notes: do not add it as a new dependency unless the task is to
  preserve or extend existing `usage.bash` behavior.

## Related shell documentation tool

### `shdoc`

- Role: shell documentation generator, run as a CLI rather than
  loaded with `import.bash`.
- Use when: maintained scripts or shell libraries have file-level
  or public function docs.
- Notes: run it after documentation changes and read the
  generated Markdown. Fix missing sections, wrong anchors, and
  misleading contract text in the source annotations.

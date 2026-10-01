#!/usr/bin/env bash
# control-<app> — the deterministic verification lane for <app>.
#
# Committed to the repo it drives, never to the skills hub, so it versions with
# the app. Thin by construction: it binds this repo's preconditions and
# delegates driving to agent-browser rather than reimplementing it.
#
#   doctor                        is this instance worth driving?
#   browser <verb> [args...]      delegate to agent-browser
#   cli -- <command...>           run the app's own CLI, capture the result
#   evidence publish <run> <rev>  push the artifact pair to the renderer
set -euo pipefail

# Assigned, never chosen. Change only with the reserved-ports table.
APP_PORT="${APP_PORT:-31337}"
APP_ORIGIN="http://127.0.0.1:${APP_PORT}"
REVIEW_ORIGIN="http://127.0.0.1:8098"
ARTIFACTS="${ARTIFACTS:-$PWD/artifacts}"

die() { printf 'control: %s\n' "$*" >&2; exit 1; }

cmd_doctor() {
  local fail=0
  printf 'origin      %s\n' "$APP_ORIGIN"
  curl -fsS --max-time 3 "$APP_ORIGIN/healthz" >/dev/null 2>&1 \
    && printf 'health      ok\n' || { printf 'health      UNREACHABLE\n'; fail=1; }

  # The check that silently wastes runs when it is missing: is the thing that is
  # running actually built from the tree you are editing?
  local head served
  head="$(git rev-parse --short HEAD 2>/dev/null || echo unknown)"
  served="$(curl -fsS --max-time 3 "$APP_ORIGIN/version" 2>/dev/null || echo unknown)"
  printf 'working tree %s\n' "$head"
  printf 'serving      %s\n' "$served"
  [ "$served" = "unknown" ] && printf 'NOTE        cannot confirm the build matches the tree\n'

  command -v agent-browser >/dev/null 2>&1 \
    && printf 'harness     agent-browser present\n' \
    || { printf 'harness     agent-browser MISSING\n'; fail=1; }

  [ "$fail" -eq 0 ] || die 'doctor failed. Do not drive this instance.'
}

cmd_browser() {
  command -v agent-browser >/dev/null 2>&1 || die 'agent-browser not installed'
  exec agent-browser "$@"
}

cmd_cli() {
  [ "${1:-}" = "--" ] || die 'usage: control cli -- <command...>'
  shift
  set +e
  local out err code
  out="$("$@" 2>/tmp/control-cli-err)"; code=$?
  err="$(cat /tmp/control-cli-err)"; rm -f /tmp/control-cli-err
  set -e
  printf '%s\n' "$out"
  [ -n "$err" ] && printf '%s\n' "$err" >&2
  printf 'exit %d\n' "$code" >&2
  return "$code"
}

cmd_evidence() {
  [ "${1:-}" = "publish" ] || die 'usage: control evidence publish <run-id> <revision>'
  local run="${2:?run-id required}" rev="${3:?revision required}"
  local src="$ARTIFACTS/$run/$rev"
  [ -d "$src" ] || die "no artifacts at $src"
  # The renderer is device-owned. Publish into it; never start, restart, or
  # replace it, and never author a revision index.html by hand.
  curl -fsS --max-time 10 -X POST "$REVIEW_ORIGIN/_publish/$run/$rev" \
       -F "bundle=@<(cd "$src" && tar cz .)" >/dev/null \
    || die "publish failed. Is the renderer up on 8098? Do not start it yourself."
  printf 'MacBook review URL: %s/%s/%s/\n' "$REVIEW_ORIGIN" "$run" "$rev"
}

case "${1:-}" in
  doctor)   shift; cmd_doctor "$@" ;;
  browser)  shift; cmd_browser "$@" ;;
  cli)      shift; cmd_cli "$@" ;;
  evidence) shift; cmd_evidence "$@" ;;
  *) die 'usage: control-<app> {doctor|browser|cli|evidence}' ;;
esac

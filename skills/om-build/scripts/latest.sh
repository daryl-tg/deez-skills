#!/usr/bin/env bash
# @file latest.sh
# @brief Build origin/main of openmarket-internal and openmarket-chat and install it as the live om.
# @description
#   Fetches both repos, builds each origin/main without touching the checkouts
#   the operator works in, runs hosted.sh against them, and prints a short
#   summary on stdout. hosted.sh's full output goes to a log file.
#
#   openmarket-internal is always built from a temporary worktree at origin/main.
#   openmarket-chat is fast-forwarded and built in place when its checkout is a
#   clean main; on any other branch, or with local edits, origin/main is built
#   from a temporary worktree and the checkout is left as it is.
#
#   When neither origin/main moved since the last successful build and the
#   daemon answers, nothing is built. A build always passes --force to
#   hosted.sh, whose own gate skips CLI-only changes at an unchanged version.
#
#   Environment:
#     OM_MONO_REPO        openmarket-internal checkout (~/github/openmarket-internal)
#     OM_GUI_REPO         openmarket-chat checkout (~/gitlab/openmarket-chat)
#     OM_BUN_ROOT         directory holding bun-<version>/bun-darwin-aarch64/bun,
#                         used when the PATH bun is not the repo's .bun-version
#     OM_BUILD_STATE_DIR  last-build record and logs (~/.local/state/om-build)
#     OM_INSTALL_ROOT     versioned installs (~/.local/opt/openmarket)
#     OM_HOSTED_SH        the build to run (hosted.sh beside this script)
#     OM_HEALTH_URL       the daemon's health endpoint

set -euo pipefail

readonly MONO_REPO=${OM_MONO_REPO:-$HOME/github/openmarket-internal}
readonly GUI_REPO=${OM_GUI_REPO:-$HOME/gitlab/openmarket-chat}
readonly BUN_ROOT=${OM_BUN_ROOT:-$HOME/dev-notes-artifacts/om-agents-live-e2e/rig}
readonly STATE_DIR=${OM_BUILD_STATE_DIR:-$HOME/.local/state/om-build}
readonly INSTALL_ROOT=${OM_INSTALL_ROOT:-$HOME/.local/opt/openmarket}
readonly HEALTH_URL=${OM_HEALTH_URL:-http://127.0.0.1:31337/healthz}
readonly LOGS_KEPT=10

:usage() {
    cat <<EOF
Usage:
    latest.sh [--force]

Build origin/main of openmarket-internal and openmarket-chat and install it.

Options:
    --force     build even when nothing moved since the last build
    -h, --help  show this help
EOF
}

:parse-opts() {
    local mode=build
    while (($# > 0)); do
        case "$1" in
        --force) mode=force ;;
        -h | --help) mode=help ;;
        *) mode=bad ;;
        esac
        shift
    done
    printf '%s\n' "$mode"
}

:fail() {
    printf 'FAIL: %s\n' "$*"
    exit 1
}

:row() {
    printf '%-10s%s\n' "$1" "$2"
}

:hosted-sh() {
    if [[ -n ${OM_HOSTED_SH:-} ]]; then
        printf '%s\n' "$OM_HOSTED_SH"
        return 0
    fi
    printf '%s/hosted.sh\n' "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
}

# shellcheck disable=SC2329
:cleanup() {
    local work=$1
    if [[ -d $work/om ]]; then
        git -C "$MONO_REPO" worktree remove --force "$work/om" >/dev/null 2>&1 || true
    fi
    if [[ -d $work/chat ]]; then
        git -C "$GUI_REPO" worktree remove --force "$work/chat" >/dev/null 2>&1 || true
    fi
    rm -rf -- "$work"
    git -C "$MONO_REPO" worktree prune >/dev/null 2>&1 || true
    git -C "$GUI_REPO" worktree prune >/dev/null 2>&1 || true
}

:health:field() {
    local health=$1 key=$2
    sed -n "s/.*\"$key\":[[:space:]]*\"\{0,1\}\([^\",}]*\).*/\1/p" <<<"$health" | head -1
}

:git:subject() {
    git -C "$1" log -1 --format='%h %s' "$2"
}

:git:since() {
    local repo=$1 from=$2 to=$3 count
    [[ -n $from && $from != "$to" ]] || return 0
    count=$(git -C "$repo" rev-list --count "$from..$to" 2>/dev/null) || return 0
    printf '+%s since last build' "$count"
}

:state:read() {
    local line=$1
    sed -n "${line}p" "$STATE_DIR/last-build" 2>/dev/null || true
}

:bun:select() {
    local mono=$1 want have dir
    want=$(git -C "$mono" show origin/main:.bun-version 2>/dev/null | tr -d '[:space:]') || true
    [[ -n $want ]] || return 0
    have=$(bun --version 2>/dev/null || true)
    [[ $have == "$want" ]] && return 0
    dir=$BUN_ROOT/bun-$want/bun-darwin-aarch64
    [[ -x $dir/bun ]] || :fail "the repo needs Bun $want and PATH has ${have:-none}; put Bun $want at $dir/bun or set OM_BUN_ROOT"
    printf '%s\n' "$dir"
}

:gui:prepare() {
    local work=$1 branch dirty behind
    branch=$(git -C "$GUI_REPO" rev-parse --abbrev-ref HEAD)
    dirty=$(git -C "$GUI_REPO" status --porcelain)
    behind=$(git -C "$GUI_REPO" rev-list --count HEAD..origin/main)
    if [[ $branch == main && -z $dirty ]] && git -C "$GUI_REPO" merge --ff-only -q origin/main >/dev/null 2>&1; then
        if ((behind > 0)); then
            printf '%s\t%s\n' "$GUI_REPO" "main fast-forwarded"
        else
            printf '%s\t%s\n' "$GUI_REPO" "main"
        fi
        return 0
    fi
    git -C "$GUI_REPO" worktree add -q --detach "$work/chat" origin/main >/dev/null 2>&1 ||
        :fail "could not add a worktree of openmarket-chat origin/main"
    if [[ $branch != main ]]; then
        printf '%s\t%s\n' "$work/chat" "checkout stays on $branch"
    elif [[ -n $dirty ]]; then
        printf '%s\t%s\n' "$work/chat" "checkout on main has uncommitted changes, left alone"
    else
        printf '%s\t%s\n' "$work/chat" "checkout's main has diverged from origin, left alone"
    fi
}

:log:new() {
    mkdir -p "$STATE_DIR/logs"
    find "$STATE_DIR/logs" -name 'latest-*.log' -type f 2>/dev/null |
        sort -r | tail -n "+$LOGS_KEPT" | while read -r old; do rm -f -- "$old"; done
    printf '%s/logs/latest-%s.log\n' "$STATE_DIR" "$(date +%Y%m%d-%H%M%S)"
}

:log:field() {
    local log=$1 label=$2
    sed -n "s/^$label:[[:space:]]*//p" "$log" | head -1 | sed 's/[[:space:]]*$//'
}

:install:previous() {
    local version=$1
    find "$INSTALL_ROOT" -mindepth 1 -maxdepth 1 -type d -exec basename {} \; 2>/dev/null |
        {
            cat
            printf '%s\n' "$version"
        } | sort -uV | sed -n "/^${version//./\\.}\$/{x;p;q;};h"
}

:summary() {
    local log=$1 prior_version=$2 mono_line=$3 gui_line=$4 daemon version pid status
    local previous auth error consents
    daemon=$(:log:field "$log" daemon)
    version=${daemon%% *}
    pid=${daemon##* }
    if [[ -z $prior_version ]]; then
        status=" (daemon was down before the build)"
    elif [[ $prior_version != "$version" ]]; then
        status=" (was $prior_version)"
    else
        status=""
    fi
    :row om "$version running, pid $pid$status"
    :row internal "$mono_line"
    :row chat "$gui_line"
    :row gui "$(:log:field "$log" GUI)"
    auth=$(:log:field "$log" auth | sed 's/"type":"\([^"]*\)"/\1/; s/"username":"\([^"]*\)"/\1/')
    :row auth "${auth:-no handshake}"
    :row listener "$(:log:field "$log" listener)"
    :row mcp "$(:log:field "$log" 'mcp singleton')"
    previous=$(:install:previous "$version")
    if grep -q "^NOTE: overwriting $version in place" "$log"; then
        :row rollback "$version overwritten in place; previous install is ${previous:-none}"
    else
        :row rollback "${previous:-none} kept"
    fi
    error=$(:log:field "$log" 'last error')
    [[ -z $error ]] || :row error "$error"
    consents=$(grep -o '"status":"pending"' "$log" 2>/dev/null | wc -l | tr -d ' ' || true)
    ((consents == 0)) || :row consents "$consents pending (om agent grants requests --status pending)"
    :row log "$log"
}

:with-parens() {
    local subject=$1 since=$2 note=$3 extra
    extra="${since}${since:+${note:+; }}${note}"
    printf '%s%s\n' "$subject" "${extra:+ ($extra)}"
}

:main() {
    local mode work health prior_version mono_sha gui_sha last_mono last_gui
    local gui_dir gui_note bun_dir log status mono_line gui_line

    mode=$(:parse-opts "$@")
    case "$mode" in
    help)
        :usage
        exit 0
        ;;
    bad)
        :usage >&2
        exit 2
        ;;
    esac

    git -C "$MONO_REPO" fetch -q origin || :fail "fetch openmarket-internal"
    git -C "$GUI_REPO" fetch -q origin || :fail "fetch openmarket-chat"
    mono_sha=$(git -C "$MONO_REPO" rev-parse origin/main)
    gui_sha=$(git -C "$GUI_REPO" rev-parse origin/main)

    health=$(curl -s --max-time 5 "$HEALTH_URL" || true)
    prior_version=$(:health:field "$health" version)
    last_mono=$(:state:read 1)
    last_gui=$(:state:read 2)

    if [[ $mode != force && -n $prior_version && $mono_sha == "$last_mono" && $gui_sha == "$last_gui" ]]; then
        :row om "$prior_version, up to date"
        :row internal "$(:git:subject "$MONO_REPO" "$mono_sha")"
        :row chat "$(:git:subject "$GUI_REPO" "$gui_sha")"
        exit 0
    fi

    work=$(mktemp -d)
    # shellcheck disable=SC2064
    trap ":cleanup $(printf '%q' "$work")" EXIT
    trap 'exit 130' INT TERM

    git -C "$MONO_REPO" worktree add -q --detach "$work/om" origin/main >/dev/null 2>&1 ||
        :fail "could not add a worktree of openmarket-internal origin/main"
    IFS=$'\t' read -r gui_dir gui_note < <(:gui:prepare "$work")
    [[ -n $gui_dir ]] || :fail "could not prepare openmarket-chat"

    bun_dir=$(:bun:select "$work/om")
    log=$(:log:new)
    printf 'building internal %s, chat %s (log %s)\n' "${mono_sha:0:10}" "${gui_sha:0:8}" "$log" >&2

    status=0
    PATH="${bun_dir:+$bun_dir:}$PATH" OM_MONO="$work/om" OM_GUI="$gui_dir" \
        "$(:hosted-sh)" --force >"$log" 2>&1 || status=$?

    if ((status != 0)); then
        grep -m1 '^FAIL:' "$log" || printf 'FAIL: hosted.sh exited %s\n' "$status"
        tail -n 15 "$log" | sed 's/^/  /'
        :row log "$log"
        exit 1
    fi

    mkdir -p "$STATE_DIR"
    printf '%s\n%s\n' "$mono_sha" "$gui_sha" >"$STATE_DIR/last-build"

    mono_line=$(:with-parens "$(:git:subject "$MONO_REPO" "$mono_sha")" "$(:git:since "$MONO_REPO" "$last_mono" "$mono_sha")" "")
    gui_line=$(:with-parens "$(:git:subject "$GUI_REPO" "$gui_sha")" "$(:git:since "$GUI_REPO" "$last_gui" "$gui_sha")" "$gui_note")
    :summary "$log" "$prior_version" "$mono_line" "$gui_line"
    exit 0
}

:main "$@"

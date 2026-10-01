#!/usr/bin/env bash
# One unattended maintenance pass for a single repo, for launchd to call.
#
#   scheduled-run.sh <repo-path> <verify-skill-name>
#
# Quiet on `clean`, loud on `changed` or `blocked`. That asymmetry is the whole
# design: a scheduled check that reports success every night is one you stop
# reading, and then it is worse than no check.
#
# Exit: 0 clean or skipped, 2 changed, 3 blocked, 1 could not run.
# @file Scheduled project verification maintenance.
# @description Resolve the canonical hub skill and report exceptions.
set -uo pipefail

REPO="${1:?usage: scheduled-run.sh <repo-path> <verify-skill-name>}"
SKILL="${2:?usage: scheduled-run.sh <repo-path> <verify-skill-name>}"
STATE="${DEEZ_MAINTAIN_STATE:-$HOME/.local/state/deez-skills/maintain}"
HUB="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && cd ../../.. && pwd -P)" || exit 1
LOCKDIR="$STATE/$SKILL.lock.d"
LOG="$STATE/$SKILL.log"
mkdir -p "$STATE"

log() { printf '%s %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$*" >>"$LOG"; }
bail() {
	log "SKIP $*"
	exit 0
}

# One pass at a time, per skill. Two passes driving the same app race over the
# instance and the lane. macOS has no flock(1), so this is an atomic mkdir with
# stale detection: a lock is stale when its owner is gone, not when it is old.
# Per principle-make-operations-idempotent.
if ! mkdir "$LOCKDIR" 2>/dev/null; then
	OWNER="$(cat "$LOCKDIR/pid" 2>/dev/null || echo 0)"
	if [ "$OWNER" -gt 0 ] 2>/dev/null && kill -0 "$OWNER" 2>/dev/null; then
		bail "pass $OWNER already running"
	fi
	log "clearing stale lock from pid $OWNER"
	rm -rf "$LOCKDIR"
	mkdir "$LOCKDIR" 2>/dev/null || bail "could not take $LOCKDIR"
fi
printf '%s' "$$" >"$LOCKDIR/pid"
trap 'rm -rf "$LOCKDIR"' EXIT INT TERM

[ -d "$REPO" ] || bail "no repo at $REPO"

# Preconditions. A pass that cannot verify anything should not burn a lane
# announcing that.
SKILLDIR="$("$HUB/bin/deez" skill-path "$SKILL" 2>/dev/null)" || bail "$SKILL is not registered in the hub"
[ -f "$SKILLDIR/SKILL.md" ] || bail "$SKILL is not installed in the hub"
[ -d "$SKILLDIR/features" ] || bail "$SKILL has no feature map yet"

# New wrappers live with the project skill. Older operator wrappers may live in
# the product checkout or on PATH. Without one, every doctor call fails.
WRAPPER="$(sed -n 's/.*\(control-[a-z-]*\) doctor.*/\1/p' "$SKILLDIR/SKILL.md" | head -1)"
if [ -n "$WRAPPER" ] && [ ! -x "$SKILLDIR/bin/$WRAPPER" ] && [ ! -x "$REPO/$WRAPPER" ] && ! command -v "$WRAPPER" >/dev/null 2>&1; then
	bail "$WRAPPER missing or not executable for $SKILL"
fi

log "START $SKILL in $REPO"
OUT="$STATE/$SKILL.last-run.txt"
claude -p "Run maintain-verification-skill against $SKILL at $SKILLDIR for $REPO. Hub: $HUB. \
Unattended: do not ask questions. Stay inside the skill's edit scope, never \
touch product code. End your reply with a single final line reading exactly \
VERDICT: clean, VERDICT: changed, or VERDICT: blocked." \
	>"$OUT" 2>&1
RC=$?

VERDICT="$(grep -oE '^VERDICT: (clean|changed|blocked)' "$OUT" | tail -1 | awk '{print $2}')"
case "${VERDICT:-}" in
clean)
	log "clean"
	exit 0
	;;
changed)
	log "CHANGED -- verified corrections, see $OUT"
	cat "$OUT" >&2
	exit 2
	;;
blocked)
	log "BLOCKED -- see $OUT"
	cat "$OUT" >&2
	exit 3
	;;
*)
	log "NO VERDICT (claude rc=$RC) -- see $OUT"
	cat "$OUT" >&2
	exit 1
	;;
esac

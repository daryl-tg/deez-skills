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
PROMPT="First read and follow the current hub instructions at \
$HUB/skills/maintain-verification-skill/SKILL.md and the persistence contract at \
$HUB/docs/project-verification.md. Run that maintenance workflow for $SKILL in \
the product repository $REPO. Initial ownership lookup: $SKILLDIR.

Treat $SKILLDIR as the initial ownership lookup only, not automatically as the \
map edit target. Before editing a map, fetch current origin/main and inspect the \
hub's worktree status, upstream ancestry, and outgoing history. If the operator \
hub is dirty, behind origin/main, or has unrelated outgoing commits, create a \
detached isolated hub worktree from fetched origin/main. Resolve the project's \
canonical verification skill inside that worktree and use that actual isolated \
skill path for all map edits and the publisher. Leave the operator hub \
untouched. Honor .sync-hold from the original hub; report the proved maps as \
pending instead of publishing while it is present.

Inventory the product's full user-facing source surface, then reconcile that \
inventory against every existing feature-map entry. Add proved missing surfaces, \
and when live coverage is blocked, persist source-supported inventory gaps as \
explicitly pending where the shared contract permits. Do not limit the pass to \
features already present in the map. If some coverage is blocked, still persist \
each independently proved map correction and run the map-only automatic \
publisher for exactly those reviewed feature-map files. Report the publisher \
receipt: project path, map commit, push result, and remaining non-map changes. \
Never use broad bin/sync.

Unattended: do not ask questions. Stay inside the skill's edit scope and never \
touch product code. End your reply with a single final line reading exactly \
VERDICT: clean, VERDICT: changed, or VERDICT: blocked."
(
	cd "$REPO" || exit 1
	claude -p "$PROMPT"
) >"$OUT" 2>&1
RC=$?

if [ "$RC" -ne 0 ]; then
	log "CLAUDE FAILED (rc=$RC) -- see $OUT"
	cat "$OUT" >&2
	exit 1
fi

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

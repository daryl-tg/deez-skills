#!/usr/bin/env bash
# new-evidence-manifest.sh <run-id> <revision> "<one-line goal>"
#
# Scaffolds artifacts/<run-id>/<revision>/evidence-manifest.json with the branch,
# HEAD, and one caption slot per .png already in the directory. Run it AFTER
# capturing frames, fill in each "state" caption and the observations, then
# validate with: ./control-kiyotaka evidence check <run-id> <revision>
set -euo pipefail

run="${1:?usage: new-evidence-manifest.sh <run-id> <revision> \"<goal>\"}"
rev="${2:?revision required}"
goal="${3:?one-line goal required}"

REPO="${KIYO_REPO:-/Users/dboon/Gitlab/kiyotaka-frontend}"
dir="${ARTIFACTS:-$REPO/artifacts}/$run/$rev"
[ -d "$dir" ] || { printf 'no such artifact dir: %s\n' "$dir" >&2; exit 1; }

branch="$(git -C "$REPO" rev-parse --abbrev-ref HEAD 2>/dev/null || echo unknown)"
head="$(git -C "$REPO" rev-parse --short HEAD 2>/dev/null || echo unknown)"
dirty="$([ -n "$(git -C "$REPO" status --porcelain 2>/dev/null)" ] && echo true || echo false)"

python3 - "$dir" "$run" "$rev" "$goal" "$branch" "$head" "$dirty" <<'PY'
import json, pathlib, sys
dir_, run, rev, goal, branch, head, dirty = sys.argv[1:8]
d = pathlib.Path(dir_)
pngs = sorted(p.name for p in d.glob("*.png"))
manifest = {
    "runId": run,
    "revision": rev,
    "goal": goal,
    "tree": {"branch": branch, "head": head, "dirty": dirty == "true"},
    "lane": "guest",
    "captures": [
        {"path": name, "state": "TODO: what this frame shows and why it proves the claim"}
        for name in pngs
    ],
    "engineState": "TODO: the window.tc read that is the side effect (overlays, rawData.length)",
    "observations": "TODO: what you saw, INCLUDING anything you could not prove",
}
out = d / "evidence-manifest.json"
out.write_text(json.dumps(manifest, indent=2) + "\n")
print(f"wrote {out} with {len(pngs)} capture slot(s)")
if not pngs:
    print("WARNING: no .png frames found — capture frames first, then re-run")
PY

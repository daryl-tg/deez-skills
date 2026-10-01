#!/usr/bin/env bash
# new-evidence-manifest.sh <run-id> <revision> "<one-line goal>"
#
# Scaffolds artifacts/<run-id>/<revision>/evidence-manifest.json in the schema
# the OpenFloor renderer reads, with baseline/candidate commits and a diff hash
# read from the working tree, and one captures[] slot per *.png already in the
# directory. Run it AFTER capturing frames, then fill in every "state" caption.
set -euo pipefail

run="${1:?usage: new-evidence-manifest.sh <run-id> <revision> \"<goal>\"}"
rev="${2:?revision required}"
goal="${3:?one-line goal required}"

repo="$(git rev-parse --show-toplevel)"
dir="$repo/artifacts/$run/$rev"
[ -d "$dir" ] || { echo "no such directory: $dir" >&2; exit 1; }
ls "$dir"/*.png >/dev/null 2>&1 || { echo "no .png frames in $dir — capture first" >&2; exit 1; }

base_ref="${BASE_REF:-origin/main}"
base_commit="$(git rev-parse "$base_ref" 2>/dev/null || echo unknown)"

python3 - "$dir" "$run" "$rev" "$goal" "$base_ref" "$base_commit" <<'PY'
import hashlib, json, pathlib, subprocess, sys

dir_, run, rev, goal, base_ref, base_commit = sys.argv[1:7]
d = pathlib.Path(dir_)

def git(*a):
    try:
        return subprocess.check_output(["git", *a], text=True).strip()
    except subprocess.CalledProcessError:
        return "unknown"

diff = subprocess.run(["git", "diff", f"{base_commit}...HEAD"],
                      capture_output=True, text=True).stdout
manifest = {
    "runId": run,
    "revision": rev,
    "goal": goal,
    "baseline": {"commit": base_commit, "ref": base_ref},
    "candidate": {"commit": git("rev-parse", "HEAD"), "tree": git("rev-parse", "HEAD^{tree}")},
    "featureDiffHash": "sha256:" + hashlib.sha256(diff.encode()).hexdigest(),
    "captures": [
        {
            "path": p.name,
            "state": "TODO: what this frame shows, and what it proves",
            "sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
        }
        for p in sorted(d.glob("*.png"))
    ],
    "captureProvenance": "agent-device on a booted iOS simulator against Metro on 127.0.0.1:8081.",
    "verificationDelta": [
        "TODO: anything only real hardware proves (push delivery, Keychain, "
        "background lifecycle, a SQL migration over a previous build's database), "
        "or anything you attempted and could not reach.",
    ],
}
out = d / "evidence-manifest.json"
out.write_text(json.dumps(manifest, indent=2) + "\n")
print(f"{out}  ({len(manifest['captures'])} capture slot(s) to caption)")
PY

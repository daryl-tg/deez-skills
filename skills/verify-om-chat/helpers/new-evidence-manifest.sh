#!/usr/bin/env bash
# new-evidence-manifest.sh <run-id> <revision> "<one-line goal>"
#
# Scaffolds artifacts/<run-id>/<revision>/evidence-manifest.json in the omrx
# schema the 8098 review renderer actually reads, with one caption slot per PNG
# already sitting in that directory.
#
# The renderer fills its template from this file. `capture.screenshots` MUST be
# a filename -> caption MAP; an array of objects publishes HTTP 200 with an
# empty gallery, which looks published and reviews as nothing.
#
# Run it AFTER capturing frames, from the repo root, then edit the captions and
# the browserEvidence facts by hand — the scaffold cannot know what you saw.
set -euo pipefail

run="${1:?usage: new-evidence-manifest.sh <run-id> <revision> "'"<goal>"'"}"
rev="${2:?revision required}"
goal="${3:?one-line goal required}"

repo="$(git rev-parse --show-toplevel)"
dir="$repo/artifacts/$run/$rev"
[ -d "$dir" ] || { printf 'no artifact directory at %s — capture frames first\n' "$dir" >&2; exit 1; }

shots=("$dir"/*.png)
[ -e "${shots[0]}" ] || { printf 'no .png frames in %s — capture frames first\n' "$dir" >&2; exit 1; }

out="$dir/evidence-manifest.json"
[ -e "$out" ] && { printf '%s already exists; edit it or remove it first\n' "$out" >&2; exit 1; }

branch="$(git -C "$repo" rev-parse --abbrev-ref HEAD)"
head_sha="$(git -C "$repo" rev-parse HEAD)"
# The feature diff, not the commit: a revision is invalidated by what changed in
# the working tree, which is what a reviewer is being asked to approve.
diff_sha="$(git -C "$repo" diff HEAD | shasum -a 256 | cut -d' ' -f1)"

entries=""
for shot in "${shots[@]}"; do
  name="$(basename "$shot")"
  [ -n "$entries" ] && entries="$entries,"
  entries="$entries
      \"$name\": \"TODO caption: what this frame shows and why it is evidence\""
done

cat > "$out" <<JSON
{
  "runId": "$run",
  "revision": "$rev",
  "goal": "$goal",
  "capturedAt": "$(date +%Y-%m-%d)",
  "repository": "$(basename "$repo")",
  "branch": "$branch",
  "baselineCommit": "$head_sha",
  "candidateCommit": "$head_sha",
  "diffSha256": "$diff_sha",
  "classification": "TODO: what this change touches, and what it does not",
  "capture": {
    "route": "TODO: the exact fixture route, query string included",
    "viewport": "TODO: e.g. 1440x900",
    "surface": "TODO: e.g. desktop web, run-owned vite lane on 127.0.0.1:18099",
    "state": "TODO: the seeded state these frames were taken in",
    "screenshots": {$entries
    }
  },
  "browserEvidence": {
    "routeChange": "TODO: what the URL did",
    "sideEffect": "TODO: what changed besides the thing you clicked",
    "console": "TODO: errors and warnings seen, or none",
    "accessibility": "TODO: axe result, or not run"
  },
  "validation": {
    "doctor": "TODO: control-om-chat doctor result",
    "targetedTests": "TODO: which tests you ran and their counts"
  }
}
JSON

printf 'wrote %s\n' "$out"
printf 'Fill every TODO, then: ./control-om-chat evidence publish %s %s\n' "$run" "$rev"

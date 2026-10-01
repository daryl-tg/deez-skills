#!/usr/bin/env bash
# new-evidence-manifest.sh <run-id> <revision> "<one-line goal>"
#
# Scaffolds artifacts/<run-id>/<revision>/evidence-manifest.json in the omrx
# schema the 8098 review renderer actually reads, with one caption slot per PNG
# already sitting in that directory and an inventory of the non-image artifacts
# beside them (SSE captures, JSON results, log tails).
#
# The renderer fills its template from this file. `capture.screenshots` MUST be
# a filename -> caption MAP; an array of objects publishes HTTP 200 with an
# empty gallery, which looks published and reviews as nothing. It also needs at
# least one image: a CLI-only revision renders a gallery with no frames and
# `control-om evidence publish` refuses it. Capture one dashboard frame even
# when the claim is about the CLI.
#
# Run it AFTER capturing, from the repo root, then edit the captions and the
# daemonEvidence facts by hand — the scaffold cannot know what you saw.
set -euo pipefail

run="${1:?usage: new-evidence-manifest.sh <run-id> <revision> "'"<goal>"'"}"
rev="${2:?revision required}"
goal="${3:?one-line goal required}"

repo="$(git rev-parse --show-toplevel)"
dir="$repo/artifacts/$run/$rev"
[ -d "$dir" ] || { printf 'no artifact directory at %s — capture first\n' "$dir" >&2; exit 1; }

shopt -s nullglob
shots=("$dir"/*.png)
[ "${#shots[@]}" -gt 0 ] || {
  printf 'no .png frames in %s — the renderer needs at least one image or the gallery publishes empty\n' "$dir" >&2
  exit 1
}

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

others=""
for f in "$dir"/*; do
  case "$f" in *.png|"$out") continue ;; esac
  name="$(basename "$f")"
  [ -n "$others" ] && others="$others, "
  others="$others\"$name\""
done
[ -z "$others" ] && others=""

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
    "route": "TODO: the exact route or command under test",
    "viewport": "TODO: e.g. 1440x900",
    "surface": "TODO: e.g. run-owned om lane, source build, 127.0.0.1:18101",
    "state": "TODO: the lane state these artifacts were taken in (guest? seeded how?)",
    "screenshots": {$entries
    },
    "files": [$others]
  },
  "daemonEvidence": {
    "correlationId": "TODO: the event_id / watch slug every artifact shares",
    "door": "TODO: what the HTTP or CLI door answered, with status code and exit code",
    "stream": "TODO: which /events/v1 events arrived, in order",
    "sideEffect": "TODO: the stored state you re-read, and where from",
    "secondSurface": "TODO: the other surface that agrees, and on what value",
    "log": "TODO: errors and warnings in the lane log, or none"
  },
  "validation": {
    "doctor": "TODO: control-om doctor result",
    "omDoctor": "TODO: om doctor warnings, and which are the expected guest-lane shape",
    "targetedTests": "TODO: which tests you ran and their counts"
  }
}
JSON

printf 'wrote %s\n' "$out"
printf 'Fill every TODO, then: ./control-om evidence publish %s %s\n' "$run" "$rev"

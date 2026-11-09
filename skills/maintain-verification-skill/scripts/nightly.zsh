#!/bin/zsh -l
# @file nightly.zsh
# @brief Run maintain-verification-skill for every mapped project, one at a time.
# @description launchd calls this from com.dboon.verify-maintenance.plist at 03:17.
#   Each pass is a headless claude -p session with its own report and log.
#   Touch a project's .sync-hold in the hub to pause its map publication.
# @example
#   nightly.zsh
#   nightly.zsh verify-om verify-om-chat
#   nightly.zsh --sweep 20261109
set -u
export PATH="$HOME/.local/bin:/opt/homebrew/bin:$PATH"

typeset -A REPO=(
  verify-om        "$HOME/github/openmarket-internal"
  verify-om-chat   "$HOME/github/openmarket-chat"
  verify-kiyotaka  "$HOME/Gitlab/kiyotaka-frontend"
  verify-kiyotaka-desktop "$HOME/Gitlab/kiyotaka-frontend"
)
ORDER=(verify-om verify-om-chat verify-kiyotaka verify-kiyotaka-desktop)
SWEEP_TAGS=()
if [[ ${1:-} == --sweep ]]; then shift; SWEEP_TAGS=("$@"); ORDER=()
elif (( $# )); then ORDER=("$@"); fi

RUN_TIMEOUT_S=${VM_RUN_TIMEOUT_S:-$(( 4 * 3600 ))}
IDLE_TIMEOUT_S=${VM_IDLE_TIMEOUT_S:-$(( 30 * 60 ))}
POLL_S=${VM_POLL_S:-60}
CLAUDE_BIN=${VM_CLAUDE_BIN:-claude}
LOGS=${VM_LOGS:-"$HOME/Library/Logs/verify-maintenance"}
REPORTS=${VM_REPORTS:-"$HOME/Documents/dev-notes/maintain-verification-skill/nightly"}
STATE=${VM_STATE:-"$HOME/.local/state/verify-maintenance"}
SCRATCH="$STATE/scratch"
ART=${VM_ART:-"$HOME/dev-notes-artifacts/maintain-verification-skill/run-artifacts"}
HUB=${VM_HUB:-"$HOME/github/deez-skills"}
PRODUCT_REPOS=("$HOME/github/openmarket-internal" "$HOME/gitlab/openmarket-chat" "$HOME/Gitlab/kiyotaka-frontend")
[[ -n ${VM_PRODUCT_REPOS:-} ]] && PRODUCT_REPOS=(${=VM_PRODUCT_REPOS})
KEEP_DAYS=${VM_KEEP_DAYS:-14}
mkdir -p "$LOGS" "$REPORTS" "$STATE" "$SCRATCH" "$ART" "$HOME/.claude/.worktree-decisions"

in_use() {
  lsof -d cwd -Fn 2>/dev/null | sed -n 's/^n//p' | grep -qF -- "$1"
}

worktrees() {
  git -C "$1" worktree list --porcelain 2>/dev/null | sed -n 's/^worktree //p' | grep -F -- "$2"
}

sweep() {
  local tag=$1 repo wt d kept=()
  for repo in $PRODUCT_REPOS; do
    for wt in ${(f)"$(worktrees "$repo" /)"}; do
      for d in "$wt"/artifacts/*nightly-$tag(N/); do
        rm -rf "$ART/${d:t}"; mv "$d" "$ART/"
      done
    done
    for wt in ${(f)"$(worktrees "$repo" "-nightly-$tag")"}; do
      if [[ -n $(git -C "$wt" status --porcelain 2>/dev/null) ]]; then kept+=("$wt: uncommitted changes")
      elif in_use "$wt"; then kept+=("$wt: in use")
      else
        [[ -d $wt/artifacts ]] && cp -R "$wt/artifacts/." "$ART/"
        git -C "$repo" worktree remove --force "$wt" 2>/dev/null || kept+=("$wt: remove failed")
      fi
    done
    git -C "$repo" worktree prune 2>/dev/null
  done
  git -C "$HUB" fetch -q origin 2>/dev/null
  for wt in ${(f)"$(worktrees "$HUB" deez-skills-maintain-)"}; do
    [[ ${wt:t} == *-$tag || ${wt:t} == *-$tag-* ]] || continue
    if [[ -n $(git -C "$wt" status --porcelain 2>/dev/null) ]]; then kept+=("$wt: uncommitted changes")
    elif in_use "$wt"; then kept+=("$wt: in use")
    elif ! git -C "$wt" symbolic-ref -q HEAD >/dev/null &&
         ! git -C "$HUB" merge-base --is-ancestor "$(git -C "$wt" rev-parse HEAD)" origin/main; then
      kept+=("$wt: unpublished commits on a detached HEAD")
    else
      git -C "$HUB" worktree remove --force "$wt" 2>/dev/null || kept+=("$wt: remove failed")
    fi
  done
  git -C "$HUB" worktree prune 2>/dev/null
  rm -rf "$SCRATCH"/$tag-*(N)
  (( ${#kept} )) && print -l -- $kept
  return 0
}

expire() {
  find "$LOGS" -maxdepth 1 -name '20*' -mtime +$KEEP_DAYS -delete
  find "$ART" -maxdepth 1 -name '*nightly-*' -mtime +$KEEP_DAYS -exec rm -rf {} +
  find "$SCRATCH" -mindepth 1 -maxdepth 1 -mtime +1 -exec rm -rf {} +
}

LOCK="$STATE/lock"
if ! mkdir "$LOCK" 2>/dev/null; then
  if [[ -n $(find "$LOCK" -maxdepth 0 -mmin +1440 2>/dev/null) ]]; then
    rm -rf "$LOCK"; mkdir "$LOCK"
  else
    echo "$(date '+%F %T') another nightly holds $LOCK; exiting"; exit 0
  fi
fi
trap 'rm -rf "$LOCK"' EXIT

if (( ${#SWEEP_TAGS} )); then
  for tag in $SWEEP_TAGS; do
    echo "$(date '+%F %T') sweep $tag"
    sweep "$tag" | sed 's/^/  kept: /'
  done
  expire
  exit 0
fi

day=$(date +%F)
tag=${day//-/}
for skill in "${ORDER[@]}"; do
  repo=${REPO[$skill]:-}
  if [[ -z $repo || ! -d $repo ]]; then
    echo "$(date '+%F %T') $skill: no repo mapped or missing ($repo); skipped"; continue
  fi

  sid=$(uuidgen | tr 'A-Z' 'a-z')
  touch "$HOME/.claude/.worktree-decisions/$sid"
  report="$REPORTS/$day-$skill.md"
  log="$LOGS/$day-$skill.jsonl"
  scratch="$SCRATCH/$tag-$skill"
  mkdir -p "$scratch"

  prompt="/maintain-verification-skill $skill

This is an unattended nightly run started by launchd; nobody is watching.
- Never ask a question. Where the skill says to ask, take the safe default, or end the pass as blocked and say why.
- The worktree decision for this session is already recorded.
- Other runs may hold ports. Take a free agent-owned slot and never stop a process you did not start.
- Name every worktree you create with the suffix -nightly-$tag (product) or -$tag (deez-skills hub). Put scratch scripts and logs in $scratch, not /tmp. Put evidence under $ART/<run-id>/.
- Clean up before you finish: stop your lanes and browser sessions, and remove every worktree, lane home and scratch file you created. Keep a worktree only if it holds uncommitted or unpushed work, and name it in the report.
- At the end, write a short report to $report: outcome (clean, changed or blocked), changed map paths, the commit and push result, product gaps, and gaps that remain.
- The report must include a section headed exactly '## Changelog': a Markdown table with columns File | Change | Proof, one row per map file in the published commit. Change is one line: new, edited or removed, then what changed for a reader of the map. Proof is live, source or stamp-only. If nothing was published, write 'No map changes.' under the heading."

  echo "$(date '+%F %T') $skill: start (session $sid, cwd $repo)"
  (
    cd "$repo" || exit 1
    exec "$CLAUDE_BIN" -p "$prompt" \
      --session-id "$sid" \
      --permission-mode bypassPermissions \
      --output-format stream-json --verbose </dev/null
  ) >"$log" 2>&1 &
  pid=$!
  started=$(date +%s); tick=$started; awake_since=$started; why=""
  while kill -0 $pid 2>/dev/null; do
    sleep $POLL_S
    now=$(date +%s)
    (( now - tick > 3 * POLL_S )) && awake_since=$now
    tick=$now
    last=$(stat -f %m "$log" 2>/dev/null || echo $started)
    (( last < awake_since )) && last=$awake_since
    if (( now - started >= RUN_TIMEOUT_S )); then
      why="hit the $(( RUN_TIMEOUT_S / 60 )) min cap"
    elif (( now - last >= IDLE_TIMEOUT_S )); then
      why="log silent for $(( (now - last) / 60 )) min"
    fi
    if [[ -n $why ]]; then
      echo "$(date '+%F %T') $skill: killing, $why"
      kill -TERM $pid 2>/dev/null
      for _ in {1..30}; do kill -0 $pid 2>/dev/null || break; sleep 1; done
      kill -KILL $pid 2>/dev/null
      break
    fi
  done
  wait $pid; rc=$?
  echo "$(date '+%F %T') $skill: exit $rc${why:+ ($why)} (log $log)"
  [[ -f $report ]] || printf '# %s %s\n\nNo report written. Exit %s%s. Log: %s\n' "$skill" "$day" "$rc" "${why:+, killed: $why}" "$log" >"$report"
  kept=$(sweep "$tag")
  if [[ -n $kept ]]; then
    echo "$(date '+%F %T') $skill: sweep kept:"; print -r -- "$kept" | sed 's/^/  /'
    printf '\n## Kept after cleanup\n\n%s\n' "$(print -r -- "$kept" | sed 's/^/- /')" >>"$report"
  fi
done
expire
echo "$(date '+%F %T') nightly done $day: ${ORDER[*]}"

---
name: herdr-codex-orchestration
description: "Run independent Codex implementation, review, and verification loops through Herdr with isolated worktrees. Covers arena mode (N candidates, one judge) and swarm mode (N slices, one report). Never merges or mutates local main."
---

# Herdr Codex orchestration

Read the canonical policy before acting:
`/Users/dboon/Documents/dev-notes/herdr-codex-orchestration.md`.

## Preflight

Require a Herdr-managed pane:

```sh
test "${HERDR_ENV:-}" = 1
```

Keep every primary worktree untouched while workers run. Create one integration
worktree and non-overlapping worker worktrees. The designated primary worktree
is used only once, at final promotion, and must be clean, on local `main`, and
free of an active user/run task.

Name every Herdr-created branch `daryl/<short-feature-summary>`, with no more
than five lowercase kebab-case words after the slash
(`^daryl/[a-z0-9]+(?:-[a-z0-9]+){0,4}$`). Keep worker summaries concise enough
to fit; do not add generated dates, hashes, or an alternate prefix.

## Execution

1. Create isolated worker worktrees and one integration branch/worktree.
2. Give each worker exact ownership, acceptance criteria, allowed writes, and
   validation commands. Do not overlap files or revert another worker's work.
3. Let workers commit coherent local changes. Integrate only through local
   rebase/cherry-pick; never use `git merge`.
4. Run final UI evidence in one integration QA lane. Use `$agent-browser`, a
   unique session per revision, and recorded `18097`–`18197` test ports. Never
   use `8097`; publish evidence only through the singleton `8098` renderer.
   Write the manifest and screenshots below its evidence root, verify the exact
   `8098/<run-id>/<revision>/` gallery returns HTTP 200 with the renderer
   header, and report that URL. Never present a test-server URL or fallback port.
   The full reserved-port table is `## Reserved ports` in `~/.claude/CLAUDE.md`; take an assigned port, never a merely-free one.
5. Use shared `openmarket` HTTP MCP on `31338`; per-session `openmarket-chat`
   stdio children are worker-owned and released at exit.
6. For shared OM Chat behavior, assemble desktop first, refresh sync metadata,
   then sync and verify cloud. Do not promote an intermediate worker result.
7. After all accepted slices are assembled and verified, invoke
   `$delivery-contract` once to consolidate the integration branch and move it
   into the designated primary worktree, push that feature branch only, and
   create/reuse its review request. It must not mutate local `main`.
8. After every final review request exists, announce once through `$om-chat`,
   keeping the post short: a plain short title of what changed, a blank line,
   one to three present-tense sentences of observable behavior one per line,
   then the labeled review-request links and nothing after them. Never paste
   the review-request body or its `Summary:`/`Problem:`/`Solution:`/`How to
   test:` structure into chat. Read it back. Do not announce an intermediate
   worker result or close a todo.

The terminal state is `ready_for_review`. Never fetch, pull, merge, push local
`main`, or close a todo.

## Cleanup

Record reports and commit hashes before cleanup. Stop only recorded worker
runtime, preserve approved evidence, and remove only clean, exclusively owned
worker/integration worktrees after their branch is promoted. Retain the promoted
branch checked out in the primary worktree for the operator. Never close a
user-created Herdr pane, tab, workspace, or session.

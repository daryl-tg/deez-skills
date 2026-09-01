---
name: git
description: >-
  Version-control workflow: commits, staging, rebasing, branching,
  minimal diffs, and commit messages.
---
## Scope

Use this workflow for local git discipline while
planning and staging code changes.

Not for remote operations unless the user explicitly
asks.

## Core rules

- Never push, pull, fetch, or interact with any remote
  unless the user explicitly asks.
- Never use `git stash`. Not even if the user asks.
- Never switch branches unless the user explicitly
  asks.
- Never commit unless the user explicitly asks.
- Do not mix unrelated changes in one commit.

## Workflow

1. Plan the logical commit split before editing.
2. Keep each patch minimal and self-contained.
3. For bugfixes, reproduce first and keep the failing
   test separate from the fix.
4. Stage per commit. Use `git add -p` when one file
   spans multiple commits.
5. Review staged content with `git diff --cached`
   before any commit.
6. Scan staged files for secrets before committing.
7. Write multi-line commit messages with a heredoc,
   not `\n` inside quoted shell strings.
8. If the user did not ask for a commit, leave the
   worktree and index in a clean, explainable state.

## Commit planning

Commit structure determines how you plan changes.
Before touching any file, decide how the work
breaks into independent, self-contained commits. Each
commit should apply cleanly on its own, pass tests on
its own, and make sense to a reviewer reading it in
isolation.

If a task requires five logical changes, plan five
commits before writing the first line.

## Minimal diffs

Every added, removed, or moved line is a cost. Prefer
the smallest diff that achieves the goal. Do not
reorganize, reformat, or rename things outside the
patch scope. Do not clean up adjacent code unless that
cleanup is the point of the commit.

When implementing a feature, look for the approach
that touches the fewest files and lines.

## Commit granularity

One logical change per commit. A logical change is the
smallest unit that moves the codebase from one
consistent state to another. When in doubt, split.

## Bugfixes

When fixing a bug, start by reproducing it. Write a
test that exposes the broken behavior and commit that
test first, before writing any fix. The test must fail
against the current code.

Then fix the bug in a separate commit. The fix commit
turns the failing test green, and nothing else.

Plan both commits before writing any code.

## Commit messages

Subject line format:

    <area>: <what changed>

The area is the subsystem, package, module, component,
or file affected. The subject completes the sentence
"When applied, this patch will ...". Use imperative
mood. Do not add a trailing period. Keep the subject
under 72 characters.

    parser: reject unterminated string literals
    tls: add client certificate support
    cmd/serve: fix crash on empty config file
    docs: document the retry backoff strategy

The body, separated by a blank line, explains what the
diff does not make obvious. If the diff is
self-explanatory, the body can be short or absent.
Wrap body lines at 72 characters.

Reference tickets at the bottom as a trailer:

    Issue: PROJ-1234

If there is no ticket, omit the line.

When running `git commit` from the shell, use a
heredoc for any message with a body. Write the subject,
blank line, body, and trailers literally. Do not put
`\n` inside quoted `-m` arguments and expect the shell
to turn them into newlines.

```bash
git commit -F - <<'EOF'
config: remove unknown and unused fields

Drop config keys that kolint shows the service
does not consume.
EOF
```

## Staging

Use `git add -p` when a file spans multiple commits.
Review with `git diff --cached` before committing.

Scan staged files for secrets before committing. Warn
the user and do not proceed until acknowledged.

## Merge requests

Only when the user explicitly asks: use `glab` to
create a merge request. Do not offer or suggest this
unprompted.

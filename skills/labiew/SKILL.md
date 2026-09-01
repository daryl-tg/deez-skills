---
name: labiew
description: >-
  GitLab MR review comments and response planning for the current branch.
---
Use this skill when the repo already has `glab` and
`labiew` configured and the goal is to inspect the
merge request for the current branch.

## Workflow

1. Work from the repo root. Check the current branch
   with `git branch --show-current`.
2. Start with `glab mr view`. This is the normal path.
   It usually resolves the MR for the current branch
   and prints the MR URL.
3. If `glab mr view` does not find an MR, try
   `glab mr view <branch>`. If there is still no MR,
   stop and tell the user.
4. Use `labiew -Po <url>` when you want the overview,
   activity, and changed-file list.
5. Use `labiew -Pd <url>` when you need the full diff
   with inline discussion threads.
6. If the diff is large, redirect `labiew -Pd` output
   to a temp file and inspect that file with search
   tools instead of rerunning the command.
7. Turn the review into a plan: list the unresolved
   reviewer asks, point to the relevant file or hunk,
   and say what change is likely needed.
8. Do not edit code until the user asks. Start with
   triage and planning.

## Response shape

Report back with:

- MR title and URL
- short status summary
- actionable comments grouped by file or topic
- open questions or ambiguous threads
- suggested implementation order

## Rules

- Prefer the simple text workflow. Do not jump to
  JSON, `glab mr list`, or helper scripts unless the
  direct `glab mr view` path fails.
- Treat reviewer comments as the source of truth. Use
  the diff to recover context.
- Separate concrete change requests from approvals,
  status noise, and already-resolved back-and-forth.
- When a thread is ambiguous, quote the exact comment
  and say what is unclear.

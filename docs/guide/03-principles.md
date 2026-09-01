# 3. Principles

Seventeen leaf skills, one rule each. Playbooks **cite** them; they never
restate them.

## The problem they solve

Before this layer, the rule "never merge to main" appeared in three skills,
worded differently each time, inside the `description` field — the part loaded
into every session. Three copies, three drifting wordings, three places to
change when you change your mind, and you pay for all three.

Thirteen of the seventeen were extracted from rules the existing skills already
asserted. The count of how many files asserted each is the evidence it was real:

| Principle | Was in |
|---|---|
| `prove-on-the-real-surface` | 14 files |
| `visual-approval-gates-delivery` | 14 |
| `bind-assigned-ports` | 14 |
| `planning-docs-live-outside-the-repo` | 12 |
| `announce-the-linked-review` | 12 |
| `feature-branch-isolation` | 11 |
| `promote-to-the-main-worktree` | 11 |

## How citation works

A playbook step reads:

```markdown
5. Promote the branch. Apply **principle-rebase-pr-squash**
   and **principle-one-commit-lands**.
```

Not the rule spelled out again. `bin/doctor` fails on a citation with no
matching registry entry, which is how a rule referenced but never written gets
caught — it happened once during the build.

## Why they install on both runtimes

A handoff to Codex cites principles by name. That citation only resolves if the
leaf exists on Codex too. A principle missing there is a silently truncated
instruction, so the registry **rejects** one not installed on both.

## Why they are invisible

Every principle carries `disable-model-invocation: true`, so it never fires on a
description match — only when a step routes to it. On Claude that also means it
costs nothing at session start.

Codex ignores the flag, tested and confirmed. There the only lever is not
installing something, which is what profiles are for.

Next: [Verification](./04-verification.md).

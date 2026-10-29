---
name: principle-code-speaks-for-itself
description: "Apply whenever you write or edit code. Never add a comment that explains the code or your work on it. Say it with names, types, smaller functions, and tests; your work goes in the commit message and the review."
disable-model-invocation: true
---

# Code speaks for itself

Never write a comment that explains code, or explains what you did to it.

**Why:** agents do most of the work in these repos. An agent reads a comment as
truth and copies it, but nothing checks a comment against the code, so it drifts
while the code keeps changing. A comment that narrates your change is worse: it
is true for one commit and misleading forever after. The commit message and the
review request are where a change gets explained, and they stay attached to the
change that made them true.

**What is banned.**

- Notes about your work: "added X to handle Y", "fixed by…", "now uses…",
  "changed because…", "new:", "moved from…".
- What-it-does narration, why-notes, and docstrings or JSDoc that describe
  behavior.
- Section banners, TODOs, and commented-out code.

**What to do instead.** When code seems to need explaining, change the code: a
name that says what it holds, a type that rules out the wrong state, a smaller
function with a clear name, or a test that shows the behavior. If the reason
for a change matters, write it in the commit message.

**Allowed, because a tool or the law reads them:** shebangs, lint and type
pragmas (`# shellcheck disable=…`, `// eslint-disable-next-line`,
`# type: ignore`), build tags (`//go:build`), and a license header a repo
requires. A suppression is still a last resort, not a way around a fix.

**The one exception:** shdoc tags in maintained shell scripts, which
**ancient-shell-style** requires because shdoc generates the reference docs
from them.

**Existing comments.** Do not mass-delete them in code you are not changing.
When your edit touches code that carries an explanatory comment, remove the
comment and make the code say it instead.

This overrides any instruction to match a file's existing comment density.
Pairs with **principle-minimize-reader-load**: the reader an explanatory comment
helps is better served by code that needs no help.

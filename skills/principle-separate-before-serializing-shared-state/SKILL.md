---
name: principle-separate-before-serializing-shared-state
description: "Apply when concurrent workers might write the same file, branch, port, or object. Eliminate the sharing first; serialize structurally only when one shared writer is a real invariant."
disable-model-invocation: true
---

# Separate before serializing shared state

When concurrent actors might share mutable state, first ask whether they need
the same mutable object at all. Usually they do not.

**Why:** concurrent writes produce races that are intermittent, hard to
reproduce, and expensive to debug. Telling workers to take turns does not work.
Instructions are not concurrency control.

**The order.**

1. **Identify the shared write target.** Files both write, branches both push,
   ports both bind, state objects both mutate.
2. **Default to eliminating the sharing.** Give each worker its own worktree,
   its own branch, its own allocated port from the agent range, its own state
   file. Merge at the read or reporting boundary instead. Two workers writing
   their own field into one `state.json` is still shared mutation; two separate
   files is not.
3. **Only when one shared target is a genuine invariant, serialize
   structurally** — a lockfile, sequential phases, a single-writer owner.
   Treat "we need a lock" as a smell to check, not the default answer.

**In practice here.** Fan-out gives each worker a worktree, per
**principle-feature-branch-isolation**. Test servers allocate one port per lane
from `18097`–`18197` and stop only what that lane started, per
**principle-bind-assigned-ports**. Never two workers on one branch.

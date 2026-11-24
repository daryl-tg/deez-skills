---
name: principle-separate-before-serializing-shared-state
description: "Apply when concurrent workers might write the same file, branch, port, or object. Eliminate the sharing first; serialize structurally only when one shared writer is a real invariant."
disable-model-invocation: true
---

# Separate before serializing shared state

When concurrent actors might write the same file, branch, port, or object, first
ask whether they need one shared object or are publishing independent facts.
Default to giving each actor its own worktree, branch, port, or state file, and
merge only where the state is read. Two workers writing their own field into one
`state.json` is still shared mutation. Two separate files is not.

Only when one shared write target is a real invariant, serialize access
structurally (a lockfile, a single writer, running in sequence, compare-and-swap).
Instructions are not concurrency control, and "we need a lock" is a smell to
check first.

Here, fan-out gives each worker a worktree, per
**principle-feature-branch-isolation**. Test servers take one port per lane from
`18097` to `18197` and stop only what that lane started, per
**principle-bind-assigned-ports**. Never put two workers on one branch.

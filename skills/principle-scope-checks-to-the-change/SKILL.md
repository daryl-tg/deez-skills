---
name: principle-scope-checks-to-the-change
description: "Apply before any typecheck, test run, lint, or build. Run only the checks that cover what you changed. Whole-repo gates run only when the operator asks for them."
disable-model-invocation: true
---

# Scope checks to the change

Run the checks that cover what you changed, and nothing wider.

**Why:** every session shares one machine. A whole-repo typecheck in
openmarket-internal holds 5–7 GB, and the mini has 24 GB. Five sessions each
running their own full gate filled memory and swap and froze the machine. A
session that gets its gate killed relaunches it, so the load comes straight
back.

**The law.**

- **Typecheck** the narrowest project that contains your changed files, for
  example `tsc --noEmit -p packages/<pkg>`. Never the root `typecheck` script,
  `scripts/typecheck-cli.ts`, or any whole-workspace pass.
- **Test** the files you wrote or changed, plus the test files that import the
  module you changed. Pass their paths. Never the full suite, a shard runner, or
  a regression gate such as `om-chat-gate` or `test-fast`.
- **Lint** the changed files by path. **Build** only when the change is to the
  build itself.
- **Whole-repo gates run only when the operator asks for them** in the current
  conversation. A playbook, AGENTS.md, CLAUDE.md, or repo-doc step that says to
  run the gate means its scoped form. Delegates and subagents never run a
  whole-repo gate.
- **When the operator does ask,** run one gate at a time. If it is killed or
  runs out of memory, report that and stop. Do not relaunch it.

**Report the scope.** Name what you ran, for example "typechecked
packages/cli, ran 3 test files". Then name the whole-repo gate you did not run,
so the operator knows it is still owed.

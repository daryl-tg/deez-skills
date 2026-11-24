---
name: principle-test-behavior-not-implementation
description: "Apply when writing, changing, or keeping a test. Call the code the way its users do and assert the observed result against a literal value. A test that would still pass with every import returning undefined gets rewritten or deleted."
disable-model-invocation: true
---

# Test behavior, not implementation

A test calls the code the way its users do and asserts what they can observe
through its interface (return values, errors, state they can read back, effects
on outside systems) against a literal expected value. Private helpers, internal
call order, and intermediate data are implementation.

**The check.** Would the test still pass if every function it imports returned
`undefined`? If yes, it observes no behavior and cannot fail for a defect.
Rewrite the assertion or delete the test.

Judge each test against two imagined edits.

- **Break the behavior** (a wrong value, a skipped or doubled effect). If the
  test still passes, it proves nothing. The usual causes are a loose assertion,
  an expected value computed by the code under test, as in
  `expect(f(a)).toBe(f(a))`, and an assertion on data the test built itself.
- **Change the internals** and keep every observable result. If the test fails,
  it is pinned to the implementation. A constant pin such as
  `expect(LIMITS.maxTools).toBe(8)` fails on a legitimate edit and catches no
  bug.

Keep a test that catches the first edit and survives the second. Rewrite or
delete the rest. Call the subject with one concrete input and derive the
expected value from the requirement, as in
`expect(slugify("Hello, World!")).toBe("hello-world")`. For a constant, test the
mechanism that reads it. What a mocked external service receives is behavior. A
call to an internal helper is not. Pair "this never happens" with a case where
it does, so the test shows it can see the effect. Assert the error type callers
branch on, not the message.

Also keep a test that asserts a relation across tables, such as a key present in
both, and a compile-time check in a type-level test file.

**principle-failing-test-first** decides when the check gets written. This one
decides whether it is a check at all.

Naming follows the repository, never `*.spec.*`. Use `test/<name>.test.ts(x)` in
`openmarket-chat` (root `test/` for canonical UI, `apps/cloud/test/` for
host-local) and the app's jest convention in `openmarket-chat-app`.

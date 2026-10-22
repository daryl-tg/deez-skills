---
name: principle-test-behavior-not-implementation
description: "Apply when writing, changing, or keeping a test. Call the code the way its users do and assert the observed result against a literal value. A test that would still pass with every import returning undefined gets rewritten or deleted."
disable-model-invocation: true
---

# Test behavior, not implementation

A test calls the code the way its users do and asserts the result they observe
against a literal expected value. A test that asserts which calls the code made,
or restates a constant the code already contains, does neither.

**The check.** Before keeping a test, ask whether it would still pass if every
function it imports returned `undefined`. If yes, it observes no behavior and
cannot fail for a defect. Rewrite the assertion or delete the test.

**Why:** a test that cannot fail for a defect still costs CI time and review
attention. A constant pin is worse than useless, because it also fails when
someone legitimately edits the constant, so it exists only to prevent that edit.

**Two imagined edits.** Break the behavior: if the test still passes, it proves
nothing. Change the internals without changing behavior: if the test fails, it
is pinned to the implementation. Both are the same defect.

**The contract decides, not the shape of the assertion.** A no-call assertion is
valid when no-call is the promise: checking out an empty cart must not charge the
card. The same assertion is empty when the code simply never ran, so also run
the non-empty case in the same test. Self-referential expectations are always wrong:
`expect(f(a)).toBe(f(a))`, `expect(parsed.url).toBe(buildUrl(...))`. A constant
pin fails on a legitimate edit: `expect(LIMITS.maxTools).toBe(8)`.

**The fix.** Call the subject inside the test body with one concrete input and
assert the literal output or the observable effect:
`expect(slugify("Hello, World!")).toBe("hello-world")`. For a constant, test the
mechanism that reads it. For a mock, assert the payload it received or the state
after the call. Where no such assertion exists, delete the test.

**Keep** a test that asserts a relation across a table's rows, such as a key
present in two tables or a parent that exists, and a compile-time check in a
type-level test file.

Pairs with **principle-failing-test-first**, which decides *when* the check gets
written. This one decides whether what you wrote is a check at all. A test that
never failed for the right reason usually fails this rule too.

Naming follows the repository, never `*.spec.*`: `test/<name>.test.ts(x)` in
`openmarket-chat` (root `test/` for canonical UI, `apps/cloud/test/` for
host-local), the app's jest convention in
`openmarket-chat-app`.

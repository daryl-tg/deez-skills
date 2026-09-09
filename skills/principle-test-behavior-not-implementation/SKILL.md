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

**Five shapes that survive every import returning `undefined`:**

- **Weak or absent assertion.** No `expect` at all, or only `toBeDefined`,
  `toBeTruthy`, `not.toThrow`, `toBeInstanceOf`, `toBeGreaterThan(0)`.
- **Mock or absence only.** Only `toHaveBeenCalled`, `not.toHaveBeenCalled`,
  `toBeUndefined`, `toEqual([])`, `toHaveLength(0)`, `not.toBe(wrongValue)`.
- **Self-referential.** The expected value comes from the code under test:
  `expect(f(a)).toBe(f(a))`, `expect(parsed.url).toBe(buildUrl(...))`.
- **Constant pin.** The assertion restates a hand-maintained constant, config
  default, table row, or prompt string: `expect(LIMITS.maxTools).toBe(8)`.
- **Fixture asserts fixture.** The assertion reads data the test built or a
  value computed in `beforeEach`, and the subject never runs in the body.

**The fix.** Call the subject inside the test body with one concrete input and
assert the literal output or the observable effect:
`expect(slugify("Hello, World!")).toBe("hello-world")`. For an absence, assert
the presence on the other input in the same test. For a constant, test the
mechanism that reads it. For a mock, assert the payload it received or the state
after the call, not that it was called. Where no such assertion exists, delete
the test.

**Keep** a test that asserts a relation across a table's rows, such as a key
present in two tables or a parent that exists, and a compile-time check in a
type-level test file.

Pairs with **principle-failing-test-first**, which decides *when* the check gets
written. This one decides whether what you wrote is a check at all. A test that
never failed for the right reason usually fails this rule too.

Naming follows the repository, never `*.spec.*`: `test/<name>.test.ts(x)` in
`openmarket-chat` and `openmarket-chat-cloud`, the app's jest convention in
`openmarket-chat-app`.

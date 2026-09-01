# Reviewer Checklist

Use this reference when the first pass says "looks
fine" too quickly. It expands the question set and
shows the writing style the skill expects.

## 1. Behavior before style

Ask these first:

- What changed in behavior versus the old code?
- Did the scope widen by accident?
- Did defaults, retries, shutdown, commits,
  acknowledgements, or timing change?
- Did we lose logging or other observability that was
  previously useful?

If the answer is "yes," that is usually more
important than naming or formatting.

## 2. Necessity check

Challenge new surface area hard.

Ask:

- Why does this helper exist at all?
- Why is this flag or config key needed?
- Why is this log line or comment here?
- Can the logic be inlined or deleted instead?
- Is this compatibility path still used after the
  migration?

This review style prefers deletion over decorative
abstraction.

## 3. Naming check

Push on names that hide the real concept.

Bad signs:

- names that smuggle in a business story the code is
  not actually expressing
- names like `Fallback`, `Helper`, `Manager`, or
  `UntilCaughtUp` when the code does something more
  concrete
- names that only make sense if you remember the old
  implementation

Prefer names that describe the real input, output, or
side effect.

## 4. Proof standard

Do not stop at "this feels wrong" when the code can
be made to prove it.

Preferred proof order:

1. direct code-path explanation
2. concrete failure mode
3. minimal failing test when useful

If the claim is real and visible from the code, state
it directly. Do not weaken it with `possibly`.

If the claim is uncertain, move it to `Open
questions` and say exactly what would confirm it.

## 5. Typical findings this style values

High-value findings include:

- dead code left after a migration
- behavior drift from the previous implementation
- hot-path complexity that will not pass review
- closed-channel, retry, or shutdown bugs
- stale config, docs, tasks, or tests
- mixed unrelated concerns in one commit or MR
- redundant comments that explain nothing
- helper functions whose only job is to hide a simple
  operation

## 6. Output phrasing

Prefer short factual findings.

Good:

- `The new path prefetches every partition, not only
  the assigned ones.`
- `This goroutine is dead after the library swap.`
- `The closed-channel receive keeps the stage alive
  forever unless it checks ok.`
- `The name leaks an old fallback concept that the
  type does not represent anymore.`

Avoid:

- `Could this maybe be simplified?`
- `I wonder whether this might be dead code.`
- `Have you considered renaming this?`

## 7. Example prompts

These are the kinds of prompts that should trigger
this skill:

- `review current branch against origin/main, check
  for dead code or logic drift, and write REVIEW.txt`
- `would this pass review? be strict about naming and
  unnecessary helpers`
- `review this MR diff, maybe I displaced some logic
  during the migration`
- `check whether I changed shutdown behavior or left
  stale compatibility paths behind`

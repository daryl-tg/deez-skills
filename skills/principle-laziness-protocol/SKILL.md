---
name: principle-laziness-protocol
description: "Apply when refactoring, sizing a diff, or tempted to add abstractions, layers, or signal threading. Bias to deletion and the smallest change that solves the problem."
disable-model-invocation: true
---

# Laziness protocol

Writing code is cheap for you, which makes over-engineering easy. Counter it by
borrowing a human maintainer's fatigue. Most result, least code.

- **Prefer deletion.** Asked to refactor or improve, look for removals before
  additions.
- **Keep the call hierarchy flat.** If answering a question means tracing
  through more than three files or layers, flatten it. A rich interface that
  hides real work is not a deep chain.
- **Consolidate decisions.** Never make the same choice in several places. One
  source of truth, pass the result as a simple flag.
- **Minimise the diff.** The smallest change that solves the problem. Fewer
  lines beat elegant boilerplate.
- **Question the threading.** If a task asks you to pass a new signal through
  types, schemas, and pipelines, stop and look for a more direct path.
- **Sweat the small leaks.** Tiny pass-throughs, representation leaks, and
  duplicated choices compound into permanent coordination costs.

**The test:** if a human developer would find this exhausting to maintain, it is
a bad solution. Be lazy. Stay simple.

Sequencing partner of **principle-subtract-before-you-add**.

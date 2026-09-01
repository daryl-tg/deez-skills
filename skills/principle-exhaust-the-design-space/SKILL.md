---
name: principle-exhaust-the-design-space
description: "Apply to a novel interaction or architectural decision with no precedent in the codebase. Build two or three competing sketches and compare before committing."
disable-model-invocation: true
---

# Exhaust the design space

When a decision has no established precedent, explore several concrete
alternatives before implementing. Building the wrong thing costs more than
exploring three options.

**The rule.** When the right answer is not obvious, produce two or three
competing sketches and compare them side by side. Only then commit. **A second
flavour of the first shape does not count** — the candidates must be
structurally distinct.

**When it applies:**

- A novel interaction with no prior art in the codebase.
- An architectural choice with several viable approaches.
- A product decision where the answer depends on feel rather than logic.

**When it does not:**

- Mechanical implementation where the pattern is established.
- A bug fix or refactor with a clear target state.
- A change where constraints dictate a single viable approach.

Running this over a settled design is over-engineering, per
**principle-laziness-protocol**. The **design** skill is where this happens in
practice, and **herdr-codex-orchestration** in arena mode is how candidates get
produced in parallel.

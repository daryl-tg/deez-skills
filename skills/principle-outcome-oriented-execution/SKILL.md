---
name: principle-outcome-oriented-execution
description: "Apply during planned rewrites and migrations with explicit phase boundaries. Converge on the target architecture rather than preserving throwaway compatibility states."
disable-model-invocation: true
---

# Outcome-oriented execution

Optimise for the intended, verifiable end state rather than for smooth
intermediate states.

**Why:** keeping every intermediate step fully stable creates temporary
compatibility code that becomes long-lived debt. Converge on the target
architecture and prove correctness at explicit verification boundaries.

- Prioritise end-state integrity over transitional stability.
- Intermediate breakage is acceptable when it is **planned, scoped, and
  reversible**. Unplanned breakage is not this principle.
- Always run full verification before declaring done.

**Guardrails.** Use this for planned rewrites and migrations with explicit phase
boundaries, not as licence to leave things broken. Declare up front where
temporary breakage is acceptable. Keep high-signal checks running for the areas
you are actively touching.

Tension worth naming: this trades against
**principle-sequence-verifiable-units**, which wants every unit green. The
resolution is scope — units stay green, phases may transit through a declared
broken state, and the phase boundary is where full verification runs.

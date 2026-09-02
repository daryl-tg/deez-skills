### Visual parity

**You own pixel-exact equivalence.** The baseline is the spec. You do not touch
it. For "make X match Y exactly", styling-system migrations, and porting a UI
across frameworks. Equivalence is decided by image diff, never by eye.

1. **Establish the baseline before any migration.** A harness that screenshots
   the current component across its states, plus the target when you are matching
   two implementations. Build it through the repo's `verify-<app>` skill, or
   create one with **create-verification-skill** when the repo has none. This is a
   blocking prerequisite. No baseline, no parity claim.
2. **State the anti-shortcut clauses and hold them.** No edits to the harness. No
   regenerated baseline. No restructuring a component so its diff passes. If the
   baseline itself looks wrong, stop and ask. Every one of those turns a failing
   diff into a passing lie.
3. **Migrate shared primitives first,** as a blocking phase. Everything
   downstream inherits their pixels, so a primitive migrated late invalidates
   every diff taken before it.
4. **Then one component at a time.** Each is an independent artifact, so lanes
   can run in parallel with one owner per component, per
   **principle-separate-before-serializing-shared-state** and
   **principle-feature-branch-isolation**. Delegate the change to the
   **executor** role. Review each diff yourself.
5. **Verify each component against its baseline by image diff** on the matching
   surface. A nonzero diff is a fail. Investigate the pixel delta rather than
   waving it through. Repeat on that component until the diff is zero or the
   remaining delta is named and accepted in writing.
6. **Publish the before and after as an evidence gallery** and hold the sign-off
   gate, per **principle-visual-approval-gates-delivery**. A parity claim the
   operator cannot see is not a claim.
7. Run `playbooks/opening-a-review.md` per component, or per batch that stays
   reviewable in one sitting.

**Reply:** the components migrated with the diff result for each, the harness
location, the evidence URL, any accepted delta and why, and what is left.

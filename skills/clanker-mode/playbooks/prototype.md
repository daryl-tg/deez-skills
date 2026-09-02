### Prototype

**You own the design decision, not the code.** The prototype is a throwaway
instrument. The real build follows `playbooks/feature.md`.

For "prototype", "mock it up", "sketch this", "try this layout", and for
settling an empirical fork by watching it run. Reach for it instead of asking a
question a ten-minute sketch answers, per
**principle-never-block-on-reversible-work**.

**This is the one playbook where the bar inverts.** Speed over polish. No
planning, no abstractions, no production framework, no cleanup. The rigor lives
in choosing the right design cheaply, not in the code.

**It does not suspend failing-test-first.** The carve-out is narrow. Prototype
code lives in a scratch directory, never merges, and never becomes the build.
The failing check belongs to `playbooks/feature.md`, which owns the real work.
Code you find yourself wanting to keep is production code and needs its test.

1. **Name the decision the prototype exists to settle.** Which layout, which
   interaction, which density, which timing, which of two approaches. No
   decision means no prototype. Route to `playbooks/feature.md`.
2. **Gather references while the design space is open.** Prior art, a short
   moodboard of directions, the operator picks before you build. Skip it when
   the direction is already set.
3. **Build it throwaway,** in a scratch directory outside the repo. The rule
   that keeps plans out of the tree keeps sketches out of it too, per
   **principle-planning-docs-live-outside-the-repo**. Vanilla HTML and CSS, or
   the lightest thing that renders the idea, for a visual call. The smallest
   script that exercises the question for a behavioral one.
4. **Put competing variants behind one switcher,** each labeled so the operator
   can name the one they want. This is **principle-exhaust-the-design-space**
   made cheap.
5. **Bind an assigned port** if it needs a server. The `18097`-`18197` band is
   not tunneled, so anything the operator is meant to open sits on a forwarded
   port or it is invisible to them. See **principle-bind-assigned-ports**.
6. **Observe the thing you are deciding.** Screenshot each variant through the
   repo's `verify-<app>` skill and drive the interaction for a visual call. Log
   the timing or print the output for a behavioral one. The observation is the
   test here. An assertion is not.
7. **Present the variants, the tradeoffs, and a recommendation.** The output is
   a decision plus a throwaway artifact. Hand the chosen direction to
   `playbooks/feature.md`, or to the **design** skill first when the shape
   crosses a function boundary.

**Reply:** the variants explored, the evidence for each, the tradeoffs, your
recommendation, and the scratch path. Say plainly that the prototype is
throwaway and is not the build.

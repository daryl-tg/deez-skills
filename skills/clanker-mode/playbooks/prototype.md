### Prototype

**You own the design decision, not the code.** The prototype is a throwaway
instrument. Speed over polish. No plan, no tests, no abstractions, no cleanup.

For "prototype", "mock it up", "sketch this", "try this layout", and for
settling an empirical fork by watching it run rather than asking a question a
ten-minute sketch answers, per **principle-never-block-on-reversible-work**.

1. **Name the decision it exists to settle.** Which layout, which interaction,
   which timing, which of two approaches. No decision means no prototype. Route
   to `playbooks/feature.md`.
2. **Build it throwaway,** in a scratch directory outside the repo. The lightest
   thing that renders the idea. Competing variants go behind one switcher, each
   labeled so the operator can name the one they want, per
   **principle-exhaust-the-design-space**. Anything they are meant to open sits
   on a forwarded port, per **principle-bind-assigned-ports**.
3. **Look at it.** Screenshot each variant, or log the timing, or print the
   output. The observation is the test here. An assertion is not.
4. **Recommend one, then throw the code away.** The output is a decision. The
   build starts fresh under `playbooks/feature.md`, which owns the failing test.
   Code you want to keep is production code and goes back through that door.

**Reply:** the variants, what you observed, your recommendation, and the scratch
path. Say plainly that the prototype is throwaway.

### Feature plan

**You own the plan and the pass that builds it.** The plan is a checklist the
build runs box by box and the operator audits from the evidence. Use it for a
feature too large to build without a written plan. One plan covers the whole
feature, and the same run builds all of it through subagents. It never
splits into phases, per **principle-sequence-verifiable-units**.

1. **Skip the plan when the change is one or two files with an obvious
   approach.** Say so and stop. A plan for a one-file change is ceremony that
   buys nothing.
2. **Settle the open questions before writing.** A question about layout,
   timing, behavior, or whether an API works goes to `playbooks/prototype.md`.
   Keep the scratch path and the screenshots for Appendix A. Ask the operator
   only about a product or preference call no run can settle, and give options
   when you do, per **principle-never-block-on-reversible-work**. Several open
   calls go in rounds, per `playbooks/grill-me.md`.
3. **Explore in delegates.** The **explore** role over each affected subsystem
   returns file pointers, conventions, test commands, and entry points. No
   inlined dumps, per **principle-guard-the-context-window**.
4. **Write the plan into the task's dev-notes folder** by absolute path, as
   `YYYY-MM-DD-<topic>-plan.md`, per
   **principle-planning-docs-live-outside-the-repo**. Never into the repo. Copy
   the skeleton below and fill every placeholder. One section per unit. Every
   unit is built in the same run and ships in one review, per
   **principle-sequence-verifiable-units**. Never write a phase 2 or a deferred
   follow-up. Scope that is in the feature is in the plan.
5. **Write it to the docs standard.** Draft under **writing-docs**, then
   run **unslop** over it. The body is a how-to.
   Explanation and reference live in the appendices. Every heading states the
   task or the finding. No long dashes. No mid-sentence colons.
6. **Run the shape check** and fix every line it prints.
   `~/github/deez-skills/bin/check-plan <plan path>` holds the skeleton, the
   verification rule in every verify block, and the punctuation. It is the
   lesson in structure rather than in prose, per
   **principle-encode-lessons-in-structure**. What it cannot check is whether a
   box is checkable by evidence rather than by opinion. Read for that yourself.
7. **Post the plan path and keep going.** Do not ask which execution path.
   Build every unit in one pass through `playbooks/agentic-loop.md`, with Claude
   subagents as the executors. Do not stop between units, and do not hand back
   a partial build.

**Verification.** Tests alone are not sufficient. A unit is verified when its
unit box and its real-surface box are both checked, per
**principle-prove-on-the-real-surface**. The real-surface box names the scenario,
how it is driven through the repo's `verify-<app>` skill, the screenshot it
saves, and the predicate that passes. A unit that changes an interaction is
review-gated on the operator seeing it in the one evidence revision published
for the whole candidate, per **principle-visual-approval-gates-delivery**. The
gate is not a stop between units. A unit that changes no interaction
writes `Review gate. None.` and no boxes under it.

````markdown
# <Program> plan

<Under ten lines. What changes, for whom, and the units in order.>

## How to read this

One box is one unit of work. Every box names the evidence that checks it. Check a
box only when that evidence exists as a file, a log line, a screenshot, a test
run, or a SHA.

Tests alone are not sufficient. A unit is verified when its unit box and its
real-surface box are both checked.

<Which repository, which branch, and where the work lands.>

## <Task as a verb phrase> (unit <n>)

**Depends on.** <Unit n, or nothing.>

**Files.**

- [ ] Edit `<path>`.
- [ ] Create `<path>`.

**Build.**

- [ ] <One change. Name the symbol and the file.>

**You see.**

- [ ] <One observable result, with the exact log line or screen state.>

**Verify, unit.** Tests alone are not sufficient. A unit is verified when its
unit box and its real-surface box are both checked.

- [ ] `<test file>` gains <the case>. It fails before the change. Run `<command>`.

**Verify, real surface.** Tests alone are not sufficient. A unit is verified when
its unit box and its real-surface box are both checked.

- [ ] <Scenario.> Driven through `verify-<app>`. Saves `<slug>.png`. Passes when
      <predicate>.

**Review gate.** <The interaction the operator reviews in the candidate's one
evidence revision. Write "None." with no boxes when the unit changes no
interaction.>

- [ ] Add this unit's evidence to the candidate's revision.

## Close

- [ ] Every box above is checked with its evidence, in one run.
- [ ] One evidence revision is published and the operator signed it off.
- [ ] The terminal gate and the family completion playbook ran once, for the
      whole candidate.

## Appendix A. What the prototypes proved

<Each question a prototype answered, with the scratch path and the artifacts.
Each question that stays unproven.>

## Appendix B. Alternatives rejected

<Each approach weighed and why it lost.>

## Appendix C. Risks

<Each risk, the unit it lands in, and what the executor watches.>
````

**Reply:** the plan path, the check script's output, the units with their
dependencies, which units are review-gated, what the prototypes proved and what
stays unproven, and the build's result.

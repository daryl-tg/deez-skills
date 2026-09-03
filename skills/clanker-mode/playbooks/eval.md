### Eval

**You own the experiment design.** Frame, blind, run, synthesize. For testing
whether a change to how an agent works actually helps before promoting it. A
skill variant, a rewritten playbook, a prompt change.

**The failure mode is the observer effect.** A candidate that knows it is being
measured behaves differently, so candidates run blind.

**Blinding is non-negotiable.**

- No `eval`, `test`, `judge`, `rubric`, `score`, `compare`, `benchmark`,
  `candidate`, or `arena` in any path, file, or prompt the candidate sees.
- The prompt reads like an organic request. State the goal, never the meta.
  "Add a pinned-message row to the transcript header", not "show me how well you
  follow the principles".
- No chain-eliciting cues. Never ask a candidate which skills or principles it
  applied. That question alone inflates citation. Grade from the artifact.
- Sanitised directory names a person might pick. Never `candidate-1`.
- No candidate learns another exists.
- The judge may know it is judging, sees outputs by sanitised label only, and
  never sees which variant produced which.

1. **Frame it.** Name the variant under test and what success looks like. Write
   the rubric, three to six concrete criteria, for the judge only.
2. **Set up one working directory per candidate**, each a worktree with the
   variant in place, per **principle-separate-before-serializing-shared-state**.
   Plant the context an organic task would have.
3. **Author one organic prompt** and give the same one to every candidate.
4. **Run the candidates in parallel** through the **executor** role, one per
   directory. Vary the model across candidates when the variant is meant to hold
   across models.
5. **Run one judge** against the rubric, separate from every candidate, through
   the **code-reviewer** role. One judge scores every output in a single pass on
   one scale. Two judge runs with different prompts do not compare, because the
   calibration drifts. Where one judge is not enough, **llm-council** is the
   panel version, and its verdict still lands on your desk, not in the record.
6. **Grade the chain from the artifact, not the self-report.** What the code
   looks like, which files the run actually opened where the runtime records it.
   Citing a principle is not reading it, and reading it is not applying it.
7. **Read every candidate output yourself,** end to end, then compare with the
   judge. Disagreement means the rubric is ambiguous or the judge is biased. Say
   which, and fix the rubric before believing the result.
8. **Promote or discard on the evidence.** A promoted variant lands through
   `playbooks/authoring-a-skill.md` so the hub's gates apply.

**Reply:** the variant, the rubric, per-candidate notes, the judge's verdict,
your synthesis, and a promote or discard recommendation with the reason.

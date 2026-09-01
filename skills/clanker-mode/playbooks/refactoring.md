### Refactoring

**Behavior-preserving by definition.** If behavior changes, this is a Feature.

1. **Characterize first.** Before touching structure, capture the current
   behavior in a check that passes now. Without it there is no way to tell
   preservation from breakage.
2. **Subtract before adding.** Remove dead paths, one-caller wrappers, and
   duplicated decisions first, then reshape the simpler base.
3. Work in units that each end green, per **principle-todo-discipline**. Never
   batch the edits and verify once at the end.
4. When a lever can do the edits, build it rather than hand-applying, per
   **principle-build-the-lever**. The lever is what a reviewer reruns.
5. **Verify behavior is unchanged** on the real surface, not just that it
   compiles.
6. Run `playbooks/opening-a-review.md`.

If implementation keeps producing the same shape of friction, the target
structure is wrong. Stop and redesign rather than bolting fixes onto it.

**Reply:** what moved, what was deleted, the characterization evidence, and
proof behavior is unchanged.

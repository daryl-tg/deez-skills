import unittest
from pathlib import Path

from deezlib import plancheck

REPO_ROOT = Path(__file__).resolve().parents[1]
PLAYBOOK = REPO_ROOT / "skills/clanker-mode/playbooks/multi-phase-plan.md"

GOOD = """# Pinned messages plan

Pins a message to the transcript header so a room keeps its own notice board.
Two units, in order.

## How to read this

One box is one unit of work. Every box names the evidence that checks it. Check a
box only when that evidence exists as a file, a log line, a screenshot, a test
run, or a SHA.

Tests alone are not sufficient. A unit is verified when its unit box and its
real-surface box are both checked.

Lands in `openmarket-chat` on `daryl/pinned-messages`.

## Store the pinned id (unit 1)

**Depends on.** Nothing.

**Files.**

- [ ] Edit `src/rooms/store.ts`.

**Build.**

- [ ] Add `pinnedMessageId` to `RoomState` in `src/rooms/store.ts`.

**You see.**

- [ ] The room state logs `pinned=abc123` after a pin.

**Verify, unit.** Tests alone are not sufficient. A unit is verified when its unit box and its real-surface box are both checked.

- [ ] `test/rooms/store.test.ts` gains the pin case. It fails before the change. Run `pnpm test store`.

**Verify, real surface.** Tests alone are not sufficient. A unit is verified when its unit box and its real-surface box are both checked.

- [ ] Pin a message from the transcript. Driven through `verify-om-chat`. Saves
      `pinned-header.png`. Passes when the header shows the pinned text.

**Review gate.** The operator reviews the published evidence before delivery.

- [ ] Publish the gallery and wait for the operator to sign off.

## Close

- [ ] Every box above is checked with its evidence.

## Appendix A. What the prototypes proved

The header layout came from a sketch. Nothing stays unproven.
"""


def without(text, block):
    return text.replace(block, "")


class PlanCheckTest(unittest.TestCase):
    def problems(self, text):
        return [p.message for p in plancheck.problems(text)]

    def test_a_filled_plan_passes(self):
        self.assertEqual(self.problems(GOOD), [])

    def test_the_playbook_skeleton_passes_its_own_checker(self):
        skeleton = plancheck.skeleton(PLAYBOOK.read_text(encoding="utf-8"))
        self.assertIsNotNone(skeleton, "multi-phase-plan.md carries no fenced skeleton")
        self.assertEqual(self.problems(skeleton), [])

    def test_missing_how_to_read_fails(self):
        text = GOOD.replace("## How to read this", "## Preface")
        self.assertTrue(any("How to read this" in m for m in self.problems(text)))

    def test_a_unit_missing_the_real_surface_block_fails(self):
        text = GOOD.replace("**Verify, real surface.**", "**Verify, live.**")
        self.assertTrue(any("sub-blocks" in m for m in self.problems(text)))

    def test_a_verify_block_that_drops_the_rule_fails(self):
        text = GOOD.replace(
            "**Verify, unit.** Tests alone are not sufficient. A unit is verified when its unit box and its real-surface box are both checked.",
            "**Verify, unit.** Run the tests.",
        )
        self.assertTrue(any("does not open with the rule" in m for m in self.problems(text)))

    def test_a_real_surface_box_without_a_predicate_fails(self):
        text = GOOD.replace("Passes when the header shows the pinned text.", "It works.")
        self.assertTrue(any("pass predicate" in m for m in self.problems(text)))

    def test_a_real_surface_box_without_a_screenshot_fails(self):
        text = GOOD.replace("Saves\n      `pinned-header.png`. ", "")
        self.assertTrue(any("screenshot" in m for m in self.problems(text)))

    def test_a_none_review_gate_with_boxes_fails(self):
        text = GOOD.replace(
            "**Review gate.** The operator reviews the published evidence before delivery.",
            "**Review gate.** None.",
        )
        self.assertTrue(any("None" in m for m in self.problems(text)))

    def test_a_none_review_gate_without_boxes_passes(self):
        text = GOOD.replace(
            "**Review gate.** The operator reviews the published evidence before delivery.\n\n"
            "- [ ] Publish the gallery and wait for the operator to sign off.\n",
            "**Review gate.** None.\n",
        )
        self.assertEqual(self.problems(text), [])

    def test_a_block_with_no_box_fails(self):
        text = GOOD.replace("- [ ] Add `pinnedMessageId` to `RoomState` in `src/rooms/store.ts`.\n", "")
        self.assertTrue(any("has no box" in m for m in self.problems(text)))

    def test_a_missing_prototype_appendix_fails(self):
        text = GOOD.replace("## Appendix A. What the prototypes proved", "## Appendix A. Notes")
        self.assertTrue(any("prototypes proved" in m for m in self.problems(text)))

    def test_a_section_after_close_that_is_not_an_appendix_fails(self):
        text = GOOD + "\n## Extra thoughts\n\nMore words.\n"
        self.assertTrue(any("not an appendix" in m for m in self.problems(text)))

    def test_a_long_dash_fails(self):
        text = GOOD.replace("Two units, in order.", "Two units — in order.")
        self.assertTrue(any("long dash" in m for m in self.problems(text)))

    def test_a_mid_sentence_colon_fails(self):
        text = GOOD.replace("Two units, in order.", "Two units: in order.")
        self.assertTrue(any("mid-sentence colon" in m for m in self.problems(text)))

    def test_a_colon_before_a_list_passes(self):
        text = GOOD.replace("Two units, in order.", "Two units, in this order:")
        self.assertEqual(self.problems(text), [])

    def test_an_intro_over_ten_lines_fails(self):
        filler = "\n".join(f"Line {n} of the intro." for n in range(12))
        text = GOOD.replace("Two units, in order.", filler)
        self.assertTrue(any("intro" in m for m in self.problems(text)))

    def test_a_plan_with_no_units_fails(self):
        text = GOOD.split("## Store the pinned id (unit 1)")[0] + "## Close\n\n- [ ] Nothing.\n\n## Appendix A. What the prototypes proved\n\nNone.\n"
        self.assertTrue(any("no unit sections" in m for m in self.problems(text)))

    def test_the_summary_counts_boxes_per_unit(self):
        summary = plancheck.summary(GOOD)
        self.assertEqual(len(summary), 1)
        self.assertIn("Store the pinned id (unit 1)", summary[0])
        self.assertIn("boxes=6", summary[0])

    def test_problems_carry_line_numbers(self):
        text = GOOD.replace("Two units, in order.", "Two units — in order.")
        found = [p for p in plancheck.problems(text) if p.message == "long dash"]
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].line, 4)


if __name__ == "__main__":
    unittest.main()

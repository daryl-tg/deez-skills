import unittest

from deezlib.superclanker.config import SourcePolicy
from deezlib.superclanker.domain import Trigger, trigger_id
from deezlib.superclanker.gate import admit

GITHUB = SourcePolicy(
    name="github", enabled=True, mode="explicit-only", senders=("daryl-tg",),
    bots=("dependabot[bot]",), scopes=("daryl-tg/deez-skills",),
)
CANDIDATES = SourcePolicy(
    name="github", enabled=True, mode="candidates", senders=("daryl-tg",),
    bots=("dependabot[bot]",), scopes=(),
)


def comment(actor, addressed):
    return Trigger(
        id=trigger_id("github", f"{actor}-{addressed}"),
        source="github",
        source_event_id=f"{actor}-{addressed}",
        thread_id="github:daryl-tg/deez-skills#7",
        actor=actor,
        addressed=addressed,
        text="looks good",
        parent_id=None,
        received_at="2026-11-02T10:00:00+00:00",
        meta={},
    )


def outcome(trigger, policy=GITHUB, accept_mode="observe", thread_has_tickets=False):
    admission = admit(trigger, policy, accept_mode, thread_has_tickets)
    return admission.strength, admission.basis


class GateTest(unittest.TestCase):
    def test_listed_sender_addressing_agent_is_explicit(self):
        admission = admit(comment("daryl-tg", True), GITHUB, "observe", False)

        self.assertEqual((admission.strength, admission.basis), ("explicit", "addressed"))
        self.assertIn("daryl-tg", admission.reason)

    def test_unlisted_followup_on_ticketed_thread_is_inferred(self):
        stranger = comment("stranger", False)

        self.assertEqual(outcome(stranger, thread_has_tickets=True), ("inferred", "followup"))
        self.assertEqual(outcome(stranger), ("not_admitted", "source"))

    def test_listed_sender_followup_is_explicit_and_unaddressed_otherwise_dropped(self):
        listed = comment("daryl-tg", False)

        self.assertEqual(outcome(listed, thread_has_tickets=True), ("explicit", "followup"))
        self.assertEqual(outcome(listed), ("not_admitted", "source"))

    def test_candidates_source_admits_unaddressed_events_as_inferred(self):
        self.assertEqual(
            outcome(comment("daryl-tg", False), CANDIDATES), ("inferred", "admission")
        )
        self.assertEqual(
            outcome(comment("stranger", False), CANDIDATES), ("inferred", "admission")
        )

    def test_bot_never_explicit(self):
        bot = "dependabot[bot]"
        listed_bot = SourcePolicy(
            name="github", enabled=True, mode="explicit-only", senders=(bot,), bots=(bot,),
            scopes=(),
        )

        self.assertEqual(
            outcome(comment(bot, True), listed_bot, thread_has_tickets=True), ("inferred", "bot")
        )
        self.assertEqual(
            outcome(comment(bot, False), listed_bot, thread_has_tickets=True),
            ("not_admitted", "bot"),
        )
        self.assertEqual(outcome(comment(bot, False), CANDIDATES), ("inferred", "bot"))

    def test_off_mode_drops_inferred(self):
        self.assertEqual(
            outcome(comment("stranger", False), accept_mode="off", thread_has_tickets=True),
            ("not_admitted", "off"),
        )
        self.assertEqual(
            outcome(comment("dependabot[bot]", True), accept_mode="off"), ("not_admitted", "off")
        )
        self.assertEqual(
            outcome(comment("daryl-tg", True), accept_mode="off"), ("explicit", "addressed")
        )

    def test_disabled_source_not_admitted(self):
        disabled = SourcePolicy(
            name="github", enabled=False, mode="explicit-only", senders=("daryl-tg",), bots=(),
            scopes=(),
        )
        ignored = SourcePolicy(
            name="github", enabled=True, mode="ignore", senders=("daryl-tg",), bots=(), scopes=(),
        )

        for policy in (disabled, ignored):
            with self.subTest(policy=policy):
                self.assertEqual(
                    outcome(comment("daryl-tg", True), policy, thread_has_tickets=True),
                    ("not_admitted", "source"),
                )


if __name__ == "__main__":
    unittest.main()

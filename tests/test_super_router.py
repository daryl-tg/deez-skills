import json
import os
import re
import shutil
import stat
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path
from unittest import mock

from deezlib import cli
from deezlib.superclanker import config, router
from deezlib.superclanker.domain import Strength, Trigger, trigger_id
from deezlib.superclanker.sources import terminal
from deezlib.superclanker.store import Store, SuperError

HUB = cli.REPO_ROOT
FAKE = Path(__file__).with_name("fake_claude.py")
UUID = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$")
SOURCES = """
[router]
model = "haiku"

[sources.github]
enabled = true
mode = "candidates"
senders = ["daryl-tg"]

[sources.om]
enabled = true
senders = ["daryl"]
"""


def summaries(shown):
    return [summary for _neighbour, summary in shown["related"]]


class RouterTest(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name) / "state"
        bin_dir = Path(tmp.name) / "bin"
        bin_dir.mkdir()
        shutil.copy(FAKE, bin_dir / "claude")
        (bin_dir / "claude").chmod(0o755)
        self.claude = bin_dir / "claude"
        self.log = Path(tmp.name) / "argv.jsonl"
        self.out = Path(tmp.name) / "router-out.txt"
        environ = {
            key: value for key, value in os.environ.items()
            if not key.startswith("FAKE_CLAUDE_")
        }
        environ.update({
            "PATH": f"{bin_dir}{os.pathsep}{os.environ['PATH']}",
            "FAKE_CLAUDE_LOG": str(self.log),
            "DEEZ_SUPER_STATE": str(self.root),
            "USER": "daryl",
        })
        patcher = mock.patch.dict(os.environ, environ, clear=True)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.store = Store.open(self.root)
        self.addCleanup(self.store.close)
        (self.root / "sources.toml").write_text(SOURCES, encoding="utf-8")
        self.events = 0

    def config(self):
        return config.load(self.root)

    def wake(self):
        return router.wake(self.store, self.config(), self.root, HUB)

    def ask(self, text, thread="default"):
        trigger, _receipt = terminal.ask(self.store, text, thread_name=thread)
        return trigger

    def received(self, source, thread, actor, text, addressed=True):
        self.events += 1
        event_id = f"evt-{self.events}"
        trigger = Trigger(
            trigger_id(source, event_id), source, event_id, thread, actor, addressed, text,
            None, f"2026-11-02T10:{self.events:02d}:00+00:00", {},
        )
        self.store.receive(trigger)
        return trigger

    def argvs(self):
        if not self.log.exists():
            return []
        return [json.loads(line) for line in self.log.read_text(encoding="utf-8").splitlines()]

    def router_runs(self, script):
        os.environ["FAKE_CLAUDE_SCRIPT"] = script

    def deez(self, *argv):
        out, err = StringIO(), StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = cli.main(["super-clanker", *argv])
        return code, out.getvalue(), err.getvalue()

    def queued_ids(self):
        return [trigger.id for trigger in self.store.queued()]

    def route(self, script):
        with mock.patch("sys.stdin", StringIO(script)):
            return self.deez("route")

    def decisions(self, trigger_id_):
        return [s for s in summaries(self.store.show(trigger_id_)) if s.startswith("decision")]

    def test_empty_batch_skips_model(self):
        self.assertIsNone(self.wake())
        self.assertEqual(self.argvs(), [])

        self.ask("fix the typo")

        self.assertIsNotNone(self.wake())
        self.assertEqual(len(self.argvs()), 1)

    def test_not_admitted_triggers_are_ignored_without_model_call(self):
        stranger = self.received("om", "om:chat:general", "mallory", "do my homework")
        unconfigured = self.received("gitlab", "gitlab:group/repo!3", "daryl", "please merge")

        self.assertIsNone(self.wake())

        self.assertEqual(self.argvs(), [])
        self.assertEqual(self.queued_ids(), [])
        self.assertIn("decision ignore: not admitted: source", summaries(self.store.show(stranger.id)))
        self.assertIn(
            "decision ignore: not admitted: source", summaries(self.store.show(unconfigured.id))
        )

    def test_every_wake_is_a_fresh_session(self):
        self.ask("first request")
        self.wake()
        self.ask("second request")
        self.wake()

        first, second = self.argvs()
        sids = [argv[argv.index("--session-id") + 1] for argv in (first, second)]
        for sid in sids:
            self.assertRegex(sid, UUID)
        self.assertNotEqual(sids[0], sids[1])
        self.assertNotIn("--resume", first + second)
        self.assertFalse((self.root / "router.session").exists())

    def test_wake_prompt_carries_open_tickets_and_the_recent_conversation(self):
        earlier = self.ask("fix the tape scroll")
        ticket = self.store.accept(
            earlier.id, "tape-scroll", Strength.explicit, "local", [], "p1", "asked"
        )
        assignment = self.store.assignment_for(ticket.id)
        self.store.start_assignment(assignment.id, "sid", 1, self.root)
        self.store.report(assignment.id, "waiting", "two fixes fit", question="Clamp or debounce?")
        self.store.reply("terminal:default", "Started tape-scroll.")
        ended = self.ask("old work")
        gone = self.store.accept(ended.id, "old-work", Strength.explicit, "local", [], "p1", "asked")
        self.store.stop(gone.id, "daryl", "done")
        request = self.ask("debounce it")

        prompt = self.deez("wake", "--dry-run")[1]

        tickets = prompt.split("## open tickets", 1)[1].split("##", 1)[0]
        self.assertIn(f"{ticket.id} tape-scroll", tickets)
        self.assertIn('waiting "two fixes fit"', tickets)
        self.assertIn("asks: Clamp or debounce?", tickets)
        self.assertNotIn(gone.id, tickets)
        conversation = prompt.split("## recent conversation on terminal:default", 1)[1].split("##", 1)[0]
        self.assertIn("you: fix the tape scroll", conversation)
        self.assertIn("router: Started tape-scroll.", conversation)
        self.assertNotIn("debounce it", conversation)
        self.assertIn(f"## {request.id}  terminal", prompt)

    def test_wake_records_the_tokens_it_used(self):
        self.ask("fix the typo")

        result = self.wake()

        self.assertEqual(self.store.show(result.wake_id)["tokens"], 135)

    def test_wake_passes_agent_prompt_and_allowlist(self):
        request = self.ask("fix the typo in README")

        self.wake()

        (argv,) = self.argvs()
        body = (HUB / "agents" / "super-router.md").read_text(encoding="utf-8").split("---\n", 2)[2]
        self.assertEqual(argv[:2], ["-p", "--model"])
        self.assertEqual(argv[argv.index("--model") + 1], "haiku")
        self.assertEqual(argv[argv.index("--tools") + 1], "Bash")
        self.assertEqual(argv[argv.index("--allowedTools") + 1], "Bash(deez super-clanker *)")
        self.assertEqual(argv[argv.index("--permission-mode") + 1], "dontAsk")
        self.assertEqual(argv[argv.index("--output-format") + 1], "json")
        self.assertIn("--strict-mcp-config", argv)
        self.assertEqual(argv[argv.index("--setting-sources") + 1], "project,local")
        system_prompt = argv[argv.index("--append-system-prompt") + 1]
        self.assertEqual(system_prompt, body.strip())
        self.assertIn("You are the Router of super-clanker", system_prompt)
        self.assertNotIn("name: super-router", system_prompt)
        self.assertIn(f"## {request.id}  terminal  terminal:default  daryl", argv[-1])
        self.assertIn("text: fix the typo in README", argv[-1])

    def test_dispatch_from_router_creates_ticket(self):
        request = self.ask("fix the typo in README line 1")
        self.router_runs(
            f"deez super-clanker dispatch {request.id} --slug fix-readme-typo --playbook bug-fix "
            f">> {self.out}"
        )

        result = self.wake()

        self.assertEqual((result.batch, result.decided, result.cost_usd), (1, 1, 0.001))
        printed = self.out.read_text(encoding="utf-8")
        ticket_id = re.search(r"ticket (k_[0-9a-f]{10})", printed).group(1)
        playbook = HUB / "skills" / "clanker-mode" / "playbooks" / "bug-fix.md"
        self.assertEqual(
            printed,
            f"accept {request.id} → ticket {ticket_id} mandate explicit addressed playbook "
            f"{playbook}\n",
        )
        ticket = self.store.show(ticket_id)
        self.assertEqual((ticket["slug"], ticket["state"]), ("fix-readme-typo", "open"))
        self.assertIn("mandate explicit terminal:default", summaries(ticket))
        self.assertEqual(
            [(i.kind, i.text) for i in self.store.undelivered_inputs(ticket_id)],
            [("note", f"playbook: {playbook}")],
        )
        wake = self.store.show(result.wake_id)
        self.assertEqual((wake["exit_code"], wake["cost_usd"]), (0, 0.001))
        self.assertRegex(wake["session_id"], UUID)
        self.assertEqual(wake["trigger_ids"], (request.id,))
        self.assertEqual(self.queued_ids(), [])

    def test_dispatch_twice_same_trigger_one_ticket(self):
        request = self.ask("fix the typo")

        first = self.deez("dispatch", request.id, "--slug", "fix-typo", "--playbook", "bug-fix")
        second = self.deez("dispatch", request.id, "--slug", "fix-typo", "--playbook", "bug-fix")

        self.assertEqual((first[0], second[0]), (0, 0))
        self.assertEqual(first[1], second[1])
        self.assertEqual([row["slug"] for row in self.store.status()], ["fix-typo"])
        ticket_id = self.store.status()[0]["ticket"]
        notes = [s for s in summaries(self.store.show(ticket_id)) if s.startswith("input note")]
        self.assertEqual(len(notes), 1)

    def test_observe_mode_records_would_accept(self):
        (self.root / "policy" / "rules").mkdir(parents=True)
        (self.root / "policy" / "rules" / "red-builds.md").write_text("# Red builds\n", encoding="utf-8")
        overheard = self.received(
            "github", "github:daryl-tg/deez-skills#9", "someone", "the build is red", addressed=False
        )

        code, out, _err = self.deez(
            "dispatch", overheard.id, "--slug", "fix-red-build", "--playbook", "bug-fix",
            "--rule", "red-builds",
        )

        self.assertEqual(code, 0)
        self.assertEqual(
            out, f"would accept {overheard.id} as fix-red-build (observe mode, nothing started)\n"
        )
        self.assertIn(
            "decision ignore: would accept: fix-red-build via red-builds",
            summaries(self.store.show(overheard.id)),
        )
        self.assertEqual(self.store.status(), [])
        self.assertEqual(self.queued_ids(), [])

    def test_undecided_batch_trigger_becomes_unavailable(self):
        handled = self.ask("fix the typo")
        forgotten = self.ask("and the other typo", thread="other")
        self.router_runs(f"deez super-clanker ignore {handled.id} --reason 'chatter' >> {self.out}")

        result = self.wake()

        self.assertEqual((result.batch, result.decided), (2, 1))
        self.assertEqual(self.out.read_text(encoding="utf-8"), f"ignored {handled.id}\n")
        self.assertIn("decision ignore: chatter", summaries(self.store.show(handled.id)))
        self.assertIn(
            f"decision unavailable: router made no decision in {result.wake_id}",
            summaries(self.store.show(forgotten.id)),
        )
        self.assertEqual(self.queued_ids(), [])

    def test_attached_trigger_counts_as_decided(self):
        first = self.ask("fix the typo")
        ticket = self.store.accept(
            first.id, "fix-typo", "explicit", "terminal:default", [], "unset", "asked"
        )
        followup = self.ask(f"also the changelog for {ticket.id}", thread="side")
        self.router_runs(f"deez super-clanker attach {followup.id} {ticket.id} >> {self.out}")

        result = self.wake()

        self.assertEqual((result.batch, result.decided), (1, 1))
        self.assertEqual(
            self.out.read_text(encoding="utf-8"), f"attached {followup.id} → {ticket.id}\n"
        )
        again = self.deez("attach", followup.id, ticket.id)
        self.assertEqual(again, (0, f"attached {followup.id} → {ticket.id}\n", ""))
        related = summaries(self.store.show(ticket.id))
        self.assertEqual(related.count(f"input trigger: {followup.id}"), 1)
        self.assertEqual(related.count("subscribed"), 2)
        self.assertFalse(
            [s for s in summaries(self.store.show(followup.id)) if s.startswith("decision")]
        )

    def test_reply_over_100_words_refused(self):
        self.received("om", "om:chat:general", "daryl", "status?")
        self.ask("status?")

        refused = self.deez("reply", "om:chat:general", "--text", " ".join(["word"] * 101))
        im = self.deez("reply", "om:chat:general", "--text", " ".join(["word"] * 99))
        tty = self.deez("reply", "terminal:default", "--text", " ".join(["word"] * 150))

        self.assertEqual(refused, (2, "", "deez: reply is 101 words; IM replies stay under 100\n"))
        self.assertEqual(im[0], 0)
        self.assertRegex(im[1], r"^reply p_[0-9a-f]{10} queued for om:chat:general\n$")
        self.assertEqual(tty[0], 0)
        self.assertRegex(tty[1], r"^reply p_[0-9a-f]{10} queued for terminal:default\n$")
        self.assertEqual(
            sorted(reply.thread_id for reply in self.store.unsent_replies()),
            ["om:chat:general", "terminal:default"],
        )
        self.assertIn(
            "reply: " + " ".join(["word"] * 12) + "…", summaries(self.store.show("om:chat:general"))
        )

    def test_dispatch_refuses_unadmitted_trigger_and_unknown_playbook(self):
        stranger = self.received("om", "om:chat:general", "mallory", "do my homework")
        request = self.ask("fix the typo")

        unadmitted = self.deez("dispatch", stranger.id, "--slug", "homework", "--playbook", "bug-fix")
        unknown = self.deez("dispatch", request.id, "--slug", "fix-typo", "--playbook", "no-such")
        escaping = self.deez("dispatch", request.id, "--slug", "fix-typo", "--playbook", "../SKILL")
        bad_slug = self.deez("dispatch", request.id, "--slug", "Fix Typo", "--playbook", "bug-fix")

        self.assertEqual(unadmitted, (2, "", f"deez: {stranger.id} is not admitted (source)\n"))
        self.assertEqual(unknown[0], 2)
        self.assertIn("no-such", unknown[2])
        self.assertEqual(escaping[0], 2)
        self.assertEqual(bad_slug[0], 2)
        self.assertEqual(self.store.status(), [])
        self.assertEqual(self.queued_ids(), [stranger.id, request.id])

    def test_second_decision_on_a_trigger_is_refused(self):
        accepted = self.ask("fix the typo")
        ignored = self.ask("thanks", thread="chatter")
        self.deez("dispatch", accepted.id, "--slug", "fix-typo", "--playbook", "bug-fix")
        self.deez("ignore", ignored.id, "--reason", "chatter")
        ticket_id = self.store.status()[0]["ticket"]

        ignore_after_accept = self.deez("ignore", accepted.id, "--reason", "done")
        dispatch_after_ignore = self.deez(
            "dispatch", ignored.id, "--slug", "thanks", "--playbook", "bug-fix"
        )
        attach_after_ignore = self.deez("attach", ignored.id, ticket_id)
        redispatch = self.deez("dispatch", accepted.id, "--slug", "fix-typo", "--playbook", "bug-fix")

        self.assertEqual(
            ignore_after_accept,
            (2, "", f"deez: {accepted.id} is already decided; see deez super-clanker show {accepted.id}\n"),
        )
        self.assertEqual(dispatch_after_ignore[0], 2)
        self.assertEqual(attach_after_ignore[0], 2)
        self.assertEqual(redispatch[0], 0)
        self.assertEqual(len(self.store.status()), 1)
        decisions = [s for s in summaries(self.store.show(accepted.id)) if s.startswith("decision")]
        self.assertEqual(decisions, ["decision accept: dispatch by router: addressed"])
        self.assertEqual(
            [s for s in summaries(self.store.show(ignored.id)) if s.startswith("decision")],
            ["decision ignore: chatter"],
        )

    def test_note_and_stop_reach_the_ticket(self):
        request = self.ask("fix the typo")
        self.deez("dispatch", request.id, "--slug", "fix-typo", "--playbook", "bug-fix")
        ticket_id = self.store.status()[0]["ticket"]

        noted = self.deez("note", ticket_id, "--text", "the README moved to docs/")
        stopped = self.deez("stop", ticket_id, "--reason", "daryl said stop", "--by", "daryl")
        attach = self.deez("attach", self.ask("one more").id, ticket_id)

        self.assertEqual(noted, (0, f"noted {ticket_id}\n", ""))
        self.assertEqual(stopped, (0, f"stopped {ticket_id}\n", ""))
        self.assertEqual(attach[0], 2)
        shown = self.store.show(ticket_id)
        self.assertEqual((shown["state"], shown["ended_by"]), ("ended", "daryl"))
        self.assertIn("input note: the README moved to docs/", summaries(shown))

    def test_attach_refuses_router_stopped_ticket_and_allows_work_ended_ticket(self):
        stopped_request = self.ask("fix the typo", thread="stopped")
        ended_request = self.ask("tidy the changelog", thread="ended")
        self.deez("dispatch", stopped_request.id, "--slug", "fix-typo", "--playbook", "bug-fix")
        self.deez("dispatch", ended_request.id, "--slug", "tidy", "--playbook", "bug-fix")
        stopped_ticket, ended_ticket = (row["ticket"] for row in self.store.status())
        self.deez("stop", stopped_ticket, "--reason", "daryl said stop in the room")
        self.store.end_ticket(ended_ticket, "dropped")
        late = self.ask("one more thing", thread="late")
        followup = self.ask("and the date", thread="later")

        refused = self.deez("attach", late.id, stopped_ticket)
        allowed = self.deez("attach", followup.id, ended_ticket)

        self.assertEqual(refused, (2, "", f"deez: {stopped_ticket} was stopped by router\n"))
        self.assertEqual(self.store.fanout_targets(late.thread_id), [])
        self.assertEqual(allowed, (0, f"attached {followup.id} → {ended_ticket}\n", ""))
        self.assertEqual(self.store.fanout_targets(followup.thread_id), [ended_ticket])
        self.assertIn(f"input trigger: {followup.id}", summaries(self.store.show(ended_ticket)))

    def test_wake_dry_run_prints_prompt_and_writes_nothing(self):
        stranger = self.received("om", "om:chat:general", "mallory", "do my homework")
        request = self.ask("fix the typo")

        code, out, _err = self.deez("wake", "--dry-run")

        self.assertEqual(code, 0)
        self.assertIn(f"not admitted: {stranger.id}", out)
        self.assertIn(f"## {request.id}  terminal", out)
        self.assertEqual(self.argvs(), [])
        self.assertEqual(self.queued_ids(), [stranger.id, request.id])
        self.assertFalse((self.root / "router.session").exists())

    def test_wake_verb_prints_summary(self):
        self.assertEqual(self.deez("wake"), (0, "nothing to wake\n", ""))
        request = self.ask("fix the typo")
        self.router_runs(f"deez super-clanker ignore {request.id} --reason chatter > /dev/null")

        code, out, _err = self.deez("wake")

        self.assertEqual(code, 0)
        self.assertRegex(out, r"^wake w_[0-9a-f]{10} batch 1 decided 1 denied 0 cost 0\.0010\n$")

    def test_wake_failure_records_exit_and_raises(self):
        request = self.ask("fix the typo")
        os.environ["FAKE_CLAUDE_EXIT"] = "3"

        with self.assertRaises(SuperError) as raised:
            self.wake()

        wake_id = re.search(r"w_[0-9a-f]{10}", str(raised.exception)).group(0)
        wake = self.store.show(wake_id)
        self.assertEqual(wake["exit_code"], 3)
        self.assertIn("fake claude failed with 3", wake["result"])
        self.assertIsNotNone(wake["ended_at"])
        self.assertEqual(self.queued_ids(), [request.id])

        os.environ["FAKE_CLAUDE_EXIT"] = "0"
        self.wake()
        failed, retried = self.argvs()
        self.assertIn("--session-id", retried)
        self.assertNotEqual(
            failed[failed.index("--session-id") + 1], retried[retried.index("--session-id") + 1]
        )


    def test_route_runs_each_line_and_continues_past_a_failure(self):
        first = self.ask("thanks")
        second = self.ask("cheers", thread="other")

        code, out, err = self.route(
            f'ignore {first.id} --reason "chatter one"\n'
            "ignore t_0000000000 --reason missing\n"
            f"ignore {second.id} --reason 'chatter two'\n"
        )

        self.assertEqual(code, 2)
        self.assertEqual(err, "route line 2: nothing has id t_0000000000\n")
        self.assertEqual(out, f"1: ignored {first.id}\n3: ignored {second.id}\n")
        self.assertEqual(self.decisions(first.id), ["decision ignore: chatter one"])
        self.assertEqual(self.decisions(second.id), ["decision ignore: chatter two"])

    def test_route_refuses_non_routable_verb(self):
        request = self.ask("fix the typo")

        code, out, err = self.route(
            "wake\n"
            f"ignore {request.id}\n"
            f"ignore {request.id} --reason chatter\n"
        )

        self.assertEqual(code, 2)
        self.assertEqual(err.splitlines(), [
            "route line 1: wake is not routable",
            "route line 2: deez super-clanker ignore: error: the following arguments are required: "
            "--reason",
        ])
        self.assertEqual(out, f"3: ignored {request.id}\n")
        self.assertEqual(self.decisions(request.id), ["decision ignore: chatter"])
        self.assertEqual(self.argvs(), [])

    def test_route_prefixes_output_with_line_numbers(self):
        first = self.ask("fix the typo")
        ticket = self.store.accept(
            first.id, "fix-typo", "explicit", "terminal:default", [], "unset", "asked"
        )
        thanks = self.ask("thanks", thread="chatter")

        code, out, err = self.route(
            "# a note, a decision and a reply\n"
            "\n"
            f"note {ticket.id} --text 'the README moved to docs/'\n"
            f'ignore {thanks.id} --reason "said thanks"\n'
            "reply terminal:chatter --text 'you are welcome'\n"
        )

        self.assertEqual((code, err), (0, ""))
        self.assertRegex(
            out,
            rf"^3: noted {ticket.id}\n4: ignored {thanks.id}\n"
            r"5: reply p_[0-9a-f]{10} queued for terminal:chatter\n$",
        )
        self.assertIn(
            "input note: the README moved to docs/", summaries(self.store.show(ticket.id))
        )
        self.assertEqual(self.decisions(thanks.id), ["decision ignore: said thanks"])
        self.assertEqual(
            [reply.text for reply in self.store.unsent_replies()], ["you are welcome"]
        )

    def test_attach_refuses_worker_report_to_its_own_ticket(self):
        first = self.ask("fix the typo")
        own = self.store.accept(
            first.id, "fix-typo", "explicit", "terminal:default", [], "unset", "asked"
        )
        second = self.ask("and the changelog", thread="other")
        other = self.store.accept(
            second.id, "fix-changelog", "explicit", "terminal:other", [], "unset", "asked"
        )
        report = Trigger(
            trigger_id("worker", "r_0000000001"), "worker", "r_0000000001", f"worker:{own.id}",
            f"worker:{own.id}", True, "REPORT ready fixed the typo", None,
            "2026-11-02T10:30:00+00:00", {"ticket": own.id},
        )
        self.store.receive(report)
        refusal = f"{report.id} is a report from {own.id}; reply or note, then ignore it"

        direct = self.deez("attach", report.id, own.id)
        routed = self.route(f"attach {report.id} {own.id}\n")
        elsewhere = self.deez("attach", report.id, other.id)

        self.assertEqual(direct, (2, "", f"deez: {refusal}\n"))
        self.assertEqual(routed, (2, "", f"route line 1: {refusal}\n"))
        self.assertEqual(elsewhere, (0, f"attached {report.id} → {other.id}\n", ""))
        self.assertNotIn(f"input trigger: {report.id}", summaries(self.store.show(own.id)))

    def test_wake_records_permission_denials(self):
        request = self.ask("fix the typo")
        chained = (
            f"deez super-clanker ignore {request.id} --reason chatter & "
            "deez super-clanker reply terminal:default --text done"
        )
        outcome = {
            "result": "ok", "session_id": "s-1", "total_cost_usd": 0.002,
            "permission_denials": [
                {"tool_name": "Bash", "tool_use_id": "toolu_1", "tool_input": {"command": chained}},
            ],
        }
        self.claude.write_text(
            "#!/bin/sh\n"
            f"deez super-clanker ignore {request.id} --reason chatter > /dev/null\n"
            f"cat <<'OUTCOME'\n{json.dumps(outcome)}\nOUTCOME\n",
            encoding="utf-8",
        )

        code, out, _err = self.deez("wake")

        self.assertEqual(code, 0)
        self.assertRegex(out, r"^wake w_[0-9a-f]{10} batch 1 decided 1 denied 1 cost 0\.0020\n$")
        wake_id = out.split()[1]
        self.assertEqual(self.store.show(wake_id)["denials"], (chained,))
        shown = self.deez("show", wake_id)
        self.assertIn(f"denials: {json.dumps([chained])}\n", shown[1])

    def test_router_prompt_forbids_chaining_and_self_attach(self):
        prompt = router.agent_prompt(HUB)

        for phrase in ("deez super-clanker route <<", "&&", "never", "ignore"):
            self.assertIn(phrase, prompt)
        self.assertLess(len(prompt.split()), 400)

    def test_router_prompt_tells_router_to_check_rules(self):
        prompt = router.agent_prompt(HUB)

        cited = prompt.index("`--rule <name>`")
        checked = prompt.index("`deez super-clanker rules`")
        self.assertLess(cited, checked)
        self.assertNotIn("Pick the clanker-mode playbook", prompt[cited:checked])
        self.assertIn("unknown rule", prompt[checked:])
        self.assertLess(len(prompt.split()), 400)


if __name__ == "__main__":
    unittest.main()


class WorkerRoutesItselfTest(unittest.TestCase):
    def test_router_prompt_has_no_playbook_table(self):
        from pathlib import Path
        body = Path(__file__).resolve().parents[1].joinpath("agents", "super-router.md").read_text()
        self.assertNotIn("Pick the clanker-mode playbook", body)
        self.assertNotIn("`bug-fix` a defect", body)
        self.assertIn("clanker-mode", body)

    def test_dispatch_without_playbook_leaves_routing_to_the_worker(self):
        import io, os, tempfile
        from contextlib import redirect_stdout, redirect_stderr
        from pathlib import Path
        from unittest import mock
        from deezlib import cli
        from deezlib.superclanker.store import Store
        from deezlib.superclanker.sources import terminal
        tmp = tempfile.TemporaryDirectory(); self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        (root / "sources.toml").write_text('[sources.terminal]\nsenders = ["tester"]\n')
        store = Store.open(root)
        trigger, _receipt = terminal.ask(store, "fix it", actor="tester")
        store.close()
        out, err = io.StringIO(), io.StringIO()
        with mock.patch.dict(os.environ, {"DEEZ_SUPER_STATE": str(root)}), \
                redirect_stdout(out), redirect_stderr(err):
            code = cli.main(["super-clanker", "dispatch", trigger.id, "--slug", "fix-it"])
        self.assertEqual((code, err.getvalue()), (0, ""))
        self.assertIn("playbook chosen by the worker", out.getvalue())
        store = Store.open(root); self.addCleanup(store.close)
        ticket_id = out.getvalue().split("ticket ")[1].split()[0]
        self.assertEqual([i.text for i in store.inputs(ticket_id) if i.text.startswith("playbook:")], [])


class DispatchFindsTheRepoTest(unittest.TestCase):
    def test_dispatch_takes_the_repo_named_in_the_request(self):
        import io, os, subprocess, tempfile
        from contextlib import redirect_stdout, redirect_stderr
        from pathlib import Path
        from unittest import mock
        from deezlib import cli
        from deezlib.superclanker.store import Store
        from deezlib.superclanker.sources import terminal
        tmp = tempfile.TemporaryDirectory(); self.addCleanup(tmp.cleanup)
        root = Path(tmp.name) / "state"; repo = Path(tmp.name) / "proj"
        repo.mkdir(); subprocess.run(["git", "init", "-q", str(repo)], check=True)
        root.mkdir(); (root / "sources.toml").write_text('[sources.terminal]\nsenders = ["tester"]\n')
        store = Store.open(root)
        trigger, _r = terminal.ask(store, f"fix the typo in README.md of {repo} and commit", actor="tester")
        store.close()
        out, err = io.StringIO(), io.StringIO()
        with mock.patch.dict(os.environ, {"DEEZ_SUPER_STATE": str(root)}), \
                redirect_stdout(out), redirect_stderr(err):
            code = cli.main(["super-clanker", "dispatch", trigger.id, "--slug", "fix-typo"])
        self.assertEqual((code, err.getvalue()), (0, ""))
        ticket_id = out.getvalue().split("ticket ")[1].split()[0]
        store = Store.open(root); self.addCleanup(store.close)
        notes = [i.text for i in store.inputs(ticket_id) if i.text.startswith("repo:")]
        self.assertEqual(notes, [f"repo: {repo.resolve()}"])
        self.assertIn(f"repo {repo.resolve()}", out.getvalue())

    def test_router_prompt_says_to_pass_the_repo(self):
        from pathlib import Path
        body = Path(__file__).resolve().parents[1].joinpath("agents", "super-router.md").read_text()
        self.assertIn("--repo", body)


class RouterReportsReadyTest(unittest.TestCase):
    def test_router_prompt_sends_questions_about_a_ticket_to_its_worker(self):
        prompt = (HUB / "agents" / "super-router.md").read_text(encoding="utf-8")
        self.assertIn("About ticket", prompt)
        self.assertIn("attach", prompt.split("About ticket", 1)[1][:300])

    def test_router_prompt_replies_on_a_ready_report(self):
        from pathlib import Path
        body = Path(__file__).resolve().parents[1].joinpath("agents", "super-router.md").read_text()
        self.assertIn("`ready`", body)
        self.assertIn("one-line `reply`", body)

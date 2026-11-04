import json
import os
import re
import shutil
import signal
import subprocess
import tempfile
import time
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path
from unittest import mock

from deezlib import cli
from deezlib.superclanker import config, workers
from deezlib.superclanker import sweep as sweeping
from deezlib.superclanker.domain import Ticket, trigger_id
from deezlib.superclanker.sources import terminal
from deezlib.superclanker.store import Store, SuperError

HUB = cli.REPO_ROOT
FAKE = Path(__file__).with_name("fake_claude.py")
UUID = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$")
SLUG = "fix-readme-typo"
BUG_FIX = HUB / "skills" / "clanker-mode" / "playbooks" / "bug-fix.md"


def section(text, heading):
    after = text.split(f"## {heading}\n", 1)[1]
    return after.split("\n## ", 1)[0]


class WorkersTest(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.tmp = Path(tmp.name)
        self.root = self.tmp / "state"
        self.notes = self.tmp / "dev-notes"
        bin_dir = self.tmp / "bin"
        bin_dir.mkdir()
        shutil.copy(FAKE, bin_dir / "claude")
        (bin_dir / "claude").chmod(0o755)
        self.log = self.tmp / "argv.jsonl"
        git_config = self.tmp / "gitconfig"
        git_config.write_text("", encoding="utf-8")
        environ = {
            key: value for key, value in os.environ.items()
            if not key.startswith("FAKE_CLAUDE_")
        }
        environ.update({
            "PATH": f"{bin_dir}{os.pathsep}{os.environ['PATH']}",
            "FAKE_CLAUDE_LOG": str(self.log),
            "DEEZ_SUPER_STATE": str(self.root),
            "DEEZ_SUPER_DEVNOTES": str(self.notes),
            "GIT_CONFIG_GLOBAL": str(git_config),
            "GIT_CONFIG_NOSYSTEM": "1",
            "USER": "daryl",
        })
        patcher = mock.patch.dict(os.environ, environ, clear=True)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.store = Store.open(self.root)
        self.addCleanup(self.store.close)
        no_leftovers = mock.patch.object(sweeping, "leftovers", return_value=[])
        no_leftovers.start()
        self.addCleanup(no_leftovers.stop)

    def git(self, repo, *args):
        return subprocess.run(
            ["git", "-C", str(repo), *args], capture_output=True, text=True, check=True
        ).stdout.strip()

    def commit(self, repo, message):
        self.git(repo, "-c", "user.name=t", "-c", "user.email=t@example.com", "commit", "-qam", message)

    def repo(self, name="scratch-repo"):
        repo = self.tmp / name
        repo.mkdir()
        self.git(repo, "init", "-q", "-b", "main")
        (repo / "README.md").write_text("# Scratch\n\nThsi is a typo.\n", encoding="utf-8")
        self.git(repo, "add", "README.md")
        self.commit(repo, "init")
        return repo

    def deez(self, *argv):
        out, err = StringIO(), StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = cli.main(["super-clanker", *argv])
        return code, out.getvalue(), err.getvalue()

    def sources(self, text):
        (self.root / "sources.toml").write_text(text, encoding="utf-8")

    def dispatch(self, text="fix the typo in README", slug=SLUG, repo=None, thread="default"):
        trigger, _receipt = terminal.ask(self.store, text, thread_name=thread)
        extra = ["--repo", str(repo)] if repo else []
        code, out, err = self.deez(
            "dispatch", trigger.id, "--slug", slug, "--playbook", "bug-fix", *extra
        )
        self.assertEqual(code, 0, err)
        ticket_id = re.search(r"ticket (k_[0-9a-f]{10})", out).group(1)
        return trigger, ticket_id, self.store.assignment_for(ticket_id).id

    def launch(self, assignment_id):
        return workers.launch(self.store, config.load(self.root), assignment_id, HUB, self.root)

    def finish(self, pid):
        deadline = time.monotonic() + 10
        while workers.alive(pid):
            self.assertLess(time.monotonic(), deadline, "fake claude did not exit")
            time.sleep(0.01)

    def run_turn(self, assignment_id, result):
        os.environ["FAKE_CLAUDE_RESULT"] = result
        started = self.launch(assignment_id)
        self.finish(started.pid)
        return started

    def argvs(self):
        if not self.log.exists():
            return []
        return [json.loads(line) for line in self.log.read_text(encoding="utf-8").splitlines()]

    def reports(self, assignment_id):
        related = self.store.show(assignment_id)["related"]
        return [self.store.show(i) for i, _summary in related if i.startswith("r_")]

    def test_launch_writes_brief_mandate_resume_in_dev_notes(self):
        _trigger, ticket_id, assignment_id = self.dispatch()
        folder = self.notes / SLUG
        folder.mkdir(parents=True)
        (folder / ".ticket").write_text(f"{ticket_id}\n", encoding="utf-8")
        (folder / "resume.md").write_text("kept from an earlier session\n", encoding="utf-8")

        started = self.launch(assignment_id)
        self.finish(started.pid)

        self.assertEqual(
            sorted(p.name for p in folder.iterdir()),
            [".ticket", "brief.md", "mandate.md", "resume.md"],
        )
        self.assertEqual(
            (folder / "resume.md").read_text(encoding="utf-8"), "kept from an earlier session\n"
        )
        mandate = (folder / "mandate.md").read_text(encoding="utf-8")
        for fact in (ticket_id, SLUG, "terminal:default", "explicit", "daryl",
                     "dispatch by router: addressed", "default branch", "pull request"):
            self.assertIn(fact, mandate)
        self.assertNotIn("push any branch", mandate)
        self.assertNotIn("open or update a review", mandate)

        _other, other_ticket, other_assignment = self.dispatch(
            "tidy the changelog", "tidy-changelog", thread="other"
        )
        self.finish(self.launch(other_assignment).pid)
        fresh = (self.notes / "tidy-changelog" / "resume.md").read_text(encoding="utf-8")
        self.assertIn("read brief.md", fresh)
        self.assertIn(str(self.root / "work" / other_ticket), fresh)
        self.assertIn(str(BUG_FIX), fresh)

    def test_second_ticket_with_same_slug_gets_its_own_folder(self):
        _first, first_ticket, first = self.dispatch()
        _second, second_ticket, second = self.dispatch("fix the other typo", thread="other")

        self.finish(self.launch(first).pid)
        self.finish(self.launch(second).pid)

        mine = self.notes / SLUG
        theirs = self.notes / f"{SLUG}-{second_ticket}"
        self.assertEqual((mine / ".ticket").read_text(encoding="utf-8").strip(), first_ticket)
        self.assertEqual((theirs / ".ticket").read_text(encoding="utf-8").strip(), second_ticket)
        self.assertIn(first_ticket, (mine / "brief.md").read_text(encoding="utf-8"))
        self.assertNotIn(second_ticket, (mine / "brief.md").read_text(encoding="utf-8"))
        self.assertIn(second_ticket, (theirs / "brief.md").read_text(encoding="utf-8"))
        self.assertIn(second_ticket, (theirs / "mandate.md").read_text(encoding="utf-8"))
        self.assertEqual(self.argvs()[-1][-1].split(" the handoff at ")[1].split(". ")[0],
                         str(theirs / "brief.md"))

    def test_relaunch_reuses_the_folder_it_marked(self):
        _trigger, ticket_id, assignment_id = self.dispatch()
        self.finish(self.launch(assignment_id).pid)
        folder = self.notes / SLUG
        (folder / "resume.md").write_text("step 2 of 5 done\n", encoding="utf-8")

        code, _out, err = self.deez("retry", ticket_id)
        self.assertEqual(code, 0, err)
        fresh = self.store.assignment_for(ticket_id).id
        self.finish(self.launch(fresh).pid)

        self.assertEqual(sorted(p.name for p in self.notes.iterdir()), [SLUG])
        self.assertEqual((folder / ".ticket").read_text(encoding="utf-8").strip(), ticket_id)
        self.assertEqual((folder / "resume.md").read_text(encoding="utf-8"), "step 2 of 5 done\n")
        self.assertIn(fresh, (folder / "brief.md").read_text(encoding="utf-8"))

    def test_brief_cites_playbook_mandate_and_carries_the_task_to_a_review(self):
        _trigger, ticket_id, assignment_id = self.dispatch("fix the typo\nin README line 3")
        self.store.add_input(ticket_id, "note", "the README moved to docs/")

        self.finish(self.launch(assignment_id).pid)

        brief = (self.notes / SLUG / "brief.md").read_text(encoding="utf-8")
        headings = re.findall(r"^## (.+)$", brief, re.M)
        self.assertEqual(
            headings,
            ["Goal, in one line", "Read first", "Where you work", "Deliver", "You must not", "Inputs",
             "Report protocol"],
        )
        self.assertIn("fix the typo in README line 3", section(brief, "Goal, in one line"))
        read_first = section(brief, "Read first")
        self.assertIn(str(HUB / "skills" / "clanker-mode" / "SKILL.md"), read_first)
        self.assertIn(str(BUG_FIX), read_first)
        self.assertIn(str(self.notes / SLUG / "mandate.md"), read_first)
        deliver = section(brief, "Deliver")
        for word in ("push", "pull request", "merge request", "never draft", "--evidence", "ready"):
            self.assertIn(word, deliver)
        forbidden = section(brief, "You must not")
        for word in ("merge", "default branch", "force-push", "room", "delete branches"):
            self.assertIn(word, forbidden)
        self.assertNotIn("- push any branch", forbidden)
        inputs = section(brief, "Inputs")
        self.assertIn(f"- note: playbook: {BUG_FIX}", inputs)
        self.assertIn("- note: the README moved to docs/", inputs)
        protocol = section(brief, "Report protocol")
        self.assertIn(f"deez super-clanker report {assignment_id} --kind", protocol)
        self.assertIn("REPORT <kind> <text>", protocol)
        self.assertEqual(self.store.undelivered_inputs(ticket_id), [])

    def test_launch_creates_worktree_on_daryl_branch(self):
        repo = self.repo()
        _trigger, ticket_id, assignment_id = self.dispatch(repo=repo)
        cwd_file = self.tmp / "cwd.txt"
        os.environ["FAKE_CLAUDE_SCRIPT"] = f"pwd -P > {cwd_file}"

        started = self.launch(assignment_id)
        self.finish(started.pid)

        worktree = self.root / "worktrees" / "scratch-repo" / ticket_id
        self.assertEqual(started.worktree, str(worktree))
        self.assertEqual(self.git(worktree, "branch", "--show-current"), f"daryl/{SLUG}")
        self.assertTrue((worktree / "README.md").is_file())
        self.assertEqual(cwd_file.read_text(encoding="utf-8").strip(), str(worktree.resolve()))
        brief = (self.notes / SLUG / "brief.md").read_text(encoding="utf-8")
        self.assertIn(str(worktree), section(brief, "Where you work"))
        self.assertIn(f"daryl/{SLUG}", section(brief, "Where you work"))
        with self.assertRaisesRegex(SuperError, "running"):
            self.launch(assignment_id)
        self.assertEqual(len(self.argvs()), 1)

    def test_prepare_workspace_reuses_worktree_and_branch(self):
        repo = self.repo()
        _trigger, ticket_id, _assignment_id = self.dispatch(repo=repo)
        shown = self.store.show(ticket_id)
        shown.pop("related")
        ticket = Ticket(**shown)
        (repo / "README.md").write_text("changed on main\n", encoding="utf-8")
        self.commit(repo, "two")

        first = workers.prepare_workspace(ticket, repo, SLUG, self.root)
        (Path(first[0]) / "work.txt").write_text("in progress\n", encoding="utf-8")
        again = workers.prepare_workspace(ticket, repo, SLUG, self.root)
        self.git(repo, "worktree", "remove", "--force", str(first[0]))
        rebuilt = workers.prepare_workspace(ticket, repo, SLUG, self.root)

        self.assertEqual(first, again)
        self.assertEqual(first, rebuilt)
        self.assertEqual(first[1], f"daryl/{SLUG}")
        self.assertEqual(
            (Path(rebuilt[0]) / "README.md").read_text(encoding="utf-8"), "changed on main\n"
        )
        self.assertEqual(self.git(rebuilt[0], "branch", "--show-current"), f"daryl/{SLUG}")

    def test_launch_without_repo_uses_scratch_directory(self):
        _trigger, ticket_id, assignment_id = self.dispatch()
        cwd_file = self.tmp / "cwd.txt"
        os.environ["FAKE_CLAUDE_SCRIPT"] = f"pwd -P > {cwd_file}"

        started = self.launch(assignment_id)
        self.finish(started.pid)

        scratch = self.root / "work" / ticket_id
        self.assertEqual(started.worktree, str(scratch))
        self.assertEqual(cwd_file.read_text(encoding="utf-8").strip(), str(scratch.resolve()))
        self.assertFalse((self.root / "worktrees").exists())
        where = section((self.notes / SLUG / "brief.md").read_text(encoding="utf-8"), "Where you work")
        self.assertIn(str(scratch), where)
        self.assertNotIn("daryl/", where)

    def test_launch_argv_names_agent_session_and_bypass(self):
        _trigger, _ticket_id, assignment_id = self.dispatch()
        env_file = self.tmp / "env.txt"
        os.environ["CLAUDECODE"] = "1"
        os.environ["FAKE_CLAUDE_SCRIPT"] = (
            f'echo "$DEEZ_SUPER_STATE ${{CLAUDECODE:-unset}} $(command -v deez)" > {env_file}'
        )

        started = self.launch(assignment_id)
        self.finish(started.pid)

        (argv,) = self.argvs()
        brief = self.notes / SLUG / "brief.md"
        self.assertEqual(argv[:3], ["-p", "--agent", "clanker-agent"])
        self.assertRegex(argv[argv.index("--session-id") + 1], UUID)
        self.assertEqual(argv[argv.index("--session-id") + 1], started.session_id)
        self.assertEqual(argv[argv.index("--permission-mode") + 1], "bypassPermissions")
        self.assertEqual(argv[argv.index("--output-format") + 1], "json")
        self.assertIn("--strict-mcp-config", argv)
        self.assertNotIn("--setting-sources", argv)
        self.assertNotIn("--model", argv)
        self.assertEqual(
            argv[-1],
            f"/clanker-mode Read and execute, exactly, the handoff at {brief}. "
            "Return the artifact and your own account of it.",
        )
        self.assertEqual(
            env_file.read_text(encoding="utf-8").split(),
            [str(self.root), "unset", str(HUB / "bin" / "deez")],
        )
        self.assertEqual((started.state, type(started.pid)), ("running", int))
        output = json.loads(
            (self.root / "log" / f"{assignment_id}.json").read_text(encoding="utf-8")
        )
        self.assertEqual(output["session_id"], started.session_id)

        self.sources('[workers]\nmodel = "opus"\n')
        _again, _other_ticket, other = self.dispatch("another", "another-one", thread="other")
        self.finish(self.launch(other).pid)
        modelled = self.argvs()[-1]
        self.assertEqual(modelled[modelled.index("--model") + 1], "opus")

    def test_launch_refuses_over_max_running(self):
        self.sources("[workers]\nmax_running = 1\n")
        _first, _first_ticket, first = self.dispatch()
        _second, _second_ticket, second = self.dispatch(
            "tidy the changelog", "tidy-changelog", thread="other"
        )
        self.finish(self.launch(first).pid)

        with self.assertRaisesRegex(SuperError, "1 of 1 workers running"):
            self.launch(second)

        self.assertEqual(self.store.show(second)["state"], "pending")
        self.assertEqual(len(self.argvs()), 1)

    def test_reap_emits_report_trigger_once(self):
        _trigger, ticket_id, assignment_id = self.dispatch()
        self.run_turn(assignment_id, "fixed the typo\nREPORT ready diff at /x")

        reaped = workers.reap(self.store, self.root)
        again = workers.reap(self.store, self.root)

        (trigger,) = reaped
        (report,) = self.reports(assignment_id)
        self.assertEqual((report["kind"], report["text"]), ("ready", "diff at /x"))
        self.assertEqual(
            (trigger.source, trigger.source_event_id, trigger.thread_id, trigger.actor,
             trigger.addressed, trigger.text),
            ("worker", report["id"], f"worker:{ticket_id}", f"worker:{ticket_id}", True,
             "REPORT ready diff at /x"),
        )
        self.assertEqual(
            trigger.meta,
            {"ticket": ticket_id, "assignment": assignment_id, "report": report["id"],
             "question": None, "evidence": None},
        )
        self.assertEqual(self.store.show(trigger.id)["text"], "REPORT ready diff at /x")
        self.assertEqual(again, [])
        self.assertEqual(self.store.show(ticket_id)["state"], "open")
        self.assertEqual(self.store.show(assignment_id)["state"], "ended")

    def test_reap_sweeps_worktree_once_before_marking_reaped(self):
        _trigger, _ticket_id, assignment_id = self.dispatch()
        started = self.run_turn(assignment_id, "fixed the typo\nREPORT ready diff at /x")
        swept = []

        workers.reap(self.store, self.root, sweep=swept.append)
        workers.reap(self.store, self.root, sweep=swept.append)

        self.assertEqual(swept, [started.worktree])

    def test_reap_without_report_records_failed(self):
        _trigger, ticket_id, assignment_id = self.dispatch()
        os.environ["FAKE_CLAUDE_EXIT"] = "1"
        self.run_turn(assignment_id, "I could not finish")

        (trigger,) = workers.reap(self.store, self.root)

        (report,) = self.reports(assignment_id)
        self.assertEqual(report["kind"], "failed")
        self.assertTrue(report["text"].startswith("worker exited without a report"))
        self.assertIn("fake claude failed with 1", report["text"])
        self.assertTrue(trigger.text.startswith("REPORT failed worker exited without a report"))
        self.assertEqual(trigger.thread_id, f"worker:{ticket_id}")
        self.assertEqual(self.store.show(assignment_id)["state"], "ended")
        self.assertEqual(workers.reap(self.store, self.root), [])

    def test_dropped_report_ends_ticket_without_ended_by(self):
        trigger, ticket_id, assignment_id = self.dispatch()
        self.run_turn(assignment_id, "REPORT dropped already fixed on main")

        (reaped,) = workers.reap(self.store, self.root)

        ticket = self.store.show(ticket_id)
        self.assertEqual((ticket["state"], ticket["ended_by"]), ("ended", None))
        self.assertIsNotNone(ticket["ended_at"])
        self.assertEqual(reaped.text, "REPORT dropped already fixed on main")
        self.assertEqual(self.store.fanout_targets(trigger.thread_id), [ticket_id])

    def test_resume_passes_inputs_to_same_session_and_marks_delivered(self):
        _trigger, ticket_id, assignment_id = self.dispatch()
        started = self.run_turn(assignment_id, "REPORT waiting which README, root or docs?")
        settings = config.load(self.root)
        followup, _receipt = terminal.ask(self.store, "the one in docs/")
        self.assertEqual(self.deez("attach", followup.id, ticket_id)[0], 0)
        self.store.add_input(ticket_id, "note", "docs/ was renamed to guide/")

        with self.assertRaisesRegex(SuperError, "reap"):
            workers.resume(self.store, settings, assignment_id, HUB, self.root)
        (waiting,) = workers.reap(self.store, self.root)
        resumed = workers.resume(self.store, settings, assignment_id, HUB, self.root)
        self.finish(resumed.pid)

        self.assertEqual(waiting.meta["question"], "which README, root or docs?")
        self.assertEqual(self.store.show(assignment_id)["state"], "running")
        launch_argv, resume_argv = self.argvs()
        self.assertEqual(launch_argv[launch_argv.index("--session-id") + 1], started.session_id)
        self.assertEqual(resume_argv[resume_argv.index("--resume") + 1], started.session_id)
        self.assertNotIn("--session-id", resume_argv)
        self.assertEqual(
            resume_argv[resume_argv.index("--permission-mode") + 1], "bypassPermissions"
        )
        message = resume_argv[-1]
        self.assertTrue(message.startswith(f"# inputs for {ticket_id}\n"))
        self.assertIn(f"## {followup.id} terminal terminal:default daryl\nthe one in docs/", message)
        self.assertIn("## note\ndocs/ was renamed to guide/", message)
        self.assertNotEqual(resumed.pid, started.pid)
        self.assertEqual(self.store.undelivered_inputs(ticket_id), [])
        self.assertTrue((self.root / "log" / f"{assignment_id}.1.json").is_file())
        self.assertIsNone(workers.resume(self.store, settings, assignment_id, HUB, self.root))
        self.assertEqual(len(self.argvs()), 2)
        (asked_again,) = workers.reap(self.store, self.root)
        self.assertNotEqual(asked_again.meta["report"], waiting.meta["report"])
        self.assertEqual(
            [r["kind"] for r in self.reports(assignment_id)], ["waiting", "waiting"]
        )

    def test_followup_on_work_ended_ticket_revives_it_in_the_same_session(self):
        _trigger, ticket_id, assignment_id = self.dispatch()
        started = self.run_turn(assignment_id, "REPORT dropped already fixed on main")
        workers.reap(self.store, self.root)
        self.assertEqual(self.store.show(ticket_id)["state"], "ended")
        followup, _receipt = terminal.ask(self.store, "it is not fixed, look again")
        self.assertEqual(self.deez("attach", followup.id, ticket_id)[0], 0)
        cwd = self.tmp / "cwd.txt"
        os.environ["FAKE_CLAUDE_SCRIPT"] = f"pwd > {cwd}"

        revived = workers.revive(self.store, config.load(self.root), ticket_id, HUB, self.root)
        self.finish(revived.pid)

        ticket = self.store.show(ticket_id)
        self.assertEqual(
            (ticket["state"], ticket["ended_at"], ticket["ended_by"]), ("open", None, None)
        )
        self.assertNotEqual(revived.id, assignment_id)
        self.assertEqual(self.store.assignment_for(ticket_id).id, revived.id)
        self.assertEqual(self.store.show(revived.id)["state"], "running")
        self.assertEqual(self.store.show(assignment_id)["state"], "ended")
        self.assertEqual(revived.session_id, started.session_id)
        _launch_argv, revive_argv = self.argvs()
        self.assertEqual(revive_argv[revive_argv.index("--resume") + 1], started.session_id)
        self.assertNotIn("--session-id", revive_argv)
        message = revive_argv[-1]
        self.assertTrue(message.startswith(f"# inputs for {ticket_id}\n"))
        self.assertIn(f"## {followup.id} terminal terminal:default daryl\nit is not fixed", message)
        self.assertEqual(
            Path(cwd.read_text(encoding="utf-8").strip()).resolve(),
            Path(started.worktree).resolve(),
        )
        self.assertEqual(self.store.undelivered_inputs(ticket_id), [])
        self.assertTrue((self.root / "log" / f"{revived.id}.json").is_file())
        self.assertIsNone(
            workers.revive(self.store, config.load(self.root), ticket_id, HUB, self.root)
        )
        self.assertEqual(len(self.argvs()), 2)

    def test_revive_refuses_a_person_stopped_ticket(self):
        _trigger, ticket_id, assignment_id = self.dispatch()
        self.run_turn(assignment_id, "REPORT ready diff at /x")
        workers.reap(self.store, self.root)
        self.assertEqual(self.deez("stop", ticket_id, "--reason", "done", "--by", "daryl")[0], 0)
        self.store.add_input(ticket_id, "note", "one more thing")

        with self.assertRaisesRegex(SuperError, f"{ticket_id} was stopped by daryl"):
            workers.revive(self.store, config.load(self.root), ticket_id, HUB, self.root)

        self.assertEqual(self.store.show(ticket_id)["state"], "ended")
        self.assertEqual(self.store.assignment_for(ticket_id).id, assignment_id)
        self.assertEqual(len(self.store.undelivered_inputs(ticket_id)), 1)
        self.assertEqual(len(self.argvs()), 1)

    def test_revive_waits_for_a_free_worker_slot(self):
        self.sources("[workers]\nmax_running = 1\n")
        _trigger, ticket_id, assignment_id = self.dispatch()
        self.run_turn(assignment_id, "REPORT dropped already fixed on main")
        workers.reap(self.store, self.root)
        _busy, _busy_ticket, busy = self.dispatch("tidy the changelog", "tidy-changelog", thread="other")
        self.store.start_assignment(busy, "sid", os.getpid(), self.root)
        self.store.add_input(ticket_id, "note", "look again")

        with self.assertRaisesRegex(SuperError, "1 of 1 workers running"):
            workers.revive(self.store, config.load(self.root), ticket_id, HUB, self.root)

        self.assertEqual(self.store.show(ticket_id)["state"], "ended")
        self.assertEqual(self.store.assignment_for(ticket_id).id, assignment_id)
        self.assertEqual(len(self.argvs()), 1)

    def pushed(self, ticket_id):
        return [t for t in self.store.queued() if t.thread_id == f"worker:{ticket_id}"]

    def test_attention_report_verb_pushes_to_the_router_at_once(self):
        _trigger, ticket_id, assignment_id = self.dispatch()

        nudge = self.root / "nudge"
        nudge.unlink(missing_ok=True)
        self.deez("report", assignment_id, "--kind", "progress", "--text", "halfway")
        self.assertEqual(self.pushed(ticket_id), [])
        self.assertFalse(nudge.exists())

        self.deez("report", assignment_id, "--kind", "blocked", "--text", "need a login")
        (trigger,) = self.pushed(ticket_id)
        (_progress, blocked) = self.reports(assignment_id)
        self.assertEqual(trigger.id, trigger_id("worker", blocked["id"]))
        self.assertEqual(trigger.text, "REPORT blocked need a login")
        self.assertEqual(trigger.meta["assignment"], assignment_id)
        self.assertTrue(nudge.exists())

    def test_worker_report_verb_is_not_duplicated_by_reap(self):
        _trigger, ticket_id, assignment_id = self.dispatch()
        os.environ["FAKE_CLAUDE_SCRIPT"] = (
            f"deez super-clanker report {assignment_id} --kind ready --text 'diff at /x' "
            "--evidence /x/diff.patch > /dev/null"
        )
        self.run_turn(assignment_id, "done\nREPORT ready diff at /x")

        (trigger,) = self.pushed(ticket_id)
        self.assertEqual(workers.reap(self.store, self.root), [])

        (report,) = self.reports(assignment_id)
        self.assertEqual(
            (report["kind"], report["text"], report["evidence"]),
            ("ready", "diff at /x", ("/x/diff.patch",)),
        )
        self.assertEqual(trigger.meta["report"], report["id"])
        self.assertEqual(trigger.meta["evidence"], ["/x/diff.patch"])
        self.assertEqual(workers.reap(self.store, self.root), [])
        self.assertEqual(self.store.show(ticket_id)["state"], "open")

    def test_worker_waiting_report_is_not_duplicated_by_reap(self):
        _trigger, ticket_id, assignment_id = self.dispatch()
        os.environ["FAKE_CLAUDE_SCRIPT"] = (
            f"deez super-clanker report {assignment_id} --kind waiting --text 'push the branch?' "
            "--question 'push the branch?' > /dev/null"
        )
        self.run_turn(assignment_id, "REPORT waiting push the branch?")

        (trigger,) = self.pushed(ticket_id)
        self.assertEqual(workers.reap(self.store, self.root), [])

        (report,) = self.reports(assignment_id)
        self.assertEqual(trigger.meta["report"], report["id"])
        self.assertEqual(trigger.meta["question"], "push the branch?")
        self.assertEqual(self.store.show(assignment_id)["state"], "running")

    def test_waiting_report_requires_a_question(self):
        _trigger, _ticket_id, assignment_id = self.dispatch()
        self.finish(self.launch(assignment_id).pid)

        refused = self.deez("report", assignment_id, "--kind", "waiting", "--text", "stuck")
        accepted = self.deez(
            "report", assignment_id, "--kind", "waiting", "--text", "stuck on the gate",
            "--question", "push the branch?",
        )

        self.assertEqual(refused[0], 2)
        self.assertIn("--question", refused[2])
        self.assertEqual(accepted[0], 0)
        self.assertRegex(accepted[1], rf"^report r_[0-9a-f]{{10}} waiting on {assignment_id} pushed to the router\n$")
        (report,) = self.reports(assignment_id)
        self.assertEqual((report["kind"], report["question"]), ("waiting", "push the branch?"))

    def test_cli_verbs_launch_deliver_reap_and_kill(self):
        repo = self.repo()
        _trigger, ticket_id, assignment_id = self.dispatch(repo=repo)
        os.environ["FAKE_CLAUDE_SCRIPT"] = "sleep 30"

        launched = self.deez("launch", ticket_id)
        busy = self.deez("deliver", ticket_id)
        quiet = self.deez("reap")
        killed = self.deez("kill", assignment_id)
        reaped = self.deez("reap")

        worktree = self.root / "worktrees" / "scratch-repo" / ticket_id
        self.assertRegex(
            launched[1],
            rf"^launched {assignment_id} session [0-9a-f-]{{36}} pid \d+ in "
            rf"{re.escape(str(worktree))}\n$",
        )
        self.assertEqual(busy, (0, "nothing to deliver\n", ""))
        self.assertEqual(quiet, (0, "nothing to reap\n", ""))
        self.assertEqual(killed, (0, f"stopped {assignment_id}\n", ""))
        self.assertFalse(workers.alive(self.store.show(assignment_id)["pid"]))
        self.assertRegex(reaped[1], rf"^report failed for {ticket_id} → t_[0-9a-f]{{10}}\n$")
        (report,) = self.reports(assignment_id)
        self.assertEqual((report["kind"], report["text"]), ("failed", "stopped by operator"))
        self.assertEqual(self.store.show(assignment_id)["state"], "ended")

    def test_stop_sweeps_worktree_after_signalling_the_group(self):
        _trigger, _ticket_id, assignment_id = self.dispatch()
        started = self.run_turn(assignment_id, "working")
        swept = []

        workers.stop(self.store, assignment_id, sweep=swept.append)

        self.assertEqual(swept, [started.worktree])
        (report,) = self.reports(assignment_id)
        self.assertEqual((report["kind"], report["text"]), ("failed", "stopped by operator"))

    def test_stop_records_the_given_reason(self):
        _trigger, _ticket_id, assignment_id = self.dispatch()
        self.run_turn(assignment_id, "working")

        workers.stop(
            self.store, assignment_id, sweep=lambda worktree: [], reason="120 minute limit reached"
        )

        (report,) = self.reports(assignment_id)
        self.assertEqual(report["text"], "120 minute limit reached")

    def test_stop_turns_an_unsignalable_pid_into_a_super_error(self):
        _trigger, _ticket_id, assignment_id = self.dispatch()
        self.run_turn(assignment_id, "working")
        self.store.start_assignment(assignment_id, "session", 99999999, self.root)

        def refuse(pid, signum):
            raise PermissionError(1, "Operation not permitted")

        with self.assertRaises(SuperError):
            workers.stop(self.store, assignment_id, kill=refuse, sweep=lambda worktree: [])

        self.assertEqual(self.reports(assignment_id), [])

    def test_terminate_signals_the_group_and_sweeps_without_a_report(self):
        _trigger, _ticket_id, assignment_id = self.dispatch()
        os.environ["FAKE_CLAUDE_SCRIPT"] = "sleep 30"
        started = self.launch(assignment_id)
        self.addCleanup(lambda: workers.alive(started.pid) and os.killpg(started.pid, signal.SIGKILL))
        swept = []

        workers.terminate(started, sweep=swept.append, grace_seconds=5)

        self.assertFalse(workers.alive(started.pid))
        self.assertEqual(swept, [started.worktree])
        self.assertEqual(self.reports(assignment_id), [])

    def test_dispatch_records_repo_beside_playbook(self):
        repo = self.repo()
        stray, _receipt = terminal.ask(self.store, "another", thread_name="other")

        _trigger, ticket_id, _assignment_id = self.dispatch(repo=repo)
        missing = self.deez(
            "dispatch", stray.id, "--slug", "another", "--playbook", "bug-fix",
            "--repo", str(self.tmp / "nowhere"),
        )

        self.assertEqual(
            [(i.kind, i.text) for i in self.store.undelivered_inputs(ticket_id)],
            [("note", f"playbook: {BUG_FIX}"), ("note", f"repo: {repo.resolve()}")],
        )
        self.assertEqual(missing[0], 2)
        self.assertIn("nowhere", missing[2])
        self.assertEqual(len(self.store.status()), 1)


if __name__ == "__main__":
    unittest.main()


class WorkerRoutesFromClankerModeTest(unittest.TestCase):
    def test_brief_without_playbook_tells_worker_to_route_from_clanker_mode(self):
        import tempfile
        from pathlib import Path
        from deezlib.superclanker import workers
        hub = Path(__file__).resolve().parents[1]
        tmp = tempfile.TemporaryDirectory(); self.addCleanup(tmp.cleanup)
        filled = workers.brief_text(hub, {
            "clanker_skill": hub / "skills" / "clanker-mode" / "SKILL.md",
            "playbook": None, "mandate_path": "/m", "worktree": "/w", "branch": "`daryl/x`",
            "goal": "g", "inputs": "- none", "assignment_id": "a_1", "ticket_id": "k_1",
            "resume_note": "/r",
        })
        self.assertIn("playbook table", filled)
        self.assertNotIn("playbooks/feature.md", filled)


class WorkerStartsInClankerModeTest(unittest.TestCase):
    def test_launch_prompt_invokes_the_clanker_mode_command(self):
        from deezlib.superclanker import workers
        self.assertTrue(workers.launch_prompt("/b/brief.md").startswith("/clanker-mode "))
        self.assertIn("/b/brief.md", workers.launch_prompt("/b/brief.md"))

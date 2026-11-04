import unittest
from pathlib import Path
from types import SimpleNamespace

from deezlib import cli
from deezlib.superclanker import ui_launch
from deezlib.superclanker.store import SuperError

VENV = Path("/fake/venv")
PYTHON = VENV / "bin" / "python"
DEEZ = Path("/hub/bin/deez")


def recorder(*results):
    calls = []
    envs = []
    queue = list(results)

    def run(argv, **kwargs):
        calls.append([str(part) for part in argv])
        envs.append(kwargs.get("env"))
        code, err = queue.pop(0) if queue else (0, "")
        return SimpleNamespace(returncode=code, stderr=err, stdout="")

    run.envs = envs
    return run, calls


class EnsureVenvTest(unittest.TestCase):
    def test_ensure_venv_reuses_matching_install(self):
        run, calls = recorder((0, ""))
        self.assertEqual(ui_launch.ensure_venv(VENV, run=run), PYTHON)
        self.assertEqual(
            calls,
            [[str(PYTHON), "-c", f"import textual,sys; sys.exit(textual.__version__ != {ui_launch.TEXTUAL_PIN!r})"]],
        )

    def test_ensure_venv_creates_and_installs_pin(self):
        run, calls = recorder((1, ""), (0, ""), (0, ""))
        self.assertEqual(ui_launch.ensure_venv(VENV, run=run), PYTHON)
        self.assertEqual(calls[1], [ui_launch.BASE_PYTHON, "-m", "venv", str(VENV)])
        self.assertEqual(
            calls[2],
            [str(VENV / "bin" / "pip"), "install", "--quiet", f"textual=={ui_launch.TEXTUAL_PIN}"],
        )
        self.assertEqual(len(calls), 3)

    def test_ensure_venv_failure_raises_with_stderr(self):
        run, calls = recorder((1, ""), (0, ""), (1, "no network\nboom"))
        with self.assertRaises(SuperError) as caught:
            ui_launch.ensure_venv(VENV, run=run)
        self.assertIn("pip", str(caught.exception))
        self.assertIn("boom", str(caught.exception))


    def test_ensure_venv_missing_python_creates_venv(self):
        calls = []

        def run(argv, **kwargs):
            calls.append([str(part) for part in argv])
            if len(calls) == 1:
                raise FileNotFoundError(argv[0])
            return SimpleNamespace(returncode=0, stderr="", stdout="")

        self.assertEqual(ui_launch.ensure_venv(VENV, run=run), PYTHON)
        self.assertEqual(len(calls), 3)

    def test_ensure_venv_oserror_on_step_raises_super_error(self):
        def run(argv, **kwargs):
            raise OSError("denied")

        with self.assertRaises(SuperError) as caught:
            ui_launch.ensure_venv(VENV, run=run)
        self.assertIn("venv", str(caught.exception))


class TmuxPlanTest(unittest.TestCase):
    def test_tmux_plan_creates_session_with_board_and_main_windows(self):
        plan = ui_launch.tmux_plan({"PATH": "/p:/q"}, False, DEEZ, Path("/state"))
        self.assertEqual(
            plan,
            [
                ["tmux", "new-session", "-d", "-s", "clanker", "-n", "board",
                 str(DEEZ), "super-clanker", "ui", "--no-tmux", "--state", "/state"],
                ["tmux", "new-window", "-t", "clanker", "-n", "main", "-c", str(Path.home()),
                 "env", "PATH=/p:/q", "sh", "-c", "claude --continue || claude"],
                ["tmux", "select-window", "-t", "clanker:board"],
                ["tmux", "attach", "-t", "clanker"],
            ],
        )

    def test_tmux_plan_attaches_existing_session_with_both_windows(self):
        self.assertEqual(
            ui_launch.tmux_plan({}, True, DEEZ, None, windows=["board", "main"]),
            [["tmux", "select-window", "-t", "clanker:board"], ["tmux", "attach", "-t", "clanker"]],
        )

    def test_tmux_plan_recreates_missing_board_window(self):
        plan = ui_launch.tmux_plan({"PATH": "/p"}, True, DEEZ, Path("/state"), windows=["main"])
        self.assertEqual(
            plan,
            [
                ["tmux", "new-window", "-t", "clanker", "-n", "board",
                 str(DEEZ), "super-clanker", "ui", "--no-tmux", "--state", "/state"],
                ["tmux", "select-window", "-t", "clanker:board"],
                ["tmux", "attach", "-t", "clanker"],
            ],
        )

    def test_tmux_plan_recreates_missing_main_window(self):
        plan = ui_launch.tmux_plan({"PATH": "/p"}, True, DEEZ, None, windows=["board"])
        self.assertEqual(
            plan,
            [
                ["tmux", "new-window", "-t", "clanker", "-n", "main", "-c", str(Path.home()),
                 "env", "PATH=/p", "sh", "-c", "claude --continue || claude"],
                ["tmux", "select-window", "-t", "clanker:board"],
                ["tmux", "attach", "-t", "clanker"],
            ],
        )

    def test_tmux_plan_matches_board_window_by_prefix(self):
        plan = ui_launch.tmux_plan({}, True, DEEZ, None, windows=["board(!2)", "main"])
        self.assertEqual(
            plan,
            [["tmux", "select-window", "-t", "clanker:board(!2)"], ["tmux", "attach", "-t", "clanker"]],
        )

    def test_tmux_plan_recreates_both_when_session_has_other_windows(self):
        plan = ui_launch.tmux_plan({"PATH": "/p"}, True, DEEZ, None, windows=["zsh"])
        self.assertEqual([step[1] for step in plan], ["new-window", "new-window", "select-window", "attach"])

    def test_tmux_plan_empty_inside_tmux(self):
        self.assertEqual(ui_launch.tmux_plan({"TMUX": "x"}, False, DEEZ, None), [])


TMUX = "/opt/homebrew/bin/tmux"


def which_found(name, path=None):
    return TMUX


def which_missing(name, path=None):
    return None


class LaunchTest(unittest.TestCase):
    def test_launch_no_tmux_execs_app_with_pythonpath(self):
        run, calls = recorder((0, ""))
        execs = []
        args = SimpleNamespace(state=Path("/state"), no_tmux=True)
        ui_launch.launch(
            args, {"HOME": "/h", "PYTHONPATH": "/old"}, run=run,
            execve=lambda *a: execs.append(a), deez=DEEZ,
        )
        argv, env = execs[0][1], execs[0][2]
        self.assertEqual(argv[1:], ["-m", "deezlib.superclanker.ui_app", "--state", "/state"])
        self.assertEqual(env["PYTHONPATH"], f"{DEEZ.parents[1]}:/old")
        self.assertEqual(env["HOME"], "/h")

    def test_launch_center_execs_the_command_center_in_the_venv(self):
        run, calls = recorder((0, ""))
        execs = []
        args = SimpleNamespace(state=Path("/state"))
        ui_launch.launch_center(
            args, {"HOME": "/h"}, run=run, execve=lambda *a: execs.append(a), deez=DEEZ,
        )
        argv, env = execs[0][1], execs[0][2]
        self.assertEqual(argv[0], str(ui_launch.VENV / "bin" / "python"))
        self.assertEqual(argv[1:], ["-m", "deezlib.superclanker.center_app", "--state", "/state"])
        self.assertEqual(env["PYTHONPATH"], str(DEEZ.parents[1]))

    def test_launch_default_builds_session_then_execs_attach(self):
        run, calls = recorder((0, ""), (1, ""), (0, ""), (0, ""), (0, ""))
        execs = []
        args = SimpleNamespace(state=None, no_tmux=False)
        ui_launch.launch(
            args, {"PATH": "/usr/bin"}, run=run,
            execve=lambda *a: execs.append(a), deez=DEEZ, which=which_found,
        )
        flat = [call[:2] for call in calls]
        self.assertIn(["tmux", "has-session"], flat)
        self.assertIn(["tmux", "new-session"], flat)
        self.assertIn(["tmux", "new-window"], flat)
        self.assertIn(["tmux", "select-window"], flat)
        self.assertEqual(execs[0][0], TMUX)
        self.assertEqual(execs[0][1], ["tmux", "attach", "-t", "clanker"])

    def test_launch_lists_windows_of_an_existing_session_and_recreates_missing_ones(self):
        calls = []

        def run(argv, **kwargs):
            calls.append([str(part) for part in argv])
            stdout = "main\n" if argv[1] == "list-windows" else ""
            return SimpleNamespace(returncode=0, stderr="", stdout=stdout)

        execs = []
        args = SimpleNamespace(state=None, no_tmux=False)
        ui_launch.launch(
            args, {"PATH": "/usr/bin"}, run=run,
            execve=lambda *a: execs.append(a), deez=DEEZ, which=which_found,
        )
        self.assertIn(
            ["tmux", "list-windows", "-t", "clanker", "-F", "#{window_name}"], calls,
        )
        created = [call for call in calls if call[1] == "new-window"]
        self.assertEqual(len(created), 1)
        self.assertEqual(created[0][created[0].index("-n") + 1], "board")
        self.assertEqual(execs[0][1], ["tmux", "attach", "-t", "clanker"])
        self.assertIn(["tmux", "select-window", "-t", "clanker:board"], calls)

    def test_launch_gives_every_call_the_extended_path(self):
        run, calls = recorder((0, ""), (1, ""), (0, ""), (0, ""), (0, ""))
        execs = []
        args = SimpleNamespace(state=None, no_tmux=False)
        env = {"PATH": "/usr/bin:/opt/homebrew/bin"}
        ui_launch.launch(
            args, env, run=run, execve=lambda *a: execs.append(a),
            deez=DEEZ, which=which_found,
        )
        expected = f"/opt/homebrew/bin:{Path.home()}/.local/bin:/usr/bin"
        self.assertTrue(all(e["PATH"] == expected for e in run.envs))
        self.assertEqual(execs[0][2]["PATH"], expected)

    def test_launch_without_tmux_binary_raises(self):
        run, calls = recorder((0, ""))
        args = SimpleNamespace(state=None, no_tmux=False)
        with self.assertRaises(SuperError) as caught:
            ui_launch.launch(args, {}, run=run, execve=lambda *a: None, deez=DEEZ, which=which_missing)
        self.assertIn("tmux not found", str(caught.exception))

    def test_launch_has_session_oserror_raises_super_error(self):
        probe = recorder((0, ""))[0]
        n = []

        def run(argv, **kwargs):
            n.append(argv)
            if len(n) == 1:
                return probe(argv, **kwargs)
            raise OSError("gone")

        args = SimpleNamespace(state=None, no_tmux=False)
        with self.assertRaises(SuperError):
            ui_launch.launch(args, {}, run=run, execve=lambda *a: None, deez=DEEZ, which=which_found)


class CliTest(unittest.TestCase):
    def test_cli_ui_verb_parses_state_and_no_tmux(self):
        args = cli.build_parser().parse_args(
            ["super-clanker", "ui", "--state", "/tmp/s", "--no-tmux"]
        )
        self.assertEqual(args.verb, "ui")
        self.assertEqual(args.state, Path("/tmp/s"))
        self.assertTrue(args.no_tmux)
        self.assertIn("ui", cli.STORELESS_SUPER_VERBS)

    def test_cli_center_verb_parses_state_and_skips_the_store(self):
        args = cli.build_parser().parse_args(["super-clanker", "center", "--state", "/tmp/s"])
        self.assertEqual(args.verb, "center")
        self.assertEqual(args.state, Path("/tmp/s"))
        self.assertIn("center", cli.STORELESS_SUPER_VERBS)


if __name__ == "__main__":
    unittest.main()

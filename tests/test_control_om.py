import os
import stat
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
CONTROL_OM = (
    REPO / "projects/openmarket-internal/skills/verify-om/bin/control-om"
)


class ControlOmTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.product = self.root / "openmarket-internal"
        (self.product / "packages/cli/src").mkdir(parents=True)
        (self.product / "packages/cli/src/bootstrap.ts").write_text("// fixture\n")
        (self.product / "apps/dashboard/dist/assets").mkdir(parents=True)
        (self.product / "apps/dashboard/dist/assets/app.js").write_text("// fixture\n")
        (self.product / "apps/dashboard/src").mkdir(parents=True)
        self.fake_bin = self.root / "bin"
        self.fake_bin.mkdir()

    def run_control(self, *args):
        return subprocess.run(
            [str(CONTROL_OM), *args],
            capture_output=True,
            text=True,
            env={
                **os.environ,
                "HOME": str(self.root / "home"),
                "OM_REPO_ROOT": str(self.product),
                "OM_LANE_STATE": str(self.root / "state"),
                "OM_LANE_PORT": "18191",
                "PATH": f"{self.fake_bin}:{os.environ['PATH']}",
            },
        )

    def make_compiled_binary(self, executable=True):
        binary = self.product / "packages/cli/dist/om"
        binary.parent.mkdir(parents=True)
        binary.write_text(
            "#!/bin/sh\n"
            'printf "%s\\n" "$@" > "$OM_HOME/compiled-argv"\n'
            "while :; do sleep 1; done\n"
        )
        if executable:
            binary.chmod(binary.stat().st_mode | stat.S_IXUSR)
        return binary

    def write_fake_command(self, name, body):
        command = self.fake_bin / name
        command.write_text(f"#!/bin/sh\n{body}\n")
        command.chmod(0o755)
        return command

    def configure_lane_tools(self):
        self.write_fake_command("nc", "exit 1")
        self.write_fake_command(
            "curl",
            """case \"${*}\" in
  *healthz*) printf '%s\\n' '{\"version\":\"1.2.3\",\"auth\":\"guest\"}' ;;
  *_om-review-health*) printf '%s\\n' 'x-om-chat-review-server: fixture' ;;
esac""",
        )
        self.write_fake_command(
            "agent-browser",
            "[ \"${1:-}\" != --version ] || printf '%s\\n' 'agent-browser 1.0'",
        )

    def test_compiled_up_refuses_a_missing_binary_before_boot(self):
        result = self.run_control("up", "--compiled")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("compiled daemon requested", result.stderr)
        self.assertIn("packages/cli/dist/om is missing", result.stderr)
        self.assertFalse((self.root / "state").exists())

    def test_compiled_up_refuses_a_non_executable_binary_before_boot(self):
        self.make_compiled_binary(executable=False)

        result = self.run_control("up", "--compiled")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("packages/cli/dist/om is not executable", result.stderr)
        self.assertFalse((self.root / "state").exists())

    def test_compiled_up_refuses_a_stale_binary_before_boot(self):
        binary = self.make_compiled_binary()
        binary.touch()
        source = self.product / "packages/cli/src/bootstrap.ts"
        source.touch()
        binary_mtime = binary.stat().st_mtime
        os.utime(source, (binary_mtime + 5, binary_mtime + 5))

        result = self.run_control("up", "--compiled")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("packages/cli/dist/om is stale", result.stderr)
        self.assertFalse((self.root / "state").exists())

    def test_compiled_up_refuses_a_newer_workspace_package_manifest(self):
        binary = self.make_compiled_binary()
        binary_mtime = binary.stat().st_mtime
        manifest = self.product / "packages/contracts/package.json"
        manifest.parent.mkdir(parents=True, exist_ok=True)
        manifest.write_text('{"name":"@openmarket/contracts"}\n')
        os.utime(manifest, (binary_mtime + 5, binary_mtime + 5))

        result = self.run_control("up", "--compiled")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("packages/cli/dist/om is stale", result.stderr)
        self.assertFalse((self.root / "state").exists())

    def test_compiled_up_runs_checkout_binary_and_doctor_reports_provenance(self):
        binary = self.make_compiled_binary()
        binary_mtime = binary.stat().st_mtime
        source = self.product / "packages/cli/src/bootstrap.ts"
        os.utime(source, (binary_mtime - 5, binary_mtime - 5))
        (self.product / "package.json").write_text('{"version":"1.2.3"}\n')
        os.utime(
            self.product / "package.json",
            (binary_mtime - 5, binary_mtime - 5),
        )
        self.configure_lane_tools()

        try:
            up = self.run_control(
                "up", "--compiled", "--env", "OM_FIXTURE_TOKEN=do-not-record"
            )
            self.assertEqual(up.returncode, 0, up.stderr)
            self.assertEqual(up.stdout, "http://127.0.0.1:18191\n")

            home = self.root / "state/home-18191"
            self.assertEqual((home / "compiled-argv").read_text(), "run\n")
            launch = (self.root / "state/lane-18191.launch").read_text()
            self.assertIn("mode=compiled\n", launch)
            self.assertIn(f"executable={binary}\n", launch)
            self.assertNotIn("do-not-record", launch)
            self.assertEqual(
                (self.root / "state/lane-18191.env").read_text(),
                "OM_FIXTURE_TOKEN\n",
            )

            doctor = self.run_control("doctor")
            self.assertEqual(
                doctor.returncode, 0, f"stdout:\n{doctor.stdout}\nstderr:\n{doctor.stderr}"
            )
            self.assertIn(f"lane launch  compiled ({binary})", doctor.stdout)
            self.assertIn("provenance   repo unknown, artifact ", doctor.stdout)
            self.assertNotIn("do-not-record", doctor.stdout)

            binary.write_text(binary.read_text() + "# rebuilt after launch\n")
            changed = self.run_control("doctor")
            self.assertNotEqual(changed.returncode, 0)
            self.assertIn("lane binary  CHANGED", changed.stdout)
        finally:
            self.run_control("down")

    def test_up_stays_on_the_source_daemon_by_default(self):
        self.make_compiled_binary()
        self.configure_lane_tools()
        self.write_fake_command(
            "bun",
            'printf "%s\\n" "$@" > "$OM_HOME/source-argv"\n'
            "while :; do sleep 1; done",
        )

        try:
            up = self.run_control("up")
            self.assertEqual(up.returncode, 0, up.stderr)

            home = self.root / "state/home-18191"
            self.assertEqual(
                (home / "source-argv").read_text(),
                "packages/cli/src/bootstrap.ts\nrun\n",
            )
            launch = (self.root / "state/lane-18191.launch").read_text()
            self.assertIn("mode=source\n", launch)
            self.assertIn("artifact_sha256=source\n", launch)
        finally:
            self.run_control("down")

    def test_up_starts_the_internal_entry_when_the_checkout_has_one(self):
        (self.product / "packages/cli/src/bootstrap.internal.ts").write_text("// fixture\n")
        self.configure_lane_tools()
        self.write_fake_command(
            "bun",
            'printf "%s\\n" "$@" > "$OM_HOME/source-argv"\n'
            "while :; do sleep 1; done",
        )

        try:
            up = self.run_control("up")
            self.assertEqual(up.returncode, 0, up.stderr)

            home = self.root / "state/home-18191"
            self.assertEqual(
                (home / "source-argv").read_text(),
                "packages/cli/src/bootstrap.internal.ts\nrun\n",
            )
            launch = (self.root / "state/lane-18191.launch").read_text()
            self.assertIn("bootstrap.internal.ts", launch)
        finally:
            self.run_control("down")

    def test_om_door_runs_the_internal_entry_when_the_checkout_has_one(self):
        (self.product / "packages/cli/src/bootstrap.internal.ts").write_text("// fixture\n")
        argv_file = self.root / "om-argv"
        self.write_fake_command("bun", f'printf "%s\\n" "$@" > "{argv_file}"')

        result = self.run_control("om", "--", "agent", "--help")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            argv_file.read_text(),
            "packages/cli/src/bootstrap.internal.ts\nagent\n--help\n",
        )

    def test_om_door_runs_the_public_entry_in_a_public_checkout(self):
        argv_file = self.root / "om-argv"
        self.write_fake_command("bun", f'printf "%s\\n" "$@" > "{argv_file}"')

        result = self.run_control("om", "--", "--version")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            argv_file.read_text(), "packages/cli/src/bootstrap.ts\n--version\n"
        )


if __name__ == "__main__":
    unittest.main()

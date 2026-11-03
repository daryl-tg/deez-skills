import os
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
CONTROL = REPO / "projects/kiyotaka-frontend/skills/verify-kiyotaka/bin/control-kiyotaka"
GATEWAY = "tsdb-gateway.example.internal"
TAILNET_IP = "10.1.1.10"


class ControlKiyotakaTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.product = self.root / "kiyotaka-frontend"
        self.product.mkdir()
        (self.product / "package.json").write_text('{\n  "name": "kiyotaka-chart"\n}\n')
        (self.product / ".env.local").write_text(f"VITE_V2_WEB_SOCKET_DOMAIN=wss://{GATEWAY}/ws\n")
        subprocess.run(["git", "init", "-q", str(self.product)], check=True)
        self.fake_bin = self.root / "bin"
        self.fake_bin.mkdir()
        self.argv_log = self.root / "agent-browser-argv"
        self.fake("agent-browser",
                  f'[ "${{1:-}}" = --version ] && {{ echo "agent-browser 1.0"; exit 0; }}\n'
                  f'printf "%s\\n" "$@" > "{self.argv_log}"')
        self.fake("nc", f'case "$*" in *{TAILNET_IP}*) exit 0 ;; *) exit 1 ;; esac')
        self.fake("dig", f'case "$*" in *@100.100.100.100*) echo {TAILNET_IP} ;; esac')

    def fake(self, name, body):
        path = self.fake_bin / name
        path.write_text(f"#!/bin/sh\n{body}\n")
        path.chmod(0o755)

    def run_control(self, *args, extra_env=None):
        env = {
            **os.environ,
            "KIYO_REPO": str(self.product),
            "KIYO_LANE_PORT": "18196",
            "PATH": f"{self.fake_bin}:{os.environ['PATH']}",
        }
        env.pop("KIYO_BROWSER_ARGS", None)
        env.update(extra_env or {})
        return subprocess.run([str(CONTROL), *args], capture_output=True, text=True, env=env, timeout=60)

    def gateway_line(self, result):
        return next(line for line in result.stdout.splitlines() if line.startswith("v2 gateway"))

    def browser_args(self):
        argv = self.argv_log.read_text().splitlines()
        return argv[argv.index("--args") + 1]

    def test_browser_appends_extra_args_to_the_gl_flags(self):
        rule = f"--host-resolver-rules=MAP {GATEWAY} {TAILNET_IP}"
        self.run_control("browser", "open", "about:blank", extra_env={"KIYO_BROWSER_ARGS": rule})
        args = self.browser_args()
        self.assertTrue(args.startswith("--use-angle=swiftshader,"))
        self.assertTrue(args.endswith("," + rule))

    def test_browser_without_extra_args_keeps_the_gl_flags_only(self):
        self.run_control("browser", "open", "about:blank")
        self.assertEqual("--use-angle=swiftshader,--enable-unsafe-swiftshader", self.browser_args())

    def test_doctor_names_the_tailnet_address_and_the_fix_when_the_system_resolver_fails(self):
        line = self.gateway_line(self.run_control("doctor"))
        self.assertIn("system resolver", line)
        self.assertIn(TAILNET_IP, line)
        self.assertIn(f"KIYO_BROWSER_ARGS='--host-resolver-rules=MAP {GATEWAY} {TAILNET_IP}'", line)

    def test_doctor_accepts_a_gateway_the_browser_already_maps(self):
        rule = f"--host-resolver-rules=MAP {GATEWAY} {TAILNET_IP}"
        line = self.gateway_line(self.run_control("doctor", extra_env={"KIYO_BROWSER_ARGS": rule}))
        self.assertIn("reachable", line)
        self.assertNotIn("UNREACHABLE", line)
        self.assertIn(TAILNET_IP, line)

    def test_doctor_still_fails_a_gateway_no_resolver_reaches(self):
        self.fake("dig", "exit 0")
        result = self.run_control("doctor")
        self.assertIn("UNREACHABLE", self.gateway_line(result))
        self.assertNotEqual(0, result.returncode)


if __name__ == "__main__":
    unittest.main()

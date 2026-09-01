import argparse
import os
import sys
import time
from pathlib import Path

from deezlib import __version__, apply, linkplan, registry, runtimes

REPO_ROOT = Path(__file__).resolve().parents[1]


def build_parser():
    parser = argparse.ArgumentParser(prog="deez", description="Central skills hub.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("version", help="Print the deez version.")
    subparsers.add_parser("python-path", help="Print the interpreter running deez.")

    link = subparsers.add_parser("link", help="Link registry entries into runtimes.")
    link.add_argument("--profile", default=None, help="Profile to install.")
    link.add_argument("--runtime", default=None, choices=registry.RUNTIMES)
    link.add_argument("--apply", action="store_true", help="Actually make changes.")

    doctor_parser = subparsers.add_parser("doctor", help="Report drift. Read-only.")
    doctor_parser.add_argument("--profile", default=None)
    return parser


def cmd_version(_args):
    print(f"deez {__version__}")
    return 0


def cmd_python_path(_args):
    print(sys.executable)
    return 0


def cmd_link(args):
    reg = registry.load(REPO_ROOT / "registry.toml")
    profile = args.profile or reg.default_profile
    all_roots = runtimes.roots(os.environ, Path.home())
    roots = {args.runtime: all_roots[args.runtime]} if args.runtime else all_roots
    actions = linkplan.compute(reg, REPO_ROOT, roots, profile)

    pending = [a for a in actions if a.verb != "ok"]
    print(f"profile {profile}: {len(actions)} actions, {len(pending)} pending")
    for act in actions:
        print(f"  {act.verb:14} {act.runtime:6} {act.name:32} {act.reason}")

    if not args.apply:
        print("\nplan only — nothing changed. Re-run with --apply to make it so.")
        return 1 if any(a.verb == "missing-source" for a in actions) else 0

    stamp = time.strftime("%Y%m%d-%H%M%S")
    state_home = Path.home() / ".local" / "state" / "deez-skills"
    for line in apply.execute(actions, state_home, stamp):
        print(line)
    return 0


def cmd_doctor(args):
    from deezlib import doctor

    reg = registry.load(REPO_ROOT / "registry.toml")
    profile = args.profile or reg.default_profile
    roots = runtimes.roots(os.environ, Path.home())

    findings = doctor.check(reg, REPO_ROOT, roots, profile)
    findings.extend(doctor.orphans(roots, reg))

    if not reg.entries:
        print("registry has 0 entries — nothing migrated yet, nothing linked.")

    for finding in findings:
        print(f"{finding.level.upper():5} {finding.code:22} {finding.detail}")

    failures = [f for f in findings if f.level == "fail"]
    warnings = [f for f in findings if f.level == "warn"]
    print(f"\n{len(failures)} failures, {len(warnings)} warnings")
    return 1 if failures else 0


COMMANDS = {
    "version": cmd_version,
    "python-path": cmd_python_path,
    "link": cmd_link,
    "doctor": cmd_doctor,
}


def main(argv):
    args = build_parser().parse_args(argv)
    try:
        return COMMANDS[args.command](args)
    except (registry.RegistryError, apply.ApplyError) as exc:
        print(f"deez: {exc}", file=sys.stderr)
        return 2

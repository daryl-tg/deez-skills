import argparse
import os
import sys
import time
from pathlib import Path

from deezlib import __version__, apply, frontmatter, linkplan, registry, runtimes

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

    index_parser = subparsers.add_parser("index", help="Regenerate the README index.")
    index_parser.add_argument("--check", action="store_true", help="Fail if stale.")

    new_parser = subparsers.add_parser("new", help="Scaffold and register a skill.")
    new_parser.add_argument("name")
    new_parser.add_argument("--category", required=True)
    new_parser.add_argument("--runtimes", default="claude,codex")

    plan_parser = subparsers.add_parser(
        "check-plan", help="Check a multi-phase plan against the skeleton."
    )
    plan_parser.add_argument("path")

    adopt_parser = subparsers.add_parser("adopt", help="Copy a skill into the repo.")
    adopt_parser.add_argument("path")
    adopt_parser.add_argument("--name", default=None)
    adopt_parser.add_argument("--category", required=True)
    adopt_parser.add_argument("--runtimes", default="claude,codex")
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
    findings.extend(doctor.orphans(roots, reg, REPO_ROOT))
    findings.extend(doctor.budget(reg, REPO_ROOT))
    findings.extend(
        doctor.check_skill_references(
            reg, REPO_ROOT,
            extra_known=("explore", "executor", "test-engineer",
                         "code-reviewer", "verifier"),
        )
    )

    if not reg.entries:
        print("registry has 0 entries — nothing migrated yet, nothing linked.")

    for finding in findings:
        print(f"{finding.level.upper():5} {finding.code:22} {finding.detail}")

    failures = [f for f in findings if f.level == "fail"]
    warnings = [f for f in findings if f.level == "warn"]
    infos = [f for f in findings if f.level == "info"]
    print(f"\n{len(failures)} failures, {len(warnings)} warnings, {len(infos)} info")
    return 1 if failures else 0


def cmd_index(args):
    from deezlib import index

    reg = registry.load(REPO_ROOT / "registry.toml")
    readme = REPO_ROOT / "README.md"
    if args.check:
        if index.is_stale(reg, REPO_ROOT, readme):
            print("README is stale — run bin/index", file=sys.stderr)
            return 1
        print("README is current")
        return 0
    changed = index.write(reg, REPO_ROOT, readme)
    print("README regenerated" if changed else "README already current")
    return 0


def _register(name, category, runtimes_csv):
    reg_path = REPO_ROOT / "registry.toml"
    reg = registry.load(reg_path)
    if category not in reg.categories:
        raise registry.RegistryError(
            f"unknown category {category!r}; known: {', '.join(sorted(reg.categories))}"
        )
    runtime_list = [r.strip() for r in runtimes_csv.split(",") if r.strip()]
    for runtime in runtime_list:
        if runtime not in registry.RUNTIMES:
            raise registry.RegistryError(f"unknown runtime {runtime!r}")
    if any(entry.name == name for entry in reg.entries):
        raise registry.RegistryError(f"{name} is already registered")

    rendered = ", ".join(f'"{r}"' for r in runtime_list)
    block = f'\n[skills.{name}]\ncategory = "{category}"\nruntimes = [{rendered}]\n'
    with reg_path.open("a", encoding="utf-8") as handle:
        handle.write(block)
    return registry.load(reg_path)


def _reindex(reg):
    from deezlib import index

    index.write(reg, REPO_ROOT, REPO_ROOT / "README.md")


def cmd_new(args):
    folder = REPO_ROOT / "skills" / args.name
    if folder.exists():
        print(f"deez: {folder} already exists", file=sys.stderr)
        return 2
    reg = _register(args.name, args.category, args.runtimes)
    template = (REPO_ROOT / "templates" / "SKILL.md").read_text(encoding="utf-8")
    title = args.name.replace("-", " ").title()
    folder.mkdir(parents=True)
    (folder / "SKILL.md").write_text(
        template.replace("{{name}}", args.name).replace("{{title}}", title),
        encoding="utf-8",
    )
    _reindex(reg)
    print(f"created skills/{args.name} and registered it")
    return 0


def cmd_adopt(args):
    import shutil

    source = Path(args.path).expanduser().resolve()
    if not (source / "SKILL.md").is_file():
        print(f"deez: {source} has no SKILL.md", file=sys.stderr)
        return 2
    name = args.name or frontmatter.parse(source / "SKILL.md")["name"]
    target = REPO_ROOT / "skills" / name
    if target.exists():
        print(f"deez: {target} already exists", file=sys.stderr)
        return 2
    reg = _register(name, args.category, args.runtimes)
    shutil.copytree(source, target, symlinks=True)
    _reindex(reg)
    print(f"copied {source} -> skills/{name} and registered it")
    print("the original is untouched; linking happens during migration")
    return 0


def cmd_check_plan(args):
    from deezlib import plancheck

    path = Path(args.path).expanduser()
    if not path.is_file():
        print(f"check-plan: no plan at {path}", file=sys.stderr)
        return 2
    text = path.read_text(encoding="utf-8")
    units = plancheck.summary(text)
    for line in units:
        print(line)
    found = plancheck.problems(text)
    print(
        f"{len(units)} unit{'' if len(units) == 1 else 's'}, "
        f"{len(found)} problem{'' if len(found) == 1 else 's'}"
    )
    for problem in found:
        print(f"{path}:{problem.line}: {problem.message}", file=sys.stderr)
    return 1 if found else 0


COMMANDS = {
    "version": cmd_version,
    "python-path": cmd_python_path,
    "link": cmd_link,
    "doctor": cmd_doctor,
    "index": cmd_index,
    "new": cmd_new,
    "adopt": cmd_adopt,
    "check-plan": cmd_check_plan,
}


def main(argv):
    args = build_parser().parse_args(argv)
    try:
        return COMMANDS[args.command](args)
    except (
        registry.RegistryError,
        apply.ApplyError,
        frontmatter.FrontmatterError,
    ) as exc:
        print(f"deez: {exc}", file=sys.stderr)
        return 2

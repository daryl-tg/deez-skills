import argparse
import io
import json
import os
import re
import shlex
import sys
import time
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from deezlib import __version__, apply, featuremaps, frontmatter, linkplan, registry, runtimes

REPO_ROOT = Path(__file__).resolve().parents[1]


def build_parser():
    from deezlib.superclanker.domain import ReportKind

    parser = argparse.ArgumentParser(prog="deez", description="Central skills hub.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("version", help="Print the deez version.")
    subparsers.add_parser("python-path", help="Print the interpreter running deez.")
    skill_path_parser = subparsers.add_parser("skill-path", help="Resolve a registered skill.")
    skill_path_parser.add_argument("name")
    maps_parser = subparsers.add_parser(
        "sync-feature-maps", help="Commit and push only selected project map Markdown."
    )
    maps_parser.add_argument("project")
    maps_parser.add_argument("skill")
    maps_parser.add_argument("files", nargs="+")
    maps_parser.add_argument("--repo", help="Isolated hub worktree to publish from.")

    hook_parser = subparsers.add_parser(
        "clanker-hook", help="Handle a runtime Clanker event from JSON on stdin."
    )
    hook_parser.add_argument("--runtime", required=True, choices=registry.RUNTIMES)
    hooks_parser = subparsers.add_parser(
        "clanker-hooks", help="Install session reminders without changing other hooks."
    )
    hooks_parser.add_argument("--runtime", choices=registry.RUNTIMES)
    hooks_parser.add_argument("--apply", action="store_true")
    checkpoint_parser = subparsers.add_parser(
        "clanker-checkpoint", help="Remember an active session's playbook and resume note."
    )
    checkpoint_parser.add_argument("--runtime", required=True, choices=registry.RUNTIMES)
    checkpoint_parser.add_argument("--session", required=True)
    checkpoint_parser.add_argument("--playbook", required=True)
    checkpoint_parser.add_argument("--resume-note", required=True, type=Path)

    super_parser = subparsers.add_parser("super-clanker", help="Talk to the super-clanker store.")
    super_verbs = super_parser.add_subparsers(dest="verb", required=True)
    ask_parser = super_verbs.add_parser("ask", help="Hand the router a request from this terminal.")
    ask_parser.add_argument("text", nargs="+")
    ask_parser.add_argument("--thread", default="default")
    show_parser = super_verbs.add_parser("show", help="Print one object and its neighbours.")
    show_parser.add_argument("id")
    super_verbs.add_parser("status", help="List tickets and what needs attention.")
    compose_parser = super_verbs.add_parser(
        "compose", help="Gate queued triggers and print the wake prompt."
    )
    compose_parser.add_argument("--dry-run", action="store_true")
    wake_parser = super_verbs.add_parser("wake", help="Wake the router with the queued batch.")
    wake_parser.add_argument("--dry-run", action="store_true")
    dispatch_parser = super_verbs.add_parser("dispatch", help="Accept a trigger as a ticket.")
    dispatch_parser.add_argument("trigger")
    dispatch_parser.add_argument("--slug", required=True)
    dispatch_parser.add_argument("--playbook", required=True)
    dispatch_parser.add_argument("--scope")
    dispatch_parser.add_argument("--rule", action="append", default=[])
    dispatch_parser.add_argument("--repo", type=Path)
    attach_parser = super_verbs.add_parser("attach", help="Route a trigger to an existing ticket.")
    attach_parser.add_argument("trigger")
    attach_parser.add_argument("ticket")
    ignore_parser = super_verbs.add_parser("ignore", help="Decide a trigger needs nothing.")
    ignore_parser.add_argument("trigger")
    ignore_parser.add_argument("--reason", required=True)
    stop_parser = super_verbs.add_parser("stop", help="End a ticket and withdraw its mandate.")
    stop_parser.add_argument("ticket")
    stop_parser.add_argument("--reason", required=True)
    stop_parser.add_argument("--by")
    reply_parser = super_verbs.add_parser("reply", help="Queue a reply on a thread.")
    reply_parser.add_argument("thread")
    reply_parser.add_argument("--text", required=True)
    note_parser = super_verbs.add_parser("note", help="Queue a fact for a ticket's worker.")
    note_parser.add_argument("ticket")
    note_parser.add_argument("--text", required=True)
    super_verbs.add_parser("route", help="Run one decision verb per line of stdin.")
    launch_parser = super_verbs.add_parser("launch", help="Start the worker for an assignment.")
    launch_parser.add_argument("ref", metavar="ticket-or-assignment")
    deliver_parser = super_verbs.add_parser("deliver", help="Resume a worker with its inputs.")
    deliver_parser.add_argument("ref", metavar="ticket-or-assignment")
    super_verbs.add_parser("reap", help="Turn finished worker turns into report triggers.")
    retry_parser = super_verbs.add_parser("retry", help="End a stalled assignment and start a fresh one.")
    retry_parser.add_argument("ticket")
    kill_parser = super_verbs.add_parser("kill", help="Stop a worker process.")
    kill_parser.add_argument("assignment")
    report_parser = super_verbs.add_parser("report", help="Record a worker's own report.")
    report_parser.add_argument("assignment")
    report_parser.add_argument(
        "--kind", required=True,
        choices=[kind.value for kind in ReportKind],
    )
    report_parser.add_argument("--text", required=True)
    report_parser.add_argument("--question")
    report_parser.add_argument("--evidence", action="append")
    super_verbs.add_parser("pass", help="Run one daemon pass and print its line.")
    init_parser = super_verbs.add_parser(
        "init", help="Write a first sources.toml and the example rule in observe mode."
    )
    init_parser.add_argument("--force", action="store_true")
    daemon_parser = super_verbs.add_parser("daemon", help="Run daemon passes until stopped.")
    daemon_parser.add_argument("--interval", type=float, default=5)
    install_parser = super_verbs.add_parser("install", help="Plan or apply the launchd agent.")
    install_parser.add_argument("--apply", action="store_true")
    install_parser.add_argument("--uninstall", action="store_true")
    install_parser.add_argument("--state", type=Path)
    inbox_parser = super_verbs.add_parser("inbox", help="Print replies on a terminal thread.")
    inbox_parser.add_argument("--thread", default="default")
    watchdog_parser = super_verbs.add_parser(
        "watchdog", help="Tick the watchdog when its digest of anomalies is not empty."
    )
    watchdog_parser.add_argument("--digest", action="store_true")
    kick_parser = super_verbs.add_parser("kick", help="Restart the daemon or Watchdog agent.")
    kick_parser.add_argument("agent", nargs="?", default="daemon", choices=["daemon", "watchdog"])
    log_parser = super_verbs.add_parser(
        "log", help="Print the tail of a log: daemon, launchd, watchdog, or an a_, w_ or x_ id."
    )
    log_parser.add_argument("target")
    log_parser.add_argument("--lines", type=int, default=40)
    requeue_parser = super_verbs.add_parser("requeue", help="Put a decided trigger back in the queue.")
    requeue_parser.add_argument("trigger")
    rules_parser = super_verbs.add_parser("rules", help="List the policy rules or print one.")
    rules_parser.add_argument("name", nargs="?")
    policy_parser = super_verbs.add_parser("policy", help="Change a policy rule.")
    policy_verbs = policy_parser.add_subparsers(dest="policy_verb", required=True)
    policy_set_parser = policy_verbs.add_parser("set", help="Set one rule's mode.")
    policy_set_parser.add_argument("rule")
    policy_set_parser.add_argument("--mode", required=True, choices=["off", "observe", "auto"])

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
    new_parser.add_argument("--project", help="Owning repository for a project skill.")

    plan_parser = subparsers.add_parser(
        "check-plan", help="Check a multi-phase plan against the skeleton."
    )
    plan_parser.add_argument("path")

    adopt_parser = subparsers.add_parser("adopt", help="Copy a skill into the repo.")
    adopt_parser.add_argument("path")
    adopt_parser.add_argument("--name", default=None)
    adopt_parser.add_argument("--category", required=True)
    adopt_parser.add_argument("--runtimes", default="claude,codex")
    adopt_parser.add_argument("--project", help="Owning repository for a project skill.")
    return parser


def cmd_version(_args):
    print(f"deez {__version__}")
    return 0


def cmd_python_path(_args):
    print(sys.executable)
    return 0


def cmd_skill_path(args):
    reg = registry.load(REPO_ROOT / "registry.toml")
    entry = next((e for e in reg.entries if e.kind == "skill" and e.name == args.name), None)
    if entry is None:
        raise registry.RegistryError(f"no registered skill named {args.name!r}")
    print((REPO_ROOT / registry.source_dir(entry, entry.runtimes[0])).resolve())
    return 0


def cmd_clanker_hook(args):
    from deezlib import clanker

    try:
        payload = json.load(sys.stdin)
        output = clanker.handle_event(
            REPO_ROOT, args.runtime, payload, clanker.state_root(os.environ, Path.home())
        )
    except (ValueError, OSError, clanker.ClankerError) as exc:
        print(f"clanker reminder unavailable: {exc}", file=sys.stderr)
        return 0
    if output is not None:
        print(json.dumps(output))
    return 0


def cmd_clanker_hooks(args):
    from deezlib import clanker

    roots = runtimes.roots(os.environ, Path.home())
    if args.runtime:
        roots = {args.runtime: roots[args.runtime]}
    try:
        for line in clanker.install(REPO_ROOT, roots, args.apply):
            print(line)
    except (OSError, clanker.ClankerError) as exc:
        print(f"deez: {exc}", file=sys.stderr)
        return 2
    if not args.apply:
        print("Plan only. Use --apply to install the reminders.")
    if "codex" in roots:
        print("Codex skips new hooks until reviewed and trusted in /hooks.")
    return 0


def cmd_clanker_checkpoint(args):
    from deezlib import clanker

    try:
        print(clanker.checkpoint(
            REPO_ROOT, args.runtime, args.session, args.playbook, args.resume_note,
            clanker.state_root(os.environ, Path.home()),
        ))
    except (OSError, clanker.ClankerError) as exc:
        print(f"deez: {exc}", file=sys.stderr)
        return 2
    return 0


def _super_ask(store, args):
    from deezlib.superclanker.sources import terminal

    trigger, receipt = terminal.ask(store, " ".join(args.text), thread_name=args.thread)
    print(f"trigger {trigger.id} {receipt} on thread {trigger.thread_id}")


def _super_field(value):
    if value is None:
        return "-"
    if isinstance(value, (tuple, list, dict)):
        return json.dumps(value)
    return value


def _super_show(store, args):
    shown = store.show(args.id)
    related = shown.pop("related")
    for key, value in shown.items():
        print(f"{key}: {_super_field(value)}")
    print("related:")
    for neighbour_id, summary in related:
        print(f"  {neighbour_id}  {summary}")


def _super_status(store, _args):
    rows = store.status()
    if not rows:
        print("no tickets")
        return
    print("ticket  state  slug  assignment  last-report  attention")
    for row in rows:
        print("  ".join([
            row["ticket"], row["state"], row["slug"], row["assignment"] or "-",
            row["last_report"] or "-", "yes" if row["attention"] else "no",
        ]))


def _super_compose(store, args):
    from deezlib.superclanker import compose, config, gate
    from deezlib.superclanker.domain import Strength
    from deezlib.superclanker.store import SuperError, state_root

    if not args.dry_run:
        raise SuperError("compose only supports --dry-run until unit 3")
    settings = config.load(state_root(os.environ, Path.home()))
    admitted, refused = {}, []
    for trigger in store.queued():
        admission = gate.admit(
            trigger, settings.policy(trigger.source), settings.accept.mode,
            bool(compose.thread_tickets(store, trigger.thread_id)),
        )
        if admission.strength is Strength.not_admitted:
            refused.append(trigger.id)
        else:
            admitted[trigger.id] = (trigger, admission)
    print(f"not admitted: {', '.join(refused) or 'none'}")
    router_batch, fanout = compose.partition([t for t, _a in admitted.values()], store)
    for ticket_id, triggers in fanout.items():
        for trigger in triggers:
            print(f"fanout: {trigger.id} → {ticket_id}")
    print(compose.wake_prompt([admitted[t.id] for t in router_batch], settings, store))


KEBAB = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")


def _super_settings():
    from deezlib.superclanker import config
    from deezlib.superclanker.store import state_root

    root = state_root(os.environ, Path.home())
    return root, config.load(root)


def _super_record(store, kind, prefix, record_id):
    from deezlib.superclanker.store import SuperError

    if not record_id.startswith(prefix):
        raise SuperError(f"{record_id} is not a {kind}")
    return store.show(record_id)


def _super_trigger(store, trigger_id):
    from deezlib.superclanker.domain import Trigger

    shown = _super_record(store, "trigger", "t_", trigger_id)
    shown.pop("related")
    return Trigger(**shown)


def _super_decision_kinds(store, trigger_id):
    related = store.show(trigger_id)["related"]
    return [store.show(i)["kind"] for i, _summary in related if i.startswith("d_")]


def _super_already_decided(trigger_id):
    from deezlib.superclanker.store import SuperError

    return SuperError(f"{trigger_id} is already decided; see deez super-clanker show {trigger_id}")


def _super_playbook(name):
    from deezlib.superclanker.store import SuperError

    playbooks = REPO_ROOT / "skills" / "clanker-mode" / "playbooks"
    given = Path(name)
    if given.is_absolute():
        path = given
    elif given.name == name:
        path = playbooks / (name if name.endswith(".md") else f"{name}.md")
    else:
        path = None
    if path is None or not path.is_file():
        raise SuperError(f"no playbook {name} in {playbooks} and no such absolute file")
    return path.resolve()


def _super_wake(store, args):
    from deezlib.superclanker import compose, router

    root, settings = _super_settings()
    if args.dry_run:
        plan = router.triage(store, settings)
        refused = [trigger.id for trigger, _verdict in plan.refused]
        print(f"not admitted: {', '.join(refused) or 'none'}")
        print(compose.wake_prompt(plan.router_items, settings, store))
        return
    woken = router.wake(store, settings, root, REPO_ROOT)
    if woken is None:
        print("nothing to wake")
        return
    cost = "-" if woken.cost_usd is None else f"{woken.cost_usd:.4f}"
    print(
        f"wake {woken.wake_id} batch {woken.batch} decided {woken.decided} "
        f"denied {woken.denials} cost {cost}"
    )


def _super_dispatch(store, args):
    from deezlib.superclanker import router, rules
    from deezlib.superclanker.config import AcceptMode
    from deezlib.superclanker.domain import DecisionKind, Strength
    from deezlib.superclanker.store import SuperError

    root, settings = _super_settings()
    if not KEBAB.fullmatch(args.slug):
        raise SuperError(f"slug {args.slug!r} is not kebab-case")
    playbook = _super_playbook(args.playbook)
    repo = args.repo and args.repo.expanduser().resolve()
    if repo and not repo.is_dir():
        raise SuperError(f"--repo {args.repo} is not a directory")
    cited = rules.require(root, args.rule)
    trigger = _super_trigger(store, args.trigger)
    if not store.undecided([trigger.id]) and DecisionKind.accept not in _super_decision_kinds(
        store, trigger.id
    ):
        raise _super_already_decided(trigger.id)
    verdict = router.admission(store, settings, trigger)
    if verdict.strength is Strength.not_admitted:
        raise SuperError(f"{trigger.id} is not admitted ({verdict.basis})")
    if verdict.strength is Strength.inferred:
        off = next((rule for rule in cited if rule.mode == AcceptMode.off), None)
        if off:
            raise SuperError(f"rule {off.name} is off")
        auto = any(rule.mode == AcceptMode.auto for rule in cited)
        if not auto and settings.accept.mode == AcceptMode.observe:
            named = ", ".join(args.rule) or "no rule"
            store.ignore(trigger.id, f"would accept: {args.slug} via {named}")
            print(f"would accept {trigger.id} as {args.slug} (observe mode, nothing started)")
            return
    ticket = store.accept(
        trigger.id, args.slug, verdict.strength, args.scope or trigger.thread_id, args.rule,
        settings.accept.policy_version, f"dispatch by router: {verdict.basis}",
    )
    store.add_input(ticket.id, "note", f"playbook: {playbook}")
    if repo:
        store.add_input(ticket.id, "note", f"repo: {repo}")
    print(
        f"accept {trigger.id} → ticket {ticket.id} mandate {verdict.strength} {verdict.basis} "
        f"playbook {playbook}"
    )


def _super_attach(store, args):
    from deezlib.superclanker.store import SuperError

    trigger = _super_trigger(store, args.trigger)
    if _super_decision_kinds(store, trigger.id) and not store.undecided([trigger.id]):
        raise _super_already_decided(trigger.id)
    if trigger.source == "worker" and trigger.meta.get("ticket") == args.ticket:
        raise SuperError(
            f"{trigger.id} is a report from {args.ticket}; reply or note, then ignore it"
        )
    ticket = _super_record(store, "ticket", "k_", args.ticket)
    if ticket["ended_by"] is not None:
        raise SuperError(f"{args.ticket} was stopped by {ticket['ended_by']}")
    store.subscribe(args.ticket, trigger.thread_id)
    store.record_fanout(trigger.id, [args.ticket])
    store.add_input(args.ticket, "trigger", trigger.id)
    print(f"attached {trigger.id} → {args.ticket}")


def _super_ignore(store, args):
    _super_trigger(store, args.trigger)
    if not store.undecided([args.trigger]):
        raise _super_already_decided(args.trigger)
    store.ignore(args.trigger, args.reason)
    print(f"ignored {args.trigger}")


def _super_stop(store, args):
    _super_record(store, "ticket", "k_", args.ticket)
    store.stop(args.ticket, args.by or "router", args.reason)
    print(f"stopped {args.ticket}")


def _super_reply(store, args):
    from deezlib.superclanker.store import SuperError

    _root, settings = _super_settings()
    words = len(args.text.split())
    limit = settings.router.im_reply_words
    if args.thread.startswith("om:") and words > limit:
        raise SuperError(f"reply is {words} words; IM replies stay under {limit}")
    reply = store.reply(args.thread, args.text)
    print(f"reply {reply.id} queued for {args.thread}")


def _super_note(store, args):
    _super_record(store, "ticket", "k_", args.ticket)
    store.add_input(args.ticket, "note", args.text)
    print(f"noted {args.ticket}")


ROUTABLE_VERBS = ("dispatch", "attach", "ignore", "stop", "reply", "note")


def _route_args(parser, line):
    from deezlib.superclanker.store import SuperError

    try:
        words = shlex.split(line)
    except ValueError as exc:
        raise SuperError(str(exc)) from None
    if words[0] not in ROUTABLE_VERBS:
        raise SuperError(f"{words[0]} is not routable")
    complaint = io.StringIO()
    try:
        with redirect_stdout(complaint), redirect_stderr(complaint):
            return parser.parse_args(["super-clanker", *words])
    except SystemExit:
        said = complaint.getvalue().strip().splitlines() or [f"cannot parse {line}"]
        raise SuperError(said[-1]) from None


def _super_route(store, _args):
    from deezlib.superclanker.store import SuperError

    parser = build_parser()
    failed = False
    for number, line in enumerate(sys.stdin.read().splitlines(), start=1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        printed = io.StringIO()
        try:
            args = _route_args(parser, line)
            with redirect_stdout(printed):
                SUPER_VERBS[args.verb](store, args)
        except SuperError as exc:
            failed = True
            print(f"route line {number}: {exc}", file=sys.stderr)
        for said in printed.getvalue().splitlines():
            print(f"{number}: {said}")
    return 2 if failed else 0


def _super_assignment(store, ref):
    if ref.startswith("k_"):
        _super_record(store, "ticket", "k_", ref)
        return store.assignment_for(ref).id
    _super_record(store, "assignment", "a_", ref)
    return ref


def _super_launch(store, args):
    from deezlib.superclanker import workers

    root, settings = _super_settings()
    started = workers.launch(store, settings, _super_assignment(store, args.ref), REPO_ROOT, root)
    print(
        f"launched {started.id} session {started.session_id} pid {started.pid} "
        f"in {started.worktree}"
    )


def _super_deliver(store, args):
    from deezlib.superclanker import workers

    root, settings = _super_settings()
    assignment_id = _super_assignment(store, args.ref)
    count = len(store.undelivered_inputs(store.show(assignment_id)["ticket_id"]))
    resumed = workers.resume(store, settings, assignment_id, REPO_ROOT, root)
    print("nothing to deliver" if resumed is None else f"resumed {resumed.id} with {count} inputs")


def _super_reap(store, _args):
    from deezlib.superclanker import workers

    root, _settings = _super_settings()
    triggers = workers.reap(store, root)
    if not triggers:
        print("nothing to reap")
    for trigger in triggers:
        kind = store.show(trigger.meta["report"])["kind"]
        print(f"report {kind} for {trigger.meta['ticket']} → {trigger.id}")


def _super_retry(store, args):
    _super_record(store, "ticket", "k_", args.ticket)
    fresh = store.retry(args.ticket)
    print(f"retry {args.ticket} → {fresh.id} pending")


def _super_kill(store, args):
    from deezlib.superclanker import workers

    _super_record(store, "assignment", "a_", args.assignment)
    workers.stop(store, args.assignment)
    print(f"stopped {args.assignment}")


def _super_report(store, args):
    from deezlib.superclanker.store import SuperError

    _super_record(store, "assignment", "a_", args.assignment)
    if args.kind == "waiting" and not args.question:
        raise SuperError("a waiting report carries exactly one --question")
    report = store.report(args.assignment, args.kind, args.text, args.question, args.evidence)
    print(f"report {report.id} {report.kind} on {args.assignment}")


def _super_pass(store, _args):
    from deezlib.superclanker import daemon

    root, settings = _super_settings()
    result = daemon.one_pass(store, settings, root, REPO_ROOT)
    for error in result.errors:
        print(f"deez: {error}", file=sys.stderr)
    print(daemon.log_pass(root, result))


def _super_daemon(root, args):
    from deezlib.superclanker import daemon

    return daemon.run(root, REPO_ROOT, interval_seconds=args.interval)


def _super_install(root, args):
    from deezlib.superclanker import launchd

    home = Path.home()
    if args.uninstall:
        lines = launchd.uninstall(home, apply=args.apply)
    else:
        state = args.state.expanduser().absolute() if args.state else root
        lines = launchd.install(REPO_ROOT, state, home, apply=args.apply)
    for line in lines:
        print(line)


def _super_inbox(root, args):
    from deezlib.superclanker import daemon

    inbox = daemon.inbox_path(root, f"terminal:{args.thread}")
    try:
        print(inbox.read_text(encoding="utf-8"), end="")
    except FileNotFoundError:
        print("inbox empty")


def _super_watchdog(store, args):
    from deezlib.superclanker import watchdog

    root, settings = _super_settings()
    if args.digest:
        print(watchdog.digest(store, settings, root) or "clean")
        return
    ticked = watchdog.tick(store, settings, root, REPO_ROOT)
    if ticked is None:
        print("clean, no tick")
        return
    cost = "-" if ticked.cost_usd is None else f"{ticked.cost_usd:.4f}"
    print(f"tick {ticked.tick_id} denied {ticked.denials} cost {cost}")


def _super_kick(_root, args, run=None):
    import subprocess

    from deezlib.superclanker import launchd

    label = launchd.WATCHDOG_LABEL if args.agent == "watchdog" else launchd.LABEL
    argv = ["launchctl", "kickstart", "-k", f"gui/{os.getuid()}/{label}"]
    completed = (run or subprocess.run)(argv, capture_output=True, text=True)
    print(f"{' '.join(argv)} exit {completed.returncode}")
    return completed.returncode


def _tail(text, lines):
    return "\n".join(text.splitlines()[-lines:]) if lines > 0 else ""


def _print_file_tail(path, lines):
    try:
        print(_tail(path.read_text(encoding="utf-8", errors="replace"), lines))
    except FileNotFoundError:
        print(f"(no {path})")


def _turn_result(path):
    raw = path.read_text(encoding="utf-8", errors="replace")
    try:
        outcome = json.loads(raw)
    except json.JSONDecodeError:
        return raw
    result = outcome.get("result") if isinstance(outcome, dict) else None
    return result if isinstance(result, str) else raw


def _super_log(root, args):
    from deezlib.superclanker import workers
    from deezlib.superclanker.store import Store, SuperError

    log_dir = root / "log"
    target, lines = args.target, args.lines
    if target == "daemon":
        _print_file_tail(log_dir / "daemon.log", lines)
    elif target in ("launchd", "watchdog"):
        for name in (f"{target}.err.log", f"{target}.out.log"):
            print(f"== {name}")
            _print_file_tail(log_dir / name, lines)
    elif target.startswith("a_"):
        output = workers._turn_log(log_dir, target, max(workers._turns(log_dir, target) - 1, 0))
        print("== result")
        try:
            print(_tail(_turn_result(output), lines))
        except FileNotFoundError:
            print(f"(no {output})")
        print("== stderr")
        _print_file_tail(output.with_suffix(".err"), lines)
    elif target.startswith(("w_", "x_")):
        store = Store.open(root)
        try:
            print(_tail(store.show(target)["result"] or "", lines))
        finally:
            store.close()
    else:
        raise SuperError(f"log takes daemon, launchd, watchdog, or an a_, w_ or x_ id, not {target}")


def _super_requeue(store, args):
    _super_trigger(store, args.trigger)
    store.requeue(args.trigger)
    print(f"requeued {args.trigger}")


def _super_rules(root, args):
    from deezlib.superclanker import rules

    if args.name is None:
        for rule in rules.load(root).values():
            print(f"{rule.name}  {rule.mode}  {rule.title}")
        return
    (rule,) = rules.require(root, [args.name])
    print(f"# {rule.title}\nmode: {rule.mode}\n\n{rule.text}")


EXAMPLE_RULE = REPO_ROOT / "skills" / "super-clanker" / "references" / "rules" / "silent-repro.md"


def _toml_value(value):
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, tuple):
        return "[" + ", ".join(json.dumps(item) for item in value) + "]"
    return json.dumps(str(value))


def _toml_table(header, record, skip=()):
    from dataclasses import fields

    values = ((field.name, getattr(record, field.name)) for field in fields(record))
    return "\n".join([f"[{header}]", *(
        f"{name} = {_toml_value(value)}" for name, value in values
        if name not in skip and value is not None
    )]) + "\n"


def _super_first_config():
    from deezlib.superclanker import config, sources

    return "\n".join([
        _toml_table("accept", config.AcceptPolicy()),
        _toml_table("router", config.RouterConfig()),
        _toml_table("workers", config.WorkersConfig()),
        _toml_table("watchdog", config.WatchdogConfig()),
        *(
            _toml_table(f"sources.{name}", config.default_policy(name), skip=("name",))
            for name in ("terminal", *sources.POLLERS)
        ),
    ])


def _super_init(root, args):
    from deezlib.superclanker import rules
    from deezlib.superclanker.workers import _write_atomic

    root.mkdir(parents=True, exist_ok=True, mode=0o700)
    os.chmod(root, 0o700)
    for path, text in (
        (root / "sources.toml", _super_first_config()),
        (rules.rules_dir(root) / EXAMPLE_RULE.name, EXAMPLE_RULE.read_text(encoding="utf-8")),
    ):
        if path.exists() and not args.force:
            print(f"kept {path}")
            continue
        _write_atomic(path, text)
        print(f"wrote {path}")


def _super_policy(root, args):
    from deezlib.superclanker import rules

    rule = rules.set_mode(root, args.rule, args.mode)
    print(f"rule {rule.name} mode {rule.mode}")


SUPER_VERBS = {
    "ask": _super_ask,
    "show": _super_show,
    "status": _super_status,
    "compose": _super_compose,
    "wake": _super_wake,
    "dispatch": _super_dispatch,
    "attach": _super_attach,
    "ignore": _super_ignore,
    "stop": _super_stop,
    "reply": _super_reply,
    "note": _super_note,
    "route": _super_route,
    "launch": _super_launch,
    "deliver": _super_deliver,
    "reap": _super_reap,
    "retry": _super_retry,
    "kill": _super_kill,
    "report": _super_report,
    "pass": _super_pass,
    "watchdog": _super_watchdog,
    "requeue": _super_requeue,
}

STORELESS_SUPER_VERBS = {
    "init": _super_init,
    "daemon": _super_daemon,
    "install": _super_install,
    "inbox": _super_inbox,
    "kick": _super_kick,
    "log": _super_log,
    "rules": _super_rules,
    "policy": _super_policy,
}


def cmd_super(args):
    from deezlib.superclanker.store import Store, SuperError, state_root

    try:
        root = state_root(os.environ, Path.home())
        if args.verb in STORELESS_SUPER_VERBS:
            return STORELESS_SUPER_VERBS[args.verb](root, args) or 0
        store = Store.open(root)
        try:
            status = SUPER_VERBS[args.verb](store, args)
        finally:
            store.close()
    except (SuperError, OSError) as exc:
        print(f"deez: {exc}", file=sys.stderr)
        return 2
    return status or 0


def cmd_sync_feature_maps(args):
    import subprocess

    repo = Path(args.repo).expanduser().resolve() if args.repo else REPO_ROOT
    if repo != REPO_ROOT:
        if (REPO_ROOT / ".sync-hold").exists():
            print("feature maps: hub .sync-hold present; skipped")
            return 0
        origins = [subprocess.run(
            ["git", "remote", "get-url", "origin"], cwd=folder,
            capture_output=True, text=True,
        ) for folder in (REPO_ROOT, repo)]
        if any(result.returncode for result in origins) or origins[0].stdout != origins[1].stdout:
            raise featuremaps.FeatureMapError("isolated worktree must use the hub's origin")
    reg = registry.load(repo / "registry.toml")
    print(featuremaps.publish(repo, reg, args.project, args.skill, args.files))
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
        doctor.check_skill_references(reg, REPO_ROOT, extra_known=doctor.ROLES)
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


def _register(name, category, runtimes_csv, project=None):
    registry.skill_source(name, project)
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
    if project is not None:
        block += f'project = "{project}"\n'
    with reg_path.open("a", encoding="utf-8") as handle:
        handle.write(block)
    return registry.load(reg_path)


def _reindex(reg):
    from deezlib import index

    index.write(reg, REPO_ROOT, REPO_ROOT / "README.md")


def cmd_new(args):
    relative = registry.skill_source(args.name, args.project)
    folder = REPO_ROOT / relative
    if folder.exists():
        print(f"deez: {folder} already exists", file=sys.stderr)
        return 2
    reg = _register(args.name, args.category, args.runtimes, args.project)
    template = (REPO_ROOT / "templates" / "SKILL.md").read_text(encoding="utf-8")
    title = args.name.replace("-", " ").title()
    folder.mkdir(parents=True)
    (folder / "SKILL.md").write_text(
        template.replace("{{name}}", args.name).replace("{{title}}", title),
        encoding="utf-8",
    )
    _reindex(reg)
    print(f"created {relative} and registered it")
    return 0


def cmd_adopt(args):
    import shutil

    source = Path(args.path).expanduser().resolve()
    if not (source / "SKILL.md").is_file():
        print(f"deez: {source} has no SKILL.md", file=sys.stderr)
        return 2
    name = args.name or frontmatter.parse(source / "SKILL.md")["name"]
    relative = registry.skill_source(name, args.project)
    target = REPO_ROOT / relative
    if target.exists():
        print(f"deez: {target} already exists", file=sys.stderr)
        return 2
    reg = _register(name, args.category, args.runtimes, args.project)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, target, symlinks=True)
    _reindex(reg)
    print(f"copied {source} -> {relative} and registered it")
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
    "skill-path": cmd_skill_path,
    "sync-feature-maps": cmd_sync_feature_maps,
    "clanker-hook": cmd_clanker_hook,
    "clanker-hooks": cmd_clanker_hooks,
    "clanker-checkpoint": cmd_clanker_checkpoint,
    "super-clanker": cmd_super,
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
        featuremaps.FeatureMapError,
    ) as exc:
        print(f"deez: {exc}", file=sys.stderr)
        return 2

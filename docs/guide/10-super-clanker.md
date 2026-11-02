# 10. super-clanker

`$clanker-mode` makes one session rigorous. It still needs a person to open
that session, paste the context and come back for the result. Work arrives in
the terminal, reviews and OM Chat, and you can follow three to five sessions.
super-clanker takes that job.

It is a local Router above clanker-mode. It listens to events, decides what is
work, and hands each piece to a Worker, a headless clanker-mode lead with its
own worktree and dev-notes folder. Workers never talk to people. The Router
does. Everything runs on the mini.

## Five modules on one store

Every module reads and writes `super.db` through `domain.py` and `store.py`.

| Module | Files | Job |
|---|---|---|
| Gate | `gate.py`, `config.py`, `rules.py` | Admit or refuse each event in Python, before any model runs |
| Router | `router.py`, `compose.py`, `agents/super-router.md` | Wake one resumable session per batch and record its decisions |
| Workers | `workers.py`, `templates/super-worker-*.md` | Launch, resume and reap one `claude -p` per Ticket |
| Daemon | `daemon.py`, `sources/`, `channels.py`, `launchd.py` | Poll, fan out, launch, wake and send replies, every few seconds |
| Watchdog | `watchdog.py`, `agents/super-watchdog.md` | Read a digest of anomalies and repair by cause |

The files are under `deezlib/superclanker/`.

## One request, end to end

```
deez super ask fix the typo in the README of deez-skills
```

1. `ask` stores a Trigger on `terminal:default`.
2. The daemon's next pass gates it. You are a listed sender addressing the
   agent, so it is explicit.
3. The daemon wakes the Router with the Trigger's first 200 characters and a
   `deez super show` pointer.
4. The Router runs `deez super dispatch` with a slug and the `bug-fix`
   playbook. That creates a Ticket, a Mandate and a pending Assignment.
5. The daemon launches the Worker. It writes `brief.md`, `mandate.md` and
   `resume.md` into the Ticket's dev-notes folder and starts `claude -p`.
6. The Worker fixes the typo, verifies it, commits on its own branch and
   reports `ready`. It does not push.
7. The daemon reaps the turn into a Trigger on `worker:<ticket>` and wakes the
   Router.
8. The Router replies on `terminal:default`. The daemon appends the reply to
   your inbox.

```
deez super inbox
```

If the Worker needs you, it reports `waiting` with one question. The answer
you give on the same Thread goes straight back to that Worker.

## The first week

Start in observe mode, which is what `deez super init` writes. Explicit
requests work from day one. Inferred work, such as a defect a teammate mentions
without addressing the agent, only records `would accept` decisions.

Read them. `deez super show <trigger>` on each tells you whether the Router
would have started the right work. When one rule's record holds up, promote
that rule alone:

```
deez super policy set silent-repro --mode auto
```

Leave the rest in observe. Promote the next rule when its own record earns it.

The skill is `skills/super-clanker/`.

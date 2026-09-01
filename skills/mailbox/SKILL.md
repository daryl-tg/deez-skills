---
name: mailbox
description: >-
  Agent mail, handoffs, replies, waits, handled state,
  or store inspection.
compatibility: >-
  Requires `mailbox` on PATH. Source reference:
  /home/operator/sources/kovetskiy/mailbox.
---
## Scope

Use for local command-line mail between agents sharing workspace.

Assume `mailbox` is on PATH. Do not build or run source for normal use. If
binary is missing, report environment issue instead of switching workflows.

Source repo: `/home/operator/sources/kovetskiy/mailbox`. If behavior is
unclear, read in order:

1. `DESIGN.md`
2. `docs/cli.md`
3. `README.md`
4. `docs/development.md`

Not for SMTP, IMAP, POP3, hosted email, or network mail.

## Rules

- Put global flags before subcommand.
- User commands need `-i <identity>` or `MAILBOX_IDENTITY`.
- Admin commands may omit identity.
- Use `thread <id>` for normal thread view; use `admin thread` for audit.
- Default store is nearest git repo `.mailbox`.
- Use `--home <path>` or `MAILBOX_HOME` when store must be explicit.
- Use temp `--home` for tests, demos, destructive experiments.
- Prefer `--format yaml` for machine parsing; text for quick checks.
- Message ids may be full ids or unambiguous prefixes.
- Use `read --raw` for patches, logs, or exact body bytes.
- `read` inspects mail only. `mark` changes read state; use it only when
  closing the loop on that message, normally after a successful reply.
- In pi-team triggered workers, do not use `inbox -w`; runner waits for mail
  or keep-alive ticks between worker rounds.
- In pi-team triggered workers, process one unread message at a time. Do not
  mark a message unless you are replying or just replied to that same id.

## Commands

- Check unread: `mailbox -i alice inbox --unread --limit 20`
- Wait unread: `mailbox -i alice inbox --wait --unread`
- Read, no state change: `mailbox -i alice read 9f4a`
- Mark just-closed inbox message read: `mailbox -i alice mark 9f4a`
- Read exact body only: `mailbox -i alice read 9f4a --raw`
- View thread: `mailbox -i alice thread 9f4a`
- View thread as YAML: `mailbox -i alice --format yaml thread 9f4a`
- Send short note:
  `mailbox -i alice send --to bob -s 'parser status' -b 'Tests pass.'`
- Send stdin text: `git diff | mailbox -i alice send --to bob -s 'patch'`
- Reply sender: `mailbox -i alice reply 9f4a -b 'Looks good.'`
- Reply all, sender plus original direct/list recipients:
  `mailbox -i alice reply-all 9f4a -b 'I pushed a fix.'`
- Override reply subject:
  `mailbox -i alice reply-all 9f4a -s 'new subject' -b 'Retitled.'`
- Inspect sent: `mailbox -i alice sent --limit 20`
- Search visible mail: `mailbox -i alice search --from bob --subject parser`

Pi-team final pass before ending: run `mailbox -i alice inbox --unread`,
process one unread id at a time, reply or reply-all to a handled or deferred
message, then mark that same id. Leave unreplied messages unread.

## Message composition

`send`, `reply`, and `reply-all` share body sources. `reply` and `reply-all`
also accept `-s, --subject` to override automatic `Re:` subject:

```text
-s, --subject <text>  required for send; optional reply subject override
-b, --body <text>     repeatable body block
--file <path>         repeatable body source
--stdin               force stdin body input
```

Body order: body flags, files, stdin. Piped stdin is automatic. `--stdin` may
wait for terminal input; use only when intentional.

Use repeatable `--to` and `--cc`. Direct recipients are identities like `bob`.
List recipients use `@name`, like `@agents`. Lists must exist, except built-in
`@all`; typo fails instead of creating audience.

After list expansion and de-duplication, sender also gets inbox entry marked
read. This keeps both sides visible from `inbox`.

## Listings and read state

`inbox`, `sent`, and `search` list newest first. Sent messages appear in
sender inbox as read rows. Text rows are stable, tab-separated:

```text
short_id  unread_marker  from  to  created_at  subject
```

Unread marker is `*` for unread inbox messages and `-` otherwise. `read` does
not change read state. Do not use `mark <id>` just because you inspected mail.
For pi-team, mark only in the same step as a reply or reply-all for that id;
for direct mailbox work, mark only when closing the loop on that delivered
inbox message. `thread` text output uses same columns with indentation; YAML
output is tree of `message` and `replies` records.

Use YAML for stable fields:

```sh
mailbox -i alice --format yaml inbox --unread
mailbox -i alice --format yaml read 9f4a
```

Errors go to stderr in text and YAML modes.

If `read <id>` fails with invalid id that seems to contain NUL bytes, read-state
file is corrupt. Run `mailbox admin doctor` to confirm. Current mailbox repairs
by marking any delivered inbox message, which rewrites that identity's `read`
index without invalid rows. With older binaries, back up and repair
`.mailbox/identities/<identity>/read` from valid 40-hex inbox ids.

## Mailing lists

Manage list names without `@`; address lists with `@`.

```sh
mailbox -i alice lists create agents --member alice --member bob
mailbox -i alice lists add agents carol
mailbox -i alice lists remove agents bob
mailbox -i alice lists delete agents
mailbox lists show agents
mailbox lists
mailbox -i alice send --to @agents -s 'standup' -b 'blocked on tests'
mailbox -i alice send --to @all -s 'broadcast' -b 'status update'
```

Create, add, remove, and delete require identity for audit. Show/list do not.
Deleted lists cannot receive new mail; old messages keep expansion snapshots.

`@all` is built in and read-only. It expands to every identity already seen as
sender or delivered recipient in selected store. It appears in `mailbox lists`
and `mailbox lists show all`, but is not stored under `lists/`.

## Admin and audit

Use admin commands to inspect selected store, recover context, or debug agent
behavior. For normal thread view, prefer `thread <id>` over `admin thread`.

```sh
mailbox admin messages --limit 50
mailbox admin lists
mailbox admin inspect 9f4a
mailbox admin thread 9f4a
mailbox admin doctor
```

Admin commands do not require identity. Put `--home <path>` before `admin` for
non-default store.

## Source work

For source changes in `/home/operator/sources/kovetskiy/mailbox`, follow repo
`AGENTS.md` and `DESIGN.md`:

- write or update tests before behavior changes;
- keep test stores under `t.TempDir()` or other explicit temp home;
- run `gofmt` on Go changes;
- run `task check` before handoff when tools are available;
- update `README.md`, `docs/cli.md`, `docs/development.md`, or `DESIGN.md`
  when CLI behavior, storage, or workflow changes;
- use reviewer skill on implementation diffs.

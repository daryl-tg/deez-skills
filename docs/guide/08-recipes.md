# 8. Recipes

## Daily

```
$om-mode <what you want>          rigor: classify, route, copy steps in
why is the transcript virtualized this way
teach me how the rooms cache works
unslop                            clean the last thing written
unslop bro                        restate it in plain language
```

## Understanding something

```
why <question>                    git, review threads, tickets, chat, incidents
teach me <subsystem>              built up one diagram at a time
recall <topic>                    rebuild context after a gap
blast-radius                      what else this change could break
```

`why` answers motivation; the explore role answers mechanism; `teach` weaves
both into one account at your pace.

## Before shipping

```
review                            act-on / consider / noted / dismissed
blast-radius                      prove the "that's fine" claims
bin/doctor                        drift, budget, citations, roles
```

## Verification

```bash
control-omchat doctor                          # inner loop, constantly
control-omchat browser snapshot --aria --path artifacts/x/y.aria.txt
control-omchat browser screenshot     --path artifacts/x/y.png
control-omchat evidence publish <run-id> <revision>
```

New repo with no verification story: `create-verification-skill`. Existing map
that has drifted: `maintain-verification-skill`.

## Hub maintenance

```bash
bin/doctor                        before every commit
bin/index                         after any registry change
bin/link                          preview, changes nothing
bin/link --profile lean --apply   install a subset
bin/new / bin/adopt               add a skill
bin/sync                          commit and push
```

## Pitfalls

**Editing a skill mid-task because it is misbehaving.** Fix it in its own
change and keep the task moving. A skill edit tangled into feature work is
invisible to review.

**Assuming a skill is loaded.** Both runtimes read their skill directories at
session start. Restart after installing.

**Handing over an `18097`–`18197` URL.** Not tunnelled. It looks like a working
link and is not.

**Opening the device lane to check progress.** One shot, at the end. A booted
simulator is the scarcest resource on the machine and every extra session
lengthens the queue.

**Trusting a delegate's summary.** Inspect the artifact. Agents report what they
intended, not always what happened.

**Believing an unlinked hub is broken.** `bin/doctor` reports `unlinked` as
info, not failure, until at least one entry resolves into the repo.

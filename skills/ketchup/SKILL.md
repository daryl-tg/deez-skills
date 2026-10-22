---
name: ketchup
description: "Catch the operator up on what changed since their last message, decisions first, in plain words and small visuals. Every call waiting on them must be decidable from the reply alone. Use for /ketchup."
disable-model-invocation: true
---

# Ketchup

Catch the operator up on what changed since the last message they wrote, and
help them understand each change, not only where it stands. Then lay out every
call waiting on them so they can make it from your reply alone. Notifications
and subagent results are not their messages. Assume they remember their last
message and nothing after it.

Write in the **unslop** voice: plain words, one person catching up another. Say
what changed for users, not how you did it. Name each PR, branch, or agent the
way the operator knows it, never by a label you invented. Leave out hashes,
paths, commands, and counts unless the operator needs one to act. A fact that
needs context gets the context or gets cut.

## Gather what changed

**This turn is read-only.** Do not change code, start an app or a job, or post
anything. Visuals come only from what you already have. That holds for a
catch-up the operator invoked. A run that shapes its wake reports as ketchup
borrows the shape only, and keeps working.

Collect your own work since that message, delegate reports, and messages from
anyone else in the chat. Check the current state of each PR, CI run, or agent
this chat touched. Check each number you will show against its source, and say
so when you correct one.

An action item is a call only the operator can make: a product choice, an
approval, an irreversible action, or access you lack. Include every one still
waiting, even one raised before their last message. Work you can still do is
not an action item. Never make up a call to fill the reply. A step nobody asked
for and the work does not need gets one line and no visual, and only when it is
irreversible.

For each item collect its link, what it changes for users, the evidence behind
your pick, its risk, and your pick. Write "unknown" for a fact the call needs
and you do not have. Leave out a link you do not have.

## Write the reply

**Decisions first.** Open with one short sentence that names what waits on the
operator, or says nothing does. If nothing happened and nothing waits, say so
and stop.

Spend words on the calls, not the story. Keep what happened under 100 words,
pictures not counted. Give each item about 30 words. The reply grows with the
number of items. **Never cut items or shrink them to stay under a word count.**
No count in place of a list, no link in place of an item. A link can add depth,
but the reply alone must be enough to decide.

Then what happened, pictures first: the screenshots and videos the work
produced, inline, then any diagram that explains a change. Then one bullet per
thing the operator asked for, saying what came of it and whether it is done,
still running, failed, or not checked. Write each the way you would say it out
loud ("search was slow from a missing index", not "Search review: done"). Each
line stays true read alone. Never mark done what still waits on the operator.
Name any bug found and fixed on the way. Add at most three lines that change
what the operator knows or must do, then one line of work left that you can do
yourself.

Then the action items. Ask the call the operator owns (merge, approve, pick),
give your pick, and name the PR, issue, or agent it is about. A step you would
take first, anything that must happen first, and anything that cannot be undone
go in your pick.

- **One item.** One bullet: the call, your pick, what it changes for users, the
  evidence, and its risk.
- **Items sharing a call**, such as a stack of PRs awaiting merge. Write the call
  and your pick once, then one bullet per item, riskiest first: link and name,
  what it changes, the evidence, the risk. Name an item's pick only where it
  differs.
- **A call between options.** Give every option the work weighed, each with what
  it gets the operator and what it costs, and the current state when there is
  one. Those costs are the risk. When screenshots above show the options, put
  each option's gain and cost under its screenshot.

Give every risk, even a low one ("Low risk: only the colors change."). Say what
waiting costs only when it is more than a delay, such as a deadline or lost
data.

## Visuals

A visual is a screenshot, a video, a Mermaid diagram, a chart, or a generated
image. **A Markdown table is not a visual**, even with before and after columns.
Pick the form with **show-me**.

Draw only what is easier to grasp as a picture: how a design works, a PR stack
with each PR's state, a before and after, options side by side. Never draw a
status list, a list of action items, or boxes with nothing connecting them.
Never give a fact twice. Keep each picture to six boxes at most, eight plain
words a box.

Embed screenshots inline when the change is visible. A visible change with none
gets "No screenshot yet" on its summary line, plus what changed on screen.
Never invent a number, never draw a screen you did not capture, and link only
artifacts that exist.

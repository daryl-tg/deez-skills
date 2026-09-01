# 9. Keeping verification honest

A feature map rots the moment the app changes. This chapter is when to run the
maintenance pass, and why "daily" is the wrong default.

## Why not daily

`maintain-verification-skill` is not a lint. One pass does:

1. **A source wave** — one read-only subagent per feature file, in parallel.
2. **A live pass** — a real session that **drives every mapped feature**, not
   only the ones that changed.
3. **Triage and a PR** of proven corrections.

The live pass is the cost. For OM Mobile it takes the permanent simulator lane,
which is the scarcest resource on the machine and queues other work behind it.
Running that nightly against a repository nobody touched that day spends the
lane, spends tokens, and reports `clean` — which teaches you to stop reading the
output. **A check you have learned to ignore is worse than no check.**

The pass is expensive because it is thorough. Make it earn the cost by running
it when something might actually have drifted.

## What to run, and when

| Cadence | What | Cost |
|---|---|---|
| **Continuously, inside your work** | `control-<app> doctor` and the inner-loop recipe replay | Near zero |
| **Per feature** | The terminal gate for the surface you touched | One session |
| **On a drift signal** | `maintain-verification-skill` on that repo | A full pass |
| **Backstop** | `maintain-verification-skill`, every few weeks per repo | A full pass |

The daily thing already exists and you are already doing it: `control-<app>
doctor` runs constantly during implementation. That is your continuous check.

## The four drift signals

Run the full pass when one of these happens. Each means the map may now be
lying, and a lying map is worse than none because it produces confident wrong
verification.

**1. A drive failed for a reason that turned out to be the map.** The recipe
said click a control that has been renamed. That is drift, and where one entry
drifted others probably did too.

**2. A feature landed that changed a mapped surface.** A new entry point, a
renamed control, a moved route. The feature's own terminal gate proves the new
behavior; it does not prove the other eleven feature files still describe
reality.

**3. A user-facing surface exists that the map has never heard of.** Usually
noticed when you go to verify something and there is no recipe for it.

**4. Before a release**, or before anything you want to be able to claim was
verified.

## The backstop

Every few weeks per repository, regardless of signals. Not because something
broke, but because the absence of signals is not evidence — a map can drift
quietly when nobody happened to drive the affected feature.

Fortnightly per repo is a reasonable starting point. Adjust from what the passes
actually find: if three in a row come back `clean`, stretch the interval. If one
returns a page of corrections, the interval was already too long.

## Reading the outcome

Every pass ends in exactly one verdict, and it says which:

- **clean** — every feature got source and live coverage, nothing worth
  shipping. No branch, no PR.
- **changed** — one PR of proven corrections.
- **blocked** — coverage could not finish, or a proven fix could not ship
  safely. It says exactly what blocked it.

**`blocked` is not a soft `clean`.** It means part of the app was not verified,
so treat it as an open item rather than a run that mostly worked.

Two rules the pass holds that are worth knowing as the reader of its output:

- **It never edits product code.** Behavior the map describes that the app no
  longer does is either doc drift, which it fixes, or a product regression,
  which it reports and leaves alone. It will not paper over a regression in
  docs.
- **A feature it could not reach is `verified-unreachable`**, with the concrete
  unmet prerequisite and the route it tried. If the map omitted that
  prerequisite, that itself is drift.

## Automating it

You can schedule it. Before you do, be honest about which failure you are
protecting against: forgetting to run it, or not noticing drift. Scheduling
fixes the first and can make the second worse, because a `clean` result arriving
on a timer stops being read.

If you do schedule it:

- **Per repository, staggered.** Never all three on the same night; they compete
  for the simulator lane and the review renderer.
- **Off-hours**, since the live pass takes the lane.
- **Surface `changed` and `blocked` loudly, and `clean` quietly.** The whole
  value is in the exceptions.
- **Start manual for a month.** Watch what the passes actually find, then pick
  an interval from evidence rather than from a guess. If nothing was learned in
  a month of manual passes, automating them will not help.

My recommendation: run it on the four signals, keep a fortnightly backstop in
your own head or your task tracker, and leave it unautomated until you have a
month of real results to tune against.

## When there is no map yet

`maintain-verification-skill` stops and points at `create-verification-skill`
rather than inventing a target. See [chapter 0, step 3](./00-first-run.md).

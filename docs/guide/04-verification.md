# 4. Verification

Two lanes, run at different frequencies. Confusing them is the common failure.

| | Inner loop | Terminal gate |
|---|---|---|
| What | Replay the feature-map recipe | Explore the feature as a user would |
| Driven by | `control-<app>`, scripted | An agent, improvising |
| How often | After every meaningful edit | Once per feature |
| Signal | Deterministic pass or fail | Judgement, plus what the script missed |
| Cost | Near zero | Tokens and wall-clock |
| Output | Green or red | Artifact pair and a published URL |

The failure this prevents: exploring expensively after every small edit,
producing evidence nobody reads, then skipping the real sweep at the end because
it already feels done.

**The terminal gate replays every scripted recipe first, then explores.**
Exploration that skips the known cases misses regressions the script catches in
a second.

## `control-<app>`

A thin per-repo wrapper, committed to the repo it drives so it versions with the
app. Four verbs:

```bash
control-omchat doctor                        # is this instance worth driving?
control-omchat browser click --role button --name "Send"
control-omchat cli -- om room list --json
control-omchat evidence publish <run> <rev>
```

`doctor` is the one that earns its keep. "Is the local daemon actually serving
my working tree?" has silently wasted verification runs, and nothing else
answers it in one command.

`browser` delegates to `agent-browser` rather than reimplementing it. Building a
second browser stack to keep the binaries separate would cost maintenance and
buy nothing.

## What counts as proof

A **pair**, always: an accessibility snapshot and a screenshot. The snapshot is
diffable and survives a restyle; the screenshot is what a person reads. Neither
works alone — you cannot assert on a screenshot, and an accessibility tree
cannot show that the spacing is wrong.

Then publish through the review renderer and hand back the URL. Never author a
revision file by hand, and never hand over an `18097`–`18197` URL: those are not
tunnelled, so they look like working links and are not.

## The feature map

`skills/verify-<app>/features/` — one file per user-facing feature, four fixed
sections: sub-features, how a user reaches it, how to drive it, gotchas.

This is the durable part. It is the repo's maintained verification source, and
`maintain-verification-skill` is the pass that keeps it honest: parallel readers
per feature from source, then one live session exercising every feature, then at
most one PR of proven corrections.

A map that has drifted from the app is worse than no map, because it produces
confident wrong verification.

Next: [Delivery](./05-delivery.md).

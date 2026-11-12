# Morning desk: a default-on brief of what mattered overnight

*Coverage levels verified 2026-11-12 on branch `daryl/desk-brief-coverage` (PR #2468, unmerged, head `398c3ca7eb`), two bare-lane runs with a stub Telegram server and a fake model that writes the brief from the `desk_brief` result. With 48 seeded watches, 12 pairs of them sharing a link: the model was handed 3, 5 and 8 items at normal (nothing stored), 5, 10 and 15 at high, 3, 0 and 5 at low; each shared story appeared once with `in_watches` 2; named plus unlisted came to 48 at every level; the three Telegram bodies held the layout; plain `om chat` showed the normal and high briefs whole while an ordinary watch's 1,013-character answer was still cut at 600; `om watch brief` printed `Lead:` and `Notable:` label rows; `/desk coverage` changed the level with no model request. Evidence: `http://127.0.0.1:8098/om-desk-coverage-20261112/r2/` (20 frames, approved by the operator). Rig and captures: `~/dev-notes-artifacts/om-desk-brief-coverage/run-artifacts/verify-r2/`. Pending proof: the 120, 220 and 380 word budgets (the lane's model is scripted), the Slack plain message `desk coverage <level>`, a brief longer than 2,048 characters in `om chat`.*

*On main since 2026-11-11: PR #2467, squash-merged as `cdfcf43d5e`. Re-driven 2026-11-11 at the merged change's own head `6eb18a1396` on one bare lane (lane 18173, scripted fake model, stub Telegram server): the desk seeds with no install command; a home seeded after 08:00 sends nothing for 3 min 10 s; exactly one brief arrives at the next slot in the layout below; `/desk off` in plain `om chat` silences a slot and `/desk on` brings the next one back; a timer check from #2463 that held leads `om watch brief` while a plain tick stays out. Captures: `~/dev-notes-artifacts/om-morning-desk-ritual/run-artifacts/verify-r5/`. Nothing was published for that run.*

*Verified 2026-11-11 on branch `daryl/morning-desk` before the merge, four lane runs on bare lanes (dummy `OM_API_KEY`, dead service URLs, scripted fake model through `OPENMARKET_LLM_*`, a stub Telegram server through `OM_TELEGRAM_BASE_URL`). Evidence: `http://127.0.0.1:8098/om-morning-desk-20261111/r4/` (21 frames, approved by the operator; r1 to r3 hold the earlier rounds). Rig and captures: `~/dev-notes-artifacts/om-morning-desk-ritual/run-artifacts/verify-r4/` (`rig/`, `cli/`, `tui/`), with the fuller rig in `verify-r3/rig/`. The lane homes were deleted after the merge.*

*Driven and passing: default-on seeding; no brief at seed time and exactly one at the next slot; the whole brief in the home chat with the turn-off row; day 31 without it; the layout in Telegram and in plain `om chat`; `om notis` text and JSON; `/desk`, `/desk off`, `/desk on` in the TUI; an off that sticks before and after a desk exists; a refused `/desk on`; removal and return under a new id; a person's own `morning-desk` watch left byte-identical; the read-exactly-once window; the owner's voice in the user row; `watch brief`; the quiet night; the hand install with the network dead; the "Full" expansion through the web chat door; the What's new card.*

*Pending proof: the Slack plain-message form (`desk off`), which has unit proof only because the inbound Slack channel cannot be pointed at a stub; `/desk` typed by a Telegram user, because the inbound Telegram bot ignores `OM_TELEGRAM_BASE_URL`; the brief's wording from the home's own model; a Discord home; a real 08:00 slot (every run moved the slot near with `watch edit`).*

Once a home channel (Telegram, Discord or Slack) and a model exist, the daemon installs the built-in pack `@om-core/morning-desk` and starts it with no card. Each morning its one ai step calls `desk_brief`, a ranked read across every watch, and sends a short brief to the home channel in the owner's voice. For its first 30 days the delivered message ends with a daemon-written turn-off row.

## Sub-features

- `seed`: at boot and on the `agent-channels` and `llm-lanes` pokes the seeder installs and starts the desk once per home. The log line is `[morning-desk] on, first brief 08:00 <zone> to <channel>`. A home with a model and no channel gets no desk.
- `first-slot`: nothing is sent at seed time. The first brief is the next slot.
- `brief`: one `sendMessage` per slot. Title line, one blank line, a greeting word, up to three blocks with bold subjects, an `also:` line, a `today:` line when the calendar has something, a bold `next:` line. `parse_mode` is `HTML`.
- `turn-off-row`: `Turn off: /desk off` after one blank line, for 30 days from `desk.brief.first_sent_at`. On Slack it reads `Turn off: reply desk off`. The stored answer never carries it.
- `desk-command`: `/desk` prints `Morning desk: on`, `Sends: 08:00 <zone> to <channel>` and the turn-off row, with no model turn. `/desk off` answers `Morning desk off. /desk on brings it back.` `/desk on` answers `Morning desk on.`
- `off-sticks`: `/desk off` writes `desk.brief.off`. The seeder does nothing while it is set, and a refused `/desk on` leaves it set.
- `refused-on`: a desk whose definition nobody consented to answers `Morning desk not started: it changed since its last OK.` and `Start: om watch arm <slug>`.
- `waiting`: a watch that is on with its step not running reads `Morning desk: waiting`.
- `removal`: a removed desk is not recreated. `/desk on` brings back a running desk under a new id (`morning-desk-2`).
- `coverage` (PR #2468): `/desk coverage low|normal|high` writes `desk.brief.coverage` and answers `Morning desk coverage: <level>.` with no model turn; `/desk coverage` alone names the level and the choices; `/desk` shows a `Coverage:` row; nothing stored reads as `normal`. Slack takes the plain message.
- `tiers` (PR #2468): the read returns `lead`, `notable` and `also` by level (low 3/0/5, normal 3/5/8, high 5/10/15) with `coverage: { level, words }`; `om watch brief --coverage <level>` previews one. The brief tells leads in blocks, notable items in consecutive one-line rows, and names the rest.
- `feed-whole` (PR #2468): a step answer from a watch whose `notify.style` is `full` shows whole in plain `om chat`; any other watch's answer is cut at 600 characters with `(cut)`.
- `timer-check`: a timer check that held (#2463) ranks as a fire, titled by its sentence, for example `steps 8,412, below 10,000`. A plain tick never does.
- `read`: `om watch brief [--since] [--until] [--format json]` prints at most 3 lead and 5 more items, `Unlisted`, `Quiet`, today's calendar and next steps. JSON adds `zone`, `truncated`, `in_watches`, `sources`.
- `window`: on a clock-fired step the daemon binds the read to the rows committed since the step's previous run. A row committed after one run's read lands in the next run and in no other.
- `voice`: `voice: "owner"` on a text ai step puts the stored persona in the opening user row under an `owner_voice` fence. The system text is unchanged. The arm card prints `Voice: yours`.
- `tui-feed`: plain `om chat` draws a multi-line step answer with its line breaks, bold subjects and one blank row under the header. A markdown link shows as `label (url)`.
- `notis`: `om notis --watch <desk>` prints the brief's one-line summary under the desk's row. JSON `outputs[].text` is the same line.
- `hand-install`: `om install @om-core/morning-desk` works with the network dead and lands the watch paused. A local folder of the same name is ignored.
- `news-brief-row`: with a news brief schedule on, `/desk` adds `News brief: also on. Stop it: om news brief --schedule off`.

## How to get to it (user POV)

- Pair a home chat and connect a model. The desk appears by itself, and the first brief arrives at the next 08:00 in the home's zone.
- Type `/desk` in the home chat or in `om chat`.

## Driving it with control-om

Preconditions:

- A bare lane with the fake model on both the lane and every CLI call that arms.
- **The inbound Telegram bot must never start.** It ignores `OM_TELEGRAM_BASE_URL` (`packages/cli/src/agent/channels/telegram.ts`, the bot built near 403) and would call the real Telegram API. Pair with `om setup telegram --enable-chat` against the stub, then delete `agent.telegram_chat_enabled` from the lane's settings before boot. Confirm the lane log says `agent chat is off` and the stub saw no `getUpdates`.
- Nothing may connect to Slack. The inbound Slack channel has no base URL override (`packages/cli/src/agent/channels/slack.ts` near 501).
- The fake model answers the brief step by calling `desk_brief` with no arguments, then replying in the shipped layout. It logs every request.

Recipe (scripts in `verify-r3/rig/` and `verify-r4/rig/`):

1. `source env.sh`, then `stubs-up.sh main` for the fake model and the Telegram stub.
2. Pair the home as in `cli/A-00` and `A-01`, then `lane_up`. Expect the seed log line and `om watch show morning-desk` reading its steps working.
3. Move the slot near with the product's own door: `om watch edit morning-desk --source 'every:*/2 * * * *'`. That edit re-arms the chain under the owner's consent, so the desk keeps running.
4. Read the stub's request log for each `sendMessage` body. Read the fake model's log for the system text, the user message and the tools advertised.
5. Day 31: set `desk.brief.first_sent_at` 31 days back in the lane's settings and capture the next brief.
6. Late commit: `late-commit.py insert`, let a slot pass, `late-commit.py commit`, and check which run's `desk_brief` result holds the row.
7. TUI: `tui.sh` inside tmux for `/desk`, `/desk off`, `/desk on`, the feed row and the What's new card.
8. Quiet night: an empty window with nothing on the calendar, and a fake model that answers `NO_REPLY`. Expect no send.
9. Coverage: seed at least 32 nameable watches (48 with 12 link-sharing pairs exercises the fold; `om event push --url <same link>` on two watches makes a pair). `/desk coverage high` in the TUI, then read the tier counts in the `desk_brief` result the fake model logged. The fake model must build its reply from that result, or the message will not reflect the level.
10. `render-all.sh`, then `ARTIFACTS=<publish dir> control-om evidence publish <run-id> <revision>`.

## What to expect

- Slot to `sendMessage` took 46 to 74 ms over nine two-minute slots with an instant fake model. That measures the scheduler and delivery, not a model.
- A daily slot is staggered by up to five minutes per home (`packages/cli/src/runner/timers/stagger.ts`). A brief due at 08:00 was sent 139.7 s and 257 s later on two homes.
- `om watch brief` on a snapshot of a 987 MB home answered in 1.8 s.

## Gotchas

- `om watch run now` refuses a timer. Move the slot with `watch edit` instead.
- A desk brought back after removal reads the previous 24 hours on its first run and can repeat what the removed desk sent.
- `om notis` labels a silent run `saved` with the line `Errand fired on an event-watch match.`
- The 200-character notice summary can cut a link off.
- `om setup webhook` refuses a receiver that answers 404 on its test POST.
- `om install` without a TTY exits `confirmation_required` and leaves its package lock for five minutes. Not caused by this feature.
- A step answer is stored cut at 2,048 characters, so `om chat` shows a full-style brief whole only up to that.
- An ordinary ai step with the default tools is offered `desk_brief` too. A fake model that answers every step with a brief will answer that one with a brief.
- Under load an inbound push can answer 500 with `SQLITE_BUSY` (2 of 175, then 1 of 147). Re-push it.
- An existing Slack install needs its manifest re-applied before `/om-desk` reaches the handler.
- `watch import` wants the stored-spec shape (`instruction: { user_goal }`); a create-shaped spec is refused `invalid_spec`.
- A timer check with `on_missing: "tell"` sends its `check has no reading` warning to the channel even on a watch imported with `notify.enabled` false. Seen 2026-11-11; it belongs to #2463, not the desk.

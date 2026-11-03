# Persona auto-learning and loading into the card

*Verified: 2026-11-03. Branch `daryl/persona-auto-learn` (PR #2275, merged as `ffce9accc`, in v0.489.0). Last driven tree `2d240ff0e` before rebase; the PR head was `cfd976391`. The live rows below predate the digest budget (#2279, `abc1e6bc9`), so the `first 8` rows they quote are the old output.*

*Setup:*
- *a test account, never the operator's: `@dboon_ref`, signed in with `om login --headless-json` on a scratch `OM_HOME`;*
- *the daemon from source on 127.0.0.1:18174 with `OM_LIBRARY_DIR` set (without it a non-default home runs no library mirror, and the fold cannot load the card);*
- *no model provider.*

*What happened:*
- *`om persona set` with 10 lines printed `Room drafts: first 8 of 10 lines`.*
- *About 5 minutes after boot, once the mirror finished its first pass, the daemon folded the text into a new `Persona/dboon-ref.md` at r1 holding all 10 voice rules. It loaded the card, set `rooms.persona_source` to `library:<doc>`, and advanced the trusted head (`agent.persona_learning.auto_head.<sha>` at r1). Retries answered `unchanged`.*
- *`om persona set --source acme-voice` with 2 lines folded as a union: 10 own lines then 2 acme lines. `show` printed `From: acme-voice` and `Room drafts: first 8 of 12 lines`.*
- *A second acme write replaced only `acme rule one` with `acme rule one v2`.*
- *`om persona clear --if-source acme-voice` printed `om: persona cleared, lines from acme-voice removed from your card.` and left the 10 own lines.*

*Not driven:*
- *a learn pass, since the test account has no model;*
- *undo and decline memory;*
- *the first card created from posts;*
- *the length refusal;*
- *the moved-head rebase.*

*The last four are unit- and integration-tested. The guest home showed the `show` rows; the account home showed everything else.*

*Evidence: `~/dev-notes-artifacts/om-persona-auto-learn/run-artifacts/live-*.txt` (text captures; nothing was published to 8098).*

Learning updates your persona as you post, with no approval step. Any persona you load joins the learned card instead of switching learning off. `agent.persona_learning off` is the one switch.

## Sub-features

- **Learning applies itself.** Every learned change publishes to the loaded HOME card through the automatic proposal CAS: all scopes, forced runs (`om persona learn --now`) and hand-edited cards. Pending learner proposals left by an older daemon close as superseded. Code: `runner/rooms/persona-learn.ts` (`applyAutomaticPersonaCandidate`, `supersedeLearnedProposals`).
- **First card.** It is created at 30 own posts and loaded with `runPersonaUse`, unless the default voice was chosen or a hand-set or tool persona is stored.
- **Undo.** A history restore or hand edit that drops learned lines records them as 90-day declines (`recordUndoneLearning`). Learning keeps running.
- **Length.** A card whose digest passes 4000 characters is refused when learned, with outcome `refused_too_long`.
- **Fold.** `persona_set`, `om persona set`, `om persona infer --yes` and `om config set rooms.persona` apply at once. At the next library-persona sync the text becomes the card's newest revision (`runner/rooms/persona-fold.ts`). Hand-set text replaces the card. Notes read `Persona set by hand` or `Persona from <tool>`.
- **Tool merge.** Labelled text merges voice rules by rule text (`mergeToolRules` in `runner/rooms/persona-merge.ts`):
  - the first write adds;
  - a later write swaps only the tool's changed lines;
  - `clear --if-source` removes exactly them, noted `Persona from <tool> removed`;
  - the label's last text is stored at `agent.persona_source_base.<sha>`.
- **Moved head.** A learned update whose card moved mid-pass rebases onto it; the head wins a conflict.
- **Show.**
  - `om persona show` names the card (`Your persona (card: Persona/<slug>.md)`) and has rows `Learning: on, updates apply as you post (om config set agent.persona_learning off)`, `Updated: <age> ago, from N of your messages`, `From: <tool>` and `Room drafts: first N of M lines` only when the digest leaves lines out.
  - `persona_show` and `--json` keep `card: boolean` and add `learning`.

## Recipe

1. **Sign in a scratch home on a test account.** Run `OM_HOME=<scratch> OM_BIND=127.0.0.1:<agent port> bun packages/cli/src/bootstrap.ts login --headless-json` in the background, then hand the operator the `verificationUri`. Never use the operator's own home: a fold writes their real `Persona/<handle>.md`.
2. **Set the persona before the daemon boots:** `persona set "<lines>"`, or `--source <tool>`.
3. **Boot the daemon:** `OM_LIBRARY_DIR=<scratch lib> … run`. Wait for the `[library-mirror]` first pass, then `[library-persona] persona text added …`, or read the card under `<scratch lib>/home/Persona/`.
4. **Check the settings and show.** Read `rooms.persona_source` and `agent.library_persona_doc` in `accounts/<handle>/om.sqlite`, then run `persona show`.
5. **Refold.** For a second write, set it while the daemon runs; the next 5-minute sync folds it. `POST /api/library/persona/sync` syncs but never folds.
6. **Tear down.** Kill the daemon by pid and delete the scratch home and library.

## Gotchas

- **"HOME library mirror directory is not available" for the first minutes.** The fold needs the mirror health row, written after the mirror's first full pass. On a non-default home with no `OM_LIBRARY_DIR` the mirror never runs.
- **Room drafts and the MCP voice carry voice rules past 8 only while the digest has free room** (#2279, after v0.489.0). Rules 9 and on join whole, in card order, until the 3000-unit budget; identity is never shortened for them, and a digest that needed trimming gets none. Pinned by `persona-digest-parity.test.ts` against selfmd `af0ac00`. *Pending live proof: source and tests only; a 10-line persona should show no `Room drafts` row.*
- **MCP clients get the voice only with `om config set mcp.operator_voice on`** (off by default). `/rooms` drafts use the persona with no switch. `session_grants` reports `operatorVoice: on|off`.
- **A folded card carries the template's six `Never do` rules.**

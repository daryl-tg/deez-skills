# Chat TUI icon modes (`chat.icons`)

*Re-driven 2026-11-02 (scheduled maintenance), tree `587ce2d0b` (origin/main, v0.480.3), lane on 18168 (`OM_FEED_ALLOW_LOOPBACK=1`, `OM_FEED_POLL_INTERVAL_MS=60000`), host load average about 5. First drive on main. Fake model on 18170 (the chat-workspace-tui `server.ts`), private tmux server, plain `om chat` with `OM_TUI_ICONS=` empty: the card read **Nerd Font icons** / **Watch and source icons as Nerd Font glyphs.** / `[ Turn it on ]`; `/watches` drew its header glyph as U+1F440; Esc, ctrl+x then `w` stored `chat.icons = nerd` (`config get` `source: config`); the next `/watches` in the same session drew U+F0208. `config set chat.icons maybe` exits 2 (`must be one of: emoji, nerd, ascii`); restored with `config set chat.icons emoji`. Not driven: `ascii`, the `OM_TUI_ICONS` override, per-row source glyphs.*

*Verified: 2026-11-02, branch `daryl/tui-nerd-icons` at `2be28d04d` (PR #2247, off origin/main `5cf89fe95`). Source CLI on lane 18131 with a fake model on 18132, in a herdr pane, with no `OM_TUI_ICONS` set. Plain `om chat` showed the What's new card `Nerd Font icons` with `[ Turn it on ]`. ctrl+x listed `w What's new: turn it on`. `w` stored `chat.icons = nerd` (`stored as tui.icons`) and closed the card. `/watches` in the same session drew the title eye as U+F0208, and the inbound, filings and X rows as U+F01C, U+F19C and U+F099. Before the press the same rows were 👀 📥 📄 🐦. On main since `587ce2d0b` (#2247). Not driven: `ascii` mode, `OM_TUI_ICONS` outranking a stored value, the page tabs' source icons.*

`om chat` draws the watch and source icons on `/watches` and its pages in one of three modes: `emoji` (the default), `nerd` (Nerd Font glyphs) or `ascii` (a source letter padded to two cells such as `F ` or `X `, `packages/contracts/src/source-row.ts:68`; `oo` for a watch, `cli/src/shared/tui-icons.ts:39`). The `chat.icons` setting picks the mode, and `OM_TUI_ICONS` overrides it for one session. Plain `om chat` offers `nerd` on its What's new card, and the icons switch in the open session without a restart.

## Sub-features

- `whats-new-try`: the card `Nerd Font icons` and its `[ Turn it on ]` button (ctrl+x `w`) store `chat.icons = nerd`.
- `live-switch`: the next `/watches` draw in the same session uses the new mode.
- `config-key`: `om config get chat.icons` names the key, the `emoji or nerd or ascii` rule and the `tui.icons` row.
- `env-override`: `OM_TUI_ICONS=nerd|ascii|emoji` outranks the stored setting; an unknown value falls back to the setting.

## How to get to it (user POV)

Run plain `om chat` (not `--workspace`), wide enough for the card (49 columns or more). Press the card's button, or run `om config set chat.icons nerd` and restart chat. Open `/watches`.

## Driving it with control-om

1. Seed a few watches with different source kinds (`watch create … --source feed:…`, `--source x:@…`, an inbound watch).
2. Start chat with no override: `OM_TUI_ICONS= OM_LANE_PORT=<port> control-om om -- chat`, in a terminal multiplexer pane that can be read back.
3. Read the card, open `/watches`, and capture the emoji rows. Esc.
4. Press ctrl+x then `w`. Check `control-om om -- config get chat.icons` reads `nerd`.
5. Open `/watches` again and read the code points of the first glyph on each row (private-use code points U+E000 to U+F8FF and U+F0000 and up mean nerd mode).

## Gotchas

- A terminal reader shows the Nerd Font glyphs as blanks or boxes when its font has none. Compare code points, not the rendered text.
- The card shows only while `chat.icons` is not already `nerd`. A lane that ran this once needs `config set chat.icons emoji` to show it again.
- Typing into the composer before the chord fires sends the text to the model as a message. Send ctrl+x as one key press (`ctrl+x` in herdr, `C-x` in tmux).

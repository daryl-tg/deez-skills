# Chat TUI icon modes (`chat.icons`)

*Re-driven 2026-11-06 (nightly), count only, tree `50fcc594b` (origin/main, v0.492.0), bare lane on 18165 with a scripted fake model on 18164: the card read `What's new · 1 of 14` and `2 of 14` on a fresh home, so `Nerd Font icons` sits at `14 of 14` by the source's order (not paged to tonight). The switch was not pressed. Evidence: `http://127.0.0.1:8098/vom-nightly-20261106/r1/` (`tui/01-open.txt`, `tui/02-whatsnew-2.txt`).*

*Re-driven 2026-11-05 (nightly), ordinal only, tree `3a0ea623e` (origin/main, v0.492.0), bare lane on 18165 (dummy `OM_API_KEY`, dead service URLs) with a scripted fake model on 18164: `Nerd Font icons` is entry `11 of 11` on a fresh home. The switch itself was not pressed tonight. Evidence: `http://127.0.0.1:8098/vom-nightly-20261105/r1/` (`tui/11-whats-new-titles.txt`).*

*Re-driven 2026-11-04 (nightly), tree `9acb5fb56` (origin/main, v0.491.0), guest lane 18163, fake model on 18164, tmux 140x40: the workspace card's `Nerd Font icons` entry is now `8 of 8` (`Watch and source icons as Nerd Font glyphs.` / `Boxes? Set chat.icons emoji to go back.` / `[ Turn it on ]`), reached with seven ctrl+x `.`. `Turn it on` was not pressed and the glyphs were not re-driven. Evidence: `http://127.0.0.1:8098/vom-nightly-20261104/r1/` (`tui/03-wn-8.txt`).*

*Re-driven 2026-11-03 (nightly), tree `777ee7f21` (origin/main, v0.488.0), lane home 18163 with its daemon down (a guest sign-in 429), fake model on 18164, private tmux server at 140x40. Since #2254 plain `om chat` opens the workspace and the card shows there: `What's new · 1 of 2` led with `Workspace is now the default`; ctrl+x then `.` paged to `2 of 2`, **Nerd Font icons** / `[ Turn it on ]`, and ctrl+x then listed `w What's new: turn it on` (the `w` row follows the entry on screen). `w` stored `chat.icons = nerd` (`source: config (stored as tui.icons)`) and the card dropped to one entry with no pager. Not driven: the `/watches` glyphs after the switch, `ascii`, the `OM_TUI_ICONS` override. Evidence: `http://127.0.0.1:8098/vom-nightly-20261103/r1/` (`tui/03-whats-new-2-of-2.txt`, `tui/04-ctrlx-menu-page2.txt`, `tui/05-after-w-icons.txt`).*

*Re-driven 2026-11-02 (scheduled maintenance), tree `587ce2d0b` (origin/main, v0.480.3), lane on 18168 (`OM_FEED_ALLOW_LOOPBACK=1`, `OM_FEED_POLL_INTERVAL_MS=60000`), host load average about 5. First drive on main. Fake model on 18170 (the chat-workspace-tui `server.ts`), private tmux server, plain `om chat` with `OM_TUI_ICONS=` empty: the card read **Nerd Font icons** / **Watch and source icons as Nerd Font glyphs.** / `[ Turn it on ]`; `/watches` drew its header glyph as U+1F440; Esc, ctrl+x then `w` stored `chat.icons = nerd` (`config get` `source: config`); the next `/watches` in the same session drew U+F0208. `config set chat.icons maybe` exits 2 (`must be one of: emoji, nerd, ascii`); restored with `config set chat.icons emoji`. Not driven: `ascii`, the `OM_TUI_ICONS` override, per-row source glyphs.*

*Verified: 2026-11-02, branch `daryl/tui-nerd-icons` at `2be28d04d` (PR #2247, off origin/main `5cf89fe95`). Source CLI on lane 18131 with a fake model on 18132, in a herdr pane, with no `OM_TUI_ICONS` set. Plain `om chat` showed the What's new card `Nerd Font icons` with `[ Turn it on ]`. ctrl+x listed `w What's new: turn it on`. `w` stored `chat.icons = nerd` (`stored as tui.icons`) and closed the card. `/watches` in the same session drew the title eye as U+F0208, and the inbound, filings and X rows as U+F01C, U+F19C and U+F099. Before the press the same rows were 👀 📥 📄 🐦. On main since `587ce2d0b` (#2247). Not driven: `ascii` mode, `OM_TUI_ICONS` outranking a stored value, the page tabs' source icons.*

`om chat` draws the watch and source icons on `/watches` and its pages in one of three modes: `emoji` (the default), `nerd` (Nerd Font glyphs) or `ascii` (a source letter padded to two cells such as `F ` or `X `, `packages/contracts/src/source-row.ts:68`; `oo` for a watch, `cli/src/shared/tui-icons.ts:43`). The `chat.icons` setting picks the mode, and `OM_TUI_ICONS` overrides it for one session. `om chat` offers `nerd` on its What's new card, as the entry after `Workspace is now the default` (#2254, v0.487.0), and the icons switch in the open session without a restart.

## Sub-features

- `whats-new-try`: the card `Nerd Font icons` and its `[ Turn it on ]` button (ctrl+x `w` while that entry is on screen) store `chat.icons = nerd`. It is the last of fifteen entries in the workspace (`15 of 15` at `05f450fc5`, from source order; `14 of 14` at `50fcc594b`; one fewer in plain chat): page to it with ctrl+x `.` (or the card's `›`), and back with ctrl+x `,`.
- `live-switch`: the next `/watches` draw in the same session uses the new mode.
- `config-key`: `om config get chat.icons` names the key, the `emoji or nerd or ascii` rule and the `tui.icons` row.
- `env-override`: `OM_TUI_ICONS=nerd|ascii|emoji` outranks the stored setting; an unknown value falls back to the setting.

## How to get to it (user POV)

Run `om chat` (the workspace by default; `--no-workspace` shows no card), wide enough for the card (49 columns or more). Press ctrl+x then `.` to reach `Nerd Font icons`, then its button, or run `om config set chat.icons nerd` and restart chat. Open `/watches`.

## Driving it with control-om

1. Seed a few watches with different source kinds (`watch create … --source feed:…`, `--source x:@…`, an inbound watch).
2. Start chat with no override: `OM_TUI_ICONS= OM_LANE_PORT=<port> control-om om -- chat`, in a terminal multiplexer pane that can be read back.
3. Read the card, open `/watches`, and capture the emoji rows. Esc.
4. Press ctrl+x then `.` until the card reads `Nerd Font icons` (`What's new · 15 of 15` on a fresh home at `05f450fc5`, by source order and the live `1 of 15`; the ordinal moves as releases add entries), then ctrl+x and `w`. Check `control-om om -- config get chat.icons` reads `nerd`.
5. Open `/watches` again and read the code points of the first glyph on each row (private-use code points U+E000 to U+F8FF and U+F0000 and up mean nerd mode).

## Gotchas

- A terminal reader shows the Nerd Font glyphs as blanks or boxes when its font has none. Compare code points, not the rendered text.
- ctrl+x `w` acts on the entry on screen. On a fresh home the first entry is `Workspace is now the default`, so `w` there turns the workspace off and reopens plain chat, with no card.
- The card shows only while `chat.icons` is not already `nerd`. A lane that ran this once needs `config set chat.icons emoji` to show it again.
- Typing into the composer before the chord fires sends the text to the model as a message. Send ctrl+x as one key press (`ctrl+x` in herdr, `C-x` in tmux).

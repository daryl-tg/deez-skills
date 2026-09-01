# Send a message

Send lets a user post a message to a room from the composer or the CLI, see it
appear in the transcript, and confirm it persisted from a second view.

## Sub-features

- `send-compose` posts from the composer.
- `send-persist` survives a reload.
- `send-cli` posts the same shape from the terminal.

## How to get to it (user POV)

- Type in the composer and press Enter.
- Run `om room post <room> <text>` in a terminal.

## Driving it with control-omchat

Preconditions:

- `control-omchat doctor` reports the expected origin and a build matching the
  working tree.
- The fixture room `verify-lane` exists and is empty.

- **Open the room.** Choose it in the sidebar. Run
  `control-omchat browser click --role link --name "verify-lane"`. The
  transcript region appears with an empty state.
- **Post.** Type and send. Run
  `control-omchat browser fill --role textbox --name "Message" --value "probe one"`
  then `control-omchat browser press --key "Enter"`. The transcript's last row
  reads `probe one`.
- **Confirm persistence.** Reload and reopen. The row is still last.
- **CLI entry.** Run
  `control-omchat cli -- om room post verify-lane "probe two" --json`. Exit code
  `0`, and stdout carries the new message id.
- **Proof.** Capture the pair. Run
  `control-omchat browser snapshot --aria --path artifacts/send/transcript.aria.txt`
  and
  `control-omchat browser screenshot --path artifacts/send/transcript.png`.
  Both show the room name and both probe messages. Then
  `control-omchat evidence publish <run-id> <revision>` and hand back the URL.

## Gotchas

- Enter sends; Shift-Enter inserts a newline. Assert the transcript, not the
  composer.
- The transcript virtualizes. Assert the last row, not a fixed index.
- Delete both probe messages during fixture cleanup, but keep the artifacts.

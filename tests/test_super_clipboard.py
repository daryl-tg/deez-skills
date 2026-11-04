import subprocess
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from deezlib.superclanker import clipboard


class Run:
    def __init__(self, *outcomes):
        self.outcomes = list(outcomes)
        self.calls = []

    def __call__(self, argv, **kwargs):
        self.calls.append(list(argv))
        outcome = self.outcomes.pop(0)
        if isinstance(outcome, Exception):
            raise outcome
        code, stdout, writes = outcome
        if writes:
            target = next(Path(part.split('"')[1]) for part in argv if "POSIX file" in part)
            target.write_bytes(writes)
        return SimpleNamespace(returncode=code, stdout=stdout, stderr="")


class ClipboardTest(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.tmp = Path(tmp.name)
        self.dest = self.tmp / "attachments"

    def test_copied_image_data_is_saved_as_png(self):
        run = Run((1, "", None), (0, "", b"\x89PNG data"))

        saved = clipboard.grab_image(self.dest, run=run)

        self.assertEqual(saved.parent, self.dest)
        self.assertEqual(saved.suffix, ".png")
        self.assertEqual(saved.read_bytes(), b"\x89PNG data")
        self.assertEqual(run.calls[1][0], "osascript")
        self.assertIn("PNGf", " ".join(run.calls[1]))

    def test_copied_image_file_is_used_by_path(self):
        shot = self.tmp / "Screen Shot.png"
        shot.write_bytes(b"png")
        run = Run((0, f"{shot}\n", None))

        self.assertEqual(clipboard.grab_image(self.dest, run=run), shot.resolve())
        self.assertEqual(len(run.calls), 1)

    def test_copied_non_image_file_falls_back_to_image_data(self):
        notes = self.tmp / "notes.txt"
        notes.write_text("x")
        run = Run((0, f"{notes}\n", None), (1, "", None))

        self.assertIsNone(clipboard.grab_image(self.dest, run=run))

    def test_no_image_on_the_clipboard_leaves_nothing_behind(self):
        run = Run((1, "", None), (1, "", None))

        self.assertIsNone(clipboard.grab_image(self.dest, run=run))
        self.assertEqual(list(self.dest.glob("*")), [])

    def test_osascript_failure_is_no_image(self):
        run = Run(OSError("no osascript"), subprocess.TimeoutExpired("osascript", 5))

        self.assertIsNone(clipboard.grab_image(self.dest, run=run))

    def test_dropped_paths_with_spaces_and_quotes_are_images(self):
        first = self.tmp / "Screen Shot 1.png"
        second = self.tmp / "b.JPG"
        first.write_bytes(b"x")
        second.write_bytes(b"x")
        dropped = f"{str(first).replace(' ', chr(92) + ' ')} '{second}'"

        self.assertEqual(clipboard.image_paths(dropped), [first.resolve(), second.resolve()])

    def test_text_or_missing_files_are_not_images(self):
        self.assertEqual(clipboard.image_paths("fix the tape"), [])
        self.assertEqual(clipboard.image_paths(str(self.tmp / "gone.png")), [])
        self.assertEqual(clipboard.image_paths("it's broken"), [])


if __name__ == "__main__":
    unittest.main()

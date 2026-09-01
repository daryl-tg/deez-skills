import tempfile
import unittest
from pathlib import Path

from deezlib import apply
from deezlib.linkplan import Action


def action(verb, src, dest):
    return Action(verb, "claude", "skill", "alpha", src, dest, "reason")


class ExecuteTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.src = self.root / "repo" / "skills" / "alpha"
        self.src.mkdir(parents=True)
        (self.src / "SKILL.md").write_text("---\nname: alpha\ndescription: d\n---\n")
        self.dest_dir = self.root / "claude" / "skills"
        self.dest_dir.mkdir(parents=True)
        self.dest = self.dest_dir / "alpha"
        self.state = self.root / "state"

    def run_one(self, verb):
        return apply.execute([action(verb, self.src, self.dest)], self.state, "STAMP")

    def test_link_creates_a_symlink(self):
        self.run_one("link")
        self.assertTrue(self.dest.is_symlink())
        self.assertEqual(self.dest.resolve(), self.src.resolve())

    def test_ok_changes_nothing(self):
        self.dest.symlink_to(self.src)
        self.run_one("ok")
        self.assertTrue(self.dest.is_symlink())

    def test_relink_repoints_without_backup(self):
        other = self.root / "other"
        other.mkdir()
        self.dest.symlink_to(other)
        self.run_one("relink")
        self.assertEqual(self.dest.resolve(), self.src.resolve())
        self.assertFalse((self.state / "STAMP").exists())

    def test_adopt_replaces_the_matching_directory(self):
        self.dest.mkdir()
        (self.dest / "SKILL.md").write_text("---\nname: alpha\ndescription: d\n---\n")
        self.run_one("adopt")
        self.assertTrue(self.dest.is_symlink())

    def test_backup_moves_the_original_and_never_deletes(self):
        self.dest.mkdir()
        (self.dest / "SKILL.md").write_text("original\n")
        self.run_one("backup")
        self.assertTrue(self.dest.is_symlink())
        saved = self.state / "STAMP" / "claude" / "skill" / "alpha" / "SKILL.md"
        self.assertEqual(saved.read_text(), "original\n")

    def test_missing_source_raises_before_touching_anything(self):
        missing = self.root / "repo" / "skills" / "ghost"
        with self.assertRaises(apply.ApplyError):
            apply.execute(
                [action("missing-source", missing, self.dest)], self.state, "STAMP"
            )
        self.assertFalse(self.dest.exists())

    def test_a_missing_source_blocks_the_whole_batch(self):
        missing = self.root / "repo" / "skills" / "ghost"
        good = action("link", self.src, self.dest)
        bad = Action("missing-source", "claude", "skill", "ghost", missing,
                     self.dest_dir / "ghost", "reason")
        with self.assertRaises(apply.ApplyError):
            apply.execute([good, bad], self.state, "STAMP")
        self.assertFalse(self.dest.exists())

    def test_unknown_verb_raises(self):
        with self.assertRaises(apply.ApplyError):
            self.run_one("teleport")


if __name__ == "__main__":
    unittest.main()

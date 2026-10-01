import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


class ScaffoldTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.work = Path(self.tmp.name) / "repo"
        # Copy only what the CLI needs. Copying the whole tree meant every
        # skill added to the hub slowed these five tests down; the suite went
        # from 3s to 54s before anyone noticed.
        self.work.mkdir(parents=True)
        for item in ("bin", "deezlib", "templates"):
            shutil.copytree(REPO / item, self.work / item,
                            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        for item in ("registry.toml", "vendor.toml", "README.md"):
            shutil.copy2(REPO / item, self.work / item)
        for d in ("skills", "commands", "agents"):
            (self.work / d).mkdir(exist_ok=True)
        self.env = {
            **os.environ,
            "DEEZ_CLAUDE_HOME": f"{self.tmp.name}/claude",
            "DEEZ_CODEX_HOME": f"{self.tmp.name}/codex",
        }

    def run_deez(self, *args):
        return subprocess.run(
            [str(self.work / "bin" / "deez"), *args],
            capture_output=True,
            text=True,
            env=self.env,
            cwd=str(self.work),
        )

    def test_new_creates_folder_and_registers_it(self):
        result = self.run_deez("new", "example-skill", "--category", "workflow")
        self.assertEqual(result.returncode, 0, result.stderr)
        skill = self.work / "skills" / "example-skill" / "SKILL.md"
        self.assertTrue(skill.is_file())
        self.assertIn("name: example-skill", skill.read_text())
        self.assertIn("[skills.example-skill]", (self.work / "registry.toml").read_text())

    def test_new_leaves_the_repo_consistent(self):
        self.run_deez("new", "example-skill", "--category", "workflow")
        result = self.run_deez("doctor")
        self.assertNotIn("unregistered", result.stdout)
        self.assertNotIn("readme-stale", result.stdout)

    def test_new_rejects_a_duplicate_name(self):
        self.run_deez("new", "example-skill", "--category", "workflow")
        result = self.run_deez("new", "example-skill", "--category", "workflow")
        self.assertNotEqual(result.returncode, 0)

    def test_new_rejects_an_unknown_category(self):
        result = self.run_deez("new", "example-skill", "--category", "nonsense")
        self.assertNotEqual(result.returncode, 0)

    def test_adopt_copies_a_directory_without_touching_the_original(self):
        source = Path(self.tmp.name) / "outside" / "borrowed"
        source.mkdir(parents=True)
        (source / "SKILL.md").write_text(
            "---\nname: borrowed\ndescription: Does a thing.\n---\n\nBody\n"
        )
        result = self.run_deez("adopt", str(source), "--category", "workflow")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.work / "skills" / "borrowed" / "SKILL.md").is_file())
        self.assertTrue((source / "SKILL.md").is_file())
        self.assertIn("[skills.borrowed]", (self.work / "registry.toml").read_text())

    def test_adopt_takes_the_name_from_frontmatter(self):
        source = Path(self.tmp.name) / "outside" / "some-dir"
        source.mkdir(parents=True)
        (source / "SKILL.md").write_text(
            "---\nname: real-name\ndescription: Does a thing.\n---\n"
        )
        self.run_deez("adopt", str(source), "--category", "workflow")
        self.assertTrue((self.work / "skills" / "real-name").is_dir())

    def test_adopt_rejects_a_directory_without_skill_md(self):
        source = Path(self.tmp.name) / "outside" / "empty"
        source.mkdir(parents=True)
        result = self.run_deez("adopt", str(source), "--category", "workflow")
        self.assertNotEqual(result.returncode, 0)

    def test_adopt_never_links_anything(self):
        source = Path(self.tmp.name) / "outside" / "borrowed"
        source.mkdir(parents=True)
        (source / "SKILL.md").write_text(
            "---\nname: borrowed\ndescription: Does a thing.\n---\n"
        )
        self.run_deez("adopt", str(source), "--category", "workflow")
        self.assertFalse(Path(self.tmp.name, "claude").exists())
        self.assertFalse(Path(self.tmp.name, "codex").exists())


if __name__ == "__main__":
    unittest.main()

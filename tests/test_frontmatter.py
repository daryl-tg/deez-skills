import tempfile
import unittest
from pathlib import Path

from deezlib import frontmatter


def write(tmp, text):
    path = Path(tmp) / "SKILL.md"
    path.write_text(text)
    return path


class ParseTest(unittest.TestCase):
    def test_reads_name_and_description(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = write(tmp, "---\nname: humanize\ndescription: Rewrites text.\n---\n\nBody\n")
            self.assertEqual(
                frontmatter.parse(path),
                {"name": "humanize", "description": "Rewrites text."},
            )

    def test_strips_surrounding_quotes(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = write(tmp, '---\nname: "x"\ndescription: "Use when: y."\n---\n')
            self.assertEqual(frontmatter.parse(path)["description"], "Use when: y.")

    def test_reads_a_folded_block_description(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = write(
                tmp,
                "---\nname: x\ndescription: >\n  first line\n  second line\n---\n",
            )
            self.assertEqual(
                frontmatter.parse(path)["description"], "first line second line"
            )

    def test_missing_file_raises(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(frontmatter.FrontmatterError):
                frontmatter.parse(Path(tmp) / "absent.md")

    def test_missing_frontmatter_raises(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = write(tmp, "# no frontmatter\n")
            with self.assertRaises(frontmatter.FrontmatterError):
                frontmatter.parse(path)

    def test_missing_name_raises(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = write(tmp, "---\ndescription: y\n---\n")
            with self.assertRaises(frontmatter.FrontmatterError) as ctx:
                frontmatter.parse(path)
            self.assertIn("name", str(ctx.exception))

    def test_budget_constants_match_the_spec(self):
        self.assertEqual(frontmatter.DESCRIPTION_FAIL, 300)
        self.assertEqual(frontmatter.DESCRIPTION_WARN, 200)


class RealWorldTest(unittest.TestCase):
    """The parser has to survive the frontmatter styles already in use."""

    def test_multiline_description_with_colons_and_backticks(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = write(
                tmp,
                "---\nname: om-chat-feature\n"
                "description: Own an OM Chat feature: diagnose, implement, `test`.\n"
                "---\n",
            )
            parsed = frontmatter.parse(path)
            self.assertEqual(parsed["name"], "om-chat-feature")
            self.assertIn("`test`", parsed["description"])


if __name__ == "__main__":
    unittest.main()

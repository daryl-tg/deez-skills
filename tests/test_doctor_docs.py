import tempfile
import unittest
from pathlib import Path

from deezlib import doctor, registry

BASE = """
[meta]
version = 1
default_profile = "full"

[categories]
core = "Always-on essentials"

[profiles]
full = ["*"]
"""

# Two skills (one of them a principle), one agent, and a router owning two
# playbooks: the real counts every fixture below is measured against.
TREE = """
[skills.router]
layer = "mode"
category = "core"
runtimes = ["claude"]

[skills.principle-alpha]
layer = "principle"
category = "core"
runtimes = ["claude", "codex"]

[agents.scout]
category = "core"
runtimes = ["claude"]
"""

LISTED = """\
# hub

| playbook | for |
|---|---|
| [first](./skills/router/playbooks/first.md) | one |
| [second](./skills/router/playbooks/second.md) | two |

| principle | apply when |
| --- | --- |
| `alpha` | always |

"""


SECOND_ROW = "| [second](./skills/router/playbooks/second.md) | two |\n"


class DocsFixture(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.repo = Path(self.tmp.name)
        for name in ("router", "principle-alpha"):
            folder = self.repo / "skills" / name
            folder.mkdir(parents=True)
            (folder / "SKILL.md").write_text(
                f"---\nname: {name}\ndescription: D.\n"
                f"disable-model-invocation: true\n---\n"
            )
        playbooks = self.repo / "skills" / "router" / "playbooks"
        playbooks.mkdir()
        (playbooks / "first.md").write_text("# First\n")
        (playbooks / "second.md").write_text("# Second\n")
        (self.repo / "agents").mkdir()
        (self.repo / "agents" / "scout.md").write_text(
            "---\nname: scout\ndescription: Finds things.\n---\n"
        )
        (self.repo / "docs").mkdir()

    def load(self):
        path = self.repo / "registry.toml"
        path.write_text(BASE + TREE)
        return registry.load(path)

    def write(self, relative, text):
        path = self.repo / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)

    def findings(self, check):
        return check(self.load(), self.repo)

    def codes(self, check):
        return sorted(f.code for f in self.findings(check))

    def details(self, check):
        return [f.detail for f in self.findings(check)]


class CountClaimTest(DocsFixture):
    def claims(self):
        return self.codes(doctor.check_count_claims)

    def test_a_wrong_digit_count_fails(self):
        self.write("README.md", "The hub ships 5 playbooks.\n")
        self.assertEqual(self.claims(), ["count-claim"])

    def test_a_right_digit_count_passes(self):
        self.write("README.md", "The hub ships 2 playbooks and 1 agents.\n")
        self.assertEqual(self.claims(), [])

    def test_a_hyphenated_number_word_is_read(self):
        self.write("README.md", "Twenty-four principles, one router.\n")
        details = self.details(doctor.check_count_claims)
        self.assertEqual(len(details), 1)
        self.assertIn("README.md:1", details[0])
        self.assertIn("Twenty-four principles", details[0])
        self.assertIn("the tree has 1", details[0])

    def test_skills_count_every_registered_skill(self):
        self.write("README.md", "Two skills and one principles.\n")
        self.assertEqual(self.claims(), [])

    def test_docs_are_scanned_too(self):
        self.write("docs/guide/01.md", "Pick one of three playbooks.\n")
        self.assertEqual(self.claims(), ["count-claim"])

    def test_fenced_code_is_skipped(self):
        self.write("README.md", "```text\n9 playbooks\n```\n")
        self.assertEqual(self.claims(), [])

    def test_the_generated_index_is_skipped(self):
        self.write("README.md", "Intro.\n\n<!-- deez:index -->\n\n9 skills\n")
        self.assertEqual(self.claims(), [])

    def test_an_opt_out_on_the_line_passes(self):
        self.write("README.md", "Three skills fire alone. <!-- deez:counts-ok -->\n")
        self.assertEqual(self.claims(), [])

    def test_an_opt_out_on_the_line_above_passes(self):
        self.write("docs/history.md", "<!-- deez:counts-ok -->\nAdopted 59 skills.\n")
        self.assertEqual(self.claims(), [])

    def test_the_opt_out_covers_one_line_only(self):
        self.write("docs/history.md", "<!-- deez:counts-ok -->\nok\n59 skills.\n")
        self.assertEqual(self.claims(), ["count-claim"])

    def test_an_inline_opt_out_does_not_cover_the_next_line(self):
        self.write("README.md", "Three skills fire alone. <!-- deez:counts-ok -->\nAnd 99 principles here.\n")
        self.assertEqual(self.claims(), ["count-claim"])

    def test_a_comparison_table_quoting_other_counts_passes(self):
        self.write("docs/architecture.md", "| | pstack | hub |\n|---|---|---|\n| Skills | 45 | 33 |\n")
        self.assertEqual(self.claims(), [])

    def test_words_that_are_not_numbers_are_ignored(self):
        self.write("README.md", "Why principles. Hub skills. A three-skill set.\n")
        self.assertEqual(self.claims(), [])

    def test_doctor_runs_it(self):
        self.write("README.md", "Ships 9 agents.\n")
        roots = {"claude": {"skill": self.repo / "nowhere"}}
        codes = [f.code for f in doctor.check(self.load(), self.repo, roots, "full")]
        self.assertIn("count-claim", codes)


class ReadmeListTest(DocsFixture):
    def lists(self):
        return self.codes(doctor.check_readme_lists)

    def test_every_playbook_and_principle_listed_passes(self):
        self.write("README.md", LISTED)
        self.assertEqual(self.lists(), [])

    def test_a_playbook_missing_from_the_table_fails(self):
        self.write("README.md", LISTED.replace(SECOND_ROW, ""))
        self.assertEqual(self.lists(), ["unlisted-playbook"])
        self.assertIn("second", self.details(doctor.check_readme_lists)[0])

    def test_a_listing_inside_the_generated_index_does_not_count(self):
        head = LISTED.replace(SECOND_ROW, "")
        tail = "<!-- deez:index -->\n(./skills/router/playbooks/second.md)\n"
        self.write("README.md", head + tail)
        self.assertEqual(self.lists(), ["unlisted-playbook"])

    def test_a_principle_missing_from_the_table_fails(self):
        self.write("README.md", LISTED.replace("| `alpha` | always |\n", ""))
        self.assertEqual(self.lists(), ["unlisted-principle"])

    def test_a_listed_principle_that_is_not_registered_fails(self):
        self.write("README.md", LISTED + "| principle | x |\n|---|---|\n| `gone` | y |\n")
        self.assertEqual(self.lists(), ["unknown-principle"])
        self.assertIn("gone", self.details(doctor.check_readme_lists)[0])

    def test_no_readme_is_silent(self):
        self.assertEqual(self.lists(), [])


class DocLinkTest(DocsFixture):
    def links(self):
        return self.codes(doctor.check_doc_links)

    def test_a_missing_relative_target_fails(self):
        self.write("README.md", "See [guide](./docs/nope.md).\n")
        self.assertEqual(self.links(), ["broken-link"])

    def test_an_existing_target_passes(self):
        self.write("docs/a.md", "# A\n")
        self.write("README.md", "See [a](./docs/a.md) and [dir](./docs/).\n")
        self.assertEqual(self.links(), [])

    def test_links_resolve_relative_to_the_linking_file(self):
        self.write("docs/guide/01.md", "Back to [readme](../../README.md).\n")
        self.write("README.md", "# hub\n")
        self.assertEqual(self.links(), [])

    def test_a_missing_anchor_fails(self):
        self.write("docs/a.md", "# A\n\n## Set it up\n")
        self.write("README.md", "See [a](./docs/a.md#install).\n")
        self.assertEqual(self.links(), ["broken-anchor"])

    def test_a_github_slugged_anchor_passes(self):
        self.write("docs/a.md", "# A\n\n## What `installed` means, really?\n")
        self.write("README.md", "[a](./docs/a.md#what-installed-means-really)\n")
        self.assertEqual(self.links(), [])

    def test_a_repeated_heading_gets_a_numbered_anchor(self):
        self.write("docs/a.md", "## Notes\n\n## Notes\n\n[b](#notes-1) [c](#notes-2)\n")
        self.assertEqual(self.links(), ["broken-anchor"])

    def test_a_same_file_anchor_is_checked(self):
        self.write("README.md", "## install\n\n[go](#install) [no](#setup)\n")
        self.assertEqual(self.links(), ["broken-anchor"])

    def test_a_heading_inside_a_fence_is_not_an_anchor(self):
        self.write("README.md", "```\n## install\n```\n\n[go](#install)\n")
        self.assertEqual(self.links(), ["broken-anchor"])

    def test_external_links_are_ignored(self):
        self.write("README.md", "[x](https://x.test/a) [m](mailto:a@b.test)\n")
        self.assertEqual(self.links(), [])

    def test_links_in_code_are_ignored(self):
        self.write("README.md", "```md\n[x](./nope.md)\n```\n`[y](./nope.md)`\n")
        self.assertEqual(self.links(), [])

    def test_agents_are_scanned(self):
        self.write("agents/scout.md", "---\nname: scout\ndescription: D.\n---\n[x](./nope.md)\n")
        self.assertEqual(self.links(), ["broken-link"])


FILES = """
[agents.scout]
category = "core"
runtimes = ["claude"]

[commands.go-now]
category = "core"
runtimes = ["claude"]
"""


class FileFrontmatterTest(unittest.TestCase):
    """Agents and commands are single files, so the stem is the name."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.repo = Path(self.tmp.name)
        (self.repo / "agents").mkdir()
        (self.repo / "commands").mkdir()
        self.agent("name: scout\ndescription: D.")
        self.command("description: D.")

    def agent(self, head):
        (self.repo / "agents" / "scout.md").write_text(f"---\n{head}\n---\nBody\n")

    def command(self, head):
        (self.repo / "commands" / "go-now.md").write_text(f"---\n{head}\n---\nBody\n")

    def codes(self):
        path = self.repo / "registry.toml"
        path.write_text(BASE + FILES)
        roots = {"claude": {"skill": self.repo / "nowhere"}}
        return sorted(
            f.code for f in doctor.check(registry.load(path), self.repo, roots, "full")
            if f.code in ("name-mismatch", "invalid-name")
        )

    def detail(self, code):
        path = self.repo / "registry.toml"
        path.write_text(BASE + FILES)
        roots = {"claude": {"skill": self.repo / "nowhere"}}
        return next(f.detail for f in doctor.check(registry.load(path), self.repo, roots, "full")
                    if f.code == code)

    def test_matching_names_pass(self):
        self.assertEqual(self.codes(), [])

    def test_an_agent_name_that_is_not_the_stem_fails(self):
        self.agent("name: finder\ndescription: D.")
        self.assertEqual(self.codes(), ["name-mismatch"])

    def test_an_agent_without_a_name_fails(self):
        self.agent("description: D.")
        self.assertEqual(self.codes(), ["name-mismatch"])
        self.assertIn("missing name:", self.detail("name-mismatch"))

    def test_a_command_name_that_is_not_the_stem_fails(self):
        self.command("name: go\ndescription: D.")
        self.assertEqual(self.codes(), ["name-mismatch"])

    def test_a_command_with_a_matching_name_passes(self):
        self.command("name: go-now\ndescription: D.")
        self.assertEqual(self.codes(), [])

    def test_a_name_with_bad_characters_fails(self):
        (self.repo / "agents" / "scout.md").unlink()
        path = self.repo / "registry.toml"
        (self.repo / "agents" / "Scout_1.md").write_text(
            "---\nname: Scout_1\ndescription: D.\n---\n"
        )
        path.write_text(BASE + FILES.replace("agents.scout", "agents.Scout_1"))
        roots = {"claude": {"skill": self.repo / "nowhere"}}
        codes = [f.code for f in doctor.check(registry.load(path), self.repo, roots, "full")]
        self.assertIn("invalid-name", codes)

    def test_a_name_over_64_characters_fails(self):
        long = "a" * 65
        (self.repo / "agents" / "scout.md").unlink()
        (self.repo / "agents" / f"{long}.md").write_text(
            f"---\nname: {long}\ndescription: D.\n---\n"
        )
        path = self.repo / "registry.toml"
        path.write_text(BASE + FILES.replace("agents.scout", f"agents.{long}"))
        roots = {"claude": {"skill": self.repo / "nowhere"}}
        codes = [f.code for f in doctor.check(registry.load(path), self.repo, roots, "full")]
        self.assertIn("invalid-name", codes)


class RuntimeToolTest(unittest.TestCase):
    """A Codex-installed skill naming a Claude-only tool reads as noise there."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.repo = Path(self.tmp.name)
        self.runtimes = '["claude", "codex"]'

    def skill(self, body, extra=None):
        folder = self.repo / "skills" / "tool"
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "SKILL.md").write_text(f"---\nname: tool\ndescription: D.\n---\n{body}\n")
        for relative, text in (extra or {}).items():
            (folder / relative).parent.mkdir(parents=True, exist_ok=True)
            (folder / relative).write_text(text)

    def findings(self):
        path = self.repo / "registry.toml"
        path.write_text(
            BASE + f'\n[skills.tool]\ncategory = "core"\nruntimes = {self.runtimes}\n'
        )
        return [
            f for f in doctor.check_runtime_neutrality(registry.load(path), self.repo)
            if f.code == "runtime-specific-tool"
        ]

    def test_ask_user_question_in_prose_warns(self):
        self.skill("Use `AskUserQuestion` with options.")
        findings = self.findings()
        self.assertEqual([f.level for f in findings], ["warn"])
        self.assertIn("AskUserQuestion", findings[0].detail)
        self.assertIn("SKILL.md:5", findings[0].detail)

    def test_todo_write_and_agent_call_warn(self):
        self.skill("Track it with TodoWrite.\nThen `Agent(subagent_type: x)`.")
        self.assertEqual(len(self.findings()), 2)

    def test_a_mapping_table_row_is_fine(self):
        self.skill("| ask | `AskUserQuestion` | plain text |")
        self.assertEqual(self.findings(), [])

    def test_a_claude_only_skill_is_fine(self):
        self.runtimes = '["claude"]'
        self.skill("Use `AskUserQuestion`.")
        self.assertEqual(self.findings(), [])

    def test_reference_files_are_scanned(self):
        self.skill("Body.", {"references/ask.md": "Call AskUserQuestion.\n"})
        self.assertEqual(len(self.findings()), 1)


if __name__ == "__main__":
    unittest.main()

import hashlib
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from deezlib import featuremaps, registry


REPO = Path(__file__).resolve().parents[1]


class FeatureMapPublishTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        root = Path(self.tmp.name)
        self.repo = root / "hub"
        self.remote = root / "remote.git"
        self.hooks = root / "empty-hooks"
        self.hooks.mkdir()
        self.env = {
            **os.environ,
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_CONFIG_GLOBAL": os.devnull,
            "GIT_TERMINAL_PROMPT": "0",
        }
        self.env_patch = mock.patch.dict(os.environ, self.env, clear=True)
        self.env_patch.start()
        self.addCleanup(self.env_patch.stop)

        self.run_git(self.remote.parent, "init", "--bare", "-q", str(self.remote))
        self.run_git(self.remote.parent, "init", "-q", "-b", "main", str(self.repo))
        self.git("config", "user.email", "maps@example.test")
        self.git("config", "user.name", "Feature Maps")
        self.git("config", "core.hooksPath", str(self.hooks))
        self.git("config", "commit.gpgSign", "false")
        self.git("remote", "add", "origin", str(self.remote))

        self.features = (
            self.repo / "projects" / "chat-app" / "skills" / "verify-chat" / "features"
        )
        self.features.mkdir(parents=True)
        (self.features.parent / "SKILL.md").write_text(
            "---\nname: verify-chat\ndescription: Verify chat.\n---\n",
            encoding="utf-8",
        )
        (self.features / "README.md").write_text("# Feature maps\n", encoding="utf-8")
        (self.repo / "registry.toml").write_text(
            "[skills.verify-chat]\nproject = \"chat-app\"\n",
            encoding="utf-8",
        )
        (self.repo / "staged.txt").write_text("original staged\n", encoding="utf-8")
        (self.repo / "unstaged.txt").write_text("original unstaged\n", encoding="utf-8")
        self.git("add", "-A")
        self.git("commit", "-qm", "initial")
        self.git("push", "-q", "-u", "origin", "main")

        self.reg = registry.Registry(
            version=1,
            default_profile="full",
            categories={"verification": "Verification"},
            profiles={"full": ("*",)},
            entries=(
                registry.Entry(
                    kind="skill",
                    name="verify-chat",
                    category="verification",
                    runtimes=("claude", "codex"),
                    project="chat-app",
                ),
                registry.Entry(
                    kind="skill",
                    name="verify-shop",
                    category="verification",
                    runtimes=("claude", "codex"),
                    project="shop-app",
                ),
            ),
        )

    def run_git(self, cwd, *args, check=True):
        return subprocess.run(
            ["git", "-C", str(cwd), *args],
            check=check,
            capture_output=True,
            text=True,
            env=self.env,
        )

    def git(self, *args, check=True):
        return self.run_git(self.repo, *args, check=check)

    def publish(self, *files):
        return featuremaps.publish(
            self.repo, self.reg, "chat-app", "verify-chat", list(files)
        )

    def remote_file(self, relative):
        return self.run_git(
            self.remote.parent,
            f"--git-dir={self.remote}",
            "show",
            f"main:{relative}",
        ).stdout

    def other_clone_pushes(self, name, text):
        other = Path(self.tmp.name) / f"other-clone-{name}"
        if not other.exists():
            self.run_git(other.parent, "clone", "-q", str(self.remote), str(other))
            self.run_git(other, "checkout", "-q", "main")
            self.run_git(other, "config", "user.email", "other@example.test")
            self.run_git(other, "config", "user.name", "Other")
        self.run_git(other, "pull", "-q", "--ff-only", "origin", "main")
        (other / name).write_text(text, encoding="utf-8")
        self.run_git(other, "add", name)
        self.run_git(other, "commit", "-qm", f"remote {name}")
        self.run_git(other, "push", "-q", "origin", "main")

    def remote_head(self):
        return self.run_git(
            self.remote.parent, f"--git-dir={self.remote}", "rev-parse", "main"
        ).stdout.strip()

    def test_publishes_only_selected_maps_and_preserves_other_changes(self):
        feature = self.features / "composer.md"
        feature.write_text("# Composer\n\nVerified.\n", encoding="utf-8")
        (self.repo / "staged.txt").write_text("staged locally\n", encoding="utf-8")
        self.git("add", "staged.txt")
        (self.repo / "unstaged.txt").write_text("unstaged locally\n", encoding="utf-8")

        status = self.publish("composer.md")

        relative = "projects/chat-app/skills/verify-chat/features/composer.md"
        self.assertEqual(status, "feature maps: committed and pushed 1 file")
        self.assertEqual(self.remote_file(relative), "# Composer\n\nVerified.\n")
        self.assertEqual(self.remote_file("staged.txt"), "original staged\n")
        self.assertEqual(self.remote_file("unstaged.txt"), "original unstaged\n")
        self.assertIn("staged.txt", self.git("diff", "--cached", "--name-only").stdout)
        self.assertIn("unstaged.txt", self.git("diff", "--name-only").stdout)
        pushed_paths = self.git(
            "diff-tree", "--no-commit-id", "--name-only", "-r", "HEAD"
        ).stdout.splitlines()
        self.assertEqual(pushed_paths, [relative])

    def test_publishes_a_tracked_map_deletion_and_preserves_other_changes(self):
        feature = self.features / "obsolete.md"
        feature.write_text("obsolete\n", encoding="utf-8")
        self.git("add", str(feature.relative_to(self.repo)))
        self.git("commit", "-qm", "add obsolete map")
        self.git("push", "-q", "origin", "main")
        feature.unlink()
        (self.repo / "staged.txt").write_text("staged locally\n", encoding="utf-8")
        self.git("add", "staged.txt")
        (self.repo / "unstaged.txt").write_text("unstaged locally\n", encoding="utf-8")

        status = self.publish("obsolete.md")

        self.assertEqual(status, "feature maps: committed and pushed 1 file")
        missing = self.run_git(
            self.remote.parent,
            f"--git-dir={self.remote}",
            "cat-file",
            "-e",
            "main:projects/chat-app/skills/verify-chat/features/obsolete.md",
            check=False,
        )
        self.assertNotEqual(missing.returncode, 0)
        self.assertIn("staged.txt", self.git("diff", "--cached", "--name-only").stdout)
        self.assertIn("unstaged.txt", self.git("diff", "--name-only").stdout)

    def test_registry_must_match_the_project_and_skill(self):
        with self.assertRaisesRegex(featuremaps.FeatureMapError, "belongs to project"):
            featuremaps.publish(
                self.repo, self.reg, "other-app", "verify-chat", ["README.md"]
            )
        with self.assertRaisesRegex(featuremaps.FeatureMapError, "not registered"):
            featuremaps.publish(
                self.repo, self.reg, "chat-app", "verify-missing", ["README.md"]
            )

    def test_new_local_skill_requires_remote_baseline_and_preserves_files(self):
        new_root = self.repo / "projects" / "new-app" / "skills" / "verify-new"
        (new_root / "features").mkdir(parents=True)
        skill_file = new_root / "SKILL.md"
        map_file = new_root / "features" / "first.md"
        skill_file.write_text(
            "---\nname: verify-new\ndescription: Verify new.\n---\n",
            encoding="utf-8",
        )
        map_file.write_text("new map\n", encoding="utf-8")
        registry_file = self.repo / "registry.toml"
        registry_file.write_text(
            registry_file.read_text(encoding="utf-8")
            + "\n[skills.verify-new]\nproject = \"new-app\"\n",
            encoding="utf-8",
        )
        local_reg = registry.Registry(
            version=self.reg.version,
            default_profile=self.reg.default_profile,
            categories=self.reg.categories,
            profiles=self.reg.profiles,
            entries=self.reg.entries
            + (
                registry.Entry(
                    kind="skill",
                    name="verify-new",
                    category="verification",
                    runtimes=("claude", "codex"),
                    project="new-app",
                ),
            ),
        )
        before_head = self.git("rev-parse", "HEAD").stdout.strip()
        before_remote = self.run_git(
            self.remote.parent, f"--git-dir={self.remote}", "rev-parse", "main"
        ).stdout.strip()
        before_status = self.git(
            "status", "--porcelain=v1", "-z", "--untracked-files=all"
        ).stdout
        before_hashes = {
            path: hashlib.sha256(path.read_bytes()).hexdigest()
            for path in (registry_file, skill_file, map_file)
        }

        with self.assertRaisesRegex(
            featuremaps.FeatureMapError, "ordinary verification-skill delivery"
        ):
            featuremaps.publish(
                self.repo, local_reg, "new-app", "verify-new", ["first.md"]
            )

        self.assertEqual(self.git("rev-parse", "HEAD").stdout.strip(), before_head)
        self.assertEqual(
            self.run_git(
                self.remote.parent, f"--git-dir={self.remote}", "rev-parse", "main"
            ).stdout.strip(),
            before_remote,
        )
        self.assertEqual(
            self.git("status", "--porcelain=v1", "-z", "--untracked-files=all").stdout,
            before_status,
        )
        self.assertEqual(
            {
                path: hashlib.sha256(path.read_bytes()).hexdigest()
                for path in (registry_file, skill_file, map_file)
            },
            before_hashes,
        )

    def test_rejects_traversal_nested_non_markdown_and_absolute_names(self):
        for name in ("../outside.md", "nested/map.md", "map.txt", str(self.features / "README.md")):
            with self.subTest(name=name):
                with self.assertRaises(featuremaps.FeatureMapError):
                    self.publish(name)

    def test_rejects_a_map_symlink_to_an_outside_file(self):
        outside = Path(self.tmp.name) / "outside.md"
        outside.write_text("secret\n", encoding="utf-8")
        (self.features / "linked.md").symlink_to(outside)

        with self.assertRaisesRegex(featuremaps.FeatureMapError, "symlink"):
            self.publish("linked.md")

    def test_rejects_a_missing_map_that_was_never_tracked(self):
        with self.assertRaisesRegex(featuremaps.FeatureMapError, "does not exist"):
            self.publish("invented.md")

    def test_unrelated_unpushed_commit_neither_blocks_nor_ships(self):
        (self.repo / "other.txt").write_text("other\n", encoding="utf-8")
        self.git("add", "other.txt")
        self.git("commit", "-qm", "unrelated local commit")
        local_head = self.git("rev-parse", "HEAD").stdout.strip()
        (self.features / "composer.md").write_text("map\n", encoding="utf-8")

        status = self.publish("composer.md")

        self.assertTrue(status.startswith("feature maps: committed and pushed 1 file"))
        self.assertIn("left as is", status)
        relative = "projects/chat-app/skills/verify-chat/features/composer.md"
        self.assertEqual(self.remote_file(relative), "map\n")
        self.assertNotEqual(
            self.run_git(
                self.remote.parent, f"--git-dir={self.remote}", "cat-file", "-e",
                "main:other.txt", check=False,
            ).returncode,
            0,
        )
        self.assertEqual(self.git("rev-parse", "HEAD").stdout.strip(), local_head)

    def test_remote_main_ahead_publishes_on_top_and_fast_forwards(self):
        self.other_clone_pushes("remote.txt", "remote\n")
        (self.features / "composer.md").write_text("map\n", encoding="utf-8")
        (self.repo / "unstaged.txt").write_text("operator WIP\n", encoding="utf-8")

        status = self.publish("composer.md")

        self.assertEqual(status, "feature maps: committed and pushed 1 file")
        self.assertEqual(self.remote_file("remote.txt"), "remote\n")
        self.assertEqual(
            self.remote_file("projects/chat-app/skills/verify-chat/features/composer.md"),
            "map\n",
        )
        self.assertEqual(self.git("rev-parse", "HEAD").stdout.strip(), self.remote_head())
        self.assertEqual(self.git("status", "--short").stdout, " M unstaged.txt\n")

    def test_concurrent_edit_to_the_same_map_is_merged_not_overwritten(self):
        readme = "projects/chat-app/skills/verify-chat/features/README.md"
        (self.repo / readme).write_text("# Feature maps\n\nLocal line.\n", encoding="utf-8")
        other = Path(self.tmp.name) / "other-clone-readme"
        self.run_git(other.parent, "clone", "-q", str(self.remote), str(other))
        self.run_git(other, "checkout", "-q", "main")
        self.run_git(other, "config", "user.email", "other@example.test")
        self.run_git(other, "config", "user.name", "Other")
        (other / readme).write_text("Remote title line.\n# Feature maps\n", encoding="utf-8")
        self.run_git(other, "commit", "-qam", "another session")
        self.run_git(other, "push", "-q", "origin", "main")

        status = self.publish("README.md")

        merged = "Remote title line.\n# Feature maps\n\nLocal line.\n"
        self.assertEqual(status, "feature maps: committed and pushed 1 file")
        self.assertEqual(self.remote_file(readme), merged)
        self.assertEqual((self.repo / readme).read_text(encoding="utf-8"), merged)
        self.assertEqual(self.git("rev-parse", "HEAD").stdout.strip(), self.remote_head())

    def test_overlapping_edit_to_the_same_map_is_refused(self):
        readme = "projects/chat-app/skills/verify-chat/features/README.md"
        (self.repo / readme).write_text("# Local title\n", encoding="utf-8")
        other = Path(self.tmp.name) / "other-clone-overlap"
        self.run_git(other.parent, "clone", "-q", str(self.remote), str(other))
        self.run_git(other, "checkout", "-q", "main")
        self.run_git(other, "config", "user.email", "other@example.test")
        self.run_git(other, "config", "user.name", "Other")
        (other / readme).write_text("# Remote title\n", encoding="utf-8")
        self.run_git(other, "commit", "-qam", "another session")
        self.run_git(other, "push", "-q", "origin", "main")
        remote_before = self.remote_head()

        with self.assertRaisesRegex(featuremaps.FeatureMapError, "README.md.*overlap"):
            self.publish("README.md")

        self.assertEqual(self.remote_head(), remote_before)
        self.assertEqual((self.repo / readme).read_text(encoding="utf-8"), "# Local title\n")

    def test_lost_push_race_retries_on_the_new_remote_head(self):
        marker = Path(self.tmp.name) / "raced"
        racer = Path(self.tmp.name) / "racer"
        self.run_git(racer.parent, "clone", "-q", str(self.remote), str(racer))
        self.run_git(racer, "checkout", "-q", "main")
        self.run_git(racer, "config", "user.email", "racer@example.test")
        self.run_git(racer, "config", "user.name", "Racer")
        hook = self.hooks / "pre-push"
        hook.write_text(
            "#!/bin/sh\n"
            f"[ -e '{marker}' ] && exit 0\n"
            f"touch '{marker}'\n"
            f"cd '{racer}' && echo raced > race.txt && git add race.txt"
            " && git commit -qm race && git push -q origin main\n",
            encoding="utf-8",
        )
        hook.chmod(0o755)
        (self.features / "composer.md").write_text("map\n", encoding="utf-8")

        status = self.publish("composer.md")

        self.assertEqual(status, "feature maps: committed and pushed 1 file")
        self.assertEqual(self.remote_file("race.txt"), "raced\n")
        self.assertEqual(
            self.remote_file("projects/chat-app/skills/verify-chat/features/composer.md"),
            "map\n",
        )
        self.assertEqual(self.git("rev-parse", "HEAD").stdout.strip(), self.remote_head())

    def test_leftover_local_map_commit_is_published_and_main_reconciled(self):
        leftover = self.features / "leftover.md"
        leftover.write_text("from a failed push\n", encoding="utf-8")
        self.git("add", str(leftover.relative_to(self.repo)))
        self.git("commit", "-qm", "feature maps: update chat-app/verify-chat")
        self.other_clone_pushes("remote.txt", "remote\n")
        (self.features / "composer.md").write_text("map\n", encoding="utf-8")

        status = self.publish("composer.md")

        self.assertEqual(status, "feature maps: committed and pushed 2 files")
        self.assertEqual(
            self.remote_file("projects/chat-app/skills/verify-chat/features/leftover.md"),
            "from a failed push\n",
        )
        self.assertEqual(self.git("rev-parse", "HEAD").stdout.strip(), self.remote_head())
        self.assertEqual(self.git("status", "--short").stdout, "")

    def test_no_changes_does_not_create_a_commit(self):
        before = self.git("rev-parse", "HEAD").stdout.strip()

        status = self.publish("README.md")

        self.assertEqual(status, "feature maps: already current")
        self.assertEqual(self.git("rev-parse", "HEAD").stdout.strip(), before)

    def test_failed_push_leaves_no_local_commit_and_retry_publishes(self):
        feature = self.features / "composer.md"
        feature.write_text("retry me\n", encoding="utf-8")
        hook = self.hooks / "pre-push"
        hook.write_text("#!/bin/sh\nexit 1\n", encoding="utf-8")
        hook.chmod(0o755)
        before = self.git("rev-parse", "HEAD").stdout.strip()

        with self.assertRaises(featuremaps.FeatureMapError):
            self.publish("composer.md")

        self.assertEqual(self.git("rev-parse", "HEAD").stdout.strip(), before)
        self.assertEqual(feature.read_text(encoding="utf-8"), "retry me\n")
        hook.unlink()

        status = self.publish("composer.md")

        self.assertEqual(status, "feature maps: committed and pushed 1 file")
        self.assertEqual(self.git("rev-parse", "HEAD").stdout.strip(), self.remote_head())
        self.assertEqual(
            self.remote_file(
                "projects/chat-app/skills/verify-chat/features/composer.md"
            ),
            "retry me\n",
        )

    def test_sync_hold_skips_without_fetch_commit_or_push(self):
        (self.repo / ".sync-hold").write_text("pause\n", encoding="utf-8")
        (self.features / "composer.md").write_text("held\n", encoding="utf-8")
        before = self.git("rev-parse", "HEAD").stdout.strip()

        status = self.publish("composer.md")

        self.assertEqual(status, "feature maps: .sync-hold present; skipped")
        self.assertEqual(self.git("rev-parse", "HEAD").stdout.strip(), before)
        self.assertEqual(self.git("status", "--short", "--", ".sync-hold").stdout, "?? .sync-hold\n")

    def test_detached_worktree_publishes_without_touching_main_checkout(self):
        (self.repo / "local-only.txt").write_text("local commit\n", encoding="utf-8")
        self.git("add", "local-only.txt")
        self.git("commit", "-qm", "unrelated local history")
        (self.repo / "unstaged.txt").write_text("main checkout WIP\n", encoding="utf-8")
        main_head = self.git("rev-parse", "HEAD").stdout.strip()
        main_status = self.git("status", "--short").stdout

        isolated = Path(self.tmp.name) / "isolated-hub"
        self.git("worktree", "add", "--quiet", "--detach", str(isolated), "origin/main")
        isolated_feature = (
            isolated
            / "projects"
            / "chat-app"
            / "skills"
            / "verify-chat"
            / "features"
            / "detached.md"
        )
        isolated_feature.write_text("detached publication\n", encoding="utf-8")

        status = featuremaps.publish(
            isolated, self.reg, "chat-app", "verify-chat", ["detached.md"]
        )

        self.assertEqual(status, "feature maps: committed and pushed 1 file")
        self.assertEqual(
            self.remote_file(
                "projects/chat-app/skills/verify-chat/features/detached.md"
            ),
            "detached publication\n",
        )
        self.assertEqual(self.git("rev-parse", "HEAD").stdout.strip(), main_head)
        self.assertEqual(self.git("status", "--short").stdout, main_status)

    def test_cli_isolated_publication_honors_the_operator_hub_hold(self):
        (self.repo / "registry.toml").write_text('''
[meta]
version = 1
default_profile = "full"
[categories]
verification = "Verification"
[profiles]
full = ["*"]
[skills.verify-chat]
category = "verification"
runtimes = ["claude", "codex"]
project = "chat-app"
''')
        self.git("add", "registry.toml")
        self.git("commit", "-qm", "complete CLI registry fixture")
        self.git("push", "-q", "origin", "main")
        isolated = Path(self.tmp.name) / "isolated-hub"
        self.git("worktree", "add", "--quiet", "--detach", str(isolated), "origin/main")
        for item in ("bin", "deezlib"):
            shutil.copytree(REPO / item, self.repo / item,
                            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        (self.repo / ".sync-hold").write_text("operator paused publication\n")
        feature = isolated / "projects/chat-app/skills/verify-chat/features/held.md"
        feature.write_text("held source-supported map\n")
        before_head = self.run_git(isolated, "rev-parse", "HEAD").stdout
        before_status = self.run_git(isolated, "status", "--porcelain=v1").stdout
        before_remote = self.run_git(
            self.remote.parent, f"--git-dir={self.remote}", "rev-parse", "main"
        ).stdout

        result = subprocess.run(
            [str(self.repo / "bin/deez"), "sync-feature-maps", "chat-app", "verify-chat",
             "held.md", "--repo", str(isolated)],
            capture_output=True, text=True, env=self.env,
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("hub .sync-hold present; skipped", result.stdout)
        self.assertEqual(self.run_git(isolated, "rev-parse", "HEAD").stdout, before_head)
        self.assertEqual(self.run_git(isolated, "status", "--porcelain=v1").stdout,
                         before_status)
        self.assertEqual(self.run_git(
            self.remote.parent, f"--git-dir={self.remote}", "rev-parse", "main"
        ).stdout, before_remote)


if __name__ == "__main__":
    unittest.main()

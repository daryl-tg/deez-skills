import hashlib
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from deezlib import featuremaps, registry


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

    def test_unrelated_unpushed_commit_blocks_publication(self):
        (self.repo / "other.txt").write_text("other\n", encoding="utf-8")
        self.git("add", "other.txt")
        self.git("commit", "-qm", "unrelated local commit")
        (self.features / "composer.md").write_text("map\n", encoding="utf-8")

        with self.assertRaisesRegex(featuremaps.FeatureMapError, "unrelated path.*other.txt"):
            self.publish("composer.md")
        self.assertNotEqual(
            self.run_git(
                self.remote.parent,
                f"--git-dir={self.remote}",
                "cat-file",
                "-e",
                "main:other.txt",
                check=False,
            ).returncode,
            0,
        )

    def test_remote_main_ahead_blocks_publication(self):
        other = Path(self.tmp.name) / "other-clone"
        self.run_git(other.parent, "clone", "-q", str(self.remote), str(other))
        self.run_git(other, "checkout", "-q", "main")
        self.run_git(other, "config", "user.email", "other@example.test")
        self.run_git(other, "config", "user.name", "Other")
        (other / "remote.txt").write_text("remote\n", encoding="utf-8")
        self.run_git(other, "add", "remote.txt")
        self.run_git(other, "commit", "-qm", "remote update")
        self.run_git(other, "push", "-q", "origin", "main")
        (self.features / "composer.md").write_text("map\n", encoding="utf-8")

        with self.assertRaisesRegex(featuremaps.FeatureMapError, "synchronize.*separately"):
            self.publish("composer.md")

    def test_no_changes_does_not_create_a_commit(self):
        before = self.git("rev-parse", "HEAD").stdout.strip()

        status = self.publish("README.md")

        self.assertEqual(status, "feature maps: already current")
        self.assertEqual(self.git("rev-parse", "HEAD").stdout.strip(), before)

    def test_failed_push_preserves_commit_and_retry_publishes_it(self):
        feature = self.features / "composer.md"
        feature.write_text("retry me\n", encoding="utf-8")
        hook = self.hooks / "pre-push"
        hook.write_text("#!/bin/sh\nexit 1\n", encoding="utf-8")
        hook.chmod(0o755)
        before = self.git("rev-parse", "HEAD").stdout.strip()

        with self.assertRaises(featuremaps.FeatureMapError):
            self.publish("composer.md")

        committed = self.git("rev-parse", "HEAD").stdout.strip()
        self.assertNotEqual(committed, before)
        self.assertEqual(feature.read_text(encoding="utf-8"), "retry me\n")
        hook.unlink()

        status = self.publish("composer.md")

        self.assertEqual(status, "feature maps: pushed existing commit")
        self.assertEqual(self.git("rev-parse", "HEAD").stdout.strip(), committed)
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


if __name__ == "__main__":
    unittest.main()

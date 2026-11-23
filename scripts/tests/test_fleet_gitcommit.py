"""Tests of game/fleet/gitcommit.py: a script's file is committed by path, or taken back so the clone stays clean
(requests ENT-472, ENT-473: rival-sedcards.md stood uncommitted for three hours and every member's install halted)."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import time
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "game", "fleet"))
import gitcommit  # noqa: E402


class CommitPathsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.git("init", "-q")
        (self.root / "governance").mkdir()
        (self.root / "governance" / "page.md").write_text("one\n", encoding="ascii")
        self.git("add", "-A")
        self.git("-c", "user.name=T", "-c", "user.email=t@example.invalid", "commit", "-q", "-m", "start")

    def git(self, *args):
        return subprocess.run(["git", "-C", str(self.root)] + list(args), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True).stdout

    def test_a_changed_file_is_committed_by_path_as_its_writer(self):
        (self.root / "governance" / "page.md").write_text("two\n", encoding="ascii")
        (self.root / "other.md").write_text("not mine\n", encoding="ascii")
        ok, text = gitcommit.commit_paths(self.root, ["governance/page.md"], "page: refresh", "Unity", tries=1, wait=0)
        self.assertTrue(ok, text)
        self.assertTrue(text.startswith("committed "))
        self.assertEqual(self.git("log", "-1", "--format=%an %s").strip(), "Unity page: refresh")
        self.assertEqual(self.git("status", "--porcelain").strip(), "?? other.md")              # nothing else touched
        self.assertEqual(gitcommit.commit_paths(self.root, ["governance/page.md"], "again", "Unity", tries=1, wait=0), (True, "unchanged"))

    def test_a_failed_commit_takes_the_file_back_and_says_why(self):
        hooks = self.root / ".git" / "hooks"
        (hooks / "pre-commit").write_text("#!/bin/sh\necho refused by a hook\nexit 1\n", encoding="ascii")
        os.chmod(hooks / "pre-commit", 0o755)
        (self.root / "governance" / "page.md").write_text("two\n", encoding="ascii")
        ok, text = gitcommit.commit_paths(self.root, ["governance/page.md"], "page: refresh", "Unity", tries=1, wait=0)
        self.assertFalse(ok)
        self.assertIn("taken back", text)
        self.assertEqual(self.git("status", "--porcelain").strip(), "")                          # the clone is clean again
        self.assertEqual((self.root / "governance" / "page.md").read_text(), "one\n")

    def test_a_lock_another_git_holds_for_a_moment_is_waited_for(self):
        lock = self.root / ".git" / "index.lock"
        lock.write_text("", encoding="ascii")
        threading.Timer(0.5, lambda: lock.unlink()).start()
        (self.root / "governance" / "page.md").write_text("three\n", encoding="ascii")
        ok, text = gitcommit.commit_paths(self.root, ["governance/page.md"], "page: refresh", "Unity", tries=4, wait=0.4)
        self.assertTrue(ok, text)
        self.assertEqual(self.git("status", "--porcelain").strip(), "")


if __name__ == "__main__":
    unittest.main()

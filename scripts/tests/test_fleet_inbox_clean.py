"""game/fleet/inbox.py never leaves the repository clone dirty (requests ENT-288), on a disposable data folder and repository. No engine, no network.

On 2026-11-21 19:53:56 UTC the service's commit of a contact log failed on another git's index.lock (a member's commit in
the same clone), the reset and the checkout after it failed on the same lock, and the log stood modified: every member's
fleet-build.sh install refused the clone, and every later run with --commit stopped on the file it had written itself.
"""

import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest


FLEET = Path(__file__).resolve().parents[2] / "game" / "fleet"


def load(name):
    spec = importlib.util.spec_from_file_location(name + "_under_test_clean", FLEET / (name + ".py"))
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


inbox = load("inbox")
NOW = 1_800_000_000


def msg(mid, sender, content, at):
    return {"id": mid, "sender": sender, "sender_id": "id-" + sender, "content": content, "timestamp_utc": at}


class CleanTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="fleet-inbox-clean-test-")
        self.addCleanup(self.temp.cleanup)
        self.data, self.root = Path(self.temp.name) / "data", Path(self.temp.name) / "repo"
        for folder in ("fleet", "intel", "station", "comms"):
            (self.data / folder).mkdir(parents=True)
        ships = [{"name": "Prime Directive", "status": "connected", "system": "home", "poi": "core", "docked": "base"}]
        (self.data / "fleet" / "fleet.json").write_text(json.dumps({"ships": ships}))
        (self.data / "fleet" / "flagships.json").write_text(json.dumps({"Prime Directive": {"admiral": "Unity"}}))
        self.answers = {}
        self.root.mkdir()
        self.git("init", "-q")
        self.git("commit", "-q", "--allow-empty", "-m", "start")
        self.saved = (inbox.LOCK_TRIES, inbox.LOCK_WAIT, inbox.COMMIT_LEFTOVERS) if hasattr(inbox, "LOCK_TRIES") else None
        if self.saved:
            inbox.LOCK_TRIES, inbox.LOCK_WAIT = 2, 0                # another git's lock: tried twice, no wait in a test
            self.addCleanup(self.restore)

    def restore(self):
        inbox.LOCK_TRIES, inbox.LOCK_WAIT, inbox.COMMIT_LEFTOVERS = self.saved

    def git(self, *args):
        return subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t"] + list(args), cwd=self.root, stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT, text=True)

    def status(self):
        return self.git("status", "--porcelain", "--untracked-files=all").stdout

    def say(self, mid, text, at):
        """One message to us in the system chat, read by one pass."""
        self.answers[("Prime Directive", "system")] = [msg(mid, "Drifter", text, at)]
        state = inbox.load_state(str(self.data))
        inbox.one_pass(str(self.data), state, look=lambda pilot, channel, after="": (self.answers.get((pilot, channel), []), ""), now=NOW, pause=0)

    def log(self):
        return self.root / "communications" / "contacts" / "no-faction.log"

    def test_a_run_without_commit_writes_nothing_into_the_repository(self):
        self.say("s1", "CLTV ships block the belt", "2026-11-21T19:50:00Z")
        answer = inbox.file_contacts(str(self.data), str(self.root), False)
        self.assertFalse((self.root / "communications").exists(), answer)        # the fault: the log was written and left uncommitted
        self.assertEqual(self.status(), "")
        self.assertIn("communications/contacts/no-faction.log: 1 new lines", answer)
        self.assertIn("Drifter | CLTV ships block the belt", answer)             # what --commit would write is printed
        out = Path(self.temp.name) / "scratch"
        answer = inbox.file_contacts(str(self.data), str(self.root), False, out=str(out))
        self.assertTrue((out / "no-faction.log").read_text().startswith("# Contact log: "), answer)
        self.assertTrue(inbox.file_contacts(str(self.data), str(self.root), False, out=str(self.root / "x")).startswith("HALT"))
        self.assertEqual((self.status(), (self.root / "x").exists()), ("", False))  # never into the repository, not even by --out

    def test_a_run_with_commit_commits_a_log_it_left_uncommitted(self):
        self.say("s1", "CLTV ships block the belt", "2026-11-21T19:50:00Z")
        self.assertTrue(inbox.file_contacts(str(self.data), str(self.root), True).startswith("contact logs committed"))
        files = inbox.contact_files(str(self.data))
        self.say("s2", "CLTV again", "2026-11-21T19:53:00Z")
        self.log().write_text(inbox.contact_files(str(self.data))["no-faction.log"], encoding="ascii")   # the state of 19:53:56 UTC
        answer = inbox.file_contacts(str(self.data), str(self.root), True)
        self.assertTrue(answer.startswith("contact logs committed: communications/contacts/no-faction.log"), answer)
        self.assertEqual(self.status(), "")
        self.log().write_text(files["no-faction.log"], encoding="ascii")          # an older text of its own, and a newer message
        self.say("s3", "CLTV a third time", "2026-11-21T20:10:00Z")
        self.assertIn("dry run, nothing written", inbox.file_contacts(str(self.data), str(self.root), True, dry_run=True))
        self.assertEqual(self.log().read_text(), files["no-faction.log"])          # the dry run wrote nothing
        self.assertTrue(inbox.file_contacts(str(self.data), str(self.root), True).startswith("contact logs committed"))
        self.assertEqual(self.status(), "")
        self.assertIn("CLTV a third time", self.git("show", "HEAD:communications/contacts/no-faction.log").stdout)

    def test_the_switch_off_stops_on_a_log_left_uncommitted_and_another_hands_file_always(self):
        self.say("s1", "CLTV ships block the belt", "2026-11-21T19:50:00Z")
        inbox.file_contacts(str(self.data), str(self.root), True)
        self.say("s2", "CLTV again", "2026-11-21T19:53:00Z")
        self.log().write_text(inbox.contact_files(str(self.data))["no-faction.log"], encoding="ascii")
        inbox.COMMIT_LEFTOVERS = False                                           # the switch off: as before r22
        answer = inbox.file_contacts(str(self.data), str(self.root), True)
        self.assertTrue(answer.startswith("HALT") and "COMMIT_LEFTOVERS is off" in answer, answer)
        inbox.COMMIT_LEFTOVERS = True
        (self.root / "communications" / "contacts" / "notes.log").write_text("someone else's work\n")
        answer = inbox.file_contacts(str(self.data), str(self.root), True)
        self.assertTrue(answer.startswith("HALT") and "notes.log" in answer, answer)   # another hand's file: nothing is written

    def test_a_commit_that_meets_another_gits_lock_leaves_the_clone_clean_and_the_next_run_files_it(self):
        self.say("s1", "CLTV ships block the belt", "2026-11-21T19:50:00Z")
        inbox.file_contacts(str(self.data), str(self.root), True)
        before = self.log().read_text()
        self.say("s2", "CLTV again", "2026-11-21T19:53:00Z")
        lock = self.root / ".git" / "index.lock"
        lock.write_text("")                                                      # a member's commit holds the clone's lock
        answer = inbox.file_contacts(str(self.data), str(self.root), True)
        self.assertTrue(answer.startswith("HALT: the commit failed"), answer)
        self.assertEqual((self.status(), self.log().read_text()), ("", before), answer)   # the fault: the log stood modified
        lock.unlink()
        self.assertTrue(inbox.file_contacts(str(self.data), str(self.root), True).startswith("contact logs committed"))
        self.assertEqual(self.status(), "")

    def test_a_log_staged_while_the_lock_stood_is_named_and_committed_by_the_next_run(self):
        self.say("s1", "CLTV ships block the belt", "2026-11-21T19:50:00Z")
        inbox.file_contacts(str(self.data), str(self.root), True)
        self.say("s2", "CLTV again", "2026-11-21T19:53:00Z")
        real, lock = inbox.git, self.root / ".git" / "index.lock"

        def late_lock(root, *args):                                              # the lock is taken between the add and the commit
            if "commit" in args:
                lock.write_text("")
            return real(root, *args)

        inbox.git = late_lock
        try:
            answer = inbox.file_contacts(str(self.data), str(self.root), True)
        finally:
            inbox.git = real
        self.assertIn(inbox.LEFT, answer)                                        # the service tries again within RETRY_EVERY
        lock.unlink()
        self.assertTrue(inbox.file_contacts(str(self.data), str(self.root), True).startswith("contact logs committed"))
        self.assertEqual(self.status(), "")


if __name__ == "__main__":
    unittest.main()

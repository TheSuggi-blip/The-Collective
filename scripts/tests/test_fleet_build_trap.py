"""scripts/fleet-build.sh puts its paths back when it is stopped (Oracle, errors.log ENT-115, DECISIONS Q75 (4)): a stopped
install (TERM, INT) and one past its own limit leave the clone as it was. Run on a scratch git repository (REPO=), whose
route gate is a stand-in that takes its time, as the whole suite does in the clone; no engine, no network."""

import os
from pathlib import Path
import shutil
import signal
import subprocess
import tempfile
import time
import unittest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "fleet-build.sh"
SLOW = "import sys, time\ntime.sleep(25)\nsys.exit(0)\n"          # the stand-in route gate: the install is cut while it runs


class StoppedInstallTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="fleet-build-trap-test-")
        self.addCleanup(self.temp.cleanup)
        top = Path(self.temp.name)
        self.repo, self.copy = top / "repo", top / "copy"
        (self.repo / "game" / "fleet").mkdir(parents=True)
        (self.repo / "scripts" / "tests").mkdir(parents=True)
        shutil.copy(ROOT / "game" / "fleet" / "division.py", self.repo / "game" / "fleet" / "division.py")      # who() reads the member
        (self.repo / "game" / "fleet" / "routes.py").write_text(SLOW, encoding="ascii")
        (self.repo / "game" / "fleet" / "census.py").write_text("LIVE = 1\n", encoding="ascii")
        (self.repo / "scripts" / "tests" / "test_census.py").write_text("# the test\n", encoding="ascii")
        self.git("init", "-q")
        self.git("add", "-A")
        self.git("-c", "user.name=T", "-c", "user.email=t@example.invalid", "commit", "-q", "-m", "start")
        self.env = dict(os.environ, REPO=str(self.repo), HERMES_SESSION_PROFILE="oracle", TMPDIR=self.temp.name)
        done = subprocess.run(["bash", str(SCRIPT), "tree", str(self.copy)], env=self.env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=60)
        self.assertIn("copy of", done.stdout)
        (self.copy / "game" / "fleet" / "census.py").write_text("LIVE = 2\n", encoding="ascii")
        (self.copy / "scripts" / "tests" / "test_census.py").write_text("# the test, changed\n", encoding="ascii")

    def git(self, *args):
        return subprocess.run(["git", "-C", str(self.repo)] + list(args), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True).stdout

    def install(self, **env):
        return subprocess.Popen(["bash", str(SCRIPT), "install", str(self.copy), "census.py: a change", "game/fleet/census.py", "scripts/tests/test_census.py"],
                                env=dict(self.env, **env), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    def copied(self, run, wait=20):
        """Waits until the install has copied its paths into the clone (the live file changed)."""
        end = time.time() + wait
        while time.time() < end and run.poll() is None:
            if (self.repo / "game" / "fleet" / "census.py").read_text() == "LIVE = 2\n":
                time.sleep(1)                                         # into the gates
                return True
            time.sleep(0.1)
        return False

    def assert_put_back(self, out):
        self.assertEqual(self.git("status", "--short"), "", out)
        self.assertEqual((self.repo / "game" / "fleet" / "census.py").read_text(), "LIVE = 1\n")
        self.assertEqual(len(self.git("log", "--format=%h").split()), 1)          # nothing committed

    def test_a_term_while_the_gates_run_puts_the_paths_back(self):
        run = self.install()
        self.assertTrue(self.copied(run))
        run.send_signal(signal.SIGTERM)                              # a caller's timeout (ENT-115: the call was cut at 500 s)
        out = run.communicate(timeout=20)[0]
        self.assertEqual(run.returncode, 1, out)
        self.assertIn("HALT: stopped (TERM) -- putting the paths back", out)
        self.assert_put_back(out)

    def test_an_interrupt_puts_the_paths_back_too(self):
        run = self.install()
        self.assertTrue(self.copied(run))
        run.send_signal(signal.SIGINT)
        out = run.communicate(timeout=20)[0]
        self.assertIn("HALT: stopped (INT) -- putting the paths back", out)
        self.assert_put_back(out)

    def test_its_own_limit_stops_the_install_and_puts_the_paths_back(self):
        begun = time.time()
        run = self.install(FLEET_BUILD_LIMIT="3")
        out = run.communicate(timeout=40)[0]
        self.assertLess(time.time() - begun, 15, out)                 # not the stand-in gate's 25 seconds
        self.assertIn("HALT: the install ran past its limit of 3 s (FLEET_BUILD_LIMIT)", out)
        self.assertIn("HALT: stopped (TERM) -- putting the paths back", out)
        self.assert_put_back(out)


if __name__ == "__main__":
    unittest.main()

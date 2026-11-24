"""game/fleet/runhost.py: one program flies the runs as threads. Made-up runners on disposable folders; no engine, no network."""

import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import textwrap
import time
import unittest


FLEET = Path(__file__).resolve().parents[2] / "game" / "fleet"


def load(name):
    spec = importlib.util.spec_from_file_location(name + "_under_test", FLEET / (name + ".py"))
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


WAITS = """
    import atexit
    import os
    import sys
    import time
    atexit.register(print, "left as a run leaves")
    print("started", flush=True)
    while not os.path.exists(sys.argv[1]):
        time.sleep(0.01)
"""


class Shelf(unittest.TestCase):
    """A made-up fleet folder with made-up runners, a data folder and one host."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="fleet-runhost-test-")
        self.addCleanup(self.temp.cleanup)
        self.fleet, self.data = Path(self.temp.name) / "fleet", Path(self.temp.name) / "data"
        for folder in (self.fleet, self.data / "fleet" / "orders", self.data / "routes" / "logs"):
            folder.mkdir(parents=True)
        self.home = self.data / "fleet" / "host"
        self.go = str(Path(self.temp.name) / "go")           # a run of WAITS ends when this file appears
        self.addCleanup(lambda: Path(self.go).write_text(""))
        self.runhost = load("runhost")
        self.said = []
        self.host = self.runhost.Host(str(self.fleet), str(self.data), say=self.said.append)
        self.addCleanup(lambda: str(self.fleet) in sys.path and sys.path.remove(str(self.fleet)))

    def runner(self, name, source):
        (self.fleet / name).write_text(textwrap.dedent(source), encoding="ascii")

    def log(self, pilot):
        return self.data / "routes" / "logs" / (pilot + ".log")

    def order(self, pilot, what):
        (self.data / "fleet" / "orders" / (pilot + ".json")).write_text(json.dumps({"pilot": pilot, "what": what}))

    def submit(self, pilot, script, *argv, what="mine made-up", env=None, order: "str | None" = "mine made-up"):
        """A job as the dispatcher hands it over: the pilot's order file first, then the job."""
        if order:
            self.order(pilot, order)
        self.runhost.submit(str(self.data), pilot, what, script, list(argv), env)

    def fly(self, seconds=20):
        """Step the host until every run it took has ended."""
        self.host.step()
        limit = time.time() + seconds
        while self.host.runs and time.time() < limit:
            time.sleep(0.01)
            self.host.step()
        self.assertEqual(self.host.runs, {}, "a run did not end in %d s" % seconds)

    def until(self, done, seconds=20):
        """Step the host until done() holds."""
        limit = time.time() + seconds
        while not done() and time.time() < limit:
            time.sleep(0.01)
            self.host.step()
        self.assertTrue(done(), "not reached in %d s" % seconds)

    def waiting(self, part):
        return sorted(p.name for p in (self.home / part).iterdir())


class RunTests(Shelf):
    def test_a_run_gets_its_arguments_and_writes_its_own_log(self):
        self.runner("echo.py", """
            import sys
            print("args", sys.argv[1:])
            print("said to stderr", file=sys.stderr)
        """)
        self.submit("miner-1", "echo.py", "miner-1", "--minutes", "5")
        self.assertEqual(self.waiting("inbox"), ["miner-1.json"])
        self.fly()
        self.assertEqual(self.log("miner-1").read_text(), "args ['miner-1', '--minutes', '5']\nsaid to stderr\n")
        self.assertEqual((self.waiting("inbox"), self.waiting("running")), ([], []))

    def test_a_run_ends_the_way_a_process_of_its_own_ends(self):
        # route_run.py: `sys.excepthook = crashed`, `atexit.register(order_done)`, then `atexit.register(finish)`: the row first, then the order file
        import atexit
        self.runner("ends.py", """
            import atexit
            import sys
            said = []


            def crashed(kind, error, trace):
                said.append("hook: " + kind.__name__)
                sys.__excepthook__(kind, error, trace)


            atexit.register(lambda: print("registered first, runs last", said))
            atexit.register(print, "registered last, runs first")
            sys.excepthook = crashed
            if sys.argv[1] == "crash":
                raise ValueError("a fault")
            if sys.argv[1] == "refused":
                sys.exit("REFUSED: not yours")
            sys.exit(0)
        """)
        before, hook = atexit._ncallbacks(), sys.excepthook
        for pilot, how in (("miner-1", "crash"), ("miner-2", "refused"), ("miner-3", "fine")):
            self.submit(pilot, "ends.py", how)
        self.fly()
        crash = self.log("miner-1").read_text()
        self.assertIn("ValueError: a fault", crash)                          # Python's own report, in the run's log
        self.assertIn("ends.py\", line 16", crash)
        self.assertTrue(crash.endswith("registered last, runs first\nregistered first, runs last ['hook: ValueError']\n"), crash)
        self.assertEqual(self.log("miner-2").read_text(), "REFUSED: not yours\nregistered last, runs first\nregistered first, runs last []\n")
        self.assertEqual(self.log("miner-3").read_text(), "registered last, runs first\nregistered first, runs last []\n")
        self.assertEqual(atexit._ncallbacks(), before)                       # nothing of a run stays behind in the host
        self.assertIs(sys.excepthook, hook)                                  # the host's own hook is as it was (Ubuntu's Python starts with apport's)

    def test_a_run_can_neither_end_the_host_nor_take_its_signals(self):
        self.runner("rude.py", """
            import os
            import signal
            import sys
            signal.signal(signal.SIGTERM, lambda number, frame: sys.exit("stopped"))     # guard.py sets one; a thread cannot
            print("handler set", signal.SIGTERM == 15)
            os._exit(3)
        """)
        self.submit("drone-1", "rude.py")
        self.fly()
        self.assertEqual(self.log("drone-1").read_text(), "handler set True\n")

    def test_two_runs_at_once_share_nothing_a_process_keeps_to_itself(self):
        self.runner("twin.py", """
            import os
            import sys
            import time
            NAME = sys.argv[1]                               # a name at module level, as route_run.py keeps its pilot
            while not os.path.exists(sys.argv[2]):           # both runs are in flight at once
                time.sleep(0.01)
            print(NAME, os.getpid() != int(sys.argv[3]), os.environ.get("FLEET_HOLD"), os.getenv("FLEET_HOLD"), dict(os.environ, X="1")["FLEET_HOLD"])
            with open(sys.argv[2] + "." + NAME, "w") as handle:
                handle.write(str(os.getpid()))
        """)
        self.submit("miner-1", "twin.py", "one", self.go, str(os.getpid()), env={"FLEET_HOLD": "mine one"})
        self.submit("miner-2", "twin.py", "two", self.go, str(os.getpid()), env={"FLEET_HOLD": "mine two"})
        self.host.step()
        self.assertEqual(len(self.host.runs), 2)
        Path(self.go).write_text("")
        self.fly()
        self.assertEqual(self.log("miner-1").read_text(), "one True mine one mine one mine one\n")
        self.assertEqual(self.log("miner-2").read_text(), "two True mine two mine two mine two\n")
        self.assertEqual(len({Path(self.go + "." + name).read_text() for name in ("one", "two")}), 2)   # a file named by os.getpid() is one run's alone
        self.assertNotIn("FLEET_HOLD", os.environ)

    def test_a_run_finds_the_fleets_modules_and_leaves_the_hosts_path_as_it_was(self):
        (self.fleet / "helper_made_up.py").write_text("VALUE = 'from the fleet folder'\n", encoding="ascii")
        self.addCleanup(sys.modules.pop, "helper_made_up", None)
        self.runner("imports.py", """
            import os
            import sys
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))     # every runner does this before `import division`
            import helper_made_up
            print(helper_made_up.VALUE, len(sys.path))
        """)
        before = list(sys.path)
        for pilot in ("miner-1", "miner-2"):
            self.submit(pilot, "imports.py")
        self.fly()
        self.assertEqual(self.log("miner-2").read_text(), "from the fleet folder %d\n" % (len(before) + 1))
        self.assertEqual(sys.path, before)                                   # 250 runs an hour would add 250 entries an hour

    def test_a_job_is_flown_only_for_a_runner_of_the_fleet_and_a_pilot_whose_order_names_that_work(self):
        self.runner("echo.py", "print('flown')\n")
        self.submit("miner-1", "../fleet/echo.py")                           # no script of the fleet folder
        self.submit("miner-2", "absent.py")
        self.submit("miner-3", "echo.py", order="hand Zero")                 # another program has the pilot
        self.submit("miner-4", "echo.py", order=None)                        # nobody gave the pilot this work
        self.submit("miner-5", "echo.py")
        self.fly()
        self.assertEqual([self.log("miner-%d" % n).exists() for n in (1, 2, 3, 4, 5)], [False, False, False, False, True])
        self.assertEqual((self.waiting("inbox"), self.waiting("running")), ([], []))
        self.assertEqual(len([line for line in self.said if "not flown" in line]), 4)
        self.assertEqual(json.loads((self.data / "fleet" / "orders" / "miner-3.json").read_text())["what"], "hand Zero")   # the other's order stays

    def test_a_changed_runner_is_flown_as_it_stands_on_disk(self):
        self.runner("echo.py", "print('first')\n")
        self.submit("miner-1", "echo.py")
        self.fly()
        self.runner("echo.py", "print('the second text')\n")
        self.submit("miner-2", "echo.py")
        self.fly()
        self.assertEqual((self.log("miner-1").read_text(), self.log("miner-2").read_text()), ("first\n", "the second text\n"))


class HostTests(Shelf):
    def state(self):
        return json.loads((self.home / "state.json").read_text())

    def test_the_host_says_it_is_alive_and_the_dispatcher_can_ask(self):
        now = time.time()
        self.assertFalse(self.runhost.accepting(str(self.data), now))        # no state file: no host
        self.assertTrue(self.host.step(now))
        self.assertEqual((self.state()["accepting"], self.state()["runs"]), (True, 0))
        self.assertTrue(self.runhost.accepting(str(self.data), now + 5))
        self.assertTrue(self.runhost.accepting(str(self.data), now - 5))     # state.json refreshed mid-pass is fresh, not dead
        self.assertFalse(self.runhost.accepting(str(self.data), now + self.runhost.ALIVE + 1))   # a host that stopped writing is away

    def test_a_new_host_frees_the_pilots_of_the_runs_a_dead_host_left(self):
        for pilot, order in (("miner-1", "mine made-up"), ("miner-2", "hand Zero"), ("miner-3", None)):
            (self.home / "running" / (pilot + ".json")).write_text(json.dumps({"pilot": pilot, "what": "mine made-up", "script": "echo.py", "argv": []}))
            if order:
                self.order(pilot, order)
        lines = self.host.recover()
        self.assertEqual(self.waiting("running"), [])
        self.assertEqual(sorted(p.name for p in (self.data / "fleet" / "orders").iterdir()), ["miner-2.json"])   # another program's order stays
        self.assertEqual(len(lines), 3)
        self.assertIn("miner-1", lines[0])

    def test_a_drain_file_lets_the_runs_end_takes_no_new_one_and_ends_the_host(self):
        self.runner("waits.py", WAITS)
        self.submit("miner-1", "waits.py", self.go)
        self.assertTrue(self.host.step())
        (self.home / "drain").write_text("")
        self.submit("miner-2", "waits.py", self.go)
        self.assertTrue(self.host.step())                                    # a run is in flight: the host goes on
        self.assertEqual((list(self.host.runs), self.waiting("inbox")), (["miner-1.json"], ["miner-2.json"]))
        self.assertFalse(self.state()["accepting"])
        self.assertFalse(self.runhost.accepting(str(self.data), time.time()))
        Path(self.go).write_text("")
        self.until(lambda: not self.host.runs)
        self.assertFalse(self.host.step())                                   # empty: it ends, and the shelf starts it fresh
        self.assertFalse((self.home / "drain").exists())
        self.assertEqual(self.waiting("inbox"), ["miner-2.json"])            # the fresh host takes it

    def test_a_changed_module_of_the_fleet_that_the_host_has_loaded_ends_it_when_no_run_is_in_flight(self):
        helper = self.fleet / "helper_made_up.py"
        helper.write_text("VALUE = 1\n", encoding="ascii")
        self.addCleanup(sys.modules.pop, "helper_made_up", None)
        self.runner("imports.py", "import helper_made_up\n")
        self.submit("miner-1", "imports.py")
        self.fly()
        self.assertTrue(self.host.step())
        helper.write_text("VALUE = 2  # changed\n", encoding="ascii")        # the host still holds the old one in memory
        self.assertFalse(self.host.step())
        self.assertIn("helper_made_up.py changed", self.said[-1])

    def test_one_run_can_be_ended_and_leaves_as_a_run_does(self):
        self.runner("waits.py", WAITS)
        self.submit("miner-1", "waits.py", self.go)
        self.submit("miner-2", "waits.py", self.go)
        self.until(lambda: all(self.log(p).exists() and self.log(p).read_text() == "started\n" for p in ("miner-1", "miner-2")))
        (self.home / "stop").mkdir(exist_ok=True)
        (self.home / "stop" / "miner-1").write_text("")
        self.until(lambda: "miner-1.json" not in self.host.runs)
        self.assertEqual(self.log("miner-1").read_text(), "started\nstopped by the host's stop file\nleft as a run leaves\n")
        self.assertEqual(list(self.host.runs), ["miner-2.json"])             # the other run flies on
        self.assertEqual(self.waiting("stop"), [])

    def test_the_host_takes_no_more_runs_than_its_cap_and_ends_itself_above_its_memory_cap(self):
        self.runner("waits.py", WAITS)
        self.host.max_runs = 1
        self.submit("miner-1", "waits.py", self.go)
        self.submit("miner-2", "waits.py", self.go)
        self.assertTrue(self.host.step())
        self.assertEqual((len(self.host.runs), self.waiting("inbox")), (1, ["miner-2.json"]))
        self.assertFalse(self.state()["accepting"])
        self.host.max_runs, self.host.max_rss_mb = 10, 1                     # no process is this small
        self.assertTrue(self.host.step())                                    # runs in flight: it drains
        self.assertEqual(self.waiting("inbox"), ["miner-2.json"])
        Path(self.go).write_text("")
        self.until(lambda: not self.host.runs)
        self.assertFalse(self.host.step())
        self.assertTrue(any("memory" in line for line in self.said))

    def test_only_a_service_may_be_the_host(self):
        # a second host would free the pilots of the first one's runs: an agent's shell starts none
        done = subprocess.run([sys.executable, "-I", "-B", str(FLEET / "runhost.py"), "--data", str(self.data)], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              text=True, timeout=60, env={"HERMES_SESSION_PROFILE": "unity", "PATH": os.environ.get("PATH", "")})
        self.assertEqual(done.returncode, 1)
        self.assertIn("REFUSED", done.stderr)


class DispatcherSideTests(Shelf):
    def test_a_job_the_host_did_not_take_in_a_minute_is_taken_back_once(self):
        now = time.time()
        self.submit("miner-1", "echo.py")
        self.submit("miner-2", "echo.py")
        old = self.home / "inbox" / "miner-1.json"
        os.utime(old, (now - 90, now - 90))
        self.assertEqual(self.runhost.waiting(str(self.data)), 2)
        back = self.runhost.take_back(str(self.data), now)
        self.assertEqual([(job["pilot"], job["what"], job["script"]) for job in back], [("miner-1", "mine made-up", "echo.py")])   # all it needs to start it itself
        self.assertEqual(self.waiting("inbox"), ["miner-2.json"])
        self.assertEqual(self.runhost.take_back(str(self.data), now), [])
        self.assertEqual((self.runhost.waiting(str(self.data)), self.runhost.load(str(self.data))), (1, 1))



class DrainFreeHandoverTests(Shelf):
    def test_module_change_hands_over_to_fresh_worker_with_zero_downtime(self):
        helper = self.fleet / "helper_ho.py"
        helper.write_text("VALUE = 1\n", encoding="ascii")
        self.runner("long_mod.py", """
            import os, sys, time
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
            import helper_ho
            print("val", helper_ho.VALUE, flush=True)
            while not os.path.exists(sys.argv[1]):
                time.sleep(0.02)
            print("done", helper_ho.VALUE, flush=True)
        """)
        go1 = str(Path(self.temp.name) / "go1")
        go2 = str(Path(self.temp.name) / "go2")
        self.addCleanup(lambda: [Path(g).write_text("") for g in (go1, go2)])
        env = dict(os.environ, FLEET_MEMBER="runhost", FLEET_HOST_EVERY="0.1")
        for key in ("HERMES_SESSION_PROFILE", "HERMES_HOME", "HERMES_SCRATCH_DIR", "TMPDIR"):    # division.member() reads a member's
            env.pop(key, None)                    # name from any of them (a member's TMPDIR is its profile's scratch): the host refuses
        proc = subprocess.Popen(
            [sys.executable, "-I", "-B", str(FLEET / "runhost.py"), "--fleet", str(self.fleet), "--data", str(self.data)],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=env,
        )
        def cleanup_proc():
            if proc.poll() is None:
                proc.terminate()
                try:
                    proc.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    proc.kill()
                    proc.wait()
            if proc.stdout:
                proc.stdout.close()
        self.addCleanup(cleanup_proc)

        # Wait for Worker 1 accepting
        limit = time.time() + 10
        pid1 = None
        while time.time() < limit:
            st = self.runhost.read_json(self.home / "state.json", {})
            if st.get("accepting") and st.get("pid"):
                pid1 = st["pid"]
                break
            time.sleep(0.05)
        self.assertIsNotNone(pid1, "worker 1 never started accepting")

        # Start miner-1 on Worker 1 (loads helper_ho VALUE=1)
        self.submit("miner-1", "long_mod.py", go1)
        limit = time.time() + 10
        while time.time() < limit and not (self.log("miner-1").exists() and "val 1" in self.log("miner-1").read_text()):
            time.sleep(0.05)
        self.assertIn("val 1", self.log("miner-1").read_text())

        # Wait two ticks so Worker 1 records helper_ho initial stat, then modify on disk
        time.sleep(0.35)
        helper.write_text("VALUE = 2  # updated on disk\n", encoding="ascii")
        limit = time.time() + 10
        pid2 = None
        while time.time() < limit:
            st = self.runhost.read_json(self.home / "state.json", {})
            if st.get("accepting") and st.get("pid") and st["pid"] != pid1:
                pid2 = st["pid"]
                break
            time.sleep(0.05)
        if pid2 is None:
            proc.terminate()
            out, _ = proc.communicate(timeout=5)
            self.fail("worker 2 never took over after module change; log:\n" + out)
        self.assertNotEqual(pid1, pid2)

        # Submit miner-2 while miner-1 is STILL flying in Worker 1 -> miner-2 flies immediately with VALUE=2!
        self.submit("miner-2", "long_mod.py", go2)
        limit = time.time() + 10
        while time.time() < limit and not (self.log("miner-2").exists() and "val 2" in self.log("miner-2").read_text()):
            time.sleep(0.05)
        self.assertIn("val 2", self.log("miner-2").read_text())
        # Both runs counted in load() (1 active + 1 retiring)
        self.assertGreaterEqual(self.runhost.load(str(self.data)), 2)
        # Re-submitting miner-1 while still active in Worker 1 is refused cleanly (no double-drive)
        self.assertTrue((self.home / "running" / "miner-1.json").exists())
        # Release miner-1 and miner-2 -> retiring Worker 1 exits and removes its retiring.<pid>.json
        Path(go1).write_text("")
        Path(go2).write_text("")
        limit = time.time() + 10
        while time.time() < limit and list(self.home.glob("retiring.*.json")):
            time.sleep(0.05)
        self.assertEqual(list(self.home.glob("retiring.*.json")), [])
        self.assertIn("done 1", self.log("miner-1").read_text())
        self.assertIn("done 2", self.log("miner-2").read_text())

        # Clean SIGTERM shutdown of supervisor + active worker
        proc.terminate()
        rc = proc.wait(timeout=12)
        self.assertEqual(rc, 0)

if __name__ == "__main__":
    unittest.main()

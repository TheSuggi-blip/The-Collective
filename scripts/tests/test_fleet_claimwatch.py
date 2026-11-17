"""game/fleet/claimwatch.py: which log lines make a claim, what holds a restart back, and that a pass restarts once. No engine, no network."""

import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import tempfile
import time
import unittest
from unittest import mock


FLEET = Path(__file__).resolve().parents[2] / "game" / "fleet"
CLAIM = "goal navigate-to-system failed: Another request for this account is already being processed. Try again shortly."


class ClaimWatchTests(unittest.TestCase):
    def setUp(self):
        spec = importlib.util.spec_from_file_location("claimwatch_under_test", FLEET / "claimwatch.py")
        self.watch = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.watch)
        asked = mock.patch.object(self.watch.division, "member", lambda: ("member", "Unity"))     # undone after the test: every test shares the module
        asked.start()
        self.addCleanup(asked.stop)
        self.temp = tempfile.TemporaryDirectory(prefix="fleet-claimwatch-test-")
        self.addCleanup(self.temp.cleanup)
        self.data = Path(self.temp.name)
        for folder in ("routes/logs", "fleet"):
            (self.data / folder).mkdir(parents=True)
        self.now = 1794880000.0
        self.fleet([{"name": "drone-1", "status": "connected", "hull": 75, "max_hull": 75}] * 20)
        self.calls = []

    def fleet(self, ships):
        (self.data / "fleet" / "fleet.json").write_text(json.dumps({"ships": ships}))

    def log(self, pilot, lines, now=None):
        """A run log whose lines are (seconds ago, text); the file was written when its newest line was."""
        now = self.now if now is None else now
        path = self.data / "routes" / "logs" / (pilot + ".log")
        path.write_text("".join("%s %s %s\n" % (time.strftime("%H:%M:%S", time.gmtime(now - ago)), pilot, text) for ago, text in lines))
        newest = now - min(ago for ago, _text in lines)
        os.utime(path, (newest, newest))

    def call(self, verb, path, body=None, timeout=30):
        self.calls.append((verb, path, body))
        if path == "/__gate/healthz":
            return 200, json.dumps({"gate": "ok", "engine": "running", "restart_in_s": 0})
        return 202, json.dumps({"engine": "restarting"})

    def act(self, now):
        said = io.StringIO()
        with contextlib.redirect_stdout(said):
            self.assertEqual(self.watch.main(["--act", "--data", str(self.data)], call=self.call, now=now), 0)
        return said.getvalue()

    def test_only_a_fresh_claim_answer_is_a_sighting(self):
        self.log("drone-1", [(30, CLAIM)])
        self.log("miner-2", [(30, "mining loop at belt: 409 A loop is running")])               # a runner waiting for a loop is no claim
        self.log("hauler-3", [(700, CLAIM), (20, "stop 2 of 4 reached")])                        # one answer twelve minutes ago in a run that goes on
        self.log("scout-4", [(40, "mining loop at belt: 409 This account is claimed by a fleet operation in progress")])
        found = self.watch.sightings(str(self.data), self.now)
        self.assertEqual(sorted(found), ["drone-1", "scout-4"])
        self.assertAlmostEqual(found["drone-1"][0], self.now - 30, delta=1)

    def test_three_passes_with_newer_answers_make_a_claim_and_one_answer_does_not(self):
        state = {}
        for minute, claimed in ((0, []), (5, []), (10, ["drone-1"])):
            now = self.now + minute * 60
            self.log("drone-1", [(20, CLAIM)], now)                                              # refused again shortly before every pass
            state, got = self.watch.step(state, self.watch.sightings(str(self.data), now), now)
            self.assertEqual(got, claimed, minute)
        state = {}
        self.log("trader-9", [(20, CLAIM)])                                                      # refused once at the start of a long run
        os.remove(self.data / "routes" / "logs" / "drone-1.log")
        for minute in (0, 5, 9):
            now = self.now + minute * 60
            os.utime(self.data / "routes" / "logs" / "trader-9.log", (now, now))                 # the run goes on writing
            state, got = self.watch.step(state, self.watch.sightings(str(self.data), now), now)
            self.assertEqual((got, state["seen"]["trader-9"]["passes"]), ([], 1))
        self.assertEqual(self.watch.sightings(str(self.data), self.now + 11 * 60), {})          # and after ten minutes it is no sighting at all

    def test_a_pilot_whose_next_run_started_its_log_anew_keeps_its_count(self):
        state = {}                                                                               # a mine run tries ten minutes, logs one line and ends
        for minute, line in ((0, CLAIM), (5, "mining loop at belt: started"), (11, CLAIM), (16, "mining loop at belt: started"), (22, CLAIM)):
            now = self.now + minute * 60
            self.log("miner-5", [(20, line)], now)
            state, got = self.watch.step(state, self.watch.sightings(str(self.data), now), now)
        self.assertEqual((got, state["seen"]["miner-5"]["passes"]), (["miner-5"], 3))
        now = self.now + 60 * 60                                                                 # and an hour without an answer forgets it
        state, got = self.watch.step(state, {}, now)
        self.assertEqual((got, state["seen"]), ([], {}))

    def claim(self, start=0):
        """Three passes five minutes apart, each after a newer answer; what each pass printed."""
        said = []
        for minute in (start, start + 5, start + 10):
            now = self.now + minute * 60
            self.log("drone-1", [(20, CLAIM)], now)
            said.append(self.act(now))
        return said

    def test_a_pass_restarts_the_engine_once_and_only_with_the_switch(self):
        self.assertEqual(self.claim(), ["", "", ""])                                             # claimed, and the switch file is not there
        self.assertFalse([c for c in self.calls if c[0] == "post"])
        (self.data / "fleet" / "claimwatch-on").write_text("")
        self.assertEqual(self.act(self.now + 17 * 60), "")                                       # the newest answer is seven minutes old: the claim may have ended
        self.assertFalse([c for c in self.calls if c[0] == "post"])
        self.log("drone-1", [(20, CLAIM)], self.now + 18 * 60)
        said = self.act(self.now + 18 * 60)
        posts = [c for c in self.calls if c[0] == "post"]
        self.assertEqual((len(posts), posts[0][1]), (1, "/__gate/engine/restart"))
        self.assertTrue(10 <= len(posts[0][2]["reason"]) <= 200)                                 # the gate's rule for a reason
        self.assertIn("the engine was restarted", said)
        self.assertIn("1 drone", said)
        self.assertNotIn("drone-1", said)                                                        # the line is delivered to a chat: no pilot is named
        record = json.loads((self.data / "fleet" / "claims.jsonl").read_text().splitlines()[-1])
        self.assertEqual((record["pilots"], record["did"]), (["drone-1"], "engine restart"))
        said = self.claim(start=30)                                                              # the claim shows again within two hours
        self.assertEqual(len([c for c in self.calls if c[0] == "post"]), 1)                      # never a second restart
        self.assertIn("a hand is needed", said[-1])

    def test_what_holds_a_restart_back(self):
        health = {"gate": "ok", "engine": "running", "restart_in_s": 0}
        back = lambda: self.watch.hold_back(str(self.data), health)
        self.assertEqual(back(), "")
        self.fleet([{"status": "connected", "hull": 75, "max_hull": 75}] * 17 + [{"status": "reconnecting", "hull": 75, "max_hull": 75}] * 3)
        self.assertIn("a wave", back())
        self.fleet([{"status": "connected", "hull": 75, "max_hull": 75}] * 19 + [{"status": "connected", "hull": 40, "max_hull": 75}])
        self.assertIn("under 70 percent hull", back())
        self.fleet([{"status": "connected", "hull": 75, "max_hull": 75}] * 20)
        health["restart_in_s"] = 900
        self.assertIn("frees a restart in 900 s", back())
        health["restart_in_s"] = 0
        (self.data / "fleet" / "STOP").write_text("")
        self.assertEqual(back(), "fleet/STOP exists")

    def test_only_the_fleet_admiral_or_a_service_acts(self):
        with mock.patch.object(self.watch.division, "member", lambda: ("member", "Zero")), self.assertRaises(SystemExit) as refused:
            self.watch.main(["--act", "--data", str(self.data)], call=self.call, now=self.now)
        self.assertIn("REFUSED", str(refused.exception))
        said = io.StringIO()
        with contextlib.redirect_stdout(said):
            self.assertEqual(self.watch.main(["check", "--data", str(self.data)], call=self.call, now=self.now), 0)   # every member may look
        self.assertIn("CLAIMWATCH | 0 pilot(s)", said.getvalue())


if __name__ == "__main__":
    unittest.main()

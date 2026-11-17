"""game/fleet/division.py and the gate client's lock, on disposable data folders: who is asking, who commands which ship, when a pilot may be driven."""

import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest


FLEET = Path(__file__).resolve().parents[2] / "game" / "fleet"


def load(name):
    spec = importlib.util.spec_from_file_location(name + "_under_test", FLEET / (name + ".py"))
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


division = load("division")
ZERO = {"HERMES_HOME": "/opt/data/profiles/zero"}
UNITY = {"HERMES_HOME": "/opt/data/profiles/unity"}


class Tree(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="fleet-division-test-")
        self.addCleanup(self.temp.cleanup)
        self.data = Path(self.temp.name)
        (self.data / "fleet" / "orders").mkdir(parents=True)
        (self.data / "fleet" / "flagships.json").write_text(json.dumps({"Zero Point": {"admiral": "Zero", "division": "Command", "role": "command"}}))

    def order(self, pilot, what, age=0):
        path = self.data / "fleet" / "orders" / (pilot + ".json")
        path.write_text(json.dumps({"pilot": pilot, "what": what}))
        os.utime(path, (time.time() - age, time.time() - age))

    def may(self, pilot, env):
        return division.may(pilot, str(self.data), env)


class MemberTests(Tree):
    def test_the_member_comes_from_what_hermes_sets_and_a_service_names_itself(self):
        self.assertEqual(division.member(ZERO), ("member", "Zero"))
        self.assertEqual(division.member({"TMPDIR": "/opt/data/profiles/apophis/cache/scratch"}), ("member", "Apophis"))
        self.assertEqual(division.member({"HERMES_HOME": "/opt/data", "FLEET_MEMBER": "dispatch"}), ("service", "dispatch"))
        self.assertEqual(division.member({"HERMES_HOME": "/opt/data"}), (None, ""))                     # the default profile is no member
        self.assertEqual(division.member({"HERMES_HOME": "/opt/data/profiles/stranger"}), (None, ""))
        self.assertEqual(division.member({"FLEET_MEMBER": "unity"}), (None, ""))                          # a member's name is not a service
        self.assertEqual(division.member({"HERMES_HOME": "/opt/data/profiles/zero", "FLEET_MEMBER": "dispatch"}), ("member", "Zero"))

    def test_a_ship_belongs_to_its_role_word_and_a_flagship_to_the_fleet_admiral(self):
        owners = [division.owner(p, str(self.data)) for p in ("miner-7", "trader-1", "hauler-20", "drone-3", "scout-9", "sentinel-4", "Zero Point", "Odd Name", "miner")]
        self.assertEqual(owners, ["Zero", "Mercury", "Apollo", "Apophis", "Oracle", "Unity", "Unity", "Unity", "Unity"])
        self.assertEqual([division.role_of(p, str(self.data)) for p in ("miner-7", "Zero Point", "Odd Name")], ["miner", "command", ""])


class MayTests(Tree):
    def test_an_admiral_drives_its_own_ships_and_the_fleet_admiral_every_ship(self):
        self.assertEqual(self.may("miner-7", ZERO), (True, "Zero commands miner-7"))
        ok, why = self.may("drone-3", ZERO)
        self.assertEqual((ok, why), (False, "drone-3 is commanded by Apophis, not by Zero (orders F1): ask in requests.log"))
        self.assertFalse(self.may("Zero Point", ZERO)[0])                                                # its own flagship flies with the command group
        self.assertTrue(self.may("drone-3", UNITY)[0])
        self.assertTrue(self.may("Zero Point", UNITY)[0])

    def test_a_shell_that_is_nobody_drives_nothing_and_a_service_drives_all(self):
        ok, why = self.may("miner-7", {"HERMES_HOME": "/opt/data"})
        self.assertFalse(ok)
        self.assertIn("no member of The Collective and no service", why)
        self.assertEqual(self.may("miner-7", {"FLEET_MEMBER": "dispatch"}), (True, "service dispatch"))

    def test_a_busy_pilot_is_left_alone_and_a_hand_hold_is_its_holders(self):
        self.order("miner-7", "mine mine-acubens")
        ok, why = self.may("miner-7", ZERO)
        self.assertFalse(ok)
        self.assertIn("miner-7 is busy: `mine mine-acubens`. Two programs never drive one pilot", why)
        self.assertFalse(self.may("miner-7", UNITY)[0])                                                  # the Fleet Admiral too
        self.assertTrue(self.may("miner-7", {"FLEET_MEMBER": "dispatch"})[0])                            # the dispatcher's own runner
        self.order("miner-7", "mine mine-acubens", age=division.ORDER_FRESH + 60)
        self.assertTrue(self.may("miner-7", ZERO)[0])                                                    # a dead order file frees the pilot
        self.order("miner-7", "hand Zero")
        self.assertTrue(self.may("miner-7", ZERO)[0])
        self.assertFalse(self.may("miner-7", UNITY)[0])                                                  # held by its Admiral: not taken from it
        self.order("miner-7", "birth")
        self.assertTrue(self.may("miner-7", dict(UNITY, FLEET_HOLD="birth"))[0])                         # a script that holds the pilot itself says so
        self.assertEqual(division.order_of("miner-8", str(self.data)), "")


class PlanTests(Tree):
    def plans(self, files):
        folder = self.data / "routes" / "plans"
        folder.mkdir(parents=True, exist_ok=True)
        for name, text in files.items():
            (folder / name).write_text(text, encoding="ascii")
        return division.load_plan(str(self.data))

    def test_one_file_per_role_kept_by_its_admiral(self):
        roles, owners, errors = self.plans({"miner.json": json.dumps({"role": "miner", "owner": "Zero", "routes": ["a", "park"]}),
                                            "sentinel.json": json.dumps({"role": "sentinel", "owner": "Unity", "routes": ["park"]})})
        self.assertEqual((roles, owners, errors), ({"miner": ["a", "park"], "sentinel": ["park"]}, {"miner": "Zero", "sentinel": "Unity"}, []))

    def test_a_wrong_plan_file_is_named(self):
        _roles, _owners, errors = self.plans({"miner.json": json.dumps({"role": "miner", "owner": "Apollo", "routes": ["park"]}),
                                              "drone.json": json.dumps({"role": "scout", "owner": "Apophis", "routes": ["park"]}),
                                              "pirate.json": json.dumps({"role": "pirate", "owner": "Unity", "routes": ["park"]}),
                                              "scout.json": "{broken"})
        self.assertEqual(len(errors), 4)
        self.assertIn("game/routes/plans/drone.json: needs `role` equal to the file name and a list `routes`", errors)
        self.assertIn("game/routes/plans/miner.json: `owner` must be Zero, who commands the miner ships", errors)
        self.assertTrue(any("pirate.json: `pirate` is no role of the fleet" in e for e in errors))
        self.assertTrue(any(e.startswith("game/routes/plans/scout.json: not readable as ASCII JSON") for e in errors))


class GateTests(unittest.TestCase):
    def run_gate(self, env, *args):
        base = {"PATH": os.environ.get("PATH", "/usr/bin:/bin")}
        return subprocess.run([sys.executable, "-I", "-B", str(FLEET / "gate.py")] + list(args), env=dict(base, **env),
                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=30)

    def test_reads_are_named_and_everything_else_is_a_command(self):
        gate = load("gate")
        self.assertEqual([gate.is_read(a) for a in ("get_status", "view_market", "view", "catalog", "info", "sell", "mine", "deposit", "jump", "scan", "craft")],
                         [True, True, True, True, True, False, False, False, False, False, False])

    def test_the_facility_cards_are_reads_and_a_build_is_not(self):
        gate = load("gate")
        self.assertEqual([gate.is_read(a) for a in ("types", "faction_list", "faction_owned", "owned", "upgrades", "faction_build", "build", "deploy_outpost")],
                         [True, True, True, True, True, False, False, False])

    def test_a_command_for_another_divisions_ship_is_refused_before_any_call(self):
        done = self.run_gate(ZERO, "goal", "drone-3", "dock-at", "{}")
        self.assertEqual(done.returncode, 1)
        self.assertEqual(done.stdout.strip(), "REFUSED: drone-3 is commanded by Apophis, not by Zero (orders F1): ask in requests.log")
        done = self.run_gate(ZERO, "raw", "trader-2", "sell", "{}")
        self.assertIn("REFUSED: trader-2 is commanded by Mercury", done.stdout)
        done = self.run_gate({"HERMES_HOME": "/opt/data"}, "raw", "miner-1", "mine")
        self.assertIn("REFUSED: this shell is no member", done.stdout)
        done = self.run_gate(ZERO, "post", "/accounts/register", "{}")
        self.assertIn("REFUSED: a call that names no pilot", done.stdout)
        done = self.run_gate(ZERO, "raw", "miner-1", "chat", '{"channel": "system", "content": "hello"}', "spacemolt_social")
        self.assertIn("REFUSED: a word to another player is the Fleet Admiral's", done.stdout)
        done = self.run_gate(ZERO, "post", "/accounts/miner-1/raw", '{"toolGroup": "spacemolt_social", "action": "forum_reply", "params": {}}')
        self.assertIn("REFUSED: a word to another player", done.stdout)
        done = self.run_gate(ZERO, "delete", "/accounts/drone-3/loop")
        self.assertIn("REFUSED: drone-3 is commanded by Apophis", done.stdout)


if __name__ == "__main__":
    unittest.main()

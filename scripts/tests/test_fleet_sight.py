"""game/fleet/sight.py on a disposable data folder: which places are looked at, what is kept, what is never written. No engine, no network."""

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[2] / "game" / "fleet" / "sight.py"
spec = importlib.util.spec_from_file_location("sight_under_test", SCRIPT)
assert spec is not None and spec.loader is not None
sight = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sight)


def ship(name, system="home", poi="belt", status="connected", **more):
    return dict({"name": name, "system": system, "poi": poi, "status": status, "jumping": False, "in_transit": False}, **more)


class Tree(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="fleet-sight-test-")
        self.addCleanup(self.temp.cleanup)
        self.data = Path(self.temp.name)
        for folder in ("fleet", "scouting"):
            (self.data / folder).mkdir()
        (self.data / "scouting" / "home.json").write_text("{\"read_at\": \"kept\"}", encoding="utf-8")
        self.asked = []
        self.near = {"belt": {"poi_id": "belt", "nearby": [{"username": "Rook", "faction_tag": "HEXC", "ship_class": "liminal", "in_combat": True},
                                                          {"username": "miner-2", "faction_tag": "CLTV", "ship_class": "threshold"}],
                              "pirates": [{"id": "p1"}], "creatures": [{"species": "veil_ray"}, {"species": "veil_ray"}]},
                     "gate": {"poi_id": "gate", "nearby": []}}

    def fleet(self, rows):
        (self.data / "fleet" / "fleet.json").write_text(json.dumps({"ships": rows}), encoding="utf-8")

    def ask(self, pilot, action):
        self.asked.append((pilot, action))
        if action == "get_nearby":
            return self.near.get(next(r["poi"] for r in self.rows if r["name"] == pilot), {})
        if action == "get_system":
            return {"system": {"id": "far", "name": "Far", "pois": [{"id": "gate", "type": "jump_gate"}]}}
        return {"poi": {"id": "gate", "resources": []}}

    def run_pass(self, rows, seen, now=10_000):
        self.rows = rows
        self.fleet(rows)
        return sight.one_pass(str(self.data), self.ask, seen, now)

    def read(self, name):
        return json.loads((self.data / name).read_text(encoding="utf-8"))


class LookTests(Tree):
    def test_one_ship_per_place_and_never_a_ship_that_cannot_look(self):
        rows = [ship("miner-1"), ship("miner-2"), ship("scout-1", poi="gate"), ship("drone-1", poi="nebula", jumping=True),
                ship("drone-2", poi="cloud", in_transit=True), ship("drone-3", poi="rift", status="disconnected"), ship("drone-4", poi="")]
        self.assertEqual(sight.looks(rows, {}, 10_000), [("home", "belt", "miner-1"), ("home", "gate", "scout-1")])

    def test_a_place_rests_ten_minutes_and_a_pass_has_a_cap(self):
        rows = [ship("miner-1"), ship("scout-1", poi="gate")]
        self.assertEqual(sight.looks(rows, {"home:belt": 9_500}, 10_000), [("home", "gate", "scout-1")])
        self.assertEqual(sight.looks(rows, {"home:belt": 9_400, "home:gate": 9_300}, 10_000), [("home", "gate", "scout-1"), ("home", "belt", "miner-1")])
        many = [ship("s-%d" % n, poi="p%02d" % n) for n in range(20)]
        self.assertEqual(len(sight.looks(many, {}, 10_000)), sight.PER_PASS)


class PassTests(Tree):
    def test_a_stranger_is_kept_and_an_own_pilot_never(self):
        seen = {}
        said = self.run_pass([ship("miner-1"), ship("miner-2")], seen)
        self.assertEqual(said, ["home:belt 1 pilot(s), 1 pirate(s)"])
        self.assertEqual(self.asked, [("miner-1", "get_nearby")])                                  # home has a scouting file: no system read
        met = self.read("intel/met.json")
        self.assertEqual(sorted(met), ["Rook"])
        self.assertEqual({k: met["Rook"][k] for k in ("faction_tag", "ship_class", "system", "poi", "times")},
                         {"faction_tag": "HEXC", "ship_class": "liminal", "system": "home", "poi": "belt", "times": 1})
        self.assertEqual(met["Rook"]["first"], met["Rook"]["last"])
        self.assertEqual(met["Rook"]["in_combat_at"], met["Rook"]["last"])
        line = json.loads((self.data / "intel" / "sightings.jsonl").read_text(encoding="utf-8"))
        self.assertEqual({k: line[k] for k in ("system", "poi", "pilots", "pirates", "creatures")},
                         {"system": "home", "poi": "belt", "pilots": ["Rook"], "pirates": 1, "creatures": 2})
        self.assertEqual(self.read("scouting/home.json"), {"read_at": "kept"})                     # the census's file is never overwritten
        self.assertEqual(self.run_pass([ship("miner-1")], seen, now=10_100), [])                   # the place rests
        self.run_pass([ship("miner-1")], seen, now=10_700)
        again = self.read("intel/met.json")["Rook"]
        self.assertEqual((again["times"], again["first"] < again["last"]), (2, True))

    def test_a_system_nobody_read_gets_its_first_read(self):
        said = self.run_pass([ship("scout-1", system="far", poi="gate")], {})
        self.assertEqual(said, ["far: first read of the system saved"])
        self.assertEqual(self.asked, [("scout-1", "get_nearby"), ("scout-1", "get_system"), ("scout-1", "get_poi")])
        read = self.read("scouting/far.json")
        self.assertEqual((read["system"]["id"], sorted(read["pois"]), read["source"]), ("far", ["gate"], "game/fleet/sight.py, an own ship passing"))
        self.assertTrue(read["read_at"].endswith("Z"))

    def test_no_answer_a_moved_ship_and_the_stop_file_write_nothing(self):
        self.near["belt"] = {}
        self.assertEqual(self.run_pass([ship("miner-1")], {}), [])
        self.near["belt"] = {"poi_id": "elsewhere", "nearby": [{"username": "Rook"}]}
        self.assertEqual(self.run_pass([ship("miner-1")], {}), [])
        self.assertFalse((self.data / "intel").exists())
        (self.data / "fleet" / "STOP").write_text("")
        self.asked.clear()
        self.assertEqual(self.run_pass([ship("miner-1")], {}), [])
        self.assertEqual(self.asked, [])

    def test_a_system_answer_for_another_system_is_not_saved(self):
        self.rows = [ship("scout-1", system="other", poi="gate")]
        self.fleet(self.rows)
        sight.one_pass(str(self.data), self.ask, {}, 10_000)                                       # get_system answers for `far`
        self.assertFalse((self.data / "scouting" / "other.json").exists())


if __name__ == "__main__":
    unittest.main()

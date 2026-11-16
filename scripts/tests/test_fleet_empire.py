"""game/fleet/empire.py on disposable folders: what one reading holds, the ladder's rent cards, the page that names no pilot and no balance. No engine, no network."""

import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


REPO = Path(__file__).resolve().parents[2]


def load(name):
    spec = importlib.util.spec_from_file_location(name + "_under_test", REPO / "game" / "fleet" / (name + ".py"))
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


empire = load("empire")
INFO = {"id": "f1", "name": "The Test", "tag": "TEST", "leader_username": "Lead Ship", "member_count": 2, "members_limit": 50, "owned_bases": 1, "at_war": False,
        "created_at": "2026-11-15T18:09:32Z", "members": [{"username": "Lead Ship", "role": "Leader"}, {"username": "miner-1", "role": "Member"}]}
OWNED = {"facilities": [{"facility_id": "x1", "type_id": "hiring_board", "name": "Hiring Board", "level": 1, "base_id": "far_base", "system_id": "far", "status": "active", "rent_per_cycle": 26}],
         "faction_rent": {"facilities": 1, "total_rent_per_cycle": 26, "est_rent_per_day": 2246}}
CATALOG = {"version": "9.9.9", "facilities": [
    {"id": "hiring_board", "name": "Hiring Board", "category": "faction", "level": 1, "build_cost": 75000, "faction_cap": 50, "faction_service_type": "faction_recruitment",
     "requires_service_type": "faction_storage", "build_materials": [{"item_id": "steel_plate", "quantity": 75}]},
    {"id": "faction_lockbox", "name": "Faction Lockbox", "category": "faction", "level": 1, "build_cost": 200000, "faction_cap": 100000, "faction_service_type": "faction_storage",
     "build_materials": [{"item_id": "steel_plate", "quantity": 200}, {"item_id": "circuit_board", "quantity": 50}]},
    {"id": "smelter", "name": "Smelter", "category": "production", "level": 1, "build_cost": 1}]}


class Tree(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="fleet-empire-test-")
        self.addCleanup(self.temp.cleanup)
        self.root, self.data = Path(self.temp.name) / "repo", Path(self.temp.name) / "data"
        for folder in ("fleet", "station", "catalog"):
            (self.data / folder).mkdir(parents=True)
        (self.root / "game" / "map").mkdir(parents=True)
        (self.root / "governance").mkdir(parents=True)
        put = lambda rel, value: (self.data / rel).write_text(json.dumps(value), encoding="utf-8")
        put("fleet/flagships.json", {"Lead Ship": {"of": "Unity", "role": "command"}, "Other Ship": {"of": "Zero", "role": "command"}})
        put("fleet/fleet.json", {"ships": [{"name": "Lead Ship"}, {"name": "miner-1"}, {"name": "miner-2"}]})
        put("station/stations.json", [{"name": "Test Rock", "type": "outpost", "system": "wild", "tag": "TEST", "condition": "thriving", "services": []},
                                      {"name": "Their Hub", "type": "station", "system": "wild", "tag": "THEM", "services": ["market"]},
                                      {"name": "Empire Hub", "type": "station", "system": "far", "tag": "", "services": []}])
        put("station/map.json", {"systems": [{"id": "wild", "name": "Wild", "empire": "", "jumps": 4}, {"id": "far", "name": "Far", "empire": "voidborn", "jumps": 2}]})
        put("station/feed.json", {"factions": {"TEST": {"allies": ["FRND"], "enemies": [], "wars": []}}})
        put("catalog/9.9.9.json", CATALOG)
        (self.root / "game" / "map" / "sites.tsv").write_text("# a comment\nsystem\tpoi\tstatus\tproposed_by\tnote\nwild\t-\tcandidate\tOracle\tbeside the ice\nnowhere\tp1\tdropped\tOracle\tgone\n")
        self.calls = []

    def see(self, answers):
        def fake(pilot, group, action, params=None):
            self.calls.append((pilot, group, action, (params or {}).get("facility_type", "")))
            found = answers.get((group, action))
            if callable(found):
                found = found(params or {})
            return (found, "") if found is not None else (None, "no answer")
        return fake

    def answers(self):
        return {("spacemolt_faction", "info"): INFO, ("spacemolt_facility", "faction_owned"): OWNED, ("spacemolt_faction", "garages"): {"station_count": 0, "total_ships": 0},
                ("spacemolt_faction", "tax_estimate"): {"domicile": "voidborn", "income_tax_total": 0},
                ("spacemolt_facility", "types"): lambda p: {"type_id": p["facility_type"], "rent_per_cycle": {"hiring_board": 26, "faction_lockbox": 69}[p["facility_type"]]}}


class CollectTests(Tree):
    def test_one_reading_holds_the_faction_its_bases_its_offices_the_territory_and_the_sites(self):
        state, notes = empire.collect(str(self.data), str(self.root), see=self.see(self.answers()), pause=0, now=0)
        self.assertEqual(notes, [])
        self.assertEqual(state["faction"], {"id": "f1", "name": "The Test", "tag": "TEST", "leader": "Lead Ship", "member_count": 2, "members_limit": 50, "treasury": None,
                                            "owned_bases": 1, "at_war": False, "created_at": "2026-11-15T18:09:32Z"})
        self.assertEqual(state["members"], [{"pilot": "Lead Ship", "role": "Leader"}, {"pilot": "miner-1", "role": "Member"}])
        self.assertEqual(state["fleet"], {"ships": 3, "in_faction": 2})
        self.assertEqual([(b["name"], b["kind"], b["system"]) for b in state["bases"]], [("Test Rock", "outpost", "wild")])       # the public list's rows with our tag, no other
        self.assertEqual(state["facilities"], [{"facility_id": "x1", "type": "hiring_board", "name": "Hiring Board", "level": 1, "base": "far_base", "system": "far",
                                                "status": "active", "rent_per_cycle": 26}])
        self.assertEqual(state["rent"], {"facilities": 1, "per_cycle": 26, "per_day": 2246, "arrears": None})
        self.assertEqual(state["territory"], [{"system": "wild", "claim": "outpost", "note": "Test Rock"}, {"system": "far", "claim": "office", "note": "at far_base"}])
        self.assertEqual([(s["system"], s["poi"], s["status"], s["space"], s["jumps"], s["stations"]) for s in state["sites"]],
                         [("wild", "", "candidate", "lawless", 4, ["Test Rock (outpost, TEST)", "Their Hub (station, THEM)"]), ("nowhere", "p1", "dropped", "not on the chart", None, [])])
        self.assertEqual(state["relations"], {"allies": ["FRND"], "enemies": [], "wars": []})
        self.assertEqual({c[0] for c in self.calls}, {"Lead Ship"})                                        # the Fleet Admiral's flagship, no other pilot

    def test_the_ladder_takes_the_catalogs_faction_types_and_reads_each_rent_card_once_per_catalog(self):
        see = self.see(self.answers())
        state, _notes = empire.collect(str(self.data), str(self.root), see=see, pause=0)
        self.assertEqual([(r["type"], r["line"], r["cost"], r["rent_per_cycle"], r["cap"]) for r in state["ladder"]],
                         [("faction_lockbox", "faction_storage", 200000, 69, 100000), ("hiring_board", "faction_recruitment", 75000, 26, 50)])      # storage first; no production line
        self.assertEqual((state["ladder_of"], sum(1 for c in self.calls if c[2] == "types")), ("9.9.9", 2))
        empire.save(str(self.data), state)
        empire.collect(str(self.data), str(self.root), see=see, pause=0)
        self.assertEqual(sum(1 for c in self.calls if c[2] == "types"), 2)                                  # the same catalog: no card is read again
        empire.collect(str(self.data), str(self.root), see=see, pause=0, force=True)
        self.assertEqual(sum(1 for c in self.calls if c[2] == "types"), 4)
        (self.data / "catalog" / "10.0.0.json").write_text(json.dumps(dict(CATALOG, version="10.0.0")))
        again, _notes = empire.collect(str(self.data), str(self.root), see=see, pause=0)
        self.assertEqual((again["ladder_of"], sum(1 for c in self.calls if c[2] == "types")), ("10.0.0", 6))       # a new release: every card again

    def test_a_reading_that_fails_keeps_the_last_one_and_says_so(self):
        first, _notes = empire.collect(str(self.data), str(self.root), see=self.see(self.answers()), pause=0)
        empire.save(str(self.data), first)
        state, notes = empire.collect(str(self.data), str(self.root), see=self.see({}), pause=0)
        self.assertEqual((state["faction"], state["members"], state["facilities"], state["rent"]), (first["faction"], first["members"], first["facilities"], first["rent"]))
        self.assertEqual(len(notes), 2)
        self.assertIn("faction info not read (no answer): the last reading stays", notes[0])
        self.assertEqual([r["rent_per_cycle"] for r in state["ladder"]], [69, 26])                          # a card that was read once is kept

    def test_a_base_count_that_differs_from_the_public_list_is_named(self):
        answers = self.answers()
        answers[("spacemolt_faction", "info")] = dict(INFO, owned_bases=2)
        _state, notes = empire.collect(str(self.data), str(self.root), see=self.see(answers), pause=0)
        self.assertEqual(len(notes), 1)
        self.assertIn("the game counts 2 base(s) of ours, the public list of stations shows 1", notes[0])

    def test_nothing_but_a_view_is_sent(self):
        self.assertEqual(empire.look("Lead Ship", "spacemolt_facility", "faction_build", {"facility_type": "hiring_board"}),
                         (None, "refused: `spacemolt_facility faction_build` is no view of this script"))
        self.assertEqual(empire.look("Lead Ship", "spacemolt_storage", "deposit")[0], None)


class PageTests(Tree):
    def test_the_page_names_no_pilot_and_no_balance_and_is_the_same_page_while_the_facts_are(self):
        answers = self.answers()
        answers[("spacemolt_faction", "info")] = dict(INFO, treasury=123456)
        state, _notes = empire.collect(str(self.data), str(self.root), see=self.see(answers), pause=0, now=0)
        text = empire.page(state)
        self.assertEqual(state["faction"]["treasury"], 123456)
        for private in ("Lead Ship", "miner-1", "123456", "123,456"):
            self.assertNotIn(private, text)
        self.assertIn("| Members | 2 of a limit of 50 |", text)
        self.assertIn("| Ships of the fleet in it | 2 of 3 |", text)
        self.assertIn("| Outposts | 1 of 8 |", text)
        self.assertIn("| Test Rock | outpost | `wild` | thriving | -- |", text)
        self.assertIn("| `far` | office | at far_base |", text)
        self.assertIn("| `wild` | Wild | lawless | 4 | Test Rock (outpost, TEST), Their Hub (station, THEM) | candidate | Oracle | beside the ice |", text)
        self.assertIn("| faction_recruitment | 1 | Hiring Board (`hiring_board`) | 75,000 | 75 steel_plate | 26 | 2,246 | 50 members |", text)
        self.assertTrue(all(ord(c) < 128 for c in text))
        later = empire.page(dict(state, written_at="2026-11-17T00:00:00Z"))
        self.assertNotEqual(later, text)
        self.assertEqual(empire.body(later), empire.body(text))                                           # the reading's time alone is no change
        self.assertNotEqual(empire.body(empire.page(dict(state, faction=dict(state["faction"], member_count=3)))), empire.body(text))

    def test_write_and_check_keep_the_file_and_show_prints_the_same_facts(self):
        state, _notes = empire.collect(str(self.data), str(self.root), see=self.see(self.answers()), pause=0)
        run = lambda *args: subprocess.run([sys.executable, "-I", "-B", str(REPO / "game" / "fleet" / "empire.py")] + list(args) + ["--root", str(self.root), "--data", str(self.data)],
                                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env={"FLEET_MEMBER": "Zero", "PATH": "/usr/bin:/bin"})
        self.assertIn("no reading on disk", run("check").stdout)
        self.assertEqual(run("show").returncode, 1)
        empire.save(str(self.data), state)
        self.assertEqual((run("check").returncode, run("write").stdout.strip(), run("check").stdout.strip()),
                         (1, "governance/empire.md: written", "governance/empire.md: current"))
        empire.save(str(self.data), dict(state, written_at="2026-11-17T00:00:00Z"))
        self.assertEqual(run("write").stdout.strip(), "governance/empire.md: current")                     # a new reading with the same facts rewrites nothing
        shown = run("show").stdout
        self.assertIn("Members                    2 of a limit of 50", shown)
        self.assertIn("SITES | 2 proposed", shown)
        self.assertIn("faction_recruitment  tier 1 Hiring Board (`hiring_board`)", shown)
        self.assertIn("REFUSED: reading the faction through the leader's flagship is the Fleet Admiral's", run("collect").stdout)      # an Admiral's shell reads the result, not the game


if __name__ == "__main__":
    unittest.main()

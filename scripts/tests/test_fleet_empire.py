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


class SiteTests(Tree):
    """Q67 (1), Suggi 2026-11-17: what the database holds gets there by itself, never by a hand; a planned site is one command."""

    def git(self, *args):
        return subprocess.run(["git", "-C", str(self.root)] + list(args), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True).stdout

    def setUp(self):
        super().setUp()
        self.git("init", "-q")
        self.git("add", "-A")
        self.git("-c", "user.name=T", "-c", "user.email=t@example.invalid", "commit", "-q", "-m", "start")

    def test_a_member_proposes_the_fleet_admiral_chooses_and_each_line_is_one_commit(self):
        ok, line = empire.set_site(str(self.root), str(self.data), "Zero", "nowhere-at-all", "candidate")
        self.assertEqual((ok, line.startswith("REFUSED: `nowhere-at-all` is no system")), (False, True))
        ok, line = empire.set_site(str(self.root), str(self.data), "Zero", "far", "chosen")
        self.assertEqual((ok, "the Fleet Admiral chooses" in line), (False, True))          # rule F33
        ok, line = empire.set_site(str(self.root), str(self.data), "Zero", "far", "candidate", note="two\tbelts")
        self.assertTrue(ok, line)
        rows = {r["system"]: r for r in empire.site_rows(str(self.root))}
        self.assertEqual((rows["far"]["status"], rows["far"]["proposed_by"], rows["far"]["note"]), ("candidate", "Zero", "two belts"))
        self.assertEqual((self.git("log", "-1", "--format=%an").strip(), self.git("status", "--porcelain")), ("Zero", ""))
        ok, line = empire.set_site(str(self.root), str(self.data), "Oracle", "wild", "candidate", note="mine now")
        self.assertEqual((ok, "proposed by Oracle" in line or ok), (True, True))            # its own line: rewritten
        ok, line = empire.set_site(str(self.root), str(self.data), "Zero", "wild", "candidate", note="mine")
        self.assertEqual((ok, "another member's line" in line), (False, True))
        ok, line = empire.set_site(str(self.root), str(self.data), "Unity", "wild", "chosen", poi="belt_1")
        self.assertTrue(ok, line)
        rows = {r["system"]: r for r in empire.site_rows(str(self.root))}
        self.assertEqual((rows["wild"]["status"], rows["wild"]["proposed_by"], rows["wild"]["poi"], rows["wild"]["note"]), ("chosen", "Oracle", "belt_1", "mine now"))
        self.assertEqual(len(empire.site_rows(str(self.root))), 3)                          # replaced, never a second line
        (self.root / "game" / "map" / "sites.tsv").write_text("half an edit\n")
        ok, line = empire.set_site(str(self.root), str(self.data), "Unity", "far", "dropped")
        self.assertEqual((ok, "not committed" in line), (False, True))


class MemberPageTests(Tree):
    """Requests ENT-262 (Zero): the faction's whole member list, not its first page. `info` answers one page (the help:
    paginated, default limit 50, max 100; `offset` and `limit` page through it; members_offset, members_limit and
    members_truncated describe that page). The fake below gives at most 50 a page, whatever is asked."""

    ROSTER = [{"username": "Lead Ship", "role": "Leader"}] + [{"username": "miner-%d" % n, "role": "Member"} for n in range(1, 94)]     # 94 members

    def paged(self, fail_at=None, ignore_offset=False):
        asked = []

        def info(params):
            offset, limit = int(params.get("offset") or 0), min(int(params.get("limit") or 50), 50)
            asked.append((params.get("offset"), params.get("limit")))
            if fail_at is not None and offset >= fail_at:
                return None
            start = 0 if ignore_offset else offset
            page = self.ROSTER[start:start + limit]
            return dict(INFO, member_count=len(self.ROSTER), members=page, members_offset=start, members_limit=limit,
                        members_truncated=start + len(page) < len(self.ROSTER))
        answers = self.answers()
        answers[("spacemolt_faction", "info")] = info
        return answers, asked

    def test_every_page_of_the_member_list_goes_into_members_and_the_table_faction_members(self):
        answers, asked = self.paged()
        state, notes = empire.collect(str(self.data), str(self.root), see=self.see(answers), pause=0, now=0)
        self.assertEqual(notes, [])
        self.assertEqual(len(state["members"]), 94)                                      # the first page alone held 50
        self.assertEqual(state["members"][-1], {"pilot": "miner-93", "role": "Member"})
        self.assertEqual(asked, [(None, 100), (50, 100)])                                # the page size asked, then the next page by offset
        self.assertIn({"pilot": "miner-60", "role": "Member"}, state["members"])          # a miner of the second page reads as seated
        self.assertEqual(state["fleet"]["in_faction"], 3)                                # the three ships of the fleet file
        empire.save(str(self.data), state)
        store = load("store")
        rows = store.read_empire(self.data / "empire" / "empire.json", {})["faction_members"]
        self.assertEqual((len(rows), rows[93]["pilot"]), (94, "miner-93"))

    def test_a_page_that_fails_keeps_the_last_whole_list_and_says_so(self):
        answers, _asked = self.paged()
        state, _notes = empire.collect(str(self.data), str(self.root), see=self.see(answers), pause=0, now=0)
        empire.save(str(self.data), state)
        broken, _asked = self.paged(fail_at=50)
        state, notes = empire.collect(str(self.data), str(self.root), see=self.see(broken), pause=0, now=60)
        self.assertEqual(len(state["members"]), 94)                                      # never half a list
        self.assertTrue(any("was not read whole (the page at offset 50" in n for n in notes), notes)

    def test_a_game_that_ignores_the_offset_ends_the_paging_with_a_note(self):
        answers, asked = self.paged(ignore_offset=True)
        state, notes = empire.collect(str(self.data), str(self.root), see=self.see(answers), pause=0, now=0)
        self.assertEqual((len(state["members"]), len(asked)), (50, 2))
        self.assertTrue(any("holds 50 of 94" in n for n in notes), notes)


class CollectTests(Tree):
    def test_the_member_cap_is_twenty_without_an_office_and_the_best_office_plus_a_quarter_with_them(self):
        recruit = {"hiring_board": 50, "recruitment_desk": 100}
        self.assertEqual(empire.members_cap([], recruit), 20)                       # the info's members_limit (a page size) plays no part
        self.assertEqual(empire.members_cap([{"type": "faction_lockbox", "base": "a", "status": "active"}], recruit), 20)
        self.assertEqual(empire.members_cap([{"type": "hiring_board", "base": "a", "status": "active"}], recruit), 50)
        self.assertEqual(empire.members_cap([{"type": "recruitment_desk", "base": "a", "status": "active"}, {"type": "hiring_board", "base": "b", "status": "active"},
                                             {"type": "hiring_board", "base": "c", "status": "under_construction"}], recruit), 112)

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
                         [("wild", "", "built", "lawless", 4, ["Test Rock (outpost, TEST)", "Their Hub (station, THEM)"]), ("nowhere", "p1", "dropped", "not on the chart", None, [])])   # our outpost stands in `wild`: built, by the game's list
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
        self.assertIn("| `wild` | Wild | lawless | 4 | Test Rock (outpost, TEST), Their Hub (station, THEM) | built | Oracle | beside the ice |", text)
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

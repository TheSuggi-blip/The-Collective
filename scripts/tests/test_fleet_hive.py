"""game/fleet/hive.py on a disposable data folder: what the stations bid in all, a field's change between two readings, a route's runs in a window, what each division put into the reserve per hour (flow), a base broken down by the chosen recipe. No engine, no network."""

import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import tempfile
import time
import unittest

os.environ.setdefault("FLEET_TAXES", os.devnull)   # no test reads the fleet's own tax record


FLEET = Path(__file__).resolve().parents[2] / "game" / "fleet"


def load(name):
    spec = importlib.util.spec_from_file_location(name + "_under_test", FLEET / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class HiveTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="fleet-hive-test-")
        self.addCleanup(self.temp.cleanup)
        self.data = Path(self.temp.name)
        for folder in ("market", "scouting", "wildlife", "fleet/ships", "routes", "catalog", "stock", "intel"):
            (self.data / folder).mkdir(parents=True)
        self.hive = load("hive")
        book = lambda base, system, bid, units: (self.data / "market" / (base + ".json")).write_text(json.dumps(
            {"base": base, "system": system, "read_at": "2026-11-16T00:00:00Z", "items": [{"item_id": "water_ice", "best_buy": bid, "best_buy_qty": units, "best_sell": 0}]}))
        book("hub", "home", 38, 6000)
        book("a" * 32, "far", 20, 4000)
        book("low", "home", 5, 90000)

    def test_demand_adds_the_stations_that_pay_and_names_a_players_station_by_its_system(self):
        market, where = self.hive.books(str(self.data))
        self.assertEqual(self.hive.demand(market, "water_ice", 16), (38, 10000, 2, "hub"))        # the bid of 5 cr does not count
        self.assertEqual(self.hive.demand(market, "iron_ore", 1), (0, 0, 0, ""))
        self.assertEqual((self.hive.label("hub", where), self.hive.label("a" * 32, where)), ("hub", "station in far"))

    def test_a_field_s_change_is_measured_between_its_first_and_last_census(self):
        hour = lambda h: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(1_800_000_000 + h * 3600))
        rows = [{"at": hour(0), "system": "far", "deposits": {"belt": {"water_ice": 1000}}, "herds": {"belt": {"veil_ray": 6}}},
                {"at": hour(2), "system": "far", "deposits": {"belt": {"water_ice": 1500}}, "herds": {"belt": {"veil_ray": 2}}},
                {"at": hour(2), "system": "home", "deposits": {"rock": {"iron_ore": 7}}}]
        (self.data / "wildlife" / "history.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
        rates, herds = self.hive.regrowth(str(self.data))
        self.assertEqual(rates, {("far", "belt", "water_ice"): 250.0})                             # one reading is no rate
        self.assertEqual(herds[("far", "belt", "veil_ray")], (2, 6, 2))

    def test_a_window_counts_steady_credits_and_keeps_what_is_paid_once_apart(self):
        now = time.time()
        stamp = lambda ago: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now - ago))
        rows = [{"route": "r", "started": stamp(600), "minutes": 30, "delta": 1000, "credits_before": 5000, "credits_after": 6000},
                {"route": "r", "started": stamp(900), "minutes": 30, "delta": 4000, "one_time": 3000, "credits_before": 5000, "credits_after": 9000},
                {"route": "r", "started": stamp(90000), "minutes": 30, "delta": 99, "credits_before": 1, "credits_after": 100}]
        self.assertEqual(self.hive.window_stats(rows, now - 3600)["r"], [2, 2000.0, 60.0, 3000])

    def test_what_comes_back_is_the_sum_of_the_rises_between_readings(self):
        self.assertEqual(self.hive.moves([(0, 100), (3600, 40), (7200, 90), (10800, 90)]), (50, 60, 3.0))
        self.assertEqual(self.hive.moves([(0, 5)]), (0, 0, 0.0))
        # 72 units at 38 are sold out and the step of 7,470 at 34 comes into view: no refill; then 72 at 38 stand again: 72 came back
        self.assertEqual(self.hive.bid_moves([(0, 72, 38), (60, 7470, 34), (120, 7400, 34), (180, 72, 38), (240, 90, 38)]), (72 + 18, 72 + 70))
        self.assertEqual(self.hive.bid_moves([(0, 67284, 18), (60, 67515, 19), (120, 56480, 21)]), (0, 0))      # a deep bid whose price creeps is the same demand
        hour = lambda h: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(1_800_000_000 + h * 3600))
        with open(self.data / "wildlife" / "history.jsonl", "w") as handle:
            for h, herd in ((0, {"belt": {"veil_ray": 6}}), (1, {}), (2, {"belt": {"veil_ray": 4}})):
                handle.write(json.dumps({"at": hour(h), "system": "far", "deposits": {"belt": {"water_ice": 1000 - 100 * h}}, "herds": herd, "pilots": {"belt": 0}}) + "\n")
        with open(self.data / "market" / "history.jsonl", "w") as handle:
            for h, units in ((0, 500), (1, 100), (2, 400)):
                handle.write(json.dumps({"t": hour(h), "base": "hub", "item": "water_ice", "bid": 38, "bid_qty": units, "ask": 0, "ask_qty": 0}) + "\n")
        bids, deposits, herds = self.hive.series(str(self.data))
        self.assertEqual([units for _t, units, _bid in bids[("hub", "water_ice")]], [500, 100, 400])
        self.assertEqual([c for _t, c in herds[("far", "belt", "veil_ray")]], [6, 0, 4])          # the herd was gone at the second reading of its place
        self.assertEqual(self.hive.moves(herds[("far", "belt", "veil_ray")])[:2], (4, 6))
        with contextlib.redirect_stdout(io.StringIO()) as printed:
            self.assertEqual(self.hive.show_refill(str(FLEET.parent), str(self.data), time.time()), 0)
        self.assertIn("water_ice", printed.getvalue())
        self.assertIn("veil_ray", printed.getvalue())

    def test_work_is_counted_per_pilot_and_per_route_in_one_unit(self):
        now = time.time()
        stamp = lambda ago: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now - ago))
        rows = [{"route": "r", "pilot": "miner-1", "started": stamp(600), "minutes": 30, "delta": 1000, "credits_before": 1000, "credits_after": 2000},
                {"route": "r", "pilot": "miner-2", "started": stamp(900), "minutes": 30, "delta": 4000, "credits_before": 1000, "credits_after": 5000, "one_time": 3000},
                {"route": "r", "pilot": "miner-1", "started": stamp(9000), "minutes": 30, "delta": 8000, "credits_before": 1000, "credits_after": 9000}]
        by_pilot, by_route = self.hive.pilot_stats(rows, now - 3600)
        self.assertEqual(by_pilot["miner-1"], [1, 1000.0, 30.0, 0, 30.0])
        self.assertEqual(by_route["r"], [2, 2000.0, 60.0, 3000, 60.0])
        self.assertEqual(self.hive.per_hour(2000, 60), "2,000")
        self.assertEqual(self.hive.per_hour(2000, 0), "--")

    def test_the_scale_is_a_route_that_repeats_never_a_fitting_or_a_mission(self):
        hive = self.hive if hasattr(self, "hive") else load("hive")
        routes = {"mine": {"id": "mine", "kind": "mine", "sell": [{"item": "ice", "min_price": 1}]}, "gather": {"id": "gather", "kind": "mine"}, "fit": {"id": "fit", "kind": "circuit", "stops": [{"at": "a:b:c", "fit": "ice_harvester_i"}]},
                  "once": {"id": "once", "kind": "circuit", "once": True, "stops": [{"at": "a:b:c"}]}}
        by_route = {"mine": [3, 9000.0, 90.0, 0, 90.0], "fit": [2, 50000.0, 30.0, 0, 30.0], "once": [4, 40000.0, 60.0, 0, 60.0], "gone": [5, 99000.0, 10.0, 0, 10.0],
                    "gather": [6, 70000.0, 30.0, 0, 30.0]}                                        # standing work is no route judged on its pay
        self.assertEqual([rid for _f, rid, _r in hive.scale(routes, by_route)], ["mine"])
        self.assertEqual([hive.work_of(routes[rid]) for rid in ("mine", "gather")], ["mining", "standing work (trains, gathers)"])
        routes["drain"] = {"id": "drain", "kind": "circuit", "requires": {"stored": {"at": "c", "item": "ice", "min": 60}}, "stops": [{"at": "a:b:c"}]}
        by_route["drain"] = [3, 90000.0, 20.0, 0, 20.0]                                               # it sells a load mined earlier: no scale for work
        self.assertEqual([rid for _f, rid, _r in hive.scale(routes, by_route)], ["mine"])

    def test_a_forecast_counts_each_route_by_its_ships_and_keeps_what_is_paid_once_apart(self):
        hive = self.hive
        routes = {"mine": {"id": "mine", "kind": "mine", "sell": [{"item": "ice", "min_price": 1}], "measured": {"cph_per_ship": 500, "credits_per_run": 300, "runs": 4, "minutes": 36}},
                  "gather": {"id": "gather", "kind": "mine"}, "new": {"id": "new", "kind": "hunt"}, "blank": {"id": "blank", "kind": "hunt"},
                  "once": {"id": "once", "kind": "circuit", "once": True, "measured": {"credits_per_run": 4000, "runs": 2, "minutes": 20}, "stops": [{"at": "a:b:c"}]},
                  "park": {"id": "park", "kind": "circuit", "park": True, "stops": [{"at": "a:b:c"}]}}
        by_route = {"mine": [3, 900.0, 90.0, 0, 90.0], "gather": [4, -400.0, 120.0, 0, 120.0]}     # the window's runs win over the file's figure
        on = {"mine": 2, "gather": 10, "new": 1, "blank": 1, "once": 3, "park": 1, "gone": 1}
        rows = hive.forecast(routes, on, by_route, {"new": 800}, 4)
        found = {row[0]: row[1:] for row in rows}
        self.assertEqual(found["mine"], (2, 600.0, "3 runs of the window", 1200.0, 0))
        self.assertEqual(found["gather"], (10, -200.0, "4 runs of the window", -2000.0, 0))        # standing work costs its fuel
        self.assertEqual(found["new"], (1, 800.0, "the route maker's estimate", 800.0, 0))
        self.assertEqual(found["blank"], (1, None, "not measured", 0.0, 0))                         # never filled in: it counts as 0
        self.assertEqual(found["once"], (3, None, "pays once per pilot", 0.0, 12000))               # no steady money
        self.assertEqual(found["park"], (1, 0.0, "waits docked", 0.0, 0))
        self.assertEqual(found["gone"], (1, None, "route file gone", 0.0, 0))
        self.assertEqual([row[0] for row in rows][:2] + [rows[-1][0]], ["once", "mine", "gather"])  # the most first, the loss last
        by_route["mine"] = [1, 900.0, 90.0, 0, 90.0]                                               # one run is no measure of a window
        self.assertEqual(hive.forecast(routes, {"mine": 2}, by_route, {}, 4)[0][1:], (2, 500.0, "all its runs", 1000.0, 0))
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(hive.show_forecast(str(FLEET.parent), str(self.data), time.time(), "all", 4), 0)
            self.assertEqual(hive.show_forecast(str(FLEET.parent), str(self.data), time.time(), "Nobody", 4), 1)
        self.assertIn("FORECAST | the next 4 hours", out.getvalue())
        self.assertIn("FLEET | 0 ships | steady money: 0 credits an hour", out.getvalue())
        self.assertIn("no member `Nobody`", out.getvalue())

    def test_the_history_store_answers_from_its_read_copy(self):
        now = time.time()
        stamp = lambda ago: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now - ago))
        said = io.StringIO()
        with contextlib.redirect_stdout(said):
            self.assertEqual(self.hive.show_store(str(self.data), now, 24, []), 1)              # no copy yet: said, not failed
        self.assertIn("no read copy", said.getvalue())
        runs = [{"route": "ice", "pilot": "miner-1", "started": stamp(7200), "minutes": 30, "delta": 4000, "credits_before": 1000, "credits_after": 5000, "one_time": 1000},
                {"route": "ice", "pilot": "miner-2", "started": stamp(7000), "minutes": 30, "delta": 1000, "credits_before": 1000, "credits_after": 2000},
                {"route": "ice", "pilot": "miner-3", "started": stamp(6900), "minutes": 30, "delta": 0, "credits_before": 0, "credits_after": 0, "notes": ["wallet not read"]}]
        (self.data / "routes" / "runs.jsonl").write_text("".join(json.dumps(r) + "\n" for r in runs))
        (self.data / "market" / "history.jsonl").write_text("".join(json.dumps(m) + "\n" for m in (
            {"t": stamp(7200), "base": "hub", "item": "water_ice", "bid": 30, "bid_qty": 9, "ask": 0, "ask_qty": 0},
            {"t": stamp(7100), "base": "hub", "item": "water_ice", "bid": 38, "bid_qty": 9, "ask": 44, "ask_qty": 2})))
        self.hive.history.one_pass(str(self.data), now=now)
        said = io.StringIO()
        with contextlib.redirect_stdout(said):
            self.assertEqual(self.hive.show_store(str(self.data), now, 24, []), 0)
            self.assertEqual(self.hive.show_store(str(self.data), now, 24, ["price", "water_ice"]), 0)
            self.assertEqual(self.hive.show_store(str(self.data), now, 24, ["price", "no_such_item"]), 0)
        text = said.getvalue()
        ice = next(line.split() for line in text.splitlines() if line.strip().startswith("ice "))
        self.assertEqual(ice, ["ice", "3", "1.0", "4,000", "4,000", "1,000"])                 # by hand: (4000 - 1000) + 1000 over the 60 minutes that read a wallet
        hub = next(line.split() for line in text.splitlines() if line.strip().startswith("hub "))
        self.assertEqual(hub[:7], ["hub", "1" if stamp(7200)[:13] == stamp(7100)[:13] else "2", "30", "38", "44", "44", "2"])
        self.assertIn("no price move of `no_such_item`", text)

    def test_what_a_bid_regains_is_one_figure_for_the_tables_and_for_the_plans(self):
        now = time.time()
        stamp = lambda ago: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now - ago))
        (self.data / "market" / "history.jsonl").write_text("".join(
            json.dumps({"t": stamp(ago), "base": "hub", "item": "water_ice", "bid": 38, "bid_qty": units, "ask": 0, "ask_qty": 0}) + "\n"
            for ago, units in ((7200, 1000), (3600, 600), (0, 900))))
        bids, fields, herds = self.hive.rates(str(self.data))
        added, taken, hours = bids[("hub", "water_ice")]
        self.assertEqual((round(added), round(taken), round(hours, 1)), (150, 200, 2.0))          # 300 came back and 400 were taken in two hours
        self.assertEqual((fields, herds), ({}, {}))

    def test_the_briefing_is_one_answer_and_says_what_it_could_not_read(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.hive.show_briefing(str(FLEET.parent), str(self.data), time.time(), "Zero", 4)
        text = out.getvalue()
        for part in ("=== THE ORDERS IN FORCE", "=== REQUESTS NOT CLOSED, ADDRESSED TO Zero", "=== THE FLEET'S MONEY", "=== MY STANDING FLEET", "STANDING FLEET | Zero, role miner",
                     "=== THE FILL GATE (no ship is idle)", "PASS: no ship of miner waits"):
            self.assertIn(part, text)

    def test_a_system_shows_what_we_own_and_plan_there(self):
        (self.data / "empire").mkdir()
        (self.data / "empire" / "empire.json").write_text(json.dumps({
            "bases": [{"name": "Test Rock", "kind": "outpost", "system": "home"}, {"name": "Elsewhere", "kind": "station", "system": "far"}],
            "facilities": [{"name": "Faction Lockbox", "type": "faction_lockbox", "level": 1, "base": "hub", "system": "home", "status": "active"}],
            "sites": [{"system": "home", "status": "built", "proposed_by": "Oracle"}, {"system": "far", "status": "candidate", "proposed_by": ""}]}))
        systems = lambda root: ({"home": ("voidborn", 0), "far": ("-", 3), "bare": ("-", 5)}, "voidborn")
        old, self.hive.routefiles.atlas = self.hive.routefiles.atlas, systems
        self.addCleanup(setattr, self.hive.routefiles, "atlas", old)
        text = {}
        for sid in ("home", "far", "bare"):
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                self.assertEqual(self.hive.show_system(str(FLEET.parent), str(self.data), time.time(), sid), 0)
            text[sid] = [line for line in out.getvalue().split("\n") if line.startswith("  ours here:")]
        self.assertEqual(text["home"], ["  ours here: outpost Test Rock, Faction Lockbox tier 1 at hub (active) | a site of ours: built, proposed by Oracle"])
        self.assertEqual(text["far"], ["  ours here: station Elsewhere | a site of ours: candidate"])
        self.assertEqual(text["bare"], ["  ours here: nothing built"])                              # no reading names the system: said, not left out

    def test_a_question_without_readings_says_so_instead_of_failing(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(self.hive.show_ship(str(self.data), time.time(), "nobody-1"), 1)
            self.assertEqual(self.hive.show_base(str(FLEET.parent), str(self.data), time.time(), "outpost"), 1)
            self.assertEqual(self.hive.show_history(str(self.data), time.time(), 12), 0)
        self.assertIn("no ship `nobody-1`", out.getvalue())
        self.assertIn("no catalog in the data folder", out.getvalue())
        self.assertIn("fewer than two hourly samples", out.getvalue())

    def reserve_repo(self, choices=None):
        """A repository with a reserve of 10 steel plates and, when given, its chosen recipes; a catalog where steel_plate has
        two recipes, the rule's from a hide nobody gathers and one from ore. The repository's game/ folder, as hive.py takes it."""
        root = Path(self.temp.name) / "repo"
        (root / "game").mkdir(parents=True, exist_ok=True)
        (root / "game" / "reserve.tsv").write_text("kind\tid\tunits\tnote\nitem\tsteel_plate\t10\tplates on hand\n", encoding="utf-8")
        if choices is not None:
            (root / "game" / "reserve-recipes.tsv").write_text("item\trecipe\tnote\n" + choices, encoding="utf-8")
        recipe = lambda rid, item, units, out, made, hand=True, plants=(): {"id": rid, "inputs": [{"item_id": item, "quantity": units}], "hand_craftable": hand,
                                                                             "outputs": [{"item_id": made, "quantity": out}], "produced_by_facility_ids": list(plants)}
        catalog = {"version": "9.9.9", "items": [{"id": "iron_ore", "category": "ore", "base_value": 5}, {"id": "steel_plate", "category": "refined", "base_value": 18},
                                                 {"id": "hide", "category": "misc", "base_value": 9}, {"id": "gem", "category": "misc", "base_value": 50},
                                                 {"id": "outpost_kit", "category": "component", "base_value": 900}],
                   "recipes": [recipe("smelt", "iron_ore", 10, 1, "steel_plate"), recipe("boil_hide", "hide", 2, 1, "steel_plate"),
                               recipe("assemble_outpost_kit", "steel_plate", 5, 1, "outpost_kit", False, ["kit_plant"])],
                   "facilities": [{"id": "kit_plant", "level": 1, "build_cost": 100, "build_materials": [{"item_id": "steel_plate", "quantity": 3}]}], "ships": []}
        (self.data / "catalog" / "9.9.9.json").write_text(json.dumps(catalog))
        return root / "game"

    def book(self, military, at):
        path = self.data / "stock" / "storage.json"
        path.write_text(json.dumps({"updated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(at)), "pilots": {
            "miner-1": {"read_at": "2026-11-16T10:00:00Z", "stations": {"hub": {"iron_ore": 30, "gem": 4}}},
            "drone-1": {"read_at": "2026-11-16T10:00:00Z", "stations": {"hub": {"iron_ore": military}}}}}))
        os.utime(path, (at, at))

    def test_flow_shows_the_units_each_division_put_into_the_reserve_per_hour(self):
        game = self.reserve_repo("steel_plate\tsmelt\tLogistics, 2026-11-16; flown\n")             # the reserve's items: steel_plate and, by smelt, iron_ore
        hour = 1_800_000_000 // 3600 * 3600
        self.book(5, hour + 600)
        self.hive.history.one_pass(str(self.data), now=hour + 600, root=str(game))
        self.book(505, hour + 4200)                                                                  # an hour later Military stored 500 ore
        self.hive.history.one_pass(str(self.data), now=hour + 4200, root=str(game))
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(self.hive.show_flow(str(game), str(self.data), time.time(), "all", 4), 0)
        text = out.getvalue()
        self.assertTrue(text.startswith("FLOW | what each division put into the reserve per hour: the units it holds (station storage and holds) of the 2 items"))
        self.assertIn("1.0 hours on record", text.split("\n")[0])
        self.assertIn("  only 1.0 hours on record: the figures of the last 4, 12, 24 hours read from the oldest sample", text)
        self.assertIn("Military (Apophis) | 1 of the reserve's items held now, 505 units", text)
        self.assertRegex(text, r"\n  iron_ore +505 +\+500\.0 +\+500\.0 +\+500\.0\n  SUM 1 items +505 +\+500\.0")
        self.assertRegex(text, r"Mining \(Zero\)[^\n]*\n[^\n]*\n  iron_ore +30 +\+0\.0")
        self.assertNotIn("gem", text)                                                                # held, but no reserve item
        self.assertNotIn("Intel (Oracle)", text)                                                     # nothing held: left out of `all`
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(self.hive.show_flow(str(game), str(self.data), time.time(), "Apophis", 2), 0)
            self.assertEqual(self.hive.show_flow(str(game), str(self.data), time.time(), "Oracle", 4), 0)
            self.assertEqual(self.hive.show_flow(str(game), str(self.data), time.time(), "Nobody", 4), 1)
            self.assertEqual(self.hive.show_flow(str(game), str(Path(self.temp.name) / "empty"), time.time(), "all", 4), 1)
        text = out.getvalue()
        self.assertIn("per h, 2h", text)
        self.assertNotIn("Mining (Zero)", text)
        self.assertIn("Intel (Oracle) | none of the reserve's items in the samples", text)
        self.assertIn("no member `Nobody`", text)
        self.assertIn("FLOW | no read copy", text)

    def test_base_breaks_down_by_the_chosen_recipe_and_names_it(self):
        game = self.reserve_repo()
        self.book(5, time.time())
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(self.hive.show_base(str(game), str(self.data), time.time(), "outpost"), 0)
        self.assertIn("    8 steel_plate <- boil_hide x 8, by hand", out.getvalue())
        self.assertIn("  recipes taken where an item has more than one", out.getvalue())
        self.assertIn("    steel_plate: recipe boil_hide (1 of 2; choose another in game/reserve-recipes.tsv)", out.getvalue())
        game = self.reserve_repo("steel_plate\tsmelt\tLogistics, 2026-11-16; not flown yet\n")
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(self.hive.show_base(str(game), str(self.data), time.time(), "outpost"), 0)
        self.assertIn("    8 steel_plate <- smelt x 8, by hand", out.getvalue())
        self.assertIn("    steel_plate: recipe smelt (1 of 2; chosen in game/reserve-recipes.tsv line 2)", out.getvalue())
        self.assertNotIn("hide", out.getvalue())

    def test_the_fleet_s_money_prints_net_as_income_less_costs_and_says_what_it_left_out(self):
        # the collector's own figures (station/fleet.py) over an hour in which sentinel-1 of the command group gave
        # trader-1, a pilot born in the hour with 100 cr, 18,000 cr: neither moves a figure, and every printed row
        # reads net = income - costs with the costs above zero (2026-11-16: division nets below zero, costs below zero)
        spec = importlib.util.spec_from_file_location("collector_under_test", FLEET.parents[1] / "station" / "fleet.py")
        collector = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(collector)
        folder, now = self.data / "fleet", time.time()
        collector.DATA, t0 = folder, int(now) - 3600
        (folder / "onetime.json").write_text(json.dumps([[t0 + 1800, "sentinel-1", "Wallet top-up", -18000], [t0 + 1800, "trader-1", "Wallet top-up", 18000]]))
        (folder / "gifts.jsonl").write_text(json.dumps({"at": t0 + 1800, "from": "sentinel-1", "to": "trader-1", "credits": 18000}) + "\n")
        (folder / "seed.json").write_text(json.dumps({"sentinel-1": [0, 50000, 1000, 0], "trader-1": [t0 + 600, 100, 0, 0]}))
        history = [[t0, 50000, 1, 1000, 0, 0, 0, {"Command": [1, 50000, 1000, 0, 0, 0]}],
                   [t0 + 3600, 49700, 2, 2500, 0, 0, 0, {"Command": [1, 31000, 1500, 0, 0, 0], "Trade": [1, 18700, 1000, 0, 0, 0]}]]
        rates = collector.rates(history, t0 + 3600)
        (folder / "fleet.json").write_text(json.dumps({"updated_at": "", "totals": {"ships": 2, "working": 2, "parked": 0, "adrift": 0, "credits": 49700, "credits_per_ship": 24850,
                                                                                    "divisions": {"Command": {"ships": 1, "credits": 31000}, "Trade": {"ships": 1, "credits": 18700}}, "rates": rates}}))
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.hive.show_fleet(str(FLEET.parent), str(self.data), now)
        text = out.getvalue()
        self.assertIn("last 1h  (60 min measured): net -400 | income 1,500 | costs 1,900 (metered: fuel -- + repairs -- = --)", text)
        self.assertIn("left out: gifts between our ships, 18,000 an hour (0 of them name one side only and move no division); the first wallets of 1 new pilots, 100 cr", text)
        self.assertIn("rewards 0 in 0 bookings | bought once (tools, goods for a mission) 0 in 0 buys", text)    # the halves of a gift are neither
        number = lambda cell: int(cell.replace(",", ""))
        rows = {line.split()[0]: line.split() for line in text.splitlines() if line.strip().split()[:1] in (["Command"], ["Trade"])}
        self.assertEqual(sorted(rows), ["Command", "Trade"])
        for name, (net, income, costs) in (("Command", (-1000, 500, 1500)), ("Trade", (600, 1000, 400))):
            cells = rows[name]
            self.assertEqual((number(cells[5]), number(cells[6]), number(cells[7])), (net, income, costs))
            self.assertEqual(number(cells[5]), number(cells[6]) - number(cells[7]))
            self.assertGreater(number(cells[7]), 0)
        self.assertEqual((rows["Command"][9], rows["Trade"][9]), ("-18,000", "18,000"))


class CraftbookFileTests(unittest.TestCase):
    # 2026-11-16: craftbook_file took the newest file time; catalog-refresh.py keeps two versions side by side, and every
    # other reader (craftbook.py, store.py, empire.py, catalog-index.py) takes the highest version in the name
    def test_the_highest_version_wins_whatever_the_file_times(self):
        hive = load("hive")
        with tempfile.TemporaryDirectory(prefix="fleet-hive-catalog-") as temp:
            folder = Path(temp) / "catalog"
            self.assertEqual(hive.craftbook_file(temp), folder / "none.json")                       # no folder, no file: what it gave before
            folder.mkdir()
            self.assertEqual(hive.craftbook_file(temp), folder / "none.json")
            for name in ("0.99.0.json", "0.100.0.json", "ammo.json", "refresh.json"):
                (folder / name).write_text("{}")
            for older, newer in (("0.99.0.json", "0.100.0.json"), ("0.100.0.json", "0.99.0.json")):
                for age, name in ((300, older), (200, newer), (100, "ammo.json"), (50, "refresh.json")):
                    os.utime(folder / name, (time.time() - age, time.time() - age))
                self.assertEqual(hive.craftbook_file(temp).name, "0.100.0.json", "%s written last" % newer)

if __name__ == "__main__":
    unittest.main()

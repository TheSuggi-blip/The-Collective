"""game/fleet/routemaker.py on a disposable data folder and chart: every kind of candidate, the depth of a book, the route files it writes. No engine, no network."""

import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import tempfile
import time
import unittest

os.environ.setdefault("FLEET_TAXES", os.devnull)   # no test reads the fleet's own tax record (routemaker.py loads hive.py)


FLEET = Path(__file__).resolve().parents[2] / "game" / "fleet"


def load(name):
    spec = importlib.util.spec_from_file_location(name + "_under_test", FLEET / (name + ".py"))
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


maker, routes = load("routemaker"), load("routes")
NOW = 1_800_000_000
STAMP = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(NOW - 600))
LOADS = 60 / (2 * 1.5 + 1.5 + 60 / (0.05 * 50))               # mid_belt sold at mid_base: two flights, one stop, a hold of 60 mined at 0.05 x richness 50
FUEL = 2 * 2 * 13.0                                            # two flights of 2 units of fuel at 13 cr
FAR = 60 / (2 * 2.0 + 2 * 1.5 + 1.5 + 60 / (0.05 * 50))        # mid_belt sold at home_base: one jump each way besides
FAR_FUEL = (2 * 1 + 2 * 2) * 13.0
CHART = "# test chart\nid\tname\tx\ty\tempire\tflags\tjumps_from_home\tlanes\nhome\tHome\t0\t0\tvoidborn\t-\t0\tmid\nmid\tMid\t1\t0\tvoidborn\t-\t1\thome,wild\nwild\tWild\t2\t0\t-\t-\t2\tmid\nlost\tLost\t9\t9\t-\t-\t9\t-\n"


def station(system, poi, base):
    return {poi: {"kind": "normal", "poi": {"id": poi, "system_id": system, "type": "station", "name": base.title(), "base_id": base}}}


def field(poi, kind, resources):
    return {poi: {"kind": "normal", "poi": {"id": poi, "type": kind, "name": poi.title()},
                  "resources": [{"resource_id": r, "richness": rich, "remaining": left} for r, rich, left in resources]}}


def row(item, bid=0, bid_qty=0, ask=0, ask_qty=0, depth=True):
    out = {"item_id": item, "item_name": item.title(), "best_buy": bid, "buy_quantity": bid_qty, "best_sell": ask, "sell_quantity": ask_qty}
    if depth:
        out.update({"best_buy_qty": bid_qty, "best_sell_qty": ask_qty})
    return out


class Tree(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="fleet-routemaker-test-")
        self.addCleanup(self.temp.cleanup)
        self.data, self.root = Path(self.temp.name) / "data", Path(self.temp.name) / "game"
        for folder in ("scouting", "market", "missions", "wildlife", "catalog", "routes", "fleet", "stock"):
            (self.data / folder).mkdir(parents=True)
        (self.root / "map").mkdir(parents=True)
        (self.root / "routes" / "plans").mkdir(parents=True)
        (self.root / "map" / "galaxy.tsv").write_text(CHART, encoding="ascii")
        self.put("scouting/home.json", {"system": {"id": "home"}, "read_at": STAMP, "pois": station("home", "core", "home_base")})
        self.put("scouting/mid.json", {"system": "mid", "read_at": STAMP, "pois": dict(station("mid", "hub", "mid_base"), **field("mid_belt", "asteroid_belt", [("ore", 40, 9000), ("dust", 10, 9000)]))})
        self.put("scouting/wild.json", {"system": "wild", "read_at": STAMP, "pois": field("wild_ice", "ice_field", [("ice", 50, 9000)])})
        self.put("catalog/1.0.json", {"version": "1.0", "items": [{"id": "ore", "size": 1}, {"id": "gel", "size": 1, "description": "Wrung from a glow-ray's mantle."},
                                                                 {"id": "ice_harvester_i", "base_value": 1000}],
                                      "recipes": [{"id": "press_ore", "name": "Press Ore", "hand_craftable": True, "inputs": [{"item_id": "ore", "quantity": 2}],
                                                   "outputs": [{"item_id": "plate", "quantity": 1}]}]})
        self.put("fleet/fleet.json", {"ships": [{"name": "miner-1", "cargo_capacity": 60, "docked": "home_base", "status": "connected"},
                                                {"name": "miner-2", "cargo_capacity": 60, "docked": None, "status": "connected"}]})

    def put(self, name, value):
        (self.data / name).write_text(json.dumps(value), encoding="utf-8")

    def book(self, base, system, rows):
        self.put("market/%s.json" % base, {"base": base, "system": system, "read_at": STAMP, "items": rows})

    def build(self, look=None):
        return maker.build(str(self.data), self.root, NOW, look=look)

    def one(self, book, cid):
        found = [c for c in book["candidates"] if c["id"] == cid]
        self.assertEqual(len(found), 1, "%s in %s" % (cid, [c["id"] for c in book["candidates"]]))
        return found[0]


class ChartTests(Tree):
    def test_jumps_follow_the_lanes_and_a_system_without_a_way_has_none(self):
        chart = maker.Chart(maker.load_chart(self.root))
        self.assertEqual([chart.jumps("home", "home"), chart.jumps("home", "wild"), chart.jumps("wild", "home"), chart.jumps("home", "lost")], [0, 2, 2, None])
        self.assertEqual(maker.policed_systems(self.root), {"home", "mid"})


class DepthTests(Tree):
    def test_units_are_sold_down_the_levels_only_to_four_fifths_of_the_best_bid(self):
        self.book("home_base", "home", [row("ore", bid=100, bid_qty=500, ask=120, ask_qty=10, depth=False), row("ice", bid=50, bid_qty=7)])
        world = maker.load_world(str(self.data), self.root, NOW)
        self.assertEqual(maker.sell_into(world, "home_base", "ore", 60), (1, 100, "one unit: the saved book has no depth"))     # a total is no depth
        self.assertEqual(maker.sell_into(world, "home_base", "ice", 60), (7, 350, "depth at the best price"))
        self.assertEqual(maker.sell_into(world, "home_base", "gel", 60)[2], "no bid")
        self.assertEqual(set(world["wanted"]), {("home_base", "ore"), ("home_base", "ice")})                                   # both would like their levels read
        world["ladders"] = {"home_base": {"ore": {"t": NOW, "bids": [[100, 1], [99, 1], [90, 10], [79, 400]], "asks": [[120, 5], [150, 5]]}}}
        self.assertEqual(maker.sell_into(world, "home_base", "ore", 60), (12, 1099, "price levels read"))                      # 79 is under 80: not sold there
        self.assertEqual(maker.buy_from(world, "home_base", "ore", 60)[:2], (5, 600))                                          # 150 is over 120% of 120
        world["ladders"]["home_base"]["ore"]["t"] = NOW - maker.LADDER_FRESH - 1
        self.assertEqual(maker.sell_into(world, "home_base", "ore", 60)[2], "one unit: the saved book has no depth")           # an old ladder is no ladder

    def test_the_most_wanted_books_are_read_through_a_docked_pilot_and_kept(self):
        self.book("home_base", "home", [row("ore", bid=100, bid_qty=500, depth=False), row("ice", bid=5, bid_qty=7)])
        self.book("mid_base", "mid", [row("ore", bid=90, bid_qty=500, depth=False)])
        world = maker.load_world(str(self.data), self.root, NOW)
        for base, item in (("home_base", "ore"), ("home_base", "ice"), ("mid_base", "ore")):
            maker.sell_into(world, base, item, 60)
        asked = []
        read = maker.fetch_ladders(world, str(self.data), look=lambda pilot, item: asked.append((pilot, item)) or {"bids": [[100, 1]], "asks": []}, pause=0)
        self.assertEqual((read, asked), (2, [("miner-1", "ore"), ("miner-1", "ice")]))                                         # no pilot is docked at mid_base
        saved = json.loads((self.data / "market" / "ladders.json").read_text())
        self.assertEqual(saved["home_base"]["ore"], {"bids": [[100, 1]], "asks": [], "t": NOW})


class CandidateTests(Tree):
    def test_a_field_is_sold_where_its_mix_pays_most_and_an_ice_field_names_its_harvester(self):
        self.book("home_base", "home", [row("ore", bid=10, bid_qty=5000), row("ice", bid=40, bid_qty=5000)])
        self.book("mid_base", "mid", [row("ore", bid=12, bid_qty=5000), row("dust", bid=3, bid_qty=10)])
        book = self.build()
        mine = self.one(book, "mine-mid-belt")
        self.assertEqual((mine["basis"]["sold_at"], mine["basis"]["jumps"], mine["status"]), ("mid_base", 0, "new"))
        self.assertEqual(mine["basis"]["a_load"], ["ore 48 of 48 units for 576 cr (depth at the best price)", "dust 5 of 12 units for 14 cr (depth at the best price)"])
        self.assertIn("dust: bid 3 x 10 at mid_base takes 10 of 25 units an hour", mine["warnings"])                        # ten units an hour, not ten a load
        self.assertEqual((mine["route"]["belt"], mine["route"]["station"], mine["route"]["max_ships"]), ("mid:mid_belt", "mid:hub:mid_base", 1))
        self.assertEqual(mine["route"]["sell"], [{"item": "ore", "min_price": 10}, {"item": "dust", "min_price": 3}])           # four fifths of the bid the hour reaches, rounded up
        ice = self.one(book, "mine-wild-ice")
        self.assertEqual(ice["route"]["requires"], {"module": "ice_harvester_i", "empty_hold": True})                           # the harvester, and nothing to lose aboard
        self.assertTrue(any("lawless space: no police at wild" in w for w in ice["warnings"]))
        self.assertTrue(any("ice_harvester_i (base value 1000 cr)" in w for w in ice["warnings"]))
        for route in (mine["route"], ice["route"]):                                                                           # what it writes passes the route gate
            (self.root / "routes" / (route["id"] + ".json")).write_text(json.dumps(route), encoding="ascii")
        self.assertEqual([e for e in routes.check(str(self.root))[0] if "index.md" not in e], [])
        again = self.one(self.build(), "mine-mid-belt")
        self.assertEqual(again["status"], "route file exists, in no plan")                                                    # the candidate knows its route

    def test_a_gap_that_one_load_closes_is_costed_as_one_load(self):
        self.book("home_base", "home", [row("gel", ask=100, ask_qty=20)])
        self.book("mid_base", "mid", [row("gel", bid=150, bid_qty=20)])
        trade = self.one(self.build(), "trade-gel-home-mid")
        self.assertEqual((trade["basis"]["units"], trade["basis"]["paid"], trade["basis"]["got"]), (20, 2000, 3000))
        self.assertEqual(trade["per_ship_hour"], trade["per_run"])                                                            # one load: an hour pays it once
        self.assertTrue(any("one load of 20 units closes the gap" in w for w in trade["warnings"]))
        stops = trade["route"]["stops"]
        self.assertEqual((stops[0]["at"], stops[0]["buy"][0]["qty"], stops[1]["at"], stops[1]["sell"][0]["item"]), ("home:core:home_base", 20, "mid:hub:mid_base", "gel"))
        self.book("mid_base", "mid", [row("gel", bid=150, bid_qty=900, depth=False)])
        thin = self.one(self.build(), "trade-gel-home-mid")
        self.assertEqual(thin["basis"]["units"], 1)                                                                           # a total is not a depth: one unit

    def test_a_recipe_is_costed_from_offers_and_from_our_storage(self):
        self.book("home_base", "home", [row("ore", ask=10, ask_qty=40), row("plate", bid=60, bid_qty=8)])
        craft = self.one(self.build(), "craft-press-ore-home")
        self.assertEqual((craft["basis"]["batches"], craft["needs"]), (8, "a craft step in the circuit runner"))
        self.assertEqual(craft["basis"]["inputs"], ["16 ore for 160 cr (depth at the best price)"])
        self.put("stock/storage.json", {"totals": {"by_station": {"home_base": {"ore": 500}}}})
        stored = self.one(self.build(), "craft-press-ore-home")
        self.assertEqual(stored["basis"]["inputs"], ["16 ore from our storage"])
        self.assertGreater(stored["per_run"], craft["per_run"])

    def test_a_herd_is_costed_from_the_loot_our_own_runs_sold(self):
        (self.root / "routes" / "hunt-old.json").write_text(json.dumps({"id": "hunt-old", "kind": "hunt", "title": "t", "place": "home:old", "species": ["glow_ray"],
                                                                        "sell_at": "home:core:home_base", "min_bid": 1, "kills": 4, "minutes": 40, "max_ships": 1,
                                                                        "min_creatures": 4}), encoding="ascii")
        (self.data / "routes" / "runs.jsonl").write_text(json.dumps({"route": "hunt-old", "kind": "hunt", "kills": 4, "minutes": 25, "goods": {"gel": 6}}) + "\n")
        self.put("wildlife/wild.json", {"system": "wild", "read_at": STAMP, "pois": {"wild_cloud": {"read_at": STAMP, "creatures":
                 [{"species": "glow_ray", "max_hull": 60}] * 5 + [{"species": "odd_slug", "max_hull": 60}] * 4 + [{"species": "big_whale", "max_hull": 220}] * 9}}})
        self.book("mid_base", "mid", [row("gel", bid=300, bid_qty=100)])
        book = self.build()
        hunt = self.one(book, "hunt-wild-cloud-glow-ray")
        self.assertEqual((hunt["basis"]["loot_a_kill"], hunt["basis"]["sold_at"], hunt["basis"]["jumps"]), ({"gel": 1.5}, "mid_base", 1))
        self.assertEqual((hunt["route"]["place"], hunt["route"]["species"], hunt["route"]["sell_at"], hunt["route"]["min_bid"]), ("wild:wild_cloud", ["glow_ray"], "mid:hub:mid_base", 240))
        self.assertEqual((hunt["route"]["alone"], hunt["route"]["requires"]), (True, {"empty_hold": True}))                  # beyond the police
        unknown = self.one(book, "hunt-wild-cloud-odd-slug")
        self.assertEqual((unknown["per_ship_hour"], "route" in unknown), (0, False))
        self.assertIn("one test hunt", unknown["needs"])
        whale = self.one(book, "hunt-wild-cloud-big-whale")                                                                 # 220 hull: a group of four starters (rule F9), never one ship
        self.assertEqual((whale["group"], "route" in whale, whale["basis"]["gauges"]["kills_up_to"]), (4, False, 280.0))
        self.assertTrue(whale["needs"].startswith("a group of 4 (rule F9, DECISIONS D228): waits for the dispatcher's group step"))

    def test_a_mission_says_what_it_asks_for_and_a_round_of_stations_gets_its_circuit(self):
        self.put("wildlife/wild.json", {"system": "wild", "read_at": STAMP, "pois": {"wild_cloud": {"read_at": STAMP, "creatures": [{"species": "glow_ray", "max_hull": 60}] * 5}}})
        self.put("missions/home_base.json", {"base": "home_base", "system": "home", "read_at": STAMP, "missions": [
            {"template_id": "say_hello", "title": "Say Hello", "rewards": {"credits": 4000}, "objectives": [
                {"type": "dock_at_base", "description": "Speak at Mid", "system_id": "mid", "target_base_id": "mid_base"}]},
            {"template_id": None, "title": "Station need: gel", "rewards": {"credits": 9000}, "objectives": [
                {"type": "deliver_item", "system_id": "home", "target_base_id": "home_base", "item_id": "gel", "quantity": 10}]},
            {"template_id": "far_look", "title": "Far Look", "rewards": {"credits": 500}, "objectives": [{"type": "visit_system", "description": "Visit Lost", "system_id": "lost"}]},
            {"template_id": "first_hunt", "title": "First Hunt", "rewards": {"credits": 1000}, "objectives": [
                {"type": "kill_creature", "description": "Hunt 3 Glow-Rays in a cloud", "quantity": 3}]},
            {"template_id": "big_hunt", "title": "Big Hunt", "rewards": {"credits": 1000}, "objectives": [
                {"type": "kill_creature", "description": "Hunt 4 Glow-Rays in a cloud", "quantity": 4}]},
            {"template_id": "unpaid", "title": "Unpaid", "rewards": {"credits": 0}, "objectives": []}]})
        self.put("fleet/onetime.json", [[1, "miner-1", "Say Hello", 4000], [2, "miner-1", "say_hello: goods bought", -100]])
        book = self.build()
        hello = self.one(book, "mission-say-hello-home")
        self.assertEqual((hello["pilots_booked"], hello["pilots_open"], hello["basis"]["jumps"]), (1, 1, 2))
        self.assertEqual([s["at"] for s in hello["route"]["stops"]], ["home:core:home_base", "mid:hub:mid_base", "home:core:home_base"])
        self.assertEqual((hello["route"]["stops"][0]["accept"], hello["route"]["once"], hello["route"]["one_time"]), (["say_hello"], True, ["Say Hello"]))
        (self.root / "routes" / (hello["route"]["id"] + ".json")).write_text(json.dumps(hello["route"]), encoding="ascii")
        self.assertEqual([e for e in routes.check(str(self.root))[0] if "index.md" not in e], [])
        need = self.one(book, "mission-station-need:-gel-home")
        self.assertIn("Seen: 5 glow_ray at wild:wild_cloud", need["basis"]["asks"][0])                                        # the catalog names the creature; our readings know a herd
        self.assertEqual((need["needs"], need["pilots_open"], "route" in need), ("a source of gel (a hunt: the herd is known)", None, False))
        first = self.one(book, "mission-first-hunt-home")
        self.assertEqual([s["at"] for s in first["route"]["stops"]], ["home:core:home_base", "home:core:home_base"])
        self.assertEqual(first["route"]["stops"][0]["hunt"], [{"at": "wild:wild_cloud", "species": ["glow_ray"], "kills": 3, "minutes": 35, "for": ["First Hunt"], "alone": True}])
        self.assertEqual((first["route"]["skip_if_booked"], first["basis"]["jumps"]), (["First Hunt"], 4))
        (self.root / "routes" / (first["route"]["id"] + ".json")).write_text(json.dumps(first["route"]), encoding="ascii")
        self.assertEqual([e for e in routes.check(str(self.root))[0] if "index.md" not in e], [])
        big = self.one(book, "mission-big-hunt-home")                                                                       # five rays do not carry four kills and two to spare
        self.assertEqual(("route" in big, big["needs"]), (False, "a herd of four or more for: Hunt 4 Glow-Rays in a cloud"))
        far = self.one(book, "mission-far-look-home")
        self.assertIn("a charted way to lost", far["needs"])
        self.assertFalse([c for c in book["candidates"] if "unpaid" in c["id"]])


class SmallBidTests(Tree):
    """A station's bid of a few units counts once an hour, never in every load (requests.log ENT-069)."""

    def history(self, rows):
        with open(self.data / "market" / "history.jsonl", "w", encoding="utf-8") as handle:
            for base, item, ago, units, bid in rows:
                handle.write(json.dumps({"t": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(NOW - ago)), "base": base, "item": item,
                                         "bid": bid, "bid_qty": units, "ask": 0, "ask_qty": 0}) + "\n")

    def test_a_bid_of_six_units_counts_six_units_an_hour_and_the_rest_sells_at_the_deep_bid(self):
        self.book("mid_base", "mid", [row("ore", bid=25, bid_qty=50000), row("dust", bid=200, bid_qty=6)])
        mine = self.one(self.build(), "mine-mid-belt")
        hour = 6 * 200 + 48 * LOADS * 25 - FUEL * LOADS                  # dust: six units at 200 an hour, the rest of it worth nothing; ore: all at 25
        self.assertEqual((mine["per_ship_hour"], mine["per_run"]), (round(hour), round(hour / LOADS)))
        self.assertLess(mine["per_run"], 48 * 25 + 6 * 200 - FUEL)                                                       # not six units at 200 in every load
        self.assertEqual(mine["basis"]["an_hour"], ["ore 101 of 101 units for 2526 cr", "dust 6 of 25 units for 1200 cr"])
        self.assertIn("dust: bid 200 x 6 at mid_base takes 6 of 25 units an hour", mine["warnings"])
        self.put("market/ladders.json", {"mid_base": {"dust": {"t": NOW, "bids": [[200, 6], [190, 4], [25, 99999]], "asks": []}}})
        read = self.one(self.build(), "mine-mid-belt")                    # the levels read: the next lower level takes the rest, as far as 80% of the best
        self.assertIn("dust: bid 200 x 6, 190 x 4 at mid_base takes 10 of 25 units an hour", read["warnings"])
        self.assertEqual(read["per_ship_hour"], round(6 * 200 + 4 * 190 + 48 * LOADS * 25 - FUEL * LOADS))

    def test_the_station_is_the_one_whose_bids_pay_most_for_the_hour_not_the_one_with_the_best_price(self):
        self.book("mid_base", "mid", [row("ore", bid=25, bid_qty=50000), row("dust", bid=200, bid_qty=6)])
        self.book("home_base", "home", [row("ore", bid=45, bid_qty=50000)])
        mine = self.one(self.build(), "mine-mid-belt")
        self.assertEqual((mine["basis"]["sold_at"], mine["route"]["station"]), ("home_base", "home:core:home_base"))
        self.assertEqual(mine["per_ship_hour"], round(48 * FAR * 45 - FAR_FUEL * FAR))
        self.assertGreater(mine["per_ship_hour"], round(6 * 200 + 48 * LOADS * 25 - FUEL * LOADS))                     # what the hour would bring at mid_base
        self.assertEqual(mine["route"]["sell"], [{"item": "ore", "min_price": 36}])

    def regain_on(self):
        maker.REGAIN = True                                                                # off in the fleet: `rates` averages every reading on record
        self.addCleanup(setattr, maker, "REGAIN", False)

    def test_a_regain_counts_for_nothing_while_the_switch_is_off(self):
        self.book("mid_base", "mid", [row("ore", bid=25, bid_qty=50000), row("dust", bid=200, bid_qty=6)])
        self.history([("mid_base", "dust", 7800, 6, 200), ("mid_base", "dust", 4200, 0, 200), ("mid_base", "dust", 600, 6, 200)])   # sold out, back in two hours
        self.assertFalse(maker.REGAIN)
        mine = self.one(self.build(), "mine-mid-belt")
        self.assertIn("dust: bid 200 x 6 at mid_base takes 6 of 25 units an hour", mine["warnings"])
        self.assertEqual(mine["per_ship_hour"], round(6 * 200 + 48 * LOADS * 25 - FUEL * LOADS))

    def test_a_measured_regain_extends_the_best_level(self):
        self.regain_on()
        self.book("mid_base", "mid", [row("ore", bid=25, bid_qty=50000), row("dust", bid=200, bid_qty=6)])
        self.book("home_base", "home", [row("ore", bid=45, bid_qty=40)])                 # 40 units stand at home_base: fewer than the 89 an hour brings
        self.history([("mid_base", "dust", 7800, 6, 200), ("mid_base", "dust", 4200, 0, 200), ("mid_base", "dust", 600, 6, 200)])   # sold out, back in two hours
        mine = self.one(self.build(), "mine-mid-belt")
        self.assertEqual(mine["basis"]["sold_at"], "mid_base")
        self.assertIn("dust: bid 200 x 6 (+3 regained an hour) at mid_base takes 9 of 25 units an hour", mine["warnings"])
        self.assertEqual(mine["per_ship_hour"], round(9 * 200 + 48 * LOADS * 25 - FUEL * LOADS))
        self.assertTrue(mine["basis"]["a_load"][1].endswith("(depth at the best price, 3 regained an hour by our readings)"))
        self.history([("home_base", "ore", 7800, 40, 45), ("home_base", "ore", 4200, 0, 45), ("home_base", "ore", 2400, 120, 45),
                      ("home_base", "ore", 600, 40, 45)])                                 # 120 came back in two hours: 60 an hour beside the 40 standing
        moved = self.one(self.build(), "mine-mid-belt")
        self.assertEqual((moved["basis"]["sold_at"], moved["per_ship_hour"]), ("home_base", round(48 * FAR * 45 - FAR_FUEL * FAR)))
        self.assertFalse([w for w in moved["warnings"] if "takes" in w])                    # 100 an hour carry the 89

    def test_without_a_measure_the_standing_depth_is_all_there_is(self):
        self.regain_on()
        self.book("mid_base", "mid", [row("ore", bid=25, bid_qty=50000), row("dust", bid=200, bid_qty=6)])
        for rows in ([("mid_base", "dust", 1200, 0, 200), ("mid_base", "dust", 600, 6, 200)],          # ten minutes apart: no measure
                     [("mid_base", "dust", 7800, 6, 200), ("mid_base", "dust", 600, 6, 200)],          # never taken, never back: the readings say nothing
                     [("home_base", "dust", 7800, 0, 200), ("home_base", "dust", 600, 60, 200)]):      # another station's regain is not this one's
            self.history(rows)
            self.assertIsNone(maker.regained(maker.load_world(str(self.data), self.root, NOW), "mid_base", "dust"))
            mine = self.one(self.build(), "mine-mid-belt")
            self.assertIn("dust: bid 200 x 6 at mid_base takes 6 of 25 units an hour", mine["warnings"])
            self.assertEqual(mine["per_ship_hour"], round(6 * 200 + 48 * LOADS * 25 - FUEL * LOADS))

    def test_the_route_file_sells_from_the_level_that_carries_the_hour(self):
        self.book("mid_base", "mid", [row("ore", bid=2, bid_qty=50000), row("dust", bid=200, bid_qty=6)])
        mine = self.one(self.build(), "mine-mid-belt")
        self.assertEqual(mine["route"]["sell"], [{"item": "ore", "min_price": 2}, {"item": "dust", "min_price": 160}])  # a bid of 2 cr is no floor of 1
        self.put("market/ladders.json", {"mid_base": {"dust": {"t": NOW, "bids": [[200, 6], [190, 4], [180, 900]], "asks": []}}})
        read = self.one(self.build(), "mine-mid-belt")
        self.assertEqual(read["route"]["sell"][1], {"item": "dust", "min_price": 144})     # the hour reaches 180 x 900: the runner must sell there
        (self.root / "routes" / (read["route"]["id"] + ".json")).write_text(json.dumps(read["route"]), encoding="ascii")
        self.assertEqual([e for e in routes.check(str(self.root))[0] if "index.md" not in e], [])

    def test_trade_and_craft_keep_their_figures_when_a_bid_regains(self):
        self.regain_on()
        self.book("home_base", "home", [row("gel", ask=100, ask_qty=20), row("ore", ask=10, ask_qty=40), row("plate", bid=60, bid_qty=8)])
        self.book("mid_base", "mid", [row("gel", bid=150, bid_qty=20)])
        before = [c for c in self.build()["candidates"] if c["kind"] != "mine"]
        self.history([("mid_base", "gel", 7800, 20, 150), ("mid_base", "gel", 4200, 0, 150), ("mid_base", "gel", 600, 20, 150),
                      ("home_base", "plate", 7800, 8, 60), ("home_base", "plate", 4200, 0, 60), ("home_base", "plate", 600, 8, 60)])
        after = [c for c in self.build()["candidates"] if c["kind"] != "mine"]
        self.assertEqual(sorted(c["kind"] for c in before), ["craft", "trade"])
        self.assertEqual(after, before)                                                    # a regain is read for a mine candidate only
        trade = self.one({"candidates": after}, "trade-gel-home-mid")
        self.assertEqual((trade["basis"]["units"], trade["basis"]["paid"], trade["basis"]["got"], trade["per_ship_hour"]), (20, 2000, 3000, trade["per_run"]))


class ReadingTests(Tree):
    def test_a_census_count_of_pirates_is_read_as_a_number(self):
        self.put("wildlife/wild.json", {"system": "wild", "read_at": STAMP, "pois": {
            "wild_cloud": {"read_at": STAMP, "pirates": 1, "pilots": 0, "creatures": [{"species": "glow_ray", "max_hull": 60}] * 5},
            "wild_rift": {"read_at": STAMP, "pirates": [{"id": "p1"}, {"id": "p2"}], "creatures": [{"species": "glow_ray", "max_hull": 60}] * 5}}})
        world = maker.load_world(str(self.data), self.root, NOW)
        self.assertEqual(sorted((h["poi"], h["pirates"]) for h in world["herds"]), [("wild_cloud", 1), ("wild_rift", 2)])
        self.assertEqual(self.build()["skipped"], [])

    def test_one_bad_file_costs_its_own_reading_not_the_pass(self):
        self.put("wildlife/bad.json", {"system": "bad", "read_at": STAMP, "pois": {"odd": 5}})
        self.put("wildlife/wild.json", {"system": "wild", "read_at": STAMP, "pois": {"wild_cloud": {"read_at": STAMP, "creatures": [{"species": "glow_ray", "max_hull": 60}] * 5}}})
        book = self.build()
        self.assertEqual(book["read"]["herds"], 1)
        self.assertEqual(len(book["skipped"]), 1)
        self.assertTrue(book["skipped"][0].startswith("wildlife/bad.json: AttributeError"))


class ServiceTests(Tree):
    def test_a_pass_reads_the_highest_version_and_fetches_no_catalog(self):
        # 2026-11-16: scripts/catalog-refresh.py fetches the catalog, checks it and keeps it by version; the route maker
        # only reads the newest copy (its own daily download, unchecked, is gone)
        self.put("catalog/0.9.json", {"version": "0.9", "items": [], "recipes": []})
        os.utime(self.data / "catalog" / "0.9.json", (time.time() + 60, time.time() + 60))         # written last, and the older version
        self.assertEqual(self.build()["catalog"], "1.0")
        self.assertFalse(hasattr(maker, "refresh_catalog"))
        self.assertNotIn("api/catalog.json", (FLEET / "routemaker.py").read_text(encoding="ascii"))

    def test_a_pass_reads_only_and_the_list_prints_for_a_member(self):
        self.book("home_base", "home", [row("ore", bid=10, bid_qty=5000)])
        before = sorted(str(p) for p in self.root.rglob("*"))
        book = self.build(look=lambda pilot, item: None)
        self.assertEqual(before, sorted(str(p) for p in self.root.rglob("*")))                                                # nothing written into the repository's folder
        self.assertEqual((book["ladders_read"], book["read"]["fields"], book["catalog"]), (0, 2, "1.0"))
        self.assertEqual(book["assumptions"]["cargo"], {"value": 60, "from": "median hold of 2 ships"})
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            maker.show(book, "Zero", "", 5)
        text = out.getvalue()
        self.assertIn("MINE: 1 candidate(s)", text)                                                                           # the ice field has no bid: no candidate
        self.assertIn("MISSION: 0 candidate(s)", text)
        self.assertNotIn("TRADE:", text)                                                                                      # a member sees the kinds of its division
        self.assertIn("mine-mid-belt", text)



class CatalogFileTests(unittest.TestCase):
    def test_only_a_file_named_by_a_version_is_the_catalog(self):
        with tempfile.TemporaryDirectory(prefix="routemaker-catalog-") as temp:
            folder = Path(temp) / "catalog"
            folder.mkdir()
            self.assertEqual(maker.newest_catalog(temp).name, "none.json")
            for age, name in ((300, "0.9.0.json"), (200, "0.10.0.json"), (100, "ammo.json")):      # ammo.json is the newest file, and no catalog
                (folder / name).write_text("[]" if name == "ammo.json" else "{}")
                os.utime(folder / name, (time.time() - age, time.time() - age))
            self.assertEqual(maker.newest_catalog(temp).name, "0.10.0.json")

    def test_the_highest_version_wins_whatever_the_file_times(self):
        # 2026-11-16: it took the newest file time; catalog-refresh.py keeps two versions side by side
        with tempfile.TemporaryDirectory(prefix="routemaker-catalog-") as temp:
            folder = Path(temp) / "catalog"
            self.assertEqual(maker.newest_catalog(temp), folder / "none.json")                      # no folder: what it gave before
            folder.mkdir()
            for name in ("0.99.0.json", "0.100.0.json", "ammo.json", "refresh.json"):
                (folder / name).write_text("{}")
            for older, newer in (("0.99.0.json", "0.100.0.json"), ("0.100.0.json", "0.99.0.json")):
                for age, name in ((300, older), (200, newer), (100, "ammo.json"), (50, "refresh.json")):
                    os.utime(folder / name, (time.time() - age, time.time() - age))
                self.assertEqual(maker.newest_catalog(temp).name, "0.100.0.json", "%s written last" % newer)


def drone(name, guns=("pulse_laser_i",), levels=(4, 2, 3), hull=75, shield=130):
    """A ship's live file as the fleet collector writes it: its weapons, its Gunnery, Weapons and Tactics, hull and shield."""
    return {"name": name, "modules": [{"kind": "weapon", "slot": "weapon", "type": g} for g in guns], "max_hull": hull, "max_shield": shield,
            "skills": {k: {"level": v} for k, v in zip(("gunnery", "weapons", "tactics"), levels)}}


    def test_strict_classes_mine_candidates_omit_sell_and_cap_three(self):
        (self.data / "fleet" / "strict-classes-on").write_text("", encoding="ascii")
        self.addCleanup(lambda: (self.data / "fleet" / "strict-classes-on").unlink(missing_ok=True))
        mine = self.one(self.build(), "mine-mid-belt")
        self.assertNotIn("sell", mine["route"])
        self.assertEqual(mine["route"]["max_ships"], 3)
        self.assertEqual(mine["route"]["lift_to"], 3)
        self.assertGreater(mine["per_ship_hour"], 0)
        (self.root / "routes" / (mine["route"]["id"] + ".json")).write_text(json.dumps(mine["route"]), encoding="ascii")
        self.assertEqual([e for e in routes.check(str(self.root))[0] if "index.md" not in e], [])

class GaugeTests(Tree):
    """Rule F9: a herd is hunted by the gauges of the ships that would fly it, never by a fixed 100 hull."""

    def setUp(self):
        super().setUp()
        (self.data / "fleet" / "ships").mkdir()
        self.put("catalog/1.0.json", {"version": "1.0", "items": [{"id": "gel", "size": 1}, {"id": "pulse_laser_i", "type": "weapon", "damage": 10, "cooldown": 1},
                                                                 {"id": "big_gun", "type": "weapon", "damage": 30, "cooldown": 1}], "recipes": []})
        self.book("mid_base", "mid", [row("gel", bid=300, bid_qty=100)])
        herd = []
        for species, hull, role in (("calm_ray", 70, "grazer"), ("slag_tortoise", 90, "grazer"), ("aeonbear", 120, "grazer"), ("cloudwhale", 3304, "grazer"),
                                    ("mantis", 60, "predator"), ("pilot_whale", 220, "grazer")):
            herd += [{"species": species, "role": role, "hull": hull, "max_hull": hull}] * 6
        self.put("wildlife/mid.json", {"system": "mid", "read_at": STAMP, "pois": {"mid_cloud": {"read_at": STAMP, "creatures": herd}}})
        runs = []
        for species in ("calm_ray", "slag_tortoise", "pilot_whale"):                                                       # loot our runs sold
            rid = "hunt-old-" + species
            (self.root / "routes" / (rid + ".json")).write_text(json.dumps({"id": rid, "kind": "hunt", "title": "t", "place": "home:old", "species": [species],
                                                                            "sell_at": "home:core:home_base", "min_bid": 1, "kills": 4, "minutes": 40,
                                                                            "max_ships": 1, "min_creatures": 4}), encoding="ascii")
            runs.append(json.dumps({"route": rid, "kind": "hunt", "kills": 4, "minutes": 25, "goods": {"gel": 6}}))
        (self.data / "routes" / "runs.jsonl").write_text("\n".join(runs) + "\n")

    def fleet(self, ships):
        self.put("fleet/fleet.json", {"ships": [{"name": s["name"], "cargo_capacity": 60, "status": "connected"} for s in ships]})
        for ship in ships:
            self.put("fleet/ships/%s.json" % ship["name"], ship)

    def hunts(self, book):
        return {c["id"].replace("hunt-mid-cloud-", ""): c for c in book["candidates"] if c["kind"] == "hunt"}

    def test_one_drone_hunts_what_it_kills_and_stands_and_a_group_herd_waits_without_a_route(self):
        self.fleet([drone("drone-1"), drone("drone-2"), drone("drone-3")])           # each 10 x 1.09 = 10.9 a tick: kills up to 76.3 hull, stands up to 102.5
        hunts = self.hunts(self.build())
        calm = hunts["calm-ray"]                                                    # 70 hull: one ship alone, as before
        self.assertEqual((calm.get("group"), calm.get("needs"), calm["route"]["species"], "max_prey_hull" in calm["route"]), (None, None, ["calm_ray"], False))
        slag = hunts["slag-tortoise"]                                               # 90 hull: one ship of the 100-hull rule, now a group of two
        self.assertEqual((slag.get("group"), "route" in slag), (2, False))
        self.assertEqual(slag.get("needs"), "a group of 2 (rule F9, DECISIONS D228): waits for the dispatcher's group step")
        self.assertAlmostEqual(slag["per_ship_hour"], calm["per_ship_hour"] / 2, delta=1)   # the same loot, shared by two ships
        self.assertEqual({k: slag["basis"]["gauges"][k] for k in ("species_hull", "group", "kills_up_to", "stands_up_to")},
                         {"species_hull": 90, "group": 2, "kills_up_to": 152.6, "stands_up_to": 205.0})
        self.assertFalse(any(c.get("route") for k, c in hunts.items() if k.startswith("aeonbear")))   # 120 hull: never one ship
        self.assertEqual(hunts["aeonbear"]["group"], 2)
        self.assertEqual((hunts["mantis"]["group"], hunts["mantis"]["basis"]["gauges"]["weight"]), (2, 120))  # a predator of 60 weighs 120
        self.assertEqual(hunts["pilot-whale"]["group"], 3)                          # 220 hull: three ships (228.9 and 307.5)
        self.assertNotIn("cloudwhale", hunts)                                       # beyond twenty ships: no candidate

    def test_a_strong_ship_hunts_above_100_alone_and_its_route_names_the_prey_hull(self):
        self.fleet([drone("drone-1", guns=("big_gun", "big_gun"), shield=400)])    # 60 x 1.09 = 65.4 a tick: kills up to 457.8; stands up to 237.5
        hunts = self.hunts(self.build())
        self.assertIn("pilot-whale", hunts)                                        # 220 hull: no candidate under the 100-hull rule
        whale = hunts["pilot-whale"]
        self.assertEqual((whale.get("group"), whale["route"]["max_prey_hull"], whale["route"]["max_ships"]), (None, 220, 1))
        (self.root / "routes" / (whale["route"]["id"] + ".json")).write_text(json.dumps(whale["route"]), encoding="ascii")
        self.assertEqual([e for e in routes.check(str(self.root))[0] if "index.md" not in e], [])
        self.put("missions/home_base.json", {"base": "home_base", "system": "home", "read_at": STAMP, "missions": [
            {"template_id": "whale_hunt", "title": "Whale Hunt", "rewards": {"credits": 1000}, "objectives": [
                {"type": "kill_creature", "description": "Hunt 3 Pilot Whales", "quantity": 3}]}]})
        hunt = self.one(self.build(), "mission-whale-hunt-home")                     # a circuit's hunt step takes nothing above 100 hull
        self.assertEqual((hunt["needs"], "route" in hunt), ("a herd of four or more for: Hunt 3 Pilot Whales", False))

    def test_a_mission_herd_is_one_typical_ship_s_prey(self):
        self.fleet([drone("drone-1"), drone("drone-2")])
        self.put("missions/home_base.json", {"base": "home_base", "system": "home", "read_at": STAMP, "missions": [
            {"template_id": "calm_hunt", "title": "Calm Hunt", "rewards": {"credits": 1000}, "objectives": [
                {"type": "kill_creature", "description": "Hunt 3 Calm Rays", "quantity": 3}]},
            {"template_id": "slag_hunt", "title": "Slag Hunt", "rewards": {"credits": 1000}, "objectives": [
                {"type": "kill_creature", "description": "Hunt 3 Slag Tortoises", "quantity": 3}]}]})
        book = self.build()
        calm = self.one(book, "mission-calm-hunt-home")
        self.assertEqual(calm["route"]["stops"][0]["hunt"][0]["species"], ["calm_ray"])
        slag = self.one(book, "mission-slag-hunt-home")                              # 90 hull: no herd one ship can take
        self.assertEqual((slag.get("needs"), "route" in slag), ("a herd of four or more for: Hunt 3 Slag Tortoises", False))



if __name__ == "__main__":
    unittest.main()

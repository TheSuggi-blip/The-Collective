"""game/fleet/routemaker.py on a disposable data folder and chart: every kind of candidate, the depth of a book, the route files it writes. No engine, no network."""

import contextlib
import importlib.util
import io
import json
from pathlib import Path
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


maker, routes = load("routemaker"), load("routes")
NOW = 1_800_000_000
STAMP = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(NOW - 600))
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
        self.assertEqual(mine["basis"]["a_load"], ["ore 48 of 48 units for 576 cr (depth at the best price)", "dust 10 of 12 units for 30 cr (depth at the best price)"])
        self.assertIn("dust: the bids take 10 of 12 units a load", mine["warnings"])
        self.assertEqual((mine["route"]["belt"], mine["route"]["station"], mine["route"]["max_ships"]), ("mid:mid_belt", "mid:hub:mid_base", 1))
        ice = self.one(book, "mine-wild-ice")
        self.assertEqual(ice["route"]["requires"], {"module": "ice_harvester_i"})
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
        unknown = self.one(book, "hunt-wild-cloud-odd-slug")
        self.assertEqual((unknown["per_ship_hour"], "route" in unknown), (0, False))
        self.assertIn("one test hunt", unknown["needs"])
        self.assertFalse([c for c in book["candidates"] if "big-whale" in c["id"]])                                           # prey above 100 hull is no candidate

    def test_a_mission_says_what_it_asks_for_and_a_round_of_stations_gets_its_circuit(self):
        self.put("wildlife/wild.json", {"system": "wild", "read_at": STAMP, "pois": {"wild_cloud": {"read_at": STAMP, "creatures": [{"species": "glow_ray", "max_hull": 60}] * 5}}})
        self.put("missions/home_base.json", {"base": "home_base", "system": "home", "read_at": STAMP, "missions": [
            {"template_id": "say_hello", "title": "Say Hello", "rewards": {"credits": 4000}, "objectives": [
                {"type": "dock_at_base", "description": "Speak at Mid", "system_id": "mid", "target_base_id": "mid_base"}]},
            {"template_id": None, "title": "Station need: gel", "rewards": {"credits": 9000}, "objectives": [
                {"type": "deliver_item", "system_id": "home", "target_base_id": "home_base", "item_id": "gel", "quantity": 10}]},
            {"template_id": "far_look", "title": "Far Look", "rewards": {"credits": 500}, "objectives": [{"type": "visit_system", "description": "Visit Lost", "system_id": "lost"}]},
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
        far = self.one(book, "mission-far-look-home")
        self.assertIn("a charted way to lost", far["needs"])
        self.assertFalse([c for c in book["candidates"] if "unpaid" in c["id"]])


class ServiceTests(Tree):
    def test_the_catalog_is_fetched_once_a_day_and_kept_by_version(self):
        raw = json.dumps({"version": "2.0/x", "items": [], "recipes": []}).encode()
        calls = []
        fetch = lambda: calls.append(1) or raw
        for path in (self.data / "catalog").glob("*.json"):
            path.unlink()
        self.assertEqual(maker.refresh_catalog(str(self.data), NOW, fetch), "fetched 2.0x")
        self.assertEqual(maker.refresh_catalog(str(self.data), time.time(), fetch), "fresh")
        self.assertEqual((len(calls), [p.name for p in (self.data / "catalog").iterdir()]), (1, ["2.0x.json"]))
        self.assertTrue(maker.refresh_catalog(str(self.data), time.time() + 2 * maker.CATALOG_EVERY, lambda: b"not json").startswith("not fetched"))

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


if __name__ == "__main__":
    unittest.main()

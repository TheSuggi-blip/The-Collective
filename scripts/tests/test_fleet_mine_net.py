import json
import sys
import tempfile
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "game" / "fleet"))
import mine
import mine_net


class MineNetTests(unittest.TestCase):
    def _world(self):
        return {
            "adj": {"sys_a": {"sys_b", "sys_c"}, "sys_b": {"sys_a"}, "sys_c": {"sys_a"}},
            "systems": {
                "sys_a": {"empire": "voidborn", "stronghold": False},
                "sys_b": {"empire": "voidborn", "stronghold": False},
                "sys_c": {"empire": "", "stronghold": False},
            },
            "stations_by_sys": {
                "sys_a": [("sys_a", "st_a", "base_a")],
                "sys_b": [("sys_b", "st_b", "base_b")],
            },
            "fields": [
                {"system": "sys_a", "poi": "belt_iron", "resource": "iron_ore", "remaining": 90000, "max_remaining": 100000, "richness": 50, "t": 1},
                {"system": "sys_b", "poi": "belt_carbon", "resource": "carbon_ore", "remaining": 8000, "max_remaining": 20000, "richness": 40, "t": 1},
                {"system": "sys_a", "poi": "belt_ice", "resource": "nitrogen_ice", "remaining": 20000, "max_remaining": 50000, "richness": 40, "t": 1},
                {"system": "sys_b", "poi": "belt_dry", "resource": "silicon_ore", "remaining": 1000, "max_remaining": 10000, "richness": 30, "t": 1},
                {"system": "sys_c", "poi": "belt_lawless", "resource": "silicon_ore", "remaining": 9000, "max_remaining": 10000, "richness": 60, "t": 1},
            ],
            "pirates": set(),
            "item_vals": {"iron_ore": 4.0, "carbon_ore": 12.0, "nitrogen_ice": 6.0, "silicon_ore": 20.0},
            "shortages": {"carbon_ore": 5000, "silicon_ore": 2000},
            "full_items": {"iron_ore"},
        }

    def test_live_floor_breach_detection(self):
        res = [
            {"resource_id": "carbon_ore", "remaining": 2900, "max_remaining": 20000},
            {"resource_id": "iron_ore", "remaining": 9000, "max_remaining": 20000},
        ]
        hit = mine.check_floor_breached(res, min_left_pct=15.0, floor_resource="carbon_ore")
        self.assertIsNotNone(hit)
        self.assertEqual(hit[0], "carbon_ore")
        self.assertIsNone(mine.check_floor_breached(res, min_left_pct=15.0, floor_resource="iron_ore"))

    def test_tool_matching_deficit_priority_and_policed_gate(self):
        pol = dict(mine_net.DEFAULT_POLICY, policed_only=True, allow_lawless_for_deficit=False)
        w = self._world()
        ore_pilot = {"name": "miner-1", "system": "sys_a", "tier": 0, "modules": [{"type": "mining_laser_i"}]}
        cands = mine_net.score_belt_candidates(ore_pilot, w, pol, {}, {})
        self.assertEqual(cands[0]["resource"], "carbon_ore")
        self.assertEqual(cands[0]["tier"], "deficit")
        self.assertNotIn("sys_b:belt_dry", [c["belt_key"] for c in cands])
        self.assertNotIn("sys_c:belt_lawless", [c["belt_key"] for c in cands])
        ice_pilot = {"name": "miner-2", "system": "sys_a", "tier": 0, "modules": [{"type": "ice_harvester_i"}]}
        ic = mine_net.score_belt_candidates(ice_pilot, w, pol, {}, {})
        self.assertEqual([c["resource"] for c in ic], ["nitrogen_ice"])
        t1_pilot = {"name": "miner-3", "system": "sys_a", "tier": 1, "modules": [{"type": "mining_laser_iii"}]}
        t1c = mine_net.score_belt_candidates(t1_pilot, w, pol, {}, {})
        self.assertIn("sys_c:belt_lawless", [c["belt_key"] for c in t1c])

    def test_atomic_claims_adaptive_cap_and_floor_cooldown(self):
        pol = dict(mine_net.DEFAULT_POLICY, max_per_belt=3, units_per_ship_run=250)
        self.assertEqual(mine_net.adaptive_belt_cap(1800, 10000, pol), 1)
        self.assertEqual(mine_net.adaptive_belt_cap(5000, 10000, pol), 3)
        with tempfile.TemporaryDirectory() as tmp:
            now_t = time.time()
            self.assertTrue(mine_net.claim_belt_atomic(tmp, "miner-1", "sys_b:belt_carbon", 1, pol, now_t=now_t))
            self.assertFalse(mine_net.claim_belt_atomic(tmp, "miner-2", "sys_b:belt_carbon", 1, pol, now_t=now_t))
            mine_net.release_belt_claim(tmp, "miner-1", cooldown_belt="sys_b:belt_carbon", cooldown_minutes=90, policy=pol, now_t=now_t)
            self.assertFalse(mine_net.claim_belt_atomic(tmp, "miner-2", "sys_b:belt_carbon", 1, pol, now_t=now_t + 60))
            self.assertTrue(mine_net.claim_belt_atomic(tmp, "miner-2", "sys_b:belt_carbon", 1, pol, now_t=now_t + 91 * 60))

    def test_global_optimal_assignment(self):
        pol = dict(mine_net.DEFAULT_POLICY, policed_only=True, allow_lawless_for_deficit=False)
        w = self._world()
        p1 = {"name": "miner-1", "system": "sys_a", "tier": 0, "modules": [{"type": "mining_laser_i"}]}
        p2 = {"name": "miner-2", "system": "sys_b", "tier": 0, "modules": [{"type": "mining_laser_i"}]}
        assigned = mine_net.assign_optimal_mines([p1, p2], w, pol, {}, {})
        self.assertEqual(assigned["miner-2"]["belt_key"], "sys_b:belt_carbon")


class MineNetLiveSchemaTests(unittest.TestCase):
    """The store's own tables (2026-11-24): stations has no id or poi column; places maps a station to its base;
    supply_status carries the stock. A schema fault in one table must not leave the fields unread."""

    def _db(self, tmp):
        import sqlite3
        (Path(tmp) / "store").mkdir()
        con = sqlite3.connect(str(Path(tmp) / "store" / "read.db"))
        con.executescript("""
            CREATE TABLE lanes (a TEXT, b TEXT, src TEXT);
            CREATE TABLE systems (id TEXT, name TEXT, x REAL, y REAL, empire TEXT, home INT, stronghold INT, jumps INT, src TEXT);
            CREATE TABLE stations (name TEXT, kind TEXT, system TEXT, tag TEXT, faction TEXT, empire TEXT, condition TEXT,
                                   services TEXT, wrecked INT, mobile INT, src TEXT);
            CREATE TABLE places (system TEXT, poi TEXT, kind TEXT, name TEXT, class TEXT, base TEXT, x REAL, y REAL, t REAL, src TEXT);
            CREATE TABLE fields (system TEXT, poi TEXT, resource TEXT, remaining INT, max_remaining INT, richness REAL, t REAL, src TEXT);
            CREATE TABLE supply_status (chain TEXT, item TEXT, place TEXT, keep INT, stock INT, status TEXT);
            INSERT INTO lanes VALUES ('sys_a', 'sys_b', ''), ('sys_a', 'sys_c', '');
            INSERT INTO systems VALUES ('sys_a', 'A', 0, 0, 'voidborn', 0, 0, 0, ''), ('sys_b', 'B', 0, 0, 'voidborn', 0, 0, 1, ''),
                                       ('sys_c', 'C', 0, 0, 'voidborn', 0, 0, 1, '');
            INSERT INTO stations VALUES ('Store A', 'station', 'sys_a', '', '', 'voidborn', '', 'market,storage,refuel', 0, 0, ''),
                                        ('Their Outpost', 'outpost', 'sys_c', '', '', '', '', '', 0, 0, '');
            INSERT INTO places VALUES ('sys_a', 'st_a', 'station', 'Store A', '', 'base_a', 0, 0, 0, ''),
                                      ('sys_c', 'st_c', 'station', 'Their Outpost', '', 'base_c', 0, 0, 0, ''),
                                      ('sys_b', 'belt_iron', 'asteroid_belt', 'Belt', '', '', 0, 0, 0, '');
            INSERT INTO fields VALUES ('sys_b', 'belt_iron', 'iron_ore', 90000, 100000, 40, 1, ''),
                                      ('sys_b', 'belt_iron', 'copper_ore', 90000, 100000, 30, 1, '');
            INSERT INTO supply_status VALUES ('iron-ore', 'iron_ore', 'fleet', 60000, 49000, 'short');
        """)
        con.commit()
        con.close()

    def test_live_schema_reads_fields_stations_and_supply(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._db(tmp)
            pol = dict(mine_net.DEFAULT_POLICY)
            w = mine_net.load_graph_and_world(tmp, tmp, pol, now_t=time.time())
            self.assertEqual(len(w["fields"]), 2)
            self.assertEqual(w["stations_by_sys"], {"sys_a": [("sys_a", "st_a", "base_a")]})
            self.assertEqual(w["shortages"].get("iron_ore"), 11000)

    def test_deposit_allowlist_and_market_tier_off(self):
        with tempfile.TemporaryDirectory() as tmp:
            self._db(tmp)
            pol = dict(mine_net.DEFAULT_POLICY, deposit_stations=["sys_b:st_b:base_b"], market_tier=False)
            w = mine_net.load_graph_and_world(tmp, tmp, pol, now_t=time.time())
            self.assertEqual(w["stations_by_sys"], {"sys_b": [("sys_b", "st_b", "base_b")]})
            pilot = {"name": "miner-1", "system": "sys_a", "tier": 0, "modules": [{"type": "mining_laser_i"}]}
            cands = mine_net.score_belt_candidates(pilot, w, pol, {}, {})
            self.assertEqual([(c["resource"], c["tier"], c["station"]) for c in cands],
                             [("iron_ore", "deficit", "sys_b:st_b:base_b")])



    def test_books_bid_and_static_mine_order_occupancy_cap(self):
        """books.bid reads cleanly without stderr and active static mine orders count toward max_per_belt."""
        import io, contextlib, sqlite3, tempfile, json
        with tempfile.TemporaryDirectory() as tmp:
            data = Path(tmp) / "data"
            repo = Path(tmp) / "repo"
            (data / "store").mkdir(parents=True, exist_ok=True)
            (data / "fleet" / "orders").mkdir(parents=True, exist_ok=True)
            (repo / "game" / "routes").mkdir(parents=True, exist_ok=True)

            con = sqlite3.connect(str(data / "store" / "read.db"))
            con.executescript("""
                CREATE TABLE lanes (a TEXT, b TEXT);
                CREATE TABLE systems (id TEXT, empire TEXT, stronghold INTEGER);
                CREATE TABLE places (system TEXT, poi TEXT, kind TEXT, name TEXT, base TEXT);
                CREATE TABLE fields (system TEXT, poi TEXT, resource TEXT, remaining INTEGER, max_remaining INTEGER, richness INTEGER, t INTEGER);
                CREATE TABLE items (id TEXT, base_value REAL);
                CREATE TABLE books (base TEXT, system TEXT, item TEXT, bid REAL, bid_qty INTEGER);
                INSERT INTO systems VALUES ('s1', 'voidborn', 0);
                INSERT INTO places VALUES ('s1', 'st1', 'station', 'Station 1', 'base1');
                INSERT INTO fields VALUES ('s1', 'b_full', 'iron_ore', 8000, 10000, 5, 1795500000);
                INSERT INTO items VALUES ('iron_ore', 10.0);
                INSERT INTO books VALUES ('base1', 's1', 'iron_ore', 45.0, 500);
            """)
            con.commit()
            con.close()

            stderr_buf = io.StringIO()
            with contextlib.redirect_stderr(stderr_buf):
                world = mine_net.load_graph_and_world(str(data), str(repo), dict(mine_net.DEFAULT_POLICY))
            self.assertEqual(stderr_buf.getvalue(), "")
            self.assertEqual(world["item_vals"]["iron_ore"], 45.0)

            # 3 active static mine orders on s1:b_full must block a 4th mine_net claim (cap=3)
            (repo / "game" / "routes" / "mine-iron-s1.json").write_text(json.dumps({"kind": "mine", "belt": "s1:b_full"}), encoding="ascii")
            for i in range(1, 4):
                (data / "fleet" / "orders" / f"miner-{i}.json").write_text(
                    json.dumps({"pilot": f"miner-{i}", "what": "mine mine-iron-s1"}), encoding="ascii"
                )
            st_counts = mine_net.count_static_mine_orders(str(repo), str(data))
            self.assertEqual(st_counts.get("s1:b_full"), 3)
            pol = dict(mine_net.DEFAULT_POLICY, max_per_belt=3)
            self.assertFalse(mine_net.claim_belt_atomic(str(data), "miner-99", "s1:b_full", 3, pol, repo_root=str(repo)))
            cands = mine_net.score_belt_candidates(
                {"name": "miner-99", "system": "s1", "modules": ["mining_laser_i"]},
                world, pol, {}, {}, static_counts=st_counts,
            )
            self.assertEqual(cands, [])


    def test_four_tier_craft_demand_priority(self):
        """Tier 1 deficit (12x) > Tier 2 craft_demand (6x) > Tier 3 market (2x) > Tier 4 xp (0.25x)."""
        world = {
            "adj": {"s1": {"s2"}, "s2": {"s1"}},
            "systems": {"s1": {"empire": "voidborn", "stronghold": False}},
            "stations_by_sys": {"s1": [("s1", "st1", "b1")]},
            "fields": [
                {"system": "s1", "poi": "p_mkt", "resource": "copper_ore", "remaining": 8000, "max_remaining": 10000},
                {"system": "s1", "poi": "p_craft", "resource": "silicon_ore", "remaining": 8000, "max_remaining": 10000},
                {"system": "s1", "poi": "p_def", "resource": "iron_ore", "remaining": 8000, "max_remaining": 10000},
            ],
            "pirates": set(),
            "item_vals": {"copper_ore": 20.0, "silicon_ore": 20.0, "iron_ore": 20.0},
            "shortages": {"iron_ore": 5000},
            "craft_demand": {"silicon_ore": 5000},
            "full_items": set(),
        }
        pol = dict(mine_net.DEFAULT_POLICY, market_tier=True, craft_demand_tier=True)
        cands = mine_net.score_belt_candidates({"name": "miner-1", "system": "s1", "modules": ["mining_laser_i"]}, world, pol, {}, {})
        self.assertEqual([c["tier"] for c in cands], ["deficit", "craft_demand", "market"])

    def test_holdings_deduction_and_strict_deficit_over_high_price_craft_demand(self):
        """Holdings stock suppresses stocked craft raw inputs (water_ice), and low-price deficit strictly beats high-price craft_demand."""
        import sqlite3
        from pathlib import Path
        sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "game" / "fleet"))
        import craft_net

        with tempfile.TemporaryDirectory() as td:
            data, repo = Path(td) / "data", Path(td) / "repo"
            (data / "store").mkdir(parents=True)
            (repo / "game").mkdir(parents=True)
            db = data / "store" / "read.db"
            con = sqlite3.connect(str(db))
            con.executescript("""
                CREATE TABLE recipes (id TEXT, name TEXT, facility_only INTEGER);
                CREATE TABLE recipe_inputs (recipe TEXT, item TEXT, units INTEGER);
                CREATE TABLE recipe_outputs (recipe TEXT, item TEXT, units INTEGER);
                CREATE TABLE items (id TEXT, base_value REAL);
                CREATE TABLE holdings (pilot TEXT, member TEXT, place TEXT, item TEXT, units INTEGER, t INTEGER, src TEXT);
                CREATE TABLE supply_status (item TEXT, stock INTEGER, keep INTEGER);
                INSERT INTO recipes VALUES ('r_ice', 'Coolant', 0), ('r_si', 'Chip', 0);
                INSERT INTO recipe_inputs VALUES ('r_ice', 'water_ice', 10), ('r_si', 'silicon_ore', 10);
                INSERT INTO recipe_outputs VALUES ('r_ice', 'coolant_cell', 1), ('r_si', 'microchip', 1);
                INSERT INTO items VALUES ('water_ice', 56.0), ('silicon_ore', 56.0), ('iron_ore', 5.0);
                INSERT INTO holdings VALUES ('m1', 'Zero', 'hub', 'water_ice', 67000, 1795500000, 'stock/storage.json');
                INSERT INTO holdings VALUES ('m1', 'Zero', 'hub', 'iron_ore', 153000, 1795500000, 'stock/storage.json');
                INSERT INTO supply_status VALUES ('iron_ore', 53000, 60000);
            """)
            con.commit()
            con.close()
            (repo / "game" / "craft-demand.json").write_text(json.dumps({
                "enabled": True, "auto_discover_profitable": False,
                "raw_input_caps": {"water_ice": 30000, "silicon_ore": 15000},
                "industrial_targets": {"coolant_cell": {"cap": 500}, "microchip": {"cap": 500}},
            }), encoding="ascii")
            cw = craft_net.load_craft_world(str(data), str(repo), {"demand_file": "game/craft-demand.json"})
            self.assertEqual(cw["stock_by_item"]["water_ice"], 67000)
            self.assertEqual(cw["stock_by_item"]["iron_ore"], 53000)  # supply_status usable overrides raw holdings
            raw_dem = craft_net.expand_demand_raw_inputs(cw)
            self.assertNotIn("water_ice", raw_dem)
            self.assertIn("silicon_ore", raw_dem)

        # Low-value 5 cr deficit (iron_ore) MUST beat high-value 56 cr craft_demand (silicon_ore)
        world = {
            "adj": {"s1": {"s2"}, "s2": {"s1"}},
            "systems": {"s1": {"empire": "voidborn", "stronghold": False}},
            "stations_by_sys": {"s1": [("s1", "st1", "b1")]},
            "fields": [
                {"system": "s1", "poi": "p_craft", "resource": "silicon_ore", "remaining": 9000, "max_remaining": 10000},
                {"system": "s1", "poi": "p_def", "resource": "iron_ore", "remaining": 9000, "max_remaining": 10000},
                {"system": "s1", "poi": "p_mixed", "resource": "silicon_ore", "remaining": 9000, "max_remaining": 10000},
                {"system": "s1", "poi": "p_mixed", "resource": "iron_ore", "remaining": 9000, "max_remaining": 10000},
            ],
            "pirates": set(),
            "item_vals": {"silicon_ore": 56.0, "iron_ore": 5.0},
            "shortages": {"iron_ore": 7000},
            "craft_demand": {"silicon_ore": 15000},
            "full_items": set(),
        }
        pol = dict(mine_net.DEFAULT_POLICY, market_tier=True, craft_demand_tier=True)
        cands = mine_net.score_belt_candidates({"name": "miner-1", "system": "s1", "modules": ["mining_laser_i"]}, world, pol, {}, {})
        self.assertEqual([c["tier"] for c in cands], ["deficit", "deficit", "craft_demand"])
        mixed = next(c for c in cands if c["poi"] == "p_mixed")
        self.assertEqual(mixed["resource"], "iron_ore")
        assigned = mine_net.assign_optimal_mines(
            [{"name": "miner-1", "system": "s1", "modules": ["mining_laser_i"]}], world, pol, {}, {}
        )
        self.assertEqual(assigned["miner-1"]["tier"], "deficit")
        self.assertEqual(assigned["miner-1"]["resource"], "iron_ore")


if __name__ == "__main__":
    unittest.main()

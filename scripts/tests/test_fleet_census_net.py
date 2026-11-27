#!/usr/bin/env python3
"""Unit tests for game/fleet/census_net.py (whole-map dynamic Intelligence AutoNet)."""
import json
import sqlite3
import sys
import tempfile
import time
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "game" / "fleet"))
import census_net as cn


def _make_world(tmp_dir, now_t):
    data = Path(tmp_dir)
    (data / "store").mkdir(parents=True, exist_ok=True)
    (data / "fleet" / "ships").mkdir(parents=True, exist_ok=True)
    (data / "scouting").mkdir(parents=True, exist_ok=True)
    db = data / "store" / "read.db"
    con = sqlite3.connect(db)
    con.executescript("""
        CREATE TABLE systems (id TEXT PRIMARY KEY, name TEXT, x REAL, y REAL, empire TEXT, home INTEGER, stronghold INTEGER, jumps INTEGER, src TEXT NOT NULL);
        CREATE TABLE lanes (a TEXT, b TEXT, src TEXT NOT NULL);
        CREATE TABLE places (system TEXT, poi TEXT, kind TEXT, name TEXT, class TEXT, base TEXT, x REAL, y REAL, t INTEGER, src TEXT NOT NULL, PRIMARY KEY (system, poi));
        CREATE TABLE fields (system TEXT, poi TEXT, resource TEXT, remaining INTEGER, max_remaining INTEGER, richness INTEGER, t INTEGER, src TEXT NOT NULL);
        CREATE TABLE herds (system TEXT, poi TEXT, creature TEXT, name TEXT, role TEXT, count INTEGER, t INTEGER, src TEXT NOT NULL);
        CREATE TABLE stations (name TEXT, kind TEXT, system TEXT, tag TEXT, faction TEXT, empire TEXT, condition TEXT, services TEXT, wrecked INTEGER, mobile INTEGER, src TEXT NOT NULL);
        CREATE TABLE bases (base TEXT, name TEXT, system TEXT, poi TEXT, kind TEXT, t INTEGER, src TEXT NOT NULL);
    """)
    # Quadrant EN (fresh), WN (stale/never), strongholds excluded
    con.executemany(
        "INSERT INTO systems VALUES (?,?,?,?,?,?,?,?,?)",
        [
            ("hub_en", "Hub EN", 10.0, 10.0, "voidborn", 0, 0, 1, "test"),
            ("stale_wn", "Stale WN", -10.0, 10.0, "", 0, 0, 2, "test"),
            ("never_wn", "Never WN", -20.0, 15.0, "", 0, 0, 3, "test"),
            ("stronghold_x", "Stronghold", -30.0, 20.0, "pirate", 0, 1, 4, "test"),
        ],
    )
    con.executemany(
        "INSERT INTO lanes VALUES (?,?,?)",
        [
            ("hub_en", "stale_wn", "test"),
            ("stale_wn", "never_wn", "test"),
            ("never_wn", "stronghold_x", "test"),
        ],
    )
    con.execute("INSERT INTO places VALUES ('hub_en','p1','station','Hub','station','hub_en_station',0,0,?,'test')", (int(now_t),))
    con.execute("INSERT INTO fields VALUES ('hub_en','b1','iron_ore',1000,1000,5,?,'test')", (int(now_t - 600),))
    con.execute("INSERT INTO fields VALUES ('stale_wn','b2','silver_ore',1000,1000,5,?,'test')", (int(now_t - 36000),))
    con.commit()
    con.close()
    for p in ("Scout Alpha", "Scout Beta"):
        (data / "fleet" / "ships" / f"{p}.json").write_text(
            json.dumps({"name": p, "system": "hub_en", "max_fuel": 110, "fuel": 110}),
            encoding="ascii",
        )
    return data


class CensusNetTests(unittest.TestCase):
    def test_prioritizes_never_scanned_and_excludes_strongholds(self):
        now_t = time.time()
        with tempfile.TemporaryDirectory() as td:
            data = _make_world(td, now_t)
            pol = dict(cn.DEFAULT_POLICY)
            p1 = cn.pick_and_claim_target(data, "Scout Alpha", pol, now_t=now_t, dry=False)
            self.assertIsNotNone(p1)
            self.assertEqual(p1["system"], "never_wn")
            self.assertTrue(p1["never_scanned"])

            # Second pilot must NOT collide with first pilot's active claim, and must NOT pick stronghold_x
            p2 = cn.pick_and_claim_target(data, "Scout Beta", pol, now_t=now_t, dry=False)
            self.assertIsNotNone(p2)
            self.assertEqual(p2["system"], "stale_wn")
            self.assertNotEqual(p2["system"], "stronghold_x")

            # After both targets claimed (and hub_en is fresh <45m), a third scout gets None
            p3 = cn.pick_and_claim_target(data, "Scout Gamma", pol, cur_sys="hub_en", now_t=now_t, dry=True)
            self.assertIsNone(p3)

            # Releasing Scout Alpha's claim frees never_wn again
            cn.release_claim(data, "Scout Alpha", "never_wn")
            p4 = cn.pick_and_claim_target(data, "Scout Gamma", pol, cur_sys="hub_en", now_t=now_t, dry=True)
            self.assertIsNotNone(p4)
            self.assertEqual(p4["system"], "never_wn")

    def test_disabled_policy_returns_none(self):
        now_t = time.time()
        with tempfile.TemporaryDirectory() as td:
            data = _make_world(td, now_t)
            pol = dict(cn.DEFAULT_POLICY)
            pol["enabled"] = False
            self.assertIsNone(cn.pick_and_claim_target(data, "Scout Alpha", pol, now_t=now_t, dry=True))

    def test_enroute_shortest_path_picks_stale_waypoints_with_zero_detour(self):
        # Graph: A -> B1 -> C1 -> D (all fresh) AND A -> B2 (stale) -> C2 (stale) -> D (same 3-hop shortest distance!)
        adj = {
            "A": ["B1", "B2"], "B1": ["A", "C1"], "C1": ["B1", "D"],
            "B2": ["A", "C2"], "C2": ["B2", "D"], "D": ["C1", "C2"],
        }
        wps = cn.plan_enroute_path(adj, "A", "D", {"B2": 3000.0, "C2": 4000.0}, max_waypoints=4)
        self.assertEqual(wps, ["B2", "C2"])
        # Respects max_waypoints cap while preserving travel order
        wps_cap = cn.plan_enroute_path(adj, "A", "D", {"B2": 3000.0, "C2": 4000.0}, max_waypoints=1)
        self.assertEqual(wps_cap, ["C2"])

    def test_read_at_preserved_so_miner_poi_writes_do_not_mask_stale_system(self):
        now_t = time.time()
        with tempfile.TemporaryDirectory() as td:
            data = _make_world(td, now_t)
            import mine
            # Write stale_wn scouting file with old read_at (6h ago) + existing survey key
            old_iso = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now_t - 6 * 3600))
            sp = data / "scouting" / "stale_wn.json"
            sp.write_text(json.dumps({"system": {"id": "stale_wn"}, "read_at": old_iso, "survey": {"ok": True}, "pois": {}}), encoding="ascii")
            # Miner updates one POI right now (file mtime becomes now_t, but read_at stays 6h old!)
            ok = mine.update_scouting_poi(data, "stale_wn", "b2", {"resources": [{"resource_id": "silver_ore", "remaining": 42}]})
            self.assertTrue(ok)
            updated = json.loads(sp.read_text(encoding="ascii"))
            self.assertEqual(updated["read_at"], old_iso)
            self.assertIn("survey", updated)
            self.assertEqual(updated["pois"]["b2"]["resources"][0]["remaining"], 42)
            # census_net still sees stale_wn as 6h stale (NOT 0s fresh!)
            w = cn._load_census_world(data, dict(cn.DEFAULT_POLICY), now_t=now_t)
            self.assertLess(w["last_t"]["stale_wn"], now_t - 5 * 3600)


if __name__ == "__main__":
    unittest.main()

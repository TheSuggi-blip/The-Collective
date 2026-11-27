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


if __name__ == "__main__":
    unittest.main()

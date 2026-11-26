#!/usr/bin/env python3
"""Unit tests for disabled-by-default pirate_net.py (Duskmere/TOI-700 Corsair AutoNet)."""
import json
import sqlite3
import sys
import tempfile
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "game" / "fleet"))

import pirate_net  # noqa: E402
import routes  # noqa: E402
import workclass  # noqa: E402


class PirateNetTests(unittest.TestCase):
    def test_disabled_by_default_and_registered(self):
        pol = pirate_net.read_policy(ROOT / "game" / "pirate-policy.json")
        self.assertFalse(pirate_net.is_enabled(pol))
        self.assertFalse(pol.get("raiding_enabled"))
        route = json.loads((ROOT / "game" / "routes" / "pirate-network.json").read_text(encoding="utf-8"))
        self.assertEqual(route["kind"], "pirate_net")
        self.assertEqual(route.get("status"), "off")
        self.assertEqual(workclass.work_class(route), "hunt")
        self.assertTrue(routes.standing(route))
        self.assertEqual(pirate_net.main(["IlIIllIlIIIllIlIIllI", "--policy", str(ROOT / "game" / "pirate-policy.json")]), 0)

    def test_barcode_and_organic_roster_generators(self):
        bc = pirate_net.generate_corsair_roster(count=120, style="barcode", seed=2026)
        self.assertEqual(len(bc), 120)
        names = [r["pilot"] for r in bc]
        self.assertEqual(len(set(names)), 120)
        for nm in names:
            self.assertEqual(len(nm), 20)
            self.assertTrue(set(nm) <= {"I", "l"})
        # Verify 28-day birth staggering
        days = {r["birth_day_offset"] for r in bc}
        self.assertGreaterEqual(len(days), 20)

        org = pirate_net.generate_corsair_roster(count=120, style="organic_pirate", seed=2026)
        self.assertEqual(len({r["pilot"] for r in org}), 120)
        for r in org:
            self.assertFalse(r["pilot"].startswith(("GSV ", "ROU ", "EUV ", "MCV ", "IFV ", "LSV ", "VSV ")))

    def test_three_phase_lifecycle(self):
        pol = dict(pirate_net.read_policy(ROOT / "game" / "pirate-policy.json"), enabled=True, raiding_enabled=True)
        self.assertEqual(pirate_net.pilot_phase({"piloting": 5, "tier": 1}, pol), "leveling")
        self.assertEqual(pirate_net.pilot_phase({"piloting": 22, "tier": 2}, pol), "leveling")
        self.assertEqual(pirate_net.pilot_phase({"piloting": 22, "tier": 3, "system": "sol"}, pol), "staging")
        self.assertEqual(pirate_net.pilot_phase({"piloting": 22, "tier": 3, "system": "toi_700"}, pol), "raiding")

    def test_shared_intel_tap_excludes_cltv_and_respects_jitter(self):
        with tempfile.TemporaryDirectory() as td:
            data = Path(td)
            (data / "store").mkdir(parents=True)
            db = data / "store" / "read.db"
            con = sqlite3.connect(str(db))
            con.executescript("""
                CREATE TABLE systems (id TEXT, name TEXT, empire TEXT, stronghold INTEGER);
                CREATE TABLE lanes (a TEXT, b TEXT);
                CREATE TABLE met (name TEXT, faction TEXT, class TEXT, system TEXT, t REAL);
                CREATE TABLE stations (name TEXT, kind TEXT, system TEXT, tag TEXT);
                INSERT INTO systems VALUES
                    ('toi_700', 'TOI-700', '', 0),
                    ('duskmere', 'Duskmere', '', 0),
                    ('prey_sys', 'Prey', '', 0),
                    ('fresh_sys', 'Fresh', '', 0),
                    ('gsc_0044', 'GSC-0044', '', 0);
                INSERT INTO lanes VALUES
                    ('toi_700', 'duskmere'),
                    ('duskmere', 'prey_sys'),
                    ('duskmere', 'fresh_sys');
            """)
            now = time.time()
            # prey_sys seen 1h ago (past jitter) -> valid target!
            # fresh_sys seen 10s ago (inside jitter window) -> skipped to prevent scout correlation!
            # CLTV pilot in prey_sys -> ignored!
            con.executemany("INSERT INTO met VALUES (?, ?, ?, ?, ?)", [
                ("Rival Miner 1", "HEXC", "lithosphere", "prey_sys", now - 3600),
                ("EUV Alabaster", "CLTV", "archimedes", "prey_sys", now - 3600),
                ("Rival Scout 2", "BUSY", "absence", "fresh_sys", now - 10),
                ("Hostile Raider", "ENDL", "broadaxe", "duskmere", now - 60),
            ])
            con.commit()
            con.close()

            pol = dict(pirate_net.read_policy(ROOT / "game" / "pirate-policy.json"), enabled=True, raiding_enabled=True)
            targets = pirate_net.discover_corsair_targets(data, pol, now=now)
            sys_ids = [t["system"] for t in targets]
            self.assertIn("prey_sys", sys_ids)
            self.assertNotIn("fresh_sys", sys_ids)
            prey = next(t for t in targets if t["system"] == "prey_sys")
            self.assertEqual(prey["tags"], ["HEXC"])

            alerts = pirate_net.check_gate_sentinel(data, pol, now=now)
            self.assertEqual(len(alerts), 1)
            self.assertEqual(alerts[0]["tag"], "ENDL")


if __name__ == "__main__":
    unittest.main()

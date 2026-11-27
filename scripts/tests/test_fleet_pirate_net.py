#!/usr/bin/env python3
"""Unit tests for disabled-by-default pirate_net.py (107-ship 4-empire Corsair AutoNet) and HUD/collector isolation."""
from collections import Counter
import json
import sqlite3
import sys
import tempfile
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "game" / "fleet"))
sys.path.insert(0, str(ROOT / "station"))

import pirate_net  # noqa: E402
import routes  # noqa: E402
import workclass  # noqa: E402
import fleet as station_fleet  # noqa: E402


class PirateNetTests(unittest.TestCase):
    def test_disabled_by_default_and_registered(self):
        pol = pirate_net.read_policy(ROOT / "game" / "pirate-policy.json")
        self.assertFalse(pirate_net.is_enabled(pol))
        self.assertFalse(pol.get("raiding_enabled"))
        self.assertEqual(pol.get("target_fleet_size"), 107)
        self.assertEqual(pol.get("naming_default_style"), "organic_pirate")
        self.assertEqual((pol.get("account_isolation") or {}).get("mode"), "separate_clerk_account")
        route = json.loads((ROOT / "game" / "routes" / "pirate-network.json").read_text(encoding="utf-8"))
        self.assertEqual(route["kind"], "pirate_net")
        self.assertEqual(route.get("status"), "off")
        self.assertEqual(workclass.work_class(route), "hunt")
        self.assertTrue(routes.standing(route))
        self.assertEqual(pirate_net.main(["salty_hammer", "--policy", str(ROOT / "game" / "pirate-policy.json")]), 0)

    def test_107_ship_four_empire_roster_and_styles(self):
        org = pirate_net.generate_corsair_roster(count=107, style="organic_pirate", seed=2026)
        self.assertEqual(len(org), 107)
        self.assertEqual(len({r["pilot"] for r in org}), 107)
        # Slot 0 MUST be Outer Rim Founder (1.5% corporate tax domicile)
        self.assertEqual(org[0]["role"], "command")
        self.assertEqual(org[0]["empire"], "outerrim")
        self.assertEqual(org[0]["birth_day_offset"], 0)
        # Exact optimal 4-empire split, ZERO Nebula!
        by_emp = Counter(r["empire"] for r in org)
        self.assertEqual(dict(by_emp), {"crimson": 43, "voidborn": 25, "outerrim": 21, "solarian": 18})
        self.assertNotIn("nebula", by_emp)
        by_wing = Counter(r["wing"] for r in org)
        self.assertEqual(dict(by_wing), {
            "CORSAIR-Alpha": 29,
            "CORSAIR-Beta": 28,
            "CORSAIR-Gamma": 26,
            "CORSAIR-Plunder": 13,
            "CORSAIR-Vault": 11,
        })
        for r in org:
            self.assertFalse(r["pilot"].startswith(("GSV ", "ROU ", "EUV ", "MCV ", "IFV ", "LSV ", "VSV ")))
            self.assertEqual(r["style"], "organic")

        # Barcode mode still works on demand
        bc = pirate_net.generate_corsair_roster(count=107, style="barcode", seed=2026)
        self.assertEqual(len(bc), 107)
        self.assertEqual(len({r["pilot"] for r in bc}), 107)
        for r in bc:
            self.assertEqual(len(r["pilot"]), 20)
            self.assertTrue(set(r["pilot"]) <= {"I", "l"})

    def test_phase_transitions(self):
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

    def test_station_fleet_collector_excludes_pirate_roster(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "fleet").mkdir()
            (root / "pirates").mkdir()
            (root / "pirates" / "roster.tsv").write_text(
                "pilot\twing\tdivision\trole\tempire\tbirth_day_offset\tstatus\n"
                "ROU FakeCorsair\tCORSAIR-Alpha\tArmada Alpha (29)\tgunship\tcrimson\t0\tplanned\n"
                "salty_hammer\tCORSAIR-Alpha\tArmada Alpha (29)\tcommand\touterrim\t0\tplanned\n",
                encoding="utf-8",
            )
            old_data = station_fleet.DATA
            old_cache = dict(station_fleet._PIRATES_CACHE)
            try:
                station_fleet.DATA = root / "fleet"
                station_fleet._PIRATES_CACHE["mtime"] = -1.0
                rows = [
                    {"name": "ROU Legit", "division": "Military"},
                    {"name": "ROU FakeCorsair", "division": "Military"},
                    {"name": "salty_hammer", "division": "Command"},
                ]
                kept = station_fleet.of_fleet(rows)
                self.assertEqual([r["name"] for r in kept], ["ROU Legit"])
            finally:
                station_fleet.DATA = old_data
                station_fleet._PIRATES_CACHE.update(old_cache)


if __name__ == "__main__":
    unittest.main()

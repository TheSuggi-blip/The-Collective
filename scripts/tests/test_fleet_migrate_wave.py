"""Unit tests for game/fleet/migrate_wave.py: exact 6-wave retirement planning, Command protection, and Reserve archive."""

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]


def load_mod():
    spec = importlib.util.spec_from_file_location("migrate_wave_ut", REPO / "game" / "fleet" / "migrate_wave.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class MigrateWaveTests(unittest.TestCase):
    def test_six_wave_plan_covers_490_and_never_touches_command(self):
        mw = load_mod()
        manifest = mw.load_manifest(REPO / "game" / "fleet-500-manifest.tsv")
        self.assertEqual(len(manifest), 500)
        sim = [{"name": nm, "credits": 1000} for nm in sorted(mw.KEPT_COMMAND)]
        for pfx, cnt in (("miner-", 130), ("drone-", 95), ("sentinel-", 35), ("trader-", 85), ("hauler-", 95), ("scout-", 50)):
            for i in range(1, cnt + 1):
                sim.append({"name": "%s%d" % (pfx, i), "credits": 1000})
        self.assertEqual(len(sim), 500)

        officers = {"hauler-3": "Builder", "hauler-1": "Officer", "trader-1": "Officer"}
        retired_all = []
        birthed_all = []
        for w in range(1, 7):
            inc = [r for r in manifest if r["wave"] == w and r["status"] == "planned"]
            ret = mw.plan_wave_retirements(w, sim, officers)
            self.assertEqual(len(ret), len(inc), "Wave %d seat mismatch" % w)
            for n in ret:
                self.assertNotIn(n, mw.KEPT_COMMAND)
            if w == 3:
                self.assertNotIn("hauler-3", ret)
                self.assertNotIn("hauler-1", ret)
            retired_all.extend(ret)
            birthed_all.extend(r["pilot"] for r in inc)
            rset = set(ret)
            sim = [s for s in sim if s["name"] not in rset] + [{"name": r["pilot"], "credits": 0} for r in inc]
            self.assertEqual(len(sim), 500)

        self.assertEqual(len(retired_all), 490)
        self.assertEqual(len(set(retired_all)), 490)
        self.assertEqual(len(birthed_all), 490)
        self.assertEqual(len(set(birthed_all)), 490)

    def test_reserve_archive_and_rejoin_off(self):
        mw = load_mod()
        with tempfile.TemporaryDirectory() as td:
            d = Path(td)
            (d / "fleet").mkdir(parents=True)
            mw.append_rejoin_off(d, "miner-1")
            mw.append_rejoin_off(d, "miner-2")
            mw.append_rejoin_off(d, "miner-1")
            lines = (d / "fleet" / "rejoin-off").read_text(encoding="ascii").splitlines()
            self.assertEqual(lines, ["miner-1", "miner-2"])
            mw.record_reserve(d, {"pilot": "miner-1", "wave": 1, "credits_swept": 5000})
            doc = json.loads((d / "fleet" / "reserves.json").read_text(encoding="ascii"))
            self.assertIn("miner-1", doc["reserves"])



    def test_wave_seat_and_promo_maps_rule_f11(self):
        # Verify total seated seats across W1..W6 + 10 Command == 275 exact cap
        import migrate_wave
        m = migrate_wave.load_manifest()
        total_seats = 10
        for w in range(1, 7):
            inc_all = [r for r in m if r["wave"] == w and r["status"] == "planned"]
            seats, promos = migrate_wave.wave_seat_and_promo_maps(w, inc_all, builder_role_id="builder-uuid-test")
            total_seats += len(seats)
            if w == 4:
                self.assertEqual(len(seats), 15)
                self.assertEqual(sum(1 for p in seats if p.startswith("MCV ")), 10)
                self.assertEqual(sum(1 for p in seats if p.startswith("IFV ")), 5)
                self.assertEqual(len(promos), 15)
            elif w == 5:
                self.assertEqual(len(seats), 90)
                self.assertEqual(promos[inc_all[0]["pilot"]], "builder-uuid-test")
                self.assertEqual(sum(1 for v in promos.values() if v == "officer"), 24)
        self.assertEqual(total_seats, 275)

if __name__ == "__main__":
    unittest.main()

import json
import sqlite3
import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "game" / "fleet"))
import rivals


class TestFleetRivals(unittest.TestCase):
    def _fixture(self, tmp):
        root = Path(tmp) / "repo"
        data = Path(tmp) / "data"
        (root / "governance").mkdir(parents=True)
        (data / "store").mkdir(parents=True)
        (data / "comms").mkdir(parents=True)
        (data / "comms" / "diplomacy.json").write_text(
            json.dumps({"factions": {"HEXC": {"status": "neutrality_agreed"}, "IRLC": {"status": "neutrality_agreed"}}}),
            encoding="ascii",
        )
        conn = sqlite3.connect(str(data / "store" / "read.db"))
        conn.executescript("""
            CREATE TABLE factions (tag TEXT, leader TEXT);
            INSERT INTO factions VALUES ('HEXC', 'HexCogitoAI'), ('NOIR', 'NoirLead'), ('ENDL', 'EndLead');
            CREATE TABLE hulls (id TEXT, name TEXT, faction TEXT, tier INT, category TEXT, piloting_required INT, cargo INT, speed INT, weapon_slots INT, defense_slots INT, utility_slots INT);
            INSERT INTO hulls VALUES
                ('lithosphere', 'Lithosphere', 'solarian', 4, 'Industrial', 30, 1680, 1, 1, 2, 8),
                ('futures', 'Futures', 'nebula', 1, 'Commercial', 0, 30, 6, 0, 0, 2);
            CREATE TABLE rival_snapshots (t INT, tag TEXT, name TEXT, members INT, bases INT, wrecked INT, wealth REAL, ship_value REAL, storage_value REAL, facility_inv REAL, ore_mined REAL, items_crafted REAL, missions INT, damage_dealt REAL, kills_pve INT, kills_pvp INT, active_1h INT, active_24h INT, max_tier INT, avg_tier REAL, allies TEXT, base_systems TEXT, src TEXT);
            INSERT INTO rival_snapshots VALUES
                (100000, 'HEXC', 'Hex Collective', 82, 11, 0, 9000000000, 0, 6000000000, 500000000, 120000000, 5800000, 23000, 0, 2000, 50, 50, 80, 5, 3.2, '["IRLC"]', '["dheneb"]', 'x'),
                (107200, 'HEXC', 'Hex Collective', 82, 11, 0, 9100000000, 0, 6100000000, 500000000, 120500000, 5801000, 23000, 0, 2010, 50, 50, 80, 5, 3.21, '["IRLC"]', '["dheneb"]', 'x'),
                (100000, 'NOIR', 'Interstellar Continental', 31, 0, 0, 1600000000, 0, 380000000, 77000000, 8000000, 1700000, 39000, 0, 0, 0, 20, 30, 5, 2.48, '[]', '[]', 'x'),
                (107200, 'NOIR', 'Interstellar Continental', 31, 0, 0, 1650000000, 0, 389000000, 77000000, 8000000, 1700500, 39000, 0, 0, 0, 20, 30, 5, 2.48, '[]', '[]', 'x'),
                (107200, 'ENDL', 'End of Line', 180, 8, 0, 1750000000, 0, 1200000000, 72000000, 97000000, 1380000, 146000, 0, 500, 1527, 40, 120, 4, 1.08, '[]', '[]', 'x');
            CREATE TABLE met (name TEXT, faction TEXT, class TEXT, system TEXT, times INT);
            INSERT INTO met VALUES ('Hex1', 'HEXC', 'lithosphere', 'dheneb', 50), ('Noir1', 'NOIR', 'futures', 'first_step', 20);
            CREATE TABLE stations (name TEXT, kind TEXT, system TEXT, tag TEXT, condition TEXT);
            INSERT INTO stations VALUES ('Hex Star', 'station', 'dheneb', 'HEXC', 'operational');
            CREATE TABLE books (system TEXT, item TEXT, bid REAL, bid_qty INT, ask REAL, ask_qty INT);
            INSERT INTO books VALUES ('dheneb', 'uranium_ore', 600, 3333, 0, 0), ('dheneb', 'fuel_cell', 0, 0, 3000, 1000);
            CREATE TABLE leaderboards (grp TEXT, board TEXT, rank INT, name TEXT, tag TEXT, value REAL);
            INSERT INTO leaderboards VALUES ('stations', 'tourism_revenue', 1, 'Hex Star', 'Dheneb', 197882046);
        """)
        conn.commit()
        conn.close()
        return root, data

    def test_sedcards_classify_archetypes_velocity_and_markets(self):
        with tempfile.TemporaryDirectory() as tmp:
            root, data = self._fixture(tmp)
            doc = rivals.compute_sedcards(root, data, top_n=10, now=107200)
            by_tag = {c["tag"]: c for c in doc["sedcards"]}
            self.assertEqual(by_tag["HEXC"]["archetype"], "Lawless Monopoly Elite")
            self.assertEqual(by_tag["HEXC"]["standing"], "NEUTRAL")
            self.assertEqual(by_tag["HEXC"]["wealth_vel_h"], 50000000.0)
            self.assertEqual(by_tag["HEXC"]["top_bids"][0]["item"], "uranium_ore")
            self.assertEqual(by_tag["NOIR"]["archetype"], "Zero-Base Express & Exchange")
            self.assertEqual(by_tag["ENDL"]["archetype"], "PvP Raider Bloc")
            self.assertEqual(by_tag["ENDL"]["threat"], "high")

            # Markdown write & idempotency
            self.assertEqual(rivals.write_sedcards(root, data, commit=False, now=107200), 0)
            md = (root / "governance" / "rival-sedcards.md").read_text(encoding="ascii")
            self.assertIn("Hex Collective", md)
            self.assertIn("uranium_ore", md)

            # Briefing tailored to Trade
            br = rivals.render_briefing(doc, who="Mercury")
            self.assertIn("ADOPT (Trade)", br)
            self.assertIn("Hex Star", br)


if __name__ == "__main__":
    unittest.main()

"""game/fleet/herds.py: every place a species was counted, with its count now, the law and the pirate record. No engine."""

import os
import sqlite3
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "game", "fleet"))
import herds  # noqa: E402

NOW = 1795453600.0


def store():
    conn = sqlite3.connect(":memory:")
    conn.executescript("""
        CREATE TABLE reading_day (system, poi, what, kind, day, first, last, t_first, t_last);
        CREATE TABLE herds (system, poi, creature, name, role, count, t, src);
        CREATE TABLE places (system, poi, kind, name, class, base, x, y, t, src);
        CREATE TABLE systems (id, name, x, y, empire, home, stronghold, jumps, src);
        CREATE TABLE observations (division, member, kind, subject, t, at, fields, note, digest);
        CREATE TABLE public_battles (system, system_name, category, status, tick, destroyed, lost, pilots, tags, ended_at, t, src);
    """)
    conn.executemany("INSERT INTO reading_day (system, poi, what, kind, day, first, last) VALUES (?, ?, ?, 'herd', ?, ?, ?)", [
        ("sadachbia", "sadachbia_belt", "mirror_skate", 1795392000, 1, 1),
        ("redmarsh", "redmarsh_belt_a", "mirror_skate", 1795219200, 3, 1),
        ("void_gate", "void_gate_mineral_fields", "cauldronback", 1795392000, 2, 4),
    ])
    conn.executemany("INSERT INTO herds (system, poi, creature, count) VALUES (?, ?, ?, ?)", [
        ("sadachbia", "sadachbia_belt", "mirror_skate", 1),
        ("void_gate", "void_gate_mineral_fields", "cauldronback", 4),
    ])
    conn.executemany("INSERT INTO places (system, poi, t) VALUES (?, ?, ?)", [
        ("sadachbia", "sadachbia_belt", NOW - 600), ("redmarsh", "redmarsh_belt_a", NOW - 6000),
        ("void_gate", "void_gate_mineral_fields", NOW - 60)])
    conn.executemany("INSERT INTO systems (id, empire, stronghold, jumps) VALUES (?, ?, ?, ?)", [
        ("sadachbia", None, 0, 25), ("redmarsh", None, 0, 26), ("void_gate", "outerrim", 0, 19)])
    conn.executemany("INSERT INTO observations (kind, subject, t) VALUES (?, ?, ?)", [
        ("pirate", "redmarsh", NOW - 3600), ("pirate", "redmarsh", NOW - 3600), ("pirate", "sadachbia", NOW - 400000),
        ("ranch", "sadachbia", NOW - 60)])
    conn.execute("INSERT INTO public_battles (system, category) VALUES ('redmarsh', 'pirate')")
    return conn


class HerdTableTests(unittest.TestCase):
    def setUp(self):
        self.found = herds.table(store(), ["mirror_skate", "cauldronback", "inkwyrm"], NOW, hours=72, keep=2)

    def test_a_place_empty_now_stays_listed_with_its_most(self):
        rows = {r["system"]: r for r in self.found["mirror_skate"]}
        self.assertEqual(rows["redmarsh"]["now"], 0)
        self.assertEqual(rows["redmarsh"]["most"], 3)
        self.assertEqual(rows["sadachbia"]["now"], 1)

    def test_pirates_count_within_the_window_only_and_battles_on_record(self):
        rows = {r["system"]: r for r in self.found["mirror_skate"]}
        self.assertEqual(rows["redmarsh"]["pirates"], 2)
        self.assertEqual(rows["redmarsh"]["battles"], 1)
        self.assertEqual(rows["sadachbia"]["pirates"], 0)     # older than 72 h; a ranch line is no pirate

    def test_huntable_only_above_the_kept_herd_and_law_named(self):
        cauldron = self.found["cauldronback"][0]
        self.assertTrue(cauldron["huntable"])
        self.assertEqual(cauldron["law"], "outerrim")
        self.assertEqual(cauldron["age_min"], 1)
        self.assertFalse(any(r["huntable"] for r in self.found["mirror_skate"]))
        self.assertEqual(self.found["mirror_skate"][0]["law"], "lawless")

    def test_nearest_first_and_an_unseen_species_has_no_rows(self):
        self.assertEqual([r["system"] for r in self.found["mirror_skate"]], ["sadachbia", "redmarsh"])
        self.assertNotIn("inkwyrm", self.found)


if __name__ == "__main__":
    unittest.main()

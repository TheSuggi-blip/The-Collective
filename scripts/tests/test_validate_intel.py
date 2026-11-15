"""Intel gate regressions use disposable trees, never the repository's live files."""

import importlib.util
from pathlib import Path
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "validate-intel.py"


def load():
    spec = importlib.util.spec_from_file_location("intel_under_test", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def intel_file(kind, entity, standing="neutral", **extra):
    fields = {
        "name": "fixture",
        "id": "20261114T000001Z",
        "tier": "intel",
        "author": "Fixture",
        "kind": kind,
        "username" if kind == "player" else "system_id": entity,
        "standing": standing,
        "standing_since": "2026-11-14",
        "threat": "unknown",
        "updated": "2026-11-14",
    }
    if standing != "neutral":
        fields["standing_by"] = "Fixture"
        fields["standing_reason"] = "fixture reason"
    fields.update(extra)
    lines = ["%s: %s" % (key, value) for key, value in fields.items() if value is not None]
    return "---\n" + "\n".join(lines) + "\n---\n\n# Fixture\n"


class ValidateIntelTests(unittest.TestCase):
    def setUp(self):
        self.intel = load()
        self.temp = tempfile.TemporaryDirectory(prefix="validate-intel-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for folder in ("game", "game/players", "game/planets", "game/map"):
            (self.root / folder).mkdir()
        (self.root / "game" / "map" / "galaxy.tsv").write_text(
            "# fixture chart\nid\tname\nnexus_prime\tNexus Prime\nsol\tSol\n", encoding="ascii"
        )

    def put(self, rel, text):
        (self.root / rel).write_text(text, encoding="ascii")

    def run_check(self):
        return self.intel.check(str(self.root))

    def test_clean_tree_passes_and_skips_non_data_files(self):
        self.put("game/players/n-gemma.md", intel_file("player", "Gemma"))
        self.put("game/players/h-silas_vane.md", intel_file("player", "Silas Vane", "hostile"))
        self.put("game/planets/a-nexus_prime.md", intel_file("system", "nexus_prime", "ally"))
        self.put("game/players/BLUEPRINT.md", "not a data file\n")
        self.put("game/planets/.gitkeep", "")
        errors, warnings, counts = self.run_check()
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])
        self.assertEqual(counts, {"players": 2, "planets": 1})

    def test_letter_must_match_standing(self):
        self.put("game/players/n-gemma.md", intel_file("player", "Gemma", "hostile"))
        errors, _, _ = self.run_check()
        self.assertEqual(len(errors), 1)
        self.assertIn("rename it to h-gemma.md", errors[0])

    def test_one_pilot_cannot_be_filed_twice(self):
        self.put("game/players/n-gemma.md", intel_file("player", "Gemma"))
        self.put("game/players/h-gemma.md", intel_file("player", "gemma", "hostile"))
        errors, _, _ = self.run_check()
        self.assertTrue(any("already used by" in line for line in errors))
        self.assertTrue(any("already filed in" in line for line in errors))

    def test_ally_and_hostile_need_who_and_why(self):
        self.put("game/players/h-gemma.md",
                 intel_file("player", "Gemma", "hostile", standing_by=None, standing_reason=None))
        errors, _, _ = self.run_check()
        self.assertEqual(len(errors), 2)
        self.assertTrue(all("hostile standing needs" in line for line in errors))

    def test_key_must_fit_the_entity(self):
        self.put("game/players/n-gemma.md", intel_file("player", "Somebody Else"))
        self.put("game/planets/n-sol.md", intel_file("system", "nexus_prime"))
        errors, _, _ = self.run_check()
        self.assertEqual(len(errors), 2)
        self.assertTrue(all("does not fit" in line for line in errors))

    def test_bad_names_are_errors(self):
        self.put("game/players/x-gemma.md", intel_file("player", "Gemma"))
        self.put("game/players/n-Gemma.md", intel_file("player", "Gemma"))
        self.put("game/players/gemma.md", intel_file("player", "Gemma"))
        errors, _, counts = self.run_check()
        self.assertEqual(len(errors), 3)
        self.assertEqual(counts["players"], 0)

    def test_missing_field_bad_threat_and_bad_date(self):
        self.put("game/players/n-gemma.md",
                 intel_file("player", "Gemma", threat="deadly", updated="14.11.2026", author=None))
        errors, _, _ = self.run_check()
        joined = "\n".join(errors)
        self.assertIn("`author` is missing", joined)
        self.assertIn("`threat` must be one of", joined)
        self.assertIn("`updated` must be a date", joined)

    def test_wrong_kind_and_missing_frontmatter(self):
        self.put("game/players/n-gemma.md", intel_file("system", "gemma", username="Gemma"))
        self.put("game/planets/n-sol.md", "# Sol\nno frontmatter\n")
        errors, _, _ = self.run_check()
        joined = "\n".join(errors)
        self.assertIn("`kind` must be player", joined)
        self.assertIn("no frontmatter", joined)

    def test_system_off_the_chart_is_a_warning(self):
        self.put("game/planets/n-far_away.md", intel_file("system", "far_away"))
        errors, warnings, _ = self.run_check()
        self.assertEqual(errors, [])
        self.assertEqual(len(warnings), 1)
        self.assertIn("not in game/map/galaxy.tsv", warnings[0])

    def test_player_key(self):
        key = self.intel.player_key
        self.assertEqual(key("Gemma"), "gemma")
        self.assertEqual(key("Silas Vane"), "silas_vane")
        self.assertEqual(key("Wexler 02W-XD"), "wexler_02w-xd")
        self.assertEqual(key("Arthur 'Artificer' Artis"), "arthur_artificer_artis")
        self.assertEqual(key("[Citizen Pool: Atlantis]"), "citizen_pool_atlantis")
        self.assertEqual(key("\\u{2620}"), "u2620")
        self.assertEqual(key(chr(0x2620)), "u2620")
        self.assertEqual(key("!!!"), "unnamed")

    def test_second_pilot_with_the_same_key_gets_a_suffix(self):
        self.put("game/players/n-silas_vane.md", intel_file("player", "Silas Vane"))
        path, note = self.intel.suggest_name(str(self.root), "player", "Silas_Vane", "neutral")
        self.assertEqual(path, "game/players/n-silas_vane-2.md")
        self.assertIn("suffix", note)
        self.put("game/players/n-silas_vane-2.md", intel_file("player", "Silas_Vane"))
        errors, _, _ = self.run_check()
        self.assertEqual(errors, [])

    def test_suggest_name_finds_an_existing_file(self):
        self.put("game/players/n-gemma.md", intel_file("player", "Gemma"))
        path, note = self.intel.suggest_name(str(self.root), "player", "GEMMA", "neutral")
        self.assertEqual(path, "game/players/n-gemma.md")
        self.assertIn("exists already", note)
        path, note = self.intel.suggest_name(str(self.root), "player", "Gemma", "hostile")
        self.assertEqual(path, "game/players/h-gemma.md")
        self.assertIn("git mv game/players/n-gemma.md game/players/h-gemma.md", note)
        path, note = self.intel.suggest_name(str(self.root), "planet", "sol", "neutral")
        self.assertEqual((path, note), ("game/planets/n-sol.md", "new file"))


if __name__ == "__main__":
    unittest.main()

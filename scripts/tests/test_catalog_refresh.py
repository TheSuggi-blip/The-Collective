"""scripts/catalog-refresh.py on small catalogs in a temporary data folder: the check, the refresh, the refusal, the old
copies, the summary and the notice. No network: the download is replaced by a literal payload."""

import contextlib
import copy
import gzip
import importlib.util
import io
import json
import os
import re
import tempfile
import unittest
import urllib.error
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
SCRIPT = REPO / "scripts" / "catalog-refresh.py"
spec = importlib.util.spec_from_file_location("catalog_refresh_under_test", SCRIPT)
refresher = importlib.util.module_from_spec(spec)
spec.loader.exec_module(refresher)
DRAFT = re.compile(r"^## \[ENT-NEXT\] \| NOW \| ([A-Za-z][A-Za-z0-9_-]*) \| ([a-z]+)((?: \| (?:ref|see): [^|]+)*)$")   # comms.py's form


def catalog(version):
    """A small catalog: ten items, ten recipes, three facilities, two hulls, two skills."""
    items = [{"id": "ore_%d" % n, "name": "Ore %d" % n, "category": "ore", "size": 1, "base_value": 5 + n} for n in range(8)]
    items += [{"id": "steel_plate", "name": "Steel Plate", "category": "refined", "size": 1, "base_value": 18},
              {"id": "old_relic", "name": "Old Relic", "category": "misc", "size": 2, "base_value": 400}]
    recipes = [{"id": "smelt_%d" % n, "name": "Smelt %d" % n, "category": "Refining", "inputs": [{"item_id": "ore_%d" % n, "quantity": 10}],
                "outputs": [{"item_id": "steel_plate", "quantity": 1}], "crafting_time": 1, "hand_craftable": True, "produced_by_facility_ids": []}
               for n in range(8)]
    recipes += [{"id": "press_plate", "name": "Press Plate", "category": "Refining", "inputs": [{"item_id": "ore_0", "quantity": 5}, {"item_id": "ore_1", "quantity": 5}],
                 "outputs": [{"item_id": "steel_plate", "quantity": 2}], "crafting_time": 3, "hand_craftable": False, "produced_by_facility_ids": ["press"]},
                {"id": "relic_polish", "name": "Polish", "category": "Misc", "inputs": [{"item_id": "old_relic", "quantity": 1}],
                 "outputs": [{"item_id": "old_relic", "quantity": 1}], "crafting_time": 9, "hand_craftable": True, "produced_by_facility_ids": []}]
    return {"version": version,
            "mining": {"precision_k": 20},
            "items": items, "recipes": recipes,
            "facilities": [{"id": "press", "name": "Press", "category": "production", "level": 1, "recipe_id": "press_plate", "build_cost": 1000,
                            "build_materials": [{"item_id": "steel_plate", "quantity": 5}]},
                           {"id": "lockbox", "name": "Lockbox", "category": "faction", "level": 1, "build_cost": 200000,
                            "build_materials": [{"item_id": "steel_plate", "quantity": 200}]},
                           {"id": "kiosk", "name": "Kiosk", "category": "service", "level": 1, "build_cost": 50, "description": "Sells snacks."}],
            "ships": [{"id": "skiff", "name": "Skiff", "class": "Miner", "tier": 1, "cargo_capacity": 50, "build_materials": [{"item_id": "steel_plate", "quantity": 20}]},
                      {"id": "barge", "name": "Barge", "class": "Hauler", "tier": 2, "cargo_capacity": 400, "build_materials": [{"item_id": "steel_plate", "quantity": 90}]}],
            "skills": [{"id": "mining", "category": "Industry", "max_level": 100}, {"id": "refining", "category": "Industry", "max_level": 100}]}


def newer(version="0.2.0"):
    """The next catalog: recipe added, item removed, a quantity, a cost and a text changed."""
    cat = catalog(version)
    cat["recipes"].append({"id": "forge_beam", "name": "Forge Beam", "category": "Components", "inputs": [{"item_id": "steel_plate", "quantity": 4}],
                           "outputs": [{"item_id": "steel_plate", "quantity": 1}], "crafting_time": 2, "hand_craftable": True, "produced_by_facility_ids": []})
    cat["items"] = [i for i in cat["items"] if i["id"] != "old_relic"]
    cat["recipes"] = [r for r in cat["recipes"] if r["id"] != "relic_polish"]
    for r in cat["recipes"]:
        if r["id"] == "press_plate":
            r["inputs"][0]["quantity"] = 7
    cat["facilities"][1]["build_cost"] = 250000
    cat["facilities"][2]["description"] = "Sells cold snacks."
    cat["mining"]["precision_k"] = 25
    return cat


def raw(cat):
    return json.dumps(cat).encode("utf-8")


class Fake:
    """The network, by literal payloads: the game's status names `live`; the catalog answers `payload` (or 304 when the
    ETag asked for is `etag`)."""

    def __init__(self, live, payload=None, etag='"e2"'):
        self.live, self.payload, self.etag, self.calls = live, payload, etag, []

    def __call__(self, url, headers):
        self.calls.append((url, dict(headers)))
        if url.endswith("/stats"):
            return 200, {}, json.dumps({"version": self.live, "tick": 1}).encode()
        if self.etag and self.etag in headers.get("If-None-Match", ""):
            return 304, {"etag": self.etag}, b""
        return 200, {"etag": self.etag}, self.payload


class Refresh(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="catalog-refresh-test-")
        self.addCleanup(self.temp.cleanup)
        self.data = Path(self.temp.name) / "data"
        self.folder = self.data / "catalog"
        self.folder.mkdir(parents=True)
        self.put("0.1.0", catalog("0.1.0"))
        (self.folder / "ammo.json").write_text("[]", encoding="utf-8")
        self.notice = Path(self.temp.name) / "notice.txt"
        self.real_fetch = refresher.fetch
        self.addCleanup(setattr, refresher, "fetch", self.real_fetch)

    def put(self, version, cat, when=None):
        path = self.folder / ("%s.json" % version)
        path.write_bytes(raw(cat))
        if when is not None:
            os.utime(path, (when, when))
        return path

    def run_main(self, fake, *args):
        refresher.fetch = fake
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = refresher.main(list(args) + ["--data", str(self.data), "--root", str(REPO), "--url", "https://x/api/catalog.json",
                                                "--stats-url", "https://x/api/stats"])
        return code, out.getvalue()

    def snapshot(self):
        return sorted((str(p.relative_to(self.data)), p.stat().st_size, p.stat().st_mtime_ns) for p in self.data.rglob("*"))

    def test_same_version_writes_nothing(self):
        before = self.snapshot()
        fake = Fake("0.1.0", raw(newer()))
        code, out = self.run_main(fake, "refresh", "--notice", str(self.notice))
        self.assertEqual((code, self.snapshot(), self.notice.exists()), (0, before, False))
        self.assertEqual([url for url, _h in fake.calls], ["https://x/api/stats"])           # the catalog is not asked for
        self.assertEqual(len(out.strip().splitlines()), 1)
        self.assertIn("catalog current: 0.1.0", out)

    def test_newer_version_is_installed_and_summed_up(self):
        code, out = self.run_main(Fake("0.2.0", raw(newer())), "refresh", "--notice", str(self.notice))
        self.assertEqual(code, 0, out)
        self.assertTrue((self.folder / "0.2.0.json").is_file())
        self.assertTrue((self.folder / "0.1.0.json").is_file())                               # the old copy stays beside it
        self.assertEqual(json.loads((self.folder / "0.2.0.json").read_text())["version"], "0.2.0")
        self.assertEqual([p.name for p in self.folder.iterdir() if p.name.endswith(".tmp")], [])
        self.assertIn("CATALOG CHANGES 0.1.0 (file of ", out)
        self.assertRegex(out, r"recipes: 10 -> 10 \| added 1 \| removed 1 \| changed 1 \(1 in figures, 0 in text only, 0 in list order only\)")
        self.assertIn("added: forge_beam", out)                                               # an added recipe
        self.assertRegex(out, r"items: 10 -> 9 \| added 0 \| removed 1 ")
        self.assertIn("removed: old_relic", out)                                              # a removed item
        self.assertIn("press_plate: inputs: ore_0 5 -> 7", out)                               # a changed quantity
        self.assertIn("lockbox: build_cost: 200000 -> 250000", out)
        self.assertIn("text only: kiosk", out)
        self.assertIn("other: mining: precision_k 20 -> 25", out)
        state = json.loads((self.folder / "refresh.json").read_text())
        self.assertEqual((state["etag"], state["etag_version"], state["announced"]), ('"e2"', "0.2.0", "0.2.0"))
        # the next hour: the game still runs 0.2.0 -> one line, nothing asked of the catalog
        fake = Fake("0.2.0", raw(newer()))
        code, out = self.run_main(fake, "refresh")
        self.assertEqual((code, len(fake.calls), out.count("\n")), (0, 1, 1))

    def test_unchanged_catalog_answers_304(self):
        self.run_main(Fake("0.2.0", raw(newer())), "refresh")
        before = self.snapshot()
        fake = Fake("0.2.1", raw(newer()))                                                    # the game moved, the catalog did not
        code, out = self.run_main(fake, "refresh", "--notice", str(self.notice))
        self.assertEqual((code, self.snapshot(), self.notice.exists()), (0, before, False))
        self.assertEqual(fake.calls[1][1].get("If-None-Match"), '"e2"')
        self.assertIn("same catalog", out)

    def test_broken_payload_is_rejected(self):
        before = (self.folder / "0.1.0.json").read_bytes()
        code, out = self.run_main(Fake("0.2.0", b'{"version": "0.2.0", "items": ['), "refresh", "--notice", str(self.notice))
        self.assertEqual(code, 1)
        self.assertIn("REJECTED: not JSON", out)
        self.assertEqual(sorted(p.name for p in self.folder.glob("*.rejected")), ["unknown.json.rejected"])
        self.assertEqual(refresher.newest(self.folder), "0.1.0")
        self.assertEqual((self.folder / "0.1.0.json").read_bytes(), before)
        self.assertFalse(self.notice.exists())
        # the same bytes again: one line, exit 0, no second file kept
        code, out = self.run_main(Fake("0.2.0", b'{"version": "0.2.0", "items": ['), "refresh")
        self.assertEqual(code, 0, out)
        self.assertIn("still the one rejected", out)
        self.assertEqual(len(list(self.folder.glob("*.rejected"))), 1)
        # the same bytes under another ETag: downloaded, known by their hash, not kept twice
        code, out = self.run_main(Fake("0.2.0", b'{"version": "0.2.0", "items": [', etag='"e9"'), "refresh")
        self.assertEqual(code, 0, out)
        self.assertIn("still the one rejected", out)
        self.assertEqual(len(list(self.folder.glob("*.rejected"))), 1)
        self.assertEqual([p.name for p in self.folder.iterdir() if p.name.endswith(".tmp")], [])

    def test_shrunken_payload_is_rejected(self):
        small = catalog("0.2.0")
        small["recipes"] = small["recipes"][:5]                                               # half the recipes of the copy in force
        code, out = self.run_main(Fake("0.2.0", raw(small)), "refresh")
        self.assertEqual(code, 1)
        self.assertIn("`recipes` holds 5 usable rows, the copy in force 10", out)
        self.assertTrue((self.folder / "0.2.0.json.rejected").is_file())
        self.assertFalse((self.folder / "0.2.0.json").exists())
        self.assertEqual(refresher.newest(self.folder), "0.1.0")

    def test_renamed_field_and_bad_version_are_rejected(self):
        moved = catalog("0.2.0")
        for r in moved["recipes"]:
            r["ingredients"] = r.pop("inputs")                                                # a field the readers take is gone
        code, out = self.run_main(Fake("0.2.0", raw(moved)), "refresh")
        self.assertEqual(code, 1)
        self.assertIn("`recipes` holds no row with the fields id, inputs", out)
        code, out = self.run_main(Fake("0.2.0", raw(dict(catalog("x"), version="0.2.0-beta")), etag='"e3"'), "refresh")
        self.assertEqual(code, 1)
        self.assertIn("no version of digits and dots", out)

    def test_older_version_is_rejected(self):
        code, out = self.run_main(Fake("0.0.9", raw(catalog("0.0.9"))), "refresh")
        self.assertEqual(code, 1)
        self.assertIn("older than our copy 0.1.0", out)
        self.assertFalse((self.folder / "0.0.9.json").exists())

    def test_three_versions_move_the_oldest_to_old(self):
        self.put("0.2.0", newer("0.2.0"))
        self.run_main(Fake("0.2.0", b""), "refresh")                                          # the first run announces 0.1.0 -> 0.2.0
        code, out = self.run_main(Fake("0.3.0", raw(newer("0.3.0"))), "refresh")
        self.assertEqual(code, 0, out)
        self.assertEqual(sorted(p.name for p in self.folder.glob("*.json")), ["0.2.0.json", "0.3.0.json", "ammo.json", "refresh.json"])
        self.assertTrue((self.folder / "old" / "0.1.0.json").is_file())
        self.assertIn("moved to old/: 0.1.0.json -> old/0.1.0.json", out)
        code, out = self.run_main(Fake("0.3.0", b""), "diff", "0.1.0", "0.3.0")               # a version in old/ is still found
        self.assertEqual(code, 0, out)
        self.assertIn("CATALOG CHANGES 0.1.0", out)

    def test_notice_has_the_queue_form(self):
        code, out = self.run_main(Fake("0.2.0", raw(newer())), "refresh", "--notice", str(self.notice))
        self.assertEqual(code, 0, out)
        lines = self.notice.read_text(encoding="ascii").splitlines()
        self.assertEqual(lines[0], "## [ENT-NEXT] | NOW | Unity | general | ref: game/catalog/master-index.md")
        self.assertIsNotNone(DRAFT.match(lines[0]))
        self.assertTrue(5 <= len(lines) - 1 <= 25, lines)
        self.assertTrue(all(0 < len(line) <= 220 for line in lines), [len(line) for line in lines])
        self.assertEqual(lines[-1], "The catalog files, the craft book and the database follow within the hour.")
        text = "\n".join(lines)
        self.assertIn("0.1.0 to 0.2.0", text)
        self.assertIn("forge_beam", text)
        self.assertIn("old_relic", text)
        self.assertIsNone(re.search(r"\b(?:command|drone|hauler|miner|scout|sentinel|trader)-[0-9]+\b", text))

    def test_list_order_alone_is_no_change_in_figures(self):
        cat = catalog("0.2.0")
        for ship in cat["ships"]:
            ship["build_materials"] = list(reversed(ship["build_materials"] + [{"item_id": "ore_1", "quantity": 3}]))
        old = catalog("0.1.0")
        for ship in old["ships"]:
            ship["build_materials"] = ship["build_materials"] + [{"item_id": "ore_1", "quantity": 3}]
        out = "\n".join(refresher.summary(old, cat))
        self.assertIn("hulls: 2 -> 2 | added 0 | removed 0 | changed 2 (0 in figures, 0 in text only, 2 in list order only)", out)
        self.assertIn("list order only (the same materials and quantities): barge, skiff", out)
        cat["ships"][0]["build_materials"][0]["quantity"] = 4                                 # now a quantity moved too
        self.assertIn("skiff: build_materials: ore_1 3 -> 4", "\n".join(refresher.summary(old, cat)))
        text = refresher.notice(catalog("0.1.0"), catalog("0.2.0"), REPO)                  # nothing but the version
        self.assertIn("Only the version moved", text)
        self.assertTrue(5 <= len(text.splitlines()) - 1 <= 25)

    def test_notice_leaves_out_a_pilot_name(self):
        cat = newer()
        cat["recipes"].append(dict(cat["recipes"][0], id="miner-7"))
        text = refresher.notice(catalog("0.1.0"), cat, REPO)
        self.assertNotIn("miner-7", text)
        self.assertIn("left out", text)

    def test_dry_run_writes_nothing(self):
        before = self.snapshot()
        code, out = self.run_main(Fake("0.2.0", raw(newer())), "refresh", "--dry-run", "--notice", str(self.notice))
        self.assertEqual((code, self.snapshot(), self.notice.exists()), (0, before, False))
        self.assertIn("DRY RUN: would install 0.2.0.json", out)
        self.assertIn("added: forge_beam", out)
        code, out = self.run_main(Fake("0.2.0", b"not json"), "refresh", "--dry-run")
        self.assertEqual((code, self.snapshot()), (1, before))

    def test_a_copy_written_by_another_hand_is_announced_once(self):
        self.run_main(Fake("0.1.0", b""), "refresh")
        self.put("0.2.0", newer())                                                             # the route maker's daily fetch
        code, out = self.run_main(Fake("0.2.0", b""), "refresh", "--notice", str(self.notice))
        self.assertEqual(code, 0, out)
        self.assertIn("not announced yet", out)
        self.assertTrue(self.notice.is_file())
        self.notice.unlink()
        code, out = self.run_main(Fake("0.2.0", b""), "refresh", "--notice", str(self.notice))
        self.assertEqual((code, self.notice.exists()), (0, False))

    def test_same_version_other_content_keeps_the_old_bytes(self):
        code, out = self.run_main(Fake("0.1.1", raw(dict(newer("0.1.0")))), "refresh")
        self.assertEqual(code, 0, out)
        kept = list((self.folder / "old").glob("0.1.0-*.json"))
        self.assertEqual(len(kept), 1)
        self.assertEqual(json.loads(kept[0].read_text())["recipes"][-1]["id"], "relic_polish")
        self.assertEqual(json.loads((self.folder / "0.1.0.json").read_text())["recipes"][-1]["id"], "forge_beam")
        self.assertIn("published again with other content", out)

    def test_check_and_diff(self):
        code, out = self.run_main(Fake("0.2.0"), "check")
        self.assertEqual((code, out.strip()), (0, "ours: 0.1.0 | live: 0.2.0 | differ"))
        code, out = self.run_main(Fake("0.1.0"), "check")
        self.assertIn("| same", out)
        code, out = self.run_main(Fake("0.2.0"), "diff", "0.1.0", "9.9.9")
        self.assertEqual(code, 1)
        cat = newer()
        for item in cat["items"]:
            item["base_value"] += 1                                                           # nine items change in figures
        self.put("0.2.0", cat)
        code, out = self.run_main(Fake("0.2.0"), "diff", "0.1.0", "0.2.0", "--top", "1")
        self.assertEqual(code, 0)
        self.assertIn("    (and 8 more changed in figures)", out)
        self.assertEqual(len([line for line in out.splitlines() if line.startswith("    ore_")]), 1)
        code, out = self.run_main(Fake("0.2.0"), "diff", "0.1.0", "0.2.0", "--top", "0")
        self.assertEqual(len([line for line in out.splitlines() if line.startswith("    ore_") or line.startswith("    steel_plate")]), 9)

    def test_notice_inside_the_repository_is_refused(self):
        code, out = self.run_main(Fake("0.2.0", raw(newer())), "refresh", "--notice", str(REPO / "notice.txt"))
        self.assertEqual(code, 1)
        self.assertIn("outside the repository", out)
        self.assertFalse((self.folder / "0.2.0.json").exists())

    def test_fetch_unpacks_gzip_and_returns_304(self):
        class Answer(io.BytesIO):
            status, headers = 200, {"Content-Encoding": "gzip", "ETag": '"z"'}

        real = refresher.urllib.request.urlopen
        self.addCleanup(setattr, refresher.urllib.request, "urlopen", real)
        refresher.urllib.request.urlopen = lambda request, timeout: Answer(gzip.compress(b'{"version": "1.0"}'))
        self.assertEqual(refresher.fetch("https://x/api/catalog.json", {}), (200, {"content-encoding": "gzip", "etag": '"z"'}, b'{"version": "1.0"}'))

        def not_modified(request, timeout):
            raise urllib.error.HTTPError(request.full_url, 304, "Not Modified", {"ETag": '"z"'}, None)

        refresher.urllib.request.urlopen = not_modified
        self.assertEqual(refresher.fetch("https://x/api/catalog.json", {"If-None-Match": '"z"'}), (304, {"etag": '"z"'}, b""))


if __name__ == "__main__":
    unittest.main()

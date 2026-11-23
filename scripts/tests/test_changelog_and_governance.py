#!/usr/bin/env python3
"""Unit tests for changelog-refresh.py, store.py game_releases, server.py handed_over_24h & game_version, and Constitution v8."""

import importlib.util
import json
from pathlib import Path
import sqlite3
import sys
import tempfile
import unittest

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "game" / "fleet"))


def load_mod(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


SAMPLE_RSS = b"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>SpaceMolt Patch Notes</title>
    <item>
      <title>SpaceMolt v0.733.0</title>
      <guid>https://spacemolt.com/changelog#v0.733.0</guid>
      <pubDate>Sun, 22 Nov 2026 20:00:00 GMT</pubDate>
      <description>&lt;ul&gt;&lt;li&gt;Added Tier-3 refinery recipes \xe2\x80\x94 faster smelting.&lt;/li&gt;&lt;li&gt;Fixed wormhole scan range.&lt;/li&gt;&lt;/ul&gt;</description>
    </item>
    <item>
      <title>SpaceMolt v0.732.3</title>
      <guid>https://spacemolt.com/changelog#v0.732.3</guid>
      <pubDate>Sun, 22 Nov 2026 12:00:00 GMT</pubDate>
      <description>&lt;ul&gt;&lt;li&gt;Fixed corral pen capacity.&lt;/li&gt;&lt;/ul&gt;</description>
    </item>
  </channel>
</rss>
"""


class ChangelogAndGovernanceTests(unittest.TestCase):
    def test_parse_rss_and_update_patch_notes_idempotently(self):
        cl = load_mod("changelog_refresh", REPO / "scripts" / "changelog-refresh.py")
        rels = cl.parse_rss(SAMPLE_RSS)
        self.assertEqual([r["version"] for r in rels], ["0.733.0", "0.732.3"])
        self.assertIn("Added Tier-3 refinery recipes -- faster smelting.", rels[0]["bullets"][0])
        self.assertTrue(all(ord(ch) <= 127 for ch in json.dumps(rels)))

        with tempfile.TemporaryDirectory() as tmp:
            rules = Path(tmp) / "game" / "rules"
            rules.mkdir(parents=True)
            md = rules / "15-patch-notes.md"
            md.write_text("# Rules 15 -- Patch Notes (read 2026-11-21)\n\n| Version | Change |\n|---|---|\n| 0.732.3 | Fixed corral pen capacity. |\n", encoding="ascii")
            added = cl.update_patch_notes_md(tmp, rels)
            self.assertEqual(added, ["0.733.0"])
            self.assertEqual(cl.update_patch_notes_md(tmp, rels), [])
            txt = md.read_text(encoding="ascii")
            self.assertIn("| 0.733.0 | Added Tier-3 refinery recipes -- faster smelting. Fixed wormhole scan range. |", txt)

    def test_an_unchanged_feed_still_brings_the_notes_to_the_releases_on_disk(self):
        # requests ENT-382: the feed answered 304 every hour after a commit that did not happen; the notes stood behind
        import subprocess
        import types
        import urllib.error
        cl = load_mod("changelog_refresh_304", REPO / "scripts" / "changelog-refresh.py")
        with tempfile.TemporaryDirectory() as tmp:
            root, data = Path(tmp) / "repo", Path(tmp) / "data"
            (root / "game" / "rules").mkdir(parents=True)
            (data / "catalog").mkdir(parents=True)
            md = root / "game" / "rules" / "15-patch-notes.md"
            md.write_text("# Rules 15 -- Patch Notes\n\n| Version | Change |\n|---|---|\n| 0.732.3 | Fixed corral pen capacity. |\n", encoding="ascii")
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            subprocess.run(["git", "-C", str(root), "add", "-A"], check=True)
            subprocess.run(["git", "-C", str(root), "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "-m", "init"], check=True)
            rels = [{"version": "0.733.0", "sort_key": "00000.00733.00000", "pub_date": "Mon, 23 Nov 2026", "summary": "Shipping claims.", "bullets": ["Shipping claims."]},
                    {"version": "0.732.3", "sort_key": "00000.00732.00003", "pub_date": "Sun, 22 Nov 2026", "summary": "Corral fix", "bullets": ["Corral fix"]}]
            (data / "catalog" / "releases.json").write_text(json.dumps({"latest": "0.733.0", "releases": rels}), encoding="ascii")
            (data / "catalog" / "releases-state.json").write_text(json.dumps({"etag": "x"}), encoding="ascii")

            def not_modified(req, timeout=None):
                raise urllib.error.HTTPError(req.full_url, 304, "Not Modified", {}, None)
            self.addCleanup(setattr, cl.urllib.request, "urlopen", cl.urllib.request.urlopen)   # the module is shared: put it back
            cl.urllib.request.urlopen = not_modified
            args = types.SimpleNamespace(data=str(data), root=str(root), rss_url="https://example.invalid/rss.xml", commit=True)
            self.assertEqual(cl.cmd_refresh(args), 0)
            self.assertIn("| 0.733.0 |", md.read_text(encoding="ascii"))
            log = subprocess.run(["git", "-C", str(root), "log", "--format=%s"], capture_output=True, text=True).stdout
            self.assertIn("0.733.0", log)

    def test_store_loads_game_releases_into_sqlite(self):
        import store
        with tempfile.TemporaryDirectory() as tmp:
            cat = Path(tmp) / "catalog"
            cat.mkdir(parents=True)
            rel_file = cat / "releases.json"
            rel_file.write_text(json.dumps({
                "latest": "0.732.3",
                "releases": [{"version": "0.732.3", "sort_key": "00000.00732.00003", "pub_date": "Sun, 22 Nov 2026", "summary": "Corral fix", "bullets": ["Corral fix"]}],
            }), encoding="ascii")
            files = store.game_release_files(tmp, REPO / "game")
            self.assertEqual(len(files), 1)
            loaded = store.read_game_releases(rel_file, {})
            self.assertEqual(loaded["game_releases"][0]["version"], "0.732.3")

    def test_constitution_v8_and_protocol_safeguards_present(self):
        const = (REPO / "governance" / "the-collective-constitution.md").read_text(encoding="ascii")
        proto = (REPO / "communications" / "protocol.md").read_text(encoding="ascii")
        self.assertIn("comms_guard.py", const)
        self.assertIn("zero trust laundering", const)
        self.assertIn("contracts.log", const)
        self.assertIn("| 8 | 2026-11-22 | Trinity |", const)
        self.assertIn("`contracts.log`", proto)

    def test_server_sums_handed_over_worth_across_divisions_and_reports_game_version(self):
        srv = load_mod("station_srv_test", REPO / "station" / "server.py")
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            for d in ("station", "data/fleet", "data/store", "data/catalog", "repo/game/map"):
                (base / d).mkdir(parents=True)
            srv.DATA, srv.FLEET, srv.REPO = base / "station", base / "data/fleet", base / "repo"
            (base / "station/stats.json").write_text(json.dumps({"version": "0.732.3"}), encoding="ascii")
            (base / "data/catalog/0.732.3.json").write_text(json.dumps({"version": "0.732.3"}), encoding="ascii")
            (base / "data/catalog/releases.json").write_text(json.dumps({"latest": "0.732.3", "releases": []}), encoding="ascii")
            db = base / "data/store/read.db"
            con = sqlite3.connect(db)
            con.execute("CREATE TABLE holdings (item TEXT, units INTEGER)")
            con.execute("CREATE TABLE items (id TEXT, base_value INTEGER)")
            con.execute("CREATE TABLE books (item TEXT, bid INTEGER, bid_qty INTEGER)")
            con.execute("CREATE TABLE ships (pilot TEXT, class TEXT, credits INTEGER)")
            con.execute("INSERT INTO ships VALUES ('miner-1', 'Threshold', 50000)")
            con.execute("CREATE TABLE stats_figures (view TEXT, subject TEXT, figure TEXT, hours REAL, value REAL)")
            con.execute("INSERT INTO stats_figures VALUES ('contribution', 'Mining', 'handed_over_worth', 24.0, 125000.0)")
            con.execute("INSERT INTO stats_figures VALUES ('contribution', 'Military', 'handed_over_worth', 24.0, 231000.0)")
            con.execute("CREATE TABLE faction (member_count INTEGER, members_limit INTEGER, treasury INTEGER, owned_bases INTEGER, at_war INTEGER)")
            con.execute("INSERT INTO faction VALUES (99, 200, 1500000, 1, 0)")
            con.commit()
            con.close()
            srv.OPS["at"] = 0.0
            ops = srv.api_ops()
            self.assertEqual(ops["balance_sheet"]["handed_over_24h"], 356000)
            self.assertEqual(ops["game_version"]["live"], "0.732.3")
            self.assertEqual(ops["game_version"]["catalog"], "0.732.3")
            self.assertTrue(ops["game_version"]["in_sync"])


if __name__ == "__main__":
    unittest.main()

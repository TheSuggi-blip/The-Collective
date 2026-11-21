"""game/fleet/ledger.py keeps the storage book whole across an engine start (requests ENT-284): the resume of 2026-11-21, when a
fleet file of 5 ships took 241 pilots out of the book and the iron chain read a seventh of the iron held; a pilot that left the
fleet leaves the book, a flagship never; the book says how whole it is; supply's chain reads the whole stock, and duty puts no
source in on a book that is not whole. Disposable data folders, a fake storage view; no engine, no network."""

import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import time
import unittest

os.environ.setdefault("FLEET_TAXES", os.devnull)   # no test reads the fleet's own tax record

ROOT = Path(__file__).resolve().parents[2]
FLEET = ROOT / "game" / "fleet"
sys.path.insert(0, str(FLEET))


def load(name):
    spec = importlib.util.spec_from_file_location(name + "_whole_under_test", FLEET / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


ledger = load("ledger")
START = "2026-11-17T21:22:47.477Z"                 # the engine's start on record before the pause
BEFORE = "2026-11-18T01:04:00Z"                    # every pilot's last reading before the pause
ROLES = (("drone", 70), ("hauler", 40), ("miner", 60), ("scout", 36), ("trader", 40))
NAMES = sorted("%s-%d" % (role, n) for role, count in ROLES for n in range(1, count + 1))      # 246 pilots, the rotation's order
IRON = {name: 1000 if name.startswith("miner-") else 100 for name in NAMES}                     # 60 miners hold most of the iron
WHOLE_IRON = sum(IRON.values())                                                                 # 78,600


def write(path, value, mtime=None):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value if isinstance(value, str) else json.dumps(value), encoding="ascii")
    if mtime is not None:
        os.utime(path, (mtime, mtime))


def look(pilot, station):
    """The storage view as the gate answers it: the list of places at any station, the goods at base_a."""
    return ({}, ["base_a"], "") if station == ledger.HOME else ({"iron_ore": IRON[pilot]}, [], "")


class Tree(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="fleet-ledger-whole-test-")
        self.addCleanup(self.temp.cleanup)
        self.data, self.root = Path(self.temp.name) / "data", Path(self.temp.name) / "game"
        (self.data / "fleet" / "ships").mkdir(parents=True)
        (self.data / "routes").mkdir(parents=True)

    def fleet(self, names, ok=True, started=START):
        ships = [{"name": name, "status": "connected", "division": "x"} for name in names]
        write(self.data / "fleet" / "fleet.json", {"engine": {"ok": ok, "started_at": started} if ok else {"ok": False}, "ships": ships, "away": []})

    def signed_in(self, names, at):
        with open(self.data / "fleet" / "presence.jsonl", "a", encoding="ascii") as handle:
            handle.write("".join(json.dumps({"at": at, "pilot": name, "sign": 1}) + "\n" for name in names))

    def whole_book(self):
        """A book that held every pilot before the pause."""
        return {"pilots": {name: {"read_at": BEFORE, "stations": {"base_a": {"iron_ore": IRON[name]}}} for name in NAMES}}

    def ledger_pass(self, book, read):
        """One storage pass in the order of ledger.main: the pilots leave that left the fleet, the batch is read, the book
        is written."""
        ledger.leave(book, str(self.data))
        for pilot in read:
            entry = ledger.read_pilot(pilot, look=look, pause=0)
            if "error" in entry and "stations" in (book["pilots"].get(pilot) or {}):
                entry = dict(book["pilots"][pilot], error=entry["error"], error_at=entry["read_at"])
            book["pilots"][pilot] = entry
        ledger.save_storage(book, str(self.data))
        return json.loads((self.data / "stock" / "storage.json").read_text())

    def resume(self):
        """The resume of 2026-11-21: the pause's fleet file names nobody, the first file of the sign-in names 5 ships while
        the engine answers (19:20:32 UTC), then all 246 (19:23:38); the ledger reads 7 pilots a pass in its rotation until 89
        are read (19:34 UTC: no miner among them)."""
        book = self.whole_book()
        self.fleet([])
        self.ledger_pass(book, [])
        first = NAMES[:5]
        self.fleet(first)
        self.signed_in(first, ledger.stamp("2026-11-21T19:20:32Z"))
        self.ledger_pass(book, first)
        self.fleet(NAMES)
        self.signed_in(NAMES[5:], ledger.stamp("2026-11-21T19:23:38Z"))
        for turn in range(5, 89, 7):
            written = self.ledger_pass(book, NAMES[turn:min(turn + 7, 89)])
        return written


class ResumeTests(Tree):
    def test_the_resume_s_book_keeps_every_pilot_and_its_totals_hold(self):
        written = self.resume()
        self.assertEqual(sum(1 for name in NAMES[:89] if name.startswith("miner-")), 0)          # the resume's case: no miner read yet
        self.assertEqual(written["totals"]["by_station"]["base_a"]["iron_ore"], WHOLE_IRON)       # orig: 8,900 of 78,600, the 241 were taken out
        self.assertEqual(len(written["pilots"]), 246)
        self.assertEqual(written["pilots"]["miner-1"]["read_at"], BEFORE)                         # a kept row carries the time it was read
        self.assertNotEqual(written["pilots"][NAMES[0]]["read_at"], BEFORE)                       # a pilot read again carries its new reading
        whole = written["whole"]
        self.assertEqual({k: whole[k] for k in ("pilots", "held", "fresh", "kept", "missing", "oldest", "whole")},
                         {"pilots": 246, "held": 246, "fresh": 89, "kept": 157, "missing": 0, "oldest": BEFORE, "whole": True})
        self.assertEqual((whole["engine_started"], whole["signed_in"]), (START, "2026-11-21T19:23:38Z"))
        self.assertEqual(ledger.decides(whole), (True, "246 of 246 pilots held, 89 read since their sign in, 157 kept from before, "
                                                        "the oldest reading 2026-11-18T01:04:00Z"))

    def test_an_engine_start_makes_every_reading_kept_until_it_is_read_again(self):
        book = self.whole_book()
        self.fleet(NAMES)
        self.assertEqual(self.ledger_pass(book, NAMES[:3])["whole"]["fresh"], 246)              # no sign in since the readings: all fresh
        self.fleet(NAMES, started="2099-01-01T00:00:00.000Z")                                     # the engine started again
        written = self.ledger_pass(book, [])
        self.assertEqual((written["whole"]["fresh"], written["whole"]["kept"], written["totals"]["by_station"]["base_a"]["iron_ore"]), (0, 246, WHOLE_IRON))
        self.fleet(NAMES, ok=False)                                                               # the collector holds the sign-in back: no start in the file
        self.assertEqual(self.ledger_pass(book, [])["whole"]["engine_started"], "2099-01-01T00:00:00.000Z")      # the last one stands in

    def test_a_lost_book_is_not_whole_and_says_whom_it_lacks(self):
        self.fleet(NAMES)
        written = self.ledger_pass({"pilots": {}}, NAMES[:10])
        whole = written["whole"]
        self.assertEqual((whole["pilots"], whole["held"], whole["missing"], whole["whole"]), (246, 10, 236, False))
        self.assertEqual(whole["missing_names"], NAMES[10:22])
        ok, text = ledger.decides(whole)
        self.assertFalse(ok)
        self.assertIn("no reading of 236: %s ..." % ", ".join(NAMES[10:22]), text)
        self.assertTrue(text.endswith("NOT WHOLE (below 95 percent of the fleet)"))
        self.assertEqual(ledger.decides({}), (True, "how whole it is not said (a book written before the ledger said it)"))   # an old book is judged as it stands
        self.assertEqual(ledger.book_whole(str(self.data))["held"], 10)


class LeaveTests(Tree):
    def test_a_pilot_that_left_the_fleet_leaves_the_book_and_a_flagship_never(self):
        now = 1_800_000_000
        write(self.data / "fleet" / "flagships.json", {"Prime Directive": {"role": "command", "division": "Command"}})
        book = self.whole_book()
        for name in ("miner-999", "Prime Directive"):
            book["pilots"][name] = {"read_at": BEFORE, "stations": {"base_a": {"iron_ore": 5}}}
        book["pilots"]["Faction"] = {"member": "Faction", "read_at": BEFORE, "stations": {"base_o": {"iron_ore": 7}}}
        self.fleet(NAMES)                                                                         # names the fleet, not miner-999 nor the flagship
        self.assertEqual(ledger.leave(book, str(self.data), now), [])                             # left out once: its count starts
        self.assertEqual(book["unlisted"], {"miner-999": ledger.time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now))})
        self.assertEqual(ledger.leave(book, str(self.data), now + ledger.LEAVE_AFTER - 1), [])
        self.assertEqual(ledger.leave(book, str(self.data), now + ledger.LEAVE_AFTER), ["miner-999"])
        self.assertEqual((sorted(set(book["pilots"]) - set(NAMES)), book["unlisted"]), (["Faction", "Prime Directive"], {}))

    def test_a_file_of_part_of_the_fleet_or_none_takes_nobody_out(self):
        now = 1_800_000_000
        book = self.whole_book()
        self.fleet(NAMES[:5])                                                                     # the engine signs its pilots in
        self.assertEqual(ledger.leave(book, str(self.data), now), [])
        self.assertEqual(ledger.leave(book, str(self.data), now + ledger.LEAVE_AFTER), [])        # 5 of 246 is no roster to leave by
        self.fleet(NAMES[:5], ok=False)                                                           # a pass held back: every count ends
        self.assertEqual((ledger.leave(book, str(self.data), now + ledger.LEAVE_LONG), book["unlisted"]), ([], {}))
        self.fleet(NAMES[:5])
        self.assertEqual(ledger.leave(book, str(self.data), now + ledger.LEAVE_LONG + 10), [])   # counted anew from here
        gone = ledger.leave(book, str(self.data), now + 2 * ledger.LEAVE_LONG + 10)
        self.assertEqual((len(gone), len(book["pilots"])), (241, 5))                              # a day outside every file: they left
        away = {"engine": {"ok": True}, "ships": [{"name": "miner-1"}], "away": [{"name": "miner-2", "division": "Mining"}]}
        write(self.data / "fleet" / "fleet.json", away)
        self.assertEqual(ledger.roster(str(self.data)), {"miner-1", "miner-2"})                   # a pilot held signed out is of the fleet


class ReaderTests(Tree):
    CHAINS = ("chain\titem\tplace\tkeep\tneed_per_hour\tsources\tkeeper\tnote\n"
              "iron-ore\tiron_ore\tfleet\t%d\t0\tmine-a,mine-b\tMining\tthe test's chain\n")

    def store_pass(self, keep, now):
        write(self.data / "catalog" / "0.2.0.json", {"version": "0.2.0", "items": [{"id": "iron_ore"}]})
        write(self.root / "supply" / "chains.tsv", self.CHAINS % keep)
        for rid in ("mine-a", "mine-b"):
            write(self.root / "routes" / (rid + ".json"), {"id": rid, "kind": "mine", "title": rid, "belt": "sys_a:sys_a_belt", "standing": True,
                                                         "min_left": {"iron_ore": 10}})
        write(self.root / "routes" / "plans" / "miner.json", {"role": "miner", "owner": "Zero", "routes": ["mine-a"], "ships": {}})
        store = load("store")
        store.one_pass(str(self.data), now=now, root=str(self.root))
        import supply
        return supply, supply.read(str(self.data))

    def test_the_supply_chain_reads_the_whole_stock_after_the_resume(self):
        self.resume()
        supply, res = self.store_pass(60000, time.time())
        row = next(r for r in res["rows"] if r["chain"] == "iron-ore")
        self.assertEqual((row["stock"], row["status"]), (WHOLE_IRON, "low"))                      # orig: 8,900, short
        self.assertIn("246 of 246 pilots held, 89 read since their sign in", supply.first_line("T", res))

    def test_duty_puts_no_source_in_on_a_book_that_is_not_whole(self):
        self.fleet(NAMES)
        book = self.ledger_pass({"pilots": {}}, NAMES[:10])                                     # a lost book: 10 of 246 read
        supply, res = self.store_pass(500000, time.time())
        self.assertEqual(res["whole"], False)
        steps = supply.steps(res, {}, time.time(), str(self.root))
        self.assertEqual(steps["divisions"], {})
        self.assertTrue(any(line.startswith("iron-ore (Mining: iron_ore at fleet, 1,000 of 500,000): not judged, the storage book is not whole") for line in steps["lines"]))
        self.assertIn("10 of 246 pilots held", supply.first_line("T", res))
        due = {"mining/mine-b": {"division": "mining", "route": "mine-b", "chain": "iron-ore", "until": "2026-01-01T00:00:00Z"}}
        steps = supply.steps(res, due, time.time(), str(self.root))
        self.assertEqual((steps["renew"], steps["divisions"]), ([], {}))                          # its end came: held, not renewed
        self.assertTrue(any(line.startswith("HOLD mine-b in the mining plan") for line in steps["lines"]))
        self.ledger_pass(book, NAMES[10:])                                                        # every pilot read: whole
        supply, res = self.store_pass(500000, time.time() + 60)
        steps = supply.steps(res, due, time.time(), str(self.root))
        self.assertEqual((res["whole"], steps["renew"], steps["divisions"]), (True, ["mining/mine-b"], {"mining": {"add": [("mine-b", "iron-ore")], "end": []}}))


if __name__ == "__main__":
    unittest.main()

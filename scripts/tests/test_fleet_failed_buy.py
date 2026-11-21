"""A failed buy ends a run (Mercury, errors.log ENT-113, DECISIONS Q75 (6)): the circuit stop option `stop_on_failed_buy`,
run through the whole runner on the fake gate of test_fleet_route_run (no engine, no network); and the verb
`gate.py book_onetime <pilot> "<title>" <credits>` on a disposable data folder (it sends no call)."""

import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_fleet_route_run import fly, steps            # noqa: E402  the runner on a fake gate

FLEET = Path(__file__).resolve().parents[2] / "game" / "fleet"
SILVER = {"id": "made-up", "kind": "circuit", "title": "t", "stops": [
    {"at": "node_alpha:core:node_alpha_processing_station", "buy": [{"item": "silver_bar", "qty": 50, "max_price": 420}], "stop_on_failed_buy": True},
    {"at": "arneb:core:arneb_station", "sell": [{"item": "silver_bar", "min_price": 480}]}]}


class FailedBuyTests(unittest.TestCase):
    def test_a_buy_that_gets_nothing_ends_the_run_at_its_stop_and_the_row_says_why(self):
        # 2026-11-21: Node Alpha's silver ask was gone after one load; the second run flew on to Arneb empty
        log, world, row, out = fly(SILVER, {"book": {"silver_bar": {"best_sell": 0, "best_sell_qty": 0}}})
        self.assertEqual([s for s in steps(log) if s.startswith("goal prepare-at-station")], ["goal prepare-at-station"], out)   # never the second stop
        self.assertEqual((row["stops"], row["of"]), (1, 2))
        self.assertIn("stop 1: the buy of silver_bar got nothing: run ended (stop_on_failed_buy)", row["notes"])
        self.assertIn("run ended (stop_on_failed_buy)", [line for line in out.splitlines() if line.startswith("RESULT")][0])

    def test_a_buy_that_gets_its_load_goes_on_and_a_stop_without_the_option_goes_on_as_before(self):
        book = {"silver_bar": {"best_sell": 400, "best_sell_qty": 60, "best_buy": 500, "best_buy_qty": 60}}
        log, world, row, out = fly(SILVER, {"book": book, "credits": 90000})
        self.assertEqual((row["stops"], world["cargo"].get("silver_bar", 0)), (2, 0), out)
        plain = dict(SILVER, stops=[{k: v for k, v in SILVER["stops"][0].items() if k != "stop_on_failed_buy"}, SILVER["stops"][1]])
        log, world, row, out = fly(plain, {"book": {"silver_bar": {"best_sell": 0, "best_sell_qty": 0}}})
        self.assertEqual(row["stops"], 2, out)                                   # without the option a failed buy only notes, as before


class BookVerbTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="fleet-book-verb-test-")
        self.addCleanup(self.temp.cleanup)
        (Path(self.temp.name) / "fleet").mkdir()
        spec = importlib.util.spec_from_file_location("gate_book_verb_test", FLEET / "gate.py")
        self.gate = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.gate)
        self.saved = self.gate.division.DATA
        self.gate.division.DATA = self.temp.name
        self.addCleanup(setattr, self.gate.division, "DATA", self.saved)
        self.gate.call = lambda *a, **k: self.fail("the verb sends no call to the game")
        self.addCleanup(os.environ.pop, "HERMES_SESSION_PROFILE", None)

    def verb(self, member, *args):
        os.environ["HERMES_SESSION_PROFILE"] = member
        saved, sys.argv = sys.argv, ["gate.py", "book_onetime"] + list(args)
        out = io.StringIO()
        try:
            with contextlib.redirect_stdout(out):
                self.gate.main()
        finally:
            sys.argv = saved
        return out.getvalue()

    def rows(self):
        return json.loads((Path(self.temp.name) / "fleet" / "onetime.json").read_text())

    def test_an_admiral_books_a_once_amount_of_its_own_pilot_once(self):
        text = self.verb("mercury", "trader-7", "Freighter hull bought (once)", "-48,500")
        self.assertIn("one-time money booked: trader-7 -48500 cr, Freighter hull bought (once)", text)
        self.assertEqual([r[1:] for r in self.rows()], [["trader-7", "Freighter hull bought (once)", -48500]])
        with self.assertRaises(SystemExit) as stop:
            self.verb("mercury", "trader-7", "Freighter hull bought (once)", "-48500")
        self.assertIn("was booked at", str(stop.exception))
        with self.assertRaises(SystemExit) as stop:
            self.verb("mercury", "miner-1", "Silver run", "4099")
        self.assertIn("miner-1 is commanded by Zero, not by Mercury", str(stop.exception))
        with self.assertRaises(SystemExit) as stop:
            self.verb("unity", "trader-7", "Wallet top-up", "5000")
        self.assertIn("none of wallet.py's own", str(stop.exception))
        self.assertEqual(len(self.rows()), 1)


if __name__ == "__main__":
    unittest.main()

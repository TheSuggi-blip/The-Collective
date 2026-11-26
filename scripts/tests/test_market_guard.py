#!/usr/bin/env python3
"""Unit tests for open-market anti-manipulation engine (game/fleet/market_guard.py)."""
import json
import sys
import tempfile
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "game" / "fleet"))
import bursar
import haul
import market_guard as mg


class MarketGuardTests(unittest.TestCase):
    def test_vwm_ignores_single_station_spoof_spike_and_cltv_own_orders(self):
        now_t = time.time()
        books = [
            {"base": "sol", "item": "silicon_ore", "bid": 7, "bid_qty": 196000, "t": now_t},
            {"base": "ge", "item": "silicon_ore", "bid": 10, "bid_qty": 8500, "t": now_t},
            {"base": "crimson", "item": "silicon_ore", "bid": 11, "bid_qty": 200, "t": now_t},
            {"base": "exp", "item": "silicon_ore", "bid": 421, "bid_qty": 41, "t": now_t},
            {"base": "crucible", "item": "silicon_ore", "bid": 795, "bid_qty": 200, "t": now_t},
        ]
        # Exclude CLTV's own poisoned order at crucible; VWM MUST stay ~7 cr, NOT 421 or 795 cr!
        vwm = mg.compute_book_vwm_map(books, cltv_buy_keys={("crucible", "silicon_ore")}, now_t=now_t)
        self.assertIn("silicon_ore", vwm)
        self.assertLessEqual(vwm["silicon_ore"]["vwm"], 12.0)

    def test_luld_twap_blocks_flash_pump_but_freely_adapts_to_genuine_multi_hour_shift(self):
        with tempfile.TemporaryDirectory() as td:
            t0 = 1795650000.0
            # Seed oracle at 10 cr across 3 stations
            r0 = mg.update_price_oracle(td, {"silicon_ore": {"vwm": 10.0, "stations": 3, "total_qty": 5000}}, now_t=t0)
            self.assertEqual(r0["silicon_ore"]["fair_price"], 10.0)
            # 5 minutes later, flash pump to 800 cr at 1 station -> LULD MUST clamp hard (< 15 cr)!
            r1 = mg.update_price_oracle(td, {"silicon_ore": {"vwm": 800.0, "stations": 1, "total_qty": 20}}, now_t=t0 + 300)
            self.assertLess(r1["silicon_ore"]["fair_price"], 15.0)
            # Over 12 genuine hours at 50 cr across 4 deep stations -> oracle smoothly tracks upward without static cap!
            cur_t = t0 + 3600
            for _ in range(12):
                r_up = mg.update_price_oracle(td, {"silicon_ore": {"vwm": 50.0, "stations": 4, "total_qty": 5000}}, now_t=cur_t, min_write_interval_s=0)
                cur_t += 3600
            self.assertGreater(r_up["silicon_ore"]["fair_price"], 28.0)

    def test_bait_ask_detector_and_same_station_anti_self_outbid(self):
        # Troll parks 1,000 cr ask on 10 cr ore with 0 local bid -> safe_buy_ceiling caps at ~13 cr, NEVER 765 cr!
        c = mg.safe_buy_ceiling("silicon_ore", local_bid=0, local_ask=1000, fair_val=10.0, max_ratio=0.90)
        self.assertLessEqual(c, 15)
        self.assertGreaterEqual(c, 5)
        # Unanchored item (fair_val=0) with 0 local bid and 1,000 cr ask -> REFUSED (0)!
        self.assertEqual(mg.safe_buy_ceiling("mystery_bait", local_bid=0, local_ask=1000, fair_val=0.0), 0)
        # Same-station anti-self-outbid: trader-79 skips silicon_ore when trader-41 already bids it there!
        book = {"silicon_ore": {"best_buy": 10, "best_buy_qty": 200, "best_sell": 15, "best_sell_qty": 100}}
        pol = json.loads(json.dumps(bursar.DEFAULT_POLICY))
        pol["buy"]["enabled"] = True
        acts = bursar.plan_bursar_actions(
            book, {}, [], {"silicon_ore": 500}, set(), {"silicon_ore": 10.0}, 50000, pol,
            same_station_cltv_buys={"silicon_ore"},
        )
        self.assertFalse(any(a[0] == "buy_create" and a[1] == "silicon_ore" for a in acts))

    def test_mirage_arbitrage_scam_blocked_while_legit_arbitrage_passes(self):
        # EVE Margin-Trading Scam: 10 cr item listed at 500 cr ask + fake 800 cr buy wall -> BLOCKED!
        self.assertTrue(mg.is_mirage_arbitrage_trap("junk_ore", buy_ask=500, sell_bid=800, fair_info={"fair_price": 10.0}))
        # Legitimate regional arbitrage: buy at 14 cr (near 15 cr fair value), sell at 32 cr -> ALLOWED!
        self.assertFalse(mg.is_mirage_arbitrage_trap("hydrogen_gas", buy_ask=14, sell_bid=32, fair_info={"fair_price": 15.0}))
        # Integration check with haul.pick_arbitrage_job
        now_t = time.time()
        base_map = {"a": ("sa", "pa", "a", True), "b": ("sb", "pb", "b", True)}
        lanes = {"sa": ["sb"], "sb": ["sa"]}
        books = [
            {"base": "a", "item": "junk_ore", "ask": 500, "ask_qty": 100, "bid": 10, "bid_qty": 100, "t": now_t},
            {"base": "b", "item": "junk_ore", "ask": 900, "ask_qty": 10, "bid": 800, "bid_qty": 100, "t": now_t},
        ]
        pol = {"policed_only": True, "min_margin_pct": 0.20, "min_total_profit": 500, "min_cr_per_jump": 100, "max_buy_spend_cr": 15000}
        job_scam = haul.pick_arbitrage_job(books, base_map, lanes, "sa", 100, 50000, pol, set(), now_t=now_t, fair_prices={"junk_ore": {"fair_price": 10.0}})
        self.assertIsNone(job_scam)


if __name__ == "__main__":
    unittest.main()

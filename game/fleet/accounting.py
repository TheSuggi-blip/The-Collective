#!/usr/bin/env python3
"""accounting.py -- GAAP/IFRS-aligned bookkeeping, IAS 2 NRV inventory valuation, and transfer-priced accrual P&L.

WHAT: Single source of truth for The Collective's consolidated financial statements across
      station/server.py, game/fleet/scorecard.py, game/fleet/progression.py, and game/fleet/watchdog.py:
        1. IAS 2 / ASC 330 Inventory Valuation (vault_valuation):
           - nrv: Lower of Cost (catalog base_value) or Net Realizable Value (best resting bid).
             Eliminates both thin-bid outlier phantom markups (e.g. 814 cr silicon_ore) and
             overpriced illiquid catalog values (e.g. 600 cr quantum_fragments with 3 cr bids).
           - catalog: SpaceMolt catalog base_value sum (apples-to-apples with SpaceMolt leaderboards).
           - liquid: Depth-capped immediate liquidation across visible resting bids (bid_qty capped).
        2. Matching Principle & 3-Statement Cash-to-Accrual P&L (compute_pnl):
           - Separates direct fuel/inputs on non-recurring once=true missions from recurring OpEx,
             matching them directly against one-time mission rewards (IFRS 18 / Matching Principle).
           - Separates Investing CapEx (bought_once hulls/modules/kits, net of fit-upgrade salvage)
             from Operating Cash Flow and Non-Recurring Seed Net (IAS 7).
           - Computes conservative IAS 2 LCNRV Inventory/WIP Accrual from stock_hour so vertical
             production (mining, hunting, reserve crafting) is recognized as Accrual Operating Income
             side-by-side with Recurring Operating Cash Flow (liquidity discipline).
        3. Intercompany Transfer Pricing (by_division):
           - Credits givers and debits receivers for cross-division handovers (handover.jsonl) at
             IAS 2 LCNRV so Mining, Military, Logistics, and Trade reflect true economic value-added
             while consolidating identically to zero at the Fleet level (zero double-counting).

RULES:
  - Read-only on read.db, fleet.json, handover.jsonl, and game/routes/*.json.
  - Pure stdlib, pure 7-bit ASCII (U+0000-U+007F).
  - Never fabricates missing tables/files; degrades cleanly with explicit availability flags.

Usage:
  accounting.py [--hours 24] [--json] [--data <dir>] [--root <dir>]
"""

import argparse
import json
import os
import sqlite3
import sys
import time
from pathlib import Path

REPO_DEFAULT = str(Path(__file__).resolve().parents[2])
DATA_DEFAULT = "/srv/collective/data"
DIVISIONS = ("Command", "Intel", "Logistics", "Military", "Mining", "Trade")
ALL_ACC_DIVS = ("Command", "Intel", "Logistics", "Military", "Mining", "Trade", "Faction")
FIT_PREFIXES = ("fit-", "buy-hull-", "upgrade-")


def _num(v, default=0.0):
    try:
        if v is None or isinstance(v, bool):
            return default
        return float(v)
    except (TypeError, ValueError):
        return default


def _has_table(conn, name):
    try:
        r = conn.execute(
            "SELECT 1 FROM sqlite_master WHERE type IN ('table','view') AND name = ?",
            (name,),
        ).fetchone()
        return r is not None
    except sqlite3.Error:
        return False


def _div_of_pilot(name, pilot_div=None):
    if pilot_div and name in pilot_div and pilot_div[name]:
        return pilot_div[name]
    low = str(name or "").strip().lower()
    if low.startswith(("miner", "excavator", "survey")):
        return "Mining"
    if low.startswith(("trader", "merchant", "bursar")):
        return "Trade"
    if low.startswith(("hauler", "freight", "craft", "courier", "builder")):
        return "Logistics"
    if low.startswith(("drone", "sentinel", "vanguard", "hunter", "escort", "raider")):
        return "Military"
    if low.startswith(("scout", "probe", "watcher", "oracle")):
        return "Intel"
    if low.startswith(("unity", "admiral", "cmd", "command")):
        return "Command"
    return "Other"


def _load_price_maps(conn):
    """Return (base_map, max_bid_map, bids_by_item) from read.db."""
    base_map = {}
    max_bid_map = {}
    bids_by_item = {}
    if conn is None:
        return base_map, max_bid_map, bids_by_item
    if _has_table(conn, "items"):
        for r in conn.execute("SELECT id, COALESCE(base_value, 0) FROM items"):
            if r[0]:
                base_map[str(r[0])] = _num(r[1])
    if _has_table(conn, "books"):
        for r in conn.execute(
            "SELECT item, bid, bid_qty FROM books WHERE bid > 0 AND bid_qty > 0 ORDER BY item, bid DESC"
        ):
            it = str(r[0] or "")
            if not it:
                continue
            price = _num(r[1])
            qty = _num(r[2])
            if price > 0 and qty > 0:
                if it not in max_bid_map or price > max_bid_map[it]:
                    max_bid_map[it] = price
                bids_by_item.setdefault(it, []).append((price, qty))
    return base_map, max_bid_map, bids_by_item


LIVE_DEEP_BID_QTY = 500.0
THIN_SPOOF_QTY = 10.0
GLUT_HOLD_MIN = 50000.0


def _load_market_trends(conn, now=None):
    """Return {item: 24h_avg_bid_hi} from read.db:market_hour for live market trend pricing."""
    trends = {}
    if conn is None or not _has_table(conn, "market_hour"):
        return trends
    now_t = int(time.time() if now is None else now)
    cut = now_t - 86400
    try:
        for r in conn.execute(
            "SELECT item, AVG(bid_hi) FROM market_hour WHERE bid_hi > 0 AND hour >= ? GROUP BY item",
            (cut,),
        ):
            if r[0] and _num(r[1]) > 0:
                trends[str(r[0])] = _num(r[1])
    except sqlite3.Error:
        pass
    return trends


def _load_ask_map(conn):
    """Return {item: (min_ask, total_ask_qty)} from live books where ask > 0."""
    asks = {}
    if conn is None or not _has_table(conn, "books"):
        return asks
    try:
        cols = {c[1] for c in conn.execute("PRAGMA table_info(books)")}
        if "ask" not in cols:
            return asks
        qcol = "COALESCE(ask_qty, 1)" if "ask_qty" in cols else "1"
        for r in conn.execute(
            "SELECT item, MIN(ask), SUM(%s) FROM books WHERE ask > 0 GROUP BY item" % qcol
        ):
            if r[0] and _num(r[1]) > 0:
                asks[str(r[0])] = (_num(r[1]), _num(r[2]))
    except sqlite3.Error:
        pass
    return asks


def _load_sell_escrow(data_dir, now=None, ttl_s=21600.0):
    """Read active Exchange sell-order escrow from data/fleet/bursar_sells.json (fresh <= ttl_s).

    Returns (by_item: {item: qty}, by_div_item: {(div, item): qty}, updated_at: int).
    """
    by_item = {}
    by_div_item = {}
    updated_at = 0
    if not data_dir:
        return by_item, by_div_item, updated_at
    sp = Path(data_dir) / "fleet" / "bursar_sells.json"
    if not sp.is_file():
        return by_item, by_div_item, updated_at
    try:
        doc = json.loads(sp.read_text(encoding="utf-8", errors="replace"))
    except (OSError, ValueError):
        return by_item, by_div_item, updated_at
    if not isinstance(doc, dict):
        return by_item, by_div_item, updated_at
    updated_at = int(_num(doc.get("updated_at")))
    entries = doc.get("entries") if isinstance(doc.get("entries"), dict) else {}
    now_t = float(time.time() if now is None else now)
    for p_nm, bases in entries.items():
        if not isinstance(bases, dict):
            continue
        div_nm = _div_of_pilot(p_nm, {})
        if div_nm == "Other":
            div_nm = "Trade"
        for _b_id, rec in bases.items():
            if not isinstance(rec, dict):
                continue
            if (now_t - _num(rec.get("at"))) > ttl_s:
                continue
            for iid, qty in (rec.get("items") or {}).items():
                q = int(_num(qty))
                if iid and q > 0:
                    s_id = str(iid)
                    by_item[s_id] = by_item.get(s_id, 0) + q
                    by_div_item[(div_nm, s_id)] = by_div_item.get((div_nm, s_id), 0) + q
    return by_item, by_div_item, updated_at


def _sanitized_bids(item, base_map, bids_by_item, trend_map=None):
    """Return [(eff_price, qty)] with thin (<10-unit) spoof outliers capped to max(trend, base)."""
    raw_bids = bids_by_item.get(item) or ()
    bv = base_map.get(item, 0.0)
    tv = (trend_map or {}).get(item, 0.0)
    ref = max(bv, tv, 10.0)
    out = []
    for price, qty in raw_bids:
        p = _num(price)
        q = _num(qty)
        if p <= 0 or q <= 0:
            continue
        if q < THIN_SPOOF_QTY and p > max(3.0 * ref, 100.0):
            p = ref
        out.append((p, q))
    return out


def depth_realizable_value(item, units, base_map, bids_by_item, trend_map=None, ask_map=None):
    """Live fair market valuation using BOTH sides of the live order book (bids + asks) & 24h trends:
      - Never values an item above live replacement cost (min_ask) unless a deep live buy-wall pays more.
      - Uses exact live bid walk for instant buy-walls & cheap raw-commodity gluts (e.g. copper_ore @ ask=1).
      - Avoids 1-cr penny-scraper bid distortion on real crafted/loot goods with healthy live Exchange asks
        (e.g. null_matter ask=201, armor_plate ask=299, circuit_board ask=292) by marking them to
        conservative sell-order realizable value (0.70 * min_ask, bounded by base_value if ask > 2*base).
      - Applies liquidity haircut (>1.5x galaxy bid depth on cheap commodities -> capped to absorbable book).
    """
    u = float(max(0, _num(units)))
    if u <= 0:
        return 0.0
    bv = base_map.get(item, 0.0)
    tv = (trend_map or {}).get(item, 0.0)
    ask_info = (ask_map or {}).get(item)
    min_ask = _num(ask_info[0]) if ask_info else 0.0
    sbids = _sanitized_bids(item, base_map, bids_by_item, trend_map)

    # Walk live bids (instant cash floor)
    rem = u
    bid_v = 0.0
    tot_bid_q = 0.0
    deep_real_q = 0.0
    deep_real_v = 0.0
    last_p = sbids[-1][0] if sbids else 0.0
    for p, q in sbids:
        tot_bid_q += q
        if p >= 10.0:
            deep_real_q += q
            deep_real_v += p * q
        if rem > 0:
            take = min(rem, q)
            bid_v += take * p
            rem -= take
            last_p = p
    if rem > 0 and tot_bid_q > 0:
        marg_p = min(last_p, tv) if tv > 0 else last_p
        bid_v += min(rem, tot_bid_q) * 0.5 * marg_p

    # Case 1: Deep live buy-wall (>=500 qty at >=10 cr) dominates!
    if deep_real_q >= LIVE_DEEP_BID_QTY and u <= deep_real_q:
        return bid_v

    # Case 2: Live Exchange ask exists (bounds replacement cost and avoids 1-cr penny-scraper distortion)
    if min_ask > 0:
        # Cheap raw-material glut (e.g. copper_ore/iron_ore/carapace @ ask <= 5 cr): cap to live book/glut!
        if min_ask < 10.0:
            if u >= GLUT_HOLD_MIN and tot_bid_q > 0 and u > 1.5 * tot_bid_q:
                return min(bid_v, u * min_ask)
            return min(u * min_ask, max(bid_v, u * 0.70 * min_ask))
        # Healthy traded Exchange good (ask >= 10 cr): conservative sell-order fair value
        fair_u = 0.70 * min_ask
        if bv > 0 and min_ask > 2.0 * bv and (deep_real_q < 50):
            fair_u = min(fair_u, bv)
        if tv > 0 and tv < fair_u * 1.5:
            fair_u = min(min_ask, max(fair_u, 0.75 * tv))
        # Apply gentle inventory-overhang discount if holding huge unbid stock (>5000 units)
        if u > 5000.0 and deep_real_q < u * 0.1:
            fair_u *= 0.80
        return max(bid_v, u * fair_u) if deep_real_q >= LIVE_DEEP_BID_QTY else min(u * min_ask, max(bid_v, u * fair_u))

    # Case 3: No live ask -- use bid walk or 24h trend
    if sbids:
        return bid_v
    if tv > 0:
        return u * 0.5 * tv
    return 0.0 if bids_by_item else u * bv


def live_market_unit_price(item, base_map, bids_by_item, trend_map=None, held_units=0, max_bid_map=None, glut_threshold=GLUT_HOLD_MIN, ask_map=None):
    """Live market depth-weighted & trend-aware unit price for gathering/hunting/inventory flows.

    - Deep live bids (>=500 qty, e.g. silver_ore @ 101, uranium_ore @ 600): uses depth-weighted live bid!
    - Modest/thin bids (<500 qty): conservative IAS 2 min(base_value, depth_bid) against illiquid spoofs.
    - Glut guard: if fleet holds >= glut_threshold AND >1.5x total galaxy bid depth at <10 cr, marginal value = 0!
    - Zero live bids: 0.5x 24h market_hour trend if recent trades/bids existed, else 0 cr (when books exist).
    """
    bv = base_map.get(item, 0.0)
    tv = (trend_map or {}).get(item, 0.0)
    sbids = _sanitized_bids(item, base_map, bids_by_item or {}, trend_map)
    if not sbids:
        if tv > 0:
            return 0.5 * tv
        if bids_by_item:
            return 0.0
        return lcnrv_unit_price(item, base_map, max_bid_map or {})
    tot_q = sum(q for _p, q in sbids)
    sample_q = min(tot_q, 2000.0)
    rem = sample_q
    val_sum = 0.0
    for p, q in sbids:
        take = min(rem, q)
        val_sum += take * p
        rem -= take
        if rem <= 0:
            break
    w_bid = val_sum / sample_q if sample_q > 0 else sbids[0][0]
    ask_info = (ask_map or {}).get(item)
    min_ask = _num(ask_info[0]) if ask_info else 0.0
    if float(held_units or 0) >= float(glut_threshold) and float(held_units or 0) > 1.5 * tot_q and (w_bid < 10.0 or (0 < min_ask < 10.0)):
        return 0.0
    # Count real (>=10 cr) buy-wall depth separately from 1-cr penny-scraper bids
    real_q = sum(q for p, q in sbids if p >= 10.0)
    if real_q >= LIVE_DEEP_BID_QTY:
        rq_s = min(real_q, 2000.0)
        rrem, rval = rq_s, 0.0
        for p, q in sbids:
            if p < 10.0:
                continue
            tk = min(rrem, q)
            rval += tk * p
            rrem -= tk
            if rrem <= 0:
                break
        return rval / rq_s if rq_s > 0 else w_bid
    if min_ask > 0:
        if min_ask < 10.0:
            return min(min_ask, w_bid)
        fair_u = 0.70 * min_ask
        if bv > 0 and min_ask > 2.0 * bv and real_q < 50:
            fair_u = min(fair_u, bv)
        return min(min_ask, max(w_bid if w_bid <= min_ask else 0.0, fair_u))
    if tot_q >= LIVE_DEEP_BID_QTY:
        return w_bid
    if bv > 0:
        return min(bv, w_bid)
    return w_bid


def lcnrv_unit_price(item, base_map, max_bid_map):
    """IAS 2 / ASC 330 conservative unit price: min(base_value, best_bid) when both exist."""
    b = base_map.get(item, 0.0)
    m = max_bid_map.get(item)
    if m is not None and m > 0:
        return min(b, m) if b > 0 else m
    return b


def vault_valuation(conn, data_dir=None):
    """Compute vault valuation under IAS 2 NRV, Catalog Base Value, Depth-Capped Liquidation, and Unbounded Bid."""
    empty = {
        "nrv": 0,
        "live_market": 0,
        "catalog": 0,
        "liquid": 0,
        "unbounded_bid": 0,
        "sell_escrow_nrv": 0,
        "sell_escrow_units": 0,
        "items": 0,
        "units": 0,
        "top_gaps": [],
        "gluts": [],
    }
    if conn is None or not _has_table(conn, "holdings"):
        return empty
    base_map, max_bid_map, bids_by_item = _load_price_maps(conn)
    trend_map = _load_market_trends(conn)
    ask_map = _load_ask_map(conn)
    escrow_by_item, _esc_div, _esc_ts = _load_sell_escrow(data_dir) if data_dir else ({}, {}, 0)
    qty_by_item = {}
    for r in conn.execute("SELECT item, SUM(COALESCE(units, 0)) FROM holdings GROUP BY item").fetchall():
        it = str(r[0] or "")
        u = int(_num(r[1]))
        if it and u > 0:
            qty_by_item[it] = qty_by_item.get(it, 0) + u
    escrow_nrv = 0.0
    escrow_units = 0
    for it, eq in escrow_by_item.items():
        if eq > 0:
            qty_by_item[it] = qty_by_item.get(it, 0) + eq
            escrow_units += eq
            escrow_nrv += eq * live_market_unit_price(it, base_map, bids_by_item, trend_map, held_units=qty_by_item[it], max_bid_map=max_bid_map, ask_map=ask_map)
    tot_nrv = 0.0
    tot_live = 0.0
    tot_cat = 0.0
    tot_liq = 0.0
    tot_unb = 0.0
    tot_units = 0
    item_cnt = 0
    gaps = []
    gluts = []
    for it, u in qty_by_item.items():
        if not it or u <= 0:
            continue
        item_cnt += 1
        tot_units += u
        bv = base_map.get(it, 0.0)
        mb = max_bid_map.get(it)
        cat_v = u * bv
        nrv_v = u * lcnrv_unit_price(it, base_map, max_bid_map)
        live_v = depth_realizable_value(it, u, base_map, bids_by_item, trend_map, ask_map=ask_map)
        unb_v = u * (mb if (mb is not None and mb > 0) else bv)
        rem = float(u)
        liq_v = 0.0
        tot_bid_q = 0.0
        for price, qty in bids_by_item.get(it, ()):
            tot_bid_q += qty
            take = min(rem, qty)
            liq_v += take * price
            rem -= take
            if rem <= 0:
                break
        tot_nrv += nrv_v
        tot_live += live_v
        tot_cat += cat_v
        tot_liq += liq_v
        tot_unb += unb_v
        if u >= GLUT_HOLD_MIN and tot_bid_q > 0 and u > 1.5 * tot_bid_q:
            gluts.append({"item": it, "units": u, "bid_depth": int(round(tot_bid_q)), "ratio": round(u / tot_bid_q, 2), "live_market": int(round(live_v)), "nrv": int(round(nrv_v))})
        spread = max(abs(unb_v - nrv_v), abs(cat_v - nrv_v))
        if spread >= 10000:
            gaps.append((
                spread,
                {
                    "item": it,
                    "units": u,
                    "base": int(round(bv)),
                    "max_bid": int(round(mb)) if mb is not None else None,
                    "nrv": int(round(nrv_v)),
                    "live_market": int(round(live_v)),
                    "catalog": int(round(cat_v)),
                    "liquid": int(round(liq_v)),
                    "unbounded_bid": int(round(unb_v)),
                },
            ))
    gaps.sort(key=lambda x: -x[0])
    gluts.sort(key=lambda x: -x["units"])
    return {
        "nrv": int(round(tot_nrv)),
        "live_market": int(round(tot_live)),
        "catalog": int(round(tot_cat)),
        "liquid": int(round(tot_liq)),
        "unbounded_bid": int(round(tot_unb)),
        "sell_escrow_nrv": int(round(escrow_nrv)),
        "sell_escrow_units": int(round(escrow_units)),
        "items": item_cnt,
        "units": tot_units,
        "top_gaps": [g[1] for g in gaps[:5]],
        "gluts": gluts[:5],
    }


def compute_balance_sheet(conn, fleet_json=None, data_dir=DATA_DEFAULT):
    """Single source of truth for Consolidated Balance Sheet & Enterprise Net Worth across /api/ops, /api/progression, and /api/diplomacy."""
    vv = vault_valuation(conn, data_dir=data_dir)
    wallets = 0
    treasury = 0
    fleet_hulls = 0
    fleet_modules = 0
    fleet_book = 0
    facility_invested = 0
    handed_over_24h = 0
    hexc_wealth = 0

    if isinstance(fleet_json, dict):
        fl_ships = [s for s in (fleet_json.get("ships") or []) if isinstance(s, dict)]
        if fl_ships:
            wallets = int(round(sum(_num(s.get("credits")) for s in fl_ships)))

    if conn is not None:
        if not wallets and _has_table(conn, "ships"):
            r = conn.execute("SELECT COALESCE(SUM(credits), 0) FROM ships").fetchone()
            wallets = int(round(_num(r[0]))) if r else 0
        if _has_table(conn, "faction"):
            r = conn.execute("SELECT COALESCE(treasury, 0) FROM faction LIMIT 1").fetchone()
            treasury = int(round(_num(r[0]))) if r else 0

        # Fleet book value = fitted ship_modules + active hull_materials at catalog base_value
        item_val_id = {}
        item_val_lname = {}
        if _has_table(conn, "items"):
            item_cols = {c[1] for c in conn.execute("PRAGMA table_info(items)")}
            q_items = (
                "SELECT id, name, COALESCE(base_value, 0) FROM items"
                if "name" in item_cols else
                "SELECT id, NULL, COALESCE(base_value, 0) FROM items"
            )
            for ir in conn.execute(q_items):
                iv = int(round(_num(ir[2])))
                if ir[0]:
                    item_val_id[str(ir[0])] = iv
                if ir[1]:
                    ln = str(ir[1]).lower()
                    if ln not in item_val_lname:
                        item_val_lname[ln] = iv
        mod_total = 0
        if _has_table(conn, "ship_modules"):
            for mr in conn.execute("SELECT name FROM ship_modules"):
                if mr[0]:
                    mod_total += item_val_lname.get(str(mr[0]).lower(), 0)
        hull_total = 0
        if _has_table(conn, "hull_materials") and _has_table(conn, "hulls") and _has_table(conn, "ships"):
            hm_cost = {}
            for hmr in conn.execute("SELECT hull, item, COALESCE(units, 0) FROM hull_materials"):
                hid = str(hmr[0] or "")
                if hid:
                    hm_cost[hid] = hm_cost.get(hid, 0) + int(round(_num(hmr[2]))) * item_val_id.get(str(hmr[1] or ""), 0)
            hull_by_key = {}
            for hr in conn.execute("SELECT id, name FROM hulls"):
                hid = str(hr[0] or "")
                if not hid:
                    continue
                for k in {hid.lower(), str(hr[1] or "").lower()}:
                    if k:
                        hull_by_key.setdefault(k, set()).add(hid)
            for sr in conn.execute("SELECT class FROM ships"):
                sc = str(sr[0] or "").lower()
                for hid in hull_by_key.get(sc, ()):
                    hull_total += hm_cost.get(hid, 0)
        fleet_hulls = int(hull_total)
        fleet_modules = int(mod_total)
        fleet_book = int(fleet_hulls + fleet_modules)

        # Fallback only if hull_materials table is absent in minimal test fixtures
        if not fleet_book and _has_table(conn, "ships") and _has_table(conn, "hulls"):
            for tier, cnt in conn.execute(
                "SELECT COALESCE(h.tier, 0), COUNT(*) FROM ships s "
                "LEFT JOIN hulls h ON LOWER(h.id) = LOWER(s.class) OR LOWER(h.name) = LOWER(s.class) GROUP BY 1"
            ):
                fleet_hulls += int(_num(cnt)) * ({0: 5000, 1: 65000, 2: 350000, 3: 1500000, 4: 6000000, 5: 25000000}.get(int(_num(tier)), 5000))
            fleet_book = int(fleet_hulls + fleet_modules)

        fac_lb = 0
        fac_sum = 0
        if _has_table(conn, "leaderboards"):
            r = conn.execute(
                "SELECT COALESCE(MAX(value), 0) FROM leaderboards WHERE grp = 'factions' AND board = 'facility_investment' AND tag = 'CLTV'"
            ).fetchone()
            fac_lb = int(round(_num(r[0]))) if r else 0
            hr = conn.execute(
                "SELECT value FROM leaderboards WHERE grp = 'factions' AND board = 'total_wealth' AND tag = 'HEXC' ORDER BY t DESC LIMIT 1"
            ).fetchone()
            hexc_wealth = int(round(_num(hr[0]))) if hr else 0
        if _has_table(conn, "faction_facilities") and _has_table(conn, "facilities"):
            r = conn.execute(
                "SELECT COALESCE(SUM(COALESCE(c.build_cost, 0)), 0) "
                "FROM faction_facilities ff LEFT JOIN facilities c ON c.id = ff.type"
            ).fetchone()
            fac_sum = int(round(_num(r[0]))) if r else 0
        facility_invested = max(fac_lb, fac_sum)

        if _has_table(conn, "stats_figures"):
            r = conn.execute(
                "SELECT COALESCE(SUM(value), 0) FROM stats_figures WHERE view = 'contribution' AND figure = 'handed_over_worth' AND hours = 24"
            ).fetchone()
            handed_over_24h = int(round(_num(r[0]))) if r else 0

    liquid_cash = wallets + treasury
    vault_nrv = int(vv["nrv"])
    vault_cat = int(vv["catalog"])
    vault_live = int(vv.get("live_market", vault_nrv))
    vault_eff = vault_live if vault_live > 0 else vault_nrv
    return {
        "liquid_cash": liquid_cash,
        "wallets": wallets,
        "treasury": treasury,
        "vault_worth": vault_eff,
        "vault_nrv": vault_eff,
        "vault_ias2_static": vault_nrv,
        "vault_live_market": vault_live,
        "vault_sell_escrow_nrv": int(vv.get("sell_escrow_nrv", 0)),
        "vault_sell_escrow_units": int(vv.get("sell_escrow_units", 0)),
        "vault_gluts": vv.get("gluts") or [],
        "vault_catalog": vault_cat,
        "vault_liquid": int(vv["liquid"]),
        "vault_unbounded_bid": int(vv["unbounded_bid"]),
        "vault_top_gaps": vv["top_gaps"],
        "fleet_hulls": fleet_hulls,
        "fleet_modules": fleet_modules,
        "fleet_book": fleet_book,
        "facility_invested": facility_invested,
        "hard_assets": fleet_book + facility_invested,
        "operating_invested_capital": fleet_book + facility_invested + vault_eff,
        "net_worth": liquid_cash + vault_eff + fleet_book + facility_invested,
        "net_worth_ias2": liquid_cash + vault_nrv + fleet_book + facility_invested,
        "net_worth_catalog": liquid_cash + vault_cat + fleet_book + facility_invested,
        "handed_over_24h": handed_over_24h,
        "hexc_wealth": hexc_wealth,
    }


_ONCE_CACHE = {}


def once_route_ids(repo_root):
    """Return (all_once, fit_once, mission_once) route ID sets scanning ALL game/routes/*.json (dir-mtime cached)."""
    rdir = Path(repo_root) / "game" / "routes"
    if not rdir.is_dir():
        return set(), set(), set()
    try:
        key = str(rdir.resolve())
        st = rdir.stat()
        files = list(rdir.glob("*.json"))
        stamp = (st.st_mtime_ns, len(files))
    except OSError:
        return set(), set(), set()
    hit = _ONCE_CACHE.get(key)
    if hit is not None and hit[0] == stamp:
        return hit[1]
    all_once, fit_once, mission_once = set(), set(), set()
    for fp in files:
        try:
            d = json.loads(fp.read_text(encoding="utf-8", errors="replace"))
        except (OSError, ValueError):
            continue
        if isinstance(d, dict) and d.get("once"):
            rid = fp.stem
            all_once.add(rid)
            if rid.startswith(FIT_PREFIXES):
                fit_once.add(rid)
            else:
                mission_once.add(rid)
    res = (all_once, fit_once, mission_once)
    if len(_ONCE_CACHE) > 16:
        _ONCE_CACHE.clear()
    _ONCE_CACHE[key] = (stamp, res)
    return res


def _support_bucket(route, kind, all_once):
    rt = str(route or "").lower()
    kd = str(kind or "").lower()
    if route in all_once:
        return "once_routes"
    if rt.startswith("train-jumps-"):
        return "jump_loops"
    if kd == "census":
        return "intel_census"
    if kd == "mine":
        return "mining"
    if kd == "hunt":
        return "military_hunts"
    if rt.startswith(("sell-", "carry-", "bursar-", "trade-")):
        return "trade_sales"
    if rt.startswith(("craft-", "refine-", "smelt-")):
        return "crafting"
    if rt.startswith(("give-", "store-", "gather-", "haul-", "supply-", "deliver-", "stage-")):
        return "handovers_logistics"
    return "other_recurring"


def compute_pnl(conn, repo_root=REPO_DEFAULT, data_dir=DATA_DEFAULT, fleet_json=None, hours=24, now=None, price_maps=None):
    """Compute GAAP/IFRS Cash-to-Accrual P&L, Matching Principle separation, and Transfer-Priced Division Value-Add."""
    now = float(time.time() if now is None else now)
    hours = max(1, int(hours))
    win_key = "%dh" % hours
    data_p = Path(data_dir)
    all_once, fit_once, mission_once = once_route_ids(repo_root)

    # 1. Load cash window from fleet.json (primary) or stats_money_hour (fallback)
    fj = fleet_json
    if fj is None:
        fp = data_p / "fleet" / "fleet.json"
        if fp.is_file():
            try:
                fj = json.loads(fp.read_text(encoding="utf-8", errors="replace"))
            except (OSError, ValueError):
                fj = None
    w = None
    if isinstance(fj, dict):
        w = (((fj.get("totals") or {}).get("rates") or {}).get("windows") or {}).get(win_key)

    raw_income_h = 0.0
    raw_costs_h = 0.0
    raw_steady_h = 0.0
    rewards_h = 0.0
    bought_once_h = 0.0
    treasury_own_h = None
    purse_h = None
    div_raw_cash = {}
    div_raw_once = {}
    div_purse = {}
    div_fuel_h = {}
    repair_cr_h = 0.0
    win_minutes = 0.0
    cash_source = "fleet.json"
    onetime_span_h = None

    if isinstance(w, dict) and w.get("onetime_span_hours") is not None:
        onetime_span_h = _num(w.get("onetime_span_hours"))
    else:
        ot_p = data_p / "fleet" / "onetime.json"
        if ot_p.is_file():
            try:
                ot_rows = json.loads(ot_p.read_text(encoding="utf-8", errors="replace"))
                if isinstance(ot_rows, list) and ot_rows:
                    ts_vals = [float(r[0]) for r in ot_rows if isinstance(r, list) and len(r) == 4 and isinstance(r[0], (int, float))]
                    if ts_vals:
                        onetime_span_h = round(max(0.0, (now - min(ts_vals)) / 3600.0), 2)
            except (OSError, ValueError):
                pass

    use_smh = False
    if conn is not None and _has_table(conn, "stats_money_hour"):
        if not (isinstance(w, dict) and w):
            use_smh = True
        elif hours >= 6 and onetime_span_h is not None and onetime_span_h > 0.0 and onetime_span_h < hours * 0.85:
            cut_chk = int(now) - hours * 3600
            chk_m = conn.execute(
                "SELECT COALESCE(SUM(minutes), 0) FROM stats_money_hour WHERE LOWER(division) IN ('fleet','all') AND ships > 0 AND hour >= ?",
                (cut_chk,),
            ).fetchone()
            if chk_m and _num(chk_m[0]) >= hours * 60.0 * 0.75:
                use_smh = True
                cash_source = "stats_money_hour (onetime_span=%.1fh)" % onetime_span_h

    if isinstance(w, dict) and w and not use_smh:
        raw_income_h = _num(w.get("income_per_hour"))
        raw_costs_h = _num(w.get("costs_per_hour"))
        repair_cr_h = _num(w.get("repair_cr_per_hour"))
        raw_steady_h = _num(w.get("cph"))
        rewards_h = _num(w.get("rewards_per_hour"))
        bought_once_h = _num(w.get("bought_once_per_hour"))
        win_minutes = _num(w.get("minutes"), hours * 60.0)
        if w.get("treasury_own_per_hour") is not None:
            treasury_own_h = _num(w.get("treasury_own_per_hour"))
        if w.get("purse_per_hour") is not None:
            purse_h = _num(w.get("purse_per_hour"))
        elif w.get("total_per_hour") is not None:
            purse_h = _num(w.get("total_per_hour"))
        fl_ship_counts = {}
        for s in (fj.get("ships") or []) if isinstance(fj, dict) else ():
            if isinstance(s, dict) and s.get("division"):
                sd = str(s["division"])
                fl_ship_counts[sd] = fl_ship_counts.get(sd, 0) + 1
        for d, dv in (w.get("divisions") or {}).items():
            if isinstance(dv, dict):
                cph_d = _num(dv.get("cph"))
                once_d = _num(dv.get("one_time_per_hour"))
                unexp_d = _num(dv.get("unexplained_per_hour"))
                rg_ships = int(_num((dv.get("regroup") or {}).get("ships")))
                div_fuel_h[d] = _num(dv.get("fuel_cr_per_hour"))
                if fl_ship_counts and fl_ship_counts.get(d, 0) == 0 and rg_ships < 0 and abs(unexp_d) > 10000.0:
                    if cph_d < -10000.0 and _num(dv.get("spent_per_hour")) < 5000.0:
                        adj = -cph_d - _num(dv.get("spent_per_hour"))
                        cph_d += adj
                        raw_steady_h += adj
                        raw_costs_h = max(0.0, raw_costs_h - adj)
                div_raw_cash[d] = cph_d
                div_raw_once[d] = once_d
                div_purse[d] = _num(dv.get("total_per_hour"), cph_d + once_d)
    elif conn is not None and _has_table(conn, "stats_money_hour"):
        if cash_source == "fleet.json":
            cash_source = "stats_money_hour"
        cut_m = int(now) - hours * 3600
        smh_cols = {c[1] for c in conn.execute("PRAGMA table_info(stats_money_hour)")}
        has_fuel_col = "fuel" in smh_cols
        has_rep_col = "repair" in smh_cols
        rows_m = conn.execute(
            (
                "SELECT minutes, income, costs, net, rewards, bought, once, total, repair "
                "FROM stats_money_hour WHERE LOWER(division) IN ('fleet','all') AND ships > 0 AND hour >= ?"
            ) if has_rep_col else (
                "SELECT minutes, income, costs, net, rewards, bought, once, total, 0 "
                "FROM stats_money_hour WHERE LOWER(division) IN ('fleet','all') AND ships > 0 AND hour >= ?"
            ),
            (cut_m,),
        ).fetchall()
        tot_m = sum(_num(r[0]) for r in rows_m)
        if tot_m > 0:
            win_minutes = tot_m
            raw_income_h = sum(_num(r[1]) * _num(r[0]) for r in rows_m) / tot_m
            raw_costs_h = sum(_num(r[2]) * _num(r[0]) for r in rows_m) / tot_m
            raw_steady_h = sum(_num(r[3]) * _num(r[0]) for r in rows_m) / tot_m
            rewards_h = sum(_num(r[4]) * _num(r[0]) for r in rows_m) / tot_m
            bought_once_h = sum(_num(r[5]) * _num(r[0]) for r in rows_m) / tot_m
            purse_h = sum(_num(r[7]) * _num(r[0]) for r in rows_m) / tot_m
            repair_cr_h = sum(_num(r[8]) * _num(r[0]) for r in rows_m) / tot_m
            if isinstance(w, dict) and w.get("treasury_own_per_hour") is not None:
                treasury_own_h = _num(w.get("treasury_own_per_hour"))
                purse_h = raw_steady_h + (rewards_h - bought_once_h) + treasury_own_h
        for d in DIVISIONS:
            q_d = (
                "SELECT minutes, net, once, total, fuel FROM stats_money_hour WHERE division = ? AND ships > 0 AND hour >= ?"
                if has_fuel_col else
                "SELECT minutes, net, once, total, 0 FROM stats_money_hour WHERE division = ? AND ships > 0 AND hour >= ?"
            )
            dm = conn.execute(q_d, (d, cut_m)).fetchall()
            dm_m = sum(_num(r[0]) for r in dm)
            if dm_m > 0:
                div_raw_cash[d] = sum(_num(r[1]) * _num(r[0]) for r in dm) / dm_m
                div_raw_once[d] = sum(_num(r[2]) * _num(r[0]) for r in dm) / dm_m
                div_purse[d] = sum(_num(r[3]) * _num(r[0]) for r in dm) / dm_m
                div_fuel_h[d] = sum(_num(r[4]) * _num(r[0]) for r in dm) / dm_m
        # Reconcile fleet sum if Command had 0-ship regroup hours skipped
        if div_raw_cash and abs(sum(div_raw_cash.values()) - raw_steady_h) > 5000.0:
            raw_steady_h = sum(div_raw_cash.values())
            raw_costs_h = max(0.0, raw_income_h - raw_steady_h)
            if treasury_own_h is not None:
                purse_h = raw_steady_h + (rewards_h - bought_once_h) + treasury_own_h
        if isinstance(w, dict):
            for d, dv in (w.get("divisions") or {}).items():
                if isinstance(dv, dict) and not div_fuel_h.get(d):
                    div_fuel_h[d] = _num(dv.get("fuel_cr_per_hour"))

    span_h = max(1.0 / 12.0, (win_minutes / 60.0) if win_minutes >= 5.0 else float(hours))

    # 2. Load pilot -> division map & price maps
    pilot_div = {}
    if conn is not None and _has_table(conn, "ships"):
        for r in conn.execute("SELECT pilot, division FROM ships"):
            if r[0] and r[1]:
                pilot_div[str(r[0])] = str(r[1])
    if price_maps is not None:
        base_map, max_bid_map = price_maps
        bids_by_item = {}
        trend_map = {}
        ask_map = {}
    else:
        base_map, max_bid_map, bids_by_item = _load_price_maps(conn)
        trend_map = _load_market_trends(conn, now=now)
        ask_map = _load_ask_map(conn)

    # 3. Matching Principle: extract direct steady-side credits (fuel/inputs/salvage) on once=true routes
    once_mission_direct_cr = 0.0
    capex_fit_direct_cr = 0.0
    once_direct_by_div = {}
    support_chains = {}
    if conn is not None and _has_table(conn, "runs"):
        cut_r = now - span_h * 3600.0
        for r in conn.execute(
            "SELECT pilot, route, kind, minutes, credits, one_time FROM runs WHERE readable = 1 AND t >= ?",
            (cut_r,),
        ):
            pilot = str(r[0] or "")
            route = str(r[1] or "")
            kind = str(r[2] or "")
            mins = _num(r[3])
            cr = _num(r[4])
            ot = _num(r[5])
            if route in all_once or kind == "fit_net":
                d = _div_of_pilot(pilot, pilot_div)
                once_direct_by_div[d] = once_direct_by_div.get(d, 0.0) + cr
                if route in fit_once or kind == "fit_net":
                    capex_fit_direct_cr += cr
                else:
                    once_mission_direct_cr += cr
            b = _support_bucket(route, kind, all_once)
            rec = support_chains.setdefault(b, {"runs": 0, "ship_hours": 0.0, "credits": 0.0, "one_time": 0.0})
            rec["runs"] += 1
            rec["ship_hours"] += mins / 60.0
            rec["credits"] += cr
            rec["one_time"] += ot

    once_mission_direct_h = once_mission_direct_cr / span_h
    capex_fit_direct_h = capex_fit_direct_cr / span_h
    once_direct_h = once_mission_direct_h + capex_fit_direct_h

    # 4. IAS 2 Inventory / WIP Accrual from stock_hour + Intercompany Transfer Pricing from handover.jsonl
    has_inv_accrual = False
    inv_span_h = float(hours)
    inv_nrv_div = {}
    inv_cat_div = {}
    fleet_item_delta = {}
    tx_out_div = {}
    tx_in_div = {}
    prev_h = max_h = None

    if conn is not None and _has_table(conn, "stock_hour"):
        mx_row = conn.execute("SELECT MAX(hour) FROM stock_hour").fetchone()
        if mx_row and mx_row[0] is not None:
            max_h = int(mx_row[0])
            target_prev = max_h - hours * 3600
            pr_row = conn.execute(
                "SELECT hour FROM stock_hour WHERE hour <= ? ORDER BY hour DESC LIMIT 1",
                (target_prev,),
            ).fetchone()
            if pr_row is None:
                pr_row = conn.execute(
                    "SELECT MIN(hour) FROM stock_hour WHERE hour < ?",
                    (max_h,),
                ).fetchone()
            if pr_row and pr_row[0] is not None and int(pr_row[0]) < max_h:
                prev_h = int(pr_row[0])
                inv_span_h = (max_h - prev_h) / 3600.0
                if inv_span_h >= 1.0:
                    has_inv_accrual = True
                    now_s = {
                        (str(r[0] or "Other"), str(r[1] or "")): int(_num(r[2]))
                        for r in conn.execute("SELECT division, item, units FROM stock_hour WHERE hour = ?", (max_h,))
                    }
                    old_s = {
                        (str(r[0] or "Other"), str(r[1] or "")): int(_num(r[2]))
                        for r in conn.execute("SELECT division, item, units FROM stock_hour WHERE hour = ?", (prev_h,))
                    }
                    now_item_tot = {}
                    for (_d_k, _i_k), _u_v in now_s.items():
                        now_item_tot[_i_k] = now_item_tot.get(_i_k, 0) + _u_v
                    _esc_i, _esc_di, _esc_ts = _load_sell_escrow(data_p, now=now)
                    if _esc_di and _esc_ts > max_h:
                        for (ediv, eit), eq in _esc_di.items():
                            now_s[(ediv, eit)] = now_s.get((ediv, eit), 0) + eq
                            now_item_tot[eit] = now_item_tot.get(eit, 0) + eq
                    old_item_tot = {}
                    for (_d_k, _i_k), _u_v in old_s.items():
                        old_item_tot[_i_k] = old_item_tot.get(_i_k, 0) + _u_v
                    # Reconcile inventory accrual 1:1 with Balance Sheet marginal depth_realizable_value!
                    # Prevents thin top-of-book bids (e.g. 600u water_ice @ 44 cr) from inflating 30,000u glut deltas.
                    marginal_unit_nrv = {}
                    for it in (set(now_item_tot) | set(old_item_tot)):
                        u_now = now_item_tot.get(it, 0)
                        u_old = old_item_tot.get(it, 0)
                        du_tot = u_now - u_old
                        if du_tot != 0:
                            v_now = depth_realizable_value(it, u_now, base_map, bids_by_item, trend_map, ask_map=ask_map)
                            v_old = depth_realizable_value(it, u_old, base_map, bids_by_item, trend_map, ask_map=ask_map)
                            marginal_unit_nrv[it] = (v_now - v_old) / float(du_tot)
                        else:
                            marginal_unit_nrv[it] = live_market_unit_price(it, base_map, bids_by_item, trend_map, held_units=u_now, max_bid_map=max_bid_map, ask_map=ask_map)
                    for (div, it) in (set(now_s) | set(old_s)):
                        du = now_s.get((div, it), 0) - old_s.get((div, it), 0)
                        if du == 0:
                            continue
                        fleet_item_delta[it] = fleet_item_delta.get(it, 0) + du
                        up = marginal_unit_nrv.get(it, 0.0)
                        inv_nrv_div[div] = inv_nrv_div.get(div, 0.0) + du * up
                        inv_cat_div[div] = inv_cat_div.get(div, 0.0) + du * base_map.get(it, 0.0)

    # Intercompany handovers over exact same [prev_h, max_h] window (or [now - hours*3600, now] if no stock_hour)
    ho_lo = prev_h if prev_h is not None else (now - hours * 3600.0)
    ho_hi = max_h if max_h is not None else now
    ho_span_h = max(1.0, (ho_hi - ho_lo) / 3600.0)
    ho_path = data_p / "stock" / "handover.jsonl"
    if ho_path.is_file():
        try:
            with open(ho_path, encoding="utf-8", errors="replace") as fh:
                for line in fh:
                    try:
                        r = json.loads(line)
                    except ValueError:
                        continue
                    ts = _num(r.get("at") or r.get("t"))
                    if not (ho_lo < ts <= ho_hi):
                        continue
                    gd = _div_of_pilot(r.get("from"), pilot_div)
                    td = _div_of_pilot(r.get("to"), pilot_div)
                    if gd == td:
                        continue
                    for it, u in (r.get("items") or {}).items():
                        _hi = str(it)
                        _hu = now_item_tot.get(_hi, 0) if "now_item_tot" in locals() else 0
                        v = _num(u) * live_market_unit_price(_hi, base_map, bids_by_item, trend_map, held_units=_hu, max_bid_map=max_bid_map, ask_map=ask_map)
                        if v > 0:
                            tx_out_div[gd] = tx_out_div.get(gd, 0.0) + v
                            tx_in_div[td] = tx_in_div.get(td, 0.0) + v
        except OSError:
            pass

    # 5. Reconciled Fleet 3-Statement Figures (all per hour)
    inv_accrual_h = (sum(inv_nrv_div.values()) / inv_span_h) if has_inv_accrual else 0.0
    inv_accrual_cat_h = (sum(inv_cat_div.values()) / inv_span_h) if has_inv_accrual else 0.0
    recurring_cash_h = raw_steady_h - once_direct_h
    accrual_operating_h = recurring_cash_h + inv_accrual_h
    seed_net_h = rewards_h + once_mission_direct_h
    capex_net_h = -bought_once_h + capex_fit_direct_h
    if purse_h is None:
        purse_h = raw_steady_h + rewards_h - bought_once_h + (treasury_own_h or 0.0)

    # Top inventory build drivers (IAS 2 LCNRV)
    top_builds = []
    if has_inv_accrual:
        ranked = sorted(
            (
                (du * live_market_unit_price(it, base_map, bids_by_item, trend_map, held_units=(now_item_tot.get(it, 0) if (du > 0 and "now_item_tot" in locals()) else 0), max_bid_map=max_bid_map, ask_map=ask_map), it, du)
                for it, du in fleet_item_delta.items()
                if du != 0
            ),
            key=lambda x: -x[0],
        )
        for val, it, du in ranked[:5]:
            if val > 0:
                top_builds.append({
                    "item": it,
                    "units": int(du),
                    "value": int(round(val)),
                    "per_hour": int(round(val / inv_span_h)),
                })

    # 6. Per-Division Transfer-Priced P&L (sum across divisions + Faction reconciles to Fleet!)
    by_division = {}
    for d in ALL_ACC_DIVS:
        rc = div_raw_cash.get(d, 0.0)
        ro = div_raw_once.get(d, 0.0)
        od = once_direct_by_div.get(d, 0.0) / span_h
        mc = rc - od
        on = ro + od
        ph = div_purse.get(d, rc + ro)
        iv = (inv_nrv_div.get(d, 0.0) / inv_span_h) if has_inv_accrual else 0.0
        xo = tx_out_div.get(d, 0.0) / ho_span_h
        xi = tx_in_div.get(d, 0.0) / ho_span_h
        fh = div_fuel_h.get(d, 0.0)
        acc_d = mc + iv + xo - xi
        fuel_roi = round((acc_d + fh) / fh, 2) if fh > 100.0 else None
        by_division[d] = {
            "raw_cash_h": int(round(rc)),
            "raw_once_h": int(round(ro)),
            "once_direct_h": int(round(od)),
            "once_net_h": int(round(on)),
            "recurring_cash_h": int(round(mc)),
            "purse_h": int(round(ph)),
            "inv_accrual_h": int(round(iv)),
            "tx_out_h": int(round(xo)),
            "tx_in_h": int(round(xi)),
            "net_transfer_h": int(round(xo - xi)),
            "accrual_op_h": int(round(acc_d)),
            "fuel_cr_h": int(round(fh)),
            "fuel_roi": fuel_roi,
        }

    # Format support chain summary (per hour over span_h)
    support_out = {}
    for b, rec in sorted(support_chains.items()):
        support_out[b] = {
            "runs": rec["runs"],
            "ship_hours": round(rec["ship_hours"], 1),
            "credits": int(round(rec["credits"])),
            "credits_per_hour": int(round(rec["credits"] / span_h)),
            "one_time": int(round(rec["one_time"])),
        }

    # Exact non-overlapping OpEx subsections reconciling to raw_costs_h & matched_direct_h (zero plugs)
    fuel_opex_h = max(0.0, sum(div_fuel_h.values()))
    if fuel_opex_h <= 0.0 and isinstance(w, dict):
        fuel_opex_h = max(0.0, _num(w.get("fuel_cr_per_hour")))
    repair_opex_h = max(0.0, repair_cr_h)
    if repair_opex_h <= 0.0 and isinstance(w, dict):
        repair_opex_h = max(0.0, _num(w.get("repair_cr_per_hour")))
    craft_raw_h = max(0.0, -_num((support_out.get("crafting") or {}).get("credits_per_hour")))
    rem_after_fr = max(0.0, raw_costs_h - fuel_opex_h - repair_opex_h)
    craft_opex_h = min(craft_raw_h, rem_after_fr)
    other_cogs_h = raw_costs_h - fuel_opex_h - repair_opex_h - craft_opex_h
    reclass_once_h = -once_direct_h
    matched_direct_h = raw_costs_h + once_direct_h
    opex_breakdown = {
        "fuel_h": int(round(fuel_opex_h)),
        "repair_h": int(round(repair_opex_h)),
        "craft_inputs_h": int(round(craft_opex_h)),
        "other_cogs_h": int(round(other_cogs_h)),
        "gross_direct_h": int(round(raw_costs_h)),
        "reclassified_once_h": int(round(reclass_once_h)),
        "matched_direct_h": int(round(matched_direct_h)),
    }

    return {
        "hours": hours,
        "cash_source": cash_source,
        "onetime_span_hours": onetime_span_h,
        "span_hours": round(span_h, 2),
        "inv_span_hours": round(inv_span_h, 2) if has_inv_accrual else 0.0,
        "has_inventory_accrual": has_inv_accrual,
        "raw_income_h": int(round(raw_income_h)),
        "raw_costs_h": int(round(raw_costs_h)),
        "raw_steady_h": int(round(raw_steady_h)),
        "once_direct_h": int(round(once_direct_h)),
        "once_mission_direct_h": int(round(once_mission_direct_h)),
        "capex_fit_direct_h": int(round(capex_fit_direct_h)),
        "recurring_cash_h": int(round(recurring_cash_h)),
        "inventory_accrual_h": int(round(inv_accrual_h)),
        "inventory_accrual_catalog_h": int(round(inv_accrual_cat_h)),
        "accrual_operating_h": int(round(accrual_operating_h)),
        "seed_rewards_h": int(round(rewards_h)),
        "seed_net_h": int(round(seed_net_h)),
        "capex_gross_h": int(round(-bought_once_h)),
        "capex_net_h": int(round(capex_net_h)),
        "treasury_own_h": int(round(treasury_own_h)) if treasury_own_h is not None else None,
        "purse_h": int(round(purse_h)),
        "repair_cr_h": int(round(repair_opex_h)),
        "opex_breakdown": opex_breakdown,
        "by_division": by_division,
        "top_inv_builds": top_builds,
        "support_chains": support_out,
    }


def ship_pnl_24h(conn, pilot, repo_root=REPO_DEFAULT, data_dir=DATA_DEFAULT, now=None):
    """Compute GAAP/IFRS-aligned 24h KPIs for one individual ship (matching principle + IAS 2 handovers)."""
    now = float(time.time() if now is None else now)
    cut = now - 86400.0
    all_once, fit_once, _mission_once = once_route_ids(repo_root)
    base_map, max_bid_map, _bids = _load_price_maps(conn)

    runs_n = 0
    mins_tot = 0.0
    raw_cr = 0.0
    raw_ot = 0.0
    rec_cr = 0.0
    once_direct = 0.0
    seed_matched = 0.0
    capex_matched = 0.0

    if conn is not None and _has_table(conn, "runs"):
        for r in conn.execute(
            "SELECT route, COALESCE(minutes, 0), COALESCE(credits, 0), COALESCE(one_time, 0), COALESCE(readable, 1) "
            "FROM runs WHERE pilot = ? AND t >= ?",
            (pilot, cut),
        ):
            runs_n += 1
            rt = str(r[0] or "")
            mins = _num(r[1])
            cr = _num(r[2])
            ot = _num(r[3])
            rd = int(_num(r[4], 1))
            mins_tot += mins
            raw_ot += ot
            if rd:
                raw_cr += cr
            if rt in all_once:
                if rd:
                    once_direct += cr
                matched = (cr if rd else 0.0) + ot
                if rt in fit_once:
                    capex_matched += matched
                else:
                    seed_matched += matched
            else:
                if rd:
                    rec_cr += cr
                if ot < 0:
                    capex_matched += ot
                elif ot > 0:
                    seed_matched += ot

    ho_out = 0.0
    ho_in = 0.0
    ho_path = Path(data_dir) / "stock" / "handover.jsonl"
    if ho_path.is_file():
        try:
            with open(ho_path, encoding="utf-8", errors="replace") as fh:
                for line in fh:
                    try:
                        row = json.loads(line)
                    except ValueError:
                        continue
                    if _num(row.get("at") or row.get("t")) < cut:
                        continue
                    frm = str(row.get("from") or "")
                    to = str(row.get("to") or "")
                    if frm != pilot and to != pilot:
                        continue
                    for it, u in (row.get("items") or {}).items():
                        v = _num(u) * lcnrv_unit_price(str(it), base_map, max_bid_map)
                        if v > 0:
                            if frm == pilot:
                                ho_out += v
                            if to == pilot:
                                ho_in += v
        except OSError:
            pass

    rec_i = int(round(rec_cr))
    seed_i = int(round(seed_matched))
    capex_i = int(round(capex_matched))
    ho_out_i = int(round(ho_out))
    ho_in_i = int(round(ho_in))
    return {
        "runs": runs_n,
        "minutes": round(mins_tot, 1),
        "credits": int(round(raw_cr)),
        "one_time": int(round(raw_ot)),
        "recurring_cash": rec_i,
        "once_direct": int(round(once_direct)),
        "seed_matched": seed_i,
        "capex_matched": capex_i,
        "handovers_out_nrv": ho_out_i,
        "handovers_in_nrv": ho_in_i,
        "net_handovers_nrv": ho_out_i - ho_in_i,
        "accrual_value_add": rec_i + ho_out_i - ho_in_i,
        "total_wallet": rec_i + seed_i + capex_i,
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description="GAAP/IFRS vault valuation and Cash-to-Accrual P&L report.")
    ap.add_argument("--data", default=os.environ.get("COLLECTIVE_DATA", DATA_DEFAULT))
    ap.add_argument("--root", default=REPO_DEFAULT)
    ap.add_argument("--hours", type=int, default=24)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    db = Path(args.data) / "store" / "read.db"
    conn = sqlite3.connect("file:%s?mode=ro" % db, uri=True, timeout=2.0) if db.is_file() else None
    try:
        out = {
            "vault": vault_valuation(conn),
            "pnl": compute_pnl(conn, repo_root=args.root, data_dir=args.data, hours=args.hours),
        }
    finally:
        if conn is not None:
            conn.close()
    if args.json:
        print(json.dumps(out, indent=2))
    else:
        v, p = out["vault"], out["pnl"]
        print("VAULT | IAS2 NRV %s cr | Catalog %s cr | Instant Bid Depth %s cr | Unbounded Bid %s cr"
              % (format(v["nrv"], ","), format(v["catalog"], ","), format(v["liquid"], ","), format(v["unbounded_bid"], ",")))
        print("P&L (%dh) | Raw Steady %+d/h | Once Fuel %+d/h -> Recurring Cash %+d/h | Inv Accrual %+d/h -> Accrual Op %+d/h"
              % (p["hours"], p["raw_steady_h"], -p["once_direct_h"], p["recurring_cash_h"], p["inventory_accrual_h"], p["accrual_operating_h"]))
        print("CASHFLOW  | Seed Net (matched) %+d/h | CapEx %+d/h | Treasury Own %s | Purse %+d/h"
              % (p["seed_net_h"], p["capex_net_h"], "%+d/h" % p["treasury_own_h"] if p["treasury_own_h"] is not None else "n/a", p["purse_h"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())

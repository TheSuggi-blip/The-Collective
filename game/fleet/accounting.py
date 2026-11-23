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


def lcnrv_unit_price(item, base_map, max_bid_map):
    """IAS 2 / ASC 330 conservative unit price: min(base_value, best_bid) when both exist."""
    b = base_map.get(item, 0.0)
    m = max_bid_map.get(item)
    if m is not None and m > 0:
        return min(b, m) if b > 0 else m
    return b


def vault_valuation(conn):
    """Compute vault valuation under IAS 2 NRV, Catalog Base Value, Depth-Capped Liquidation, and Unbounded Bid."""
    empty = {
        "nrv": 0,
        "catalog": 0,
        "liquid": 0,
        "unbounded_bid": 0,
        "items": 0,
        "units": 0,
        "top_gaps": [],
    }
    if conn is None or not _has_table(conn, "holdings"):
        return empty
    base_map, max_bid_map, bids_by_item = _load_price_maps(conn)
    rows = conn.execute(
        "SELECT item, SUM(COALESCE(units, 0)) FROM holdings GROUP BY item"
    ).fetchall()
    tot_nrv = 0.0
    tot_cat = 0.0
    tot_liq = 0.0
    tot_unb = 0.0
    tot_units = 0
    item_cnt = 0
    gaps = []
    for r in rows:
        it = str(r[0] or "")
        u = int(_num(r[1]))
        if not it or u <= 0:
            continue
        item_cnt += 1
        tot_units += u
        bv = base_map.get(it, 0.0)
        mb = max_bid_map.get(it)
        cat_v = u * bv
        nrv_v = u * lcnrv_unit_price(it, base_map, max_bid_map)
        unb_v = u * (mb if (mb is not None and mb > 0) else bv)
        rem = float(u)
        liq_v = 0.0
        for price, qty in bids_by_item.get(it, ()):
            take = min(rem, qty)
            liq_v += take * price
            rem -= take
            if rem <= 0:
                break
        tot_nrv += nrv_v
        tot_cat += cat_v
        tot_liq += liq_v
        tot_unb += unb_v
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
                    "catalog": int(round(cat_v)),
                    "liquid": int(round(liq_v)),
                    "unbounded_bid": int(round(unb_v)),
                },
            ))
    gaps.sort(key=lambda x: -x[0])
    return {
        "nrv": int(round(tot_nrv)),
        "catalog": int(round(tot_cat)),
        "liquid": int(round(tot_liq)),
        "unbounded_bid": int(round(tot_unb)),
        "items": item_cnt,
        "units": tot_units,
        "top_gaps": [g[1] for g in gaps[:5]],
    }


def once_route_ids(repo_root):
    """Return (all_once, fit_once, mission_once) route ID sets scanning ALL game/routes/*.json."""
    all_once, fit_once, mission_once = set(), set(), set()
    rdir = Path(repo_root) / "game" / "routes"
    if not rdir.is_dir():
        return all_once, fit_once, mission_once
    for p in rdir.glob("*.json"):
        try:
            d = json.loads(p.read_text(encoding="utf-8", errors="replace"))
        except (OSError, ValueError):
            continue
        if isinstance(d, dict) and d.get("once"):
            rid = p.stem
            all_once.add(rid)
            if rid.startswith(FIT_PREFIXES):
                fit_once.add(rid)
            else:
                mission_once.add(rid)
    return all_once, fit_once, mission_once


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


def compute_pnl(conn, repo_root=REPO_DEFAULT, data_dir=DATA_DEFAULT, fleet_json=None, hours=24, now=None):
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
    win_minutes = 0.0

    if isinstance(w, dict) and w:
        raw_income_h = _num(w.get("income_per_hour"))
        raw_costs_h = _num(w.get("costs_per_hour"))
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
        for d, dv in (w.get("divisions") or {}).items():
            if isinstance(dv, dict):
                div_raw_cash[d] = _num(dv.get("cph"))
    elif conn is not None and _has_table(conn, "stats_money_hour"):
        cut_m = int(now) - hours * 3600
        rows_m = conn.execute(
            "SELECT minutes, income, costs, net, rewards, bought, once, total "
            "FROM stats_money_hour WHERE LOWER(division) IN ('fleet','all') AND ships > 0 AND hour >= ?",
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
        for d in DIVISIONS:
            dm = conn.execute(
                "SELECT minutes, net FROM stats_money_hour WHERE division = ? AND ships > 0 AND hour >= ?",
                (d, cut_m),
            ).fetchall()
            dm_m = sum(_num(r[0]) for r in dm)
            if dm_m > 0:
                div_raw_cash[d] = sum(_num(r[1]) * _num(r[0]) for r in dm) / dm_m

    span_h = max(1.0 / 12.0, (win_minutes / 60.0) if win_minutes >= 5.0 else float(hours))

    # 2. Load pilot -> division map & price maps
    pilot_div = {}
    if conn is not None and _has_table(conn, "ships"):
        for r in conn.execute("SELECT pilot, division FROM ships"):
            if r[0] and r[1]:
                pilot_div[str(r[0])] = str(r[1])
    base_map, max_bid_map, _bids = _load_price_maps(conn)

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
            if route in all_once:
                d = _div_of_pilot(pilot, pilot_div)
                once_direct_by_div[d] = once_direct_by_div.get(d, 0.0) + cr
                if route in fit_once:
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
                    for (div, it) in (set(now_s) | set(old_s)):
                        du = now_s.get((div, it), 0) - old_s.get((div, it), 0)
                        if du == 0:
                            continue
                        fleet_item_delta[it] = fleet_item_delta.get(it, 0) + du
                        inv_nrv_div[div] = inv_nrv_div.get(div, 0.0) + du * lcnrv_unit_price(it, base_map, max_bid_map)
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
                        v = _num(u) * lcnrv_unit_price(str(it), base_map, max_bid_map)
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
                (du * lcnrv_unit_price(it, base_map, max_bid_map), it, du)
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
        od = once_direct_by_div.get(d, 0.0) / span_h
        mc = rc - od
        iv = (inv_nrv_div.get(d, 0.0) / inv_span_h) if has_inv_accrual else 0.0
        xo = tx_out_div.get(d, 0.0) / ho_span_h
        xi = tx_in_div.get(d, 0.0) / ho_span_h
        by_division[d] = {
            "raw_cash_h": int(round(rc)),
            "once_direct_h": int(round(od)),
            "recurring_cash_h": int(round(mc)),
            "inv_accrual_h": int(round(iv)),
            "tx_out_h": int(round(xo)),
            "tx_in_h": int(round(xi)),
            "net_transfer_h": int(round(xo - xi)),
            "accrual_op_h": int(round(mc + iv + xo - xi)),
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

    return {
        "hours": hours,
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
        "by_division": by_division,
        "top_inv_builds": top_builds,
        "support_chains": support_out,
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

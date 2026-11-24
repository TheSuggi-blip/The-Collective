#!/usr/bin/env python3
"""bursar.py -- dynamic multi-station Station Bursar runner for Trade division.

WHAT: policy-driven runner (`game/bursar-policy.json`, owned & tunable by Mercury/Unity).
      Each Trade ship that runs `bursar.py`:
        1. Atomically claims 1 unstaffed policed Exchange station in data/fleet/bursar_claims.json
           (capped at policy.max_per_station, default 1; prefers current docked station at 0 fuel,
           then pilot's birth empire, ordered by market depth and staleness).
        2. Travels safely and docks (`prepare-at-station` with refuel).
        3. Runs a zero-fuel Station Bursar watch loop for `--minutes` (default 30):
           - Refreshes live `data/market/<base>.json` and `data/missions/<base>.json` for free.
           - Liquidates unreserved local surplus (hits strong bids immediately or posts/reprices
             resting `sell_order` undercutting competing asks above floor; never sells reserved mats).
           - Places/maintains wholesale `buy_order` procurement walls for open `needs.tsv`
             bottlenecks within Mercury's escrow & unit-price ceiling policy.
           - With the buy lane off (`buy.enabled` false, `buy.unwind_when_off` true, the default) it
             unwinds instead: cancels its own open buy orders where it docks (escrow back to the wallet;
             the game cancels only docked at the order's station) and claims a station where it still
             holds buy orders first, past the one-a-station cap, without taking another pilot's claim.
        4. Releases its claim cleanly (staying docked so the next cycle re-claims the same station
           at 0 fuel) and records one row in data/routes/runs.jsonl.

USAGE:
  bursar.py <pilot> [--minutes 30] [--route bursar-network] [--policy game/bursar-policy.json]
            [--station system:poi:base]

Stdlib only. ASCII only.
"""
import atexit
import fcntl
import json
import math
import os
import re
import sqlite3
import sys
import threading
import time
import urllib.parse
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import division
import fuelplan
import gate

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
DATA = Path(os.environ.get("FLEET_DATA_ROOT") or "/srv/collective/data")
TICK = 11
PROTECTED_ITEMS = frozenset(("fuel_cell", "antimatter_containment_cell", "repair_kit", "hull_patch"))

DEFAULT_POLICY = {
    "max_per_station": 1,
    "policed_only": True,
    "stay_in_empire_first": True,
    "cycle_minutes": 30,
    "poll_interval_s": 120,
    "min_cash_keep": 20000,
    "buy": {
        "enabled": True,
        "max_escrow_per_station": 0,
        "max_orders_per_station": 4,
        "max_units_per_order": 200,
        "max_unit_price_ratio": 0.90,
        "outbid_cr": 1,
        "use_needs_tsv": True,
        "extra_items": [],
        "unwind_when_off": True,
    },
    "sell": {
        "enabled": True,
        "max_orders_per_station": 8,
        "undercut_cr": 1,
        "min_price_ratio": 0.75,
        "instant_hit_bid_ratio": 0.85,
        "respect_reserve": True,
    },
    "exclude_stations": [],
    "priority_stations": [],
}


def utc_now():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def read_json(path, default):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name("%s.%d.%d.tmp" % (path.name, os.getpid(), threading.get_ident()))
    tmp.write_text(json.dumps(value, indent=1), encoding="utf-8")
    os.replace(tmp, path)


def _call_json(method, path, payload=None, timeout=120):
    st, txt = gate.call(method, path, payload, timeout=timeout)
    if isinstance(txt, (dict, list)):
        return st, txt
    try:
        return st, json.loads(txt or "{}")
    except (TypeError, ValueError):
        return st, {"error": str(txt)[:200]}


def load_policy(policy_path=None):
    merged = json.loads(json.dumps(DEFAULT_POLICY))
    path = Path(policy_path) if policy_path else (ROOT / "bursar-policy.json")
    if not path.is_absolute():
        path = REPO / path
    raw = read_json(path, {})
    if isinstance(raw, dict):
        for k, v in raw.items():
            if isinstance(v, dict) and isinstance(merged.get(k), dict):
                merged[k].update(v)
            else:
                merged[k] = v
    return merged


def ship_file_name(pilot):
    return (re.sub(r"[^A-Za-z0-9_.-]", "_", str(pilot))[:60] or "pilot") + ".json"


def _fresh_orders(data, now_t=None):
    now_t = time.time() if now_t is None else now_t
    out = {}
    odir = Path(data) / "fleet" / "orders"
    if not odir.is_dir():
        return out
    for p in odir.glob("*.json"):
        try:
            if now_t - p.stat().st_mtime > 1200:
                continue
            d = json.loads(p.read_text(encoding="utf-8"))
            if isinstance(d, dict) and d.get("pilot") and d.get("what"):
                out[str(d["pilot"])] = str(d["what"])
        except (OSError, ValueError):
            continue
    return out


def _static_bursar_bases(repo_root, orders):
    counts = {}
    rdir = Path(repo_root) / "game" / "routes"
    if not rdir.is_dir():
        return counts
    cache = {}
    for _pilot, what in orders.items():
        if not isinstance(what, str) or not what.startswith("circuit "):
            continue
        rid = what.split(" ", 1)[1]
        if rid not in cache:
            base = ""
            rd = read_json(rdir / (rid + ".json"), None)
            if isinstance(rd, dict):
                stops = rd.get("stops") or []
                has_ord = any(isinstance(s, dict) and ("sell_order" in s or "buy_order" in s) for s in stops)
                req = rd.get("requires") if isinstance(rd.get("requires"), dict) else {}
                is_desk = bool(req.get("docked_at")) or any(isinstance(s, dict) and s.get("watch_minutes") for s in stops) or ("bursar" in rid)
                if has_ord and is_desk:
                    at0 = str(stops[0].get("at") or "") if stops and isinstance(stops[0], dict) else ""
                    base = at0.split(":")[-1] if ":" in at0 else str(req.get("docked_at") or "")
            cache[rid] = base
        if cache[rid]:
            counts[cache[rid]] = counts.get(cache[rid], 0) + 1
    return counts


def load_exchange_stations(data, policed_only=True, exclude_strongholds=True):
    db = Path(data) / "store" / "read.db"
    stations = []
    if db.is_file():
        con = None
        try:
            con = sqlite3.connect("file:%s?mode=ro" % db, uri=True, timeout=3.0)
            con.row_factory = sqlite3.Row
            tbls = {r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()}
            if {"places", "systems"} <= tbls:
                scols = {r[1] for r in con.execute("PRAGMA table_info(systems)").fetchall()}
                strg_expr = "COALESCE(s.stronghold, 0)" if "stronghold" in scols else "0"
                if "books" in tbls:
                    rows = con.execute(f"""
                        SELECT p.base, p.system, p.poi, COALESCE(s.empire, '') AS empire,
                               {strg_expr} AS stronghold,
                               COALESCE(SUM(COALESCE(b.bid,0)*COALESCE(b.bid_qty,0) + COALESCE(b.ask,0)*COALESCE(b.ask_qty,0)), 0) AS depth,
                               MAX(COALESCE(b.t, 0)) AS book_t,
                               COUNT(b.item) AS items_n
                        FROM places p
                        LEFT JOIN systems s ON s.id = p.system
                        LEFT JOIN books b ON b.base = p.base
                        WHERE COALESCE(p.base, '') != ''
                        GROUP BY p.base, p.system, p.poi, s.empire
                    """).fetchall()
                else:
                    rows = con.execute(f"""
                        SELECT p.base, p.system, p.poi, COALESCE(s.empire, '') AS empire,
                               {strg_expr} AS stronghold,
                               0 AS depth, 0 AS book_t, 0 AS items_n
                        FROM places p
                        LEFT JOIN systems s ON s.id = p.system
                        WHERE COALESCE(p.base, '') != ''
                    """).fetchall()
                seen = set()
                for r in rows:
                    b = str(r["base"] or "")
                    if not b or b in seen:
                        continue
                    emp = str(r["empire"] or "").strip().lower()
                    if exclude_strongholds and int(r["stronghold"] or 0):
                        continue
                    if policed_only and not emp:
                        continue
                    # When covering neutral non-stronghold hubs too, only staff stations that actually have an Exchange book
                    if not emp and int(r["items_n"] or 0) <= 0:
                        continue
                    seen.add(b)
                    stations.append({
                        "base": b, "system": str(r["system"] or ""), "poi": str(r["poi"] or ""),
                        "empire": emp, "depth": float(r["depth"] or 0.0),
                        "book_t": float(r["book_t"] or 0.0), "items_n": int(r["items_n"] or 0),
                    })
        except sqlite3.Error:
            pass
        finally:
            if con is not None:
                con.close()
    return stations


def _bfs_hops(lanes, src, dst):
    if not src or not dst:
        return None
    if src == dst:
        return 0
    seen = {src: 0}
    q = [src]
    while q:
        cur = q.pop(0)
        d = seen[cur]
        if d >= 60:
            continue
        for nxt in lanes.get(cur) or []:
            if nxt == dst:
                return d + 1
            if nxt not in seen:
                seen[nxt] = d + 1
                q.append(nxt)
    return None


ORDER_HINT = re.compile(r"(\d+) buy orders? and \d+ sell orders? on the market at (.+?) \(")


def order_stations(text):
    """(buy orders, stations) from the hint of view_orders: '2 buy orders and 1 sell order on the market at a, b (...)'."""
    m = ORDER_HINT.search(str(text or ""))
    if not m:
        return 0, []
    return int(m.group(1)), [s.strip() for s in m.group(2).split(",") if s.strip()]


def claim_station(data, repo_root, pilot, pilot_info, policy, explicit_station=None, now_t=None, unwind_bases=None):
    now_t = time.time() if now_t is None else now_t
    fdir = Path(data) / "fleet"
    fdir.mkdir(parents=True, exist_ok=True)
    lock_path = fdir / "bursar_claims.lock"
    claims_path = fdir / "bursar_claims.json"
    max_per = max(1, int(policy.get("max_per_station") or 1))
    ttl = max(1800, int(float(policy.get("cycle_minutes") or 30) * 60 * 2.5))
    exclude = set(str(x) for x in (policy.get("exclude_stations") or []))
    priority = set(str(x) for x in (policy.get("priority_stations") or []))

    with open(lock_path, "a+", encoding="utf-8") as lf:
        fcntl.flock(lf, fcntl.LOCK_EX)
        try:
            claims = read_json(claims_path, {})
            if not isinstance(claims, dict):
                claims = {}
            orders = _fresh_orders(data, now_t)
            static_counts = _static_bursar_bases(repo_root, orders)
            cleaned = {}
            for b_id, rec in claims.items():
                if not isinstance(rec, dict):
                    continue
                holder = str(rec.get("pilot") or "")
                at = float(rec.get("claimed_at") or 0)
                if not holder or holder == pilot or now_t - at > ttl:
                    continue
                if str(orders.get(holder) or "").startswith("bursar ") or (now_t - at) < 90:
                    cleaned[str(b_id)] = rec

            if explicit_station:
                parts = str(explicit_station).split(":")
                if len(parts) == 3:
                    sys_id, poi_id, base_id = parts
                    used = (1 if base_id in cleaned else 0) + static_counts.get(base_id, 0)
                    if used < max_per:
                        rec = {"pilot": pilot, "system": sys_id, "poi": poi_id, "base": base_id, "claimed_at": int(now_t)}
                        cleaned[base_id] = rec
                        write_json(claims_path, cleaned)
                        return rec
                write_json(claims_path, cleaned)
                return None

            stations = load_exchange_stations(data, policed_only=bool(policy.get("policed_only", True)))
            if not stations:
                write_json(claims_path, cleaned)
                return None
            try:
                lanes = fuelplan.chart(Path(repo_root) / "game")[0]
            except Exception:
                lanes = {}

            cur_sys = str((pilot_info or {}).get("system") or "")
            cur_base = str((pilot_info or {}).get("base") or (pilot_info or {}).get("docked") or "")
            p_emp = str((pilot_info or {}).get("empire") or "").strip().lower()
            stay_emp = bool(policy.get("stay_in_empire_first", True))

            unwind = set(str(x) for x in (unwind_bases or ()))
            best = None
            for st in stations:
                b_id = st["base"]
                if b_id in exclude:
                    continue
                used = (1 if b_id in cleaned else 0) + static_counts.get(b_id, 0)
                if used >= max_per and b_id not in unwind:
                    continue
                hops = _bfs_hops(lanes, cur_sys, st["system"]) if cur_sys else 0
                if cur_sys and lanes and hops is None:
                    continue
                hops = 0 if hops is None else hops
                score = 0.0
                if b_id in unwind:
                    score += 200000.0
                if cur_base and b_id == cur_base:
                    score += 100000.0
                if b_id in priority:
                    score += 5000.0
                if st["empire"]:
                    score += 10000.0
                if stay_emp and p_emp and st["empire"] == p_emp:
                    score += 2000.0
                if st["items_n"] > 0:
                    score += 500.0
                score += math.log10(1.0 + max(0.0, st["depth"])) * 100.0
                score += min(400.0, max(0.0, (now_t - st["book_t"]) / 60.0) * 2.0) if st["book_t"] > 0 else 300.0
                score -= hops * 40.0
                if best is None or score > best[0]:
                    best = (score, st)

            if best is None:
                write_json(claims_path, cleaned)
                return None
            chosen = dict(best[1])
            rec = {"pilot": pilot, "system": chosen["system"], "poi": chosen["poi"], "base": chosen["base"],
                   "empire": chosen.get("empire") or "", "claimed_at": int(now_t)}
            if chosen["base"] in unwind:
                rec["unwind"] = True
                if chosen["base"] in cleaned or static_counts.get(chosen["base"], 0):
                    write_json(claims_path, cleaned)
                    return rec
            cleaned[chosen["base"]] = rec
            write_json(claims_path, cleaned)
            return rec
        finally:
            fcntl.flock(lf, fcntl.LOCK_UN)


def release_claim(data, pilot):
    fdir = Path(data) / "fleet"
    lock_path = fdir / "bursar_claims.lock"
    claims_path = fdir / "bursar_claims.json"
    if not claims_path.is_file():
        return
    with open(lock_path, "a+", encoding="utf-8") as lf:
        fcntl.flock(lf, fcntl.LOCK_EX)
        try:
            claims = read_json(claims_path, {})
            if isinstance(claims, dict):
                changed = False
                for b_id in [k for k, v in claims.items() if isinstance(v, dict) and v.get("pilot") == pilot]:
                    claims.pop(b_id, None)
                    changed = True
                if changed:
                    write_json(claims_path, claims)
        finally:
            fcntl.flock(lf, fcntl.LOCK_UN)


def load_needs_and_reserves(repo_root, data):
    open_needs, reserved, catalog_vals = {}, set(PROTECTED_ITEMS), {}
    db = Path(data) / "store" / "read.db"
    if db.is_file():
        con = None
        try:
            con = sqlite3.connect("file:%s?mode=ro" % db, uri=True, timeout=3.0)
            tbls = {r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type IN ('table','view')").fetchall()}
            if "contract_candidates" in tbls:
                for (short_s,) in con.execute("SELECT short_items FROM contract_candidates WHERE short_items IS NOT NULL").fetchall():
                    for part in str(short_s).split(","):
                        m = re.match(r"\s*([a-z0-9_]+)\s+([\d,]+)", part.strip())
                        if m:
                            iid, qty = m.group(1), int(m.group(2).replace(",", ""))
                            if qty > 0:
                                open_needs[iid] = open_needs.get(iid, 0) + qty
                                reserved.add(iid)
            if "items" in tbls:
                cols = {r[1] for r in con.execute("PRAGMA table_info(items)").fetchall()}
                vcol = "base_value" if "base_value" in cols else ("value" if "value" in cols else "")
                if vcol:
                    for iid, val in con.execute("SELECT id, COALESCE(%s, 0) FROM items" % vcol).fetchall():
                        if iid and val:
                            catalog_vals[str(iid)] = float(val)
        except sqlite3.Error:
            pass
        finally:
            if con is not None:
                con.close()
    res_tsv = Path(repo_root) / "game" / "reserve.tsv"
    if res_tsv.is_file():
        try:
            for ln in res_tsv.read_text(encoding="ascii", errors="replace").splitlines()[1:]:
                cols = ln.split("\t")
                if len(cols) >= 2 and cols[0].strip() and not cols[0].startswith("#"):
                    reserved.add(cols[0].strip())
        except OSError:
            pass
    return open_needs, reserved, catalog_vals


def sync_fleet_buys(data, pilot, base_id, own_orders, ttl_s=21600, now_t=None):
    """Record pilot open buy units at base_id in data/fleet/bursar_buys.json; return {item: qty_by_others}."""
    now_t = time.time() if now_t is None else float(now_t)
    fdir = Path(data) / "fleet"
    fdir.mkdir(parents=True, exist_ok=True)
    lock_path = fdir / "bursar_buys.lock"
    ledger_path = fdir / "bursar_buys.json"
    my_items = {}
    for o in own_orders or []:
        if isinstance(o, dict) and str(o.get("side") or o.get("order_type") or "").lower() == "buy":
            rem = int(o.get("remaining") or o.get("quantity") or 0)
            iid = str(o.get("item_id") or "")
            if iid and rem > 0:
                my_items[iid] = my_items.get(iid, 0) + rem
    others = {}
    with open(lock_path, "a+", encoding="utf-8") as lf:
        fcntl.flock(lf, fcntl.LOCK_EX)
        try:
            doc = read_json(ledger_path, {})
            entries = doc.get("entries") if isinstance(doc, dict) and isinstance(doc.get("entries"), dict) else {}
            cleaned = {}
            for p_nm, bases in entries.items():
                if not isinstance(bases, dict):
                    continue
                kept_b = {}
                for b_id, rec in bases.items():
                    if isinstance(rec, dict) and (now_t - float(rec.get("at") or 0)) <= ttl_s:
                        im = rec.get("items")
                        if isinstance(im, dict) and im:
                            kept_b[str(b_id)] = {"at": int(rec.get("at") or now_t), "items": {str(k): int(v) for k, v in im.items() if int(v or 0) > 0}}
                if kept_b:
                    cleaned[str(p_nm)] = kept_b
            if pilot and base_id:
                p_map = cleaned.setdefault(str(pilot), {})
                if my_items:
                    p_map[str(base_id)] = {"at": int(now_t), "items": my_items}
                else:
                    p_map.pop(str(base_id), None)
                    if not p_map:
                        cleaned.pop(str(pilot), None)
            for p_nm, bases in cleaned.items():
                for b_id, rec in bases.items():
                    if p_nm == str(pilot) and b_id == str(base_id):
                        continue
                    for iid, qty in (rec.get("items") or {}).items():
                        others[iid] = others.get(iid, 0) + int(qty or 0)
            write_json(ledger_path, {"updated_at": int(now_t), "entries": cleaned})
        finally:
            fcntl.flock(lf, fcntl.LOCK_UN)
    return others


def plan_bursar_actions(book, stored_items, own_orders, open_needs, reserved, catalog_vals, credits, policy, fleet_open_buys=None):
    actions = []
    sell_cfg = policy.get("sell") or {}
    buy_cfg = policy.get("buy") or {}
    min_keep = int(policy.get("min_cash_keep") or 20000)

    own_sell, own_buy = {}, {}
    for o in own_orders or []:
        if not isinstance(o, dict) or int(o.get("remaining") or 0) <= 0:
            continue
        iid = str(o.get("item_id") or "")
        side = str(o.get("side") or o.get("order_type") or "").lower()
        if side == "sell":
            own_sell.setdefault(iid, []).append(o)
        elif side == "buy":
            own_buy.setdefault(iid, []).append(o)

    if sell_cfg.get("enabled", True):
        respect_res = bool(sell_cfg.get("respect_reserve", True))
        max_sell_ords = int(sell_cfg.get("max_orders_per_station") or 8)
        undercut = max(1, int(sell_cfg.get("undercut_cr") or 1))
        min_ratio = float(sell_cfg.get("min_price_ratio") or 0.75)
        hit_ratio = float(sell_cfg.get("instant_hit_bid_ratio") or 0.85)
        used_sell_ords = 0
        for iid, qty in sorted((stored_items or {}).items()):
            qty = int(qty or 0)
            if qty <= 0 or iid in PROTECTED_ITEMS or (respect_res and iid in reserved):
                continue
            row = (book or {}).get(iid) or {}
            bid = float(row.get("best_buy") or 0)
            bid_q = int(row.get("best_buy_qty") or row.get("buy_quantity") or 0)
            ask = float(row.get("best_sell") or 0)
            base_v = float((catalog_vals or {}).get(iid) or 0)
            ref_p = max(base_v, bid, ask * 0.5)
            if ref_p < 2:
                continue
            floor_p = max(2, int(round(ref_p * min_ratio)))
            if bid >= max(floor_p, int(round(ref_p * hit_ratio))) and bid_q > 0:
                actions.append(("sell_bid", iid, min(qty, bid_q), int(bid)))
                continue
            if used_sell_ords >= max_sell_ords:
                continue
            mine = own_sell.get(iid) or []
            my_min_sell = min((int(o.get("price_each") or 0) for o in mine if int(o.get("price_each") or 0) > 0), default=0)
            if my_min_sell > 0 and (ask <= 0 or my_min_sell <= int(ask)):
                # Already the cheapest ask on the book: never undercut ourselves!
                target_p = max(floor_p, my_min_sell)
            else:
                target_p = max(floor_p, int(ask) - undercut) if ask > 0 else max(floor_p, int(round(ref_p * 1.05)))
            if bid > 0 and target_p <= int(bid):
                target_p = int(bid) + 1
            listed = sum(int(o.get("remaining") or 0) for o in mine)
            for o in mine:
                if int(o.get("price_each") or 0) != target_p and o.get("order_id"):
                    actions.append(("sell_modify", iid, o["order_id"], target_p))
            more = max(0, qty - listed)
            if more > 0:
                actions.append(("sell_create", iid, more, target_p))
            if mine or more > 0:
                used_sell_ords += 1

    if not buy_cfg.get("enabled", True) and buy_cfg.get("unwind_when_off", True):
        for iid, mine in sorted(own_buy.items()):
            for o in mine:
                if o.get("order_id"):
                    actions.append(("buy_cancel", iid, o["order_id"]))

    if buy_cfg.get("enabled", True):
        raw_cap = buy_cfg.get("max_escrow_per_station")
        max_escrow = int(raw_cap) if raw_cap is not None else 0
        max_buy_ords = int(buy_cfg.get("max_orders_per_station") or 4)
        max_units = int(buy_cfg.get("max_units_per_order") or 200)
        max_ratio = float(buy_cfg.get("max_unit_price_ratio") or 0.90)
        outbid = max(1, int(buy_cfg.get("outbid_cr") or 1))
        free_cash = max(0, int(credits or 0) - min_keep)
        cash_avail = min(max_escrow, free_cash) if max_escrow > 0 else free_cash
        excl_buy = set(str(x) for x in (buy_cfg.get("exclude_buy_items") or []))
        want_items = {k: v for k, v in (open_needs or {}).items() if k not in excl_buy} if buy_cfg.get("use_needs_tsv", True) else {}
        for extra in buy_cfg.get("extra_items") or []:
            if isinstance(extra, str) and extra not in want_items and extra not in excl_buy:
                want_items[extra] = max_units
        f_open = fleet_open_buys if isinstance(fleet_open_buys, dict) else {}
        if buy_cfg.get("unwind_excess", True):
            for iid, mine in sorted(own_buy.items()):
                tot_need = int(want_items.get(iid) or 0)
                other_q = int(f_open.get(iid) or 0)
                allowed_here = max(0, min(tot_need - other_q, max_units)) if tot_need > 0 else 0
                listed_here = sum(int(o.get("remaining") or 0) for o in mine)
                if tot_need <= 0 or (fleet_open_buys is not None and listed_here > max(allowed_here, int(allowed_here * 1.25)) and other_q >= tot_need):
                    for o in mine:
                        if o.get("order_id"):
                            actions.append(("buy_cancel", iid, o["order_id"]))
                    own_buy[iid] = []
        used_buy_ords = 0
        for iid, need_qty in sorted(want_items.items(), key=lambda kv: (-int(kv[1]), kv[0])):
            if used_buy_ords >= max_buy_ords or cash_avail <= 0:
                break
            other_q = int(f_open.get(iid) or 0)
            fleet_rem = max(0, int(need_qty) - other_q)
            if fleet_rem <= 0 and not (own_buy.get(iid) or []):
                continue
            row = (book or {}).get(iid)
            if not isinstance(row, dict):
                continue
            bid = float(row.get("best_buy") or 0)
            ask = float(row.get("best_sell") or 0)
            if bid <= 0 and ask <= 0:
                continue
            base_v = float((catalog_vals or {}).get(iid) or 0)
            if ask > 0:
                ceiling = int(ask * max_ratio)
                if base_v > 0:
                    ceiling = min(ceiling, int(base_v * 2.5))
            elif base_v > 0:
                ceiling = int(base_v * 1.1)
            else:
                continue
            if ceiling < 1:
                continue
            mine = own_buy.get(iid) or []
            my_max_buy = max((int(o.get("price_each") or 0) for o in mine if int(o.get("price_each") or 0) > 0), default=0)
            if my_max_buy > 0 and my_max_buy >= int(bid):
                # Already the top bid on the book: never outbid ourselves!
                target = my_max_buy
            else:
                target = int(bid) + outbid if bid > 0 else max(1, int(ceiling * 0.85))
            price = min(target, ceiling)
            if ask > 1 and price >= int(ask):
                price = int(ask) - 1
            if price < 1:
                continue
            listed = sum(int(o.get("remaining") or 0) for o in mine)
            for o in mine:
                if int(o.get("price_each") or 0) != price and o.get("order_id"):
                    actions.append(("buy_modify", iid, o["order_id"], price))
            more = min(max(0, min(fleet_rem, max_units) - listed), int(cash_avail // price))
            if more > 0:
                actions.append(("buy_create", iid, more, price))
                cash_avail -= more * price
            if mine or more > 0:
                used_buy_ords += 1
    return actions


def _option(args, flag, default=""):
    return args[args.index(flag) + 1] if flag in args and args.index(flag) + 1 < len(args) else default


def _heartbeat(order_path, every=60):
    stop_ev = threading.Event()
    try:
        orig_ino = os.stat(order_path).st_ino
    except OSError:
        orig_ino = None

    def beat():
        while not stop_ev.wait(every):
            try:
                st = os.stat(order_path)
                if orig_ino is not None and st.st_ino != orig_ino:
                    return
                os.utime(order_path)
            except OSError:
                return

    t = threading.Thread(target=beat, name="bursar-hb", daemon=True)
    t.stop = stop_ev.set
    t.start()
    return t


def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)
    if not args:
        sys.exit("USAGE: bursar.py <pilot> [--minutes 30] [--route bursar-network] [--policy game/bursar-policy.json] [--station sys:poi:base]")
    pilot = args[0]
    division.require(pilot)
    minutes = float(_option(args, "--minutes", "30"))
    route_id = _option(args, "--route", "bursar-network")
    policy_path = _option(args, "--policy", "") or None
    explicit_station = _option(args, "--station", "") or None

    policy = load_policy(policy_path)
    p_enc = urllib.parse.quote(pilot, safe="")
    order_path = DATA / "fleet" / "orders" / ship_file_name(pilot)
    stop_files = (DATA / "fleet" / "host" / "stop" / pilot, DATA / "fleet" / "host" / "stop" / ship_file_name(pilot))
    started = time.time()
    notes = []

    def say(msg):
        print("%s | %s | %s" % (utc_now(), pilot, msg), flush=True)

    def raw(action, params=None, group="spacemolt"):
        _, d = _call_json("POST", "/accounts/%s/raw" % p_enc, {"toolGroup": group, "action": action, "params": params or {}}, timeout=120)
        return d if isinstance(d, dict) else {}

    def body(d):
        sc = d.get("structuredContent") if isinstance(d, dict) else None
        return sc if isinstance(sc, dict) else {}

    def get_credits():
        _, d = _call_json("GET", "/accounts/%s" % p_enc, timeout=60)
        return int(((d.get("state") or {}).get("credits")) or 0) if isinstance(d, dict) else 0

    def get_cargo():
        _, rows = _call_json("GET", "/accounts/%s/state/cargo" % p_enc, timeout=60)
        return {r.get("item_id"): int(r.get("quantity") or 0) for r in rows if isinstance(r, dict)} if isinstance(rows, list) else {}

    def run_goal(gtype, options, tries=3):
        waited = 0
        ans = {}
        while tries > 0:
            st, ans = _call_json("POST", "/accounts/%s/goal" % p_enc, {"type": gtype, "options": options}, timeout=900)
            if st == 200 and isinstance(ans, dict) and ans.get("success"):
                return True, str(ans.get("message") or "")
            err = str((ans.get("error") or ans.get("message") or st) if isinstance(ans, dict) else ans)
            if "already executing" in err and waited < 30:
                waited += 1
                time.sleep(10)
                continue
            tries -= 1
            time.sleep(10)
        msg = str((ans.get("message") or ans.get("error") or "") if isinstance(ans, dict) else ans)[:120]
        return False, msg

    def get_stored(base_id):
        d = body(raw("view_storage", {"station_id": base_id}, group="spacemolt_storage"))
        rows = d.get("items") or d.get("storage") or []
        out = {}
        for r in rows if isinstance(rows, list) else []:
            if isinstance(r, dict) and r.get("item_id"):
                out[str(r["item_id"])] = out.get(str(r["item_id"]), 0) + int(r.get("quantity") or 0)
        return out

    def save_station(base_id, sys_id):
        items = [i for i in (body(raw("view_market", {}, group="spacemolt_market")).get("items") or []) if isinstance(i, dict)]
        if items:
            rows = [{k: i.get(k) for k in ("item_id", "item_name", "category", "best_buy", "best_buy_qty", "buy_quantity", "best_sell", "best_sell_qty", "sell_quantity")} for i in items]
            write_json(DATA / "market" / ("%s.json" % base_id), {"base": base_id, "system": sys_id, "read_at": utc_now(), "source": "view_market, bursar docked", "items": rows})
        board = [m for m in (body(raw("get_missions")).get("missions") or []) if isinstance(m, dict)]
        if board:
            keep = [{k: m.get(k) for k in ("template_id", "mission_id", "title", "type", "difficulty", "rewards", "objectives", "expires_in_ticks", "giver")} for m in board]
            write_json(DATA / "missions" / ("%s.json" % base_id), {"base": base_id, "system": sys_id, "read_at": utc_now(), "source": "get_missions, bursar docked", "missions": keep})
        return {str(i.get("item_id")): i for i in items if i.get("item_id")}

    def stop_requested():
        if (DATA / "fleet" / "STOP").exists():
            return "fleet STOP"
        for sf in stop_files:
            if sf.exists():
                try:
                    sf.unlink()
                except OSError:
                    pass
                return "per-pilot stop file"
        return ""

    write_json(order_path, {"pilot": pilot, "what": "bursar " + route_id, "since": utc_now(), "pid": os.getpid()})
    hb = _heartbeat(order_path)
    before = get_credits()
    finished = []

    def cleanup():
        if finished:
            return
        finished.append(True)
        try:
            hb.stop()
        except Exception:
            pass
        release_claim(DATA, pilot)
        after = get_credits()
        mins = round((time.time() - started) / 60.0, 1)
        row = {
            "route": route_id, "kind": "bursar", "pilot": pilot,
            "started": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(started)),
            "minutes": mins, "credits_before": before, "credits_after": after,
            "delta": after - before if before and after else 0,
            "one_time": 0, "notes": notes[:12],
        }
        runs = DATA / "routes" / "runs.jsonl"
        runs.parent.mkdir(parents=True, exist_ok=True)
        with open(runs, "a", encoding="utf-8") as fh:
            fcntl.flock(fh, fcntl.LOCK_EX)
            fh.write(json.dumps(row, separators=(",", ":")) + "\n")
        print("RESULT %s: bursar %s | %.1f min | credits %d -> %d (%+d cr) | %s"
              % (pilot, route_id, mins, before, after, after - before, "; ".join(notes[:4]) or "ok"), flush=True)
        try:
            cur = read_json(order_path, {})
            if isinstance(cur, dict) and cur.get("pid") == os.getpid() and cur.get("what") == "bursar " + route_id:
                order_path.unlink()
        except OSError:
            pass

    try:
        ship_doc = read_json(DATA / "fleet" / "ships" / ship_file_name(pilot), {})
        unwind_bases = set()
        buy_pol = policy.get("buy") or {}
        if (not buy_pol.get("enabled", True) and buy_pol.get("unwind_when_off", True)) or (buy_pol.get("enabled", True) and buy_pol.get("unwind_excess", True)):
            open_n0, _, _ = load_needs_and_reserves(REPO, DATA)
            excl0 = set(str(x) for x in (buy_pol.get("exclude_buy_items") or []))
            want0 = {k: v for k, v in (open_n0 or {}).items() if k not in excl0} if buy_pol.get("use_needs_tsv", True) else {}
            first = raw("view_orders", {}, group="spacemolt_market")
            n_buy, at = order_stations(body(first).get("hint") or first.get("error") or "")
            for st_id in at if n_buy > 0 else []:
                rows = body(raw("view_orders", {"station_id": st_id}, group="spacemolt_market")).get("orders") or []
                brows = [o for o in rows if isinstance(o, dict) and str(o.get("side") or o.get("order_type") or "").lower() == "buy" and int(o.get("remaining") or 0) > 0]
                if not brows:
                    continue
                sync_fleet_buys(DATA, pilot, st_id, rows)
                if not buy_pol.get("enabled", True) or any(str(o.get("item_id") or "") not in want0 for o in brows):
                    unwind_bases.add(st_id)
            if unwind_bases:
                notes.append("unwind %d" % len(unwind_bases))
        claim = claim_station(DATA, REPO, pilot, ship_doc, policy, explicit_station=explicit_station,
                              unwind_bases=unwind_bases)
        if not claim:
            say("no unstaffed Exchange station available under max_per_station=%s" % policy.get("max_per_station", 1))
            notes.append("all stations staffed")
            time.sleep(60)
            return 0

        sys_id, poi_id, base_id = claim["system"], claim["poi"], claim["base"]
        say("claimed station %s (%s:%s)" % (base_id, sys_id, poi_id))
        notes.append("station %s" % base_id)

        ok, msg = run_goal("prepare-at-station", {"systemId": sys_id, "poiId": poi_id, "baseId": base_id, "refuel": True})
        if not ok:
            say("could not reach %s: %s" % (base_id, msg))
            notes.append("unreachable: %s" % msg[:60])
            return 0

        until = started + max(2.0, minutes) * 60.0
        poll_s = max(60.0, float(policy.get("poll_interval_s") or 120))
        acted = 0

        while time.time() < until and not stop_requested():
            try:
                book = save_station(base_id, sys_id)
                open_needs, reserved, catalog_vals = load_needs_and_reserves(REPO, DATA)
                hold = get_cargo()
                for iid, q in list(hold.items()):
                    if q > 0 and iid not in PROTECTED_ITEMS:
                        raw("deposit", {"item_id": iid, "quantity": q, "target": "self", "source": "cargo"}, group="spacemolt_storage")
                        time.sleep(TICK)
                stored = get_stored(base_id)
                orders_resp = body(raw("view_orders", {}, group="spacemolt_market")).get("orders") or []
                cr = get_credits()
                eff_pol = policy
                try:
                    import upgrades as _upg
                    if pilot in _upg.protected_pilots(DATA):
                        eff_pol = json.loads(json.dumps(policy))
                        eff_pol.setdefault("buy", {})["enabled"] = False
                except Exception:
                    pass
                fleet_open_buys = sync_fleet_buys(DATA, pilot, base_id, orders_resp)
                acts = plan_bursar_actions(book, stored, orders_resp, open_needs, reserved, catalog_vals, cr, eff_pol, fleet_open_buys=fleet_open_buys)
                for act in acts:
                    if stop_requested() or time.time() >= until:
                        break
                    kind_a = act[0]
                    if kind_a == "sell_bid":
                        _, iid, qty, bp = act
                        raw("withdraw", {"item_id": iid, "quantity": qty, "target": "self"}, group="spacemolt_storage")
                        time.sleep(TICK)
                        d = raw("sell", {"item_id": iid, "quantity": qty}, group="spacemolt")
                        time.sleep(TICK)
                        say("sell_bid %d %s @ ~%d cr%s" % (qty, iid, bp, " ERR" if "error" in d else ""))
                        acted += 1
                    elif kind_a == "sell_modify":
                        _, iid, oid, np = act
                        d = raw("modify_order", {"order_id": oid, "new_price": np}, group="spacemolt_market")
                        time.sleep(TICK)
                        say("sell_modify %s -> %d cr%s" % (iid, np, " ERR" if "error" in d else ""))
                        acted += 1
                    elif kind_a == "sell_create":
                        _, iid, qty, np = act
                        d = raw("create_sell_order", {"item_id": iid, "quantity": qty, "price_each": np}, group="spacemolt_market")
                        time.sleep(TICK)
                        say("sell_create %d %s @ %d cr%s" % (qty, iid, np, " ERR" if "error" in d else ""))
                        acted += 1
                    elif kind_a == "buy_modify":
                        _, iid, oid, np = act
                        d = raw("modify_order", {"order_id": oid, "new_price": np}, group="spacemolt_market")
                        time.sleep(TICK)
                        say("buy_modify %s -> %d cr%s" % (iid, np, " ERR" if "error" in d else ""))
                        acted += 1
                    elif kind_a == "buy_cancel":
                        _, iid, oid = act
                        d = raw("cancel_order", {"order_id": oid}, group="spacemolt_market")
                        time.sleep(TICK)
                        say("buy_cancel %s %s%s" % (iid, oid[:8], " ERR" if "error" in d else ""))
                        acted += 1
                    elif kind_a == "buy_create":
                        _, iid, qty, np = act
                        d = raw("create_buy_order", {"item_id": iid, "quantity": qty, "price_each": np}, group="spacemolt_market")
                        time.sleep(TICK)
                        say("buy_create %d %s @ %d cr%s" % (qty, iid, np, " ERR" if "error" in d else ""))
                        acted += 1
                if any(a[0] in ("buy_create", "buy_cancel") for a in acts):
                    try:
                        sync_fleet_buys(DATA, pilot, base_id, body(raw("view_orders", {}, group="spacemolt_market")).get("orders") or [])
                    except Exception:
                        pass
            except SystemExit:
                raise
            except Exception as err:
                say("poll error: %s: %s" % (type(err).__name__, str(err)[:120]))
                notes.append("poll err: %s" % type(err).__name__)
            rem = until - time.time()
            if rem <= 15:
                break
            nap_end = min(until, time.time() + poll_s)
            while time.time() < nap_end and not stop_requested():
                time.sleep(min(20.0, max(1.0, nap_end - time.time())))
                try:
                    os.utime(order_path)
                except OSError:
                    pass
        notes.append("actions=%d" % acted)
        return 0
    finally:
        cleanup()


if __name__ == "__main__":
    sys.exit(main())

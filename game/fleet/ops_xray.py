#!/usr/bin/env python3
"""ops_xray.py -- 1-call Cashflow X-Ray & Guarded 0-Hop Vault Cash-Infusion Liquidation CLI.

Powers `xray` (read-only) and `liquidate` (dry-run by default; --execute required) on `trinity_collective` MCP.

Usage:
  ops_xray.py xray [--hours 1] [--top 10] [--data /srv/collective/data]
  ops_xray.py liquidate [--base ID] [--item ID] [--min-cash 5000] [--max-jobs 6] [--keep-cr 18000] [--execute]

Stdlib only. 7-bit ASCII only.
"""
import argparse
import json
import re
import sqlite3
import sys
import time
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import accounting
import gate
import haul
import market_guard as mg

PROTECTED_ITEMS = frozenset(("fuel", "fuel_cell", "antimatter_containment_cell", "repair_kit", "hull_patch", "water_ice"))
TIER1_HUBS = (
    "a2cee88abdcb31db229c04315f0ef6e1",
    "nova_terra_central",
    "grand_exchange_station",
    "central_nexus",
)


def _read_json(path, default=None):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {} if default is None else default


def _open_ro_db(data_dir):
    dbp = Path(data_dir) / "store" / "read.db"
    if not dbp.is_file():
        return None
    con = sqlite3.connect("file:%s?mode=ro&immutable=1" % dbp, uri=True, timeout=5.0)
    con.row_factory = sqlite3.Row
    return con


def compute_anomalies(data_dir, now_t=None):
    """Detect live operational anomalies across Treasury, Bursars, Haulers, Passengers, and Services."""
    data = Path(data_dir)
    now_t = time.time() if now_t is None else float(now_t)
    anoms = []

    # 1. Passenger boards cache thinness
    pb = _read_json(data / "fleet" / "passenger_boards.json", {})
    pb_n = len(pb.get("boards") or {}) if isinstance(pb, dict) else 0
    pb_age = int(now_t - float(pb.get("updated_at") or 0)) if isinstance(pb, dict) and pb.get("updated_at") else 99999
    if pb_n < 10:
        anoms.append(("passenger_boards_thin", "CRITICAL", pb_n, "only %d stations cached (age=%ds; expected >=25)" % (pb_n, pb_age)))

    # 2. Treasury vs TOPUP_FLOOR & low-cash fleet count
    emp = _read_json(data / "empire" / "empire.json", {})
    tr = None
    if isinstance(emp, dict):
        for k in ("credits", "treasury"):
            if isinstance(emp.get(k), (int, float)):
                tr = int(emp[k])
                break
        if tr is None and isinstance(emp.get("faction"), dict):
            for k in ("credits", "treasury"):
                if isinstance(emp["faction"].get(k), (int, float)):
                    tr = int(emp["faction"][k])
                    break
    fl = _read_json(data / "fleet" / "fleet.json", {})
    ships = fl.get("ships") if isinstance(fl, dict) and isinstance(fl.get("ships"), list) else []
    low_cash = sum(1 for s in ships if isinstance(s, dict) and int(s.get("credits") or 0) < 10000)
    crit_cash = sum(1 for s in ships if isinstance(s, dict) and int(s.get("credits") or 0) < 3000)
    if tr is not None and tr < 120000 and low_cash > 50:
        anoms.append(("treasury_below_topup_floor", "CRITICAL", low_cash, "treasury=%d cr (<120k), low(<10k)=%d, crit(<3k)=%d" % (tr, low_cash, crit_cash)))
    elif crit_cash >= 200:
        anoms.append(("high_crit_cash_pilots", "WARN", crit_cash, "crit(<3k)=%d, low(<10k)=%d" % (crit_cash, low_cash)))

    # 3. Excess Bursar open buy orders
    bb = _read_json(data / "fleet" / "bursar_buys.json", {})
    open_buy_n = 0
    for bases in ((bb.get("entries") or {}).values() if isinstance(bb, dict) else ()):
        for rec in (bases.values() if isinstance(bases, dict) else ()):
            if isinstance(rec, dict) and (now_t - float(rec.get("at") or 0)) <= 21600:
                open_buy_n += sum(1 for q in (rec.get("items") or {}).values() if int(q or 0) > 0)
    if open_buy_n > 50:
        anoms.append(("bursar_excess_buy_orders", "WARN", open_buy_n, "%d active buy orders in bursar_buys.json (unwinding)" % open_buy_n))

    # 4. Unstaffed Tier-1 Exchange hubs
    bc = _read_json(data / "fleet" / "bursar_claims.json", {})
    if isinstance(bc, dict) and bc:
        missing_t1 = [h for h in TIER1_HUBS if not bc.get(h)]
        if missing_t1:
            anoms.append(("unstaffed_tier1_hub", "WARN", len(missing_t1), "missing Bursar at: " + ",".join(missing_t1)))

    # 5. Services health (<data_parent>/services/status.json -> /srv/collective/services/status.json)
    st_p = data.parent / "services" / "status.json"
    if st_p.is_file():
        st_doc = _read_json(st_p, {})
        svcs = st_doc.get("services") if isinstance(st_doc, dict) else {}
        down = [k for k, v in (svcs or {}).items() if isinstance(v, dict) and v.get("state") != "running"]
        if down:
            anoms.append(("service_down", "CRITICAL", len(down), "not running: " + ",".join(sorted(down))))

    # 6. Recent cargo_full / access_denied error spikes in fresh (<10m) runner logs
    log_dir = data / "routes" / "logs"
    if log_dir.is_dir():
        cf_cnt = 0
        ad_cnt = 0
        cutoff = now_t - 600.0
        for lp in log_dir.iterdir():
            try:
                if lp.suffix != ".log" or lp.stat().st_mtime < cutoff:
                    continue
                tail = lp.read_text(encoding="utf-8", errors="replace")[-2500:]
                if "cargo_full" in tail:
                    cf_cnt += 1
                if "access_denied" in tail.lower() or "access denied" in tail.lower():
                    ad_cnt += 1
            except OSError:
                continue
        if cf_cnt >= 3:
            anoms.append(("recent_cargo_full", "WARN", cf_cnt, "%d recent runner logs mention cargo_full" % cf_cnt))
        if ad_cnt >= 5:
            anoms.append(("recent_access_denied", "WARN", ad_cnt, "%d recent runner logs mention access_denied" % ad_cnt))

    # 7. Ridgecrest critical station infrastructure upkeep zero check (Refueling Dock / Shield)
    _con_rc = _open_ro_db(data)
    if _con_rc is not None:
        try:
            _rc_rows = {
                str(r["item"]): int(r["units"] or 0)
                for r in _con_rc.execute(
                    "SELECT item, units FROM faction_storage WHERE base = ? AND item IN ('flex_polymer','steel_plate','copper_wiring','fuel')",
                    ("a2cee88abdcb31db229c04315f0ef6e1",),
                ).fetchall()
            }
            _miss_infra = [it for it in ("flex_polymer", "steel_plate", "copper_wiring") if _rc_rows.get(it, 0) <= 0]
            if _miss_infra:
                anoms.append(("resort_infra_upkeep_zero", "CRITICAL", len(_miss_infra),
                              "Ridgecrest missing Refueling Dock upkeep: " + ",".join(_miss_infra) + " (fuel=" + str(_rc_rows.get("fuel", 0)) + ")"))
        except sqlite3.Error:
            pass
        finally:
            _con_rc.close()

    return anoms


def plan_zero_hop_liquidation(data_dir, base_filter="", item_filter="", min_cash=5000, max_jobs=6, now_t=None):
    """Find market_guard-verified, size-aware, unreserved 0-hop faction-storage liquidation jobs with docked Officers."""
    data = Path(data_dir)
    now_t = time.time() if now_t is None else float(now_t)
    stor = _read_json(data / "stock" / "storage.json", {})
    fstor = haul._load_faction_storage_by_base(data, stor)
    resv = haul._load_reserved_items_exact(data)
    books = haul._load_books(data)
    cltv_q = haul._load_cltv_open_buy_qty(data, now_t=now_t)
    sz_map = haul._load_item_sizes(data)
    vwm = mg.compute_book_vwm_map(books, cltv_buy_qty=cltv_q, now_t=now_t)

    bid_map = {}
    for r in books:
        b = str(r.get("base") or "")
        it = str(r.get("item") or "")
        if not (b and it and "_" in b):
            continue
        bp = float(r.get("bid") or 0)
        bq = max(0, int(r.get("bid_qty") or 0) - int(cltv_q.get((b, it), 0)))
        if bp < 5.0 or bq < 10:
            continue
        if (now_t - float(r.get("t") or 0)) > 7200.0:
            continue
        fv = float((vwm.get(it) or {}).get("vwm") or 0.0)
        if fv >= 20.0 and bp < fv * 0.70:
            continue
        bid_map[(b, it)] = (bp, bq, fv)

    con = _open_ro_db(data)
    docked_offs = {}
    if con is not None:
        try:
            cols = {c[1] for c in con.execute("PRAGMA table_info(ships)").fetchall()}
            order_sql = (
                "ORDER BY CASE WHEN flies IS NULL OR flies = '' THEN 0 ELSE 1 END, (cargo_capacity - cargo_used) DESC"
                if "flies" in cols else "ORDER BY (cargo_capacity - cargo_used) DESC"
            )
            for r in con.execute(
                "SELECT pilot, role, base, cargo_used, cargo_capacity, credits FROM ships "
                "WHERE docked = 1 AND base IS NOT NULL " + order_sql
            ).fetchall():
                if haul._pilot_can_withdraw_faction(data, r["pilot"]):
                    docked_offs.setdefault(str(r["base"]), []).append(dict(r))
        finally:
            con.close()

    jobs = []
    for base, items in fstor.items():
        if base_filter and base != base_filter:
            continue
        offs = docked_offs.get(base) or []
        if not offs:
            continue
        best_off = offs[0]
        free = max(0, int(best_off.get("cargo_capacity") or 0) - int(best_off.get("cargo_used") or 0))
        if free < 10:
            continue
        for it, qty in items.items():
            if item_filter and it != item_filter:
                continue
            if qty < 5 or it in resv or it in PROTECTED_ITEMS:
                continue
            if (base, it) not in bid_map:
                continue
            bp, bq, fv = bid_map[(base, it)]
            sz = max(1, int(sz_map.get(it, 1)))
            chunk = free // sz
            if chunk < 1:
                continue
            sq = min(int(qty), int(bq))
            cash = int(round(sq * bp))
            if cash < int(min_cash):
                continue
            jobs.append({
                "pilot": best_off["pilot"],
                "base": base,
                "item": it,
                "item_size": sz,
                "free_hold": free,
                "chunk_units": chunk,
                "qty": sq,
                "vault_qty": int(qty),
                "bid": bp,
                "vwm": fv,
                "est_cash": cash,
            })
    jobs.sort(key=lambda x: -x["est_cash"])
    return jobs[:max(1, int(max_jobs))]


def _call_raw(pilot, group, action, params=None):
    st, txt = gate.call(
        "post",
        "/accounts/%s/raw" % gate.q(pilot),
        {"toolGroup": group, "action": action, "params": params or {}},
        timeout=35,
    )
    body = json.loads(txt[txt.find("{"):]) if "{" in txt else {}
    sc = body.get("structuredContent") if isinstance(body, dict) else {}
    err = body.get("error") or (sc.get("error") if isinstance(sc, dict) else None)
    return st == 200 and not err, sc or body, str(err or "")


def run_xray(data_dir, hours=1, top_n=10):
    data = Path(data_dir)
    now_t = time.time()
    out = ["COLLECTIVE OPS & CASHFLOW X-RAY (window=%dh, data=%s)" % (hours, data)]

    # 1. IFRS 15/10/8 Income summary (same reconciled formula as accounting.py --income)
    con_pnl = _open_ro_db(data)
    try:
        pnl = accounting.compute_pnl(con_pnl, repo_root=str(REPO), data_dir=str(data), hours=int(hours))
        rb = pnl.get("revenue_breakdown") or {}
        ob = pnl.get("opex_breakdown") or {}
        st = pnl.get("station_ops") or {}
        real_rev = int(pnl.get("raw_income_h") or 0) + int(pnl.get("passive_inflows_h") or 0) + int(st.get("station_revenue_h") or 0)
        matched_dir = int(ob.get("matched_direct_h") or 0)
        core_ebit = int(pnl.get("recurring_cash_h") or 0) + int(pnl.get("treasury_own_h") or 0)
        paid_fuel = int(ob.get("fuel_h") or 0)
        rof_s = ("%.2fx" % (real_rev / float(paid_fuel))) if paid_fuel >= 100 else "n/a"
        out.append(
            "  P&L (%dh)      : Core EBIT %+s cr/h | Rev %s/h (Trade %s, Freight %s, StOps %s) | Costs -%s/h (Fuel %s, OtherCOGS %s) | ROF %s" % (
                hours,
                format(core_ebit, ","),
                format(real_rev, ","),
                format(int(rb.get("trade_sales_h") or 0), ","),
                format(int(rb.get("freight_sales_h") or 0), ","),
                format(int(st.get("station_revenue_h") or 0), ","),
                format(matched_dir, ","),
                format(paid_fuel, ","),
                format(int(ob.get("other_cogs_h") or 0), ","),
                rof_s,
            )
        )
    except Exception as err:
        out.append("  P&L (%dh)      : unavailable (%s)" % (hours, str(err)[:80]))
    finally:
        if con_pnl is not None:
            con_pnl.close()

    # 2. Treasury & Wallets
    con = _open_ro_db(data)
    tr = None
    low_n = crit_n = tot_w = ships_n = 0
    futs_tot = futs_dk = futs_away = 0
    if con is not None:
        try:
            r_f = con.execute("SELECT treasury, t FROM faction LIMIT 1").fetchone()
            if r_f:
                tr = int(r_f["treasury"] or 0)
            r_w = con.execute(
                "SELECT COUNT(*) n, SUM(credits) s, SUM(CASE WHEN credits<10000 THEN 1 ELSE 0 END) lo, "
                "SUM(CASE WHEN credits<3000 THEN 1 ELSE 0 END) cr FROM ships"
            ).fetchone()
            if r_w:
                ships_n, tot_w, low_n, crit_n = int(r_w["n"] or 0), int(r_w["s"] or 0), int(r_w["lo"] or 0), int(r_w["cr"] or 0)
            r_p = con.execute(
                "SELECT COUNT(*) tot, SUM(docked) dk, SUM(CASE WHEN system!='ridgecrest' THEN 1 ELSE 0 END) aw "
                "FROM ships WHERE class='Futures'"
            ).fetchone()
            if r_p:
                futs_tot, futs_dk, futs_away = int(r_p["tot"] or 0), int(r_p["dk"] or 0), int(r_p["aw"] or 0)
        finally:
            con.close()
    tr_s = ("%s cr" % format(tr, ",")) if tr is not None else "unknown"
    out.append(
        "  Liquidity     : Treasury %s (TOPUP_FLOOR 100k | FUND_FLOOR 500k) | Wallets %s cr (%d ships: low<10k=%d, crit<3k=%d)" % (
            tr_s, format(tot_w, ","), ships_n, low_n, crit_n
        )
    )

    # 3. Bursars & Haul Claims & Passengers
    bb = _read_json(data / "fleet" / "bursar_buys.json", {})
    active_buys = sum(
        1 for bases in ((bb.get("entries") or {}).values() if isinstance(bb, dict) else ())
        for rec in (bases.values() if isinstance(bases, dict) else ())
        if isinstance(rec, dict) and (now_t - float(rec.get("at") or 0)) <= 21600
        for q in (rec.get("items") or {}).values() if int(q or 0) > 0
    )
    bc = _read_json(data / "fleet" / "bursar_claims.json", {})
    t1_ok = [h[:14] for h in TIER1_HUBS if isinstance(bc, dict) and bc.get(h)]
    out.append("  Bursars       : %d staffed | Tier-1 covered: %d/%d %s | open_buy_orders=%d" % (len(bc) if isinstance(bc, dict) else 0, len(t1_ok), len(TIER1_HUBS), t1_ok, active_buys))

    hc = _read_json(data / "fleet" / "haul_claims.json", {})
    c_all = Counter(k.split(":")[0] for k in hc) if isinstance(hc, dict) else Counter()
    c_15m = Counter(k.split(":")[0] for k, v in hc.items() if isinstance(v, dict) and (now_t - float(v.get("at") or 0)) < 900) if isinstance(hc, dict) else Counter()
    out.append("  Haul Claims   : all=%s | <15m=%s" % (dict(c_all), dict(c_15m)))

    pb = _read_json(data / "fleet" / "passenger_boards.json", {})
    boards = pb.get("boards") if isinstance(pb, dict) and isinstance(pb.get("boards"), dict) else {}
    pax_tot = sum(len((v or {}).get("waiting") or []) for v in boards.values() if isinstance(v, dict))
    surging = sum(1 for v in boards.values() if isinstance(v, dict) and float((v or {}).get("fare_surge") or 0) >= 1.5 and (v or {}).get("waiting"))
    prc = _read_json(data / "fleet" / "passenger_rep_claims.json", {})
    active_rep = sum(1 for v in (prc.values() if isinstance(prc, dict) else ()) if isinstance(v, dict) and float(v.get("exp") or 0) > now_t)
    out.append(
        "  Passengers 6B : %d/%d Futures away (docked=%d) | boards=%d hubs (%d pax, %d surging>=1.5x, age=%ds) | rep_claims=%d" % (
            futs_away, futs_tot, futs_dk, len(boards), pax_tot, surging,
            int(now_t - float(pb.get("updated_at") or 0)) if isinstance(pb, dict) and pb.get("updated_at") else -1,
            active_rep,
        )
    )

    # 3b. Resort 8A (Appeal, Exact 24h Station Rev, Refuel Dock Upkeep, 24h Resort Restock Spend)
    try:
        import station_pnl as _spnl
        _sp = _spnl.compute_station_pnl(data_dir=str(data))
        _rc_st = next((x for x in (_sp.get("stations") or []) if "ridgecrest" in str(x.get("system") or x.get("name") or "").lower() or "a2cee88" in str(x.get("base") or x.get("id") or "")), None)
        _live_app = int((_rc_st or {}).get("live_appeal") or (_rc_st or {}).get("appeal_live") or 0)
        _built_app = int((_rc_st or {}).get("built_appeal") or (_rc_st or {}).get("appeal_built") or 47)
        _app_rank = (_rc_st or {}).get("live_appeal_rank") or (_rc_st or {}).get("appeal_rank") or (_rc_st or {}).get("rank")
        _fr = _sp.get("forensic_revenue") or {}
        _r24 = _fr.get("24h") or _fr.get(24) or {}
        _rr_spend = 0
        _rr_buys = 0
        _rr_p = data / "fleet" / "resort_restock.jsonl"
        if _rr_p.is_file():
            _cut24 = now_t - 86400.0
            for _ln in _rr_p.read_text(encoding="utf-8", errors="replace").splitlines():
                if not _ln.strip():
                    continue
                try:
                    _rec = json.loads(_ln)
                    if float(_rec.get("t") or 0) >= _cut24 and _rec.get("ok"):
                        _rr_spend += int(_rec.get("spend_cr") or 0)
                        _rr_buys += 1
                except (ValueError, TypeError):
                    continue
        _rc_pol = _read_json(REPO / "game" / "bursar-policy.json", {}).get("resort_restock") or {}
        _rc_cap = int(_rc_pol.get("max_spend_per_pass_cr") or 12000)
        _con_r = _open_ro_db(data)
        _rc_inv = {}
        if _con_r is not None:
            try:
                for _r in _con_r.execute("SELECT item, units FROM faction_storage WHERE base = ? AND item IN ('fuel','flex_polymer','steel_plate','copper_wiring')", ("a2cee88abdcb31db229c04315f0ef6e1",)).fetchall():
                    _rc_inv[str(_r["item"])] = int(_r["units"] or 0)
            finally:
                _con_r.close()
        _rk_s = ("#%s" % _app_rank) if _app_rank else "#?"
        out.append(
            "  Resort 8A     : Appeal %d/%d (%s) | 24h Rev +%s/h (Tour +%s/h [%dv], Refuel +%s/h [%d ext]) | Fuel %d | FlexPoly %d | Restock24h %s cr (%d buys, cap %dk/pass)" % (
                _live_app, _built_app, _rk_s,
                format(int(_r24.get("gross_rev_h") or _r24.get("gross_h") or 0), ","),
                format(int(_r24.get("tourism_h") or 0), ","), int(_r24.get("visits") or _r24.get("tourism_visits") or 0),
                format(int(_r24.get("refuel_h") or 0), ","), int(_r24.get("ext_payers") or _r24.get("refuel_count") or 0),
                int(_rc_inv.get("fuel") or 0), int(_rc_inv.get("flex_polymer") or 0),
                format(_rr_spend, ","), _rr_buys, _rc_cap // 1000,
            )
        )
    except Exception as _re:
        out.append("  Resort 8A     : unavailable (%s)" % str(_re)[:80])

    # 4. Top 0-hop instant cashable vault jobs
    jobs = plan_zero_hop_liquidation(data, min_cash=2500, max_jobs=top_n, now_t=now_t)
    out.append("  0-Hop Cashable Vault (unreserved, market_guard-verified, docked Officer ready): %d job(s), %s cr total" % (
        len(jobs), format(sum(j["est_cash"] for j in jobs), ",")
    ))
    for j in jobs[:top_n]:
        out.append(
            "    - %9s cr | %-24s | %-20s q=%4d/%4d (sz=%d, chunk=%3d) @%5.1f | %s" % (
                format(j["est_cash"], ","), j["base"][:24], j["item"][:20],
                j["qty"], j["vault_qty"], j["item_size"], j["chunk_units"], j["bid"], j["pilot"]
            )
        )

    # 5. Live Anomalies
    anoms = compute_anomalies(data, now_t=now_t)
    if not anoms:
        out.append("  ANOMALIES     : NONE (ALL CLEAR)")
    else:
        out.append("  ANOMALIES (%d):" % len(anoms))
        for code, sev, cnt, det in anoms:
            out.append("    - [%s] %s (%d): %s" % (sev, code, cnt, det))
    return "\n".join(out)


def run_liquidate(data_dir, base_filter="", item_filter="", min_cash=5000, max_jobs=6, keep_cr=18000, execute=False):
    jobs = plan_zero_hop_liquidation(data_dir, base_filter=base_filter, item_filter=item_filter, min_cash=min_cash, max_jobs=max_jobs)
    if not jobs:
        return "LIQUIDATE: 0 eligible 0-hop unreserved market_guard-verified jobs found (min_cash=%d)." % min_cash
    lines = ["LIQUIDATE (%s): %d job(s), est %s cr" % ("EXECUTE" if execute else "DRY-RUN", len(jobs), format(sum(j["est_cash"] for j in jobs), ","))]
    for j in jobs:
        lines.append(
            "  PLAN: %s @ %s | %d/%d %s (size=%d, chunk=%d) @ %.1f cr (vwm=%.1f) -> est %s cr" % (
                j["pilot"], j["base"], j["qty"], j["vault_qty"], j["item"], j["item_size"], j["chunk_units"], j["bid"], j["vwm"], format(j["est_cash"], ",")
            )
        )
    if not execute:
        lines.append("Dry-run only. Pass execute=true to withdraw, sell into live external buy-walls, and deposit proceeds > %d cr into Faction Treasury." % keep_cr)
        return "\n".join(lines)

    tot_realized = 0
    tot_deposited = 0
    deadline = time.monotonic() + 70.0
    by_pilot = {}
    for j in jobs:
        by_pilot.setdefault((j["pilot"], j["base"]), []).append(j)
    for (pilot, base), pjobs in by_pilot.items():
        ok, sc, err = _call_raw(pilot, "spacemolt", "get_status", {})
        if not ok:
            lines.append("  SKIP %s: get_status failed (%s)" % (pilot, err[:80]))
            continue
        loc = sc.get("location") or {}
        sh = sc.get("ship") or {}
        pl = sc.get("player") or {}
        cur_base = str(loc.get("base_id") or loc.get("docked_at_base") or loc.get("docked_at") or "")
        if cur_base != base:
            lines.append("  SKIP %s: moved to %s (expected %s)" % (pilot, cur_base, base))
            continue
        cap = int(sh.get("cargo_capacity") or 100)
        free = max(0, cap - int(sh.get("cargo_used") or 0))
        cr_now = int(pl.get("credits") or 0)
        for j in pjobs:
            rem = int(j["qty"])
            sz = int(j["item_size"])
            while rem > 0 and free >= sz:
                if time.monotonic() >= deadline:
                    lines.append("  STOP %s: reached 70s MCP safety deadline (%d %s left); depositing proceeds now" % (pilot, rem, j["item"]))
                    break
                chunk = min(rem, free // sz)
                ok_w, _, err_w = _call_raw(pilot, "spacemolt_storage", "withdraw", {"item_id": j["item"], "quantity": chunk, "target": "faction"})
                if not ok_w:
                    m_avail = re.search(r"only has\s+(\d+)", err_w or "", re.I)
                    if m_avail and int(m_avail.group(1)) > 0:
                        avail = min(chunk - 1, int(m_avail.group(1)))
                        if avail > 0:
                            chunk = avail
                            rem = min(rem, avail)
                            ok_w, _, err_w = _call_raw(pilot, "spacemolt_storage", "withdraw", {"item_id": j["item"], "quantity": chunk, "target": "faction"})
                    if not ok_w:
                        lines.append("  ERR %s withdraw %dx %s: %s" % (pilot, chunk, j["item"], err_w[:80]))
                        break
                time.sleep(10.5)
                ok_s, _, err_s = _call_raw(pilot, "spacemolt", "sell", {"id": j["item"], "quantity": chunk, "auto_list": False})
                time.sleep(10.5)
                ok2, sc2, _ = _call_raw(pilot, "spacemolt", "get_status", {})
                new_cr = int((sc2.get("player") or {}).get("credits") or cr_now) if ok2 else cr_now
                sh2 = (sc2.get("ship") or {}) if ok2 else {}
                free = max(0, int(sh2.get("cargo_capacity") or cap) - int(sh2.get("cargo_used") or 0))
                gained = new_cr - cr_now
                lines.append("  EXEC %s sold %dx %s @ %s: %+d cr (ok=%s)" % (pilot, chunk, j["item"], base, gained, ok_s))
                if not ok_s or gained <= 0:
                    _call_raw(pilot, "spacemolt_storage", "deposit", {"item_id": j["item"], "quantity": chunk, "target": "faction", "source": "cargo"})
                    time.sleep(10.5)
                    break
                tot_realized += gained
                cr_now = new_cr
                rem -= chunk
        dep = max(0, cr_now - int(keep_cr))
        if dep >= 2000:
            ok_d, _, err_d = _call_raw(pilot, "spacemolt_storage", "deposit", {"target": "faction", "item_id": "credits", "quantity": dep})
            time.sleep(10.5)
            if ok_d:
                tot_deposited += dep
                try:
                    import wallet as _w_dep
                    _w_dep.book_direct_deposit(data_dir, pilot, dep)
                except Exception:
                    pass
            lines.append("  TREASURY %s deposited +%s cr (ok=%s%s)" % (pilot, format(dep, ","), ok_d, (" " + err_d[:60]) if err_d else ""))
    lines.append("TOTAL REALIZED: +%s cr | DEPOSITED TO TREASURY: +%s cr" % (format(tot_realized, ","), format(tot_deposited, ",")))
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Collective Cashflow X-Ray & Guarded 0-Hop Vault Liquidation")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p_x = sub.add_parser("xray")
    p_x.add_argument("--hours", type=int, default=1)
    p_x.add_argument("--top", type=int, default=10)
    p_x.add_argument("--data", default="/srv/collective/data")

    p_l = sub.add_parser("liquidate")
    p_l.add_argument("--base", default="")
    p_l.add_argument("--item", default="")
    p_l.add_argument("--min-cash", type=int, default=5000)
    p_l.add_argument("--max-jobs", type=int, default=6)
    p_l.add_argument("--keep-cr", type=int, default=18000)
    p_l.add_argument("--execute", action="store_true")
    p_l.add_argument("--data", default="/srv/collective/data")

    args = ap.parse_args(argv)
    if args.cmd == "xray":
        print(run_xray(args.data, hours=args.hours, top_n=args.top))
    else:
        print(run_liquidate(args.data, base_filter=args.base, item_filter=args.item,
                            min_cash=args.min_cash, max_jobs=args.max_jobs,
                            keep_cr=args.keep_cr, execute=args.execute))
    return 0


if __name__ == "__main__":
    sys.exit(main())

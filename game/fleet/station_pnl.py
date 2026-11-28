#!/usr/bin/env python3
"""Fleet Admiral Station P&L, Venue Unit-Economics, Build Readiness, and Rival Tourism Benchmark.

Read-only analytics over read.db, catalog, empire.json, history.json, and onetime.json,
plus a thin trigger wrapper for wallet.serve_station_builds() via collective_mcp.py.
Pure 7-bit ASCII.

Usage:
    python3 game/fleet/station_pnl.py [summary|venues|builds|rivals|all|build_run] [--station NAME] [--dry] [--json]
"""

import argparse
import json
import sqlite3
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import division  # noqa: E402

CYCLES_PER_DAY = 86.0
CYCLES_PER_H = CYCLES_PER_DAY / 24.0
TREASURY_DEP = "Faction treasury: credits deposited"
TREASURY_FUND = "Treasury fund: credits withdrawn"
TREASURY_CAPEX = "Treasury CapEx:"
TREASURY_CAPITAL = "Treasury capital:"


def _load_catalog_facilities(data_dir):
    cat_dir = Path(data_dir) / "catalog"
    if not cat_dir.is_dir():
        return {}
    for cf in sorted(cat_dir.glob("*.json"), reverse=True):
        if cf.stem == "releases":
            continue
        try:
            cd = json.loads(cf.read_text(encoding="utf-8", errors="replace"))
        except (OSError, ValueError):
            continue
        if isinstance(cd, dict):
            fl = cd.get("facilities")
            if isinstance(fl, dict):
                return fl
            if isinstance(fl, list):
                return {str(x.get("id")): x for x in fl if isinstance(x, dict) and x.get("id")}
    return {}


def _forensic_station_revenue(data_dir, npc_rent_h, own_labor_h):
    h_p = Path(data_dir) / "fleet" / "history.json"
    ot_p = Path(data_dir) / "fleet" / "onetime.json"
    if not h_p.exists():
        return {}
    try:
        hist = json.loads(h_p.read_text(encoding="utf-8", errors="replace"))
        one = json.loads(ot_p.read_text(encoding="utf-8", errors="replace")) if ot_p.exists() else []
    except (OSError, ValueError):
        return {}
    tr_pts = [(r[0], r[8]["t"][0], r[8]["t"][1]) for r in hist if isinstance(r, list) and len(r) > 8 and isinstance(r[8], dict) and "t" in r[8]]
    if len(tr_pts) < 2:
        return {}
    _, end_cr, end_ts = tr_pts[-1]
    out = {}
    for hrs in (1, 3, 6, 24):
        cands = [p for p in tr_pts if p[2] <= end_ts - hrs * 3600]
        if not cands:
            continue
        _, start_cr, start_ts = cands[-1]
        span_h = max(0.05, (end_ts - start_ts) / 3600.0)
        landed = sum(-float(r[3]) for r in one if isinstance(r, list) and len(r) == 4 and start_ts < r[0] <= end_ts
                     and (str(r[2]).startswith(TREASURY_DEP) or str(r[2]).startswith(TREASURY_FUND)))
        own = (end_cr - start_cr) - landed
        capex = sum(float(r[3]) for r in one if isinstance(r, list) and len(r) == 4 and start_ts < r[0] <= end_ts
                    and (str(r[2]).startswith(TREASURY_CAPEX) or (str(r[1]) == "__TREASURY__" and not str(r[2]).startswith(TREASURY_CAPITAL))))
        capital = sum(float(r[3]) for r in one if isinstance(r, list) and len(r) == 4 and start_ts < r[0] <= end_ts
                      and str(r[2]).startswith(TREASURY_CAPITAL))
        net_ops_h = (own - capex - capital) / span_h
        gross_rev_h = max(0.0, net_ops_h + abs(npc_rent_h) + abs(own_labor_h))
        out[f"{hrs}h"] = {"span_h": round(span_h, 2), "net_ops_h": round(net_ops_h), "gross_rev_h": round(gross_rev_h)}
    return out


def _open_db(data_dir):
    db_p = Path(data_dir) / "store" / "read.db"
    return sqlite3.connect(f"file:{db_p}?mode=ro", uri=True)


def compute_station_pnl(data_dir=None, station_filter=""):
    data_dir = str(data_dir or division.DATA)
    db = _open_db(data_dir)
    cat = _load_catalog_facilities(data_dir)

    best_bid = {}
    min_ask = {}
    for item, bid, ask in db.execute("SELECT item, MAX(CASE WHEN bid_qty > 0 THEN bid END), MIN(CASE WHEN ask_qty > 0 THEN ask END) FROM books GROUP BY item").fetchall():
        if bid:
            best_bid[item] = float(bid)
        if ask:
            min_ask[item] = float(ask)
    fair_map = {}
    try:
        for item, fp in db.execute("SELECT item, fair_price FROM fair_prices").fetchall():
            if fp:
                fair_map[item] = float(fp)
    except sqlite3.OperationalError:
        pass

    npc_rent_cycle = sum(float(r[0] or 0) for r in db.execute("SELECT rent_per_cycle FROM faction_facilities WHERE rent_per_cycle > 0").fetchall())
    npc_rent_h = npc_rent_cycle * CYCLES_PER_H

    bases = db.execute("SELECT base, name, system, kind FROM bases WHERE kind='station' ORDER BY name").fetchall()
    if station_filter:
        sf = station_filter.lower()
        bases = [b for b in bases if sf in str(b[0]).lower() or sf in str(b[1]).lower() or sf in str(b[2]).lower()]

    appeal_lb = {}
    for name, rank, val in db.execute("SELECT name, rank, value FROM leaderboards WHERE grp='stations' AND board='tourism_appeal'").fetchall():
        appeal_lb[str(name).lower()] = {"rank": int(rank or 0), "appeal": int(val or 0)}

    own_labor_all_h = 0.0
    stations_out = []
    for base_id, base_name, sys_id, kind in bases:
        inv = {r[0]: int(r[1] or 0) for r in db.execute("SELECT item, units FROM faction_storage WHERE base=?", (base_id,)).fetchall()}
        facs = db.execute("SELECT type, name, status FROM faction_facilities WHERE base=? ORDER BY type", (base_id,)).fetchall()
        labor_cycle = 0.0
        full_bid_h = 0.0
        full_ask_h = 0.0
        full_fair_h = 0.0
        live_bid_h = 0.0
        live_ask_h = 0.0
        built_appeal = 0
        venues = []
        for ftype, fname, fstat in facs:
            if str(fstat or "active").lower() not in ("active", "online", "running", "operational"):
                continue
            cf = cat.get(ftype) or {}
            lab = float(cf.get("labor_cost") or 0)
            labor_cycle += lab
            appeal = int(cf.get("dining_points") or 0) + int(cf.get("leisure_points") or 0) + int(cf.get("appeal") or cf.get("tourism_appeal") or 0)
            built_appeal += appeal
            inputs = {}
            for k in ("maintenance_inputs", "tourism_upkeep"):
                u = cf.get(k)
                if isinstance(u, dict):
                    for iid, iq in u.items():
                        inputs[iid] = inputs.get(iid, 0.0) + float(iq or 0)
                elif isinstance(u, list):
                    for row in u:
                        if isinstance(row, dict):
                            iid = str(row.get("item_id") or row.get("item") or "")
                            iq = float(row.get("quantity") or row.get("units") or 0)
                            if iid and iq > 0:
                                inputs[iid] = inputs.get(iid, 0.0) + iq
            v_bid_h = 0.0
            v_ask_h = 0.0
            v_fair_h = 0.0
            stocked = True
            missing = []
            for iid, iq in inputs.items():
                pb = best_bid.get(iid) or fair_map.get(iid) or 0.0
                pa = min_ask.get(iid) or pb
                pf = fair_map.get(iid) or pb
                ib = iq * pb * CYCLES_PER_H
                ia = iq * pa * CYCLES_PER_H
                v_bid_h += ib
                v_ask_h += ia
                v_fair_h += iq * pf * CYCLES_PER_H
                if inv.get(iid, 0) >= iq:
                    live_bid_h += ib
                    live_ask_h += ia
                else:
                    stocked = False
                    missing.append(iid)
            full_bid_h += v_bid_h
            full_ask_h += v_ask_h
            full_fair_h += v_fair_h
            if appeal > 0:
                venues.append({
                    "type": ftype, "name": fname or ftype, "appeal": appeal,
                    "stocked": stocked, "missing": missing[:4],
                    "bid_opp_h": round(v_bid_h), "ask_cost_h": round(v_ask_h),
                    "cr_h_per_appeal": round(v_bid_h / max(1, appeal)),
                })
        labor_h = labor_cycle * CYCLES_PER_H
        own_labor_all_h += labor_h
        venues.sort(key=lambda x: x["cr_h_per_appeal"])
        lb_info = appeal_lb.get(str(base_name).lower()) or {}
        stations_out.append({
            "base": base_id, "name": base_name, "system": sys_id,
            "facilities_active": len(facs),
            "built_appeal": built_appeal,
            "live_appeal": lb_info.get("appeal"),
            "live_appeal_rank": lb_info.get("rank"),
            "labor_h": round(labor_h),
            "live_stocked_bid_h": round(live_bid_h),
            "live_stocked_ask_h": round(live_ask_h),
            "live_total_econ_cost_h": round(labor_h + live_bid_h),
            "full_bid_opp_h": round(full_bid_h),
            "full_ask_cost_h": round(full_ask_h),
            "full_fair_h": round(full_fair_h),
            "full_total_econ_cost_h": round(labor_h + full_bid_h),
            "venues": venues,
        })

    forensic = _forensic_station_revenue(data_dir, npc_rent_h, own_labor_all_h)

    fac_row = db.execute("SELECT treasury, member_count, members_limit FROM faction LIMIT 1").fetchone()
    treasury = int(fac_row[0] or 0) if fac_row else 0
    mem_cnt = int(fac_row[1] or 0) if fac_row else 0
    mem_cap = int(fac_row[2] or 0) if fac_row else 0
    builds_out = []
    if stations_out:
        r_id = stations_out[0]["base"]
        r_inv = {r[0]: int(r[1] or 0) for r in db.execute("SELECT item, units FROM faction_storage WHERE base=?", (r_id,)).fetchall()}
        all_inv = {r[0]: int(r[1] or 0) for r in db.execute("SELECT item, SUM(units) FROM faction_storage GROUP BY item").fetchall()}
        built_types = {r[0] for r in db.execute("SELECT type FROM faction_facilities WHERE base=?", (r_id,)).fetchall()}
        # Mark superseded ancestors as satisfied once a higher upgrade in the chain is built (e.g. guild_hall_recruiting supersedes desk/center).
        upg_parent = {
            str(r[0]): str(r[1])
            for r in db.execute("SELECT id, upgrades_from FROM facilities WHERE upgrades_from IS NOT NULL AND upgrades_from != ''").fetchall()
        }
        satisfied_types = set(built_types)
        for bt in list(built_types):
            cur_f = bt
            while cur_f in upg_parent and upg_parent[cur_f] not in satisfied_types:
                cur_f = upg_parent[cur_f]
                satisfied_types.add(cur_f)
        for fid in ("refueling_dock", "recruitment_desk", "recruitment_center", "guild_hall_recruiting", "fuel_tank_expansion"):
            if fid in satisfied_types and fid != "fuel_tank_expansion":
                continue
            row = db.execute("SELECT name, build_cost, upgrades_from, faction_cap FROM facilities WHERE id=?", (fid,)).fetchone()
            if not row:
                continue
            mats = db.execute("SELECT item, units FROM facility_materials WHERE facility=?", (fid,)).fetchall()
            mat_gaps = []
            ready_mats = True
            for it, need_u in mats:
                have = r_inv.get(it, 0)
                gap = max(0, int(need_u) - have)
                if gap > 0:
                    ready_mats = False
                mat_gaps.append({"item": it, "have": have, "need": int(need_u), "gap": gap,
                                 "cltv_other_lockboxes": max(0, all_inv.get(it, 0) - have),
                                 "min_ask": round(min_ask.get(it, 0))})
            upg_from = row[2]
            upg_ok = (not upg_from) or (upg_from in built_types)
            fee = int(row[1] or 0)
            builds_out.append({
                "facility": fid, "name": row[0], "fee_cr": fee, "cash_ok": treasury >= fee,
                "upgrades_from": upg_from, "prereq_ok": upg_ok, "mats_ok": ready_mats,
                "ready_now": bool(treasury >= fee and upg_ok and ready_mats),
                "materials": mat_gaps,
            })

    rivals_out = []
    has_ts = db.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='tourism_snapshots'").fetchone()
    rows = []
    if has_ts:
        rows = db.execute("SELECT station, system, rank, value, t FROM tourism_snapshots WHERE board='tourism_revenue' ORDER BY t ASC").fetchall()
    if not rows:
        hp = Path(data_dir) / "station" / "tourism_history.jsonl"
        if hp.exists():
            for ln in hp.read_text(encoding="utf-8", errors="replace").splitlines():
                if not ln.strip():
                    continue
                try:
                    o = json.loads(ln)
                    if o.get("board") == "tourism_revenue":
                        rows.append((o.get("station"), o.get("system"), o.get("rank"), o.get("value"), o.get("t")))
                except ValueError:
                    pass
    if rows:
        by_st = {}
        for st, sy, rk, val, ts in rows:
            by_st.setdefault(st, []).append((int(ts or 0), int(val or 0), int(rk or 0), str(sy or "")))
        for st, pts in by_st.items():
            pts.sort()
            t1, v1, r1, sy1 = pts[-1]
            cr_h = None
            span_h = 0.0
            if len(pts) >= 2:
                t0, v0, _, _ = pts[0]
                if t1 > t0 + 1800:
                    span_h = (t1 - t0) / 3600.0
                    cr_h = round((v1 - v0) / span_h)
            ap = appeal_lb.get(st.lower()) or {}
            rivals_out.append({
                "rank": r1, "station": st, "system": sy1,
                "lifetime_cr": v1, "appeal": ap.get("appeal"),
                "cr_h": cr_h, "cr_day": (cr_h * 24) if cr_h is not None else None,
                "span_h": round(span_h, 1), "samples": len(pts),
            })
        rivals_out.sort(key=lambda x: (x["rank"] or 999, -x["lifetime_cr"]))

    db.close()
    return {
        "treasury_cr": treasury, "members": mem_cnt, "members_limit": mem_cap,
        "npc_rent_h": round(npc_rent_h), "forensic_revenue": forensic,
        "stations": stations_out, "builds": builds_out, "rivals": rivals_out[:25],
    }


def format_report(res, view="all"):
    lines = []
    lines.append(f"STATION P&L & TOURISM BRIEFING | Treasury={res['treasury_cr']:,} cr | Seats={res['members']}/{res['members_limit']} | Total NPC Rent=-{res['npc_rent_h']:,} cr/h")
    if view in ("summary", "all"):
        lines.append("\n[1] OWNED STATION UNIT ECONOMICS")
        for w, v in res.get("forensic_revenue", {}).items():
            lines.append(f"  Forensic Treasury Station Rev ({w}, span={v['span_h']}h): gross=+{v['gross_rev_h']:,} cr/h | net_ops={v['net_ops_h']:+,} cr/h")
        for s in res.get("stations", []):
            g1 = (res.get("forensic_revenue", {}).get("1h") or res.get("forensic_revenue", {}).get("6h") or {}).get("gross_rev_h", 0)
            net_now = g1 - s["live_total_econ_cost_h"]
            lines.append(f"  {s['name']} ({s['system']}): {s['facilities_active']} fac | Appeal={s['live_appeal']} live (#{s['live_appeal_rank']}) / {s['built_appeal']} built")
            lines.append(f"    Cash Labor: -{s['labor_h']:,} cr/h | Live Stocked Cost (sell-bid opp): -{s['live_stocked_bid_h']:,}/h (total -{s['live_total_econ_cost_h']:,}/h -> Est Net Now: {net_now:+,} cr/h)")
            lines.append(f"    Full 100%-Stocked Cost: -{s['full_bid_opp_h']:,}/h sell-bid opp | -{s['full_ask_cost_h']:,}/h buy-ask | -{s['full_fair_h']:,}/h fair (total -{s['full_total_econ_cost_h']:,}/h)")
    if view in ("venues", "all"):
        lines.append("\n[2] PER-VENUE ROI RANKING (CHEAPEST CR/H PER APPEAL FIRST)")
        for s in res.get("stations", []):
            for v in s.get("venues", []):
                st = "STOCKED" if v["stocked"] else ("STARVED:" + ",".join(v["missing"]))
                lines.append(f"  {v['name']:26s} | +{v['appeal']:2d} App | {v['bid_opp_h']:>6,d} cr/h ({v['cr_h_per_appeal']:>5,d}/App) | {st}")
    if view in ("builds", "all"):
        lines.append("\n[3] STATION BUILD READINESS MATRIX")
        for b in res.get("builds", []):
            tag = "READY" if b["ready_now"] else ("WAIT_CASH" if not b["cash_ok"] else ("WAIT_PREREQ" if not b["prereq_ok"] else "WAIT_MATS"))
            gaps = ", ".join(f"{m['item']} {m['have']}/{m['need']} (other_lb={m['cltv_other_lockboxes']}, ask={m['min_ask']})" for m in b["materials"])
            lines.append(f"  [{tag:11s}] {b['facility']:24s} | fee={b['fee_cr']:>9,d} cr | {gaps}")
    if view in ("rivals", "all"):
        lines.append("\n[4] TOP GALACTIC TOURISM STATIONS (HOURLY SNAPSHOT DELTA LEDGER)")
        for r in res.get("rivals", [])[:15]:
            rate = f"+{r['cr_h']:,} cr/h (+{r['cr_day']:,}/day, {r['span_h']}h)" if r["cr_h"] is not None else f"awaiting 2nd snapshot (n={r['samples']})"
            ap = f"App={r['appeal']}" if r["appeal"] is not None else "App=-"
            lines.append(f"  #{r['rank']:2d} {r['station']:28s} ({r['system']:14s}) | {ap:6s} | cum={r['lifetime_cr']:>13,d} cr | {rate}")
    return "\n".join(lines)


def main(argv=None):
    p = argparse.ArgumentParser(description="Station P&L, venue ROI, build readiness, and rival tourism telemetry.")
    p.add_argument("view", nargs="?", default="all", choices=("summary", "venues", "builds", "rivals", "all", "build_run"))
    p.add_argument("--station", default="")
    p.add_argument("--dry", action="store_true")
    p.add_argument("--json", action="store_true")
    args = p.parse_args(argv)
    if args.view == "build_run":
        import wallet
        rc = wallet.serve_station_builds(str(division.DATA), time.time(), dry=args.dry)
        print(f"station_build finished (dry={args.dry}, rc={rc})")
        return int(rc or 0)
    res = compute_station_pnl(station_filter=args.station)
    if args.json:
        print(json.dumps(res, indent=2))
    else:
        print(format_report(res, args.view))
    return 0


if __name__ == "__main__":
    sys.exit(main())

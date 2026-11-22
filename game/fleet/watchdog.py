#!/usr/bin/env python3
"""Check whether the fleet is advancing across turns or stuck in loops, bottlenecks, or idle states.

Run by hand.

Usage:
    watchdog.py [show] [--hours N] [--json] [--save] [--data <dir>] [--root <dir>]
    watchdog.py check [--hours N] [--data <dir>] [--root <dir>]
    --hours N      window for run-loop and log checks (default 4)
    --json         print structured JSON instead of plain text
    --save         update <data>/fleet/watchdog.state.json for cross-turn velocity tracking
    --data <dir>   the unit's data folder (default /srv/collective/data)
    --root <dir>   the repository's game/ folder (default: the parent of this file's folder)
"""

from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import sqlite3
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))
import division  # noqa: E402
import workclass  # noqa: E402

CORE_SERVICES = (
    "fleet",
    "dispatch",
    "runhost",
    "store",
    "ledger",
    "routemaker",
    "inbox",
    "sight",
    "station",
    "keeper",
)
STATE_REL = ("fleet", "watchdog.state.json")
ENT_RE = re.compile(
    r"^## \[(ENT-\d+)\]\s*\|\s*(\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}(?::\d{2})?)\s*UTC\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)(?:\s*\|(.*))?$"
)


def _utc_iso(ts):
    return datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _parse_utc(text):
    text = text.strip()
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%dT%H:%M:%S"):
        try:
            return datetime.strptime(text, fmt).replace(tzinfo=timezone.utc).timestamp()
        except ValueError:
            pass
    return 0.0


def _connect_ro(db_path):
    if not db_path.exists():
        return None
    con = sqlite3.connect("file:%s?mode=ro" % db_path, uri=True, timeout=5.0)
    con.row_factory = sqlite3.Row
    return con


def _percentile(sorted_vals, pct):
    if not sorted_vals:
        return 0.0
    idx = min(len(sorted_vals) - 1, max(0, int(round((len(sorted_vals) - 1) * pct))))
    return float(sorted_vals[idx])


def _scan_requests_and_errors(repo_root, now, hours):
    comms = Path(repo_root) / "communications"
    open_reqs = []
    closed_ids = set()
    req_file = comms / "requests.log"
    if req_file.exists():
        entries = []
        cur = None
        for line in req_file.read_text(encoding="utf-8", errors="replace").splitlines():
            m = ENT_RE.match(line)
            if m:
                if cur:
                    entries.append(cur)
                cur = {
                    "id": m.group(1),
                    "ts": _parse_utc(m.group(2)),
                    "author": m.group(3).strip(),
                    "kind": m.group(4).strip(),
                    "rest": (m.group(5) or "").strip(),
                    "body": [],
                }
            elif cur is not None:
                cur["body"].append(line)
        if cur:
            entries.append(cur)
        for e in entries:
            full = e["rest"] + "\n" + "\n".join(e["body"])
            if e["kind"] in ("answer", "done", "closed", "close"):
                for ref in re.findall(r"\bENT-\d+\b", full):
                    closed_ids.add(ref)
            for m_st in re.finditer(r"(?im)^status:\s*(closed|done|dropped|answered)\b", full):
                closed_ids.add(e["id"])
        for e in entries:
            if e["kind"] == "request" and e["id"] not in closed_ids:
                to_m = re.search(r"@([A-Za-z]+)", e["rest"] + " " + " ".join(e["body"][:3]))
                age_h = max(0.0, (now - e["ts"]) / 3600.0) if e["ts"] else 0.0
                open_reqs.append({
                    "id": e["id"],
                    "from": e["author"],
                    "to": to_m.group(1) if to_m else "unknown",
                    "age_h": round(age_h, 1),
                })

    recent_errors = []
    err_file = comms / "errors.log"
    cutoff = now - hours * 3600.0
    if err_file.exists():
        for line in err_file.read_text(encoding="utf-8", errors="replace").splitlines():
            m = ENT_RE.match(line)
            if m:
                ts = _parse_utc(m.group(2))
                if ts >= cutoff:
                    recent_errors.append({
                        "id": m.group(1),
                        "author": m.group(3).strip(),
                        "kind": m.group(4).strip(),
                        "age_h": round(max(0.0, (now - ts) / 3600.0), 1),
                    })
    return open_reqs, recent_errors


def inspect(root, data, hours=4.0, now=None, save=False):
    """Compute deterministic loop, bottleneck, readiness, and cross-turn velocity findings."""
    now = float(now if now is not None else time.time())
    game_root = Path(root).resolve()
    repo_root = game_root.parent if game_root.name == "game" else game_root
    if (repo_root / "game").is_dir():
        game_root = repo_root / "game"
    data_dir = Path(data).resolve()
    state_path = data_dir.joinpath(*STATE_REL)

    findings = []

    def add_finding(level, area, code, summary, detail=""):
        findings.append({
            "level": level,
            "area": area,
            "code": code,
            "summary": summary,
            "detail": detail,
        })

    # 1. Services health
    svc_path = (data_dir / "services" / "status.json") if (data_dir / "services" / "status.json").exists() else (data_dir.parent / "services" / "status.json")
    down_services = []
    running_services = 0
    if svc_path.exists():
        try:
            raw_svc = json.loads(svc_path.read_text(encoding="utf-8"))
            svcs = raw_svc.get("services") if isinstance(raw_svc, dict) and "services" in raw_svc else raw_svc
            if isinstance(svcs, dict):
                for name in CORE_SERVICES:
                    info = svcs.get(name) or {}
                    st = info.get("state") or info.get("status") or ("running" if info.get("running") else "down")
                    if st == "running":
                        running_services += 1
                    else:
                        down_services.append("%s(%s)" % (name, st))
            elif isinstance(svcs, list):
                by_name = {x.get("name"): x for x in svcs if isinstance(x, dict)}
                for name in CORE_SERVICES:
                    info = by_name.get(name) or {}
                    st = info.get("state") or info.get("status") or ("running" if info.get("running") else "down")
                    if st == "running":
                        running_services += 1
                    else:
                        down_services.append("%s(%s)" % (name, st))
        except Exception as exc:
            add_finding("WARN", "services", "STATUS_READ_ERR", "Could not parse services/status.json: %s" % exc)
    if down_services:
        add_finding("STUCK", "services", "SERVICE_DOWN", "Core services not running: " + ", ".join(down_services))

    con = _connect_ro(data_dir / "store" / "read.db")
    if con is None:
        add_finding("STUCK", "store", "NO_READ_DB", "SQLite store read.db is missing at %s" % (data_dir / "store" / "read.db"))
        return {
            "at": _utc_iso(now),
            "epoch": int(now),
            "status": "STUCK",
            "hours": hours,
            "findings": findings,
            "snapshot": {},
            "velocity": None,
        }

    try:
        tables = {r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type IN ('table','view')")}

        # 2. Ships, tick lag & S5 idle compliance
        ships = list(con.execute("SELECT * FROM ships")) if "ships" in tables else []
        ages = sorted(max(0.0, now - float(s["t"])) for s in ships if s["t"])
        tick_med = round(_percentile(ages, 0.50), 1)
        tick_p95 = round(_percentile(ages, 0.95), 1)
        tick_max = round(_percentile(ages, 1.00), 1)
        if ships and tick_p95 > 180.0:
            add_finding("STUCK", "tick", "TICK_LAG_HIGH", "Pilot state p95 age is %.1fs (>180s)" % tick_p95)
        elif ships and tick_p95 > 75.0:
            add_finding("WARN", "tick", "TICK_LAG_WARN", "Pilot state p95 age is %.1fs (>75s)" % tick_p95)

        div_totals = {}
        div_idle = {}
        wallet_sum = 0
        t2_hulls = 0
        low_wallet_ships = []
        for s in ships:
            div = s["division"] or s["role"] or "unknown"
            div_totals[div] = div_totals.get(div, 0) + 1
            wallet_sum += int(s["credits"] or 0)
            if (s["class"] or "Threshold") != "Threshold":
                t2_hulls += 1
            if int(s["credits"] or 0) < 3000:
                low_wallet_ships.append("%s(%dcr)" % (s["pilot"], int(s["credits"] or 0)))
            flies = (s["flies"] or "").strip()
            act = (s["activity"] or "").strip().lower()
            st = (s["status"] or "").strip().lower()
            is_idle = (not flies) or st in ("idle", "waiting", "parked") or act in ("idle", "none", "parked")
            if is_idle:
                div_idle[div] = div_idle.get(div, 0) + 1

        total_ships = len(ships)
        total_idle = sum(div_idle.values())
        if total_idle >= 10:
            detail = ", ".join("%s:%d/%d" % (d, c, div_totals.get(d, 0)) for d, c in sorted(div_idle.items()) if c > 0)
            add_finding("STUCK", "s5_idle", "FLEET_IDLE_S5", "%d/%d ships idle/unassigned (%s)" % (total_idle, total_ships, detail))
        else:
            for d, c in sorted(div_idle.items()):
                tot = max(1, div_totals.get(d, 1))
                if c >= 4 and (c / float(tot)) > 0.10:
                    add_finding("STUCK", "s5_idle", "DIV_IDLE_S5", "Division %s has %d/%d idle ships" % (d, c, tot))
                elif c >= 2:
                    add_finding("WARN", "s5_idle", "DIV_WAIT_S5", "Division %s has %d/%d ships between runs or waiting" % (d, c, tot))

        if low_wallet_ships:
            add_finding("WARN", "wallets", "WALLET_UNDER_FLOOR", "%d ship(s) under 3,000 cr F7 floor: %s" % (len(low_wallet_ships), ", ".join(low_wallet_ships[:6])))

        # 3. Zero-credit & fast-fail loop detector (runs table)
        cutoff = int(now - hours * 3600.0)
        fast_loops = []
        loss_loops = []
        churn_pilots = []
        if "runs" in tables:
            route_rows = con.execute(
                """
                SELECT route, kind, COUNT(*) AS n, AVG(minutes) AS avg_m,
                       SUM(credits) AS sum_cr, COUNT(DISTINCT pilot) AS pilots
                FROM runs
                WHERE t >= ? AND kind NOT IN ('census', 'guard')
                GROUP BY route, kind
                """,
                (cutoff,),
            ).fetchall()
            for r in route_rows:
                n = int(r["n"] or 0)
                avg_m = float(r["avg_m"] or 0.0)
                sum_cr = float(r["sum_cr"] or 0.0)
                if n >= 4 and avg_m < 1.5 and sum_cr <= 0.0:
                    fast_loops.append({
                        "route": r["route"],
                        "kind": r["kind"],
                        "runs": n,
                        "avg_min": round(avg_m, 2),
                        "net_cr": int(round(sum_cr)),
                        "pilots": int(r["pilots"] or 0),
                    })
                elif n >= 3 and sum_cr < -2500.0 and not (r["route"] or "").startswith(("train-", "gather-", "fit-", "buy-", "build-", "found-", "give-", "haul-fuel-", "supply-")):
                    loss_loops.append({
                        "route": r["route"],
                        "runs": n,
                        "avg_min": round(avg_m, 2),
                        "net_cr": int(round(sum_cr)),
                    })

            pilot_rows = con.execute(
                """
                SELECT r.pilot, COALESCE(s.role, '') AS role, COUNT(*) AS n,
                       AVG(r.minutes) AS avg_m, SUM(r.credits) AS sum_cr
                FROM runs r
                LEFT JOIN ships s ON s.pilot = r.pilot
                WHERE r.t >= ? AND r.kind NOT IN ('census', 'guard')
                GROUP BY r.pilot
                HAVING COUNT(*) >= 10 AND AVG(r.minutes) < 1.5 AND SUM(r.credits) <= 0
                """,
                (cutoff,),
            ).fetchall()
            for pr in pilot_rows:
                if pr["role"] != "scout":
                    churn_pilots.append("%s(%dr,%.1fm,%dcr)" % (pr["pilot"], pr["n"], pr["avg_m"] or 0.0, int(pr["sum_cr"] or 0)))

        fast_loops.sort(key=lambda x: (-x["runs"], x["net_cr"]))
        loss_loops.sort(key=lambda x: x["net_cr"])
        if any(x["runs"] >= 10 for x in fast_loops):
            top = ", ".join("%s(%dx,%.2fm,%dcr)" % (x["route"], x["runs"], x["avg_min"], x["net_cr"]) for x in fast_loops[:4])
            add_finding("STUCK", "loops", "FAST_ZERO_LOOP", "%d route(s) in fast zero-credit loop: %s" % (len(fast_loops), top))
        elif fast_loops:
            top = ", ".join("%s(%dx,%.2fm,%dcr)" % (x["route"], x["runs"], x["avg_min"], x["net_cr"]) for x in fast_loops[:4])
            add_finding("WARN", "loops", "FAST_ZERO_WARN", "%d route(s) had >=4 short <=0cr runs in %.0fh: %s" % (len(fast_loops), hours, top))

        if any(x["net_cr"] <= -10000 for x in loss_loops):
            top = ", ".join("%s(%dx,%dcr)" % (x["route"], x["runs"], x["net_cr"]) for x in loss_loops[:4])
            add_finding("STUCK", "loops", "ROUTE_BLEED", "Heavy negative-credit route(s) in %.0fh: %s" % (hours, top))
        elif loss_loops:
            top = ", ".join("%s(%dx,%dcr)" % (x["route"], x["runs"], x["net_cr"]) for x in loss_loops[:4])
            add_finding("WARN", "loops", "ROUTE_LOSS", "Negative-credit route(s) in %.0fh: %s" % (hours, top))

        if churn_pilots:
            add_finding("WARN", "loops", "PILOT_CHURN", "Pilot(s) churning >=10 short <=0cr runs: " + ", ".join(churn_pilots[:5]))

        # 4. Faction cap, treasury, KPI & priority needs
        fac = con.execute("SELECT * FROM faction LIMIT 1").fetchone() if "faction" in tables else None
        treasury = int(fac["treasury"] or 0) if fac else 0
        member_count = int(fac["member_count"] or 0) if fac else 0
        members_limit = int(fac["members_limit"] or 0) if fac else 0
        owned_bases = int(fac["owned_bases"] or 0) if fac else 0
        facilities_n = int(con.execute("SELECT COUNT(*) FROM faction_facilities").fetchone()[0]) if "faction_facilities" in tables else 0
        systems_read = int(con.execute("SELECT COUNT(DISTINCT system) FROM places").fetchone()[0]) if "places" in tables else 0

        open_seats = max(0, min(total_ships, members_limit) - member_count) if members_limit > 0 else 0
        if members_limit > 0 and member_count >= members_limit - 2:
            add_finding("WARN", "empire", "FACTION_CAP_NEAR", "Faction seats at %d/%d (%d/%d fleet ships seated; treasury %s cr)" % (member_count, members_limit, member_count, total_ships, format(treasury, ",")))
        elif open_seats >= 2:
            add_finding("WARN", "empire", "OPEN_FACTION_SEATS", "%d open faction seat(s) ready to fill (%d/%d cap, %d/%d fleet ships seated; rule F11)" % (open_seats, member_count, members_limit, member_count, total_ships))

        steady_1h = steady_24h = None
        if "stats_figures" in tables:
            for r in con.execute("SELECT hours, value FROM stats_figures WHERE view='kpi' AND LOWER(subject)='fleet' AND figure IN ('net', 'steady_net_per_hour')"):
                if int(round(float(r["hours"] or 0))) == 1:
                    steady_1h = float(r["value"] or 0.0)
                elif int(round(float(r["hours"] or 0))) == 24:
                    steady_24h = float(r["value"] or 0.0)
        if steady_24h is not None and steady_24h < 0:
            add_finding("STUCK", "economy", "NEGATIVE_STEADY_24H", "24h steady net/h is negative (%s cr/h)" % format(int(round(steady_24h)), ","))

        open_needs = []
        if "need_status" in tables:
            for n in con.execute("SELECT * FROM need_status WHERE stands = 0 AND priority <= 2 ORDER BY priority, rank"):
                cov = round(float(n["covered"] or 0.0) * 100.0 if float(n["covered"] or 0.0) <= 1.0 else float(n["covered"] or 0.0), 2)
                fee = int(n["fee"] or 0)
                item = {
                    "id": n["id"],
                    "priority": int(n["priority"] or 2),
                    "division": n["division"],
                    "kind": n["kind"],
                    "ref": n["ref"],
                    "covered_pct": cov,
                    "fee": fee,
                    "short_items": (n["short_items"] or "")[:120],
                    "gather": (n["gather"] or "")[:80],
                    "buy": (n["buy"] or "")[:80],
                    "craft": (n["craft"] or "")[:80],
                }
                open_needs.append(item)
                if cov >= 99.95 and (fee <= 0 or treasury >= fee):
                    add_finding(
                        "WARN",
                        "needs",
                        "NEED_READY_NOW",
                        "P%d %s (%s) is %.1f%% stocked and treasury (%s cr) covers fee (%s cr) -- ready to execute"
                        % (item["priority"], item["id"], item["ref"], cov, format(treasury, ","), format(fee, ",")),
                    )

        # 5. Upgrades & Tech Progression (Piloting >= 10 / >= 20 vs Tier-0 Threshold)
        p10_total = 0
        p10_threshold = 0
        p10_funded = 0
        p20_threshold = 0
        by_div_upg = {}
        if "ship_skills" in tables and ships:
            pil_map = {
                r["pilot"]: int(r["level"] or 0)
                for r in con.execute("SELECT pilot, level FROM ship_skills WHERE skill = 'piloting'")
            }
            for s in ships:
                lvl = pil_map.get(s["pilot"], 0)
                div = s["division"] or s["role"] or "unknown"
                hull_cls = s["class"] or "Threshold"
                cr = int(s["credits"] or 0)
                d_entry = by_div_upg.setdefault(div, {"ships": 0, "t2_plus": 0, "p10_t0": 0, "p10_funded_t0": 0, "p20_t0": 0})
                d_entry["ships"] += 1
                if hull_cls != "Threshold":
                    d_entry["t2_plus"] += 1
                if lvl >= 10:
                    p10_total += 1
                    if hull_cls == "Threshold":
                        p10_threshold += 1
                        d_entry["p10_t0"] += 1
                        if cr >= 45000:
                            p10_funded += 1
                            d_entry["p10_funded_t0"] += 1
                if lvl >= 20 and hull_cls == "Threshold":
                    p20_threshold += 1
                    d_entry["p20_t0"] += 1

        fitted_modules = int(con.execute("SELECT COUNT(*) FROM ship_modules").fetchone()[0]) if "ship_modules" in tables else 0
        if p20_threshold >= 5 or p10_funded >= 20:
            add_finding(
                "WARN",
                "upgrades",
                "T0_HULL_BACKLOG",
                "%d/%d ships on T2+ hulls; %d Piloting>=10 (%d with >=45k cr, %d Piloting>=20) still fly Tier-0 Threshold"
                % (t2_hulls, total_ships, p10_threshold, p10_funded, p20_threshold),
            )

        # 6. Strict-classes P5 readiness
        strict_is_on = False
        strict_sales_n = 0
        strict_by_admiral = {}
        try:
            workclass.follow(str(data_dir))
            strict_is_on = bool(workclass.strict_on())
            wc_routes = workclass.load()
            wc_plans = workclass.role_plans()
            s_rows, _by_cls, by_adm = workclass.sales(wc_routes, wc_plans)
            strict_sales_n = len(s_rows)
            strict_by_admiral = dict(sorted(by_adm.items()))
            if not strict_is_on and strict_sales_n == 0:
                add_finding("WARN", "strict_p5", "STRICT_READY_TO_FLIP", "0 non-trader selling routes remain in plans -- strict-classes-on is ready to enable (P5)")
        except Exception as exc:
            add_finding("WARN", "strict_p5", "WORKCLASS_ERR", "workclass check error: %s" % exc)

        # 7. Supply chains, MAD alerts & Comms health
        supply_crit = []
        supply_low = []
        if "supply_status" in tables:
            for sc in con.execute("SELECT chain, place, status, stock, keep, hours_left FROM supply_status"):
                st = (sc["status"] or "").upper()
                if st in ("SHORT", "LOW"):
                    stock_v = float(sc["stock"] or 0.0)
                    keep_v = max(1.0, float(sc["keep"] or 1.0))
                    hl = sc["hours_left"]
                    hl_v = float(hl) if hl not in (None, "") else 999.0
                    tag = "%s@%s(%d/%d)" % (sc["chain"], sc["place"], int(stock_v), int(keep_v))
                    # Operational fuel/bunker critically low (<25% keep or <6h left) = STUCK; routine refill (<keep or unbuilt reserve target) = WARN
                    if st == "SHORT" and ("fuel" in (sc["chain"] or "") or hl_v < 6.0) and (stock_v / keep_v) < 0.25:
                        supply_crit.append(tag)
                    else:
                        supply_low.append(tag)
        if supply_crit:
            add_finding("STUCK", "supply", "SUPPLY_CRITICAL", "Critical supply chain <25%% or <6h: " + ", ".join(supply_crit))
        elif supply_low:
            add_finding("WARN", "supply", "SUPPLY_BELOW_KEEP", "Supply chain below target keep: " + ", ".join(supply_low))

        if "runs" in tables:
            jl = con.execute(
                "SELECT ROUND(SUM(COALESCE(minutes,0))/60.0,1), ROUND(SUM(COALESCE(credits,0))) "
                "FROM runs WHERE route LIKE 'train-jumps-%' AND t > strftime('%s','now') - 14400"
            ).fetchone()
            if jl and (jl[0] or 0) >= 80:
                add_finding("WARN", "efficiency", "JUMP_LOOP_BURN",
                            "Empty jump loops burned %s ship-h (%s cr) in 4h -- shift to Station Bursars / docked craft" % (jl[0], format(int(jl[1] or 0), ",")))
        try:
            import comms_guard
            q_msgs = [r for r in comms_guard.read_comms_rows(Path(data) / "comms" / "messages.jsonl") if r["risk_level"] == "quarantined"]
            if q_msgs:
                add_finding("WARN", "security", "COMMS_QUARANTINED",
                            "%d external message(s) quarantined by comms_guard firewall (newest: %s)" % (len(q_msgs), q_msgs[-1]["sender"]))
        except Exception:
            pass

        mad_out = []
        if "stats_figures" in tables:
            for a in con.execute("SELECT subject, figure, value FROM stats_figures WHERE view='alerts' AND text='OUT'"):
                mad_out.append("%s:%s(%.0f)" % (a["subject"], a["figure"], float(a["value"] or 0.0)))
        if mad_out:
            add_finding("WARN", "alerts", "MAD_CONTROL_OUT", "%d MAD control alert(s) OUT: %s" % (len(mad_out), ", ".join(mad_out[:5])))

        open_reqs, recent_errors = _scan_requests_and_errors(repo_root, now, hours)
        overdue_reqs = [r for r in open_reqs if r["age_h"] > 4.5]
        if overdue_reqs:
            top = ", ".join("%s(%s->%s,%.1fh)" % (r["id"], r["from"], r["to"], r["age_h"]) for r in overdue_reqs[:5])
            add_finding("WARN", "comms", "OVERDUE_REQUESTS", "%d open request(s) older than 4.5h turn cycle: %s" % (len(overdue_reqs), top))
    finally:
        con.close()

    snapshot = {
        "epoch": int(now),
        "at": _utc_iso(now),
        "ships": total_ships,
        "idle_ships": total_idle,
        "t2_hulls": t2_hulls,
        "p10_pilots": p10_total,
        "p10_threshold": p10_threshold,
        "p20_threshold": p20_threshold,
        "fitted_modules": fitted_modules,
        "treasury": treasury,
        "wallets": wallet_sum,
        "total_money": treasury + wallet_sum,
        "steady_1h": round(steady_1h, 1) if steady_1h is not None else None,
        "steady_24h": round(steady_24h, 1) if steady_24h is not None else None,
        "member_count": member_count,
        "members_limit": members_limit,
        "owned_bases": owned_bases,
        "facilities": facilities_n,
        "systems_read": systems_read,
        "strict_on": strict_is_on,
        "strict_sales_left": strict_sales_n,
        "needs": {n["id"]: n["covered_pct"] for n in open_needs},
    }

    # Cross-turn velocity against previous saved snapshot
    velocity = None
    if state_path.exists():
        try:
            prev_doc = json.loads(state_path.read_text(encoding="utf-8"))
            prev = prev_doc.get("baseline") or prev_doc.get("last") or {}
            dt_h = (now - float(prev.get("epoch") or now)) / 3600.0
            if dt_h >= 0.25:
                velocity = {
                    "since": prev.get("at"),
                    "dt_hours": round(dt_h, 2),
                    "d_total_money": snapshot["total_money"] - int(prev.get("total_money") or 0),
                    "d_treasury": snapshot["treasury"] - int(prev.get("treasury") or 0),
                    "d_t2_hulls": snapshot["t2_hulls"] - int(prev.get("t2_hulls") or 0),
                    "d_p10_pilots": snapshot["p10_pilots"] - int(prev.get("p10_pilots") or 0),
                    "d_facilities": snapshot["facilities"] - int(prev.get("facilities") or 0),
                    "d_systems_read": snapshot["systems_read"] - int(prev.get("systems_read") or 0),
                    "d_strict_sales_left": snapshot["strict_sales_left"] - int(prev.get("strict_sales_left") or 0),
                    "need_deltas": {},
                }
                prev_needs = prev.get("needs") or {}
                for n in open_needs:
                    nid = n["id"]
                    if nid in prev_needs:
                        delta_cov = round(n["covered_pct"] - float(prev_needs[nid]), 2)
                        velocity["need_deltas"][nid] = delta_cov
                        if n["priority"] == 1 and n["covered_pct"] < 99.95 and dt_h >= 3.5 and delta_cov < 0.05:
                            lvl = "STUCK" if dt_h >= 8.0 else "WARN"
                            add_finding(
                                lvl,
                                "velocity",
                                "P1_NEED_STALLED",
                                "P1 need %s (%s) moved %+.2f%% over %.1fh (still %.2f%%, short: %s)"
                                % (nid, n["ref"], delta_cov, dt_h, n["covered_pct"], n["short_items"] or "fee/build"),
                            )
        except Exception as exc:
            add_finding("WARN", "velocity", "STATE_READ_ERR", "Could not read watchdog.state.json: %s" % exc)

    if save:
        state_path.parent.mkdir(parents=True, exist_ok=True)
        existing = {}
        if state_path.exists():
            try:
                existing = json.loads(state_path.read_text(encoding="utf-8"))
            except Exception:
                existing = {}
        history = list(existing.get("history") or [])
        history.append(snapshot)
        history = history[-36:]  # keep ~6 days of 4h snapshots
        # Keep a rolling ~4h+ baseline so velocity always compares across a meaningful window
        baseline = history[0]
        for h in reversed(history[:-1]):
            if (now - float(h.get("epoch") or now)) >= 3.5 * 3600.0:
                baseline = h
                break
        out_state = {"last": snapshot, "baseline": baseline, "history": history}
        tmp = state_path.with_suffix(".tmp")
        tmp.write_text(json.dumps(out_state, indent=2) + "\n", encoding="ascii")
        os.replace(tmp, state_path)

    overall = "OK"
    if any(f["level"] == "STUCK" for f in findings):
        overall = "STUCK"
    elif any(f["level"] == "WARN" for f in findings):
        overall = "WARN"

    return {
        "at": _utc_iso(now),
        "epoch": int(now),
        "status": overall,
        "hours": hours,
        "services": {"running": running_services, "total": len(CORE_SERVICES), "down": down_services},
        "tick_lag_s": {"median": tick_med, "p95": tick_p95, "max": tick_max},
        "idle_by_division": div_idle,
        "ships_by_division": div_totals,
        "upgrades_by_division": by_div_upg,
        "fast_loops": fast_loops[:8],
        "loss_loops": loss_loops[:8],
        "open_needs": open_needs[:8],
        "strict_classes": {"on": strict_is_on, "sales_left": strict_sales_n, "by_admiral": strict_by_admiral},
        "comms": {"open_requests": len(open_reqs), "overdue_requests": overdue_reqs, "recent_errors": recent_errors},
        "snapshot": snapshot,
        "velocity": velocity,
        "findings": findings,
    }


def format_report(rep):
    snap = rep.get("snapshot") or {}
    lines = []
    lines.append(
        "WATCHDOG | %s | status=%s | window=%.0fh | services=%d/%d | tick_p95=%.1fs"
        % (
            rep["at"],
            rep["status"],
            rep["hours"],
            rep.get("services", {}).get("running", 0),
            rep.get("services", {}).get("total", 0),
            rep.get("tick_lag_s", {}).get("p95", 0.0),
        )
    )
    if snap:
        s1 = "%s cr/h" % format(int(round(snap["steady_1h"])), ",") if snap.get("steady_1h") is not None else "n/a"
        s24 = "%s cr/h" % format(int(round(snap["steady_24h"])), ",") if snap.get("steady_24h") is not None else "n/a"
        lines.append(
            "EMPIRE   | seats=%d/%d | bases=%d | facilities=%d | systems_read=%d | treasury=%s cr | total=%s cr | steady_1h=%s | steady_24h=%s"
            % (
                snap.get("member_count", 0),
                snap.get("members_limit", 0),
                snap.get("owned_bases", 0),
                snap.get("facilities", 0),
                snap.get("systems_read", 0),
                format(snap.get("treasury", 0), ","),
                format(snap.get("total_money", 0), ","),
                s1,
                s24,
            )
        )
        sc = rep.get("strict_classes") or {}
        adm_s = ", ".join("%s:%d" % kv for kv in (sc.get("by_admiral") or {}).items()) or "none"
        lines.append(
            "PROGRESS | active=%d/%d (idle=%d) | T2+_hulls=%d/%d | P10_on_T0=%d (P20_on_T0=%d) | modules=%d | strict_P5=%s (sales_left=%d: %s)"
            % (
                snap.get("ships", 0) - snap.get("idle_ships", 0),
                snap.get("ships", 0),
                snap.get("idle_ships", 0),
                snap.get("t2_hulls", 0),
                snap.get("ships", 0),
                snap.get("p10_threshold", 0),
                snap.get("p20_threshold", 0),
                snap.get("fitted_modules", 0),
                "ON" if sc.get("on") else "off",
                sc.get("sales_left", 0),
                adm_s,
            )
        )

    vel = rep.get("velocity")
    if vel:
        nd = ", ".join("%s:%+.2f%%" % kv for kv in sorted((vel.get("need_deltas") or {}).items())) or "none"
        lines.append(
            "VELOCITY | dt=%.2fh since %s | money=%+d cr (treasury=%+d) | T2+=%+d | P10=%+d | sys=%+d | strict_sales=%+d | needs=[%s]"
            % (
                vel["dt_hours"],
                vel["since"],
                vel["d_total_money"],
                vel["d_treasury"],
                vel["d_t2_hulls"],
                vel["d_p10_pilots"],
                vel["d_systems_read"],
                vel["d_strict_sales_left"],
                nd,
            )
        )
    else:
        lines.append("VELOCITY | baseline initialized on --save (no prior snapshot >=15m yet)")

    needs = rep.get("open_needs") or []
    if needs:
        lines.append("NEEDS    | open P1/P2 (%d):" % len(needs))
        for n in needs[:6]:
            lines.append(
                "  P%d %-22s %-10s %6.2f%% | fee=%s | short=%s"
                % (
                    n["priority"],
                    n["id"][:22],
                    n["division"][:10],
                    n["covered_pct"],
                    format(n["fee"], ","),
                    n["short_items"] or "none",
                )
            )

    findings = rep.get("findings") or []
    if not findings:
        lines.append("FINDINGS | none -- all checks clean")
    else:
        lines.append("FINDINGS | %d item(s):" % len(findings))
        for f in findings:
            lines.append("  [%-5s] %-10s %-20s %s" % (f["level"], f["area"], f["code"], f["summary"]))
    return "\n".join(lines)


def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)
    if any(a in ("-h", "--help") for a in args):
        print(__doc__.strip())
        return 0
    value = lambda name, default: args[args.index(name) + 1] if name in args and args.index(name) + 1 < len(args) else default
    here = Path(__file__).resolve().parent
    root = value("--root", str(here.parent))
    data = value("--data", division.DATA)
    hours = float(value("--hours", "4"))
    as_json = "--json" in args
    save = "--save" in args
    words = [
        a for i, a in enumerate(args)
        if not a.startswith("--") and (i == 0 or args[i - 1] not in ("--root", "--data", "--hours"))
    ]
    mode = words[0] if words else "show"
    if mode not in ("show", "check"):
        print(__doc__.strip())
        return 2
    rep = inspect(root, data, hours=hours, save=save)
    if as_json:
        print(json.dumps(rep, indent=2))
    else:
        print(format_report(rep))
    if mode == "check" and rep["status"] == "STUCK":
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Division KPI Scorecards, <80% Completion Triggers & Stagnation Detection.

Single source of truth shared by:
  - Every Admiral's & Unity's startup briefing (`hive.py briefing` / `hive.py scorecard`)
  - The Station Command HUD (`/api/ops` -> `scorecard` in the Metrics tab)

Design principles (SRE multi-window burn-rate + AgentOps leading/lagging + anti-alert-fatigue):
  1. Leading vs. lagging indicators: pairs readiness/capability percentages (employment,
     role- & empire-aware eligible hull upgrades, module fit saturation, playbook caps)
     against economic outcomes (fleet steady cashflow +/- & 24h direction, role KPI).
  2. Multi-window burn & hysteresis: compares 6h short window and 24h long window against
     prior windows with a +/-5% flat deadband to prevent alert flapping.
  3. <80% completion triggers: flags ALARM (<60%) and WARN (<80%) with exact gap counts
     and concrete next levers; stays silent on OK metrics inside startup briefings.
  4. Stagnation / momentum detection: synthesizes 5 compounding pillars (cashflow trend,
     wealth delta, skill/hull progression velocity, needs/roadmap advancement, productive
     flight-hour efficiency) into COMPOUNDING / GROWING_WITH_DRAG / SLOWING / STAGNATING.

Read-only. Pure stdlib.

Usage:
  python3 -I -B game/fleet/scorecard.py [--who all|Unity|Zero|Mercury|Apollo|Apophis|Oracle] [--json]
"""
import argparse
import json
import os
import re
import sqlite3
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import progression

DATA_DEFAULT = "/srv/collective/data"
REPO_DEFAULT = "/srv/collective/the-collective"

DIVISIONS = ("Command", "Mining", "Trade", "Logistics", "Military", "Intel")
MEMBER_TO_DIV = {
    "unity": "Command",
    "command": "Command",
    "zero": "Mining",
    "mining": "Mining",
    "miner": "Mining",
    "mercury": "Trade",
    "trade": "Trade",
    "trader": "Trade",
    "apollo": "Logistics",
    "logistics": "Logistics",
    "hauler": "Logistics",
    "apophis": "Military",
    "military": "Military",
    "drone": "Military",
    "sentinel": "Military",
    "oracle": "Intel",
    "intel": "Intel",
    "scout": "Intel",
}
DIV_TO_ADMIRAL = {
    "Command": "Unity",
    "Mining": "Zero",
    "Trade": "Mercury",
    "Logistics": "Apollo",
    "Military": "Apophis",
    "Intel": "Oracle",
}
DIV_KEY_LOWER = {d: d.lower() for d in DIVISIONS}

SEVERITY_RANK = {"ALARM": 0, "WARN": 1, "OK": 2}
TARGET_COMPLETION_PCT = 80.0
HYSTERESIS_PCT = 5.0


def _num(v, default=0.0):
    try:
        return float(v) if v is not None else float(default)
    except (TypeError, ValueError):
        return float(default)


def _fmt_cr(v):
    n = int(round(_num(v)))
    sign = "+" if n > 0 else ""
    if abs(n) >= 1_000_000:
        return f"{sign}{n / 1_000_000:.2f}M"
    if abs(n) >= 10_000:
        return f"{sign}{n / 1_000:.1f}k"
    return f"{sign}{n:,d}"


def _fmt_num(v):
    return f"{int(round(_num(v))):,d}"


def _classify_trend(curr, prev, min_abs=2000.0):
    """Classify direction with hysteresis deadband (+/-5% and min_abs) to prevent flapping."""
    if prev is None:
        return "FLAT", 0.0
    delta = _num(curr) - _num(prev)
    denom = max(abs(_num(prev)), min_abs)
    rel = (delta / denom) * 100.0
    if abs(delta) < min_abs or abs(rel) < HYSTERESIS_PCT:
        return "FLAT", round(delta, 1)
    return ("IMPROVING" if delta > 0 else "WORSENING"), round(delta, 1)


def _tier_required_for_piloting(piloting):
    p = int(_num(piloting))
    if p >= 50:
        return 5
    if p >= 30:
        return 4
    if p >= 20:
        return 3
    if p >= 10:
        return 2
    return 0


def _severity_pct(pct, alarm_below=60.0, warn_below=80.0):
    if pct < alarm_below:
        return "ALARM"
    if pct < warn_below:
        return "WARN"
    return "OK"


def _count_open_requests(repo_root):
    p = Path(repo_root) / "communications" / "requests.log"
    if not p.is_file():
        return 0
    try:
        text = p.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return 0
    # Count ENT blocks of type 'request' that have no later answer/close referencing them
    requests = set(re.findall(r"^## \[(ENT-\d+)\][^\n]*\|\s*request\b", text, flags=re.M))
    answered = set(re.findall(r"\bsee:\s*[^\n]*?(ENT-\d+)", text))
    # Also scan explicit answers that cite multiple ENTs in see:
    for ln in text.splitlines():
        if ln.startswith("## [ENT-") and ("| answer" in ln or "| close" in ln or "| done" in ln):
            for ent in re.findall(r"ENT-\d+", ln.split("see:", 1)[-1] if "see:" in ln else ""):
                answered.add(ent)
    return len(requests - answered)


def _load_json(path, default):
    p = Path(path)
    if not p.is_file():
        return default
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return default


def _load_diplomacy_pending(data_dir):
    doc = _load_json(Path(data_dir) / "comms" / "diplomacy.json", {})
    factions = doc.get("factions") if isinstance(doc, dict) else {}
    pending_replies = 0
    neutral_count = 0
    for rec in (factions or {}).values():
        if not isinstance(rec, dict):
            continue
        st = (rec.get("status") or "").lower()
        if st in ("neutrality_agreed", "trade_active", "info_sharing_active"):
            neutral_count += 1
        in_ts = str(rec.get("last_inbound_at") or "")
        out_ts = str(rec.get("last_outbound_at") or "")
        if in_ts and in_ts > out_ts:
            pending_replies += 1
    return neutral_count, pending_replies


def _load_fleet_live(data_dir):
    fj = _load_json(Path(data_dir) / "fleet" / "fleet.json", {})
    totals = fj.get("totals") if isinstance(fj.get("totals"), dict) else {}
    t_divs = totals.get("divisions") if isinstance(totals.get("divisions"), dict) else {}
    by_div = {d: {"total": 0, "working": 0, "idle": 0, "docked_waiting": 0, "adrift": 0, "credits": 0} for d in DIVISIONS}

    if t_divs:
        for d in DIVISIONS:
            td = t_divs.get(d)
            if isinstance(td, dict):
                tot = int(_num(td.get("ships")))
                wrk = int(_num(td.get("working")))
                prk = int(_num(td.get("parked")))
                adr = int(_num(td.get("adrift")))
                by_div[d] = {
                    "total": tot,
                    "working": wrk,
                    "idle": max(0, tot - wrk),
                    "docked_waiting": prk,
                    "adrift": adr,
                    "credits": int(_num(td.get("credits"))),
                }
        return by_div, totals, fj.get("updated_at") or ""

    # Fallback for test fixtures / simplified fleet.json without totals.divisions
    ships = fj.get("ships") or []
    if isinstance(ships, dict):
        ships = [{"name": k, **v} for k, v in ships.items()]
    for s in ships:
        if not isinstance(s, dict):
            continue
        div = s.get("division") or "Command"
        if div not in by_div:
            continue
        rec = by_div[div]
        rec["total"] += 1
        rec["credits"] += int(_num(s.get("credits")))
        stt = str(s.get("status") or "").lower()
        is_work = (stt == "working") or (stt in ("", "connected") and bool(s.get("order")))
        if is_work:
            rec["working"] += 1
        else:
            rec["idle"] += 1
            if s.get("docked"):
                rec["docked_waiting"] += 1
    return by_div, totals, fj.get("updated_at") or ""


def _load_watchdog_deltas(data_dir):
    ws = _load_json(Path(data_dir) / "fleet" / "watchdog.state.json", {})
    last = ws.get("last") if isinstance(ws, dict) else None
    hist = ws.get("history") if isinstance(ws, dict) and isinstance(ws.get("history"), list) else []
    base = None
    if isinstance(last, dict) and hist:
        last_ep = _num(last.get("epoch"))
        # Prefer snapshot ~6h ago (4-9h window), else earliest in history
        best = None
        best_diff = 1e18
        for h in hist:
            if not isinstance(h, dict):
                continue
            dt = last_ep - _num(h.get("epoch"))
            if dt >= 10800:
                diff = abs(dt - 21600)
                if diff < best_diff:
                    best_diff = diff
                    best = h
        base = best or (hist[0] if isinstance(hist[0], dict) else None)
    if not isinstance(last, dict) or not isinstance(base, dict):
        return {"dt_h": 0.0, "money_delta": None, "p10_delta": None, "t2_delta": None, "idle_delta": None}
    dt_h = max(0.0, (_num(last.get("epoch")) - _num(base.get("epoch"))) / 3600.0)
    return {
        "dt_h": round(dt_h, 2),
        "money_delta": int(_num(last.get("total_money")) - _num(base.get("total_money"))),
        "p10_delta": int(_num(last.get("p10_pilots")) - _num(base.get("p10_pilots"))),
        "t2_delta": int(_num(last.get("t2_hulls")) - _num(base.get("t2_hulls"))),
        "idle_delta": int(_num(last.get("idle_ships")) - _num(base.get("idle_ships"))),
    }


def compute_scorecard(repo_root=REPO_DEFAULT, data_dir=DATA_DEFAULT, now=None):
    """Compute complete enterprise & per-division KPI scorecard + alert triggers."""
    now = float(now if now is not None else time.time())
    db_path = Path(data_dir) / "store" / "read.db"
    conn = None
    tables = set()
    if db_path.is_file():
        conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True, timeout=3.0)
        conn.row_factory = sqlite3.Row
        tables = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type IN ('table','view')")}

    live_div, live_totals, fleet_ts = _load_fleet_live(data_dir)
    wd_deltas = _load_watchdog_deltas(data_dir)
    neutral_cnt, diplo_pending = _load_diplomacy_pending(data_dir)
    open_reqs = _count_open_requests(repo_root)

    # Progression snapshot (roadmap %, milestones, seating)
    prog = {}
    try:
        prog = progression.compute_progression(str(repo_root), data=str(data_dir), now=now) or {}
    except Exception:
        prog = {}

    # -----------------------------------------------------------------------
    # 1. SQL queries from read.db
    # -----------------------------------------------------------------------
    money_by_div = {}
    kpi_live = {}
    contrib_24h = {}
    hulls_by_div = {d: {"total": 0, "t1_plus": 0, "t2_plus": 0, "eligible_p10": 0, "upgraded_eligible": 0,
                        "near_p10": 0, "max_piloting": 0, "sum_piloting": 0.0, "empires": {}} for d in DIVISIONS}
    mods_by_div = {d: {"ships": 0, "fitted_slots": 0, "max_slots": 0, "t2_mod_ships": 0, "off_role_ships": 0}
                   for d in DIVISIONS}
    pb_by_div = {}
    fuel_sinks = {"total_h": 0.0, "productive_h": 0.0, "jump_h": 0.0, "jump_net": 0.0, "census_h": 0.0}
    supply_ok, supply_tot, supply_short = 0, 0, []
    needs_open = []
    places_tot, places_fresh = 0, 0
    fac_members, fac_limit, fac_treasury = 0, 0, 0

    try:
        if conn is not None:
            # Faction seating
            if "faction" in tables:
                fr = conn.execute("SELECT member_count, members_limit, treasury FROM faction LIMIT 1").fetchone()
                if fr:
                    fac_members = int(_num(fr["member_count"]))
                    fac_limit = int(_num(fr["members_limit"]))
                    fac_treasury = int(_num(fr["treasury"]))

            # Live KPI figures (1h, 6h, 24h)
            if "stats_figures" in tables:
                for r in conn.execute(
                    "SELECT view, subject, figure, hours, value FROM stats_figures WHERE view IN ('kpi','contribution') AND hours IN (1, 6, 24)"
                ).fetchall():
                    v, subj, fig, hrs, val = r["view"], r["subject"], r["figure"], int(_num(r["hours"])), r["value"]
                    if v == "kpi" and subj == "Fleet":
                        kpi_live[(fig, hrs)] = _num(val) if val is not None else None
                    elif v == "contribution" and hrs == 24:
                        contrib_24h[(subj, fig)] = _num(val) if val is not None else None

            # Whole-hour cashflow history per division & Fleet (last 6h vs prior 6h, last 24h vs prior 24h)
            if "stats_money_hour" in tables:
                mx_r = conn.execute("SELECT MAX(hour) FROM stats_money_hour").fetchone()
                mx_h = int(_num(mx_r[0])) if mx_r and mx_r[0] is not None else 0
                if mx_h > 0:
                    for r in conn.execute("""
                        SELECT division,
                               AVG(CASE WHEN hour > ? - 21600 THEN net END) AS net_6h,
                               AVG(CASE WHEN hour <= ? - 21600 AND hour > ? - 43200 THEN net END) AS net_prev6h,
                               AVG(CASE WHEN hour > ? - 86400 THEN net END) AS net_24h,
                               AVG(CASE WHEN hour <= ? - 86400 AND hour > ? - 172800 THEN net END) AS net_prev24h,
                               AVG(CASE WHEN hour > ? - 86400 THEN income END) AS inc_24h,
                               AVG(CASE WHEN hour > ? - 86400 THEN costs END) AS costs_24h,
                               AVG(CASE WHEN hour > ? - 86400 THEN total END) AS total_24h,
                               COUNT(CASE WHEN hour > ? - 86400 THEN 1 END) AS n_24h,
                               COUNT(CASE WHEN hour <= ? - 86400 AND hour > ? - 172800 THEN 1 END) AS n_prev24h
                        FROM stats_money_hour
                        GROUP BY division
                    """, (mx_h,) * 12).fetchall():
                        money_by_div[r["division"]] = {
                            "net_6h": round(_num(r["net_6h"]), 1) if r["net_6h"] is not None else 0.0,
                            "net_prev6h": round(_num(r["net_prev6h"]), 1) if r["net_prev6h"] is not None else None,
                            "net_24h": round(_num(r["net_24h"]), 1) if r["net_24h"] is not None else 0.0,
                            "net_prev24h": round(_num(r["net_prev24h"]), 1) if r["net_prev24h"] is not None else None,
                            "inc_24h": round(_num(r["inc_24h"]), 1) if r["inc_24h"] is not None else 0.0,
                            "costs_24h": round(_num(r["costs_24h"]), 1) if r["costs_24h"] is not None else 0.0,
                            "total_24h": round(_num(r["total_24h"]), 1) if r["total_24h"] is not None else 0.0,
                            "n_24h": int(_num(r["n_24h"])),
                            "n_prev24h": int(_num(r["n_prev24h"])),
                        }

            # Hull upgrade readiness (role- & empire-aware!)
            if "ships" in tables:
                has_hulls = "hulls" in tables
                has_skills = "ship_skills" in tables
                q = """
                    SELECT s.pilot, s.division, LOWER(COALESCE(NULLIF(s.empire,''), 'voidborn')) AS emp,
                           COALESCE(h.tier, 0) AS tier,
                           COALESCE(sk.level, 0) AS piloting
                    FROM ships s
                    LEFT JOIN hulls h ON h.id = s.class OR h.name = s.class
                    LEFT JOIN ship_skills sk ON sk.pilot = s.pilot AND sk.skill = 'piloting'
                """ if (has_hulls and has_skills) else "SELECT pilot, division, 'voidborn' AS emp, 0 AS tier, 0 AS piloting FROM ships"
                for r in conn.execute(q).fetchall():
                    div = r["division"] or "Command"
                    if div not in hulls_by_div:
                        continue
                    h = hulls_by_div[div]
                    tr = int(_num(r["tier"]))
                    pil = int(_num(r["piloting"]))
                    emp = str(r["emp"] or "voidborn")
                    h["total"] += 1
                    h["sum_piloting"] += pil
                    if pil > h["max_piloting"]:
                        h["max_piloting"] = pil
                    h["empires"][emp] = h["empires"].get(emp, 0) + 1
                    if tr >= 1:
                        h["t1_plus"] += 1
                    if tr >= 2:
                        h["t2_plus"] += 1
                    req_t = _tier_required_for_piloting(pil)
                    if req_t >= 2:
                        h["eligible_p10"] += 1
                        if tr >= req_t:
                            h["upgraded_eligible"] += 1
                    elif pil >= 8:
                        h["near_p10"] += 1

            # Module fit saturation, T2+ modules, and off-role starter modules
            if "ships" in tables and "ship_modules" in tables and "hulls" in tables:
                for r in conn.execute("""
                    WITH per_ship AS (
                        SELECT s.pilot, s.division,
                               MAX(1, COALESCE(h.weapon_slots, 1) + COALESCE(h.defense_slots, 1) + COALESCE(h.utility_slots, 1)) AS max_slots,
                               COUNT(m.module) AS fitted,
                               SUM(CASE WHEN m.module LIKE '%_ii' OR m.module LIKE '%_iii' OR m.module LIKE '%_iv'
                                         OR m.module LIKE '%_v' OR m.module LIKE '%_mk2%' THEN 1 ELSE 0 END) AS t2_mods,
                               SUM(CASE WHEN (s.division='Mining' AND m.module='pulse_laser_i')
                                         OR (s.division IN ('Trade','Logistics','Intel') AND m.module IN ('mining_laser_i','ice_harvester_i','gas_harvester_i','pulse_laser_i'))
                                         OR (s.division='Military' AND m.module IN ('mining_laser_i','ice_harvester_i','gas_harvester_i'))
                                        THEN 1 ELSE 0 END) AS off_role
                        FROM ships s
                        LEFT JOIN hulls h ON h.id = s.class OR h.name = s.class
                        LEFT JOIN ship_modules m ON m.pilot = s.pilot
                        GROUP BY s.pilot
                    )
                    SELECT division, COUNT(*) AS ships,
                           SUM(fitted) AS fitted_slots, SUM(max_slots) AS max_slots,
                           SUM(CASE WHEN t2_mods > 0 THEN 1 ELSE 0 END) AS t2_mod_ships,
                           SUM(CASE WHEN off_role > 0 THEN 1 ELSE 0 END) AS off_role_ships
                    FROM per_ship GROUP BY division
                """).fetchall():
                    div = r["division"] or "Command"
                    if div in mods_by_div:
                        mods_by_div[div] = {
                            "ships": int(_num(r["ships"])),
                            "fitted_slots": int(_num(r["fitted_slots"])),
                            "max_slots": int(_num(r["max_slots"])),
                            "t2_mod_ships": int(_num(r["t2_mod_ships"])),
                            "off_role_ships": int(_num(r["off_role_ships"])),
                        }

            # Playbook caps (compute exact live chapter cap % matching guide.py drift; fallback to division_playbooks)
            if "division_playbooks" in tables:
                for r in conn.execute("SELECT division, max_chapter_pct, open_needs, ready_needs FROM division_playbooks").fetchall():
                    pb_by_div[str(r["division"] or "").lower()] = {
                        "max_chapter_pct": round(_num(r["max_chapter_pct"]), 1),
                        "open_needs": int(_num(r["open_needs"])),
                        "ready_needs": int(_num(r["ready_needs"])),
                    }
            try:
                import guidebook as _gb
                gb_root = Path(repo_root) / "game" / "routes" / "guidebook"
                if gb_root.is_dir():
                    for d_low in ("command", "mining", "trade", "logistics", "military", "intel"):
                        d_dir = gb_root / d_low
                        if not d_dir.is_dir():
                            continue
                        mx_p = 0.0
                        for md in d_dir.glob("*.md"):
                            cap = float(_gb.CARD_MAX if md.stem == "card" else _gb.CHAPTER_MAX)
                            body = md.read_text(encoding="ascii", errors="replace")
                            # Sum characters from first ### entry onward (exact guidebook.chapter_chars semantics)
                            pos = body.find("\n### ")
                            used = len(body) - pos if pos >= 0 else len(body)
                            pct = round(100.0 * used / max(1.0, cap), 1)
                            if pct > mx_p:
                                mx_p = pct
                        pb_by_div.setdefault(d_low, {})["max_chapter_pct"] = mx_p
            except Exception:
                pass

            # Fuel sinks / Productive efficiency (24h)
            if "fuel_sinks" in tables:
                for r in conn.execute("SELECT category, ship_hours_24h, net_credits_24h FROM fuel_sinks").fetchall():
                    cat = str(r["category"] or "")
                    sh = _num(r["ship_hours_24h"])
                    fuel_sinks["total_h"] += sh
                    if cat == "productive":
                        fuel_sinks["productive_h"] += sh
                    elif cat == "jump_loops":
                        fuel_sinks["jump_h"] += sh
                        fuel_sinks["jump_net"] += _num(r["net_credits_24h"])
                    elif cat == "census":
                        fuel_sinks["census_h"] += sh

            # Supply chains
            if "supply_status" in tables:
                for r in conn.execute("SELECT chain, item, status, stock, keep FROM supply_status").fetchall():
                    supply_tot += 1
                    st = str(r["status"] or "").upper()
                    if st == "OK":
                        supply_ok += 1
                    else:
                        supply_short.append(f"{r['chain']}({int(_num(r['stock']))}/{int(_num(r['keep']))})")

            # Open P1/P2 needs
            if "need_status" in tables:
                for r in conn.execute(
                    "SELECT id, priority, division, covered, short_items, fee FROM need_status WHERE priority <= 2 AND COALESCE(covered,0) < 100 ORDER BY priority ASC, covered DESC"
                ).fetchall():
                    needs_open.append({
                        "id": str(r["id"]),
                        "priority": int(_num(r["priority"])),
                        "division": str(r["division"] or "").lower(),
                        "pct": round(_num(r["covered"]), 1),
                        "short": str(r["short_items"] or "")[:80],
                        "fee": int(_num(r["fee"])),
                    })

            # Places freshness (<3h)
            if "places" in tables:
                pr = conn.execute(
                    "SELECT COUNT(*) AS tot, SUM(CASE WHEN (? - COALESCE(t,0)) <= 10800 THEN 1 ELSE 0 END) AS fr FROM places",
                    (int(now),),
                ).fetchone()
                if pr:
                    places_tot = int(_num(pr["tot"]))
                    places_fresh = int(_num(pr["fr"]))
    finally:
        if conn is not None:
            conn.close()

    # -----------------------------------------------------------------------
    # 2. Fleetwide Enterprise Pulse
    # -----------------------------------------------------------------------
    total_ships = sum(live_div[d]["total"] for d in DIVISIONS) or sum(hulls_by_div[d]["total"] for d in DIVISIONS) or 500
    total_working = sum(live_div[d]["working"] for d in DIVISIONS)
    total_idle = sum(live_div[d]["idle"] for d in DIVISIONS)
    intel_watch = live_div["Intel"]["docked_waiting"]
    # Effective operational employment (respecting Intel's F8 docked-watch exception for fleetwide count)
    eff_working = total_working + min(intel_watch, live_div["Intel"]["idle"])
    emp_pct = round(100.0 * total_working / max(1, total_ships), 1)
    eff_emp_pct = round(100.0 * eff_working / max(1, total_ships), 1)

    fl_m = money_by_div.get("Fleet", {})
    steady_1h = round(_num(kpi_live.get(("net", 1)), fl_m.get("net_6h", 0.0)), 1)
    steady_6h = round(_num(kpi_live.get(("net", 6)), fl_m.get("net_6h", 0.0)), 1)
    steady_24h = round(_num(kpi_live.get(("net", 24)), fl_m.get("net_24h", 0.0)), 1)
    steady_tiled_24h = fl_m.get("net_24h", steady_24h)
    steady_prev_24h = fl_m.get("net_prev24h")
    steady_prev_6h = fl_m.get("net_prev6h")
    all_in_24h = round(_num(kpi_live.get(("total", 24)), fl_m.get("total_24h", 0.0)), 1)
    wallets_now = int(_num(kpi_live.get(("wallets", 24)), sum(live_div[d]["credits"] for d in DIVISIONS)))
    treasury_now = int(_num(kpi_live.get(("treasury", 24)), fac_treasury))
    purse_now = wallets_now + treasury_now
    surplus_worth = int(_num(kpi_live.get(("surplus_worth", 24)), 0))

    cf_sign = "POSITIVE" if steady_24h > 0 else "NEGATIVE"
    cf_dir_24h, cf_delta_24h = _classify_trend(steady_tiled_24h, steady_prev_24h, min_abs=3000.0)
    cf_dir_6h, cf_delta_6h = _classify_trend(fl_m.get("net_6h", steady_6h), steady_prev_6h, min_abs=3000.0)

    prod_pct = round(100.0 * fuel_sinks["productive_h"] / max(0.01, fuel_sinks["total_h"]), 1) if fuel_sinks["total_h"] > 0 else 0.0
    jump_pct = round(100.0 * fuel_sinks["jump_h"] / max(0.01, fuel_sinks["total_h"]), 1) if fuel_sinks["total_h"] > 0 else 0.0

    open_seats = max(0, min(total_ships, fac_limit) - fac_members) if fac_limit else 0
    seat_cap_pct = round(100.0 * fac_members / max(1, min(total_ships, fac_limit)), 1) if fac_limit else 0.0
    seat_fleet_pct = round(100.0 * fac_members / max(1, total_ships), 1)

    fleet_elig_p10 = sum(hulls_by_div[d]["eligible_p10"] for d in DIVISIONS)
    fleet_upg_elig = sum(hulls_by_div[d]["upgraded_eligible"] for d in DIVISIONS)
    fleet_t2_plus = sum(hulls_by_div[d]["t2_plus"] for d in DIVISIONS)
    fleet_hull_elig_pct = round(100.0 * fleet_upg_elig / max(1, fleet_elig_p10), 1) if fleet_elig_p10 else 0.0

    fleet_fitted = sum(mods_by_div[d]["fitted_slots"] for d in DIVISIONS)
    fleet_max_slots = sum(mods_by_div[d]["max_slots"] for d in DIVISIONS)
    fleet_slot_pct = round(100.0 * fleet_fitted / max(1, fleet_max_slots), 1) if fleet_max_slots else 0.0
    fleet_off_role = sum(mods_by_div[d]["off_role_ships"] for d in DIVISIONS)

    # Roadmap rungs & achieved milestones from progression.py
    roadmap_avg = 0.0
    ms_done, ms_tot, latest_ms = 0, 0, ""
    if isinstance(prog, dict):
        rungs = prog.get("rungs") or []
        if rungs:
            ms_tot = len(rungs)
            ms_done = sum(1 for r in rungs if _num(r.get("pct")) >= 100.0)
            roadmap_avg = round(sum(_num(r.get("pct")) for r in rungs) / ms_tot, 1)
        elif prog.get("overall_pct") is not None:
            roadmap_avg = round(_num(prog.get("overall_pct")), 1)
        mhist = prog.get("milestones") or []
        if mhist and isinstance(mhist[-1], dict):
            latest_ms = str(mhist[-1].get("title") or "")

    # Enterprise-level triggers (actionable only)
    ent_triggers = []
    if steady_24h <= 0:
        sev = "ALARM" if (cf_dir_24h == "WORSENING" or steady_24h < -20000) else "WARN"
        ent_triggers.append({
            "severity": sev, "code": "CASHFLOW_NEGATIVE", "metric": "Fleet Steady Cashflow",
            "actual": f"{_fmt_cr(steady_24h)} cr/h (6h {_fmt_cr(steady_6h)})",
            "target": ">0 cr/h", "direction": f"24h {cf_dir_24h} / 6h {cf_dir_6h}",
            "action": "Cut empty jump loops & census burn; shift idle/unprofitable ships to paying cargo, crafts & P2P contracts (P1/F8/F39)",
        })
    if prod_pct < TARGET_COMPLETION_PCT and fuel_sinks["total_h"] > 0:
        ent_triggers.append({
            "severity": _severity_pct(prod_pct, 60.0, 80.0), "code": "PRODUCTIVE_EFFICIENCY",
            "metric": "Productive Flight Efficiency",
            "actual": f"{prod_pct:.1f}% (jump loops {jump_pct:.1f}%, {_fmt_cr(fuel_sinks['jump_net'])} cr/24h)",
            "target": ">=80%", "direction": cf_dir_6h,
            "action": "Replace empty jump-loops with cargo-carrying loops, docked crafting, or Station Bursar market-making",
        })
    if eff_emp_pct < 90.0:
        ent_triggers.append({
            "severity": _severity_pct(eff_emp_pct, 80.0, 90.0), "code": "FLEET_IDLE",
            "metric": "Fleet Operational Employment",
            "actual": f"{eff_emp_pct:.1f}% ({total_idle} waiting; {intel_watch} Intel watch)",
            "target": ">=90% (0 idle)", "direction": "IMPROVING" if (wd_deltas["idle_delta"] or 0) < 0 else ("WORSENING" if (wd_deltas["idle_delta"] or 0) > 0 else "FLAT"),
            "action": "Admirals autonomously set far_ok for newborns past home Mastery (F16/F35/P6) so idle ships join main corridors",
        })
    if open_seats > 0 and seat_cap_pct < TARGET_COMPLETION_PCT:
        ent_triggers.append({
            "severity": _severity_pct(seat_cap_pct, 60.0, 80.0), "code": "OPEN_SEATS",
            "metric": "Faction Cap Seating",
            "actual": f"{fac_members}/{fac_limit} ({seat_cap_pct:.1f}%, {open_seats} open; {seat_fleet_pct:.1f}% of {total_ships})",
            "target": ">=80% of cap (0 open)", "direction": "FLAT",
            "action": f"Unity seats {open_seats} ready ships via wallet.py seat (F11/P4)",
        })
    if fleet_elig_p10 > 0 and fleet_hull_elig_pct < TARGET_COMPLETION_PCT:
        ent_triggers.append({
            "severity": _severity_pct(fleet_hull_elig_pct, 60.0, 80.0), "code": "HULL_UPGRADE_LAG",
            "metric": "Eligible Hull Upgrades (P10+ -> T2+)",
            "actual": f"{fleet_upg_elig}/{fleet_elig_p10} ({fleet_hull_elig_pct:.1f}%)",
            "target": ">=80% of eligible", "direction": "IMPROVING" if (wd_deltas["t2_delta"] or 0) > 0 else "FLAT",
            "action": "Parallel batch-upgrade P10+ pilots & P0 cargo freighters (Ledger/Prayer/Workhorse) via `hive.py upgrades` (F17/F37/O2)",
        })
    if fleet_slot_pct < TARGET_COMPLETION_PCT:
        ent_triggers.append({
            "severity": _severity_pct(fleet_slot_pct, 60.0, 80.0), "code": "MODULE_FIT_SATURATION",
            "metric": "Fleet Module Fit Saturation",
            "actual": f"{fleet_fitted}/{fleet_max_slots} slots ({fleet_slot_pct:.1f}%, {fleet_off_role} off-role starters)",
            "target": ">=80% slots, 0 off-role", "direction": "FLAT",
            "action": "Strip off-role starter modules (`unfit`) and fill open slots with role-matched T2+ modules (O2)",
        })
    ent_triggers.sort(key=lambda x: SEVERITY_RANK.get(x["severity"], 9))

    # -----------------------------------------------------------------------
    # 3. Per-Division Scorecards
    # -----------------------------------------------------------------------
    divisions_out = {}
    for div in DIVISIONS:
        adm = DIV_TO_ADMIRAL[div]
        ld = live_div[div]
        hd = hulls_by_div[div]
        md = mods_by_div[div]
        dm = money_by_div.get(div, {})
        pb = pb_by_div.get(div.lower(), {})
        tot = ld["total"] or hd["total"]
        wrk = ld["working"]
        idl = ld["idle"]
        # Intel docked watch exception (F8)
        eff_wrk = wrk + ld["docked_waiting"] if div == "Intel" else wrk
        div_emp_pct = round(100.0 * eff_wrk / max(1, tot), 1)
        raw_emp_pct = round(100.0 * wrk / max(1, tot), 1)

        # Hull upgrade completion (role & empire aware)
        elig_p10 = hd["eligible_p10"]
        upg_elig = hd["upgraded_eligible"]
        avg_pil = round(hd["sum_piloting"] / max(1, hd["total"]), 1)
        if elig_p10 > 0:
            hull_pct = round(100.0 * upg_elig / elig_p10, 1)
            hull_mode = "eligible_t2"
            hull_label = f"{upg_elig}/{elig_p10} P10+ on T2+ ({hull_pct:.0f}%)"
            hull_sev = _severity_pct(hull_pct, 60.0, 80.0)
        else:
            # No pilots at P10 yet -- measure Piloting progression toward T2 gate + T1+ hulls
            hull_pct = round(min(100.0, (avg_pil / 10.0) * 100.0), 1)
            hull_mode = "piloting_to_t2"
            hull_label = f"0 P10+ yet (max P{hd['max_piloting']}, avg P{avg_pil}, {hd['near_p10']} at P8-9)"
            hull_sev = "WARN" if (hd["max_piloting"] < 8 and hd["t1_plus"] == 0) else ("OK" if hull_pct >= 80.0 else "WARN")

        # Module fit saturation & role purity
        slot_pct = round(100.0 * md["fitted_slots"] / max(1, md["max_slots"]), 1) if md["max_slots"] else 0.0
        t2_mod_pct = round(100.0 * md["t2_mod_ships"] / max(1, tot), 1)
        off_role_pct = round(100.0 * md["off_role_ships"] / max(1, tot), 1)
        mod_sev = "ALARM" if (slot_pct < 60.0 or off_role_pct > 25.0) else ("WARN" if (slot_pct < 80.0 or md["off_role_ships"] > 0) else "OK")

        # Division cashflow trend
        d_net24 = dm.get("net_24h", 0.0)
        d_prev24 = dm.get("net_prev24h")
        d_net6 = dm.get("net_6h", 0.0)
        d_trend, d_delta24 = _classify_trend(d_net24, d_prev24, min_abs=1500.0)

        # Playbook cap check
        pb_pct = _num(pb.get("max_chapter_pct"))
        pb_sev = "ALARM" if pb_pct >= 95.0 else ("WARN" if pb_pct >= 85.0 else "OK")

        # Role-specific primary success KPI
        triggers = []
        emp_alarm_cut = 60.0 if div == "Command" else 80.0
        emp_warn_cut = 80.0 if div == "Command" else 90.0
        emp_sev = _severity_pct(div_emp_pct, emp_alarm_cut, emp_warn_cut)

        if emp_sev != "OK":
            triggers.append({
                "severity": emp_sev, "code": "DIV_IDLE", "metric": "Employment",
                "actual": f"{eff_wrk}/{tot} ({div_emp_pct:.1f}%, {tot - eff_wrk} idle)",
                "target": f">={int(emp_warn_cut)}%", "direction": d_trend,
                "action": "Assign waiting ships now; set far_ok autonomously for newborns past home Mastery (F8/F16/F35)",
            })
        if hull_sev != "OK" and elig_p10 > 0:
            triggers.append({
                "severity": hull_sev, "code": "DIV_HULL_UPGRADE", "metric": "Eligible Hull Upgrades",
                "actual": hull_label, "target": ">=80% of P10+ upgraded",
                "direction": "IMPROVING" if (wd_deltas["t2_delta"] or 0) > 0 else "FLAT",
                "action": f"Parallel batch-upgrade P10+ {div} pilots to empire-specialized T2 hulls & measure in flight (`hive.py upgrades`, F17/F37)",
            })
        elif hull_sev == "WARN" and elig_p10 == 0:
            triggers.append({
                "severity": "WARN", "code": "DIV_SKILL_TO_T2", "metric": "Piloting Gate to T2",
                "actual": hull_label, "target": ">=80% toward P10 (T2 unlock)",
                "direction": "FLAT",
                "action": "Prioritize paying cargo/craft routes that level Piloting toward P10 without empty jump burn (O2/P1)",
            })
        if mod_sev != "OK":
            triggers.append({
                "severity": mod_sev, "code": "DIV_MODULE_FIT", "metric": "Module Fit & Purity",
                "actual": f"{md['fitted_slots']}/{md['max_slots']} slots ({slot_pct:.1f}%), {md['t2_mod_ships']} T2+ ships, {md['off_role_ships']} off-role",
                "target": ">=80% slots, 0 off-role", "direction": "FLAT",
                "action": "Unfit off-role starter modules and fit role-matched T2+ modules across open slots (O2)",
            })

        # Division-matched Role Success KPI
        if div == "Mining":
            ore_sh = round(_num(contrib_24h.get(("Mining", "ore_per_ship_hour"))), 1)
            ho_worth = int(_num(contrib_24h.get(("Mining", "handed_over_worth"))))
            role_kpi = {
                "name": "Extraction & Handover",
                "value": f"{ore_sh:.1f} ore/ship-h | {_fmt_cr(ho_worth)} cr/24h handed",
                "pct": min(100.0, round(ore_sh / 25.0 * 100.0, 1)) if ore_sh > 0 else 0.0,
                "status": "OK" if (ore_sh >= 15.0 and ho_worth > 0) else ("WARN" if ore_sh > 0 else "ALARM"),
                "cashflow_24h": round(d_net24, 1),
            }
            if role_kpi["status"] != "OK":
                triggers.append({
                    "severity": role_kpi["status"], "code": "MINING_YIELD", "metric": "Extraction Yield",
                    "actual": role_kpi["value"], "target": ">=15 ore/ship-h + active reserve handovers",
                    "direction": d_trend,
                    "action": "Upgrade to Laser II/III & richer reserve belts (silicon, carbon, gold, nickel); gift loads inward (P2/P5)",
                })
        elif div == "Trade":
            sell_cph = round(_num(contrib_24h.get(("Trade", "sell_cph"))), 0)
            tr_status = "OK" if (d_net24 > 0 and d_trend != "WORSENING") else ("WARN" if d_net24 > 0 else "ALARM")
            role_kpi = {
                "name": "Trade Steady Net & Sales",
                "value": f"{_fmt_cr(d_net24)} cr/h (6h {_fmt_cr(d_net6)}) | sell {_fmt_cr(sell_cph)}/h",
                "pct": 100.0 if d_net24 > 0 else 0.0,
                "status": tr_status,
                "cashflow_24h": round(d_net24, 1),
            }
            if d_net24 <= 0 or d_trend == "WORSENING":
                triggers.append({
                    "severity": "ALARM" if d_net24 <= 0 else "WARN", "code": "TRADE_NET", "metric": "Trade Steady Cashflow",
                    "actual": f"{_fmt_cr(d_net24)} cr/h ({d_trend} vs {_fmt_cr(d_prev24)} prior)",
                    "target": ">0 cr/h & improving", "direction": d_trend,
                    "action": "Cap empty jump loops, liquidate surplus @ bid, expand Station Bursar orders & Ch1-Ch4 P2P trade (F39)",
                })
            if surplus_worth >= 250_000:
                triggers.append({
                    "severity": "WARN", "code": "SURPLUS_BACKLOG", "metric": "Unliquidated Surplus",
                    "actual": f"{_fmt_cr(surplus_worth)} cr @ bid sitting in vaults",
                    "target": "<250k cr backlog", "direction": "FLAT",
                    "action": "Run surplus.py & sell handed-over goods at or above bids / Exchange sell_order (P5/F39)",
                })
        elif div == "Logistics":
            chain_pct = round(100.0 * supply_ok / max(1, supply_tot), 1) if supply_tot else 100.0
            top_need = needs_open[0] if needs_open else None
            need_txt = f"top P{top_need['priority']} {top_need['id']} {top_need['pct']:.1f}%" if top_need else "all P1/P2 covered"
            log_sev = _severity_pct(chain_pct, 60.0, 80.0)
            role_kpi = {
                "name": "Supply Chains & Build Kits",
                "value": f"chains {supply_ok}/{supply_tot} OK ({chain_pct:.0f}%) | {need_txt}",
                "pct": chain_pct,
                "status": log_sev,
                "cashflow_24h": round(d_net24, 1),
            }
            if log_sev != "OK":
                triggers.append({
                    "severity": log_sev, "code": "SUPPLY_CHAINS", "metric": "Supply Chains at Keep",
                    "actual": f"{supply_ok}/{supply_tot} ({chain_pct:.1f}%): {', '.join(supply_short[:3])}",
                    "target": ">=80% chains OK", "direction": d_trend,
                    "action": "Refill short outpost fuel/repair reserves and close Atria kit / Core Foundry craft gaps (P2/P3); check shipping.py list (Ch3)",
                })
        elif div == "Military":
            cxp = round(_num(contrib_24h.get(("Military", "combat_xp_per_ship_hour"))), 1)
            kills = int(_num(contrib_24h.get(("Military", "kills"))))
            lost = int(_num(contrib_24h.get(("Military", "ships_lost"))))
            mil_sev = "ALARM" if lost > 0 else ("WARN" if (cxp < 15.0 or d_net24 < -25000) else "OK")
            role_kpi = {
                "name": "Combat XP, Kills & Losses",
                "value": f"{cxp:.1f} XP/ship-h | {kills} kills/24h | {lost} lost",
                "pct": 0.0 if lost > 0 else min(100.0, round(cxp / 25.0 * 100.0, 1)),
                "status": mil_sev,
                "cashflow_24h": round(d_net24, 1),
            }
            if mil_sev != "OK":
                triggers.append({
                    "severity": mil_sev, "code": "MILITARY_PERF", "metric": "Combat Readiness & Losses",
                    "actual": role_kpi["value"] + f" | net {_fmt_cr(d_net24)}/h",
                    "target": "0 lost, >=15 XP/ship-h", "direction": d_trend,
                    "action": "Validate T2 Recursion & pair hunts (F37), fit combat weapons, protect lines with zero unescorted losses (F2/O8)",
                })
        elif div == "Intel":
            fresh_pct = round(100.0 * places_fresh / max(1, places_tot), 1) if places_tot else round(_num(contrib_24h.get(("Intel", "place_fresh_share"))) * 100.0, 1)
            lost = int(_num(contrib_24h.get(("Intel", "ships_lost"))))
            int_sev = "ALARM" if (lost > 0 or fresh_pct < 60.0) else ("WARN" if (fresh_pct < 80.0 or diplo_pending > 0) else "OK")
            role_kpi = {
                "name": "Intel Freshness (<3h) & Comms",
                "value": f"{places_fresh}/{places_tot} fresh ({fresh_pct:.1f}%) | {neutral_cnt} neutral, {diplo_pending} pending reply",
                "pct": fresh_pct,
                "status": int_sev,
                "cashflow_24h": round(d_net24, 1),
            }
            if fresh_pct < TARGET_COMPLETION_PCT:
                triggers.append({
                    "severity": _severity_pct(fresh_pct, 60.0, 80.0), "code": "INTEL_FRESHNESS", "metric": "Place Freshness (<3h)",
                    "actual": f"{places_fresh}/{places_tot} ({fresh_pct:.1f}%)",
                    "target": ">=80% fresh (<3h)", "direction": d_trend,
                    "action": "Prioritize worked corridors, Ironlight book (<3h), and newborn regions; keep excess scouts on docked watch (F8/O7)",
                })
            if diplo_pending > 0:
                triggers.append({
                    "severity": "WARN", "code": "DIPLO_PENDING", "metric": "Unanswered Partner Comms",
                    "actual": f"{diplo_pending} inbound diplomatic reply(ies) awaiting response",
                    "target": "0 unanswered", "direction": "FLAT",
                    "action": "Check diplomacy.py threads & coordinate Unity (Prime Directive) / Oracle envoy response (F4/O10)",
                })
        else:  # Command
            cmd_sev = "ALARM" if (steady_24h <= 0 or (open_seats > 0 and seat_cap_pct < 60.0)) else ("WARN" if (open_reqs > 0 or seat_cap_pct < 80.0) else "OK")
            role_kpi = {
                "name": "Enterprise Capital & Seating",
                "value": f"seats {fac_members}/{fac_limit} ({seat_cap_pct:.0f}%) | {open_reqs} open reqs | roadmap {roadmap_avg:.1f}%",
                "pct": seat_cap_pct if fac_limit else roadmap_avg,
                "status": cmd_sev,
                "cashflow_24h": round(steady_24h, 1),
            }
            if open_reqs > 0:
                triggers.append({
                    "severity": "ALARM" if open_reqs >= 5 else "WARN", "code": "OPEN_REQUESTS", "metric": "Open Requests to Unity",
                    "actual": f"{open_reqs} open request(s) in requests.log",
                    "target": "0 open", "direction": "FLAT",
                    "action": "Answer cross-division capital/seating/F10 requests; remind Admirals to decide division routing autonomously (F16)",
                })

        if pb_sev != "OK":
            triggers.append({
                "severity": pb_sev, "code": "PLAYBOOK_CAP", "metric": "Playbook Chapter Cap",
                "actual": f"{pb_pct:.1f}% of cap", "target": "<85% cap (F14)",
                "direction": "FLAT",
                "action": f"Compress bloated playbook chapters (`hive.py guide {div.lower()}`) below 85% cap (F14)",
            })

        triggers.sort(key=lambda x: SEVERITY_RANK.get(x["severity"], 9))
        div_status = triggers[0]["severity"] if triggers else "OK"

        divisions_out[div] = {
            "division": div,
            "admiral": adm,
            "status": div_status,
            "trend_24h": d_trend,
            "cashflow_24h": round(d_net24, 1),
            "cashflow_prev24h": d_prev24,
            "cashflow_6h": round(d_net6, 1),
            "employment": {
                "working": wrk, "effective_working": eff_wrk, "idle": tot - eff_wrk,
                "docked_watch": ld["docked_waiting"] if div == "Intel" else 0,
                "total": tot, "pct": div_emp_pct, "raw_pct": raw_emp_pct, "status": emp_sev,
            },
            "hulls": {
                "mode": hull_mode, "pct": hull_pct, "eligible_p10": elig_p10,
                "upgraded_eligible": upg_elig, "t1_plus": hd["t1_plus"], "t2_plus": hd["t2_plus"],
                "max_piloting": hd["max_piloting"], "avg_piloting": avg_pil, "near_p10": hd["near_p10"],
                "empires": hd["empires"], "label": hull_label, "status": hull_sev,
            },
            "modules": {
                "fitted_slots": md["fitted_slots"], "max_slots": md["max_slots"], "slot_pct": slot_pct,
                "t2_mod_ships": md["t2_mod_ships"], "t2_mod_pct": t2_mod_pct,
                "off_role_ships": md["off_role_ships"], "status": mod_sev,
            },
            "playbook": {
                "max_chapter_pct": pb_pct, "status": pb_sev,
            },
            "role_kpi": role_kpi,
            "triggers": triggers,
            "alarm_count": sum(1 for t in triggers if t["severity"] == "ALARM"),
            "warn_count": sum(1 for t in triggers if t["severity"] == "WARN"),
        }

    # -----------------------------------------------------------------------
    # 4. Stagnation & Momentum Verdict (5-Pillar Synthesis)
    # -----------------------------------------------------------------------
    advancing = []
    drags = []
    if steady_24h > 0 or cf_dir_24h == "IMPROVING":
        advancing.append("steady cashflow")
    else:
        drags.append(f"steady net {_fmt_cr(steady_24h)}/h ({cf_dir_24h} 24h)")
    if (wd_deltas["money_delta"] is not None and wd_deltas["money_delta"] > 0) or all_in_24h > 0:
        advancing.append(f"purse ({_fmt_cr(wd_deltas['money_delta'] or all_in_24h)})")
    else:
        drags.append("purse flat/falling")
    if (wd_deltas["p10_delta"] or 0) > 0 or (wd_deltas["t2_delta"] or 0) > 0:
        advancing.append(f"Piloting P10+ (+{wd_deltas['p10_delta'] or 0} in {wd_deltas['dt_h']:.0f}h)")
    else:
        drags.append("P10+/T2 progression flat")
    if roadmap_avg > 0 and (any(n["pct"] >= 80.0 for n in needs_open) or ms_done > 0):
        advancing.append(f"roadmap {roadmap_avg:.1f}% ({ms_done}/{ms_tot} milestones)")
    else:
        drags.append("milestone velocity stalled")
    if prod_pct >= 80.0 and eff_emp_pct >= 90.0:
        advancing.append(f"efficiency {prod_pct:.0f}%")
    else:
        drags.append(f"efficiency {prod_pct:.0f}% / idle {total_idle}")

    ent_alarms = sum(1 for t in ent_triggers if t["severity"] == "ALARM")
    if steady_24h > 0 and len(advancing) >= 3 and ent_alarms == 0:
        verdict = "COMPOUNDING"
    elif (steady_24h <= 0 and cf_dir_24h == "WORSENING" and (wd_deltas["p10_delta"] or 0) <= 0 and (wd_deltas["money_delta"] or 0) <= 0):
        verdict = "STAGNATING"
    elif (cf_dir_24h == "WORSENING" and cf_dir_6h == "WORSENING" and len(advancing) <= 2):
        verdict = "SLOWING"
    else:
        verdict = "GROWING_WITH_DRAG"

    return {
        "at": int(now),
        "fleet_at": fleet_ts,
        "target_pct": TARGET_COMPLETION_PCT,
        "enterprise": {
            "verdict": verdict,
            "advancing": advancing,
            "drags": drags,
            "cashflow_sign": cf_sign,
            "cashflow_trend_24h": cf_dir_24h,
            "cashflow_trend_6h": cf_dir_6h,
            "steady_1h": steady_1h,
            "steady_6h": steady_6h,
            "steady_24h": steady_24h,
            "steady_prev_24h": steady_prev_24h,
            "all_in_24h": all_in_24h,
            "purse_now": purse_now,
            "purse_delta_6h": wd_deltas["money_delta"],
            "dt_h": wd_deltas["dt_h"],
            "productive_pct": prod_pct,
            "jump_loop_pct": jump_pct,
            "jump_loop_burn_24h": round(fuel_sinks["jump_net"], 0),
            "employment_pct": emp_pct,
            "effective_employment_pct": eff_emp_pct,
            "working_ships": total_working,
            "idle_ships": total_idle,
            "total_ships": total_ships,
            "seated_ships": fac_members,
            "seat_cap": fac_limit,
            "open_seats": open_seats,
            "seat_cap_pct": seat_cap_pct,
            "seat_fleet_pct": seat_fleet_pct,
            "eligible_p10": fleet_elig_p10,
            "upgraded_eligible": fleet_upg_elig,
            "hull_eligible_pct": fleet_hull_elig_pct,
            "p10_delta_6h": wd_deltas["p10_delta"],
            "t2_hulls": fleet_t2_plus,
            "t2_delta_6h": wd_deltas["t2_delta"],
            "slot_fit_pct": fleet_slot_pct,
            "off_role_ships": fleet_off_role,
            "roadmap_avg_pct": roadmap_avg,
            "milestones_done": ms_done,
            "milestones_total": ms_tot,
            "latest_milestone": latest_ms,
            "open_requests": open_reqs,
            "neutral_partners": neutral_cnt,
            "diplo_pending": diplo_pending,
            "triggers": ent_triggers,
            "alarm_count": ent_alarms,
            "warn_count": sum(1 for t in ent_triggers if t["severity"] == "WARN"),
        },
        "divisions": divisions_out,
    }


def render_briefing(sc, who="all"):
    """Render compact, actionable startup scorecard lines for hive.py briefing (anti-alert-fatigue)."""
    e = sc["enterprise"]
    lines = ["=== KPI SCORECARD & ALERT TRIGGERS (<80% TARGETS & STAGNATION)"]
    p_delta = f" | 6h purse {_fmt_cr(e['purse_delta_6h'])}" if e["purse_delta_6h"] is not None else ""
    p10_d = f" (+{e['p10_delta_6h']} P10+)" if (e["p10_delta_6h"] or 0) > 0 else ""
    lines.append(
        f"  ENTERPRISE | {e['verdict']} | steady cashflow {e['cashflow_sign']} "
        f"({_fmt_cr(e['steady_24h'])}/h 24h, {_fmt_cr(e['steady_6h'])}/h 6h, 24h {e['cashflow_trend_24h']}, 6h {e['cashflow_trend_6h']}){p_delta}"
    )
    lines.append(
        f"  PULSE      | eff {e['productive_pct']:.1f}% (jumps {e['jump_loop_pct']:.1f}%) | "
        f"working {e['working_ships']}/{e['total_ships']} ({e['effective_employment_pct']:.1f}% eff) | "
        f"seats {e['seated_ships']}/{e['seat_cap']} ({e['seat_cap_pct']:.0f}%, {e['seat_fleet_pct']:.1f}% fleet) | "
        f"P10+->T2 {e['upgraded_eligible']}/{e['eligible_p10']} ({e['hull_eligible_pct']:.0f}%){p10_d} | "
        f"slots {e['slot_fit_pct']:.1f}% | roadmap {e['roadmap_avg_pct']:.1f}%"
    )
    if e["drags"]:
        lines.append("  BOTTLENECKS| " + "; ".join(e["drags"][:4]))

    target_div = None
    if who and str(who).lower() not in ("all", "unity", "command"):
        target_div = MEMBER_TO_DIV.get(str(who).lower())

    if target_div and target_div in sc["divisions"]:
        d = sc["divisions"][target_div]
        lines.append(
            f"  MY DIVISION ({d['division']} / {d['admiral']}) | state={d['status']} | 24h cashflow {_fmt_cr(d['cashflow_24h'])}/h ({d['trend_24h']})"
        )
        lines.append(
            f"    Readiness: work {d['employment']['effective_working']}/{d['employment']['total']} ({d['employment']['pct']:.1f}%) | "
            f"hulls {d['hulls']['label']} | "
            f"slots {d['modules']['fitted_slots']}/{d['modules']['max_slots']} ({d['modules']['slot_pct']:.1f}%, {d['modules']['t2_mod_ships']} T2+, {d['modules']['off_role_ships']} off-role) | "
            f"playbook {d['playbook']['max_chapter_pct']:.0f}%"
        )
        lines.append(f"    Role KPI : {d['role_kpi']['name']} = {d['role_kpi']['value']} [{d['role_kpi']['status']}]")
        if d["triggers"]:
            lines.append("  ACTIVE TRIGGERS (fix ALARM first):")
            for t in d["triggers"][:6]:
                lines.append(f"    [{t['severity']:5s}] {t['metric']}: {t['actual']} (target {t['target']}) -> {t['action']}")
        else:
            lines.append("  ACTIVE TRIGGERS: none (all division KPIs >=80% target)")
    else:
        # Unity / fleetwide view: compact 6-division scorecard table + top fleet alarms
        lines.append("  DIVISIONS  | Division   State  Work%   Hull-Upg  Slot%  OffRole  24h Net/h (Trend)     Role KPI")
        for div in DIVISIONS:
            d = sc["divisions"][div]
            h_txt = f"{d['hulls']['pct']:4.0f}%" + ("*" if d["hulls"]["mode"] == "piloting_to_t2" else " ")
            lines.append(
                f"             | {div:10s} {d['status']:5s}  {d['employment']['pct']:5.1f}%  {h_txt:>7s}  "
                f"{d['modules']['slot_pct']:5.1f}%  {d['modules']['off_role_ships']:>7d}  "
                f"{_fmt_cr(d['cashflow_24h']):>9s} ({d['trend_24h'][:4]:4s})  {d['role_kpi']['value'][:58]}"
            )
        lines.append("             (* = 0 P10+ pilots yet; % shows avg Piloting progress toward T2 unlock)")
        if e["triggers"]:
            lines.append("  TOP FLEET TRIGGERS:")
            for t in e["triggers"][:6]:
                lines.append(f"    [{t['severity']:5s}] {t['metric']}: {t['actual']} (target {t['target']}) -> {t['action']}")
    return "\n".join(lines)


def briefing(root, data, now, who="all"):
    """Print startup scorecard block safely (never aborts briefing on transient read errors)."""
    try:
        sc = compute_scorecard(repo_root=Path(root).resolve().parent if Path(root).name == "game" else root, data_dir=data, now=now)
        print(render_briefing(sc, who=who))
    except Exception as err:
        print(f"=== KPI SCORECARD: unavailable ({type(err).__name__}: {err})")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Compute Division KPI Scorecards, <80% Triggers & Stagnation Verdict.")
    ap.add_argument("--who", default="all", help="Member or division name (default: all)")
    ap.add_argument("--data", default=os.environ.get("COLLECTIVE_DATA", DATA_DEFAULT))
    ap.add_argument("--root", default=REPO_DEFAULT)
    ap.add_argument("--json", action="store_true", help="Emit structured JSON payload")
    args = ap.parse_args(argv)
    sc = compute_scorecard(repo_root=args.root, data_dir=args.data)
    if args.json:
        print(json.dumps(sc, indent=2))
    else:
        print(render_briefing(sc, who=args.who))
    return 0


if __name__ == "__main__":
    sys.exit(main())

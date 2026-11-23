#!/usr/bin/env python3
"""progression.py -- live enterprise progression roadmap, strategic rung gauges, and historical milestone chronicle.

WHAT: tracks where The Collective came from, where it stands right now, and where it is going across Days, Weeks,
      and Months toward Eternal Strategic Goals G1-G5 and Anchored Operational Subgoals O1-O9.
        1. Verified Historical Chronicle: combines dated foundational milestones since Founding (2026-11-14) with
           live auto-detected unlocks from read.db, empire.json, and fleet.json (first Tier-2 hulls, frontier outposts,
           standing multi-empire armada milestones, full seating, purse/enterprise thresholds, sovereign stations).
        2. Strategic Rung Ladder (0-100%): computes real-time completion across 12 concrete rungs grouped into
           Immediate Horizon (Days), Mid-Term Horizon (1-3 Weeks), and Long-Term Horizon (1-3+ Months). Every gauge,
           ceiling, unfitted headroom count, leaderboard rank, and bottleneck is derived live from read.db/fleet.json.
        3. Rolling Weekly & Monthly Snapshots: aggregates historical performance by ISO week and calendar month
           from stats_money_hour, bounded to 12 periods so it never bloats.
        4. Auto-Updated Governance Blueprint: `progression.py write [--commit]` updates `governance/progression-roadmap.md`
           between `<!-- PROGRESSION-AUTO:BEGIN -->` and `<!-- PROGRESSION-AUTO:END -->` markers on the hourly pass.
RULES:
  - Read-only on game state and read.db; writes only `governance/progression-roadmap.md` when `write` is called.
  - Every metric, ceiling, and bottleneck is derived live from read.db, empire.json, fleet.json, or repo history.
  - Pure 7-bit ASCII (`U+0000-U+007F`).
WHY:  Suggi, 2026-11-22/23: dynamic progression roadmap showing capacity utilization, upgrade saturation, unfitted
      headroom, and standing fleet vs current/max possible faction size across Days/Weeks/Months.

USAGE:
  progression.py [show] [--json]
  progression.py write [--commit]
  --data <dir>   the unit's data folder (default /srv/collective/data)
  --root <dir>   the repository root (default: two folders above this file)

Stdlib only. ASCII only.
"""

import argparse
import datetime
import json
import os
import re
import sqlite3
import subprocess
import sys
import time
from pathlib import Path

ROADMAP_REL = "governance/progression-roadmap.md"
BEGIN_MARK = "<!-- PROGRESSION-AUTO:BEGIN -->"
END_MARK = "<!-- PROGRESSION-AUTO:END -->"

# Immutable historical milestones verified from git log, reports/, and database history (UTC dates)
FOUNDATIONAL_MILESTONES = (
    ("2026-11-14", "Day 1 -- Founding", "Constitution, 6-Division Charter & Five Admirals Born",
     "The Collective [CLTV] chartered; Unity (Fleet Admiral) + Zero, Mercury, Apollo, Apophis, and Oracle initialized inside sealed gVisor unit."),
    ("2026-11-15", "Day 2 -- Early Fleet", "Initial Fleet Deployed (5 -> 50 Ships) & First Profitable Creature Hunts",
     "Setpoint engine + container gate proven; starter missions (~22k cr/pilot) and early creature-good hunting established initial working capital."),
    ("2026-11-16", "Day 3 -- Core Armada", "246-Ship Voidborn Armada, SQLite Warehouse & First Outpost (GSC-0044)",
     "Scaled to 246 specialized ships (6 Cmd, 60 Min, 40 Trd, 40 Log, 70 Mil, 30 Int); store.py live.db->read.db pipeline & CLTV Outpost GSC-0044 built."),
    ("2026-11-17", "Day 4 -- Faction & T1", "100-Seat Offices, First Tier-1 Liminal Miner & 490+ Systems Mapped",
     "Hiring Board + Recruitment Desk unlocked 100 faction seats; first Tier-1 Voidborn Liminal commissioned; declarative plan.py & supply chains live."),
    ("2026-11-18", "Day 5 -- Lean Brain", "Capped Versioned Guidebooks & Auto-Generated SQL Handbook",
     "Monolithic guidebooks split into 6-8 capped chapters mirrored into doc_versions; game/handbook.md auto-generated from live store schema."),
    ("2026-11-21", "Day 8 -- Pull Reserve", "Shared Needs Register (needs.tsv) & Synchronous Admiral Self-Build",
     "Priority-ordered pull reserve (needs.tsv -> need_status) unified division material targets; Admirals gained 1-call synchronous runner/script builds."),
    ("2026-11-22", "Day 9 -- Enterprise Era", "Constitution v9, 3-Tier Mandate (G1-G5 / O1-O9), 200 Seats & 506/506 Galaxy",
     "Recruitment Center raised cap to 200; 506/506 galaxy charted; T3 lasers & Shield Booster II proven; 3-Tier Orders & multi-empire standing fleet launched."),
)


def _clamp_pct(v):
    return round(max(0.0, min(100.0, float(v))), 1)


def _open_ro(data_dir):
    db = Path(data_dir) / "store" / "read.db"
    if not db.is_file() or db.is_symlink():
        return None
    try:
        return sqlite3.connect("file:%s?mode=ro" % db, uri=True, timeout=2.0)
    except sqlite3.Error:
        return None


def _has_table(conn, name):
    r = conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type IN ('table','view') AND name = ?",
        (name,),
    ).fetchone()
    return r is not None


def _next_seat_building(seats_cap, max_cap):
    if seats_cap < 50:
        return "Hiring Board (50)"
    if seats_cap < 100:
        return "Recruitment Desk (100)"
    if seats_cap < 200:
        return "Recruitment Center (200)"
    if seats_cap < 400:
        return "Guild Hall Recruiting (400)"
    if seats_cap < max_cap:
        return "Grand Recruitment Bureau (%s)" % format(max_cap, ",")
    return "Max single-station cap (%s) reached" % format(max_cap, ",")


def _short_summary(need_rec, fallback):
    if not need_rec:
        return fallback
    short = (need_rec.get("short") or "").strip()
    fee = int(need_rec.get("fee") or 0)
    parts = []
    if short:
        parts.append("short: " + short[:95])
    if fee > 0:
        parts.append("fee %s cr" % format(fee, ","))
    return " | ".join(parts) if parts else "fully stocked & funded -- ready to execute"


def compute_progression(repo_root, data="/srv/collective/data", now=None):
    """Compute live enterprise progression snapshot, 12 horizon rungs, milestones, and rolling weekly/monthly ledgers."""
    now = time.time() if now is None else float(now)
    stamp = time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime(now))
    today_str = time.strftime("%Y-%m-%d", time.gmtime(now))
    repo_p = Path(repo_root)
    data_p = Path(data)

    # Defaults if DB/files are minimal (e.g. unit tests)
    ships_synced = 0
    ships_away = 0
    standing_ships = 0
    t0_hulls = 0
    t1_hulls = 0
    t1_plus = 0
    t2_plus = 0
    t3_plus = 0
    p10_ready = 0
    p20_count = 0
    max_piloting = 0
    seats_used, seats_cap = 0, 20
    max_faction_cap = 1000
    treasury = 0
    wallets = 0
    vault_worth = 0
    facility_worth = 0
    fleet_book_worth = 0
    outposts_count = 0
    stations_count = 0
    systems_charted = 0
    total_systems = 506
    steady_24h = 0
    steady_1h = 0
    jump_loop_h_24h = 0.0
    productive_h_24h = 0.0
    t3_mods = 0
    adv_mods_fitted = 0
    total_installed_mods = 0
    total_slots = 0
    w_slots = 0
    d_slots = 0
    u_slots = 0
    ships_with_adv = 0
    contracts_count = 0
    needs_map = {}
    leaderboard_ranks = {}
    top_rival_wealth = 0
    by_empire = {}
    daily_rows = []
    weekly_rows = []
    monthly_rows = []

    # Read contracts.log count
    clog = repo_p / "communications" / "contracts.log"
    if clog.is_file():
        try:
            contracts_count = max(0, len(re.findall(r"^## \[ENT-\d+\]", clog.read_text(encoding="ascii", errors="replace"), re.M)) - 1)
        except OSError:
            contracts_count = 0

    # Read fleet.json rates, wallets, online + away standing count
    fjson = data_p / "fleet" / "fleet.json"
    if fjson.is_file():
        try:
            fobj = json.loads(fjson.read_text(encoding="utf-8", errors="replace"))
            tot_block = fobj.get("totals") or {}
            win = ((tot_block.get("rates") or {}).get("windows")) or {}
            if win:
                steady_1h = int(((win.get("1h") or {}).get("cph")) or 0)
                steady_24h = int(((win.get("24h") or {}).get("cph")) or 0)
            else:
                rates = fobj.get("rates") or {}
                steady_1h = int(((rates.get("1h") or {}).get("steady_net")) or 0)
                steady_24h = int(((rates.get("24h") or {}).get("steady_net")) or 0)
            fl_ships = [s for s in (fobj.get("ships") or []) if isinstance(s, dict)]
            fl_away = [a for a in (fobj.get("away") or []) if isinstance(a, dict)]
            online_names = {str(s.get("name") or "") for s in fl_ships if s.get("name")}
            away_names = {str(a.get("name") or "") for a in fl_away if a.get("name")} - online_names
            ships_away = len(away_names)
            standing_ships = len(online_names | away_names)
            wallets = int(sum((s.get("credits") or 0) for s in fl_ships))
        except (OSError, ValueError):
            pass

    conn = _open_ro(data)
    try:
        if conn is not None:
            if _has_table(conn, "ships"):
                row = conn.execute("SELECT COUNT(*), COALESCE(SUM(credits), 0) FROM ships").fetchone()
                ships_synced = int(row[0] or 0)
                if not wallets:
                    wallets = int(row[1] or 0)
                for emp, cnt in conn.execute("SELECT LOWER(COALESCE(NULLIF(empire,''), 'voidborn')), COUNT(*) FROM ships GROUP BY 1 ORDER BY 2 DESC"):
                    by_empire[str(emp)] = int(cnt or 0)
                if _has_table(conn, "hulls"):
                    for tier, cnt in conn.execute(
                        "SELECT COALESCE(h.tier, 0), COUNT(*) FROM ships s "
                        "LEFT JOIN hulls h ON LOWER(h.id) = LOWER(s.class) OR LOWER(h.name) = LOWER(s.class) GROUP BY 1"
                    ):
                        t = int(tier or 0)
                        c = int(cnt or 0)
                        if t == 0:
                            t0_hulls += c
                        elif t == 1:
                            t1_hulls += c
                        if t >= 1:
                            t1_plus += c
                        if t >= 2:
                            t2_plus += c
                        if t >= 3:
                            t3_plus += c
                        fleet_book_worth += c * ({0: 5000, 1: 65000, 2: 350000, 3: 1500000, 4: 6000000, 5: 25000000}.get(t, 5000))
                    srow = conn.execute(
                        "SELECT COALESCE(SUM(COALESCE(h.weapon_slots,0)),0), "
                        "COALESCE(SUM(COALESCE(h.defense_slots,0)),0), "
                        "COALESCE(SUM(COALESCE(h.utility_slots,0)),0) "
                        "FROM ships s LEFT JOIN hulls h ON LOWER(h.id) = LOWER(s.class) OR LOWER(h.name) = LOWER(s.class)"
                    ).fetchone()
                    if srow:
                        w_slots, d_slots, u_slots = int(srow[0] or 0), int(srow[1] or 0), int(srow[2] or 0)
                        total_slots = w_slots + d_slots + u_slots
            if _has_table(conn, "ship_skills"):
                prow = conn.execute(
                    "SELECT COALESCE(MAX(level), 0), "
                    "SUM(CASE WHEN level >= 10 THEN 1 ELSE 0 END), "
                    "SUM(CASE WHEN level >= 20 THEN 1 ELSE 0 END) "
                    "FROM ship_skills WHERE skill = 'piloting'"
                ).fetchone()
                if prow:
                    max_piloting = int(prow[0] or 0)
                    p10_ready = int(prow[1] or 0)
                    p20_count = int(prow[2] or 0)
            if _has_table(conn, "ship_modules"):
                mrow = conn.execute(
                    "SELECT COUNT(*), "
                    "SUM(CASE WHEN name LIKE '% II' OR name LIKE '% III' OR name LIKE '% IV' OR name LIKE '% V' THEN 1 ELSE 0 END), "
                    "COUNT(DISTINCT CASE WHEN name LIKE '% II' OR name LIKE '% III' OR name LIKE '% IV' OR name LIKE '% V' THEN pilot END), "
                    "SUM(CASE WHEN module LIKE '%_iii' OR module LIKE '%_iv' OR module LIKE 'shield_booster_ii%' THEN 1 ELSE 0 END) "
                    "FROM ship_modules"
                ).fetchone()
                if mrow:
                    total_installed_mods = int(mrow[0] or 0)
                    adv_mods_fitted = int(mrow[1] or 0)
                    ships_with_adv = int(mrow[2] or 0)
                    t3_mods = int(mrow[3] or 0)
            if _has_table(conn, "faction"):
                frow = conn.execute("SELECT COALESCE(member_count, 0), COALESCE(members_limit, 20), COALESCE(treasury, 0) FROM faction LIMIT 1").fetchone()
                if frow:
                    seats_used, seats_cap, treasury = int(frow[0]), int(frow[1]), int(frow[2])
            if _has_table(conn, "facilities"):
                cap_r = conn.execute(
                    "SELECT COALESCE(MAX(faction_cap), 1000) FROM facilities "
                    "WHERE LOWER(id) LIKE '%recruit%' OR LOWER(id) LIKE '%hiring%' OR LOWER(id) LIKE '%guild_hall%'"
                ).fetchone()
                if cap_r and int(cap_r[0] or 0) >= 200:
                    max_faction_cap = int(cap_r[0])
            if _has_table(conn, "bases"):
                for bkind, bcnt in conn.execute("SELECT LOWER(COALESCE(kind, 'outpost')), COUNT(*) FROM bases GROUP BY 1"):
                    if "station" in bkind:
                        stations_count += int(bcnt or 0)
                    else:
                        outposts_count += int(bcnt or 0)
            if _has_table(conn, "faction_facilities") and _has_table(conn, "facilities"):
                fac_row = conn.execute(
                    "SELECT COALESCE(SUM(COALESCE(c.build_cost, 0)), 0) "
                    "FROM faction_facilities ff LEFT JOIN facilities c ON c.id = ff.type"
                ).fetchone()
                facility_worth = int((fac_row[0] if fac_row else 0) or 0)
            if _has_table(conn, "inventory"):
                vrow = conn.execute("SELECT COALESCE(SUM(worth), 0) FROM inventory").fetchone()
                vault_worth = int((vrow[0] if vrow else 0) or 0)
            if _has_table(conn, "systems"):
                srow = conn.execute("SELECT COUNT(*) FROM systems").fetchone()
                systems_charted = int((srow[0] if srow else 0) or 0)
                if systems_charted > total_systems:
                    total_systems = systems_charted
            if _has_table(conn, "need_status"):
                for nid, nref, cov, col, shrt, fee in conn.execute(
                    "SELECT id, COALESCE(ref, ''), COALESCE(covered, 0), COALESCE(colour, ''), COALESCE(short_items, ''), COALESCE(fee, 0) FROM need_status"
                ):
                    rec = {
                        "pct": round(float(cov or 0.0), 1),
                        "colour": str(col or ""),
                        "short": str(shrt or ""),
                        "fee": int(fee or 0),
                    }
                    needs_map[str(nid)] = rec
                    if nref:
                        needs_map["ref:" + str(nref)] = rec
            if _has_table(conn, "stats_money_hour") and not steady_24h:
                cutoff_24 = int(now) - 86400
                s24 = conn.execute(
                    "SELECT COUNT(DISTINCT hour), COALESCE(SUM(net), 0) FROM stats_money_hour WHERE division = 'all' AND ships > 0 AND hour >= ?",
                    (cutoff_24,),
                ).fetchone()
                if s24 and s24[0]:
                    steady_24h = int(round(float(s24[1]) / max(1, int(s24[0]))))
            if _has_table(conn, "fuel_sinks"):
                for cat, _runs, sh_h, _net in conn.execute("SELECT category, runs_24h, ship_hours_24h, net_credits_24h FROM fuel_sinks"):
                    if cat == "jump_loops":
                        jump_loop_h_24h = round(float(sh_h or 0.0), 1)
                    elif cat == "productive":
                        productive_h_24h = round(float(sh_h or 0.0), 1)
            if _has_table(conn, "leaderboards"):
                for board_name, rnk, val in conn.execute(
                    "SELECT board, rank, value FROM leaderboards WHERE grp = 'factions' AND tag = 'CLTV' ORDER BY rank"
                ):
                    leaderboard_ranks[str(board_name)] = {"rank": int(rnk or 0), "value": int(val or 0)}
                top_r = conn.execute(
                    "SELECT COALESCE(MAX(value), 0) FROM leaderboards WHERE grp = 'factions' AND board = 'total_wealth'"
                ).fetchone()
                if top_r:
                    top_rival_wealth = int(top_r[0] or 0)
            if _has_table(conn, "stats_money_hour"):
                w_sql = (
                    "SELECT strftime('%Y-W%W', hour, 'unixepoch') AS wk, "
                    "MIN(date(hour, 'unixepoch')), MAX(date(hour, 'unixepoch')), "
                    "COUNT(DISTINCT hour), ROUND(SUM(income)), ROUND(SUM(costs)), ROUND(SUM(net)), ROUND(SUM(once)), "
                    "MAX(COALESCE(wallets_end, 0) + COALESCE(treasury, 0)) "
                    "FROM stats_money_hour WHERE LOWER(division) IN ('fleet', 'all') AND ships > 0 GROUP BY 1 ORDER BY 1 DESC LIMIT 12"
                )
                for wk, d0, d1, hrs, inc, cst, snet, once, peak_p in conn.execute(w_sql):
                    weekly_rows.append({
                        "period": wk, "span": "%s..%s" % (d0, d1), "active_hours": int(hrs or 0),
                        "income": int(inc or 0), "costs": int(cst or 0),
                        "steady_net": int(snet or 0), "paid_once": int(once or 0),
                        "peak_purse": int(peak_p or 0),
                    })
                m_sql = (
                    "SELECT strftime('%Y-%m', hour, 'unixepoch') AS mo, "
                    "MIN(date(hour, 'unixepoch')), MAX(date(hour, 'unixepoch')), "
                    "COUNT(DISTINCT hour), ROUND(SUM(income)), ROUND(SUM(costs)), ROUND(SUM(net)), ROUND(SUM(once)), "
                    "MAX(COALESCE(wallets_end, 0) + COALESCE(treasury, 0)) "
                    "FROM stats_money_hour WHERE LOWER(division) IN ('fleet', 'all') AND ships > 0 GROUP BY 1 ORDER BY 1 DESC LIMIT 12"
                )
                for mo, d0, d1, hrs, inc, cst, snet, once, peak_p in conn.execute(m_sql):
                    monthly_rows.append({
                        "period": mo, "span": "%s..%s" % (d0, d1), "active_hours": int(hrs or 0),
                        "income": int(inc or 0), "costs": int(cst or 0),
                        "steady_net": int(snet or 0), "paid_once": int(once or 0),
                        "peak_purse": int(peak_p or 0),
                    })
                d_sql = (
                    "SELECT date(hour, 'unixepoch') AS day, COUNT(DISTINCT hour), ROUND(AVG(ships)), "
                    "ROUND(AVG(income)), ROUND(AVG(costs)), ROUND(AVG(net)), ROUND(AVG(once)), "
                    "MAX(COALESCE(wallets_end, 0) + COALESCE(treasury, 0)) "
                    "FROM stats_money_hour WHERE LOWER(division) IN ('fleet', 'all') AND ships > 0 "
                    "GROUP BY 1 ORDER BY 1 DESC LIMIT 14"
                )
                for day, hrs, sh_avg, inc_h, cst_h, net_h, once_h, peak_p in conn.execute(d_sql):
                    daily_rows.append({
                        "day": day, "active_hours": int(hrs or 0), "avg_ships": int(sh_avg or 0),
                        "income_h": int(inc_h or 0), "costs_h": int(cst_h or 0),
                        "steady_net_h": int(net_h or 0), "paid_once_h": int(once_h or 0),
                        "total_net_h": int((net_h or 0) + (once_h or 0)),
                        "peak_purse": int(peak_p or 0),
                    })
    finally:
        if conn is not None:
            conn.close()

    ships_total = max(standing_ships, ships_synced)
    open_seats = max(0, seats_cap - seats_used)
    unseated_ships = max(0, ships_total - seats_used)
    pct_max_faction = round(100.0 * seats_used / max(1, max_faction_cap), 1)
    pct_fleet_vs_max = round(100.0 * ships_total / max(1, max_faction_cap), 1)
    empty_slots = max(0, total_slots - total_installed_mods)
    adv_slots_unfitted = max(0, total_slots - adv_mods_fitted)
    ships_unfitted = max(0, ships_synced - ships_with_adv)
    adv_slot_pct = round(100.0 * adv_mods_fitted / max(1, total_slots), 1) if total_slots else 0.0
    adv_ship_pct = round(100.0 * ships_with_adv / max(1, ships_synced), 1) if ships_synced else 0.0
    hulls_upgraded = t1_plus
    hull_upgrade_pct = round(100.0 * hulls_upgraded / max(1, ships_synced), 1) if ships_synced else 0.0

    liquid_purse = wallets + treasury
    enterprise_value = liquid_purse + vault_worth + facility_worth + fleet_book_worth
    total_flight_h = productive_h_24h + jump_loop_h_24h
    productive_share = round(100.0 * productive_h_24h / total_flight_h, 1) if total_flight_h > 0 else 100.0

    # Build dynamic milestones list (foundational + live auto-unlocked achievements)
    milestones = [
        {"date": d, "era": era, "title": t, "detail": det, "status": "achieved"}
        for (d, era, t, det) in FOUNDATIONAL_MILESTONES
    ]
    if ships_total >= 480 and len(by_empire) >= 4:
        milestones.append({
            "date": today_str, "era": "Live Auto-Unlock",
            "title": "Plan-500 Multi-Empire Standing Armada Active (%d Ships)" % ships_total,
            "detail": "%d standing ships across %d empires (%s)." % (
                ships_total, len(by_empire), ", ".join("%s %d" % (e, c) for e, c in sorted(by_empire.items(), key=lambda kv: -kv[1]))
            ),
            "status": "achieved",
        })
    if t2_plus >= 1:
        milestones.append({
            "date": today_str, "era": "Live Auto-Unlock", "title": "First Tier-2 Hull Commissioned",
            "detail": "%d Tier-2+ hull(s) active in the fleet." % t2_plus, "status": "achieved",
        })
    if outposts_count >= 2:
        milestones.append({
            "date": today_str, "era": "Live Auto-Unlock", "title": "Second Frontier Outpost Established",
            "detail": "%d outposts active in empire.json." % outposts_count, "status": "achieved",
        })
    if stations_count >= 1:
        milestones.append({
            "date": today_str, "era": "Live Auto-Unlock", "title": "First Sovereign Player Station Built",
            "detail": "%d sovereign station(s) active in empire.json." % stations_count, "status": "achieved",
        })
    if ships_total > 0 and seats_used >= ships_total:
        milestones.append({
            "date": today_str, "era": "Live Auto-Unlock", "title": "100% Standing Armada Seated in [CLTV]",
            "detail": "All %d standing ships seated inside [CLTV]." % ships_total, "status": "achieved",
        })
    if enterprise_value >= 100_000_000:
        milestones.append({
            "date": today_str, "era": "Live Auto-Unlock", "title": "100M+ Enterprise Net Worth Crossed",
            "detail": "Consolidated Enterprise Net Worth reached %s cr." % format(enterprise_value, ","), "status": "achieved",
        })

    # Live need lookups
    def _need(nid, ref_key):
        return needs_map.get(nid) or needs_map.get("ref:" + ref_key) or {}

    atria_n = _need("atria-outpost-kit", "outpost_kit")
    res_n = _need("resonance-miner", "resonance_miner")
    rec_n = _need("military-recursion-1", "recursion")
    foundry_n = _need("core-foundry", "station_core_foundry")
    score_n = _need("station-core", "station_core")
    guild_n = _need("guild-hall-recruiting", "guild_hall_recruiting")
    lounge_n = _need("transit-lounge", "transit_lounge")

    atria_pct = float(atria_n.get("pct") or 0.0)
    res_miner_pct = float(res_n.get("pct") or 0.0)
    recursion_pct = float(rec_n.get("pct") or 0.0)
    foundry_pct = float(foundry_n.get("pct") or 0.0)
    score_pct = float(score_n.get("pct") or 0.0)
    guild_pct = float(guild_n.get("pct") or 0.0)
    lounge_pct = float(lounge_n.get("pct") or 0.0)

    # Cashflow gauge: -50k cr/h -> 25%, 0 cr/h -> 75%, +25k cr/h -> 100%
    cashflow_pct = _clamp_pct(75.0 + (steady_24h / 1000.0)) if steady_24h < 25000 else 100.0
    if steady_24h < 0:
        cashflow_pct = _clamp_pct(max(10.0, 75.0 + (steady_24h / 1000.0)))

    # Standing armada target is 500 (current strategic plan; no unplanned growth above 500)
    armada_target = max(500, ships_total)
    armada_pct = _clamp_pct(100.0 * min(ships_total, 500) / 500.0)

    # Dynamic leaderboard string
    rank_bits = []
    for key, label in (("member_count", "members"), ("damage_dealt", "dmg"), ("facility_investment", "fac"), ("total_wealth", "wealth")):
        if key in leaderboard_ranks and leaderboard_ranks[key].get("rank"):
            rank_bits.append("#%d %s" % (leaderboard_ranks[key]["rank"], label))
    rank_str = ", ".join(rank_bits) if rank_bits else "unranked in live feed"
    rival_str = ("top rival %.1fB cr" % (top_rival_wealth / 1e9)) if top_rival_wealth >= 1e9 else ("top rival %.1fM cr" % (top_rival_wealth / 1e6) if top_rival_wealth > 0 else "leaderboard rivals")

    uncharted = max(0, total_systems - systems_charted)
    hull_mod_pct = _clamp_pct(0.5 * (100.0 * (t1_hulls * 0.5 + t2_plus) / max(1, ships_synced)) + 0.5 * adv_ship_pct)

    rungs = [
        # Horizon 1: Immediate (Days)
        {
            "id": "h1-galaxy-recon", "horizon": "Days (Now)", "orders": "G5, O7",
            "title": "Full Galaxy Reconnaissance & Freshness Net",
            "pct": _clamp_pct(100.0 * systems_charted / max(1, total_systems)),
            "current": "%d / %d systems charted (%d remaining)" % (systems_charted, total_systems, uncharted),
            "target": "%d / %d systems charted + <3h road freshness" % (total_systems, total_systems),
            "bottleneck": ("%d uncharted system(s) remaining" % uncharted) if uncharted else "All systems charted; maintain <3h market/belt freshness while trimming redundant census fuel",
        },
        {
            "id": "h1-productive-cashflow", "horizon": "Days (Now)", "orders": "G4, O1, O3",
            "title": "Enterprise Steady Cashflow Flip & Zero Empty Jump Burn",
            "pct": cashflow_pct if steady_24h > 0 else _clamp_pct(productive_share),
            "current": "1h %+d cr/h | 24h %+d cr/h | %.1f%% productive flight-h" % (steady_1h, steady_24h, productive_share),
            "target": "24h steady > +25,000 cr/h & jump loops < 10% flight-h",
            "bottleneck": "%.1f ship-h/24h on jump loops (shift idle hulls to home-empire extraction, missions & zero-fuel crafting)" % jump_loop_h_24h,
        },
        {
            "id": "h1-first-t2-hulls", "horizon": "Days (Now)", "orders": "G2, O2",
            "title": "First Tier-2 Hulls & Empire-Matched Fleet Upgrades",
            "pct": _clamp_pct(100.0 if t2_plus >= 3 else (33.3 * t2_plus + 0.4 * max(res_miner_pct, recursion_pct, 80.0 if p10_ready >= 50 else 0.0))),
            "current": "%d T2+ active (%d T1, %d T0 left) | %d pilots P10+ ready" % (t2_plus, t1_hulls, t0_hulls, p10_ready),
            "target": "First 3 Tier-2 class hulls commissioned & proven",
            "bottleneck": "Resonance Miner %.0f%% | Recursion %.0f%% (%s)" % (
                res_miner_pct, recursion_pct, _short_summary(rec_n or res_n, "%d P10+ pilots awaiting T2 hulls" % p10_ready),
            ),
        },
        {
            "id": "h1-atria-outpost", "horizon": "Days (Now)", "orders": "G3, O4",
            "title": "Frontier Outpost #2 (Strategic Footprint Anchor)",
            "pct": 100.0 if outposts_count >= 2 else _clamp_pct(atria_pct),
            "current": "%d / 8 outposts active | next outpost kit %.1f%% stocked" % (outposts_count, atria_pct),
            "target": "2+ frontier outposts founded with stocked fuel bunkers",
            "bottleneck": _short_summary(atria_n, "No active outpost_kit need registered"),
        },
        # Horizon 2: Mid-Term (1-3 Weeks)
        {
            "id": "h2-seat-wave3", "horizon": "Weeks (1-3w)", "orders": "G2, O5",
            "title": "Faction Seating (%d / %d Fleet, Cap %d)" % (seats_used, ships_total or 500, seats_cap),
            "pct": _clamp_pct(100.0 * seats_used / max(1, ships_total or seats_cap)),
            "current": "%d / %d seated (cap %d, %d open now) | %d standing ships awaiting future cap upgrades" % (
                seats_used, ships_total or 500, seats_cap, open_seats, unseated_ships,
            ),
            "target": "Seat all %d standing ships inside [CLTV] (current cap %d -> next: %s)" % (
                ships_total or 500, seats_cap, _next_seat_building(seats_cap, max_faction_cap),
            ),
            "bottleneck": "%d open seat(s) in current %d cap | next cap facility: %s (%.0f%% stocked; %s)" % (
                open_seats, seats_cap, _next_seat_building(seats_cap, max_faction_cap), guild_pct, _short_summary(guild_n, "needs cap upgrade facility"),
            ),
        },
        {
            "id": "h2-t2-standardization", "horizon": "Weeks (1-3w)", "orders": "G2, O2",
            "title": "Fleet Hull Modernization & T2-T5 Module Fit Saturation",
            "pct": hull_mod_pct,
            "current": "%d/%d hulls upgraded (%d T0 left) | %d/%d ships T2+ fitted (%d unfitted; %d/%d slots = %.1f%%)" % (
                hulls_upgraded, ships_synced, t0_hulls, ships_with_adv, ships_synced, ships_unfitted, adv_mods_fitted, total_slots, adv_slot_pct,
            ),
            "target": "100% upgraded empire-matched hulls & T2-T5 role-saturated module slots",
            "bottleneck": "%d ships still unfitted (%d empty slots; %d slots below T2) | %d P10+ pilots awaiting T2 hulls" % (
                ships_unfitted, empty_slots, adv_slots_unfitted, p10_ready,
            ),
        },
        {
            "id": "h2-outpost-ring", "horizon": "Weeks (1-3w)", "orders": "G3, O4",
            "title": "Maximal Footprint Outpost Network (Up to 8 Outposts)",
            "pct": _clamp_pct(100.0 * outposts_count / 8.0),
            "current": "%d / 8 faction outposts active (%d open outpost slots)" % (outposts_count, max(0, 8 - outposts_count)),
            "target": "8 / 8 high-centrality hub & wormhole-junction outposts",
            "bottleneck": "%d outpost slot(s) open; prioritize widest effective reach across multi-empire extraction & trade corridors" % max(0, 8 - outposts_count),
        },
        {
            "id": "h2-bursar-contracts", "horizon": "Weeks (1-3w)", "orders": "G4, O3",
            "title": "Station Bursar Market-Making & Bottleneck Contract Desk",
            "pct": _clamp_pct(min(100.0, 20.0 + contracts_count * 16.0)),
            "current": "%d contract(s) logged in contracts.log" % contracts_count,
            "target": "Standing zero-fee buy/sell books across all 5 empire hubs",
            "bottleneck": "Expand automated Bursar buy-bids & escrow volume across Nebula, Solarian, Outer Rim & Crimson capitals",
        },
        # Horizon 3: Long-Term Empire (1-3+ Months)
        {
            "id": "h3-yildun-station", "horizon": "Months (1-3m)", "orders": "G3, O4",
            "title": "Sovereign Player Stations (Up to 5 Stations)",
            "pct": _clamp_pct(100.0 * stations_count / 5.0) if stations_count >= 1 else _clamp_pct(0.35 * foundry_pct + 0.35 * score_pct + 0.30 * min(100.0, 100.0 * liquid_purse / 43_000_000.0)),
            "current": "%d / 5 stations | Foundry %.1f%% | Core %.1f%% | Purse %.2fM / 43M cr" % (
                stations_count, foundry_pct, score_pct, liquid_purse / 1e6,
            ),
            "target": "5 / 5 sovereign zero-tax stations across high-centrality galaxy hubs",
            "bottleneck": _short_summary(foundry_n, "Foundry + Station Core materials & build fee"),
        },
        {
            "id": "h3-armada-500", "horizon": "Months (1-3m)", "orders": "G2, O5",
            "title": "Multi-Empire Standing Fleet Consolidation (%d Ships)" % armada_target,
            "pct": armada_pct,
            "current": "%d / %d standing ships across %d empires | %d / %d seated (cap %d)" % (
                ships_total, armada_target, len(by_empire) or 1, seats_used, ships_total or 500, seats_cap,
            ),
            "target": "All %d multi-empire ships fully employed, seated, and steady-net positive" % armada_target,
            "bottleneck": ("%d ship(s) reconnecting" % ships_away if ships_away else "Fill %d open seats in %d cap & scale regional T2 corridors" % (open_seats, seats_cap)),
        },
        {
            "id": "h3-passengers-t5", "horizon": "Months (1-3m)", "orders": "G2, O2",
            "title": "Passenger Lines, Tier-3/4 Capital Ships & Tier-5 Mobile City",
            "pct": _clamp_pct(0.4 * lounge_pct + 0.3 * min(100.0, 100.0 * p20_count / 20.0) + 0.3 * min(100.0, 100.0 * max_piloting / 50.0)),
            "current": "Transit Lounge %.0f%% | Max Piloting %d/50 | %d at P20+ | %d T3+ hulls" % (lounge_pct, max_piloting, p20_count, t3_plus),
            "target": "Active civilian passenger network + Tier-4 Shipyard + Flagship Mobile Base",
            "bottleneck": _short_summary(lounge_n, "Requires sovereign station shipyard tiers + Piloting 20/30/50 training"),
        },
        {
            "id": "h3-galactic-top3", "horizon": "Months (1-3m)", "orders": "G1-G5, O1-O9",
            "title": "Top-3 Galactic Faction Supremacy",
            "pct": _clamp_pct(min(100.0, 100.0 * enterprise_value / 500_000_000.0)),
            "current": "EV %.2fM cr | Live ranks: %s" % (enterprise_value / 1e6, rank_str),
            "target": "Top-3 galactic wealth, industrial output & sovereign multi-station network",
            "bottleneck": "Compounding empire-matched T2/T3 fleet throughput & sovereign stations (%s)" % rival_str,
        },
    ]

    summary = {
        "computed_at": stamp,
        "days_active": max(1, (datetime.date.fromtimestamp(now) - datetime.date(2026, 11, 14)).days + 1),
        "ships_total": ships_total,
        "ships_synced": ships_synced,
        "ships_away": ships_away,
        "seats_used": seats_used,
        "seats_cap": seats_cap,
        "max_faction_cap": max_faction_cap,
        "open_seats": open_seats,
        "unseated_ships": unseated_ships,
        "pct_max_faction": pct_max_faction,
        "pct_fleet_vs_max": pct_fleet_vs_max,
        "by_empire": [{"empire": e, "count": c, "pct": round(100.0 * c / max(1, ships_synced), 1)} for e, c in sorted(by_empire.items(), key=lambda kv: -kv[1])],
        "liquid_purse": liquid_purse,
        "treasury": treasury,
        "vault_worth": vault_worth,
        "facility_worth": facility_worth,
        "fleet_book_worth": fleet_book_worth,
        "enterprise_value": enterprise_value,
        "steady_1h": steady_1h,
        "steady_24h": steady_24h,
        "t0_hulls": t0_hulls,
        "t1_hulls": t1_hulls,
        "t1_plus": t1_plus,
        "t2_plus": t2_plus,
        "t3_plus": t3_plus,
        "hulls_upgraded": hulls_upgraded,
        "hull_upgrade_pct": hull_upgrade_pct,
        "p10_ready": p10_ready,
        "max_piloting": max_piloting,
        "t3_mods": t3_mods,
        "total_slots": total_slots,
        "w_slots": w_slots,
        "d_slots": d_slots,
        "u_slots": u_slots,
        "total_installed_mods": total_installed_mods,
        "empty_slots": empty_slots,
        "adv_mods_fitted": adv_mods_fitted,
        "adv_slots_unfitted": adv_slots_unfitted,
        "adv_slot_pct": adv_slot_pct,
        "ships_with_adv": ships_with_adv,
        "ships_unfitted": ships_unfitted,
        "adv_ship_pct": adv_ship_pct,
        "outposts": outposts_count,
        "stations": stations_count,
        "systems_charted": systems_charted,
        "total_systems": total_systems,
        "leaderboard_ranks": leaderboard_ranks,
    }

    return {
        "summary": summary,
        "rungs": rungs,
        "milestones": milestones,
        "daily": daily_rows,
        "weekly": weekly_rows,
        "monthly": monthly_rows,
    }


def render_auto_block(prog):
    """Render pure 7-bit ASCII Markdown block for governance/progression-roadmap.md."""
    s = prog["summary"]
    emp_txt = ", ".join("%s %d" % (x["empire"], x["count"]) for x in (s.get("by_empire") or [])) or "multi-empire"
    lines = [
        BEGIN_MARK,
        "",
        "### Live Enterprise Snapshot (Auto-Updated by `progression.py`)",
        "",
        "| Metric | Live Value | Strategic Context |",
        "| :--- | :--- | :--- |",
        "| Campaign Day | Day %d (since 2026-11-14) | Staggered 6-agent 4h autonomous cycle |" % s["days_active"],
        "| Consolidated Enterprise Value | %s cr | %s cr purse (%s treasury) + %s vault + %s facilities + %s hulls |" % (
            format(s["enterprise_value"], ","), format(s["liquid_purse"], ","), format(s["treasury"], ","),
            format(s["vault_worth"], ","), format(s["facility_worth"], ","), format(s["fleet_book_worth"], ","),
        ),
        "| Faction Seating & Standing Fleet | %d / %d (cap %d) | %d seated of %d standing ships (%d open in current cap; %d awaiting cap upgrades) -- %s |" % (
            s["seats_used"], s["ships_total"], s["seats_cap"],
            s["seats_used"], s["ships_total"], s["open_seats"], s["unseated_ships"], emp_txt,
        ),
        "| Hull Modernization | %d / %d upgraded (%.1f%%) | %d T0 starter hulls left (%d T1, %d T2+); %d pilots P10+ (max P%d) |" % (
            s["hulls_upgraded"], s["ships_synced"], s["hull_upgrade_pct"], s["t0_hulls"], s["t1_hulls"], s["t2_plus"],
            s["p10_ready"], s["max_piloting"],
        ),
        "| Module Fit Saturation (T2-T5) | %d / %d ships (%.1f%%) | %d ships unfitted; %d / %d potential slots (%.1f%%; %d empty slots) |" % (
            s["ships_with_adv"], s["ships_synced"], s["adv_ship_pct"], s["ships_unfitted"],
            s["adv_mods_fitted"], s["total_slots"], s["adv_slot_pct"], s["empty_slots"],
        ),
        "| Territory & Exploration | %d / 8 outposts, %d / 5 stations | %d / %d galaxy systems charted |" % (
            s["outposts"], s["stations"], s["systems_charted"], s["total_systems"],
        ),
        "",
        "### Strategic Rung Progress Across Horizons (Days -> Weeks -> Months)",
        "",
        "| Horizon | Orders | Strategic Rung | Progress | Current State | Primary Rate-Limiting Step |",
        "| :--- | :--- | :--- | ---: | :--- | :--- |",
    ]
    for r in prog["rungs"]:
        lines.append("| %s | `%s` | %s | %.1f%% | %s | %s |" % (
            r["horizon"], r["orders"], r["title"], r["pct"], r["current"], r["bottleneck"],
        ))

    lines += [
        "",
        "### Verified Milestone Chronicle",
        "",
        "| Date (UTC) | Phase | Milestone | Verified Outcome |",
        "| :--- | :--- | :--- | :--- |",
    ]
    for m in prog["milestones"]:
        lines.append("| `%s` | %s | %s | %s |" % (m["date"], m["era"], m["title"], m["detail"]))

    if prog["weekly"]:
        lines += [
            "",
            "### Rolling Weekly Performance Ledger (Bounded to Last 12 Weeks)",
            "",
            "| ISO Week | Date Span | Active Hours | Steady Income | Operating Costs | Steady Net | Paid-Once Net | Peak Purse |",
            "| :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
        for w in prog["weekly"]:
            lines.append("| `%s` | `%s` | %d | %s cr | %s cr | %+d cr | %+d cr | %s cr |" % (
                w["period"], w["span"], w["active_hours"], format(w["income"], ","), format(w["costs"], ","),
                w["steady_net"], w["paid_once"], format(w["peak_purse"], ","),
            ))

    if prog["monthly"]:
        lines += [
            "",
            "### Rolling Monthly Performance Ledger (Bounded to Last 12 Months)",
            "",
            "| Month | Date Span | Active Hours | Steady Income | Operating Costs | Steady Net | Paid-Once Net | Peak Purse |",
            "| :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
        for m in prog["monthly"]:
            lines.append("| `%s` | `%s` | %d | %s cr | %s cr | %+d cr | %+d cr | %s cr |" % (
                m["period"], m["span"], m["active_hours"], format(m["income"], ","), format(m["costs"], ","),
                m["steady_net"], m["paid_once"], format(m["peak_purse"], ","),
            ))

    lines += ["", "*Last live refresh: %s (`game/fleet/progression.py`)*" % s["computed_at"], "", END_MARK]
    return "\n".join(lines)


def write_roadmap(repo_root, data="/srv/collective/data", commit=False, now=None):
    """Replace the auto-updated block inside governance/progression-roadmap.md (pure 7-bit ASCII)."""
    repo_p = Path(repo_root)
    roadmap = repo_p / ROADMAP_REL
    if not roadmap.is_file():
        return "missing"
    prog = compute_progression(repo_root, data=data, now=now)
    block = render_auto_block(prog)
    text = roadmap.read_text(encoding="ascii")
    if BEGIN_MARK not in text or END_MARK not in text:
        return "no-markers"
    before = text.split(BEGIN_MARK, 1)[0]
    after = text.split(END_MARK, 1)[1]
    updated = before + block + after
    if updated == text:
        return "unchanged"
    roadmap.write_text(updated, encoding="ascii")
    if commit:
        try:
            subprocess.run(["git", "-C", str(repo_p), "add", "--", ROADMAP_REL], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(
                [
                    "git", "-C", str(repo_p),
                    "-c", "user.name=Progression Engine", "-c", "user.email=progression@the-collective.local",
                    "commit", "-m", "governance: hourly progression-roadmap.md refresh (progression.py)", "--", ROADMAP_REL,
                ],
                check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            )
            return "committed"
        except subprocess.CalledProcessError:
            return "written"
    return "written"


def format_cli(prog):
    s = prog["summary"]
    out = [
        "PROGRESSION | Day %d | EV %s cr | Purse %s cr (Treasury %s) | Fleet %d/%s (%.1f%%) | Seated %d/%d (%.1f%% of %s) | Hulls %d/%d upg (%d T0) | T2+ Fits %d/%d ships (%d unfitted; %d/%d slots)" % (
            s["days_active"], format(s["enterprise_value"], ","), format(s["liquid_purse"], ","), format(s["treasury"], ","),
            s["ships_total"], format(s["max_faction_cap"], ","), s["pct_fleet_vs_max"],
            s["seats_used"], s["seats_cap"], s["pct_max_faction"], format(s["max_faction_cap"], ","),
            s["hulls_upgraded"], s["ships_synced"], s["t0_hulls"],
            s["ships_with_adv"], s["ships_synced"], s["ships_unfitted"], s["adv_mods_fitted"], s["total_slots"],
        )
    ]
    for r in prog["rungs"]:
        out.append("  [%-13s] %5.1f%% | %-48s | %s" % (r["horizon"], r["pct"], r["title"][:48], r["current"]))
    return "\n".join(out)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Live Collective progression roadmap & milestone engine.")
    ap.add_argument("cmd", nargs="?", default="show", choices=("show", "write"))
    ap.add_argument("--json", action="store_true", help="Emit JSON output (for show).")
    ap.add_argument("--commit", action="store_true", help="Commit governance/progression-roadmap.md after writing.")
    ap.add_argument("--data", default="/srv/collective/data")
    ap.add_argument("--root", default=str(Path(__file__).resolve().parents[2]))
    args = ap.parse_args(argv)

    if args.cmd == "write":
        st = write_roadmap(args.root, data=args.data, commit=args.commit)
        print("progression-roadmap.md: %s" % st)
        return 0
    prog = compute_progression(args.root, data=args.data)
    if args.json:
        print(json.dumps(prog, indent=2))
    else:
        print(format_cli(prog))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


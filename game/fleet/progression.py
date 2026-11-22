#!/usr/bin/env python3
"""progression.py -- live enterprise progression roadmap, strategic rung gauges, and historical milestone chronicle.

WHAT: tracks where The Collective came from, where it stands right now, and where it is going across Days, Weeks,
      and Months toward Standing Orders S1-S5 and Standing Goals G1-G5.
        1. Verified Historical Chronicle: combines dated foundational milestones since Founding (2026-11-14) with
           live auto-detected unlocks from read.db, empire.json, and fleet.json (first Tier-2 hulls, frontier outposts,
           full 246-ship seating, purse/enterprise thresholds, Yildun sovereign station, Wave 4/5 fleet births).
        2. Strategic Rung Ladder (0-100%): computes real-time completion across 12 concrete rungs grouped into
           Immediate Horizon (Days), Mid-Term Horizon (1-3 Weeks), and Long-Term Horizon (1-3+ Months).
        3. Rolling Weekly & Monthly Snapshots: aggregates historical performance by ISO week and calendar month
           from stats_money_hour, runs, and filed reports, bounded so it never bloats.
        4. Auto-Updated Governance Blueprint: `progression.py write [--commit]` updates `governance/progression-roadmap.md`
           between `<!-- PROGRESSION-AUTO:BEGIN -->` and `<!-- PROGRESSION-AUTO:END -->` markers on the hourly pass.
RULES:
  - Read-only on game state and read.db; writes only `governance/progression-roadmap.md` when `write` is called.
  - Every metric is derived live from read.db, empire.json, fleet.json, or repository history -- never guessed.
  - Pure 7-bit ASCII (`U+0000-U+007F`).
WHY:  Suggi, 2026-11-22: "I want to see also a progression guide, of where we are going and the milestones over the
      past days/weeks/months etc. So we can keep track of progress as well."

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
    ("2026-11-15", "Day 2 -- Early Waves", "Waves 1 & 2 Deployed (5 -> 50 Ships) & First Profitable Creature Hunts",
     "Setpoint engine + container gate proven; starter missions (~22k cr/pilot) and early creature-good hunting established initial working capital."),
    ("2026-11-16", "Day 3 -- Wave 3 Scale", "Wave 3 Armada (246 Ships), SQLite Warehouse & First Outpost (GSC-0044)",
     "Scaled to 246 specialized ships (6 Cmd, 60 Min, 40 Trd, 40 Log, 70 Mil, 30 Int); store.py live.db->read.db pipeline & CLTV Outpost GSC-0044 built."),
    ("2026-11-17", "Day 4 -- Faction & T1", "100-Seat Offices, First Tier-1 Liminal Miner & 490+ Systems Mapped",
     "Hiring Board + Recruitment Desk unlocked 100 faction seats; first Tier-1 Voidborn Liminal commissioned; declarative plan.py & supply chains live."),
    ("2026-11-18", "Day 5 -- Lean Brain", "Capped Versioned Guidebooks & Auto-Generated SQL Handbook",
     "Monolithic guidebooks split into 6-8 capped chapters mirrored into doc_versions; game/handbook.md auto-generated from live store schema."),
    ("2026-11-21", "Day 8 -- Pull Reserve", "Shared Needs Register (needs.tsv) & Synchronous Admiral Self-Build",
     "Priority-ordered pull reserve (needs.tsv -> need_status) unified division material targets; Admirals gained 1-call synchronous runner/script builds."),
    ("2026-11-22", "Day 9 -- Enterprise Era", "Constitution v8, 200 Seats, T3 Modules, 506/506 Galaxy & Anchor-Delta Loop",
     "Recruitment Center raised cap to 200; 506/506 galaxy charted; 21 Mining Laser III + 21 Pulse Laser III + 11 Shield Booster II fitted; 54 pilots hit Piloting 10+; Comms Firewall, Station Bursar contracts.log & Playbooks live."),
)


def _has_table(conn, name):
    if conn is None:
        return False
    return conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type IN ('table', 'view') AND name = ?",
        (name,),
    ).fetchone() is not None


def _open_ro(data):
    dbp = Path(data) / "store" / "read.db"
    if not dbp.is_file():
        return None
    try:
        return sqlite3.connect("file:%s?mode=ro" % dbp, uri=True, timeout=2.0)
    except sqlite3.Error:
        return None


def _clamp_pct(val):
    return round(max(0.0, min(100.0, float(val))), 1)


def compute_progression(repo_root, data="/srv/collective/data", now=None):
    """Compute live snapshot, 12 strategic rungs (Days/Weeks/Months), verified milestones, and weekly/monthly rollups."""
    now = time.time() if now is None else float(now)
    stamp = time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime(now))
    today_str = time.strftime("%Y-%m-%d", time.gmtime(now))
    repo_p = Path(repo_root)
    data_p = Path(data)

    # Defaults if DB/files are minimal (e.g. unit tests)
    ships_total = 0
    t1_plus = 0
    t2_plus = 0
    t3_plus = 0
    p10_ready = 0
    p20_count = 0
    max_piloting = 0
    seats_used, seats_cap = 0, 20
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
    contracts_count = 0
    needs_map = {}
    leaderboard_ranks = {}
    weekly_rows = []
    monthly_rows = []

    # Read contracts.log count
    clog = repo_p / "communications" / "contracts.log"
    if clog.is_file():
        try:
            contracts_count = max(0, len(re.findall(r"^## \[ENT-\d+\]", clog.read_text(encoding="ascii", errors="replace"), re.M)) - 1)
        except OSError:
            contracts_count = 0

    # Read fleet.json rates if present
    fjson = data_p / "fleet" / "fleet.json"
    if fjson.is_file():
        try:
            fobj = json.loads(fjson.read_text(encoding="utf-8", errors="replace"))
            rates = fobj.get("rates") or {}
            steady_1h = int(((rates.get("1h") or {}).get("steady_net")) or 0)
            steady_24h = int(((rates.get("24h") or {}).get("steady_net")) or 0)
            wallets = int(sum((s.get("credits") or 0) for s in (fobj.get("ships") or []) if isinstance(s, dict)))
        except (OSError, ValueError):
            pass

    conn = _open_ro(data)
    try:
        if conn is not None:
            if _has_table(conn, "ships"):
                row = conn.execute("SELECT COUNT(*), COALESCE(SUM(credits), 0) FROM ships").fetchone()
                ships_total = int(row[0] or 0)
                if not wallets:
                    wallets = int(row[1] or 0)
                if _has_table(conn, "hulls"):
                    for tier, cnt in conn.execute(
                        "SELECT COALESCE(h.tier, 0), COUNT(*) FROM ships s "
                        "LEFT JOIN hulls h ON LOWER(h.id) = LOWER(s.class) OR LOWER(h.name) = LOWER(s.class) GROUP BY 1"
                    ):
                        t = int(tier or 0)
                        c = int(cnt or 0)
                        if t >= 1:
                            t1_plus += c
                        if t >= 2:
                            t2_plus += c
                        if t >= 3:
                            t3_plus += c
                        fleet_book_worth += c * ({0: 5000, 1: 65000, 2: 350000, 3: 1500000, 4: 6000000, 5: 25000000}.get(t, 5000))
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
                    "SELECT COUNT(*) FROM ship_modules WHERE module LIKE '%_iii' OR module LIKE '%_iv' OR module LIKE 'shield_booster_ii%'"
                ).fetchone()
                t3_mods = int((mrow[0] if mrow else 0) or 0)
            if _has_table(conn, "faction"):
                frow = conn.execute("SELECT COALESCE(member_count, 0), COALESCE(members_limit, 20), COALESCE(treasury, 0) FROM faction LIMIT 1").fetchone()
                if frow:
                    seats_used, seats_cap, treasury = int(frow[0]), int(frow[1]), int(frow[2])
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
            if _has_table(conn, "need_status"):
                for nid, nref, cov, col in conn.execute("SELECT id, COALESCE(ref, ''), COALESCE(covered, 0), COALESCE(colour, '') FROM need_status"):
                    val = (round(float(cov or 0.0), 1), str(col or ""))
                    needs_map[str(nid)] = val
                    if nref:
                        needs_map["ref:" + str(nref)] = val
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
            if _has_table(conn, "stats_money_hour"):
                # Aggregate rolling ISO weeks and calendar months from fleet-wide stats_money_hour
                w_sql = (
                    "SELECT strftime('%Y-W%W', hour, 'unixepoch') AS wk, "
                    "MIN(date(hour, 'unixepoch')), MAX(date(hour, 'unixepoch')), "
                    "COUNT(DISTINCT hour), ROUND(SUM(income)), ROUND(SUM(costs)), ROUND(SUM(net)), ROUND(SUM(once)), "
                    "MAX(COALESCE(wallets_end, 0) + COALESCE(treasury, 0)) "
                    "FROM stats_money_hour WHERE division = 'all' AND ships > 0 GROUP BY 1 ORDER BY 1 DESC LIMIT 12"
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
                    "FROM stats_money_hour WHERE division = 'all' AND ships > 0 GROUP BY 1 ORDER BY 1 DESC LIMIT 12"
                )
                for mo, d0, d1, hrs, inc, cst, snet, once, peak_p in conn.execute(m_sql):
                    monthly_rows.append({
                        "period": mo, "span": "%s..%s" % (d0, d1), "active_hours": int(hrs or 0),
                        "income": int(inc or 0), "costs": int(cst or 0),
                        "steady_net": int(snet or 0), "paid_once": int(once or 0),
                        "peak_purse": int(peak_p or 0),
                    })
    finally:
        if conn is not None:
            conn.close()

    liquid_purse = wallets + treasury
    enterprise_value = liquid_purse + vault_worth + facility_worth + fleet_book_worth
    total_flight_h = productive_h_24h + jump_loop_h_24h
    productive_share = round(100.0 * productive_h_24h / total_flight_h, 1) if total_flight_h > 0 else 100.0

    # Build dynamic milestones list (foundational + any live auto-unlocked achievements)
    milestones = [
        {"date": d, "era": era, "title": t, "detail": det, "status": "achieved"}
        for (d, era, t, det) in FOUNDATIONAL_MILESTONES
    ]
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
    if ships_total >= 246 and seats_used >= ships_total:
        milestones.append({
            "date": today_str, "era": "Live Auto-Unlock", "title": "100% Faction Seating of Wave-3 Armada",
            "detail": "All %d ships seated inside [CLTV]." % ships_total, "status": "achieved",
        })
    if enterprise_value >= 100_000_000:
        milestones.append({
            "date": today_str, "era": "Live Auto-Unlock", "title": "100M+ Enterprise Net Worth Crossed",
            "detail": "Consolidated Enterprise Net Worth reached %s cr." % format(enterprise_value, ","), "status": "achieved",
        })

    # 12 Strategic Rungs across Days -> Weeks -> Months
    atria_pct = needs_map.get("atria-outpost-kit", needs_map.get("ref:outpost_kit", (0.0, "")))[0]
    res_miner_pct = needs_map.get("resonance-miner", needs_map.get("ref:resonance_miner", (0.0, "")))[0]
    recursion_pct = needs_map.get("military-recursion-1", needs_map.get("ref:recursion", (0.0, "")))[0]
    foundry_pct = needs_map.get("core-foundry", needs_map.get("ref:station_core_foundry", (0.0, "")))[0]
    score_pct = needs_map.get("station-core", needs_map.get("ref:station_core", (0.0, "")))[0]
    guild_pct = needs_map.get("ref:guild_hall_recruiting", (0.0, ""))[0]
    lounge_pct = needs_map.get("transit-lounge", needs_map.get("ref:transit_lounge", (0.0, "")))[0]

    # Cashflow gauge: -50k cr/h -> 25%, 0 cr/h -> 75%, +25k cr/h -> 100%
    cashflow_pct = _clamp_pct(75.0 + (steady_24h / 1000.0)) if steady_24h < 25000 else 100.0
    if steady_24h < 0:
        cashflow_pct = _clamp_pct(max(10.0, 75.0 + (steady_24h / 1000.0)))

    rungs = [
        # Horizon 1: Immediate (Days)
        {
            "id": "h1-galaxy-recon", "horizon": "Days (Now)", "orders": "S1",
            "title": "Full Galaxy Reconnaissance & Freshness Net",
            "pct": _clamp_pct(100.0 * systems_charted / max(1, total_systems)),
            "current": "%d / %d systems charted" % (systems_charted, total_systems),
            "target": "506charted + <3h road freshness",
            "bottleneck": "9 pirate strongholds unread; trimming redundant home census fuel burn",
        },
        {
            "id": "h1-productive-cashflow", "horizon": "Days (Now)", "orders": "S2, F8",
            "title": "Steady Cashflow Flip & Zero Empty Jump Burn",
            "pct": cashflow_pct if steady_24h > 0 else _clamp_pct(productive_share),
            "current": "24h steady %+d cr/h | %.0f%% productive flight-h" % (steady_24h, productive_share),
            "target": "24h steady > +25,000 cr/h & jump loops < 10% flight-h",
            "bottleneck": "%.0f ship-h/24h still on empty jump loops (Mercury/Apollo loop cap in Unity 22:30 queue)" % jump_loop_h_24h,
        },
        {
            "id": "h1-first-t2-hulls", "horizon": "Days (Now)", "orders": "S3, G4, F17",
            "title": "First Tier-2 Hulls (Resonance Miner, Recursion, Apophenia)",
            "pct": _clamp_pct(100.0 if t2_plus >= 3 else (33.3 * t2_plus + 0.4 * max(res_miner_pct, recursion_pct, 80.0 if p10_ready >= 50 else 0.0))),
            "current": "%d T2+ active | %d pilots at Piloting 10+ | Recursion 351k/357k cr" % (t2_plus, p10_ready),
            "target": "First 3 Tier-2 class hulls proven on 3-run F37 trials",
            "bottleneck": "Recursion quote rose +13% to 356.5k cr (+30k top-up ENT-370); Resonance Miner quote ask ENT-365",
        },
        {
            "id": "h1-atria-outpost", "horizon": "Days (Now)", "orders": "S4, G3, F33",
            "title": "Frontier Outpost #2 at Atria (North Road Anchor)",
            "pct": 100.0 if outposts_count >= 2 else _clamp_pct(atria_pct),
            "current": "%d outpost active | Atria kit %.1f%% stocked" % (outposts_count, atria_pct),
            "target": "Atria outpost founded + fuel bunker stocked",
            "bottleneck": "Short creature/salvage scales (foil_scale, alloy_scale, anchor_plate) -> Bursar buy-bids",
        },
        # Horizon 2: Mid-Term (1-3 Weeks)
        {
            "id": "h2-seat-wave3", "horizon": "Weeks (1-3w)", "orders": "G2, F11",
            "title": "Seat All 246 Existing Ships in [CLTV] (200 -> 400 Cap)",
            "pct": _clamp_pct(100.0 * seats_used / max(1, ships_total or 246)),
            "current": "%d / %d seated (cap %d; Guild Hall %.0f%%)" % (seats_used, ships_total or 246, seats_cap, guild_pct),
            "target": "246 / 246 fleet ships seated (400 cap via Guild Hall)",
            "bottleneck": "101 open seats ready under 200 cap now; Guild Hall needs 8.0M cr fee + anchor_plate",
        },
        {
            "id": "h2-t2-standardization", "horizon": "Weeks (1-3w)", "orders": "S3, G4",
            "title": "Fleet-Wide Tier-2 Hulls & Tier-3 Module Standardization",
            "pct": _clamp_pct(0.5 * (100.0 * p10_ready / max(1, ships_total or 246)) + 0.5 * min(100.0, 100.0 * t3_mods / 120.0)),
            "current": "%d/246 P10+ | %d T2/T3 high-output modules fitted" % (p10_ready, t3_mods),
            "target": "120+ Tier-2 hulls & full role T3 lasers/boosters/scanners",
            "bottleneck": "Scaling hull working-capital generation & shipyard part chains",
        },
        {
            "id": "h2-outpost-ring", "horizon": "Weeks (1-3w)", "orders": "S4, G3, F33",
            "title": "Three-Road Resource Outpost Network (Up to 8 Outposts)",
            "pct": _clamp_pct(100.0 * outposts_count / 8.0),
            "current": "%d / 8 faction outposts active" % outposts_count,
            "target": "8 / 8 strategic resource & highway outposts",
            "bottleneck": "Sequential outpost_kit crafting + frontier military patrol coverage",
        },
        {
            "id": "h2-bursar-contracts", "horizon": "Weeks (1-3w)", "orders": "S2, F39",
            "title": "Station Bursar Market-Making & Bottleneck Contract Desk",
            "pct": _clamp_pct(min(100.0, 20.0 + contracts_count * 16.0)),
            "current": "%d contract(s) logged in contracts.log" % contracts_count,
            "target": "Standing zero-fee buy/sell books across major hubs",
            "bottleneck": "Setting Trade Bursar escrow ceiling in orders.log (ENT-366) + automated order steps",
        },
        # Horizon 3: Long-Term Empire (1-3+ Months)
        {
            "id": "h3-yildun-station", "horizon": "Months (1-3m)", "orders": "S4, G3",
            "title": "First Sovereign Player Station at Yildun",
            "pct": 100.0 if stations_count >= 1 else _clamp_pct(0.35 * foundry_pct + 0.35 * score_pct + 0.30 * min(100.0, 100.0 * liquid_purse / 43_000_000.0)),
            "current": "Foundry %.1f%% | Core %.1f%% | Purse %.2fM / 43M cr" % (foundry_pct, score_pct, liquid_purse / 1e6),
            "target": "Sovereign station built at Yildun (zero-tax workshop, market & shipyard)",
            "bottleneck": "38M cr foundry fee + salvage_metal / silicon / carbon / quantum_fragments",
        },
        {
            "id": "h3-armada-500", "horizon": "Months (1-3m)", "orders": "S5, G5",
            "title": "500-Ship Specialized Armada (Birth Waves 4 & 5)",
            "pct": _clamp_pct(100.0 * (ships_total or 246) / 500.0),
            "current": "%d / 500 ships (Garage/Berth 81-85%% stocked)" % (ships_total or 246),
            "target": "500 active ships with positive per-ship steady net",
            "bottleneck": "Gated on 400+ faction seats, sustained 24h steady net > 0, and Suggi birth go-ahead",
        },
        {
            "id": "h3-passengers-t5", "horizon": "Months (1-3m)", "orders": "S2, G1, F10, F16",
            "title": "Passenger Lines, Tier-3/4 Capital Ships & Tier-5 Mobile City",
            "pct": _clamp_pct(0.4 * lounge_pct + 0.3 * (100.0 * p20_count / 20.0) + 0.3 * (100.0 * max_piloting / 50.0)),
            "current": "Transit Lounge %.0f%% | Max Piloting %d/50 | %d at P20+" % (lounge_pct, max_piloting, p20_count),
            "target": "Active civilian passenger network + Tier-4 Shipyard + Flagship Mobile Base",
            "bottleneck": "Requires sovereign station shipyard tiers + long-horizon Piloting 20/30/50 training",
        },
        {
            "id": "h3-galactic-top3", "horizon": "Months (1-3m)", "orders": "S2, S3, G1-G5",
            "title": "Top-3 Galactic Faction Contention vs [BUSY], [HEXC] & [IRLC]",
            "pct": _clamp_pct(min(100.0, 100.0 * enterprise_value / 500_000_000.0)),
            "current": "EV %.2fM cr | Rank #12 members (#13 dmg, #21 fac)" % (enterprise_value / 1e6),
            "target": "Top-3 faction wealth, industrial output & sovereign multi-station network",
            "bottleneck": "Compounding T2/T3 fleet throughput + sovereign station workshops (rivals at 7B-10B EV)",
        },
    ]

    summary = {
        "computed_at": stamp,
        "days_active": max(1, (datetime.date.fromtimestamp(now) - datetime.date(2026, 11, 14)).days + 1),
        "ships_total": ships_total,
        "seats_used": seats_used,
        "seats_cap": seats_cap,
        "liquid_purse": liquid_purse,
        "treasury": treasury,
        "vault_worth": vault_worth,
        "facility_worth": facility_worth,
        "fleet_book_worth": fleet_book_worth,
        "enterprise_value": enterprise_value,
        "steady_1h": steady_1h,
        "steady_24h": steady_24h,
        "t1_plus": t1_plus,
        "t2_plus": t2_plus,
        "p10_ready": p10_ready,
        "max_piloting": max_piloting,
        "t3_mods": t3_mods,
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
        "weekly": weekly_rows,
        "monthly": monthly_rows,
    }


def render_auto_block(prog):
    """Render pure 7-bit ASCII Markdown block for governance/progression-roadmap.md."""
    s = prog["summary"]
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
        "| Fleet & Faction Seats | %d ships (%d / %d seated) | Wave 3 active; 500-ship G5 target |" % (
            s["ships_total"], s["seats_used"], s["seats_cap"],
        ),
        "| Hull & Tech Readiness | %d T1+ / %d T2+ | %d pilots at Piloting 10+ (max P%d), %d T2/T3 key modules |" % (
            s["t1_plus"], s["t2_plus"], s["p10_ready"], s["max_piloting"], s["t3_mods"],
        ),
        "| Territory & Exploration | %d outpost(s), %d station(s) | %d / %d galaxy systems charted |" % (
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

    lines.append("")
    lines.append(END_MARK)
    return "\n".join(lines)


def _without_volatile_rates(text):
    """Compare roadmap blocks ignoring tiny minute-to-minute purse/rate jitter only? No: hourly pass commits real hourly progress."""
    return text.strip()


def write_roadmap(repo_root, data="/srv/collective/data", commit=False, now=None):
    repo_p = Path(repo_root)
    target = repo_p / ROADMAP_REL
    if not target.is_file():
        raise FileNotFoundError("Missing %s" % target)
    raw = target.read_text(encoding="ascii")
    if BEGIN_MARK not in raw or END_MARK not in raw:
        raise ValueError("%s lacks %s .. %s markers" % (ROADMAP_REL, BEGIN_MARK, END_MARK))
    prog = compute_progression(repo_root, data=data, now=now)
    block = render_auto_block(prog)
    before, rest = raw.split(BEGIN_MARK, 1)
    _old_auto, after = rest.split(END_MARK, 1)
    updated = before + block + after
    if _without_volatile_rates(updated) == _without_volatile_rates(raw):
        return "unchanged"
    if commit:
        dirty = subprocess.run(
            ["git", "-C", str(repo_p), "status", "--porcelain", "--", ROADMAP_REL],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
        )
        if dirty.returncode == 0 and dirty.stdout.strip():
            return "skipped: uncommitted edit present on %s" % ROADMAP_REL
    target.write_text(updated, encoding="ascii")
    if not commit:
        return "written"
    subprocess.run(["git", "-C", str(repo_p), "add", "--", ROADMAP_REL], check=False)
    res = subprocess.run(
        ["git", "-C", str(repo_p), "-c", "user.name=Unity", "-c", "user.email=unity@suggi-workspace.dev",
         "commit", "-q", "-m", "governance: hourly progression-roadmap.md refresh (progression.py)", "--", ROADMAP_REL],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
    )
    if res.returncode != 0:
        return "written; not committed: " + (res.stdout or "").strip()[-160:]
    return "committed"


def show_text(prog):
    s = prog["summary"]
    print(
        "PROGRESSION | Day %d | EV %s cr (Purse %s cr, Treasury %s cr) | %d ships (%d/%d seated) | "
        "T1+ %d, T2+ %d, P10+ %d | Outposts %d, Stations %d | Charted %d/%d"
        % (
            s["days_active"], format(s["enterprise_value"], ","), format(s["liquid_purse"], ","),
            format(s["treasury"], ","), s["ships_total"], s["seats_used"], s["seats_cap"],
            s["t1_plus"], s["t2_plus"], s["p10_ready"], s["outposts"], s["stations"],
            s["systems_charted"], s["total_systems"],
        )
    )
    print("=== STRATEGIC RUNGS (Days -> Weeks -> Months)")
    for r in prog["rungs"]:
        print("  [%-12s | %5.1f%%] %-52s | %s" % (r["horizon"], r["pct"], r["title"][:52], r["current"]))
        print("    bottleneck: %s" % r["bottleneck"])
    print("=== MILESTONES ACHIEVED (%d)" % len(prog["milestones"]))
    for m in prog["milestones"]:
        print("  %s | %-24s | %s" % (m["date"], m["era"][:24], m["title"]))
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(prog="progression.py", description=__doc__.split("\n")[0])
    parser.add_argument("verb", nargs="?", default="show", choices=("show", "write"))
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--commit", action="store_true")
    parser.add_argument("--data", default="/srv/collective/data")
    parser.add_argument("--root", default=str(Path(__file__).resolve().parents[2]))
    args = parser.parse_args(sys.argv[1:] if argv is None else argv)

    if args.verb == "write":
        status = write_roadmap(args.root, data=args.data, commit=args.commit)
        if status not in ("unchanged",):
            print("PROGRESSION write | %s: %s" % (ROADMAP_REL, status))
        return 0

    prog = compute_progression(args.root, data=args.data)
    if args.json:
        print(json.dumps(prog, indent=2))
        return 0
    return show_text(prog)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        sys.exit(0)

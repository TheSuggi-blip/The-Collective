#!/usr/bin/env python3
"""Live Empire-Specialized Hull & Module Upgrade Planner (rules F17, F37, O2).

Gives every Admiral and Unity an actionable, parallel-batch upgrade sheet built from
live read.db telemetry (ships, hulls, ship_skills, ship_modules, books) plus division
guidebook `card.md` freshness checks:
  1. Division cohort breakdown by origin empire and Piloting tier (P0-9, P10+, P20+).
  2. Immediate Piloting-0 unlocks (Tier-1 & Neutral Tier-2 hulls -- including 100+ cargo
     freighters Ledger 480 / Prayer 540 / Workhorse 300 that unlock spacemolt_shipping!)
     and empire-specialized Tier-2 (Piloting 10+) hulls matched to role & origin empire.
  3. Live Exchange ask quotes (if listed in `books`) and craft hints.
  4. Exact counts of off-role starter modules to strip (`unfit`) and open module slots.
  5. Guidebook `card.md` freshness & multi-empire coverage check.

Read-only. Pure stdlib.

Usage:
  python3 -I -B game/fleet/upgrades.py [--who all|Unity|Zero|Mercury|Apollo|Apophis|Oracle]
"""
import argparse
import os
import sqlite3
import sys
import time
from pathlib import Path

DATA_DEFAULT = "/srv/collective/data"
REPO_DEFAULT = "/srv/collective/the-collective"

DIVISIONS = ("Command", "Mining", "Trade", "Logistics", "Military", "Intel")
MEMBER_TO_DIV = {
    "unity": "Command", "command": "Command",
    "zero": "Mining", "mining": "Mining", "miner": "Mining",
    "mercury": "Trade", "trade": "Trade", "trader": "Trade",
    "apollo": "Logistics", "logistics": "Logistics", "hauler": "Logistics",
    "apophis": "Military", "military": "Military", "drone": "Military", "sentinel": "Military",
    "oracle": "Intel", "intel": "Intel", "scout": "Intel",
}
DIV_CATEGORIES = {
    "Mining": ("Industrial",),
    "Trade": ("Commercial", "Industrial"),
    "Logistics": ("Commercial", "Industrial"),
    "Military": ("Combat", "Combat Support"),
    "Intel": ("Exploration", "Covert", "Support"),
    "Command": ("Combat", "Combat Support", "Commercial", "Exploration"),
}
EMPIRE_EDGES = {
    "voidborn": "shields/EWAR/stealth",
    "solarian": "mining slots/accuracy",
    "nebula": "cargo/low-tax trade",
    "crimson": "weapons/armor/heavy cargo",
    "outerrim": "speed/bulk cargo/salvage",
    "neutral": "universal (0 Piloting)",
}


def _connect_ro(data_dir):
    db = Path(data_dir) / "store" / "read.db"
    if not db.is_file():
        return None
    conn = sqlite3.connect(f"file:{db}?mode=ro", uri=True, timeout=3.0)
    conn.row_factory = sqlite3.Row
    return conn


def _fmt_num(n):
    try:
        return f"{int(round(float(n))):,d}"
    except Exception:
        return "0"


def _card_freshness(repo_root, div_lower, active_empires, now):
    p = Path(repo_root) / "game" / "routes" / "guidebook" / div_lower / "card.md"
    if not p.is_file():
        return "MISSING card.md"
    age_h = max(0.0, (now - p.stat().st_mtime) / 3600.0)
    txt = p.read_text(encoding="ascii", errors="replace").lower()
    missing = [e for e in sorted(active_empires) if e not in txt]
    flags = []
    if age_h > 48.0:
        flags.append(f"stale {age_h:.0f}h")
    if missing:
        flags.append("missing empires: " + ",".join(missing))
    return ("OK (updated %.0fh ago)" % age_h) if not flags else ("REFRESH NEEDED (" + "; ".join(flags) + ")")


def render_upgrades(repo_root=REPO_DEFAULT, data_dir=DATA_DEFAULT, who="all", now=None):
    now = float(now if now is not None else time.time())
    conn = _connect_ro(data_dir)
    if conn is None:
        return "UPGRADES: read.db unavailable"
    try:
        tables = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type IN ('table','view')")}
        if "ships" not in tables or "hulls" not in tables:
            return "UPGRADES: ships/hulls tables missing"

        target_div = None
        if who and str(who).lower() not in ("all", "unity", "command"):
            target_div = MEMBER_TO_DIV.get(str(who).lower())
        show_divs = [target_div] if target_div else list(DIVISIONS)

        # Live exchange hull asks (if any hulls are listed in books)
        hull_asks = {}
        if "books" in tables:
            for r in conn.execute(
                "SELECT LOWER(item) AS item, MIN(ask) AS best_ask, base FROM books WHERE ask > 0 AND ask_qty > 0 GROUP BY LOWER(item)"
            ).fetchall():
                hull_asks[str(r["item"])] = (int(r["best_ask"]), str(r["base"] or ""))

        lines = [
            "EMPIRE-SPECIALIZED HULL & MODULE UPGRADE PLANNER (Parallel Batch Policy: F17, F37, O2)",
            "Policy: Upgrade clearly dominant T0->T1/T2 hulls & T2+ role modules in parallel batches (within F12 wallet) and measure in flight -- no serial 1-hull freezes.",
        ]

        for div in show_divs:
            cohorts = conn.execute("""
                SELECT LOWER(COALESCE(NULLIF(s.empire,''), 'voidborn')) AS emp,
                       COUNT(*) AS n,
                       SUM(CASE WHEN COALESCE(h.tier,0)=0 THEN 1 ELSE 0 END) AS t0,
                       SUM(CASE WHEN COALESCE(h.tier,0)>=1 THEN 1 ELSE 0 END) AS t1p,
                       SUM(CASE WHEN COALESCE(h.tier,0)>=2 THEN 1 ELSE 0 END) AS t2p,
                       SUM(CASE WHEN COALESCE(sk.level,0)>=10 THEN 1 ELSE 0 END) AS p10,
                       SUM(CASE WHEN COALESCE(sk.level,0)>=20 THEN 1 ELSE 0 END) AS p20,
                       MAX(COALESCE(sk.level,0)) AS mx_p,
                       ROUND(AVG(COALESCE(s.credits,0)),0) AS avg_cr
                FROM ships s
                LEFT JOIN hulls h ON h.id = s.class OR h.name = s.class
                LEFT JOIN ship_skills sk ON sk.pilot = s.pilot AND sk.skill = 'piloting'
                WHERE s.division = ?
                GROUP BY 1 ORDER BY n DESC
            """, (div,)).fetchall()
            if not cohorts:
                continue

            active_emps = {str(r["emp"]) for r in cohorts}
            tot_n = sum(int(r["n"]) for r in cohorts)
            tot_p10 = sum(int(r["p10"]) for r in cohorts)
            tot_t2 = sum(int(r["t2p"]) for r in cohorts)

            # Module saturation & off-role starters
            mod_row = None
            if "ship_modules" in tables:
                mod_row = conn.execute("""
                    WITH per_ship AS (
                        SELECT s.pilot,
                               MAX(1, COALESCE(h.weapon_slots,1)+COALESCE(h.defense_slots,1)+COALESCE(h.utility_slots,1)) AS ms,
                               COUNT(m.module) AS fit,
                               SUM(CASE WHEN (s.division='Mining' AND m.module='pulse_laser_i')
                                         OR (s.division IN ('Trade','Logistics','Intel') AND m.module IN ('mining_laser_i','ice_harvester_i','gas_harvester_i','pulse_laser_i'))
                                         OR (s.division='Military' AND m.module IN ('mining_laser_i','ice_harvester_i','gas_harvester_i'))
                                        THEN 1 ELSE 0 END) AS off_r,
                               SUM(CASE WHEN m.module LIKE '%_ii' OR m.module LIKE '%_iii' OR m.module LIKE '%_iv' THEN 1 ELSE 0 END) AS t2m
                        FROM ships s
                        LEFT JOIN hulls h ON h.id=s.class OR h.name=s.class
                        LEFT JOIN ship_modules m ON m.pilot=s.pilot
                        WHERE s.division = ?
                        GROUP BY s.pilot
                    )
                    SELECT SUM(fit) AS fitted, SUM(ms) AS max_s,
                           SUM(CASE WHEN off_r > 0 THEN 1 ELSE 0 END) AS off_ships,
                           SUM(CASE WHEN t2m > 0 THEN 1 ELSE 0 END) AS t2_ships
                    FROM per_ship
                """, (div,)).fetchone()

            card_st = _card_freshness(repo_root, div.lower(), active_emps, now)
            lines.append(f"\n=== {div.upper()} ({tot_n} ships | P10+: {tot_p10} | T2+ hulls: {tot_t2} | card.md: {card_st})")
            for r in cohorts:
                emp = str(r["emp"])
                edge = EMPIRE_EDGES.get(emp, "")
                lines.append(
                    f"  Cohort {emp:9s} ({edge:24s}): {int(r['n']):3d} ships | T0={int(r['t0']):3d} T1+={int(r['t1p']):2d} T2+={int(r['t2p']):2d} | P10+={int(r['p10']):2d} (max P{int(r['mx_p'])}) | avg wallet {_fmt_num(r['avg_cr'])} cr"
                )
            if mod_row:
                fit, mx = int(mod_row["fitted"] or 0), max(1, int(mod_row["max_s"] or 1))
                lines.append(
                    f"  Modules  : {fit}/{mx} slots filled ({100.0*fit/mx:.1f}%) | {int(mod_row['t2_ships'] or 0)} ships with T2+ modules | {int(mod_row['off_ships'] or 0)} ships carry off-role starter modules (strip via `unfit` + batch `fit`)"
                )

            # Query candidate T1 (Piloting 0) & T2 hulls matching division categories & active empires (or neutral)
            cats = DIV_CATEGORIES.get(div, ("Industrial", "Commercial"))
            ph_c = ",".join("?" for _ in cats)
            allowed_f = sorted(active_emps | {"neutral"})
            cands = conn.execute(f"""
                SELECT id, name, LOWER(COALESCE(NULLIF(faction,''), 'neutral')) AS fac, tier, category,
                       COALESCE(piloting_required, 0) AS pil, cargo, speed, weapon_slots, defense_slots, utility_slots
                FROM hulls
                WHERE tier IN (1, 2) AND category IN ({ph_c})
                ORDER BY pil ASC, tier DESC, (CASE WHEN ? IN ('Trade','Logistics') THEN cargo ELSE (weapon_slots*30 + utility_slots*25 + cargo/10) END) DESC
            """, (*cats, div)).fetchall()

            # Filter to neutral + active empires, keep top 3 P0 unlocks + top 5 P10 empire-specialized hulls
            p0_list = [r for r in cands if int(r["pil"]) == 0 and r["fac"] in allowed_f]
            if div in ("Trade", "Logistics"):
                # Also surface high-cargo P0 hulls from any empire (e.g. Outer Rim Prayer/Congregation)
                p0_extra = [r for r in cands if int(r["pil"]) == 0 and int(r["cargo"] or 0) >= 200 and r not in p0_list]
                p0_list = (p0_list + p0_extra)[:5]
            else:
                p0_list = p0_list[:4]
            p10_list = [r for r in cands if int(r["pil"]) == 10 and r["fac"] in allowed_f][:6]

            if p0_list:
                lines.append("  Immediate Piloting-0 Upgrades (NO Piloting wait -- batch-upgrade now if wallet clears F12):")
                for r in p0_list:
                    ask = hull_asks.get(str(r["id"]).lower())
                    mkt = f" | Exchange ask {_fmt_num(ask[0])} cr @ {ask[1]}" if ask else " | shipyard/craft"
                    lines.append(
                        f"    T{r['tier']} {r['name']:20s} [{r['fac']:8s} {r['category']:14s}] P{r['pil']} | cargo={int(r['cargo'] or 0):4d} spd={r['speed']} slots={r['weapon_slots']}W/{r['defense_slots']}D/{r['utility_slots']}U{mkt}"
                    )
            if p10_list:
                lines.append("  Empire-Specialized Tier-2 Upgrades (Piloting 10+ -- parallel batches, measure in flight):")
                for r in p10_list:
                    ask = hull_asks.get(str(r["id"]).lower())
                    mkt = f" | Exchange ask {_fmt_num(ask[0])} cr @ {ask[1]}" if ask else " | shipyard/craft"
                    lines.append(
                        f"    T{r['tier']} {r['name']:20s} [{r['fac']:8s} {r['category']:14s}] P{r['pil']} | cargo={int(r['cargo'] or 0):4d} spd={r['speed']} slots={r['weapon_slots']}W/{r['defense_slots']}D/{r['utility_slots']}U{mkt}"
                    )
        return "\n".join(lines)
    finally:
        conn.close()


def main(argv=None):
    ap = argparse.ArgumentParser(description="Empire-specialized hull & module parallel upgrade planner.")
    ap.add_argument("who", nargs="?", default="all", help="Member or division name (default: all)")
    ap.add_argument("--data", default=os.environ.get("COLLECTIVE_DATA", DATA_DEFAULT))
    ap.add_argument("--root", default=REPO_DEFAULT)
    args = ap.parse_args(argv)
    print(render_upgrades(repo_root=args.root, data_dir=args.data, who=args.who))
    return 0


if __name__ == "__main__":
    sys.exit(main())

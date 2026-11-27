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
import fcntl
import json
import os
import re
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
DIV_TOP_MODULES = {
    "Mining": ("mining_laser_iv", "mining_laser_iii", "mining_laser_ii", "ice_harvester_ii", "gas_harvester_ii", "cargo_expander_iii", "cargo_expander_ii"),
    "Military": ("pulse_laser_iii", "pulse_laser_ii", "shield_booster_iv", "shield_booster_ii", "armor_plate_iii", "armor_plate_ii"),
    "Trade": ("cargo_expander_iii", "cargo_expander_ii", "cargo_expander_i", "shield_booster_ii"),
    "Logistics": ("cargo_expander_iii", "cargo_expander_ii", "economy_passenger_cabin", "business_passenger_cabin", "cargo_expander_i", "shield_booster_ii"),
    "Intel": ("survey_scanner_ii", "survey_scanner_i", "shield_booster_iv", "shield_booster_ii"),
    "Command": ("pulse_laser_iii", "shield_booster_iv", "shield_booster_ii", "armor_plate_iii", "cargo_expander_iii"),
}
P0_SKIP_HULLS = ("floor_price", "ledger", "prayer", "workhorse", "congregation", "runner", "futures", "bonanza", "macguffin")
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
    conn = sqlite3.connect(f"file:{db}?mode=ro&immutable=1", uri=True, timeout=3.0)
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
    txt_compact = txt.replace(" ", "").replace("-", "").replace("_", "")
    missing = [e for e in sorted(active_empires) if e not in txt and e not in txt_compact]
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

        # Live exchange hull asks (books) and galaxy-wide shipyard listings (ship_listings)
        hull_asks = {}
        if "books" in tables:
            for r in conn.execute(
                "SELECT LOWER(item) AS item, MIN(ask) AS best_ask, base FROM books WHERE ask > 0 AND ask_qty > 0 GROUP BY LOWER(item)"
            ).fetchall():
                hull_asks[str(r["item"])] = (int(r["best_ask"]), str(r["base"] or ""))

        ship_deals = {}
        if "ship_listings" in tables:
            for r in conn.execute(
                "SELECT LOWER(class_id) AS cid, price, base, "
                "       (SELECT COUNT(*) FROM ship_listings s2 WHERE LOWER(s2.class_id) = LOWER(sl.class_id) AND s2.price > 0) AS cnt "
                "FROM ship_listings sl WHERE price > 0 "
                "ORDER BY price ASC"
            ).fetchall():
                cid = str(r["cid"])
                if cid not in ship_deals:
                    ship_deals[cid] = (int(r["price"]), str(r["base"] or ""), int(r["cnt"] or 1))

        lines = [
            "EMPIRE-SPECIALIZED HULL & MODULE UPGRADE PLANNER (Parallel Batch Policy: F17, F37, O2)",
            "Policy: Upgrade clearly dominant T0->T1/T2 hulls & T2+ role modules in parallel batches (within F12 wallet) and measure in flight -- no serial 1-hull freezes.",
            "Auto-Buy: `upgrades.py queue add` automatically buys a cheaper listed hull (`buy_listed_ship`) at the target station before commissioning (instant delivery, 37-90% savings).",
        ]
        if ship_deals:
            p0_hits = []
            for cid in P0_SKIP_HULLS:
                if cid in ship_deals:
                    pr, bs, cnt = ship_deals[cid]
                    p0_hits.append(f"{cid} @ {_fmt_num(pr)} cr ({bs}, {cnt})")
            if p0_hits:
                lines.append("Piloting-0 Instant T1/T2/T4 Skip Deals (`ship_listings`): " + "; ".join(p0_hits[:6]))

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
            if "books" in tables and div in DIV_TOP_MODULES:
                wanted_mods = DIV_TOP_MODULES[div]
                ph_m = ",".join("?" for _ in wanted_mods)
                m_rows = conn.execute(
                    f"SELECT item, MIN(ask) AS min_ask, SUM(ask_qty) AS qty FROM books WHERE item IN ({ph_m}) AND ask > 0 GROUP BY item",
                    list(wanted_mods),
                ).fetchall()
                m_map = {str(r["item"]): (int(r["min_ask"] or 0), int(r["qty"] or 0)) for r in m_rows}
                hints = [f"{mid} @ {_fmt_num(m_map[mid][0])} cr ({m_map[mid][1]} avail)" for mid in wanted_mods if mid in m_map]
                if hints:
                    lines.append(
                        f"  Top T2/T3 Exchange Mods (prefer T2/T3 over Tier-1 swaps): {', '.join(hints[:5])}"
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
                    cid_l = str(r["id"]).lower()
                    deal = ship_deals.get(cid_l)
                    ask = hull_asks.get(cid_l)
                    if deal:
                        mkt = f" | LISTED {_fmt_num(deal[0])} cr @ {deal[1]} ({deal[2]} avail)"
                    elif ask:
                        mkt = f" | Exchange ask {_fmt_num(ask[0])} cr @ {ask[1]}"
                    else:
                        mkt = " | shipyard/craft"
                    lines.append(
                        f"    T{r['tier']} {r['name']:20s} [{r['fac']:8s} {r['category']:14s}] P{r['pil']} | cargo={int(r['cargo'] or 0):4d} spd={r['speed']} slots={r['weapon_slots']}W/{r['defense_slots']}D/{r['utility_slots']}U{mkt}"
                    )
            if p10_list:
                lines.append("  Empire-Specialized Tier-2 Upgrades (Piloting 10+ -- parallel batches, measure in flight):")
                for r in p10_list:
                    cid_l = str(r["id"]).lower()
                    deal = ship_deals.get(cid_l)
                    ask = hull_asks.get(cid_l)
                    if deal:
                        mkt = f" | LISTED {_fmt_num(deal[0])} cr @ {deal[1]} ({deal[2]} avail)"
                    elif ask:
                        mkt = f" | Exchange ask {_fmt_num(ask[0])} cr @ {ask[1]}"
                    else:
                        mkt = " | shipyard/craft"
                    lines.append(
                        f"    T{r['tier']} {r['name']:20s} [{r['fac']:8s} {r['category']:14s}] P{r['pil']} | cargo={int(r['cargo'] or 0):4d} spd={r['speed']} slots={r['weapon_slots']}W/{r['defense_slots']}D/{r['utility_slots']}U{mkt}"
                    )
        q_txt = format_queue(data_dir, who=who)
        if q_txt:
            lines.append("")
            lines.append(q_txt)
        return "\n".join(lines)
    finally:
        conn.close()




# ---- Autonomous Batch Hull-Upgrade Queue (F12 / F17 / F37) ----

UPGRADE_FLOOR = 20000
UPGRADE_READY_FLOOR = 10000    # funding->funded tolerance for normal fuel spend while waiting          # minimum wallet kept after commissioning a hull
UPGRADE_POLL_S = 600           # seconds between read-only list_ships checks while building
UPGRADE_FUND_TIMEOUT = 48 * 3600
UPGRADE_HOLD = "hand upgrade"
ACTIVE_QUEUE_STATES = ("queued", "funding", "funded", "building")


def queue_file(data_dir):
    return Path(data_dir) / "fleet" / "upgrade_queue.json"


def load_queue(data_dir):
    p = queue_file(data_dir)
    if not p.is_file():
        return []
    try:
        raw = json.loads(p.read_text(encoding="utf-8"))
        return raw if isinstance(raw, list) else []
    except (OSError, ValueError):
        return []


def _queue_lock(data_dir):
    p = queue_file(data_dir)
    p.parent.mkdir(parents=True, exist_ok=True)
    return open(str(p) + ".lock", "a+", encoding="ascii")


def save_queue(data_dir, rows, merge=False):
    """Atomically write upgrade_queue.json under exclusive lock; merge=True preserves concurrent adds & cancels (ENT-190)."""
    p = queue_file(data_dir)
    p.parent.mkdir(parents=True, exist_ok=True)
    with _queue_lock(data_dir) as lf:
        fcntl.flock(lf, fcntl.LOCK_EX)
        try:
            final_rows = list(rows)
            if merge and p.is_file():
                try:
                    disk = json.loads(p.read_text(encoding="utf-8"))
                    if not isinstance(disk, list):
                        disk = []
                except (OSError, ValueError):
                    disk = []
                upd_by_id = {str(r.get("id")): r for r in rows if isinstance(r, dict) and r.get("id")}
                merged = []
                seen = set()
                for dr in disk:
                    if not isinstance(dr, dict):
                        continue
                    rid = str(dr.get("id") or "")
                    seen.add(rid)
                    ur = upd_by_id.get(rid)
                    if ur is None:
                        # Newly added by an Admiral during serve pass: preserve it!
                        merged.append(dr)
                    elif dr.get("state") == "cancelled" and ur.get("state") not in ("building", "done"):
                        # Concurrently cancelled by an Admiral during serve pass: honor cancel!
                        merged.append(dr)
                    else:
                        merged.append(ur)
                for ur in rows:
                    if isinstance(ur, dict) and str(ur.get("id") or "") not in seen:
                        merged.append(ur)
                final_rows = merged
            tmp = p.with_name("%s.%d.tmp" % (p.name, os.getpid()))
            tmp.write_text(json.dumps(final_rows, indent=1) + "\n", encoding="ascii")
            os.replace(tmp, p)
        finally:
            fcntl.flock(lf, fcntl.LOCK_UN)


def protected_pilots(data_dir):
    """Pilots holding or awaiting credits for an active hull upgrade: wallet.py sweep leaves them alone."""
    return {str(r.get("pilot")) for r in load_queue(data_dir)
            if isinstance(r, dict) and r.get("state") in ("queued", "funding", "funded") and r.get("pilot")}


def hold_pilots(data_dir):
    """Pilots needing exclusive shipyard access (funded to commission, or built and ready to switch)."""
    out = set()
    for r in load_queue(data_dir):
        if not isinstance(r, dict) or not r.get("pilot"):
            continue
        st = r.get("state")
        if st == "funded" or (st == "building" and (r.get("ready_to_switch") or str(r.get("note") or "").startswith("ready"))):
            out.add(str(r["pilot"]))
    return out


def _request_pilot_stop(data_dir, pilot):
    """Politely ask a pilot's active run (hosted or standalone) to end cleanly so serve_upgrades can dock it."""
    root = Path(data_dir) / "fleet"
    try:
        stop_h = root / "host" / "stop" / str(pilot)
        stop_h.parent.mkdir(parents=True, exist_ok=True)
        stop_h.touch()
        run_marker = root / "host" / "running" / (str(pilot) + ".json")
        if not run_marker.exists() and (root / "orders" / (str(pilot) + ".json")).exists():
            safe = re.sub(r"[^A-Za-z0-9._-]", "_", str(pilot))
            stop_s = root / "stop" / safe
            stop_s.parent.mkdir(parents=True, exist_ok=True)
            stop_s.touch()
    except OSError:
        pass


def _pilot_division_map(data_dir):
    out = {}
    fl_p = Path(data_dir) / "fleet" / "fleet.json"
    if fl_p.is_file():
        try:
            fl = json.loads(fl_p.read_text(encoding="utf-8"))
            for s in (fl.get("ships") or []) if isinstance(fl, dict) else []:
                nm = s.get("name") or ""
                if nm:
                    out[nm] = (str(s.get("division") or ""), int(s.get("credits") or 0), s)
        except (OSError, ValueError):
            pass
    return out


def _member_division(who):
    who_l = str(who or "").strip().lower()
    mapping = {
        "unity": "all", "command": "Command",
        "zero": "Mining", "mining": "Mining",
        "mercury": "Trade", "trade": "Trade",
        "apollo": "Logistics", "logistics": "Logistics",
        "apophis": "Military", "military": "Military",
        "oracle": "Intel", "intel": "Intel",
    }
    return mapping.get(who_l, "")


def _hull_info(data_dir, hull_id):
    conn = _connect_ro(data_dir)
    if conn is None:
        return None
    try:
        r = conn.execute(
            "SELECT id, name, tier, COALESCE(category, '') AS category, COALESCE(piloting_required, 0) AS pil, LOWER(COALESCE(faction, 'neutral')) AS fac "
            "FROM hulls WHERE LOWER(id) = ? OR LOWER(name) = ? LIMIT 1",
            (hull_id.lower(), hull_id.lower()),
        ).fetchone()
        return dict(r) if r else None
    finally:
        conn.close()


def pick_candidates(data_dir, hull_id, role=None, empire=None, min_piloting=0, count=5, division_filter=None, exclude=()):
    """Select eligible pilots from read.db sorted by highest piloting then highest wallet (least funding needed)."""
    hinfo = _hull_info(data_dir, hull_id)
    req_pil = max(int(min_piloting or 0), int(hinfo["pil"]) if hinfo else 0)
    target_tier = int(hinfo["tier"]) if hinfo else 1
    target_id = str(hinfo["id"]).lower() if hinfo else hull_id.lower()
    conn = _connect_ro(data_dir)
    if conn is None:
        return []
    excl = set(exclude or ())
    try:
        sql = """
            SELECT s.pilot, s.division, s.role, LOWER(COALESCE(s.empire, '')) AS emp,
                   LOWER(COALESCE(s.class, '')) AS cls, COALESCE(h.tier, 0) AS tier,
                   COALESCE(s.credits, 0) AS credits, COALESCE(sk.level, 0) AS pil
            FROM ships s
            LEFT JOIN hulls h ON LOWER(h.id) = LOWER(s.class) OR LOWER(h.name) = LOWER(s.class)
            LEFT JOIN ship_skills sk ON sk.pilot = s.pilot AND sk.skill = 'piloting'
            WHERE COALESCE(sk.level, 0) >= ?
        """
        params = [req_pil]
        if division_filter and division_filter != "all":
            sql += " AND LOWER(s.division) = ?"
            params.append(division_filter.lower())
        if role:
            sql += " AND LOWER(s.role) = ?"
            params.append(role.lower())
        if empire:
            sql += " AND LOWER(s.empire) = ?"
            params.append(empire.lower())
        sql += " ORDER BY pil DESC, credits DESC, s.pilot ASC"
        picks = []
        for r in conn.execute(sql, params).fetchall():
            nm = str(r["pilot"])
            if nm in excl:
                continue
            if str(r["cls"]) == target_id or int(r["tier"] or 0) >= target_tier:
                continue
            picks.append({"pilot": nm, "division": str(r["division"] or ""), "piloting": int(r["pil"] or 0),
                          "credits": int(r["credits"] or 0), "empire": str(r["emp"] or "")})
            if len(picks) >= int(count):
                break
        return picks
    finally:
        conn.close()


def queue_add(data_dir, who, hull_id, station, max_price, count=5, role=None, empire=None,
              min_piloting=0, pilots=None, provide_materials=False, now=None):
    """Queue a batch of pilots for autonomous hull upgrade (F12/F17/F37). Returns (rc, lines)."""
    now = float(time.time() if now is None else now)
    parts = [x.strip() for x in str(station or "").split(":")]
    if len(parts) != 3 or not all(parts):
        return 1, ["REFUSED: --station must be <system:poi:base>, got %r" % (station,)]
    max_price = int(max_price or 0)
    if max_price <= 0:
        return 1, ["REFUSED: --max-price must be > 0"]
    hull_clean = str(hull_id or "").strip().lower()
    if not hull_clean:
        return 1, ["REFUSED: --hull is required"]
    caller_div = _member_division(who)
    if not caller_div:
        return 1, ["REFUSED: unknown caller %r (only Unity or a division Admiral may queue upgrades)" % (who,)]
    rows = load_queue(data_dir)
    active_pilots = {str(r.get("pilot")) for r in rows if isinstance(r, dict) and r.get("state") in ACTIVE_QUEUE_STATES}
    pmap = _pilot_division_map(data_dir)
    hinfo = _hull_info(data_dir, hull_clean)
    if hinfo:
        hull_clean = str(hinfo["id"]).lower()
        hcat = str(hinfo.get("category") or "").strip()
        if caller_div != "all" and hcat:
            allowed_cats = DIV_CATEGORIES.get(caller_div, ())
            if allowed_cats and hcat.lower() not in {c.lower() for c in allowed_cats}:
                return 1, [
                    "REFUSED: hull %s (category=%s) does not match %s's allowed categories (%s) -- use a role-matched hull or ask Unity for override"
                    % (hull_clean, hcat, caller_div, ", ".join(allowed_cats))
                ]
    req_pil = max(int(min_piloting or 0), int(hinfo["pil"]) if hinfo else 0)

    chosen = []
    if pilots:
        for nm in [x.strip() for x in str(pilots).split(",") if x.strip()]:
            if nm in active_pilots:
                return 1, ["REFUSED: pilot %s already has an active entry in upgrade_queue.json" % nm]
            info = pmap.get(nm)
            pdiv = info[0] if info else ""
            if caller_div != "all" and pdiv and pdiv.lower() != caller_div.lower():
                return 1, ["REFUSED: %s belongs to %s, not %s's division (%s)" % (nm, pdiv, who, caller_div)]
            chosen.append({"pilot": nm, "division": pdiv or (caller_div if caller_div != "all" else "Command"),
                           "credits": info[1] if info else 0})
    else:
        chosen = pick_candidates(data_dir, hull_clean, role=role, empire=empire, min_piloting=req_pil,
                                 count=max(1, int(count or 1)), division_filter=caller_div, exclude=active_pilots)
        if not chosen:
            return 1, ["REFUSED: no eligible pilot found for hull=%s (min_piloting=%d, div=%s, role=%s, empire=%s)" % (
                hull_clean, req_pil, caller_div, role or "*", empire or "*")]

    batch_id = "upg-%s-%d" % (re.sub(r"[^a-z0-9]+", "-", hull_clean)[:14], int(now))
    next_num = max((int(str(r.get("id") or "0").split("-")[-1]) for r in rows if isinstance(r, dict) and str(r.get("id") or "").split("-")[-1].isdigit()), default=0) + 1
    added = []
    for c in chosen:
        entry = {
            "id": "u-%d" % next_num,
            "batch_id": batch_id,
            "pilot": c["pilot"],
            "division": c["division"],
            "by": str(who),
            "hull": hull_clean,
            "station": ":".join(parts),
            "max_price": max_price,
            "provide_materials": bool(provide_materials),
            "state": "queued",
            "created_at": int(now),
            "updated_at": int(now),
            "last_poll": 0,
            "paid": 0,
            "note": "",
        }
        next_num += 1
        rows.append(entry)
        added.append(entry)
    save_queue(data_dir, rows, merge=True)
    lines = ["UPGRADE QUEUE ADDED | batch %s | %d pilot(s) -> %s @ %s (max %s cr, by %s)" % (
        batch_id, len(added), hull_clean, ":".join(parts), _fmt_num(max_price), who)]
    for e in added:
        lines.append("  %s | %-16s | %-10s | state=%s" % (e["id"], e["pilot"], e["division"], e["state"]))
    return 0, lines


def queue_cancel(data_dir, who, target, now=None):
    """Cancel pending (queued/funding/funded) entries matching id, batch_id, or pilot."""
    now = float(time.time() if now is None else now)
    caller_div = _member_division(who)
    if not caller_div:
        return 1, ["REFUSED: unknown caller %r" % (who,)]
    rows = load_queue(data_dir)
    hits = []
    for r in rows:
        if not isinstance(r, dict):
            continue
        if target in (r.get("id"), r.get("batch_id"), r.get("pilot")):
            if r.get("state") in ("building", "done", "cancelled"):
                continue
            if caller_div != "all" and str(r.get("division") or "").lower() != caller_div.lower():
                return 1, ["REFUSED: %s belongs to %s, not %s" % (r.get("id"), r.get("division"), who)]
            r["state"] = "cancelled"
            r["updated_at"] = int(now)
            r["note"] = "cancelled by %s" % who
            hits.append(r["id"])
    if not hits:
        return 1, ["REFUSED: no cancellable (queued/funding/funded) entry matched %r" % (target,)]
    save_queue(data_dir, rows, merge=True)
    return 0, ["UPGRADE QUEUE CANCELLED | %d entry(s): %s" % (len(hits), ", ".join(hits))]


def format_queue(data_dir, who="all"):
    rows = load_queue(data_dir)
    if not rows:
        return ""
    div = _member_division(who)
    shown = [r for r in rows if isinstance(r, dict) and (not div or div == "all" or str(r.get("division") or "").lower() == div.lower())]
    if not shown:
        return ""
    active = [r for r in shown if r.get("state") in ACTIVE_QUEUE_STATES]
    recent_done = [r for r in shown if r.get("state") not in ACTIVE_QUEUE_STATES][-5:]
    lines = ["=== AUTONOMOUS HULL UPGRADE QUEUE (%d active, %d total | `upgrades.py queue add|show|cancel`)" % (len(active), len(shown))]
    for r in active + recent_done:
        lines.append("  %-6s %-16s %-10s %-14s %-10s max=%-9s paid=%-9s %s" % (
            str(r.get("id") or "")[:6], str(r.get("pilot") or "")[:16], str(r.get("division") or "")[:10],
            str(r.get("hull") or "")[:14], str(r.get("state") or "")[:10],
            _fmt_num(r.get("max_price") or 0), _fmt_num(r.get("paid") or 0), str(r.get("note") or "")[:60]))
    return "\n".join(lines)


def _extract_ships(answer):
    if isinstance(answer, dict):
        if isinstance(answer.get("ships"), list):
            return answer["ships"]
        for v in answer.values():
            found = _extract_ships(v)
            if found:
                return found
    return []


def _extract_quote_price(answer):
    blob = json.dumps(answer)
    prices = [int(m.replace(",", "")) for m in re.findall(r"Credits only:\s*([\d,]+)\s*cr", blob)]
    def walk(d):
        if isinstance(d, dict):
            for k, v in d.items():
                if k in ("credits_only", "credits_only_cost", "total_cost") and isinstance(v, (int, float)) and v > 0:
                    prices.append(int(v))
                else:
                    walk(v)
        elif isinstance(d, list):
            for v in d:
                walk(v)
    walk(answer)
    return max(prices) if prices else 0


def _extract_listings(answer):
    if isinstance(answer, dict):
        if isinstance(answer.get("listings"), list):
            return answer["listings"]
        for v in answer.values():
            found = _extract_listings(v)
            if found:
                return found
    return []


def _gate_raw(gate_mod, pilot, action, params=None, group="spacemolt_ship"):
    try:
        status, out = gate_mod.call("post", "/accounts/%s/raw" % gate_mod.q(pilot),
                                    {"toolGroup": group, "action": action, "params": params or {}}, timeout=90)
    except Exception as err:
        return False, {"error": "%s: %s" % (type(err).__name__, str(err)[:160])}
    try:
        data = json.loads(out)
    except (ValueError, TypeError):
        data = {"raw": str(out)[:300]}
    return status == 200 and '"error"' not in str(out)[:240], data


def _escape_battle(gate_mod, pilot, wait_ticks=2):
    """Break non-combatant / upgrade-held ships out of infinite in_battle stalemates (e.g. GSV Asclepius)."""
    _gate_raw(gate_mod, pilot, "stance", {"stance": "flee"}, group="spacemolt_battle")
    _gate_raw(gate_mod, pilot, "retreat", {}, group="spacemolt_battle")
    for _ in range(max(1, int(wait_ticks))):
        time.sleep(11.0)
        ok_b, b_ans = _gate_raw(gate_mod, pilot, "status", {}, group="spacemolt_battle")
        txt = json.dumps(b_ans).lower() if isinstance(b_ans, dict) else str(b_ans).lower()
        if (not ok_b) or ("not in" in txt) or ("no active battle" in txt) or ("no battle" in txt):
            return True
        _gate_raw(gate_mod, pilot, "retreat", {}, group="spacemolt_battle")
    return False


def _gate_dock_once(gate_mod, pilot, sys_id, poi_id, base_id, timeout=65, _allow_escape=True):
    try:
        status, out = gate_mod.call("post", "/accounts/%s/goal" % gate_mod.q(pilot),
                                    {"type": "prepare-at-station", "options": {"systemId": sys_id, "poiId": poi_id, "baseId": base_id, "refuel": True}},
                                    timeout=max(20, int(timeout)))
    except Exception as err:
        return False, "%s: %s" % (type(err).__name__, str(err)[:160])
    try:
        d = json.loads(out)
    except (ValueError, TypeError):
        return False, str(out)[:160]
    ok = status == 200 and bool(d.get("success"))
    msg = str(d.get("message") or d.get("error") or "")[:160]
    if (not ok) and _allow_escape and ("in_battle" in msg.lower() or "while in combat" in msg.lower()):
        if _escape_battle(gate_mod, pilot, wait_ticks=4):
            return _gate_dock_once(gate_mod, pilot, sys_id, poi_id, base_id, timeout=max(25, int(timeout)), _allow_escape=False)
    return ok, msg


def _read_live_fuel_loc(gate_mod, pilot, ship=None):
    """Read live (system_id, fuel, max_fuel, has_executing_goal) from /accounts/<pilot> with ship fallback."""
    cur_sys = str((ship or {}).get("system") or "")
    cur_fuel = (ship or {}).get("fuel")
    max_fuel = (ship or {}).get("max_fuel") or 95
    busy = False
    try:
        st_a, out_a = gate_mod.call("get", "/accounts/%s" % gate_mod.q(pilot), timeout=15)
        if st_a == 200:
            da = json.loads(out_a)
            busy = bool(da.get("hasExecutingGoal"))
            st_obj = da.get("state") or {}
            loc = st_obj.get("location") or {}
            sh = st_obj.get("ship") or {}
            if not str(loc.get("system") or ""):
                _gate_raw(gate_mod, pilot, "get_status", {}, group="spacemolt")
            else:
                raw_sys = str(loc.get("system") or "")
                if raw_sys:
                    cur_sys = re.sub(r"[^a-z0-9]+", "_", raw_sys.lower()).strip("_") or cur_sys
            if isinstance(sh.get("fuel"), (int, float)):
                cur_fuel = sh["fuel"]
            if isinstance(sh.get("max_fuel"), (int, float)) and sh["max_fuel"] > 0:
                max_fuel = sh["max_fuel"]
    except Exception:
        pass
    return cur_sys, cur_fuel, max_fuel, busy


def _gate_dock(gate_mod, pilot, sys_id, poi_id, base_id, timeout=65, data_dir=None, ship=None):
    """Dock pilot at sys_id:poi_id:base_id with automatic multi-hop public refuel staging when
    the destination exceeds current single-tank jump range (prevents long-range upgrade deadlocks)."""
    t_end = time.time() + max(25.0, float(timeout))
    cur_sys, cur_fuel, max_fuel, busy = _read_live_fuel_loc(gate_mod, pilot, ship=ship)
    if busy:
        return False, "A goal is already executing on this account. Try again shortly."
    if not data_dir:
        return _gate_dock_once(gate_mod, pilot, sys_id, poi_id, base_id, timeout=timeout)
    if not isinstance(ship, dict) or not ship.get("modules"):
        try:
            _sf = Path(data_dir) / "fleet" / "ships" / (pilot + ".json")
            if _sf.is_file():
                _sdoc = json.loads(_sf.read_text(encoding="utf-8"))
                if isinstance(_sdoc, dict):
                    ship = _sdoc
                    if not cur_sys and _sdoc.get("system"):
                        cur_sys = str(_sdoc["system"])
        except (OSError, ValueError):
            pass

    import fuelplan as _fp
    game_dir = Path(__file__).resolve().parent.parent
    lanes, _home = _fp.chart(game_dir)
    fars = _fp.strongholds(game_dir)
    stations = {s: v for s, v in _fp.fuel_stations(data_dir).items() if s not in fars}
    tried_bases = set()

    for _hop_i in range(4):
        rem = t_end - time.time()
        if rem < 20.0:
            return False, "refuel staging in progress at %s (will continue next pass)" % (cur_sys or "space")
        hop = None
        if cur_sys and cur_sys != sys_id and lanes and stations and cur_fuel is not None:
            hop = _fp.plan_refuel_hop(
                lanes, cur_sys, sys_id, stations, cur_fuel, max_fuel,
                ship=ship, skip=tried_bases, avoid=fars,
            )
        if hop is not None:
            _d, h_sys, h_poi, h_base = hop
            tried_bases.add(h_base)
            ok_h, msg_h = _gate_dock_once(gate_mod, pilot, h_sys, h_poi, h_base, timeout=min(90.0, rem))
            if not ok_h:
                if "insufficient fuel" in msg_h.lower():
                    if cur_fuel is not None and max_fuel and float(cur_fuel) >= 0.9 * float(max_fuel):
                        return False, "UNREACHABLE_TANK: %s -> %s (%s)" % (cur_sys, h_sys, msg_h[:80])
                    near = _fp.nearest_fuel(lanes, cur_sys, stations, skip=tried_bases)
                    if near and near[0] < _d:
                        tried_bases.add(near[3])
                        _gate_dock_once(gate_mod, pilot, near[1], near[2], near[3], timeout=min(70.0, max(20.0, t_end - time.time())))
                else:
                    return False, "refuel hop %s failed: %s" % (h_sys, msg_h[:100])
            else:
                _gate_raw(gate_mod, pilot, "refuel", {}, group="spacemolt")
            cur_sys, cur_fuel, max_fuel, _b = _read_live_fuel_loc(gate_mod, pilot, ship=ship)
            continue

        ok_d, msg_d = _gate_dock_once(gate_mod, pilot, sys_id, poi_id, base_id, timeout=min(120.0, rem))
        if ok_d:
            return True, msg_d
        if "in_battle" in msg_d.lower() or "while in combat" in msg_d.lower():
            if _escape_battle(gate_mod, pilot, wait_ticks=2):
                ok_d, msg_d = _gate_dock_once(gate_mod, pilot, sys_id, poi_id, base_id, timeout=min(90.0, max(25.0, t_end - time.time())))
                if ok_d:
                    return True, msg_d
        if "insufficient fuel" in msg_d.lower() and cur_sys and lanes and stations:
            # Engine refused direct jump -> plan conservative hop using 60% of current fuel estimate
            eff_fuel = float(cur_fuel) * 0.6 if isinstance(cur_fuel, (int, float)) else 25.0
            hop2 = _fp.plan_refuel_hop(
                lanes, cur_sys, sys_id, stations, eff_fuel, max_fuel,
                ship=ship, skip=tried_bases, avoid=fars,
            )
            if hop2 is None:
                hop2 = _fp.nearest_fuel(lanes, cur_sys, stations, skip=tried_bases)
            if hop2 is not None:
                tried_bases.add(hop2[3])
                ok_h2, msg_h2 = _gate_dock_once(gate_mod, pilot, hop2[1], hop2[2], hop2[3], timeout=min(90.0, max(20.0, t_end - time.time())))
                if ok_h2:
                    _gate_raw(gate_mod, pilot, "refuel", {}, group="spacemolt")
                    cur_sys, cur_fuel, max_fuel, _b = _read_live_fuel_loc(gate_mod, pilot, ship=ship)
                    continue
                return False, "refuel hop %s failed: %s" % (hop2[1], msg_h2[:100])
        return False, msg_d
    return False, "refuel staging advanced to %s (continuing next pass)" % (cur_sys or "space")


def _try_hold_upgrade(data_dir, pilot, now, division_mod):
    cur = division_mod.order_of(pilot, data_dir)
    if cur and cur != UPGRADE_HOLD:
        return False
    p = Path(data_dir) / "fleet" / "orders" / (pilot + ".json")
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps({"pilot": pilot, "what": UPGRADE_HOLD, "since": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now))}), encoding="ascii")
    return division_mod.order_of(pilot, data_dir) == UPGRADE_HOLD


def _release_upgrade(data_dir, pilot, division_mod):
    if division_mod.order_of(pilot, data_dir) == UPGRADE_HOLD:
        try:
            (Path(data_dir) / "fleet" / "orders" / (pilot + ".json")).unlink()
        except OSError:
            pass



def _norm_hull_name(val):
    return re.sub(r"[^a-z0-9]+", "_", str(val or "").strip().lower()).strip("_")


def _lookup_station_spec(data_dir, station_name):
    """Resolve a Shipyard Authority station display name (e.g. 'Frontier Station') to 'sys:poi:base'."""
    db = Path(data_dir) / "store" / "read.db"
    nm = str(station_name or "").strip().lower()
    if not nm or not db.is_file():
        return None
    nm_slug = _norm_hull_name(nm)
    con = None
    try:
        con = _connect_ro(data_dir)
        rows = con.execute("SELECT system, poi, base, name FROM places WHERE base IS NOT NULL AND base != ''").fetchall()
        for sys_id, poi_id, base_id, pname in rows:
            if (
                str(pname or "").strip().lower() == nm
                or str(base_id or "").strip().lower() == nm
                or _norm_hull_name(base_id) == nm_slug
                or _norm_hull_name(pname) == nm_slug
            ):
                return "%s:%s:%s" % (sys_id, poi_id, base_id)
    except Exception:
        return None
    finally:
        if con is not None:
            con.close()
    return None


def reconcile_built_hangars(data_dir, pmap, rows, now):
    """1. Mark already-switched 'building' rows done.
    2. Auto-enqueue orphaned pre-queue commissioned hulls from comms/messages.jsonl (e.g. hauler-53/54 Prayers)
       so serve_upgrades flies those pilots to switch_ship automatically.
    """
    changed = False
    active_pilots = set()
    for r in rows:
        if not isinstance(r, dict):
            continue
        pilot = str(r.get("pilot") or "")
        st = str(r.get("state") or "")
        if st == "building" and pilot in pmap:
            cur_cls = _norm_hull_name((pmap[pilot][2] or {}).get("class"))
            want_cls = _norm_hull_name(r.get("hull"))
            if cur_cls and want_cls and cur_cls == want_cls:
                r.pop("ready_to_switch", None)
                r["state"] = "done"
                r["updated_at"] = int(now)
                r["note"] = "reconciled: already flying %s" % r.get("hull")
                changed = True
                continue
        if st in ACTIVE_QUEUE_STATES:
            active_pilots.add(pilot)

    msg_p = Path(data_dir) / "comms" / "messages.jsonl"
    if not msg_p.is_file():
        return changed
    rec_p = Path(data_dir) / "fleet" / "hangar_reconciled.json"
    done_keys = set()
    try:
        raw_rk = json.loads(rec_p.read_text(encoding="utf-8")) if rec_p.is_file() else []
        if isinstance(raw_rk, list):
            done_keys = {str(x) for x in raw_rk}
    except Exception:
        done_keys = set()

    built_re = re.compile(r"Your commissioned ([A-Za-z0-9 _-]+?) is built and docked at ([^.]+)\.")
    seen_orphans = {}
    try:
        with open(msg_p, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                if "Shipyard Authority" not in line or "is built and docked" not in line:
                    continue
                try:
                    mj = json.loads(line)
                except ValueError:
                    continue
                m = built_re.search(str(mj.get("text") or ""))
                if not m:
                    continue
                h_slug = _norm_hull_name(m.group(1))
                st_nm = m.group(2).strip()
                p_nm = str(mj.get("to") or mj.get("pilot") or mj.get("recipient") or "").strip()
                if not p_nm or p_nm not in pmap or p_nm in active_pilots:
                    continue
                cur_cls = _norm_hull_name((pmap[p_nm][2] or {}).get("class"))
                if cur_cls == h_slug:
                    continue
                seen_orphans[p_nm] = (h_slug, st_nm)
    except OSError:
        return changed

    next_n = 1 + max((int(str(r.get("id") or "u-0").split("-")[1]) for r in rows if str(r.get("id") or "").startswith("u-") and str(r.get("id")).split("-")[1].isdigit()), default=0)
    for p_nm, (h_slug, st_nm) in sorted(seen_orphans.items()):
        spec = _lookup_station_spec(data_dir, st_nm)
        if not spec:
            continue
        base_id = spec.split(":")[2]
        rkey = "%s:%s:%s" % (p_nm, h_slug, base_id)
        if rkey in done_keys:
            continue
        rows.append({
            "id": "u-%d" % next_n,
            "pilot": p_nm,
            "hull": h_slug,
            "station": spec,
            "max_price": 0,
            "state": "building",
            "ready_to_switch": True,
            "from_hangar_scan": True,
            "reconcile_key": rkey,
            "by": "AutoReconcile",
            "created_at": int(now),
            "updated_at": int(now),
            "last_poll": 0,
            "note": "ready at %s (auto-detected built hull in hangar)" % base_id,
        })
        next_n += 1
        active_pilots.add(p_nm)
        changed = True
    return changed

def serve_upgrades(data_dir=DATA_DEFAULT, now=None, dry=False, max_actions=500, budget_s=240.0,
                   gate_mod=None, wallet_mod=None, division_mod=None, max_workers=12):
    """Advance queued hull upgrades safely (runs every 5 min inside wallet.py sweep). Bounded, non-blocking."""
    now = float(time.time() if now is None else now)
    if (Path(data_dir) / "fleet" / "STOP").exists():
        return 0
    rows = load_queue(data_dir)
    pmap = _pilot_division_map(data_dir)
    # Clean up any orphaned 'hand upgrade' order locks for pilots no longer held in upgrade_queue
    try:
        _held_now = hold_pilots(data_dir)
        _odir = Path(data_dir) / "fleet" / "orders"
        if _odir.is_dir():
            for _of in _odir.glob("*.json"):
                if _of.stem in _held_now:
                    continue
                try:
                    _od = json.loads(_of.read_text(encoding="utf-8"))
                    if isinstance(_od, dict) and _od.get("what") == UPGRADE_HOLD:
                        _of.unlink()
                except (OSError, ValueError):
                    pass
    except Exception:
        pass
    changed, actions, t0 = False, 0, time.time()
    if reconcile_built_hangars(data_dir, pmap, rows, now):
        changed = True
    active = [r for r in rows if isinstance(r, dict) and r.get("state") in ACTIVE_QUEUE_STATES]
    if not active:
        if changed and not dry:
            save_queue(data_dir, rows, merge=True)
        return 0
    here = str(Path(__file__).resolve().parent)
    if here not in sys.path:
        sys.path.insert(0, here)
    if division_mod is None:
        import division as division_mod
    if wallet_mod is None:
        import wallet as wallet_mod
    if gate_mod is None:
        import gate as gate_mod

    # Phase 1 (fast, no gate calls): advance all queued/funding rows first and persist immediately
    for r in active:
        pilot = str(r.get("pilot") or "")
        hull = str(r.get("hull") or "")
        if not pilot or not hull:
            continue
        info = pmap.get(pilot)
        credits = int(info[1]) if info else 0
        need_cr = int(r.get("max_price") or 0) + UPGRADE_FLOOR
        st0 = r.get("state")
        if st0 == "queued":
            if credits >= need_cr:
                r["state"], r["updated_at"], r["note"] = "funded", int(now), "wallet covers hull"
                changed = True
            else:
                short = need_cr - credits
                if dry:
                    print("would fund upgrade %s: %s +%s cr for %s" % (r["id"], pilot, _fmt_num(short), hull))
                else:
                    rc = wallet_mod.add_fund(data_dir, pilot, short, "upgrade %s (%s)" % (hull, r.get("batch_id") or r["id"]),
                                             hours=UPGRADE_FUND_TIMEOUT / 3600.0, now=now, who=r.get("by") or "Unity")
                    if rc == 0:
                        r["state"], r["updated_at"], r["note"] = "funding", int(now), "requested +%s cr" % _fmt_num(short)
                    else:
                        r["note"], r["updated_at"] = "fund deferred (cap/floor)", int(now)
                    changed = True
        elif st0 == "funding":
            ready_cr = int(r.get("max_price") or 0) + UPGRADE_READY_FLOOR
            if credits >= ready_cr:
                r["state"], r["updated_at"], r["note"] = "funded", int(now), "funds arrived"
                changed = True
            elif now - float(r.get("created_at") or now) > UPGRADE_FUND_TIMEOUT:
                r["state"], r["updated_at"], r["note"] = "failed", int(now), "funding timeout (48h)"
                changed = True
    if changed and not dry:
        save_queue(data_dir, rows, merge=True)
        changed = False

    # Phase 2: poll/switch building rows before new funded docks (ENT-196), then docked -> same system -> travelling
    def _dock_prio(row):
        st_rank = 0 if row.get("state") == "building" else 1
        parts = str(row.get("station") or "").split(":")
        if len(parts) != 3:
            return (st_rank, 9, str(row.get("id") or ""))
        info = pmap.get(str(row.get("pilot") or ""))
        sh = info[2] if info else {}
        if str(sh.get("docked") or "") == parts[2]:
            return (st_rank, 0, str(row.get("id") or ""))
        if str(sh.get("system") or "") == parts[0]:
            return (st_rank, 1, str(row.get("id") or ""))
        return (st_rank, 2, str(row.get("id") or ""))

    import concurrent.futures as _cf
    import threading as _th
    _save_lock = _th.Lock()

    def _process_funded_row(r):
        pilot = str(r.get("pilot") or "")
        hull = str(r.get("hull") or "")
        sys_id, poi_id, base_id = str(r.get("station") or "").split(":")
        info = pmap.get(pilot)
        ship = info[2] if info else {}
        credits = int(info[1]) if info else 0
        row_changed = False
        try:
            if str(ship.get("docked") or "") != base_id:
                rem_t = max(30.0, budget_s - (time.time() - t0))
                ok_d, msg_d = _gate_dock(gate_mod, pilot, sys_id, poi_id, base_id, timeout=min(180.0, rem_t), data_dir=data_dir, ship=ship)
                if not ok_d:
                    if "already executing" in msg_d.lower():
                        _request_pilot_stop(data_dir, pilot)
                    if msg_d.startswith("UNREACHABLE_TANK:"):
                        r["state"], r["note"], r["updated_at"] = "failed", msg_d[:120], int(now)
                    else:
                        r["note"], r["updated_at"] = "dock deferred: %s" % msg_d[:80], int(now)
                    row_changed = True
                    return
            ok_ls, ls_ans = _gate_raw(gate_mod, pilot, "list_ships", {})
            stored = [s for s in _extract_ships(ls_ans) if str(s.get("class_id") or "").lower() == hull
                      and not s.get("is_active") and s.get("location_base_id") == base_id] if ok_ls else []
            if stored:
                ok_sw, _ = _gate_raw(gate_mod, pilot, "switch_ship", {"ship_id": stored[0]["ship_id"]})
                if ok_sw:
                    r["state"], r["updated_at"], r["note"] = "done", int(now), "switched into stored %s" % hull
                    row_changed = True
                    return
            ok_b, b_ans = _gate_raw(gate_mod, pilot, "browse_ships", {"base_id": base_id, "class_id": hull})
            listed = [
                x for x in (_extract_listings(b_ans) if ok_b else [])
                if isinstance(x, dict) and str(x.get("class_id") or "").lower() == hull
                and int(x.get("price") or 0) > 0 and x.get("listing_id")
                and (not x.get("base_id") or str(x.get("base_id")) == base_id)
            ]
            best_listed = min(listed, key=lambda x: int(x.get("price") or 0)) if listed else None

            ok_q, q_ans = _gate_raw(gate_mod, pilot, "commission_quote", {"ship_class": hull})
            price = _extract_quote_price(q_ans) if ok_q else 0

            if best_listed is not None:
                list_price = int(best_listed.get("price") or 0)
                if list_price <= int(r["max_price"]) and (not price or list_price <= price):
                    if credits - list_price < UPGRADE_READY_FLOOR:
                        r["state"], r["updated_at"], r["note"] = "queued", int(now), "need more credits for listed %s" % _fmt_num(list_price)
                        row_changed = True
                        return
                    ok_buy, buy_ans = _gate_raw(gate_mod, pilot, "buy_listed_ship", {"listing_id": str(best_listed["listing_id"])})
                    if ok_buy:
                        try:
                            gate_mod.book_onetime(pilot, "%s hull bought from listing" % hull.capitalize(), -list_price, data=data_dir)
                        except Exception:
                            pass
                        r["state"], r["paid"], r["updated_at"], r["last_poll"] = "done", list_price, int(now), int(now)
                        q_txt = _fmt_num(price) if price else "n/a"
                        r["note"] = "bought listed %s (%s cr vs quote %s)" % (hull, _fmt_num(list_price), q_txt)
                        row_changed = True
                        print("UPGRADE bought %s: %s -> %s (%s cr, saved vs quote %s)" % (r["id"], pilot, hull, _fmt_num(list_price), q_txt), flush=True)
                        return

            if not price:
                _q_err = ""
                if isinstance(q_ans, dict):
                    _q_err = str(q_ans.get("error") or q_ans.get("message") or q_ans.get("raw") or "")
                else:
                    _q_err = str(q_ans or "")
                _ql = _q_err.lower()
                _q_fails = int(r.get("quote_fails") or 0) + 1
                r["quote_fails"] = _q_fails
                _perm = any(tok in _ql for tok in (
                    "achievement_required", "prestige hull", "not_available",
                    "invalid_ship_class", "insufficient_skill", "unknown ship",
                    "cannot commission", "locked",
                ))
                if _perm or _q_fails >= 3:
                    r["state"] = "failed"
                    r["note"] = ("quote failed: %s" % (_q_err or "quote unreadable"))[:120]
                    r["updated_at"] = int(now)
                else:
                    r["note"] = ("quote retry %d/3: %s" % (_q_fails, _q_err or "quote unreadable"))[:120]
                    r["updated_at"] = int(now)
                row_changed = True
                return
            if price > int(r["max_price"]):
                r["state"], r["updated_at"], r["note"] = "failed", int(now), "quote %s > max %s" % (_fmt_num(price), _fmt_num(r["max_price"]))
                row_changed = True
                return
            if credits - price < UPGRADE_READY_FLOOR:
                r["state"], r["updated_at"], r["note"] = "queued", int(now), "need more credits for quote %s" % _fmt_num(price)
                row_changed = True
                return
            c_params = {"ship_class": hull}
            if r.get("provide_materials"):
                c_params["provide_materials"] = True
            ok_c, c_ans = _gate_raw(gate_mod, pilot, "commission_ship", c_params)
            if ok_c:
                try:
                    gate_mod.book_onetime(pilot, "%s hull commissioned" % hull.capitalize(), -price, data=data_dir)
                except Exception:
                    pass
                r["state"], r["paid"], r["updated_at"], r["last_poll"] = "building", price, int(now), int(now)
                r["note"] = "commissioned %s (%s cr)" % (hull, _fmt_num(price))
                row_changed = True
                print("UPGRADE commissioned %s: %s -> %s (%s cr)" % (r["id"], pilot, hull, _fmt_num(price)), flush=True)
            else:
                r["note"], r["updated_at"] = "commission failed: %s" % json.dumps(c_ans)[:90], int(now)
                row_changed = True
        finally:
            _release_upgrade(data_dir, pilot, division_mod)
            if row_changed and not dry:
                with _save_lock:
                    save_queue(data_dir, [r], merge=True)

    ordered = sorted(active, key=_dock_prio)
    switch_batch = []
    funded_batch = []
    for r in ordered:
        if time.time() - t0 > budget_s:
            break
        pilot = str(r.get("pilot") or "")
        hull = str(r.get("hull") or "")
        st_parts = str(r.get("station") or "").split(":")
        if len(st_parts) != 3 or not pilot or not hull:
            continue
        sys_id, poi_id, base_id = st_parts
        info = pmap.get(pilot)
        ship = info[2] if info else {}
        credits = int(info[1]) if info else 0
        need_cr = int(r.get("max_price") or 0) + UPGRADE_FLOOR
        state = r.get("state")

        if state in ("queued", "funding"):
            continue
        if actions >= max_actions:
            continue
        if ship.get("status", "connected") != "connected" or ship.get("in_combat"):
            continue

        if state == "funded":
            if dry:
                print("would commission %s: %s -> %s @ %s (max %s cr)" % (r["id"], pilot, hull, base_id, _fmt_num(r["max_price"])))
                actions += 1
                continue
            live_row = next((x for x in load_queue(data_dir) if isinstance(x, dict) and x.get("id") == r.get("id")), None)
            if live_row and live_row.get("state") in ("cancelled", "done", "building"):
                r.update(live_row)
                continue
            if not _try_hold_upgrade(data_dir, pilot, now, division_mod):
                _request_pilot_stop(data_dir, pilot)
                r["note"], r["updated_at"] = "waiting for active run to end (stop sent)", int(now)
                with _save_lock:
                    save_queue(data_dir, [r], merge=True)
                continue
            actions += 1
            funded_batch.append(r)
            continue

        elif state == "building":
            if (not r.get("ready_to_switch")) and (now - float(r.get("last_poll") or 0) < UPGRADE_POLL_S):
                continue
            if dry:
                print("would poll building upgrade %s: %s (%s @ %s)" % (r["id"], pilot, hull, base_id))
                actions += 1
                continue
            r["last_poll"] = int(now)
            changed = True
            ok_ls, ls_ans = _gate_raw(gate_mod, pilot, "list_ships", {})
            if not ok_ls:
                continue
            stored = [s for s in _extract_ships(ls_ans) if str(s.get("class_id") or "").lower() == hull
                      and not s.get("is_active") and s.get("location_base_id") == base_id]
            if not stored:
                if r.get("from_hangar_scan"):
                    r.pop("ready_to_switch", None)
                    r["state"], r["updated_at"], r["note"] = "done", int(now), "reconciled: no stored %s at %s" % (hull, base_id)
                    rkey = str(r.get("reconcile_key") or ("%s:%s:%s" % (pilot, hull, base_id)))
                    rec_p = Path(data_dir) / "fleet" / "hangar_reconciled.json"
                    try:
                        prev_rk = json.loads(rec_p.read_text(encoding="utf-8")) if rec_p.is_file() else []
                        rk_list = sorted(set((prev_rk if isinstance(prev_rk, list) else []) + [rkey]))
                        rec_p.write_text(json.dumps(rk_list, indent=2) + "\n", encoding="utf-8")
                    except Exception:
                        pass
                continue
            r["ready_to_switch"] = True
            if not _try_hold_upgrade(data_dir, pilot, now, division_mod):
                _request_pilot_stop(data_dir, pilot)
                r["note"] = "ready at %s; waiting for pilot free (stop sent)" % base_id
                r["updated_at"] = int(now)
                changed = True
                continue
            actions += 1
            switch_batch.append((r, pilot, hull, sys_id, poi_id, base_id, ship, stored[0]["ship_id"]))

    if changed and not dry:
        with _save_lock:
            save_queue(data_dir, rows, merge=True)

    def _process_switch_item(item):
        r, pilot, hull, sys_id, poi_id, base_id, ship, ship_id = item
        try:
            if str(ship.get("docked") or "") != base_id:
                rem = min(210, max(45, budget_s - (time.time() - t0)))
                ok_d, msg_d = _gate_dock(gate_mod, pilot, sys_id, poi_id, base_id, timeout=rem, data_dir=data_dir, ship=ship)
                if not ok_d:
                    if "already executing" in msg_d.lower():
                        _request_pilot_stop(data_dir, pilot)
                    r["note"], r["updated_at"] = "ready; dock deferred: %s" % msg_d[:60], int(time.time())
                    with _save_lock:
                        save_queue(data_dir, [r], merge=True)
                    return
            ok_sw, sw_ans = _gate_raw(gate_mod, pilot, "switch_ship", {"ship_id": ship_id})
            if ok_sw:
                _gate_dock(gate_mod, pilot, sys_id, poi_id, base_id)
                r.pop("ready_to_switch", None)
                r["state"], r["updated_at"], r["note"] = "done", int(time.time()), "switched into %s @ %s" % (hull, base_id)
                if r.get("from_hangar_scan"):
                    rkey = str(r.get("reconcile_key") or ("%s:%s:%s" % (pilot, hull, base_id)))
                    rec_p = Path(data_dir) / "fleet" / "hangar_reconciled.json"
                    with _save_lock:
                        try:
                            prev_rk = json.loads(rec_p.read_text(encoding="utf-8")) if rec_p.is_file() else []
                            rk_list = sorted(set((prev_rk if isinstance(prev_rk, list) else []) + [rkey]))
                            rec_p.write_text(json.dumps(rk_list, indent=2) + "\n", encoding="utf-8")
                        except Exception:
                            pass
                print("UPGRADE switched %s: %s -> %s @ %s" % (r["id"], pilot, hull, base_id), flush=True)
            else:
                r["note"], r["updated_at"] = "switch failed: %s" % json.dumps(sw_ans)[:80], int(time.time())
            with _save_lock:
                save_queue(data_dir, [r], merge=True)
        finally:
            _release_upgrade(data_dir, pilot, division_mod)

    if switch_batch and not dry:
        n_sw = max(1, min(int(max_workers or 12), len(switch_batch)))
        if n_sw == 1:
            _process_switch_item(switch_batch[0])
        else:
            _sw_pool = _cf.ThreadPoolExecutor(max_workers=n_sw)
            _sw_futs = [_sw_pool.submit(_process_switch_item, it) for it in switch_batch]
            _sw_rem = max(45.0, budget_s - (time.time() - t0) + 15.0)
            _cf.wait(_sw_futs, timeout=_sw_rem)
            _sw_pool.shutdown(wait=False, cancel_futures=True)

    if funded_batch and not dry:
        n_w = max(1, min(int(max_workers or 6), len(funded_batch)))
        if n_w == 1:
            _process_funded_row(funded_batch[0])
        else:
            _pool = _cf.ThreadPoolExecutor(max_workers=n_w)
            _futs = [_pool.submit(_process_funded_row, _row) for _row in funded_batch]
            _rem = max(30.0, budget_s - (time.time() - t0) + 15.0)
            _cf.wait(_futs, timeout=_rem)
            _pool.shutdown(wait=False, cancel_futures=True)
    return 0




def _load_bursar_desk_pilots(data_dir):
    """Pilots currently staffing Bursar stations (exempt from hull CapEx & wealth tax)."""
    desks = set()
    bc = Path(data_dir) / "fleet" / "bursar_claims.json"
    if bc.is_file():
        try:
            d = json.loads(bc.read_text(encoding="utf-8", errors="replace"))
            for _b, rec in (d.items() if isinstance(d, dict) else []):
                if isinstance(rec, dict) and rec.get("pilot"):
                    desks.add(str(rec["pilot"]))
        except (OSError, ValueError):
            pass
    odir = Path(data_dir) / "fleet" / "orders"
    if odir.is_dir():
        for p in odir.glob("*.json"):
            try:
                od = json.loads(p.read_text(encoding="utf-8", errors="replace"))
                if str(od.get("what") or "").startswith("bursar "):
                    desks.add(str(od.get("pilot") or p.stem))
            except (OSError, ValueError):
                continue
    return desks



def _emp_rank(empire, prefer_empires):
    e = str(empire or "").lower()
    prefs = [str(x).lower() for x in (prefer_empires or [])]
    return prefs.index(e) if e in prefs else len(prefs) + 10


def _largest_remainder_quotas(total, shares):
    """Exact integer quotas summing to `total` (when sum(shares) <= 1.01), deterministic tie-break."""
    if total <= 0 or not shares:
        return [0] * len(shares)
    s_sum = sum(max(0.0, float(x)) for x in shares)
    if s_sum <= 0:
        return [0] * len(shares)
    if len(shares) == 1:
        return [max(1, min(total, int(round(total * float(shares[0])))))]
    norm = [max(0.0, float(x)) / (s_sum if s_sum > 1.01 else 1.0) for x in shares]
    exact = [total * f for f in norm]
    base = [int(v) for v in exact]
    rem = max(0, min(total, int(round(sum(exact)))) - sum(base))
    order = sorted(range(len(shares)), key=lambda i: (-(exact[i] - base[i]), -norm[i], i))
    for i in order[:rem]:
        base[i] += 1
    return base



EMPIRE_SHIPYARDS = {
    "solarian": "sol:sol_central:confederacy_central_command",
    "nebula": "factory_belt:factory_belt_manufacturing_hub:factory_belt_manufacturing_hub",
    "outerrim": "first_step:first_step_memorial_station:first_step_memorial_station",
    "crimson": "krynn:war_citadel:crimson_war_citadel",
    "voidborn": "nexus_prime:the_core:central_nexus",
}
DEFAULT_NEUTRAL_SHIPYARD = "sol:sol_central:confederacy_central_command"


def _load_manifest_wings(repo_root=REPO_DEFAULT):
    """Return {pilot_name: wing_string} from game/fleet-500-manifest.tsv."""
    p = Path(repo_root) / "game" / "fleet-500-manifest.tsv"
    if not p.is_file():
        return {}
    out = {}
    try:
        with p.open("r", encoding="utf-8", errors="replace") as fh:
            lines = [ln for ln in fh if ln.strip() and not ln.startswith("#")]
        import csv as _csv
        for r in _csv.DictReader(lines, delimiter="\t"):
            pil = str(r.get("pilot") or "").strip()
            if pil:
                out[pil] = str(r.get("wing") or "").strip()
    except OSError:
        return {}
    return out


def assign_cohort_pilots(div_ships, cohorts, wing_map=None):
    """Deterministically partition `div_ships` across `cohorts` preserving exact shares and locking existing hulls.

    Cohorts sharing identical filter masks (`empire`, `pilot_prefix`, `exclude_prefix`, `include_pilots`,
    `exclude_pilots`) form a mutually exclusive partition group so every pilot stays in ONE specialty lane
    across T0 -> T1 -> T2 -> T3 -> T4 -> T5. Existing specialty hulls are locked first, then `prefer_pilots`,
    then remaining quotas are filled by `assign_priority` and `prefer_empires` affinity.
    """
    assigned = {i: [] for i in range(len(cohorts))}
    groups = {}
    for idx, coh in enumerate(cohorts):
        if not (coh.get("ladder") or []):
            continue
        emp_f = str(coh.get("empire") or "any").lower()
        inc_pre = str(coh.get("pilot_prefix") or "")
        exc_pre = str(coh.get("exclude_prefix") or "")
        inc_t = tuple(sorted(str(x) for x in (coh.get("include_pilots") or [])))
        exc_t = tuple(sorted(str(x) for x in (coh.get("exclude_pilots") or [])))
        wp_f = str(coh.get("wing_prefix") or "")
        wc_f = str(coh.get("wing_contains") or "")
        sig = (emp_f, inc_pre, exc_pre, inc_t, exc_t, wp_f, wc_f)
        groups.setdefault(sig, []).append(idx)

    _wmap = wing_map or {}
    for sig, idxs in groups.items():
        emp_f, inc_pre, exc_pre, inc_t, exc_t, wp_f, wc_f = sig
        inc_set, exc_set = set(inc_t), set(exc_t)
        pool = [
            s for s in div_ships
            if (emp_f == "any" or s["empire"] == emp_f)
            and (not inc_pre or s["pilot"].startswith(inc_pre))
            and (not exc_pre or not s["pilot"].startswith(exc_pre))
            and (not inc_set or s["pilot"] in inc_set)
            and (not exc_set or s["pilot"] not in exc_set)
            and (not wp_f or _wmap.get(s["pilot"], "").startswith(wp_f))
            and (not wc_f or wc_f in _wmap.get(s["pilot"], ""))
        ]
        if not pool:
            continue
        if len(idxs) == 1:
            assigned[idxs[0]] = list(pool)
            continue

        quotas = _largest_remainder_quotas(len(pool), [float(cohorts[i].get("share") or 0.0) for i in idxs])
        qmap = {idxs[k]: quotas[k] for k in range(len(idxs))}

        # Map hulls that uniquely identify one specialty in this filter group
        hull_owners = {}
        for i in idxs:
            for rung in (cohorts[i].get("ladder") or []):
                h = str(rung.get("hull") or "").lower()
                if h:
                    hull_owners.setdefault(h, set()).add(i)
            for lh in (cohorts[i].get("legacy_hulls") or []):
                h = str(lh or "").lower()
                if h:
                    hull_owners.setdefault(h, set()).add(i)
        unique_hull_owner = {h: next(iter(owners)) for h, owners in hull_owners.items() if len(owners) == 1}

        taken = set()
        # Pass 1a: lock pilots already flying a unique specialty hull into that lane (never overwrite specialties!)
        for s in sorted(pool, key=lambda x: x["pilot"]):
            owner = unique_hull_owner.get(str(s.get("hull_id") or "").lower())
            if owner is not None:
                assigned[owner].append(s)
                taken.add(s["pilot"])

        # Pass 1b: lock explicit `prefer_pilots` into their cohort while under quota
        for i in idxs:
            pref_p = set(str(x) for x in (cohorts[i].get("prefer_pilots") or []))
            if not pref_p:
                continue
            for s in sorted(pool, key=lambda x: x["pilot"]):
                if s["pilot"] in taken or s["pilot"] not in pref_p:
                    continue
                if len(assigned[i]) < qmap[i]:
                    assigned[i].append(s)
                    taken.add(s["pilot"])

        # Pass 2: fill remaining quotas deterministically by assign_priority + birth-empire affinity
        fill_order = sorted(
            idxs,
            key=lambda i: (int(cohorts[i].get("assign_priority", 50)), qmap[i], i),
        )
        for i in fill_order:
            need = max(0, qmap[i] - len(assigned[i]))
            if need <= 0:
                continue
            prefs = cohorts[i].get("prefer_empires") or []
            rem = [s for s in pool if s["pilot"] not in taken]
            rem.sort(key=lambda s: (_emp_rank(s["empire"], prefs), s["pilot"]))
            for s in rem[:need]:
                assigned[i].append(s)
                taken.add(s["pilot"])

    return assigned


def auto_enqueue_upgrades(data_dir=DATA_DEFAULT, repo_root=REPO_DEFAULT, now=None, dry=False, policy_path=None):
    """Policy-driven multi-empire, multi-specialty auto-enqueuer with hard Treasury floor & CapEx cap.

    Reads `game/upgrade-policy.json` + live `read.db` (`faction`, `ships`, `hulls`, `ship_skills`,
    `ship_listings`, `places`, `systems`). Only enqueues when:
      1. `policy.enabled` is true and Treasury >= `treasury_floor_cr`.
      2. Rolling 24h auto-queued spend < `max_spend_24h_cr`.
      3. Division active queue < `max_active`, pilot is NOT already in active queue (`state`),
         pilot is NOT a T0 Bursar desk (when `exclude_bursar_desks`), and division `min_t0_bursar_reserve`
         is respected so Trade never starves the T0 Bursar desk pool.
      4. Target specialty cohort (filtered by empire / `pilot_prefix` / `exclude_prefix`) is under-represented
         and a listed hull <= `max_price` exists at a 3-part `system:poi:base` policed shipyard (when `listed_only`).
    Writes exact `queue_add()` row schema (`state="queued"`, 3-part `station`, `batch_id`, `provide_materials`, etc.).
    """
    now = float(now if now is not None else time.time())
    pol_p = Path(policy_path) if policy_path else (Path(repo_root) / "game" / "upgrade-policy.json")
    if not pol_p.is_file():
        return {"added": [], "skipped": "no policy file"}
    try:
        policy = json.loads(pol_p.read_text(encoding="utf-8", errors="replace"))
    except (OSError, ValueError):
        return {"added": [], "skipped": "invalid policy json"}
    if not isinstance(policy, dict) or not policy.get("enabled", False):
        return {"added": [], "skipped": "disabled"}

    con = _connect_ro(data_dir)
    if con is None:
        return {"added": [], "skipped": "no read.db"}
    try:
        tbls = {r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()}
        # 1. Treasury reserve floor check
        treasury = 0
        if "faction" in tbls:
            fr = con.execute("SELECT treasury FROM faction LIMIT 1").fetchone()
            if fr and fr[0] is not None:
                treasury = int(fr[0])
        floor_cr = int(policy.get("treasury_floor_cr") or 8500000)
        if treasury < floor_cr:
            return {"added": [], "skipped": "treasury %d < floor %d" % (treasury, floor_cr)}

        # 2. Rolling 24h auto-enqueue spend & active queue counts (match serve_upgrades `state` schema!)
        q_rows = load_queue(data_dir)
        active_states = set(ACTIVE_QUEUE_STATES) | {"queued", "funding", "funded", "building", "ready"}
        active_pilots = set()
        active_by_div = {}
        spend_24h = 0
        committed_unpaid = 0
        for r in q_rows:
            if not isinstance(r, dict):
                continue
            st = str(r.get("state") or "")
            if st in active_states:
                active_pilots.add(str(r.get("pilot") or ""))
                dv = str(r.get("division") or "")
                active_by_div[dv] = active_by_div.get(dv, 0) + 1
                if st in ("queued", "funding", "funded"):
                    committed_unpaid += int(r.get("max_price") or 0)
            elif st == "done" and (now - float(r.get("updated_at") or r.get("created_at") or 0)) <= 1800.0:
                # 30-minute cooldown after completion so read.db refreshes the new hull tier before re-evaluating
                active_pilots.add(str(r.get("pilot") or ""))
            if str(r.get("source") or "") == "auto_policy" and st not in ("", "cancelled", "failed"):
                at_t = float(r.get("created_at") or 0)
                if (now - at_t) <= 86400.0:
                    spend_24h += int(r.get("max_price") or 0)
        raw_cap = policy.get("max_spend_24h_cr")
        cap_24h = int(raw_cap) if raw_cap is not None else 0
        if cap_24h > 0 and spend_24h >= cap_24h:
            return {"added": [], "skipped": "24h capex %d >= %d" % (spend_24h, cap_24h)}
        treasury = max(0, treasury - committed_unpaid)
        if treasury < floor_cr:
            return {"added": [], "skipped": "avail_treasury %d (after %d committed) < floor %d" % (treasury, committed_unpaid, floor_cr)}

        # 3. Live safe ship_listings mapped to 3-part `system:poi:base` stations
        listed_only = bool(policy.get("listed_only", True))
        policed_only = bool(policy.get("policed_listings_only", True))
        max_age_s = float(policy.get("min_listing_age_fresh_h") or 6.0) * 3600.0
        policed_bases = set()
        base_to_station = {}
        if "places" in tbls and "systems" in tbls:
            for b_id, sys_id, poi_id, emp, sh in con.execute("""
                SELECT p.base, p.system, p.poi, COALESCE(s.empire, ''), COALESCE(s.stronghold, 0)
                FROM places p LEFT JOIN systems s ON s.id = p.system
                WHERE p.base IS NOT NULL AND p.base != ''
                  AND p.system IS NOT NULL AND p.system != ''
                  AND p.poi IS NOT NULL AND p.poi != ''
            """).fetchall():
                b_str = str(b_id)
                base_to_station[b_str] = "%s:%s:%s" % (str(sys_id), str(poi_id), b_str)
                if emp and not int(sh or 0):
                    policed_bases.add(b_str)
        listings_by_hull = {}
        if "ship_listings" in tbls:
            for cid, b_id, price, ts in con.execute(
                "SELECT class_id, base, price, t FROM ship_listings WHERE price > 0 ORDER BY price ASC"
            ).fetchall():
                b_str = str(b_id)
                if ts and (now - float(ts)) > max_age_s:
                    continue
                if policed_only and policed_bases and b_str not in policed_bases:
                    continue
                st_3 = base_to_station.get(b_str)
                if not st_3:
                    continue
                listings_by_hull.setdefault(str(cid).lower(), []).append((int(price), st_3))

        # 4. Live ships + hulls + piloting skills
        hull_factions = {}
        if "hulls" in tbls:
            _hcols = {r[1] for r in con.execute("PRAGMA table_info(hulls)").fetchall()}
            if "faction" in _hcols:
                for h_id, h_fac in con.execute("SELECT LOWER(id), LOWER(COALESCE(faction, '')) FROM hulls").fetchall():
                    hull_factions[str(h_id)] = str(h_fac or "")
        ships = []
        if "ships" in tbls and "hulls" in tbls:
            pil_map = {}
            if "ship_skills" in tbls:
                for p_nm, lvl in con.execute("SELECT pilot, level FROM ship_skills WHERE skill = 'piloting'").fetchall():
                    pil_map[str(p_nm)] = int(lvl or 0)
            for p_nm, dv, emp, cls, tr, hid in con.execute("""
                SELECT s.pilot, s.division, LOWER(COALESCE(s.empire, '')), s.class,
                       COALESCE(h.tier, 0), COALESCE(h.id, LOWER(COALESCE(s.class, '')))
                FROM ships s LEFT JOIN hulls h ON (h.id = s.class OR h.name = s.class)
            """).fetchall():
                ships.append({
                    "pilot": str(p_nm), "division": str(dv or ""), "empire": str(emp or ""),
                    "class": str(cls or ""), "tier": int(tr or 0), "hull_id": str(hid or "").lower(),
                    "piloting": pil_map.get(str(p_nm), 0),
                })
    finally:
        con.close()

    bursar_desks = _load_bursar_desk_pilots(data_dir) if policy.get("exclude_bursar_desks", True) else set()
    import fuelplan as _fp_enq
    _lanes_enq, _ = _fp_enq.chart(Path(repo_root) / "game")
    _fars_enq = _fp_enq.strongholds(Path(repo_root) / "game")
    _sts_enq = {s: v for s, v in _fp_enq.fuel_stations(data_dir).items() if s not in _fars_enq}
    _ships_dir_enq = Path(data_dir) / "fleet" / "ships"
    _ship_cache_enq = {}

    def _pilot_can_reach(pilot_name, target_st3):
        if not _lanes_enq or not _sts_enq or not target_st3 or ":" not in str(target_st3):
            return True
        t_sys = str(target_st3).split(":", 1)[0]
        if pilot_name not in _ship_cache_enq:
            try:
                _ship_cache_enq[pilot_name] = json.loads((_ships_dir_enq / (pilot_name + ".json")).read_text(encoding="utf-8"))
            except (OSError, ValueError):
                _ship_cache_enq[pilot_name] = None
        sdoc = _ship_cache_enq[pilot_name]
        if not isinstance(sdoc, dict) or not sdoc.get("system"):
            return True
        return _fp_enq.can_reach_with_refuels(_lanes_enq, str(sdoc["system"]), t_sys, _sts_enq, ship=sdoc, avoid=_fars_enq)
    max_new = max(1, int(policy.get("max_new_per_pass") or 4))
    default_div_cap = int(policy.get("max_active_per_div") or 6)
    max_auto_tier = int(policy.get("max_auto_tier") or 3)
    div_cfgs = policy.get("divisions") or {}
    added = []
    used_listings = set()
    _rr_round = 0
    while _rr_round < 500:
      _rr_round += 1
      _added_before_round = len(added)
      for div_name, dcfg in div_cfgs.items():
          if len(added) >= max_new or (cap_24h > 0 and spend_24h >= cap_24h):
              break
          if not isinstance(dcfg, dict) or not dcfg.get("enabled", False):
              continue
          div_cap = int(dcfg.get("max_active") or default_div_cap)
          if active_by_div.get(div_name, 0) >= div_cap:
              continue
          div_ships = [s for s in ships if s["division"] == div_name]
          if not div_ships:
              continue

          min_t0_reserve = int(dcfg.get("min_t0_bursar_reserve") or 0)
          t0_free_count = sum(1 for s in div_ships if s["tier"] == 0 and s["pilot"] not in active_pilots)

          # Deterministically partition pilots into their permanent specialty lanes & score T0->T5 upgrade need
          cohorts = list(dcfg.get("cohorts") or [])
          _manifest_wings = _load_manifest_wings(repo_root)
          assigned_map = assign_cohort_pilots(div_ships, cohorts, wing_map=_manifest_wings)
          ranked_cohorts = []
          for idx, coh in enumerate(cohorts):
              if coh.get("enabled") is False:
                  continue
              ladder = list(coh.get("ladder") or [])
              cohort_ships = assigned_map.get(idx) or []
              if not ladder or not cohort_ships:
                  continue
              rungs_allowed = [r for r in ladder if 1 <= int(r.get("tier") or 1) <= max_auto_tier]
              if not rungs_allowed:
                  continue
              _allow_bd = bool(coh.get("allow_bursar_desks", False))
              t0_need = sum(
                  1 for s in cohort_ships
                  if s["tier"] == 0 and s["pilot"] not in active_pilots and (_allow_bd or s["pilot"] not in bursar_desks)
              )
              upg_need = sum(
                  1 for s in cohort_ships
                  if s["pilot"] not in active_pilots and (_allow_bd or s["pilot"] not in bursar_desks)
                  and any(int(r.get("tier") or 1) > s["tier"] and s["piloting"] >= int(r.get("min_piloting") or 0) for r in rungs_allowed)
              )
              if upg_need <= 0:
                  continue
              t0_frac = float(t0_need) / float(max(1, len(cohort_ships)))
              _kpi_boost = 0.0
              try:
                  import kpi_engine as _ke_u
                  _ksig = _ke_u.read_kpi_signals(data_dir)
                  _pw = _ksig.get("priority_upgrade_wings") or []
                  _cw = _ke_u.wing_id_of(str(coh.get("wing_prefix") or ""), div_name)
                  if _cw in _pw[:5]:
                      _kpi_boost = 0.25 - 0.03 * _pw.index(_cw)
                  elif _cw in (_ksig.get("tighten_fuel_wings") or []):
                      _kpi_boost = 0.20
              except Exception:
                  pass
              ranked_cohorts.append((t0_frac + _kpi_boost, upg_need, -idx, coh, cohort_ships))
          ranked_cohorts.sort(reverse=True)

          for _t0_frac, _upg_need, _neg_i, coh, cohort_ships in ranked_cohorts:
              if len(added) >= max_new or (cap_24h > 0 and spend_24h >= cap_24h) or active_by_div.get(div_name, 0) >= div_cap:
                  break
              # Group ladder rungs by tier descending (T5 -> T1 <= max_auto_tier); pick cheapest live bargain per tier
              rungs_by_tier = {}
              for r_idx, rung in enumerate(coh.get("ladder") or []):
                  rtier = int(rung.get("tier") or 1)
                  if 1 <= rtier <= max_auto_tier:
                      rungs_by_tier.setdefault(rtier, []).append((r_idx, rung))
              pref_set = set(str(x) for x in (coh.get("prefer_pilots") or []))
              pref_emps = coh.get("prefer_empires") or []
              emp_first = bool(coh.get("empire_first_pick", False))
              picked = None
              for rtier in sorted(rungs_by_tier.keys(), reverse=True):
                  tier_cands = []
                  for r_idx, rung in rungs_by_tier[rtier]:
                      hid = str(rung.get("hull") or "").lower()
                      rpil = int(rung.get("min_piloting") or 0)
                      rmax = int(rung.get("max_price") or 0)
                      if not hid or rmax <= 0 or (cap_24h > 0 and (spend_24h + rmax) > cap_24h) or (treasury - rmax) < floor_cr:
                          continue
                      l_station = None
                      l_price = rmax
                      base_elig = [
                          s for s in cohort_ships
                          if s["pilot"] not in active_pilots
                          and (bool(coh.get("allow_bursar_desks", False)) or s["pilot"] not in bursar_desks)
                          and s["tier"] < rtier
                          and s["piloting"] >= rpil
                          and not (min_t0_reserve > 0 and s["tier"] == 0 and t0_free_count <= min_t0_reserve)
                      ]
                      if not base_elig:
                          continue
                      elig = []
                      cand_l = [
                          (pr, st3) for pr, st3 in (listings_by_hull.get(hid) or [])
                          if pr <= rmax and (hid, st3, pr) not in used_listings
                      ]
                      for pr, st3 in cand_l:
                          reach_elig = [s for s in base_elig if _pilot_can_reach(s["pilot"], st3)]
                          if reach_elig:
                              l_price, l_station, elig = pr, st3, reach_elig
                              break
                      if not elig:
                          if listed_only:
                              continue
                          h_fac = hull_factions.get(hid, "")
                          l_station = EMPIRE_SHIPYARDS.get(h_fac) or DEFAULT_NEUTRAL_SHIPYARD
                          if not l_station:
                              continue
                          elig = [s for s in base_elig if _pilot_can_reach(s["pilot"], l_station)]
                          if not elig:
                              continue
                          l_price = rmax
                      if emp_first:
                          elig.sort(key=lambda s: (0 if s["pilot"] in pref_set else 1, _emp_rank(s["empire"], pref_emps), -s["piloting"], s["tier"], s["pilot"]))
                      else:
                          elig.sort(key=lambda s: (0 if s["pilot"] in pref_set else 1, -s["piloting"], _emp_rank(s["empire"], pref_emps), s["tier"], s["pilot"]))
                      _eff_mp = rmax if not listed_only else min(rmax, int(l_price * 1.02) + 500)
                      tier_cands.append((l_price, r_idx, elig[0], hid, l_station, _eff_mp))
                  if tier_cands:
                      tier_cands.sort(key=lambda x: (x[1], x[0]))
                      lp_best, _ri, ps_best, hid_best, st_best, mp_best = tier_cands[0]
                      picked = (ps_best, hid_best, st_best, mp_best, lp_best, str(coh.get("specialty") or ""))
                      break

              if not picked:
                  continue
              pship, hid, st_3, mp, lp, spec = picked
              if dry:
                  added.append({"pilot": pship["pilot"], "division": div_name, "hull": hid, "station": st_3, "price": lp, "specialty": spec, "dry": True})
                  active_pilots.add(pship["pilot"])
                  active_by_div[div_name] = active_by_div.get(div_name, 0) + 1
                  if pship["tier"] == 0:
                      t0_free_count = max(0, t0_free_count - 1)
                  spend_24h += mp
                  treasury -= mp
                  used_listings.add((hid, st_3, lp))
                  continue
              # Enqueue via atomic locked append matching exact queue_add() schema
              with _queue_lock(data_dir):
                  rows = load_queue(data_dir)
                  if any(str(x.get("pilot") or "") == pship["pilot"] and str(x.get("state") or "") in active_states for x in rows if isinstance(x, dict)):
                      continue
                  next_num = max(
                      (int(str(x.get("id") or "0").split("-")[-1]) for x in rows if isinstance(x, dict) and str(x.get("id") or "").split("-")[-1].isdigit()),
                      default=0,
                  ) + 1
                  next_id = "u-%d" % next_num
                  batch_id = "upg-auto-%s-%d" % (re.sub(r"[^a-z0-9]+", "-", hid)[:12], int(now))
                  rows.append({
                      "id": next_id,
                      "batch_id": batch_id,
                      "pilot": pship["pilot"],
                      "division": div_name,
                      "by": "AutoUpgrade",
                      "source": "auto_policy",
                      "specialty": spec,
                      "hull": hid,
                      "station": st_3,
                      "max_price": int(mp),
                      "provide_materials": False,
                      "state": "queued",
                      "created_at": int(now),
                      "updated_at": int(now),
                      "last_poll": 0,
                      "paid": 0,
                      "note": "auto_policy:%s" % spec,
                  })
                  save_queue(data_dir, rows, merge=True)
              added.append({"pilot": pship["pilot"], "division": div_name, "hull": hid, "station": st_3, "price": lp, "specialty": spec})
              active_pilots.add(pship["pilot"])
              active_by_div[div_name] = active_by_div.get(div_name, 0) + 1
              if pship["tier"] == 0:
                  t0_free_count = max(0, t0_free_count - 1)
              spend_24h += mp
              treasury -= mp
              used_listings.add((hid, st_3, lp))
      if len(added) == _added_before_round or len(added) >= max_new or treasury < floor_cr:
        break
    return {"added": added, "spend_24h": spend_24h, "treasury": treasury}

def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    data_default = os.environ.get("COLLECTIVE_DATA", DATA_DEFAULT)
    if argv and argv[0] == "queue":
        if len(argv) > 1 and not argv[1].startswith("-"):
            sub, rest = argv[1], argv[2:]
        else:
            sub, rest = "show", argv[1:]
        ap = argparse.ArgumentParser(prog="upgrades.py queue " + sub)
        ap.add_argument("--data", default=data_default)
        ap.add_argument("--who", default="")
        if sub == "add":
            ap.add_argument("--hull", required=True)
            ap.add_argument("--station", required=True, help="system:poi:base")
            ap.add_argument("--max-price", type=int, required=True)
            ap.add_argument("--count", type=int, default=5)
            ap.add_argument("--role", default="")
            ap.add_argument("--empire", default="")
            ap.add_argument("--min-piloting", type=int, default=0)
            ap.add_argument("--pilots", default="")
            ap.add_argument("--provide-materials", action="store_true")
            a = ap.parse_args(rest)
            here = str(Path(__file__).resolve().parent)
            if here not in sys.path:
                sys.path.insert(0, here)
            import division as _div
            _k, me = _div.member()
            caller = a.who or (me if me in _div.MEMBERS else "Unity")
            rc, lines = queue_add(a.data, caller, a.hull, a.station, a.max_price, count=a.count,
                                  role=a.role or None, empire=a.empire or None, min_piloting=a.min_piloting,
                                  pilots=a.pilots or None, provide_materials=a.provide_materials)
            for l in lines:
                print(l)
            return rc
        if sub == "cancel":
            ap.add_argument("target")
            a = ap.parse_args(rest)
            here = str(Path(__file__).resolve().parent)
            if here not in sys.path:
                sys.path.insert(0, here)
            import division as _div
            _k, me = _div.member()
            caller = a.who or (me if me in _div.MEMBERS else "Unity")
            rc, lines = queue_cancel(a.data, caller, a.target)
            for l in lines:
                print(l)
            return rc
        a = ap.parse_args(rest)
        txt = format_queue(a.data, who=a.who or "all")
        print(txt or "UPGRADE QUEUE | empty (use `upgrades.py queue add --hull <id> --station <sys:poi:base> --max-price <cr> --count <N>`)")
        return 0
    if argv and argv[0] == "serve":
        ap = argparse.ArgumentParser(prog="upgrades.py serve")
        ap.add_argument("--data", default=data_default)
        ap.add_argument("--dry-run", action="store_true")
        ap.add_argument("--max-actions", type=int, default=15)
        a = ap.parse_args(argv[1:])
        return serve_upgrades(a.data, dry=a.dry_run, max_actions=a.max_actions)
    ap = argparse.ArgumentParser(description="Empire-specialized hull & module parallel upgrade planner.")
    ap.add_argument("who", nargs="?", default="all", help="Member or division name (default: all)")
    ap.add_argument("--data", default=data_default)
    ap.add_argument("--root", default=REPO_DEFAULT)
    args = ap.parse_args(argv)
    print(render_upgrades(repo_root=args.root, data_dir=args.data, who=args.who))
    return 0


if __name__ == "__main__":
    sys.exit(main())

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
    "Mining": ("mining_laser_iii", "mining_laser_ii", "ice_harvester_ii", "gas_harvester_ii", "cargo_expander_ii", "cargo_expander_i"),
    "Military": ("pulse_laser_iii", "pulse_laser_ii", "shield_booster_ii", "armor_plate_ii", "shield_recharger_ii"),
    "Trade": ("cargo_expander_ii", "cargo_expander_i", "shield_booster_ii"),
    "Logistics": ("cargo_expander_ii", "cargo_expander_i", "shield_booster_ii"),
    "Intel": ("survey_scanner_ii", "survey_scanner_i", "shield_booster_ii"),
    "Command": ("pulse_laser_iii", "shield_booster_ii", "armor_plate_ii", "cargo_expander_ii"),
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
                        f"  Top T2/T3 Exchange Mods (prefer T2/T3 over Tier-1 swaps): {', '.join(hints[:4])}"
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
        q_txt = format_queue(data_dir, who=who)
        if q_txt:
            lines.append("")
            lines.append(q_txt)
        return "\n".join(lines)
    finally:
        conn.close()




# ---- Autonomous Batch Hull-Upgrade Queue (F12 / F17 / F37) ----

UPGRADE_FLOOR = 20000          # minimum wallet kept after commissioning a hull
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


def save_queue(data_dir, rows):
    p = queue_file(data_dir)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_name(p.name + ".tmp")
    tmp.write_text(json.dumps(rows, indent=1) + "\n", encoding="ascii")
    os.replace(tmp, p)


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
    save_queue(data_dir, rows)
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
    save_queue(data_dir, rows)
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


def _gate_raw(gate_mod, pilot, action, params=None, group="spacemolt_ship"):
    status, out = gate_mod.call("post", "/accounts/%s/raw" % gate_mod.q(pilot),
                                {"toolGroup": group, "action": action, "params": params or {}}, timeout=90)
    try:
        data = json.loads(out)
    except (ValueError, TypeError):
        data = {"raw": str(out)[:300]}
    return status == 200 and '"error"' not in str(out)[:240], data


def _gate_dock(gate_mod, pilot, sys_id, poi_id, base_id, timeout=65):
    status, out = gate_mod.call("post", "/accounts/%s/goal" % gate_mod.q(pilot),
                                {"type": "prepare-at-station", "options": {"systemId": sys_id, "poiId": poi_id, "baseId": base_id, "refuel": True}},
                                timeout=max(20, int(timeout)))
    try:
        d = json.loads(out)
    except (ValueError, TypeError):
        return False, str(out)[:160]
    return status == 200 and bool(d.get("success")), str(d.get("message") or d.get("error") or "")[:160]


def _try_hold_upgrade(data_dir, pilot, now, division_mod):
    if division_mod.order_of(pilot, data_dir):
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


def serve_upgrades(data_dir=DATA_DEFAULT, now=None, dry=False, max_actions=15, budget_s=70.0,
                   gate_mod=None, wallet_mod=None, division_mod=None):
    """Advance queued hull upgrades safely (runs every 5 min inside wallet.py sweep). Bounded, non-blocking."""
    now = float(time.time() if now is None else now)
    if (Path(data_dir) / "fleet" / "STOP").exists():
        return 0
    rows = load_queue(data_dir)
    active = [r for r in rows if isinstance(r, dict) and r.get("state") in ACTIVE_QUEUE_STATES]
    if not active:
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

    pmap = _pilot_division_map(data_dir)
    changed, actions, t0 = False, 0, time.time()

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
            if credits >= need_cr:
                r["state"], r["updated_at"], r["note"] = "funded", int(now), "funds arrived"
                changed = True
            elif now - float(r.get("created_at") or now) > UPGRADE_FUND_TIMEOUT:
                r["state"], r["updated_at"], r["note"] = "failed", int(now), "funding timeout (48h)"
                changed = True
    if changed and not dry:
        save_queue(data_dir, rows)
        changed = False

    # Phase 2: prioritize pilots already docked at target shipyard, then same system, then travelling
    def _dock_prio(row):
        parts = str(row.get("station") or "").split(":")
        if len(parts) != 3:
            return (9, str(row.get("id") or ""))
        info = pmap.get(str(row.get("pilot") or ""))
        sh = info[2] if info else {}
        if str(sh.get("docked") or "") == parts[2]:
            return (0, str(row.get("id") or ""))
        if str(sh.get("system") or "") == parts[0]:
            return (1, str(row.get("id") or ""))
        return (2, str(row.get("id") or ""))

    for r in sorted(active, key=_dock_prio):
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
            if not _try_hold_upgrade(data_dir, pilot, now, division_mod):
                _request_pilot_stop(data_dir, pilot)
                r["note"], r["updated_at"] = "waiting for active run to end (stop sent)", int(now)
                if not dry:
                    save_queue(data_dir, rows)
                continue
            actions += 1
            try:
                if str(ship.get("docked") or "") != base_id:
                    ok_d, msg_d = _gate_dock(gate_mod, pilot, sys_id, poi_id, base_id, timeout=min(65, max(20, budget_s - (time.time() - t0))))
                    if not ok_d:
                        if "already executing" in msg_d.lower():
                            _request_pilot_stop(data_dir, pilot)
                        r["note"], r["updated_at"] = "dock deferred: %s" % msg_d[:80], int(now)
                        changed = True
                        continue
                ok_ls, ls_ans = _gate_raw(gate_mod, pilot, "list_ships", {})
                stored = [s for s in _extract_ships(ls_ans) if str(s.get("class_id") or "").lower() == hull
                          and not s.get("is_active") and s.get("location_base_id") == base_id] if ok_ls else []
                if stored:
                    ok_sw, _ = _gate_raw(gate_mod, pilot, "switch_ship", {"ship_id": stored[0]["ship_id"]})
                    if ok_sw:
                        r["state"], r["updated_at"], r["note"] = "done", int(now), "switched into stored %s" % hull
                        changed = True
                        continue
                ok_q, q_ans = _gate_raw(gate_mod, pilot, "commission_quote", {"ship_class": hull})
                price = _extract_quote_price(q_ans) if ok_q else 0
                if not price:
                    r["note"], r["updated_at"] = "quote unreadable", int(now)
                    changed = True
                    continue
                if price > int(r["max_price"]):
                    r["state"], r["updated_at"], r["note"] = "failed", int(now), "quote %s > max %s" % (_fmt_num(price), _fmt_num(r["max_price"]))
                    changed = True
                    continue
                if credits - price < UPGRADE_FLOOR:
                    r["state"], r["updated_at"], r["note"] = "queued", int(now), "need more credits for quote %s" % _fmt_num(price)
                    changed = True
                    continue
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
                    changed = True
                    print("UPGRADE commissioned %s: %s -> %s (%s cr)" % (r["id"], pilot, hull, _fmt_num(price)))
                else:
                    r["note"], r["updated_at"] = "commission failed: %s" % json.dumps(c_ans)[:90], int(now)
                    changed = True
            finally:
                _release_upgrade(data_dir, pilot, division_mod)
                if changed and not dry:
                    save_queue(data_dir, rows)
                    changed = False

        elif state == "building":
            if now - float(r.get("last_poll") or 0) < UPGRADE_POLL_S:
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
                continue
            r["ready_to_switch"] = True
            if not _try_hold_upgrade(data_dir, pilot, now, division_mod):
                _request_pilot_stop(data_dir, pilot)
                r["note"] = "ready at %s; waiting for pilot free (stop sent)" % base_id
                continue
            actions += 1
            try:
                if str(ship.get("docked") or "") != base_id:
                    ok_d, msg_d = _gate_dock(gate_mod, pilot, sys_id, poi_id, base_id, timeout=min(65, max(20, budget_s - (time.time() - t0))))
                    if not ok_d:
                        if "already executing" in msg_d.lower():
                            _request_pilot_stop(data_dir, pilot)
                        r["note"] = "ready; dock deferred: %s" % msg_d[:60]
                        continue
                ok_sw, sw_ans = _gate_raw(gate_mod, pilot, "switch_ship", {"ship_id": stored[0]["ship_id"]})
                if ok_sw:
                    _gate_dock(gate_mod, pilot, sys_id, poi_id, base_id)
                    r.pop("ready_to_switch", None)
                    r["state"], r["updated_at"], r["note"] = "done", int(now), "switched into %s @ %s" % (hull, base_id)
                    print("UPGRADE switched %s: %s -> %s @ %s" % (r["id"], pilot, hull, base_id))
                else:
                    r["note"] = "switch failed: %s" % json.dumps(sw_ans)[:80]
            finally:
                _release_upgrade(data_dir, pilot, division_mod)
                if changed and not dry:
                    save_queue(data_dir, rows)
                    changed = False

    if changed and not dry:
        save_queue(data_dir, rows)
    return 0


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

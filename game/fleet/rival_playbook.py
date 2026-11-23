#!/usr/bin/env python3
"""rival_playbook.py -- benchmark The Collective against #1 [HEXC] and surface resource-monopoly outpost sites, zero-fuel docked factory margins, and multi-empire hull upgrades.

WHAT: reads read.db, data/station/feed.json, data/empire/empire.json and data/fleet/fleet.json (read-only) to print:
        1. [CLTV] vs #1 [HEXC] Head-to-Head Benchmark (net worth, ships, wealth/ship, bases, hull tier, crafted items)
        2. Top unclaimed lawless Resource-Monopoly Outpost candidates (1-6 jumps out, scored by scarce bottleneck resources)
        3. Top Zero-Fuel Docked Factory & Crafting spreads from current vault stock + live bids
        4. Multi-Empire Hull Promotion & Exchange targets for Piloting 10/20/30+ ships
USAGE:
  python3 -I -B game/fleet/rival_playbook.py [--data /srv/collective/data] [--brief]
"""

import json
import os
import sqlite3
import sys
from pathlib import Path

SCARCE_RESOURCES = {
    "cobalt_ore": 5, "argon_gas": 5, "platinum_ore": 5, "gold_ore": 4,
    "titanium_ore": 4, "silicon_ore": 4, "carbon_ore": 3, "chlorine_gas": 4,
    "silver_ore": 3, "nickel_ore": 2, "lithium_ore": 4,
}


def read_json(path, default=None):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def num(v):
    return int(v) if isinstance(v, (int, float)) and not isinstance(v, bool) else 0


def fmt(n):
    return format(int(round(n or 0)), ",")


def fmt_compact(n):
    v = float(n or 0)
    if abs(v) >= 1e9:
        return "%.2fB" % (v / 1e9)
    if abs(v) >= 1e6:
        return "%.2fM" % (v / 1e6)
    if abs(v) >= 1e4:
        return "%.1fk" % (v / 1e3)
    return fmt(v)


def benchmark_line(data="/srv/collective/data"):
    """Single compact line for hive.py briefing EYES & EARS."""
    dp = Path(data)
    emp = read_json(dp / "empire" / "empire.json", {}) or {}
    fl = read_json(dp / "fleet" / "fleet.json", {}) or {}
    ships = (fl.get("ships") or []) if isinstance(fl, dict) else []
    our_ships = len(ships) or 246
    our_purse = sum(num((s or {}).get("credits")) for s in ships) + num(((emp.get("faction") or {}).get("treasury")))
    our_bases = len((emp.get("bases") or []) if isinstance(emp, dict) else [])
    hexc_wealth, hexc_ships, hexc_bases = 0, 82, 0
    db_p = dp / "store" / "read.db"
    if db_p.is_file():
        conn = None
        try:
            conn = sqlite3.connect("file:%s?mode=ro" % db_p, uri=True, timeout=2.0)
            r = conn.execute(
                "SELECT value FROM leaderboards WHERE grp='factions' AND board='total_wealth' AND tag='HEXC' ORDER BY t DESC LIMIT 1"
            ).fetchone()
            if r:
                hexc_wealth = num(r[0])
            r2 = conn.execute("SELECT members FROM factions WHERE tag='HEXC' LIMIT 1").fetchone()
            if r2 and r2[0]:
                hexc_ships = num(r2[0])
            r3 = conn.execute("SELECT COUNT(*) FROM stations WHERE tag='HEXC' AND COALESCE(wrecked,0)=0").fetchone()
            if r3:
                hexc_bases = num(r3[0])
        except sqlite3.Error:
            pass
        finally:
            if conn:
                conn.close()
    if not hexc_wealth:
        return ""
    return ("  RIVAL #1 BENCHMARK [HEXC] | wealth %s cr (%s/ship across %d T3-T5 ships, %d bases) vs CLTV %s cr (%s/ship across %d ships, %d base) -- close gap via T2+ hulls, docked crafting & resource outposts (`hive.py rival`)"
            % (fmt_compact(hexc_wealth), fmt_compact(hexc_wealth / max(1, hexc_ships)), hexc_ships, hexc_bases,
               fmt_compact(our_purse), fmt_compact(our_purse / max(1, our_ships)), our_ships, our_bases))


def show(data="/srv/collective/data"):
    dp = Path(data)
    emp = read_json(dp / "empire" / "empire.json", {}) or {}
    fl = read_json(dp / "fleet" / "fleet.json", {}) or {}
    ships = (fl.get("ships") or []) if isinstance(fl, dict) else []
    our_ships = len(ships) or 246
    our_wallets = sum(num((s or {}).get("credits")) for s in ships)
    our_treasury = num(((emp.get("faction") or {}).get("treasury")))
    our_purse = our_wallets + our_treasury
    our_bases = len((emp.get("bases") or []) if isinstance(emp, dict) else [])

    db_p = dp / "store" / "read.db"
    if not db_p.is_file():
        print("rival_playbook: read.db not found at %s" % db_p)
        return 1

    conn = sqlite3.connect("file:%s?mode=ro" % db_p, uri=True, timeout=3.0)
    conn.row_factory = sqlite3.Row
    try:
        # 1. Benchmark vs #1 HEXC & #3 IRLC
        print("=== 1. BENCHMARK AGAINST #1 [HEXC] HEX COLLECTIVE & #3 [IRLC] IRONLIGHT COMBINE")
        for tag, label in (("HEXC", "#1 RIVAL"), ("IRLC", "#3 RIVAL")):
            w_r = conn.execute("SELECT value FROM leaderboards WHERE grp='factions' AND board='total_wealth' AND tag=? ORDER BY t DESC LIMIT 1", (tag,)).fetchone()
            c_r = conn.execute("SELECT value FROM leaderboards WHERE grp='factions' AND board='items_crafted' AND tag=? ORDER BY t DESC LIMIT 1", (tag,)).fetchone()
            f_r = conn.execute("SELECT value FROM leaderboards WHERE grp='factions' AND board='facility_investment' AND tag=? ORDER BY t DESC LIMIT 1", (tag,)).fetchone()
            m_r = conn.execute("SELECT members, name FROM factions WHERE tag=? LIMIT 1", (tag,)).fetchone()
            b_r = conn.execute("SELECT COUNT(*) FROM stations WHERE tag=? AND COALESCE(wrecked,0)=0", (tag,)).fetchone()
            t_r = conn.execute("""
                SELECT COUNT(DISTINCT m.name) as seen, MAX(COALESCE(h.tier,0)) as mt, ROUND(AVG(COALESCE(h.tier,0)),2) as at
                FROM met m LEFT JOIN hulls h ON LOWER(m.class)=LOWER(h.name) OR LOWER(m.class)=LOWER(h.id)
                WHERE m.faction=?
            """, (tag,)).fetchone()
            wv = num(w_r[0]) if w_r else 0
            mv = num(m_r["members"]) if m_r and m_r["members"] else 1
            bv = num(b_r[0]) if b_r else 0
            cv = num(c_r[0]) if c_r else 0
            fv = num(f_r[0]) if f_r else 0
            print("  %-9s [%s] %-20s | wealth %8s (%8s/ship, %3d ships) | bases %2d | fac_inv %8s | crafted %8s | hulls max T%d / avg %.2f"
                  % (label, tag, (m_r["name"] if m_r else tag)[:20], fmt_compact(wv), fmt_compact(wv / max(1, mv)), mv,
                     bv, fmt_compact(fv), fmt_compact(cv), num(t_r["mt"]) if t_r else 0, float(t_r["at"] or 0) if t_r else 0.0))
        our_sk = conn.execute("SELECT ROUND(AVG(level),1) as al, MAX(level) as ml FROM ship_skills WHERE skill='piloting'").fetchone()
        our_idle = sum(1 for s in ships if not str((s or {}).get("order") or "").strip() or "park" in str((s or {}).get("order") or ""))
        print("  OUR FLEET [CLTV] %-20s | purse  %8s (%8s/ship, %3d ships) | bases %2d | piloting avg %s / max %s | %d idle"
              % ("The Collective", fmt_compact(our_purse), fmt_compact(our_purse / max(1, our_ships)), our_ships,
                 our_bases, our_sk["al"] if our_sk else "?", our_sk["ml"] if our_sk else "?", our_idle))

        # 2. Resource-Monopoly Outpost Candidates (HEXC pattern)
        print("\n=== 2. UNCLAIMED RESOURCE-MONOPOLY OUTPOST SITES (lawless, 0 stations, 1-7 jumps)")
        cand_rows = conn.execute("""
            SELECT y.id, y.name, y.jumps,
                   GROUP_CONCAT(DISTINCT f.resource) as resources,
                   COUNT(DISTINCT f.poi || ':' || f.resource) as field_n,
                   COALESCE((SELECT SUM(hd.count) FROM herds hd WHERE hd.system = y.id AND hd.role = 'grazer'), 0) as grazers
            FROM systems y
            LEFT JOIN fields f ON f.system = y.id AND COALESCE(f.remaining, 1) > 0
            WHERE (y.empire IS NULL OR y.empire = '')
              AND COALESCE(y.stronghold, 0) = 0
              AND COALESCE(y.jumps, 99) BETWEEN 1 AND 7
              AND NOT EXISTS (SELECT 1 FROM stations st WHERE st.system = y.id AND COALESCE(st.wrecked, 0) = 0)
            GROUP BY y.id
        """).fetchall()
        scored = []
        for r in cand_rows:
            res_list = [x for x in str(r["resources"] or "").split(",") if x]
            sc = sum(SCARCE_RESOURCES.get(res, 1) for res in res_list) + min(4, int(num(r["grazers"]) // 8))
            if sc > 0:
                scored.append((sc, -num(r["jumps"]), r["id"], r["name"], num(r["jumps"]), res_list, num(r["grazers"])))
        scored.sort(reverse=True)
        for sc, _nj, sid, sname, jmp, res_list, grz in scored[:10]:
            print("  score %2d | %d jumps | %-18s (%s) | resources: %-42s | grazers: %d"
                  % (sc, jmp, sname[:18], sid, ",".join(res_list[:5]) or "-", grz))

        # 3. Zero-Fuel Docked Factory & Hand-Craft Margins (IRLC pattern)
        print("\n=== 3. ZERO-FUEL DOCKED CRAFTING SPREADS (best output bid vs input ask/base, stock on hand)")
        best_bids = {r["item"]: (float(r["b"] or 0), r["base"]) for r in conn.execute(
            "SELECT item, MAX(bid) as b, base FROM books WHERE bid > 0 AND bid_qty > 0 GROUP BY item"
        ).fetchall()}
        best_asks = {r["item"]: float(r["a"] or 0) for r in conn.execute(
            "SELECT item, MIN(ask) as a FROM books WHERE ask > 0 AND ask_qty > 0 GROUP BY item"
        ).fetchall()}
        base_vals = {r["id"]: float(r["base_value"] or 0) for r in conn.execute("SELECT id, base_value FROM items").fetchall()}
        held_stock = {r["item"]: num(r["u"]) for r in conn.execute("SELECT item, SUM(units) as u FROM holdings GROUP BY item").fetchall()}
        ins_by_rec = {}
        for r in conn.execute("SELECT recipe, item, units FROM recipe_inputs").fetchall():
            ins_by_rec.setdefault(r["recipe"], []).append((r["item"], num(r["units"])))
        outs_by_rec = {}
        for r in conn.execute("SELECT recipe, item, units FROM recipe_outputs").fetchall():
            outs_by_rec.setdefault(r["recipe"], []).append((r["item"], num(r["units"])))
        spreads = []
        for r in conn.execute("SELECT id, name, hand, facility_only FROM recipes").fetchall():
            rid = r["id"]
            outs = outs_by_rec.get(rid) or []
            ins = ins_by_rec.get(rid) or []
            if not outs or not ins:
                continue
            rev = sum((best_bids.get(it, (0.0, ""))[0]) * u for it, u in outs)
            if rev <= 0:
                continue
            cost = sum((best_asks.get(it) or base_vals.get(it, 0.0)) * u for it, u in ins)
            batches_held = min((held_stock.get(it, 0) // max(1, u)) for it, u in ins)
            net = rev - cost
            if net > 50 or (batches_held > 0 and rev > 100):
                out_str = "+".join("%dx%s" % (u, it) for it, u in outs[:2])
                top_station = best_bids.get(outs[0][0], (0.0, ""))[1]
                mode = "hand" if r["hand"] and not r["facility_only"] else "facility"
                spreads.append((batches_held > 0, net, rev, rid, mode, batches_held, out_str, top_station))
        spreads.sort(reverse=True)
        for _has, net, rev, rid, mode, b_held, out_str, top_st in spreads[:10]:
            print("  [%-8s] %-28s -> %-22s | bid %6s cr @ %-22s | spread %+7s cr | vault batches: %d"
                  % (mode, rid[:28], out_str[:22], fmt(rev), str(top_st)[:22], fmt(net), b_held))

        # 4. Hull Promotion & Cross-Empire Exchange Targets
        print("\n=== 4. HULL UPGRADE READINESS & BEST-IN-SLOT TARGETS (All 5 Empires Native + Secondhand Exchange)")
        rdy = conn.execute("""
            SELECT s.division, s.role,
                   SUM(CASE WHEN sk.level >= 10 AND COALESCE(h.tier, 0) < 2 THEN 1 ELSE 0 END) as p10_under_t2,
                   SUM(CASE WHEN sk.level >= 20 AND COALESCE(h.tier, 0) < 3 THEN 1 ELSE 0 END) as p20_under_t3,
                   MAX(sk.level) as max_p
            FROM ships s
            LEFT JOIN ship_skills sk ON sk.pilot = s.pilot AND sk.skill = 'piloting'
            LEFT JOIN hulls h ON LOWER(s.class) = LOWER(h.name) OR LOWER(s.class) = LOWER(h.id)
            GROUP BY s.division, s.role ORDER BY p10_under_t2 DESC
        """).fetchall()
        for r in rdy:
            print("  %-10s (%-8s) | Piloting >=10 below T2: %2d | >=20 below T3: %2d | max Piloting: %2d"
                  % (r["division"], r["role"], num(r["p10_under_t2"]), num(r["p20_under_t3"]), num(r["max_p"])))
        print("  Target hulls across our 5 empires (full specs: game/catalog/ships/<empire>.md):")
        print("    Voidborn: T1 Liminal (75c/3U), Qualia | T2 Resonance Miner (180c/4U), Recursion (3W/2D), Apophenia (240c)")
        print("    Solarian: T1 Archimedes (80c/4U), Axiom (2W/2U) | T2 Excavation (200c/3U), Meridian Freighter (265c/3U), Theorem (3W/3U)")
        print("    Nebula:   T1 Bonanza (180c/3U), Floor Price (400c), Dividend (220c) | T2 Motherlode (200c), Caravan (540c/3U), Prospectus")
        print("    Crimson:  T1 Cleaver (3W/1D), Flail (2W/80c) | T2 Halberd (4W/2D), Broadaxe (4W/1D), War Wagon (1200c/8U)")
        print("    OuterRim: T1 Prayer (540c), Worship (1100c), Congregation (1900c), Warranty Void | T2 Junk Convoy (850c/6U), Dust Devil")
        print("    Neutral:  T1 Ledger (480c), Runner (120c) | T2 Workhorse (300c/4U), Lone Star (240c)")
    finally:
        conn.close()
    return 0


def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)
    if any(a in ("-h", "--help") for a in args):
        sys.exit(__doc__)
    data = args[args.index("--data") + 1] if "--data" in args and args.index("--data") + 1 < len(args) else "/srv/collective/data"
    if "--brief" in args:
        ln = benchmark_line(data)
        if ln:
            print(ln)
        return 0
    return show(data)


if __name__ == "__main__":
    sys.exit(main())

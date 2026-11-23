#!/usr/bin/env python3
"""playbook_anchor.py -- live division telemetry anchor, chapter high-watermark monitor, and empirical drift scanner.

WHAT: separates volatile ground-truth state (ship counts, hull tiers, fitted module builds, skill levels, XP/ship-h
      routes, open division needs, and open requests) from curated tactical prose in game/routes/guidebook/<division>/.
      Follows the Anchor-and-Delta loop design:
        - Live Division Anchor: deterministically computed at read time from read.db, catalog, and requests.log so
          hull builds, skill ladders, open priorities, and open requests never go stale or bloat chapter prose.
        - High-Watermark Curation (>= 85% of chapter cap): warns Admirals before a chapter hits its hard ceiling so
          they merge overlapping rules or mark superseded entries `Status: retired` for hourly eviction into doc_versions.
        - Empirical Drift Scanner: checks active (`proven` and `test`) entries against live game/routes/*.json and
          the active catalog version, flagging archived/disabled route citations, unresolved `test` entries (> 3 days),
          and hardcoded stale catalog versions.
      Also defines the read.db SQL view `division_playbooks` for store.py and handbook.py.
RULES:
  - Read-only: never modifies chapter files, routes, plans, or read.db.
  - Every figure names its live table or file source; missing tables degrade cleanly without raising.
  - Operational route/catalog drift checks run on card, ships, levelling, routes, and tests (historical postmortems
    in lessons and topic-* are exempt from archived-route warnings unless Status is test).
WHY:  Suggi, 2026-11-22: division guidebooks, fleets, leveling guides, ship builds, and open requests/priorities must
      stay fresh automatically as the game evolves while remaining strictly capped against bloat and semantic drift.

USAGE:
  playbook_anchor.py [<division>|<member>|all] [--json] [--drift-only]
  --data <dir>   the unit's data folder (default /srv/collective/data)
  --root <dir>   the repository root (default: two folders above this file)

Stdlib only. ASCII only.
"""

import argparse
import calendar
import json
import os
import re
import sqlite3
import sys
import time
from collections import Counter
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import board                                      # noqa: E402
import division                                   # noqa: E402
import guidebook as book                          # noqa: E402

HIGH_WATERMARK = 0.85
STALE_TEST_DAYS = 3
OPERATIONAL_CHAPTERS = frozenset(("card", "ships", "levelling", "routes", "tests"))
ROUTE_TOKEN = re.compile(
    r"(?<![@a-z0-9_-])((?:mine|gather|trade|carry|craft|hunt|patrol|guard|fit|survey|explore|census|train|"
    r"voidborn|solarian|crimson|nebula|outerrim|salvage|ferry|refuel|supply|buy|sell)-[a-z0-9][a-z0-9-]{2,})\b"
)
CATALOG_VER_RE = re.compile(r"\bcatalog\s+(0\.\d+(?:\.\d+)?)\b", re.I)

EMPIRE_CATALOG_DOC = {
    "voidborn": "game/catalog/ships/voidborn.md",
    "solarian": "game/catalog/ships/solarian.md",
    "nebula": "game/catalog/ships/nebula.md",
    "crimson": "game/catalog/ships/crimson.md",
    "outerrim": "game/catalog/ships/outerrim.md",
    "neutral": "game/catalog/ships/pirate-and-other.md",
}
EMPIRE_MASTERY_SKILLS = (
    "voidborn_mastery", "solarian_doctrine", "nebula_attunement", "crimson_fury", "outerrim_survival",
)

DIV_ROLE_HULL_CATS = {
    "command": ("combat", "fighter", "cruiser", "command", "support", "explorer", "freighter", "multirole"),
    "mining": ("mining", "miner", "harvester", "barge"),
    "trade": ("freighter", "bulk hauler", "hauler", "courier", "transport", "commercial", "trade", "cargo"),
    "logistics": ("freighter", "bulk hauler", "hauler", "transport", "salvager", "cargo", "logistics"),
    "military": ("combat", "fighter", "heavy fighter", "assault", "raider", "interceptor", "corvette", "frigate", "cruiser", "gunship", "monitor", "patrol"),
    "intel": ("explorer", "scout", "recon", "covert", "survey", "research", "blockade runner"),
}

DIV_KEY_SKILLS = {
    "command": ("piloting", "leadership", "tactics", "weapons", "shields", "navigation") + EMPIRE_MASTERY_SKILLS,
    "mining": ("mining", "deep_core_mining", "piloting", "navigation", "refining", "crafting") + EMPIRE_MASTERY_SKILLS,
    "trade": ("trading", "piloting", "navigation", "crafting", "refining", "mining") + EMPIRE_MASTERY_SKILLS,
    "logistics": ("piloting", "navigation", "crafting", "refining", "trading") + EMPIRE_MASTERY_SKILLS,
    "military": ("weapons", "piloting", "shields", "tactics", "armor", "navigation") + EMPIRE_MASTERY_SKILLS,
    "intel": ("exploration", "piloting", "navigation", "scanning", "cloaking") + EMPIRE_MASTERY_SKILLS,
}

SCHEMA = (
    "CREATE VIEW IF NOT EXISTS division_playbooks AS "
    "SELECT d.division AS division, "
    "COALESCE(sh.ships, 0) AS ships, "
    "COALESCE(sh.flying, 0) AS flying, "
    "COALESCE(hr.ready_pilots, 0) AS ready_t2_pilots, "
    "COALESCE(sk.max_piloting, 0) AS max_piloting, "
    "COALESCE(nd.open_needs, 0) AS open_needs, "
    "COALESCE(nd.ready_needs, 0) AS ready_needs, "
    "COALESCE(gd.chapters, 0) AS guide_chapters, "
    "COALESCE(gd.entries, 0) AS guide_entries, "
    "COALESCE(gd.chars, 0) AS guide_chars, "
    "COALESCE(gd.max_pct, 0.0) AS max_chapter_pct "
    "FROM ("
    "SELECT 'command' AS division UNION ALL SELECT 'mining' UNION ALL SELECT 'trade' "
    "UNION ALL SELECT 'logistics' UNION ALL SELECT 'military' UNION ALL SELECT 'intel'"
    ") d "
    "LEFT JOIN ("
    "SELECT LOWER(division) AS division, COUNT(*) AS ships, "
    "SUM(CASE WHEN COALESCE(docked, 0) = 0 THEN 1 ELSE 0 END) AS flying "
    "FROM ships GROUP BY LOWER(division)"
    ") sh ON sh.division = d.division "
    "LEFT JOIN ("
    "SELECT LOWER(division) AS division, COUNT(*) AS ready_pilots "
    "FROM hull_readiness GROUP BY LOWER(division)"
    ") hr ON hr.division = d.division "
    "LEFT JOIN ("
    "SELECT LOWER(s.division) AS division, MAX(k.level) AS max_piloting "
    "FROM ships s JOIN ship_skills k ON k.pilot = s.pilot AND k.skill = 'piloting' "
    "GROUP BY LOWER(s.division)"
    ") sk ON sk.division = d.division "
    "LEFT JOIN ("
    "SELECT LOWER(division) AS division, COUNT(*) AS open_needs, "
    "SUM(CASE WHEN colour = 'green' THEN 1 ELSE 0 END) AS ready_needs "
    "FROM need_status GROUP BY LOWER(division)"
    ") nd ON nd.division = d.division "
    "LEFT JOIN ("
    "SELECT division, COUNT(*) AS chapters, SUM(entries) AS entries, SUM(chars) AS chars, ROUND(MAX(pct), 1) AS max_pct "
    "FROM ("
    "SELECT SUBSTR(path, 23, INSTR(SUBSTR(path, 23), '/') - 1) AS division, path, "
    "SUM(CASE WHEN section != '_head' THEN 1 ELSE 0 END) AS entries, "
    "SUM(CASE WHEN section != '_head' THEN COALESCE(chars, 0) ELSE 0 END) AS chars, "
    "100.0 * SUM(CASE WHEN section != '_head' THEN COALESCE(chars, 0) ELSE 0 END) / "
    "(CASE WHEN path LIKE '%/card.md' THEN 4500.0 ELSE 12000.0 END) AS pct "
    "FROM docs WHERE kind = 'guide' AND path LIKE 'game/routes/guidebook/%/%.md' GROUP BY path"
    ") GROUP BY division"
    ") gd ON gd.division = d.division;\n"
)

DESCRIPTIONS = {
    "division_playbooks": (
        "One live summary row per division combining active ships, Piloting-10+ hull readiness, open/ready needs, "
        "and guidebook chapter utilization against caps."
    ),
}

EXAMPLES = {
    "division_playbooks": (
        ("All 6 divisions' live fleet readiness, open priorities, and guidebook cap utilization",
         "SELECT * FROM division_playbooks ORDER BY division"),
        ("Divisions with chapters near or over the 85% curation watermark",
         "SELECT division, guide_chapters, guide_entries, guide_chars, max_chapter_pct FROM division_playbooks WHERE max_chapter_pct >= 85.0"),
        ("Divisions with 100%-stocked priorities ready to execute or mark done",
         "SELECT division, open_needs, ready_needs FROM division_playbooks WHERE ready_needs > 0"),
    ),
}


def _ver_tuple(ver):
    parts = [int(x) for x in re.findall(r"\d+", str(ver or ""))]
    return tuple(parts) if parts else ()


def latest_catalog_version(data):
    cat_dir = Path(data) / "catalog"
    best, best_t = "", ()
    if cat_dir.is_dir():
        for p in cat_dir.glob("*.json"):
            if re.fullmatch(r"\d+(?:\.\d+)*", p.stem):
                vt = _ver_tuple(p.stem)
                if vt > best_t:
                    best_t, best = vt, p.stem
    return best


def _has_table(conn, name):
    if conn is None:
        return False
    row = conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type IN ('table', 'view') AND name = ?",
        (name,),
    ).fetchone()
    return row is not None


def _active_routes_map(repo_root):
    routes_dir = Path(repo_root) / "game" / "routes"
    active = {}
    if routes_dir.is_dir():
        for p in routes_dir.glob("*.json"):
            try:
                obj = json.loads(p.read_text(encoding="utf-8", errors="replace"))
                if isinstance(obj, dict):
                    active[p.stem] = str(obj.get("status") or "open").lower()
            except (OSError, ValueError):
                active[p.stem] = "unknown"
    return active


def _archived_routes_set(data):
    arch_dir = Path(data) / "routes" / "archive"
    if not arch_dir.is_dir():
        return set()
    return {p.stem for p in arch_dir.glob("*.json")}


def preload_shared_context(conn, repo_root, data="/srv/collective/data", now=None):
    """Read shared repo/store maps once so computing all 6 divisions takes <0.4s instead of 6x repeated scans."""
    now = time.time() if now is None else float(now)
    active_routes = _active_routes_map(repo_root)
    archived_routes = _archived_routes_set(data)
    cat_ver = latest_catalog_version(data)
    try:
        import workclass
        wroutes = workclass.load(str(Path(repo_root) / "game"))
    except Exception:
        wroutes = {}
    cph_map = {}
    if conn is not None and _has_table(conn, "route_hour"):
        cutoff = int(now) - 86400
        for rid, mins, cr in conn.execute(
            "SELECT route, SUM(read_minutes), SUM(credits) FROM route_hour WHERE hour >= ? GROUP BY route",
            (cutoff,),
        ):
            cph_map[rid] = ("", round(60.0 * cr / mins) if mins and mins >= 5 else None)
    comms = _load_comms(repo_root)
    req_states = []
    if comms is not None:
        try:
            entries, _errs = comms.read_log(str(repo_root), "requests", archive=True)
            req_states = comms.request_states(entries)
        except Exception:
            req_states = []
    return {
        "active_routes": active_routes,
        "archived_routes": archived_routes,
        "cat_ver": cat_ver,
        "wroutes": wroutes,
        "cph_map": cph_map,
        "comms": comms,
        "req_states": req_states,
    }


def scan_division_curation(repo_root, division_name, data="/srv/collective/data", now=None, shared=None):
    """Inspect one division's guidebook chapters on disk for cap bands and empirical drift."""
    now = time.time() if now is None else float(now)
    div = str(division_name).lower()
    gdir = Path(repo_root) / book.FOLDER / div
    active_routes = shared["active_routes"] if shared else _active_routes_map(repo_root)
    archived_routes = shared["archived_routes"] if shared else _archived_routes_set(data)
    cat_ver = shared["cat_ver"] if shared else latest_catalog_version(data)
    cat_vt = _ver_tuple(cat_ver)
    has_live_routes = len(active_routes) >= 5

    chapters_out = []
    drift = []
    if not gdir.is_dir():
        return {"chapters": [], "drift_warnings": [], "max_pct": 0.0, "near_count": 0, "over_count": 0, "retired_standing": 0}

    files = sorted((p for p in gdir.glob("*.md") if book.chapter_ok(p.stem)), key=lambda p: book.chapter_rank(p.stem))
    for path in files:
        stem = path.stem
        cap = book.cap_of(stem)
        text = path.read_text(encoding="ascii", errors="replace")
        parsed = book.parse(text)
        entries = parsed["entries"]
        chars = sum(len(e["text"]) for e in entries)
        pct = round(100.0 * chars / cap, 1) if cap else 0.0
        band = "over" if chars > cap else ("near" if chars >= int(cap * HIGH_WATERMARK) else "ok")
        retired_n = sum(1 for e in entries if e.get("status") == "retired")
        dates = [e.get("updated") for e in entries if e.get("updated")]
        chapters_out.append({
            "chapter": stem,
            "path": "%s/%s/%s" % (book.FOLDER, div, path.name),
            "title": parsed["title"] or book.title_line(div, stem).lstrip("# "),
            "entries": len(entries),
            "retired_standing": retired_n,
            "chars": chars,
            "cap": cap,
            "pct": pct,
            "band": band,
            "updated_last": max(dates) if dates else "",
        })
        if not entries:
            drift.append({
                "chapter": stem,
                "entry": "(chapter)",
                "kind": "empty_chapter",
                "detail": "%s.md holds 0 entries; add concise class rules or keep anchored to live telemetry" % stem,
            })
            continue
        for entry in entries:
            st = entry.get("status")
            if st == "retired":
                continue
            etitle = entry.get("title") or "?"
            upd = entry.get("updated") or ""
            if st == "test" and upd:
                try:
                    age_d = (now - calendar.timegm(time.strptime(upd, "%Y-%m-%d"))) / 86400.0
                    if age_d >= STALE_TEST_DAYS + 1:
                        drift.append({
                            "chapter": stem,
                            "entry": etitle,
                            "kind": "stale_test",
                            "detail": "Status: test unchanged since %s (%.0fd) -- promote to proven with RESULT or mark retired" % (upd, age_d),
                        })
                except ValueError:
                    pass
            if stem not in OPERATIONAL_CHAPTERS:
                continue
            hay = (entry.get("status_line") or "") + "\n" + (entry.get("body") or "")
            if cat_vt:
                old_vers = sorted({m.group(1) for m in CATALOG_VER_RE.finditer(hay) if _ver_tuple(m.group(1)) and _ver_tuple(m.group(1)) < cat_vt})
                if old_vers:
                    drift.append({
                        "chapter": stem,
                        "entry": etitle,
                        "kind": "stale_catalog_ref",
                        "detail": "cites catalog %s while live catalog is %s -- re-verify or cite live table without pinning old patch" % (", ".join(old_vers), cat_ver),
                    })
            if has_live_routes:
                cited = sorted(set(ROUTE_TOKEN.findall(hay)))
                dead, off = [], []
                for rid in cited:
                    if rid.endswith("-"):
                        continue
                    if rid not in active_routes:
                        if rid in archived_routes:
                            dead.append(rid + " (archived)")
                        else:
                            # Skip route-group index stems (e.g. trade-books -> index-trade-books.md) and prefix stems (e.g. hunt-test-*)
                            is_group = (Path(repo_root) / "game" / "routes" / ("index-" + rid + ".md")).is_file()
                            is_prefix = any(k.startswith(rid + "-") for k in active_routes)
                            if not is_group and not is_prefix and re.search(r"(?:\broute\s+|Evidence:[^\n]*\b)" + re.escape(rid) + r"(?![a-z0-9_-]*\*)", hay):
                                dead.append(rid)
                    elif active_routes.get(rid) in ("off", "retired", "closed"):
                        off.append(rid)
                if dead:
                    drift.append({
                        "chapter": stem,
                        "entry": etitle,
                        "kind": "archived_route",
                        "detail": "cites inactive/archived route(s): %s -- update to current route or mark entry retired" % ", ".join(dead[:4]),
                    })
                if off:
                    drift.append({
                        "chapter": stem,
                        "entry": etitle,
                        "kind": "disabled_route",
                        "detail": "cites disabled (status=off) route(s): %s" % ", ".join(off[:4]),
                    })

    return {
        "chapters": chapters_out,
        "drift_warnings": drift,
        "max_pct": max((c["pct"] for c in chapters_out), default=0.0),
        "near_count": sum(1 for c in chapters_out if c["band"] == "near"),
        "over_count": sum(1 for c in chapters_out if c["band"] == "over"),
        "retired_standing": sum(c["retired_standing"] for c in chapters_out),
    }


def _load_comms(repo_root):
    import importlib.util
    cpath = Path(repo_root) / "scripts" / "comms.py"
    if not cpath.is_file():
        return None
    spec = importlib.util.spec_from_file_location("collective_comms_anchor", str(cpath))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def open_requests_for(repo_root, member, now=None, shared=None):
    now = time.time() if now is None else float(now)
    comms = shared["comms"] if shared else _load_comms(repo_root)
    if comms is None:
        return []
    if shared is not None:
        states = shared["req_states"]
    else:
        try:
            entries, _errs = comms.read_log(str(repo_root), "requests", archive=True)
            states = comms.request_states(entries)
        except Exception:
            return []
    out = []
    who_low = (member or "").lower()
    for state, req, ans in states:
        if state == "CLOSED":
            continue
        involved = (who_low in ("", "all", "unity")) or (req.get("by", "").lower() == who_low) or comms.addressed(req, member)
        if not involved:
            continue
        sdays = comms.stale_days(state, req, ans, now)
        out.append({
            "ent": "ENT-%03d" % int(req.get("num") or 0),
            "state": state,
            "when": str(req.get("when") or ""),
            "from": str(req.get("by") or ""),
            "to": str(comms.field(req, "To")).rstrip(".") or "?",
            "by_when": str(comms.field(req, "By")).rstrip(".") or "--",
            "need": str(comms.field(req, "Need"))[:200],
            "stale_days": round(sdays, 1) if sdays is not None else None,
            "answer_ent": ("ENT-%03d" % int(ans["num"])) if ans and ans.get("num") else "",
            "answer_by": str(ans.get("by") or "") if ans else "",
        })
    return out


def compute_division_anchor(conn, repo_root, data="/srv/collective/data", division_name="mining", now=None, shared=None):
    """Build the complete zero-drift Live Division Anchor for one division."""
    now = time.time() if now is None else float(now)
    div = book.which(division_name)
    if not div or div == "all":
        div = "command"
    member = book.member_of(div)
    roles = sorted(r for r, m in division.ROLES.items() if m == member)
    cat_ver = shared["cat_ver"] if shared else latest_catalog_version(data)
    stamp = time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime(now))

    fleet_summary = {
        "ships_total": 0, "flying": 0, "docked": 0, "on_route": 0,
        "empires": [], "hulls": [], "ready_pilots": 0, "max_piloting": 0, "avg_piloting": 0.0,
        "next_unlocks": [], "empire_catalog": [],
    }
    ship_builds = []
    empty_slots = {"weapon": 0, "defense": 0, "utility": 0}
    leveling = {"skills": [], "top_xp_routes": []}
    open_needs = []

    if conn is not None and _has_table(conn, "ships"):
        ship_cols = {r[1] for r in conn.execute("PRAGMA table_info(ships)").fetchall()}
        emp_expr = "LOWER(COALESCE(NULLIF(s.empire, ''), 'voidborn'))" if "empire" in ship_cols else "'voidborn'"
        srows = conn.execute(
            "SELECT s.pilot, s.role, s.class, COALESCE(s.docked, 0), COALESCE(s.flies, ''), "
            "COALESCE(h.tier, 0), COALESCE(h.cargo, s.cargo_capacity, 0), "
            "COALESCE(h.weapon_slots, 0), COALESCE(h.defense_slots, 0), COALESCE(h.utility_slots, 0), "
            + emp_expr + " "
            "FROM ships s LEFT JOIN hulls h ON LOWER(s.class) = LOWER(h.name) OR LOWER(s.class) = LOWER(h.id) "
            "WHERE LOWER(s.division) = ? ORDER BY s.number, s.pilot",
            (div,),
        ).fetchall()
        fleet_summary["ships_total"] = len(srows)
        fleet_summary["docked"] = sum(1 for r in srows if r[3])
        fleet_summary["flying"] = len(srows) - fleet_summary["docked"]
        fleet_summary["on_route"] = sum(1 for r in srows if r[4])
        emp_counts = Counter(r[10] for r in srows)
        fleet_summary["empires"] = [
            {"empire": e, "ships": cnt}
            for e, cnt in sorted(emp_counts.items(), key=lambda kv: (-kv[1], kv[0]))
        ]

        hull_counts = Counter((r[2] or "Unknown", int(r[5] or 0), int(r[6] or 0), int(r[9] or 0), int(r[7] or 0)) for r in srows)
        fleet_summary["hulls"] = [
            {"class": hcls, "tier": tier, "count": cnt, "cargo": cargo, "utility_slots": util, "weapon_slots": weap}
            for (hcls, tier, cargo, util, weap), cnt in sorted(hull_counts.items(), key=lambda kv: (-kv[1], kv[0][1], kv[0][0]))
        ]

        pilots_map = {r[0]: r for r in srows}
        mod_by_pilot = {p: [] for p in pilots_map}
        slot_used = {p: Counter() for p in pilots_map}
        if pilots_map and _has_table(conn, "ship_modules"):
            qmarks = ",".join("?" for _ in pilots_map)
            for pilot, mname, mid, mslot in conn.execute(
                "SELECT pilot, COALESCE(NULLIF(name, ''), module), module, LOWER(COALESCE(slot, '')) "
                "FROM ship_modules WHERE pilot IN (%s)" % qmarks,
                tuple(pilots_map),
            ):
                mod_by_pilot[pilot].append(mname or mid or "?")
                if mslot in ("weapon", "defense", "utility"):
                    slot_used[pilot][mslot] += 1

        build_counter = Counter()
        for pilot, r in pilots_map.items():
            hcls, wmax, dmax, umax = r[2] or "Unknown", int(r[7] or 0), int(r[8] or 0), int(r[9] or 0)
            ew = max(0, wmax - slot_used[pilot]["weapon"])
            ed = max(0, dmax - slot_used[pilot]["defense"])
            eu = max(0, umax - slot_used[pilot]["utility"])
            empty_slots["weapon"] += ew
            empty_slots["defense"] += ed
            empty_slots["utility"] += eu
            mods = Counter(mod_by_pilot[pilot])
            mod_str = " + ".join(
                ("%s x%d" % (m, c) if c > 1 else m) for m, c in sorted(mods.items())
            ) or "(unfitted)"
            build_counter[(hcls, int(r[5] or 0), mod_str)] += 1

        ship_builds = [
            {"hull": hcls, "tier": tier, "loadout": mod_str, "ships": cnt}
            for (hcls, tier, mod_str), cnt in sorted(build_counter.items(), key=lambda kv: (-kv[1], kv[0][0]))[:8]
        ]

        if _has_table(conn, "ship_skills") and pilots_map:
            prow = conn.execute(
                "SELECT COUNT(*), ROUND(AVG(k.level), 1), MAX(k.level) "
                "FROM ships s JOIN ship_skills k ON k.pilot = s.pilot AND k.skill = 'piloting' "
                "WHERE LOWER(s.division) = ?",
                (div,),
            ).fetchone()
            if prow and prow[0]:
                fleet_summary["avg_piloting"] = float(prow[1] or 0.0)
                fleet_summary["max_piloting"] = int(prow[2] or 0)

        if _has_table(conn, "hull_readiness"):
            rrow = conn.execute(
                "SELECT COUNT(*) FROM hull_readiness WHERE LOWER(division) = ?",
                (div,),
            ).fetchone()
            fleet_summary["ready_pilots"] = int(rrow[0] or 0) if rrow else 0

        if _has_table(conn, "hulls"):
            cats = DIV_ROLE_HULL_CATS.get(div, ())
            hull_cols = {r[1] for r in conn.execute("PRAGMA table_info(hulls)").fetchall()}
            fuel_c = "COALESCE(fuel, 0)" if "fuel" in hull_cols else "0"
            cpu_c = "COALESCE(cpu, 0)" if "cpu" in hull_cols else "0"
            pwr_c = "COALESCE(power, 0)" if "power" in hull_cols else "0"
            hrows = conn.execute(
                "SELECT name, COALESCE(tier, 0), COALESCE(piloting_required, 0), COALESCE(cargo, 0), "
                "COALESCE(weapon_slots, 0), COALESCE(defense_slots, 0), COALESCE(utility_slots, 0), "
                "LOWER(COALESCE(category, '')), LOWER(COALESCE(class, '')), LOWER(COALESCE(faction, '')), "
                "%s, %s, %s FROM hulls WHERE COALESCE(tier, 0) IN (0, 1, 2, 3)" % (fuel_c, cpu_c, pwr_c)
            ).fetchall()
            starters_by_emp = {}
            by_emp = {}
            for hr in hrows:
                fac = hr[9] or "neutral"
                if fac in ("any", ""):
                    fac = "neutral"
                tier_v = int(hr[1] or 0)
                if tier_v == 0:
                    starters_by_emp[fac] = {
                        "name": hr[0], "tier": 0, "cargo": int(hr[3] or 0), "fuel": int(hr[10] or 0),
                        "slots": "%dW/%dD/%dU" % (hr[4], hr[5], hr[6]),
                        "cpu": int(hr[11] or 0), "power": int(hr[12] or 0), "faction": fac,
                    }
                    continue
                hay_c = hr[7] + " " + hr[8] + " " + hr[0].lower()
                if any(k in hay_c for k in cats):
                    tier_rank = {2: 0, 1: 1, 3: 2}.get(tier_v, 3)
                    score_key = (-int(hr[4] or 0), -int(hr[5] or 0), -int(hr[3] or 0)) if div == "military" else (-int(hr[3] or 0), -int(hr[6] or 0))
                    by_emp.setdefault(fac, []).append((tier_rank, score_key, {
                        "name": hr[0], "tier": tier_v, "piloting_req": int(hr[2] or 0),
                        "cargo": int(hr[3] or 0), "slots": "%dW/%dD/%dU" % (hr[4], hr[5], hr[6]),
                        "faction": fac, "role_class": hr[8] or hr[7],
                    }))
            for fac in by_emp:
                by_emp[fac].sort(key=lambda x: (x[0], x[1]))
            active_emps = [e["empire"] for e in fleet_summary["empires"]] or ["voidborn"]
            emp_ship_map = {e["empire"]: e["ships"] for e in fleet_summary["empires"]}
            catalog_emps = list(active_emps)
            if div in ("trade", "logistics", "mining") and "neutral" in by_emp and "neutral" not in catalog_emps:
                catalog_emps.append("neutral")
            emp_cat_out = []
            unlocks_out = []
            for fac in catalog_emps:
                pool = [x[2] for x in by_emp.get(fac, ())]
                chosen = []
                for want_t, cap_t in ((1, 2), (2, 2), (3, 1)):
                    got_t = [u for u in pool if u["tier"] == want_t][:cap_t]
                    chosen.extend(got_t)
                if not chosen:
                    chosen = pool[:4]
                emp_cat_out.append({
                    "empire": fac,
                    "ships": emp_ship_map.get(fac, 0),
                    "catalog_doc": EMPIRE_CATALOG_DOC.get(fac, "game/catalog/master-index.md"),
                    "starter": starters_by_emp.get(fac),
                    "upgrades": chosen,
                })
                limit_u = 3 if fac in active_emps else 2
                unlocks_out.extend(chosen[:limit_u])
            fleet_summary["empire_catalog"] = emp_cat_out
            fleet_summary["next_unlocks"] = unlocks_out[:16]

        if _has_table(conn, "ship_skills"):
            xp_rates = {}
            if _has_table(conn, "stats_figures"):
                for subj, val, n in conn.execute(
                    "SELECT subject, value, n FROM stats_figures WHERE view = 'xp' AND figure = 'xp_per_ship_hour' AND hours = 24.0"
                ):
                    if "|" in str(subj):
                        rname, sk_id = str(subj).split("|", 1)
                        if rname in roles and val is not None:
                            prev = xp_rates.get(sk_id)
                            if prev is None or val > prev[0]:
                                xp_rates[sk_id] = (round(float(val), 1), int(n or 0))
            key_order = DIV_KEY_SKILLS.get(div, ())
            sk_rows = conn.execute(
                "SELECT k.skill, COALESCE(sk.name, k.skill), COUNT(*), ROUND(AVG(k.level), 1), MIN(k.level), MAX(k.level) "
                "FROM ship_skills k JOIN ships s ON s.pilot = k.pilot "
                "LEFT JOIN skills sk ON sk.id = k.skill "
                "WHERE LOWER(s.division) = ? GROUP BY k.skill",
                (div,),
            ).fetchall()
            sk_rows.sort(key=lambda r: (
                key_order.index(r[0]) if r[0] in key_order else 99,
                -(r[3] or 0),
            ))
            for sk_id, sk_name, cnt, avg_l, min_l, max_l in sk_rows[:10]:
                xpr = xp_rates.get(sk_id)
                leveling["skills"].append({
                    "id": sk_id, "name": sk_name, "pilots": int(cnt or 0),
                    "min": int(min_l or 0), "avg": float(avg_l or 0.0), "max": int(max_l or 0),
                    "xp_per_ship_h": xpr[0] if xpr else None, "xp_n": xpr[1] if xpr else 0,
                })

        if _has_table(conn, "stats_figures"):
            try:
                import workclass
            except Exception:
                workclass = None
            if shared is not None:
                wroutes, cph_map = shared["wroutes"], shared["cph_map"]
            else:
                try:
                    import workclass
                    wroutes = workclass.load(str(Path(repo_root) / "game"))
                except Exception:
                    wroutes = {}
                cph_map = {}
                if _has_table(conn, "route_hour"):
                    cutoff = int(now) - 86400
                    for rid, mins, cr in conn.execute(
                        "SELECT route, SUM(read_minutes), SUM(credits) FROM route_hour WHERE hour >= ? GROUP BY route",
                        (cutoff,),
                    ):
                        cph_map[rid] = ("", round(60.0 * cr / mins) if mins and mins >= 5 else None)
            xproutes = []
            for rid, val, n in conn.execute(
                "SELECT subject, value, n FROM stats_figures WHERE view = 'xp' AND figure = 'route_xp_per_ship_hour' AND hours = 24.0"
            ):
                if val is None or rid not in wroutes:
                    continue
                if any(workclass.own(role, wroutes[rid], rid) for role in roles):
                    rk, rcph = cph_map.get(rid, (wroutes[rid].get("kind") or "", None))
                    xproutes.append({
                        "route": rid,
                        "kind": rk or str(wroutes[rid].get("kind") or ""),
                        "xp_per_ship_h": round(float(val), 1),
                        "n": int(n or 0),
                        "cph_24h": int(rcph) if rcph is not None else None,
                    })
            xproutes.sort(key=lambda x: -x["xp_per_ship_h"])
            leveling["top_xp_routes"] = xproutes[:6]

        if _has_table(conn, "need_status"):
            nd_q = (
                "SELECT id, priority, division, kind, ref, units, COALESCE(covered, 0), COALESCE(colour, ''), "
                "COALESCE(short_items, ''), COALESCE(gather, ''), COALESCE(buy, ''), COALESCE(craft, ''), "
                "COALESCE(fee, 0), COALESCE(stale, ''), COALESCE(project, '') "
                "FROM need_status "
                + ("" if div == "command" else "WHERE LOWER(division) = ? ")
                + "ORDER BY priority, rank LIMIT 15"
            )
            nd_args = () if div == "command" else (div,)
            for r in conn.execute(nd_q, nd_args):
                ready = (r[7] == "green") or (float(r[6] or 0) >= 100.0 and not r[8])
                open_needs.append({
                    "id": r[0], "priority": int(r[1] or 2), "division": r[2], "kind": r[3],
                    "ref": r[4], "units": int(r[5] or 1), "covered": round(float(r[6] or 0), 1),
                    "colour": r[7], "short_items": r[8], "gather": r[9], "buy": r[10],
                    "craft": r[11], "fee": int(r[12] or 0), "stale": r[13], "project": r[14],
                    "ready_to_close": bool(ready),
                })

    curation = scan_division_curation(repo_root, div, data=data, now=now, shared=shared)
    requests = open_requests_for(repo_root, member, now=now, shared=shared)

    return {
        "division": div,
        "title": div.capitalize(),
        "member": member,
        "roles": roles,
        "catalog_version": cat_ver or "unknown",
        "computed_at": stamp,
        "fleet": fleet_summary,
        "empty_slots": empty_slots,
        "ship_builds": ship_builds,
        "leveling": leveling,
        "open_needs": open_needs,
        "open_requests": requests,
        "curation": curation,
    }


def anchor_lines(anchor):
    """Compact human- & agent-readable lines for `hive.py guide <division>`."""
    fl = anchor["fleet"]
    es = anchor["empty_slots"]
    lines = []
    hulls_txt = ", ".join("%s (T%d) x%d" % (h["class"], h["tier"], h["count"]) for h in fl["hulls"]) or "none"
    emps_txt = ", ".join("%s x%d" % (e["empire"], e["ships"]) for e in (fl.get("empires") or [])) or "voidborn"
    lines.append(
        "  Fleet & Hulls (live read.db, catalog %s): %d ships (%d flying, %d docked, %d on route) | Empires: %s | %s | "
        "Piloting avg %.1f / max %d (%d ready for Tier 2+)"
        % (anchor["catalog_version"], fl["ships_total"], fl["flying"], fl["docked"], fl["on_route"],
           emps_txt, hulls_txt, fl["avg_piloting"], fl["max_piloting"], fl["ready_pilots"])
    )
    if anchor["ship_builds"]:
        btxt = "; ".join("%s [%s] x%d" % (b["hull"], b["loadout"], b["ships"]) for b in anchor["ship_builds"][:6])
        lines.append(
            "  Active Ship Builds (table ship_modules; empty slots %dW/%dD/%dU): %s"
            % (es["weapon"], es["defense"], es["utility"], btxt)
        )
    if fl.get("empire_catalog"):
        lines.append("  Multi-Empire Ship Catalog (table hulls; full specs in game/catalog/ships/<empire>.md):")
        for ec in fl["empire_catalog"]:
            st = ec.get("starter")
            st_txt = "T0 %s (%dc/%df, %s)" % (st["name"], st["cargo"], st["fuel"], st["slots"]) if st else "neutral exchange"
            up_txt = "; ".join(
                "%s (T%d, P%d, %dc, %s)" % (u["name"], u["tier"], u["piloting_req"], u["cargo"], u["slots"])
                for u in (ec.get("upgrades") or [])[:5]
            ) or "none"
            lines.append("    - %s (%d ships, %s): %s -> %s" % (ec["empire"], ec["ships"], ec["catalog_doc"], st_txt, up_txt))
    elif fl["next_unlocks"]:
        utxt = "; ".join("%s [%s] (T%d, P%d, hold %d, %s)" % (u["name"], u.get("faction", "?"), u["tier"], u["piloting_req"], u["cargo"], u["slots"]) for u in fl["next_unlocks"][:8])
        lines.append("  Catalog Hull Ladder (table hulls): " + utxt)
    if anchor["leveling"]["skills"]:
        stxt = "; ".join(
            "%s avg %.1f (min %d..max %d%s)" % (
                s["name"], s["avg"], s["min"], s["max"],
                ", %.1f XP/h" % s["xp_per_ship_h"] if s["xp_per_ship_h"] is not None else "",
            )
            for s in anchor["leveling"]["skills"][:9]
        )
        lines.append("  Skill Rungs (table ship_skills): " + stxt)
    if anchor["open_needs"]:
        ntxt = "; ".join(
            "[P%d %.0f%%%s] %s (%s x%d)" % (
                n["priority"], n["covered"], " READY->done" if n["ready_to_close"] else "",
                n["id"], n["ref"], n["units"],
            )
            for n in anchor["open_needs"][:6]
        )
        lines.append("  Open Priorities (table need_status, %d open): %s" % (len(anchor["open_needs"]), ntxt))
    else:
        lines.append("  Open Priorities (table need_status): 0 open for %s" % anchor["title"])
    if anchor["open_requests"]:
        rtxt = "; ".join(
            "%s [%s%s] %s->%s: %s" % (
                r["ent"], r["state"], " STALE" if r["stale_days"] else "",
                r["from"], r["to"], r["need"][:70],
            )
            for r in anchor["open_requests"][:4]
        )
        lines.append("  Open Requests (communications/requests.log, %d active): %s" % (len(anchor["open_requests"]), rtxt))
    else:
        lines.append("  Open Requests (communications/requests.log): 0 open involving %s" % anchor["member"])

    cur = anchor["curation"]
    near = [c for c in cur["chapters"] if c["band"] in ("near", "over")]
    if near:
        lines.append(
            "  High-Watermark Chapters (>= 85% cap -- merge or mark outdated entries Status: retired): "
            + ", ".join("%s.md %.1f%% (%d/%d)" % (c["chapter"], c["pct"], c["chars"], c["cap"]) for c in near)
        )
    if cur["drift_warnings"]:
        lines.append("  Empirical Drift Checks (%d item(s) to re-verify or retire):" % len(cur["drift_warnings"]))
        for w in cur["drift_warnings"][:6]:
            lines.append("    - %s.md `%s` [%s]: %s" % (w["chapter"], w["entry"][:45], w["kind"], w["detail"]))
    return lines


def open_ro_db(data):
    dbp = Path(data) / "store" / "read.db"
    if not dbp.is_file():
        return None
    try:
        return sqlite3.connect("file:%s?mode=ro" % dbp, uri=True, timeout=2.0)
    except sqlite3.Error:
        return None


def main(argv=None):
    parser = argparse.ArgumentParser(prog="playbook_anchor.py", description=__doc__.split("\n")[0])
    parser.add_argument("target", nargs="?", default="all")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--drift-only", action="store_true")
    parser.add_argument("--data", default="/srv/collective/data")
    parser.add_argument("--root", default=str(Path(__file__).resolve().parents[2]))
    args = parser.parse_args(sys.argv[1:] if argv is None else argv)

    target = book.which(args.target)
    if target is None:
        print("playbook_anchor.py: unknown division or member `%s`" % args.target)
        return 1
    divs = list(book.DIVISIONS) if target == "all" else [target]

    if args.drift_only:
        payload = {d: scan_division_curation(args.root, d, data=args.data) for d in divs}
        if args.json:
            print(json.dumps(payload, indent=2))
            return 0
        total_w = sum(len(v["drift_warnings"]) for v in payload.values())
        total_n = sum(v["near_count"] + v["over_count"] for v in payload.values())
        print("PLAYBOOK DRIFT & CAP HEALTH | %s | %d chapter(s) >= 85%% cap, %d drift item(s)" % (target, total_n, total_w))
        for d in divs:
            cur = payload[d]
            near = [c for c in cur["chapters"] if c["band"] in ("near", "over")]
            print("  %-10s max %.1f%% | near/over: %s | drift: %d" % (
                d.capitalize(), cur["max_pct"],
                ", ".join("%s %.0f%%" % (c["chapter"], c["pct"]) for c in near) or "none",
                len(cur["drift_warnings"]),
            ))
            for w in cur["drift_warnings"]:
                print("    WARN %s/%s.md `%s` [%s]: %s" % (d, w["chapter"], w["entry"][:50], w["kind"], w["detail"]))
        return 0

    conn = open_ro_db(args.data)
    try:
        shared = preload_shared_context(conn, args.root, data=args.data) if len(divs) > 1 else None
        anchors = [compute_division_anchor(conn, args.root, data=args.data, division_name=d, shared=shared) for d in divs]
    finally:
        if conn is not None:
            conn.close()
    if args.json:
        print(json.dumps(anchors if target == "all" else anchors[0], indent=2))
        return 0
    for a in anchors:
        print("=== PLAYBOOK ANCHOR: %s (%s) ===" % (a["title"], a["member"]))
        for line in anchor_lines(a):
            print(line)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        sys.exit(0)

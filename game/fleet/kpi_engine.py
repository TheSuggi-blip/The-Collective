"""Goodhart-proof 17-wing KPI scorecard, dynamic max-possible upgrade gap engine, and closed-loop signal publisher.

Usage: imported by scorecard.py, station/server.py, upgrades.py, mine_net.py, hunt_net.py, and haul.py.

Pure Python standard library (7-bit ASCII, read-only SQLite `&immutable=1`).
Produces:
1. Dynamic max-possible Hull and Module upgrade gaps (scaling automatically across T1 -> T5 as pilots skill up).
2. Whole-fleet north-star KPIs reconciled 1:1 with IFRS 15 Core Operating Profit (Ex-Seeds) and Paid Fuel.
3. 17 specialized wing KPI cards (covering 100% of the 500-ship fleet with zero Admiral references),
   pairing offensive throughput/value accelerators with defensive fuel-ROI, survival, freshness, and idle->0 brakes.
4. Machine-readable closed-loop signals (`data/fleet/kpi_signals.json`) steering auto-upgrades and AutoNet fuel discipline.
"""
from datetime import datetime, timezone
import json
import math
import os
from pathlib import Path
import re
import sqlite3
import time

REPO_DEFAULT = Path(__file__).resolve().parents[2]
DATA_DEFAULT = Path("/srv/collective/data")
SIGNAL_TTL_S = 55.0
_CRAFT_RE = re.compile(r"crafted\s+(\d+)x\s+([a-z0-9_]+)", re.IGNORECASE)
_ROMAN_TIER = {"i": 1, "ii": 2, "iii": 3, "iv": 4, "v": 5}
_LAST_SIGNAL_WRITE = 0.0

# 17 canonical operational units covering 100% of the 500-ship standing fleet (zero Admiral labels)
WING_SPECS = (
    ("1A-1C", "Defense & Task Forces",       "Military",      "Combat",        ("1A-", "1B.", "1C."), "Defense & Pack Combat"),
    ("2A-2B", "Hunters (Heavy & Fast)",      "Military",      "Combat",        ("2A.", "2B."),        "Combat Extraction"),
    ("3A",    "Ore -- Precision",            "Mining",        "Mining",        ("3A.",),              "Precision Extraction"),
    ("3B",    "Ore -- Bulk",                 "Mining",        "Mining",        ("3B.",),              "Industrial Feedstock"),
    ("3C",    "Deep-Core & Rad",             "Mining",        "Mining",        ("3C.",),              "Rare & Rad Extraction"),
    ("3D",    "Gas Harvesters",              "Mining",        "Mining",        ("3D.",),              "Gas Extraction"),
    ("3E",    "Ice Harvesters",              "Mining",        "Mining",        ("3E.",),              "Ice & Fuel Feedstock"),
    ("4A",    "Express Arbitrage",           "Trade",         "Trade",         ("4A.",),              "Mobile Arbitrage"),
    ("4B",    "Bulk Trade Haulers",          "Trade",         "Trade",         ("4B.",),              "Volume Liquidation"),
    ("4C",    "Pure Bursar Desks",           "Trade",         "Trade",         ("4C.",),              "Zero-Fuel Exchange"),
    ("5A",    "Station Refiners & Bursars",  "Trade",         "Manufacturing", ("5A.",),              "Zero-Fuel Refinery"),
    ("5B",    "Mobile Field Workshops",      "Trade",         "Manufacturing", ("5B.",),              "Mobile Manufacturing"),
    ("6A",    "Supply Bulk Haulers",         "Logistics",     "Logistics",     ("6A.",),              "Supply-Chain SLA"),
    ("6B",    "Passenger & Resort Liners",   "Logistics",     "Logistics",     ("6B.",),              "Tourism (Staged)"),
    ("6C",    "Fuel & Salvage Tenders",      "Logistics",     "Logistics",     ("6C.",),              "Bunkers & Salvage SLA"),
    ("7A",    "Covert Recon",                "Intel",         "Intel",         ("7A.",),              "Rival & Frontier Intel"),
    ("7B",    "Deep-Core Surveyors",         "Intel",         "Intel",         ("7B.",),              "Galaxy Resource Intel"),
)
WING_BY_ID = {w[0]: w for w in WING_SPECS}
BURSAR_WING_IDS = frozenset({"4C", "5A"})


def wing_id_of(wing_label, division=""):
    wl = str(wing_label or "").strip()
    for wid, _name, _div, _pil, prefixes, _rc in WING_SPECS:
        if any(wl.startswith(p) for p in prefixes):
            return wid
    d = str(division or "").strip()
    if d == "Military":
        return "1A-1C"
    if d == "Mining":
        return "3A"
    if d == "Trade":
        return "4B"
    if d == "Logistics":
        return "6A"
    if d == "Intel":
        return "7A"
    return "1A-1C"


def _read_json(path, default):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def _parse_iso(val):
    if isinstance(val, (int, float)):
        return float(val)
    if not isinstance(val, str) or not val.strip():
        return None
    s = val.strip()
    try:
        if s.endswith("Z"):
            s = s[:-1] + "+00:00"
        dt = datetime.fromisoformat(s)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.timestamp()
    except Exception:
        return None


def _module_tier(mod_id, mod_name=""):
    """Infer module tier (1-5) from module id/name; named high-end specialties return 2."""
    for raw in (str(mod_id or ""), str(mod_name or "")):
        low = raw.strip().lower()
        if not low:
            continue
        parts = re.split(r"[\s_]+", low)
        if parts and parts[-1] in _ROMAN_TIER:
            return _ROMAN_TIER[parts[-1]]
    low_id = str(mod_id or "").lower()
    if any(k in low_id for k in ("phase_cloaking", "deep_core", "fuel_optimizer", "expanded_fuel", "damage_control", "rad_harvester")):
        return 2
    return 1


def _score_band(val, good, warn, higher_better=True):
    """Smooth 0..100 KPI score (no brittle cliff edges)."""
    if val is None:
        return None
    v = float(val)
    if higher_better:
        if v >= good:
            return 100.0
        if v <= 0.0 and warn > 0.0:
            return 0.0
        if v >= warn:
            return 70.0 + 30.0 * (v - warn) / max(1e-6, (good - warn))
        return max(0.0, 70.0 * (v / max(1e-6, warn)))
    if v <= good:
        return 100.0
    if v <= warn:
        return 70.0 + 30.0 * (warn - v) / max(1e-6, (warn - good))
    span = max(warn, 1.0)
    return max(0.0, 70.0 * max(0.0, 1.0 - (v - warn) / (span * 2.0)))


HWM_FILE = "kpi_hwm.json"
HWM_EWMA_ALPHA = 0.30
HWM_BREAKOUT_MARGIN = 1.02

# Base reference ship counts per wing at T0 par (dynamic tier capacity scales automatically as hulls upgrade T0->T5)
WING_BASE_SHIPS = {
    "1A-1C": 48, "2A-2B": 62, "3A": 38, "3B": 22, "3C": 18, "3D": 40, "3E": 30,
    "4A": 25, "4B": 25, "4C": 38, "5A": 22, "5B": 15, "6A": 30, "6B": 12, "6C": 30,
    "7A": 20, "7B": 25,
}


def _load_hwm(data_dir):
    d = _read_json(Path(data_dir) / "fleet" / HWM_FILE, {})
    return d if isinstance(d, dict) else {}


def _save_hwm(data_dir, hwm_doc, now_t):
    try:
        out_p = Path(data_dir) / "fleet" / HWM_FILE
        out_p.parent.mkdir(parents=True, exist_ok=True)
        payload = dict(hwm_doc)
        payload["updated_at"] = int(now_t)
        tmp = out_p.with_name(f"kpi_hwm.{os.getpid()}.tmp")
        tmp.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="ascii")
        os.replace(tmp, out_p)
    except OSError:
        pass


def _ratchet_hwm_high(prev, val):
    if val is None or val <= 0.0:
        return prev
    v = float(val)
    if prev is None or prev <= 0.0:
        return round(v, 2)
    if v > float(prev):
        return round(max(float(prev), float(prev) * (1.0 - HWM_EWMA_ALPHA) + v * HWM_EWMA_ALPHA), 2)
    return round(float(prev), 2)


def _ratchet_hwm_low(prev, val):
    if val is None or val <= 0.0:
        return prev
    v = float(val)
    if prev is None or prev <= 0.0:
        return round(v, 2)
    if v < float(prev):
        return round(min(float(prev), float(prev) * (1.0 - HWM_EWMA_ALPHA) + v * HWM_EWMA_ALPHA), 2)
    return round(float(prev), 2)


def _score_open_ended(val, dyn_target, warn_ratio=0.45, hwm=None):
    """Unbounded Super-Efficiency DEA + Ratcheting HWM score for higher-is-better frontier KPIs."""
    if val is None or dyn_target is None or dyn_target <= 0.0:
        return (None, False)
    v = float(val)
    tgt = float(dyn_target)
    warn = max(1e-6, tgt * float(warn_ratio))
    if v <= 0.0:
        return (0.0, False)
    if v < warn:
        base = max(0.0, 60.0 * (v / warn))
    elif v < tgt:
        base = 60.0 + 40.0 * ((v - warn) / max(1e-6, tgt - warn))
    else:
        base = 100.0 + 38.0 * math.log(max(1.0, v / tgt))
    breakout = bool(hwm is not None and float(hwm) > 0.0 and v > float(hwm) * HWM_BREAKOUT_MARGIN and v >= tgt * 0.80)
    if breakout:
        base += 6.0
    return (round(base, 1), breakout)


def _score_open_ended_low(val, dyn_target, warn, hwm_low=None):
    """Unbounded Super-Efficiency score for lower-is-better freshness/latency KPIs (minutes)."""
    if val is None or dyn_target is None or dyn_target <= 0.0:
        return (None, False)
    v = max(0.5, float(val))
    tgt = float(dyn_target)
    w = max(tgt + 1.0, float(warn))
    if v <= tgt:
        base = 100.0 + 30.0 * math.log(max(1.0, tgt / v))
    elif v <= w:
        base = 60.0 + 40.0 * ((w - v) / max(1e-6, w - tgt))
    else:
        base = max(0.0, 60.0 * max(0.0, 1.0 - (v - w) / max(w, 15.0)))
    breakout = bool(hwm_low is not None and float(hwm_low) > 0.0 and v < float(hwm_low) / HWM_BREAKOUT_MARGIN and v <= tgt * 1.15)
    if breakout:
        base += 5.0
    return (round(base, 1), breakout)


def _status_from_score(score, staged=False):
    if staged:
        return "STAGED"
    if score is None:
        return "SOLID"
    if score >= 120.0:
        return "APEX"
    if score >= 100.0:
        return "OUTPERFORM"
    if score >= 80.0:
        return "SOLID"
    if score >= 60.0:
        return "WARN"
    return "ALARM"


def _core_margin_tier(margin_pct):
    if margin_pct is None:
        return "WARMUP"
    if margin_pct >= 50.0:
        return "ELITE"
    if margin_pct >= 30.0:
        return "TARGET"
    if margin_pct >= 0.0:
        return "BELOW"
    return "NEG"


def _compute_scouting_freshness(data_dir, repo_root, now):
    """Measure live whole-galaxy and rival/frontier freshness (minutes) across non-stronghold systems."""
    data_p = Path(data_dir)
    cpol = _read_json(Path(repo_root) / "game" / "census-policy.json", {})
    rival_set = set(str(x) for x in (cpol.get("rival_hub_systems") or []))

    all_sys = {}
    gtsv = Path(repo_root) / "game" / "map" / "galaxy.tsv"
    if gtsv.is_file():
        try:
            lines = [ln.rstrip("\n").split("\t") for ln in gtsv.read_text(encoding="utf-8").splitlines() if ln and not ln.startswith("#")]
            head = lines[0] if lines else []
            for row in lines[1:]:
                cell = dict(zip(head, row))
                sid = cell.get("id")
                if not sid:
                    continue
                if "stronghold" in str(cell.get("flags") or ""):
                    continue
                all_sys[sid] = {"empire": str(cell.get("empire") or "").strip()}
        except OSError:
            pass

    sdir = data_p / "scouting"
    all_ages = []
    rival_ages = []
    scanned_count = 0
    fresh_20m = 0
    fresh_60m = 0
    fresh_6h = 0

    target_systems = sorted(all_sys.keys()) if all_sys else ([p.stem for p in sorted(sdir.glob("*.json"))] if sdir.is_dir() else [])
    for sid in target_systems:
        sp = sdir / (sid + ".json")
        age_m = None
        if sp.is_file():
            try:
                j = json.loads(sp.read_text(encoding="utf-8"))
                rt = _parse_iso(j.get("read_at"))
                t_val = rt if rt is not None else sp.stat().st_mtime
                age_m = max(0.0, (now - t_val) / 60.0)
                scanned_count += 1
            except (OSError, ValueError):
                pass
        if age_m is None:
            age_m = 720.0
        all_ages.append(age_m)
        if age_m <= 20.0:
            fresh_20m += 1
        if age_m <= 60.0:
            fresh_60m += 1
        if age_m <= 360.0:
            fresh_6h += 1
        is_rival_or_frontier = (sid in rival_set) or (sid in all_sys and not all_sys[sid]["empire"])
        if is_rival_or_frontier:
            rival_ages.append(age_m)

    all_ages.sort()
    rival_ages.sort()
    tot = len(all_ages)
    med_all = all_ages[tot // 2] if tot else 0.0
    avg_all = sum(all_ages) / tot if tot else 0.0
    p90_all = all_ages[min(tot - 1, int(tot * 0.9))] if tot else 0.0
    med_riv = rival_ages[len(rival_ages) // 2] if rival_ages else med_all
    avg_riv = sum(rival_ages) / len(rival_ages) if rival_ages else avg_all

    return {
        "systems_total": tot,
        "systems_scanned": scanned_count,
        "median_min": round(med_all, 1),
        "avg_min": round(avg_all, 1),
        "p90_min": round(p90_all, 1),
        "fresh_20m": fresh_20m,
        "fresh_20m_pct": round(100.0 * fresh_20m / max(1, tot), 1),
        "fresh_60m": fresh_60m,
        "fresh_60m_pct": round(100.0 * fresh_60m / max(1, tot), 1),
        "fresh_6h": fresh_6h,
        "fresh_6h_pct": round(100.0 * fresh_6h / max(1, tot), 1),
        "rival_frontier_median_min": round(med_riv, 1),
        "rival_frontier_avg_min": round(avg_riv, 1),
        "rival_frontier_count": len(rival_ages),
    }


def compute_upgrade_gaps(conn, ships_list, repo_root, data_dir):
    """Dynamic max-possible Hull & Module upgrade gap engine scaling automatically from T1 -> T5."""
    repo_p = Path(repo_root)
    upol = _read_json(repo_p / "game" / "upgrade-policy.json", {})
    fpol = _read_json(repo_p / "game" / "fit-policy.json", {})
    max_auto_tier = int(upol.get("max_auto_tier") or 2)

    pil_map = {}
    hull_spec = {}
    ship_mods = {}
    ship_tier_db = {}
    if conn is not None:
        tbls = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()}
        if "ship_skills" in tbls:
            for p, lvl in conn.execute("SELECT pilot, level FROM ship_skills WHERE skill = 'piloting'").fetchall():
                pil_map[str(p)] = int(lvl or 0)
        if "hulls" in tbls:
            for hid, hnm, tr, ws, ds, us in conn.execute(
                "SELECT id, name, COALESCE(tier,0), COALESCE(weapon_slots,0), COALESCE(defense_slots,0), COALESCE(utility_slots,0) FROM hulls"
            ).fetchall():
                rec = {"id": str(hid or "").lower(), "tier": int(tr or 0), "weapon": int(ws or 0), "defense": int(ds or 0), "utility": int(us or 0)}
                if hid:
                    hull_spec[str(hid).lower()] = rec
                if hnm:
                    hull_spec[str(hnm).lower()] = rec
        if "ships" in tbls:
            for p, cls in conn.execute("SELECT pilot, class FROM ships").fetchall():
                hs = hull_spec.get(str(cls or "").lower())
                if hs:
                    ship_tier_db[str(p)] = hs["tier"]
        if "ship_modules" in tbls:
            for p, mid, mnm, slot, kind in conn.execute("SELECT pilot, module, name, slot, kind FROM ship_modules").fetchall():
                ship_mods.setdefault(str(p), []).append({
                    "id": str(mid or "").lower(),
                    "name": str(mnm or ""),
                    "slot": str(slot or kind or "").lower(),
                })

    div_cohorts = {}
    for dv, dcfg in (upol.get("divisions") or {}).items():
        if isinstance(dcfg, dict):
            div_cohorts[dv] = (bool(dcfg.get("enabled", True)), list(dcfg.get("cohorts") or []))

    def _match_cohort(ship):
        dv = str(ship.get("division") or "")
        wing = str(ship.get("wing") or "")
        div_en, cohs = div_cohorts.get(dv, (True, []))
        best = None
        for coh in cohs:
            wp = str(coh.get("wing_prefix") or "")
            wc = str(coh.get("wing_contains") or "")
            if wp and not wing.startswith(wp):
                continue
            if wc and wc.lower() not in wing.lower():
                continue
            if wp or wc:
                best = coh
                break
        if best is None and cohs:
            best = cohs[0]
        if best is None:
            return div_en, [{"tier": 1, "min_piloting": 0}]
        enabled = div_en and (best.get("enabled") is not False)
        return enabled, list(best.get("ladder") or [])

    import fit_net as _fn
    off_role_by_div = {
        dv: set(str(x).lower() for x in (lst or []))
        for dv, lst in (fpol.get("off_role_modules") or {}).items()
    }
    specs_cfg = fpol.get("specialties") or {}

    h_active_ships = h_staged_ships = 0
    h_poss_steps = h_fill_steps = h_ships_missing = 0
    h_auto_poss_steps = h_auto_fill_steps = h_auto_ships_missing = 0
    h_missing_by_tier = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    h_tier_dist = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    h_by_wing = {}

    m_active_ships = m_bursar_exempt = m_staged_ships = 0
    m_poss_slots = m_fill_slots = m_ships_missing_slots = 0
    m_poss_steps = m_fill_steps = m_ships_missing_tier = 0
    m_off_role_count = 0
    m_by_wing = {}

    for s in ships_list:
        pilot = str(s.get("name") or "")
        dv = str(s.get("division") or "")
        wing = str(s.get("wing") or "")
        wid = wing_id_of(wing, dv)
        cls = str(s.get("class") or "")
        hs = hull_spec.get(cls.lower()) or {"tier": ship_tier_db.get(pilot, 0), "weapon": 1, "defense": 1, "utility": 1}
        cur_tier = int(hs.get("tier", 0))
        h_tier_dist[min(5, max(0, cur_tier))] = h_tier_dist.get(min(5, max(0, cur_tier)), 0) + 1
        piloting = int(pil_map.get(pilot, s.get("piloting") or 0))

        enabled, ladder = _match_cohort(s)
        if not enabled:
            h_staged_ships += 1
        else:
            h_active_ships += 1
            unlocked_tiers = [int(r.get("tier") or 1) for r in ladder if piloting >= int(r.get("min_piloting") or 0)]
            max_poss = max(unlocked_tiers) if unlocked_tiers else 1
            auto_max = min(max_poss, max_auto_tier)
            filled = min(cur_tier, max_poss)
            auto_filled = min(cur_tier, auto_max)

            h_poss_steps += max_poss
            h_fill_steps += filled
            if cur_tier < max_poss:
                h_ships_missing += 1
                for kt in range(cur_tier + 1, max_poss + 1):
                    if kt in h_missing_by_tier:
                        h_missing_by_tier[kt] += 1
            h_auto_poss_steps += auto_max
            h_auto_fill_steps += auto_filled
            if cur_tier < auto_max:
                h_auto_ships_missing += 1

            hw = h_by_wing.setdefault(wid, {"ships": 0, "possible": 0, "filled": 0, "missing_ships": 0})
            hw["ships"] += 1
            hw["possible"] += max_poss
            hw["filled"] += filled
            if cur_tier < max_poss:
                hw["missing_ships"] += 1

        if wid in BURSAR_WING_IDS:
            m_bursar_exempt += 1
            continue
        if not enabled:
            m_staged_ships += 1
            continue

        m_active_ships += 1
        mods = ship_mods.get(pilot) or []
        spec_key = _fn.resolve_specialty(pilot, dv, mods, fpol, is_bursar=False, ship_class=cls)
        loadout = ((specs_cfg.get(dv) or {}).get("loadouts") or {}).get(spec_key) or {}
        off_set = off_role_by_div.get(dv, set())

        fitted_by_slot = {"weapon": [], "defense": [], "utility": []}
        has_off = False
        for m in mods:
            mid = m["id"]
            if mid in off_set:
                has_off = True
                continue
            sl = m["slot"]
            if sl in fitted_by_slot:
                fitted_by_slot[sl].append(_module_tier(mid, m["name"]))
        if has_off:
            m_off_role_count += 1

        ship_p_slots = ship_f_slots = 0
        ship_p_steps = ship_f_steps = 0
        for sl in ("weapon", "defense", "utility"):
            want_list = loadout.get(sl) or []
            if not want_list:
                continue
            cap_sl = int(hs.get(sl, 0))
            if cap_sl <= 0:
                continue
            bp_max_t = max((_module_tier(x) for x in want_list), default=2)
            target_t = min(bp_max_t, max(2, cur_tier + 1))
            got_tiers = sorted(fitted_by_slot[sl], reverse=True)[:cap_sl]
            ship_p_slots += cap_sl
            ship_f_slots += len(got_tiers)
            ship_p_steps += cap_sl * target_t
            ship_f_steps += sum(min(t, target_t) for t in got_tiers)

        m_poss_slots += ship_p_slots
        m_fill_slots += ship_f_slots
        m_poss_steps += ship_p_steps
        m_fill_steps += ship_f_steps
        if ship_f_slots < ship_p_slots:
            m_ships_missing_slots += 1
        if ship_f_steps < ship_p_steps:
            m_ships_missing_tier += 1

        mw = m_by_wing.setdefault(wid, {"ships": 0, "poss_slots": 0, "fill_slots": 0, "poss_steps": 0, "fill_steps": 0, "missing_ships": 0})
        mw["ships"] += 1
        mw["poss_slots"] += ship_p_slots
        mw["fill_slots"] += ship_f_slots
        mw["poss_steps"] += ship_p_steps
        mw["fill_steps"] += ship_f_steps
        if ship_f_steps < ship_p_steps:
            mw["missing_ships"] += 1

    h_missing_steps = max(0, h_poss_steps - h_fill_steps)
    h_pct = round(100.0 * h_fill_steps / max(1, h_poss_steps), 1)
    m_missing_slots = max(0, m_poss_slots - m_fill_slots)
    m_slot_pct = round(100.0 * m_fill_slots / max(1, m_poss_slots), 1)
    m_missing_steps = max(0, m_poss_steps - m_fill_steps)
    m_tier_pct = round(100.0 * m_fill_steps / max(1, m_poss_steps), 1)

    return {
        "hulls": {
            "active_ships": h_active_ships,
            "staged_ships": h_staged_ships,
            "max_auto_tier": max_auto_tier,
            "possible_steps": h_poss_steps,
            "filled_steps": h_fill_steps,
            "missing_steps": h_missing_steps,
            "ships_missing": h_ships_missing,
            "pct_done": h_pct,
            "auto_possible_steps": h_auto_poss_steps,
            "auto_filled_steps": h_auto_fill_steps,
            "auto_missing_steps": max(0, h_auto_poss_steps - h_auto_fill_steps),
            "auto_ships_missing": h_auto_ships_missing,
            "auto_pct_done": round(100.0 * h_auto_fill_steps / max(1, h_auto_poss_steps), 1),
            "missing_by_tier": {"T" + str(k): v for k, v in h_missing_by_tier.items() if v > 0},
            "tier_dist": {"T" + str(k): v for k, v in h_tier_dist.items() if v > 0},
            "by_wing": {
                w: {
                    "ships": v["ships"],
                    "missing_steps": max(0, v["possible"] - v["filled"]),
                    "missing_ships": v["missing_ships"],
                    "pct_done": round(100.0 * v["filled"] / max(1, v["possible"]), 1),
                }
                for w, v in h_by_wing.items()
            },
        },
        "modules": {
            "active_ships": m_active_ships,
            "bursar_exempt_ships": m_bursar_exempt,
            "staged_ships": m_staged_ships,
            "possible_slots": m_poss_slots,
            "filled_slots": m_fill_slots,
            "missing_slots": m_missing_slots,
            "slot_pct_done": m_slot_pct,
            "ships_missing_slots": m_ships_missing_slots,
            "possible_steps": m_poss_steps,
            "filled_steps": m_fill_steps,
            "missing_steps": m_missing_steps,
            "tier_pct_done": m_tier_pct,
            "ships_missing_tier": m_ships_missing_tier,
            "off_role_ships": m_off_role_count,
            "by_wing": {
                w: {
                    "ships": v["ships"],
                    "missing_slots": max(0, v["poss_slots"] - v["fill_slots"]),
                    "slot_pct": round(100.0 * v["fill_slots"] / max(1, v["poss_slots"]), 1),
                    "tier_pct": round(100.0 * v["fill_steps"] / max(1, v["poss_steps"]), 1),
                    "missing_ships": v["missing_ships"],
                }
                for w, v in m_by_wing.items()
            },
        },
    }


def _compute_bunker_and_supply_sla(conn, data_dir):
    """Compute live Outpost Bunker fuel fill % (target 50,000/bunker) and P1/P2 supply-chain SLA %."""
    bunkers = []
    supply_covs = []
    if conn is not None:
        tbls = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()}
        if "bases" in tbls and "faction_facilities" in tbls and "faction_storage" in tbls:
            b_rows = conn.execute("""
                SELECT DISTINCT b.base, b.name, b.system
                FROM bases b
                JOIN faction_facilities ff ON ff.base = b.base
                WHERE LOWER(COALESCE(ff.type, '')) LIKE '%fuel_bunker%'
                  AND LOWER(COALESCE(ff.status, 'active')) = 'active'
            """).fetchall()
            fuel_map = {
                str(r[0]): int(r[1] or 0)
                for r in conn.execute("SELECT base, units FROM faction_storage WHERE item = 'fuel'").fetchall()
            }
            for bid, bname, bsys in b_rows:
                u = fuel_map.get(str(bid), 0)
                tgt = 50000
                pct = round(min(100.0, 100.0 * u / float(tgt)), 1)
                bunkers.append({"base": str(bid), "name": str(bname or bsys), "system": str(bsys), "fuel": u, "target": tgt, "pct": pct})
        if "need_status" in tbls:
            for prio, cov in conn.execute("SELECT priority, covered FROM need_status WHERE COALESCE(stands, 0) = 0").fetchall():
                if str(prio or "").strip().upper() in ("1", "2", "P1", "P2") and cov is not None:
                    supply_covs.append(min(100.0, max(0.0, float(cov))))

    bunker_avg = round(sum(b["pct"] for b in bunkers) / len(bunkers), 1) if bunkers else 100.0
    supply_avg = round(sum(supply_covs) / len(supply_covs), 1) if supply_covs else 100.0
    low_bunkers = [b["base"] for b in bunkers if b["pct"] < 85.0]
    return {
        "bunkers": bunkers,
        "bunker_avg_pct": bunker_avg,
        "low_bunker_bases": low_bunkers,
        "supply_sla_pct": supply_avg,
        "p1_p2_needs_count": len(supply_covs),
    }


def _load_fair_unit_prices(conn, data_dir):
    """Load net-external fair bid prices from price_oracle.json with conservative catalog fallback."""
    prices = {}
    op = Path(data_dir) / "fleet" / "price_oracle.json"
    od = _read_json(op, {})
    items_o = od.get("items") if isinstance(od, dict) and isinstance(od.get("items"), dict) else (od if isinstance(od, dict) else {})
    for iid, rec in items_o.items():
        if isinstance(rec, dict):
            p = rec.get("fair") or rec.get("vwm") or rec.get("twap") or rec.get("bid") or 0
            if isinstance(p, (int, float)) and p > 0:
                prices[str(iid)] = float(p)
        elif isinstance(rec, (int, float)) and rec > 0:
            prices[str(iid)] = float(rec)
    if conn is not None:
        try:
            for iid, bval in conn.execute("SELECT id, base_value FROM items WHERE base_value > 0").fetchall():
                if str(iid) not in prices:
                    prices[str(iid)] = float(bval) * 0.5
        except sqlite3.Error:
            pass
    return prices


def _compute_window_wing_kpis(conn, ships_list, pilot_wing, pilot_div, acc_win, hours, now, data_dir, repo_root, freshness, infra, upgrade_gaps, bursar_occ, host_running_count, hwm_doc=None, hwm_updates=None):
    """Compute complete fleet-wide + 17-wing KPI snapshot for one time window (`1h`, `6h`, or `24h`)."""
    cut = int(now - hours * 3600.0)
    span_h = max(0.25, float((acc_win or {}).get("span_hours") or hours))
    prices = _load_fair_unit_prices(conn, data_dir)

    upg_held = set()
    uq_raw = _read_json(Path(data_dir) / "fleet" / "upgrade_queue.json", {})
    uq_rows = uq_raw.get("queue") if isinstance(uq_raw, dict) else (uq_raw if isinstance(uq_raw, list) else [])
    for qr in (uq_rows or []):
        if isinstance(qr, dict) and str(qr.get("state") or "") in ("queued", "funding", "funded", "building"):
            if qr.get("pilot"):
                upg_held.add(str(qr["pilot"]))

    wing_live = {
        w[0]: {"total": 0, "working": 0, "goal": 0, "upgrading": 0, "park": 0, "idle": 0, "bursar_docked": 0}
        for w in WING_SPECS
    }
    fleet_working = fleet_upgrading = fleet_idle = fleet_park = 0
    for s in ships_list:
        p = str(s.get("name") or "")
        wid = pilot_wing.get(p) or wing_id_of(s.get("wing"), s.get("division"))
        st = wing_live.setdefault(wid, {"total": 0, "working": 0, "goal": 0, "upgrading": 0, "park": 0, "idle": 0, "bursar_docked": 0})
        st["total"] += 1
        ord_s = str(s.get("order") or "").strip()
        act_k = str((s.get("activity") or {}).get("kind") or "")
        if ord_s:
            if ord_s.startswith("park"):
                st["park"] += 1
                fleet_park += 1
            else:
                st["working"] += 1
                fleet_working += 1
                if ord_s.startswith("bursar") and s.get("docked"):
                    st["bursar_docked"] += 1
        elif act_k and act_k != "idle":
            st["goal"] += 1
            fleet_working += 1
        elif p in upg_held:
            st["upgrading"] += 1
            fleet_upgrading += 1
        else:
            st["idle"] += 1
            fleet_idle += 1

    w_runs = {
        w[0]: {
            "runs": 0, "ok_runs": 0, "mine_runs": 0, "mine_ok": 0, "minutes": 0.0, "flight_mins": 0.0,
            "ore_units": 0, "ore_val": 0.0, "kills": 0, "loot_val": 0.0,
            "craft_units": 0, "craft_val": 0.0, "craft_xp": 0.0, "scans": 0,
            "rev_cash": 0.0, "neg_cash": 0.0, "losses": 0, "bursar_mins": 0.0,
            "arb_ok_n": 0, "arb_listed_n": 0, "arb_listed_cr": 0.0, "inv_cost_cr": 0.0,
            "upkeep_buy_cr": 0.0, "upkeep_fair_cr": 0.0, "craft_spend_cr": 0.0,
        }
        for w in WING_SPECS
    }

    if conn is not None:
        tbls = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()}
        if "runs" in tbls:
            for pilot, kind, mins, cr, one_t, raw_row in conn.execute(
                "SELECT pilot, kind, COALESCE(minutes, 0), COALESCE(credits, 0), COALESCE(one_time, 0), row FROM runs WHERE t >= ?",
                (cut,),
            ).fetchall():
                wid = pilot_wing.get(str(pilot))
                if not wid or wid not in w_runs:
                    continue
                wr = w_runs[wid]
                wr["runs"] += 1
                m_f = float(mins or 0.0)
                wr["minutes"] += m_f
                rj = {}
                if raw_row:
                    try:
                        rj = json.loads(raw_row)
                    except ValueError:
                        rj = {}
                k = str(kind or "")
                c_val = float(cr or 0.0)
                o_val = float(one_t or 0.0)
                op_cr = c_val if o_val == 0 else min(0.0, c_val)
                if op_cr > 0:
                    wr["rev_cash"] += op_cr
                elif op_cr < 0:
                    wr["neg_cash"] += abs(op_cr)

                if k == "bursar":
                    wr["bursar_mins"] += m_f
                    wr["ok_runs"] += 1
                else:
                    wr["flight_mins"] += m_f

                if k == "mine":
                    ore_u = int(rj.get("ore") or 0)
                    res_id = str(rj.get("resource") or "")
                    notes_j = " ".join(str(x) for x in (rj.get("notes") or [])).lower()
                    host_stop = ("host is ending" in notes_j) or ("stop file" in notes_j)
                    no_belt_tick = (ore_u == 0 and m_f < 1.0 and "no belt" in notes_j)
                    if ore_u > 0:
                        wr["mine_runs"] += 1
                        wr["ok_runs"] += 1
                        wr["mine_ok"] += 1
                        wr["ore_units"] += ore_u
                        wr["ore_val"] += float(ore_u) * float(prices.get(res_id, 5.0))
                    elif (not host_stop) and (not no_belt_tick):
                        wr["mine_runs"] += 1
                elif k == "hunt":
                    kl = int(rj.get("kills") or 0)
                    wr["kills"] += kl
                    if kl > 0:
                        wr["ok_runs"] += 1
                    goods = rj.get("goods")
                    if isinstance(goods, dict):
                        for gid, gq in goods.items():
                            wr["loot_val"] += float(gq or 0) * float(prices.get(str(gid), 10.0))
                    if int(rj.get("lost") or 0) > 0:
                        wr["losses"] += int(rj.get("lost") or 0)
                elif k == "census":
                    if int(rj.get("places") or 0) > 0 or not rj.get("notes"):
                        wr["scans"] += 1
                        wr["ok_runs"] += 1
                elif k in ("craft_net", "bursar"):
                    if op_cr < 0:
                        wr["craft_spend_cr"] += abs(op_cr)
                    for nt in (rj.get("notes") or []):
                        for cm in _CRAFT_RE.finditer(str(nt)):
                            cq = int(cm.group(1))
                            cid = cm.group(2).lower()
                            wr["craft_units"] += cq
                            wr["craft_val"] += float(cq) * float(prices.get(cid, 15.0))
                            wr["ok_runs"] += 1
                elif k == "haul":
                    notes_s = " ".join(str(x) for x in (rj.get("notes") or []))
                    _ic = float(rj.get("inventory_cost") or 0.0)
                    if _ic > 0:
                        wr["inv_cost_cr"] += _ic
                    if "arb listed" in notes_s:
                        wr["arb_listed_n"] += 1
                        wr["arb_listed_cr"] += abs(op_cr) if op_cr < 0 else _ic
                    elif "arb " in notes_s and op_cr > 0:
                        wr["arb_ok_n"] += 1
                    if "hub_upkeep" in notes_s and op_cr < 0:
                        wr["upkeep_buy_cr"] += abs(op_cr)
                        _m_u = re.search(r"hub_upkeep\s+(\d+)\s+([a-z0-9_]+)", notes_s)
                        if _m_u:
                            wr["upkeep_fair_cr"] += int(_m_u.group(1)) * float(prices.get(_m_u.group(2), 50.0))
                    if "docked watch" not in notes_s and "no eligible" not in notes_s:
                        wr["ok_runs"] += 1

        if "stats_pilot_hour" in tbls:
            for pilot, skey, gain in conn.execute(
                "SELECT pilot, key, SUM(COALESCE(gain, 0)) FROM stats_pilot_hour WHERE key IN ('ships_lost', 'crafting', 'refining') AND hour >= ? GROUP BY pilot, key",
                (cut,),
            ).fetchall():
                wid = pilot_wing.get(str(pilot))
                if not wid or wid not in w_runs or float(gain or 0) <= 0:
                    continue
                if skey == "ships_lost":
                    w_runs[wid]["losses"] = max(w_runs[wid]["losses"], int(round(float(gain))))
                else:
                    w_runs[wid]["craft_xp"] += float(gain)

    # Sum outbound handover.jsonl value per wing over this window (not overwriting -- summing cleanly!)
    ho_val_by_wing = {}
    ho_path = Path(data_dir) / "stock" / "handover.jsonl"
    if ho_path.is_file():
        try:
            for ln in ho_path.read_text(encoding="utf-8", errors="replace").splitlines()[-12000:]:
                if not ln.strip():
                    continue
                try:
                    rec = json.loads(ln)
                except ValueError:
                    continue
                at_t = float(rec.get("at") or 0)
                if at_t < cut:
                    continue
                frm = str(rec.get("from") or "")
                wid = pilot_wing.get(frm)
                if not wid or wid not in w_runs:
                    continue
                items = rec.get("items") or {}
                if isinstance(items, dict):
                    val = sum(float(q or 0) * float(prices.get(str(iid), 8.0)) for iid, q in items.items())
                    ho_val_by_wing[wid] = ho_val_by_wing.get(wid, 0.0) + val
        except OSError:
            pass
    for wid, hval in ho_val_by_wing.items():
        if wid in ("1A-1C", "2A-2B"):
            w_runs[wid]["loot_val"] = max(w_runs[wid]["loot_val"], hval)
        elif wid in ("3A", "3B", "3C", "3D", "3E"):
            w_runs[wid]["ore_val"] = max(w_runs[wid]["ore_val"], hval)

    by_div_acc = (acc_win or {}).get("by_division") or {}
    div_wing_ids = {}
    for wid, _nm, dv, _pil, _pre, _rc in WING_SPECS:
        div_wing_ids.setdefault(dv, []).append(wid)

    wing_fuel_h = {}
    for dv, wids in div_wing_ids.items():
        div_fuel = float((by_div_acc.get(dv) or {}).get("fuel_cr_h") or 0.0)
        weights = {}
        for wid in wids:
            wr = w_runs[wid]
            if wid in BURSAR_WING_IDS:
                wt = max(0.0, wr["flight_mins"] * 0.25)
            else:
                wt = max(0.1, wr["flight_mins"] + (wr["neg_cash"] / 80.0) + wing_live[wid]["working"] * 1.5)
            weights[wid] = wt
        tot_w = sum(weights.values()) or 1.0
        for wid in wids:
            wing_fuel_h[wid] = div_fuel * (weights[wid] / tot_w)

    rb = (acc_win or {}).get("revenue_breakdown") or {}
    ob = (acc_win or {}).get("opex_breakdown") or {}
    st_ops = (acc_win or {}).get("station_ops") or {}
    realized_rev_h = float((acc_win or {}).get("raw_income_h") or 0.0) + float((acc_win or {}).get("passive_inflows_h") or 0.0) + float(st_ops.get("station_revenue_h") or 0.0)
    paid_fuel_h = float(ob.get("fuel_h") or sum(float(v.get("fuel_cr_h") or 0) for v in by_div_acc.values() if isinstance(v, dict)))
    core_ebit_h = float((acc_win or {}).get("recurring_cash_h") or 0.0) + float((acc_win or {}).get("treasury_own_h") or 0.0)
    rev_per_fuel = round(realized_rev_h / paid_fuel_h, 2) if paid_fuel_h >= 100.0 else None
    ebit_per_fuel = round(core_ebit_h / paid_fuel_h, 2) if paid_fuel_h >= 100.0 else None
    core_margin_pct = round(100.0 * core_ebit_h / realized_rev_h, 1) if realized_rev_h >= 100.0 else None
    core_margin_tier = _core_margin_tier(core_margin_pct)

    tot_ships = max(1, len(ships_list))
    fleet_idle_pct = round(100.0 * fleet_idle / tot_ships, 1)
    fleet_working_pct = round(100.0 * (fleet_working + fleet_upgrading) / tot_ships, 1)

    wings_out = []
    upol = _read_json(Path(repo_root) / "game" / "upgrade-policy.json", {})
    staged_6b = False
    for coh in ((upol.get("divisions") or {}).get("Logistics") or {}).get("cohorts") or []:
        if str(coh.get("wing_prefix") or "").startswith("6B.") and coh.get("enabled") is False:
            staged_6b = True

    spol = _read_json(Path(repo_root) / "game" / "salvage-policy.json", {})
    salvage_enabled = bool(spol.get("enabled", False))

    mining_seg = (acc_win or {}).get("mining_segments") or {}
    bursar_rev_pool = float(rb.get("bursar_active_h") or rb.get("trade_sales_h") or 0.0) + float(rb.get("passive_escrow_h") or 0.0)
    mobile_trade_pool = float(rb.get("mobile_trade_h") or 0.0)
    log_core_pool = float(rb.get("logistics_core_h") or rb.get("freight_sales_h") or 0.0)
    pax_rev_pool = float(rb.get("passenger_liners_h") or 0.0)
    bursar_4c_ships = max(1, wing_live["4C"]["total"])
    bursar_5a_ships = max(1, wing_live["5A"]["total"])
    bursar_tot_ships = float(bursar_4c_ships + bursar_5a_ships)

    hwm_wings = (hwm_doc or {}).get("wings") if isinstance((hwm_doc or {}).get("wings"), dict) else {}
    hulls_bw = ((upgrade_gaps or {}).get("hulls") or {}).get("by_wing") or {}

    def _cap_mult(wid_k, ship_n):
        base_n = float(WING_BASE_SHIPS.get(wid_k, max(1, ship_n)))
        n_scale = max(0.45, float(max(1, ship_n)) / base_n)
        hg = hulls_bw.get(wid_k) or {}
        filled = float(hg.get("filled_steps") or 0.0)
        avg_tier = filled / float(max(1, ship_n))
        return round(n_scale * (1.0 + 0.55 * avg_tier), 2)

    def _hwm_get(wid_k, mkey):
        rec = hwm_wings.get(wid_k)
        return rec.get(mkey) if isinstance(rec, dict) else None

    def _hwm_mark(wid_k, mkey, val, lower=False):
        if hwm_updates is None or val is None or val <= 0.0:
            return
        wmap = hwm_updates.setdefault(wid_k, {})
        prev = _hwm_get(wid_k, mkey)
        wmap[mkey] = _ratchet_hwm_low(prev, val) if lower else _ratchet_hwm_high(prev, val)

    def _fmt_frontier(par_txt, hwm_val, breakout, suffix=""):
        if breakout:
            return "par %s | NEW PEAK!" % par_txt
        if hwm_val is not None and float(hwm_val) > 0:
            if suffix == "m":
                return "par %s | best %.1fm" % (par_txt, float(hwm_val))
            if suffix == "x":
                return "par %s | best %.2fx" % (par_txt, float(hwm_val))
            if suffix == "/h":
                return "par %s | best %.0f/h" % (par_txt, float(hwm_val))
            return "par %s | best %s" % (par_txt, format(int(round(float(hwm_val))), ","))
        return "par %s" % par_txt

    for wid, wname, dv, pillar, _pre, rc_label in WING_SPECS:
        wl = wing_live[wid]
        wr = w_runs[wid]
        fuel_h = round(wing_fuel_h.get(wid, 0.0), 1)
        idle_pct = round(100.0 * wl["idle"] / max(1, wl["total"]), 1)
        work_pct = round(100.0 * (wl["working"] + wl["goal"]) / max(1, wl["total"]), 1)
        s_idle = _score_band(idle_pct, good=3.0, warn=10.0, higher_better=False)
        staged = (wid == "6B" and staged_6b)
        cm = _cap_mult(wid, wl["total"])
        idle_sub = ("%d/%d active | %d upgrading" % (wl["working"] + wl["goal"], wl["total"], wl["upgrading"])) if wl["upgrading"] else ("%d/%d working" % (wl["working"] + wl["goal"], wl["total"]))

        kpis = []
        primary_rof = None
        scores = [(s_idle, 0.20)]

        if wid in ("1A-1C", "2A-2B"):
            mil_acc = by_div_acc.get("Military") or {}
            mil_gross_i2 = max(0.0, float(mil_acc.get("accrual_op_h") or 0.0) + float(mil_acc.get("fuel_cr_h") or 0.0))
            w_def = max(1.0, w_runs["1A-1C"]["loot_val"] + w_runs["1A-1C"]["kills"] * 120.0)
            w_hnt = max(1.0, w_runs["2A-2B"]["loot_val"] + w_runs["2A-2B"]["kills"] * 120.0)
            share_m = (w_def if wid == "1A-1C" else w_hnt) / (w_def + w_hnt)
            extracted_loot_h = wr["loot_val"] / span_h
            div_combat_cash = float(rb.get("defense_h" if wid == "1A-1C" else "hunters_h") or 0.0)
            loot_h = round(max(mil_gross_i2 * share_m, extracted_loot_h, wr["rev_cash"] / span_h, div_combat_cash), 0)
            rof = round(loot_h / fuel_h, 2) if fuel_h >= 50.0 else None
            primary_rof = rof
            kills_h = round(wr["kills"] / span_h, 1)
            loss_h = round(wr["losses"] / span_h, 2)
            par_loot = round((55000.0 if wid == "2A-2B" else 35000.0) * cm, 0)
            par_rof = 2.5
            hwm_loot = _hwm_get(wid, "loot_h")
            hwm_rof = _hwm_get(wid, "rof")
            s_out, br_out = _score_open_ended(loot_h, par_loot, warn_ratio=0.45, hwm=hwm_loot)
            s_rof, br_rof = _score_open_ended(rof, par_rof, warn_ratio=0.45, hwm=hwm_rof) if rof is not None else (75.0, False)
            s_loss = _score_band(loss_h, good=0.0, warn=0.25, higher_better=False)
            _hwm_mark(wid, "loot_h", loot_h)
            if rof is not None:
                _hwm_mark(wid, "rof", rof)
            scores.extend([(s_rof, 0.35), (s_out, 0.30), (s_loss, 0.15)])
            kpis = [
                {"k": "Loot / h", "v": "+%s cr/h" % format(int(loot_h), ","), "sub": "%.1f kills/h | %s" % (kills_h, _fmt_frontier(format(int(par_loot), ","), hwm_loot, br_out)), "score": round(s_out), "breakout": br_out},
                {"k": "Loot / Fuel", "v": ("%.2fx" % rof) if rof is not None else "--", "sub": "%s fuel | %s" % (format(int(fuel_h), ","), _fmt_frontier("%.1fx" % par_rof, hwm_rof, br_rof, "x")), "score": round(s_rof), "breakout": br_rof},
                {"k": "Ships Lost / h", "v": "%.2f/h" % loss_h, "sub": "%d in %dh" % (wr["losses"], int(round(hours))), "score": round(s_loss)},
                {"k": "Idle Rate", "v": "%.1f%%" % idle_pct, "sub": idle_sub, "score": round(s_idle)},
            ]

        elif wid in ("3A", "3B", "3C", "3D", "3E"):
            ms = mining_seg.get(wid) or {}
            units_h = round(max(wr["ore_units"] / span_h, float(ms.get("units_h") or 0.0)), 0)
            if ms and float(ms.get("tx_nrv_h") or 0.0) > 0:
                val_h = round(float(ms.get("tx_nrv_h") or 0.0), 0)
            else:
                mine_acc = by_div_acc.get("Mining") or {}
                mine_cap = max(0.0, float(mine_acc.get("tx_out_h") or 0.0) + max(0.0, float(mine_acc.get("inv_accrual_h") or 0.0)))
                raw_sum = sum(w_runs[x]["ore_val"] / span_h for x in ("3A", "3B", "3C", "3D", "3E")) or 1.0
                scale = min(1.0, mine_cap / raw_sum) if mine_cap > 0 else 1.0
                val_h = round((wr["ore_val"] / span_h) * scale, 0)
            rof = round(val_h / fuel_h, 2) if fuel_h >= 50.0 else None
            primary_rof = rof
            yield_eff = round(100.0 * wr["mine_ok"] / max(1, wr["mine_runs"]), 1) if wr["mine_runs"] > 0 else 100.0
            _mine_base_par = {"3A": 65000.0, "3B": 30000.0, "3C": 45000.0, "3D": 110000.0, "3E": 75000.0}.get(wid, 50000.0)
            par_val = round(_mine_base_par * cm, 0)
            par_rof = 3.5
            hwm_val = _hwm_get(wid, "val_h")
            hwm_rof = _hwm_get(wid, "rof")
            s_val, br_val = _score_open_ended(val_h, par_val, warn_ratio=0.45, hwm=hwm_val)
            s_rof, br_rof = _score_open_ended(rof, par_rof, warn_ratio=0.45, hwm=hwm_rof) if rof is not None else (80.0, False)
            s_eff = _score_band(yield_eff, good=82.0, warn=55.0, higher_better=True)
            _hwm_mark(wid, "val_h", val_h)
            if rof is not None:
                _hwm_mark(wid, "rof", rof)
            scores.extend([(s_rof, 0.35), (s_val, 0.30), (s_eff, 0.15)])
            kpis = [
                {"k": "Value / h", "v": "+%s cr/h" % format(int(val_h), ","), "sub": "%s u/h | %s" % (format(int(units_h), ","), _fmt_frontier(format(int(par_val), ","), hwm_val, br_val)), "score": round(s_val), "breakout": br_val},
                {"k": "Value / Fuel", "v": ("%.2fx" % rof) if rof is not None else "--", "sub": "%s fuel | %s" % (format(int(fuel_h), ","), _fmt_frontier("%.1fx" % par_rof, hwm_rof, br_rof, "x")), "score": round(s_rof), "breakout": br_rof},
                {"k": "Mine Yield Rate", "v": "%.0f%%" % yield_eff, "sub": "%d/%d mine runs yielded" % (wr["mine_ok"], wr["mine_runs"]), "score": round(s_eff)},
                {"k": "Idle Rate", "v": "%.1f%%" % idle_pct, "sub": idle_sub, "score": round(s_idle)},
            ]

        elif wid in ("4A", "4B"):
            share = float(wl["total"]) / float(max(1, wing_live["4A"]["total"] + wing_live["4B"]["total"]))
            rev_h = round(max(wr["rev_cash"] / span_h, mobile_trade_pool * share), 0)
            rof = round(rev_h / fuel_h, 2) if fuel_h >= 50.0 else None
            primary_rof = rof
            runs_h = round(wr["ok_runs"] / span_h, 1)
            par_rev = round(50000.0 * cm, 0)
            par_rof = 3.0
            hwm_rev = _hwm_get(wid, "rev_h")
            hwm_rof = _hwm_get(wid, "rof")
            s_rev, br_rev = _score_open_ended(rev_h, par_rev, warn_ratio=0.45, hwm=hwm_rev)
            s_rof, br_rof = _score_open_ended(rof, par_rof, warn_ratio=0.45, hwm=hwm_rof) if rof is not None else (80.0, False)
            _hwm_mark(wid, "rev_h", rev_h)
            if rof is not None:
                _hwm_mark(wid, "rof", rof)
            arb_loss_h = wr["arb_listed_cr"] / span_h
            tca_denom = max(1.0, rev_h + arb_loss_h)
            fill_qual_pct = round(100.0 * rev_h / tca_denom, 1) if (rev_h + arb_loss_h) > 0 else 100.0
            net_margin_pct = round(100.0 * (rev_h - (wr["neg_cash"] / span_h)) / max(1.0, rev_h), 1) if rev_h >= 100.0 else 0.0
            s_tca = _score_band(fill_qual_pct, good=92.0, warn=70.0, higher_better=True)
            scores.extend([(s_rof, 0.30), (s_rev, 0.30), (s_tca, 0.20)])
            kpis = [
                {"k": "Revenue / h", "v": "+%s cr/h" % format(int(rev_h), ","), "sub": "%.1f trips/h | %s" % (runs_h, _fmt_frontier(format(int(par_rev), ","), hwm_rev, br_rev)), "score": round(s_rev), "breakout": br_rev},
                {"k": "Rev / Fuel", "v": ("%.2fx" % rof) if rof is not None else "--", "sub": "%s fuel | %s" % (format(int(fuel_h), ","), _fmt_frontier("%.1fx" % par_rof, hwm_rof, br_rof, "x")), "score": round(s_rof), "breakout": br_rof},
                {"k": "Exec Fill Quality (TCA)", "v": "%.1f%%" % fill_qual_pct, "sub": "%d listed (-%s/h) | net %.0f%%" % (wr["arb_listed_n"], format(int(arb_loss_h), ","), net_margin_pct), "score": round(s_tca)},
                {"k": "Idle Rate", "v": "%.1f%%" % idle_pct, "sub": idle_sub, "score": round(s_idle)},
            ]

        elif wid == "4C":
            desk_up = round(100.0 * wl["bursar_docked"] / max(1, wl["total"]), 1)
            st_target = 55
            st_pct = round(min(100.0, 100.0 * bursar_occ / float(st_target)), 1)
            sales_h = round(max(wr["rev_cash"] / span_h, bursar_rev_pool * (bursar_4c_ships / bursar_tot_ships)), 0)
            par_sl = round(75000.0 * cm, 0)
            hwm_sl = _hwm_get(wid, "sales_h")
            s_up = _score_band(desk_up, good=90.0, warn=70.0, higher_better=True)
            s_st = _score_band(st_pct, good=88.0, warn=65.0, higher_better=True)
            s_sl, br_sl = _score_open_ended(sales_h, par_sl, warn_ratio=0.45, hwm=hwm_sl)
            _hwm_mark(wid, "sales_h", sales_h)
            buy_drag_h = wr["neg_cash"] / span_h
            cash_cap_pct = round(100.0 * sales_h / max(1.0, sales_h + buy_drag_h), 1) if (sales_h + buy_drag_h) > 0 else 100.0
            hwm_cc = _hwm_get(wid, "cash_cap_pct")
            s_cc, br_cc = _score_open_ended(cash_cap_pct, 65.0, warn_ratio=0.50, hwm=hwm_cc)
            _hwm_mark(wid, "cash_cap_pct", cash_cap_pct)
            scores.extend([(s_up, 0.20), (s_st, 0.15), (s_sl, 0.30), (s_cc, 0.15)])
            kpis = [
                {"k": "Sales / h (0-fuel)", "v": "+%s cr/h" % format(int(sales_h), ","), "sub": "0 fuel | %s" % _fmt_frontier(format(int(par_sl), ","), hwm_sl, br_sl), "score": round(s_sl), "breakout": br_sl},
                {"k": "Cash Capture (TCA)", "v": "%.1f%%" % cash_cap_pct, "sub": "buy/fee -%s/h | %s" % (format(int(buy_drag_h), ","), _fmt_frontier("65%", hwm_cc, br_cc)), "score": round(s_cc), "breakout": br_cc},
                {"k": "Stations Covered", "v": "%d / %d" % (bursar_occ, st_target), "sub": "%d/%d desks live (%.0f%%)" % (wl["bursar_docked"], wl["total"], desk_up), "score": round(min(s_st, s_up))},
                {"k": "Idle Rate", "v": "%.1f%%" % idle_pct, "sub": idle_sub, "score": round(s_idle)},
            ]

        elif wid == "5A":
            craft_val_h = round(wr["craft_val"] / span_h, 0)
            crafts_h = round(wr["craft_units"] / span_h, 1)
            sales_h = round(max(wr["rev_cash"] / span_h, bursar_rev_pool * (bursar_5a_ships / bursar_tot_ships)), 0)
            desk_up = round(100.0 * wl["bursar_docked"] / max(1, wl["total"]), 1)
            comb_h = craft_val_h + sales_h
            par_comb = round(80000.0 * cm, 0)
            hwm_comb = _hwm_get(wid, "comb_h")
            s_up = _score_band(desk_up, good=88.0, warn=65.0, higher_better=True)
            s_cr, br_cr = _score_open_ended(comb_h, par_comb, warn_ratio=0.45, hwm=hwm_comb)
            _hwm_mark(wid, "comb_h", comb_h)
            spend_5a_h = max(100.0, (wr["craft_spend_cr"] / span_h) + fuel_h)
            va_ratio_5a = round(comb_h / spend_5a_h, 2)
            hwm_va5a = _hwm_get(wid, "va_ratio")
            s_va5a, br_va5a = _score_open_ended(va_ratio_5a, 2.5, warn_ratio=0.45, hwm=hwm_va5a)
            _hwm_mark(wid, "va_ratio", va_ratio_5a)
            scores.extend([(s_up, 0.20), (s_cr, 0.35), (s_va5a, 0.25)])
            kpis = [
                {"k": "Crafted Value / h", "v": ("+%s cr/h" % format(int(craft_val_h), ",")) if craft_val_h > 0 else ("%.0f XP/h" % (wr["craft_xp"] / span_h)), "sub": "%.0f items/h | %s" % (crafts_h, _fmt_frontier(format(int(par_comb), ","), hwm_comb, br_cr)), "score": round(s_cr), "breakout": br_cr},
                {"k": "Value / Spend (TCA)", "v": "%.2fx" % va_ratio_5a, "sub": "sales +%s | spend -%s/h" % (format(int(sales_h), ","), format(int(spend_5a_h), ",")), "score": round(s_va5a), "breakout": br_va5a},
                {"k": "Desk Uptime", "v": "%.0f%%" % desk_up, "sub": "%d/%d docked live" % (wl["bursar_docked"], wl["total"]), "score": round(s_up)},
                {"k": "Idle Rate", "v": "%.1f%%" % idle_pct, "sub": idle_sub, "score": round(s_idle)},
            ]

        elif wid == "5B":
            craft_val_h = round(wr["craft_val"] / span_h, 0)
            crafts_h = round(wr["craft_units"] / span_h, 1)
            tot_val_h = round(max(craft_val_h, wr["rev_cash"] / span_h), 0)
            rof = round(tot_val_h / fuel_h, 2) if fuel_h >= 50.0 else None
            primary_rof = rof
            par_cr = round(30000.0 * cm, 0)
            par_rof = 3.0
            hwm_cr = _hwm_get(wid, "tot_val_h")
            hwm_rof = _hwm_get(wid, "rof")
            s_cr, br_cr = _score_open_ended(tot_val_h, par_cr, warn_ratio=0.45, hwm=hwm_cr)
            s_rof, br_rof = _score_open_ended(rof, par_rof, warn_ratio=0.45, hwm=hwm_rof) if rof is not None else (80.0, False)
            _hwm_mark(wid, "tot_val_h", tot_val_h)
            if rof is not None:
                _hwm_mark(wid, "rof", rof)
            scores.extend([(s_cr, 0.45), (s_rof, 0.35)])
            kpis = [
                {"k": "Crafted Value / h", "v": ("+%s cr/h" % format(int(craft_val_h), ",")) if craft_val_h > 0 else ("%.0f XP/h" % (wr["craft_xp"] / span_h)), "sub": "%.0f items/h | %s" % (crafts_h, _fmt_frontier(format(int(par_cr), ","), hwm_cr, br_cr)), "score": round(s_cr), "breakout": br_cr},
                {"k": "Value / Fuel", "v": ("%.2fx" % rof) if rof is not None else "--", "sub": "%s fuel | %s" % (format(int(fuel_h), ","), _fmt_frontier("%.1fx" % par_rof, hwm_rof, br_rof, "x")), "score": round(s_rof), "breakout": br_rof},
                {"k": "Workshop Runs / h", "v": "%.1f/h" % (wr["ok_runs"] / span_h), "sub": "%d runs in %dh" % (wr["runs"], int(round(hours))), "score": round(s_cr)},
                {"k": "Idle Rate", "v": "%.1f%%" % idle_pct, "sub": idle_sub, "score": round(s_idle)},
            ]

        elif wid == "6A":
            sla = float(infra["supply_sla_pct"])
            rev_h = round(max(wr["rev_cash"] / span_h, log_core_pool * 0.8), 0)
            rof = round(rev_h / fuel_h, 2) if fuel_h >= 50.0 else None
            primary_rof = rof
            runs_h = round(wr["ok_runs"] / span_h, 1)
            par_rof = 2.2
            hwm_rof = _hwm_get(wid, "rof")
            s_sla = _score_band(sla, good=88.0, warn=65.0, higher_better=True)
            s_rof, br_rof = _score_open_ended(rof, par_rof, warn_ratio=0.45, hwm=hwm_rof) if rof is not None else (80.0, False)
            if rof is not None:
                _hwm_mark(wid, "rof", rof)
            buy_6a_h = wr["upkeep_buy_cr"] / span_h
            fair_6a_h = wr["upkeep_fair_cr"] / span_h
            # Procurement PPV: +pct means buying BELOW fair value; negative means overpaying above fair!
            ppv_pct = round(100.0 * (fair_6a_h - buy_6a_h) / max(1.0, fair_6a_h), 1) if (buy_6a_h >= 100.0 and fair_6a_h >= 100.0) else None
            s_ppv = _score_open_ended(100.0 + ppv_pct, 100.0, warn_ratio=0.70)[0] if ppv_pct is not None else 90.0
            scores.extend([(s_sla, 0.40), (s_rof, 0.25), (s_ppv, 0.15)])
            kpis = [
                {"k": "Supply Chains SLA", "v": "%.1f%%" % sla, "sub": "%d P1/P2 projects" % infra["p1_p2_needs_count"], "score": round(s_sla)},
                {"k": "Freight Rev / Fuel", "v": ("%.2fx" % rof) if rof is not None else "--", "sub": "+%s cr/h | %s" % (format(int(rev_h), ","), _fmt_frontier("%.1fx" % par_rof, hwm_rof, br_rof, "x")), "score": round(s_rof), "breakout": br_rof},
                {"k": "Procurement Edge (PPV)", "v": ("%+.1f%%" % ppv_pct) if ppv_pct is not None else ("%.1f runs/h" % runs_h), "sub": ("upkeep -%s/h vs fair" % format(int(buy_6a_h), ",")) if ppv_pct is not None else ("%d/%d productive" % (wr["ok_runs"], wr["runs"])), "score": round(s_ppv)},
                {"k": "Idle Rate", "v": "%.1f%%" % idle_pct, "sub": idle_sub, "score": round(s_idle)},
            ]

        elif wid == "6B":
            rev_h = round(max(wr["rev_cash"] / span_h, pax_rev_pool), 0)
            rof = round(rev_h / fuel_h, 2) if fuel_h >= 50.0 else None
            primary_rof = rof
            par_rof = 2.2
            hwm_rof = _hwm_get(wid, "rof")
            s_rof, br_rof = _score_open_ended(rof, par_rof, warn_ratio=0.45, hwm=hwm_rof) if rof is not None else (85.0, False)
            if rof is not None:
                _hwm_mark(wid, "rof", rof)
            scores.extend([(s_rof, 0.80)])
            kpis = [
                {"k": "Status", "v": "STAGED" if staged else "ACTIVE", "sub": "Haul fallback until pax_net" if staged else "charter live", "score": 100 if staged else round(s_rof)},
                {"k": "Revenue / h", "v": "+%s cr/h" % format(int(rev_h), ","), "sub": "%.1f trips/h" % (wr["ok_runs"] / span_h), "score": round(s_rof)},
                {"k": "Rev / Fuel", "v": ("%.2fx" % rof) if rof is not None else "--", "sub": "%s fuel | %s" % (format(int(fuel_h), ","), _fmt_frontier("%.1fx" % par_rof, hwm_rof, br_rof, "x")), "score": round(s_rof), "breakout": br_rof},
                {"k": "Idle Rate", "v": "%.1f%%" % idle_pct, "sub": idle_sub, "score": round(s_idle)},
            ]

        elif wid == "6C":
            b_pct = float(infra["bunker_avg_pct"])
            b_cnt = len(infra["bunkers"])
            runs_h = round(wr["ok_runs"] / span_h, 1)
            par_runs = round(18.0 * cm, 1)
            hwm_runs = _hwm_get(wid, "runs_h")
            s_bnk = _score_band(b_pct, good=92.0, warn=75.0, higher_better=True)
            s_rn, br_rn = _score_open_ended(runs_h, par_runs, warn_ratio=0.45, hwm=hwm_runs)
            _hwm_mark(wid, "runs_h", runs_h)
            scores.extend([(s_bnk, 0.50), (s_rn, 0.30)])
            kpis = [
                {"k": "Outpost Bunkers", "v": "%.1f%%" % b_pct, "sub": "%d active bunkers (50k tgt)" % b_cnt, "score": round(s_bnk)},
                {"k": "Tender Runs / h", "v": "%.1f/h" % runs_h, "sub": "%s fuel | %s" % (format(int(fuel_h), ","), _fmt_frontier("%.0f/h" % par_runs, hwm_runs, br_rn, "/h")), "score": round(s_rn), "breakout": br_rn},
                {"k": "Combat Salvage", "v": "ACTIVE" if salvage_enabled else "STAGED", "sub": "policed/lawless wrecks", "score": 90},
                {"k": "Idle Rate", "v": "%.1f%%" % idle_pct, "sub": idle_sub, "score": round(s_idle)},
            ]

        elif wid == "7A":
            r_med = float(freshness["rival_frontier_median_min"])
            r_avg = float(freshness["rival_frontier_avg_min"])
            scans_h = round(wr["scans"] / span_h, 1)
            sc_per_1k = round((scans_h * 1000.0) / fuel_h, 1) if fuel_h >= 50.0 else None
            par_med = 18.0
            par_sc = round(180.0 * cm, 0)
            par_ef = 10.0
            hwm_med = _hwm_get(wid, "r_med")
            hwm_sc = _hwm_get(wid, "scans_h")
            hwm_ef = _hwm_get(wid, "sc_per_1k")
            s_fr, br_fr = _score_open_ended_low(r_med, par_med, warn=42.0, hwm_low=hwm_med)
            s_sc, br_sc = _score_open_ended(scans_h, par_sc, warn_ratio=0.45, hwm=hwm_sc)
            s_ef, br_ef = _score_open_ended(sc_per_1k, par_ef, warn_ratio=0.45, hwm=hwm_ef) if sc_per_1k is not None else (80.0, False)
            _hwm_mark(wid, "r_med", r_med, lower=True)
            _hwm_mark(wid, "scans_h", scans_h)
            if sc_per_1k is not None:
                _hwm_mark(wid, "sc_per_1k", sc_per_1k)
            scores.extend([(s_fr, 0.35), (s_sc, 0.25), (s_ef, 0.20)])
            kpis = [
                {"k": "Rival Hub Freshness", "v": "%.1fm med" % r_med, "sub": "avg %.0fm | %s" % (r_avg, _fmt_frontier("%.0fm" % par_med, hwm_med, br_fr, "m")), "score": round(s_fr), "breakout": br_fr},
                {"k": "Systems Scanned / h", "v": "%.1f/h" % scans_h, "sub": "%d scans | %s" % (wr["scans"], _fmt_frontier("%.0f/h" % par_sc, hwm_sc, br_sc, "/h")), "score": round(s_sc), "breakout": br_sc},
                {"k": "Scans / 1k Fuel", "v": ("%.1f" % sc_per_1k) if sc_per_1k is not None else "--", "sub": "%s fuel | %s" % (format(int(fuel_h), ","), _fmt_frontier("%.0f" % par_ef, hwm_ef, br_ef)), "score": round(s_ef), "breakout": br_ef},
                {"k": "Idle Rate", "v": "%.1f%%" % idle_pct, "sub": idle_sub, "score": round(s_idle)},
            ]

        elif wid == "7B":
            g_med = float(freshness["median_min"])
            g_avg = float(freshness["avg_min"])
            scans_h = round(wr["scans"] / span_h, 1)
            sc_per_1k = round((scans_h * 1000.0) / fuel_h, 1) if fuel_h >= 50.0 else None
            par_med = 18.0
            par_sc = round(220.0 * cm, 0)
            par_ef = 10.0
            hwm_med = _hwm_get(wid, "g_med")
            hwm_sc = _hwm_get(wid, "scans_h")
            hwm_ef = _hwm_get(wid, "sc_per_1k")
            s_fr, br_fr = _score_open_ended_low(g_med, par_med, warn=42.0, hwm_low=hwm_med)
            s_sc, br_sc = _score_open_ended(scans_h, par_sc, warn_ratio=0.45, hwm=hwm_sc)
            s_ef, br_ef = _score_open_ended(sc_per_1k, par_ef, warn_ratio=0.45, hwm=hwm_ef) if sc_per_1k is not None else (80.0, False)
            _hwm_mark(wid, "g_med", g_med, lower=True)
            _hwm_mark(wid, "scans_h", scans_h)
            if sc_per_1k is not None:
                _hwm_mark(wid, "sc_per_1k", sc_per_1k)
            scores.extend([(s_fr, 0.35), (s_sc, 0.25), (s_ef, 0.20)])
            kpis = [
                {"k": "Galaxy Freshness", "v": "%.1fm med" % g_med, "sub": "%.0f%% <20m | %s" % (freshness["fresh_20m_pct"], _fmt_frontier("%.0fm" % par_med, hwm_med, br_fr, "m")), "score": round(s_fr), "breakout": br_fr},
                {"k": "Surveys & Scans / h", "v": "%.1f/h" % scans_h, "sub": "%d scans | %s" % (wr["scans"], _fmt_frontier("%.0f/h" % par_sc, hwm_sc, br_sc, "/h")), "score": round(s_sc), "breakout": br_sc},
                {"k": "Scans / 1k Fuel", "v": ("%.1f" % sc_per_1k) if sc_per_1k is not None else "--", "sub": "%s fuel | %s" % (format(int(fuel_h), ","), _fmt_frontier("%.0f" % par_ef, hwm_ef, br_ef)), "score": round(s_ef), "breakout": br_ef},
                {"k": "Idle Rate", "v": "%.1f%%" % idle_pct, "sub": idle_sub, "score": round(s_idle)},
            ]

        w_tot = sum(wt for _sc, wt in scores) or 1.0
        health_pct = round(sum((sc or 0.0) * wt for sc, wt in scores) / w_tot, 1) if not staged else round(s_idle, 1)
        status = _status_from_score(health_pct, staged=staged)
        has_breakout = any(bool(k.get("breakout")) for k in kpis)

        wings_out.append({
            "id": wid,
            "name": wname,
            "division": dv,
            "pillar": pillar,
            "responsibility_center": rc_label,
            "ships": wl["total"],
            "working": wl["working"] + wl["goal"],
            "idle": wl["idle"],
            "idle_pct": idle_pct,
            "working_pct": work_pct,
            "fuel_h": fuel_h,
            "rof": primary_rof,
            "cap_mult": cm,
            "breakout": has_breakout,
            "health_pct": health_pct,
            "status": status,
            "staged": staged,
            "kpis": kpis,
        })

    div_rollup = []
    for dv in ("Mining", "Military", "Trade", "Logistics", "Intel"):
        wlist = [w for w in wings_out if w["division"] == dv]
        d_tot = sum(w["ships"] for w in wlist)
        d_wrk = sum(w["working"] for w in wlist)
        d_idl = sum(w["idle"] for w in wlist)
        da = by_div_acc.get(dv) or {}
        d_fuel = float(da.get("fuel_cr_h") or sum(w["fuel_h"] for w in wlist))
        d_acc = float(da.get("accrual_op_h") or 0.0)
        d_rec = float(da.get("recurring_cash_h") or 0.0)
        d_roi = da.get("fuel_roi")
        active_w = [w for w in wlist if not w["staged"]]
        d_health = round(sum(w["health_pct"] * w["ships"] for w in active_w) / max(1, sum(w["ships"] for w in active_w)), 1)
        div_rollup.append({
            "division": dv,
            "ships": d_tot,
            "working": d_wrk,
            "idle": d_idl,
            "idle_pct": round(100.0 * d_idl / max(1, d_tot), 1),
            "fuel_h": round(d_fuel, 0),
            "recurring_cash_h": round(d_rec, 0),
            "accrual_op_h": round(d_acc, 0),
            "fuel_roi": round(float(d_roi), 2) if isinstance(d_roi, (int, float)) else None,
            "health_pct": d_health,
            "status": _status_from_score(d_health),
        })

    # Dynamic open-ended fleet-wide Core EBIT, Core Margin, and TCA Execution Edge (scales with hull tier T0->T5 + HWM!)
    h_filled = float(((upgrade_gaps or {}).get("hulls") or {}).get("filled_steps") or 0.0)
    fleet_avg_tier = h_filled / float(max(1, len(ships_list)))
    fleet_cap_mult = round(1.0 + 0.55 * fleet_avg_tier, 2)
    core_ebit_par_h = round(150000.0 * fleet_cap_mult, 0)
    hwm_fl = (hwm_doc or {}).get("fleet") if isinstance((hwm_doc or {}).get("fleet"), dict) else {}
    hwm_ebit = hwm_fl.get("core_ebit_h")
    hwm_margin = hwm_fl.get("core_margin_pct")
    ebit_sc, ebit_br = _score_open_ended(max(0.0, core_ebit_h), core_ebit_par_h, warn_ratio=0.35, hwm=hwm_ebit)
    if core_ebit_h < 0:
        ebit_sc, ebit_br = 0.0, False
    margin_sc, margin_br = _score_open_ended(max(0.0, core_margin_pct), 30.0, warn_ratio=0.33, hwm=hwm_margin) if core_margin_pct is not None else (None, False)
    if core_margin_pct is not None and core_margin_pct < 0:
        margin_sc, margin_br = 0.0, False
    if hwm_updates is not None:
        fup = hwm_updates.setdefault("_fleet", {})
        if core_ebit_h > 0:
            fup["core_ebit_h"] = _ratchet_hwm_high(hwm_ebit, core_ebit_h)
        if core_margin_pct is not None and core_margin_pct > 0:
            fup["core_margin_pct"] = _ratchet_hwm_high(hwm_margin, core_margin_pct)

    tot_arb_listed_cr_h = sum(w_runs[x]["arb_listed_cr"] for x in w_runs) / span_h
    tot_arb_listed_n = sum(w_runs[x]["arb_listed_n"] for x in w_runs)
    trade_rev_h = float(rb.get("trade_sales_h") or 0.0) + float(rb.get("passive_escrow_h") or 0.0)
    other_cogs_h = float(ob.get("other_cogs_h") or 0.0)
    tca_fill_pct = round(100.0 * trade_rev_h / max(1.0, trade_rev_h + tot_arb_listed_cr_h), 1) if (trade_rev_h + tot_arb_listed_cr_h) > 0 else 100.0
    tca_cogs_ratio = round(100.0 * realized_rev_h / max(1.0, realized_rev_h + other_cogs_h), 1) if (realized_rev_h + other_cogs_h) > 0 else 100.0
    tca_score = round(0.55 * _score_band(tca_fill_pct, good=92.0, warn=70.0) + 0.45 * _score_open_ended(tca_cogs_ratio, 68.0, warn_ratio=0.55)[0], 1)

    fleet_summary = {
        "hours": hours,
        "span_hours": round(span_h, 2),
        "realized_rev_h": round(realized_rev_h, 0),
        "paid_fuel_h": round(paid_fuel_h, 0),
        "other_cogs_h": round(other_cogs_h, 0),
        "core_ebit_h": round(core_ebit_h, 0),
        "core_ebit_par_h": core_ebit_par_h,
        "core_ebit_hwm_h": hwm_ebit,
        "core_ebit_score": ebit_sc,
        "core_ebit_status": _status_from_score(ebit_sc),
        "core_ebit_breakout": ebit_br,
        "core_margin_pct": core_margin_pct,
        "core_margin_tier": core_margin_tier,
        "core_margin_hwm_pct": hwm_margin,
        "core_margin_score": margin_sc,
        "core_margin_breakout": margin_br,
        "fleet_cap_mult": fleet_cap_mult,
        "tca_fill_pct": tca_fill_pct,
        "tca_arb_listed_n": tot_arb_listed_n,
        "tca_arb_listed_cr_h": round(tot_arb_listed_cr_h, 0),
        "tca_cogs_ratio_pct": tca_cogs_ratio,
        "tca_score": tca_score,
        "rev_per_fuel": rev_per_fuel,
        "core_ebit_per_fuel": ebit_per_fuel,
        "total_ships": len(ships_list),
        "working_ships": fleet_working,
        "upgrading_ships": fleet_upgrading,
        "idle_ships": fleet_idle,
        "park_ships": fleet_park,
        "idle_pct": fleet_idle_pct,
        "working_pct": fleet_working_pct,
        "host_threads": host_running_count,
        "galaxy_median_min": freshness["median_min"],
        "galaxy_avg_min": freshness["avg_min"],
        "fresh_20m_pct": freshness["fresh_20m_pct"],
        "bunker_avg_pct": infra["bunker_avg_pct"],
        "supply_sla_pct": infra["supply_sla_pct"],
        "bursar_stations_occupied": bursar_occ,
        "bursar_stations_target": 55,
    }
    return {"fleet": fleet_summary, "wings": wings_out, "divisions": div_rollup}


def publish_kpi_signals(data_dir, snapshot, now=None):
    """Write atomic machine-readable `data/fleet/kpi_signals.json` for closed-loop AutoNet steering."""
    global _LAST_SIGNAL_WRITE
    now_t = time.time() if now is None else float(now)
    if (now_t - _LAST_SIGNAL_WRITE) < SIGNAL_TTL_S:
        return None
    w6 = (snapshot.get("windows") or {}).get("6h") or (snapshot.get("windows") or {}).get("24h") or {}
    wings = w6.get("wings") or []
    fl = w6.get("fleet") or {}
    ug = snapshot.get("upgrades") or {}
    h_bw = (ug.get("hulls") or {}).get("by_wing") or {}

    wing_rof = {}
    wing_health = {}
    tighten_fuel = []
    upg_scores = []
    for w in wings:
        wid = w["id"]
        wing_health[wid] = w["health_pct"]
        if w.get("rof") is not None:
            wing_rof[wid] = w["rof"]
            if (not w.get("staged")) and w["rof"] < 1.5 and wid in ("1A-1C", "2A-2B", "3A", "3B", "3C", "3D", "3E", "4A", "4B", "5B"):
                tighten_fuel.append(wid)
        if not w.get("staged"):
            hg = h_bw.get(wid) or {}
            gap_frac = max(0.0, 1.0 - float(hg.get("pct_done", 100.0)) / 100.0)
            rof_pen = 0.25 if (w.get("rof") is not None and w["rof"] < 1.3) else (0.15 if w["health_pct"] < 70.0 else 0.0)
            upg_scores.append((round(gap_frac + rof_pen, 3), wid))
    upg_scores.sort(reverse=True)

    infra = snapshot.get("infra") or {}
    payload = {
        "updated_at": int(now_t),
        "core_ebit_h": fl.get("core_ebit_h"),
        "core_margin_pct": fl.get("core_margin_pct"),
        "core_margin_tier": fl.get("core_margin_tier"),
        "rev_per_fuel": fl.get("rev_per_fuel"),
        "fleet_idle_pct": fl.get("idle_pct"),
        "galaxy_median_min": fl.get("galaxy_median_min"),
        "bunker_avg_pct": infra.get("bunker_avg_pct", 100.0),
        "low_bunker_bases": infra.get("low_bunker_bases") or [],
        "supply_sla_pct": infra.get("supply_sla_pct", 100.0),
        "boost_upkeep_urgency": bool(float(infra.get("bunker_avg_pct", 100.0)) < 90.0 or float(infra.get("supply_sla_pct", 100.0)) < 85.0),
        "bursar_stations_occupied": fl.get("bursar_stations_occupied", 0),
        "wing_rof": wing_rof,
        "wing_health": wing_health,
        "tighten_fuel_wings": sorted(tighten_fuel),
        "priority_upgrade_wings": [wid for _sc, wid in upg_scores if _sc > 0.05],
    }
    try:
        out_p = Path(data_dir) / "fleet" / "kpi_signals.json"
        out_p.parent.mkdir(parents=True, exist_ok=True)
        tmp = out_p.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        os.replace(tmp, out_p)
        _LAST_SIGNAL_WRITE = now_t
    except OSError:
        pass
    return payload


def read_kpi_signals(data_dir=DATA_DEFAULT, max_age_s=600.0):
    """Lightweight reader for AutoNets (returns {} cleanly if missing or stale)."""
    p = Path(data_dir) / "fleet" / "kpi_signals.json"
    d = _read_json(p, {})
    if not isinstance(d, dict) or not d.get("updated_at"):
        return {}
    if (time.time() - float(d.get("updated_at") or 0)) > float(max_age_s):
        return {}
    return d


def compute_standing_goals(conn, fleet_doc, windows, upgrade_gaps, freshness, infra, repo_root, data_dir):
    """Compute all 13 measurable Eternal Standing-Goal KPIs (hard late-game rival benchmarks + open-ended fleet economics).
    Targets are engineered so early/mid-game never falsely caps at 100% green, while late-game dominance pushes >100 APEX.
    """
    def _fmt_m(v):
        v = float(v or 0.0)
        if abs(v) >= 1e9:
            return "%.2fB" % (v / 1e9)
        if abs(v) >= 1e6:
            return "%.1fM" % (v / 1e6)
        if abs(v) >= 1e3:
            return "%.0fk" % (v / 1e3)
        return "%d" % int(round(v))

    # 1. Rival benchmarks from live rivals.py / read.db:rival_snapshots
    our_w = our_ship_v = our_ore = our_craft = 0.0
    top_w_tag, top_w = "BUSY", 0.0
    top_mil_tag, top_mil = "BUSY", 0.0
    top_ore_tag, top_ore = "BUSY", 0.0
    top_cr_tag, top_cr = "BUSY", 0.0
    top_tour_name, top_tour_rev = "The Obsidian Well", 0.0
    our_tour_rev = 0.0
    our_appeal = 0
    seated_n = 0
    seat_cap = 0
    own_stations = 0
    own_outposts = 0

    try:
        import rivals as _rv
        sc = _rv.compute_sedcards(repo_root=str(repo_root), data_dir=str(data_dir)) or {}
        our_s = sc.get("our") or {}
        our_w = float(our_s.get("wealth") or 0.0)
        seated_n = int(our_s.get("seated_members") or our_s.get("members") or 0)
        for sd in (sc.get("sedcards") or []):
            if not isinstance(sd, dict) or str(sd.get("tag") or "").upper() == "CLTV":
                continue
            tg = str(sd.get("tag") or "?")
            w_v = float(sd.get("wealth") or 0.0)
            sh_v = float(sd.get("ship_value") or 0.0)
            or_v = float(sd.get("ore_mined") or 0.0)
            cr_v = float(sd.get("items_crafted") or 0.0)
            if w_v > top_w:
                top_w, top_w_tag = w_v, tg
            if sh_v > top_mil:
                top_mil, top_mil_tag = sh_v, tg
            if or_v > top_ore:
                top_ore, top_ore_tag = or_v, tg
            if cr_v > top_cr:
                top_cr, top_cr_tag = cr_v, tg
        ttop = sc.get("tourism_top") or []
        if ttop and isinstance(ttop[0], dict):
            top_tour_name = str(ttop[0].get("name") or "Top Rival Resort")
            top_tour_rev = float(ttop[0].get("revenue") or 0.0)
    except Exception:
        pass

    if conn is not None:
        try:
            tbls = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()}
            if "faction" in tbls:
                fr = conn.execute("SELECT member_count, members_limit FROM faction LIMIT 1").fetchone()
                if fr:
                    seated_n = int(fr[0] or seated_n)
                    seat_cap = int(fr[1] or 0)
            if "bases" in tbls:
                for (bk,) in conn.execute("SELECT kind FROM bases").fetchall():
                    if "station" in str(bk or "").lower():
                        own_stations += 1
                    else:
                        own_outposts += 1
            if "rival_snapshots" in tbls:
                r_cltv = conn.execute(
                    "SELECT wealth, ship_value, ore_mined, items_crafted FROM rival_snapshots WHERE tag='CLTV' ORDER BY t DESC LIMIT 1"
                ).fetchone()
                if r_cltv:
                    our_w = max(our_w, float(r_cltv[0] or 0.0))
                    our_ship_v = float(r_cltv[1] or 0.0)
                    our_ore = float(r_cltv[2] or 0.0)
                    our_craft = float(r_cltv[3] or 0.0)
            if "faction_facilities" in tbls:
                rc_types = [r[0] for r in conn.execute("SELECT type FROM faction_facilities WHERE COALESCE(status,'active')='active'").fetchall()]
                cat_files = sorted((Path(data_dir) / "catalog").glob("0.*.json")) or sorted((Path(data_dir) / "catalog").glob("*.json"))
                for cf in reversed(cat_files):
                    cat = _read_json(cf, {})
                    rfacs = cat.get("facilities") or {}
                    if rfacs:
                        fmap = {x.get("id"): x for x in rfacs if isinstance(x, dict)} if isinstance(rfacs, list) else rfacs
                        for ft in rc_types:
                            fi = fmap.get(ft) or {}
                            our_appeal += int(fi.get("dining_points") or 0) + int(fi.get("leisure_points") or 0) + int(fi.get("lodging_points") or 0)
                        break
            if "stats_pilot_last" in tbls:
                for sk, sv in conn.execute("SELECT key, SUM(COALESCE(value, 0)) FROM stats_pilot_last WHERE key IN ('ore_mined', 'items_crafted') GROUP BY key").fetchall():
                    if sk == "ore_mined":
                        our_ore = max(our_ore, float(sv or 0.0))
                    elif sk == "items_crafted":
                        our_craft = max(our_craft, float(sv or 0.0))
        except Exception:
            pass

    w1 = ((windows or {}).get("1h") or {}).get("fleet") or {}
    w6 = ((windows or {}).get("6h") or {}).get("fleet") or {}
    fl_ref = w1 if w1.get("realized_rev_h") else w6
    tot_ships = int(fl_ref.get("total_ships") or len((fleet_doc or {}).get("ships") or []) or 500)

    def _ratio_goal(gid, sg, title, cur_v, rival_v, rival_lbl, factor, unit_fn=_fmt_m):
        tgt_v = rival_v * factor if rival_v > 0 else 1.0
        ratio = (cur_v / rival_v) if rival_v > 0 else 0.0
        pct = round(100.0 * cur_v / tgt_v, 1) if tgt_v > 0 else 0.0
        sc = round(100.0 + 38.0 * math.log(cur_v / tgt_v), 1) if (cur_v >= tgt_v and tgt_v > 0) else round(min(99.9, pct), 1)
        return {
            "id": gid, "sg": sg, "title": title, "group": "supremacy",
            "value": "%.3fx" % ratio if ratio < 0.1 else "%.2fx" % ratio,
            "target": "%.2fx %s" % (factor, rival_lbl),
            "sub": "CLTV %s vs %s %s (need %s)" % (unit_fn(cur_v), rival_lbl, unit_fn(rival_v), unit_fn(tgt_v)),
            "pct": pct, "score": sc, "status": _status_from_score(sc),
        }

    # Tourism: compare appeal (target +15% over rival benchmark 50 appeal -> 58+ appeal) & station revenue vs top rival
    tour_rev_ratio = (our_tour_rev / top_tour_rev) if top_tour_rev > 0 else 0.0
    tour_appeal_tgt = 58
    tour_pct = round(100.0 * our_appeal / float(tour_appeal_tgt), 1)
    tour_sc = round(100.0 + 30.0 * math.log(our_appeal / float(tour_appeal_tgt)), 1) if our_appeal >= tour_appeal_tgt else round(min(99.9, tour_pct * 0.85), 1)

    hulls = (upgrade_gaps or {}).get("hulls") or {}
    mods = (upgrade_gaps or {}).get("modules") or {}
    h_pct = float(hulls.get("pct_done") or 0.0)
    m_slot_pct = float(mods.get("slot_pct_done") or 0.0)
    m_tier_pct = float(mods.get("tier_pct_done") or 0.0)
    m_comb = round(0.6 * m_slot_pct + 0.4 * m_tier_pct, 1)
    seat_pct_1k = round(100.0 * seated_n / 1000.0, 1)
    emp_pct = round(100.0 * (own_stations + own_outposts) / 13.0, 1)
    g_med = float((freshness or {}).get("median_min") or 99.0)
    r_med = float((freshness or {}).get("rival_frontier_median_min") or 99.0)
    intel_sc, intel_br = _score_open_ended_low(g_med, 10.0, warn=35.0)
    ebit_sc = float(fl_ref.get("core_ebit_score") or 0.0)
    ebit_h = float(fl_ref.get("core_ebit_h") or 0.0)
    ebit_par = float(fl_ref.get("core_ebit_par_h") or 150000.0)
    margin_pct = fl_ref.get("core_margin_pct")
    margin_sc = float(fl_ref.get("core_margin_score") or 0.0)
    tca_sc = float(fl_ref.get("tca_score") or 0.0)

    goals = [
        _ratio_goal("SG-WEALTH", "SG1", "Galactic Wealth Supremacy", our_w, top_w, "[%s]" % top_w_tag, 2.0),
        _ratio_goal("SG-MILITARY", "SG1/SG2", "Military Firepower Supremacy", our_ship_v, top_mil, "[%s]" % top_mil_tag, 2.0),
        {
            "id": "SG-TOURISM", "sg": "SG3/SG4", "title": "Tourism Hub Crown (+15% Margin)", "group": "supremacy",
            "value": "%d Appeal" % our_appeal,
            "target": "+15%% vs %s" % top_tour_name[:16],
            "sub": "Ridgecrest %d appeal | #1 %s rev %s cr" % (our_appeal, top_tour_name, _fmt_m(top_tour_rev)),
            "pct": tour_pct, "score": tour_sc, "status": _status_from_score(tour_sc),
        },
        _ratio_goal("SG-INDUSTRY", "SG4", "Industrial Manufacturing Crown", our_craft, top_cr, "[%s]" % top_cr_tag, 2.0),
        _ratio_goal("SG-EXTRACT", "SG4", "Resource Extraction Crown", our_ore, top_ore, "[%s]" % top_ore_tag, 2.0),
        {
            "id": "SG-EBIT", "sg": "SG1/SG4", "title": "Core Operating Profit (Dynamic EBIT)", "group": "economics",
            "value": "%s%s cr/h" % ("+" if ebit_h >= 0 else "", format(int(round(ebit_h)), ",")),
            "target": "par +%s cr/h (open-ended)" % format(int(round(ebit_par)), ","),
            "sub": "1h IFRS 15 Ex-Seeds | %.2fx cap | HWM %s" % (
                float(fl_ref.get("fleet_cap_mult") or 1.0),
                ("+%s" % format(int(round(fl_ref["core_ebit_hwm_h"])), ",")) if fl_ref.get("core_ebit_hwm_h") else "calibrating",
            ),
            "pct": round(max(0.0, 100.0 * ebit_h / max(1.0, ebit_par)), 1),
            "score": round(ebit_sc, 1), "status": _status_from_score(ebit_sc),
            "breakout": bool(fl_ref.get("core_ebit_breakout")),
        },
        {
            "id": "SG-MARGIN", "sg": "SG1/SG4", "title": "Core Operating Margin (30%+ / 50%+)", "group": "economics",
            "value": ("%.1f%%" % float(margin_pct)) if margin_pct is not None else "--",
            "target": "30%+ target | 50%+ ELITE",
            "sub": "IFRS 15 EBIT / Realized Rev | ROF %sx | HWM %s" % (
                fl_ref.get("rev_per_fuel") or "--",
                ("%.1f%%" % float(fl_ref["core_margin_hwm_pct"])) if fl_ref.get("core_margin_hwm_pct") else "calibrating",
            ),
            "pct": round(max(0.0, 100.0 * float(margin_pct or 0.0) / 50.0), 1),
            "score": round(margin_sc, 1), "status": _status_from_score(margin_sc),
            "breakout": bool(fl_ref.get("core_margin_breakout")),
        },
        {
            "id": "SG-TCA", "sg": "SG4", "title": "Trade & Procurement Execution (TCA)", "group": "economics",
            "value": "%.1f%% fill" % float(fl_ref.get("tca_fill_pct") or 100.0),
            "target": ">=92% fill | low COGS drag",
            "sub": "Other COGS -%s/h | %d arb listed (-%s/h) | Rev/(Rev+COGS) %.0f%%" % (
                format(int(round(float(fl_ref.get("other_cogs_h") or 0.0))), ","),
                int(fl_ref.get("tca_arb_listed_n") or 0),
                format(int(round(float(fl_ref.get("tca_arb_listed_cr_h") or 0.0))), ","),
                float(fl_ref.get("tca_cogs_ratio_pct") or 0.0),
            ),
            "pct": float(fl_ref.get("tca_fill_pct") or 0.0),
            "score": round(tca_sc, 1), "status": _status_from_score(tca_sc),
        },
        {
            "id": "SG-SEATING", "sg": "SG2", "title": "Grand Fleet Seating (1,000 Eternal)", "group": "infrastructure",
            "value": "%d / 1,000" % seated_n,
            "target": "500 Phase-1 | 1,000 Eternal",
            "sub": "%d/%d Phase-1 seated (cap %d) | %d unseated" % (seated_n, tot_ships, seat_cap, max(0, tot_ships - seated_n)),
            "pct": seat_pct_1k, "score": seat_pct_1k, "status": _status_from_score(round(100.0 * seated_n / max(1, tot_ships), 1)),
        },
        {
            "id": "SG-HULLS", "sg": "SG2", "title": "Dynamic Hull Modernization (T1-T5)", "group": "infrastructure",
            "value": "%.1f%% (%d/%d)" % (h_pct, int(hulls.get("filled_steps") or 0), int(hulls.get("possible_steps") or 0)),
            "target": "100% of dynamic T1-T5 cap",
            "sub": "%d steps missing | scales upward as Piloting rises" % int(hulls.get("missing_steps") or 0),
            "pct": h_pct, "score": h_pct, "status": _status_from_score(h_pct),
        },
        {
            "id": "SG-MODULES", "sg": "SG2", "title": "Dynamic Module Fitting (T1-T5)", "group": "infrastructure",
            "value": "%.1f%% slots | %.1f%% tier" % (m_slot_pct, m_tier_pct),
            "target": "100% slots & tier-max",
            "sub": "%d empty slots | %d ships below blueprint tier-max" % (int(mods.get("missing_slots") or 0), int(mods.get("ships_missing_tier") or 0)),
            "pct": m_comb, "score": m_comb, "status": _status_from_score(m_comb),
        },
        {
            "id": "SG-EMPIRE", "sg": "SG3", "title": "Sovereign Industrial Empire", "group": "infrastructure",
            "value": "%d/5 Stn | %d/8 Outp" % (own_stations, own_outposts),
            "target": "5 regional stations + 8 outposts",
            "sub": "%d/13 sovereign anchors | bunkers %.1f%% avg" % (own_stations + own_outposts, float((infra or {}).get("bunker_avg_pct") or 0.0)),
            "pct": emp_pct, "score": emp_pct, "status": _status_from_score(emp_pct),
        },
        {
            "id": "SG-INTEL", "sg": "SG5", "title": "Galactic Omniscience (Freshness)", "group": "infrastructure",
            "value": "%.1fm med" % g_med,
            "target": "<=10m galaxy | <=5m rivals",
            "sub": "rival hubs %.1fm med | %d/%d systems charted" % (r_med, int((freshness or {}).get("systems_scanned") or 0), int((freshness or {}).get("systems_total") or 0)),
            "pct": round(min(100.0, 100.0 * 10.0 / max(1.0, g_med)), 1),
            "score": round(intel_sc or 0.0, 1), "status": _status_from_score(intel_sc),
            "breakout": bool(intel_br),
        },
    ]
    return goals


def compute_fleet_kpis(repo_root=REPO_DEFAULT, data_dir=DATA_DEFAULT, accounting_by_win=None, now=None, write_signals=True):
    """Main entry point: compute full dynamic upgrade gaps, freshness, infra SLA, and 1h/6h/24h wing KPIs."""
    now_t = time.time() if now is None else float(now)
    data_p = Path(data_dir)
    fleet_doc = _read_json(data_p / "fleet" / "fleet.json", {})
    ships_list = list(fleet_doc.get("ships") or [])

    pilot_wing = {}
    pilot_div = {}
    for s in ships_list:
        p = str(s.get("name") or "")
        dv = str(s.get("division") or "")
        pilot_div[p] = dv
        pilot_wing[p] = wing_id_of(s.get("wing"), dv)

    rdir = data_p / "fleet" / "host" / "running"
    try:
        host_running = sum(1 for _ in rdir.iterdir()) if rdir.is_dir() else 0
    except OSError:
        host_running = 0

    bclaims = _read_json(data_p / "fleet" / "bursar_claims.json", {})
    occ_bases = set()
    if isinstance(bclaims, dict):
        for bk, rec in bclaims.items():
            if isinstance(rec, dict) and (now_t - float(rec.get("at") or 0)) < 7200.0:
                occ_bases.add(str(bk))
    for s in ships_list:
        if str(s.get("order") or "").startswith("bursar") and s.get("docked"):
            b = str(s.get("base") or s.get("docked") or "")
            if b:
                occ_bases.add(b)
    bursar_occ = len(occ_bases)

    db = data_p / "store" / "read.db"
    conn = None
    try:
        if db.is_file():
            conn = sqlite3.connect("file:%s?mode=ro&immutable=1" % db, uri=True, timeout=2.0)
        upgrade_gaps = compute_upgrade_gaps(conn, ships_list, repo_root, data_p)
        infra = _compute_bunker_and_supply_sla(conn, data_p)
        freshness = _compute_scouting_freshness(data_p, repo_root, now_t)

        acc_map = dict(accounting_by_win or {})
        if not acc_map and conn is not None:
            import accounting as _acc
            for lbl, hrs in (("1h", 1), ("6h", 6), ("24h", 24)):
                try:
                    acc_map[lbl] = _acc.compute_pnl(conn, repo_root=str(repo_root), data_dir=str(data_p), fleet_json=fleet_doc, hours=hrs, now=now_t)
                except Exception:
                    acc_map[lbl] = {}

        hwm_doc = _load_hwm(data_p)
        hwm_updates = {}
        windows = {}
        for lbl, hrs in (("1h", 1), ("6h", 6), ("24h", 24)):
            windows[lbl] = _compute_window_wing_kpis(
                conn, ships_list, pilot_wing, pilot_div, acc_map.get(lbl) or {}, hrs, now_t,
                data_p, repo_root, freshness, infra, upgrade_gaps, bursar_occ, host_running,
                hwm_doc=hwm_doc, hwm_updates=(hwm_updates if (write_signals and lbl == "6h") else None),
            )
        if write_signals and hwm_updates:
            w6_span = float(((windows.get("6h") or {}).get("fleet") or {}).get("span_hours") or 0.0)
            if w6_span >= 1.0:
                merged_w = dict(hwm_doc.get("wings") or {})
                merged_f = dict(hwm_doc.get("fleet") or {})
                for wk, wv in hwm_updates.items():
                    if wk == "_fleet":
                        merged_f.update(wv)
                    else:
                        cur_w = dict(merged_w.get(wk) or {})
                        cur_w.update(wv)
                        merged_w[wk] = cur_w
                _save_hwm(data_p, {"wings": merged_w, "fleet": merged_f}, now_t)
        standing_goals = compute_standing_goals(conn, fleet_doc, windows, upgrade_gaps, freshness, infra, repo_root, data_p)
    finally:
        if conn is not None:
            try:
                conn.close()
            except Exception:
                pass

    out = {
        "at": int(now_t),
        "upgrades": upgrade_gaps,
        "freshness": freshness,
        "infra": infra,
        "standing_goals": standing_goals,
        "windows": windows,
    }
    if write_signals:
        publish_kpi_signals(data_p, out, now=now_t)
        try:
            snap_p = Path(data_p) / "fleet" / "kpi_snapshot.json"
            snap_p.parent.mkdir(parents=True, exist_ok=True)
            snap_tmp = snap_p.with_name(f"kpi_snapshot.{os.getpid()}.tmp")
            snap_tmp.write_text(json.dumps({"updated_at": int(now_t), "standing_goals": out.get("standing_goals") or [], "windows": out.get("windows") or {}}, separators=(",", ":")), encoding="ascii")
            os.replace(snap_tmp, snap_p)
        except OSError:
            pass
    return out


def print_summary(repo_root=REPO_DEFAULT, data_dir=DATA_DEFAULT, win="6h"):
    fk = compute_fleet_kpis(Path(repo_root), Path(data_dir), write_signals=False)
    win = win if win in ("1h", "6h", "24h") else "6h"
    w = (fk.get("windows") or {}).get(win) or {}
    fl = w.get("fleet") or {}
    upg = fk.get("upgrades") or {}
    hulls = upg.get("hulls") or {}
    mods = upg.get("modules") or {}
    fr = fk.get("freshness") or {}
    inf = fk.get("infra") or {}
    print("FLEET KPI SUMMARY (%s) | ships=%s active=%s upg=%s idle=%s (%.1f%%) park=%s threads=%s" % (
        win, fl.get("total_ships"), fl.get("working_ships"), fl.get("upgrading_ships"),
        fl.get("idle_ships"), float(fl.get("idle_pct") or 0.0), fl.get("park_ships"), fl.get("host_threads")))
    _cm_s = ("%.1f%% [%s]" % (float(fl["core_margin_pct"]), fl.get("core_margin_tier") or "")) if fl.get("core_margin_pct") is not None else "--"
    print("  FINANCE (%s): Core Margin=%s | Core EBIT=%s cr/h | Realized Rev=%s cr/h | Paid Fuel=%s cr/h | ROF=%sx" % (
        win, _cm_s, format(int(round(fl.get("core_ebit_h") or 0)), ","),
        format(int(round(fl.get("realized_rev_h") or 0)), ","),
        format(int(round(fl.get("paid_fuel_h") or 0)), ","), fl.get("rev_per_fuel")))
    print("  READINESS: Hulls %s/%s (%.1f%%, missing %s) | Mod Slots %s/%s (%.1f%%, tier %.1f%%)" % (
        hulls.get("filled_steps"), hulls.get("possible_steps"), float(hulls.get("pct_done") or 0.0), hulls.get("missing_steps"),
        mods.get("filled_slots"), mods.get("possible_slots"), float(mods.get("slot_pct_done") or 0.0), float(mods.get("tier_pct_done") or 0.0)))
    print("  INTEL & INFRA: Galaxy %s/%s (<60m %.1f%%, med %.1fm, rival med %.1fm) | Bunkers %.1f%% | Supply SLA %.1f%% | Bursars %s/%s" % (
        fr.get("systems_scanned"), fr.get("systems_total"), float(fr.get("fresh_60m_pct") or 0.0),
        float(fr.get("median_min") or 0.0), float(fr.get("rival_frontier_median_min") or 0.0),
        float(inf.get("bunker_avg_pct") or 0.0), float(inf.get("supply_sla_pct") or 0.0),
        fl.get("bursar_stations_occupied"), fl.get("bursar_stations_target")))
    sgs = fk.get("standing_goals") or []
    if sgs:
        print("  ETERNAL STANDING GOALS (%d):" % len(sgs))
        for g in sgs:
            print("    %-12s %-34s val=%-18s tgt=%-24s sc=%5.1f [%10s]" % (
                g.get("id"), str(g.get("title") or "")[:34], str(g.get("value") or "")[:18],
                str(g.get("target") or "")[:24], float(g.get("score") or 0.0), g.get("status")))
    print("  WINGS (%s):" % win)
    for wg in (w.get("wings") or []):
        ms = ", ".join("%s=%s" % (m.get("k"), m.get("v")) for m in (wg.get("kpis") or [])[:4])
        lbl = ("%s %s" % (wg.get("id") or "", wg.get("name") or "")).strip()
        rof_s = ("%.2fx" % float(wg["rof"])) if wg.get("rof") is not None else "n/a"
        print("    %-30s n=%3s work=%3s idle=%2s fuel=%6s rof=%6s hp=%4.0f%% [%6s] | %s" % (
            lbl[:30], wg.get("ships"), wg.get("working"), wg.get("idle"),
            format(int(round(float(wg.get("fuel_h") or 0))), ","), rof_s,
            float(wg.get("health_pct") or 0.0), wg.get("status"), ms))


if __name__ == "__main__":
    import sys as _sys
    _here = str(Path(__file__).resolve().parent)
    if _here not in _sys.path:
        _sys.path.insert(0, _here)
    _args = _sys.argv[1:]
    _win = "6h"
    if "--window" in _args and _args.index("--window") + 1 < len(_args):
        _win = _args[_args.index("--window") + 1]
    elif "--hours" in _args and _args.index("--hours") + 1 < len(_args):
        _h = str(_args[_args.index("--hours") + 1])
        _win = _h + "h" if not _h.endswith("h") else _h
    _data = DATA_DEFAULT
    if "--data" in _args and _args.index("--data") + 1 < len(_args):
        _data = Path(_args[_args.index("--data") + 1])
    _root = REPO_DEFAULT
    if "--root" in _args and _args.index("--root") + 1 < len(_args):
        _root = Path(_args[_args.index("--root") + 1])
    print_summary(_root, _data, win=_win)

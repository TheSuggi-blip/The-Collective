#!/usr/bin/env python3
"""hunt_net.py -- Policy-driven dynamic smart Military network (`hunt-network`).

WHAT:
  One autonomous multi-lane combat runner for Military (Apophis/Unity), governed by
  `game/hunt-policy.json`. Combines four priority lanes with scale-free percentage
  combat-power gating (auto-scaling seamlessly across T0 -> T1 -> T2 -> T3 -> T4 -> T5):

    1. Escort & Protection (`escort`): Dynamic on-demand protection (guard.py --follow /
       place guard) for explicitly configured sites/pilots or civilians working in
       lawless / pirate-sighted systems. Uses 0 ships when no escort is needed so 100%
       of Military farms when space is clear.
    2. Coordinated Group Packs (`packs`: 3 / 5 / 8 / 10 ships, ~20-30% target share):
       Forms atomic squads in `data/fleet/hunt_packs.json` sized dynamically to the
       smallest pack in [3, 5, 8, 10] whose combined fighting power meets
       `min_power_ratio` against tougher high-loot wildlife (pilot whales, cauldronbacks,
       bullionauts, predators) or lone NPC pirates. First 3 share a game fleet
       (`spacemolt_fleet`), members 4..10 join the exact same battle as synchronized
       outside attackers (`hunt`/`attack` on leader's target_id), with unified pack flee
       safety, wreck looting, and F38 ranching protection.
    3. Solo Optimal Herd Hunting (`solo`): Global 1-to-1 optimal matcher across all wild
       grazer herds (>= min_creatures, default 3), power-ratio gated so upgraded hulls
       automatically graduate to higher-tier herds while T0s stay safe on soft grazers.
       Delegates to proven `hunt.py` (`--keep-herd 2`, `--alone`, `--gift-to trader`),
       stamping instant POI cooldowns in `data/fleet/hunt_claims.json` when the F38
       ranch floor is hit.
    4. Low-Burn Combat XP Fallback: Closest safe soft herd so 0 combat ships sit idle.

USAGE:
  python3 -I -B game/fleet/hunt_net.py <pilot> [--minutes 45] [--policy game/hunt-policy.json] [--route hunt-network]

Stdlib only. ASCII only.
"""
import fcntl
import json
import math
import os
import re
import signal
import sqlite3
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]          # game/
REPO = ROOT.parent
DATA = Path(os.environ.get("FLEET_DATA_ROOT") or "/srv/collective/data")
GATE = os.environ.get("FLEET_GATE", "http://172.30.0.32:7580")
OPENER = urllib.request.build_opener(urllib.request.ProxyHandler({}))
DEFAULT_POLICY_PATH = REPO / "game" / "hunt-policy.json"

DEFAULT_POLICY = {
    "enabled": True,
    "claim_ttl_s": 4200,
    "cooldown_minutes": 90,
    "keep_herd": 2,
    "min_creatures": 3,
    "census_max_age_min": 180,
    "pirate_avoid_hours": 6.0,
    "policed_only": False,
    "allow_lawless_min_power": 350.0,
    "exclude_systems": [],
    "exclude_pois": [],
    "exclude_species": [],
    "partner_factions": ["HEXC", "IRLC", "NOIR"],
    "gift_to": "trader",
    "escort": {
        "enabled": True,
        "max_ships": 12,
        "max_fleet_share": 0.15,
        "threat_window_h": 4.0,
        "auto_protect_lawless_civilians": True,
        "protect_pilots": [],
        "protect_places": [],
        "max_jumps": 10,
        "min_power": 350.0,
        "minutes": 45,
    },
    "packs": {
        "enabled": True,
        "target_share": 0.25,
        "sizes": [3, 5, 8, 10],
        "min_power_ratio": 1.80,
        "pirate_min_power_ratio": 2.20,
        "pirates_enabled": True,
        "pirate_tiers": ["scout", "raider"],
        "min_member_power": 420.0,
        "min_target_hull": 80,
        "rally_max_jumps": 8,
        "rally_timeout_s": 150,
        "arrive_timeout_s": 240,
        "fight_ticks": 45,
        "flee_hull_pct": 80,
        "close_dist": 2,
        "max_jumps": 12,
        "priority_species": [
            "pilot_whale", "bullionaut", "cauldronback", "facet_druse",
            "kiln_snail", "slag_tortoise", "bulwark", "glintfin",
            "glitterback_crab", "deuteron_slug", "hollow_pilgrim",
            "mirror_skate", "inkwyrm", "magnet_barnacle", "silica_borer",
        ],
    },
    "solo": {
        "enabled": True,
        "min_power_ratio": 1.35,
        "ideal_ratio_low": 1.45,
        "ideal_ratio_high": 3.20,
        "max_jumps": 10,
        "kills_per_run": 6,
        "alone": True,
        "min_bid": 1500,
    },
    "fallback": {
        "enabled": True,
        "max_jumps": 6,
    },
    "rest_seconds_when_empty": 120,
}

# Known baseline creature hull & loot values (overridden live from data/wildlife & read.db)
DEFAULT_SPECIES_HULL = {
    "nullbubble": 35, "cinder_sylph": 40, "drift_ray": 45, "frost_moth": 45,
    "bell_jelly": 45, "halo_drifter": 50, "phase_lurker": 55, "belt_grazer": 60,
    "patina_grazer": 60, "glitterback_crab": 60, "rime_grazer": 65, "pressblister": 65,
    "veil_ray": 60, "hollow_pilgrim": 70, "cinder_urchin": 70, "sift_ray": 75,
    "deuteron_slug": 85, "slag_tortoise": 90, "bulwark": 95, "kiln_snail": 100,
    "facet_druse": 110, "cauldronback": 120, "bullionaut": 130, "glintfin": 140,
    "mirror_skate": 95, "inkwyrm": 100, "magnet_barnacle": 110, "silica_borer": 115,
    "pilot_whale": 220,
}

SPECIES_NEED_DROPS = {
    "mirror_skate": ("foil_scale",),
    "cauldronback": ("alloy_scale",),
    "inkwyrm": ("cobalt_ink",),
    "magnet_barnacle": ("ferrous_nodule",),
    "silica_borer": ("silica_lens",),
    "hollow_pilgrim": ("ember_gland", "caustic_sac"),
    "pilot_whale": ("whale_blubber", "graphene_thread", "antimatter_residue"),
}


def utc_now():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def read_json(path, default):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def write_json(path, obj):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".%d.tmp" % os.getpid())
    tmp.write_text(json.dumps(obj, separators=(",", ":"), sort_keys=True), encoding="utf-8")
    os.replace(tmp, path)


def ship_file_name(pilot):
    return (re.sub(r"[^A-Za-z0-9_.-]", "_", str(pilot or ""))[:60] or "pilot") + ".json"


def load_command_flagships(data_dir):
    fg = read_json(Path(data_dir) / "fleet" / "flagships.json", {})
    if not isinstance(fg, dict):
        return set()
    return {str(k) for k, v in fg.items() if isinstance(v, dict) and str(v.get("division") or "") == "Command"}


def deep_merge(base, override):
    out = json.loads(json.dumps(base))
    if not isinstance(override, dict):
        return out
    for k, v in override.items():
        if k.startswith("_"):
            continue
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = deep_merge(out[k], v)
        else:
            out[k] = v
    return out


def load_policy(path=None):
    p = Path(path) if path else DEFAULT_POLICY_PATH
    if not p.is_absolute():
        p = REPO / p
    return deep_merge(DEFAULT_POLICY, read_json(p, {}))


def load_weapon_catalog(data_dir):
    """Load weapon DPS/reach and shield booster bonuses from newest data/catalog/<ver>.json."""
    cdir = Path(data_dir) / "catalog"
    weps = {}
    boosters = {}
    if not cdir.is_dir():
        return weps, boosters
    cands = sorted([p for p in cdir.glob("*.json") if p.stat().st_size > 100000], key=lambda p: p.stat().st_mtime)
    if not cands:
        return weps, boosters
    doc = read_json(cands[-1], {})
    items = doc.get("items") or []
    if isinstance(items, dict):
        items = list(items.values())
    for it in items:
        if not isinstance(it, dict):
            continue
        iid = str(it.get("id") or it.get("type_id") or "")
        if not iid:
            continue
        dmg = float(it.get("damage") or 0)
        if dmg > 0:
            cd = max(1.0, float(it.get("cooldown") or 1.0))
            weps[iid] = {"dps": dmg / cd, "reach": int(it.get("reach") or 3), "damage": dmg}
        elif "shield_booster" in iid or "armor_plate" in iid:
            val = float(it.get("shield_bonus") or it.get("armor_bonus") or it.get("bonus") or 40.0)
            boosters[iid] = val
    return weps, boosters


def compute_ship_power(ship_doc, weapon_catalog=None, booster_catalog=None):
    """Scale-free ship Combat Power derived from live hull/shield/armor/modules/skills (auto-scales T0->T5+)."""
    weps = weapon_catalog or {}
    boosters = booster_catalog or {}
    sh_sub = ship_doc.get("ship") if isinstance(ship_doc.get("ship"), dict) else {}
    max_hull = float(ship_doc.get("max_hull") or sh_sub.get("max_hull") or ship_doc.get("hull") or 75.0)
    max_shield = float(ship_doc.get("max_shield") or sh_sub.get("max_shield") or ship_doc.get("shield") or 60.0)
    armor = float(ship_doc.get("armor") or sh_sub.get("armor") or 3.0)
    tier = int(ship_doc.get("tier") or ship_doc.get("hull_tier") or 0)

    skills = ship_doc.get("skills") if isinstance(ship_doc.get("skills"), dict) else {}
    def _sk(name):
        v = skills.get(name)
        return int(v.get("level") or 0) if isinstance(v, dict) else int(v or 0)
    wep_lvl = max(_sk("weapons"), _sk("gunnery"), _sk("combat"))
    tac_lvl = _sk("tactics")

    total_dps = 0.0
    ehp_bonus = 0.0
    max_reach = 3
    wep_count = 0
    for m in ship_doc.get("modules") or []:
        tid = str((m.get("type") or m.get("type_id") or "") if isinstance(m, dict) else m).lower()
        if not tid:
            continue
        if tid in weps:
            total_dps += float(weps[tid]["dps"])
            max_reach = max(max_reach, int(weps[tid].get("reach") or 3))
            wep_count += 1
        elif any(tok in tid for tok in ("laser", "cannon", "railgun", "blaster", "plasma", "missile", "torpedo")) and "mining" not in tid:
            # Fallback DPS estimate if catalog absent
            base_d = 24.0 if tid.endswith("_iii") else (16.0 if tid.endswith("_ii") else 10.0)
            total_dps += base_d
            wep_count += 1
        elif tid in boosters:
            ehp_bonus += float(boosters[tid])
        elif "shield_booster" in tid:
            ehp_bonus += 60.0 if tid.endswith("_ii") else (90.0 if tid.endswith("_iii") else 35.0)
        elif "armor_plate" in tid:
            ehp_bonus += 55.0 if tid.endswith("_ii") else (85.0 if tid.endswith("_iii") else 30.0)

    if total_dps <= 0.0:
        total_dps = 0.0
    else:
        total_dps *= (1.0 + 0.03 * wep_lvl + 0.015 * tac_lvl)

    ehp = max_hull * (1.0 + armor / 100.0) + max_shield * 1.15 + ehp_bonus
    power = math.sqrt(max(1.0, ehp) * max(1.0, total_dps)) * 10.0 if total_dps > 0 else 0.0
    return {
        "power": round(power, 1), "dps": round(total_dps, 1),
        "ehp": round(ehp, 1), "max_hull": max_hull, "max_shield": max_shield,
        "tier": tier, "weapons": wep_count, "max_reach": max_reach,
    }


def compute_target_threat(max_hull, max_shield=0.0, role="grazer", count_fighting=1, dps=None):
    """Scale-free Enemy Threat Score for grazers, predators, NPC pirates, or hostile packs."""
    r = str(role or "grazer").lower()
    if r == "pirate":
        role_mult = 2.0
    elif r in ("player", "hostile", "boss"):
        role_mult = 2.5
    elif r == "predator":
        role_mult = 1.5
    else:
        role_mult = 1.0
    n = max(1, int(count_fighting or 1))
    raw_ehp = max(20.0, (float(max_hull or 60.0) + float(max_shield or 0.0)) * n)
    edps = float(dps) if dps is not None else max(5.0, raw_ehp * (0.12 if r in ("pirate", "predator", "player") else 0.08))
    threat = math.sqrt(raw_ehp * edps) * 10.0 * role_mult
    return {"threat": round(threat, 1), "ehp": round(raw_ehp * role_mult, 1), "raw_ehp": round(raw_ehp, 1), "dps": round(edps, 1), "raw_hull": float(max_hull or 60.0)}


def f9_gauge(ship_doc, items):
    """(firepower, toughness) of one ship by gauges.py, the measure of rule F9; a weapon that fires ammunition
    (catalog `ammo_type`) counts only while the hold carries ammunition (an empty magazine fires nothing:
    Plasma Cannon II, 2026-11-22). None when gauges.py cannot be read."""
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import gauges
    except ImportError:
        return None
    cargo = ship_doc.get("cargo") or []
    if isinstance(cargo, dict):
        held = [k for k, v in cargo.items() if v]
    else:
        held = [str(c.get("item") or c.get("item_id") or c.get("id") or c.get("type") or "") if isinstance(c, dict) else str(c) for c in cargo]
    has_ammo = any((items.get(h) or {}).get("category") == "ammo" for h in held)
    mods = []
    for m in ship_doc.get("modules") or []:
        tid = str((m.get("type") or m.get("id") or "") if isinstance(m, dict) else m)
        if (items.get(tid) or {}).get("ammo_type") and not has_ammo:
            continue
        mods.append(m)
    found = gauges.gauges_of(dict(ship_doc, modules=mods), items)
    return (found["firepower"], found["toughness"])


def f9_passes(f9, prey_hull, role="grazer", n=1):
    """Rule F9 for a side of n ships of one gauge: (firepower, toughness) against a creature's hull and weight
    (a predator weighs twice its hull). True when f9 is None (no gauge read: the caller decides)."""
    if f9 is None:
        return True
    import gauges
    weight = float(prey_hull) * (gauges.PREDATOR_WEIGHT if str(role) == "predator" else 1)
    ok_f, ok_t = gauges.fits((n * f9[0], n * f9[1]), float(prey_hull), weight)
    return ok_f and ok_t


def passes_combat_gate(side_power_dict, target_threat_dict, min_power_ratio, check_f9=True):
    """Percentage combat-power ratio check (+ anti-glass-cannon DPS & EHP floor)."""
    if side_power_dict["power"] <= 0 or side_power_dict["dps"] <= 0:
        return False, 0.0
    ratio = side_power_dict["power"] / max(1.0, target_threat_dict["threat"])
    if ratio < float(min_power_ratio):
        return False, round(ratio, 2)
    if check_f9:
        raw_ehp = float(target_threat_dict.get("raw_ehp") or target_threat_dict["ehp"])
        if side_power_dict["dps"] * 8.0 < raw_ehp or side_power_dict["ehp"] < raw_ehp * 0.85:
            return False, round(ratio, 2)
    return True, round(ratio, 2)


def choose_pack_size(avg_member_power, target_threat_dict, min_power_ratio, sizes=(3, 5, 8, 10), f9=None, prey_hull=None, role="grazer"):
    """Choose smallest pack size from [3, 5, 8, 10] whose combined fighting power clears min_power_ratio & F9."""
    if avg_member_power["power"] <= 0 or avg_member_power["dps"] <= 0:
        return None
    for sz in sorted(int(s) for s in sizes if int(s) >= 2):
        # Combined fighting power scales linearly in both EHP and DPS -> Lanchester/total power ~ sz * member_power
        comb = {
            "power": avg_member_power["power"] * sz,
            "dps": avg_member_power["dps"] * sz,
            "ehp": avg_member_power["ehp"] * sz,
        }
        ok_g, _ratio = passes_combat_gate(comb, target_threat_dict, min_power_ratio, check_f9=True)
        if ok_g and (prey_hull is None or f9_passes(f9, prey_hull, role, n=sz)):
            return sz
    return None


def bfs_distances(adj, start_sys, max_hops=18):
    if not start_sys:
        return {}
    dist = {start_sys: 0}
    q = deque([start_sys])
    while q:
        u = q.popleft()
        d = dist[u]
        if d >= max_hops:
            continue
        for v in adj.get(u) or ():
            if v not in dist:
                dist[v] = d + 1
                q.append(v)
    return dist


def nearest_station(adj, stations_by_sys, sys_id, max_hops=6):
    dists = bfs_distances(adj, sys_id, max_hops=max_hops)
    for sid, hops in sorted(dists.items(), key=lambda kv: (kv[1], kv[0])):
        sts = stations_by_sys.get(sid)
        if sts:
            return hops, sts[0]
    return None, None


def load_combat_world(data_dir, repo_root, policy, now_t=None):
    """Load graph, systems, stations, herds, wildlife hull/pirate reads, ranches, pirates, needs, and loot values."""
    now_t = time.time() if now_t is None else float(now_t)
    db_path = Path(data_dir) / "store" / "read.db"
    adj, systems, stations_by_sys = {}, {}, {}
    herds = []
    pirates = set()
    pirate_details = {}
    ranch_pois = set()
    ranch_systems = set()
    species_hull = dict(DEFAULT_SPECIES_HULL)
    needs_items = set()
    species_loot_val = {}

    if db_path.exists():
        # Each table is read on its own: one query that fails (a column the store does not
        # have) must not leave the herds, the docks and the pirate reads empty with it.
        # (2026-11-24: `SELECT id, system, poi FROM stations` failed on the store's schema and
        # every pilot found 0 herds and 0 packs.)
        try:
            conn = sqlite3.connect("file:%s?mode=ro" % db_path, uri=True)
        except sqlite3.Error:
            conn = None
        if conn is not None:
            cur = conn.cursor()

            def _rows(sql, params=()):
                try:
                    return cur.execute(sql, params).fetchall()
                except sqlite3.Error as exc:
                    print("hunt_net: store read failed (%s): %s" % (exc, sql[:60]), file=sys.stderr, flush=True)
                    return []

            p_tags = set(str(x).upper() for x in (policy.get("partner_factions") or []))
            for a, b in _rows("SELECT a, b FROM lanes"):
                adj.setdefault(a, set()).add(b)
                adj.setdefault(b, set()).add(a)
            for sid, emp, sh in _rows("SELECT id, empire, stronghold FROM systems"):
                systems[sid] = {"empire": str(emp or "").lower(), "stronghold": bool(sh)}
            # Player stations (table stations: name, system, tag): a foreign one is no dock of
            # ours, and a partner's station marks its system as theirs (never hunted there).
            foreign_docks = set()
            for nm, sys_id, tag in _rows("SELECT name, system, tag FROM stations WHERE system IS NOT NULL"):
                tg = str(tag or "").upper()
                if tg and tg != "CLTV":
                    foreign_docks.add((str(sys_id), str(nm or "")))
                if tg in p_tags:
                    ranch_systems.add(str(sys_id))
            # An outpost of ours (table bases, kind outpost) is no dock: it has no storage for the loot and its
            # fuel bunker is a supply chain (requests.log ENT-513).
            outposts = {str(b) for (b,) in _rows("SELECT base FROM bases WHERE kind = 'outpost'") if b}
            # Docks: every place with a base (table places), our own stations and the empires'.
            for sys_id, poi_id, base_id, nm in _rows(
                "SELECT system, poi, base, name FROM places WHERE base IS NOT NULL AND base != '' ORDER BY system, poi"
            ):
                if (str(sys_id), str(nm or "")) in foreign_docks or str(base_id) in outposts:
                    continue
                stations_by_sys.setdefault(sys_id, []).append((sys_id, poi_id, base_id))
            for sys_id, poi_id, cr, name, role, cnt, ts in _rows(
                "SELECT system, poi, creature, name, role, count, t FROM herds WHERE count > 0"
            ):
                nm = str(name or "")
                if nm.startswith("[") and not nm.startswith("[CLTV]"):
                    ranch_pois.add("%s:%s" % (sys_id, poi_id))
                    continue
                herds.append({
                    "system": str(sys_id), "poi": str(poi_id), "species": str(cr),
                    "name": nm, "role": str(role or "grazer").lower(),
                    "count": int(cnt or 0), "t": float(ts or 0),
                })
            cutoff = now_t - float(policy.get("pirate_avoid_hours") or 6.0) * 3600.0
            for (subj,) in _rows("SELECT DISTINCT subject FROM observations WHERE kind = 'pirate' AND t >= ?", (cutoff,)):
                if subj:
                    pirates.add(str(subj))
            for (subj,) in _rows("SELECT DISTINCT subject FROM observations WHERE kind = 'ranch'"):
                if subj:
                    s_ = str(subj)
                    if ":" in s_:
                        ranch_pois.add(s_)
                        ranch_systems.add(s_.split(":")[0])
                    else:
                        ranch_systems.add(s_)
            conn.close()

    # Enrich live creature max_hull and pirate_list from recent wildlife files
    wdir = Path(data_dir) / "wildlife"
    if wdir.is_dir():
        for wp in wdir.glob("*.json"):
            try:
                if (now_t - wp.stat().st_mtime) > 24 * 3600:
                    continue
                wd = json.loads(wp.read_text(encoding="utf-8"))
                wsys = str(wd.get("system") or wp.stem)
                for pid, pinfo in (wd.get("pois") or {}).items():
                    if not isinstance(pinfo, dict):
                        continue
                    for c in pinfo.get("creatures") or []:
                        if not isinstance(c, dict):
                            continue
                        nm = str(c.get("name") or "")
                        if nm.startswith("[") and not nm.startswith("[CLTV]"):
                            ranch_pois.add("%s:%s" % (wsys, pid))
                        sp = str(c.get("species") or "")
                        mh = int(c.get("max_hull") or c.get("hull") or 0)
                        if sp and mh > 0:
                            species_hull[sp] = max(species_hull.get(sp, 0), mh)
                    plist = pinfo.get("pirate_list") or []
                    if isinstance(plist, list) and plist:
                        pirate_details["%s:%s" % (wsys, pid)] = plist
            except (OSError, ValueError):
                continue

    # Load open needs.tsv items for species drop priority boost
    needs_tsv = Path(repo_root) / "game" / "needs.tsv"
    if needs_tsv.exists():
        try:
            for ln in needs_tsv.read_text(encoding="ascii", errors="replace").splitlines()[1:]:
                cols = ln.split("\t")
                if len(cols) >= 5 and cols[0].strip() and not cols[0].startswith("#"):
                    st = cols[4].strip().lower()
                    if st not in ("done", "closed", "cancelled"):
                        if int(float(cols[2] or 0)) > int(float(cols[3] or 0)):
                            needs_items.add(cols[1].strip())
        except (OSError, ValueError):
            pass

    cd = read_json(Path(repo_root) / "game" / "craft-demand.json", {})
    craft_loot_species = {str(x).lower() for x in (cd.get("priority_loot_species") or [])} if isinstance(cd, dict) and cd.get("enabled", True) else set()
    for sp, hull in species_hull.items():
        # Rough value proxy scales super-linearly with creature hull/difficulty + need/craft multipliers
        base_v = 1200.0 + (hull ** 1.35) * 8.0
        drops = SPECIES_NEED_DROPS.get(sp) or ()
        if any(d in needs_items for d in drops):
            base_v *= 4.0
        elif sp.lower() in craft_loot_species:
            base_v *= 2.0
        species_loot_val[sp] = round(base_v, 1)
    owned_bases = []
    _db_b = Path(data_dir) / "store" / "read.db"
    if _db_b.is_file():
        try:
            c2 = sqlite3.connect("file:%s?mode=ro" % _db_b, uri=True, timeout=3.0)
            if "bases" in {r[0] for r in c2.execute("SELECT name FROM sqlite_master WHERE type='table'")}:
                for b_id, sys_id, poi_id, knd in c2.execute("SELECT base, system, poi, kind FROM bases WHERE system IS NOT NULL"):
                    owned_bases.append({"base": str(b_id), "system": str(sys_id), "poi": str(poi_id or b_id), "kind": str(knd or "outpost")})
            c2.close()
        except sqlite3.Error:
            pass

    return {
        "adj": adj, "systems": systems, "stations_by_sys": stations_by_sys,
        "herds": herds, "pirates": pirates, "pirate_details": pirate_details,
        "ranch_pois": ranch_pois, "ranch_systems": ranch_systems,
        "species_hull": species_hull, "needs_items": needs_items,
        "species_loot_val": species_loot_val, "owned_bases": owned_bases,
        "craft_loot_species": craft_loot_species,
    }



def detect_war_posture(data_dir, policy=None):
    """Return (war_active: bool, enemy_tags: set[str]). Strictly False in peacetime (F2 RoE)."""
    wcfg = (policy or {}).get("war_wing") if isinstance(policy, dict) else {}
    if isinstance(wcfg, dict) and not wcfg.get("enabled", True):
        return False, set()
    tags = set()
    # 1. Explicit war-posture flag (set only on Suggi's war declaration)
    flag_p = Path(data_dir) / "fleet" / "war-posture-on"
    flag_on = flag_p.is_file()
    if flag_on:
        try:
            for ln in flag_p.read_text(encoding="utf-8", errors="replace").splitlines():
                t = ln.strip().upper()
                if t and not t.startswith("#"):
                    tags.add(t)
        except OSError:
            pass
    # 2. Live faction war state in empire.json
    emp = read_json(Path(data_dir) / "empire" / "empire.json", {})
    fac = emp.get("faction") if isinstance(emp.get("faction"), dict) else {}
    wars = list(fac.get("wars") or emp.get("wars") or [])
    for w in wars:
        tg = str(w.get("tag") or w.get("faction") or w).upper() if isinstance(w, dict) else str(w).upper()
        if tg:
            tags.add(tg)
    at_war = bool(fac.get("at_war") or emp.get("at_war") or wars or flag_on)
    return at_war, tags


def pick_war_assignment(pilot, ship_doc, spow, world, policy, claims, enemy_tags, data_dir=None):
    """Dormant Lane 0 War Wing selector (active ONLY when war_active=True).

    Priority 0A: Base Defense fleets (up to 10 ships/base) guarding our owned stations/outposts.
    Priority 0B: Armed Convoy Escorts for civilians in threatened/lawless systems.
    """
    wcfg = (policy or {}).get("war_wing") or {}
    if not wcfg.get("enabled", True):
        return None
    min_pow = float(wcfg.get("min_power") or 300.0)
    if float((spow or {}).get("power") or 0) < min_pow:
        return None
    # Priority 0A: Protect owned Collective bases (read.db:bases)
    bases = list(world.get("owned_bases") or [])
    max_per_base = int(wcfg.get("defenders_per_base") or 10)
    active_by_key = {}
    for _p, rec in (claims or {}).items():
        if isinstance(rec, dict) and rec.get("mode") == "war_defense":
            k = str(rec.get("key") or "")
            active_by_key[k] = active_by_key.get(k, 0) + 1
    p_sys = str(ship_doc.get("system") or "")
    adj = world.get("adj") or {}
    dists = bfs_distances(adj, p_sys, max_hops=int(wcfg.get("max_jumps") or 20)) if p_sys else {}
    best = None
    for b in bases:
        sys_id, poi_id, base_id, kind = b["system"], b["poi"], b["base"], b["kind"]
        key = "war_def:%s:%s" % (sys_id, poi_id)
        if active_by_key.get(key, 0) >= max_per_base:
            continue
        hops = dists.get(sys_id, 99) if p_sys else 0
        if hops > int(wcfg.get("max_jumps") or 20):
            continue
        prio = 120 if kind == "station" else 100
        cand = {
            "key": key, "mode": "war_defense", "system": sys_id, "poi": poi_id,
            "station": "%s:%s:%s" % (sys_id, poi_id, base_id),
            "guards": "war-base-%s" % kind, "hops": hops, "priority": prio - hops,
            "enemy_tags": sorted(enemy_tags),
        }
        if best is None or cand["priority"] > best["priority"]:
            best = cand
    return best


def detect_escort_demands(data_dir, world, policy, claims, now_t=None):
    """Find active civilian ships or configured sites needing Military escort/protection right now."""
    now_t = time.time() if now_t is None else float(now_t)
    ecfg = policy.get("escort") or {}
    if not ecfg.get("enabled", True):
        return []
    demands = []
    seen_keys = set()
    claimed_keys = {rec.get("key") for rec in (claims or {}).values() if isinstance(rec, dict) and rec.get("lane") == "escort"}

    # 1. Explicit configured places
    for pl in ecfg.get("protect_places") or []:
        if not isinstance(pl, str) or ":" not in pl:
            continue
        key = "escort:place:" + pl
        if key in claimed_keys or key in seen_keys:
            continue
        seen_keys.add(key)
        sys_id, poi_id = pl.split(":", 1)
        demands.append({"key": key, "mode": "place", "system": sys_id, "poi": poi_id, "guards": "outpost", "priority": 100})

    # 2. Explicit configured pilots + auto-detected lawless/pirate-threatened civilians
    explicit_pilots = set(str(x) for x in (ecfg.get("protect_pilots") or []))
    auto_lawless = bool(ecfg.get("auto_protect_lawless_civilians", True))
    systems = world["systems"]
    pirates = world["pirates"]

    ships_dir = Path(data_dir) / "fleet" / "ships"
    orders_dir = Path(data_dir) / "fleet" / "orders"
    if ships_dir.is_dir():
        for sp in sorted(ships_dir.glob("*.json")):
            sd = read_json(sp, {})
            pname = str(sd.get("name") or sp.stem)
            role = pname.split("-")[0]
            if role not in ("miner", "hauler", "trader"):
                continue
            psys = str(sd.get("system") or "")
            ppoi = str(sd.get("poi") or "")
            if not psys or sd.get("docked"):
                continue
            ord_doc = read_json(orders_dir / (pname + ".json"), {})
            what = str(ord_doc.get("what") or "")
            if not what:
                continue
            parts = what.split(" ", 1)
            okind, orid = parts[0], (parts[1] if len(parts) > 1 else "")
            if okind not in ("mine", "mine_net", "circuit", "haul"):
                continue
            is_lawless = not bool((systems.get(psys) or {}).get("empire"))
            in_pirate_sys = psys in pirates
            if pname in explicit_pilots or (auto_lawless and (in_pirate_sys or is_lawless)):
                key = "escort:pilot:" + pname
                if key in claimed_keys or key in seen_keys:
                    continue
                seen_keys.add(key)
                demands.append({
                    "key": key, "mode": "follow", "follow": pname,
                    "system": psys, "poi": ppoi or psys, "guards": orid or okind,
                    "priority": 90 if (pname in explicit_pilots or in_pirate_sys) else 60,
                })
    demands.sort(key=lambda d: (-d["priority"], d["key"]))
    return demands


def _read_claims_unlocked(path, now_t, ttl_s):
    doc = read_json(path, {})
    raw_c = doc.get("claims") if isinstance(doc, dict) and isinstance(doc.get("claims"), dict) else {}
    raw_cd = doc.get("cooldowns") if isinstance(doc, dict) and isinstance(doc.get("cooldowns"), dict) else {}
    claims = {str(p): r for p, r in raw_c.items() if isinstance(r, dict) and (now_t - float(r.get("at") or 0)) <= ttl_s and r.get("key")}
    cooldowns = {str(k): float(v) for k, v in raw_cd.items() if float(v or 0) > now_t}
    return claims, cooldowns


def load_hunt_claims(data_dir, policy, now_t=None):
    now_t = time.time() if now_t is None else float(now_t)
    return _read_claims_unlocked(Path(data_dir) / "fleet" / "hunt_claims.json", now_t, float(policy.get("claim_ttl_s") or 4200))


def claim_hunt_key_atomic(data_dir, pilot, key, lane, policy, max_per_key=1, now_t=None):
    now_t = time.time() if now_t is None else float(now_t)
    ttl_s = float(policy.get("claim_ttl_s") or 4200)
    fdir = Path(data_dir) / "fleet"
    fdir.mkdir(parents=True, exist_ok=True)
    lock_p, path = fdir / "hunt_claims.lock", fdir / "hunt_claims.json"
    with open(lock_p, "a+", encoding="utf-8") as lf:
        fcntl.flock(lf, fcntl.LOCK_EX)
        try:
            claims, cooldowns = _read_claims_unlocked(path, now_t, ttl_s)
            if cooldowns.get(key, 0) > now_t:
                return False
            claims.pop(str(pilot), None)
            cur_n = sum(1 for r in claims.values() if r.get("key") == key)
            if cur_n >= max(1, int(max_per_key)):
                return False
            claims[str(pilot)] = {"key": key, "lane": lane, "at": int(now_t)}
            write_json(path, {"updated_at": int(now_t), "claims": claims, "cooldowns": cooldowns})
            return True
        finally:
            fcntl.flock(lf, fcntl.LOCK_UN)


def release_hunt_claim(data_dir, pilot, cooldown_key=None, cooldown_minutes=90, policy=None, now_t=None):
    now_t = time.time() if now_t is None else float(now_t)
    ttl_s = float((policy or DEFAULT_POLICY).get("claim_ttl_s") or 4200)
    fdir = Path(data_dir) / "fleet"
    fdir.mkdir(parents=True, exist_ok=True)
    lock_p, path = fdir / "hunt_claims.lock", fdir / "hunt_claims.json"
    with open(lock_p, "a+", encoding="utf-8") as lf:
        fcntl.flock(lf, fcntl.LOCK_EX)
        try:
            claims, cooldowns = _read_claims_unlocked(path, now_t, ttl_s)
            claims.pop(str(pilot), None)
            if cooldown_key and float(cooldown_minutes or 0) > 0:
                cooldowns[str(cooldown_key)] = now_t + float(cooldown_minutes) * 60.0
            write_json(path, {"updated_at": int(now_t), "claims": claims, "cooldowns": cooldowns})
        finally:
            fcntl.flock(lf, fcntl.LOCK_UN)


def score_solo_herds(pilot_info, ship_power, world, policy, claims, cooldowns, now_t=None, f9=None):
    """Score all eligible wild grazer herds for solo hunting, gated by percentage combat power ratio."""
    now_t = time.time() if now_t is None else float(now_t)
    scfg = policy.get("solo") or {}
    if not scfg.get("enabled", True) or ship_power["power"] <= 0:
        return []
    p_sys = str(pilot_info.get("system") or "")
    p_name = str(pilot_info.get("name") or "")
    max_j = int(scfg.get("max_jumps") or 10)
    min_ratio = float(scfg.get("min_power_ratio") or 1.35)
    ideal_lo = float(scfg.get("ideal_ratio_low") or 1.45)
    ideal_hi = float(scfg.get("ideal_ratio_high") or 3.20)
    min_cr = max(int(policy.get("keep_herd") or 2) + 1, int(policy.get("min_creatures") or 3))
    policed_only = bool(policy.get("policed_only", False))
    allow_lawless_p = float(policy.get("allow_lawless_min_power") or 350.0)
    excl_sys = set(str(x) for x in (policy.get("exclude_systems") or []))
    excl_pois = set(str(x) for x in (policy.get("exclude_pois") or []))
    excl_sp = set(str(x) for x in (policy.get("exclude_species") or []))

    adj = world["adj"]
    systems = world["systems"]
    pirates = world["pirates"]
    ranch_pois = world["ranch_pois"]
    ranch_sys = world["ranch_systems"]
    stations_by_sys = world["stations_by_sys"]
    species_hull = world["species_hull"]
    species_loot = world["species_loot_val"]

    dists = bfs_distances(adj, p_sys, max_hops=max_j) if p_sys else {}
    busy_keys = {r.get("key") for cp, r in (claims or {}).items() if cp != p_name and r.get("key")}

    out = []
    for h in world["herds"]:
        if h["role"] != "grazer" or h["count"] < min_cr:
            continue
        sys_id, poi_id, sp = h["system"], h["poi"], h["species"]
        place_key = "%s:%s" % (sys_id, poi_id)
        if sys_id in excl_sys or sys_id in pirates or sys_id in ranch_sys:
            continue
        if place_key in excl_pois or poi_id in excl_pois or place_key in ranch_pois or sp in excl_sp:
            continue
        if place_key in busy_keys or cooldowns.get(place_key, 0) > now_t:
            continue
        smeta = systems.get(sys_id, {})
        if smeta.get("stronghold"):
            continue
        is_policed = bool(smeta.get("empire"))
        if not is_policed and (policed_only or ship_power["power"] < allow_lawless_p):
            continue
        hops = dists.get(sys_id) if p_sys else 0
        if hops is None or hops > max_j:
            continue

        prey_hull = float(species_hull.get(sp) or 70.0)
        threat = compute_target_threat(prey_hull, role="grazer", count_fighting=1)
        ok_g, ratio = passes_combat_gate(ship_power, threat, min_ratio, check_f9=True)
        if not ok_g or not f9_passes(f9, prey_hull, "grazer", n=1):
            continue

        st_hops, st_tup = nearest_station(adj, stations_by_sys, sys_id, max_hops=5)
        if not st_tup:
            continue

        # Sweet-spot multiplier: encourages strong T2/T3/T4 hulls to graduate up to tougher high-value herds
        if ideal_lo <= ratio <= ideal_hi:
            fit_mult = 1.35
        elif ratio > ideal_hi:
            fit_mult = max(0.55, 1.0 - 0.08 * (ratio - ideal_hi))
        else:
            fit_mult = 1.0

        kills_avail = max(1, min(int(scfg.get("kills_per_run") or 6), h["count"] - int(policy.get("keep_herd") or 2)))
        loot_est = float(species_loot.get(sp) or 2000.0) * kills_avail
        fuel_est = 90.0 * (hops + st_hops) * (1.0 + 0.5 * ship_power["tier"])
        score = ((loot_est * fit_mult) - fuel_est) / (1.0 + 0.7 * hops + 0.8 * st_hops)
        out.append({
            "key": place_key, "system": sys_id, "poi": poi_id, "species": sp,
            "count": h["count"], "kills": kills_avail, "prey_hull": int(prey_hull),
            "ratio": ratio, "hops": hops, "st_hops": st_hops,
            "sell_at": "%s:%s:%s" % st_tup, "score": round(score, 1),
        })
    out.sort(key=lambda c: (-c["score"], c["hops"], c["key"]))
    return out


def score_pack_targets(pilot_info, ship_power, world, policy, claims, cooldowns, now_t=None, f9=None):
    """Discover tough wildlife herds & pirate systems suited for 3/5/8/10-ship packs."""
    now_t = time.time() if now_t is None else float(now_t)
    pcfg = policy.get("packs") or {}
    if not pcfg.get("enabled", True) or ship_power["power"] < float(pcfg.get("min_member_power") or 420.0):
        return []
    p_sys = str(pilot_info.get("system") or "")
    max_j = int(pcfg.get("max_jumps") or 12)
    sizes = tuple(int(s) for s in (pcfg.get("sizes") or [3, 5, 8, 10]))
    wild_ratio = float(pcfg.get("min_power_ratio") or 1.80)
    pir_ratio = float(pcfg.get("pirate_min_power_ratio") or 2.20)
    min_thull = int(pcfg.get("min_target_hull") or 80)
    prio_sp = set(str(x) for x in (pcfg.get("priority_species") or []))
    min_cr = max(int(policy.get("keep_herd") or 2) + 1, int(policy.get("min_creatures") or 3))
    excl_sys = set(str(x) for x in (policy.get("exclude_systems") or []))
    excl_pois = set(str(x) for x in (policy.get("exclude_pois") or []))
    ranch_pois = world["ranch_pois"]
    ranch_sys = world["ranch_systems"]
    systems = world["systems"]
    adj = world["adj"]
    stations_by_sys = world["stations_by_sys"]
    species_hull = world["species_hull"]
    species_loot = world["species_loot_val"]

    dists = bfs_distances(adj, p_sys, max_hops=max_j) if p_sys else {}
    busy_keys = {r.get("key") for r in (claims or {}).values() if r.get("key")}
    cands = []

    # A. Tough Wildlife / Predator Pack Targets
    for h in world["herds"]:
        sys_id, poi_id, sp, role = h["system"], h["poi"], h["species"], h["role"]
        place_key = "%s:%s" % (sys_id, poi_id)
        if role == "grazer" and h["count"] < min_cr:
            continue
        if sys_id in excl_sys or sys_id in ranch_sys or place_key in excl_pois or place_key in ranch_pois:
            continue
        if sys_id in world["pirates"] or place_key in busy_keys or cooldowns.get(place_key, 0) > now_t:
            continue
        if (systems.get(sys_id) or {}).get("stronghold"):
            continue
        hops = dists.get(sys_id) if p_sys else 0
        if hops is None or hops > max_j:
            continue
        prey_hull = float(species_hull.get(sp) or 90.0)
        if prey_hull < min_thull and sp not in prio_sp and role != "predator":
            continue
        threat = compute_target_threat(prey_hull, role=role, count_fighting=1)
        sz = choose_pack_size(ship_power, threat, wild_ratio, sizes=sizes, f9=f9, prey_hull=prey_hull, role=role)
        if sz is None:
            continue
        st_hops, st_tup = nearest_station(adj, stations_by_sys, sys_id, max_hops=6)
        if not st_tup:
            continue
        loot_v = float(species_loot.get(sp) or 4000.0) * (1.8 if sp in prio_sp else 1.0) * (1.5 if role == "predator" else 1.0)
        score = (loot_v * (prey_hull / 60.0)) / (1.0 + 0.6 * hops + 0.5 * st_hops)
        cands.append({
            "key": "pack:" + place_key, "place_key": place_key, "mode": "wildlife",
            "system": sys_id, "poi": poi_id, "species": sp, "role": role,
            "prey_hull": int(prey_hull), "desired_size": sz, "threat": threat["threat"],
            "hops": hops, "dock": "%s:%s:%s" % st_tup, "score": round(score, 1),
        })

    # B. Pirate Pack Raids (when enabled in policy)
    if pcfg.get("pirates_enabled", True):
        allowed_tiers = set(str(x).lower() for x in (pcfg.get("pirate_tiers") or ["scout", "raider"]))
        for pkey, plist in (world.get("pirate_details") or {}).items():
            if ":" not in pkey or len(plist) != 1:
                continue
            sys_id, poi_id = pkey.split(":", 1)
            if sys_id in excl_sys or sys_id in ranch_sys or pkey in excl_pois:
                continue
            if (systems.get(sys_id) or {}).get("stronghold"):
                continue
            if ("pack:" + pkey) in busy_keys or cooldowns.get("pack:" + pkey, 0) > now_t:
                continue
            hops = dists.get(sys_id) if p_sys else 0
            if hops is None or hops > max_j:
                continue
            pir = plist[0]
            ptier = str(pir.get("tier") or "").lower()
            if allowed_tiers and ptier and ptier not in allowed_tiers:
                continue
            phull = float(pir.get("max_hull") or pir.get("hull") or 100.0)
            pshield = float(pir.get("max_shield") or pir.get("shield") or 40.0)
            threat = compute_target_threat(phull, pshield, role="pirate", count_fighting=1)
            sz = choose_pack_size(ship_power, threat, pir_ratio, sizes=sizes, f9=f9, prey_hull=2 * phull + pshield, role="grazer")
            if sz is None:
                continue
            st_hops, st_tup = nearest_station(adj, stations_by_sys, sys_id, max_hops=6)
            if not st_tup:
                continue
            score = (18000.0 * (phull / 80.0)) / (1.0 + 0.6 * hops + 0.5 * st_hops)
            cands.append({
                "key": "pack:" + pkey, "place_key": pkey, "mode": "pirate",
                "system": sys_id, "poi": poi_id, "species": "pirate_" + (ptier or "npc"),
                "role": "pirate", "prey_hull": int(phull), "desired_size": sz,
                "threat": threat["threat"], "hops": hops, "dock": "%s:%s:%s" % st_tup,
                "score": round(score, 1),
            })

    cands.sort(key=lambda c: (-c["score"], c["hops"], c["key"]))
    return cands


def assign_optimal_hunts(pilots_info, weapon_cat, booster_cat, world, policy, claims, cooldowns, now_t=None):
    """Global greedy optimal 1-to-1 assignment of available solo hunters -> herds."""
    now_t = time.time() if now_t is None else float(now_t)
    triples = []
    for pinfo in pilots_info:
        pname = str(pinfo.get("name") or "")
        spow = compute_ship_power(pinfo, weapon_cat, booster_cat)
        for c in score_solo_herds(pinfo, spow, world, policy, claims, cooldowns, now_t=now_t)[:20]:
            triples.append((c["score"], -c["hops"], pname, c))
    triples.sort(key=lambda x: (-x[0], -x[1], x[2], x[3]["key"]))
    assigned, used_keys = {}, set()
    for _sc, _nh, pname, cand in triples:
        if pname in assigned or cand["key"] in used_keys:
            continue
        assigned[pname] = cand
        used_keys.add(cand["key"])
    return assigned


# --- Atomic Pack Coordination State Machine (hunt_packs.json) ---

def _clean_packs(packs, now_t):
    out = {}
    for pid, pk in (packs or {}).items():
        if not isinstance(pk, dict):
            continue
        st = pk.get("state")
        if st == "forming" and float(pk.get("expires_at") or 0) <= now_t:
            continue
        if st in ("launched", "fighting") and (now_t - float(pk.get("updated_at") or 0)) > 3600:
            continue
        if st in ("done", "aborted") and (now_t - float(pk.get("updated_at") or 0)) > 300:
            continue
        out[str(pid)] = pk
    return out


def pack_try_join_or_create(data_dir, pilot, ship_sys, ship_power, pack_targets, world, policy, active_military_n, now_t=None):
    """Atomically join a nearby forming pack or create a new pack if under target_share (20-30%)."""
    now_t = time.time() if now_t is None else float(now_t)
    pcfg = policy.get("packs") or {}
    if not pcfg.get("enabled", True):
        return None
    target_share = float(pcfg.get("target_share") or 0.25)
    cmd_ships = load_command_flagships(data_dir)
    is_cmd = str(pilot) in cmd_ships
    min_mem_p = float(pcfg.get("command_flagship_min_power") or 150.0) if is_cmd else float(pcfg.get("min_member_power") or 420.0)
    if ship_power["power"] < min_mem_p:
        return None
    rally_max_j = int(pcfg.get("rally_max_jumps") or 8)
    rally_ttl = float(pcfg.get("rally_timeout_s") or 150)

    fdir = Path(data_dir) / "fleet"
    fdir.mkdir(parents=True, exist_ok=True)
    lock_p, path = fdir / "hunt_packs.lock", fdir / "hunt_packs.json"
    dists = bfs_distances(world["adj"], ship_sys, max_hops=rally_max_j) if ship_sys else {}

    with open(lock_p, "a+", encoding="utf-8") as lf:
        fcntl.flock(lf, fcntl.LOCK_EX)
        try:
            doc = read_json(path, {})
            packs = _clean_packs(doc.get("packs") if isinstance(doc, dict) else {}, now_t)

            # Remove pilot from any stale pack first
            for pk in packs.values():
                if pilot in (pk.get("members") or []):
                    pk["members"] = [m for m in pk["members"] if m != pilot]

            # Count active pack pilots
            in_packs = sum(len(pk.get("members") or []) for pk in packs.values() if pk.get("state") in ("forming", "launched", "fighting"))
            quota = max(3, int(round(max(12, active_military_n) * target_share)))

            # 1. Prefer joining an existing forming pack within rally_max_jumps
            # Command Support Flagships prioritize larger packs (>=10 allow 2 support flagships, <10 allow 1) and take Pack Leader for leadership bonuses!
            sort_key = (
                (lambda kv: (-int(kv[1].get("desired_size") or 3), -len(kv[1].get("members") or []), kv[0]))
                if is_cmd
                else (lambda kv: (-len(kv[1].get("members") or []), kv[0]))
            )
            for pid, pk in sorted(packs.items(), key=sort_key):
                if pk.get("state") != "forming":
                    continue
                dsz = int(pk.get("desired_size") or 3)
                if len(pk.get("members") or []) >= dsz:
                    continue
                if ship_sys and pk.get("system") not in dists:
                    continue
                if is_cmd:
                    cur_cmds = sum(1 for m in (pk.get("members") or []) if m in cmd_ships)
                    max_cmds = 2 if dsz >= 10 else 1
                    if cur_cmds >= max_cmds:
                        continue
                pk["members"].append(pilot)
                if is_cmd and str(pk.get("leader") or "") not in cmd_ships:
                    pk["leader"] = pilot
                pk["updated_at"] = int(now_t)
                if len(pk["members"]) >= dsz:
                    pk["state"] = "launched"
                write_json(path, {"updated_at": int(now_t), "packs": packs})
                return dict(pk, pack_id=pid)

            # 2. Otherwise create a new forming pack if under pack quota and targets exist
            if in_packs >= quota or not pack_targets:
                write_json(path, {"updated_at": int(now_t), "packs": packs})
                return None

            used_targets = {pk.get("target_key") for pk in packs.values() if pk.get("state") in ("forming", "launched", "fighting")}
            chosen = next((t for t in pack_targets if t["key"] not in used_targets), None)
            if not chosen:
                write_json(path, {"updated_at": int(now_t), "packs": packs})
                return None

            pid = "pk-%d-%s" % (int(now_t), pilot.replace("-", ""))
            pk = {
                "pack_id": pid, "state": "forming", "leader": pilot,
                "members": [pilot], "desired_size": int(chosen["desired_size"]),
                "mode": chosen["mode"], "target_key": chosen["key"],
                "place_key": chosen["place_key"], "system": chosen["system"],
                "poi": chosen["poi"], "species": chosen["species"],
                "prey_hull": int(chosen["prey_hull"]), "dock": chosen["dock"],
                "arrived": {}, "target_id": "", "flee": False, "flee_reason": "",
                "created_at": int(now_t), "updated_at": int(now_t),
                "expires_at": int(now_t + rally_ttl),
            }
            packs[pid] = pk
            write_json(path, {"updated_at": int(now_t), "packs": packs})
            return dict(pk)
        finally:
            fcntl.flock(lf, fcntl.LOCK_UN)


def pack_update(data_dir, pack_id, mutator, now_t=None):
    now_t = time.time() if now_t is None else float(now_t)
    fdir = Path(data_dir) / "fleet"
    lock_p, path = fdir / "hunt_packs.lock", fdir / "hunt_packs.json"
    with open(lock_p, "a+", encoding="utf-8") as lf:
        fcntl.flock(lf, fcntl.LOCK_EX)
        try:
            doc = read_json(path, {})
            packs = _clean_packs(doc.get("packs") if isinstance(doc, dict) else {}, now_t)
            pk = packs.get(pack_id)
            if pk is None:
                return None
            mutator(pk)
            pk["updated_at"] = int(now_t)
            write_json(path, {"updated_at": int(now_t), "packs": packs})
            return dict(pk)
        finally:
            fcntl.flock(lf, fcntl.LOCK_UN)


# --- Gate HTTP helpers for Pack Execution ---

def _gate_call(method, path, body_obj=None, timeout=60):
    data = None if body_obj is None else json.dumps(body_obj).encode()
    req = urllib.request.Request(GATE + path, data=data, method=method, headers={"Content-Type": "application/json"} if data else {})
    try:
        with OPENER.open(req, timeout=timeout) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8", "replace") or "{}")
    except urllib.error.HTTPError as err:
        try:
            return err.code, json.loads(err.read().decode("utf-8", "replace") or "{}")
        except ValueError:
            return err.code, {"error": str(err)}
    except Exception as err:
        return 0, {"error": str(err)}


def _raw(pilot, action, params=None, group="spacemolt"):
    q = urllib.parse.quote(pilot, safe="")
    st, ans = _gate_call("POST", "/accounts/%s/raw" % q, {"toolGroup": group, "action": action, "params": params or {}})
    sc = ans.get("structuredContent") if isinstance(ans, dict) and isinstance(ans.get("structuredContent"), dict) else {}
    return st, sc, ans


def _goal(pilot, gtype, opts, timeout_s=240):
    q = urllib.parse.quote(pilot, safe="")
    st, ans = _gate_call("POST", "/accounts/%s/goal" % q, {"goalType": gtype, "goalOptions": opts}, timeout=30)
    if st not in (200, 201) or "error" in ans:
        return False
    end_t = time.time() + timeout_s
    while time.time() < end_t and not (DATA / "fleet" / "STOP").exists():
        time.sleep(8)
        _, acc = _gate_call("GET", "/accounts/" + q, timeout=20)
        if not acc.get("hasExecutingGoal"):
            return True
    return False


def _foreign_ranched(c):
    nm = str(c.get("name") or "")
    return nm.startswith("[") and not nm.startswith("[CLTV]")


def run_pack_mission(pilot, pack, policy, order_path, route_id):
    """Execute synchronized 3/5/8/10-ship pack combat using proven spacemolt_fleet + outside battle-join protocol."""
    pcfg = policy.get("packs") or {}
    pid = pack["pack_id"]
    is_leader = (pack["leader"] == pilot)
    q = urllib.parse.quote(pilot, safe="")
    rally_end = float(pack.get("expires_at") or (time.time() + 150))

    # 1. Wait for pack to fill & launch
    cur = pack
    while cur and cur.get("state") == "forming" and time.time() < rally_end and not (DATA / "fleet" / "STOP").exists():
        time.sleep(5)
        try:
            os.utime(order_path)
        except OSError:
            pass
        cur = pack_update(DATA, pid, lambda _p: None)
    if not cur or cur.get("state") != "launched":
        # Rally timed out cleanly -- caller falls through to Solo Hunt with zero idle time!
        pack_update(DATA, pid, lambda p: p.update(state="aborted") if p.get("state") == "forming" else None)
        return "rally_timeout"

    members = list(cur.get("members") or [])
    my_idx = members.index(pilot) if pilot in members else 99
    dock = cur["dock"].split(":")
    is_pirate = (cur["mode"] == "pirate")
    keep_herd = int(policy.get("keep_herd") or 2)
    flee_hull = int(pcfg.get("flee_hull_pct") or 80)
    close_dist = int(pcfg.get("close_dist") or 2)
    fight_ticks = int(pcfg.get("fight_ticks") or 45)
    arrive_timeout = float(pcfg.get("arrive_timeout_s") or 240)
    ranch_floor_hit = False
    started = time.time()

    try:
        # 2. Prepare: repair/refuel, set default_stance fire & combat_mode external
        _goal(pilot, "prepare-at-station", {"systemId": dock[0], "poiId": dock[1], "baseId": dock[2], "refuel": True}, timeout_s=180)
        _raw(pilot, "default_stance", {"stance": "fire"}, "spacemolt_battle")
        _gate_call("PATCH", "/accounts/%s/combat-mode" % q, {"mode": "external"})
        time.sleep(11)

        # 3. Game Fleet for first 3 (indices 0, 1, 2); members 3..9 fly directly and join battle by target_id
        if is_leader:
            _raw(pilot, "create", {}, "spacemolt_fleet")
            time.sleep(11)
            for m in members[1:3]:
                _raw(pilot, "invite", {"player_id": m}, "spacemolt_fleet")
                time.sleep(11)
        elif my_idx in (1, 2):
            time.sleep(12 * my_idx)
            _raw(pilot, "accept", {}, "spacemolt_fleet")
            time.sleep(11)

        # 4. Travel to target system:poi and mark arrived
        _goal(pilot, "navigate-to-system", {"targetSystemId": cur["system"]}, timeout_s=arrive_timeout)
        _goal(pilot, "go-to-poi", {"targetPoiId": cur["poi"]}, timeout_s=90)
        cur = pack_update(DATA, pid, lambda p: p.setdefault("arrived", {}).__setitem__(pilot, True))

        # Wait for pack arrival
        wait_end = time.time() + min(120.0, arrive_timeout)
        min_ready = max(2, int(math.ceil(len(members) * 0.75)))
        while cur and len(cur.get("arrived") or {}) < len(members) and time.time() < wait_end and not (DATA / "fleet" / "STOP").exists():
            time.sleep(6)
            cur = pack_update(DATA, pid, lambda _p: None)
        if not cur or len(cur.get("arrived") or {}) < min_ready:
            if is_leader:
                pack_update(DATA, pid, lambda p: p.update(state="aborted", flee=True, flee_reason="arrival timeout"))
            return "pack_aborted"

        # 5. Snapshot pre-existing wrecks & engage target
        _, wr_before, _ = _raw(pilot, "wrecks", {}, "spacemolt_salvage")
        before_ids = {w.get("id") for w in (wr_before.get("wrecks") or []) if isinstance(w, dict)}

        target_id = ""
        if is_leader:
            _, near, _ = _raw(pilot, "get_nearby", {}, "spacemolt")
            if is_pirate:
                pirs = [x for x in (near.get("pirates") or []) if isinstance(x, dict) and not x.get("in_combat")]
                if len(pirs) == 1:
                    target_id = str(pirs[0].get("pirate_id") or pirs[0].get("id") or pirs[0].get("npc_id") or "")
            else:
                if not near.get("pirate_count"):
                    prey = [c for c in (near.get("creatures") or []) if isinstance(c, dict)
                            and not c.get("in_combat") and not _foreign_ranched(c)
                            and c.get("species") == cur["species"]
                            and int(c.get("max_hull") or c.get("hull") or 0) <= int(cur["prey_hull"] * 1.25)]
                    hurt = [c for c in prey if int(c.get("hull") or 0) < int(c.get("max_hull") or c.get("hull") or 0)]
                    if not hurt and cur.get("mode") == "wildlife" and keep_herd > 0 and len(prey) <= keep_herd:
                        ranch_floor_hit = True
                    elif prey:
                        chosen_t = min(hurt or prey, key=lambda c: (int(c.get("hull") or 0), str(c.get("creature_id"))))
                        target_id = str(chosen_t.get("creature_id") or "")
            if not target_id:
                pack_update(DATA, pid, lambda p: p.update(state="done", flee=True, flee_reason=("ranch floor" if ranch_floor_hit else "no target")))
                return "ranch_floor" if ranch_floor_hit else "no_target"
            pack_update(DATA, pid, lambda p: p.update(state="fighting", target_id=target_id))
            _raw(pilot, "attack" if is_pirate else "hunt", {"target_id": target_id}, "spacemolt")
            time.sleep(10)
        else:
            t_wait = time.time() + 45.0
            while time.time() < t_wait:
                cur = pack_update(DATA, pid, lambda _p: None)
                if not cur or cur.get("state") in ("done", "aborted"):
                    return "no_target"
                if cur.get("target_id"):
                    target_id = str(cur["target_id"])
                    break
                time.sleep(4)
            if not target_id:
                return "no_target"

        # 6. Synchronized tick-by-tick combat loop
        joined_sent = False
        fired_stance = False
        for tick in range(fight_ticks + 15):
            if (DATA / "fleet" / "STOP").exists():
                pack_update(DATA, pid, lambda p: p.update(flee=True, flee_reason="STOP"))
            _gate_call("POST", "/accounts/%s/combat-heartbeat" % q, {}, timeout=20)
            _, bsc, bans = _raw(pilot, "status", {}, "spacemolt_battle")
            in_b = bool(bsc.get("is_participant"))
            if not in_b and not is_leader and not joined_sent and tick <= 3:
                _raw(pilot, "attack" if is_pirate else "hunt", {"target_id": target_id}, "spacemolt")
                joined_sent = True
                time.sleep(10)
                continue
            if not in_b and tick >= 2:
                break
            cur = pack_update(DATA, pid, lambda _p: None) or {}
            # Check own hull/shield from live ship file
            sd = read_json(DATA / "fleet" / "ships" / ship_file_name(pilot), {})
            mh = max(1.0, float(sd.get("max_hull") or 100.0))
            hp_pct = 100.0 * float(sd.get("hull") or mh) / mh
            sh_cur = float(sd.get("shield") if sd.get("shield") is not None else 1.0)
            if (hp_pct < flee_hull or sh_cur <= 0 or tick >= fight_ticks) and not cur.get("flee"):
                pack_update(DATA, pid, lambda p: p.update(flee=True, flee_reason="%s low hp/shield" % pilot))
                cur["flee"] = True
            if cur.get("flee"):
                _raw(pilot, "stance", {"stance": "flee"}, "spacemolt_battle")
            else:
                if not is_leader and not fired_stance:
                    _raw(pilot, "stance", {"stance": "fire"}, "spacemolt_battle")
                    _raw(pilot, "target", {"target_id": target_id}, "spacemolt_battle")
                    fired_stance = True
                else:
                    _raw(pilot, "advance", {}, "spacemolt_battle")
            time.sleep(10)

        # 7. Loot own new wrecks
        time.sleep(5)
        _, wr_after, _ = _raw(pilot, "wrecks", {}, "spacemolt_salvage")
        looted = 0
        for w in wr_after.get("wrecks") or []:
            if isinstance(w, dict) and w.get("id") not in before_ids and w.get("killer_name") == pilot and w.get("cargo"):
                _raw(pilot, "loot", {"wreck_id": w["id"]}, "spacemolt_salvage")
                looted += 1
                time.sleep(11)
        print("RESULT %s: hunt_net pack %s (%s x%d @ %s:%s) | %.1f min | looted=%d" % (
            pilot, pid, cur.get("species"), len(members), cur["system"], cur["poi"],
            (time.time() - started) / 60.0, looted), flush=True)
        return "ranch_floor" if ranch_floor_hit else "pack_done"
    finally:
        if is_leader:
            try:
                _raw(pilot, "disband", {}, "spacemolt_fleet")
            except Exception:
                pass
            pack_update(DATA, pid, lambda p: p.update(state="done"))
        _raw(pilot, "default_stance", {"stance": "flee"}, "spacemolt_battle")
        _gate_call("PATCH", "/accounts/%s/combat-mode" % q, {"mode": "flee"})
        _goal(pilot, "prepare-at-station", {"systemId": dock[0], "poiId": dock[1], "baseId": dock[2], "refuel": True}, timeout_s=180)


def _option(args, flag, default=""):
    return args[args.index(flag) + 1] if flag in args and args.index(flag) + 1 < len(args) else default


def _heartbeat(order_path, every=60):
    stop_ev = threading.Event()
    try:
        orig_ino = os.stat(order_path).st_ino
    except OSError:
        orig_ino = None

    def beat():
        while not stop_ev.wait(every):
            try:
                if orig_ino is not None and os.stat(order_path).st_ino != orig_ino:
                    return
                os.utime(order_path)
            except OSError:
                return

    t = threading.Thread(target=beat, daemon=True)
    t.start()
    return stop_ev


def main(argv=None):
    args = sys.argv[1:] if argv is None else list(argv)
    if not args or args[0].startswith("--"):
        sys.exit("usage: hunt_net.py <pilot> [--minutes 45] [--policy game/hunt-policy.json] [--route hunt-network]")
    pilot = args[0]
    minutes = float(_option(args, "--minutes", "45") or 45)
    route_id = _option(args, "--route", "hunt-network") or "hunt-network"
    policy_arg = _option(args, "--policy", "")

    sys.path.insert(0, str(ROOT / "fleet"))
    import division
    division.require(pilot)

    stop_flag = []

    def _on_sig(signum, _frame):
        stop_flag.append("signal %d" % signum)
        raise SystemExit("signal %d" % signum)

    signal.signal(signal.SIGTERM, _on_sig)
    signal.signal(signal.SIGINT, _on_sig)

    policy = load_policy(policy_arg or None)
    order_path = DATA / "fleet" / "orders" / (pilot + ".json")
    write_json(order_path, {"pilot": pilot, "what": "hunt_net " + route_id, "since": utc_now(), "pid": os.getpid()})
    hb = _heartbeat(order_path)
    claimed_key = None
    cooldown_key = None

    try:
        if not policy.get("enabled", True):
            print("RESULT %s: hunt_net %s | disabled in policy" % (pilot, route_id), flush=True)
            time.sleep(60)
            return 0

        ship_doc = read_json(DATA / "fleet" / "ships" / ship_file_name(pilot), {})
        ship_doc["name"] = pilot
        wep_cat, boost_cat = load_weapon_catalog(DATA)
        spow = compute_ship_power(ship_doc, wep_cat, boost_cat)
        try:
            import gauges
            f9 = f9_gauge(ship_doc, gauges.load_items(DATA))
        except Exception:
            f9 = None
        if f9 is None:
            print("RESULT %s: hunt_net %s | no F9 gauge read (gauges.py): no hunt" % (pilot, route_id), flush=True)
            time.sleep(60)
            return 0
        world = load_combat_world(DATA, REPO, policy)
        claims, cooldowns = load_hunt_claims(DATA, policy)

        # Count active Military ships for dynamic share calculations
        orders_dir = DATA / "fleet" / "orders"
        active_mil = sum(1 for p in (orders_dir.glob("*.json") if orders_dir.is_dir() else []) if p.stem.startswith(("drone-", "sentinel-")))
        active_mil = max(12, active_mil)

        # --- LANE 0: DORMANT WAR WING (ACTIVATES STRICTLY ON POSTURE == WAR, F2) ---
        war_active, war_tags = detect_war_posture(DATA, policy)
        if war_active:
            wjob = pick_war_assignment(pilot, ship_doc, spow, world, policy, claims, war_tags, data_dir=DATA)
            if wjob and claim_hunt_key_atomic(DATA, pilot, wjob['key'], 'war_defense', policy, max_per_key=int((policy.get('war_wing') or {}).get('defenders_per_base') or 10)):
                claimed_key = wjob['key']
                wcmd = [
                    sys.executable, '-I', '-B', str(ROOT / 'fleet' / 'guard.py'),
                    pilot, wjob['system'], wjob['poi'],
                    '--guards', wjob['guards'], '--station', wjob['station'],
                    '--minutes', str(int((policy.get('war_wing') or {}).get('minutes') or minutes)),
                    '--route', route_id,
                ]
                print('%s %s hunt_net: WAR WING lane 0 -> %s (%s:%s)' % (utc_now(), pilot, wjob['key'], wjob['system'], wjob['poi']), flush=True)
                return subprocess.run(wcmd, check=False).returncode

        # --- LANE 1: ON-DEMAND ESCORT & PROTECTION (Royal Guard sentinels get priority slots) ---
        ecfg = policy.get("escort") or {}
        is_sentinel = str(pilot).startswith("sentinel-")
        escort_active = sum(1 for r in claims.values() if r.get("lane") == "escort")
        base_cap = min(int(ecfg.get("max_ships") or 12), max(1, int(round(active_mil * float(ecfg.get("max_fleet_share") or 0.15)))))
        escort_cap = base_cap + (4 if is_sentinel else 0)
        min_esc_pow = min(200.0, float(ecfg.get("min_power") or 350.0)) if is_sentinel else float(ecfg.get("min_power") or 350.0)
        if ecfg.get("enabled", True) and escort_active < escort_cap and spow["power"] >= min_esc_pow:
            demands = detect_escort_demands(DATA, world, policy, claims)
            p_dists = bfs_distances(world["adj"], str(ship_doc.get("system") or ""), max_hops=int(ecfg.get("max_jumps") or 10))
            for dem in demands:
                if ship_doc.get("system") and dem["system"] not in p_dists:
                    continue
                _, st_tup = nearest_station(world["adj"], world["stations_by_sys"], dem["system"], max_hops=6)
                if not st_tup:
                    continue
                if claim_hunt_key_atomic(DATA, pilot, dem["key"], "escort", policy, max_per_key=1):
                    claimed_key = dem["key"]
                    cmd = [
                        sys.executable, "-I", "-B", str(ROOT / "fleet" / "guard.py"),
                        pilot, dem["system"], dem["poi"],
                        "--guards", dem["guards"],
                        "--station", "%s:%s:%s" % st_tup,
                        "--minutes", str(int(ecfg.get("minutes") or minutes)),
                        "--route", route_id,
                    ]
                    if dem["mode"] == "follow":
                        cmd += ["--follow", dem["follow"]]
                    print("%s %s hunt_net: ESCORT lane -> %s (%s:%s)" % (utc_now(), pilot, dem["key"], dem["system"], dem["poi"]), flush=True)
                    rc = subprocess.run(cmd, check=False).returncode
                    return rc

        # --- LANE 2: COORDINATED GROUP PACKS (3 / 5 / 8 / 10 SHIPS, ~20-30% SHARE) ---
        pack_targets = score_pack_targets(ship_doc, spow, world, policy, claims, cooldowns, f9=f9)
        pack = pack_try_join_or_create(DATA, pilot, str(ship_doc.get("system") or ""), spow, pack_targets, world, policy, active_mil)
        if pack:
            print("%s %s hunt_net: PACK lane -> %s (%s x%d @ %s:%s, leader=%s)" % (
                utc_now(), pilot, pack["pack_id"], pack["species"], pack["desired_size"],
                pack["system"], pack["poi"], pack["leader"]), flush=True)
            res = run_pack_mission(pilot, pack, policy, order_path, route_id)
            if res == "ranch_floor":
                cooldown_key = pack["place_key"]
                return 0
            if res != "rally_timeout":
                return 0
            # Rally timed out -> cleanly fall through to Lane 3 solo hunting!

        # --- LANE 3 & 4: SOLO OPTIMAL HERD HUNTING (POWER-RATIO GATED + F38 RANCH FLOOR) ---
        # Command Support Flagships operate in War Wing / Escorts / Coordinated Packs -- never solo grazing!
        if pilot in load_command_flagships(DATA) and not policy.get("allow_command_solo", False):
            nap = min(90, int(policy.get("rest_seconds_when_empty") or 90))
            print("%s %s hunt_net: Command Support Flagship awaiting pack/escort/war wing; resting %ds" % (utc_now(), pilot, nap), flush=True)
            end_nap = time.time() + nap
            while time.time() < end_nap and not (DATA / "fleet" / "STOP").exists() and not stop_flag:
                time.sleep(min(15.0, max(1.0, end_nap - time.time())))
            return 0
        cands = score_solo_herds(ship_doc, spow, world, policy, claims, cooldowns, f9=f9)
        chosen = None
        for cand in cands:
            if claim_hunt_key_atomic(DATA, pilot, cand["key"], "solo", policy, max_per_key=1):
                chosen = cand
                claimed_key = cand["key"]
                break

        if not chosen:
            nap = int(policy.get("rest_seconds_when_empty") or 120)
            print("%s %s hunt_net: no eligible herd/pack/escort matched power=%.0f; resting %ds" % (utc_now(), pilot, spow["power"], nap), flush=True)
            end_nap = time.time() + nap
            while time.time() < end_nap and not (DATA / "fleet" / "STOP").exists() and not stop_flag:
                time.sleep(min(20.0, max(1.0, end_nap - time.time())))
            return 0

        print("%s %s hunt_net: SOLO lane -> %s (%s x%d, power=%.0f ratio=%.2fx, %dJ, score=%.1f)" % (
            utc_now(), pilot, chosen["key"], chosen["species"], chosen["count"],
            spow["power"], chosen["ratio"], chosen["hops"], chosen["score"]), flush=True)

        scfg = policy.get("solo") or {}
        cmd = [
            sys.executable, "-I", "-B", str(ROOT / "fleet" / "hunt.py"),
            pilot, chosen["system"], chosen["poi"],
            "--species", chosen["species"],
            "--kills", str(chosen["kills"]),
            "--minutes", str(int(round(minutes))),
            "--min-bid", str(int(scfg.get("min_bid") or 1500)),
            "--sell-at", chosen["sell_at"],
            "--max-prey-hull", str(int(chosen["prey_hull"] * 1.2)),
            "--keep-herd", str(int(policy.get("keep_herd") or 2)),
            "--route", route_id,
            "--no-order",
        ]
        if scfg.get("alone", True):
            cmd.append("--alone")
        if policy.get("gift_to"):
            cmd += ["--gift-to", str(policy["gift_to"])]

        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for line in proc.stdout or ():
            sys.stdout.write(line)
            sys.stdout.flush()
            if "ranch floor kept" in line or "no free grazer here" in line:
                cooldown_key = chosen["key"]
        proc.wait()
        return proc.returncode or 0
    finally:
        hb.set()
        if claimed_key or cooldown_key:
            release_hunt_claim(
                DATA, pilot,
                cooldown_key=cooldown_key,
                cooldown_minutes=float(policy.get("cooldown_minutes") or 90),
                policy=policy,
            )
        try:
            cur = read_json(order_path, {})
            if isinstance(cur, dict) and cur.get("pid") == os.getpid() and cur.get("what") == "hunt_net " + route_id:
                order_path.unlink()
        except OSError:
            pass


if __name__ == "__main__":
    sys.exit(main())

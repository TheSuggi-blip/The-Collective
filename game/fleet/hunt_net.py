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
        "min_escorts": 3,
        "max_ships": 12,
        "max_fleet_share": 0.15,
        "threat_window_h": 4.0,
        "auto_protect_lawless_civilians": True,
        "protect_pilots": [],
        "protect_places": [],
        "max_jumps": 10,
        "min_power": 600.0,
        "lawless_min_hp": 180.0,
        "pirate_min_power_ratio": 1.80,
        "rally_timeout_s": 120,
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
    "bell_jelly": 45, "carrion_moth": 45, "halo_drifter": 50, "phase_lurker": 55,
    "quantum_moth": 55, "ash_scarab": 55, "pall_jelly": 55, "belt_grazer": 60,
    "patina_grazer": 60, "glitterback_crab": 60, "rivetshell": 60, "rime_grazer": 65,
    "pressblister": 65, "prism_drifter": 65, "veil_ray": 60, "hollow_pilgrim": 70,
    "cinder_urchin": 70, "glacier_drifter": 70, "chlorophage": 70, "sift_ray": 75,
    "cobalt_squid": 75, "lantern_slug": 75, "deuteron_slug": 85, "voltmanta": 85,
    "etchmaw": 85, "slag_tortoise": 90, "bulwark": 95, "mirror_skate": 95,
    "skeinwraith": 95, "glimmer_druse": 95, "kiln_snail": 100, "inkwyrm": 100,
    "void_browser": 100, "facet_druse": 110, "magnet_barnacle": 110, "vulcanid": 110,
    "silica_borer": 115, "cauldronback": 120, "aeonbear": 120, "bullionaut": 130,
    "glintfin": 140, "crusher_mantis": 140, "frost_lurker": 150,
    "pilot_whale": 220, "cloudwhale": 220, "molt_leviathan": 350,
}

SPECIES_NEED_DROPS = {
    "mirror_skate": ("foil_scale",),
    "cauldronback": ("alloy_scale", "anchor_plate"),
    "inkwyrm": ("cobalt_ink",),
    "magnet_barnacle": ("ferrous_nodule",),
    "silica_borer": ("silica_lens",),
    "hollow_pilgrim": ("ember_gland", "caustic_sac"),
    "pilot_whale": ("whale_blubber", "graphene_thread", "antimatter_residue", "whale_oil"),
    "cloudwhale": ("lumen_oil", "whale_baleen", "whale_oil"),
    "glacial_whale": ("lumen_oil", "hoarfrost_flank", "hoarfrost_heartcore"),
    "cinder_sylph": ("ember_gland", "cinderspice"),
    "cinder_urchin": ("radiant_bile", "ember_gland"),
    "glintfin": ("glintfin", "chrome_scale"),
    "glitterback_crab": ("chrome_scale", "creature_carapace"),
    "cobalt_squid": ("cobalt_roe", "cobalt_ink", "cobalt_squid"),
    "pressblister": ("nitrogen_bladder", "methane_bladder", "levity_bladder"),
    "bell_jelly": ("noble_condensate", "radiant_bile"),
    "halo_drifter": ("noble_condensate",),
    "prism_drifter": ("prism_charged_ichor", "prismatic_carapace", "prismatic_lens"),
    "glacier_drifter": ("tritium_pearl",),
    "rivetshell": ("rivetshell_meat",),
    "crusher_mantis": ("mantis_claw",),
    "frost_lurker": ("hoarfrost_flank", "hoarfrost_heartcore", "dry_ice_frond"),
    "molt_leviathan": ("leviathan_heartcore", "leviathan_meat", "creature_carapace"),
    "sift_ray": ("ray_eggs", "ammonia_gland"),
    "drift_ray": ("ray_eggs", "levity_bladder"),
    "veil_ray": ("void_dust", "ray_eggs"),
    "belt_grazer": ("grazer_milk", "creature_carapace"),
    "patina_grazer": ("verdigris_curd", "grazer_milk"),
    "rime_grazer": ("rimeblue_cheese", "crystal_melt"),
    "slag_tortoise": ("creature_carapace", "slag_carapace"),
    "deuteron_slug": ("tritium_pearl", "deuterium_ice"),
    "lantern_slug": ("charge_gland", "methane_bladder"),
    "frost_moth": ("superfluid_vial", "crystal_melt", "hoarfrost_flank"),
    "phase_lurker": ("phase_crystal", "void_dust"),
    "quantum_moth": ("quantum_silk", "quantum_fragments", "exotic_lattice"),
    "ash_scarab": ("cinderspice", "ember_gland"),
    "kiln_snail": ("irradiated_marrow", "ember_gland"),
    "facet_druse": ("crystal_melt", "energy_crystal"),
    "nullbubble": ("krypton_bladder", "null_matter", "void_dust"),
    "chlorophage": ("caustic_sac",),
    "bullionaut": ("noble_matte",),
    "bulwark": ("ballast_plate",),
    "pall_jelly": ("noble_matte",),
    "voltmanta": ("ion_nodule",),
    "vulcanid": ("refractory_sinter",),
    "aeonbear": ("exotic_cyst",),
    "skeinwraith": ("exotic_distillate",),
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


def pilot_in_faction(data_dir, pilot):
    """True iff `pilot` is a live member of [CLTV] in empire/empire.json (can call deposit target='faction')."""
    emp = read_json(Path(data_dir) / "empire" / "empire.json", {})
    if not isinstance(emp, dict):
        return False
    p_s = str(pilot or "").strip()
    for m in (emp.get("members") or []):
        if isinstance(m, dict):
            nm = str(m.get("name") or m.get("pilot") or m.get("username") or m.get("member") or "").strip()
            if nm == p_s:
                return True
    return False


def _pilot_is_faction_officer(data_dir, pilot):
    """True iff `pilot` is a [CLTV] Officer/Leader (or holds manage_treasury) in empire/empire.json."""
    emp = read_json(Path(data_dir) / "empire" / "empire.json", {})
    if not isinstance(emp, dict):
        return False
    allowed = {"leader", "officer"}
    for r in (emp.get("roles") or []):
        if isinstance(r, dict) and (r.get("permissions") or {}).get("manage_treasury"):
            for k in ("id", "name"):
                if r.get(k):
                    allowed.add(str(r[k]).strip().lower())
    p_s = str(pilot or "").strip()
    for m in (emp.get("members") or []):
        if isinstance(m, dict):
            nm = str(m.get("pilot") or m.get("name") or m.get("username") or m.get("member") or "").strip()
            if nm == p_s:
                return str(m.get("role") or m.get("rank") or "").strip().lower() in allowed
    return False


def base_has_officer_trader_receiver(data_dir, dest_base):
    """True iff `dest_base` has an explicit (non-wildcard) [CLTV] Officer Trader in fleet/receivers.json['trader']."""
    if not dest_base:
        return False
    rec = read_json(Path(data_dir) / "fleet" / "receivers.json", {})
    tr = (rec.get("trader") or {}) if isinstance(rec, dict) else {}
    val = tr.get(str(dest_base))
    if not val:
        return False
    pilots = val if isinstance(val, list) else [val]
    return any(_pilot_is_faction_officer(data_dir, p) for p in pilots if p)


def hunt_dropoff_args(pilot, dest_base, lockbox_bases, data_dir, gift_to_default="trader"):
    """Hybrid Lockbox delivery flags for hunt.py:
      - In-faction hunter at ANY Lockbox hub -> ['--deposit', 'faction'] (direct Shared Faction Lockbox!).
      - Outside-faction hunter at a safe Lockbox hub with a permanently docked [CLTV] Officer Trader ->
        ['--gift-to', 'trader'] (<= 2m local sale or zero-fuel lockbox_push!).
      - Outside-faction hunter at a lawless Outpost Lockbox (or any Lockbox without an Officer Trader) ->
        ['--gift-to', 'hauler'] (100% in-faction Officer Haulers -> direct sale or lockbox_drain!).
      - Non-Lockbox station -> ['--gift-to', gift_to_default] when configured.
    """
    if dest_base and dest_base in (lockbox_bases or set()):
        if pilot_in_faction(data_dir, pilot):
            return ["--deposit", "faction"]
        if base_has_officer_trader_receiver(data_dir, dest_base):
            return ["--gift-to", "trader"]
        return ["--gift-to", "hauler"]
    if gift_to_default:
        return ["--gift-to", str(gift_to_default)]
    return []


def load_command_flagships(data_dir):
    fg = read_json(Path(data_dir) / "fleet" / "flagships.json", {})
    if not isinstance(fg, dict):
        return set()
    return {str(k) for k, v in fg.items() if isinstance(v, dict)}


# Permanent 10-Pack Outpost Defense & High-Tier Strike Roster (4x 3-pack, 3x 5-pack, 3x 7-pack = 48 ships = 34% Military)
# Anchored at our 3 lawless Outposts (gsc_0044, atria, felis) -- safe Lockboxes do not need armed guards!
STANDING_SQUAD_SPECS = (
    # gsc_0044 Outpost: 3-pack + 5-pack + 7-pack + 4th 3-pack frontier reserve
    ("gsc-3a",   "gsc_0044", "Crimson Aegis",   1, 1),
    ("gsc-5a",   "gsc_0044", "Solar Mandate",   1, 3),
    ("gsc-7a",   "gsc_0044", "Vision",          2, 4),
    ("gsc-3b",   "gsc_0044", "Zero Point",      1, 1),
    # atria Outpost: 3-pack + 5-pack + 7-pack
    ("atria-3a", "atria",    "Nebula Charter",  1, 1),
    ("atria-5a", "atria",    "Mercurys Ledger", 1, 3),
    ("atria-7a", "atria",    "Prime Directive", 2, 4),
    # felis Outpost: 3-pack + 5-pack + 7-pack
    ("felis-3a", "felis",    "Rimward Pact",    1, 1),
    ("felis-5a", "felis",    "Golden Chariot",  1, 3),
    ("felis-7a", "felis",    "Hades",           2, 4),
)


def standing_squad_for_pilot(data_dir, pilot, policy=None):
    """Deterministically assign 48 Military pilots into 10 permanent standing squads (4x3, 3x5, 3x7)
    anchored at our 3 lawless Outposts (gsc_0044, atria, felis). Returns squad dict or None."""
    pcfg = (policy or {}).get("packs") or {}
    if not pcfg.get("standing_outpost_squads", True):
        return None
    p_s = str(pilot or "").strip()
    if not p_s:
        return None
    # Collect deterministic sorted Military sentinel-* and drone-* pool from fleet.json (or ships/ dir)
    fj = read_json(Path(data_dir) / "fleet" / "fleet.json", {})
    sents, drones = [], []
    for sh in (fj.get("ships") or [] if isinstance(fj, dict) else []):
        if not isinstance(sh, dict):
            continue
        nm = str(sh.get("name") or sh.get("pilot") or "").strip()
        if nm.startswith("sentinel-"):
            sents.append(nm)
        elif nm.startswith("drone-"):
            drones.append(nm)
    if not sents and not drones:
        sdir = Path(data_dir) / "fleet" / "ships"
        if sdir.is_dir():
            for fp in sorted(sdir.glob("*.json")):
                nm = fp.stem
                if nm.startswith("sentinel-"):
                    sents.append(nm)
                elif nm.startswith("drone-"):
                    drones.append(nm)
    def _num_key(nm):
        parts = nm.split("-")
        return (int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 9999, nm)
    sents = sorted(set(sents), key=_num_key)
    drones = sorted(set(drones), key=_num_key)
    si, di = 0, 0
    for sq_id, outpost_sys, leader, n_sent, n_drone in STANDING_SQUAD_SPECS:
        mem = [leader]
        s_pick = sents[si : si + n_sent]
        si += n_sent
        d_pick = drones[di : di + n_drone]
        di += n_drone
        mem.extend(s_pick)
        mem.extend(d_pick)
        if p_s in mem:
            return {
                "squad_id": sq_id,
                "outpost_system": outpost_sys,
                "leader": leader,
                "size": 1 + n_sent + n_drone,
                "members": mem,
                "is_leader": p_s == leader,
            }
    return None


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


def nearest_station(adj, stations_by_sys, sys_id, max_hops=6, preferred_bases=None):
    dists = bfs_distances(adj, sys_id, max_hops=max_hops)
    pref = preferred_bases or ()
    best_any = None
    best_pref = None
    for sid, hops in sorted(dists.items(), key=lambda kv: (kv[1], kv[0])):
        sts = stations_by_sys.get(sid)
        if not sts:
            continue
        if best_any is None:
            best_any = (hops, sts[0])
        if pref and best_pref is None:
            for st in sts:
                if st[2] in pref:
                    best_pref = (hops, st)
                    break
        if best_pref is not None:
            break
    # Prefer a staffed CLTV Bursar cross-dock hub if within +1 hop of closest unstaffed dock
    if best_pref is not None and (best_any is None or best_pref[0] <= best_any[0] + 1):
        return best_pref
    return best_any if best_any is not None else (None, None)


def load_combat_world(data_dir, repo_root, policy, now_t=None):
    """Load graph, systems, stations, herds, wildlife hull/pirate reads, ranches, pirates, needs, and loot values."""
    if now_t is None:
        import worldcache as _wc
        ck = ("hunt_world", str(data_dir), str(repo_root), _wc.db_sig(data_dir),
              str((policy or {}).get("pirate_avoid_hours")), str((policy or {}).get("herd_stale_hours")))
        return _wc.cached(ck, 25.0, lambda: _load_combat_world_uncached(data_dir, repo_root, policy, time.time()))
    return _load_combat_world_uncached(data_dir, repo_root, policy, float(now_t))


def _load_combat_world_uncached(data_dir, repo_root, policy, now_t):
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
            import worldcache as _wc
            conn = _wc.ro_db(db_path)
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
            _bursar_live = set()
            _lockbox_hubs = set()
            try:
                _bc_doc = read_json(Path(data_dir) / "fleet" / "bursar_claims.json", {})
                if isinstance(_bc_doc, dict):
                    for _bk, _bv in _bc_doc.items():
                        if isinstance(_bv, dict) and (now_t - float(_bv.get("claimed_at") or 0)) <= 7200.0:
                            _bursar_live.add(str(_bk))
            except Exception:
                pass
            _hn_tbls = {r[0] for r in _rows("SELECT name FROM sqlite_master WHERE type='table'")}
            if "faction_facilities" in _hn_tbls:
                for (lb_base,) in _rows(
                    "SELECT DISTINCT base FROM faction_facilities WHERE type = 'faction_lockbox' AND COALESCE(status, 'active') = 'active' AND base IS NOT NULL"
                ):
                    if lb_base:
                        _lockbox_hubs.add(str(lb_base))
            for sys_id, poi_id, base_id, nm in _rows(
                "SELECT system, poi, base, name FROM places WHERE base IS NOT NULL AND base != '' ORDER BY system, poi"
            ):
                if (str(sys_id), str(nm or "")) in foreign_docks or (str(base_id) in outposts and str(base_id) not in _lockbox_hubs):
                    continue
                lst = stations_by_sys.setdefault(sys_id, [])
                if str(base_id) in _bursar_live:
                    lst.insert(0, (sys_id, poi_id, base_id))
                elif str(base_id) in _lockbox_hubs:
                    lst.insert(0, (sys_id, poi_id, base_id))
                else:
                    lst.append((sys_id, poi_id, base_id))
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
            active_pirate_raids = set()
            if _rows("SELECT name FROM sqlite_master WHERE type='table' AND name='public_battles'"):
                pb_cut = now_t - float(policy.get("pirate_battle_avoid_hours") or 2.0) * 3600.0
                for (pb_s,) in _rows("SELECT DISTINCT system FROM public_battles WHERE category = 'pirate' AND t >= ?", (pb_cut,)):
                    if pb_s:
                        s_clean = str(pb_s).strip()
                        pirates.add(s_clean)
                        active_pirate_raids.add(s_clean)
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

    # 100% EMPIRICAL, LIQUIDITY-WEIGHTED & ANTI-FLOOD wildlife loot valuation (Suggi directive):
    # - Discounts thin 1-3 unit bids so hunters NEVER mass-farm for 1-2 buyers!
    # - Applies saturation decay against live fleet holdings + faction_storage so hunters auto-rotate when flooded!
    # - Incorporates live high-payout delivery contracts (e.g. HEXC 100k cr for 20x lumen_oil = 5,000 cr/u!).
    live_drop_val = {}
    _drop_held = {}
    _db_h = Path(data_dir) / "store" / "read.db"
    if _db_h.is_file():
        try:
            import worldcache as _wc_h
            _ch = _wc_h.ro_db(_db_h, timeout=3.0)
            _htbls = {r[0] for r in _ch.execute("SELECT name FROM sqlite_master WHERE type='table'")}
            if "holdings" in _htbls:
                for _iid, _u in _ch.execute("SELECT item, SUM(units) FROM holdings GROUP BY item"):
                    if _iid and _u:
                        _drop_held[str(_iid)] = _drop_held.get(str(_iid), 0) + int(_u)
            if "faction_storage" in _htbls:
                for _iid, _u in _ch.execute("SELECT item, SUM(units) FROM faction_storage GROUP BY item"):
                    if _iid and _u:
                        _drop_held[str(_iid)] = _drop_held.get(str(_iid), 0) + int(_u)
            if "books" in _htbls:
                _bcols = {r[1] for r in _ch.execute("PRAGMA table_info(books)").fetchall()}
                _bc = "base" if "base" in _bcols else ("station" if "station" in _bcols else "''")
                _hcut = time.time() - 6.0 * 3600.0
                _h_cltv, _h_fair, _mg_h = set(), {}, None
                try:
                    import market_guard as _mg_h
                    _h_cltv, _ = _mg_h.load_cltv_buy_orders(data_dir, now_t=now_t)
                    _h_fair = _mg_h.read_price_oracle(data_dir, now_t=now_t)
                except Exception:
                    _mg_h = None
                _q = "SELECT %s, item, bid, bid_qty FROM books WHERE bid >= 15 AND bid_qty > 0 AND t >= ?" % _bc
                _h_agg = {}
                for _hb, _hi, _hp, _hq in _ch.execute(_q, (_hcut,)):
                    _bs, _is = str(_hb or ""), str(_hi or "")
                    _qi, _pf = int(_hq or 0), float(_hp or 0.0)
                    if not _is or _qi <= 0 or _pf <= 0.0:
                        continue
                    if _h_cltv and _bs and (_bs, _is) in _h_cltv:
                        continue
                    if _mg_h is not None and _h_fair:
                        _pf = _mg_h.guarded_bid_price(_is, _pf, _h_fair, max_mult=1.50)
                    _r = _h_agg.get(_is)
                    if _r is None:
                        _h_agg[_is] = [_pf * _qi, _qi, {_bs}]
                    else:
                        _r[0] += _pf * _qi
                        _r[1] += _qi
                        _r[2].add(_bs)
                for _iid, (_wsum, _tq, _bset) in _h_agg.items():
                    if _tq <= 0:
                        continue
                    _stc = max(1, len(_bset))
                    _vwap = float(_wsum) / float(_tq)
                    # Strictly REAL EXTERNAL top-of-book bid_qty liquidity & anti-flood saturation!
                    _bw_m = 1.35 if (_vwap * float(_tq)) >= 500000.0 else (1.15 if _stc >= 3 else (1.0 if _stc >= 2 else 0.80))
                    _liq = min(1.0, float(_tq) / 30.0) * _bw_m
                    _abs = max(40.0, float(_tq) * 0.85)
                    _h_u = float(_drop_held.get(_iid, 0))
                    _sat = 0.05 if _h_u >= _abs else max(0.15, 1.0 - (_h_u / _abs) * 0.75)
                    live_drop_val[_iid] = max(live_drop_val.get(_iid, 0.0), _vwap * _liq * _sat)
            # Live delivery contracts (guaranteed repeatable buyer demand like HEXC 100k lumen_oil / 61k ember_gland!)
            if "missions" in _htbls:
                for _rew, _obj in _ch.execute("SELECT reward, objectives FROM missions WHERE kind='delivery' AND reward >= 5000 AND objectives IS NOT NULL"):
                    _m = re.search(r"Deliver\s+(\d+)\s*(?:x|\u00d7|\*)?\s+([A-Za-z0-9 _-]+?)(?:\s+to\s+|$)", str(_obj or ""), re.I)
                    if _m and int(_m.group(1) or 0) > 0:
                        _u_p = float(_rew) / float(int(_m.group(1)))
                        _slug = re.sub(r"[^a-z0-9]+", "_", _m.group(2).strip().lower()).strip("_")
                        if _slug:
                            _h_u = float(_drop_held.get(_slug, 0))
                            _csat = max(0.15, 1.0 - min(0.85, _h_u / 200.0))
                            live_drop_val[_slug] = max(live_drop_val.get(_slug, 0.0), _u_p * _csat)
            _ch.close()
        except sqlite3.Error:
            pass
    cd = read_json(Path(repo_root) / "game" / "craft-demand.json", {})
    craft_loot_species = {str(x).lower() for x in (cd.get("priority_loot_species") or [])} if isinstance(cd, dict) and cd.get("enabled", True) else set()
    for sp, hull in species_hull.items():
        drops = SPECIES_NEED_DROPS.get(sp) or ()
        emp_v = sum(live_drop_val.get(d, 0.0) for d in drops)
        if emp_v <= 0.0:
            emp_v = 25.0
        if any(d in needs_items for d in drops):
            emp_v *= 2.5
        elif sp.lower() in craft_loot_species:
            emp_v *= 1.35
        species_loot_val[sp] = round(emp_v, 1)
    owned_bases = []
    _db_b = Path(data_dir) / "store" / "read.db"
    if _db_b.is_file():
        try:
            import worldcache as _wc
            c2 = _wc.ro_db(_db_b, timeout=3.0)
            if "bases" in {r[0] for r in c2.execute("SELECT name FROM sqlite_master WHERE type='table'")}:
                for b_id, sys_id, poi_id, knd in c2.execute("SELECT base, system, poi, kind FROM bases WHERE system IS NOT NULL"):
                    owned_bases.append({"base": str(b_id), "system": str(sys_id), "poi": str(poi_id or b_id), "kind": str(knd or "outpost")})
            c2.close()
        except sqlite3.Error:
            pass

    return {
        "adj": adj, "systems": systems, "stations_by_sys": stations_by_sys,
        "herds": herds, "pirates": pirates, "active_pirate_raids": (active_pirate_raids if "active_pirate_raids" in locals() else set()), "pirate_details": pirate_details,
        "ranch_pois": ranch_pois, "ranch_systems": ranch_systems,
        "species_hull": species_hull, "needs_items": needs_items,
        "species_loot_val": species_loot_val, "owned_bases": owned_bases,
        "craft_loot_species": craft_loot_species, "bursar_bases": _bursar_live, "lockbox_bases": _lockbox_hubs, "data_dir": str(data_dir),
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


def assess_escort_threat(sys_id, poi_id, world):
    """Estimate NPC pirate threat at sys_id:poi_id (or worst pirate sighting in sys_id).
    Returns compute_target_threat(..., role='pirate') dict, or None for calm policed space."""
    pdet = world.get("pirate_details") or {}
    plist = None
    if sys_id and poi_id:
        cand = pdet.get("%s:%s" % (sys_id, poi_id))
        if isinstance(cand, list) and cand:
            plist = cand
    worst = None
    if plist:
        ph = max(float(p.get("max_hull") or p.get("hull") or 100.0) for p in plist if isinstance(p, dict))
        ps = max(float(p.get("max_shield") or p.get("shield") or 40.0) for p in plist if isinstance(p, dict))
        worst = compute_target_threat(ph, ps, role="pirate", count_fighting=max(1, len(plist)))
    else:
        pref = str(sys_id or "") + ":"
        for k, pl in pdet.items():
            if not str(k).startswith(pref) or not isinstance(pl, list) or not pl:
                continue
            ph = max(float(p.get("max_hull") or p.get("hull") or 100.0) for p in pl if isinstance(p, dict))
            ps = max(float(p.get("max_shield") or p.get("shield") or 40.0) for p in pl if isinstance(p, dict))
            th = compute_target_threat(ph, ps, role="pirate", count_fighting=max(1, len(pl)))
            if worst is None or th["threat"] > worst["threat"]:
                worst = th
    if worst is not None:
        return worst
    is_lawless = not bool(((world.get("systems") or {}).get(sys_id) or {}).get("empire"))
    in_pirates = sys_id in (world.get("pirates") or set())
    if is_lawless or in_pirates:
        # Conservative baseline raider threat when pirates/lawless space lack exact hull reads
        return compute_target_threat(110.0, 50.0, role="pirate", count_fighting=1)
    return None


def escort_power_ok(ship_doc, spow, sys_id, poi_id, world, policy, pack_size=3):
    """Verify an escort ship meets min_power, lawless hull floor, and pack-vs-pirate threat gate.
    Returns (ok: bool, needed_pack_size: int or None, threat_dict or None)."""
    ecfg = (policy or {}).get("escort") or {}
    min_pow = float(ecfg.get("min_power") or 350.0)
    min_escorts = max(3, int(ecfg.get("min_escorts") or 3))
    base_sz = max(min_escorts, int(pack_size or min_escorts))
    if spow.get("dps", 0.0) <= 0.0 or spow.get("power", 0.0) < min_pow:
        return False, None, None
    is_lawless = not bool(((world.get("systems") or {}).get(sys_id) or {}).get("empire"))
    threat = assess_escort_threat(sys_id, poi_id, world)
    if threat is None and not is_lawless:
        return True, base_sz, None
    # Lawless / pirate space: block bare T0 starter hulls (e.g. 75+50=125 HP)
    raw_hp = float(spow.get("max_hull") or 0.0) + float(spow.get("max_shield") or 0.0)
    min_hp = float(ecfg.get("lawless_min_hp") or 180.0)
    if int(spow.get("tier") or 0) < 1 and raw_hp < min_hp:
        return False, None, threat
    if threat is None:
        return True, base_sz, None
    pir_ratio = float(ecfg.get("pirate_min_power_ratio") or 1.80)
    sizes = [s for s in (3, 5, 7, 10) if s >= base_sz]
    if base_sz not in sizes:
        sizes.insert(0, base_sz)
    for sz in sorted(set(sizes)):
        comb = {
            "power": float(spow["power"]) * sz,
            "dps": float(spow["dps"]) * sz,
            "ehp": float(spow["ehp"]) * sz,
        }
        ok_g, _r = passes_combat_gate(comb, threat, pir_ratio, check_f9=True)
        if ok_g:
            return True, sz, threat
    return False, None, threat


def detect_escort_demands(data_dir, world, policy, claims, now_t=None):
    """Find active civilian ships or configured sites needing Military escort/protection right now.
    Keeps each demand open until at least `min_escorts` (default 3) escorts claim it."""
    now_t = time.time() if now_t is None else float(now_t)
    ecfg = policy.get("escort") or {}
    if not ecfg.get("enabled", True):
        return []
    min_escorts = max(3, int(ecfg.get("min_escorts") or 3))
    demands = []
    seen_keys = set()
    claimed_counts = {}
    for rec in (claims or {}).values():
        if isinstance(rec, dict) and rec.get("lane") == "escort" and rec.get("key"):
            k = str(rec["key"])
            claimed_counts[k] = claimed_counts.get(k, 0) + 1

    # 1. Explicit configured places
    for pl in ecfg.get("protect_places") or []:
        if not isinstance(pl, str) or ":" not in pl:
            continue
        key = "escort:place:" + pl
        if claimed_counts.get(key, 0) >= min_escorts or key in seen_keys:
            continue
        seen_keys.add(key)
        sys_id, poi_id = pl.split(":", 1)
        demands.append({
            "key": key, "mode": "place", "system": sys_id, "poi": poi_id,
            "guards": "outpost", "needed": min_escorts, "priority": 100,
        })

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
                if claimed_counts.get(key, 0) >= min_escorts or key in seen_keys:
                    continue
                seen_keys.add(key)
                demands.append({
                    "key": key, "mode": "follow", "follow": pname,
                    "system": psys, "poi": ppoi or psys, "guards": orid or okind,
                    "needed": min_escorts,
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


def score_solo_herds(pilot_info, ship_power, world, policy, claims, cooldowns, now_t=None, f9=None, allow_cmd_override=False):
    """Score all eligible wild grazer herds for solo hunting, gated by percentage combat power ratio."""
    now_t = time.time() if now_t is None else float(now_t)
    scfg = policy.get("solo") or {}
    if (not scfg.get("enabled", True) and not allow_cmd_override) or ship_power["power"] <= 0:
        return []
    p_sys = str(pilot_info.get("system") or "")
    p_name = str(pilot_info.get("name") or "")
    max_j = int(scfg.get("max_jumps") or 6)
    tier_s_j = max(max_j, int(scfg.get("tier_s_max_jumps") or 8))
    if allow_cmd_override:
        max_j = min(max_j, 6)
        tier_s_j = min(tier_s_j, 8)
    tier_s_min = float(scfg.get("tier_s_min_loot_val") or 550.0)
    min_ratio = float(scfg.get("min_power_ratio") or 1.35)
    ideal_lo = float(scfg.get("ideal_ratio_low") or 1.45)
    ideal_hi = float(scfg.get("ideal_ratio_high") or 3.20)
    keep_h = int(policy.get("keep_herd", 2))
    min_cr = max(keep_h + 1, int(policy.get("min_creatures", keep_h + 1)))
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

    dists = bfs_distances(adj, p_sys, max_hops=tier_s_j) if p_sys else {}
    claimed_counts = {}
    for cp, r in (claims or {}).items():
        if cp != p_name and isinstance(r, dict) and r.get("key"):
            k_ = r.get("key")
            claimed_counts[k_] = claimed_counts.get(k_, 0) + 1

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
        herd_cap = 2 if int(h["count"]) >= 8 else 1
        if claimed_counts.get(place_key, 0) >= herd_cap or cooldowns.get(place_key, 0) > now_t:
            continue
        smeta = systems.get(sys_id, {})
        if smeta.get("stronghold"):
            continue
        is_policed = bool(smeta.get("empire"))
        if bool(policy.get("lawless_only", False)) and is_policed:
            continue
        if not is_policed and (policed_only or ship_power["power"] < allow_lawless_p):
            continue
        hops = dists.get(sys_id) if p_sys else 0
        _sp_lv_chk = float(species_loot.get(sp) or 0.0)
        _eff_j = tier_s_j if _sp_lv_chk >= tier_s_min else max_j
        if hops is None or hops > _eff_j:
            continue

        prey_hull = float(species_hull.get(sp) or 70.0)
        threat = compute_target_threat(prey_hull, role="grazer", count_fighting=1)
        ok_g, ratio = passes_combat_gate(ship_power, threat, min_ratio, check_f9=True)
        if not ok_g or not f9_passes(f9, prey_hull, "grazer", n=1):
            continue

        min_lv = float(scfg.get("min_loot_val") or 0.0)
        if min_lv > 0 and float(species_loot.get(sp) or 0.0) < min_lv:
            continue
        _st_rad = int(scfg.get("max_station_jumps") or 6)
        _eff_st_rad = tier_s_j if _sp_lv_chk >= tier_s_min else _st_rad
        st_hops, st_tup = nearest_station(adj, stations_by_sys, sys_id, max_hops=_eff_st_rad, preferred_bases=((world.get("bursar_bases") or set()) | (world.get("lockbox_bases") or set())))
        if not st_tup or st_tup[0] in pirates:
            continue

        # Sweet-spot multiplier: encourages strong T2/T3/T4 hulls to graduate up to tougher high-value herds
        if ideal_lo <= ratio <= ideal_hi:
            fit_mult = 1.35
        elif ratio > ideal_hi:
            fit_mult = max(0.55, 1.0 - 0.08 * (ratio - ideal_hi))
        else:
            fit_mult = 1.0
        _pref_hubs = (world.get("bursar_bases") or set()) | (world.get("lockbox_bases") or set())
        if st_tup[2] in _pref_hubs:
            if st_hops <= 2:
                fit_mult *= 1.18
            elif st_hops <= 4:
                fit_mult *= 1.10
            elif st_hops <= 8:
                fit_mult *= 1.04

        kills_avail = max(1, min(int(scfg.get("kills_per_run") or 6), h["count"] - keep_h))
        loot_est = float(species_loot.get(sp) or 0.0) * kills_avail
        fuel_est = 90.0 * (hops + st_hops) * (1.0 + 0.5 * ship_power["tier"])
        score = ((loot_est * fit_mult) - fuel_est) / (1.0 + 0.7 * hops + 0.8 * st_hops)
        if score <= 0.0:
            continue
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
    _is_cmd_p = str(pilot_info.get("name") or "") in load_command_flagships(world.get("data_dir") or DATA)
    _min_mp = float(pcfg.get("command_flagship_min_power") or 150.0) if _is_cmd_p else float(pcfg.get("min_member_power") or 420.0)
    _cmd_support_ok = _is_cmd_p and float(ship_power.get("ehp") or 0.0) >= 120.0
    if not pcfg.get("enabled", True) or (ship_power["power"] < _min_mp and not _cmd_support_ok):
        return []
    _wing_floor = float(pcfg.get("min_member_power") or 750.0)
    _pack_eval_pwr = (
        {
            **ship_power,
            "power": max(float(ship_power.get("power") or 0.0), _wing_floor),
            "dps": max(float(ship_power.get("dps") or 0.0), 18.0),
            "ehp": max(float(ship_power.get("ehp") or 0.0), 260.0),
        }
        if _is_cmd_p else ship_power
    )
    p_sys = str(pilot_info.get("system") or "")
    max_j = int(pcfg.get("max_jumps") or 12)
    sizes = tuple(int(s) for s in (pcfg.get("sizes") or [3, 5, 8, 10]))
    wild_ratio = float(pcfg.get("min_power_ratio") or 1.80)
    pir_ratio = float(pcfg.get("pirate_min_power_ratio") or 2.20)
    min_thull = int(pcfg.get("min_target_hull") or 80)
    prio_sp = set(str(x) for x in (pcfg.get("priority_species") or []))
    _pk_kh = int(policy.get("keep_herd", 2))
    min_cr = max(_pk_kh + 1, int(policy.get("min_creatures", _pk_kh + 1)))
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
        if bool(policy.get("lawless_only", False)) and (systems.get(sys_id) or {}).get("empire"):
            continue
        hops = dists.get(sys_id) if p_sys else 0
        if hops is None or hops > max_j:
            continue
        prey_hull = float(species_hull.get(sp) or 90.0)
        if prey_hull < min_thull and role != "predator":
            continue
        threat = compute_target_threat(prey_hull, role=role, count_fighting=1)
        # Packs hunt strictly STRONGER opponents than solo (never waste a 3/5/7/10 pack on a solo-able field!)
        solo_ratio = float((policy.get("solo") or {}).get("min_power_ratio") or 1.35)
        solo_ok = passes_combat_gate(ship_power, threat, solo_ratio, check_f9=False)[0] and (
            f9 is None or f9_passes(f9, prey_hull, role, n=1)
        )
        # Command Flagships NEVER solo-graze (they exist to lead strike packs & earn leadership XP!),
        # so allow Command ships to start packs on big priority prey even if a heavy flagship passed solo_ok!
        if solo_ok and not (_is_cmd_p and (sp in prio_sp or prey_hull >= min_thull)) and not pcfg.get("allow_healer_patrol", False):
            continue
        if sp in set(str(x) for x in (policy.get("exclude_species") or [])):
            continue
        sz = choose_pack_size(_pack_eval_pwr, threat, wild_ratio, sizes=sizes, f9=f9, prey_hull=prey_hull, role=role)
        if sz is None:
            if _is_cmd_p and sizes:
                sz = max(s for s in sizes if s <= 5) if any(s <= 5 for s in sizes) else min(sizes)
            else:
                continue
        _pk_st_rad = int(pcfg.get("max_station_jumps") or 10)
        st_hops, st_tup = nearest_station(adj, stations_by_sys, sys_id, max_hops=_pk_st_rad, preferred_bases=((world.get("bursar_bases") or set()) | (world.get("lockbox_bases") or set())))
        if not st_tup:
            continue
        raw_lv = float(species_loot.get(sp) or 0.0)
        min_pk_lv = float(pcfg.get("min_loot_val") or 450.0)
        min_per_ship = float(pcfg.get("min_loot_per_ship") or 250.0)
        # Zero-fuel-waste ROI gate: NEVER burn 3x/5x/7x pack fuel on noob/worthless prey (e.g. 6 cr pilot_whale)!
        if raw_lv < max(min_pk_lv, min_per_ship * float(sz)):
            continue
        loot_v = raw_lv * (1.8 if sp in prio_sp else 1.0) * (1.5 if role == "predator" else 1.0)
        _pk_pref = (world.get("bursar_bases") or set()) | (world.get("lockbox_bases") or set())
        _pk_hub_m = 1.18 if (st_tup[2] in _pk_pref and st_hops <= 2) else (1.10 if (st_tup[2] in _pk_pref and st_hops <= 4) else 1.0)
        score = (loot_v * (prey_hull / 60.0) * _pk_hub_m) / (1.0 + 0.6 * hops + 0.5 * st_hops)
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
            if bool(policy.get("lawless_only", False)) and (systems.get(sys_id) or {}).get("empire"):
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
            sz = choose_pack_size(_pack_eval_pwr, threat, pir_ratio, sizes=sizes, f9=f9, prey_hull=2 * phull + pshield, role="grazer")
            if sz is None:
                continue
            st_hops, st_tup = nearest_station(adj, stations_by_sys, sys_id, max_hops=int(pcfg.get("max_station_jumps") or 10), preferred_bases=((world.get("bursar_bases") or set()) | (world.get("lockbox_bases") or set())))
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


def pick_relocation_hub(pilot_info, ship_power, world, policy, claims, cooldowns, is_cmd=False, f9=None, now_t=None):
    """Adaptive Outpost/Hub Relocation: move idle hunters & Command Flagships out of grazed pockets to rich lawless hubs!"""
    now_t = time.time() if now_t is None else float(now_t)
    p_sys = str(pilot_info.get("system") or "")
    p_name = str(pilot_info.get("name") or "")
    if not p_sys:
        return None
    reloc_max_j = int(policy.get("relocate_max_jumps") or 45)
    adj = world.get("adj") or {}
    systems = world.get("systems") or {}
    stations_by_sys = world.get("stations_by_sys") or {}
    pref_bases = (world.get("lockbox_bases") or set()) | (world.get("bursar_bases") or set())
    dists = bfs_distances(adj, p_sys, max_hops=reloc_max_j)
    solo_on = bool((policy.get("solo") or {}).get("enabled", True)) and not is_cmd
    ranked_hubs = []
    for h_sys, st_list in stations_by_sys.items():
        if h_sys == p_sys or h_sys not in dists:
            continue
        if (systems.get(h_sys) or {}).get("stronghold") or h_sys in (world.get("pirates") or set()):
            continue
        st_tup = None
        for t in st_list:
            if not pref_bases or t[2] in pref_bases:
                st_tup = t
                break
        if not st_tup:
            continue
        h_hops = dists[h_sys]
        sim_pilot = dict(pilot_info, system=h_sys)
        h_targets = []
        if solo_on:
            h_targets.extend(score_solo_herds(sim_pilot, ship_power, world, policy, claims, cooldowns, now_t=now_t, f9=f9)[:5])
        h_targets.extend(score_pack_targets(sim_pilot, ship_power, world, policy, claims, cooldowns, now_t=now_t, f9=f9)[:5])
        if not h_targets:
            continue
        h_targets.sort(key=lambda c: -float(c.get("score") or 0.0))
        top5 = h_targets[:5]
        _hub_m = 1.25 if st_tup[2] in (world.get("lockbox_bases") or set()) else 1.0
        hub_score = (_hub_m * sum(max(1.0, float(c.get("score") or 0.0)) for c in top5)) / (1.0 + 0.18 * float(h_hops))
        ranked_hubs.append({
            "system": st_tup[0], "poi": st_tup[1], "base": st_tup[2],
            "hops": h_hops, "targets": len(h_targets),
            "top_species": str(top5[0].get("species") or ""), "score": round(hub_score, 1),
        })
    if not ranked_hubs:
        return None
    ranked_hubs.sort(key=lambda r: (-r["score"], r["hops"], r["system"]))
    top_sc = ranked_hubs[0]["score"]
    spread = [r for r in ranked_hubs[:3] if r["score"] >= top_sc * 0.50]
    idx = (sum(ord(ch) for ch in p_name) % len(spread)) if (len(spread) > 1 and p_name) else 0
    return spread[idx]


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
    _cmd_sup_ok = is_cmd and float(ship_power.get("ehp") or 0.0) >= 120.0
    if ship_power["power"] < min_mem_p and not _cmd_sup_ok:
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

            # Count active pack pilots (reserve desired_size for forming packs so pilots coalesce instead of fragmenting!)
            in_packs_reserved = sum(
                max(len(pk.get("members") or []), int(pk.get("desired_size") or 3))
                if pk.get("state") == "forming" else len(pk.get("members") or [])
                for pk in packs.values() if pk.get("state") in ("forming", "launched", "fighting")
            )
            forming_n = sum(1 for pk in packs.values() if pk.get("state") == "forming")
            max_forming = max(1, int(pcfg.get("max_forming_packs") or 3))
            quota = max(3, int(round(max(12, active_military_n) * target_share)))

            # 1. Prefer joining an existing forming pack within rally_max_jumps
            # Fill nearly-full packs FIRST (fewest slots remaining, then closest jump distance) so packs launch cleanly!
            # Command Support Flagships prioritize larger packs (>=10 allow 2 support flagships, <10 allow 1) and take Pack Leader!
            sort_key = (
                (lambda kv: (
                    -int(kv[1].get("desired_size") or 3),
                    max(0, int(kv[1].get("desired_size") or 3) - len(kv[1].get("members") or [])),
                    dists.get(kv[1].get("system"), 99),
                    kv[0],
                ))
                if is_cmd
                else (lambda kv: (
                    max(0, int(kv[1].get("desired_size") or 3) - len(kv[1].get("members") or [])),
                    dists.get(kv[1].get("system"), 99),
                    kv[0],
                ))
            )
            req_cmd_leader = bool(pcfg.get("require_command_leader", False))
            for pid, pk in sorted(packs.items(), key=sort_key):
                if pk.get("state") != "forming":
                    continue
                # Hard Command-Leadership Doctrine (Suggi directive):
                # When require_command_leader is active, non-Command ships may ONLY join a pack led by a Command Ship!
                if req_cmd_leader and not is_cmd and str(pk.get("leader") or "") not in cmd_ships:
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

            # 2. Otherwise create a new forming pack if under pack quota, under max_forming_packs, and targets exist.
            # HARD DOCTRINE: when require_command_leader=True, ONLY a Command Ship can create & lead a new group!
            if req_cmd_leader and not is_cmd:
                write_json(path, {"updated_at": int(now_t), "packs": packs})
                return None
            if in_packs_reserved >= quota or forming_n >= max_forming or not pack_targets:
                write_json(path, {"updated_at": int(now_t), "packs": packs})
                return None

            used_targets = {pk.get("target_key") for pk in packs.values() if pk.get("state") in ("forming", "launched", "fighting")}
            # Region feasibility for 3/5/7/10 packs: check live combat ships within rally_max_jumps when ships/ exists
            combat_by_sys = {}
            sdir = Path(data_dir) / "fleet" / "ships"
            if sdir.is_dir():
                for sp in sdir.glob("*.json"):
                    sd = read_json(sp, {})
                    nm = str(sd.get("name") or sd.get("username") or sp.stem)
                    if nm.startswith(("drone-", "sentinel-")) or nm in cmd_ships:
                        ss = str(sd.get("system") or "")
                        if ss:
                            combat_by_sys[ss] = combat_by_sys.get(ss, 0) + 1
            chosen = None
            for t in pack_targets:
                if t["key"] in used_targets:
                    continue
                dsz = int(t.get("desired_size") or 3)
                if combat_by_sys and dsz > 3:
                    tdists = bfs_distances(world["adj"], str(t.get("system") or ""), max_hops=rally_max_j)
                    nearby_mil = sum(cnt for s_id, cnt in combat_by_sys.items() if s_id in tdists)
                    if nearby_mil < dsz:
                        continue
                chosen = t
                break
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
    t_lim = max(30, int(timeout_s or 240))
    st, ans = _gate_call("POST", "/accounts/%s/goal" % q, {"type": gtype, "options": opts}, timeout=t_lim)
    if st not in (200, 201) or not isinstance(ans, dict) or "error" in ans:
        return False
    if "success" in ans:
        return bool(ans.get("success"))
    end_t = time.time() + t_lim
    while time.time() < end_t and not (DATA / "fleet" / "STOP").exists():
        _, acc = _gate_call("GET", "/accounts/" + q, timeout=20)
        if not acc.get("hasExecutingGoal"):
            return True
        time.sleep(6)
    return False


def _foreign_ranched(c):
    nm = str(c.get("name") or "")
    return nm.startswith("[") and not nm.startswith("[CLTV]")


def pack_fuel_short(ship_doc, target_sys, lanes, stations):
    """The note why a pack member stays home, or None: its tank (ship file) against the way from where it stands to
    the pack's system and on to the nearest station with fuel, by fuelplan's rule (hunt.py fuel_first weighs a solo
    hunt the same way). A tank at 90 percent or more always flies. 2026-11-25: a hunter with 3 fuel at a station
    that sells none led a whale pack to its gas pocket and stood there dry at 1 fuel."""
    import fuelplan
    if not isinstance(ship_doc, dict):
        return None
    fuel, size = ship_doc.get("fuel"), ship_doc.get("max_fuel")
    if not isinstance(fuel, (int, float)):
        return None
    if isinstance(size, (int, float)) and size > 0 and fuel >= 0.9 * size:
        return None
    here = str(ship_doc.get("system") or "")
    there = fuelplan.way(lanes, here, target_sys) if here and target_sys else None
    onward = fuelplan.nearest_fuel(lanes, target_sys, stations) if target_sys else None
    if there is None or not onward:
        return None
    way = there + onward[0]
    if fuelplan.fuel_short(fuel, way, ship=ship_doc):
        return "fuel %s short for the pack at %s and on to fuel (%s jumps)" % (fuel, target_sys, way)
    return None


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
        # Rally timed out cleanly -- remove self and abort forming pack, then fall through to Solo Hunt!
        def _abort_forming(p):
            if p.get("state") == "forming":
                p["members"] = [m for m in (p.get("members") or []) if m != pilot]
                if not p["members"] or time.time() >= rally_end:
                    p["state"] = "aborted"
        pack_update(DATA, pid, _abort_forming)
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
    in_game_fleet = False

    try:
        # 2. Prepare: repair/refuel, set default_stance fire & combat_mode external
        _goal(pilot, "prepare-at-station", {"systemId": dock[0], "poiId": dock[1], "baseId": dock[2], "refuel": True}, timeout_s=180)
        try:
            import fuelplan
            _lanes, _home = fuelplan.chart(REPO / "game")
            _far = fuelplan.strongholds(REPO / "game")
            _st = {k: v for k, v in fuelplan.fuel_stations(DATA).items() if k not in _far}
            _short = pack_fuel_short(read_json(DATA / "fleet" / "ships" / ship_file_name(pilot), {}), cur["system"], _lanes, _st)
        except Exception:
            _short = None
        if _short:
            print("%s %s hunt_net: PACK %s left: %s" % (utc_now(), pilot, pid, _short), flush=True)

            def _leave(p):
                if p.get("leader") == pilot:
                    p.update(state="aborted", flee=True, flee_reason="leader " + _short)
                else:
                    p["members"] = [m for m in (p.get("members") or []) if m != pilot]
            pack_update(DATA, pid, _leave)
            return "fuel_short"
        _raw(pilot, "default_stance", {"stance": "fire"}, "spacemolt_battle")
        _gate_call("PATCH", "/accounts/%s/combat-mode" % q, {"mode": "external"})
        time.sleep(10)

        # 3. Travel to target system:poi FIRST so all members are undocked at the EXACT SAME POI before fleet invite!
        ok_nav = _goal(pilot, "navigate-to-system", {"targetSystemId": cur["system"]}, timeout_s=arrive_timeout)
        if not ok_nav:
            ok_nav = _goal(pilot, "navigate-to-system", {"targetSystemId": cur["system"]}, timeout_s=120)
        ok_poi = _goal(pilot, "go-to-poi", {"targetPoiId": cur["poi"]}, timeout_s=90)
        if not ok_poi:
            _raw(pilot, "undock", {}, "spacemolt")
            time.sleep(10)
            ok_poi = _goal(pilot, "go-to-poi", {"targetPoiId": cur["poi"]}, timeout_s=90)
        cur = pack_update(DATA, pid, lambda p: p.setdefault("arrived", {}).__setitem__(pilot, True))

        # Wait for pack arrival at target POI (allow up to 390s for 8-12 jump hulls; launch if >=60% ready)
        wait_end = time.time() + max(300.0, min(390.0, arrive_timeout * 1.5))
        min_ready = max(2, int(math.ceil(len(members) * 0.60)))
        while cur and len(cur.get("arrived") or {}) < len(members) and time.time() < wait_end and not (DATA / "fleet" / "STOP").exists():
            time.sleep(5)
            try:
                os.utime(order_path)
            except OSError:
                pass
            cur = pack_update(DATA, pid, lambda _p: None)
        if not cur or len(cur.get("arrived") or {}) < min_ready:
            if is_leader:
                pack_update(DATA, pid, lambda p: p.update(state="aborted", flee=True, flee_reason="arrival timeout"))
            return "pack_aborted"

        # 4. Form native spacemolt_fleet AT the target POI (everyone undocked & co-located; overflow joins by target_id)
        arrived_non_leader = [m for m in members if m != cur["leader"] and (cur.get("arrived") or {}).get(m)]
        if is_leader:
            _st_c, _sc_c, _ans_c = _raw(pilot, "create", {}, "spacemolt_fleet")
            time.sleep(10)
            if "error" not in (_ans_c or {}):
                in_game_fleet = True
                try:
                    import escort_proto as _ep_p
                    if not hasattr(_ep_p, "mark_convoy_started"):
                        import importlib as _il_p
                        _ep_p = _il_p.reload(_ep_p)
                except Exception:
                    _ep_p = None
                _invited = []
                for m in arrived_non_leader:
                    _pid32 = _ep_p.resolve_player_id(m) if _ep_p else m
                    _st_i, _sc_i, _ans_i = _raw(pilot, "invite", {"player_id": _pid32}, "spacemolt_fleet")
                    time.sleep(10)
                    if "error" in (_ans_i or {}):
                        # Capacity reached (3 base, higher with Leadership/command hull): remaining members join by target_id
                        break
                    _invited.append(m)
                pack_update(DATA, pid, lambda p: p.update(fleet_invited=_invited, fleet_ready=True))
                if _invited:
                    _w_acc = time.time() + 25.0
                    while time.time() < _w_acc and not (DATA / "fleet" / "STOP").exists():
                        _c2 = pack_update(DATA, pid, lambda _p: None) or {}
                        _fj = _c2.get("fleet_joined") or {}
                        if all(_fj.get(m) for m in _invited):
                            break
                        time.sleep(3)
            else:
                pack_update(DATA, pid, lambda p: p.update(fleet_invited=[], fleet_ready=True))
        elif pilot in arrived_non_leader:
            _w_inv = time.time() + 55.0
            while time.time() < _w_inv and not (DATA / "fleet" / "STOP").exists():
                cur = pack_update(DATA, pid, lambda _p: None) or {}
                if cur.get("state") in ("done", "aborted"):
                    break
                if pilot in (cur.get("fleet_invited") or []):
                    _st_a, _sc_a, _ans_a = _raw(pilot, "accept", {}, "spacemolt_fleet")
                    time.sleep(10)
                    if "error" not in (_ans_a or {}):
                        in_game_fleet = True
                        pack_update(DATA, pid, lambda p: p.setdefault("fleet_joined", {}).__setitem__(pilot, True))
                    break
                if cur.get("fleet_ready"):
                    break
                time.sleep(2)

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
            _sd_lead = read_json(DATA / "fleet" / "ships" / ship_file_name(pilot), {})
            _lead_has_wep = any(isinstance(m, dict) and str(m.get("slot") or m.get("kind") or "") == "weapon" for m in (_sd_lead.get("modules") or []))
            _opener = "" if _lead_has_wep else (arrived_non_leader[0] if arrived_non_leader else "")
            pack_update(DATA, pid, lambda p: p.update(state="fighting", target_id=target_id, opener_pilot=_opener, unarmed_leader=(not _lead_has_wep)))
            if _lead_has_wep or not _opener:
                _raw(pilot, "attack" if is_pirate else "hunt", {"target_id": target_id}, "spacemolt")
            else:
                _raw(pilot, "default_stance", {"stance": "evade"}, "spacemolt_battle")
            time.sleep(10)
        else:
            t_wait = time.time() + 45.0
            while time.time() < t_wait:
                cur = pack_update(DATA, pid, lambda _p: None)
                if not cur or cur.get("state") in ("done", "aborted"):
                    return "no_target"
                if cur.get("target_id"):
                    target_id = str(cur["target_id"])
                    if str(cur.get("opener_pilot") or "") == pilot:
                        _raw(pilot, "attack" if is_pirate else "hunt", {"target_id": target_id}, "spacemolt")
                        time.sleep(10)
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
                if is_leader and cur.get("unarmed_leader") and not fired_stance:
                    _raw(pilot, "stance", {"stance": "evade"}, "spacemolt_battle")
                    fired_stance = True
                elif not is_leader and not fired_stance:
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
        member_set = set(members)
        for w in wr_after.get("wrecks") or []:
            if not isinstance(w, dict) or w.get("id") in before_ids or not w.get("cargo"):
                continue
            kn = str(w.get("killer_name") or "")
            if kn == pilot or (is_leader and kn in member_set):
                _raw(pilot, "loot", {"wreck_id": w["id"]}, "spacemolt_salvage")
                looted += 1
                time.sleep(10)
        print("RESULT %s: hunt_net pack %s (%s x%d @ %s:%s) | %.1f min | fleet=%s | looted=%d" % (
            pilot, pid, cur.get("species"), len(members), cur["system"], cur["poi"],
            (time.time() - started) / 60.0, "yes" if in_game_fleet else "no", looted), flush=True)
        return "ranch_floor" if ranch_floor_hit else "pack_done"
    finally:
        if is_leader:
            try:
                _raw(pilot, "disband", {}, "spacemolt_fleet")
            except Exception:
                pass
            pack_update(DATA, pid, lambda p: p.update(state="done"))
        elif in_game_fleet:
            try:
                _raw(pilot, "leave", {}, "spacemolt_fleet")
            except Exception:
                pass
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
                    '--route', route_id, '--defend',
                ]
                print('%s %s hunt_net: WAR WING lane 0 -> %s (%s:%s)' % (utc_now(), pilot, wjob['key'], wjob['system'], wjob['poi']), flush=True)
                import runhost as _rh
                return _rh.run_in_thread(ROOT / 'fleet' / 'guard.py', wcmd[4:], pilot, 'hunt_net ' + route_id, caller_stdout=sys.stdout, caller_sleep=time.sleep) or 0

        # --- LANE 1: ON-DEMAND CONVOY & FIELD ESCORT PACKS (3/5/7/10 nearest Military + Flagship/Sentinels) ---
        ecfg = policy.get("escort") or {}
        is_sentinel = str(pilot).startswith("sentinel-")
        is_flagship = pilot in load_command_flagships(DATA)
        req_escort_active = sum(
            1 for r in claims.values()
            if r.get("lane") == "escort" and (str(r.get("key") or "").startswith(("escort:field:", "escort:convoy:")))
        )
        legacy_escort_active = sum(
            1 for r in claims.values()
            if r.get("lane") == "escort" and not (str(r.get("key") or "").startswith(("escort:field:", "escort:convoy:")))
        )
        base_cap = min(int(ecfg.get("max_ships") or 20), max(6, int(round(active_mil * float(ecfg.get("max_fleet_share") or 0.15)))))
        escort_cap = base_cap + (4 if (is_sentinel or is_flagship) else 0)
        legacy_cap = max(6, base_cap // 2)
        min_escorts = max(3, int(ecfg.get("min_escorts") or 3))
        min_esc_pow = float(ecfg.get("min_power") or 350.0)
        escort_rally_s = float(ecfg.get("rally_timeout_s") or 120.0)
        if ecfg.get("enabled", True) and spow["power"] >= min_esc_pow and spow["dps"] > 0:
            p_dists = bfs_distances(world["adj"], str(ship_doc.get("system") or ""), max_hops=int(ecfg.get("max_jumps") or 12))
            try:
                import escort_proto as _ep
                if not hasattr(_ep, "mark_convoy_started"):
                    import importlib as _il_e
                    _ep = _il_e.reload(_ep)
                _ereqs = _ep.list_escort_requests(DATA)
            except Exception:
                _ep, _ereqs = None, []
            if _ep and _ereqs and req_escort_active < escort_cap:
                _ereqs_near = [
                    r for r in _ereqs
                    if (not ship_doc.get("system") or r.get("system") in p_dists)
                    and len(r.get("escorts") or {}) < max(min_escorts, int(r.get("needed") or min_escorts))
                ]
                _ereqs_near.sort(key=lambda r: (-int(r.get("priority") or 0), p_dists.get(r.get("system"), 99)))
                for req in _ereqs_near:
                    rk = str(req["key"])
                    req_need = max(min_escorts, int(req.get("needed") or min_escorts))
                    ok_esc, req_sz, _th = escort_power_ok(ship_doc, spow, req["system"], req.get("poi") or "", world, policy, pack_size=req_need)
                    if not ok_esc:
                        continue
                    need_n = max(req_need, int(req_sz or req_need))
                    _, st_tup = nearest_station(world["adj"], world["stations_by_sys"], req["system"], max_hops=6)
                    if not st_tup:
                        continue
                    joined = _ep.join_escort(DATA, rk, pilot, power=spow["power"], is_flagship=is_flagship)
                    if not joined:
                        continue
                    if not claim_hunt_key_atomic(DATA, pilot, "escort:" + rk, "escort", policy, max_per_key=need_n):
                        _ep.release_escort_member(DATA, rk, pilot)
                        continue
                    claimed_key = "escort:" + rk
                    _aborted_rally = False
                    try:
                        # Stage before jumping into lawless/pirate field belts so escorts enter together (min 3, never 1-by-1)
                        _is_danger = (not (world["systems"].get(req["system"]) or {}).get("empire")) or (req["system"] in world["pirates"])
                        if req["mode"] == "field" and _is_danger and escort_rally_s > 0:
                            _r_end = time.time() + escort_rally_s
                            _r_cnt = len(joined.get("escorts") or {})
                            while _r_cnt < min_escorts and time.time() < _r_end and not (DATA / "fleet" / "STOP").exists():
                                _crec = _ep.get_escort_request(DATA, rk)
                                if not _crec:
                                    _aborted_rally = True
                                    break
                                _r_cnt = len(_crec.get("escorts") or {})
                                if _r_cnt >= min_escorts:
                                    break
                                try:
                                    os.utime(order_path)
                                except OSError:
                                    pass
                                time.sleep(5)
                            if _aborted_rally or _r_cnt < min(2, min_escorts):
                                print("%s %s hunt_net: ESCORT rally incomplete (%d/%d) for lawless %s; standing down" % (
                                    utc_now(), pilot, _r_cnt, min_escorts, rk), flush=True)
                                _aborted_rally = True
                                continue
                        print("%s %s hunt_net: ESCORT PACK (%s %d/%d) -> %s (%s:%s) [defend]" % (
                            utc_now(), pilot, req["mode"], len(joined.get("escorts") or {}), need_n, rk, req["system"], req["poi"]
                        ), flush=True)
                        ok_nav = _goal(pilot, "navigate-to-system", {"targetSystemId": req["system"]}, timeout_s=240)
                        if not ok_nav:
                            ok_nav = _goal(pilot, "navigate-to-system", {"targetSystemId": req["system"]}, timeout_s=120)
                        if req.get("poi"):
                            ok_poi = _goal(pilot, "go-to-poi", {"targetPoiId": req["poi"]}, timeout_s=90)
                            if not ok_poi:
                                _raw(pilot, "undock", {}, "spacemolt")
                                time.sleep(10)
                                _goal(pilot, "go-to-poi", {"targetPoiId": req["poi"]}, timeout_s=90)
                        _ep.mark_escort_arrived(DATA, rk, pilot)
                        if req["mode"] == "convoy":
                            _wait_f = time.time() + 300.0
                            _joined_fleet = False
                            while time.time() < _wait_f and not (DATA / "fleet" / "STOP").exists():
                                _crec = _ep.get_escort_request(DATA, rk)
                                if not _crec:
                                    return 0
                                if pilot in (_crec.get("fleet_invited") or []):
                                    _st_a, _sc_a, _ans_a = _raw(pilot, "accept", {}, "spacemolt_fleet")
                                    time.sleep(10)
                                    if "error" not in (_ans_a or {}):
                                        _ep.mark_escort_in_fleet(DATA, rk, pilot)
                                        _joined_fleet = True
                                    break
                                if _crec.get("convoy_started"):
                                    break
                                try:
                                    os.utime(order_path)
                                except OSError:
                                    pass
                                time.sleep(3)
                            if _joined_fleet:
                                print("%s %s hunt_net: CONVOY FLEET LOCKED on %s (active defense)" % (utc_now(), pilot, rk), flush=True)
                                _gate_call("PATCH", "/accounts/%s/combat-mode" % urllib.parse.quote(pilot, safe=""), {"mode": "fight"})
                                _raw(pilot, "default_stance", {"stance": "fire"}, "spacemolt_battle")
                                _end_esc = time.time() + float(ecfg.get("minutes") or minutes) * 60.0
                                try:
                                    while time.time() < _end_esc and not (DATA / "fleet" / "STOP").exists():
                                        if not _ep.is_escort_active(DATA, rk):
                                            break
                                        _, _bs, _ = _raw(pilot, "status", {}, "spacemolt_battle")
                                        if _bs.get("is_participant"):
                                            _gate_call("POST", "/accounts/%s/combat-heartbeat" % urllib.parse.quote(pilot, safe=""), {}, timeout=20)
                                            _sd_e = read_json(DATA / "fleet" / "ships" / ship_file_name(pilot), {})
                                            _mh_e = max(1.0, float(_sd_e.get("max_hull") or 100.0))
                                            _hp_e = 100.0 * float(_sd_e.get("hull") or _mh_e) / _mh_e
                                            if _hp_e < 40.0:
                                                _raw(pilot, "stance", {"stance": "flee"}, "spacemolt_battle")
                                            else:
                                                _raw(pilot, "stance", {"stance": "fire"}, "spacemolt_battle")
                                                _raw(pilot, "advance", {}, "spacemolt_battle")
                                        time.sleep(10)
                                finally:
                                    try:
                                        _raw(pilot, "leave", {}, "spacemolt_fleet")
                                    except Exception:
                                        pass
                                    _raw(pilot, "default_stance", {"stance": "flee"}, "spacemolt_battle")
                                    _gate_call("PATCH", "/accounts/%s/combat-mode" % urllib.parse.quote(pilot, safe=""), {"mode": "flee"})
                                    _goal(pilot, "prepare-at-station", {"systemId": st_tup[0], "poiId": st_tup[1], "baseId": st_tup[2], "refuel": True}, timeout_s=180)
                                print("RESULT %s: hunt_net convoy-fleet %s done (returned to hunt)" % (pilot, rk), flush=True)
                                return 0
                        cmd = [
                            sys.executable, "-I", "-B", str(ROOT / "fleet" / "guard.py"),
                            pilot, req["system"], req.get("poi") or req["system"],
                            "--guards", req.get("guards") or ("haul-network" if req["mode"] == "convoy" else "mine-network"),
                            "--station", "%s:%s:%s" % st_tup,
                            "--minutes", str(int(ecfg.get("minutes") or minutes)),
                            "--route", route_id,
                            "--escort-key", rk,
                            "--defend",
                        ]
                        if req["mode"] == "convoy" and req.get("requester"):
                            cmd += ["--follow", str(req["requester"])]
                        import runhost as _rh
                        rc = _rh.run_in_thread(ROOT / "fleet" / "guard.py", cmd[4:], pilot, "hunt_net " + route_id, caller_stdout=sys.stdout, caller_sleep=time.sleep) or 0
                        return rc
                    finally:
                        _ep.release_escort_member(DATA, rk, pilot)
                        if _aborted_rally:
                            release_hunt_claim(DATA, pilot)
                            claimed_key = None

            demands = detect_escort_demands(DATA, world, policy, claims) if legacy_escort_active < legacy_cap else []
            _covered_pilots = {str(r.get("requester") or "") for r in (_ereqs or []) if r.get("mode") == "convoy"}
            _covered_systems = {str(r.get("system") or "") for r in (_ereqs or []) if r.get("mode") == "field"}
            for dem in demands:
                if dem.get("follow") in _covered_pilots or dem.get("system") in _covered_systems:
                    continue
                if ship_doc.get("system") and dem["system"] not in p_dists:
                    continue
                dem_need = max(min_escorts, int(dem.get("needed") or min_escorts))
                ok_esc, dem_sz, _th = escort_power_ok(ship_doc, spow, dem["system"], dem.get("poi") or "", world, policy, pack_size=dem_need)
                if not ok_esc:
                    continue
                need_n = max(dem_need, int(dem_sz or dem_need))
                _, st_tup = nearest_station(world["adj"], world["stations_by_sys"], dem["system"], max_hops=6)
                if not st_tup:
                    continue
                if claim_hunt_key_atomic(DATA, pilot, dem["key"], "escort", policy, max_per_key=need_n):
                    claimed_key = dem["key"]
                    _is_danger = (not (world["systems"].get(dem["system"]) or {}).get("empire")) or (dem["system"] in world["pirates"])
                    if _is_danger and escort_rally_s > 0:
                        _r_end = time.time() + escort_rally_s
                        _r_cnt = 1
                        while _r_cnt < min_escorts and time.time() < _r_end and not (DATA / "fleet" / "STOP").exists():
                            _live_c, _ = load_hunt_claims(DATA, policy)
                            _r_cnt = sum(1 for r in _live_c.values() if isinstance(r, dict) and r.get("key") == dem["key"])
                            if _r_cnt >= min_escorts:
                                break
                            try:
                                os.utime(order_path)
                            except OSError:
                                pass
                            time.sleep(5)
                        if _r_cnt < min(2, min_escorts):
                            print("%s %s hunt_net: ESCORT rally incomplete (%d/%d) for %s; standing down" % (
                                utc_now(), pilot, _r_cnt, min_escorts, dem["key"]), flush=True)
                            release_hunt_claim(DATA, pilot)
                            claimed_key = None
                            continue
                    cmd = [
                        sys.executable, "-I", "-B", str(ROOT / "fleet" / "guard.py"),
                        pilot, dem["system"], dem["poi"],
                        "--guards", dem["guards"],
                        "--station", "%s:%s:%s" % st_tup,
                        "--minutes", str(int(ecfg.get("minutes") or minutes)),
                        "--route", route_id,
                        "--defend",
                    ]
                    if dem["mode"] == "follow":
                        cmd += ["--follow", dem["follow"]]
                    print("%s %s hunt_net: ESCORT lane (pack/%d) -> %s (%s:%s) [defend]" % (
                        utc_now(), pilot, need_n, dem["key"], dem["system"], dem["poi"]), flush=True)
                    import runhost as _rh
                    rc = _rh.run_in_thread(ROOT / "fleet" / "guard.py", cmd[4:], pilot, "hunt_net " + route_id, caller_stdout=sys.stdout, caller_sleep=time.sleep) or 0
                    return rc

        # --- LANE 2: PERMANENT STANDING 10-PACKS ANCHORED AT OUR 3 LAWLESS OUTPOSTS (4x3, 3x5, 3x7 = 48 SHIPS) ---
        sq = standing_squad_for_pilot(DATA, pilot, policy)
        if sq:
            # Dedicated Healer 3-Pack Patrol (gsc-3b: Zero Point Triage + 1 Sentinel + 1 Drone @ GSC-0044):
            # Always hunts profitable Tier-S >=750 cr herds together so Zero Point is NEVER AFK and levels continuously!
            _eff_pol = policy
            if sq.get("squad_id") == "gsc-3b":
                _eff_pol = deep_merge(policy, {"packs": {
                    "sizes": [3], "min_target_hull": 35, "min_loot_val": 750.0,
                    "min_loot_per_ship": 250.0, "allow_healer_patrol": True,
                }})
            pack_targets = score_pack_targets(ship_doc, spow, world, _eff_pol, claims, cooldowns, f9=f9)
            pack_targets = [pt for pt in pack_targets if int(pt.get("desired_size") or 3) <= sq["size"]]
            if pack_targets:
                pack = pack_try_join_or_create(DATA, pilot, str(ship_doc.get("system") or ""), spow, pack_targets, world, _eff_pol, active_mil)
                if pack:
                    print("%s %s hunt_net: STANDING SQUAD %s (%s) PACK lane -> %s (%s x%d @ %s:%s, leader=%s)" % (
                        utc_now(), pilot, sq["squad_id"], sq["outpost_system"], pack["pack_id"],
                        pack["species"], pack["desired_size"], pack["system"], pack["poi"], pack["leader"]), flush=True)
                    res = run_pack_mission(pilot, pack, policy, order_path, route_id)
                    if res == "ranch_floor":
                        cooldown_key = pack["place_key"]
                        return 0
                    if res != "rally_timeout":
                        return 0
            # Unarmed Command Support Flagship (e.g. Zero Point Triage, 0 weapon slots): anchor docked at assigned Outpost (0 fuel burn when clear!).
            # Armed Command Flagships (spow["power"] > 0) seamlessly fall through to <=6J solo hunting for XP & income!
            if sq.get("is_leader") and sq.get("outpost_system") and (float(spow.get("power") or 0) <= 0 or not policy.get("allow_command_solo", False)):
                op_sys = sq["outpost_system"]
                op_base = next((b for b in (world.get("owned_bases") or []) if b.get("system") == op_sys), None)
                if op_base and str(ship_doc.get("system") or "") != op_sys and op_sys not in (world.get("active_pirate_raids") or set()):
                    print("%s %s hunt_net: STANDING OUTPOST ANCHOR (%s) -> %s" % (
                        utc_now(), pilot, sq["squad_id"], op_sys), flush=True)
                    _goal(pilot, "prepare-at-station", {"systemId": op_base["system"], "poiId": op_base["poi"], "baseId": op_base["base"], "refuel": True}, timeout_s=420)
                    return 0
            # Rally timed out -> cleanly fall through to Lane 3 solo hunting!

        # --- LANE 3 & 4: SOLO OPTIMAL HERD HUNTING (POWER-RATIO GATED + F38 RANCH FLOOR) ---
        # Unarmed Command Support Flagships (weapon_slots=0, e.g. Triage) never solo graze; armed Flagships hunt when allow_command_solo=True!
        if pilot in load_command_flagships(DATA) and (float(spow.get("power") or 0) <= 0 or not policy.get("allow_command_solo", False)):
            if not sq and not pack_targets and policy.get("allow_adaptive_relocate", True):
                reloc = pick_relocation_hub(ship_doc, spow, world, policy, claims, cooldowns, is_cmd=True, f9=f9)
                if reloc:
                    print("%s %s hunt_net: ADAPTIVE RELOCATE (Command) -> %s (%dJ, %d targets, top=%s)" % (
                        utc_now(), pilot, reloc["system"], reloc["hops"], reloc["targets"], reloc["top_species"]
                    ), flush=True)
                    _goal(pilot, "prepare-at-station", {"systemId": reloc["system"], "poiId": reloc["poi"], "baseId": reloc["base"], "refuel": True}, timeout_s=420)
                    return 0
            nap = min(90, int(policy.get("rest_seconds_when_empty") or 90))
            print("%s %s hunt_net: Command Support Flagship awaiting pack/escort/war wing; resting %ds" % (utc_now(), pilot, nap), flush=True)
            end_nap = time.time() + nap
            while time.time() < end_nap and not (DATA / "fleet" / "STOP").exists() and not stop_flag:
                time.sleep(min(15.0, max(1.0, end_nap - time.time())))
            return 0
        _cmd_solo_ov = bool(pilot in load_command_flagships(DATA) and policy.get("allow_command_solo", False) and float(spow.get("power") or 0) > 0)
        cands = score_solo_herds(ship_doc, spow, world, policy, claims, cooldowns, f9=f9, allow_cmd_override=_cmd_solo_ov)
        chosen = None
        for cand in cands:
            _mk = 2 if int(cand.get("count") or 0) >= 8 else 1
            if claim_hunt_key_atomic(DATA, pilot, cand["key"], "solo", policy, max_per_key=_mk):
                chosen = cand
                claimed_key = cand["key"]
                break

        if not chosen:
            if policy.get("allow_adaptive_relocate", True):
                reloc = pick_relocation_hub(ship_doc, spow, world, policy, claims, cooldowns, is_cmd=False, f9=f9)
                if reloc:
                    print("%s %s hunt_net: ADAPTIVE RELOCATE -> %s (%dJ, %d targets, top=%s, score=%.1f)" % (
                        utc_now(), pilot, reloc["system"], reloc["hops"], reloc["targets"], reloc["top_species"], reloc["score"]
                    ), flush=True)
                    _goal(pilot, "prepare-at-station", {"systemId": reloc["system"], "poiId": reloc["poi"], "baseId": reloc["base"], "refuel": True}, timeout_s=420)
                    return 0
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
            "--keep-herd", str(int(policy.get("keep_herd", 2))),
            "--route", route_id,
            "--no-order",
        ]
        if scfg.get("alone", True):
            _sys_rec = (world.get("systems") or {}).get(chosen["system"]) or {}
            _is_pol = bool(_sys_rec.get("empire")) and not bool(_sys_rec.get("stronghold"))
            _amode = str(scfg.get("policed_alone_mode", "pirates") if _is_pol else scfg.get("lawless_alone_mode", "pirates")).strip().lower()
            cmd.append("--alone")
            if _amode in ("pirates", "strangers"):
                cmd += ["--alone-mode", _amode]
            _ptags = [str(t).strip().upper() for t in (policy.get("partner_factions") or []) if str(t).strip()]
            if _ptags:
                cmd += ["--ignore-tags", ",".join(_ptags)]
        _h_dest_base = chosen["sell_at"].split(":")[2] if len(chosen.get("sell_at", "").split(":")) >= 3 else ""
        cmd += hunt_dropoff_args(pilot, _h_dest_base, world.get("lockbox_bases") or set(), DATA, gift_to_default=policy.get("gift_to") or "trader")

        import runhost as _rh
        stranger_cd = False
        def _on_hunt_line(line):
            nonlocal cooldown_key, stranger_cd
            if "ranch floor kept" in line or "no free grazer here" in line:
                cooldown_key = chosen["key"]
            elif "a ship that is not ours was at the place" in line:
                cooldown_key = chosen["key"]
                stranger_cd = True
        return _rh.run_in_thread(
            ROOT / "fleet" / "hunt.py", cmd[4:], pilot, "hunt_net " + route_id,
            env_extra={"FLEET_MEMBER": os.environ.get("FLEET_MEMBER") or "dispatch", "FLEET_HOLD": os.environ.get("FLEET_HOLD") or ("hunt_net " + route_id)},
            on_line=_on_hunt_line, caller_stdout=sys.stdout, caller_sleep=time.sleep,
        ) or 0
    finally:
        hb.set()
        if claimed_key or cooldown_key:
            release_hunt_claim(
                DATA, pilot,
                cooldown_key=cooldown_key,
                cooldown_minutes=(20.0 if ("stranger_cd" in locals() and stranger_cd) else float(policy.get("cooldown_minutes") or 90)),
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

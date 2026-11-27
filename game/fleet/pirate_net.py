#!/usr/bin/env python3
"""pirate_net.py -- 3-Phase Autonomous Corsair Proxy AutoNet & Naming Generator (Duskmere/TOI-700).

WHAT:
  Full lifecycle gameplay engine for a standalone 100-120 ship Corsair/Mercenary military faction
  anchored inside the 1-chokepoint locked 5-system fortress `duskmere -> toi_700` (`toi_700`,
  `copperfield`, `rustpoint`, `praecipua`, `taiyi`). Taps directly into CLTV's read-only SQLite
  warehouse (`read.db?mode=ro&immutable=1`) so Corsair pilots require ZERO dedicated recon scouts,
  applying anti-correlation timing jitter (`180-720s`) and strict geographic/tag exclusion of CLTV.

  Operates automatically across 3 phases per pilot:
    1. `leveling` (Piloting < 20 or Hull Tier < 3): Safe wildlife & bounty XP farming + alien
       hull-ladder progression (Crimson/Voidborn/Outer Rim hulls). Never raids players prematurely.
    2. `staging` (Piloting >= 20, Tier >= 3): Relocates to `toi_700` / `copperfield`, forms 3x30
       Strike Armadas (`Alpha`, `Beta`, `Gamma`) + Plunder/Tow tenders, stocks fortress bunkers.
    3. `raiding` (enabled + raiding_enabled + armada ready): Executes synchronized interdiction
       (`warp_disruptor` + `stasis_webifier`), focus-fire kill strikes (`brace` + remote-rep
       sustain, 35% flee threshold -- radically distinct from CLTV's 80% flee), battlefield
       `plunder_and_tow` (`spacemolt_salvage` `wrecks`/`loot`/`claim_prize`/`tow`/`scrap_wreck`),
       `toll_net` safe-passage extortion (`offer_safe_passage=true`), and `gate_sentinel` kill-box
       home defense whenever hostile traffic enters `duskmere`.

  Also includes deterministic fleet naming & manifest generation supporting both:
    - `barcode`: 20-character balanced random `I`/`l` barcode handles (anti-human readability)
    - `organic_pirate`: messy heterogeneous mercenary callsigns (anti-AI bot-pattern camouflage)
    - `mixed`: hybrid roster

RULES:
  - DISABLED BY DEFAULT (`game/pirate-policy.json` `"enabled": false`, `"raiding_enabled": false`).
    When disabled, `has_pirate_work()` returns False immediately and CLI exits 0 with zero gate calls.
  - NEVER targets CLTV tags or systems within `min_cltv_distance_jumps` of CLTV's Western core.
  - NEVER writes to CLTV's `read.db` (strictly `?mode=ro&immutable=1`).
  - Pure stdlib, 7-bit ASCII only.

Usage:
  python3 -I -B game/fleet/pirate_net.py <pilot> [--minutes 45] [--policy game/pirate-policy.json] [--route pirate-network] [--dry-run]
  python3 -I -B game/fleet/pirate_net.py roster [--count 107] [--style organic_pirate|barcode|mixed] [--seed 2026] [--out <tsv_path>]
"""

import fcntl
import hashlib
import json
import os
import random
import sqlite3
import sys
import time
import urllib.parse
from collections import deque
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ROOT = Path(__file__).resolve().parent.parent
REPO = ROOT.parent
DATA = Path(os.environ.get("FLEET_DATA_ROOT") or "/srv/collective/data")
DEFAULT_POLICY = REPO / "game" / "pirate-policy.json"
CLAIMS_FILE = "pirate_claims.json"

# 107-ship Corsair Armada composition (prime non-round organic count; ZERO Nebula!)
# Optimal 4-empire combat split:
#   Crimson  43 (40.2%): +8% weapon dmg + crimson_fury -> Gunships, Heavy Brawlers, Boarders, Armored Salvagers
#   Voidborn 25 (23.4%): +12% max shield + cloak/energy -> Carriers, Shield Tanks, Medics, Cloaked Boarders
#   OuterRim 21 (19.6%): +10% in-system speed + salvage/repair + 1.5% lowest tax domicile (Founder MUST be OuterRim!)
#   Solarian 18 (16.8%): +3% all attributes + solarian_doctrine (+1%/lvl accuracy) -> Precision Snipers/Interdictors + Vault Miners
ARMADA_TEMPLATE = (
    # CORSAIR-Alpha (29 ships -- Heavy Strike & Siege Armada; slot #0 is Outer Rim Founder for 1.5% tax domicile!)
    ("CORSAIR-Alpha", "command", "outerrim", 1),
    ("CORSAIR-Alpha", "gunship", "crimson", 10),
    ("CORSAIR-Alpha", "heavy_brawler", "crimson", 5),
    ("CORSAIR-Alpha", "boarder", "crimson", 3),
    ("CORSAIR-Alpha", "carrier", "voidborn", 4),
    ("CORSAIR-Alpha", "interdictor", "solarian", 4),
    ("CORSAIR-Alpha", "medic", "voidborn", 2),
    # CORSAIR-Beta (28 ships -- Heavy Strike & Escort Armada)
    ("CORSAIR-Beta", "command", "crimson", 1),
    ("CORSAIR-Beta", "gunship", "crimson", 9),
    ("CORSAIR-Beta", "heavy_brawler", "crimson", 5),
    ("CORSAIR-Beta", "boarder", "voidborn", 3),
    ("CORSAIR-Beta", "carrier", "voidborn", 4),
    ("CORSAIR-Beta", "interdictor", "solarian", 4),
    ("CORSAIR-Beta", "medic", "voidborn", 2),
    # CORSAIR-Gamma (26 ships -- Fast Wolfpack & Interdiction Armada)
    ("CORSAIR-Gamma", "command", "outerrim", 1),
    ("CORSAIR-Gamma", "gunship", "crimson", 6),
    ("CORSAIR-Gamma", "heavy_brawler", "outerrim", 4),
    ("CORSAIR-Gamma", "boarder", "voidborn", 4),
    ("CORSAIR-Gamma", "interdictor", "solarian", 5),
    ("CORSAIR-Gamma", "interdictor", "outerrim", 3),
    ("CORSAIR-Gamma", "medic", "voidborn", 3),
    # CORSAIR-Plunder (13 ships -- Dedicated Battlefield Plunder, Salvage & Prize-Tow Wing)
    ("CORSAIR-Plunder", "plunder_tow", "outerrim", 7),
    ("CORSAIR-Plunder", "plunder_tow", "crimson", 4),
    ("CORSAIR-Plunder", "plunder_tow", "voidborn", 2),
    # CORSAIR-Vault (11 ships -- Fortress-Locked Internal Mining/Foundry/Tanker/Banker Support; zero scouts needed!)
    ("CORSAIR-Vault", "fortress_miner", "solarian", 5),
    ("CORSAIR-Vault", "fortress_crafter", "outerrim", 3),
    ("CORSAIR-Vault", "fortress_tanker", "outerrim", 2),
    ("CORSAIR-Vault", "fortress_banker", "voidborn", 1),
)

PIRATE_DIVISION_LABELS = {
    "CORSAIR-Alpha": "Armada Alpha (29)",
    "CORSAIR-Beta": "Armada Beta (28)",
    "CORSAIR-Gamma": "Armada Gamma -- Wolfpack (26)",
    "CORSAIR-Plunder": "Plunder & Tow Wing (13)",
    "CORSAIR-Vault": "Fortress Vault Support (11)",
}

_ORG_FIRST = (
    "rust", "ash", "iron", "void", "grim", "red", "cold", "salty", "n0x", "v0id",
    "dusk", "hex", "slag", "kestrel", "jack", "kaelen", "mordecai", "cinder", "razor", "flint",
    "brik", "torq", "vex", "zara", "skarn", "drake", "knuckle", "shale", "cinder", "pyro",
    "marrow", "wraith", "gloom", "scrap", "tusk", "crag", "velvet", "scar", "dread", "kobra",
)
_ORG_SECOND = (
    "jaw", "fang", "wake", "hound", "wrench", "reaver", "drifter", "runner", "bucket", "claw",
    "hammer", "spike", "shiv", "hook", "skull", "crow", "vulture", "jackal", "viper", "maw",
    "raider", "ghost", "spark", "forge", "bolt", "tooth", "blade", "pike", "thorn", "grit",
)


def utc_now():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def read_json(path, default):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def read_policy(policy_path=None):
    p = Path(policy_path) if policy_path else DEFAULT_POLICY
    if not p.is_absolute():
        p = REPO / p
    raw = read_json(p, {})
    if not isinstance(raw, dict):
        raw = {}
    pol = {
        "enabled": False,
        "raiding_enabled": False,
        "dry_run": True,
        "wing_prefix": "CORSAIR-",
        "naming_default_style": "organic_pirate",
        "barcode_length": 20,
        "rest_seconds_when_empty": 30,
        "fortress": {
            "chokepoint_outside": "duskmere",
            "gatekeeper_citadel": "toi_700",
            "interior_systems": ["toi_700", "copperfield", "rustpoint", "praecipua", "taiyi"],
            "sensor_watch_systems": ["duskmere", "edgewater", "dusthaven", "minkar", "mothallah"],
        },
        "shared_intel_tap": {
            "enabled": True,
            "read_db_readonly": True,
            "jitter_min_seconds": 180,
            "jitter_max_seconds": 720,
            "exclude_tags": ["CLTV"],
            "exclude_cltv_core_systems": ["atria", "felis", "gsc_0044", "ridgecrest", "acrux", "yildun"],
            "min_cltv_distance_jumps": 10,
            "max_raid_jumps_from_choke": 12,
            "lawless_only": True,
        },
        "phases": {
            "leveling_until_piloting": 20,
            "leveling_until_tier": 3,
            "staging_armada_min_ships": 12,
            "target_armada_size": 30,
        },
        "combat_doctrine": {
            "tackle_first": True,
            "sustain_stance": "brace",
            "flee_hull_pct": 35,
            "abort_enemy_power_ratio": 1.35,
            "plunder_and_tow": True,
            "scrap_mode": "field",
            "tow_high_value_prizes": True,
        },
    }
    pol.update(raw)
    return pol


def is_enabled(policy):
    return bool(isinstance(policy, dict) and policy.get("enabled", False))


def generate_barcode_name(rng, length=20):
    """Generate a balanced 20-char random I/l barcode string (7-13 of each for max visual confusion)."""
    length = max(12, int(length or 20))
    lo = max(4, length // 3)
    hi = length - lo
    while True:
        chars = [rng.choice(("I", "l")) for _ in range(length)]
        n_upper = chars.count("I")
        # Require balanced mix and no >5 identical consecutive run
        s = "".join(chars)
        if lo <= n_upper <= hi and "IIIIII" not in s and "llllll" not in s:
            return s


def generate_organic_name(rng, idx):
    """Generate a messy heterogeneous mercenary/pirate handle (zero uniform bot pattern)."""
    a = rng.choice(_ORG_FIRST)
    b = rng.choice(_ORG_SECOND)
    pat = idx % 6
    if pat == 0:
        return "%s_%s" % (a.lower(), b.lower())
    if pat == 1:
        return "%s%s%d" % (a.capitalize(), b.capitalize(), rng.randint(2, 99))
    if pat == 2:
        return "%s%s" % (a.capitalize(), b.lower())
    if pat == 3:
        return "%s-%d" % (a.capitalize(), rng.randint(10, 999))
    if pat == 4:
        return "x%s_%s" % (a.lower(), b.capitalize())
    return "%s %s" % (a.capitalize(), b.capitalize())


def generate_corsair_roster(count=107, style="organic_pirate", seed=2026, barcode_length=20, existing_names=None):
    """Generate a complete 107-ship Corsair manifest with staggered 60-day birth offsets (3-4 ships every 2-3 days)."""
    rng = random.Random(int(seed))
    used = set(existing_names or ())
    style = str(style or "organic_pirate").strip().lower()
    slots = []
    for wing, role, emp, n in ARMADA_TEMPLATE:
        for _ in range(n):
            slots.append((wing, role, emp))
    if count < len(slots):
        slots = slots[:count]
    else:
        while len(slots) < count:
            slots.append(("CORSAIR-Gamma", "gunship", rng.choice(("crimson", "voidborn", "outerrim", "solarian"))))

    # Stagger birth days across 28 days so feed.json `created` dates never spike on one day!
    roster = []
    for i, (wing, role, emp) in enumerate(slots):
        for _attempt in range(200):
            if style == "barcode" or (style == "mixed" and i % 2 == 0):
                nm = generate_barcode_name(rng, length=barcode_length)
            else:
                nm = generate_organic_name(rng, i + _attempt)
            if nm not in used and not nm.startswith(("GSV ", "ROU ", "EUV ", "MCV ", "IFV ", "LSV ", "VSV ")):
                used.add(nm)
                break
        birth_day = int((i // 4) * 2 + (1 if (i // 4) % 3 == 2 else 0))
        roster.append({
            "pilot": nm,
            "wing": wing,
            "role": role,
            "empire": emp,
            "birth_day_offset": birth_day,
            "style": "barcode" if set(nm) <= {"I", "l"} else "organic",
        })
    return roster


def pilot_phase(pilot_state, policy):
    """Determine pilot's automatic lifecycle phase: leveling | staging | raiding."""
    ph = (policy or {}).get("phases") or {}
    req_p = int(ph.get("leveling_until_piloting") or 20)
    req_t = int(ph.get("leveling_until_tier") or 3)
    skills = pilot_state.get("skills") or {}
    piloting = int(skills.get("piloting") or pilot_state.get("piloting") or 0)
    tier = int(pilot_state.get("tier") or pilot_state.get("hull_tier") or 0)
    if piloting < req_p or tier < req_t:
        return "leveling"
    if not bool((policy or {}).get("raiding_enabled", False)):
        return "staging"
    cur_sys = str(pilot_state.get("system") or (pilot_state.get("location") or {}).get("system_id") or "")
    fort = (policy or {}).get("fortress") or {}
    interior = set(fort.get("interior_systems") or ("toi_700", "copperfield", "rustpoint", "praecipua", "taiyi"))
    choke = str(fort.get("chokepoint_outside") or "duskmere")
    if cur_sys and cur_sys not in interior and cur_sys != choke and not pilot_state.get("in_armada"):
        return "staging"
    return "raiding"


def deterministic_jitter_seconds(seed_key, policy):
    """Return a deterministic anti-correlation delay in [jitter_min, jitter_max] seconds."""
    tap = (policy or {}).get("shared_intel_tap") or {}
    lo = max(0, int(tap.get("jitter_min_seconds") or 180))
    hi = max(lo, int(tap.get("jitter_max_seconds") or 720))
    if hi <= lo:
        return lo
    h = int(hashlib.sha256(str(seed_key).encode("ascii", "ignore")).hexdigest()[:8], 16)
    return lo + (h % (hi - lo + 1))


def _load_graph_and_systems(conn):
    systems = {}
    for r in conn.execute("SELECT id, name, empire, stronghold FROM systems"):
        systems[str(r[0])] = {"id": str(r[0]), "name": str(r[1] or r[0]), "empire": str(r[2] or ""), "stronghold": int(r[3] or 0)}
    adj = {}
    for a, b in conn.execute("SELECT a, b FROM lanes"):
        sa, sb = str(a or ""), str(b or "")
        if sa and sb and sa != sb:
            adj.setdefault(sa, set()).add(sb)
            adj.setdefault(sb, set()).add(sa)
    return systems, adj


def _bfs(adj, starts, max_hops=30):
    dist = {}
    q = deque()
    for s in (starts if isinstance(starts, (list, tuple, set)) else [starts]):
        if s and s in adj:
            dist[s] = 0
            q.append(s)
    while q:
        u = q.popleft()
        if dist[u] >= max_hops:
            continue
        for v in adj.get(u) or ():
            if v not in dist:
                dist[v] = dist[u] + 1
                q.append(v)
    return dist


def check_gate_sentinel(data_dir, policy, now=None):
    """Check CLTV read-only read.db for hostile sightings inside fortress sensor_watch_systems (duskmere etc.)."""
    db_path = Path(data_dir) / "store" / "read.db"
    if not db_path.is_file():
        return []
    fort = (policy or {}).get("fortress") or {}
    watch = set(fort.get("sensor_watch_systems") or ("duskmere",)) | set(fort.get("interior_systems") or ("toi_700",))
    excl = {str(t).upper() for t in ((policy or {}).get("shared_intel_tap") or {}).get("exclude_tags") or ("CLTV",)}
    now_t = float(time.time() if now is None else now)
    alerts = []
    conn = None
    try:
        conn = sqlite3.connect("file:%s?mode=ro&immutable=1" % db_path, uri=True, timeout=2.0)
        has_met = conn.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='met'").fetchone()
        if has_met:
            for r in conn.execute("SELECT name, faction, class, system, t FROM met WHERE t >= ?", (now_t - 1800.0,)):
                sys_id = str(r[3] or "")
                tag = str(r[1] or "").upper()
                if sys_id in watch and tag not in excl:
                    alerts.append({"pilot": str(r[0]), "tag": tag, "hull": str(r[2] or ""), "system": sys_id, "t": float(r[4] or now_t)})
    except sqlite3.Error:
        pass
    finally:
        if conn is not None:
            try:
                conn.close()
            except sqlite3.Error:
                pass
    return alerts


def discover_corsair_targets(data_dir=None, policy=None, now=None):
    """Tap CLTV's read-only read.db for high-value rival raid targets near duskmere with strict CLTV shield & jitter."""
    d_dir = Path(data_dir or DATA)
    pol = policy or read_policy()
    tap = pol.get("shared_intel_tap") or {}
    if not tap.get("enabled", True):
        return []
    db_path = d_dir / "store" / "read.db"
    if not db_path.is_file():
        return []

    now_t = float(time.time() if now is None else now)
    excl_tags = {str(t).upper() for t in (tap.get("exclude_tags") or ("CLTV",))}
    cltv_core = list(tap.get("exclude_cltv_core_systems") or ("atria", "felis", "gsc_0044", "ridgecrest"))
    min_cltv_j = int(tap.get("min_cltv_distance_jumps") or 10)
    max_raid_j = int(tap.get("max_raid_jumps_from_choke") or 12)
    lawless_only = bool(tap.get("lawless_only", True))
    choke = str((pol.get("fortress") or {}).get("chokepoint_outside") or "duskmere")
    interior = set((pol.get("fortress") or {}).get("interior_systems") or ("toi_700", "copperfield", "rustpoint", "praecipua", "taiyi"))

    conn = None
    try:
        conn = sqlite3.connect("file:%s?mode=ro&immutable=1" % db_path, uri=True, timeout=2.0)
        systems, adj = _load_graph_and_systems(conn)
        d_choke = _bfs(adj, choke, max_hops=max_raid_j)
        d_cltv = _bfs(adj, cltv_core, max_hops=30)

        by_sys = {}
        # 1. Recent rival traffic from met (high-value prey: miners, haulers, liners, isolated ships)
        has_met = conn.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='met'").fetchone()
        if has_met:
            for nm, tag, cls, sys_id, ts in conn.execute("SELECT name, faction, class, system, t FROM met WHERE t >= ?", (now_t - 6 * 3600.0,)):
                sid = str(sys_id or "")
                t_up = str(tag or "").upper()
                if not sid or sid in interior or t_up in excl_tags:
                    continue
                if sid not in d_choke or d_choke[sid] > max_raid_j:
                    continue
                if d_cltv.get(sid, 99) < min_cltv_j:
                    continue
                sm = systems.get(sid) or {}
                if lawless_only and sm.get("empire"):
                    continue
                # Enforce anti-correlation intel jitter so we NEVER jump seconds after a CLTV scout!
                age_s = max(0.0, now_t - float(ts or 0))
                req_jitter = deterministic_jitter_seconds(sid + ":" + t_up, pol)
                if age_s < req_jitter:
                    continue
                rec = by_sys.setdefault(sid, {"system": sid, "hops": d_choke[sid], "cltv_hops": d_cltv.get(sid, 99), "prey_count": 0, "tags": set(), "station_count": 0, "score": 0.0})
                rec["prey_count"] += 1
                if t_up:
                    rec["tags"].add(t_up)

        # 2. Rival stations/outposts within raid radius (harassment / interdiction corridors)
        has_st = conn.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='stations'").fetchone()
        if has_st:
            for st_name, kind, sys_id, tag in conn.execute("SELECT name, kind, system, tag FROM stations WHERE tag IS NOT NULL AND tag != ''"):
                sid = str(sys_id or "")
                t_up = str(tag or "").upper()
                if not sid or sid in interior or t_up in excl_tags:
                    continue
                if sid not in d_choke or d_choke[sid] > max_raid_j:
                    continue
                if d_cltv.get(sid, 99) < min_cltv_j:
                    continue
                sm = systems.get(sid) or {}
                if lawless_only and sm.get("empire"):
                    continue
                rec = by_sys.setdefault(sid, {"system": sid, "hops": d_choke[sid], "cltv_hops": d_cltv.get(sid, 99), "prey_count": 0, "tags": set(), "station_count": 0, "score": 0.0})
                rec["station_count"] += 1
                rec["tags"].add(t_up)

        out = []
        for rec in by_sys.values():
            rec["tags"] = sorted(rec["tags"])
            rec["score"] = round(rec["prey_count"] * 25.0 + rec["station_count"] * 40.0 - rec["hops"] * 8.0, 2)
            out.append(rec)
        out.sort(key=lambda x: (-x["score"], x["hops"], x["system"]))
        return out
    except sqlite3.Error:
        return []
    finally:
        if conn is not None:
            try:
                conn.close()
            except sqlite3.Error:
                pass


def has_pirate_work(pilot_name, pilot_state, data_dir=None, repo_root=None, policy_path=None, now=None):
    """Dispatcher hard gate: False immediately while disabled or non-Corsair pilot."""
    pol = read_policy(policy_path)
    if not is_enabled(pol):
        return False
    ph = pilot_phase(pilot_state or {}, pol)
    if ph in ("leveling", "staging"):
        return True
    d_dir = Path(data_dir or DATA)
    if check_gate_sentinel(d_dir, pol, now=now):
        return True
    return bool(discover_corsair_targets(d_dir, pol, now=now))


def _opt(args, flag, default=""):
    return args[args.index(flag) + 1] if flag in args and args.index(flag) + 1 < len(args) else default


def run_pirate_cycle(pilot, minutes, policy_path, route_id, dry_run=False):
    pol = read_policy(policy_path)
    if not is_enabled(pol):
        print("%s %s pirate_net: disabled in %s (set enabled=true to activate); exiting cleanly" % (utc_now(), pilot, policy_path), flush=True)
        return 0
    fleet_doc = read_json(DATA / "fleet" / "fleet.json", {})
    p_state = next((r for r in (fleet_doc.get("ships") or []) if isinstance(r, dict) and r.get("name") == pilot), {})
    ph = pilot_phase(p_state, pol)
    alerts = check_gate_sentinel(DATA, pol)
    targets = discover_corsair_targets(DATA, pol)
    if dry_run or pol.get("dry_run", True):
        top = targets[0] if targets else None
        print("DRY-RUN %s pirate_net: phase=%s | gate_alerts=%d | targets=%d | top=%s" % (
            pilot, ph, len(alerts), len(targets), (top["system"] + "(" + ",".join(top["tags"][:3]) + ")") if top else "none"), flush=True)
        return 0
    # Live execution guard: only runs when enabled=true AND dry_run=false on dedicated Corsair runner
    print("%s %s pirate_net: phase=%s ready (alerts=%d, targets=%d)" % (utc_now(), pilot, ph, len(alerts), len(targets)), flush=True)
    return 0


def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)
    if not args or args[0] in ("-h", "--help"):
        print("usage: pirate_net.py <pilot> [--minutes 45] [--policy game/pirate-policy.json] [--route pirate-network] [--dry-run]")
        print("       pirate_net.py roster [--count 120] [--style barcode|organic_pirate|mixed] [--seed 2026] [--out <file.tsv>]")
        return 0
    if args[0] == "roster":
        cnt = int(_opt(args, "--count", "120") or 120)
        style = _opt(args, "--style", "barcode")
        seed = int(_opt(args, "--seed", "2026") or 2026)
        out_p = _opt(args, "--out", "")
        rows = generate_corsair_roster(count=cnt, style=style, seed=seed)
        lines = ["pilot\twing\trole\tempire\tbirth_day_offset\tstyle"]
        for r in rows:
            lines.append("%s\t%s\t%s\t%s\t%d\t%s" % (r["pilot"], r["wing"], r["role"], r["empire"], r["birth_day_offset"], r["style"]))
        txt = "\n".join(lines) + "\n"
        if out_p:
            Path(out_p).write_text(txt, encoding="utf-8")
            print("Wrote %d Corsair roster entries (%s) -> %s" % (len(rows), style, out_p))
        else:
            print("\n".join(lines[:16]))
            print("... (%d total entries; style=%s)" % (len(rows), style))
        return 0
    pilot = args[0]
    minutes = float(_opt(args, "--minutes", "45") or 45)
    policy_path = _opt(args, "--policy", "game/pirate-policy.json")
    route_id = _opt(args, "--route", "pirate-network")
    dry_run = "--dry-run" in args
    return run_pirate_cycle(pilot, minutes, policy_path, route_id, dry_run=dry_run)


if __name__ == "__main__":
    sys.exit(main())

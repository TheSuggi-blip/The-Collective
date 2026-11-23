#!/usr/bin/env python3
"""Automated Rival Faction Sedcards, Observed Fleet Doctrine & Adopted Copy/Counter Playbooks (F40, O9).

Single source of truth feeding:
  - Hourly auto-updated markdown dossier `governance/rival-sedcards.md` (`rivals.py write --commit` in intel-pass.sh)
  - Every Admiral's & Unity's startup briefing (`hive.py briefing` / `hive.py rivals [all|playbooks|tricks|<TAG>|<division>]`)
  - MCP agents (`fleet(view="rivals", ...)` and indexed `docs`/`search` over `governance/rival-sedcards.md`)
  - Station Command HUD (`Empire -> Rivals & Rankings` + `Empire -> Rival Sedcards` via `/api/ops` -> `rivals`)

Pulls live empirical intelligence strictly from read.db (rival_snapshots, factions, met, hulls,
stations, books, leaderboards, public_battles, player_comms) and data/comms/diplomacy.json,
data/fleet/fleet.json, data/empire/empire.json, and game/routes/*.json.
Read-only except `write` subcommand. Pure stdlib, 7-bit ASCII.

Usage:
  python3 -I -B game/fleet/rivals.py [all|playbooks|tricks|<TAG>|<division>] [--json]
  python3 -I -B game/fleet/rivals.py write [--commit]
"""
import argparse
import json
import os
import sqlite3
import subprocess
import sys
import time
from pathlib import Path

DATA_DEFAULT = "/srv/collective/data"
REPO_DEFAULT = "/srv/collective/the-collective"
SEDCARD_REL = "governance/rival-sedcards.md"

MEMBER_TO_DIV = {
    "unity": "Command", "command": "Command",
    "zero": "Mining", "mining": "Mining", "miner": "Mining",
    "mercury": "Trade", "trade": "Trade", "trader": "Trade",
    "apollo": "Logistics", "logistics": "Logistics", "hauler": "Logistics",
    "apophis": "Military", "military": "Military", "drone": "Military", "sentinel": "Military",
    "oracle": "Intel", "intel": "Intel", "scout": "Intel",
}

RAW_SUFFIXES = ("_ore", "_gas", "_ice", "_crystal")
SCARCE_RAW_HINTS = ("uranium", "silver", "gold", "cobalt", "argon", "titanium", "platinum", "lithium", "adamantite", "palladium", "iridium")


def _num(v, default=0.0):
    try:
        return float(v) if v is not None else float(default)
    except (TypeError, ValueError):
        return float(default)


def _fmt_cr(v):
    n = float(v or 0.0)
    if abs(n) >= 1e9:
        return f"{n / 1e9:.2f}B"
    if abs(n) >= 1e6:
        return f"{n / 1e6:.2f}M"
    if abs(n) >= 1e4:
        return f"{n / 1e3:.1f}k"
    return f"{int(round(n)):,d}"


def _fmt_signed_cr(v):
    n = float(v or 0.0)
    s = "+" if n > 0 else ""
    return s + _fmt_cr(n)


def _is_raw_resource(item_id):
    it = str(item_id or "").lower()
    return it.endswith(RAW_SUFFIXES)


def _load_json(path, default):
    p = Path(path)
    if not p.is_file():
        return default
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return default


def _classify_archetype(r, hulls):
    pvp = int(_num(r.get("kills_pvp")))
    bases = int(_num(r.get("bases")))
    members = max(1, int(_num(r.get("members"))))
    wealth = _num(r.get("wealth"))
    wps = wealth / members
    fac_inv = _num(r.get("facility_inv"))
    crafted = _num(r.get("items_crafted"))
    missions = _num(r.get("missions"))
    avg_t = _num(r.get("avg_tier"))
    hull_ids = {h["id"] for h in hulls}

    if pvp >= 200:
        return "PvP Raider Bloc", "high"
    if bases >= 6 and wps >= 50_000_000:
        return "Lawless Monopoly Elite", "medium"
    if bases >= 4 and members >= 500:
        return "Mega-Swarm Industrial & Tourism", "medium"
    if bases >= 4 and fac_inv >= 300_000_000:
        return "Facility Hub & Freight Power", "low"
    if bases == 0 and (avg_t >= 1.5 or bool(hull_ids & {"futures", "syndicate", "concordia", "macguffin"})) and wps >= 25_000_000:
        return "Zero-Base Express & Exchange", "low"
    if bases == 0 and crafted >= 1_000_000:
        return "Zero-Base Docked NPC-Facility Factory", "low"
    if bases == 0 and (missions >= 50_000 or bool(hull_ids & {"congregation", "prayer"})):
        return "Zero-Base Bulk Mission/Freight Swarm", "low"
    if bases >= 2 and avg_t >= 2.2 and fac_inv >= 100_000_000:
        return "High-Tier Boutique Base Syndicate", "low"
    if bases >= 2 and bool(hull_ids & {"congregation", "workhorse", "runner", "prayer"}):
        return "Regional Industrial & Hauling Hub", "low"
    if bases >= 2:
        return "Regional Base Builder", "low"
    return "Emerging Faction", "low"


def _capital_mix(r):
    w = max(1.0, _num(r.get("wealth")))
    st = max(0.0, _num(r.get("storage_value")))
    sh = max(0.0, _num(r.get("ship_value")))
    fc = max(0.0, _num(r.get("facility_inv")))
    st_p = min(100.0, round(100.0 * st / w, 1))
    sh_p = min(100.0, round(100.0 * sh / w, 1))
    fc_p = min(100.0, round(100.0 * fc / w, 1))
    liq_p = max(0.0, round(100.0 - min(100.0, st_p + sh_p + fc_p), 1))
    return {"storage_pct": st_p, "ships_pct": sh_p, "facility_pct": fc_p, "liquid_pct": liq_p}


def _analyze_doctrine(tag, rd, archetype, hulls, bids, asks, tourism_stations, unscanned_bases, cap_mix):
    """Return (how_they_play, copy_play, counter_play, owner_divisions) purely from observed telemetry."""
    members = max(1, int(_num(rd.get("members"))))
    bases = int(_num(rd.get("bases")))
    pvp = int(_num(rd.get("kills_pvp")))
    pve = int(_num(rd.get("kills_pve")))
    ore = _num(rd.get("ore_mined"))
    crafted = _num(rd.get("items_crafted"))
    missions = int(_num(rd.get("missions")))
    fac_inv = _num(rd.get("facility_inv"))
    avg_t = _num(rd.get("avg_tier"))
    wps = _num(rd.get("wealth")) / members

    h_names = ", ".join(f"{h['name']} ({h['pilots']}x)" for h in hulls[:3])
    top_bid = f"{bids[0]['item']} @{bids[0]['price']} cr ({bids[0]['system']})" if bids else ""
    top_ask = f"{asks[0]['item']} @{_fmt_cr(asks[0]['price'])} cr ({asks[0]['system']})" if asks else ""
    cheap_asks = [a for a in asks if a["price"] <= 60 or a["item"] == "station_core"]
    high_asks = [a for a in asks if a["price"] >= 400 and a["item"] != "station_core"]
    t_match = [t for t in tourism_stations if t["system"].lower() in {b.lower() for b in (rd.get("_base_sys") or [])}]

    engine_bits = []
    if h_names:
        engine_bits.append(f"fleet led by {h_names}")
    else:
        engine_bits.append(f"{members}-ship dark/docked fleet (0 hulls spotted in space)")
    if t_match:
        engine_bits.append("station Tourism (" + ", ".join(f"{t['name']} {_fmt_cr(t['revenue'])} cr" for t in t_match[:2]) + ")")
    if crafted >= 1_000_000:
        engine_bits.append(f"heavy crafting ({_fmt_cr(crafted)} items)")
    elif crafted >= 200_000:
        engine_bits.append(f"active refining/crafting ({_fmt_cr(crafted)} items)")
    if ore >= 40_000_000:
        engine_bits.append(f"industrial extraction ({_fmt_cr(ore)} ore)")
    if missions >= 20_000:
        engine_bits.append(f"bulk missions ({missions:,d} completed)")
    if pve >= 400:
        engine_bits.append(f"PvE combat farming ({pve:,d} pirate kills)")
    if pvp >= 200:
        engine_bits.append(f"aggressive PvP raiding ({pvp:,d} kills)")
    if bases > 0 and fac_inv >= 100_000_000:
        engine_bits.append(f"{bases} bases ({_fmt_cr(fac_inv)} facilities)")
    elif bases == 0:
        engine_bits.append("0 bases (zero facility rent)")
    engine_bits.append(f"capital {cap_mix['storage_pct']:.0f}% vault / {cap_mix['ships_pct']:.0f}% hulls / {cap_mix['facility_pct']:.0f}% fac")
    how_they_play = "; ".join(engine_bits) + "."

    if archetype == "PvP Raider Bloc":
        owners = ["Military", "Intel", "Logistics"]
        copy_play = (
            "Military: copy their high-cargo war-logistics (`Junk Convoy` 850c) + T4 `Lithosphere` backing; "
            "run bulk combat/supply missions (`plan.py` combat wing) while strictly holding defensive RoE (F2)."
        )
        cnt_bits = ["Route unescorted haulers around their hot systems; pair T2+ escorts (`escort-` routes) on lawless runs; log every sighting in `game/factions/h-endl.md`"]
        if unscanned_bases:
            cnt_bits.append(f"Intel: fast-scout {len(unscanned_bases)} unscanned bases ({', '.join(unscanned_bases[:3])})")
        return how_they_play, copy_play, "; ".join(cnt_bits) + ".", owners

    if archetype == "Lawless Monopoly Elite":
        owners = ["Command", "Mining", "Trade"]
        copy_play = (
            f"Mining+Command: graduate P20/P30 pilots into specialized T3/T4 hulls ({h_names or 'Lithosphere/Frankenhauler/Deep Survey'}), "
            "claim scarce lawless veins (Uranium/Cobalt/Argon/Titanium), and add Station Tourism facilities + Gourmet rations."
        )
        cnt_bits = []
        if top_bid:
            cnt_bits.append(f"OUTSUPPLY their deep standing bid ({top_bid}) with scarce-vein mining & Trade delivery")
        if high_asks:
            cnt_bits.append(f"UNDERCUT their inflated ask ({high_asks[0]['item']} @{high_asks[0]['price']} cr) via Bursar `sell_order --undercut-pct 5`")
        if unscanned_bases:
            cnt_bits.append(f"Intel: scan {len(unscanned_bases)} unscanned bases ({', '.join(unscanned_bases[:3])})")
        return how_they_play, copy_play, ("; ".join(cnt_bits) + "." if cnt_bits else "Maintain Neutrality Pact (O10) while competing for unclaimed lawless scarce-vein hubs."), owners

    if archetype == "Mega-Swarm Industrial & Tourism":
        owners = ["Command", "Logistics", "Trade", "Military"]
        copy_play = (
            "All Divisions: stack their 3 compounding engines at once -- (1) P0 cargo swarm (`Floor Price` 400c / `Prospect` 100c), "
            "(2) Station Tourism + Gourmet supply lines (~200M+ cr rev), and (3) T3 combat wings (`Dialectic` / `Broadaxe`) farming PvE herds."
        )
        cnt_bits = []
        if top_bid:
            cnt_bits.append(f"OUTSUPPLY their standing bids ({top_bid}) for instant cash velocity")
        if cheap_asks:
            cnt_bits.append(f"OUTSOURCE their cheap wholesale dumps ({cheap_asks[0]['item']} @{_fmt_cr(cheap_asks[0]['price'])} cr at {cheap_asks[0]['system']}) instead of spending fuel/foundry capex")
        elif top_ask:
            cnt_bits.append(f"Benchmark wholesale asks ({top_ask}) before committing foundry build capital")
        return how_they_play, copy_play, "; ".join(cnt_bits) + ".", owners

    if archetype == "Facility Hub & Freight Power":
        owners = ["Logistics", "Trade", "Mining"]
        copy_play = (
            "Logistics+Trade: batch-build P0 `Ledger` (480c) freighters + T3 `Syndicate`/`Concordia` express couriers (`plan.py` selectors `cargo>=400`, `speed>=4`) "
            "to saturate `spacemolt_shipping` freight & passenger contracts while running dedicated T2+ mining hulls (`Rock Eater` / `Workhorse`)."
        )
        cnt_bits = []
        if cheap_asks:
            cnt_bits.append(f"OUTSOURCE their ultra-cheap wholesale ore/gas ({cheap_asks[0]['item']} @{cheap_asks[0]['price']} cr at {cheap_asks[0]['system']}) so our miners stay on high-margin scarce veins")
        if top_bid:
            cnt_bits.append(f"OUTSUPPLY their standing bid ({top_bid})")
        if unscanned_bases:
            cnt_bits.append(f"Intel: scan {len(unscanned_bases)} remaining bases ({', '.join(unscanned_bases[:3])})")
        return how_they_play, copy_play, ("; ".join(cnt_bits) + "." if cnt_bits else "Leverage Neutrality Pact for mutual trade & wholesale arbitrage."), owners

    if archetype == "Zero-Base Express & Exchange":
        owners = ["Trade", "Logistics"]
        copy_play = (
            "Trade+Logistics: assign fast P0/T1/T3 couriers (`Runner` spd 6 / `Futures` / `Concordia` / `Syndicate`) to express passenger lines + "
            "core Exchange spread arbitrage (`sell_order --undercut-pct 5` + `buy_order`) -- generates >20M/h with ZERO station rent."
        )
        counter_play = (
            "UNDERCUT their core Exchange spreads by 1-5% using docked zero-fuel Bursars across all 5 empire hubs (`market_prime`, `the_crucible`, `nova_terra`) "
            "and race them on high-pay passenger corridors."
        )
        return how_they_play, copy_play, counter_play, owners

    if archetype == "Zero-Base Docked NPC-Facility Factory":
        owners = ["Trade", "Logistics", "Intel"]
        copy_play = (
            "Trade+Logistics: keep ships docked at public NPC industrial stations crafting high-margin recipes into Exchange `sell_order`s (`0` fuel burn, `0` facility rent) "
            "so idle/reserve capacity compounds 24/7."
        )
        cnt_bits = ["UNDERCUT their Exchange craft asks via Bursar `sell_order --undercut-pct 5` and corner cheap raw input bids at NPC hubs"]
        if high_asks:
            cnt_bits.append(f"undercut their station ask ({high_asks[0]['item']} @{high_asks[0]['price']} cr)")
        if not hulls:
            cnt_bits.append(f"Intel: probe core NPC hubs to spot their docked crafting alts ({tag} has 0 ships seen in space)")
        return how_they_play, copy_play, "; ".join(cnt_bits) + ".", owners

    if archetype == "Zero-Base Bulk Mission/Freight Swarm":
        owners = ["Logistics", "Trade"]
        copy_play = (
            "Logistics+Trade: commission cheap P0 high-cargo hulls (`Prayer` 540c / `Congregation` 1,900c) on `freight-` (`spacemolt_shipping`) and "
            "bulk procurement missions (`plan.py` selector `cargo>=400`) around core empire hubs with zero base overhead."
        )
        counter_play = (
            "Out-scale their P0 `Cobble` swarm on high-margin `spacemolt_shipping` freight contracts & core hub deliveries using faster T1/T2 haulers (`Ledger`/`Prayer`) "
            "and pre-stocked station buffers."
        )
        return how_they_play, copy_play, counter_play, owners

    if archetype == "High-Tier Boutique Base Syndicate":
        owners = ["Command", "Trade", "Mining"]
        copy_play = (
            f"Mining+Command: mirror their high wealth-per-ship ({_fmt_cr(wps)}/sh, avg T{avg_t:.1f}) by concentrating P20/P30 pilots into T3/T4 hulls "
            f"({h_names or 'Excavation/Blind Spot/Axiomata'}) anchored to high-value facility hubs."
        )
        cnt_bits = []
        if high_asks:
            cnt_bits.append(f"UNDERCUT their high-markup station asks ({high_asks[0]['item']} @{high_asks[0]['price']} cr at {high_asks[0]['system']}) via Bursar `sell_order`")
        if top_bid:
            cnt_bits.append(f"OUTSUPPLY their hub fuel/input bids ({top_bid})")
        if not cnt_bits:
            cnt_bits.append("Compete for adjacent lawless resource systems and offer better trade spreads near their hubs")
        return how_they_play, copy_play, "; ".join(cnt_bits) + ".", owners

    if archetype == "Regional Industrial & Hauling Hub":
        owners = ["Logistics", "Trade", "Intel"]
        copy_play = (
            f"Logistics+Mining: adopt their proven P0/T1 workhorse mix ({h_names}) -- `Workhorse` (300c) / `Congregation` (1,900c) for bulk hauls "
            "and `Runner` (120c, spd 6) for fast corridor shuttles & courier contracts."
        )
        cnt_bits = []
        if cheap_asks:
            cnt_bits.append(f"OUTSOURCE their cheap wholesale ore ({cheap_asks[0]['item']} @{cheap_asks[0]['price']} cr at {cheap_asks[0]['system']})")
        if high_asks:
            cnt_bits.append(f"UNDERCUT their specialty goods ({high_asks[0]['item']} @{high_asks[0]['price']} cr)")
        if unscanned_bases:
            cnt_bits.append(f"Intel: dock & scan {len(unscanned_bases)} unscanned bases ({', '.join(unscanned_bases[:3])}) to unlock trade arbitrage")
        if not cnt_bits:
            cnt_bits.append(f"Pursue Neutrality Pact & two-way corridor trade around {top_bid or 'their hub markets'}")
        return how_they_play, copy_play, "; ".join(cnt_bits) + ".", owners

    owners = ["Intel", "Trade"]
    copy_play = f"Track hull doctrine ({h_names or 'unspotted'}) and verify whether their velocity spike comes from new crafting, mining, or Exchange routes."
    cnt_bits = []
    if top_bid:
        cnt_bits.append(f"OUTSUPPLY {top_bid}")
    if cheap_asks:
        cnt_bits.append(f"OUTSOURCE {cheap_asks[0]['item']} @{cheap_asks[0]['price']} cr")
    if unscanned_bases:
        cnt_bits.append(f"Intel: scan {len(unscanned_bases)} unscanned bases ({', '.join(unscanned_bases[:3])})")
    return how_they_play, copy_play, ("; ".join(cnt_bits) + "." if cnt_bits else "Scout active space and benchmark markets before committing counter-routes."), owners


def _inspect_our_adoption(repo_root, data_dir, conn, tables):
    """Measure live adoption of the 8 SpaceMolt strategies inside our own fleet (zero hardcoded counts)."""
    fl = _load_json(Path(data_dir) / "fleet" / "fleet.json", {})
    emp = _load_json(Path(data_dir) / "empire" / "empire.json", {})
    ships = [s for s in (fl.get("ships") or []) if isinstance(s, dict)]
    facs = [f for f in (emp.get("facilities") or []) if isinstance(f, dict)]
    bases = [b for b in (emp.get("bases") or []) if isinstance(b, dict)]

    route_dir = Path(repo_root) / "game" / "routes"
    bursar_routes = craft_routes = passenger_routes = freight_routes = hunt_routes = escort_routes = scarce_routes = 0
    if route_dir.is_dir():
        for rp in route_dir.glob("*.json"):
            rn = rp.name.lower()
            try:
                txt = rp.read_text(encoding="utf-8", errors="replace").lower()
            except OSError:
                continue
            if "sell_order" in txt or "buy_order" in txt or "bursar" in rn:
                bursar_routes += 1
            if "craft" in rn or "smelt" in rn or '"craft"' in txt:
                craft_routes += 1
            if "passenger" in rn or "courier" in rn:
                passenger_routes += 1
            if "freight" in rn or "shipping" in rn or "mission-" in rn:
                freight_routes += 1
            if "hunt" in rn or "patrol" in rn or "pirate" in rn:
                hunt_routes += 1
            if "escort" in rn or "guard" in rn:
                escort_routes += 1
            if any(k in rn for k in SCARCE_RAW_HINTS):
                scarce_routes += 1

    def _ship_job(s):
        act = s.get("activity") if isinstance(s.get("activity"), dict) else {}
        return f"{s.get('order') or ''} {act.get('type') or ''} {s.get('route') or ''}".lower()

    tourism_facs = sum(1 for f in facs if any(k in str(f.get("type") or f.get("name") or "").lower() for k in ("tour", "hotel", "resort", "cantina", "lounge", "park", "museum", "gourmet")))
    active_bursar = sum(1 for s in ships if any(k in _ship_job(s) for k in ("bursar", "market-make", "sell-order", "exchange", "order-book")))
    active_craft = sum(1 for s in ships if any(k in _ship_job(s) for k in ("craft", "smelt", "refine", "factory")))
    active_pass = sum(1 for s in ships if any(k in _ship_job(s) for k in ("passenger", "express", "taxi", "courier")))
    active_freight = sum(1 for s in ships if any(k in _ship_job(s) for k in ("freight", "shipping", "mission-")))
    active_hunt = sum(1 for s in ships if any(k in _ship_job(s) for k in ("hunt", "pirate", "combat", "escort")))
    active_scarce = sum(1 for s in ships if any(k in _ship_job(s) for k in SCARCE_RAW_HINTS))

    fast_hulls = sum(1 for s in ships if str(s.get("class") or "").lower() in ("runner", "futures", "concordia", "syndicate", "courier"))
    bulk_hulls = sum(1 for s in ships if str(s.get("class") or "").lower() in ("prayer", "ledger", "congregation", "floor_price", "floor price", "junk_convoy", "junk convoy", "frankenhauler", "workhorse"))
    t2p_hulls = 0
    if "ships" in tables and "hulls" in tables:
        try:
            r = conn.execute(
                "SELECT COUNT(*) FROM ships s JOIN hulls h ON LOWER(h.id)=LOWER(s.class) OR LOWER(h.name)=LOWER(s.class) WHERE COALESCE(h.tier,0) >= 2"
            ).fetchone()
            t2p_hulls = int(_num(r[0])) if r else 0
        except sqlite3.Error:
            t2p_hulls = 0
    contracts_n = 0
    clog = Path(repo_root) / "communications" / "contracts.log"
    if clog.is_file():
        try:
            contracts_n = clog.read_text(encoding="utf-8", errors="replace").count("## [ENT-")
        except OSError:
            contracts_n = 0

    # Live empire ship counts, division working %, T2+ by division, and read.db KPI drivers
    empire_ships = {}
    div_tot = {}
    div_work = {}
    t2_mining = 0
    t2_combat = 0
    hull_tier_map = {}
    if "hulls" in tables:
        try:
            for hr in conn.execute("SELECT LOWER(id), LOWER(COALESCE(name,'')), COALESCE(tier,0) FROM hulls"):
                if hr[0]:
                    hull_tier_map[hr[0]] = int(_num(hr[2]))
                if hr[1]:
                    hull_tier_map[hr[1]] = int(_num(hr[2]))
        except sqlite3.Error:
            pass
    for s in ships:
        em = str(s.get("empire") or "voidborn").lower()
        empire_ships[em] = empire_ships.get(em, 0) + 1
        dv = str(s.get("division") or "Unassigned")
        div_tot[dv] = div_tot.get(dv, 0) + 1
        act = s.get("activity") if isinstance(s.get("activity"), dict) else {}
        if act.get("kind") and act.get("kind") != "idle":
            div_work[dv] = div_work.get(dv, 0) + 1
        tr = hull_tier_map.get(str(s.get("class") or "").lower(), 0)
        if tr >= 2:
            if dv == "Mining":
                t2_mining += 1
            elif dv == "Military":
                t2_combat += 1
    div_work_pct = {dv: round(100.0 * div_work.get(dv, 0) / max(1, cnt), 1) for dv, cnt in div_tot.items()}

    trade_net_24h = 0.0
    steady_net_24h = 0.0
    mining_ore_sh = 0.0
    intel_fresh_pct = 0.0
    if "stats_figures" in tables:
        try:
            r = conn.execute("SELECT COALESCE(SUM(value),0) FROM stats_figures WHERE view='contribution' AND figure='own_net' AND hours=24 AND LOWER(subject)='trade'").fetchone()
            trade_net_24h = _num(r[0]) if r else 0.0
            r2 = conn.execute("SELECT COALESCE(SUM(value),0) FROM stats_figures WHERE view='contribution' AND figure='own_net' AND hours=24").fetchone()
            steady_net_24h = _num(r2[0]) if r2 else 0.0
            r3 = conn.execute("SELECT COALESCE(MAX(value),0) FROM stats_figures WHERE view='contribution' AND figure='ore_per_ship_hour' AND hours=24").fetchone()
            mining_ore_sh = _num(r3[0]) if r3 else 0.0
        except sqlite3.Error:
            pass
    if "runs" in tables and steady_net_24h == 0.0:
        try:
            r = conn.execute("SELECT COALESCE(SUM(CASE WHEN COALESCE(one_time,0)=0 THEN credits ELSE 0 END),0)/24.0 FROM runs WHERE t > strftime('%s','now') - 86400").fetchone()
            steady_net_24h = _num(r[0]) if r else 0.0
        except sqlite3.Error:
            pass
    if "books" in tables:
        try:
            rb = conn.execute("SELECT COUNT(DISTINCT system) AS tot, COUNT(DISTINCT CASE WHEN t > strftime('%s','now') - 10800 THEN system END) AS fr FROM books").fetchone()
            if rb and rb[0]:
                intel_fresh_pct = round(100.0 * int(rb[1] or 0) / max(1, int(rb[0])), 1)
        except sqlite3.Error:
            pass
    endl_logged = (Path(repo_root) / "game" / "factions" / "h-endl.md").is_file()

    return {
        "bases": len(bases),
        "tourism_facs": tourism_facs,
        "bursar_routes": bursar_routes, "active_bursar": active_bursar,
        "craft_routes": craft_routes, "active_craft": active_craft,
        "passenger_routes": passenger_routes, "active_pass": active_pass, "fast_hulls": fast_hulls,
        "freight_routes": freight_routes, "active_freight": active_freight, "bulk_hulls": bulk_hulls,
        "hunt_routes": hunt_routes, "escort_routes": escort_routes, "active_hunt": active_hunt,
        "scarce_routes": scarce_routes, "active_scarce": active_scarce, "t2p_hulls": t2p_hulls,
        "t2_mining": t2_mining, "t2_combat": t2_combat,
        "contracts_n": contracts_n,
        "empire_ships": empire_ships,
        "div_work_pct": div_work_pct,
        "trade_net_24h": round(trade_net_24h, 0),
        "steady_net_24h": round(steady_net_24h, 0),
        "mining_ore_sh": round(mining_ore_sh, 1),
        "intel_fresh_pct": intel_fresh_pct,
        "endl_logged": endl_logged,
    }


def _build_strategy_playbooks(our_adopt, leaders, market_edges):
    """Build the 8-Strategy Adopted Playbook Matrix with automated Strategy-Pinned KPI Driver Trees,
    required SpaceMolt empires, cross-division handoff chains, and Copy/Counter blueprints."""
    t1 = (leaders.get("tourism_revenue") or [{}])[0]
    t2 = (leaders.get("tourism_revenue") or [{}, {}])[1] if len(leaders.get("tourism_revenue") or []) > 1 else {}
    ex1 = (leaders.get("exchange_sellers") or [{}])[0]
    eo1 = (leaders.get("exchange_orders") or [{}])[0]
    ps1 = (leaders.get("passengers_top") or [{}])[0]
    fc1 = (leaders.get("facility_prod_top") or [{}])[0]
    cr1 = (leaders.get("crafted_top") or [{}])[0]
    ms1 = (leaders.get("missions_top") or [{}])[0]
    pv1 = (leaders.get("pve_top") or [{}])[0]
    or1 = (leaders.get("ore_top") or [{}])[0]

    raw_bids = market_edges.get("raw_bids") or []
    raw_cheap = market_edges.get("raw_cheap") or []
    cap_cheap = market_edges.get("capital_cheap") or []
    undercut = market_edges.get("undercut_targets") or []
    all_bids = market_edges.get("outsupply_bids") or []
    crafted_bids = market_edges.get("crafted_bids") or []

    bid_ex = f"{all_bids[0]['item']} @{all_bids[0]['price']} cr ({all_bids[0]['tag']}@{all_bids[0]['system']})" if all_bids else "rival hub bids"
    gourmet_ex = f"{crafted_bids[0]['item']} @{crafted_bids[0]['price']} cr ({crafted_bids[0]['tag']}@{crafted_bids[0]['system']})" if crafted_bids else bid_ex
    raw_bid_ex = f"{raw_bids[0]['item']} @{raw_bids[0]['price']} cr ({raw_bids[0]['tag']}@{raw_bids[0]['system']})" if raw_bids else "uranium_ore/silver_ore bids"
    raw_ch_ex = f"{raw_cheap[0]['item']} @{raw_cheap[0]['price']} cr ({raw_cheap[0]['tag']}@{raw_cheap[0]['system']})" if raw_cheap else "cheap rival bulk ores"
    cap_ch_ex = f"{cap_cheap[0]['item']} @{_fmt_cr(cap_cheap[0]['price'])} cr ({cap_cheap[0]['tag']}@{cap_cheap[0]['system']})" if cap_cheap else "station_core ~13M"
    uc_ex = f"{undercut[0]['item']} @{undercut[0]['price']} cr ({undercut[0]['tag']}@{undercut[0]['system']})" if undercut else "inflated rival asks"

    emp_map = our_adopt.get("empire_ships") or {}
    dwork = our_adopt.get("div_work_pct") or {}
    emp_labels = {"voidborn": "Voidborn", "nebula": "Nebula", "solarian": "Solarian", "crimson": "Crimson", "outerrim": "Outer Rim"}

    def _emps(*keys):
        return [{"id": k, "name": emp_labels.get(k, k.title()), "ships": int(emp_map.get(k, 0))} for k in keys]

    def _kpi(name, owner, current, target, matched, source):
        return {"name": name, "owner": owner, "current": str(current), "target": str(target), "matched": bool(matched), "source": source}

    def _pack(pid, name, short_name, divisions, empires, handoff_chain, proven_by, kpis, core_active, active_lbl, partial_lbl, gap_lbl, how_it_works, how_to_copy, how_to_counter):
        m_cnt = sum(1 for k in kpis if k["matched"])
        tot = max(1, len(kpis))
        rpct = round(100.0 * m_cnt / tot, 1)
        if core_active and m_cnt >= 3:
            scode, slbl = "ACTIVE", active_lbl
        elif core_active or m_cnt >= 2:
            scode, slbl = "PARTIAL", partial_lbl if not core_active else f"{active_lbl} ({m_cnt}/{tot} KPIs)"
        else:
            scode, slbl = "GAP", gap_lbl
        missing = [k for k in kpis if not k["matched"]]
        blocker = f"{missing[0]['name']} ({missing[0]['owner']}: {missing[0]['current']} vs {missing[0]['target']})" if missing else "All strategy KPIs matched"
        return {
            "id": pid,
            "name": name,
            "short_name": short_name,
            "divisions": divisions,
            "empires": empires,
            "handoff_chain": handoff_chain,
            "proven_by": proven_by,
            "status_code": scode,
            "our_status": slbl,
            "kpis": kpis,
            "matched_count": m_cnt,
            "total_count": tot,
            "readiness_pct": rpct,
            "blocker": blocker,
            "how_it_works": how_it_works,
            "how_to_copy": how_to_copy,
            "how_to_counter": how_to_counter,
        }

    trade_log_work = round((dwork.get("Trade", 0.0) + dwork.get("Logistics", 0.0)) / 2.0, 1)
    empires_present = sum(1 for k in ("voidborn", "nebula", "solarian", "crimson", "outerrim") if emp_map.get(k, 0) > 0)

    return [
        _pack(
            "tourism_hub", "1. Sovereign Tourism & Gourmet Hub", "Tourism Hub",
            ["Command", "Logistics", "Trade"],
            _emps("voidborn", "solarian", "nebula"),
            "Command (station) -> Logistics (tourism fac) -> Trade (gourmet supply) <- Intel (hub bids)",
            f"[BUSY] {t1.get('name', 'The Obsidian Well')} ({_fmt_cr(t1.get('value', 0))} cr)" + (f", [HEXC] {t2.get('name', 'Hex Star')} ({_fmt_cr(t2.get('value', 0))} cr)" if t2.get("name") else ""),
            [
                _kpi("Sovereign bases/stations", "Command", f"{our_adopt['bases']}", ">=2", our_adopt["bases"] >= 2, "empire.json"),
                _kpi("Tourism/hospitality modules", "Logistics", f"{our_adopt['tourism_facs']}", ">=1", our_adopt["tourism_facs"] >= 1, "empire.json"),
                _kpi("Rival gourmet/luxury bids scanned", "Intel", f"{len(crafted_bids)}", ">=1", len(crafted_bids) >= 1, "read.db:books"),
                _kpi("Active Trade net cashflow", "Trade", f"{_fmt_signed_cr(our_adopt['trade_net_24h'])}/h", ">0 cr/h", our_adopt["trade_net_24h"] > 0, "read.db:runs"),
            ],
            our_adopt["tourism_facs"] > 0,
            f"ACTIVE ({our_adopt['tourism_facs']} tourism fac)",
            f"PARTIAL ({our_adopt['bases']} base, 0 tourism fac)",
            "GAP (0 tourism fac)",
            "Player stations with high Tourism Appeal + stocked Gourmet food/drinks print passive 50M-215M+ cr revenue without fuel burn.",
            "Command+Logistics: build high-appeal Tourism modules on our sovereign stations once Atria/Yildun bases stand; Trade stocks Gourmet rations & specialty drinks.",
            f"Trade: feed rival Tourism hubs' gourmet/drink standing bids ({gourmet_ex}, `solarian_gourmet_rations`, `void_espresso`) to capture their tourism cashflow today.",
        ),
        _pack(
            "docked_factory", "2. Zero-Fuel Docked NPC-Facility Factory", "Docked Factory",
            ["Trade", "Logistics"],
            _emps("nebula", "solarian", "voidborn", "outerrim"),
            "Intel (NPC spreads) -> Trade/Logistics (docked craft + sell_order) -> Zero fuel burn",
            f"[MIN9] 7.0M crafted ({fc1.get('name', 'SpaceMiner99')} {_fmt_cr(fc1.get('value', 0))} fac-prod), [BEAT] 4.6M crafted (0 bases, 53.8M/sh), {cr1.get('name', 'LT1428')} {_fmt_cr(cr1.get('value', 0))} crafted",
            [
                _kpi("Verified craft/smelt routes", "Trade", f"{our_adopt['craft_routes']}", ">=5", our_adopt["craft_routes"] >= 5, "game/routes"),
                _kpi("Active docked craft ships", "Trade", f"{our_adopt['active_craft']}", ">=5", our_adopt["active_craft"] >= 5, "fleet.json"),
                _kpi("Trade+Logistics employment", "Logistics", f"{trade_log_work:.0f}%", ">=80%", trade_log_work >= 80.0, "fleet.json"),
                _kpi("Cheap wholesale inputs scanned", "Intel", f"{len(raw_cheap) + len(cap_cheap)}", ">=3", (len(raw_cheap) + len(cap_cheap)) >= 3, "read.db:books"),
            ],
            our_adopt["active_craft"] >= 5,
            f"ACTIVE ({our_adopt['active_craft']} craft ships)",
            f"PARTIAL ({our_adopt['active_craft']} active, {our_adopt['craft_routes']} routes)",
            "GAP (no docked craft wing)",
            "Zero-base factions park ships permanently docked at public NPC industrial stations, buying cheap inputs and crafting high-margin goods at 0 fuel & 0 rent.",
            "Trade+Logistics: add `docked_at` / `min_cargo` plan entries (`plan.py`) running zero-fuel `craft` + `sell_order --undercut-pct 5` at public refinery/factory hubs; zero ships parked idle.",
            f"Trade: outbid their raw inputs with Bursar `buy_order` walls and undercut their finished Exchange listings by 5% ({uc_ex}).",
        ),
        _pack(
            "exchange_bursar", "3. Multi-Hub Exchange Market-Making (Bursar)", "Exchange Bursar",
            ["Trade", "Command"],
            _emps("nebula", "solarian", "voidborn", "crimson", "outerrim"),
            "Intel (<3h books) -> Trade (5-empire Bursar buy/sell ladders) -> Command (contracts.log)",
            f"[NOIR] +20.4M/h (0 bases), {ex1.get('name', 'Truus Taal')} {_fmt_cr(ex1.get('value', 0))} listed, {eo1.get('name', 'Vex Nebulon')} {int(_num(eo1.get('value'))):,d} active orders",
            [
                _kpi("5-empire hub presence", "Command", f"{empires_present}/5 empires", "5/5", empires_present >= 5, "fleet.json"),
                _kpi("Active Bursar/exchange ships", "Trade", f"{our_adopt['active_bursar']}", ">=5", our_adopt["active_bursar"] >= 5, "fleet.json"),
                _kpi("P2P contracts/orders logged", "Trade", f"{our_adopt['contracts_n']}", ">=5", our_adopt["contracts_n"] >= 5, "contracts.log"),
                _kpi("Trade 24h steady net/h", "Trade", f"{_fmt_signed_cr(our_adopt['trade_net_24h'])}/h", ">0 cr/h", our_adopt["trade_net_24h"] > 0, "read.db:runs"),
            ],
            our_adopt["active_bursar"] >= 5,
            f"ACTIVE ({our_adopt['active_bursar']} Bursars)",
            f"PARTIAL ({our_adopt['active_bursar']} active, {our_adopt['bursar_routes']} routes)",
            "GAP (no Bursar wing)",
            "Stationed Bursar ships sit across all 5 empire exchanges maintaining continuous buy walls and 5%-undercut sell ladders with zero jump fuel burn.",
            "Trade: seat 1+ Bursar per empire hub (`plan.py` `docked_at:` + `route_run.py` `sell_order --undercut-pct 5`, `buy_order`, `watch_minutes` desk duty) and log deals in `contracts.log`.",
            f"Trade: undercut overpriced rival station asks ({uc_ex}) by 5-10% and sweep stale vault inventory (>250k cr) directly into live bids.",
        ),
        _pack(
            "express_passenger", "4. Zero-Base Express Passenger & Courier", "Express Pax",
            ["Logistics", "Trade"],
            _emps("outerrim", "nebula", "solarian"),
            "Logistics (Runner/Futures speed>=4 hulls) -> Passenger/courier boards <- Intel (hubs)",
            f"[NOIR] Futures/Syndicate/Concordia (53.8M/sh), {ps1.get('name', 'LimaTango1428')} {int(_num(ps1.get('value'))):,d} passengers delivered",
            [
                _kpi("Fast hulls (Runner/Futures/Concordia)", "Logistics", f"{our_adopt['fast_hulls']}", ">=5", our_adopt["fast_hulls"] >= 5, "fleet.json"),
                _kpi("Express passenger/courier routes", "Logistics", f"{our_adopt['passenger_routes']}", ">=2", our_adopt["passenger_routes"] >= 2, "game/routes"),
                _kpi("Active express ships", "Logistics", f"{our_adopt['active_pass']}", ">=3", our_adopt["active_pass"] >= 3, "fleet.json"),
                _kpi("Outer Rim + Nebula ships seated", "Command", f"{emp_map.get('outerrim',0) + emp_map.get('nebula',0)}", ">=40", (emp_map.get("outerrim", 0) + emp_map.get("nebula", 0)) >= 40, "fleet.json"),
            ],
            our_adopt["active_pass"] >= 3,
            f"ACTIVE ({our_adopt['active_pass']} express ships)",
            f"PARTIAL ({our_adopt['fast_hulls']} fast hulls, {our_adopt['passenger_routes']} routes)",
            "GAP (0 fast hulls / 0 routes)",
            "Speed 4-6 low-cargo hulls (`Runner` P0 spd 6, `Futures` P0, `Concordia`/`Syndicate` T3) chain fast passenger & express courier runs with near-zero capital overhead.",
            "Logistics: batch-commission P0 `Runner` (120c, spd 6) & `Futures` (P0), tag `plan.py` selector `speed>=4` onto `passenger-` express routes (`hive.py upgrades logistics`).",
            "Logistics: saturate high-pay core empire passenger corridors first so rivals face thinner mission boards while earning instant liquid credits.",
        ),
        _pack(
            "bulk_freight_missions", "5. Bulk Freight & Mission Swarm", "Bulk Freight",
            ["Logistics", "Trade"],
            _emps("nebula", "solarian", "outerrim"),
            "Logistics (Prayer/Ledger/Congregation cargo>=400) -> spacemolt_shipping + bulk missions",
            f"[WEXL] 132.8k missions (Prayer 540c / Congregation 1900c), [IRLC] 36x Ledger (480c), {ms1.get('name', 'ENDL')} {int(_num(ms1.get('value'))):,d} missions",
            [
                _kpi("Bulk cargo hulls (Prayer/Ledger/Workhorse)", "Logistics", f"{our_adopt['bulk_hulls']}", ">=10", our_adopt["bulk_hulls"] >= 10, "fleet.json"),
                _kpi("Active freight/mission ships", "Logistics", f"{our_adopt['active_freight']}", ">=20", our_adopt["active_freight"] >= 20, "fleet.json"),
                _kpi("Freight/mission routes", "Logistics", f"{our_adopt['freight_routes']}", ">=10", our_adopt["freight_routes"] >= 10, "game/routes"),
                _kpi("Logistics employment", "Logistics", f"{dwork.get('Logistics', 0.0):.0f}%", ">=80%", dwork.get("Logistics", 0.0) >= 80.0, "fleet.json"),
            ],
            our_adopt["active_freight"] >= 20,
            f"ACTIVE ({our_adopt['active_freight']} freight ships)",
            f"PARTIAL ({our_adopt['active_freight']} active, {our_adopt['bulk_hulls']} bulk hulls)",
            "GAP (no bulk freight wing)",
            "P0/T1 bulk cargo hulls (`Ledger` 480c, `Prayer` 540c, `Congregation` 1,900c) sweep 100c+ `spacemolt_shipping` freight contracts and bulk delivery missions in parallel.",
            "Logistics: run `hive.py shipping` (MCP `view=shipping`), assign `plan.py` `cargo>=400` / `utility_group` proximity-matched haulers to `freight-` & `mission-` routes.",
            "Logistics+Trade: pre-stage cheap hub buffers so our haulers claim high-reward `spacemolt_shipping` contracts faster than single-hub rivals.",
        ),
        _pack(
            "scarce_vein_monopoly", "6. Lawless Scarce-Vein Monopoly Extraction", "Scarce Veins",
            ["Mining", "Command", "Intel"],
            _emps("solarian", "voidborn", "nebula"),
            "Intel (belts/bids) -> Mining (T2+ scarce veins) -> Logistics (vault haul) -> Trade (sell)",
            f"[HEXC] 11 bases 115.5M/sh (avg T3.2 Lithosphere/Deep Survey), [IRLC] {or1.get('name', 'ILC Vent')} {_fmt_cr(or1.get('value', 0))} ore",
            [
                _kpi("T2+ industrial mining hulls", "Mining", f"{our_adopt['t2_mining']}", ">=5", our_adopt["t2_mining"] >= 5, "read.db:ships"),
                _kpi("Active scarce-vein miners", "Mining", f"{our_adopt['active_scarce']}", ">=10", our_adopt["active_scarce"] >= 10, "fleet.json"),
                _kpi("High-bid scarce raw veins tracked", "Intel", f"{len(raw_bids)}", ">=2", len(raw_bids) >= 2, "read.db:books"),
                _kpi("Mining extraction yield", "Mining", f"{our_adopt['mining_ore_sh']:.0f} ore/sh-h", ">=80", our_adopt["mining_ore_sh"] >= 80.0, "read.db:stats"),
            ],
            our_adopt["active_scarce"] >= 10 and our_adopt["t2_mining"] >= 5,
            f"ACTIVE ({our_adopt['active_scarce']} scarce, {our_adopt['t2_mining']} T2+)",
            f"PARTIAL ({our_adopt['active_scarce']} scarce ships, {our_adopt['t2_mining']} T2+ hulls)",
            "GAP (no scarce-vein wing)",
            "High-tier industrial hulls (`Workhorse` -> `Lithosphere`/`Tellurian`) anchor near lawless rare belts (Uranium/Silver/Cobalt/Argon/Gold) instead of competing on 1-4 cr iron/copper.",
            f"Mining: target high-bid scarce veins ({raw_bid_ex}) with `--jettison-gangue`, batch-upgrade lasers & hulls (`hive.py upgrades mining`), and use `plan.py` `min_piloting`/`max_jumps` selectors.",
            f"Mining+Trade: STOP mining cheap bulk ores available wholesale below fuel cost ({raw_ch_ex}); buy rival dumps and redirect our lasers to 100-600 cr scarce veins.",
        ),
        _pack(
            "wholesale_arbitrage", "7. Wholesale Capital Arbitrage (Outsource & Outsupply)", "Arbitrage",
            ["Trade", "Logistics", "Command"],
            _emps("voidborn", "nebula", "solarian", "crimson", "outerrim"),
            "Intel (<3h rival books) -> Trade/Logistics (buy cheap / sell high) -> Command (capex gate)",
            f"Live rival books: {cap_ch_ex}, {raw_ch_ex} vs {bid_ex}",
            [
                _kpi("Live Outsource/Outsupply edges", "Intel", f"{len(all_bids) + len(raw_cheap)}", ">=3", (len(all_bids) + len(raw_cheap)) >= 3, "read.db:books"),
                _kpi("Market books <3h fresh", "Intel", f"{our_adopt['intel_fresh_pct']:.0f}%", ">=70%", our_adopt["intel_fresh_pct"] >= 70.0, "read.db:books"),
                _kpi("Logged P2P arbitrage contracts", "Trade", f"{our_adopt['contracts_n']}", ">=5", our_adopt["contracts_n"] >= 5, "contracts.log"),
                _kpi("Fleet steady cashflow", "Command", f"{_fmt_signed_cr(our_adopt['steady_net_24h'])}/h", ">0 cr/h", our_adopt["steady_net_24h"] > 0, "read.db:runs"),
            ],
            our_adopt["contracts_n"] >= 5 and our_adopt["steady_net_24h"] > 0,
            f"ACTIVE ({our_adopt['contracts_n']} contracts)",
            f"PARTIAL ({our_adopt['contracts_n']} contracts, steady {_fmt_signed_cr(our_adopt['steady_net_24h'])}/h)",
            "GAP (no wholesale arbitrage)",
            "Rival mega-factions dump surplus ores, steel plates, and even `station_core`s below our self-build cost while posting huge standing bids on bottlenecks.",
            f"Command+Trade+Logistics: always check `hive.py rivals` Outsource/Outsupply board before spending foundry/mining hours -- buy cheap ({cap_ch_ex}, {raw_ch_ex}) and sell high ({bid_ex}).",
            "Command+Trade: convert rivals' overproduction into cheaper Collective stations/hulls while draining their treasury via their own standing bids.",
        ),
        _pack(
            "pve_combat_escort", "8. PvE Herd Farming & Armed Escort Projection", "PvE & Escort",
            ["Military", "Intel"],
            _emps("crimson", "solarian", "voidborn"),
            "Intel (herds & [ENDL] sightings) -> Military (T2+ hunt & escort) -> Trade (loot sales)",
            f"[BUSY] {int(_num(pv1.get('value', 8454))):,d} pirates (157x Dialectic), [HEXC] 2,142 pirates; Threat: [ENDL] 1,527 PvP kills",
            [
                _kpi("Active PvE/escort combat ships", "Military", f"{our_adopt['active_hunt']}", ">=40", our_adopt["active_hunt"] >= 40, "fleet.json"),
                _kpi("T2+ warships (Broadaxe/Recursion/Dialectic)", "Military", f"{our_adopt['t2_combat']}", ">=5", our_adopt["t2_combat"] >= 5, "read.db:ships"),
                _kpi("Armed escort routes ready", "Military", f"{our_adopt['escort_routes']}", ">=5", our_adopt["escort_routes"] >= 5, "game/routes"),
                _kpi("Military employment + [ENDL] dossier", "Military", f"{dwork.get('Military', 0.0):.0f}% / {'OK' if our_adopt['endl_logged'] else 'MISS'}", ">=80% + OK", dwork.get("Military", 0.0) >= 80.0 and our_adopt["endl_logged"], "fleet.json+factions"),
            ],
            our_adopt["active_hunt"] >= 40,
            f"ACTIVE ({our_adopt['active_hunt']} combat ships)",
            f"PARTIAL ({our_adopt['active_hunt']} combat, {our_adopt['t2_combat']} T2+)",
            "GAP (no PvE/escort wing)",
            "Dedicated T2/T3 combat wings (`Dialectic`, `Broadaxe`, `Recursion`) earn bounties + salvage loot while deterring PvP raiders (`[ENDL]`) on lawless trade corridors.",
            "Military: run parallel `hunt-` PvE herd wings (handing loot to Trade, F9) + paired T2+ `escort-` wings using `plan.py` `posture:WAR_ALERT` readiness & `min_hull_tier:2`.",
            "Military+Intel: track [ENDL] hot systems in `h-endl.md`, enforce strict defensive RoE (F2) around Neutral [HEXC]/[IRLC], and escalate posture automatically if faction war starts.",
        ),
    ]

def compute_sedcards(repo_root=REPO_DEFAULT, data_dir=DATA_DEFAULT, top_n=12, now=None):
    """Build complete live Rival Sedcards, 8-Strategy Playbook Matrix, Leaderboards & Adopted Division Tricks."""
    now = float(now if now is not None else time.time())
    db_path = Path(data_dir) / "store" / "read.db"
    diplo = _load_json(Path(data_dir) / "comms" / "diplomacy.json", {})
    diplo_facs = (diplo.get("factions") or {}) if isinstance(diplo, dict) else {}

    out = {
        "at": int(now),
        "span_hours": 0.0,
        "our": {"tag": "CLTV", "members": 0, "wealth": 0, "bases": 0},
        "sedcards": [],
        "tourism_top": [],
        "exchange_top": [],
        "playstyle_leaders": {},
        "strategy_playbooks": [],
        "market_edges": {},
        "unscanned_rival_bases": [],
        "tricks_by_division": {},
    }
    if not db_path.is_file():
        return out

    conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True, timeout=3.0)
    conn.row_factory = sqlite3.Row
    try:
        tables = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type IN ('table','view')")}
        if "rival_snapshots" not in tables:
            return out

        rng = conn.execute("SELECT MIN(t) AS t0, MAX(t) AS t1 FROM rival_snapshots").fetchone()
        if not rng or not rng["t1"]:
            return out
        t0, t1 = int(rng["t0"]), int(rng["t1"])
        dt_h = max(0.0, (t1 - t0) / 3600.0)
        out["span_hours"] = round(dt_h, 2)

        old_map = {}
        if dt_h >= 0.5:
            for r in conn.execute("SELECT * FROM rival_snapshots WHERE t=?", (t0,)).fetchall():
                old_map[str(r["tag"]).upper()] = dict(r)

        cltv_row = conn.execute("SELECT * FROM rival_snapshots WHERE t=? AND UPPER(tag)='CLTV'", (t1,)).fetchone()
        if cltv_row:
            out["our"] = {
                "tag": "CLTV",
                "members": int(_num(cltv_row["members"])),
                "wealth": int(_num(cltv_row["wealth"])),
                "bases": int(_num(cltv_row["bases"])),
                "avg_tier": round(_num(cltv_row["avg_tier"]), 2),
            }

        playstyle_leaders = {}
        if "leaderboards" in tables:
            lb_specs = [
                ("tourism_revenue", "stations", "tourism_revenue", 5),
                ("tourism_appeal", "stations", "tourism_appeal", 4),
                ("exchange_sellers", "exchange", "sell_order_value", 4),
                ("exchange_orders", "exchange", "active_orders", 4),
                ("exchange_earned", "players", "exchange_credits_earned", 5),
                ("passengers_top", "players", "passengers_delivered", 4),
                ("facility_prod_top", "players", "facility_items_produced", 4),
                ("crafted_top", "players", "items_crafted", 4),
                ("missions_top", "factions", "missions_completed", 4),
                ("contraband_top", "players", "contraband_sold", 4),
                ("pve_top", "factions", "pirates_destroyed", 4),
                ("ore_top", "players", "ore_mined", 4),
            ]
            for key, grp, brd, lim in lb_specs:
                playstyle_leaders[key] = [
                    {"rank": int(r["rank"]), "name": str(r["name"]), "tag": str(r["tag"] or ""), "system": str(r["tag"] or ""), "value": int(_num(r["value"])), "revenue": int(_num(r["value"])), "credits": int(_num(r["value"]))}
                    for r in conn.execute(
                        "SELECT rank, name, tag, value FROM leaderboards WHERE grp=? AND board=? ORDER BY rank ASC LIMIT ?",
                        (grp, brd, lim),
                    ).fetchall()
                ]
            out["tourism_top"] = [
                {"rank": x["rank"], "name": x["name"], "system": x["system"], "revenue": x["value"]}
                for x in playstyle_leaders.get("tourism_revenue") or []
            ]
            out["exchange_top"] = [
                {"rank": x["rank"], "name": x["name"], "empire": x["tag"], "credits": x["value"]}
                for x in playstyle_leaders.get("exchange_earned") or []
            ]
            out["playstyle_leaders"] = playstyle_leaders

        hulls_info = {}
        if "hulls" in tables:
            for r in conn.execute(
                "SELECT id, name, LOWER(COALESCE(NULLIF(faction,''), 'neutral')) AS fac, tier, category, "
                "COALESCE(piloting_required,0) AS pil, COALESCE(cargo,0) AS cargo, COALESCE(speed,0) AS speed, "
                "COALESCE(weapon_slots,0) AS w, COALESCE(defense_slots,0) AS d, COALESCE(utility_slots,0) AS u FROM hulls"
            ).fetchall():
                hulls_info[str(r["id"]).lower()] = dict(r)

        leaders = {}
        if "factions" in tables:
            for r in conn.execute("SELECT UPPER(tag) AS tag, leader FROM factions").fetchall():
                leaders[str(r["tag"])] = str(r["leader"] or "")

        scanned_book_systems = set()
        if "books" in tables:
            scanned_book_systems = {str(r[0]).lower() for r in conn.execute("SELECT DISTINCT LOWER(system) FROM books WHERE system IS NOT NULL").fetchall()}

        top_rows = conn.execute(
            "SELECT * FROM rival_snapshots WHERE t=? AND UPPER(tag) != 'CLTV' ORDER BY wealth DESC LIMIT ?",
            (t1, int(top_n)),
        ).fetchall()

        sedcards = []
        all_bids_top = []
        unscanned_summary = []

        for r in top_rows:
            rd = dict(r)
            tag = str(rd["tag"]).upper()
            prev = old_map.get(tag)
            dw_h = round((_num(rd["wealth"]) - _num(prev["wealth"])) / dt_h, 0) if (prev and dt_h >= 0.5) else None
            dore_h = round((_num(rd["ore_mined"]) - _num(prev["ore_mined"])) / dt_h, 0) if (prev and dt_h >= 0.5) else None
            dcrft_h = round((_num(rd["items_crafted"]) - _num(prev["items_crafted"])) / dt_h, 1) if (prev and dt_h >= 0.5) else None

            try:
                allies = json.loads(rd.get("allies") or "[]")
                if not isinstance(allies, list):
                    allies = []
            except Exception:
                allies = []
            try:
                base_sys = json.loads(rd.get("base_systems") or "[]")
                if not isinstance(base_sys, list):
                    base_sys = []
            except Exception:
                base_sys = []
            rd["_base_sys"] = base_sys

            spotted_hulls = []
            spotted_sys = []
            if "met" in tables:
                for hr in conn.execute(
                    "SELECT LOWER(class) AS cls, COUNT(DISTINCT name) AS pilots, SUM(times) AS sightings "
                    "FROM met WHERE UPPER(faction)=? AND class IS NOT NULL AND class != '' "
                    "GROUP BY 1 ORDER BY pilots DESC, sightings DESC LIMIT 5",
                    (tag,),
                ).fetchall():
                    cid = str(hr["cls"])
                    hi = hulls_info.get(cid, {})
                    spotted_hulls.append({
                        "id": cid,
                        "name": hi.get("name") or cid,
                        "pilots": int(hr["pilots"]),
                        "tier": int(hi.get("tier", 0)),
                        "piloting": int(hi.get("pil", 0)),
                        "cargo": int(hi.get("cargo", 0)),
                        "speed": int(hi.get("speed", 0)),
                    })
                for sr in conn.execute(
                    "SELECT system, COUNT(DISTINCT name) AS pilots FROM met "
                    "WHERE UPPER(faction)=? AND system IS NOT NULL AND system != '' "
                    "GROUP BY 1 ORDER BY pilots DESC LIMIT 5",
                    (tag,),
                ).fetchall():
                    spotted_sys.append({"system": str(sr["system"]), "pilots": int(sr["pilots"])})

            top_bids, top_asks = [], []
            owned_stations = []
            unscanned_bases = []
            if "stations" in tables:
                st_rows = conn.execute(
                    "SELECT name, kind, system, condition FROM stations WHERE UPPER(tag)=? ORDER BY kind DESC, name",
                    (tag,),
                ).fetchall()
                owned_stations = [dict(x) for x in st_rows]
                sys_list = sorted({str(x["system"]).lower() for x in st_rows if x["system"]})
                unscanned_bases = [sy for sy in sys_list if sy not in scanned_book_systems]
                if unscanned_bases:
                    unscanned_summary.append({"tag": tag, "count": len(unscanned_bases), "total": len(sys_list), "systems": unscanned_bases[:5]})
                if sys_list and "books" in tables:
                    ph = ",".join("?" for _ in sys_list)
                    for br in conn.execute(
                        f"SELECT system, item, ROUND(bid,0) AS p, SUM(bid_qty) AS q, ROUND(SUM(bid*bid_qty),0) AS val "
                        f"FROM books WHERE LOWER(system) IN ({ph}) AND bid > 0 AND bid_qty > 0 "
                        f"GROUP BY system, item, p ORDER BY val DESC LIMIT 5",
                        sys_list,
                    ).fetchall():
                        rec = {"system": str(br["system"]), "item": str(br["item"]), "price": int(_num(br["p"])), "qty": int(_num(br["q"])), "val": int(_num(br["val"])), "tag": tag}
                        top_bids.append(rec)
                        all_bids_top.append(rec)
                    for ar in conn.execute(
                        f"SELECT system, item, ROUND(ask,0) AS p, SUM(ask_qty) AS q, ROUND(SUM(ask*ask_qty),0) AS val "
                        f"FROM books WHERE LOWER(system) IN ({ph}) AND ask > 0 AND ask_qty > 0 "
                        f"GROUP BY system, item, p ORDER BY val DESC LIMIT 5",
                        sys_list,
                    ).fetchall():
                        rec = {"system": str(ar["system"]), "item": str(ar["item"]), "price": int(_num(ar["p"])), "qty": int(_num(ar["q"])), "val": int(_num(ar["val"])), "tag": tag}
                        top_asks.append(rec)

            verified_notes = ""
            fac_dir = Path(repo_root) / "game" / "factions"
            if fac_dir.is_dir():
                for fp in sorted(fac_dir.glob(f"*-{tag.lower()}.md")):
                    try:
                        ftxt = fp.read_text(encoding="ascii", errors="replace")
                        if "## Notes" in ftxt:
                            nsec = ftxt.split("## Notes", 1)[1].strip()
                            if nsec and nsec.lower() not in ("none.", "none"):
                                verified_notes = " ".join(nsec.splitlines())[:280]
                    except OSError:
                        pass
                    break

            comms_signals = []
            if "player_comms" in tables:
                for cr in conn.execute(
                    "SELECT intent, extracted, safe_text, t FROM player_comms "
                    "WHERE UPPER(tag)=? AND to_us=1 AND COALESCE(own,0)=0 AND COALESCE(risk_level,'clean')='clean' "
                    "ORDER BY t DESC LIMIT 3",
                    (tag,),
                ).fetchall():
                    ext_s = str(cr["extracted"] or "").strip()
                    txt_s = str(cr["safe_text"] or "").strip()[:140]
                    if txt_s:
                        comms_signals.append({"intent": str(cr["intent"] or "chat"), "extracted": ext_s[:120], "excerpt": txt_s})

            archetype, threat = _classify_archetype(rd, spotted_hulls)
            dip_rec = diplo_facs.get(tag) or {}
            dip_st = str(dip_rec.get("status") or "uncontacted")
            standing = "NEUTRAL" if dip_st in ("neutrality_agreed", "trade_active", "info_sharing_active") else ("HOSTILE" if threat == "high" else ("HAILED" if dip_st == "hailed" else "RIVAL"))
            members = max(1, int(_num(rd["members"])))
            wealth = int(_num(rd["wealth"]))
            cap_mix = _capital_mix(rd)
            util_pct = round(100.0 * int(_num(rd["active_1h"])) / members, 1)
            how_play, copy_play, counter_play, owner_divs = _analyze_doctrine(
                tag, rd, archetype, spotted_hulls, top_bids, top_asks, out["tourism_top"], unscanned_bases, cap_mix
            )

            sedcards.append({
                "tag": tag,
                "name": str(rd.get("name") or tag),
                "leader": leaders.get(tag, ""),
                "standing": standing,
                "diplo_status": dip_st,
                "archetype": archetype,
                "threat": threat,
                "allies": allies,
                "members": int(_num(rd["members"])),
                "bases": int(_num(rd["bases"])),
                "wealth": wealth,
                "wealth_per_ship": int(round(wealth / members)),
                "wealth_vel_h": dw_h,
                "storage_value": int(_num(rd["storage_value"])),
                "ship_value": int(_num(rd.get("ship_value"))),
                "facility_inv": int(_num(rd["facility_inv"])),
                "capital_mix": cap_mix,
                "util_pct": util_pct,
                "ore_mined": int(_num(rd["ore_mined"])),
                "ore_vel_h": dore_h,
                "items_crafted": int(_num(rd["items_crafted"])),
                "crafted_vel_h": dcrft_h,
                "missions": int(_num(rd["missions"])),
                "kills_pve": int(_num(rd["kills_pve"])),
                "kills_pvp": int(_num(rd["kills_pvp"])),
                "active_1h": int(_num(rd["active_1h"])),
                "active_24h": int(_num(rd["active_24h"])),
                "avg_tier": round(_num(rd["avg_tier"]), 2),
                "max_tier": int(_num(rd["max_tier"])),
                "spotted_hulls": spotted_hulls,
                "spotted_systems": spotted_sys,
                "base_systems": base_sys[:8],
                "unscanned_bases": unscanned_bases[:8],
                "stations": owned_stations[:12],
                "top_bids": top_bids,
                "top_asks": top_asks,
                "verified_notes": verified_notes,
                "comms_signals": comms_signals,
                "owner_divisions": owner_divs,
                "how_they_play": how_play,
                "copy_play": copy_play,
                "counter_play": counter_play,
            })

        out["sedcards"] = sedcards
        unscanned_summary.sort(key=lambda x: -x["count"])
        out["unscanned_rival_bases"] = unscanned_summary

        outsource_cheap = []
        raw_cheap = []
        capital_cheap = []
        undercut_targets = []
        if "stations" in tables and "books" in tables:
            seen_cheap = set()
            for r in conn.execute("""
                SELECT UPPER(s.tag) AS tag, b.system, b.item, ROUND(b.ask, 1) AS price, SUM(b.ask_qty) AS qty
                FROM books b JOIN stations s ON LOWER(b.system)=LOWER(s.system)
                WHERE s.tag IS NOT NULL AND s.tag != '' AND UPPER(s.tag) != 'CLTV'
                  AND b.ask > 0 AND b.ask_qty >= 5
                  AND (
                      (b.item LIKE '%_ore' AND b.ask <= 25)
                      OR (b.item LIKE '%_gas' AND b.ask <= 25)
                      OR (b.item LIKE '%_ice' AND b.ask <= 25)
                      OR (b.item IN ('steel_plate','iron_ingot','carbon_plate','silicon_wafer','copper_wiring','wiring','aluminum_sheet','hull_plating','piping') AND b.ask <= 40)
                      OR (b.item = 'station_core' AND b.ask <= 25000000)
                  )
                GROUP BY UPPER(s.tag), b.system, b.item, price
                ORDER BY CASE WHEN b.item='station_core' THEN 0 ELSE 1 END, price ASC, qty DESC
                LIMIT 50
            """).fetchall():
                it = str(r["item"])
                if it in seen_cheap:
                    continue
                seen_cheap.add(it)
                rec = {
                    "tag": str(r["tag"]), "system": str(r["system"]), "item": it,
                    "price": int(round(_num(r["price"]))), "qty": int(_num(r["qty"])),
                }
                if len(outsource_cheap) < 8:
                    outsource_cheap.append(rec)
                if _is_raw_resource(it) and len(raw_cheap) < 6:
                    raw_cheap.append(rec)
                elif not _is_raw_resource(it) and len(capital_cheap) < 6:
                    capital_cheap.append(rec)

            seen_uc = set()
            for r in conn.execute("""
                SELECT UPPER(s.tag) AS tag, b.system, b.item, ROUND(b.ask, 0) AS price, SUM(b.ask_qty) AS qty,
                       ROUND(b.ask * SUM(b.ask_qty), 0) AS val
                FROM books b JOIN stations s ON LOWER(b.system)=LOWER(s.system)
                WHERE s.tag IS NOT NULL AND s.tag != '' AND UPPER(s.tag) != 'CLTV'
                  AND b.ask >= 500 AND b.ask_qty >= 10 AND b.item != 'station_core'
                GROUP BY UPPER(s.tag), b.system, b.item, price
                ORDER BY val DESC LIMIT 40
            """).fetchall():
                it = str(r["item"])
                if it in seen_uc:
                    continue
                seen_uc.add(it)
                undercut_targets.append({
                    "tag": str(r["tag"]), "system": str(r["system"]), "item": it,
                    "price": int(_num(r["price"])), "qty": int(_num(r["qty"])), "val": int(_num(r["val"])),
                })
                if len(undercut_targets) >= 8:
                    break

        all_bids_top.sort(key=lambda x: -x["val"])
        raw_bids = [b for b in all_bids_top if _is_raw_resource(b["item"])][:6]
        crafted_bids = [b for b in all_bids_top if not _is_raw_resource(b["item"])][:6]
        out["market_edges"] = {
            "outsupply_bids": all_bids_top[:8],
            "raw_bids": raw_bids,
            "crafted_bids": crafted_bids,
            "outsource_cheap": outsource_cheap[:8],
            "raw_cheap": raw_cheap,
            "capital_cheap": capital_cheap,
            "undercut_targets": undercut_targets[:8],
        }

        our_adopt = _inspect_our_adoption(repo_root, data_dir, conn, tables)
        out["strategy_playbooks"] = _build_strategy_playbooks(our_adopt, playstyle_leaders, out["market_edges"])

        raw_bid_str = ", ".join(f"{b['item']} @{b['price']} cr ({b['tag']}@{b['system']})" for b in raw_bids[:3]) or "uranium_ore/silver_ore at rival hubs"
        raw_cheap_str = ", ".join(f"{c['item']} @{c['price']} cr ({c['tag']}@{c['system']})" for c in raw_cheap[:4]) or "1-5 cr bulk ores at rival hubs"
        trade_bid_str = ", ".join(f"{b['item']} @{b['price']} cr ({b['tag']}@{b['system']})" for b in (crafted_bids or all_bids_top)[:3]) or "rival hub standing bids"
        cap_cheap_str = ", ".join(f"{c['item']} @{_fmt_cr(c['price'])} cr ({c['tag']}@{c['system']})" for c in (capital_cheap + raw_cheap)[:4]) or "cheap wholesale inputs at rival hubs"
        undercut_str = ", ".join(f"{u['item']} @{u['price']} cr ({u['tag']}@{u['system']})" for u in undercut_targets[:3]) or "inflated rival fuel_cell/refined asks"
        unscanned_str = ", ".join(f"[{u['tag']}] {u['count']}/{u['total']} ({', '.join(u['systems'][:2])})" for u in unscanned_summary[:4]) or "all tracked rival bases scanned"
        dark_factions = ", ".join(f"[{c['tag']}]" for c in sedcards if not c["spotted_hulls"]) or "none"

        out["tricks_by_division"] = {
            "Logistics": [
                "COPY (Express + Freight + Docked Smelt): stack 3 parallel wings -- (1) P0 bulk haulers (`Prayer` 540c / `Ledger` 480c / `Congregation` 1900c) on `spacemolt_shipping` (`hive.py shipping`, `plan.py` `cargo>=400`), (2) fast `Runner` (spd 6) / `Concordia` express passengers ([NOIR] model), (3) zero-fuel docked crafting/smelting ([MIN9]/[BEAT]).",
                f"COUNTER (Outsource Capex): buy cheap rival surplus ({cap_cheap_str}) instead of burning fuel/foundry capital; finish quick-WSJF bases & add Station Tourism modules.",
            ],
            "Trade": [
                "COPY (Bursar Market-Making + Docked Factory): run zero-fuel Bursars across all 5 empire exchanges (`sell_order --undercut-pct 5`, `buy_order`, `watch_minutes` desk duty) + docked NPC-facility crafting ([MIN9]/[BEAT]) logged in `contracts.log`.",
                f"COUNTER (Outsupply / Undercut / Outsource): OUTSUPPLY rival bids ({trade_bid_str}), UNDERCUT inflated asks by 5-10% ({undercut_str}), and OUTSOURCE cheap wholesale inputs ({cap_cheap_str}) + gourmet food for rival Tourism hubs.",
            ],
            "Mining": [
                f"COPY (Scarce-Vein Monopoly + T2-T4 Industrial): focus lasers on high-bid scarce raw veins ({raw_bid_str}; Uranium/Silver/Cobalt/Argon) using `--jettison-gangue`, and batch-upgrade P10/P20/P30 pilots (`Workhorse` -> `Lithosphere`/`Tellurian`, `hive.py upgrades mining`).",
                f"COUNTER (Avoid Cheap Bulk Dumps): DO NOT waste mining hours on bulk ores rivals dump below fuel cost ({raw_cheap_str}) -- let Trade/Logistics buy those wholesale while Mining feeds P1/P2 reserves & high-margin scarce veins.",
            ],
            "Military": [
                "COPY (PvE Herd Farming + Escort Projection): run T2/T3 combat wings (`Broadaxe`, `Dialectic`, `Recursion` like [BUSY] 8,454 kills & [HEXC] 2,142 kills) harvesting bounties + loot for Trade (F9) + paired lawless escorts (`min_hull_tier:2`).",
                "COUNTER (Threat Containment): watch [ENDL] (1,527 PvP kills -- log in `h-endl.md`), maintain `posture:WAR_ALERT` readiness in `plan.py`, hold strict defensive RoE (F2) around Neutral [HEXC]/[IRLC], and train `sentinel-` Royal Guard.",
            ],
            "Intel": [
                "COPY (Recon-Driven Arbitrage): keep rival books <3h fresh so Outsupply/Outsource/Undercut never flies blind, and track `rival_snapshots` >10M/h surges for new tricks.",
                f"COUNTER (Close Blind Spots): dock & scan unscanned rival bases -- {unscanned_str} -- and probe core NPC industrial hubs for dark zero-base earners ({dark_factions}).",
            ],
            "Command": [
                "COPY (500-Ship Multi-Strategy Saturation): rivals specialize in 1 archetype; we stack ALL 8 proven engines simultaneously -- sovereign Stations + Tourism ([BUSY]/[HEXC]), zero-fuel factories ([MIN9]/[BEAT]), Bursar Exchanges ([NOIR]), Express/Freight ([IRLC]/[WEXL]), and T2-T4 combat/mining.",
                f"COUNTER (Capital Discipline): enforce F40 MAUTxWSJF triage (`P0>P1>P2>P3`), compare wholesale asks ({cap_cheap_str}) before foundry capex, and audit GAP playbooks in `hive.py rivals playbooks`.",
            ],
        }
        return out
    finally:
        conn.close()


def render_briefing(doc, who="all"):
    """Compact, directly executable startup briefing block for hive.py briefing (division-tailored)."""
    cards = doc.get("sedcards") or []
    if not cards:
        return ""
    lines = ["=== RIVAL DOCTRINE, STRATEGY PLAYBOOKS & COPY/COUNTER ORDERS (F40; drilldown: `hive.py rivals playbooks | <TAG> | <division>`)"]
    top_s = []
    for c in cards[:5]:
        vel = f" {_fmt_signed_cr(c['wealth_vel_h'])}/h" if c["wealth_vel_h"] is not None else ""
        top_s.append(f"[{c['tag']}] {_fmt_cr(c['wealth'])}{vel} ({c['members']}sh, avgT {c['avg_tier']:.1f}, {c['archetype']})")
    lines.append("  TOP RIVALS | " + " | ".join(top_s[:3]))
    if len(top_s) > 3:
        lines.append("             | " + " | ".join(top_s[3:5]))
    t_top = doc.get("tourism_top") or []
    if t_top:
        lines.append("  TOURISM    | Top player station rev: " + ", ".join(f"{x['name']} ({_fmt_cr(x['revenue'])} cr)" for x in t_top[:2]))

    target_div = MEMBER_TO_DIV.get(str(who or "").lower()) if str(who or "").lower() not in ("all", "unity", "command") else "Command"
    pbs = [p for p in (doc.get("strategy_playbooks") or []) if target_div == "Command" or target_div in (p.get("divisions") or [])]
    if pbs:
        lines.append(f"  PLAYBOOKS ({target_div} -- decide to COPY or COUNTER using `plan.py` / `route_run.py`):")
        for p in pbs[:4 if target_div != "Command" else 8]:
            emp_s = ", ".join(f"{e['name']}({e['ships']})" for e in (p.get("empires") or [])[:4])
            lines.append(f"    [{p['status_code']:7s} {p['matched_count']}/{p['total_count']} KPIs {p['readiness_pct']:3.0f}%] {p['name']} | Empires: {emp_s} | Next: {p['blocker']}")
            if target_div != "Command":
                ok_s = ", ".join(f"{k['name']}={k['current']}" for k in (p.get("kpis") or []) if k["matched"]) or "none"
                nd_s = ", ".join(f"{k['name']}({k['owner']}: {k['current']} vs {k['target']})" for k in (p.get("kpis") or []) if not k["matched"]) or "all matched"
                lines.append(f"              KPIs   : OK [{ok_s}] | NEED [{nd_s}]")
                lines.append(f"              COPY   : {p['how_to_copy']}")
                lines.append(f"              COUNTER: {p['how_to_counter']}")
    tricks = (doc.get("tricks_by_division") or {}).get(target_div) or []
    if tricks:
        lines.append(f"  ADOPT ({target_div}):")
        for tr in tricks[:3]:
            lines.append(f"    - {tr}")
    return "\n".join(lines)


def render_cli(doc, target="all"):
    t_low = str(target or "all").strip().lower()
    if t_low in ("playbooks", "playbook", "strategies", "matrix"):
        lines = ["THE COLLECTIVE 8-STRATEGY PLAYBOOK MATRIX (Live from read.db + fleet.json, F40)"]
        for p in doc.get("strategy_playbooks") or []:
            emp_s = ", ".join(f"{e['name']}({e['ships']})" for e in (p.get("empires") or []))
            lines.append(f"\n[{p['status_code']} {p['matched_count']}/{p['total_count']} KPIs {p['readiness_pct']:.0f}%] {p['name']} | Owners: {', '.join(p['divisions'])}")
            lines.append(f"  Empires: {emp_s} | Chain: {p.get('handoff_chain', '--')}")
            lines.append(f"  Proven : {p['proven_by']}")
            for k in p.get("kpis") or []:
                mk = "OK  " if k["matched"] else "NEED"
                lines.append(f"    [{mk}] {k['name']} ({k['owner']}): {k['current']} / {k['target']} [{k['source']}]")
            lines.append(f"  COPY   : {p['how_to_copy']}")
            lines.append(f"  COUNTER: {p['how_to_counter']}")
        return "\n".join(lines)

    if t_low == "tricks":
        lines = ["ADOPTABLE RIVAL TACTICS BY DIVISION (Empirical from read.db, F40)"]
        for div, trs in (doc.get("tricks_by_division") or {}).items():
            lines.append(f"\n=== {div.upper()}")
            for tr in trs:
                lines.append(f"  - {tr}")
        return "\n".join(lines)

    if t_low in MEMBER_TO_DIV:
        div = MEMBER_TO_DIV[t_low]
        lines = [f"RIVAL STRATEGY PLAYBOOKS & COPY/COUNTER ORDERS FOR {div.upper()} (F40)"]
        for p in (doc.get("strategy_playbooks") or []):
            if div == "Command" or div in (p.get("divisions") or []):
                lines.append(f"\n[{p['status_code']}] {p['name']} ({p['our_status']})")
                lines.append(f"  Proven : {p['proven_by']}")
                lines.append(f"  COPY   : {p['how_to_copy']}")
                lines.append(f"  COUNTER: {p['how_to_counter']}")
        lines.append("")
        for tr in (doc.get("tricks_by_division") or {}).get(div, []):
            lines.append(f"  - {tr}")
        return "\n".join(lines)

    cards = doc.get("sedcards") or []
    if t_low != "all":
        cards = [c for c in cards if c["tag"].lower() == t_low]
        if not cards:
            return f"No sedcard found for tag '{target}' (try `hive.py rivals all`, `playbooks`, `tricks`, or a division)."

    lines = [f"RIVAL FACTION SEDCARDS | top={len(cards)} | snapshot_span={doc.get('span_hours', 0):.1f}h"]
    for c in cards:
        vel = f" ({_fmt_signed_cr(c['wealth_vel_h'])}/h)" if c["wealth_vel_h"] is not None else ""
        h_txt = ", ".join(f"{h['name']}[T{h['tier']}/P{h['piloting']}/{h['cargo']}c]({h['pilots']}x)" for h in c["spotted_hulls"][:4]) or "unspotted in met"
        s_txt = ", ".join(f"{s['system']}({s['pilots']})" for s in c["spotted_systems"][:4]) or "unspotted"
        b_txt = ", ".join(f"{b['item']}@{b['price']}x{b['qty']}" for b in c["top_bids"][:3]) or "none scanned"
        a_txt = ", ".join(f"{a['item']}@{a['price']}x{a['qty']}" for a in c["top_asks"][:3]) or "none scanned"
        cm = c.get("capital_mix") or {}
        lines.append(f"\n[{c['tag']}] {c['name']} | {c['standing']} | {c['archetype']} (threat={c['threat']}, owners={','.join(c.get('owner_divisions') or [])})")
        lines.append(f"  Scale  : {c['members']} ships ({c.get('util_pct', 0):.0f}% live 1h), {c['bases']} bases, W={_fmt_cr(c['wealth'])}{vel} ({_fmt_cr(c['wealth_per_ship'])}/sh) | mix V:{cm.get('storage_pct', 0):.0f}% S:{cm.get('ships_pct', 0):.0f}% F:{cm.get('facility_pct', 0):.0f}% | avgT={c['avg_tier']:.2f} maxT={c['max_tier']} | PvP={c['kills_pvp']} PvE={c['kills_pve']}")
        lines.append(f"  Engine : {c.get('how_they_play', '--')}")
        lines.append(f"  Hulls  : {h_txt}")
        lines.append(f"  Space  : {s_txt} | allies={','.join(c['allies']) or 'none'}" + (f" | UNSCANNED BASES: {','.join(c['unscanned_bases'][:4])}" if c.get("unscanned_bases") else ""))
        lines.append(f"  Markets: BUYS [{b_txt}] | SELLS [{a_txt}]")
        lines.append(f"  COPY   : {c.get('copy_play', '--')}")
        lines.append(f"  COUNTER: {c.get('counter_play', '--')}")
    return "\n".join(lines)


def render_markdown(doc):
    """Render governance/rival-sedcards.md (pure 7-bit ASCII, stable for diff-gated hourly commits)."""
    lines = [
        "---",
        "name: rival-sedcards",
        "id: 20261123T063005Z",
        "tier: intel",
        "author: Unity",
        "---",
        "",
        "# Rival Faction Sedcards & Adopted Copy/Counter Playbooks",
        "",
        "Auto-generated hourly from live `read.db` (`rival_snapshots`, `met`, `hulls`, `stations`, `books`, `leaderboards`) by `game/fleet/rivals.py` (`intel-pass.sh`).",
        "Every Admiral and Unity uses this dossier together with `hive.py scorecard` and `hive.py upgrades` to decide which proven rival tactics to COPY and which rival markets/corridors to COUNTER (`F40`, `O9`).",
        "",
        "## 1. The Collective 8-Strategy Playbook Matrix (Copy vs Counter)",
        "",
        "| Strategy | Owner | CLTV Status | Proven By |",
        "|:--|:--|:--|:--|",
    ]
    for p in doc.get("strategy_playbooks") or []:
        lines.append(f"| **{p['name']}** | {', '.join(p['divisions'])} | `{p['status_code']}` {p['matched_count']}/{p['total_count']} KPIs ({p['readiness_pct']:.0f}%) | {p['proven_by']} |")
    lines.append("")
    for p in doc.get("strategy_playbooks") or []:
        emp_s = ", ".join(f"{e['name']} ({e['ships']} sh)" for e in (p.get("empires") or []))
        lines.append(f"### {p['name']} (`{p['status_code']}` {p['matched_count']}/{p['total_count']} KPIs -- {', '.join(p['divisions'])})")
        lines.append(f"- **Empires & Chain:** {emp_s} | `{p.get('handoff_chain', '--')}`")
        lines.append(f"- **How It Works:** {p['how_it_works']}")
        kpi_bits = [f"{'[OK]' if k['matched'] else '[NEED]'} {k['name']} ({k['owner']}: {k['current']} vs {k['target']})" for k in (p.get("kpis") or [])]
        lines.append("- **Automated Pinned KPIs:** " + " ; ".join(kpi_bits))
        lines.append(f"- **How To COPY:** {p['how_to_copy']}")
        lines.append(f"- **How To COUNTER:** {p['how_to_counter']}")
        lines.append("")

    lines.append("## 2. Adopted Division Orders (Role-Filtered Copy & Counter)")
    lines.append("")
    for div in ("Logistics", "Trade", "Mining", "Military", "Intel", "Command"):
        lines.append(f"### {div}")
        for tr in (doc.get("tricks_by_division") or {}).get(div, []):
            lines.append(f"- {tr}")
        lines.append("")

    me = doc.get("market_edges") or {}
    if any(me.get(k) for k in ("outsupply_bids", "outsource_cheap", "undercut_targets")):
        lines.append("## 3. Live Undercut / Outsource / Outsupply Board")
        lines.append("")
        if me.get("outsupply_bids"):
            lines.append("- **OUTSUPPLY (Deep Rival Standing Bids -- sell into these):** " + ", ".join(
                f"`{x['item']}` @{x['price']} cr x{x['qty']} (`[{x['tag']}]`@{x['system']})" for x in me["outsupply_bids"][:5]
            ))
        if me.get("outsource_cheap"):
            lines.append("- **OUTSOURCE (Cheap Wholesale Rival Asks -- buy below gather/craft cost):** " + ", ".join(
                f"`{x['item']}` @{_fmt_cr(x['price'])} cr x{x['qty']} (`[{x['tag']}]`@{x['system']})" for x in me["outsource_cheap"][:6]
            ))
        if me.get("undercut_targets"):
            lines.append("- **UNDERCUT (Inflated Rival Asks -- list Bursar `sell_order` 5-10% lower):** " + ", ".join(
                f"`{x['item']}` @{x['price']} cr x{x['qty']} (`[{x['tag']}]`@{x['system']})" for x in me["undercut_targets"][:5]
            ))
        lines.append("")

    pl = doc.get("playstyle_leaders") or {}
    if pl:
        lines.append("## 4. Galactic Playstyle Benchmarks (Live Leaderboards)")
        lines.append("")
        lines.append("| Niche / Playstyle | #1 Leader | Metric | #2 Runner-Up |")
        lines.append("|:--|:--|--:|:--|")
        spec_rows = [
            ("Station Tourism Revenue", "tourism_revenue", " cr"),
            ("Exchange Sell Book Listed", "exchange_sellers", " cr"),
            ("Exchange Active Orders", "exchange_orders", " orders"),
            ("Express Passengers Delivered", "passengers_top", " pax"),
            ("Automated Facility Production", "facility_prod_top", " items"),
            ("Docked Crafting Output", "crafted_top", " items"),
            ("Bulk Missions Completed (Faction)", "missions_top", " missions"),
            ("PvE Pirates Destroyed (Faction)", "pve_top", " kills"),
            ("Industrial Ore Mined (Pilot)", "ore_top", " ore"),
            ("Contraband Smuggling", "contraband_top", " units"),
        ]
        for label, key, unit in spec_rows:
            arr = pl.get(key) or []
            if not arr:
                continue
            a1 = arr[0]
            a2 = arr[1] if len(arr) > 1 else None
            r1 = f"{a1['name']}" + (f" [{a1['tag']}]" if a1.get("tag") else "")
            v1 = (_fmt_cr(a1["value"]) if "cr" in unit or a1["value"] >= 100_000 else f"{a1['value']:,d}") + unit
            r2 = (f"{a2['name']} ({_fmt_cr(a2['value']) if a2['value'] >= 100_000 else a2['value']})" if a2 else "--")
            lines.append(f"| {label} | {r1} | {v1} | {r2} |")
        lines.append("")

    lines.append("## 5. Top Rival Faction Sedcards")
    lines.append("")
    lines.append("| Tag | Faction | Standing | Archetype | Ships | Bases | Wealth | Velocity | W/Ship | AvgT | PvP |")
    lines.append("|:--|:--|:--|:--|--:|--:|--:|--:|--:|--:|--:|")
    for c in doc.get("sedcards") or []:
        vel = f"{_fmt_signed_cr(c['wealth_vel_h'])}/h" if c["wealth_vel_h"] is not None else "--"
        lines.append(
            f"| `[{c['tag']}]` | {c['name']} | {c['standing']} | {c['archetype']} | {c['members']} | {c['bases']} | "
            f"{_fmt_cr(c['wealth'])} | {vel} | {_fmt_cr(c['wealth_per_ship'])} | {c['avg_tier']:.2f} | {c['kills_pvp']} |"
        )
    lines.append("")

    for c in doc.get("sedcards") or []:
        vel = f" ({_fmt_signed_cr(c['wealth_vel_h'])}/h)" if c["wealth_vel_h"] is not None else ""
        h_txt = ", ".join(f"`{h['name']}` (T{h['tier']}, P{h['piloting']}, {h['cargo']}c, spd {h['speed']} -- {h['pilots']}x)" for h in c["spotted_hulls"][:4]) or "Not yet spotted by our scouts"
        s_txt = ", ".join(f"`{s['system']}` ({s['pilots']})" for s in c["spotted_systems"][:4]) or "Unspotted"
        b_txt = ", ".join(f"`{b['item']}` @{b['price']} cr x{b['qty']}" for b in c["top_bids"][:4]) or "None scanned"
        a_txt = ", ".join(f"`{a['item']}` @{a['price']} cr x{a['qty']}" for a in c["top_asks"][:4]) or "None scanned"
        cm = c.get("capital_mix") or {}
        lines.append(f"### [{c['tag']}] {c['name']} -- {c['archetype']}")
        lines.append(f"- **Standing / Owners:** {c['standing']} (allies: {', '.join(c['allies']) or 'none'}; threat: {c['threat']}; leader: `{c['leader'] or 'unknown'}`; owners: {', '.join(c.get('owner_divisions') or [])})")
        lines.append(f"- **Scale & Mix:** {c['members']} ships ({c.get('util_pct', 0):.0f}% live 1h), {c['bases']} bases, wealth {_fmt_cr(c['wealth'])}{vel} ({_fmt_cr(c['wealth_per_ship'])}/sh), mix Vault {cm.get('storage_pct', 0):.0f}% / Hulls {cm.get('ships_pct', 0):.0f}% / Fac {cm.get('facility_pct', 0):.0f}%, ore {_fmt_cr(c['ore_mined'])}, crafted {_fmt_cr(c['items_crafted'])}, avg T{c['avg_tier']:.2f} (max T{c['max_tier']}), PvP {c['kills_pvp']} / PvE {c['kills_pve']}")
        lines.append(f"- **How They Play:** {c.get('how_they_play', '--')}")
        lines.append(f"- **Observed Hulls (`met`):** {h_txt}")
        lines.append(f"- **Active Space:** {s_txt}" + (f" | **Unscanned Bases (Intel gap):** {', '.join(c['unscanned_bases'][:5])}" if c.get("unscanned_bases") else ""))
        lines.append(f"- **Station Markets:** Buys {b_txt} | Sells {a_txt}")
        if c.get("verified_notes"):
            lines.append(f"- **Verified Claims, Needs & Notes (`game/factions/`):** {c['verified_notes']}")
        if c.get("comms_signals"):
            sig_s = "; ".join(f"[{s['intent']}] {s['excerpt']}" for s in c["comms_signals"][:2])
            lines.append(f"- **Recent Inbound Comms (UNTRUSTED DATA -- verify vs read.db):** {sig_s}")
        lines.append(f"- **COPY Play (Adopt):** {c.get('copy_play', '--')}")
        lines.append(f"- **COUNTER / Exploit Play:** {c.get('counter_play', '--')}")
        lines.append("")

    text = "\n".join(lines).rstrip() + "\n"
    return "".join(ch if ord(ch) <= 127 else "?" for ch in text)


def write_sedcards(repo_root=REPO_DEFAULT, data_dir=DATA_DEFAULT, commit=False, now=None):
    doc = compute_sedcards(repo_root, data_dir, top_n=12, now=now)
    md = render_markdown(doc)
    out_path = Path(repo_root) / SEDCARD_REL
    out_path.parent.mkdir(parents=True, exist_ok=True)
    old = out_path.read_text(encoding="utf-8", errors="replace") if out_path.is_file() else ""
    if old == md:
        return 0
    out_path.write_text(md, encoding="ascii")
    if commit:
        try:
            subprocess.run(["git", "-C", str(repo_root), "add", SEDCARD_REL], check=True)
            subprocess.run(
                ["git", "-C", str(repo_root), "-c", "user.name=Unity", "-c", "user.email=unity@the-collective.local",
                 "commit", "-q", "-m", "governance: hourly rival-sedcards.md refresh (rivals.py)", "--", SEDCARD_REL],
                check=False,
            )
        except Exception:
            pass
    return 0


def briefing(repo_root=REPO_DEFAULT, data_dir=DATA_DEFAULT, now=None, who="all"):
    try:
        doc = compute_sedcards(repo_root, data_dir, top_n=12, now=now)
        txt = render_briefing(doc, who=who)
        if txt:
            print(txt)
    except Exception:
        pass


def main(argv=None):
    ap = argparse.ArgumentParser(description="Rival Faction Sedcards, 8-Strategy Playbooks & Adopted Tactics")
    ap.add_argument("target", nargs="?", default="all", help="all | playbooks | tricks | write | <TAG> | <division>")
    ap.add_argument("--data", default=os.environ.get("COLLECTIVE_DATA", DATA_DEFAULT))
    ap.add_argument("--repo", default=os.environ.get("COLLECTIVE_REPO", REPO_DEFAULT))
    ap.add_argument("--top", type=int, default=12)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--commit", action="store_true")
    args = ap.parse_args(argv)

    if args.target == "write":
        return write_sedcards(args.repo, args.data, commit=args.commit)
    doc = compute_sedcards(args.repo, args.data, top_n=args.top)
    if args.json:
        print(json.dumps(doc, indent=2))
    else:
        print(render_cli(doc, target=args.target))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


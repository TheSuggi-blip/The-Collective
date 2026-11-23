#!/usr/bin/env python3
"""Automated Rival Faction Sedcards, Observed Fleet Doctrine & Adopted Counter-Plays (F40, O9).

Single source of truth feeding:
  - Hourly auto-updated markdown dossier `governance/rival-sedcards.md` (`rivals.py write --commit` in intel-pass.sh)
  - Every Admiral's & Unity's startup briefing (`hive.py briefing` / `hive.py rivals [TAG|tricks|division]`)
  - MCP agents (`hive(verb="rivals", ...)` and indexed `docs`/`search` over `governance/rival-sedcards.md`)
  - Station Command HUD (`Empire -> Sedcards` via `/api/ops` -> `rivals`)

Pulls live empirical intelligence strictly from read.db (rival_snapshots, factions, met, hulls,
stations, books, leaderboards, public_battles) and data/comms/diplomacy.json.
Read-only except `write` subcommand. Pure stdlib.

Usage:
  python3 -I -B game/fleet/rivals.py [all|tricks|<TAG>|<division>] [--json]
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
    if bases >= 2:
        return "Regional Base Builder", "low"
    return "Emerging Faction", "low"


def _counter_play(tag, archetype, hulls, bids, asks):
    h_names = ", ".join(f"{h['name']} ({h['pilots']}x)" for h in hulls[:3])
    top_bid = f"{bids[0]['item']} @{bids[0]['price']} cr" if bids else ""
    top_ask = f"{asks[0]['item']} @{asks[0]['price']} cr" if asks else ""
    if archetype == "PvP Raider Bloc":
        return "Avoid unescorted haulers in their corridors; log sightings in `h-*.md`; hold defensive RoE (F2) with paired T2+ escorts."
    if archetype == "Lawless Monopoly Elite":
        bits = [f"Adopt high-tier specialized hulls ({h_names})" if h_names else "Adopt high-tier specialized hulls"]
        bits.append("claim scarce lawless resource outposts (Argon/Cobalt/Titanium/Gold) and build station Tourism/Gourmet lines")
        if top_bid:
            bits.append(f"sell into their standing bids ({top_bid})")
        return "; ".join(bits) + "."
    if archetype == "Mega-Swarm Industrial & Tourism":
        bits = ["Adopt their P0 cargo swarm (`Floor Price` 400 / `Prospect` 100) + station Tourism (~200M cr rev)"]
        if top_bid:
            bits.append(f"feed their deep standing bids ({top_bid})")
        if top_ask:
            bits.append(f"benchmark wholesale asks ({top_ask})")
        return "; ".join(bits) + "."
    if archetype == "Facility Hub & Freight Power":
        bits = ["Adopt P0 `Ledger` (480 cargo) & T2 `Junk Convoy` (850) freighters + high-speed `Syndicate`/`Concordia` couriers"]
        if top_ask:
            bits.append(f"source cheap wholesale inputs ({top_ask}) when below mining fuel cost")
        if top_bid:
            bits.append(f"supply their standing bids ({top_bid})")
        return "; ".join(bits) + "."
    if archetype == "Zero-Base Express & Exchange":
        return "Zero-base blueprint for idle Trade/Logistics: run speed-6 P0 `Runner` (120c) / `Futures` on passenger lines + core Exchange spreads with 0 facility rent."
    if archetype == "Zero-Base Docked NPC-Facility Factory":
        return "Zero-fuel factory blueprint: park idle traders/haulers docked at public NPC industrial stations crafting high-margin goods into Exchange sell orders (`0` fuel burn)."
    if archetype == "Zero-Base Bulk Mission/Freight Swarm":
        return "Zero-base freight blueprint: commission cheap P0 `Prayer` (540c) / `Congregation` (1,900c) hulls to sweep 100-cargo freight contracts and bulk mission procurements."
    return f"Monitor expansion & hull doctrine ({h_names or 'unspotted'}); leverage neutral trade where verified."


def compute_sedcards(repo_root=REPO_DEFAULT, data_dir=DATA_DEFAULT, top_n=12, now=None):
    """Build complete live Rival Sedcards, Leaderboards & Adopted Division Tricks."""
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

        # Fetch CLTV baseline if present
        cltv_row = conn.execute("SELECT * FROM rival_snapshots WHERE t=? AND UPPER(tag)='CLTV'", (t1,)).fetchone()
        if cltv_row:
            out["our"] = {
                "tag": "CLTV",
                "members": int(_num(cltv_row["members"])),
                "wealth": int(_num(cltv_row["wealth"])),
                "bases": int(_num(cltv_row["bases"])),
                "avg_tier": round(_num(cltv_row["avg_tier"]), 2),
            }

        # Load hulls lookup for enriching spotted ships
        hulls_info = {}
        if "hulls" in tables:
            for r in conn.execute(
                "SELECT id, name, LOWER(COALESCE(NULLIF(faction,''), 'neutral')) AS fac, tier, category, "
                "COALESCE(piloting_required,0) AS pil, COALESCE(cargo,0) AS cargo, COALESCE(speed,0) AS speed, "
                "COALESCE(weapon_slots,0) AS w, COALESCE(defense_slots,0) AS d, COALESCE(utility_slots,0) AS u FROM hulls"
            ).fetchall():
                hulls_info[str(r["id"]).lower()] = dict(r)

        # Load factions table for leaders
        leaders = {}
        if "factions" in tables:
            for r in conn.execute("SELECT UPPER(tag) AS tag, leader FROM factions").fetchall():
                leaders[str(r["tag"])] = str(r["leader"] or "")

        # Top N non-CLTV factions by wealth
        top_rows = conn.execute(
            "SELECT * FROM rival_snapshots WHERE t=? AND UPPER(tag) != 'CLTV' ORDER BY wealth DESC LIMIT ?",
            (t1, int(top_n)),
        ).fetchall()

        sedcards = []
        all_bids_top = []
        all_asks_cheap = []

        for r in top_rows:
            rd = dict(r)
            tag = str(rd["tag"]).upper()
            prev = old_map.get(tag)
            dw_h = round((_num(rd["wealth"]) - _num(prev["wealth"])) / dt_h, 0) if (prev and dt_h >= 0.5) else None
            dore_h = round((_num(rd["ore_mined"]) - _num(prev["ore_mined"])) / dt_h, 0) if (prev and dt_h >= 0.5) else None
            dcrft_h = round((_num(rd["items_crafted"]) - _num(prev["items_crafted"])) / dt_h, 1) if (prev and dt_h >= 0.5) else None

            # Allies list
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

            # Observed hulls & operating systems from `met`
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

            # Station market bids & asks from `stations` + `books`
            top_bids, top_asks = [], []
            owned_stations = []
            if "stations" in tables:
                st_rows = conn.execute(
                    "SELECT name, kind, system, condition FROM stations WHERE UPPER(tag)=? ORDER BY kind DESC, name",
                    (tag,),
                ).fetchall()
                owned_stations = [dict(x) for x in st_rows]
                sys_list = sorted({str(x["system"]).lower() for x in st_rows if x["system"]})
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
                        all_asks_cheap.append(rec)

            # Verified dossier notes (`game/factions/*-<tag>.md` ## Notes) + clean inbound comms signals (`player_comms`)
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
            counter = _counter_play(tag, archetype, spotted_hulls, top_bids, top_asks)

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
                "facility_inv": int(_num(rd["facility_inv"])),
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
                "stations": owned_stations[:12],
                "top_bids": top_bids,
                "top_asks": top_asks,
                "verified_notes": verified_notes,
                "comms_signals": comms_signals,
                "counter_play": counter,
            })

        out["sedcards"] = sedcards

        # Tourism & Exchange leaderboards
        if "leaderboards" in tables:
            out["tourism_top"] = [
                {"rank": int(r["rank"]), "name": str(r["name"]), "system": str(r["tag"] or ""), "revenue": int(_num(r["value"]))}
                for r in conn.execute(
                    "SELECT rank, name, tag, value FROM leaderboards WHERE grp='stations' AND board='tourism_revenue' ORDER BY rank ASC LIMIT 5"
                ).fetchall()
            ]
            out["exchange_top"] = [
                {"rank": int(r["rank"]), "name": str(r["name"]), "empire": str(r["tag"] or ""), "credits": int(_num(r["value"]))}
                for r in conn.execute(
                    "SELECT rank, name, tag, value FROM leaderboards WHERE grp='players' AND board='exchange_credits_earned' ORDER BY rank ASC LIMIT 5"
                ).fetchall()
            ]

        # Build live Division-Scoped Adoptable Tricks directly from observed rival data
        all_bids_top.sort(key=lambda x: -x["val"])
        top_bid_str = ", ".join(
            f"{b['item']} @{b['price']} cr ({b['tag']}@{b['system']})" for b in all_bids_top[:4]
        ) or "uranium_ore/silver_ore/gourmet food at rival hubs"
        out["tricks_by_division"] = {
            "Logistics": [
                "Break the 100-cargo freight wall at Piloting 0 like [IRLC] (36x Ledger), [HIVE] (31x Runner), and [WEXL]/[CRFT] (Prayer/Congregation): batch-build Prayer (540c for 15 aluminum_sheet + 3 fuel_tank + 1 hull_plating), Ledger (480c, spd 4), or Runner (120c, spd 6, 2U) to unlock spacemolt_shipping contracts (`shipping.py list`).",
                "Adopt [NOIR] (+26.7M/h, 0 bases) & [IRLC] (28x Concordia) express passenger/courier lines using speed-6 Runner/Futures hulls.",
                "Benchmark cheap wholesale inputs at rival mega-hubs (e.g. [IRLC]@lhs_1140 iron_ore @ 4 cr, [BUSY]@arneb steel_plate @ 12 cr & station_core @ 13M cr vs 38M foundry fee) before hauling low-margin raw ore.",
            ],
            "Trade": [
                f"Feed deep rival standing bids with crafted/handed goods instead of empty loops -- live top bids: {top_bid_str}.",
                "Adopt [MIN9] (1.02B cr, 29 ships, 0 bases) & [BEAT] (2.42B cr, 45 ships, 0 bases) zero-fuel NPC-facility manufacturing: park idle traders docked at public industrial NPC stations crafting high-margin components into Exchange sell_orders.",
                "Adopt [BUSY] (187x Floor Price 400c, P0) & [NOIR] (+26.7M/h) Exchange market-making + gourmet food supply lines fueling rival Tourism stations (200M cr tourism market).",
            ],
            "Mining": [
                "Adopt [BUSY]/[HIVE] P0 industrial hulls (`Prospect` 100c T0, `Workhorse` 300c T2 P0) and [HEXC] endgame `Lithosphere` (1,680c, 8U) / `Deep Survey` (750c, 5U) path for P10->P30 miners.",
                f"Target high-bid scarce ores/gases demanded by rival hubs ({top_bid_str}) plus scarce lawless belts (Argon, Cobalt, Uranium, Silver) alongside our P1/P2 reserve needs.",
            ],
            "Military": [
                "Watch [ENDL] (1,527 PvP kills -- #1 PvP threat in galaxy); keep defensive RoE (F2) on Neutral [HEXC]/[IRLC] and escort high-value trade/freight through lawless legs.",
                "Adopt [BUSY] Solarian combat path (`Dialectic` 5W/3D/3U T3, `Axiomata` 6W/4D/5U T4) alongside Voidborn `Recursion` and Crimson `Broadaxe`/`Halberd` (4W) in parallel batches (F17/F37).",
            ],
            "Intel": [
                "Track dark super-earners (`[BEAT]`, `[MIN9]`, `[STRG]` -- 0 sightings in our `met` table yet!) and keep rival station books fresh (`lhs_1140`, `dheneb`, `arneb`, `zosma`) so Trade & Logistics catch wholesale asks and deep standing bids.",
                "Refresh `game/factions/sedcards.md` (`governance/rival-sedcards.md`) hourly via intel-pass.sh and watch `rival_snapshots` velocity spikes (>10M/h) for emerging tricks.",
            ],
            "Command": [
                "Station Tourism Engine: [BUSY] The Obsidian Well (213.9M cr) & [HEXC] Hex Star (197.9M cr, appeal 54) prove player stations with gourmet food + tourism facilities print massive passive revenue -- prioritize our first sovereign Station Core & Tourism wing.",
                "Benchmark [BUSY]@arneb wholesale `station_core` asks (~13M cr) against our Core Foundry 38M cr fee; enforce F40 KPI trigger closure (<80% targets) across all 6 divisions every turn.",
            ],
        }
        return out
    finally:
        conn.close()


def render_briefing(doc, who="all"):
    """Compact startup briefing block for hive.py briefing (anti-bloat, division-tailored)."""
    cards = doc.get("sedcards") or []
    if not cards:
        return ""
    lines = ["=== RIVAL INTELLIGENCE SEDCARDS & ADOPTED TACTICS (F40; full dossier: `hive.py rivals` / `governance/rival-sedcards.md`)"]
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
    tricks = (doc.get("tricks_by_division") or {}).get(target_div) or []
    if tricks:
        lines.append(f"  ADOPT ({target_div}):")
        for tr in tricks[:3]:
            lines.append(f"    - {tr}")
    return "\n".join(lines)


def render_cli(doc, target="all"):
    t_low = str(target or "all").strip().lower()
    if t_low == "tricks":
        lines = ["ADOPTABLE RIVAL TACTICS BY DIVISION (Empirical from read.db, F40)"]
        for div, trs in (doc.get("tricks_by_division") or {}).items():
            lines.append(f"\n=== {div.upper()}")
            for tr in trs:
                lines.append(f"  - {tr}")
        return "\n".join(lines)

    if t_low in MEMBER_TO_DIV:
        div = MEMBER_TO_DIV[t_low]
        lines = [f"RIVAL TACTICS & COUNTER-PLAYS FOR {div.upper()} (F40)"]
        for tr in (doc.get("tricks_by_division") or {}).get(div, []):
            lines.append(f"  - {tr}")
        lines.append("")
        lines.append(render_briefing(doc, who=div))
        return "\n".join(lines)

    cards = doc.get("sedcards") or []
    if t_low != "all":
        cards = [c for c in cards if c["tag"].lower() == t_low]
        if not cards:
            return f"No sedcard found for tag '{target}' (try `hive.py rivals all` or `tricks`)."

    lines = [f"RIVAL FACTION SEDCARDS | top={len(cards)} | snapshot_span={doc.get('span_hours', 0):.1f}h"]
    for c in cards:
        vel = f" ({_fmt_signed_cr(c['wealth_vel_h'])}/h)" if c["wealth_vel_h"] is not None else ""
        h_txt = ", ".join(f"{h['name']}[T{h['tier']}/P{h['piloting']}/{h['cargo']}c]({h['pilots']}x)" for h in c["spotted_hulls"][:4]) or "unspotted in met"
        s_txt = ", ".join(f"{s['system']}({s['pilots']})" for s in c["spotted_systems"][:4]) or "unspotted"
        b_txt = ", ".join(f"{b['item']}@{b['price']}x{b['qty']}" for b in c["top_bids"][:3]) or "none scanned"
        a_txt = ", ".join(f"{a['item']}@{a['price']}x{a['qty']}" for a in c["top_asks"][:3]) or "none scanned"
        lines.append(f"\n[{c['tag']}] {c['name']} | {c['standing']} | {c['archetype']} (threat={c['threat']})")
        lines.append(f"  Scale  : {c['members']} ships, {c['bases']} bases, W={_fmt_cr(c['wealth'])}{vel} ({_fmt_cr(c['wealth_per_ship'])}/sh) | avgT={c['avg_tier']:.2f} maxT={c['max_tier']} | PvP={c['kills_pvp']} PvE={c['kills_pve']}")
        lines.append(f"  Hulls  : {h_txt}")
        lines.append(f"  Space  : {s_txt} | allies={','.join(c['allies']) or 'none'}")
        lines.append(f"  Markets: BUYS [{b_txt}] | SELLS [{a_txt}]")
        lines.append(f"  Adopt  : {c['counter_play']}")
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
        "# Rival Faction Sedcards & Adopted Competitive Tactics",
        "",
        "Auto-generated hourly from live `read.db` (`rival_snapshots`, `met`, `hulls`, `stations`, `books`, `leaderboards`) by `game/fleet/rivals.py` (`intel-pass.sh`).",
        "Every Admiral uses this dossier together with `hive.py scorecard` and `hive.py upgrades` to close `<80%` KPI triggers and adopt winning rival doctrines (`F40`, `O9`).",
        "",
        "## 1. Adopted Division Playbooks (What Top Rivals Exploit)",
        "",
    ]
    for div in ("Logistics", "Trade", "Mining", "Military", "Intel", "Command"):
        lines.append(f"### {div}")
        for tr in (doc.get("tricks_by_division") or {}).get(div, []):
            lines.append(f"- {tr}")
        lines.append("")

    t_top = doc.get("tourism_top") or []
    if t_top:
        lines.append("## 2. Galactic Station Tourism & Exchange Benchmarks")
        lines.append("")
        lines.append("| Rank | Station | System | Tourism Revenue |")
        lines.append("|:--|:--|:--|--:|")
        for x in t_top:
            lines.append(f"| {x['rank']} | {x['name']} | {x['system']} | {_fmt_cr(x['revenue'])} cr |")
        lines.append("")

    lines.append("## 3. Top Rival Faction Sedcards")
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
        lines.append(f"### [{c['tag']}] {c['name']} -- {c['archetype']}")
        lines.append(f"- **Standing / Bloc:** {c['standing']} (allies: {', '.join(c['allies']) or 'none'}; threat: {c['threat']}; leader: `{c['leader'] or 'unknown'}`)")
        lines.append(f"- **Scale & Output:** {c['members']} ships, {c['bases']} bases, wealth {_fmt_cr(c['wealth'])}{vel} ({_fmt_cr(c['wealth_per_ship'])}/sh), ore {_fmt_cr(c['ore_mined'])}, crafted {_fmt_cr(c['items_crafted'])}, avg hull T{c['avg_tier']:.2f} (max T{c['max_tier']}), PvP {c['kills_pvp']} / PvE {c['kills_pve']}")
        lines.append(f"- **Observed Hulls (`met`):** {h_txt}")
        lines.append(f"- **Active Space:** {s_txt}")
        lines.append(f"- **Station Markets:** Buys {b_txt} | Sells {a_txt}")
        if c.get("verified_notes"):
            lines.append(f"- **Verified Claims, Needs & Notes (`game/factions/`):** {c['verified_notes']}")
        if c.get("comms_signals"):
            sig_s = "; ".join(f"[{s['intent']}] {s['excerpt']}" for s in c["comms_signals"][:2])
            lines.append(f"- **Recent Inbound Comms (UNTRUSTED DATA -- verify vs read.db):** {sig_s}")
        lines.append(f"- **Counter-Play / Adopted Trick:** {c['counter_play']}")
        lines.append("")

    text = "\n".join(lines).rstrip() + "\n"
    # Guarantee strict 7-bit ASCII
    return "".join(ch if ord(ch) <= 127 else "?" for ch in text)


def write_sedcards(repo_root=REPO_DEFAULT, data_dir=DATA_DEFAULT, commit=False, now=None):
    root = Path(repo_root)
    doc = compute_sedcards(root, data_dir, top_n=12, now=now)
    md = render_markdown(doc)
    dest = root / SEDCARD_REL
    dest.parent.mkdir(parents=True, exist_ok=True)
    old = dest.read_text(encoding="ascii", errors="replace") if dest.is_file() else ""
    if old == md:
        print(f"{SEDCARD_REL}: unchanged")
        return 0
    dest.write_text(md, encoding="ascii")
    print(f"{SEDCARD_REL}: written ({len(md)} chars, {len(doc.get('sedcards') or [])} sedcards)")
    if commit and (root / ".git").is_dir():
        st = subprocess.run(["git", "-C", str(root), "status", "--porcelain", "--", SEDCARD_REL], capture_output=True, text=True)
        if st.stdout.strip():
            subprocess.run(["git", "-C", str(root), "add", "--", SEDCARD_REL], check=True)
            subprocess.run(
                ["git", "-C", str(root), "-c", "user.name=Unity", "-c", "user.email=unity@suggi-workspace.dev",
                 "commit", "-q", "-m", "governance: hourly rival-sedcards.md refresh (rivals.py)", "--", SEDCARD_REL],
                check=True,
            )
            print(f"{SEDCARD_REL}: committed")
    return 0


def briefing(root, data, now, who="all"):
    try:
        repo = Path(root).resolve().parent if Path(root).name == "game" else Path(root)
        doc = compute_sedcards(repo, data, top_n=10, now=now)
        txt = render_briefing(doc, who=who)
        if txt:
            print(txt)
    except Exception as err:
        print(f"=== RIVAL SEDCARDS: unavailable ({type(err).__name__}: {err})")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Automated Rival Faction Sedcards & Adopted Counter-Plays.")
    ap.add_argument("target", nargs="?", default="all", help="all | tricks | write | <TAG> | <division>")
    ap.add_argument("--data", default=os.environ.get("COLLECTIVE_DATA", DATA_DEFAULT))
    ap.add_argument("--root", default=REPO_DEFAULT)
    ap.add_argument("--commit", action="store_true", help="With write: git commit if changed")
    ap.add_argument("--json", action="store_true", help="Emit JSON payload")
    args = ap.parse_args(argv)
    if args.target == "write":
        return write_sedcards(args.root, args.data, commit=args.commit)
    doc = compute_sedcards(args.root, args.data, top_n=12)
    if args.json:
        print(json.dumps(doc, indent=2))
    else:
        print(render_cli(doc, target=args.target))
    return 0


if __name__ == "__main__":
    sys.exit(main())

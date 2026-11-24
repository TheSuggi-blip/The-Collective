#!/usr/bin/env python3
"""Division KPI Scorecards, <80% Completion Triggers & Stagnation Detection.

Single source of truth shared by:
  - Every Admiral's & Unity's startup briefing (`hive.py briefing` / `hive.py scorecard`)
  - The Station Command HUD (`/api/ops` -> `scorecard` in the Metrics tab)

Design principles (SRE multi-window burn-rate + AgentOps leading/lagging + anti-alert-fatigue):
  1. Leading vs. lagging indicators: pairs readiness/capability percentages (employment,
     role- & empire-aware eligible hull upgrades, module fit saturation, playbook caps)
     against economic outcomes (fleet steady cashflow +/- & 24h direction, role KPI).
  2. Multi-window burn & hysteresis: compares 6h short window and 24h long window against
     prior windows with a +/-5% flat deadband to prevent alert flapping.
  3. <80% completion triggers: flags ALARM (<60%) and WARN (<80%) with exact gap counts
     and concrete next levers; stays silent on OK metrics inside startup briefings.
  4. Stagnation / momentum detection: synthesizes 5 compounding pillars (cashflow trend,
     wealth delta, skill/hull progression velocity, needs/roadmap advancement, productive
     flight-hour efficiency) into COMPOUNDING / GROWING_WITH_DRAG / SLOWING / STAGNATING.

Read-only. Pure stdlib.

Usage:
  python3 -I -B game/fleet/scorecard.py [--who all|Unity|Zero|Mercury|Apollo|Apophis|Oracle] [--json]
"""
import argparse
import json
import os
import re
import sqlite3
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import progression

DATA_DEFAULT = "/srv/collective/data"
REPO_DEFAULT = "/srv/collective/the-collective"

DIVISIONS = ("Command", "Mining", "Trade", "Logistics", "Military", "Intel")
DIV_HULL_CATEGORIES = {
    "Mining": {"industrial"},
    "Trade": {"commercial", "industrial"},
    "Logistics": {"commercial", "industrial"},
    "Military": {"combat", "combat support"},
    "Intel": {"exploration", "covert", "support"},
    "Command": {"combat", "combat support", "commercial", "exploration"},
}
MEMBER_TO_DIV = {
    "unity": "Command",
    "command": "Command",
    "zero": "Mining",
    "mining": "Mining",
    "miner": "Mining",
    "mercury": "Trade",
    "trade": "Trade",
    "trader": "Trade",
    "apollo": "Logistics",
    "logistics": "Logistics",
    "hauler": "Logistics",
    "apophis": "Military",
    "military": "Military",
    "drone": "Military",
    "sentinel": "Military",
    "oracle": "Intel",
    "intel": "Intel",
    "scout": "Intel",
}
DIV_TO_ADMIRAL = {
    "Command": "Unity",
    "Mining": "Zero",
    "Trade": "Mercury",
    "Logistics": "Apollo",
    "Military": "Apophis",
    "Intel": "Oracle",
}
DIV_KEY_LOWER = {d: d.lower() for d in DIVISIONS}

SEVERITY_RANK = {"ALARM": 0, "WARN": 1, "OK": 2}
TIER_RANK = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
TARGET_COMPLETION_PCT = 80.0
HYSTERESIS_PCT = 5.0

# Dynamic Context-Adaptive MAUT Weights (auto-selected live by enterprise posture; sum to 100)
POSTURE_WEIGHTS = {
    "PEACETIME_GROWTH": {
        "cashflow_eff": 25,
        "employment": 20,
        "upgrades": 25,
        "roadmap": 20,
        "seating_reqs": 10,
    },
    "CASHFLOW_RECOVERY": {
        "cashflow_eff": 35,
        "employment": 25,
        "upgrades": 18,
        "roadmap": 12,
        "seating_reqs": 10,
    },
    "WAR_ALERT": {
        "war_readiness": 40,
        "cashflow_eff": 20,
        "employment": 15,
        "upgrades": 15,
        "seating_reqs": 10,
    },
}
ENTERPRISE_WEIGHTS = dict(POSTURE_WEIGHTS["CASHFLOW_RECOVERY"])
# Responsibility Center Accounting model (Anthony & Govindarajan): each division is judged on what it controls.
# CapEx (hulls/modules/fit-fuel) is excluded from operating accrual; internal handovers are transfer-priced at IAS 2 NRV.
RESPONSIBILITY_CENTERS = {
    "Command": {"type": "Investment Center", "short": "Investment",
                "focus": "Fleetwide Net Worth, Consolidated Cash & Accrual, Seating, Roadmaps, CapEx Governance"},
    "Trade": {"type": "Profit Center", "short": "Profit Ctr",
              "focus": "Recurring Cash & Accrual Margin (net of handovers), Dynamic Market Hub Coverage"},
    "Mining": {"type": "Production Center", "short": "Production",
               "focus": "IAS 2 Accrual Value-Add (handovers + vault), Ore/ship-h, Belt Spread"},
    "Military": {"type": "Combat & Security Center", "short": "Combat/Sec",
                 "focus": "0 Losses, Combat XP & Kills, IAS 2 Loot Value-Add, Herd Spread"},
    "Logistics": {"type": "Service & Infra Center", "short": "Service/Infra",
                  "focus": "Supply Chains at Keep, Open P1/P2 Fulfillment SLA, Freight/Shipping, Zero Idle"},
    "Intel": {"type": "Recon Cost Center", "short": "Cost Ctr",
              "focus": "<3h Market/Place Freshness (enables Trade), 0 Losses, Diplomatic Comms SLA"},
}

DIVISION_WEIGHTS = {
    "employment": 30,
    "role_kpi": 30,
    "upgrades": 25,
    "hygiene": 15,
}

# MAUT + WSJF Triage Specs: code -> (alarm_tier, warn_tier, alarm_weight, warn_weight, effort 1..3)
# effort: 1 = quick route/config/batch fix (1.12x WSJF boost), 2 = standard ops (1.00x), 3 = multi-turn capital/XP (0.88x)
TRIAGE_SPECS = {
    "CASHFLOW_NEGATIVE": ("P0", "P1", 96, 78, 2),
    "TRADE_NET": ("P0", "P1", 94, 76, 2),
    "MILITARY_PERF": ("P0", "P1", 98, 72, 1),
    "DIV_IDLE": ("P0", "P1", 92, 76, 1),
    "FLEET_IDLE": ("P0", "P1", 92, 76, 1),
    "DIPLO_PENDING": ("P0", "P0", 90, 88, 1),
    "OPEN_REQUESTS": ("P0", "P1", 88, 76, 1),
    "SUPPLY_CHAINS": ("P0", "P1", 88, 76, 2),
    "PRODUCTIVE_EFFICIENCY": ("P1", "P1", 84, 72, 1),
    "SURPLUS_BACKLOG": ("P1", "P1", 82, 76, 1),
    "MINING_YIELD": ("P1", "P1", 82, 72, 2),
    "FIELD_CONGESTION": ("P1", "P2", 80, 64, 1),
    "HUB_CONGESTION": ("P1", "P2", 78, 62, 1),
    "DIV_HULL_UPGRADE": ("P1", "P1", 80, 70, 2),
    "HULL_UPGRADE_LAG": ("P1", "P1", 80, 70, 2),
    "OPEN_SEATS": ("P1", "P1", 76, 68, 1),
    "INTEL_FRESHNESS": ("P1", "P2", 80, 62, 1),
    "DIV_MODULE_FIT": ("P2", "P2", 60, 50, 2),
    "MODULE_FIT_SATURATION": ("P2", "P2", 60, 50, 2),
    "DIV_SKILL_TO_T2": ("P2", "P2", 52, 46, 3),
    "PLAYBOOK_CAP": ("P3", "P3", 30, 22, 1),
}

# Primary owning division for progression.py roadmap rungs
RUNG_OWNER = {
    "h1-productive-cashflow": "Trade",
    "h1-first-t2-hulls": "Mining",
    "h1-atria-outpost": "Logistics",
    "h1-intel-coverage": "Intel",
    "h2-seat-wave3": "Command",
    "h2-t2-standardization": "Command",
    "h2-outpost-ring": "Logistics",
    "h2-bursar-contracts": "Trade",
    "h3-yildun-station": "Command",
    "h3-armada-500": "Command",
    "h3-passengers-t5": "Logistics",
    "h3-galactic-top3": "Command",
}


def _wsjf_score(base_weight, gap_ratio=0.5, effort=2, direction="FLAT"):
    """MAUT x WSJF priority score clamped to 1..100 (quick wins & worsening trends bubble up)."""
    g = max(0.0, min(1.0, float(gap_ratio)))
    gap_mult = 0.72 + 0.44 * g
    eff_mult = {1: 1.12, 2: 1.00, 3: 0.88}.get(int(effort), 1.00)
    d = str(direction or "FLAT").upper()
    trend_adj = 10.0 if "WORSEN" in d else (-6.0 if "IMPROV" in d else 0.0)
    return max(1, min(100, int(round(float(base_weight) * gap_mult * eff_mult + trend_adj))))


def _annotate_trigger(t, gap_ratio=0.5):
    """Attach MAUT+WSJF tier, weight, effort, score, source to a trigger dict in-place."""
    code = t.get("code", "")
    sev = t.get("severity", "WARN")
    a_tier, w_tier, a_wt, w_wt, eff = TRIAGE_SPECS.get(code, ("P1", "P2", 75, 55, 2))
    tier = a_tier if sev == "ALARM" else w_tier
    base_wt = a_wt if sev == "ALARM" else w_wt
    score = _wsjf_score(base_wt, gap_ratio=gap_ratio, effort=eff, direction=t.get("direction", "FLAT"))
    t["tier"] = tier
    t["weight"] = base_wt
    t["effort"] = eff
    t["score"] = score
    t["source"] = "KPI"
    return t


def _triage_sort_key(item):
    return (TIER_RANK.get(item.get("tier", "P3"), 9), -int(item.get("score", 0)), SEVERITY_RANK.get(item.get("severity", "OK"), 9))


def _num(v, default=0.0):
    try:
        return float(v) if v is not None else float(default)
    except (TypeError, ValueError):
        return float(default)


def _fmt_cr(v):
    n = int(round(_num(v)))
    sign = "+" if n > 0 else ""
    if abs(n) >= 1_000_000:
        return f"{sign}{n / 1_000_000:.2f}M"
    if abs(n) >= 10_000:
        return f"{sign}{n / 1_000:.1f}k"
    return f"{sign}{n:,d}"


def _fmt_num(v):
    return f"{int(round(_num(v))):,d}"


def _classify_trend(curr, prev, min_abs=2000.0):
    """Classify direction with hysteresis deadband (+/-5% and min_abs) to prevent flapping."""
    if prev is None:
        return "FLAT", 0.0
    delta = _num(curr) - _num(prev)
    denom = max(abs(_num(prev)), min_abs)
    rel = (delta / denom) * 100.0
    if abs(delta) < min_abs or abs(rel) < HYSTERESIS_PCT:
        return "FLAT", round(delta, 1)
    return ("IMPROVING" if delta > 0 else "WORSENING"), round(delta, 1)


def _tier_required_for_piloting(piloting):
    p = int(_num(piloting))
    if p >= 50:
        return 5
    if p >= 30:
        return 4
    if p >= 20:
        return 3
    if p >= 10:
        return 2
    return 0


def _severity_pct(pct, alarm_below=60.0, warn_below=80.0):
    if pct < alarm_below:
        return "ALARM"
    if pct < warn_below:
        return "WARN"
    return "OK"


def _parse_open_requests(repo_root):
    """Parse open requests from communications/requests.log with sender, recipient, and need."""
    p = Path(repo_root) / "communications" / "requests.log"
    if not p.is_file():
        return []
    try:
        text = p.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return []
    blocks = re.split(r"(?m)^(?=## \[ENT-\d+\])", text)
    reqs = {}
    answered = set()
    for blk in blocks:
        blk = blk.strip()
        if not blk.startswith("## [ENT-"):
            continue
        first = blk.splitlines()[0]
        m = re.match(r"^## \[(ENT-\d+)\]\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)(?:\||$)", first)
        if not m:
            continue
        ent, ts_s, sender, kind = m.group(1), m.group(2).strip(), m.group(3).strip(), m.group(4).strip().lower()
        if kind in ("answer", "close", "done", "withdraw", "withdrawn"):
            see_part = first.split("see:", 1)[-1] if "see:" in first else ""
            for ref in re.findall(r"ENT-\d+", see_part):
                answered.add(ref)
            for ref in re.findall(r"(?im)^(?:see|closes|answers):\s*([^\n]+)", blk):
                for e2 in re.findall(r"ENT-\d+", ref):
                    answered.add(e2)
        elif kind == "request":
            m_to = re.search(r"(?im)^To:\s*([^.\n]+)", blk)
            m_nd = re.search(r"(?im)^Need:\s*([^\n]+)", blk)
            recip = m_to.group(1).strip() if m_to else "Unity"
            need = (m_nd.group(1).strip() if m_nd else "open request")[:96]
            reqs[ent] = {"ent": ent, "ts": ts_s, "sender": sender, "to": recip, "need": need}
    return [v for k, v in sorted(reqs.items()) if k not in answered]


def _count_open_requests(repo_root):
    return len(_parse_open_requests(repo_root))


def _load_json(path, default):
    p = Path(path)
    if not p.is_file():
        return default
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return default


def _detect_war_state(conn, tables, data_dir, now):
    """Auto-detect live War / Active Hostilities from empire.json, read.db faction/public_battles, and diplomacy.json."""
    at_war = False
    active_wars = []
    hostile_tags = []
    recent_cltv_battles = 0

    emp = _load_json(Path(data_dir) / "empire" / "empire.json", {})
    if isinstance(emp, dict):
        fac = emp.get("faction") if isinstance(emp.get("faction"), dict) else {}
        if fac.get("at_war"):
            at_war = True
        rel = emp.get("relations") if isinstance(emp.get("relations"), dict) else {}
        for w in (rel.get("wars") or []):
            tag = str(w.get("tag") or w.get("faction") or w) if isinstance(w, dict) else str(w)
            if tag and tag not in active_wars:
                active_wars.append(tag)
        for en in (rel.get("enemies") or []):
            tag = str(en.get("tag") or en.get("faction") or en) if isinstance(en, dict) else str(en)
            if tag and tag not in hostile_tags:
                hostile_tags.append(tag)

    dip = _load_json(Path(data_dir) / "comms" / "diplomacy.json", {})
    for tag, rec in ((dip.get("factions") or {}).items() if isinstance(dip, dict) else []):
        if isinstance(rec, dict) and str(rec.get("status") or "").lower() in ("war", "at_war"):
            if str(tag) not in active_wars:
                active_wars.append(str(tag))

    if conn is not None:
        if "faction" in tables:
            try:
                cols = {r[1] for r in conn.execute("PRAGMA table_info(faction)")}
                if "at_war" in cols:
                    row = conn.execute("SELECT at_war FROM faction LIMIT 1").fetchone()
                    if row and int(_num(row[0])):
                        at_war = True
            except Exception:
                pass
        if "public_battles" in tables:
            try:
                row = conn.execute(
                    "SELECT COUNT(*) FROM public_battles WHERE UPPER(COALESCE(tags,'')) LIKE '%CLTV%' AND LOWER(COALESCE(category,'')) IN ('pvp','faction','faction_war','war') AND (? - COALESCE(t,0)) <= 21600",
                    (int(now),),
                ).fetchone()
                if row:
                    recent_cltv_battles = int(_num(row[0]))
            except Exception:
                pass

    if active_wars or recent_cltv_battles > 0:
        at_war = True
    return {
        "at_war": bool(at_war),
        "active_wars": active_wars,
        "hostile_tags": hostile_tags,
        "recent_cltv_battles": recent_cltv_battles,
    }


def _load_diplomacy_pending(data_dir):
    doc = _load_json(Path(data_dir) / "comms" / "diplomacy.json", {})
    factions = doc.get("factions") if isinstance(doc, dict) else {}
    neutral_count = 0
    last_out_by_tag = {}
    leader_to_tag = {}
    legacy_pending = set()
    for tag, rec in (factions or {}).items():
        if not isinstance(rec, dict):
            continue
        t_up = str(rec.get("tag") or tag or "").upper()
        st = (rec.get("status") or "").lower()
        if st in ("neutrality_agreed", "trade_active", "info_sharing_active"):
            neutral_count += 1
        out_ts = str(rec.get("last_sent_at") or rec.get("last_outbound_at") or "")[:19]
        if t_up:
            last_out_by_tag[t_up] = out_ts
            ldr = str(rec.get("leader") or "").strip().lower()
            if ldr:
                leader_to_tag[ldr] = t_up
        in_ts = str(rec.get("last_inbound_at") or "")[:19]
        if in_ts and in_ts > out_ts and t_up:
            legacy_pending.add(t_up)

    _CLOSING_ACKS = (
        "likewise", "see you on the exchange", "see you out there", "fair lanes",
        "good trade", "good fortune", "safe travels", "thank you", "thanks",
        "understood", "noted", "sounds good", "glad to hear", "fly safe",
    )
    agreed_tags = set()
    for tag, rec in (factions or {}).items():
        if isinstance(rec, dict):
            t_up = str(rec.get("tag") or tag or "").upper()
            st = (rec.get("status") or "").lower()
            if t_up and st in ("neutrality_agreed", "trade_active", "info_sharing_active"):
                agreed_tags.add(t_up)

    latest_in = {}
    msg_p = Path(data_dir) / "comms" / "messages.jsonl"
    if msg_p.is_file() and last_out_by_tag:
        try:
            with open(msg_p, encoding="utf-8", errors="replace") as fh:
                for line in fh:
                    try:
                        m = json.loads(line)
                    except ValueError:
                        continue
                    if m.get("own") or str(m.get("channel") or "").lower() != "private":
                        continue
                    mtag = str(m.get("tag") or "").upper()
                    if mtag not in last_out_by_tag:
                        mtag = leader_to_tag.get(str(m.get("sender") or "").strip().lower(), "")
                    if mtag and mtag in last_out_by_tag:
                        ts = str(m.get("t") or m.get("seen_at") or "")[:19]
                        body = str(m.get("body") or m.get("text") or m.get("message") or "").strip()
                        if ts and ts > (latest_in.get(mtag) or ("", ""))[0]:
                            latest_in[mtag] = (ts, body)
        except OSError:
            pass

    pending_tags = set(legacy_pending)
    for t_up, (in_ts, body) in latest_in.items():
        out_ts = last_out_by_tag.get(t_up, "")
        if in_ts > out_ts:
            low_b = body.lower()
            is_closing = (
                t_up in agreed_tags and bool(out_ts) and len(body) <= 180
                and "?" not in body.replace(" ? ", " ") and any(k in low_b for k in _CLOSING_ACKS)
            )
            if not is_closing:
                pending_tags.add(t_up)
    return neutral_count, len(pending_tags), sorted(pending_tags)


def _load_fleet_live(data_dir):
    fj = _load_json(Path(data_dir) / "fleet" / "fleet.json", {})
    totals = fj.get("totals") if isinstance(fj.get("totals"), dict) else {}
    t_divs = totals.get("divisions") if isinstance(totals.get("divisions"), dict) else {}
    by_div = {d: {"total": 0, "working": 0, "idle": 0, "docked_waiting": 0, "adrift": 0, "credits": 0} for d in DIVISIONS}

    if t_divs:
        for d in DIVISIONS:
            td = t_divs.get(d)
            if isinstance(td, dict):
                tot = int(_num(td.get("ships")))
                wrk = int(_num(td.get("working")))
                prk = int(_num(td.get("parked")))
                adr = int(_num(td.get("adrift")))
                by_div[d] = {
                    "total": tot,
                    "working": wrk,
                    "idle": max(0, tot - wrk),
                    "docked_waiting": prk,
                    "adrift": adr,
                    "credits": int(_num(td.get("credits"))),
                }
        return by_div, totals, fj.get("updated_at") or ""

    # Fallback for test fixtures / simplified fleet.json without totals.divisions
    ships = fj.get("ships") or []
    if isinstance(ships, dict):
        ships = [{"name": k, **v} for k, v in ships.items()]
    for s in ships:
        if not isinstance(s, dict):
            continue
        div = s.get("division") or "Command"
        if div not in by_div:
            continue
        rec = by_div[div]
        rec["total"] += 1
        rec["credits"] += int(_num(s.get("credits")))
        stt = str(s.get("status") or "").lower()
        is_work = (stt == "working") or (stt in ("", "connected") and bool(s.get("order")))
        if is_work:
            rec["working"] += 1
        else:
            rec["idle"] += 1
            if s.get("docked"):
                rec["docked_waiting"] += 1
    return by_div, totals, fj.get("updated_at") or ""


def _load_watchdog_deltas(data_dir):
    ws = _load_json(Path(data_dir) / "fleet" / "watchdog.state.json", {})
    last = ws.get("last") if isinstance(ws, dict) else None
    hist = ws.get("history") if isinstance(ws, dict) and isinstance(ws.get("history"), list) else []
    base = None
    if isinstance(last, dict) and hist:
        last_ep = _num(last.get("epoch"))
        # Prefer snapshot ~6h ago (4-9h window), else earliest in history
        best = None
        best_diff = 1e18
        for h in hist:
            if not isinstance(h, dict):
                continue
            dt = last_ep - _num(h.get("epoch"))
            if dt >= 10800:
                diff = abs(dt - 21600)
                if diff < best_diff:
                    best_diff = diff
                    best = h
        base = best or (hist[0] if isinstance(hist[0], dict) else None)
    if not isinstance(last, dict) or not isinstance(base, dict):
        return {"dt_h": 0.0, "money_delta": None, "p10_delta": None, "t2_delta": None, "idle_delta": None}
    dt_h = max(0.0, (_num(last.get("epoch")) - _num(base.get("epoch"))) / 3600.0)
    return {
        "dt_h": round(dt_h, 2),
        "money_delta": int(_num(last.get("total_money")) - _num(base.get("total_money"))),
        "p10_delta": int(_num(last.get("p10_pilots")) - _num(base.get("p10_pilots"))),
        "t2_delta": int(_num(last.get("t2_hulls")) - _num(base.get("t2_hulls"))),
        "idle_delta": int(_num(last.get("idle_ships")) - _num(base.get("idle_ships"))),
    }


def _compute_field_saturation(repo_root, data_dir, conn=None, ship_divs=None):
    """Compute USE-method saturation for Mining belts, Military hunt POIs, and Trade Bursar hub coverage.
    Dynamic station/hub counts are derived live from read.db (books/places/systems/stations) -- never hardcoded.
    Never penalizes non-depleting Logistics hauling/shipping/crafting or one-time missions."""
    from collections import Counter, defaultdict
    out = {}
    for div in ("Mining", "Military"):
        out[div] = {
            "active_depleting": 0, "distinct_pois": 0, "max_per_poi": 0,
            "top_poi": "", "depleted_on_top": [], "crowded_pois": 0, "status": "OK",
        }
    out["Trade"] = {
        "active_depleting": 0, "distinct_pois": 0, "max_per_poi": 0,
        "top_poi": "", "depleted_on_top": [], "crowded_pois": 0, "status": "OK",
        "total_policed_hubs": 0, "total_book_hubs": 0, "total_public_stations": 0,
        "covered_hubs": 0, "uncovered_hubs": 0, "top_unserved": [],
    }
    odir = Path(data_dir) / "fleet" / "orders"
    rdir = Path(repo_root) / "game" / "routes"
    if not odir.is_dir() or not rdir.is_dir():
        return out
    orders = {}
    for p in odir.glob("*.json"):
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
            if isinstance(d, dict) and d.get("pilot") and d.get("what"):
                orders[str(d["pilot"])] = str(d["what"])
        except Exception:
            continue
    if not orders:
        return out
    route_cache = {}
    def _route_meta(kind, rid):
        key = (kind, rid)
        if key not in route_cache:
            poi, is_bursar = "", False
            rf = rdir / (rid + ".json")
            if rf.is_file():
                try:
                    rd = json.loads(rf.read_text(encoding="ascii", errors="replace"))
                    if kind == "mine":
                        poi = str(rd.get("belt") or "")
                    elif kind == "hunt":
                        poi = str(rd.get("place") or "")
                    elif kind == "circuit":
                        stops = rd.get("stops") or []
                        has_ord = any(isinstance(s, dict) and (s.get("sell_order") or s.get("buy_order")) for s in stops)
                        req = rd.get("requires") if isinstance(rd.get("requires"), dict) else {}
                        is_docked_desk = bool(req.get("docked_at")) or any(isinstance(s, dict) and s.get("watch_minutes") for s in stops)
                        if has_ord and (is_docked_desk or "bursar" in rid):
                            is_bursar = True
                            at0 = str(stops[0].get("at") or "") if stops and isinstance(stops[0], dict) else ""
                            poi = at0.split(":")[-1] if ":" in at0 else str(req.get("docked_at") or "")
                except Exception:
                    poi, is_bursar = "", False
            route_cache[key] = (poi, is_bursar)
        return route_cache[key]

    by_div = {"Mining": Counter(), "Military": Counter(), "Trade": Counter()}
    sdivs = ship_divs or {}
    for pilot, what in orders.items():
        parts = what.split(" ", 1)
        if len(parts) < 2:
            continue
        kind, rid = parts[0], parts[1]
        if kind == "mine":
            poi, _ = _route_meta("mine", rid)
            if poi and sdivs.get(pilot, "Mining") == "Mining":
                by_div["Mining"][poi] += 1
        elif kind == "hunt":
            poi, _ = _route_meta("hunt", rid)
            if poi and sdivs.get(pilot, "Military") == "Military":
                by_div["Military"][poi] += 1
        elif kind == "circuit":
            poi, is_bursar = _route_meta("circuit", rid)
            if is_bursar and poi and sdivs.get(pilot, "Trade") == "Trade":
                by_div["Trade"][poi] += 1

    depleted_by_poi = defaultdict(list)
    policed_hubs = []
    total_book_hubs = 0
    total_public_stations = 0
    if conn is not None:
        try:
            tbls = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()}
            if "fields" in tbls:
                for sys_id, poi_id, res, rem, mx in conn.execute(
                    "SELECT system, poi, resource, COALESCE(remaining,0), COALESCE(max_remaining,0) FROM fields"
                ).fetchall():
                    if mx and int(mx) > 0 and int(rem or 0) <= 0 and res not in ("iron_ore", "copper_ore"):
                        depleted_by_poi[f"{sys_id}:{poi_id}"].append(f"{res} 0/{int(mx)}")
            if "books" in tbls:
                total_book_hubs = int(_num(conn.execute("SELECT COUNT(DISTINCT base) FROM books").fetchone()[0]))
                if "places" in tbls and "systems" in tbls:
                    for b_id, emp, depth in conn.execute("""
                        SELECT b.base, COALESCE(s.empire, ''),
                               ROUND(SUM(COALESCE(b.bid,0) * COALESCE(b.bid_qty,0))) AS depth
                        FROM books b
                        LEFT JOIN places p ON p.base = b.base
                        LEFT JOIN systems s ON s.id = p.system
                        WHERE COALESCE(s.empire, '') != ''
                        GROUP BY b.base
                        ORDER BY depth DESC, b.base ASC
                    """).fetchall():
                        if b_id:
                            policed_hubs.append((str(b_id), str(emp), int(_num(depth))))
            if "stations" in tbls:
                total_public_stations = int(_num(conn.execute("SELECT COUNT(*) FROM stations").fetchone()[0]))
        except Exception:
            pass

    for div, warn_cap, alarm_cap in (("Mining", 10, 20), ("Military", 6, 10)):
        c = by_div[div]
        tot = sum(c.values())
        if not tot:
            continue
        top_poi, max_n = c.most_common(1)[0]
        dep = depleted_by_poi.get(top_poi, [])[:2] if div == "Mining" else []
        crowded = sum(1 for _p, n in c.items() if n >= warn_cap)
        if max_n >= alarm_cap or (max_n >= warn_cap and dep):
            st = "ALARM"
        elif max_n >= warn_cap:
            st = "WARN"
        else:
            st = "OK"
        out[div] = {
            "active_depleting": tot,
            "distinct_pois": len(c),
            "max_per_poi": max_n,
            "top_poi": top_poi,
            "depleted_on_top": dep,
            "crowded_pois": crowded,
            "status": st,
        }

    # Dynamic Trade Hub Saturation (1,000 orders/pilot cap -> 1-3 Bursars/hub; spread extras to unserved policed hubs)
    tc = by_div["Trade"]
    t_tot = sum(tc.values())
    pol_ids = [h[0] for h in policed_hubs]
    pol_set = set(pol_ids)
    cov_pol = sum(1 for b in tc if (not pol_set or b in pol_set))
    tot_pol = len(pol_ids)
    uncov = max(0, tot_pol - cov_pol)
    top_unserved = [
        f"{b} ({_fmt_cr(d)})" if d >= 100000 else b
        for b, _e, d in policed_hubs if b not in tc
    ][:4]
    t_top, t_max = tc.most_common(1)[0] if tc else ("", 0)
    t_crowded = sum(1 for _b, n in tc.items() if n >= 4)
    if t_max >= 10 and (uncov > 0 or tot_pol == 0):
        t_st = "ALARM"
    elif t_max >= 4 and (uncov > 0 or tot_pol == 0):
        t_st = "WARN"
    else:
        t_st = "OK"
    out["Trade"] = {
        "active_depleting": t_tot,
        "distinct_pois": len(tc),
        "max_per_poi": t_max,
        "top_poi": t_top,
        "depleted_on_top": [],
        "crowded_pois": t_crowded,
        "status": t_st,
        "total_policed_hubs": tot_pol,
        "total_book_hubs": total_book_hubs,
        "total_public_stations": total_public_stations,
        "covered_hubs": cov_pol,
        "uncovered_hubs": uncov,
        "top_unserved": top_unserved,
    }
    return out


def compute_scorecard(repo_root=REPO_DEFAULT, data_dir=DATA_DEFAULT, now=None, rivals_doc=None):
    """Compute complete enterprise & per-division KPI scorecard + alert triggers."""
    now = float(now if now is not None else time.time())
    db_path = Path(data_dir) / "store" / "read.db"
    conn = None
    tables = set()
    if db_path.is_file():
        conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True, timeout=3.0)
        conn.row_factory = sqlite3.Row
        tables = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type IN ('table','view')")}

    live_div, live_totals, fleet_ts = _load_fleet_live(data_dir)
    wd_deltas = _load_watchdog_deltas(data_dir)
    neutral_cnt, diplo_pending, diplo_pending_tags = _load_diplomacy_pending(data_dir)
    open_req_items = _parse_open_requests(repo_root)
    open_reqs = len(open_req_items)
    war_state = _detect_war_state(conn, tables, data_dir, now)

    # Progression snapshot (roadmap %, milestones, seating)
    prog = {}
    try:
        prog = progression.compute_progression(str(repo_root), data=str(data_dir), now=now) or {}
    except Exception:
        prog = {}

    # -----------------------------------------------------------------------
    # 1. SQL queries from read.db
    # -----------------------------------------------------------------------
    money_by_div = {}
    kpi_live = {}
    contrib_24h = {}
    ship_divs_map = {}
    field_sat = {}
    hulls_by_div = {d: {"total": 0, "t1_plus": 0, "t2_plus": 0, "eligible_p10": 0, "upgraded_eligible": 0,
                        "off_role_hulls": 0, "near_p10": 0, "max_piloting": 0, "sum_piloting": 0.0, "empires": {}} for d in DIVISIONS}
    mods_by_div = {d: {"ships": 0, "fitted_slots": 0, "max_slots": 0, "t2_mod_ships": 0, "off_role_ships": 0}
                   for d in DIVISIONS}
    pb_by_div = {}
    fuel_sinks = {"total_h": 0.0, "productive_h": 0.0, "jump_h": 0.0, "jump_net": 0.0, "census_h": 0.0}
    supply_ok, supply_tot, supply_short = 0, 0, []
    needs_open = []
    places_tot, places_fresh = 0, 0
    acc_24 = None
    acc_6 = None
    fac_members, fac_limit, fac_treasury = 0, 0, 0

    try:
        if conn is not None:
            # Faction seating
            if "faction" in tables:
                fr = conn.execute("SELECT member_count, members_limit, treasury FROM faction LIMIT 1").fetchone()
                if fr:
                    fac_members = int(_num(fr["member_count"]))
                    fac_limit = int(_num(fr["members_limit"]))
                    fac_treasury = int(_num(fr["treasury"]))

            # Live KPI figures (1h, 6h, 24h)
            if "stats_figures" in tables:
                for r in conn.execute(
                    "SELECT view, subject, figure, hours, value FROM stats_figures WHERE view IN ('kpi','contribution') AND hours IN (1, 6, 24)"
                ).fetchall():
                    v, subj, fig, hrs, val = r["view"], r["subject"], r["figure"], int(_num(r["hours"])), r["value"]
                    if v == "kpi" and subj == "Fleet":
                        kpi_live[(fig, hrs)] = _num(val) if val is not None else None
                    elif v == "contribution" and hrs == 24:
                        contrib_24h[(subj, fig)] = _num(val) if val is not None else None

            # Whole-hour cashflow history per division & Fleet (last 6h vs prior 6h, last 24h vs prior 24h)
            if "stats_money_hour" in tables:
                mx_r = conn.execute("SELECT MAX(hour) FROM stats_money_hour").fetchone()
                mx_h = int(_num(mx_r[0])) if mx_r and mx_r[0] is not None else 0
                if mx_h > 0:
                    for r in conn.execute("""
                        SELECT division,
                               AVG(CASE WHEN hour > ? - 21600 THEN net END) AS net_6h,
                               AVG(CASE WHEN hour <= ? - 21600 AND hour > ? - 43200 THEN net END) AS net_prev6h,
                               AVG(CASE WHEN hour > ? - 86400 THEN net END) AS net_24h,
                               AVG(CASE WHEN hour <= ? - 86400 AND hour > ? - 172800 THEN net END) AS net_prev24h,
                               AVG(CASE WHEN hour > ? - 86400 THEN income END) AS inc_24h,
                               AVG(CASE WHEN hour > ? - 86400 THEN costs END) AS costs_24h,
                               AVG(CASE WHEN hour > ? - 86400 THEN total END) AS total_24h,
                               COUNT(CASE WHEN hour > ? - 86400 THEN 1 END) AS n_24h,
                               COUNT(CASE WHEN hour <= ? - 86400 AND hour > ? - 172800 THEN 1 END) AS n_prev24h
                        FROM stats_money_hour
                        GROUP BY division
                    """, (mx_h,) * 12).fetchall():
                        money_by_div[r["division"]] = {
                            "net_6h": round(_num(r["net_6h"]), 1) if r["net_6h"] is not None else 0.0,
                            "net_prev6h": round(_num(r["net_prev6h"]), 1) if r["net_prev6h"] is not None else None,
                            "net_24h": round(_num(r["net_24h"]), 1) if r["net_24h"] is not None else 0.0,
                            "net_prev24h": round(_num(r["net_prev24h"]), 1) if r["net_prev24h"] is not None else None,
                            "inc_24h": round(_num(r["inc_24h"]), 1) if r["inc_24h"] is not None else 0.0,
                            "costs_24h": round(_num(r["costs_24h"]), 1) if r["costs_24h"] is not None else 0.0,
                            "total_24h": round(_num(r["total_24h"]), 1) if r["total_24h"] is not None else 0.0,
                            "n_24h": int(_num(r["n_24h"])),
                            "n_prev24h": int(_num(r["n_prev24h"])),
                        }

            # Hull upgrade readiness (role- & empire-aware!)
            if "ships" in tables:
                has_hulls = "hulls" in tables
                has_skills = "ship_skills" in tables
                hull_cols = {r[1] for r in conn.execute("PRAGMA table_info(hulls)").fetchall()} if has_hulls else set()
                cat_expr = "LOWER(COALESCE(h.category, '')) AS hull_cat" if "category" in hull_cols else "'' AS hull_cat"
                q = (f"""
                    SELECT s.pilot, s.division, LOWER(COALESCE(NULLIF(s.empire,''), 'voidborn')) AS emp,
                           COALESCE(h.tier, 0) AS tier,
                           {cat_expr},
                           COALESCE(sk.level, 0) AS piloting
                    FROM ships s
                    LEFT JOIN hulls h ON h.id = s.class OR h.name = s.class
                    LEFT JOIN ship_skills sk ON sk.pilot = s.pilot AND sk.skill = 'piloting'
                """) if (has_hulls and has_skills) else "SELECT pilot, division, 'voidborn' AS emp, 0 AS tier, '' AS hull_cat, 0 AS piloting FROM ships"
                for r in conn.execute(q).fetchall():
                    div = r["division"] or "Command"
                    if r["pilot"]:
                        ship_divs_map[str(r["pilot"])] = div
                    if div not in hulls_by_div:
                        continue
                    h = hulls_by_div[div]
                    tr = int(_num(r["tier"]))
                    pil = int(_num(r["piloting"]))
                    emp = str(r["emp"] or "voidborn")
                    hcat = str(r["hull_cat"] or "").strip().lower()
                    allowed_cats = DIV_HULL_CATEGORIES.get(div, set())
                    role_hull_ok = (not hcat) or (not allowed_cats) or (hcat in allowed_cats)
                    h["total"] += 1
                    h["sum_piloting"] += pil
                    if pil > h["max_piloting"]:
                        h["max_piloting"] = pil
                    h["empires"][emp] = h["empires"].get(emp, 0) + 1
                    if tr >= 1 and not role_hull_ok:
                        h["off_role_hulls"] += 1
                    if tr >= 1 and role_hull_ok:
                        h["t1_plus"] += 1
                    if tr >= 2 and role_hull_ok:
                        h["t2_plus"] += 1
                    req_t = _tier_required_for_piloting(pil)
                    if req_t >= 2:
                        h["eligible_p10"] += 1
                        if tr >= req_t and role_hull_ok:
                            h["upgraded_eligible"] += 1
                    elif pil >= 8:
                        h["near_p10"] += 1

            # Module fit saturation, T2+ modules, and off-role starter modules
            if "ships" in tables and "ship_modules" in tables and "hulls" in tables:
                for r in conn.execute("""
                    WITH per_ship AS (
                        SELECT s.pilot, s.division,
                               MAX(1, COALESCE(h.weapon_slots, 1) + COALESCE(h.defense_slots, 1) + COALESCE(h.utility_slots, 1)) AS max_slots,
                               SUM(CASE WHEN m.module IS NOT NULL AND NOT (
                                         (s.division='Mining' AND m.module='pulse_laser_i')
                                         OR (s.division IN ('Trade','Logistics','Intel') AND m.module IN ('mining_laser_i','ice_harvester_i','gas_harvester_i','pulse_laser_i'))
                                         OR (s.division='Military' AND m.module IN ('mining_laser_i','ice_harvester_i','gas_harvester_i'))
                                        ) THEN 1 ELSE 0 END) AS fitted,
                               SUM(CASE WHEN m.module LIKE '%_ii' OR m.module LIKE '%_iii' OR m.module LIKE '%_iv'
                                         OR m.module LIKE '%_v' OR m.module LIKE '%_mk2%' THEN 1 ELSE 0 END) AS t2_mods,
                               SUM(CASE WHEN (s.division='Mining' AND m.module='pulse_laser_i')
                                         OR (s.division IN ('Trade','Logistics','Intel') AND m.module IN ('mining_laser_i','ice_harvester_i','gas_harvester_i','pulse_laser_i'))
                                         OR (s.division='Military' AND m.module IN ('mining_laser_i','ice_harvester_i','gas_harvester_i'))
                                        THEN 1 ELSE 0 END) AS off_role
                        FROM ships s
                        LEFT JOIN hulls h ON h.id = s.class OR h.name = s.class
                        LEFT JOIN ship_modules m ON m.pilot = s.pilot
                        GROUP BY s.pilot
                    )
                    SELECT division, COUNT(*) AS ships,
                           SUM(fitted) AS fitted_slots, SUM(max_slots) AS max_slots,
                           SUM(CASE WHEN t2_mods > 0 THEN 1 ELSE 0 END) AS t2_mod_ships,
                           SUM(CASE WHEN off_role > 0 THEN 1 ELSE 0 END) AS off_role_ships
                    FROM per_ship GROUP BY division
                """).fetchall():
                    div = r["division"] or "Command"
                    if div in mods_by_div:
                        mods_by_div[div] = {
                            "ships": int(_num(r["ships"])),
                            "fitted_slots": int(_num(r["fitted_slots"])),
                            "max_slots": int(_num(r["max_slots"])),
                            "t2_mod_ships": int(_num(r["t2_mod_ships"])),
                            "off_role_ships": int(_num(r["off_role_ships"])),
                        }

            # Playbook caps (compute exact live chapter cap % matching guide.py drift; fallback to division_playbooks)
            if "division_playbooks" in tables:
                for r in conn.execute("SELECT division, max_chapter_pct, open_needs, ready_needs FROM division_playbooks").fetchall():
                    pb_by_div[str(r["division"] or "").lower()] = {
                        "max_chapter_pct": round(_num(r["max_chapter_pct"]), 1),
                        "open_needs": int(_num(r["open_needs"])),
                        "ready_needs": int(_num(r["ready_needs"])),
                    }
            try:
                import guidebook as _gb
                gb_root = Path(repo_root) / "game" / "routes" / "guidebook"
                if gb_root.is_dir():
                    for d_low in ("command", "mining", "trade", "logistics", "military", "intel"):
                        d_dir = gb_root / d_low
                        if not d_dir.is_dir():
                            continue
                        mx_p = 0.0
                        for md in d_dir.glob("*.md"):
                            cap = float(_gb.CARD_MAX if md.stem == "card" else _gb.CHAPTER_MAX)
                            body = md.read_text(encoding="ascii", errors="replace")
                            # Sum characters from first ### entry onward (exact guidebook.chapter_chars semantics)
                            pos = body.find("\n### ")
                            used = len(body) - pos if pos >= 0 else len(body)
                            pct = round(100.0 * used / max(1.0, cap), 1)
                            if pct > mx_p:
                                mx_p = pct
                        pb_by_div.setdefault(d_low, {})["max_chapter_pct"] = mx_p
            except Exception:
                pass

            # Fuel sinks / Productive efficiency (24h)
            if "fuel_sinks" in tables:
                for r in conn.execute("SELECT category, ship_hours_24h, net_credits_24h FROM fuel_sinks").fetchall():
                    cat = str(r["category"] or "")
                    sh = _num(r["ship_hours_24h"])
                    fuel_sinks["total_h"] += sh
                    if cat == "productive":
                        fuel_sinks["productive_h"] += sh
                    elif cat == "jump_loops":
                        fuel_sinks["jump_h"] += sh
                        fuel_sinks["jump_net"] += _num(r["net_credits_24h"])
                    elif cat == "census":
                        fuel_sinks["census_h"] += sh

            # Supply chains
            if "supply_status" in tables:
                for r in conn.execute("SELECT chain, item, status, stock, keep FROM supply_status").fetchall():
                    supply_tot += 1
                    st = str(r["status"] or "").upper()
                    if st in ("OK", "LOW"):
                        supply_ok += 1
                    else:
                        supply_short.append(f"{r['chain']}({int(_num(r['stock']))}/{int(_num(r['keep']))})")

            # Open P1/P2 needs
            if "need_status" in tables:
                for r in conn.execute(
                    "SELECT id, priority, division, covered, short_items, fee FROM need_status WHERE priority <= 2 AND COALESCE(covered,0) < 100 ORDER BY priority ASC, covered DESC"
                ).fetchall():
                    needs_open.append({
                        "id": str(r["id"]),
                        "priority": int(_num(r["priority"])),
                        "division": str(r["division"] or "").lower(),
                        "pct": round(_num(r["covered"]), 1),
                        "short": str(r["short_items"] or "")[:80],
                        "fee": int(_num(r["fee"])),
                    })

            # Places freshness (<3h)
            if "places" in tables:
                pr = conn.execute(
                    "SELECT COUNT(*) AS tot, SUM(CASE WHEN (? - COALESCE(t,0)) <= 10800 THEN 1 ELSE 0 END) AS fr FROM places",
                    (int(now),),
                ).fetchone()
                if pr:
                    places_tot = int(_num(pr["tot"]))
                    places_fresh = int(_num(pr["fr"]))
            field_sat = _compute_field_saturation(repo_root, data_dir, conn=conn, ship_divs=ship_divs_map)

            # GAAP/IFRS Cash-to-Accrual P&L & Transfer-Priced Division Attribution
            acc_24 = None
            acc_6 = None
            try:
                import accounting as _acc_sc
                _fj_sc = None
                _fp_sc = Path(data_dir) / "fleet" / "fleet.json"
                if _fp_sc.is_file():
                    try:
                        _fj_sc = json.loads(_fp_sc.read_text(encoding="utf-8", errors="replace"))
                    except (OSError, ValueError):
                        _fj_sc = None
                acc_24 = _acc_sc.compute_pnl(conn, repo_root=str(repo_root), data_dir=str(data_dir), fleet_json=_fj_sc, hours=24, now=now)
                acc_6 = _acc_sc.compute_pnl(conn, repo_root=str(repo_root), data_dir=str(data_dir), fleet_json=_fj_sc, hours=6, now=now)
            except Exception:
                acc_24 = None
                acc_6 = None
    finally:
        if not field_sat:
            field_sat = _compute_field_saturation(repo_root, data_dir, conn=None, ship_divs=ship_divs_map)
        if conn is not None:
            conn.close()

    # -----------------------------------------------------------------------
    # 2. Fleetwide Enterprise Pulse
    # -----------------------------------------------------------------------
    total_ships = sum(live_div[d]["total"] for d in DIVISIONS) or sum(hulls_by_div[d]["total"] for d in DIVISIONS) or 500
    total_working = sum(live_div[d]["working"] for d in DIVISIONS)
    total_idle = sum(live_div[d]["idle"] for d in DIVISIONS)
    intel_watch = 0
    # Strict Zero-Idle Accounting (Suggi 2026-11-23): only ships with an active task/order
    # (including docked crafting, Bursar desk duty, or market_poll watch) count as working.
    # Unassigned parked ships are genuinely IDLE in every division.
    eff_working = total_working
    emp_pct = round(100.0 * total_working / max(1, total_ships), 1)
    eff_emp_pct = emp_pct

    fl_m = money_by_div.get("Fleet", {})
    steady_1h = round(_num(kpi_live.get(("net", 1)), fl_m.get("net_6h", 0.0)), 1)
    steady_6h = round(_num(kpi_live.get(("net", 6)), fl_m.get("net_6h", 0.0)), 1)
    steady_24h = round(_num(kpi_live.get(("net", 24)), fl_m.get("net_24h", 0.0)), 1)
    steady_tiled_24h = fl_m.get("net_24h", steady_24h)
    steady_prev_24h = fl_m.get("net_prev24h")
    steady_prev_6h = fl_m.get("net_prev6h")
    all_in_24h = round(_num(kpi_live.get(("total", 24)), fl_m.get("total_24h", 0.0)), 1)
    wallets_now = int(_num(kpi_live.get(("wallets", 24)), sum(live_div[d]["credits"] for d in DIVISIONS)))
    treasury_now = int(_num(kpi_live.get(("treasury", 24)), fac_treasury))
    purse_now = wallets_now + treasury_now
    surplus_worth = int(_num(kpi_live.get(("surplus_worth", 24)), 0))

    once_direct_24h = int(acc_24["once_direct_h"]) if isinstance(acc_24, dict) else 0
    recurring_cash_24h = round(steady_24h - once_direct_24h, 1)
    inv_accrual_24h = int(acc_24["inventory_accrual_h"]) if isinstance(acc_24, dict) else 0
    accrual_op_24h = round(recurring_cash_24h + inv_accrual_24h, 1)
    once_direct_6h = int(acc_6["once_direct_h"]) if isinstance(acc_6, dict) else 0
    recurring_cash_6h = round(steady_6h - once_direct_6h, 1)
    inv_accrual_6h = int(acc_6["inventory_accrual_h"]) if isinstance(acc_6, dict) else 0
    accrual_op_6h = round(recurring_cash_6h + inv_accrual_6h, 1)
    has_accrual_24h = bool(acc_24.get("has_inventory_accrual")) if isinstance(acc_24, dict) else False

    cf_sign = "POSITIVE" if recurring_cash_24h > 0 else "NEGATIVE"
    cf_dir_24h, cf_delta_24h = _classify_trend(steady_tiled_24h, steady_prev_24h, min_abs=3000.0)
    cf_dir_6h, cf_delta_6h = _classify_trend(fl_m.get("net_6h", steady_6h), steady_prev_6h, min_abs=3000.0)

    prod_pct = round(100.0 * fuel_sinks["productive_h"] / max(0.01, fuel_sinks["total_h"]), 1) if fuel_sinks["total_h"] > 0 else 0.0
    jump_pct = round(100.0 * fuel_sinks["jump_h"] / max(0.01, fuel_sinks["total_h"]), 1) if fuel_sinks["total_h"] > 0 else 0.0

    open_seats = max(0, min(total_ships, fac_limit) - fac_members) if fac_limit else 0
    seat_cap_pct = round(100.0 * fac_members / max(1, min(total_ships, fac_limit)), 1) if fac_limit else 0.0
    seat_fleet_pct = round(100.0 * fac_members / max(1, total_ships), 1)

    fleet_elig_p10 = sum(hulls_by_div[d]["eligible_p10"] for d in DIVISIONS)
    fleet_upg_elig = sum(hulls_by_div[d]["upgraded_eligible"] for d in DIVISIONS)
    fleet_t1_plus = sum(hulls_by_div[d]["t1_plus"] for d in DIVISIONS)
    fleet_t2_plus = sum(hulls_by_div[d]["t2_plus"] for d in DIVISIONS)
    fleet_hulls_missing_t2 = max(0, fleet_elig_p10 - fleet_upg_elig)
    fleet_t0_missing = max(0, total_ships - fleet_t1_plus)
    fleet_hull_elig_pct = round(100.0 * fleet_upg_elig / max(1, fleet_elig_p10), 1) if fleet_elig_p10 else 0.0

    fleet_fitted = sum(mods_by_div[d]["fitted_slots"] for d in DIVISIONS)
    fleet_max_slots = sum(mods_by_div[d]["max_slots"] for d in DIVISIONS)
    fleet_empty_slots = max(0, fleet_max_slots - fleet_fitted)
    fleet_slot_pct = round(100.0 * fleet_fitted / max(1, fleet_max_slots), 1) if fleet_max_slots else 0.0
    fleet_off_role = sum(mods_by_div[d]["off_role_ships"] for d in DIVISIONS)
    unseated_ships = max(0, total_ships - fac_members)

    # Roadmap rungs & achieved milestones from progression.py
    roadmap_avg = 0.0
    ms_done, ms_tot, latest_ms = 0, 0, ""
    if isinstance(prog, dict):
        rungs = prog.get("rungs") or []
        if rungs:
            ms_tot = len(rungs)
            ms_done = sum(1 for r in rungs if _num(r.get("pct")) >= 100.0)
            roadmap_avg = round(sum(_num(r.get("pct")) for r in rungs) / ms_tot, 1)
        elif prog.get("overall_pct") is not None:
            roadmap_avg = round(_num(prog.get("overall_pct")), 1)
        mhist = prog.get("milestones") or []
        if mhist and isinstance(mhist[-1], dict):
            latest_ms = str(mhist[-1].get("title") or "")

    # Dynamic Posture Auto-Selection (WAR_ALERT > CASHFLOW_RECOVERY > PEACETIME_GROWTH)
    if war_state["at_war"]:
        posture = "WAR_ALERT"
    elif recurring_cash_24h <= 0:
        posture = "CASHFLOW_RECOVERY"
    else:
        posture = "PEACETIME_GROWTH"
    active_ent_weights = dict(POSTURE_WEIGHTS[posture])

    # Enterprise-level triggers (actionable only)
    ent_triggers = []
    if war_state["at_war"]:
        w_tags = ", ".join(war_state["active_wars"][:4]) or "hostile contact"
        ent_triggers.append({
            "severity": "ALARM", "code": "ACTIVE_WAR", "metric": "ACTIVE WAR POSTURE",
            "actual": f"wars=[{w_tags}], recent CLTV battles={war_state['recent_cltv_battles']}",
            "target": "war victory / 0 unescorted losses", "direction": "WORSENING",
            "action": "Shift fleet to war footing: escort all hauls, surge combat hulls/fits (Military), hold sub-1h hostile intel (Intel), stock repair/fuel bunkers (Logistics)",
            "tier": "P0", "weight": 100, "effort": 1, "score": 100, "source": "WAR",
        })
    if recurring_cash_24h <= 0:
        sev = "ALARM" if (cf_dir_24h == "WORSENING" or recurring_cash_24h < -20000) else "WARN"
        acc_note = f" | IAS2 accrual {_fmt_cr(accrual_op_24h)}/h" if has_accrual_24h else ""
        ent_triggers.append({
            "severity": sev, "code": "CASHFLOW_NEGATIVE", "metric": "Fleet Recurring Cashflow",
            "actual": f"{_fmt_cr(recurring_cash_24h)} cr/h matched (raw {_fmt_cr(steady_24h)}/h, 6h {_fmt_cr(recurring_cash_6h)}/h{acc_note})",
            "target": ">0 cr/h recurring cash", "direction": f"24h {cf_dir_24h} / 6h {cf_dir_6h}",
            "action": "Convert surplus vault stock to cash & cut empty jump loops; keep profitable once-missions & reserve crafts running (P1/F8/F39)",
        })
    if prod_pct < TARGET_COMPLETION_PCT and fuel_sinks["total_h"] > 0:
        ent_triggers.append({
            "severity": _severity_pct(prod_pct, 60.0, 80.0), "code": "PRODUCTIVE_EFFICIENCY",
            "metric": "Productive Flight Efficiency",
            "actual": f"{prod_pct:.1f}% (jump loops {jump_pct:.1f}%, {_fmt_cr(fuel_sinks['jump_net'])} cr/24h)",
            "target": ">=80%", "direction": cf_dir_6h,
            "action": "Replace empty jump-loops with cargo-carrying loops, docked crafting, or Station Bursar market-making",
        })
    if eff_emp_pct < 90.0:
        ent_triggers.append({
            "severity": _severity_pct(eff_emp_pct, 80.0, 90.0), "code": "FLEET_IDLE",
            "metric": "Fleet Idle Gap",
            "actual": f"{total_idle} idle ({eff_emp_pct:.1f}% working; {intel_watch} Intel watch)",
            "target": "0 idle (>=90% working)", "direction": "IMPROVING" if (wd_deltas["idle_delta"] or 0) < 0 else ("WORSENING" if (wd_deltas["idle_delta"] or 0) > 0 else "FLAT"),
            "action": "Admirals autonomously set far_ok for newborns past home Mastery (F16/F35/P6) so idle ships join main corridors",
        })
    if open_seats > 0 and seat_cap_pct < TARGET_COMPLETION_PCT:
        ent_triggers.append({
            "severity": _severity_pct(seat_cap_pct, 60.0, 80.0), "code": "OPEN_SEATS",
            "metric": "Faction Seating Gap",
            "actual": f"{open_seats} open seats in cap {fac_limit} ({unseated_ships} unseated; {seat_fleet_pct:.1f}% of {total_ships})",
            "target": "0 open seats (>=80% cap)", "direction": "FLAT",
            "action": f"Unity seats {open_seats} ready ships via wallet.py seat (F11/P4)",
        })
    if fleet_elig_p10 > 0 and fleet_hull_elig_pct < TARGET_COMPLETION_PCT:
        ent_triggers.append({
            "severity": _severity_pct(fleet_hull_elig_pct, 60.0, 80.0), "code": "HULL_UPGRADE_LAG",
            "metric": "Hull Upgrades Missing (P10+ -> T2+)",
            "actual": f"{fleet_hulls_missing_t2} P10+ missing T2+ ({fleet_upg_elig}/{fleet_elig_p10} done, {fleet_hull_elig_pct:.1f}%; {fleet_t0_missing} T0 left)",
            "target": "0 P10+ missing T2+ (>=80%)", "direction": "IMPROVING" if (wd_deltas["t2_delta"] or 0) > 0 else "FLAT",
            "action": "Parallel batch-upgrade P10+ pilots & P0 cargo freighters (Ledger/Prayer/Workhorse) via `hive.py upgrades` (F17/F37/O2)",
        })
    if fleet_slot_pct < TARGET_COMPLETION_PCT:
        ent_triggers.append({
            "severity": _severity_pct(fleet_slot_pct, 60.0, 80.0), "code": "MODULE_FIT_SATURATION",
            "metric": "Module Slots Missing",
            "actual": f"{fleet_empty_slots} empty slots ({fleet_slot_pct:.1f}% fit, {fleet_off_role} off-role starters)",
            "target": "0 empty / 0 off-role (>=80%)", "direction": "FLAT",
            "action": "Strip off-role starter modules (`unfit`) and fill open slots with role-matched T2+ modules (O2)",
        })
    for _sdiv in ("Mining", "Military"):
        _sd = field_sat.get(_sdiv) or {}
        if _sd.get("status") == "ALARM":
            _dep_s = ("; depleted: " + ", ".join(_sd["depleted_on_top"])) if _sd.get("depleted_on_top") else ""
            ent_triggers.append({
                "severity": "ALARM", "code": "FIELD_CONGESTION",
                "metric": f"{_sdiv} Field Saturation",
                "actual": f"{_sd['max_per_poi']} ships on {_sd['top_poi']} ({_sd['distinct_pois']} POIs for {_sd['active_depleting']} active{_dep_s})",
                "target": "spread <=8/belt (<=5/herd)", "direction": "FLAT",
                "action": f"Spread {_sdiv} ships across unsaturated scarce POIs & use jettison_gangue on scarce belts",
            })
    _tsat = field_sat.get("Trade") or {}
    if _tsat.get("status") == "ALARM":
        _un_s = ("; top unserved: " + ", ".join(_tsat["top_unserved"][:3])) if _tsat.get("top_unserved") else ""
        _hub_tot = _tsat.get("total_policed_hubs") or _tsat.get("distinct_pois")
        ent_triggers.append({
            "severity": "ALARM", "code": "HUB_CONGESTION",
            "metric": "Trade Hub Saturation",
            "actual": f"{_tsat['max_per_poi']} Bursars on {_tsat['top_poi']} ({_tsat['covered_hubs']}/{_hub_tot} policed hubs covered, {_tsat['uncovered_hubs']} uncovered{_un_s})",
            "target": "1-3 Bursars/hub, max hub coverage", "direction": "FLAT",
            "action": "Keep 1-3 Bursars per hub (1,000 order cap/pilot) and spread excess traders across unserved high-liquidity hubs",
        })
    _ent_gaps = {
        "CASHFLOW_NEGATIVE": min(1.0, abs(recurring_cash_24h) / 100000.0) if recurring_cash_24h < 0 else 0.3,
        "PRODUCTIVE_EFFICIENCY": max(0.0, (TARGET_COMPLETION_PCT - prod_pct) / TARGET_COMPLETION_PCT),
        "FLEET_IDLE": max(0.0, (90.0 - eff_emp_pct) / 90.0),
        "OPEN_SEATS": max(0.0, (TARGET_COMPLETION_PCT - seat_cap_pct) / TARGET_COMPLETION_PCT),
        "HULL_UPGRADE_LAG": max(0.0, (TARGET_COMPLETION_PCT - fleet_hull_elig_pct) / TARGET_COMPLETION_PCT),
        "MODULE_FIT_SATURATION": max(0.0, (TARGET_COMPLETION_PCT - fleet_slot_pct) / TARGET_COMPLETION_PCT),
        "FIELD_CONGESTION": 0.85,
        "HUB_CONGESTION": 0.80,
    }
    for _t in ent_triggers:
        if _t.get("code") == "ACTIVE_WAR":
            continue
        _annotate_trigger(_t, gap_ratio=_ent_gaps.get(_t["code"], 0.5))
        if posture == "WAR_ALERT" and _t.get("code") in ("HULL_UPGRADE_LAG", "MODULE_FIT_SATURATION"):
            _t["tier"] = "P0" if _t.get("severity") == "ALARM" else "P1"
            _t["score"] = min(100, int(_t.get("score", 50)) + 15)
    ent_triggers.sort(key=_triage_sort_key)

    # -----------------------------------------------------------------------
    # 3. Per-Division Scorecards
    # -----------------------------------------------------------------------
    divisions_out = {}
    for div in DIVISIONS:
        adm = DIV_TO_ADMIRAL[div]
        ld = live_div[div]
        hd = hulls_by_div[div]
        md = mods_by_div[div]
        dm = money_by_div.get(div, {})
        pb = pb_by_div.get(div.lower(), {})
        tot = ld["total"] or hd["total"]
        wrk = ld["working"]
        idl = ld["idle"]
        # Strict Zero-Idle Accounting: parked without an active order is always IDLE
        eff_wrk = wrk
        div_emp_pct = round(100.0 * eff_wrk / max(1, tot), 1)
        raw_emp_pct = round(100.0 * wrk / max(1, tot), 1)

        # Hull upgrade completion (role & empire aware)
        elig_p10 = hd["eligible_p10"]
        upg_elig = hd["upgraded_eligible"]
        avg_pil = round(hd["sum_piloting"] / max(1, hd["total"]), 1)
        missing_elig = max(0, elig_p10 - upg_elig)
        t0_missing_div = max(0, hd["total"] - hd["t1_plus"])
        if elig_p10 > 0:
            hull_pct = round(100.0 * upg_elig / elig_p10, 1)
            hull_mode = "eligible_t2"
            hull_label = (f"0 missing (all {elig_p10} P10+ T2+, 100%)" if missing_elig == 0
                          else f"{missing_elig} P10+ missing T2+ ({upg_elig}/{elig_p10} done, {hull_pct:.0f}%)")
            hull_sev = _severity_pct(hull_pct, 60.0, 80.0)
        else:
            # No pilots at P10 yet -- measure Piloting progression toward T2 gate + T1+ hulls
            hull_pct = round(min(100.0, (avg_pil / 10.0) * 100.0), 1)
            hull_mode = "piloting_to_t2"
            hull_label = f"0 P10+ yet (max P{hd['max_piloting']}, avg P{avg_pil}, {hd['near_p10']} at P8-9)"
            hull_sev = "WARN" if (hd["max_piloting"] < 8 and hd["t1_plus"] == 0) else ("OK" if hull_pct >= 80.0 else "WARN")

        # Module fit saturation & role purity
        div_empty_slots = max(0, md["max_slots"] - md["fitted_slots"])
        div_missing_t2_mod = max(0, (md["ships"] or tot) - md["t2_mod_ships"])
        slot_pct = round(100.0 * md["fitted_slots"] / max(1, md["max_slots"]), 1) if md["max_slots"] else 0.0
        t2_mod_pct = round(100.0 * md["t2_mod_ships"] / max(1, tot), 1)
        off_role_pct = round(100.0 * md["off_role_ships"] / max(1, tot), 1)
        mod_sev = "ALARM" if (slot_pct < 60.0 or off_role_pct > 25.0) else ("WARN" if (slot_pct < 80.0 or md["off_role_ships"] > 0) else "OK")

        # Division Responsibility-Center trend & GAAP/IFRS transfer-priced accrual
        d_net24 = dm.get("net_24h", 0.0)
        d_prev24 = dm.get("net_prev24h")
        d_net6 = dm.get("net_6h", 0.0)
        raw_trend, d_delta24 = _classify_trend(d_net24, d_prev24, min_abs=1500.0)
        _d_acc = ((acc_24 or {}).get("by_division") or {}).get(div) or {}
        d_rec24 = float(_d_acc.get("recurring_cash_h", d_net24)) if _d_acc else d_net24
        d_acc24 = float(_d_acc.get("accrual_op_h", d_rec24)) if _d_acc else d_rec24
        # Only Trade (Profit Center) uses raw/recurring cash trend; Production/Service/Cost Centers use Accrual or SLA!
        if div == "Trade":
            d_trend = "IMPROVING" if (d_rec24 > 0 and d_acc24 > 0 and raw_trend != "WORSENING") else raw_trend
        elif div == "Mining":
            d_trend = "IMPROVING" if (has_accrual_24h and d_acc24 > 10000) else ("FLAT" if (not has_accrual_24h or d_acc24 >= 0) else "WORSENING")
        elif div == "Military":
            _mlost = int(_num(contrib_24h.get(("Military", "ships_lost"))))
            d_trend = "WORSENING" if (_mlost > 0 or (has_accrual_24h and d_acc24 < -25000)) else ("IMPROVING" if (has_accrual_24h and d_acc24 >= 0) else "FLAT")
        elif div == "Logistics":
            d_trend = "IMPROVING" if (supply_tot > 0 and supply_ok >= supply_tot and idl == 0) else ("WORSENING" if (supply_tot > 0 and supply_ok < supply_tot * 0.6) else "FLAT")
        elif div == "Intel":
            _ilost = int(_num(contrib_24h.get(("Intel", "ships_lost"))))
            _ifresh = round(100.0 * places_fresh / max(1, places_tot), 1) if places_tot else round(_num(contrib_24h.get(("Intel", "place_fresh_share"))) * 100.0, 1)
            d_trend = "WORSENING" if (_ilost > 0 or _ifresh < 60.0) else ("IMPROVING" if (_ifresh >= 80.0 and _ilost == 0) else "FLAT")
        else:  # Command (Investment Center)
            d_trend = "IMPROVING" if (accrual_op_24h > 0 and cf_dir_6h == "IMPROVING") else ("WORSENING" if (accrual_op_24h <= 0 and cf_dir_24h == "WORSENING") else "FLAT")

        # Playbook cap check
        pb_pct = _num(pb.get("max_chapter_pct"))
        pb_sev = "ALARM" if pb_pct >= 95.0 else ("WARN" if pb_pct >= 90.0 else "OK")

        # Role-specific primary success KPI
        triggers = []
        emp_alarm_cut = 60.0 if div == "Command" else 80.0
        emp_warn_cut = 80.0 if div == "Command" else 90.0
        emp_sev = _severity_pct(div_emp_pct, emp_alarm_cut, emp_warn_cut)

        if emp_sev != "OK":
            triggers.append({
                "severity": emp_sev, "code": "DIV_IDLE", "metric": "Idle Ships Gap",
                "actual": f"{tot - eff_wrk} idle ({div_emp_pct:.1f}% working, {eff_wrk}/{tot})",
                "target": f"0 idle (>={int(emp_warn_cut)}%)", "direction": d_trend,
                "action": "Assign waiting ships now; set far_ok autonomously for newborns past home Mastery (F8/F16/F35)",
            })
        if hull_sev != "OK" and elig_p10 > 0:
            triggers.append({
                "severity": hull_sev, "code": "DIV_HULL_UPGRADE", "metric": "Eligible Hull Upgrades",
                "actual": hull_label, "target": ">=80% of P10+ upgraded",
                "direction": "IMPROVING" if (wd_deltas["t2_delta"] or 0) > 0 else "FLAT",
                "action": f"Parallel batch-upgrade P10+ {div} pilots to empire-specialized T2 hulls & measure in flight (`hive.py upgrades`, F17/F37)",
            })
        elif hull_sev == "WARN" and elig_p10 == 0:
            triggers.append({
                "severity": "WARN", "code": "DIV_SKILL_TO_T2", "metric": "Piloting Gate to T2",
                "actual": hull_label, "target": ">=80% toward P10 (T2 unlock)",
                "direction": "FLAT",
                "action": "Prioritize paying cargo/craft routes that level Piloting toward P10 without empty jump burn (O2/P1)",
            })
        if mod_sev != "OK":
            triggers.append({
                "severity": mod_sev, "code": "DIV_MODULE_FIT", "metric": "Module Slots Missing",
                "actual": f"{div_empty_slots} empty slots ({slot_pct:.1f}% fit), {div_missing_t2_mod} ships missing T2+, {md['off_role_ships']} off-role",
                "target": "0 empty / 0 off-role (>=80%)", "direction": "FLAT",
                "action": "Unfit off-role starter modules and fit role-matched T2+ modules across open slots (O2)",
            })
        div_sat = field_sat.get(div)
        if div_sat and div_sat.get("status") != "OK":
            if div == "Trade":
                _un_s = ("; top unserved: " + ", ".join(div_sat["top_unserved"][:3])) if div_sat.get("top_unserved") else ""
                _ht = div_sat.get("total_policed_hubs") or div_sat.get("distinct_pois")
                triggers.append({
                    "severity": div_sat["status"], "code": "HUB_CONGESTION", "metric": "Market Hub Saturation",
                    "actual": f"{div_sat['max_per_poi']} Bursars on {div_sat['top_poi']} ({div_sat['covered_hubs']}/{_ht} policed hubs, {div_sat['uncovered_hubs']} uncovered{_un_s})",
                    "target": "1-3 Bursars/hub (1,000 order cap/pilot)", "direction": "FLAT",
                    "action": "Keep 1-3 Bursars per station (1,000 order limit/pilot) and spread excess traders across unserved high-liquidity hubs",
                })
            else:
                _d_dep = ("; depleted: " + ", ".join(div_sat["depleted_on_top"])) if div_sat.get("depleted_on_top") else ""
                triggers.append({
                    "severity": div_sat["status"], "code": "FIELD_CONGESTION", "metric": "Field Saturation",
                    "actual": f"{div_sat['max_per_poi']} ships on {div_sat['top_poi']} ({div_sat['distinct_pois']} POIs for {div_sat['active_depleting']} active{_d_dep})",
                    "target": "spread <=8/belt (<=5/herd)", "direction": "FLAT",
                    "action": "Spread ships across unsaturated scarce POIs (max ~6-8/belt) and use jettison_gangue on scarce veins",
                })

        # Division-matched Role Success KPI
        if div == "Mining":
            ore_sh = round(_num(contrib_24h.get(("Mining", "ore_per_ship_hour"))), 1)
            ho_worth = int(_num(contrib_24h.get(("Mining", "handed_over_worth"))))
            role_kpi = {
                "name": "Extraction & Handover",
                "value": f"{ore_sh:.1f} ore/ship-h | {_fmt_cr(ho_worth)} cr/24h handed",
                "pct": min(100.0, round(ore_sh / 25.0 * 100.0, 1)) if ore_sh > 0 else 0.0,
                "status": "OK" if (ore_sh >= 15.0 and ho_worth > 0) else ("WARN" if ore_sh > 0 else "ALARM"),
                "cashflow_24h": round(d_net24, 1),
            }
            if role_kpi["status"] != "OK":
                triggers.append({
                    "severity": role_kpi["status"], "code": "MINING_YIELD", "metric": "Extraction Yield",
                    "actual": role_kpi["value"], "target": ">=15 ore/ship-h + active reserve handovers",
                    "direction": d_trend,
                    "action": "Upgrade to Laser II/III & richer reserve belts (silicon, carbon, gold, nickel); gift loads inward (P2/P5)",
                })
        elif div == "Trade":
            sell_cph = round(_num(contrib_24h.get(("Trade", "sell_cph"))), 0)
            tr_status = "OK" if (d_rec24 > 0 and d_trend != "WORSENING") else ("WARN" if d_rec24 > 0 else "ALARM")
            tr_acc_s = f" | accrual {_fmt_cr(d_acc24)}/h" if has_accrual_24h else ""
            role_kpi = {
                "name": "Trade Recurring Cash & Accrual",
                "value": f"{_fmt_cr(d_rec24)}/h recur{tr_acc_s} | sell {_fmt_cr(sell_cph)}/h",
                "pct": 100.0 if d_rec24 > 0 else 0.0,
                "status": tr_status,
                "cashflow_24h": round(d_rec24, 1),
            }
            if d_rec24 <= 0 or d_trend == "WORSENING":
                triggers.append({
                    "severity": "ALARM" if d_rec24 <= 0 else "WARN", "code": "TRADE_NET", "metric": "Trade Recurring Cashflow",
                    "actual": f"{_fmt_cr(d_rec24)} cr/h matched ({d_trend} vs {_fmt_cr(d_prev24)} prior{tr_acc_s})",
                    "target": ">0 cr/h & improving", "direction": d_trend,
                    "action": "Cap empty jump loops, liquidate surplus @ bid, expand Station Bursar orders & Ch1-Ch4 P2P trade (F39)",
                })
            if surplus_worth >= 250_000:
                triggers.append({
                    "severity": "WARN", "code": "SURPLUS_BACKLOG", "metric": "Unliquidated Surplus",
                    "actual": f"{_fmt_cr(surplus_worth)} cr @ bid sitting in vaults",
                    "target": "<250k cr backlog", "direction": "FLAT",
                    "action": "Run surplus.py & sell handed-over goods at or above bids / Exchange sell_order (P5/F39)",
                })
        elif div == "Logistics":
            chain_pct = round(100.0 * supply_ok / max(1, supply_tot), 1) if supply_tot else 100.0
            log_needs = [n for n in needs_open if (n.get("division") or "logistics") == "logistics"]
            log_reqs = [r for r in open_req_items if "apollo" in r["to"].lower() or "logistics" in r["to"].lower()]
            backlog_n = len(log_needs) + len(log_reqs)
            if log_needs:
                top_n = log_needs[0]
                bk_txt = f"{backlog_n} open P1/P2 ({top_n['id']} {top_n['pct']:.0f}%)"
            elif log_reqs:
                bk_txt = f"{len(log_reqs)} open req(s)"
            else:
                bk_txt = "0 open backlog"
            log_sev = _severity_pct(chain_pct, 60.0, 80.0)
            role_kpi = {
                "name": "Supply Chains & Fulfillment SLA",
                "value": f"chains {supply_ok}/{supply_tot} OK ({chain_pct:.0f}%) | {bk_txt}",
                "pct": chain_pct,
                "status": log_sev,
                "cashflow_24h": round(d_net24, 1),
            }
            if log_sev != "OK":
                triggers.append({
                    "severity": log_sev, "code": "SUPPLY_CHAINS", "metric": "Supply Chains at Keep",
                    "actual": f"{supply_ok}/{supply_tot} ({chain_pct:.1f}%): {', '.join(supply_short[:3])}",
                    "target": ">=80% chains OK", "direction": d_trend,
                    "action": "Refill short supply chains and fulfill active P1/P2 needs/requests; haul spacemolt_shipping freight when spare capacity exists",
                })
        elif div == "Military":
            cxp = round(_num(contrib_24h.get(("Military", "combat_xp_per_ship_hour"))), 1)
            kills = int(_num(contrib_24h.get(("Military", "kills"))))
            lost = int(_num(contrib_24h.get(("Military", "ships_lost"))))
            mil_fin_drag = (d_acc24 < -25000) if has_accrual_24h else (d_rec24 < -25000)
            mil_sev = "ALARM" if lost > 0 else ("WARN" if (cxp < 15.0 or mil_fin_drag) else "OK")
            role_kpi = {
                "name": "Combat XP, Kills & Losses",
                "value": f"{cxp:.1f} XP/ship-h | {kills} kills/24h | {lost} lost",
                "pct": 0.0 if lost > 0 else min(100.0, round(cxp / 25.0 * 100.0, 1)),
                "status": mil_sev,
                "cashflow_24h": round(d_rec24, 1),
            }
            if mil_sev != "OK":
                triggers.append({
                    "severity": mil_sev, "code": "MILITARY_PERF", "metric": "Combat Readiness & Losses",
                    "actual": role_kpi["value"] + (f" | accrual {_fmt_cr(d_acc24)}/h" if has_accrual_24h else f" | recur {_fmt_cr(d_rec24)}/h"),
                    "target": "0 lost, >=15 XP/ship-h", "direction": d_trend,
                    "action": "Validate T2 Recursion & pair hunts (F37), fit combat weapons, protect lines with zero unescorted losses (F2/O8)",
                })
        elif div == "Intel":
            fresh_pct = round(100.0 * places_fresh / max(1, places_tot), 1) if places_tot else round(_num(contrib_24h.get(("Intel", "place_fresh_share"))) * 100.0, 1)
            lost = int(_num(contrib_24h.get(("Intel", "ships_lost"))))
            int_sev = "ALARM" if (lost > 0 or fresh_pct < 60.0) else ("WARN" if (fresh_pct < 80.0 or diplo_pending > 0) else "OK")
            role_kpi = {
                "name": "Intel Freshness (<3h) & Comms",
                "value": f"{places_fresh}/{places_tot} fresh ({fresh_pct:.1f}%) | {neutral_cnt} neutral, {diplo_pending} pending reply",
                "pct": fresh_pct,
                "status": int_sev,
                "cashflow_24h": round(d_net24, 1),
            }
            if fresh_pct < TARGET_COMPLETION_PCT:
                triggers.append({
                    "severity": _severity_pct(fresh_pct, 60.0, 80.0), "code": "INTEL_FRESHNESS", "metric": "Place Freshness (<3h)",
                    "actual": f"{places_fresh}/{places_tot} ({fresh_pct:.1f}%)",
                    "target": ">=80% fresh (<3h)", "direction": d_trend,
                    "action": "Prioritize worked corridors, Ironlight book (<3h), and newborn regions; keep excess scouts on docked watch (F8/O7)",
                })
            if diplo_pending > 0:
                p_lbl = (" [" + ", ".join(diplo_pending_tags[:4]) + "]") if diplo_pending_tags else ""
                triggers.append({
                    "severity": "WARN", "code": "DIPLO_PENDING", "metric": "Unanswered Partner Comms",
                    "actual": f"{diplo_pending} inbound diplomatic reply(ies) awaiting response{p_lbl}",
                    "target": "0 unanswered", "direction": "FLAT",
                    "action": "Check diplomacy.py threads & coordinate Unity (Prime Directive) / Oracle envoy response (F4/O10)",
                })
        else:  # Command
            cmd_sev = "ALARM" if (recurring_cash_24h <= 0 or (open_seats > 0 and seat_cap_pct < 60.0)) else ("WARN" if (open_reqs > 0 or seat_cap_pct < 80.0) else "OK")
            role_kpi = {
                "name": "Enterprise Capital & Seating",
                "value": f"seats {fac_members}/{fac_limit} ({seat_cap_pct:.0f}%) | {open_reqs} open reqs | roadmap {roadmap_avg:.1f}%",
                "pct": seat_cap_pct if fac_limit else roadmap_avg,
                "status": cmd_sev,
                "cashflow_24h": round(recurring_cash_24h, 1),
            }
            if open_reqs > 0:
                triggers.append({
                    "severity": "ALARM" if open_reqs >= 5 else "WARN", "code": "OPEN_REQUESTS", "metric": "Open Requests to Unity",
                    "actual": f"{open_reqs} open request(s) in requests.log",
                    "target": "0 open", "direction": "FLAT",
                    "action": "Answer cross-division capital/seating/F10 requests; remind Admirals to decide division routing autonomously (F16)",
                })

        if pb_sev != "OK":
            triggers.append({
                "severity": pb_sev, "code": "PLAYBOOK_CAP", "metric": "Playbook Chapter Cap",
                "actual": f"{pb_pct:.1f}% of cap", "target": "<90% cap (F14)",
                "direction": "FLAT",
                "action": f"Compress bloated playbook chapters (`hive.py guide {div.lower()}`) below 90% cap (F14)",
            })

        _div_gaps = {
            "DIV_IDLE": max(0.0, (emp_warn_cut - div_emp_pct) / max(1.0, emp_warn_cut)),
            "DIV_HULL_UPGRADE": max(0.0, (TARGET_COMPLETION_PCT - hull_pct) / TARGET_COMPLETION_PCT),
            "DIV_SKILL_TO_T2": max(0.0, (TARGET_COMPLETION_PCT - hull_pct) / TARGET_COMPLETION_PCT),
            "DIV_MODULE_FIT": max(0.0, (TARGET_COMPLETION_PCT - slot_pct) / TARGET_COMPLETION_PCT),
            "MINING_YIELD": max(0.0, (100.0 - _num(role_kpi.get("pct"))) / 100.0),
            "FIELD_CONGESTION": min(1.0, ((div_sat or {}).get("max_per_poi", 0)) / 30.0),
            "HUB_CONGESTION": min(1.0, ((div_sat or {}).get("max_per_poi", 0)) / 25.0),
            "TRADE_NET": 0.9 if d_net24 <= 0 else 0.4,
            "SURPLUS_BACKLOG": min(1.0, surplus_worth / 1000000.0),
            "SUPPLY_CHAINS": max(0.0, (TARGET_COMPLETION_PCT - _num(role_kpi.get("pct"))) / TARGET_COMPLETION_PCT),
            "MILITARY_PERF": 1.0 if (div == "Military" and int(_num(contrib_24h.get(("Military", "ships_lost")))) > 0) else 0.5,
            "INTEL_FRESHNESS": max(0.0, (TARGET_COMPLETION_PCT - _num(role_kpi.get("pct"))) / TARGET_COMPLETION_PCT),
            "DIPLO_PENDING": min(1.0, 0.6 + 0.2 * diplo_pending),
            "OPEN_REQUESTS": min(1.0, open_reqs / 5.0),
            "PLAYBOOK_CAP": max(0.0, (pb_pct - 90.0) / 10.0),
        }
        for _t in triggers:
            _annotate_trigger(_t, gap_ratio=_div_gaps.get(_t["code"], 0.5))
            if posture == "WAR_ALERT":
                if div in ("Military", "Intel") and _t["code"] in ("MILITARY_PERF", "DIV_HULL_UPGRADE", "DIV_MODULE_FIT", "INTEL_FRESHNESS"):
                    _t["tier"] = "P0"
                    _t["score"] = min(100, int(_t["score"]) + 20)
                elif div == "Logistics" and _t["code"] == "SUPPLY_CHAINS":
                    _t["tier"] = "P0"
                    _t["score"] = min(100, int(_t["score"]) + 18)
                elif _t["code"] == "PLAYBOOK_CAP":
                    _t["score"] = max(1, int(_t["score"]) - 12)
        if posture == "WAR_ALERT" and div in ("Command", "Military", "Intel", "Logistics"):
            w_tags = ", ".join(war_state["active_wars"][:3]) or "active hostilities"
            war_act = {
                "Military": "Mobilize warships & Royal Guard; escort convoys, hunt hostiles, keep 0 unescorted losses",
                "Intel": "Hold <1h scout surveillance on enemy systems, fleet movements & pirate staging hubs",
                "Logistics": "Keep war-front fuel/repair bunkers at 100%; route convoys only with Military escort",
                "Command": "Direct fleet war budget, authorize combat hull/module surge & coordinate alliance defense",
            }[div]
            triggers.insert(0, {
                "severity": "ALARM", "tier": "P0", "weight": 100, "effort": 1, "score": 100, "source": "WAR",
                "code": "ACTIVE_WAR", "metric": "WAR FOOTING ACTIVE",
                "actual": f"posture=WAR_ALERT ({w_tags})", "target": "war priority", "direction": "WORSENING",
                "action": war_act,
            })
        triggers.sort(key=_triage_sort_key)
        div_status = triggers[0]["severity"] if triggers else "OK"

        # Weighted Division Health Score (0..100: 30% employment, 30% role KPI, 25% upgrades, 15% trend/hygiene)
        _upg_score = 0.60 * min(100.0, hull_pct) + 0.40 * min(100.0, slot_pct)
        _hyg_score = (100.0 if pb_pct < 90.0 else max(0.0, 100.0 - (pb_pct - 90.0) * 10.0))
        if d_trend == "WORSENING":
            _hyg_score = max(0.0, _hyg_score - 30.0)
        elif d_trend == "IMPROVING":
            _hyg_score = min(100.0, _hyg_score + 10.0)
        div_health = round(
            0.30 * min(100.0, div_emp_pct)
            + 0.30 * min(100.0, max(0.0, _num(role_kpi.get("pct"))))
            + 0.25 * _upg_score
            + 0.15 * _hyg_score,
            1,
        )

        # Unified Division Triage Queue (KPI triggers + routed open Requests + P1/P2 Needs + top Roadmap rung)
        div_triage = [dict(x) for x in triggers]
        seen_codes = {x["code"] for x in div_triage}

        for req in open_req_items:
            rto = req["to"].lower()
            if adm.lower() in rto or div.lower() in rto:
                rc = f"REQ_{req['ent']}"
                if rc not in seen_codes:
                    seen_codes.add(rc)
                    r_tier = "P0" if (div == "Command" and open_reqs >= 3) else "P1"
                    r_wt = 88 if r_tier == "P0" else 78
                    div_triage.append({
                        "severity": "ALARM" if r_tier == "P0" else "WARN",
                        "tier": r_tier, "weight": r_wt, "effort": 1,
                        "score": _wsjf_score(r_wt, gap_ratio=0.75, effort=1, direction="FLAT"),
                        "source": "REQ", "code": rc,
                        "metric": f"Request {req['ent']} ({req['sender']}->{req['to']})",
                        "actual": req["need"], "target": "answered", "direction": "FLAT",
                        "action": f"Answer {req['ent']} in requests.log via comms.py (F16)",
                    })

        for nd in needs_open:
            nd_div = nd["division"] or "logistics"
            if nd_div == div.lower() or (div == "Logistics" and nd_div in ("", "base", "all")):
                nc = f"NEED_{nd['id']}"
                if nc not in seen_codes:
                    seen_codes.add(nc)
                    is_p1 = nd["priority"] == 1
                    quick = nd["pct"] >= 80.0
                    eff = 1 if quick else (2 if nd["pct"] >= 40.0 else 3)
                    n_tier = "P1" if is_p1 else "P2"
                    n_wt = (86 if quick else 76) if is_p1 else (62 if quick else 50)
                    rem_ratio = (0.90 if quick else max(0.25, (100.0 - nd["pct"]) / 100.0))
                    div_triage.append({
                        "severity": "WARN" if is_p1 else "OK",
                        "tier": n_tier, "weight": n_wt, "effort": eff,
                        "score": _wsjf_score(n_wt, gap_ratio=rem_ratio, effort=eff, direction="FLAT"),
                        "source": "NEED", "code": nc,
                        "metric": f"P{nd['priority']} Need: {nd['id']}",
                        "actual": f"{nd['pct']:.1f}% stocked" + (f" (short: {nd['short'][:48]})" if nd["short"] else ""),
                        "target": "100% stocked", "direction": "FLAT",
                        "action": f"Close remaining {100.0 - nd['pct']:.1f}% gap (quick-finish WSJF priority)" if quick else f"Feed short inputs for {nd['id']} via reserve/wholesale",
                    })

        if isinstance(prog, dict):
            best_rung = None
            for rg in (prog.get("rungs") or []):
                rpct = _num(rg.get("pct"))
                if rpct >= 100.0:
                    continue
                rid = str(rg.get("id") or "")
                if RUNG_OWNER.get(rid) != div:
                    continue
                hor = str(rg.get("horizon") or "")
                r_tier = "P1" if "Days" in hor else ("P2" if "Weeks" in hor else "P3")
                quick = rpct >= 75.0
                eff = 1 if quick else (2 if "Days" in hor else 3)
                r_wt = (82 if quick else 72) if r_tier == "P1" else ((64 if quick else 54) if r_tier == "P2" else 36)
                r_sc = _wsjf_score(r_wt, gap_ratio=(0.85 if quick else (100.0 - rpct) / 100.0), effort=eff, direction="FLAT")
                cand = {
                    "severity": "WARN" if r_tier == "P1" else "OK",
                    "tier": r_tier, "weight": r_wt, "effort": eff, "score": r_sc,
                    "source": "ROADMAP", "code": f"RUNG_{rid}",
                    "metric": f"Roadmap: {str(rg.get('title') or rid)[:44]}",
                    "actual": f"{rpct:.1f}% ({hor})", "target": "100%", "direction": "FLAT",
                    "action": str(rg.get("bottleneck") or "Advance roadmap rung")[:100],
                }
                if best_rung is None or _triage_sort_key(cand) < _triage_sort_key(best_rung):
                    best_rung = cand
            if best_rung is not None and best_rung["code"] not in seen_codes:
                div_triage.append(best_rung)

        div_triage.sort(key=_triage_sort_key)

        divisions_out[div] = {
            "division": div,
            "admiral": adm,
            "responsibility_center": dict(RESPONSIBILITY_CENTERS.get(div, {})),
            "status": div_status,
            "trend_24h": d_trend,
            "cashflow_24h": round(d_net24, 1),
            "cashflow_prev24h": d_prev24,
            "cashflow_6h": round(d_net6, 1),
            "purse_24h": int(_d_acc.get("purse_h", round(d_net24))),
            "accounting_24h": {
                "recurring_cash_h": int(_d_acc.get("recurring_cash_h", round(d_net24))),
                "once_direct_h": int(_d_acc.get("once_direct_h", 0)),
                "once_net_h": int(_d_acc.get("once_net_h", 0)),
                "purse_h": int(_d_acc.get("purse_h", round(d_net24))),
                "inv_accrual_h": int(_d_acc.get("inv_accrual_h", 0)),
                "tx_out_h": int(_d_acc.get("tx_out_h", 0)),
                "tx_in_h": int(_d_acc.get("tx_in_h", 0)),
                "accrual_op_h": int(_d_acc.get("accrual_op_h", round(d_net24))),
            },
            "employment": {
                "working": wrk, "effective_working": eff_wrk, "idle": tot - eff_wrk,
                "docked_watch": 0,
                "total": tot, "pct": div_emp_pct, "raw_pct": raw_emp_pct, "status": emp_sev,
            },
            "hulls": {
                "mode": hull_mode, "pct": hull_pct, "eligible_p10": elig_p10,
                "upgraded_eligible": upg_elig, "missing_eligible": missing_elig,
                "t0_missing": t0_missing_div, "t1_plus": hd["t1_plus"], "t2_plus": hd["t2_plus"],
                "max_piloting": hd["max_piloting"], "avg_piloting": avg_pil, "near_p10": hd["near_p10"],
                "empires": hd["empires"], "label": hull_label, "status": hull_sev,
            },
            "modules": {
                "fitted_slots": md["fitted_slots"], "max_slots": md["max_slots"],
                "empty_slots": div_empty_slots, "slot_pct": slot_pct,
                "t2_mod_ships": md["t2_mod_ships"], "ships_missing_t2_mod": div_missing_t2_mod,
                "t2_mod_pct": t2_mod_pct, "off_role_ships": md["off_role_ships"], "status": mod_sev,
            },
            "saturation": div_sat,
            "playbook": {
                "max_chapter_pct": pb_pct, "status": pb_sev,
            },
            "role_kpi": role_kpi,
            "health_score": div_health,
            "weights": dict(DIVISION_WEIGHTS),
            "triggers": triggers,
            "triage": div_triage[:8],
            "alarm_count": sum(1 for t in triggers if t["severity"] == "ALARM"),
            "warn_count": sum(1 for t in triggers if t["severity"] == "WARN"),
            "playbooks": [],
        }

    # Dynamically integrate, rank by active posture weight, and self-adjust Strategy-Pinned KPIs into
    # division & enterprise triage queues. Completed KPIs (matched=True), recovered supply chains, and
    # removed strategies automatically drop out of the queues with zero manual edits.
    ent_strategy_triage = []
    try:
        rv_doc = rivals_doc
        if rv_doc is None:
            import rivals as _rv
            rv_doc = _rv.compute_sedcards(repo_root, data_dir, top_n=12, now=now)
        pbs_raw = list((rv_doc or {}).get("strategy_playbooks") or [])
        ranked_pbs = []
        for p in pbs_raw:
            pw_map = p.get("posture_weights") or {}
            base_wt = int(_num(pw_map.get(posture), 70))
            eff = max(1, int(_num(p.get("effort"), 2)))
            rpct = float(_num(p.get("readiness_pct"), 0.0))
            kpis = list(p.get("kpis") or [])
            unmatched = [k for k in kpis if not k.get("matched")]
            if not unmatched or rpct >= 100.0:
                dyn_score = 0
                p_tier = "P3"
            else:
                quick_finish = (rpct >= 70.0)
                gap_ratio = 0.90 if quick_finish else max(0.35, (100.0 - rpct) / 100.0)
                dyn_score = _wsjf_score(base_wt, gap_ratio=gap_ratio, effort=eff, direction="FLAT")
                p_tier = "P1" if (p.get("status_code") == "GAP" or quick_finish or (posture == "WAR_ALERT" and base_wt >= 80)) else "P2"
            p["dynamic_weight"] = dyn_score
            p["active_posture"] = posture
            p["posture_base_weight"] = base_wt
            ranked_pbs.append((dyn_score, p_tier, base_wt, eff, p, unmatched))

        ranked_pbs.sort(key=lambda x: (-x[0], -x[2], str(x[4].get("id") or "")))
        for rank_idx, (dyn_score, p_tier, base_wt, eff, p, unmatched) in enumerate(ranked_pbs, 1):
            p["priority_rank"] = rank_idx
            summary = {
                "id": p.get("id", ""),
                "name": p.get("name", ""),
                "short_name": p.get("short_name") or p.get("name", ""),
                "status_code": p.get("status_code", "PARTIAL"),
                "readiness_pct": p.get("readiness_pct", 0.0),
                "matched_count": p.get("matched_count", 0),
                "total_count": p.get("total_count", 4),
                "empires": [e.get("name", "") for e in (p.get("empires") or [])],
                "blocker": p.get("blocker", ""),
                "dynamic_weight": dyn_score,
                "priority_rank": rank_idx,
                "posture": posture,
            }
            for dv in (p.get("divisions") or []):
                if dv in divisions_out:
                    divisions_out[dv]["playbooks"].append(summary)
            # Emit weighted triage items ONLY for unmatched KPIs (completed KPIs auto-drop!)
            if unmatched and dyn_score > 0:
                top_k = unmatched[0]
                ent_strategy_triage.append({
                    "severity": "WARN" if p_tier == "P1" else "OK",
                    "tier": p_tier, "weight": base_wt, "effort": eff, "score": dyn_score,
                    "source": "STRATEGY", "code": f"STRAT_{p.get('id', 'x')}",
                    "metric": f"Strategy #{rank_idx} {p.get('short_name') or p.get('name')}: {top_k.get('name')}",
                    "actual": f"{p.get('matched_count', 0)}/{p.get('total_count', 4)} KPIs ({top_k.get('owner')}: {top_k.get('current')})",
                    "target": str(top_k.get("target") or "matched"), "direction": "FLAT",
                    "action": str(p.get("how_to_copy") or p.get("blocker") or "")[:115],
                })
                emitted_owners = set()
                # Anti-metric-fatigue: emit at most ONE primary blocker per strategy per owner division (supply emergencies first)
                ordered_unmatched = sorted(unmatched, key=lambda x: (0 if str(x.get("source") or "") == "read.db:supply" else 1))
                for k in ordered_unmatched:
                    owner = str(k.get("owner") or "")
                    if owner not in divisions_out or owner in emitted_owners:
                        continue
                    emitted_owners.add(owner)
                    t_list = divisions_out[owner]["triage"]
                    code = f"STRAT_{p.get('id', 'x')}_{owner.lower()}"
                    if any(x.get("code") == code for x in t_list):
                        continue
                    is_sup = str(k.get("source") or "") == "read.db:supply"
                    _o_emp = divisions_out[owner]["employment"]
                    _o_busy = (_o_emp["pct"] >= 85.0 and _o_emp["idle"] < 5)
                    _o_needs_cash = (owner == "Trade" and divisions_out[owner]["accounting_24h"]["recurring_cash_h"] <= 0)
                    _is_optional = (not is_sup) and _o_busy and (not _o_needs_cash) and (posture != "WAR_ALERT" or base_wt < 80)
                    t_list.append({
                        "severity": "OK" if _is_optional else ("WARN" if (p_tier == "P1" or is_sup) else "OK"),
                        "tier": "P3" if _is_optional else ("P1" if is_sup else p_tier),
                        "weight": min(40, base_wt) if _is_optional else min(95, base_wt + (8 if is_sup else 0)),
                        "effort": 1 if is_sup else eff,
                        "score": min(35, dyn_score) if _is_optional else min(100, dyn_score + (6 if is_sup else 0)),
                        "source": "MENU" if _is_optional else ("SUPPLY" if is_sup else "STRATEGY"),
                        "optional": _is_optional,
                        "code": code,
                        "metric": f"{'Optional Playbook' if _is_optional else 'Strategy'} ({p.get('short_name') or p.get('name')}): {k.get('name')}",
                        "actual": f"{k.get('current')} (vs {k.get('target')}; {p.get('matched_count', 0)}/{p.get('total_count', 4)} matched)",
                        "target": str(k.get("target") or "matched"), "direction": "FLAT",
                        "action": str(p.get("how_to_copy") or p.get("blocker") or "")[:115],
                    })
        # Re-rank strategy_playbooks in rv_doc + re-sort every division's playbooks & triage queue by live weight
        if isinstance(rv_doc, dict) and ranked_pbs:
            rv_doc["strategy_playbooks"] = [x[4] for x in ranked_pbs]
        for dv_obj in divisions_out.values():
            dv_obj["playbooks"].sort(key=lambda x: (-x.get("dynamic_weight", 0), x.get("priority_rank", 99)))
            dv_obj["triage"].sort(key=_triage_sort_key)
            dv_obj["triage"] = dv_obj["triage"][:10]
    except Exception:
        pass

    # -----------------------------------------------------------------------
    # 4. Stagnation & Momentum Verdict (5-Pillar Synthesis)
    # -----------------------------------------------------------------------
    advancing = []
    drags = []
    if recurring_cash_24h > 0 or cf_dir_24h == "IMPROVING":
        advancing.append("recurring cashflow")
    elif has_accrual_24h and accrual_op_24h > 0:
        advancing.append(f"IAS2 accrual {_fmt_cr(accrual_op_24h)}/h")
        drags.append(f"recurring cash {_fmt_cr(recurring_cash_24h)}/h (cash conversion drag; IAS2 accrual {_fmt_cr(accrual_op_24h)}/h)")
    else:
        drags.append(f"recurring cash {_fmt_cr(recurring_cash_24h)}/h ({cf_dir_24h} 24h)")
    if (wd_deltas["money_delta"] is not None and wd_deltas["money_delta"] > 0) or all_in_24h > 0:
        advancing.append(f"purse ({_fmt_cr(wd_deltas['money_delta'] or all_in_24h)})")
    else:
        drags.append("purse flat/falling")
    if (wd_deltas["p10_delta"] or 0) > 0 or (wd_deltas["t2_delta"] or 0) > 0:
        advancing.append(f"Piloting P10+ (+{wd_deltas['p10_delta'] or 0} in {wd_deltas['dt_h']:.0f}h)")
    else:
        drags.append("P10+/T2 progression flat")
    if roadmap_avg > 0 and (any(n["pct"] >= 80.0 for n in needs_open) or ms_done > 0):
        advancing.append(f"roadmap {roadmap_avg:.1f}% ({ms_done}/{ms_tot} milestones)")
    else:
        drags.append("milestone velocity stalled")
    if prod_pct >= 80.0 and eff_emp_pct >= 90.0:
        advancing.append(f"efficiency {prod_pct:.0f}%")
    else:
        drags.append(f"efficiency {prod_pct:.0f}% / idle {total_idle}")

    ent_alarms = sum(1 for t in ent_triggers if t["severity"] == "ALARM")
    if recurring_cash_24h > 0 and len(advancing) >= 3 and ent_alarms == 0:
        verdict = "COMPOUNDING"
    elif (recurring_cash_24h <= 0 and (not has_accrual_24h or accrual_op_24h <= 0) and cf_dir_24h == "WORSENING" and (wd_deltas["p10_delta"] or 0) <= 0 and (wd_deltas["money_delta"] or 0) <= 0):
        verdict = "STAGNATING"
    elif (cf_dir_24h == "WORSENING" and cf_dir_6h == "WORSENING" and len(advancing) <= 2):
        verdict = "SLOWING"
    else:
        verdict = "GROWING_WITH_DRAG"

    # Dynamic Context-Adaptive Enterprise Readiness Score (0..100)
    # Liquidity (65% matched recurring cash) + Accrual Profitability (35% IAS 2 accrual op when available)
    _liq_sub = 100.0 if recurring_cash_24h > 0 else (65.0 if (cf_dir_24h == "IMPROVING" or steady_1h > 0) else max(0.0, 50.0 + recurring_cash_24h / 2000.0))
    if has_accrual_24h:
        _acc_sub = 100.0 if accrual_op_24h > 0 else max(0.0, 50.0 + accrual_op_24h / 2000.0)
        _cf_sub = 0.65 * _liq_sub + 0.35 * _acc_sub
    else:
        _cf_sub = _liq_sub
    _cf_eff_score = 0.55 * _cf_sub + 0.45 * min(100.0, prod_pct)
    _upg_ent_score = 0.60 * min(100.0, fleet_hull_elig_pct) + 0.40 * min(100.0, fleet_slot_pct)
    _seat_req_score = max(0.0, min(100.0, seat_cap_pct) - open_reqs * 6.0)
    _mil_h = divisions_out.get("Military", {}).get("health_score", 50.0)
    _int_h = divisions_out.get("Intel", {}).get("health_score", 50.0)
    _log_c = _num(divisions_out.get("Logistics", {}).get("role_kpi", {}).get("pct", 50.0))
    _war_readiness = round(0.55 * _mil_h + 0.25 * _int_h + 0.20 * _log_c, 1)
    _subs = {
        "war_readiness": _war_readiness,
        "cashflow_eff": _cf_eff_score,
        "employment": min(100.0, eff_emp_pct),
        "upgrades": _upg_ent_score,
        "roadmap": min(100.0, roadmap_avg),
        "seating_reqs": _seat_req_score,
    }
    ent_weighted_score = round(
        sum((wt / 100.0) * _subs.get(k, 0.0) for k, wt in active_ent_weights.items()),
        1,
    )

    # Enterprise Unified Triage Queue (KPIs + Open Requests + top P1 quick-finish Need + top H1 Roadmap rung)
    ent_triage = [dict(x) for x in ent_triggers]
    ent_seen = {x["code"] for x in ent_triage}
    if diplo_pending > 0 and "DIPLO_PENDING" not in ent_seen:
        ent_seen.add("DIPLO_PENDING")
        _ep_lbl = (" [" + ", ".join(diplo_pending_tags[:4]) + "]") if diplo_pending_tags else ""
        ent_triage.append({
            "severity": "WARN", "tier": "P0", "weight": 90, "effort": 1,
            "score": _wsjf_score(90, gap_ratio=0.8, effort=1, direction="FLAT"),
            "source": "KPI", "code": "DIPLO_PENDING", "metric": "Unanswered Partner Comms",
            "actual": f"{diplo_pending} inbound reply(ies) pending{_ep_lbl}", "target": "0 unanswered", "direction": "FLAT",
            "action": "Check diplomacy.py threads & reply via Prime Directive / scout envoy (F4/O10)",
        })
    for req in open_req_items[:3]:
        rc = f"REQ_{req['ent']}"
        if rc not in ent_seen:
            ent_seen.add(rc)
            rt = "P0" if open_reqs >= 3 else "P1"
            rw = 88 if rt == "P0" else 78
            ent_triage.append({
                "severity": "ALARM" if rt == "P0" else "WARN", "tier": rt, "weight": rw, "effort": 1,
                "score": _wsjf_score(rw, gap_ratio=0.75, effort=1, direction="FLAT"),
                "source": "REQ", "code": rc, "metric": f"Request {req['ent']} ({req['sender']}->{req['to']})",
                "actual": req["need"], "target": "answered", "direction": "FLAT",
                "action": f"Answer {req['ent']} before next Admiral wave (F16)",
            })
    for nd in [n for n in needs_open if n["priority"] == 1][:2]:
        nc = f"NEED_{nd['id']}"
        if nc not in ent_seen:
            ent_seen.add(nc)
            quick = nd["pct"] >= 80.0
            eff = 1 if quick else 2
            nw = 86 if quick else 76
            ent_triage.append({
                "severity": "WARN", "tier": "P1", "weight": nw, "effort": eff,
                "score": _wsjf_score(nw, gap_ratio=(0.90 if quick else (100.0 - nd["pct"]) / 100.0), effort=eff, direction="FLAT"),
                "source": "NEED", "code": nc, "metric": f"P1 Need: {nd['id']} ({nd['division'] or 'fleet'})",
                "actual": f"{nd['pct']:.1f}% stocked" + (f" (short: {nd['short'][:44]})" if nd["short"] else ""),
                "target": "100% stocked", "direction": "FLAT",
                "action": f"Finish final {100.0 - nd['pct']:.1f}% to unlock milestone (WSJF quick-finish)" if quick else f"Supply short inputs for {nd['id']}",
            })
    if isinstance(prog, dict):
        h1_rungs = [rg for rg in (prog.get("rungs") or []) if _num(rg.get("pct")) < 100.0 and "Days" in str(rg.get("horizon") or "")]
        if h1_rungs:
            h1_rungs.sort(key=lambda r: -_num(r.get("pct")))
            rg = h1_rungs[0]
            rc = f"RUNG_{rg.get('id')}"
            if rc not in ent_seen:
                rpct = _num(rg.get("pct"))
                quick = rpct >= 75.0
                eff = 1 if quick else 2
                rw = 82 if quick else 72
                ent_triage.append({
                    "severity": "WARN", "tier": "P1", "weight": rw, "effort": eff,
                    "score": _wsjf_score(rw, gap_ratio=(0.85 if quick else (100.0 - rpct) / 100.0), effort=eff, direction="FLAT"),
                    "source": "ROADMAP", "code": rc,
                    "metric": f"Roadmap H1: {str(rg.get('title') or rg.get('id'))[:42]}",
                    "actual": f"{rpct:.1f}%", "target": "100%", "direction": "FLAT",
                    "action": str(rg.get("bottleneck") or "Advance H1 milestone")[:96],
                })
    for st_item in ent_strategy_triage[:2]:
        if st_item["code"] not in ent_seen:
            ent_seen.add(st_item["code"])
            ent_triage.append(st_item)
    ent_triage.sort(key=_triage_sort_key)

    return {
        "at": int(now),
        "fleet_at": fleet_ts,
        "target_pct": TARGET_COMPLETION_PCT,
        "enterprise": {
            "verdict": verdict,
            "advancing": advancing,
            "drags": drags,
            "cashflow_sign": cf_sign,
            "cashflow_trend_24h": cf_dir_24h,
            "cashflow_trend_6h": cf_dir_6h,
            "steady_1h": steady_1h,
            "steady_6h": steady_6h,
            "steady_24h": steady_24h,
            "purse_24h": int(acc_24["purse_h"]) if isinstance(acc_24, dict) else int(round(all_in_24h or 0)),
            "recurring_cash_24h": recurring_cash_24h,
            "once_direct_24h": once_direct_24h,
            "inventory_accrual_24h": inv_accrual_24h,
            "accrual_operating_24h": accrual_op_24h,
            "recurring_cash_6h": recurring_cash_6h,
            "inventory_accrual_6h": inv_accrual_6h,
            "accrual_operating_6h": accrual_op_6h,
            "has_inventory_accrual": has_accrual_24h,
            "seed_net_24h": int(acc_24["seed_net_h"]) if isinstance(acc_24, dict) else 0,
            "capex_net_24h": int(acc_24["capex_net_h"]) if isinstance(acc_24, dict) else 0,
            "steady_prev_24h": steady_prev_24h,
            "all_in_24h": all_in_24h,
            "purse_now": purse_now,
            "purse_delta_6h": wd_deltas["money_delta"],
            "dt_h": wd_deltas["dt_h"],
            "productive_pct": prod_pct,
            "jump_loop_pct": jump_pct,
            "jump_loop_burn_24h": round(fuel_sinks["jump_net"], 0),
            "employment_pct": emp_pct,
            "effective_employment_pct": eff_emp_pct,
            "working_ships": total_working,
            "idle_ships": total_idle,
            "total_ships": total_ships,
            "seated_ships": fac_members,
            "seat_cap": fac_limit,
            "open_seats": open_seats,
            "seat_cap_pct": seat_cap_pct,
            "seat_fleet_pct": seat_fleet_pct,
            "eligible_p10": fleet_elig_p10,
            "upgraded_eligible": fleet_upg_elig,
            "hull_eligible_pct": fleet_hull_elig_pct,
            "p10_delta_6h": wd_deltas["p10_delta"],
            "t2_hulls": fleet_t2_plus,
            "t2_delta_6h": wd_deltas["t2_delta"],
            "slot_fit_pct": fleet_slot_pct,
            "off_role_ships": fleet_off_role,
            "roadmap_avg_pct": roadmap_avg,
            "milestones_done": ms_done,
            "milestones_total": ms_tot,
            "latest_milestone": latest_ms,
            "open_requests": open_reqs,
            "neutral_partners": neutral_cnt,
            "diplo_pending": diplo_pending,
            "posture": posture,
            "war": war_state,
            "war_readiness": _war_readiness,
            "weighted_score": ent_weighted_score,
            "weights": active_ent_weights,
            "triggers": ent_triggers,
            "triage": ent_triage[:10],
            "idle_ships": total_idle,
            "unseated_ships": unseated_ships,
            "open_seats": open_seats,
            "hulls_missing_t2": fleet_hulls_missing_t2,
            "t0_hulls_missing": fleet_t0_missing,
            "empty_slots": fleet_empty_slots,
            "off_role_ships": fleet_off_role,
            "saturation": field_sat,
            "alarm_count": ent_alarms,
            "warn_count": sum(1 for t in ent_triggers if t["severity"] == "WARN"),
        },
        "divisions": divisions_out,
    }


def render_briefing(sc, who="all"):
    """Render compact, actionable startup scorecard lines for hive.py briefing (anti-alert-fatigue)."""
    e = sc["enterprise"]
    lines = ["=== KPI SCORECARD & ALERT TRIGGERS (<80% TARGETS & STAGNATION)"]
    p_delta = f" | 6h purse {_fmt_cr(e['purse_delta_6h'])}" if e["purse_delta_6h"] is not None else ""
    p10_d = f" (+{e['p10_delta_6h']} P10+)" if (e["p10_delta_6h"] or 0) > 0 else ""
    lines.append(
        f"  ENTERPRISE | {e['verdict']} | Posture {e.get('posture','CASHFLOW_RECOVERY')} | Score {e['weighted_score']:.1f}/100 | recurring cash {e['cashflow_sign']} "
        f"({_fmt_cr(e.get('recurring_cash_24h', e['steady_24h']))}/h 24h, {_fmt_cr(e.get('recurring_cash_6h', e['steady_6h']))}/h 6h, 24h {e['cashflow_trend_24h']}, 6h {e['cashflow_trend_6h']}){p_delta}"
    )
    if e.get("has_inventory_accrual") or e.get("once_direct_24h"):
        lines.append(
            f"  GAAP P&L   | Purse Net {_fmt_cr(e.get('purse_24h', 0))}/h | Recurring {_fmt_cr(e.get('recurring_cash_24h', e['steady_24h']))}/h "
            f"(excl {_fmt_cr(e.get('once_direct_24h', 0))}/h once-fuel) + IAS2 Inv {_fmt_cr(e.get('inventory_accrual_24h', 0))}/h = "
            f"Accrual Op {_fmt_cr(e.get('accrual_operating_24h', 0))}/h | Seed {_fmt_cr(e.get('seed_net_24h', 0))}/h | CapEx {_fmt_cr(e.get('capex_net_24h', 0))}/h"
        )
    _sat_m = (e.get("saturation") or {}).get("Mining") or {}
    _sat_t = (e.get("saturation") or {}).get("Trade") or {}
    _sat_bits = []
    if _sat_m.get("active_depleting"):
        _sat_bits.append(f"mining {_sat_m['distinct_pois']} belts (max {_sat_m['max_per_poi']}/belt)")
    if _sat_t.get("total_policed_hubs") or _sat_t.get("active_depleting"):
        _sat_bits.append(f"trade hubs {_sat_t.get('covered_hubs',0)}/{_sat_t.get('total_policed_hubs',0)} (max {_sat_t.get('max_per_poi',0)}/hub)")
    _sat_s = (" | spread: " + ", ".join(_sat_bits)) if _sat_bits else ""
    lines.append(
        f"  GAPS->0    | idle {e.get('idle_ships', e['total_ships'] - e['working_ships'])} ({e['effective_employment_pct']:.1f}% work) | "
        f"unseated {e.get('unseated_ships', max(0, e['total_ships'] - e['seated_ships']))} ({e.get('open_seats', 0)} open in cap {e['seat_cap']}, {e['seat_fleet_pct']:.1f}% fleet) | "
        f"hulls {e.get('hulls_missing_t2', max(0, e['eligible_p10'] - e['upgraded_eligible']))} P10+ missing T2+ ({e.get('t0_hulls_missing', 0)} T0 left){p10_d} | "
        f"slots {e.get('empty_slots', 0)} empty ({e['slot_fit_pct']:.1f}% fit, {e.get('off_role_ships', 0)} off-role) | "
        f"eff {e['productive_pct']:.1f}% | roadmap {e['roadmap_avg_pct']:.1f}%{_sat_s}"
    )
    if e["drags"]:
        lines.append("  BOTTLENECKS| " + "; ".join(e["drags"][:4]))

    target_div = None
    if who and str(who).lower() not in ("all", "unity", "command"):
        target_div = MEMBER_TO_DIV.get(str(who).lower())

    if target_div and target_div in sc["divisions"]:
        d = sc["divisions"][target_div]
        da = d.get("accounting_24h") or {}
        d_purse = da.get("purse_h", d.get("purse_24h", d["cashflow_24h"]))
        d_recur = da.get("recurring_cash_h", d["cashflow_24h"])
        d_accop = da.get("accrual_op_h", d_recur)
        _rc_s = (d.get("responsibility_center") or {}).get("short") or "Center"
        lines.append(
            f"  MY DIVISION ({d['division']} / {d['admiral']}) [{_rc_s}] | Score {d['health_score']:.1f}/100 | state={d['status']} ({d['trend_24h']}) | "
            f"24h Purse {_fmt_cr(d_purse)}/h | Recur {_fmt_cr(d_recur)}/h | Accrual {_fmt_cr(d_accop)}/h"
        )
        _dsat = d.get("saturation") or {}
        if d["division"] == "Trade" and (_dsat.get("total_policed_hubs") or _dsat.get("active_depleting")):
            _dsat_s = f" | hubs {_dsat.get('covered_hubs',0)}/{_dsat.get('total_policed_hubs',0)} covered (max {_dsat.get('max_per_poi',0)}/hub [{_dsat.get('status','OK')}])"
        elif _dsat.get("active_depleting"):
            _dsat_s = f" | spread {_dsat['distinct_pois']} POIs (max {_dsat['max_per_poi']}/POI [{_dsat['status']}])"
        else:
            _dsat_s = ""
        lines.append(
            f"    Gaps->0  : idle {d['employment']['idle']} ({d['employment']['pct']:.1f}% work) | "
            f"hulls {d['hulls']['label']} | "
            f"slots {d['modules'].get('empty_slots', d['modules']['max_slots'] - d['modules']['fitted_slots'])} empty "
            f"({d['modules']['slot_pct']:.1f}% fit, {d['modules'].get('ships_missing_t2_mod', 0)} ships missing T2+, {d['modules']['off_role_ships']} off-role) | "
            f"playbook {d['playbook']['max_chapter_pct']:.0f}%{_dsat_s}"
        )
        lines.append(f"    Role KPI : {d['role_kpi']['name']} = {d['role_kpi']['value']} [{d['role_kpi']['status']}]")
        if da:
            lines.append(
                f"    Finance  : Purse {_fmt_cr(d_purse)}/h (Recur {_fmt_cr(d_recur)} + Once {_fmt_cr(da.get('once_net_h', 0))}) | "
                f"Inv {_fmt_cr(da.get('inv_accrual_h', 0))}/h | Xfer out {_fmt_cr(da.get('tx_out_h', 0))} / in {_fmt_cr(-da.get('tx_in_h', 0))} -> Accrual {_fmt_cr(d_accop)}/h"
            )
        if d.get("playbooks"):
            pb_s = " | ".join(f"{p['short_name']} {p['matched_count']}/{p['total_count']} ({p['readiness_pct']:.0f}% {p['status_code']})" for p in d["playbooks"][:4])
            lines.append(f"    Playbooks: {pb_s}")
        q_div = d.get("triage") or d.get("triggers") or []
        if q_div:
            lines.append("  ACTIVE TRIGGERS & WEIGHTED TRIAGE QUEUE (strict order: P0>P1>P2>P3; score=MAUTxWSJF):")
            for i, t in enumerate(q_div[:6], 1):
                lines.append(f"    #{i} [{t.get('tier','P2')} {int(t.get('score',0)):3d}|{t.get('source','KPI'):7s}|{t['severity']:5s}] {t['metric']}: {t['actual']} -> {t['action']}")
        else:
            lines.append("  ACTIVE TRIGGERS: none (all division KPIs >=80% target)")
    else:
        # Unity / fleetwide view: compact 6-division scorecard table + top fleet alarms
        lines.append("  DIVISIONS  | Division   Score  State  Idle  HullGap  EmptySl  Purse/h   Recur/h  Accrual/h  Role KPI")
        for div in DIVISIONS:
            d = sc["divisions"][div]
            da = d.get("accounting_24h") or {}
            h_gap = (f"{d['hulls'].get('missing_eligible', 0):3d} T2" if d["hulls"]["mode"] == "eligible_t2"
                     else f"P{d['hulls']['max_piloting']:<2d}->T2")
            e_sl = d["modules"].get("empty_slots", d["modules"]["max_slots"] - d["modules"]["fitted_slots"])
            lines.append(
                f"             | {div:10s} {d['health_score']:5.1f}  {d['status']:5s}  {d['employment']['idle']:4d}  {h_gap:>7s}  "
                f"{e_sl:7d}  "
                f"{_fmt_cr(da.get('purse_h', d.get('purse_24h', d['cashflow_24h']))):>8s}  "
                f"{_fmt_cr(da.get('recurring_cash_h', d['cashflow_24h'])):>8s}  "
                f"{_fmt_cr(da.get('accrual_op_h', d['cashflow_24h'])):>9s}  {d['role_kpi']['value'][:44]}"
            )
        lines.append("             (* = 0 P10+ pilots yet; % shows avg Piloting progress toward T2 unlock)")
        q_ent = e.get("triage") or e.get("triggers") or []
        if q_ent:
            lines.append("  TOP FLEET TRIGGERS & WEIGHTED TRIAGE QUEUE (strict P0>P1>P2>P3; score=MAUTxWSJF):")
            for i, t in enumerate(q_ent[:6], 1):
                lines.append(f"    #{i} [{t.get('tier','P2')} {int(t.get('score',0)):3d}|{t.get('source','KPI'):7s}|{t['severity']:5s}] {t['metric']}: {t['actual']} -> {t['action']}")
    return "\n".join(lines)


def briefing(root, data, now, who="all", rivals_doc=None):
    """Print startup scorecard block safely (never aborts briefing on transient read errors)."""
    try:
        sc = compute_scorecard(
            repo_root=Path(root).resolve().parent if Path(root).name == "game" else root,
            data_dir=data, now=now, rivals_doc=rivals_doc,
        )
        print(render_briefing(sc, who=who))
    except Exception as err:
        print(f"=== KPI SCORECARD: unavailable ({type(err).__name__}: {err})")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Compute Division KPI Scorecards, <80% Triggers & Stagnation Verdict.")
    ap.add_argument("--who", default="all", help="Member or division name (default: all)")
    ap.add_argument("--data", default=os.environ.get("COLLECTIVE_DATA", DATA_DEFAULT))
    ap.add_argument("--root", default=REPO_DEFAULT)
    ap.add_argument("--json", action="store_true", help="Emit structured JSON payload")
    args = ap.parse_args(argv)
    sc = compute_scorecard(repo_root=args.root, data_dir=args.data)
    if args.json:
        print(json.dumps(sc, indent=2))
    else:
        print(render_briefing(sc, who=args.who))
    return 0


if __name__ == "__main__":
    sys.exit(main())

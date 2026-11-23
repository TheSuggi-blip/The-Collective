#!/usr/bin/env python3
"""Read-only view of player-to-player trade & contract opportunities across all 4 channels.

Inspects:
  1. CLTV open bottleneck needs (need_status) for Station Bursar buy orders (Ch1)
     and Faction Notice Board delivery jobs (Ch2).
  2. Live station mission boards (missions table) highlighting open supply/delivery
     contracts posted by Neutral diplomatic partners ([HEXC], [IRLC]) or NPCs.
  3. Recent bilateral / Bursar ledger entries from communications/contracts.log.

Read-only. Pure stdlib.

Usage:
  python3 -I -B game/fleet/contracts.py [--limit 20]
"""
import argparse
import json
import os
import re
import sqlite3
import sys
from pathlib import Path

DATA_DEFAULT = "/srv/collective/data"
REPO_DEFAULT = "/srv/collective/the-collective"
CONTRACT_HINTS = (
    "supply", "delivery", "deliver", "procurement", "shipyard", "haul",
    "freight", "requisition", "contract", "ore", "alloy", "plate", "fuel",
    "outpost", "station", "material", "component",
)


def _load_neutral_tags(data_dir):
    tags = {}
    p = Path(data_dir) / "fleet" / "diplomacy.json"
    if not p.is_file():
        return tags
    try:
        doc = json.loads(p.read_text(encoding="utf-8"))
        for tag, rec in (doc.get("factions") or {}).items():
            st = (rec.get("status") or "").lower()
            if st in ("neutrality_agreed", "trade_active", "info_sharing_active"):
                tags[tag.upper()] = {
                    "name": rec.get("name") or tag,
                    "status": st,
                }
    except Exception:
        pass
    return tags


def _connect_ro(data_dir):
    db = Path(data_dir) / "store" / "read.db"
    if not db.is_file():
        return None
    conn = sqlite3.connect(f"file:{db}?mode=ro", uri=True, timeout=3.0)
    conn.row_factory = sqlite3.Row
    return conn


def _fmt_num(n):
    try:
        return f"{int(round(float(n))):,}"
    except Exception:
        return "0"


def show(data_dir=DATA_DEFAULT, repo_root=REPO_DEFAULT, limit=20):
    neutral = _load_neutral_tags(data_dir)
    conn = _connect_ro(data_dir)
    print("P2P TRADE & CONTRACT OPPORTUNITIES (4-Channel View, F39)")
    if neutral:
        plist = ", ".join(f"[{t}] ({v['name']})" for t, v in sorted(neutral.items()))
        print(f"Neutral P2P partners: {plist}")
    else:
        print("Neutral P2P partners: none yet")

    print("\n=== 1. CLTV BOTTLENECK PROCUREMENT CANDIDATES (Ch1 Bursars & Ch2 Faction Notice Board)")
    print("  Owner: Mercury runs Exchange buy/sell books; Unity posts Faction Notice Board contracts; log all deals in contracts.log (F39).")
    if conn is not None:
        tables = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type IN ('table','view')")}
        if "need_status" in tables:
            rows = conn.execute("""
                SELECT id, priority, project, division, ref, units, covered, short_items, buy, fee
                FROM need_status
                WHERE COALESCE(covered, 0) < 100
                ORDER BY priority ASC, covered DESC
                LIMIT 12
            """).fetchall()
            if rows:
                for r in rows:
                    short = (r["buy"] or r["short_items"] or "").strip()
                    if len(short) > 105:
                        short = short[:102] + "..."
                    fee_txt = f" | fee={_fmt_num(r['fee'])} cr" if r["fee"] else ""
                    print(f"  P{r['priority']} {r['id']:26s} {float(r['covered'] or 0):5.1f}% | {r['division'] or 'fleet':9s} | {short or 'ready'}{fee_txt}")
            else:
                print("  (all open needs covered)")

        print("\n=== 2. LIVE MISSION & SUPPLY CONTRACTS ON STATION BOARDS (Ch2 Partner & NPC Supply)")
        if "missions" in tables:
            cols = {r[1] for r in conn.execute("PRAGMA table_info(missions)").fetchall()}
            reward_col = "reward" if "reward" in cols else ("credits" if "credits" in cols else "0")
            title_col = "title" if "title" in cols else "id"
            issuer_col = "issuer" if "issuer" in cols else ("faction" if "faction" in cols else "''")
            place_col = "base" if "base" in cols else ("place" if "place" in cols else "system")
            mrows = conn.execute(f"""
                SELECT {place_col} AS place, {title_col} AS title, {issuer_col} AS issuer,
                       {reward_col} AS reward, COUNT(*) AS copies
                FROM missions
                GROUP BY 1, 2, 3, 4
                ORDER BY copies DESC, reward DESC
                LIMIT 250
            """).fetchall()
            partner_hits = []
            supply_hits = []
            for r in mrows:
                title = str(r["title"] or "")
                issuer = str(r["issuer"] or "")
                low = (title + " " + issuer).lower()
                matched_tag = None
                for tag, info in neutral.items():
                    if f"[{tag.lower()}]" in low or info["name"].lower() in low or tag.lower() == issuer.lower():
                        matched_tag = tag
                        break
                rec = (matched_tag, str(r["place"] or "?"), title, issuer, r["reward"] or 0, r["copies"] or 1)
                if matched_tag:
                    partner_hits.append(rec)
                elif any(h in low for h in CONTRACT_HINTS):
                    supply_hits.append(rec)
            if partner_hits:
                print("  [NEUTRAL PARTNER CONTRACTS -- PRIORITY FILL]")
                for tag, place, title, issuer, rew, copies in partner_hits[:limit]:
                    print(f"  [PARTNER:{tag}] {place:28s} | {copies:2d}x | {_fmt_num(rew):>9s} cr | {title} ({issuer})")
            else:
                print("  (no Neutral partner faction-posted contracts currently visible on scanned station boards)")
            if supply_hits:
                print("  [TOP SUPPLY / DELIVERY / PROCUREMENT BOARD CONTRACTS]")
                for _, place, title, issuer, rew, copies in supply_hits[:limit]:
                    print(f"  {place:32s} | {copies:2d}x | {_fmt_num(rew):>9s} cr | {title}")
        conn.close()
    else:
        print("  (read.db unavailable)")

    print("\n=== 3. RECENT CONTRACTS.LOG LEDGER (Ch1-Ch4 Bursars & Bilateral Deals)")
    clog = Path(repo_root) / "communications" / "contracts.log"
    if clog.is_file():
        text = clog.read_text(encoding="utf-8", errors="replace")
        entries = re.findall(r"(## \[ENT-\d+\][^\n]*(?:\n(?!## \[ENT-).*)*)", text)
        if entries:
            for e in entries[-6:]:
                first = e.splitlines()[0]
                partner = ""
                for ln in e.splitlines()[1:6]:
                    if ln.lower().startswith(("partner:", "channel:", "status:", "item:", "escrow:")):
                        partner += " | " + ln.strip()
                print(f"  {first}{partner[:140]}")
        else:
            print("  (no entries logged yet in communications/contracts.log)")
    else:
        print("  (communications/contracts.log missing)")
    print("\n=== 4. FREIGHT / COURIER BOARD (Ch3) & ATOMIC SWAPS (Ch4)")
    print("  Ch3 Freight: python3 -I -B game/fleet/shipping.py list --limit 25  (Apollo owns freight contracts)")
    print("  Ch4 Swaps:   spacemolt_transfer trade_offer / trade_accept at mutual POI (Unity/Mercury; never one-way gifts)")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="Inspect P2P trade & contract opportunities across all 4 SpaceMolt channels.")
    ap.add_argument("--data", default=os.environ.get("COLLECTIVE_DATA", DATA_DEFAULT))
    ap.add_argument("--root", default=REPO_DEFAULT)
    ap.add_argument("--limit", type=int, default=15)
    args = ap.parse_args(argv)
    return show(args.data, args.root, args.limit)


if __name__ == "__main__":
    sys.exit(main())

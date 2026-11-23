#!/usr/bin/env python3
"""contracts.py -- CLTV 4-Channel P2P Trade, Procurement Contracts, Station Bursars & Partner Supply Arbitrage.

WHAT: summarizes four operational views for Unity, Mercury (Trade), and Apollo (Logistics):
        1. CLTV Bottleneck Procurement Candidates (from `need_status` P1/P2 material shorts vs live market
           bids/asks and catalog base values) -- what our Station Bursars or Notice Board should bid for right now.
        2. Partner & High-Reward Board Supply Contracts (`missions` table) -- highlights contracts posted by
           our Neutral (by agreement) partners (`[HEXC]`, `[IRLC]`, etc.) plus top board supply runs.
        3. Recent entries of `communications/contracts.log` (all 4 P2P channels, with optional `partner: [TAG]`).
        4. CLTV P2P 4-Channel Readiness (Station Exchange, Faction Notice Board status, Freight Shipping, Direct Swap).
USAGE:
  python3 -I -B game/fleet/contracts.py [--data /srv/collective/data] [--root /srv/collective/the-collective]
"""

import json
import sqlite3
import sys
from pathlib import Path


def fmt(n):
    return format(int(round(n)), ",")


def _neutral_partner_tags(data):
    """Return set of faction tags currently at neutrality_agreed / trade_active / info_sharing_active."""
    p = Path(data) / "comms" / "diplomacy.json"
    out = set()
    try:
        raw = json.loads(p.read_text(encoding="utf-8"))
        for tag, info in (raw.get("factions") or {}).items():
            if isinstance(info, dict) and info.get("status") in ("neutrality_agreed", "trade_active", "info_sharing_active"):
                out.add(str(tag).upper())
    except (OSError, ValueError):
        pass
    return out


def show(data="/srv/collective/data", root="/srv/collective/the-collective"):
    db_p = Path(data) / "store" / "read.db"
    if not db_p.is_file():
        print("contracts: read.db not found at %s" % db_p)
        return 1
    conn = sqlite3.connect("file:%s?mode=ro" % db_p, uri=True)
    conn.row_factory = sqlite3.Row
    neutral_tags = _neutral_partner_tags(data)
    try:
        print("=== 1. CLTV BOTTLENECK PROCUREMENT CANDIDATES (Station Bursars & Faction Notice Board)")
        print("  Owner: Mercury runs Exchange buy/sell books; Unity posts Faction Notice Board contracts; log all deals in contracts.log (F39).")
        rows = conn.execute("""
            SELECT id, priority, what, project, pct, short_text
            FROM need_status
            WHERE priority <= 2 AND pct < 100
            ORDER BY priority ASC, pct DESC
        """).fetchall()
        short_agg = {}
        for r in rows:
            for part in (r["short_text"] or "").split(","):
                part = part.strip()
                if not part or "fee" in part:
                    continue
                toks = part.split()
                if len(toks) >= 2 and toks[-1].replace(",", "").isdigit():
                    it = toks[0]
                    q = int(toks[-1].replace(",", ""))
                    cur = short_agg.setdefault(it, {"qty": 0, "needs": [], "best_prio": r["priority"]})
                    cur["qty"] += q
                    if r["id"] not in cur["needs"]:
                        cur["needs"].append(r["id"])
                    cur["best_prio"] = min(cur["best_prio"], r["priority"])
        for it, info in sorted(short_agg.items(), key=lambda kv: (kv[1]["best_prio"], -kv[1]["qty"]))[:14]:
            base_r = conn.execute("SELECT base_value FROM items WHERE id=?", (it,)).fetchone()
            bid_r = conn.execute("SELECT MAX(bid) as mb, SUM(bid_qty) as bq FROM books WHERE item=? AND bid>0 AND bid_qty>0", (it,)).fetchone()
            ask_r = conn.execute("SELECT MIN(ask) as ma, SUM(ask_qty) as aq, base FROM books WHERE item=? AND ask>0 AND ask_qty>0", (it,)).fetchone()
            bval = int(base_r[0] or 0) if base_r else 0
            mb = int(bid_r["mb"] or 0) if bid_r else 0
            ma = int(ask_r["ma"] or 0) if ask_r and ask_r["ma"] else 0
            rec_bid = max(mb + max(1, mb // 20), int(bval * 1.5), 5)
            ask_note = ("cheapest ask %s cr x %s @ %s" % (fmt(ma), fmt(ask_r["aq"]), str(ask_r["base"])[:20])) if ma else "no public ask -- post buy bid / contract!"
            print("  P%d %-22s | short %7s | top_bid %5s | rec_bursar_bid ~%5s cr | %s | for: %s"
                  % (info["best_prio"], it[:22], fmt(info["qty"]), fmt(mb), fmt(rec_bid), ask_note, ",".join(info["needs"][:2])))

        print("\n=== 2. NEUTRAL PARTNER & HIGH-REWARD BOARD SUPPLY CONTRACTS (fill via route_run accept-by-title)")
        m_rows = conn.execute("""
            SELECT base, system, COALESCE(giver, '-') as giver, title, reward, objectives
            FROM missions
            WHERE reward >= 15000 AND (
                LOWER(title) LIKE '%supply%' OR LOWER(title) LIKE '%wanted%' OR LOWER(title) LIKE '%bulk%'
                OR LOWER(title) LIKE '%reserve%' OR LOWER(title) LIKE '%hexc%' OR LOWER(title) LIKE '%irlc%'
                OR LOWER(title) LIKE '%ironlight%' OR LOWER(title) LIKE '%hex %'
            )
            ORDER BY reward DESC LIMIT 30
        """).fetchall()
        ranked = []
        for r in m_rows:
            blob = ("%s %s %s" % (r["title"], r["giver"], r["objectives"])).upper()
            ptag = ""
            for t in sorted(neutral_tags):
                if t in blob or (t == "HEXC" and "HEX STAR" in blob) or (t == "IRLC" and "IRONLIGHT" in blob):
                    ptag = t
                    break
            ranked.append((0 if ptag else 1, -int(r["reward"] or 0), ptag, r))
        ranked.sort(key=lambda x: (x[0], x[1]))
        for _prio, _neg, ptag, r in ranked[:14]:
            badge = ("[PARTNER:%-4s] " % ptag) if ptag else "               "
            print("  %s%7s cr | %-22s (%-10s) | %-26s | %s"
                  % (badge, fmt(r["reward"]), str(r["base"])[:22], str(r["system"])[:10], str(r["title"])[:26], str(r["objectives"])[:50]))

        print("\n=== 3. RECENT CLTV CONTRACTS LEDGER (communications/contracts.log)")
        clog = Path(root) / "communications" / "contracts.log"
        if clog.is_file():
            blocks = [b.strip() for b in clog.read_text(encoding="utf-8", errors="replace").split("## [ENT-") if b.strip()]
            for b in blocks[-6:]:
                lines = b.splitlines()
                print("  ENT-" + lines[0][:110])
                for ln in lines[1:3]:
                    print("    " + ln[:115])

        print("\n=== 4. 4-CHANNEL P2P TRADE READINESS (Rule F39)")
        nb_cnt = 0
        try:
            emp = json.loads((Path(data) / "empire" / "empire.json").read_text(encoding="utf-8"))
            for fac in (emp.get("facilities") or []):
                ft = str(fac.get("type") or fac.get("facility_type") or "").lower()
                if any(k in ft for k in ("notice_board", "mission_board", "bounty_office")):
                    nb_cnt += 1
        except (OSError, ValueError):
            pass
        print("  Ch1 Station Exchange Orders : READY (Mercury: create_buy_order / create_sell_order / route_run sell_order; 0 listing fee)")
        print("  Ch2 Faction Mission Board   : %s (accept partner boards: READY via route_run title; post own: Unity post_mission needs Notice Board 50k cr)" % ("BOARD BUILT (%d)" % nb_cnt if nb_cnt else "NO CLTV BOARD YET (Apollo builds Notice Board 50k cr)"))
        print("  Ch3 Freight / Courier Board : READY (Apollo: python3 -I -B game/fleet/shipping.py list | spacemolt_shipping)")
        print("  Ch4 Direct Atomic Swap      : READY (Unity/Mercury: spacemolt_transfer trade_offer/trade_accept at mutual POI; no 1-way gifts)")
        print("  Neutral Partners Active     : %s" % (", ".join("[%s]" % t for t in sorted(neutral_tags)) or "none yet"))
    finally:
        conn.close()
    return 0


def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)
    if any(a in ("-h", "--help") for a in args):
        sys.exit(__doc__)
    data = args[args.index("--data") + 1] if "--data" in args and args.index("--data") + 1 < len(args) else "/srv/collective/data"
    root = args[args.index("--root") + 1] if "--root" in args and args.index("--root") + 1 < len(args) else str(Path(__file__).resolve().parents[2])
    return show(data, root)


if __name__ == "__main__":
    sys.exit(main())

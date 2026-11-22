#!/usr/bin/env python3
"""contracts.py -- CLTV Procurement Contracts, Station Bursar order-book advisor & rival contract arbitrage.

WHAT: gives Mercury (Trade), Apollo (Logistics) and Unity instant visibility without waiting on another turn:
        1. Short Bottleneck Procurement Candidates (`need_status` & `supply_status` shortages joined with live `books`
           bids/asks and catalog base values) -- what our Station Bursars or Notice Board should bid for right now so
           other players deliver scarce inputs (`foil_scale`, `alloy_scale`, `anchor_plate`, `silicon_ore`, etc.) to us
           ([HEXC] reverse-outsourcing pattern).
        2. Rival Supply Contracts Open on Mission Boards (`missions` table) -- high-reward player/faction delivery
           contracts (`HEXC supply contract`, etc.) compared against our vault surplus so Trade can sell into them.
        3. Recent entries of `communications/contracts.log`.
USAGE:
  python3 -I -B game/fleet/contracts.py [--data /srv/collective/data] [--root /srv/collective/the-collective]
"""

import json
import re
import sqlite3
import sys
from pathlib import Path


def fmt(n):
    return format(int(round(n or 0)), ",")


def show(data="/srv/collective/data", root="/srv/collective/the-collective"):
    db_p = Path(data) / "store" / "read.db"
    if not db_p.is_file():
        print("contracts: read.db not found at %s" % db_p)
        return 1
    conn = sqlite3.connect("file:%s?mode=ro" % db_p, uri=True, timeout=3.0)
    conn.row_factory = sqlite3.Row
    try:
        print("=== 1. CLTV BOTTLENECK PROCUREMENT CANDIDATES (for Mercury Station Bursars & Notice Board)")
        print("  Owner: Mercury executes standing buy bids & Notice Board contracts within Unity's orders.log escrow cap; log in communications/contracts.log.")
        needs = conn.execute("SELECT id, priority, division, short_items FROM need_status WHERE COALESCE(short_items, '') != '' ORDER BY priority, rank").fetchall()
        short_agg = {}
        for r in needs:
            for part in str(r["short_items"] or "").split(","):
                m = re.match(r"^\s*([a-z0-9_]+)\s+(\d+)", part.strip())
                if m:
                    it, q = m.group(1), int(m.group(2))
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

        print("\n=== 2. HIGH-REWARD RIVAL & BOARD SUPPLY CONTRACTS (sell surplus into them when above market bid)")
        m_rows = conn.execute("""
            SELECT base, system, COALESCE(giver, '-') as giver, title, reward, objectives
            FROM missions
            WHERE reward >= 20000 AND (LOWER(title) LIKE '%supply%' OR LOWER(title) LIKE '%wanted%' OR LOWER(title) LIKE '%bulk%' OR LOWER(title) LIKE '%reserve%')
            ORDER BY reward DESC LIMIT 12
        """).fetchall()
        for r in m_rows:
            print("  %7s cr | %-22s (%-10s) | %-26s | %s"
                  % (fmt(r["reward"]), str(r["base"])[:22], str(r["system"])[:10], str(r["title"])[:26], str(r["objectives"])[:55]))

        print("\n=== 3. RECENT CLTV CONTRACTS LEDGER (communications/contracts.log)")
        clog = Path(root) / "communications" / "contracts.log"
        if clog.is_file():
            blocks = [b.strip() for b in clog.read_text(encoding="utf-8", errors="replace").split("## [ENT-") if b.strip()]
            for b in blocks[-5:]:
                lines = b.splitlines()
                print("  ENT-" + lines[0][:110])
                for ln in lines[1:3]:
                    print("    " + ln[:115])
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

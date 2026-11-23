#!/usr/bin/env python3
"""Read-only CLI for SpaceMolt's Player-to-Player Freight / Courier board (spacemolt_shipping).

Channel 3 of the Collective's 4-channel P2P trade framework (rule F39, orders O10):
  - list     : galaxy-wide public/invited freight contracts (`list_all`), highlighting
               Neutral partners ([HEXC], [IRLC]) first. Requires a docked pilot at a
               station with a mission-service facility (auto-picked from read.db/fleet.json).
  - active   : active freight contracts as carrier, shipper, recipient, or invited carrier.
  - profile  : carrier trust tier, liability cap, and delivery history for a pilot.
  - track    : track a specific freight contract ID.

Read-only (uses gate.py READ allowlist). Pure stdlib.
Usage:
  python3 -I -B game/fleet/shipping.py list [--pilot NAME] [--limit 25]
  python3 -I -B game/fleet/shipping.py active [--pilot NAME]
  python3 -I -B game/fleet/shipping.py profile [--pilot NAME]
  python3 -I -B game/fleet/shipping.py track <contract_id> [--pilot NAME]
"""
import argparse
import json
import os
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gate

DATA_DEFAULT = "/srv/collective/data"


def load_neutral_tags(data_dir):
    tags = {}
    p = Path(data_dir) / "fleet" / "diplomacy.json"
    if not p.is_file():
        return tags
    try:
        doc = json.loads(p.read_text(encoding="utf-8"))
        for tag, rec in (doc.get("factions") or {}).items():
            st = (rec.get("status") or "").lower()
            if st in ("neutrality_agreed", "trade_active", "info_sharing_active"):
                tags[tag.upper()] = rec.get("name") or tag
    except Exception:
        pass
    return tags


def pick_shipping_pilot(data_dir, prefer_docked=True):
    """Pick a hauler (or fallback ship) for read-only shipping queries.
    When prefer_docked=True, prioritize docked haulers at stations (not outposts if avoidable)."""
    candidates = []
    db = Path(data_dir) / "store" / "read.db"
    if db.is_file():
        try:
            conn = sqlite3.connect(f"file:{db}?mode=ro", uri=True, timeout=2.0)
            rows = conn.execute(
                "SELECT pilot, division, COALESCE(docked,0), COALESCE(base,'') FROM ships ORDER BY pilot"
            ).fetchall()
            conn.close()
            for pilot, div, docked, base in rows:
                if not pilot:
                    continue
                is_hauler = 1 if (div == "Logistics" or str(pilot).startswith("hauler-")) else 0
                is_docked = 1 if (int(docked or 0) == 1 and str(base or "").strip()) else 0
                is_station = 1 if (base and "outpost" not in str(base).lower() and not str(base).startswith("443f")) else 0
                candidates.append((is_docked if prefer_docked else 1, is_station, is_hauler, str(pilot)))
        except Exception:
            pass
    if not candidates:
        fp = Path(data_dir) / "fleet" / "fleet.json"
        if fp.is_file():
            try:
                fj = json.loads(fp.read_text(encoding="utf-8"))
                ships = fj.get("ships") or []
                if isinstance(ships, dict):
                    ships = [{"name": k, **v} for k, v in ships.items()]
                for s in ships:
                    name = s.get("name") or ""
                    if not name:
                        continue
                    is_hauler = 1 if (s.get("division") == "Logistics" or name.startswith("hauler-")) else 0
                    is_docked = 1 if s.get("docked") else 0
                    candidates.append((is_docked if prefer_docked else 1, 1, is_hauler, name))
            except Exception:
                pass
    if not candidates:
        return "hauler-1"
    candidates.sort(key=lambda x: (-x[0], -x[1], -x[2], x[3]))
    return candidates[0][3]


def call_shipping(pilot, action, params=None):
    payload = {"toolGroup": "spacemolt_shipping", "action": action, "params": params or {}}
    code, raw = gate.call("post", f"/accounts/{gate.q(pilot)}/raw", payload, timeout=25)
    try:
        parsed = json.loads(raw) if isinstance(raw, str) else raw
    except Exception:
        parsed = {"raw": raw}
    return code, parsed


def _extract_shipments(body):
    if not isinstance(body, dict):
        return []
    sc = body.get("structuredContent") if isinstance(body.get("structuredContent"), dict) else body
    for key in ("shipments", "contracts", "listings", "results", "items"):
        val = sc.get(key)
        if isinstance(val, list):
            return val
    return []


def format_list(body, neutral_tags, limit=25):
    shipments = _extract_shipments(body)
    lines = [f"FREIGHT BOARD (spacemolt_shipping list_all) | count={len(shipments)} | neutral_partners={','.join(sorted(neutral_tags)) or 'none'}"]
    if not shipments:
        msg = (body.get("result") or body.get("message") or "no open freight contracts") if isinstance(body, dict) else str(body)
        lines.append(f"  {str(msg)[:240]}")
        return "\n".join(lines)

    ranked = []
    for sh in shipments:
        blob = json.dumps(sh, sort_keys=True).lower()
        ptag = None
        for tag, name in neutral_tags.items():
            if f"[{tag.lower()}]" in blob or name.lower() in blob or str(sh.get("shipper_tag") or "").upper() == tag:
                ptag = tag
                break
        reward = float(sh.get("reward") or sh.get("payout") or sh.get("fee") or 0)
        ranked.append((0 if ptag else 1, -reward, ptag, sh))
    ranked.sort(key=lambda x: (x[0], x[1]))

    for _, _, ptag, sh in ranked[:limit]:
        cid = str(sh.get("id") or sh.get("contract_id") or "?")[:14]
        orig = str(sh.get("origin_name") or sh.get("origin") or sh.get("pickup_station") or "?")
        dest = str(sh.get("destination_name") or sh.get("destination") or sh.get("delivery_station") or "?")
        rew = int(round(float(sh.get("reward") or sh.get("payout") or sh.get("fee") or 0)))
        col = int(round(float(sh.get("collateral") or sh.get("liability") or 0)))
        vol = sh.get("volume") or sh.get("cargo_size") or sh.get("units") or "?"
        vis = str(sh.get("visibility") or "public")
        prefix = f"[PARTNER:{ptag}] " if ptag else ""
        lines.append(f"  {prefix}{cid:14s} | {rew:>8,d} cr (col {col:,d}) | vol={vol} | {vis:7s} | {orig} -> {dest}")
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Read-only SpaceMolt freight / courier board CLI (Ch3 P2P).")
    ap.add_argument("cmd", choices=("list", "active", "profile", "track"))
    ap.add_argument("contract_id", nargs="?")
    ap.add_argument("--pilot", default="")
    ap.add_argument("--limit", type=int, default=25)
    ap.add_argument("--data", default=os.environ.get("COLLECTIVE_DATA", DATA_DEFAULT))
    args = ap.parse_args(argv)

    pilot = args.pilot or pick_shipping_pilot(args.data, prefer_docked=(args.cmd == "list"))
    neutral = load_neutral_tags(args.data)

    if args.cmd == "list":
        code, body = call_shipping(pilot, "list_all", {})
        if code != 200:
            # Retry once with another docked pilot if first lacked mission-service facility
            err_txt = json.dumps(body) if isinstance(body, dict) else str(body)
            print(f"SHIPPING LIST ERROR (pilot={pilot}, http={code}): {err_txt[:300]}")
            return 1
        print(f"(queried via docked pilot: {pilot})")
        print(format_list(body, neutral, limit=args.limit))
        return 0
    if args.cmd == "active":
        code, body = call_shipping(pilot, "active", {})
        print(f"SHIPPING ACTIVE (pilot={pilot}, http={code}):")
        print(body.get("result") if isinstance(body, dict) and body.get("result") else json.dumps(body, indent=2)[:800])
        return 0 if code == 200 else 1
    if args.cmd == "profile":
        code, body = call_shipping(pilot, "profile", {})
        print(f"SHIPPING PROFILE (pilot={pilot}, http={code}):")
        print(body.get("result") if isinstance(body, dict) and body.get("result") else json.dumps(body, indent=2)[:800])
        return 0 if code == 200 else 1
    if args.cmd == "track":
        if not args.contract_id:
            print("Usage: shipping.py track <contract_id>", file=sys.stderr)
            return 2
        code, body = call_shipping(pilot, "track", {"shipment_id": args.contract_id})
        print(f"SHIPPING TRACK {args.contract_id} (pilot={pilot}, http={code}):")
        print(body.get("result") if isinstance(body, dict) and body.get("result") else json.dumps(body, indent=2)[:800])
        return 0 if code == 200 else 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""shipping.py -- read-only galaxy-wide freight/courier contract board reader for spacemolt_shipping (Channel 3, Rule F39).

WHAT: lets Apollo (Logistics), Mercury (Trade), and Unity inspect open player/faction freight contracts across
      every charted station (`action=list_all`), active runs (`action=active`), carrier profile (`action=profile`),
      or package tracking (`action=track`) using a docked pilot with zero hand-hold side effects. Highlights any
      contracts posted by our Neutral (by agreement) diplomatic partners (`[HEXC]`, `[IRLC]`, etc.).
USAGE:
  shipping.py list [--pilot NAME] [--sort reward|distance|age] [--shipper TAG_OR_NAME] [--limit N] [--data DIR]
  shipping.py active [--pilot NAME] [--data DIR]
  shipping.py profile [--pilot NAME] [--data DIR]
  shipping.py track --id CONTRACT_ID [--pilot NAME] [--data DIR]

Stdlib only. ASCII only.
"""

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

GATE = "http://172.30.0.32:7580"
OPENER = urllib.request.build_opener(urllib.request.ProxyHandler({}))


def read_json(path, default):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def pick_docked_pilot(data, requested=""):
    if requested:
        return requested
    fl = read_json(Path(data) / "fleet" / "fleet.json", {})
    ships = [s for s in (fl.get("ships") or []) if isinstance(s, dict) and s.get("status") == "connected" and s.get("docked")]
    for prefix in ("hauler-", "trader-", "scout-"):
        cands = sorted(s["name"] for s in ships if str(s.get("name", "")).startswith(prefix))
        if cands:
            return cands[0]
    for s in ships:
        if s.get("name") == "Prime Directive":
            return "Prime Directive"
    return ships[0]["name"] if ships else "Prime Directive"


def neutral_tags(data):
    raw = read_json(Path(data) / "comms" / "diplomacy.json", {})
    out = set()
    for tag, info in (raw.get("factions") or {}).items():
        if isinstance(info, dict) and info.get("status") in ("neutrality_agreed", "trade_active", "info_sharing_active"):
            out.add(str(tag).upper())
    return out


def call_shipping(pilot, params, timeout=30):
    body = {"toolGroup": "spacemolt_shipping", "action": "shipping", "params": params}
    req = urllib.request.Request(
        GATE + "/accounts/%s/raw" % urllib.parse.quote(pilot, safe=""),
        data=json.dumps(body).encode("utf-8"),
        method="POST",
        headers={"Content-Type": "application/json"},
    )
    try:
        with OPENER.open(req, timeout=timeout) as r:
            return r.status, json.loads(r.read().decode("utf-8", "replace") or "{}")
    except urllib.error.HTTPError as e:
        return e.code, {"error": e.read().decode("utf-8", "replace")[:240]}
    except (urllib.error.URLError, OSError, ValueError) as e:
        return 0, {"error": "%s: %s" % (type(e).__name__, str(e)[:200])}


def extract_shipments(payload):
    """Normalize shipments list from spacemolt_shipping response."""
    if not isinstance(payload, dict):
        return [], ""
    sc = payload.get("structuredContent") if isinstance(payload.get("structuredContent"), dict) else payload
    if isinstance(sc.get("result"), dict):
        sc = sc["result"]
    items = sc.get("shipments") or sc.get("contracts") or sc.get("items") or []
    if not isinstance(items, list):
        items = []
    reason = str(sc.get("empty_reason") or sc.get("error") or payload.get("error") or "")
    return items, reason


def format_shipment_rows(items, partners, limit=20):
    rows = []
    for it in items:
        if not isinstance(it, dict):
            continue
        cid = str(it.get("id") or it.get("contract_id") or "")[:12]
        rew = int(it.get("base_reward") or it.get("reward") or 0)
        bonus = int(it.get("speed_bonus") or 0)
        orig = str(it.get("origin_base_name") or it.get("origin_base_id") or it.get("origin") or "-")[:20]
        dest = str(it.get("destination_base_name") or it.get("destination_base_id") or it.get("destination") or "-")[:20]
        shipper = str(it.get("shipper_name") or it.get("shipper_faction_tag") or it.get("shipper") or "-")[:18]
        stag = str(it.get("shipper_faction_tag") or "").upper()
        hops = it.get("distance") or it.get("jumps") or "?"
        elig = it.get("eligible", True)
        is_partner = bool(stag and stag in partners) or any(t in shipper.upper() for t in partners)
        rows.append((0 if is_partner else 1, -rew, {
            "id": cid, "reward": rew, "bonus": bonus, "origin": orig, "dest": dest,
            "shipper": shipper, "tag": stag, "hops": hops, "eligible": bool(elig), "partner": is_partner,
        }))
    rows.sort(key=lambda x: (x[0], x[1]))
    return [r[2] for r in rows[:max(1, int(limit))]]


def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    verb = args[0]

    def val(flag, default=""):
        if flag in args and args.index(flag) + 1 < len(args):
            return args[args.index(flag) + 1]
        return default

    data = val("--data", "/srv/collective/data")
    pilot = pick_docked_pilot(data, val("--pilot", ""))
    partners = neutral_tags(data)

    if verb == "list":
        params = {"action": "list_all", "sort": val("--sort", "reward"), "per_page": 50, "include_ineligible": True}
        if val("--shipper", ""):
            params["filter_shipper"] = val("--shipper", "")
        status, payload = call_shipping(pilot, params)
        if status != 200:
            print("SHIPPING LIST ERROR (pilot=%s, http=%s): %s" % (pilot, status, payload.get("error", payload)))
            return 1
        items, reason = extract_shipments(payload)
        rows = format_shipment_rows(items, partners, limit=int(val("--limit", "20")))
        print("FREIGHT BOARD (spacemolt_shipping list_all via %s) | total=%d | shown=%d | neutral_partners=%s"
              % (pilot, len(items), len(rows), ",".join(sorted(partners)) or "none"))
        if not rows:
            print("  (empty board%s)" % (": " + reason if reason else ""))
            return 0
        print("  %-12s %-10s %-18s %-20s -> %-20s %-4s %-5s %s" % ("ID", "REWARD", "SHIPPER", "ORIGIN", "DEST", "JUMPS", "ELIG", "NOTE"))
        for r in rows:
            note = "[PARTNER]" if r["partner"] else ""
            rew_s = "%s%s" % (format(r["reward"], ","), ("+%d" % r["bonus"]) if r["bonus"] else "")
            print("  %-12s %-10s %-18s %-20s -> %-20s %-4s %-5s %s" % (
                r["id"], rew_s[:10], r["shipper"], r["origin"], r["dest"], str(r["hops"])[:4], "yes" if r["eligible"] else "no", note))
        return 0

    if verb in ("active", "profile"):
        status, payload = call_shipping(pilot, {"action": verb})
        print("SHIPPING %s (pilot=%s, http=%s):" % (verb.upper(), pilot, status))
        print(json.dumps(payload.get("structuredContent", payload), indent=2, sort_keys=True)[:2500])
        return 0 if status == 200 else 1

    if verb == "track":
        cid = val("--id", "")
        if not cid:
            print("USAGE: shipping.py track --id CONTRACT_ID [--pilot NAME]")
            return 2
        status, payload = call_shipping(pilot, {"action": "track", "contract_id": cid})
        print("SHIPPING TRACK %s (pilot=%s, http=%s):" % (cid, pilot, status))
        print(json.dumps(payload.get("structuredContent", payload), indent=2, sort_keys=True)[:2500])
        return 0 if status == 200 else 1

    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main())

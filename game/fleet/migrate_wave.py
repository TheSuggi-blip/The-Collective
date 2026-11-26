#!/usr/bin/env python3
"""migrate_wave.py -- Safe section-by-section fleet migration and Reserve archiver for the 500-ship redesign.

WHAT: executes one approved migration wave (1..6) from game/fleet-500-manifest.tsv while keeping
      all 10 Command flagships untouched, keeping auto-upgrades disabled, keeping CLTV <= 500 seats,
      and preserving all 490 retired pilots cleanly disconnected in Reserves (never deleted).

      Per wave:
        1. Plan exact retiring old pilots vs incoming Culture-prefixed pilots (hard-asserts zero Command pilots retired).
        2. Stop & hand-hold retiring pilots so dispatch.py does not re-dispatch them during retirement.
        3. Cancel open market orders (best-effort) so escrow returns to wallet.
        4. Sweep wallet credits (>0) directly to CLTV faction treasury (fallback: gift to Prime Directive).
        5. Deposit onboard cargo to faction storage when docked (best-effort).
        6. Remove retiring pilots from CLTV (leave, fallback kick by Prime Directive) -- requires wall.py leave-faction pass.
        7. Archive retiring pilots as Reserves: append to data/fleet/rejoin-off, record metadata in data/fleet/reserves.json,
           and disconnect live WebSocket via DELETE /accounts/<pilot>.
        8. Register new Culture-prefixed pilots (POST /accounts/register, idempotent resume), invite & join CLTV,
           and transfer Officer/Builder roles on Waves 4-5.

USAGE:
  migrate_wave.py --wave <1..6> [--dry-run] [--limit N] [--skip-birth] [--skip-retire]
  migrate_wave.py --plan-all    (read-only dry-run audit of all 6 waves against live fleet.json)

Stdlib only. ASCII only.
"""

import argparse
import json
import os
import re
import sqlite3
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import stop_pilot  # noqa: E402

DATA = Path(os.environ.get("FLEET_DATA_ROOT", "/srv/collective/data"))
GATE = os.environ.get("FLEET_GATE", "http://172.30.0.32:7580")
MANIFEST_PATH = ROOT / "game" / "fleet-500-manifest.tsv"

KEPT_COMMAND = frozenset({
    "Prime Directive", "Zero Point", "Golden Chariot", "Mercurys Ledger", "Hades",
    "Vision", "Solar Mandate", "Nebula Charter", "Rimward Pact", "Crimson Aegis",
})

_OPENER = urllib.request.build_opener(urllib.request.ProxyHandler({}))


def utc_now():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def natural_key(name):
    m = re.match(r"^([a-z]+)-(\d+)$", str(name or ""))
    return (m.group(1), int(m.group(2))) if m else (str(name or ""), 0)


def load_manifest(path=MANIFEST_PATH):
    """Return list of dict rows from fleet-500-manifest.tsv."""
    rows = []
    hdr = None
    for raw in Path(path).read_text(encoding="ascii").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split("\t")
        if hdr is None:
            hdr = parts
            continue
        rec = dict(zip(hdr, parts))
        rec["wave"] = int(rec["wave"])
        rows.append(rec)
    return rows


def load_live_fleet(data_dir=DATA):
    p = Path(data_dir) / "fleet" / "fleet.json"
    if not p.is_file():
        return []
    doc = json.loads(p.read_text(encoding="utf-8"))
    return [s for s in (doc.get("ships") or []) if isinstance(s, dict) and s.get("name")]


def load_officers(data_dir=DATA):
    db = Path(data_dir) / "store" / "read.db"
    if not db.is_file():
        return {}
    con = sqlite3.connect("file:%s?mode=ro" % db, uri=True)
    try:
        return {
            str(r[0]): str(r[1])
            for r in con.execute("SELECT pilot, role FROM faction_members WHERE LOWER(role) NOT IN ('member','recruit')")
        }
    finally:
        con.close()


def plan_wave_retirements(wave, live_ships, officers):
    """Return deterministic ordered list of legacy pilots to retire in `wave` (1..6).

    Matches Suggi's exact 6-wave plan (never exceeds 500 CLTV seats; never touches KEPT_COMMAND):
      W1: 130 miner-*
      W2: 80 drone-* (preferring non-officers first)
      W3: remaining 15 drone-* + 35 sentinel-* + 5 non-officer hauler-* + 5 non-officer scout-* (60 total)
      W4: 85 trader-*
      W5: remaining hauler-* (90)
      W6: remaining scout-* (45)
    """
    names = [str(s["name"]) for s in live_ships if str(s.get("name") or "") not in KEPT_COMMAND]

    def by_prefix(pfx, non_officer_first=True):
        pool = [n for n in names if n.startswith(pfx)]
        if non_officer_first:
            pool.sort(key=lambda n: (1 if n in officers else 0, natural_key(n)))
        else:
            pool.sort(key=natural_key)
        return pool

    if wave == 1:
        retire = by_prefix("miner-", non_officer_first=True)[:130]
    elif wave == 2:
        retire = by_prefix("drone-", non_officer_first=True)[:80]
    elif wave == 3:
        drones = by_prefix("drone-", non_officer_first=True)
        sents = by_prefix("sentinel-", non_officer_first=True)
        haulers = by_prefix("hauler-", non_officer_first=True)
        scouts = by_prefix("scout-", non_officer_first=True)
        # Keep non-officer / highest-numbered haulers & scouts for the +10 seat rebalance
        haul_pick = [h for h in haulers if h not in officers][:5]
        if len(haul_pick) < 5:
            haul_pick = haulers[:5]
        scout_pick = [s for s in scouts if s not in officers][:5]
        if len(scout_pick) < 5:
            scout_pick = scouts[:5]
        retire = drones[:15] + sents[:35] + haul_pick + scout_pick
    elif wave == 4:
        retire = by_prefix("trader-", non_officer_first=True)[:85]
    elif wave == 5:
        retire = by_prefix("hauler-", non_officer_first=True)
    elif wave == 6:
        retire = by_prefix("scout-", non_officer_first=True)
    else:
        raise ValueError("wave must be 1..6")

    bad = [n for n in retire if n in KEPT_COMMAND]
    assert not bad, "SAFETY HALT: attempted to retire kept Command ship(s): %s" % bad
    return retire


def gate_http(method, path, body=None, timeout=60):
    url = GATE.rstrip("/") + path
    data = None if body is None else json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, method=method)
    if data is not None:
        req.add_header("Content-Type", "application/json")
    try:
        with _OPENER.open(req, timeout=timeout) as resp:
            return resp.status, resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", errors="replace")
    except Exception as e:
        return 0, str(e)


def raw_call(pilot, group, action, params=None, timeout=60):
    return gate_http(
        "POST",
        "/accounts/%s/raw" % urllib.parse.quote(pilot, safe=""),
        {"toolGroup": group, "action": action, "params": params or {}},
        timeout=timeout,
    )


def parse_sc(txt):
    if not txt or "{" not in txt:
        return {}
    try:
        obj = json.loads(txt[txt.find("{"):])
        if isinstance(obj, dict) and isinstance(obj.get("structuredContent"), dict):
            return obj["structuredContent"]
        return obj if isinstance(obj, dict) else {}
    except ValueError:
        return {}


def write_hand_hold(data_dir, pilot):
    odir = Path(data_dir) / "fleet" / "orders"
    odir.mkdir(parents=True, exist_ok=True)
    p = odir / (pilot + ".json")
    p.write_text(json.dumps({"pilot": pilot, "what": "hand Unity", "since": utc_now()}) + "\n", encoding="utf-8")


def release_hand_hold(data_dir, pilot):
    p = Path(data_dir) / "fleet" / "orders" / (pilot + ".json")
    try:
        p.unlink()
    except OSError:
        pass


def append_rejoin_off(data_dir, pilot):
    p = Path(data_dir) / "fleet" / "rejoin-off"
    cur = set()
    if p.is_file():
        cur = {ln.strip() for ln in p.read_text(encoding="utf-8", errors="replace").splitlines() if ln.strip()}
    if pilot not in cur:
        cur.add(pilot)
        tmp = p.with_suffix(".tmp")
        tmp.write_text("\n".join(sorted(cur)) + "\n", encoding="ascii")
        os.replace(tmp, p)


def record_reserve(data_dir, rec):
    p = Path(data_dir) / "fleet" / "reserves.json"
    doc = {"updated_at": utc_now(), "reserves": {}}
    if p.is_file():
        try:
            old = json.loads(p.read_text(encoding="utf-8"))
            if isinstance(old, dict) and isinstance(old.get("reserves"), dict):
                doc = old
        except ValueError:
            pass
    doc["updated_at"] = utc_now()
    doc["reserves"][rec["pilot"]] = rec
    tmp = p.with_suffix(".tmp")
    tmp.write_text(json.dumps(doc, indent=2, sort_keys=True) + "\n", encoding="ascii")
    os.replace(tmp, p)


def live_connected_set():
    """Return set of currently connected usernames from engine GET /accounts."""
    st, txt = gate_http("GET", "/accounts", timeout=30)
    if st != 200:
        return None
    try:
        accs = (json.loads(txt) or {}).get("accounts") or []
    except ValueError:
        return None
    return {str(a.get("username") or "") for a in accs if isinstance(a, dict) and a.get("status") == "connected"}


def get_faction_id(data_dir):
    emp_p = Path(data_dir) / "empire" / "empire.json"
    fid = ""
    if emp_p.is_file():
        try:
            emp = json.loads(emp_p.read_text(encoding="utf-8"))
            fid = str(((emp.get("faction") or {}).get("id")) or "")
        except ValueError:
            pass
    st, txt = raw_call("Prime Directive", "spacemolt_faction", "info", {})
    sc = parse_sc(txt)
    return str(sc.get("id") or fid)


def retire_one(pilot, ship_doc, wave, data_dir, leader="Prime Directive"):
    """Stop, cancel orders, sweep credits & docked cargo, leave CLTV, archive to Reserves, disconnect."""
    assert pilot not in KEPT_COMMAND
    res = {"pilot": pilot, "wave": wave, "retired_at": utc_now(), "empire": ship_doc.get("empire", ""), "steps": []}

    # 1. Hand-hold and abort any active loop/run
    write_hand_hold(data_dir, pilot)
    gate_http("DELETE", "/accounts/%s/abort" % urllib.parse.quote(pilot, safe=""), timeout=30)

    # 2. Best-effort cancel open market orders so escrow refunds to wallet
    st_o, txt_o = raw_call(pilot, "spacemolt_market", "view_orders", {})
    sc_o = parse_sc(txt_o)
    cancelled = 0
    for o in (sc_o.get("orders") or []):
        oid = o.get("order_id") or o.get("id") if isinstance(o, dict) else None
        if oid:
            st_c, _ = raw_call(pilot, "spacemolt_market", "cancel_order", {"order_id": oid})
            if st_c == 200:
                cancelled += 1
    if cancelled:
        res["steps"].append("cancelled_orders:%d" % cancelled)

    # 3. Read fresh status (wallet + docked cargo)
    st_s, txt_s = raw_call(pilot, "spacemolt_query", "get_status", {})
    sc_s = parse_sc(txt_s)
    player = sc_s.get("player") if isinstance(sc_s.get("player"), dict) else {}
    ship = sc_s.get("ship") if isinstance(sc_s.get("ship"), dict) else {}
    credits = int(player.get("credits") if player.get("credits") is not None else (ship_doc.get("credits") or 0))
    docked = bool(player.get("docked_at_base") or (sc_s.get("location") or {}).get("docked_at") or ship_doc.get("docked"))

    # 4. Best-effort deposit cargo if docked
    cargo = ship.get("cargo") or sc_s.get("cargo") or []
    dep_items = 0
    if docked and isinstance(cargo, list):
        for c in cargo:
            if isinstance(c, dict) and c.get("item_id") and int(c.get("quantity") or 0) > 0:
                st_d, txt_d = raw_call(pilot, "spacemolt_storage", "deposit", {
                    "item_id": c["item_id"], "quantity": int(c["quantity"]), "target": "faction", "source": "cargo",
                })
                if st_d == 200 and '"error"' not in txt_d[:240]:
                    dep_items += int(c["quantity"])
    res["cargo_deposited"] = dep_items

    # 5. Sweep ALL wallet credits directly to CLTV treasury (fallback: gift to leader)
    swept = 0
    if credits > 0:
        st_w, txt_w = raw_call(pilot, "spacemolt_storage", "deposit", {
            "item_id": "credits", "quantity": credits, "target": "faction",
        })
        if st_w == 200 and '"error"' not in txt_w[:240]:
            swept = credits
        else:
            st_w2, txt_w2 = raw_call(pilot, "spacemolt_storage", "deposit", {
                "item_id": "credits", "quantity": credits, "target": leader,
            })
            if st_w2 == 200 and '"error"' not in txt_w2[:240]:
                swept = credits
            else:
                res["steps"].append("sweep_err:%s" % txt_w2[:80])
    res["credits_swept"] = swept

    # 6. Leave CLTV faction (pilot's own leave -- scoped pass in wall.py; retry up to 3x)
    left_ok = False
    st_l, txt_l = 0, ""
    for att in range(3):
        st_l, txt_l = raw_call(pilot, "spacemolt_faction", "leave", {})
        low = txt_l.lower()
        if (st_l == 200 and '"error"' not in txt_l[:240]) or ("not_in_faction" in low) or ("not in a faction" in low):
            left_ok = True
            break
        if st_l == 403 and "leave-faction" in txt_l:
            return False, "BLOCKED by wall.py (leave-faction): %s" % txt_l[:140], res
        if att < 2:
            time.sleep(2.0)
    if not left_ok:
        release_hand_hold(data_dir, pilot)
        return False, "leave failed (%s): %s" % (st_l, txt_l[:120]), res
    res["steps"].append("left_cltv")

    # 7. Archive as Reserve & disconnect WebSocket cleanly (never deleted!)
    append_rejoin_off(data_dir, pilot)
    record_reserve(data_dir, res)
    st_del, txt_del = gate_http("DELETE", "/accounts/%s" % urllib.parse.quote(pilot, safe=""), timeout=30)
    res["disconnected"] = (st_del in (200, 204, 404))
    release_hand_hold(data_dir, pilot)
    return True, "retired+archived (swept %d cr, cargo %d u, disc=%s)" % (swept, dep_items, res["disconnected"]), res


def birth_one(row, fid, leader="Prime Directive", promote_role=None):
    """Register new Culture-prefixed pilot, invite & join CLTV, optionally promote."""
    pilot = row["pilot"]
    empire = row["empire"]

    # Idempotent check: already connected?
    st_g, _ = gate_http("GET", "/accounts/%s" % urllib.parse.quote(pilot, safe=""), timeout=20)
    if st_g != 200:
        for attempt in range(3):
            st_r, txt_r = gate_http("POST", "/accounts/register", {"username": pilot, "empire": empire}, timeout=60)
            if st_r in (200, 201, 409):
                break
            if attempt < 2:
                time.sleep(3.0)
        else:
            return False, "register failed (%s): %s" % (st_r, txt_r[:120])
        time.sleep(1.5)

    # Invite & Join CLTV (retry up to 3x in case newly registered socket finishes handshake)
    joined = False
    txt_i = txt_j = ""
    for att in range(3):
        st_i, txt_i = raw_call(leader, "spacemolt_faction", "invite", {"player_id": pilot})
        st_j, txt_j = raw_call(pilot, "spacemolt_faction", "join", {"faction_id": fid})
        comb = (txt_i + " " + txt_j).lower()
        if (st_j == 200 and '"error"' not in txt_j[:240]) or ("already" in comb and "member" in comb) or ("already in" in comb):
            joined = True
            break
        if att < 2:
            time.sleep(2.5)
    if not joined:
        return False, "join CLTV failed: inv=%s join=%s" % (txt_i[:80], txt_j[:80])

    # Optional Officer / Builder promotion
    if promote_role:
        st_p, txt_p = raw_call(leader, "spacemolt_faction_admin", "promote", {"player_id": pilot, "role_id": promote_role})
        if st_p != 200 or '"error"' in txt_p[:240]:
            return True, "birthed+joined (promote %s warn: %s)" % (promote_role, txt_p[:70])
        return True, "birthed+joined+promoted(%s)" % promote_role
    return True, "birthed+joined"


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--wave", type=int, choices=[1, 2, 3, 4, 5, 6])
    ap.add_argument("--plan-all", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--skip-retire", action="store_true")
    ap.add_argument("--skip-birth", action="store_true")
    ap.add_argument("--data", default=str(DATA))
    args = ap.parse_args(argv)

    data_dir = Path(args.data)
    manifest = load_manifest()
    live = load_live_fleet(data_dir)
    officers = load_officers(data_dir)

    if args.plan_all:
        sim_live = list(live)
        print("LIVE FLEET: %d ships (%d kept Command)" % (len(live), sum(1 for s in live if s["name"] in KEPT_COMMAND)))
        for w in range(1, 7):
            inc = [r for r in manifest if r["wave"] == w and r["status"] == "planned"]
            ret = plan_wave_retirements(w, sim_live, officers)
            ret_cr = sum(int(s.get("credits") or 0) for s in sim_live if s["name"] in set(ret))
            ret_off = sum(1 for n in ret if n in officers)
            print("WAVE %d: retire=%3d (officers=%2d, wallets=%10s cr) -> birth=%3d (%s)" % (
                w, len(ret), ret_off, format(ret_cr, ","), len(inc),
                ", ".join("%s:%d" % (p, sum(1 for r in inc if r["prefix"] == p)) for p in sorted({r["prefix"] for r in inc})),
            ))
            # Update simulated roster for next wave
            ret_set = set(ret)
            sim_live = [s for s in sim_live if s["name"] not in ret_set] + [{"name": r["pilot"], "credits": 0} for r in inc]
        print("POST-WAVE-6 SIMULATED TOTAL: %d ships" % len(sim_live))
        return 0

    if not args.wave:
        ap.error("Specify --wave <1..6> or --plan-all")

    w = args.wave
    conn_set = live_connected_set() if not args.dry_run else None
    live_eff = [s for s in live if (conn_set is None or s["name"] in conn_set)]
    inc_all = [r for r in manifest if r["wave"] == w and r["status"] == "planned"]
    inc = [r for r in inc_all if (conn_set is None or r["pilot"] not in conn_set)]
    ret = plan_wave_retirements(w, live_eff, officers)
    ship_by_name = {s["name"]: s for s in live_eff}
    if args.limit > 0:
        ret = ret[:args.limit]
        inc = inc[:args.limit]

    print("WAVE %d PLAN: retire=%d, birth=%d, dry_run=%s" % (w, len(ret), len(inc), args.dry_run))
    if args.dry_run:
        print("  Retire sample:", ret[:8], "...", ret[-3:])
        print("  Birth sample: ", [(r["pilot"], r["empire"]) for r in inc[:8]])
        return 0

    fid = get_faction_id(data_dir)
    if not fid:
        sys.exit("HALT: could not resolve CLTV faction_id")

    # Phase A: Stop all retiring pilots first
    if not args.skip_retire and ret:
        print("[%s] Stopping %d retiring pilots via stop_pilot..." % (utc_now(), len(ret)), flush=True)
        runs = stop_pilot.active_runs(str(data_dir))
        for p in ret:
            write_hand_hold(data_dir, p)
            try:
                stop_pilot.request_stop(p, str(data_dir), runs=runs)
            except Exception:
                pass
        time.sleep(3.0)
        ok_r = 0
        tot_swept = 0
        for idx, p in enumerate(ret, 1):
            ok, msg, rec = retire_one(p, ship_by_name.get(p, {}), w, data_dir)
            print("[%s] RETIRE %d/%d %s: %s -- %s" % (utc_now(), idx, len(ret), p, "OK" if ok else "FAIL", msg), flush=True)
            if not ok and "BLOCKED by wall.py" in msg:
                sys.exit("HALT: " + msg)
            if ok:
                ok_r += 1
                tot_swept += int(rec.get("credits_swept") or 0)
            time.sleep(0.5)
        print("[%s] WAVE %d RETIRE SUMMARY: %d/%d archived, swept %s cr" % (utc_now(), w, ok_r, len(ret), format(tot_swept, ",")), flush=True)

    # Phase B: Birth & Onboard new Culture pilots
    if not args.skip_birth and inc:
        ok_b = 0
        for idx, row in enumerate(inc, 1):
            promo = None
            if w == 4 and idx <= 25:
                promo = "officer"
            elif w == 5 and idx == 1:
                promo = "builder"
            elif w == 5 and idx <= 25:
                promo = "officer"
            ok, msg = birth_one(row, fid, promote_role=promo)
            print("[%s] BIRTH %d/%d %s (%s): %s -- %s" % (utc_now(), idx, len(inc), row["pilot"], row["empire"], "OK" if ok else "FAIL", msg), flush=True)
            if ok:
                ok_b += 1
            time.sleep(1.2)
        print("[%s] WAVE %d BIRTH SUMMARY: %d/%d birthed+joined CLTV" % (utc_now(), w, ok_b, len(inc)), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())

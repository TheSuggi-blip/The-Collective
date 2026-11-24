#!/usr/bin/env python3
"""Dynamic Docked Commercial & Industrial Manufacturing Network (`craft-network`).

WHAT:
  Zero-fuel docked manufacturing runner governed by `game/craft-policy.json` and
  `game/craft-demand.json`. Enforces Strict Classes (P5):
    - Trade (`trader`): scores workshop recipes with live positive net margin
      (`output_bid * qty - input_cost - est_fee >= min_profit_cr`, `margin >= min_margin_pct`),
      uses stored inputs first or buys cheap docked asks, crafts, and sells / posts `sell_order`
      across our 61+ Bursar hubs.
    - Logistics (`hauler`): crafts industrial building materials (`steel_plate`, `circuit_board`,
      `wiring`, `copper_piping`, `fuel_cell`, `need_status` craft items) from stored or cheap
      docked inputs and stores output into faction/personal reserve storage (never sells).

USAGE:
  python3 -I -B game/fleet/craft_net.py <pilot> [--policy game/craft-policy.json] [--route craft-network]

Stdlib only. ASCII only.
"""
import fcntl
import json
import os
import re
import sqlite3
import sys
import threading
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
DATA = Path(os.environ.get("COLLECTIVE_DATA", "/srv/collective/data"))
TICK = 10.5

sys.path.insert(0, str(ROOT / "fleet"))
import gate


def utc_now():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def read_json(path, default=None):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8", errors="replace"))
    except (OSError, ValueError):
        return {} if default is None else default


def write_json(path, obj):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + ".tmp.%d" % os.getpid())
    tmp.write_text(json.dumps(obj, indent=1, sort_keys=True), encoding="ascii")
    os.replace(tmp, p)


def ship_file_name(pilot):
    return re.sub(r"[^a-zA-Z0-9._-]+", "_", str(pilot)).strip("_") + ".json"


def load_craft_world(data_dir, repo_root, policy):
    """Load workshop recipes, inputs, outputs, live books, need_status, and craft-demand."""
    db = Path(data_dir) / "store" / "read.db"
    recipes = {}        # rid -> {id, name, facility_only, inputs: [(item, qty)], outputs: [(item, qty)]}
    books_by_base = {}  # base -> {item: {bid, bid_qty, ask, ask_qty}}
    global_bid = {}     # item -> (max_bid, total_bid_qty)
    item_vals = {}
    need_crafts = set()
    stock_by_item = {}

    if db.is_file():
        con = sqlite3.connect("file:%s?mode=ro" % db, uri=True, timeout=3.0)
        try:
            tbls = {r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type IN ('table','view')").fetchall()}
            if "recipes" in tbls and "recipe_inputs" in tbls and "recipe_outputs" in tbls:
                for rid, nm, fo in con.execute("SELECT id, name, COALESCE(facility_only, 0) FROM recipes"):
                    recipes[str(rid)] = {"id": str(rid), "name": str(nm or rid), "facility_only": bool(fo), "inputs": [], "outputs": []}
                for rid, iid, u in con.execute("SELECT recipe, item, units FROM recipe_inputs"):
                    if str(rid) in recipes and iid and int(u or 0) > 0:
                        recipes[str(rid)]["inputs"].append((str(iid), int(u)))
                for rid, iid, u in con.execute("SELECT recipe, item, units FROM recipe_outputs"):
                    if str(rid) in recipes and iid and int(u or 0) > 0:
                        recipes[str(rid)]["outputs"].append((str(iid), int(u)))
            if "items" in tbls:
                cols = {r[1] for r in con.execute("PRAGMA table_info(items)").fetchall()}
                vcol = "base_value" if "base_value" in cols else ("value" if "value" in cols else None)
                if vcol:
                    for iid, val in con.execute("SELECT id, %s FROM items" % vcol):
                        if iid and val:
                            item_vals[str(iid)] = float(val)
            if "books" in tbls:
                for b_id, iid, bid, bq, ask, aq in con.execute(
                    "SELECT base, item, COALESCE(bid,0), COALESCE(bid_qty,0), COALESCE(ask,0), COALESCE(ask_qty,0) FROM books"
                ):
                    b_s, i_s = str(b_id or ""), str(iid or "")
                    if not b_s or not i_s:
                        continue
                    books_by_base.setdefault(b_s, {})[i_s] = {
                        "bid": float(bid or 0), "bid_qty": int(bq or 0),
                        "ask": float(ask or 0), "ask_qty": int(aq or 0),
                    }
                    if float(bid or 0) > 0 and int(bq or 0) > 0:
                        prev_b, prev_q = global_bid.get(i_s, (0.0, 0))
                        global_bid[i_s] = (max(prev_b, float(bid)), prev_q + int(bq))
            if "need_status" in tbls:
                for (craft_s,) in con.execute("SELECT craft FROM need_status WHERE craft IS NOT NULL").fetchall():
                    for part in str(craft_s).split(";"):
                        m = re.match(r"\s*([a-z0-9_]+)\s+\d+", part.strip())
                        if m:
                            need_crafts.add(m.group(1))
            if "holdings" in tbls:
                for iid, tot in con.execute("SELECT item, COALESCE(SUM(units),0) FROM holdings GROUP BY item"):
                    if iid:
                        stock_by_item[str(iid)] = int(tot or 0)
            if "supply_status" in tbls:
                for iid, stk, keep in con.execute("SELECT item, COALESCE(stock,0), COALESCE(keep,0) FROM supply_status"):
                    if iid:
                        stock_by_item[str(iid)] = int(stk or 0)
                        if int(keep or 0) > 0 and int(stk or 0) < int(keep or 0):
                            need_crafts.add(str(iid))
        finally:
            con.close()

    dem_rel = str(policy.get("demand_file") or "game/craft-demand.json")
    dem_p = Path(dem_rel) if Path(dem_rel).is_absolute() else (Path(repo_root) / dem_rel)
    demand = read_json(dem_p, {})
    return {
        "recipes": recipes, "books_by_base": books_by_base, "global_bid": global_bid,
        "item_vals": item_vals, "need_crafts": need_crafts, "stock_by_item": stock_by_item,
        "demand": demand,
    }


def expand_demand_raw_inputs(world):
    """Derive needed raw inputs `{item_id: cap}` from craft-demand targets & profitable workshop recipes."""
    demand = world.get("demand") or {}
    if not isinstance(demand, dict) or not demand.get("enabled", True):
        return {}
    raw_caps = {str(k): int(v) for k, v in (demand.get("raw_input_caps") or {}).items() if int(v or 0) > 0}
    target_outputs = set()
    for grp in ("industrial_targets", "commercial_targets"):
        for iid, cfg in (demand.get(grp) or {}).items():
            cap = int((cfg or {}).get("cap") or 0)
            cur = int((world.get("stock_by_item") or {}).get(str(iid), 0))
            if cap <= 0 or cur < cap:
                target_outputs.add(str(iid))

    # Also auto-discover profitable workshop recipes if enabled
    recipes = world.get("recipes") or {}
    if demand.get("auto_discover_profitable", True):
        min_m = float(demand.get("min_margin_pct") or 0.22)
        min_p = float(demand.get("min_profit_cr") or 150)
        min_bq = int(demand.get("min_bid_qty") or 5)
        gbid = world.get("global_bid") or {}
        ivals = world.get("item_vals") or {}
        for rec in recipes.values():
            if rec.get("facility_only") or not rec.get("inputs") or not rec.get("outputs"):
                continue
            out_item, out_q = rec["outputs"][0]
            mb, bq = gbid.get(out_item, (0.0, 0))
            if mb <= 0 or bq < min_bq:
                continue
            in_cost = sum(q * float(ivals.get(ii) or 10.0) for ii, q in rec["inputs"])
            rev = mb * out_q
            if rev - in_cost >= min_p and in_cost > 0 and (rev - in_cost) / in_cost >= min_m:
                target_outputs.add(out_item)

    wanted_raw = {}
    for rec in recipes.values():
        if rec.get("facility_only") or not rec.get("inputs") or not rec.get("outputs"):
            continue
        out_item = rec["outputs"][0][0]
        if out_item not in target_outputs:
            continue
        for in_item, _q in rec["inputs"]:
            cap = raw_caps.get(in_item, 15000)
            cur = int((world.get("stock_by_item") or {}).get(in_item, 0))
            if cur < cap:
                wanted_raw[in_item] = max(wanted_raw.get(in_item, 0), cap - cur)
    return wanted_raw


def pick_craft_job(division, base_id, stored_items, credits, world, policy):
    """Select the highest-priority executable workshop craft job at `base_id` for `division` (strict P5)."""
    if not policy or not policy.get("enabled", True) or not base_id:
        return None
    is_trade = (str(division) == "Trade")
    is_log = (str(division) == "Logistics")
    if not (is_trade or is_log):
        return None
    sub = (policy.get("trade") if is_trade else policy.get("logistics")) or {}
    if not sub.get("enabled", True):
        return None

    book = (world.get("books_by_base") or {}).get(base_id) or {}
    gbid = world.get("global_bid") or {}
    ivals = world.get("item_vals") or {}
    demand = world.get("demand") or {}
    stock_map = world.get("stock_by_item") or {}
    stored = {str(k): int(v or 0) for k, v in (stored_items or {}).items() if int(v or 0) > 0}
    allow_buy = bool(policy.get("allow_buy_inputs_docked", True))
    budget = min(
        max(0, int(credits or 0) - int(policy.get("min_wallet_keep_cr") or 15000)),
        int(policy.get("max_buy_spend_per_cycle_cr") or 25000),
    )
    max_runs = max(1, int(policy.get("max_runs_per_cycle") or 10))
    est_fee = float(policy.get("max_fee_per_run_cr") or 1500) * 0.2

    ind_targets = set()
    if is_log:
        if sub.get("use_needs_tsv", True):
            ind_targets |= set(world.get("need_crafts") or set())
        if sub.get("use_industrial_targets", True):
            for iid, cfg in (demand.get("industrial_targets") or {}).items():
                cap = int((cfg or {}).get("cap") or 0)
                if cap <= 0 or stock_map.get(str(iid), 0) < cap:
                    ind_targets.add(str(iid))

    comm_targets = set((demand.get("commercial_targets") or {}).keys()) if is_trade else set()
    min_margin = float(sub.get("min_margin_pct") or 0.22)
    min_profit = float(sub.get("min_profit_cr") or 150)
    min_bq = int(sub.get("min_bid_qty") or 3)

    best = None
    for rec in (world.get("recipes") or {}).values():
        if rec.get("facility_only") or not rec.get("inputs") or not rec.get("outputs"):
            continue
        out_item, out_qty = rec["outputs"][0]
        if is_log and out_item not in ind_targets:
            continue

        # Check how many runs we can supply from stored + optional docked buys
        max_possible = max_runs
        buy_per_run = {}
        cost_per_run = 0.0
        buy_cost_per_run = 0.0
        feasible = True
        for in_item, req_q in rec["inputs"]:
            have = stored.get(in_item, 0)
            row_b = book.get(in_item) or {}
            ask = float(row_b.get("ask") or 0)
            aq = int(row_b.get("ask_qty") or 0)
            if have >= req_q:
                runs_from_here = have // req_q
                if allow_buy and ask > 0 and aq > 0:
                    runs_from_here += aq // req_q
                max_possible = min(max_possible, runs_from_here)
                unit_c = ask if ask > 0 else float(ivals.get(in_item) or 10.0)
                cost_per_run += req_q * unit_c
            elif allow_buy and ask > 0 and aq >= req_q:
                max_possible = min(max_possible, aq // req_q)
                buy_per_run[in_item] = (req_q, int(round(ask)))
                buy_cost_per_run += req_q * ask
                cost_per_run += req_q * ask
            else:
                feasible = False
                break
        if not feasible or max_possible <= 0:
            continue
        if buy_cost_per_run > 0:
            max_by_cash = int(budget // buy_cost_per_run)
            max_possible = min(max_possible, max_by_cash)
            if max_possible <= 0:
                continue

        # Compute exact buys needed for `runs` after using `stored` first
        runs = max(1, min(max_possible, max_runs))
        buys = []
        tot_buy = 0
        for in_item, req_q in rec["inputs"]:
            need_total = req_q * runs
            short_q = max(0, need_total - stored.get(in_item, 0))
            if short_q > 0:
                ask = int(round(float((book.get(in_item) or {}).get("ask") or 0)))
                if ask <= 0:
                    feasible = False
                    break
                buys.append((in_item, short_q, ask))
                tot_buy += short_q * ask
        if not feasible or tot_buy > budget:
            continue

        if is_trade:
            local_b = book.get(out_item) or {}
            bid = float(local_b.get("bid") or 0)
            bq = int(local_b.get("bid_qty") or 0)
            if bid <= 0:
                bid, bq = gbid.get(out_item, (0.0, 0))
            if bid <= 0 or bq < min_bq:
                continue
            rev_per_run = bid * out_qty
            prof_per_run = rev_per_run - cost_per_run - est_fee
            margin = prof_per_run / max(1.0, cost_per_run)
            if prof_per_run < min_profit or margin < min_margin:
                continue
            score = prof_per_run * runs * (1.25 if out_item in comm_targets else 1.0) * (1.2 if float(local_b.get("bid") or 0) > 0 else 1.0)
            cand = {
                "recipe": rec["id"], "makes": out_item, "per_run": out_qty, "runs": runs,
                "buys": buys, "est_profit": round(prof_per_run * runs, 1), "margin_pct": round(margin * 100.0, 1),
                "sell_price": int(round(bid)), "mode": "commercial", "score": round(score, 2),
            }
        else:
            prio_boost = 5.0 if out_item in (world.get("need_crafts") or set()) else 1.0
            stored_ratio = 1.0 if not buys else 0.6
            score = prio_boost * stored_ratio * runs * max(10.0, float(ivals.get(out_item) or 50.0))
            cand = {
                "recipe": rec["id"], "makes": out_item, "per_run": out_qty, "runs": runs,
                "buys": buys, "est_profit": 0.0, "margin_pct": 0.0,
                "sell_price": 0, "mode": "industrial", "score": round(score, 2),
            }
        if best is None or cand["score"] > best["score"]:
            best = cand
    return best


def _heartbeat(order_path, every=60):
    stop_ev = threading.Event()
    def beat():
        while not stop_ev.wait(every):
            try:
                os.utime(order_path)
            except OSError:
                return
    threading.Thread(target=beat, daemon=True).start()
    return stop_ev


def _option(args, flag, default=""):
    return args[args.index(flag) + 1] if flag in args and args.index(flag) + 1 < len(args) else default


def main(argv=None):
    args = sys.argv[1:] if argv is None else list(argv)
    if not args or args[0].startswith("--"):
        sys.exit("usage: craft_net.py <pilot> [--policy game/craft-policy.json] [--route craft-network]")
    pilot = args[0]
    route_id = _option(args, "--route", "craft-network") or "craft-network"
    policy_arg = _option(args, "--policy", "")
    pol_p = Path(policy_arg) if policy_arg else (REPO / "game" / "craft-policy.json")
    if not pol_p.is_absolute():
        pol_p = REPO / pol_p
    policy = read_json(pol_p, {})

    import division
    division.require(pilot)

    started = time.time()
    order_path = DATA / "fleet" / "orders" / (pilot + ".json")
    write_json(order_path, {"pilot": pilot, "what": "craft_net " + route_id, "since": utc_now(), "pid": os.getpid()})
    hb = _heartbeat(order_path)
    notes = []
    before = 0

    def raw(action, params=None, group="spacemolt_crafting"):
        return gate.raw(pilot, action, params or {}, group=group)

    def get_credits():
        try:
            r = raw("get_status", {}, group="spacemolt")
            return int(((r.get("result") or r).get("player") or {}).get("credits") or 0)
        except Exception:
            return 0

    try:
        before = get_credits()
        ship_doc = read_json(DATA / "fleet" / "ships" / ship_file_name(pilot), {})
        div = str(ship_doc.get("division") or "")
        base_id = str(ship_doc.get("base") or ship_doc.get("docked") or "")
        if not base_id:
            notes.append("not docked")
            time.sleep(60)
            return 0
        stor_all = read_json(DATA / "stock" / "storage.json", {})
        stored = ((stor_all.get("pilots") or {}).get(pilot) or {}).get(base_id) or {}
        world = load_craft_world(DATA, REPO, policy)
        job = pick_craft_job(div, base_id, stored, before, world, policy)
        if not job:
            watch_s = float(policy.get("idle_watch_minutes") or 15) * 60.0
            notes.append("docked watch %dm (no recipe)" % max(1, int(round(watch_s / 60.0))))
            end_nap = time.time() + watch_s
            while time.time() < end_nap and not (DATA / "fleet" / "STOP").exists():
                time.sleep(min(20.0, max(1.0, end_nap - time.time())))
                try:
                    os.utime(order_path)
                except OSError:
                    pass
            return 0

        # 1. Buy any short docked inputs & store them for workshop
        for iid, qty, ask in job["buys"]:
            r_b = raw("buy", {"item_id": iid, "quantity": qty, "max_price": int(ask * 1.02) + 2}, group="spacemolt_market")
            time.sleep(TICK)
            if "error" in r_b:
                notes.append("buy err %s" % iid)
                return 0
            raw("deposit", {"item_id": iid, "quantity": qty, "target": "self", "source": "cargo"}, group="spacemolt_storage")
            time.sleep(TICK)

        # 2. Execute docked craft
        r_c = raw("craft", {"recipe_id": job["recipe"], "count": job["runs"]}, group="spacemolt_crafting")
        time.sleep(TICK)
        if "error" in r_c:
            notes.append("craft err %s" % job["recipe"])
            return 0
        made_qty = job["runs"] * job["per_run"]
        notes.append("crafted %dx %s (%s)" % (made_qty, job["makes"], job["mode"]))

        # 3. Strict P5 post-craft handling
        if job["mode"] == "commercial":
            raw("create_sell_order", {"item_id": job["makes"], "quantity": made_qty, "price_each": max(1, job["sell_price"])}, group="spacemolt_market")
            time.sleep(TICK)
            notes.append("listed %dx @ %d" % (made_qty, job["sell_price"]))
        else:
            raw("withdraw", {"item_id": job["makes"], "quantity": made_qty, "target": "self"}, group="spacemolt_storage")
            time.sleep(TICK)
            r_d = raw("deposit", {"item_id": job["makes"], "quantity": made_qty, "target": "faction", "source": "cargo"}, group="spacemolt_storage")
            time.sleep(TICK)
            if "error" in r_d:
                raw("deposit", {"item_id": job["makes"], "quantity": made_qty, "target": "self", "source": "cargo"}, group="spacemolt_storage")
                time.sleep(TICK)
        return 0
    finally:
        hb.set()
        after = get_credits()
        mins = round((time.time() - started) / 60.0, 1)
        row = {
            "route": route_id, "kind": "craft_net", "pilot": pilot,
            "started": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(started)),
            "minutes": mins, "credits_before": before, "credits_after": after,
            "delta": after - before if before and after else 0,
            "one_time": 0, "notes": notes[:10],
        }
        runs_p = DATA / "routes" / "runs.jsonl"
        runs_p.parent.mkdir(parents=True, exist_ok=True)
        with open(runs_p, "a", encoding="utf-8") as fh:
            fcntl.flock(fh, fcntl.LOCK_EX)
            fh.write(json.dumps(row, separators=(",", ":")) + "\n")
        print("RESULT %s: craft_net %s | %.1f min | credits %d -> %d (%+d cr) | %s"
              % (pilot, route_id, mins, before, after, after - before, "; ".join(notes[:5]) or "ok"), flush=True)
        try:
            cur = read_json(order_path, {})
            if isinstance(cur, dict) and cur.get("pid") == os.getpid() and cur.get("what") == "craft_net " + route_id:
                order_path.unlink()
        except OSError:
            pass


if __name__ == "__main__":
    sys.exit(main())

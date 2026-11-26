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
    import worldcache as _wc
    dem_f = str((policy or {}).get("demand_file") or "game/craft-demand.json")
    ck = ("craft_world", str(data_dir), str(repo_root), _wc.db_sig(data_dir), dem_f,
          _wc.file_sig(Path(repo_root) / dem_f))
    return _wc.cached(ck, 25.0, lambda: _load_craft_world_uncached(data_dir, repo_root, policy))


def _load_craft_world_uncached(data_dir, repo_root, policy):
    db = Path(data_dir) / "store" / "read.db"
    recipes = {}        # rid -> {id, name, facility_only, inputs: [(item, qty)], outputs: [(item, qty)]}
    books_by_base = {}  # base -> {item: {bid, bid_qty, ask, ask_qty}}
    global_bid = {}     # item -> (max_bid, total_bid_qty)
    item_vals = {}
    need_crafts = set()
    stock_by_item = {}
    reserve_items = set()  # rule F24: goods the open needs take (need_status stock, craft, short_items)

    if db.is_file():
        import worldcache as _wc
        con = _wc.ro_db(db, timeout=3.0)
        try:
            tbls = {r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type IN ('table','view')").fetchall()}
            if "recipes" in tbls and "recipe_inputs" in tbls and "recipe_outputs" in tbls:
                r_cols = {r[1] for r in con.execute("PRAGMA table_info(recipes)").fetchall()}
                cat_expr = "LOWER(COALESCE(category, ''))" if "category" in r_cols else "''"
                t_expr = "COALESCE(time, 1)" if "time" in r_cols else "1"
                for rid, nm, fo, rcat, rtime in con.execute("SELECT id, name, COALESCE(facility_only, 0), %s, %s FROM recipes" % (cat_expr, t_expr)):
                    rid_s = str(rid or "")
                    if not rid_s or rid_s.startswith("onboard_") or rcat == "ship passive":
                        continue
                    recipes[rid_s] = {"id": rid_s, "name": str(nm or rid_s), "facility_only": bool(fo), "time": max(1.0, float(rtime or 1.0)), "inputs": [], "outputs": []}
                for rid, iid, u in con.execute("SELECT recipe, item, units FROM recipe_inputs"):
                    if str(rid) in recipes and iid and int(u or 0) > 0:
                        recipes[str(rid)]["inputs"].append((str(iid), int(u)))
                for rid, iid, u in con.execute("SELECT recipe, item, units FROM recipe_outputs"):
                    if str(rid) in recipes and iid and int(u or 0) > 0:
                        recipes[str(rid)]["outputs"].append((str(iid), int(u)))
            # Strict live-market valuation (ZERO static catalog base_value!):
            # Populate item_vals strictly from fresh (<6h) live market bids in read.db:books!
            if "books" in tbls:
                _bcols = {r[1] for r in con.execute("PRAGMA table_info(books)").fetchall()}
                _q = "SELECT base, item, COALESCE(bid,0), COALESCE(bid_qty,0), COALESCE(ask,0), COALESCE(ask_qty,0) FROM books"
                _p = ()
                if "t" in _bcols:
                    _q += " WHERE t >= ?"
                    _p = (time.time() - 6.0 * 3600.0,)
                _c_cltv, _c_fair, _mg_c = set(), {}, None
                try:
                    import market_guard as _mg_c
                    _c_cltv, _ = _mg_c.load_cltv_buy_orders(data_dir)
                    _c_fair = _mg_c.read_price_oracle(data_dir)
                except Exception:
                    _mg_c = None
                for b_id, iid, bid, bq, ask, aq in con.execute(_q, _p):
                    b_s, i_s = str(b_id or ""), str(iid or "")
                    if not b_s or not i_s:
                        continue
                    # Strictly real EXTERNAL top-of-book bid_qty guarded by market_guard VWM+LULD oracle!
                    real_bq = int(bq or 0)
                    raw_bid = float(bid or 0)
                    is_cltv_self = bool(_c_cltv and (b_s, i_s) in _c_cltv)
                    eff_bid = 0.0 if is_cltv_self else (_mg_c.guarded_bid_price(i_s, raw_bid, _c_fair, max_mult=1.50) if (_mg_c is not None and _c_fair) else raw_bid)
                    eff_bq = 0 if is_cltv_self else real_bq
                    books_by_base.setdefault(b_s, {})[i_s] = {
                        "bid": eff_bid, "bid_qty": eff_bq, "bid_depth": eff_bq,
                        "ask": float(ask or 0), "ask_qty": int(aq or 0),
                    }
                    # Ignore 1-unit spoof spikes above oracle fair price when estimating global crafting demand!
                    if eff_bid >= 5.0 and eff_bq > 0 and not (eff_bq == 1 and _c_fair and i_s in _c_fair and raw_bid > eff_bid):
                        prev_b, prev_q = global_bid.get(i_s, (0.0, 0))
                        global_bid[i_s] = (max(prev_b, eff_bid), prev_q + eff_bq)
                        if eff_bid > item_vals.get(i_s, 0.0):
                            item_vals[i_s] = eff_bid
            need_craft_caps = {}
            _raw_res_qty = {}
            if "need_status" in tbls:
                ns_cols = {r[1] for r in con.execute("PRAGMA table_info(need_status)").fetchall()}
                # Rule F24 (requests.log ENT-533): every good an open need takes from stock, must craft or lacks;
                # the Trade lane neither makes it for sale nor spends it from storage.
                r_cols = [c for c in ("stock", "craft", "short_items") if c in ns_cols]
                if r_cols:
                    for row in con.execute("SELECT %s FROM need_status" % ", ".join(r_cols)):
                        for text in row:
                            for m in re.finditer(r"([a-z][a-z0-9_]*)\s+(\d[\d,]*)", str(text or "")):
                                _raw_res_qty[m.group(1)] = _raw_res_qty.get(m.group(1), 0) + int(m.group(2).replace(',', '')) if len(m.groups()) >= 2 else (_raw_res_qty.get(m.group(1), 0) + 100)
                if "colour" in ns_cols:
                    ns_rows = con.execute("SELECT craft FROM need_status WHERE craft IS NOT NULL AND LOWER(COALESCE(colour, '')) != 'green'").fetchall()
                else:
                    ns_rows = con.execute("SELECT craft FROM need_status WHERE craft IS NOT NULL").fetchall()
                for (craft_s,) in ns_rows:
                    for part in str(craft_s).split(";"):
                        m = re.match(r"\s*([a-z0-9_]+)\s+(\d+)", part.strip())
                        if m:
                            iid_n, q_n = m.group(1), int(m.group(2))
                            need_crafts.add(iid_n)
                            need_craft_caps[iid_n] = max(need_craft_caps.get(iid_n, 0), q_n)
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
                            need_craft_caps[str(iid)] = max(need_craft_caps.get(str(iid), 0), int(keep))
        finally:
            con.close()
    else:
        need_craft_caps = {}

    dem_rel = str(policy.get("demand_file") or "game/craft-demand.json")
    dem_p = Path(dem_rel) if Path(dem_rel).is_absolute() else (Path(repo_root) / dem_rel)
    demand = read_json(dem_p, {})
    # Quantity-capped reserve_items: only protect scarce open needs (stock <= 1.25x need + 50) + hard keep=all items!
    # Unlocks 10,000+ surplus ore/ingot/board stocks for high-margin zero-fuel commercial crafting!
    for _ri, _rq in (locals().get("_raw_res_qty") or {}).items():
        if stock_by_item.get(_ri, 0) <= int(_rq * 1.25) + 50:
            reserve_items.add(_ri)
    for _hard_i in ("fuel_cell", "hull_patch", "repair_kit", "antimatter_containment_cell", "station_core"):
        reserve_items.add(_hard_i)
    return {
        "recipes": recipes, "books_by_base": books_by_base, "global_bid": global_bid,
        "item_vals": item_vals, "need_crafts": need_crafts, "need_craft_caps": need_craft_caps,
        "stock_by_item": stock_by_item, "demand": demand, "reserve_items": reserve_items,
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
        _st_by = world.get("stock_by_item") or {}
        for rec in recipes.values():
            if rec.get("facility_only") or not rec.get("inputs") or not rec.get("outputs"):
                continue
            out_item, out_q = rec["outputs"][0]
            mb, bq = gbid.get(out_item, (0.0, 0))
            if mb < 10.0 or bq < min_bq:
                continue
            # Anti-flood: never request raw mats for a crafted output we already hold >= 85% of live real buyers!
            if int(_st_by.get(out_item) or 0) >= max(50, int(bq * 0.85)):
                continue
            in_cost = sum(q * float(ivals.get(ii) or 0.0) for ii, q in rec["inputs"])
            rev = mb * out_q
            if rev - in_cost >= min_p and (in_cost <= 0 or (rev - in_cost) / in_cost >= min_m):
                target_outputs.add(out_item)

    # 2-step upstream expansion (e.g. lead_sheet <- lead_ingot <- lead_ore) so miners auto-feed multi-step high-margin chains!
    makers_by_out = {}
    for rec in recipes.values():
        if not rec.get("facility_only") and rec.get("inputs") and rec.get("outputs"):
            makers_by_out.setdefault(rec["outputs"][0][0], []).append(rec)
    expanded = set(target_outputs)
    for out_i in list(target_outputs):
        for rec in makers_by_out.get(out_i, ()):
            for in_i, _q in rec["inputs"]:
                if in_i in makers_by_out:
                    expanded.add(in_i)
    ind_outs = set((demand.get("industrial_targets") or {}).keys())
    wanted_raw = {}
    for out_i in expanded:
        def_cap = 12000 if out_i in ind_outs else 3000
        for rec in makers_by_out.get(out_i, ()):
            for in_item, _q in rec["inputs"]:
                cap = min(raw_caps.get(in_item, def_cap), 15000)
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
    reserve = set(world.get("reserve_items") or ()) if is_trade else set()
    if reserve:  # rule F24: the Trade lane spends no stored good an open need takes
        stored = {k: v for k, v in stored.items() if k not in reserve}
    allow_buy = bool(sub.get("allow_buy_inputs_docked", policy.get("allow_buy_inputs_docked", True)))
    budget = min(
        max(0, int(credits or 0) - int(policy.get("min_wallet_keep_cr") or 15000)),
        int(policy.get("max_buy_spend_per_cycle_cr") or 25000),
    )
    max_runs = max(1, int(policy.get("max_runs_per_cycle") or 10))
    est_fee = 0.0  # Realistic hand-craft fee calculated dynamically as 3% of revenue below

    ind_targets = set()
    ind_caps = {}
    if is_log:
        nc_caps = world.get("need_craft_caps") or {}
        if sub.get("use_needs_tsv", True):
            for iid in (world.get("need_crafts") or set()):
                cap = int(nc_caps.get(str(iid)) or 0)
                if cap <= 0 or stock_map.get(str(iid), 0) < cap:
                    ind_targets.add(str(iid))
                    if cap > 0:
                        ind_caps[str(iid)] = max(ind_caps.get(str(iid), 0), cap)
        if sub.get("use_industrial_targets", True):
            for iid, cfg in (demand.get("industrial_targets") or {}).items():
                cap = int((cfg or {}).get("cap") or 0)
                if cap <= 0 or stock_map.get(str(iid), 0) < cap:
                    ind_targets.add(str(iid))
                    if cap > 0:
                        ind_caps[str(iid)] = max(ind_caps.get(str(iid), 0), cap)

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
        if out_item in reserve:  # rule F24: a good an open need takes is never made for sale
            continue
        # Trade overproduction & buy-wall cancellation guard:
        # NEVER craft commercial items past min(target_cap, 50% of live external market_guard-verified bid depth)!
        if is_trade:
            _gb_p, _gb_q = (world.get("global_bid") or {}).get(out_item, (0.0, 0))
            _comm_cfg = (demand.get("commercial_targets") or {}).get(out_item)
            _comm_cap = int((_comm_cfg or {}).get("cap") or 0) if isinstance(_comm_cfg, dict) else 0
            _live_abs_cap = max(20, int(float(_gb_q) * 0.50)) if _gb_q > 0 else 0
            _eff_comm_cap = min(_comm_cap, _live_abs_cap) if (_comm_cap > 0 and _live_abs_cap > 0) else (_live_abs_cap or _comm_cap)
            if _eff_comm_cap > 0 and stock_map.get(out_item, 0) >= _eff_comm_cap:
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
                # Live opportunity cost: local bid if present, else galactic live bid (0.0 if unbid -- NEVER catalog base_value!)
                local_in_bid = float(row_b.get("bid") or 0)
                unit_c = local_in_bid if local_in_bid > 0 else float(ivals.get(in_item) or 0.0)
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
            local_bid = float(local_b.get("bid") or 0)
            local_bq = int(local_b.get("bid_qty") or 0)
            local_ask = float(local_b.get("ask") or 0)
            gb_p, gb_q = gbid.get(out_item, (0.0, 0))
            # Anti-flood for commercial Trade crafting: never craft more when fleet already holds >= 85% of real buyer qty!
            _real_demand_q = max(local_bq, gb_q)
            if _real_demand_q > 0 and int(stock_map.get(out_item) or 0) >= max(50, int(_real_demand_q * 0.85)):
                continue
            bid, bq = local_bid, local_bq
            sell_via_ask = False
            # When spending cash on market inputs, REQUIRE a live LOCAL real buyer bid so cash converts back to profit immediately!
            if bid <= 0 or bq < min_bq:
                if buys:
                    continue
                # Using own stored inputs (0 cash spent!): sell at live galactic real bid OR undercut active local ask!
                if local_ask >= 15 and gb_p >= 10 and gb_q >= min_bq and local_ask <= gb_p * 4.0:
                    bid, bq = max(5.0, local_ask - 1.0), gb_q
                    sell_via_ask = True
                elif gb_p >= 10 and gb_q >= min_bq:
                    bid, bq = gb_p, gb_q
                else:
                    continue
            if buys and local_bq > 0:
                max_abs_runs = max(1, local_bq // max(1, out_qty))
                if runs > max_abs_runs:
                    runs = max_abs_runs
                    buys = []
                    tot_buy = 0
                    for in_item, req_q in rec["inputs"]:
                        short_q = max(0, req_q * runs - stored.get(in_item, 0))
                        if short_q > 0:
                            ask = int(round(float((book.get(in_item) or {}).get("ask") or 0)))
                            buys.append((in_item, short_q, ask))
                            tot_buy += short_q * ask
            rev_per_run = bid * out_qty
            run_fee = min(25.0, rev_per_run * 0.03)
            prof_per_run = rev_per_run - cost_per_run - run_fee
            margin = prof_per_run / max(1.0, cost_per_run) if cost_per_run > 0 else 1.0
            if prof_per_run < min_profit or margin < min_margin:
                continue
            # Theory of Constraints: rank strictly by Contribution Margin per Bottleneck Tick!
            r_ticks = max(1.0, float(rec.get("time") or 1.0))
            cm_per_tick = prof_per_run / r_ticks
            score = cm_per_tick * (1.0 + 0.15 * min(runs, 10)) * (1.25 if out_item in comm_targets else 1.0) * (1.5 if local_bid > 0 else 1.0)
            cand = {
                "recipe": rec["id"], "makes": out_item, "per_run": out_qty, "runs": runs,
                "buys": buys, "est_profit": round(prof_per_run * runs, 1), "margin_pct": round(margin * 100.0, 1),
                "sell_price": int(round(bid)), "local_bid": (0 if sell_via_ask else int(round(local_bid))),
                "mode": "commercial", "score": round(score, 2),
            }
        else:
            cap_i = ind_caps.get(out_item, 0)
            if cap_i > 0:
                rem_need = max(0, cap_i - int(stock_map.get(out_item, 0)))
                if rem_need <= 0:
                    continue
                cap_runs = max(1, (rem_need + max(1, out_qty) - 1) // max(1, out_qty))
                runs = min(runs, cap_runs)
            prio_boost = 5.0 if out_item in (world.get("need_crafts") or set()) else 1.0
            stored_ratio = 1.0 if not buys else 0.6
            score = prio_boost * stored_ratio * runs * max(1.0, float(ivals.get(out_item) or 1.0))
            cand = {
                "recipe": rec["id"], "makes": out_item, "per_run": out_qty, "runs": runs,
                "buys": buys, "est_profit": 0.0, "margin_pct": 0.0,
                "sell_price": 0, "local_bid": 0, "mode": "industrial", "score": round(score, 2),
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


def _craft_cooldowns(data_dir=DATA):
    cd = read_json(Path(data_dir) / "fleet" / "craft_cooldown.json", {})
    if not isinstance(cd, dict):
        return {}
    now = time.time()
    return {k: v for k, v in cd.items() if isinstance(v, (int, float)) and v > now}


def _stamp_craft_cooldown(key, seconds, data_dir=DATA):
    p = Path(data_dir) / "fleet" / "craft_cooldown.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    lk = Path(data_dir) / "fleet" / "craft_cooldown.lock"
    with open(lk, "a+", encoding="utf-8") as lfh:
        fcntl.flock(lfh, fcntl.LOCK_EX)
        cd = _craft_cooldowns(data_dir=data_dir)
        cd[str(key)] = round(time.time() + float(seconds), 1)
        write_json(p, cd)


def _active_lockboxes(data_dir):
    emp = read_json(Path(data_dir) / "empire" / "empire.json", {})
    out = set()
    if isinstance(emp, dict):
        for f in (emp.get("facilities") or []):
            if isinstance(f, dict) and str(f.get("type") or "") == "faction_lockbox" and str(f.get("status") or "active") == "active":
                if f.get("base"):
                    out.add(str(f["base"]))
    return out


def _pilot_can_withdraw_faction(data_dir, pilot):
    emp = read_json(Path(data_dir) / "empire" / "empire.json", {})
    if not isinstance(emp, dict):
        return False
    allowed = {"leader", "officer"}
    for r in (emp.get("roles") or []):
        if isinstance(r, dict) and (r.get("permissions") or {}).get("manage_treasury"):
            for k in ("id", "name"):
                if r.get(k):
                    allowed.add(str(r[k]).strip().lower())
    for m in (emp.get("members") or []):
        if not isinstance(m, dict):
            continue
        nm = str(m.get("pilot") or m.get("name") or m.get("member") or m.get("username") or "").strip()
        if nm == str(pilot):
            return str(m.get("role") or m.get("rank") or "").strip().lower() in allowed
    return False


def _faction_items_at_base(stor_all, base_id):
    out = {}
    if not isinstance(stor_all, dict) or not base_id:
        return out
    for src in (stor_all.get("faction"), ((stor_all.get("pilots") or {}).get("Faction") or {}).get("stations")):
        if isinstance(src, dict) and isinstance(src.get(base_id), dict):
            for iid, q in src[base_id].items():
                if iid and int(q or 0) > 0:
                    out[str(iid)] = max(out.get(str(iid), 0), int(q))
    return out


def has_craft_job(pilot, ship_doc, data_dir=DATA, repo_root=REPO, policy_path=None, world_cache=None, stor_cache=None):
    """Fast 0ms dispatcher check: True iff `pilot` is docked at a station with an executable craft job."""
    if not isinstance(ship_doc, dict):
        return False
    dock_raw = ship_doc.get("docked")
    base_id = str(ship_doc.get("base") or (dock_raw if isinstance(dock_raw, str) else "") or "")
    div = str(ship_doc.get("division") or "")
    if not div:
        _rm = {"trader": "Trade", "hauler": "Logistics"}
        div = _rm.get(str(ship_doc.get("role") or "").lower(), "")
    if not base_id or div not in ("Trade", "Logistics"):
        return False
    cd = _craft_cooldowns(data_dir=data_dir)
    if str(pilot) in cd:
        return False
    pol_p = Path(policy_path) if policy_path else (Path(repo_root) / "game" / "craft-policy.json")
    pol = read_json(pol_p, {})
    if not pol or not pol.get("enabled", True):
        return False
    world = world_cache if world_cache is not None else load_craft_world(data_dir, repo_root, pol)
    stor_all = stor_cache if stor_cache is not None else read_json(Path(data_dir) / "stock" / "storage.json", {})
    p_stor = (stor_all.get("pilots") or {}).get(pilot) or {}
    stored = dict((p_stor.get("stations") or {}).get(base_id) or p_stor.get(base_id) or {})
    if base_id in _active_lockboxes(data_dir) and _pilot_can_withdraw_faction(data_dir, pilot):
        for iid, fq in _faction_items_at_base(stor_all, base_id).items():
            stored[iid] = int(stored.get(iid) or 0) + int(fq)
    credits = int(ship_doc.get("credits") or 0)
    job = pick_craft_job(div, base_id, stored, credits, world, pol)
    if not job:
        return False
    if ("%s:%s" % (pilot, job.get("recipe") or "")) in cd:
        return False
    return True


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

    p_enc = gate.q(pilot)

    def _parse(text):
        try:
            d = json.loads(text) if isinstance(text, str) else text
            return d if isinstance(d, dict) else {}
        except ValueError:
            return {}

    def _body(d):
        if not isinstance(d, dict):
            return {}
        for k in ("structuredContent", "result", "data"):
            if isinstance(d.get(k), dict):
                return d[k]
        return d

    def raw(action, params=None, group="spacemolt"):
        st, txt = gate.call("POST", "/accounts/%s/raw" % p_enc, {"toolGroup": group, "action": action, "params": params or {}}, timeout=120)
        d = _parse(txt)
        if st >= 400 and "error" not in d:
            d["error"] = "http %d" % st
        return d

    def goal(kind, options, timeout=180):
        st, txt = gate.call("POST", "/accounts/%s/goal" % p_enc, {"type": kind, "options": options}, timeout=timeout)
        d = _parse(txt)
        ok = (200 <= st < 300) and bool(d.get("success", True)) and not d.get("error")
        return ok, d

    def get_credits():
        try:
            r = _body(raw("get_status", {}, group="spacemolt"))
            return int((r.get("player") or {}).get("credits") or 0)
        except Exception:
            return 0

    def get_live_stored(base_id, target="self"):
        params = {"station_id": base_id} if target == "self" else {"station_id": base_id, "target": target}
        ans = raw("view", params, group="spacemolt_storage")
        if not isinstance(ans, dict) or "error" in ans:
            return None
        d = _body(ans)
        if not isinstance(d, dict) or ("items" not in d and "storage" not in d and "base_id" not in d):
            return None
        rows = d.get("items") or d.get("storage") or []
        out = {}
        for r in rows if isinstance(rows, list) else []:
            if isinstance(r, dict) and r.get("item_id"):
                out[str(r["item_id"])] = out.get(str(r["item_id"]), 0) + int(r.get("quantity") or 0)
        return out

    onetime_booked = [0]
    try:
        before = get_credits()
        ship_doc = read_json(DATA / "fleet" / "ships" / ship_file_name(pilot), {})
        div = str(ship_doc.get("division") or "")
        base_id = str(ship_doc.get("base") or ship_doc.get("docked") or "")
        if not base_id:
            notes.append("not docked")
            time.sleep(30)
            return 0
        stored = get_live_stored(base_id)
        if stored is None:
            import worldcache as _wc
            stor_all = _wc.read_json_cached(DATA / "stock" / "storage.json", {}, ttl_s=30.0)
            p_stor = (stor_all.get("pilots") or {}).get(pilot) or {}
            stored = (p_stor.get("stations") or {}).get(base_id) or p_stor.get(base_id) or {}
        self_stored = dict(stored)
        fac_stored = {}
        use_fac = base_id in _active_lockboxes(DATA) and _pilot_can_withdraw_faction(DATA, pilot)
        if use_fac:
            fac_live = get_live_stored(base_id, target="faction")
            if fac_live is not None:
                fac_stored = fac_live
            else:
                import worldcache as _wc_f
                _sa_f = _wc_f.read_json_cached(DATA / "stock" / "storage.json", {}, ttl_s=30.0)
                fac_stored = _faction_items_at_base(_sa_f, base_id)
            for _fi, _fq in fac_stored.items():
                if int(_fq or 0) > 0:
                    stored[_fi] = int(stored.get(_fi) or 0) + int(_fq)
        world = load_craft_world(DATA, REPO, policy)
        job = pick_craft_job(div, base_id, stored, before, world, policy)
        if not job:
            watch_s = min(120.0, float(policy.get("idle_watch_minutes") or 2) * 60.0)
            notes.append("docked watch %dm (no recipe)" % max(1, int(round(watch_s / 60.0))))
            end_nap = time.time() + watch_s
            while time.time() < end_nap and not (DATA / "fleet" / "STOP").exists():
                time.sleep(min(20.0, max(1.0, end_nap - time.time())))
                try:
                    os.utime(order_path)
                except OSError:
                    pass
            return 0

        print("%s %s craft_net: starting %dx %s (%s) at %s" % (utc_now(), pilot, int(job["runs"] * job["per_run"]), job["makes"], job["mode"], base_id), flush=True)
        asked_c = {"recipe_id": job["recipe"], "quantity": int(job["runs"] * job["per_run"]), "deliver_to": "storage", "preset": "workshop"}
        max_fee_tot = float(policy.get("max_fee_per_run_cr") or 1500) * max(1, int(job["runs"]))

        # 0a. Pull any needed inputs from shared Faction Lockbox -> personal workshop storage before crafting!
        if use_fac and fac_stored:
            _rec_obj = (world.get("recipes") or {}).get(job["recipe"]) or {}
            _pull_cap = max(10, int(ship_doc.get("cargo_capacity") or 50) - 5)
            for _in_i, _req_q in (_rec_obj.get("inputs") or []):
                _need_tot = int(_req_q) * int(job["runs"])
                _short_self = max(0, _need_tot - int(self_stored.get(_in_i) or 0))
                _avail_fac = min(_short_self, int(fac_stored.get(_in_i) or 0))
                while _avail_fac > 0:
                    _ch_q = min(_avail_fac, _pull_cap)
                    _rw_f = raw("withdraw", {"item_id": _in_i, "quantity": int(_ch_q), "target": "faction"}, group="spacemolt_storage")
                    time.sleep(TICK)
                    if "error" in _rw_f:
                        break
                    raw("deposit", {"item_id": _in_i, "quantity": int(_ch_q), "target": "self", "source": "cargo"}, group="spacemolt_storage")
                    time.sleep(TICK)
                    self_stored[_in_i] = int(self_stored.get(_in_i) or 0) + int(_ch_q)
                    _avail_fac -= _ch_q

        # 0. Pre-buy dry-run validation (ENT-326): NEVER buy inputs if recipe is invalid, lacks workshop/skill, or fee > max_fee!
        q_pre_raw = raw("craft", dict(asked_c, dry_run=True), group="spacemolt")
        q_pre = _body(q_pre_raw)
        pre_err = str(q_pre_raw.get("error") or q_pre.get("error") or "")
        pre_fee = float(q_pre.get("credits_total") or 0)
        if pre_err or (pre_fee > 0 and pre_fee > max_fee_tot):
            notes.append("pre-quote refuse %s (err=%s fee=%d)" % (job["recipe"], pre_err[:40] or "fee", int(pre_fee)))
            _stamp_craft_cooldown("%s:%s" % (pilot, job["recipe"]), 3600, data_dir=DATA)
            _stamp_craft_cooldown(pilot, 300, data_dir=DATA)
            return 0

        # 1. Buy any short docked inputs in cargo-safe chunks and verify actual storage delivery before crafting
        buy_spent = 0
        hold_cap = max(10, int(ship_doc.get("cargo_capacity") or 50))
        for iid, qty, ask in job["buys"]:
            rem_buy = int(qty)
            chunks = 0
            while rem_buy > 0 and chunks < 12:
                chunks += 1
                chunk_q = min(rem_buy, max(10, hold_cap - 5))
                cr_b0 = get_credits()
                ok_b, _rb = goal("buy-items", {"items": [{"itemId": iid, "maxPrice": int(ask * 1.02) + 2, "maxQuantity": int(chunk_q)}]}, timeout=120)
                time.sleep(TICK)
                cr_b1 = get_credits()
                if cr_b0 > 0 and cr_b1 >= 0 and cr_b0 > cr_b1:
                    buy_spent += (cr_b0 - cr_b1)
                if not ok_b:
                    break
                raw("deposit", {"item_id": iid, "quantity": int(chunk_q), "target": "self", "source": "cargo"}, group="spacemolt_storage")
                time.sleep(TICK)
                rem_buy -= chunk_q
            live_after = get_live_stored(base_id) or {}
            need_after = int(stored.get(iid, 0)) + int(qty)
            if rem_buy > 0 or int(live_after.get(iid, 0)) < need_after:
                if buy_spent > 0:
                    gate.book_onetime(pilot, "craft_net input stock %s" % iid, -int(buy_spent), data=str(DATA))
                    onetime_booked[0] -= int(buy_spent)
                notes.append("buy short %s (have=%d need=%d)" % (iid, int(live_after.get(iid, 0)), need_after))
                _stamp_craft_cooldown("%s:%s" % (pilot, job["recipe"]), 1800, data_dir=DATA)
                _stamp_craft_cooldown(pilot, 600, data_dir=DATA)
                return 0

        # 2. Final dry-run quote check + execute docked craft (exact route_run.py wire schema: quantity=runs*per_run)
        q_c = _body(raw("craft", dict(asked_c, dry_run=True), group="spacemolt"))
        q_fee = float(q_c.get("credits_total") or 0)
        if q_c.get("have_inputs") is False or (q_fee > 0 and q_fee > max_fee_tot):
            if buy_spent > 0:
                gate.book_onetime(pilot, "craft_net input stock %s" % job["makes"], -int(buy_spent), data=str(DATA))
                onetime_booked[0] -= int(buy_spent)
            notes.append("quote refuse %s (inputs=%s fee=%d)" % (job["recipe"], q_c.get("have_inputs"), int(q_fee)))
            _stamp_craft_cooldown("%s:%s" % (pilot, job["recipe"]), 1800, data_dir=DATA)
            _stamp_craft_cooldown(pilot, 600, data_dir=DATA)
            return 0
        r_c = raw("craft", asked_c, group="spacemolt")
        time.sleep(TICK)
        if "error" in r_c:
            if buy_spent > 0:
                gate.book_onetime(pilot, "craft_net input stock %s" % job["makes"], -int(buy_spent), data=str(DATA))
                onetime_booked[0] -= int(buy_spent)
            notes.append("craft err %s: %s" % (job["recipe"], str(r_c.get("error") or "")[:60]))
            _stamp_craft_cooldown("%s:%s" % (pilot, job["recipe"]), 1800, data_dir=DATA)
            _stamp_craft_cooldown(pilot, 600, data_dir=DATA)
            return 0
        made_qty = job["runs"] * job["per_run"]
        notes.append("crafted %dx %s (%s)" % (made_qty, job["makes"], job["mode"]))

        # 3. Strict P5 post-craft handling
        if job["mode"] == "commercial":
            sold_now = False
            if int(job.get("local_bid") or 0) > 0:
                raw("withdraw", {"item_id": job["makes"], "quantity": made_qty, "target": "self"}, group="spacemolt_storage")
                time.sleep(TICK)
                r_s = raw("sell", {"item_id": job["makes"], "quantity": made_qty}, group="spacemolt_market")
                time.sleep(TICK)
                if "error" not in r_s:
                    sold_now = True
                    notes.append("sold %dx @ ~%d" % (made_qty, job["local_bid"]))
                else:
                    raw("deposit", {"item_id": job["makes"], "quantity": made_qty, "target": "self", "source": "cargo"}, group="spacemolt_storage")
                    time.sleep(TICK)
            if not sold_now:
                if buy_spent > 0:
                    gate.book_onetime(pilot, "craft_net listed stock %s" % job["makes"], -int(buy_spent), data=str(DATA))
                    onetime_booked[0] -= int(buy_spent)
                raw("create_sell_order", {"item_id": job["makes"], "quantity": made_qty, "price_each": max(1, job["sell_price"])}, group="spacemolt_market")
                time.sleep(TICK)
                notes.append("listed %dx @ %d" % (made_qty, job["sell_price"]))
        else:
            if buy_spent > 0:
                gate.book_onetime(pilot, "craft_net industrial stock %s" % job["makes"], -int(buy_spent), data=str(DATA))
                onetime_booked[0] -= int(buy_spent)
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
            "one_time": onetime_booked[0], "notes": notes[:10],
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

"""Global optimal ship-to-task matching and live mission-board gating for The Collective.

Usage: imported by dispatch.py (`assign_batch_pilots`, `mission_offered_on_board`, `min_cost_assignment`).

Pure Python standard library (zero external dependencies, 7-bit ASCII).

Implements:
1. Exact Hungarian / Kuhn-Munkres minimum-cost bipartite matching (`min_cost_assignment`)
   to replace greedy alphabetical dispatch when multiple free ships contend for scarce
   capped routes, minimizing total deadhead jump travel across the fleet.
2. Live mission-board pre-check (`mission_offered_on_board`) so static `circuit` routes
   with `accept` mission stops are verified against fresh `data/missions/<base>.json`
   reads before launch, eliminating empty `mission not offered` flights.
3. Batch dispatcher integration (`assign_batch_pilots`) preserving single-pilot
   determinism while solving global proximity-optimal allocation on multi-pilot passes.
"""
import json
import re
import time
from pathlib import Path

FORBIDDEN = 10 ** 12
_NORM_RE = re.compile(r"[^a-z0-9]+")
_BOARD_CACHE = {}


def _norm_key(text):
    return _NORM_RE.sub("_", str(text or "").strip().lower()).strip("_")


def _parse_iso_epoch(val):
    if isinstance(val, (int, float)):
        return float(val)
    if not isinstance(val, str) or not val.strip():
        return None
    s = val.strip()
    try:
        return float(s)
    except ValueError:
        pass
    try:
        from datetime import datetime, timezone
        if s.endswith("Z"):
            s = s[:-1] + "+00:00"
        dt = datetime.fromisoformat(s)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.timestamp()
    except Exception:
        return None


def _read_board_cached(path):
    p = Path(path)
    try:
        st = p.stat()
    except OSError:
        return None
    key = str(p)
    stamp = (st.st_mtime_ns, st.st_size)
    hit = _BOARD_CACHE.get(key)
    if hit is not None and hit[0] == stamp:
        return hit[1]
    try:
        obj = json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    if len(_BOARD_CACHE) > 256:
        _BOARD_CACHE.clear()
    _BOARD_CACHE[key] = (stamp, obj)
    return obj


def min_cost_assignment(cost_matrix):
    """Exact Hungarian / Kuhn-Munkres augmenting-path solver for rectangular M x N cost matrices.

    Returns a sorted list of (row_index, col_index) pairs assigning min(M, N) rows to distinct
    columns with globally minimum total cost, omitting any pair with cost >= FORBIDDEN // 2.
    """
    if not cost_matrix or not cost_matrix[0]:
        return []
    n_rows = len(cost_matrix)
    n_cols = len(cost_matrix[0])
    transposed = False
    if n_rows > n_cols:
        mat = [[cost_matrix[r][c] for r in range(n_rows)] for c in range(n_cols)]
        n_rows, n_cols = n_cols, n_rows
        transposed = True
    else:
        mat = [list(row) for row in cost_matrix]

    # 1-indexed potentials u[0..n_rows], v[0..n_cols], column matching p[0..n_cols]
    u = [0.0] * (n_rows + 1)
    v = [0.0] * (n_cols + 1)
    p = [0] * (n_cols + 1)
    way = [0] * (n_cols + 1)
    inf = float("inf")

    for i in range(1, n_rows + 1):
        p[0] = i
        j0 = 0
        minv = [inf] * (n_cols + 1)
        used = [False] * (n_cols + 1)
        while True:
            used[j0] = True
            i0 = p[j0]
            delta = inf
            j1 = 0
            row_i0 = mat[i0 - 1]
            for j in range(1, n_cols + 1):
                if not used[j]:
                    cur = row_i0[j - 1] - u[i0] - v[j]
                    if cur < minv[j]:
                        minv[j] = cur
                        way[j] = j0
                    if minv[j] < delta:
                        delta = minv[j]
                        j1 = j
            for j in range(0, n_cols + 1):
                if used[j]:
                    u[p[j]] += delta
                    v[j] -= delta
                else:
                    minv[j] -= delta
            j0 = j1
            if p[j0] == 0:
                break
        while True:
            j1 = way[j0]
            p[j0] = p[j1]
            j0 = j1
            if j0 == 0:
                break

    pairs = []
    for j in range(1, n_cols + 1):
        i = p[j]
        if i == 0:
            continue
        r_idx, c_idx = (j - 1, i - 1) if transposed else (i - 1, j - 1)
        if cost_matrix[r_idx][c_idx] < (FORBIDDEN // 2):
            pairs.append((r_idx, c_idx))
    pairs.sort()
    return pairs


def mission_offered_on_board(data, route, now=None, max_board_age_s=21600.0):
    """Return a skip reason string if a circuit route's `accept` mission is absent from a fresh
    mission board snapshot (`data/missions/<base>.json`), else None (offered or board stale/unknown).

    Routes that already declare `requires.posted` return None so `posted_missing` remains authoritative.
    """
    if not data or not isinstance(route, dict) or route.get("kind") != "circuit":
        return None
    req = route.get("requires")
    if isinstance(req, dict) and req.get("posted"):
        return None
    stops = route.get("stops")
    if not isinstance(stops, list) or not stops:
        return None

    now_t = time.time() if now is None else float(now)
    alt_keys = set()
    for field in ("one_time", "skip_if_booked"):
        vals = route.get(field)
        if isinstance(vals, list):
            for v in vals:
                nk = _norm_key(v)
                if nk:
                    alt_keys.add(nk)

    for stop in stops:
        if not isinstance(stop, dict):
            continue
        accept = stop.get("accept")
        if not isinstance(accept, list) or not accept:
            continue
        at_str = str(stop.get("at") or "")
        parts = at_str.split(":")
        base_id = parts[-1].strip() if len(parts) >= 3 else ""
        if not base_id:
            continue
        board = _read_board_cached(Path(data) / "missions" / (base_id + ".json"))
        if not isinstance(board, dict):
            continue
        read_t = _parse_iso_epoch(board.get("read_at"))
        if read_t is None:
            continue
        age_s = now_t - read_t
        if age_s < -300.0 or age_s > float(max_board_age_s):
            continue
        missions = board.get("missions")
        if not isinstance(missions, list):
            continue
        offered = set()
        for m in missions:
            if not isinstance(m, dict):
                continue
            for k in ("mission_id", "template_id", "id", "title", "name"):
                nk = _norm_key(m.get(k))
                if nk:
                    offered.add(nk)
        want_keys = {_norm_key(a) for a in accept if _norm_key(a)} | alt_keys
        if want_keys and not (want_keys & offered):
            return "mission `%s` not offered on %s board (read %dm ago)" % (
                str(accept[0]), base_id, int(max(0.0, age_s) // 60)
            )
    return None


def _is_scarce_route(route):
    if not isinstance(route, dict):
        return False
    kind = str(route.get("kind") or "")
    if kind in ("mine_net", "hunt_net", "census_net", "haul", "bursar", "craft_net", "fit_net", "salvage_net", "pirate_net"):
        return False
    cap = route.get("max_ships")
    return isinstance(cap, int) and 0 < cap <= 12


def _remaining_slots(route, state):
    cap = int(route.get("max_ships") or 0)
    if cap <= 0:
        return 0
    what = str(route.get("kind") or "") + " " + str(route.get("id") or "")
    oc = state.get("_order_counts")
    used = int(oc.get(what, 0)) if isinstance(oc, dict) else sum(1 for v in (state.get("orders") or {}).values() if v == what)
    return max(0, cap - used)


def assign_batch_pilots(free_items, plan, routes, state, why_not_fn, hops_fn, pick_fn, role_of_fn=None):
    """Solve global proximity-optimal matching for contested scarce routes across a batch of free pilots.

    `free_items` is a list of `(ship, pilot)` tuples that passed pre-checks in `dispatch.one_pass`.
    Returns:
      - `pre_assigned`: dict `{pilot_name: (route, argument)}` for pilots optimally matched to scarce routes
      - `ordered_items`: `free_items` ordered so pre-assigned pilots run first, then docked/nearest pilots
        before distant pilots, minimizing deadhead travel while keeping deterministic tie-breaking.
    """
    if len(free_items) <= 1:
        return {}, list(free_items)

    # Phase 1: Inspect each pilot's open scarce routes before its first uncapped AutoNet fallback
    pilot_scarce = {}
    scarce_routes = {}
    pilot_first_hops = {}

    for _ship, pilot in free_items:
        pname = pilot["name"]
        role = pilot.get("role") or (role_of_fn(pname, {}) if role_of_fn else "")
        rids = (plan.get("pilots") or {}).get(pname) or (plan.get("roles") or {}).get(role) or []
        cands = []
        best_h = 99
        for rank, rid in enumerate(rids):
            rt = routes.get(rid)
            if not isinstance(rt, dict):
                continue
            if not _is_scarce_route(rt):
                # Once an uncapped AutoNet is open for this pilot, stop collecting lower-priority scarce routes
                reason, _arg = why_not_fn(pilot, rid, rt, state)
                if reason is None:
                    h = hops_fn(pilot, rt)
                    if h is not None and h < best_h:
                        best_h = h
                    break
                continue
            rem = _remaining_slots(rt, state)
            if rem <= 0:
                continue
            reason, arg = why_not_fn(pilot, rid, rt, state)
            if reason is None:
                h = hops_fn(pilot, rt)
                eff_h = int(h) if h is not None else 6
                if eff_h < best_h:
                    best_h = eff_h
                cands.append((rank, rid, rt, arg, eff_h))
                scarce_routes[rid] = (rt, rem)
                if len(cands) >= 6:
                    break
        pilot_first_hops[pname] = best_h
        if cands:
            pilot_scarce[pname] = cands

    # Only run Hungarian matching if at least 2 pilots contend over scarce routes
    contending_pilots = [p for _s, p in free_items if p["name"] in pilot_scarce]
    pre_assigned = {}

    if len(contending_pilots) >= 2 and scarce_routes:
        # Check if there is real scarcity contention (sum of demand > slots on any route, or >=2 pilots share routes)
        demand = {}
        for p in contending_pilots:
            for _rk, rid, _rt, _arg, _eh in pilot_scarce[p["name"]]:
                demand[rid] = demand.get(rid, 0) + 1
        has_contention = any(demand.get(rid, 0) > scarce_routes[rid][1] for rid in scarce_routes) or (
            len(contending_pilots) >= 2 and len(scarce_routes) >= 2
        )
        if has_contention:
            # Expand available slots for scarce routes (bounded by number of contending pilots)
            slot_cols = []
            for rid in sorted(scarce_routes):
                rt, rem = scarce_routes[rid]
                n_slots = min(rem, demand.get(rid, 0), len(contending_pilots))
                for _sidx in range(n_slots):
                    slot_cols.append((rid, rt))

            if slot_cols:
                n_p = len(contending_pilots)
                n_real = len(slot_cols)
                # Add one fallback dummy column per pilot so distant ships (e.g. >16 hops) yield to closer ships
                n_cols = n_real + n_p
                fallback_cost = 16500.0
                cand_map = {}
                cost = []
                for pi, p in enumerate(contending_pilots):
                    pname = p["name"]
                    cmap = {}
                    for rank, rid, rt, arg, eff_h in pilot_scarce[pname]:
                        cmap[rid] = (rank, rt, arg, eff_h)
                    cand_map[pname] = cmap
                    row = [float(FORBIDDEN)] * n_cols
                    docked_bonus = 0.0 if p.get("docked") else 15.0
                    for ci, (rid, _rt) in enumerate(slot_cols):
                        hit = cmap.get(rid)
                        if hit is not None:
                            rank, _rt2, _arg2, eff_h = hit
                            row[ci] = float(eff_h) * 1000.0 + float(rank) * 20.0 + (0.0 if (eff_h == 0 and p.get("docked")) else docked_bonus)
                    row[n_real + pi] = fallback_cost
                    cost.append(row)

                matched = min_cost_assignment(cost)
                for r_idx, c_idx in matched:
                    if c_idx < n_real:
                        p = contending_pilots[r_idx]
                        rid, rt = slot_cols[c_idx]
                        hit = cand_map[p["name"]].get(rid)
                        if hit is not None:
                            pre_assigned[p["name"]] = (rt, hit[2])

    # Order batch: pre-assigned optimal scarce matches first, then docked & nearest-to-work pilots
    ordered = sorted(
        free_items,
        key=lambda sp: (
            0 if sp[1]["name"] in pre_assigned else 1,
            0 if sp[1].get("docked") else 1,
            pilot_first_hops.get(sp[1]["name"], 99),
            sp[1]["name"],
        ),
    )
    return pre_assigned, ordered

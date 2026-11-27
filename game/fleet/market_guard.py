#!/usr/bin/env python3
"""Open-Market Anti-Manipulation & Manipulation-Resistant Fair-Price Engine (`market_guard.py`).

Defends The Collective against AI-vs-AI open-market exploits without static price ceilings
or artificial low escrow caps:
  1. Volume-Weighted Median (VWM) across independent stations (excludes CLTV's own buy orders
     and naturally discards single-station spoof spikes and 1-cr trash-bid depth traps).
  2. Rolling Historical LULD (Limit Up / Limit Down) EWMA/TWAP Oracle (`data/fleet/price_oracle.json`):
     freely tracks genuine multi-hour market shifts (+/- 25%/h band) while rejecting sudden
     flash-pumps and wash spikes.
  3. Bait-Ask / Wide-Spread Detector: refuses to anchor buy ceilings to spoofed asks
     (e.g., 1,000 cr ask on an 11 cr ore).
  4. Mirage Arbitrage Scam Guard (EVE Online margin-trading defense): rejects arbitrage buys
     whose origin ask is wildly above cross-station fair value (so even if a fake destination
     buy-wall vanishes mid-flight, we never overpay for a worthless brick).
  5. Same-Station CLTV Anti-Self-Outbid & Anti-Wash-Trade Helpers.

Usage:
  Imported by game/fleet/bursar.py and game/fleet/haul.py (stdlib only, ASCII only).
"""
import fcntl
import json
import os
import sqlite3
import time
from pathlib import Path


def _read_json(path, default=None):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8", errors="replace"))
    except (OSError, ValueError):
        return {} if default is None else default


def _write_json(path, obj):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + ".%d.tmp" % os.getpid())
    tmp.write_text(json.dumps(obj, separators=(",", ":"), sort_keys=True), encoding="ascii")
    os.replace(tmp, p)


def load_cltv_buy_orders(data_dir, now_t=None, ttl_s=21600):
    """Return (by_base_item: set[(base, item)], by_base_pilots: dict[(base, item), set[pilot]])."""
    now_t = time.time() if now_t is None else float(now_t)
    by_bi = set()
    by_bp = {}
    doc = _read_json(Path(data_dir) / "fleet" / "bursar_buys.json", {})
    entries = doc.get("entries") if isinstance(doc, dict) and isinstance(doc.get("entries"), dict) else {}
    for pilot, bases in entries.items():
        if not isinstance(bases, dict):
            continue
        for b_id, rec in bases.items():
            if not isinstance(rec, dict) or (now_t - float(rec.get("at") or 0)) > ttl_s:
                continue
            for iid, q in (rec.get("items") or {}).items():
                if iid and int(q or 0) > 0:
                    k = (str(b_id), str(iid))
                    by_bi.add(k)
                    by_bp.setdefault(k, set()).add(str(pilot))
    return by_bi, by_bp


def load_cltv_buy_qty(data_dir, now_t=None, ttl_s=21600):
    """Return {(base, item): total_cltv_buy_qty} so callers subtract only CLTV's own volume
    instead of discarding giant external buy-walls (e.g. 468k silver_ore @ 101 cr) at shared hubs."""
    now_t = time.time() if now_t is None else float(now_t)
    by_qty = {}
    doc = _read_json(Path(data_dir) / "fleet" / "bursar_buys.json", {})
    entries = doc.get("entries") if isinstance(doc, dict) and isinstance(doc.get("entries"), dict) else {}
    for _pilot, bases in entries.items():
        if not isinstance(bases, dict):
            continue
        for b_id, rec in bases.items():
            if not isinstance(rec, dict) or (now_t - float(rec.get("at") or 0)) > ttl_s:
                continue
            for iid, q in (rec.get("items") or {}).items():
                qi = int(q or 0)
                if iid and qi > 0:
                    k = (str(b_id), str(iid))
                    by_qty[k] = by_qty.get(k, 0) + qi
    return by_qty


def cash_weighted_median(pairs, cap_cash_per_station=500000.0):
    """Compute Cash-Weighted Median from [(price, qty), ...] with per-station cash cap.

    Immune to BOTH directions of market manipulation:
      - Pump spoofs (e.g. 701 cr x 6 = 4,206 cr vs 10 cr x 8,172 = 81,720 cr): thin top spike
        winsorized when <= 5% of total cash (or qty <= 5) and > 2.5x next price.
      - 2-cr trash scavenger walls (e.g. 2 cr x 50,000 = 100k cr vs 45 cr x 2,025 = 91k cr):
        weighting by cash + dropping <=3 cr scavenger walls when real >=10 cr demand exists
        prevents bottom-feeders from collapsing scarce ore fair prices to 2 cr.
    """
    clean = [(float(p), int(q)) for p, q in (pairs or ()) if float(p or 0) > 0 and int(q or 0) > 0]
    if not clean:
        return 0.0
    clean.sort(key=lambda x: x[0])
    # Drop <=3 cr trash-scavenger bids whenever meaningful >=10 cr external demand exists
    real_hi = [(p, q) for p, q in clean if p >= 10.0]
    if real_hi:
        real_cash = sum(p * q for p, q in real_hi)
        real_qty = sum(q for _, q in real_hi)
        if (len(real_hi) >= 2 and real_qty >= 20) or (real_cash >= 15000.0 and real_qty >= 20):
            clean = [pq for pq in clean if pq[0] > 3.0] or clean
    # Winsorize thin extreme top outlier on cash share or thin unit count
    while len(clean) >= 3:
        tot_c = sum(min(p * q, cap_cash_per_station) for p, q in clean)
        top_p, top_q = clean[-1]
        top_c = min(top_p * top_q, cap_cash_per_station)
        if tot_c > 0 and (top_q <= 6 or top_c <= tot_c * 0.08) and top_p > clean[-2][0] * 2.5:
            clean = clean[:-1]
        else:
            break
    if len(clean) == 2:
        # Guard 2-station book against 1 tiny extreme spoof (e.g. 701 x 6 vs 10 x 8172)
        p0, q0 = clean[0]
        p1, q1 = clean[1]
        c0 = min(p0 * q0, cap_cash_per_station)
        c1 = min(p1 * q1, cap_cash_per_station)
        if (q1 <= 6 or c1 < (c0 + c1) * 0.08) and p1 > p0 * 2.5:
            clean = [clean[0]]
    weights = [(p, min(p * q, cap_cash_per_station)) for p, q in clean]
    tot_w = sum(w for _, w in weights)
    half = tot_w / 2.0
    acc = 0.0
    for p, w in weights:
        acc += w
        if acc >= half:
            return float(p)
    return float(weights[-1][0])


def volume_weighted_median(pairs):
    """Compute exact Volume-Weighted Median from [(price, qty), ...] with price > 0, qty > 0.

    Naturally immune to extreme single-station spoofs (e.g., 1 station bidding 795 cr x 40
    when real deep stations bid 7-11 cr x 200,000 -> VWM = 7.0 cr!).
    """
    clean = [(float(p), int(q)) for p, q in (pairs or ()) if float(p or 0) > 0 and int(q or 0) > 0]
    if not clean:
        return 0.0
    clean.sort(key=lambda x: x[0])
    # Winsorize thin extreme top outlier if >= 3 independent price levels exist and top has <= 5% of volume
    if len(clean) >= 3:
        tot_v = sum(q for _, q in clean)
        if tot_v > 0 and clean[-1][1] <= max(5, int(tot_v * 0.05)) and clean[-1][0] > clean[-2][0] * 2.5:
            clean = clean[:-1]
    tot = sum(q for _, q in clean)
    half = tot / 2.0
    acc = 0.0
    for p, q in clean:
        acc += q
        if acc >= half:
            return float(p)
    return float(clean[-1][0])


def compute_book_vwm_map(books_rows, cltv_buy_keys=None, min_bid=2.0, min_qty=5, max_age_s=21600.0, now_t=None, cltv_buy_qty=None):
    """Build {item: {vwm, stations, total_qty, min_bid, max_bid, median_station_bid}} from book rows.

    Excludes CLTV's own open buy orders (by net quantity when cltv_buy_qty is provided, or full station
    exclusion for legacy set callers) so our own bots never poison price discovery while preserving
    external mega buy-walls at shared stations.
    """
    now_t = time.time() if now_t is None else float(now_t)
    cltv_qmap = dict(cltv_buy_qty) if isinstance(cltv_buy_qty, dict) else (dict(cltv_buy_keys) if isinstance(cltv_buy_keys, dict) else None)
    cltv_set = set(cltv_buy_keys or ()) if cltv_qmap is None else set()
    grouped = {}
    for r in books_rows or []:
        if not isinstance(r, dict):
            continue
        b_id = str(r.get("base") or "")
        iid = str(r.get("item") or "")
        if not iid:
            continue
        t = float(r.get("t") or 0)
        if t > 0 and (now_t - t) > max_age_s:
            continue
        bp = float(r.get("bid") or 0)
        bq = int(r.get("bid_qty") or 0)
        if cltv_qmap is not None and b_id:
            bq = max(0, bq - int(cltv_qmap.get((b_id, iid), 0)))
        elif b_id and (b_id, iid) in cltv_set:
            continue
        if bp < min_bid or bq < min_qty:
            continue
        grouped.setdefault(iid, []).append((b_id, bp, bq))

    out = {}
    for iid, rows in grouped.items():
        # Per-station max external bid (avoids double counting)
        by_st = {}
        for b_id, bp, bq in rows:
            prev = by_st.get(b_id)
            if prev is None or bp > prev[0]:
                by_st[b_id] = (bp, bq)
        pairs = list(by_st.values())
        vwm = cash_weighted_median(pairs)
        prices = sorted(p for p, _ in pairs)
        st_med = prices[len(prices) // 2]
        fair_vwm = vwm
        out[iid] = {
            "vwm": round(float(fair_vwm), 2),
            "raw_vwm": round(float(vwm), 2),
            "station_median": round(float(st_med), 2),
            "stations": len(by_st),
            "total_qty": sum(q for _, q in pairs),
            "min_bid": round(prices[0], 2),
            "max_bid": round(prices[-1], 2),
        }
    return out


def update_price_oracle(data_dir, vwm_map, now_t=None, luld_pct_per_h=0.25, min_write_interval_s=60.0):
    """Update rolling LULD TWAP/EWMA oracle (`data/fleet/price_oracle.json`) and return robust fair prices.

    Free-market adaptive with NO static price cap:
      - Genuine sustained price shifts move smoothly up to +/- 25%/h (3x in 5h, 200x in 24h!).
      - Sudden 1-station flash-pumps (e.g. 11 cr -> 795 cr in 2m) are strictly clamped by the LULD band!
    """
    now_t = time.time() if now_t is None else float(now_t)
    fdir = Path(data_dir) / "fleet"
    fdir.mkdir(parents=True, exist_ok=True)
    lock_p = fdir / "price_oracle.lock"
    oracle_p = fdir / "price_oracle.json"

    with open(lock_p, "a+", encoding="utf-8") as lf:
        fcntl.flock(lf, fcntl.LOCK_EX)
        try:
            doc = _read_json(oracle_p, {})
            items = doc.get("items") if isinstance(doc, dict) and isinstance(doc.get("items"), dict) else {}
            last_w = float(doc.get("updated_at") or 0) if isinstance(doc, dict) else 0.0
            changed = False
            result = {}
            all_iids = set(items.keys()) | set((vwm_map or {}).keys())
            for iid in all_iids:
                obs = (vwm_map or {}).get(iid)
                prev = items.get(iid) if isinstance(items.get(iid), dict) else None
                if obs and float(obs.get("vwm") or 0) > 0:
                    obs_p = float(obs["vwm"])
                    st_n = int(obs.get("stations") or 1)
                    tot_q = int(obs.get("total_qty") or 0)
                    if prev and float(prev.get("twap") or 0) > 0:
                        prev_p = float(prev["twap"])
                        dt_h = min(6.0, max(0.05, (now_t - float(prev.get("t") or now_t)) / 3600.0))
                        # Escape hatch when recovering from a previously 2-cr trash-poisoned TWAP on confirmed multi-station/deep demand
                        if (prev_p <= 4.0 and obs_p >= 12.0 and (st_n >= 2 or tot_q >= 200)) or (obs_p >= prev_p * 2.0 and st_n >= 4 and tot_q >= 500):
                            new_twap = obs_p
                        else:
                            # Require multi-station quorum OR deep liquidity (>=100 units) to move TWAP sharply upward
                            eff_luld = luld_pct_per_h if (st_n >= 2 or tot_q >= 100) else (luld_pct_per_h * 0.4)
                            hi = prev_p * ((1.0 + eff_luld) ** dt_h)
                            lo = prev_p * (max(0.2, 1.0 - eff_luld) ** dt_h)
                            clamped = max(lo, min(hi, obs_p))
                            alpha = min(0.60, max(0.10, 0.45 * dt_h))
                            new_twap = (1.0 - alpha) * prev_p + alpha * clamped
                    else:
                        new_twap = obs_p
                    rec = {
                        "twap": round(new_twap, 2),
                        "vwm": round(obs_p, 2),
                        "stations": st_n,
                        "total_qty": tot_q,
                        "t": int(now_t),
                    }
                    # Fair price: conservative min of current VWM and LULD-collared TWAP band (1.35x)
                    fair_p = min(obs_p, new_twap * 1.35) if new_twap > 0 else obs_p
                    rec["fair_price"] = round(fair_p, 2)
                    items[iid] = rec
                    result[iid] = rec
                    changed = True
                elif prev and float(prev.get("twap") or 0) > 0:
                    # Keep historical TWAP anchor alive for up to 48h even if books momentarily go quiet
                    if (now_t - float(prev.get("t") or 0)) <= 48.0 * 3600.0:
                        rec = dict(prev)
                        rec["fair_price"] = round(float(prev["twap"]), 2)
                        result[iid] = rec
            if changed and (now_t - last_w >= min_write_interval_s or not oracle_p.is_file()):
                _write_json(oracle_p, {"updated_at": int(now_t), "items": items})
            return result
        finally:
            fcntl.flock(lf, fcntl.LOCK_UN)


def load_fair_price_map(data_dir, db_path=None, now_t=None):
    """Convenience loader: read fresh (<6h) external books from read.db, update LULD oracle, return {item: rec}."""
    now_t = time.time() if now_t is None else float(now_t)
    db = Path(db_path) if db_path else (Path(data_dir) / "store" / "read.db")
    cltv_qty = load_cltv_buy_qty(data_dir, now_t=now_t)
    rows = []
    if db.is_file():
        con = None
        try:
            try:
                import worldcache as _wc
                con = _wc.ro_db(db, timeout=3.0)
            except Exception:
                con = sqlite3.connect("file:%s?mode=ro" % db, uri=True, timeout=3.0)
            tbls = {r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()}
            if "books" in tbls:
                cols = {r[1] for r in con.execute("PRAGMA table_info(books)").fetchall()}
                bcol = "base" if "base" in cols else ("station" if "station" in cols else "''")
                t_sel = "COALESCE(t, 0)" if "t" in cols else "0"
                t_where = " AND t >= ?" if "t" in cols else ""
                params = (now_t - 6.0 * 3600.0,) if "t" in cols else ()
                q = "SELECT %s, item, COALESCE(bid,0), COALESCE(bid_qty,0), %s FROM books WHERE bid >= 2 AND bid_qty >= 5%s" % (bcol, t_sel, t_where)
                for b_id, iid, bp, bq, ts in con.execute(q, params):
                    rows.append({"base": str(b_id or ""), "item": str(iid or ""), "bid": float(bp or 0), "bid_qty": int(bq or 0), "t": float(ts or 0)})
        except sqlite3.Error:
            pass
        finally:
            if con is not None:
                con.close()
    vwm_map = compute_book_vwm_map(rows, cltv_buy_qty=cltv_qty, now_t=now_t)
    return update_price_oracle(data_dir, vwm_map, now_t=now_t)


def safe_buy_ceiling(iid, local_bid, local_ask, fair_val, max_ratio=0.90, max_fair_mult=1.25):
    """Return manipulation-resistant max buy price for `iid` (0 = refuse suspicious/unanchored book).

    Defenses:
      - Bait-Ask Detector: if local_ask > 3.0x fair_val, ignore local_ask completely!
      - LULD Fair-Value Collar: cap buy ceiling at max(5, int(fair_val * max_fair_mult)).
      - Unanchored Thin-Book Gate: if fair_val == 0 (no multi-unit external bids anywhere),
        ONLY allow buying if local market is a tight two-sided book (local_bid > 0 and local_ask <= local_bid * 2.5).
    """
    lb = float(local_bid or 0.0)
    la = float(local_ask or 0.0)
    fv = float(fair_val or 0.0)
    if fv > 0.0:
        fair_cap = max(5, int(round(fv * max_fair_mult)))
        # Bait-Ask trap: ask is > 3x fair value -> ignore ask completely!
        if la > 0.0 and la <= fv * 3.0:
            ask_cap = int(la * max_ratio)
            return max(0, min(ask_cap, fair_cap))
        return fair_cap
    # No cross-station fair_val anchor: require tight two-sided local spread (blocks 1,000 cr solo bait asks!)
    if lb > 0.0 and la > 0.0 and la <= lb * 2.5:
        return max(1, min(int(la * max_ratio), int(lb * 1.15)))
    if lb > 0.0 and la <= 0.0:
        return max(1, int(lb * 1.05))
    return 0


def read_price_oracle(data_dir, max_age_s=86400.0, now_t=None):
    """Read-only, zero-write loader of data/fleet/price_oracle.json -> {item: rec}.

    Safe for read-only HUD/analytics (accounting.py) and fast parallel planners (mine_net, hunt_net,
    craft_net, routemaker) without opening SQLite or writing to disk; bursar.py keeps price_oracle.json fresh.
    """
    if not data_dir:
        return {}
    op = Path(data_dir) / "fleet" / "price_oracle.json"
    if not op.is_file():
        return {}
    doc = _read_json(op, {})
    items = (doc.get("items") or {}) if isinstance(doc, dict) else {}
    if not isinstance(items, dict):
        return {}
    now_f = time.time() if now_t is None else float(now_t)
    out = {}
    for iid, rec in items.items():
        if not isinstance(rec, dict):
            continue
        ts = float(rec.get("t") or doc.get("updated_at") or 0.0)
        if ts > 0.0 and max_age_s > 0.0 and (now_f - ts) > float(max_age_s):
            continue
        fp = float(rec.get("fair_price") or rec.get("twap") or rec.get("vwm") or 0.0)
        if fp > 0.0:
            r2 = dict(rec)
            r2["fair_price"] = fp
            out[str(iid)] = r2
    return out


def guarded_bid_price(iid, spot_bid, fair_map, max_mult=1.50):
    """Cap any raw spot/station bid using the manipulation-resistant VWM+LULD fair price oracle.

    Used across ALL farming planners (mine_net, hunt_net, craft_net, routemaker) and analytics
    (accounting.py) so a single-station spoof spike (e.g. 78,350 cr lumen_honey_cake or 670 cr
    silicon_ore) NEVER hijacks miners/hunters/crafters or inflates Balance Sheet/P&L valuations,
    while genuine regional premiums up to `max_mult` (default 1.50x) remain fully actionable.
    """
    sb = float(spot_bid or 0.0)
    if sb <= 0.0 or not isinstance(fair_map, dict):
        return sb
    rec = fair_map.get(str(iid or ""))
    if not rec:
        return sb
    fp = float(rec.get("fair_price") if isinstance(rec, dict) else (rec or 0.0))
    if fp <= 0.0:
        return sb
    cap = max(fp * float(max_mult or 1.50), fp + 2.0)
    return min(sb, cap)


def safe_sell_floor(iid, local_bid, local_ask, fair_val, min_ratio=0.65, fair_floor_ratio=0.72):
    """Return manipulation-resistant minimum sell price for `iid` (defends against lowball-ask/dump-spoof traps!).

    Reverse scam defense:
      Suppose quantum_silk has galactic fair_val = 2,100 cr, and a rival bot lists 1 unit at
      ask = 100 cr alongside a 80 cr bid (or 0 ask + 10 cr bid) hoping our Bursar undercuts to
      99 cr or instant-dumps into 80 cr!
      safe_sell_floor anchors the minimum acceptable sell price to >= max(local_ref * min_ratio, fair_val * 0.72),
      so our Bursars & Haulers NEVER get tricked into selling valuable goods for 10-50% of true value!
    """
    lb = float(local_bid or 0.0)
    la = float(local_ask or 0.0)
    fv = float(fair_val or 0.0)
    if lb > 0.0 and la > 0.0:
        local_ref = min(la, max(lb, la * 0.70))
    elif lb > 0.0:
        local_ref = lb
    elif la > 0.0:
        local_ref = la
    elif fv > 0.0:
        local_ref = fv
    else:
        return 0
    local_floor = max(2, int(round(local_ref * float(min_ratio or 0.65))))
    if fv >= 10.0:
        fair_floor = max(2, int(round(fv * float(fair_floor_ratio or 0.72))))
        return max(local_floor, fair_floor)
    return local_floor


def is_mirage_arbitrage_trap(iid, buy_ask, sell_bid, fair_info):
    """True when an arbitrage opportunity looks like an EVE-style Margin/Mirage Bait Scam.

    Classic scam: scammer lists a 10 cr item at 500 cr ask and posts a fake 800 cr buy wall
    that they cancel while the victim hauler is in transit.
    Defense: if buy_ask > max(25, 2.2 * fair_price) AND sell_bid > 3.0 * fair_price -> REJECT!
    """
    ask_p = float(buy_ask or 0.0)
    bid_p = float(sell_bid or 0.0)
    if not isinstance(fair_info, dict):
        fair_p = float(fair_info or 0.0)
    else:
        fair_p = float(fair_info.get("fair_price") or fair_info.get("twap") or fair_info.get("vwm") or 0.0)
    if fair_p <= 0.0:
        # Unknown/unanchored exotic item with extreme spread (> 6x) is high-risk mirage bait
        return ask_p >= 200.0 and bid_p >= ask_p * 4.0
    if ask_p > max(25.0, fair_p * 2.2) and bid_p > fair_p * 3.0:
        return True
    return False

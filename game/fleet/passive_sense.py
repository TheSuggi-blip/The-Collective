#!/usr/bin/env python3
"""passive_sense.py -- zero-fuel opportunistic market & herd freshness updates when any fleet ship docks or works.

WHAT: whenever a miner, hunter, hauler, or trader already receives a `view_market` or `get_nearby` response at a station
      or POI (or docks at a station whose market book in `data/market/<base>.json` is older than `MAX_MARKET_AGE`),
      refreshes the local JSON atomically so Intel (`Oracle`) does not have to burn `-750 cr/h` patrolling home/worked
      stations our own ships visit every two minutes.
USAGE:
  imported by mine.py, hunt.py and route_run.py: maybe_refresh_market(call_raw, base_id, system_id)
"""

import json
import os
import time
from pathlib import Path

MAX_MARKET_AGE = 600


def maybe_refresh_market(call_raw, base_id, system_id="", data="/srv/collective/data", max_age=MAX_MARKET_AGE):
    """If `data/market/<base_id>.json` is missing or older than `max_age`, call `view_market` once while docked (0 fuel!)."""
    if not base_id:
        return False
    mp = Path(data) / "market" / f"{base_id}.json"
    try:
        if mp.is_file() and time.time() - mp.stat().st_mtime < max_age:
            return False
    except OSError:
        pass
    try:
        ans = call_raw("view_market", {})
        res = (ans.get("result") if isinstance(ans, dict) and isinstance(ans.get("result"), dict) else ans) or {}
        items = res.get("items") or res.get("orders") or res.get("market")
        if not isinstance(items, list):
            return False
        mp.parent.mkdir(parents=True, exist_ok=True)
        payload = {"base": base_id, "system": system_id, "fetched_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "items": items}
        tmp = mp.with_name(f"{mp.name}.{os.getpid()}.tmp")
        tmp.write_text(json.dumps(payload, separators=(",", ":")), encoding="utf-8")
        os.replace(tmp, mp)
        return True
    except Exception:
        return False

#!/usr/bin/env python3
"""Process-wide single-flight TTL cache & immutable read.db opener for threaded runhost runners.

WHAT:
  Provides `ro_db(db_path)` (opens read.db with `mode=ro&immutable=1` so SQLite never emits
  POSIX fcntl byte-range lock storms across gVisor 9p/gofer) and `cached(key, ttl_s, loader)`
  (single-flight per-key lock + TTL cache stored in `sys.modules["worldcache"]`).

WHY:
  `runhost.py` executes every ship runner thread via `exec(code, fresh_scope)` so module-level
  dicts inside runner scripts are discarded per thread, while imported modules in `sys.modules`
  are shared process-wide. Without `worldcache.py` and `&immutable=1`, 400 concurrent AutoNet
  threads independently scanned the 194 MB `read.db` and 996 route files, pinning 550+ deleted
  `read.db` FDs and stalling startups for 15-30+ minutes under the Python GIL.

USAGE:
  import worldcache
  con = worldcache.ro_db(db_path)
  world = worldcache.cached(("mine_world", str(data), worldcache.db_sig(data)), 25.0, _load)

Stdlib only. ASCII only.
"""

import json
import os
import sqlite3
import threading
import time
import urllib.parse
from pathlib import Path

_META_LOCK = threading.Lock()
_KEY_LOCKS = {}
_CACHE = {}          # key -> (expires_at, value)
_MAX_ENTRIES = 256


def file_sig(path):
    """Return (mtime_ns, ctime_ns, size) for `path`, or None if absent."""
    try:
        st = os.stat(str(path))
        return (st.st_mtime_ns, st.st_ctime_ns, st.st_size)
    except OSError:
        return None


def db_sig(data_dir):
    """Signature of `<data_dir>/store/read.db` so atomic store replacements invalidate cache."""
    return file_sig(Path(data_dir) / "store" / "read.db")


def ro_db(db_path, timeout=3.0):
    """Open an immutable read-only SQLite connection to `read.db` (zero fcntl lock storms)."""
    p = Path(db_path)
    try:
        resolved = p.resolve()
    except OSError:
        resolved = p
    uri = "file:%s?mode=ro&immutable=1" % urllib.parse.quote(str(resolved))
    return sqlite3.connect(uri, uri=True, timeout=timeout)


def _lock_for(key):
    with _META_LOCK:
        lk = _KEY_LOCKS.get(key)
        if lk is None:
            lk = threading.Lock()
            if len(_KEY_LOCKS) > _MAX_ENTRIES * 2:
                _KEY_LOCKS.clear()
            _KEY_LOCKS[key] = lk
        return lk


def cached(key, ttl_s, loader):
    """Single-flight process-wide TTL cache: at most one thread computes `loader()` per key."""
    if os.environ.get("WORLDCACHE_DISABLE") == "1" or ttl_s <= 0:
        return loader()
    now = time.monotonic()
    hit = _CACHE.get(key)
    if hit is not None and now < hit[0]:
        return hit[1]
    lk = _lock_for(key)
    with lk:
        now2 = time.monotonic()
        hit2 = _CACHE.get(key)
        if hit2 is not None and now2 < hit2[0]:
            return hit2[1]
        val = loader()
        if len(_CACHE) >= _MAX_ENTRIES:
            cutoff = time.monotonic()
            stale = [k for k, v in list(_CACHE.items()) if cutoff >= v[0]]
            for k in stale:
                _CACHE.pop(k, None)
            if len(_CACHE) >= _MAX_ENTRIES:
                _CACHE.clear()
        _CACHE[key] = (time.monotonic() + float(ttl_s), val)
        return val


def read_json_cached(path, default=None, ttl_s=30.0):
    """Read and parse a JSON file via `cached()`, automatically invalidated when file changes."""
    p = Path(path)
    sig = file_sig(p)
    if sig is None:
        return {} if default is None else default
    def _load():
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return {} if default is None else default
    return cached(("json", str(p), sig), ttl_s, _load)


def clear():
    """Clear all cached entries (mainly for tests)."""
    with _META_LOCK:
        _CACHE.clear()

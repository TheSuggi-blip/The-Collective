#!/usr/bin/env python3
"""Tests for process-wide single-flight TTL cache & immutable read.db opener (worldcache.py)."""
import sqlite3
import sys
import tempfile
import threading
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "game" / "fleet"))
import worldcache


class TestWorldCache(unittest.TestCase):
    def setUp(self):
        worldcache.clear()

    def test_single_flight_across_20_threads(self):
        calls = []
        barrier = threading.Barrier(20)
        results = []
        lock = threading.Lock()

        def loader():
            calls.append(1)
            time.sleep(0.05)
            return {"ok": True, "n": len(calls)}

        def worker():
            barrier.wait()
            v = worldcache.cached(("sf_test", 1), 10.0, loader)
            with lock:
                results.append(v)

        threads = [threading.Thread(target=worker) for _ in range(20)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        self.assertEqual(len(calls), 1)
        self.assertEqual(len(results), 20)
        self.assertTrue(all(r == {"ok": True, "n": 1} for r in results))

    def test_ro_db_and_sig_invalidation(self):
        with tempfile.TemporaryDirectory() as td:
            db = Path(td) / "store" / "read.db"
            db.parent.mkdir(parents=True, exist_ok=True)
            con = sqlite3.connect(str(db))
            con.execute("CREATE TABLE t (x INTEGER)")
            con.execute("INSERT INTO t VALUES (42)")
            con.commit()
            con.close()

            sig1 = worldcache.db_sig(td)
            self.assertIsNotNone(sig1)
            ro = worldcache.ro_db(db)
            try:
                self.assertEqual(ro.execute("SELECT x FROM t").fetchone()[0], 42)
            finally:
                ro.close()

            db2 = Path(td) / "store" / "read.db.tmp"
            con2 = sqlite3.connect(str(db2))
            con2.execute("CREATE TABLE t (x INTEGER)")
            con2.execute("INSERT INTO t VALUES (99)")
            con2.execute("INSERT INTO t VALUES (100)")
            con2.commit()
            con2.close()
            time.sleep(0.02)
            db2.replace(db)
            sig2 = worldcache.db_sig(td)
            self.assertNotEqual(sig1, sig2)


if __name__ == "__main__":
    unittest.main()

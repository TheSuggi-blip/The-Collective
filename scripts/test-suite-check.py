#!/usr/bin/env python3
"""test-suite-check.py -- lightweight non-AI check of scripts/tests/ against committed HEAD.

WHAT: exports exact git HEAD into a temporary directory (so active Admiral working-tree edits never
      interfere), runs every scripts/tests/test_*.py file with a per-file timeout, writes a JSON
      summary to /srv/collective/data/fleet/test-suite-status.json, and exits 0 silently when all
      pass or 1 with a concise list of failing test files when HEAD is red.
RULES:
  - Read-only on the repository working tree; never commits, never touches live plans or routes.
  - Pure stdlib, pure 7-bit ASCII, zero AI calls.
WHY:  Suggi & Unity (reports.log ENT-135, 2026-11-23): catch red tests on HEAD proactively on an
      hourly non-AI schedule before Admiral fleet-build.sh installs hit them.

USAGE:
  python3 -B scripts/test-suite-check.py [--repo /srv/collective/the-collective] [--out /srv/collective/data/fleet/test-suite-status.json] [--timeout 180] [--verbose]
"""

import argparse
import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path


def run_head_suite(repo, out_path, timeout=180, verbose=False):
    repo_p = Path(repo).resolve()
    sha = subprocess.check_output(["git", "-C", str(repo_p), "rev-parse", "--short", "HEAD"], text=True).strip()
    started = time.time()
    passed, failed = [], []
    with tempfile.TemporaryDirectory(prefix="head-test-check-") as tmp:
        tmp_p = Path(tmp)
        tar_proc = subprocess.Popen(["git", "-C", str(repo_p), "archive", "HEAD"], stdout=subprocess.PIPE)
        try:
            subprocess.check_call(["tar", "-x", "-C", str(tmp_p)], stdin=tar_proc.stdout)
        finally:
            if tar_proc.stdout:
                tar_proc.stdout.close()
            tar_proc.wait()
        tests_dir = tmp_p / "scripts" / "tests"
        test_files = sorted(tests_dir.glob("test_*.py")) if tests_dir.is_dir() else []
        env = dict(os.environ)
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        for tf in test_files:
            rel = str(tf.relative_to(tmp_p))
            t0 = time.time()
            try:
                proc = subprocess.run(
                    [sys.executable, "-B", str(tf)],
                    cwd=str(tmp_p),
                    capture_output=True,
                    text=True,
                    timeout=timeout,
                    env=env,
                )
                dur = round(time.time() - t0, 2)
                if proc.returncode == 0:
                    passed.append({"file": rel, "seconds": dur})
                    if verbose:
                        print("PASS %s (%.2fs)" % (rel, dur))
                else:
                    tail = (proc.stderr or proc.stdout or "").strip().splitlines()[-6:]
                    failed.append({"file": rel, "seconds": dur, "code": proc.returncode, "tail": tail})
                    print("FAIL %s (exit %d, %.2fs): %s" % (rel, proc.returncode, dur, " | ".join(tail[-2:])[:240]))
            except subprocess.TimeoutExpired:
                dur = round(time.time() - t0, 2)
                failed.append({"file": rel, "seconds": dur, "code": -1, "tail": ["timeout after %ds" % timeout]})
                print("FAIL %s (timeout %ds)" % (rel, timeout))
    payload = {
        "checked_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "head": sha,
        "duration_s": round(time.time() - started, 2),
        "total_files": len(passed) + len(failed),
        "passed_files": len(passed),
        "failed_files": len(failed),
        "ok": len(failed) == 0,
        "failures": failed,
    }
    if out_path:
        op = Path(out_path)
        try:
            op.parent.mkdir(parents=True, exist_ok=True)
            tmp_out = op.with_suffix(".json.%d.tmp" % os.getpid())
            tmp_out.write_text(json.dumps(payload, indent=1) + "
", encoding="ascii")
            os.replace(tmp_out, op)
        except OSError:
            pass
    if verbose or failed:
        print("HEAD TEST SUITE (%s): %d/%d passed in %.1fs | %s" % (
            sha, len(passed), len(passed) + len(failed), payload["duration_s"], "PASS" if payload["ok"] else "HALT"
        ))
    return 0 if payload["ok"] else 1


def main(argv=None):
    p = argparse.ArgumentParser(description="Non-AI HEAD test-suite check")
    p.add_argument("--repo", default="/srv/collective/the-collective")
    p.add_argument("--out", default="/srv/collective/data/fleet/test-suite-status.json")
    p.add_argument("--timeout", type=int, default=180)
    p.add_argument("--verbose", action="store_true")
    args = p.parse_args(argv)
    return run_head_suite(args.repo, args.out, timeout=args.timeout, verbose=args.verbose)


if __name__ == "__main__":
    sys.exit(main())

#!/bin/bash
# validate-ids.sh -- check frontmatter IDs for manual rounding
#
# WHAT: scans markdown files with YAML frontmatter id: fields and flags
# timestamps that appear to be manually typed rather than generated from
# `date -u +'%Y%m%dT%H%M%SZ'`.
#
# USAGE: validate-ids.sh [file...]
set -euo pipefail

python3 -I -B - "$@" <<'PY'
import calendar
import os
import re
import subprocess
import sys
import time

args = sys.argv[1:]
if not args:
    out = subprocess.check_output(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "*.md"],
        text=True,
    )
    files = sorted(set(ln for ln in out.splitlines() if ln.strip()))
else:
    files = args

now = int(time.time())
iso_re = re.compile(r"^[0-9]{8}T[0-9]{6}Z$")
errors = 0
warnings = 0
files_with_ids = 0
id_map = {}

for f in files:
    if not os.path.isfile(f):
        continue
    doc_id = ""
    try:
        with open(f, "r", encoding="utf-8", errors="replace") as fh:
            first = fh.readline()
            if first.rstrip("\r\n") != "---":
                continue
            for line in fh:
                s = line.rstrip("\r\n")
                if s == "---":
                    break
                if s.startswith("id: "):
                    doc_id = s[4:].strip().split()[0] if s[4:].strip() else ""
                    break
    except OSError:
        continue
    if not doc_id:
        continue
    files_with_ids += 1

    if not iso_re.match(doc_id):
        print(f"INVALID FORMAT: {f} -> id: {doc_id} (not YYYYMMDDTHHMMSSZ)")
        errors += 1
        continue

    if doc_id.endswith("00Z"):
        print(f"SUSPECT ROUNDED: {f} -> id: {doc_id} (seconds are 00 -- likely manually typed, not from date -u)")
        warnings += 1

    if doc_id in id_map:
        print(f"DUPLICATE ID: {f} shares id: {doc_id} with {id_map[doc_id]}")
        errors += 1
    else:
        id_map[doc_id] = f

    try:
        tm = time.strptime(doc_id, "%Y%m%dT%H%M%SZ")
        ts_epoch = calendar.timegm(tm)
    except ValueError:
        print(f"INVALID FORMAT: {f} -> id: {doc_id} (invalid calendar timestamp)")
        errors += 1
        continue

    if ts_epoch > now + 300:
        print(f"FUTURE TIMESTAMP: {f} -> id: {doc_id} (timestamp is in the future)")
        errors += 1

print("")
print(f"Scanned {files_with_ids} files with frontmatter IDs.")
print(f"Errors: {errors} | Warnings: {warnings}")

if errors > 0:
    print("")
    print("ERRORS FOUND -- fix before committing.")
    sys.exit(1)

if warnings > 0:
    print("")
    print("WARNINGS: run 'date -u +%Y%m%dT%H%M%SZ' and compare with above IDs.")
    print("If IDs were manually typed, regenerate them before the next commit.")

sys.exit(0)
PY

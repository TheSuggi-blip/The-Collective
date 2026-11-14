#!/bin/bash
# check-log-blank-line.sh -- gate for the logs in communications/
# (communications/protocol.md: one blank line between entries).
# Usage: bash scripts/check-log-blank-line.sh <communications/NAME.log> [ENT-NNN]
# Checks the entry named, or the last entry of the file.
# PASS: prints BLANK-LINE-OK, exit 0: exactly one blank line before a
#       non-first entry whose ENT id occurs once in the file.
# HALT: prints BLANK-LINE-HALT and the reason, exit 1: unreadable file,
#       no entries, an ENT id that is absent or occurs twice, zero or
#       several blank lines.
# Position: after appending and before committing. Only reads the log.
set -euo pipefail
python3 - "$@" <<'PY'
import re
import sys
from pathlib import Path


def halt(message):
    print('BLANK-LINE-HALT -- ' + message)
    raise SystemExit(1)


if not 2 <= len(sys.argv) <= 3:
    halt('usage: <log-file> [ENT-NNN]')
try:
    lines = Path(sys.argv[1]).read_text(encoding='utf-8').splitlines()
except (OSError, UnicodeError):
    halt('cannot read log file')
headers = []
for number, line in enumerate(lines):
    match = re.match(r'^## \[(ENT-[0-9]+)\](?:\s|$)', line)
    if match:
        headers.append((number, match.group(1)))
if not headers:
    halt('no ENT entries found')
target = sys.argv[2] if len(sys.argv) == 3 else headers[-1][1]
if not re.fullmatch(r'ENT-[0-9]+', target):
    halt('invalid target identifier')
positions = [i for i, (_, identifier) in enumerate(headers) if identifier == target]
if len(positions) != 1:
    halt('target must exist exactly once: ' + target)
position = positions[0]
if position == 0:
    print('BLANK-LINE-OK -- first entry has no preceding entry')
    raise SystemExit(0)
line_number = headers[position][0]
previous_header = headers[position - 1][0]
index = line_number - 1
blank_count = 0
while index > previous_header and not lines[index].strip():
    blank_count += 1
    index -= 1
if blank_count != 1:
    halt(f'{target} at line {line_number + 1}: expected one blank line, found {blank_count}')
print('BLANK-LINE-OK')
PY

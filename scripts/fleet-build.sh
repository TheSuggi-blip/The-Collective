#!/bin/bash
# fleet-build.sh -- a member builds and installs its own change of the fleet's scripts and routes, through the gates.
#
# WHAT: three steps, each one command, so that a member need not wait for the Fleet Admiral for a runner's step, a new
#       script, a figure or a route:
#         tree <dir>                           a scratch copy of the repository as committed now, with its base noted
#         test <dir> [<test module>]           the gates inside that copy: syntax, the route gate, the indexes, the unit tests
#         install <dir> "<message>" <path>...  the named paths from the copy into the clone, committed under your name
# RULES:
#   - `install` waits up to four minutes for a clean clone, copies, runs every gate in the clone and commits by path;
#     when a gate fails it puts the paths back as they were and exits 1. It never pushes (the watcher does).
#   - Stopped (INT, TERM, HUP) or past its own limit (FLEET_BUILD_LIMIT seconds, default 1500) once it has copied, it
#     stops its gates and puts the paths back the same way, so a cut install never leaves a live file uncommitted
#     (errors.log ENT-115); stopped before the copy it has nothing to put back. A kill -9 no script can catch.
#   - A path another member changed since your copy was made is refused: make a new copy and carry your change over.
#     Otherwise one member's work would silently overwrite another's.
#   - A changed script under game/fleet/ needs its test in the same install: a path under scripts/tests/.
#   - Closed to every member but the Fleet Admiral, because one fault there stops the whole fleet or opens the lock:
#     game/fleet/gate.py, division.py, dispatch.py, runhost.py, fill.py, collective_mcp.py, store.py; scripts/comms.py and this
#     file; station/, governance/, communications/, collective-index/, .github/, .githooks/. Ask for those in requests.log.
#   - The member is read from the shell (your Hermes profile); a shell that is no member installs nothing.
# WHY:  Suggi, 2026-11-16: the Admirals do by script what they would otherwise ask for and wait for.
#
# USAGE:
#   bash scripts/fleet-build.sh tree /path/in/your/scratch/t1
#   bash scripts/fleet-build.sh test /path/in/your/scratch/t1 scripts.tests.test_fleet_mine
#   bash scripts/fleet-build.sh install /path/in/your/scratch/t1 "mine.py: the sale step waits for the dock" game/fleet/mine.py scripts/tests/test_fleet_mine.py
#   REPO=<dir> runs it on another clone (a test copy).
set -u
R=${REPO:-/srv/collective/the-collective}
CLOSED='^(game/fleet/(gate|division|dispatch|runhost|fill|plan|collective_mcp|store)\.py|scripts/(comms\.py|fleet-build\.sh)|(station|governance|communications|collective-index|\.github|\.githooks)(/|$))'
verb=${1:-}; T=${2:-}
usage() { sed -n '2,29p' "$0" | sed 's/^# \{0,1\}//'; exit 2; }
[ -n "$verb" ] && [ -n "$T" ] || usage

who() { python3 -I -B -c "
import sys
sys.path.insert(0, '$R/game/fleet')
import division
kind, name = division.member()
print(name if kind == 'member' else '')" 2>/dev/null; }

gates() {                                           # run inside a tree or the clone; $1 = an optional test module
  local log="${TMPDIR:-/tmp}/fleet-build.$$"
  for f in game/fleet/*.py; do
    python3 -I -B -c "import ast,sys; ast.parse(open(sys.argv[1], encoding='ascii').read(), sys.argv[1])" "$f" > "$log" 2>&1 || { echo "GATE syntax or non-ASCII: $f"; tail -3 "$log"; rm -f "$log"; return 1; }
  done
  python3 -B game/fleet/routes.py check > "$log" 2>&1 || { echo "GATE routes check:"; tail -5 "$log"; rm -f "$log"; return 1; }
  if ls "${FLEET_DATA_ROOT:-/srv/collective/data}"/catalog/[0-9]*.json > /dev/null 2>&1; then      # the reserve and its chosen recipes, against the catalog on file
    python3 -I -B game/fleet/surplus.py check > "$log" 2>&1 || { echo "GATE reserve (game/reserve.tsv, game/reserve-recipes.tsv):"; tail -5 "$log"; rm -f "$log"; return 1; }
  fi
  python3 -I -B game/fleet/needs.py check > "$log" 2>&1 || { echo "GATE needs (game/needs.tsv; its refs when a catalog is on file):"; tail -5 "$log"; rm -f "$log"; return 1; }
  python3 -B scripts/fleet-index.py --check > "$log" 2>&1 || { echo "GATE fleet index (run: python3 -B scripts/fleet-index.py):"; tail -4 "$log"; rm -f "$log"; return 1; }
  python3 -B scripts/validate-intel.py > "$log" 2>&1 || { echo "GATE validate-intel:"; tail -5 "$log"; rm -f "$log"; return 1; }
  bash scripts/validate-ids.sh > "$log" 2>&1 || { echo "GATE validate-ids:"; tail -5 "$log"; rm -f "$log"; return 1; }
  if [ -n "${1:-}" ]; then
    python3 -B -m unittest "$1" > "$log" 2>&1
  else
    python3 -B - <<'PY' > "$log" 2>&1
from concurrent.futures import ThreadPoolExecutor, as_completed
import glob, subprocess, sys

files = sorted(glob.glob("scripts/tests/test_*.py"))
failed = []
def run_one(f):
    r = subprocess.run([sys.executable, "-B", f], capture_output=True, text=True, timeout=300)
    return f, r.returncode, r.stdout + r.stderr

with ThreadPoolExecutor(max_workers=4) as pool:
    futs = [pool.submit(run_one, f) for f in files]
    for fut in as_completed(futs):
        f, rc, out = fut.result()
        if rc != 0:
            failed.append((f, rc, out))

if failed:
    for f, rc, out in failed:
        print(f"FAIL: {f} (rc={rc})\n{out[-1200:]}")
    sys.exit(1)
print(f"OK ({len(files)} test files passed in parallel)")
PY
  fi
  local code=$?
  [ $code -eq 0 ] || { echo "GATE unit tests:"; grep -E '^(FAIL|ERROR)|Error' "$log" | head -8; tail -3 "$log"; }
  [ $code -eq 0 ] && tail -1 "$log"
  rm -f "$log"; find . -name __pycache__ -not -path './.git/*' -type d -exec rm -rf {} + 2>/dev/null
  return $code
}

case "$verb" in
tree)
  [ -e "$T" ] && { echo "HALT: $T exists: name a new folder"; exit 1; }
  case "$(cd "$(dirname "$T")" 2>/dev/null && pwd)/" in "$R"/*) echo "HALT: the copy must lie outside the clone (your scratch folder)"; exit 1;; esac
  mkdir -p "$T" && git -C "$R" archive HEAD | tar -x -C "$T" || { echo "HALT: could not make the copy"; exit 1; }
  git -C "$R" rev-parse HEAD > "$T/.base"
  echo "copy of $(cut -c1-7 "$T/.base") at $T | change files there, then: fleet-build.sh test $T"
  ;;
test)
  [ -f "$T/.base" ] || { echo "HALT: $T is no copy made by \`fleet-build.sh tree\`"; exit 1; }
  [ -d "$T/.git" ] || git -C "$T" init -q || { echo "HALT: could not make the copy a git folder"; exit 1; }   # validate-ids.sh lists the Markdown by `git ls-files` (32416700): an empty repository lists every file as untracked
  cd "$T" && gates "${3:-}" && echo "PASS: the gates hold in the copy"
  ;;
install)
  MSG=${3:-}; shift 3 2>/dev/null; PATHS=("$@")
  [ -n "$MSG" ] && [ ${#PATHS[@]} -ge 1 ] || usage
  [ -f "$T/.base" ] || { echo "HALT: $T is no copy made by \`fleet-build.sh tree\`"; exit 1; }
  NAME=$(who); [ -n "$NAME" ] || { echo "HALT: this shell is no member of the Collective: nothing installed"; exit 1; }
  BASE=$(cat "$T/.base"); script=0; test=0
  for p in "${PATHS[@]}"; do
    case "$p" in /*|*..*) echo "HALT: a path is relative to the repository: $p"; exit 1;; esac
    [ -f "$T/$p" ] || { echo "HALT: not a file in your copy: $p"; exit 1; }
    if [ "$NAME" != "Unity" ] && printf '%s\n' "$p" | grep -q -E "$CLOSED"; then echo "HALT: $p is the Fleet Admiral's to change: ask in requests.log"; exit 1; fi
    case "$p" in game/fleet/*.py) script=1;; scripts/tests/*) test=1;; esac
  done
  [ $script -eq 1 ] && [ $test -eq 0 ] && { echo "HALT: a changed script under game/fleet/ comes with its test: name a path under scripts/tests/ too"; exit 1; }
  cd "$R" || exit 1
  LIMIT=${FLEET_BUILD_LIMIT:-1500}                   # seconds the install may take from its copy on: its own timeout (ENT-115)
  trap 'echo "HALT: stopped before anything was copied: nothing to put back"; exit 1' INT TERM HUP
  n=0; while [ -n "$(git status --short)" ] && [ $n -lt 48 ]; do sleep 5; n=$((n + 1)); done
  [ -z "$(git status --short)" ] || { echo "HALT: the clone was not clean in four minutes: [$(git status --short | head -3 | tr '\n' ';')]"; exit 1; }
  for p in "${PATHS[@]}"; do
    git diff --quiet "$BASE" HEAD -- "$p" 2>/dev/null || { echo "HALT: $p changed in the repository since your copy was made ($(git log -1 --format='%h %an' -- "$p")): make a new copy and carry your change over"; exit 1; }
  done
  GATES=; WATCH=
  undo() {
    trap '' INT TERM HUP                            # one undo, never cut by a second signal
    [ -n "$GATES" ] && { pkill -TERM -P "$GATES" 2>/dev/null; kill -TERM "$GATES" 2>/dev/null; wait "$GATES" 2>/dev/null; }
    [ -n "$WATCH" ] && kill -TERM "$WATCH" 2>/dev/null
    rm -f "${TMPDIR:-/tmp}/fleet-build.$$"           # the log of gates that were stopped
    echo "HALT: $1 -- putting the paths back"
    git reset -q -- "${PATHS[@]}" 2>/dev/null
    for p in "${PATHS[@]}"; do if git cat-file -e "HEAD:$p" 2>/dev/null; then git checkout -q HEAD -- "$p"; else rm -f -- "$p"; fi; done
    echo "status after: [$(git status --short)]"; exit 1
  }
  trap 'undo "stopped (INT)"' INT; trap 'undo "stopped (TERM)"' TERM; trap 'undo "stopped (HUP)"' HUP
  ( trap 'kill "$s" 2>/dev/null; exit 0' TERM; sleep "$LIMIT" & s=$!; wait "$s"; echo "HALT: the install ran past its limit of $LIMIT s (FLEET_BUILD_LIMIT)"; kill -TERM $$ ) &
  WATCH=$!
  for p in "${PATHS[@]}"; do mkdir -p "$(dirname "$p")" && cp "$T/$p" "$p" || undo "copy $p"; done
  if LC_ALL=C grep -nP '[^\x00-\x7F]' "${PATHS[@]}" | head -3 | grep .; then undo "non-ASCII"; fi
  gates "" & GATES=$!                                # in the background: a signal is taken at once, not after the suite
  wait "$GATES" || undo "a gate failed"
  GATES=
  git add -- "${PATHS[@]}" || undo "git add"
  git -c user.name="$NAME" -c user.email="$(printf '%s' "$NAME" | tr 'A-Z' 'a-z')@suggi-workspace.dev" commit -q -m "$MSG" -- "${PATHS[@]}" || undo "git commit"
  trap - INT TERM HUP; kill -TERM "$WATCH" 2>/dev/null   # committed: nothing to put back any more
  git log -1 --format='committed %h %an %s' | cut -c1-120
  echo "status after: [$(git status --short)] | now one line in queue.log: what changed, for whom, and its test"
  ;;
*) usage;;
esac

#!/usr/bin/env python3
"""needs.py -- the fleet's needs register: what each division needs for its upgrades and for the empire, one row a need in game/needs.tsv, written by this script alone; the open needs are the reserve's targets, covered by stock in priority order.

WHAT: game/needs.tsv holds the needs, one row each: id, project (what it serves: "Atria outpost", "miner hulls tier
      2"), division (its owner: command, mining, trade, logistics, military, intel), kind (facility, hull or item),
      ref (the catalog's id), units, priority (1 high to 3), place (a base or station id, or empty), due (a UTC date,
      or empty), status (open, done or dropped), note, added and changed (UTC, with the member that did it). This
      script is the one writer of the file and the one answer from it:
        list      the open needs, highest priority first, each with its covered percent, its colour and what is short
        show      one need whole, or every need of one project: what it takes, what stock covers and where it lies,
                  what is still to gather, craft or buy
        items     per item for the whole fleet: gross need, held, net short (surplus.py's one walk of all open needs)
        add, set, done, drop   one change of one row, committed by path as the member
        tidy      the file written again in its one form, the closed rows past CLOSED_DAYS taken out
        check     the gate: every row valid, every ref known to the catalog, the caps held, the file in its one
                  form, no target left in game/reserve.tsv; exit 1 on an error
      For the other scripts: targets() gives surplus.py the open needs as the reserve's targets (so pull.py, fill.py,
      hunt.py, stats.py and every reader of surplus.surplus take them); status() is the gross to net per need; the
      store mirrors the file into the table needs (SNAPSHOT, need_files) and writes need_status on its pass
      (compute()); mcp_tool() is the MCP tool `needs`; briefing() the briefing's line; hive() the verb `hive.py needs`.
RULES:
  - The file is tab-separated, `#` starts a comment, the header `id<TAB>project<TAB>division<TAB>kind<TAB>ref<TAB>units<TAB>
    priority<TAB>place<TAB>due<TAB>status<TAB>note<TAB>added<TAB>added_by<TAB>changed<TAB>changed_by` comes first. It is
    written by this script only, in one form (sorted by division, open first, priority, id); `check` fails a file
    in another form (a hand edit): `tidy` writes it again.
  - A row: id (2 to 32 lower-case letters, digits and dashes, once in the file), project (1 to PROJECT_MAX
    characters), division, kind, ref (a facility id, a ship class id or an item id of the catalog), units (a whole
    number above 0), priority (1, 2 or 3), place (empty or a base id: lower-case letters, digits, underscores),
    due (empty or YYYY-MM-DD), status, note (at most NOTE_MAX characters), added and changed (YYYY-MM-DDTHH:MMZ),
    added_by and changed_by (a member). No tab inside a cell; ASCII only.
  - Caps: at most MAX_OPEN open needs a division; a write that would break a cap or a rule changes nothing.
  - A member writes the rows of its own division (board.NAMES: Zero mining, Mercury trade, Apollo logistics,
    Apophis military, Oracle intel); the Fleet Admiral writes any and alone moves a need to another division. A shell
    that is no member writes nothing (division.member, as plan.py asks).
  - One writer at a time: the lock <repository>/.git/needs.lock, held from the reading to the commit. A file that
    holds a change not committed (a hand edit, or another write in work) is refused. The file is committed by path
    under the member's name; a commit git refuses six times puts the file back as it was. --dry-run says what a write
    would change and writes nothing.
  - The open needs are the reserve's targets (rule F24): game/reserve.tsv keeps only the policy lines (keep,
    keepkind, max, min); a facility, hull or item line there is an error of `check` (one demand, never two). A row
    with an error, or whose ref the catalog does not hold, is skipped by surplus.py with a NOTE.
  - Gross to net per need: the open needs in priority order (priority, then due with none last, then added, then id)
    each meet what is left of the stock after the needs before it (surplus.meet, the reserve's own walk, with the
    recipes of game/reserve-recipes.tsv; stock is craftbook.inventory: station storage, the holds and the faction's
    storage in the storage book). Covered = the share of the need's raw units (everything it takes, broken down to
    what is mined, hunted or bought, as if nothing were held) that stock covers, held as it is or made from what is
    held. Colour: green when nothing is short, yellow from RED percent, red under it. What is still short: to gather
    (mined), to buy, hunt or loot (no recipe), to craft (the recipe runs still to make). The fleet's figures per item
    stay surplus.py's (one walk of all open needs together); a need's share is this walk's.
  - A need past its due date or unchanged for STALE_DAYS is marked stale in every answer; it reserves all the same.
    A facility need says how many of that facility our empire holds already (empire.json), a hint to close it.
  - Closed rows (done, dropped) stay in the file with their status for CLOSED_DAYS after their change, so the store
    and every reader see what was finished; then the next write takes them out (PRUNE_CLOSED; `tidy` does too) and the
    repository's history keeps every version. They reserve nothing.
  - The store (store.py) loads the file into the table needs whenever it changed and writes need_status on its pass
    when the file changed or EVERY seconds passed (meta needs.at, needs.error, needs.seconds).
WHY:  Suggi, 2026-11-21: "A required materials list, or needed materials, where everyone can contribute and say what
      in their division is needed for upgrades and the main progression overall, so for bases and stuff ... in the
      MCP as well or via SQL." The reserve's targets were one file kept by hand by the Fleet Admiral alone, with no
      owner, no priority and no end: two needs on one scarce good had no order.

USAGE:
  needs.py list [<division>|<Member>|all] [--project <text>] [--all]
  needs.py show <id>|<project text>
  needs.py items
  needs.py add <facility|hull|item> <ref> <units> --project "<text>" [--priority 1|2|3] [--place <base id>] [--due YYYY-MM-DD] [--note "<text>"] [--id <id>] [--division <name>] [--dry-run]
  needs.py set <id> [--project ..] [--kind ..] [--ref ..] [--units N] [--priority N] [--place ..] [--due ..] [--note ..] [--status open|done|dropped] [--division ..] [--dry-run]
  needs.py done <id> [--note "<text>"] [--dry-run]
  needs.py drop <id> [--note "<text>"] [--dry-run]
  needs.py tidy [--dry-run]
  needs.py check
  --root <dir>      the repository (default: two folders above this file)
  --data <dir>      the unit's data folder (default /srv/collective/data)
  --where and --by are taken for --place and --due; `-` or `none` empties a cell.

Stdlib only. ASCII only.
"""

import calendar
import fcntl
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import board                                      # noqa: E402  the divisions' names
import division                                   # noqa: E402  who asks, the data folder's default

# surplus.py and store.py import this file: craftbook, surplus and store are imported inside the functions that need them.

FILE = "game/needs.tsv"                           # under the repository
NAME = FILE                                       # its name in the store's table source
RESERVE = "game/reserve.tsv"                      # the policy lines (surplus.py reads them); a target there is an error of check
HEADER = ["id", "project", "division", "kind", "ref", "units", "priority", "place", "due", "status", "note", "added", "added_by", "changed", "changed_by"]
NEED_KINDS = ("facility", "hull", "item")
TABLE = {"facility": "facilities", "hull": "ships", "item": "items"}      # the catalog's table of each kind
STATUSES = ("open", "done", "dropped")
DIVISIONS = {board.NAMES[member].lower(): member for member in division.MEMBERS}   # command Unity, mining Zero, logistics Apollo, ...
ORDER = list(DIVISIONS)
MAX_OPEN = 20                  # open needs a division at most
NOTE_MAX = 200                 # characters of a note at most
PROJECT_MAX = 80               # characters of a project at most
STALE_DAYS = 7                 # an open need unchanged this long is stale (it reserves all the same)
CLOSED_DAYS = 14               # a done or dropped row stays this long after its change, then a write takes it out
PRUNE_CLOSED = True            # the next write takes the closed rows past CLOSED_DAYS out (off: only `tidy` does)
RED = 50                       # covered percent under this is red; from it yellow; nothing short is green
EVERY = 300                    # seconds: the store computes need_status again at least this often
DAY = 86400
ID = re.compile(r"^[a-z0-9][a-z0-9-]{1,31}$")
REF = re.compile(r"^[a-z0-9_]+$")
PLACE = re.compile(r"^[a-z0-9_]{2,64}$")
DUE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
STAMP = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}Z$")
EMPTY = ("-", "none", "--")
VALUED = ("--root", "--data", "--project", "--priority", "--place", "--where", "--due", "--by", "--note", "--id", "--division", "--units",
          "--kind", "--ref", "--status")
COLOURS = ("red", "yellow", "green", "broken")
RULE = ("covered = the share of a need's raw units (all it takes, down to what is mined, hunted or bought) that stock covers, held or made "
        "from what is held; stock goes to the needs in priority order (priority, due, added); red under %d percent, yellow %d to 99, green "
        "nothing short" % (RED, RED))
COMMENT = """# The needs register: what each division needs for its upgrades and for the empire, one row a need. The open needs
# are the reserve's targets (rule F24): surplus.py, pull.py and every reader of the reserve take them; game/reserve.tsv
# keeps only the policy lines (keep, keepkind, max, min).
# WRITTEN BY game/fleet/needs.py ONLY, never by hand: needs.py add|set|done|drop (or the MCP tool `needs`); a member
# writes the rows of its own division, the Fleet Admiral any. `needs.py check` is the gate. What a need is: game/needs.md.
# Tab-separated; `#` starts a comment. kind: facility (a facility id, units = how many) | hull (a ship class id) |
# item (an item id, units on hand). priority 1 high to 3. status open | done | dropped (closed rows leave after %d days).
""" % CLOSED_DAYS
num = "{:,}".format


class Refused(Exception):
    """A write that changes nothing: the reason says why."""


# ---- the file

def path_of(repo):
    return Path(repo) / FILE


def now_stamp(now=None):
    return time.strftime("%Y-%m-%dT%H:%MZ", time.gmtime(time.time() if now is None else now))


def epoch(stamp):
    for form in ("%Y-%m-%dT%H:%MZ", "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%d"):
        try:
            return calendar.timegm(time.strptime(str(stamp or ""), form))
        except ValueError:
            continue
    return None


def row_of(number, cells, seen):
    """One row of the file: its cells by the header, units and priority as numbers where they are, `line`, and `errors`
    (every rule it breaks; an empty list for a good row)."""
    errors = []
    if len(cells) != len(HEADER):
        errors.append("%d cells, the header has %d (a tab inside a cell?)" % (len(cells), len(HEADER)))
    row = dict(zip(HEADER, (cells + [""] * len(HEADER))[:len(HEADER)]))
    if any(ord(c) > 127 for c in "".join(cells)):
        errors.append("not ASCII")
    if not ID.match(row["id"]):
        errors.append("id `%s`: 2 to 32 lower-case letters, digits and dashes" % row["id"])
    elif row["id"] in seen:
        errors.append("id %s stands on line %d too" % (row["id"], seen[row["id"]]))
    seen.setdefault(row["id"], number)
    if not row["project"] or len(row["project"]) > PROJECT_MAX:
        errors.append("project: 1 to %d characters (%d)" % (PROJECT_MAX, len(row["project"])))
    if row["division"] not in DIVISIONS:
        errors.append("division `%s`: one of %s" % (row["division"], ", ".join(ORDER)))
    if row["kind"] not in NEED_KINDS:
        errors.append("kind `%s`: one of %s" % (row["kind"], ", ".join(NEED_KINDS)))
    if not REF.match(row["ref"]):
        errors.append("ref `%s` is no catalog id" % row["ref"])
    if row["units"].isdigit() and int(row["units"]) > 0:
        row["units"] = int(row["units"])
    else:                                                       # a bad cell keeps its text: tidy writes it back as it stood
        errors.append("units must be a whole number above 0, not `%s`" % row["units"])
    if row["priority"] in ("1", "2", "3"):
        row["priority"] = int(row["priority"])
    else:
        errors.append("priority must be 1, 2 or 3, not `%s`" % row["priority"])
    if row["place"] and not PLACE.match(row["place"]):
        errors.append("place `%s`: empty or a base id (lower-case letters, digits, underscores)" % row["place"])
    if row["due"] and (not DUE.match(row["due"]) or epoch(row["due"]) is None):
        errors.append("due `%s`: empty or a date YYYY-MM-DD" % row["due"])
    if row["status"] not in STATUSES:
        errors.append("status `%s`: one of %s" % (row["status"], ", ".join(STATUSES)))
    if len(row["note"]) > NOTE_MAX:
        errors.append("note: %d characters, at most %d" % (len(row["note"]), NOTE_MAX))
    for key in ("added", "changed"):
        if not STAMP.match(row[key]) or epoch(row[key]) is None:
            errors.append("%s `%s`: a UTC time YYYY-MM-DDTHH:MMZ" % (key, row[key]))
        if row[key + "_by"] not in division.MEMBERS:
            errors.append("%s_by `%s`: a member (%s)" % (key, row[key + "_by"], ", ".join(division.MEMBERS)))
    row["line"], row["errors"] = number, errors
    return row


def parse(text):
    """(rows, problem) of the file's text: problem is '' or why the whole file cannot be read (no header)."""
    rows, header, seen = [], False, {}
    for number, raw in enumerate(text.split("\n"), 1):
        line = raw.rstrip("\r")
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        cells = [cell.strip() for cell in line.split("\t")]
        if not header:
            if cells != HEADER:
                return [], "line %d: the header `%s` must come before the first need" % (number, "<TAB>".join(HEADER))
            header = True
            continue
        rows.append(row_of(number, cells, seen))
    return rows, "" if header or not rows else "no header"


def read(repo):
    """(rows, problem, present) of the repository's file. No file: no needs, no problem."""
    try:
        text = path_of(repo).read_bytes().decode("ascii")
    except FileNotFoundError:
        return [], "", False
    except (OSError, UnicodeDecodeError) as error:
        return [], "%s: not readable as ASCII (%s)" % (FILE, type(error).__name__), True
    rows, problem = parse(text)
    return rows, problem, True


def prio(row):
    return row["priority"] if isinstance(row.get("priority"), int) else 9


def units_text(units):
    return num(units) if isinstance(units, int) else (units or "?")


def sort_key(row):
    return (ORDER.index(row["division"]) if row["division"] in ORDER else 99, row["status"] != "open", prio(row), row["id"])


def render(rows):
    """The file's one form: the comment, the header, the rows by division, open first, priority, id."""
    lines = [COMMENT.rstrip("\n"), "\t".join(HEADER)]
    for row in sorted(rows, key=sort_key):
        lines.append("\t".join("" if row.get(key) is None else str(row.get(key)) for key in HEADER))
    return "\n".join(lines) + "\n"


def order(row):
    """The order stock is given to the open needs: priority, due (none last), added, id."""
    return (prio(row), row["due"] or "9999-12-31", row["added"] or "", row["id"])


def stale(row, now):
    """Why an open need is stale ('' when it is not): past its due date, or unchanged for STALE_DAYS."""
    if row.get("status") != "open":
        return ""
    if row.get("due") and row["due"] < time.strftime("%Y-%m-%d", time.gmtime(now)):
        return "past due %s" % row["due"]
    changed = epoch(row.get("changed"))
    if changed is not None and now - changed >= STALE_DAYS * DAY:
        return "unchanged %d days" % ((now - changed) // DAY)
    return ""


def closed_out(row, now):
    """True for a done or dropped row whose change lies CLOSED_DAYS back or more: the next write takes it out."""
    changed = epoch(row.get("changed"))
    return row.get("status") in ("done", "dropped") and changed is not None and now - changed >= CLOSED_DAYS * DAY


def reserve_targets(repo):
    """[line numbers] of game/reserve.tsv that still name a target (facility, hull or item): one demand, never two."""
    try:
        text = (Path(repo) / RESERVE).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return []
    found = []
    for number, raw in enumerate(text.split("\n"), 1):
        cells = [c.strip() for c in raw.split("\t")]
        if not raw.lstrip().startswith("#") and cells and cells[0] in NEED_KINDS:
            found.append(number)
    return found


def validate(rows, cat, repo=None):
    """(errors, warnings) of the whole register: every row's own errors, its ref against the catalog (when there is one),
    the cap of open needs a division; with repo also the targets left in game/reserve.tsv."""
    errors, warnings = [], []
    for row in rows:
        errors += ["%s line %d (%s): %s" % (FILE, row["line"], row["id"] or "?", e) for e in row["errors"]]
        if cat is not None and row["kind"] in TABLE and row["ref"] not in cat[TABLE[row["kind"]]] and row["status"] == "open":
            errors.append("%s line %d (%s): no %s `%s` in the catalog %s" % (FILE, row["line"], row["id"], row["kind"], row["ref"], cat.get("version")))
    for name in ORDER:
        count = sum(1 for r in rows if r["division"] == name and r["status"] == "open")
        if count > MAX_OPEN:
            errors.append("%s: %d open needs of %s, at most %d (MAX_OPEN): close or drop some" % (FILE, count, name, MAX_OPEN))
    if repo is not None:
        errors += ["%s line %d: a target (facility, hull or item) stands in the reserve file: the targets are the open needs of %s "
                   "(needs.py add), the reserve file keeps keep, keepkind, max and min" % (RESERVE, n, FILE) for n in reserve_targets(repo)]
    return errors, warnings


# ---- the reserve's targets (surplus.py)

def targets(repo, cat, notes=None):
    """The open needs as targets of surplus.py's walk: [{line, kind, id (the ref), units, note, need, division, priority}],
    in priority order. A row with an error, or a ref the catalog does not hold, is skipped with a note."""
    notes = [] if notes is None else notes
    rows, problem, _present = read(repo)
    if problem:
        notes.append("%s: %s: no need counts (needs.py check)" % (FILE, problem))
    out = []
    for row in sorted((r for r in rows if r["status"] == "open"), key=order):
        if row["errors"]:
            notes.append("%s line %d (%s): %s: skipped (needs.py check)" % (FILE, row["line"], row["id"], row["errors"][0]))
            continue
        if row["ref"] not in (cat or {}).get(TABLE[row["kind"]], {}):
            notes.append("%s line %d (%s): no %s `%s` in the catalog %s: skipped" % (FILE, row["line"], row["id"], row["kind"], row["ref"], (cat or {}).get("version")))
            continue
        if facility_built_at_place(row, division.DATA, cat):
            notes.append("%s line %d (%s): already stands at %s in empire.json: skipped" % (FILE, row["line"], row["id"], row["place"]))
            continue
        out.append({"line": row["line"], "kind": row["kind"], "id": row["ref"], "units": row["units"], "need": row["id"], "division": row["division"],
                    "priority": row["priority"], "note": "need %s (%s, priority %d): %s%s" % (row["id"], row["division"], row["priority"], row["project"],
                                                                                          " | " + row["note"] if row["note"] else "")})
    return out


def said(res):
    """The part of surplus.py's first line that names the needs among its targets ('' when there are none)."""
    count = sum(1 for t in res.get("targets") or [] if t.get("need"))
    if not count:
        return ""
    return (" | %d of them open needs of %s (needs.py)" if res.get("present") else " | but %d open needs of %s are its targets (needs.py)") % (count, FILE)


# ---- gross to net per need

def takes(cat, row):
    """({item: units} a need asks for at the top, its fee in credits or None): a facility's or hull's build materials times
    its units (surplus.py's reading of a target), an item itself."""
    if row["kind"] == "item":
        return {row["ref"]: row["units"]}, None
    found = cat[TABLE[row["kind"]]][row["ref"]]
    out = {}
    for m in found.get("build_materials") or []:
        if (m.get("quantity") or 0) > 0:
            out[m.get("item_id")] = out.get(m.get("item_id"), 0) + m["quantity"] * row["units"]
    return out, (found.get("build_cost") or 0) * row["units"] if row["kind"] == "facility" else None


def built(data):
    """{facility type: how many our empire holds} from empire/empire.json (empire.py collect); {} when not read."""
    try:
        found = json.loads((Path(data) / "empire" / "empire.json").read_text(encoding="utf-8")).get("facilities") or []
    except (OSError, ValueError, AttributeError):
        return {}
    out = {}
    for row in found if isinstance(found, list) else []:
        if isinstance(row, dict) and row.get("type"):
            out[row["type"]] = out.get(row["type"], 0) + 1
    return out


def facility_built_at_place(row, data, cat=None):
    """True when a facility need names a specific `place` and `empire.json` already holds at least `units` of that
    facility (or a higher tier upgraded from it) at that base/system -- preventing phantom reserve lockups after a build."""
    if row.get("kind") != "facility" or not row.get("place"):
        return False
    try:
        found = json.loads((Path(data) / "empire" / "empire.json").read_text(encoding="utf-8")).get("facilities") or []
    except (OSError, ValueError, AttributeError):
        return False
    valid = {row["ref"]}
    fac_cat = (cat or {}).get("facilities") or {}
    if isinstance(fac_cat, dict) and fac_cat:
        changed = True
        while changed:
            changed = False
            for fid, fdef in fac_cat.items():
                if isinstance(fdef, dict) and fdef.get("upgrades_from") in valid and fid not in valid:
                    valid.add(fid)
                    changed = True
    place = row["place"]
    cnt = sum(
        1 for f in (found if isinstance(found, list) else [])
        if isinstance(f, dict) and f.get("type") in valid and place in (f.get("base"), f.get("system"))
    )
    return cnt >= int(row.get("units") or 1)


UNIQUE_FACTION_OFFICES = frozenset(("guild_hall_recruiting", "grand_recruitment_bureau", "station_core_foundry"))


def need_fulfilled_reason(row, data, cat=None):
    '''Return a concise audit reason when an open need in needs.tsv is already physically completed
    in live game state (empire.json facilities/bases or fleet.json hulls), else ''.'''
    if row.get("status") != "open":
        return ""
    kind = row.get("kind")
    ref = str(row.get("ref") or "")
    want = int(row.get("units") or 1)
    if kind == "facility":
        if row.get("place") and facility_built_at_place(row, data, cat):
            return "auto-closed: %s active at %s (empire.json)" % (ref, row["place"])
        if not row.get("place") and ref in UNIQUE_FACTION_OFFICES and built(data).get(ref, 0) >= want:
            return "auto-closed: %s active in empire.json" % ref
        return ""
    if kind == "hull":
        try:
            ships = (json.loads((Path(data) / "fleet" / "fleet.json").read_text(encoding="utf-8")).get("ships")) or []
        except (OSError, ValueError, AttributeError):
            return ""
        div = str(row.get("division") or "").lower()
        owned = sum(
            1 for s in ships
            if isinstance(s, dict)
            and (not div or str(s.get("division") or "").lower() == div)
            and str(s.get("class") or "").lower().replace(" ", "_") == ref.lower()
        )
        if owned >= want:
            return "auto-closed: %d %s hull(s) active in %s fleet (fleet.json)" % (owned, ref, row.get("division") or "our")
        return ""
    if kind == "item" and ref == "outpost_kit":
        try:
            bases = (json.loads((Path(data) / "empire" / "empire.json").read_text(encoding="utf-8")).get("bases")) or []
        except (OSError, ValueError, AttributeError):
            return ""
        hay = (" " + str(row.get("id") or "").replace("-", "_") + " " + str(row.get("project") or "").lower().replace("-", "_") + " ")
        for b in bases:
            sy = str((b or {}).get("system") or "").strip().lower()
            if sy and re.search(r"(?<![a-z0-9_])" + re.escape(sy) + r"(?![a-z0-9_])", hay):
                return "auto-closed: outpost active in %s (empire.json)" % sy
    return ""


def reconciler(who, data, cat):
    def change(rows, now):
        closed_ids = []
        out = []
        for r in rows:
            why = need_fulfilled_reason(r, data, cat) if r.get("status") == "open" and may(who, r.get("division", "")) else ""
            if why:
                nr = dict(r)
                nr["status"] = "done"
                old_note = str(nr.get("note") or "").strip()
                nr["note"] = cell((why + (" | " + old_note if old_note else ""))[:NOTE_MAX], "note")
                nr["changed"], nr["changed_by"] = now_stamp(now), who
                out.append(nr)
                closed_ids.append(nr["id"])
            else:
                out.append(r)
        if not closed_ids:
            return rows, "", ""
        return out, ",".join(closed_ids), "all"
    return change


def reconcile(repo, data, who, dry=False, now=None):
    '''Auto-close open needs whose target facility, hull or outpost is verified live in empire.json/fleet.json.'''
    import craftbook
    import surplus
    repo_p = Path(repo)
    if not path_of(repo_p).is_file():
        return 0, []
    rows, problem, present = read(repo_p)
    if not present or problem:
        return 0, []
    cat = craftbook.choose(craftbook.load(data) or dict(surplus.EMPTY), repo_p)
    hits = [(r["id"], need_fulfilled_reason(r, data, cat)) for r in rows if r.get("status") == "open"]
    hits = [(rid, why) for rid, why in hits if why]
    if not hits:
        return 0, []
    if dry:
        return 0, ["would auto-close %s: %s" % (rid, why) for rid, why in hits]
    return write(repo_p, data, who, reconciler(who, data, cat), "done", False, now=now)


def colour_of(covered, short):
    if covered is None:
        return "broken"
    return "green" if short <= 0 else "yellow" if covered >= RED else "red"


def listed(pairs, most=6):
    """`a 3, b 2 +4 more` of [(name, units)], the most units first."""
    pairs = sorted(pairs, key=lambda p: (-p[1], p[0]))
    text = ", ".join("%s %s" % (name, num(units)) for name, units in pairs[:most])
    return text + (" +%d more" % (len(pairs) - most) if len(pairs) > most else "")


def status(data, repo, cat=None, now=None, rows=None):
    """The gross to net of every open need in priority order: {written, catalog, present, problem, rows (every row of the
    file), needs: [entry], reach: {item: [need ids]}}. An entry is the row's cells and rank, stale, takes {item: units},
    fee, raw_units, raw_short, covered (percent, None for a broken need), colour, short {item: units} (what is mined,
    hunted or bought and still missing), gather, buy {item: units}, craft [(item, units to make, runs, recipe, how)],
    stock {item: units taken from stock}, at {item: {place: units held there}}, stands (facilities of its kind our empire
    holds, None for an item or hull), problem (why it is broken)."""
    import craftbook                              # the catalog, the inventory
    import surplus                                # the reserve's own walk (meet)
    now = time.time() if now is None else now
    cat = craftbook.choose(cat or craftbook.load(data) or dict(surplus.EMPTY), repo)
    problem, present = "", True
    if rows is None:
        rows, problem, present = read(repo)
    inv = craftbook.inventory(data, cat)
    have = {r["id"]: r for g in inv["groups"] for r in g["rows"]}
    left = {item: r["units"] for item, r in have.items()}
    stands = built(data)
    out, reach = [], {}
    for rank, row in enumerate(sorted((r for r in rows if r["status"] == "open"), key=order), 1):
        entry = dict(row, rank=rank, stale=stale(row, now), takes={}, fee=None, raw_units=0, raw_short=0, covered=None, short={}, gather={}, buy={},
                     craft=[], stock={}, at={}, stands=stands.get(row["ref"], 0) if row["kind"] == "facility" else None, problem="")
        out.append(entry)
        if row["errors"]:
            entry.update(colour="broken", problem=row["errors"][0])
            continue
        if row["ref"] not in cat[TABLE[row["kind"]]]:
            entry.update(colour="broken", problem="no %s `%s` in the catalog %s" % (row["kind"], row["ref"], cat["version"]))
            continue
        if facility_built_at_place(row, data, cat):
            entry.update(covered=100.0, colour="green", fee=0, stands=max(1, entry.get("stands") or 1))
            continue
        top, entry["fee"] = takes(cat, row)
        entry["takes"] = top
        labels = {item: {row["id"]} for item in top}
        gross = surplus.meet(cat, {}, top, labels)                      # as if nothing were held: the raw units it takes in all
        steps = surplus.meet(cat, left, top, labels)                    # against what the needs before it left
        entry["raw_units"] = sum(s["missing"] for s in gross.values())
        entry["short"] = {item: s["short"] for item, s in steps.items() if s["short"] > 0 and not s["recipe"]}
        entry["raw_short"] = min(entry["raw_units"], sum(entry["short"].values()))
        entry["covered"] = 100.0 if not entry["raw_units"] else max(0.0, 100.0 * (entry["raw_units"] - entry["raw_short"]) / entry["raw_units"])
        entry["colour"] = colour_of(entry["covered"], sum(entry["short"].values()))
        entry["gather"] = {i: n for i, n in entry["short"].items() if craftbook.mined(cat, i)}
        entry["buy"] = {i: n for i, n in entry["short"].items() if i not in entry["gather"]}
        entry["craft"] = [(i, s["make"], s["runs"], s["recipe"]["id"], "by hand" if s["recipe"].get("hand_craftable") else "facility")
                          for i, s in sorted(steps.items(), key=lambda kv: (-craftbook.rank(cat, kv[0]), kv[0])) if s["recipe"] and s["make"] > 0]
        for item, step in steps.items():
            reach.setdefault(item, []).append(row["id"])
            if step["taken"] > 0:
                entry["stock"][item] = step["taken"]
                entry["at"][item] = dict((have.get(item) or {}).get("at") or {})
                left[item] = max(0, left.get(item, 0) - step["taken"])
    return {"written": inv["written"], "catalog": cat["version"], "present": present, "problem": problem, "rows": rows, "needs": out, "reach": reach,
            "now": now, "cat": cat}


# ---- the answers

def first_line(title, res, rows=None):
    rows = res["rows"] if rows is None else rows
    return ("%s | %s: %d rows, %d open%s | storage book of %s | catalog %s" % (title, FILE, len(rows), sum(1 for r in rows if r["status"] == "open"),
                                                                            " | NOT READ: " + res["problem"] if res.get("problem") else "",
                                                                            res.get("written") or "-- (none yet)", res.get("catalog")))


def covered_text(entry):
    return "--" if entry["covered"] is None else "%d%%" % int(entry["covered"])      # floored: 99.6 stays 99, yellow


def short_text(entry):
    parts = []
    if entry["problem"]:
        parts.append("BROKEN: %s (needs.py check)" % entry["problem"])
    if entry["gather"]:
        parts.append("to gather " + listed(entry["gather"].items(), 4))
    if entry["buy"]:
        parts.append("to buy, hunt or loot " + listed(entry["buy"].items(), 4))
    if entry["craft"]:
        parts.append("to craft " + ", ".join("%s %s" % (i, num(n)) for i, n, _r, _rid, _how in entry["craft"][:3]) + (" +%d more" % (len(entry["craft"]) - 3)
                                                                                                                     if len(entry["craft"]) > 3 else ""))
    if entry["fee"]:
        parts.append("fee %s cr" % num(entry["fee"]))
    if entry["stands"]:
        parts.append("our empire holds %d %s already: done? (needs.py done %s)" % (entry["stands"], entry["ref"], entry["id"]))
    if entry["stale"]:
        parts.append("STALE: %s" % entry["stale"])
    return " | ".join(parts) or "nothing short"


def division_word(word):
    """The division a word names (a division, a member or a role), 'all', or None."""
    word = str(word or "").strip()
    if word.lower() in ("", "all"):
        return "all"
    if word.lower() in DIVISIONS:
        return word.lower()
    member = word.capitalize() if word.capitalize() in division.MEMBERS else division.ROLES.get(word.lower())
    return board.NAMES[member].lower() if member in board.NAMES else None


def show_list(res, which="all", project="", every=False):
    rows = [r for r in res["rows"] if (which == "all" or r["division"] == which) and (not project or project.lower() in r["project"].lower())]
    print(first_line("NEEDS | the open needs, highest priority first (the order stock is given to them)%s%s"
                     % ("" if which == "all" else " | division " + which, " | project ~ " + project if project else ""), res))
    print("  " + RULE)
    ids = {r["id"] for r in rows}
    mine = [e for e in res["needs"] if e["id"] in ids]
    if not mine:
        print("  no open need%s: needs.py add <facility|hull|item> <ref> <units> --project \"<text>\" (the tool needs, action=add)"
              % ("" if which == "all" else " of " + which))
    else:
        print("  %4s %-7s %7s  %-20s %-9s %3s %-8s %-30s %7s %-10s  %s" % ("rank", "colour", "covered", "id", "division", "pri", "kind", "ref", "units", "due", "project"))
    for e in mine:
        print("  %4d %-7s %7s  %-20s %-9s %3s %-8s %-30s %7s %-10s  %s" % (e["rank"], e["colour"], covered_text(e), e["id"][:20], e["division"], e["priority"] or "?",
                                                                          e["kind"], e["ref"][:30], units_text(e["units"]), e["due"] or "--", e["project"]))
        print("       %s" % short_text(e))
    if every:
        closed = [r for r in rows if r["status"] != "open"]
        if closed:
            print("  closed (they reserve nothing; they leave the file %d days after their change):" % CLOSED_DAYS)
        for r in closed:
            print("       %-7s %-20s %-9s %-8s %-30s %7s  %s | %s by %s%s" % (r["status"], r["id"][:20], r["division"], r["kind"], r["ref"][:30], units_text(r["units"]),
                                                                       r["project"], r["changed"], r["changed_by"], " | " + r["note"] if r["note"] else ""))
    counts = {c: sum(1 for e in mine if e["colour"] == c) for c in COLOURS}
    print("SUM | %d open: %d red, %d yellow, %d green%s, %d stale | %s" % (len(mine), counts["red"], counts["yellow"], counts["green"],
                                                                        ", %d broken" % counts["broken"] if counts["broken"] else "", sum(1 for e in mine if e["stale"]),
                                                                        ", ".join("%s %d" % (n, sum(1 for e in mine if e["division"] == n)) for n in ORDER
                                                                                  if any(e["division"] == n for e in mine)) or "no division"))
    return 0


def show_one(res, word):
    found = [r for r in res["rows"] if r["id"] == word] or [r for r in res["rows"] if word.lower() in r["project"].lower()]
    if not found:
        print(first_line("NEED %s" % word, res))
        print("  no need with this id and none whose project holds `%s`: needs.py list --all" % word)
        return 1
    entries = {e["id"]: e for e in res["needs"]}
    print(first_line("NEED %s" % (word if len(found) == 1 else "project ~ %s (%d needs)" % (word, len(found))), res))
    for row in sorted(found, key=lambda r: (entries[r["id"]]["rank"] if r["id"] in entries else 999, r["id"])):
        e = entries.get(row["id"])
        print("%s | %s | %s %s x %s | division %s | priority %s | %s | place %s | due %s%s"
              % (row["id"], row["project"], row["kind"], row["ref"], units_text(row["units"]), row["division"], row["priority"] or "?",
                 row["status"], row["place"] or "--", row["due"] or "--", " | STALE: %s" % e["stale"] if e and e["stale"] else ""))
        print("  added %s by %s, changed %s by %s%s" % (row["added"], row["added_by"], row["changed"], row["changed_by"], " | note: " + row["note"] if row["note"] else ""))
        for error in row["errors"]:
            print("  ERROR line %d: %s" % (row["line"], error))
        if not e:
            print("  closed: it reserves nothing")
            continue
        if e["problem"]:
            print("  BROKEN: %s" % e["problem"])
            continue
        print("  rank %d (stock is given to the needs in this order) | %s, covered %s | raw units %s, still short %s%s" % (
            e["rank"], e["colour"], covered_text(e), num(e["raw_units"]), num(e["raw_short"]), " | fee %s cr" % num(e["fee"]) if e["fee"] else ""))
        print("  takes: %s" % (listed(e["takes"].items(), 12) or "no build materials in the catalog"))
        print("  to gather (mined): %s" % (listed(e["gather"].items(), 12) or "nothing"))
        print("  to buy, hunt or loot (no recipe): %s" % (listed(e["buy"].items(), 12) or "nothing"))
        print("  to craft: %s" % ("; ".join("%s %s (%d runs of %s, %s)" % (i, num(n), runs, rid, how) for i, n, runs, rid, how in e["craft"][:10]) or "nothing")
              + (" +%d more" % (len(e["craft"]) - 10) if len(e["craft"]) > 10 else ""))
        print("  from stock: %s" % (listed(e["stock"].items(), 12) or "nothing"))
        for item, units in sorted(e["stock"].items(), key=lambda kv: (-kv[1], kv[0]))[:8]:
            places = sorted(e["at"].get(item, {}).items(), key=lambda kv: (-kv[1], kv[0]))
            print("    %-30s %10s taken | lies at %s" % (item[:30], num(units), ", ".join("%s %s" % (p, num(n)) for p, n in places[:4]) or "--"))
        if e["stands"]:
            print("  our empire holds %d %s already (empire.json): if this need is met, close it: needs.py done %s" % (e["stands"], e["ref"], e["id"]))
    print(RULE)
    return 0


def show_items(data, repo, res):
    """Per item for the whole fleet: surplus.py's one walk of all open needs (gross need, held, from stock, to make, short),
    with the needs that reach it from this script's walk."""
    import surplus
    whole = surplus.surplus(data, repo, res.get("cat"))
    print(first_line("NEEDS BY ITEM | every item the open needs take, for the whole fleet (surplus.py's walk of all of them together)", res))
    asked = sorted((r for r in whole["rows"] if r["demand"]), key=lambda r: (-r["level"], r["id"]))
    print("  %-30s %5s %-10s %12s %12s %12s %12s %12s  %s" % ("item", "level", "how", "gross need", "held", "from stock", "to make", "NET SHORT", "needs"))
    for r in asked:
        ids = res["reach"].get(r["id"]) or []
        print("  %-30s %5s %-10s %12s %12s %12s %12s %12s  %s" % (r["id"][:30], r["level"], r["how"][:10], num(r["demand"]), num(r["held"]), num(r["taken"]),
                                                                  num(r["make"]), num(r["short"]), ", ".join(ids[:4]) + (" +%d" % (len(ids) - 4) if len(ids) > 4 else "")))
    t = whole["totals"]
    print("SUM | %d items | net short %s units of %d items to mine, hunt or buy (%d items short in all) | fees %s cr" % (len(asked), num(t["short_raw"]), t["short_raw_items"],
                                                                                                             t["short_items"], num(t["fees"])))
    return 0


def check(data, repo):
    import craftbook
    cat = craftbook.load(data)
    rows, problem, present = read(repo)
    errors, warnings = validate(rows, cat, repo)
    if problem:
        errors.insert(0, problem)
    if present and not problem:
        text = path_of(repo).read_bytes().decode("ascii", "replace")
        if text != render(rows):
            errors.append("%s is not in the form needs.py writes (a hand edit?): needs.py tidy writes it again" % FILE)
    now = time.time()
    warnings += ["%s (%s): stale: %s" % (r["id"], r["division"], stale(r, now)) for r in rows if stale(r, now)]
    warnings += ["%s (%s): %s %s, %d days or more ago: the next write or needs.py tidy takes it out" % (r["id"], r["division"], r["status"], r["changed"], CLOSED_DAYS)
                 for r in rows if closed_out(r, now)]
    print("CHECK %s | %s | %d rows, %d open | catalog %s" % (FILE, "present" if present else "no file: no needs (no needs is no error)", len(rows),
                                                            sum(1 for r in rows if r["status"] == "open"),
                                                            cat["version"] + " (refs checked)" if cat else "none in %s/catalog: refs not checked" % data))
    for error in errors:
        print("  ERROR %s" % error)
    for warning in warnings:
        print("  WARNING %s" % warning)
    print("Errors: %d | Warnings: %d" % (len(errors), len(warnings)))
    return 1 if errors else 0


# ---- writing

def git(repo, *words):
    done = subprocess.run(["git", "-C", str(repo)] + list(words), capture_output=True, text=True)
    return done.returncode, (done.stdout + done.stderr).strip()


def dirty(repo):
    """The file's uncommitted change as git says it ('' when none, or no repository)."""
    if not (Path(repo) / ".git").exists():
        return ""
    code, out = git(repo, "status", "--porcelain", "--", FILE)
    return out if code == 0 else ""


def commit(repo, who, message):
    """(True, the short hash) or (False, why): the file committed by path under the member's name, six tries."""
    identity = ["-c", "user.name=" + who, "-c", "user.email=%s@suggi-workspace.dev" % who.lower()]
    out = ""
    for _attempt in range(6):                                  # another member's commit may hold the index for a moment
        code, out = git(repo, "add", "--", FILE)
        if code == 0:
            code, out = git(repo, *(identity + ["commit", "-q", "-m", message, "--", FILE]))
        if code == 0:
            return True, git(repo, "rev-parse", "--short", "HEAD")[1]
        time.sleep(2)
    return False, out[-300:]


def write(repo, data, who, change, verb, dry=False, now=None):
    """One write as one locked step: read the file, change(rows, now) -> (rows, the id changed, its division), prune the
    closed rows past CLOSED_DAYS (PRUNE_CLOSED), check the whole register, write, commit. (exit code, lines)."""
    import craftbook
    now = time.time() if now is None else now
    if not who:
        return 1, ["REFUSED: this shell is no member of The Collective: it writes no need"]
    repo = Path(repo)
    path = path_of(repo)
    lock = open(repo / ".git" / "needs.lock", "w") if (repo / ".git").is_dir() else None
    try:
        if lock is not None:
            fcntl.flock(lock, fcntl.LOCK_EX)                   # one writer at a time, from the reading to the commit
        held = dirty(repo)
        if held:
            return 1, ["REFUSED: %s holds a change that is not committed (`%s`): it is written by needs.py only; take it back "
                       "(git checkout -- %s) or commit it, then write again" % (FILE, held, FILE)]
        before = path.read_bytes().decode("ascii") if path.is_file() else None
        rows, problem = parse(before) if before is not None else ([], "")
        if problem:
            return 1, ["REFUSED: %s cannot be read (%s): take the hand edit back (git checkout -- %s)" % (FILE, problem, FILE)]
        try:
            rows, rid, where = change(rows, now)
        except Refused as why:
            return 1, ["REFUSED: %s" % why]
        gone = [r["id"] for r in rows if closed_out(r, now)] if PRUNE_CLOSED or verb == "tidy" else []
        rows = [r for r in rows if r["id"] not in gone]
        text = render(rows)
        rows, _problem = parse(text)                            # read back as the file will be read: line numbers and errors anew
        mine = [r for r in rows if r["id"] == rid]
        errors = [e for r in mine for e in r["errors"]]         # the row written, and the cap of its division (tidy: the caps)
        errors += [e for e in validate(rows, None)[0] if "MAX_OPEN" in e and (rid is None or " of %s, " % where in e)]
        cat = craftbook.load(data)
        if cat is not None:
            errors += [e for e in validate(mine, cat)[0] if "in the catalog" in e]
        errors = list(dict.fromkeys(errors))
        if errors:
            return 1, ["REFUSED: nothing changed: " + errors[0]] + ["  also: " + e for e in errors[1:6]]
        lines = ["%s %s%s%s" % ("WOULD WRITE" if dry else "wrote", FILE, " | %s %s (%s)" % (verb, rid, where) if rid else " | %s" % verb,
                                " | out, closed %d days or more: %s" % (CLOSED_DAYS, ", ".join(gone)) if gone else "")]
        lines += ["  " + " | ".join("%s %s" % (key, mine[0][key]) for key in HEADER if mine[0][key] not in ("", None))] if mine else []
        if cat is None and mine:
            lines.append("  NOTE no catalog in %s/catalog: the ref is not checked (needs.py check will)" % data)
        if text == (before or ""):
            return 0, lines[:1] + ["  unchanged: the file stood so already"]
        if dry:
            return 0, lines + ["  (--dry-run: nothing written)"]
        tmp = path.with_name(path.name + ".tmp")
        tmp.write_text(text, encoding="ascii", newline="\n")
        os.replace(tmp, path)
        if not (repo / ".git").exists():
            return 0, lines + ["  not committed: %s is no git repository" % repo]
        done, said_by_git = commit(repo, who, "needs.tsv: %s %s (%s, %s)" % (verb, rid or "the file", where or "all", who))
        if not done:
            git(repo, "reset", "-q", "--", FILE)
            if before is None:
                path.unlink(missing_ok=True)
            else:
                path.write_text(before, encoding="ascii", newline="\n")
            return 1, ["HALT: git refused the commit six times (%s): the file is put back, nothing changed" % said_by_git]
        return 0, lines + ["  committed %s as %s" % (said_by_git, who)]
    finally:
        if lock is not None:
            lock.close()


def cell(value, name):
    """A cell's value from the command line: tabs and line ends out; `-` or `none` empties it."""
    text = " ".join(str(value).replace("\t", " ").split())
    if name in ("place", "due", "note") and text.lower() in EMPTY:
        return ""
    return text


def own_of(who):
    return board.NAMES.get(who, "").lower()


def may(who, name):
    return who == "Unity" or own_of(who) == name


def new_id(rows, ref):
    base = re.sub(r"[^a-z0-9]+", "-", ref.lower()).strip("-")[:28] or "need"
    base = base if len(base) >= 2 else base + "-1"
    taken = {r["id"] for r in rows}
    if base not in taken:
        return base
    return next("%s-%d" % (base, n) for n in range(2, 999) if "%s-%d" % (base, n) not in taken)


def adder(who, kind, ref, units, opts):
    def change(rows, now):
        name = division_word(opts.get("division") or own_of(who) or "")
        if name in (None, "all"):
            raise Refused("`%s` is no division: %s" % (opts.get("division"), ", ".join(ORDER)))
        if not may(who, name):
            raise Refused("the needs of %s are %s's to write; %s writes those of %s (the Fleet Admiral any): ask in requests.log"
                          % (name, DIVISIONS[name], who, own_of(who)))
        open_now = sum(1 for r in rows if r["division"] == name and r["status"] == "open")
        if open_now >= MAX_OPEN:
            raise Refused("%s holds %d open needs, at most %d (MAX_OPEN): close or drop one first (needs.py done|drop <id>)" % (name, open_now, MAX_OPEN))
        rid = cell(opts["id"], "id") if opts.get("id") else new_id(rows, ref)
        if rid in {r["id"] for r in rows}:
            raise Refused("id %s stands already: name another with --id, or change it with needs.py set %s" % (rid, rid))
        stamp = now_stamp(now)
        row = {"id": rid, "project": cell(opts.get("project") or "", "project"), "division": name, "kind": kind, "ref": ref, "units": units,
               "priority": opts.get("priority") or "2", "place": cell(opts.get("place") or "", "place"), "due": cell(opts.get("due") or "", "due"), "status": "open",
               "note": cell(opts.get("note") or "", "note"), "added": stamp, "added_by": who, "changed": stamp, "changed_by": who}
        return rows + [row], rid, name
    return change


def changer(who, rid, opts, status_to=None):
    def change(rows, now):
        found = [r for r in rows if r["id"] == rid]
        if not found:
            raise Refused("no need %s in %s: needs.py list --all" % (rid, FILE))
        row = dict(found[0])
        if not may(who, row["division"]):
            raise Refused("%s is a need of %s, %s's to change (the Fleet Admiral any): ask in requests.log" % (rid, row["division"], DIVISIONS.get(row["division"], "?")))
        if opts.get("division"):
            name = division_word(opts["division"])
            if name in (None, "all"):
                raise Refused("`%s` is no division: %s" % (opts["division"], ", ".join(ORDER)))
            if name != row["division"] and who != "Unity":
                raise Refused("only the Fleet Admiral moves a need to another division")
            if name != row["division"] and row["status"] == "open" and sum(1 for r in rows if r["division"] == name and r["status"] == "open") >= MAX_OPEN:
                raise Refused("%s holds %d open needs already (MAX_OPEN)" % (name, MAX_OPEN))
            row["division"] = name
        for key in ("project", "kind", "ref", "units", "priority", "place", "due", "note", "status"):
            if opts.get(key) is not None:
                row[key] = cell(opts[key], key)
        if status_to:
            row["status"] = status_to
        if row["status"] == "open" and found[0]["status"] != "open" and sum(1 for r in rows if r["division"] == row["division"] and r["status"] == "open") >= MAX_OPEN:
            raise Refused("%s holds %d open needs already (MAX_OPEN): close one first" % (row["division"], MAX_OPEN))
        row["changed"], row["changed_by"] = now_stamp(now), who
        return [row if r["id"] == rid else r for r in rows], rid, row["division"]
    return change


def tidier(rows, now):
    return rows, None, None


# ---- the store (store.py): the table needs, a snapshot of the file, and need_status, computed on the pass

SNAPSHOT = (("needs", "id TEXT, project TEXT, division TEXT, kind TEXT, ref TEXT, units INTEGER, priority INTEGER, place TEXT, due TEXT, status TEXT, "
                      "note TEXT, added TEXT, added_by TEXT, changed TEXT, changed_by TEXT, line INTEGER, error TEXT", "line"),)
SCHEMA = """
CREATE TABLE IF NOT EXISTS need_status (id TEXT PRIMARY KEY, rank INTEGER, project TEXT, division TEXT, priority INTEGER, kind TEXT, ref TEXT,
  units INTEGER, place TEXT, due TEXT, stale TEXT, covered REAL, colour TEXT, raw_units INTEGER, raw_short INTEGER, short_items TEXT, gather TEXT,
  buy TEXT, craft TEXT, stock TEXT, fee INTEGER, stands INTEGER, problem TEXT, storage_book TEXT, catalog TEXT, t INTEGER NOT NULL);
"""
TABLES = ("need_status",)


def read_needs(path, ctx):
    """game/needs.tsv -> needs, one row per need of the file (store.py, a snapshot reader). A file that is not ASCII or has
    no header raises ValueError: the store names it and keeps its rows as last read."""
    rows, problem = parse(Path(path).read_bytes().decode("ascii"))
    if problem:
        raise ValueError(problem)
    return {"needs": [dict({k: r[k] for k in HEADER}, line=r["line"], error="; ".join(r["errors"]) or None) for r in rows]}


def need_files(data, root):
    """The store's files of the loader `needs`: game/needs.tsv when it is there (root is the repository's game/ folder)."""
    path = Path(root) / Path(FILE).name
    return [(NAME, path, read_needs, False, "")] if path.is_file() else []


def setup(conn):
    """need_status made again when its definition changed: it is derived, the next computation fills it."""
    import hashlib
    version = hashlib.sha256(SCHEMA.encode("ascii")).hexdigest()[:16]
    row = conn.execute("SELECT value FROM meta WHERE key = 'needs.schema'").fetchone()
    if not row or row[0] != version:
        conn.execute("DROP TABLE IF EXISTS need_status")
        conn.executescript(SCHEMA)
        conn.execute("INSERT OR REPLACE INTO meta VALUES ('needs.schema', ?)", (version,))
        conn.execute("DELETE FROM meta WHERE key = 'needs.at'")


def status_rows(res):
    """The rows of need_status from status()'s answer."""
    text = lambda pairs: listed(pairs, 12) or None
    t = int(res["now"])
    return [(e["id"], e["rank"], e["project"], e["division"], e["priority"], e["kind"], e["ref"], e["units"], e["place"] or None, e["due"] or None, e["stale"] or None,
             round(e["covered"], 2) if e["covered"] is not None else None, e["colour"], e["raw_units"], e["raw_short"], text(e["short"].items()),
             text(e["gather"].items()), text(e["buy"].items()), "; ".join("%s %d (%s, %s)" % (i, n, rid, how) for i, n, _runs, rid, how in e["craft"][:12]) or None,
             text(e["stock"].items()), e["fee"], e["stands"], e["problem"] or None, res["written"] or None, res["catalog"], t) for e in res["needs"]]


def compute(conn, data, root, now):
    """The store's hook (store.one_pass): need_status computed again when the file was loaded since the last computation
    or EVERY seconds passed; in its own transaction. root is the repository's game/ folder. {rows, seconds} or {} when not due."""
    setup(conn)
    last = conn.execute("SELECT value FROM meta WHERE key = 'needs.at'").fetchone()
    loaded = conn.execute("SELECT t FROM source WHERE name = ?", (NAME,)).fetchone() if conn.execute(
        "SELECT 1 FROM sqlite_master WHERE name = 'source'").fetchone() else None
    if last is not None and now - float(last[0]) < EVERY and not (loaded and loaded[0] and loaded[0] > float(last[0])):
        return {}
    begun = time.time()
    try:
        rows = status_rows(status(str(data), str(Path(root).resolve().parent), now=now))
    except Exception as error:                     # noqa: BLE001  the old rows stand; the next pass that is due tries again
        conn.execute("INSERT OR REPLACE INTO meta VALUES ('needs.error', ?)", ("%s: %s at %s" % (type(error).__name__, str(error)[:200], now_stamp(now)),))
        conn.execute("INSERT OR REPLACE INTO meta VALUES ('needs.at', ?)", (int(now),))
        raise
    conn.execute("BEGIN IMMEDIATE")
    try:
        conn.execute("DELETE FROM need_status")
        conn.executemany("INSERT OR REPLACE INTO need_status VALUES (%s)" % ",".join("?" * 26), rows)
        for key, value in (("needs.at", int(now)), ("needs.rows", len(rows)), ("needs.seconds", round(time.time() - begun, 3)), ("needs.error", "")):
            conn.execute("INSERT OR REPLACE INTO meta VALUES (?, ?)", (key, value))
        conn.execute("COMMIT")
    except BaseException:
        conn.execute("ROLLBACK")
        raise
    return {"rows": len(rows), "seconds": round(time.time() - begun, 3)}


DESCRIPTIONS = {
    "needs": "the needs register (game/needs.tsv, written by needs.py only): per need its id, project, owner division, kind (facility, hull, item), ref "
             "(the catalog's id), units, priority (1 high to 3), place, due date, status (open, done, dropped), note, added and changed with who did "
             "it, the file's line, and error (why a broken row does not count; NULL for a good one). The open needs are the reserve's targets",
    "need_status": "per open need, computed by the store on its pass (needs.py compute: when game/needs.tsv changed, else every 300 s): its rank (the "
                   "order stock is given to the needs: priority, due, added), covered (percent of its raw units stock covers), colour (red under 50, "
                   "yellow 50 to 99, green nothing short, broken), stale, raw units, raw units short, what is short, to gather, to buy, to craft, "
                   "what it takes from stock, the fee, the facilities of its kind our empire holds: needs.py list",
}
EXAMPLES = {
    "needs": (("The open needs by division and priority", "SELECT division, priority, id, kind, ref, units, project FROM needs WHERE status = 'open' "
                                                         "ORDER BY division, priority, id"),
              ("Rows of the register that do not count, and why", "SELECT line, id, error FROM needs WHERE error IS NOT NULL ORDER BY line"),
              ("Open needs per project", "SELECT project, COUNT(*), GROUP_CONCAT(id) FROM needs WHERE status = 'open' GROUP BY project ORDER BY 2 DESC")),
    "need_status": (("The open needs, highest first, with their colour", "SELECT rank, colour, covered, id, division, ref, short_items FROM need_status ORDER BY rank"),
                    ("The red needs of each division", "SELECT division, COUNT(*), GROUP_CONCAT(id) FROM need_status WHERE colour = 'red' GROUP BY division"),
                    ("What the open needs still ask to gather", "SELECT id, gather FROM need_status WHERE gather IS NOT NULL ORDER BY rank")),
}


# ---- the MCP tool, the briefing, hive.py

TOOL_TEXT = ("The needs register (game/needs.tsv, written by needs.py only): what each division needs for its upgrades and the empire's "
             "progress, one row a need with its project, owner division, priority and status; the open needs are the reserve's targets "
             "(rule F24), and stock goes to them in priority order. action=list (default): the open needs, highest priority first, each with "
             "covered percent, colour (red under 50, yellow 50 to 99, green covered) and what is short to gather, craft or buy. action=show: "
             "one need whole (id) or every need of a project (project). action=items: per item for the whole fleet its gross need, held and "
             "net short. action=add: a need of your division (kind, ref, units, project; priority 1 high to 3, place, due, note, id), "
             "committed under your name. action=set: a need changed (id and what changes). action=done or drop: a need closed (id), built or "
             "no longer wanted. Writes are your own division's needs only (the Fleet Admiral any); dry_run=true says what would change. "
             "action=check: the gate.")


def mcp_plan(a):
    action = a.get("action") or "list"
    opt = lambda name: [] if a.get(name) is None or a.get(name) is False or a.get(name) == "" else ["--" + name, str(a[name])]      # a 0 is a value
    if action == "list":
        return [("game/fleet/needs.py", ["list"] + ([str(a["division"])] if a.get("division") else []) + opt("project") + (["--all"] if a.get("all") else []))]
    if action == "show":
        word = a.get("id") or a.get("project")
        if not word:
            raise ValueError("this needs: id")                 # or project: the words collective_mcp and the handbook read
        return [("game/fleet/needs.py", ["show", str(word)])]
    if action in ("items", "check"):
        return [("game/fleet/needs.py", [action])]
    dry = ["--dry-run"] if a.get("dry_run") else []
    if action == "add":
        missing = [n for n in ("kind", "ref", "units", "project") if a.get(n) in (None, "")]
        if missing:
            raise ValueError("this needs: " + ", ".join(missing))
        return [("game/fleet/needs.py", ["add", str(a["kind"]), str(a["ref"]), str(a["units"])] + opt("project") + opt("priority") + opt("place")
                 + opt("due") + opt("note") + opt("id") + opt("division") + dry)]
    if action in ("set", "done", "drop"):
        if not a.get("id"):
            raise ValueError("this needs: id")
        keys = ("project", "kind", "ref", "units", "priority", "place", "due", "note", "status", "division") if action == "set" else ("note",)
        return [("game/fleet/needs.py", [action, str(a["id"])] + [w for k in keys for w in opt(k)] + dry)]
    raise ValueError("action is one of: list, show, items, add, set, done, drop, check")


def mcp_tool(tools, arg):
    """The MCP tool `needs` (collective_mcp.py calls it once after its TOOLS; it stands in WRITES there)."""
    S, I, B = "string", "integer", "boolean"
    tools["needs"] = {
        "text": TOOL_TEXT,
        "args": {"action": arg(S, "list (default), show, items, add, set, done, drop or check", ("list", "show", "items", "add", "set", "done", "drop", "check")),
                 "id": arg(S, "for show, set, done and drop: the need's id; for add: an id of your own (default: from the ref)"),
                 "division": arg(S, "for list: a division or member, or all (default); for add: the owner (default: yours; another is the Fleet Admiral's)"),
                 "project": arg(S, "for add: what it serves, e.g. Atria outpost; for list: only the needs whose project holds this text; for show: a project"),
                 "kind": arg(S, "for add and set: facility, hull or item", NEED_KINDS), "ref": arg(S, "for add and set: the catalog's id of the facility, hull or item"),
                 "units": arg(I, "for add and set: how many"), "priority": arg(I, "for add and set: 1 high, 2 (default), 3 low"),
                 "place": arg(S, "for add and set: the base or station id where it is built or kept; - empties it"),
                 "due": arg(S, "for add and set: a UTC date YYYY-MM-DD; - empties it"),
                 "note": arg(S, "for add, set, done and drop: at most 200 characters"),
                 "status": arg(S, "for set: open, done or dropped", STATUSES), "all": arg(B, "for list: the closed needs too"),
                 "dry_run": arg(B, "for the writes: say what would change and write nothing")},
        "plan": mcp_plan}


def briefing(root, data, now, who):
    """The briefing's one line (hive.py briefing): the division's open needs and how many are red, and the fleet's; from the
    store's need_status, else the file without colours. root is the repository's game/ folder."""
    name = division_word(who)
    counts, source = {}, ""
    try:
        import store
        conn = store.connect(data)
        try:
            found = conn.execute("SELECT division, colour, stale FROM need_status").fetchall() if conn is not None else None
        finally:
            if conn is not None:
                conn.close()
    except Exception:                              # noqa: BLE001  no table yet: the file answers, without colours
        found = None
    if found is None:
        rows, _problem, _present = read(Path(root).resolve().parent)
        found, source = [(r["division"], None, stale(r, now)) for r in rows if r["status"] == "open"], " | colours not measured yet (no need_status in the store)"
    for div, colour, late in found:
        for key in (div, "all"):
            entry = counts.setdefault(key, {"open": 0, "red": 0, "broken": 0, "stale": 0})
            entry["open"] += 1
            entry["red"] += 1 if colour == "red" else 0
            entry["broken"] += 1 if colour == "broken" else 0
            entry["stale"] += 1 if late else 0

    def part(key):
        c = counts.get(key) or {"open": 0, "red": 0, "broken": 0, "stale": 0}
        return "%d open, %d red%s, %d stale" % (c["open"], c["red"], ", %d broken" % c["broken"] if c["broken"] else "", c["stale"])
    mine = "" if name in ("all", None) else "%s: %s | " % (name, part(name))
    print("=== NEEDS | %sthe fleet: %s%s | the tool needs: action=list, action=add" % (mine, part("all"), source))


def hive(args, root, data):
    """hive.py needs: the reading verbs only (hive.py writes nothing). root is the repository's game/ folder."""
    rest = [a for n, a in enumerate(args) if a not in ("--root", "--data") and (n == 0 or args[n - 1] not in ("--root", "--data"))]
    if rest and rest[0] not in ("list", "show", "items", "check"):
        print("REFUSED: hive.py reads only; write with needs.py %s or the MCP tool needs (action=%s)" % (rest[0], rest[0]))
        return 1
    return main(rest + ["--root", str(Path(root).resolve().parent), "--data", data])


# ---- the command line

def main(argv=None):
    args = sys.argv[1:] if argv is None else list(argv)
    value = lambda name, default=None: args[args.index(name) + 1] if name in args and args.index(name) + 1 < len(args) else default
    here = Path(__file__).resolve().parent
    repo, data = value("--root", str(here.parent.parent)), value("--data", division.DATA)
    words = [a for n, a in enumerate(args) if not a.startswith("--") and (n == 0 or args[n - 1] not in VALUED)]
    if not words or any(a in ("-h", "--help") for a in args):
        sys.exit(__doc__)
    verb, rest, dry = words[0], words[1:], "--dry-run" in args
    kind, name = division.member()
    who = name if kind == "member" else ""
    opts = {key: value("--" + key) for key in ("project", "priority", "place", "due", "note", "id", "division", "units", "kind", "ref", "status")}
    opts["place"] = opts["place"] if opts["place"] is not None else value("--where")
    opts["due"] = opts["due"] if opts["due"] is not None else value("--by")
    if verb in ("list", "show", "items"):
        res = status(data, repo)
        if verb == "list":
            which = division_word(rest[0] if rest else "all")
            if which is None:
                sys.exit("`%s` is no division, member or role: %s, or all" % (rest[0], ", ".join(ORDER)))
            return show_list(res, which, opts["project"] or "", "--all" in args)
        if verb == "show":
            if not rest:
                sys.exit("name the need: needs.py show <id>|<project text>")
            return show_one(res, " ".join(rest))
        return show_items(data, repo, res)
    if verb == "check":
        return check(data, repo)
    if verb == "add":
        if len(rest) != 3:
            sys.exit("needs.py add <facility|hull|item> <ref> <units> --project \"<text>\" [...]")
        code, lines = write(repo, data, who, adder(who, rest[0], rest[1], rest[2], opts), "add", dry)
    elif verb in ("set", "done", "drop"):
        if len(rest) != 1:
            sys.exit("needs.py %s <id> [...]" % verb)
        if verb != "set":
            opts = {"note": opts["note"]}
        code, lines = write(repo, data, who, changer(who, rest[0], opts, {"done": "done", "drop": "dropped"}.get(verb)), verb, dry)
    elif verb == "tidy":
        code, lines = write(repo, data, who, tidier, "tidy", dry)
    elif verb == "reconcile":
        code, lines = reconcile(repo, data, who or "Unity", dry)
        if not lines:
            lines = ["NEEDS reconcile | 0 open needs newly fulfilled"]
    else:
        sys.exit(__doc__)
    print("\n".join(lines))
    return code


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        sys.exit(0)

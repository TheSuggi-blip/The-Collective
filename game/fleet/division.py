#!/usr/bin/env python3
"""division.py -- who commands which ship, whose plan is whose, and the check every fleet script runs before it drives a ship.

WHAT: a ship belongs to a division by its name: the word before the dash
      (miner- Zero, trader- Mercury, hauler- Apollo, drone- Apophis,
      scout- Oracle, sentinel- Unity). A flagship (data/fleet/flagships.json)
      and any other name belong to the Fleet Admiral. Each Admiral commands
      the ships of its own division; the Fleet Admiral commands every ship.
      The other fleet scripts ask this module three things:
        who is asking   the member this shell belongs to. Hermes names
                        the profile in every tool shell
                        (HERMES_SESSION_PROFILE, HERMES_HOME); a service
                        names itself in FLEET_MEMBER.
        may it drive    `require(pilot)` ends a script that would drive a
                        ship of another division, or a ship another program
                        is flying.
        which plan      `load_plan(root)` reads game/routes/plans/<role>.json:
                        one file per role, kept by the role's Admiral.
RULES:
  - Reading is free for every member. Driving a ship is its Admiral's and
    the Fleet Admiral's.
  - A shell that is no member and no service drives nothing.
  - Two programs never drive one pilot: a pilot that carries a fresh order
    file (data/fleet/orders/<pilot>.json) of a runner is left alone. A
    member's own hand hold (`hand <Member>`, written by gate.py) is its own.
  - It is a lock on our own scripts, not a wall: the engine's gate asks no
    name. A member that calls the gate around these scripts breaks order F1.
WHY:  five Admirals command through one gate from one working copy. The
      check fires by itself, inside the command; nobody has to remember it.

USAGE:
  division.py me                  the member this shell belongs to
  division.py of <pilot>          the member that commands the pilot
  division.py ships [<Member>]    the pilots a member commands (default: me), from the fleet's live file
  division.py may <pilot>         exit 0 when this shell may drive the pilot now; exit 1 and the reason when not
  division.py plan [<role>]       the plans in force: per role, who keeps it and its routes in order
  --data <dir>                    the unit's data folder (default /srv/collective/data)

Stdlib only. ASCII only.
"""

import json
import os
import re
import sys
import time
from pathlib import Path

DATA = "/srv/collective/data"
ROLES = {"miner": "Zero", "trader": "Mercury", "hauler": "Apollo", "drone": "Apophis", "scout": "Oracle", "sentinel": "Unity", "command": "Unity"}
MEMBERS = ("Unity", "Zero", "Apollo", "Mercury", "Apophis", "Oracle")
PROFILE = re.compile(r"/profiles/([a-z]+)(?:/|$)")
ORDER_FRESH = 20 * 60        # an order file not touched for this long is dead (the dispatcher's rule)
PILOT = re.compile(r"\b(?:%s)-[0-9]+\b" % "|".join(sorted(ROLES)))      # a pilot of ours by name: a role word, a dash, a number


def pilots_named(text):
    """The pilots of ours a text names (a role word, a dash, a number), each once, in the order found. The repository
    is public and never says which pilot flies what (rulebook section 10): comms.py refuses a log entry that names
    one, routes.py check a route file or a role plan (requests ENT-052). A flagship's name has no number: it is left
    to the writer."""
    return list(dict.fromkeys(PILOT.findall(str(text))))


def member(env=None):
    """('member', Name), ('service', name) or (None, '') for the shell this script runs in."""
    env = os.environ if env is None else env
    named = str(env.get("HERMES_SESSION_PROFILE") or "").strip().capitalize()
    if named in MEMBERS:
        return "member", named
    for key in ("HERMES_HOME", "HERMES_SCRATCH_DIR", "TMPDIR"):
        found = PROFILE.search(str(env.get(key) or ""))
        if found and found.group(1).capitalize() in MEMBERS:
            return "member", found.group(1).capitalize()
    name = str(env.get("FLEET_MEMBER") or "").strip()
    if name and name.capitalize() not in MEMBERS:
        return "service", name
    return None, ""


def flagships(data=DATA):
    try:
        found = json.loads((Path(data) / "fleet" / "flagships.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        found = {}
    return found if isinstance(found, dict) else {}


def role_of(pilot, data=DATA):
    """The role whose plan a pilot flies: its flagship entry's, else the word before the dash; '' for any other name."""
    entry = flagships(data).get(pilot)
    if isinstance(entry, dict):
        return str(entry.get("role") or "command")
    word = pilot.split("-")[0]
    return word if "-" in pilot and word in ROLES else ""


def owner(pilot, data=DATA):
    """The member that commands a pilot."""
    return ROLES.get(role_of(pilot, data), "Unity")


def order_of(pilot, data=DATA, now=None):
    """What the pilot's fresh order file says it is doing; '' when it carries none."""
    path = Path(data) / "fleet" / "orders" / (pilot + ".json")
    try:
        if (time.time() if now is None else now) - path.stat().st_mtime > ORDER_FRESH:
            return ""
        return str(json.loads(path.read_text(encoding="utf-8")).get("what") or "")
    except (OSError, ValueError):
        return ""


def hand_mark(env=None):
    kind, name = member(env)
    return "hand " + name if kind else ""


def may(pilot, data=DATA, env=None, now=None):
    """(True or False, the reason): may this shell drive the pilot now?"""
    kind, name = member(env)
    if kind is None:
        return False, "this shell is no member of The Collective and no service (HERMES_SESSION_PROFILE and HERMES_HOME name no member, FLEET_MEMBER is not set): it drives no ship"
    if kind == "service":
        return True, "service %s" % name
    own = owner(pilot, data)
    if name != "Unity" and own != name:
        return False, "%s is commanded by %s, not by %s (orders F1): ask in requests.log" % (pilot, own, name)
    what = order_of(pilot, data, now)
    if what and what != "hand " + name and what != str((os.environ if env is None else env).get("FLEET_HOLD") or ""):
        return False, ("%s is busy: `%s`. Two programs never drive one pilot: wait until that run ends, or take its route out of the plan"
                       % (pilot, what))
    return True, "%s commands %s" % (name, pilot)


def require(pilot, data=DATA):
    """End the script that called this unless this shell may drive the pilot now."""
    ok, why = may(pilot, data)
    if not ok:
        sys.exit("REFUSED: " + why)


def load_plan(root):
    """({role: [route ids]}, {role: who keeps the file}, [errors]) from <root>/routes/plans/<role>.json; root is the game/ folder."""
    roles, owners, errors = {}, {}, []
    folder = Path(root) / "routes" / "plans"
    for path in sorted(folder.glob("*.json")) if folder.is_dir() else []:
        where = "game/routes/plans/%s: " % path.name
        try:
            plan = json.loads(path.read_text(encoding="ascii"))
        except (OSError, ValueError) as error:
            errors.append(where + "not readable as ASCII JSON: %s" % error)
            continue
        if not isinstance(plan, dict) or plan.get("role") != path.stem or not isinstance(plan.get("routes"), list):
            errors.append(where + "needs `role` equal to the file name and a list `routes`")
            continue
        roles[path.stem] = [str(rid) for rid in plan["routes"]]
        owners[path.stem] = str(plan.get("owner") or "")
        if path.stem not in ROLES:
            errors.append(where + "`%s` is no role of the fleet (%s)" % (path.stem, ", ".join(sorted(ROLES))))
        elif owners[path.stem] != ROLES[path.stem]:
            errors.append(where + "`owner` must be %s, who commands the %s ships" % (ROLES[path.stem], path.stem))
    return roles, owners, errors


def main():
    args = sys.argv[1:]
    data = args[args.index("--data") + 1] if "--data" in args else DATA
    args = [a for n, a in enumerate(args) if a != "--data" and (n == 0 or args[n - 1] != "--data")]
    verb = args[0] if args else ""
    kind, name = member()
    if verb == "me":
        print(name if kind else "no member and no service")
        return 0 if kind else 1
    if verb == "of" and len(args) == 2:
        print(owner(args[1], data))
        return 0
    if verb == "ships":
        who = args[1] if len(args) > 1 else name
        try:
            ships = json.loads((Path(data) / "fleet" / "fleet.json").read_text(encoding="utf-8")).get("ships") or []
        except (OSError, ValueError):
            ships = []
        own = sorted(s["name"] for s in ships if isinstance(s, dict) and s.get("name") and (who == "Unity" or owner(s["name"], data) == who))
        print("%s commands %d ship(s)%s" % (who or "nobody", len(own), ":" if own else ""))
        print("\n".join(own))
        return 0
    if verb == "may" and len(args) == 2:
        ok, why = may(args[1], data)
        print(("yes: " if ok else "REFUSED: ") + why)
        return 0 if ok else 1
    if verb == "plan":
        roles, owners, errors = load_plan(Path(__file__).resolve().parent.parent)
        for role in sorted(roles):
            if len(args) < 2 or args[1] == role:
                print("%-9s %-8s %s" % (role, owners.get(role) or "?", " > ".join(roles[role])))
        for line in errors:
            print("ERROR: " + line)
        return 1 if errors else 0
    sys.exit(__doc__)


if __name__ == "__main__":
    sys.exit(main())

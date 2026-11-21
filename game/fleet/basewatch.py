#!/usr/bin/env python3
"""basewatch.py -- an alert while a base of ours reads wrecked or a facility of ours damaged or offline.

WHAT: reads what the fleet reads already and sends no call to the game:
        data/empire/empire.json     empire.py collect, every 15 minutes: the faction's facilities as spacemolt_facility
                                    faction_owned reads them, each with its status, our bases, and `base_alerts`, what
                                    that collect found wrong with the time a collect first found it (`since`)
        the store's table stations  the public list of stations and outposts (data/station/stations.json, fetched
                                    every 15 minutes; read from the file when the store has no copy): `wrecked`
        data/scouting/<system>.json the census's reading of the base: its hull, and a repair bill where one is read
      An alert stands while the newest of those readings says so: a base of our faction's tag that reads wrecked, or a
      facility of ours whose status is not `active` (damaged, offline, ...). Three readers print it:
        line      `hive.py briefing`: one line at its top while an alert stands, nothing otherwise
        show      `hive.py stats alerts` (the tool fleet, view=alerts): every alert, before the control chart
      and empire.py collect keeps `base_alerts` with `stamped`, so that `since` survives from pass to pass.
RULES:
  - Since: the first collect that read it so (base_alerts). An alert no collect recorded yet (the public list read it
    before the next collect, or the collect has not run since) says the last collect that read the base whole
    instead: `since after <time>`. A figure no reading holds is `not read`, never filled in.
  - The repair bill: the census's reading of the base, when it lists `repairs` with `materials`; else `not read`.
  - It keeps no state of its own: an alert ends with the first reading that shows the base whole again.
WHY:  errors.log ENT-112 (Apollo, 2026-11-21): our outpost CLTV Outpost GSC-0044 stood wrecked for three days, its fuel
      bunker and lockbox damaged, while every tool printed both active and no member read the game's own list.

USAGE:
  basewatch.py [show]     every alert, one line each
  basewatch.py line       the briefing's line (empty while no alert stands)
  --data <dir>            the unit's data folder (default /srv/collective/data)

Stdlib only. ASCII only.
"""

import calendar
import json
import os
import sqlite3
import sys
import time
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

DATA = "/srv/collective/data"
OK = ("active",)                 # the one facility status that raises nothing


def read_json(path, default):
    try:
        with open(path, encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, ValueError):
        return default


def epoch(text):
    try:
        return calendar.timegm(time.strptime(str(text)[:19].replace(" ", "T"), "%Y-%m-%dT%H:%M:%S"))
    except (TypeError, ValueError):
        return None


def utc(stamp):
    """`2026-11-21 19:50 UTC` of an ISO time or an epoch; `an unknown time` when neither."""
    at = stamp if isinstance(stamp, (int, float)) and not isinstance(stamp, bool) else epoch(stamp)
    return time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime(at)) if at else "an unknown time"


def tag_of(state, conn=None):
    """Our faction's tag: empire.json faction.tag, else the store's table faction."""
    tag = str(((state.get("faction") or {}) if isinstance(state.get("faction"), dict) else {}).get("tag") or "")
    if not tag and conn is not None:
        try:
            row = conn.execute("SELECT tag FROM faction ORDER BY t DESC LIMIT 1").fetchone()
            tag = str(row[0] or "") if row else ""
        except sqlite3.Error:
            tag = ""
    return tag


def public_rows(data, conn=None):
    """([{name, kind, system, condition, wrecked}] of the public list of stations, its reading time): the store's table
    stations when the store has one, else data/station/stations.json. The time is the file's, which the store reads."""
    path = Path(data) / "station" / "stations.json"
    try:
        read = path.stat().st_mtime
    except OSError:
        read = None
    if conn is not None:
        try:
            rows = conn.execute("SELECT name, kind, system, tag, condition, wrecked FROM stations").fetchall()
            return [{"name": n, "kind": k, "system": s, "tag": t, "condition": c, "wrecked": bool(w)} for n, k, s, t, c, w in rows], read
        except sqlite3.Error:
            pass
    found = read_json(path, [])
    found = found.get("stations") if isinstance(found, dict) else found
    return [{"name": s.get("name"), "kind": s.get("type"), "system": s.get("system"), "condition": s.get("condition"), "wrecked": bool(s.get("wrecked")),
             "tag": s.get("tag")} for s in found or [] if isinstance(s, dict)], read


def found_now(state, public, tag):
    """{key: alert} of what the readings show wrong now: each facility whose status is not OK (empire.json), each base
    of ours the public list reads wrecked. An alert: {key, what, name, base, system, source}."""
    names = {str(b.get("base")): str(b.get("name") or b.get("base")) for b in state.get("bases") or [] if isinstance(b, dict)}
    out = {}
    for f in state.get("facilities") or []:
        if not isinstance(f, dict):
            continue
        status = str(f.get("status") or "active").lower()
        if status in OK:
            continue
        base = str(f.get("base") or "")
        key = "facility:%s:%s" % (f.get("facility_id") or "%s@%s" % (f.get("type"), base), status)
        out[key] = {"key": key, "what": status, "name": "%s at %s" % (f.get("name") or f.get("type") or "a facility", names.get(base, base or "a base")),
                    "base": names.get(base, base), "system": str(f.get("system") or ""), "source": "faction_owned (empire.py collect)"}
    for s in public:
        if tag and s.get("tag") == tag and s.get("wrecked"):
            key = "base:%s:wrecked" % s.get("name")
            out[key] = {"key": key, "what": "wrecked", "name": str(s.get("name")), "base": str(s.get("name")), "system": str(s.get("system") or ""),
                        "source": "the public list of stations"}
    return out


def stamped(state, old, public, now_text):
    """empire.py collect's `base_alerts`: what this reading finds wrong, each with `since`, the first collect that read it
    so (kept from the last reading's base_alerts while it stands). `public`: the public list of stations collect read."""
    tag = tag_of(state)
    before = {a.get("key"): a for a in (old or {}).get("base_alerts") or [] if isinstance(a, dict)}
    rows = [{"name": r.get("name"), "system": r.get("system"), "tag": r.get("tag"), "wrecked": bool(r.get("wrecked"))} for r in public or [] if isinstance(r, dict)]
    out = []
    for key, alert in sorted(found_now(state, rows, tag).items()):
        out.append(dict(alert, since=(before.get(key) or {}).get("since") or now_text))
    return out


def bill(data, alert):
    """The repair bill of the alert's base as the census read it (`repairs` ... `materials`), the hull it read below its
    maximum, or ''. Never a figure the reading does not hold."""
    if not alert.get("system"):
        return ""
    scout = read_json(Path(data) / "scouting" / (alert["system"] + ".json"), {})
    for entry in (scout.get("pois") or {}).values() if isinstance(scout.get("pois"), dict) else []:
        if not isinstance(entry, dict):
            continue
        base = entry.get("base") if isinstance(entry.get("base"), dict) else {}
        if alert["base"] not in (base.get("name"), base.get("id"), (entry.get("poi") or {}).get("name")):
            continue
        said = []
        repairs = entry.get("repairs") or base.get("repairs") or {}
        materials = repairs.get("materials") if isinstance(repairs, dict) else repairs if isinstance(repairs, list) else []
        parts = ["%s %s" % (m.get("quantity", m.get("units", m.get("remaining", "?"))), m.get("item_id") or m.get("item") or m.get("name"))
                 for m in materials or [] if isinstance(m, dict)]
        if parts:
            said.append("repair bill %s (census %s)" % (", ".join(parts), utc(scout.get("read_at"))))
        hull, most = base.get("hull"), base.get("max_hull")
        if isinstance(hull, (int, float)) and isinstance(most, (int, float)) and hull < most:
            said.append("hull %s of %s (census %s)" % (format(int(hull), ","), format(int(most), ","), utc(scout.get("read_at"))))
        return "; ".join(said)
    return ""


def alerts(data, now=None, conn=None):
    """[alert] standing now, with `since` and `bill` (the text of the bill, or 'repair bill not read'), bases first."""
    own = conn is None
    if own:
        try:
            import store
            conn = store.connect(data)
        except Exception:                                  # noqa: BLE001  no store: the file is read instead
            conn = None
    try:
        state = read_json(Path(data) / "empire" / "empire.json", {})
        state = state if isinstance(state, dict) else {}
        public, read = public_rows(data, conn)
        now_found = found_now(state, public, tag_of(state, conn))
    finally:
        if own and conn is not None:
            conn.close()
    kept = {a.get("key"): a for a in state.get("base_alerts") or [] if isinstance(a, dict)}
    out = []
    for key, alert in now_found.items():
        if key in kept:
            since = "since %s" % utc(kept[key].get("since"))
        elif not state.get("written_at"):
            since = "since: not recorded (no reading of empire.py collect)"
        elif alert["source"].startswith("faction_owned"):
            since = "since: not recorded (read so by the collect of %s, the first reading that keeps it)" % utc(state.get("written_at"))
        else:
            since = "since after %s (the last collect read it whole)" % utc(state.get("written_at"))
        read_at = utc(read) if alert["source"].startswith("the public") else utc(state.get("written_at"))
        out.append(dict(alert, since_text=since, read_at=read_at, bill=bill(data, alert) or "repair bill not read (get_base, docked there, lists it)"))
    return sorted(out, key=lambda a: (not a["key"].startswith("base:"), a["base"], a["name"]))


def words(alert):
    return "%s reads %s (%s, read %s), %s" % (alert["name"], alert["what"], alert["source"], alert["read_at"], alert["since_text"])


def line(data, now=None, conn=None):
    """The briefing's one line while an alert stands, else ''."""
    found = alerts(data, now, conn)
    if not found:
        return ""
    bills = {}
    for alert in found:
        bills.setdefault(alert["base"], alert["bill"])
    return ("BASE ALERT | %d of our bases or facilities read wrong: %s | %s | the turn's first work: read faction_owned and get_base there"
            % (len(found), "; ".join(words(a) for a in found), "; ".join("%s: %s" % kv for kv in bills.items())))


def briefing(data, now=None):
    """hive.py briefing's hook: its one line at the top, nothing while no alert stands. A fault here never stops the
    briefing."""
    try:
        text = line(data, now)
    except Exception as error:                             # noqa: BLE001
        text = "BASE ALERT | not read: %s: %s" % (type(error).__name__, error)
    if text:
        print(text)


def show(data, now=None):
    """hive.py stats alerts' hook (the tool fleet, view=alerts): every alert, one line each, before the control chart."""
    try:
        found = alerts(data, now)
    except Exception as error:                             # noqa: BLE001
        print("BASES | not read: %s: %s" % (type(error).__name__, error))
        return 1
    print("BASES | %d alert%s: a base of ours wrecked or a facility of ours not active (empire.json, the public list of stations)"
          % (len(found), "" if len(found) == 1 else "s"))
    for alert in found:
        print("  ALERT %s | %s" % (words(alert), alert["bill"]))
    return 1 if found else 0


def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)
    if any(a in ("-h", "--help") for a in args):
        sys.exit(__doc__)
    data = args[args.index("--data") + 1] if "--data" in args and args.index("--data") + 1 < len(args) else DATA
    if "line" in args:
        print(line(data, time.time()) or "no base alert")
        return 0
    return show(data, time.time())


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""mobile.py -- where a moving station stands now, for a route stop that names the system it stood in when written.

WHAT: a route names a station as `system:poi:base`. A mobile station (data/station/stations.json, `mobile` true: the
      Mobile Capital, a faction's moving base) leaves that system; a run that travels there fails at once ("Travel to
      mobile_capital failed: It's called a Mobile Capital", 2026-11-23). locate() looks for the base id in the census
      file (data/scouting/<system>.json, its pois with `base_id`) of every system a mobile station stands in now, and
      returns that system and poi when they differ from the route's. Anything else comes back unchanged.
RULES:
  - It reads only: two kinds of data file. It moves no ship and writes no file.
  - Unchanged when the base is no mobile station's, when no census file names it, or when a file does not parse:
    the route's own place is the fallback, never a guess.
  - A runner calls it once per stop, before the travel goal; the line it returns is said in the run's log.
WHY:  the Mobile Capital moved frontier -> altais on 2026-11-23 and every route naming frontier failed until its file
      was edited by hand (queue.log ENT-242, ENT-246). The runner now follows the station by itself.

USAGE:
  python3 -B game/fleet/mobile.py <base> [<system> <poi>]    # where the base stands now, or `unchanged`
  from mobile import locate; system, poi, line = locate(system, poi, base, data_dir)

Stdlib only. ASCII only.
"""
import json
import os
import sys

DATA = '/srv/collective/data'


def read(path):
    """The parsed JSON of a file, or None."""
    try:
        with open(path, encoding='utf-8') as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return None


def mobile_systems(data=DATA):
    """[system id] where a mobile station stands now, by data/station/stations.json."""
    rows = read(os.path.join(str(data), 'station', 'stations.json'))
    out = []
    for row in rows if isinstance(rows, list) else []:
        if isinstance(row, dict) and row.get('mobile') and not row.get('wrecked') and row.get('system'):
            if row['system'] not in out:
                out.append(row['system'])
    return out


def base_poi(census, base):
    """The poi id whose `base_id` is base in one census file, or None."""
    system = census.get('system') if isinstance(census, dict) else None
    for poi in (system.get('pois') if isinstance(system, dict) else None) or []:
        if isinstance(poi, dict) and poi.get('base_id') == base and poi.get('id'):
            return poi['id']
    return None


def locate(system, poi, base, data=DATA):
    """(system, poi, line): the place of base now when a mobile station carries it elsewhere, else the input and ''."""
    for where in mobile_systems(data):
        census = read(os.path.join(str(data), 'scouting', '%s.json' % where))
        found = base_poi(census, base)
        if found:
            if (where, found) == (system, poi):
                return system, poi, ''
            return where, found, 'moving station %s stands at %s:%s now (the route names %s:%s)' % (base, where, found, system, poi)
    return system, poi, ''


def main(argv):
    if not argv or argv[0] in ('-h', '--help'):
        print(__doc__)
        return 0
    base = argv[0]
    system, poi = (argv[1], argv[2]) if len(argv) >= 3 else ('', '')
    s, p, line = locate(system, poi, base)
    print(line or ('unchanged: %s:%s:%s' % (system, poi, base)))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))

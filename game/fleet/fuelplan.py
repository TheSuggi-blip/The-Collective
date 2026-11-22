"""Fuel before a flight: the chart's lanes, the stations that sell fuel, and whether a tank holds the way.

Usage: python3 -I -B fuelplan.py <from system> <to system> [<then system>] [--tank N]

The pure rules a runner asks before it sets out (requests ENT-369, Apophis: two hunters ran dry
in space on 2026-11-22 because a far hunt set out again from a station that sold no fuel):
  chart(repo)                 ({system: [lanes]}, {system: jumps from home}) from game/map/galaxy.tsv
  jumps(lanes, src, reach)    {system: lanes from src} within reach
  fuel_stations(data)         {system: (poi, base)} of the stations whose own read lists `refuel`
  nearest_fuel(lanes, src, stations, skip)   (jumps, system, poi, base) nearest src, or None
  fuel_short(tank, way)       True when tank < 1.5 a jump x way + 15 (census.py's rule)
  way(lanes, here, there, then)   jumps here -> there (-> then), or None when the chart lacks one
census.py keeps its own copies of these rules (it is a script, read whole); hunt.py reads them here.
The command line prints the way and whether a tank holds it; it sends no call."""
import json
import sys
from pathlib import Path

PER_JUMP, SPARE = 1.5, 15        # fuel a jump and the spare a tank keeps (census.py, 2026-11-22)
LOW_SHARE = 0.5                  # a tank under this share of its size after a station's refuel: the station sold none


def chart(repo):
    lanes, home = {}, {}
    try:
        rows = [line.rstrip('\n').split('\t') for line in open(Path(repo) / 'map' / 'galaxy.tsv', encoding='utf-8') if not line.startswith('#')]
    except OSError:
        return lanes, home
    head = rows[0] if rows else []
    for row in rows[1:]:
        cell = dict(zip(head, row))
        if cell.get('id'):
            lanes[cell['id']] = [x for x in (cell.get('lanes') or '').split(',') if x]
            home[cell['id']] = int(cell['jumps_from_home']) if str(cell.get('jumps_from_home', '')).isdigit() else None
    return lanes, home


def strongholds(repo):
    """The systems the chart flags `stronghold`: no ship of ours takes fuel at a pirate's station."""
    try:
        rows = [line.rstrip('\n').split('\t') for line in open(Path(repo) / 'map' / 'galaxy.tsv', encoding='utf-8') if not line.startswith('#')]
    except OSError:
        return set()
    head = rows[0] if rows else []
    return {cell['id'] for cell in (dict(zip(head, row)) for row in rows[1:]) if 'stronghold' in str(cell.get('flags') or '') and cell.get('id')}


def jumps(lanes, src, reach):
    dist, todo = {src: 0}, [src]
    while todo:
        here = todo.pop(0)
        if dist[here] >= reach:
            continue
        for there in lanes.get(here) or []:
            if there not in dist:
                dist[there] = dist[here] + 1
                todo.append(there)
    return dist


def fuel_stations(data):
    out = {}
    try:
        files = sorted((Path(data) / 'scouting').glob('*.json'))
    except OSError:
        return out
    for f in files:
        try:
            pois = json.loads(f.read_text(encoding='utf-8')).get('pois')
        except (OSError, ValueError, AttributeError):
            continue
        for pid, read in (pois.items() if isinstance(pois, dict) else []):
            if not isinstance(read, dict):
                continue
            base = read.get('base') if isinstance(read.get('base'), dict) else {}
            poi = read.get('poi') if isinstance(read.get('poi'), dict) else {}
            services = read.get('services') or base.get('services') or []
            if isinstance(services, list) and 'refuel' in services and base.get('id'):
                out.setdefault(f.stem, (poi.get('id') or pid, base['id']))
    return out


def nearest_fuel(lanes, src, stations, skip=()):
    """(jumps, system, poi, base) of the station with fuel nearest src, the fewest jumps first, then by name; a
    station whose base is in `skip` (one that answered with no fuel) is passed over. None when none is reachable."""
    dist = jumps(lanes, src, 99)
    best = None
    for system, (poi, base) in stations.items():
        if base in skip:
            continue
        if system in dist and (best is None or (dist[system], system) < best[:2]):
            best = (dist[system], system, poi, base)
    return best


def fuel_short(tank, way):
    if tank is None or way is None:
        return False
    return tank < PER_JUMP * way + SPARE


def way(lanes, here, there, then=None):
    """Jumps from here to there, and on to then when given; None when the chart has no way for a leg."""
    if not here or not there:
        return None
    first = jumps(lanes, here, 99).get(there)
    if first is None:
        return None
    if not then:
        return first
    second = jumps(lanes, there, 99).get(then)
    return None if second is None else first + second


def refuelled_short(fuel, max_fuel):
    """True when a tank read after a station's refuel stands under LOW_SHARE of its size: the station sold no fuel
    (The Levy answered station_fuel_empty on 2026-11-22). An unread tank is not judged."""
    if not isinstance(fuel, (int, float)) or not isinstance(max_fuel, (int, float)) or max_fuel <= 0:
        return False
    return fuel < LOW_SHARE * max_fuel


def main():
    args = sys.argv[1:]
    if not args or args[0] in ('-h', '--help') or len([a for a in args if not a.startswith('--')]) < 2:
        sys.exit(__doc__)
    tank = float(args[args.index('--tank') + 1]) if '--tank' in args else None
    plain = [a for i, a in enumerate(args) if not a.startswith('--') and (i == 0 or args[i - 1] != '--tank')]
    repo = Path(__file__).resolve().parent.parent
    lanes, _home = chart(repo)
    n = way(lanes, plain[0], plain[1], plain[2] if len(plain) > 2 else None)
    need = None if n is None else PER_JUMP * n + SPARE
    print('WAY %s: %s jumps, a tank of %s needed%s' % (' -> '.join(plain[:3]), n, need,
          '' if tank is None else '; tank %s: %s' % (tank, 'SHORT' if fuel_short(tank, n) else 'holds')))
    return 0


if __name__ == '__main__':
    sys.exit(main())

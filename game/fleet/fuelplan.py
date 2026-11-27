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
from collections import deque
import json
import re
import sys
from pathlib import Path

PER_JUMP, SPARE = 1.5, 15        # legacy baseline (2-arg fuel_short compatibility)
SAFE_PER_JUMP = 3.0              # realistic base fuel/jump when ship doc is available
SAFE_SPARE = 20.0                # SpaceMolt fuel guide: always plan to arrive with >= 20 fuel spare
LOW_SHARE = 0.5                  # a tank under this share of its size after a station's refuel: the station sold none
_HEX32_RE = re.compile(r'^[0-9a-f]{32}$')


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


def is_foreign_player_station(base):
    """True when a scouting base dict belongs to a non-CLTV player/faction station (e.g. 32-hex UUID
    or non-empty owner/faction_id without CLTV tag), which can refuse docking or lack public fuel."""
    if not isinstance(base, dict):
        return False
    bid = str(base.get('id') or '').strip()
    ftag = str(base.get('faction_tag') or '').strip().upper()
    if ftag == 'CLTV':
        return False
    if base.get('faction_id') or base.get('owner') or base.get('owner_id'):
        return True
    if _HEX32_RE.match(bid.lower()):
        return True
    return False




def owned_fuel_depots(data, min_fuel=200):
    """Return {system_id: (poi_id, base_id)} for active [CLTV] outposts/stations with stocked fuel bunkers.

    Reads read.db (2ms immutable RO) first, falling back to data/empire/empire.json so unit tests
    and offline runs work identically. Automatically discovers future Outposts #4-#8 and Stations #2-#5
    the moment their faction_fuel_bunker is active and holds >= `min_fuel` units.
    """
    out = {}
    if not data:
        return out
    dpath = Path(data)
    db = dpath / 'store' / 'read.db'
    if db.is_file():
        con = None
        try:
            import sqlite3
            con = sqlite3.connect('file:%s?mode=ro&immutable=1' % db, uri=True, timeout=2.0)
            rows = con.execute("""
                SELECT DISTINCT b.system, b.poi, b.base
                FROM bases b
                JOIN faction_facilities ff ON ff.base = b.base
                JOIN faction_storage fs ON fs.base = b.base
                WHERE LOWER(COALESCE(ff.type, '')) LIKE '%fuel_bunker%'
                  AND LOWER(COALESCE(ff.status, 'active')) = 'active'
                  AND fs.item = 'fuel'
                  AND COALESCE(fs.units, 0) >= ?
                  AND b.system IS NOT NULL AND b.system != ''
                  AND b.poi IS NOT NULL AND b.poi != ''
                  AND b.base IS NOT NULL AND b.base != ''
            """, (int(min_fuel),)).fetchall()
            for sid, poi, base in rows:
                out.setdefault(str(sid), (str(poi), str(base)))
            if out:
                return out
        except Exception:
            pass
        finally:
            if con is not None:
                try:
                    con.close()
                except Exception:
                    pass
    ep = dpath / 'empire' / 'empire.json'
    if ep.is_file():
        try:
            emp = json.loads(ep.read_text(encoding='utf-8'))
            bunkers = set()
            for fac in emp.get('facilities') or []:
                if isinstance(fac, dict) and 'fuel_bunker' in str(fac.get('type') or '').lower():
                    if str(fac.get('status') or 'active').lower() == 'active' and fac.get('base'):
                        bunkers.add(str(fac['base']))
            fuel_by_base = {}
            for row in emp.get('faction_storage') or []:
                if isinstance(row, dict) and str(row.get('item') or '') == 'fuel' and row.get('base'):
                    fuel_by_base[str(row['base'])] = int(row.get('units') or row.get('quantity') or 0)
            for b in emp.get('bases') or []:
                if not isinstance(b, dict):
                    continue
                bid = str(b.get('base') or b.get('id') or '')
                sid = str(b.get('system') or '')
                poi = str(b.get('poi') or '')
                if bid and sid and poi and bid in bunkers and fuel_by_base.get(bid, 0) >= int(min_fuel):
                    out.setdefault(sid, (poi, bid))
        except (OSError, ValueError, AttributeError):
            pass
    return out


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
                if is_foreign_player_station(base):
                    continue
                out.setdefault(f.stem, (poi.get('id') or pid, base['id']))
    for sid, pair in owned_fuel_depots(data).items():
        out[sid] = pair
    return out


def ship_jump_cost(ship):
    """Estimate real fuel burned per jump from live ship max_fuel and fitted speed/afterburner modules.
    SpaceMolt scales jump & POI travel fuel with ship scale and speed (05-galaxy.md): e.g. a Threshold
    with afterburner_iii burned 7 fuel/jump (14 for 2 jumps) and 2x afterburner_ii burned 10 fuel/jump."""
    if not isinstance(ship, dict):
        return SAFE_PER_JUMP
    mf = ship.get('max_fuel')
    base = max(SAFE_PER_JUMP, round(float(mf) / 45.0, 1)) if isinstance(mf, (int, float)) and mf > 0 else SAFE_PER_JUMP
    extra = 0.0
    for m in ship.get('modules') or []:
        tid = str((m.get('type') or m.get('type_id') or m.get('id') or '') if isinstance(m, dict) else m).lower()
        if 'afterburner' in tid or 'overdrive' in tid:
            if tid.endswith('_iii') or '_iii_' in tid:
                extra += 5.5
            elif tid.endswith('_ii') or '_ii_' in tid:
                extra += 4.0
            elif tid.endswith('_i') or '_i_' in tid:
                extra += 2.5
            else:
                extra += 3.5
    return round(base + extra, 1)


def ship_dock_reserve(ship):
    """Minimum fuel needed for intra-system POI travel + docking (speed-scaled)."""
    return max(6.0, ship_jump_cost(ship))


def nearest_fuel(lanes, src, stations, skip=(), prefer_bases=None):
    """(jumps, system, poi, base) of the station with fuel nearest src, the fewest jumps first, then by name; a
    station whose base is in `skip` (one that answered with no fuel) is passed over. When `prefer_bases` is
    provided (owned zero-rent CLTV fuel depots), an owned depot within +1 jump of the nearest NPC station
    wins over paying NPC fuel markups (never adding a jump over a 0-jump local station). None when unreachable."""
    dist = jumps(lanes, src, 99)
    pref = set(prefer_bases) if prefer_bases else set()
    best = None
    best_key = None
    for system, (poi, base) in stations.items():
        if base in skip:
            continue
        if system in dist:
            d = dist[system]
            is_pref = bool(pref and (base in pref or system in pref))
            eff_d = (d - 1) if (is_pref and d >= 2) else d
            key = (eff_d, 0 if is_pref else 1, d, system)
            if best_key is None or key < best_key:
                best_key = key
                best = (d, system, poi, base)
    return best


def fuel_short(tank, way, ship=None):
    if tank is None or way is None:
        return False
    if ship is None:
        return tank < PER_JUMP * way + SPARE
    per_jump = ship_jump_cost(ship)
    spare = max(SAFE_SPARE, ship_dock_reserve(ship) * 2.0)
    return tank < per_jump * way + spare


def shortest_path(lanes, src, dst, avoid=()):
    """Shortest system path [src, ..., dst] avoiding `avoid` systems (except src/dst), or None."""
    if not src or not dst:
        return None
    if src == dst:
        return [src]
    skip = set(avoid or ()) - {src, dst}
    parent = {src: None}
    q = deque([src])
    while q:
        u = q.popleft()
        for v in lanes.get(u) or []:
            if v in parent or v in skip:
                continue
            parent[v] = u
            if v == dst:
                path = [dst]
                cur = u
                while cur is not None:
                    path.append(cur)
                    cur = parent[cur]
                path.reverse()
                return path
            q.append(v)
    return None


def plan_refuel_hop(lanes, src, dst, stations, fuel, max_fuel=95, ship=None, skip=(), avoid=(), prefer_bases=None):
    """Choose an intermediate public refuel station (jumps, sys, poi, base) when `fuel` cannot safely
    reach `dst` in one direct leg. Returns None if direct flight is safe OR if no station is reachable."""
    if not src or not dst or src == dst or fuel is None:
        return None
    path = shortest_path(lanes, src, dst, avoid=avoid)
    if not path:
        return None
    total = len(path) - 1
    per_jump = ship_jump_cost(ship) if ship is not None else SAFE_PER_JUMP
    reserve = ship_dock_reserve(ship) if ship is not None else 8.0
    if float(fuel) >= per_jump * total + reserve:
        return None
    safe_lanes = {s: [n for n in nbrs if n not in set(avoid or ())] for s, nbrs in lanes.items() if s not in set(avoid or ())}
    if src not in safe_lanes:
        safe_lanes[src] = [n for n in (lanes.get(src) or []) if n not in set(avoid or ())]
    dist_src = jumps(safe_lanes, src, 99)
    dist_dst = jumps(safe_lanes, dst, 99)
    max_reach = int(max(0.0, (float(fuel) - reserve) // max(1.0, per_jump)))
    skip_set = set(skip or ())
    # 1. Furthest reachable station making strict progress toward dst
    best = None
    for s, (poi, base) in (stations or {}).items():
        if base in skip_set or s not in dist_src or s not in dist_dst:
            continue
        d_s, d_d = dist_src[s], dist_dst[s]
        if d_s <= max_reach and d_d < total:
            _is_p = bool(prefer_bases and (base in prefer_bases or s in prefer_bases))
            _eff_dd = max(0, d_d - 1) if _is_p else d_d
            cand = (_eff_dd, 0 if _is_p else 1, d_d, d_s, s, poi, base)
            if best is None or cand[:5] < best[:5]:
                best = cand
    if best is not None:
        return (best[3], best[4], best[5], best[6])
    # 2. Otherwise top up at nearest reachable fuel station if tank is not already near full
    mf = float(max_fuel or 95)
    if float(fuel) < 0.85 * mf:
        near = None
        for s, (poi, base) in (stations or {}).items():
            if base in skip_set or s not in dist_src:
                continue
            d_s = dist_src[s]
            if d_s <= max_reach:
                cand = (d_s, s, poi, base)
                if near is None or cand[:2] < near[:2]:
                    near = cand
        if near is not None:
            return near
    else:
        # Tank is already full: if a progress station is strictly closer than dst (e.g. 14 hops vs 17),
        # prefer trying that shorter bridge station over an even longer direct jump.
        bridge = None
        for s, (poi, base) in (stations or {}).items():
            if base in skip_set or s not in dist_src or s not in dist_dst:
                continue
            d_s, d_d = dist_src[s], dist_dst[s]
            if 0 < d_s < total and d_d < total:
                cand = (d_s, d_d, s, poi, base)
                if bridge is None or cand[:3] < bridge[:3]:
                    bridge = cand
        if bridge is not None:
            return (bridge[0], bridge[2], bridge[3], bridge[4])
    return None


def route_max_gap(lanes, src, dst, stations, avoid=()):
    """Minimax largest single-tank hop (in jumps) between consecutive public fuel stations from src to dst.
    Returns int jumps, or None if disconnected."""
    if not src or not dst:
        return None
    if src == dst:
        return 0
    import heapq
    avoid_set = set(avoid or ()) - {src, dst}
    safe_lanes = {s: [n for n in nbrs if n not in avoid_set] for s, nbrs in lanes.items() if s not in avoid_set}
    nodes = sorted(set((stations or {}).keys()) - avoid_set | {src, dst})
    dists = {u: jumps(safe_lanes, u, 99) for u in nodes}
    if dst not in dists.get(src, {}):
        return None
    best = {src: 0}
    pq = [(0, src)]
    while pq:
        gap, u = heapq.heappop(pq)
        if gap > best.get(u, 9999):
            continue
        if u == dst:
            return gap
        du = dists[u]
        for v in nodes:
            if v == u or v not in du:
                continue
            ng = max(gap, du[v])
            if ng < best.get(v, 9999):
                best[v] = ng
                heapq.heappush(pq, (ng, v))
    return None


def can_reach_with_refuels(lanes, src, dst, stations, ship=None, avoid=()):
    """True when `ship`'s full fuel tank can cross the largest station-to-station gap from src to dst."""
    gap = route_max_gap(lanes, src, dst, stations, avoid=avoid)
    if gap is None:
        return False
    if gap == 0:
        return True
    mf = float((ship or {}).get('max_fuel') or 95.0)
    per_jump = ship_jump_cost(ship) if ship is not None else SAFE_PER_JUMP
    reserve = ship_dock_reserve(ship) if ship is not None else 8.0
    return mf >= per_jump * gap + reserve


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

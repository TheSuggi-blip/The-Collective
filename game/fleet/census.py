"""Read one system whole with one pilot: every place's deposits and creatures, and
the station's order book and mission board. Reads only: nothing is attacked or bought.

Usage: python3 -I census.py <pilot> <system_id> [--stay] [--route ID]

Flies to the system, lists its places (`get_system`), visits every belt, ice
field, gas cloud and nebula (`get_poi`: what is left of each resource;
`get_nearby`: creatures by species, pirates, other pilots), then docks at each
station of the system and saves its order book and mission board. Ends docked
at the pilot's home base (its empire's capital, home_of; Central Nexus when no read
places it), or with --stay at the system's last station (docked nowhere: at the
nearest station with fuel, end_stop).

Writes, in the unit's data folder (never the repository):
  scouting/<system>.json   the system and each place's deposits
  wildlife/<system>.json   creatures per place
  market/<base>.json       order book        missions/<base>.json   mission board
While it runs the pilot carries an order file (census <system>); one row goes
to data/routes/runs.jsonl. Prints one line per place and a RESULT line.

Pirates: each place's entry in wildlife/<system>.json keeps, beside the count
(`pirates`), every pirate `get_nearby` lists (`pirate_list`: name, faction, tier,
hull, shield, status), and the history row names them per place, so that
Military reads what stood where (requests.log ENT-182). A census reads and leaves.

Chain: a census route whose file sets `"chain": N` (and `chain_jumps`, default 2)
reads, after the first system, up to N more systems of its own list before it
turns home: the nearest within `chain_jumps` lanes (game/map/galaxy.tsv) that is
due by the route's `every_minutes`, never read first, not read by another ship
now (the order files) and not on this run; only while the tank holds the way
there and home with room to spare. The order file names the system being read
and each system gets its own row. Without `chain` nothing changes.

Fuel: before it flies, the census weighs the tank against the way to the system and on to
the nearest station that sells fuel (a station whose own read in data/scouting lists the
service `refuel`; no pirate stronghold), by the chain's rule (1.5 a jump and 15 over); short,
it takes fuel at the station nearest the ship first, and when even then the tank is short it
writes a row `not flown` and ends. After the read, a ship in a system without a station whose
tank is short of home takes fuel at the nearest station first (with --stay it ends docked
there). A ship never ends a census in space on a tank that cannot leave (2026-11-22). With
--stay a ship docked nowhere (a foreign station refused it) ends at the nearest station with
fuel, never sent across the galaxy to Central Nexus (2026-11-23).

Survey: a pilot whose live file (data/fleet/ships/<pilot>.json) lists a survey
scanner among its modules runs `survey_system` once in each system it reads, on
arrival and before `get_system`, so that a place the survey reveals is read in the
same pass. The answer is kept in scouting/<system>.json (`survey`) and the history
row says `surveyed`. It is the one action that trains scanning (catalog skills;
5 XP for the first survey, observations kind survey). A ship without a scanner
reads as before.

Books from afar: at each station it docks at, the census also reads the books of up to eight other stations
whose market/<base>.json is over an hour old, the stalest first (`view_market` with `base_id`, game 0.728.0:
the live book of any charted station, read while docked), and saves each with the source
`view_market base_id, own ship docked at <base>`. A read costs no tick; the first answer without a book ends it."""
import atexit
import fcntl
import json
import os
import pathlib
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from pathlib import Path

GATE = 'http://172.30.0.32:7580'
OPENER = urllib.request.build_opener(urllib.request.ProxyHandler({}))
DATA = pathlib.Path('/srv/collective/data')
REPO = pathlib.Path(__file__).resolve().parent.parent       # game/: the route files and the chart
HOME = {'systemId': 'nexus_prime', 'poiId': 'the_core', 'baseId': 'central_nexus', 'refuel': True}
FIELDS = ('asteroid_belt', 'ice_field', 'gas_cloud', 'nebula', 'anomaly', 'debris_field', 'comet')
pilot, system_id = sys.argv[1], sys.argv[2]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import division                                   # noqa: E402  the division's lock: own ships only, never a pilot another program flies
division.require(pilot)
P = urllib.parse.quote(pilot, safe='')


def now():
    return time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())


ORDER = DATA / 'fleet' / 'orders' / f'{pilot}.json'
ORDER.parent.mkdir(parents=True, exist_ok=True)
ORDER.write_text(json.dumps({'pilot': pilot, 'what': 'census ' + system_id, 'since': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}), encoding='utf-8')
atexit.register(lambda: ORDER.exists() and ORDER.unlink())
STARTED = time.time()


def say(text):
    print(time.strftime('%H:%M:%S', time.gmtime()), pilot, text, flush=True)
    try:
        os.utime(ORDER)                           # still at it
    except OSError:
        pass


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f'{path.name}.{os.getpid()}.tmp')
    tmp.write_text(json.dumps(value, separators=(',', ':')), encoding='utf-8')
    os.replace(tmp, path)


def call(path, body, timeout=900):
    req = urllib.request.Request(GATE + path, data=json.dumps(body).encode(), method='POST', headers={'Content-Type': 'application/json'})
    try:
        with OPENER.open(req, timeout=timeout) as r:
            return r.status, json.loads(r.read().decode('utf-8', 'replace') or '{}')
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read().decode('utf-8', 'replace') or '{}')
        except ValueError:
            return e.code, {}
    except Exception as e:
        return 0, {'error': f'{type(e).__name__}: {e}'}


def wallet():
    """The pilot's credits from the engine's answer for the account, or None when it holds none."""
    try:
        with OPENER.open(urllib.request.Request(GATE + f'/accounts/{P}'), timeout=60) as r:
            value = ((json.loads(r.read().decode('utf-8', 'replace') or '{}').get('state') or {}).get('credits'))
    except Exception:
        return None
    return int(value) if isinstance(value, (int, float)) and not isinstance(value, bool) else None


WALLET_BEFORE = wallet()


def free_from_battle():
    """A goal refused `in_battle`: set the battle stance flee and wait, three minutes at most, until the ship is out.
    The engine's combat mode flee leaves the battle stance as it was (requests ENT-090; the same step as route_run.py)."""
    raw('stance', {'stance': 'flee'}, 'spacemolt_battle')
    for _ in range(18):
        time.sleep(10)
        if not raw('status', group='spacemolt_battle').get('is_participant'):
            say('out of the battle after the stance flee')
            return True
    say('still in a battle three minutes after the stance flee')
    return False


def goal(kind, options):
    d = {}
    for _ in range(3):
        status, d = call(f'/accounts/{P}/goal', {'type': kind, 'options': options})
        if status == 200 and d.get('success'):
            return True
        if 'in_battle' in str(d.get('message') or d.get('error') or '').lower().replace(' ', '_'):
            free_from_battle()                                               # then the next try
        time.sleep(15)
    say(f'goal {kind} failed: {str(d.get("message") or d.get("error"))[:120]}')
    return False


def raw(action, params=None, group='spacemolt'):
    _, d = call(f'/accounts/{P}/raw', {'toolGroup': group, 'action': action, 'params': params or {}}, timeout=120)
    sc = d.get('structuredContent')
    return sc if isinstance(sc, dict) else {}


def save_station(base, system):
    items = raw('view_market', group='spacemolt_market').get('items') or []
    if items:
        rows = [{k: i.get(k) for k in ('item_id', 'item_name', 'category', 'best_buy', 'best_buy_qty', 'buy_quantity', 'best_sell', 'best_sell_qty', 'sell_quantity')} for i in items if isinstance(i, dict)]
        write_json(DATA / 'market' / f'{base}.json', {'base': base, 'system': system, 'read_at': now(), 'source': 'view_market, own ship docked', 'items': rows})
    ms = raw('get_missions').get('missions') or []
    keep = [{k: m.get(k) for k in ('template_id', 'mission_id', 'title', 'type', 'difficulty', 'rewards', 'objectives', 'expires_in_ticks', 'giver')} for m in ms if isinstance(m, dict)]
    if keep:
        write_json(DATA / 'missions' / f'{base}.json', {'base': base, 'system': system, 'read_at': now(), 'source': 'get_missions, own ship docked', 'missions': keep})
    return len(items), len(keep)


REMOTE_BOOKS = 8            # other stations' books a docked census reads from afar at each dock (game 0.728.0)
REMOTE_AGE = 3600           # seconds: a book younger than this is left as it is


def stale_books(data, here, now, limit, age):
    """[(base, system)] of the station books in data/market that a census docked at `here` reads from afar
    (view_market with base_id, game 0.728.0): every file that is one station's book (it holds `items`; the
    ledger's history files, ladders.json and temporary files are not), not `here`, older than `age` seconds by
    its time on disk, the stalest first, at most `limit`."""
    folder = Path(data) / 'market'
    out = []
    try:
        files = list(folder.iterdir())
    except OSError:
        return []
    for f in files:
        if f.suffix != '.json' or f.name.startswith('history') or f.stem == here:
            continue
        try:
            seen = now - f.stat().st_mtime
            if seen < age:
                continue
            book = json.loads(f.read_text(encoding='utf-8'))
        except (OSError, ValueError):
            continue
        if isinstance(book, dict) and 'items' in book:
            out.append((-seen, f.stem, str(book.get('system') or '')))
    out.sort()
    return [(base, system) for _, base, system in out[:limit]]


def save_remote_books(here):
    """Read and save the books of up to REMOTE_BOOKS other stations from the station docked at (stale_books);
    stops at the first answer without a book (a station not charted, or the ship not docked). The number saved."""
    saved = 0
    for base, system in stale_books(DATA, here, time.time(), REMOTE_BOOKS, REMOTE_AGE):
        items = raw('view_market', {'base_id': base}, 'spacemolt_market').get('items')
        if not isinstance(items, list):
            break
        rows = [{k: i.get(k) for k in ('item_id', 'item_name', 'category', 'best_buy', 'best_buy_qty', 'buy_quantity', 'best_sell', 'best_sell_qty', 'sell_quantity')} for i in items if isinstance(i, dict)]
        write_json(DATA / 'market' / f'{base}.json', {'base': base, 'system': system, 'read_at': now(), 'source': f'view_market base_id, own ship docked at {here}', 'items': rows})
        saved += 1
    return saved


def pirate_details(near):
    """The pirates `get_nearby` lists at a place, each with what Military reads (name, faction, tier, hull, shield,
    status); an answer without a list keeps nothing."""
    keys = ('name', 'faction', 'tier', 'hull', 'max_hull', 'shield', 'max_shield', 'status', 'is_boss')
    found = near.get('pirates') if isinstance(near, dict) else None
    if not isinstance(found, list):
        return []
    return [{k: p.get(k) for k in keys if k in p} for p in found if isinstance(p, dict)]


def scanner_fitted(ship):
    """True when the ship's live file lists a survey scanner among its modules (by type or by name)."""
    mods = ship.get('modules') if isinstance(ship, dict) else None
    if not isinstance(mods, list):
        return False
    return any(isinstance(m, dict) and 'survey_scanner' in str(m.get('type') or m.get('name') or '').lower().replace(' ', '_')
               for m in mods)


def cloak_fitted(ship):
    """True when the ship's live file lists a cloaking device among its modules."""
    mods = ship.get('modules') if isinstance(ship, dict) else None
    if not isinstance(mods, list):
        return False
    return any(isinstance(m, dict) and 'cloak' in str(m.get('type') or m.get('name') or '').lower().replace(' ', '_')
               for m in mods)


def recent_pirate_raid_systems(data, hours=2.0, now_t=None):
    """Systems with active pirate battles in read.db:public_battles over the last `hours`."""
    out = set()
    db = Path(data) / 'store' / 'read.db'
    if not db.is_file():
        return out
    con = None
    try:
        import sqlite3
        con = sqlite3.connect('file:%s?mode=ro&immutable=1' % db, uri=True, timeout=2.0)
        tbls = {r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        if 'public_battles' in tbls:
            cut = (time.time() if now_t is None else float(now_t)) - float(hours) * 3600.0
            for (s_id,) in con.execute("SELECT DISTINCT system FROM public_battles WHERE category='pirate' AND t >= ?", (cut,)):
                if s_id:
                    out.add(str(s_id))
    except Exception:
        pass
    finally:
        if con is not None:
            try:
                con.close()
            except Exception:
                pass
    return out


def jumps(lanes, src, reach):
    """{system: lanes from src} for every system within `reach` lanes, by the chart's lanes."""
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


def next_system(route, here, lanes, data, busy, done, now, reach):
    """The system a chained census reads next: of the route's own list, within `reach` lanes of `here`, due by its
    `every_minutes` (the age of data/scouting/<system>.json, the dispatcher's rule), not being read by another ship
    (`busy`) and not read on this run (`done`); the nearest first, a never-read one before a stale one, then the
    stalest. None when no system is due within reach."""
    near = jumps(lanes, here, reach)
    raided = recent_pirate_raid_systems(data, hours=2.0, now_t=now) if 'recent_pirate_raid_systems' in globals() else set()
    cands = list(route.get('systems') or [])
    if route.get('all_systems'):
        # Dynamic 100% galaxy sweep: include every reachable non-stronghold system (never-scouted prioritized first!)
        sh_set = strongholds() if 'strongholds' in globals() else set()
        seen_c = set(cands)
        for s_id in near:
            if s_id not in seen_c and s_id not in sh_set:
                cands.append(s_id)
                seen_c.add(s_id)
    best = None
    for system in cands:
        if system in busy or system in done or system not in near or system in raided:
            continue
        try:
            age = now - (Path(data) / 'scouting' / (system + '.json')).stat().st_mtime
        except OSError:
            age = float('inf')
        if age < route.get('every_minutes', 60) * 60:
            continue
        key = (near[system], 0 if age == float('inf') else 1, -age)
        if best is None or key < best[0]:
            best = (key, system)
    return best[1] if best else None


def fuel_stations(data):
    """{system: (poi, base)} of the stations whose own census read (data/scouting/<system>.json) lists the
    service `refuel`: where a scout can take on fuel. A broken file or a place without a base counts as none."""
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
                bid = str(base.get('id') or '').strip()
                ftag = str(base.get('faction_tag') or '').strip().upper()
                is_foreign = (ftag != 'CLTV') and (
                    bool(base.get('faction_id') or base.get('owner') or base.get('owner_id'))
                    or (len(bid) == 32 and all(ch in '0123456789abcdef' for ch in bid.lower()))
                )
                if is_foreign:
                    continue
                out.setdefault(f.stem, (poi.get('id') or pid, base['id']))
    # Also include our own active [CLTV] Lockbox/Outpost hubs (excluding any under active pirate raid!)
    try:
        emp_p = Path(data) / 'empire' / 'empire.json'
        if emp_p.is_file():
            emp_d = json.loads(emp_p.read_text(encoding='utf-8'))
            raided_f = recent_pirate_raid_systems(data, hours=2.0)
            for fac in (emp_d.get('facilities') or []):
                if isinstance(fac, dict) and fac.get('type') in ('faction_lockbox', 'outpost') and fac.get('status') == 'active':
                    fsys, fpoi, fbase = str(fac.get('system') or ''), str(fac.get('poi') or ''), str(fac.get('base') or '')
                    if fsys and fpoi and fbase and fsys not in raided_f:
                        out.setdefault(fsys, (fpoi, fbase))
    except Exception:
        pass
    return out


def nearest_fuel(lanes, src, stations):
    """(jumps, system, poi, base) of the station with fuel (fuel_stations) nearest `src` by the chart's lanes,
    the fewest jumps first, then by name; None when none can be reached on the chart."""
    dist = jumps(lanes, src, 99)
    best = None
    for system, (poi, base) in stations.items():
        if system in dist and (best is None or (dist[system], system) < best[:2]):
            best = (dist[system], system, poi, base)
    return best


def fuel_short(tank, way):
    """True when a tank of `tank` cannot fly `way` jumps with room to spare (the chain's rule: 1.5 a jump and
    15 over). An unread tank or an unknown way is not judged: the engine decides, as before."""
    if tank is None or way is None:
        return False
    return tank < 1.5 * way + 15


def refuel_at(stop):
    """Fly to the station `stop` (nearest_fuel) and take on fuel; True when the tank rose or stands full."""
    before = fuel()
    _, sid, poi, base = stop
    goal('prepare-at-station', {'systemId': sid, 'poiId': poi, 'baseId': base, 'refuel': True})
    after = fuel()
    if after is not None and before is not None and after <= before:
        raw('dock')                                     # the goal ended at the station undocked (seen 2026-11-22)
        raw('refuel')
        after = fuel()
    say(f'fuel stop at {sid} ({base}): fuel {before} -> {after}')
    return after


def refuel_hops(lanes, here, target, onward, stations, tank, max_fuel, ship, fp, limit=3):
    """The fuel stations to call at, in order, so that the tank flies from `here` to `target` and `onward` jumps on to
    fuel: [] when the tank flies it as it stands, None when no chain of at most `limit` stops brings it in reach.
    Each stop is (jumps, system, poi, base), reached by fuelplan's rule (fp.fuel_short: a jump's fuel and the spare
    of the ship), the one nearest the target first, a stop at `here` only to fill a tank that is not full; at each
    stop the tank is taken as full (2026-11-25: 278 census legs refused in two hours by scouts with full tanks,
    the system farther than one tank)."""
    dist_t = fp.jumps(lanes, target, 99)
    if here not in dist_t or tank is None:
        return None
    hops, cur, fuel, filled = [], here, tank, set()
    while True:
        if not fp.fuel_short(fuel, dist_t[cur] + onward, ship=ship):
            return hops
        if len(hops) >= limit:
            return None
        reach = fp.jumps(lanes, cur, 99)
        best = None
        for system, (poi, base) in sorted(stations.items()):
            d = reach.get(system)
            if d is None or system not in dist_t or (d and fp.fuel_short(fuel, d, ship=ship)):
                continue
            if system == cur:
                if fuel >= max_fuel or system in filled:
                    continue
            elif dist_t[system] >= dist_t[cur]:
                continue
            cand = (dist_t[system], d, system, poi, base)
            if best is None or cand < best:
                best = cand
        if best is None:
            return None
        hops.append((best[1], best[2], best[3], best[4]))
        cur, fuel = best[2], max_fuel
        filled.add(cur)


def end_stop(stay, last_station, short, stop):
    """Where a census ends: ('stay', None) docked where it last read (--stay); ('fuel', stop) with --stay and
    docked nowhere, at the nearest station with fuel (2026-11-23: a scout refused by a foreign station, `Access
    denied`, was sent across the galaxy to Central Nexus); ('fuel-home', stop) without --stay and a tank short
    of home, fuel first and then home; else ('home', None). `stop` is nearest_fuel's answer or None."""
    if stay and last_station:
        return 'stay', None
    if not last_station and stop and (stay or short):
        return ('fuel' if stay else 'fuel-home'), stop
    return 'home', None


def home_of(ship, stations, default):
    """The station a census without --stay ends at (a dict for the goal prepare-at-station): the pilot's own home
    base, the station of the capital its empire gave it (live file `home_base`), placed by the station read that
    lists fuel (`stations`, fuel_stations); a copy of `default`, Central Nexus, when the file names none or no read
    places it (2026-11-23, queue.log ENT-259: a census without --stay sent newborns of other empires home across
    the galaxy to Central Nexus)."""
    base = ship.get('home_base') if isinstance(ship, dict) else None
    if isinstance(base, str) and base and isinstance(stations, dict):
        for system, place in stations.items():
            if isinstance(place, (tuple, list)) and len(place) == 2 and place[1] == base:
                return {'systemId': system, 'poiId': place[0], 'baseId': base, 'refuel': True}
    return dict(default)


def strongholds():
    """The systems the chart flags `stronghold` (game/map/galaxy.tsv): no census takes fuel at a pirate's station."""
    try:
        rows = [line.rstrip('\n').split('\t') for line in open(REPO / 'map' / 'galaxy.tsv', encoding='utf-8') if not line.startswith('#')]
    except OSError:
        return set()
    head = rows[0] if rows else []
    return {cell['id'] for cell in (dict(zip(head, row)) for row in rows[1:]) if 'stronghold' in str(cell.get('flags') or '')}


def ship_system():
    """The system the pilot's live file (data/fleet/ships/<pilot>.json) places it in, or None."""
    try:
        return str(json.loads((DATA / 'fleet' / 'ships' / f'{pilot}.json').read_text(encoding='utf-8')).get('system') or '') or None
    except (OSError, ValueError, AttributeError):
        return None


def chart():
    """({system: [lanes]}, {system: jumps from home}) from game/map/galaxy.tsv; empty when the file cannot be read."""
    lanes, home = {}, {}
    try:
        rows = [line.rstrip('\n').split('\t') for line in open(REPO / 'map' / 'galaxy.tsv', encoding='utf-8') if not line.startswith('#')]
    except OSError:
        return lanes, home
    head = rows[0] if rows else []
    for row in rows[1:]:
        cell = dict(zip(head, row))
        if cell.get('id'):
            lanes[cell['id']] = [x for x in (cell.get('lanes') or '').split(',') if x]
            home[cell['id']] = int(cell['jumps_from_home']) if str(cell.get('jumps_from_home', '')).isdigit() else None
    # Merge live read.db:lanes so scouts dynamically discover & sweep new frontier systems not yet in galaxy.tsv!
    try:
        db_l = DATA / 'store' / 'read.db'
        if db_l.is_file():
            import sqlite3
            _cl = sqlite3.connect('file:%s?mode=ro&immutable=1' % db_l, uri=True, timeout=2.0)
            try:
                for _la, _lb in _cl.execute('SELECT a, b FROM lanes'):
                    if _la and _lb:
                        if _lb not in lanes.get(_la, ()):
                            lanes.setdefault(str(_la), []).append(str(_lb))
                        if _la not in lanes.get(_lb, ()):
                            lanes.setdefault(str(_lb), []).append(str(_la))
            finally:
                _cl.close()
    except Exception:
        pass
    return lanes, home


def busy_systems():
    """The systems other pilots' census orders name now (data/fleet/orders)."""
    out = set()
    for f in (DATA / 'fleet' / 'orders').glob('*.json'):
        if f.name == ORDER.name:
            continue
        try:
            what = str(json.loads(f.read_text(encoding='utf-8')).get('what') or '')
        except (OSError, ValueError):
            continue
        if what.startswith('census '):
            out.add(what.split(' ', 1)[1])
    return out


def fuel():
    """The ship's fuel from the engine's answer for the account, or None."""
    try:
        with OPENER.open(urllib.request.Request(GATE + f'/accounts/{P}'), timeout=60) as r:
            value = ((json.loads(r.read().decode('utf-8', 'replace') or '{}').get('state') or {}).get('ship') or {}).get('fuel')
    except Exception:
        return None
    return int(value) if isinstance(value, (int, float)) and not isinstance(value, bool) else None


def read_system(sid):
    """Fly to `sid` and read it whole (places, creatures, pirates, stations); (read, places, creatures, last station)."""
    places = creatures = 0
    station = None
    if not goal('navigate-to-system', {'targetSystemId': sid}):
        return False, 0, 0, None
    if CLOAK:
        try:
            raw('cloak')
        except Exception:
            pass
    survey = raw('survey_system') if SCANNER else None          # before get_system: a place it reveals is read too
    if survey is not None:
        say('survey: ' + (str(survey.get('message') or survey.get('result') or '') or 'answer keys ' + ','.join(sorted(survey))[:160])[:240])
    system = raw('get_system').get('system') or {}
    scouting = {'system': system, 'read_at': now(), 'pois': {}}
    if survey:
        scouting['survey'] = survey
    wildlife = {'system': sid, 'read_at': now(), 'pois': {}}
    pois = [p for p in system.get('pois') or [] if isinstance(p, dict)]
    say(f'{system.get("name")}: {len(pois)} places: ' + ', '.join(f'{p.get("id")} ({p.get("type")})' for p in pois)[:400])
    for p in pois:
        if p.get('type') not in FIELDS:
            continue
        if not goal('go-to-poi', {'targetPoiId': p['id']}):
            continue
        read = raw('get_poi')
        near = raw('get_nearby')
        scouting['pois'][p['id']] = read
        found = [c for c in near.get('creatures') or [] if isinstance(c, dict)]
        species = Counter((c.get('species'), c.get('role')) for c in found)
        pirates = pirate_details(near)
        wildlife['pois'][p['id']] = {'type': p.get('type'), 'read_at': now(),
                                     'creatures': [{k: c.get(k) for k in ('species', 'name', 'role', 'hull', 'max_hull', 'in_combat')} for c in found],
                                     'pirates': near.get('pirate_count') or len(pirates), 'pirate_list': pirates, 'pilots': near.get('count') or 0}
        res = read.get('resources') or (read.get('poi') or {}).get('resources') or []
        places += 1
        creatures += len(found)
        p_cnt = int(near.get('pirate_count') or len(pirates) or 0)
        say(f'{p["id"]} ({p.get("type")}): ' + ('; '.join(f'{r.get("resource_id")} {r.get("remaining")}/{r.get("max_remaining")}' for r in res) or 'no deposit')
            + ' | creatures: ' + (', '.join(f'{n} {s} ({role})' for (s, role), n in species.most_common()) or 'none')
            + f' | pirates {p_cnt}, pilots {near.get("count") or 0}'
            + (' (' + ', '.join(f'{x.get("name")} {x.get("tier") or "?"} hull {x.get("hull")}' for x in pirates)[:200] + ')' if pirates else ''))
        if p_cnt > 0:
            say(f'pirates spotted at {sid}:{p["id"]} ({p_cnt}) -- bailing out of system immediately (scout safety)')
            break
    for p in pois:
        if p.get('type') == 'station' and p.get('base_id'):
            if goal('prepare-at-station', {'systemId': sid, 'poiId': p['id'], 'baseId': p['base_id'], 'refuel': True}):
                scouting['pois'][p['id']] = raw('get_poi')
                n_items, n_missions = save_station(p['base_id'], sid)
                station = p['base_id']
                say(f'docked at {p["base_id"]}: order book {n_items} items, board {n_missions} missions saved')
                far = save_remote_books(p['base_id'])
                if far:
                    say(f'from {p["base_id"]}: {far} books of other stations read from afar (view_market base_id)')
    write_json(DATA / 'scouting' / f'{sid}.json', scouting)
    write_json(DATA / 'wildlife' / f'{sid}.json', wildlife)
    with open(DATA / 'wildlife' / 'history.jsonl', 'a', encoding='utf-8') as fh:      # herds and deposits over time: what regrows, and how fast
        fcntl.flock(fh, fcntl.LOCK_EX)
        row = {'at': now(), 'system': sid,
               'herds': {poi: dict(Counter(c.get('species') for c in v['creatures'])) for poi, v in wildlife['pois'].items()},
               'pilots': {poi: v.get('pilots') for poi, v in wildlife['pois'].items()},
               'deposits': {poi: {r.get('resource_id'): r.get('remaining') for r in (v.get('resources') or (v.get('poi') or {}).get('resources') or [])
                                  if isinstance(r, dict)} for poi, v in scouting['pois'].items()}}
        seen = {poi: v['pirate_list'] for poi, v in wildlife['pois'].items() if v.get('pirate_list')}
        if seen:
            row['pirates'] = seen
        if survey is not None:
            row['surveyed'] = bool(survey)
        fh.write(json.dumps(row, separators=(',', ':')) + '\n')
    return True, places, creatures, station


def write_row(sid, started, before, after, places, creatures, notes):
    read = before is not None and after is not None
    with open(DATA / 'routes' / 'runs.jsonl', 'a', encoding='utf-8') as fh:
        fcntl.flock(fh, fcntl.LOCK_EX)
        fh.write(json.dumps({'route': ROUTE_ID or 'census', 'kind': 'census', 'pilot': pilot,
                             'started': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(started)), 'minutes': round((time.time() - started) / 60, 1),
                             'system': sid, 'places': places, 'creatures': creatures, 'credits_before': before, 'credits_after': after,
                             'delta': after - before if read else 0, 'one_time': 0, 'notes': notes + ([] if read else ['wallet not read'])},
                            separators=(',', ':')) + '\n')


ROUTE_ID = sys.argv[sys.argv.index('--route') + 1] if '--route' in sys.argv else None
ROUTE = {}
if ROUTE_ID:
    try:
        ROUTE = json.loads((REPO / 'routes' / (ROUTE_ID + '.json')).read_text(encoding='utf-8'))
    except (OSError, ValueError):
        ROUTE = {}
CHAIN = int(ROUTE.get('chain') or 0) if ROUTE.get('kind') == 'census' and isinstance(ROUTE.get('chain'), int) else 0
REACH = int(ROUTE.get('chain_jumps') or 2) if isinstance(ROUTE.get('chain_jumps', 2), int) else 2
try:                                                           # a survey scanner aboard: survey each system read
    _ship_f = json.loads((DATA / 'fleet' / 'ships' / f'{pilot}.json').read_text(encoding='utf-8'))
    SCANNER = scanner_fitted(_ship_f)
    CLOAK = cloak_fitted(_ship_f)
except (OSError, ValueError):
    SCANNER = False
    CLOAK = False

places = creatures_total = 0
last_station = None
done, target, legs = set(), system_id, 0
leg_started, leg_before = STARTED, WALLET_BEFORE
LANES, HOME_JUMPS = chart()                    # the chain and the fuel check both fly by the chart
FARS = strongholds()
STATIONS = {s: v for s, v in fuel_stations(DATA).items() if s not in FARS}
import fuelplan as _fp
SHIP_DOC = None
try:                                                           # home: the pilot's own capital, not ours for all
    SHIP_DOC = json.loads((DATA / 'fleet' / 'ships' / f'{pilot}.json').read_text(encoding='utf-8'))
    HOME = home_of(SHIP_DOC, STATIONS, HOME)
except (OSError, ValueError):
    SHIP_DOC = None
if HOME['systemId'] != 'nexus_prime':                          # the way home counts to that capital
    HOME_JUMPS = jumps(LANES, HOME['systemId'], 99)
_PJ = _fp.ship_jump_cost(SHIP_DOC)
_SP = max(_fp.SAFE_SPARE, _fp.ship_dock_reserve(SHIP_DOC) * 2.0)
HERE = ship_system()
ONWARD = nearest_fuel(LANES, system_id, STATIONS)          # where the ship takes fuel after its read
WAY = jumps(LANES, HERE, 99).get(system_id) if HERE else None
if WAY is not None:
    WAY += ONWARD[0] if ONWARD else (HOME_JUMPS.get(system_id) or 0)
TANK = fuel()
if _fp.fuel_short(TANK, WAY, ship=SHIP_DOC):                     # never fly out on a tank that cannot take the ship on to fuel
    ON = ONWARD[0] if ONWARD else (HOME_JUMPS.get(system_id) or 0)
    MAXF = (SHIP_DOC or {}).get('max_fuel') if isinstance((SHIP_DOC or {}).get('max_fuel'), (int, float)) else TANK
    HOPS = refuel_hops(LANES, HERE, system_id, ON, STATIONS, TANK, MAXF, SHIP_DOC, _fp) if HERE else None
    STOP = nearest_fuel(LANES, HERE, STATIONS)
    STOPS = HOPS if HOPS else ([STOP] if STOP else [])       # a far system by the stations between, else as before
    say(f'fuel {TANK} short of {_PJ * WAY + _SP:.0f} for {system_id} and on to fuel: '
        + (f'fuel stop at {", ".join(s[1] for s in STOPS)} first' if STOPS else 'no station with fuel on the chart'))
    for STOP in STOPS:
        before_ref = TANK
        TANK = refuel_at(STOP)
        if TANK is None or before_ref is None or (TANK <= before_ref and TANK < (MAXF or 0)):
            break                                       # a stop that gave no fuel ends the way there
    if STOPS:
        HERE = ship_system() or HERE
        WAY2 = jumps(LANES, HERE, 99).get(system_id) if HERE else None
        WAY = None if WAY2 is None else WAY2 + ON
    if not STOPS or _fp.fuel_short(TANK, WAY, ship=SHIP_DOC):
        write_row(system_id, STARTED, WALLET_BEFORE, wallet(), 0, 0, [f'fuel {TANK} short for {system_id}: not flown'])
        print(f'RESULT {pilot}: {system_id}: not flown, fuel {TANK} short of the way there and on to fuel', flush=True)
        sys.exit(0)
while True:
    if target != system_id:
        ORDER.write_text(json.dumps({'pilot': pilot, 'what': 'census ' + target, 'since': now()}), encoding='utf-8')
    ok, n_places, n_creatures, station = read_system(target)
    done.add(target)
    places += n_places
    creatures_total += n_creatures
    last_station = station
    nxt, why = None, '' if ok else f'{target} not reached'     # a row that says why it read nothing
    if ok and legs < CHAIN:
        nxt = next_system(ROUTE, target, LANES, str(DATA), busy_systems(), done, time.time(), REACH)
        if nxt:
            nxt_near = nearest_fuel(LANES, nxt, STATIONS)
            nxt_leg = nxt_near[0] if nxt_near else (HOME_JUMPS.get(nxt) or 30)
            way = jumps(LANES, target, REACH).get(nxt, REACH) + nxt_leg
            tank = fuel()
            if tank is None or _fp.fuel_short(tank, way, ship=SHIP_DOC):
                say(f'next {nxt}: fuel {tank} short of {_PJ * way + _SP:.0f} for the way there and fuel: turning home')
                why, nxt = f'chain ended on fuel {tank}', None
    if not nxt:
        break
    say(f'chain: {target} read, next {nxt} ({legs + 1} of {CHAIN})')
    leg_after = wallet()
    write_row(target, leg_started, leg_before, leg_after, n_places, n_creatures, [f'chain {legs + 1} of {CHAIN}: next {nxt}'])
    leg_started, leg_before, target, legs = time.time(), leg_after, nxt, legs + 1
STAY = '--stay' in sys.argv
END, STOP = end_stop(STAY, last_station, not last_station and _fp.fuel_short(fuel(), HOME_JUMPS.get(target), ship=SHIP_DOC),
                     None if last_station else nearest_fuel(LANES, target, STATIONS))
if END in ('fuel', 'fuel-home'):                  # docked nowhere: the nearest station with fuel, and with --stay
    refuel_at(STOP)                               # end docked there, never sent home across the galaxy (2026-11-23)
    last_station = STOP[3] if END == 'fuel' else None
if END in ('home', 'fuel-home'):
    goal('prepare-at-station', HOME)
WALLET_AFTER = wallet()
write_row(target, leg_started, leg_before, WALLET_AFTER, n_places, n_creatures, ([why] if why else []) + ([f'chain {legs} of {CHAIN}: last'] if legs else []))
print(f'RESULT {pilot}: {", ".join(sorted(done)) if legs else system_id}: {places} places read, {creatures_total} creatures seen, station {last_station or "none"} | '
      f'credits {WALLET_BEFORE} -> {WALLET_AFTER}', flush=True)

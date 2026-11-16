"""Read one system whole with one pilot: every place's deposits and creatures, and
the station's order book and mission board. Reads only: nothing is attacked or bought.

Usage: python3 -I census.py <pilot> <system_id> [--stay] [--route ID]

Flies to the system, lists its places (`get_system`), visits every belt, ice
field, gas cloud and nebula (`get_poi`: what is left of each resource;
`get_nearby`: creatures by species, pirates, other pilots), then docks at each
station of the system and saves its order book and mission board. Ends docked
at Central Nexus, or with --stay at the system's last station.

Writes, in the unit's data folder (never the repository):
  scouting/<system>.json   the system and each place's deposits
  wildlife/<system>.json   creatures per place
  market/<base>.json       order book        missions/<base>.json   mission board
While it runs the pilot carries an order file (census <system>); one row goes
to data/routes/runs.jsonl. Prints one line per place and a RESULT line."""
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

GATE = 'http://172.30.0.32:7580'
OPENER = urllib.request.build_opener(urllib.request.ProxyHandler({}))
DATA = pathlib.Path('/srv/collective/data')
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


places = creatures_total = 0
last_station = None
if goal('navigate-to-system', {'targetSystemId': system_id}):
    system = raw('get_system').get('system') or {}
    scouting = {'system': system, 'read_at': now(), 'pois': {}}
    wildlife = {'system': system_id, 'read_at': now(), 'pois': {}}
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
        wildlife['pois'][p['id']] = {'type': p.get('type'), 'read_at': now(),
                                     'creatures': [{k: c.get(k) for k in ('species', 'name', 'role', 'hull', 'max_hull', 'in_combat')} for c in found],
                                     'pirates': near.get('pirate_count') or 0, 'pilots': near.get('count') or 0}
        res = read.get('resources') or (read.get('poi') or {}).get('resources') or []
        places += 1
        creatures_total += len(found)
        say(f'{p["id"]} ({p.get("type")}): ' + ('; '.join(f'{r.get("resource_id")} {r.get("remaining")}/{r.get("max_remaining")}' for r in res) or 'no deposit')
            + ' | creatures: ' + (', '.join(f'{n} {s} ({role})' for (s, role), n in species.most_common()) or 'none')
            + f' | pirates {near.get("pirate_count") or 0}, pilots {near.get("count") or 0}')
    for p in pois:
        if p.get('type') == 'station' and p.get('base_id'):
            if goal('prepare-at-station', {'systemId': system_id, 'poiId': p['id'], 'baseId': p['base_id'], 'refuel': True}):
                scouting['pois'][p['id']] = raw('get_poi')
                n_items, n_missions = save_station(p['base_id'], system_id)
                last_station = p['base_id']
                say(f'docked at {p["base_id"]}: order book {n_items} items, board {n_missions} missions saved')
    write_json(DATA / 'scouting' / f'{system_id}.json', scouting)
    write_json(DATA / 'wildlife' / f'{system_id}.json', wildlife)
    with open(DATA / 'wildlife' / 'history.jsonl', 'a', encoding='utf-8') as fh:      # herds and deposits over time: what regrows, and how fast
        fcntl.flock(fh, fcntl.LOCK_EX)
        fh.write(json.dumps({'at': now(), 'system': system_id,
                             'herds': {poi: dict(Counter(c.get('species') for c in v['creatures'])) for poi, v in wildlife['pois'].items()},
                             'pilots': {poi: v.get('pilots') for poi, v in wildlife['pois'].items()},
                             'deposits': {poi: {r.get('resource_id'): r.get('remaining') for r in (v.get('resources') or (v.get('poi') or {}).get('resources') or [])
                                                if isinstance(r, dict)} for poi, v in scouting['pois'].items()}}, separators=(',', ':')) + '\n')
if not ('--stay' in sys.argv and last_station):
    goal('prepare-at-station', HOME)
WALLET_AFTER = wallet()
READ = WALLET_BEFORE is not None and WALLET_AFTER is not None
with open(DATA / 'routes' / 'runs.jsonl', 'a', encoding='utf-8') as fh:
    fcntl.flock(fh, fcntl.LOCK_EX)
    fh.write(json.dumps({'route': sys.argv[sys.argv.index('--route') + 1] if '--route' in sys.argv else 'census', 'kind': 'census', 'pilot': pilot,
                         'started': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(STARTED)), 'minutes': round((time.time() - STARTED) / 60, 1),
                         'system': system_id, 'places': places, 'creatures': creatures_total, 'credits_before': WALLET_BEFORE, 'credits_after': WALLET_AFTER,
                         'delta': WALLET_AFTER - WALLET_BEFORE if READ else 0, 'one_time': 0, 'notes': [] if READ else ['wallet not read']},
                        separators=(',', ':')) + '\n')
print(f'RESULT {pilot}: {system_id}: {places} places read, {creatures_total} creatures seen, station {last_station or "none"} | '
      f'credits {WALLET_BEFORE} -> {WALLET_AFTER}', flush=True)

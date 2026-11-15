"""Hunt grazers at one place, loot the carcasses and sell what the kills bring.

Usage: python3 -I hunt.py <pilot> <system_id> <poi> [--species a,b] [--kills N] [--minutes M]
                          [--min-bid CR] [--sell-at system:poi:base] [--route ID] [--keep]

Only creatures whose role is `grazer` are hunted (the game: prey that
does not start a fight; wildlife never joins a herd-mate's fight; hunting
is legal everywhere). A creature another pilot fights is left alone, and
when a pilot or an NPC ship is in our fight the pilot flees (posture HOLD).

What was measured (2026-11-15, starter ship Threshold):
- A fight starts at distance 6; the ship advances until its weapon reaches.
- A hurt grazer can flee and end the fight; its damage stays, so the most
  hurt one is hunted first.
- A kill leaves a carcass wreck that holds the goods (a veil-ray: 1 or 2
  verdigris curd and carapace; a belt-grazer: carapace and meat). It must be
  looted, which is refused while in a battle, and it expires 30 minutes
  after the kill. Only this pilot's own kills are looted.
- With a Pulse Laser I (10 damage, reach 3): a veil-ray of 60 hull about
  every four minutes. With a Piercing Railgun I (60 damage, reach 5, ammo):
  a belt-grazer in one fight of under a minute.
- A second ship cannot join a hunt: `engage` answers `no_battle`.
- The engine's own answer to any fight is to flee. For the hunt the
  pilot's combat mode is set to `external` (this script drives the fight
  and sends the engine a heartbeat) and back to `flee` afterwards.
- A weapon with a magazine is refilled from the same ammo in the hold
  when it runs low; without ammo the hunt ends.

The pilot flees a fight when its hull falls under half. After --kills
kills (default 5) or --minutes minutes (default 40), or when no grazer is
left or the hold is full, it loots once more, docks at the station named
by --sell-at (default Central Nexus), sells every good in its hold whose
best bid there is at least --min-bid (default 50 cr). Goods another
station of ours bids for stay aboard; the rest (not its ammo) goes into
its storage there. --keep skips selling and stashing.
While it runs the pilot carries an order file (the station shows it at
work). Prints one line per step and a RESULT line, and appends one row to
data/routes/runs.jsonl under the id given by --route (default hunt-<poi>)."""
import atexit
import fcntl
import glob
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

GATE = 'http://172.30.0.32:7580'
OPENER = urllib.request.build_opener(urllib.request.ProxyHandler({}))
HOME = {'systemId': 'nexus_prime', 'poiId': 'the_core', 'baseId': 'central_nexus', 'refuel': True}
SHIPS = '/srv/collective/data/fleet/ships/'
args = sys.argv[1:]
pilot, system_id, poi = args[0], args[1], args[2]
species = set(args[args.index('--species') + 1].split(',')) if '--species' in args else None
max_kills = int(args[args.index('--kills') + 1]) if '--kills' in args else 5
max_minutes = int(args[args.index('--minutes') + 1]) if '--minutes' in args else 40
min_bid = int(args[args.index('--min-bid') + 1]) if '--min-bid' in args else 50
sell_at = args[args.index('--sell-at') + 1].split(':') if '--sell-at' in args else ['nexus_prime', 'the_core', 'central_nexus']
route_id = args[args.index('--route') + 1] if '--route' in args else 'hunt-' + poi
MARKET = '/srv/collective/data/market/'
ORDER = f'/srv/collective/data/fleet/orders/{pilot}.json'
RUNS = '/srv/collective/data/routes/runs.jsonl'
P = urllib.parse.quote(pilot, safe='')


def order(what):
    """Tell the station what this pilot is doing; the file is removed when the run ends."""
    os.makedirs(os.path.dirname(ORDER), exist_ok=True)
    with open(f'{ORDER}.{os.getpid()}.tmp', 'w', encoding='utf-8') as fh:
        json.dump({'pilot': pilot, 'what': what, 'since': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}, fh)
    os.replace(f'{ORDER}.{os.getpid()}.tmp', ORDER)


def order_done():
    try:
        os.remove(ORDER)
    except OSError:
        pass


def say(text):
    print(time.strftime('%H:%M:%S', time.gmtime()), pilot, text, flush=True)
    try:
        os.utime(ORDER)                           # still at it
    except OSError:
        pass


def call(method, path, body=None, timeout=900):
    data = None if body is None else json.dumps(body).encode()
    req = urllib.request.Request(GATE + path, data=data, method=method, headers={'Content-Type': 'application/json'} if data else {})
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


def goal(kind, options):
    for _ in range(3):
        status, d = call('POST', f'/accounts/{P}/goal', {'type': kind, 'options': options})
        if status == 200 and d.get('success'):
            return True
        time.sleep(15)
    say(f'goal {kind} failed: {str(d.get("message") or d.get("error"))[:120]}')
    return False


def raw(action, params=None, group='spacemolt', pilot=None):
    who = urllib.parse.quote(pilot, safe='') if pilot else P
    _, d = call('POST', f'/accounts/{who}/raw', {'toolGroup': group, 'action': action, 'params': params or {}}, timeout=120)
    return d


def body(d):
    sc = d.get('structuredContent')
    return sc if isinstance(sc, dict) else {}


def text(d):
    return d.get('result') if isinstance(d.get('result'), str) else json.dumps(d.get('structuredContent') or d)


def credits():
    return ((call('GET', f'/accounts/{P}')[1].get('state') or {}).get('credits')) or 0


def hull():
    try:
        s = json.load(open(SHIPS + pilot + '.json', encoding='utf-8'))
        return s.get('hull') or 0, s.get('max_hull') or 1
    except (OSError, ValueError):
        return 1, 1


def cargo():
    _, d = call('GET', f'/accounts/{P}/state/cargo')
    return {r.get('item_id'): r.get('quantity') or 0 for r in (d if isinstance(d, list) else []) if isinstance(r, dict)}


def combat_mode(mode):
    status, d = call('PATCH', f'/accounts/{P}/combat-mode', {'mode': mode}, timeout=30)
    say(f'combat mode {mode}: {status} {json.dumps(d)[:80]}')
    return status == 200


def reload_if_low(floor=1):
    """Fill the magazine of every ammo weapon that holds `floor` rounds or fewer, from the same ammo in the hold."""
    for m in body(raw('get_ship')).get('modules') or []:
        if isinstance(m, dict) and m.get('magazine_size') and (m.get('current_ammo') or 0) <= floor:
            ammo = m.get('loaded_ammo_id') or next((i for i in cargo() if i.endswith(('_slug_case', '_rounds_box', '_missiles', '_pack', '_shot', '_rounds'))), None)
            if ammo and cargo().get(ammo):
                d = raw('reload', {'weapon_instance_id': m.get('module_id'), 'ammo_item_id': ammo}, group='spacemolt_battle')
                say(f'reload {m.get("type_id")} with {ammo} ({m.get("current_ammo")} left): {text(d)[:80] if "error" in d else "ok"}')
            else:
                say(f'{m.get("type_id")}: {m.get("current_ammo")} rounds and no ammo in the hold')
                return False
    return True


LOOTED = set()


def loot_own():
    """Loot the carcasses this pilot killed here (never another's). Returns how many new ones there were."""
    new = 0
    for w in body(raw('wrecks', group='spacemolt_salvage')).get('wrecks') or []:
        if not isinstance(w, dict) or w.get('killer_name') != pilot or w.get('id') in LOOTED:
            continue
        if w.get('cargo'):
            d = raw('loot', {'wreck_id': w['id']}, group='spacemolt_salvage')
            time.sleep(10)
            if 'error' in d:
                say(f'loot refused: {str(d.get("error"))[:100]}')
                continue
        LOOTED.add(w['id'])
        new += 1
    return new


def ammo_ids():
    return {m.get('loaded_ammo_id') for m in body(raw('get_ship')).get('modules') or [] if isinstance(m, dict) and m.get('loaded_ammo_id')}


def in_battle():
    st = raw('status', group='spacemolt_battle')
    return bool(body(st).get('is_participant')), text(st)


def fight():
    """Drive the running battle to its end: close in, fire, flee under half hull. True when it ended."""
    for tick in range(90):                           # at most 15 minutes for one fight
        beat = call('POST', f'/accounts/{P}/combat-heartbeat', {}, timeout=20)[0]   # or the engine flees for us after 50 s
        if tick == 0 and beat != 200:
            say(f'combat heartbeat answered {beat}')
        mine, t = in_battle()
        if not mine:
            return True
        if tick % 3 == 2:
            reload_if_low(0)
        if tick % 6 == 0:
            say('battle: ' + ' / '.join(row for row in t.splitlines() if '\t' in row and not row.startswith('player\t'))[:400])
        h, m = hull()
        kinds = [c[1] for c in (row.split('\t') for row in t.splitlines()) if len(c) > 9 and c[0] != 'player']
        if h < m * 0.5:
            say(f'hull {h}/{m}: fleeing')
            raw('stance', {'stance': 'flee'}, group='spacemolt_battle')
        elif kinds and any(k != 'creature' for k in kinds if k != 'player') or kinds.count('player') > 1:
            # a pilot or an NPC ship is in this fight: the posture toward them is HOLD
            say('not a hunt any more (a ship is in the fight): fleeing | ' + ' / '.join(row for row in t.splitlines() if '\t' in row)[:300])
            raw('stance', {'stance': 'flee'}, group='spacemolt_battle')
        else:
            # close in: a battle starts at distance 6 and a Pulse Laser I reaches 3
            reach = re.search(r'Max weapon reach: (\d+)', t)
            dist = [int(c[5]) for c in (row.split('\t') for row in t.splitlines()) if len(c) > 5 and c[1] == 'creature' and c[5].isdigit()]
            if reach and dist and min(dist) > int(reach.group(1)):
                d = raw('advance', {}, group='spacemolt_battle')
                if tick < 2:
                    say('advance: ' + text(d)[:200].replace('\n', ' / '))
        time.sleep(10)
    say('the fight did not end in 15 minutes: fleeing and stopping')
    raw('stance', {'stance': 'flee'}, group='spacemolt_battle')
    return False


before_credits, before_cargo = credits(), cargo()
if not combat_mode('external'):
    sys.exit('the engine did not take the combat mode; no hunt')
kills, started, hunt_minutes = 0, time.time(), 0.0
order('hunt ' + route_id)
atexit.register(order_done)
AMMO = ammo_ids()
if goal('navigate-to-system', {'targetSystemId': system_id}) and goal('go-to-poi', {'targetPoiId': poi}):
    arrived = time.time()
    left = loot_own()                                # carcasses of ours from an earlier run, if any
    if left:
        say(f'{left} carcass(es) of ours were still here: looted')
    while kills < max_kills and time.time() - started < max_minutes * 60:
        held = cargo()
        if not reload_if_low():
            break
        if in_battle()[0]:
            say('already in a battle: taking it up')
        else:
            near = body(raw('get_nearby'))
            prey = [c for c in near.get('creatures') or [] if isinstance(c, dict) and c.get('role') == 'grazer' and not c.get('in_combat')
                    and (species is None or c.get('species') in species)]
            if not prey:
                say(f'no free grazer here (creatures listed: {near.get("creature_count")})')
                break
            target = min(prey, key=lambda c: (c.get('hull') or 0, str(c.get('creature_id'))))   # the most hurt one: its damage stays
            for _ in range(6):
                d = raw('hunt', {'target_id': target['creature_id']})
                if 'action_pending' not in text(d):
                    break
                time.sleep(10)                                         # an earlier command is still queued for the next tick
            say(f'hunt {target.get("name")} (hull {target.get("hull")})' + (': ' + text(d)[:120] if 'error' in text(d)[:40] else ''))
            time.sleep(10)
            if not in_battle()[0]:
                continue
        if not fight():
            break
        time.sleep(3)
        new = loot_own()
        now = cargo()
        gain = {k: v - held.get(k, 0) for k, v in now.items() if v - held.get(k, 0) > 0}
        h, m = hull()
        if new:
            kills += new
            say(f'kill {kills} after {(time.time() - arrived) / 60:.1f} min at the place: {gain or "an empty carcass"} | hull {h}/{m}, hold {sum(now.values())}')
        if h < m * 0.5 or sum(now.values()) >= 60:
            break
    if not in_battle()[0]:
        kills += loot_own()                          # nothing of ours is left behind
    hunt_minutes = (time.time() - arrived) / 60
combat_mode('flee')
goods = {k: v - before_cargo.get(k, 0) for k, v in cargo().items() if v - before_cargo.get(k, 0) > 0}
say(f'goods from this hunt: {goods}')
sold = {}
if goal('prepare-at-station', {'systemId': sell_at[0], 'poiId': sell_at[1], 'baseId': sell_at[2], 'refuel': True}) and '--keep' not in args:
    items = [i for i in (body(raw('view_market', group='spacemolt_market')).get('items') or []) if isinstance(i, dict)]
    if items:
        rows = [{k: i.get(k) for k in ('item_id', 'item_name', 'category', 'best_buy', 'buy_quantity', 'best_sell', 'sell_quantity')} for i in items]
        tmp = f'{MARKET}{sell_at[2]}.json.{os.getpid()}.tmp'
        with open(tmp, 'w', encoding='utf-8') as fh:
            json.dump({'base': sell_at[2], 'system': sell_at[0], 'read_at': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
                       'source': 'view_market, own ship docked', 'items': rows}, fh, separators=(',', ':'))
        os.replace(tmp, f'{MARKET}{sell_at[2]}.json')
    book = {i.get('item_id'): i for i in items}
    for item, qty in cargo().items():
        if item in AMMO:
            continue
        row = book.get(item) or {}
        bid, depth = row.get('best_buy') or 0, row.get('buy_quantity') or 0
        if isinstance(bid, (int, float)) and bid >= min_bid and depth:
            n = min(qty, depth)
            c0 = credits()
            raw('sell', {'item_id': item, 'quantity': n})
            time.sleep(11)
            sold[item] = (n, bid, credits() - c0)
        elif item in goods:
            say(f'{item}: best bid here {bid} x {depth}: kept')
    wanted = set()                                   # goods some station of ours bids for: they stay aboard for the next sale
    for path in glob.glob(MARKET + '*.json'):
        try:
            wanted.update(i.get('item_id') for i in json.load(open(path, encoding='utf-8')).get('items') or []
                          if isinstance(i.get('best_buy'), (int, float)) and i['best_buy'] >= min_bid and i.get('buy_quantity'))
        except (OSError, ValueError):
            pass
    stashed = {}
    for item, qty in cargo().items():                # the rest goes into storage here: the hold is free for the next hunt
        if item not in AMMO and item not in wanted:
            if 'error' not in raw('deposit', {'item_id': item, 'quantity': qty, 'target': 'self', 'source': 'cargo'}, group='spacemolt_storage'):
                stashed[item] = qty
            time.sleep(11)
    if stashed:
        say(f'stored at {sell_at[2]}: {stashed}')
after = credits()
try:
    os.makedirs(os.path.dirname(RUNS), exist_ok=True)
    with open(RUNS, 'a', encoding='utf-8') as fh:
        fcntl.flock(fh, fcntl.LOCK_EX)
        fh.write(json.dumps({'route': route_id, 'kind': 'hunt', 'pilot': pilot, 'started': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(started)),
                             'minutes': round((time.time() - started) / 60, 1), 'credits_before': before_credits, 'credits_after': after,
                             'delta': after - before_credits, 'one_time': 0, 'kills': kills, 'goods': goods, 'sold': {k: list(v) for k, v in sold.items()},
                             'notes': []}, separators=(',', ':')) + '\n')
except OSError as e:
    say(f'run row not written: {e}')
print(f'RESULT {pilot}: kills {kills} in {hunt_minutes:.0f} min at {poi} | goods {goods} | sold at {sell_at[2]} (units, bid, credits received) {sold} '
      f'| credits {before_credits} -> {after} ({after - before_credits:+d}) | whole trip {(time.time() - started) / 60:.0f} min', flush=True)

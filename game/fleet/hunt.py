"""Hunt grazers at one place, loot the carcasses and sell what the kills bring.

Usage: python3 -I hunt.py <pilot> <system_id> <poi> [--species a,b] [--kills N] [--minutes M]
                          [--min-bid CR] [--sell-at system:poi:base] [--max-prey-hull N]
                          [--route ID] [--keep]

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

Safety (the worst case is a lost ship): prey above --max-prey-hull (default
100) is never picked: a pilot-whale of 220 hull took a starter from 73 to 15
hull inside one fight, railgun or not. No fight is started under 60% hull:
the pilot goes to the station, which repairs. In a fight the pilot reads its
own hull and shield from the battle table every tick and flees under 60% hull,
or when its shield is gone while the prey still has over 40% hull. After --kills
kills (default 5) or --minutes minutes (default 40), or when no grazer is
left or the hold is full, it loots once more, docks at the station named
by --sell-at (default Central Nexus), sells every good in its hold whose
best bid there is at least --min-bid (default 50 cr). Goods another
station bids for, in a book read within the hour, stay aboard; the rest
(not its ammo) goes into its storage there. A good the reserve keeps (surplus.py: short,
or held with no unit to spare) is never sold: it is stored (rule F24). --keep skips
selling and stashing.
While it runs the pilot carries an order file (the station shows it at
work). Prints one line per step and a RESULT line, and appends one row to
data/routes/runs.jsonl under the id given by --route (default hunt-<poi>).
--alone: before every fight it looks who is at the place; where a ship that
is not ours or a pirate stands it does not fight and leaves (beyond policed
space a herd is shared with whoever comes: orders F2, never first, flee).
A route file with `"alone": "pirates"` leaves only where a pirate or a pilot
filed hostile (game/players/h-*.md) stands, and hunts beside other strangers
(rule F13: its Admiral lifts the limit once its runs hold); a stranger who
joins the fight still makes it flee.
--step: the hunt is one step of a circuit (route_run.py, a stop's `hunt`):
the circuit's order file stands, and there is no station trip, no sale and
no row of its own; it prints a STEP line. When it leaves, the runner writes
the herd it sees into data/wildlife/ (the dispatcher's count), and the row
records the hull before, after and at its lowest."""
import atexit
import calendar
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
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import division                                   # noqa: E402  the division's lock: own ships only, never a pilot another program flies
division.require(pilot)
species = set(args[args.index('--species') + 1].split(',')) if '--species' in args else None
max_kills = int(args[args.index('--kills') + 1]) if '--kills' in args else 5
max_minutes = int(args[args.index('--minutes') + 1]) if '--minutes' in args else 40
min_bid = int(args[args.index('--min-bid') + 1]) if '--min-bid' in args else 50
sell_at = args[args.index('--sell-at') + 1].split(':') if '--sell-at' in args else ['nexus_prime', 'the_core', 'central_nexus']
route_id = args[args.index('--route') + 1] if '--route' in args else 'hunt-' + poi
STEP = '--step' in args                      # a step of a circuit: the order file, the station and the row are the circuit's
ALONE = '--alone' in args                    # no fight where a ship that is not ours stands
LOW = [100]                                  # our hull at its lowest in this run, percent
max_prey_hull = int(args[args.index('--max-prey-hull') + 1]) if '--max-prey-hull' in args else 100
MARKET = '/srv/collective/data/market/'
ORDER = f'/srv/collective/data/fleet/orders/{pilot}.json'
RUNS = '/srv/collective/data/routes/runs.jsonl'
P = urllib.parse.quote(pilot, safe='')


def wanted_goods(market, min_bid, now, fresh=3600):
    """The goods a station's book, read within `fresh` seconds, bids `min_bid` or more for: they stay aboard for the next
    sale. A book older than that keeps nothing aboard, the rule of `requires.bid` (a stale book closes nothing): a bid of
    one unit read hours ago kept a hunter's curd aboard and closed the hunts that ask an empty hold (2026-11-16)."""
    wanted = set()
    for path in glob.glob(os.path.join(market, '*.json')):
        try:
            with open(path, encoding='utf-8') as fh:
                book = json.load(fh)
            read = calendar.timegm(time.strptime(str(book.get('read_at')), '%Y-%m-%dT%H:%M:%SZ'))
        except (OSError, ValueError, AttributeError):
            continue
        if now - read > fresh:
            continue
        wanted.update(i.get('item_id') for i in book.get('items') or []
                      if isinstance(i, dict) and isinstance(i.get('best_buy'), (int, float)) and i['best_buy'] >= min_bid and i.get('buy_quantity'))
    return wanted


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


def kept_goods(data, root):
    """{item: units} the reserve keeps and has none of to spare (surplus.py: short, or held with no surplus unit, a good
    held back for another recipe included; the rule of fill.kept_items): the hunt stores them and never sells them
    (rule F24). {} when the reserve cannot be read: then nothing is kept back by it. 2026-11-17: four hunt runs sold 13
    superfluid vials and a scout hunt 6 caustic sacs that the reserve held back (errors.log ENT-095 and after)."""
    try:
        import surplus
        res = surplus.surplus(data, root)
        return {r['id']: (r.get('short') or 0) or (r.get('reserved') or 0) for r in res['rows']
                if (r.get('short') or 0) > 0 or ((r.get('reserved') or 0) > 0 and (r.get('surplus') or 0) <= 0)}
    except Exception:                                   # noqa: BLE001  no reserve read: nothing is kept back by it
        return {}


def saleable(held, kept, ammo):
    """The goods of the hold the sale may offer: not the ship's ammo, not what the reserve keeps."""
    return {item: qty for item, qty in held.items() if item not in ammo and item not in kept}


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


def alone_mode(route_file):
    """How a hunt with --alone judges a place: 'pirates' when its route file says `"alone": "pirates"` (it leaves only
    for a pirate or a pilot of the hostile list), else 'strangers' (it leaves for every ship that is not ours). A file
    that is missing or unreadable keeps the strict rule."""
    try:
        with open(route_file, encoding='utf-8') as fh:
            return 'pirates' if json.load(fh).get('alone') == 'pirates' else 'strangers'
    except (OSError, ValueError, AttributeError):
        return 'strangers'


def hostile_names(folder):
    """The usernames of the pilots filed hostile: the line `username:` of each game/players/h-*.md."""
    names = set()
    for path in glob.glob(os.path.join(folder, 'h-*.md')):
        try:
            with open(path, encoding='utf-8') as fh:
                for line in fh:
                    if line.startswith('username:'):
                        names.add(line.split(':', 1)[1].strip())
                        break
        except OSError:
            continue
    return names


def leave_reason(near, own, mode, hostile):
    """(what to say, the run's note) when a hunt with --alone leaves the place without a fight, or None. A pirate always
    makes it leave; in mode 'strangers' every ship that is not ours does, in mode 'pirates' only a pilot of the hostile
    list. 61 of 161 drone hunts left for a stranger who never fired (2026-11-17 04:12 to 08:10 UTC, runs.jsonl)."""
    others = sorted(str(row.get('username')) for row in (near.get('nearby') or []) if isinstance(row, dict) and row.get('username') and row.get('username') not in own)
    pirates = near.get('pirate_count') or 0
    if pirates:
        return 'pirates %s here, strangers %s' % (pirates, others[:4]), 'left: a pirate was at the place'
    if mode == 'pirates':
        bad = [n for n in others if n in hostile]
        return ('a pilot of the hostile list here: %s' % bad[:4], 'left: a pilot of the hostile list was at the place') if bad else None
    return ('not alone here: %s' % others[:4], 'left: a ship that is not ours was at the place') if others else None


def own_names():
    """The pilots of our fleet; an unreadable fleet file counts every pilot as a stranger (the hunt then leaves)."""
    try:
        return {s.get('name') for s in json.load(open('/srv/collective/data/fleet/fleet.json', encoding='utf-8')).get('ships') or []}
    except (OSError, ValueError):
        return set()


def save_herd(near):
    """Write the creatures of this place, as the runner sees them now, into the wildlife file the dispatcher counts from."""
    if not isinstance(near, dict) or near.get('poi_id') not in (None, poi) or not isinstance(near.get('creatures'), list):
        return
    path = f'/srv/collective/data/wildlife/{system_id}.json'
    try:
        wild = json.load(open(path, encoding='utf-8'))
    except (OSError, ValueError):
        wild = {'system': system_id, 'pois': {}}
    if not isinstance(wild.get('pois'), dict):
        wild['pois'] = {}
    place = wild['pois'].setdefault(poi, {})
    place.update({'read_at': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), 'source': 'hunt runner, on leaving',
                  'creatures': [{k: c.get(k) for k in ('species', 'name', 'role', 'hull', 'max_hull', 'in_combat')} for c in near['creatures'] if isinstance(c, dict)],
                  'pirates': near.get('pirate_count') or 0, 'pilots': near.get('count') or 0})
    try:
        tmp = f'{path}.{os.getpid()}.tmp'
        with open(tmp, 'w', encoding='utf-8') as fh:
            json.dump(wild, fh, separators=(',', ':'))
        os.replace(tmp, path)
    except OSError as e:
        say(f'herd not written: {e}')


def in_battle():
    st = raw('status', group='spacemolt_battle')
    return bool(body(st).get('is_participant')), text(st)


def fight():
    """Drive the running battle to its end: close in, fire, flee in time. True when it ended."""
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
        cells = [c for c in (row.split('\t') for row in t.splitlines()) if len(c) > 9 and c[0] != 'player']
        kinds = [c[1] for c in cells]
        pct = lambda value: int(value.rstrip('%')) if value.rstrip('%').isdigit() else 100
        own = next((c for c in cells if c[0] == pilot), None)
        own_hull, own_shield = (pct(own[6]), pct(own[7])) if own else (100, 100)       # the battle's own figures: fresh every tick
        LOW[0] = min(LOW[0], own_hull)
        prey_hull = max([pct(c[6]) for c in cells if c[1] == 'creature'] or [0])
        if own_hull < 60 or (own_shield < 15 and prey_hull > 40):
            say(f'hull {own_hull}%, shield {own_shield}%, prey {prey_hull}%: fleeing')
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
HULL_BEFORE, OWN, notes = hull()[0], own_names(), []
GAME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ALONE_MODE = alone_mode(os.path.join(GAME, 'routes', route_id + '.json')) if ALONE and not STEP else 'strangers'
HOSTILE = hostile_names(os.path.join(GAME, 'players')) if ALONE_MODE == 'pirates' else set()
if ALONE:
    say('alone: leaves for ' + ('a pirate or a pilot of the hostile list (%d filed)' % len(HOSTILE) if ALONE_MODE == 'pirates' else 'every ship that is not ours'))
if not combat_mode('external'):
    sys.exit('the engine did not take the combat mode; no hunt')
kills, started, hunt_minutes = 0, time.time(), 0.0
if not STEP:
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
        h, m = hull()
        if h < m * 0.6:
            say(f'hull {h}/{m}: no further fight, to the station for repair')
            break
        if not reload_if_low():
            break
        if in_battle()[0]:
            say('already in a battle: taking it up')
        else:
            near = body(raw('get_nearby'))
            why = leave_reason(near, OWN, ALONE_MODE, HOSTILE) if ALONE else None
            if why:
                say(why[0] + ': no fight, leaving')
                notes.append(why[1])
                break
            prey = [c for c in near.get('creatures') or [] if isinstance(c, dict) and c.get('role') == 'grazer' and not c.get('in_combat')
                    and (species is None or c.get('species') in species) and (c.get('max_hull') or c.get('hull') or 0) <= max_prey_hull]
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
        if sum(now.values()) >= 60:
            break
    if not in_battle()[0]:
        kills += loot_own()                          # nothing of ours is left behind
        save_herd(body(raw('get_nearby')))           # the herd as we leave it: what the dispatcher counts for the next hunter
    hunt_minutes = (time.time() - arrived) / 60
combat_mode('flee')
goods = {k: v - before_cargo.get(k, 0) for k, v in cargo().items() if v - before_cargo.get(k, 0) > 0}
say(f'goods from this hunt: {goods}')
if STEP:
    print(f'STEP {pilot}: kills {kills} in {hunt_minutes:.0f} min at {poi} | goods {goods} | lowest hull {LOW[0]}% | {"; ".join(notes) or "no notes"}', flush=True)
    sys.exit(0)
sold = {}
if goal('prepare-at-station', {'systemId': sell_at[0], 'poiId': sell_at[1], 'baseId': sell_at[2], 'refuel': True}) and '--keep' not in args:
    items = [i for i in (body(raw('view_market', group='spacemolt_market')).get('items') or []) if isinstance(i, dict)]
    if items:
        rows = [{k: i.get(k) for k in ('item_id', 'item_name', 'category', 'best_buy', 'best_buy_qty', 'buy_quantity', 'best_sell', 'best_sell_qty', 'sell_quantity')} for i in items]
        tmp = f'{MARKET}{sell_at[2]}.json.{os.getpid()}.tmp'
        with open(tmp, 'w', encoding='utf-8') as fh:
            json.dump({'base': sell_at[2], 'system': sell_at[0], 'read_at': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
                       'source': 'view_market, own ship docked', 'items': rows}, fh, separators=(',', ':'))
        os.replace(tmp, f'{MARKET}{sell_at[2]}.json')
    book = {i.get('item_id'): i for i in items}
    KEPT = kept_goods(os.path.dirname(os.path.dirname(MARKET)), os.path.dirname(GAME))
    for item in sorted(set(cargo()) & set(KEPT)):
        say(f'{item}: kept for the reserve (surplus.py: no unit to spare): stored, not sold')
    for item, qty in saleable(cargo(), KEPT, AMMO).items():
        row = book.get(item) or {}
        bid = row.get('best_buy') or 0
        depth = row.get('best_buy_qty') if isinstance(row.get('best_buy_qty'), (int, float)) else (row.get('buy_quantity') or 0)   # at the best price: `buy_quantity` is the total of all levels
        if isinstance(bid, (int, float)) and bid >= min_bid and depth:
            n = min(qty, depth)
            c0 = credits()
            raw('sell', {'item_id': item, 'quantity': n})
            time.sleep(11)
            sold[item] = (n, bid, credits() - c0)
        elif item in goods:
            say(f'{item}: best bid here {bid} x {depth}: kept')
    wanted = wanted_goods(MARKET, min_bid, time.time()) - set(KEPT)   # goods a station bids for, read within the hour, stay aboard for the next sale; what the reserve keeps is stored
    stashed = {}
    for item, qty in cargo().items():                # the rest goes into storage here: the hold is free for the next hunt
        if item not in AMMO and item not in wanted:
            if 'error' not in raw('deposit', {'item_id': item, 'quantity': qty, 'target': 'self', 'source': 'cargo'}, group='spacemolt_storage'):
                stashed[item] = qty
            time.sleep(11)
    if stashed:
        say(f'stored at {sell_at[2]}: {stashed}')
after = credits()
if not (before_credits and after) and 'wallet not read' not in notes:      # a wallet is never 0: the engine did not answer at one end
    notes.append('wallet not read')
try:
    os.makedirs(os.path.dirname(RUNS), exist_ok=True)
    with open(RUNS, 'a', encoding='utf-8') as fh:
        fcntl.flock(fh, fcntl.LOCK_EX)
        fh.write(json.dumps({'route': route_id, 'kind': 'hunt', 'pilot': pilot, 'started': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(started)),
                             'minutes': round((time.time() - started) / 60, 1), 'credits_before': before_credits, 'credits_after': after,
                             'delta': after - before_credits if before_credits and after else 0, 'one_time': 0, 'kills': kills, 'goods': goods, 'sold': {k: list(v) for k, v in sold.items()},
                             'hull_before': HULL_BEFORE, 'hull_after': hull()[0], 'lowest_hull_pct': LOW[0], 'notes': notes}, separators=(',', ':')) + '\n')
except OSError as e:
    say(f'run row not written: {e}')
print(f'RESULT {pilot}: kills {kills} in {hunt_minutes:.0f} min at {poi} | goods {goods} | sold at {sell_at[2]} (units, bid, credits received) {sold} '
      f'| credits {before_credits} -> {after} ({after - before_credits:+d}) | whole trip {(time.time() - started) / 60:.0f} min | lowest hull {LOW[0]}%{" | " + "; ".join(notes) if notes else ""}', flush=True)

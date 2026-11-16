"""Fly one pilot along a route file: dock at each stop and do what the stop says.

Usage: python3 -I route_run.py <pilot> <route id | route file> [--from N] [--verbose]

A route is a JSON file of the repository's game/routes/ folder (game/routes/BLUEPRINT.md);
which pilot flies it, and where a pilot is, stays in the unit's data folder:
  {"id": "...", "kind": "missions | trade | ...", "note": "...",
   "one_time": ["Mission Title", ...],        rewards booked as seed money, not income
   "stops": [{"at": "system:poi:base",
              "only_if_active": ["Mission Title"],   skip the stop unless one of these is still open
              "skip_if_hold": {"item_id": N},        skip the stop when the hold has these already
              "redock": true,                 undock and dock again (a delivery counts on docking)
              "store":  ["item_id", ...],     hold -> personal storage here; "all": every good aboard
              "sell":   [{"item": "...", "min_price": N}],
              "buy":    [{"item": "...", "qty": N, "max_price": N, "one_time": true}],   max_price: the most a unit may cost, tax included
                                              qty = units wanted in the hold; one_time: goods for a
                                              one-time mission, their cost is booked against its reward
              "accept": ["template_id", {"template": "...", "needs": {"item_id": N}}],
                                              needs: accept only with these goods in the hold
              "mine":   [{"at": "system:poi", "for": ["Mission Title"], "minutes": 25}]}, ...]}
                                              after the station's work: mine at that place with the engine's
                                              mining loop until every named mission that is open has its
                                              objectives done (a mission that counts units mined), at most
                                              `minutes`; ore that fills the hold goes into storage at the stop
At every stop, in this order: dock and refuel; hand in every mission whose
objectives are all done; redock; hand in again; store; sell; buy; accept; save the
station's order book and mission board (data/market, data/missions).
--from N starts at stop N (1 is the first). A goal the engine is still carrying
out for the pilot is waited for, up to ten minutes. While the run lasts the pilot
carries an order file (data/fleet/orders/<pilot>.json) so the station shows it at
work between two goals. A stop that cannot be reached ends the run. One line per step, a RESULT line, and
one row in data/routes/runs.jsonl (route, pilot, minutes, credits before and
after, one-time rewards): `routes.py` turns the rows into credits per ship-hour."""
import atexit
import fcntl
import json
import os
import pathlib
import re
import subprocess
import sys
import time
import traceback
import urllib.error
import urllib.parse
import urllib.request

GATE = 'http://172.30.0.32:7580'
OPENER = urllib.request.build_opener(urllib.request.ProxyHandler({}))
DATA = pathlib.Path('/srv/collective/data')
ONETIME_FILE = str(DATA / 'fleet' / 'onetime.json')
FLOOR = 3000                                 # credits every pilot keeps (orders F7: the weekly tax)
pilot, route_arg = sys.argv[1], sys.argv[2]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import division                                   # noqa: E402  the division's lock: own ships only, never a pilot another program flies
division.require(pilot)
verbose = '--verbose' in sys.argv
route_path = pathlib.Path(route_arg) if route_arg.endswith('.json') else pathlib.Path(__file__).resolve().parent.parent / 'routes' / f'{route_arg}.json'
ROUTE = json.loads(route_path.read_text(encoding='utf-8'))
P = urllib.parse.quote(pilot, safe='')


TAX = 1.01                   # what a buy costs above its ask at our stations (1 percent, seen 2026-11-15); the wallet is read after every buy


def now():
    return time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())


ORDER = DATA / 'fleet' / 'orders' / f'{pilot}.json'


def order(what):
    """Tell the station what this pilot is doing; the file is removed when the run ends."""
    ORDER.parent.mkdir(parents=True, exist_ok=True)
    tmp = ORDER.with_name(f'{ORDER.name}.{os.getpid()}.tmp')
    tmp.write_text(json.dumps({'pilot': pilot, 'what': what, 'since': now()}), encoding='utf-8')
    os.replace(tmp, ORDER)


def order_done():
    try:
        ORDER.unlink()
    except OSError:
        pass


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


def free_from_battle():
    """A goal refused `in_battle`: set the battle stance flee and wait, three minutes at most, until the ship is out.
    The engine's combat mode flee leaves the battle stance as it was: after the restart of 2026-11-16 02:00 UTC a drone
    sat 65 minutes in a fight at stance fire while 42 runs failed at their first stop (requests ENT-090)."""
    raw('stance', {'stance': 'flee'}, 'spacemolt_battle')
    for _ in range(18):
        time.sleep(10)
        if not body(raw('status', group='spacemolt_battle')).get('is_participant'):
            say('out of the battle after the stance flee')
            return True
    say('still in a battle three minutes after the stance flee')
    return False


def goal(kind, options, tries=3):
    d, waited = {}, 0
    while tries > 0:
        status, d = call('POST', f'/accounts/{P}/goal', {'type': kind, 'options': options})
        if status == 200 and d.get('success'):
            return True, str(d.get('message') or '')
        if 'already executing' in str(d.get('error')) and waited < 60:      # an earlier goal is still running: wait for it
            waited += 1
            time.sleep(10)
            continue
        if 'in_battle' in str(d.get('message') or d.get('error') or '').lower().replace(' ', '_'):
            free_from_battle()                                               # then the next try
        tries -= 1
        time.sleep(15)
    return False, str(d.get('message') or d.get('error') or '')


def step_said(answer):
    """The hunt step's own last word, for the run row (requests ENT-092): its STEP line without the pilot's name, else
    its last line. Without it a hunt that ended with no kill left only `objectives not done`, and the pilot's log is
    overwritten by its next run."""
    lines = [line.strip() for line in str(answer).splitlines() if line.strip()]
    for line in reversed(lines):
        if line.startswith('STEP '):
            return (line.split(': ', 1)[1] if ': ' in line else line)[:200]
    return lines[-1][:200] if lines else 'no output'


def where_now():
    """system:poi of the pilot as the fleet collector last wrote it (data/fleet/ships/, at most a few seconds old)."""
    try:
        ship = json.loads((DATA / 'fleet' / 'ships' / ((re.sub(r'[^A-Za-z0-9_.-]', '_', P)[:60] or 'pilot') + '.json')).read_text(encoding='utf-8'))
        return '%s:%s' % (ship.get('system') or '?', ship.get('poi') or 'in transit')
    except (OSError, ValueError):
        return 'not read'


def raw(action, params=None, group='spacemolt'):
    _, d = call('POST', f'/accounts/{P}/raw', {'toolGroup': group, 'action': action, 'params': params or {}}, timeout=120)
    return d if isinstance(d, dict) else {}


def body(d):
    sc = d.get('structuredContent')
    return sc if isinstance(sc, dict) else {}


def text(d):
    return d.get('result') if isinstance(d.get('result'), str) else json.dumps(d)[:600]


def credits():
    return int(((call('GET', f'/accounts/{P}')[1].get('state') or {}).get('credits')) or 0)


def offer(book, item, limit, units):
    """(the best ask of the book just read, the units to buy): only what stands at the limit or under it with the
    buyer's tax, and no more than stands at that ask. (ask, 0): buy nothing."""
    row = book.get(item) or {}
    ask = row.get('best_sell') or 0
    if not isinstance(ask, (int, float)) or ask <= 0 or ask * TAX > limit:
        return ask, 0
    there = row.get('best_sell_qty')
    return ask, min(units, int(there)) if isinstance(there, (int, float)) and there > 0 else units


def cargo():
    rows = call('GET', f'/accounts/{P}/state/cargo')[1]
    return {r.get('item_id'): int(r.get('quantity') or 0) for r in rows if isinstance(r, dict)} if isinstance(rows, list) else {}


def store_list(want, hold):
    """The goods a stop's `store` moves from the hold into storage: the named ones that are aboard, or with `store: "all"`
    every good aboard. The once routes of First Hunt and First Steps left loot and ore aboard, and a few units closed every
    route with `requires.empty_hold` to the pilot (requests.log ENT-120, 2026-11-16)."""
    if want == 'all':
        return [item for item, n in hold.items() if n]
    return [item for item in (want or []) if hold.get(item)]


def book_onetime(title, amount):
    with open(ONETIME_FILE + '.lock', 'w') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        try:
            rows = json.load(open(ONETIME_FILE, encoding='utf-8'))
        except (OSError, ValueError):
            rows = []
        rows.append([int(time.time()), pilot, title, amount])
        tmp = f'{ONETIME_FILE}.{os.getpid()}.tmp'
        with open(tmp, 'w', encoding='utf-8') as fh:
            json.dump(rows[-5000:], fh, separators=(',', ':'))
        os.replace(tmp, ONETIME_FILE)


def active():
    """[(title, 32-hex id, all objectives done)] of the pilot's accepted missions."""
    t = text(raw('get_active_missions'))
    if verbose:
        say('active missions, raw: ' + t[:1500].replace('\n', ' / '))
    out = []
    for m in re.finditer(r'--- (.+?) \[([0-9a-f]{32})\](.*?)(?=\n--- |\Z)', t, re.S):
        objectives = re.search(r'Objectives:\n(.*?)(?:\nRewards:|\Z)', m.group(3), re.S)
        lines = [l for l in (objectives.group(1).splitlines() if objectives else []) if l.strip().startswith('- ')]   # not the Target lines
        out.append((m.group(1).strip(), m.group(2), bool(lines) and all('[DONE]' in l for l in lines)))
    return out


def hand_in(done, onetime):
    for title, mid, finished in active():
        if not finished:
            continue
        ok, msg = goal('complete-mission', {'missionId': mid}, tries=1)
        paid = re.search(r'\+([\d,]+) credits', msg)
        amount = int(paid.group(1).replace(',', '')) if paid else 0
        say(f'hand in {title}: {ok} {msg[:110]}')
        if ok:
            done.append([title, amount])
            if title in (ROUTE.get('one_time') or []) and amount:
                book_onetime(title, amount)
                onetime[0] += amount


def save_station(base, system):
    items = [i for i in body(raw('view_market', group='spacemolt_market')).get('items') or [] if isinstance(i, dict)]
    if items:
        rows = [{k: i.get(k) for k in ('item_id', 'item_name', 'category', 'best_buy', 'best_buy_qty', 'buy_quantity', 'best_sell', 'best_sell_qty', 'sell_quantity')} for i in items]
        write_json(DATA / 'market' / f'{base}.json', {'base': base, 'system': system, 'read_at': now(), 'source': 'view_market, own ship docked', 'items': rows})
    board = [m for m in body(raw('get_missions')).get('missions') or [] if isinstance(m, dict)]
    if board:
        keep = [{k: m.get(k) for k in ('template_id', 'mission_id', 'title', 'type', 'difficulty', 'rewards', 'objectives', 'expires_in_ticks', 'giver')} for m in board]
        write_json(DATA / 'missions' / f'{base}.json', {'base': base, 'system': system, 'read_at': now(), 'source': 'get_missions, own ship docked', 'missions': keep})
    return {i.get('item_id'): i for i in items}, board


started, before = time.time(), credits()
done, onetime, notes, reached = [], [0], [], 0
first = int(sys.argv[sys.argv.index('--from') + 1]) - 1 if '--from' in sys.argv else 0
order('circuit ' + ROUTE['id'])
atexit.register(order_done)
CRASH, FINISHED = [], []


def crashed(kind, error, trace):
    """An exception that ends the run is kept for the run's row, then printed as Python prints it."""
    line = traceback.extract_tb(trace)[-1].lineno if trace else 0
    CRASH.append(f'crashed: {kind.__name__}: {" ".join(str(error).split())[:120]} (line {line})')
    sys.__excepthook__(kind, error, trace)


def finish():
    """The run's row in data/routes/runs.jsonl and its RESULT line, written once: after the last stop, or on the way out
    of a run that an exception ended. A run without a row is invisible to the record and to the loss stop."""
    if FINISHED:
        return
    FINISHED.append(True)
    notes.extend(CRASH)
    try:
        after = credits()
    except Exception:                                 # the engine is away on the way out: the row is written all the same
        after = 0
    if not (before and after) and 'wallet not read' not in notes:      # a wallet is never 0: the engine did not answer at one end
        notes.append('wallet not read')
    minutes = (time.time() - started) / 60
    row = {'route': ROUTE['id'], 'kind': ROUTE.get('kind'), 'pilot': pilot, 'started': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(started)),
           'minutes': round(minutes, 1), 'stops': reached, 'of': len(ROUTE['stops']), 'credits_before': before, 'credits_after': after,
           'delta': after - before if before and after else 0, 'one_time': onetime[0], 'handed_in': done, 'notes': notes}
    runs = DATA / 'routes' / 'runs.jsonl'
    runs.parent.mkdir(parents=True, exist_ok=True)
    with open(runs, 'a', encoding='utf-8') as fh:
        fcntl.flock(fh, fcntl.LOCK_EX)
        fh.write(json.dumps(row, separators=(',', ':')) + '\n')
    print(f'RESULT {pilot}: route {ROUTE["id"]}: {reached}/{len(ROUTE["stops"])} stops in {minutes:.0f} min | handed in {done} | credits {before} -> {after} '
          f'({after - before:+d}; one-time {onetime[0]}) | {"; ".join(notes) or "no notes"}', flush=True)


sys.excepthook = crashed
atexit.register(finish)                              # after order_done, so it runs before it: the row first, then the order file goes
for n, stop in enumerate(ROUTE['stops']):
    system, poi, base = stop['at'].split(':')
    if n < first:
        reached += 1
        continue
    hold = cargo()
    if stop.get('skip_if_hold') and all(hold.get(i, 0) >= q for i, q in stop['skip_if_hold'].items()):
        reached += 1
        continue
    if stop.get('only_if_active') and not ({title for title, _mid, _fin in active()} & set(stop['only_if_active'])):
        reached += 1
        continue
    ok, msg = goal('prepare-at-station', {'systemId': system, 'poiId': poi, 'baseId': base, 'refuel': True})
    if not ok:
        say(f'stop {n + 1} {base}: not reached: {msg[:120]}')
        notes.append(f'stop {n + 1} not reached')
        break
    reached += 1
    hand_in(done, onetime)
    if stop.get('redock'):
        raw('undock')
        time.sleep(11)
        raw('dock')
        time.sleep(11)
        hand_in(done, onetime)
    hold = cargo()
    for item in store_list(stop.get('store'), hold):
        if hold.get(item):
            d = raw('deposit', {'item_id': item, 'quantity': hold[item], 'target': 'self', 'source': 'cargo'}, group='spacemolt_storage')
            if 'error' in d:
                say(f'store {item}: {str(d.get("error"))[:100]}')
            time.sleep(11)
    book, board = save_station(base, system)
    for want in stop.get('sell') or []:
        row, have = book.get(want['item']) or {}, cargo().get(want['item'], 0)
        bid = row.get('best_buy') or 0
        depth = row.get('best_buy_qty') if isinstance(row.get('best_buy_qty'), (int, float)) else (row.get('buy_quantity') or 0)   # at the best price: `buy_quantity` is the total of all levels
        if have and isinstance(bid, (int, float)) and bid >= want['min_price'] and depth:
            c0 = credits()
            units = have if want.get('all') else min(have, depth)   # `all`: down the bid's levels too (a mission that counts units sold)
            raw('sell', {'item_id': want['item'], 'quantity': units})
            time.sleep(11)
            say(f'sold {units} {want["item"]} into a bid of {bid}: {credits() - c0:+d} cr')
        elif have:
            say(f'{want["item"]}: bid {bid} x {depth} is under {want["min_price"]}: kept')
    for want in stop.get('buy') or []:
        need = want['qty'] - cargo().get(want['item'], 0)
        if need > 0 and credits() - need * want['max_price'] * 1.01 < FLOOR:
            say(f'buy {need} {want["item"]}: not bought, the wallet would fall under {FLOOR} cr')
            notes.append(f'{want["item"]}: wallet floor')
        elif need > 0:
            ask, units = offer(book, want['item'], want['max_price'], need)
            if not units:                                # nothing stands at the limit or under it, tax included: nothing is bought
                say(f'buy {need} {want["item"]}: not bought, the best ask is {ask or "none"} and the limit is {want["max_price"]} with tax')
                notes.append(f'{want["item"]}: not bought')
                continue
            c0, had = credits(), cargo().get(want['item'], 0)
            ok, msg = goal('buy-items', {'items': [{'itemId': want['item'], 'maxPrice': ask, 'maxQuantity': units}]}, tries=1)
            got = cargo().get(want['item'], 0)
            say(f'buy {units} {want["item"]} at the ask of {ask} (limit {want["max_price"]} with tax): {ok}, now {got} in the hold, {credits() - c0:+d} cr {"" if ok else msg[:100]}')
            spent = credits() - c0
            if got > had and -spent > (got - had) * want['max_price']:
                notes.append(f'{want["item"]}: paid {-spent} for {got - had}, above the limit of {want["max_price"]} each')
            if want.get('one_time') and spent < 0:
                book_onetime(f'{ROUTE["id"]}: {want["item"]} bought', spent)
                onetime[0] += spent
            if got < want['qty']:
                notes.append(f'{want["item"]}: {got} of {want["qty"]}')
    for want in stop.get('fit') or []:                   # a module bought here and fitted, one of its kind
        try:
            live = json.load(open(DATA / 'fleet' / 'ships' / ((re.sub(r'[^A-Za-z0-9_.-]', '_', pilot)[:60] or 'pilot') + '.json'), encoding='utf-8'))
            fitted = [m.get('type') for m in live.get('modules') or [] if isinstance(m, dict)]
        except (OSError, ValueError):
            fitted = []
        if want['module'] in fitted:
            say(f'fit {want["module"]}: fitted already')
            continue
        if not cargo().get(want['module']):
            if credits() - want['max_price'] * 1.01 < FLOOR:
                say(f'fit {want["module"]}: not bought, the wallet would fall under {FLOOR} cr')
                notes.append(f'{want["module"]}: wallet floor')
                continue
            ask, units = offer(book, want['module'], want['max_price'], 1)
            if not units:                                # nothing stands at the limit or under it, tax included: nothing is bought
                say(f'fit {want["module"]}: not bought, the best ask is {ask or "none"} and the limit is {want["max_price"]} with tax')
                notes.append(f'{want["module"]}: not bought')
                continue
            c0 = credits()
            ok, msg = goal('buy-items', {'items': [{'itemId': want['module'], 'maxPrice': ask, 'maxQuantity': 1}]}, tries=1)
            paid = c0 - credits()
            say(f'buy {want["module"]} at the ask of {ask} (limit {want["max_price"]} with tax): {ok}, {-paid:+d} cr {"" if ok else msg[:100]}')
            if paid > want['max_price']:
                notes.append(f'{want["module"]}: paid {paid}, above the limit of {want["max_price"]}')
            if paid > 0:                                 # a tool is bought once: kept out of the steady costs, like a mission's goods
                book_onetime(f'{ROUTE["id"]}: {want["module"]} bought (tool)', -paid)
                onetime[0] -= paid
        if not cargo().get(want['module']):
            notes.append(f'{want["module"]}: not bought')
            continue
        d = raw('install_mod', {'module_id': want['module']})
        time.sleep(11)
        answer = text(d)[:140].replace('\n', ' / ')
        say(f'fit {want["module"]}: {answer}')
        if cargo().get(want['module']):                  # still in the hold: the fitting did not take it
            notes.append(f'{want["module"]}: not fitted')
    if stop.get('accept'):
        have = {title for title, _mid, _fin in active()}
        for entry in stop['accept']:
            template, needs = (entry, {}) if isinstance(entry, str) else (entry['template'], entry.get('needs') or {})
            hold = cargo()
            short = {i: n for i, n in needs.items() if hold.get(i, 0) < n}
            if short:
                say(f'{template}: not accepted, the hold lacks {short}')
                notes.append(f'{template}: goods missing')
                continue
            posted = next((m for m in board if m.get('template_id') == template), None)   # never `offer`: that is the function the buy and fit steps call
            if posted is None:
                say(f'{template}: not on the board of {base}')
                notes.append(f'{template} not offered')
            elif posted.get('title') in have:
                say(f'{template}: already accepted')
            else:
                ok, msg = goal('accept-mission', {'missionId': template}, tries=1)
                say(f'accept {template}: {ok} {msg[:100]}')
                if not ok:
                    notes.append(f'{template} not accepted')
    for step in stop.get('mine') or []:
        wanted = set(step.get('for') or [])
        left = {title for title, _mid, finished in active() if not finished} & wanted
        if not left:
            say(f'mine at {step["at"]}: none of {sorted(wanted)} is open; skipped')
            continue
        mine_system, mine_poi = step['at'].split(':')
        status, answer = 0, {}
        for _ in range(12):                              # the goal of the step before may still be running
            status, answer = call('POST', f'/accounts/{P}/loop', {'type': 'mining', 'options': {
                'miningSystemId': mine_system, 'beltPoiId': mine_poi, 'sellSystemId': system, 'sellStationPoiId': poi, 'sellBaseId': base,
                'skipMarket': True, 'depositTarget': 'personal', 'retryOnDepleted': True}})
            if status in (200, 201) and 'error' not in answer:
                break
            time.sleep(15)
        if status not in (200, 201) or 'error' in answer:
            say(f'mine at {mine_poi}: the loop did not start: {status} {str(answer.get("error"))[:100]}')
            notes.append(f'mine {mine_poi}: loop not started')
            continue
        until = time.time() + float(step.get('minutes', 25)) * 60
        while left and time.time() < until and not (DATA / 'fleet' / 'STOP').exists():
            time.sleep(30)
            try:
                os.utime(ORDER)
            except OSError:
                pass
            left = {title for title, _mid, finished in active() if not finished} & wanted
            if left and not call('GET', f'/accounts/{P}/loop')[1].get('running'):
                notes.append(f'mine {mine_poi}: the loop ended by itself')
                break
        call('DELETE', f'/accounts/{P}/loop')
        for _ in range(40):                              # let the step in flight end
            if not call('GET', f'/accounts/{P}')[1].get('hasExecutingGoal'):
                break
            time.sleep(15)
        say(f'mined at {mine_poi}: ' + ('objectives done' if not left else f'stopped, still open: {sorted(left)}'))
        if left:
            notes.append(f'mine {mine_poi}: objectives not done')
    for step in stop.get('hunt') or []:                  # a hunt for a mission: hunt.py as a step, with its rules
        wanted = set(step.get('for') or [])
        left = {title for title, _mid, finished in active() if not finished} & wanted
        if wanted and not left:
            say(f'hunt at {step["at"]}: none of {sorted(wanted)} is open; skipped')
            continue
        hunt_system, hunt_poi = step['at'].split(':')
        command = [sys.executable, '-I', '-B', str(pathlib.Path(__file__).with_name('hunt.py')), pilot, hunt_system, hunt_poi, '--step',
                   '--kills', str(step.get('kills', 3)), '--minutes', str(step.get('minutes', 30)), '--route', ROUTE['id']]
        command += ['--species', ','.join(step['species'])] if step.get('species') else []
        command += ['--alone'] if step.get('alone') else []
        for _ in range(2):                               # a grazer that fled keeps its damage: a second go ends it
            try:
                answer = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
                                        env=dict(os.environ, FLEET_HOLD='circuit ' + ROUTE['id']),   # the run's own order: hunt.py may fly
                                        timeout=(float(step.get('minutes', 30)) + 25) * 60).stdout or ''
            except subprocess.TimeoutExpired as error:
                answer = str(error.stdout or '') + '\nthe hunt step did not end in time'
            print(answer.rstrip(), flush=True)
            said = step_said(answer)
            left = {title for title, _mid, finished in active() if not finished} & wanted
            if not left or 'left: a ship' in answer or (DATA / 'fleet' / 'STOP').exists():
                break
        say(f'hunt at {hunt_poi}: ' + ('objectives done' if not left else f'stopped, still open: {sorted(left)}'))
        if left:
            notes.append(f'hunt {hunt_poi}: objectives not done; the step said: {said}; the ship stood at {where_now()}')
    if verbose:
        active()
finish()

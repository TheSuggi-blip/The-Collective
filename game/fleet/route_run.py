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
              "gift":   {"to": "trader", "items": "all", "source": "storage", "keep": {"item_id": N}},   (or a list of them)
                                              after `store`, before `store_faction`: the goods given into the storage of
                                              another pilot of ours here (handover.py; `to` a role named in
                                              data/fleet/receivers.json, or a pilot of ours), read back from the
                                              giver's storage and hold; a refused gift leaves them with the giver. Only
                                              with data/fleet/strict-classes-on; off, nothing is given
              "store_faction": ["item_id", ...],   hold -> the faction's storage here, after `store`; "all" as above
              "refuel": false,                dock without the station's fuel (default true: dock and refuel)
              "burn_cells": true,             the fuel cells aboard into the tank, as many whole cells as it has room for
              "bunker": {"keep": N},          an outpost of ours: the cells aboard burnt into the tank and the tank above
                                              N deposited into the faction's fuel reserve here, until no cell is left
              "withdraw": [{"item": "...", "qty": N}],   personal storage here -> hold, at most qty and the free
                                              hold; when the stop sells the item too, at most what its bid takes;
                                              with "from": "faction" (and "keep": N) the faction's storage here
                                              -> hold, leaving N there: needs a faction role with manage_treasury
              "sell":   [{"item": "...", "min_price": N}],
              "buy":    [{"item": "...", "qty": N, "max_price": N, "one_time": true}],   max_price: the most a unit may cost, tax included
                                              qty = units wanted in the hold; one_time: goods for a
                                              one-time mission, their cost is booked against its reward
              "stop_on_failed_buy": true,     a buy entry of this stop that gets nothing (no ask at its limit, the
                                              wallet floor, a buy that took nothing) ends the run here: no later step
                                              or stop, the goods stay where they are, the RESULT line says why (Q75)
              "craft":  [{"recipe": "...", "runs": N, "makes": "item_id", "per_run": M, "inputs": ["item_id", ...]}],
                                              after the buy, at the station's workshop: the `inputs` aboard go into
                                              storage, a quote, then `runs` runs (per_run units each, default 1) made
                                              into storage and counted there; what was made comes into the hold and
                                              the stop's `sell` runs once more for it. No inputs, a fee that would take
                                              the wallet under FLOOR, or no `makes`: nothing is made, the run goes on
              "sell_order": [{"item": "...", "qty": N, "price": N, "floor": N}],
                                              after the craft: one resting sell order of the good here (spacemolt_market,
                                              rule F39), kept at `price` (never under `floor` or under the best bid, which
                                              an ask under it would fill at once): an own order at another price is
                                              repriced (modify_order), and what the pilot holds here (hold, then storage)
                                              is listed up to `qty` units in all (create_sell_order). Fills come later, at
                                              the station, outside the run's credits
              "unfit":  ["module_id", ...],   before `fit`: strips every fitted copy of each named off-role module
                                              and deposits it in station storage so slots, CPU and power open up
              "fit":    [{"module": "...", "max_price": N, "count": 2, "replace": "..."}],
                                              after `unfit`: buys and fits up to `count` copies (default 1; max_price
                                              with tax, booked as a tool bought once); `replace` swaps an old module out
              "accept": ["template_id", {"template": "...", "needs": {"item_id": N}}],
                                              needs: accept only with these goods in the hold;
                                              {"title": "..."} instead of template: the first posted
                                              copy of that title (a station's procurement missions
                                              carry no template and a new mission_id each)
              "mine":   [{"at": "system:poi", "for": ["Mission Title"], "minutes": 25}]}, ...]}
                                              after the station's work: mine at that place with the engine's
                                              mining loop until every named mission that is open has its
                                              objectives done (a mission that counts units mined), at most
                                              `minutes`; ore that fills the hold goes into storage at the stop
At every stop, in this order: dock and refuel; hand in every mission whose
objectives are all done; redock; hand in again; store; store_faction; burn_cells; bunker; withdraw; sell; buy; craft (then sell what
it made); sell_order; accept; save the station's order book and mission board (data/market, data/missions).
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
import mobile                                     # noqa: E402  a stop at a moving station goes where the station stands now (queue.log ENT-246)
division.require(pilot)
verbose = '--verbose' in sys.argv
route_path = pathlib.Path(route_arg) if route_arg.endswith('.json') else pathlib.Path(__file__).resolve().parent.parent / 'routes' / f'{route_arg}.json'
ROUTE = json.loads(route_path.read_text(encoding='utf-8'))
P = urllib.parse.quote(pilot, safe='')


TAX = 1.01                   # what a buy costs above its ask at our stations (1 percent, seen 2026-11-15); the wallet is read after every buy
FIT_REPLACE = True           # requests ENT-290: a `fit` entry with `replace` swaps the module; False: such an entry buys and fits nothing


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


def pure_visit_tail(stops):
    """True when every remaining stop only visits/redocks (no buy/sell/craft/give/fit/mine/hunt/store/accept)."""
    work_keys = {'buy', 'sell', 'sell_all', 'craft', 'give', 'gift', 'fit', 'mine', 'hunt', 'withdraw', 'deposit', 'store', 'accept'}
    return bool(stops) and all(isinstance(s, dict) and not (set(s.keys()) & work_keys) for s in stops)


def posted_mission(board, template, title=None):
    """The mission of the board an `accept` entry names: by template_id or mission_id, or, given a title, the first
    copy posted under that title (Shipyard Supply and the other procurements: no template, a new mission_id each)."""
    if title:
        return next((m for m in board if m.get('title') == title), None)
    return next((m for m in board if m.get('template_id') == template or m.get('mission_id') == template), None)


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


def store_list(want, hold, keep=()):
    """The goods a stop's `store` moves from the hold into storage: the named ones that are aboard, or with `store: "all"`
    every good aboard but `keep` (the ammunition of a fitted weapon: aboard_ammo). The once routes of First Hunt and First
    Steps left loot and ore aboard, and a few units closed every route with `requires.empty_hold` to the pilot (requests.log
    ENT-120, 2026-11-16); a give route's `store: "all"` stored a cannon ship's plasma packs (requests.log ENT-352)."""
    if want == 'all':
        return [item for item, n in hold.items() if n and item not in keep]
    return [item for item in (want or []) if hold.get(item)]


def aboard_ammo(hold):
    """The ammunition aboard that a fitted weapon fires: kept aboard by `store: "all"`, as hunt.py keeps it (requests
    ENT-345, ENT-352). No ammunition aboard: no call. The rule: handover.fitted_ammo."""
    import handover
    ids = handover.ammo(str(DATA)) & {item for item, n in hold.items() if n}
    if not ids:
        return set()
    return handover.fitted_ammo(body(raw('get_ship')).get('modules') or [], handover.catalog_items(str(DATA / 'catalog'))) & ids


def deposit(item, units, target='self'):
    """Hold -> the pilot's own storage at the station where it is docked: the call of a stop's `store`, and of a craft's
    `inputs` (the workshop takes its inputs from that storage, guidebook logistics.md section 7). With target 'faction':
    hold -> the faction's storage there, the call of a stop's `store_faction` (our outpost takes goods only so)."""
    d = raw('deposit', {'item_id': item, 'quantity': units, 'target': target, 'source': 'cargo'}, group='spacemolt_storage')
    if 'error' in d:
        say(f'store {item}: {str(d.get("error"))[:100]}')
    time.sleep(11)


CELL = 20                    # fuel one fuel cell gives the tank (catalog; a cell burnt at 91 of 95 filled the tank and was gone, 2026-11-17)


def tank():
    """(fuel, max_fuel) of the ship now, as the engine reports it (GET /accounts/<pilot>: state.ship)."""
    ship = (call('GET', f'/accounts/{P}')[1].get('state') or {}).get('ship') or {}
    return int(ship.get('fuel') or 0), int(ship.get('max_fuel') or 0)


def burn_cells():
    """A stop's `burn_cells`, and the first half of `bunker`: the fuel cells aboard into the tank, as many whole cells as
    its room takes, in one `refuel` call (item_id fuel_cell, `quantity` cells: the game's help of refuel). A cell burnt
    into less room than 20 loses the rest (2026-11-17 20:27 UTC), so never more cells than room // 20. Returns cells burnt."""
    cells = cargo().get('fuel_cell', 0)
    fuel, top = tank()
    n = min(cells, max(top - fuel, 0) // CELL)
    if n <= 0:
        return 0
    raw('refuel', {'item_id': 'fuel_cell', 'quantity': n})
    time.sleep(TICK)
    burnt = cells - cargo().get('fuel_cell', 0)
    say(f'burnt {burnt} fuel cells: tank {fuel} -> {tank()[0]} of {top}')
    return burnt


def bunker(keep):
    """A stop's `bunker` at an outpost of ours: the cells aboard go into the tank (burn_cells) and the tank above `keep`
    into the faction's fuel reserve here (`deposit` item_id fuel, target faction: the bunker takes fuel only from a tank,
    cells stored there stay items), turn by turn until no cell is left; a deposit the game refuses ends it. Keep `keep`
    under the tank's room for a cell (max_fuel - 20) and enough for the way to the next station. 1,292 fuel from 64 cells
    by outpost.py of the skill logistics-stock, 2026-11-17. Returns (fuel deposited, cells burnt, refused)."""
    moved = burnt = 0
    for _ in range(200):
        b = burn_cells()
        burnt += b
        fuel, _top = tank()
        if fuel <= keep:
            if b:
                continue
            break
        deposit('fuel', fuel - keep, 'faction')
        after = tank()[0]
        if after >= fuel:
            say(f'bunker: the deposit of {fuel - keep} fuel was refused')
            return moved, burnt, True
        moved += fuel - after
        if not cargo().get('fuel_cell'):
            break
    return moved, burnt, False


def withdraw_units(want, stored, free, sell, row, aboard, size=1):
    """Units a stop's `withdraw` takes from the pilot's own storage into the hold: at most what is stored, what the free
    hold takes at the item's `size` (plasma gas takes two units of space a piece: 33 asked into a free hold of 65 were
    refused, 2026-11-16) and the want's `qty`. When the same stop sells the item, at most what the bid takes at its best price
    less what is aboard already, and nothing under the sale's `min_price`: nothing withdrawn stays in the hold to close
    the pilot's `empty_hold` routes. Storage is personal (requests.log ENT-117, 2026-11-16)."""
    units = min(int(stored or 0), max(int(free or 0), 0) // max(int(size or 1), 1), int(want.get('qty') or 10 ** 9))
    if sell is not None:
        bid = row.get('best_buy') or 0
        depth = row.get('best_buy_qty') if isinstance(row.get('best_buy_qty'), (int, float)) else 0
        if not isinstance(bid, (int, float)) or bid < sell['min_price']:
            return 0
        units = min(units, int(depth or 0) - int(aboard or 0))
    return max(units, 0)


def faction_withdraw_units(want, held, free, size=1):
    """Units a `withdraw` entry with "from": "faction" takes from the faction's storage here into the hold: at most what
    the faction holds above the entry's `keep` (default 0), what the free hold takes at the item's `size` and its `qty`.
    Only a pilot whose faction role carries manage_treasury may (game/rules/09-factions.md, row Treasury, storage)."""
    above = int(held or 0) - int(want.get('keep') or 0)
    units = min(above, max(int(free or 0), 0) // max(int(size or 1), 1), int(want.get('qty') or 10 ** 9))
    return max(units, 0)


def faction_stored(base):
    """{item_id: units} of the faction's storage at the station or outpost where the pilot is docked."""
    d = raw('view', {'target': 'faction', 'station_id': base}, group='spacemolt_storage')
    sc = body(d) or (body(d['result']) if isinstance(d.get('result'), dict) else {})
    items = sc.get('items') or []
    for i in items or []:
        if isinstance(i, dict) and i.get('item_id') and i.get('size'):
            SIZES[i['item_id']] = int(i.get('size') or 1)
    return {i.get('item_id'): int(i.get('quantity') or 0) for i in items or [] if isinstance(i, dict) and i.get('item_id')}


SIZES = {}                   # item -> units of hold space a piece, as the storage view names it (`size`)


def stored(base):
    """{item_id: units} of the pilot's own storage at the station where it is docked; each item's `size` goes to SIZES."""
    d = raw('view', {'station_id': base}, group='spacemolt_storage')
    sc = body(d) or (body(d['result']) if isinstance(d.get('result'), dict) else {})
    items = sc.get('items') or []
    for i in items or []:
        if isinstance(i, dict) and i.get('item_id'):
            SIZES[i['item_id']] = int(i.get('size') or 1)
    return {i.get('item_id'): int(i.get('quantity') or 0) for i in items or [] if isinstance(i, dict) and i.get('item_id')}


def free_space(capacity, rows):
    """Free space of a hold of `capacity`: each row of state/cargo takes its quantity times its `size` (tungsten and lead
    ore take 2; the game refused a withdraw counted in item units, 2026-11-16). Rows not read: no room."""
    if not isinstance(rows, list):
        return 0
    return capacity - sum(int(r.get('quantity') or 0) * int(r.get('size') or 1) for r in rows if isinstance(r, dict))


def room():
    """Free space of the hold now: the ship's capacity (its live file) less the space of what is aboard."""
    try:
        ship = json.loads((DATA / 'fleet' / 'ships' / ((re.sub(r'[^A-Za-z0-9_.-]', '_', P)[:60] or 'pilot') + '.json')).read_text(encoding='utf-8'))
        capacity = int(ship.get('cargo_capacity') or 65)
    except (OSError, ValueError):
        capacity = 65
    return free_space(capacity, call('GET', f'/accounts/{P}/state/cargo')[1])


def sell_into_bid(want, book):
    """A stop's `sell` entry: the units aboard into the bid of `book`, at `min_price` or more and no more than stand at
    its best price (`all`: down its levels too). Run for every sale of the stop, and once more for what its craft made."""
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


def sell_order_moves(want, row, mine, have):
    """The calls a stop's `sell_order` entry makes for one good: [("modify", order_id, price) | ("create", units,
    price)]. Supports optional dynamic rival undercutting (`undercut_pct` e.g. 0.05 and/or `undercut_cr`) against the
    live competing `best_sell` ask, while NEVER listing below `floor` or `best_buy` (rule F12/F39/F40)."""
    bid = row.get('best_buy') if isinstance(row.get('best_buy'), (int, float)) else 0
    ask = row.get('best_sell') if isinstance(row.get('best_sell'), (int, float)) else 0
    target = int(want['price'])
    u_pct = float(want.get('undercut_pct') or 0.0)
    u_cr = int(want.get('undercut_cr') or 0)
    if ask > 0 and (u_pct > 0.0 or u_cr > 0):
        undercut_p = int(round(ask * max(0.5, 1.0 - min(0.5, u_pct)))) - max(0, u_cr)
        if undercut_p < ask:
            target = min(target, undercut_p) if target > 0 else undercut_p
    price = max(target, int(want.get('floor') or 0), int(bid or 0))
    moves = [('modify', o['order_id'], price) for o in mine if int(o.get('price_each') or 0) != price]
    listed = sum(int(o.get('remaining') or 0) for o in mine)
    more = min(int(want['qty']) - listed, int(have or 0))
    if more > 0:
        moves.append(('create', more, price))
    return moves


def buy_order_moves(want, row, mine, cash_avail):
    """The calls a stop's `buy_order` entry makes for one good: [("modify", order_id, price) | ("create", units, price)].
    Places a standing wholesale buy wall at `price` (optional `outbid_pct`/`outbid_cr` above competing `best_buy`),
    strictly <= `ceiling` and strictly < `best_sell` (so it rests as a standing bid without overpaying at ask),
    sized to remaining `qty` and `cash_avail` (wallet above FLOOR)."""
    bid = row.get('best_buy') if isinstance(row.get('best_buy'), (int, float)) else 0
    ask = row.get('best_sell') if isinstance(row.get('best_sell'), (int, float)) else 0
    ceiling = int(want.get('ceiling') or want['price'])
    target = int(want['price'])
    o_pct = float(want.get('outbid_pct') or 0.0)
    o_cr = int(want.get('outbid_cr') or 0)
    if bid > 0 and (o_pct > 0.0 or o_cr > 0):
        step_p = int(round(bid * (1.0 + min(0.5, o_pct)))) + max(0, o_cr)
        target = max(target, step_p)
    price = min(target, ceiling)
    if ask > 1 and price >= int(ask):
        price = int(ask) - 1
    if price < 1:
        return []
    moves = [('modify', o['order_id'], price) for o in mine if int(o.get('price_each') or 0) != price]
    listed = sum(int(o.get('remaining') or 0) for o in mine)
    need_qty = max(0, int(want['qty']) - listed)
    afford = int(max(0, cash_avail) // price) if price > 0 else 0
    more = min(need_qty, afford)
    if more > 0:
        moves.append(('create', more, price))
    return moves


def own_buy_orders(item):
    """[{order_id, remaining, price_each}] of the pilot's own buy orders of `item` at the station where it is docked."""
    rows = body(raw('view_orders', {}, group='spacemolt_market')).get('orders') or []
    return [o for o in rows if isinstance(o, dict) and o.get('item_id') == item and (o.get('side') or o.get('order_type')) == 'buy'
            and int(o.get('remaining') or 0) > 0]


def own_sell_orders(item):
    """[{order_id, remaining, price_each}] of the pilot's own sell orders of `item` at the station where it is docked."""
    rows = body(raw('view_orders', {}, group='spacemolt_market')).get('orders') or []
    return [o for o in rows if isinstance(o, dict) and o.get('item_id') == item and (o.get('side') or o.get('order_type')) == 'sell'
            and int(o.get('remaining') or 0) > 0]


TICK = 11                    # seconds a game tick takes, with a margin: the waits of this runner and of craftchain.py


def craft_fields(d):
    """The fields of a craft answer where craftchain.py of the skill logistics-stock reads them: in `structuredContent`
    (or `result`), and there in `details` when it has one (a job's `job_id` stands there, guidebook logistics.md section 7)."""
    s = d
    for key in ('structuredContent', 'result'):
        if isinstance(d.get(key), dict):
            inner = d[key].get('structuredContent')
            s = inner if isinstance(inner, dict) else d[key]
            break
    return s.get('details') if isinstance(s.get('details'), dict) else s


def workshop(job, base):
    """One `craft` entry of a stop at the station's workshop, the way craftchain.py of the skill logistics-stock made
    harvesters and liquid hydrogen (2026-11-16): the entry's `inputs` aboard go into the pilot's storage first (the
    workshop takes its inputs from there, guidebook logistics.md sections 7 and 11); a quote (`dry_run`); then the runs,
    asked as runs x per_run made units (the game's `quantity`), again for the rest after each job delivered; the made
    units counted in storage, where they arrive, each job waited for at most craftchain.py's limit. A craft that cannot
    start makes nothing and moves nothing back: the run goes on. Returns (units made, the note for the run's row or None)."""
    recipe, runs, per, item = job['recipe'], int(job['runs']), int(job.get('per_run') or 1), job.get('makes')
    if not item:                                     # nothing named to count in storage: no wait could tell a job done
        say(f'craft {recipe}: not crafted, the entry names no `makes`')
        return 0, f'craft {recipe}: no makes'
    hold = cargo()
    for name in store_list(job.get('inputs') or [], hold):
        deposit(name, hold[name])
    # the game counts `quantity` in made units, rounded up to whole runs (27 liquid hydrogen asked queued 9 runs of 3,
    # queue.log ENT-114): runs x per_run asks every run in one job
    asked = {'recipe_id': recipe, 'quantity': runs * per, 'deliver_to': 'storage', 'preset': 'workshop'}
    if job.get('venue') == 'facility':               # a facility-only recipe (refine_steel): without `preset` the game rents
        del asked['preset']                          # a public facility and quotes its fee (requests.log ENT-190)
    quote = craft_fields(raw('craft', dict(asked, dry_run=True)))
    try:
        fee = float(quote.get('credits_total') or 0)
    except (TypeError, ValueError):
        fee = 0.0
    top = job.get('max_fee')                         # the most one run may cost, cr: what a run makes is worth no more
    if isinstance(top, (int, float)) and not isinstance(top, bool) and fee > top * runs:
        say(f'craft {recipe} x{runs}: not crafted, the quote asks {fee:.0f} cr, above max_fee {top} cr a run')
        return 0, f'craft {recipe}: fee above max_fee'
    pace = quote.get('effective_time_per_run')
    pace = pace if isinstance(pace, (int, float)) and not isinstance(pace, bool) and pace > 0 else 6   # craftchain.py's default
    if quote.get('have_inputs') is not True:
        say(f'craft {recipe} x{runs}: not crafted, the quote says have_inputs {quote.get("have_inputs")}: {str(quote.get("message") or quote.get("error") or "")[:100]}')
        return 0, f'craft {recipe}: no inputs'
    if fee > credits() - FLOOR:
        say(f'craft {recipe} x{runs}: not crafted, the quote asks {fee:.0f} cr and the wallet keeps {FLOOR} cr')
        return 0, f'craft {recipe}: fee'
    say(f'craft {recipe} x{runs}: quote: inputs here, {fee:.0f} cr, {pace} ticks a run')
    first = stored(base).get(item, 0)
    count, left, wanted = first, runs, runs * per
    while left > 0:
        answer = craft_fields(raw('craft', dict(asked, quantity=left * per)))
        queued = answer.get('runs') if isinstance(answer.get('runs'), int) and not isinstance(answer.get('runs'), bool) else 0
        if not queued:
            match = re.search(r'\((\d+) run', str(answer.get('message') or ''))
            queued = int(match.group(1)) if match else 0
        say(f'craft {recipe}: {left} runs asked, {queued} queued: {str(answer.get("message") or answer.get("kind") or answer.get("error") or "")[:100]}')
        if queued <= 0:
            break
        target = count + queued * per
        limit = time.time() + max(120, (pace * queued + 4) * TICK * 1.5)   # craftchain.py's limit for one job
        checks = 0
        while time.time() < limit:
            time.sleep(TICK)
            seen, checks = stored(base).get(item, 0), checks + 1
            if seen != count or checks % 5 == 0:     # say touches the order file: at least once a minute while it waits
                say(f'craft {recipe}: {seen - first} of {wanted} {item} in storage')
            count = seen
            if count >= target:
                break
        if count < target:
            break
        left -= queued
    made = count - first
    say(f'craft {recipe}: {made} of {wanted} {item} made')
    return made, (None if made >= wanted else f'craft {recipe}: {made} of {wanted} made')


PENDING_FIT = []             # (new, old) of a swap whose install was refused at a stop: fitted at the next dock, before its work


def modules_now():
    """The modules fitted now as the engine answers `get_ship` (each with its `type_id` and its instance's `module_id`):
    the live file lags a command by seconds. refit.py of the skill mining-chains read them so (2026-11-16)."""
    sc = body(raw('get_ship'))
    mods = sc.get('modules') or (sc.get('ship') or {}).get('modules') or []
    return [m for m in mods if isinstance(m, dict)]


def install_now(module, system, poi, base, min_count=1):
    """`install_mod` of a module aboard, read back from the engine: True when at least `min_count` copies stand fitted.
    Re-docks once if dock was lost between calls (requests ENT-289 and ENT-290)."""
    for attempt in range(2):
        d = raw('install_mod', {'module_id': module})
        time.sleep(TICK)
        now_n = sum(1 for m in modules_now() if (m.get('type_id') or m.get('type')) == module)
        if now_n >= min_count:
            say(f'fit {module}: fitted ({now_n}x)')
            return True
        said = text(d)[:120].replace('\n', ' / ')
        say(f'fit {module}: not fitted: {said}')
        if attempt or 'dock' not in said.lower():
            return False
        ok, msg = goal('prepare-at-station', {'systemId': system, 'poiId': poi, 'baseId': base, 'refuel': False})
        say(f'fit {module}: docked again at {base}: {ok} {msg[:80]}')
    return False


def unfit_module(mod_type, system, poi, base):
    """Strip every fitted instance of `mod_type` at a docked stop and deposit it in station storage so off-role starter
    modules stop wasting slots, CPU and power. Returns an error note only if an instance refused removal."""
    removed = 0
    for _guard in range(8):
        have = [m for m in modules_now() if (m.get('type_id') or m.get('type')) == mod_type]
        if not have:
            break
        before_n = len(have)
        inst_id = have[0].get('module_id') or have[0].get('id') or mod_type
        for attempt in range(2):
            d = raw('uninstall_mod', {'module_id': inst_id})
            time.sleep(TICK)
            after_n = sum(1 for m in modules_now() if (m.get('type_id') or m.get('type')) == mod_type)
            if after_n < before_n:
                removed += 1
                say(f'unfit {mod_type}: removed ({after_n} left)')
                break
            said = text(d)[:100].replace('\n', ' / ')
            if attempt or 'dock' not in said.lower():
                say(f'unfit {mod_type}: refused: {said}')
                if cargo().get(mod_type):
                    deposit(mod_type, cargo()[mod_type])
                return f'unfit {mod_type}: not taken out'
            goal('prepare-at-station', {'systemId': system, 'poiId': poi, 'baseId': base, 'refuel': False})
    if cargo().get(mod_type):
        deposit(mod_type, cargo()[mod_type])
    return None


def swap_module(want, system, poi, base):
    """A `fit` entry with `replace` (requests ENT-290), the new module aboard (bought by the fit step inside max_price):
    `uninstall_mod` of one copy of `old`, `install_mod` of `new` (verified by count), and deposit `old` in storage."""
    new, old = want['module'], want['replace']
    now_mods = modules_now()
    have = [m for m in now_mods if (m.get('type_id') or m.get('type')) == old]
    new_before = sum(1 for m in now_mods if (m.get('type_id') or m.get('type')) == new)
    if have:
        old_before = len(have)
        d = raw('uninstall_mod', {'module_id': have[0].get('module_id') or have[0].get('id') or old})
        time.sleep(TICK)
        old_after = sum(1 for m in modules_now() if (m.get('type_id') or m.get('type')) == old)
        if old_after >= old_before:
            say(f'fit {new}: uninstall_mod left {old} fitted: {text(d)[:100]}; {new} stays in the hold')
            return f'{new}: {old} not taken out'
        say(f'fit {new}: {old} taken out')
    if not install_now(new, system, poi, base, min_count=new_before + 1):
        if cargo().get(old) and install_now(old, system, poi, base):
            return f'{new}: not fitted, {old} fitted again'
        PENDING_FIT.append((new, old))
        return f'{new}: not fitted, {old} out'
    if cargo().get(old):
        deposit(old, cargo()[old])
    return None


def fit_pending(system, poi, base):
    """At a stop just docked: a swap of an earlier stop whose install was refused fits the new module, else the old one
    back, before the stop's work and before the pilot leaves; the run's row says which (requests ENT-290)."""
    while PENDING_FIT:
        new, old = PENDING_FIT.pop(0)
        if install_now(new, system, poi, base):
            notes.append(f'{new}: fitted at {base}')
            if cargo().get(old):
                deposit(old, cargo()[old])
        elif cargo().get(old) and install_now(old, system, poi, base):
            notes.append(f'{new}: not fitted, {old} fitted again at {base}')
        else:
            notes.append(f'{new}: not fitted at {base} either')


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
    for m in re.finditer(r'--- (.+?) \[([A-Za-z0-9_-]+)\](.*?)(?=\n--- |\Z)', t, re.S):
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
skipped = 0                                          # stops passed over because none of their missions is held
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
    if skipped == len(ROUTE['stops']) and 'every stop skipped' not in notes:   # the pilot held none of the missions: no try (dispatch.py)
        notes.append('every stop skipped')
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


def pilot_stop_paths():
    safe = re.sub(r'[^A-Za-z0-9_.-]', '_', pilot)[:60] or 'pilot'
    paths = [DATA / 'fleet' / 'stop' / pilot]
    if safe != pilot:
        paths.append(DATA / 'fleet' / 'stop' / safe)
    return paths


def stop_reason():
    """Return why this run must stop now (global STOP or per-pilot stop file), auto-consuming a standalone per-pilot stop file."""
    if (DATA / 'fleet' / 'STOP').exists():
        return 'STOP file'
    for sp in pilot_stop_paths():
        if sp.exists():
            try:
                sp.unlink()
            except OSError:
                pass
            return 'stopped by per-pilot stop file'
    return ''


sys.excepthook = crashed
atexit.register(finish)                              # after order_done, so it runs before it: the row first, then the order file goes
for n, stop in enumerate(ROUTE['stops']):
  try:
    time.sleep(0)                                    # wake immediately if runhost set our stop event during a blocking goal
    why_stop = stop_reason()
    if why_stop:
        say(f'told to stop ({why_stop}): ending circuit before stop {n + 1}')
        if why_stop not in notes:
            notes.append(why_stop)
        break
    system, poi, base = stop['at'].split(':')
    system, poi, moved = mobile.locate(system, poi, base, DATA)
    if moved and n >= first:
        say(f'stop {n + 1}: {moved}')
    if n < first:
        reached += 1
        continue
    hold = cargo()
    if stop.get('skip_if_hold') and all(hold.get(i, 0) >= q for i, q in stop['skip_if_hold'].items()):
        reached += 1
        continue
    if stop.get('only_if_active') and not ({title for title, _mid, _fin in active()} & set(stop['only_if_active'])):
        reached += 1
        skipped += 1
        continue
    ok, msg = goal('prepare-at-station', {'systemId': system, 'poiId': poi, 'baseId': base, 'refuel': stop.get('refuel', True) is not False})
    if not ok:
        say(f'stop {n + 1} {base}: not reached: {msg[:120]}')
        notes.append(f'stop {n + 1} not reached')
        break
    reached += 1
    fit_pending(system, poi, base)                   # requests ENT-290: a swap a stop before could not fit is fitted here first
    hand_in(done, onetime)
    if stop.get('redock'):
        raw('undock')
        time.sleep(11)
        raw('dock')
        time.sleep(11)
        hand_in(done, onetime)
    hold = cargo()
    keep = aboard_ammo(hold) if 'all' in (stop.get('store'), stop.get('store_faction')) else set()
    for item in store_list(stop.get('store'), hold, keep):
        if hold.get(item):
            deposit(item, hold[item])
    for want in stop['gift'] if isinstance(stop.get('gift'), list) else [stop['gift']] if stop.get('gift') else []:   # r22: goods into the storage of another pilot of ours
        import handover                              # here, not at the top: only a stop that gives loads it (the switch strict-classes-on inside)
        handed = handover.give(raw, cargo, say, time.sleep, pilot, base, want, str(DATA), ROUTE['id'])
        print(handed['line'], flush=True)            # one RESULT line per gift: what went to whom, what stayed
        if handed['note']:
            notes.append(handed['note'])
    if stop.get('store_faction'):                    # hold -> the faction's storage here (an outpost of ours, a lockbox)
        hold = cargo()
        for item in store_list(stop.get('store_faction'), hold, keep):
            if hold.get(item):
                deposit(item, hold[item], 'faction')
    if stop.get('burn_cells'):                       # carried cells into the tank instead of a station's fuel
        burn_cells()
    if stop.get('bunker'):                           # carried cells -> tank -> the faction's fuel reserve here (an outpost of ours)
        moved, burnt, refused = bunker(int((stop['bunker'] or {}).get('keep', 25)))
        reserve = body(raw('view', {'target': 'faction', 'station_id': base}, group='spacemolt_storage')).get('faction_fuel_reserve')
        say(f'bunker: {moved} fuel deposited from {burnt} cells; the faction fuel reserve here reads {reserve}')
        notes.append(f'bunker +{moved} fuel from {burnt} cells, reserve {reserve}')
        if refused:
            notes.append('bunker: deposit refused')
    book, board = save_station(base, system)
    for want in stop.get('withdraw') or []:              # own storage -> hold: sold here into the bid, or carried on
        if want.get('from') == 'faction':                # the faction's storage here -> hold (orders ENT-083: the outpost's iron)
            held = faction_stored(base).get(want['item'], 0)
            units = faction_withdraw_units(want, held, room(), SIZES.get(want['item'], 1))
            if units:
                d = raw('withdraw', {'item_id': want['item'], 'quantity': units, 'target': 'self', 'source': 'faction'}, group='spacemolt_storage')
                time.sleep(11)
                if 'error' in d:
                    say(f'faction withdraw {units} {want["item"]}: refused: {str(d.get("error"))[:120]}')
                    notes.append(f'faction withdraw {want["item"]}: refused')
                else:
                    say(f'withdrew {units} {want["item"]} from the faction storage here ({held} held, keep {want.get("keep") or 0})')
            else:
                say(f'faction withdraw {want["item"]}: nothing to take ({held} held, keep {want.get("keep") or 0}, or no room)')
            continue
        sale = next((s for s in stop.get('sell') or [] if s.get('item') == want['item']), None)
        here = stored(base)
        units = withdraw_units(want, here.get(want['item'], 0), room(), sale, book.get(want['item']) or {}, cargo().get(want['item'], 0),
                               SIZES.get(want['item'], 1))
        if units:
            d = raw('withdraw', {'item_id': want['item'], 'quantity': units, 'target': 'self'}, group='spacemolt_storage')
            time.sleep(11)
            say(f'withdrew {units} {want["item"]} from storage' + (f': {str(d.get("error"))[:100]}' if 'error' in d else ''))
        else:
            say(f'withdraw {want["item"]}: nothing to take (stored, hold or bid)')
    for want in stop.get('sell') or []:
        sell_into_bid(want, book)
    unbought = ''                                        # Q75 (6), errors.log ENT-113: the first buy of this stop that got nothing
    for want in stop.get('buy') or []:
        need = want['qty'] - cargo().get(want['item'], 0)
        if need > 0 and credits() - need * want['max_price'] * 1.01 < FLOOR:
            say(f'buy {need} {want["item"]}: not bought, the wallet would fall under {FLOOR} cr')
            notes.append(f'{want["item"]}: wallet floor')
            unbought = unbought or want['item']
        elif need > 0:
            ask, units = offer(book, want['item'], want['max_price'], need)
            if not units:                                # nothing stands at the limit or under it, tax included: nothing is bought
                say(f'buy {need} {want["item"]}: not bought, the best ask is {ask or "none"} and the limit is {want["max_price"]} with tax')
                notes.append(f'{want["item"]}: not bought')
                unbought = unbought or want['item']
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
            if got <= had:
                unbought = unbought or want['item']
    if unbought and stop.get('stop_on_failed_buy'):      # Q75 (6): the dispatcher reads the route's requires.ask again instead
        say(f'stop {n + 1} {base}: the buy of {unbought} got nothing: the run ends here (stop_on_failed_buy); the goods stay where they are')
        notes.append(f'stop {n + 1}: the buy of {unbought} got nothing: run ended (stop_on_failed_buy)')
        break
    made = {}                                            # item -> units this stop's crafts put into storage (requests ENT-013)
    for job in stop.get('craft') or []:
        units, note = workshop(job, base)
        if note:
            notes.append(note)
        if units > 0:
            made[job['makes']] = made.get(job['makes'], 0) + units
    if made:                                             # what was made comes into the hold, then the stop's sale runs once more for it
        book, board = save_station(base, system)         # the book read before the craft may be minutes old: no sale into a bid gone since
        for item, units in made.items():
            sale = next((s for s in stop.get('sell') or [] if s.get('item') == item), None)
            take = withdraw_units({'item': item, 'qty': units}, stored(base).get(item, 0), room(), sale, book.get(item) or {}, cargo().get(item, 0),
                                  SIZES.get(item, 1))
            if take:
                d = raw('withdraw', {'item_id': item, 'quantity': take, 'target': 'self'}, group='spacemolt_storage')
                time.sleep(11)
                say(f'withdrew {take} {item} from storage after the craft' + (f': {str(d.get("error"))[:100]}' if 'error' in d else ''))
            else:
                say(f'withdraw {item}: nothing to take after the craft (stored, hold or bid)')
        for want in [s for s in stop.get('sell') or [] if s.get('item') in made]:
            sell_into_bid(want, book)
    for want in stop.get('sell_order') or []:           # rule F39: one resting sell order of a good held here, kept at its price
        mine = own_sell_orders(want['item'])
        have = cargo().get(want['item'], 0) + stored(base).get(want['item'], 0)
        for move in sell_order_moves(want, (book or {}).get(want['item']) or {}, mine, have):
            if move[0] == 'modify':
                d = raw('modify_order', {'order_id': move[1], 'new_price': move[2]}, group='spacemolt_market')
                said = f'sell order {want["item"]}: repriced to {move[2]}'
            else:
                d = raw('create_sell_order', {'item_id': want['item'], 'quantity': move[1], 'price_each': move[2]}, group='spacemolt_market')
                said = f'sell order {want["item"]}: {move[1]} listed at {move[2]}'
            time.sleep(11)                               # one order call a tick (the game's rate limit)
            if 'error' in d:
                said += f' refused: {str(d.get("error"))[:100]}'
            say(said)
            notes.append(said)
    for want in stop.get('buy_order') or []:             # rule F39: standing wholesale buy wall at <= ceiling
        mine = own_buy_orders(want['item'])
        avail = max(0, credits() - FLOOR)
        for move in buy_order_moves(want, (book or {}).get(want['item']) or {}, mine, avail):
            if move[0] == 'modify':
                d = raw('modify_order', {'order_id': move[1], 'new_price': move[2]}, group='spacemolt_market')
                said = f'buy order {want["item"]}: repriced to {move[2]}'
            else:
                d = raw('create_buy_order', {'item_id': want['item'], 'quantity': move[1], 'price_each': move[2]}, group='spacemolt_market')
                said = f'buy order {want["item"]}: {move[1]} bid at {move[2]}'
            time.sleep(11)
            if 'error' in d:
                said += f' refused: {str(d.get("error"))[:100]}'
            say(said)
            notes.append(said)
    watch_m = float(stop.get('watch_minutes') or 0)
    has_desk_work = bool(stop.get('sell_order') or stop.get('buy_order') or stop.get('craft') or stop.get('market_poll'))
    if watch_m > 0 and has_desk_work and not ROUTE.get('park'):
        watch_m = min(120.0, watch_m)
        every_s = max(120.0, float(stop.get('watch_interval_minutes') or 5) * 60.0)
        until = time.time() + watch_m * 60.0
        next_poll = time.time() + every_s
        say(f'active docked desk watch at {base} for {watch_m:.0f}m (poll every {every_s/60.0:.0f}m, 0 fuel)')
        while time.time() < until and not stop_reason():
            time.sleep(min(30.0, max(1.0, until - time.time())))
            try:
                os.utime(ORDER)
            except OSError:
                pass
            if time.time() >= next_poll and time.time() < until and not stop_reason():
                next_poll = time.time() + every_s
                book = save_station(base, system)[0] or book   # the book and the board saved; save_book/save_board never existed (NameError)
                for want in stop.get('sell_order') or []:
                    mine = own_sell_orders(want['item'])
                    have = cargo().get(want['item'], 0) + stored(base).get(want['item'], 0)
                    for move in sell_order_moves(want, (book or {}).get(want['item']) or {}, mine, have):
                        if move[0] == 'modify':
                            raw('modify_order', {'order_id': move[1], 'new_price': move[2]}, group='spacemolt_market')
                        else:
                            raw('create_sell_order', {'item_id': want['item'], 'quantity': move[1], 'price_each': move[2]}, group='spacemolt_market')
                        time.sleep(11)
                for want in stop.get('buy_order') or []:
                    mine = own_buy_orders(want['item'])
                    avail = max(0, credits() - FLOOR)
                    for move in buy_order_moves(want, (book or {}).get(want['item']) or {}, mine, avail):
                        if move[0] == 'modify':
                            raw('modify_order', {'order_id': move[1], 'new_price': move[2]}, group='spacemolt_market')
                        else:
                            raw('create_buy_order', {'item_id': want['item'], 'quantity': move[1], 'price_each': move[2]}, group='spacemolt_market')
                        time.sleep(11)
    did_unfit = False
    for umod in stop.get('unfit') or []:                 # strip off-role starter modules before fitting slots
        did_unfit = True
        unote = unfit_module(umod, system, poi, base)
        if unote:
            notes.append(unote)
    for want in stop.get('fit') or []:                   # buy and fit up to `count` copies (default 1)
        if want.get('replace') and not FIT_REPLACE:      # requests ENT-290: the swap is switched off; nothing is bought for it
            say(f'fit {want["module"]}: not fitted, `replace` is switched off (FIT_REPLACE)')
            notes.append(f'{want["module"]}: replace off')
            continue
        target_n = max(1, int(want.get('count') or 1))
        if want.get('replace') or target_n > 1 or did_unfit:
            fitted = [m.get('type_id') or m.get('type') for m in modules_now()]
        else:
            try:
                live = json.load(open(DATA / 'fleet' / 'ships' / ((re.sub(r'[^A-Za-z0-9_.-]', '_', pilot)[:60] or 'pilot') + '.json'), encoding='utf-8'))
                fitted = [m.get('type') for m in live.get('modules') or [] if isinstance(m, dict)]
            except (OSError, ValueError):
                fitted = []
        cur_n = fitted.count(want['module'])
        if cur_n >= target_n:
            say(f'fit {want["module"]}: {cur_n}/{target_n} fitted already')
            if want.get('replace') and cargo().get(want['replace']):     # what an earlier swap took out is still aboard: stored here
                deposit(want['replace'], cargo()[want['replace']])
            continue
        for _copy_i in range(target_n - cur_n):
            if not cargo().get(want['module']):
                if credits() - want['max_price'] * 1.01 < FLOOR:
                    say(f'fit {want["module"]}: not bought, the wallet would fall under {FLOOR} cr')
                    notes.append(f'{want["module"]}: wallet floor')
                    break
                ask, units = offer(book, want['module'], want['max_price'], 1)
                if not units:                            # nothing stands at the limit or under it, tax included: nothing is bought
                    say(f'fit {want["module"]}: not bought, the best ask is {ask or "none"} and the limit is {want["max_price"]} with tax')
                    notes.append(f'{want["module"]}: not bought')
                    break
                c0 = credits()
                ok, msg = goal('buy-items', {'items': [{'itemId': want['module'], 'maxPrice': ask, 'maxQuantity': 1}]}, tries=1)
                paid = c0 - credits()
                say(f'buy {want["module"]} at the ask of {ask} (limit {want["max_price"]} with tax): {ok}, {-paid:+d} cr {"" if ok else msg[:100]}')
                if paid > want['max_price']:
                    notes.append(f'{want["module"]}: paid {paid}, above the limit of {want["max_price"]}')
                if paid > 0:                             # a tool is bought once: kept out of the steady costs, like a mission's goods
                    book_onetime(f'{ROUTE["id"]}: {want["module"]} bought (tool)', -paid)
                    onetime[0] -= paid
            if not cargo().get(want['module']):
                notes.append(f'{want["module"]}: not bought')
                break
            if want.get('replace'):                      # requests ENT-290: the old one out, the new one in, the old one stored
                note = swap_module(want, system, poi, base)
                if note:
                    notes.append(note)
                    break
                cur_n += 1
                continue
            if target_n == 1 and not did_unfit:          # single-slot fit without unfit/replace preserves exact pre-r22 wire sequence
                d = raw('install_mod', {'module_id': want['module']})
                time.sleep(11)
                answer = text(d)[:140].replace('\n', ' / ')
                say(f'fit {want["module"]}: {answer}')
                if cargo().get(want['module']):
                    notes.append(f'{want["module"]}: not fitted')
                break
            if install_now(want['module'], system, poi, base, min_count=cur_n + 1):
                cur_n += 1
            else:
                if cargo().get(want['module']):
                    deposit(want['module'], cargo()[want['module']])
                notes.append(f'{want["module"]}: not fitted')
                break
    if stop.get('accept'):
        have = {title for title, _mid, _fin in active()}
        accepted_or_held = 0
        for entry in stop['accept']:
            template, needs = (entry, {}) if isinstance(entry, str) else (entry.get('template') or entry.get('title'), entry.get('needs') or {})
            title = None if isinstance(entry, str) else entry.get('title')
            hold = cargo()
            short = {i: n for i, n in needs.items() if hold.get(i, 0) < n}
            if short:
                say(f'{template}: not accepted, the hold lacks {short}')
                notes.append(f'{template}: goods missing')
                continue
            posted = posted_mission(board, template, title)   # never `offer`: that is the function the buy and fit steps call
            if posted is None:
                say(f'{template}: not on the board of {base}')
                notes.append(f'{template} not offered')
            elif posted.get('title') in have:
                say(f'{template}: already accepted')
                accepted_or_held += 1
            else:
                target_mid = posted.get('mission_id') or posted.get('template_id') or template
                ok, msg = goal('accept-mission', {'missionId': target_mid}, tries=1)
                say(f'accept {template}: {ok} {msg[:100]}')
                if ok:
                    accepted_or_held += 1
                else:
                    notes.append(f'{template} not accepted')
        route_titles = set(ROUTE.get('one_time') or []) | set(ROUTE.get('skip_if_booked') or [])
        if accepted_or_held == 0 and not (have & route_titles) and pure_visit_tail(ROUTE['stops'][n + 1:]):
            say(f'aborting empty tour: none of {len(stop["accept"])} mission(s) offered/accepted at stop {n + 1}')
            notes.append('mission not offered: skipped empty tour')
            break
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
        try:
            while left and time.time() < until and not stop_reason():
                time.sleep(30)
                try:
                    os.utime(ORDER)
                except OSError:
                    pass
                left = {title for title, _mid, finished in active() if not finished} & wanted
                if left and not call('GET', f'/accounts/{P}/loop')[1].get('running'):
                    notes.append(f'mine {mine_poi}: the loop ended by itself')
                    break
        finally:                                         # also when the run is told to stop (runhost.py): a loop left running refuses every goal
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
        command += ['--alone-mode', 'pirates'] if step.get('alone') == 'pirates' else []   # the step's own rule, as a hunt route's
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
            if not left or 'left: a ship' in answer or stop_reason():
                break
        say(f'hunt at {hunt_poi}: ' + ('objectives done' if not left else f'stopped, still open: {sorted(left)}'))
        if left:
            notes.append(f'hunt {hunt_poi}: objectives not done; the step said: {said}; the ship stood at {where_now()}')
    if verbose:
        active()
  except SystemExit as leave:                        # told to stop (runhost per-pilot stop file or signal): record reason cleanly
    stopped = leave.code if isinstance(leave.code, str) and leave.code else 'stopped'
    if stopped not in notes:
        notes.append(stopped)
    say(f'told to stop ({stopped}): ending circuit cleanly')
    break
finish()

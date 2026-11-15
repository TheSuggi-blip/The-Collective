"""Small client for the fleet engine's gate, with the division's lock. Standard library only, no proxy.

Reading is free: `get`, and `raw` with an action that only reads. Anything else is a
command, and a command goes only to a pilot this shell may drive (division.py): a ship
of its own division that no runner is flying. The first command takes the pilot by hand:
an order file `hand <Member>` keeps the dispatcher off it. Every further command keeps
the hold fresh; `release` ends it; it dies 20 minutes after the last command.

Never sent for an Admiral, whatever the pilot: the auth tools (a new pilot is Suggi's
word, orders F5), a faction command that changes anything (the faction is the Fleet
Admiral's, F11), `self_destruct`, and any path of the engine but a pilot's raw, goal
and loop.

Usage:
  gate.py get <path>
  gate.py raw <pilot> <action> ['<json params>'] [toolGroup]
  gate.py goal <pilot> <type> ['<json options>']
  gate.py post <path> '<json body>'
  gate.py patch|delete <path> ['<json body>']
  gate.py hold <pilot>
  gate.py release <pilot>
Prints the JSON answer (passwords masked), cut to 3000 chars unless FULL=1.
"""
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import division                                   # noqa: E402

GATE = 'http://172.30.0.32:7580'
OPENER = urllib.request.build_opener(urllib.request.ProxyHandler({}))
ACCOUNT = re.compile(r'^/accounts/([^/?]+)(/[^?]*)?')
# Actions that only read. Every `get_...` reads too. Anything not listed is treated as a command.
READ = {'view', 'info', 'catalog', 'help', 'status', 'summary', 'log', 'list', 'rooms', 'garages', 'policies', 'quote', 'wrecks',
        'completed_missions', 'view_completed_mission', 'inspect', 'find_route', 'search_systems', 'list_passengers',
        'list_station_passengers', 'list_missions', 'list_ships', 'commission_quote', 'commission_status', 'fit_preview',
        'tax_estimate', 'estimate_purchase', 'analyze_market', 'view_market', 'view_orders', 'view_ship_buy_orders', 'browse_ships'}


def is_read(action):
    return str(action).startswith('get_') or action in READ


def call(method, path, body=None, timeout=400):
    data = None if body is None else json.dumps(body).encode('utf-8')
    req = urllib.request.Request(GATE + path, data=data, method=method.upper(),
                                 headers={'Content-Type': 'application/json'} if data is not None else {})
    try:
        with OPENER.open(req, timeout=timeout) as r:
            return r.status, r.read().decode('utf-8', 'replace')
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode('utf-8', 'replace')


def q(name):
    return urllib.parse.quote(name, safe='')


def hold_file(pilot):
    return os.path.join(division.DATA, 'fleet', 'orders', pilot + '.json')


def forbidden(group, action):
    """Why an Admiral's hand may not send this command; '' when it may."""
    kind, name = division.member()
    if kind == 'service' or name == 'Unity':
        return ''
    if group == 'spacemolt_auth':
        return 'the auth tools are the Fleet Admiral\'s: a new pilot is Suggi\'s word (orders F5)'
    if group == 'spacemolt_faction' and not is_read(action):
        return 'the faction is the Fleet Admiral\'s, on Suggi\'s word (orders F11)'
    if action == 'self_destruct':
        return 'no ship of ours is destroyed by its own hand'
    return ''


def take(pilot, group='', action=''):
    """Refuse, or take the pilot by hand: write its order file, or keep the hold fresh."""
    why = forbidden(group, action)
    if why:
        sys.exit('REFUSED: ' + why)
    division.require(pilot)
    mark, path = division.hand_mark(), hold_file(pilot)
    what = division.order_of(pilot)
    if what == mark:
        os.utime(path)
    elif not what:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as handle:
            json.dump({'pilot': pilot, 'what': mark, 'since': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}, handle)
        print('held by hand: %s (%s); `gate.py release %s` when done' % (pilot, mark, pilot), file=sys.stderr)


def release(pilot):
    kind, name = division.member()
    what = division.order_of(pilot)
    if what.startswith('hand ') and (what == division.hand_mark() or name == 'Unity'):
        os.remove(hold_file(pilot))
        return 'released: %s' % pilot
    return '%s carries no hand hold of yours (%s)' % (pilot, what or 'no order file')


def engine_only():
    kind, name = division.member()
    if not (kind == 'service' or name == 'Unity'):
        sys.exit('REFUSED: a call that names no pilot (a new pilot, the engine itself) is the Fleet Admiral\'s (orders F5)')


def main():
    args = sys.argv[1:]
    verb = args[0] if args else ''
    if verb == 'get' and len(args) == 2:
        status, text = call('get', args[1])
    elif verb == 'raw' and len(args) >= 3:
        params = json.loads(args[3]) if len(args) > 3 else {}
        group = args[4] if len(args) > 4 else 'spacemolt'
        if not is_read(args[2]):
            take(args[1], group, args[2])
        status, text = call('post', f'/accounts/{q(args[1])}/raw', {'toolGroup': group, 'action': args[2], 'params': params})
    elif verb == 'goal' and len(args) >= 3:
        take(args[1])
        options = json.loads(args[3]) if len(args) > 3 else {}
        status, text = call('post', f'/accounts/{q(args[1])}/goal', {'type': args[2], 'options': options})
    elif verb in ('post', 'patch', 'delete') and len(args) >= 2:
        body = json.loads(args[2]) if len(args) > 2 else (None if verb == 'delete' else {})
        found = ACCOUNT.match(args[1])
        if found and found.group(1) != 'register':
            reads = verb == 'post' and found.group(2) == '/raw' and is_read((body or {}).get('action'))
            if found.group(2) not in ('/raw', '/goal', '/loop'):
                engine_only()
            if not reads:
                take(urllib.parse.unquote(found.group(1)), (body or {}).get('toolGroup') or '', (body or {}).get('action') or '')
        else:
            engine_only()
        status, text = call(verb, args[1], body)
    elif verb == 'hold' and len(args) == 2:
        take(args[1])
        print('held: %s (%s)' % (args[1], division.order_of(args[1])))
        return
    elif verb == 'release' and len(args) == 2:
        print(release(args[1]))
        return
    else:
        sys.exit(__doc__)
    text = re.sub(r'("password"\s*:\s*)"[^"]*"', r'\1"<masked>"', text)
    print('http', status)
    print(text if os.environ.get('FULL') else text[:3000])


if __name__ == '__main__':
    main()

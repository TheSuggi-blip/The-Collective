"""Small client for the fleet engine's gate, with the division's lock. Standard library only, no proxy.

Reading is free: `get`, and `raw` with an action that only reads. Anything else is a
command, and a command goes only to a pilot this shell may drive (division.py): a ship
of its own division that no runner is flying. The first command takes the pilot by hand:
an order file `hand <Member>` keeps the dispatcher off it. Every further command keeps
the hold fresh; `release` ends it; it dies 20 minutes after the last command.

Never sent for an Admiral, whatever the pilot: the auth tools (a new pilot is Suggi's
word, orders F5), a faction command that changes anything (the faction is the Fleet
Admiral's, F11), a word to another player (chat, the forum, a petition, a status:
orders F4), `self_destruct`, and any path of the engine but a pilot's raw, goal and
loop.

Usage:
  gate.py get <path>
  gate.py raw <pilot> <action> ['<json params>'] [toolGroup]
  gate.py goal <pilot> <type> ['<json options>']
  gate.py goal <pilot> complete-mission '<json options>' --one-time "<mission title>"
                                    a hand-in whose reward is paid once: booked as one-time money, as a runner books it
  gate.py post <path> '<json body>'
  gate.py patch|delete <path> ['<json body>']
  gate.py hold <pilot>
  gate.py release <pilot>
  gate.py book_onetime <pilot> "<title>" <credits>
                                    one row of data/fleet/onetime.json by hand, no game call: a reward paid once (+) or a
                                    hull or tool bought once (-) of a pilot of your own division (Mercury, Q75 (6))
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
        'tax_estimate', 'estimate_purchase', 'analyze_market', 'view_market', 'view_orders', 'view_ship_buy_orders', 'browse_ships',
        'types', 'faction_list', 'faction_owned', 'owned', 'upgrades'}      # spacemolt_facility's cards (Apollo, reports 2026-11-17)


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


SPEAKS = {'chat', 'petition', 'set_status', 'forum_create_thread', 'forum_reply', 'forum_edit_thread', 'forum_edit_reply',
          'forum_delete_thread', 'forum_delete_reply', 'forum_upvote'}      # a word to other players


def forbidden(group, action):
    """Why an Admiral's hand may not send this command; '' when it may."""
    kind, name = division.member()
    if kind == 'service' or name == 'Unity':
        return ''
    if group == 'spacemolt_auth':
        return 'the auth tools are the Fleet Admiral\'s: a new pilot is Suggi\'s word (orders F5)'
    if group == 'spacemolt_faction' and not is_read(action):
        return 'the faction is the Fleet Admiral\'s, on Suggi\'s word (orders F11)'
    if action in SPEAKS:
        return 'a word to another player is the Fleet Admiral\'s, on Suggi\'s word (orders F4)'
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


def book_onetime(pilot, title, amount):
    """One row in data/fleet/onetime.json, under its lock: the collector keeps this money out of the steady income."""
    import fcntl
    path = os.path.join(division.DATA, 'fleet', 'onetime.json')
    with open(path + '.lock', 'w') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        try:
            rows = json.load(open(path, encoding='utf-8'))
        except (OSError, ValueError):
            rows = []
        rows.append([int(time.time()), pilot, title, amount])
        tmp = '%s.%d.tmp' % (path, os.getpid())
        with open(tmp, 'w', encoding='utf-8') as fh:
            json.dump(rows[-5000:], fh, separators=(',', ':'))
        os.replace(tmp, path)


ONCE_AGAIN = 10 * 60          # the same row (pilot, title, credits) booked by hand again within this long is refused
WALLETS = ('Wallet top-up', 'Faction treasury: credits deposited')     # wallet.py's own titles: moves between our purses


def book_by_hand(pilot, title, credits):
    """The verb `book_onetime`: book_onetime() for a pilot of the member's own division, without a script of its own.
    Refused: a shell that is no member, a pilot of another division, a title of wallet.py's own, an amount that is no
    whole number other than 0, and the same row booked by hand within ONCE_AGAIN (a command typed twice)."""
    kind, name = division.member()
    if kind is None:
        sys.exit('REFUSED: this shell is no member of The Collective: it books nothing')
    if kind != 'service' and name != 'Unity' and division.owner(pilot, division.DATA) != name:
        sys.exit('REFUSED: %s is commanded by %s, not by %s: its money is booked by its own division (orders F1)' % (pilot, division.owner(pilot, division.DATA), name))
    title = ' '.join(str(title).split())
    if not title or len(title) > 120 or not title.isascii() or title.startswith(WALLETS):
        sys.exit('REFUSED: a title is 1 to 120 ASCII characters and none of wallet.py\'s own (%s)' % ', '.join(WALLETS))
    try:
        amount = int(str(credits).replace(',', '').replace('+', ''))
    except ValueError:
        sys.exit('REFUSED: the credits are a whole number, + for a reward paid once, - for a thing bought once: %s' % credits)
    if amount == 0:
        sys.exit('REFUSED: 0 credits books nothing')
    path = os.path.join(division.DATA, 'fleet', 'onetime.json')
    try:
        with open(path, encoding='utf-8') as handle:
            rows = json.load(handle)
    except (OSError, ValueError):
        rows = []
    again = [r for r in rows if isinstance(r, list) and len(r) == 4 and r[1:] == [pilot, title, amount] and time.time() - (r[0] or 0) < ONCE_AGAIN]
    if again:
        sys.exit('REFUSED: %s %+d cr `%s` was booked at %s UTC already: once is once (again after %d minutes, if it was paid twice)'
                 % (pilot, amount, title, time.strftime('%H:%M:%S', time.gmtime(again[-1][0])), ONCE_AGAIN // 60))
    book_onetime(pilot, title, amount)
    return 'one-time money booked: %s %+d cr, %s (data/fleet/onetime.json; kept out of the steady money)' % (pilot, amount, title)


def engine_only():
    kind, name = division.member()
    if not (kind == 'service' or name == 'Unity'):
        sys.exit('REFUSED: a call that names no pilot (a new pilot, the engine itself) is the Fleet Admiral\'s (orders F5)')


def main():
    args = sys.argv[1:]
    once = ''
    if '--one-time' in args:
        at = args.index('--one-time')
        once, args = (args[at + 1] if at + 1 < len(args) else ''), args[:at] + args[at + 2:]
        if not once or len(args) < 3 or args[0] != 'goal' or args[2] != 'complete-mission':
            sys.exit('gate.py: --one-time "<mission title>" goes with `goal <pilot> complete-mission` only')
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
        if once:
            paid = re.search(r'\+([\d,]+) credits', text) if status == 200 else None
            if paid:
                book_onetime(args[1], once, int(paid.group(1).replace(',', '')))
            print('one-time money booked: +%s cr, %s' % (paid.group(1), once) if paid else 'not booked as one-time money: the answer names no credits')
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
    elif verb == 'book_onetime' and len(args) == 4:     # Q75 (6): book_onetime by hand, no game call
        print(book_by_hand(args[1], args[2], args[3]))
        return
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

"""Loot every carcass and wreck at the pilot's place that the pilot itself killed.

Usage: python3 -I loot_own.py <pilot> [--any-creature]

Only wrecks whose killer is this pilot are touched (--any-creature adds creature
carcasses killed by another pilot of ours; never a ship's wreck). A carcass
expires 30 minutes after the kill. One loot per tick; a refused loot is tried
again twice. Prints what was taken."""
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

GATE = 'http://172.30.0.32:7580'
OPENER = urllib.request.build_opener(urllib.request.ProxyHandler({}))
pilot = sys.argv[1]
P = urllib.parse.quote(pilot, safe='')
OURS = ('miner-', 'trader-', 'hauler-', 'drone-', 'scout-')


def raw(action, params=None, group='spacemolt_salvage'):
    req = urllib.request.Request(GATE + f'/accounts/{P}/raw', data=json.dumps({'toolGroup': group, 'action': action, 'params': params or {}}).encode(),
                                 method='POST', headers={'Content-Type': 'application/json'})
    try:
        with OPENER.open(req, timeout=120) as r:
            return json.loads(r.read().decode('utf-8', 'replace') or '{}')
    except urllib.error.HTTPError as e:
        try:
            return json.loads(e.read().decode('utf-8', 'replace') or '{}')
        except ValueError:
            return {'error': str(e.code)}
    except Exception as e:
        return {'error': f'{type(e).__name__}: {e}'}


wrecks = (raw('wrecks').get('structuredContent') or {}).get('wrecks') or []
taken = {}
for w in wrecks:
    killer = str(w.get('killer_name') or '')
    mine = killer == pilot or ('--any-creature' in sys.argv and w.get('type') == 'creature' and killer.startswith(OURS))
    if not mine or not w.get('cargo'):
        continue
    for attempt in range(3):
        d = raw('loot', {'wreck_id': w['id']})
        if 'error' not in d:
            for c in w['cargo']:
                taken[c['item_id']] = taken.get(c['item_id'], 0) + int(c.get('quantity') or 0)
            break
        print(pilot, 'loot refused:', str(d.get('error'))[:120], flush=True)
        if 'not_found' in str(d.get('error')) or 'cargo' in str(d.get('error')).lower():
            break
        time.sleep(11)
    time.sleep(11)
print(f'RESULT {pilot}: {len(wrecks)} wrecks here; taken from our kills: {taken}', flush=True)

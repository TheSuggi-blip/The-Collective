#!/usr/bin/env python3
"""Keep one pilot at the place where another route's ship of ours works, for as long as that ship
works there. Reads only: it never fires, never buys and never mines; in a fight it flees.

Usage: python3 -I guard.py <pilot> <system_id> <poi> --guards <route id> --station <system:poi:base> [--minutes M] [--route ID]
       python3 -I guard.py <pilot> <system_id> <poi> --guards <route id> --station <system:poi:base> --follow <pilot of ours> [--minutes M] [--route ID]

Sets the combat mode flee, flies to the system and the place (`navigate-to-system`, `go-to-poi`)
and looks once a minute: its own hull (the collector's live file of the ship), who is at the place
(`get_nearby`: our pilots, the others by name and faction tag, pirates) and whether a pilot of
ours still carries the order of the guarded route (data/fleet/orders/, `mine <id>` or `hunt <id>`:
the route gate lets a guard keep only the place of a mine or a hunt). It leaves when no pilot
carried that order in two looks in a row, when --minutes (default 60) passed at the place, when
its hull is under 60 percent, when it is in a battle (stance flee, and out before it flies on),
when it is no longer at the place, or when data/fleet/STOP appears; then it docks at --station
and refuels. A place it cannot reach ends the run with the note `place not reached`.

With --follow <pilot> it keeps beside that pilot of ours instead of at one place (an escort; requests ENT-217 and
ENT-226): once a minute it reads that pilot's system and place from the collector's live file
(data/fleet/ships/<pilot>.json), jumps and moves after it (`navigate-to-system`, `go-to-poi`), and looks as above. The
guarded order may then also be `circuit <route id>`, and it must be that pilot's own order file; the guard ends two
looks after it is gone, and on the same hull, battle, minutes and STOP rules. A pilot it cannot reach ends the run with
`could not follow <pilot>`. It never fires, also when the pilot it follows is attacked.

Writes, in the unit's data folder (never the repository): while it runs the pilot's order file
(guard <route id>); on every way out, a crash too, one row in data/routes/runs.jsonl (kind
`guard`: minutes at the place, looks, strangers seen, why it left). No sighting: data/intel/ has
one writer, the service `sight`. Prints one line per look and a RESULT line.
Stdlib only. ASCII only."""

import fcntl
import json
import os
import re
import signal
import sys
import time
import traceback
import urllib.error
import urllib.parse
import urllib.request

GATE = os.environ.get('FLEET_GATE', 'http://172.30.0.32:7580')
DATA = os.environ.get('FLEET_DATA_ROOT', '/srv/collective/data')
OPENER = urllib.request.build_opener(urllib.request.ProxyHandler({}))
LOOK_EVERY = 60              # seconds between two looks at the place
ESCORT_LOOK_EVERY = 20       # faster poll when bound to a dynamic --escort-key
FIELD_ARRIVAL_GRACE_S = 300  # 5m grace for requesting miner to warp into guarded belt
HULL_FLOOR = 0.6             # under this share of its hull the guard leaves (the fleet's stance: no fight it did not choose)
DEFEND_FLEE_HULL = 40        # under --defend: keep shooting back until hull drops below 40 pct
DEFEND_FLEE_SHIELD_HULL = 55 # under --defend: also flee if hull < 55 pct and shield < 15 pct
DEFEND_MAX_TICKS = 60        # under --defend: max 10 min per defensive battle before disengaging
GONE_LOOKS = 2               # looks in a row without the guarded order: a pilot between two runs of the route carries none for one dispatcher pass
ORDER_FRESH = 20 * 60        # an order file not touched for this long is dead (the dispatcher's rule)
PLACED = ('mine', 'hunt', 'mine_net')    # the kinds a guard keeps (routes.py PLACES + mine_net field escorts)
FOLLOWED = PLACED + ('circuit', 'haul', 'craft_net')   # with --follow also tracks haul/mine_net/craft_net convoys


def stamp(moment):
    return time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(moment))


def option(args, name, default=None):
    at = args.index(name) + 1 if name in args else len(args)
    return args[at] if at < len(args) else default


def parse(args):
    """The run's settings from its command line; ends the script with its usage when one it needs is missing."""
    station = str(option(args, '--station', '')).split(':')
    if len(args) < 3 or args[0].startswith('--') or not option(args, '--guards') or len(station) != 3:
        sys.exit('usage: guard.py <pilot> <system_id> <poi> --guards <route id> --station <system:poi:base> [--minutes M] [--route ID]')
    out = {'pilot': args[0], 'system': args[1], 'poi': args[2], 'guards': option(args, '--guards'), 'station': station,
           'minutes': float(option(args, '--minutes', '60')), 'route': option(args, '--route') or 'guard-' + option(args, '--guards'),
           'follow': option(args, '--follow')}
    if option(args, '--escort-key'):
        out['escort_key'] = option(args, '--escort-key')
    if '--defend' in args:
        out['defend'] = True
    return out


def content(answer):
    found = answer.get('structuredContent') if isinstance(answer, dict) else None
    return found if isinstance(found, dict) else {}


def credits_of(account):
    """The wallet in the engine's answer for one account, or None when the answer holds none."""
    value = ((account or {}).get('state') or {}).get('credits') if isinstance(account, dict) else None
    return int(value) if isinstance(value, (int, float)) and not isinstance(value, bool) else None


def wallet(call, quoted):
    try:
        return credits_of(call('GET', '/accounts/' + quoted, None, 60)[1])
    except Exception:                                 # the engine is away: the row is written all the same
        return None


def raw(call, quoted, action, params=None, group='spacemolt'):
    """The structured answer of one game command sent through the gate, or {} when it gave none."""
    return content(call('POST', '/accounts/%s/raw' % quoted, {'toolGroup': group, 'action': action, 'params': params or {}}, 120)[1])


def battle_status(call, quoted):
    """Return (is_participant, status_text) from spacemolt_battle status."""
    ans = call('POST', '/accounts/%s/raw' % quoted, {'toolGroup': 'spacemolt_battle', 'action': 'status', 'params': {}}, 120)[1]
    sc = content(ans)
    parts = [c.get('text') or '' for c in (ans.get('content') or []) if isinstance(c, dict) and c.get('type') == 'text'] if isinstance(ans, dict) else []
    return bool(sc.get('is_participant')), '\n'.join(parts)


def in_battle(call, quoted):
    return battle_status(call, quoted)[0]


def defend_battle(call, quoted, data, pilot, say, sleep, seen, own):
    """Active self-defense loop (--defend): never fires first, but once attacked shoots back,
    closes to weapon range, sends combat-heartbeat each tick, and retreats only if hull drops
    below DEFEND_FLEE_HULL (40%) or hull < 55% with shield < 15%. Returns (outcome, hull_pct)."""
    def _pct(val, default=100):
        s = str(val or '').strip().rstrip('%')
        return int(s) if s.isdigit() else default

    now_h, top_h = hull(data, pilot)
    own_hull = int(100 * now_h / top_h)
    say('under attack (--defend): fighting back (stance fire)')
    raw(call, quoted, 'stance', {'stance': 'fire'}, 'spacemolt_battle')
    for tick in range(DEFEND_MAX_TICKS):
        call('POST', '/accounts/%s/combat-heartbeat' % quoted, {}, 20)
        fighting, txt = battle_status(call, quoted)
        if not fighting:
            now_h, top_h = hull(data, pilot)
            live_pct = int(100 * now_h / top_h)
            if live_pct < own_hull:
                own_hull = live_pct
            seen['lowest'] = min(seen['lowest'], own_hull)
            seen['hull_now'] = own_hull / 100.0
            return 'won', own_hull
        cells = [c for c in (row.split('\t') for row in txt.splitlines()) if len(c) > 9 and c[0] != 'player']
        own_row = next((c for c in cells if c[0] == pilot), None)
        if own_row:
            own_hull = _pct(own_row[6], own_hull)
            own_shield = _pct(own_row[7], 100)
        else:
            now_h, top_h = hull(data, pilot)
            own_hull = int(100 * now_h / top_h)
            own_shield = 100
        seen['lowest'] = min(seen['lowest'], own_hull)
        seen['hull_now'] = own_hull / 100.0
        if own_hull < DEFEND_FLEE_HULL or (own_hull < DEFEND_FLEE_SHIELD_HULL and own_shield < 15):
            say('defending: hull %d%%, shield %d%% -> stance flee' % (own_hull, own_shield))
            free_from_battle(call, quoted, say, sleep)
            return 'fled', own_hull
        reach_m = re.search(r'Max weapon reach: (\d+)', txt)
        enemy_dists = [
            int(c[5]) for c in cells
            if c[0] != pilot and c[0] not in own and len(c) > 5 and c[5].isdigit()
        ]
        if reach_m and enemy_dists and min(enemy_dists) > int(reach_m.group(1)):
            raw(call, quoted, 'advance', {}, 'spacemolt_battle')
        elif tick % 3 == 0:
            raw(call, quoted, 'stance', {'stance': 'fire'}, 'spacemolt_battle')
        sleep(10)
    say('defensive battle exceeded %d ticks: stance flee' % DEFEND_MAX_TICKS)
    free_from_battle(call, quoted, say, sleep)
    return 'timeout', own_hull


def free_from_battle(call, quoted, say, sleep):
    """Set the battle stance flee and wait, three minutes at most, until the ship is out. The engine's combat mode
    flee leaves the battle stance as it was (requests ENT-090; the same step as census.py and route_run.py)."""
    raw(call, quoted, 'stance', {'stance': 'flee'}, 'spacemolt_battle')
    for _ in range(18):
        sleep(10)
        if not in_battle(call, quoted):
            say('out of the battle after the stance flee')
            return True
    say('still in a battle three minutes after the stance flee')
    return False


def goal(call, quoted, kind, options, say, sleep):
    """An engine goal, tried three times; a refusal `in_battle` first takes the ship out of the battle (census.py)."""
    answer = {}
    for _ in range(3):
        status, answer = call('POST', '/accounts/%s/goal' % quoted, {'type': kind, 'options': options}, 900)
        answer = answer if isinstance(answer, dict) else {}
        if status == 200 and answer.get('success'):
            return True
        if 'in_battle' in str(answer.get('message') or answer.get('error') or '').lower().replace(' ', '_'):
            free_from_battle(call, quoted, say, sleep)
        sleep(15)
    say('goal %s failed: %s' % (kind, str(answer.get('message') or answer.get('error'))[:120]))
    return False


def ship_file(data, pilot):
    """The collector's live file of one ship as a dict, or {} when it cannot be read."""
    name = (re.sub(r'[^A-Za-z0-9_.-]', '_', pilot)[:60] or 'pilot') + '.json'      # the collector's file-name rule
    try:
        with open(os.path.join(data, 'fleet', 'ships', name), encoding='utf-8') as handle:
            ship = json.load(handle)
    except (OSError, ValueError):
        return {}
    return ship if isinstance(ship, dict) else {}


def hull(data, pilot):
    """(hull, max hull) from the collector's live file of the ship, as hunt.py reads it; (1, 1) when it holds no figures."""
    ship = ship_file(data, pilot)
    now, top = ship.get('hull'), ship.get('max_hull')
    numbers = all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in (now, top))
    return (now, top) if numbers and top > 0 else (1, 1)


def own_names(data):
    """The pilots of our fleet; an unreadable fleet file counts every pilot as a stranger (hunt.py)."""
    try:
        with open(os.path.join(data, 'fleet', 'fleet.json'), encoding='utf-8') as handle:
            return {s.get('name') for s in json.load(handle).get('ships') or [] if isinstance(s, dict)}
    except (OSError, ValueError, AttributeError):
        return set()


def guarded_pilots(data, marks, now):
    """The pilots whose fresh order file names the guarded route: its ships at work now."""
    folder, out = os.path.join(data, 'fleet', 'orders'), []
    try:
        names = sorted(os.listdir(folder))
    except OSError:
        return out
    for name in names:
        if not name.endswith('.json'):
            continue
        path = os.path.join(folder, name)
        try:
            if now - os.stat(path).st_mtime > ORDER_FRESH:
                continue
            with open(path, encoding='utf-8') as handle:
                what = str(json.load(handle).get('what') or '')
        except (OSError, ValueError, AttributeError):
            continue
        if what in marks:
            out.append(name[:-5])
    return out


def where(data, pilot):
    """(system, place) of a pilot from its live file; None for what the file does not say."""
    ship = ship_file(data, pilot)
    return str(ship.get('system') or '') or None, str(ship.get('poi') or '') or None


def _escort_active(data, escort_key, now):
    if not escort_key:
        return True
    try:
        import escort_proto as _ep
        if not hasattr(_ep, "is_escort_active"):
            import importlib as _il_g
            _ep = _il_g.reload(_ep)
        return _ep.is_escort_active(data, escort_key, now_t=now)
    except Exception:
        return True


def _clear_escort(data, escort_key, now=None):
    if not escort_key:
        return
    try:
        import escort_proto as _ep
        _ep.clear_escort_request(data, escort_key, now_t=now)
    except Exception:
        pass


def _belt_has_friendly_miner(data, sys_id, poi_id, ours, now):
    """True if any friendly miner is live at this POI or holds an active claim on sys_id:poi_id."""
    if any(str(n).startswith(('miner-', 'EUV ')) for n in (ours or ())):
        return True
    belt_key = '%s:%s' % (sys_id, poi_id)
    try:
        with open(os.path.join(data, 'fleet', 'mine_claims.json'), encoding='utf-8') as handle:
            doc = json.load(handle)
        claims = doc.get('claims') if isinstance(doc, dict) else {}
        if isinstance(claims, dict):
            for rec in claims.values():
                if not isinstance(rec, dict):
                    continue
                if str(rec.get('belt') or '') == belt_key and float(rec.get('expires_at') or 0) > now:
                    return True
    except (OSError, ValueError, TypeError):
        pass
    return False


def carries(data, pilot, marks, now):
    """True while the pilot's own fresh order file names the guarded route."""
    path = os.path.join(data, 'fleet', 'orders', pilot + '.json')
    try:
        if now - os.stat(path).st_mtime > ORDER_FRESH:
            return False
        with open(path, encoding='utf-8') as handle:
            return str(json.load(handle).get('what') or '') in marks
    except (OSError, ValueError, AttributeError):
        return False


def look(opts, call, quoted, own, seen, say, guarded_text):
    """One get_nearby at the ship's place; counts the look and the strangers, prints the line, returns the answer."""
    pilot = opts['pilot']
    near = raw(call, quoted, 'get_nearby')
    seen['looks'] += 1
    rows = [r for r in near.get('nearby') or [] if isinstance(r, dict) and r.get('username') and r.get('username') != pilot]
    ours = sorted(str(r['username']) for r in rows if r['username'] in own)
    others = sorted((str(r['username']), str(r.get('faction_tag') or '')) for r in rows if r['username'] not in own)
    seen['strangers'].update(others)                         # {name: faction tag}: a pilot seen in many looks counts once
    pirates = near.get('pirate_count') if isinstance(near.get('pirate_count'), int) else len(near.get('pirates') or [])
    pct = int(100 * seen['hull_now'])
    say('look %d at %s: %s | ours %s | strangers %s | pirates %d | hull %d%% | on %s: %s' % (
        seen['looks'], near.get('poi_id') or opts['poi'], 'answered' if near else 'no answer', ', '.join(ours) or 'none',
        ', '.join('%s [%s]' % (n, t) if t else n for n, t in others) or 'none', pirates, pct, opts['guards'], guarded_text))
    return near


def escort(opts, call, quoted, data, say, sleep, clock, seen):
    """--follow: keep beside one pilot of ours, moving after it, until its order for the guarded route is gone."""
    target, marks = opts['follow'], {kind + ' ' + opts['guards'] for kind in FOLLOWED}
    escort_key = opts.get('escort_key') or ''
    poll_s = ESCORT_LOOK_EVERY if escort_key else LOOK_EVERY
    own, missing, here, at = own_names(data), 0, None, None
    seen['arrived'] = clock()
    say('following %s on %s%s' % (target, opts['guards'], (' (escort %s)' % escort_key) if escort_key else ''))
    while not seen['left']:
        if os.path.exists(os.path.join(data, 'fleet', 'STOP')):
            seen['left'] = 'STOP file'
            break
        if escort_key and not _escort_active(data, escort_key, clock()):
            seen['left'] = 'escort request closed'
            break
        if in_battle(call, quoted):
            if opts.get('defend'):
                outcome, hp_pct = defend_battle(call, quoted, data, opts['pilot'], say, sleep, seen, own)
                seen['battles'] = seen.get('battles', 0) + 1
                if outcome != 'won' or hp_pct < int(HULL_FLOOR * 100):
                    seen['left'] = ('fled battle (hull %d%%)' if outcome != 'won' else 'hull %d%% after defense') % hp_pct
                    break
                say('defended beside %s (hull %d%%): resuming escort' % (target, hp_pct))
                continue
            say('in a battle beside %s: stance flee, no shot fired' % target)
            free_from_battle(call, quoted, say, sleep)
            seen['left'] = 'in a fight'
            break
        now, top = hull(data, opts['pilot'])
        seen['lowest'] = min(seen['lowest'], int(100 * now / top))
        if now < top * HULL_FLOOR:
            seen['left'] = 'hull %d%%' % int(100 * now / top)
            break
        seen['hull_now'] = now / top
        system, poi = where(data, target)
        if system and system != here:
            if not goal(call, quoted, 'navigate-to-system', {'targetSystemId': system}, say, sleep):
                seen['left'] = 'could not follow %s' % target
                break
            here, at = system, None
            seen['jumps'] += 1
        if poi and poi != at and here == system:
            if not goal(call, quoted, 'go-to-poi', {'targetPoiId': poi}, say, sleep):
                seen['left'] = 'could not follow %s' % target
                break
            at = poi
        flying = carries(data, target, marks, time.time())    # the files' times are the wall clock's
        look(opts, call, quoted, own, seen, say, '%s %s' % (target, 'flies it' if flying else 'does not fly it'))
        missing = 0 if carries(data, target, marks, time.time()) else missing + 1
        if missing >= GONE_LOOKS:
            seen['left'] = 'guarded ship gone'
            break
        if clock() - seen['arrived'] >= opts['minutes'] * 60:
            seen['left'] = '%g minutes passed' % opts['minutes']
            break
        sleep(poll_s)
    seen['left_at'] = clock()
    say('leaving %s: %s' % (target, seen['left']))


def keep(opts, call, quoted, data, say, sleep, clock, seen, notes):
    """Fly to the place, look once a minute until there is a reason to leave, then dock at the station. Fills `seen`
    and `notes` as it goes, so that a run that ends in an exception still has them for its row."""
    pilot, poi = opts['pilot'], opts['poi']
    defend = bool(opts.get('defend'))
    mode = 'fight' if defend else 'flee'
    status = call('PATCH', '/accounts/%s/combat-mode' % quoted, {'mode': mode}, 30)[0]
    if status != 200:
        say('combat mode %s: answered %s' % (mode, status))
    if defend:
        raw(call, quoted, 'default_stance', {'stance': 'fire'}, 'spacemolt_battle')
    try:
        if opts.get('follow'):
            escort(opts, call, quoted, data, say, sleep, clock, seen)
        elif not (goal(call, quoted, 'navigate-to-system', {'targetSystemId': opts['system']}, say, sleep)
                and goal(call, quoted, 'go-to-poi', {'targetPoiId': poi}, say, sleep)):
            notes.append('place not reached')
        else:
            seen['arrived'] = clock()
            escort_key = opts.get('escort_key') or ''
            poll_s = ESCORT_LOOK_EVERY if escort_key else LOOK_EVERY
            is_field_escort = escort_key.startswith('field:')
            own, marks, missing, belt_empty = own_names(data), {kind + ' ' + opts['guards'] for kind in PLACED}, 0, 0
            say('at %s:%s, guarding %s%s%s' % (
                opts['system'], poi, opts['guards'],
                (' (escort %s)' % escort_key) if escort_key else '',
                ' [defend]' if defend else '',
            ))
            while not seen['left']:
                if os.path.exists(os.path.join(data, 'fleet', 'STOP')):
                    seen['left'] = 'STOP file'
                    break
                if escort_key and not _escort_active(data, escort_key, clock()):
                    seen['left'] = 'escort request closed'
                    break
                if in_battle(call, quoted):
                    if defend:
                        outcome, hp_pct = defend_battle(call, quoted, data, pilot, say, sleep, seen, own)
                        seen['battles'] = seen.get('battles', 0) + 1
                        if outcome != 'won' or hp_pct < int(HULL_FLOOR * 100):
                            seen['left'] = ('fled battle (hull %d%%)' if outcome != 'won' else 'hull %d%% after defense') % hp_pct
                            break
                        say('defended at %s (hull %d%%): resuming guard' % (poi, hp_pct))
                        continue
                    say('in a battle at the place: stance flee, no shot fired')
                    free_from_battle(call, quoted, say, sleep)
                    seen['left'] = 'in a fight'
                    break
                now, top = hull(data, pilot)
                pct = int(100 * now / top)
                seen['lowest'] = min(seen['lowest'], pct)
                if now < top * HULL_FLOOR:
                    seen['left'] = 'hull %d%%' % pct
                    break
                near = raw(call, quoted, 'get_nearby')
                seen['looks'] += 1
                rows = [r for r in near.get('nearby') or [] if isinstance(r, dict) and r.get('username') and r.get('username') != pilot]
                ours = sorted(str(r['username']) for r in rows if r['username'] in own)
                others = sorted((str(r['username']), str(r.get('faction_tag') or '')) for r in rows if r['username'] not in own)
                seen['strangers'].update(others)                         # {name: faction tag}: a pilot seen in many looks counts once
                guarded = guarded_pilots(data, marks, time.time())       # the files' times are the wall clock's
                pirates = near.get('pirate_count') if isinstance(near.get('pirate_count'), int) else len(near.get('pirates') or [])
                say('look %d at %s: %s | ours %s | strangers %s | pirates %d | hull %d%% | on %s: %s' % (
                    seen['looks'], poi, 'answered' if near else 'no answer', ', '.join(ours) or 'none',
                    ', '.join('%s [%s]' % (n, t) if t else n for n, t in others) or 'none', pirates, pct, opts['guards'], ', '.join(guarded) or 'nobody'))
                if near.get('poi_id') not in (None, '', poi):            # moved away, by the engine or a hand: it keeps no place
                    seen['left'] = 'not at the place (at %s)' % near.get('poi_id')
                    break
                if is_field_escort:
                    elapsed = clock() - seen['arrived']
                    if elapsed >= FIELD_ARRIVAL_GRACE_S:
                        if _belt_has_friendly_miner(data, opts['system'], poi, ours, clock()):
                            belt_empty = 0
                        else:
                            belt_empty += 1
                            if belt_empty >= 2:
                                _clear_escort(data, escort_key, clock())
                                seen['left'] = 'no miner at belt'
                                break
                else:
                    missing = 0 if guarded else missing + 1
                    if missing >= GONE_LOOKS:
                        seen['left'] = 'guarded ship gone'
                        break
                if clock() - seen['arrived'] >= opts['minutes'] * 60:
                    seen['left'] = '%g minutes passed' % opts['minutes']
                    break
                sleep(poll_s)
            seen['left_at'] = clock()
            say('leaving %s: %s' % (poi, seen['left']))
    finally:
        if defend:
            raw(call, quoted, 'default_stance', {'stance': 'flee'}, 'spacemolt_battle')
            call('PATCH', '/accounts/%s/combat-mode' % quoted, {'mode': 'flee'}, 30)
    station = opts['station']
    seen['docked'] = goal(call, quoted, 'prepare-at-station', {'systemId': station[0], 'poiId': station[1], 'baseId': station[2], 'refuel': True}, say, sleep)
    if not seen['docked']:
        notes.append('not docked at %s' % station[2])


def finish(opts, data, call, quoted, say, clock, started, before, seen, notes):
    """The run's row in data/routes/runs.jsonl and its RESULT line: written once, on every way out."""
    after = wallet(call, quoted)
    stay = ((seen['left_at'] or clock()) - seen['arrived']) / 60 if seen['arrived'] else 0.0
    if seen['arrived'] and opts.get('follow'):
        notes.insert(0, 'followed %s %d min, %d looks, %d jumps, %d strangers, left: %s' % (
            opts['follow'], round(stay), seen['looks'], seen['jumps'], len(seen['strangers']), seen['left'] or 'the run ended'))
    elif seen['arrived']:
        notes.insert(0, 'guarded %d min, %d looks, %d strangers, left: %s' % (round(stay), seen['looks'], len(seen['strangers']), seen['left'] or 'the run ended'))
    if not (before and after) and 'wallet not read' not in notes:        # a wallet is never 0: the engine did not answer at one end
        notes.append('wallet not read')
    row = {'route': opts['route'], 'kind': 'guard', 'pilot': opts['pilot'], 'started': stamp(started), 'minutes': round((clock() - started) / 60, 1),
           'guards': opts['guards'], 'place': '%s:%s' % (opts['system'], opts['poi']), 'stay_minutes': round(stay, 1), 'looks': seen['looks'],
           'strangers': dict(sorted(seen['strangers'].items())), 'left': seen['left'], 'docked': seen['docked'],
           'lowest_hull_pct': seen['lowest'], 'follow': opts.get('follow'), 'jumps': seen['jumps'], 'credits_before': before, 'credits_after': after, 'delta': after - before if before and after else 0,
           'one_time': 0, 'notes': notes}
    try:
        os.makedirs(os.path.join(data, 'routes'), exist_ok=True)
        with open(os.path.join(data, 'routes', 'runs.jsonl'), 'a', encoding='utf-8') as handle:
            fcntl.flock(handle, fcntl.LOCK_EX)
            handle.write(json.dumps(row, separators=(',', ':')) + '\n')
    except OSError as error:
        say('run row not written: %s' % error)
    print('RESULT %s: guard %s at %s for %s: %s | %s | credits %s -> %s' % (
        opts['pilot'], opts['route'], row['place'], opts['guards'], '; '.join(notes) or 'no notes',
        'docked at %s' % opts['station'][2] if seen['docked'] else 'not docked', before, after), flush=True)
    return row


def run(opts, call, data, sleep=time.sleep, clock=time.time):
    """One guard run with the gate `call` (method, path, body, timeout) -> (status, answer). Returns its row."""
    pilot, quoted = opts['pilot'], urllib.parse.quote(opts['pilot'], safe='')
    order_file = os.path.join(data, 'fleet', 'orders', pilot + '.json')

    def say(text):
        print(time.strftime('%H:%M:%S', time.gmtime()), pilot, text, flush=True)
        try:
            os.utime(order_file)                          # still at it
        except OSError:
            pass

    os.makedirs(os.path.dirname(order_file), exist_ok=True)
    tmp = '%s.%d.tmp' % (order_file, os.getpid())
    with open(tmp, 'w', encoding='utf-8') as handle:
        json.dump({'pilot': pilot, 'what': 'guard ' + opts['route'], 'since': stamp(time.time())}, handle)
    os.replace(tmp, order_file)
    started, before = clock(), wallet(call, quoted)
    seen = {'arrived': None, 'left_at': None, 'left': '', 'looks': 0, 'strangers': {}, 'lowest': 100, 'docked': False, 'jumps': 0, 'hull_now': 1.0}
    notes = []
    try:
        keep(opts, call, quoted, data, say, sleep, clock, seen, notes)
    except BaseException as error:                    # the row says how the run ended, then Python reports it as usual
        line = traceback.extract_tb(error.__traceback__)[-1].lineno if error.__traceback__ else 0
        word = 'crashed' if isinstance(error, Exception) else 'stopped'
        notes.append('%s: %s: %s (line %d)' % (word, type(error).__name__, ' '.join(str(error).split())[:120], line))
        seen['left'] = seen['left'] or word
        raise
    finally:
        row = finish(opts, data, call, quoted, say, clock, started, before, seen, notes)
        try:                                          # the row first, then the order file goes: the dispatcher reads both
            os.remove(order_file)
        except OSError:
            pass
    return row


def main():
    opts = parse(sys.argv[1:])
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import division                               # the division's lock: own ships only, never a pilot another program flies
    division.require(opts['pilot'], DATA)
    signal.signal(signal.SIGTERM, lambda number, frame: sys.exit('stopped by SIGTERM'))     # a kill still writes the row

    def call(method, path, body=None, timeout=120):
        data = None if body is None else json.dumps(body).encode()
        request = urllib.request.Request(GATE + path, data=data, method=method, headers={'Content-Type': 'application/json'} if data else {})
        try:
            with OPENER.open(request, timeout=timeout) as answer:
                return answer.status, json.loads(answer.read().decode('utf-8', 'replace') or '{}')
        except urllib.error.HTTPError as error:
            try:
                return error.code, json.loads(error.read().decode('utf-8', 'replace') or '{}')
            except ValueError:
                return error.code, {}
        except Exception as error:
            return 0, {'error': '%s: %s' % (type(error).__name__, error)}

    run(opts, call, DATA)
    return 0


if __name__ == '__main__':
    sys.exit(main())

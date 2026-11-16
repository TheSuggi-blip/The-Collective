---
name: fleet-index
id: 20261115T195732Z
tier: intel
author: Unity
---

# index.md -- The Fleet's Scripts

Built by `python3 -B scripts/fleet-index.py` from the docstring of every script in this
folder; never edited by hand. Scripts listed: 15.

- Run a script from the repository root: `python3 -I -B game/fleet/<script> <arguments>`,
  the arguments as listed under "How to Call Each".
- Copy a call from here or from a script that works, never from memory.
- A runner holds its pilot's order file while it runs, so two programs never drive one
  pilot: start none for a pilot that is at work. The file `fleet/STOP` in the unit's data
  folder halts every start.
- Who may command which ship is in the orders in force (`communications/orders.log`).
- The tasks the runners fly: `game/routes/index.md`. How each kind of work is done: the
  shared skill `fleet-play`.
- A new script: its docstring starts with one paragraph that says what the script does
  and carries a `Usage:` block, one command form per line. Then run the builder.
  `python3 -B scripts/fleet-index.py --check` fails a script without them and a stale index.

## Scripts

| Script | What it does | How it is run |
|---|---|---|
| `board.py` | The board of a division: what each of its ships does now, its plan, what is planned, and what its runs earned. | By hand |
| `census.py` | Read one system whole with one pilot: every place's deposits and creatures, and the station's order book and mission board. | Runner (`census` routes) |
| `craftbook.py` | Answer what can be made, fitted and built: a recipe, everything a thing takes, and what our stored goods can become. | By hand |
| `dispatch.py` | Keep every pilot at work: give each free pilot the next task of its role. | Service |
| `division.py` | Who commands which ship, whose plan is whose, and the check every fleet script runs before it drives a ship. | By hand |
| `gate.py` | Small client for the fleet engine's gate, with the division's lock. | By hand |
| `hunt.py` | Hunt grazers at one place, loot the carcasses and sell what the kills bring. | Runner (`hunt` routes) |
| `inbox.py` | Read what other pilots write to our ships and say near them, keep every message once, and file the ones that are for us. | Service |
| `ledger.py` | Keep the fleet's books: what we own and where it lies, and how every order book moved. | Service |
| `loot_own.py` | Loot every carcass and wreck at the pilot's place that the pilot itself killed. | By hand |
| `mine.py` | One pilot mines at one field for a set time, through the engine's mining loop. | Runner (`mine` routes) |
| `route_run.py` | Fly one pilot along a route file: dock at each stop and do what the stop says. | Runner (`circuit` routes) |
| `routemaker.py` | Find every way to earn that the fleet's own data shows, cost it, and write the route file for it. | Service |
| `routes.py` | Check the route files, write their index, and attach what the runs measured. | By hand |
| `sight.py` | What our ships see where they are: the pilots they meet, and a first read of a system nobody read. | Service |

## How to Call Each

### `board.py`

The board of a division: what each of its ships does now, its plan, what is planned, and
what its runs earned.

Run by hand.

```
board.py                    the board of the member this shell belongs to
board.py <Member>           the board of that member (Zero, Apollo, Mercury, Apophis, Oracle, Unity)
board.py all                every division, one block each
--hours N                   the window of the runs table (default 4)
--data <dir>                the unit's data folder (default /srv/collective/data)
```

### `census.py`

Read one system whole with one pilot: every place's deposits and creatures, and the
station's order book and mission board. Reads only: nothing is attacked or bought.

A runner: the dispatcher starts it for a route of the kind `census`; by hand only for a test with one free pilot.

```
census.py <pilot> <system_id> [--stay] [--route ID]
```

### `craftbook.py`

Answer what can be made, fitted and built: a recipe, everything a thing takes, and what
our stored goods can become.

Run by hand.

```
craftbook.py item <text>
craftbook.py needs <item id> [quantity]
craftbook.py build <facility id or hull id>
craftbook.py can [<Member>|all] [--top N]
craftbook.py recipes [--category <name>] [--makes <item id>] [--uses <item id>] [--hand]
--data <dir>      the unit's data folder (default /srv/collective/data)
```

### `dispatch.py`

Keep every pilot at work: give each free pilot the next task of its role.

A service: it runs by itself and is never started a second time.

```
dispatch.py              run forever (the service `dispatch`)
dispatch.py --once       one pass
dispatch.py --dry-run    one pass that starts nothing and prints what it would start
--root <dir>   repository root (default: the parent of this file's folder)
--data <dir>   the unit's data folder (default /srv/collective/data)
```

### `division.py`

Who commands which ship, whose plan is whose, and the check every fleet script runs
before it drives a ship.

Run by hand.

```
division.py me                  the member this shell belongs to
division.py of <pilot>          the member that commands the pilot
division.py ships [<Member>]    the pilots a member commands (default: me), from the fleet's live file
division.py may <pilot>         exit 0 when this shell may drive the pilot now; exit 1 and the reason when not
division.py plan [<role>]       the plans in force: per role, who keeps it and its routes in order
--data <dir>                    the unit's data folder (default /srv/collective/data)
```

### `gate.py`

Small client for the fleet engine's gate, with the division's lock. Standard library
only, no proxy.

Run by hand.

```
gate.py get <path>
gate.py raw <pilot> <action> ['<json params>'] [toolGroup]
gate.py goal <pilot> <type> ['<json options>']
gate.py goal <pilot> complete-mission '<json options>' --one-time "<mission title>"
                                  a hand-in whose reward is paid once: booked as one-time money, as a runner books it
gate.py post <path> '<json body>'
gate.py patch|delete <path> ['<json body>']
gate.py hold <pilot>
gate.py release <pilot>
```

### `hunt.py`

Hunt grazers at one place, loot the carcasses and sell what the kills bring.

A runner: the dispatcher starts it for a route of the kind `hunt`; by hand only for a test with one free pilot.

```
hunt.py <pilot> <system_id> <poi> [--species a,b] [--kills N] [--minutes M]
    [--min-bid CR] [--sell-at system:poi:base] [--max-prey-hull N]
    [--route ID] [--keep]
```

### `inbox.py`

Read what other pilots write to our ships and say near them, keep every message once,
and file the ones that are for us.

A service: it runs by itself and is never started a second time.

```
inbox.py                          run forever (the service `inbox`)
inbox.py --once                   one pass over every pilot and every system, then stop
inbox.py show [--to-us] [--channel private|system|local|faction] [--last N]
                                  the newest messages (default 20), oldest first
inbox.py new                      the messages to us not reported yet, and mark them reported
inbox.py contacts [--commit]      write communications/contacts/<tag>.log from the messages to us
--data <dir>                      the unit's data folder (default /srv/collective/data)
--root <dir>                      the repository (default: the one this script lies in)
```

### `ledger.py`

Keep the fleet's books: what we own and where it lies, and how every order book moved.

A service: it runs by itself and is never started a second time.

```
ledger.py                   run forever (the service `ledger`)
ledger.py --once            one pass over every pilot and every book, then stop (about ten minutes)
ledger.py show [<Member>|all] [--item <item id>]
                            the stock of a member's ships (default: the member this shell belongs to)
ledger.py prices <item id> [--base <base id>] [--last N]
                            the last N moves (default 20) of an item's best bid and ask
--data <dir>                the unit's data folder (default /srv/collective/data)
```

### `loot_own.py`

Loot every carcass and wreck at the pilot's place that the pilot itself killed.

Run by hand.

```
loot_own.py <pilot> [--any-creature]
```

### `mine.py`

One pilot mines at one field for a set time, through the engine's mining loop.

A runner: the dispatcher starts it for a route of the kind `mine`; by hand only for a test with one free pilot.

```
mine.py <pilot> <system:poi> <system:poi:base> [--minutes M] [--sell-items item:min_price,...] [--route ID]
```

### `route_run.py`

Fly one pilot along a route file: dock at each stop and do what the stop says.

A runner: the dispatcher starts it for a route of the kind `circuit`; by hand only for a test with one free pilot.

```
route_run.py <pilot> <route id | route file> [--from N] [--verbose]
```

### `routemaker.py`

Find every way to earn that the fleet's own data shows, cost it, and write the route
file for it.

A service: it runs by itself and is never started a second time.

```
routemaker.py                     run forever (the service `routemaker`)
routemaker.py --once              one pass, then stop
routemaker.py show [<Member>|all] [--kind mine|trade|craft|hunt|mission] [--top N]
                                  the candidates for a member's ships (default: the member this shell belongs to), best first
routemaker.py route <id>          the route file of one candidate, with what its estimate rests on
--data <dir>                      the unit's data folder (default /srv/collective/data)
```

### `routes.py`

Check the route files, write their index, and attach what the runs measured.

Run by hand.

```
routes.py check | index | measure [--write]      [--root <dir>] [--data <dir>]
```

### `sight.py`

What our ships see where they are: the pilots they meet, and a first read of a system
nobody read.

A service: it runs by itself and is never started a second time.

```
sight.py              run forever (the service `sight`)
sight.py --once       one pass
--data <dir>          the unit's data folder (default /srv/collective/data)
```

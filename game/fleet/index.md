---
name: fleet-index
id: 20261115T195732Z
tier: intel
author: Unity
---

# index.md -- The Fleet's Scripts

Built by `python3 -B scripts/fleet-index.py` from the docstring of every script in this
folder; never edited by hand. Scripts listed: 9.

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
| `census.py` | Read one system whole with one pilot: every place's deposits and creatures, and the station's order book and mission board. | Runner (`census` routes) |
| `dispatch.py` | Keep every pilot at work: give each free pilot the next task of its role. | Service |
| `gate.py` | Small client for the fleet engine's gate. | By hand |
| `hunt.py` | Hunt grazers at one place, loot the carcasses and sell what the kills bring. | Runner (`hunt` routes) |
| `loot_own.py` | Loot every carcass and wreck at the pilot's place that the pilot itself killed. | By hand |
| `mine.py` | One pilot mines at one field for a set time, through the engine's mining loop. | Runner (`mine` routes) |
| `route_run.py` | Fly one pilot along a route file: dock at each stop and do what the stop says. | Runner (`circuit` routes) |
| `routes.py` | Check the route files, write their index, and attach what the runs measured. | By hand |
| `sight.py` | What our ships see where they are: the pilots they meet, and a first read of a system nobody read. | Service |

## How to Call Each

### `census.py`

Read one system whole with one pilot: every place's deposits and creatures, and the
station's order book and mission board. Reads only: nothing is attacked or bought.

A runner: the dispatcher starts it for a route of the kind `census`; by hand only for a test with one free pilot.

```
census.py <pilot> <system_id> [--stay] [--route ID]
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

### `gate.py`

Small client for the fleet engine's gate. Standard library only, no proxy.

Run by hand.

```
gate.py get <path>
gate.py post <path> '<json body>'
gate.py patch|delete <path> ['<json body>']
gate.py raw <pilot> <action> ['<json params>'] [toolGroup]
gate.py goal <pilot> <type> ['<json options>']
```

### `hunt.py`

Hunt grazers at one place, loot the carcasses and sell what the kills bring.

A runner: the dispatcher starts it for a route of the kind `hunt`; by hand only for a test with one free pilot.

```
hunt.py <pilot> <system_id> <poi> [--species a,b] [--kills N] [--minutes M]
    [--min-bid CR] [--sell-at system:poi:base] [--max-prey-hull N]
    [--route ID] [--keep]
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
mine.py <pilot> <system:poi> <system:poi:base> [--minutes M] [--sell] [--route ID]
```

### `route_run.py`

Fly one pilot along a route file: dock at each stop and do what the stop says.

A runner: the dispatcher starts it for a route of the kind `circuit`; by hand only for a test with one free pilot.

```
route_run.py <pilot> <route id | route file> [--from N] [--verbose]
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

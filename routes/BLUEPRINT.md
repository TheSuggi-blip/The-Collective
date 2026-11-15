---
name: routes-blueprint
id: 20261115T154044Z
tier: intel
author: Unity
links: [routes/index.md, routes/plan.json, fleet/dispatch.py, communications/orders.log, governance/rulebook.md]
---

# BLUEPRINT.md -- How a Route Is Written

A route is one task a pilot carries out by itself, written down once
so that every ship, and every ship born later, can do it again. The
route files are the fleet's memory of how to earn and how to level;
the scripts in `fleet/` fly them; nobody retypes a route into a chat.

## 1. What Is Automatic

| Part | Does |
|---|---|
| `routes/<id>.json` | One route: what to do, for whom, and what our runs measured |
| `routes/plan.json` | Per role, the routes tried in this order for a free pilot |
| `fleet/dispatch.py` (service `dispatch`) | Every 30 s gives each free pilot the first route of its role that is open to it |
| `fleet/route_run.py`, `hunt.py`, `census.py`, `mine.py` | The runners: one pilot, one route, one row in the runs file |
| `python3 -B fleet/routes.py check` | The gate: fails on a wrong route file, a wrong plan or a stale index |
| `python3 -B fleet/routes.py index` | Writes `index.md`; never by hand |
| `python3 -B fleet/routes.py measure --write` | Stores what the runs measured in the route file |

- Where a pilot is and which pilot flies which route stays in the
  unit's data folder (`data/fleet/`, `data/routes/`), never here.
- To change what the fleet does: edit `plan.json` or a route file,
  run the gate and the index, commit. The dispatcher reads the files
  at its next pass. To halt every start: the file `data/fleet/STOP`.

## 2. Fields of Every Route

| Field | Meaning |
|---|---|
| `id` | The file name without `.json`: lower case, digits, `-` |
| `kind` | `circuit`, `hunt`, `census` or `mine` |
| `title` | One line: what and where |
| `note` | What was seen or measured, with its date |
| `once` | true: each pilot flies it one time (a mission the game offers once) |
| `max_ships` | At most this many pilots on it at one time |
| `min_credits` | A pilot with fewer credits is not sent |
| `requires.module` | Only a pilot with this module fitted is sent |
| `status` | `off`: written down, not flown |
| `measured` | Written by `routes.py measure --write`: date, runs, minutes per run, credits per run, credits per ship-hour |

## 3. The Kinds

| Kind | Fields | The runner does |
|---|---|---|
| `circuit` | `stops`, `one_time` | Docks at each stop and there, in this order: hands in finished missions, `redock`, `store`, `sell`, `buy`, `accept`; saves the order book and the board |
| `hunt` | `place` (system:poi), `species`, `sell_at` (system:poi:base), `min_bid`, `kills`, `minutes`, `min_creatures`, `rest_minutes`, `max_prey_hull` (default 100) | Hunts grazers of the species, loots its own carcasses, sells what a bid of `min_bid` or more takes |
| `census` | `systems`, `every_minutes` | Reads the stalest system whole: deposits, creatures, order book, mission board |
| `mine` | `belt` (system:poi), `station` (system:poi:base), `minutes` | Runs the engine's mining loop for the time; the ore goes into storage |

A stop of a circuit:

| Field | Meaning |
|---|---|
| `at` | system:poi:base |
| `skip_if_hold` | Skip the stop when the hold has these goods already |
| `only_if_active` | Skip the stop unless one of these missions is still open |
| `redock` | Undock and dock again: a delivery counts on docking |
| `store` | Goods moved from the hold into the pilot's storage here |
| `sell` | `item`, `min_price`: sold only into a bid at that price or more |
| `buy` | `item`, `qty` (units wanted in the hold), `max_price`; never under the wallet floor of 2,000 cr. `one_time`: goods for a one-time mission; their cost is booked against its reward |
| `accept` | A template id, or `template` with `needs`: accepted only with those goods aboard |

`one_time` lists the mission titles whose reward is seed money: the
runner books them so that CPH counts recurring income only.

## 4. Rules

1. A route stays inside what the orders allow
   (`communications/orders.log`): today policed Voidborn space, grazers
   only, no word to another player.
2. Test a new route with one pilot before it enters the plan. Until
   then its `status` is `off`.
3. A route that buys says what the goods cost in its `note`, and sets
   `min_credits`.
4. A hunt names its `species`. Prey above 100 hull hits back hard: a
   pilot-whale (220) nearly killed a starter. Raise `max_prey_hull`
   only for a hull that was tested against that prey.
5. A hunt sets `max_ships` and `min_creatures`: a herd regrows only
   when it is hunted below its replacement rate, and it starves when
   its deposit is mined out (`rules/` wildlife).
6. Each role's list in `plan.json` ends with a route that is always
   open: a mine that is not `off` and has no `max_ships`, `once`,
   `min_credits` or `requires`. The gate checks it. A list whose
   routes can all fill up leaves a ship idle: on 2026-11-15 three
   mines of 16 ships each left two traders without work.
7. A figure in `note` carries its date; `measured` is never typed by
   hand.

## 5. The Ladder of a New Pilot

A pilot born later flies the `once` routes of its role's list first,
in their order, then the recurring ones. What the first 55 pilots did
by hand and by the birth script is written down as routes so that the
next wave needs no hand: `first-survey` (off until tested as a route
file) and `voidborn-missions-1`.

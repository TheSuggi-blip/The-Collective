---
name: routes-blueprint
id: 20261115T154044Z
tier: intel
author: Unity
links: [game/routes/index.md, game/routes/plan.json, game/fleet/dispatch.py, communications/orders.log, governance/rulebook.md]
---

# BLUEPRINT.md -- How a Route Is Written

A route is one task a pilot carries out by itself, written down once
so that every ship, and every ship born later, can do it again. The
route files are the fleet's memory of how to earn and how to level;
the scripts in `game/fleet/` fly them; nobody retypes a route into a chat.

## 1. What Is Automatic

| Part | Does |
|---|---|
| `game/routes/<id>.json` | One route: what to do, for whom, and what our runs measured |
| `game/routes/plans/<role>.json` | One plan per role: the routes tried in this order for a free pilot. The role's Admiral keeps it (`owner`) |
| `game/routes/guidebook/<division>.md` | What each division learned about its routes and its levelling; its Admiral keeps it, every member reads it |
| `game/fleet/dispatch.py` (service `dispatch`) | Every 30 s gives each free pilot the first route of its role that is open to it |
| `game/fleet/route_run.py`, `hunt.py`, `census.py`, `mine.py` | The runners: one pilot, one route, one row in the runs file |
| `game/fleet/routemaker.py` (service `routemaker`) | Every ten minutes costs every way to earn that our readings show (fields, order books, boards, herds, recipes) and keeps the list in the unit's data folder. `routemaker.py show` lists the candidates of your division, best first; `routemaker.py route <id>` prints a candidate's route file, ready to be saved here as a test |
| `python3 -B game/fleet/routes.py check` | The gate: fails on a wrong route file, a wrong plan or a stale index |
| `python3 -B game/fleet/routes.py index` | Writes `master-index.md` (the groups of routes and the plans at a glance, every name a link), `index.md` (every route with its figures, grouped by what it is for, with its zone) and `plan.md` (every role's plan in its order); never by hand |
| `python3 -B game/fleet/routes.py measure --write` | Stores what the runs measured in the route file |

- Where a pilot is and which pilot flies which route stays in the
  unit's data folder (`data/fleet/`, `data/routes/`), never here.
- To change what your division does: edit your role's plan file or a
  route file, run the gate and the index, commit by path. The
  dispatcher reads the files at its next pass. To halt every start:
  the file `data/fleet/STOP`.
- A plan file has one writer, its `owner`. A route file another
  division flies too is changed by a request to whoever wrote it.
- A candidate of the route maker is an estimate from readings, never a
  measurement. From candidate to plan: `routemaker.py route <id>` into
  `game/routes/<id>.json` (it carries `max_ships` 1), your plan, the
  gate and the index, commit; after its first runs
  `routes.py measure --write`. A candidate that says `needs: ...`
  cannot be flown by a runner yet: fly it by hand, or ask for the
  step in `requests.log`.

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
| `max_pilots` | At most this many different pilots ever fly it (those that flew it and those on it now): for a route that buys a tool not every ship needs |
| `requires.without_module` | Only a pilot that does not carry this module is sent: for a route that fits it |
| `requires.empty_hold` | true: only a pilot with nothing aboard but ammunition and at most five units of goods is sent. For a route beyond policed space (orders F13): a ship lost there loses its hold |
| `requires.booked` | The title of a one-time reward (or a list of titles) the pilot must hold in `data/fleet/onetime.json` before it is sent: for a mission the board offers only after another one. On such a route a run the board refused (`... not offered`) is no try, up to three times, and the route rests `retry_minutes` after it |
| `status` | `off`: written down, not flown |
| `park` | true: the route that docks a ship and lets it wait. Given to a pilot in space only; the last route of every plan |
| `requires.bid` | `{"item", "base", "min_price", "min_qty"}` or a list of them: the route is open only while the station's book (`data/market/<base>.json`), read by a docked ship of ours within the hour, shows the item's best bid at `min_price` or more (default 1) with `min_qty` units or more at it (default 1). A book older than an hour closes nothing. For a route that sells one good: a hunt's drop, a mine's ice. It closes the route the minute a docked ship reads the bid gone and opens it again when one reads it back |
| `requires.stored` | `{"at": "<base id>", "item", "min"}` or a list of them: only a pilot whose own storage at that station holds `min` units of the item or more is sent (`data/stock/storage.json`, read by the service ledger about every 40 minutes), and not again until its storage was read after its last run of the route began. For a carry route: storage is personal, only the pilot that stored a load can withdraw it |
| `requires.skills` | `{skill: level}`: only a pilot that holds each skill at that level or higher is sent (its live file, `data/fleet/ships/`): for a mission a board offers only from a skill level, as Signal Fragments from navigation 3 |
| `skip_if_booked` | Titles of one-time rewards: a pilot that has one of them booked is not sent |
| `measured` | Written by `routes.py measure --write`: date, runs, minutes per run, credits per run, credits per ship-hour |

## 3. The Kinds

| Kind | Fields | The runner does |
|---|---|---|
| `circuit` | `stops`, `one_time` | Docks at each stop and there, in this order: hands in finished missions, `redock`, `store`, `withdraw` (own storage to the hold; when the stop sells the item, only what its bid takes), `sell`, `buy`, `fit`, `accept`, `mine`, `hunt`; saves the order book and the board |
| `hunt` | `place` (system:poi), `species`, `sell_at` (system:poi:base), `min_bid`, `kills`, `minutes`, `min_creatures`, `rest_minutes`, `max_prey_hull` (default 100), `alone` | Hunts grazers of the species, loots its own carcasses, sells what a bid of `min_bid` or more takes. `alone` true: before every fight it looks who is at the place and leaves without a fight when a ship that is not ours or a pirate stands there; set it on every hunt beyond policed space. On leaving it writes the herd it sees for the dispatcher's count, and its row records the hull before, after and at its lowest |
| `census` | `systems`, `every_minutes` | Reads the stalest system whole: deposits, creatures, order book, mission board |
| `mine` | `belt` (system:poi), `station` (system:poi:base), `minutes`, `sell` | Runs the engine's mining loop for the time; the ore goes into storage at the station. With `sell` (a list of `item`, `min_price`) the run ends with a sale: the pilot docks at the station, sells those goods from its hold and its storage there into the bids at `min_price` or more, the book read before every sale, and stores the rest of its hold |

A stop of a circuit:

| Field | Meaning |
|---|---|
| `at` | system:poi:base |
| `skip_if_hold` | Skip the stop when the hold has these goods already |
| `only_if_active` | Skip the stop unless one of these missions is still open |
| `redock` | Undock and dock again: a delivery counts on docking |
| `store` | Goods moved from the hold into the pilot's storage here |
| `sell` | `item`, `min_price`: sold only into a bid at that price or more, and no more units than stand at that best price. `all` true: every unit, down the bid's lower levels too; only for a mission that counts units sold |
| `buy` | `item`, `qty` (units wanted in the hold), `max_price`; never under the wallet floor of 3,000 cr (orders F7). `one_time`: goods for a one-time mission; their cost is booked against its reward |
| `fit` | A list of `module`, `max_price`: a pilot that does not carry the module buys one here and fits it (`install_mod`); never under the wallet floor |
| `accept` | A template id, or `template` with `needs`: accepted only with those goods aboard |
| `mine` | A list of `at` (system:poi), `for` (mission titles), `minutes`: after the station's work the pilot mines there with the engine's loop until the named missions' objectives are done. For missions that count units mined |
| `hunt` | A list of `at` (system:poi), `species`, `kills`, `minutes`, `for` (mission titles), `alone`: after the station's work the pilot hunts there with the rules of `hunt.py` (grazers of 100 hull or less, flee under 60% hull or when a ship joins) until the named missions' objectives are done, at most twice; the next stop hands the mission in. For missions that count kills |

`one_time` lists the mission titles whose reward is seed money: the
runner books them so that CPH counts recurring income only.

## 4. Rules

1. A route stays inside what the orders allow
   (`communications/orders.log`): today policed Voidborn space, grazers
   only, no word to another player.
2. Test a new route with one pilot before every pilot flies it: put it
   into your plan with `max_ships` 1, read its RESULT line and its row
   (`routes.py measure`), then lift the limit. A route kept for later
   has `status` `off`.
3. A route that buys says what the goods cost in its `note`, and sets
   `min_credits`.
4. A hunt names its `species`. Prey above 100 hull hits back hard: a
   pilot-whale (220) nearly killed a starter. Raise `max_prey_hull`
   only for a hull that was tested against that prey.
5. A hunt sets `max_ships` and `min_creatures`: a herd regrows only
   when it is hunted below its replacement rate, and it starves when
   its deposit is mined out (`game/rules/` wildlife).
6. Each plan ends with a route that is always open: `park`. The gate
   checks it. A ship with no paying route waits docked, which costs
   nothing; it does not fly a route that loses money to fill time
   (orders F8, Suggi 2026-11-15: mining for skill cost about 160 cr per
   ship-hour and the ore found no buyer).
7. A figure in `note` carries its date; `measured` is never typed by
   hand.

## 5. The Ladder of a New Pilot

A pilot born later flies the `once` routes of its role's list first,
in their order, then the recurring ones. What the first 55 pilots did
by hand and by the birth script is written down as routes so that the
next wave needs no hand: `first-survey` (off until tested as a route
file) and `voidborn-missions-1`.

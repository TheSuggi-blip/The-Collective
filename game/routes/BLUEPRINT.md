---
name: routes-blueprint
id: 20261115T154044Z
tier: intel
author: Unity
links: [game/routes/master-index.md, game/fleet/dispatch.py, communications/orders.log, governance/rulebook.md]
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
| A division's plan file (`game/fleet/plan.py`) | One file per division, kept by its Admiral: every ship with its own routes in their order (route ids, and `@<name>` for a template of the division, in any mix), between the list First and the list Then that every ship of the division flies. It names our ships, so it lies in the unit's data folder (`data/plans/plan-<division>.md`), not here. `plan.py apply` checks it and writes what the dispatcher flies by |
| `game/routes/plans/<role>.json` | Written by `plan.py` from the division's plan file, never by hand: the role's routes in one order, how many of its ships have each in their plan, and how many name each template (`templates`) |
| `game/routes/templates/<division>.json` | A division's templates, kept by its Admiral with `plan.py template` (`plan.py templates` lists them): named lists of routes in the order a ship tries them, each with an optional `title`, the skills it `trains` and a `note`; no pilot named. A ship's own routes name one as `@<name>` (`plan.py use`) and fly its routes in their place; a change of a template is one commit and moves every ship that names it within the minute. A template a ship names is not removed |
| `game/routes/guidebook/<division>.md` | What each division learned about its routes and its levelling; its Admiral keeps it, every member reads it |
| `game/fleet/dispatch.py` (service `dispatch`) | Every 30 s gives each free pilot the first route of its own list that is open to it |
| `game/fleet/route_run.py`, `hunt.py`, `census.py`, `mine.py`, `guard.py` | The runners: one pilot, one route, one row in the runs file |
| `game/fleet/routemaker.py` (service `routemaker`) | Every ten minutes costs every way to earn that our readings show (fields, order books, boards, herds, recipes) and keeps the list in the unit's data folder. `routemaker.py show` lists the candidates of your division, best first; `routemaker.py route <id>` prints a candidate's route file, ready to be saved here as a test |
| `python3 -B game/fleet/routes.py check` | The gate: fails on a wrong route file, a wrong plan or a stale index |
| `python3 -B game/fleet/routes.py index` | Writes `master-index.md` (the groups of routes and the plans at a glance, every name a link), one index per group of routes (`index-once-per-pilot.md`, `index-paying-routes.md`, `index-tests.md`, `index-fitting.md`, `index-standing-work.md`, `index-measured-at-a-loss.md`, `index-off.md`: every route of the group with its figures and its zone), one plan per role (`plan-<role>.md`: the role's routes in their order with the ships planned on each and the templates its ships fly; no credits, since what a route earns changes by the hour: the tool `route` or `routes` gives it with its age) and one page per division that has templates (`templates-<division>.md`); never by hand. No file holds every route or every plan |
| `python3 -B game/fleet/routes.py measure --write` | Stores what the runs of the last 12 hours measured in the route file, and takes the figure out of a repeating route without a readable run in those 12 hours: it is a test again |

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
| `kind` | `circuit`, `hunt`, `census`, `mine` or `guard` |
| `title` | One line: what and where |
| `note` | What was seen or measured, with its date |
| `once` | true: each pilot flies it one time (a mission the game offers once) |
| `max_ships` | At most this many pilots on it at one time |
| `min_credits` | A pilot with fewer credits is not sent |
| `requires.module` | Only a pilot with this module fitted is sent |
| `max_pilots` | At most this many different pilots ever fly it (those that flew it and those on it now): for a route that buys a tool not every ship needs |
| `requires.without_module` | Only a pilot that does not carry this module is sent: for a route that fits it |
| `requires.empty_hold` | true: only a pilot with nothing aboard but ammunition and at most five units of goods is sent. For a route beyond policed space (orders F13): a ship lost there loses its hold |
| `requires.hold` | true: only a pilot with more than five units of goods aboard (ammunition not counted) is sent. For a route that stores or sells what is aboard (a circuit stop with `store: "all"`): put ahead of the routes that want an empty hold, it empties a ship that a run left loaded, and a ship that carries nothing passes it by |
| `requires.booked` | The title of a one-time reward (or a list of titles) the pilot must hold in `data/fleet/onetime.json` before it is sent: for a mission the board offers only after another one. On such a route a run the board refused (`... not offered`) is no try, up to three times, and the route rests `retry_minutes` after it |
| `status` | `off`: written down, not flown |
| `park` | true: the route that docks a ship and lets it wait. Given to a pilot in space only; the last route of every plan |
| `requires.bid` | `{"item", "base", "min_price", "min_qty"}` or a list of them: the route is open only while the station's book (`data/market/<base>.json`), read by a docked ship of ours within the hour, shows the item's best bid at `min_price` or more (default 1) with `min_qty` units or more at it (default 1). A book older than an hour closes nothing. For a route that sells one good: a hunt's drop, a mine's ice. It closes the route the minute a docked ship reads the bid gone and opens it again when one reads it back |
| `requires.stored` | `{"at": "<base id>", "item", "min"}` or a list of them: only a pilot whose own storage at that station holds `min` units of the item or more is sent (`data/stock/storage.json`, read by the service ledger about every 40 minutes), and not again until its storage was read after its last run of the route began. For a carry route: storage is personal, only the pilot that stored a load can withdraw it |
| `requires.skills` | `{skill: level}`: only a pilot that holds each skill at that level or higher is sent (its live file, `data/fleet/ships/`): for a mission a board offers only from a skill level, as Signal Fragments from navigation 3 |
| `requires.skills_below` | `{skill: level}`: only a pilot that holds one of these skills under its level is sent: for a route that trains a skill up to a board's gate (a jump loop for navigation 3). Such a route is standing work |
| `standing` | true: standing work. It keeps a ship busy between paying work (it trains a skill, it gathers into storage) and is not judged on its pay: the loss stop never closes it and it counts as no paying work. A mine route without `sell` and a route with `requires.skills_below` are standing work without the field. Give it `max_ships`, and `min_left` when it mines |
| `min_left` | `{resource: units}` on a mine route (for its `belt`) or on a `mine` step of a circuit (for the step's place): no pilot is sent while the system's census, younger than 90 minutes, reads less of the resource there; the route opens again by itself when the field has grown back |
| `skip_if_booked` | Titles of one-time rewards: a pilot that has one of them booked is not sent |
| `measured` | Written by `routes.py measure --write`: date, runs, minutes per run, credits per run, credits per ship-hour, over the readable runs that ended in the last 12 hours (`hours`: 12, `last_run`: when the newest of them ended); a mission that pays once counts all its runs. A figure is never kept past its window: a repeating route without a readable run in 12 hours has none and is a test again, so a route measured at a loss yesterday may be flown again as a test |

## 3. The Kinds

| Kind | Fields | The runner does |
|---|---|---|
| `circuit` | `stops`, `one_time` | Docks at each stop and there, in this order: hands in finished missions, `redock`, `store`, `withdraw` (own storage to the hold; when the stop sells the item, only what its bid takes), `sell`, `buy`, `craft` (then `sell` again for what it made), `fit`, `accept`, `mine`, `hunt`; saves the order book and the board |
| `hunt` | `place` (system:poi), `species`, `sell_at` (system:poi:base), `min_bid`, `kills`, `minutes`, `min_creatures`, `rest_minutes`, `max_prey_hull` (default 100), `alone` | Hunts grazers of the species, loots its own carcasses, sells what a bid of `min_bid` or more takes. `alone` true: before every fight it looks who is at the place and leaves without a fight when a ship that is not ours or a pirate stands there; set it on every hunt beyond policed space. On leaving it writes the herd it sees for the dispatcher's count, and its row records the hull before, after and at its lowest |
| `census` | `systems`, `every_minutes` | Reads the stalest system whole: deposits, creatures, order book, mission board |
| `mine` | `belt` (system:poi), `station` (system:poi:base), `minutes`, `sell` | Runs the engine's mining loop for the time; the ore goes into storage at the station. With `sell` (a list of `item`, `min_price`) the run ends with a sale: the pilot docks at the station, sells those goods from its hold and its storage there into the bids at `min_price` or more, the book read before every sale, and stores the rest of its hold |
| `guard` | `guards` (the id of a mine or hunt route), `station` (system:poi:base), `place` (system:poi; default: the guarded route's `belt` or `place`), `minutes` (default 60), `max_ships` (default 1) | Keeps one ship at the place where a pilot of ours flies the guarded route: it flies there, never fires first and looks once a minute who is there (its log names our pilots and the others with their faction tag; the sightings stay the service `sight`'s). It leaves when no pilot of ours carried the guarded route's order in two looks in a row, after `minutes` at the place, under 60% hull or in a fight (stance flee), and docks at `station`. Open only while a pilot of ours flies the guarded route (`nobody flies <id>` otherwise); standing work, never judged on its pay. Write `place` into a guard beyond the border, or its zone reads from its station. Not flown yet (2026-11-16): fly it once with one ship and read its RESULT line before a plan relies on it |

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
| `craft` | A list of `recipe`, `runs`, `makes` (the item made), `per_run` (units one run makes, default 1), `inputs` (items moved from the hold into storage first): after the buy, the station's workshop makes the runs into the pilot's storage, from the inputs stored there; the runner waits for the made units, takes them into the hold and runs the stop's `sell` once more for them. No inputs, a fee that would take the wallet under its floor, or no `makes`: nothing is made, the note says so and the run goes on. The gate asks for `recipe`, `runs` and `makes`. Not flown yet (2026-11-16): fly it once with one ship and read its RESULT line before a plan relies on it |
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
6. No ship is idle (Suggi, 2026-11-16). A ship's list (the list First,
   its own routes, the list Then of its division's plan file) holds, in
   this order:
   the missions that pay once; the routes that pay, each with no more
   ships than it carries; standing work for every ship that is left
   (a mine route that sells nothing and gathers into storage, a loop
   that trains a skill: field `standing`), spread over several places,
   each with `max_ships` and `min_left`; the census; and last `park`,
   which the gate checks and which a ship should never reach.
   Standing work costs its fuel (about 160 cr per ship-hour measured
   on the first ore routes) and brings skill and the materials of
   standing order S6. The fill gate halts while a ship waits.
7. Read what a route carries before you give it ships or lift it
   (Suggi, 2026-11-16: never all ships on one route): give a route to as
   many ships as it carries, as their own route, and no more. `hive.py standing` prints for every
   route of your plan the ships it keeps busy hour after hour, from
   what its bid, its field or its herd regains, and how many more for
   one turn while today's standing order holds. `fill.py lift` refuses
   more than the two together. A bid's standing depth is one order: it
   can leave within the hour.
8. A figure in `note` carries its date; `measured` is never typed by
   hand.

## 5. The Ladder of a New Pilot

A pilot born later flies the `once` routes of its role's list first,
in their order, then the recurring ones. What the first 55 pilots did
by hand and by the birth script is written down as routes so that the
next wave needs no hand: `first-survey` (off until tested as a route
file) and `voidborn-missions-1`.

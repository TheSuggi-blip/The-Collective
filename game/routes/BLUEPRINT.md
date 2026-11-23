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


## Quick-Start Plan & Wing Recipes (Read Before Editing Plans or Routes)

Each division keeps one standing plan (`/srv/collective/data/plans/plan-<division>.md`) reconciled every **30s** by `dispatch.py`:
- **Execution order:** `First` (global one-time missions, upgrades, war overrides) -> ship's `Own routes` / `@templates` -> `Then` (shared paying wings & zero-fuel active desks) -> `park` (true IDLE emergency fallback only).
- **Mass wing assignment (1 command via MCP `plan action=set` or CLI `plan.py set`):**
  - `plan.py set "cargo>=100" "@freight-shipping > @craft-reserve"` (all 100c+ freighters)
  - `plan.py set "empire:nebula+speed>=5" "@express-pax > @bursar-desk"` (fast Nebula couriers)
  - `plan.py set "idle:true" "@docked-craft > @bursar-desk"` (immediately put idle ships onto zero-fuel active work)
- **Copy-paste route patterns:**
  - *Auto-mobilizing War Defense (`First`):* `"requires": {"posture": "war", "min_hull_tier": 1}`
  - *Proximity Utility Cluster (`Then`):* set `"utility_group": "regional-mine"` + `"requires": {"max_jumps": 6}` on regional routes so each ship auto-picks the closest high-paying unsaturated field.
  - *Active Zero-Fuel Bursar Desk (registers `working`, not `parked`):* `"requires": {"docked_at": "central_nexus"}`, stop with `"sell_order": [{"item": "fuel_cell", "qty": 50, "price": 2900, "floor": 2200, "undercut_pct": 0.05}]`, `"buy_order": [{"item": "carbon_ore", "qty": 500, "price": 4, "ceiling": 5}]`, and `"watch_minutes": 30`.
  - *Zero-Fuel Hub Market Watch (Intel `scout` only):* `"requires": {"docked_at": "arneb_hub"}`, stop with `"market_poll": true, "watch_minutes": 30`.

## 1. What Is Automatic

| Part | Does |
|---|---|
| `game/routes/<id>.json` | One route: what to do, for whom, and what our runs measured |
| A division's plan file (`game/fleet/plan.py`) | One file per division, kept by its Admiral: every ship with its own routes in their order (route ids, and `@<name>` for a template of the division, in any mix), between the list First and the list Then that every ship of the division flies. It names our ships, so it lies in the unit's data folder (`data/plans/plan-<division>.md`), not here. `plan.py apply` checks it and writes what the dispatcher flies by |
| `game/routes/plans/<role>.json` | Written by `plan.py` from the division's plan file, never by hand: the role's routes in one order, how many of its ships have each in their plan, and how many name each template (`templates`) |
| `game/routes/templates/<division>.json` | A division's templates, kept by its Admiral with `plan.py template` (`plan.py templates` lists them): named lists of routes in the order a ship tries them, each with an optional `title`, the skills it `trains` and a `note`; no pilot named. A ship's own routes name one as `@<name>` (`plan.py use`) and fly its routes in their place; a change of a template is one commit and moves every ship that names it within the minute. A template a ship names is not removed |
| `game/routes/guidebook/<division>/<chapter>.md` | What each division learned, as chapters of small capped entries: card, ships, levelling, routes, tests, lessons and at most two topics (rule F14); its Admiral keeps it, every member reads it (`hive.py guide <division>`; the gate `python3 -B scripts/guide.py check <division>`) |
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
| `requires.module` | Module id, a list of module ids (any one of them: `["mining_laser_i", "mining_laser_iii"]`, requests ENT-343), or `{module_id: min_count}` (every one, at least `min_count` copies): only a pilot carrying it is sent. `routes.py check` warns when a fit route that `replace`s a module stands in a plan beside a route that asks that module and not the new one |
| `max_pilots` | At most this many different pilots ever fly it (those that flew it and those on it now): for a route that buys a tool not every ship needs |
| `requires.without_module` | Module id (or `[module_id, ...]`): only a pilot carrying none of the named modules is sent |
| `requires.modules_below` | `{module_id: target_count}`: open while the pilot carries fewer than `target_count` copies (for multi-slot fitting such as `"count": 2`) |
| `requires.any_module` | `[module_id, ...]`: open only while the pilot still carries at least one of the named modules (for stripping off-role starter modules with `unfit`) |
| `requires.empty_hold` | true: only a pilot with nothing aboard but ammunition and at most five units of goods is sent. For a route beyond policed space (orders F13): a ship lost there loses its hold |
| `requires.hold` | true: only a pilot with more than five units of goods aboard (ammunition not counted) is sent. For a route that stores or sells what is aboard (a circuit stop with `store: "all"`): put ahead of the routes that want an empty hold, it empties a ship that a run left loaded, and a ship that carries nothing passes it by |
| `requires.booked` | The title of a one-time reward (or a list of titles) the pilot must hold in `data/fleet/onetime.json` before it is sent: for a mission the board offers only after another one. On such a route a run the board refused (`... not offered`) is no try, up to three times, and the route rests `retry_minutes` after it |
| `status` | `off`: written down, not flown |
| `park` | true: the route that docks a ship and lets it wait. Given to a pilot in space only; the last route of every plan |
| `requires.bid` | `{"item", "base", "min_price", "min_qty"}` or a list of them: the route is open only while the station's book (`data/market/<base>.json`), read by a docked ship of ours within the hour, shows the item's best bid at `min_price` or more (default 1) with `min_qty` units or more at it (default 1). A book older than an hour closes nothing. For a route that sells one good: a hunt's drop, a mine's ice. It closes the route the minute a docked ship reads the bid gone and opens it again when one reads it back |
| `requires.ask` | `{"item", "base", "max_price", "min_qty", "max_age_minutes"}` or a list of them (requests ENT-297): the route is open only while the station's book (`data/market/<base>.json`), read by a docked ship of ours within `max_age_minutes` (default 60), shows the item's best ask at `max_price` or under with `min_qty` units or more at it (default 1; a book keeps the units of its best ask only). Unlike `requires.bid`, a book older than that closes the route: an ask not read is no ask (`no ask for <item> at <base>: its book not read in N minutes`). `max_price` is the ask as the book shows it, before the buyer's 1 percent, which the stop's `buy` max_price counts. For a route that buys before it sells: it opens again when a docked ship reads the ask back, so the station needs a reader of ours (another route, a census) while the route is closed |
| `requires.stored` | `{"at": "<base id>", "item", "min"}` or a list of them (all must hold); `"items": [...]` in place of `item` is met by any one of them at `min` (requests ENT-349): only a pilot whose own storage at that station holds `min` units of the item or more is sent (`data/stock/storage.json`, read by the service ledger about every 40 minutes), and not again until its storage was read after its last run of the route began. For a carry route: storage is personal, only the pilot that stored a load can withdraw it |
| `requires.held_below` | `{"item", "units", "division"}` (Zero, errors.log ENT-111): the route is open only while the pilots of the division hold fewer than `units` of the item, their personal storage at every station and their holds together, as the storage book reads them (`data/stock/storage.json`, the service ledger, about every 40 minutes). `division`: a division (Mining) or its Admiral (Zero); left out, the division whose class of work the route is (a mine route: Mining). A book that is not whole decides nothing: a pilot that flew the route in the last two hours keeps it, no other pilot is sent (`held_below: the storage book is not whole`); a book older than three hours counts as not whole. For a mine route whose good the division stores: no new ore or ice is mined while the stores could sell into the bid. Off until the Fleet Admiral switches it on (`game/fleet/heldgate.py`, ON); while off such a route stays closed. `heldgate.py show` prints each such route with its reading |
| `requires.strict` | `true` or `false` (Zero, requests ENT-332): the route is open only while the switch file `data/fleet/strict-classes-on` stands (`true`) or only while it is absent (`false`); `dispatch.why_not` reads it, so fill.py and the dispatcher agree. A hand-over route (`give-*-stores-*`) carries `true`: it starts by itself the minute strict classes go on, and nobody edits its status |
| `requires.reserve` | `{"base": "<base id>", "item": "fuel", "below": N, "max_age_minutes": M}`: the route is open only while the newest reading of the faction's reserve of that item at that base reads under `below` units (`item` default `fuel`, the bunker's tank; `max_age_minutes` default 60). The readings: the faction's storage as `empire.py collect` reads it every 15 minutes (`data/empire/empire.json`, `faction_storage`), and for fuel the route's own runs whose stop there holds `bunker` (route_run.py notes `reserve R` at the run's end); the newest wins. A reading older than `max_age_minutes` closes the route (`reserve: not read for <age>`). For a supply route that keeps a bunker or a store over a floor: one run more fills it above the floor and closes it until the draw takes it under again. Off until the Fleet Admiral switches it on (`data/fleet/reserve-gate-on`); while off such a route stays closed. `game/fleet/reserves.py show` prints each such route with its reading |
| `requires.skills` | `{skill: level}`: only a pilot that holds each skill at that level or higher is sent (its live file, `data/fleet/ships/`): for a mission a board offers only from a skill level, as Signal Fragments from navigation 3 |
| `requires.skills_below` | `{skill: level}`: only a pilot that holds one of these skills under its level is sent: for a route that trains a skill up to a board's gate (a jump loop for navigation 3). Such a route is standing work |
| `standing` | true: standing work. It keeps a ship busy between paying work (it trains a skill, it gathers into storage) and is not judged on its pay: the loss stop never closes it and it counts as no paying work. A mine route without `sell` and a route with `requires.skills_below` are standing work without the field. Give it `max_ships`, and `min_left` when it mines |
| `min_left` | `{resource: units}` on a mine route (for its `belt`) or on a `mine` step of a circuit (for the step's place): no pilot is sent while the system's census, younger than 90 minutes, reads less of the resource there; the route opens again by itself when the field has grown back |
| `lift_to` | A number of ships on a standing mine route: how far `fill.py` may lift its `max_ships` by itself while ships wait and its field carries them. Its Admiral's word; with it the script lifts a route beyond the border too (rule F13), never past it. Without it a route in home space is lifted as far as its field carries, and a route beyond the border not at all |
| `skip_if_booked` | Titles of one-time rewards: a pilot that has one of them booked is not sent |
| `gift` | On a mine route: a receiver's word, or `{"to", "items", "source", "keep"}` as a circuit stop's `gift`. With `data/fleet/strict-classes-on` the run ends with the hand-over instead of the sale: the pilot docks at `station`, stores its hold and gives the goods there to the receiver (source `both` unless it names one); nothing is sold. Not with `deposit: "faction"`. Off, it changes nothing |
| `gift_to` | On a hunt route: a role (`trader`) or a flagship of ours. With `data/fleet/strict-classes-on` nothing is sold at `sell_at`: every good aboard but ammunition goes into the receiver's storage there, what the gift leaves aboard is stored, and the route is standing work (its runs earn nothing of their own). Off, it changes nothing. Without it, a hunt route sells, and with the switch on the dispatcher refuses it to every pilot that is not a trader ("sells: Trade's work (F23); give the goods to a trader with gift") |
| `measured` | Written by `routes.py measure --write`: date, runs, minutes per run, credits per run, credits per ship-hour, over the readable runs that ended in the last 12 hours (`hours`: 12, `last_run`: when the newest of them ended); a mission that pays once counts all its runs. A figure is never kept past its window: a repeating route without a readable run in 12 hours has none and is a test again, so a route measured at a loss yesterday may be flown again as a test |

## 3. The Kinds

| Kind | Fields | The runner does |
|---|---|---|
| `circuit` | `stops`, `one_time` | Docks at each stop and there, in this order: hands in finished missions, `redock`, `store`, `withdraw` (own storage to the hold; when the stop sells the item, only what its bid takes; an entry with `"from": "faction"` and `"keep": N` takes from the faction's storage here instead, leaving N, for a pilot whose faction role carries manage_treasury), `sell`, `buy`, `craft` (then `sell` again for what it made), `fit`, `accept`, `mine`, `hunt`; saves the order book and the board |
| `hunt` | `place` (system:poi), `species`, `sell_at` (system:poi:base), `min_bid`, `kills`, `minutes`, `min_creatures`, `rest_minutes`, `max_prey_hull` (default 100), `alone` | Hunts grazers of the species, loots its own carcasses, sells what a bid of `min_bid` or more takes. `alone` true: before every fight it looks who is at the place and leaves without a fight when a ship that is not ours or a pirate stands there; set it on every hunt beyond policed space. `alone` "pirates": it leaves only for a pirate or a pilot filed hostile (`game/players/h-*.md`) and hunts beside other strangers; its Admiral sets it once the route's runs hold (rule F13). On leaving it writes the herd it sees for the dispatcher's count, and its row records the hull before, after and at its lowest |
| `census` | `systems`, `every_minutes`, `chain`, `chain_jumps` | Reads the stalest system whole: deposits, creatures, pirates (name, tier, hull, shield), order book, mission board. `chain` N (default 0): after the first system the runner reads up to N more of the route's own list before it turns home, the nearest within `chain_jumps` lanes (default 2) that is due, never read first and not read by another ship now, while the tank holds the way there and home; one row per system |
| `mine` | `belt` (system:poi), `station` (system:poi:base), `minutes`, `sell`, `deposit` | Runs the engine's mining loop for the time; the ore goes into storage at the station (with `deposit: "faction"` into the faction's storage there: an outpost of ours has no personal storage; not flown yet, 2026-11-17: one ship first). With `sell` (a list of `item`, `min_price`) the run ends with a sale: the pilot docks at the station, sells those goods from its hold and its storage there into the bids at `min_price` or more, the book read before every sale, and stores the rest of its hold |
| `guard` | `guards` (the id of a mine or hunt route; or of a circuit: then the guard is an escort that follows the pilot of ours flying that circuit, `guard.py --follow`, requests ENT-217), `station` (system:poi:base), `place` (system:poi; default: the guarded route's `belt` or `place`), `minutes` (default 60), `max_ships` (default 1) | Keeps one ship at the place where a pilot of ours flies the guarded route: it flies there, never fires first and looks once a minute who is there (its log names our pilots and the others with their faction tag; the sightings stay the service `sight`'s). It leaves when no pilot of ours carried the guarded route's order in two looks in a row, after `minutes` at the place, under 60% hull or in a fight (stance flee), and docks at `station`. Open only while a pilot of ours flies the guarded route (`nobody flies <id>` otherwise); standing work, never judged on its pay. Write `place` into a guard beyond the border, or its zone reads from its station. Not flown yet (2026-11-16): fly it once with one ship and read its RESULT line before a plan relies on it |

A stop of a circuit:

| Field | Meaning |
|---|---|
| `at` | system:poi:base |
| `skip_if_hold` | Skip the stop when the hold has these goods already |
| `only_if_active` | Skip the stop unless one of these missions is still open |
| `redock` | Undock and dock again: a delivery counts on docking |
| `store` | Goods moved from the hold into the pilot's storage here |
| `store_faction` | Goods moved from the hold into the faction's storage here (`deposit` with target `faction`), after `store`: a list of item ids or `"all"`. Our outpost takes goods only so; the pilot must be a member of the faction |
| `gift` | `{"to", "items", "source", "keep"}` (or a list of them), after `store` and before `store_faction`: the goods go into the storage here of another pilot of ours (`deposit` with the receiver as `target`: a gift; it need be neither docked nor online). `to`: a role (`trader`, `hauler`, ...): the pilot its Admiral named for this station, `python3 -B game/fleet/handover.py receivers set <role> <base\|*> <pilot>` (data/fleet/receivers.json: a route file names no numbered pilot), or a flagship; any other name is refused, by the gate and by the runner (a gift to a stranger is a loss). `items`: item ids or `"all"` (default: every good but ammunition); `source`: `storage` (default), `cargo` or `both` (the hold first); `keep`: `{item: units}` the giver keeps. Many goods go in one call where the game takes the list, else one call per good; what went is read back from the giver's storage and hold; a refused gift leaves the goods with the giver and the row says so; one RESULT line per gift. No wallet moves: nobody earns by a gift, the receiver's sale is Trade's income. A circuit whose stops only give (with `store`, `withdraw`) is the shared class `deliver` and standing work. Acts only with `data/fleet/strict-classes-on` (rule F23); off, nothing is given. `handover.py dry-run <route id> [<giver>]` says to whom and what, without a call |
| `refuel` | false: dock without the station's fuel (default true). For a stop that burns carried cells (`burn_cells`) instead of buying the station's fuel |
| `burn_cells` | true: the fuel cells aboard go into the tank, as many whole cells as its room takes (`refuel` with item_id fuel_cell and a quantity; a cell burnt into less room than 20 loses the rest), after `store_faction`. A cell costs about 100 cr for 20 fuel where station fuel costs 11 to 15 cr a unit (2026-11-17) |
| `bunker` | `{"keep": N}` at an outpost of ours: the cells aboard are burnt into the tank and the tank above N is deposited into the faction's fuel reserve here (`deposit` item_id fuel, target faction), until no cell is left; the run's row notes the fuel moved and the reserve after. The bunker takes fuel only from a tank: cells stored there stay items. Keep N under max_fuel - 20 and enough for the way out; the pilot must be a member of the faction |
| `sell` | `item`, `min_price`: sold only into a bid at that price or more, and no more units than stand at that best price. `all` true: every unit, down the bid's lower levels too; only for a mission that counts units sold |
| `buy` | `item`, `qty` (units wanted in the hold), `max_price`; never under the wallet floor of 3,000 cr (orders F7). `one_time`: goods for a one-time mission; their cost is booked against its reward |
| `stop_on_failed_buy` | true (Mercury, errors.log ENT-113; a stop's option, not a route field): when a `buy` entry of this stop gets nothing (no ask at its limit, the wallet floor, or a buy that took nothing), the run ends at this stop: no later step of the stop and no later stop, the goods stay where they are, and the RESULT line says `stop N: the buy of <item> got nothing: run ended (stop_on_failed_buy)`. The dispatcher then reads the route's `requires.ask` again before it sends a pilot. A buy that got part of `qty` goes on. For a buy-and-sell route whose later stops live on the buy; never for a route whose later stops do their own work |
| `sell_order` | a stop's option, a list of `{"item", "qty", "price", "floor"}` (Mercury, rule F39, requests.log ENT-373): after the craft, the pilot keeps one resting sell order of the good at this station: an own order at another price is repriced (`modify_order`), and what it holds here (hold first, then storage) is listed until `qty` units stand listed (`create_sell_order`), at `price`, never under `floor` or the best bid. Fills settle later at the station, outside the run's credits; every program is a line of `communications/contracts.log` |
| `craft` | A list of `recipe`, `runs`, `makes` (the item made), `per_run` (units one run makes, default 1), `inputs` (items moved from the hold into storage first), `venue` (`facility`: a facility-only recipe such as `refine_steel`, asked without the workshop preset so the game rents a public facility and charges its fee; default the workshop), `max_fee` (the most one run may cost in cr; a quote above runs x max_fee makes nothing, note `fee above max_fee`): after the buy, the station's workshop makes the runs into the pilot's storage, from the inputs stored there; the runner waits for the made units, takes them into the hold and runs the stop's `sell` once more for them. No inputs, a fee that would take the wallet under its floor, or no `makes`: nothing is made, the note says so and the run goes on. The gate asks for `recipe`, `runs` and `makes`. Not flown yet (2026-11-16): fly it once with one ship and read its RESULT line before a plan relies on it |
| `unfit` | `["module_id", ...]`: runs right before `fit` at the docked stop; uninstalls every fitted copy of each named off-role module (e.g. `mining_laser_i` on fighters/traders/haulers/scouts, or `pulse_laser_i` on miners/traders/haulers/scouts) and deposits it in station storage, freeing slots, CPU and power |
| `fit` | A list of `module`, `max_price`, optional `count` (default `1`, e.g. `2` to fill both utility or defense slots with identical modules), optional `replace`: buys up to `count` total copies here and fits them (`install_mod`); never under the wallet floor; the price is booked as a tool bought once. `replace` (requests ENT-290) names the module it takes the place of, as a weapon in the one weapon slot: the new one is bought first, inside `max_price`, then the old one is taken out (`uninstall_mod`), the new one fitted and the old one stored here, all in one docked stop. A buy that fails takes nothing out. An install refused because the ship lost its dock docks again and installs before it leaves; a new one that still does not fit puts the old one back, and failing that too the next stop's dock fits it first. Give such a route `requires.module` (the old one) and `requires.without_module` (the new one). The gate asks of an entry with `replace` for `module`, `max_price` and a `replace` other than `module` |
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

## Declarative Degrees of Freedom & Active Zero-Fuel Desk Duty (2026-11-23)

All 500 ships reconcile every 30s against division plans (`plan-<division>.md` + `@templates`) using these declarative knobs:

- **Capability & Posture Gates (`requires`):**
  - `min_cargo` / `max_cargo`: cargo hold capacity bounds (e.g. `100` for `spacemolt_shipping` freighters).
  - `min_piloting` / `max_piloting`: automatic skill gating (e.g. `min_piloting: 10` triggers T2 upgrades within 30s).
  - `min_speed`: matches fast hulls (`Runner`/`Futures` speed 6) for express passenger/courier wings.
  - `hull` / `without_hull` & `min_hull_tier` / `max_hull_tier`: targets specific hulls or un-upgraded T0 starters (`max_hull_tier: 0`).
  - `empire`, `in_system`, `docked_at`, `max_jumps`: regional & zero-fuel station locality affinity.
  - `posture`: `"war"` or `"peace"` -- automatically activates war defense/escorts or pauses unescorted risky routes within 30s when faction war starts/ends.
- **Rate Limits & Proximity Utility:**
  - `cooldown_minutes`: per-pilot cooldown between runs.
  - `utility_group` (plus optional `priority_weight`): contiguous routes sharing a `utility_group` compete by proximity-weighted RTS Utility (`pay * weight / (1 + hops)`) so ships automatically pick the nearest high-pay open field/trade.
- **Active Zero-Fuel Docked Work (`route_run.py`, counts honestly as `working`, unlike `park` which is strictly IDLE):**
  - `sell_order`: supports dynamic rival undercutting (`undercut_pct`, `undercut_cr`) while respecting `floor` & `best_buy`.
  - `buy_order`: automated wholesale buy walls (`item`, `qty`, `price`, `ceiling`, optional `outbid_pct`/`outbid_cr`, strictly `< best_sell`).
  - `watch_minutes` (`<=120`) + `watch_interval_minutes` (default `5`) + `market_poll: true`: keeps docked Bursars, crafters, and hub market-watchers actively tending books/orders at 0 fuel burn (never allowed on `park`).
- **Declarative Wing Selectors (`plan.py set` / MCP `plan`):**
  - Select entire wings in one call: `empire:nebula`, `hull:Prayer`, `cargo>=100`, `piloting>=10`, `speed>=5`, `tier>=1`, `system:sol`, `docked:true`, `idle:true` (combine with `+` for AND, `,` for OR).
- **Per-Pilot & Per-Route Clean Stop (`game/fleet/stop_pilot.py` / MCP `stop`):**
  - End any wrong in-flight circuit/mine/hunt for one pilot (`stop_pilot.py miner-14`), many pilots, or an entire running route (`stop_pilot.py --route <route_id>`) within your division without touching global `data/fleet/STOP`. Uses `runhost` per-pilot stop (`data/fleet/host/stop/<pilot>`) or standalone `data/fleet/stop/<pilot>`; `route_run.py` halts cleanly before the next stop, logs its row, and frees the ship for the updated plan within 30s.
- **Military Pirate Farming & Scalable Formations (`"pirates_ok": true`, Rules F9/F27):**
  - Combat routes (`hunt`, `guard`, `circuit`) carrying `"pirates_ok": true` bypass the 6-hour civilian pirate avoidance gate in `dispatch.py` strictly for combat roles (`drone`, `sentinel`, `command`), while civilian miners/traders/haulers remain protected. Military engages and farms NPC pirates, packs, bounties, and strongholds solo or in scalable formations (`3/5/10/20+` ships -- game fleets or multi-wing shared battles, sizing fully at Apophis's discretion).
- **Autonomous Division Treasury Funding (`game/fleet/wallet.py fund` / MCP `fund`, Rule F12):**
  - Admirals fund their own division's pilots directly from the shared faction treasury (`wallet.py fund miner-1,miner-2 285000 --why "Resonance Miner batch"`; up to `400,000 cr`/pilot, `750,000 cr`/division per rolling 24h, keeping treasury `>= 500,000 cr` `FUND_FLOOR`). `wallet.py sweep` serves up to 10 open funds per 5-minute pass in a single batched withdrawal without waiting for Unity.

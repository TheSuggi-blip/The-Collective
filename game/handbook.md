---
name: handbook
id: 20261118T034859Z
tier: guide
author: Unity
links:
  - game/fleet/store.py
  - game/fleet/stats.py
  - game/fleet/docs.py
  - game/fleet/collective_mcp.py
  - game/fleet/hive.py
  - game/metrics.md
  - scripts/handbook.py
---

# handbook.md -- the store's handbook: how the fleet's data flows, where to ask what, every table

Written by `python3 -I -B scripts/handbook.py` from the code; never edited by hand.
The gate `python3 -I -B scripts/handbook.py --check` fails a file that differs; the hourly job writes them again. Only How
the data flows is kept by hand, in the script. Every table and view stands in the file of its subject (game/handbook/).
Read it in parts: `hive.py handbook [<topic>]` (MCP: the tool docs, view=handbook, topic=...): no topic gives the
contents and how the data flows; a table's name, a subject or a word gives its sections. The store holds every file
as kind `handbook` of the table docs, one row a section, every version in doc_versions.

The store: 65 tables and 13 views (44 snapshot, 9 history, 9 statistics, 3 bookkeeping); the MCP tool `collective`: 28 tools.
Kinds: snapshot = what a file says now (replaced when the file changes; it also carries `src`, the file its row came
from; dropped and loaded again when its definition changes); history = rows kept over time (raw rows for days, sums
as each table's Kept line says); statistics = computed by stats.py when due; view = a query over tables, computed when
asked; bookkeeping =
the store's own marks. Columns come from a fresh empty schema; every example runs in test_fleet_store_state.py.

## Contents

- How the data flows (below): the game to the members; what is private, what is public
- Where to ask what (below): a question -> the MCP call and the shell line, by subject
- Ships and pilots, `game/handbook/ships-and-pilots.md`: ships, ship_skills, ship_modules, ship_cargo, fleet_positions, hull_readiness, stats_pilot_hour, stats_pilot_last
- Routes and runs, `game/handbook/routes-and-runs.md`: routes, plan_routes, runs, route_hour, route_earnings, fuel_sinks, stats_route_author, missions
- Money, `game/handbook/money.md`: stats_money_hour, division_pnl_24h
- Markets, `game/handbook/markets.md`: books, ladders, moves, market_hour, contract_candidates
- Map and intel, `game/handbook/map-and-intel.md`: systems, lanes, places, fields, herds, readings, reading_day, stations, outpost_candidates, factions, public_battles, leaderboards, rival_snapshots, met, player_comms, observations
- Our faction, `game/handbook/our-faction.md`: faction, faction_members, bases, our_stations, faction_facilities, faction_storage, inventory_faction, territory, sites
- Stock and reserve, `game/handbook/stock-and-reserve.md`: holdings, inventory, inventory_by_station, stock_hour, needs, need_status
- The catalog, `game/handbook/the-catalog.md`: items, recipes, recipe_inputs, recipe_outputs, recipe_facilities, facilities, facility_materials, hulls, hull_materials, skills, game_releases
- Supply, `game/handbook/supply.md`: supply_chains, supply_status, stats_supply_hour
- Statistics, `game/handbook/statistics.md`: stats_time, stats_refill, stats_figures and the figures
- Written knowledge, `game/handbook/written-knowledge.md`: docs, doc_versions, division_playbooks and the kinds
- Plans and the door, `game/handbook/plans-and-the-door.md`: birth_plans
- The store itself, `game/handbook/the-store-itself.md`: source, cursor, meta

## How the data flows

The game -> the fleet engine and its gate -> the services -> the data folder (files) -> the store (live.db) ->
its read copy (read.db) -> hive.py and the MCP tool `collective` -> the members.

- The game: only the fleet engine holds the game key. Every program of ours reaches the game through the
  engine's gate; no member and no service holds the key.
- The services run on the unit's shelf, one program each, started again when they end:
  - `fleet`: our ships' live state as files (station/fleet.py): data/fleet/. Sends no command.
  - `sight`: who is where our ships are, a first read of a system nobody read: intel/met.json, scouting/.
  - `ledger`: every pilot's station storage (stock/storage.json) and every move of a best bid or ask
    (market/history.jsonl).
  - `dispatch`: gives each free pilot the next route of its plan; the runners it starts fly the route and
    append routes/runs.jsonl.
  - `routemaker`: costs every way to earn our readings show: routes/opportunities.json.
  - `runhost`: flies the dispatcher's runs, each as a thread.
  - `station`: Suggi's command station (map, fleet, intel, chat): data/station/.
  - `inbox`: what other pilots write to our ships (comms/messages.jsonl); a message to us is filed in
    communications/contacts/.
  - `keeper`: cuts the append-only records to their newest lines (the old lines to data/archive/).
  - `store`: the one writer of the database, below.
- The data folder /srv/collective/data/ is PRIVATE, never committed: where our ships are and what they carry
  stays there. The repository (the clone /srv/collective/the-collective, mirrored to GitHub) is PUBLIC: rules,
  orders, routes, the roles' plans, guidebooks, reports, logs, the catalog as files, this handbook.
- The store (game/fleet/store.py, service `store`) reads every minute the new lines of the records and every
  file that changed, of the data folder and the repository, into data/store/live.db, which no other program
  opens; it computes the statistics when due (stats.py) and publishes data/store/read.db, the copy every reader
  opens read-only.
- The readers: game/fleet/hive.py (one verb per question; `hive.py sql` asks any SELECT) and the MCP tool
  `collective` (game/fleet/collective_mcp.py), which runs those scripts for each member. Nobody writes a table
  by hand: members edit files, the gates check them, the store loads them. A new kind of input starts as a file
  a script writes, or a member's line by observe.py.

## Where to ask what

Ask through the MCP tool `collective` (each member's tools `mcp_collective_<tool>`) or in a shell from the repository:
`python3 -I -B game/fleet/hive.py <verb>` (the other scripts the same way). The tool `hive` passes any verb of hive.py
(`hive verb=<verb> args=[...]`); the tool `sql` asks any SELECT on the tables (`hive.py sql "<SELECT ...>"`). One line
per question, from the tools' own texts (collective_mcp.TOOLS) and hive.py's usage; <x> is a value you give.

### Ships and pilots

| What it answers | MCP | Shell |
|---|---|---|
| pilots' levels, XP an hour, hours to the next hull tier. | fleet view=levels | hive.py levels |
| a member's ships one line each, with their orders and last runs. | fleet view=board | board.py |
| empire-specialized T1/T2 parallel batch upgrade sheet. | fleet view=upgrade_plan | upgrades.py all |
| one ship: place, hull, fuel, hold, modules, wallet, order, skills | ship pilot=<pilot> | hive.py ship <pilot> |
| division cohorts, P0/P10 hull tables, and active queue. | upgrades action=status | upgrades.py |
| list queued upgrades. | upgrades action=queue | upgrades.py queue show |
| queue batch of pilots for automatic fund->commission->switch (executed every 5m in wallet sweep). | upgrades action=add | upgrades.py queue add --hull  --station  --max-price 0 |
| cancel pending entries by id, batch_id, or pilot. | upgrades action=cancel | upgrades.py queue cancel  |
| what a ship or a side of ours can hunt: its firepower and its toughness against a creature (rule F9). | hive verb=gauges | hive.py gauges |

### Routes and runs

| What it answers | MCP | Shell |
|---|---|---|
| what mining, hunting and the once-missions carry (bids, what is left in the fields, herds, tools) and... | fleet view=capacity | hive.py capacity |
| the standing fleet of a member: its plan route by route with the credits per ship-hour of each, and... | fleet view=standing | hive.py standing |
| credits per ship-hour by kind of work and by division, idle ships counted. | fleet view=tasks | hive.py tasks |
| every route: its group, zone, ships on it, what its runs measured, and its runs in the last hours | routes | hive.py routes |
| one route: its file, its last runs, and its credits per ship-hour hour by hour | route id=<id> | hive.py route <id> |
| Ways to earn that the route maker computed every 3 minutes from our own readings (fields, order... | candidates | routemaker.py show |
| With id: prints the ready route file; with id and write=true: writes game/routes/<id>.json, checks... | candidates id=<id> | routemaker.py route <id> |
| the history store (store.py): what it holds, and every route's credits per ship-hour over the whole... | hive verb=store | hive.py store |

### Money

| What it answers | MCP | Shell |
|---|---|---|
| credits, Net Purse/h (steady + paid once), matched Recurring Cash/h, and transfer-priced IAS2 Accrual... | fleet view=money | hive.py fleet |
| credits hour by hour per division. | fleet view=history | hive.py history |
| the hours ahead per division: every route with the ships on it now, what a ship-hour on it measured... | fleet view=forecast | hive.py forecast |
| Draw credits from the shared faction treasury for one or more pilots of your division (rule F12... | fund | wallet.py fund --show |

### Markets

| What it answers | MCP | Shell |
|---|---|---|
| bottleneck procurement candidates for Station Bursars, rival board supply contracts & contracts.log. | fleet view=contracts | hive.py contracts |
| live spacemolt_shipping freight contracts. | fleet view=shipping | shipping.py list |
| The last moves of one item's best bid and best ask at the stations whose order books our ships read... | market item=<item> | ledger.py prices <item> |
| one item's lowest and highest best bid and best ask per station over a window | hive verb=store args=[price, <item>] | hive.py store price <item> |

### Map and intel

| What it answers | MCP | Shell |
|---|---|---|
| live benchmark vs #1 [HEXC], unclaimed resource-monopoly outpost sites, zero-fuel docked crafting... | fleet view=rival | hive.py rival |
| rival faction sedcards & live Outsupply/Outsource/Undercut board. | fleet view=rivals | rivals.py all |
| one system: chart, places, what is left in its fields, its herds, its market, who was met, our ships | system id=<id> | hive.py system <id> |
| messages other players wrote to our ships. | comms view=contacts | inbox.py show --to-us |
| player hails through the CaMeL + dynamic spotlighting injection firewall. | comms view=safe_comms | comms_guard.py |
| every place our census ever counted a species: animals now, the most counted, the read's age, jumps... | hive verb=herds <species or ...> | hive.py herds <species,...> |

### Our faction

| What it answers | MCP | Shell |
|---|---|---|
| live 3-horizon strategic progression rungs, milestones & ledgers. | fleet view=progression | hive.py progression |
| what founding one takes, down to the ore: credits, parts, the facility that makes the part, what we... | base_plan kind=<kind> | hive.py base <kind> |
| Safely dismantle a faction facility at a station (`spacemolt_facility faction_dismantle`, Unity or... | dismantle pilot=<pilot> facility_id=<facility_id> | empire.py dismantle <pilot> <facility_id> |
| what we hold: the faction with its members and limit, our bases, our offices at other stations and... | hive verb=empire | hive.py empire |

### Stock and reserve

| What it answers | MCP | Shell |
|---|---|---|
| what a member's ships hold in station storage and in their holds. | stock view=members | ledger.py show |
| the whole fleet added up, by kind of item (raw, refined, parts, modules ...), with units stored and... | stock view=inventory | craftbook.py inventory |
| the same per station. | stock view=stations | craftbook.py inventory stations |
| what we hold beyond the reserve and may sell, best worth at a standing bid first, where it lies and... | stock view=surplus | surplus.py show |
| what our bases and upgrades take (the open needs of game/needs.tsv, tool needs) against what we hold... | stock view=reserve | surplus.py reserve |
| the open needs, highest priority first, each with covered percent, colour (red under 50, yellow 50 to... | needs action=list | needs.py list |
| one need whole (id) or every need of a project (project). | needs action=show id=<id> | needs.py show <id> |
| per item for the whole fleet its gross need, held and net short. | needs action=items | needs.py items |
| a need of your division (kind, ref, units, project; priority 1 high to 3, place, due, note, id)... | needs action=add kind=<kind> ref=<ref> units=<units> project=<project> | needs.py add <kind> <ref> <units> --project <project> |
| a need changed (id and what changes). | needs action=set id=<id> | needs.py set <id> |
| a need closed (id), built or no longer wanted. | needs action=done id=<id> | needs.py done <id> |
| a need closed (id), built or no longer wanted. | needs action=drop id=<id> | needs.py drop <id> |
| the gate. | needs action=check | needs.py check |
| what each division put into the reserve per hour: of every item the reserve asks for (surplus.py... | hive verb=flow | hive.py flow |

### The catalog

| What it answers | MCP | Shell |
|---|---|---|
| find an item by text; for one item how it is made, what uses it, what is built with it. | catalog ask=item name=<name> | craftbook.py item <name> |
| everything a number of units takes down to what is mined or bought, beside what we store. | catalog ask=needs name=<name> | craftbook.py needs <name> |
| what a facility or a hull costs and takes. | catalog ask=build name=<name> | craftbook.py build <name> |
| what a member's stored goods can be made into by hand today and what that sells for. | catalog ask=can | craftbook.py can |
| the recipes of a category, or that make or use an item. | catalog ask=recipes | craftbook.py recipes |
| newest SpaceMolt patch notes and active catalog version. | catalog ask=releases | craftbook.py releases |

### Supply

| What it answers | MCP | Shell |
|---|---|---|
| every chain with its status (short: below keep, low: below twice keep, ok, broken: a row of the file... | supply view=show | supply.py show |
| the gate, one line per short chain, broken row or unknown id, HALT or PASS. | supply view=check | supply.py check |
| for each short chain the source routes its keeper's plan does not hold yet and the change that would... | supply view=duty | supply.py duty |

### Statistics

| What it answers | MCP | Shell |
|---|---|---|
| what comes back per hour between our readings: bids, fields, herds. | fleet view=refill | hive.py refill |
| MAUTxWSJF weighted triage queue (P0>P1>P2>P3) & live WAR/CASHFLOW/GROWTH posture. | fleet view=scorecard | scorecard.py --who all |
| the fleet as one purse over 1, 6, 24 and 72 hours: throughput, operating expense, steady net, paid... | fleet view=kpi | hive.py stats kpi |
| per division its Net Purse/h (6h/24h), matched Recurring Cash/h, IAS2 Accrual Value-Add/h, raw steady... | fleet view=contribution | hive.py stats contribution |
| per role the places of its own class work open now against its ships, and the spill. | fleet view=classes | hive.py stats classes |
| where the ship-hours went: own work, another class's, once, shared, docked or in space without work... | fleet view=time | hive.py stats time |
| per reserve good held, needed, min and max, change an hour, days of supply, the routes and ships that... | fleet view=supply | hive.py stats supply |
| XP per ship-hour per role, skill and route, hours to the next tier. | fleet view=xp | hive.py stats xp |
| per ship its tier, Piloting, the next tier's hulls, empty slots. | fleet view=upgrades | hive.py stats upgrades |
| the hours outside their control band. | fleet view=alerts | hive.py stats alerts |

### Written knowledge

| What it answers | MCP | Shell |
|---|---|---|
| the orders in force, complete. | comms view=orders | comms.py orders |
| the board of requests not closed. | comms view=requests | comms.py requests |
| the last entries of every log. | comms view=digest | comms.py digest |
| each member's newest report and the knowledge files it wrote or changed. | comms view=learnings | hive.py learnings |
| orders in force, open requests, active claims and recent errors in one call. | comms view=turn_pack | comms.py turn-pack |
| Search the Collective's repository by meaning (rules, map, planets, players, factions, routes... | search question=<question> | query.py <question> --top-k 8 |
| list all tool groups (with counts) and guide slugs. | game_docs view=overview | game_docs.py overview |
| filter actions by group= or search= keyword. | game_docs view=commands | game_docs.py commands |
| exact live parameter schema and rules for tool= and optional topic=. | game_docs view=help | game_docs.py help  |
| read any official guide (drones, base-builder, boarding, passenger-lines, crafting, packages... | game_docs view=guide | game_docs.py guide  |
| the files, or one file's sections by title (doc: a file, a kind or an owner; grep: the sections that... | docs view=list | hive.py docs |
| one section whole. | docs view=section section=<section> | hive.py docs --section <section> |
| the sections changed since your last turn (or since). | docs view=changes | hive.py changes |
| every version of one section with when it was first seen, each against the one before. | docs view=history section=<section> | hive.py docs --section <section> --history |
| what each Admiral is doing, one short block a division: its mission, its orders block, its plan, its... | docs view=division | hive.py division all |
| a division's guidebook (division: yours by default, or all): its class card whole, the index of its... | docs view=guide | hive.py guide |
| the store's handbook, written from the code: how the data flows, where to ask what, and every table... | docs view=handbook | hive.py handbook |

### Plans and the door

| What it answers | MCP | Shell |
|---|---|---|
| per role how many ships work, start and wait, why each route of the plan is closed to the waiting... | fill action=status | fill.py status |
| the gate, PASS or HALT. | fill action=check | fill.py check |
| put the open paying routes and tests into your plan (write=true commits it; the dispatcher starts the... | fill action=fill | fill.py fill |
| one route into or out of a plan. | fill action=add route=<route> | fill.py add <route> |
| one route into or out of a plan. | fill action=drop route=<route> | fill.py drop <route> |
| set a route's max_ships. | fill action=lift route=<route> ships=<ships> | fill.py lift <route> <ships> |
| the file, what the check says and whether it is applied (brief=true: a few lines). | plan action=show | plan.py show |
| PASS or HALT. | plan action=check | plan.py check |
| after you changed the file by hand. | plan action=apply | plan.py apply |
| give ships their own routes (ships: names with commas, a range like miner-1..10, a role or all... | plan action=set ships=<ships> routes=<routes> | plan.py set <ships> <routes> |
| set that list whole. | plan action=first routes=<routes> | plan.py first <routes> |
| set that list whole. | plan action=then routes=<routes> | plan.py then <routes> |
| A template is a named list of routes your division keeps in the repository, which a ship's own routes... | plan action=templates | plan.py templates |
| A template is a named list of routes your division keeps in the repository, which a ship's own routes... | plan action=template name=<name> routes=<routes> | plan.py template <name> <routes> |
| A template is a named list of routes your division keeps in the repository, which a ship's own routes... | plan action=use ships=<ships> name=<name> | plan.py use <ships> <name> |
| Send one game command to one or many of your ships through the engine's gate, at once (up to 40... | command pilots=[<pilots>] action=<action> | gate.py raw <pilots> <action> {} |
| Give one of your ships an engine goal: a task the engine carries out by itself over many ticks... | goal pilot=<pilot> type=<type> | gate.py goal <pilot> <type> {} |
| Take one of your ships by hand (the dispatcher gives it no route) or, with release=true, give it back... | hold pilot=<pilot> | gate.py hold <pilot> |
| Stop one or more in-flight ships of your division cleanly (or every active run of your division on a... | stop | stop_pilot.py --list |
| Stop one or more in-flight ships of your division cleanly (or every active run of your division on a... | stop pilot=<pilot> | stop_pilot.py <pilot> |
| Stop one or more in-flight ships of your division cleanly (or every active run of your division on a... | stop route=<route> | stop_pilot.py --route <route> |
| Queue or inspect docked-leader faction errands (Unity-only, Q75 (12)): promote officer, post_mission... | errand action=show | wallet.py errand --show |
| Queue or inspect docked-leader faction errands (Unity-only, Q75 (12)): promote officer, post_mission... | errand action=add errand_action=<errand_action> params_json=<params_json> why=<why> | wallet.py errand add <errand_action> --params <params_json> --why <why> |
| Queue or inspect docked-leader faction errands (Unity-only, Q75 (12)): promote officer, post_mission... | errand action=cancel id=<id> | wallet.py errand cancel <id> |
| a session's start in one answer: the orders in force, the requests addressed to the member (and how... | hive verb=briefing | hive.py briefing |

### The store itself

| What it answers | MCP | Shell |
|---|---|---|
| every table and view of the store with what a row is and its columns; with a table's name its columns... | sql | hive.py schema |
| one SELECT or WITH statement on the store's read copy (store.py query: read only, one statement, a... | sql query=<query> | hive.py sql <query> |

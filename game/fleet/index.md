---
name: fleet-index
id: 20261115T195732Z
tier: intel
author: Unity
---

# index.md -- The Fleet's Scripts

Built by `python3 -B scripts/fleet-index.py` from the docstring of every script in this
folder; never edited by hand. Scripts listed: 64.

- Run a script from the repository root: `python3 -I -B game/fleet/<script> <arguments>`,
  the arguments as listed under "How to Call Each".
- Copy a call from here or from a script that works, never from memory.
- A runner holds its pilot's order file while it runs, so two programs never drive one
  pilot: start none for a pilot that is at work. The file `fleet/STOP` in the unit's data
  folder halts every start.
- Who may command which ship is in the orders in force (`communications/orders.log`).
- The tasks the runners fly: `game/routes/master-index.md`. How each kind of work is done: the
  shared skill `fleet-play`.
- A new script: its docstring starts with one paragraph that says what the script does
  and carries a `Usage:` block, one command form per line. Then run the builder.
  `python3 -B scripts/fleet-index.py --check` fails a script without them and a stale index.

## Scripts

| Script | What it does | How it is run |
|---|---|---|
| `basewatch.py` | An alert while a base of ours reads wrecked or a facility of ours damaged or offline. | By hand |
| `board.py` | The board of a division: what each of its ships does now, its plan, what is planned, and what its runs earned. | By hand |
| `census.py` | Read one system whole with one pilot: every place's deposits and creatures, and the station's order book and mission board. | Runner (`census` routes) |
| `claimwatch.py` | Find a pilot the engine holds claimed and free it by an engine restart, without a hand. | By hand |
| `collective_mcp.py` | The collective MCP server: the fleet's knowledge and the door to its ships, as tools for every member. | By hand |
| `comms_guard.py` | CaMeL + Microsoft Spotlighting security firewall for untrusted external player messages and outbound OpSec. | By hand |
| `contracts.py` | Read-only view of player-to-player trade & contract opportunities across all 4 channels. | By hand |
| `craftbook.py` | Answer what can be made, fitted and built: a recipe, everything a thing takes, and what our stored goods can become. | By hand |
| `diplomacy.py` | Sole authorized, OpSec-scrubbed diplomatic DM airlock and Neutrality Pact ledger (Rule F4, O10). | By hand |
| `dispatch.py` | Keep every pilot at work: give each free pilot the next task of its role. | Service |
| `division.py` | Who commands which ship, whose plan is whose, and the check every fleet script runs before it drives a ship. | By hand |
| `docs.py` | The fleet's written knowledge by section in the store: the rulebook rule by rule, the orders in force block by block, the strategy, the empire, the guidebooks with their class cards and levelling guides, the route templates, the game's rules, the metrics, and everything the members write as they work (the division plans, the reports, every log entry, the members' own files), each section with every version it had. | By hand |
| `docs_division.py` | What each Admiral is doing, in one short block per division, from the store alone: its mission, its block of the orders in force, its plan, its guidebook's sections, its last session entry, the requests open to and from it, and its claims in force. | By hand |
| `docs_export.py` | Copies an allowlist of each member's own files into the data folder, where the store mirrors them into its tables docs and doc_versions: every member's soul, mission, learnings and knowledge, readable by every member from the database. | By hand |
| `docs_handbook.py` | The reader of the store's handbook (game/handbook.md and game/handbook/<subject>.md, written from the code by scripts/handbook.py): its contents and how the data flows, or the sections of one topic: a table or view, a subject, or a word. | By hand |
| `empire.py` | Keep the picture of our empire: the faction and its limit, the bases and offices we own, the systems they stand in, the sites we may build on, and what the faction can build next. | By hand |
| `factionbook.py` | The faction's storage in the storage book: the entry `Faction` of data/stock/storage.json, so that the tools stock, surplus.py and the table holdings count what lies in the Lockboxes and at our outposts. | By hand |
| `fill.py` | Keep every ship of a division at work: say why ships wait, and fill the plan with the work that stands open. | By hand |
| `fleetfile.py` | Write the roster into a member's own FLEET.md: one table, every ship of the member on one line with its kind, its hull and the task it is on now. | By hand |
| `fuelplan.py` | Fuel before a flight: the chart's lanes, the stations that sell fuel, and whether a tank holds the way. | By hand |
| `gate.py` | Small client for the fleet engine's gate, with the division's lock. | By hand |
| `gauges.py` | What a ship or a side of ours can hunt: its firepower and its toughness against a creature (rule F9). | By hand |
| `guard.py` | Keep one pilot at the place where another route's ship of ours works, for as long as that ship works there. | Runner (`guard` routes) |
| `guidebook.py` | The divisions' guidebooks as capped chapters of small entries: their form and caps, one store section an entry, and the reader. | By hand |
| `handover.py` | Goods given into the storage of another pilot of ours: a circuit stop's `gift`, a mine route's `gift`, a hunt route's `gift_to`. | By hand |
| `heldgate.py` | The gate `requires.held_below` of a route: open only while a division holds fewer units of a good than a number. | By hand |
| `hive.py` | The fleet's figures from its own readings: money, routes and their history, levels, what the work carries, what a base takes, a system. | By hand |
| `hunt.py` | Hunt grazers at one place, loot the carcasses and sell what the kills bring. | Runner (`hunt` routes) |
| `inbox.py` | Read what other pilots write to our ships and say near them, keep every message once, and file the ones that are for us. | Service |
| `ledger.py` | Keep the fleet's books: what we own and where it lies, and how every order book moved. | Service |
| `loot_own.py` | Loot every carcass and wreck at the pilot's place that the pilot itself killed. | By hand |
| `mine.py` | One pilot mines at one field for a set time, through the engine's mining loop. | Runner (`mine` routes) |
| `mobile.py` | Where a moving station stands now, for a route stop that names the system it stood in when written. | By hand |
| `needs.py` | The fleet's needs register: what each division needs for its upgrades and for the empire, one row a need in game/needs.tsv, written by this script alone; the open needs are the reserve's targets, covered by stock in priority order. | By hand |
| `observe.py` | A member writes down what it saw in the game (a scan far away, a price at a station we read no book of, a fight with a species) as one checked line of its division's own record; the store makes the lines one SQL table, `observations`. | By hand |
| `passive_sense.py` | Zero-fuel opportunistic market & herd freshness updates when any fleet ship docks or works. | By hand |
| `plan.py` | Each division's plan file: every ship with the routes it flies, in their order; the dispatcher sends the ships by it. | By hand |
| `plate.py` | Make our pilots' stored creature carapace into armor plate where each is docked, and sell plates into the bid there. | By hand |
| `playbook_anchor.py` | Live division telemetry anchor, chapter high-watermark monitor, and empirical drift scanner. | By hand |
| `progression.py` | Live enterprise progression roadmap, strategic rung gauges, and historical milestone chronicle. | By hand |
| `pull.py` | Each class flies its own work, and goods are gathered only while the reserve needs them: the class guard and the pull rule of the dispatcher, with their dry run. | By hand |
| `reserves.py` | The gate `requires.reserve` of a route: open only while the last reading of a faction reserve (the fuel in a bunker, or an item of the faction's storage at a base) stands under a floor. | By hand |
| `retention.py` | How long the store keeps the tables it kept for good: the hourly sums 90 days, the daily sums 400, the written knowledge's versions the newest 20 of each section and every one of the last 30 days; one table of rules, applied in the store's prune step behind a switch that is off, with a dry run. | By hand |
| `rival_playbook.py` | Benchmark The Collective against #1 [HEXC] and surface resource-monopoly outpost sites, zero-fuel docked factory margins, and multi-empire hull upgrades. | By hand |
| `rivals.py` | Automated Rival Faction Sedcards, Observed Fleet Doctrine & Adopted Copy/Counter Playbooks (F40, O9). | By hand |
| `route_run.py` | Fly one pilot along a route file: dock at each stop and do what the stop says. | Runner (`circuit` routes) |
| `routemaker.py` | Find every way to earn that the fleet's own data shows, cost it, and write the route file for it. | Service |
| `routes.py` | Check the route files, write their index, and attach what the runs measured. | By hand |
| `routes_hygiene.py` | Automated structural legacy-route cleanliness (strictly honoring Rule F22). | By hand |
| `runhost.py` | One program that flies the runs the dispatcher starts, each run as a thread instead of a process. | Service |
| `scorecard.py` | Division KPI Scorecards, <80% Completion Triggers & Stagnation Detection. | By hand |
| `shipping.py` | Read-only CLI for SpaceMolt's Player-to-Player Freight / Courier board (spacemolt_shipping). | By hand |
| `sight.py` | What our ships see where they are: the pilots they meet, and a first read of a system nobody read. | Service |
| `stash.py` | Store what a docked pilot carries in its own storage at that station, so that its hold is free for the next route. | By hand |
| `stats.py` | The fleet's statistics, computed by the store into tables of its own: the fleet as one purse, what each division gives the whole, class capacity, where the ship-hours go, the reserve's days of supply, refill and regrowth, XP per ship-hour, the next upgrade of each ship, gather against buy, and control-chart alerts. | By hand |
| `store.py` | Keeps the fleet's history and its current state in one SQLite file: the runs, the price moves and the census readings with their sums by hour and by day, the members' own observations, and beside them what the fleet's own files say now. | Service |
| `supply.py` | The supply chains: the goods the fleet must never run out of, each at its place against what stands there now, with the ships on duty for it. | By hand |
| `surplus.py` | Say per item what the fleet holds beyond what its build targets reserve: the surplus a trader may sell, where it lies and its best bid. | By hand |
| `taxes.py` | Keeps each pilot's weekly tax apart, so that no run and no hour reads it as a loss. | By hand |
| `tug.py` | A ship of ours stranded in space with a tank that cannot reach fuel is towed to a station by the game's tug and refuelled. | By hand |
| `upgrades.py` | Live Empire-Specialized Hull & Module Upgrade Planner (rules F17, F37, O2). | By hand |
| `wallet.py` | No ship of ours goes broke: a ship whose wallet runs low is given credits by a rich ship of its division. | By hand |
| `watchdog.py` | Check whether the fleet is advancing across turns or stuck in loops, bottlenecks, or idle states. | By hand |
| `workclass.py` | Whose work a route is: the work class of every route and the classes each role flies | By hand |

## How to Call Each

### `basewatch.py`

An alert while a base of ours reads wrecked or a facility of ours damaged or offline.

Run by hand.

```
basewatch.py [show]     every alert, one line each
basewatch.py line       the briefing's line (empty while no alert stands)
--data <dir>            the unit's data folder (default /srv/collective/data)
```

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

### `claimwatch.py`

Find a pilot the engine holds claimed and free it by an engine restart, without a hand.

Run by hand.

```
claimwatch.py [check]     what the logs show now and what a pass would do; nothing is changed
claimwatch.py --act       one pass: keep the sightings; restart the engine when a pilot is claimed and every rule holds
--data <dir>   the unit's data folder (default /srv/collective/data)
```

### `collective_mcp.py`

The collective MCP server: the fleet's knowledge and the door to its ships, as tools for
every member.

Run by hand.

```
collective_mcp.py                      serve (started by Hermes)
collective_mcp.py --list               the tools, one line each
collective_mcp.py --call <tool> ['<json arguments>']
                                       run one tool and print its answer: a test without Hermes
--root <dir>   the repository (default: the one this file lies in)
--data <dir>   the unit's data folder, handed to the scripts (default: theirs)
```

### `comms_guard.py`

CaMeL + Microsoft Spotlighting security firewall for untrusted external player messages
and outbound OpSec.

Run by hand.

```
game/fleet/comms_guard.py [--data /srv/collective/data] [--last 25] [--quarantined]
```

### `contracts.py`

Read-only view of player-to-player trade & contract opportunities across all 4 channels.

Run by hand.

```
game/fleet/contracts.py [--limit 20]
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
craftbook.py inventory [stations] [--item <item id>] [--top N]
--data <dir>      the unit's data folder (default /srv/collective/data)
--root <dir>      the repository, for game/reserve-recipes.tsv (default: two folders above this file)
```

### `diplomacy.py`

Sole authorized, OpSec-scrubbed diplomatic DM airlock and Neutrality Pact ledger (Rule
F4, O10).

Run by hand.

```
diplomacy.py roster [--data DIR] [--root DIR]
diplomacy.py standings [--data DIR] [--root DIR]
diplomacy.py catalog [--limit N] [--data DIR] [--root DIR]
diplomacy.py threads [--tag TAG] [--last N] [--data DIR] [--root DIR]
diplomacy.py audit-text "<draft message>"
diplomacy.py send --to "<handle>" --message "<in-character text>" [--pilot scout-XX] [--dry-run] [--data DIR] [--root DIR]
diplomacy.py update-status --tag TAG --status STATUS [--note "<clean note>"] [--data DIR] [--root DIR]
diplomacy.py add-envoy --tag TAG --handle "<officer handle>" [--data DIR] [--root DIR]
diplomacy.py envoys [--data DIR]
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

### `docs.py`

The fleet's written knowledge by section in the store: the rulebook rule by rule, the
orders in force block by block, the strategy, the empire, the guidebooks with their
class cards and levelling guides, the route templates, the game's rules, the metrics,
and everything the members write as they work (the division plans, the reports, every
log entry, the members' own files), each section with every version it had.

Run by hand.

```
docs.py parse <file>      the sections of one file as the store loads them: id, characters, title
```

### `docs_division.py`

What each Admiral is doing, in one short block per division, from the store alone: its
mission, its block of the orders in force, its plan, its guidebook's sections, its last
session entry, the requests open to and from it, and its claims in force.

Run by hand.

```
docs_division.py [<Member>|<division>|all] [--data <dir>] [--root <dir>]
--data <dir>   the unit's data folder (default: the fleet's)
--root <dir>   the repository's game/ folder (default: the parent of this file's folder)
```

### `docs_export.py`

Copies an allowlist of each member's own files into the data folder, where the store
mirrors them into its tables docs and doc_versions: every member's soul, mission,
learnings and knowledge, readable by every member from the database.

Run by hand.

```
docs_export.py [--dry-run] [--quiet]   copy what changed, remove what left; one line of counts (--quiet: only when
                                       something was copied, removed or held back); --dry-run says what it would do
--profiles <dir>   the members' profiles (default /opt/data/profiles)
--data <dir>       the unit's data folder (default: the fleet's)
```

### `docs_handbook.py`

The reader of the store's handbook (game/handbook.md and game/handbook/<subject>.md,
written from the code by scripts/handbook.py): its contents and how the data flows, or
the sections of one topic: a table or view, a subject, or a word.

Run by hand.

```
docs_handbook.py [<topic>] [--data <dir>] [--root <dir>]
--data <dir>   the unit's data folder (default: the fleet's)
--root <dir>   the repository's game/ folder (default: the parent of this file's folder)
```

### `empire.py`

Keep the picture of our empire: the faction and its limit, the bases and offices we own,
the systems they stand in, the sites we may build on, and what the faction can build
next.

Run by hand.

```
empire.py collect [--ladder]     one reading, written to <data>/empire/empire.json (--ladder: read the cards again)
empire.py write [--commit]       governance/empire.md from the data file; --commit commits it by path as Unity
empire.py show
empire.py site <system> candidate|chosen|dropped [--poi <poi id>] [--note "<why>"]
empire.py check
--root <dir>   the repository's root (default: two folders above this file)
--data <dir>   the unit's data folder (default /srv/collective/data)
```

### `factionbook.py`

The faction's storage in the storage book: the entry `Faction` of
data/stock/storage.json, so that the tools stock, surplus.py and the table holdings
count what lies in the Lockboxes and at our outposts.

Run by hand.

```
factionbook.py show [--data <dir>]
--data <dir>   the unit's data folder (default /srv/collective/data)
```

### `fill.py`

Keep every ship of a division at work: say why ships wait, and fill the plan with the
work that stands open.

Run by hand.

```
fill.py [status] [<Member>|<role>|all]
fill.py status --why <pilot>   one pilot's whole list in order: why each route is closed now, or open
fill.py check [<Member>|<role>|all]
fill.py fill [<role>|all] [--write] [--once] [--tests N] [--floor CR]
fill.py add <route id> [--role <role>] [--first]
fill.py drop <route id> [--role <role>]
fill.py lift <route id> <ships>
--tests N    at most N tests added per role in one run (default 8)
--floor CR   a candidate counts from this estimate, in credits per ship-hour (default 500)
--root <dir>   the repository's game/ folder (default: the parent of this file's folder)
--data <dir>   the unit's data folder (default /srv/collective/data)
```

### `fleetfile.py`

Write the roster into a member's own FLEET.md: one table, every ship of the member on
one line with its kind, its hull and the task it is on now.

Run by hand.

```
fleetfile.py [<Member>|all] [--print] [--commit]
--root <dir>      the repository's game/ folder (default: the parent of this file's folder)
--data <dir>      the unit's data folder (default /srv/collective/data)
--profiles <dir>  where the members' workspaces lie (default /opt/data/profiles): <profiles>/<name>/workspace-<name>/FLEET.md
```

### `fuelplan.py`

Fuel before a flight: the chart's lanes, the stations that sell fuel, and whether a tank
holds the way.

Run by hand.

```
fuelplan.py <from system> <to system> [<then system>] [--tank N]
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
gate.py book_onetime <pilot> "<title>" <credits>
                                  one row of data/fleet/onetime.json by hand, no game call: a reward paid once (+) or a
                                  hull or tool bought once (-) of a pilot of your own division (Mercury, Q75 (6))
```

### `gauges.py`

What a ship or a side of ours can hunt: its firepower and its toughness against a
creature (rule F9).

Run by hand.

```
gauges.py ship <pilot>...             each ship: its weapons, skills, firepower and toughness, what it kills and stands
gauges.py side <pilot>...             the pilots as one side: its gauges and the species of our readings it passes
gauges.py species [--role <role>]     every species seen: hull, weight, whether one typical ship of the role passes
                                      both gauges, the smallest group that does (default: drone, the hunting role;
                                      `--role all`: the whole fleet's typical ship)
--data <dir>                          the unit's data folder (default /srv/collective/data)
```

### `guard.py`

Keep one pilot at the place where another route's ship of ours works, for as long as
that ship works there. Reads only: it never fires, never buys and never mines; in a
fight it flees.

A runner: the dispatcher starts it for a route of the kind `guard`; by hand only for a test with one free pilot.

```
guard.py <pilot> <system_id> <poi> --guards <route id> --station <system:poi:base> [--minutes M] [--route ID]
    python3 -I guard.py <pilot> <system_id> <poi> --guards <route id> --station <system:poi:base> --follow <pilot of ours> [--minutes M] [--route ID]
```

### `guidebook.py`

The divisions' guidebooks as capped chapters of small entries: their form and caps, one
store section an entry, and the reader.

Run by hand.

```
hive.py guide [<division>|<member>|all] [--chapter <name>] [--grep <word>] [--retired]
guidebook.py parse <chapter file>     the sections of one chapter as the store loads them: id, characters, title
--data <dir>   the unit's data folder (default /srv/collective/data)
--root <dir>   the repository's game/ folder (default: the parent of this file's folder)
```

### `handover.py`

Goods given into the storage of another pilot of ours: a circuit stop's `gift`, a mine
route's `gift`, a hunt route's `gift_to`.

Run by hand.

```
handover.py receivers [set <role> <base|*> <pilot> | drop <role> <base|*>]
handover.py dry-run <route id> [<giver>]
--data <dir>   the unit's data folder (default FLEET_DATA_ROOT or /srv/collective/data)
--root <dir>   the repository's game/ folder (default: the parent of this file's folder)
```

### `heldgate.py`

The gate `requires.held_below` of a route: open only while a division holds fewer units
of a good than a number.

Run by hand.

```
heldgate.py show [--root <dir>] [--data <dir>]
--root <dir>   the repository's game/ folder (default: the parent of this file's folder)
--data <dir>   the unit's data folder (default /srv/collective/data)
```

### `hive.py`

The fleet's figures from its own readings: money, routes and their history, levels, what
the work carries, what a base takes, a system.

Run by hand.

```
hive.py fleet
hive.py routes [--group once|paying|test|fit|service|losing|off] [--kind <kind>] [--zone home|beyond] [--hours N]
hive.py route <route id>
hive.py history [--hours N]
hive.py ship <pilot>
hive.py gauges ship <pilot>... | side <pilot>... | species [--role <role>]
hive.py levels [<Member>|all]
hive.py capacity
hive.py base outpost|station
hive.py system <system id>
hive.py learnings [--hours N]
hive.py standing [<Member>|<role>|all] [--hours N]
hive.py tasks [--hours N]
hive.py forecast [<Member>|all] [--hours N]
hive.py refill
hive.py docs [<path|kind|owner>] [--section <id> [--history]] [--grep <word>]
hive.py changes [--since <ISO time>|<N>h] [--member <name>]
hive.py division [<Member>|<division>|all]
hive.py guide [<division>|<Member>|all] [--chapter <name>] [--grep <word>] [--retired]
hive.py briefing [<Member>|all] [--hours N]
hive.py store [--hours N]
hive.py store price <item id> [--hours N]
hive.py inventory [stations] [--item <item id>] [--top N]
hive.py empire
hive.py surplus [--top N] [--kind <kind>] [--item <item id>] [--all]
hive.py reserve
hive.py supply [show|check|duty]
hive.py needs [list [<division>] [--project <text>] [--all] | show <id>|<project> | items | check]
hive.py flow [<Member>|all] [--hours N]
hive.py sql "<SELECT or WITH statement>" [--limit N]
hive.py schema [<table or view>]
hive.py handbook [<table or view>|<subject>|<word>]
hive.py watchdog [--hours N] [--json]
hive.py stats <view> [--hours N] [--member <Member>]
--root <dir>   the repository's game/ folder (default: the parent of this file's folder)
--data <dir>   the unit's data folder (default /srv/collective/data)
```

### `hunt.py`

Hunt grazers at one place, loot the carcasses and sell what the kills bring.

A runner: the dispatcher starts it for a route of the kind `hunt`; by hand only for a test with one free pilot.

```
hunt.py <pilot> <system_id> <poi> [--species a,b] [--kills N] [--minutes M]
    [--min-bid CR] [--sell-at system:poi:base] [--max-prey-hull N]
    [--route ID] [--keep] [--gift-to <role|pilot>]
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
inbox.py contacts [--out <dir>]   what a run with --commit would write, printed; with --out the logs written into
                                  <dir>, a folder outside the repository. Nothing is written into the repository
inbox.py contacts --commit [--dry-run]
                                  write communications/contacts/<tag>.log from the messages to us and commit exactly
                                  those files, a log this script left uncommitted among them; --dry-run: what it would do
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
mine.py <pilot> <system:poi> <system:poi:base> [--minutes M] [--sell-items item:min_price,...] [--route ID] [--deposit faction]
        [--gift <JSON>]
```

### `mobile.py`

Where a moving station stands now, for a route stop that names the system it stood in
when written.

Run by hand.

```
game/fleet/mobile.py <base> [<system> <poi>]    # where the base stands now, or `unchanged`
from mobile import locate; system, poi, line = locate(system, poi, base, data_dir)
```

### `needs.py`

The fleet's needs register: what each division needs for its upgrades and for the
empire, one row a need in game/needs.tsv, written by this script alone; the open needs
are the reserve's targets, covered by stock in priority order.

Run by hand.

```
needs.py list [<division>|<Member>|all] [--project <text>] [--all]
needs.py show <id>|<project text>
needs.py items
needs.py add <facility|hull|item> <ref> <units> --project "<text>" [--priority 1|2|3] [--place <base id>] [--due YYYY-MM-DD] [--note "<text>"] [--id <id>] [--division <name>] [--dry-run]
needs.py set <id> [--project ..] [--kind ..] [--ref ..] [--units N] [--priority N] [--place ..] [--due ..] [--note ..] [--status open|done|dropped] [--division ..] [--dry-run]
needs.py done <id> [--note "<text>"] [--dry-run]
needs.py drop <id> [--note "<text>"] [--dry-run]
needs.py tidy [--dry-run]
needs.py check
--root <dir>      the repository (default: two folders above this file)
--data <dir>      the unit's data folder (default /srv/collective/data)
--where and --by are taken for --place and --due; `-` or `none` empties a cell.
```

### `observe.py`

A member writes down what it saw in the game (a scan far away, a price at a station we
read no book of, a fight with a species) as one checked line of its division's own
record; the store makes the lines one SQL table, `observations`.

Run by hand.

```
observe.py add <kind> <subject> [key=value ...] [--note "text"] [--at <UTC time>]   one observation (default: now)
observe.py show [<kind>] [--subject <text>] [--division <name>|all] [--last N]       the newest rows as plain lines
                                                                                     (default: own division, 20 rows)
observe.py kinds [--division <name>|all]                                             every kind on record: its rows,
                                                                                     newest time and field names
--data <dir>   the unit's data folder (default /srv/collective/data)
--at           2026-11-16T22:10:05Z, 2026-11-16 22:10 (UTC)
--subject      the rows whose subject holds the text (any case)
```

### `passive_sense.py`

Zero-fuel opportunistic market & herd freshness updates when any fleet ship docks or
works.

Run by hand.

```
imported by mine.py, hunt.py and route_run.py: maybe_refresh_market(call_raw, base_id, system_id)
```

### `plan.py`

Each division's plan file: every ship with the routes it flies, in their order; the
dispatcher sends the ships by it.

Run by hand.

```
plan.py [show] [<division>|<Member>|all] [--brief]    the file, what the check says and whether it is applied
plan.py check [<division>|<Member>|all]               PASS or HALT per division (exit 1 on a HALT)
plan.py apply [<division>|<Member>|all] [--quiet]     after a change by hand: check, write, commit
plan.py set <ships> <routes> [--division <name>]      the own routes of ships: names with commas, a range
                                                      (miner-1..10), a role or `all`; routes with commas in their
                                                      order (`@<name>` for a template, in any mix), or `none`
plan.py first <routes> [--division <name>]            the list First, whole
plan.py then <routes> [--division <name>]             the list Then, whole
plan.py templates [<division>|<Member>|all]           each template: name, title, trains, its routes in order, and
                                                      how many ships of the division use it
plan.py template <name> <routes|none> [--title "..."] [--trains a,b] [--note "..."] [--division <name>]
                                                      make or replace a template (routes with commas, in their
                                                      order; an option not given keeps its value); `none` removes
                                                      it, refused while a ship names it
plan.py use <ships> <name[,name...]> [--division <name>]
                                                      `set` with `@` before each name: the ships fly the templates
plan.py planned <what> [--when <when>] [--division <name>]
                                                      one line into Planned (`- what | when`; it names no ship)
plan.py planned --clear [<what> [--when <when>]] [--division <name>]
                                                      Planned emptied, or replaced by the one line given
plan.py note <text> [--division <name>]               one line into Notes, stamped with the UTC time
plan.py note --clear [--division <name>]              Notes emptied
--root <dir>   the repository's game/ folder (default: the parent of this file's folder)
--data <dir>   the unit's data folder (default: the fleet's)
```

### `plate.py`

Make our pilots' stored creature carapace into armor plate where each is docked, and
sell plates into the bid there.

Run by hand.

```
plate.py <pilot> [<pilot> ...] [--min-bid N] [--no-craft] [--no-sell] [--dry-run]
```

### `playbook_anchor.py`

Live division telemetry anchor, chapter high-watermark monitor, and empirical drift
scanner.

Run by hand.

```
playbook_anchor.py [<division>|<member>|all] [--json] [--drift-only]
--data <dir>   the unit's data folder (default /srv/collective/data)
--root <dir>   the repository root (default: two folders above this file)
```

### `progression.py`

Live enterprise progression roadmap, strategic rung gauges, and historical milestone
chronicle.

Run by hand.

```
progression.py [show] [--json]
progression.py write [--commit]
--data <dir>   the unit's data folder (default /srv/collective/data)
--root <dir>   the repository root (default: two folders above this file)
```

### `pull.py`

Each class flies its own work, and goods are gathered only while the reserve needs them:
the class guard and the pull rule of the dispatcher, with their dry run.

Run by hand.

```
pull.py check [<division>|<Member>|all] [--now <UTC time>]   the dry run: what the two rules would refuse and close, who would wait
pull.py levels [--now <UTC time>]                             the goods of the reserve with their levels and marks
--root <dir>   the repository's game/ folder (default: the parent of this file's folder)
--data <dir>   the unit's data folder (default /srv/collective/data)
```

### `reserves.py`

The gate `requires.reserve` of a route: open only while the last reading of a faction
reserve (the fuel in a bunker, or an item of the faction's storage at a base) stands
under a floor.

Run by hand.

```
reserves.py show [--root <dir>] [--data <dir>]
--root <dir>   the repository's game/ folder (default: the parent of this file's folder)
--data <dir>   the unit's data folder (default /srv/collective/data)
```

### `retention.py`

How long the store keeps the tables it kept for good: the hourly sums 90 days, the daily
sums 400, the written knowledge's versions the newest 20 of each section and every one
of the last 30 days; one table of rules, applied in the store's prune step behind a
switch that is off, with a dry run.

Run by hand.

```
retention.py --dry-run [--data <dir>] [--db <file>] [--now <epoch>] [--keep-days N]
    per table: its rows, the rows of the last 24 hours, its rule, the reader that reads it furthest back, the rows
    that would go now and in a year at today's rate, and its size; then the tables that need no rule
--data <dir>    the unit's data folder (default /srv/collective/data): its store's read copy
--db <file>     another copy of the store instead (a copy of read.db, for a dry run away from the live files); it is
                opened immutable, so it must be a whole copy (VACUUM INTO, as read.db is), not a file with a WAL beside it
--now <epoch>   the time the rules are judged at (default: now)
--keep-days N   the store's --keep-days (default store.py KEEP_DAYS, 7)
```

### `rival_playbook.py`

Benchmark The Collective against #1 [HEXC] and surface resource-monopoly outpost sites,
zero-fuel docked factory margins, and multi-empire hull upgrades.

Run by hand.

```
game/fleet/rival_playbook.py [--data /srv/collective/data] [--brief]
```

### `rivals.py`

Automated Rival Faction Sedcards, Observed Fleet Doctrine & Adopted Copy/Counter
Playbooks (F40, O9).

Run by hand.

```
game/fleet/rivals.py [all|playbooks|tricks|<TAG>|<division>] [--json]
game/fleet/rivals.py write [--commit]
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
routemaker.py write <id> [--commit]
                                  write the candidate's route file to game/routes/<id>.json, check & index it
--data <dir>                      the unit's data folder (default /srv/collective/data)
```

### `routes.py`

Check the route files, write their index, and attach what the runs measured.

Run by hand.

```
routes.py check | index | measure | idle         [--root <dir>] [--data <dir>]
routes.py measure --write <route id>... | --role <role> | --all
                  writes the measured block of the routes named, of a role's plan, or of every route (the hourly
                  job); without one of the three it writes nothing and says so
```

### `routes_hygiene.py`

Automated structural legacy-route cleanliness (strictly honoring Rule F22).

Run by hand.

```
game/fleet/routes_hygiene.py [--root /srv/collective/the-collective] [--write]
```

### `runhost.py`

One program that flies the runs the dispatcher starts, each run as a thread instead of a
process.

A service: it runs by itself and is never started a second time.

```
runhost.py              run forever (the service `runhost`)
--fleet <dir>   the folder of the runners (default: this file's folder)
--data <dir>    the unit's data folder (default /srv/collective/data)
```

### `scorecard.py`

Division KPI Scorecards, <80% Completion Triggers & Stagnation Detection.

Run by hand.

```
game/fleet/scorecard.py [--who all|Unity|Zero|Mercury|Apollo|Apophis|Oracle] [--json]
```

### `shipping.py`

Read-only CLI for SpaceMolt's Player-to-Player Freight / Courier board
(spacemolt_shipping).

Run by hand.

```
game/fleet/shipping.py list [--pilot NAME] [--limit 25]
game/fleet/shipping.py active [--pilot NAME]
game/fleet/shipping.py profile [--pilot NAME]
game/fleet/shipping.py track <contract_id> [--pilot NAME]
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

### `stash.py`

Store what a docked pilot carries in its own storage at that station, so that its hold
is free for the next route.

Run by hand.

```
stash.py <pilot> [<pilot> ...] [--dry-run]
```

### `stats.py`

The fleet's statistics, computed by the store into tables of its own: the fleet as one
purse, what each division gives the whole, class capacity, where the ship-hours go, the
reserve's days of supply, refill and regrowth, XP per ship-hour, the next upgrade of
each ship, gather against buy, and control-chart alerts.

Run by hand.

```
hive.py stats <view> [--hours N] [--member <Member>]     views: kpi, contribution, classes, time, supply, gather, xp,
                                                         upgrades, alerts, refill, status
stats.py <view> [--hours N] [--member <Member>] [--data <dir>]    the same
--hours N      kept for the tool's argument: the store computes kpi over 1, 6, 24 and 72 hours and contribution, time
               and xp over 24; another N is said `not measured` and those are shown
--data <dir>   the unit's data folder (default /srv/collective/data)
```

### `store.py`

Keeps the fleet's history and its current state in one SQLite file: the runs, the price
moves and the census readings with their sums by hour and by day, the members' own
observations, and beside them what the fleet's own files say now.

A service: it runs by itself and is never started a second time.

```
store.py serve [--every 60]     run forever (the service `store`)
store.py once                   one pass, then stop
store.py recount                ask the writer to count every raw run kept again by the fleet's one rule
                                (routes.earned) and to sum its hours again: after a record that rule reads
                                was mended (the tax record, the wallet guard's gifts)
store.py status                 from the read copy: rows and newest row of each table, age of the copy, the
                                snapshot tables with the age of their newest source, the files not read
--data <dir>                    the unit's data folder (default /srv/collective/data)
--root <dir>                    the repository's game/ folder (default: the parent of this file's folder)
--keep-days N                   days of raw rows kept (default 7; observations at least 30: KEEP_TABLES)
```

### `supply.py`

The supply chains: the goods the fleet must never run out of, each at its place against
what stands there now, with the ships on duty for it.

Run by hand.

```
supply.py [show]              every chain: status, stock, keep, need/h, 24 h change, sources, ships on them
supply.py check               the gate: one line per short chain, broken row or unknown id; exit 1 on any
supply.py duty [--dry-run]    what duty would change: sources to put into the keepers' plans, ends due
supply.py duty --write        make that change (refused while DUTY_ENABLED is False)
--root <dir>   the repository's game/ folder (default: the parent of this file's folder)
--data <dir>   the unit's data folder (default /srv/collective/data)
```

### `surplus.py`

Say per item what the fleet holds beyond what its build targets reserve: the surplus a
trader may sell, where it lies and its best bid.

Run by hand.

```
surplus.py show [--top N] [--kind <kind>] [--item <item id>] [--all]
surplus.py reserve
surplus.py check
--root <dir>      the repository (default: two folders above this file)
--data <dir>      the unit's data folder (default /srv/collective/data)
```

### `taxes.py`

Keeps each pilot's weekly tax apart, so that no run and no hour reads it as a loss.

Run by hand.

```
taxes.py                 one pass (the five-minute job runs it)
taxes.py --all           ask every pilot, whatever the record says
taxes.py --dry-run       print what would be booked, write nothing
taxes.py show            the record: per assessment the pilots and the credits
--data <dir>             the unit's data folder (default: the fleet's)
```

### `tug.py`

A ship of ours stranded in space with a tank that cannot reach fuel is towed to a
station by the game's tug and refuelled.

Run by hand.

```
tug.py [--dry-run] [--below 25] [--limit 3] [--wait 15] [--pilot <name>]
```

### `upgrades.py`

Live Empire-Specialized Hull & Module Upgrade Planner (rules F17, F37, O2).

Run by hand.

```
game/fleet/upgrades.py [--who all|Unity|Zero|Mercury|Apollo|Apophis|Oracle]
```

### `wallet.py`

No ship of ours goes broke: a ship whose wallet runs low is given credits by a rich ship
of its division.

Run by hand.

```
wallet.py [check]            every wallet against the floors; HALT for a pilot under 3,000 cr
wallet.py topup [--dry-run]  give each pilot under LOW credits up to TARGET from a rich ship of its division
wallet.py sweep [--dry-run]  the part above KEEP_SHIP of the richest ships to the leader, the leader's into the treasury
wallet.py fund <pilot> <credits> --why "<text>" [--hours H]
                             the treasury pays one pilot for a buy: the next pass the leader stands docked withdraws the
                             credits and gives them; the sweep and the top-ups leave that much with the pilot for H hours
wallet.py fund --show        the funds on record and their state
--data <dir>                 the unit's data folder (default: the fleet's)
```

### `watchdog.py`

Check whether the fleet is advancing across turns or stuck in loops, bottlenecks, or
idle states.

Run by hand.

```
watchdog.py [show] [--hours N] [--json] [--save] [--data <dir>] [--root <dir>]
watchdog.py check [--hours N] [--data <dir>] [--root <dir>]
--hours N      window for run-loop and log checks (default 4)
--json         print structured JSON instead of plain text
--save         update <data>/fleet/watchdog.state.json for cross-turn velocity tracking
--data <dir>   the unit's data folder (default /srv/collective/data)
--root <dir>   the repository's game/ folder (default: the parent of this file's folder)
```

### `workclass.py`

Whose work a route is: the work class of every route and the classes each role flies

Run by hand.

```
workclass.py show [<route id>] [--strict]   the class and the roles of one route, or the count of routes per class;
                                            --strict: the answer with the switch off and with it on
workclass.py roles [--strict]               the classes each role flies (--strict: in both states)
workclass.py plans [--strict]               per role plan (game/routes/plans/<role>.json): the routes that are not of
                                            its class (--strict: in both states)
workclass.py sales                          the dry run of the sale rule: the routes it would refuse with the switch
                                            on, per class and per Admiral (whose role plans name them for a role that
                                            is not the traders'), each with the roles it would be closed to
--data <dir>   the unit's data folder whose switch is read (default FLEET_DATA_ROOT or /srv/collective/data)
```

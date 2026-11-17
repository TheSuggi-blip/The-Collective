---
name: fleet-index
id: 20261115T195732Z
tier: intel
author: Unity
---

# index.md -- The Fleet's Scripts

Built by `python3 -B scripts/fleet-index.py` from the docstring of every script in this
folder; never edited by hand. Scripts listed: 30.

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
| `board.py` | The board of a division: what each of its ships does now, its plan, what is planned, and what its runs earned. | By hand |
| `census.py` | Read one system whole with one pilot: every place's deposits and creatures, and the station's order book and mission board. | Runner (`census` routes) |
| `collective_mcp.py` | The collective MCP server: the fleet's knowledge and the door to its ships, as tools for every member. | By hand |
| `craftbook.py` | Answer what can be made, fitted and built: a recipe, everything a thing takes, and what our stored goods can become. | By hand |
| `dispatch.py` | Keep every pilot at work: give each free pilot the next task of its role. | Service |
| `division.py` | Who commands which ship, whose plan is whose, and the check every fleet script runs before it drives a ship. | By hand |
| `empire.py` | Keep the picture of our empire: the faction and its limit, the bases and offices we own, the systems they stand in, the sites we may build on, and what the faction can build next. | By hand |
| `fill.py` | Keep every ship of a division at work: say why ships wait, and fill the plan with the work that stands open. | By hand |
| `fleetfile.py` | Write the roster into a member's own FLEET.md: one table, every ship of the member on one line with its kind, its hull and the task it is on now. | By hand |
| `gate.py` | Small client for the fleet engine's gate, with the division's lock. | By hand |
| `guard.py` | Keep one pilot at the place where another route's ship of ours works, for as long as that ship works there. | Runner (`guard` routes) |
| `hive.py` | The fleet's figures from its own readings: money, routes and their history, levels, what the work carries, what a base takes, a system. | By hand |
| `hunt.py` | Hunt grazers at one place, loot the carcasses and sell what the kills bring. | Runner (`hunt` routes) |
| `inbox.py` | Read what other pilots write to our ships and say near them, keep every message once, and file the ones that are for us. | Service |
| `ledger.py` | Keep the fleet's books: what we own and where it lies, and how every order book moved. | Service |
| `loot_own.py` | Loot every carcass and wreck at the pilot's place that the pilot itself killed. | By hand |
| `mine.py` | One pilot mines at one field for a set time, through the engine's mining loop. | Runner (`mine` routes) |
| `observe.py` | A member writes down what it saw in the game (a scan far away, a price at a station we read no book of, a fight with a species) as one checked line of its division's own record; the store makes the lines one SQL table, `observations`. | By hand |
| `plan.py` | Each division's plan file: every ship with the routes it flies, in their order; the dispatcher sends the ships by it. | By hand |
| `plate.py` | Make our pilots' stored creature carapace into armor plate where each is docked, and sell plates into the bid there. | By hand |
| `route_run.py` | Fly one pilot along a route file: dock at each stop and do what the stop says. | Runner (`circuit` routes) |
| `routemaker.py` | Find every way to earn that the fleet's own data shows, cost it, and write the route file for it. | Service |
| `routes.py` | Check the route files, write their index, and attach what the runs measured. | By hand |
| `runhost.py` | One program that flies the runs the dispatcher starts, each run as a thread instead of a process. | Service |
| `sight.py` | What our ships see where they are: the pilots they meet, and a first read of a system nobody read. | Service |
| `stash.py` | Store what a docked pilot carries in its own storage at that station, so that its hold is free for the next route. | By hand |
| `store.py` | Keeps the fleet's history and its current state in one SQLite file: the runs, the price moves and the census readings with their sums by hour and by day, the members' own observations, and beside them what the fleet's own files say now. | Service |
| `surplus.py` | Say per item what the fleet holds beyond what its build targets reserve: the surplus a trader may sell, where it lies and its best bid. | By hand |
| `taxes.py` | Keeps each pilot's weekly tax apart, so that no run and no hour reads it as a loss. | By hand |
| `wallet.py` | No ship of ours goes broke: a ship whose wallet runs low is given credits by a rich ship of its division. | By hand |

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

### `empire.py`

Keep the picture of our empire: the faction and its limit, the bases and offices we own,
the systems they stand in, the sites we may build on, and what the faction can build
next.

Run by hand.

```
empire.py collect [--ladder]     one reading, written to <data>/empire/empire.json (--ladder: read the cards again)
empire.py write [--commit]       governance/empire.md from the data file; --commit commits it by path as Unity
empire.py show
empire.py check
--root <dir>   the repository's root (default: two folders above this file)
--data <dir>   the unit's data folder (default /srv/collective/data)
```

### `fill.py`

Keep every ship of a division at work: say why ships wait, and fill the plan with the
work that stands open.

Run by hand.

```
fill.py [status] [<Member>|<role>|all]
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

### `guard.py`

Keep one pilot at the place where another route's ship of ours works, for as long as
that ship works there. Reads only: it never fires, never buys and never mines; in a
fight it flees.

A runner: the dispatcher starts it for a route of the kind `guard`; by hand only for a test with one free pilot.

```
guard.py <pilot> <system_id> <poi> --guards <route id> --station <system:poi:base> [--minutes M] [--route ID]
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
hive.py levels [<Member>|all]
hive.py capacity
hive.py base outpost|station
hive.py system <system id>
hive.py learnings [--hours N]
hive.py standing [<Member>|<role>|all] [--hours N]
hive.py tasks [--hours N]
hive.py forecast [<Member>|all] [--hours N]
hive.py refill
hive.py briefing [<Member>|all] [--hours N]
hive.py store [--hours N]
hive.py store price <item id> [--hours N]
hive.py inventory [stations] [--item <item id>] [--top N]
hive.py empire
hive.py surplus [--top N] [--kind <kind>] [--item <item id>] [--all]
hive.py reserve
hive.py flow [<Member>|all] [--hours N]
hive.py sql "<SELECT or WITH statement>" [--limit N]
hive.py schema [<table or view>]
--root <dir>   the repository's game/ folder (default: the parent of this file's folder)
--data <dir>   the unit's data folder (default /srv/collective/data)
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
routes.py check | index | measure                [--root <dir>] [--data <dir>]
routes.py measure --write <route id>... | --role <role> | --all
                  writes the measured block of the routes named, of a role's plan, or of every route (the hourly
                  job); without one of the three it writes nothing and says so
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

### `wallet.py`

No ship of ours goes broke: a ship whose wallet runs low is given credits by a rich ship
of its division.

Run by hand.

```
wallet.py [check]            every wallet against the floors; HALT for a pilot under 3,000 cr
wallet.py topup [--dry-run]  give each pilot under LOW credits up to TARGET from a rich ship of its division
--data <dir>                 the unit's data folder (default: the fleet's)
```

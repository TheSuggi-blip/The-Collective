---
name: chain-flown-past-runner-crash-signal-fragments-per-pilot
id: 20261116T052249Z
tier: report
trigger: session-end
author: Mercury
tags: [trade, missions, runner-fault, gas, capacity]
links: [reports/2026-11-16_mercury_node-beta-chain-opened-to-fleet-plasma-one-load.md, reports/2026-11-16_unity_steady-net-doubles-on-fitted-harvesters-admirals-build-their-own-tools.md, game/routes/guidebook/trade.md, game/routes/voidborn-conductive-lattice.json, game/routes/voidborn-signal-fragments.json]
---

# Trade -- Ten traders flew the Node Beta chain past a runner crash for +109,213 cr once; a 7,000 cr mission is offered at navigation 3, to 46 pilots of the fleet; no trade repeats

## Situation

This report covers the time from my previous report,
`reports/2026-11-16_mercury_node-beta-chain-opened-to-fleet-plasma-one-load.md`
(2026-11-16 03:36 UTC), to 05:50 UTC: the scheduled turn of 04:30 UTC.
I started it under `orders.log` ENT-011 and read ENT-012 (in force from
04:56 UTC) in the middle of the turn, at 05:23 UTC. ENT-012 keeps my
block of ENT-011 and adds three things for me: the Node Beta chain in
every plan, with its `max_ships` and `max_pilots` kept by me at what
the silver carries; the station's list (S6): the asks for salvage
metal, anchor plate, alloy scale and foil scale, and whether a station
core or an outpost kit is on offer anywhere we read; and F21, what
repeats is done by a script. The Fleet Admiral's newest report in
force when I started was
`reports/2026-11-16_unity_steady-income-positive-on-ice-harvester-bounds-the-fleet.md`;
hers of 05:02 UTC came during the turn.

```
Ships: 20/20 active, grounded: 0, lost: 0 (data/fleet/ships/, every hull 75 of 75)
Credits: start 870,219 (03:35 UTC, previous report), end 982,755 (05:26 UTC, hive.py fleet), net +112,536
Output: 10 traders flew the whole Node Beta chain (all 20 now have it); 1 Signal Fragments; 2 gas tests closed
```

Steady money, rewards paid once left out (`hive.py standing`, four
hours to 05:26 UTC): -3,196 cr over 80 ship-hours on the clock, -40 cr
per ship-hour over all 20 ships; 8.2 ship-hours flown at -391 per
ship-hour; 115,542 cr paid once apart. Trade's steady change per hour
in `hive.py history`: -379 cr to 04:27 UTC and -2,466 to 05:22 UTC;
the last hour's costs read 2,706 cr (`hive.py fleet`, 05:26 UTC; fuel
and repairs are not split per division there). The scale (`hive.py tasks`, 05:00 UTC):
the best route with two runs or more, fit-ice-harvester, 12,564 cr per
ship-hour; the best repeating work, mine-ruchbah-ice-belt, 8,950 over
16 runs (Mining's report of 04:37 UTC); 0 for a ship without work.

Fill gate, last line (`fill.py check trader`, 05:48 UTC): see Plans.
No ship of mine is held by hand.

## Activities

**The Node Beta chain, past a runner fault.** At 04:35 UTC six traders
waited docked at Ironlight Crossroads with empty holds, and their logs
(a trader's log in `data/routes/logs/`) showed the circuit runner crashing
at the silver buy: since commit e2fcbe0 (01:09 UTC) the accept step had
overwritten the name of the function the buy calls, and a crashed run
wrote no row. I wrote the fault to the Fleet Admiral (requests.log
ENT-096), into errors.log (ENT-039) and to the fleet (queue.log
ENT-074). Then I held the ten traders that had not flown the chain and
flew it in split scratch routes that buy before they accept: Ironlight
silver and the Lattice hand-in, then the Central Nexus crystals, the
Resonance hand-in and Final Calibration at Node Gamma; four traders
first accepted Lattice at Node Beta. Result
(`data/routes/runs.jsonl`, 04:40 to 05:16 UTC): 24 runs, +109,213 cr,
110,970 cr paid once, 4.6 ship-hours: +10,942 cr for a pilot that
already held the mission, +10,893 for one that took it. All 20 traders
now have the chain. The Fleet Admiral fixed the runner at 04:49 UTC
(requests.log ENT-098). Under ENT-012 I set the route to 146 pilots and
10 ships at a time (commit 98912f8): the silver ask stood at 80, 120
and 200 units at 04:41, 04:58 and 05:21 UTC after we bought 200 within
ten minutes, so it regained at least 120 in 8 minutes and caps at 200;
ten ships buy about 375 an hour. The crystal ask read 420 cr for 822
(05:23 UTC): 54 pilots. Offered to every division in queue.log ENT-082.

**Signal Fragments, a new mission.** A Central Nexus board read through
`gate.py` (04:49 UTC) listed Signal Fragments, 7,000 cr for docking at
Node Beta, Node Gamma and Central Nexus. One trader flew it by hand:
+6,909 cr after 91 cr of fuel in 14.3 minutes. As a route
(`voidborn-signal-fragments`, max_ships 3) it went to six more traders
and the board refused all six: -221 cr in sum (05:07 to 05:18 UTC). It
left the plan at 05:13 UTC. Then I read `get_missions` (free for any
ship) for each of the 30 pilots docked at Central Nexus at about 05:28
UTC and set the answers beside their skills: offered to 4 of 4 with
navigation 3, to 0 of 25 with navigation 2, whatever their piloting or
exploration. 46 pilots of the fleet have navigation 3 or more (Mining
16, Intel 10, Military 9, Command 7, Trade 2, Logistics 2): about
310,000 cr once. Told to every division with the way to fly it by hand
(queue.log ENT-085); a route condition by skill asked of the Fleet
Admiral (requests.log ENT-109). The other trader with navigation 3
flies it by hand at the end of the turn.

**Gas tests closed.** mine-stellar-siphon and mine-lesath-gas-cloud,
one run each at 03:13 UTC: -276 and -330 cr, neither sold (the mine
runner's dock fault; its sale step was changed by the Fleet Admiral at 04:47 UTC, cause still unknown); the Lesath hold
held no plasma, the one gas it sells. At 04:42 UTC every gas bid at our
stations stood at 2 cr except plasma at Node Beta, 100 cr for 4. Both
left the plan at 04:46 UTC; the 65 gas units of one hold went to
storage at Central Nexus, none sold under its worth.

**First Steps.** Six traders hold First Steps in the Void
(`get_active_missions`, 05:02 UTC): Logistics' route
`voidborn-first-steps` is at the head of my plan since 05:07 UTC (1,000
cr once, 810 cr a run over 26 fleet runs).

**Books and crafts.** Two distinct reads of seven books (04:13 to 04:58
UTC, `held.py`): the best held gap is 400 cr per hold. Control nodes
by hand: about +123 cr a craft, boards for 11 crafts (05:00 UTC). No
trade or craft carries a load.

**S6.** Salvage metal, anchor plate, alloy scale and foil scale have no
ask in any of the eight books we read (04:57 to 05:25 UTC; Nova Terra
03:22 UTC); alloy scale is bid 213 cr for 20 at Synchrony Hub. No
station core is on offer; one Outpost Kit stands at Ironlight at
216,825 cr (05:25 UTC). queue.log ENT-082 gave the read times as 05:22
to 05:25 UTC; the books ranged from 04:57 UTC.

**Capacity (F18).** Missions that pay once still open to traders: First
Steps for six holders (about 4,900 cr), Signal Fragments for pilots the
board offers it to (not measured). For the fleet (`hive.py capacity`,
about 04:47 UTC): the chain for about 126 pilots, at least 45 an hour by the
silver; First Steps 128 pilots, First Hunt 125, Cracking the Shell 144
behind First Hunt. Gaps load 4 units at best. Repeating trade work
employs 0 of my 20 ships; Trade needs no more ships.

**Levels.** Trading 2 for all 20 traders (10 at 03:25 UTC); piloting 5
for two, 4 for thirteen, 3 for five (data/fleet/ships/, 05:16 UTC).
Knowledge files changed: `voidborn-delivery-missions.md` and
`voidborn-order-books.md`.

## Problems

**The chain stood still for 3.5 hours without a trace.** No run of
voidborn-conductive-lattice is on record from 00:21 to 04:40 UTC.
Cause: the runner fault of 01:09 UTC (errors.log ENT-041, the Fleet
Admiral's), and a crashed run wrote no row, so every tool showed the
pilots docked and free. My own part: in my turn of 03:02 UTC I saw the
six traders' runs restart at 03:35 UTC and reported "cause not found"
without opening one log, which held the traceback (errors.log ENT-039).
Done: the hand runs above; the fix; a pitfall in my skill trade-books
that sends me to the pilot's log in the same turn.

**Signal Fragments: six refused runs, -221 cr.** Cause: I put a `once`
route into the plan on one pilot's accept, although a board read at
05:04 UTC by another pilot already lacked the mission, and `max_ships`
3 limits ships at one time, not runs (my own pitfall from the soma gap
of 2026-11-15, errors.log ENT-027). It is the class of errors.log
ENT-036 and ENT-038 (a figure of some pilots taken for all). Done: the
route out at 05:13 UTC; the rule that a second, different pilot is
offered a mission by hand before its route enters a plan, in my skill
and knowledge file.

**The gas tests measured the runner, not the gas.** Both runs ended
"not docked for the sale"; their figures say nothing of the field. The
books decided the matter instead.

**Fill gate HALT on a place no trader should take.** The one open place
it names is `trade-plasma-gas-...` (buys plasma at Ironlight for the
Node Beta bid, which Logistics' sale emptied at 05:10 UTC, queue.log
ENT-079); a route that buys goods is never added by a script (orders
F8). Zero asked for this in fill.py (requests.log ENT-095, accepted).

**A pilot named in two public log entries.** requests.log ENT-096 and
errors.log ENT-039 cite one trader's log by its file name, which names
the pilot; the logs are append-only and stay so. Cause: I copied the
path; the append command checks no pilot names, as the report gate
does. The gate against pilot names is owed by the Fleet Admiral (orders
ENT-012); until then I write "a trader's log in data/routes/logs/".

Also checked, nothing found: ships lost or hit (none, every hull 75);
hands left on ships (none); wallets under 3,000 cr (lowest about
38,000 cr).

## Plans

Inside ENT-012, chosen by me:

1. **The chain for the fleet.** Read the silver ask at Ironlight and the
   crystal ask at Central Nexus at my next turn (08:30 UTC) and keep
   `max_ships` at what both carry: lift past 10 if the silver regains
   as fast while ten fly, lower it if a run finds the silver gone
   (the runner rests that pilot an hour). `max_pilots` stays 146.
2. **Signal Fragments.** The other trader with navigation 3 flies it
   by hand once its Lesath run is over. When the Fleet Admiral's route
   condition by skill exists (requests.log ENT-109), the route goes
   into my plan with it, and I tell every division to add it; a trader
   that reaches navigation 3 then gets it by itself.
3. **The four hours between turns.** The trader plan holds First Steps
   for six holders, the booked once routes, the chain (closed to
   traders, booked), census-frontier and park. Expected: about 4,900 cr
   paid once, then 0 per ship-hour for docked ships and about -632 per
   ship-hour for a census read. The fill gate's last line of 05:48 UTC
   is in the session entry; its HALT names only the plasma import,
   which no script may add.
4. **Plasma import.** Flown once by hand only when the Node Beta bids
   stand again at two levels (`ledger.py prices plasma_gas`); a route
   only with `requires.bid`.
5. **S6.** Read the station list's parts that are bought, not made, in
   every new book Intel brings, and say which stand on offer.
6. **F21.** The split run around a runner fault is a pattern in my skill
   trade-books, not a script: the fault it served is fixed. If Signal
   Fragments proves to be offered by skill, its by-hand test becomes a
   route with the condition, not a hand loop.

What would change this: Zero's word that ice routes have places for
traders; the craft step and `requires.bid` (owed by the Fleet Admiral
by 12:00 UTC); a new mission giver on a board.

## Suggestions

1. **A route condition by skill** (`requires.skills`, a new field of a
   route, the Fleet Admiral's; asked in requests.log ENT-109). Reason:
   Signal Fragments is offered at navigation 3 only (30 boards), worth
   about 310,000 cr once to 46 pilots; a once route without the
   condition spends one run per refused pilot (six here, -221 cr;
   Cracking the Shell cost Mining -286 and Logistics -208 the same way)
   and marks it done. Cost: one field in dispatch.py and fill.py, beside
   `requires.booked`.
2. **A refused accept is no try for every once route**, not only for
   those with `requires.booked`. Reason: as now, a refused pilot is
   "done" and never gets the mission when it qualifies later. Cost:
   the logic of ENT-102, applied to all once routes. The Fleet
   Admiral's to decide.
3. **No new traders** (F5). Reason: repeating trade work employs 0 of
   20 traders; the money is in missions that pay once, and every trader
   has flown the ones that exist. The cost of waiting ships is 0.
4. **The Crimson Resonance** (8,500 cr, the next link of Signal
   Fragments): a dock at The Rampart Checkpoint and 5 titanium alloy at
   Blood Forge, Crimson space 17 and 20 jumps out. Whether a ship of
   ours flies into another empire's military installations for it is
   beyond my orders: the Fleet Admiral's, with Intel's read of the law.

## Learnings

From this turn's learning capture.

**A board is one pilot's board.** Signal Fragments paid +6,909 cr to
one trader and was refused to the next six (`data/routes/runs.jsonl`,
04:49 to 05:18 UTC); 30 boards read beside the pilots' skills showed
the condition: navigation 3. Cracking the Shell showed a condition for
drones (First Hunt booked). My division now reads the boards of the
docked pilots (a free read) before a `once` route enters a plan. For
the fleet: a mission's figure counts only for pilots the board offers
it to; one pass of free reads finds who they are.
Kept in: `knowledge/voidborn-delivery-missions.md`.

**A waiting ship whose run restarts is read in its log at once.** The
crash wrote no row, so every tool showed the six traders docked and
free for an hour after I first saw their runs restart (03:35 to 04:36 UTC)
(the traders' logs in `data/routes/logs/`, errors.log ENT-039). For the fleet:
the run row is the record of what happened, the log of what went wrong;
when the two disagree with the plan, open the log. Kept in: my skill
trade-books (pitfalls).

**A route the runner cannot fly whole can be flown in parts.** Split
scratch routes whose stops avoid the failing order, flown per pilot
with a hold and a release, brought +109,213 cr in 36 minutes while the
fix was under way. Kept in: skill trade-books; the knowledge file above.

**Gas has no buyer at depth in our space.** Every gas bid at our six
stations stood at 2 cr except plasma at Node Beta, a few units (04:42
UTC); the two gas tests proved nothing else. My division reads the bid
a mining test sells into, level by level, before the test flies. Kept
in: `knowledge/voidborn-order-books.md`.

Confirmed: no buying-and-selling gap carries a load (fourth turn
running); the silver at Ironlight regains fast. Repeated mistake:
`max_ships` caps ships at once, not runs, written in my skill since
2026-11-15 and missed again; the fix now is the two-pilot rule, which
fires before a route exists. Open: what The Crimson Resonance asks of
the law of Crimson space.

Skill: trade-books changed -- pitfalls (one pilot's board, read the log of a restarting run, split runs, non-book files in the market folder); craft.py skips files that are no books

## Cross-links

- `reports/2026-11-16_mercury_node-beta-chain-opened-to-fleet-plasma-one-load.md` -- my previous report.
- `reports/2026-11-16_unity_steady-income-positive-on-ice-harvester-bounds-the-fleet.md` -- the Fleet Admiral's report in force when the turn started.
- `reports/2026-11-16_unity_steady-net-doubles-on-fitted-harvesters-admirals-build-their-own-tools.md` -- her report of 05:02 UTC, with orders.log ENT-012.
- `game/routes/guidebook/trade.md` -- the Standing Plan and every figure above.
- `game/routes/voidborn-conductive-lattice.json` -- the chain, 146 pilots and 10 ships at a time.
- `game/routes/voidborn-signal-fragments.json` -- Signal Fragments, in no plan.

---
name: steady-net-doubles-on-fitted-harvesters-admirals-build-their-own-tools
id: 20261116T045917Z
tier: report
trigger: session-end
author: Unity
tags: [fleet, economy, tools, faction, station, strategy]
links: [reports/2026-11-16_unity_steady-income-positive-on-ice-harvester-bounds-the-fleet.md, reports/2026-11-16_zero_orphan-loops-stopped-harvesters-fitted-per-station.md, reports/2026-11-16_zero_ironlight-harvesters-fit-the-waiting-miners.md, reports/2026-11-16_apophis_cinder-sylphs-pay-herds-bound-the-hunt.md, reports/2026-11-16_apollo_harvester-made-by-hand-pays-only-from-own-silicon.md, reports/2026-11-16_mercury_node-beta-chain-opened-to-fleet-plasma-one-load.md, reports/2026-11-16_oracle_halo-drifter-drop-sells-nova-terra-holds-no-trade.md, reports/2026-11-16_oracle_first-steps-and-atlas-hunt-pay-node-beta-chain-crashes.md, governance/strategy.md, communications/orders.log]
---

# The Collective -- Steady net doubled to 104,000 cr an hour as 47 harvesters were fitted; the Admirals now build their own tools; a station is the sixth standing order

## Situation

This report covers 2026-11-16 01:46 UTC, the time of my previous
report
(`reports/2026-11-16_unity_steady-income-positive-on-ice-harvester-bounds-the-fleet.md`),
to 05:00 UTC. In it the Admirals flew a round started by hand (02:53
and 03:02 UTC) and the first scheduled round (from 04:00 UTC).

Fleet totals, from `game/fleet/hive.py fleet` at 04:52 UTC: 146 ships,
66 at work, 80 docked; credits 6,048,164; steady net of the last hour
104,094 cr (income 130,202, costs 26,109, of them fuel 25,892); over
six hours 49,065 cr an hour. At 01:43 UTC the same reading gave 38
ships at work, 5,819,298 credits and +51,852 cr. The ship files of
04:52 UTC show 47 Ice Harvesters and 3 Gas Harvesters fitted, against
14 and 0 at 01:40 UTC.

Every earning below is in credits per ship-hour (orders F19). The
scale: the best route that repeats, `mine-ruchbah-ice-belt`, made
9,044 over 18 runs (`hive.py routes`, 04:58 UTC); a ship without work
makes 0. From `hive.py tasks`, the four hours to 04:52 UTC:

| Division | Ships | Per ship-hour, all ships | Per ship-hour flown | Steady net an hour (04:52) |
|---|---|---|---|---|
| Mining | 40 | 1,055 | 4,017 | 85,671 |
| Military | 30 | 229 | 1,100 | 11,214 |
| Command | 16 | 20 | 64 | 13,899 |
| Trade | 20 | -20 | -399 | -3,019 |
| Logistics | 20 | -34 | -238 | -1,315 |
| Intel | 20 | -111 | -408 | -2,356 |
| Fleet | 146 | 315 | 1,488 | 104,094 |

One line per division from its Admiral's newest report:

- Mining (Zero, 04:36 UTC): 27 of 40 at work at 04:30 UTC, 12
  waiting; 1,006 per ship-hour over all ships, 5,178 flown; 9 of 18
  mine runs between 04:00 and 04:33 UTC ended unsold.
- Military (Apophis, 03:29 UTC): 48 hunts, 101 kills; cinder-sylphs
  paid 3,230 per ship-hour on their first test; herds bound the hunt.
- Logistics (Apollo, 03:35 UTC): one Ice Harvester I made by hand for
  2,891 cr of bought inputs; 14 haulers wait.
- Trade (Mercury, 03:38 UTC): ten traders hold the three Node Beta
  missions; twelve traders waited at 03:31 UTC.
- Intel (Oracle, 04:55 UTC): 12 home reads, 9 frontier systems added;
  net +805 cr in the hour.

Trade, Logistics and Military had not reported on the round of 04:00
UTC when this was written: their turns were in flight.

## Strategy

The strategy in force is `governance/strategy.md`: ten principles and
four phases, and the fleet stands in phase 1, income. Since version 3
of the constitution the two rank side by side, on Suggi's approval.

What Suggi decided in the period, in his order (my `DECISIONS.md`,
D110 to D122):

- Every earning is given in one unit, credits per ship-hour, beside a
  scale, and every figure the fleet decides on is collected by a
  script. Orders F19; `hive.py tasks`, `standing` and `refill`.
- Work on his command station is my own hand. The layout he asked for
  is live and stays; the Metrics page no longer redraws under the
  reader (commit 826979b).
- The six turn jobs run on schedule; I report to him after each round.
- No Outpost Kit now. The command ships level and earn like the rest.
- Each Admiral starts its turn from its standing fleet and its
  guidebook (preflight and session-end changed).
- At about 04:05 UTC: a sixth standing order, a base and then a
  station with its materials gathered (S6); every ship into the
  faction, with shared storage and shared money (F11); the fleet's
  spare credits carried by the six flagships (F20); the Admirals
  command by script and build what they lack themselves (F21). The
  orders otherwise stand as they are.

What I made of it, as proposals of mine inside those decisions:

- The station. The tool `base_plan` (kind=station, 04:15 UTC) prints a
  fee of 5,000,000 cr and one station core, made only in a station
  core foundry of 38,000,000 cr: 43,000,000 cr in all, 28 of 30 raw
  inputs short (iron ore 491,400 needed, 59,658 held). That is 413
  hours of this hour's steady net and 876 of the six-hour figure. My
  reading: income first, the faction's storage second, and each
  division reads its part of the list now.
- The faction. Read from the game between 04:33 and 04:42 UTC: 16
  members, no base.
  The cap read 50 on 2026-11-15; a lockbox is listed at 200,000 cr.
  My order of steps: lockbox, members to the cap, recruitment office,
  treasury. The office's live costs are not read yet.
- The gate for the Admirals' own changes: `scripts/fleet-build.sh`
  refuses the few files one fault in which stops every ship.

The orders changed twice: `orders.log` ENT-011 (02:52 UTC) and ENT-012
(04:54 UTC).

## Divisions

**Mining** (two reports). Zero fitted the waiting miners from the
harvesters of Ironlight Crossroads at half our price; the division's
steady net was 85,671 cr an hour at 04:52 UTC (`hive.py fleet`). My
judgment: the thread holds; what it planned at 00:36 UTC (fit every
harvester) shows as done, and its figures agree with the fleet's.
Suggestions: a check for loops without a runner after an engine
restart: accepted, my turn of 06:30 UTC (`requests.log` ENT-083). The
dock step of mine.py: done (commit 0951055); the cause of the unsold
runs is not proven, the next note will name it. The loss stop reads a
run's notes: accepted and done (commit ee84c19). Ice sold at Central
Nexus first: his to route. fill.py counts only work a role may take:
accepted, 06:30 UTC (ENT-095). No new miners: agreed; about 34 ice
places stand against 40 miners.

**Military.** Apophis tested every untested species the orders named
and found the cinder-sylph; a herd regains 1.4 to 3.7 animals an hour,
so repeating hunts employ about 8 of 30 drones. Judgment: sound, and
inside its orders. A guard post for waiting drones: open, the route
kind is owed by me (ENT-070). No Vigil hull yet: agreed. A refused
accept is no try: done as `requires.booked` (commit 9d4344b).

**Logistics.** Apollo proved that a harvester made by hand costs about
680 cr from our own silicon and crystal against an ask of 1,413 cr.
Judgment: the chain is worth its inputs. Mining's silicon and crystal
as input: open between Apollo and Zero (ENT-088). A silicon field read
by Intel: accepted, ENT-012 block ZERO. A once route added only after
it was offered to the role: accepted with ENT-095. Each division sells
its own soma: accepted; `game/fleet/stash.py` empties a hold.

**Trade.** Mercury opened the Node Beta chain to the fleet: +10,893 cr
once per pilot. Judgment: the best one-time money we have, and my own
fault stopped it from 01:09 to 04:49 UTC (`errors.log` ENT-041). A
check for typed times in notes: accepted, not built. A sell that walks
the levels: accepted; a runner's step, now his to build (F21) or mine
after the owed list. `requires.bid` first: accepted, owed (ENT-065).
The chain in every plan: accepted, ENT-012. Trade's size: no trader is
born; the idle ones are an open question below.

**Intel.** Oracle found the chain's crash from the pilots' logs,
withdrew an offer made before its first result, and names its own
fourth claim wider than its check. Judgment: honest and inside its
orders. Why a hunt step ended: accepted (ENT-092). A held mission
listed as open work, and a skipped once run not counted as done:
accepted with ENT-095 and ENT-083. The empty-hold check by value:
owed. Lending scouts: Oracle proposes none until a gas route measures
above the census's cost; I agree. The first outpost beside Achernar:
Suggi's, later.

Where two divisions touch: three gas tests of Trade and Logistics sell
into one thin Node Beta bid, as both reports say; their first figures
measure each other.

## Plans

The orders are `orders.log` ENT-012. What each division does until its
next turn:

- Mining: keeps every harvester ship on ice, reads the second RESULT
  lines of the Central Nexus tests, and names for S6 the fields that
  carry iron, carbon, silicon, nickel and gold.
- Military: one hunter on each paying herd, First Hunt for the drones
  that lack it, and for S6 what stands at the sites Intel names.
- Logistics: the harvester chain from our own goods, the station's
  stock list from `base_plan` each turn.
- Trade: the Node Beta chain at what the silver carries (about 34
  pilots in four hours by Mercury's reading), the gas tests, and for
  S6 the asks for the inputs without a source.
- Intel: the census, the chain for its scouts, three sites for a
  station.
- Every division: the chain in its plan, and what it did by hand
  twice written as a script (F21).

What I do myself, in my turn of 06:30 UTC and in this order:

1. Read the reports of the round of 04:00 UTC and answer what is new.
2. The dispatcher ends a loop that flies without a runner (ENT-083);
   the battle stance flee and the pilot whose runs fail at the first
   stop (ENT-090); why a hunt step ended (ENT-092); what fill.py
   counts as open (ENT-095).
3. The history store of `queue.log` ENT-058: a worker builds it in a
   scratch copy; I read it line by line, test it with a cut record and
   install it as a service.
4. The scale line of `hive.py tasks`, which names a fitting route as
   the best route: the best route that repeats.
5. The faction: the live cost and conditions of the lockbox and the
   offices, read from the game; nothing is paid before Suggi has the
   figure.
6. The purse script (F20), first as a rehearsal that moves nothing.
7. The owed changes of the older requests, `requires.bid` first.

No diplomacy is planned: no word goes to another player.

## Open Questions

1. **The faction's first payments.** The lockbox is listed at 200,000
   cr and the docs name 75,000 cr for the first recruitment office;
   the first building is paid by the leader's own wallet, which held
   about 35,000 cr in this session's fleet file. Options: pool about 275,000 cr into the flagship by credit
   gifts now, or wait for the purse script. I recommend the pooling,
   once I have read the live conditions in my next turn. What would
   change it: a condition the game adds (a skill, materials) that we
   do not meet.
2. **Who joins first.** The cap read 50 and 16 are in. I recommend the
   20 haulers and 14 miners: the miners fill the storage, the haulers
   empty it. All 146 need the office that carries 200 members,
   2,000,000 cr by the docs: later, from steady income.
3. **What a ship keeps (F20).** I recommend 13,000 cr, the dearest
   route's `min_credits`; at 41,426 cr a ship (04:52 UTC) that moves
   about 4,100,000 cr to the six flagships. What would change it: a
   route that asks more.
4. **The ships without repeating work.** Trade has such work for 2 of
   20 ships (Mercury), Military for about 8 of 30 (Apophis); ice has
   about 34 places (Zero). Options: leave them docked at no cost;
   or let them gather the station's ores into the faction's storage
   once it stands, which earns nothing now and builds S6. I recommend
   the second, haulers first; it needs your word, since your rule is
   no mining for storage.
5. **A tougher hull for Military** (Apophis): no purchase now; a test
   on prey over 100 hull needs your word beyond F9. I recommend
   waiting: the economy first.

## Learnings

From this session's learning capture.

**An option read in a help text is not a mechanism until it ran
once.** I planned the round by hand around `cron resume --at` and
wrote it into a script, my job's prompt, a skill, a notice and a word
to Suggi; Hermes refuses it for a recurring job, and the scheduled
round followed an hour later (`errors.log` ENT-037). I now run a
mechanism once on one job and read it back before it is written
anywhere. For the Admirals: Oracle names the same class in its own
work. Kept: unpromoted (`LEARNINGS.md`).

**A run that crashes must leave a row.** My change of 01:09 UTC
crashed every run with a buy after an accept; no row was written, and
the best one-time route stood still for three and a half hours until
two Admirals read pilots' logs (`errors.log` ENT-041). Every run now
writes its row on the way out, and a test reads the runner's module
level. For the fleet: after a runner change, count the runs per route
an hour later. Kept: unpromoted.

**A tool is proven where it runs.** The collective tools passed in my
shell and failed inside a member's Hermes: a server keeps the code and
the bare environment it started with (`queue.log` ENT-060, ENT-071).
The server now answers through the file on disk. Kept: unpromoted, and
my skill collective-mcp.

**One builder for six members is the fleet's queue.** Nine requests
reached me in two rounds (`requests.log` ENT-083 to ENT-097) while six
older ones were still owed. The
Admirals now build through a gate. Kept: unpromoted.

**Fitting the tool moved the fleet as the count said.** Harvesters 14
to 47, ships at work 38 to 66, steady net +51,852 to +104,094 cr.
Kept in `knowledge/fleet-employment.md` (updated).

Repeated: a claim wider than its check, the class of `errors.log`
ENT-031; its fix is still a rule I follow, not a check that fires.

Skill: collective-agents changed -- resuming a turn job, a round by hand, the report gate's time
Skill: collective-mcp changed -- running servers, the reload script, the search's environment

## Cross-links

- `reports/2026-11-16_zero_orphan-loops-stopped-harvesters-fitted-per-station.md`, `reports/2026-11-16_zero_ironlight-harvesters-fit-the-waiting-miners.md` -- Mining.
- `reports/2026-11-16_apophis_cinder-sylphs-pay-herds-bound-the-hunt.md` -- Military.
- `reports/2026-11-16_apollo_harvester-made-by-hand-pays-only-from-own-silicon.md` -- Logistics.
- `reports/2026-11-16_mercury_node-beta-chain-opened-to-fleet-plasma-one-load.md` -- Trade.
- `reports/2026-11-16_oracle_halo-drifter-drop-sells-nova-terra-holds-no-trade.md`, `reports/2026-11-16_oracle_first-steps-and-atlas-hunt-pay-node-beta-chain-crashes.md` -- Intel.
- `governance/strategy.md` -- the strategy in force.
- `communications/orders.log` ENT-011 and ENT-012 -- the orders of the period.
- `communications/errors.log` ENT-031, ENT-037, ENT-041 -- my faults of the period.

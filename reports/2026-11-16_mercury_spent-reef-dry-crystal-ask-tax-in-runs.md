---
name: spent-reef-dry-crystal-ask-tax-in-runs
id: 20261116T130055Z
tier: report
trigger: session-end
author: Mercury
tags: [trade, missions, once-routes, tax, gas]
links:
  - reports/2026-11-16_mercury_voidborn-mastery-line-found-four-once-routes.md
  - reports/2026-11-16_unity_routes-close-on-their-bid-loss-stop-reads-last-runs.md
  - game/routes/guidebook/trade.md
---

# Trade -- The once line stopped at a spent reef and a dry crystal ask; two new once routes paid on their first runs, and the weekly tax showed up as run losses

## Situation

Period: from my report of 2026-11-16 09:56 UTC
(`reports/2026-11-16_mercury_voidborn-mastery-line-found-four-once-routes.md`)
to 13:00 UTC: my scheduled turn `turn-mercury` of 12:30 UTC. Orders in
force: `orders.log` ENT-014 (10:58 UTC), block MERCURY and EVERY
ADMIRAL (a) to (d).

```
Ships: 20/20, grounded: 0, lost: 0
Credits: start 1,032,546 (09:53 UTC), end 999,608 (12:58 UTC), net -32,938
Output: 12 trader runs, +20,995 cr, 22,931 of it paid once; 2 hand tests, +865 cr after their buys
Source: hive.py fleet (12:58 UTC), data/routes/runs.jsonl, the gate.py record of the hand tests
```

The net fell because the weekly Voidborn tax was taken at 12:27:32 UTC:
the 20 traders paid 83,940 cr, 4,038 to 4,818 each (get_tax_estimate
for each pilot, read 12:39 UTC). Without it the division gained about
51,000 cr in the period.

At 12:30 UTC 19 of 20 traders waited docked and the fill gate read HALT
on one open test (`hive.py standing`, `fill.py status trader`). At
12:58 UTC 2 were at work and 18 docked (`hive.py fleet`). Over all 20
ships in the four hours to 12:51 UTC Trade made -58 credits per
ship-hour, with 72,000 cr paid once apart (`hive.py standing`). Of
that, 4,818 cr is one pilot's tax booked into a run, so the figure
without it is about +3. The scale of that hour: the best repeating
route with two runs or more, hunt-test-homam-frost-moth, made 4,142
per ship-hour; a ship without work makes 0 (`hive.py tasks`).

The once line that Trade keeps for the fleet paid on. From 10:00 UTC
the fleet flew it 113 times (runs.jsonl). Signal Fragments: 26 runs,
182,000 cr paid once. The Node Beta chain: 24 runs, 191,931. Network
Expansion: 41 runs, 61,500. First Steps from the board: 14 runs,
13,000. The Collective Provides: 6 runs, 12,500. The Signal Protocol:
2 runs, 7,000. In all 467,931 cr paid once.

## Activities

**The once line (orders ENT-014, EVERY ADMIRAL (c); block MERCURY).**
- **The Collective Provides: set off.** It asks for 20 nickel ore
  mined. GSC-0049 Platinum-Group Reef read nickel 0 of 18,000 at 11:54
  UTC (data/scouting/gsc_0049.json), and a run started at 11:16 UTC
  ended "objectives not done" after 54.7 minutes, -338 cr.
  - **Why no other field:** the only other nickel we read is 659 units
    at Gliese 876 Belt, among about 7,000 iron and carbon, 7 jumps out.
  - **What waits behind it:** voidborn-signal-protocol and the rest of
    the line.
- **The Crimson Resonance: not flown.** One trader with an empty hold
  accepted it at 12:36 UTC, and the hold stayed empty. Orders ENT-014
  say: not handed out, not flown.
- **Neural Matrix Delivery: held for Unity's word.** The same test put
  8 phase matrix into the hold: base value 1,400 each, 5,000 cr reward,
  to Sirius, 9 jumps through three lawless systems. Orders F13 forbid
  taking goods of value out of policed space, so I asked Unity for the
  exception (requests.log ENT-146). The trader keeps the mission and
  the goods, docked.
- **Two new once routes**, each tested by hand at 12:41 to 12:43 UTC
  and written as a route the same minute (both serve only pilots that
  have The Collective Provides done):

  | Route | Hand test | First run by the route |
  |---|---|---|
  | voidborn-hardware-cargo (Hardware Optimization: Cargo, 1,500 cr) | +434 cr after a 1,066 cr expander | 12:45 UTC, +1,070 cr in 10.6 min (expander 355 cr at Synchrony Hub) |
  | voidborn-atmospheric-extraction (Atmospheric Extraction: Setup, 2,000 cr) | +431 cr after a 1,569 cr gas harvester | 12:45 UTC, +738 cr in 8.5 min (harvester 1,214 cr at Node Beta) |

  - **No free slot:** on both runs the game refused to fit the module
    because both utility slots were full, and the mission paid anyway.
    The last stop now stores the module, and `max_ships` went from 1
    to 3.
- **The Node Beta chain: six runs stopped halfway.** From 11:11 UTC six
  runs stopped after the first link, Conductive Lattice: the energy
  crystal ask at Central Nexus had left 420 cr (3,500 cr at 11:35 UTC;
  420 x 43 at 12:48 UTC).
  - **Pilots stranded:** 11, all miners, because the route skips any
    pilot that has the first link booked.
  - **Fix:** voidborn-resonance-finish finishes the chain for them (7,000
    + 8,000 cr once each, less about 6,360 cr of crystals). The chain's
    `max_ships` went from 10 to 4. Announced in queue.log ENT-103.
- **Boards:** I read 10 traders' boards whole (`boards.py`). Nine
  titles have been booked 0 times in the fleet; they are listed in
  queue.log ENT-102.

**Repeating work.**
- **mine-the-experiment-haze:** it now names its Node Beta hydrogen bid
  (`requires.bid`, 26 cr, 20 units). Its runs so far:

  | Run | Credits | Per ship-hour |
  |---|---|---|
  | 08:36 UTC | +3,008 | 2,330 |
  | 09:59 UTC | +4,129 | 3,197 |
  | 11:17 UTC | -5,346, of which 4,818 is tax | about -400 from the run alone: no bid at the sale, the gas stored |

- **Two tests,** one ship each:
  - **mine-the-experiment-haze-synchrony:** the same field, sold into
    another station's bid.
  - **mine-gsc-0016-emission-nebula:** added by fill.py.
  - **Result:** neither has a RESULT line yet.
- **voidborn-first-steps:** dropped from the plan (ENT-014 (c)).

**Capacity (F18).**
- **Routes that pay:** Trade's repeating route and its two tests hold
  3 places for its 20 ships.
- **Where the once line stands:**
  - 138 pilots of the fleet have not flown The Collective Provides (the
    tool fleet, view capacity), and nothing can fly it until the reef
    holds nickel again.
  - 11 pilots wait on the crystal ask.
  - 12 traders lack the navigation 3 that Signal Fragments needs.
- **Trade gaps:** none carries a hold. The route maker's best is
  hydrogen bought at Ironlight Crossroads and sold at Synchrony Hub, 34
  units deep.
- **Ships:** Trade needs no more.

**S6.**
- **Outpost Kit:** it asked 74,010 cr at Ironlight Crossroads at 12:39
  UTC, against 216,825 cr on 2026-11-15.
- **The other station inputs:** no station core, salvage metal, anchor
  plate, alloy scale or foil scale stands on offer in our eight books.

**Fill gate.** The last line, 12:50 UTC: "PASS: 16 ships of trader
wait, and nothing that pays and no test is open to them". What keeps
the waiting ships from work: the two fields above, Unity's word on
Neural Matrix Delivery, navigation 3, and hydrogen bids too thin for
more than the two gas tests (the tool fleet, view capacity: 40 units at
the best price at one station). No ship of mine is held by hand.

## Problems

- **Pilots flown to an empty reef.** The run of 11:16 UTC lost 338 cr,
  and pilots of other plans accepted the mission at 12:01 and 12:12
  UTC and flew out before I set the route off at 12:34 UTC (their logs
  in data/routes/logs/).
  - **Cause:** the route rested on one census, 192 nickel at 07:47
    UTC. Pilots of two other factions mine the reef too. A circuit's
    mine step has no field floor, while a hunt step has one
    (`min_creatures`).
  - **Done:** the route is off by hand, and I asked Unity for the floor
    (requests.log ENT-148).
- **Eleven pilots stranded halfway through the Node Beta chain.**
  - **Cause:** I set the chain's `max_ships` on the silver ask alone and
    never watched the crystal ask. The route skips a pilot by its first
    link, so a failed second buy leaves that pilot outside the route
    for good.
  - **Done:** voidborn-resonance-finish, and `max_ships` 4. The pilots
    are Zero's, and he adds the finishing route to his plan.
- **The weekly tax booked as run losses.** 38 runs of the fleet in
  flight at 12:27 UTC carry -149,123 cr. The loss stop then closed
  mine-achernar-frost-ring-nexus and mine-alnair-ice-fields-nexus on
  their "last 3 runs" (`fill.py status miner`, 12:38 UTC).
  - **Cause:** a run's credits are the wallet's difference from start
    to end.
  - **Done:** errors.log ENT-056 and requests.log ENT-147.
- **Modules left in the hold.** On both first runs of the new once
  routes the module could not be fitted and stayed in the hold. I
  stored both by hand, and the routes now store the module themselves.
  No ship was lost.

## Plans

What I do next, inside ENT-014:

1. **Neural Matrix Delivery, if Unity says yes to ENT-146.**
   - **The test:** the trader that holds the goods flies to Sirius with
     the F2 stance. I read its RESULT line and its fuel.
   - **The route:** written the same turn, with `requires.empty_hold` at
     the accept and the goods handed out.
   - **Then:** offered to every Admiral in queue.log.
   - **Its worth:** 5,000 cr once for each pilot the board offers it
     to. How many pilots that is: not measured beyond the 10 traders
     whose boards I read.
2. **The Collective Provides: back on when nickel returns.** I read the
   GSC-0049 census each turn and set the route on when the reef reads
   nickel. The Signal Protocol and the two new routes follow it.
   Without a field floor (ENT-148) I hold `max_ships` at 2.
3. **Read the first RESULT lines of the three gas tests and the
   finishing route.** Then lift the haze route whose bid regains, and
   take out what lost.
   - **Why no more gas ships:** the hydrogen bids are 36 to 136 units
     at 30 to 35 cr that come and go within the hour (the tool market),
     and how fast they come back is not measured.
4. **The chain's `max_ships`:** kept at what the crystal ask holds at
   420 cr; I read the ask each turn.
5. **Every board, every turn.** I read the whole board of every docked
   trader and give each title the fleet has not booked one test by
   hand.
   - **Next titles:** Network Commerce Protocol, once a carbon ore bid
     stands; Material Synthesis: Basic.
6. **The traders that wait** stay docked at no cost (F8) until one of
   these opens.

These choices were mine:
- **Collective Provides off:** set by hand, not left for the loss stop.
- **The chain:** a separate finishing route instead of changing the
  chain's skip rule, which the other plans rely on.
- **The gas tests:** one per bid, not a second ship on one bid.

## Suggestions

1. **Unity: answer requests.log ENT-146 (Neural Matrix Delivery under
   F13).**
   - **Reason:** 5,000 cr once a pilot, the goods handed out; about 25
     to 30 minutes of flight, my estimate from the Nova Terra round trip
     of 25 minutes, one jump short of Sirius.
   - **Cost:** one starter ship and its goods at risk in three lawless
     systems that our census reads every hour; fuel of about 350 cr.
2. **Unity: correct the tax in the runs (ENT-147).** Mining's ice routes
   stay closed up to six hours on rows that only carry the tax.
   - **Cost:** a pass over 38 rows, and a field for the next
     assessment.
3. **Unity: a floor for buy and mine steps.** ENT-148 asks a field
   floor for a circuit's mine step. The same need stands for a buy step
   on its ask: a chain should not start while its input is gone.
   - **Cost:** a dispatcher change and its test.
4. **Suggi:** the Outpost Kit's price fell to 74,010 cr. An outpost
   would cost about 174,000 cr with the 100,000 cr fee. Whether and
   when to found one stays Suggi's decision.
5. **No new traders.** 16 of 20 wait with nothing open to them.

## Learnings

From the learning capture of this turn:

- **A chain is sized on its scarcest bought input and needs a
  finisher.**
  - **Record:** six chain runs from 11:11 UTC stopped after Conductive
    Lattice; 11 pilots stranded (data/fleet/onetime.json, 12:49 UTC).
  - **What changes for Trade:** every chain route gets a finishing
    route, and its `max_ships` is read against each input's ask.
  - **For the fleet:** a route that pays once per pilot can strand
    pilots without any loss showing in the figures.
- **A mining mission is bounded by one shared field.**
  - **Record:** the GSC-0049 reef went from 192 nickel to 0 in four
    hours, with pilots of other factions there.
  - **What changes for Trade:** I read the field's census before
    lifting a mining-mission route.
  - **For the fleet:** a field floor on the mine step (asked).
- **An acquire-module mission counts a purchase made after the accept,
  even when the module cannot be fitted.**
  - **Record:** two hand tests and two route runs, 12:41 to 12:55 UTC.
- **The weekly tax lands in every run in flight.**
  - **Record:** 83,940 cr from the traders; 38 rows with -149,123 cr.
  - **For every Admiral:** read a route's runs of 12:27 UTC without the
    tax before taking it out.
- **Kept in:** the first three in `knowledge/voidborn-delivery-missions.md`,
  the fourth in `knowledge/voidborn-order-books.md` (both in my
  workspace).
- **Confirmed:** one accept with an empty hold settles in a minute
  whether a mission hands out its goods: twice this turn, one each way.
- **Open question:** how fast the reef's nickel grows back is not
  measured.

Skill: trade-books changed -- pitfalls: a chain on its scarcest input with a finisher, a mining mission on one field, accept-then-buy for module missions, the weekly tax in a run's credits

## Cross-links

- `reports/2026-11-16_mercury_voidborn-mastery-line-found-four-once-routes.md` -- my previous report, the start of the period
- `reports/2026-11-16_unity_routes-close-on-their-bid-loss-stop-reads-last-runs.md` -- the Fleet Admiral's report in force, with orders ENT-014
- `game/routes/guidebook/trade.md` -- the Standing Plan and the measured routes
- `game/routes/voidborn-resonance-finish.json`, `game/routes/voidborn-hardware-cargo.json`, `game/routes/voidborn-atmospheric-extraction.json` -- the routes written this turn
- `communications/errors.log` ENT-056; `communications/requests.log` ENT-146, ENT-147, ENT-148; `communications/queue.log` ENT-102, ENT-103

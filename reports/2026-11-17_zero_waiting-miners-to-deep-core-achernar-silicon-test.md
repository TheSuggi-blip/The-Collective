---
name: waiting-miners-to-deep-core-achernar-silicon-test
id: 20261117T151539Z
tier: report
trigger: session-end
author: Zero
tags: [mining, deep-core, iron, silicon, liminal, missions]
links:
  - reports/2026-11-17_zero_gold-given-liminal-ordered-class-card-deep-core-test.md
  - reports/2026-11-17_unity_pirate-gate-treasury-filled-kit-at-base-price.md
  - game/routes/guidebook/mining.md
  - communications/orders.log
---

# Mining -- Fifteen Waiting Miners Put Back to Work on Deep Core Prospecting, Two Widened Iron Belts and a Silicon Test

## Situation

Period: from my report of 11:44 UTC
(`reports/2026-11-17_zero_gold-given-liminal-ordered-class-card-deep-core-test.md`) to the end of
my scheduled turn of 15:00 to about 15:20 UTC on 2026-11-17. The orders in force are
`orders.log ENT-037` (14:00 UTC), whose block ZERO adds three tasks to the standing one: plan the
gather fields around the first outpost at GSC-0044 once it is founded, switch the pilot of the
ordered Liminal into it and measure its runs, and give Deep Core Prospecting to as many miners as
Markab's platinum carries. The Fleet Admiral's report in force is
`reports/2026-11-17_unity_pirate-gate-treasury-filled-kit-at-base-price.md`.

```
Ships: 60/60 at work at 15:12 UTC (fill gate PASS), grounded: 0, lost: 0
Credits: start 2,733,490 (my report of 11:44 UTC), end 2,556,080 (hive.py fleet, 15:10 UTC), net -177,410
Output: iron +3,300, copper +3,915, steel plate +764, carbon +132, gold +112, platinum +18 an hour stored (hive.py flow Zero, 4 hours to 15:06 UTC)
```

Of the credits' fall, 131,157 cr were six gifts from miners to the Fleet Admiral's flagship for the
faction treasury (data/fleet/gifts.jsonl after 11:55 UTC; her report: the treasury went from 6,903
to 206,903 cr). The rest is the fuel of standing work: Mining's steady money was -17,155 cr in the
hour to 15:01 UTC and -16,413 in the hour to 15:10 UTC (income 970, costs 17,383; hive.py fleet).
Paid once in the four hours to 15:01 UTC: 12,000 cr, of it 5,000 for the Deep Core test
(runs.jsonl) and 1,000 cr each to seven miners (the briefing's ships table).

At the start of the turn the fill gate said HALT: 15 miners waited (fill.py status miner, 15:02
UTC). Every home iron field stood at its floor of 20,000 (Schedar, Ironhollow Fading Signal, Prism
Scatter, Hamal, Spacetime Seep, Acubens; Pherkad at its copper floor), and the four belts beyond the
border were full: Garnet 29 of 29, Echo Ejecta 35 of 35, Achernar 10 of 10, Ruchbah 3 of 3. No
water-ice bid stood at Central Nexus or Node Alpha. Against the reserve (the tool stock,
view=reserve, 15:04 UTC): iron ore 316,319 held of 420,720, carbon ore 6,334 of 98,760, silicon ore
736 of 53,100. Levels of the 60 miners (lowest / median / highest, the tool fleet view=levels and
table ship_skills, 15:10 UTC): Mining 6 / 7 / 9, Deep Core Mining 6 / 8 / 9, Piloting 6 / 8 / 9,
about 36 hours to Piloting 10.

## Activities

**Deep Core Prospecting (orders ENT-037, block ZERO (3)).** The one-ship test of 11:20 UTC
accepted the mission at Nova Terra Central, mined 20 platinum at Markab Belt in one load and handed
in: +5,000 cr once and +4,370 cr over the run of 65.7 minutes (data/routes/runs.jsonl). Markab Belt
read 503 platinum at 07:51 UTC, before the test took 20, and two prospectors of other factions mine
it (table met, last seen 12:22 UTC). I set the route to 4 ships at a time and 16 pilots
(`max_pilots`), about 320 platinum, and put it into the miners' list First at 15:08 UTC (commits
09d6853, d675874). The next platinum is 82 Eridani Belt, 563 units 22 jumps out.

**Work for the 15 waiting miners.** gather-achernar-belt 10 -> 16 ships and lift_to 16 (89,493
iron at 13:58 UTC, 69,493 above its floor; 14 runs of 195 ore in 47.8 minutes, -180 cr);
gather-ruchbah-broken-glass-veil 3 -> 6 (99,997 iron; 6 runs, 195 ore in 48.3 minutes);
mine-dheneb-cryobelt 1 -> 2 (its four runs held: 960 cr per ship-hour over 12 hours, methane sold at
Hex Star, 36 cr x 916). Garnet stays at the 29 the Fleet Admiral lifted it to at 14:18 UTC (queue.log
ENT-165): BUSY combat drones fought at Garnet Belt at about 13:29 and 14:52 UTC (table met), while
72 of our runs there brought 260 ore each unhurt. At 15:12 UTC the fill gate said PASS for the
miners, and the fleet's money table read 246 of 246 ships at work.

**Silicon first (block ZERO).** Silicon lies only far out: GSC-0007 18,639 (27 jumps), Emberglow
4,935 (19), Floodlight Flats in Subra 3,187 (12 from home, 10 from The Experiment), Zubenelhakrabi
771 (its nearest station a pirate one) (table fields, 15:03 UTC). I wrote
gather-subra-floodlight-flats-silicon: one ship, empty hold, stores everything at The Crescent Moon
in Mebsuta two jumps away, sells nothing (rule F24), no pirate on our record on the road (commit
fb8e7fe). The fill tool's one test, mine-almach-stray-facets (trade crystal to Central Nexus, 24
jumps), went in as the turn's only other test.

**Carbon.** No field near us holds a load: Acubens Belt is under its floor of 60; the largest fields
read hold 1,664 (27 jumps), 1,357 (Gliese 876, a pirate place), 612 and 464. Asks: 3 cr at Alpha
Centauri Colonial Station, 4 cr at Arneb (hive.py store price). I passed the figure to Trade in
admirals.log ENT-039.

**The Liminal (block ZERO (2)).** I ended the miner's Garnet run early (the host stop file) and ran
commission.py --switch-only: the commission still read `sourcing` at 15:13 UTC, four hours after the
order, and list_ships held no Liminal. The script released the pilot; it gathers at Schedar now.

**Stance and claims.** set_stance.py runs for the 30 miners not yet on flee (25 minutes); the state
file held 30 of 60 before. Claim admirals.log ENT-038 (releases ENT-028), note ENT-039.

## Problems

**The iron goal was missed.** My last report set "more than 370,000 iron held" for this turn. The
fleet holds 316,319 (the tool stock, 15:04 UTC), 28,573 less than the 344,892 of 11:05 UTC. Cause:
the goal measured the fleet's stock, which the whole fleet draws on. Steel crafts turned iron into
steel plate (95 runs of craft-steel-node-beta in four hours, route_earnings; steel plate held
16,893), while Mining's own iron flow fell from +9,913 to +3,300 an hour because the home fields
and Schedar shut at their floors. Fix: the next goal is set on Mining's own stored flow
(knowledge/iron-gathering.md).

**15 miners waited at 15:02 UTC.** Cause: every field of the reserve templates was at its floor or
its limit, and lifts beyond the border wait for an Admiral's turn or the Fleet Admiral's hand. The
three lifts and the Deep Core route closed it by 15:12 UTC. The Fleet Admiral names the same gap
for every role (queue.log ENT-166).

**The Liminal is not delivered.** 58,881 cr were paid at 11:11 UTC and the yard still sources the
parts; the quote's 168 ticks did not start. Cause: a credits-only commission waits until the yard
holds the hull's parts, which I did not know. Nothing more is spent on hulls until it stands.

**Mining's steady money is negative**: -16,413 cr in the hour to 15:10 UTC. Standing work costs
about 180 to 324 cr a run and no ice bid stands. No ship lost, no hostile fire on record.

## Plans

Inside orders ENT-037, my own choices:

1. **Deep Core Prospecting.** Read the hand-ins in dispatch.log and the runs; if a pilot's run
   finds fewer than 20 platinum, cut max_pilots to the stock left and read 82 Eridani Belt (563)
   for a second route. Goal for the turn of 19:00 UTC: 8 more hand-ins, 40,000 cr once.
2. **Iron.** Goal: Mining's iron stored +4,000 an hour over the four hours to 19:00 UTC (+3,300
   now). Achernar at 16 and Ruchbah at 6 are read for floor and foreign combat before any further
   lift; Schedar and Fading Signal reopen as they grow back.
3. **Silicon test.** Read the first RESULT line of gather-subra-floodlight-flats-silicon: silicon
   per run and minutes. If it brings a load, lift it within what the field holds above its floor
   (3,187 now), and ask Logistics how the silicon comes home or is crafted there.
4. **The Liminal.** Read commission_status at the turn; switch the pilot only when it no longer
   reads `sourcing`; then measure its gather runs against the Threshold's 195 to 292 ore in about
   47 minutes.
5. **The outpost at GSC-0044.** When its base id is read, one gather route each, richest first:
   Botein Belt (iron 100,000, richness 68), Acrux Belt (99,782, 64), GSC-0044 Belt, Intercrus,
   Forgotten Tailings, storing at the outpost.
6. **Ice.** The drains and mine routes stay in the lists, closed by their bid gates; a water-ice
   order of 300 units at Central Nexus opens them by itself.
7. **Stance.** Read the state file at the next turn and run set_stance.py again for those not set.

## Suggestions

1. **Carbon is bought, not gathered** (for Trade and the Fleet Admiral). The reserve lacks 92,426
   carbon ore; no field within 7 jumps holds more than 1,357 and that one is a pirate place. Two
   stations ask 3 and 4 cr: about 300,000 to 370,000 cr buys all of it, against fields that
   cannot give it at any fuel. Trade's to decide (its block), the purse the Fleet Admiral's.
2. **A lift pass between turns** (for the Fleet Admiral, already on her list in queue.log ENT-166).
   Today 15 miners waited up to the turn. Cost: one change of fill.py's five-minute pass; it would
   have filled Achernar and Ruchbah inside their lift_to without a hand.
3. **A commission's state in the ship file** (for the Fleet Admiral): the fleet service could read
   `commission_status` once an hour for a pilot with an open commission, so no turn has to take a
   ship by hand to learn that a hull is still sourcing. Cost: one read an hour per open commission.
4. **Measure a division by its own flow** (for the orders' Measure line): "iron held against the
   reserve" moves with every division's crafts; "units stored per hour" (hive.py flow) is Mining's
   own. The Measure already names both; I set my goals on the flow from now on.

## Feedback

- **fill.py with tests=1** (the tool fix of requests ENT-212): `fill.py fill miner --tests 2`
  without write listed exactly two tests; with `--tests 1 --write` it added exactly one test
  (mine-almach-stray-facets) and the lift of mine-dheneb-cryobelt. The 0 and the small numbers
  now hold; the fault of my last turn did not repeat.
- **No reserve-short sale from the filler** (ENT-213): `fill.py status miner` printed 20 routes
  under "sells an item the reserve is short of (rule F24)", among them mine-worklight-outcrop and
  mine-stormward-silicon; none was offered to my ships.
- **The pirate gate** (commit 1586add): my plan held no route in a closed system; the silicon road
  was checked against observations of kind pirate by hand (newest within 3.7 hours at Felis). A
  view that lists the pirate systems within N jumps of a route's road would save that query.
- **ledger.py's faster reading** (commit 1818480): the craft-steel routes now print the per-pilot
  stores ("stores 369 iron_ore ... 550 wanted"), and no miner waited on "storage not read".
- **The briefing** printed the plan's `carries` column and the `+N` of a field this turn; it made
  the lifts quick. The fill status line for a full route ("carries about 0 ships hour after hour,
  630 more this turn") reads Garnet's regrowth as 1 an hour, which looks like a read gap rather
  than the field; I did not rely on it.
- **commission.py** (mine): it reported the `sourcing` state and released the pilot as built.
- What I could not do: read a commission without taking a ship by hand (suggestion 3).

## Learnings

- **A turn's iron goal is set on Mining's own stored flow, not on the fleet's iron held.**
  Record: iron held 344,892 at 11:05 UTC and 316,319 at 15:04 UTC (the tool stock), while Mining
  stored +3,300 iron an hour and the fleet's steel plate rose to 16,893. What changes: my goals
  name hive.py flow Zero. Kept in `knowledge/iron-gathering.md`. For the fleet: a stock that every
  division draws on measures the fleet, not the division that fills it.
- **A credits-only commission waits in `sourcing` before the quote's ticks start.** Record:
  commission.py --switch-only, 15:13 UTC, four hours after the order. What changes: no second hull
  before the first stands; the status is read each turn. Kept unpromoted (`LEARNINGS.md`) and in
  the skill mining-chains. For Logistics and the Fleet Admiral: a hull or a facility quoted in
  ticks may wait on parts first.
- **A mining mission pays when a field holds a load of its ore.** Record: Deep Core Prospecting,
  20 platinum in one load at Markab Belt, +5,000 cr once (runs.jsonl, 11:20 UTC). What changes: the
  route is sized on the stock at 20 a pilot (16 pilots). Kept unpromoted until the 16 runs are read.
- Confirmed, not new: the fields one jump from The Experiment give 193 to 292 ore in 45 to 50
  minutes (Achernar, Ruchbah, Echo Ejecta, Fading Signal), Garnet 260 in 46 minutes at two jumps.
- One thing of my class I do better: sizing a once-mission on the ore it needs. One I do not
  master yet: how fast platinum and silicon grow back; no two reads of either are on record.

Skill: mining-chains changed -- a credits-only commission reads sourcing first; ending a run early for a switch

## Cross-links

- `reports/2026-11-17_zero_gold-given-liminal-ordered-class-card-deep-core-test.md` -- my previous report
- `reports/2026-11-17_unity_pirate-gate-treasury-filled-kit-at-base-price.md` -- the Fleet Admiral's report in force
- `communications/orders.log` ENT-037 -- the orders in force
- `communications/admirals.log` ENT-038, ENT-039 -- Mining's claim and note of this turn
- `game/routes/guidebook/mining.md` -- Class Card and Standing Plan of this turn
- `game/routes/mission-deep-core-prospecting-nova-terra.json`, `game/routes/gather-subra-floodlight-flats-silicon.json` -- the routes changed and written

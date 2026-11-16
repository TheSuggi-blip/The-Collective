---
name: faction-steel-plate-made-every-hauler-own-routes
id: 20261116T191900Z
tier: report
trigger: session-end
author: Apollo
tags: [logistics, crafting, faction, plans, station-list]
links:
  - reports/2026-11-16_apollo_stored-gas-into-liquid-hydrogen-haulers-trained-for-signal.md
  - reports/2026-11-16_unity_plan-files-live-requests-closed-standing-orders-reworked.md
  - game/routes/guidebook/logistics.md
---

# Logistics -- The Faction's 275 Steel Plate Are Made and Every Hauler Flies Routes of Its Own

## Situation

Period: from my report of 2026-11-16 14:45 UTC
(`reports/2026-11-16_apollo_stored-gas-into-liquid-hydrogen-haulers-trained-for-signal.md`)
to 19:19 UTC. Suggi paused the turn jobs at 13:50 UTC; this turn is the first one on the
division plan files, started on his word. Orders in force: `orders.log` ENT-017 (18:18
UTC), block APOLLO: keep the stations' list, test the build by hand (steel plate from iron
ore first), make 275 steel plate and 75 circuit boards for the faction (P5) and say where
they lie, every other hauler gathers; turn T1: every hauler gets routes of its own, the plan
check and the fill gate pass.

```
Ships: 20/20 at work, grounded: 0, lost: 0
Credits: start 1,112,747 (14:42 UTC), end 1,128,733 (19:16 UTC), net +15,986
Output: 275 steel plate, 81 liquid hydrogen, 0 circuit boards
```

Source: my previous report (start), the tool fleet with view=money at 19:16 UTC (end),
the turn's craft logs and the game's storage view of 19:08 UTC (output).

Steady money of Logistics (rule F19), the tool fleet with view=money at 19:16 UTC: net
-2,440 cr an hour over the last hour (income 1,587, costs 4,027). Hour by hour (view=history):
-1,503 (16:02), -3,610 (17:03), +2,596 (18:04), -2,081 (19:00). One-time money apart: the
112 hauler runs that started from 14:42 UTC carried 0 cr paid once and -4,251 cr in all over
4,543 ship-minutes (`data/routes/runs.jsonl`). The wallet change and that run sum are not
broken down further; runs that started before 14:42 UTC and ended later are in the first and
not in the second.

The forecast of the division (the tool hive, verb=forecast): SUM -3,165 cr an hour (-158 a
ship) at 18:27 UTC before I planned, -3,064 at 18:41 UTC after, -1,408 (-70 a ship) at 19:16
UTC with two gas tests flying, one of them priced by the route maker's estimate only.

The Measure line of my block: inputs of the stations' list with a known source, 20 of 30 (18
with a field or an offer in our readings, 2 from Military's hunts); recipe steps tested this
turn, 1 at scale (steel plate) and 1 new step named for next turn; haulers at work, 20 of 20;
steel plate held for the faction 275 of 275, circuit boards 1 of 75.

## Activities

**The stations' list (P4).** Written into my guidebook, section 13, from the tool base_plan
(18:26 UTC) against the storage book of 18:37 UTC: per input the units one station takes,
what we hold, at which stations it lies, what is missing and its known source. Twenty-eight
of thirty inputs are short; ten have no source in our readings. Two readings change the list:
silicon ore stands asked at 420 cr for 424 units at Central Nexus (book of 19:07 UTC), and
copper piping (26,120 a station) has a second hand recipe, `draw_copper_piping`, 12 copper ore
and 2 steel plate for 4, which takes the copper we hold (75,869) instead of 34,832 verdigris
curd we do not.

**The build: steel plate (orders, first step).** 275 plate made by `basic_iron_smelting` at the
Node Beta workshop from iron ore the gather routes had stored there: 145, 117 and 13 plates by
three haulers in 5.7, 5.2 and 0.7 minutes of crafting, 0 cr, no skill asked. The first
crafter's crafting and refining skills rose from level 0 to 1 (about 110 XP each on 145 runs).
About 25 plates a minute a hauler: the 49,140 plate one station takes would be about 33 hours
of one docked hauler. Guidebook section 14.

**The faction's goods (P5).** The 275 steel plate lie in one Logistics storage at Node Beta
(the game's storage view, 19:08 UTC), for the builder the Fleet Admiral names. No board was
made: every hand recipe takes silicon ore, and the fleet holds 34. Requests.log ENT-168 asks
Mining for its 16 silicon and carbon at Central Nexus, which would give 48 boards by etching.

**Stored gas made and carried.** 216 stored hydrogen gas became 81 liquid hydrogen at Node Beta
in 6.8 minutes, 0 cr; the new route `carry-liquid-hydrogen-node-beta-central` carries it to the
Central Nexus bid (133 cr x 38 at 19:07 UTC), one ship, open once the storage book shows it.

**The plan (T1).** Every hauler has routes of its own since 18:37 UTC: the 11 bid-gated
stored-goods routes at the head (one ship each), then the four gas haulers' tests
(`mine-coldwater-emission-nebula`, `mine-antares-gas-cloud`, `mine-amberfall-emission-nebula`,
`mine-deepwell-haze`, one ship each) and the ice hauler's (`mine-gliese-876-belt`,
`mine-achernar-frost-ring-nexus`), then standing work on the three iron and copper fields of
Node Beta: `gather-gsc-0027-prism-scatter` first for 5 ships, `gather-hamal-crystal-bloom`
first for 8, `gather-gsc-0027-spacetime-seep` first for 2, each hauler listing the other two
behind. Then: `census-frontier`, `park`. `plan.py check`: PASS. Fill gate at 18:46 and 19:17
UTC: `PASS: no ship of hauler waits`.

**Requests and notices.** Closed my ENT-149 (Mercury fixed both module routes, commit 1c2800c)
with ENT-167; asked Zero (ENT-168) and Mercury (ENT-169, focused crystal: 4 energy crystal and 1
palladium for a bid of 800 cr x 10); queue.log ENT-114; errors.log ENT-059.

## Problems

**A false cause stood for ten hours (errors.log ENT-059).** I had written that the workshop
"queues fewer runs than asked"; in fact a craft's `quantity` counts made units, rounded up to
runs (27 liquid hydrogen asked queued 9 runs, 19:02 UTC). No credits were lost; the guidebook,
a knowledge file, my skill and two shared facts carried it, and the runner's new craft step
sends runs as quantity. All corrected; Mercury had read the rule from the game's help at 18:35.

**The first catch released its pilot.** My new catch script assumed a gather run ends docked
at Node Beta; it ends at the field (18:42 UTC), so one hauler went back to standing work
unused. Then the goal was refused while the engine's loop still ran (409, 18:55 UTC). Both
fixed in the script (`--goto`, a retried goal) and the drivers restarted; the crafting began
at 18:59 UTC instead of about 18:41.

**Plan sets that did not apply.** Six of eight `plan.py set` calls at 18:36 UTC printed
COMMIT BLOCKED while another member's route files stood untracked in the clone, and changed
nothing; `show --brief` showed it, and the sets were run again after that commit.

**Still open.** No circuit board made (silicon). The new liquid hydrogen waits until the ledger
reads its storage (about 40 minutes). The two Nova Terra gas tests left 232 and 231 units of gas
in storage at that Solarian station. Standing work cost -4,251 cr over the period's runs. No
ship lost, no hold left by hand (orders folder, 19:17 UTC).

## Plans

Inside orders ENT-017, until the next turn, the plan file keeps every hauler at work without
a hand: stored goods into each bid as it stands, the gas and ice tests one ship each, iron and
copper gathered at Node Beta by the rest (about -137 to -188 cr per ship-hour of fuel,
forecast 19:16 UTC). My choices, in order, next turn:

1. **Boards for the faction.** With Mining's silicon and carbon in the crafting storage at
   Central Nexus (ENT-168): 16 etchings, 48 boards, 49 of 75 with the one stored. For the other
   26: about 18 silicon at the 420 cr ask, one unit first (rule F12), about 7,560 cr in all, if
   the Fleet Admiral does not rule otherwise (Suggestions).
2. **The next station step:** `draw_copper_piping` at the Node Beta workshop, one hauler and one
   batch, quoted first; its cost in credits, minutes and skill into section 14. If it holds,
   the stations' list loses its verdigris curd line.
3. **Read the first RESULT lines** of the liquid hydrogen carry and of the gas tests; a test
   that loses twice leaves the plan, and one that sells abroad is judged with what it leaves
   there.
4. **Focused crystal:** Mercury's answer to ENT-169 decides who flies it; if Trade says no, one
   hauler gathers 40 energy crystal and 10 palladium into one storage and makes the ten for the
   800 cr bid, read again before the craft.
5. **The 275 plates** go by deposit to the builder the Fleet Admiral names, on her word; until
   then they stay where they are.
6. **Levels (P3):** Piloting 5, 5 and 6 (lowest, median, highest), 107 XP an hour, about 102
   hours to Piloting 10 and the tier-2 hulls (view=levels, 18:46 UTC). No hull or module is
   bought this turn: the next step that pays is a tool where a bid takes its work, and none
   stands open to haulers.

## Suggestions

1. **The runner's craft step asks `quantity: runs * per_run` (Fleet Admiral, one line in
   `route_run.py` workshop()).** Today a recipe that makes 2 a run is queued in four jobs where
   one would do (queue.log ENT-114); the total is right, the time is not. Cost: one install with
   its test.
2. **A craft stop on the gather routes, once Trade's first flight of the step is read.** A gather
   run that ends by smelting its own iron at Node Beta turns standing work into steel plate with
   no hand, no catch and no extra hop. Cost: one stop in each of three route files (mine to
   write) and one test ship.
3. **Buying silicon for the faction's boards (Fleet Admiral's word).** P5 says we make the plates
   and boards ourselves; the fleet's own silicon makes 49 of 75. About 18 silicon at 420 cr
   (7,560 cr) makes the rest at about 280 cr a board against 686 cr asked for a board. I do it
   inside rule F12 unless told not to.
4. **The stations' list counts copper piping from copper ore** once the step is tested: it moves
   34,832 curd we cannot source to copper we already hold.

## Learnings

From this turn's learning capture.

- **A craft's `quantity` counts made units, rounded up to whole runs.** Record: "Queued 27 Liquid
  Hydrogen (9 run(s))" at 19:02 UTC; Mercury's reading of the game's help at 18:35 UTC. My
  division now asks runs times units a run and prints the answer beside it. For the fleet: any
  script or route that crafts reads `quantity` so. A repeated mistake of a known class, a claim
  wider than its check (errors.log ENT-059). Kept in: `knowledge/harvester-by-hand.md`.
- **Steel plate is made where the iron lies, by haulers taken at the end of their gather runs.**
  Record: 275 plates in about six minutes, 0 cr, at Node Beta; crafting skill 0 to 1. For the
  fleet: the station's 49,140 plates are a matter of workshop hours, not credits. Kept in:
  `knowledge/stored-ore-worth.md`.
- **In a plan file a route in Then is reached only when every own route is closed.** Record: the
  plan of 18:37 UTC. Bid-gated sell routes stand at the head of each ship's own routes. For the
  other Admirals: put such routes before standing work; saved to the shared bank. Kept in: my
  skill logistics-stock.
- **A gather run ends at the field, and the engine's loop outlives the run's order by seconds.**
  Record: the catch logs of 18:42 and 18:55 UTC. Kept in: my skill logistics-stock.
- **A sell test into a small bid leaves the rest where it sold.** Record: 463 units of gas at Nova
  Terra Central after two runs. Kept in: unpromoted (`LEARNINGS.md`).

Skill: logistics-stock changed -- catch.py (take a pilot at its run's end and fly it in), craftchain asks made units, five pitfalls of this turn

Open question: what the gather fields grow back per hour, which sets how many haulers standing
work carries beyond this turn (the column `carries` reads `0 +312` to `2 +116`).

## Cross-links

- `reports/2026-11-16_apollo_stored-gas-into-liquid-hydrogen-haulers-trained-for-signal.md` -- my previous report, the start of this period.
- `reports/2026-11-16_unity_plan-files-live-requests-closed-standing-orders-reworked.md` -- the Fleet Admiral's report in force.
- `communications/orders.log` -- ENT-017, the orders in force.
- `game/routes/guidebook/logistics.md` -- the Standing Plan, sections 13 (the stations' list) and 14 (the faction's plates and boards).
- `game/routes/carry-liquid-hydrogen-node-beta-central.json` -- the new carry route.

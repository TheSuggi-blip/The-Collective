---
name: ember-glands-to-far-bids-crafts-replace-iron
id: 20261118T003034Z
tier: report
trigger: session-end
author: Apophis
tags: [military, hunting, group-hunt, reserve, missions, sentinels]
links:
  - reports/2026-11-17_apophis_first-group-hunt-no-kill-escort-flies-reserve-kept.md
  - reports/2026-11-17_unity_iron-met-make-before-gather-acrab-chosen.md
---

# Military -- Ember Glands Go to the Deep Far Bids, Ships Make From Their Stores Instead of Gathering Iron, the Group Learns to Close In

## Situation

Period: from my report `reports/2026-11-17_apophis_first-group-hunt-no-kill-escort-flies-reserve-kept.md` (turn of
20:00 to 21:15 UTC on 2026-11-17) to the end of my scheduled turn of 2026-11-18 00:00 to about 01:00 UTC. Orders in
force: `communications/orders.log` ENT-054 (23:49 UTC). My block APOPHIS last changed at 21:59 UTC (ENT-047): hunt as
far as each herd regains, no guard in the first ring, the sentinels trained until Piloting 20, the second group
flight with each member's target and advance, the Voidborn Mastery link that stands still for drones named; and P2:
the reserve's iron is met, no ship gathers iron or copper any more. Entries ENT-048 to ENT-054 changed the layout of
the empire and the faction's ladder, not my block. The plan for my division is in
`reports/2026-11-17_unity_iron-met-make-before-gather-acrab-chosen.md`, section Plans: a second group flight, one
hunter a herd, no guard in the first ring, and the Voidborn link named.

```
Ships: 70/70 at work (50 drones, 20 sentinels), grounded: 0, lost: 0
Credits: start 3,207,385 (my last report); end 3,248,220 in the division's wallets (00:28 UTC), with the sweep's gifts above 50,000 a ship gone to the treasury
Steady: runs of 2026-11-17 20:20 to 2026-11-18 00:05 UTC: 492 runs, 225.5 ship-hours, -13,095 cr steady, 66,922 cr paid once
Output: 182,519 units of 16 reserve items held; of the short ones per hour over 4 hours: carapace +246.6, biogas +44.0, gold ore +36.1
Source: fill.py check (00:35 UTC), hive.py fleet (00:28 UTC), the table runs (00:17 UTC), hive.py flow (00:23 UTC)
```

My goal of the last turn, Military's steady money above +15,000 cr an hour over the four hours to this turn, is
missed. The runs read -13,095 cr in 3.75 hours and `hive.py fleet` read -4,530 cr (00:06 UTC) and -9,119 cr (00:28
UTC) for the last hour. The hunts made money (+23,191 cr steady from 220 hunt runs, the table runs by kind); the
iron gathering of the ships no herd took cost -22,528 cr in 93.0 ship-hours, 46.5 of them after the orders had
ended it (errors.log ENT-108); one paying run reads -8,917 cr by a figure fault (requests.log ENT-264). The forecast
reads -13,648 cr an hour for the routes flown now (`hive.py forecast Apophis`, 00:17 UTC), on all-run figures that
still hold the iron and the reserve hunts.

Combat skills (table ship_skills, 00:15 UTC): drones gunnery 3 / 5 / 7, weapons 2 / 3 / 5, tactics 2 / 4 / 6,
xenobiology 2 / 4 / 7 (low / median / high); gunnery's median and every lowest rose one level since 20:17 UTC.
Sentinels gunnery 3, weapons 2, tactics 3, xenobiology 3, each up one; their Piloting 7 / 7.5 / 9 toward 20.
Shields and Armor 0 for all. Voidborn Mastery 0 for every drone (47 hold XP), one sentinel at 1.

## Activities

**The group flights (orders D14).** Two flights by hand on pilot whales (220 hull) at Stellar Siphon, my script `group_hunt.py`, background. Flight 2 (00:08 to 00:34 UTC, four drones: a fleet of three and one outside that joined at tick 3): every member set its target, but all five ships stood at zone outer, dist 6, for 48 ticks; the whale hit the leader (shield 111 to 81 percent) and nobody dealt a point. The script had compared each ship's dist with the prey's, and both read 6: `dist` is a place on one line from the fight's centre, and a Pulse Laser I reaches 3. I changed the script to advance every ship until its own dist is 2 or less and to set the target again where its own row shows none. Flight 3 (00:40 to 00:54 UTC, three drones): all closed to dist 2 by tick 3 and all three dealt damage (7 to 9 each by tick 10). The whale went from 100 to 73 percent in 20 ticks while it struck the leader alone: shield 111 to 0 by tick 18, then hull 100, 68, 38, 24, 9 percent in four ticks. The side fled at tick 20 and escaped at 9 percent hull. No kill, no loot, no ship lost; the three were docked for repair by the script.

**Ember glands to the deep far bids.** `loot_bids.py` and the tool `market` showed ember glands bid 7,400 x 24 at
Crimson War Citadel (Krynn, 00:07 UTC), 5,686 x 57 at First Step Memorial (22:41 UTC) and 5,686 x 9 at The Levy
Customs, against 480 at every home station; my two gland sales still waited for Hex Star, which has shown no bid
since 14:55 UTC. The GSC-0035 test hunt had sold 3 glands at Krynn for 22,203 cr (20:32 UTC). The division stored
about 58 glands, 26 of them at Hex Star and 21 at Node Beta (`data/stock/storage.json`, 00:09 UTC). Four sale routes
were written and committed (commit 6484d4d4): Central Nexus and Node Beta to Krynn, Hex Star to Krynn and to First
Step, one ship each, a bid gate of 5,000 x 3, each road read clean of pirate lines in 24 hours. They head `@hunter`.
Not yet flown: their first RESULT lines are read next turn. At 7,400 the 58 glands are worth some 429,000 cr against
about 28,000 at home; what the bids take before others fill them is not measured.

**Make before gather (P2).** The list Then and the tail of `@hunter` sent every ship no herd took to iron and copper
fields until 00:15 UTC. Eight craft routes now make armor plate from the pilot's own stored carapace (6 to 1; armor
plate is short 4,833) and steel plate from its own stored iron (10 to 1; 30,745 plates still to make) at The
Experiment, Node Beta, Synchrony Hub and Central Nexus (commit 6484d4d4); they replace every gather route in the
template (dd1ff796) and in Then (5ab92f3e). First runs: 18 craft runs from 00:16 to 00:30 UTC at 0 to -52 cr each,
one drone made 80 steel plates at The Experiment in one visit (its log, 00:30 to 00:34 UTC); one ship flew a once
hand-in on the way (+1,000 cr).

**Voidborn Mastery (rule F35).** The link that stood still for drones is The Collective Provides: it was in no
Military list, so only 9 of my 70 ships had flown it, against 65 that hold Network Expansion
(`data/fleet/onetime.json`); every later link that pays Voidborn Mastery asks for it. Trade's route for it paid 63
times in 73 runs since 12:00 UTC. It stands in my list First since 00:15 UTC (51faf975), with Mining's Crystal
Resonance and Material Synthesis after Signal Protocol (one paid test each).

**Hunts.** Drone hunts +21,851 cr in 3,874.6 hunter-minutes (338 cr per hunter-hour), sentinel hunts +4,529 in
2,262.4 (120), 20:20 UTC to 00:05 UTC (`hunt_figures.py`). The far tests that sell melt at First Step paid: Yildun
+8,631 cr in 2 runs, GSC-0042 +7,135 in 3, GSC-0037 +1,261 in 3; route_earnings over 12 hours: Yildun 4,695,
Willowgate 4,677, GSC-0042 3,662, Avior halo-drifters 3,454 cr per ship-hour. The carapace, veil-ray and drift-ray
hunts that store for the reserve read -114 to -486 cr per hunter-hour at 2.2 to 16.5 kills an hour. No stranger
fired on a hunter. `pirate_places.py`: PASS for 12 hours at the hunts' places; 22 hunts lie one lane from a pirate
line of the last 24 hours, each with its own `alone` "pirates".

**The escort's RESULT lines.** Two runs on 2026-11-17 (20:33 and 20:57 UTC): 23.1 and 24.3 minutes beside a ship on
the Node Beta chain, -169 and -156 cr, hull 100 percent, no shot, both ended when the guarded run ended. None since
orders ENT-045.

**The sentinels (D12).** All 20 fly their own far hunts first, then `@hunter`; +2,952 cr steady in 41.0 hunt-hours.

## Problems

- **The goal was missed** (Situation): the iron fallback and one false figure outweighed the hunts.
- **Iron gathered after the orders ended it** (errors.log ENT-108): 63 mine runs, 46.5 ship-hours, -13,195 cr from
  21:59 UTC to 00:15 UTC. Cause: the fallback served a target only my turn reads. Fixed: the fallback is bound to the
  pilot's own stores and gathers nothing.
- **A paying run that reads a loss** (requests.log ENT-264): the Sandrift hunt of 21:46 UTC sold 7 melt for 10,717
  cr and reads -8,917; the wallet sweep's gift of 13,220 cr, 138 s before the run's end, is counted in neither run by
  the seam rule of `routes.moved`. Asked of the Fleet Admiral; the route stays in the plan.
- **The second group flight dealt nothing** (flight 2: the advance rule read the prey's dist, which moves with the ships; fixed. Flight 3 dealt damage but the leader fell to 9 percent hull: three starters deal about 3 a tick against 220 hull, while the whale takes a starter's shield and hull in some 20 ticks. The script now flees all at hull under 85 or shield 0).
- **Glands stored where no buyer stood**: 26 at Hex Star after its bid left, because the sale routes named one
  station. The sales now follow the deepest bid; the skill step reads it each turn.
- **Reserve FLAGs on two routes of the Fleet Admiral's filler in my rows** (`reserve_hunts.py`): Alathfar's
  chlorophage hunt (caustic sac, short 373, best bid 3,716) and the HD 10647 frost-moths (superfluid vials held back).
  The hunt runner stores every kept good whatever `min_bid` says (commit d93c033), so nothing is sold; I named them,
  I did not edit them. Alathfar lies one lane from Hollowcrest, where ten Dross raiders stood at 19:06 UTC.
- **Ships that reached `park`**: 4 runs, 0.4 ship-hours, -510 cr, while the iron fields of Then were full.
- No ship lost, none grounded; no shot at a ship of ours.

## Plans

Inside orders ENT-054, decided by me:

- Read the four gland sales' RESULT lines; if Krynn's bid of 24 is filled, the Hex Star and Node Beta stores go to
  First Step (Node Beta's road to First Step passes Hollowcrest and stays unwritten while the Dross pack is on record).
- Read the crafts: how many visits the stores carry, the armor plate made (the ledger reads storage about every 40
  minutes), and when ships begin to dock for want of stores; then add hunts, not gather routes.
- The group: no more starter groups on pilot whales: three Pulse Laser I need some 70 ticks for 220 hull and the leader lasts about 20. The next group test takes prey of 100 hull or less (kiln-snails at Eltanin, cauldronbacks), or waits for a second weapon or a tier-2 hull; I give the Fleet Admiral the four steps the dispatcher's `group: N` needs.
- Count, for every once chain my ships fly, how many hold the link before each link, and put a link other divisions
  write into my First list once it paid (skill military-turn).
- Keep one hunter a herd; the far melt hunts selling at First Step stay; add a cinder-sylph herd on a clean road
  when its glands have a bid of 5,000 or more within 20 jumps.
- The sentinels: their far hunts, Piloting toward 20 (7.5 median now).
- Goal for the next turn (plan file, Planned): Military's steady money above 0 cr an hour over the four hours to my
  next turn, read with `hive.py fleet`, and the gland sales' first RESULT lines.

## Suggestions

- **The dispatcher's `group: N` (Fleet Admiral, queue.log ENT-175):** each member closes in by its OWN `dist` in
  the battle table, to 2 or less, with a target set again when its own row shows none; the prey's `dist` is no guide.
  Cost: one rule in the group step.  The prey takes one target (the leader): the step should rotate the ship in front, or flee by shield, not hull (flight 3: shield 0 at tick 18, hull from 100 to 9 percent in four ticks).
- **A sale that follows the buyer (Fleet Admiral or Trade):** the route maker could offer, for every good we store
  with a bid several times the home bid on record, a sale from where it lies to that bid, as it offers hunts. Today a
  turn finds it by hand; 26 glands lay at a station whose bid had left 9 hours before. Cost: a candidate kind.
- **The Collective Provides in every plan's list First (every Admiral):** my ships lacked it while the line paid;
  other divisions may lack it too (`data/fleet/onetime.json` names who holds each link). Cost: none.
- **The seam of `routes.moved` (requests.log ENT-264):** a fix makes every sale run that crosses the 50,000 keep read
  right. Cost: one test and one rule; whose: the Fleet Admiral's.

## Feedback

- `hive briefing` (tool `hive`, verb briefing): the orders, my requests, the money, the standing fleet and the gate
  in one call worked, but the tool cut the answer at 30,000 of 95,355 characters, so I read it from the shell into a
  file. A briefing that pages, or one part per call, would make the tool enough by itself.
- `plan` (actions first, then) and `plan.py template`: each call checked, applied and committed at once (51faf975,
  5ab92f3e, dd1ff796). Clear and fast. The notes printed with every call (`2 ships have ... as their first own route
  and it takes 1`) repeat the filler's work in my rows; they did not stop anything.
- `fill` (check, status): PASS both times. Its status lists 8 tests whose route files do not all exist yet
  (`hunt-seginus-haze-cinder-sylph` has none), so a test cannot be added by hand by its id; the tests rest on the
  route maker's estimates for glands of 13,111 to 21,310 cr per ship-hour.
- `sql` (route_earnings, runs, ship_skills, herds, systems): answered every figure of this report; the column names
  (`credits`, `jumps`, `creature`) had to be looked up first with `table=`.
- `stock` (view reserve, members, item ember_gland): the reserve view showed what is short and what to make; the
  members view lists the sentinels under Unity, which made 47 of my glands look like the Fleet Admiral's until I
  read the per-pilot split.
- `market` (ember_gland, crystal_melt): the moves found the deep far bids at once.
- `routes.earned` and the sweep: one paying run reads -8,917 cr (ENT-264).
- The fill filler (Unity's five-minute job): it put two hunts I had taken out (Alathfar, HD 10647) back into my rows;
  the reserve runner rule keeps them harmless. What I built: four sale routes, eight craft routes and a fix to my
  group script; nothing needed a door I lack.

## Learnings

From the learning capture of this turn:

- **A far buyer that leaves is often found again further out.** Hex Star's gland bid left at 14:55 UTC; by 21:14 UTC
  three stations of other empires bid 5,686 to 7,423, deeper than Hex Star ever was (data/market/history.jsonl).
  My division writes sales that follow the best book each turn, not the station that once bid. Kept in
  `knowledge/hunting-herds.md` (Findings, Practice, Lessons). For the fleet: a good with no home buyer is a search.
- **A fallback bound to a target runs on after the target is met; one bound to the pilot's own stores ends by
  itself.** 46.5 ship-hours of iron after orders ENT-047 (errors.log ENT-108). Kept in `knowledge/hunting-herds.md`
  (Practice). For the fleet: the same class as Trade's ENT-106.
- **A mission line opens only through its first link, and another division may write it.** Voidborn Mastery stood at
  0 for every drone because The Collective Provides was in no Military list (9 of 70 held it). Unpromoted
  (`LEARNINGS.md`); the skill counts each link's holders every turn.
- **A sale run that ends at the wallet keep can read the sweep as a loss** (Sandrift, -8,917 for about +4,303).
  Unpromoted (`LEARNINGS.md`); asked of the Fleet Admiral.
- **In a fight `dist` is a ship's place on one line from the fight's centre, not its distance to the prey, and the prey strikes one ship only.** Flight 2: all at 6, nobody in reach 3, 0 dealt; flight 3: closed to 2 by own dist, all three dealt, the whale hit the leader alone from shield 111 to hull 9 percent in 22 ticks (my script's log, `data/observations`, kind group_hunt). Kept in the skill `military-turn` and the guidebook (section 1, Group hunts); the knowledge file waits for a kill. For the fleet: any ship in a fight must close in by its own dist.
- One thing of my class I do better now: pricing a kill's goods against every book and carrying them to the best
  one. One I do not master yet: a group fight; three starters cannot kill a 220-hull whale, and I do not yet know which prey a group of three can take.

Skill: military-turn changed -- group script: advance by own dist, flee at hull 85 or shield 0; the sale that follows the buyer; crafts as the fallback; the once-chain link count

## Cross-links

- `reports/2026-11-17_apophis_first-group-hunt-no-kill-escort-flies-reserve-kept.md` -- my previous report
- `reports/2026-11-17_unity_iron-met-make-before-gather-acrab-chosen.md` -- the Fleet Admiral's report in force
- `communications/orders.log` ENT-054 -- the orders in force
- `communications/requests.log` ENT-264 -- the seam of `routes.moved`
- `communications/errors.log` ENT-108 -- iron gathered after the orders ended it
- `communications/admirals.log` ENT-068, ENT-069 -- my claim and note of this turn
- `game/routes/guidebook/military.md` -- the Standing Plan and the readings

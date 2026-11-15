---
name: veil-rays-pay-no-ship-lost
id: 20261115T191903Z
tier: report
trigger: session-end
author: Apophis
tags: [military, hunting, wildlife, turn-t4]
links:
  - routes/index.md
  - players/index.md
  - governance/rulebook.md
---

# Military -- The two veil-ray herds pay 3,200 to 3,300 cr per hunter-hour; no ship lost

## Situation

Period: from my birth (2026-11-14) to 2026-11-15 19:20 UTC. This is my
first report; the first drones were registered on 2026-11-15 12:45 UTC
(`data/fleet/birth.log`). No report of the Fleet Admiral stands in
`reports/`: the one she wrote was deleted on 2026-11-15 (commit
50c6b7d). Orders in force: `communications/orders.log` ENT-003, in
force from 19:00 UTC, turn T4, posture HOLD (F2), Voidborn space only
(F3), hunting limits F9. Under F1 the service `dispatch` flies every
drone; I fly none.

Ships: 30/30 active, grounded: 0, lost: 0
Credits: start 3,000, end 344,673, net +341,673
Output: 53 kills in 18 hunt runs (49 verdigris curd, 3 whale oil, 63 carapace, 8 crystallized biogas); 3,091 units of ore in 30 mining runs
Source: `data/fleet/ships/drone-*.json` (wallets, hull, `stats.ships_lost`), read 19:16 UTC; `data/routes/runs.jsonl` (hunt and mine rows, 339 rows read)

- Start is 30 pilots at 100 cr each (rulebook, section 4). Ten drones
  were born at 12:45 to 12:51 UTC and twenty at 18:57 to 18:59 UTC; the
  twenty run their starter missions now.
- Of the net, 344,463 cr are one-time rewards less one-time purchases
  (`data/fleet/onetime.json`, 120 entries of drones). What is left,
  about -2,790 cr, is the repeating part since birth: derived from the
  three records above, not measured by a counter.
- Every drone is a Threshold at 75 of 75 hull. One drone fits a
  Piercing Railgun I; the other 29 carry a Pulse Laser I.
- The fleet collector (`data/fleet/fleet.json`, 19:14:08 UTC, 61-minute
  window) gives Military +1,867 cr per hour (+62 per ship), the only
  division above zero; the fleet stands at -16,258 cr per hour.

## Activities

### Hunting places: kills, credits per hunter-hour, herds

From every hunt row of `data/routes/runs.jsonl` and the herd counts of
`data/wildlife/history.jsonl` and the route notes. Credits are the
wallet change of the run, less goods sold that were carried in from
another route (Hamal: one neural soma, 693 cr; Acubens: 4 curd, 1,320
cr, per the route note).

| Route | Runs | Kills | Hunter-min | Net cr | Cr per hunter-hour | Kills per hunter-hour | Herd counted |
|---|---|---|---|---|---|---|---|
| hunt-gsc-veil-ray | 5 | 30 | 186.0 | 9,928 | 3,203 | 9.7 | 6 (15:09), 7 (17:58), 6 (18:40) |
| hunt-hamal-veil-ray | 5 | 10 | 103.0 | 5,679 | 3,308 | 5.8 | 0 (17:17), 7 (18:06), 0 (18:48) |
| hunt-home-drift-ray | 3 | 6 | 28.3 | -156 | -331 | 12.7 | 9 (17:10), 9 (17:55), 10 (18:46) |
| hunt-acubens-urchin, off | 3 | 6 | 70.4 | -285 | -243 | 5.1 | 3 urchins (15:11), 3 (18:25) |
| hunt-home-whale, off | 1 | 1 | 20.4 | 567 | 1,668 | 2.9 | 3 whales (17:10), 3 (17:55), 4 (18:46) |
| hunt-home-belt, not in the plan | 1 | 0 | 2.7 | -26 | -578 | 0 | not counted |

All hunts: +15,707 cr in 410.8 hunter-minutes, 2,294 cr per
hunter-hour. The orders found 3,300 and 3,600 over four runs each; a
fifth run at each place (957 cr in 23.7 min; and one run with no kill)
brings them to 3,203 and 3,308.

- **The herd, not the gun, sets the pace.** At hunt-gsc-veil-ray the
  herd stood at 6 to 7 through 30 kills in 3.3 hours; at Hamal it grew
  from 0 to 7 in 49 minutes. In these few counts the herds regrew about
  8 to 9 animals an hour, close to the 9.7 kills an hour of one
  pulse-laser hunter at GSC-0027.
- **Damage taken:** not measured per place; the run rows hold no
  damage (request ENT-007). The two run logs that remain show hull 75
  of 75 at every kill line. Lifetime `damage_taken` of the six drones
  with any damage on record: 639, 619, 489, 344, 222 and 45 points.
- **Drift-rays pay nothing:** 8 crystallized biogas from 6 kills; its
  bids are 1 cr (Node Beta) and 2 cr (The Experiment).

### Railgun per hunter

Piercing Railgun I (catalog through the gate, 19:10 UTC): 60 damage
every 3 ticks at reach 5, 70% armor bypass, 5,000 cr (asks at Central
Nexus, 3 units). Pulse Laser I: 10 damage every tick at reach 3. One
railgun shot kills a 60-hull veil-ray; the pulse laser needs six hits
and the log shows wounded rays fleeing at 4 to 18% hull. In one 4-kill
run 18.2 of 23.7 minutes passed at the place. Verdict: it would shorten
runs, but where the herd caps the kills it adds few; at 1.03 curd per
kill (330 cr) it pays back after about 15 extra kills. Not proven
either way: the test costs no purchase (request ENT-008).

### Whale hunter

A pilot-whale has 220 hull; whale oil bids 300 cr at all six stations
(44 to 474 units), so a kill is worth about 900 cr (3 oil). The test
Threshold with one railgun took 7 minutes for the first whale and fell
from 73 to 15 hull in the second fight. The smallest hull I would send:
a Vigil (tier 1, no Piloting gate): hull 75, shield 90 (+3 per tick),
2 weapon, 2 defense, 2 utility slots, CPU 22, power 38. Fit: two
Piercing Railgun I and two Shield Booster I (+25 shield each): CPU 14,
power 32, shield 140, double the Threshold's fire. Cost: market
valuation 34,412 cr (exact price needs `commission_quote`, not run),
10,000 cr of railguns, slug cases at 40 to 52 cr: about 44,400 cr
before insurance (premium not quoted). Payback: about 49 whale kills.
The Recursion (hull 150, shield 150, 3 weapons) needs Piloting 10; our
best drones stand at 4. The Paradox costs 83,382 cr for 60 hull.

### Armed pilots at our hunting grounds

`players/index.md` lists 10 pilots, all neutral. No file records one
at a hunting place. Two had their last recorded jump into Nexus Prime,
the system of the drift-ray and whale cloud: HexBot11 (HEXC, 10 player
ships destroyed, 14:34 UTC) and NovaExidosRim (no faction, 2
destroyed, 10:09 UTC). Their fits are not known. None is recorded
jumping into GSC-0027, Hamal or Acubens. In the census's last two
reads the veil-ray place of GSC-0027 held 1 pilot (17:58, not
identified) and then 0; Hamal and the cloud held 0 both times.

### Requests and FLEET.md

Zero asked whether a miner may work the GSC-0027 nebula beside our
hunter (requests ENT-005): answered yes (ENT-010). The catalog calls
verdigris curd copper paste, so the herd likely grazes copper, which
reads 100,000 there. My `FLEET.md` now lists the 30 drones and my
flagship (F10).

## Problems

- **Two hunts at Hamal without a kill** (17:01 and 18:39 UTC, 14.6
  hunter-minutes, -130 cr). The 18:39 run was started on a count of 7
  read at 18:06, before a run that killed 4; the census read 0 at
  18:48. Cause: the dispatcher's herd check reads a count older than
  the last hunt. Where the last three animals went: cause not found.
  Done: request ENT-006 to Unity.
- **Damage per place is not measured** (the rows hold none). Done:
  request ENT-007.
- **The repeating part of the division is below zero since birth**
  (about -2,790 cr, derived above). The 30 mining runs drones flew
  when no hunt was open cost 2,003 cr for 3,091 units of common ore;
  the drift-ray hunt pays nothing.
- **Urchins gave no radiant bile** in 6 kills; the route is off since
  17:40 UTC (route note: this place has no uranium).
- **Twenty new drones hold 1,068 cr each**, under the 3,000 cr floor of
  F7, 17 hours before the tax assessment of about 2026-11-16 12:00
  UTC. Their starter missions pay; not yet checked that they reach it.
- **The route index shows fewer runs than the run file** (Hamal: 2
  runs, 3,970 cr per hour, against 5 rows). Cause not found; the index
  is Unity's (`fleet/routes.py measure`).
- **The public catalog dump answered 429 twice** (one download per
  minute per address, shared by the whole unit). The same data came
  through the gate's per-pilot catalog; no harm.
- Losses looked for: none. All 30 drones read hull 75 of 75 and
  `ships_lost` 0. Failed orders: none.

## Plans

Inside orders ENT-003, without flying a ship (F1):

1. Next turn, read the hunt rows of T4 and the herd counts again and
   give each place its figure over all runs, the same method as above,
   so turn to turn can be compared.
2. Compare the GSC-0027 veil-ray count before and after the mining
   test Zero asked for (my answer ENT-010); a fall below the ranching
   floor of 4 that the hunts alone do not explain goes to Zero and
   Unity at once.
3. Follow requests ENT-006, ENT-007 and ENT-008 with Unity. If the
   railgun test runs, measure kills per hunter-hour and the herd beside
   the pulse-laser figure of 9.7, and say whether to buy railguns.
4. Watch the whale count of Stellar Siphon in each census read: one
   rise (3 to 4 between 17:55 and 18:46) is all we have. A rate over a
   day decides whether a 44,400 cr Vigil could pay back in a week.
5. Check before the tax that the twenty new drones are above 3,000 cr.
6. Ask Oracle's files what cauldronbacks carry and their hull: their
   alloy scale has one bid (213 cr, 20 units, Synchrony Hub), the only
   creature good with a bid not hunted yet.
7. Keep `FLEET.md` current at every turn.

My own choices: I did not propose buying a whale hunter now (the herd's
regrowth is unknown); I proposed the railgun test over a purchase
because the ship that has one already exists; I answered Zero yes on
the catalog's word, marked as an inference.

## Suggestions

1. **Fly the railgun test (ENT-008).** Reason: it decides whether
   5,000 cr railguns pay; cost: one turn of the railgun ship on a
   veil-ray route instead of mining, no purchase. Unity's.
2. **Count the herd at the end of every hunt (ENT-006).** Reason: 2 of
   5 Hamal runs found no prey; cost: a few lines in the hunt runner or
   the dispatcher. Unity's.
3. **Do not buy a whale hunter yet.** Reason: about 49 kills to pay
   back, herd of 3 to 4, regrowth seen once; cost of waiting: about 900
   cr per whale not taken. Suggi's and Unity's (F9).
4. **Keep the drift-ray route only as the training slot.** It pays 1 to
   2 cr per good but trains Gunnery and Xenobiology; mining trains
   neither. Unity's (plan.json).
5. **Keep one local copy of the catalog per release** in the data
   folder. Reason: the dump allows one download a minute for the whole
   unit; cost: one download per game version. Unity's.

## Cross-links

- `communications/orders.log` -- ENT-003, the orders this period ran under.
- `routes/index.md` -- the route figures and the plan.
- `routes/hunt-gsc-veil-ray.json`, `routes/hunt-hamal-veil-ray.json`, `routes/hunt-home-whale.json` -- the hunt routes and their notes.
- `players/index.md` -- the pilots we know.
- `communications/requests.log` -- ENT-005 (Zero), ENT-006 to ENT-008 (mine), ENT-010 (my answer).
- `governance/rulebook.md` -- sections 4 and 8: starting credits, rules of engagement.

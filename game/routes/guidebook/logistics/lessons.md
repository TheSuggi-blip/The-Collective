# Logistics guidebook -- Lessons (lessons.md)

### How this guidebook is kept
Status: proven. Updated: 2026-11-16. Evidence: migrated from guidebook/logistics.md, the text above its first section.

Kept by Apollo; read by every member. What the Logistics division
learned about its routes, its levelling and its ships, so that every
ship born later starts where the others stand. Started by the Fleet
Admiral on 2026-11-15 from the runs so far; from here Apollo writes it,
at the end of every turn.

- A figure comes from `python3 -B game/fleet/routes.py measure` or from a
  run's RESULT line, and carries its date. A number no record holds is
  written `not measured`.
- The plan in force is the division's plan file (`plan.py show`, the tool
  plan); `game/routes/plan-hauler.md` is written from it, and every route
  with its figure is in `game/routes/master-index.md` and its sub-indexes.

### Fuel: What a Leg Costs (for every Admiral)
Status: proven. Updated: 2026-11-15. Evidence: migrated from guidebook/logistics.md section 6.

Measured from the fleet collector's ship files, sampled every 10 s.

- 1 unit per jump (87 jumps) and 1 per in-system leg (116 legs),
  2026-11-15 19:04 to 19:24 UTC.
- From dock to dock, about n+1 units for a hop of n jumps, billed at the
  arrival refuel of ships that left with a full tank (2026-11-15 21:30
  to 21:45 UTC): 1 jump 2 units (115 of 116 hops), 2 jumps 3 units (2
  hops), 3 jumps 5 units (1 hop).
- Price per unit, all-in (`fuel_price_all_in` of the census files, and
  117 refuels seen): Node Beta 11, The Experiment 11, Node Alpha 12,
  Synchrony Hub 12, Central Nexus 13, Node Gamma 15. The rules say the
  price rises as the tank empties; every bill read was for a nearly
  full tank.
- So: Central Nexus to Node Beta and back costs 48 cr (22 + 26); a
  three-jump hop about 55 to 75 cr one way. A load must beat its round
  trip before tax and before the ship's time.
- Seen 2026-11-15 23:29 to 23:37 UTC: Central Nexus to Synchrony Hub,
  3 jumps, 39 cr; Synchrony Hub to The Experiment, 2 jumps by the
  engine's path, 22 cr.

### Storage by Hand: The Calls and Their Answers
Status: proven. Updated: 2026-11-16. Evidence: migrated from guidebook/logistics.md section 7.

Through `game/fleet/gate.py`, one hauler at a time. A `raw` call holds
the ship by hand by itself (`held by hand: ...`); release it docked.

| Call | Answer |
|---|---|
| `gate.py hold <pilot>` | `held: <pilot> (hand Apollo)` |
| `raw <pilot> view '{"station_id":"central_nexus"}' spacemolt_storage` | the storage there, item by item, and `locations` (every station with goods). The action name `storage` is refused (`invalid_action`) |
| `raw <pilot> craft '{"recipe_id":"basic_iron_smelting","quantity":1,"deliver_to":"storage","preset":"workshop","dry_run":true}'` | `kind: quote`: 10 iron ore for 1 steel plate, `credits_total` 0, venue Station Workshop, 0.27 ticks a run, `have_inputs` true |
| the same quote for `basic_copper_processing` (1), `manufacture_ferrous_slugs` (5) | 8 copper ore for 1 copper wiring, 0 cr, 0.32 ticks; 2 steel plate and 3 iron ore for 5 ferrous slug cases, 0 cr, 1.12 ticks |
| the same quote for `fabricate_circuit_boards` (2026-11-15 23:45 UTC, at The Experiment) | 3 copper ore, 2 silicon ore and 1 energy crystal for 2 circuit boards, 0 cr, 6 ticks a run, Station Workshop; with or without `preset` the same venue |
| the same without `preset`, `refine_steel` (2), `process_copper_wiring` (2) | a rented public facility: 5 iron ore for 2 plate, 19 cr (10 labor, 9 fee); 4 copper ore for 2 wiring, 17 cr (7 labor, 10 fee) |
| `craft` as above without `dry_run` (quantity 2) | `kind: job` with a `job_id` in `structuredContent.details`; the text part of the answer carries the ship's location |
| `craft '{}'` (no recipe) | the queue: `total_jobs` 0 after 34 s, the job done |
| `raw <pilot> view_market '{"item_id":"voidborn_neural_soma"}' spacemolt_market` | every level of both sides with its `source`: at Synchrony Hub at 23:33 UTC `buy 678cr 3 station` |
| `raw <pilot> sell '{"item_id":"voidborn_neural_soma","quantity":3}'` with an empty hold | taken from storage there: credits 34,597 to 36,631 (+2,034, 3 x 678); the bid was empty after it |
| `raw <pilot> withdraw '{"item_id":"...","quantity":1,"target":"self"}' spacemolt_storage` | storage to hold. With `"target":"cargo"` refused: `invalid_target`, valid targets are `self` and `faction`; player, empire, `faction:TAG` and `station:ID` targets are deposit-only |
| `raw <pilot> deposit '{"item_id":"...","quantity":1,"target":"self","source":"cargo"}' spacemolt_storage` | hold to storage at the station where the ship is docked |
| `raw <pilot> deposit '{"item_id":"...","quantity":N,"target":"<another pilot of ours>","source":"cargo"}' spacemolt_storage` | hold to that pilot's storage at this station; the wall let it pass (2026-11-16, before 04:55 UTC). `scripts/gather.py` of the skill logistics-stock does it for many donors, withdraw first where the goods lie in storage |
| `gate.py release <pilot>` | `released: <pilot>`, docked |

The workshop runs only while the pilot stays docked there, takes the
inputs from that pilot's own storage at that station, and costs no
credits. Storage is personal: a good another pilot stores is moved to
another pilot only by a deposit to that player, which is a gift.

### What the Ice Routes Leave Behind
Status: proven. Updated: 2026-11-17. Evidence: migrated from guidebook/logistics.md section 9.

From the books of our six stations and of LHS 1140 (the first foreign
book), 2026-11-15 22:51 to 23:45 UTC, and the catalog's recipes:

| Good | Buyer |
|---|---|
| Water ice | Station bids with depth: 20 to 34 cr for 905 to 26,340 units at five stations (23:43 to 23:45 UTC) |
| Methane ice | Station pools of 1,000 that empty and refill: 47 cr at Synchrony Hub and The Experiment from 20:33 UTC, 36 cr at Node Gamma and Node Alpha; all six stations read 0 or 7 cr from 23:20 to 23:29 UTC, five stood at 36 cr for 1,000 again from 23:32 to 23:36 and Synchrony Hub by 23:45 UTC (`data/market/history.jsonl`) |
| Deuterium ice | Thin: station bids of 188 to 226 cr for 5 and 6 units at Node Beta and Node Alpha, seen in six moves of the book from 20:45 to 22:51 UTC; 2 to 3 cr at The Experiment |
| Nitrogen ice | 2 cr for 49 at The Experiment (the only bid read). Its hand recipe (5 ice to 4 liquid nitrogen) meets a 2 cr bid |
| Helium ice | 2 cr for 500 at The Experiment; its recipe is facility-only and helium-3 is bid 2 cr |
| Oxygen ice | No bid; its recipe is facility-only and oxygen gas has no bid |

LHS 1140 bids for methane ice only (36 cr for 500 at 23:45 UTC; nothing at 23:21 UTC). And no ship carries goods of value out of
Voidborn space (orders F13): a buyer beyond the border is no use to the
goods we store until that order changes.

### The Harvester Chain: an Ice Harvester I Made by Hand
Status: proven. Updated: 2026-11-16. Evidence: migrated from guidebook/logistics.md section 11.

Tested 2026-11-16 with one hauler at the Central Nexus workshop (orders.log
ENT-011, block APOLLO). Every step is a by-hand recipe at the Station
Workshop: 0 cr fee, no skill asked for in any quote (`craft` with
`dry_run`), and the work runs only while the pilot stays docked there.

| Step | Recipe, runs | Inputs | Out | Time |
|---|---|---|---|---|
| Steel | `basic_iron_smelting` x4 | 40 iron ore (stored) | 4 steel plate | 0.27 ticks a run |
| Wiring | `basic_copper_processing` x2 | 16 copper ore (stored) | 2 copper wiring | 0.32 ticks a run |
| Boards | `carbon_arc_circuit_etching` x1 | 2 silicon ore, 12 carbon ore (stored) | 3 circuit boards | 6 ticks |
| Power cell | `build_power_cell` x1 | 2 circuit boards, 3 energy crystal, 2 copper wiring | 1 power cell | 6.75 ticks |
| Harvester | `build_ice_harvester_i` x1 | 4 steel plate, 2 circuit boards, 3 flex polymer, 1 power cell | 1 Ice Harvester I | 15 ticks |

Measured: the crafts ran from 03:07 to 03:14 UTC, about 7 minutes with
the waits between steps; the hop from Node Beta and the docking took 5
minutes before. Bought at Central Nexus at the asks of the 03:05 UTC book:
2 silicon ore (380 each), 2 energy crystal (420 each; the third was
stored), 1 circuit board (436; the fourth board, since one etching gives 3)
and 3 flex polymer (276 each): 2,891 cr with the 1% tax. The Central
Nexus power cell ask of 415 x 1 (02:51 UTC book) was gone by 03:05 UTC
(1,995 x 52), so the cell was made.

What one costs, by where its inputs come from:

| Inputs | Cost of one harvester |
|---|---|
| All bought at Central Nexus (silicon 380, crystal 420, flex 276) | about 3,130 cr with tax |
| Silicon and crystal bought, flex at Node Alpha (129 x 102, 02:46 UTC) | about 2,690 cr with tax |
| The fleet's own silicon and crystal, flex bought at Node Alpha | about 390 cr in flex, plus goods whose best bids are 40 to 60 cr: about 680 cr in all |
| Bought whole | 1,413 cr at four of our stations; 638 cr at LHS 1140, six lawless jumps out |

So the chain pays only from the fleet's own silicon ore and energy
crystal. What bounds it (`stock`, 2026-11-16 03:14 UTC): 48 silicon ore
(47 in Mining's storage), 135 energy crystal (132 Mining's), 226 carbon
ore spread over five divisions. At 2.67 silicon, 16 carbon and 3 crystal
a harvester, carbon bounds it at about 14 and silicon at about 18. Each
pilot crafts from its own storage only: the goods are first deposited
into one pilot's storage at one station (a gift between our own pilots,
which the wall lets pass).

Staged for ten (2026-11-16 04:51 to 05:15 UTC): `scripts/gather.py` of the
skill logistics-stock moved 101 carbon ore, 138 iron ore and 106 copper ore
from six haulers docked at Central Nexus into the crafting hauler's
storage there; one hauler bought 30 flex polymer at Node Alpha at 129 cr
(3,908 cr, 3,958 with fuel); the workshop made 20 steel plate and 18 copper
wiring from them, free. That storage then held 20 steel plate, 18 copper
wiring, 103 carbon ore, 30 flex polymer and the harvester made before.
What ten more take: 40 steel plate, 40 circuit boards (14 etchings: 28
silicon, 168 carbon; or `fabricate_circuit_boards`, 2 silicon, 3 copper
and 1 crystal for 2 boards), 10 power cells (30 crystal, 20 wiring) and 30
flex. With 103 carbon and 30 silicon: 8 etchings and 7 fabrications give
38 boards, so 9 harvesters; 20 more steel plate (200 iron ore) and 2
wiring are still to be gathered.

Five made (2026-11-16 08:52 to 09:24 UTC, one hauler at the Central Nexus
workshop, by `craftchain.py` of the skill logistics-stock): 7 carbon-arc
etchings (14 silicon, 84 carbon) gave 21 boards, then 5 power cells, then 5
harvesters; 0 cr fee, no skill asked, about 32 minutes of crafting with the
waits. The etchings came as jobs of 3, 2, 1 and 1 runs because a craft's
`quantity` counts made units, rounded up to runs: 7 asked of a recipe that makes
3 a run is 3 runs (queue.log ENT-114, 2026-11-16 19:02 UTC); 5 power cells and 5
harvesters, 1 a run, were queued whole (about 32 and 70 ticks). The harvesters took about 18
minutes for five, about 3.6 minutes each against 13.9 ticks quoted (about
2.5 minutes at 11 s a tick). Mining gave 30 silicon ore and
35 energy crystal by deposit (requests.log ENT-124). The first harvester is
fitted to the hauler that made it (09:25 UTC); the five lie in its storage,
unplaced, because the bids bound ice work (section 12). Left there: 16
silicon, 20 crystal, 19 carbon, 15 flex polymer, 8 wiring, 1 board; four
more need 160 iron ore and about 15 copper ore gathered (1 etching and 6
`fabricate_circuit_boards` runs for their 16 boards).

### Capacity of the Domain (orders F18)
Status: proven. Updated: 2026-11-17. Evidence: migrated from guidebook/logistics.md section 12.

Read 2026-11-16 23:49 to 2026-11-17 00:24 UTC (the tools stock with view=reserve, base_plan with
kind=station, fill with action=status, the runs table):

- Storage of Logistics at Node Beta: iron ore from 25 to 1,892 a pilot in 39 storages
  (Node Beta 600 or more in 19), copper ore up to 1,295 a pilot, energy crystal 1 to 15 in
  22 storages; the faction's 293 steel plate and 4 copper piping in one storage; at Central
  Nexus 32 silicon, 20 energy crystal, 15 flex polymer, 5 Ice Harvester I and carbon ore 1 to
  89 in 23 storages.
- What limits it first: the bids for the stored goods; the silicon for the boards (Trade's
  claim on the one deep ask); iron for the station.
- Ships the division's work employs: 33 on the shared gather fields, 1 on the steel craft,
  1 on the gold test, up to 11 on stored goods while their bids stand, up to 3 on gas, the
  once line for the rest. Logistics needs no more ships.

Read 2026-11-16 12:48 to 13:36 UTC (the tools stock, catalog with ask=can,
base_plan with kind=station, fill with action=status):

- Storage of Logistics: iron ore 11,431 and copper ore 6,063 at Central Nexus,
  Node Beta and Synchrony Hub; at Node Beta 213 argon, 204 hydrogen (made into 75
  liquid hydrogen at 13:35 UTC), 175 neon, 105 null matter and 83 plasma gas; 58
  neural soma by ones to fours in 29 storages (Synchrony Hub 30, Node Beta 21,
  Central Nexus 5, The Experiment 2; storage book of 13:44 UTC); 128 platinum, 30
  palladium, 84 nickel, 46 rhodium and 32 osmium ore from the reef of The
  Collective Provides; 6 armor plate (Node Beta 3, The Experiment 3); the chain's
  goods and 5 made Ice Harvester I at Central Nexus.
- What it makes by hand today (ask=can): steel plate and copper wiring from the
  ore (bids of 15 and 2 cr), ionized neon (bid 2 cr), one armor plate, and liquid
  hydrogen (111 cr x 112 at Central Nexus). The liquid hydrogen and the plate stood
  at the highest bids of these (books of 12:48 to 13:36 UTC).
- What limits it first: the bids. Soma pools of 1 to 4 at 376 to 734 cr, plate
  pools of 4 to 6 at 234 to 361 cr, plasma 33 at 96 cr, hydrogen gas 1 unit at
  34 cr at Node Beta at 13:36 UTC; water ice no bid at Central Nexus at 12:48 UTC.
- Ships the hauling employs: the once line for 5 to 10 haulers this turn; one
  ship per stored-goods route while its bid stands; three gas tests. No repeating
  route pays a hauler. Logistics needs no more ships.
- For the station (S6, base_plan 12:55 UTC): the five inputs the fleet holds most
  of by units are iron ore (59,564 of 491,400), copper ore (40,988 of 768),
  carbon ore (1,335 of 97,008), creature carapace (787 of 35,640) and platinum ore
  (523 of 3,720); the five it lacks most are iron ore (431,836 short; fields of
  100,000 at Ruchbah and Nightveil), salvage metal (249,600; no field, no offer),
  carbon ore (95,673; Gliese 876 and Furud belts, 44,531 on offer at 4 cr at Nova
  Terra Central), anchor plate (93,690; none) and alloy scale (56,520; none).
  Proposed to keep rather than sell: platinum ore (short 3,197; bid 63 cr, ask
  150 cr at Central Nexus), iron and copper ore (kept already), energy crystal
  (120 of 80) and nitrogen bladder (13 of 192; bid 1 to 2 cr).

Read 2026-11-16 08:47 to 09:00 UTC (the tools stock, fleet with
view=capacity, catalog with ask=can, base_plan with kind=station):

- Storage of Logistics: iron ore 11,431 and copper ore 6,063 at Node Beta,
  Synchrony Hub and Central Nexus; 204 hydrogen, 213 argon, 175 neon and 83
  plasma gas at Node Beta; 58 neural soma (storage book of 09:16 UTC); the chain's goods at Central
  Nexus; 6 armor plate after this turn's sales.
- What it makes by hand today (ask=can): armor plate from the carapace
  left (about 1 to 3 plates a station), 75 liquid hydrogen (bid 98 x 12),
  copper wiring and steel plate with no bid worth a sale.
- The work a harvester opens: water ice is bid at 29 cr for 5,333 units at
  Central Nexus, about 20 ships for four hours, methane ice about 27, and 48
  ships carry a harvester. The bids, not the tool, bound ice work today, as
  Zero answered (requests.log ENT-115).
- Ships the hauling employs: the once missions for every hauler that turn; no
  repeating route was measured for haulers then. Logistics needs no more ships; each
  repeating place that opens (a bid that regains more than the miners take)
  is one waiting hauler put to work.
- For the station (S6, base_plan 08:59 UTC): the five inputs the fleet holds
  most of against the need are copper ore (40,928 held, 768 needed), iron
  ore (59,458 of 491,400), creature carapace (746 of 35,640), carbon ore
  (814 of 97,008) and energy crystal (135 of 80); the five it lacks most are
  iron ore (431,942 short; fields of 100,000 at Dimming Pocket and Low
  Charge Glint), salvage metal (249,600; no field, no offer), carbon ore
  (96,194; Gliese 876 and Furud belts, 44,531 on offer at 4 cr at Nova Terra
  Central), anchor plate (93,690; none) and alloy scale (56,520; none).

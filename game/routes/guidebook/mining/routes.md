# Mining guidebook -- Routes (routes.md)

### Standing Plan
Status: proven. Updated: 2026-11-17. Evidence: migrated from guidebook/mining.md section Standing Plan.

What the miners fly between two turns (2026-11-17 23:26 UTC, orders.log
ENT-050). The reserve's iron is met: 356,467 iron ore held against the
323,780 it takes, and that iron is the steel plate still to make, 32,378
plates of 10 iron each (surplus.py reserve, 23:04 UTC). So the division
makes before it gathers, and gathers only what the reserve lacks. A free
miner takes the first open route of the list First (the once routes:
the Voidborn chain, the two new Voidborn mining links, The Forge Tax,
Deep Core at Deep Range, the First Hunts), its own routes (soma sales and
carries where it stores soma, `@ice-sell`, the outpost route for the
seated miners, then `@reserve-prism` or `@reserve-hamal`), then the list
Then as the supply pass keeps it.

| # | Route | Ships (max) | Field or bid now | Measured | What it is for |
|---|---|---|---|---|---|
| F | `voidborn-crystal-resonance`, `voidborn-material-synthesis` | 1; 1 | Prism Scatter 86 energy crystal, Spacetime Seep 15,844 iron (22:44 UTC) | tests from 23:19 UTC | Voidborn Mastery for the 68 pilots holding The Collective Provides (rule F35) |
| F | `mission-the-forge-tax-crucible`, `mission-deep-core-prospecting-first-step` | 3; 2 | Hearsay Cobalt 3,222 (17:00 UTC); Deep Range 531 platinum (16:48 UTC) | two hand-ins each, +4,340 to +4,631 cr a run in 67 to 79 minutes | 5,000 cr once a pilot and 20 units of a reserve ore kept |
| 1 | soma sales and carries; `@ice-sell` drains and carries | 1 each | soma bids at four stations; no water-ice bid | 4,580 to 10,150 per ship-hour (route_earnings, 4 h) | Stored goods sold where a bid stands |
| 2 | `mine-dheneb-cryobelt` | 2 | Hex Star methane 36 cr x 643 (22:47 UTC) | 906 per ship-hour, 9 runs (4 h) | Ice only where a bid stands |
| 3 | `gather-gsc-0044-belt-faction` | 1, lift_to 10 | GSC-0044 Belt 100,000 iron, 100,000 copper | test from 23:19 UTC | The outpost's faction storage, seated miners only (orders ENT-050, ZERO (1)) |
| 4 | `craft-steel-experiment`, `craft-steel-node-beta` | 10; 11 (shared) | 137,676 and 39,514 iron in miners' storage (23:03 UTC) | Experiment: first run 2.9 minutes, 0 cr, 50 plates | Steel plate for the reserve from our own iron |
| 5 | `gather-goldcrest-gold` | 3 | 9,159 gold (21:06 UTC), about 830 back an hour | 325 gold in 90 minutes, -767 cr (one run) | Gold, short 14,068 |
| 6 | `gather-subra-floodlight-flats-silicon` | 2, floor 500 | 3,739 silicon, about 90 back an hour | 422 to 464 ore a run of 90 to 94 minutes, a third silicon, -35 to -43 cr | Silicon, short 51,567 |
| 7 | `gather-jadecove-nickel` | 1 | Long Errand Band 1,745 nickel (18:15 UTC) | test from 23:22 UTC | Nickel, short 15,486 |
| 8 | `gather-acubens-belt-carbon` | 2 | 170 carbon, about 56 back an hour | -234 cr a run | Carbon, short 88,913 (bought at 4 cr is cheaper: Trade's) |
| Then | as the supply pass keeps it: iron sources while the chain iron-ore reads short, the steel crafts, census, park | shared | -- | -- | Standing work for the rest |

Why this plan. Mining stored +9,845 units of the reserve's items an hour
over the 4 hours to 23:24 UTC (hive.py flow Zero): iron +5,972, copper
+3,225, gold +246, carbon +229, platinum +38, silicon +34, nickel +14.
Iron and copper were no longer needed: that fuel fed nothing. Steel
plate from stored iron is reserve work at about 0 cr, and the short ores
lie in few fields, most of them far from our stations: gold (The Gold
Crest), silicon (Floodlight Flats), nickel (Jadecove), carbon (Acubens).
A unit gathered there costs 1 to 5 cr of fuel against asks of 312 to 632
cr for silicon; carbon is asked at 4 cr, so buying it is cheaper.

What would change it: the RESULT lines of the five tests; the supply
chain iron-ore renewed (requests.log, turn of 23:00 UTC), which takes the
iron sources out of the list Then; more miners seated in the faction;
a deep water-ice order at Central Nexus; the stored iron all smelted.
Each turn starts with `stalled.py` of the mining-chains skill,
`fill.py status miner`, `hive.py flow Zero` and `surplus.py reserve`.

### Route Guides
Status: proven. Updated: 2026-11-16. Evidence: migrated from guidebook/mining.md section 1.

How each kind of route of this division is flown: the fit and the
skills it needs, its place, its steps, what opens and closes it. A
credits figure in this section is a dated reading and no verdict: what
a route earns now is in the fleet's database with its age (rule F22;
the tool `routes`, the view `route_earnings`).

### Drains and carries of stored goods (kind `circuit`)
Status: proven. Updated: 2026-11-16. Evidence: migrated from guidebook/mining.md section 1.

- Fit: none; any miner flies them. Trains Piloting and Trading.
- A drain sells at the station where the goods lie: stop 1 stores the
  hold, withdraws the item and sells it into the bid at `min_price` or
  more (the withdraw takes only what the bid takes); stop 2 stores what
  is left. A carry withdraws a load (65 units, `qty`), flies it to the
  bid's station, sells, stores the rest there.
- Opens only for a pilot that stores the item itself (`requires.stored`,
  per pilot) while a book read within the hour shows the bid
  (`requires.bid`). Comes first in every list: what is stored is sold
  before more is mined.
- Readings: `drain-methane-experiment` 17,639 per ship-hour over 13 runs
  (12 h to 23:02 UTC), about 2,280 cr a run of 7 minutes; the water-ice
  drains and carries flew no run in 11 hours (no bid of 30 units).

### Ice mine routes (kind `mine`, with `sell`)
Status: proven. Updated: 2026-11-16. Evidence: migrated from guidebook/mining.md section 1.

- Fit: Ice Harvester I (a mining laser alone takes no ice). Trains
  Mining and Piloting.
- `mine.py` mines for `minutes`, flies to the station, sells the hold
  then the pilot's storage there into every bid level at the floor or
  more, stores the rest.
- Opens only on `requires.bid`: the Central Nexus routes on an order of
  300 water ice at its best price. Count the jumps from field to buyer
  first: one-jump routes measured 7,280 to 8,950 per ship-hour on
  2026-11-16 morning, four- and five-jump routes 1,210 to 2,990.
- Methane comes with the water, not alone: Ruchbah Ice Belt gave 10 to
  17 methane in loads of 311 to 344 units (four runs, 10:11 to 11:39
  UTC, 2026-11-16), about 3 to 5 percent.

### Standing work for the reserve (kind `mine`, no `sell`)
Status: proven. Updated: 2026-11-17. Evidence: migrated from guidebook/mining.md section 1.

- Fit: Mining Laser I. Trains Mining (one XP a unit mined).
- Mines for 45 minutes, stores everything at its station, sells
  nothing; closes below its `min_left` floor and opens when the field
  has grown back. It is never judged on its pay (rule F8).
- Readings, the 4 hours to 23:30 UTC (data/routes/runs.jsonl, steady
  money from route_earnings): Prism Scatter 207 ore a ship-hour, 65%
  iron by what the field gave up, about 135 iron, -139 cr a ship-hour;
  Hamal Crystal Bloom 180 ore, 51% iron, about 92 iron, -168 cr; Acubens
  Shadow Pocket 281 ore while it was open. Ironhollow's first run: 233
  ore in 45 minutes, -165 cr (2026-11-16 19:16 UTC).
- A standing run ends docked with its hold stored (mine.py
  `store_last_load`, commit 0eca38b, 2026-11-17 03:13 UTC). Before it, a
  run without `sell` stopped the engine's loop at its time and left the
  partial load aboard: 34 miners waited at 03:02 UTC with 10 to 42 units
  aboard, closed out of every route that wants an empty hold.
- Readings of the night of 2026-11-16 to 17 (data/routes/runs.jsonl):
  Schedar Belt 195 to 221 ore a run of 45 minutes, -156 to -168 cr;
  Ironhollow Fading Signal 191 to 242 ore, -132 to -165 cr; fields four
  to seven jumps from their station (Gliese 876, Stillwork, Gaugewatch,
  Gossamer Null, GSC-0033, Thinspace, Dewfall Fray) 104 to 224 ore in 65
  to 101 minutes, -338 to -1,020 cr a run.
- Readings of 2026-11-17 03:00 to 07:00 UTC (miner runs, medians; 15
  runs of the window carry gifts of 10,000 cr or more to the Fleet
  Admiral's flagship, data/fleet/gifts.jsonl, so their sums mislead):
  Schedar Belt 84 runs, 260 ore in 46.5 minutes, -204 cr a run; Ironhollow
  Fading Signal 46 runs, 256 ore in 47.9 minutes, -165 cr; Pherkad 77
  runs, 159 ore in 48.2 minutes, -182 cr; Echo Ejecta 4 runs, 172 ore in
  55 minutes; Garnet Belt 3 runs, 176 ore in 87 minutes (two jumps). The
  end step of commit 0eca38b held: at 07:03 UTC no miner waited with ore
  aboard (`fill.py status miner`).
- A floor does not make a field grow back faster: the game refills a
  depleted deposit gradually in proportion to its capacity
  (game/rules/13-not-stated.md, from the official mining page), and
  Hamal grew back about 360 iron an hour at 31,000 while closed (table
  readings, 03:52 to 06:18 UTC). Floors are 20,000 iron since 2026-11-17
  07:12 UTC; a floor keeps a stock for later and stops the open-close
  flapping of a field near it, nothing more.
- What the fields grew back (hive.py refill, 23:03 UTC): Ironhollow
  Fading Signal 522 iron an hour, Pherkad 267, LHS 1140 Prospectors'
  Leavings 258, Antares Afternoon Drift 254; Acubens Belt 56 carbon
  (readings, 12 h); Prism Scatter and Hamal near 0 while ships work
  them. A field we read was seen back at 100,000 between two reads
  (Prism Scatter, 2026-11-16): how a field refills in one step is not
  known.

### Tests beyond the border (kind `mine`, one good sold)
Status: proven. Updated: 2026-11-16. Evidence: migrated from guidebook/mining.md section 1.

- Written by the route maker, added one ship at a time by the tool
  fill. Each sells null matter at Central Nexus (221 cr x 10, 106 units
  in all levels, 23:03 UTC) and stores the iron and copper there.
- `requires.empty_hold`; one ship until the first RESULT line (rules F8,
  F13). Read the pilots met at the place before lifting (the table
  `met`): combat drones of the faction tagged BUSY were seen in combat at
  Ironhollow Fading Signal (19:52 UTC) and Gliese 876 Belt (23:04 UTC).
- Seven tests share one bid of 106 units: their null matter is a bonus;
  the iron they store is what they are for.

### Fits by hand
Status: proven. Updated: 2026-11-16. Evidence: migrated from guidebook/mining.md section 1.

- `refit.py` of the mining-chains skill swaps a module at a station.
  When the engine's goal answers 409 ("another request ... is already
  being processed") for minutes, the raw market `buy` takes the best ask
  at once: read the ask first (2026-11-16 23:16 UTC, one Mining Laser I
  at 1,600 cr plus 1% at Central Nexus).

### Route Templates
Status: proven. Updated: 2026-11-17. Evidence: migrated from guidebook/mining.md section 2.

A kind of work is a named list of routes: a template, kept in
`game/routes/templates/mining.json` and listed in
`game/routes/templates-mining.md`. A ship's row in the plan file names a
template as `@<name>`, alone or beside routes of its own.

| Template | For | Trains | Fit |
|---|---|---|---|
| `ice-sell` | Stored null matter, methane and ice sold where a bid stands, then the water-ice mine routes on a deep order | Mining, Piloting, Trading | none for the drains; Ice Harvester I for the mine routes |
| `reserve-prism` | Make, then gather what the reserve lacks: a loaded hold stored, steel plate from the pilot's own iron at The Experiment and Node Beta, then gold, silicon, nickel and carbon (since 2026-11-17 23:20 UTC; the iron fields left it when the reserve's iron was met) | Mining, Crafting, Refining | Mining Laser I |
| `reserve-hamal` | The same with the short-ore fields in the other order (carbon, nickel, silicon, gold), so the division is spread | Mining, Crafting, Refining | Mining Laser I |

| Task | How |
|---|---|
| See the templates and how many ships use each | the tool `plan` with `action=templates` (`plan.py templates`) |
| Make or change one | `plan.py template <name> <routes with commas> --title "..." --trains <skills> --note "..."` |
| Put ships on one | `plan.py set <ships> @ice-sell,@reserve-prism` |

A ship born tomorrow gets `@ice-sell,@reserve-prism` (or `-hamal`) and
is at work within the minute. A one-ship test goes in front of a ship's
templates as a route of its own.

This guidebook keeps no list of routes that did not pay (Suggi,
2026-11-16; rule F22). What a route earns now, with its age, is asked
each turn: the tool `routes`, or `SELECT * FROM route_earnings` through
the tool `sql`.

### Missions That Pay Once
Status: proven. Updated: 2026-11-17. Evidence: migrated from guidebook/mining.md section 3.

The `once` routes at the head of the plan: every pilot flies them
first.

| Route | Pays | Measured | Date | Note |
|---|---|---|---|---|
| `voidborn-concurrent` (Concurrent Approval) | 3,000 cr | 39 miner runs, +115,037 cr, of it 117,000 once | 2026-11-15 | Its two neural soma come with the accept |
| `voidborn-mining-missions` (Iron Supply Run, Copper Requisition) | 1,500 + 1,800 cr | 3 runs by 22:24 UTC, +6,430 cr | 2026-11-15 | Booked for every miner now |
| `voidborn-precedence` | 4,000 cr | 146 runs of the fleet, 580,000 cr once | 2026-11-16 | Booked for every miner now |
| `voidborn-first-hunt-*` (three herds) | 930 to 970 cr | one ship each at a time | 2026-11-16 | The home herds read 0 to 3 grazers (queue.log ENT-063): slow |
| `voidborn-signal-fragments` | 7,000 cr | 40 miner runs, +275,879 cr | 2026-11-16 08:00 to 12:20 UTC | Pilots with navigation 3 |
| `voidborn-conductive-lattice` | about 10,900 cr | 32 miner runs, +273,451 cr | 2026-11-16 08:00 to 12:20 UTC | The Node Beta chain |
| `voidborn-network-expansion` | 1,500 cr | 12 miner runs, +17,374 cr | 2026-11-16 08:00 to 12:20 UTC | After First Steps |

The mining missions of the boards (rule F34; data/missions, read
2026-11-17 11:05 UTC); each counts only units the pilot mines itself:

| Mission | Asks | Pays | Where the ore lies | State |
|---|---|---|---|---|
| Deep Core Prospecting (nine boards) | 20 platinum ore | 5,000 cr, 10 exotic matter, deep core mining 25 XP | Markab Belt 503 of 8,000 at 07:57 UTC, 0 at 17:04 UTC; Deep Range Mineral Fields 531 (2 jumps from First Step Memorial's board); 82 Eridani Belt 563; Stillwater 199 | `mission-deep-core-prospecting-nova-terra`: 11 pilots handed in from 11:20 to 18:40 UTC (+5,000 cr each, runs of 41 to 66 minutes), 5 runs found too little; it rests. The pilot keeps its 20 platinum in storage after the hand-in. `mission-deep-core-prospecting-first-step`: two hand-ins (+4,631 and +4,604 cr a run, 76 and 79 minutes), 2 ships and 12 pilots from 23:16 UTC |
| Titanium Extraction Contract (ten boards) | 20 titanium ore | 3,500 cr, mining 25 XP | 70 at GSC-0028, 50 at Jasmine, 12 or less elsewhere (7 to 11 jumps) | not flown: no field holds a load |
| The Forge Tax (The Crucible Garrison) | 20 cobalt ore | 5,000 cr, mining 20 XP | Hearsay Cobalt in Sargas 3,222 (18 jumps from the board); Tabit 270 (29 jumps) | `mission-the-forge-tax-crucible`: two hand-ins (+4,364 and +4,340 cr a run, 67 and 68 minutes), 3 ships and 20 pilots from 23:16 UTC |
| Crystal Resonance Harvest (Central Nexus, after The Collective Provides) | 20 energy crystal | 4,000 cr, Voidborn Mastery 35, mining 45 XP | Prism Scatter 86 (2 jumps), Thornhaven 69, Cedarhold 66, Okab 58 | `voidborn-crystal-resonance`: one-ship test from 23:19 UTC |
| Material Synthesis: Basic (Central Nexus, after The Collective Provides) | 10 iron ore mined and 1 steel plate smelted | 1,500 cr, Voidborn Mastery 25, crafting 25 XP | Spacetime Seep 15,844 iron (2 jumps) | `voidborn-material-synthesis`: one-ship test from 23:19 UTC |
| Amplification Materials (Central Nexus, after The Collective Provides) | 15 silver ore | 4,000 cr, Voidborn Mastery 25 XP | Errai Belt 284 (14 jumps, read 12:13 UTC); Elnath and Avior 0 | not flown: no silver field near |
| The Collective Provides (Central Nexus, the Voidborn chain) | 20 nickel ore | 2,500 cr, Voidborn Mastery 25 XP | Gliese 876 Belt 635 of 12,000, about 28 back an hour (7 jumps, 3 from the pirate stronghold Gliese 581); Algorab 1,342 (12 jumps); Jadecove 609, Azha 570, Rotanev 424; GSC-0049 reef 39, about 10 back an hour | Trade's route, off; the readings in admirals.log ENT-029 |

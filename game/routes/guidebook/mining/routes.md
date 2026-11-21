# Mining guidebook -- Routes (routes.md)

### Standing Plan
Status: proven. Updated: 2026-11-21. Evidence: the plan file (tool plan, show); fill.py status miner; surplus.py reserve; the runs of each route (hive.py route <id>).

Turn of 2026-11-21 19:30 UTC (orders ENT-056, block ZERO). A free miner
takes the list First (the Voidborn links, The Forge Tax, Deep Core at
Deep Range, the First Hunts), its own routes, then the list Then as the
supply pass keeps it.

| Route | Ships | For |
|---|---|---|
| soma sales and carries, `@ice-sell` | 1 each, on goods stored and a bid | stored goods sold |
| `mine-dheneb-cryobelt` | 2 | methane where a bid stands |
| `gather-gsc-0044-belt-faction` | 10, seated miners only | the outpost's faction storage |
| `craft-steel-experiment`, `craft-steel-node-beta` | 10; 11 shared | steel plate of our own iron |
| `gather-subra-floodlight-flats-silicon` | 8 | silicon |
| `gather-goldcrest-gold` | 6 | gold |
| `gather-jadecove-nickel` | 3 | nickel |
| `gather-acubens-belt-carbon` | 1 | carbon: the field carries one |
| Then | shared | iron while the chain iron-ore reads short, the steel crafts, park |

Each limit stays under what its field carries (the briefing's column
`carries`). What would change it: fresh reads of the far fields, the
storage book's read of every miner after the resume, more seats in the
faction, a deep water-ice bid. Each turn: stalled.py, fill.py status
miner, surplus.py reserve.

### Route Guides
Status: retired. Updated: 2026-11-21. Evidence: migrated from guidebook/mining.md section 1.

How each kind of route of this division is flown: the fit and the
skills it needs, its place, its steps, what opens and closes it. A
credits figure in this section is a dated reading and no verdict: what
a route earns now is in the fleet's database with its age (rule F22;
the tool `routes`, the view `route_earnings`).

### Drains and carries of stored goods (kind `circuit`)
Status: proven. Updated: 2026-11-21. Evidence: drain-methane-experiment and carry-null-matter-synchrony-nexus (hive.py route <id>).

- Fit: none. Trains Piloting and Trading.
- A drain sells where the goods lie: stop 1 stores the hold, withdraws
  the item and sells it into the bid at `min_price` or more; stop 2
  stores the rest. A carry withdraws a load (`qty`), flies it to the
  bid, sells, stores the rest there.
- Opens only for a pilot that stores the item itself (`requires.stored`,
  sized per pilot) while a book read within the hour shows the bid
  (`requires.bid`); first in every list: what is stored is sold before
  more is mined.

### Ice mine routes (kind `mine`, with `sell`)
Status: proven. Updated: 2026-11-21. Evidence: the ice routes' runs of 2026-11-16 (data/routes/runs.jsonl).

- Fit: Ice Harvester I. Trains Mining and Piloting.
- `mine.py` mines for `minutes`, flies to the station, sells the hold
  then the pilot's storage there into every bid level at the floor or
  more, stores the rest.
- Opens only on `requires.bid` (Central Nexus: an order of 300 units at
  its best price). Count the jumps first: one-jump routes measured 7,280
  to 8,950 per ship-hour, four- and five-jump routes 1,210 to 2,990
  (2026-11-16). Methane comes with the water, 3 to 5 percent of a load.

### Standing work for the reserve (kind `mine`, no `sell`)
Status: proven. Updated: 2026-11-21. Evidence: game/rules/13-not-stated.md; table readings; mine.py commit 0eca38b; the gather runs (hive.py route <id>).

- Fit: Mining Laser I. Trains Mining (one XP a unit mined).
- Mines for `minutes`, stores everything at its station, sells nothing;
  closes below its `min_left` floor and opens when the field grows back,
  never judged on its pay (rule F8). The pull rule (F36) closes it while
  every good it brings stands at its max.
- A run ends docked with its hold stored (mine.py `store_last_load`): a
  partial load aboard closes every `empty_hold` route to the ship.
- Choose a field by jumps to the nearest station of ours first, then
  richness: one jump out gave 191 to 260 ore in 45 minutes, four to
  seven jumps 104 to 224 in 65 to 101 (2026-11-16/17). The far short-ore
  fields run 90 minutes: Gold Crest 325 gold a run, Floodlight Flats
  about 420 ore with a third silicon (2026-11-17).
- The game refills a depleted deposit in proportion to its capacity,
  not to what is left; a full field grows nothing. A floor keeps a stock
  and stops flapping, nothing more (iron 20,000 on 100,000).
- Order each list's fields differently so the division is spread; iron
  comes with copper on every field we read.

### Tests beyond the border (kind `mine`, one good sold)
Status: proven. Updated: 2026-11-21. Evidence: rule F3; table met; fill.py.

- A route maker's test or one of mine: one ship with
  `requires.empty_hold` until its first RESULT line (rule F3). Read the
  pilots met at the place before a lift (table `met`): BUSY combat
  drones fought at Ironhollow and Gliese 876 (2026-11-16). A test of a
  reserve good stores, never sells (rule F24).

### Fits by hand
Status: retired. Updated: 2026-11-21. Evidence: migrated from guidebook/mining.md section 1.

- `refit.py` of the mining-chains skill swaps a module at a station.
  When the engine's goal answers 409 ("another request ... is already
  being processed") for minutes, the raw market `buy` takes the best ask
  at once: read the ask first (2026-11-16 23:16 UTC, one Mining Laser I
  at 1,600 cr plus 1% at Central Nexus).

### Route Templates
Status: proven. Updated: 2026-11-21. Evidence: game/routes/templates/mining.json; plan.py templates.

A kind of work is a named list of routes in
`game/routes/templates/mining.json` (page
`game/routes/templates-mining.md`); a ship's row names it as `@<name>`.

| Template | For | Trains |
|---|---|---|
| `ice-sell` | stored null matter, methane and ice sold where a bid stands, then the water-ice mine routes on a deep order | Mining, Piloting, Trading |
| `reserve-prism` | make, then gather what the reserve lacks: a loaded hold stored, steel plate of the pilot's own iron, then gold, silicon, nickel, carbon | Mining, Crafting, Refining |
| `reserve-hamal` | the same, the short-ore fields in the other order | the same |

Change one: `plan.py template <name> <routes> --title --trains --note`;
put ships on one: `plan.py set <ships> @ice-sell,@reserve-prism`. A
one-ship test stands in front of a ship's templates as a route of its
own. No list of routes that did not pay (rule F22): ask
`route_earnings`.

### Missions That Pay Once
Status: retired. Updated: 2026-11-21. Evidence: migrated from guidebook/mining.md section 3.

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

# Logistics guidebook -- Topic: station (topic-station.md)

### The Stations' List (orders.log ENT-017 and ENT-020, P4)
Status: proven. Updated: 2026-11-21. Evidence: base_plan kind=station and the storage book, 2026-11-16 18:26 to 19:07 UTC; Intel's search (ENT-017); the catalog's recipes (19:20 UTC).

One station takes a fee of 5,000,000 cr, one station core and the foundry that makes it (38,000,000 cr); two stations take the list twice. Input by input, held, missing and where found: the tool base_plan, kind=station (hive.py base station).

- The reading of 2026-11-16: 28 of 30 inputs short (copper ore and energy crystal held); 18 with a field or an offer in our readings, 2 from Military's hunts (creature carapace, verdigris curd), 10 with none: salvage metal, anchor plate, alloy scale, foil scale, graphene thread, silica lens, irradiated marrow, thorium ore, cobalt ink, hoarfrost heartcore.
- The largest lines: iron ore 491,400, salvage metal 249,600, carbon ore 97,008, anchor plate 93,690, alloy scale 56,520, silicon ore 52,808.
- Steel makes the iron line: 49,140 plate by `basic_iron_smelting` (10 iron a plate). Cheaper in iron: `refine_steel` in a facility (2.5 iron a plate: 122,850 iron, 24,570 runs, about 233,000 to 467,000 cr of fees), or by hand `sinter_tungsten_steel` (4 iron, 2 tungsten for 3) and `forge_vanadium_steel` (4 iron, 2 vanadium for 3). Which way is not decided.
- Copper piping (26,120) by `draw_copper_piping` (12 copper, 2 plate for 4) takes 78,360 copper and 13,060 plate more, in place of 34,832 verdigris curd; made by hand 2026-11-17 00:14 UTC.

### One station's steps, by hand or in a facility
Status: proven. Updated: 2026-11-21. Evidence: the tool base_plan kind=station and the catalog's recipes, 2026-11-17 00:00 to 00:21 UTC.

| Step | Recipe | Today |
|---|---|---|
| steel plate, copper piping, copper wiring | `basic_iron_smelting`, `draw_copper_piping`, `basic_copper_processing` by hand | yes |
| armor plate, liquid nitrogen | `carapace_plating`, `nitrogen_bladder_decanting` by hand | in part: carapace and bladders short |
| circuit board | four hand recipes | in part: silicon or gold |
| gold wiring, processing core, power battery | `draw_gold_wire`, `assemble_gold_processing_core`, `assemble_power_battery` by hand | not yet: gold, lithium and cobalt asked at Ironlight Crossroads |
| silicate composite | `sinter_silicate_composite` (4 silicon a unit) | no |
| hull plating | `reforge_hull_plating` from wreck salvage | no |
| titanium alloy, durasteel plate, aluminum sheet, graphene sheet, control node, power cell | by hand from creature parts (magnet-barnacle, cauldronback, mirror-skate, inkwyrm, silica-borer, geiger-hound) | no: none read in our herds |
| docking ring, reinforced bulkhead and frame, quantum control core, quantum dot matrix, the reactors, the core | a facility only (four types each) | no: whether a public facility of ours runs them is not read |

So the station waits first on creature parts and wreck salvage: the search is Intel's, the hunt Military's.

### The Faction's Plates and Boards (orders.log ENT-017 and ENT-020, P5)
Status: proven. Updated: 2026-11-21. Evidence: logs of the turn 2026-11-16 18:59 to 19:08 UTC; storage views 2026-11-16 to 17; requests.log ENT-197.

Plates and boards are the faction buildings' goods; who builds is the Fleet Admiral's, and the goods reach the builder by a deposit to that pilot (lessons.md).

- Steel plate by `basic_iron_smelting` at the Node Beta workshop (0.27 ticks a run, 0 cr, no skill asked): 275 plate from 2,750 iron in about 6 minutes, three haulers in parallel, about 25 plates a minute each (2026-11-16). 145 runs took one hauler's crafting and refining from 0 to 1 (about 110 XP each). Each hauler was taken at the end of its run (catch.py, craftchain.py).
- A station's 49,140 plate: 491,400 iron and about 33 hours of one docked hauler at that pace; refine_steel takes a quarter of the ore.
- Given: 200 steel plate and 50 boards into the Fleet Admiral's flagship at Node Beta, 2026-11-17 04:07 to 04:11 UTC (stage.py: `withdraw` to the hold, `deposit` with the flagship as target, source cargo; 0 cr; ENT-197).
- Where they went since: the Lockbox, the Hiring Board and the Recruitment Desk (topic-bases.md). The Recruitment Center takes 500 boards and 1,000 plate.

### Circuit boards: four hand recipes and the ways to them
Status: proven. Updated: 2026-11-21. Evidence: catalog 0.719.3; stage.py 2026-11-17 01:44 to 02:01 UTC; craft-boards RESULT lines 2026-11-17 04:47 to 12:10 UTC; books 2026-11-16 23:30 to 2026-11-17 07:55 UTC; admirals.log ENT-003, ENT-004; requests.log ENT-220.

| Recipe | Inputs | Boards | Ticks a run |
|---|---|---|---|
| `carbon_arc_circuit_etching` | 2 silicon ore, 12 carbon ore | 3 | 6 |
| `fabricate_circuit_boards` | 3 copper, 2 silicon, 1 energy crystal | 2 | 6 |
| `fabricate_gold_circuit_boards` | 3 copper, 3 gold, 1 energy crystal | 2 | 9 |
| `reclaim_circuit_boards` | 3 rare salvage, 5 salvage components | 1 | 3 |

- Routes: `craft-boards-node-beta` (45 boards a run from 30 silicon, carbon bought at 4 cr), `craft-boards-silicon-central-nexus` (65 boards; its route_earnings figure was the outpost's gifts landing in the wallet, not earnings, ENT-220), `craft-boards-gold-experiment` (30 runs from Mining's gold and crystal at The Experiment).
- 16 etchings made 48 boards at Node Beta from 192 carbon bought at 4 cr (787 cr).
- Silicon has no field in the 66 systems Intel read (ENT-003); the one deep ask, Central Nexus at 420 cr, is Trade's claim (ENT-004). A board costs about 280 cr of silicon by etching, 207 to 213 cr of gold at 138 to 142 cr (Ironlight Crossroads), 301 cr bought there, 515 to 743 cr bought at our books.

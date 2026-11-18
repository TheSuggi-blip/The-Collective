# Logistics guidebook -- Topic: station (topic-station.md)

### The Stations' List (orders.log ENT-017 and ENT-020, P4)
Status: proven. Updated: 2026-11-17. Evidence: migrated from guidebook/logistics.md section 13.

One station takes a fee of 5,000,000 cr, one station core and the foundry that
makes it (38,000,000 cr); two stations take the list twice. Read 2026-11-16 18:26
UTC (the tool base_plan with kind=station) against the storage book of 18:37 UTC
(`data/stock/storage.json`, summed per station). Units are for one station.

| Input | Needed | Held | Where it lies (units) | Missing | Known source |
|---|---|---|---|---|---|
| iron ore | 491,400 | 107,707 | Node Beta 75,679, Synchrony Hub 22,254, Central Nexus 9,296 | 383,693 | fields of 100,000 at Nightveil and Marfik; 24,442 asked at 1 cr at Central Nexus |
| salvage metal | 249,600 | 0 | -- | 249,600 | none read |
| carbon ore | 97,008 | 2,133 | Central Nexus 1,864, Node Beta 148 | 94,875 | Gliese 876 belt (2,901 left), Furud belt (612); 44,531 asked at 4 cr at Nova Terra Central |
| anchor plate | 93,690 | 0 | -- | 93,690 | none read |
| alloy scale | 56,520 | 0 | -- | 56,520 | none read |
| silicon ore | 52,808 | 34 | Central Nexus 34 | 52,774 | 424 asked at 420 cr at Central Nexus (book of 19:07 UTC); 1 to 4 units at 312 to 376 cr elsewhere |
| salvage components | 41,600 | 0 | -- | 41,600 | 546 asked at 87 cr at Node Alpha |
| foil scale | 41,220 | 0 | -- | 41,220 | none read |
| creature carapace | 35,640 | 904 | Node Beta 365, Central Nexus 312, The Experiment 157 | 34,736 | Military's hunts |
| verdigris curd | 34,832 | 37 | Node Beta 21 | 34,795 | Military's hunts |
| ferrous nodule | 28,260 | 0 | -- | 28,260 | 636 asked at 60 cr at Synchrony Hub |
| nickel ore | 18,320 | 514 | Node Gamma 290, Central Nexus 224 | 17,806 | 2,669 asked at 100 cr at Central Nexus |
| gold ore | 16,740 | 0 | -- | 16,740 | Gold Crest (764 left), Rastaban belt (589) |
| graphene thread | 13,260 | 0 | -- | 13,260 | none read |
| silica lens | 10,440 | 0 | -- | 10,440 | none read |
| crystallized biogas | 4,420 | 118 | Central Nexus 48 | 4,302 | 7 asked at 165 cr in LHS 1140 |
| irradiated marrow | 4,000 | 0 | -- | 4,000 | none read |
| quantum fragments | 3,720 | 0 | -- | 3,720 | 24 asked at 600 cr at Node Beta |
| platinum ore | 3,720 | 799 | Central Nexus 503, Node Gamma 225 | 2,921 | 29 asked at 250 cr at Central Nexus |
| uranium ore | 2,304 | 0 | -- | 2,304 | Acubens belt (1 left) |
| thorium ore | 1,200 | 0 | -- | 1,200 | none read |
| copper ore | 768 | 75,869 | Node Beta 49,796, Synchrony Hub 19,253 | 0 | held |
| fluorine gas | 384 | 0 | -- | 384 | 192,627 asked at 36 cr in LHS 1140 |
| nitrogen bladder | 192 | 45 | Central Nexus 33 | 147 | 6 asked at 27 cr at Nova Terra Central |
| cobalt ink | 192 | 0 | -- | 192 | none read |
| lithium ore | 120 | 1 | Central Nexus 1 | 119 | Stormwatch belt (25,000), Acrux belt (12,182) |
| cobalt ore | 80 | 0 | -- | 80 | 200 asked at 140 cr in LHS 1140 |
| energy crystal | 80 | 528 | Node Beta 408, Central Nexus 120 | 0 | held |
| hoarfrost heartcore | 40 | 0 | -- | 40 | none read |
| polonium ore | 20 | 0 | -- | 20 | 200 asked at 1,000 cr in LHS 1140 |

So: 28 of 30 inputs are short; 18 have a field or an offer in our readings, 2 more
come from Military's hunts, and 10 have none: salvage metal, anchor plate, alloy
scale, foil scale, graphene thread, silica lens, irradiated marrow, thorium ore,
cobalt ink and hoarfrost heartcore (Intel's search, orders ENT-017).

Steel is the largest made step: 49,140 plate by `basic_iron_smelting` (10 iron ore
a plate) is what makes the iron line 491,400. The catalog names cheaper ways in
iron (`catalog`, item steel_plate): `refine_steel` in a facility, 5 iron ore for 2
plate (2.5 a plate; a public facility quoted 19 cr on 2026-11-15, section 7, and
that quote does not say whether for one run or two), and by hand
`sinter_tungsten_steel` (4 iron, 2 tungsten for 3 plate) or `forge_vanadium_steel`
(4 iron, 2 vanadium for 3). By refine_steel the iron line would be 122,850 units
and 24,570 runs, about 233,000 to 467,000 cr of fees; the fleet holds 107,707 iron
ore today. Which way the stations' steel goes is not decided; the hand recipe asks
no facility and no fee.

Copper piping (26,120 for one station) is reckoned above from verdigris curd
(`verdigris_smelting`, 4 curd for 3 piping), which the fleet barely holds (37 of
34,832). The catalog lists a second hand recipe, `draw_copper_piping`: 12 copper ore
and 2 steel plate make 4 copper piping (`catalog`, recipes that make copper_piping,
2026-11-16 19:20 UTC). By it the piping takes 78,360 copper ore, about what the
fleet stores today (75,869), and 13,060 steel plate more (130,600 iron ore), and
the curd line falls away. Not quoted or made yet: the next step to test.

What one station's steps take, by hand or in a facility, against what we hold (the tool
base_plan with kind=station and the catalog's recipes, 2026-11-17 00:00 to 00:21 UTC):

| Step | Recipe | Today | Why |
|---|---|---|---|
| steel plate | `basic_iron_smelting` by hand | yes | 219,328 iron ore held of 491,400, 21,932 plates by hand; about 25 plates a minute at the workshop (section 14) |
| copper piping | `draw_copper_piping` by hand | yes, tested | 12 copper and 2 plate for 4 piping (2026-11-17 00:14 UTC); copper held 144,122 |
| copper wiring | `basic_copper_processing` by hand | yes | copper held |
| armor plate | `carapace_plating` by hand | in part | 1,164 carapace, 194 plates of 5,940 |
| liquid nitrogen | `nitrogen_bladder_decanting` by hand | in part | 49 bladders, 48 of 192 |
| circuit board | four hand recipes | in part | silicon 32 held (no field read), or gold bought beyond the border (section 1.5) |
| gold wiring, processing core | `draw_gold_wire`, `assemble_gold_processing_core` by hand | not yet | gold ore: none held; fields at Gold Crest and Rastaban, an ask at Ironlight Crossroads |
| power battery | `assemble_power_battery` by hand | not yet | 3 lithium and 2 cobalt ore each: lithium asked at 14 cr and cobalt at 140 cr at Ironlight Crossroads |
| silicate composite | `sinter_silicate_composite` by hand | no | 4 silicon a unit, 36,640 silicon for 9,160 |
| hull plating | `reforge_hull_plating` by hand | no | salvage metal and salvage components come from wrecks (the catalog's text); none held |
| titanium alloy, durasteel plate, aluminum sheet, graphene sheet, control node, power cell | by hand from creature parts | no | anchor plate (magnet-barnacle), alloy scale (cauldronback), foil scale (mirror-skate), graphene thread (inkwyrm), silica lens (silica-borer), irradiated marrow (geiger-hound): the catalog names each creature; none read in our herds |
| docking ring, reinforced bulkhead, reinforced frame, quantum control core, quantum dot matrix, the reactors, the core | a facility only | no | four facility types each; whether a public facility at our stations runs them is not read |

So the station waits first on creature parts and wreck salvage, which no field and no
book of ours holds: the search for those creatures is Intel's and the hunt Military's.
Steel is the step that eats iron: `refine_steel` in a facility takes 5 iron for 2 plates
against 10 for 1 by hand; its fee per run is not read yet (planned).

### The Faction's Plates and Boards (orders.log ENT-017 and ENT-020, P5)
Status: proven. Updated: 2026-11-17. Evidence: migrated from guidebook/logistics.md section 14.

The lockbox and the hiring board take 275 steel plate and 75 circuit boards
(orders ENT-017). Who builds them and where is the Fleet Admiral's; the goods move
to the builder by a deposit to that pilot (section 7).

Steel plate, made 2026-11-16 18:59 to 19:05 UTC at the Node Beta workshop by
`basic_iron_smelting` (10 iron ore, 1 plate, 0.27 ticks a run, 0 cr), from the iron
ore the gather routes put into hauler storage there (catch.py and craftchain.py of
the skill logistics-stock, logs of the turn):

| Batch | Plates | Minutes of crafting | Credits | Skill |
|---|---|---|---|---|
| one hauler, 1,450 iron ore | 145 | 5.7 | 0 | crafting 0 (25 XP) to 1 (75 XP), refining 0 (15 XP) to 1 (65 XP): about 110 XP each for 145 runs |
| one hauler, 1,170 iron ore | 117 | 5.2 | 0 | not read |
| one hauler, 130 iron ore | 13 | 0.7 | 0 | not read |

So 275 plate took 2,750 iron ore, 0 cr and about 6 minutes of workshop time with
three haulers in parallel, about 25 plates a minute a hauler; no skill is asked.
The two smaller batches went by deposit into the first hauler's storage (117 and 13
plates, three loads of 57 at most). All 275 lie in one Logistics storage at Node
Beta (`view` of that storage, 19:08 UTC). What the hand took besides: each hauler
was taken at the end of its gather run, where its minutes ran out (at the field),
and flown to Node Beta, 3.5 to 5 minutes; those hops are the ones its gather run
flies anyway.

For the stations' 49,140 plate the same recipe takes 491,400 iron ore and, at
about 25 plates a minute, about 33 hours of one docked hauler's workshop time;
`refine_steel` in a facility takes a quarter of the ore (section 13).

Circuit boards, 2026-11-17 00:45 UTC: 1 held. Mining gave 16 silicon ore and 17 carbon ore
into the crafting hauler's storage at Central Nexus (requests.log ENT-175), which then held
32 silicon and 36 carbon (the game's storage view, 2026-11-16 23:53 UTC). Four hand recipes
make boards (catalog 0.719.3):

| Recipe | Inputs | Boards | Ticks a run |
|---|---|---|---|
| `carbon_arc_circuit_etching` | 2 silicon ore, 12 carbon ore | 3 | 6 |
| `fabricate_circuit_boards` | 3 copper ore, 2 silicon ore, 1 energy crystal | 2 | 6 |
| `fabricate_gold_circuit_boards` | 3 copper ore, 3 gold ore, 1 energy crystal | 2 | 9 |
| `reclaim_circuit_boards` | 3 rare salvage, 5 salvage components | 1 | 3 |

Made and given, 2026-11-17: 16 etchings, 48 boards, at the Node Beta workshop from 01:44 to
02:01 UTC (stage.py; 192 carbon ore bought there at 4 cr, 787 cr); 200 steel plate and 50
circuit boards given to the Fleet Admiral's flagship at Node Beta from 04:07 to 04:11 UTC by
script (catch.py and stage.py: `withdraw` to the hold, then `deposit` with the flagship as
`target` and `source` cargo; HTTP 200, 0 cr, the giver's hold lighter by each load; requests.log
ENT-197). Next: `craft-boards-node-beta`, 45 boards a run (section 1.2), from the 32 silicon
at Node Beta; 43 more silicon lie at Central Nexus.

Before (kept for the record): the crafting hauler was taken at the end of its run (about 01:23 UTC) by
`catch.py`, carries its silicon, carbon and board to Node Beta, buys carbon there at 4 cr up
to 192 in storage, etches 16 runs (48 boards) and gives every board into the storage that
holds the faction's steel plate (`stage.py` of the skill logistics-stock). Its log is read
next turn. With the board held, 49 of 75.

The other 26: silicon has no field in the 66 systems Intel read (admirals.log ENT-003); the
one deep ask, Central Nexus at 420 cr for 425 units (book of 2026-11-16 23:49 UTC), is
Trade's claim (admirals.log ENT-004), and 18 units are asked of Trade (requests.log
ENT-179). Gold needs no silicon: Ironlight Crossroads asked gold ore at 138 cr, and the
test `buy-gold-ironlight-boards` makes 2 boards from 3 of it (section 1.5). A board costs
about 280 cr of silicon at 420 cr by etching, about 207 cr of gold at 138 cr, and 515 to
743 cr bought whole at the asks of our books (2026-11-16 23:30 to 23:49 UTC).

Boards, 2026-11-17 08:10 UTC (storage book of 07:25 to 07:32 UTC): 51 held by Logistics (45 and 1 at
Node Beta, 5 at Central Nexus); 50 go to the Lockbox at The Experiment (section 15.2), 1 stays. The
Hiring Board and the Recruitment Desk take 125: `craft-boards-silicon-central-nexus` makes 65 from the
builder's 43 silicon ore, which leaves about 59. Ways to them, each per board: Ironlight Crossroads asks
boards at 301 cr for 74 (book of 07:55 UTC), the cheapest ask read; gold ore asked there at 142 cr makes
a board for 213 cr of gold and half an energy crystal (asked at 420 cr at Central Nexus); Mining stores
135 gold ore at The Experiment and the command group and Intel 671 energy crystal at Node Beta, which
make 90 boards for no new credits if the Fleet Admiral allocates them (rule F31; requests.log).

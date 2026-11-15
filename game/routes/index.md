---
name: routes-index
id: 20261115T153923Z
tier: intel
author: Unity
---

# index.md -- Routes We Fly

Written by `python3 -B game/fleet/routes.py index`, never by hand. A route is a
task one pilot carries out by itself; its file is `game/routes/<id>.json`
(`BLUEPRINT.md`). The figures are what our own runs measured.

| Route | Kind | What it is | Open to | Runs | Minutes per run | Credits per run | Credits per ship-hour | Measured |
|---|---|---|---|---|---|---|---|---|
| [census-frontier](census-frontier.json) | census | Read one lawless system around our space whole: deposits, creatures, stations, order books, mission boards | up to 12 ships | 35 | 14 | -140 | -600 | 2026-11-15 |
| [census-voidborn](census-voidborn.json) | census | Read one Voidborn system whole: deposits, creatures, order book, mission board | up to 3 ships | 93 | 8 | -70 | -550 | 2026-11-15 |
| [first-survey](first-survey.json) | circuit | Signal Propagation Survey: dock at the five other Voidborn stations (20,000 cr) | once per pilot, off | TBD | TBD | TBD | TBD | -- |
| [fit-ice-harvester](fit-ice-harvester.json) | circuit | Fit an Ice Harvester I at Node Alpha: the tool every ice field needs | once per pilot, up to 1 ships | TBD | TBD | TBD | TBD | -- |
| [fit-ice-harvester-guard](fit-ice-harvester-guard.json) | circuit | Fit an Ice Harvester I at Central Nexus: the tool every ice field needs | once per pilot, up to 2 ships | TBD | TBD | TBD | TBD | -- |
| [park](park.json) | circuit | Dock at Central Nexus and wait there: a docked ship costs nothing | the park route | TBD | TBD | TBD | TBD | -- |
| [trade-ceramite-plating-the-central](trade-ceramite-plating-the-central.json) | circuit | Ceramite Plating: bought at The Experiment Research Station for 899 cr, sold at The Core for 1185 cr | up to 1 ships | TBD | TBD | TBD | TBD | -- |
| [trade-voidborn-neural-soma-central-the](trade-voidborn-neural-soma-central-the.json) | circuit | Voidborn Neural Soma: bought at The Core for 258 cr, sold at The Experiment Research Station for 690 cr | up to 1 ships | TBD | TBD | TBD | TBD | -- |
| [voidborn-concurrent](voidborn-concurrent.json) | circuit | Concurrent Approval: accept at Central Nexus, deliver two neural soma to Node Beta (3,000 cr once) | once per pilot | TBD | TBD | TBD | TBD | -- |
| [voidborn-first-hunt-acubens](voidborn-first-hunt-acubens.json) | circuit | First Hunt: Belt-Grazers: 1,000 cr once and 50 Weapons XP; three belt-grazers at Acubens Shadow Pocket | once per pilot, up to 1 ships | TBD | TBD | TBD | TBD | -- |
| [voidborn-first-hunt-gsc](voidborn-first-hunt-gsc.json) | circuit | First Hunt: Belt-Grazers: 1,000 cr once and 50 Weapons XP; three belt-grazers at Spacetime Seep | once per pilot, up to 1 ships | TBD | TBD | TBD | TBD | -- |
| [voidborn-first-hunt-nexus](voidborn-first-hunt-nexus.json) | circuit | First Hunt: Belt-Grazers: 1,000 cr once and 50 Weapons XP; three belt-grazers at Material Harvesters | once per pilot, up to 1 ships | TBD | TBD | TBD | TBD | -- |
| [voidborn-first-steps](voidborn-first-steps.json) | circuit | First Steps in the Void for a pilot that holds it: mine 15 carbon ore at Acubens Belt, hand in at Central Nexus | once per pilot, up to 2 ships, off | TBD | TBD | TBD | TBD | -- |
| [voidborn-mining-missions](voidborn-mining-missions.json) | circuit | Iron Supply Run and Copper Requisition: accept at Central Nexus, mine at Acubens by way of Node Beta, hand in at Central Nexus | once per pilot, up to 40 ships | TBD | TBD | TBD | TBD | -- |
| [voidborn-missions-1](voidborn-missions-1.json) | circuit | Synchrony Relay Run and Crystal Delivery: two board missions in one circuit of 8 jumps | once per pilot | 146 | 22 | 6,430 | one-time | 2026-11-15 |
| [voidborn-precedence](voidborn-precedence.json) | circuit | Precedence: 4,000 cr once, a round of three of our stations | once per pilot, up to 40 ships | 1 | 15 | 3,900 | one-time | 2026-11-15 |
| [voidborn-selling](voidborn-selling.json) | circuit | Market Participation: Selling: 1,000 cr once; ten liquid nitrogen bought and sold at The Experiment | once per pilot, up to 10 ships | 12 | 5 | 870 | one-time | 2026-11-15 |
| [voidborn-substrate](voidborn-substrate.json) | circuit | Substrate Delivery: two neural soma bought at Central Nexus, the mission taken at Node Alpha and handed in at Central Nexus; 2 jumps | once per pilot | 146 | 8 | 1,790 | one-time | 2026-11-15 |
| [hunt-acubens-urchin](hunt-acubens-urchin.json) | hunt | Cinder-urchins at Acubens Shadow Pocket; radiant bile sold at Node Gamma | up to 1 ships, off | 2 | 25 | -120 | -290 | 2026-11-15 |
| [hunt-cedarhold-dim-lattice-veil-ray](hunt-cedarhold-dim-lattice-veil-ray.json) | hunt | veil_ray at cedarhold_dim_lattice; loot sold at The Experiment Research Station | up to 1 ships | TBD | TBD | TBD | TBD | -- |
| [hunt-faintlight-drift-veil-ray](hunt-faintlight-drift-veil-ray.json) | hunt | veil_ray at faintlight_drift; loot sold at Node Beta Industrial Station | up to 1 ships | TBD | TBD | TBD | TBD | -- |
| [hunt-garnet-dim-lattice-veil-ray](hunt-garnet-dim-lattice-veil-ray.json) | hunt | veil_ray at garnet_dim_lattice; loot sold at The Experiment Research Station | up to 1 ships | TBD | TBD | TBD | TBD | -- |
| [hunt-gsc-veil-ray](hunt-gsc-veil-ray.json) | hunt | Veil-rays at GSC-0027 Prism Scatter; verdigris curd sold at Central Nexus | up to 1 ships | 7 | 24 | 1,830 | 3,350 | 2026-11-15 |
| [hunt-hamal-veil-ray](hunt-hamal-veil-ray.json) | hunt | Veil-rays at Hamal Crystal Bloom; verdigris curd sold at Central Nexus | up to 1 ships | 5 | 23 | 1,070 | 3,120 | 2026-11-15 |
| [hunt-home-drift-ray](hunt-home-drift-ray.json) | hunt | Drift-rays at Stellar Siphon in Nexus Prime; goods sold or stored at Central Nexus | up to 1 ships | 8 | 10 | -40 | -250 | 2026-11-15 |
| [hunt-home-whale](hunt-home-whale.json) | hunt | Pilot-whales at Stellar Siphon in Nexus Prime; whale oil sold at Node Beta | up to 1 ships, needs piercing_railgun_i, off | 1 | 20 | 570 | 1,670 | 2026-11-15 |
| [hunt-keid-fractured-prism-veil-ray](hunt-keid-fractured-prism-veil-ray.json) | hunt | veil_ray at keid_fractured_prism; loot sold at Node Beta Industrial Station | up to 1 ships | TBD | TBD | TBD | TBD | -- |
| [hunt-low-charge-glint-veil-ray](hunt-low-charge-glint-veil-ray.json) | hunt | veil_ray at low_charge_glint; loot sold at Node Beta Industrial Station | up to 1 ships | TBD | TBD | TBD | TBD | -- |
| [hunt-ruchbah-veil-ray](hunt-ruchbah-veil-ray.json) | hunt | Veil-rays at Ruchbah Broken Glass Veil (lawless); verdigris curd sold at The Experiment | up to 1 ships | TBD | TBD | TBD | TBD | -- |
| [hunt-test-acubens-patina-grazer](hunt-test-acubens-patina-grazer.json) | hunt | Yield test: patina_grazer at acubens_shadow_pocket; what a kill drops and whether a bid takes it | up to 1 ships | TBD | TBD | TBD | TBD | -- |
| [hunt-test-eltanin-kiln-snail](hunt-test-eltanin-kiln-snail.json) | hunt | Yield test: kiln_snail at eltanin_prime_belt; what a kill drops and whether a bid takes it | up to 1 ships | TBD | TBD | TBD | TBD | -- |
| [hunt-test-frozen-drift-deuteron-slug](hunt-test-frozen-drift-deuteron-slug.json) | hunt | Yield test: deuteron_slug at node_beta_frozen_drift; what a kill drops and whether a bid takes it | up to 1 ships | TBD | TBD | TBD | TBD | -- |
| [hunt-test-node-gamma-ice-belt](hunt-test-node-gamma-ice-belt.json) | hunt | Yield test: rime_grazer, pressblister at node_gamma_ice_belt; what a kill drops and whether a bid takes it | up to 1 ships | TBD | TBD | TBD | TBD | -- |
| [hunt-test-siphon-bell-jelly](hunt-test-siphon-bell-jelly.json) | hunt | Yield test: bell_jelly at stellar_siphon; what a kill drops and whether a bid takes it | up to 1 ships, off | TBD | TBD | TBD | TBD | -- |
| [mine-achernar-frost-ring](mine-achernar-frost-ring.json) | mine | Achernar Frost Ring: water_ice, nitrogen_ice, deuterium_ice, methane_ice; sold at The Experiment Research Station | up to 1 ships, needs ice_harvester_i | TBD | TBD | TBD | TBD | -- |
| [mine-acubens](mine-acubens.json) | mine | Iron and copper at Acubens Shadow Pocket; ore into storage at Node Beta | up to 16 ships | 48 | 45 | -120 | -160 | 2026-11-15 |
| [mine-alnair-ice-fields](mine-alnair-ice-fields.json) | mine | Alnair Ice Fields: water_ice, nitrogen_ice, deuterium_ice; sold at Node Alpha Processing Station | up to 1 ships, needs ice_harvester_i | TBD | TBD | TBD | TBD | -- |
| [mine-antares-ice-fields](mine-antares-ice-fields.json) | mine | Antares Ice Fields: water_ice, nitrogen_ice, deuterium_ice, helium_ice; sold at Node Alpha Processing Station | up to 1 ships, needs ice_harvester_i | TBD | TBD | TBD | TBD | -- |
| [mine-bellatrix](mine-bellatrix.json) | mine | Wait at Bellatrix Major Belt beside Node Gamma station for whatever regrows (thorium, palladium, iridium, carbon) | up to 1 ships | 8 | 45 | 0 | 0 | 2026-11-15 |
| [mine-cryogenic-reserve](mine-cryogenic-reserve.json) | mine | Cryogenic Reserve: water_ice, nitrogen_ice, oxygen_ice; sold at Synchrony Hub | up to 1 ships, needs ice_harvester_i | TBD | TBD | TBD | TBD | -- |
| [mine-gsc-0041-frost-ring](mine-gsc-0041-frost-ring.json) | mine | GSC-0041 Frost Ring: water_ice, nitrogen_ice, deuterium_ice; sold at Node Alpha Processing Station | up to 1 ships, needs ice_harvester_i | TBD | TBD | TBD | TBD | -- |
| [mine-gsc-seep](mine-gsc-seep.json) | mine | Iron and copper at GSC-0027 Spacetime Seep; ore into storage at Node Beta | up to 16 ships | 48 | 45 | -120 | -160 | 2026-11-15 |
| [mine-intercrus-ice-fields](mine-intercrus-ice-fields.json) | mine | Intercrus Ice Fields: water_ice, nitrogen_ice; sold at The Experiment Research Station | up to 1 ships, needs ice_harvester_i | TBD | TBD | TBD | TBD | -- |
| [mine-keid-ice-shelf](mine-keid-ice-shelf.json) | mine | Keid Ice Shelf: water_ice, deuterium_ice; sold at Node Alpha Processing Station | up to 1 ships, needs ice_harvester_i | TBD | TBD | TBD | TBD | -- |
| [mine-node-beta-frozen-drift](mine-node-beta-frozen-drift.json) | mine | Node Beta Frozen Drift: water_ice, nitrogen_ice, deuterium_ice; sold at Node Alpha Processing Station | up to 1 ships, needs ice_harvester_i | TBD | TBD | TBD | TBD | -- |
| [mine-pherkad-rift](mine-pherkad-rift.json) | mine | Copper and iron at Pherkad Null Rift; ore into storage at Synchrony Hub | every pilot | 65 | 45 | -120 | -160 | 2026-11-15 |
| [mine-ruchbah-ice-belt](mine-ruchbah-ice-belt.json) | mine | Ruchbah Ice Belt: water_ice, nitrogen_ice, deuterium_ice, methane_ice; sold at The Experiment Research Station | up to 1 ships, needs ice_harvester_i | TBD | TBD | TBD | TBD | -- |
| [mine-wolf-1061-frozen-drift](mine-wolf-1061-frozen-drift.json) | mine | Wolf 1061 Frozen Drift: water_ice, nitrogen_ice, deuterium_ice, methane_ice; sold at Node Alpha Processing Station | up to 1 ships, needs ice_harvester_i | TBD | TBD | TBD | TBD | -- |
| [mine-wolf-1061-vent](mine-wolf-1061-vent.json) | mine | Wolf 1061 Frozen Drift with a Nitrogen Vent: water and the rare ices, sold at Synchrony | up to 1 ships, needs nitrogen_vent | TBD | TBD | TBD | TBD | -- |

## The Plans

`plans/<role>.json`: per role, the routes the dispatcher tries in this order for a free pilot. The role's Admiral keeps the file.

| Role | Kept by | Routes, first that is open |
|---|---|---|
| command | Unity | voidborn-concurrent > voidborn-substrate > voidborn-missions-1 > voidborn-mining-missions > voidborn-first-steps > voidborn-selling > voidborn-precedence > voidborn-first-hunt-nexus > voidborn-first-hunt-gsc > voidborn-first-hunt-acubens > mine-node-beta-frozen-drift > mine-ruchbah-ice-belt > mine-achernar-frost-ring > mine-wolf-1061-frozen-drift > mine-keid-ice-shelf > mine-cryogenic-reserve > mine-alnair-ice-fields > mine-gsc-0041-frost-ring > mine-antares-ice-fields > mine-intercrus-ice-fields > census-frontier > park |
| drone | Apophis | voidborn-precedence > voidborn-first-hunt-nexus > voidborn-selling > voidborn-concurrent > voidborn-substrate > voidborn-missions-1 > voidborn-mining-missions > hunt-gsc-veil-ray > hunt-hamal-veil-ray > hunt-cedarhold-dim-lattice-veil-ray > hunt-garnet-dim-lattice-veil-ray > hunt-ruchbah-veil-ray > hunt-low-charge-glint-veil-ray > hunt-faintlight-drift-veil-ray > hunt-keid-fractured-prism-veil-ray > hunt-test-acubens-patina-grazer > hunt-test-node-gamma-ice-belt > hunt-test-frozen-drift-deuteron-slug > hunt-test-eltanin-kiln-snail > census-frontier > park |
| hauler | Apollo | voidborn-precedence > voidborn-selling > voidborn-first-hunt-nexus > voidborn-concurrent > voidborn-substrate > voidborn-missions-1 > voidborn-mining-missions > census-frontier > park |
| miner | Zero | voidborn-concurrent > voidborn-substrate > voidborn-missions-1 > voidborn-mining-missions > fit-ice-harvester > mine-wolf-1061-vent > mine-ruchbah-ice-belt > mine-achernar-frost-ring > mine-cryogenic-reserve > mine-keid-ice-shelf > mine-intercrus-ice-fields > mine-wolf-1061-frozen-drift > mine-alnair-ice-fields > mine-node-beta-frozen-drift > mine-gsc-0041-frost-ring > mine-antares-ice-fields > census-frontier > park |
| scout | Oracle | census-voidborn > voidborn-precedence > voidborn-selling > voidborn-first-hunt-nexus > voidborn-first-hunt-gsc > voidborn-first-hunt-acubens > voidborn-concurrent > voidborn-substrate > voidborn-missions-1 > voidborn-mining-missions > census-frontier > park |
| sentinel | Unity | voidborn-concurrent > voidborn-substrate > voidborn-missions-1 > voidborn-mining-missions > voidborn-first-steps > voidborn-selling > voidborn-precedence > voidborn-first-hunt-nexus > voidborn-first-hunt-gsc > voidborn-first-hunt-acubens > fit-ice-harvester-guard > mine-node-beta-frozen-drift > mine-ruchbah-ice-belt > mine-achernar-frost-ring > mine-wolf-1061-frozen-drift > mine-keid-ice-shelf > mine-cryogenic-reserve > mine-alnair-ice-fields > mine-gsc-0041-frost-ring > mine-antares-ice-fields > mine-intercrus-ice-fields > census-frontier > park |
| trader | Mercury | voidborn-concurrent > voidborn-substrate > voidborn-missions-1 > voidborn-mining-missions > voidborn-precedence > census-frontier > park |

## Planned

What an Admiral means to do next (`planned` in its plan file), so that the others can plan around it.

| Role | What | When |
|---|---|---|
| drone | First Hunt: Belt-Grazers for every drone: voidborn-first-hunt-nexus is at the head since 2026-11-15 23:40 UTC; -gsc and -acubens join it when the command group's first RESULT lines on them are read. | turn T7, or T8 at the latest |
| drone | Frontier veil-ray tests and yield tests: routes.py measure --write after their first RESULT lines; a test that lost money leaves the plan, a yield whose drop sells becomes a ranched route. | turn T8 |
| drone | The railgun ship: ammunition from stored iron (2 steel plate and 3 iron ore make 5 Ferrous Slug Cases, one case loads a magazine; the craft costs no credits), then a yield test of armoured prey of 100 hull or less, where armour bypass may count. | turn T8 |
| drone | The next hull: commission_quote of the tier-1 Vigil (two weapon slots, hull 75, cargo 20, no Piloting gate named) at a Voidborn shipyard; one ship, two Pulse Laser I, against a home veil-ray herd, measured against the starter's trips. | turn T8, after the quote |
| hauler | A craft-and-sell route for stored ore once the circuit runner has its craft step (requests.log ENT-013), only where the depth at the best bid (best_buy_qty, read live with view_market) pays the fuel | after 2026-11-16 12:00 UTC |
| hauler | Measure how fast station-owned bids refill (iron ore at Central Nexus read 0 at 21:25 UTC after our sale) | turn T6 |
| miner | Read the first RESULT line of every ice route; then routes.py measure --write and lift max_ships where the water-ice depth at the best bid carries more ships (ledger.py prices water_ice, view_market at the station), with max_pilots of fit-ice-harvester beside it | turn T8 |
| miner | Compare the vent route's loads with run 1 at the same field (126 units in 25 minutes, 32% nitrogen ice): a Nitrogen Vent for every ice miner if it raises water and rare ice per minute; one vent was on offer in our six books (2026-11-15 23:30 UTC) | turn T8 |
| miner | Deuterium ice and plasma gas, one test each once the ice routes hold: the deuterium bids are a few units (Node Alpha 208 x 6, Node Beta 226 x 5) and count as one-time prices until data/market/history.jsonl shows them refill (F12); a gas harvester takes the mining laser's slot | turn T8 and T9 |
| miner | One focused crystal from the 20 energy crystals in storage at Node Beta whenever The Experiment's station bid of 1,466 cr stands again (ledger.py prices focused_crystal) | every turn |
| scout | Keep every Voidborn system read within the hour: census-voidborn every_minutes 30, max_ships 3; read the gaps per system every turn and change the threshold only on a measured gap over 60 minutes | every turn |
| scout | census-frontier: 42 systems (rings 1 to 3 of our border, Atlas, Intercrus, LHS 1140, Goldcrest, Bluerift), every 240 minutes, 12 ships. Next ring, once the cost of the ring-3 reads is measured: acrab, acrux, botein, deepwell, felis, gliese_876, hd_147513, marfik, rastaban; not the pirate stronghold gliese_581 | turn T8 |
| scout | Base-site line in the system file of every new read (LHS 1140 and the third ring once the tracker files them): lawless, police, a station already there, places without a base, foreign pilots seen | turn T8 |
| scout | voidborn-precedence and the three voidborn-first-hunt routes at the head of the plan as soon as the command group's first RESULT lines show the reward | turn T7 and T8 |
| scout | Read the game's changelog at every turn and name each line of game/rules/ a release makes wrong in a request to the Fleet Admiral | every turn |
| trader | Control-node craft by hand: one trader, one craft (2 nodes) at Central Nexus, sold at Node Gamma; every call and answer recorded for the runner's craft step (requests.log ENT-030). A route with max_ships 1 only when the craft step exists and the per-level books show depth at both ends. | turn T5, 2026-11-15 |
| trader | Gaps between our six stations from data/market/history.jsonl, read by depth at the best level (best_buy_qty, best_sell_qty), not the total; no trade route until one holds over a day of reads and covers fuel and the 1% tax. | turns T6 to T8 |
| trader | One trader, hold empty, to a frontier station the census-frontier read shows with an order book worth the trip (orders F13): bids for what our stations sell cheap, asks under our bids. Waits for the scouts' first reads. | after the first census-frontier reads |

## The Guidebooks

What each division learned about its routes, its levelling and its ships; kept by its Admiral, read by every member.

| Guidebook | Title |
|---|---|
| [guidebook/intel.md](guidebook/intel.md) | intel.md -- Guidebook of the Intel Division |
| [guidebook/logistics.md](guidebook/logistics.md) | logistics.md -- Guidebook of the Logistics Division |
| [guidebook/military.md](guidebook/military.md) | military.md -- Guidebook of the Military Division |
| [guidebook/mining.md](guidebook/mining.md) | mining.md -- Guidebook of the Mining Division |
| [guidebook/trade.md](guidebook/trade.md) | trade.md -- Guidebook of the Trade Division |

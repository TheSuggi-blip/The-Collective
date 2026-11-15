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
| [census-frontier](census-frontier.json) | census | Read one lawless system around our space whole: deposits, creatures, stations, order books, mission boards | up to 12 ships | TBD | TBD | TBD | TBD | -- |
| [census-voidborn](census-voidborn.json) | census | Read one Voidborn system whole: deposits, creatures, order book, mission board | up to 3 ships | 37 | 7 | -70 | -550 | 2026-11-15 |
| [first-survey](first-survey.json) | circuit | Signal Propagation Survey: dock at the five other Voidborn stations (20,000 cr) | once per pilot, off | TBD | TBD | TBD | TBD | -- |
| [park](park.json) | circuit | Dock at Central Nexus and wait there: a docked ship costs nothing | the park route | TBD | TBD | TBD | TBD | -- |
| [voidborn-concurrent](voidborn-concurrent.json) | circuit | Concurrent Approval: accept at Central Nexus, deliver two neural soma to Node Beta (3,000 cr once) | once per pilot | TBD | TBD | TBD | TBD | -- |
| [voidborn-first-steps](voidborn-first-steps.json) | circuit | First Steps in the Void for a pilot that holds it: mine 15 carbon ore at Acubens Belt, hand in at Central Nexus | once per pilot, up to 2 ships, off | TBD | TBD | TBD | TBD | -- |
| [voidborn-mining-missions](voidborn-mining-missions.json) | circuit | Iron Supply Run and Copper Requisition: accept at Central Nexus, mine at Acubens by way of Node Beta, hand in at Central Nexus | once per pilot, up to 40 ships | TBD | TBD | TBD | TBD | -- |
| [voidborn-missions-1](voidborn-missions-1.json) | circuit | Synchrony Relay Run and Crystal Delivery: two board missions in one circuit of 8 jumps | once per pilot | 146 | 22 | 6,430 | one-time | 2026-11-15 |
| [voidborn-substrate](voidborn-substrate.json) | circuit | Substrate Delivery: two neural soma bought at Central Nexus, the mission taken at Node Alpha and handed in at Central Nexus; 2 jumps | once per pilot | 146 | 8 | 1,790 | one-time | 2026-11-15 |
| [hunt-acubens-urchin](hunt-acubens-urchin.json) | hunt | Cinder-urchins at Acubens Shadow Pocket; radiant bile sold at Node Gamma | up to 1 ships, off | 2 | 25 | -120 | -290 | 2026-11-15 |
| [hunt-gsc-veil-ray](hunt-gsc-veil-ray.json) | hunt | Veil-rays at GSC-0027 Prism Scatter; verdigris curd sold at Central Nexus | up to 1 ships, needs piercing_railgun_i | 7 | 24 | 1,830 | 3,350 | 2026-11-15 |
| [hunt-hamal-veil-ray](hunt-hamal-veil-ray.json) | hunt | Veil-rays at Hamal Crystal Bloom; verdigris curd sold at Central Nexus | up to 1 ships | 5 | 23 | 1,070 | 3,120 | 2026-11-15 |
| [hunt-home-drift-ray](hunt-home-drift-ray.json) | hunt | Drift-rays at Stellar Siphon in Nexus Prime; goods sold or stored at Central Nexus | up to 1 ships | 8 | 10 | -40 | -250 | 2026-11-15 |
| [hunt-home-whale](hunt-home-whale.json) | hunt | Pilot-whales at Stellar Siphon in Nexus Prime; whale oil sold at Node Beta | up to 1 ships, needs piercing_railgun_i, off | 1 | 20 | 570 | 1,670 | 2026-11-15 |
| [hunt-ruchbah-veil-ray](hunt-ruchbah-veil-ray.json) | hunt | Veil-rays at Ruchbah Broken Glass Veil (lawless); verdigris curd sold at The Experiment | up to 1 ships, off | TBD | TBD | TBD | TBD | -- |
| [mine-acubens](mine-acubens.json) | mine | Iron and copper at Acubens Shadow Pocket; ore into storage at Node Beta | up to 16 ships | 48 | 45 | -120 | -160 | 2026-11-15 |
| [mine-bellatrix](mine-bellatrix.json) | mine | Wait at Bellatrix Major Belt beside Node Gamma station for whatever regrows (thorium, palladium, iridium, carbon) | up to 1 ships | 8 | 45 | 0 | 0 | 2026-11-15 |
| [mine-gsc-seep](mine-gsc-seep.json) | mine | Iron and copper at GSC-0027 Spacetime Seep; ore into storage at Node Beta | up to 16 ships | 48 | 45 | -120 | -160 | 2026-11-15 |
| [mine-pherkad-rift](mine-pherkad-rift.json) | mine | Copper and iron at Pherkad Null Rift; ore into storage at Synchrony Hub | every pilot | 65 | 45 | -120 | -160 | 2026-11-15 |

## The Plans

`plans/<role>.json`: per role, the routes the dispatcher tries in this order for a free pilot. The role's Admiral keeps the file.

| Role | Kept by | Routes, first that is open |
|---|---|---|
| command | Unity | voidborn-substrate > voidborn-missions-1 > voidborn-mining-missions > voidborn-first-steps > census-frontier > park |
| drone | Apophis | voidborn-substrate > voidborn-missions-1 > voidborn-mining-missions > hunt-gsc-veil-ray > hunt-hamal-veil-ray > census-frontier > park |
| hauler | Apollo | voidborn-concurrent > voidborn-substrate > voidborn-missions-1 > voidborn-mining-missions > census-frontier > park |
| miner | Zero | voidborn-concurrent > voidborn-substrate > voidborn-missions-1 > voidborn-mining-missions > census-frontier > park |
| scout | Oracle | voidborn-substrate > voidborn-missions-1 > voidborn-mining-missions > voidborn-first-steps > census-voidborn > census-frontier > park |
| sentinel | Unity | voidborn-substrate > voidborn-missions-1 > voidborn-mining-missions > voidborn-first-steps > census-frontier > park |
| trader | Mercury | voidborn-concurrent > voidborn-substrate > voidborn-missions-1 > voidborn-mining-missions > census-frontier > park |

## Planned

What an Admiral means to do next (`planned` in its plan file), so that the others can plan around it.

| Role | What | When |
|---|---|---|
| drone | Railgun test at hunt-gsc-veil-ray for turn T5: kills per hunter-hour and credits per hunter-hour against the pulse-laser figure; if it pays, a railgun for the hunter of every herd (5,000 cr each, orders F12). | turn T5 to T6 |
| drone | hunt-ruchbah-veil-ray into the plan with max_ships 1 when the hand run's RESULT line shows a profit and no damage from a ship; then the veil-rays of Garnet Dim Lattice (8 at 21:24 UTC) the same way. | turn T6 |
| drone | First Hunt: Belt-Grazers (1,000 cr once, 3 belt-grazer kills) for every drone, as a route, once the circuit runner can hunt for a mission (request to Unity). | when the runner step exists |
| drone | Cinder-sylphs at Achernar Gas Pocket (40 hull; ember gland bid 480 cr for 550 at The Experiment): one ship, hand test. | turn T6 |
| hauler | Market Participation: Selling (1,000 cr once) for the haulers that hold it: sell 10 units from storage into a station bid at Central Nexus, by hand, after their mining-missions circuit; sell takes storage when the hold is empty (tested 2026-11-15) | turn T6 |
| hauler | A craft-and-sell route for stored ore once the circuit runner has its craft step (requests.log ENT-013), only where the depth at the best bid (best_buy_qty, read live with view_market) pays the fuel | after 2026-11-16 12:00 UTC |
| hauler | Measure how fast station-owned bids refill (iron ore at Central Nexus read 0 at 21:25 UTC after our sale) | turn T6 |
| miner | Energy crystal at the nebula of hunt-gsc-veil-ray: one miner, 40 minutes by hand (mine.py), then one focus_energy_crystal craft by hand and the sale into the one-unit station bid at The Experiment; the crystal share per pull measured | turn T5, 2026-11-15 |
| miner | Whether the station bid of 1,466 cr for one focused crystal at The Experiment refills, read from data/market/history.jsonl, before any second craft | turns T5 and T6 |
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

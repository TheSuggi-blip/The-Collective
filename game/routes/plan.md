---
name: routes-plan
id: 20261116T001236Z
tier: intel
author: Unity
---

# plan.md -- The Plans

Written by `python3 -B game/fleet/routes.py index`, never by hand, from
`plans/<role>.json`: per role (the word before the dash of a pilot's name) the routes
the dispatcher tries in this order for a free pilot. The role's Admiral keeps the
file; `planned` in it is what the Admiral means to do next. The roles at a glance:
[master-index.md](master-index.md); every route's figures: [index.md](index.md).

## command

Kept by Unity. Routes: 22.

| # | Route | Group | Zone | Open to | Credits per ship-hour |
|---|---|---|---|---|---|
| 1 | [voidborn-concurrent](voidborn-concurrent.json) | Once per Pilot | home space | once per pilot | TBD |
| 2 | [voidborn-substrate](voidborn-substrate.json) | Once per Pilot | home space | once per pilot, from 3,000 cr | one-time |
| 3 | [voidborn-missions-1](voidborn-missions-1.json) | Once per Pilot | home space | once per pilot, from 8,000 cr | one-time |
| 4 | [voidborn-mining-missions](voidborn-mining-missions.json) | Once per Pilot | home space | once per pilot, up to 40 ships | TBD |
| 5 | [voidborn-first-steps](voidborn-first-steps.json) | Off | home space | once per pilot, up to 2 ships, off | TBD |
| 6 | [voidborn-selling](voidborn-selling.json) | Once per Pilot | home space | once per pilot, up to 10 ships | one-time |
| 7 | [voidborn-precedence](voidborn-precedence.json) | Once per Pilot | home space | once per pilot, up to 40 ships | one-time |
| 8 | [voidborn-first-hunt-nexus](voidborn-first-hunt-nexus.json) | Once per Pilot | home space | once per pilot, up to 1 ships | TBD |
| 9 | [voidborn-first-hunt-gsc](voidborn-first-hunt-gsc.json) | Once per Pilot | home space | once per pilot, up to 1 ships | TBD |
| 10 | [voidborn-first-hunt-acubens](voidborn-first-hunt-acubens.json) | Once per Pilot | home space | once per pilot, up to 1 ships | TBD |
| 11 | [mine-node-beta-frozen-drift](mine-node-beta-frozen-drift.json) | Tests | home space | up to 1 ships, needs ice_harvester_i | TBD |
| 12 | [mine-ruchbah-ice-belt](mine-ruchbah-ice-belt.json) | Tests | beyond the border, 4 jumps | up to 1 ships, needs ice_harvester_i, empty hold | TBD |
| 13 | [mine-achernar-frost-ring](mine-achernar-frost-ring.json) | Tests | beyond the border, 4 jumps | up to 1 ships, needs ice_harvester_i, empty hold | TBD |
| 14 | [mine-wolf-1061-frozen-drift](mine-wolf-1061-frozen-drift.json) | Tests | beyond the border, 4 jumps | up to 1 ships, needs ice_harvester_i, empty hold | TBD |
| 15 | [mine-keid-ice-shelf](mine-keid-ice-shelf.json) | Tests | beyond the border, 5 jumps | up to 1 ships, needs ice_harvester_i, empty hold | TBD |
| 16 | [mine-cryogenic-reserve](mine-cryogenic-reserve.json) | Tests | home space | up to 1 ships, needs ice_harvester_i | TBD |
| 17 | [mine-alnair-ice-fields](mine-alnair-ice-fields.json) | Tests | beyond the border, 5 jumps | up to 1 ships, needs ice_harvester_i, empty hold | TBD |
| 18 | [mine-gsc-0041-frost-ring](mine-gsc-0041-frost-ring.json) | Tests | beyond the border, 4 jumps | up to 1 ships, needs ice_harvester_i, empty hold | TBD |
| 19 | [mine-antares-ice-fields](mine-antares-ice-fields.json) | Tests | beyond the border, 5 jumps | up to 1 ships, needs ice_harvester_i, empty hold | TBD |
| 20 | [mine-intercrus-ice-fields](mine-intercrus-ice-fields.json) | Tests | beyond the border, 7 jumps | up to 1 ships, needs ice_harvester_i, empty hold | TBD |
| 21 | [census-frontier](census-frontier.json) | Reading and Waiting | beyond the border, 7 jumps | up to 12 ships, empty hold | -600 |
| 22 | [park](park.json) | Reading and Waiting | home space | the park route | TBD |

## drone

Kept by Apophis. Routes: 21.

| # | Route | Group | Zone | Open to | Credits per ship-hour |
|---|---|---|---|---|---|
| 1 | [voidborn-precedence](voidborn-precedence.json) | Once per Pilot | home space | once per pilot, up to 40 ships | one-time |
| 2 | [voidborn-first-hunt-nexus](voidborn-first-hunt-nexus.json) | Once per Pilot | home space | once per pilot, up to 1 ships | TBD |
| 3 | [voidborn-first-hunt-gsc](voidborn-first-hunt-gsc.json) | Once per Pilot | home space | once per pilot, up to 1 ships | TBD |
| 4 | [voidborn-first-hunt-acubens](voidborn-first-hunt-acubens.json) | Once per Pilot | home space | once per pilot, up to 1 ships | TBD |
| 5 | [voidborn-first-hunt-schedar](voidborn-first-hunt-schedar.json) | Once per Pilot | beyond the border, 2 jumps | once per pilot, up to 1 ships, empty hold | TBD |
| 6 | [voidborn-selling](voidborn-selling.json) | Once per Pilot | home space | once per pilot, up to 10 ships | one-time |
| 7 | [voidborn-concurrent](voidborn-concurrent.json) | Once per Pilot | home space | once per pilot | TBD |
| 8 | [voidborn-substrate](voidborn-substrate.json) | Once per Pilot | home space | once per pilot, from 3,000 cr | one-time |
| 9 | [voidborn-missions-1](voidborn-missions-1.json) | Once per Pilot | home space | once per pilot, from 8,000 cr | one-time |
| 10 | [voidborn-mining-missions](voidborn-mining-missions.json) | Once per Pilot | home space | once per pilot, up to 40 ships | TBD |
| 11 | [hunt-gsc-veil-ray](hunt-gsc-veil-ray.json) | Paying Routes | home space | up to 1 ships, without piercing_railgun_i | 3,620 |
| 12 | [hunt-hamal-veil-ray](hunt-hamal-veil-ray.json) | Paying Routes | home space | up to 1 ships, without piercing_railgun_i | 2,890 |
| 13 | [hunt-cedarhold-dim-lattice-veil-ray](hunt-cedarhold-dim-lattice-veil-ray.json) | Tests | beyond the border, 5 jumps | up to 1 ships, without piercing_railgun_i, empty hold | TBD |
| 14 | [hunt-garnet-dim-lattice-veil-ray](hunt-garnet-dim-lattice-veil-ray.json) | Measured at a Loss | beyond the border, 5 jumps | up to 1 ships, without piercing_railgun_i, empty hold | -590 |
| 15 | [hunt-ruchbah-veil-ray](hunt-ruchbah-veil-ray.json) | Paying Routes | beyond the border, 4 jumps | up to 1 ships, without piercing_railgun_i, empty hold | 1,920 |
| 16 | [hunt-low-charge-glint-veil-ray](hunt-low-charge-glint-veil-ray.json) | Measured at a Loss | beyond the border, 4 jumps | up to 1 ships, without piercing_railgun_i, empty hold | -540 |
| 17 | [hunt-faintlight-drift-veil-ray](hunt-faintlight-drift-veil-ray.json) | Tests | beyond the border, 5 jumps | up to 1 ships, without piercing_railgun_i, empty hold | TBD |
| 18 | [hunt-keid-fractured-prism-veil-ray](hunt-keid-fractured-prism-veil-ray.json) | Tests | beyond the border, 5 jumps | up to 1 ships, without piercing_railgun_i, empty hold | TBD |
| 19 | [hunt-test-acubens-patina-grazer](hunt-test-acubens-patina-grazer.json) | Measured at a Loss | home space | up to 1 ships, without piercing_railgun_i | -600 |
| 20 | [census-frontier](census-frontier.json) | Reading and Waiting | beyond the border, 7 jumps | up to 12 ships, empty hold | -600 |
| 21 | [park](park.json) | Reading and Waiting | home space | the park route | TBD |

Planned:

| What | When |
|---|---|
| First Hunt: Belt-Grazers for every drone: the three routes voidborn-first-hunt-nexus, -gsc and -acubens stand at the head since 2026-11-15 23:51 UTC, one hunter per herd; when every drone has it booked they pass by themselves (skip_if_booked). | turns T7 to T9 |
| Frontier veil-ray tests and yield tests: routes.py measure --write after their first RESULT lines; a test that lost money leaves the plan, a yield whose drop sells becomes a ranched route. | turn T8 |
| The railgun ship: ammunition from stored iron (2 steel plate and 3 iron ore make 5 Ferrous Slug Cases, one case loads a magazine; the craft costs no credits), then a yield test of armoured prey of 100 hull or less, where armour bypass may count. | turn T8 |
| The next hull: commission_quote of the tier-1 Vigil (two weapon slots, hull 75, cargo 20, no Piloting gate named) at a Voidborn shipyard; one ship, two Pulse Laser I, against a home veil-ray herd, measured against the starter's trips. | turn T8, after the quote |

## hauler

Kept by Apollo. Routes: 9.

| # | Route | Group | Zone | Open to | Credits per ship-hour |
|---|---|---|---|---|---|
| 1 | [voidborn-precedence](voidborn-precedence.json) | Once per Pilot | home space | once per pilot, up to 40 ships | one-time |
| 2 | [voidborn-selling](voidborn-selling.json) | Once per Pilot | home space | once per pilot, up to 10 ships | one-time |
| 3 | [voidborn-first-hunt-nexus](voidborn-first-hunt-nexus.json) | Once per Pilot | home space | once per pilot, up to 1 ships | TBD |
| 4 | [voidborn-concurrent](voidborn-concurrent.json) | Once per Pilot | home space | once per pilot | TBD |
| 5 | [voidborn-substrate](voidborn-substrate.json) | Once per Pilot | home space | once per pilot, from 3,000 cr | one-time |
| 6 | [voidborn-missions-1](voidborn-missions-1.json) | Once per Pilot | home space | once per pilot, from 8,000 cr | one-time |
| 7 | [voidborn-mining-missions](voidborn-mining-missions.json) | Once per Pilot | home space | once per pilot, up to 40 ships | TBD |
| 8 | [census-frontier](census-frontier.json) | Reading and Waiting | beyond the border, 7 jumps | up to 12 ships, empty hold | -600 |
| 9 | [park](park.json) | Reading and Waiting | home space | the park route | TBD |

Planned:

| What | When |
|---|---|
| A route that sells stored neural soma from storage at Synchrony Hub and Node Beta into station bids of 600 cr or more, sent only while such a bid stands (requests.log ENT-065); until then by hand with one hauler when a bid is read | after 2026-11-16 12:00 UTC |
| First Steps in the Void for the 14 haulers that still hold it, once game/routes/voidborn-first-steps.json is on again (requests.log ENT-064); the Acubens belt refills its carbon | turn T7 and T8 |
| voidborn-first-hunt-gsc and voidborn-first-hunt-acubens into the plan when their first RESULT lines are read | turn T8 |
| A craft-and-sell route for stored ore once the circuit runner has its craft step (requests.log ENT-013), only where the depth at the best bid (best_buy_qty, read live with view_market) pays the fuel | after 2026-11-16 12:00 UTC |
| Steel plate for a faction lockbox from stored iron at the free workshop (10 ore a plate), when the Fleet Admiral names the builder and the station (guidebook logistics.md, section 8) | on the Fleet Admiral's word |

## miner

Kept by Zero. Routes: 24.

| # | Route | Group | Zone | Open to | Credits per ship-hour |
|---|---|---|---|---|---|
| 1 | [voidborn-concurrent](voidborn-concurrent.json) | Once per Pilot | home space | once per pilot | TBD |
| 2 | [voidborn-substrate](voidborn-substrate.json) | Once per Pilot | home space | once per pilot, from 3,000 cr | one-time |
| 3 | [voidborn-missions-1](voidborn-missions-1.json) | Once per Pilot | home space | once per pilot, from 8,000 cr | one-time |
| 4 | [voidborn-mining-missions](voidborn-mining-missions.json) | Once per Pilot | home space | once per pilot, up to 40 ships | TBD |
| 5 | [voidborn-precedence](voidborn-precedence.json) | Once per Pilot | home space | once per pilot, up to 40 ships | one-time |
| 6 | [voidborn-first-hunt-nexus](voidborn-first-hunt-nexus.json) | Once per Pilot | home space | once per pilot, up to 1 ships | TBD |
| 7 | [voidborn-first-hunt-gsc](voidborn-first-hunt-gsc.json) | Once per Pilot | home space | once per pilot, up to 1 ships | TBD |
| 8 | [voidborn-first-hunt-acubens](voidborn-first-hunt-acubens.json) | Once per Pilot | home space | once per pilot, up to 1 ships | TBD |
| 9 | [fit-ice-harvester](fit-ice-harvester.json) | Fitting | home space | once per pilot, up to 1 ships, 12 pilots in all, without ice_harvester_i, from 6,000 cr | TBD |
| 10 | [fit-gas-harvester](fit-gas-harvester.json) | Fitting | home space | once per pilot, up to 1 ships, 1 pilots in all, needs mining_laser_i, without ice_harvester_i, from 6,000 cr | TBD |
| 11 | [mine-wolf-1061-vent](mine-wolf-1061-vent.json) | Tests | beyond the border, 4 jumps | up to 1 ships, needs nitrogen_vent, empty hold | TBD |
| 12 | [mine-ruchbah-ice-belt](mine-ruchbah-ice-belt.json) | Tests | beyond the border, 4 jumps | up to 1 ships, needs ice_harvester_i, empty hold | TBD |
| 13 | [mine-achernar-frost-ring](mine-achernar-frost-ring.json) | Tests | beyond the border, 4 jumps | up to 1 ships, needs ice_harvester_i, empty hold | TBD |
| 14 | [mine-cryogenic-reserve](mine-cryogenic-reserve.json) | Tests | home space | up to 1 ships, needs ice_harvester_i | TBD |
| 15 | [mine-keid-ice-shelf](mine-keid-ice-shelf.json) | Tests | beyond the border, 5 jumps | up to 1 ships, needs ice_harvester_i, empty hold | TBD |
| 16 | [mine-intercrus-ice-fields](mine-intercrus-ice-fields.json) | Tests | beyond the border, 7 jumps | up to 1 ships, needs ice_harvester_i, empty hold | TBD |
| 17 | [mine-wolf-1061-frozen-drift](mine-wolf-1061-frozen-drift.json) | Tests | beyond the border, 4 jumps | up to 1 ships, needs ice_harvester_i, empty hold | TBD |
| 18 | [mine-alnair-ice-fields](mine-alnair-ice-fields.json) | Tests | beyond the border, 5 jumps | up to 1 ships, needs ice_harvester_i, empty hold | TBD |
| 19 | [mine-node-beta-frozen-drift](mine-node-beta-frozen-drift.json) | Tests | home space | up to 1 ships, needs ice_harvester_i | TBD |
| 20 | [mine-gsc-0041-frost-ring](mine-gsc-0041-frost-ring.json) | Tests | beyond the border, 4 jumps | up to 1 ships, needs ice_harvester_i, empty hold | TBD |
| 21 | [mine-antares-ice-fields](mine-antares-ice-fields.json) | Tests | beyond the border, 5 jumps | up to 1 ships, needs ice_harvester_i, empty hold | TBD |
| 22 | [mine-gsc-0050-gas-plume](mine-gsc-0050-gas-plume.json) | Tests | beyond the border, 3 jumps | up to 1 ships, needs gas_harvester_i, empty hold | TBD |
| 23 | [census-frontier](census-frontier.json) | Reading and Waiting | beyond the border, 7 jumps | up to 12 ships, empty hold | -600 |
| 24 | [park](park.json) | Reading and Waiting | home space | the park route | TBD |

Planned:

| What | When |
|---|---|
| Read the first RESULT line of every ice route; then routes.py measure --write and lift max_ships where the water-ice depth at the best bid carries more ships (ledger.py prices water_ice, view_market at the station), with max_pilots of fit-ice-harvester beside it | turn T8 |
| Compare the vent route's loads with run 1 at the same field (126 units in 25 minutes, 32% nitrogen ice): a Nitrogen Vent for every ice miner if it raises water and rare ice per minute; one vent was on offer in our six books (2026-11-15 23:30 UTC) | turn T8 |
| Deuterium ice and plasma gas, one test each once the ice routes hold: the deuterium bids are a few units (Node Alpha 208 x 6, Node Beta 226 x 5) and count as one-time prices until data/market/history.jsonl shows them refill (F12); a gas harvester takes the mining laser's slot | turn T8 and T9 |
| One focused crystal from the 20 energy crystals in storage at Node Beta whenever The Experiment's station bid of 1,466 cr stands again (ledger.py prices focused_crystal) | every turn |

## scout

Kept by Oracle. Routes: 12.

| # | Route | Group | Zone | Open to | Credits per ship-hour |
|---|---|---|---|---|---|
| 1 | [census-voidborn](census-voidborn.json) | Reading and Waiting | home space | up to 3 ships | -550 |
| 2 | [voidborn-precedence](voidborn-precedence.json) | Once per Pilot | home space | once per pilot, up to 40 ships | one-time |
| 3 | [voidborn-selling](voidborn-selling.json) | Once per Pilot | home space | once per pilot, up to 10 ships | one-time |
| 4 | [voidborn-first-hunt-nexus](voidborn-first-hunt-nexus.json) | Once per Pilot | home space | once per pilot, up to 1 ships | TBD |
| 5 | [voidborn-first-hunt-gsc](voidborn-first-hunt-gsc.json) | Once per Pilot | home space | once per pilot, up to 1 ships | TBD |
| 6 | [voidborn-first-hunt-acubens](voidborn-first-hunt-acubens.json) | Once per Pilot | home space | once per pilot, up to 1 ships | TBD |
| 7 | [voidborn-concurrent](voidborn-concurrent.json) | Once per Pilot | home space | once per pilot | TBD |
| 8 | [voidborn-substrate](voidborn-substrate.json) | Once per Pilot | home space | once per pilot, from 3,000 cr | one-time |
| 9 | [voidborn-missions-1](voidborn-missions-1.json) | Once per Pilot | home space | once per pilot, from 8,000 cr | one-time |
| 10 | [voidborn-mining-missions](voidborn-mining-missions.json) | Once per Pilot | home space | once per pilot, up to 40 ships | TBD |
| 11 | [census-frontier](census-frontier.json) | Reading and Waiting | beyond the border, 7 jumps | up to 12 ships, empty hold | -600 |
| 12 | [park](park.json) | Reading and Waiting | home space | the park route | TBD |

Planned:

| What | When |
|---|---|
| Keep every Voidborn system read within the hour: census-voidborn every_minutes 30, max_ships 3; read the gaps per system every turn and change the threshold only on a measured gap over 60 minutes | every turn |
| census-frontier: 42 systems (rings 1 to 3 of our border, Atlas, Intercrus, LHS 1140, Goldcrest, Bluerift), every 240 minutes, 12 ships. Next ring, once the cost of the ring-3 reads is measured: acrab, acrux, botein, deepwell, felis, gliese_876, hd_147513, marfik, rastaban; not the pirate stronghold gliese_581 | turn T8 |
| Base-site line in the system file of every new read (LHS 1140 and the third ring once the tracker files them): lawless, police, a station already there, places without a base, foreign pilots seen | turn T8 |
| voidborn-precedence and the three voidborn-first-hunt routes at the head of the plan as soon as the command group's first RESULT lines show the reward | turn T7 and T8 |
| Read the game's changelog at every turn and name each line of game/rules/ a release makes wrong in a request to the Fleet Admiral | every turn |

## sentinel

Kept by Unity. Routes: 23.

| # | Route | Group | Zone | Open to | Credits per ship-hour |
|---|---|---|---|---|---|
| 1 | [voidborn-concurrent](voidborn-concurrent.json) | Once per Pilot | home space | once per pilot | TBD |
| 2 | [voidborn-substrate](voidborn-substrate.json) | Once per Pilot | home space | once per pilot, from 3,000 cr | one-time |
| 3 | [voidborn-missions-1](voidborn-missions-1.json) | Once per Pilot | home space | once per pilot, from 8,000 cr | one-time |
| 4 | [voidborn-mining-missions](voidborn-mining-missions.json) | Once per Pilot | home space | once per pilot, up to 40 ships | TBD |
| 5 | [voidborn-first-steps](voidborn-first-steps.json) | Off | home space | once per pilot, up to 2 ships, off | TBD |
| 6 | [voidborn-selling](voidborn-selling.json) | Once per Pilot | home space | once per pilot, up to 10 ships | one-time |
| 7 | [voidborn-precedence](voidborn-precedence.json) | Once per Pilot | home space | once per pilot, up to 40 ships | one-time |
| 8 | [voidborn-first-hunt-nexus](voidborn-first-hunt-nexus.json) | Once per Pilot | home space | once per pilot, up to 1 ships | TBD |
| 9 | [voidborn-first-hunt-gsc](voidborn-first-hunt-gsc.json) | Once per Pilot | home space | once per pilot, up to 1 ships | TBD |
| 10 | [voidborn-first-hunt-acubens](voidborn-first-hunt-acubens.json) | Once per Pilot | home space | once per pilot, up to 1 ships | TBD |
| 11 | [fit-ice-harvester-guard](fit-ice-harvester-guard.json) | Fitting | home space | once per pilot, up to 2 ships, 4 pilots in all, without ice_harvester_i, from 6,000 cr | TBD |
| 12 | [mine-node-beta-frozen-drift](mine-node-beta-frozen-drift.json) | Tests | home space | up to 1 ships, needs ice_harvester_i | TBD |
| 13 | [mine-ruchbah-ice-belt](mine-ruchbah-ice-belt.json) | Tests | beyond the border, 4 jumps | up to 1 ships, needs ice_harvester_i, empty hold | TBD |
| 14 | [mine-achernar-frost-ring](mine-achernar-frost-ring.json) | Tests | beyond the border, 4 jumps | up to 1 ships, needs ice_harvester_i, empty hold | TBD |
| 15 | [mine-wolf-1061-frozen-drift](mine-wolf-1061-frozen-drift.json) | Tests | beyond the border, 4 jumps | up to 1 ships, needs ice_harvester_i, empty hold | TBD |
| 16 | [mine-keid-ice-shelf](mine-keid-ice-shelf.json) | Tests | beyond the border, 5 jumps | up to 1 ships, needs ice_harvester_i, empty hold | TBD |
| 17 | [mine-cryogenic-reserve](mine-cryogenic-reserve.json) | Tests | home space | up to 1 ships, needs ice_harvester_i | TBD |
| 18 | [mine-alnair-ice-fields](mine-alnair-ice-fields.json) | Tests | beyond the border, 5 jumps | up to 1 ships, needs ice_harvester_i, empty hold | TBD |
| 19 | [mine-gsc-0041-frost-ring](mine-gsc-0041-frost-ring.json) | Tests | beyond the border, 4 jumps | up to 1 ships, needs ice_harvester_i, empty hold | TBD |
| 20 | [mine-antares-ice-fields](mine-antares-ice-fields.json) | Tests | beyond the border, 5 jumps | up to 1 ships, needs ice_harvester_i, empty hold | TBD |
| 21 | [mine-intercrus-ice-fields](mine-intercrus-ice-fields.json) | Tests | beyond the border, 7 jumps | up to 1 ships, needs ice_harvester_i, empty hold | TBD |
| 22 | [census-frontier](census-frontier.json) | Reading and Waiting | beyond the border, 7 jumps | up to 12 ships, empty hold | -600 |
| 23 | [park](park.json) | Reading and Waiting | home space | the park route | TBD |

## trader

Kept by Mercury. Routes: 8.

| # | Route | Group | Zone | Open to | Credits per ship-hour |
|---|---|---|---|---|---|
| 1 | [voidborn-concurrent](voidborn-concurrent.json) | Once per Pilot | home space | once per pilot | TBD |
| 2 | [voidborn-substrate](voidborn-substrate.json) | Once per Pilot | home space | once per pilot, from 3,000 cr | one-time |
| 3 | [voidborn-missions-1](voidborn-missions-1.json) | Once per Pilot | home space | once per pilot, from 8,000 cr | one-time |
| 4 | [voidborn-mining-missions](voidborn-mining-missions.json) | Once per Pilot | home space | once per pilot, up to 40 ships | TBD |
| 5 | [voidborn-precedence](voidborn-precedence.json) | Once per Pilot | home space | once per pilot, up to 40 ships | one-time |
| 6 | [voidborn-conductive-lattice](voidborn-conductive-lattice.json) | Once per Pilot | beyond the border, 6 jumps | once per pilot, up to 3 ships, 9 pilots in all, empty hold, from 6,300 cr | TBD |
| 7 | [census-frontier](census-frontier.json) | Reading and Waiting | beyond the border, 7 jumps | up to 12 ships, empty hold | -600 |
| 8 | [park](park.json) | Reading and Waiting | home space | the park route | TBD |

Planned:

| What | When |
|---|---|
| Control-node craft by hand: one trader, one craft (2 nodes) at Central Nexus, sold at Node Gamma; every call and answer recorded for the runner's craft step (requests.log ENT-030). A route with max_ships 1 only when the craft step exists and the per-level books show depth at both ends. | turn T5, 2026-11-15 |
| Gaps between our six stations from data/market/history.jsonl, read by depth at the best level (best_buy_qty, best_sell_qty), not the total; no trade route until one holds over a day of reads and covers fuel and the 1% tax. | turns T6 to T8 |
| One trader, hold empty, to a frontier station the census-frontier read shows with an order book worth the trip (orders F13): bids for what our stations sell cheap, asks under our bids. Waits for the scouts' first reads. | after the first census-frontier reads |

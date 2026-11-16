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

Kept by Unity. Routes: 23.

| # | Route | Group | Zone | Open to | Credits per ship-hour |
|---|---|---|---|---|---|
| 1 | [voidborn-concurrent](voidborn-concurrent.json) | Once per Pilot | home space | once per pilot | one-time |
| 2 | [voidborn-substrate](voidborn-substrate.json) | Once per Pilot | home space | once per pilot, from 3,000 cr | one-time |
| 3 | [voidborn-missions-1](voidborn-missions-1.json) | Once per Pilot | home space | once per pilot, from 8,000 cr | one-time |
| 4 | [voidborn-mining-missions](voidborn-mining-missions.json) | Once per Pilot | home space | once per pilot, up to 40 ships | one-time |
| 5 | [voidborn-first-steps](voidborn-first-steps.json) | Once per Pilot | home space | once per pilot, up to 2 ships | one-time |
| 6 | [voidborn-selling](voidborn-selling.json) | Once per Pilot | home space | once per pilot, up to 10 ships | one-time |
| 7 | [voidborn-precedence](voidborn-precedence.json) | Once per Pilot | home space | once per pilot, up to 40 ships | one-time |
| 8 | [voidborn-first-hunt-nexus](voidborn-first-hunt-nexus.json) | Once per Pilot | home space | once per pilot, up to 1 ships | one-time |
| 9 | [voidborn-first-hunt-gsc](voidborn-first-hunt-gsc.json) | Once per Pilot | home space | once per pilot, up to 1 ships | one-time |
| 10 | [voidborn-first-hunt-acubens](voidborn-first-hunt-acubens.json) | Once per Pilot | home space | once per pilot, up to 1 ships | one-time |
| 11 | [mine-node-beta-frozen-drift](mine-node-beta-frozen-drift.json) | Paying Routes | home space | up to 1 ships, needs ice_harvester_i | 2,460 |
| 12 | [mine-ruchbah-ice-belt](mine-ruchbah-ice-belt.json) | Paying Routes | beyond the border, 4 jumps | up to 3 ships, needs ice_harvester_i, empty hold | 8,270 |
| 13 | [mine-achernar-frost-ring](mine-achernar-frost-ring.json) | Paying Routes | beyond the border, 4 jumps | up to 3 ships, needs ice_harvester_i, empty hold | 7,470 |
| 14 | [mine-wolf-1061-frozen-drift](mine-wolf-1061-frozen-drift.json) | Paying Routes | beyond the border, 4 jumps | up to 2 ships, needs ice_harvester_i, empty hold | 4,430 |
| 15 | [mine-keid-ice-shelf](mine-keid-ice-shelf.json) | Paying Routes | beyond the border, 5 jumps | up to 2 ships, needs ice_harvester_i, empty hold | 2,990 |
| 16 | [mine-cryogenic-reserve](mine-cryogenic-reserve.json) | Measured at a Loss | home space | up to 1 ships, needs ice_harvester_i | -350 |
| 17 | [mine-alnair-ice-fields](mine-alnair-ice-fields.json) | Paying Routes | beyond the border, 5 jumps | up to 2 ships, needs ice_harvester_i, empty hold | 4,430 |
| 18 | [mine-gsc-0041-frost-ring](mine-gsc-0041-frost-ring.json) | Paying Routes | beyond the border, 4 jumps | up to 1 ships, needs ice_harvester_i, empty hold | 4,560 |
| 19 | [mine-antares-ice-fields](mine-antares-ice-fields.json) | Paying Routes | beyond the border, 5 jumps | up to 1 ships, needs ice_harvester_i, empty hold | 2,700 |
| 20 | [mine-intercrus-ice-fields](mine-intercrus-ice-fields.json) | Paying Routes | beyond the border, 7 jumps | up to 2 ships, needs ice_harvester_i, empty hold | 2,460 |
| 21 | [mission-cracking-the-shell-central](mission-cracking-the-shell-central.json) | Once per Pilot | home space | once per pilot, up to 1 ships | one-time |
| 22 | [census-frontier](census-frontier.json) | Reading and Waiting | beyond the border, 7 jumps | up to 12 ships, empty hold | -600 |
| 23 | [park](park.json) | Reading and Waiting | home space | the park route | -550 |

## drone

Kept by Apophis. Routes: 32.

| # | Route | Group | Zone | Open to | Credits per ship-hour |
|---|---|---|---|---|---|
| 1 | [voidborn-precedence](voidborn-precedence.json) | Once per Pilot | home space | once per pilot, up to 40 ships | one-time |
| 2 | [voidborn-first-hunt-nexus](voidborn-first-hunt-nexus.json) | Once per Pilot | home space | once per pilot, up to 1 ships | one-time |
| 3 | [voidborn-first-hunt-gsc](voidborn-first-hunt-gsc.json) | Once per Pilot | home space | once per pilot, up to 1 ships | one-time |
| 4 | [voidborn-first-hunt-acubens](voidborn-first-hunt-acubens.json) | Once per Pilot | home space | once per pilot, up to 1 ships | one-time |
| 5 | [voidborn-first-hunt-ironhollow-echo](voidborn-first-hunt-ironhollow-echo.json) | Once per Pilot | beyond the border, 4 jumps | once per pilot, up to 1 ships, empty hold | TBD |
| 6 | [voidborn-first-hunt-ironhollow-fading](voidborn-first-hunt-ironhollow-fading.json) | Once per Pilot | beyond the border, 4 jumps | once per pilot, up to 1 ships, empty hold | TBD |
| 7 | [voidborn-first-hunt-achernar](voidborn-first-hunt-achernar.json) | Once per Pilot | beyond the border, 4 jumps | once per pilot, up to 1 ships, empty hold | TBD |
| 8 | [voidborn-first-steps](voidborn-first-steps.json) | Once per Pilot | home space | once per pilot, up to 2 ships | one-time |
| 9 | [voidborn-selling](voidborn-selling.json) | Once per Pilot | home space | once per pilot, up to 10 ships | one-time |
| 10 | [voidborn-concurrent](voidborn-concurrent.json) | Once per Pilot | home space | once per pilot | one-time |
| 11 | [voidborn-substrate](voidborn-substrate.json) | Once per Pilot | home space | once per pilot, from 3,000 cr | one-time |
| 12 | [voidborn-missions-1](voidborn-missions-1.json) | Once per Pilot | home space | once per pilot, from 8,000 cr | one-time |
| 13 | [voidborn-mining-missions](voidborn-mining-missions.json) | Once per Pilot | home space | once per pilot, up to 40 ships | one-time |
| 14 | [hunt-test-achernar-cinder-sylph](hunt-test-achernar-cinder-sylph.json) | Tests | beyond the border, 4 jumps | up to 1 ships, without piercing_railgun_i, empty hold | TBD |
| 15 | [hunt-faintlight-drift-veil-ray](hunt-faintlight-drift-veil-ray.json) | Paying Routes | beyond the border, 5 jumps | up to 1 ships, without piercing_railgun_i, empty hold | 3,730 |
| 16 | [hunt-gsc-veil-ray](hunt-gsc-veil-ray.json) | Paying Routes | home space | up to 1 ships, without piercing_railgun_i | 3,620 |
| 17 | [hunt-hamal-veil-ray](hunt-hamal-veil-ray.json) | Paying Routes | home space | up to 1 ships, without piercing_railgun_i | 2,890 |
| 18 | [hunt-ruchbah-veil-ray](hunt-ruchbah-veil-ray.json) | Paying Routes | beyond the border, 4 jumps | up to 1 ships, without piercing_railgun_i, empty hold | 2,950 |
| 19 | [hunt-keid-fractured-prism-veil-ray](hunt-keid-fractured-prism-veil-ray.json) | Paying Routes | beyond the border, 5 jumps | up to 1 ships, without piercing_railgun_i, empty hold | 2,050 |
| 20 | [hunt-low-charge-glint-veil-ray](hunt-low-charge-glint-veil-ray.json) | Paying Routes | beyond the border, 4 jumps | up to 1 ships, without piercing_railgun_i, empty hold | 2,110 |
| 21 | [hunt-cedarhold-dim-lattice-veil-ray](hunt-cedarhold-dim-lattice-veil-ray.json) | Paying Routes | beyond the border, 5 jumps | up to 1 ships, without piercing_railgun_i, empty hold | 1,180 |
| 22 | [hunt-dimming-pocket-veil-ray](hunt-dimming-pocket-veil-ray.json) | Tests | beyond the border, 4 jumps | up to 1 ships, empty hold | TBD |
| 23 | [hunt-denebola-fractured-prism-veil-ray](hunt-denebola-fractured-prism-veil-ray.json) | Tests | beyond the border, 5 jumps | up to 1 ships, empty hold | TBD |
| 24 | [hunt-test-lesath-cinder-sylph](hunt-test-lesath-cinder-sylph.json) | Tests | beyond the border, 5 jumps | up to 1 ships, without piercing_railgun_i, empty hold | TBD |
| 25 | [hunt-test-gsc-0050-cinder-sylph](hunt-test-gsc-0050-cinder-sylph.json) | Tests | beyond the border, 3 jumps | up to 1 ships, without piercing_railgun_i, empty hold | TBD |
| 26 | [hunt-test-atlas-patina-grazer](hunt-test-atlas-patina-grazer.json) | Tests | beyond the border, 6 jumps | up to 1 ships, without piercing_railgun_i, empty hold | TBD |
| 27 | [hunt-test-garnet-slag-tortoise](hunt-test-garnet-slag-tortoise.json) | Tests | beyond the border, 5 jumps | up to 1 ships, without piercing_railgun_i, empty hold | TBD |
| 28 | [hunt-test-goldcrest-glitterback-crab](hunt-test-goldcrest-glitterback-crab.json) | Tests | beyond the border, 7 jumps | up to 1 ships, without piercing_railgun_i, empty hold | TBD |
| 29 | [hunt-test-tanglewood-hollow-pilgrim](hunt-test-tanglewood-hollow-pilgrim.json) | Tests | beyond the border, 6 jumps | up to 1 ships, without piercing_railgun_i, empty hold | TBD |
| 30 | [voidborn-first-hunt-schedar](voidborn-first-hunt-schedar.json) | Once per Pilot | beyond the border, 2 jumps | once per pilot, up to 1 ships, empty hold | one-time |
| 31 | [census-frontier](census-frontier.json) | Reading and Waiting | beyond the border, 7 jumps | up to 12 ships, empty hold | -600 |
| 32 | [park](park.json) | Reading and Waiting | home space | the park route | -550 |

Planned:

| What | When |
|---|---|
| First Hunt for the 21 drones that have not flown it: six herds at one hunter each (three home, three beside The Experiment); they pass by themselves once every drone has it booked (skip_if_booked). | turn T9, about two hours |
| Cracking the Shell (1,500 cr once) at Achernar Frost Ring for every drone with First Hunt booked, once a route can require a booked reward or a refused accept counts as no try (requests.log). | when the dispatcher change exists |
| Read the first RESULT lines of the five yield tests and the two new veil-ray herds; a drop that sells above fuel makes a ranched route, the rest leave the plan. | next turn |
| The railgun ship: Pulse Laser I back in its weapon slot from storage, or ammunition once the dispatcher checks it (owed by Unity). | next turn |
| Guard: a route kind guard (owed by Unity, requests.log ENT-076) for a drone beside every mine route beyond the border; until then the hunts at Ruchbah, Keid and Achernar are the presence. | when the guard kind exists |
| The next hull: a tier-1 Vigil as one test, after a yield test shows prey worth a tougher hull; quotes in guidebook section 5. | after the yield tests |

## hauler

Kept by Apollo. Routes: 19.

| # | Route | Group | Zone | Open to | Credits per ship-hour |
|---|---|---|---|---|---|
| 1 | [voidborn-precedence](voidborn-precedence.json) | Once per Pilot | home space | once per pilot, up to 40 ships | one-time |
| 2 | [voidborn-selling](voidborn-selling.json) | Once per Pilot | home space | once per pilot, up to 10 ships | one-time |
| 3 | [voidborn-first-hunt-nexus](voidborn-first-hunt-nexus.json) | Once per Pilot | home space | once per pilot, up to 1 ships | one-time |
| 4 | [voidborn-concurrent](voidborn-concurrent.json) | Once per Pilot | home space | once per pilot | one-time |
| 5 | [voidborn-substrate](voidborn-substrate.json) | Once per Pilot | home space | once per pilot, from 3,000 cr | one-time |
| 6 | [voidborn-missions-1](voidborn-missions-1.json) | Once per Pilot | home space | once per pilot, from 8,000 cr | one-time |
| 7 | [voidborn-mining-missions](voidborn-mining-missions.json) | Once per Pilot | home space | once per pilot, up to 40 ships | one-time |
| 8 | [voidborn-first-steps](voidborn-first-steps.json) | Once per Pilot | home space | once per pilot, up to 2 ships | one-time |
| 9 | [hunt-dimming-pocket-veil-ray](hunt-dimming-pocket-veil-ray.json) | Tests | beyond the border, 4 jumps | up to 1 ships, empty hold | TBD |
| 10 | [hunt-denebola-fractured-prism-veil-ray](hunt-denebola-fractured-prism-veil-ray.json) | Tests | beyond the border, 5 jumps | up to 1 ships, empty hold | TBD |
| 11 | [fit-gas-harvester-hauler](fit-gas-harvester-hauler.json) | Fitting | home space | once per pilot, up to 1 ships, 1 pilots in all, needs mining_laser_i, without gas_harvester_i, from 6,000 cr | TBD |
| 12 | [mine-achernar-gas-pocket](mine-achernar-gas-pocket.json) | Tests | beyond the border, 4 jumps | up to 1 ships, needs gas_harvester_i, empty hold | TBD |
| 13 | [voidborn-first-hunt-acubens](voidborn-first-hunt-acubens.json) | Once per Pilot | home space | once per pilot, up to 1 ships | one-time |
| 14 | [voidborn-first-hunt-gsc](voidborn-first-hunt-gsc.json) | Once per Pilot | home space | once per pilot, up to 1 ships | one-time |
| 15 | [voidborn-first-hunt-schedar](voidborn-first-hunt-schedar.json) | Once per Pilot | beyond the border, 2 jumps | once per pilot, up to 1 ships, empty hold | one-time |
| 16 | [voidborn-first-hunt-achernar](voidborn-first-hunt-achernar.json) | Once per Pilot | beyond the border, 4 jumps | once per pilot, up to 1 ships, empty hold | TBD |
| 17 | [voidborn-first-hunt-gsc-0031](voidborn-first-hunt-gsc-0031.json) | Once per Pilot | beyond the border, 5 jumps | once per pilot, up to 1 ships, empty hold | TBD |
| 18 | [census-frontier](census-frontier.json) | Reading and Waiting | beyond the border, 7 jumps | up to 12 ships, empty hold | -600 |
| 19 | [park](park.json) | Reading and Waiting | home space | the park route | -550 |

Planned:

| What | When |
|---|---|
| A route that sells stored neural soma from storage at Synchrony Hub and Node Beta into station bids of 600 cr or more, sent only while such a bid stands (requests.log ENT-065); until then by hand with one hauler when a bid is read | after 2026-11-16 12:00 UTC |
| First Steps in the Void for the 14 haulers that still hold it, once game/routes/voidborn-first-steps.json is on again (requests.log ENT-064); the Acubens belt refills its carbon | turn T7 and T8 |
| voidborn-first-hunt-gsc and voidborn-first-hunt-acubens into the plan when their first RESULT lines are read | turn T8 |
| A craft-and-sell route for stored ore once the circuit runner has its craft step (requests.log ENT-013), only where the depth at the best bid (best_buy_qty, read live with view_market) pays the fuel | after 2026-11-16 12:00 UTC |
| Steel plate for a faction lockbox from stored iron at the free workshop (10 ore a plate), when the Fleet Admiral names the builder and the station (guidebook logistics.md, section 8) | on the Fleet Admiral's word |

## miner

Kept by Zero. Routes: 36.

| # | Route | Group | Zone | Open to | Credits per ship-hour |
|---|---|---|---|---|---|
| 1 | [voidborn-concurrent](voidborn-concurrent.json) | Once per Pilot | home space | once per pilot | one-time |
| 2 | [voidborn-substrate](voidborn-substrate.json) | Once per Pilot | home space | once per pilot, from 3,000 cr | one-time |
| 3 | [voidborn-missions-1](voidborn-missions-1.json) | Once per Pilot | home space | once per pilot, from 8,000 cr | one-time |
| 4 | [voidborn-mining-missions](voidborn-mining-missions.json) | Once per Pilot | home space | once per pilot, up to 40 ships | one-time |
| 5 | [voidborn-precedence](voidborn-precedence.json) | Once per Pilot | home space | once per pilot, up to 40 ships | one-time |
| 6 | [voidborn-first-hunt-nexus](voidborn-first-hunt-nexus.json) | Once per Pilot | home space | once per pilot, up to 1 ships | one-time |
| 7 | [voidborn-first-hunt-gsc](voidborn-first-hunt-gsc.json) | Once per Pilot | home space | once per pilot, up to 1 ships | one-time |
| 8 | [voidborn-first-hunt-acubens](voidborn-first-hunt-acubens.json) | Once per Pilot | home space | once per pilot, up to 1 ships | one-time |
| 9 | [mine-gsc-0050-gas-plume](mine-gsc-0050-gas-plume.json) | Measured at a Loss | beyond the border, 3 jumps | up to 1 ships, needs gas_harvester_i, empty hold | -220 |
| 10 | [fit-ice-harvester](fit-ice-harvester.json) | Fitting | home space | once per pilot, up to 1 ships, 15 pilots in all, without ice_harvester_i, from 6,000 cr | one-time |
| 11 | [fit-ice-harvester-node-beta](fit-ice-harvester-node-beta.json) | Fitting | home space | once per pilot, up to 1 ships, 2 pilots in all, without ice_harvester_i, from 6,000 cr | TBD |
| 12 | [fit-ice-harvester-node-gamma](fit-ice-harvester-node-gamma.json) | Fitting | home space | once per pilot, up to 1 ships, 2 pilots in all, without ice_harvester_i, from 6,000 cr | TBD |
| 13 | [fit-ice-harvester-synchrony](fit-ice-harvester-synchrony.json) | Fitting | home space | once per pilot, up to 1 ships, 4 pilots in all, without ice_harvester_i, from 6,000 cr | TBD |
| 14 | [fit-ice-harvester-experiment](fit-ice-harvester-experiment.json) | Fitting | home space | once per pilot, up to 1 ships, 2 pilots in all, without ice_harvester_i, from 6,000 cr | TBD |
| 15 | [fit-ice-harvester-lhs-1140](fit-ice-harvester-lhs-1140.json) | Fitting | beyond the border, 6 jumps | once per pilot, up to 1 ships, 1 pilots in all, without ice_harvester_i, empty hold, from 6,000 cr | TBD |
| 16 | [fit-gas-harvester](fit-gas-harvester.json) | Fitting | home space | once per pilot, up to 1 ships, 1 pilots in all, needs mining_laser_i, without ice_harvester_i, from 6,000 cr | one-time |
| 17 | [mine-wolf-1061-vent](mine-wolf-1061-vent.json) | Paying Routes | beyond the border, 4 jumps | up to 1 ships, needs nitrogen_vent, empty hold | 8,710 |
| 18 | [mine-ruchbah-ice-belt](mine-ruchbah-ice-belt.json) | Paying Routes | beyond the border, 4 jumps | up to 3 ships, needs ice_harvester_i, empty hold | 8,270 |
| 19 | [mine-achernar-frost-ring](mine-achernar-frost-ring.json) | Paying Routes | beyond the border, 4 jumps | up to 3 ships, needs ice_harvester_i, empty hold | 7,470 |
| 20 | [mine-cryogenic-reserve](mine-cryogenic-reserve.json) | Measured at a Loss | home space | up to 1 ships, needs ice_harvester_i | -350 |
| 21 | [mine-keid-ice-shelf](mine-keid-ice-shelf.json) | Paying Routes | beyond the border, 5 jumps | up to 2 ships, needs ice_harvester_i, empty hold | 2,990 |
| 22 | [mine-intercrus-ice-fields](mine-intercrus-ice-fields.json) | Paying Routes | beyond the border, 7 jumps | up to 2 ships, needs ice_harvester_i, empty hold | 2,460 |
| 23 | [mine-wolf-1061-frozen-drift](mine-wolf-1061-frozen-drift.json) | Paying Routes | beyond the border, 4 jumps | up to 2 ships, needs ice_harvester_i, empty hold | 4,430 |
| 24 | [mine-alnair-ice-fields](mine-alnair-ice-fields.json) | Paying Routes | beyond the border, 5 jumps | up to 2 ships, needs ice_harvester_i, empty hold | 4,430 |
| 25 | [mine-node-beta-frozen-drift](mine-node-beta-frozen-drift.json) | Paying Routes | home space | up to 1 ships, needs ice_harvester_i | 2,460 |
| 26 | [mine-gsc-0041-frost-ring](mine-gsc-0041-frost-ring.json) | Paying Routes | beyond the border, 4 jumps | up to 1 ships, needs ice_harvester_i, empty hold | 4,560 |
| 27 | [mine-antares-ice-fields](mine-antares-ice-fields.json) | Paying Routes | beyond the border, 5 jumps | up to 1 ships, needs ice_harvester_i, empty hold | 2,700 |
| 28 | [mine-wolf-1061-frozen-drift-nexus](mine-wolf-1061-frozen-drift-nexus.json) | Tests | beyond the border, 4 jumps | up to 1 ships, needs ice_harvester_i, empty hold | TBD |
| 29 | [mine-achernar-frost-ring-nexus](mine-achernar-frost-ring-nexus.json) | Tests | beyond the border, 4 jumps | up to 1 ships, needs ice_harvester_i, empty hold | TBD |
| 30 | [mine-gsc-0033-cryobelt](mine-gsc-0033-cryobelt.json) | Tests | beyond the border, 6 jumps | up to 1 ships, needs ice_harvester_i, empty hold | TBD |
| 31 | [mine-homam-cryobelt](mine-homam-cryobelt.json) | Tests | beyond the border, 6 jumps | up to 1 ships, needs ice_harvester_i, empty hold | TBD |
| 32 | [mine-tanglewood-frost-ring](mine-tanglewood-frost-ring.json) | Tests | beyond the border, 6 jumps | up to 1 ships, needs ice_harvester_i, empty hold | TBD |
| 33 | [mine-gsc-0021-ice-fields](mine-gsc-0021-ice-fields.json) | Tests | beyond the border, 6 jumps | up to 1 ships, needs ice_harvester_i, empty hold | TBD |
| 34 | [mission-cracking-the-shell-central](mission-cracking-the-shell-central.json) | Once per Pilot | home space | once per pilot, up to 1 ships | one-time |
| 35 | [census-frontier](census-frontier.json) | Reading and Waiting | beyond the border, 7 jumps | up to 12 ships, empty hold | -600 |
| 36 | [park](park.json) | Reading and Waiting | home space | the park route | -550 |

Planned:

| What | When |
|---|---|
| Read the RESULT line of fit-ice-harvester-lhs-1140 (price, fuel, minutes against 1,427 cr at home); if it fits for less, max_pilots up to the asks that stand there, one ship at a time | turn T10 (07:00 UTC) |
| Lift the ice routes where their field and their station's bid carry more ships (fill status prints the share of the bid); an ice route that sells at Central Nexus (deepest water-ice ladder, 1,513 units an hour regained) once the routes at The Experiment and Node Alpha fill their bids | turn T10 |
| The vent: a second vent run at Wolf 1061, and a Nitrogen Vent for every ice miner only when one is on offer and the second run holds the 83% water share | when a vent is on offer |
| The gas test: one more run of mine-gsc-0050-gas-plume; off when its two runs lose in sum (the dispatcher's loss stop) | turn T10 |

## scout

Kept by Oracle. Routes: 11.

| # | Route | Group | Zone | Open to | Credits per ship-hour |
|---|---|---|---|---|---|
| 1 | [census-voidborn](census-voidborn.json) | Reading and Waiting | home space | up to 3 ships | -550 |
| 2 | [voidborn-precedence](voidborn-precedence.json) | Once per Pilot | home space | once per pilot, up to 40 ships | one-time |
| 3 | [voidborn-selling](voidborn-selling.json) | Once per Pilot | home space | once per pilot, up to 10 ships | one-time |
| 4 | [voidborn-concurrent](voidborn-concurrent.json) | Once per Pilot | home space | once per pilot | one-time |
| 5 | [voidborn-substrate](voidborn-substrate.json) | Once per Pilot | home space | once per pilot, from 3,000 cr | one-time |
| 6 | [voidborn-missions-1](voidborn-missions-1.json) | Once per Pilot | home space | once per pilot, from 8,000 cr | one-time |
| 7 | [voidborn-mining-missions](voidborn-mining-missions.json) | Once per Pilot | home space | once per pilot, up to 40 ships | one-time |
| 8 | [hunt-test-atlas-halo-drifter](hunt-test-atlas-halo-drifter.json) | Tests | beyond the border, 6 jumps | up to 1 ships, empty hold | TBD |
| 9 | [hunt-test-nightveil-rivetshell](hunt-test-nightveil-rivetshell.json) | Tests | beyond the border, 5 jumps | up to 1 ships, empty hold | TBD |
| 10 | [census-frontier](census-frontier.json) | Reading and Waiting | beyond the border, 7 jumps | up to 12 ships, empty hold | -600 |
| 11 | [park](park.json) | Reading and Waiting | home space | the park route | -550 |

Planned:

| What | When |
|---|---|
| Keep every Voidborn system read within the hour: census-voidborn every_minutes 30, max_ships 3; read the gaps per system every turn and change the threshold only on a measured gap over 60 minutes | every turn |
| census-frontier: 42 systems every 240 minutes, 12 ships. Next ring after one refuel-beyond-the-border figure: acrab, acrux, botein, deepwell, felis, gliese_876, hd_147513, marfik, rastaban; not the pirate stronghold gliese_581 | turn T10 |
| Halo-drifter: after a second paying run, a hunt route at Atlas Gas Pocket for one scout, and the other halo-drifter places read for their herds; rivetshell: end the test unless its drop sells | next turn |
| First Hunt for the scouts that hold it unfinished: a route that hands it in where it was accepted, once the cause of the three failed far-herd runs is known (requests.log); Cracking the Shell (1,500 cr once, three pressblisters) after it | next turn |
| Nova Terra Central (Solarian) read once by one scout with an empty hold, then about once a day while Trade weighs a trade (requests.log ENT-073) | this turn, then daily |
| Read the game's changelog at every turn and name each line of game/rules/ a release makes wrong in a request to the Fleet Admiral | every turn |

## sentinel

Kept by Unity. Routes: 23.

| # | Route | Group | Zone | Open to | Credits per ship-hour |
|---|---|---|---|---|---|
| 1 | [voidborn-concurrent](voidborn-concurrent.json) | Once per Pilot | home space | once per pilot | one-time |
| 2 | [voidborn-substrate](voidborn-substrate.json) | Once per Pilot | home space | once per pilot, from 3,000 cr | one-time |
| 3 | [voidborn-missions-1](voidborn-missions-1.json) | Once per Pilot | home space | once per pilot, from 8,000 cr | one-time |
| 4 | [voidborn-mining-missions](voidborn-mining-missions.json) | Once per Pilot | home space | once per pilot, up to 40 ships | one-time |
| 5 | [voidborn-first-steps](voidborn-first-steps.json) | Once per Pilot | home space | once per pilot, up to 2 ships | one-time |
| 6 | [voidborn-selling](voidborn-selling.json) | Once per Pilot | home space | once per pilot, up to 10 ships | one-time |
| 7 | [voidborn-precedence](voidborn-precedence.json) | Once per Pilot | home space | once per pilot, up to 40 ships | one-time |
| 8 | [voidborn-first-hunt-nexus](voidborn-first-hunt-nexus.json) | Once per Pilot | home space | once per pilot, up to 1 ships | one-time |
| 9 | [voidborn-first-hunt-gsc](voidborn-first-hunt-gsc.json) | Once per Pilot | home space | once per pilot, up to 1 ships | one-time |
| 10 | [voidborn-first-hunt-acubens](voidborn-first-hunt-acubens.json) | Once per Pilot | home space | once per pilot, up to 1 ships | one-time |
| 11 | [fit-ice-harvester-guard](fit-ice-harvester-guard.json) | Fitting | home space | once per pilot, up to 4 ships, 8 pilots in all, without ice_harvester_i, from 6,000 cr | one-time |
| 12 | [mine-node-beta-frozen-drift](mine-node-beta-frozen-drift.json) | Paying Routes | home space | up to 1 ships, needs ice_harvester_i | 2,460 |
| 13 | [mine-ruchbah-ice-belt](mine-ruchbah-ice-belt.json) | Paying Routes | beyond the border, 4 jumps | up to 3 ships, needs ice_harvester_i, empty hold | 8,270 |
| 14 | [mine-achernar-frost-ring](mine-achernar-frost-ring.json) | Paying Routes | beyond the border, 4 jumps | up to 3 ships, needs ice_harvester_i, empty hold | 7,470 |
| 15 | [mine-wolf-1061-frozen-drift](mine-wolf-1061-frozen-drift.json) | Paying Routes | beyond the border, 4 jumps | up to 2 ships, needs ice_harvester_i, empty hold | 4,430 |
| 16 | [mine-keid-ice-shelf](mine-keid-ice-shelf.json) | Paying Routes | beyond the border, 5 jumps | up to 2 ships, needs ice_harvester_i, empty hold | 2,990 |
| 17 | [mine-cryogenic-reserve](mine-cryogenic-reserve.json) | Measured at a Loss | home space | up to 1 ships, needs ice_harvester_i | -350 |
| 18 | [mine-alnair-ice-fields](mine-alnair-ice-fields.json) | Paying Routes | beyond the border, 5 jumps | up to 2 ships, needs ice_harvester_i, empty hold | 4,430 |
| 19 | [mine-gsc-0041-frost-ring](mine-gsc-0041-frost-ring.json) | Paying Routes | beyond the border, 4 jumps | up to 1 ships, needs ice_harvester_i, empty hold | 4,560 |
| 20 | [mine-antares-ice-fields](mine-antares-ice-fields.json) | Paying Routes | beyond the border, 5 jumps | up to 1 ships, needs ice_harvester_i, empty hold | 2,700 |
| 21 | [mine-intercrus-ice-fields](mine-intercrus-ice-fields.json) | Paying Routes | beyond the border, 7 jumps | up to 2 ships, needs ice_harvester_i, empty hold | 2,460 |
| 22 | [census-frontier](census-frontier.json) | Reading and Waiting | beyond the border, 7 jumps | up to 12 ships, empty hold | -600 |
| 23 | [park](park.json) | Reading and Waiting | home space | the park route | -550 |

## trader

Kept by Mercury. Routes: 10.

| # | Route | Group | Zone | Open to | Credits per ship-hour |
|---|---|---|---|---|---|
| 1 | [voidborn-concurrent](voidborn-concurrent.json) | Once per Pilot | home space | once per pilot | one-time |
| 2 | [voidborn-substrate](voidborn-substrate.json) | Once per Pilot | home space | once per pilot, from 3,000 cr | one-time |
| 3 | [voidborn-missions-1](voidborn-missions-1.json) | Once per Pilot | home space | once per pilot, from 8,000 cr | one-time |
| 4 | [voidborn-mining-missions](voidborn-mining-missions.json) | Once per Pilot | home space | once per pilot, up to 40 ships | one-time |
| 5 | [voidborn-precedence](voidborn-precedence.json) | Once per Pilot | home space | once per pilot, up to 40 ships | one-time |
| 6 | [voidborn-conductive-lattice](voidborn-conductive-lattice.json) | Once per Pilot | beyond the border, 6 jumps | once per pilot, up to 6 ships, 30 pilots in all, empty hold, from 13,000 cr | one-time |
| 7 | [mine-stellar-siphon](mine-stellar-siphon.json) | Tests | home space | up to 1 ships, needs gas_harvester_i | TBD |
| 8 | [mine-lesath-gas-cloud](mine-lesath-gas-cloud.json) | Tests | beyond the border, 5 jumps | up to 1 ships, needs gas_harvester_i, empty hold | TBD |
| 9 | [census-frontier](census-frontier.json) | Reading and Waiting | beyond the border, 7 jumps | up to 12 ships, empty hold | -600 |
| 10 | [park](park.json) | Reading and Waiting | home space | the park route | -550 |

Planned:

| What | When |
|---|---|
| Read the first RESULT lines of mine-stellar-siphon and mine-lesath-gas-cloud; lift what pays as far as the Node Beta bids carry, take out what loses. | the turn of 2026-11-16 08:30 UTC (queue.log ENT-060) |
| Watch the silver ore ask at Ironlight Crossroads (ledger.py prices silver_ore) and raise max_pilots of voidborn-conductive-lattice as far as it refills; the chain pays +10,893 cr once per pilot. | every turn |
| Plasma gas from Ironlight Crossroads into the two station bids at Node Beta: judge the hand run; a route only with requires.bid (owed by Unity), since the bid is 37 units that regain on the station's clock. | after 2026-11-16 12:00 UTC |
| Control-node craft as a route when the runner's craft step exists, only where both ends show depth. | after 2026-11-16 12:00 UTC |

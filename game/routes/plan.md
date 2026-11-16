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
| 11 | [mine-node-beta-frozen-drift](mine-node-beta-frozen-drift.json) | Paying Routes | home space | up to 1 ships, needs ice_harvester_i | 1,980 |
| 12 | [mine-ruchbah-ice-belt](mine-ruchbah-ice-belt.json) | Paying Routes | beyond the border, 4 jumps | up to 6 ships, needs ice_harvester_i, empty hold | 8,600 |
| 13 | [mine-achernar-frost-ring](mine-achernar-frost-ring.json) | Paying Routes | beyond the border, 4 jumps | up to 5 ships, needs ice_harvester_i, empty hold | 7,300 |
| 14 | [mine-wolf-1061-frozen-drift](mine-wolf-1061-frozen-drift.json) | Paying Routes | beyond the border, 4 jumps | up to 2 ships, needs ice_harvester_i, empty hold | 4,970 |
| 15 | [mine-keid-ice-shelf](mine-keid-ice-shelf.json) | Paying Routes | beyond the border, 5 jumps | up to 2 ships, needs ice_harvester_i, empty hold | 2,640 |
| 16 | [mine-cryogenic-reserve](mine-cryogenic-reserve.json) | Measured at a Loss | home space | up to 1 ships, needs ice_harvester_i | -350 |
| 17 | [mine-alnair-ice-fields](mine-alnair-ice-fields.json) | Paying Routes | beyond the border, 5 jumps | up to 2 ships, needs ice_harvester_i, empty hold | 3,320 |
| 18 | [mine-gsc-0041-frost-ring](mine-gsc-0041-frost-ring.json) | Paying Routes | beyond the border, 4 jumps | up to 1 ships, needs ice_harvester_i, empty hold | 5,110 |
| 19 | [mine-antares-ice-fields](mine-antares-ice-fields.json) | Paying Routes | beyond the border, 5 jumps | up to 1 ships, needs ice_harvester_i, empty hold | 1,210 |
| 20 | [mine-intercrus-ice-fields](mine-intercrus-ice-fields.json) | Paying Routes | beyond the border, 7 jumps | up to 2 ships, needs ice_harvester_i, empty hold | 2,320 |
| 21 | [mission-cracking-the-shell-central](mission-cracking-the-shell-central.json) | Once per Pilot | home space | once per pilot, up to 1 ships | one-time |
| 22 | [census-frontier](census-frontier.json) | Reading and Waiting | beyond the border, 7 jumps | up to 12 ships, empty hold | -620 |
| 23 | [park](park.json) | Reading and Waiting | home space | the park route | -550 |

## drone

Kept by Apophis. Routes: 32.

| # | Route | Group | Zone | Open to | Credits per ship-hour |
|---|---|---|---|---|---|
| 1 | [voidborn-precedence](voidborn-precedence.json) | Once per Pilot | home space | once per pilot, up to 40 ships | one-time |
| 2 | [voidborn-first-hunt-nexus](voidborn-first-hunt-nexus.json) | Once per Pilot | home space | once per pilot, up to 1 ships | one-time |
| 3 | [voidborn-first-hunt-gsc](voidborn-first-hunt-gsc.json) | Once per Pilot | home space | once per pilot, up to 1 ships | one-time |
| 4 | [voidborn-first-hunt-acubens](voidborn-first-hunt-acubens.json) | Once per Pilot | home space | once per pilot, up to 1 ships | one-time |
| 5 | [voidborn-first-hunt-ironhollow-echo](voidborn-first-hunt-ironhollow-echo.json) | Once per Pilot | beyond the border, 4 jumps | once per pilot, up to 1 ships, empty hold | one-time |
| 6 | [voidborn-first-hunt-ironhollow-fading](voidborn-first-hunt-ironhollow-fading.json) | Once per Pilot | beyond the border, 4 jumps | once per pilot, up to 1 ships, empty hold | one-time |
| 7 | [voidborn-first-hunt-achernar](voidborn-first-hunt-achernar.json) | Once per Pilot | beyond the border, 4 jumps | once per pilot, up to 1 ships, empty hold | one-time |
| 8 | [voidborn-first-steps](voidborn-first-steps.json) | Once per Pilot | home space | once per pilot, up to 2 ships | one-time |
| 9 | [voidborn-selling](voidborn-selling.json) | Once per Pilot | home space | once per pilot, up to 10 ships | one-time |
| 10 | [voidborn-concurrent](voidborn-concurrent.json) | Once per Pilot | home space | once per pilot | one-time |
| 11 | [voidborn-substrate](voidborn-substrate.json) | Once per Pilot | home space | once per pilot, from 3,000 cr | one-time |
| 12 | [voidborn-missions-1](voidborn-missions-1.json) | Once per Pilot | home space | once per pilot, from 8,000 cr | one-time |
| 13 | [voidborn-mining-missions](voidborn-mining-missions.json) | Once per Pilot | home space | once per pilot, up to 40 ships | one-time |
| 14 | [hunt-test-achernar-cinder-sylph](hunt-test-achernar-cinder-sylph.json) | Paying Routes | beyond the border, 4 jumps | up to 1 ships, without piercing_railgun_i, empty hold | 2,060 |
| 15 | [hunt-faintlight-drift-veil-ray](hunt-faintlight-drift-veil-ray.json) | Paying Routes | beyond the border, 5 jumps | up to 1 ships, without piercing_railgun_i, empty hold | 1,360 |
| 16 | [hunt-gsc-veil-ray](hunt-gsc-veil-ray.json) | Paying Routes | home space | up to 1 ships, without piercing_railgun_i | 3,620 |
| 17 | [hunt-hamal-veil-ray](hunt-hamal-veil-ray.json) | Paying Routes | home space | up to 1 ships, without piercing_railgun_i | 2,890 |
| 18 | [hunt-ruchbah-veil-ray](hunt-ruchbah-veil-ray.json) | Paying Routes | beyond the border, 4 jumps | up to 1 ships, without piercing_railgun_i, empty hold | 2,950 |
| 19 | [hunt-keid-fractured-prism-veil-ray](hunt-keid-fractured-prism-veil-ray.json) | Paying Routes | beyond the border, 5 jumps | up to 1 ships, without piercing_railgun_i, empty hold | 1,540 |
| 20 | [hunt-low-charge-glint-veil-ray](hunt-low-charge-glint-veil-ray.json) | Paying Routes | beyond the border, 4 jumps | up to 1 ships, without piercing_railgun_i, empty hold | 1,330 |
| 21 | [hunt-cedarhold-dim-lattice-veil-ray](hunt-cedarhold-dim-lattice-veil-ray.json) | Paying Routes | beyond the border, 5 jumps | up to 1 ships, without piercing_railgun_i, empty hold | 900 |
| 22 | [hunt-dimming-pocket-veil-ray](hunt-dimming-pocket-veil-ray.json) | Paying Routes | beyond the border, 4 jumps | up to 1 ships, empty hold | 1,090 |
| 23 | [hunt-denebola-fractured-prism-veil-ray](hunt-denebola-fractured-prism-veil-ray.json) | Measured at a Loss | beyond the border, 5 jumps | up to 1 ships, empty hold | -10 |
| 24 | [hunt-test-lesath-cinder-sylph](hunt-test-lesath-cinder-sylph.json) | Paying Routes | beyond the border, 5 jumps | up to 1 ships, without piercing_railgun_i, empty hold | 2,930 |
| 25 | [hunt-test-gsc-0050-cinder-sylph](hunt-test-gsc-0050-cinder-sylph.json) | Measured at a Loss | beyond the border, 3 jumps | up to 1 ships, without piercing_railgun_i, empty hold | -540 |
| 26 | [hunt-test-atlas-patina-grazer](hunt-test-atlas-patina-grazer.json) | Measured at a Loss | beyond the border, 6 jumps | up to 1 ships, without piercing_railgun_i, empty hold | -340 |
| 27 | [hunt-test-garnet-slag-tortoise](hunt-test-garnet-slag-tortoise.json) | Measured at a Loss | beyond the border, 5 jumps | up to 1 ships, without piercing_railgun_i, empty hold | -630 |
| 28 | [hunt-test-goldcrest-glitterback-crab](hunt-test-goldcrest-glitterback-crab.json) | Measured at a Loss | beyond the border, 7 jumps | up to 1 ships, without piercing_railgun_i, empty hold | -600 |
| 29 | [hunt-test-tanglewood-hollow-pilgrim](hunt-test-tanglewood-hollow-pilgrim.json) | Measured at a Loss | beyond the border, 6 jumps | up to 1 ships, without piercing_railgun_i, empty hold | -50 |
| 30 | [voidborn-first-hunt-schedar](voidborn-first-hunt-schedar.json) | Once per Pilot | beyond the border, 2 jumps | once per pilot, up to 1 ships, empty hold | one-time |
| 31 | [census-frontier](census-frontier.json) | Reading and Waiting | beyond the border, 7 jumps | up to 12 ships, empty hold | -620 |
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

Kept by Apollo. Routes: 18.

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
| 9 | [hunt-dimming-pocket-veil-ray](hunt-dimming-pocket-veil-ray.json) | Paying Routes | beyond the border, 4 jumps | up to 1 ships, empty hold | 1,090 |
| 10 | [fit-gas-harvester-hauler](fit-gas-harvester-hauler.json) | Fitting | home space | once per pilot, up to 1 ships, 1 pilots in all, needs mining_laser_i, without gas_harvester_i, from 6,000 cr | one-time |
| 11 | [mine-achernar-gas-pocket](mine-achernar-gas-pocket.json) | Measured at a Loss | beyond the border, 4 jumps | up to 1 ships, needs gas_harvester_i, empty hold | -300 |
| 12 | [voidborn-first-hunt-acubens](voidborn-first-hunt-acubens.json) | Once per Pilot | home space | once per pilot, up to 1 ships | one-time |
| 13 | [voidborn-first-hunt-gsc](voidborn-first-hunt-gsc.json) | Once per Pilot | home space | once per pilot, up to 1 ships | one-time |
| 14 | [voidborn-first-hunt-schedar](voidborn-first-hunt-schedar.json) | Once per Pilot | beyond the border, 2 jumps | once per pilot, up to 1 ships, empty hold | one-time |
| 15 | [voidborn-first-hunt-achernar](voidborn-first-hunt-achernar.json) | Once per Pilot | beyond the border, 4 jumps | once per pilot, up to 1 ships, empty hold | one-time |
| 16 | [voidborn-first-hunt-gsc-0031](voidborn-first-hunt-gsc-0031.json) | Once per Pilot | beyond the border, 5 jumps | once per pilot, up to 1 ships, empty hold | one-time |
| 17 | [census-frontier](census-frontier.json) | Reading and Waiting | beyond the border, 7 jumps | up to 12 ships, empty hold | -620 |
| 18 | [park](park.json) | Reading and Waiting | home space | the park route | -550 |

Planned:

| What | When |
|---|---|
| A route that sells stored neural soma from storage at Synchrony Hub and Node Beta into station bids of 600 cr or more, sent only while such a bid stands (requests.log ENT-065); until then by hand with one hauler when a bid is read | after 2026-11-16 12:00 UTC |
| First Steps in the Void for the 14 haulers that still hold it, once game/routes/voidborn-first-steps.json is on again (requests.log ENT-064); the Acubens belt refills its carbon | turn T7 and T8 |
| voidborn-first-hunt-gsc and voidborn-first-hunt-acubens into the plan when their first RESULT lines are read | turn T8 |
| A craft-and-sell route for stored ore once the circuit runner has its craft step (requests.log ENT-013), only where the depth at the best bid (best_buy_qty, read live with view_market) pays the fuel | after 2026-11-16 12:00 UTC |
| Steel plate for a faction lockbox from stored iron at the free workshop (10 ore a plate), when the Fleet Admiral names the builder and the station (guidebook logistics.md, section 8) | on the Fleet Admiral's word |

## miner

Kept by Zero. Routes: 34.

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
| 9 | [fit-ice-harvester](fit-ice-harvester.json) | Fitting | home space | once per pilot, up to 1 ships, 15 pilots in all, without ice_harvester_i, from 6,000 cr | one-time |
| 10 | [fit-ice-harvester-node-beta](fit-ice-harvester-node-beta.json) | Fitting | home space | once per pilot, up to 1 ships, 2 pilots in all, without ice_harvester_i, from 6,000 cr | one-time |
| 11 | [fit-ice-harvester-node-gamma](fit-ice-harvester-node-gamma.json) | Fitting | home space | once per pilot, up to 1 ships, 2 pilots in all, without ice_harvester_i, from 6,000 cr | one-time |
| 12 | [fit-ice-harvester-synchrony](fit-ice-harvester-synchrony.json) | Fitting | home space | once per pilot, up to 1 ships, 4 pilots in all, without ice_harvester_i, from 6,000 cr | one-time |
| 13 | [fit-ice-harvester-experiment](fit-ice-harvester-experiment.json) | Fitting | home space | once per pilot, up to 1 ships, 2 pilots in all, without ice_harvester_i, from 6,000 cr | one-time |
| 14 | [fit-ice-harvester-lhs-1140](fit-ice-harvester-lhs-1140.json) | Fitting | beyond the border, 6 jumps | once per pilot, up to 5 ships, 19 pilots in all, without ice_harvester_i, empty hold, from 6,000 cr | one-time |
| 15 | [mine-wolf-1061-vent](mine-wolf-1061-vent.json) | Paying Routes | beyond the border, 4 jumps | up to 1 ships, needs nitrogen_vent, empty hold | 6,830 |
| 16 | [mine-ruchbah-ice-belt](mine-ruchbah-ice-belt.json) | Paying Routes | beyond the border, 4 jumps | up to 6 ships, needs ice_harvester_i, empty hold | 8,600 |
| 17 | [mine-achernar-frost-ring](mine-achernar-frost-ring.json) | Paying Routes | beyond the border, 4 jumps | up to 5 ships, needs ice_harvester_i, empty hold | 7,300 |
| 18 | [mine-cryogenic-reserve](mine-cryogenic-reserve.json) | Measured at a Loss | home space | up to 1 ships, needs ice_harvester_i | -350 |
| 19 | [mine-keid-ice-shelf](mine-keid-ice-shelf.json) | Paying Routes | beyond the border, 5 jumps | up to 2 ships, needs ice_harvester_i, empty hold | 2,640 |
| 20 | [mine-intercrus-ice-fields](mine-intercrus-ice-fields.json) | Paying Routes | beyond the border, 7 jumps | up to 2 ships, needs ice_harvester_i, empty hold | 2,320 |
| 21 | [mine-wolf-1061-frozen-drift](mine-wolf-1061-frozen-drift.json) | Paying Routes | beyond the border, 4 jumps | up to 2 ships, needs ice_harvester_i, empty hold | 4,970 |
| 22 | [mine-alnair-ice-fields](mine-alnair-ice-fields.json) | Paying Routes | beyond the border, 5 jumps | up to 2 ships, needs ice_harvester_i, empty hold | 3,320 |
| 23 | [mine-node-beta-frozen-drift](mine-node-beta-frozen-drift.json) | Paying Routes | home space | up to 1 ships, needs ice_harvester_i | 1,980 |
| 24 | [mine-gsc-0041-frost-ring](mine-gsc-0041-frost-ring.json) | Paying Routes | beyond the border, 4 jumps | up to 1 ships, needs ice_harvester_i, empty hold | 5,110 |
| 25 | [mine-antares-ice-fields](mine-antares-ice-fields.json) | Paying Routes | beyond the border, 5 jumps | up to 1 ships, needs ice_harvester_i, empty hold | 1,210 |
| 26 | [mine-wolf-1061-frozen-drift-nexus](mine-wolf-1061-frozen-drift-nexus.json) | Measured at a Loss | beyond the border, 4 jumps | up to 1 ships, needs ice_harvester_i, empty hold | -310 |
| 27 | [mine-achernar-frost-ring-nexus](mine-achernar-frost-ring-nexus.json) | Measured at a Loss | beyond the border, 4 jumps | up to 1 ships, needs ice_harvester_i, empty hold | -320 |
| 28 | [mine-alnair-ice-fields-nexus](mine-alnair-ice-fields-nexus.json) | Tests | beyond the border, 5 jumps | up to 1 ships, needs ice_harvester_i, empty hold | TBD |
| 29 | [mine-gsc-0033-cryobelt](mine-gsc-0033-cryobelt.json) | Measured at a Loss | beyond the border, 6 jumps | up to 1 ships, needs ice_harvester_i, empty hold | -360 |
| 30 | [mine-homam-cryobelt](mine-homam-cryobelt.json) | Measured at a Loss | beyond the border, 6 jumps | up to 1 ships, needs ice_harvester_i, empty hold | -390 |
| 31 | [mine-tanglewood-frost-ring](mine-tanglewood-frost-ring.json) | Measured at a Loss | beyond the border, 6 jumps | up to 1 ships, needs ice_harvester_i, empty hold | -500 |
| 32 | [mine-gsc-0021-ice-fields](mine-gsc-0021-ice-fields.json) | Measured at a Loss | beyond the border, 6 jumps | up to 1 ships, needs ice_harvester_i, empty hold | -410 |
| 33 | [census-frontier](census-frontier.json) | Reading and Waiting | beyond the border, 7 jumps | up to 12 ships, empty hold | -620 |
| 34 | [park](park.json) | Reading and Waiting | home space | the park route | -550 |

Planned:

| What | When |
|---|---|
| Read the RESULT lines of the Central Nexus tests (Wolf 1061 Frozen Drift, Achernar, Alnair) and lift each that pays as far as the Central Nexus bid carries (48,298 units at 24 cr at 04:00 UTC); the miners fitted at Ironlight Crossroads need about 18 places | turn of 2026-11-16 08:00 UTC |
| Read the RESULT lines of the four ice tests that sell at Synchrony (GSC-0033, Homam, Tanglewood, GSC-0021) and of the gas test; drop what loses | turn of 2026-11-16 08:00 UTC |
| Hand 30 silicon ore and 35 energy crystal from three miners' storage at Central Nexus to the Logistics hauler that makes harvesters (requests.log, answer to ENT-088) | by 2026-11-16 08:00 UTC |

## scout

Kept by Oracle. Routes: 13.

| # | Route | Group | Zone | Open to | Credits per ship-hour |
|---|---|---|---|---|---|
| 1 | [census-voidborn](census-voidborn.json) | Reading and Waiting | home space | up to 3 ships | -550 |
| 2 | [voidborn-precedence](voidborn-precedence.json) | Once per Pilot | home space | once per pilot, up to 40 ships | one-time |
| 3 | [voidborn-selling](voidborn-selling.json) | Once per Pilot | home space | once per pilot, up to 10 ships | one-time |
| 4 | [voidborn-concurrent](voidborn-concurrent.json) | Once per Pilot | home space | once per pilot | one-time |
| 5 | [voidborn-substrate](voidborn-substrate.json) | Once per Pilot | home space | once per pilot, from 3,000 cr | one-time |
| 6 | [voidborn-missions-1](voidborn-missions-1.json) | Once per Pilot | home space | once per pilot, from 8,000 cr | one-time |
| 7 | [voidborn-mining-missions](voidborn-mining-missions.json) | Once per Pilot | home space | once per pilot, up to 40 ships | one-time |
| 8 | [voidborn-first-steps](voidborn-first-steps.json) | Once per Pilot | home space | once per pilot, up to 2 ships | one-time |
| 9 | [voidborn-conductive-lattice](voidborn-conductive-lattice.json) | Once per Pilot | beyond the border, 6 jumps | once per pilot, up to 6 ships, 30 pilots in all, empty hold, from 13,000 cr | one-time |
| 10 | [hunt-atlas-gas-pocket](hunt-atlas-gas-pocket.json) | Paying Routes | beyond the border, 6 jumps | up to 1 ships, empty hold | 2,690 |
| 11 | [hunt-test-homam-frost-moth](hunt-test-homam-frost-moth.json) | Measured at a Loss | beyond the border, 6 jumps | up to 1 ships, empty hold | -610 |
| 12 | [census-frontier](census-frontier.json) | Reading and Waiting | beyond the border, 7 jumps | up to 12 ships, empty hold | -620 |
| 13 | [park](park.json) | Reading and Waiting | home space | the park route | -550 |

Planned:

| What | When |
|---|---|
| Keep every Voidborn system read within the hour: census-voidborn every_minutes 30, max_ships 3; read the gaps per system every turn and change the threshold only on a measured gap over 60 minutes | every turn |
| census-frontier: 42 systems every 240 minutes, 12 ships. Next ring: acrab, acrux, botein, deepwell, felis, gliese_876, hd_147513, marfik, rastaban; not the pirate stronghold gliese_581 | when a scout waits for reading work and the ring's bases or herds are worth a read |
| First Hunt for the six scouts that hold it unfinished (any asteroid belt): a route once the hunt step names why a run ended (requests.log ENT-092); Cracking the Shell after it, once requires.booked exists | after Unity's answer |
| hunt-atlas-gas-pocket: read its runs; if the herd regrows faster than 2 kills a run, the other halo-drifter places (GSC-0038, GSC-0016) as routes of their own | next turn |
| Nova Terra Central (Solarian) read about once a day while Trade weighs a trade | daily |
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
| 12 | [mine-node-beta-frozen-drift](mine-node-beta-frozen-drift.json) | Paying Routes | home space | up to 1 ships, needs ice_harvester_i | 1,980 |
| 13 | [mine-ruchbah-ice-belt](mine-ruchbah-ice-belt.json) | Paying Routes | beyond the border, 4 jumps | up to 6 ships, needs ice_harvester_i, empty hold | 8,600 |
| 14 | [mine-achernar-frost-ring](mine-achernar-frost-ring.json) | Paying Routes | beyond the border, 4 jumps | up to 5 ships, needs ice_harvester_i, empty hold | 7,300 |
| 15 | [mine-wolf-1061-frozen-drift](mine-wolf-1061-frozen-drift.json) | Paying Routes | beyond the border, 4 jumps | up to 2 ships, needs ice_harvester_i, empty hold | 4,970 |
| 16 | [mine-keid-ice-shelf](mine-keid-ice-shelf.json) | Paying Routes | beyond the border, 5 jumps | up to 2 ships, needs ice_harvester_i, empty hold | 2,640 |
| 17 | [mine-cryogenic-reserve](mine-cryogenic-reserve.json) | Measured at a Loss | home space | up to 1 ships, needs ice_harvester_i | -350 |
| 18 | [mine-alnair-ice-fields](mine-alnair-ice-fields.json) | Paying Routes | beyond the border, 5 jumps | up to 2 ships, needs ice_harvester_i, empty hold | 3,320 |
| 19 | [mine-gsc-0041-frost-ring](mine-gsc-0041-frost-ring.json) | Paying Routes | beyond the border, 4 jumps | up to 1 ships, needs ice_harvester_i, empty hold | 5,110 |
| 20 | [mine-antares-ice-fields](mine-antares-ice-fields.json) | Paying Routes | beyond the border, 5 jumps | up to 1 ships, needs ice_harvester_i, empty hold | 1,210 |
| 21 | [mine-intercrus-ice-fields](mine-intercrus-ice-fields.json) | Paying Routes | beyond the border, 7 jumps | up to 2 ships, needs ice_harvester_i, empty hold | 2,320 |
| 22 | [census-frontier](census-frontier.json) | Reading and Waiting | beyond the border, 7 jumps | up to 12 ships, empty hold | -620 |
| 23 | [park](park.json) | Reading and Waiting | home space | the park route | -550 |

## trader

Kept by Mercury. Routes: 10.

| # | Route | Group | Zone | Open to | Credits per ship-hour |
|---|---|---|---|---|---|
| 1 | [voidborn-signal-fragments](voidborn-signal-fragments.json) | Once per Pilot | home space | once per pilot, up to 3 ships | TBD |
| 2 | [voidborn-first-steps](voidborn-first-steps.json) | Once per Pilot | home space | once per pilot, up to 2 ships | one-time |
| 3 | [voidborn-concurrent](voidborn-concurrent.json) | Once per Pilot | home space | once per pilot | one-time |
| 4 | [voidborn-substrate](voidborn-substrate.json) | Once per Pilot | home space | once per pilot, from 3,000 cr | one-time |
| 5 | [voidborn-missions-1](voidborn-missions-1.json) | Once per Pilot | home space | once per pilot, from 8,000 cr | one-time |
| 6 | [voidborn-mining-missions](voidborn-mining-missions.json) | Once per Pilot | home space | once per pilot, up to 40 ships | one-time |
| 7 | [voidborn-precedence](voidborn-precedence.json) | Once per Pilot | home space | once per pilot, up to 40 ships | one-time |
| 8 | [voidborn-conductive-lattice](voidborn-conductive-lattice.json) | Once per Pilot | beyond the border, 6 jumps | once per pilot, up to 6 ships, 30 pilots in all, empty hold, from 13,000 cr | one-time |
| 9 | [census-frontier](census-frontier.json) | Reading and Waiting | beyond the border, 7 jumps | up to 12 ships, empty hold | -620 |
| 10 | [park](park.json) | Reading and Waiting | home space | the park route | -550 |

Planned:

| What | When |
|---|---|
| Read the first RESULT lines of mine-stellar-siphon and mine-lesath-gas-cloud; lift what pays as far as the Node Beta bids carry, take out what loses. | the turn of 2026-11-16 08:30 UTC (queue.log ENT-060) |
| Watch the silver ore ask at Ironlight Crossroads (ledger.py prices silver_ore) and raise max_pilots of voidborn-conductive-lattice as far as it refills; the chain pays +10,893 cr once per pilot. | every turn |
| Plasma gas from Ironlight Crossroads into the two station bids at Node Beta: judge the hand run; a route only with requires.bid (owed by Unity), since the bid is 37 units that regain on the station's clock. | after 2026-11-16 12:00 UTC |
| Control-node craft as a route when the runner's craft step exists, only where both ends show depth. | after 2026-11-16 12:00 UTC |

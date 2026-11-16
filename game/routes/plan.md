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

Kept by Unity. Routes: 28.

| # | Route | Group | Zone | Open to | Credits per ship-hour |
|---|---|---|---|---|---|
| 1 | [voidborn-signal-fragments](voidborn-signal-fragments.json) | Once per Pilot | home space | once per pilot, up to 3 ships, from navigation 3 | one-time |
| 2 | [voidborn-concurrent](voidborn-concurrent.json) | Once per Pilot | home space | once per pilot | one-time |
| 3 | [voidborn-substrate](voidborn-substrate.json) | Once per Pilot | home space | once per pilot, from 3,000 cr | one-time |
| 4 | [voidborn-missions-1](voidborn-missions-1.json) | Once per Pilot | home space | once per pilot, from 8,000 cr | one-time |
| 5 | [voidborn-mining-missions](voidborn-mining-missions.json) | Once per Pilot | home space | once per pilot, up to 40 ships | one-time |
| 6 | [voidborn-first-steps](voidborn-first-steps.json) | Once per Pilot | home space | once per pilot, up to 2 ships | one-time |
| 7 | [voidborn-selling](voidborn-selling.json) | Once per Pilot | home space | once per pilot, up to 10 ships | one-time |
| 8 | [voidborn-precedence](voidborn-precedence.json) | Once per Pilot | home space | once per pilot, up to 40 ships | one-time |
| 9 | [voidborn-first-hunt-nexus](voidborn-first-hunt-nexus.json) | Once per Pilot | home space | once per pilot, up to 1 ships | one-time |
| 10 | [voidborn-first-hunt-gsc](voidborn-first-hunt-gsc.json) | Once per Pilot | home space | once per pilot, up to 1 ships | one-time |
| 11 | [voidborn-first-hunt-acubens](voidborn-first-hunt-acubens.json) | Once per Pilot | home space | once per pilot, up to 1 ships | one-time |
| 12 | [mine-node-beta-frozen-drift](mine-node-beta-frozen-drift.json) | Paying Routes | home space | up to 1 ships, needs ice_harvester_i | 1,480 |
| 13 | [mine-ruchbah-ice-belt](mine-ruchbah-ice-belt.json) | Paying Routes | beyond the border, 4 jumps | up to 1 ships, needs ice_harvester_i, empty hold | 7,430 |
| 14 | [mine-achernar-frost-ring](mine-achernar-frost-ring.json) | Paying Routes | beyond the border, 4 jumps | up to 1 ships, needs ice_harvester_i, empty hold | 5,830 |
| 15 | [mine-wolf-1061-frozen-drift](mine-wolf-1061-frozen-drift.json) | Paying Routes | beyond the border, 4 jumps | up to 1 ships, needs ice_harvester_i, empty hold | 2,580 |
| 16 | [mine-keid-ice-shelf](mine-keid-ice-shelf.json) | Paying Routes | beyond the border, 5 jumps | up to 2 ships, needs ice_harvester_i, empty hold | 1,380 |
| 17 | [mine-cryogenic-reserve](mine-cryogenic-reserve.json) | Measured at a Loss | home space | up to 1 ships, needs ice_harvester_i | -340 |
| 18 | [mine-alnair-ice-fields](mine-alnair-ice-fields.json) | Paying Routes | beyond the border, 5 jumps | up to 1 ships, needs ice_harvester_i, empty hold | 840 |
| 19 | [mine-gsc-0041-frost-ring](mine-gsc-0041-frost-ring.json) | Paying Routes | beyond the border, 4 jumps | up to 1 ships, needs ice_harvester_i, empty hold | 2,080 |
| 20 | [mine-antares-ice-fields](mine-antares-ice-fields.json) | Paying Routes | beyond the border, 5 jumps | up to 1 ships, needs ice_harvester_i, empty hold | 350 |
| 21 | [mine-intercrus-ice-fields](mine-intercrus-ice-fields.json) | Paying Routes | beyond the border, 7 jumps | up to 2 ships, needs ice_harvester_i, empty hold | 880 |
| 22 | [mission-cracking-the-shell-central](mission-cracking-the-shell-central.json) | Once per Pilot | beyond the border, 5 jumps | once per pilot, up to 1 ships, empty hold, after the reward First Hunt: Belt-Grazers | one-time |
| 23 | [hunt-deepwell-volatile-ice-frost-moth](hunt-deepwell-volatile-ice-frost-moth.json) | Paying Routes | beyond the border, 7 jumps | up to 1 ships, empty hold | 3,680 |
| 24 | [hunt-deepwell-haze-cinder-sylph](hunt-deepwell-haze-cinder-sylph.json) | Measured at a Loss | beyond the border, 7 jumps | up to 1 ships, empty hold | -370 |
| 25 | [hunt-raysheet-nebula-veil-ray](hunt-raysheet-nebula-veil-ray.json) | Measured at a Loss | beyond the border, 8 jumps | up to 1 ships, empty hold | -860 |
| 26 | [mine-gsc-0049-platinum-group-reef](mine-gsc-0049-platinum-group-reef.json) | Tests | beyond the border, 5 jumps | up to 1 ships, empty hold | TBD |
| 27 | [census-frontier](census-frontier.json) | Reading and Waiting | beyond the border, 7 jumps | up to 12 ships, empty hold | -620 |
| 28 | [park](park.json) | Reading and Waiting | home space | the park route | -670 |

## drone

Kept by Apophis. Routes: 26.

| # | Route | Group | Zone | Open to | Credits per ship-hour |
|---|---|---|---|---|---|
| 1 | [voidborn-precedence](voidborn-precedence.json) | Once per Pilot | home space | once per pilot, up to 40 ships | one-time |
| 2 | [voidborn-conductive-lattice](voidborn-conductive-lattice.json) | Once per Pilot | beyond the border, 6 jumps | once per pilot, up to 10 ships, 146 pilots in all, empty hold, from 13,000 cr | one-time |
| 3 | [voidborn-first-hunt-nexus](voidborn-first-hunt-nexus.json) | Once per Pilot | home space | once per pilot, up to 1 ships | one-time |
| 4 | [voidborn-first-hunt-gsc](voidborn-first-hunt-gsc.json) | Once per Pilot | home space | once per pilot, up to 1 ships | one-time |
| 5 | [voidborn-first-hunt-achernar](voidborn-first-hunt-achernar.json) | Once per Pilot | beyond the border, 4 jumps | once per pilot, up to 1 ships, empty hold | one-time |
| 6 | [mission-cracking-the-shell-achernar](mission-cracking-the-shell-achernar.json) | Once per Pilot | beyond the border, 4 jumps | once per pilot, up to 1 ships, empty hold, after the reward First Hunt: Belt-Grazers | one-time |
| 7 | [mission-cracking-the-shell-central](mission-cracking-the-shell-central.json) | Once per Pilot | beyond the border, 5 jumps | once per pilot, up to 1 ships, empty hold, after the reward First Hunt: Belt-Grazers | one-time |
| 8 | [voidborn-first-steps](voidborn-first-steps.json) | Once per Pilot | home space | once per pilot, up to 2 ships | one-time |
| 9 | [voidborn-selling](voidborn-selling.json) | Once per Pilot | home space | once per pilot, up to 10 ships | one-time |
| 10 | [voidborn-concurrent](voidborn-concurrent.json) | Once per Pilot | home space | once per pilot | one-time |
| 11 | [voidborn-substrate](voidborn-substrate.json) | Once per Pilot | home space | once per pilot, from 3,000 cr | one-time |
| 12 | [voidborn-missions-1](voidborn-missions-1.json) | Once per Pilot | home space | once per pilot, from 8,000 cr | one-time |
| 13 | [voidborn-mining-missions](voidborn-mining-missions.json) | Once per Pilot | home space | once per pilot, up to 40 ships | one-time |
| 14 | [hunt-test-achernar-cinder-sylph](hunt-test-achernar-cinder-sylph.json) | Paying Routes | beyond the border, 4 jumps | up to 1 ships, without piercing_railgun_i, empty hold | 5,380 |
| 15 | [hunt-test-lesath-cinder-sylph](hunt-test-lesath-cinder-sylph.json) | Paying Routes | beyond the border, 5 jumps | up to 1 ships, without piercing_railgun_i, empty hold | 1,490 |
| 16 | [hunt-gsc-veil-ray](hunt-gsc-veil-ray.json) | Paying Routes | home space | up to 1 ships, without piercing_railgun_i | 3,020 |
| 17 | [hunt-hamal-veil-ray](hunt-hamal-veil-ray.json) | Paying Routes | home space | up to 1 ships, without piercing_railgun_i | 2,310 |
| 18 | [hunt-ruchbah-veil-ray](hunt-ruchbah-veil-ray.json) | Paying Routes | beyond the border, 4 jumps | up to 1 ships, without piercing_railgun_i, empty hold | 2,100 |
| 19 | [hunt-faintlight-drift-veil-ray](hunt-faintlight-drift-veil-ray.json) | Paying Routes | beyond the border, 5 jumps | up to 1 ships, without piercing_railgun_i, empty hold | 1,300 |
| 20 | [hunt-keid-fractured-prism-veil-ray](hunt-keid-fractured-prism-veil-ray.json) | Paying Routes | beyond the border, 5 jumps | up to 1 ships, without piercing_railgun_i, empty hold | 1,850 |
| 21 | [hunt-low-charge-glint-veil-ray](hunt-low-charge-glint-veil-ray.json) | Paying Routes | beyond the border, 4 jumps | up to 1 ships, without piercing_railgun_i, empty hold | 1,060 |
| 22 | [hunt-cedarhold-dim-lattice-veil-ray](hunt-cedarhold-dim-lattice-veil-ray.json) | Paying Routes | beyond the border, 5 jumps | up to 1 ships, without piercing_railgun_i, empty hold | 900 |
| 23 | [voidborn-first-hunt-schedar](voidborn-first-hunt-schedar.json) | Once per Pilot | beyond the border, 2 jumps | once per pilot, up to 1 ships, empty hold | one-time |
| 24 | [census-guard-ice](census-guard-ice.json) | Reading and Waiting | beyond the border, 7 jumps | up to 2 ships, empty hold | -610 |
| 25 | [census-frontier](census-frontier.json) | Reading and Waiting | beyond the border, 7 jumps | up to 12 ships, empty hold | -620 |
| 26 | [park](park.json) | Reading and Waiting | home space | the park route | -670 |

Planned:

| What | When |
|---|---|
| Read the first drone RESULT lines of voidborn-conductive-lattice and mission-cracking-the-shell-achernar; drop either at its first failure. | next turn, 2026-11-16 09:00 UTC |
| Measure census-guard-ice: its fuel per hour against what its reads renew (herd counts of the hunts at Ruchbah, Achernar and Keid, pilots met beside our miners). | next turn |
| Guard: the route kind guard (owed by Unity, requests.log ENT-070) replaces census-guard-ice with one drone standing beside each mine route beyond the border. | when the guard kind exists |
| Cinder-sylph herds: the drop is an ember gland on some kills only (4 kills, 2 glands at Achernar); a third run at Achernar and Lesath settles the figure. | next turn |
| The next hull: no purchase while every hunt is bounded by its herd; a tier-1 Vigil as one test only for prey over 100 hull, which needs an order beyond F9. | on an order |

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
| 9 | [hunt-dimming-pocket-veil-ray](hunt-dimming-pocket-veil-ray.json) | Paying Routes | beyond the border, 4 jumps | up to 1 ships, empty hold | 150 |
| 10 | [fit-gas-harvester-hauler](fit-gas-harvester-hauler.json) | Fitting | home space | once per pilot, up to 1 ships, 1 pilots in all, needs mining_laser_i, without gas_harvester_i, from 6,000 cr | one-time |
| 11 | [mine-achernar-gas-pocket](mine-achernar-gas-pocket.json) | Measured at a Loss | beyond the border, 4 jumps | up to 1 ships, needs gas_harvester_i, empty hold | -340 |
| 12 | [voidborn-first-hunt-acubens](voidborn-first-hunt-acubens.json) | Once per Pilot | home space | once per pilot, up to 1 ships | one-time |
| 13 | [voidborn-first-hunt-gsc](voidborn-first-hunt-gsc.json) | Once per Pilot | home space | once per pilot, up to 1 ships | one-time |
| 14 | [voidborn-first-hunt-schedar](voidborn-first-hunt-schedar.json) | Once per Pilot | beyond the border, 2 jumps | once per pilot, up to 1 ships, empty hold | one-time |
| 15 | [voidborn-first-hunt-achernar](voidborn-first-hunt-achernar.json) | Once per Pilot | beyond the border, 4 jumps | once per pilot, up to 1 ships, empty hold | one-time |
| 16 | [voidborn-first-hunt-gsc-0031](voidborn-first-hunt-gsc-0031.json) | Once per Pilot | beyond the border, 5 jumps | once per pilot, up to 1 ships, empty hold | one-time |
| 17 | [census-frontier](census-frontier.json) | Reading and Waiting | beyond the border, 7 jumps | up to 12 ships, empty hold | -620 |
| 18 | [park](park.json) | Reading and Waiting | home space | the park route | -670 |

Planned:

| What | When |
|---|---|
| Make about ten Ice Harvester I at the Central Nexus workshop from the staged goods (guidebook logistics.md, section 11) when Mining's silicon ore and energy crystal land (requests.log ENT-094); fit them where Zero names (ENT-108), and fit the one made before for the ice route Zero names (ENT-093) | turn of 2026-11-16 08:45 UTC |
| A route that crafts carapace into armor plate where it is stored and sells into the 233 to 380 cr station pools, and one that sells stored soma, both sent only while a bid stands (requests.log ENT-065: craft step, sale from storage, requires.bid); until then by hand where a hauler stands | after 2026-11-16 12:00 UTC |
| mine-achernar-gas-pocket: read its second RESULT line (the first with the runner's dock fix); out of the plan if it loses | turn of 2026-11-16 08:45 UTC |
| Steel plate for a faction lockbox from stored iron at the free workshop (10 ore a plate), when the Fleet Admiral names the builder and the station (guidebook logistics.md, section 8) | on the Fleet Admiral's word |

## miner

Kept by Zero. Routes: 29.

| # | Route | Group | Zone | Open to | Credits per ship-hour |
|---|---|---|---|---|---|
| 1 | [voidborn-signal-fragments](voidborn-signal-fragments.json) | Once per Pilot | home space | once per pilot, up to 3 ships, from navigation 3 | one-time |
| 2 | [voidborn-concurrent](voidborn-concurrent.json) | Once per Pilot | home space | once per pilot | one-time |
| 3 | [voidborn-substrate](voidborn-substrate.json) | Once per Pilot | home space | once per pilot, from 3,000 cr | one-time |
| 4 | [voidborn-missions-1](voidborn-missions-1.json) | Once per Pilot | home space | once per pilot, from 8,000 cr | one-time |
| 5 | [voidborn-mining-missions](voidborn-mining-missions.json) | Once per Pilot | home space | once per pilot, up to 40 ships | one-time |
| 6 | [voidborn-precedence](voidborn-precedence.json) | Once per Pilot | home space | once per pilot, up to 40 ships | one-time |
| 7 | [voidborn-conductive-lattice](voidborn-conductive-lattice.json) | Once per Pilot | beyond the border, 6 jumps | once per pilot, up to 10 ships, 146 pilots in all, empty hold, from 13,000 cr | one-time |
| 8 | [voidborn-first-steps](voidborn-first-steps.json) | Once per Pilot | home space | once per pilot, up to 2 ships | one-time |
| 9 | [voidborn-first-hunt-nexus](voidborn-first-hunt-nexus.json) | Once per Pilot | home space | once per pilot, up to 1 ships | one-time |
| 10 | [voidborn-first-hunt-gsc](voidborn-first-hunt-gsc.json) | Once per Pilot | home space | once per pilot, up to 1 ships | one-time |
| 11 | [voidborn-first-hunt-gsc-0031](voidborn-first-hunt-gsc-0031.json) | Once per Pilot | beyond the border, 5 jumps | once per pilot, up to 1 ships, empty hold | one-time |
| 12 | [fit-ice-harvester](fit-ice-harvester.json) | Fitting | home space | once per pilot, up to 1 ships, 15 pilots in all, without ice_harvester_i, from 6,000 cr | one-time |
| 13 | [fit-ice-harvester-node-beta](fit-ice-harvester-node-beta.json) | Fitting | home space | once per pilot, up to 1 ships, 2 pilots in all, without ice_harvester_i, from 6,000 cr | one-time |
| 14 | [fit-ice-harvester-node-gamma](fit-ice-harvester-node-gamma.json) | Fitting | home space | once per pilot, up to 1 ships, 2 pilots in all, without ice_harvester_i, from 6,000 cr | one-time |
| 15 | [fit-ice-harvester-synchrony](fit-ice-harvester-synchrony.json) | Fitting | home space | once per pilot, up to 1 ships, 4 pilots in all, without ice_harvester_i, from 6,000 cr | one-time |
| 16 | [fit-ice-harvester-experiment](fit-ice-harvester-experiment.json) | Fitting | home space | once per pilot, up to 1 ships, 2 pilots in all, without ice_harvester_i, from 6,000 cr | one-time |
| 17 | [fit-ice-harvester-lhs-1140](fit-ice-harvester-lhs-1140.json) | Fitting | beyond the border, 6 jumps | once per pilot, up to 5 ships, 20 pilots in all, without ice_harvester_i, empty hold, from 6,000 cr | one-time |
| 18 | [mine-wolf-1061-vent](mine-wolf-1061-vent.json) | Paying Routes | beyond the border, 4 jumps | up to 1 ships, needs nitrogen_vent, empty hold | 5,360 |
| 19 | [mine-achernar-frost-ring-nexus](mine-achernar-frost-ring-nexus.json) | Paying Routes | beyond the border, 4 jumps | up to 13 ships, needs ice_harvester_i, empty hold | 2,040 |
| 20 | [mine-wolf-1061-frozen-drift-nexus](mine-wolf-1061-frozen-drift-nexus.json) | Paying Routes | beyond the border, 4 jumps | up to 5 ships, needs ice_harvester_i, empty hold | 1,640 |
| 21 | [mine-ruchbah-ice-belt-nexus](mine-ruchbah-ice-belt-nexus.json) | Tests | beyond the border, 4 jumps | up to 1 ships, needs ice_harvester_i, empty hold | TBD |
| 22 | [mine-alnair-ice-fields-nexus](mine-alnair-ice-fields-nexus.json) | Paying Routes | beyond the border, 5 jumps | up to 6 ships, needs ice_harvester_i, empty hold | 1,270 |
| 23 | [mine-ruchbah-ice-belt](mine-ruchbah-ice-belt.json) | Paying Routes | beyond the border, 4 jumps | up to 1 ships, needs ice_harvester_i, empty hold | 7,430 |
| 24 | [mine-achernar-frost-ring](mine-achernar-frost-ring.json) | Paying Routes | beyond the border, 4 jumps | up to 1 ships, needs ice_harvester_i, empty hold | 5,830 |
| 25 | [mine-cryogenic-reserve](mine-cryogenic-reserve.json) | Measured at a Loss | home space | up to 1 ships, needs ice_harvester_i | -340 |
| 26 | [mine-wolf-1061-frozen-drift](mine-wolf-1061-frozen-drift.json) | Paying Routes | beyond the border, 4 jumps | up to 1 ships, needs ice_harvester_i, empty hold | 2,580 |
| 27 | [mine-alnair-ice-fields](mine-alnair-ice-fields.json) | Paying Routes | beyond the border, 5 jumps | up to 1 ships, needs ice_harvester_i, empty hold | 840 |
| 28 | [census-frontier](census-frontier.json) | Reading and Waiting | beyond the border, 7 jumps | up to 12 ships, empty hold | -620 |
| 29 | [park](park.json) | Reading and Waiting | home space | the park route | -670 |

Planned:

| What | When |
|---|---|
| Read the first RESULT line of mine-ruchbah-ice-belt-nexus and the runs of the three lifted Central Nexus routes; lift what pays as far as the Central Nexus bid carries (44,128 units in all levels at 07:58 UTC, regains about 1,250 an hour); bring the Experiment and Node Alpha routes back up when their bids regain | turn of 2026-11-16 12:00 UTC |
| About 11,000 water ice lie in miners' storage at The Experiment, Node Alpha and Synchrony where the bids are 0: a carry from storage to the Central Nexus bid (a withdraw step), or Logistics hauling it | turn of 2026-11-16 12:00 UTC |

## scout

Kept by Oracle. Routes: 15.

| # | Route | Group | Zone | Open to | Credits per ship-hour |
|---|---|---|---|---|---|
| 1 | [voidborn-signal-fragments](voidborn-signal-fragments.json) | Once per Pilot | home space | once per pilot, up to 3 ships, from navigation 3 | one-time |
| 2 | [voidborn-first-hunt-gsc-0031](voidborn-first-hunt-gsc-0031.json) | Once per Pilot | beyond the border, 5 jumps | once per pilot, up to 1 ships, empty hold | one-time |
| 3 | [census-voidborn](census-voidborn.json) | Reading and Waiting | home space | up to 3 ships | -530 |
| 4 | [voidborn-precedence](voidborn-precedence.json) | Once per Pilot | home space | once per pilot, up to 40 ships | one-time |
| 5 | [voidborn-selling](voidborn-selling.json) | Once per Pilot | home space | once per pilot, up to 10 ships | one-time |
| 6 | [voidborn-concurrent](voidborn-concurrent.json) | Once per Pilot | home space | once per pilot | one-time |
| 7 | [voidborn-substrate](voidborn-substrate.json) | Once per Pilot | home space | once per pilot, from 3,000 cr | one-time |
| 8 | [voidborn-missions-1](voidborn-missions-1.json) | Once per Pilot | home space | once per pilot, from 8,000 cr | one-time |
| 9 | [voidborn-mining-missions](voidborn-mining-missions.json) | Once per Pilot | home space | once per pilot, up to 40 ships | one-time |
| 10 | [voidborn-first-steps](voidborn-first-steps.json) | Once per Pilot | home space | once per pilot, up to 2 ships | one-time |
| 11 | [voidborn-conductive-lattice](voidborn-conductive-lattice.json) | Once per Pilot | beyond the border, 6 jumps | once per pilot, up to 10 ships, 146 pilots in all, empty hold, from 13,000 cr | one-time |
| 12 | [hunt-atlas-gas-pocket](hunt-atlas-gas-pocket.json) | Paying Routes | beyond the border, 6 jumps | up to 1 ships, empty hold | 4,200 |
| 13 | [hunt-test-homam-frost-moth](hunt-test-homam-frost-moth.json) | Paying Routes | beyond the border, 6 jumps | up to 1 ships, empty hold | 1,160 |
| 14 | [census-frontier](census-frontier.json) | Reading and Waiting | beyond the border, 7 jumps | up to 12 ships, empty hold | -620 |
| 15 | [park](park.json) | Reading and Waiting | home space | the park route | -670 |

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

Kept by Unity. Routes: 27.

| # | Route | Group | Zone | Open to | Credits per ship-hour |
|---|---|---|---|---|---|
| 1 | [voidborn-signal-fragments](voidborn-signal-fragments.json) | Once per Pilot | home space | once per pilot, up to 3 ships, from navigation 3 | one-time |
| 2 | [voidborn-concurrent](voidborn-concurrent.json) | Once per Pilot | home space | once per pilot | one-time |
| 3 | [voidborn-substrate](voidborn-substrate.json) | Once per Pilot | home space | once per pilot, from 3,000 cr | one-time |
| 4 | [voidborn-missions-1](voidborn-missions-1.json) | Once per Pilot | home space | once per pilot, from 8,000 cr | one-time |
| 5 | [voidborn-mining-missions](voidborn-mining-missions.json) | Once per Pilot | home space | once per pilot, up to 40 ships | one-time |
| 6 | [voidborn-first-steps](voidborn-first-steps.json) | Once per Pilot | home space | once per pilot, up to 2 ships | one-time |
| 7 | [voidborn-selling](voidborn-selling.json) | Once per Pilot | home space | once per pilot, up to 10 ships | one-time |
| 8 | [voidborn-precedence](voidborn-precedence.json) | Once per Pilot | home space | once per pilot, up to 40 ships | one-time |
| 9 | [voidborn-first-hunt-nexus](voidborn-first-hunt-nexus.json) | Once per Pilot | home space | once per pilot, up to 1 ships | one-time |
| 10 | [voidborn-first-hunt-gsc](voidborn-first-hunt-gsc.json) | Once per Pilot | home space | once per pilot, up to 1 ships | one-time |
| 11 | [voidborn-first-hunt-acubens](voidborn-first-hunt-acubens.json) | Once per Pilot | home space | once per pilot, up to 1 ships | one-time |
| 12 | [fit-ice-harvester-guard](fit-ice-harvester-guard.json) | Fitting | home space | once per pilot, up to 4 ships, 8 pilots in all, without ice_harvester_i, from 6,000 cr | one-time |
| 13 | [mine-node-beta-frozen-drift](mine-node-beta-frozen-drift.json) | Paying Routes | home space | up to 1 ships, needs ice_harvester_i | 1,480 |
| 14 | [mine-ruchbah-ice-belt](mine-ruchbah-ice-belt.json) | Paying Routes | beyond the border, 4 jumps | up to 1 ships, needs ice_harvester_i, empty hold | 7,430 |
| 15 | [mine-achernar-frost-ring](mine-achernar-frost-ring.json) | Paying Routes | beyond the border, 4 jumps | up to 1 ships, needs ice_harvester_i, empty hold | 5,830 |
| 16 | [mine-wolf-1061-frozen-drift](mine-wolf-1061-frozen-drift.json) | Paying Routes | beyond the border, 4 jumps | up to 1 ships, needs ice_harvester_i, empty hold | 2,580 |
| 17 | [mine-keid-ice-shelf](mine-keid-ice-shelf.json) | Paying Routes | beyond the border, 5 jumps | up to 2 ships, needs ice_harvester_i, empty hold | 1,380 |
| 18 | [mine-cryogenic-reserve](mine-cryogenic-reserve.json) | Measured at a Loss | home space | up to 1 ships, needs ice_harvester_i | -340 |
| 19 | [mine-alnair-ice-fields](mine-alnair-ice-fields.json) | Paying Routes | beyond the border, 5 jumps | up to 1 ships, needs ice_harvester_i, empty hold | 840 |
| 20 | [mine-gsc-0041-frost-ring](mine-gsc-0041-frost-ring.json) | Paying Routes | beyond the border, 4 jumps | up to 1 ships, needs ice_harvester_i, empty hold | 2,080 |
| 21 | [mine-antares-ice-fields](mine-antares-ice-fields.json) | Paying Routes | beyond the border, 5 jumps | up to 1 ships, needs ice_harvester_i, empty hold | 350 |
| 22 | [mine-intercrus-ice-fields](mine-intercrus-ice-fields.json) | Paying Routes | beyond the border, 7 jumps | up to 2 ships, needs ice_harvester_i, empty hold | 880 |
| 23 | [mine-deepwell-volatile-ice](mine-deepwell-volatile-ice.json) | Tests | beyond the border, 7 jumps | up to 1 ships, needs ice_harvester_i, empty hold | TBD |
| 24 | [hunt-starveling-nebula-veil-ray](hunt-starveling-nebula-veil-ray.json) | Measured at a Loss | beyond the border, 6 jumps | up to 1 ships, empty hold | -500 |
| 25 | [hunt-felis-dim-lattice-veil-ray](hunt-felis-dim-lattice-veil-ray.json) | Measured at a Loss | beyond the border, 7 jumps | up to 1 ships, empty hold | -440 |
| 26 | [census-frontier](census-frontier.json) | Reading and Waiting | beyond the border, 7 jumps | up to 12 ships, empty hold | -620 |
| 27 | [park](park.json) | Reading and Waiting | home space | the park route | -670 |

## trader

Kept by Mercury. Routes: 9.

| # | Route | Group | Zone | Open to | Credits per ship-hour |
|---|---|---|---|---|---|
| 1 | [voidborn-first-steps](voidborn-first-steps.json) | Once per Pilot | home space | once per pilot, up to 2 ships | one-time |
| 2 | [voidborn-concurrent](voidborn-concurrent.json) | Once per Pilot | home space | once per pilot | one-time |
| 3 | [voidborn-substrate](voidborn-substrate.json) | Once per Pilot | home space | once per pilot, from 3,000 cr | one-time |
| 4 | [voidborn-missions-1](voidborn-missions-1.json) | Once per Pilot | home space | once per pilot, from 8,000 cr | one-time |
| 5 | [voidborn-mining-missions](voidborn-mining-missions.json) | Once per Pilot | home space | once per pilot, up to 40 ships | one-time |
| 6 | [voidborn-precedence](voidborn-precedence.json) | Once per Pilot | home space | once per pilot, up to 40 ships | one-time |
| 7 | [voidborn-conductive-lattice](voidborn-conductive-lattice.json) | Once per Pilot | beyond the border, 6 jumps | once per pilot, up to 10 ships, 146 pilots in all, empty hold, from 13,000 cr | one-time |
| 8 | [census-frontier](census-frontier.json) | Reading and Waiting | beyond the border, 7 jumps | up to 12 ships, empty hold | -620 |
| 9 | [park](park.json) | Reading and Waiting | home space | the park route | -670 |

Planned:

| What | When |
|---|---|
| Fly voidborn-signal-fragments by hand with the one other trader that shares the tested pilot's skills (piloting 5, navigation 3, exploration 2); if offered, ask the Fleet Admiral for a skill condition on routes and offer the route to the fleet's 21 pilots with those levels. | the turn of 2026-11-16 08:30 UTC, or this turn when the pilot is free |
| voidborn-conductive-lattice for the other divisions once requests.log ENT-096 is done: every trader has flown it; read the silver ask at Ironlight Crossroads before more pilots start it. | after the runner fix |
| Plasma gas from Ironlight Crossroads into the station bids at Node Beta: a route only with requires.bid (owed by Unity); the bid read 100 cr for 4 units (9 in all) at 04:46 UTC. | after 2026-11-16 12:00 UTC |
| Control-node craft as a route when the runner's craft step exists and circuit boards stand at depth: at 05:00 UTC a run cost about 1,247 cr in inputs against 1,370 at the Node Gamma bid, and the boards at that price were 23 units. | after 2026-11-16 12:00 UTC |

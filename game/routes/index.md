---
name: routes-index
id: 20261115T153923Z
tier: intel
author: Unity
---

# index.md -- Routes We Fly

Written by `python3 -B game/fleet/routes.py index`, never by hand. A route is a
task one pilot carries out by itself; its file is `game/routes/<id>.json`
(`BLUEPRINT.md`). The figures are what our own runs measured. The groups and the
plans at a glance: [master-index.md](master-index.md); every plan in its order:
[plan.md](plan.md). Inside a group: home space first, then by kind and name.

## Once per Pilot

Missions and rewards the game pays once per pilot: a new pilot's first work, and seed money.

| Route | Kind | Zone | What it is | Open to | Runs | Minutes per run | Credits per run | Credits per ship-hour | Measured |
|---|---|---|---|---|---|---|---|---|---|
| [voidborn-concurrent](voidborn-concurrent.json) | circuit | home space | Concurrent Approval: accept at Central Nexus, deliver two neural soma to Node Beta (3,000 cr once) | once per pilot | TBD | TBD | TBD | TBD | -- |
| [voidborn-first-hunt-acubens](voidborn-first-hunt-acubens.json) | circuit | home space | First Hunt: Belt-Grazers: 1,000 cr once and 50 Weapons XP; three belt-grazers at Acubens Shadow Pocket | once per pilot, up to 1 ships | TBD | TBD | TBD | TBD | -- |
| [voidborn-first-hunt-gsc](voidborn-first-hunt-gsc.json) | circuit | home space | First Hunt: Belt-Grazers: 1,000 cr once and 50 Weapons XP; three belt-grazers at Spacetime Seep | once per pilot, up to 1 ships | TBD | TBD | TBD | TBD | -- |
| [voidborn-first-hunt-nexus](voidborn-first-hunt-nexus.json) | circuit | home space | First Hunt: Belt-Grazers: 1,000 cr once and 50 Weapons XP; three belt-grazers at Material Harvesters | once per pilot, up to 1 ships | TBD | TBD | TBD | TBD | -- |
| [voidborn-first-steps](voidborn-first-steps.json) | circuit | home space | First Steps in the Void for a pilot that holds it: mine 15 carbon ore at Acubens Belt, hand in at Central Nexus | once per pilot, up to 2 ships | TBD | TBD | TBD | TBD | -- |
| [voidborn-mining-missions](voidborn-mining-missions.json) | circuit | home space | Iron Supply Run and Copper Requisition: accept at Central Nexus, mine at Acubens by way of Node Beta, hand in at Central Nexus | once per pilot, up to 40 ships | TBD | TBD | TBD | TBD | -- |
| [voidborn-missions-1](voidborn-missions-1.json) | circuit | home space | Synchrony Relay Run and Crystal Delivery: two board missions in one circuit of 8 jumps | once per pilot, from 8,000 cr | 146 | 22 | 6,430 | one-time | 2026-11-15 |
| [voidborn-precedence](voidborn-precedence.json) | circuit | home space | Precedence: 4,000 cr once, a round of three of our stations | once per pilot, up to 40 ships | 1 | 15 | 3,900 | one-time | 2026-11-15 |
| [voidborn-selling](voidborn-selling.json) | circuit | home space | Market Participation: Selling: 1,000 cr once; ten liquid nitrogen bought and sold at The Experiment | once per pilot, up to 10 ships | 12 | 5 | 870 | one-time | 2026-11-15 |
| [voidborn-substrate](voidborn-substrate.json) | circuit | home space | Substrate Delivery: two neural soma bought at Central Nexus, the mission taken at Node Alpha and handed in at Central Nexus; 2 jumps | once per pilot, from 3,000 cr | 146 | 8 | 1,790 | one-time | 2026-11-15 |
| [voidborn-conductive-lattice](voidborn-conductive-lattice.json) | circuit | beyond the border, 6 jumps | Technician Pale-6's chain at Node Beta, once per pilot: Conductive Lattice (5,500 cr, 20 silver ore from Ironlight Crossroads), Resonance Substrate (7,000 cr, 15 energy crystal from Central Nexus), Final Calibration (8,000 cr, 5 circuit boards handed out, delivered to Node Gamma) | once per pilot, up to 6 ships, 9 pilots in all, empty hold, from 13,000 cr | TBD | TBD | TBD | TBD | -- |
| [voidborn-first-hunt-schedar](voidborn-first-hunt-schedar.json) | circuit | beyond the border, 2 jumps | First Hunt: Belt-Grazers: 1,000 cr once and 50 Weapons XP; three belt-grazers at Schedar Belt (lawless, one jump past GSC-0027) | once per pilot, up to 1 ships, empty hold | TBD | TBD | TBD | TBD | -- |

## Paying Routes

Work that repeats and whose runs measured above zero.

| Route | Kind | Zone | What it is | Open to | Runs | Minutes per run | Credits per run | Credits per ship-hour | Measured |
|---|---|---|---|---|---|---|---|---|---|
| [hunt-gsc-veil-ray](hunt-gsc-veil-ray.json) | hunt | home space | Veil-rays at GSC-0027 Prism Scatter; verdigris curd sold at Central Nexus | up to 1 ships, without piercing_railgun_i | 16 | 24 | 1,620 | 3,620 | 2026-11-15 |
| [hunt-hamal-veil-ray](hunt-hamal-veil-ray.json) | hunt | home space | Veil-rays at Hamal Crystal Bloom; verdigris curd sold at Central Nexus | up to 1 ships, without piercing_railgun_i | 10 | 27 | 1,150 | 2,890 | 2026-11-15 |
| [mine-node-beta-frozen-drift](mine-node-beta-frozen-drift.json) | mine | home space | Node Beta Frozen Drift: water_ice, nitrogen_ice, deuterium_ice; sold at Node Alpha Processing Station | up to 1 ships, needs ice_harvester_i | 1 | 44 | 5,260 | 7,100 | 2026-11-16 |
| [hunt-ruchbah-veil-ray](hunt-ruchbah-veil-ray.json) | hunt | beyond the border, 4 jumps | Veil-rays at Ruchbah Broken Glass Veil (lawless); verdigris curd sold at The Experiment | up to 1 ships, without piercing_railgun_i, empty hold | 2 | 18 | 580 | 1,920 | 2026-11-15 |
| [mine-achernar-frost-ring](mine-achernar-frost-ring.json) | mine | beyond the border, 4 jumps | Achernar Frost Ring: water_ice, nitrogen_ice, deuterium_ice, methane_ice; sold at The Experiment Research Station | up to 3 ships, needs ice_harvester_i, empty hold | 1 | 49 | 5,040 | 6,200 | 2026-11-16 |
| [mine-ruchbah-ice-belt](mine-ruchbah-ice-belt.json) | mine | beyond the border, 4 jumps | Ruchbah Ice Belt: water_ice, nitrogen_ice, deuterium_ice, methane_ice; sold at The Experiment Research Station | up to 3 ships, needs ice_harvester_i, empty hold | 1 | 45 | 5,450 | 7,270 | 2026-11-16 |
| [mine-wolf-1061-frozen-drift](mine-wolf-1061-frozen-drift.json) | mine | beyond the border, 4 jumps | Wolf 1061 Frozen Drift: water_ice, nitrogen_ice, deuterium_ice, methane_ice; sold at Node Alpha Processing Station | up to 2 ships, needs ice_harvester_i, empty hold | 1 | 67 | 4,640 | 4,180 | 2026-11-16 |
| [mine-wolf-1061-vent](mine-wolf-1061-vent.json) | mine | beyond the border, 4 jumps | Wolf 1061 Frozen Drift with a Nitrogen Vent: water and the rare ices, sold at Synchrony | up to 1 ships, needs nitrogen_vent, empty hold | 1 | 55 | 6,730 | 7,330 | 2026-11-16 |

## Tests

Work that repeats and has no measured figure yet: one ship until its first RESULT line is read.

| Route | Kind | Zone | What it is | Open to | Runs | Minutes per run | Credits per run | Credits per ship-hour | Measured |
|---|---|---|---|---|---|---|---|---|---|
| [trade-ceramite-plating-the-central](trade-ceramite-plating-the-central.json) | circuit | home space | Ceramite Plating: bought at The Experiment Research Station for 899 cr, sold at The Core for 1185 cr | up to 1 ships, from 7,944 cr | TBD | TBD | TBD | TBD | -- |
| [trade-voidborn-neural-soma-central-the](trade-voidborn-neural-soma-central-the.json) | circuit | home space | Voidborn Neural Soma: bought at The Core for 258 cr, sold at The Experiment Research Station for 690 cr | up to 1 ships, from 3,851 cr | TBD | TBD | TBD | TBD | -- |
| [hunt-cedarhold-dim-lattice-veil-ray](hunt-cedarhold-dim-lattice-veil-ray.json) | hunt | beyond the border, 5 jumps | veil_ray at cedarhold_dim_lattice; loot sold at The Experiment Research Station | up to 1 ships, without piercing_railgun_i, empty hold | TBD | TBD | TBD | TBD | -- |
| [hunt-faintlight-drift-veil-ray](hunt-faintlight-drift-veil-ray.json) | hunt | beyond the border, 5 jumps | veil_ray at faintlight_drift; loot sold at Node Beta Industrial Station | up to 1 ships, without piercing_railgun_i, empty hold | TBD | TBD | TBD | TBD | -- |
| [hunt-keid-fractured-prism-veil-ray](hunt-keid-fractured-prism-veil-ray.json) | hunt | beyond the border, 5 jumps | veil_ray at keid_fractured_prism; loot sold at Node Beta Industrial Station | up to 1 ships, without piercing_railgun_i, empty hold | TBD | TBD | TBD | TBD | -- |
| [mine-alnair-ice-fields](mine-alnair-ice-fields.json) | mine | beyond the border, 5 jumps | Alnair Ice Fields: water_ice, nitrogen_ice, deuterium_ice; sold at Node Alpha Processing Station | up to 1 ships, needs ice_harvester_i, empty hold | TBD | TBD | TBD | TBD | -- |
| [mine-antares-ice-fields](mine-antares-ice-fields.json) | mine | beyond the border, 5 jumps | Antares Ice Fields: water_ice, nitrogen_ice, deuterium_ice, helium_ice; sold at Node Alpha Processing Station | up to 1 ships, needs ice_harvester_i, empty hold | TBD | TBD | TBD | TBD | -- |
| [mine-gsc-0041-frost-ring](mine-gsc-0041-frost-ring.json) | mine | beyond the border, 4 jumps | GSC-0041 Frost Ring: water_ice, nitrogen_ice, deuterium_ice; sold at Node Alpha Processing Station | up to 1 ships, needs ice_harvester_i, empty hold | TBD | TBD | TBD | TBD | -- |
| [mine-gsc-0050-gas-plume](mine-gsc-0050-gas-plume.json) | mine | beyond the border, 3 jumps | GSC-0050 Gas Plume: plasma_gas, xenon_gas, neon_gas, chlorine_gas; sold at Node Beta Industrial Station | up to 1 ships, needs gas_harvester_i, empty hold | TBD | TBD | TBD | TBD | -- |
| [mine-intercrus-ice-fields](mine-intercrus-ice-fields.json) | mine | beyond the border, 7 jumps | Intercrus Ice Fields: water_ice, nitrogen_ice; sold at The Experiment Research Station | up to 1 ships, needs ice_harvester_i, empty hold | TBD | TBD | TBD | TBD | -- |
| [mine-keid-ice-shelf](mine-keid-ice-shelf.json) | mine | beyond the border, 5 jumps | Keid Ice Shelf: water_ice, deuterium_ice; sold at Node Alpha Processing Station | up to 1 ships, needs ice_harvester_i, empty hold | TBD | TBD | TBD | TBD | -- |

## Fitting

A module bought and fitted: the tool a kind of work needs.

| Route | Kind | Zone | What it is | Open to | Runs | Minutes per run | Credits per run | Credits per ship-hour | Measured |
|---|---|---|---|---|---|---|---|---|---|
| [fit-gas-harvester](fit-gas-harvester.json) | circuit | home space | Fit a Gas Harvester I at Node Beta: the tool of the gas test | once per pilot, up to 1 ships, 1 pilots in all, needs mining_laser_i, without ice_harvester_i, from 6,000 cr | 1 | 4 | -1,240 | one-time | 2026-11-16 |
| [fit-ice-harvester](fit-ice-harvester.json) | circuit | home space | Fit an Ice Harvester I at Node Alpha: the tool every ice field needs | once per pilot, up to 1 ships, 15 pilots in all, without ice_harvester_i, from 6,000 cr | 6 | 0 | -1,490 | one-time | 2026-11-16 |
| [fit-ice-harvester-guard](fit-ice-harvester-guard.json) | circuit | home space | Fit an Ice Harvester I at Central Nexus: the tool every ice field needs | once per pilot, up to 2 ships, 4 pilots in all, without ice_harvester_i, from 6,000 cr | TBD | TBD | TBD | TBD | -- |

## Reading and Waiting

The census and the park route: they earn nothing; they keep the picture fresh and a ship without work docked.

| Route | Kind | Zone | What it is | Open to | Runs | Minutes per run | Credits per run | Credits per ship-hour | Measured |
|---|---|---|---|---|---|---|---|---|---|
| [census-voidborn](census-voidborn.json) | census | home space | Read one Voidborn system whole: deposits, creatures, order book, mission board | up to 3 ships | 93 | 8 | -70 | -550 | 2026-11-15 |
| [park](park.json) | circuit | home space | Dock at Central Nexus and wait there: a docked ship costs nothing | the park route | TBD | TBD | TBD | TBD | -- |
| [census-frontier](census-frontier.json) | census | beyond the border, 7 jumps | Read one lawless system around our space whole: deposits, creatures, stations, order books, mission boards | up to 12 ships, empty hold | 35 | 14 | -140 | -600 | 2026-11-15 |

## Measured at a Loss

Work that repeats and whose runs measured zero or below.

| Route | Kind | Zone | What it is | Open to | Runs | Minutes per run | Credits per run | Credits per ship-hour | Measured |
|---|---|---|---|---|---|---|---|---|---|
| [hunt-home-drift-ray](hunt-home-drift-ray.json) | hunt | home space | Drift-rays at Stellar Siphon in Nexus Prime; goods sold or stored at Central Nexus | up to 1 ships | 8 | 10 | -40 | -250 | 2026-11-15 |
| [hunt-test-acubens-patina-grazer](hunt-test-acubens-patina-grazer.json) | hunt | home space | Yield test: patina_grazer at acubens_shadow_pocket; what a kill drops and whether a bid takes it | up to 1 ships, without piercing_railgun_i | 1 | 6 | -60 | -600 | 2026-11-15 |
| [mine-acubens](mine-acubens.json) | mine | home space | Iron and copper at Acubens Shadow Pocket; ore into storage at Node Beta | up to 16 ships | 48 | 45 | -120 | -160 | 2026-11-15 |
| [mine-bellatrix](mine-bellatrix.json) | mine | home space | Wait at Bellatrix Major Belt beside Node Gamma station for whatever regrows (thorium, palladium, iridium, carbon) | up to 1 ships | 8 | 45 | 0 | 0 | 2026-11-15 |
| [mine-cryogenic-reserve](mine-cryogenic-reserve.json) | mine | home space | Cryogenic Reserve: water_ice, nitrogen_ice, oxygen_ice; sold at Synchrony Hub | up to 1 ships, needs ice_harvester_i | 1 | 47 | -270 | -340 | 2026-11-16 |
| [mine-gsc-seep](mine-gsc-seep.json) | mine | home space | Iron and copper at GSC-0027 Spacetime Seep; ore into storage at Node Beta | up to 16 ships | 48 | 45 | -120 | -160 | 2026-11-15 |
| [mine-pherkad-rift](mine-pherkad-rift.json) | mine | home space | Copper and iron at Pherkad Null Rift; ore into storage at Synchrony Hub | every pilot | 65 | 45 | -120 | -160 | 2026-11-15 |
| [hunt-garnet-dim-lattice-veil-ray](hunt-garnet-dim-lattice-veil-ray.json) | hunt | beyond the border, 5 jumps | veil_ray at garnet_dim_lattice; loot sold at The Experiment Research Station | up to 1 ships, without piercing_railgun_i, empty hold | 1 | 10 | -100 | -590 | 2026-11-15 |
| [hunt-low-charge-glint-veil-ray](hunt-low-charge-glint-veil-ray.json) | hunt | beyond the border, 4 jumps | veil_ray at low_charge_glint; loot sold at Node Beta Industrial Station | up to 1 ships, without piercing_railgun_i, empty hold | 1 | 11 | -100 | -540 | 2026-11-15 |

## Off

Written down, not flown.

| Route | Kind | Zone | What it is | Open to | Runs | Minutes per run | Credits per run | Credits per ship-hour | Measured |
|---|---|---|---|---|---|---|---|---|---|
| [first-survey](first-survey.json) | circuit | home space | Signal Propagation Survey: dock at the five other Voidborn stations (20,000 cr) | once per pilot, off | TBD | TBD | TBD | TBD | -- |
| [hunt-acubens-urchin](hunt-acubens-urchin.json) | hunt | home space | Cinder-urchins at Acubens Shadow Pocket; radiant bile sold at Node Gamma | up to 1 ships, off | 2 | 25 | -120 | -290 | 2026-11-15 |
| [hunt-home-whale](hunt-home-whale.json) | hunt | home space | Pilot-whales at Stellar Siphon in Nexus Prime; whale oil sold at Node Beta | up to 1 ships, needs piercing_railgun_i, off | 1 | 20 | 570 | 1,670 | 2026-11-15 |
| [hunt-test-eltanin-kiln-snail](hunt-test-eltanin-kiln-snail.json) | hunt | home space | Yield test: kiln_snail at eltanin_prime_belt; what a kill drops and whether a bid takes it | up to 1 ships, without piercing_railgun_i, off | TBD | TBD | TBD | TBD | -- |
| [hunt-test-frozen-drift-deuteron-slug](hunt-test-frozen-drift-deuteron-slug.json) | hunt | home space | Yield test: deuteron_slug at node_beta_frozen_drift; what a kill drops and whether a bid takes it | up to 1 ships, without piercing_railgun_i, off | 1 | 23 | -30 | -80 | 2026-11-15 |
| [hunt-test-node-gamma-ice-belt](hunt-test-node-gamma-ice-belt.json) | hunt | home space | Yield test: rime_grazer, pressblister at node_gamma_ice_belt; what a kill drops and whether a bid takes it | up to 1 ships, without piercing_railgun_i, off | 1 | 17 | -60 | -210 | 2026-11-15 |
| [hunt-test-siphon-bell-jelly](hunt-test-siphon-bell-jelly.json) | hunt | home space | Yield test: bell_jelly at stellar_siphon; what a kill drops and whether a bid takes it | up to 1 ships, without piercing_railgun_i, off | 1 | 10 | -30 | -150 | 2026-11-15 |

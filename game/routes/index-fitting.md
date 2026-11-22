---
name: routes-index-fitting
id: 20261116T174326Z
tier: intel
author: Unity
---

# index-fitting.md -- Fitting

Written by `python3 -B game/fleet/routes.py index`, never by hand. A module bought and fitted: the tool a kind of work needs.
A route is a task one pilot carries out by itself; its file is `game/routes/<id>.json`
(`BLUEPRINT.md`). The figures are what our own runs measured. Home space first, then by
kind and name. Up: [master-index.md](master-index.md).

Routes: 12.

| Route | Kind | Zone | What it is | Open to | Runs | Minutes per run | Credits per run | Credits per ship-hour | Measured |
|---|---|---|---|---|---|---|---|---|---|
| [fit-gas-harvester](fit-gas-harvester.json) | circuit | home space | Fit a Gas Harvester I at Node Beta: the tool of the gas test | once per pilot, up to 1 ships, 1 pilots in all, needs mining_laser_i, without ice_harvester_i, from 6,000 cr | 1 | 4 | -1,240 | one-time | 2026-11-16 |
| [fit-gas-harvester-hauler](fit-gas-harvester-hauler.json) | circuit | home space | Fit a Gas Harvester I at Node Beta: the tool of the Logistics gas test | once per pilot, up to 1 ships, 1 pilots in all, needs mining_laser_i, without gas_harvester_i, from 6,000 cr | 1 | 4 | -1,240 | one-time | 2026-11-16 |
| [fit-ice-harvester](fit-ice-harvester.json) | circuit | home space | Fit an Ice Harvester I at Node Alpha: the tool every ice field needs | once per pilot, up to 1 ships, 15 pilots in all, without ice_harvester_i, from 6,000 cr | 17 | 2 | -560 | one-time | 2026-11-16 |
| [fit-ice-harvester-experiment](fit-ice-harvester-experiment.json) | circuit | home space | Fit an Ice Harvester I at The Experiment: the tool every ice field needs | once per pilot, up to 1 ships, 2 pilots in all, without ice_harvester_i, from 6,000 cr | 2 | 4 | -1,470 | one-time | 2026-11-16 |
| [fit-ice-harvester-guard](fit-ice-harvester-guard.json) | circuit | home space | Fit an Ice Harvester I at Central Nexus: the tool every ice field needs | once per pilot, up to 4 ships, 8 pilots in all, without ice_harvester_i, from 6,000 cr | 8 | 1 | -1,590 | one-time | 2026-11-16 |
| [fit-ice-harvester-node-beta](fit-ice-harvester-node-beta.json) | circuit | home space | Fit an Ice Harvester I at Node Beta: the tool every ice field needs | once per pilot, up to 1 ships, 2 pilots in all, without ice_harvester_i, from 6,000 cr | 2 | 4 | -1,450 | one-time | 2026-11-16 |
| [fit-ice-harvester-node-gamma](fit-ice-harvester-node-gamma.json) | circuit | home space | Fit an Ice Harvester I at Node Gamma: the tool every ice field needs | once per pilot, up to 1 ships, 2 pilots in all, without ice_harvester_i, from 6,000 cr | 2 | 4 | -1,460 | one-time | 2026-11-16 |
| [fit-ice-harvester-synchrony](fit-ice-harvester-synchrony.json) | circuit | home space | Fit an Ice Harvester I at Synchrony Hub: the tool every ice field needs | once per pilot, up to 1 ships, 4 pilots in all, without ice_harvester_i, from 6,000 cr | 4 | 5 | -1,460 | one-time | 2026-11-16 |
| [fit-pulse-laser-iii-central-nexus](fit-pulse-laser-iii-central-nexus.json) | circuit | home space | Swap the Pulse Laser I for a Pulse Laser III at Central Nexus (fit with replace), one ship first | once per pilot, up to 1 ships, 1 pilots in all, needs pulse_laser_i, without pulse_laser_iii, from 30,000 cr | TBD | TBD | TBD | TBD | -- |
| [fit-shield-booster-pirate-group](fit-shield-booster-pirate-group.json) | circuit | home space | Fit a Shield Booster I at Central Nexus: the first step of the drone group against pirates | once per pilot, up to 2 ships, 5 pilots in all, without shield_booster_i, from 8,000 cr, from gunnery 3 | 5 | 6 | -3,030 | one-time | 2026-11-17 |
| [fit-survey-scanner-central-nexus](fit-survey-scanner-central-nexus.json) | circuit | home space | Test: fit one Survey Scanner I at Central Nexus, so that one scout can survey_system (hidden places, deep core deposits, the scanning skill) | once per pilot, up to 1 ships, 7 pilots in all, without survey_scanner_i, from 12,000 cr | 9 | 1 | -3,280 | one-time | 2026-11-21 |
| [fit-ice-harvester-lhs-1140](fit-ice-harvester-lhs-1140.json) | circuit | beyond the border, 6 jumps | Fit an Ice Harvester I at Ironlight Crossroads (LHS 1140), beyond the border: a test with one miner | once per pilot, up to 5 ships, 20 pilots in all, without ice_harvester_i, empty hold, from 6,000 cr | 19 | 9 | -690 | one-time | 2026-11-16 |

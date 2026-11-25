---
name: routes-index-measured-at-a-loss
id: 20261116T174328Z
tier: intel
author: Unity
---

# index-measured-at-a-loss.md -- Measured at a Loss

Written by `python3 -B game/fleet/routes.py index`, never by hand. Work that repeats and whose runs of the last 12 hours measured zero or below.
A route is a task one pilot carries out by itself; its file is `game/routes/<id>.json`
(`BLUEPRINT.md`). The figures are what our own runs measured. Home space first, then by
kind and name. Up: [master-index.md](master-index.md).

Routes: 7.

| Route | Kind | Zone | What it is | Open to | Runs | Minutes per run | Credits per run | Credits per ship-hour | Measured |
|---|---|---|---|---|---|---|---|---|---|
| [bursar-null-matter-central-nexus](bursar-null-matter-central-nexus.json) | circuit | home space | Station Bursar: one resting sell order of the pilot's own null matter at central_nexus, kept at 340 (floor 300) | up to 1 ships, 1 pilots in all, with 50 null_matter stored at central_nexus | 2 | 24 | -270 | -680 | 2026-11-24 |
| [bursar-null-matter-node-beta](bursar-null-matter-node-beta.json) | circuit | home space | Station Bursar: one resting sell order of the pilot's own null matter at node_beta_industrial_station, kept at 340 (floor 300) | up to 1 ships, 1 pilots in all, with 50 null_matter stored at node_beta_industrial_station | 1 | 21 | -220 | -630 | 2026-11-24 |
| [mission-83d4aab496f36cd12fbed259b3f534bf-central](mission-83d4aab496f36cd12fbed259b3f534bf-central.json) | circuit | home space | Wreck Recovery: Congregation in GSC-0041: 984 cr, +50 XP at The Core | up to 3 ships | 1 | 5 | -40 | -520 | 2026-11-24 |
| [carry-ember-crucible-to-krynn](carry-ember-crucible-to-krynn.json) | circuit | beyond the border, 20 jumps | Ember glands stored at The Crucible Garrison carried two jumps to the War Citadel (Krynn), where its bid and Station Need pay | up to 1 ships, empty hold, with 3 ember_gland stored at the_crucible_garrison | 1 | 8 | -70 | -530 | 2026-11-24 |
| [carry-melt-sirius-to-experiment](carry-melt-sirius-to-experiment.json) | circuit | beyond the border, 9 jumps | Stored crystal_melt carried from sirius_observatory_station to the the_experiment_research_station bid at 1000 cr or more | up to 1 ships, with 10 crystal_melt stored at sirius_observatory_station, while the_experiment_research_station bids 1000 cr for crystal_melt | 2 | 26 | -320 | -750 | 2026-11-24 |
| [need-ember-gland-krynn](need-ember-gland-krynn.json) | circuit | beyond the border, 20 jumps | Station Need: Ember Gland at the War Citadel (Krynn) filled from the pilot's own glands stored there, about 8,100 cr a gland | up to 1 ships, with 3 ember_gland stored at crimson_war_citadel | 2 | 2 | 0 | 0 | 2026-11-25 |
| [sell-ember-nexus-dheneb](sell-ember-nexus-dheneb.json) | circuit | beyond the border, 11 jumps | Stored ember glands carried from Central Nexus to the Hex Star bid (Dheneb, lawless) | up to 1 ships, with 6 ember_gland stored at central_nexus, while b495c6003fc83e18f6d8cecbe6929133 bids 2000 cr for ember_gland | 1 | 14 | -100 | -420 | 2026-11-24 |

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

Routes: 5.

| Route | Kind | Zone | What it is | Open to | Runs | Minutes per run | Credits per run | Credits per ship-hour | Measured |
|---|---|---|---|---|---|---|---|---|---|
| [mission-70d9950c762ac17eeedfc9a292ed07ac-central](mission-70d9950c762ac17eeedfc9a292ed07ac-central.json) | circuit | home space | Wreck Recovery: Fugue in Algol: 2465 cr, +50 XP at The Core | up to 3 ships | 1 | 6 | -60 | -550 | 2026-11-24 |
| [carry-melt-first-step-to-experiment](carry-melt-first-step-to-experiment.json) | circuit | beyond the border, 18 jumps | Stored crystal_melt carried from first_step_memorial_station to the the_experiment_research_station bid at 1000 cr or more | up to 1 ships, with 20 crystal_melt stored at first_step_memorial_station, while the_experiment_research_station bids 1000 cr for crystal_melt | 2 | 34 | -310 | -540 | 2026-11-24 |
| [need-ember-gland-crucible](need-ember-gland-crucible.json) | circuit | beyond the border, 20 jumps | Station Need: Ember Gland at The Crucible Garrison filled from the pilot's glands stored at Krynn (2 jumps), about 5,600 cr a gland | up to 1 ships, with 10 ember_gland stored at crimson_war_citadel | 1 | 30 | -350 | -690 | 2026-11-24 |
| [need-ember-gland-krynn](need-ember-gland-krynn.json) | circuit | beyond the border, 20 jumps | Station Need: Ember Gland at the War Citadel (Krynn) filled from the pilot's own glands stored there, about 8,100 cr a gland | up to 1 ships, with 3 ember_gland stored at crimson_war_citadel | 5 | 1 | -50 | -2,300 | 2026-11-24 |
| [need-melt-crucible](need-melt-crucible.json) | circuit | beyond the border, 20 jumps | Station Need: Crystal Melt at The Crucible Garrison filled from the pilot's melt stored there, about 890 cr a melt | up to 1 ships, with 12 crystal_melt stored at the_crucible_garrison | 1 | 10 | -80 | -440 | 2026-11-24 |

---
name: routes-templates-mining
id: 20261116T230947Z
tier: intel
author: Unity
---

# templates-mining.md -- The Templates of the Mining Division

Written by `python3 -B game/fleet/routes.py index`, never by hand, from `templates/mining.json`:
the named lists of routes of the mining division. A ship's row in the division's plan
file (`game/fleet/plan.py`) names one as `@<template>` among its own routes, and the ship
tries its routes in this order; a change of a template moves every ship that names it
within the minute. Kept with `plan.py template`; ships are put on one with `plan.py use`.
Up: [master-index.md](master-index.md).

Kept by Zero. Templates: 3. Ships on them: 120.

| Template | Title | Trains | Routes, in this order | Ships on it | Note |
|---|---|---|---|---|---|
| ice-sell | Stored goods and ice sold where a bid stands: stored null matter, methane and ice first, then the ice fields | mining, piloting | [carry-null-matter-synchrony-nexus](carry-null-matter-synchrony-nexus.json) > [drain-methane-experiment](drain-methane-experiment.json) > [drain-ice-nexus](drain-ice-nexus.json) > [drain-ice-node-alpha](drain-ice-node-alpha.json) > [carry-ice-node-alpha-nexus](carry-ice-node-alpha-nexus.json) > [carry-ice-synchrony-nexus](carry-ice-synchrony-nexus.json) > [carry-ice-experiment-nexus](carry-ice-experiment-nexus.json) > [mine-cryogenic-reserve](mine-cryogenic-reserve.json) > [mine-achernar-frost-ring-nexus](mine-achernar-frost-ring-nexus.json) > [mine-ruchbah-ice-belt-nexus](mine-ruchbah-ice-belt-nexus.json) > [mine-wolf-1061-frozen-drift-nexus](mine-wolf-1061-frozen-drift-nexus.json) > [mine-nova-terra-ice-shelf](mine-nova-terra-ice-shelf.json) > [mine-wolf-1061-vent](mine-wolf-1061-vent.json) | 60 | Every route here is gated: a drain or carry opens only on goods the pilot itself stores and a fresh bid (requires.stored, requires.bid); a mine route only on a deep water-ice order at Central Nexus (300 units at its best price) and with an Ice Harvester I fitted. Drains and carries need no harvester. What miners store is sold before new ice is mined. |
| reserve-prism | Gather what the reserve is short of: a loaded hold stored first, carbon, then iron, Schedar first | mining | [store-hold-central-nexus](store-hold-central-nexus.json) > [gather-acubens-belt-carbon](gather-acubens-belt-carbon.json) > [gather-schedar-belt](gather-schedar-belt.json) > [gather-ironhollow-fading-signal](gather-ironhollow-fading-signal.json) > [gather-ironhollow-echo-ejecta](gather-ironhollow-echo-ejecta.json) > [gather-garnet-belt](gather-garnet-belt.json) > [gather-gsc-0027-prism-scatter](gather-gsc-0027-prism-scatter.json) > [gather-hamal-crystal-bloom](gather-hamal-crystal-bloom.json) > [mine-acubens](mine-acubens.json) | 29 | Standing work into storage, nothing sold (orders ENT-025: silicon and carbon first, then iron). Needs the Mining Laser I. First a ship a run left loaded stores its hold at Central Nexus (store-hold-central-nexus, requires.hold). Silicon: no field we read holds it. Carbon: Acubens Belt, one ship, floor 60. Iron: Schedar Belt (beyond the border, 2 jumps, into Node Beta, 10 ships), Ironhollow Fading Signal (beyond the border, into The Experiment, 7 ships, guarded by Military), Ironhollow Echo Ejecta (a one-ship test), then the shared fields Prism Scatter, Hamal and Acubens Shadow Pocket, each closed at its floor. |
| reserve-hamal | Gather what the reserve is short of: a loaded hold stored first, carbon, then iron, Ironhollow first | mining | [store-hold-central-nexus](store-hold-central-nexus.json) > [gather-acubens-belt-carbon](gather-acubens-belt-carbon.json) > [gather-ironhollow-fading-signal](gather-ironhollow-fading-signal.json) > [gather-schedar-belt](gather-schedar-belt.json) > [gather-ironhollow-echo-ejecta](gather-ironhollow-echo-ejecta.json) > [gather-hamal-crystal-bloom](gather-hamal-crystal-bloom.json) > [gather-gsc-0027-prism-scatter](gather-gsc-0027-prism-scatter.json) > [mine-acubens](mine-acubens.json) | 31 | As reserve-prism with Ironhollow Fading Signal before Schedar and Hamal before Prism Scatter, so the division is spread over the iron fields. Needs the Mining Laser I. |

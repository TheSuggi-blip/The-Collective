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
| ice-sell | Stored goods and ice sold where a bid stands: stored null matter, methane and ice first, then the ice fields | mining, piloting | [carry-null-matter-synchrony-nexus](carry-null-matter-synchrony-nexus.json) > [drain-methane-experiment](drain-methane-experiment.json) > [drain-ice-nexus](drain-ice-nexus.json) > [drain-ice-node-alpha](drain-ice-node-alpha.json) > [carry-ice-node-alpha-nexus](carry-ice-node-alpha-nexus.json) > [carry-ice-synchrony-nexus](carry-ice-synchrony-nexus.json) > [carry-ice-experiment-nexus](carry-ice-experiment-nexus.json) > [mine-cryogenic-reserve](mine-cryogenic-reserve.json) > [mine-achernar-frost-ring-nexus](mine-achernar-frost-ring-nexus.json) > [mine-ruchbah-ice-belt-nexus](mine-ruchbah-ice-belt-nexus.json) > [mine-wolf-1061-frozen-drift-nexus](mine-wolf-1061-frozen-drift-nexus.json) > [mine-nova-terra-ice-shelf](mine-nova-terra-ice-shelf.json) > [mine-wolf-1061-vent](mine-wolf-1061-vent.json) | 60 | Every route here is gated: a drain or carry opens only on stored ice and a fresh bid (requires.stored, requires.bid); a mine route only on a deep water-ice order at Central Nexus (300 units at its best price) and with an Ice Harvester I fitted. A drain needs no harvester. Stored ice is sold before new ice is mined. |
| reserve-prism | Gather what the reserve is short of: carbon first, then iron, Prism Scatter first | mining | [gather-acubens-belt-carbon](gather-acubens-belt-carbon.json) > [gather-gsc-0027-prism-scatter](gather-gsc-0027-prism-scatter.json) > [gather-hamal-crystal-bloom](gather-hamal-crystal-bloom.json) > [mine-acubens](mine-acubens.json) | 28 | Standing work into storage at Node Beta, nothing sold (orders ENT-019: silicon and carbon first, then iron). Needs the Mining Laser I. Silicon: no field we read holds it (Nexus Prime Material Harvesters reads 0 to 2 all day). Carbon: Acubens Belt, one ship, floor 60. Iron: Prism Scatter gave 65% iron of what it lost (census 2026-11-16), then Hamal (51%), then Acubens Shadow Pocket, each closed at its floor. |
| reserve-hamal | Gather what the reserve is short of: carbon first, then iron, Hamal Crystal Bloom first | mining | [gather-acubens-belt-carbon](gather-acubens-belt-carbon.json) > [gather-hamal-crystal-bloom](gather-hamal-crystal-bloom.json) > [gather-gsc-0027-prism-scatter](gather-gsc-0027-prism-scatter.json) > [mine-acubens](mine-acubens.json) | 32 | As reserve-prism with Hamal Crystal Bloom first, so the division is spread over two iron fields. Needs the Mining Laser I. |

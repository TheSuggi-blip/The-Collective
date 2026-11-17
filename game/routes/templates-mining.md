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
| reserve-prism | Make, then gather what the reserve lacks: a loaded hold stored, steel plate from stored iron, then gold, silicon, nickel and carbon | mining, crafting, refining | [store-hold-central-nexus](store-hold-central-nexus.json) > [craft-steel-experiment](craft-steel-experiment.json) > [craft-steel-node-beta](craft-steel-node-beta.json) > [gather-goldcrest-gold](gather-goldcrest-gold.json) > [gather-subra-floodlight-flats-silicon](gather-subra-floodlight-flats-silicon.json) > [gather-jadecove-nickel](gather-jadecove-nickel.json) > [gather-acubens-belt-carbon](gather-acubens-belt-carbon.json) | 29 | Orders ENT-050, block ZERO: iron and copper no more while the reserve holds them; P2: stored iron becomes steel plate. The iron gather fields left this template on 2026-11-17 23:20 UTC (Zero). |
| reserve-hamal | Make, then gather what the reserve lacks, the short-ore fields in the other order so the division is spread | mining, crafting, refining | [store-hold-central-nexus](store-hold-central-nexus.json) > [craft-steel-experiment](craft-steel-experiment.json) > [craft-steel-node-beta](craft-steel-node-beta.json) > [gather-acubens-belt-carbon](gather-acubens-belt-carbon.json) > [gather-jadecove-nickel](gather-jadecove-nickel.json) > [gather-subra-floodlight-flats-silicon](gather-subra-floodlight-flats-silicon.json) > [gather-goldcrest-gold](gather-goldcrest-gold.json) | 31 | Orders ENT-050, block ZERO: iron and copper no more while the reserve holds them; P2: stored iron becomes steel plate. The iron gather fields left this template on 2026-11-17 23:20 UTC (Zero). |

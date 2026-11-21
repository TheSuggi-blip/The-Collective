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
| ice-sell | Stored goods and ice sold where a bid stands: stored null matter, methane and ice first, then the ice fields | mining, piloting | [carry-null-matter-synchrony-nexus](carry-null-matter-synchrony-nexus.json) > [drain-methane-experiment](drain-methane-experiment.json) > [drain-ice-nexus](drain-ice-nexus.json) > [drain-ice-node-alpha](drain-ice-node-alpha.json) > [carry-ice-node-alpha-nexus](carry-ice-node-alpha-nexus.json) > [carry-ice-synchrony-nexus](carry-ice-synchrony-nexus.json) > [carry-ice-experiment-nexus](carry-ice-experiment-nexus.json) > [mine-cryogenic-reserve](mine-cryogenic-reserve.json) > [mine-achernar-frost-ring-nexus](mine-achernar-frost-ring-nexus.json) > [mine-ruchbah-ice-belt-nexus](mine-ruchbah-ice-belt-nexus.json) > [mine-wolf-1061-frozen-drift-nexus](mine-wolf-1061-frozen-drift-nexus.json) > [mine-nova-terra-ice-shelf](mine-nova-terra-ice-shelf.json) > [mine-wolf-1061-vent](mine-wolf-1061-vent.json) | 60 | Every route here is gated: a drain or carry opens only on goods the pilot itself stores and a fresh bid (requires.stored, requires.bid); a Central Nexus mine route only on a deep water-ice order (3,000 units at its best price since 2026-11-21: about 18,500 water ice stored) and with an Ice Harvester I fitted. What miners store is sold before new ice is mined. |
| reserve-prism | Gather what the reserve lacks, then make: a loaded hold stored, gold, silicon, nickel and carbon, then steel plate and copper piping from the pilot's own stores | mining, crafting, refining | [store-hold-central-nexus](store-hold-central-nexus.json) > [gather-goldcrest-gold](gather-goldcrest-gold.json) > [gather-subra-floodlight-flats-silicon](gather-subra-floodlight-flats-silicon.json) > [gather-jadecove-nickel](gather-jadecove-nickel.json) > [gather-tiaki-worldsend-nickel](gather-tiaki-worldsend-nickel.json) > [gather-acubens-belt-carbon](gather-acubens-belt-carbon.json) > [craft-steel-experiment](craft-steel-experiment.json) > [craft-steel-node-beta](craft-steel-node-beta.json) > [craft-piping-node-beta](craft-piping-node-beta.json) | 29 | Orders ENT-056, block ZERO: the reserve's short ores first (silicon, carbon, gold, nickel), each gather limited to what its field carries; P2: stored iron and copper become steel plate and piping where they lie. Gathers before crafts since 2026-11-21 (Zero): the crafts had taken the ships the short ores need. |
| reserve-hamal | Gather what the reserve lacks, then make: the short-ore fields in the other order so the division is spread, then steel plate and copper piping from own stores | mining, crafting, refining | [store-hold-central-nexus](store-hold-central-nexus.json) > [gather-acubens-belt-carbon](gather-acubens-belt-carbon.json) > [gather-jadecove-nickel](gather-jadecove-nickel.json) > [gather-tiaki-worldsend-nickel](gather-tiaki-worldsend-nickel.json) > [gather-subra-floodlight-flats-silicon](gather-subra-floodlight-flats-silicon.json) > [gather-goldcrest-gold](gather-goldcrest-gold.json) > [craft-steel-experiment](craft-steel-experiment.json) > [craft-steel-node-beta](craft-steel-node-beta.json) > [craft-piping-node-beta](craft-piping-node-beta.json) | 31 | Orders ENT-056, block ZERO: the reserve's short ores first, each gather limited to what its field carries; P2: stored iron and copper become steel plate and piping where they lie. Gathers before crafts since 2026-11-21 (Zero). |

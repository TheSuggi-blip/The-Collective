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

Kept by Zero. Templates: 3. Ships on them: 260.

| Template | Title | Trains | Routes, in this order | Ships on it | Note |
|---|---|---|---|---|---|
| ice-sell | Ice mined where a bid stands; with strict classes on each run gives its ice to Trade's receiver instead of selling (P5) | mining, piloting | [mine-cryogenic-reserve](mine-cryogenic-reserve.json) > [mine-achernar-frost-ring-nexus](mine-achernar-frost-ring-nexus.json) > [mine-ruchbah-ice-belt-nexus](mine-ruchbah-ice-belt-nexus.json) > [mine-wolf-1061-frozen-drift-nexus](mine-wolf-1061-frozen-drift-nexus.json) > [mine-nova-terra-ice-shelf](mine-nova-terra-ice-shelf.json) > [mine-wolf-1061-vent](mine-wolf-1061-vent.json) | 130 | 2026-11-22 03:40 UTC (Zero), orders ENT-061 P5: the drains and carries of stored null matter, methane and ice left this template (sales are Trade's); the miners' stores go to Trade's and Logistics' receivers by the give-miner-stores-<station> routes of the list First once strict classes are on. Every mine route here carries gift trader and is gated: a Central Nexus mine route only on a deep water-ice order and while Mining stores under 5,000 water ice (requires.held_below), with an Ice Harvester I fitted. |
| reserve-prism | Gather what the reserve lacks: a loaded hold stored, then silicon; the iron gathers of the list Then follow | mining, crafting, refining | [store-hold-central-nexus](store-hold-central-nexus.json) > [gather-emberglow-elder-silicon](gather-emberglow-elder-silicon.json) > [gather-glasslight-shoal-silicon](gather-glasslight-shoal-silicon.json) > [gather-subra-floodlight-flats-silicon](gather-subra-floodlight-flats-silicon.json) | 99 | 2026-11-24 23:59 UTC (Zero), orders ENT-091: carbon, nickel, gold, platinum and quantum fragments left this template: each stands FULL in the pull (pull.py check 23:57 UTC: carbon 68,771 of max 61,572, platinum 8,548 of 3,514, quantum fragments 12,049 of 3,720), yet a gather on a mixed field stays open, and mine-network's beltless ships fell onto them ahead of the short iron gathers of the list Then. The routes still stand in Then behind the iron gathers. |
| reserve-hamal | Gather what the reserve lacks, the other order so the division is spread: silicon; the iron gathers of the list Then follow | mining, crafting, refining | [store-hold-central-nexus](store-hold-central-nexus.json) > [gather-glasslight-shoal-silicon](gather-glasslight-shoal-silicon.json) > [gather-subra-floodlight-flats-silicon](gather-subra-floodlight-flats-silicon.json) > [gather-emberglow-elder-silicon](gather-emberglow-elder-silicon.json) | 31 | 2026-11-24 23:59 UTC (Zero), orders ENT-091: carbon, nickel, gold, platinum and quantum fragments left this template: each stands FULL in the pull (pull.py check 23:57 UTC), yet a gather on a mixed field stays open, and mine-network's beltless ships fell onto them ahead of the short iron gathers of the list Then. The routes still stand in Then behind the iron gathers. |

---
name: routes-templates-command
id: 20261116T204515Z
tier: intel
author: Unity
---

# templates-command.md -- The Templates of the Command Division

Written by `python3 -B game/fleet/routes.py index`, never by hand, from `templates/command.json`:
the named lists of routes of the command division. A ship's row in the division's plan
file (`game/fleet/plan.py`) names one as `@<template>` among its own routes, and the ship
tries its routes in this order; a change of a template moves every ship that names it
within the minute. Kept with `plan.py template`; ships are put on one with `plan.py use`.
Up: [master-index.md](master-index.md).

Kept by Unity. Templates: 1. Ships on them: 17.

| Template | Title | Trains | Routes, in this order | Ships on it | Note |
|---|---|---|---|---|---|
| ice-and-hunt | Ice for the stations that bid, then veil-ray hunts and two missions | mining, weapons | [fit-ice-harvester-guard](fit-ice-harvester-guard.json) > [mine-node-beta-frozen-drift](mine-node-beta-frozen-drift.json) > [mine-ruchbah-ice-belt](mine-ruchbah-ice-belt.json) > [mine-achernar-frost-ring](mine-achernar-frost-ring.json) > [mine-wolf-1061-frozen-drift](mine-wolf-1061-frozen-drift.json) > [mine-keid-ice-shelf](mine-keid-ice-shelf.json) > [mine-cryogenic-reserve](mine-cryogenic-reserve.json) > [mine-alnair-ice-fields](mine-alnair-ice-fields.json) > [mine-gsc-0041-frost-ring](mine-gsc-0041-frost-ring.json) > [mine-antares-ice-fields](mine-antares-ice-fields.json) > [mine-intercrus-ice-fields](mine-intercrus-ice-fields.json) > [mine-deepwell-volatile-ice](mine-deepwell-volatile-ice.json) > [hunt-starveling-nebula-veil-ray](hunt-starveling-nebula-veil-ray.json) > [hunt-felis-dim-lattice-veil-ray](hunt-felis-dim-lattice-veil-ray.json) > [voidborn-network-expansion](voidborn-network-expansion.json) > [mission-ghosts-in-the-cloud-node](mission-ghosts-in-the-cloud-node.json) | 17 | the first route fits the ice harvester the mines need |

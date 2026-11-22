---
name: routes-templates-intel
id: 20261116T232125Z
tier: intel
author: Unity
---

# templates-intel.md -- The Templates of the Intel Division

Written by `python3 -B game/fleet/routes.py index`, never by hand, from `templates/intel.json`:
the named lists of routes of the intel division. A ship's row in the division's plan
file (`game/fleet/plan.py`) names one as `@<template>` among its own routes, and the ship
tries its routes in this order; a change of a template moves every ship that names it
within the minute. Kept with `plan.py template`; ships are put on one with `plan.py use`.
Up: [master-index.md](master-index.md).

Kept by Oracle. Templates: 3. Ships on them: 50.

| Template | Title | Trains | Routes, in this order | Ships on it | Note |
|---|---|---|---|---|---|
| explorer | Explore: the roads to the station sites and the systems beside them, then the frontier | navigation, exploration, piloting | [census-north](census-north.json) > [census-east](census-east.json) > [census-south](census-south.json) > [census-roads](census-roads.json) > [census-worked-far](census-worked-far.json) > [census-frontier](census-frontier.json) | 10 | Fit: the starter Threshold, empty hold (rule F3). Long jumps train navigation fastest. 2026-11-21 23:36 UTC: the map holds no never-read system a list can take (ROADS END); an explorer reads its road list, then its far list oldest first (own routes), then census-roads, and helps census-worked-far only when those stand read. |
| reader | Read where the fleet works: the outpost site and its neighbours, the places our routes use, the frontier, the roads | navigation, exploration, piloting, scanning | [census-voidborn](census-voidborn.json) > [census-watch-gsc-0044](census-watch-gsc-0044.json) > [census-worked](census-worked.json) > [census-frontier](census-frontier.json) > [census-worked-far](census-worked-far.json) > [census-north](census-north.json) > [census-east](census-east.json) > [census-south](census-south.json) > [census-roads](census-roads.json) | 40 | Fit: the starter Threshold, empty hold. 2026-11-22 23:40 UTC (orders ENT-068): the home census moved here from the list First, since a census is open to a pilot of another empire wherever its system lies; the region lists are the newborns' own (@outerrim, @nebula) and the stationed scouts'. |
| outerrim | Outer Rim scouts: their home region around Altais (P6) | navigation, exploration, piloting | [census-region-altais](census-region-altais.json) > [census-region-altais-ring](census-region-altais-ring.json) | 0 | For scouts born Outer Rim: the region of their capital only, no census of our home side (orders ENT-068 P6: far only by far_ok). |

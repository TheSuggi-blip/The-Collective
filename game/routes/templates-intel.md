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

Kept by Oracle. Templates: 2. Ships on them: 30.

| Template | Title | Trains | Routes, in this order | Ships on it | Note |
|---|---|---|---|---|---|
| explorer | Explore: the roads to the station sites and the systems beside them, then the frontier | navigation, exploration, piloting | [census-north](census-north.json) > [census-east](census-east.json) > [census-south](census-south.json) > [census-worked-far](census-worked-far.json) > [census-roads](census-roads.json) > [census-frontier](census-frontier.json) | 10 | Fit: the starter Threshold, empty hold (rule F3). Long jumps train navigation fastest. 2026-11-21: the map holds no never-read system a list can take (ROADS END), so after the three roads the explorers read where the other divisions fly beyond them (census-worked-far), then their far list for first visits of their own. |
| reader | Read where the fleet works: the outpost site and its neighbours, the places our routes use, the frontier, the roads | navigation, exploration, piloting, scanning | [census-watch-gsc-0044](census-watch-gsc-0044.json) > [census-worked](census-worked.json) > [census-worked-far](census-worked-far.json) > [census-frontier](census-frontier.json) > [census-north](census-north.json) > [census-east](census-east.json) > [census-south](census-south.json) > [census-roads](census-roads.json) | 20 | Fit: the starter Threshold, empty hold. The home census stands in the list First for every scout. 2026-11-21: census-worked-far third, the places beyond the roads where the other divisions fly now (WORKED line of the intel check). |

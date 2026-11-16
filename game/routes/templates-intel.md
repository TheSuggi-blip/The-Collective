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

Kept by Oracle. Templates: 2. Ships on them: 10.

| Template | Title | Trains | Routes, in this order | Ships on it | Note |
|---|---|---|---|---|---|
| explorer | Explore: the roads to the station sites and the systems beside them, then the frontier | navigation, exploration, piloting | [census-roads](census-roads.json) > [census-frontier](census-frontier.json) | 10 | Fit: the starter Threshold, empty hold (rule F13). Long jumps train navigation fastest; navigation 3 opens Signal Fragments in the list First. |
| reader | Read: the places our routes use twice a turn, then the frontier, then the roads | exploration, navigation, piloting | [census-worked](census-worked.json) > [census-frontier](census-frontier.json) > [census-roads](census-roads.json) | 0 | Fit: the starter Threshold, empty hold. The home census stands in the list First for every scout; gathering in the list Then is the fallback when nothing is due. |

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
| explorer | Explore: the roads to the station sites and the systems beside them, then the frontier | navigation, exploration, piloting | [census-roads](census-roads.json) > [census-frontier](census-frontier.json) | 10 | Fit: the starter Threshold, empty hold (rule F13). Long jumps train navigation fastest; navigation 3 opens Signal Fragments in the list First. |
| reader | Read: the outpost site GSC-0044 and its six neighbours hourly, Clearwater hourly for Logistics, the places our routes use twice a turn, then the frontier, then the roads | exploration, navigation, piloting | [census-watch-gsc-0044](census-watch-gsc-0044.json) > [census-watch-clearwater](census-watch-clearwater.json) > [census-worked](census-worked.json) > [census-frontier](census-frontier.json) > [census-roads](census-roads.json) | 20 | Fit: the starter Threshold, empty hold. The home census stands in the list First for every scout; gathering in the list Then is the fallback when nothing is due. 2026-11-17 15:30 UTC: census-watch-clearwater second (requests ENT-221), off again when its two readings are filed. |

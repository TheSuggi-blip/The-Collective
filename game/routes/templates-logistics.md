---
name: routes-templates-logistics
id: 20261116T235833Z
tier: intel
author: Unity
---

# templates-logistics.md -- The Templates of the Logistics Division

Written by `python3 -B game/fleet/routes.py index`, never by hand, from `templates/logistics.json`:
the named lists of routes of the logistics division. A ship's row in the division's plan
file (`game/fleet/plan.py`) names one as `@<template>` among its own routes, and the ship
tries its routes in this order; a change of a template moves every ship that names it
within the minute. Kept with `plan.py template`; ships are put on one with `plan.py use`.
Up: [master-index.md](master-index.md).

Kept by Apollo. Templates: 1. Ships on them: 0.

| Template | Title | Trains | Routes, in this order | Ships on it | Note |
|---|---|---|---|---|---|
| stored-goods | Goods our haulers store, sold into a standing bid or carried to one: one ship a route, only the pilot that stores the good, only while a book of the last hour shows the bid | trading, navigation | [sell-soma-synchrony](sell-soma-synchrony.json) > [sell-soma-node-beta](sell-soma-node-beta.json) > [carry-soma-synchrony-node-alpha](carry-soma-synchrony-node-alpha.json) > [carry-soma-synchrony-node-gamma](carry-soma-synchrony-node-gamma.json) > [carry-soma-node-beta-node-alpha](carry-soma-node-beta-node-alpha.json) > [carry-soma-node-beta-node-gamma](carry-soma-node-beta-node-gamma.json) > [sell-plate-node-beta](sell-plate-node-beta.json) > [sell-plasma-node-beta](sell-plasma-node-beta.json) > [sell-liquid-hydrogen-central](sell-liquid-hydrogen-central.json) > [sell-liquid-hydrogen-node-beta](sell-liquid-hydrogen-node-beta.json) > [carry-liquid-hydrogen-node-beta-central](carry-liquid-hydrogen-node-beta-central.json) | 0 | Every route is gated by requires.stored and requires.bid: it opens for one pilot while its bid stands and closes by itself. It heads every hauler's list because a route behind standing work is never reached. |

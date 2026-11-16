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

Kept by Apollo. Templates: 3. Ships on them: 0.

| Template | Title | Trains | Routes, in this order | Ships on it | Note |
|---|---|---|---|---|---|
| stored-goods | Goods our haulers store, sold into a standing bid or carried to one: one ship a route, only the pilot that stores the good, only while a book of the last hour shows the bid | trading, navigation | [sell-soma-synchrony](sell-soma-synchrony.json) > [sell-soma-node-beta](sell-soma-node-beta.json) > [carry-soma-synchrony-node-alpha](carry-soma-synchrony-node-alpha.json) > [carry-soma-synchrony-node-gamma](carry-soma-synchrony-node-gamma.json) > [carry-soma-node-beta-node-alpha](carry-soma-node-beta-node-alpha.json) > [carry-soma-node-beta-node-gamma](carry-soma-node-beta-node-gamma.json) > [sell-plate-node-beta](sell-plate-node-beta.json) > [sell-plasma-node-beta](sell-plasma-node-beta.json) > [sell-liquid-hydrogen-central](sell-liquid-hydrogen-central.json) > [sell-liquid-hydrogen-node-beta](sell-liquid-hydrogen-node-beta.json) > [carry-liquid-hydrogen-node-beta-central](carry-liquid-hydrogen-node-beta-central.json) | 0 | Every route is gated by requires.stored and requires.bid: it opens for one pilot while its bid stands and closes by itself. It heads every hauler's list because a route behind standing work is never reached. |
| craft-reserve | Craft what we build with from the pilot's own stores: steel plate from stored iron ore at the Node Beta workshop, kept for the faction's ladder and the station | crafting, refining | [craft-steel-node-beta](craft-steel-node-beta.json) | 0 | Standing work, 0 cr a craft: requires.stored opens a route only for a pilot whose own storage holds the input, once per reading of the storage book (about 40 minutes). The board crafts wait on silicon or gold and run by hand (skill logistics-stock, stage.py). |
| gather-reserve | Fallback: gather iron and copper ore into storage at Node Beta for the reserve when no hauling or crafting stands open | mining | [gather-hamal-crystal-bloom](gather-hamal-crystal-bloom.json) > [gather-gsc-0027-prism-scatter](gather-gsc-0027-prism-scatter.json) > [gather-gsc-0027-spacetime-seep](gather-gsc-0027-spacetime-seep.json) | 0 | Shared fields: their max_ships count across the fleet and Mining claims up to 58 places on the first two (admirals.log ENT-001). min_left closes a field. Not judged on pay. |

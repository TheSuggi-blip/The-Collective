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

Kept by Apollo. Templates: 4. Ships on them: 124.

| Template | Title | Trains | Routes, in this order | Ships on it | Note |
|---|---|---|---|---|---|
| stored-goods | Goods our haulers store, sold into a standing bid or carried to one: one ship a route, only the pilot that stores the good, only while a book of the last hour shows the bid | trading, navigation | [sell-hydrogen-at-node-beta](sell-hydrogen-at-node-beta.json) > [sell-hydrogen-at-node-gamma](sell-hydrogen-at-node-gamma.json) > [carry-hydrogen-synchrony-to-experiment](carry-hydrogen-synchrony-to-experiment.json) > [sell-soma-at-node-beta](sell-soma-at-node-beta.json) > [sell-soma-at-synchrony](sell-soma-at-synchrony.json) > [sell-soma-at-experiment](sell-soma-at-experiment.json) > [carry-soma-beta-to-gamma](carry-soma-beta-to-gamma.json) > [carry-soma-synchrony-to-alpha](carry-soma-synchrony-to-alpha.json) > [sell-plate-node-beta](sell-plate-node-beta.json) > [sell-plasma-node-beta](sell-plasma-node-beta.json) > [sell-liquid-hydrogen-central](sell-liquid-hydrogen-central.json) > [sell-liquid-hydrogen-node-beta](sell-liquid-hydrogen-node-beta.json) > [carry-liquid-hydrogen-node-beta-central](carry-liquid-hydrogen-node-beta-central.json) | 40 | Every route is gated by requires.stored and requires.bid: it opens for one pilot while its bid stands and closes by itself. It heads every hauler's list because a route behind standing work is never reached. Since 2026-11-17 08:00 UTC the hydrogen and soma routes are Trade's (admirals.log ENT-011, ENT-012: open to every division, floors kept by Trade): haulers store 2,257 hydrogen gas at Node Beta and Node Gamma and 98 soma; Logistics' own soma routes (floor 500) stood under every bid (344 to 353) and are out of the template. |
| craft-reserve | Steel plate made from the pilot's own stored iron where it lies | crafting, refining | [craft-steel-node-beta](craft-steel-node-beta.json) > [craft-steel-central-nexus](craft-steel-central-nexus.json) > [craft-steel-synchrony-hub](craft-steel-synchrony-hub.json) | 40 | Node Beta first (most iron); Central Nexus and Synchrony Hub where a pilot stores 300 iron there. Any role may fly these routes (requests.log ENT-190). |
| gather-reserve | Fallback: gather iron and copper ore into storage at Node Beta for the reserve when no hauling or crafting stands open | mining | [gather-hamal-crystal-bloom](gather-hamal-crystal-bloom.json) > [gather-gsc-0027-prism-scatter](gather-gsc-0027-prism-scatter.json) > [gather-gsc-0027-spacetime-seep](gather-gsc-0027-spacetime-seep.json) | 40 | Shared fields: their max_ships count across the fleet and Mining claims up to 58 places on the first two (admirals.log ENT-001). min_left closes a field. Not judged on pay. |
| gas-harvest | Gas for the haulers with a Gas Harvester I: one ship a cloud, sold at the bid the route names, the rest stored | mining | [mine-antares-gas-cloud](mine-antares-gas-cloud.json) > [mine-amberfall-emission-nebula](mine-amberfall-emission-nebula.json) > [mine-deepwell-haze](mine-deepwell-haze.json) | 4 | Each route takes one ship; a route that loses twice is closed by the dispatcher for its six-hour window and opens again by itself (F22). Needs a Gas Harvester I fitted. The Experiment haze, Coldwater and GSC-0016 are Trade's claim (admirals.log ENT-004). |

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
| stored-goods | Goods our haulers store, sold into a standing bid or carried to one: one ship a route, only the pilot that stores the good, only while a book of the last hour shows the bid | trading, navigation | [sell-hydrogen-at-node-beta](sell-hydrogen-at-node-beta.json) > [sell-hydrogen-at-node-gamma](sell-hydrogen-at-node-gamma.json) > [sell-hydrogen-at-synchrony](sell-hydrogen-at-synchrony.json) > [carry-hydrogen-synchrony-to-experiment](carry-hydrogen-synchrony-to-experiment.json) > [sell-soma-at-node-beta](sell-soma-at-node-beta.json) > [sell-soma-at-synchrony](sell-soma-at-synchrony.json) > [sell-soma-at-experiment](sell-soma-at-experiment.json) > [carry-soma-beta-to-gamma](carry-soma-beta-to-gamma.json) > [carry-soma-synchrony-to-alpha](carry-soma-synchrony-to-alpha.json) > [carry-null-matter-beta-to-nexus](carry-null-matter-beta-to-nexus.json) > [sell-null-matter-at-nexus](sell-null-matter-at-nexus.json) > [sell-plasma-node-beta](sell-plasma-node-beta.json) > [sell-palladium-at-node-gamma](sell-palladium-at-node-gamma.json) > [carry-palladium-nexus-to-gamma](carry-palladium-nexus-to-gamma.json) > [sell-liquid-hydrogen-central](sell-liquid-hydrogen-central.json) > [sell-liquid-hydrogen-node-beta](sell-liquid-hydrogen-node-beta.json) > [carry-liquid-hydrogen-node-beta-central](carry-liquid-hydrogen-node-beta-central.json) | 40 | 2026-11-17 20:05 UTC: Trade's sell and carry routes that its template trade-sell opens to every division (each pilot sells its own stores, rule F24): hydrogen at Synchrony Hub and palladium at Node Gamma added; the two null matter tests stay Trade's claim (admirals.log ENT-053). Gated by requires.stored and requires.bid; one ship a route. |
| craft-reserve | Steel plate from each hauler's own stored iron at four workshops, then copper piping from stored plate and copper | crafting, refining | [craft-steel-logistics-experiment](craft-steel-logistics-experiment.json) > [craft-steel-logistics-node-beta](craft-steel-logistics-node-beta.json) > [craft-steel-logistics-synchrony-hub](craft-steel-logistics-synchrony-hub.json) > [craft-steel-logistics-central-nexus](craft-steel-logistics-central-nexus.json) > [craft-piping-plate-node-beta](craft-piping-plate-node-beta.json) | 40 | 2026-11-18: the reserve's iron is met, 31,440 plate still to make; piping nearly met (1,168 to make), so the piping route holds 2 ships |
| gather-reserve | Gather only what the reserve lacks: silicon at Glasslight Shoal | mining | [gather-glasslight-shoal-silicon](gather-glasslight-shoal-silicon.json) | 40 | 2026-11-18: iron and copper are met (orders ENT-052, P2); the iron and copper fields left the template. Silicon, carbon, gold and nickel fields within 8 jumps hold little and are claimed by Mining and Intel (table fields 00:07 UTC) |
| gas-harvest | Gas for the haulers with a Gas Harvester I: one ship a cloud, sold at the bid the route names, the rest stored | mining | [mine-achernar-gas-pocket](mine-achernar-gas-pocket.json) > [mine-lesath-gas-cloud](mine-lesath-gas-cloud.json) > [mine-amberfall-emission-nebula](mine-amberfall-emission-nebula.json) | 4 | Each route takes one ship; a route that loses twice is closed by the dispatcher for its six-hour window and opens again by itself (F22). Needs a Gas Harvester I fitted. Since 2026-11-17 08:10 UTC only clouds that sell and store at our own stations (Node Beta, Node Gamma), where Trade's hydrogen routes take what the gas bid leaves (sell-hydrogen-at-node-beta 35,532 cr a ship-hour, 4 hours to 07:52 UTC); Antares and Deepwell haze sold at Nova Terra Central and left 666 hydrogen and 122 plasma stored there, out of reach. The Experiment haze, Coldwater and GSC-0016 are Trade's claim (admirals.log ENT-012). |

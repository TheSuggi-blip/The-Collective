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

Kept by Apollo. Templates: 4. Ships on them: 80.

| Template | Title | Trains | Routes, in this order | Ships on it | Note |
|---|---|---|---|---|---|
| stored-goods | Goods our haulers store, sold into a standing bid or carried to one: one ship a route, only the pilot that stores the good, only while a book of the last hour shows the bid | trading, navigation | [sell-hydrogen-at-node-beta](sell-hydrogen-at-node-beta.json) > [sell-hydrogen-at-node-gamma](sell-hydrogen-at-node-gamma.json) > [sell-hydrogen-at-synchrony](sell-hydrogen-at-synchrony.json) > [carry-hydrogen-synchrony-to-experiment](carry-hydrogen-synchrony-to-experiment.json) > [sell-soma-at-node-beta](sell-soma-at-node-beta.json) > [sell-soma-at-synchrony](sell-soma-at-synchrony.json) > [sell-soma-at-experiment](sell-soma-at-experiment.json) > [carry-soma-beta-to-gamma](carry-soma-beta-to-gamma.json) > [carry-soma-synchrony-to-alpha](carry-soma-synchrony-to-alpha.json) > [carry-null-matter-beta-to-nexus](carry-null-matter-beta-to-nexus.json) > [sell-null-matter-at-nexus](sell-null-matter-at-nexus.json) > [sell-plasma-node-beta](sell-plasma-node-beta.json) > [sell-palladium-at-node-gamma](sell-palladium-at-node-gamma.json) > [carry-palladium-nexus-to-gamma](carry-palladium-nexus-to-gamma.json) > [sell-liquid-hydrogen-central](sell-liquid-hydrogen-central.json) > [sell-liquid-hydrogen-node-beta](sell-liquid-hydrogen-node-beta.json) > [carry-liquid-hydrogen-node-beta-central](carry-liquid-hydrogen-node-beta-central.json) | 40 | 2026-11-17 20:05 UTC: Trade's sell and carry routes that its template trade-sell opens to every division (each pilot sells its own stores, rule F24): hydrogen at Synchrony Hub and palladium at Node Gamma added; the two null matter tests stay Trade's claim (admirals.log ENT-053). Gated by requires.stored and requires.bid; one ship a route. |
| craft-reserve | Steel plate from each hauler's own stored iron at four workshops, then copper piping from stored plate and copper | crafting, refining | [craft-steel-logistics-experiment](craft-steel-logistics-experiment.json) > [craft-steel-logistics-node-beta](craft-steel-logistics-node-beta.json) > [craft-steel-logistics-synchrony-hub](craft-steel-logistics-synchrony-hub.json) > [craft-steel-logistics-central-nexus](craft-steel-logistics-central-nexus.json) > [craft-piping-plate-node-beta](craft-piping-plate-node-beta.json) | 40 | 2026-11-18: the reserve's iron is met, 31,440 plate still to make; piping nearly met (1,168 to make), so the piping route holds 2 ships |
| outpost-supply | What our outpost GSC-0044 takes: repair materials while its facilities are damaged, then fuel cells into its bunker while the reserve gate reads it under its floor; faction members only | navigation, piloting | [supply-repair-gsc-0044-boards](supply-repair-gsc-0044-boards.json) > [supply-repair-gsc-0044-plate](supply-repair-gsc-0044-plate.json) > [supply-bunker-gsc-0044](supply-bunker-gsc-0044.json) | 0 | 2026-11-21 20:20 UTC: the bunker and the Lockbox read damaged after the pause (faction_owned); the two repair routes are budgets (once, max_pilots), the bunker route opens under requires.reserve once the Fleet Admiral switches the gate on |
| train-hauler | The last standing work before park: jumps through our own stations for piloting (the freighter at 10) and navigation | piloting, navigation | [train-jumps-hauler](train-jumps-hauler.json) | 0 | 2026-11-21: a cost of fuel (about -165 cr a loop of 18 minutes on Trade's same loop); max_ships weighed each turn against the fleet's steady net |

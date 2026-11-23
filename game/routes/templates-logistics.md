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

Kept by Apollo. Templates: 6. Ships on them: 374.

| Template | Title | Trains | Routes, in this order | Ships on it | Note |
|---|---|---|---|---|---|
| stored-goods | Goods of Trade's class our haulers store, given to Trade's receivers at the station where they lie (P5); off until strict classes are on | navigation | [give-hauler-stores-node-beta](give-hauler-stores-node-beta.json) > [give-hauler-stores-node-gamma](give-hauler-stores-node-gamma.json) > [give-hauler-stores-nova-terra](give-hauler-stores-nova-terra.json) > [give-hauler-stores-central-nexus](give-hauler-stores-central-nexus.json) | 95 | 2026-11-22 04:10 UTC: orders ENT-061 P5: the 17 sell and carry circuits of this template left the plan; the four give routes stand off until data/fleet/strict-classes-on (requests.log ENT-332); the hydrogen stays ours for fuel cells |
| craft-reserve | Fuel cells from stored hydrogen gas, steel plate from each hauler's own stored iron at four workshops, then copper piping | crafting, refining | [craft-boards-stored-node-beta](craft-boards-stored-node-beta.json) > [craft-gold-wiring-synchrony-hub](craft-gold-wiring-synchrony-hub.json) > [craft-gold-wiring-experiment](craft-gold-wiring-experiment.json) > [craft-cells-hydrogen-node-beta](craft-cells-hydrogen-node-beta.json) > [craft-steel-logistics-experiment](craft-steel-logistics-experiment.json) > [craft-steel-logistics-node-beta](craft-steel-logistics-node-beta.json) > [craft-steel-logistics-synchrony-hub](craft-steel-logistics-synchrony-hub.json) > [craft-steel-logistics-central-nexus](craft-steel-logistics-central-nexus.json) > [craft-piping-plate-node-beta](craft-piping-plate-node-beta.json) | 95 | 2026-11-22 15:56 UTC Apollo: boards from stored silicon first (silicon binds the 23,808 short), gold wiring to 1,860, then steel (5,238 to make) and piping. Each opens only on the pilot's own stored inputs, so the receivers craft docked. |
| outpost-supply | What our outpost GSC-0044 takes: repair materials while its facilities are damaged, then fuel cells into its bunker while the reserve gate reads it under its floor; faction members only | navigation, piloting | [supply-repair-gsc-0044-boards](supply-repair-gsc-0044-boards.json) > [supply-repair-gsc-0044-plate](supply-repair-gsc-0044-plate.json) > [supply-bunker-gsc-0044-own-cells](supply-bunker-gsc-0044-own-cells.json) > [supply-bunker-gsc-0044](supply-bunker-gsc-0044.json) | 89 | 2026-11-22 04:10 UTC: the bunker first from our own cells at Node Beta while the reserve reads under the chain's keep of 5,000 (a test, F37 three runs), the buying route the backup under 4,000; repair stock as before |
| train-hauler | The last standing work before park: jumps through our own stations for piloting (the freighter at 10) and navigation | piloting, navigation | [train-jumps-hauler](train-jumps-hauler.json) | 95 | 2026-11-21: a cost of fuel (about -165 cr a loop of 18 minutes on Trade's same loop); max_ships weighed each turn against the fleet's steady net |
| newborn-rim | Outer Rim-born haulers: the once missions of Frontier Station, their home board (orders ENT-068 P6) | piloting, exploration | [mission-who-buys-old-charts-frontier](mission-who-buys-old-charts-frontier.json) > [mission-the-proposal-frontier](mission-the-proposal-frontier.json) > [mission-debris-field-reports-frontier](mission-debris-field-reports-frontier.json) > [mission-frontier-wayfinder-circuit-frontier](mission-frontier-wayfinder-circuit-frontier.json) | 0 | 2026-11-22 00:07 UTC Apollo: the 30 Outer Rim-born haulers start at Frontier Station; the shared once routes of its board, each capped by its own test (F37); no buy (the newborns hold 100 to 25,000 cr, the runner buys nothing under 3,000) |
| newborn-nebula | Nebula-born haulers: the once missions of Grand Exchange, their home board (orders ENT-068 P6) | piloting, exploration | [mission-federation-trade-route-prospectus-grand](mission-federation-trade-route-prospectus-grand.json) | 0 | 2026-11-22 00:07 UTC Apollo: the 25 Nebula-born haulers start at Grand Exchange; the shared once route of its board that needs no buy |

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

Kept by Apollo. Templates: 4. Ships on them: 154.

| Template | Title | Trains | Routes, in this order | Ships on it | Note |
|---|---|---|---|---|---|
| stored-goods | Goods of Trade's class our haulers store, given to Trade's receivers at the station where they lie (P5); off until strict classes are on | navigation | [give-hauler-stores-node-beta](give-hauler-stores-node-beta.json) > [give-hauler-stores-node-gamma](give-hauler-stores-node-gamma.json) > [give-hauler-stores-nova-terra](give-hauler-stores-nova-terra.json) > [give-hauler-stores-central-nexus](give-hauler-stores-central-nexus.json) | 40 | 2026-11-22 04:10 UTC: orders ENT-061 P5: the 17 sell and carry circuits of this template left the plan; the four give routes stand off until data/fleet/strict-classes-on (requests.log ENT-332); the hydrogen stays ours for fuel cells |
| craft-reserve | Fuel cells from stored hydrogen gas, steel plate from each hauler's own stored iron at four workshops, then copper piping | crafting, refining | [craft-cells-hydrogen-node-beta](craft-cells-hydrogen-node-beta.json) > [craft-steel-logistics-experiment](craft-steel-logistics-experiment.json) > [craft-steel-logistics-node-beta](craft-steel-logistics-node-beta.json) > [craft-steel-logistics-synchrony-hub](craft-steel-logistics-synchrony-hub.json) > [craft-steel-logistics-central-nexus](craft-steel-logistics-central-nexus.json) > [craft-piping-plate-node-beta](craft-piping-plate-node-beta.json) | 40 | 2026-11-22 00:15 UTC: fuel cells (keep fuel_cell all) from the hydrogen gas no bid takes, a test of one ship; steel as before (iron gifted to the hauler receivers once strict classes are on, queue.log ENT-201) |
| outpost-supply | What our outpost GSC-0044 takes: repair materials while its facilities are damaged, then fuel cells into its bunker while the reserve gate reads it under its floor; faction members only | navigation, piloting | [supply-repair-gsc-0044-boards](supply-repair-gsc-0044-boards.json) > [supply-repair-gsc-0044-plate](supply-repair-gsc-0044-plate.json) > [supply-bunker-gsc-0044](supply-bunker-gsc-0044.json) | 34 | 2026-11-22 00:15 UTC: both facilities ready again (faction_owned 2026-11-21 23:48 UTC); the repair routes keep the outpost's repair stock (boards by requires.reserve below 45, plate by three more loads of 60), the bunker opens under 4,000 by the reserve gate |
| train-hauler | The last standing work before park: jumps through our own stations for piloting (the freighter at 10) and navigation | piloting, navigation | [train-jumps-hauler](train-jumps-hauler.json) | 40 | 2026-11-21: a cost of fuel (about -165 cr a loop of 18 minutes on Trade's same loop); max_ships weighed each turn against the fleet's steady net |

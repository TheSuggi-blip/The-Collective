---
name: routes-templates-trade
id: 20261116T234540Z
tier: intel
author: Unity
---

# templates-trade.md -- The Templates of the Trade Division

Written by `python3 -B game/fleet/routes.py index`, never by hand, from `templates/trade.json`:
the named lists of routes of the trade division. A ship's row in the division's plan
file (`game/fleet/plan.py`) names one as `@<template>` among its own routes, and the ship
tries its routes in this order; a change of a template moves every ship that names it
within the minute. Kept with `plan.py template`; ships are put on one with `plan.py use`.
Up: [master-index.md](master-index.md).

Kept by Mercury. Templates: 2. Ships on them: 0.

| Template | Title | Trains | Routes, in this order | Ships on it | Note |
|---|---|---|---|---|---|
| trade-sell | Stored goods sold where a station bid stands: each ship sells its own stores, nothing bought | trading | [sell-soma-at-node-beta](sell-soma-at-node-beta.json) > [sell-soma-at-synchrony](sell-soma-at-synchrony.json) > [sell-soma-at-experiment](sell-soma-at-experiment.json) > [carry-soma-beta-to-gamma](carry-soma-beta-to-gamma.json) > [carry-soma-synchrony-to-alpha](carry-soma-synchrony-to-alpha.json) | 0 | Every route is gated by requires.stored (the pilot's own storage) and requires.bid (a book read within the hour at the floor); a run sells only what the bid takes. Open to every division's ships (rule F24). Starter hull, no module needed. |
| trade-craft | Goods made by hand for sale where a bid pays more than the inputs | crafting, trading | [craft-focused-crystal-node-beta](craft-focused-crystal-node-beta.json) | 0 | Inputs from the pilot's own storage at the workshop's station, at most one bought unit a run; the made good is sold into the bid named by requires.bid. A test until its first RESULT line. |

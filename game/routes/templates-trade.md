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

Kept by Mercury. Templates: 5. Ships on them: 143.

| Template | Title | Trains | Routes, in this order | Ships on it | Note |
|---|---|---|---|---|---|
| trade-sell | Stored goods sold where a station bid stands: each ship sells its own stores, nothing bought | trading | [sell-soma-at-node-beta](sell-soma-at-node-beta.json) > [sell-soma-at-synchrony](sell-soma-at-synchrony.json) > [sell-soma-at-experiment](sell-soma-at-experiment.json) > [carry-soma-beta-to-gamma](carry-soma-beta-to-gamma.json) > [carry-soma-synchrony-to-alpha](carry-soma-synchrony-to-alpha.json) > [sell-hydrogen-at-node-beta](sell-hydrogen-at-node-beta.json) > [sell-hydrogen-at-node-gamma](sell-hydrogen-at-node-gamma.json) > [carry-hydrogen-synchrony-to-experiment](carry-hydrogen-synchrony-to-experiment.json) | 40 | Every route is gated by requires.stored (the pilot's own storage) and requires.bid (a book read within the hour at the floor); a run sells only what the bid takes. Soma floor 350 (Central Nexus asks 292 in depth); hydrogen floor 30 (Ironlight asks 6 in depth). Routes written by sellgen.py of the trade-books skill. Open to every division's ships (rule F24). Starter hull, no module needed. |
| trade-craft | Goods made by hand for sale where a bid pays more than the inputs | crafting, trading | [craft-focused-crystal-node-beta](craft-focused-crystal-node-beta.json) | 40 | Inputs from the pilot's own storage at the workshop's station, at most one bought unit a run; the made good is sold into the bid named by requires.bid. A test until its first RESULT line. |
| trade-train-nav | Navigation trained to 3 on a loop of our five stations, for Signal Fragments (7,000 cr once) | navigation, piloting | [train-navigation-trader](train-navigation-trader.json) | 20 | requires.skills_below navigation 3: the route closes by itself at navigation 3, and Signal Fragments in the list First takes the pilot. About 4 navigation XP a jump, a loop of 17 to 18 minutes for about 165 cr of fuel. |
| trade-gas | Gas harvested and sold into the Node Beta and Central Nexus gas bids | mining | [mine-marfik-emission-nebula](mine-marfik-emission-nebula.json) > [mine-gsc-0016-emission-nebula](mine-gsc-0016-emission-nebula.json) > [mine-the-experiment-haze](mine-the-experiment-haze.json) > [mine-coldwater-emission-nebula](mine-coldwater-emission-nebula.json) > [mine-stellar-siphon](mine-stellar-siphon.json) > [mine-the-experiment-haze-synchrony](mine-the-experiment-haze-synchrony.json) | 3 | Needs a Gas Harvester I. One ship a route: the hydrogen and plasma bids take a few dozen units an hour; the loss stop closes a route whose last runs lost. |
| trade-gather | Fallback: iron and copper ore gathered into storage for the reserve when no trade is open | mining | [mine-pherkad-rift](mine-pherkad-rift.json) > [gather-hamal-crystal-bloom](gather-hamal-crystal-bloom.json) > [gather-gsc-0027-prism-scatter](gather-gsc-0027-prism-scatter.json) > [mine-acubens](mine-acubens.json) | 40 | Standing work (rule F8), never judged on its pay; shared fields with every division, each with its limit and iron floor. A trader on it is still offered every trade route before it. |

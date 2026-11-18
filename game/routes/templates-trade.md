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

Kept by Mercury. Templates: 3. Ships on them: 80.

| Template | Title | Trains | Routes, in this order | Ships on it | Note |
|---|---|---|---|---|---|
| trade-sell | Stored goods sold where a station bid stands: each ship sells its own stores, nothing bought | trading | [carry-null-matter-beta-to-nexus](carry-null-matter-beta-to-nexus.json) > [sell-null-matter-at-nexus](sell-null-matter-at-nexus.json) > [carry-null-matter-synchrony-nexus](carry-null-matter-synchrony-nexus.json) > [sell-soma-at-synchrony](sell-soma-at-synchrony.json) > [carry-soma-synchrony-to-alpha](carry-soma-synchrony-to-alpha.json) > [sell-soma-at-node-beta](sell-soma-at-node-beta.json) > [carry-soma-beta-to-gamma](carry-soma-beta-to-gamma.json) > [sell-soma-at-experiment](sell-soma-at-experiment.json) > [carry-palladium-nexus-to-gamma](carry-palladium-nexus-to-gamma.json) > [sell-palladium-at-node-gamma](sell-palladium-at-node-gamma.json) > [sell-hydrogen-at-node-beta](sell-hydrogen-at-node-beta.json) > [sell-hydrogen-at-node-gamma](sell-hydrogen-at-node-gamma.json) > [sell-hydrogen-at-synchrony](sell-hydrogen-at-synchrony.json) > [carry-hydrogen-synchrony-to-experiment](carry-hydrogen-synchrony-to-experiment.json) | 40 | 2026-11-17 19:42 UTC (Mercury, orders ENT-042): null matter leads: the Central Nexus bid read 200 to 210 cr for 7 to 295 units six times from 17:56 to 19:38 UTC (ledger.py prices null_matter), the only null matter bid in our books; floor 200 against Central Nexus' own ask of 213 to 220; carry-null-matter-beta-to-nexus and sell-null-matter-at-nexus are one-ship tests, carry-null-matter-synchrony-nexus is Mining's route, not claimed, one ship. Then soma 320 (cheapest ask 275 x 200,627 at Central Nexus; bids 342 to 343 x 5 to 17 at four stations), palladium 270 (cheapest ask 200 x 1; bid 548 x 2 at Synchrony Hub), hydrogen 30 (no home bid at 19:33 UTC). Every route gated by requires.stored and requires.bid; open to every division's ships (rule F24). Starter hull, no module. |
| trade-craft | Make from the pilot's own stores where they lie: copper piping, steel plate, then copper wiring | crafting, refining | [craft-piping-node-beta](craft-piping-node-beta.json) > [craft-piping-synchrony-hub](craft-piping-synchrony-hub.json) > [craft-steel-own-node-beta](craft-steel-own-node-beta.json) > [craft-steel-own-experiment](craft-steel-own-experiment.json) > [craft-steel-own-central-nexus](craft-steel-own-central-nexus.json) > [craft-wiring-synchrony-hub](craft-wiring-synchrony-hub.json) > [craft-wiring-node-beta](craft-wiring-node-beta.json) > [craft-wiring-experiment](craft-wiring-experiment.json) > [craft-steel-node-beta](craft-steel-node-beta.json) > [craft-steel-central-nexus](craft-steel-central-nexus.json) > [craft-steel-synchrony-hub](craft-steel-synchrony-hub.json) | 40 | 2026-11-17 23:41 UTC (Mercury, orders.log ENT-052 block MERCURY, requests.log ENT-256): the reserve's iron is met, so a trader without a paying trade makes before it gathers: piping and plate for the reserve first, then wiring from surplus copper; the -own- routes use up a pilot's stores at a station in one visit. |
| trade-train-nav | Navigation trained to 3 on a loop of our five stations, for Signal Fragments (7,000 cr once) | navigation, piloting | [train-navigation-trader](train-navigation-trader.json) | 0 | requires.skills_below navigation 3: the route closes by itself at navigation 3, and Signal Fragments in the list First takes the pilot. About 4 navigation XP a jump, a loop of 17 to 18 minutes for about 165 cr of fuel. |

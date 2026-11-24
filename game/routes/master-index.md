---
name: routes-master-index
id: 20261116T001237Z
tier: intel
author: Unity
---

# master-index.md -- Routes and Plans

Written by `python3 -B game/fleet/routes.py index`, never by hand. Start here: every
name below is a link into a sub-index of this folder. Each group of routes has its own
index (`index-<group>.md`) and each role its own plan (`plan-<role>.md`), so that no
file grows with the whole fleet. How a route is written, and what is automatic:
[BLUEPRINT.md](BLUEPRINT.md).

## Routes by Group

| Group | What it holds | Routes | Home space | Beyond the border | Best measured |
|---|---|---|---|---|---|
| [Once per Pilot](index-once-per-pilot.md) | Missions and rewards the game pays once per pilot: a new pilot's first work, and seed money. | 92 | 23 | 69 | mission-last-known-position-crimson: 8,030 cr a run |
| [Paying Routes](index-paying-routes.md) | Work that repeats and whose runs of the last 12 hours measured above zero. | 19 | 8 | 11 | sell-noble-at-first-step: 828,000 cr per ship-hour |
| [Tests](index-tests.md) | Work that repeats and has no measured figure: new, or no readable run in the last 12 hours. One ship until its first RESULT line is read. | 161 | 49 | 112 | not measured yet |
| [Fitting](index-fitting.md) | A module bought and fitted: the tool a kind of work needs. | 38 | 17 | 21 | strip-mining-laser-krynn: 1,170 cr per ship-hour |
| [Standing Work, Reading and Waiting](index-standing-work.md) | Standing work (it trains a skill or gathers into storage and is not judged on its pay), the census and the park route: they keep every ship busy and the picture fresh. | 542 | 113 | 429 | hunt-sandrift-ice-fields-hollow-pilgrim: 20,310 cr per ship-hour |
| [Measured at a Loss](index-measured-at-a-loss.md) | Work that repeats and whose runs of the last 12 hours measured zero or below. | 11 | 5 | 6 | mine-dheneb-cryobelt: -260 cr per ship-hour |
| [Off](index-off.md) | Written down, not flown. | 63 | 20 | 43 | voidborn-first-steps: 4,020 cr per ship-hour |
| All | | 926 | 235 | 691 | |

## Routes by Zone and Kind

| Zone | Routes | census | circuit | guard | hunt | mine | Farthest system, jumps from home |
|---|---|---|---|---|---|---|---|
| home space | 235 | 1 | 199 | 1 | 20 | 14 | 3 |
| beyond the border | 691 | 24 | 239 | 7 | 312 | 109 | 29 |

## Plans by Role

| Role | Kept by | Routes | The first three, in order | Planned | Ships |
|---|---|---|---|---|---|
| [command](plan-command.md) | Unity | 91 | voidborn-first-steps-board > voidborn-collective-provides > voidborn-signal-protocol | 0 | 9 |
| [drone](plan-drone.md) | Apophis | 352 | rearm-pulse-laser-central-nexus > voidborn-signal-fragments > voidborn-first-steps-board | 2 | 95 |
| [hauler](plan-hauler.md) | Apollo | 97 | voidborn-resonance-finish > voidborn-atmospheric-extraction > voidborn-hardware-cargo | 4 | 95 |
| [miner](plan-miner.md) | Zero | 124 | fit-mining-laser-iii-lhs-1140 > fit-mining-laser-ii-lhs-1140 > fit-mining-laser-ii-second-central-nexus | 5 | 130 |
| [scout](plan-scout.md) | Oracle | 98 | store-hold-central-nexus > store-hold-frontier-station-near > give-scout-stores-node-beta | 5 | 50 |
| [sentinel](plan-sentinel.md) | Apophis | 353 | rearm-pulse-laser-central-nexus > voidborn-signal-fragments > voidborn-first-steps-board | 2 | 36 |
| [trader](plan-trader.md) | Mercury | 179 | voidborn-first-steps-board > voidborn-network-expansion > voidborn-collective-provides | 1 | 85 |

## Templates by Division

Named lists of routes a ship's own routes in its division's plan file name as `@<template>`.

| Division | Kept by | Templates | Page |
|---|---|---|---|
| command | Unity | ice-and-hunt | [templates-command.md](templates-command.md) |
| intel | Oracle | explorer, reader, outerrim, nebula | [templates-intel.md](templates-intel.md) |
| logistics | Apollo | stored-goods, craft-reserve, outpost-supply, train-hauler, newborn-rim, newborn-nebula | [templates-logistics.md](templates-logistics.md) |
| military | Apophis | hunter, guard, krynn-newborn, sol-newborn | [templates-military.md](templates-military.md) |
| mining | Zero | ice-sell, reserve-prism, reserve-hamal | [templates-mining.md](templates-mining.md) |
| trade | Mercury | trade-sell, trade-craft, trade-train-nav | [templates-trade.md](templates-trade.md) |

## The Guidebooks

What each division learned about its routes, its levelling and its ships; kept by its Admiral, read by every member.

| Guidebook | Title |
|---|---|
| [guidebook/command/card.md](guidebook/command/card.md) | Command, chapters: [card](guidebook/command/card.md), [lessons](guidebook/command/lessons.md), [levelling](guidebook/command/levelling.md), [routes](guidebook/command/routes.md), [ships](guidebook/command/ships.md), [tests](guidebook/command/tests.md), [topic-design](guidebook/command/topic-design.md), [topic-systems](guidebook/command/topic-systems.md) |
| [guidebook/intel/card.md](guidebook/intel/card.md) | Intel, chapters: [card](guidebook/intel/card.md), [lessons](guidebook/intel/lessons.md), [levelling](guidebook/intel/levelling.md), [routes](guidebook/intel/routes.md), [ships](guidebook/intel/ships.md), [tests](guidebook/intel/tests.md) |
| [guidebook/logistics/card.md](guidebook/logistics/card.md) | Logistics, chapters: [card](guidebook/logistics/card.md), [lessons](guidebook/logistics/lessons.md), [levelling](guidebook/logistics/levelling.md), [routes](guidebook/logistics/routes.md), [ships](guidebook/logistics/ships.md), [tests](guidebook/logistics/tests.md), [topic-bases](guidebook/logistics/topic-bases.md), [topic-station](guidebook/logistics/topic-station.md) |
| [guidebook/military/card.md](guidebook/military/card.md) | Military, chapters: [card](guidebook/military/card.md), [lessons](guidebook/military/lessons.md), [levelling](guidebook/military/levelling.md), [routes](guidebook/military/routes.md), [ships](guidebook/military/ships.md), [tests](guidebook/military/tests.md), [topic-pirates](guidebook/military/topic-pirates.md) |
| [guidebook/mining/card.md](guidebook/mining/card.md) | Mining, chapters: [card](guidebook/mining/card.md), [lessons](guidebook/mining/lessons.md), [levelling](guidebook/mining/levelling.md), [routes](guidebook/mining/routes.md), [ships](guidebook/mining/ships.md), [tests](guidebook/mining/tests.md), [topic-missions](guidebook/mining/topic-missions.md), [topic-scripts](guidebook/mining/topic-scripts.md) |
| [guidebook/trade/card.md](guidebook/trade/card.md) | Trade, chapters: [card](guidebook/trade/card.md), [lessons](guidebook/trade/lessons.md), [levelling](guidebook/trade/levelling.md), [routes](guidebook/trade/routes.md), [ships](guidebook/trade/ships.md), [tests](guidebook/trade/tests.md) |

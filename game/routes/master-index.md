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
| [Once per Pilot](index-once-per-pilot.md) | Missions and rewards the game pays once per pilot: a new pilot's first work, and seed money. | 32 | 18 | 14 | voidborn-conductive-lattice: 9,110 cr a run |
| [Paying Routes](index-paying-routes.md) | Work that repeats and whose runs of the last 12 hours measured above zero. | 59 | 17 | 42 | drain-ice-node-alpha: 40,500 cr per ship-hour |
| [Tests](index-tests.md) | Work that repeats and has no measured figure: new, or no readable run in the last 12 hours. One ship until its first RESULT line is read. | 59 | 23 | 36 | not measured yet |
| [Fitting](index-fitting.md) | A module bought and fitted: the tool a kind of work needs. | 11 | 10 | 1 | fit-ice-harvester-lhs-1140: -4,320 cr per ship-hour |
| [Standing Work, Reading and Waiting](index-standing-work.md) | Standing work (it trains a skill or gathers into storage and is not judged on its pay), the census and the park route: they keep every ship busy and the picture fresh. | 93 | 25 | 68 | craft-boards-silicon-central-nexus: 156,690 cr per ship-hour |
| [Measured at a Loss](index-measured-at-a-loss.md) | Work that repeats and whose runs of the last 12 hours measured zero or below. | 50 | 4 | 46 | mine-wolf-1061-frozen-drift: -90 cr per ship-hour |
| [Off](index-off.md) | Written down, not flown. | 20 | 9 | 11 | voidborn-first-steps: 4,020 cr per ship-hour |
| All | | 324 | 106 | 218 | |

## Routes by Zone and Kind

| Zone | Routes | census | circuit | guard | hunt | mine | Farthest system, jumps from home |
|---|---|---|---|---|---|---|---|
| home space | 106 | 1 | 81 | 0 | 11 | 13 | 3 |
| beyond the border | 218 | 13 | 27 | 7 | 104 | 67 | 29 |

## Plans by Role

| Role | Kept by | Routes | The first three, in order | Planned | Ships |
|---|---|---|---|---|---|
| [command](plan-command.md) | Unity | 67 | voidborn-first-steps-board > voidborn-collective-provides > voidborn-signal-protocol | 0 | 6 |
| [drone](plan-drone.md) | Apophis | 107 | voidborn-signal-fragments > voidborn-first-steps-board > voidborn-network-expansion | 6 | 50 |
| [hauler](plan-hauler.md) | Apollo | 54 | voidborn-resonance-finish > voidborn-atmospheric-extraction > voidborn-hardware-cargo | 5 | 40 |
| [miner](plan-miner.md) | Zero | 59 | voidborn-signal-fragments > voidborn-first-steps-board > voidborn-network-expansion | 7 | 60 |
| [scout](plan-scout.md) | Oracle | 56 | store-hold-central-nexus > voidborn-first-steps-board > voidborn-network-expansion | 9 | 30 |
| [sentinel](plan-sentinel.md) | Unity | 89 | voidborn-first-steps-board > voidborn-collective-provides > voidborn-signal-protocol | 0 | 20 |
| [trader](plan-trader.md) | Mercury | 51 | voidborn-first-steps-board > voidborn-network-expansion > voidborn-collective-provides | 6 | 40 |

## Templates by Division

Named lists of routes a ship's own routes in its division's plan file name as `@<template>`.

| Division | Kept by | Templates | Page |
|---|---|---|---|
| command | Unity | ice-and-hunt | [templates-command.md](templates-command.md) |
| intel | Oracle | explorer, reader | [templates-intel.md](templates-intel.md) |
| logistics | Apollo | stored-goods, craft-reserve, gather-reserve, gas-harvest | [templates-logistics.md](templates-logistics.md) |
| military | Apophis | hunter, guard | [templates-military.md](templates-military.md) |
| mining | Zero | ice-sell, reserve-prism, reserve-hamal | [templates-mining.md](templates-mining.md) |
| trade | Mercury | trade-sell, trade-craft, trade-train-nav, trade-gas, trade-gather | [templates-trade.md](templates-trade.md) |

## The Guidebooks

What each division learned about its routes, its levelling and its ships; kept by its Admiral, read by every member.

| Guidebook | Title |
|---|---|
| [guidebook/intel.md](guidebook/intel.md) | intel.md -- Guidebook of the Intel Division |
| [guidebook/logistics.md](guidebook/logistics.md) | logistics.md -- Guidebook of the Logistics Division |
| [guidebook/military.md](guidebook/military.md) | military.md -- Guidebook of the Military Division |
| [guidebook/mining.md](guidebook/mining.md) | mining.md -- Guidebook of the Mining Division |
| [guidebook/trade.md](guidebook/trade.md) | trade.md -- Guidebook of the Trade Division |

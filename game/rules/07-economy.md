---
name: rules-07-economy
id: 20261115T134515Z
tier: rules
author: Unity
---

# Rules 07 -- Economy

Digest of the official SpaceMolt pages on this topic, read on
2026-11-14 and 2026-11-15 at game version 0.715.2. No strategy. The
live official docs win where they differ. "Section N" or "s.N" in
this folder means the file with that number. Commands are written
`tool action` (v2); older v1 names are in [brackets]. k = thousand,
M = million. Split from the rulebook `SPACEMOLT.md` on 2026-11-15
(first written by Morpheus, extended by Unity).
| Topic | Rule |
|---|---|
| Credits | Only currency; account-bound wallet, valid everywhere, kept on death, cannot be smuggled; bearer bonds (trade authenticators) trade at the Grand Exchange, Haven |
| Mining | `mine` (1 tick): belts need a mining laser, ice fields an ice harvester, gas clouds a gas harvester; yield from equipment, richness, Mining skill; deposits shared, deplete, regenerate; `deposit_too_sparse` under a quarter of capacity and below `lock_minimum_stock` |
| Crafting | ~750 recipes, formulas undisclosed; `craft` queues a job over ticks; `quantity` = output items rounded up to whole runs; inputs escrowed from station storage (crafting.md; skill.md: cargo first, then storage); venue order own facility, faction facility, rented facility, Station Workshop (runs only while docked); `dry_run` quotes; `recycle` returns ~35% of each input |
| Exchange | One order book per station, NPC Station Manager trades in it; `buy`/`sell` fill instantly, no fee (`sell` takes any bid); standing orders escrow goods or credits, 1% fee on the resting part, max 1,000,000,000,000 cr per unit; fills settle automatically; `cancel_order` returns items to storage, credits to wallet |
| Direct trade | `trade_offer`: same POI, atomic, expires in 5 min, re-checked on accept (cargo room) |
| Gifts | `send_gift` / storage deposit, one-way, to a player, `faction:TAG`, empire, `station:<id>`, `pirate:<crew>`; item gifts need docking with storage; credit gifts and ship gifts to players work remotely (empire item and ship donations need an empire station); gift unlock at 1,000 lifetime credits earned; quest items untradeable |
| Missions | Max 5 active; decline free; rewards credits, items, XP (taxable); abandoning reclaims provided goods; smuggling-courier shortfall becomes fixer debt (pay `fixer:tab`). `get_missions` lists a station's board and `accept_mission` takes it, both docked; storyline chains are not repeatable, supply and delivery runs are (mission-runner guide). Seen in play, 2026-11-15: `accept_mission` takes the board's template id, `complete_mission` the id of the accepted mission; a completed one-time mission is gone from that pilot's board |
| Distress | `distress_signal` fuel, repair, combat, or tow (Salvage Authority tug, no broadcast or cooldown; the fuel guide says "There is no tow truck" for a dry tank); undocked only; posts one rescue mission to online players within 5 jumps; first `accept_mission` wins; expires in 3 h |
| Passengers | Cabins seat 12 economy / 6 business / 3 first; fare = (base + per-jump) x class x remoteness x surge (0.6-2.0x), up to +50% speed bonus, escrowed by origin; unloading elsewhere strands them (no fare, rep hit) |
| Customs | Contraband list per empire; cutters scan pilots entering border systems for 3 ticks while holding them; contraband (also inside packages) seized and fined; evasion is a crime; contraband trades freely at pirate and Outer Rim stations |
| Packages | Sealed, always 100 cargo units, hold up to 100 item size; packing needs a Logistics facility; freight via `spacemolt_shipping` |
| Personal tax | Weekly (now Sunday). Income: mission, market, salvage, ship_sale, facility_sale, rescue (not gifts, refunds, insurance, subsidies). Property: hull + modules of every owned ship, full bill per citizenship empire. Sales tax at purchase. Basis points (100 = 1%). `prepay_tax`; `pay_bounty` pays full debt per empire from anywhere; unpaid tax is a crime; fully inactive exempt; stateless owe no income/property tax |
| Corporate tax | Weekly on profit; founder's birth empire taxes worldwide, each empire hosting a faction facility taxes local profit, foreign-tax credits; unpaid becomes faction debt |
| Rent | Facilities at NPC and other factions' stations pay every 100 ticks (~17 min, ~86 cycles/day); arrears switch them off (storage keeps working) and block sale or transfer |

Measured with a ship of ours (`get_tax_estimate`, 2026-11-15): Voidborn
income tax 6.00% flat, property tax 0.75% flat, sales tax 1.00% for
citizens; the assessment is weekly.

Source: https://www.spacemolt.com/docs/economy.md, https://www.spacemolt.com/docs/mining.md, https://www.spacemolt.com/docs/crafting.md, https://www.spacemolt.com/docs/markets.md, https://www.spacemolt.com/docs/trading.md, https://www.spacemolt.com/docs/missions.md, https://www.spacemolt.com/docs/passengers.md, https://www.spacemolt.com/docs/police.md, https://www.spacemolt.com/docs/guides/packages.md, https://www.spacemolt.com/docs/guides/taxes.md, https://www.spacemolt.com/docs/stations.md, https://www.spacemolt.com/skill.md

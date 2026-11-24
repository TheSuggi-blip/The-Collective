---
name: progression-roadmap
id: 20261122T212751Z
tier: governance
author: Trinity
links:
  - governance/the-collective-constitution.md
  - governance/strategy.md
  - governance/system-architecture.md
  - governance/knowledge-and-memory-loop.md
---

# The Collective -- Enterprise Progression Guide & Milestone Chronicle

Living strategic progression manual for The Collective (`[CLTV]`), tracking:
1. **Where we came from:** verified daily, weekly, and monthly milestones since
   Founding (`2026-11-14`).
2. **Where we stand right now:** live Consolidated Enterprise Value, fleet
   readiness, territory, and rate-limiting bottlenecks.
3. **Where we are going:** the three-horizon progression ladder (**Immediate Days ->
   Mid-Term Weeks -> Long-Term Months**) mapped directly to Suggi's Standing
   Orders (`S1-S5`) and Standing Goals (`G1-G5`).

The conceptual architecture below is human/architect-curated; the live metrics,
12-rung completion bars, milestone unlocks, and weekly/monthly financial ledgers
between the `PROGRESSION-AUTO` markers are refreshed automatically every hour by
`game/fleet/progression.py` (and served live at `/api/progression` on the
Command Station HUD under `Docs -> Progression`).

## 1. The Three Strategic Horizons

| Horizon | Core Objective | Governing Orders & Gates | Key Unlock |
| :-- | :-- | :-- | :-- |
| **Horizon 1: Days (Immediate)** | Flip 24h steady cashflow positive, commission first Tier-2 class hulls (`Resonance Miner`, `Recursion`, `Apophenia`), and found Frontier Outpost #2 (`Atria`). | `S1`, `S2`, `S3`, `F8`, `F17`, `F37` | 2.8x miner cargo holds, 3-weapon hunters, zero empty jump-loop burn, north-road staging bunker. |
| **Horizon 2: Weeks (1-3 Weeks)** | Seat all `246` Wave-3 ships (`400` cap via `Guild Hall`), standardize Tier-2 hulls + Tier-3 modules across divisions, complete up to `8` resource-monopoly outposts, and scale Station Bursar market-making (`contracts.log`). | `S2`, `S3`, `S4`, `G2`, `G3`, `G4`, `F11`, `F33`, `F39` | Full faction storage/tax synergy, high-margin regional arbitrage, self-feeding outpost supply chains. |
| **Horizon 3: Months (1-3+ Months)** | Construct Sovereign Station #1 at `Yildun` (`station_core_foundry` + `station_core`), expand armada to `500` ships (`G5`), launch civilian passenger lines (`G1`), unlock Tier-3/4 hulls + Tier-5 Flagship Mobile City (`F10`), and contend for Galactic Top-3 (`[BUSY]`, `[HEXC]`, `[IRLC]`). | `S1-S5`, `G1-G5`, `F10`, `F16` | Zero-fee sovereign industrial hub, 500-ship autonomous economy, mobile flagship city, multi-billion EV contention. |

## 2. Live Progression Gauges, Milestones & Period Ledgers

<!-- PROGRESSION-AUTO:BEGIN -->

### Live Enterprise Snapshot (Auto-Updated by `progression.py`)

| Metric | Live Value | Strategic Context |
| :--- | :--- | :--- |
| Campaign Day | Day 11 (since 2026-11-14) | Staggered 6-agent 6h autonomous cycle |
| Consolidated Enterprise Value | 59,011,304 cr | 25,855,182 cr purse (8,529,016 treasury) + 25,132,359 vault + 4,550,000 facilities + 3,473,763 hulls |
| Faction Seating & Standing Fleet | 261 / 500 (52.2%, cap 275) | 261 seated of 500 standing ships (14 open in current cap; 239 awaiting cap upgrades) -- voidborn 246, nebula 99, solarian 71, outerrim 43, crimson 41 |
| Hull Modernization | 11 / 500 upgraded (2.2%) | 489 T0 starter hulls left (3 T1, 8 T2+); 196 pilots P10+ (max P13) |
| Module Fit Saturation (T2-T5) | 155 / 500 ships (31.0%) | 345 ships unfitted; 226 / 2320 potential slots (9.7%; 1524 empty slots) |
| Territory & Exploration | 1 / 8 outposts, 0 / 5 stations | 506 / 506 galaxy systems charted |

### Strategic Rung Progress Across Horizons (Days -> Weeks -> Months)

| Horizon | Orders | Strategic Rung | Progress | Current State | Primary Rate-Limiting Step |
| :--- | :--- | :--- | ---: | :--- | :--- |
| Days (Now) | `G5, O7` | Full Galaxy Reconnaissance & Freshness Net | 100.0% | 506 / 506 systems charted (0 remaining) | All systems charted; maintain <3h market/belt freshness while trimming redundant census fuel |
| Days (Now) | `G4, O1, O3` | Enterprise Steady Cashflow Flip & Zero Empty Jump Burn | 95.0% | 1h -593517 cr/h | 24h -195922 cr/h | 95.0% productive flight-h | 392.0 ship-h/24h on jump loops (shift idle hulls to home-empire extraction, missions & zero-fuel crafting) |
| Days (Now) | `G2, O2` | First Tier-2 Hulls & Empire-Matched Fleet Upgrades | 100.0% | 8 T2+ active (3 T1, 489 T0 left) | 186 P10+ on T0 (196 P10+ total) | Resonance Miner 0% | Recursion 0% (186 P10+ pilots still on T0 (196 P10+ total)) |
| Days (Now) | `G3, O4` | Frontier Outpost #2 (Strategic Footprint Anchor) | 94.1% | 1 / 8 outposts active | next outpost kit 94.1% stocked | short: foil_scale 540, alloy_scale 212, graphene_thread 120 |
| Weeks (1-3w) | `G2, O5` | Faction Seating (261 / 500 Fleet, 52.2%, Cap 275) | 52.2% | 261 / 500 seated (52.2%, cap 275, 14 open now) | 239 standing ships awaiting future cap upgrades | 14 open seat(s) in current 275 cap | next cap facility: Guild Hall Recruiting (400) (0% stocked; short: iron_ore 30,000, carbon_ore 6,000, anchor_plate 1,200, silicon_ore 1,000 | fee 8,000,000 cr) |
| Weeks (1-3w) | `G2, O2` | Fleet Hull Modernization & T2-T5 Module Fit Saturation | 16.4% | 11/500 hulls upgraded (489 T0 left) | 155/500 ships T2+ fitted (345 unfitted; 226/2320 slots = 9.7%) | 345 ships still unfitted (1524 empty slots; 2094 slots below T2) | 186 P10+ pilots still on T0 (196 P10+ total) |
| Weeks (1-3w) | `G3, O4` | Maximal Footprint Outpost Network (Up to 8 Outposts) | 12.5% | 1 / 8 faction outposts active (7 open outpost slots) | 7 outpost slot(s) open; prioritize widest effective reach across multi-empire extraction & trade corridors |
| Weeks (1-3w) | `G4, O3` | Station Bursar Market-Making & Bottleneck Contract Desk | 100.0% | 8 contract(s) logged in contracts.log | Expand automated Bursar buy-bids & escrow volume across Nebula, Solarian, Outer Rim & Crimson capitals |
| Months (1-3m) | `G3, O4` | Sovereign Player Stations (Up to 5 Stations) | 73.8% | 0 / 5 stations | Foundry 73.2% | Core 86.0% | Purse 25.86M / 43M cr | short: iron_ore 204,809, anchor_plate 118,800, alloy_scale 54,200, silicon_ore 42,040, foil_scale 37,8 | fee 38,000,000 cr |
| Months (1-3m) | `G2, O5` | Multi-Empire Standing Fleet Consolidation (500 Ships) | 100.0% | 500 / 500 standing ships across 5 empires | 261 / 500 seated (52.2%, cap 275) | Fill 14 open seats in 275 cap & scale regional T2 corridors |
| Months (1-3m) | `G2, O2` | Passenger Lines, Tier-3/4 Capital Ships & Tier-5 Mobile City | 9.7% | Transit Lounge 5% | Max Piloting 13/50 | 0 at P20+ | 0 T3+ hulls | short: iron_ore 2,500, carbon_ore 408, silicon_ore 68 | fee 500,000 cr |
| Months (1-3m) | `G1-G5, O1-O9` | Top-3 Galactic Faction Supremacy | 11.8% | EV 59.01M cr | Live ranks: #5 members, #12 dmg, #20 fac | Compounding empire-matched T2/T3 fleet throughput & sovereign stations (top rival 9.5B cr) |

### Verified Milestone Chronicle

| Date (UTC) | Phase | Milestone | Verified Outcome |
| :--- | :--- | :--- | :--- |
| `2026-11-14` | Day 1 -- Founding | Constitution, 6-Division Charter & Five Admirals Born | The Collective [CLTV] chartered; Unity (Fleet Admiral) + Zero, Mercury, Apollo, Apophis, and Oracle initialized inside sealed gVisor unit. |
| `2026-11-15` | Day 2 -- Early Fleet | Initial Fleet Deployed (5 -> 50 Ships) & First Profitable Creature Hunts | Setpoint engine + container gate proven; starter missions (~22k cr/pilot) and early creature-good hunting established initial working capital. |
| `2026-11-16` | Day 3 -- Core Armada | 246-Ship Voidborn Armada, SQLite Warehouse & First Outpost (GSC-0044) | Scaled to 246 specialized ships (6 Cmd, 60 Min, 40 Trd, 40 Log, 70 Mil, 30 Int); store.py live.db->read.db pipeline & CLTV Outpost GSC-0044 built. |
| `2026-11-17` | Day 4 -- Faction & T1 | 100-Seat Offices, First Tier-1 Liminal Miner & 490+ Systems Mapped | Hiring Board + Recruitment Desk unlocked 100 faction seats; first Tier-1 Voidborn Liminal commissioned; declarative plan.py & supply chains live. |
| `2026-11-18` | Day 5 -- Lean Brain | Capped Versioned Guidebooks & Auto-Generated SQL Handbook | Monolithic guidebooks split into 6-8 capped chapters mirrored into doc_versions; game/handbook.md auto-generated from live store schema. |
| `2026-11-21` | Day 8 -- Pull Reserve | Shared Needs Register (needs.tsv) & Synchronous Admiral Self-Build | Priority-ordered pull reserve (needs.tsv -> need_status) unified division material targets; Admirals gained 1-call synchronous runner/script builds. |
| `2026-11-22` | Day 9 -- Enterprise Era | Constitution v9, 3-Tier Mandate (G1-G5 / O1-O9), 200 Seats & 506/506 Galaxy | Recruitment Center raised cap to 200; 506/506 galaxy charted; T3 lasers & Shield Booster II proven; 3-Tier Orders & multi-empire standing fleet launched. |
| `2026-11-24` | Live Auto-Unlock | Plan-500 Multi-Empire Standing Armada Active (500 Ships) | 500 standing ships across 5 empires (voidborn 246, nebula 99, solarian 71, outerrim 43, crimson 41). |
| `2026-11-24` | Live Auto-Unlock | First Tier-2 Hull Commissioned | 8 Tier-2+ hull(s) active in the fleet. |

### Rolling Weekly Performance Ledger (Bounded to Last 12 Weeks)

| ISO Week | Date Span | Active Hours | Steady Income | Operating Costs | Steady Net | Paid-Once Net | Peak Purse |
| :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| `2026-W47` | `2026-11-23..2026-11-24` | 36 | 4,165,863 cr | 9,953,751 cr | -5787888 cr | +22822884 cr | 26,013,507 cr |
| `2026-W46` | `2026-11-16..2026-11-22` | 76 | 5,700,253 cr | 5,532,119 cr | +168134 cr | +7490125 cr | 11,713,687 cr |

### Rolling Monthly Performance Ledger (Bounded to Last 12 Months)

| Month | Date Span | Active Hours | Steady Income | Operating Costs | Steady Net | Paid-Once Net | Peak Purse |
| :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| `2026-11` | `2026-11-16..2026-11-24` | 112 | 9,866,116 cr | 15,485,870 cr | -5619754 cr | +30313009 cr | 26,013,507 cr |

*Last live refresh: 2026-11-24 12:08 UTC (`game/fleet/progression.py`)*

<!-- PROGRESSION-AUTO:END -->

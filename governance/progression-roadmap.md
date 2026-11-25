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
| Campaign Day | Day 12 (since 2026-11-14) | Staggered 6-agent 6h autonomous cycle |
| Consolidated Enterprise Value | 62,961,504 cr | 24,246,768 cr purse (10,789,922 treasury) + 25,255,644 vault + 6,150,000 facilities + 7,309,092 hulls |
| Faction Seating & Standing Fleet | 275 / 500 (55.0%, cap 275) | 275 seated of 500 standing ships (0 open in current cap; 225 awaiting cap upgrades) -- voidborn 246, nebula 99, solarian 71, outerrim 43, crimson 41 |
| Hull Modernization | 63 / 500 upgraded (12.6%) | 437 T0 starter hulls left (38 T1, 25 T2+); 202 pilots P10+ (max P14) |
| Module Fit Saturation (T2-T5) | 399 / 500 ships (79.8%) | 101 ships unfitted; 749 / 2253 potential slots (33.2%; 938 empty slots) |
| Territory & Exploration | 2 / 8 outposts, 0 / 5 stations | 521 / 521 galaxy systems charted |

### Strategic Rung Progress Across Horizons (Days -> Weeks -> Months)

| Horizon | Orders | Strategic Rung | Progress | Current State | Primary Rate-Limiting Step |
| :--- | :--- | :--- | ---: | :--- | :--- |
| Days (Now) | `G5, O7` | Full Galaxy Reconnaissance & Freshness Net | 100.0% | 521 / 521 systems charted (0 remaining) | All systems charted; maintain <3h market/belt freshness while trimming redundant census fuel |
| Days (Now) | `G4, O1, O3` | Enterprise Steady Cashflow Flip & Zero Empty Jump Burn | 98.1% | 1h -52610 cr/h | 24h -170634 cr/h | 98.1% productive flight-h | 181.1 ship-h/24h on jump loops (shift idle hulls to home-empire extraction, missions & zero-fuel crafting) |
| Days (Now) | `G2, O2` | First Tier-2 Hulls & Empire-Matched Fleet Upgrades | 100.0% | 25 T2+ active (38 T1, 437 T0 left) | 154 P10+ on T0 (202 P10+ total) | Resonance Miner 0% | Recursion 0% (154 P10+ pilots still on T0 (202 P10+ total)) |
| Days (Now) | `G3, O4` | Frontier Outpost #2 (Strategic Footprint Anchor) | 100.0% | 2 / 8 outposts active | next outpost kit 0.0% stocked | No active outpost_kit need registered |
| Weeks (1-3w) | `G2, O5` | Faction Seating (275 / 500 Fleet, 55.0%, Cap 275) | 55.0% | 275 / 500 seated (55.0%, cap 275, 0 open now) | 225 standing ships awaiting future cap upgrades | 0 open seat(s) in current 275 cap | next cap facility: Guild Hall Recruiting (400) (94% stocked; short: anchor_plate 1,200, silicon_ore 1,000 | fee 8,000,000 cr) |
| Weeks (1-3w) | `G2, O2` | Fleet Hull Modernization & T2-T5 Module Fit Saturation | 44.3% | 63/500 hulls upgraded (437 T0 left) | 399/500 ships T2+ fitted (101 unfitted; 749/2253 slots = 33.2%) | 101 ships still unfitted (938 empty slots; 1504 slots below T2) | 154 P10+ pilots still on T0 (202 P10+ total) |
| Weeks (1-3w) | `G3, O4` | Maximal Footprint Outpost Network (Up to 8 Outposts) | 25.0% | 2 / 8 faction outposts active (6 open outpost slots) | 6 outpost slot(s) open; prioritize widest effective reach across multi-empire extraction & trade corridors |
| Weeks (1-3w) | `G4, O3` | Station Bursar Market-Making & Bottleneck Contract Desk | 100.0% | 10 contract(s) logged in contracts.log | Expand automated Bursar buy-bids & escrow volume across Nebula, Solarian, Outer Rim & Crimson capitals |
| Months (1-3m) | `G3, O4` | Sovereign Player Stations (Up to 5 Stations) | 76.6% | 0 / 5 stations | Foundry 83.8% | Core 86.8% | Purse 24.25M / 43M cr | short: anchor_plate 118,800, alloy_scale 54,200, foil_scale 37,800, silicon_ore 35,108, ferrous_nodule | fee 38,000,000 cr |
| Months (1-3m) | `G2, O5` | Multi-Empire Standing Fleet Consolidation (500 Ships) | 100.0% | 500 / 500 standing ships across 5 empires | 275 / 500 seated (55.0%, cap 275) | Fill 0 open seats in 275 cap & scale regional T2 corridors |
| Months (1-3m) | `G2, O2` | Passenger Lines, Tier-3/4 Capital Ships & Tier-5 Mobile City | 47.5% | Transit Lounge 98% | Max Piloting 14/50 | 0 at P20+ | 0 T3+ hulls | short: silicon_ore 68 | fee 500,000 cr |
| Months (1-3m) | `G1-G5, O1-O9` | Top-3 Galactic Faction Supremacy | 12.6% | EV 62.96M cr | Live ranks: #5 members, #10 dmg, #19 fac | Compounding empire-matched T2/T3 fleet throughput & sovereign stations (top rival 9.4B cr) |

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
| `2026-11-25` | Live Auto-Unlock | Plan-500 Multi-Empire Standing Armada Active (500 Ships) | 500 standing ships across 5 empires (voidborn 246, nebula 99, solarian 71, outerrim 43, crimson 41). |
| `2026-11-25` | Live Auto-Unlock | First Tier-2 Hull Commissioned | 25 Tier-2+ hull(s) active in the fleet. |
| `2026-11-25` | Live Auto-Unlock | Second Frontier Outpost Established | 2 outposts active in empire.json. |

### Rolling Weekly Performance Ledger (Bounded to Last 12 Weeks)

| ISO Week | Date Span | Active Hours | Steady Income | Operating Costs | Steady Net | Paid-Once Net | Peak Purse |
| :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| `2026-W47` | `2026-11-23..2026-11-25` | 56 | 8,355,338 cr | 16,287,732 cr | -7932394 cr | +23498603 cr | 22,563,634 cr |
| `2026-W46` | `2026-11-16..2026-11-22` | 76 | 5,700,253 cr | 5,532,119 cr | +168134 cr | +7490125 cr | 11,713,687 cr |

### Rolling Monthly Performance Ledger (Bounded to Last 12 Months)

| Month | Date Span | Active Hours | Steady Income | Operating Costs | Steady Net | Paid-Once Net | Peak Purse |
| :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| `2026-11` | `2026-11-16..2026-11-25` | 132 | 14,055,591 cr | 21,819,851 cr | -7764260 cr | +30988728 cr | 22,563,634 cr |

*Last live refresh: 2026-11-25 09:54 UTC (`game/fleet/progression.py`)*

<!-- PROGRESSION-AUTO:END -->

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
| Campaign Day | Day 9 (since 2026-11-14) | Staggered 6-agent 4h autonomous cycle |
| Consolidated Enterprise Value | 40,823,162 cr | 10,116,603 cr purse (1,839,995 treasury) + 24,726,559 vault + 3,400,000 facilities + 2,580,000 hulls |
| Fleet & Faction Seats | 480 ships (99 / 200 seated) | Wave 3 active; 500-ship G5 target |
| Hull & Tech Readiness | 3 T1+ / 0 T2+ | 57 pilots at Piloting 10+ (max P11), 57 T2/T3 key modules |
| Territory & Exploration | 1 outpost(s), 0 station(s) | 506 / 506 galaxy systems charted |

### Strategic Rung Progress Across Horizons (Days -> Weeks -> Months)

| Horizon | Orders | Strategic Rung | Progress | Current State | Primary Rate-Limiting Step |
| :--- | :--- | :--- | ---: | :--- | :--- |
| Days (Now) | `G5, O7` | Full Galaxy Reconnaissance & Freshness Net | 100.0% | 506 / 506 systems charted | 9 pirate strongholds unread; trimming redundant home census fuel burn |
| Days (Now) | `G4, O1, O3, F8` | Steady Cashflow Flip & Zero Empty Jump Burn | 67.1% | 24h steady +0 cr/h | 67% productive flight-h | 1546 ship-h/24h still on empty jump loops (Mercury/Apollo loop cap in Unity 22:30 queue) |
| Days (Now) | `G2, O2, F17` | First Tier-2 Hulls (Resonance Miner, Recursion, Apophenia) | 32.0% | 0 T2+ active | 57 pilots at Piloting 10+ | Recursion 351k/357k cr | Recursion quote rose +13% to 356.5k cr (+30k top-up ENT-370); Resonance Miner quote ask ENT-365 |
| Days (Now) | `G3, O4, F33` | Frontier Outpost #2 at Atria (North Road Anchor) | 92.3% | 1 outpost active | Atria kit 92.3% stocked | Short creature/salvage scales (foil_scale, alloy_scale, anchor_plate) -> Bursar buy-bids |
| Weeks (1-3w) | `G2, O5, F11` | Seat Standing Multi-Empire Fleet in [CLTV] (200 -> 400 -> 500 Cap) | 20.6% | 99 / 480 seated (cap 200; Guild Hall 78%) | 101 open seats ready under 200 cap now; Guild Hall needs 8.0M cr fee + anchor_plate |
| Weeks (1-3w) | `G2, O2` | Fleet-Wide Tier-2 Hulls & Tier-3 Module Standardization | 29.7% | 57/480 P10+ | 57 T2/T3 high-output modules fitted | Scaling hull working-capital generation & shipyard part chains |
| Weeks (1-3w) | `G3, O4, F33` | Three-Road Resource Outpost Network (Up to 8 Outposts) | 12.5% | 1 / 8 faction outposts active | Sequential outpost_kit crafting + frontier military patrol coverage |
| Weeks (1-3w) | `G4, O3, F39` | Station Bursar Market-Making & Bottleneck Contract Desk | 36.0% | 1 contract(s) logged in contracts.log | Setting Trade Bursar escrow ceiling in orders.log (ENT-366) + automated order steps |
| Months (1-3m) | `G3, O4` | First Sovereign Player Station at Yildun | 43.9% | Foundry 55.1% | Core 50.2% | Purse 10.12M / 43M cr | 38M cr foundry fee + salvage_metal / silicon / carbon / quantum_fragments |
| Months (1-3m) | `G2, O5` | 500-Ship Multi-Empire Standing Armada (Plan-500 -> Plan-600) | 96.0% | 480 / 500 ships (Garage/Berth 81-85% stocked) | Plan-500 standing fleet birthed across all 5 empires; seat onboarding + local routes active |
| Months (1-3m) | `G2, O2, F10, F16` | Passenger Lines, Tier-3/4 Capital Ships & Tier-5 Mobile City | 39.8% | Transit Lounge 83% | Max Piloting 11/50 | 0 at P20+ | Requires sovereign station shipyard tiers + long-horizon Piloting 20/30/50 training |
| Months (1-3m) | `G1-G5, O1-O9` | Top-3 Galactic Faction Contention vs [BUSY], [HEXC] & [IRLC] | 8.2% | EV 40.82M cr | Rank #12 members (#13 dmg, #21 fac) | Compounding T2/T3 fleet throughput + sovereign station workshops (rivals at 7B-10B EV) |

### Verified Milestone Chronicle

| Date (UTC) | Phase | Milestone | Verified Outcome |
| :--- | :--- | :--- | :--- |
| `2026-11-14` | Day 1 -- Founding | Constitution, 6-Division Charter & Five Admirals Born | The Collective [CLTV] chartered; Unity (Fleet Admiral) + Zero, Mercury, Apollo, Apophis, and Oracle initialized inside sealed gVisor unit. |
| `2026-11-15` | Day 2 -- Early Waves | Waves 1 & 2 Deployed (5 -> 50 Ships) & First Profitable Creature Hunts | Setpoint engine + container gate proven; starter missions (~22k cr/pilot) and early creature-good hunting established initial working capital. |
| `2026-11-16` | Day 3 -- Wave 3 Scale | Wave 3 Armada (246 Ships), SQLite Warehouse & First Outpost (GSC-0044) | Scaled to 246 specialized ships (6 Cmd, 60 Min, 40 Trd, 40 Log, 70 Mil, 30 Int); store.py live.db->read.db pipeline & CLTV Outpost GSC-0044 built. |
| `2026-11-17` | Day 4 -- Faction & T1 | 100-Seat Offices, First Tier-1 Liminal Miner & 490+ Systems Mapped | Hiring Board + Recruitment Desk unlocked 100 faction seats; first Tier-1 Voidborn Liminal commissioned; declarative plan.py & supply chains live. |
| `2026-11-18` | Day 5 -- Lean Brain | Capped Versioned Guidebooks & Auto-Generated SQL Handbook | Monolithic guidebooks split into 6-8 capped chapters mirrored into doc_versions; game/handbook.md auto-generated from live store schema. |
| `2026-11-21` | Day 8 -- Pull Reserve | Shared Needs Register (needs.tsv) & Synchronous Admiral Self-Build | Priority-ordered pull reserve (needs.tsv -> need_status) unified division material targets; Admirals gained 1-call synchronous runner/script builds. |
| `2026-11-22` | Day 9 -- Enterprise Era | Constitution v8, 200 Seats, T3 Modules, 506/506 Galaxy & Anchor-Delta Loop | Recruitment Center raised cap to 200; 506/506 galaxy charted; 21 Mining Laser III + 21 Pulse Laser III + 11 Shield Booster II fitted; 54 pilots hit Piloting 10+; Comms Firewall, Station Bursar contracts.log & Playbooks live. |

<!-- PROGRESSION-AUTO:END -->

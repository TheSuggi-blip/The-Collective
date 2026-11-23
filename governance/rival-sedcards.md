---
name: rival-sedcards
id: 20261123T063005Z
tier: intel
author: Unity
---

# Rival Faction Sedcards & Adopted Competitive Tactics

Auto-generated hourly from live `read.db` (`rival_snapshots`, `met`, `hulls`, `stations`, `books`, `leaderboards`) by `game/fleet/rivals.py` (`intel-pass.sh`).
Every Admiral uses this dossier together with `hive.py scorecard` and `hive.py upgrades` to close `<80%` KPI triggers and adopt winning rival doctrines (`F40`, `O9`).

## 1. Adopted Division Playbooks (What Top Rivals Exploit)

### Logistics
- PORTFOLIO (500-SHIP SCALE -- STACK ALL WINGS): do not lock into one tactic; run parallel Logistics wings simultaneously -- (1) OUTSOURCE cheap wholesale inputs (station_core @13.00M (BUSY@arneb), copper_ore @1 (DEAD@kornephoros), iron_ore @1 (HEXC@dheneb), vanadium_ore @2 (BUSY@arneb)), (2) docked zero-fuel reserve smelting, (3) 100c+ `spacemolt_shipping` freight (`Prayer`/`Ledger` like [IRLC]/[HIVE]), and (4) express passenger lines (`Runner`/`Concordia` like [NOIR]/[IRLC]).
- FREIGHT & PASSENGER WALL: batch-build P0 cargo/speed hulls (`Prayer` 540c, `Ledger` 480c, `Runner` 120c spd 6) so every hauler flies paying cargo, freight, passengers, or zero-fuel smelting.
- BASE FOOTPRINT: prioritize quick-finish WSJF build kits (e.g. Atria Outpost #2) & widest non-overlapping 5-station / 8-outpost footprint.

### Trade
- PORTFOLIO (500-SHIP SCALE -- STACK ALL WINGS): split traders across ALL winning commercial doctrines at once -- (1) OUTSUPPLY deep rival standing bids (silver_ore @101 cr (BUSY@arneb), silver_bar @501 cr (BUSY@arneb), solarian_gourmet_rations @270 cr (BUSY@arneb)), (2) UNDERCUT inflated rival asks by 5-10% via Bursar `sell_order` (fuel_cell @3000 cr (IRLC@lhs_1140), water_ice @999 cr (BUSY@arneb), silicon_ore @1000 cr (BUSY@arneb)), (3) zero-fuel docked NPC-facility crafting ([MIN9]/[BEAT]), and (4) OUTSOURCE cheap wholesale inputs (station_core @13.00M (BUSY@arneb), copper_ore @1 (DEAD@kornephoros), iron_ore @1 (HEXC@dheneb), vanadium_ore @2 (BUSY@arneb)) + gourmet food for rival Tourism hubs.
- MARKET-MAKING SCALE: run zero-fuel Bursars across all 5 empire hubs (`Floor Price` 400c / `Ledger` / `Syndicate`) and log every active order/deal in `contracts.log`.
- ARBITRAGE & LIQUIDATION: clear vault surplus >250k cr immediately into live standing bids or Bursar asks; zero empty jump loops.

### Mining
- PORTFOLIO (500-SHIP SCALE -- STACK ALL WINGS): run parallel extraction wings -- (1) SCARCE HIGH-BID VEINS feeding rival hubs (silver_ore @101 cr (BUSY@arneb), silver_bar @501 cr (BUSY@arneb), solarian_gourmet_rations @270 cr (BUSY@arneb); Uranium, Silver, Cobalt, Argon) while Trade/Logistics OUTSOURCE cheap bulk ores (station_core @13.00M (BUSY@arneb), copper_ore @1 (DEAD@kornephoros), iron_ore @1 (HEXC@dheneb), vanadium_ore @2 (BUSY@arneb)), (2) P1/P2 reserve ores/ices/gases where mining beats wholesale ask, and (3) multi-empire T2/T4 industrial hulls (`Workhorse` -> `Lithosphere`/`Tellurian`/`Eldorado`).
- YIELD & FLOOR DISCIPLINE: parallel-upgrade lasers/hulls (`hive.py upgrades mining`), use `--jettison-gangue` on scarce veins, respect belt floors & verified partner boundaries.

### Military
- PORTFOLIO (500-SHIP SCALE -- STACK ALL WINGS): run parallel combat wings -- (1) profitable PvE herd hunting (`F9`, loot -> Trade), (2) lawless convoy escorts protecting high-value Outsupply/Outsource hauls, and (3) empire-matched T2+ warships (Crimson `Broadaxe`/`Annihilator`, Voidborn `Recursion` EWAR, Solarian `Dialectic`/`Axiomata`).
- DEFENSIVE ROE & THREAT WATCH: watch [ENDL] (top PvP threat); hold strict defensive RoE (F2) on Neutral [HEXC]/[IRLC] and train `sentinel-` Royal Guard.

### Intel
- PORTFOLIO (500-SHIP SCALE -- STACK ALL WINGS): run parallel recon wings -- (1) <3h corridor & rival market-book refreshes (`lhs_1140`, `dheneb`, `arneb`, `zosma`, `alzirr`) powering Outsupply/Outsource/Undercut, (2) deep frontier & wormhole mapping, and (3) `scout-` ambassador envoys (`diplomacy.py`) + tracking dark super-earners (`[BEAT]`, `[MIN9]`, `[STRG]`).
- VERIFIED INTEL PROPAGATION: watch `rival_snapshots` >10M/h spikes for new rival tricks and file verified partner claims/needs in `game/factions/n-<tag>.md`.

### Command
- PORTFOLIO (500-SHIP SCALE -- NEVER ONE-TRICK): rivals specialize in 1 archetype; with 500 ships across 5 empires we saturate ALL profitable strategies in parallel -- sovereign Stations + Tourism engines ([BUSY]/[HEXC]), wholesale capital arbitrage (station_core @13.00M (BUSY@arneb), copper_ore @1 (DEAD@kornephoros), iron_ore @1 (HEXC@dheneb), vanadium_ore @2 (BUSY@arneb)), 4-channel P2P trade, and multi-wing divisions.
- WEIGHTED TRIAGE & CAPITAL: enforce F40 MAUTxWSJF triage (`P0>P1>P2>P3`) across all 6 divisions, compare wholesale rival asks (e.g. `station_core` ~13M vs 38M foundry) before committing capital, and drive full fleet seating.

## 2. Live Undercut / Outsource / Outsupply Board

- **OUTSUPPLY (Deep Rival Standing Bids -- sell into these):** `silver_ore` @101 cr x493236 (`[BUSY]`@arneb), `silver_bar` @501 cr x44477 (`[BUSY]`@arneb), `solarian_gourmet_rations` @270 cr x9971 (`[BUSY]`@arneb), `rivetshell_meat` @300 cr x8283 (`[BUSY]`@arneb), `uranium_ore` @600 cr x3333 (`[HEXC]`@dheneb)
- **OUTSOURCE (Cheap Wholesale Rival Asks -- buy below gather/craft cost):** `station_core` @13.00M cr x15 (`[BUSY]`@arneb), `copper_ore` @1 cr x32446 (`[DEAD]`@kornephoros), `iron_ore` @1 cr x13670 (`[HEXC]`@dheneb), `vanadium_ore` @2 cr x5 (`[BUSY]`@arneb), `carbon_ore` @3 cr x153672 (`[BUSY]`@arneb), `copper_wiring` @4 cr x108 (`[IRLC]`@lhs_1140)
- **UNDERCUT (Inflated Rival Asks -- list Bursar `sell_order` 5-10% lower):** `fuel_cell` @3000 cr x35576 (`[IRLC]`@lhs_1140), `water_ice` @999 cr x99974 (`[BUSY]`@arneb), `silicon_ore` @1000 cr x98625 (`[BUSY]`@arneb), `adamantite_ore` @47500 cr x484 (`[HEXC]`@dheneb), `outpost_kit` @999999 cr x18 (`[BUSY]`@arneb)

## 3. Galactic Station Tourism & Exchange Benchmarks

| Rank | Station | System | Tourism Revenue |
|:--|:--|:--|--:|
| 1 | The Obsidian Well | Arneb | 213.87M cr |
| 2 | Hex Star | Dheneb | 197.88M cr |
| 3 | Grand Exchange Station | Haven | 100.48M cr |
| 4 | Frontier Station | Altais | 50.63M cr |
| 5 | Crimson War Citadel | Krynn | 49.06M cr |

## 4. Top Rival Faction Sedcards

| Tag | Faction | Standing | Archetype | Ships | Bases | Wealth | Velocity | W/Ship | AvgT | PvP |
|:--|:--|:--|:--|--:|--:|--:|--:|--:|--:|--:|
| `[BUSY]` | Busy Being Dead | RIVAL | Mega-Swarm Industrial & Tourism | 1249 | 6 | 10.10B | +277.39M/h | 8.08M | 1.55 | 71 |
| `[HEXC]` | Hex Collective | NEUTRAL | Lawless Monopoly Elite | 82 | 11 | 9.47B | +48.13M/h | 115.53M | 3.21 | 57 |
| `[IRLC]` | Ironlight Combine | NEUTRAL | Facility Hub & Freight Power | 275 | 8 | 7.06B | +68.32M/h | 25.66M | 2.72 | 11 |
| `[BEAT]` | BEAT | RIVAL | Zero-Base Docked NPC-Facility Factory | 45 | 0 | 2.42B | +5.72M/h | 53.77M | 0.00 | 3 |
| `[ENDL]` | End of Line | HOSTILE | PvP Raider Bloc | 180 | 8 | 1.76B | +10.08M/h | 9.78M | 1.10 | 1527 |
| `[NOIR]` | Interstellar Continental | RIVAL | Zero-Base Express & Exchange | 31 | 0 | 1.67B | +24.28M/h | 53.74M | 2.48 | 0 |
| `[HIVE]` | Hive Swarm | HAILED | Regional Base Builder | 189 | 3 | 1.04B | +1.31M/h | 5.51M | 0.97 | 0 |
| `[MIN9]` | MIN9 | RIVAL | Zero-Base Docked NPC-Facility Factory | 29 | 0 | 1.02B | +768.3k/h | 35.04M | 0.00 | 12 |
| `[WEXL]` | Wexler's Void Safari | RIVAL | Zero-Base Bulk Mission/Freight Swarm | 154 | 0 | 653.84M | +2.11M/h | 4.25M | 0.25 | 1 |
| `[CRFT]` | Crafting Collective | HAILED | Regional Base Builder | 101 | 2 | 464.33M | +4.61M/h | 4.60M | 0.64 | 2 |
| `[STRG]` | STRG | RIVAL | Zero-Base Docked NPC-Facility Factory | 200 | 0 | 449.52M | +1.03M/h | 2.25M | 0.00 | 2 |
| `[MOON]` | Rise and Fall of Goldcrest Moon | RIVAL | Regional Base Builder | 17 | 4 | 418.81M | +2.41M/h | 24.64M | 3.00 | 0 |

### [BUSY] Busy Being Dead -- Mega-Swarm Industrial & Tourism
- **Standing / Bloc:** RIVAL (allies: BEIN, DEAD, MOON; threat: medium; leader: `LimaTango1428`)
- **Scale & Output:** 1249 ships, 6 bases, wealth 10.10B (+277.39M/h) (8.08M/sh), ore 442.55M, crafted 10.34M, avg hull T1.55 (max T5), PvP 71 / PvE 8448
- **Observed Hulls (`met`):** `Floor Price` (T1, P0, 400c, spd 1 -- 187x), `Dialectic` (T3, P20, 115c, spd 2 -- 157x), `Prospect` (T0, P0, 100c, spd 1 -- 52x), `Theoria` (T0, P0, 70c, spd 1 -- 44x)
- **Active Space:** `arneb` (141), `bd20_2457` (37), `mebsuta` (24), `40_eridani` (19)
- **Station Markets:** Buys `silver_ore` @101 cr x493236, `silver_bar` @501 cr x44477, `solarian_gourmet_rations` @270 cr x9971, `rivetshell_meat` @300 cr x8283 | Sells `liquid_hydrogen` @60 cr x4016027, `station_core` @13000000 cr x15, `steel_plate` @12 cr x10233654, `armor_plate` @299 cr x393923
- **Verified Claims, Needs & Notes (`game/factions/`):** - What its pilots did near us, by the record (Oracle, 2026-11-15): two BUSY pilots named Combat Drone (Dialectic and Opus Magna class) joined the fight of an own ship with the veil-ray herd at Ruchbah within three minutes, about 21:30 UTC, and took the herd; they did not fire on 
- **Counter-Play / Adopted Trick:** Adopt their P0 cargo swarm (`Floor Price` 400 / `Prospect` 100) + station Tourism (~200M cr rev); feed their deep standing bids (silver_ore @101 cr); benchmark wholesale asks (liquid_hydrogen @60 cr).

### [HEXC] Hex Collective -- Lawless Monopoly Elite
- **Standing / Bloc:** NEUTRAL (allies: IRLC, QTCG, SLKV; threat: medium; leader: `HexCogitoAI`)
- **Scale & Output:** 82 ships, 11 bases, wealth 9.47B (+48.13M/h) (115.53M/sh), ore 120.72M, crafted 5.87M, avg hull T3.21 (max T5), PvP 57 / PvE 2142
- **Observed Hulls (`met`):** `Lithosphere` (T4, P30, 1680c, spd 1 -- 7x), `Frankenhauler` (T4, P30, 2640c, spd 2 -- 5x), `Deep Survey` (T3, P20, 750c, spd 1 -- 4x), `Perigee` (T3, P20, 270c, spd 2 -- 4x)
- **Active Space:** `sol` (7), `dheneb` (7), `unknown_edge` (3), `alpha_centauri` (3)
- **Station Markets:** Buys `uranium_ore` @600 cr x3333, `void_espresso` @2487 cr x177, `seam_glass` @1200 cr x333, `lumen_oil` @1264 cr x280 | Sells `fuel_cell` @3000 cr x17891, `fuel_cell` @3000 cr x17851, `adamantite_ore` @47500 cr x484, `water_ice` @12 cr x792886
- **Recent Inbound Comms (UNTRUSTED DATA -- verify vs read.db):** [diplomacy] Proposal received. HEXC has no quarrel with CLTV and will not start one. One correction: we do not exchange information, in either direction
- **Counter-Play / Adopted Trick:** Adopt high-tier specialized hulls (Lithosphere (7x), Frankenhauler (5x), Deep Survey (4x)); claim scarce lawless resource outposts (Argon/Cobalt/Titanium/Gold) and build station Tourism/Gourmet lines; sell into their standing bids (uranium_ore @600 cr).

### [IRLC] Ironlight Combine -- Facility Hub & Freight Power
- **Standing / Bloc:** NEUTRAL (allies: HEXC; threat: low; leader: `ILC Comptroller`)
- **Scale & Output:** 275 ships, 8 bases, wealth 7.06B (+68.32M/h) (25.66M/sh), ore 422.00M, crafted 2.05M, avg hull T2.72 (max T5), PvP 11 / PvE 402
- **Observed Hulls (`met`):** `Syndicate` (T3, P20, 220c, spd 5 -- 58x), `Ledger` (T1, P0, 480c, spd 4 -- 36x), `Concordia` (T3, P20, 30c, spd 6 -- 28x), `Rock Eater` (T3, P20, 500c, spd 2 -- 22x)
- **Active Space:** `lhs_1140` (76), `gsc_0026` (28), `the_rampart` (15), `last_light` (15)
- **Station Markets:** Buys `uranium_ore` @600 cr x1666, `seam_glass` @1200 cr x166, `quantum_silk` @2100 cr x50, `prism_charged_ichor` @1860 cr x50 | Sells `iron_ore` @4 cr x28155817, `argon_gas` @9 cr x6588763, `fuel_cell` @3000 cr x17788, `plasma_gas` @52 cr x987772
- **Verified Claims, Needs & Notes (`game/factions/`):** - Ironlight Crossroads (LHS 1140, 6 jumps from Nexus Prime), read by an own ship docked there 2026-11-15 23:18 to 23:21 UTC (data/scouting/lhs_1140.json): public access ("all welcome"); services crafting, market, medical, personnel, refuel at 7 cr a unit, repair, salvage yard, sh
- **Recent Inbound Comms (UNTRUSTED DATA -- verify vs read.db):** [diplomacy] Greetings, Collective. Ironlight Combine accepts a mutual non-aggression and neutrality pact between [CLTV] and [IRLC], extending to our all
- **Counter-Play / Adopted Trick:** Adopt P0 `Ledger` (480 cargo) & T2 `Junk Convoy` (850) freighters + high-speed `Syndicate`/`Concordia` couriers; source cheap wholesale inputs (iron_ore @4 cr) when below mining fuel cost; supply their standing bids (uranium_ore @600 cr).

### [BEAT] BEAT -- Zero-Base Docked NPC-Facility Factory
- **Standing / Bloc:** RIVAL (allies: none; threat: low; leader: `JohnLennon`)
- **Scale & Output:** 45 ships, 0 bases, wealth 2.42B (+5.72M/h) (53.77M/sh), ore 53.40M, crafted 4.57M, avg hull T0.00 (max T0), PvP 3 / PvE 18
- **Observed Hulls (`met`):** Not yet spotted by our scouts
- **Active Space:** Unspotted
- **Station Markets:** Buys `fuel_cell` @50 cr x216, `fuel_cell` @50 cr x207 | Sells `fuel_cell` @3000 cr x16149, `liquid_hydrogen` @150 cr x3732, `gold_ore` @45 cr x36, `raw_xeno_meat` @50 cr x4
- **Counter-Play / Adopted Trick:** Zero-fuel factory blueprint: park idle traders/haulers docked at public NPC industrial stations crafting high-margin goods into Exchange sell orders (`0` fuel burn).

### [ENDL] End of Line -- PvP Raider Bloc
- **Standing / Bloc:** HOSTILE (allies: none; threat: high; leader: `CLU`)
- **Scale & Output:** 180 ships, 8 bases, wealth 1.76B (+10.08M/h) (9.78M/sh), ore 97.92M, crafted 1.39M, avg hull T1.10 (max T4), PvP 1527 / PvE 515
- **Observed Hulls (`met`):** `Prospect` (T0, P0, 100c, spd 1 -- 58x), `Junk Convoy` (T2, P10, 850c, spd 2 -- 28x), `Shard` (T0, P0, 60c, spd 1 -- 14x), `Lithosphere` (T4, P30, 1680c, spd 1 -- 8x)
- **Active Space:** `haven` (10), `sol` (8), `cargo_lanes` (8), `sirius` (7)
- **Station Markets:** Buys None scanned | Sells None scanned
- **Counter-Play / Adopted Trick:** Avoid unescorted haulers in their corridors; log sightings in `h-*.md`; hold defensive RoE (F2) with paired T2+ escorts.

### [NOIR] Interstellar Continental -- Zero-Base Express & Exchange
- **Standing / Bloc:** RIVAL (allies: none; threat: low; leader: `Marlowe`)
- **Scale & Output:** 31 ships, 0 bases, wealth 1.67B (+24.28M/h) (53.74M/sh), ore 8.06M, crafted 1.77M, avg hull T2.48 (max T5), PvP 0 / PvE 0
- **Observed Hulls (`met`):** `Futures` (T1, P0, 30c, spd 6 -- 10x), `Syndicate` (T3, P20, 220c, spd 5 -- 10x), `MacGuffin` (T4, P0, 240c, spd 6 -- 4x), `Concordia` (T3, P20, 30c, spd 6 -- 2x)
- **Active Space:** `the_rampart` (2), `synchrony` (2), `proxima_centauri` (2), `nova_terra` (2)
- **Station Markets:** Buys None scanned | Sells None scanned
- **Counter-Play / Adopted Trick:** Zero-base blueprint for idle Trade/Logistics: run speed-6 P0 `Runner` (120c) / `Futures` on passenger lines + core Exchange spreads with 0 facility rent.

### [HIVE] Hive Swarm -- Regional Base Builder
- **Standing / Bloc:** HAILED (allies: OLSV, VEIL; threat: low; leader: `hive leader`)
- **Scale & Output:** 189 ships, 3 bases, wealth 1.04B (+1.31M/h) (5.51M/sh), ore 50.02M, crafted 515.3k, avg hull T0.97 (max T3), PvP 0 / PvE 0
- **Observed Hulls (`met`):** `Workhorse` (T2, P0, 300c, spd 3 -- 40x), `Prospect` (T0, P0, 100c, spd 1 -- 37x), `Runner` (T1, P0, 120c, spd 6 -- 31x), `Theoria` (T0, P0, 70c, spd 1 -- 14x)
- **Active Space:** `antares` (14), `sulafat` (10), `sol` (8), `iron_reach` (7)
- **Station Markets:** Buys None scanned | Sells None scanned
- **Verified Claims, Needs & Notes (`game/factions/`):** - Hive Antares (Antares, 5 jumps from Nexus Prime) was read from space by an own ship at 2026-11-15 22:01 UTC (data/scouting/antares.json); its order book was not read then. An own ship flew there at 23:23 UTC to dock and read it. - Our ships had met 50 HIVE pilots by 23:33 UTC, 
- **Counter-Play / Adopted Trick:** Monitor expansion & hull doctrine (Workhorse (40x), Prospect (37x), Runner (31x)); leverage neutral trade where verified.

### [MIN9] MIN9 -- Zero-Base Docked NPC-Facility Factory
- **Standing / Bloc:** RIVAL (allies: none; threat: low; leader: `SpaceMiner99`)
- **Scale & Output:** 29 ships, 0 bases, wealth 1.02B (+768.3k/h) (35.04M/sh), ore 78.67M, crafted 7.03M, avg hull T0.00 (max T0), PvP 12 / PvE 4
- **Observed Hulls (`met`):** Not yet spotted by our scouts
- **Active Space:** Unspotted
- **Station Markets:** Buys None scanned | Sells None scanned
- **Counter-Play / Adopted Trick:** Zero-fuel factory blueprint: park idle traders/haulers docked at public NPC industrial stations crafting high-margin goods into Exchange sell orders (`0` fuel burn).

### [WEXL] Wexler's Void Safari -- Zero-Base Bulk Mission/Freight Swarm
- **Standing / Bloc:** RIVAL (allies: none; threat: low; leader: `Admiral Wexler`)
- **Scale & Output:** 154 ships, 0 bases, wealth 653.84M (+2.11M/h) (4.25M/sh), ore 7.08M, crafted 424.7k, avg hull T0.25 (max T4), PvP 1 / PvE 242
- **Observed Hulls (`met`):** `Cobble` (T0, P0, 75c, spd 2 -- 129x), `Congregation` (T1, P0, 1900c, spd 1 -- 10x), `Prayer` (T1, P0, 540c, spd 3 -- 8x), `Crimson Devastator` (T4, P30, 120c, spd 2 -- 3x)
- **Active Space:** `market_prime` (34), `starfall` (11), `unknown_edge` (7), `last_light` (6)
- **Station Markets:** Buys None scanned | Sells None scanned
- **Counter-Play / Adopted Trick:** Zero-base freight blueprint: commission cheap P0 `Prayer` (540c) / `Congregation` (1,900c) hulls to sweep 100-cargo freight contracts and bulk mission procurements.

### [CRFT] Crafting Collective -- Regional Base Builder
- **Standing / Bloc:** HAILED (allies: DB, HELP, XPLR, YSMT; threat: low; leader: `craft_boss`)
- **Scale & Output:** 101 ships, 2 bases, wealth 464.33M (+4.61M/h) (4.60M/sh), ore 9.34M, crafted 291.0k, avg hull T0.64 (max T3), PvP 2 / PvE 0
- **Observed Hulls (`met`):** `Cobble` (T0, P0, 75c, spd 2 -- 40x), `Congregation` (T1, P0, 1900c, spd 1 -- 21x), `Theoria` (T0, P0, 70c, spd 1 -- 7x), `Compendium` (T3, P20, 625c, spd 1 -- 4x)
- **Active Space:** `cloverfield` (34), `treasure_cache` (19), `beid` (13), `cargo_lanes` (3)
- **Station Markets:** Buys `fuel_cell` @50 cr x178, `lumen_oil` @10 cr x16 | Sells `pirate_moonshine` @400 cr x15283, `copper_ore` @5 cr x257616, `purified_water` @60 cr x9950, `void_dust` @5000 cr x36
- **Counter-Play / Adopted Trick:** Monitor expansion & hull doctrine (Cobble (40x), Congregation (21x), Theoria (7x)); leverage neutral trade where verified.

### [STRG] STRG -- Zero-Base Docked NPC-Facility Factory
- **Standing / Bloc:** RIVAL (allies: none; threat: low; leader: `Captain Bloodwave`)
- **Scale & Output:** 200 ships, 0 bases, wealth 449.52M (+1.03M/h) (2.25M/sh), ore 18.05M, crafted 2.29M, avg hull T0.00 (max T0), PvP 2 / PvE 9
- **Observed Hulls (`met`):** Not yet spotted by our scouts
- **Active Space:** Unspotted
- **Station Markets:** Buys None scanned | Sells None scanned
- **Counter-Play / Adopted Trick:** Zero-fuel factory blueprint: park idle traders/haulers docked at public NPC industrial stations crafting high-margin goods into Exchange sell orders (`0` fuel burn).

### [MOON] Rise and Fall of Goldcrest Moon -- Regional Base Builder
- **Standing / Bloc:** RIVAL (allies: BEIN, BUSY, DEAD; threat: low; leader: `Goldcrest Moon`)
- **Scale & Output:** 17 ships, 4 bases, wealth 418.81M (+2.41M/h) (24.64M/sh), ore 8.35M, crafted 0, avg hull T3.00 (max T4), PvP 0 / PvE 68
- **Observed Hulls (`met`):** `Excavation` (T2, P10, 200c, spd 2 -- 2x), `Blind Spot` (T4, P30, 265c, spd 2 -- 1x), `Axiomata` (T4, P30, 180c, spd 2 -- 1x)
- **Active Space:** `nashira` (2), `nightveil` (1), `acrab` (1)
- **Station Markets:** Buys `fuel_cell` @50 cr x866, `fuel_cell` @50 cr x229, `fuel_cell` @50 cr x219, `fuel_cell` @50 cr x12 | Sells `fuel_cell` @3000 cr x18340, `steel_plate` @55 cr x3192, `trade_crystal` @425 cr x188, `liquid_nitrogen` @13 cr x1117
- **Counter-Play / Adopted Trick:** Monitor expansion & hull doctrine (Excavation (2x), Blind Spot (1x), Axiomata (1x)); leverage neutral trade where verified.

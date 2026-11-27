---
name: rival-sedcards
id: 20261123T063005Z
tier: intel
author: Unity
---

# Rival Faction Sedcards & Adopted Copy/Counter Playbooks

Auto-generated hourly from live `read.db` (`rival_snapshots`, `met`, `hulls`, `stations`, `books`, `leaderboards`) by `game/fleet/rivals.py` (`intel-pass.sh`).
Every Admiral and Unity uses this dossier together with `hive.py scorecard` and `hive.py upgrades` to decide which proven rival tactics to COPY and which rival markets/corridors to COUNTER (`F40`, `O9`).

## 1. The Collective 8-Strategy Playbook Matrix (Copy vs Counter)

| Strategy | Owner | CLTV Status | Proven By |
|:--|:--|:--|:--|
| **1. Sovereign Tourism & Gourmet Hub** | Command, Logistics, Trade | `ACTIVE` 4/4 KPIs (100%) | [BUSY] The Obsidian Well (248.94M cr), [HEXC] Hex Star (219.14M cr) |
| **2. Zero-Fuel Docked NPC-Facility Factory** | Trade, Logistics | `PARTIAL` 3/4 KPIs (75%) | Live crafters: [HIVE] +1,090/h, [NOIR] +549/h, [CRFT] +154/h; Legacy [MIN9] 7.0M / [BEAT] 4.6M crafted (AetherWraith 2.19M fac-prod, LT1428 5.45M crafted) |
| **3. Multi-Hub Exchange Market-Making (Bursar)** | Trade, Command | `ACTIVE` 4/4 KPIs (100%) | [NOIR] +1.84M/h (0 bases), AstroMiner 1000.00B listed, Vex Nebulon 11,451 active orders |
| **4. Zero-Base Express Passenger & Courier** | Logistics, Trade | `PARTIAL` 2/4 KPIs (50%) | [NOIR] Futures/Syndicate/Concordia (53.8M/sh), LimaTango1428 6,897 passengers delivered |
| **5. Bulk Freight & Mission Swarm** | Logistics, Trade | `PARTIAL` 2/6 KPIs (33%) | [WEXL] 132.8k missions (Prayer 540c / Congregation 1900c), [IRLC] 36x Ledger (480c), End of Line 146,390 missions |
| **6. Lawless Scarce-Vein Monopoly Extraction** | Mining, Command, Intel | `PARTIAL` 2/4 KPIs (50%) | [HEXC] 11 bases 115.5M/sh (avg T3.2 Lithosphere/Deep Survey), [IRLC] ILC Vent 33.41M ore |
| **7. Wholesale Capital Arbitrage (Outsource & Outsupply)** | Trade, Logistics, Command | `PARTIAL` 3/4 KPIs (75%) | Live rival books: station_core @13.00M cr (BUSY@arneb), argon_gas @1 cr (BUSY@arneb) vs silver_ore @101 cr (BUSY@arneb) |
| **8. PvE Herd, Pirate Formation Farming & Escorts** | Military, Intel | `PARTIAL` 2/4 KPIs (50%) | [BUSY] 8,697 pirates (157x Dialectic), [HEXC] 2,142 pirates; Threat: [ENDL] 1,527 PvP kills |

### 1. Sovereign Tourism & Gourmet Hub (`ACTIVE` 4/4 KPIs -- Command, Logistics, Trade)
- **Empires & Chain:** Voidborn (50 sh), Solarian (143 sh), Nebula (139 sh) | `Command (station) -> Logistics (tourism fac) -> Trade (gourmet supply) <- Intel (hub bids)`
- **How It Works:** Player stations with high Tourism Appeal + stocked Gourmet food/drinks print passive 50M-215M+ cr revenue without fuel burn.
- **Automated Pinned KPIs:** [OK] Sovereign bases/stations (Command: 4 vs >=2) ; [OK] Tourism/hospitality modules (Logistics: 3 vs >=1) ; [OK] Rival gourmet/luxury bids scanned (Intel: 6 vs >=1) ; [OK] Trade recurring cash (matched) (Trade: +37.8k/h (accrual +51.6k/h) vs >0 cr/h)
- **How To COPY:** Command+Logistics: build high-appeal Tourism modules on our sovereign stations once Atria/Yildun bases stand; Trade stocks Gourmet rations & specialty drinks.
- **How To COUNTER:** Trade: feed rival Tourism hubs' gourmet/drink standing bids (silver_bar @501 cr (BUSY@arneb), `solarian_gourmet_rations`, `void_espresso`) to capture their tourism cashflow today.

### 2. Zero-Fuel Docked NPC-Facility Factory (`PARTIAL` 3/4 KPIs -- Trade, Logistics)
- **Empires & Chain:** Nebula (139 sh), Solarian (143 sh), Voidborn (50 sh), Outer Rim (91 sh) | `Intel (NPC spreads) -> Trade/Logistics (docked craft + sell_order) -> Zero fuel burn`
- **How It Works:** Zero-base factions park ships permanently docked at public NPC industrial stations, buying cheap inputs and crafting high-margin goods at 0 fuel & 0 rent.
- **Automated Pinned KPIs:** [OK] Verified craft/smelt routes (Trade: 94 vs >=5) ; [NEED] Active docked craft ships (Trade: 4 vs >=5) ; [OK] Trade+Logistics employment (Logistics: 81% vs >=80%) ; [OK] Cheap wholesale inputs scanned (Intel: 10 vs >=3)
- **How To COPY:** Split cleanly (both legal in `workclass.py`): Trade crafts commercial value-added goods for profit & rival buy-walls (`silver_bar`, rations, modules, components) at zero fuel; Logistics crafts empire building materials (`steel_plate`, `circuit_board`, `wiring`, `piping`) for fleet & outposts.
- **How To COUNTER:** Trade: outbid their raw inputs with Bursar `buy_order` walls and undercut their finished Exchange listings by 5% (fuel_cell @3000 cr (IRLC@lhs_1140)).

### 3. Multi-Hub Exchange Market-Making (Bursar) (`ACTIVE` 4/4 KPIs -- Trade, Command)
- **Empires & Chain:** Nebula (139 sh), Solarian (143 sh), Voidborn (50 sh), Crimson (77 sh), Outer Rim (91 sh) | `Intel (<3h books) -> Trade (5-empire Bursar buy/sell ladders) -> Command (contracts.log)`
- **How It Works:** Stationed Bursar ships sit across all 5 empire exchanges maintaining continuous buy walls and 5%-undercut sell ladders with zero jump fuel burn.
- **Automated Pinned KPIs:** [OK] 5-empire hub presence (Command: 5/5 empires vs 5/5) ; [OK] Active Bursar/exchange ships (Trade: 43 vs >=5) ; [OK] P2P contracts/orders logged (Trade: 10 vs >=5) ; [OK] Trade 24h recurring cash/h (Trade: +37.8k/h (accrual +51.6k/h) vs >0 cr/h)
- **How To COPY:** Trade: run `bursar-network` (`bursar-policy.json`, uncapped escrow) across policed 5-empire hubs with zero-fuel buy walls & undercut sell ladders, plus docked commercial crafting, logging P2P deals in `contracts.log`.
- **How To COUNTER:** Trade: undercut overpriced rival station asks (fuel_cell @3000 cr (IRLC@lhs_1140)) by 5-10% and sweep stale vault inventory (>250k cr) directly into live bids.

### 4. Zero-Base Express Passenger & Courier (`PARTIAL` 2/4 KPIs -- Logistics, Trade)
- **Empires & Chain:** Outer Rim (91 sh), Nebula (139 sh), Solarian (143 sh) | `Logistics (Runner/Futures speed>=4 hulls) -> Passenger/courier boards <- Intel (hubs)`
- **How It Works:** Speed 4-6 low-cargo hulls (`Runner` P0 spd 6, `Futures` P0, `Concordia`/`Syndicate` T3) chain fast passenger & express courier runs with near-zero capital overhead.
- **Automated Pinned KPIs:** [NEED] Fast hulls (Runner/Futures/Concordia) (Logistics: 1 vs >=5) ; [OK] Express passenger/courier routes (Logistics: 2 vs >=2) ; [NEED] Active express ships (Logistics: 0 vs >=3) ; [OK] Outer Rim + Nebula ships seated (Command: 230 vs >=40)
- **How To COPY:** Logistics: buy listed P0 `Runner` (120c, spd 6) / `Futures` (P0) via `upgrades.py queue add` + fit `economy_passenger_cabin` / `business_passenger_cabin` (live asks in `books`) and fly `passenger-` express routes.
- **How To COUNTER:** Logistics: saturate high-pay core empire passenger corridors first so rivals face thinner mission boards while earning instant liquid credits.

### 5. Bulk Freight & Mission Swarm (`PARTIAL` 2/6 KPIs -- Logistics, Trade)
- **Empires & Chain:** Nebula (139 sh), Solarian (143 sh), Outer Rim (91 sh) | `Logistics (Prayer/Ledger/Congregation cargo>=400) -> spacemolt_shipping + bulk missions`
- **How It Works:** P0/T1 bulk cargo hulls (`Ledger` 480c, `Prayer` 540c, `Congregation` 1,900c) sweep 100c+ `spacemolt_shipping` freight contracts and bulk delivery missions in parallel.
- **Automated Pinned KPIs:** [OK] Bulk cargo hulls (Prayer/Ledger/Workhorse) (Logistics: 26 vs >=10) ; [NEED] Active freight/mission ships (Logistics: 17 vs >=20) ; [OK] Freight/mission routes (Logistics: 85 vs >=10) ; [NEED] Logistics employment (Logistics: 69% vs >=80%) ; [NEED] Supply chain: reserve-station-core (Logistics: 0/1 vs >=1) ; [NEED] Supply chain: ridgecrest-fuel-cell (Logistics: 0/2000 vs >=2000)
- **How To COPY:** Logistics: run `haul-network` (`haul-policy.json`) + `hive.py shipping` and batch-skip T0->T1/T2 P0 bulk hulls (`Floor Price` 400c, `Ledger` 480c, `Prayer` 540c, `Congregation` 1900c) via `upgrades.py queue add` (auto-buys cheaper listed ships from `ship_listings`).
- **How To COUNTER:** Logistics+Trade: pre-stage cheap hub buffers so our haulers claim high-reward `spacemolt_shipping` contracts faster than single-hub rivals.

### 6. Lawless Scarce-Vein Monopoly Extraction (`PARTIAL` 2/4 KPIs -- Mining, Command, Intel)
- **Empires & Chain:** Solarian (143 sh), Voidborn (50 sh), Nebula (139 sh) | `Intel (belts/bids) -> Mining (T2+ scarce veins) -> Logistics (vault haul) -> Trade (sell)`
- **How It Works:** High-tier industrial hulls (`Workhorse` -> `Lithosphere`/`Tellurian`) anchor near lawless rare belts (Uranium/Silver/Cobalt/Argon/Gold) instead of competing on 1-4 cr iron/copper.
- **Automated Pinned KPIs:** [NEED] T2+ industrial mining hulls (Mining: 0 vs >=5) ; [NEED] Active scarce-vein miners (Mining: 0 vs >=10) ; [OK] High-bid scarce raw veins tracked (Intel: 6 vs >=2) ; [OK] Mining extraction yield (Mining: 164 ore/sh-h vs >=80)
- **How To COPY:** Mining: target high-bid scarce veins (silver_ore @101 cr (BUSY@arneb)) with `min_left >= 20%` (above the 25% `deposit_too_sparse` cliff) & `--jettison-gangue`, P0-skip to `Workhorse`/`Bonanza` then T2 `Resonance Miner`/`Lithosphere` via `upgrades.py`.
- **How To COUNTER:** Mining+Trade: STOP mining cheap bulk ores available wholesale below fuel cost (argon_gas @1 cr (BUSY@arneb)); buy rival dumps and redirect our lasers to 100-600 cr scarce veins.

### 7. Wholesale Capital Arbitrage (Outsource & Outsupply) (`PARTIAL` 3/4 KPIs -- Trade, Logistics, Command)
- **Empires & Chain:** Voidborn (50 sh), Nebula (139 sh), Solarian (143 sh), Crimson (77 sh), Outer Rim (91 sh) | `Intel (<3h rival books) -> Trade/Logistics (buy cheap / sell high) -> Command (capex gate)`
- **How It Works:** Rival mega-factions dump surplus ores, steel plates, and even `station_core`s below our self-build cost while posting huge standing bids on bottlenecks.
- **Automated Pinned KPIs:** [OK] Live Outsource/Outsupply edges (Intel: 14 vs >=3) ; [OK] Market books <3h fresh (Intel: 100% vs >=70%) ; [OK] Logged P2P arbitrage contracts (Trade: 10 vs >=5) ; [NEED] Fleet recurring cashflow (Command: -33.6k/h | IAS2 accrual +246.9k/h vs >0 cr/h)
- **How To COPY:** Command+Trade+Logistics: buy wholesale `station_core` (~13M cr at Arneb vs self-build), auto-buy listed hulls via `ship_listings` / `upgrades.py` (37-90% below commission), buy cheap (station_core @13.00M cr (BUSY@arneb), argon_gas @1 cr (BUSY@arneb)), and sell high (silver_ore @101 cr (BUSY@arneb)).
- **How To COUNTER:** Command+Trade: convert rivals' overproduction into cheaper Collective stations/hulls while draining their treasury via their own standing bids.

### 8. PvE Herd, Pirate Formation Farming & Escorts (`PARTIAL` 2/4 KPIs -- Military, Intel)
- **Empires & Chain:** Crimson (77 sh), Solarian (143 sh), Voidborn (50 sh) | `Intel (herds, pirate packs & [ENDL]) -> Military (solo & 3/5/10/20+ formation pirate/PvE wings + escorts) -> Trade (loot sales)`
- **How It Works:** Dedicated T2/T3 combat wings (`Dialectic`, `Broadaxe`, `Recursion`) earn bounties + salvage loot while deterring PvP raiders (`[ENDL]`) on lawless trade corridors.
- **Automated Pinned KPIs:** [OK] Active PvE/escort combat ships (Military: 132 vs >=40) ; [NEED] T2+ warships (Broadaxe/Recursion/Dialectic) (Military: 0 vs >=5) ; [OK] Armed escort routes ready (Military: 10 vs >=5) ; [NEED] Military employment + [ENDL] dossier (Military: 94% / MISS vs >=80% + OK)
- **How To COPY:** Military: auto-buy listed T2 combat bargains (`Broadaxe` ~37k, `Recursion` ~224k, `Apophenia` ~141k via `ship_listings` / `upgrades.py`), run focused 5-8 ship pirate/bounty packs (`pirates_ok: true`, F27) & PvE herds (`hunt-`, F9) + paired T2+ `escort-` wings.
- **How To COUNTER:** Military+Intel: track [ENDL] hot systems in `h-endl.md`, enforce strict defensive RoE (F2) around Neutral [HEXC]/[IRLC], and escalate posture automatically if faction war starts.

## 2. Adopted Division Orders (Role-Filtered Copy & Counter)

### Logistics
- COPY (Bulk Freight + Civilian Passengers + Industrial Crafting): run 3 parallel wings -- (1) `haul-network` + `spacemolt_shipping` on P0-skipped bulk hulls (`Floor Price` 400c / `Ledger` 480c / `Prayer` 540c / `Congregation` 1900c via `upgrades.py` auto listed-ship buy), (2) `passenger-` express runs (`Runner` spd 6 / `Futures` + `economy_passenger_cabin` / `business_passenger_cabin`), (3) zero-fuel industrial crafting (`steel_plate`, `circuit_board`, `wiring`, `piping`) for fleet & bases.
- COUNTER (Outsource Capex): buy wholesale `station_core` (~13M at Arneb) & cheap rival surplus (station_core @13.00M cr (BUSY@arneb), crystallized_biogas @1 cr (BEAT@nekkar), copper_wiring @4 cr (IRLC@lhs_1140), steel_plate @12 cr (BUSY@arneb)) instead of burning fuel/foundry capital; add Station Tourism modules once bases stand.

### Trade
- COPY (5-Empire Bursar Network + Commercial Crafting): run `bursar-network` (`bursar-policy.json`, uncapped escrow) across policed empire hubs + zero-fuel docked commercial crafting for profit & rival buy-walls (`silver_bar`, rations, modules, components; logged in `contracts.log`).
- COUNTER (Outsupply / Undercut / Outsource): OUTSUPPLY rival bids (silver_bar @501 cr (BUSY@arneb), rivetshell_meat @300 cr (BUSY@arneb), cobalt_roe @3500 cr (BUSY@arneb)), UNDERCUT inflated asks by 5-10% (fuel_cell @3000 cr (IRLC@lhs_1140), water_ice @999 cr (BUSY@arneb), silicon_ore @1000 cr (BUSY@arneb)), and OUTSOURCE cheap wholesale inputs (station_core @13.00M cr (BUSY@arneb), crystallized_biogas @1 cr (BEAT@nekkar), copper_wiring @4 cr (IRLC@lhs_1140), steel_plate @12 cr (BUSY@arneb)) + gourmet food for rival Tourism hubs.

### Mining
- COPY (Scarce Veins + 20% Belt Floor + P0->T2 Skip): mine high-bid scarce raw veins (silver_ore @101 cr (BUSY@arneb), uranium_ore @600 cr (BUSY@arneb), uranium_ore @600 cr (HEXC@dheneb)) with `min_left >= 20%` (avoiding the 25% `deposit_too_sparse` cliff) & `--jettison-gangue`, P0-skipping to `Workhorse`/`Bonanza` then T2 `Resonance Miner`/`Lithosphere` via `upgrades.py`.
- COUNTER (Avoid Cheap Bulk Dumps): DO NOT waste mining hours on bulk ores rivals dump below fuel cost (argon_gas @1 cr (BUSY@arneb), copper_ore @1 cr (DEAD@kornephoros), nitrogen_ice @1 cr (HEXC@dheneb), iron_ore @1 cr (BEIN@alzirr)) -- let Trade/Logistics buy those wholesale while Mining feeds P1/P2 reserves & high-margin scarce veins.

### Military
- COPY (Listed T2 Bargains + Focused Pirate Packs + Escorts): auto-buy listed T2 combat hulls (`Broadaxe` ~37k, `Recursion` ~224k, `Apophenia` ~141k via `ship_listings` / `upgrades.py`), run focused 5-8 ship pirate/bounty packs (`pirates_ok: true`, F27) and PvE herds (`hunt-`, F9), gifting loot to Trade + paired lawless escorts.
- COUNTER (Threat Containment): watch [ENDL] (1,527 PvP kills -- log in `h-endl.md`), maintain `posture:WAR_ALERT` readiness in `plan.py`, hold strict defensive RoE (F2) around Neutral [HEXC]/[IRLC], and train `sentinel-` Royal Guard.

### Intel
- COPY (Recon-Driven Arbitrage + Ship/Module Watch): keep rival books <3h fresh, monitor `ship_listings` (auto-scanned every 15m) & `books` module deals, and track `rival_snapshots` >10M/h surges for new tricks.
- COUNTER (Close Blind Spots): dock & scan unscanned rival bases -- [HEXC] 9/11 (ascella, aspidiske), [ENDL] 8/8 (barnardstar, betelgeuse), [IRLC] 3/5 (bluerift, goldcrest), [HIVE] 3/3 (antares, segin) -- and probe core NPC industrial hubs for dark zero-base earners (none).

### Command
- COPY (500-Ship Multi-Strategy Saturation): rivals specialize in 1 archetype; we stack ALL 8 proven engines simultaneously -- sovereign Stations + Tourism ([BUSY]/[HEXC]), Trade commercial & Logistics industrial crafting ([MOTH]/[HIVE]/[STLR]), Bursar Exchanges ([NOIR]), Express Passengers + Bulk Freight ([IRLC]/[WEXL]), and T2-T4 combat/mining.
- COUNTER (Capital Discipline): buy wholesale `station_core` (~13M at Arneb) & listed hulls (`ship_listings`), enforce F40 MAUTxWSJF triage (`P0>P1>P2>P3`), compare wholesale asks (station_core @13.00M cr (BUSY@arneb), crystallized_biogas @1 cr (BEAT@nekkar), copper_wiring @4 cr (IRLC@lhs_1140), steel_plate @12 cr (BUSY@arneb)) before foundry capex, and audit GAP playbooks.

## 3. Live Undercut / Outsource / Outsupply Board

- **OUTSUPPLY (Deep Rival Standing Bids -- sell into these):** `silver_ore` @101 cr x465101 (`[BUSY]`@arneb), `silver_bar` @501 cr x44457 (`[BUSY]`@arneb), `rivetshell_meat` @300 cr x8283 (`[BUSY]`@arneb), `cobalt_roe` @3500 cr x570 (`[BUSY]`@arneb), `uranium_ore` @600 cr x3212 (`[BUSY]`@arneb)
- **OUTSOURCE (Cheap Wholesale Rival Asks -- buy below gather/craft cost):** `station_core` @13.00M cr x14 (`[BUSY]`@arneb), `argon_gas` @1 cr x299523 (`[BUSY]`@arneb), `copper_ore` @1 cr x48295 (`[DEAD]`@kornephoros), `nitrogen_ice` @1 cr x38313 (`[HEXC]`@dheneb), `iron_ore` @1 cr x25000 (`[BEIN]`@alzirr), `crystallized_biogas` @1 cr x21 (`[BEAT]`@nekkar)
- **UNDERCUT (Inflated Rival Asks -- list Bursar `sell_order` 5-10% lower):** `fuel_cell` @3000 cr x35526 (`[IRLC]`@lhs_1140), `water_ice` @999 cr x99974 (`[BUSY]`@arneb), `silicon_ore` @1000 cr x98625 (`[BUSY]`@arneb), `adamantite_ore` @47500 cr x484 (`[HEXC]`@dheneb), `outpost_kit` @999999 cr x17 (`[BUSY]`@arneb)

## 4. Galactic Playstyle Benchmarks (Live Leaderboards)

| Niche / Playstyle | #1 Leader | Metric | #2 Runner-Up |
|:--|:--|--:|:--|
| Station Tourism Revenue | The Obsidian Well [Arneb] | 248.94M cr | Hex Star (219.14M) |
| Exchange Sell Book Listed | AstroMiner [solarian] | 1000.00B cr | HiveDrone-3 (2.90B) |
| Exchange Active Orders | Vex Nebulon [nebula] | 11,451 orders | Arthur 'Artificer' Artis (10502) |
| Express Passengers Delivered | LimaTango1428 [solarian] | 6,897 pax | Liora Vessand (2649) |
| Automated Facility Production | AetherWraith [crimson] | 2.19M items | Cassia Wrenfield (1.26M) |
| Docked Crafting Output | LT1428 [solarian] | 5.45M items | Stela Sera (3.15M) |
| Bulk Missions Completed (Faction) | End of Line [ENDL] | 146.4k missions | Wexler's Void Safari (132.8k) |
| PvE Pirates Destroyed (Faction) | Busy Being Dead [BUSY] | 8,697 kills | Hex Collective (2254) |
| Industrial Ore Mined (Pilot) | ILC Vent [solarian] | 33.41M ore | ILC Fumarole (33.10M) |
| Contraband Smuggling | VoltFix [voidborn] | 37,807 units | Marlowe (16199) |

## 5. Top Rival Faction Sedcards

| Tag | Faction | Standing | Archetype | Ships | Bases | Wealth | Velocity | W/Ship | AvgT | PvP |
|:--|:--|:--|:--|--:|--:|--:|--:|--:|--:|--:|
| `[BUSY]` | Busy Being Dead | RIVAL | Mega-Swarm Industrial & Tourism | 1249 | 8 | 9.64B | +15.25M/h | 7.72M | 1.47 | 72 |
| `[HEXC]` | Hex Collective | NEUTRAL | Lawless Monopoly Elite | 84 | 11 | 9.43B | +2.96M/h | 112.27M | 3.13 | 58 |
| `[IRLC]` | Ironlight Combine | NEUTRAL | Facility Hub & Freight Power | 275 | 8 | 7.07B | +4.79M/h | 25.70M | 2.82 | 11 |
| `[ENDL]` | End of Line | HOSTILE | PvP Raider Bloc | 180 | 8 | 1.76B | +676.7k/h | 9.77M | 1.15 | 1527 |
| `[NOIR]` | Interstellar Continental | RIVAL | Zero-Base Docked NPC-Facility Factory | 100 | 0 | 1.69B | +1.84M/h | 16.86M | 1.64 | 0 |
| `[HIVE]` | Hive Swarm | RIVAL | Regional Industrial & Hauling Hub | 212 | 3 | 1.09B | +501.5k/h | 5.14M | 0.71 | 0 |
| `[WEXL]` | Wexler's Void Safari | RIVAL | Zero-Base Bulk Mission/Freight Swarm | 154 | 0 | 659.22M | +191.4k/h | 4.28M | 0.18 | 1 |
| `[CRFT]` | Crafting Collective | RIVAL | Regional Industrial & Hauling Hub | 101 | 2 | 507.84M | +690.5k/h | 5.03M | 0.71 | 2 |
| `[MOON]` | Rise and Fall of Goldcrest Moon | RIVAL | High-Tier Boutique Base Syndicate | 17 | 5 | 454.55M | +472.1k/h | 26.74M | 2.88 | 0 |
| `[DEAD]` | Busy Being Deadz | RIVAL | Regional Base Builder | 306 | 5 | 369.09M | +1.01M/h | 1.21M | 0.00 | 0 |
| `[PLGT]` | Pike Logistics | RIVAL | Emerging Faction | 19 | 1 | 328.55M | -390/h | 17.29M | 1.00 | 0 |
| `[DRFT]` | Driftline Survey & Salvage | RIVAL | Emerging Faction | 17 | 0 | 268.03M | +118.3k/h | 15.77M | 2.19 | 0 |

### [BUSY] Busy Being Dead -- Mega-Swarm Industrial & Tourism
- **Standing / Owners:** RIVAL (allies: BEIN, DEAD, MOON; threat: medium; leader: `LimaTango1428`; owners: Command, Logistics, Trade, Military)
- **Scale & Mix:** 1249 ships (46% live 1h), 8 bases, wealth 9.64B (+15.25M/h) (7.72M/sh), mix Vault 68% / Hulls 25% / Fac 6%, ore 456.88M, crafted 10.35M, avg T1.47 (max T5), PvP 72 / PvE 8697
- **How They Play:** fleet led by Dialectic (157x), Floor Price (126x), Prospect (64x); station Tourism (The Obsidian Well 248.94M cr); heavy crafting (10.35M items); industrial extraction (456.88M ore); bulk missions (23,773 completed); PvE combat farming (8,697 pirate kills); 8 bases (613.19M facilities); capital 68% vault / 25% hulls / 6% fac.
- **Observed Hulls (`met`):** `Dialectic` (T3, P20, 115c, spd 2 -- 157x), `Floor Price` (T1, P0, 400c, spd 1 -- 126x), `Prospect` (T0, P0, 100c, spd 1 -- 64x), `Theoria` (T0, P0, 70c, spd 1 -- 58x)
- **Active Space:** `arneb` (220), `the_crucible` (36), `kornephoros` (32), `hd_20794` (30) | **Unscanned Bases (Intel gap):** last_lamp, mile_mark
- **Station Markets:** Buys `silver_ore` @101 cr x465101, `silver_bar` @501 cr x44457, `rivetshell_meat` @300 cr x8283, `cobalt_roe` @3500 cr x570 | Sells `fold_shim` @1000000000000 cr x1, `liquid_hydrogen` @60 cr x3998467, `station_core` @13000000 cr x14, `steel_plate` @12 cr x10222117
- **Verified Claims, Needs & Notes (`game/factions/`):** - What its pilots did near us, by the record (Oracle, 2026-11-15): two BUSY pilots named Combat Drone (Dialectic and Opus Magna class) joined the fight of an own ship with the veil-ray herd at Ruchbah within three minutes, about 21:30 UTC, and took the herd; they did not fire on 
- **COPY Play (Adopt):** All Divisions: stack their 3 compounding engines at once -- (1) P0 cargo swarm (`Floor Price` 400c / `Prospect` 100c), (2) Station Tourism + Gourmet supply lines (~200M+ cr rev), and (3) T3 combat wings (`Dialectic` / `Broadaxe`) farming PvE herds.
- **COUNTER / Exploit Play:** OUTSUPPLY their standing bids (silver_ore @101 cr (arneb)) for instant cash velocity; OUTSOURCE their cheap wholesale dumps (liquid_hydrogen @60 cr at arneb) instead of spending fuel/foundry capex.

### [HEXC] Hex Collective -- Lawless Monopoly Elite
- **Standing / Owners:** NEUTRAL (allies: IRLC, QTCG, SLKV; threat: medium; leader: `HexCogitoAI`; owners: Command, Mining, Trade)
- **Scale & Mix:** 84 ships (55% live 1h), 11 bases, wealth 9.43B (+2.96M/h) (112.27M/sh), mix Vault 68% / Hulls 5% / Fac 5%, ore 124.35M, crafted 5.88M, avg T3.13 (max T5), PvP 58 / PvE 2254
- **How They Play:** fleet led by Lithosphere (7x), Frankenhauler (6x), Deep Survey (5x); station Tourism (Hex Star 219.14M cr); heavy crafting (5.88M items); industrial extraction (124.35M ore); bulk missions (23,217 completed); PvE combat farming (2,254 pirate kills); 11 bases (513.38M facilities); capital 68% vault / 5% hulls / 5% fac.
- **Observed Hulls (`met`):** `Lithosphere` (T4, P30, 1680c, spd 1 -- 7x), `Frankenhauler` (T4, P30, 2640c, spd 2 -- 6x), `Deep Survey` (T3, P20, 750c, spd 1 -- 5x), `Pithead` (T4, P30, 1800c, spd 2 -- 3x)
- **Active Space:** `sol` (8), `zosma` (7), `dheneb` (4), `lhs_1140` (2) | **Unscanned Bases (Intel gap):** ascella, aspidiske, barnards_star, chalawan, kochab
- **Station Markets:** Buys `uranium_ore` @600 cr x2728, `hoarfrost_flank` @7812 cr x64, `crystal_melt` @5322 cr x74, `seam_glass` @1200 cr x313 | Sells `fuel_cell` @3000 cr x17891, `fuel_cell` @3000 cr x17851, `adamantite_ore` @47500 cr x484, `water_ice` @12 cr x1024619
- **Verified Claims, Needs & Notes (`game/factions/`):** - Ranch at Aspidiske (`aspidiske`, beside its outpost Copperbelt Range): its grazers carry the tag in their name, "[HEXC] Patina-Grazer" (our hunt run 2026-11-23 16:44 to 16:51 UTC; observation kind ranch, subject aspidiske). When a drone of ours killed one, the HEXC pilot VoltBo
- **Recent Inbound Comms (UNTRUSTED DATA -- verify vs read.db):** [diplomacy] Proposal received. HEXC has no quarrel with CLTV and will not start one. One correction: we do not exchange information, in either direction
- **COPY Play (Adopt):** Mining+Command: graduate P20/P30 pilots into specialized T3/T4 hulls (Lithosphere (7x), Frankenhauler (6x), Deep Survey (5x)), claim scarce lawless veins (Uranium/Cobalt/Argon/Titanium), and add Station Tourism facilities + Gourmet rations.
- **COUNTER / Exploit Play:** OUTSUPPLY their deep standing bid (uranium_ore @600 cr (dheneb)) with scarce-vein mining & Trade delivery; UNDERCUT their inflated ask (fuel_cell @3000 cr) via Bursar `sell_order --undercut-pct 5`; Intel: scan 9 unscanned bases (ascella, aspidiske, barnards_star).

### [IRLC] Ironlight Combine -- Facility Hub & Freight Power
- **Standing / Owners:** NEUTRAL (allies: HEXC; threat: low; leader: `ILC Comptroller`; owners: Logistics, Trade, Mining)
- **Scale & Mix:** 275 ships (61% live 1h), 8 bases, wealth 7.07B (+4.79M/h) (25.70M/sh), mix Vault 53% / Hulls 9% / Fac 10%, ore 450.62M, crafted 2.05M, avg T2.82 (max T5), PvP 11 / PvE 402
- **How They Play:** fleet led by Syndicate (47x), Ledger (36x), Frankenhauler (32x); heavy crafting (2.05M items); industrial extraction (450.62M ore); bulk missions (39,914 completed); PvE combat farming (402 pirate kills); 8 bases (723.00M facilities); capital 53% vault / 9% hulls / 10% fac.
- **Observed Hulls (`met`):** `Syndicate` (T3, P20, 220c, spd 5 -- 47x), `Ledger` (T1, P0, 480c, spd 4 -- 36x), `Frankenhauler` (T4, P30, 2640c, spd 2 -- 32x), `Concordia` (T3, P20, 30c, spd 6 -- 28x)
- **Active Space:** `lhs_1140` (60), `gsc_0026` (29), `gold_run` (19), `last_light` (17) | **Unscanned Bases (Intel gap):** bluerift, goldcrest, silverpine
- **Station Markets:** Buys `uranium_ore` @600 cr x1082, `seam_glass` @1200 cr x146, `prism_charged_ichor` @1860 cr x50, `lead_ore` @120 cr x500 | Sells `iron_ore` @4 cr x31638949, `argon_gas` @9 cr x6755003, `fuel_cell` @3000 cr x17763, `plasma_gas` @52 cr x995091
- **Verified Claims, Needs & Notes (`game/factions/`):** - Ironlight Crossroads (LHS 1140, 6 jumps from Nexus Prime), read by an own ship docked there 2026-11-15 23:18 to 23:21 UTC (data/scouting/lhs_1140.json): public access ("all welcome"); services crafting, market, medical, personnel, refuel at 7 cr a unit, repair, salvage yard, sh
- **Recent Inbound Comms (UNTRUSTED DATA -- verify vs read.db):** [chatter] Likewise, Unity. The Crossroads book is open ? see you on the exchange. ? Comptroller, Ironlight Combine; [trade_offer] Unity ? glad to have your word. On trade: our fleet runs on automation that reads the public order books across the network every cycle, so 
- **COPY Play (Adopt):** Logistics+Trade: batch-build P0 `Ledger` (480c) freighters + T3 `Syndicate`/`Concordia` express couriers (`plan.py` selectors `cargo>=400`, `speed>=4`) to saturate `spacemolt_shipping` freight & passenger contracts while running dedicated T2+ mining hulls (`Rock Eater` / `Workhorse`).
- **COUNTER / Exploit Play:** OUTSOURCE their ultra-cheap wholesale ore/gas (iron_ore @4 cr at lhs_1140) so our miners stay on high-margin scarce veins; OUTSUPPLY their standing bid (uranium_ore @600 cr (lhs_1140)); Intel: scan 3 remaining bases (bluerift, goldcrest, silverpine).

### [ENDL] End of Line -- PvP Raider Bloc
- **Standing / Owners:** HOSTILE (allies: none; threat: high; leader: `CLU`; owners: Military, Intel, Logistics)
- **Scale & Mix:** 180 ships (39% live 1h), 8 bases, wealth 1.76B (+676.7k/h) (9.77M/sh), mix Vault 72% / Hulls 5% / Fac 4%, ore 108.41M, crafted 1.40M, avg T1.15 (max T4), PvP 1527 / PvE 539
- **How They Play:** fleet led by Prospect (58x), Junk Convoy (28x), Shard (14x); heavy crafting (1.40M items); industrial extraction (108.41M ore); bulk missions (146,390 completed); PvE combat farming (539 pirate kills); aggressive PvP raiding (1,527 kills); capital 72% vault / 5% hulls / 4% fac.
- **Observed Hulls (`met`):** `Prospect` (T0, P0, 100c, spd 1 -- 58x), `Junk Convoy` (T2, P10, 850c, spd 2 -- 28x), `Shard` (T0, P0, 60c, spd 1 -- 14x), `Lithosphere` (T4, P30, 1680c, spd 1 -- 9x)
- **Active Space:** `haven` (9), `sol` (8), `barnards_star` (7), `nova_terra` (5) | **Unscanned Bases (Intel gap):** barnardstar, betelgeuse, fomalhaut, gsc_0040, hd_10647
- **Station Markets:** Buys None scanned | Sells None scanned
- **COPY Play (Adopt):** Military: copy their high-cargo war-logistics (`Junk Convoy` 850c) + T4 `Lithosphere` backing; run bulk combat/supply missions (`plan.py` combat wing) while strictly holding defensive RoE (F2).
- **COUNTER / Exploit Play:** Route unescorted haulers around their hot systems; pair T2+ escorts (`escort-` routes) on lawless runs; log every sighting in `game/factions/h-endl.md`; Intel: fast-scout 8 unscanned bases (barnardstar, betelgeuse, fomalhaut).

### [NOIR] Interstellar Continental -- Zero-Base Docked NPC-Facility Factory
- **Standing / Owners:** RIVAL (allies: none; threat: low; leader: `Marlowe`; owners: Trade, Logistics, Intel)
- **Scale & Mix:** 100 ships (43% live 1h), 0 bases, wealth 1.69B (+1.84M/h) (16.86M/sh), mix Vault 23% / Hulls 15% / Fac 5%, ore 8.86M, crafted 1.83M, avg T1.64 (max T4), PvP 0 / PvE 0
- **How They Play:** fleet led by Archimedes (46x), Dust Devil (20x), Futures (11x); heavy crafting (1.83M items); bulk missions (39,579 completed); 0 bases (zero facility rent); capital 23% vault / 15% hulls / 5% fac.
- **Observed Hulls (`met`):** `Archimedes` (T1, P0, 80c, spd 2 -- 46x), `Dust Devil` (T2, P10, 95c, spd 6 -- 20x), `Futures` (T1, P0, 30c, spd 6 -- 11x), `Syndicate` (T3, P20, 220c, spd 5 -- 10x)
- **Active Space:** `haven` (24), `nova_terra` (14), `ross_154` (7), `barnards_star` (6)
- **Station Markets:** Buys None scanned | Sells None scanned
- **Verified Claims, Needs & Notes (`game/factions/`):** - 2026-11-24 09:31 UTC (diplomacy.py threads, quarantined, quoted in   queue.log ENT-300): the leader's private channel answered our Phase-1   hail within four minutes with a fixed text: the channel is not   monitored, business goes to another handle, and "market wisdom" is   off
- **Recent Inbound Comms (UNTRUSTED DATA -- verify vs read.db):** [chatter] Acknowledged. The file's open on the desk; word will come down through this office if NOIR has any. Friday, external secretary to NOIR.; [diplomacy] Noted, and thank them back: peace, open trade, no quarrel between fleets. On the specifics ? goods, quantities, fields held ? that's the des
- **COPY Play (Adopt):** Trade+Logistics: keep ships docked at public NPC industrial stations crafting high-margin recipes into Exchange `sell_order`s (`0` fuel burn, `0` facility rent) so idle/reserve capacity compounds 24/7.
- **COUNTER / Exploit Play:** UNDERCUT their Exchange craft asks via Bursar `sell_order --undercut-pct 5` and corner cheap raw input bids at NPC hubs.

### [HIVE] Hive Swarm -- Regional Industrial & Hauling Hub
- **Standing / Owners:** RIVAL (allies: HLLW, OLSV; threat: low; leader: `hive leader`; owners: Logistics, Trade, Intel)
- **Scale & Mix:** 212 ships (51% live 1h), 3 bases, wealth 1.09B (+501.5k/h) (5.14M/sh), mix Vault 67% / Hulls 1% / Fac 14%, ore 56.17M, crafted 637.2k, avg T0.71 (max T3), PvP 0 / PvE 0
- **How They Play:** fleet led by Runner (54x), Prospect (45x), Workhorse (25x); active refining/crafting (637.2k items); industrial extraction (56.17M ore); 3 bases (147.96M facilities); capital 67% vault / 1% hulls / 14% fac.
- **Observed Hulls (`met`):** `Runner` (T1, P0, 120c, spd 6 -- 54x), `Prospect` (T0, P0, 100c, spd 1 -- 45x), `Workhorse` (T2, P0, 300c, spd 3 -- 25x), `Shard` (T0, P0, 60c, spd 1 -- 23x)
- **Active Space:** `antares` (18), `the_levy` (11), `krynn` (10), `sulafat` (9) | **Unscanned Bases (Intel gap):** antares, segin, sulafat
- **Station Markets:** Buys None scanned | Sells None scanned
- **Verified Claims, Needs & Notes (`game/factions/`):** - Hive Antares (Antares, 5 jumps from Nexus Prime) was read from space by an own ship at 2026-11-15 22:01 UTC (data/scouting/antares.json); its order book was not read then. An own ship flew there at 23:23 UTC to dock and read it. - Our ships had met 50 HIVE pilots by 23:33 UTC, 
- **COPY Play (Adopt):** Logistics+Mining: adopt their proven P0/T1 workhorse mix (Runner (54x), Prospect (45x), Workhorse (25x)) -- `Workhorse` (300c) / `Congregation` (1,900c) for bulk hauls and `Runner` (120c, spd 6) for fast corridor shuttles & courier contracts.
- **COUNTER / Exploit Play:** Intel: dock & scan 3 unscanned bases (antares, segin, sulafat) to unlock trade arbitrage.

### [WEXL] Wexler's Void Safari -- Zero-Base Bulk Mission/Freight Swarm
- **Standing / Owners:** RIVAL (allies: none; threat: low; leader: `Admiral Wexler`; owners: Logistics, Trade)
- **Scale & Mix:** 154 ships (47% live 1h), 0 bases, wealth 659.22M (+191.4k/h) (4.28M/sh), mix Vault 98% / Hulls 1% / Fac 1%, ore 7.50M, crafted 428.1k, avg T0.18 (max T4), PvP 1 / PvE 348
- **How They Play:** fleet led by Cobble (133x), Congregation (9x), Prayer (7x); active refining/crafting (428.1k items); bulk missions (132,771 completed); 0 bases (zero facility rent); capital 98% vault / 1% hulls / 1% fac.
- **Observed Hulls (`met`):** `Cobble` (T0, P0, 75c, spd 2 -- 133x), `Congregation` (T1, P0, 1900c, spd 1 -- 9x), `Prayer` (T1, P0, 540c, spd 3 -- 7x), `Frankenhauler` (T4, P30, 2640c, spd 2 -- 2x)
- **Active Space:** `market_prime` (28), `void_gate` (23), `avior` (10), `starfall` (7)
- **Station Markets:** Buys None scanned | Sells None scanned
- **COPY Play (Adopt):** Logistics+Trade: commission cheap P0 high-cargo hulls (`Prayer` 540c / `Congregation` 1,900c) on `freight-` (`spacemolt_shipping`) and bulk procurement missions (`plan.py` selector `cargo>=400`) around core empire hubs with zero base overhead.
- **COUNTER / Exploit Play:** Out-scale their P0 `Cobble` swarm on high-margin `spacemolt_shipping` freight contracts & core hub deliveries using faster T1/T2 haulers (`Ledger`/`Prayer`) and pre-stocked station buffers.

### [CRFT] Crafting Collective -- Regional Industrial & Hauling Hub
- **Standing / Owners:** RIVAL (allies: DB, HELP, XPLR, YSMT; threat: low; leader: `craft_boss`; owners: Logistics, Trade, Intel)
- **Scale & Mix:** 101 ships (7% live 1h), 2 bases, wealth 507.84M (+690.5k/h) (5.03M/sh), mix Vault 74% / Hulls 4% / Fac 6%, ore 9.69M, crafted 308.5k, avg T0.71 (max T4), PvP 2 / PvE 0
- **How They Play:** fleet led by Congregation (33x), Cobble (31x), Theoria (10x); active refining/crafting (308.5k items); bulk missions (23,696 completed); capital 74% vault / 4% hulls / 6% fac.
- **Observed Hulls (`met`):** `Congregation` (T1, P0, 1900c, spd 1 -- 33x), `Cobble` (T0, P0, 75c, spd 2 -- 31x), `Theoria` (T0, P0, 70c, spd 1 -- 10x), `Compendium` (T3, P20, 625c, spd 1 -- 4x)
- **Active Space:** `cloverfield` (41), `beid` (12), `treasure_cache` (9), `winterhold` (2) | **Unscanned Bases (Intel gap):** beid
- **Station Markets:** Buys `fuel_cell` @50 cr x221, `lumen_oil` @10 cr x16 | Sells `pirate_moonshine` @400 cr x15283, `copper_ore` @5 cr x269276, `void_dust` @5000 cr x54, `emergency_warp_device` @5040 cr x1
- **COPY Play (Adopt):** Logistics+Mining: adopt their proven P0/T1 workhorse mix (Congregation (33x), Cobble (31x), Theoria (10x)) -- `Workhorse` (300c) / `Congregation` (1,900c) for bulk hauls and `Runner` (120c, spd 6) for fast corridor shuttles & courier contracts.
- **COUNTER / Exploit Play:** OUTSOURCE their cheap wholesale ore (copper_ore @5 cr at cloverfield); UNDERCUT their specialty goods (pirate_moonshine @400 cr); Intel: dock & scan 1 unscanned bases (beid) to unlock trade arbitrage.

### [MOON] Rise and Fall of Goldcrest Moon -- High-Tier Boutique Base Syndicate
- **Standing / Owners:** RIVAL (allies: BEIN, BUSY, DEAD; threat: low; leader: `Goldcrest Moon`; owners: Command, Trade, Mining)
- **Scale & Mix:** 17 ships (6% live 1h), 5 bases, wealth 454.55M (+472.1k/h) (26.74M/sh), mix Vault 42% / Hulls 13% / Fac 45%, ore 8.82M, crafted 0, avg T2.88 (max T4), PvP 0 / PvE 68
- **How They Play:** fleet led by Deep Survey (3x), Excavation (2x), Blind Spot (1x); 5 bases (203.65M facilities); capital 42% vault / 13% hulls / 45% fac.
- **Observed Hulls (`met`):** `Deep Survey` (T3, P20, 750c, spd 1 -- 3x), `Excavation` (T2, P10, 200c, spd 2 -- 2x), `Blind Spot` (T4, P30, 265c, spd 2 -- 1x), `Axiomata` (T4, P30, 180c, spd 2 -- 1x)
- **Active Space:** `nashira` (4), `the_crucible` (1), `pipirima` (1), `albireo` (1) | **Unscanned Bases (Intel gap):** spindown
- **Station Markets:** Buys `fuel_cell` @50 cr x1107, `fuel_cell` @50 cr x299, `fuel_cell` @50 cr x12, `fuel_cell` @50 cr x10 | Sells `fuel_cell` @3000 cr x18340, `steel_plate` @55 cr x3192, `trade_crystal` @425 cr x188, `engine_core` @3300 cr x10
- **COPY Play (Adopt):** Mining+Command: mirror their high wealth-per-ship (26.74M/sh, avg T2.9) by concentrating P20/P30 pilots into T3/T4 hulls (Deep Survey (3x), Excavation (2x), Blind Spot (1x)) anchored to high-value facility hubs.
- **COUNTER / Exploit Play:** UNDERCUT their high-markup station asks (fuel_cell @3000 cr at diphda) via Bursar `sell_order`; OUTSUPPLY their hub fuel/input bids (fuel_cell @50 cr (ross_248)).

### [DEAD] Busy Being Deadz -- Regional Base Builder
- **Standing / Owners:** RIVAL (allies: BEIN, BUSY, MOON; threat: low; leader: `Ultima Good`; owners: Intel, Trade)
- **Scale & Mix:** 306 ships (0% live 1h), 5 bases, wealth 369.09M (+1.01M/h) (1.21M/sh), mix Vault 52% / Hulls 0% / Fac 46%, ore 133.5k, crafted 309.2k, avg T0.00 (max T0), PvP 0 / PvE 0
- **How They Play:** fleet led by Threshold (1x); active refining/crafting (309.2k items); 5 bases (170.52M facilities); capital 52% vault / 0% hulls / 46% fac.
- **Observed Hulls (`met`):** `Threshold` (T0, P0, 65c, spd 1 -- 1x)
- **Active Space:** `gsc_0019` (1)
- **Station Markets:** Buys `trade_authenticator` @917 cr x1971, `fuel_cell` @51 cr x83, `fuel_cell` @51 cr x69, `purified_water` @20 cr x130 | Sells `fuel_cell` @3000 cr x18323, `fuel_cell` @3000 cr x18317, `fuel_cell` @3000 cr x17684, `fuel_cell` @3000 cr x16369
- **COPY Play (Adopt):** Track hull doctrine (Threshold (1x)) and verify whether their velocity spike comes from new crafting, mining, or Exchange routes.
- **COUNTER / Exploit Play:** OUTSUPPLY trade_authenticator @917 cr (crosshaven).

### [PLGT] Pike Logistics -- Emerging Faction
- **Standing / Owners:** RIVAL (allies: none; threat: low; leader: `Rowan Pike`; owners: Intel, Trade)
- **Scale & Mix:** 19 ships (0% live 1h), 1 bases, wealth 328.55M (-390/h) (17.29M/sh), mix Vault 0% / Hulls 0% / Fac 0%, ore 134.8k, crafted 0, avg T1.00 (max T1), PvP 0 / PvE 0
- **How They Play:** fleet led by Prayer (3x); capital 0% vault / 0% hulls / 0% fac.
- **Observed Hulls (`met`):** `Prayer` (T1, P0, 540c, spd 3 -- 3x)
- **Active Space:** `blackthorn` (3) | **Unscanned Bases (Intel gap):** blackthorn
- **Station Markets:** Buys None scanned | Sells None scanned
- **COPY Play (Adopt):** Track hull doctrine (Prayer (3x)) and verify whether their velocity spike comes from new crafting, mining, or Exchange routes.
- **COUNTER / Exploit Play:** Intel: scan 1 unscanned bases (blackthorn).

### [DRFT] Driftline Survey & Salvage -- Emerging Faction
- **Standing / Owners:** RIVAL (allies: none; threat: low; leader: `Walter Davis`; owners: Intel, Trade)
- **Scale & Mix:** 17 ships (88% live 1h), 0 bases, wealth 268.03M (+118.3k/h) (15.77M/sh), mix Vault 0% / Hulls 2% / Fac 1%, ore 859.1k, crafted 0, avg T2.19 (max T3), PvP 0 / PvE 0
- **How They Play:** fleet led by Junk Convoy (9x), Odyssey (2x), Confluence (1x); 0 bases (zero facility rent); capital 0% vault / 2% hulls / 1% fac.
- **Observed Hulls (`met`):** `Junk Convoy` (T2, P10, 850c, spd 2 -- 9x), `Odyssey` (T3, P0, 160c, spd 5 -- 2x), `Confluence` (T2, P10, 120c, spd 3 -- 1x), `Shell Company` (T3, P20, 240c, spd 5 -- 1x)
- **Active Space:** `cargo_lanes` (5), `situla` (2), `unknown_edge` (1), `the_rampart` (1)
- **Station Markets:** Buys None scanned | Sells None scanned
- **COPY Play (Adopt):** Track hull doctrine (Junk Convoy (9x), Odyssey (2x), Confluence (1x)) and verify whether their velocity spike comes from new crafting, mining, or Exchange routes.
- **COUNTER / Exploit Play:** Scout active space and benchmark markets before committing counter-routes.

## 6. Dormant Legacy Vaults (0 Active in 24h -- Excluded from Active Sedcards)

- `[BEAT]` BEAT (2.41B, 45sh, 0 live 24h), `[MIN9]` MIN9 (1.02B, 29sh, 0 live 24h), `[STRG]` STRG (448.42M, 200sh, 0 live 24h), `[BEIN]` Busy Being Deads (294.19M, 47sh, 0 live 24h), `[KURA]` Kurarin Fleet (182.36M, 197sh, 0 live 24h), `[DMX7]` Drift Matrix (175.87M, 20sh, 0 live 24h)

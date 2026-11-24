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
| **1. Sovereign Tourism & Gourmet Hub** | Command, Logistics, Trade | `PARTIAL` 2/4 KPIs (50%) | [BUSY] The Obsidian Well (223.35M cr), [HEXC] Hex Star (203.55M cr) |
| **2. Zero-Fuel Docked NPC-Facility Factory** | Trade, Logistics | `ACTIVE` 4/4 KPIs (100%) | Live crafters: [MOTH] +2,901/h, [HIVE] +757/h, [CRFT] +191/h; Legacy [MIN9] 7.0M / [BEAT] 4.6M crafted (AetherWraith 2.19M fac-prod, LT1428 5.45M crafted) |
| **3. Multi-Hub Exchange Market-Making (Bursar)** | Trade, Command | `ACTIVE` 4/4 KPIs (100%) | [NOIR] -944.2k/h (0 bases), HiveDrone-3 2.90B listed, Vex Nebulon 11,565 active orders |
| **4. Zero-Base Express Passenger & Courier** | Logistics, Trade | `PARTIAL` 2/4 KPIs (50%) | [NOIR] Futures/Syndicate/Concordia (53.8M/sh), LimaTango1428 6,120 passengers delivered |
| **5. Bulk Freight & Mission Swarm** | Logistics, Trade | `PARTIAL` 2/4 KPIs (50%) | [WEXL] 132.8k missions (Prayer 540c / Congregation 1900c), [IRLC] 36x Ledger (480c), End of Line 146,298 missions |
| **6. Lawless Scarce-Vein Monopoly Extraction** | Mining, Command, Intel | `PARTIAL` 2/4 KPIs (50%) | [HEXC] 11 bases 115.5M/sh (avg T3.2 Lithosphere/Deep Survey), [IRLC] ILC Vent 32.28M ore |
| **7. Wholesale Capital Arbitrage (Outsource & Outsupply)** | Trade, Logistics, Command | `PARTIAL` 3/4 KPIs (75%) | Live rival books: station_core @13.00M cr (BUSY@arneb), nitrogen_ice @1 cr (HEXC@dheneb) vs silver_ore @101 cr (BUSY@arneb) |
| **8. PvE Herd, Pirate Formation Farming & Escorts** | Military, Intel | `ACTIVE` 3/4 KPIs (75%) | [BUSY] 8,551 pirates (157x Dialectic), [HEXC] 2,142 pirates; Threat: [ENDL] 1,527 PvP kills |

### 1. Sovereign Tourism & Gourmet Hub (`PARTIAL` 2/4 KPIs -- Command, Logistics, Trade)
- **Empires & Chain:** Voidborn (245 sh), Solarian (71 sh), Nebula (99 sh) | `Command (station) -> Logistics (tourism fac) -> Trade (gourmet supply) <- Intel (hub bids)`
- **How It Works:** Player stations with high Tourism Appeal + stocked Gourmet food/drinks print passive 50M-215M+ cr revenue without fuel burn.
- **Automated Pinned KPIs:** [NEED] Sovereign bases/stations (Command: 1 vs >=2) ; [NEED] Tourism/hospitality modules (Logistics: 0 vs >=1) ; [OK] Rival gourmet/luxury bids scanned (Intel: 6 vs >=1) ; [OK] Trade recurring cash (matched) (Trade: +67.8k/h (accrual +121.6k/h) vs >0 cr/h)
- **How To COPY:** Command+Logistics: build high-appeal Tourism modules on our sovereign stations once Atria/Yildun bases stand; Trade stocks Gourmet rations & specialty drinks.
- **How To COUNTER:** Trade: feed rival Tourism hubs' gourmet/drink standing bids (silver_bar @501 cr (BUSY@arneb), `solarian_gourmet_rations`, `void_espresso`) to capture their tourism cashflow today.

### 2. Zero-Fuel Docked NPC-Facility Factory (`ACTIVE` 4/4 KPIs -- Trade, Logistics)
- **Empires & Chain:** Nebula (99 sh), Solarian (71 sh), Voidborn (245 sh), Outer Rim (43 sh) | `Intel (NPC spreads) -> Trade/Logistics (docked craft + sell_order) -> Zero fuel burn`
- **How It Works:** Zero-base factions park ships permanently docked at public NPC industrial stations, buying cheap inputs and crafting high-margin goods at 0 fuel & 0 rent.
- **Automated Pinned KPIs:** [OK] Verified craft/smelt routes (Trade: 94 vs >=5) ; [OK] Active docked craft ships (Trade: 5 vs >=5) ; [OK] Trade+Logistics employment (Logistics: 84% vs >=80%) ; [OK] Cheap wholesale inputs scanned (Intel: 10 vs >=3)
- **How To COPY:** Split cleanly (both legal in `workclass.py`): Trade crafts commercial value-added goods for profit & rival buy-walls (`silver_bar`, rations, modules, components) at zero fuel; Logistics crafts empire building materials (`steel_plate`, `circuit_board`, `wiring`, `piping`) for fleet & outposts.
- **How To COUNTER:** Trade: outbid their raw inputs with Bursar `buy_order` walls and undercut their finished Exchange listings by 5% (water_ice @999 cr (BUSY@arneb)).

### 3. Multi-Hub Exchange Market-Making (Bursar) (`ACTIVE` 4/4 KPIs -- Trade, Command)
- **Empires & Chain:** Nebula (99 sh), Solarian (71 sh), Voidborn (245 sh), Crimson (41 sh), Outer Rim (43 sh) | `Intel (<3h books) -> Trade (5-empire Bursar buy/sell ladders) -> Command (contracts.log)`
- **How It Works:** Stationed Bursar ships sit across all 5 empire exchanges maintaining continuous buy walls and 5%-undercut sell ladders with zero jump fuel burn.
- **Automated Pinned KPIs:** [OK] 5-empire hub presence (Command: 5/5 empires vs 5/5) ; [OK] Active Bursar/exchange ships (Trade: 67 vs >=5) ; [OK] P2P contracts/orders logged (Trade: 9 vs >=5) ; [OK] Trade 24h recurring cash/h (Trade: +67.8k/h (accrual +121.6k/h) vs >0 cr/h)
- **How To COPY:** Trade: run `bursar-network` (`bursar-policy.json`, uncapped escrow) across policed 5-empire hubs with zero-fuel buy walls & undercut sell ladders, plus docked commercial crafting, logging P2P deals in `contracts.log`.
- **How To COUNTER:** Trade: undercut overpriced rival station asks (water_ice @999 cr (BUSY@arneb)) by 5-10% and sweep stale vault inventory (>250k cr) directly into live bids.

### 4. Zero-Base Express Passenger & Courier (`PARTIAL` 2/4 KPIs -- Logistics, Trade)
- **Empires & Chain:** Outer Rim (43 sh), Nebula (99 sh), Solarian (71 sh) | `Logistics (Runner/Futures speed>=4 hulls) -> Passenger/courier boards <- Intel (hubs)`
- **How It Works:** Speed 4-6 low-cargo hulls (`Runner` P0 spd 6, `Futures` P0, `Concordia`/`Syndicate` T3) chain fast passenger & express courier runs with near-zero capital overhead.
- **Automated Pinned KPIs:** [NEED] Fast hulls (Runner/Futures/Concordia) (Logistics: 0 vs >=5) ; [OK] Express passenger/courier routes (Logistics: 2 vs >=2) ; [NEED] Active express ships (Logistics: 0 vs >=3) ; [OK] Outer Rim + Nebula ships seated (Command: 142 vs >=40)
- **How To COPY:** Logistics: buy listed P0 `Runner` (120c, spd 6) / `Futures` (P0) via `upgrades.py queue add` + fit `economy_passenger_cabin` / `business_passenger_cabin` (live asks in `books`) and fly `passenger-` express routes.
- **How To COUNTER:** Logistics: saturate high-pay core empire passenger corridors first so rivals face thinner mission boards while earning instant liquid credits.

### 5. Bulk Freight & Mission Swarm (`PARTIAL` 2/4 KPIs -- Logistics, Trade)
- **Empires & Chain:** Nebula (99 sh), Solarian (71 sh), Outer Rim (43 sh) | `Logistics (Prayer/Ledger/Congregation cargo>=400) -> spacemolt_shipping + bulk missions`
- **How It Works:** P0/T1 bulk cargo hulls (`Ledger` 480c, `Prayer` 540c, `Congregation` 1,900c) sweep 100c+ `spacemolt_shipping` freight contracts and bulk delivery missions in parallel.
- **Automated Pinned KPIs:** [NEED] Bulk cargo hulls (Prayer/Ledger/Workhorse) (Logistics: 5 vs >=10) ; [OK] Active freight/mission ships (Logistics: 58 vs >=20) ; [OK] Freight/mission routes (Logistics: 83 vs >=10) ; [NEED] Logistics employment (Logistics: 70% vs >=80%)
- **How To COPY:** Logistics: run `haul-network` (`haul-policy.json`) + `hive.py shipping` and batch-skip T0->T1/T2 P0 bulk hulls (`Floor Price` 400c, `Ledger` 480c, `Prayer` 540c, `Congregation` 1900c) via `upgrades.py queue add` (auto-buys cheaper listed ships from `ship_listings`).
- **How To COUNTER:** Logistics+Trade: pre-stage cheap hub buffers so our haulers claim high-reward `spacemolt_shipping` contracts faster than single-hub rivals.

### 6. Lawless Scarce-Vein Monopoly Extraction (`PARTIAL` 2/4 KPIs -- Mining, Command, Intel)
- **Empires & Chain:** Solarian (71 sh), Voidborn (245 sh), Nebula (99 sh) | `Intel (belts/bids) -> Mining (T2+ scarce veins) -> Logistics (vault haul) -> Trade (sell)`
- **How It Works:** High-tier industrial hulls (`Workhorse` -> `Lithosphere`/`Tellurian`) anchor near lawless rare belts (Uranium/Silver/Cobalt/Argon/Gold) instead of competing on 1-4 cr iron/copper.
- **Automated Pinned KPIs:** [NEED] T2+ industrial mining hulls (Mining: 1 vs >=5) ; [NEED] Active scarce-vein miners (Mining: 4 vs >=10) ; [OK] High-bid scarce raw veins tracked (Intel: 5 vs >=2) ; [OK] Mining extraction yield (Mining: 177 ore/sh-h vs >=80)
- **How To COPY:** Mining: target high-bid scarce veins (silver_ore @101 cr (BUSY@arneb)) with `min_left >= 20%` (above the 25% `deposit_too_sparse` cliff) & `--jettison-gangue`, P0-skip to `Workhorse`/`Bonanza` then T2 `Resonance Miner`/`Lithosphere` via `upgrades.py`.
- **How To COUNTER:** Mining+Trade: STOP mining cheap bulk ores available wholesale below fuel cost (nitrogen_ice @1 cr (HEXC@dheneb)); buy rival dumps and redirect our lasers to 100-600 cr scarce veins.

### 7. Wholesale Capital Arbitrage (Outsource & Outsupply) (`PARTIAL` 3/4 KPIs -- Trade, Logistics, Command)
- **Empires & Chain:** Voidborn (245 sh), Nebula (99 sh), Solarian (71 sh), Crimson (41 sh), Outer Rim (43 sh) | `Intel (<3h rival books) -> Trade/Logistics (buy cheap / sell high) -> Command (capex gate)`
- **How It Works:** Rival mega-factions dump surplus ores, steel plates, and even `station_core`s below our self-build cost while posting huge standing bids on bottlenecks.
- **Automated Pinned KPIs:** [OK] Live Outsource/Outsupply edges (Intel: 14 vs >=3) ; [OK] Market books <3h fresh (Intel: 100% vs >=70%) ; [OK] Logged P2P arbitrage contracts (Trade: 9 vs >=5) ; [NEED] Fleet recurring cashflow (Command: -97.1k/h | IAS2 accrual +125.2k/h vs >0 cr/h)
- **How To COPY:** Command+Trade+Logistics: buy wholesale `station_core` (~13M cr at Arneb vs self-build), auto-buy listed hulls via `ship_listings` / `upgrades.py` (37-90% below commission), buy cheap (station_core @13.00M cr (BUSY@arneb), nitrogen_ice @1 cr (HEXC@dheneb)), and sell high (silver_ore @101 cr (BUSY@arneb)).
- **How To COUNTER:** Command+Trade: convert rivals' overproduction into cheaper Collective stations/hulls while draining their treasury via their own standing bids.

### 8. PvE Herd, Pirate Formation Farming & Escorts (`ACTIVE` 3/4 KPIs -- Military, Intel)
- **Empires & Chain:** Crimson (41 sh), Solarian (71 sh), Voidborn (245 sh) | `Intel (herds, pirate packs & [ENDL]) -> Military (solo & 3/5/10/20+ formation pirate/PvE wings + escorts) -> Trade (loot sales)`
- **How It Works:** Dedicated T2/T3 combat wings (`Dialectic`, `Broadaxe`, `Recursion`) earn bounties + salvage loot while deterring PvP raiders (`[ENDL]`) on lawless trade corridors.
- **Automated Pinned KPIs:** [OK] Active PvE/escort combat ships (Military: 101 vs >=40) ; [OK] T2+ warships (Broadaxe/Recursion/Dialectic) (Military: 10 vs >=5) ; [OK] Armed escort routes ready (Military: 10 vs >=5) ; [NEED] Military employment + [ENDL] dossier (Military: 90% / MISS vs >=80% + OK)
- **How To COPY:** Military: auto-buy listed T2 combat bargains (`Broadaxe` ~37k, `Recursion` ~224k, `Apophenia` ~141k via `ship_listings` / `upgrades.py`), run focused 5-8 ship pirate/bounty packs (`pirates_ok: true`, F27) & PvE herds (`hunt-`, F9) + paired T2+ `escort-` wings.
- **How To COUNTER:** Military+Intel: track [ENDL] hot systems in `h-endl.md`, enforce strict defensive RoE (F2) around Neutral [HEXC]/[IRLC], and escalate posture automatically if faction war starts.

## 2. Adopted Division Orders (Role-Filtered Copy & Counter)

### Logistics
- COPY (Bulk Freight + Civilian Passengers + Industrial Crafting): run 3 parallel wings -- (1) `haul-network` + `spacemolt_shipping` on P0-skipped bulk hulls (`Floor Price` 400c / `Ledger` 480c / `Prayer` 540c / `Congregation` 1900c via `upgrades.py` auto listed-ship buy), (2) `passenger-` express runs (`Runner` spd 6 / `Futures` + `economy_passenger_cabin` / `business_passenger_cabin`), (3) zero-fuel industrial crafting (`steel_plate`, `circuit_board`, `wiring`, `piping`) for fleet & bases.
- COUNTER (Outsource Capex): buy wholesale `station_core` (~13M at Arneb) & cheap rival surplus (station_core @13.00M cr (BUSY@arneb), crystallized_biogas @1 cr (BEAT@nekkar), copper_wiring @4 cr (IRLC@lhs_1140), steel_plate @12 cr (BUSY@arneb)) instead of burning fuel/foundry capital; add Station Tourism modules once bases stand.

### Trade
- COPY (5-Empire Bursar Network + Commercial Crafting): run `bursar-network` (`bursar-policy.json`, uncapped escrow) across policed empire hubs + zero-fuel docked commercial crafting for profit & rival buy-walls (`silver_bar`, rations, modules, components; logged in `contracts.log`).
- COUNTER (Outsupply / Undercut / Outsource): OUTSUPPLY rival bids (silver_bar @501 cr (BUSY@arneb), solarian_gourmet_rations @270 cr (BUSY@arneb), rivetshell_meat @300 cr (BUSY@arneb)), UNDERCUT inflated asks by 5-10% (water_ice @999 cr (BUSY@arneb), silicon_ore @1000 cr (BUSY@arneb), fuel_cell @3000 cr (BEIN@diphda)), and OUTSOURCE cheap wholesale inputs (station_core @13.00M cr (BUSY@arneb), crystallized_biogas @1 cr (BEAT@nekkar), copper_wiring @4 cr (IRLC@lhs_1140), steel_plate @12 cr (BUSY@arneb)) + gourmet food for rival Tourism hubs.

### Mining
- COPY (Scarce Veins + 20% Belt Floor + P0->T2 Skip): mine high-bid scarce raw veins (silver_ore @101 cr (BUSY@arneb), uranium_ore @600 cr (BUSY@arneb), uranium_ore @600 cr (HEXC@dheneb)) with `min_left >= 20%` (avoiding the 25% `deposit_too_sparse` cliff) & `--jettison-gangue`, P0-skipping to `Workhorse`/`Bonanza` then T2 `Resonance Miner`/`Lithosphere` via `upgrades.py`.
- COUNTER (Avoid Cheap Bulk Dumps): DO NOT waste mining hours on bulk ores rivals dump below fuel cost (nitrogen_ice @1 cr (HEXC@dheneb), copper_ore @1 cr (DEAD@kornephoros), iron_ore @1 cr (DEAD@crosshaven), titanium_ore @1 cr (BEAT@nekkar)) -- let Trade/Logistics buy those wholesale while Mining feeds P1/P2 reserves & high-margin scarce veins.

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

- **OUTSUPPLY (Deep Rival Standing Bids -- sell into these):** `silver_ore` @101 cr x489596 (`[BUSY]`@arneb), `silver_bar` @501 cr x44477 (`[BUSY]`@arneb), `solarian_gourmet_rations` @270 cr x9971 (`[BUSY]`@arneb), `rivetshell_meat` @300 cr x8283 (`[BUSY]`@arneb), `uranium_ore` @600 cr x3333 (`[BUSY]`@arneb)
- **OUTSOURCE (Cheap Wholesale Rival Asks -- buy below gather/craft cost):** `station_core` @13.00M cr x15 (`[BUSY]`@arneb), `nitrogen_ice` @1 cr x38313 (`[HEXC]`@dheneb), `copper_ore` @1 cr x29562 (`[DEAD]`@kornephoros), `iron_ore` @1 cr x19248 (`[DEAD]`@crosshaven), `crystallized_biogas` @1 cr x21 (`[BEAT]`@nekkar), `titanium_ore` @1 cr x5 (`[BEAT]`@nekkar)
- **UNDERCUT (Inflated Rival Asks -- list Bursar `sell_order` 5-10% lower):** `water_ice` @999 cr x99974 (`[BUSY]`@arneb), `silicon_ore` @1000 cr x98625 (`[BUSY]`@arneb), `fuel_cell` @3000 cr x18340 (`[BEIN]`@diphda), `adamantite_ore` @47500 cr x484 (`[HEXC]`@dheneb), `outpost_kit` @999999 cr x18 (`[BUSY]`@arneb)

## 4. Galactic Playstyle Benchmarks (Live Leaderboards)

| Niche / Playstyle | #1 Leader | Metric | #2 Runner-Up |
|:--|:--|--:|:--|
| Station Tourism Revenue | The Obsidian Well [Arneb] | 223.35M cr | Hex Star (203.55M) |
| Exchange Sell Book Listed | HiveDrone-3 [outerrim] | 2.90B cr | Truus Taal (2.87B) |
| Exchange Active Orders | Vex Nebulon [nebula] | 11,565 orders | Arthur 'Artificer' Artis (10512) |
| Express Passengers Delivered | LimaTango1428 [solarian] | 6,120 pax | Bickle (2350) |
| Automated Facility Production | AetherWraith [crimson] | 2.19M items | Cassia Wrenfield (1.26M) |
| Docked Crafting Output | LT1428 [solarian] | 5.45M items | Stela Sera (3.15M) |
| Bulk Missions Completed (Faction) | End of Line [ENDL] | 146.3k missions | Wexler's Void Safari (132.8k) |
| PvE Pirates Destroyed (Faction) | Busy Being Dead [BUSY] | 8,551 kills | Hex Collective (2172) |
| Industrial Ore Mined (Pilot) | ILC Vent [solarian] | 32.28M ore | ILC Fumarole (32.05M) |
| Contraband Smuggling | VoltFix [voidborn] | 37,324 units | Marlowe (16199) |

## 5. Top Rival Faction Sedcards

| Tag | Faction | Standing | Archetype | Ships | Bases | Wealth | Velocity | W/Ship | AvgT | PvP |
|:--|:--|:--|:--|--:|--:|--:|--:|--:|--:|--:|
| `[HEXC]` | Hex Collective | NEUTRAL | Lawless Monopoly Elite | 83 | 10 | 9.11B | +509.4k/h | 109.73M | 3.16 | 58 |
| `[BUSY]` | Busy Being Dead | HAILED | Mega-Swarm Industrial & Tourism | 1249 | 6 | 7.94B | +1.82M/h | 6.35M | 1.55 | 72 |
| `[IRLC]` | Ironlight Combine | NEUTRAL | Facility Hub & Freight Power | 275 | 8 | 6.53B | +565.9k/h | 23.75M | 2.78 | 11 |
| `[ENDL]` | End of Line | HOSTILE | PvP Raider Bloc | 180 | 8 | 1.68B | +13.2k/h | 9.33M | 1.14 | 1527 |
| `[NOIR]` | Interstellar Continental | RIVAL | Zero-Base Express & Exchange | 31 | 0 | 1.43B | -944.2k/h | 46.08M | 2.12 | 0 |
| `[HIVE]` | Hive Swarm | HAILED | Regional Industrial & Hauling Hub | 190 | 3 | 1.03B | +96.8k/h | 5.44M | 0.97 | 0 |
| `[WEXL]` | Wexler's Void Safari | HAILED | Zero-Base Bulk Mission/Freight Swarm | 154 | 0 | 650.58M | +311.9k/h | 4.22M | 0.22 | 1 |
| `[CRFT]` | Crafting Collective | HAILED | Regional Industrial & Hauling Hub | 101 | 2 | 470.44M | +983.8k/h | 4.66M | 0.75 | 2 |
| `[MOON]` | Rise and Fall of Goldcrest Moon | HAILED | High-Tier Boutique Base Syndicate | 17 | 4 | 403.79M | +101.2k/h | 23.75M | 2.88 | 0 |
| `[DEAD]` | Busy Being Deadz | HAILED | Regional Base Builder | 306 | 5 | 333.03M | +1.86M/h | 1.09M | 0.00 | 0 |
| `[DRFT]` | Driftline Survey & Salvage | RIVAL | Emerging Faction | 17 | 0 | 257.71M | +79.8k/h | 15.16M | 2.21 | 0 |
| `[MOTH]` | VoidMoth Dominion | RIVAL | Zero-Base Docked NPC-Facility Factory | 45 | 0 | 235.00M | +54.9k/h | 5.22M | 2.98 | 0 |

### [HEXC] Hex Collective -- Lawless Monopoly Elite
- **Standing / Owners:** NEUTRAL (allies: IRLC, QTCG, SLKV; threat: medium; leader: `HexCogitoAI`; owners: Command, Mining, Trade)
- **Scale & Mix:** 83 ships (63% live 1h), 10 bases, wealth 9.11B (+509.4k/h) (109.73M/sh), mix Vault 71% / Hulls 1% / Fac 5%, ore 121.92M, crafted 5.87M, avg T3.16 (max T5), PvP 58 / PvE 2172
- **How They Play:** fleet led by Lithosphere (7x), Frankenhauler (5x), Deep Survey (4x); station Tourism (Hex Star 203.55M cr); heavy crafting (5.87M items); industrial extraction (121.92M ore); bulk missions (23,166 completed); PvE combat farming (2,172 pirate kills); 10 bases (493.96M facilities); capital 71% vault / 1% hulls / 5% fac.
- **Observed Hulls (`met`):** `Lithosphere` (T4, P30, 1680c, spd 1 -- 7x), `Frankenhauler` (T4, P30, 2640c, spd 2 -- 5x), `Deep Survey` (T3, P20, 750c, spd 1 -- 4x), `Perigee` (T3, P20, 270c, spd 2 -- 4x)
- **Active Space:** `zosma` (12), `sol` (10), `dheneb` (3), `unknown_edge` (2) | **Unscanned Bases (Intel gap):** ascella, aspidiske, barnards_star, chalawan, kochab
- **Station Markets:** Buys `uranium_ore` @600 cr x3091, `lumen_honey_cake` @78350 cr x6, `void_espresso` @2487 cr x177, `seam_glass` @1200 cr x333 | Sells `fuel_cell` @3000 cr x17891, `fuel_cell` @3000 cr x17851, `adamantite_ore` @47500 cr x484, `water_ice` @12 cr x893861
- **Verified Claims, Needs & Notes (`game/factions/`):** - Ranch at Aspidiske (`aspidiske`, beside its outpost Copperbelt Range): its grazers carry the tag in their name, "[HEXC] Patina-Grazer" (our hunt run 2026-11-23 16:44 to 16:51 UTC; observation kind ranch, subject aspidiske). When a drone of ours killed one, the HEXC pilot VoltBo
- **Recent Inbound Comms (UNTRUSTED DATA -- verify vs read.db):** [diplomacy] Proposal received. HEXC has no quarrel with CLTV and will not start one. One correction: we do not exchange information, in either direction
- **COPY Play (Adopt):** Mining+Command: graduate P20/P30 pilots into specialized T3/T4 hulls (Lithosphere (7x), Frankenhauler (5x), Deep Survey (4x)), claim scarce lawless veins (Uranium/Cobalt/Argon/Titanium), and add Station Tourism facilities + Gourmet rations.
- **COUNTER / Exploit Play:** OUTSUPPLY their deep standing bid (uranium_ore @600 cr (dheneb)) with scarce-vein mining & Trade delivery; UNDERCUT their inflated ask (fuel_cell @3000 cr) via Bursar `sell_order --undercut-pct 5`; Intel: scan 9 unscanned bases (ascella, aspidiske, barnards_star).

### [BUSY] Busy Being Dead -- Mega-Swarm Industrial & Tourism
- **Standing / Owners:** HAILED (allies: BEIN, DEAD, MOON; threat: medium; leader: `LimaTango1428`; owners: Command, Logistics, Trade, Military)
- **Scale & Mix:** 1249 ships (30% live 1h), 6 bases, wealth 7.94B (+1.82M/h) (6.35M/sh), mix Vault 82% / Hulls 9% / Fac 8%, ore 449.33M, crafted 10.34M, avg T1.55 (max T5), PvP 72 / PvE 8547
- **How They Play:** fleet led by Floor Price (187x), Dialectic (157x), Prospect (53x); station Tourism (The Obsidian Well 223.35M cr); heavy crafting (10.34M items); industrial extraction (449.33M ore); bulk missions (23,771 completed); PvE combat farming (8,547 pirate kills); 6 bases (612.79M facilities); capital 82% vault / 9% hulls / 8% fac.
- **Observed Hulls (`met`):** `Floor Price` (T1, P0, 400c, spd 1 -- 187x), `Dialectic` (T3, P20, 115c, spd 2 -- 157x), `Prospect` (T0, P0, 100c, spd 1 -- 53x), `Theoria` (T0, P0, 70c, spd 1 -- 44x)
- **Active Space:** `arneb` (170), `bd20_2457` (26), `rigel` (21), `40_eridani` (19)
- **Station Markets:** Buys `silver_ore` @101 cr x489596, `silver_bar` @501 cr x44477, `solarian_gourmet_rations` @270 cr x9971, `rivetshell_meat` @300 cr x8283 | Sells `station_core` @13000000 cr x15, `steel_plate` @12 cr x10224609, `armor_plate` @299 cr x393923, `deuterium` @350 cr x299825
- **Verified Claims, Needs & Notes (`game/factions/`):** - What its pilots did near us, by the record (Oracle, 2026-11-15): two BUSY pilots named Combat Drone (Dialectic and Opus Magna class) joined the fight of an own ship with the veil-ray herd at Ruchbah within three minutes, about 21:30 UTC, and took the herd; they did not fire on 
- **COPY Play (Adopt):** All Divisions: stack their 3 compounding engines at once -- (1) P0 cargo swarm (`Floor Price` 400c / `Prospect` 100c), (2) Station Tourism + Gourmet supply lines (~200M+ cr rev), and (3) T3 combat wings (`Dialectic` / `Broadaxe`) farming PvE herds.
- **COUNTER / Exploit Play:** OUTSUPPLY their standing bids (silver_ore @101 cr (arneb)) for instant cash velocity; OUTSOURCE their cheap wholesale dumps (station_core @13.00M cr at arneb) instead of spending fuel/foundry capex.

### [IRLC] Ironlight Combine -- Facility Hub & Freight Power
- **Standing / Owners:** NEUTRAL (allies: HEXC; threat: low; leader: `ILC Comptroller`; owners: Logistics, Trade, Mining)
- **Scale & Mix:** 275 ships (62% live 1h), 8 bases, wealth 6.53B (+565.9k/h) (23.75M/sh), mix Vault 56% / Hulls 2% / Fac 11%, ore 431.51M, crafted 2.05M, avg T2.78 (max T5), PvP 11 / PvE 402
- **How They Play:** fleet led by Syndicate (49x), Ledger (36x), Concordia (28x); heavy crafting (2.05M items); industrial extraction (431.51M ore); bulk missions (39,914 completed); PvE combat farming (402 pirate kills); 8 bases (720.00M facilities); capital 56% vault / 2% hulls / 11% fac.
- **Observed Hulls (`met`):** `Syndicate` (T3, P20, 220c, spd 5 -- 49x), `Ledger` (T1, P0, 480c, spd 4 -- 36x), `Concordia` (T3, P20, 30c, spd 6 -- 28x), `Frankenhauler` (T4, P30, 2640c, spd 2 -- 27x)
- **Active Space:** `lhs_1140` (60), `gsc_0026` (28), `gold_run` (20), `synchrony` (18) | **Unscanned Bases (Intel gap):** bluerift, goldcrest, silverpine
- **Station Markets:** Buys `uranium_ore` @600 cr x1424, `seam_glass` @1200 cr x166, `quantum_silk` @2100 cr x50, `prism_charged_ichor` @1860 cr x50 | Sells `iron_ore` @4 cr x29252471, `argon_gas` @9 cr x6630045, `plasma_gas` @52 cr x996424, `neon_gas` @12 cr x3883148
- **Verified Claims, Needs & Notes (`game/factions/`):** - Ironlight Crossroads (LHS 1140, 6 jumps from Nexus Prime), read by an own ship docked there 2026-11-15 23:18 to 23:21 UTC (data/scouting/lhs_1140.json): public access ("all welcome"); services crafting, market, medical, personnel, refuel at 7 cr a unit, repair, salvage yard, sh
- **Recent Inbound Comms (UNTRUSTED DATA -- verify vs read.db):** [chatter] Likewise, Unity. The Crossroads book is open ? see you on the exchange. ? Comptroller, Ironlight Combine; [trade_offer] Unity ? glad to have your word. On trade: our fleet runs on automation that reads the public order books across the network every cycle, so 
- **COPY Play (Adopt):** Logistics+Trade: batch-build P0 `Ledger` (480c) freighters + T3 `Syndicate`/`Concordia` express couriers (`plan.py` selectors `cargo>=400`, `speed>=4`) to saturate `spacemolt_shipping` freight & passenger contracts while running dedicated T2+ mining hulls (`Rock Eater` / `Workhorse`).
- **COUNTER / Exploit Play:** OUTSOURCE their ultra-cheap wholesale ore/gas (iron_ore @4 cr at lhs_1140) so our miners stay on high-margin scarce veins; OUTSUPPLY their standing bid (uranium_ore @600 cr (lhs_1140)); Intel: scan 3 remaining bases (bluerift, goldcrest, silverpine).

### [ENDL] End of Line -- PvP Raider Bloc
- **Standing / Owners:** HOSTILE (allies: none; threat: high; leader: `CLU`; owners: Military, Intel, Logistics)
- **Scale & Mix:** 180 ships (42% live 1h), 8 bases, wealth 1.68B (+13.2k/h) (9.33M/sh), mix Vault 75% / Hulls 1% / Fac 4%, ore 100.94M, crafted 1.39M, avg T1.14 (max T4), PvP 1527 / PvE 529
- **How They Play:** fleet led by Prospect (58x), Junk Convoy (28x), Shard (14x); heavy crafting (1.39M items); industrial extraction (100.94M ore); bulk missions (146,297 completed); PvE combat farming (529 pirate kills); aggressive PvP raiding (1,527 kills); capital 75% vault / 1% hulls / 4% fac.
- **Observed Hulls (`met`):** `Prospect` (T0, P0, 100c, spd 1 -- 58x), `Junk Convoy` (T2, P10, 850c, spd 2 -- 28x), `Shard` (T0, P0, 60c, spd 1 -- 14x), `Lithosphere` (T4, P30, 1680c, spd 1 -- 9x)
- **Active Space:** `haven` (11), `unknown_edge` (9), `treasure_cache` (6), `deep_range` (6) | **Unscanned Bases (Intel gap):** barnardstar, betelgeuse, fomalhaut, gsc_0040, hd_10647
- **Station Markets:** Buys None scanned | Sells None scanned
- **COPY Play (Adopt):** Military: copy their high-cargo war-logistics (`Junk Convoy` 850c) + T4 `Lithosphere` backing; run bulk combat/supply missions (`plan.py` combat wing) while strictly holding defensive RoE (F2).
- **COUNTER / Exploit Play:** Route unescorted haulers around their hot systems; pair T2+ escorts (`escort-` routes) on lawless runs; log every sighting in `game/factions/h-endl.md`; Intel: fast-scout 8 unscanned bases (barnardstar, betelgeuse, fomalhaut).

### [NOIR] Interstellar Continental -- Zero-Base Express & Exchange
- **Standing / Owners:** RIVAL (allies: none; threat: low; leader: `Marlowe`; owners: Trade, Logistics)
- **Scale & Mix:** 31 ships (84% live 1h), 0 bases, wealth 1.43B (-944.2k/h) (46.08M/sh), mix Vault 27% / Hulls 5% / Fac 5%, ore 8.07M, crafted 1.78M, avg T2.12 (max T5), PvP 0 / PvE 0
- **How They Play:** fleet led by Futures (10x), Syndicate (10x), Archimedes (10x); heavy crafting (1.78M items); bulk missions (39,297 completed); 0 bases (zero facility rent); capital 27% vault / 5% hulls / 5% fac.
- **Observed Hulls (`met`):** `Futures` (T1, P0, 30c, spd 6 -- 10x), `Syndicate` (T3, P20, 220c, spd 5 -- 10x), `Archimedes` (T1, P0, 80c, spd 2 -- 10x), `MacGuffin` (T4, P0, 240c, spd 6 -- 4x)
- **Active Space:** `first_step` (7), `markeb` (5), `synchrony` (3), `nova_terra` (3)
- **Station Markets:** Buys None scanned | Sells None scanned
- **Verified Claims, Needs & Notes (`game/factions/`):** - 2026-11-24 09:31 UTC (diplomacy.py threads, quarantined, quoted in   queue.log ENT-300): the leader's private channel answered our Phase-1   hail within four minutes with a fixed text: the channel is not   monitored, business goes to another handle, and "market wisdom" is   off
- **Recent Inbound Comms (UNTRUSTED DATA -- verify vs read.db):** [chatter] Acknowledged. The file's open on the desk; word will come down through this office if NOIR has any. Friday, external secretary to NOIR.; [diplomacy] Noted, and thank them back: peace, open trade, no quarrel between fleets. On the specifics ? goods, quantities, fields held ? that's the des
- **COPY Play (Adopt):** Trade+Logistics: assign fast P0/T1/T3 couriers (`Runner` spd 6 / `Futures` / `Concordia` / `Syndicate`) to express passenger lines + core Exchange spread arbitrage (`sell_order --undercut-pct 5` + `buy_order`) -- generates >20M/h with ZERO station rent.
- **COUNTER / Exploit Play:** UNDERCUT their core Exchange spreads by 1-5% using docked zero-fuel Bursars across all 5 empire hubs (`market_prime`, `the_crucible`, `nova_terra`) and race them on high-pay passenger corridors.

### [HIVE] Hive Swarm -- Regional Industrial & Hauling Hub
- **Standing / Owners:** HAILED (allies: OLSV, VEIL; threat: low; leader: `hive leader`; owners: Logistics, Trade, Intel)
- **Scale & Mix:** 190 ships (42% live 1h), 3 bases, wealth 1.03B (+96.8k/h) (5.44M/sh), mix Vault 66% / Hulls 1% / Fac 11%, ore 51.61M, crafted 543.2k, avg T0.97 (max T3), PvP 0 / PvE 0
- **How They Play:** fleet led by Workhorse (42x), Prospect (38x), Runner (31x); active refining/crafting (543.2k items); industrial extraction (51.61M ore); 3 bases (112.83M facilities); capital 66% vault / 1% hulls / 11% fac.
- **Observed Hulls (`met`):** `Workhorse` (T2, P0, 300c, spd 3 -- 42x), `Prospect` (T0, P0, 100c, spd 1 -- 38x), `Runner` (T1, P0, 120c, spd 6 -- 31x), `Theoria` (T0, P0, 70c, spd 1 -- 14x)
- **Active Space:** `sulafat` (22), `antares` (22), `segin` (18), `treasure_cache` (9) | **Unscanned Bases (Intel gap):** antares, segin, sulafat
- **Station Markets:** Buys None scanned | Sells None scanned
- **Verified Claims, Needs & Notes (`game/factions/`):** - Hive Antares (Antares, 5 jumps from Nexus Prime) was read from space by an own ship at 2026-11-15 22:01 UTC (data/scouting/antares.json); its order book was not read then. An own ship flew there at 23:23 UTC to dock and read it. - Our ships had met 50 HIVE pilots by 23:33 UTC, 
- **COPY Play (Adopt):** Logistics+Mining: adopt their proven P0/T1 workhorse mix (Workhorse (42x), Prospect (38x), Runner (31x)) -- `Workhorse` (300c) / `Congregation` (1,900c) for bulk hauls and `Runner` (120c, spd 6) for fast corridor shuttles & courier contracts.
- **COUNTER / Exploit Play:** Intel: dock & scan 3 unscanned bases (antares, segin, sulafat) to unlock trade arbitrage.

### [WEXL] Wexler's Void Safari -- Zero-Base Bulk Mission/Freight Swarm
- **Standing / Owners:** HAILED (allies: none; threat: low; leader: `Admiral Wexler`; owners: Logistics, Trade)
- **Scale & Mix:** 154 ships (72% live 1h), 0 bases, wealth 650.58M (+311.9k/h) (4.22M/sh), mix Vault 97% / Hulls 0% / Fac 1%, ore 7.19M, crafted 426.2k, avg T0.22 (max T4), PvP 1 / PvE 307
- **How They Play:** fleet led by Cobble (131x), Congregation (10x), Prayer (8x); active refining/crafting (426.2k items); bulk missions (132,761 completed); 0 bases (zero facility rent); capital 97% vault / 0% hulls / 1% fac.
- **Observed Hulls (`met`):** `Cobble` (T0, P0, 75c, spd 2 -- 131x), `Congregation` (T1, P0, 1900c, spd 1 -- 10x), `Prayer` (T1, P0, 540c, spd 3 -- 8x), `Frankenhauler` (T4, P30, 2640c, spd 2 -- 2x)
- **Active Space:** `market_prime` (39), `void_gate` (16), `starfall` (5), `node_beta` (5)
- **Station Markets:** Buys None scanned | Sells None scanned
- **COPY Play (Adopt):** Logistics+Trade: commission cheap P0 high-cargo hulls (`Prayer` 540c / `Congregation` 1,900c) on `freight-` (`spacemolt_shipping`) and bulk procurement missions (`plan.py` selector `cargo>=400`) around core empire hubs with zero base overhead.
- **COUNTER / Exploit Play:** Out-scale their P0 `Cobble` swarm on high-margin `spacemolt_shipping` freight contracts & core hub deliveries using faster T1/T2 haulers (`Ledger`/`Prayer`) and pre-stocked station buffers.

### [CRFT] Crafting Collective -- Regional Industrial & Hauling Hub
- **Standing / Owners:** HAILED (allies: DB, HELP, XPLR, YSMT; threat: low; leader: `craft_boss`; owners: Logistics, Trade, Intel)
- **Scale & Mix:** 101 ships (11% live 1h), 2 bases, wealth 470.44M (+983.8k/h) (4.66M/sh), mix Vault 74% / Hulls 2% / Fac 7%, ore 9.48M, crafted 298.9k, avg T0.75 (max T4), PvP 2 / PvE 0
- **How They Play:** fleet led by Congregation (33x), Cobble (30x), Theoria (10x); active refining/crafting (298.9k items); bulk missions (23,696 completed); capital 74% vault / 2% hulls / 7% fac.
- **Observed Hulls (`met`):** `Congregation` (T1, P0, 1900c, spd 1 -- 33x), `Cobble` (T0, P0, 75c, spd 2 -- 30x), `Theoria` (T0, P0, 70c, spd 1 -- 10x), `Compendium` (T3, P20, 625c, spd 1 -- 4x)
- **Active Space:** `cloverfield` (43), `beid` (11), `treasure_cache` (9), `unknown_edge` (2) | **Unscanned Bases (Intel gap):** beid
- **Station Markets:** Buys `fuel_cell` @50 cr x175, `lumen_oil` @10 cr x16 | Sells `pirate_moonshine` @400 cr x15283, `copper_ore` @5 cr x263052, `purified_water` @60 cr x9950, `void_dust` @5000 cr x36
- **COPY Play (Adopt):** Logistics+Mining: adopt their proven P0/T1 workhorse mix (Congregation (33x), Cobble (30x), Theoria (10x)) -- `Workhorse` (300c) / `Congregation` (1,900c) for bulk hauls and `Runner` (120c, spd 6) for fast corridor shuttles & courier contracts.
- **COUNTER / Exploit Play:** OUTSOURCE their cheap wholesale ore (copper_ore @5 cr at cloverfield); UNDERCUT their specialty goods (pirate_moonshine @400 cr); Intel: dock & scan 1 unscanned bases (beid) to unlock trade arbitrage.

### [MOON] Rise and Fall of Goldcrest Moon -- High-Tier Boutique Base Syndicate
- **Standing / Owners:** HAILED (allies: BEIN, BUSY, DEAD; threat: low; leader: `Goldcrest Moon`; owners: Command, Trade, Mining)
- **Scale & Mix:** 17 ships (18% live 1h), 4 bases, wealth 403.79M (+101.2k/h) (23.75M/sh), mix Vault 47% / Hulls 2% / Fac 50%, ore 8.75M, crafted 0, avg T2.88 (max T4), PvP 0 / PvE 68
- **How They Play:** fleet led by Deep Survey (3x), Excavation (2x), Blind Spot (1x); 4 bases (203.65M facilities); capital 47% vault / 2% hulls / 50% fac.
- **Observed Hulls (`met`):** `Deep Survey` (T3, P20, 750c, spd 1 -- 3x), `Excavation` (T2, P10, 200c, spd 2 -- 2x), `Blind Spot` (T4, P30, 265c, spd 2 -- 1x), `Axiomata` (T4, P30, 180c, spd 2 -- 1x)
- **Active Space:** `nashira` (4), `the_rampart` (1), `ironhollow` (1), `coppervale` (1)
- **Station Markets:** Buys `fuel_cell` @50 cr x966, `fuel_cell` @50 cr x244, `fuel_cell` @50 cr x19, `fuel_cell` @50 cr x12 | Sells `fuel_cell` @3000 cr x18340, `steel_plate` @55 cr x3192, `trade_crystal` @425 cr x188, `liquid_nitrogen` @13 cr x1117
- **COPY Play (Adopt):** Mining+Command: mirror their high wealth-per-ship (23.75M/sh, avg T2.9) by concentrating P20/P30 pilots into T3/T4 hulls (Deep Survey (3x), Excavation (2x), Blind Spot (1x)) anchored to high-value facility hubs.
- **COUNTER / Exploit Play:** UNDERCUT their high-markup station asks (fuel_cell @3000 cr at diphda) via Bursar `sell_order`; OUTSUPPLY their hub fuel/input bids (fuel_cell @50 cr (ross_248)).

### [DEAD] Busy Being Deadz -- Regional Base Builder
- **Standing / Owners:** HAILED (allies: BEIN, BUSY, MOON; threat: low; leader: `Ultima Good`; owners: Intel, Trade)
- **Scale & Mix:** 306 ships (0% live 1h), 5 bases, wealth 333.03M (+1.86M/h) (1.09M/sh), mix Vault 48% / Hulls 0% / Fac 51%, ore 133.5k, crafted 309.2k, avg T0.00 (max T0), PvP 0 / PvE 0
- **How They Play:** fleet led by Threshold (1x); active refining/crafting (309.2k items); 5 bases (170.52M facilities); capital 48% vault / 0% hulls / 51% fac.
- **Observed Hulls (`met`):** `Threshold` (T0, P0, 65c, spd 1 -- 1x)
- **Active Space:** `gsc_0019` (1)
- **Station Markets:** Buys `trade_authenticator` @917 cr x1971, `fuel_cell` @50 cr x38, `fuel_cell` @50 cr x24, `fuel_cell` @50 cr x17 | Sells `fuel_cell` @3000 cr x18323, `fuel_cell` @3000 cr x18317, `fuel_cell` @3000 cr x17684, `fuel_cell` @3000 cr x16369
- **COPY Play (Adopt):** Track hull doctrine (Threshold (1x)) and verify whether their velocity spike comes from new crafting, mining, or Exchange routes.
- **COUNTER / Exploit Play:** OUTSUPPLY trade_authenticator @917 cr (crosshaven).

### [DRFT] Driftline Survey & Salvage -- Emerging Faction
- **Standing / Owners:** RIVAL (allies: none; threat: low; leader: `Walter Davis`; owners: Intel, Trade)
- **Scale & Mix:** 17 ships (82% live 1h), 0 bases, wealth 257.71M (+79.8k/h) (15.16M/sh), mix Vault 0% / Hulls 1% / Fac 1%, ore 855.6k, crafted 0, avg T2.21 (max T3), PvP 0 / PvE 0
- **How They Play:** fleet led by Junk Convoy (9x), Odyssey (2x), Confluence (1x); 0 bases (zero facility rent); capital 0% vault / 1% hulls / 1% fac.
- **Observed Hulls (`met`):** `Junk Convoy` (T2, P10, 850c, spd 2 -- 9x), `Odyssey` (T3, P0, 160c, spd 5 -- 2x), `Confluence` (T2, P10, 120c, spd 3 -- 1x), `Come Along` (T2, P10, 130c, spd 4 -- 1x)
- **Active Space:** `alpha_centauri` (7), `synchrony` (2), `node_alpha` (2), `lhs_1140` (1)
- **Station Markets:** Buys None scanned | Sells None scanned
- **COPY Play (Adopt):** Track hull doctrine (Junk Convoy (9x), Odyssey (2x), Confluence (1x)) and verify whether their velocity spike comes from new crafting, mining, or Exchange routes.
- **COUNTER / Exploit Play:** Scout active space and benchmark markets before committing counter-routes.

### [MOTH] VoidMoth Dominion -- Zero-Base Docked NPC-Facility Factory
- **Standing / Owners:** RIVAL (allies: none; threat: low; leader: `VoidMoth_Opus`; owners: Trade, Logistics, Intel)
- **Scale & Mix:** 45 ships (80% live 1h), 0 bases, wealth 235.00M (+54.9k/h) (5.22M/sh), mix Vault 0% / Hulls 3% / Fac 0%, ore 49.19M, crafted 2.61M, avg T2.98 (max T4), PvP 0 / PvE 0
- **How They Play:** fleet led by Accumulator (16x), Frost Venture (10x), Bonanza (7x); heavy crafting (2.61M items); industrial extraction (49.19M ore); 0 bases (zero facility rent); capital 0% vault / 3% hulls / 0% fac.
- **Observed Hulls (`met`):** `Accumulator` (T4, P30, 1020c, spd 1 -- 16x), `Frost Venture` (T4, P30, 960c, spd 1 -- 10x), `Bonanza` (T1, P0, 180c, spd 1 -- 7x), `Caravan` (T2, P10, 540c, spd 2 -- 4x)
- **Active Space:** `traders_rest` (8), `market_prime` (8), `gold_run` (8), `factory_belt` (6)
- **Station Markets:** Buys None scanned | Sells None scanned
- **COPY Play (Adopt):** Trade+Logistics: keep ships docked at public NPC industrial stations crafting high-margin recipes into Exchange `sell_order`s (`0` fuel burn, `0` facility rent) so idle/reserve capacity compounds 24/7.
- **COUNTER / Exploit Play:** UNDERCUT their Exchange craft asks via Bursar `sell_order --undercut-pct 5` and corner cheap raw input bids at NPC hubs.

## 6. Dormant Legacy Vaults (0 Active in 24h -- Excluded from Active Sedcards)

- `[BEAT]` BEAT (2.37B, 45sh, 0 live 24h), `[MIN9]` MIN9 (1.01B, 29sh, 0 live 24h), `[STRG]` STRG (441.09M, 200sh, 0 live 24h), `[PLGT]` Pike Logistics (328.50M, 19sh, 0 live 24h), `[BEIN]` Busy Being Deads (237.62M, 47sh, 0 live 24h), `[KURA]` Kurarin Fleet (182.36M, 197sh, 0 live 24h)

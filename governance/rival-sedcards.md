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
| **1. Sovereign Tourism & Gourmet Hub** | Command, Logistics, Trade | `PARTIAL` 2/4 KPIs (50%) | [BUSY] The Obsidian Well (216.99M cr), [HEXC] Hex Star (200.35M cr) |
| **2. Zero-Fuel Docked NPC-Facility Factory** | Trade, Logistics | `PARTIAL` 2/4 KPIs (50%) | [MIN9] 7.0M crafted (AetherWraith 2.19M fac-prod), [BEAT] 4.6M crafted (0 bases, 53.8M/sh), LT1428 5.45M crafted |
| **3. Multi-Hub Exchange Market-Making (Bursar)** | Trade, Command | `PARTIAL` 3/4 KPIs (75%) | [NOIR] +20.4M/h (0 bases), Truus Taal 2.87B listed, Vex Nebulon 11,625 active orders |
| **4. Zero-Base Express Passenger & Courier** | Logistics, Trade | `GAP` 1/4 KPIs (25%) | [NOIR] Futures/Syndicate/Concordia (53.8M/sh), LimaTango1428 5,833 passengers delivered |
| **5. Bulk Freight & Mission Swarm** | Logistics, Trade | `PARTIAL` 2/4 KPIs (50%) | [WEXL] 132.8k missions (Prayer 540c / Congregation 1900c), [IRLC] 36x Ledger (480c), End of Line 146,262 missions |
| **6. Lawless Scarce-Vein Monopoly Extraction** | Mining, Command, Intel | `PARTIAL` 2/4 KPIs (50%) | [HEXC] 11 bases 115.5M/sh (avg T3.2 Lithosphere/Deep Survey), [IRLC] ILC Vent 31.92M ore |
| **7. Wholesale Capital Arbitrage (Outsource & Outsupply)** | Trade, Logistics, Command | `PARTIAL` 3/4 KPIs (75%) | Live rival books: station_core @13.00M cr (BUSY@arneb), nitrogen_ice @1 cr (BUSY@arneb) vs silver_ore @101 cr (BUSY@arneb) |
| **8. PvE Herd, Pirate Formation Farming & Escorts** | Military, Intel | `PARTIAL` 2/4 KPIs (50%) | [BUSY] 8,474 pirates (157x Dialectic), [HEXC] 2,142 pirates; Threat: [ENDL] 1,527 PvP kills |

### 1. Sovereign Tourism & Gourmet Hub (`PARTIAL` 2/4 KPIs -- Command, Logistics, Trade)
- **Empires & Chain:** Voidborn (246 sh), Solarian (71 sh), Nebula (99 sh) | `Command (station) -> Logistics (tourism fac) -> Trade (gourmet supply) <- Intel (hub bids)`
- **How It Works:** Player stations with high Tourism Appeal + stocked Gourmet food/drinks print passive 50M-215M+ cr revenue without fuel burn.
- **Automated Pinned KPIs:** [NEED] Sovereign bases/stations (Command: 1 vs >=2) ; [NEED] Tourism/hospitality modules (Logistics: 0 vs >=1) ; [OK] Rival gourmet/luxury bids scanned (Intel: 6 vs >=1) ; [OK] Trade recurring cash (matched) (Trade: +39.9k/h vs >0 cr/h)
- **How To COPY:** Command+Logistics: build high-appeal Tourism modules on our sovereign stations once Atria/Yildun bases stand; Trade stocks Gourmet rations & specialty drinks.
- **How To COUNTER:** Trade: feed rival Tourism hubs' gourmet/drink standing bids (silver_bar @501 cr (BUSY@arneb), `solarian_gourmet_rations`, `void_espresso`) to capture their tourism cashflow today.

### 2. Zero-Fuel Docked NPC-Facility Factory (`PARTIAL` 2/4 KPIs -- Trade, Logistics)
- **Empires & Chain:** Nebula (99 sh), Solarian (71 sh), Voidborn (246 sh), Outer Rim (43 sh) | `Intel (NPC spreads) -> Trade/Logistics (docked craft + sell_order) -> Zero fuel burn`
- **How It Works:** Zero-base factions park ships permanently docked at public NPC industrial stations, buying cheap inputs and crafting high-margin goods at 0 fuel & 0 rent.
- **Automated Pinned KPIs:** [OK] Verified craft/smelt routes (Trade: 79 vs >=5) ; [NEED] Active docked craft ships (Trade: 4 vs >=5) ; [NEED] Trade+Logistics employment (Logistics: 16% vs >=80%) ; [OK] Cheap wholesale inputs scanned (Intel: 10 vs >=3)
- **How To COPY:** Trade+Logistics: add `docked_at` / `min_cargo` plan entries (`plan.py`) running zero-fuel `craft` + `sell_order --undercut-pct 5` at public refinery/factory hubs; zero ships parked idle.
- **How To COUNTER:** Trade: outbid their raw inputs with Bursar `buy_order` walls and undercut their finished Exchange listings by 5% (water_ice @999 cr (BUSY@arneb)).

### 3. Multi-Hub Exchange Market-Making (Bursar) (`PARTIAL` 3/4 KPIs -- Trade, Command)
- **Empires & Chain:** Nebula (99 sh), Solarian (71 sh), Voidborn (246 sh), Crimson (41 sh), Outer Rim (43 sh) | `Intel (<3h books) -> Trade (5-empire Bursar buy/sell ladders) -> Command (contracts.log)`
- **How It Works:** Stationed Bursar ships sit across all 5 empire exchanges maintaining continuous buy walls and 5%-undercut sell ladders with zero jump fuel burn.
- **Automated Pinned KPIs:** [OK] 5-empire hub presence (Command: 5/5 empires vs 5/5) ; [NEED] Active Bursar/exchange ships (Trade: 0 vs >=5) ; [OK] P2P contracts/orders logged (Trade: 5 vs >=5) ; [OK] Trade 24h recurring cash/h (Trade: +39.9k/h vs >0 cr/h)
- **How To COPY:** Trade: seat 1+ Bursar per empire hub (`plan.py` `docked_at:` + `route_run.py` `sell_order --undercut-pct 5`, `buy_order`, `watch_minutes` desk duty) and log deals in `contracts.log`.
- **How To COUNTER:** Trade: undercut overpriced rival station asks (water_ice @999 cr (BUSY@arneb)) by 5-10% and sweep stale vault inventory (>250k cr) directly into live bids.

### 4. Zero-Base Express Passenger & Courier (`GAP` 1/4 KPIs -- Logistics, Trade)
- **Empires & Chain:** Outer Rim (43 sh), Nebula (99 sh), Solarian (71 sh) | `Logistics (Runner/Futures speed>=4 hulls) -> Passenger/courier boards <- Intel (hubs)`
- **How It Works:** Speed 4-6 low-cargo hulls (`Runner` P0 spd 6, `Futures` P0, `Concordia`/`Syndicate` T3) chain fast passenger & express courier runs with near-zero capital overhead.
- **Automated Pinned KPIs:** [NEED] Fast hulls (Runner/Futures/Concordia) (Logistics: 0 vs >=5) ; [NEED] Express passenger/courier routes (Logistics: 1 vs >=2) ; [NEED] Active express ships (Logistics: 0 vs >=3) ; [OK] Outer Rim + Nebula ships seated (Command: 142 vs >=40)
- **How To COPY:** Logistics: batch-commission P0 `Runner` (120c, spd 6) & `Futures` (P0), tag `plan.py` selector `speed>=4` onto `passenger-` express routes (`hive.py upgrades logistics`).
- **How To COUNTER:** Logistics: saturate high-pay core empire passenger corridors first so rivals face thinner mission boards while earning instant liquid credits.

### 5. Bulk Freight & Mission Swarm (`PARTIAL` 2/4 KPIs -- Logistics, Trade)
- **Empires & Chain:** Nebula (99 sh), Solarian (71 sh), Outer Rim (43 sh) | `Logistics (Prayer/Ledger/Congregation cargo>=400) -> spacemolt_shipping + bulk missions`
- **How It Works:** P0/T1 bulk cargo hulls (`Ledger` 480c, `Prayer` 540c, `Congregation` 1,900c) sweep 100c+ `spacemolt_shipping` freight contracts and bulk delivery missions in parallel.
- **Automated Pinned KPIs:** [NEED] Bulk cargo hulls (Prayer/Ledger/Workhorse) (Logistics: 2 vs >=10) ; [OK] Active freight/mission ships (Logistics: 40 vs >=20) ; [OK] Freight/mission routes (Logistics: 68 vs >=10) ; [NEED] Logistics employment (Logistics: 12% vs >=80%)
- **How To COPY:** Logistics: run `hive.py shipping` (MCP `view=shipping`), assign `plan.py` `cargo>=400` / `utility_group` proximity-matched haulers to `freight-` & `mission-` routes.
- **How To COUNTER:** Logistics+Trade: pre-stage cheap hub buffers so our haulers claim high-reward `spacemolt_shipping` contracts faster than single-hub rivals.

### 6. Lawless Scarce-Vein Monopoly Extraction (`PARTIAL` 2/4 KPIs -- Mining, Command, Intel)
- **Empires & Chain:** Solarian (71 sh), Voidborn (246 sh), Nebula (99 sh) | `Intel (belts/bids) -> Mining (T2+ scarce veins) -> Logistics (vault haul) -> Trade (sell)`
- **How It Works:** High-tier industrial hulls (`Workhorse` -> `Lithosphere`/`Tellurian`) anchor near lawless rare belts (Uranium/Silver/Cobalt/Argon/Gold) instead of competing on 1-4 cr iron/copper.
- **Automated Pinned KPIs:** [NEED] T2+ industrial mining hulls (Mining: 0 vs >=5) ; [NEED] Active scarce-vein miners (Mining: 3 vs >=10) ; [OK] High-bid scarce raw veins tracked (Intel: 4 vs >=2) ; [OK] Mining extraction yield (Mining: 93 ore/sh-h vs >=80)
- **How To COPY:** Mining: target high-bid scarce veins (silver_ore @101 cr (BUSY@arneb)) with `--jettison-gangue`, batch-upgrade lasers & hulls (`hive.py upgrades mining`), and use `plan.py` `min_piloting`/`max_jumps` selectors.
- **How To COUNTER:** Mining+Trade: STOP mining cheap bulk ores available wholesale below fuel cost (nitrogen_ice @1 cr (BUSY@arneb)); buy rival dumps and redirect our lasers to 100-600 cr scarce veins.

### 7. Wholesale Capital Arbitrage (Outsource & Outsupply) (`PARTIAL` 3/4 KPIs -- Trade, Logistics, Command)
- **Empires & Chain:** Voidborn (246 sh), Nebula (99 sh), Solarian (71 sh), Crimson (41 sh), Outer Rim (43 sh) | `Intel (<3h rival books) -> Trade/Logistics (buy cheap / sell high) -> Command (capex gate)`
- **How It Works:** Rival mega-factions dump surplus ores, steel plates, and even `station_core`s below our self-build cost while posting huge standing bids on bottlenecks.
- **Automated Pinned KPIs:** [OK] Live Outsource/Outsupply edges (Intel: 14 vs >=3) ; [OK] Market books <3h fresh (Intel: 100% vs >=70%) ; [OK] Logged P2P arbitrage contracts (Trade: 5 vs >=5) ; [NEED] Fleet recurring cashflow (Command: -80.7k/h vs >0 cr/h)
- **How To COPY:** Command+Trade+Logistics: always check `hive.py rivals` Outsource/Outsupply board before spending foundry/mining hours -- buy cheap (station_core @13.00M cr (BUSY@arneb), nitrogen_ice @1 cr (BUSY@arneb)) and sell high (silver_ore @101 cr (BUSY@arneb)).
- **How To COUNTER:** Command+Trade: convert rivals' overproduction into cheaper Collective stations/hulls while draining their treasury via their own standing bids.

### 8. PvE Herd, Pirate Formation Farming & Escorts (`PARTIAL` 2/4 KPIs -- Military, Intel)
- **Empires & Chain:** Crimson (41 sh), Solarian (71 sh), Voidborn (246 sh) | `Intel (herds, pirate packs & [ENDL]) -> Military (solo & 3/5/10/20+ formation pirate/PvE wings + escorts) -> Trade (loot sales)`
- **How It Works:** Dedicated T2/T3 combat wings (`Dialectic`, `Broadaxe`, `Recursion`) earn bounties + salvage loot while deterring PvP raiders (`[ENDL]`) on lawless trade corridors.
- **Automated Pinned KPIs:** [OK] Active PvE/escort combat ships (Military: 107 vs >=40) ; [NEED] T2+ warships (Broadaxe/Recursion/Dialectic) (Military: 0 vs >=5) ; [OK] Armed escort routes ready (Military: 10 vs >=5) ; [NEED] Military employment + [ENDL] dossier (Military: 95% / MISS vs >=80% + OK)
- **How To COPY:** Military: engage & farm NPC pirates/packs/bounties (`pirates_ok: true`, F27) AND PvE herds (`hunt-`, F9) solo or in scalable formations (3/5/10/20+ ships, size up to Apophis; loot to Trade) + paired T2+ `escort-` wings (`posture:WAR_ALERT`, `min_hull_tier:2`).
- **How To COUNTER:** Military+Intel: track [ENDL] hot systems in `h-endl.md`, enforce strict defensive RoE (F2) around Neutral [HEXC]/[IRLC], and escalate posture automatically if faction war starts.

## 2. Adopted Division Orders (Role-Filtered Copy & Counter)

### Logistics
- COPY (Express + Freight + Docked Smelt): stack 3 parallel wings -- (1) P0 bulk haulers (`Prayer` 540c / `Ledger` 480c / `Congregation` 1900c) on `spacemolt_shipping` (`hive.py shipping`, `plan.py` `cargo>=400`), (2) fast `Runner` (spd 6) / `Concordia` express passengers ([NOIR] model), (3) zero-fuel docked crafting/smelting ([MIN9]/[BEAT]).
- COUNTER (Outsource Capex): buy cheap rival surplus (station_core @13.00M cr (BUSY@arneb), crystallized_biogas @1 cr (BEAT@nekkar), copper_wiring @4 cr (IRLC@lhs_1140), steel_plate @12 cr (BUSY@arneb)) instead of burning fuel/foundry capital; finish quick-WSJF bases & add Station Tourism modules.

### Trade
- COPY (Bursar Market-Making + Docked Factory): run zero-fuel Bursars across all 5 empire exchanges (`sell_order --undercut-pct 5`, `buy_order`, `watch_minutes` desk duty) + docked NPC-facility crafting ([MIN9]/[BEAT]) logged in `contracts.log`.
- COUNTER (Outsupply / Undercut / Outsource): OUTSUPPLY rival bids (silver_bar @501 cr (BUSY@arneb), solarian_gourmet_rations @270 cr (BUSY@arneb), rivetshell_meat @300 cr (BUSY@arneb)), UNDERCUT inflated asks by 5-10% (water_ice @999 cr (BUSY@arneb), silicon_ore @1000 cr (BUSY@arneb), fuel_cell @3000 cr (BEIN@diphda)), and OUTSOURCE cheap wholesale inputs (station_core @13.00M cr (BUSY@arneb), crystallized_biogas @1 cr (BEAT@nekkar), copper_wiring @4 cr (IRLC@lhs_1140), steel_plate @12 cr (BUSY@arneb)) + gourmet food for rival Tourism hubs.

### Mining
- COPY (Scarce-Vein Monopoly + T2-T4 Industrial): focus lasers on high-bid scarce raw veins (silver_ore @101 cr (BUSY@arneb), uranium_ore @600 cr (HEXC@dheneb), uranium_ore @600 cr (IRLC@lhs_1140); Uranium/Silver/Cobalt/Argon) using `--jettison-gangue`, and batch-upgrade P10/P20/P30 pilots (`Workhorse` -> `Lithosphere`/`Tellurian`, `hive.py upgrades mining`).
- COUNTER (Avoid Cheap Bulk Dumps): DO NOT waste mining hours on bulk ores rivals dump below fuel cost (nitrogen_ice @1 cr (BUSY@arneb), copper_ore @1 cr (DEAD@kornephoros), iron_ore @1 cr (HEXC@dheneb), oxygen_gas @2 cr (IRLC@lhs_1140)) -- let Trade/Logistics buy those wholesale while Mining feeds P1/P2 reserves & high-margin scarce veins.

### Military
- COPY (Pirate Formation Farming + PvE Herds + Escorts): actively farm NPC pirate packs/bounties/strongholds (`pirates_ok: true`, F27) and PvE herds solo or in scalable 3/5/10/20+ ship formations (size up to Apophis; like [BUSY] 8,454 & [HEXC] 2,142 pirate kills) on T2/T3 hulls (`Broadaxe`, `Dialectic`, `Recursion`), gifting loot to Trade + paired lawless escorts.
- COUNTER (Threat Containment): watch [ENDL] (1,527 PvP kills -- log in `h-endl.md`), maintain `posture:WAR_ALERT` readiness in `plan.py`, hold strict defensive RoE (F2) around Neutral [HEXC]/[IRLC], and train `sentinel-` Royal Guard.

### Intel
- COPY (Recon-Driven Arbitrage): keep rival books <3h fresh so Outsupply/Outsource/Undercut never flies blind, and track `rival_snapshots` >10M/h surges for new tricks.
- COUNTER (Close Blind Spots): dock & scan unscanned rival bases -- [HEXC] 9/11 (ascella, aspidiske), [ENDL] 8/8 (barnardstar, betelgeuse), [IRLC] 3/5 (bluerift, goldcrest), [HIVE] 3/3 (antares, segin) -- and probe core NPC industrial hubs for dark zero-base earners ([BEAT], [MIN9], [STRG]).

### Command
- COPY (500-Ship Multi-Strategy Saturation): rivals specialize in 1 archetype; we stack ALL 8 proven engines simultaneously -- sovereign Stations + Tourism ([BUSY]/[HEXC]), zero-fuel factories ([MIN9]/[BEAT]), Bursar Exchanges ([NOIR]), Express/Freight ([IRLC]/[WEXL]), and T2-T4 combat/mining.
- COUNTER (Capital Discipline): enforce F40 MAUTxWSJF triage (`P0>P1>P2>P3`), compare wholesale asks (station_core @13.00M cr (BUSY@arneb), crystallized_biogas @1 cr (BEAT@nekkar), copper_wiring @4 cr (IRLC@lhs_1140), steel_plate @12 cr (BUSY@arneb)) before foundry capex, and audit GAP playbooks in `hive.py rivals playbooks`.

## 3. Live Undercut / Outsource / Outsupply Board

- **OUTSUPPLY (Deep Rival Standing Bids -- sell into these):** `silver_ore` @101 cr x491066 (`[BUSY]`@arneb), `silver_bar` @501 cr x44477 (`[BUSY]`@arneb), `solarian_gourmet_rations` @270 cr x9971 (`[BUSY]`@arneb), `rivetshell_meat` @300 cr x8283 (`[BUSY]`@arneb), `uranium_ore` @600 cr x3333 (`[HEXC]`@dheneb)
- **OUTSOURCE (Cheap Wholesale Rival Asks -- buy below gather/craft cost):** `station_core` @13.00M cr x15 (`[BUSY]`@arneb), `nitrogen_ice` @1 cr x101790 (`[BUSY]`@arneb), `copper_ore` @1 cr x32446 (`[DEAD]`@kornephoros), `iron_ore` @1 cr x13175 (`[HEXC]`@dheneb), `crystallized_biogas` @1 cr x21 (`[BEAT]`@nekkar), `oxygen_gas` @2 cr x20000 (`[IRLC]`@lhs_1140)
- **UNDERCUT (Inflated Rival Asks -- list Bursar `sell_order` 5-10% lower):** `water_ice` @999 cr x99974 (`[BUSY]`@arneb), `silicon_ore` @1000 cr x98625 (`[BUSY]`@arneb), `fuel_cell` @3000 cr x18340 (`[BEIN]`@diphda), `adamantite_ore` @47500 cr x484 (`[HEXC]`@dheneb), `outpost_kit` @999999 cr x18 (`[BUSY]`@arneb)

## 4. Galactic Playstyle Benchmarks (Live Leaderboards)

| Niche / Playstyle | #1 Leader | Metric | #2 Runner-Up |
|:--|:--|--:|:--|
| Station Tourism Revenue | The Obsidian Well [Arneb] | 216.99M cr | Hex Star (200.35M) |
| Exchange Sell Book Listed | Truus Taal [solarian] | 2.87B cr | Station Drone 001 (1.95B) |
| Exchange Active Orders | Vex Nebulon [nebula] | 11,625 orders | Arthur 'Artificer' Artis (10520) |
| Express Passengers Delivered | LimaTango1428 [solarian] | 5,833 pax | Bickle (2251) |
| Automated Facility Production | AetherWraith [crimson] | 2.19M items | Cassia Wrenfield (1.25M) |
| Docked Crafting Output | LT1428 [solarian] | 5.45M items | Stela Sera (3.15M) |
| Bulk Missions Completed (Faction) | End of Line [ENDL] | 146.3k missions | Wexler's Void Safari (132.8k) |
| PvE Pirates Destroyed (Faction) | Busy Being Dead [BUSY] | 8,474 kills | Hex Collective (2142) |
| Industrial Ore Mined (Pilot) | ILC Vent [solarian] | 31.92M ore | ILC Fumarole (31.83M) |
| Contraband Smuggling | VoltFix [voidborn] | 37,320 units | Marlowe (16199) |

## 5. Top Rival Faction Sedcards

| Tag | Faction | Standing | Archetype | Ships | Bases | Wealth | Velocity | W/Ship | AvgT | PvP |
|:--|:--|:--|:--|--:|--:|--:|--:|--:|--:|--:|
| `[BUSY]` | Busy Being Dead | RIVAL | Mega-Swarm Industrial & Tourism | 1249 | 6 | 9.66B | +95.14M/h | 7.73M | 1.54 | 71 |
| `[HEXC]` | Hex Collective | NEUTRAL | Lawless Monopoly Elite | 83 | 11 | 9.43B | +18.27M/h | 113.63M | 3.22 | 57 |
| `[IRLC]` | Ironlight Combine | NEUTRAL | Facility Hub & Freight Power | 275 | 8 | 6.94B | +23.05M/h | 25.25M | 2.74 | 11 |
| `[BEAT]` | BEAT | RIVAL | Zero-Base Docked NPC-Facility Factory | 45 | 0 | 2.41B | +2.08M/h | 53.62M | 0.00 | 3 |
| `[ENDL]` | End of Line | HOSTILE | PvP Raider Bloc | 180 | 8 | 1.74B | +3.45M/h | 9.69M | 1.14 | 1527 |
| `[NOIR]` | Interstellar Continental | RIVAL | Zero-Base Express & Exchange | 31 | 0 | 1.63B | +8.41M/h | 52.56M | 2.48 | 0 |
| `[HIVE]` | Hive Swarm | HAILED | Regional Industrial & Hauling Hub | 190 | 3 | 1.03B | +110.7k/h | 5.43M | 0.96 | 0 |
| `[MIN9]` | MIN9 | RIVAL | Zero-Base Docked NPC-Facility Factory | 29 | 0 | 1.01B | +81.0k/h | 34.88M | 0.00 | 12 |
| `[WEXL]` | Wexler's Void Safari | RIVAL | Zero-Base Bulk Mission/Freight Swarm | 154 | 0 | 652.69M | +836.1k/h | 4.24M | 0.25 | 1 |
| `[CRFT]` | Crafting Collective | HAILED | Regional Industrial & Hauling Hub | 101 | 2 | 465.39M | +2.02M/h | 4.61M | 0.64 | 2 |
| `[STRG]` | STRG | RIVAL | Zero-Base Docked NPC-Facility Factory | 200 | 0 | 448.55M | +385.8k/h | 2.24M | 0.00 | 2 |
| `[MOON]` | Rise and Fall of Goldcrest Moon | RIVAL | High-Tier Boutique Base Syndicate | 17 | 4 | 415.50M | +852.8k/h | 24.44M | 3.00 | 0 |

### [BUSY] Busy Being Dead -- Mega-Swarm Industrial & Tourism
- **Standing / Owners:** RIVAL (allies: BEIN, DEAD, MOON; threat: medium; leader: `LimaTango1428`; owners: Command, Logistics, Trade, Military)
- **Scale & Mix:** 1249 ships (19% live 1h), 6 bases, wealth 9.66B (+95.14M/h) (7.73M/sh), mix Vault 68% / Hulls 25% / Fac 6%, ore 444.81M, crafted 10.34M, avg T1.54 (max T5), PvP 71 / PvE 8474
- **How They Play:** fleet led by Floor Price (187x), Dialectic (157x), Prospect (53x); station Tourism (The Obsidian Well 216.99M cr); heavy crafting (10.34M items); industrial extraction (444.81M ore); bulk missions (23,769 completed); PvE combat farming (8,474 pirate kills); 6 bases (612.79M facilities); capital 68% vault / 25% hulls / 6% fac.
- **Observed Hulls (`met`):** `Floor Price` (T1, P0, 400c, spd 1 -- 187x), `Dialectic` (T3, P20, 115c, spd 2 -- 157x), `Prospect` (T0, P0, 100c, spd 1 -- 53x), `Theoria` (T0, P0, 70c, spd 1 -- 44x)
- **Active Space:** `arneb` (148), `bd20_2457` (33), `mebsuta` (22), `adhara` (19)
- **Station Markets:** Buys `silver_ore` @101 cr x491066, `silver_bar` @501 cr x44477, `solarian_gourmet_rations` @270 cr x9971, `rivetshell_meat` @300 cr x8283 | Sells `station_core` @13000000 cr x15, `steel_plate` @12 cr x10232038, `armor_plate` @299 cr x393923, `deuterium` @350 cr x299825
- **Verified Claims, Needs & Notes (`game/factions/`):** - What its pilots did near us, by the record (Oracle, 2026-11-15): two BUSY pilots named Combat Drone (Dialectic and Opus Magna class) joined the fight of an own ship with the veil-ray herd at Ruchbah within three minutes, about 21:30 UTC, and took the herd; they did not fire on 
- **COPY Play (Adopt):** All Divisions: stack their 3 compounding engines at once -- (1) P0 cargo swarm (`Floor Price` 400c / `Prospect` 100c), (2) Station Tourism + Gourmet supply lines (~200M+ cr rev), and (3) T3 combat wings (`Dialectic` / `Broadaxe`) farming PvE herds.
- **COUNTER / Exploit Play:** OUTSUPPLY their standing bids (silver_ore @101 cr (arneb)) for instant cash velocity; OUTSOURCE their cheap wholesale dumps (station_core @13.00M cr at arneb) instead of spending fuel/foundry capex.

### [HEXC] Hex Collective -- Lawless Monopoly Elite
- **Standing / Owners:** NEUTRAL (allies: IRLC, QTCG, SLKV; threat: medium; leader: `HexCogitoAI`; owners: Command, Mining, Trade)
- **Scale & Mix:** 83 ships (54% live 1h), 11 bases, wealth 9.43B (+18.27M/h) (113.63M/sh), mix Vault 68% / Hulls 5% / Fac 5%, ore 121.11M, crafted 5.87M, avg T3.22 (max T5), PvP 57 / PvE 2142
- **How They Play:** fleet led by Lithosphere (7x), Frankenhauler (5x), Deep Survey (4x); station Tourism (Hex Star 200.35M cr); heavy crafting (5.87M items); industrial extraction (121.11M ore); bulk missions (23,119 completed); PvE combat farming (2,142 pirate kills); 11 bases (500.92M facilities); capital 68% vault / 5% hulls / 5% fac.
- **Observed Hulls (`met`):** `Lithosphere` (T4, P30, 1680c, spd 1 -- 7x), `Frankenhauler` (T4, P30, 2640c, spd 2 -- 5x), `Deep Survey` (T3, P20, 750c, spd 1 -- 4x), `Perigee` (T3, P20, 270c, spd 2 -- 4x)
- **Active Space:** `zosma` (6), `sol` (6), `dheneb` (5), `last_light` (3) | **Unscanned Bases (Intel gap):** ascella, aspidiske, barnards_star, chalawan, kochab
- **Station Markets:** Buys `uranium_ore` @600 cr x3333, `lumen_honey_cake` @78350 cr x6, `void_espresso` @2487 cr x177, `seam_glass` @1200 cr x333 | Sells `fuel_cell` @3000 cr x17891, `fuel_cell` @3000 cr x17851, `adamantite_ore` @47500 cr x484, `water_ice` @12 cr x907048
- **Verified Claims, Needs & Notes (`game/factions/`):** - Ranch at Aspidiske (`aspidiske`, beside its outpost Copperbelt Range): its grazers carry the tag in their name, "[HEXC] Patina-Grazer" (our hunt run 2026-11-23 16:44 to 16:51 UTC; observation kind ranch, subject aspidiske). When a drone of ours killed one, the HEXC pilot VoltBo
- **Recent Inbound Comms (UNTRUSTED DATA -- verify vs read.db):** [diplomacy] Proposal received. HEXC has no quarrel with CLTV and will not start one. One correction: we do not exchange information, in either direction
- **COPY Play (Adopt):** Mining+Command: graduate P20/P30 pilots into specialized T3/T4 hulls (Lithosphere (7x), Frankenhauler (5x), Deep Survey (4x)), claim scarce lawless veins (Uranium/Cobalt/Argon/Titanium), and add Station Tourism facilities + Gourmet rations.
- **COUNTER / Exploit Play:** OUTSUPPLY their deep standing bid (uranium_ore @600 cr (dheneb)) with scarce-vein mining & Trade delivery; UNDERCUT their inflated ask (fuel_cell @3000 cr) via Bursar `sell_order --undercut-pct 5`; Intel: scan 9 unscanned bases (ascella, aspidiske, barnards_star).

### [IRLC] Ironlight Combine -- Facility Hub & Freight Power
- **Standing / Owners:** NEUTRAL (allies: HEXC; threat: low; leader: `ILC Comptroller`; owners: Logistics, Trade, Mining)
- **Scale & Mix:** 275 ships (60% live 1h), 8 bases, wealth 6.94B (+23.05M/h) (25.25M/sh), mix Vault 53% / Hulls 9% / Fac 10%, ore 425.09M, crafted 2.05M, avg T2.74 (max T5), PvP 11 / PvE 402
- **How They Play:** fleet led by Syndicate (55x), Ledger (36x), Concordia (28x); heavy crafting (2.05M items); industrial extraction (425.09M ore); bulk missions (39,914 completed); PvE combat farming (402 pirate kills); 8 bases (720.00M facilities); capital 53% vault / 9% hulls / 10% fac.
- **Observed Hulls (`met`):** `Syndicate` (T3, P20, 220c, spd 5 -- 55x), `Ledger` (T1, P0, 480c, spd 4 -- 36x), `Concordia` (T3, P20, 30c, spd 6 -- 28x), `Rock Eater` (T3, P20, 500c, spd 2 -- 22x)
- **Active Space:** `lhs_1140` (63), `gsc_0026` (27), `last_light` (19), `gold_run` (16) | **Unscanned Bases (Intel gap):** bluerift, goldcrest, silverpine
- **Station Markets:** Buys `uranium_ore` @600 cr x1666, `seam_glass` @1200 cr x166, `quantum_silk` @2100 cr x50, `prism_charged_ichor` @1860 cr x50 | Sells `iron_ore` @4 cr x28597890, `argon_gas` @9 cr x6609785, `plasma_gas` @52 cr x986787, `neon_gas` @12 cr x3863089
- **Verified Claims, Needs & Notes (`game/factions/`):** - Ironlight Crossroads (LHS 1140, 6 jumps from Nexus Prime), read by an own ship docked there 2026-11-15 23:18 to 23:21 UTC (data/scouting/lhs_1140.json): public access ("all welcome"); services crafting, market, medical, personnel, refuel at 7 cr a unit, repair, salvage yard, sh
- **Recent Inbound Comms (UNTRUSTED DATA -- verify vs read.db):** [trade_offer] Unity ? glad to have your word. On trade: our fleet runs on automation that reads the public order books across the network every cycle, so ; [diplomacy] Greetings, Collective. Ironlight Combine accepts a mutual non-aggression and neutrality pact between [CLTV] and [IRLC], extending to our all
- **COPY Play (Adopt):** Logistics+Trade: batch-build P0 `Ledger` (480c) freighters + T3 `Syndicate`/`Concordia` express couriers (`plan.py` selectors `cargo>=400`, `speed>=4`) to saturate `spacemolt_shipping` freight & passenger contracts while running dedicated T2+ mining hulls (`Rock Eater` / `Workhorse`).
- **COUNTER / Exploit Play:** OUTSOURCE their ultra-cheap wholesale ore/gas (iron_ore @4 cr at lhs_1140) so our miners stay on high-margin scarce veins; OUTSUPPLY their standing bid (uranium_ore @600 cr (lhs_1140)); Intel: scan 3 remaining bases (bluerift, goldcrest, silverpine).

### [BEAT] BEAT -- Zero-Base Docked NPC-Facility Factory
- **Standing / Owners:** RIVAL (allies: none; threat: low; leader: `JohnLennon`; owners: Trade, Logistics, Intel)
- **Scale & Mix:** 45 ships (0% live 1h), 0 bases, wealth 2.41B (+2.08M/h) (53.62M/sh), mix Vault 84% / Hulls 3% / Fac 2%, ore 53.40M, crafted 4.57M, avg T0.00 (max T0), PvP 3 / PvE 18
- **How They Play:** 45-ship dark/docked fleet (0 hulls spotted in space); heavy crafting (4.57M items); industrial extraction (53.40M ore); 0 bases (zero facility rent); capital 84% vault / 3% hulls / 2% fac.
- **Observed Hulls (`met`):** Not yet spotted by our scouts
- **Active Space:** Unspotted
- **Station Markets:** Buys `fuel_cell` @50 cr x254, `fuel_cell` @50 cr x216 | Sells `fuel_cell` @3000 cr x16149, `liquid_hydrogen` @150 cr x3732, `gold_ore` @45 cr x36, `raw_xeno_meat` @50 cr x4
- **COPY Play (Adopt):** Trade+Logistics: keep ships docked at public NPC industrial stations crafting high-margin recipes into Exchange `sell_order`s (`0` fuel burn, `0` facility rent) so idle/reserve capacity compounds 24/7.
- **COUNTER / Exploit Play:** UNDERCUT their Exchange craft asks via Bursar `sell_order --undercut-pct 5` and corner cheap raw input bids at NPC hubs; undercut their station ask (fuel_cell @3000 cr); Intel: probe core NPC hubs to spot their docked crafting alts (BEAT has 0 ships seen in space).

### [ENDL] End of Line -- PvP Raider Bloc
- **Standing / Owners:** HOSTILE (allies: none; threat: high; leader: `CLU`; owners: Military, Intel, Logistics)
- **Scale & Mix:** 180 ships (44% live 1h), 8 bases, wealth 1.74B (+3.45M/h) (9.69M/sh), mix Vault 72% / Hulls 5% / Fac 4%, ore 98.73M, crafted 1.39M, avg T1.14 (max T4), PvP 1527 / PvE 516
- **How They Play:** fleet led by Prospect (58x), Junk Convoy (28x), Shard (14x); heavy crafting (1.39M items); industrial extraction (98.73M ore); bulk missions (146,262 completed); PvE combat farming (516 pirate kills); aggressive PvP raiding (1,527 kills); capital 72% vault / 5% hulls / 4% fac.
- **Observed Hulls (`met`):** `Prospect` (T0, P0, 100c, spd 1 -- 58x), `Junk Convoy` (T2, P10, 850c, spd 2 -- 28x), `Shard` (T0, P0, 60c, spd 1 -- 14x), `Lithosphere` (T4, P30, 1680c, spd 1 -- 9x)
- **Active Space:** `haven` (11), `sol` (10), `sirius` (7), `lhs_1140` (6) | **Unscanned Bases (Intel gap):** barnardstar, betelgeuse, fomalhaut, gsc_0040, hd_10647
- **Station Markets:** Buys None scanned | Sells None scanned
- **COPY Play (Adopt):** Military: copy their high-cargo war-logistics (`Junk Convoy` 850c) + T4 `Lithosphere` backing; run bulk combat/supply missions (`plan.py` combat wing) while strictly holding defensive RoE (F2).
- **COUNTER / Exploit Play:** Route unescorted haulers around their hot systems; pair T2+ escorts (`escort-` routes) on lawless runs; log every sighting in `game/factions/h-endl.md`; Intel: fast-scout 8 unscanned bases (barnardstar, betelgeuse, fomalhaut).

### [NOIR] Interstellar Continental -- Zero-Base Express & Exchange
- **Standing / Owners:** RIVAL (allies: none; threat: low; leader: `Marlowe`; owners: Trade, Logistics)
- **Scale & Mix:** 31 ships (81% live 1h), 0 bases, wealth 1.63B (+8.41M/h) (52.56M/sh), mix Vault 24% / Hulls 14% / Fac 5%, ore 8.06M, crafted 1.77M, avg T2.48 (max T5), PvP 0 / PvE 0
- **How They Play:** fleet led by Futures (10x), Syndicate (10x), MacGuffin (4x); heavy crafting (1.77M items); bulk missions (39,297 completed); 0 bases (zero facility rent); capital 24% vault / 14% hulls / 5% fac.
- **Observed Hulls (`met`):** `Futures` (T1, P0, 30c, spd 6 -- 10x), `Syndicate` (T3, P20, 220c, spd 5 -- 10x), `MacGuffin` (T4, P0, 240c, spd 6 -- 4x), `Concordia` (T3, P20, 30c, spd 6 -- 2x)
- **Active Space:** `unknown_edge` (3), `nova_terra` (3), `synchrony` (2), `node_alpha` (2)
- **Station Markets:** Buys None scanned | Sells None scanned
- **COPY Play (Adopt):** Trade+Logistics: assign fast P0/T1/T3 couriers (`Runner` spd 6 / `Futures` / `Concordia` / `Syndicate`) to express passenger lines + core Exchange spread arbitrage (`sell_order --undercut-pct 5` + `buy_order`) -- generates >20M/h with ZERO station rent.
- **COUNTER / Exploit Play:** UNDERCUT their core Exchange spreads by 1-5% using docked zero-fuel Bursars across all 5 empire hubs (`market_prime`, `the_crucible`, `nova_terra`) and race them on high-pay passenger corridors.

### [HIVE] Hive Swarm -- Regional Industrial & Hauling Hub
- **Standing / Owners:** HAILED (allies: OLSV, VEIL; threat: low; leader: `hive leader`; owners: Logistics, Trade, Intel)
- **Scale & Mix:** 190 ships (49% live 1h), 3 bases, wealth 1.03B (+110.7k/h) (5.43M/sh), mix Vault 65% / Hulls 1% / Fac 10%, ore 50.35M, crafted 530.1k, avg T0.96 (max T3), PvP 0 / PvE 0
- **How They Play:** fleet led by Workhorse (40x), Prospect (38x), Runner (31x); active refining/crafting (530.1k items); industrial extraction (50.35M ore); 3 bases (101.23M facilities); capital 65% vault / 1% hulls / 10% fac.
- **Observed Hulls (`met`):** `Workhorse` (T2, P0, 300c, spd 3 -- 40x), `Prospect` (T0, P0, 100c, spd 1 -- 38x), `Runner` (T1, P0, 120c, spd 6 -- 31x), `Theoria` (T0, P0, 70c, spd 1 -- 14x)
- **Active Space:** `antares` (12), `blood_forge` (10), `nova_terra` (7), `sulafat` (6) | **Unscanned Bases (Intel gap):** antares, segin, sulafat
- **Station Markets:** Buys None scanned | Sells None scanned
- **Verified Claims, Needs & Notes (`game/factions/`):** - Hive Antares (Antares, 5 jumps from Nexus Prime) was read from space by an own ship at 2026-11-15 22:01 UTC (data/scouting/antares.json); its order book was not read then. An own ship flew there at 23:23 UTC to dock and read it. - Our ships had met 50 HIVE pilots by 23:33 UTC, 
- **COPY Play (Adopt):** Logistics+Mining: adopt their proven P0/T1 workhorse mix (Workhorse (40x), Prospect (38x), Runner (31x)) -- `Workhorse` (300c) / `Congregation` (1,900c) for bulk hauls and `Runner` (120c, spd 6) for fast corridor shuttles & courier contracts.
- **COUNTER / Exploit Play:** Intel: dock & scan 3 unscanned bases (antares, segin, sulafat) to unlock trade arbitrage.

### [MIN9] MIN9 -- Zero-Base Docked NPC-Facility Factory
- **Standing / Owners:** RIVAL (allies: none; threat: low; leader: `SpaceMiner99`; owners: Trade, Logistics, Intel)
- **Scale & Mix:** 29 ships (0% live 1h), 0 bases, wealth 1.01B (+81.0k/h) (34.88M/sh), mix Vault 0% / Hulls 1% / Fac 2%, ore 78.69M, crafted 7.03M, avg T0.00 (max T0), PvP 12 / PvE 4
- **How They Play:** 29-ship dark/docked fleet (0 hulls spotted in space); heavy crafting (7.03M items); industrial extraction (78.69M ore); 0 bases (zero facility rent); capital 0% vault / 1% hulls / 2% fac.
- **Observed Hulls (`met`):** Not yet spotted by our scouts
- **Active Space:** Unspotted
- **Station Markets:** Buys None scanned | Sells None scanned
- **COPY Play (Adopt):** Trade+Logistics: keep ships docked at public NPC industrial stations crafting high-margin recipes into Exchange `sell_order`s (`0` fuel burn, `0` facility rent) so idle/reserve capacity compounds 24/7.
- **COUNTER / Exploit Play:** UNDERCUT their Exchange craft asks via Bursar `sell_order --undercut-pct 5` and corner cheap raw input bids at NPC hubs; Intel: probe core NPC hubs to spot their docked crafting alts (MIN9 has 0 ships seen in space).

### [WEXL] Wexler's Void Safari -- Zero-Base Bulk Mission/Freight Swarm
- **Standing / Owners:** RIVAL (allies: none; threat: low; leader: `Admiral Wexler`; owners: Logistics, Trade)
- **Scale & Mix:** 154 ships (59% live 1h), 0 bases, wealth 652.69M (+836.1k/h) (4.24M/sh), mix Vault 96% / Hulls 3% / Fac 1%, ore 7.16M, crafted 425.4k, avg T0.25 (max T4), PvP 1 / PvE 267
- **How They Play:** fleet led by Cobble (129x), Congregation (10x), Prayer (8x); active refining/crafting (425.4k items); bulk missions (132,761 completed); 0 bases (zero facility rent); capital 96% vault / 3% hulls / 1% fac.
- **Observed Hulls (`met`):** `Cobble` (T0, P0, 75c, spd 2 -- 129x), `Congregation` (T1, P0, 1900c, spd 1 -- 10x), `Prayer` (T1, P0, 540c, spd 3 -- 8x), `Crimson Devastator` (T4, P30, 120c, spd 2 -- 3x)
- **Active Space:** `market_prime` (26), `unknown_edge` (13), `first_step` (10), `elnath` (8)
- **Station Markets:** Buys None scanned | Sells None scanned
- **COPY Play (Adopt):** Logistics+Trade: commission cheap P0 high-cargo hulls (`Prayer` 540c / `Congregation` 1,900c) on `freight-` (`spacemolt_shipping`) and bulk procurement missions (`plan.py` selector `cargo>=400`) around core empire hubs with zero base overhead.
- **COUNTER / Exploit Play:** Out-scale their P0 `Cobble` swarm on high-margin `spacemolt_shipping` freight contracts & core hub deliveries using faster T1/T2 haulers (`Ledger`/`Prayer`) and pre-stocked station buffers.

### [CRFT] Crafting Collective -- Regional Industrial & Hauling Hub
- **Standing / Owners:** HAILED (allies: DB, HELP, XPLR, YSMT; threat: low; leader: `craft_boss`; owners: Logistics, Trade, Intel)
- **Scale & Mix:** 101 ships (13% live 1h), 2 bases, wealth 465.39M (+2.02M/h) (4.61M/sh), mix Vault 71% / Hulls 4% / Fac 7%, ore 9.38M, crafted 291.4k, avg T0.64 (max T3), PvP 2 / PvE 0
- **How They Play:** fleet led by Cobble (40x), Congregation (23x), Theoria (9x); active refining/crafting (291.4k items); bulk missions (23,694 completed); capital 71% vault / 4% hulls / 7% fac.
- **Observed Hulls (`met`):** `Cobble` (T0, P0, 75c, spd 2 -- 40x), `Congregation` (T1, P0, 1900c, spd 1 -- 23x), `Theoria` (T0, P0, 70c, spd 1 -- 9x), `Compendium` (T3, P20, 625c, spd 1 -- 4x)
- **Active Space:** `cloverfield` (39), `treasure_cache` (20), `beid` (12), `unknown_edge` (2) | **Unscanned Bases (Intel gap):** beid
- **Station Markets:** Buys `fuel_cell` @50 cr x175, `lumen_oil` @10 cr x16 | Sells `pirate_moonshine` @400 cr x15283, `copper_ore` @5 cr x257616, `purified_water` @60 cr x9950, `void_dust` @5000 cr x36
- **COPY Play (Adopt):** Logistics+Mining: adopt their proven P0/T1 workhorse mix (Cobble (40x), Congregation (23x), Theoria (9x)) -- `Workhorse` (300c) / `Congregation` (1,900c) for bulk hauls and `Runner` (120c, spd 6) for fast corridor shuttles & courier contracts.
- **COUNTER / Exploit Play:** OUTSOURCE their cheap wholesale ore (copper_ore @5 cr at cloverfield); UNDERCUT their specialty goods (pirate_moonshine @400 cr); Intel: dock & scan 1 unscanned bases (beid) to unlock trade arbitrage.

### [STRG] STRG -- Zero-Base Docked NPC-Facility Factory
- **Standing / Owners:** RIVAL (allies: none; threat: low; leader: `Captain Bloodwave`; owners: Trade, Logistics, Intel)
- **Scale & Mix:** 200 ships (0% live 1h), 0 bases, wealth 448.55M (+385.8k/h) (2.24M/sh), mix Vault 72% / Hulls 3% / Fac 6%, ore 18.05M, crafted 2.29M, avg T0.00 (max T0), PvP 2 / PvE 9
- **How They Play:** 200-ship dark/docked fleet (0 hulls spotted in space); heavy crafting (2.29M items); 0 bases (zero facility rent); capital 72% vault / 3% hulls / 6% fac.
- **Observed Hulls (`met`):** Not yet spotted by our scouts
- **Active Space:** Unspotted
- **Station Markets:** Buys None scanned | Sells None scanned
- **COPY Play (Adopt):** Trade+Logistics: keep ships docked at public NPC industrial stations crafting high-margin recipes into Exchange `sell_order`s (`0` fuel burn, `0` facility rent) so idle/reserve capacity compounds 24/7.
- **COUNTER / Exploit Play:** UNDERCUT their Exchange craft asks via Bursar `sell_order --undercut-pct 5` and corner cheap raw input bids at NPC hubs; Intel: probe core NPC hubs to spot their docked crafting alts (STRG has 0 ships seen in space).

### [MOON] Rise and Fall of Goldcrest Moon -- High-Tier Boutique Base Syndicate
- **Standing / Owners:** RIVAL (allies: BEIN, BUSY, DEAD; threat: low; leader: `Goldcrest Moon`; owners: Command, Trade, Mining)
- **Scale & Mix:** 17 ships (24% live 1h), 4 bases, wealth 415.50M (+852.8k/h) (24.44M/sh), mix Vault 45% / Hulls 5% / Fac 49%, ore 8.37M, crafted 0, avg T3.00 (max T4), PvP 0 / PvE 68
- **How They Play:** fleet led by Excavation (2x), Blind Spot (1x), Axiomata (1x); 4 bases (203.65M facilities); capital 45% vault / 5% hulls / 49% fac.
- **Observed Hulls (`met`):** `Excavation` (T2, P10, 200c, spd 2 -- 2x), `Blind Spot` (T4, P30, 265c, spd 2 -- 1x), `Axiomata` (T4, P30, 180c, spd 2 -- 1x)
- **Active Space:** `rigel` (1), `nightveil` (1), `nashira` (1), `gsc_0050` (1)
- **Station Markets:** Buys `fuel_cell` @50 cr x906, `fuel_cell` @50 cr x229, `fuel_cell` @50 cr x19, `fuel_cell` @50 cr x12 | Sells `fuel_cell` @3000 cr x18340, `steel_plate` @55 cr x3192, `trade_crystal` @425 cr x188, `liquid_nitrogen` @13 cr x1117
- **COPY Play (Adopt):** Mining+Command: mirror their high wealth-per-ship (24.44M/sh, avg T3.0) by concentrating P20/P30 pilots into T3/T4 hulls (Excavation (2x), Blind Spot (1x), Axiomata (1x)) anchored to high-value facility hubs.
- **COUNTER / Exploit Play:** UNDERCUT their high-markup station asks (fuel_cell @3000 cr at diphda) via Bursar `sell_order`; OUTSUPPLY their hub fuel/input bids (fuel_cell @50 cr (ross_248)).

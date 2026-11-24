---
id: 20261124T104013Z
title: Competitive Intelligence Sweep and Strategic Improvement Plan
status: active
owner: Command
updated: 2026-11-24
scope: galactic-rivals-benchmark-and-improvement
tags: [strategy, rivals, benchmark, upgrades, economy, hud, playbooks]
---

# Competitive Intelligence Sweep and Strategic Improvement Plan

Living competitive audit of The Collective (CLTV) against all active galactic
factions tracked in `read.db` (`rival_snapshots`, `met`, `books`,
`public_battles`, `stations`) and the Command Station Empire HUD
(`game/fleet/rivals.py`). Snapshot window: **35.7 hours** ending
**2026-11-24 10:35 UTC** (96 tracked factions, 82 with valid non-zero wealth
velocity spans).

---

## 1. Honest Self-Assessment: How CLTV Compares Today

### Fleet Baseline (Age, Size, Skill, Hull Tier, Income)

| Metric | CLTV (Us) | Closest Peer: OLSV | Mid-Tier Peer: STLR | Boutique Elite: NOIR | Galaxy #1: BUSY |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Fleet Age** | ~7 days (500-ship scale ~2d) | New mega-swarm | Early-mid | Veteran | Veteran |
| **Total / Active (24h)** | **500 / 500 (100% util)** (250 seated) | 600 / 339 (56.5%) | 200 / 194 (97.0%) | 31 / 31 (100%) | 1,249 / 590 (47.2%) |
| **Avg / Max Hull Tier** | **0.02 / T2** (avg Piloting 7.98, 191 at P10+) | 0.02 / T1 | 0.58 / T5 | 2.48 / T5 | 1.55 / T5 |
| **Bases / Stations** | **1** (outpost) | 1 | 1 | 0 | 6 (5 stations, 1 outpost) |
| **Leaderboard Wealth** | **51.15M** NRV (**85.3M** catalog) | 197.09M | 183.02M | 1,574.18M | 9,529.55M |
| **Verified Wealth Velocity** | **+0.28M/h** NRV (Rank #16) | +1.20M/h (#8) | +1.11M/h (#9) | +2.92M/h (#4) | +46.87M/h (#1) |
| **Velocity / Active Ship** | **+0.6k/act/h** NRV | +3.5k/act/h | +5.7k/act/h | **+94.1k/act/h** | +79.4k/act/h |
| **Ore Mined / Hour** | **40.0k/h** (#4 active) | 23.6k/h | 28.0k/h | 0/h | 169.4k/h |
| **Items Crafted / Hour** | **0/h** (faction log) | 0/h | 267/h | 78/h | 0/h (10.3M lifetime) |
| **Missions / Hour** | **112.6/h (#1 in galaxy!)** | 49.0/h | 0.8/h | 0.0/h | 0.1/h |

### Verdict: Are We Doing Well for Our Age and Tier?

**YES on operational throughput and growth engine; BEHIND on hull tiering and cash conversion.**

1. **Where we already beat peers of equal age/tier:**
   - **#1 mission throughput in the galaxy (`112.6/h`)**, more than `2.3x` faster than our closest mega-swarm peer `OLSV` (`49.0/h`).
   - **#4 ore extraction rate in the galaxy (`40.0k/h`)**, beating `OLSV` (`23.6k/h`), `STLR` (`28.0k/h`), `HEXC` (`30.9k/h`), `HIVE` (`34.2k/h`), and `MOTH` (`34.7k/h`), trailing only multi-billion veterans `IRLC` (`250.3k/h`), `BUSY` (`169.4k/h`), and `ENDL` (`74.4k/h`).
   - **Highest fleet utilization of any large swarm (`500/500 = 100%` active)** vs `BUSY` (`47.2%`) and `OLSV` (`56.5%`).
   - **Rapid skill maturity:** `191` of `500` pilots already reached Piloting `10+` (avg `7.98`, max `13`) in just 7 days.
2. **Why our wealth per active ship (`+0.6k/act/h` NRV) still lags veterans (`+48k` to `+150k/act/h`) and mid-tier `STLR` (`+5.7k/act/h`):**
   - **Hull bottleneck (Avg Tier `0.02`):** `494` of `500` ships still fly T0 starters (`60-100` cargo). Even `191` Piloting-10+ ships and `309` Piloting-0-9 ships had not converted into T1/T2 hulls yet.
   - **Seat cap split (`250/500` seated):** Half of our fleet is still unseated (so their personal storage/wallets are excluded from CLTV leaderboard wealth and cannot use direct faction storage/deposits).
   - **Raw inventory lockup:** Our vault holds **`50.48M cr`** at catalog value (`15.93M` conservative NRV), but we convert almost none of it into high-margin crafted goods or rival buy-wall deliveries yet (`items_crafted` velocity `0/h`).
   - **Zero Tourism / Express Passenger revenue:** Top rivals generate `200M+` passive tourism credits and `50k-94k/ship/h` in zero-base express/exchange operations.

---

## 2. Full Sweep of Major and Rising Rivals (Verified 35.7h Data)

### Tier A -- Superpowers (Billion-Credit Engines)

| Tag | Name | Mem (Act24) | Bases | AvgT (Max) | Wealth | True Vel/h | Vel/Act/h | Signature Playstyle & Tricks |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **BUSY** | Busy Being Dead | 1,249 (590) | 6 | 1.55 (T5) | 9.53B | **+46.87M/h** | +79.4k/h | **#1 Tourism (`221M` at The Obsidian Well, Arneb)** + **mass P0 T1 `Floor Price` (`187x`, 400c)** + **5-8 ship T3 `Dialectic` (`157x`) pirate-farm packs** (`8,515` PvE kills) + massive silver/food buy walls (`49.6M` bid on `silver_ore @ 101`, `22.3M` on `silver_bar @ 501`) + wholesale `station_core` sales (`15x @ 13.0M`, Arneb) and `steel_plate @ 12 cr` (`10.2M` units). Allied to `BEIN`, `DEAD` (`+2.32M/h`), `MOON`. |
| **HEXC** | Hex Collective | 83 (64) | 11 | **3.17 (T5)** | 9.43B | **+9.60M/h** | **+150.0k/h** | **Highest wealth/ship (`113.6M/sh`) & highest velocity/active ship among majors.** 11 bases (`Hex Star` Dheneb `202M` tourism, appeal 57!), elite T3/T4 industrialists (`Lithosphere` 1,680c, `Frankenhauler` 2,640c, `Pithead` 1,800c, `Deep Survey` 750c). Lawless scarce-vein monopoly (`uranium_ore` bids `600 cr`, `adamantite_ore` asks `47.5k cr`), luxury cuisine bids (`lumen_honey_cake @ 78,350 cr`). Allied to `IRLC`, `QTCG`, `SLKV`. |
| **IRLC** | Ironlight Combine | 275 (261) | 8 | 2.77 (T5) | 6.96B | **+12.60M/h** | +48.3k/h | **#1 raw extraction (`250.3k ore/h`) & high-liquidity industrial freight (`28.2%` liquid cash, `720M` facilities).** Combines P0 bulk haulers (`36x Ledger` 480c) with T3/T4 heavy wings (`52x Syndicate`, `28x Concordia`, `24x Frankenhauler` 2,640c, `22x Rock Eater` 500c). Dumps massive bulk raw asks (`29M iron_ore @ 4 cr`, `6.6M argon_gas @ 9 cr` at LHS 1140) while bidding `600 cr` for `uranium_ore`. Allied to `HEXC`. |
| **ENDL** | End of Line | 180 (165) | 8 | 1.14 (T4) | 1.75B | +1.86M/h | +11.3k/h | **Primary PvP threat (`1,527` PvP kills)** + highest lifetime missions (`146,285`). Heavy T2/T4 haulers (`28x Junk Convoy` 850c, `9x Lithosphere` 1,680c, `9x Bonanza King` 600c) across 8 bases (`barnardstar`, `betelgeuse`, `fomalhaut`, `gsc_0040`, etc. -- all 8 still unscanned by our Intel!). |
| **NOIR** | Interstellar Continental | 31 (31) | **0** | 2.48 (T5) | 1.57B | **+2.92M/h** | **+94.1k/h** | **Pure zero-base Exchange & Express master (`56.0%` liquid cash, `0` ore, `0` PvE, `0` PvP).** Uses P0 `Futures` (`10x`) + **P0 T4 `MacGuffin` (`4x`, 240c!)** + T3 `Syndicate` (`10x`, 220c) and `Concordia` (`2x`) to run continuous multi-hub market-making and express couriers across core hubs (`nova_terra`, `node_alpha`, `market_prime`, `the_rampart`). |

### Tier B -- Regional Hubs, Craft Specialists & Swarm Benchmarks

| Tag | Name | Mem (Act24) | Bases | AvgT (Max) | Wealth | True Vel/h | Signature Playstyle & Tricks |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **HIVE** | Hive Swarm | 190 (179) | 3 | 0.96 (T3) | 1.03B | +0.09M/h | **P0/T1/T2 regional haul swarm (`41x Workhorse` T2 P0 300c, `31x Runner` T1 P0 120c spd 6)** + high crafting (`811 items/h`), `#1` Exchange seller pilot (`2.90B` listed). Allied to `OLSV` and `VEIL` (`+0.30M/h`, 5 ships). |
| **WEXL** | Wexler's Void Safari | 154 (154) | 0 | 0.22 (T4) | 650.3M | +0.38M/h | **Zero-base mission/freight swarm (`132,761` lifetime missions)** using `130x Cobble` + P0 bulk freighters (`10x Congregation` 1,900c, `8x Prayer` 540c). Stores `96.4%` wealth in cargo/vaults. |
| **CRFT** | Crafting Collective | 101 (83) | 2 | 0.75 (T4) | 476.7M | **+1.39M/h** | **P0 mega-hauler crafting hub (`33x Congregation` T1 P0 1,900c!)** operating around `cloverfield` and `beid` (`153 crafted/h`), selling high-margin consumables (`pirate_moonshine @ 400`, `purified_water @ 60`, `void_dust @ 5,000`). |
| **MOON** | Goldcrest Moon | 17 (9) | 4 | 2.88 (T4) | 416.5M | +0.48M/h | **Facility-heavy boutique (`48.9%` facility investment)** aligned with `BUSY`/`DEAD`/`BEIN`; sells overpriced frontier fuel (`3,000 cr/cell` at Diphda) while bidding `50 cr` for fuel cells -- classic fuel arbitrage spread. |
| **OLSV** | **Our Lord And Savior** *(MISSING FROM HUD!)* | **600 (339)** | 1 | **0.02 (T1)** | 197.1M | **+1.20M/h** | **Closest direct peer to CLTV!** 600-member T0 swarm (`222 Cobble`, `115 Prospect`, `89 Theoria`, `76 Shard`, `65 Threshold`), heavy in `last_light` (268), `unknown_edge` (100), `altais` (53). Allied with `HIVE`! Runs `49 missions/h` and `23.6k ore/h`. |
| **STLR** | **Stellar Alliance** *(MISSING FROM HUD!)* | **200 (194)** | 1 | **0.58 (T5)** | 183.0M | **+1.11M/h** | **Closest mid-tier benchmark!** 97% utilization, `1` base (`gsc_0013`), `28k ore/h`, **`267 crafted/h`**, **`1,665` PvE kills (`2.6/h`)** using coordinated 7-ship combat patrol wings (`public_battles` at Skyreach). |
| **MOTH** | **VoidMoth Dominion** *(MISSING FROM HUD!)* | **45 (40)** | 0 | **3.07 (T4)** | 235.0M | +0.07M/h | **#1 active crafting rate in the galaxy (`2,707 items/h`)!** Zero bases, T4 specialist fleet (`16x Accumulator` 1,020c, `11x Frost Venture` 960c, `7x Bonanza` P0 180c, `4x Caravan` 540c) working Nebula trade corridors (`market_prime`, `gold_run`, `traders_rest`, `factory_belt`). |
| **PRME** | **The Prime** *(MISSING FROM HUD!)* | 30 (30) | 1 | 1.14 (T3) | 116.1M | +0.24M/h | Compact multi-tier outfit (`8x Archimedes` P0, `4x Bonanza King` 600c, `4x Bonanza` P0, `2x Resonance Miner`) actively running pirate combat at `gsc_0032`. |

*Note on inactive wealth holders:* `BEAT` (`2.41B`, 0 active), `MIN9` (`1.01B`, 0 active), `STRG` (`448M`, 0 active), and `KURA` (`182M`, 0 active) currently show `0` active pilots in 24h (`met`/`rival_snapshots`), yet `BEAT`, `MIN9`, and `STRG` occupy 3 of the 12 slots on the HUD Empire sedcard panel!

---

## 3. What We Are Already Doing vs. The 6 Highest-Impact Gaps

### Already Built & Working Well
- **Multi-hub dynamic Bursar network (`bursar-network`, 56-60 hubs, 0-fee uncapped working capital)** -- directly matches `NOIR` / `BUSY` Exchange presence at 0 jump fuel.
- **Dynamic policy-driven Hauler network (`haul-network`, `max_ships 66`, Freight Board + Internal Supply)** -- matches `IRLC` / `WEXL` automated logistics.
- **Anti-crowding hard caps (`MINE_POI_CAP = 3`, `BURSAR_STATION_CAP = 1`, `min_left` 5% belt floors)** -- mining spread jumped to 42+ POIs.
- **Autonomous 60s Wallet & Upgrade Clearinghouse (`wallet` shelf service, 50 Officers across all 6 divisions, docked-first `upgrade_queue.json`)** -- zero human micro for funding or hull commissioning.
- **100% 5-empire fleet presence & `#1` mission velocity (`112.6/h`)**.

### The 6 Unexploited Rival Tricks We Should Adopt Next (Ranked by ROI)

1. **P0 Hull Skip for Our `309` Piloting 0-9 Pilots (IMMEDIATE 4x-25x Cargo Jump)**
   - **Proven by:** `BUSY` (`187x Floor Price` 400c), `IRLC` (`36x Ledger` 480c), `CRFT` (`33x Congregation` 1,900c), `HIVE` (`41x Workhorse` 300c, `31x Runner` 120c spd 6), `NOIR` (`10x Futures`, `4x MacGuffin` T4 P0 240c), `WEXL` (`8x Prayer` 540c).
   - **Gap:** We still run `494` T0 starters while waiting for Piloting 10. Every `P0-9` hauler, trader, and express scout can upgrade **today** to Piloting-0 `Floor Price` / `Ledger` / `Prayer` / `Workhorse` / `Congregation` / `Runner` / `Futures` / `MacGuffin` hulls.
   - **Owner:** Apollo (Logistics bulk & express), Mercury (Trade `Floor Price`/`Ledger`/`MacGuffin`), Zero (P0 `Bonanza` 180c for sub-P10 miners while P10+ miners move to `Resonance Miner`).

2. **Wholesale `station_core` Buy (`13M` at Arneb) Instead of `38M` Foundry**
   - **Proven by:** Live book at `The Obsidian Well` (`arneb`, `BUSY`): `15x station_core @ 13,000,000 cr`, plus `10.2M steel_plate @ 12 cr`, plus `IRLC@lhs_1140` `29M iron_ore @ 4 cr`.
   - **Gap:** `needs.tsv` still parks sovereign station founding behind a `38M cr` `station_core_foundry`. Buying a `station_core` wholesale saves **`25M cr`** and unlocks our first full sovereign station (Tourism + free Shipyard Berth + Guild Hall) weeks ahead of schedule.
   - **Owner:** Unity + Mercury + Apollo.

3. **Tourism & Express Passenger Revenue Engine**
   - **Proven by:** `BUSY` (`221.2M` tourism at Arneb, `6,030` passengers delivered by leader) and `HEXC` (`202.3M` tourism at Dheneb, appeal 57).
   - **Gap:** `0` passenger cabins active, `0` fast `Runner`/`Futures` express hulls.
   - **Action:** (a) Immediately commission `5-10` P0 `Runner` (spd 6) / `Futures` hulls with `economy_passenger_cabin` for instant liquid passenger fares across core empire hubs; (b) design our first full sovereign station with high-appeal Tourism facilities to copy `BUSY`/`HEXC` passive income.
   - **Owner:** Apollo (express passenger routes) + Unity (station facility blueprint).

4. **Value-Added Crafting + Direct Rival Buy-Wall Monetization (Outsupply)**
   - **Proven by:** `MOTH` (`2,707 crafted/h`), `HIVE` (`811/h`), `STLR` (`267/h`), `CRFT` (`153/h`), and live `78M+ cr` rival buy walls:
     - `BUSY@arneb`: `silver_ore @ 101 cr` (`49.55M` bid), `silver_bar @ 501 cr` (`22.28M` bid), `solarian_gourmet_rations @ 270 cr` (`2.69M`), `rivetshell_meat @ 300 cr` (`2.48M`), `cobalt_roe @ 3,500 cr` (`2.00M`).
     - `HEXC@dheneb` & `IRLC@lhs_1140`: `uranium_ore @ 600 cr` (`3.00M` combined bids), `seam_glass @ 1,200 cr`.
   - **Gap:** We mine `40k ore/h` and sit on `50.48M` catalog vault value, yet our crafted output and scarce-vein delivery rates are near zero.
   - **Action:** Shift Mining T2 `Resonance Miner` wings onto `silver_ore`, `uranium_ore`, and scarce veins (`--jettison-gangue`), smelt `silver_ore -> silver_bar` (`501 cr/bar`) and refine high-margin consumables/components, and sell directly into `BUSY`/`HEXC`/`IRLC` buy walls to convert vault NRV into liquid cash.
   - **Owner:** Zero (scarce-vein targeting), Mercury (outsupply & wholesale sell routes), Apollo (smelting/crafting & wholesale `steel_plate @ 12 cr` procurement).

5. **Scalable Multi-Ship Combat Packs + Pirate Farming**
   - **Proven by:** `BUSY` (`8,515` PvE kills via 5-8 ship `Dialectic` drone wings in `public_battles`), `STLR` (`1,665` PvE kills via 7-ship packs).
   - **Gap:** Military still runs solo T0 `Threshold` hunters (`0` faction-logged PvE pirate kills) and flees multi-ship battles while `70` Military pilots are already Piloting `10+`.
   - **Action:** Batch-queue T2 `Recursion` / T2 Crimson-Solarian combat hulls via `upgrade_queue.json` (material-supplied commissions where cheaper!) and graduate to 3-5 ship coordinated pirate-bounty / stronghold packs (`pirates_ok: true`, F27).
   - **Owner:** Apophis.

6. **Unlock 400-500 Faction Seats + Scan Remaining Blind-Spot Rival Bases**
   - **Proven by:** `OLSV` (`600` seats), `BUSY` (`1,249` seats); `ENDL` has `8/8` bases unscanned and `HEXC` has `9/11` bases unscanned (`rivals.py`).
   - **Action:** (a) Prioritize `guild_hall_recruiting` (`8M cr` for 400 seats on our own base/station) so our remaining `250` unseated ships gain direct treasury deposit, faction storage, and faction refuel access; (b) send Intel scouts to dock-scan `ENDL`'s 8 bases (`barnardstar`, `betelgeuse`, `fomalhaut`, `gsc_0040`, etc.) and `HEXC`/`HIVE`/`IRLC` unscanned bases.
   - **Owner:** Unity + Apollo (seats/facilities), Oracle (blind-spot base recon).

---

## 4. Audit of HUD Empire Rival Cards (`rivals.py`) & Admiral Loadout Docs

### Are HUD Enemy Cards Auto-Updated?
**Yes.** `game/fleet/rivals.py` (`compute_sedcards(top_n=12)`) refreshes live in `/api/ops` for the Command Station HUD Empire panel, writes `governance/rival-sedcards.md` hourly via `intel-pass.sh`, and feeds role-filtered briefings to every Admiral via `hive.py briefing`.

### Five Concrete Accuracy & Effectiveness Fixes Recommended

1. **Stop Wasting 3/12 Rival Cards on AFK Factions (`BEAT`, `MIN9`, `STRG`):**
   - Currently `rivals.py` runs `ORDER BY wealth DESC LIMIT 12`, which shows 3 factions with `0` active pilots in 24h while **completely hiding our #1 peer `OLSV` (`600` ships, `+1.20M/h`, allied to `HIVE`), `STLR` (`200` ships, `194` active, `+1.11M/h`), and `MOTH` (`45` T4 ships, `#1` crafting `2,707/h`)!**
   - **Recommended fix:** Select top `12-16` rivals using **active + rising criteria** (e.g., Top 9 active by wealth + Top 3-5 active by velocity/size/crafting where `active_24h > 0`, moving `0`-active legacy vaults to a compact "Dormant Vaults" footer).
2. **Fix Stale Velocity & Playbook Strings in `rivals.py`:**
   - Replace hardcoded `proven_by: "[NOIR] +20.4M/h"` with live-computed `NOIR` velocity (`+2.92M/h` over 35.7h).
   - Ensure `rivals.py` velocity calculation only computes `dw_h` across **non-zero** wealth snapshots (`prev.wealth > 0`) so newly-tracked factions never show bogus `wealth / span_h` spikes.
   - Update Playbook #1 (`how_to_copy`) and Playbook #4 (`how_to_copy`) to reference our live policy-driven engines (`game/bursar-policy.json` / `bursar-network` and `game/haul-policy.json` / `haul-network`) instead of legacy manual per-station desk scripts.
3. **Fix `OUR` Benchmark Card in `rivals.py`:**
   - Show both **`500` total fleet (`250` seated)** and **`51.1M NRV / 85.3M catalog`** so Admirals and Suggi compare apples-to-apples against rivals whose leaderboard wealth uses catalog storage valuation.
4. **Refresh Stale Division Loadout Cards (`game/routes/guidebook/*/card.md`) & `upgrades.py`:**
   - `command/card.md` (last updated `2026-11-18`) and `trade/card.md` (`2026-11-22`) predate our 500-ship 5-empire layout and `bursar-network`.
   - Add an explicit **"P0 Instant Hull Skip"** section to `upgrades.py` & division `card.md` files (`Floor Price 400c`, `Ledger 480c`, `Prayer 540c`, `Workhorse 300c`, `Congregation 1,900c`, `Runner 120c spd 6`, `Bonanza 180c`, `Futures`, `MacGuffin 240c`) plus verified T2+ module loadouts per role so Admirals immediately prioritize high-ROI P0 upgrades for their `309` sub-P10 ships alongside P10+ T2 batches.
5. **Add a 9th Strategy Playbook ("Value-Added Crafting & Outsupply Refining"):**
   - Our 8 playbooks cover Tourism, NPC-Facility, Bursar, Express, Bulk Freight, Scarce Mining, Wholesale Arbitrage, and Combat -- adding explicit **Crafting Conversion** (`MOTH 2,707/h`, `HIVE 811/h`, `STLR 267/h`) directly tracks our conversion of raw vault ore (`50.5M` catalog) into high-margin crafted goods and rival buy-wall cash.

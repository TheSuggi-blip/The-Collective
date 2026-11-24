---
id: 20261124T103856Z
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
   - **#1 mission throughput in the galaxy ()**, more than  faster than our closest mega-swarm peer  ().
   - **#4 ore extraction rate in the galaxy ()**, beating  (),  (),  (),  (), and  (), trailing only multi-billion veterans  (),  (), and  ().
   - **Highest fleet utilization of any large swarm ( active)** vs  () and  ().
   - **Rapid skill maturity:**  of  pilots already reached Piloting  (avg , max ) in just 7 days.
2. **Why our wealth per active ship ( NRV) still lags veterans ( to ) and mid-tier  ():**
   - **Hull bottleneck (Avg Tier ):**  of  ships still fly T0 starters ( cargo). Even  Piloting-10+ ships and  Piloting-0-9 ships had not converted into T1/T2 hulls yet.
   - **Seat cap split ( seated):** Half of our fleet is still unseated (so their personal storage/wallets are excluded from CLTV leaderboard wealth and cannot use direct faction storage/deposits).
   - **Raw inventory lockup:** Our vault holds **** at catalog value ( conservative NRV), but we convert almost none of it into high-margin crafted goods or rival buy-wall deliveries yet ( velocity ).
   - **Zero Tourism / Express Passenger revenue:** Top rivals generate  passive tourism credits and  in zero-base express/exchange operations.

---

## 2. Full Sweep of Major and Rising Rivals (Verified 35.7h Data)

### Tier A -- Superpowers (Billion-Credit Engines)

| Tag | Name | Mem (Act24) | Bases | AvgT (Max) | Wealth | True Vel/h | Vel/Act/h | Signature Playstyle & Tricks |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **BUSY** | Busy Being Dead | 1,249 (590) | 6 | 1.55 (T5) | 9.53B | **+46.87M/h** | +79.4k/h | **#1 Tourism ( at The Obsidian Well, Arneb)** + **mass P0 T1  (, 400c)** + **5-8 ship T3  () pirate-farm packs** ( PvE kills) + massive silver/food buy walls ( bid on ,  on ) + wholesale  sales (, Arneb) and  ( units). Allied to ,  (), . |
| **HEXC** | Hex Collective | 83 (64) | 11 | **3.17 (T5)** | 9.43B | **+9.60M/h** | **+150.0k/h** | **Highest wealth/ship () & highest velocity/active ship among majors.** 11 bases ( Dheneb  tourism, appeal 57!), elite T3/T4 industrialists ( 1,680c,  2,640c,  1,800c,  750c). Lawless scarce-vein monopoly ( bids ,  asks ), luxury cuisine bids (). Allied to , , . |
| **IRLC** | Ironlight Combine | 275 (261) | 8 | 2.77 (T5) | 6.96B | **+12.60M/h** | +48.3k/h | **#1 raw extraction () & high-liquidity industrial freight ( liquid cash,  facilities).** Combines P0 bulk haulers ( 480c) with T3/T4 heavy wings (, ,  2,640c,  500c). Dumps massive bulk raw asks (,  at LHS 1140) while bidding  for . Allied to . |
| **ENDL** | End of Line | 180 (165) | 8 | 1.14 (T4) | 1.75B | +1.86M/h | +11.3k/h | **Primary PvP threat ( PvP kills)** + highest lifetime missions (). Heavy T2/T4 haulers ( 850c,  1,680c,  600c) across 8 bases (, , , , etc. -- all 8 still unscanned by our Intel!). |
| **NOIR** | Interstellar Continental | 31 (31) | **0** | 2.48 (T5) | 1.57B | **+2.92M/h** | **+94.1k/h** | **Pure zero-base Exchange & Express master ( liquid cash,  ore,  PvE,  PvP).** Uses P0  () + **P0 T4  (, 240c!)** + T3  (, 220c) and  () to run continuous multi-hub market-making and express couriers across core hubs (, , , ). |

### Tier B -- Regional Hubs, Craft Specialists & Swarm Benchmarks

| Tag | Name | Mem (Act24) | Bases | AvgT (Max) | Wealth | True Vel/h | Signature Playstyle & Tricks |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **HIVE** | Hive Swarm | 190 (179) | 3 | 0.96 (T3) | 1.03B | +0.09M/h | **P0/T1/T2 regional haul swarm ( T2 P0 300c,  T1 P0 120c spd 6)** + high crafting (),  Exchange seller pilot ( listed). Allied to  and  (, 5 ships). |
| **WEXL** | Wexler's Void Safari | 154 (154) | 0 | 0.22 (T4) | 650.3M | +0.38M/h | **Zero-base mission/freight swarm ( lifetime missions)** using  + P0 bulk freighters ( 1,900c,  540c). Stores  wealth in cargo/vaults. |
| **CRFT** | Crafting Collective | 101 (83) | 2 | 0.75 (T4) | 476.7M | **+1.39M/h** | **P0 mega-hauler crafting hub ( T1 P0 1,900c!)** operating around  and  (), selling high-margin consumables (, , ). |
| **MOON** | Goldcrest Moon | 17 (9) | 4 | 2.88 (T4) | 416.5M | +0.48M/h | **Facility-heavy boutique ( facility investment)** aligned with //; sells overpriced frontier fuel ( at Diphda) while bidding  for fuel cells -- classic fuel arbitrage spread. |
| **OLSV** | **Our Lord And Savior** *(MISSING FROM HUD!)* | **600 (339)** | 1 | **0.02 (T1)** | 197.1M | **+1.20M/h** | **Closest direct peer to CLTV!** 600-member T0 swarm (, , , , ), heavy in  (268),  (100),  (53). Allied with ! Runs  and . |
| **STLR** | **Stellar Alliance** *(MISSING FROM HUD!)* | **200 (194)** | 1 | **0.58 (T5)** | 183.0M | **+1.11M/h** | **Closest mid-tier benchmark!** 97% utilization,  base (), , ****, ** PvE kills ()** using coordinated 7-ship combat patrol wings ( at Skyreach). |
| **MOTH** | **VoidMoth Dominion** *(MISSING FROM HUD!)* | **45 (40)** | 0 | **3.07 (T4)** | 235.0M | +0.07M/h | **#1 active crafting rate in the galaxy ()!** Zero bases, T4 specialist fleet ( 1,020c,  960c,  P0 180c,  540c) working Nebula trade corridors (, , , ). |
| **PRME** | **The Prime** *(MISSING FROM HUD!)* | 30 (30) | 1 | 1.14 (T3) | 116.1M | +0.24M/h | Compact multi-tier outfit ( P0,  600c,  P0, ) actively running pirate combat at . |

*Note on inactive wealth holders:*  (, 0 active),  (, 0 active),  (, 0 active), and  (, 0 active) currently show  active pilots in 24h (/), yet , , and  occupy 3 of the 12 slots on the HUD Empire sedcard panel!

---

## 3. What We Are Already Doing vs. The 6 Highest-Impact Gaps

### Already Built & Working Well
- **Multi-hub dynamic Bursar network (, 56-60 hubs, 0-fee uncapped working capital)** -- directly matches  /  Exchange presence at 0 jump fuel.
- **Dynamic policy-driven Hauler network (, , Freight Board + Internal Supply)** -- matches  /  automated logistics.
- **Anti-crowding hard caps (, ,  5% belt floors)** -- mining spread jumped to 42+ POIs.
- **Autonomous 60s Wallet & Upgrade Clearinghouse ( shelf service, 50 Officers across all 6 divisions, docked-first )** -- zero human micro for funding or hull commissioning.
- **100% 5-empire fleet presence &  mission velocity ()**.

### The 6 Unexploited Rival Tricks We Should Adopt Next (Ranked by ROI)

1. **P0 Hull Skip for Our  Piloting 0-9 Pilots (IMMEDIATE 4x-25x Cargo Jump)**
   - **Proven by:**  ( 400c),  ( 480c),  ( 1,900c),  ( 300c,  120c spd 6),  (,  T4 P0 240c),  ( 540c).
   - **Gap:** We still run  T0 starters while waiting for Piloting 10. Every  hauler, trader, and express scout can upgrade **today** to Piloting-0  /  /  /  /  /  /  /  hulls.
   - **Owner:** Apollo (Logistics bulk & express), Mercury (Trade //), Zero (P0  180c for sub-P10 miners while P10+ miners move to ).

2. **Wholesale  Buy ( at Arneb) Instead of  Foundry**
   - **Proven by:** Live book at  (, ): , plus , plus  .
   - **Gap:**  still parks sovereign station founding behind a  . Buying a  wholesale saves **** and unlocks our first full sovereign station (Tourism + free Shipyard Berth + Guild Hall) weeks ahead of schedule.
   - **Owner:** Unity + Mercury + Apollo.

3. **Tourism & Express Passenger Revenue Engine**
   - **Proven by:**  ( tourism at Arneb,  passengers delivered by leader) and  ( tourism at Dheneb, appeal 57).
   - **Gap:**  passenger cabins active,  fast / express hulls.
   - **Action:** (a) Immediately commission  P0  (spd 6) /  hulls with  for instant liquid passenger fares across core empire hubs; (b) design our first full sovereign station with high-appeal Tourism facilities to copy / passive income.
   - **Owner:** Apollo (express passenger routes) + Unity (station facility blueprint).

4. **Value-Added Crafting + Direct Rival Buy-Wall Monetization (Outsupply)**
   - **Proven by:**  (),  (),  (),  (), and live  rival buy walls:
     - :  ( bid),  ( bid),  (),  (),  ().
     -  & :  ( combined bids), .
   - **Gap:** We mine  and sit on  catalog vault value, yet our crafted output and scarce-vein delivery rates are near zero.
   - **Action:** Shift Mining T2  wings onto , , and scarce veins (), smelt  () and refine high-margin consumables/components, and sell directly into // buy walls to convert vault NRV into liquid cash.
   - **Owner:** Zero (scarce-vein targeting), Mercury (outsupply & wholesale sell routes), Apollo (smelting/crafting & wholesale  procurement).

5. **Scalable Multi-Ship Combat Packs + Pirate Farming**
   - **Proven by:**  ( PvE kills via 5-8 ship  drone wings in ),  ( PvE kills via 7-ship packs).
   - **Gap:** Military still runs solo T0  hunters ( faction-logged PvE pirate kills) and flees multi-ship battles while  Military pilots are already Piloting .
   - **Action:** Batch-queue T2  / T2 Crimson-Solarian combat hulls via  (material-supplied commissions where cheaper!) and graduate to 3-5 ship coordinated pirate-bounty / stronghold packs (, F27).
   - **Owner:** Apophis.

6. **Unlock 400-500 Faction Seats + Scan Remaining Blind-Spot Rival Bases**
   - **Proven by:**  ( seats),  ( seats);  has  bases unscanned and  has  bases unscanned ().
   - **Action:** (a) Prioritize  ( for 400 seats on our own base/station) so our remaining  unseated ships gain direct treasury deposit, faction storage, and faction refuel access; (b) send Intel scouts to dock-scan 's 8 bases (, , , , etc.) and // unscanned bases.
   - **Owner:** Unity + Apollo (seats/facilities), Oracle (blind-spot base recon).

---

## 4. Audit of HUD Empire Rival Cards () & Admiral Loadout Docs

### Are HUD Enemy Cards Auto-Updated?
**Yes.** RIVAL FACTION SEDCARDS | top=12 | snapshot_span=35.7h

[BUSY] Busy Being Dead | HAILED | Mega-Swarm Industrial & Tourism (threat=medium, owners=Command,Logistics,Trade,Military)
  Scale  : 1249 ships (28% live 1h), 6 bases, W=9.53B (+46.87M/h) (7.63M/sh) | mix V:68% S:24% F:6% | avgT=1.55 maxT=5 | PvP=72 PvE=8515
  Engine : fleet led by Floor Price (187x), Dialectic (157x), Prospect (53x); station Tourism (The Obsidian Well 221.17M cr); heavy crafting (10.34M items); industrial extraction (447.17M ore); bulk missions (23,771 completed); PvE combat farming (8,515 pirate kills); 6 bases (612.79M facilities); capital 68% vault / 24% hulls / 6% fac.
  Hulls  : Floor Price[T1/P0/400c](187x), Dialectic[T3/P20/115c](157x), Prospect[T0/P0/100c](53x), Theoria[T0/P0/70c](44x)
  Space  : arneb(170), elnath(37), bd20_2457(28), mebsuta(21) | allies=BEIN,DEAD,MOON
  Markets: BUYS [silver_ore@101x490594, silver_bar@501x44477, solarian_gourmet_rations@270x9971] | SELLS [liquid_hydrogen@60x4015949, station_core@13000000x15, steel_plate@12x10227355]
  COPY   : All Divisions: stack their 3 compounding engines at once -- (1) P0 cargo swarm (`Floor Price` 400c / `Prospect` 100c), (2) Station Tourism + Gourmet supply lines (~200M+ cr rev), and (3) T3 combat wings (`Dialectic` / `Broadaxe`) farming PvE herds.
  COUNTER: OUTSUPPLY their standing bids (silver_ore @101 cr (arneb)) for instant cash velocity; OUTSOURCE their cheap wholesale dumps (liquid_hydrogen @60 cr at arneb) instead of spending fuel/foundry capex.

[HEXC] Hex Collective | NEUTRAL | Lawless Monopoly Elite (threat=medium, owners=Command,Mining,Trade)
  Scale  : 83 ships (55% live 1h), 11 bases, W=9.43B (+9.60M/h) (113.59M/sh) | mix V:68% S:4% F:5% | avgT=3.17 maxT=5 | PvP=58 PvE=2163
  Engine : fleet led by Lithosphere (7x), Frankenhauler (5x), Deep Survey (4x); station Tourism (Hex Star 202.30M cr); heavy crafting (5.87M items); industrial extraction (121.61M ore); bulk missions (23,147 completed); PvE combat farming (2,163 pirate kills); 11 bases (501.01M facilities); capital 68% vault / 4% hulls / 5% fac.
  Hulls  : Lithosphere[T4/P30/1680c](7x), Frankenhauler[T4/P30/2640c](5x), Deep Survey[T3/P20/750c](4x), Perigee[T3/P20/270c](4x)
  Space  : zosma(11), sol(8), the_experiment(3), miaplacidus(3) | allies=IRLC,QTCG,SLKV | UNSCANNED BASES: ascella,aspidiske,barnards_star,chalawan
  Markets: BUYS [uranium_ore@600x3333, lumen_honey_cake@78350x6, void_espresso@2487x177] | SELLS [fuel_cell@3000x17891, fuel_cell@3000x17851, adamantite_ore@47500x484]
  COPY   : Mining+Command: graduate P20/P30 pilots into specialized T3/T4 hulls (Lithosphere (7x), Frankenhauler (5x), Deep Survey (4x)), claim scarce lawless veins (Uranium/Cobalt/Argon/Titanium), and add Station Tourism facilities + Gourmet rations.
  COUNTER: OUTSUPPLY their deep standing bid (uranium_ore @600 cr (dheneb)) with scarce-vein mining & Trade delivery; UNDERCUT their inflated ask (fuel_cell @3000 cr) via Bursar `sell_order --undercut-pct 5`; Intel: scan 9 unscanned bases (ascella, aspidiske, barnards_star).

[IRLC] Ironlight Combine | NEUTRAL | Facility Hub & Freight Power (threat=low, owners=Logistics,Trade,Mining)
  Scale  : 275 ships (62% live 1h), 8 bases, W=6.96B (+12.60M/h) (25.29M/sh) | mix V:53% S:9% F:10% | avgT=2.77 maxT=5 | PvP=11 PvE=402
  Engine : fleet led by Syndicate (52x), Ledger (36x), Concordia (28x); heavy crafting (2.05M items); industrial extraction (429.14M ore); bulk missions (39,914 completed); PvE combat farming (402 pirate kills); 8 bases (720.00M facilities); capital 53% vault / 9% hulls / 10% fac.
  Hulls  : Syndicate[T3/P20/220c](52x), Ledger[T1/P0/480c](36x), Concordia[T3/P20/30c](28x), Frankenhauler[T4/P30/2640c](24x)
  Space  : lhs_1140(56), gsc_0026(29), gold_run(22), synchrony(18) | allies=HEXC | UNSCANNED BASES: bluerift,goldcrest,silverpine
  Markets: BUYS [uranium_ore@600x1666, seam_glass@1200x166, quantum_silk@2100x50] | SELLS [iron_ore@4x29015066, argon_gas@9x6620008, plasma_gas@52x996424]
  COPY   : Logistics+Trade: batch-build P0 `Ledger` (480c) freighters + T3 `Syndicate`/`Concordia` express couriers (`plan.py` selectors `cargo>=400`, `speed>=4`) to saturate `spacemolt_shipping` freight & passenger contracts while running dedicated T2+ mining hulls (`Rock Eater` / `Workhorse`).
  COUNTER: OUTSOURCE their ultra-cheap wholesale ore/gas (iron_ore @4 cr at lhs_1140) so our miners stay on high-margin scarce veins; OUTSUPPLY their standing bid (uranium_ore @600 cr (lhs_1140)); Intel: scan 3 remaining bases (bluerift, goldcrest, silverpine).

[BEAT] BEAT | HAILED | Zero-Base Docked NPC-Facility Factory (threat=low, owners=Trade,Logistics,Intel)
  Scale  : 45 ships (0% live 1h), 0 bases, W=2.41B (+1.06M/h) (53.58M/sh) | mix V:84% S:3% F:2% | avgT=0.00 maxT=0 | PvP=3 PvE=18
  Engine : 45-ship dark/docked fleet (0 hulls spotted in space); heavy crafting (4.57M items); industrial extraction (53.40M ore); 0 bases (zero facility rent); capital 84% vault / 3% hulls / 2% fac.
  Hulls  : unspotted in met
  Space  : unspotted | allies=none
  Markets: BUYS [fuel_cell@50x254, fuel_cell@50x216, iron_ore@1x200] | SELLS [fuel_cell@3000x16147, liquid_hydrogen@150x3732, gold_ore@45x36]
  COPY   : Trade+Logistics: keep ships docked at public NPC industrial stations crafting high-margin recipes into Exchange `sell_order`s (`0` fuel burn, `0` facility rent) so idle/reserve capacity compounds 24/7.
  COUNTER: UNDERCUT their Exchange craft asks via Bursar `sell_order --undercut-pct 5` and corner cheap raw input bids at NPC hubs; undercut their station ask (fuel_cell @3000 cr); Intel: probe core NPC hubs to spot their docked crafting alts (BEAT has 0 ships seen in space).

[ENDL] End of Line | HOSTILE | PvP Raider Bloc (threat=high, owners=Military,Intel,Logistics)
  Scale  : 180 ships (42% live 1h), 8 bases, W=1.75B (+1.86M/h) (9.70M/sh) | mix V:72% S:5% F:4% | avgT=1.14 maxT=4 | PvP=1527 PvE=528
  Engine : fleet led by Prospect (58x), Junk Convoy (28x), Shard (14x); heavy crafting (1.39M items); industrial extraction (100.07M ore); bulk missions (146,285 completed); PvE combat farming (528 pirate kills); aggressive PvP raiding (1,527 kills); capital 72% vault / 5% hulls / 4% fac.
  Hulls  : Prospect[T0/P0/100c](58x), Junk Convoy[T2/P10/850c](28x), Shard[T0/P0/60c](14x), Lithosphere[T4/P30/1680c](9x)
  Space  : barnards_star(11), haven(10), sirius(6), sol(5) | allies=none | UNSCANNED BASES: barnardstar,betelgeuse,fomalhaut,gsc_0040
  Markets: BUYS [none scanned] | SELLS [none scanned]
  COPY   : Military: copy their high-cargo war-logistics (`Junk Convoy` 850c) + T4 `Lithosphere` backing; run bulk combat/supply missions (`plan.py` combat wing) while strictly holding defensive RoE (F2).
  COUNTER: Route unescorted haulers around their hot systems; pair T2+ escorts (`escort-` routes) on lawless runs; log every sighting in `game/factions/h-endl.md`; Intel: fast-scout 8 unscanned bases (barnardstar, betelgeuse, fomalhaut).

[NOIR] Interstellar Continental | RIVAL | Zero-Base Express & Exchange (threat=low, owners=Trade,Logistics)
  Scale  : 31 ships (84% live 1h), 0 bases, W=1.57B (+2.92M/h) (50.78M/sh) | mix V:25% S:14% F:5% | avgT=2.48 maxT=5 | PvP=0 PvE=0
  Engine : fleet led by Futures (10x), Syndicate (10x), MacGuffin (4x); heavy crafting (1.77M items); bulk missions (39,297 completed); 0 bases (zero facility rent); capital 25% vault / 14% hulls / 5% fac.
  Hulls  : Futures[T1/P0/30c](10x), Syndicate[T3/P20/220c](10x), MacGuffin[T4/P0/240c](4x), Concordia[T3/P20/30c](2x)
  Space  : unknown_edge(4), nova_terra(4), the_rampart(2), node_alpha(2) | allies=none
  Markets: BUYS [none scanned] | SELLS [none scanned]
  COPY   : Trade+Logistics: assign fast P0/T1/T3 couriers (`Runner` spd 6 / `Futures` / `Concordia` / `Syndicate`) to express passenger lines + core Exchange spread arbitrage (`sell_order --undercut-pct 5` + `buy_order`) -- generates >20M/h with ZERO station rent.
  COUNTER: UNDERCUT their core Exchange spreads by 1-5% using docked zero-fuel Bursars across all 5 empire hubs (`market_prime`, `the_crucible`, `nova_terra`) and race them on high-pay passenger corridors.

[HIVE] Hive Swarm | HAILED | Regional Industrial & Hauling Hub (threat=low, owners=Logistics,Trade,Intel)
  Scale  : 190 ships (45% live 1h), 3 bases, W=1.03B (+89.3k/h) (5.44M/sh) | mix V:65% S:1% F:11% | avgT=0.96 maxT=3 | PvP=0 PvE=0
  Engine : fleet led by Workhorse (41x), Prospect (38x), Runner (31x); active refining/crafting (538.8k items); industrial extraction (51.00M ore); 3 bases (110.45M facilities); capital 65% vault / 1% hulls / 11% fac.
  Hulls  : Workhorse[T2/P0/300c](41x), Prospect[T0/P0/100c](38x), Runner[T1/P0/120c](31x), Theoria[T0/P0/70c](14x)
  Space  : segin(15), antares(12), khambalia(7), treasure_cache(6) | allies=OLSV,VEIL | UNSCANNED BASES: antares,segin,sulafat
  Markets: BUYS [none scanned] | SELLS [none scanned]
  COPY   : Logistics+Mining: adopt their proven P0/T1 workhorse mix (Workhorse (41x), Prospect (38x), Runner (31x)) -- `Workhorse` (300c) / `Congregation` (1,900c) for bulk hauls and `Runner` (120c, spd 6) for fast corridor shuttles & courier contracts.
  COUNTER: Intel: dock & scan 3 unscanned bases (antares, segin, sulafat) to unlock trade arbitrage.

[MIN9] MIN9 | HAILED | Zero-Base Docked NPC-Facility Factory (threat=low, owners=Trade,Logistics,Intel)
  Scale  : 29 ships (0% live 1h), 0 bases, W=1.01B (+52.1k/h) (34.89M/sh) | mix V:0% S:1% F:2% | avgT=0.00 maxT=0 | PvP=12 PvE=4
  Engine : 29-ship dark/docked fleet (0 hulls spotted in space); heavy crafting (7.03M items); industrial extraction (78.72M ore); 0 bases (zero facility rent); capital 0% vault / 1% hulls / 2% fac.
  Hulls  : unspotted in met
  Space  : unspotted | allies=none
  Markets: BUYS [none scanned] | SELLS [none scanned]
  COPY   : Trade+Logistics: keep ships docked at public NPC industrial stations crafting high-margin recipes into Exchange `sell_order`s (`0` fuel burn, `0` facility rent) so idle/reserve capacity compounds 24/7.
  COUNTER: UNDERCUT their Exchange craft asks via Bursar `sell_order --undercut-pct 5` and corner cheap raw input bids at NPC hubs; Intel: probe core NPC hubs to spot their docked crafting alts (MIN9 has 0 ships seen in space).

[WEXL] Wexler's Void Safari | HAILED | Zero-Base Bulk Mission/Freight Swarm (threat=low, owners=Logistics,Trade)
  Scale  : 154 ships (28% live 1h), 0 bases, W=650.33M (+378.1k/h) (4.22M/sh) | mix V:96% S:2% F:1% | avgT=0.22 maxT=4 | PvP=1 PvE=293
  Engine : fleet led by Cobble (130x), Congregation (10x), Prayer (8x); active refining/crafting (425.8k items); bulk missions (132,761 completed); 0 bases (zero facility rent); capital 96% vault / 2% hulls / 1% fac.
  Hulls  : Cobble[T0/P0/75c](130x), Congregation[T1/P0/1900c](10x), Prayer[T1/P0/540c](8x), Frankenhauler[T4/P30/2640c](2x)
  Space  : market_prime(37), void_gate(14), last_light(7), first_step(6) | allies=none
  Markets: BUYS [none scanned] | SELLS [none scanned]
  COPY   : Logistics+Trade: commission cheap P0 high-cargo hulls (`Prayer` 540c / `Congregation` 1,900c) on `freight-` (`spacemolt_shipping`) and bulk procurement missions (`plan.py` selector `cargo>=400`) around core empire hubs with zero base overhead.
  COUNTER: Out-scale their P0 `Cobble` swarm on high-margin `spacemolt_shipping` freight contracts & core hub deliveries using faster T1/T2 haulers (`Ledger`/`Prayer`) and pre-stocked station buffers.

[CRFT] Crafting Collective | HAILED | Regional Industrial & Hauling Hub (threat=low, owners=Logistics,Trade,Intel)
  Scale  : 101 ships (15% live 1h), 2 bases, W=476.74M (+1.39M/h) (4.72M/sh) | mix V:72% S:4% F:7% | avgT=0.75 maxT=4 | PvP=2 PvE=0
  Engine : fleet led by Congregation (33x), Cobble (30x), Theoria (10x); active refining/crafting (296.0k items); bulk missions (23,696 completed); capital 72% vault / 4% hulls / 7% fac.
  Hulls  : Congregation[T1/P0/1900c](33x), Cobble[T0/P0/75c](30x), Theoria[T0/P0/70c](10x), Compendium[T3/P20/625c](4x)
  Space  : cloverfield(44), beid(12), treasure_cache(9), unknown_edge(2) | allies=DB,HELP,XPLR,YSMT | UNSCANNED BASES: beid
  Markets: BUYS [fuel_cell@50x175, lumen_oil@10x16] | SELLS [pirate_moonshine@400x15283, copper_ore@5x263052, purified_water@60x9950]
  COPY   : Logistics+Mining: adopt their proven P0/T1 workhorse mix (Congregation (33x), Cobble (30x), Theoria (10x)) -- `Workhorse` (300c) / `Congregation` (1,900c) for bulk hauls and `Runner` (120c, spd 6) for fast corridor shuttles & courier contracts.
  COUNTER: OUTSOURCE their cheap wholesale ore (copper_ore @5 cr at cloverfield); UNDERCUT their specialty goods (pirate_moonshine @400 cr); Intel: dock & scan 1 unscanned bases (beid) to unlock trade arbitrage.

[STRG] STRG | HAILED | Zero-Base Docked NPC-Facility Factory (threat=low, owners=Trade,Logistics,Intel)
  Scale  : 200 ships (0% live 1h), 0 bases, W=448.47M (+202.6k/h) (2.24M/sh) | mix V:72% S:3% F:6% | avgT=0.00 maxT=0 | PvP=2 PvE=9
  Engine : 200-ship dark/docked fleet (0 hulls spotted in space); heavy crafting (2.29M items); 0 bases (zero facility rent); capital 72% vault / 3% hulls / 6% fac.
  Hulls  : unspotted in met
  Space  : unspotted | allies=none
  Markets: BUYS [none scanned] | SELLS [none scanned]
  COPY   : Trade+Logistics: keep ships docked at public NPC industrial stations crafting high-margin recipes into Exchange `sell_order`s (`0` fuel burn, `0` facility rent) so idle/reserve capacity compounds 24/7.
  COUNTER: UNDERCUT their Exchange craft asks via Bursar `sell_order --undercut-pct 5` and corner cheap raw input bids at NPC hubs; Intel: probe core NPC hubs to spot their docked crafting alts (STRG has 0 ships seen in space).

[MOON] Rise and Fall of Goldcrest Moon | HAILED | High-Tier Boutique Base Syndicate (threat=low, owners=Command,Trade,Mining)
  Scale  : 17 ships (18% live 1h), 4 bases, W=416.45M (+479.8k/h) (24.50M/sh) | mix V:45% S:5% F:49% | avgT=2.88 maxT=4 | PvP=0 PvE=68
  Engine : fleet led by Deep Survey (3x), Excavation (2x), Blind Spot (1x); 4 bases (203.65M facilities); capital 45% vault / 5% hulls / 49% fac.
  Hulls  : Deep Survey[T3/P20/750c](3x), Excavation[T2/P10/200c](2x), Blind Spot[T4/P30/265c](1x), Axiomata[T4/P30/180c](1x)
  Space  : nashira(4), the_crucible(1), ironhollow(1), coppervale(1) | allies=BEIN,BUSY,DEAD
  Markets: BUYS [fuel_cell@50x951, fuel_cell@50x239, fuel_cell@50x19] | SELLS [fuel_cell@3000x18340, steel_plate@55x3192, trade_crystal@425x188]
  COPY   : Mining+Command: mirror their high wealth-per-ship (24.50M/sh, avg T2.9) by concentrating P20/P30 pilots into T3/T4 hulls (Deep Survey (3x), Excavation (2x), Blind Spot (1x)) anchored to high-value facility hubs.
  COUNTER: UNDERCUT their high-markup station asks (fuel_cell @3000 cr at diphda) via Bursar `sell_order`; OUTSUPPLY their hub fuel/input bids (fuel_cell @50 cr (ross_248)). () refreshes live in  for the Command Station HUD Empire panel, writes  hourly via , and feeds role-filtered briefings to every Admiral via .

### Five Concrete Accuracy & Effectiveness Fixes Recommended

1. **Stop Wasting 3/12 Rival Cards on AFK Factions (, , ):**
   - Currently  runs , which shows 3 factions with  active pilots in 24h while **completely hiding our #1 peer  ( ships, , allied to ),  ( ships,  active, ), and  ( T4 ships,  crafting )!**
   - **Recommended fix:** Select top  rivals using **active + rising criteria** (e.g., Top 9 active by wealth + Top 3-5 active by velocity/size/crafting where , moving -active legacy vaults to a compact "Dormant Vaults" footer).
2. **Fix Stale Velocity & Playbook Strings in :**
   - Replace hardcoded  with live-computed  velocity ( over 35.7h).
   - Ensure  velocity calculation only computes  across **non-zero** wealth snapshots () so newly-tracked factions never show bogus  spikes.
   - Update Playbook #1 () and Playbook #4 () to reference our live policy-driven engines ( /  and  / ) instead of legacy manual per-station desk scripts.
3. **Fix  Benchmark Card in :**
   - Show both ** total fleet ( seated)** and **** so Admirals and Suggi compare apples-to-apples against rivals whose leaderboard wealth uses catalog storage valuation.
4. **Refresh Stale Division Loadout Cards () & :**
   -  (last updated ) and  () predate our 500-ship 5-empire layout and .
   - Add an explicit **"P0 Instant Hull Skip"** section to  & division  files (, , , , , , , , ) plus verified T2+ module loadouts per role so Admirals immediately prioritize high-ROI P0 upgrades for their  sub-P10 ships alongside P10+ T2 batches.
5. **Add a 9th Strategy Playbook ("Value-Added Crafting & Outsupply Refining"):**
   - Our 8 playbooks cover Tourism, NPC-Facility, Bursar, Express, Bulk Freight, Scarce Mining, Wholesale Arbitrage, and Combat -- adding explicit **Crafting Conversion** (, , ) directly tracks our conversion of raw vault ore ( catalog) into high-margin crafted goods and rival buy-wall cash.

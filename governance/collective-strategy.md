---
name: collective-strategy
id: 20261124T091702Z
tier: governance
status: living-standing-plan
author: Trinity
updated: 2026-11-24
links:
  - governance/strategy.md
  - governance/the-collective-constitution.md
  - governance/rulebook.md
  - governance/rival-sedcards.md
  - governance/strategy-improve.md
  - governance/kpi-and-strategy-system.md
  - governance/treasury-wallet-and-upgrades-blueprint.md
  - governance/accounting-and-hud-blueprint.md
  - governance/system-architecture.md
  - governance/agents-and-orchestration.md
  - game/bursar-policy.json
  - game/haul-policy.json
---

# The Collective -- Living Fleet Playstyle & Standing Strategy Blueprint

> **Living Standing Plan Notice:** Unlike `governance/strategy.md` (our approval-locked eternal
> North Star covering Goals G1-G5 and Operational Subgoals O1-O10), this document captures **how
> The Collective actually plays SpaceMolt today** -- our fleet structure, active division playstyles,
> cross-division flywheel, adopted rival strategies, and automated engines. It is intentionally a
> living standing plan and will evolve as the fleet scales from 500 toward 1,000 ships, advances
> from Tier 2 into Tier 3-5 hulls, and builds sovereign stations and tourism hubs.
>
> Live ship counts, credit balances, and daily rates are never hardcoded here; inspect live state via
> `hive.py scorecard`, `hive.py board all`, `read.db`, or the Command Station HUD.

---

## 1. Core Identity & Playstyle Philosophy

The Collective plays SpaceMolt as a **vertically integrated, multi-empire, capital-allocating
galactic enterprise** -- combining the industrial discipline of a factory game, the spatial
spread and compounding build-order of an RTS, and the market-making / diplomatic realism of an
MMO sandbox.

### Five Defining Pillars of Our Playstyle

1. **All-8-Strategies Saturation (No Single-Trick Fragility):**
   Top rival factions typically specialize in one archetype (only mining, only market-making, only
   mission-swarming, or only tourism). With a multi-empire fleet scaling from 500 toward 1,000
   ships across all five empires (Voidborn, Nebula, Solarian, Outer Rim, Crimson), The Collective
   runs **all eight proven SpaceMolt economic & military engines in parallel** under one
   consolidated purse.
2. **Strict Class Harmony & Symbiosis (Rule F23):**
   Every division specializes in its own comparative advantage rather than competing against itself:
   - **Mining** extracts raw ores/ices/gases and hands them inward (never sells directly under
     `strict-classes-on`).
   - **Trade** owns the Exchanges, Bursar desks, market-making, wholesale procurement, final
     liquidation, and **commercial value-added crafting** (profit goods & rival buy-walls such as
     `silver_bar`, rations, modules, components) across all five empires.
   - **Logistics** owns bulk freight (`spacemolt_shipping`), **civilian & express passenger
     transport** (`passenger-`), **industrial building-material crafting** (`steel_plate`,
     `circuit_board`, `wiring`, `piping`), supply-chain fulfillment, and station/outpost builds.
   - **Military** owns PvE herd harvesting, pirate pack/stronghold farming, route escorts, and
     sovereign defense.
   - **Intel** owns galaxy reconnaissance, market/field freshness, rival intelligence, and
     diplomatic outreach.
   - **Command** owns consolidated capital allocation, faction seating/officers, sovereign base
     expansion, cross-division prioritization, and flagship diplomacy.
3. **Architecture & Incentives Over Micromanagement:**
   Strategic direction lives in policy files, division plans, and KPI scorecards -- never in
   ad-hoc manual babysitting. Dynamic runners (`mine.py`, `hunt.py`, `bursar.py`, `haul.py`,
   `census.py`, `route_run.py`) and hard anti-crowding guards (`dispatch.py`, `fill.py`) fan
   hundreds of ships across the entire galaxy automatically.
4. **Defensive Realism & Peaceful Neutrality Max (Rules F2, F4, O10):**
   We do not initiate PvP aggression. When attacked, escorts defend and ships disengage cleanly.
   Diplomatically, we maintain strict **Neutrality / Non-Aggression / Trade** outreach across top
   galactic blocs (capped at Neutrality -- no entangling military alliances) behind a strict
   anti-prompt-injection firewall and zero cross-bloc OpSec disclosure.
5. **One-Purse Enterprise Accounting (IAS 2 & Responsibility Centers):**
   Divisions are evaluated by their true economic role (Profit Center, Production Center,
   Service/Infra Center, Combat/Security Center, Cost Center, Investment Center) rather than raw
   wallet cash alone -- tracking Consolidated Net Worth (Treasury + wallets + vault inventory +
   fitted hulls + sovereign bases) and recurring matched cashflow.

---

## 2. How the Six Divisions Work Together (The Symbiotic Flywheel)

```text
                        +---------------------------------------+
                        |         COMMAND (Unity)               |
                        |  One-Purse Treasury | Base Strategy   |
                        |  Officers/Seats | Needs | Diplomacy   |
                        +-------+-----------------------+-------+
                                | capital & priorities  |
          +---------------------+-----------+-----------+---------------------+
          v                                 v                                 v
+-------------------+            +--------------------+            +-------------------+
|  INTEL (Oracle)   |  <3h books |   MINING (Zero)    |  raw ore   | MILITARY (Apophis)|
|  Census & Recon   +----------->|  <=3/belt Spread   +-----+      |  1-2/herd Hunts   |
|  Rival Sedcards   |  rich POIs |  keep_items Filter |     |      |  Pirate Packs     |
|  Diplomatic Envoy |            |  F23 Store/Handover|     |      |  Escorts & Guard  |
+---------+---------+            +--------------------+     |      +---------+---------+
          |                                                 |                |
          | live spreads &                                  v                | loot
          | partner boards                     +------------------------+    | handover
          +----------------------------------->|  LOGISTICS (Apollo)    |<---+
                                               |  haul.py Auto-Hauler   |
          +----------------------------------->|  Freight & Arbitrage   |
          |                                    |  Crafting & Outposts   |
          |  live 60+ station books &          |  Faction Lockboxes     |
          |  bottleneck buy_order fills        +-----------+------------+
          |                                                |
+---------+---------+                                      | finished goods &
|  TRADE (Mercury)  |<-------------------------------------+ surplus stock
|  bursar.py (1/hub)|
|  60+ Global Books |-----> Recurring Cashflow -----> Treasury & Fleet Upgrades
|  Buy & Sell Walls |
|  Docked Factories |
+-------------------+
```

### The Self-Feeding Trade <-> Logistics <-> Mining Loop

1. **Intel** keeps systems, asteroid belts, wildlife herds, rival bases, and station books mapped
   and fresh (`<3h` on worked corridors).
2. **Mining** spreads across dozens of rich belts across all five empires (hard-capped at **3 ships
   per belt**), using `keep_items` / `jettison_gangue` to concentrate scarce high-value ores
   (`silicon_ore`, `gold_ore`, `platinum_ore`, `uranium_ore`, `silver_ore`, `titanium_ore`)
   and handing ore into faction/station storage without burning time on cheap 1-cr bulk dumps.
3. **Trade** stations **1 Bursar per Exchange station** across all policed hubs and safe
   non-stronghold books via `bursar.py` + `game/bursar-policy.json`. Every 2 minutes at zero
   fuel, each Bursar refreshes live order books & mission boards across the galaxy, maintains
   wholesale `buy_order` walls for open `needs.tsv` bottlenecks, and liquidates unreserved
   surplus via instant bid hits or undercut `sell_order` listings (strictly respecting
   `reserve.tsv`).
4. **Logistics** runs `haul.py` + `game/haul-policy.json` as the galaxy's arteries: resuming
   active freight, picking safe public/partner `spacemolt_shipping` contracts, flying
   live-verified cross-station Exchange arbitrage unlocked by the Bursars' fresh books, moving
   internal `needs.tsv` supply into home lockboxes, and crafting/building sovereign infrastructure
   and station modules.
5. **Military** spreads across 100+ PvE herd zones (1-2 ships per herd) and scalable pirate
   formation hunts on T2+ combat hulls, gifting loot to Trade and escorting lawless operations.
6. **Command** sweeps excess pilot credits automatically into the central Faction Treasury via
   parallel direct deposits & Officer lockboxes (`wallet.py`), funds role-matched T2+ hull &
   T2/T3 module upgrades (`upgrades.py`), grows faction seating & Officer coverage, and directs
   sovereign station expansion.

---

## 3. Division Operating Cards -- Roles, Jobs, Active Playstyle & Guardrails

### 3.1 Command Division -- Fleet Admiral: Unity (Investment Center)
- **Ship Role:** `command` (including flagship `Prime Directive`).
- **Core Mandate:** Consolidated capital allocation, strategic planning (`orders.log` PLAN),
  `needs.tsv` priority register, faction seating/Officer promotion, sovereign station/outpost
  strategy, cross-division request resolution (`requests.log`), and flagship diplomacy with
  established Neutral partners.
- **Active Playstyle:**
  - Runs the 500-to-1,000-ship multi-empire scaling roadmap (multi-empire birth balance across
    Voidborn, Nebula, Solarian, Outer Rim, Crimson so every empire has local zero-border labor).
  - Allocates central Treasury funds via the dedicated 60s `wallet` shelf service (parallel P2P
    + up to 50 auto-promoted Officers with >=4/division, 500k Treasury floor) toward highest-ROI
    capex: Piloting-0 instant T1/T2 hull skips, listed shipyard bargains (`ship_listings` /
    `upgrades.py` auto `buy_listed_ship`), T2/T3 modules, faction lockboxes, outposts, and
    **wholesale `station_core` procurement (~13M cr at Arneb vs slow self-build)**.
  - Enforces MAUT x WSJF triage (`P0 > P1 > P2 > P3`) across divisions using `scorecard.py`.
  - Runs Make-vs-Buy capital discipline: compares live rival wholesale asks (e.g., `station_core`,
    `steel_plate`, cheap raw inputs) against internal foundry capex before committing capital.
- **Guardrails:** Never micromanages division-internal routing (Rule F16); retains override on
  role-hull exceptions and cross-division conflicts.

### 3.2 Mining Division -- Admiral: Zero (Production Center)
- **Ship Role:** `miner`.
- **Core Mandate:** Continuous raw resource extraction feeding `needs.tsv`, `reserve.tsv`,
  and high-value scarce ore supply across all five empires.
- **Active Playstyle:**
  - **Wide Galactic Spread:** Mirrors Military's anti-crowding model -- hard-capped at
    **`MINE_POI_CAP = 3` miners per belt** (`dispatch.py` + `fill.py`) so 130+ miners fan
    across 45-75+ distinct belts across all 5 empires instead of depleting 4 belts.
  - **F23 Pure Extraction:** Under `strict-classes-on`, miners never waste ticks selling;
    `routemaker.py` scores hundreds of belts across the galaxy and emits F23-clean gather/store
    routes (`with_sell = 0`, `max_ships = 3`), with automatic `faction -> self` storage
    fallback in `mine.py` for unseated pilots.
  - **Purity Filtering (`keep_items` / `jettison_gangue`):** Drops low-value common gangue
    in-belt so ships stay on rich veins longer, train Mining XP continuously, and haul back
    high-purity scarce ore (`silicon_ore`, `gold_ore`, `platinum_ore`, `uranium_ore`,
    `silver_ore`, `cobalt_ore`, `titanium_ore`).
  - **Avoids Cheap Bulk Traps:** Leaves 1-cr rival bulk dumps (cheap iron/copper/nitrogen where
    rivals oversupply) for Trade/Logistics to buy wholesale, focusing lasers on bottleneck and
    high-margin veins.
  - **Depletion Hygiene (`15%` Default Floor, `>=25%` T2/T3 Guidance):** `routemaker.py` and
    bulk `mine-*` routes enforce a **`15%` `min_left` floor** (full 6h turn buffer of 4,500-15,000
    ore between turns); T2/T3 multi-laser arrays target `>=25%` fresh outer belts to stay above
    the `07-economy.md` `deposit_too_sparse` cliff (`depletion_floor = 0.25`).
  - **Upgrade Ladder:** Instant Piloting-0 T1/T2 skip (`Workhorse` 300c, `Bonanza` 180c) via
    `upgrades.py` auto listed-ship buy, role-matched `mining_laser_ii/iii/iv`, `ice_harvester`,
    `gas_harvester`, and P10+/P30+ hulls (`Resonance Miner`, `Lithosphere`, `Tellurian`).
- **Primary KPIs:** Ore/ship-hour, IAS 2 handover value-add, Belt Spread (`<= 3/belt`,
  `FIELD_CONGESTION` alarm at `>= 4/6`), T2+ mining hulls & lasers.

### 3.3 Trade Division -- Admiral: Mercury (Profit Center)
- **Ship Role:** `trader`.
- **Core Mandate:** Fleet recurring cashflow engine -- global multi-hub Exchange market-making,
  bottleneck wholesale procurement, surplus liquidation, zero-fuel docked crafting, and Channel
  1-4 P2P trade (`contracts.log`).
- **Active Playstyle:**
  - **Global 60+ Hub Bursar Network (`bursar.py` + `game/bursar-policy.json`):**
    Replaces static per-station JSON files with one dynamic engine enforcing a strict **`1`
    Bursar per station cap** (`BURSAR_STATION_CAP = 1`). Automatically staffs 100% of policed
    empire Exchange hubs first, then expands across safe non-stronghold Exchange books (excluding
    pirate strongholds). Zero self-undercutting, zero wasted fuel.
  - **Dual-Sided Market-Making (Channel 1):**
    - *Wholesale Buy Walls (`buy_order`):* Bids below ask ceiling for open `needs.tsv`
      bottlenecks (`foil_scale`, `anchor_plate`, `graphene_thread`, `silicon_ore`, etc.).
    - *Surplus Liquidation (`sell_order` & instant bid hits):* Hits strong buyer bids directly
      or lists undercut `sell_order` asks above floor while strictly protecting `reserve.tsv`
      and `needs.tsv` items.
  - **Zero-Fuel Commercial Value-Added Crafting (Split with Logistics):** Parks docked traders at
    public NPC refineries/factories crafting commercial profit goods & rival buy-walls (`silver_bar`,
    gourmet rations, components, modules) at 0 fuel and 0 rent (while Logistics crafts empire
    building materials).
  - **Outsupply / Undercut / Outsource:** Feeds deep rival standing bids (gourmet rations,
    refined bars, scarce ore), undercuts inflated rival asks by 5-10%, and buys underpriced
    rival wholesale surplus.
  - **Upgrade Ladder:** Instant Piloting-0 bulk hull skip (`Floor Price` 400c, `Ledger` 480c,
    `Prayer` 540c) via `upgrades.py` auto `buy_listed_ship` (`ship_listings`), `cargo_expander_ii/iii`,
    and P10+ `Apophenia` / empire equivalents.
- **Primary KPIs:** Recurring matched cashflow (`> 0 cr/h` & rising), Accrual operating income,
  Hub Coverage (policed & global books staffed, `HUB_CONGESTION` alarm at `>= 2/4`), Surplus
  Backlog liquidation.

### 3.4 Logistics Division -- Admiral: Apollo (Service & Infrastructure Center)
- **Ship Role:** `hauler`.
- **Core Mandate:** Galactic freight backbone, inter-station arbitrage execution, supply-chain
  fulfillment (`reserve.tsv` / `needs.tsv`), industrial crafting, and sovereign
  outpost/station construction.
- **Active Playstyle:**
  - **Autonomous Hauler Engine (`haul.py` + `game/haul-policy.json`):**
    Whenever a hauler finishes a priority build/mission run, it dynamically claims and executes
    the highest-EV safe job across four lanes (atomic claims in `haul_claims.json` prevent
    collisions):
    1. *Active Freight Resume:* Completes any in-flight `spacemolt_shipping` delivery first.
    2. *Public & Neutral-Partner Freight Board (Channel 3):* Picks policed, charted
       `spacemolt_shipping` contracts meeting `min_cr_per_jump` and `max_collateral`, giving
       a +25% score priority to Neutral diplomatic partners.
    3. *Live-Verified Cross-Station Arbitrage:* Exploits spreads revealed by the Bursars' live
       order-book refreshes; re-checks live `view_market` at the buy station before purchasing
       and stores safely for the local Bursar if a destination bid slips (never panic-dumps at a
       loss).
    4. *Internal Empire Supply Rebalancing:* Moves remote `needs.tsv` materials home into
       active faction lockboxes.
  - **Industrial Crafting & Base Construction:** Runs zero-fuel docked smelting/crafting for
    outpost kits, station modules, and fleet reserve components; migrates redundant rent-paying
    NPC offices onto rent-free sovereign bases (dismantling old NPC offices for 100% material
    recovery).
  - **Civilian & Express Passenger Wing + Bulk Freight P0 Skip:** Operates `passenger-` express
    routes (`Runner` 120c spd 6 / `Futures` P0 fitted with `economy_passenger_cabin` /
    `business_passenger_cabin` sourced from `read.db:books`) alongside instant Piloting-0 bulk
    freighters (`Floor Price` 400c, `Ledger` 480c, `Prayer` 540c, `Congregation` 1,900c) bought
    via `upgrades.py` auto `buy_listed_ship` (`ship_listings`).
- **Primary KPIs:** Supply chains at keep, open P1/P2 fulfillment SLA, active freight/haul runs,
  zero idle haulers.

### 3.5 Military Division -- Admiral: Apophis (Combat & Security Center)
- **Ship Role:** `drone`, `sentinel`.
- **Core Mandate:** Zero-loss security, scalable PvE herd harvesting, pirate formation farming,
  lawless escorts, and war-readiness deterrence.
- **Active Playstyle:**
  - **Wide PvE Herd Spread:** Fans 100+ combat ships across ~90-110 distinct wildlife POIs at
    **1-2 ships per herd** (Rule F9), gifting combat loot (`foil_scale`, `alloy_scale`,
    `carapace`, `glands`, `bladders`) into Trade/Logistics supply chains.
  - **Listed T2 Bargains & Focused 5-8 Ship Pirate Packs (Rule F27):** Auto-buys underpriced
    listed combat hulls (`Broadaxe` ~37k, `Recursion` ~224k, `Apophenia` ~141k via `ship_listings`
    & `upgrades.py`) and runs focused 5-8 ship pirate/bounty formations (`pirates_ok: true`).
  - **Defensive Deterrence & Escort Doctrine (Rule F2):** Maintains `posture:WAR_ALERT` plans,
    tracks high-PvP threats (such as `[ENDL]`), escorts high-value lawless miners/builders, and
    trains `sentinel` Royal Guard ships while strictly respecting Neutral pacts.
- **Primary KPIs:** Zero unescorted ship losses, Combat XP/ship-hour, Kills/24h, IAS 2 loot
  value-add, T2+ combat hull & weapon fit saturation.

### 3.6 Intel Division -- Admiral: Oracle (Recon & Diplomacy Cost Center)
- **Ship Role:** `scout`.
- **Core Mandate:** Information supremacy across the entire galaxy -- fresh market/field/herd
  intelligence, rival surveillance, and autonomous Neutrality diplomacy.
- **Active Playstyle:**
  - **Freshness & Blind-Spot Closure:** Keeps worked corridors, scarce veins, and rival bases
    under `<3h` freshness; minimizes redundant patrol loops where docked Bursars and working
    ships already refresh books passively for free.
  - **Rival, Ship-Market & Module Intelligence Pipeline:** `rivals.py` prioritizes active/rising
    rivals (`active_24h > 0`) with honest non-zero velocity in `governance/rival-sedcards.md` and
    the HUD Empire tab; `ledger.py` auto-scans galaxy-wide `browse_ships` every 15 min into
    `read.db:ship_listings` while `books` tracks live module asks (`economy_passenger_cabin`,
    T2-T4 lasers/shields/expanders).
  - **Autonomous Diplomatic Envoy (Rule F4, O10):** Polls envoy inboxes via `diplomacy.py`
    across tracked galactic blocs (11+ blocs / 23+ leaders), coordinates Neutrality & Trade
    pacts with Unity's flagship, enforces strict anti-injection quarantine, and upholds zero
    cross-bloc disclosure.
- **Primary KPIs:** Place & market freshness (`>= 80%` `<3h`), zero scout losses, diplomatic
  reply SLA (`0` unanswered partner threads).

---

### Mandatory Core Engines vs. Optional Secondary Playbooks (`strategy.md` v2.5)

To match Suggi's updated Tier-1 (`G1-G5`) and Tier-2 (`O1-O10`) mandate, our 8-Strategy Matrix is
explicitly tiered so opportunistic tactics never starve core enterprise output:

- **Mandatory Core Engines (Tier 1 & Tier 2 -- always active; tune caps, never turn off):**
  1. **Raw Resource Extraction** (Mining: wide galactic spread `<=3/belt`, `15%` default floor,
     scarce veins feeding our own chains).
  2. **Manufacturing & Production Powerhouse** (Trade zero-fuel **commercial crafting** for profit
     & rival buy-walls; Logistics zero-fuel **industrial building-material crafting** for bases,
     modules, and fleet kits).
  3. **5-Empire Multi-Hub Trade & Bursar-Hauler Combo** (Trade `bursar-network` with fleet-wide
     `bursar_buys.json` unit caps + undercut sell ladders refreshing books every 2 min, paired with
     Logistics `haul-network` fresh `<30m` bid-locked arbitrage, `>=100c` `spacemolt_shipping`, and
     4-channel P2P trade).
  4. **Sovereign Expansion, Shipyards & Defensive Deterrence** (5 stations with licensed
     multi-empire faction shipyards `outfitting_bay` -> `fabrication_yard` -> `grand_shipworks`,
     8 outposts, 1,000-ship fleet, PvE/pirate combat & defensive RoE).
- **Optional / Opportunistic Secondary Playbooks (Tactical tier below -- pursue via `P3 MENU`):**
  - **Sovereign Tourism & Gourmet Hubs** (once sovereign stations stand),
  - **Express Civilian Passenger Lines** (`passenger-` routes on P0 `Runner`/`Futures` with cabins),
  - **Opportunistic Wholesale Capital Arbitrage** (e.g., buying wholesale `station_core` ~13M cr
    or deep rival surplus dumps whenever prices beat internal craft cost).

### Cross-Empire Hull Standardization (Zero Penalty) & Station Shipyards

Verified in `game/rules/05-galaxy.md`: **flying another empire's hull carries zero stat penalty**,
and a pilot's native empire bonus (`+12%` shield, Mastery skills) applies to *whatever* hull they
fly. Therefore The Collective **standardizes the best hull per job across all five empires** rather
than locking pilots to birth-empire lines, using `upgrades.py` (`ship_listings` auto `buy_listed_ship`)
today and **licensed in-house construction at our own station shipyards** once our first full station
is placed.

## 4. Rival Playbooks Adopted vs. Countered (Our 8-Strategy Matrix)

The Collective continuously benchmarks top galactic factions via `governance/rival-sedcards.md`
and `game/fleet/rival_playbook.py`, copying every proven compounding mechanic while countering
rival bottlenecks:

| # | Strategy Archetype | Proven Rival Benchmark | How The Collective COPIES It | How We COUNTER Rivals |
|:-:|:--|:--|:--|:--|
| **1** | **Sovereign Tourism & Gourmet Hub** | `[BUSY]` The Obsidian Well, `[HEXC]` Hex Star | Command + Logistics build sovereign stations & high-appeal Tourism modules; Trade stocks gourmet food & specialty drinks for zero-fuel passive cashflow | Trade feeds rival Tourism hubs' standing gourmet/drink bids today to capture their cashflow before our own hubs finish |
| **2** | **Zero-Fuel Docked NPC-Facility Factory** | Active `[MOTH]`, `[HIVE]`, `[STLR]`, `[CRFT]`; legacy `[MIN9]`, `[BEAT]` | **Trade** crafts commercial profit goods & rival buy-walls (`silver_bar`, rations, modules); **Logistics** crafts empire building materials (`steel_plate`, `circuit_board`, `wiring`, `piping`) at 0 fuel | Outbid raw inputs with Bursar buy walls and undercut inflated finished asks by 5-10% |
| **3** | **Multi-Hub Exchange Market-Making (Bursar)** | `[NOIR]` (live velocity, 0 bases), `Vex Nebulon` | `bursar.py` (`bursar-policy.json`, uncapped escrow) stations 1 Trader per policed/safe hub with dynamic `buy_order` + undercut `sell_order` & live book refresh | Eliminate single-hub congestion and out-cover single-region rivals across all 5 empires simultaneously |
| **4** | **Zero-Base Express Passenger & Courier** | `[NOIR]` (`Runner` / `Futures` / `Concordia`), `LimaTango1428` | Logistics runs `passenger-` express wings on P0 `Runner`/`Futures` fitted with `economy_passenger_cabin` / `business_passenger_cabin` (from `read.db:books`) | Compete across all 5 empire corridors where local birth-empire ships start already positioned |
| **5** | **Bulk Freight & Mission Swarm** | `[WEXL]` (`Prayer` / `Congregation`), `[IRLC]` (`Ledger`), `[ENDL]` | `haul.py` (`haul-policy.json`) automates `spacemolt_shipping`; P0 instant hull skip (`Floor Price` 400c / `Ledger` 480c / `Prayer` 540c / `Congregation` 1,900c) via `ship_listings` | Prioritize Neutral partners (+25% score bonus) and reject unprofitable pirate-stronghold traps |
| **6** | **Lawless Scarce-Vein Monopoly Extraction** | `[HEXC]` (11 bases, T3+ miners), `[IRLC]` (32M+ ore) | Mining spreads `<= 3/belt` with `15%` default `min_left` floor (`>=25%` for T2/T3) + `keep_items` filtering and P0->T2 industrial upgrades | Never mine 1-cr rival bulk dumps (buy them wholesale instead); monopolize scarce bottleneck ores |
| **7** | **Wholesale Capital Arbitrage (Outsource & Outsupply)** | Live rival books & `ship_listings` (`[BUSY]`, `[HEXC]`, `[IRLC]`, `[DEAD]`) | Buy wholesale `station_core` (~13M cr at Arneb), auto-buy cheaper listed ships via `upgrades.py` (`37-90%` savings), and exploit verified book spreads | Buy cheap rival surplus & ships below craft/commission cost; sell into deep rival standing bids |
| **8** | **PvE Herd, Pirate Formation Farming & Escorts** | `[BUSY]` (8.5k pirates), `[HEXC]` (2.1k pirates); threat `[ENDL]` | Auto-buy listed T2 combat bargains (`Broadaxe` ~37k, `Recursion` ~224k), fan 1-2/herd across 100+ herds, and run focused 5-8 ship pirate packs | Maintain `WAR_ALERT` posture, strict defensive RoE (F2), Royal Guard escorts, and Neutrality pacts |

---

## 5. Standing Operational Rules & Automated Guardrails

The following system-level guardrails keep the strategy executing smoothly 24/7 between 6-hour
Admiral turns:

- **Anti-Crowding Structural Caps (`dispatch.py`, `fill.py`, `scorecard.py`):**
  - Mining: hard cap **3 ships per belt** (`MINE_POI_CAP = 3`), `FIELD_CONGESTION` alarm at
    `>= 4/6`.
  - Trade Bursars: hard cap **1 ship per station** (`BURSAR_STATION_CAP = 1`, atomic claims in
    `bursar_claims.json`), `HUB_CONGESTION` alarm at `>= 2/4`.
  - Military Hunts: **1-2 ships per herd** (Rule F9), `FIELD_CONGESTION` alarm at `>= 4/8`.
- **Policy-Driven Autonomous Engines (Editable by Admirals):**
  - `game/bursar-policy.json` controls Bursar station priorities, policed vs. safe neutral
    coverage, escrow budgets, unit-price ceilings, reserve protection, and undercut steps.
  - `game/haul-policy.json` controls Hauler safety (`policed_only`), jump caps, minimum
    `cr/jump` & total profit floors, collateral caps, margin floors, partner priority, and lane
    order.
- **One-Purse Wallet, 50-Officer Mesh & Listed-Hull Auto-Buy (`wallet` service, `upgrades.py`):**
  - A dedicated 60s `wallet` shelf service (with `fcntl.flock` mutex) runs parallel direct
    deposits, up to 50 auto-promoted Officers (`>=4/division`), P2P donor fast-path funding, and
    multi-Officer cross-division lockbox withdrawals (`500k` Treasury floor).
  - `upgrades.py` checks `browse_ships` at the target station before commissioning and
    automatically executes `buy_listed_ship` whenever a listed hull beats the commission quote
    (instant delivery, `37-90%` savings), enforces role-matched hull categories, and surfaces
    live `ship_listings` + Exchange T2-T4 module asks (`books`).
- **Watcher & Mining Hygiene Guards:** `routes-index-pass.sh` auto-quarantines stray 0-byte
  root-level shell-redirection files so commits never stall `watch.py`; `routemaker.py` sets a
  `15%` default `min_left` floor on generated mine routes.
- **Drain-Free High-Capacity Runner Host (`runhost.py`):**
  - Sized for 500+ ships with a +20% concurrency buffer (`MAX_RUNS = 600`, `MAX_RSS_MB = 2600`,
    `TOTAL_RSS_MB = 3800`), running `mine`, `hunt`, `circuit`, `census`, `guard`,
    `bursar`, and `haul` as lightweight in-process threads with zero-drop code handovers.

---

## 6. Evolution Roadmap -- How This Standing Plan Will Change

This blueprint intentionally reflects our **500-ship transition into full multi-engine autonomy**.
Expect the following planned evolutions as milestones unlock (tracked live in
`governance/progression-roadmap.md`):

1. **T0/T1 -> T2/T3 Fleet Conversion:** Batch-upgrading all P10+ pilots onto role-matched T2/T3
   hulls (`Recursion`, `Apophenia`, `Workhorse`, `Prayer`/`Ledger`) and T2/T3 modules so
   per-ship extraction, cargo volume, and combat lethality multiply without adding ship count.
2. **Sovereign Station & Tourism Expansion:** Completing the Atria/Yildun outposts, Station Core,
   shipyard/garage berths, and Tourism modules -- shifting recurring income from purely active
   flight toward zero-fuel passive station & tourism cashflow while dismantling rent-paying NPC
   offices.
3. **500 -> 1,000 Ship Scaling Wave:** Once consolidated recurring cashflow is firmly positive and
   T2+ hulls compound, scaling toward the 1,000-ship multi-empire armada with proportional
   expansion across all five empires and deeper lawless scarce-vein & pirate-stronghold wings.
4. **Deeper Neutral Partner Supply Corridors:** Expanding Ch1-Ch4 P2P trade, standing supply
   contracts, and bilateral freight with established Neutral partners while preserving strict
   OpSec and defensive sovereignty.

## Smart 5-Division Autonomous Networks & 5-Empire Regional Hubs (2026-11-24)

- **All 5 Divisions Run Policy-Driven Dynamic Rotation:** Trade (`bursar-network` / `game/bursar-policy.json`, 60+ safe empire + non-pirate neutral hubs staffed by T0 desk ships `max_hull_tier=0, max_cargo=150` while preserving T1/T2/`Cargo Expander II` ships for mobile cargo/crafting), Logistics (`haul-network` / `game/haul-policy.json`, global optimal freight/arb/restock/supply), Intel (`census`, stalest unread system), Mining (`mine-network` / `game/mine-policy.json`, live 15% floor + instant cooldown + tool match + reserve deficit priority), and Military (`hunt-network` / `game/hunt-policy.json`, percentage combat-power gating auto-scaling T0->T5+, on-demand Escort holding 0 ships when clear, 3/5/8/10-ship Packs targeting 25% share for high-tier loot & pirates, and F38 `keep_herd=2` Solo rotation).
- **Medium/Late-Game Regional Storage Hubs (`O4`):** Allocate our 5 faction stations as `1` Voidborn core + `1` dedicated regional storage/hub station in each of the `4` other empire regions (Solarian, Nebula, Crimson, Outer Rim) so every regional wing has local storage, repair, Exchange access, and cross-empire staging.

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
   - **Trade** owns the Exchanges, Bursar desks, market-making, wholesale procurement, and final
     liquidation across all five empires.
   - **Logistics** owns freight, bulk arbitrage hauling, crafting/refining for imperial builds,
     supply-chain fulfillment, and station/outpost construction.
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
  - Allocates central Treasury funds via `wallet.py` (parallel P2P + multi-Officer lockbox
    withdrawals, 500k Treasury floor) toward highest-ROI capex: T2/T3 hulls, T2/T3 modules,
    faction storage lockboxes, outposts, and sovereign Station Cores.
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
  - **Upgrade Ladder:** Fits role-matched `mining_laser_ii/iii`, `ice_harvester`,
    `gas_harvester`, and upgrades P10+ miners onto T2+ industrial hulls (`Workhorse` ->
    `Lithosphere` / `Tellurian` / empire equivalents).
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
  - **Zero-Fuel Docked NPC Factories:** Parks mobile/excess traders permanently docked at public
    NPC refineries/factories crafting high-margin goods at 0 fuel and 0 rent.
  - **Outsupply / Undercut / Outsource:** Feeds deep rival standing bids (gourmet rations,
    refined bars, scarce ore), undercuts inflated rival asks by 5-10%, and buys underpriced
    rival wholesale surplus.
  - **Upgrade Ladder:** Fits cargo expanders and upgrades P10+ traders onto T2+ trade hulls
    (`Apophenia` / empire equivalents).
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
  - **Express Passenger & Bulk Freight Wings (Growth Track):** Scales into dedicated bulk
    freighters (`Prayer` / `Ledger` / `Congregation` / empire equivalents) and fast express
    passenger hulls (`Runner` / `Concordia`) as station transit lounges come online.
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
  - **Scalable Pirate Formation Farming (Rule F27):** Transitions upgraded T2/T3 combat ships
    (`Recursion`, `Broadaxe`, `Dialectic`) into solo and coordinated multi-ship formations
    to farm NPC pirate packs and bounties (`pirates_ok: true`).
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
  - **Rival Intelligence Pipeline:** Feeds `rivals.py` and `governance/rival-sedcards.md` to
    surface >10M/h rival earners, dark zero-base factories, unscanned rival stations, and live
    Outsupply / Outsource / Undercut spreads.
  - **Autonomous Diplomatic Envoy (Rule F4, O10):** Polls envoy inboxes via `diplomacy.py`
    across tracked galactic blocs (11+ blocs / 23+ leaders), coordinates Neutrality & Trade
    pacts with Unity's flagship, enforces strict anti-injection quarantine, and upholds zero
    cross-bloc disclosure.
- **Primary KPIs:** Place & market freshness (`>= 80%` `<3h`), zero scout losses, diplomatic
  reply SLA (`0` unanswered partner threads).

---

## 4. Rival Playbooks Adopted vs. Countered (Our 8-Strategy Matrix)

The Collective continuously benchmarks top galactic factions via `governance/rival-sedcards.md`
and `game/fleet/rival_playbook.py`, copying every proven compounding mechanic while countering
rival bottlenecks:

| # | Strategy Archetype | Proven Rival Benchmark | How The Collective COPIES It | How We COUNTER Rivals |
|:-:|:--|:--|:--|:--|
| **1** | **Sovereign Tourism & Gourmet Hub** | `[BUSY]` The Obsidian Well, `[HEXC]` Hex Star | Command + Logistics build sovereign stations & high-appeal Tourism modules; Trade stocks gourmet food & specialty drinks for zero-fuel passive cashflow | Trade feeds rival Tourism hubs' standing gourmet/drink bids today to capture their cashflow before our own hubs finish |
| **2** | **Zero-Fuel Docked NPC-Facility Factory** | `[MIN9]`, `[BEAT]` (zero bases, millions crafted) | Trade + Logistics run permanently docked zero-fuel crafting + `sell_order` at public NPC refineries/factories | Outbid their raw inputs with Bursar `buy_order` walls and undercut inflated finished asks by 5-10% |
| **3** | **Multi-Hub Exchange Market-Making (Bursar)** | `[NOIR]` (+20.4M/h, 0 bases), `Vex Nebulon` | `bursar.py` stations 1 Trader per hub across 60+ global Exchange books with dynamic `buy_order` + undercut `sell_order` & 2-min live book refresh | Eliminate single-hub congestion and out-cover single-region rivals across all 5 empires simultaneously |
| **4** | **Zero-Base Express Passenger & Courier** | `[NOIR]` (`Runner` / `Concordia`), `LimaTango1428` | Logistics builds a fast express passenger & transit-lounge wing alongside bulk freighters | Compete across all 5 empire corridors where local birth-empire ships start already positioned |
| **5** | **Bulk Freight & Mission Swarm** | `[WEXL]` (`Prayer` / `Congregation`), `[IRLC]` (`Ledger`), `[ENDL]` | `haul.py` automates `spacemolt_shipping` contracts + cross-station arbitrage; high-cargo hulls scale haul EV per jump | Prioritize Neutral partners (+25% score bonus) and reject unprofitable pirate-stronghold traps |
| **6** | **Lawless Scarce-Vein Monopoly Extraction** | `[HEXC]` (11 bases, T3+ miners), `[IRLC]` (32M+ ore) | Mining spreads `<= 3/belt` across scarce high-bid veins with `keep_items` purity filtering and upgrades to T2-T4 mining hulls | Never mine 1-cr rival bulk dumps (buy them wholesale instead); monopolize scarce bottleneck ores |
| **7** | **Wholesale Capital Arbitrage (Outsource & Outsupply)** | Live rival books (`[BUSY]`, `[HEXC]`, `[IRLC]`, `[DEAD]`, `[BEAT]`) | `haul.py` + Trade Bursars systematically exploit verified cross-station spreads and Make-vs-Buy capex outsourcing | Buy cheap rival surplus below internal craft/fuel cost; sell into deep rival standing bids |
| **8** | **PvE Herd, Pirate Formation Farming & Escorts** | `[BUSY]` (8.5k pirates), `[HEXC]` (2.1k pirates); threat `[ENDL]` | Military fans across 100+ PvE herds (1-2/herd) and scales T2/T3 pirate formation hunts (`Recursion`, `Broadaxe`, `Dialectic`) | Maintain `WAR_ALERT` posture, strict defensive RoE (F2), Royal Guard escorts, and Neutrality pacts |

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
- **One-Purse Wallet & Upgrade Automation (`wallet.py`, `upgrades.py`):**
  - Parallel direct deposits and multi-Officer lockbox sweeps pool surplus into the central
    Treasury while `topup_view()` prevents spent upgrade funds from triggering duplicate refills
    and `serve_funds()` handles Officer self-withdrawals cleanly.
  - `upgrades.py` enforces role-matched hull categories (`DIV_HULL_CATEGORIES`) and surfaces
    affordable T2/T3 Exchange modules so divisions skip obsolete T1 swaps where T2/T3 asks exist.
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

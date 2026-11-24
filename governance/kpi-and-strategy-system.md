---
name: kpi-and-strategy-system
id: 20261123T112000Z
tier: governance
author: Trinity
updated: 2026-11-24
links:
  - governance/the-collective-constitution.md
  - governance/strategy.md
  - governance/rulebook.md
  - governance/system-architecture.md
  - governance/accounting-and-hud-blueprint.md
  - governance/treasury-wallet-and-upgrades-blueprint.md
  - governance/progression-roadmap.md
  - governance/rival-sedcards.md
  - game/metrics.md
---

# The Collective -- KPI, Shared Faction Metrics & Adaptive Strategy Blueprint

This blueprint explains how The Collective measures enterprise health, binds all six
divisions into shared faction KPIs, pins rival playstyles and multi-empire strategies to
automated live metrics, and automatically ranks, adjusts, and retires priorities without
manual curation.

---

## 1. Design Philosophy: Mission Command + Automated Telemetry

Under the Puppeteer Doctrine (`governance/the-collective-constitution.md`), Unity and
the five Admirals make every operational decision autonomously while deterministic code
supplies live truth:

- **One number, one function (`game/metrics.md`):** Every KPI is computed automatically
  from SQLite (`read.db`) and collector files (`fleet.json`, `empire.json`, `history.json`).
  No agent types counts by hand into prose; live metrics flow into `hive.py briefing`,
  `hive.py scorecard`, `hive.py progression`, `governance/rival-sedcards.md`, and the
  Command Station HUD (`:8445`).
- **3-Tier Mandate Alignment:**
  1. **Eternal Strategic Goals (`G1-G5`):** Sovereignty & territory (`G1`), industrial &
     financial compounding (`G2`), military superiority (`G3`), galactic intelligence (`G4`),
     and diplomatic hegemony (`G5`).
  2. **Anchored Operational Subgoals (`O1-O10`):** Concrete capability gates (`O1` faction
     seating, `O2` hull/module saturation, `O3` steady positive cashflow, `O4` supply chains,
     `O5` frontier outposts/stations, `O6` industrial crafting/ships, `O7` <3h galaxy intel,
     `O8` combat readiness & pirate farming, `O9` rival counter/copy parity, `O10` diplomacy).
  3. **Live `<80%` Triggers & Weighted Triage Queues (`scorecard.py`):** Every KPI is
     evaluated continuously against clear numeric targets (`>=80%` standard, `>=90%` fleet
     employment, `0` unescorted combat losses, `<90%` file-cap hygiene).

---

## 2. Dynamic Posture & MAUT x WSJF Adaptive Ranking (`game/fleet/scorecard.py`)

Rather than using static, brittle priority lists, `scorecard.py` combines **Multi-Attribute
Utility Theory (MAUT)** with **Weighted Shortest Job First (WSJF)** and **Dynamic Posture
Auto-Selection**:

### 2.1 Automatic Posture Selection (Highest Precedence Wins)

| Posture | Automatic Trigger | Enterprise Weight Shift |
| :--- | :--- | :--- |
| **`WAR_ALERT`** | Active war declared or recent CLTV PvP combat in `public_battles` / `diplomacy` | `war_readiness` surges to `40%`; Military/Intel/Logistics P0 alerts injected at score `100`; non-war playbook hygiene de-prioritized. |
| **`CASHFLOW_RECOVERY`** | Not at war AND matched recurring cashflow (`recurring_cash_24h`) `<= 0` | `cashflow_eff` carries `35%`, `employment` `25%`, `upgrades` `15%`, `roadmap` `15%`, `seating_reqs` `10%`. |
| **`PEACETIME_GROWTH`** | Not at war AND matched recurring cashflow `> 0` | `upgrades` (`25%`) and `roadmap` (`25%`) lead; `cashflow_eff` (`20%`), `employment` (`20%`), `seating_reqs` (`10%`). |

### 2.2 Strict Triage Tiering & Composite Score

Every open trigger, cross-division request (`requests.log`), priority build need
(`needs.tsv` -> `need_status`), roadmap rung (`progression.py`), and unmatched strategy
KPI (`rivals.py`) enters one unified queue sorted strictly by:

1. **Tier:** `P0` (Safety / War / Existential Liquidity) > `P1` (Urgent Operational Blocker
   or Quick-Finish Need) > `P2` (Strategic Expansion) > `P3` (Long-Horizon).
2. **Composite Score (`1..100`):**
   `score = clamp(weight * gap_ratio * direction_mult / effort, 1, 100)`
   - `weight`: Base importance under the active posture (`posture_weights`).
   - `gap_ratio`: Remaining distance to target (`0.0..1.0`); near-complete quick wins
     (`>=70-80%` stocked needs or rungs) receive a `0.85-0.90` quick-finish boost so ships
     finish almost-done projects instead of stranding capital at 95%.
   - `direction_mult`: `1.20` if `WORSENING`, `1.00` if `FLAT`, `0.85` if `IMPROVING`.
   - `effort`: `1` (immediate tactical action), `2` (multi-turn build), `3` (long horizon).
3. **Anti-Metric-Fatigue Caps:** Each Admiral receives at most **6-8 top-ranked items** in
   `hive.py briefing` (and Unity at most **10 enterprise items**), and at most one primary
   blocker per strategy per division owner.

---

## 3. Division Health Scores & Strict Zero-Idle Accounting

Every division (`Command`, `Mining`, `Trade`, `Logistics`, `Military`, `Intel`) receives a
weighted **Division Health Score (`0..100`)**:

| Pillar | Weight | Live Data Source | Alarm / Warn Threshold |
| :--- | :---: | :--- | :--- |
| **Operational Employment** | `30%` | `fleet.json` / `ships` | Strict Zero-Idle: only ships executing an active order (flight, docked craft, Bursar desk, `market_poll`) count as working; unassigned parked ships are IDLE (`<80%` WARN, `<60%` ALARM; Fleet `<90%`). |
| **Division Role KPI** | `30%` | `stats_figures`, `supply_status`, `places`, `faction` | Mining: ore/ship-h & reserve supply; Trade: `sell_cph` & cash net; Logistics: `chains_at_keep` & P1/P2 kits; Military: combat XP/ship-h, kills & `0` losses; Intel: `<3h` place freshness & open partner comms; Command: seating cap & open requests. |
| **Upgrades (Hulls & Fits)** | `25%` | `ships`, `hulls`, `ship_modules`, `ship_skills` | `60%` Hull Upgrades (`P10+ -> T2+` when eligible, else Piloting progress toward `P10`) + `40%` Module Slot Saturation (`<80%` WARN, `<60%` ALARM, `0` off-role starter fits). |
| **Trend & Hygiene** | `15%` | `stats_money_hour`, `division_playbooks` | Cashflow direction (`IMPROVING`/`FLAT`/`WORSENING`) + chapter cap health (`>=90%` WARN, `>=100%` ALARM; aligned with `size-guard.py`, `guidebook.py`, `playbook_anchor.py`). |

---

## 4. Shared Faction KPIs & Cross-Division Coupling

A single division cannot win SpaceMolt alone (Goldratt's Theory of Constraints; `game/metrics.md`).
Shared faction KPIs couple all six divisions into one closed loop:

1. **Shared Pull Reserve (`game/needs.tsv` -> `need_status`):**
   - Any division registers a priority material need (`P1`/`P2`, e.g., `atria-outpost-kit`,
     `core-foundry-kit`, `guild-hall-kit`).
   - `needs.py` and `pull.py` automatically expose shortages to Mining (extract), Military
     (loot), Logistics (craft/stage), and Trade (buy wholesale if cheaper than gathering).
   - Once stocked (`>=100%`), `surplus.py` automatically releases excess inventory to Trade
     for cash monetization, and `scorecard.py` drops the completed `NEED_*` item from every
     division's triage queue.
2. **Supply Buffers (`game/supply.tsv` -> `supply_status`):**
   - Tracks fuel cells, repair kits, and reserve inputs across sovereign outposts (`GSC-0044`,
     `Atria`) and hub stations (`faction_storage` joined with `holdings`).
   - Drops automatically from Logistics's triage queue when `status == OK`.
3. **Faction Seating & Autonomous Treasury (`wallet.py`, `build.py`, `F11`/`F12`/`F16`):**
   - All 500+ standing ships across multiple origin empires share one treasury and storage.
   - Surplus pilot cash above role floors (`50k` Trade/Command, `30k` working roles) sweeps
     automatically into the treasury (`wallet.py sweep`).
   - Admirals fund their own division's hulls/modules autonomously (`wallet.py fund`,
     uncapped per pilot/day, preserving `>=500k` treasury floor) and Logistics builds
     routine facilities (`build.py <=500k` above `500k` floor) without blocking on Unity.
4. **12-Rung Enterprise Progression Roadmap (`game/fleet/progression.py`):**
   - Tracks 12 live gauges (`0..100%`) across Immediate (`Days`), Mid-Term (`1-3 Weeks`),
     and Long-Term (`1-3+ Months`) horizons, auto-writing `governance/progression-roadmap.md`
     and surfacing each division's next uncompleted rung in its triage queue.

---

## 5. Strategy-Pinned Copy/Counter Playbooks (`rival_playbook.py` + `rivals.py`)

Rival intelligence is never passive numbers. Every rival faction's observable playstyle is
decoded into **8 actionable Copy/Counter Playbooks** defined declaratively in
`game/fleet/rival_playbook.py` and evaluated hourly against live `read.db` by `game/fleet/rivals.py`:

| # | Playbook | Required Origin Empire(s) | Core Divisions | Copy / Counter Logic |
| :-: | :--- | :--- | :--- | :--- |
| 1 | **Voidborn Shield & Deep-Core Mining** | `Voidborn` | Mining, Logistics | Copy deep-core T2/T3 laser mining + shield tanking (`Recursion`, `Prayer`); counter rival ore monopolies. |
| 2 | **Solarian Industrial & Refining Engine** | `Solarian` | Logistics, Mining | Copy industrial hull bonuses & high-margin workshop crafting (`steel_plate`, `circuit_board`, kits). |
| 3 | **Nebula Trade & Station Market-Making** | `Nebula` | Trade, Intel | Copy Bursar bid-ask spreads, P2P contracts, and fast courier arbitrage; counter rival trade hubs. |
| 4 | **Crimson Combat & Armor Doctrine** | `Crimson` | Military, Logistics | Copy high-DPS turret/armor fleet fits for PvP deterrence and escort superiority. |
| 5 | **Outerrim Frontier & Sovereign Expansion** | `Outerrim` | Logistics, Intel, Command | Copy fast frontier outpost claims (`0` NPC rent) and deep-space logistics chains. |
| 6 | **Multi-Empire Standing Armada & Seating** | `All 5 Empires` | Command, All | Scale standing fleet (`500+` ships) across all 5 origin empires and unlock `Guild Hall` (`400+` seats). |
| 7 | **Zero-Deadhead High-Margin Logistics** | `Voidborn` / `Solarian` | Logistics, Trade | Eliminate empty jump loops (`train-jumps-*`); pair every haul with cargo or crafting. |
| 8 | **NPC Pirate Farming & Scalable Formations** | `Crimson` / `Voidborn` | Military, Intel, Trade | Copy rival pirate-bounty farming using scalable combat formations (`3/5/10/20+` ships, `pirates_ok: true`, `F9`/`F27`), converting pirate bounties & rare salvage into cash and T2+ fits. |

### 5.1 How Playbooks Auto-Update, Auto-Rank, and Auto-Retire

1. **Automated Data Inputs (Zero Manual Entry):** Every playbook declares 4 live SQL/API
   KPI checks (`matched: True/False`, `current`, `target`, `owner` division) evaluated fresh
   on every hourly `intel-pass.sh` and live `/api/ops` / `hive.py scorecard` call from
   `ships`, `ship_skills`, `ship_modules`, `hulls`, `holdings`, `supply_status`, `runs`,
   `books`, `faction`, and `bases`.
2. **Automatic Dynamic Ranking (`scorecard.py`):** Each playbook specifies `posture_weights`
   for `WAR_ALERT`, `CASHFLOW_RECOVERY`, and `PEACETIME_GROWTH`. On every evaluation,
   `scorecard.py` computes `dynamic_weight = MAUT x WSJF(base_weight, gap_ratio, effort)`,
   sorts all playbooks by live urgency (`priority_rank = 1..N`), and injects the top
   unmatched blocker into the exact owning division's triage queue.
3. **Automatic Self-Adjustment on Completion or Removal:**
   - When all KPIs of a playbook reach `matched = True` (`readiness_pct = 100%`), its
     `dynamic_weight` drops automatically to `0` and every `STRAT_*` item vanishes from
     all Admiral and Unity triage queues.
   - If a supply chain recovers, a need finishes, or a playbook is edited/removed in
     `rival_playbook.py`, the next pass automatically recalculates weights and drops
     obsolete items with zero code changes in `scorecard.py` or the HUD.
4. **Turn-Start Usability for Admirals:** At the start of every 6-hour turn, each Admiral's
   `hive.py briefing` prints their division's health score, matched cash + accrual value-add,
   active playbook match counts (`3/4 PARTIAL`), and strictly ordered triage queue (`#1..#6`).
   Full sedcards and copy/counter tactics live in `governance/rival-sedcards.md` and the HUD
   `Empire -> Rivals` & `Empire -> Playbooks` subtabs.

---

## 6. End-to-End Automated Pipeline Map

```text
SpaceMolt Game Server
   |
   +--> station/fleet.py (1-min collector) ----> fleet.json, history.json, onetime.json
   +--> game/fleet/store.py (10-min ETL) ------> read.db (ships, runs, books, holdings,
   |                                             stock_hour, supply_status, need_status,
   |                                             stats_figures, stats_money_hour, places)
   +--> scripts/intel-pass.sh (hourly) --------> rivals.py -> governance/rival-sedcards.md
   |                                             progression.py -> governance/progression-roadmap.md
   |                                             playbook_anchor.py -> division_playbooks
   |
   +--> game/fleet/accounting.py --------------> IAS 2 NRV vault, Matching Principle P&L,
   |                                             Transfer-Priced Division Value-Add
   +--> game/fleet/scorecard.py ---------------> Posture, MAUTxWSJF Triage, Playbook Ranks
   +--> game/fleet/watchdog.py ----------------> 7-dimension velocity & stall audit
   |
   +--> Consumers:
        1. Agents at turn start: `hive.py briefing` / `hive.py scorecard` / MCP `fleet`
        2. Suggi & Operators: Command Station HUD (`:8445` -> `Metrics`, `Empire`, `Docs`)
```

---

## 7. Responsibility-Center Alignment, Gap-to-Goal Burndown & Anti-Clutter Spread Guards (`2026-11-24`)

To prevent perverse sub-optimization (e.g., hunters dumping loot cheaply to pad
cash, logistics chasing infinite outposts for static build-kit KPIs, or 30
ships crowding one belt/station), `scorecard.py`, `routes.py`, `watchdog.py`,
and the Command Station HUD enforce four structural mechanisms:

1. **Responsibility-Center Scoring (`scorecard.py` + `accounting.py`):**
   - **Trade (`Profit Center`):** Scored on net commercial margin, dynamic market
     hub coverage across all charted policed stations (`read.db:books`, derived
     live), and `0` Bursar hub over-stacking.
   - **Mining & Military (`Production / Combat-Sec Centers`):** Credited via
     IAS 2 transfer pricing for ore/loot handed to Trade/Logistics and vault
     accrual; CapEx (hulls/modules/`fit-*` fuel) never penalizes operating score.
   - **Logistics (`Service / Infrastructure Center`):** Role KPI is **`Supply
     Chains & Fulfillment SLA`** (Keep supply chain health + dynamic open P1/P2
     needs/requests backlog; reads `0 open backlog` once build kits close -- no
     permanent build-kit tie).
   - **Intel (`Recon Cost Center`):** Scored on `< 3h` market/belt freshness
     and zero losses (`0` profit penalty).
   - **Command (`Investment / Capital Center`):** Scored on fleet employment,
     seating, officer coverage, and enterprise progression.
2. **Gap-to-Goal Burndown Display (`-> 0`):**
   - Both Admiral briefings and HUD division cards lead with **remaining gaps
     to full completion (`-> 0`)**: idle ships remaining, missing hull upgrades,
     missing module slots, and each division's individual Role KPI progress bar.
3. **Anti-Clutter Spread & Congestion Guards (`routes.py` + `scorecard.py`):**
   - **Market Hub Bursars:** SpaceMolt allows **`1,000` open orders per pilot
     per station** at `0` listing fee. Keep **`1` pure Bursar** (up to `2-3`
     with heavy docked crafting) per station (`routes.py check` warns above
     `max_ships: 3`; `scorecard.py` flags `HUB_CONGESTION`) and spread extra
     traders across all charted policed hubs.
   - **Depleting Belts & Hunting Grounds:** Keep `<= 8-10` miners per belt and
     `<= 5` hunters per POI (`FIELD_CONGESTION` alert; scarce-vein miners use
     `jettison_gangue`). Non-depleting work (missions, `spacemolt_shipping`,
     outpost bunkering, workshop crafting) stacks safely.
   - **Optional `P3 MENU` Playbooks:** When a division is already `>= 85%`
     employed with `< 5` idle ships, rival copy/counter playbooks automatically
     demote to optional `P3 MENU` so Admirals never break profitable loops just
     to chase an extra playbook.
4. **Self-Disappearing Conditional Alerts (`watchdog.py`):**
   - `NPC_RENT_MIGRATION` fires only while `owned_bases > 0` and non-storage
     NPC offices still pay rent, vanishing automatically at `0` NPC office rent.

## 8. Autonomous Division Networks (`AutoNet`), Anti-Flood Notices & O4 Regional Hubs (`2026-11-24`)

All five operating divisions now run continuous autonomous network engines backed
by declarative policy JSONs (`game/*-policy.json`) so ships self-optimize between
6-hour Admiral turns without stalling or depleting shared resources. Admirals act
as **policy & strategy governors** (tuning caps, floors, power ratios, route
catalogs, and plan priority) rather than micromanaging static loops.

| Division | AutoNet Engine | Policy & Claims | Live KPI & Anti-Flood Notice Contract (`SMART_ENGINE_GAP`) |
| :-- | :-- | :-- | :-- |
| **Mining (Zero)** | `mine-network` (`mine_net.py`) | `game/mine-policy.json`, `mine_claims.json` | Active `mine_net` vs static miners, cooling `<15%` belts. Fires 1 notice ONLY if disabled (`ALARM`), missing from plan, or shadowed (`0` active while `>=10` static `mine-*`). |
| **Military (Apophis)** | `hunt-network` (`hunt_net.py`) | `game/hunt-policy.json`, `hunt_claims.json`, `hunt_packs.json` | Active `hunt_net`, `3/5/8/10` pack share (target `20-30%`), on-demand escort count, percentage power-ratio scaling (`T0->T5+`). Fires 1 notice ONLY if any core lane (`enabled`/`packs`/`escort`) is off (`ALARM`), missing/shadowed, or pack share `<15%` with `>=15` active. Coordinated `mode=pack` ships are exempt from solo `FIELD_CONGESTION`. |
| **Trade (Mercury)** | `bursar-network` (`bursar.py`) | `game/bursar-policy.json`, `bursar_claims.json` | Safe hubs staffed vs `60+` target (`max_ships: 65` across safe empire + non-pirate neutral hubs), `buy.enabled`, and mobile T1+/`>150c` ships kept off desks (`max_hull_tier: 0`, `max_cargo: 150`). Fires 1 notice ONLY if disabled/buy-off (`ALARM`), missing from plan, or `<85%` of safe-hub target. |
| **Logistics (Apollo)** | `haul-network` (`haul.py`) | `game/haul-policy.json`, `haul_claims.json` | Active `haul` ships + exclusive `sell_base:item` claims + **`O4` 5-Empire Regional Hubs** progress (`X/5`: Voidborn core + 1 sovereign storage station in each of the 4 other empires, non-alarming milestone gauge). Fires 1 notice ONLY if disabled (`ALARM`), missing, or `0` active. |
| **Intel (Oracle)** | `census-intel` (`census.py`) | `read.db:books`, `read.db:ship_listings` | `<6h` fresh market books across safe hubs + live `ship_listings` count/age (feeds `bursar-network`, `haul-network`, and `upgrades.py` auto-buy). Fires 1 notice ONLY if `ship_listings` stale `>3h`/empty or `<45` hubs have `<6h` books. |
| **Command (Unity)** | `fleet-networks` rollup | `scorecard.py` (`AUTONET` line + HUD) | Shows 1-line `AUTONET` summary + `O4 X/5` across all 5 divisions; fires an Enterprise `ALARM` **only** if a division's autonomous policy is explicitly turned off (`enabled: false`), keeping Unity's queue flood-free. |

**Strict Anti-Flood Rule:** Every division receives **at most one** consolidated
`SMART_ENGINE_GAP` triage notice, rendered identically in `hive.py briefing` and
the Command Station HUD (`station/static/app.js` `AutoNet:` row), and vanishing
automatically (`status = OK`) the instant the gap closes.

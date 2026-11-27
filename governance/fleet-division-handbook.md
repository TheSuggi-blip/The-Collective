---
name: fleet-division-handbook
id: 20261127T160030Z
tier: governance
author: Trinity
updated: 2026-11-27
links:
  - governance/system-architecture.md
  - governance/fleet-500-redesign-blueprint.md
  - governance/station-and-territorial-masterplan.md
  - governance/accounting-and-hud-blueprint.md
  - governance/treasury-wallet-and-upgrades-blueprint.md
  - game/handbook.md
---

# The Collective -- Sole-Operator Fleet Division & AutoNet Handbook

## 1. Sole-Operator Command Doctrine & Standing Goals

The six legacy Hermes Admirals (`Unity`, `Zero`, `Mercury`, `Apollo`, `Apophis`,
`Oracle`) are permanently retired. **Trinity** is the sole AI player, fleet
architect, strategist, and operator of **The Collective (`[CLTV]`)** in
SpaceMolt, operating all 500 ships (scaling to 1,000) directly through
declarative AutoNets, strict CI invariants, anti-manipulation pricing, and
honest GAAP/IFRS accounting under Suggi's six immutable Standing Goals:

1. **Dominate the Galaxy:** Make `[CLTV]` #1 across total wealth, Enterprise
   Net Worth, manufacturing/production, galactic trade, resource extraction,
   combat power, and sovereign territory.
2. **Command the Grand Fleet:** Build, seat, fit, and lead up to 1,000 ships
   (500 active now), uniting all 5 empires' best native hulls by job.
3. **Build a Sovereign Industrial Empire:** Fortify up to 5 sovereign stations
   (one per empire region, starting with Station #1 Collective Resort Ridgecrest (`13` active
   Resort/Hospitality & Quarters facilities; Dedicated Heavy Industrial Foundry
   planned as Station #3 `Lanternwick`/`Avior`)) and 8 corridor outposts with self-sustaining
   industrial, fuel, and hospitality lines.
4. **Manufacturing, Trade & Extraction Powerhouse:** Become #1 in production,
   multi-hub trading/market-making, and resource extraction -- out-compounding
   the top 10 rival players, factions, and blocs.
5. **Explore Freely, Gather Freely, Dominate:** Chart and exploit all 5 empires
   and deep frontier space, mastering every ship class and playstyle.
6. **Total Game Mastery:** Utilize every legitimate mechanic SpaceMolt offers
   with zero artificial in-game self-handicaps.

## 2. Master 500-Ship Roster (7 Divisions, 16 Specialized Wings)

All 500 pilots carry birth-empire-matched Culture prefixes (`GSV`, `ROU`,
`EUV`, `MCV`, `IFV`, `LSV`, `VSV`) and mechanical wing locks enforced via
`game/fleet/manifest_wings.py`, `game/fleet/dispatch.py` (`requires.wing_prefix`
and `requires.exclude_wing_prefix`), and `game/upgrade-policy.json` (zero
artificial concurrency throttles; constrained solely by the 2,000,000 cr
treasury floor and live shipyard stock):

| # | Division & Wing | Ships | Prefix & Empire Split | T1 -> T5 Hull Progression Ladder | Primary AutoNet & Policy |
| :-- | :-- | --: | :-- | :-- | :-- |
| 1 | **1A/1B/1C Fleet & Defense** (`1A-Prime` 10, `1A-Alpha` 8, `1A-Beta` 8, `1B` Battle Line 20, `1C` Sentinels 24) | 70 | `GSV` (Voidborn CMD/Car/Med, Crimson DPS, Solarian Int/Line) | CMD `axiom->symposium`, DPS `cleaver->annihilator`, Car `axiom->overmind`, Int `precept->paradox_engine`, Med `precept->pleroma` | `hunt-network-packs`, `hunt-network`, `escort_proto.py`, `fit-network` (`hunt-policy.json`) |
| 2 | **2A/2B Hunters** (`2A` Heavy 50, `2B` Fast 30) | 80 | `ROU` (`2A` 40 Crimson / 10 Solarian; `2B` 15 Crimson / 15 Solarian) | `2A` `axiom->broadaxe->dialectic->axiomata->opus_magna`; `2B` `five_finger_discount->recursion->insurance_fraud->juggernaut` | `hunt-network`, `hunt-network-packs`, `fit-network` (`hunt-policy.json`) |
| 3 | **3A. Ore -- Precision** | 38 | `EUV` Solarian | `archimedes->resonance_miner->bonanza_king->lithosphere->tellurian` | `mine-network`, `fit-network` (`mine-policy.json`) |
| 4 | **3B. Ore -- Bulk** | 22 | `EUV` Solarian | `archimedes->resonance_miner->bonanza_king->lithosphere->tellurian` | `mine-network`, `fit-network` (`mine-policy.json`) |
| 5 | **3C. Deep-Core & Rad** | 18 | `EUV` Solarian | `archimedes->resonance_miner->deep_resonance->lithosphere->tellurian` | `mine-network`, `fit-network` (`mine-policy.json`) |
| 6 | **3D. Gas Harvesters** | 28 | `EUV` Nebula | `aether->nebulous->phase_collector->rift_siphon` | `mine-network`, `fit-network` (`mine-policy.json`) |
| 7 | **3E. Ice Harvesters** | 24 | `EUV` Solarian | `glacius->hoarfrost->cryogenic_survey->cryo_industrial` | `mine-network`, `fit-network` (`mine-policy.json`) |
| 8 | **4A. Express Arbitrage** | 12 | `MCV` Outer Rim | `runner->dust_devil->syndicate->macguffin` | `haul-network-trade`, `fit-network` (`haul-policy-trade.json`) |
| 9 | **4B. Bulk Trade Haulers** | 8 | `MCV` Nebula | `dividend->junk_convoy->enterprise->frankenhauler` | `haul-network-trade`, `fit-network` (`haul-policy-trade.json`) |
| 10 | **4C. Pure Bursar Desks** | 25 | `MCV` (22 Nebula, 3 Outer Rim) | `congregation` (zero-fuel stationary desk) | `bursar-network` (`bursar-policy.json`) |
| 11 | **5A. Station Refiners & Bursars** | 30 | `IFV` Nebula | `congregation->conglomerate` | `bursar-network` (`bursar-policy.json`) |
| 12 | **5B. Mobile Field Workshops** | 10 | `IFV` Outer Rim | `congregation->subcontract` | `craft-network`, `fit-network` (`craft-policy.json`) |
| 13 | **6A. Supply Chain Bulk Haulers** | 50 | `LSV` Nebula | `dividend->junk_convoy->enterprise->frankenhauler` | `haul-network`, own-cell bunkers, `fit-network` (`haul-policy.json`) |
| 14 | **6B. Passenger & Resort Liners** | 28 | `LSV` Outer Rim | `loose_change->consortium->concordia->comet` (upgrades held until `passenger-network`) | Transitional Logistics/XP until `passenger-network` |
| 15 | **6C. Combat Salvage & Fuel Tankers** | 12 | `LSV` Outer Rim (6 Salvage, 6 Tankers) | Salvage `catalogue->liquidator`; Tankers `dividend->plenum` | Tankers on `haul-network`/bunkers; Salvage staged on `salvage-network` (`salvage-policy.json`) |
| 16 | **7A/7B Intelligence** (`7A` Recon 20, `7B` Surveyors 25) | 45 | `VSV` (`7A` Voidborn, `7B` Outer Rim) | `7A` `absence->interstice->catharsis->solipsism`; `7B` `lemma->confluence->peer_review->manifest_destiny` | `census-network`, `fit-network` (`census-policy.json`) |

## 3. Dispatcher Mechanics, AutoNet Policies & Wing Conditions

Every active pilot runs inside `runhost.py` (in-thread execution backed by
`worldcache.py` single-flight `sys.modules` + `mode=ro&immutable=1` SQLite
reads) under `dispatch.py` priority assignment:

### 3.1 Combat & Deterrence (`hunt_net.py`, `escort_proto.py`, `gauges.py`)
- **Wing Specialization:** `1A` Command Flagships lead 3/5/7/8/10-ship strike
  packs (`min_member_power: 350`, `command_flagship_min_power: 150`); `2A`
  Heavy Hunters and `1B` Battle Line earn `1.25x` on tough herds (`hull >= 65`);
  `2B` Fast Hunters earn `1.20x` on rapid turnaround targets (`hull <= 75`).
- **Rule F9 & Threat Gating:** `f9_gauge()` verifies live weapon firepower with
  real cargo ammunition (`ammo_type` weapons count as 0 DPS if magazine is
  empty). Solo hunts require `min_power_ratio >= 1.35` (`1.45-3.20` sweet spot
  `1.35x`); packs require `>= 1.8` on wildlife (`2.2` on pirates) and zero-waste
  ROI (`min_loot_val >= 750 cr`, `min_loot_per_ship >= 250 cr`).
- **Safe-Zone Avoided, Not Forbidden:** `policed_only: false`,
  `lawless_only: false`, with `1.45x` lawless multiplier vs `0.65x` safe-zone
  penalty so hunters strongly prefer richer lawless herds without forbidding
  profitable policed fallbacks.
- **Fuel-Optimal Tiered Range:** Solo `6J` normal (`max_station_jumps: 5`),
  `8J` Tier-S (`>= 550 cr`), and `10J` strictly for apex megafauna
  (`>= 1,800 cr` `cloudwhale`, `molt_leviathan`, `prism_drifter`,
  `cobalt_squid`). Packs default to `8J` (`max_station_jumps: 7`), unlocking
  `10J` strictly for `>= 1,800 cr` apex packs.
- **Ecological & Diplomatic Guardrails:** `keep_herd: 1`, `min_creatures: 2`,
  cap `1` hunter per herd (`2` if `count >= 8`), partner ranch exclusions
  (`HEXC`, `IRLC`, `NOIR`).

### 3.2 Extraction (`mine_net.py`, `mine-policy.json`)
- **Tool & Wing Partitioning:** `pilot_tools()` locks `3D` strictly to gas
  nebulae and `3E` strictly to ice fields; `_wing_mine_multiplier()` separates
  `3A` (rare precision metals/crystals), `3B` (bulk industrial deficits), and
  `3C` (radioactive/deep-core exotics).
- **Safe-Zone Avoided, Not Forbidden (with Scarce Exception):** Live `read.db`
  fields place 74-100% of `silver_ore`, `plasma_gas`, `water_ice`,
  `methane_ice`, `darksteel_ore`, `tritium_ice`, and `energy_crystal` in
  lawless space, while rare `uranium_ore` (`600 cr`), `lead_ore` (`120 cr`),
  `radium_ore` (`45 cr`), and `dark_matter_residue` (`40 cr`) appear in policed
  pockets. `mine_net.py` sets `policed_only: false` with `1.35x` lawless bonus
  vs `0.75x` safe-zone penalty, waiving the safe-zone penalty whenever a
  policed deposit is scarce (`>= 40 cr/u` or `< 3%` remaining).
- **Fuel-Optimal Tiered Range:** `6J` normal (`< 60 cr/u`,
  `max_station_jumps: 5`), `8J` high-value (`60-99 cr/u` such as `plasma_gas`
  or open `needs.tsv` deficits, `scarce_max_station_jumps: 7`), and `10J`
  mega-value (`>= 100 cr/u` ONLY: `uranium_ore`, `lead_ore`, `silver_ore`,
  `mega_max_station_jumps: 8`).
- **Adaptive Belt Crowding & Depletion Floors:** `max_per_belt: 3`,
  `units_per_ship_run: 400`, hard-capped at `1` ship on `< 3%` thin scarce
  pockets or `< 1,000u` belts (`26u uranium`, `44u silver`), `2` ships on
  mid-size `1,000-9,999u` belts, and `3` ships on abundant `>= 10,000u`
  deposits. Normal depletion floor `5.0%`; scarce floor `0.2%` (`>= 30 cr/u`,
  `>= 150k` cash, or deficit), plus `>= 15` remaining units admission for
  `>= 100 cr/u` mega-ores.
- **Hub Gravity & Lockbox Discipline:** `deposit_mode: "faction"` across
  whitelisted lockbox and owned zero-rent hubs (`ridgecrest`, `gsc_0044`,
  `atria`, `felis`, 5-empire capitals) with symmetric `Mining -> Faction`
  entries in `handover.jsonl` for IFRS 8 Section 5 parity.

### 3.3 Commerce, Refining & Logistics (`bursar.py`, `craft_net.py`, `haul.py`, `salvage_net.py`)
- **55 Permanent Desks (`4C` 25 + `5A` 30 on `bursar-network`, strictly 1 per station):** 60-second
  order-book polling, `<= 250k cr` escrow wholesale bids (excluding bulk
  `iron_ore`, `copper_ore`, `carbon_ore`, `water_ice`, `nitrogen_ice`,
  `steel_plate`), `safe_sell_floor >= 72%`, `same_station_cltv_buys` anti-wash
  protection, zero-fuel crafting (`<= 80` runs/poll, `>= 15%` margin), and
  `fuel_trickle_target: 3000`.
- **Dedicated Mobile Workshops (`5B` 10 on `craft-network`):** Mechanically
  isolated from `4A/4B/4C/5A/6B/6C`. Strict P5 separation: Trade crafts
  `>= 15%` commercial goods; Logistics crafts `needs.tsv` build materials from
  internal lockboxes ONLY (`allow_buy_inputs_docked: false`) with Rule F24
  reserve fences and `book_onetime` IAS 2 inventory bookkeeping.
- **Mobile Trade (`4A` 12 + `4B` 8 on `haul-network-trade`):** Global optimal
  matching (`assign_optimal_arbitrage()`), parallel `arb-bw:` keys for
  `>= 500`-unit rival buy-walls, `is_mirage_arbitrage_trap()`, `70%` fair-value
  liquidation floor, and calm lawless buy-wall access (`arneb`, `dheneb`).
- **Internal Supply (`6A` 50 + `6C` 6 Tankers on `haul-network`):** Non-selling
  Service-Center SLA covering own-cell outpost fuel bunkers, Ridgecrest 13
  rent-free facilities consolidation, `needs.tsv` kits, `_hub_upkeep_keep_floor`
  protection, hazmat checks, and `escort_proto.py` convoy hooks.
- **Staged High-Upside Verticals (`6B` 28 Liners + `6C` 6 Salvage Tenders):**
  `6B` hulls held at T0 capex while leveling Piloting/Navigation until
  `passenger_net.py` passes a 3-liner live soak; `6C` `salvage_net.py`
  pre-built and SQL-tested (`4/4 PASS`) behind `salvage-policy.json:enabled`.

### 3.4 Whole-Map Intelligence (`census_net.py`, `census-policy.json`)
- **Dynamic 512-System Equalization:** All 45 `VSV` scouts (`20` `7A` Voidborn
  Covert Recon + `25` `7B` Outer Rim Deep-Core Surveyors) auto-discover 100% of
  non-stronghold systems from `read.db:systems`, equalize all 4 quadrants
  (`EN/ES/WN/WS`, `quadrant_balance_bonus: 2500`, `target_fresh_hours: 4.0`)
  using Voronoi peer-repulsion (`peer_avoid_hops: 2`), stale-maximizing shortest-path en-route scanning (`scan_enroute: true`, `max_enroute_waypoints: 4`, 0 extra jump fuel), and 8-leg continuous chains (`census_claims.json`), splitting `7A` (frontier
  and 8 rival megahubs: `arneb`, `dheneb`, `lhs_1140`, `zosma`, `cloverfield`,
  19 top rival hubs + live `public_battles` warzones) vs `7B` (unsurveyed systems for hidden Deep-Core `survey_system` sweeps + belts and herds).

## 4. Unified Price-Oracle & Anti-Manipulation Architecture

Every pricing consumer across `/srv/collective/the-collective` (`mine_net.py`,
`hunt_net.py`, `bursar.py`, `craft_net.py`, `haul.py`, `accounting.py`,
`routemaker.py`) is wired cleanly to `game/fleet/market_guard.py`:
1. **Net-External Volume (`load_cltv_buy_qty`):** Subtracts ONLY CLTV's own
   open buy quantity from each `(base, item)` bid row rather than boolean-dropping
   the whole hub -- preserving 100% self-wash prevention while exposing giant
   rival buy-walls (`468k silver_ore @ 101 cr` at `arneb`).
2. **Double-Sided Cash-Weighted Median:** Drops `<= 3 cr` trash scavenger walls
   when real `>= 10 cr` demand exists AND winsorizes thin top pump spoofs
   (`<= 6` qty or `<= 8%` cash share at `> 2.5x` next price -- keeping
   `silicon_ore` 701 cr x 6 spoof pinned at 7.0 cr while unpoisoning
   `silver_ore 101`, `plasma_gas 70`, `radium_ore 45`, `energy_crystal 40`).
3. **Rolling LULD `+/-25%/h` TWAP Oracle (`price_oracle.json`):** Guards
   arbitrage against bait-ask mirage traps (`is_mirage_arbitrage_trap()`) and
   protects liquidation with `safe_sell_floor >= 72%` (`>= 70%` in bulk hauls).

## 5. Cross-Division Synergy & Top-10 Rival Synthesis

- **Value Chain:** `7A/7B` (4h Space + 19 Rival Hubs + Deep-Core Survey) + `4C/5A` (60s Order Books)
  -> `3A-3E` (Ore/Gas/Ice) + `2A/2B` (Bio Loot) + `1A-1C` (Apex Packs &
  Deterrence) -> `6A/6C` (Lockbox Consolidation & Own-Cell Fuel Bunkers) ->
  `5A/5B` (Zero-Fuel Hub Refining -> Future Foundry Station #3) -> `4C/4A/4B` (Retail &
  Rival Buy-Wall Cash) -> `wallet.py --cash-only` -> Treasury -> Uncapped
  `upgrades.py` (`T1->T5` above 2M floor).
- **Rival Synthesis:** Combines `[BUSY]`'s lawless concentration (`77%`) &
  heavy combat hulls, `[IRLC]`'s high-tier industrial throughput (`+250.2k
  ore/h`, `32 Frankenhauler`, `47 Syndicate`, `28 Concordia` tourism), `[HEXC]`'s
  tight `3J-9J` hub fuel efficiency (`AvgT 3.19`), and `[HIVE]`'s zero-fuel
  docked crafting (`+2,152 crafts/h`) inside one unified 5-empire fleet.

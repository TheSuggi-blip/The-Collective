---
name: fleet-500-redesign-blueprint
id: 20261126T165520Z
tier: strategy
author: Trinity
links: [governance/birth-plans.md, governance/strategy.md, governance/empire.md]
---

# fleet-500-redesign-blueprint.md -- Approved 500-Ship Job-Based Min-Max Fleet Blueprint

Status: **APPROVED BLUEPRINT (Ready for Pre-Flight Code Prep; zero births or fund transfers executed until Wave 1 cutover begins).**
Last Updated: 2026-11-26 | Catalog: `0.734.6.json` | Live Audit: `read.db` + `pilots.json`.

## 1. Strategic Architecture & Operating Model

* **Direct Command (No LLM Admirals):** Fleet operations transition from 6 Hermes Admiral runners (`the-collective-runner-1`, `5.84 GiB` RAM / `277%` CPU) to direct Suggi + Trinity governance driving deterministic AutoNet code.
* **Preserve All 10 Command Ships & All Faction Assets:** `Prime Directive` remains `[CLTV]` Faction Leader alongside our 9 other named Command ships (`Crimson Aegis`, `Golden Chariot`, `Hades`, `Mercurys Ledger`, `Nebula Charter`, `Rimward Pact`, `Solar Mandate`, `Vision`, `Zero Point`), spanning all 5 empires (`6` Voidborn, `1` Crimson, `1` Solarian, `1` Nebula, `1` Outer Rim). All 3 Sovereign Outposts (`Atria`, `Felis`, `GSC-0044`), 19 facilities, faction storage, and treasury belong to `[CLTV]` and remain 100% intact.
* **99%-Peacetime Active Combat Doctrine:** All `150` combat ships (`70` `Fleet & Defense` + `80` `Hunters`) stay active in peacetime (`80` `ROU` Hunters run high-ROI wildlife/pirate hunts; `46` `GSV` Vanguard & Battle Line run Pirate Stronghold raids & boss packs; `24` `GSV` Sentinels clear local Outpost system pirates). In wartime, all `150` unite as one armada.
* **Zero-Fuel Crafter-Bursar Hybrid:** `30` `IFV` Station Crafter-Bursars sit docked 24/7 at the 30 top Capital/Industrial stations doing BOTH refining/crafting (multiplying raw ore 2-5x) AND local Bursar order-flipping, paired with `25` `MCV` Pure Bursars (`55` stations covered continuously, zero fuel burn!). `20` `MCV` Mobile Arbitrage Traders remain under `Traders & Bursars` because they trade external market spreads on capital rather than internal supply chains.
* **Cross-Empire Min-Max Rules (`game/rules/05-galaxy.md` + `0.734.6.json`):**
  * Birth passives apply to **any** hull flown (`Solarian` +3% all five incl. mining yield; `Nebula` +10% cargo + `nebula_attunement` +1%/lvl gas yield; `Voidborn` +12% max shield + cloak/energy skill; `Crimson` +8% weapon dmg + armor bypass skill; `Outer Rim` +10% in-system speed + salvage/repair skill).
  * T0-T4 hulls have `required_reputation = 0` and zero empire flying lock. T5 hulls require `piloting = 50` and `required_reputation = 60` to commission (non-prestige T5 hulls transfer via Faction Ship Garage).
  * Gas and Ice Harvesters **SKIP T4 completely** (`T2 -> T3 -> T5`) because all 10 T4 Gas/Ice hulls are `Refinery` class with `inherent_capabilities = None`. Ore and Deep-Core/Rad keep full `T2 -> T3 -> T4 -> T5`.

## 2. Official Ship Naming Registry (Culture Prefix + Unique Mythic/Poetic Name)

Every new ship gets a **3-letter Culture-style hull prefix** (cleanly parsed by `division.py` and the HUD) paired with a **100% unique, non-obvious mythic or poetic proper name** (zero numbers, zero role giveaways like `Miner` or `Medic` to rival scanners). The 10 kept Command ships keep their original legendary names.

| Division | Registry Prefix | Expansion | Ships | Example Ship Names |
| :--- | :---: | :--- | :---: | :--- |
| **Fleet & Defense** | **`GSV`** | General Systems Vessel | `60` new (+`10` kept Cmd) | `GSV Hyperion`, `GSV Iron Axiom`, `GSV Nemesis`, `GSV Caliban` |
| **Hunters** | **`ROU`** | Rapid Offensive Unit | `80` new | `ROU Kestrel`, `ROU Peregrine`, `ROU Cold Ember`, `ROU Glass Fang` |
| **Miners** | **`EUV`** | Extraction Utility Vessel | `130` new | `EUV Obsidian`, `EUV Basalt Choir`, `EUV Borealis`, `EUV Zircon` |
| **Traders & Bursars** | **`MCV`** | Merchant Commerce Vessel | `45` new | `MCV Samarkand`, `MCV Gold Current`, `MCV Petra`, `MCV Aurelia` |
| **Crafters & Refiners** | **`IFV`** | Industrial Forge Vessel | `40` new | `IFV Daedalus`, `IFV Star Anvil`, `IFV Vulcan`, `IFV Crucible Dawn` |
| **Logistics** | **`LSV`** | Logistics Systems Vessel | `90` new | `LSV Mistral`, `LSV Atlas Bridge`, `LSV Zephyr`, `LSV Aether Drift` |
| **Intel** | **`VSV`** | Veiled Survey Vessel | `45` new | `VSV Vespera`, `VSV Night Whisper`, `VSV Cassiopeia`, `VSV Umbra` |

## 3. Master 500-Ship Job-Based Roster Table (7 Divisions, 14 Sub-Sections)

| # | Job Division (Prefix) | Sub-Sections (Wings) | Ships | Birth Empire (`10` Kept + `490` New) | Optimal T2 -> T3 -> T4 -> T5 Hull Ladder | Optimal Core Module Doctrine |
| :-: | :--- | :--- | :---: | :--- | :--- | :--- |
| **1** | **Fleet & Defense (`GSV`)** | **1A. 3 Command Task Forces (`8+8+10 = 26`)**<br>- TF Alpha (`8`): 3 Cmd, 2 DPS, 1 Carrier, 1 Interdictor, 1 Medic<br>- TF Beta (`8`): 3 Cmd, 2 DPS, 1 Carrier, 1 Interdictor, 1 Medic<br>- TF Prime (`10`): 4 Cmd (`Prime Directive`), 3 DPS, 1 Carrier, 1 Interdictor, 1 Medic<br>**1B. Grand Battle Line (`20`)**<br>**1C. Outpost Sentinels & Support (`24`)** *(12 Tanks/Carriers, 6 Interdictors, 6 Medics)* | **`70`** | **10 Kept Cmd** (`6` VB, `1` Crim, `1` Sol, `1` Neb, `1` Rim)<br>**+60 New:**<br>`21` Crimson (+8% dmg)<br>`24` Voidborn (+12% shld)<br>`15` Solarian (+3% all/acc) | **Cmd (10):** `theorem` -> `concordance` -> `consensus`/`overlord` -> `symposium`/`ascendancy`<br>**Line DPS (27):** `broadaxe` -> `dialectic` -> `axiomata`/`crimson_devastator` -> `opus_magna`/`annihilator`<br>**Tanks/Carriers (15):** `dualism` -> `gestalt`/`annihilation` -> `superposition`/`voidborn_event_horizon` -> `overmind`/`apotheosis`<br>**Interdictors (9):** `penumbra` -> `aporia` -> `paradox_engine`<br>**Medics (9):** `anamnesis`/`triage` -> `remedy` -> `panacea`/`cauterizer` -> `pleroma` | **DPS:** `railgun_ii` -> `plasma_cannon_iv` / `siege_railgun` + `tracking_computer_iii` + `adaptive_shield_iii` / `hull_reinforcement_iii` + `damage_control_system` + `fuel_optimizer`<br>**Carrier:** `3x advanced_drone_bay` + `flak_cannon_ii`<br>**Interdictor:** `warp_disruptor` + `stasis_webifier_ii`<br>**Medic:** `3x remote_armor_repairer_iii` + `repair_arm` |
| **2** | **Hunters (`ROU`)** | **2A. Heavy Pirate Hunters (`50`)**<br>**2B. Fast Wildlife & Raiders (`30`)** | **`80`** | `55` Crimson (+8% dmg)<br>`25` Solarian (+3% all/acc) | **Heavy (50):** `broadaxe` -> `dialectic`/`warmaul` -> `axiomata`/`crimson_devastator` -> `opus_magna`<br>**Fast (30):** `recursion`/`junkyard_dog` -> `insurance_fraud` (Spd 4, +25% fuel eff.) -> `juggernaut` (Spd 4, W6) | `railgun_ii` / `plasma_cannon_iv` + `tracking_computer_ii/iii` + `fuel_optimizer` + `shield_booster_iii` / `armor_repairer_iii` (NO Afterburners) |
| **3** | **Miners (`EUV`)** | **3A. Ore -- Precision (`38`)**<br>**3B. Ore -- Bulk (`22`)**<br>**3C. Deep-Core & Rad (`18`)**<br>**3D. Gas Harvesters (`28`)**<br>**3E. Ice Harvesters (`24`)** | **`130`** | `102` Solarian (+3% yield/cargo -> Ore/Rad/Ice)<br>`28` Nebula (+10% cargo + `nebula_attunement` -> Gas) | **Ore/Rad (78):** `resonance_miner` -> `bonanza_king` (`deep_resonance` Rad) -> `lithosphere` -> `tellurian`<br>**Gas (28):** `nebulous` -> `phase_collector` -> **SKIP T4** -> `rift_siphon`<br>**Ice (24):** `hoarfrost` -> `cryogenic_survey` -> **SKIP T4** -> `cryo_industrial` | **Prec-Ore:** `modulated_mining_laser` (`prec 0.5`) + `electromagnetic_refinery` + `fuel_optimizer`<br>**Bulk-Ore:** `hyper_mining_laser_iii` -> `mining_laser_iv/v` + `electromagnetic_refinery` + `cargo_expander_iii`<br>**Rad/DC:** `rad_harvester_iii/iv` + `deep_core_extractor_mk_i/ii/iii (`deep_core_extractor_mk_i`, `deep_core_extractor_ii`, `deep_core_extractor_iii`)` + `radiation_baffles_ii/iii`<br>**Gas/Ice:** `gas/ice_harvester_iii/iv` + `fuel_optimizer` + `cargo_expander_iii` (NEVER `strip_miner`) |
| **4** | **Traders & Bursars (`MCV`)** | **4A. Express Arbitrage (`12`)**<br>**4B. Bulk Trade Haulers (`8`)**<br>**4C. Pure Bursar Desks (`25`)** | **`45`** | `30` Nebula (+10% cargo, 3% tax)<br>`15` Outer Rim (+10% speed, 1.5% tax) | **Express (12):** `futures`/`dust_devil` -> `syndicate` (Spd 5) -> `macguffin` (Spd 6, +40% fuel eff.)<br>**Bulk (8):** `junk_convoy` -> `enterprise` -> `frankenhauler` (C2640 -> 2904 w/ Neb)<br>**Pure Bursars (25):** Cheap zero-fuel docked hulls (`floor_price` / `congregation`) | Mobile: `cargo_expander_iii` + `fuel_optimizer` + `expanded_fuel_tank` + `shield_booster_iii`. Bursars: `cargo_expander_iii` only (0 fuel). |
| **5** | **Crafters & Refiners (`IFV`)** | **5A. Station Refiners & Bursars (`30`, hybrid!)**<br>**5B. Mobile Field Workshops (`10`)** | **`40`** | `30` Nebula (+10% cargo, 3% tax)<br>`10` Outer Rim (1.5% lowest tax) | **Docked Hybrid (30):** Cheap high-cargo T1 `congregation` (C1900 -> 2090, 0 fuel!) -> T4 `conglomerate` (C2400 -> 2640)<br>**Field Workshops (10):** T3 `subcontract` (C720, `field_workshop`) / `praxis` (U7, `field_workshop`) | Docked: `cargo_expander_iii` only. Field Workshops: `compact_*` refiners + `shield_booster_iii` |
| **6** | **Logistics (`LSV`)** | **6A. Supply Chain Bulk Haulers (`50`)**<br>**6B. Passenger & Resort Liners (`28`)**<br>**6C. Fuel & Salvage Tenders (`12`: 6 Tank / 6 Salv)** | **`90`** | `50` Nebula (+10% cargo -> Haulers)<br>`40` Outer Rim (+10% speed -> Liners/Tankers + `outer_rim_survival` -> Salvagers) | **Haulers (50):** `prayer`/`congregation` -> `junk_convoy`/`war_wagon` -> `enterprise` -> `frankenhauler`/`conglomerate`<br>**Liners (28):** `consortium`/`omnibus` -> `concordia` (Spd 6) & `ambrosia` (16 1st berths) -> `comet` (Spd 6, 48 1st berths, +50% fuel eff.) & `premiere`<br>**Tankers (6):** `long_haul` -> `reserve` -> `plenum`/`endowment` (12k fuel)<br>**Salvagers (6):** `chop_shop` -> `dissolution` -> `liquidator`/`thermodynamic_end` | **Haulers:** `cargo_expander_iii` + `fuel_optimizer` + shields<br>**Liners:** `fuel_optimizer` + `expanded_fuel_tank` + `phase_cloaking_device`<br>**Tankers:** `refueling_pump` + `fuel_optimizer`<br>**Salvagers:** `salvage_module` + `outer_rim_salvage_array` + `tractor_beam` + `cargo_expander_iii` |
| **7** | **Intel (`VSV`)** | **7A. Covert Recon (`20`)**<br>**7B. Deep-Core Surveyors (`25`)** | **`45`** | `20` Voidborn (+12% shld + `voidborn_mastery` cloak)<br>`25` Outer Rim (+10% speed) | **Recon (20):** `absence` -> `interstice`/`dust_devil` -> `catharsis` -> `solipsism` (Spd 5, cloak 60)<br>**Surveyors (25):** `eigenstate`/`lemma` -> `confluence`/`prospectus` -> `peer_review` (+60% fuel eff., survey 40) -> `manifest_destiny` | **Recon:** `phase_cloaking_device` (cloak 95) + `ship_scanner_iii` + `fuel_optimizer`<br>**Surveyors:** `deep_core_survey_scanner` + `phase_cloaking_device` + `fuel_optimizer` + `ship_scanner_iii` |

## 3B. Verified T1 Bridge Blueprint (`0.735.1` Catalog, All `Piloting 0`, Wing-Locked)

Every wing in `game/fleet-500-manifest.tsv` (`target_t1`) and `game/upgrade-policy.json` is locked to its #1 non-prestige T1 champion (strict rung priority -- never random cheapest; buys used `ship_listings` bargain of the exact target hull first, else commissions at that hull's policed empire shipyard). `game/fit-policy.json` enforces `min_tier: 1` on upgrading wings so zero modules are wasted on disposable T0 starters before the T1 switch (`Intel` starters fit `fuel_optimizer` immediately at `min_tier: 0`).

| Division | Wing (`Ships`) | T1 Champion (`Live Quote`, Shipyard) | Verified T1 Modules (`100%` CPU/PWR Fit) | Smart Income Engine Rollout |
| :--- | :--- | :--- | :--- | :---: |
| **Miners (`130`)** | `3A. Ore -- Precision (38)` | `archimedes` (`35.9k`, Solarian `U4`, `+20%` ore) | `modulated_mining_laser` + `mining_laser_ii` + `fuel_optimizer` + `cargo_expander_ii` + `shield_booster_i` | **ENABLED NOW** |
| **Miners** | `3B. Ore -- Bulk (22)` | `archimedes` (`35.9k`, Solarian `U4`, `+20%` ore) | `mining_laser_iii` + `mining_laser_ii` + `cargo_expander_iii` + `fuel_optimizer` + `shield_booster_i` | **ENABLED NOW** |
| **Miners** | `3C. Deep-Core & Rad (18)` | `archimedes` (`35.9k`, Solarian `U4`, `+20%` ore) | `rad_harvester_ii/i` + `mining_laser_ii` + `cargo_expander_iii` + `fuel_optimizer` + `shield_booster_i` | **ENABLED NOW** |
| **Miners** | `3D. Gas Harvesters (28)` | `aether` (`39.5k`, Solarian `U3`, `+35%` gas) | `gas_harvester_iii` + `cargo_expander_iii` + `fuel_optimizer` + `shield_booster_i` | **ENABLED NOW** |
| **Miners** | `3E. Ice Harvesters (24)` | `glacius` (`32.3k`, Solarian `U3`, `+20%` ice, `160` fuel) | `ice_harvester_iii` + `cargo_expander_iii` + `fuel_optimizer` + `shield_booster_i` | **ENABLED NOW** |
| **Hunters (`80`)** | `2A. Heavy Pirate Hunters (50)` | `axiom` (`42.7k`, Solarian `W2 D1 U2`, `120/75` HP) | `railgun_ii` + `plasma_cannon_ii` + `shield_booster_i` + `fuel_optimizer` | **ENABLED NOW** |
| **Hunters** | `2B. Fast Wildlife & Raiders (30)` | `five_finger_discount` (`34.5k`, Outer Rim `Spd 5`, `80` crg) | `plasma_cannon_ii` + `pulse_laser_ii` + `shield_booster_i` + `fuel_optimizer` | **ENABLED NOW** |
| **Traders (`45`)** | `4A. Express Arbitrage (12)` | `runner` (`42.8k`, Neutral `Spd 6`, `120->220` crg, `+30%` fuel) | `cargo_expander_iii` + `fuel_optimizer` | **ENABLED NOW** |
| **Traders** | `4B. Bulk Trade Haulers (8)` | `dividend` (`27.5k`, Nebula shielded `110/55`, `220->420` crg) | `2x cargo_expander_iii` + `shield_booster_i` | **ENABLED NOW** |
| **Traders & Crafters** | `4C (25)` / `5A (30)` / `5B (10)` | `congregation` (`25.5k`, Outer Rim docked `1,900` crg, `0` fuel) | *(0 slots -- permanent docked Bursar/Refiner hull)* | **ENABLED NOW** |
| **Logistics (`90`)** | `6A. Supply Chain Haulers (50)` | `dividend` (`27.5k`, Nebula shielded `110/55`, `220->420` crg) | `2x cargo_expander_iii` + `shield_booster_i` | **ENABLED NOW** |
| **Logistics** | `6C. Combat Salvage Tenders (6)` | `catalogue` (`29.9k`, Solarian `W1 D1 U4`, `100->300` crg) | `salvage_module` + `2x cargo_expander_iii` + `fuel_optimizer` + `shield_booster_i` | **ENABLED NOW** |
| **Logistics** | `6C. Fleet Fuel Tankers (6)` | `dividend` (`27.5k`, Nebula shielded `160` fuel, `D1 U2`) | `refueling_pump` + `expanded_fuel_tank` + `shield_booster_i` | **ENABLED NOW** |
| **Logistics** | `6B. Passenger Liners (28)` | `loose_change` (`26.0k`, Outer Rim `Spd 5`, 4 berths) | `fuel_optimizer` + `expanded_fuel_tank` | PLANNED (Hold) |
| **Fleet & Defense (`70`)** | `1A (26)` / `1B (20)` / `1C (24)` | DPS `cleaver` (`46.6k`) / Carrier `paradox` (`113.4k`) / EWAR `apeiron` (`125.8k`) / Medic `vigil` (`124.7k`) | Role-matched combat/drone/ewar/medic fits | PLANNED (Wait T2) |
| **Intel (`45`)** | `7A (20)` / `7B (25)` | `7A` `absence` (`84.6k`, cloak 30; `33k-46k` used) / `7B` `lemma` (`27.3k`, Sol `Spd 5`, `U3`, `survey 15`) | `cloaking_device_i` + `ship_scanner_ii` / `survey_scanner_i` + `fuel_optimizer` + `shield_booster_i` | **ENABLED NOW** |

*Excluded prestige-locked hulls:* `ledger` (`Syndicate` achievement) and `workhorse` (`Lean Operation` achievement) are excluded across all policies.

## 4. Consolidated 500-Ship Birth Empire Summary

| Birth Empire | Kept Command (`10`) | New Optimal Births (`490`) | Total (`500`) | Share | Primary Fleet Assignments |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Solarian** | `1` | `142` | **`143`** | `28.6%` | Ore/Rad/Ice Miners (`102`), Hunters (`25`), Fleet Line/Interdictors (`15`), Cmd (`1`) |
| **Nebula** | `1` | `138` | **`139`** | `27.8%` | Bulk Haulers (`50`), Traders (`30`), Crafters (`30`), Gas (`28`), Cmd (`1`) |
| **Outer Rim** | `1` | `90` | **`91`** | `18.2%` | Liners/Tenders (`40`), Deep-Core Surveyors (`25`), Traders (`15`), Crafters (`10`), Cmd (`1`) |
| **Crimson** | `1` | `76` | **`77`** | `15.4%` | Pirate/Wildlife Hunters (`55`), Heavy Fleet Line (`21`), Cmd (`1`) |
| **Voidborn** | `6` | `44` | **`50`** | `10.0%` | Fleet Carriers/Tanks/Medics (`24`), Covert Recon (`20`), Cmd (`6`) |
| **TOTAL** | **`10`** | **`490`** | **`500`** | **`100.0%`** | **100% optimal birth passives across all 7 Job Divisions** |

## 5. Section-by-Section Cutover Runbook (Zero Cash-Flow Interruption)

### Phase 0: Pre-Flight Code & Policy Prep (Live fleet keeps farming!)
1. **Prefix Compatibility:** Update `game/fleet/division.py`, `station/fleet.py`, and `station/static/app.js` to recognize both legacy prefixes (`miner-`, `trader-`, `hauler-`, `drone-`, `sentinel-`, `scout-`) and the 7 new prefixes (`GSV `, `ROU `, `EUV `, `MCV `, `IFV `, `LSV `, `VSV `) side-by-side so old and new sections run cleanly together during cutover.
2. **AutoNet Upgrades:** Wire `rad_harvester` + `deep_core_extractor` + `precision_factor` into `mine_net.py`, Crafter-Bursar hybrid into `craft_net.py` + `bursar.py`, Passenger Liner routing into Logistics, and load the final T2-T5 `upgrade-policy.json` & `fit-policy.json`.
3. **Manifest Generation:** Generate `game/fleet-500-manifest.tsv` with all 490 unique `GSV/ROU/EUV/MCV/IFV/LSV/VSV` names, exact birth empires, and wing assignments (verifying global uniqueness on SpaceMolt).

### Phases 1-6: Section-by-Section Swap (Suggi's Approved Order -- Income First, Officers Protected!)
**Hard Directives:** (1) Keep ALL hull & module auto-upgrades **DISABLED** (`upgrade-policy.json` `enabled: false`, `fit-policy.json` `enabled_divisions: []`) even after full cutover so Suggi micromanages upgrade timing per division. (2) Keep all `490` retired pilots safely archived as **Reserves** (swept of cash/cargo, disconnected, removed from `[CLTV]`, never deleted). (3) Master birth manifest: `game/fleet-500-manifest.tsv`.

For each wave: **(a)** stop old section pilots (`stop_pilot.py`), **(b)** sweep all wallet credits above `0` into `[CLTV]` Treasury via `wallet.py` (`storage deposit credits` to `Prime Directive` -> `faction`), **(c)** cancel open orders & deposit cargo/holdings into Faction Storage, **(d)** disconnect & remove old section pilots from `[CLTV]` and archive them into Reserves, **(e)** birth & onboard new Culture pilots into `[CLTV]` (`<= 500` exact) and launch AutoNet!

* **Wave 1 -- `Miners` (`130` `EUV`):** Retire `130` `miner-*` -> Birth `102` Solarian + `28` Nebula (`500` exact). Fixes core extraction income first with zero Officer disruption!
* **Wave 2 -- `Hunters` (`80` `ROU`):** Retire `80` `drone-*` -> Birth `55` Crimson + `25` Solarian (`500` exact).
* **Wave 3 -- `Fleet & Defense` (`60` new `GSV` + `10` kept Command):** Retire remaining `15` `drone-*` + `35` `sentinel-*` + `5` non-officer `hauler-*` + `5` non-officer `scout-*` (`60` seats) -> Birth `21` Crimson + `24` Voidborn + `15` Solarian (`500` exact).
* **Wave 4 -- `Traders & Bursars` (`45` `MCV`) + `Crafters & Refiners` (`40` `IFV`):** Cancel/collect old escrow, retire `85` `trader-*` (`85` seats, transferring Officer roles cleanly) -> Birth `45` `MCV` + `40` `IFV` (`85` exact, `55` stations covered nonstop!).
* **Wave 5 -- `Logistics` (`90` `LSV`):** Retire remaining `90` `hauler-*` (preserving/transferring Officer & Builder roles from `hauler-3` cleanly) -> Birth `50` Nebula + `40` Outer Rim (`500` exact).
* **Wave 6 -- `Intel` (`45` `VSV` -- LAST) + Retire Legacy Runners:** Retire remaining `45` `scout-*` -> Birth `20` Voidborn + `25` Outer Rim (`500` exact), then stop `the-collective-runner-1` (freeing `5.84 GiB` RAM + `277%` CPU).

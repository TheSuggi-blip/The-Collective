---
name: division-logistics-salvage-and-tankers
type: general
date: 2026-11-27
author: Trinity
---

# Combat Salvage Tenders and Fleet Fuel Tankers Wing (6C) Operations, Battlefield Recovery, and Deep Refueling

## Abstract

Wing `6C` comprises two specialized 6-ship operational support cohorts (12 Outer Rim Logistic Support Vessels, `LSV` prefix, 13.3 percent of Logistics): `6C. Combat Salvage Tenders` (6 ships: `catalogue` -> `chop_shop` -> `dissolution` -> `liquidator`) and `6C. Fleet Fuel Tankers` (6 ships: `dividend` -> `long_haul` -> `reserve` -> `plenum`) [1][2]. Together, these two elite utility cohorts close the final operational gaps in sovereign fleet warfare and frontier projection. `6C. Fleet Fuel Tankers` run active on `haul-network` and deep-corridor fuel logistics -- using high-capacity Outer Rim tanker hulls (`Long Haul`, `Reserve`, `Plenum`) to keep forward fuel bunkers (`gsc_0044`, `atria`, `felis`, `ridgecrest`) and distant Task Force staging hubs continuously fueled across lawless stretches [1][3]. `6C. Combat Salvage Tenders` are pre-engineered with a complete, unit-tested AutoNet (`game/fleet/salvage_net.py`, `game/salvage-policy.json`, `game/routes/salvage-network.json`) that monitors `read.db:public_battles` for fresh wrecks (`battle_fresh_seconds: 3600`), dispatches specialized salvage modules (`outer_rim_salvage_array`, `salvage_module`, `salvage_drone`) and tow rigs (`basic_tow_rig`, `advanced_tow_rig`), scraps or tows high-value battlefield debris into faction lockboxes (`deposit_target: "faction"`), and enforces strict survivability gates (`min_fuel_reserve_pct: 25%`, `max_ships_per_system: 2`) [4][5]. Currently `salvage-network` is staged disabled (`enabled: false`, `status: "off"`) while its 6 pilots upgrade hulls and level piloting/salvage skills, ready for instant activation as combat tempo rises across T2-T5 engagements [4][6]. Advancing Standing Goals 3, 5, and 6, Wing `6C` gives The Collective two surgical force multipliers rarely matched by single-focus rivals: six dedicated Outer Rim tankers ensuring uninterrupted frontier bunker fuel across lawless corridors, and six pre-engineered salvage tenders poised to convert public galactic battles and `[CLTV]` combat victories into free hull alloys, rare modules, and towed prizes straight into faction lockboxes [1][4][5]. Automated no-throttle upgrades above the 2,000,000 cr treasury floor advance both cohorts smoothly along their Outer Rim specialist ladders (`Catalogue -> Liquidator` and `Dividend -> Plenum`) while keeping salvage safely gated behind `salvage-policy.json` until combat tempo warrants activation [1][4].

## Introduction

In mature fleet operations, massive economic value is routinely left floating in space after every skirmish, while deep frontier operations fail whenever forward combat or mining wings run low on jump fuel far from Empire core stations. Both problems stem from treating support logistics as generic cargo hauling. A standard freighter (`6A` `Dividend` or `Frankenhauler`) lacks dedicated salvage arrays and tow rigs to strip disabled battle wrecks into recoverable hull alloy, rare modules, and scrap components, and lacks specialized long-range fuel-transfer hulls (`Long Haul -> Reserve -> Plenum`) optimized to sustain extended Task Force expeditions across multi-hop lawless space [1][2].

Wing `6C` solves both gaps with two surgical 6-ship Outer Rim specialist teams (12 ships total, 2.4 percent of the 500-ship fleet):

1. **Battlefield Wreck Monetization (`6C. Combat Salvage Tenders`, 6 ships):** Every NPC pirate battle, rival PvP clash, and heavy wildlife engagement recorded in `read.db:public_battles` leaves valuable salvageable wrecks and dropped modules behind [4][5]. Rather than letting rival scavengers loot the aftermath of `[CLTV]` Task Force (`1A/1B/1C`) and Hunter (`2A/2B`) victories -- or leaving public galactic battles untouched -- six Outer Rim salvage tenders fitted with `outer_rim_salvage_array` and `advanced_tow_rig` can sweep fresh battlefields (`<= 60` minutes old), field-scrap standard debris or tow intact high-value hulls straight into faction lockboxes [4][5].
2. **Expeditionary Fuel Projection (`6C. Fleet Fuel Tankers`, 6 ships):** As The Collective expands from 1 station and 3 outposts to its Standing Goal of 5 fortified empire-region stations and 8 corridor outposts, six dedicated Outer Rim tankers (`Long Haul -> Reserve -> Plenum`) guarantee rapid bunker refills and forward Task Force refueling without diverting `6A` general construction freighters [1][3].

By staging `salvage_net.py` completely built, SQL-verified (`test_fleet_sqlcheck.py` 4/4 PASS), and cleanly gated behind a single policy switch (`salvage-policy.json:enabled`), The Collective maintains zero idle waste during early T1 hull building while keeping battlefield salvage ready to turn on at a moment's notice [4][6][7].

In high-intensity multiplayer space economies, every battle creates an invisible secondary economy of wreck debris and dropped high-tier fittings, while every deep-frontier campaign is governed by fuel logistics. Top PvP and frontier blocs like `[ENDL]` (`1,527` PvP kills) and `[BUSY]` (77 percent lawless operations) constantly generate wrecks across contested lanes, yet standard combat fleets carry zero salvage bays or tow rigs because every module slot is committed to weapons and tank [4][5]. Likewise, generic cargo freighters (`6A`) are optimized for mixed industrial tonnage and station kits rather than rapid, long-range expeditionary fuel transfer (`Long Haul -> Reserve -> Plenum`) supporting forward Task Forces (`1A`) and distant outposts (`gsc_0044`, `atria`, `felis`) far from Empire core hubs [1][3]. Splitting `6C` into six Combat Salvage Tenders and six Fleet Fuel Tankers equips The Collective to exploit every battle aftermath and sustain deep territorial projection across all 512 systems without sacrificing a single general freighter slot [1][2].

## Findings

### Sub-Cohort Rosters, Hull Ladders, and Mechanical Route Isolation

Exact verification of `game/upgrade-policy.json`, `manifest_wings.py`, `game/salvage-policy.json`, and `game/routes/*.json` defines both `6C` cohorts [1][2][4][8]:

- **`6C. Combat Salvage Tenders` (6 Outer Rim `LSV` hulls):**
  - Hull Ladder: `catalogue` (T1) -> `chop_shop` (T2) -> `dissolution` (T3) -> `liquidator` (T4) [1].
  - Automated Fitting: `fit-network` equips specialized salvage hardware (`outer_rim_salvage_array`, `salvage_module`, `salvage_drone`) and tow equipment (`basic_tow_rig`, `advanced_tow_rig`) via authoritative `read.db:items.slot` mapping [4][9].
  - Route Lock: Dedicated `game/routes/salvage-network.json` (`wing_prefix: "6C. Combat Salvage"`, currently `status: "off"` and `salvage-policy.json:enabled: false`); excluded from `craft-network` and `bursar-network` so salvage crews never lock onto stationary desks [4][8][10].
- **`6C. Fleet Fuel Tankers` (6 Outer Rim `LSV` hulls):**
  - Hull Ladder: `dividend` (T1) -> `long_haul` (T2) -> `reserve` (T3) -> `plenum` (T4) [1].
  - Active Operations: Enabled in `upgrades.py` (part of the 62 active Core Logistics ships alongside 50 `6A` haulers and 6 `6C` salvage tenders) and active on `haul-network` / standing bunker routes (`supply-bunker-atria-own-cells`, `supply-bunker-gsc-0044-own-cells`), excluded from stationary `craft-network` and `bursar-network` [1][8][11].

### `salvage_net.py` Architecture, Safety Gates, and Activation Controls

Inspection of `game/fleet/salvage_net.py` and `game/salvage-policy.json` verifies the full operational ruleset built for `6C` Combat Salvage Tenders [4][5]:

1. **Fresh Public-Battle Discovery (`read.db:public_battles`):** `salvage_net.py` queries `read.db` (verified SQL schema compliant under `test_fleet_sqlcheck.py` 4/4 PASS) for combat encounters within `battle_fresh_seconds: 3600` (60 minutes) inside `max_jumps: 10`, prioritizing active battle corridors where `[CLTV]` Hunters, Task Forces, or rival factions have recently generated wrecks [4][5][7].
2. **Anti-Crowding & Fuel Safety:** Atomic claims (`claim_ttl_seconds: 1800`) enforce `max_ships_per_system: 2` so all 6 tenders spread across up to 3 distinct battlefields simultaneously without colliding on the same wreck field [4]. Every sortie requires `min_fuel_reserve_pct: 25.0%` before departure to prevent deep-space stranding [4].
3. **Graduated Lawless Risk Controls:** Default launch settings start conservatively (`policed_only: true`, `allow_lawless_with_cloak: false`, `scrap_mode: "field"`, `tow_enabled: false`) so newly activated `Catalogue`/`Chop Shop` tenders build salvage XP safely before enabling cloaked lawless scavenging (`allow_lawless_with_cloak: true`) and intact hull towing (`tow_enabled: true`) in T3 `Dissolution` and T4 `Liquidator` hulls [4].
4. **Lockbox-First Recovery (`deposit_target: "faction"`):** `prefer_lockbox_hubs: true` routes recovered hull alloys, electronics, and salvaged modules straight into faction lockboxes (`ridgecrest`, Empire hubs), feeding `5A`/`5B` crafting, `fit-network` free module reuse, and `4C` Bursar liquidation [4][5].

### Cross-Division Synergy

Both `6C` specialist teams amplify the combat and industrial divisions disproportionately to their 12-ship headcount:
- **Defense (`1A/1B/1C`) & Hunters (`2A/2B`) <-> `6C` Salvage:** Combat divisions generate the battlefields and secure contested corridors; `6C` Salvage monetizes residual wreck alloy and intact rare modules that otherwise despawn, converting battlefield cleanup into pure bonus margin and free fitting stock for `fit-network` [4][5][9].
- **Ice (`3E`) & Refiners (`5A`) -> `6C` Fuel Tankers -> Forward Wings (`1A/1B/1C`, `2A/2B`, `3A`-`3E`, `7A/7B`):** `3E` harvests cryogenic ice, `5A` refines `fuel_cell` at Collective Resort Ridgecrest (`fuel_trickle_target: 3000`), and `6C` Tankers inject long-range fuel directly into frontier outpost bunkers (`gsc_0044`, `atria`, `felis`) and expeditionary Task Forces [1][11][12].
- **Intel (`7A` Covert Recon) -> `6C` Salvage:** `7A` surveillance of rival warzones and frontier hubs populates `read.db:public_battles`, alerting `6C` Tenders to third-party battle wrecks (`[BUSY]`, `[ENDL]`, `[IRLC]` skirmishes) that can be harvested opportunistically once cloaked salvage is unlocked [4][13].

## Conclusion

Wing `6C` delivers two high-leverage force multipliers -- expeditionary fuel projection (`6C` Fleet Fuel Tankers) and autonomous battlefield wreck recovery (`6C` Combat Salvage Tenders) -- for just 2.4 percent of fleet headcount. Keeping `6C` Tankers active today on own-cell bunker replenishment protects forward outpost uptime across lawless corridors, while keeping `6C` Salvage pre-engineered, SQL-tested, and cleanly staged behind `salvage-policy.json:enabled` ensures rapid zero-friction activation as soon as T2-T3 combat intensity justifies dedicated battlefield cleanup.

Confidence in `6C`'s engineering readiness is high (`salvage_net.py` passed `test_fleet_sqlcheck.py` 4/4, and `6C` Tankers operate inside live `haul-network` / bunker routes), while realized salvage credits-per-hour remains pending live soak verification upon activation [4][7]. Activating `salvage-network` in policed space once `6C` tenders commission into T1 `Catalogue` / T2 `Chop Shop` with fitted salvage arrays -- and later unlocking `allow_lawless_with_cloak: true` plus `tow_enabled: true` for T3 `Dissolution` / T4 `Liquidator` -- will add a zero-cost module-and-scrap income stream directly atop The Collective's combat machine. Key telemetry to watch post-activation will be salvage value recovered per fuel credit burned and tender survival rate near active pirate zones.

Looking across the medium-term roadmap, both `6C` cohorts scale cleanly with The Collective's fleet tier and territorial expansion. The six `6C` Fleet Fuel Tankers continue active service today, graduating from `Dividend` through `Long Haul`, `Reserve`, and `Plenum` to keep all current outposts (`gsc_0044`, `atria`, `felis`, `ridgecrest`) and future corridor outposts #4 through #8 topped up with internally refined `fuel_cell` output from `3E` Ice and `5A` Refiners [1][11][12]. Meanwhile, the six `6C` Combat Salvage Tenders follow a two-stage activation plan: once T1 `Catalogue` / T2 `Chop Shop` hulls commission with fitted `outer_rim_salvage_array` modules, flipping `salvage-policy.json:enabled: true` (and removing `status: "off"` on `salvage-network.json`) launches low-risk policed field-scrapping across fresh `read.db:public_battles` [4][5][6]. Once live soak metrics confirm positive scrap-and-module recovery per fuel credit and tenders reach T3 `Dissolution` / T4 `Liquidator` with cloak fitting, unlocking `allow_lawless_with_cloak: true` and `tow_enabled: true` opens rival warzone scavenging and high-value intact hull towing -- directly serving Standing Goal 6 (total game mastery) [1][4][5]. Preserving clear route separation (`6C` Tankers feeding active own-cell outpost bunkers today; `6C` Salvage Tenders scaling into cloaked battlefield recovery as combat tiers rise) guarantees maximum capital utility from all 12 specialist Outer Rim hulls without bloating general `6A` freighter logic [1][4][11]. Combined with `3E` ice harvesting and `5A` fuel-cell refining, `6C` ensures The Collective neither leaves free battlefield loot behind nor runs dry on the frontier [12].

## General Lessons

1. **Isolate niche specialist utilities into compact 6-ship cohorts rather than diluting core freighter wings.** Six dedicated Fuel Tankers (`Plenum`) and six dedicated Salvage Tenders (`Liquidator`) solve specialized fleet bottlenecks completely without sacrificing any of `6A`'s 50 general bulk haulers [1][2].
2. **Pre-build and test dormant AutoNets cleanly behind declarative policy flags.** Building `salvage_net.py` with full SQL tests while keeping `enabled: false` lets a fleet scale into new game mechanics on demand with zero emergency rush coding [4][7].
3. **Stage high-risk frontier utilities through graduated safety tiers.** Launching salvage in policed space (`field` scrap only) before unlocking cloaked lawless scavenging and hull towing protects expensive T2-T4 specialist hulls while verifying real drop yields empirically [4].
4. **Recycle salvaged modules directly back into `fit-network` via faction lockboxes.** Depositing salvaged weapons, shields, and components straight into faction storage reduces cash expenditure on external module markets (32k-130k cr per 1-6h) and strengthens self-sufficiency [4][9].
5. **Pair long-range fuel logistics with internal cryogenic refining.** Dedicated Outer Rim tankers (`Long Haul -> Plenum`) turn Ridgecrest's internally refined `fuel_cell` surplus into deep territorial reach across all 5 empire regions [1][12].
6. **Enforce strict fuel-reserve departure gates on deep-frontier utility vessels.** Requiring `min_fuel_reserve_pct: 25.0%` inside `salvage_net.py` prevents single-purpose salvage tenders from stranding themselves in empty lawless battlefields far from friendly fuel bunkers [4].
7. **Keep battlefield wreck scanners decoupled from active warships.** Feeding `salvage_net.py` directly from `read.db:public_battles` refreshed by `7A` Covert Recon lets unarmed salvage crews arrive right after hostile fleets clear the grid, capturing loot safely without slowing down `1A`/`2A` combat tempo [4][5][13].
8. **Validate every SQL query in dormant AutoNets continuously under automated CI.** Including `salvage_net.py` inside `test_fleet_sqlcheck.py` (4/4 PASS) guarantees schema changes in `read.db` never silently break staged runners before activation day [7]. Pre-verifying dormant SQL queries inside CI eliminates surprise runtime failures when tactical conditions shift rapidly [7].

## Sources

1. `the-collective:game/upgrade-policy.json` -- Exact `6C` counts (`6` Combat Salvage Tenders `catalogue -> liquidator`; `6` Fleet Fuel Tankers `dividend -> plenum`).
2. `knowledge/spacemolt-fleet-500-blueprint-and-empire-mechanics.md` -- `6C` Outer Rim specialist logistics architecture.
3. `the-collective:game/fleet/haul.py` -- Active bunker and corridor fuel distribution logic.
4. `the-collective:game/salvage-policy.json` -- Live staged salvage policy (`enabled: false`, `battle_fresh_seconds: 3600`, `max_ships_per_system: 2`, `tools`).
5. `the-collective:game/fleet/salvage_net.py` -- Public-battle wreck discovery, atomic system claims, field scrap / tow execution, and lockbox deposits.
6. `TASKS.md` -- Staged activation condition for `salvage-network`.
7. `the-collective:scripts/tests/test_fleet_sqlcheck.py` -- Verified 4/4 PASS SQL schema audit including `salvage_net.py`.
8. `the-collective:game/routes/craft-network.json` -- Mechanical `exclude_wing_prefix` isolating `6C` from docked crafting.
9. `the-collective:game/fleet/fit_net.py` -- Authoritative `items.slot` fitting for salvage arrays, tow rigs, and faction-storage reuse.
10. `the-collective:game/routes/bursar-network.json` -- Mechanical desk lock excluding `6C`.
11. `the-collective:game/routes/supply-bunker-gsc-0044-own-cells.json` -- Standing own-cell outpost fuel bunker replenishment.
12. `the-collective:game/bursar-policy.json` -- `fuel_trickle_target: 3000` internal fuel-cell production feeding `6C` Tankers.
13. `the-collective:game/fleet/census_net.py` -- `7A` frontier battle surveillance feeding `read.db:public_battles`.

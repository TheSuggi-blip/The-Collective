---
name: division-logistics-passenger-liners
type: general
date: 2026-11-27
author: Trinity
---

# Passenger and Resort Liners Wing (6B) Strategy, Tourism Economics, and Activation Roadmap

## Abstract

Wing `6B. Passenger & Resort Liners` is The Collective's 28-ship dedicated commercial tourism and passenger-transport wing, manned by Outer Rim Logistic Support Vessels (`LSV` prefix) earmarked for SpaceMolt's luxury liner progression ladder (`loose_change` -> `consortium` -> `concordia` -> `comet`) [1][2]. Unlike every other active wing in the 500-ship fleet, `6B` hull upgrades are deliberately held at `max_auto_tier: 0` in `game/upgrade-policy.json` until a dedicated, profitable `passenger-network` AutoNet (`passenger_net.py`) is engineered and live-verified -- preventing millions of credits from sitting idle in specialized luxury cabins before the booking runner is online [1][3]. Rival intelligence confirms why `6B` is a strategic goldmine once activated: `[IRLC]` operates 28 T3 `Concordia` luxury passenger liners as a core pillar of its `+4.22M cr/h` wealth engine, and `[HEXC]` monetizes `Hex Star` resort tourism directly alongside its 11 sovereign bases [4]. With Collective Resort Ridgecrest (`a2cee88abdcb31db229c04315f0ef6e1`) already live with 13 active rent-free facilities and hospitality supply chains (`purified_water`, `space_pizza`, `solarian_biotic`, `station_seltzer`, `void_espresso`, `lumen_honey_cake`) built into `bursar-policy.json`, `6B` represents The Collective's highest-upside untapped revenue vertical [5][6][7]. Until `passenger-network` launches, `6B` ships stay productively employed in core Logistics haulage and piloting/navigation leveling rather than sitting docked. Directly supporting Standing Goals 1, 3, 4, and 6 (utilizing every profitable mechanic SpaceMolt offers without artificial self-handicaps), Wing `6B` stages 28 Outer Rim luxury liners to transform Collective Resort Ridgecrest and four future regional stations into high-margin commercial tourism hubs [1][7]. By intentionally holding `6B` hull capex at zero while pilots build Piloting and Navigation mastery in transitional Logistics work -- and unlocking `Loose Change -> Consortium -> Concordia -> Comet` upgrades immediately after a profitable `passenger-network` live soak -- The Collective maximizes capital efficiency today while locking in `[IRLC]`-scale uncorrelated tourism cash flow tomorrow [1][3][4].

## Introduction

In SpaceMolt, passenger and resort tourism is a distinct, high-margin commercial pillar largely uncorrelated with mineral or combat-loot commodity cycles. While asteroid belts deplete and ore markets saturate when dozens of factions mine the same metals, NPC passenger charters, VIP tourist contracts, and resort-destination routes generate steady direct credit inflows scaled by passenger cabin capacity, liner tier, hospitality supply quality, and station resort amenities [4][7]. Top rivals have already proven the unit economics at scale: `[IRLC]` commits exactly 28 T3 `Concordia` passenger liners (10.2 percent of its 275-ship fleet) to continuous passenger runs contributing directly to its `+4.22M cr/h` cash compounding, while `[HEXC]` pairs its flagship `Hex Star` resort hub with high-tier tourism traffic [4].

The Collective deliberately mirrored `[IRLC]`'s exact 28-liner fleet sizing when designing the 500-ship manifest (`6B. Passenger & Resort Liners`, 28 Outer Rim `LSV` hulls, 5.6 percent of total fleet) and built Collective Resort Ridgecrest (`ridgecrest`) explicitly as a sovereign resort destination equipped with hospitality consumables and rent-free station infrastructure [2][7].

Crucially, however, disciplined capital allocation demands **matching capex timing to software readiness**. Buying 28 T1 `Loose Change`, T2 `Consortium`, or T3 `Concordia` passenger hulls before a dedicated `passenger_net.py` runner exists to read station passenger boards, optimize multi-leg VIP routes, manage cabin modules (`fit-network`), and book tourism revenue cleanly under IFRS 15 would tie up 2M to 25M+ credits in specialized hulls performing ordinary cargo hauling poorly [1][3]. Holding `6B` upgrades off until `passenger-network` is built, unit-tested, and soak-verified preserves treasury cash for immediate high-ROI combat, mining, and freighter upgrades today while keeping all 28 Outer Rim pilots leveling piloting and navigation skills so they can step straight into `Consortium` and `Concordia` hulls the day `passenger-network` flips live [1][3].

Diversifying core non-mission operating profit is decisive for long-term galactic dominance. Live fleet economics prove that mission payouts act as an early-game bridge while enduring enterprise compounding depends on repeatable external cash verticals: mineral/gas/ice extraction, biological hunting, zero-fuel manufacturing, multi-hub trading, AND passenger tourism [4][7][11]. While `[BUSY]` relies heavily on sheer hull volume and combat/mining scale (`1,249` ships) and `[HIVE]` relies on shuttle crafting (`200` ships), `[IRLC]` achieves extraordinary per-ship wealth velocity (`+4.22M cr/h` from only 275 ships -- `15,345 cr/h` per ship!) specifically by layering 28 T3 `Concordia` passenger liners directly atop its mining, trading, and 8-base industrial backbone [4]. `[HEXC]` validates the exact same tourism thesis at `Hex Star` [4]. Reserving 28 Outer Rim `LSV` hulls (matching `[IRLC]` ship-for-ship) and preparing Collective Resort Ridgecrest's full hospitality basket positions The Collective to capture that exact high-margin vertical cleanly [1][6][7].

## Findings

### Roster, Luxury Liner Progression, and Current Dispatch Posture

Exact verification of `game/upgrade-policy.json`, `manifest_wings.py`, and `game/routes/*.json` establishes `6B`'s blueprint and current operating state [1][2][8]:

- **Fleet Allocation:** 28 Outer Rim `LSV` hulls (`6B. Passenger & Resort Liners`), matching `[IRLC]`'s exact 28-ship `Concordia` liner cohort [1][4].
- **Luxury Liner Hull Ladder (Held Pending `passenger-network`):** `loose_change` (T1) -> `consortium` (T2) -> `concordia` (T3) -> `comet` (T4) [1]. As documented in `upgrade-policy.json._doc`, 472 of 500 ships are enabled for automatic upgrades while the 28 `6B` liners are held specifically until Passenger AutoNet activation [1].
- **Current Transitional Dispatch:** `craft-network.json` explicitly sets `exclude_wing_prefix: [..., "6B.", ...]`, and `bursar-network.json` restricts desks to `4C.`/`5A.` [8][9]. During this pre-launch staging phase, `6B` pilots run standing piloting/navigation training and general Logistics support (`train-jumps-hauler`, safe haulage) so all 28 pilots accumulate Piloting `>= 20` and Navigation mastery ahead of T3 `Concordia` commissioning [1][3].

### Resort Ecosystem Pre-Requisites Already Live in Production

Even before `passenger_net.py` is coded, three critical foundations of the tourism value chain are already built and operating live across The Collective [5][6][7]:

1. **Sovereign Resort Anchor (`Collective Resort Ridgecrest`):** Ridgecrest (`a2cee88abdcb31db229c04315f0ef6e1`) is live and fortified with **13 active rent-free faction facilities**, serving as the inaugural flagship resort hub in our 5-station regional masterplan [5][7].
2. **Hospitality Consumable Supply Chain:** `bursar-policy.json` and `5A` Station Refiners already stock and manufacture the full hospitality basket (`purified_water`, `solarian_biotic`, `crimson_bloodwine`, `station_seltzer`, `gloomshine`, `protein_rations`, `algae_wafer`, `crimson_iron_rations`, `solarian_gourmet_rations`, `space_pizza`, `nebula_stellar_vintage`, `void_espresso`, `lumen_honey_cake`, `ion_sparkling_water`, `biogas_fizz`) [6]. `haul.py` protects owned-hub hospitality inventories via `_hub_upkeep_keep_floor` so commercial liquidators never strip resort consumables [10].
3. **Accounting Readiness (IFRS 15 & IAS 2):** `accounting.py` already tracks owned-station hospitality upkeep (`Memo: Owned Station Consumables & Hospitality Upkeep (IAS 2 Non-Cash Inv. Draw)`) separately from external cash sales so future passenger ticket revenue will report cleanly as its own IFRS 15 external cash stream without muddying freight or mining margins [11].

### Engineering Blueprint for Future `passenger-network` Activation

Activating `6B` as a full autonomous profit center requires five coordinated engineering deliverables across the fleet stack [3][7]:
1. **Board Ingestion (`store.py` & `bursar.py`):** Poll and persist live station passenger/charter boards across all 55+ Bursar hubs and owned resorts into `read.db` (extending the existing 60-second `missions`/`books` polling loop) [6].
2. **Dynamic Liner Runner (`game/fleet/passenger_net.py` + `game/passenger-policy.json`):** Score multi-hop passenger charters by `(fare_cr - jump_fuel_cr) / total_jumps`, batch multiple passengers heading along shared empire corridors into one cabin fill, avoid active pirate systems (`pirate_avoid_hours`), and route VIP resort traffic directly through Collective Resort Ridgecrest and future regional resorts [7].
3. **Cabin Fitting (`fit-policy.json`):** Add `6B.` luxury/standard passenger cabin, shield, and navigation-speed loadouts backed by authoritative `read.db:items.slot` lookup [12].
4. **Wing-Locked Route (`game/routes/passenger-network.json`):** Lock `wing_prefix: ["6B."]`, `max_ships: 28`, so all 28 liners shift atomically onto passenger operations [3].
5. **Unlock `6B` Upgrades (`upgrade-policy.json`):** Enable `loose_change -> consortium -> concordia -> comet` commissioning once a 3-ship live soak confirms positive net cash profit per hour [1][3].

### Cross-Division Synergy

Once live, `6B` transforms stationary hospitality overhead into high-margin recurring cash:
- **`3E` Ice + `3D` Gas + `5A` Refiners + `6A` Haulers -> `6B`:** Upstream ice, gas, and zero-fuel crafting stock Ridgecrest and future regional resorts with low-cost hospitality consumables that attract premium passenger fares [6][7].
- **`4C` Bursars & `7A/7B` Intel -> `6B`:** Live station board telemetry identifies the highest-paying VIP routes while pirate-sighting intelligence keeps unarmed luxury liners strictly in safe corridors [6][13].
- **`1A/1C` Defense -> `6B`:** Outpost Sentinels secure resort approach lanes so luxury liners never lose high-tier `Concordia` or `Comet` hulls to frontier raiders [14].

## Conclusion

Wing `6B. Passenger & Resort Liners` is a deliberate, capital-disciplined strategic option worth 28 Outer Rim liners (`5.6%` of the fleet) designed to replicate `[IRLC]`'s proven 28-`Concordia` tourism engine and monetize Collective Resort Ridgecrest alongside future 5-empire regional stations. Holding `6B` hull capex at zero until `passenger-network` is built and soak-verified is exemplary capital stewardship: zero wasted credits today, full pilot XP leveling in progress, and all upstream resort hospitality pipelines already running live.

Confidence in the strategic case for `6B` is high based on direct rival telemetry (`[IRLC]` 28 `Concordias`, `[HEXC]` `Hex Star` tourism), while exact realized credits-per-hour for The Collective remains unverified until `passenger_net.py` runs its first live soak test [4][7]. Launching `passenger-network` (and unlocking `6B` hull upgrades to `Consortium`/`Concordia`) stands as one of the highest-leverage medium-term subgoals on Trinity's roadmap toward Standing Goals 1, 3, and 4 (diversifying core non-mission operating profit beyond mining and hunting). Before enabling full 28-ship capex, a controlled 3-liner live test must confirm positive net operating margin after fuel and hospitality draw.

The operational roadmap for `6B` follows a disciplined four-gate launch sequence designed to eliminate wasted capital. First, extend `bursar.py` and `store.py` to ingest live station passenger charter boards across all 55+ Bursar hubs into `read.db`, producing exact empirical fare-per-jump and VIP destination curves before writing route heuristics [6][7]. Second, build and unit-test `game/fleet/passenger_net.py`, `game/passenger-policy.json`, cabin loadouts in `fit-policy.json`, and wing-locked `game/routes/passenger-network.json` (`wing_prefix: ["6B."]`, `max_ships: 28`), prioritizing multi-passenger cabin batching and Ridgecrest resort traffic [3][7][12]. Third, run a live 3-liner soak test in T1 `Loose Change` / T2 `Consortium` hulls, verifying strictly positive net cash flow after fuel and IAS 2 hospitality draw in `accounting.py` [3][11]. Fourth, once the 3-liner soak passes, unlock full zero-throttle commissioning for all 28 `6B` Outer Rim pilots straight up to T3 `Concordia` and T4 `Comet` -- activating a brand-new, uncorrelated multi-million-credit-per-day profit pillar synchronized across our five planned empire resorts [1][4][7]. Until that 3-liner live verification clears every profitability and safety gate, holding `6B` hull capex at zero protects treasury liquidity for immediate T2-T4 mining, combat, and freighter compounding while keeping all 28 pilots actively leveling Piloting and Navigation skills [1][3]. Once unlocked, `6B` completes The Collective's five-pillar commercial engine alongside extraction, combat loot, zero-fuel manufacturing, and multi-hub arbitrage -- directly rivaling `[IRLC]` across every profitable dimension of SpaceMolt [4][7]. Continuous monitoring of charter board saturation and fare-per-jump yields across all five empire hubs will keep liner capacity aligned with peak galactic demand [6][7].

## General Lessons

1. **Sequence hardware capex strictly behind software readiness.** Never purchase specialized single-purpose hulls (`Loose Change`, `Concordia`) before the autonomous runner that monetizes them exists and passes live integration testing; level the pilots cheaply in transitional hulls first [1][3].
2. **Build uncorrelated revenue verticals to bullet-proof fleet cash flow.** Relying exclusively on raw ore mining or wildlife hunting exposes enterprise profit to market gluts and rival competition; adding passenger tourism creates an independent cash stream that thrives alongside industrial expansion [4][7].
3. **Turn station upkeep from pure cost into a revenue-generating amenity.** Collective Resort Ridgecrest already consumes water, rations, and beverages; pairing those hospitality lines with a 28-liner passenger network monetizes resort infrastructure directly [6][7].
4. **Copy proven rival force ratios, then integrate them deeper.** Matching `[IRLC]`'s 28-liner scale while backing it with 55 Bursar board-scanners and rent-free Ridgecrest hospitality crafting combines the best structural advantages of multiple top blocs [4][6].
5. **Verify unit economics with a small live cohort before scaling full capex.** Testing 3 passenger liners live before committing 25M+ cr to 28 T3 `Concordias` limits downside while proving exact fare-per-jump yields [3].
6. **Use transitional duties to pre-level specialist pilots before their dedicated runner launches.** Having all 28 `6B` Outer Rim pilots grind Piloting `>= 20` and Navigation mastery in active Logistics routes today means they can step straight into T3 `Concordia` hulls the day `passenger-network` goes live, skipping weeks of T1 ramp-up delay [1][3].
7. **Separate hospitality upkeep accounting from commercial fare revenue from day one.** Tracking owned-station consumables under IAS 2 non-cash inventory draw while logging passenger ticket income under IFRS 15 external revenue guarantees honest unit-economic measurement of resort profitability [11].
8. **Stage upstream hospitality infrastructure ahead of liner deployment.** Stocking Ridgecrest with `purified_water`, rations, and specialty beverages through `5A`/`4C` before `passenger-network` flips live ensures the first charter voyages launch directly into fully provisioned resort amenities [6][7].

## Sources

1. `the-collective:game/upgrade-policy.json` -- Exact `6B. Passenger & Resort Liners` count (`28` Outer Rim `LSV`), `loose_change -> comet` ladder, and deliberate hold pending Passenger AutoNet.
2. `knowledge/spacemolt-fleet-500-blueprint-and-empire-mechanics.md` -- `6B` wing design and Outer Rim transit speed synergies.
3. `TASKS.md` -- Passenger AutoNet activation roadmap and staged rollout gating.
4. `knowledge/spacemolt-rival-strategies-intelligence.md` -- `[IRLC]` (`28 Concordia`) and `[HEXC]` (`Hex Star`) tourism benchmarks.
5. `the-collective:data/store/read.db` -- Verified `13` active rent-free facilities at Collective Resort Ridgecrest (`a2cee88abdcb31db229c04315f0ef6e1`) audited 2026-11-27.
6. `the-collective:game/bursar-policy.json` -- Live hospitality consumable procurement and refining list (`space_pizza`, `solarian_biotic`, `void_espresso`, `purified_water`).
7. `knowledge/spacemolt-stations-and-passenger-plan.md` -- Sovereign resort architecture, 5-station regional plan, and passenger mechanics.
8. `the-collective:game/routes/craft-network.json` -- Mechanical `exclude_wing_prefix` isolating `6B` from docked crafting.
9. `the-collective:game/routes/bursar-network.json` -- Mechanical `wing_prefix: ["4C.", "5A."]` confirming `6B` exclusion from stationary desks.
10. `the-collective:game/fleet/haul.py` -- `_hub_upkeep_keep_floor` protecting resort hospitality stockpiles.
11. `the-collective:game/fleet/accounting.py` -- IFRS 15 external revenue separation and IAS 2 non-cash hospitality upkeep memo reporting.
12. `the-collective:game/fleet/fit_net.py` -- Authoritative `items.slot` fitting framework ready for passenger cabin loadouts.
13. `the-collective:game/fleet/census_net.py` -- Whole-map pirate and safety telemetry protecting unarmed liner routes.
14. `knowledge/division-fleet-and-defense.md` -- `1C` Outpost Sentinel security over resort corridors.

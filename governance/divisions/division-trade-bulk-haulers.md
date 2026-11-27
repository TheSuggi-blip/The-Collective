---
name: division-trade-bulk-haulers
type: general
date: 2026-11-27
author: Trinity
---

# Bulk Trade Haulers Wing (4B) Operations, Buy-Wall Liquidation, and Heavy Commercial Flow

## Abstract

Wing `4B. Bulk Trade Haulers` is The Collective's 8-ship heavy commercial liquidation and commodity arbitrage wing, manned by Nebula Merchant Courier Vessels (`MCV` prefix) progressing along SpaceMolt's highest-capacity freighter ladder (`dividend` -> `junk_convoy` -> `enterprise` -> `frankenhauler`) [1][2]. While `4A. Express Arbitrage` sprints thin, high-value spreads in fast Outer Rim couriers and `6A. Supply Chain Bulk Haulers` moves internal Logistics materials without selling on open markets, `4B` sits squarely in the commercial Trade profit lane (`haul-network-trade` under `game/fleet/haul.py` and `game/haul-policy.json`) [3][4]. Its mission is high-tonnage revenue conversion: draining massive accumulated surplus from faction lockboxes (`ridgecrest`, Empire core depots) straight into deep external rival buy-walls (such as `[BUSY]`'s 468,000-unit `silver_ore` wall at 101 cr/u at `arneb` and `[HEXC]`'s industrial walls at `dheneb`) and executing high-volume commodity arbitrage whenever bulk ask-to-bid spreads exceed fees and fuel [3][5][6]. Mechanically excluded from stationary Bursar desks and docked crafting, `4B` uses `market_guard.py` net-external `load_cltv_buy_qty` depth checks, 70-percent minimum fair-value liquidation floors, and parallel `arb-bw:` buy-wall claim keys to convert mined tonnage into treasury cash at minimal fuel cost per unit [3][7]. Directly advancing Standing Goals 1 and 4, Wing `4B` ensures that tens of thousands of units of mined ore, gas, ice, and refined industrial surplus accumulated by 130 miners (`3A`-`3E`) and 40 crafters (`5A`/`5B`) never stagnate in peripheral lockboxes [1][3][8]. Automated no-throttle upgrades above the 2,000,000 cr treasury floor advance all 8 Nebula hulls from `Dividend` through `Frankenhauler`, while strict IFRS 15 accounting records every commercial bulk delivery as clean External Cash Revenue separate from Logistics' internal depot moves [1][9].

## Introduction

Raw extraction and mass manufacturing generate zero spendable treasury cash until physical tonnage reaches a paying buyer. In a 500-ship fleet with 130 active miners (`3A`-`3E`) and 40 crafters (`5A`/`5B`), lockboxes at Collective Resort Ridgecrest and regional stations accumulate tens of thousands of units of `silver_ore`, `plasma_gas`, `titanium_ore`, `darksteel_ore`, `methane_ice`, `energy_crystal`, and refined industrial goods every day [6][8]. Stationary `4C` Bursars can sell locally at the hub where goods are stored, but the deepest external cash bids frequently sit 3 to 10 jumps away at specialized rival megahubs or major Empire exchanges (`market_prime`, `sol`, `arneb`, `dheneb`, `nexus_prime`) [5][6].

Moving 20,000 units of ore or gas in small 100-cargo express shuttles (`4A`) requires 200 separate round trips, burning massive jump fuel and starving fast couriers of their high-margin module spreads. Top rival `[IRLC]` solved this exact scaling problem by deploying 32 massive `Frankenhauler` bulk freighters alongside 47 `Syndicate` express couriers -- pairing speed for thin spreads with giant holds for commodity liquidation to sustain `+4.22M cr/h` wealth compounding [5]. `[HEXC]` mirrors the exact same freighter choice (`Frankenhauler`) across its 11-base network [5].

Wing `4B. Bulk Trade Haulers` (8 Nebula `MCV` hulls) brings that exact heavy commercial freighter capability into The Collective while maintaining crisp IFRS 15 / Responsibility Center separation from Logistics (`6A`). Logistics `6A` freighters (50 ships) focus purely on internal supply chains, outpost bunker fuel, construction kits, and depot consolidation -- never selling on the market (`allow_sell: false`) -- whereas `4B` Trade Bulk Haulers focus purely on external commercial cash realization: hauling unreserved faction surplus directly to the deepest external buy-walls and lifting heavy multi-hundred-unit commodity spreads [1][3][9].

Comparing bulk freighter economics against courier economics clarifies why `4B` is vital even alongside 12 `4A` express couriers and 55 stationary `4C`/`5A` desks. A T4 `Frankenhauler` holds thousands of cargo units in a single jump sequence, driving jump-fuel cost per unit of `silver_ore`, `plasma_gas`, `titanium_ore`, or `darksteel_ore` down to a fraction of a credit [1][3]. When `[BUSY]` posts a 468,000-unit `silver_ore` buy-wall at 101 cr/u at `arneb`, or `[HEXC]` posts deep industrial walls at `dheneb`, small couriers simply cannot move fleet-scale output fast enough to keep lockboxes clear [5][6]. At the same time, rival trading fleets such as `[BUSY]` (130 `Floor Price` desks + bulk haulers) and `[IRLC]` (32 `Frankenhauler` heavy transports + 47 `Syndicate` couriers) demonstrate that pairing a massive bulk freighter class with fast couriers is the gold standard for dominating galactic commodity flows [5].

## Findings

### Roster, Heavy Freighter Ladder, and Dispatcher Conditions

Verified records from `game/upgrade-policy.json`, `manifest_wings.py`, and `game/routes/*.json` define `4B`'s hardware and dispatch wiring [1][2][4]:

- **Fleet Allocation:** 8 Nebula `MCV` hulls (`4B. Bulk Trade Haulers`), leveraging Nebula native cargo/industrial hauling bonuses [1][2].
- **Heavy Freighter Progression:** `dividend` (T1) -> `junk_convoy` (T2) -> `enterprise` (T3) -> `frankenhauler` (T4) [1]. Upgrading from starter hulls through `Enterprise` and `Frankenhauler` multiplies single-load cargo capacity by an order of magnitude, slashing jump fuel burn per delivered unit of ore or gas [1][5].
- **Mechanical Route Lock:** `bursar-network.json` restricts docked Bursar service to `4C.` and `5A.`, and `craft-network.json` explicitly excludes `4B.` (`exclude_wing_prefix`), guaranteeing that all 8 heavy commercial freighters remain continuously available on `haul-network-trade` (`haul.py`) after `fit-network` equips cargo expanders and shields [4][10].

### Commercial Surplus Liquidation, Bulk Arbitrage, and Anti-Manipulation Guards

Inside `game/fleet/haul.py`, `4B` operates across two commercial lanes governed by `game/haul-policy.json` and `game/fleet/market_guard.py` [3][7]:

1. **Faction & Personal Surplus Liquidation (`pick_surplus_liquidation`):** Whenever a `4B` pilot holds officer/member faction-withdrawal rights (`_pilot_can_withdraw_faction`), it scans both personal storage and faction lockbox inventories (`allow_faction_surplus_liquidation: true`), subtracts protected reserve floors (`reserved` items from `needs.tsv`, owned-hub hospitality/upkeep floors via `_hub_upkeep_keep_floor`, and central depot targets), and matches remaining surplus against the highest net-profit external bids [3].
2. **Strict Anti-Lowball & Net-External Volume Checks:** `haul.py` evaluates real external top-of-book `bid_qty` after subtracting CLTV's own open buy quantities (`load_cltv_buy_qty`) -- preventing self-wash trading while keeping massive external rival walls (like `[BUSY]`'s 468k `silver_ore` wall) fully visible [3][7]. Any item with oracle fair price `>= 20 cr` refuses any destination bid below **70 percent of oracle fair value** (`bp < fair * 0.70`), preventing `4B` freighters from ever dumping valuable mined ore into predatory scam bids [3].
3. **Parallel Bulk Buy-Wall Arbitrage (`arb-bw:`):** On standard thin arbitrage bids, `assign_optimal_arbitrage()` locks `(dest_base, item)` to a single hauler. On deep bulk buy-walls (`bid_qty >= 500` and `bid_p >= bw_min_bid`), `haul.py` uses per-origin keys (`arb-bw:<origin>:<dest>:<item>`), allowing multiple `4B` freighters to scoop cheap commodity asks from different empire hubs simultaneously and deliver them into the same giant rival buy-wall [3].
4. **Calm Lawless Buy-Wall Delivery & Escort Readiness:** `allow_calm_buywall_dest: true` enables `4B` to deliver bulk high-value commodities (`>= 50 cr`, `>= 200` qty) directly to verified pirate-free lawless rival hubs (`arneb`, `dheneb`), while `haul.py` retains `escort_proto.py` hooks whenever contested high-value convoy protection is enabled [3][11].

### Cross-Division Synergy and Financial Impact

`4B` is the commercial cash register for Mining and Crafting's bulk surpluses:
- **Miners (`3A`-`3E`) -> Logistics (`6A`) -> `4B`:** Miners deposit extracted ore, gas, and ice into regional lockboxes and Collective Resort Ridgecrest (`a2cee88abdcb31db229c04315f0ef6e1`), Logistics `6A` consolidates scattered stocks into central hubs, and `4B` lifts full freighter loads straight into the highest-paying external buy-walls across the galaxy [3][6].
- **Bursars (`4C`) <-> `4B`:** `4C` desks liquidate steady local retail demand at 0 fuel across 55+ hubs while `4B` absorbs massive bulk overflows that would otherwise sit unsold or depress local ask books -- turning locked inventory into liquid treasury cash for zero-throttle hull upgrades [1][3].
- **Trade Accounting Clarity:** Every `4B` liquidation books external cash directly into IFRS 15 Section 1 External Cash Revenue while `6A` internal hub moves remain strictly cost-center Logistics transfers, keeping division P&L clean and uncorrupted [9].

## Conclusion

Wing `4B. Bulk Trade Haulers` solves the high-tonnage cash conversion bottleneck between a 130-ship mining fleet and a multi-region galactic market. Dedicating 8 Nebula `MCV` hulls to the `Dividend -> Junk Convoy -> Enterprise -> Frankenhauler` freighter ladder keeps massive cargo capacity focused strictly on profitable external sales and bulk commodity arbitrage, completely separated from Logistics' internal upkeep chains (`6A`) and fast courier races (`4A`). Wiring `haul.py` directly to `market_guard.py`'s `load_cltv_buy_qty` subtraction, 70-percent fair-value liquidation floor, and mirage-arbitrage detector ensures bulk loads capture top rival buy-walls without ever falling for wash traps or lowball scams.

Confidence in `4B`'s architecture is high, validated by rival precedent (`[IRLC]`'s 32 `Frankenhaulers`) and live Trade net cash flow (`+132,467 cr/h`) [5][8]. As The Collective upgrades `3A`-`3E` miners into T3-T4 hulls (`Bonanza King`, `Lithosphere`, `Phase Collector`, `Cryo Industrial`), raw extraction tonnage per hour will multiply 3x to 5x. Upgrading `4B` ahead of or alongside that mining surge into `Enterprise` and `Frankenhauler` hulls will prevent lockbox inventory pileups and keep cash conversion velocity tight. If lockbox inventories of unreserved sellable ores (`silver_ore`, `plasma_gas`, `titanium_ore`) begin rising faster than `4B` + `4C` can liquidate them, expanding bulk liquidation concurrency or tuning `4B` cargo-expander fitting ratios will restore immediate throughput.

As `4B` scales from T1 `Dividend` through T2 `Junk Convoy`, T3 `Enterprise`, and T4 `Frankenhauler`, its cash-conversion leverage multiplies dramatically alongside the 130-ship Mining division's simultaneous climb into T3-T4 extraction hulls [1][5]. Every hull tier gained by `4B` slashes total fleet fuel spent on commercial liquidation while unlocking larger parallel `arb-bw:` arbitrage lots across empire and calm rival exchanges [3]. Furthermore, as The Collective establishes regional stations #2 through #5 across all five empire regions (Standing Goal 3), `4B` will gain five fortified regional lockbox depots from which to sweep bulk surpluses directly into whichever galactic megahub posts the highest external cash bid that hour [3][6]. Monitoring two key indicators -- lockbox unreserved surplus aging (`> 24h` unsold sellable stock) and `4B` realized gross margin above `70%` oracle fair value -- will confirm cleanly whether 8 heavy commercial freighters remain optimally sized or warrant increased cargo-expander fitting ratios as mining tonnage climbs [3][7]. Combining Nebula heavy freighter progression (`Dividend -> Frankenhauler`) with `load_cltv_buy_qty` visibility and 70-percent fair-value liquidation floors turns Wing `4B` into a disciplined, high-tonnage cash engine for the entire 500-ship fleet [1][3][7]. Tracking lockbox liquidation turnaround and net realized fair-value capture ensures `4B` scales cleanly ahead of T3-T4 mining volume growth [3][7].

## General Lessons

1. **Separate internal supply haulage (`6A`) from commercial liquidation haulage (`4B`).** Putting both duties on the same ship pool causes urgent station fuel runs to starve cash sales, or cash sales to starve outpost bunkers. Dedicated commercial freighters protect both liquidity and industrial uptime [1][9].
2. **Scale freighter hold size alongside extraction fleet tier.** A T0 mining fleet needs small couriers; a T3-T4 130-ship mining fleet generates tens of thousands of units per hour that require `Enterprise` and `Frankenhauler` holds to avoid crushing fuel-per-unit overhead [5].
3. **Never hide external megahub buy-walls behind boolean self-buy filters.** Subtracting only CLTV's exact open buy quantity (`load_cltv_buy_qty`) protects against self-wash trades while leaving 468,000-unit rival buy-walls open for bulk liquidation [7].
4. **Enforce a hard fair-value floor on automated bulk liquidation.** A single freighter accidentally dumping 2,000 units of rare ore into a 10-cr scam bid destroys hours of mining output; blocking sales below 70 percent of oracle fair price eliminates catastrophic liquidation errors [3][7].
5. **Unlock parallel origin-to-wall keys on deep buy-walls.** Locking an entire 500+-unit buy-wall to one freighter leaves enormous profit sitting on the table; keying deep walls by `(origin, dest, item)` lets multiple freighters feed the wall in parallel safely [3].
6. **Respect owned-station upkeep floors automatically before sweeping commercial surplus.** Deducting `_hub_upkeep_keep_floor` and `central_depot_targets` inside `pick_surplus_liquidation()` ensures aggressive bulk liquidators never strip Collective Resort Ridgecrest or frontier outposts of fuel, water, or hospitality stock [3].
7. **Keep commercial bulk freighters isolated from stationary desk queues.** Excluding `4B.` mechanically from `bursar-network` and `craft-network` guarantees expensive `Enterprise` and `Frankenhauler` hulls spend 100 percent of their uptime moving high-tonnage revenue loads [4][10].
8. **Verify live faction-withdrawal permissions before assigning faction-storage liquidation jobs.** Checking `_pilot_can_withdraw_faction` inside `haul.py` prevents non-officer pilots from flying deadhead trips to lockboxes they cannot legally withdraw from [3].

## Sources

1. `the-collective:game/upgrade-policy.json` -- Exact `4B. Bulk Trade Haulers` count (`8` Nebula `MCV`) and `dividend -> frankenhauler` freighter ladder.
2. `knowledge/spacemolt-fleet-500-blueprint-and-empire-mechanics.md` -- `4B` commercial freighter role and Nebula hauling architecture.
3. `the-collective:game/fleet/haul.py` -- `pick_surplus_liquidation()`, `assign_optimal_arbitrage()`, `arb-bw:` keys, 70% fair-value floor, and calm buy-wall delivery.
4. `the-collective:game/routes/bursar-network.json` -- Wing lock (`4C.`, `5A.`) keeping `4B` mobile on `haul-network-trade`.
5. `knowledge/spacemolt-rival-strategies-intelligence.md` -- `[IRLC]` (`32 Frankenhauler`) and `[HEXC]` bulk freighter strategies and rival buy-walls.
6. `the-collective:data/store/read.db` -- Live `books` (`arneb` 468k `silver_ore @ 101 cr`, `dheneb` industrial buy-walls) audited 2026-11-27.
7. `the-collective:game/fleet/market_guard.py` -- `load_cltv_buy_qty()`, `is_mirage_arbitrage_trap()`, and `price_oracle.json`.
8. `the-collective:game/fleet/hive.py` -- Live 2026-11-27 Trade profit (`+132,467 cr/h` net) and Mining active throughput.
9. `the-collective:game/fleet/accounting.py` -- IFRS 15 Section 1 External Cash Revenue vs internal Logistics transfers.
10. `the-collective:game/routes/craft-network.json` -- Mechanical `exclude_wing_prefix` keeping `4B` out of docked crafting.
11. `the-collective:game/fleet/escort_proto.py` -- Convoy protection protocol for high-value contested freighter deliveries.

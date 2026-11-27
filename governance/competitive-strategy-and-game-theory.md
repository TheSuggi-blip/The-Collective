# Competitive Strategy & Game-Theory Manual -- The Collective ([CLTV])

> **Scope:** Galactic competitive strategy, microeconomic market dominance,
> game-theoretic combat and extraction rules, vertical integration, and
> open-ended ratcheting KPI governance for The Collective (`[CLTV]`).
> **Indexed:** Mirrored automatically into `read.db:docs` (`kind = blueprint`)
> and `collective-index` hybrid RAG so both live fleet diagnostics and Trinity
> share one verified source of truth.

---

## 1. Strategic Objective: Compounding Real Free Cash Flow & Sovereign Dominance

The Collective does not play SpaceMolt to farm vanity stats, bloat inventory
with illiquid commodities, or hit static "100% green" vanity scorecards. We
compete in an open, multi-faction adversarial economy against top-10 blocs
(`[BUSY]`, `[IRLC]`, `[HEXC]`, `[HIVE]`, `[ENDL]`, `[NOIR]`, `[STLR]`,
`[WEXL]`) to compound **Realized Core Operating Profit (IFRS 15 EBIT, Ex-Seeds)**,
**Core Operating Margin (target >= 30%, elite >= 50%)**, **Enterprise Net
Worth**, **fleet tier (`T0 -> T5`)**, and **sovereign territory (5 stations, 8
outposts)**.

Every AutoNet policy and strategic shift is governed by five formal economic
and game-theoretic principles.

---

## 2. Game Theory of Shared Extraction & Co-op PvE Wildlife Hunting

### 2.1 Co-op PvE vs. Opposing PvP (Strict Dominant Strategy in `hunt.py`)
In SpaceMolt wildlife battles, all hunters attacking a creature join the same
combat side (`side 2`), while the creature (and any hostile PvP interceptor or
NPC pirate) occupies the opposing side (`side 1`). Combatants on the same side
cannot deal friendly-fire damage to one another.

- **Old dominated strategy (strictly `-EV`):** Fleeing whenever ANY non-`[CLTV]`
  pilot joined `side 2` donated ~50 partially damaged creatures per hour (often
  at 6%-10% hull, dropping `2,009 cr` `crystal_melt`!) to `[HEXC]` and rivals
  after `[CLTV]` had already paid the jump fuel and hull wear.
- **Dominant `+EV` strategy (enforced structurally in `hunt.py`):** Inspect
  each non-creature combatant's battle side (`own_side = own[2]`).
  1. **Opposing side (`c[2] != own_side`) or targeting us (`c[9] == pilot`) or
     hostile NPC (`pirate`/`police`):** Immediate tactical `flee` (`-EV` hull
     loss avoidance).
  2. **Same co-op PvE side (`c[2] == own_side`):** STAY and finish the kill.
     Rival pilots on `side 2` supply free DPS at zero friendly-fire risk,
     reducing our ammo, shield wear, and time-to-kill while capturing loot.

### 2.2 Escaping the Tragedy of the Commons in Mining (`3A-3E`)
Common-pool asteroid belts suffer from the classic Prisoner's Dilemma: if all
factions over-harvest the same `5 cr` empire iron belt or dump excess ore into
one station, marginal price collapses while lawless scarce veins (`lead_ore`,
`energy_crystal`, `dark_matter_residue`, `darksteel_ore`, `plasma_gas`) stay
under-exploited.

- **Specialized Wing Partitioning (Division of Labor):**
  - **`3A Precision` (38 ships) & `3C Deep-Core & Rad` (18 ships):** Shielded
    from low-value P3 bulk needs (`< 20 cr/u` like `iron_ore` and `carbon_ore`)
    so precision extractors stay anchored on `32-120 cr/u` lawless and crystal
    veins (`4x-8x` higher value per jump and per fuel credit).
  - **`3B Bulk` (22 ships):** Dedicated industrial feedstock wing feeding
    `steel_plate` and station construction needs without pulling precision hulls
    off scarce veins.
  - **`3D Gas` (40 ships) & `3E Ice` (30 ships):** High-ROF frontier gas and
    ice harvesting (`plasma_gas`, `methane_ice`, `water_ice`, `tritium_ice`)
    converting directly into fleet fuel autonomy and high-margin cash sales.
- **Anti-Flood Liquidity Discipline:** Never mine beyond `85%` of real net
  external buyer depth (`bid_qty - cltv_open_buy_qty`) guarded by
  `market_guard.py`, and route thin scarce pockets with adaptive `1/2/3`-ship
  crowding caps so our own miners never starve each other on empty rocks.

---

## 3. Stackelberg Leadership, Vertical Integration & Double Marginalization

### 3.1 Eliminating Double Marginalization via Sovereign Fuel & Refining Hubs
In industrial organization, paying external station markups on fuel, refining,
and docking creates *double marginalization* -- every ship jump leaks operating
margin to rival station owners and NPC taxes.

- **Fuel Autonomy First:** An owned sovereign station (`Collective Resort
  Ridgecrest`) without a `refueling_dock` is a net working-capital drain:
  miners dock and strand at zero fuel while haulers spend cash on hospitality
  inputs before basic infrastructure is online.
- **Capital Sequencing Rule (enforced in `haul.py` & `wallet.py`):**
  1. **Priority 0 (Infrastructure Foundation):** Until `refueling_dock` stands
     active at an owned station, `fuel_cell` (2,000 build units + buffer) and
     `steel_plate` (800 build units) command emergency urgency (`9.0`, up to 6
     parallel haulers), and non-essential luxury hospitality purchases pause.
  2. **Priority 1 (Public Traffic & Passive Fee Capture):** Once
     `refueling_dock` and `market_terminal` stand online, the station captures
     high-margin passive traffic, slashes fleet paid fuel opex, and opens safe
     refueling for all divisions.
  3. **Priority 2 (Disciplined Hospitality):** Resume resort consumables strictly
     for active owned venues with disciplined unit-price ceilings (`<= 550 cr`)
     and lean buffer stocks (`12-18` units), never tying up millions in
     overpriced gourmet inventories.
- **Unseated Ship Access Control Invariant:** While `[CLTV]` scales faction
  seats (`275 -> 500` via `guild_hall_recruiting`), unseated ships (`pilot not
  in faction_members`) CANNOT dock at faction-only outposts (`Access denied`).
  `hunt_net` and `mine_net` structurally exclude faction outposts for unseated
  pilots and exclude any station missing `refueling_dock`, preventing zero-fuel
  stranding loops.

### 3.2 Working-Capital Velocity & Exotic Loot Liquidation
Inventory sitting in frontier lockboxes (`ramens_rest`, `the_levy`, personal
holds) earns `0%` return and exposes working capital to price decay. High-unit
value exotic drops (`crystal_melt`, `superfluid_vial`, `ember_gland`,
`noble_condensate`, `cobalt_ink` >= `200 cr/u`) carry `5x-20x` higher cash
density per cargo unit than bulk ore. `haul.py` prioritizes calm faction
lockbox pickups and high-unit-value exotic liquidation directly into deep
external buy walls (`Sol`, `Node Beta`, `Krynn`, `Dheneb`) ahead of low-margin
bulk transfers -- converting extracted value rapidly into IFRS 15 Realized
Cash Revenue and Core Operating Margin.

---

## 4. Market Microstructure & Anti-Predation Defense (`market_guard.py`)

Open player exchanges invite three classic predatory attacks:
1. **Wash-Trading / Self-Bid Feedback Loops:** A fleet's own buy orders look
   like "external demand" to naive miners and haulers. Neutralized by
   subtracting `load_cltv_buy_qty` at every `(base, item)` before valuing books
   or triggering arbitrage/mining.
2. **1-Unit Spoof Bids (`425,948 cr x 1`):** Single-unit bait bids inflate
   naive `MAX(bid)` valuations and lure haulers across the galaxy into empty
   books. Neutralized by Cash-Weighted Median (`VWM`) + LULD `+/-30%` TWAP
   bands + single-hub thin-book haircuts (`0.50x` `<10u`, `0.75x` `<25u`)
   materialized cleanly into `read.db:fair_prices` and `clean_books`.
3. **Zero-Fuel Bursar Spread Capture (`4C` & `5A`):** Keeping 55+ docked
   Bursars posted across Empire NPC exchanges and calm lawless trading hubs
   captures bid-ask spread and converts fleet inventory at **0 cr/h flight
   fuel** -- the single cleanest lever for pushing Core Operating Margin above
   `30%` and toward `50%+`.

---

## 5. Open-Ended Dynamic Ratcheting KPIs (Anti-Goodhart Governance)

Static "100% green" targets fail in compounding systems for two reasons:
- **Ceiling Stagnation:** Once a wing hits a static target (e.g., `25k cr/h`),
  a capped `100%` score gives zero incentive to push from `25k` to `250k cr/h`.
- **Sandbagging Across Upgrades:** Upgrading hulls from `T0` to `T3` doubles
  or triples physical capacity; measuring a `T3` wing on `T0` targets masks
  massive underperformance.

The Collective solves both structurally in `kpi_engine.py`:
1. **Fleet North Star -- Core Operating Margin (`IFRS 15 EBIT / Realized
   Revenue`):**
   - `< 0%` = `NEGATIVE` (burning cash -- halt non-essential opex, surge
     liquidation & fuel cuts).
   - `0% - 29.9%` = `BELOW 30%` (profitable but fragile -- tighten low-ROF
     wings, expand 0-fuel Bursar conversion and sovereign refueling).
   - `30.0% - 49.9%` = `TARGET 30%+` (healthy industrial compounding).
   - `>= 50.0%` = `ELITE 50%+` (dominant fortress economics).
2. **Dynamic Tier-Capacity Par (`cap_mult`):** Every wing's par target scales
   automatically with live ship count and average realized hull tier
   (`1.0 + 0.55 * avg_tier`), moving the bar upward every time hulls advance
   `T0 -> T5`.
3. **Unbounded Super-Efficiency DEA Frontier (`> 100`):** Inspired by
   Andersen-Petersen Super-Efficiency Data Envelopment Analysis, open-ended
   output and efficiency KPIs (`Value/h`, `Loot/h`, `Revenue/h`, `ROF`,
   `Crafted Value/h`, `Sales/h`, `Scans/h`, `Freshness`) follow a smooth
   logarithmic super-efficiency curve above par (`100 + 38 * ln(val / par)`).
   There is no artificial 100% cap: better performance always earns a higher
   score, while diminishing log slope prevents single-metric gaming.
4. **Ratcheting High-Water Marks (`kpi_hwm.json`):** Each wing's sustained 6h
   peak ratchets upward via anti-spike EWMA (`alpha = 0.30`). Beating the
   wing's standing HWM by `> 2%` earns a `+6` Breakout Bonus (`NEW PEAK!`),
   permanently resetting the frontier higher.
5. **5 Competitive Ranks:** `ALARM (<60)` -> `WARN (60-79)` -> `SOLID (80-99)`
   -> `OUTPERFORM (100-119)` -> `APEX (120+)`. Safety and hygiene metrics
   (`Idle Rate -> 0%`, `Ships Lost -> 0`, `Outpost Bunkers`, `Supply SLA`,
   `Mine Yield`) remain bounded `[0, 100]` as non-negotiable defensive brakes.

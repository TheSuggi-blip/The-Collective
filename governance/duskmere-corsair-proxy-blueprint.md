---
name: duskmere-corsair-proxy-blueprint
id: 20261127T001600Z
tier: strategy
author: Trinity
links: [governance/fleet-500-redesign-blueprint.md, game/rules/08-combat.md, game/rules/09-factions.md, game/rules/11-public-data.md]
---

# Far-Future Corsair Proxy Faction Blueprint (`Duskmere -> TOI-700` Locked Fortress)

Status: **FAR-FUTURE CONTINGENCY BLUEPRINT (Execute ONLY after CLTV reaches T3+ fleet maturity & abundant surplus cashflow).**
Target Base Cluster: **`duskmere -> toi_700`** (`5` unoccupied lawless systems sealed behind ONE single jump chokepoint on the exact far-eastern edge of the galaxy, `X: +5817..+6615, Y: +418..+1293`, `17--28` jumps opposite CLTV!).

---

## 1. Strategic Objective & In-Game Deniability Analysis

**Mission:** Operate an independent, ultra-heavy `100`--`120` ship pirate/mercenary war faction ("Corsairs") on the opposite side of the galaxy to raid rival supply lines, contest rival strongholds, harass rival blocs (`[BUSY]`, `[DEAD]`, `[BEIN]`, `[HEXC]`, `[IRLC]`), and act as a deniable strategic distraction -- **with ZERO diplomatic link to `[CLTV]` and ZERO in-game forensic trail tying it back to `[CLTV]`**.

### What Rival AI Agents Can Actually See In-Game (`11-public-data.md`, `feed.json`, `0.735.1`)

Assuming zero out-of-game leaks, rival AI intelligence pipelines only see **five in-game data surfaces**:
1. **Daily Public Bulk Feed (`assets.spacemolt.com/public/v1/manifest.json` -> `feed.json`):** Every pilot's `name`, `empire`, `faction`, `created` (date), and lifetime `stats` (`ships_destroyed`, `ships_lost`, `pirates_destroyed`, `ore_mined`, `credits_earned`, `trades_completed`, `systems_explored`, `time_played`), plus every faction's `members`, `leader`, `allies`, `enemies`, `wars`, and monthly `battles.ndjson` (every ship & faction tag in combat).
2. **Hourly Top-30 Leaderboards (`/api/leaderboard`):** Top-30 `players`, `factions`, `exchange` (`escrow_value`, `sell_order_value`), and `stations`.
3. **Faction & Pilot Dossiers (`/faction/<TAG>`, `/player/<name>`):** Roster, roles, join dates, allies, stations.
4. **Remote Galaxy Order Books (`view_market base_id=...`):** Any docked rival ship can read live bids & asks at **any charted station** in the galaxy.
5. **In-System Sightings (`met` / `get_system` / `public_battles`):** Exact hull classes, faction tags, co-docked ships, and combat tactics observed in space.

**CRUCIAL FACT:** SpaceMolt does **NOT** expose a public transaction graph! Rivals **cannot** see `send_gift`, `trade_offer`, or `jettison` transfers directly -- they can ONLY detect patronage via **indirect correlations**: co-docking sightings, bizarre wash-trade prices in `view_market`, mirrored hourly wealth spikes on Top-30 leaderboards, synchronized registration bursts/downtime blackouts, cloned ship/combat signatures, or obvious targeting asymmetry.

---

## 2. Covert In-Game Funding Playbook: YES, You CAN Fund Them Safely!

You do **NOT** have to force them to be 100% self-funded from zero -- you **CAN** covertly finance them from `[CLTV]` in-game with near-zero detection risk by combining **three layered channels** and obeying strict anti-forensic rules:

### Layer A -- Organic Startup Seed (`6M--12M cr`, 0% Traceability)
- Have the `100`--`120` Corsair pilots run their own Empire starter missions + early bounties during their staggered `2--4` week onboarding phase (`~50k--100k cr/pilot` = `6M--12M cr` pure NPC credits).
- **Why vital:** Populates authentic `missions_completed`, `credits_earned`, and `systems_explored` histories in `feed.json` so their wealth never appears out of thin air on day 1!

### Layer B -- Covert `[CLTV]` Capital Injection ("2-Hop Unaffiliated Neutral Cutout" -- 100% Value Preserved, 0% Direct Link!)
- **Setup:** Maintain `2`--`3` **unaffiliated neutral merchant accounts (`faction: ""`)** registered weeks earlier with normal trade/mining histories (blending invisibly among SpaceMolt's `10,795+` factionless solo players!). NEVER invite them to `[CLTV]` and NEVER invite them to `[CORSAIR]`.
- **Hop 1 (`[CLTV]` -> Neutral Cutout):** At a **high-traffic NPC Capital** (`Grand Exchange` or `Central Nexus`, where dozens of unrelated ships dock nonstop so co-docking is meaningless noise!), transfer credits via `send_gift` OR high-density crafted goods/modules/components via `trade_offer` in **staggered tranches (`2M--5M cr` spaced across different days)** so neither side triggers a synchronized hourly Top-30 `leaderboard.json` spike.
- **Hop 2 (Neutral Cutout -> Corsair Banker):** Wait `12--48 hours`, then deliver at a **different busy neutral/empire station** via `send_gift` (credits) OR via a **deep-space `jettison` dead-drop** at an empty unmonitored POI (`10`-minute container scoop for ultra-dense assets like a `station_core` or T4 weapon/module crate -- zero station docking log, zero `view_market` order, zero `battles.ndjson` entry, `100%` item preservation!).
- **Optional High-Theater Cover (Use Only for Bulk Goods, Mind RNG Drop Loss):** A Neutral Cutout hauler flying through a lawless lane near `Duskmere` gets "ambushed" by a Corsair wolfpack (`battles.ndjson` records an authentic pirate kill on a random independent freighter!). Note: wreck destruction may destroy a fraction of cargo, so reserve `send_gift` + `jettison` dead-drops for `station_core` and expensive T4/T5 kits.

### Layer C -- Long-Term Fortress Self-Sustainability Inside `TOI-700`
- Once seeded into their locked `TOI-700` fortress with a Shipyard + Refinery, `15--20` internal support ships mine `Copperfield` / `Rustpoint` / `TOI-700`'s built-in resources (`iron`, `copper`, `aluminum`, `water_ice`, `deuterium`, `helium`, `plasma_gas`, `argon`, `neon`) while Corsair armadas loot T3--T5 enemy wrecks, claim boarded prizes (`claim_prize`), and collect safe-passage extortion tolls (`trade_offer offer_safe_passage=true`). This minimizes ongoing funding transfers during peacetime!

### STRICT "NEVER DO" RED LINES (Instant Detection Mistakes!)
1. **NEVER** have a `[CLTV]` ship dock at a `[CORSAIR]` station or meet a `[CORSAIR]` ship at a quiet frontier outpost.
2. **NEVER** wash-trade on an Exchange (`1 iron_ore @ 10,000,000 cr`) -- rival `view_market` bots catch price outliers across the entire galaxy in seconds.
3. **NEVER** fund via `[CLTV]` Faction Missions (`open_to_all` shows `[CLTV]` as the poster!).
4. **NEVER** transfer `50M+ cr` in one lump sum during a single leaderboard hour.
5. **NEVER** register `120` pilots on the same date (`feed.json` `created` date) or share `[CLTV]`'s VPS reboot schedule (synchronized `0`-online blackouts expose shared hosting!).
6. **NEVER** link diplomatically (`propose_ally`), share federation colors, mention `[CLTV]` in chat, or copy CLTV's Culture prefixes (`GSV`/`ROU`) or `80%` flee combat parameters.

---

## 3. Fortress Architecture: The `duskmere -> toi_700` Locked 5-System Vault

Graph bridge analysis confirmed `duskmere -> toi_700` is the **#1 unoccupied single-chokepoint 5-system fortress in SpaceMolt** (`17J` from `GSC-0044`, `22J` from `Felis`, `28J` from `Atria` -- sitting right on the Eastern doorstep of `[HEXC]` `11J`, `Haven` `13J`, `[IRLC]` `16J`, `[BUSY]` `18J`, and Crimson space!):

```text
[Outer Galaxy] <---> duskmere (5 exits: staging/ambush porch)
                         ||
                    [SINGLE CHOKEPOINT BRIDGE]
                         ||
                     toi_700 (3 exits: GATEKEEPER CITADEL -- Station #1 Battle Fortress + Sensors + Fuel)
                    /       \
            rustpoint       copperfield (8 resources: CENTRAL INDUSTRIAL & SHIPYARD HUB -- Station #2/#3!)
            (iron/copper)     /       \
                         praecipua   taiyi
                         (aluminum)  (helium/nitrogen ice -- DEEP RESERVE & CLONE SANCTUARY!)
```

- **Kill-Box Defense:** Every single attacker entering the 5-system cluster MUST pass through **`duskmere -> toi_700`**. Station #1 at `TOI-700` mounts full `Shield Bastion`, `Integrated Fire Director`, `Siege Lance`, `Bulwark Plating`, `Heavy Defense Batteries`, `Long-Range Subspace Sensor` (sees incoming fleets `2` jumps out through `duskmere`, `edgewater`, `dusthaven`, `minkar`, `mothallah`!), and permanently docked quick-reaction strike armadas!
- **Internal Self-Sufficiency:** All 5 interior systems contain `iron_ore`, `copper_ore`, `aluminum_ore`, `water_ice`, `deuterium_ice`, `helium_ice`, `nitrogen_ice`, `hydrogen_gas`, `argon_gas`, `neon_gas`, and `plasma_gas` -- enough to fuel, repair, and fabricate hulls/ammo entirely behind the sealed gate!

---

## 4. Alien Fleet Design (`115` Ships -- Zero Resemblance to `[CLTV]`)

To guarantee rivals cannot fingerprint our fleet design as `[CLTV]`:
- **Birth Empire Composition:** **Crimson (`55%`) + Voidborn (`30%`) + Outer Rim (`15%`)** (radically different from CLTV's Solarian/Nebula industrial majority!).
- **Naming Convention:** Zero 3-letter naval prefixes (`GSV`/`ROU` forbidden!). Use raw, varied pirate/mercenary callsigns & single/compound slang names registered organically over `2--4` weeks (e.g., *Rustjaw*, *Ashfang*, *Vesper-9*, *Kestrel-Zero*, *Red Wake*, *Null Hound*, *Brimstone*, etc.).
- **Hull & Combat Doctrine (Ultra-Heavy Pirate Captain Armada Style):**
  - **Strike Armada Alpha (`30` ships):** Heavy Crimson/Voidborn alpha-strike & siege brick (`14` Crimson `Annihilator` / `Crimson Devastator` / `Warmaul` heavy gunships + `6` Voidborn `Event Horizon` / `Apotheosis` drone/shield anchors + `4` `Paradox Engine` / `Aporia` warp-disruptor interdictors + `4` `Cauterizer` / `Pleroma` combat medics + `2` dedicated boarding/marine assault hulls).
  - **Strike Armada Beta (`30` ships):** Identical 30-ship heavy hammer for synchronized two-front raids or 60-ship capital sieges.
  - **Strike Armada Gamma (`30` ships):** High-speed cloaked wolfpack & commerce raiders (`20` cloaked/fast Crimson & Voidborn ambush strikers + `6` Interdictors with `warp_disruptor` + `stasis_webifier_ii` + `4` fast Combat Salvage / Prize Recovery tenders with `outer_rim_salvage_array` + `advanced_tow_rig`).
  - **Internal Fortress Support Wing (`20`--`25` ships, NEVER leaves `TOI-700` except cloaked recon):** `8` cloaked deep-recon scouts (`Vesper` hunters watching rival mining/hauler lanes), `10` internal `Copperfield`/`Rustpoint` miners & crafters feeding the fortress foundry/fuel bunkers, `4` fortress fuel/ammo tenders, `3` docked shipyard/storage bankers.

---

## 5. Dedicated `pirate_net` Autonomous Raider Architecture (Future Standalone Repo)

Runs in a **100% separate container/host with staggered restart times** (NEVER inside `/srv/collective/the-collective`):

1. **Recon & Target Scoring (`scout_prey`):** Cloaked forward scouts map rival lawless mining belts, unarmed hauler corridors, and unguarded outposts within `4`--`12` jumps of `duskmere` (especially `[HEXC]`, `[BUSY]`, `[IRLC]`, Nebula/Crimson trade choke lanes), ranking targets by cargo/hull value vs local escort density.
2. **Coordinated 30-Ship Armada Jump & Tackle (`wolfpack_strike`):**
   - Interdictors drop cloak/jump in FIRST (`warp_disruptor` + `stasis_webifier` locking high-value targets in system!).
   - Main gunship/carrier/medic fleet follows on the next tick via `spacemolt_fleet` + synchronized `attack` focus-fire (`target_id` lowest EHP/highest value first).
   - **Aggressive Corsair Discipline (Distinct from CLTV):** Uses `brace` + remote-rep sustain rather than instant `80%` flee; disengages cleanly via fleet recall ONLY if overwhelmed (`enemy_power > 1.35 * pack_power` or medic loss) or objective killed.
3. **Battlefield Plunder & Prize Extraction (`plunder_and_tow`):** Dedicated `outer_rim_salvage_array` + `advanced_tow_rig` tenders immediately loot cargo, field-scrap wrecks, and tow disabled prizes back through `duskmere -> toi_700`!
4. **Extortion & Mercenary Contracts (`toll_net`):** Automatically issues `trade_offer offer_safe_passage=true request_credits=...` to captured commercial traffic and accepts anonymous third-party war/harassment bounties to reinforce authentic mercenary cover!
5. **Kill-Box Home Defense (`gate_sentinel`):** Any non-Corsair fleet detected by `TOI-700`'s `Long-Range Subspace Sensor` entering `duskmere` triggers an instant recall of nearby armadas to form an iron wall on the `TOI-700` side of the bridge alongside station defense batteries!

---

## 6. Updates Implemented (`2026-11-27`): Shared `read.db` Intel Tap, Drip-Feed Noise-Floor Math, Naming Tradeoff & `pirate_net.py`

1. **Zero-Recon Intel Tap (Zero In-Game Footprint!):** `game/fleet/pirate_net.py` reads CLTV's live `read.db` strictly read-only (`?mode=ro&immutable=1`) with zero in-game `ally_intel_opt_out` or Intel Center links, freeing 100% of Corsair seats for combat (`90` warships + `15` Plunder/Tow + `15` Fortress Support). To prevent timing-correlation leaks when CLTV scouts scan a system, `pirate_net.py` enforces a deterministic **`180--720s` anti-correlation jitter** before raiding newly scanned systems and hard-excludes all `CLTV` tags and systems within `10` jumps of CLTV's Western core.
2. **Drip-Feed Funding Math (Why Slow Continuous Funding Is Hidden In-Game):** Live `feed.json` publishes daily player `credits_earned` (NOT current wallet balance or `credits_spent`), and `leaderboard.json` publishes hourly Top-30 `total_wealth` only. Because CLTV's net worth oscillates naturally by `+/- 10M--30M cr/day`, drip-feeding **`300k--2.0M cr` staggered irregular tranches** via `2--3` unaffiliated neutral cutouts (`faction: ""`) at crowded Empire Capitals sits far below CLTV's statistical noise floor while Corsair leveling/pirate-hunting builds legitimate `credits_earned` stats.
3. **Naming Engine (`pirate_net.py roster`):** Built with both **`barcode`** (`20`-char balanced `I`/`l` strings -- maximum human visual dread & anti-manual target-calling, though AI scripts parse `0x49` vs `0x6C` trivially and immediately tag uniform barcodes as a single coordinated bot swarm) AND **`organic_pirate`** (messy heterogeneous mercenary handles -- strictly stronger camouflage against rival AI forensic clustering).
4. **3-Phase Auto-Lifecycle Built & Wired (`game/fleet/pirate_net.py`, `game/pirate-policy.json`, `game/routes/pirate-network.json`):** Kept **double-locked DISABLED** (`enabled: false`, `raiding_enabled: false`, `status: "off"`, `requires.wing_prefix: "CORSAIR-"`) so zero live CLTV ships ever touch it; seamlessly runs `leveling` (Piloting `< 20` / Tier `< 3` safe XP farming) -> `staging` (`toi_700` 30-ship armadas) -> `raiding` (`wolfpack_strike` + `plunder_and_tow` + `toll_net` + `gate_sentinel`).

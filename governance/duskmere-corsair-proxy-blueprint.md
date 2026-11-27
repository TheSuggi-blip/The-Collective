---
id: 20261127T000815Z
title: Duskmere / TOI-700 Isolated Corsair Proxy Blueprint (107-Ship 4-Empire Doctrine)
kind: blueprint
status: active
owner: Trinity
updated: 2026-11-27
---

# Duskmere / TOI-700 Isolated Corsair Proxy Blueprint

## 1. Strategic Mandate & Hard Separation

The Corsair Proxy is an autonomous 107-ship privateer/pirate faction operating out of the 1-lane dead-end **TOI-700 Fortress Pocket** (`toi_700` Gatekeeper Citadel + 4 interior systems: `copperfield`, `rustpoint`, `praecipua`, `taiyi`, guarded by an outer chokepoint watch at `duskmere`).

**Account & Runtime Isolation (Rule R22 -- Zero Overlap with CLTV):**
- **Dedicated SpaceMolt Account #2 (Separate Clerk User):** Registered under a completely separate SpaceMolt website/Clerk account and Game Client API key from `[CLTV]`. This ensures zero database linkage via `listOwnedPlayers()`, zero shared engine sessions, and zero possibility of CLTV's `wallet.py`, `dispatch.py`, or `accounting.py` sweeping or commanding Pirate pilots.
- **Defense-in-Depth Collector Guard:** `station/fleet.py` reads `/srv/collective/data/pirates/roster.tsv` and unconditionally excludes Pirate pilot names from CLTV's `fleet.json`, `totals`, `history.json`, and `rejoin`.
- **Private Data Store Outside Git:** Live Pirate pilot handles, credentials, fortress sites, and telemetry live strictly in `/srv/collective/data/pirates/` (`config.json`, `roster.tsv`, `sites.tsv`, `fleet.json`, `empire.json`), never committed to any repository.
- **No Direct Credit Trails:** Zero `gift_credits` between `[CLTV]` and the Corsair faction. Pirate wealth compounds organically via Phase 1 solo mission/bounty farming and Phase 3 prize-tow + plunder + safe-passage tolls.

## 2. Finalized 107-Ship Non-Round Fleet & Optimal 4-Empire Split (Zero Nebula)

Non-round prime target (`107` ships) avoids synthetic bot-farm fingerprints (`100` / `120` / `500`). Naming defaults to **`organic_pirate`** (messy heterogeneous human-style handles rather than uniform barcodes, which stand out to rival analytics once grouped under one faction tag).

| Empire | Ships | Share | Strategic Role & Racial Advantage |
| :-- | --: | --: | :-- |
| **Crimson** | **43** | 40.2% | `+8%` weapon damage + `crimson_fury` -> Gunships, Heavy Brawlers, Boarders, Armored Frontline Salvagers |
| **Voidborn** | **25** | 23.4% | `+12%` max shield + cloak/energy -> Carriers, Shield Tanks, Combat Medics, Cloaked Ambush Boarders |
| **Outer Rim** | **21** | 19.6% | `+10%` in-system speed + `outer_rim_survival` salvage/repair + **`1.5%` lowest corporate tax domicile (Founder MUST be Outer Rim)** -> Command/Founder, Plunder & Tow Wing, Fast Tackle Interdictors, Vault Crafters/Tankers |
| **Solarian** | **18** | 16.8% | `+3%` all 5 attributes + `solarian_doctrine` (`+1%/lvl` accuracy) -> Precision Snipers/Interdictors (hitting evasive rival haulers/liners) + Vault Miners (`copperfield`/`rustpoint`) |
| **Nebula** | **0** | 0.0% | Excluded -- trading/industry bonuses belong in `[CLTV]`, not a pure war/plunder armada |
| **Total** | **107** | **100.0%** | **5 divisions, 0 scouts (taps CLTV `read.db` read-only with 3-12 min jitter)** |

### Division Breakdown (Mirrored in HUD `Pirates` Fleet Tab Below `Intel`)

1. **Armada Alpha (29)** (`CORSAIR-Alpha`): 1 Outer Rim Founder Command, 10 Crimson Gunships, 5 Crimson Heavy Brawlers, 3 Crimson Boarders, 4 Voidborn Carriers, 4 Solarian Precision Interdictors, 2 Voidborn Medics.
2. **Armada Beta (28)** (`CORSAIR-Beta`): 1 Crimson Command, 9 Crimson Gunships, 5 Crimson Heavy Brawlers, 3 Voidborn Boarders, 4 Voidborn Carriers, 4 Solarian Precision Interdictors, 2 Voidborn Medics.
3. **Armada Gamma -- Wolfpack (26)** (`CORSAIR-Gamma`): 1 Outer Rim Command, 6 Crimson Gunships, 4 Outer Rim Fast Brawlers, 4 Voidborn Ambush Boarders, 5 Solarian Precision Interdictors, 3 Outer Rim Fast Interdictors, 3 Voidborn Medics.
4. **Plunder & Tow Wing (13)** (`CORSAIR-Plunder`): 7 Outer Rim, 4 Crimson, 2 Voidborn specialized salvage, loot-scoop, and intact prize-ship towing hulls.
5. **Fortress Vault Support (11)** (`CORSAIR-Vault`): 5 Solarian Miners, 3 Outer Rim Crafters, 2 Outer Rim Tankers, 1 Voidborn Banker locked permanently inside the TOI-700 pocket.

## 3. Staggered Growth & Autonomous Lifecycle (`game/fleet/pirate_net.py`)

- **Staggered Birth Cadence:** Launch **3-4 ships every 2-3 days** (~60-day organic ramp) so public creation timestamps (`feed.json`) never show a synchronized bot-farm spike.
  - **Wave 1 (Day +0):** 1 Outer Rim Founder Command (`1.5%` tax domicile), 1 Crimson Gunship, 1 Solarian Interdictor, 1 Voidborn Carrier.
- **Phase 1 (Leveling):** Pilots run safe solo combat/missions until `piloting >= 20` and T3 hull (`tier >= 3`). Zero PvP before T3.
- **Phase 2 (Staging):** Relocate to `toi_700` pocket, construct Gatekeeper Citadel + interior Vault outposts, fit warp disruptors + stasis webifiers + brace tanks.
- **Phase 3 (Raiding & Plunder-and-Tow):** Disabled by default (`raiding_enabled: false`). When enabled, strikes lawless rival operations >= 10 jumps outside CLTV Western core using read-only `read.db` intel with 180-720s anti-correlation jitter, strictly excluding `CLTV`.

## 4. HUD Command Visibility (CRIMSON RED)

- **Galaxy Map (`Pirate ops` layer, `#ef4444`):** Renders TOI-700 fortress space (double crimson border), Citadel/Fortress/Choke markers, built Pirate stations/outposts, and live Pirate ship tokens in crimson red -- mirroring CLTV's green (`#86d65b`).
- **Left Fleet Outliner (`Pirates` tab below `Intel`):** Collapsible division with all 5 sub-groups showing live/planned counts (`0/107` -> `107/107`) without ever inflating CLTV's 500-ship roster or financial metrics.


## 9. Collective Runner Deployment & Accelerated 7-Wave Birthplan (2026-11-27)

- **Runtime Location:** Runs strictly inside The Collective's sealed gVisor runner container (`the-collective-runner-1`) under `/srv/collective/pirates/` (supervised by `/srv/collective/services/pirate-runner/run`) using SpaceMolt Account #2 credentials (`PIRATE_SPACEMOLT_CLERK_API_KEY` + `PIRATE_SPACEMOLT_REGISTRATION_CODE`, separate SpaceMolt account from `[CLTV]`).
- **Direct Shared Intel Tap:** Reads `/srv/collective/data/store/read.db` strictly read-only (`?mode=ro` via `intel_tap.py`) to route Phase-1 leveling ships to undepleted empire ore belts and Phase-3+ raids to verified lawless rival targets while strictly excluding `[CLTV]` systems and tags.
- **Accelerated 7-Wave Birthplan (107 ships in 17 days, irregular non-round wave sizes):**
  - Wave 1 (Day 0): `11` ships (1 Outer Rim command Founder, 4 Crimson gunships, 1 Crimson heavy_brawler, 2 Voidborn carriers, 2 Solarian interdictors, 1 Voidborn medic)
  - Wave 2 (Day 3): `14` ships (cumulative `25`)
  - Wave 3 (Day 5): `17` ships (cumulative `42`)
  - Wave 4 (Day 8): `16` ships (cumulative `58`)
  - Wave 5 (Day 11): `18` ships (cumulative `76`)
  - Wave 6 (Day 14): `15` ships (cumulative `91`)
  - Wave 7 (Day 17): `16` ships (cumulative `107`)

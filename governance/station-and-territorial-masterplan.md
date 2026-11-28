---
name: station-and-territorial-masterplan
id: 20261127T000813Z
tier: strategy
author: Trinity
links: [governance/empire.md, governance/fleet-500-redesign-blueprint.md, game/map/sites.tsv]
---

# Station & Western Sovereign Empire Masterplan (5 Stations + 8 Outposts)

Approved Direction: Suggi (2026-11-27) | Live Map Audit: `read.db` (`521` systems, `0.735.1` catalog)

## 1. Rival Clutter Diagnosis & Western Sovereign Arc Thesis

Galactic coordinate mapping (`X: [-6957, +6914]`, `Y: [-7554, +6948]`, where `-Y` is North/Top and `-X` is West/Left) proves our rivals are heavily congested in the **East & Center**:

- **South-East Megacluster (`X +1875..+5954, Y +3027..+6197`):** `[BUSY]`, `[DEAD]`, `[BEIN]`, and `[MOON]` stack **20 stations** on top of one another.
- **Central / North-East Corridor (`X -1756..+3980, Y -4117..+2605`):** Crowded by `[HEXC]` (2 stations, 9 outposts), `[IRLC]` (3 stations, 5 outposts around `LHS 1140`), `[HIVE]` (3 stations), `[BEAT]`, and `[CRFT]`.
- **WIDE-OPEN WESTERN SOVEREIGN ARC (`X -6600..-1500, Y +4632..-4423`):** Sweeping from our South-West outpost **`Felis` (`-2560, +4632`)** -> West **`Atria` (`-5650, +2222`)** -> Mid-West **`Yildun`/`Avior`/`GSC-0042`/`Dabih`** -> North-West just **below and west of Outer Rim (`Tarazed` / `Ancha`)** holds **ZERO major rival stations** (`3--5` jumps clear of every rival bloc!), rich multi-resource systems (`7--11` resources each), and seamless bridge access through `GSC-0044` straight to central **`Ridgecrest`**.

**Strategic Doctrine:** Plant **Station #1 (Resort & Travel Hub)** at central **`Ridgecrest`** to vacuum galactic tourism & cross-empire commerce, while locking down the **entire Western Sovereign Arc (South-West `Felis` -> West `Atria`/`Yildun` -> Below & West of Outer Rim)** with Stations #2--#5 and Outposts #4--#8!

---

## 2. Five Player-Owned Stations (Build Order & Locations)

Every station requires `1x station_core` + `5,000,000 cr` founding fee in an open lawless system (`5` station cap, `0` facility rent on own stations).

| Build Order | Station Archetype | Target System (`x, y`) | Why This Exact System | Core Facilities & Add-On CapEx |
| :---: | :--- | :--- | :--- | :--- |
| **#1 (FIRST)** | **Resort & Travel Hub** | **`Ridgecrest`** `(-1659, -835)` *(CHOSEN -- Flag live on HUD!)* | `1J` off Solarian border, degree `6`, **#1 galactic centrality** (`11.2J` avg to all 5 empire capitals: `Sol 4J`, `Frontier 9J`, `Nexus 10J`, `Haven 12J`), `4J` from `GSC-0044`, `6--7J` clear of rival resorts (`Dheneb`/`LHS 1140`). | All `15` Dining/Leisure venues (`6.69M cr` total) + `Transit Concourse` (`9M`, `150` pax) + `Refueling Dock` + `Trade Exchange` (`1.5M`) + defenses. Proven `215M--241M cr` passive revenue model (`[BUSY]`/`[HEXC]`) + unlocks `6B` T2+ Liners (`transport_net.py`). |
| **#2** | **Grand Trade Exchange & Commercial Hub** | **`Acrux`** `(-1525, +610)` *or* **`Nembus`** `(-2033, -728)` | `Acrux` sits `1J` off Solarian AND `1J` from `GSC-0044` (`42` systems within `4J`, deg `5`); `Nembus` sits `1J` from `Ridgecrest` (`3J` from `GSC-0044`, deg `6`, `7--8J` clear of rival hubs). Both link our Western core directly into central trade flows. | `Trade Nexus` (`13.5M`) + `Commerce Hub` (`4.5M`) + `Company Exchange` (`5M`) + `Grand Recruitment Bureau` (`20M`, `1,000` seats) + `0-10%` buyer market fee (`0%` for CLTV). |
| **#3** | **Heavy Industrial & Station-Core Foundry** | **`Lanternwick`** `(-1563, -121)` *or* **`Avior`** `(-5842, -450)` | **`Lanternwick`:** `1J` off Solarian, `2J` from `GSC-0044`, **`9` gas/industrial resources** (`argon`, `chlorine`, `hydrogen`, `ion`, `neon`). **`Avior` (Western Heartland):** **`11` resources** (`nebula_gas`, `xenon_gas`, ores/ices), `6J` north of `Atria`, `3J` clear of all rivals, anchors the mid-West industrial belt! | Zero-rent `Station Core Foundry` (`38M`) + `Precision Foundry` (`13.5M`) + `Faction Office` (`+30%` production speed) + T3/T4 module & hospitality food factories. |
| **#4** | **Naval Shipyard & Fleet Drydock** | **`Yildun`** `(-5474, +89)` *or* **`Atlas`** `(-2454, +854)` | **`Yildun`** (existing Suggi-chosen Western choke point between `Atria` and Outer Rim, safe deep-West sanctuary) OR **`Atlas`** (`1J` from `GSC-0044`, `7` resources incl. `null_matter`/`nebula_gas`/`xenon_gas`, `4J` clear of rivals for instant frontline fleet refits). | `Faction Shipyard Dock/Drydock/Complex` (`15M/40M/100M`) + `Fleet Yards` (`13.5M`) + `Regenerative Medical Complex` (`13.5M`) + `Mobile Base` construction bay. |
| **#5 (LAST)** | **Battle Station / Frontier Fortress & Jump-Gate Bastion** | **`Tarazed`** `(-4546, -2798)` *or* **`GSC-0012`** `(-3032, +3741)` | **`Tarazed`:** Just below & west of Outer Rim (`5J` from `Frontier`, `30` systems within `3J`, deg `5`, `7` resources incl. `deuterium`/`tritium`/`helium_ice`) -- locks our northern Outer Rim flank! **`GSC-0012`:** `2J` north-west of `Felis`, `9` resources (`null_matter`/`xenon_gas`), locks our southern flank! | `Shield Bastion` (`3.2M`) + `Integrated Fire Director` (`3.0M`) + `Bulwark Plating` (`2.8M`) + `Siege Lance` (`2.6M`) + `Long-Range Subspace Sensor` (`12M`, `2J` POI scan) + paired **Jump Gate** to `Ridgecrest`! |

---

## 3. Eight Sovereign Outposts (`3` Built + `5` Open Slots -- Full Western Arc Coverage)

Outposts cost only `100k cr` + `outpost_kit`, carry zero maintenance/rent, and provide free fleet refueling + shared Faction Storage across our entire Western Sovereign Arc:

| # | Status | System (`x, y`) | Quadrant / Corridor | Why It Locks the Arc |
| :-: | :---: | :--- | :--- | :--- |
| **1** | **BUILT** | **`GSC-0044`** `(-2086, +722)` | Center-West Bridge | Core link between Voidborn, Solarian, and `Ridgecrest` (`4J` away). |
| **2** | **BUILT** | **`Atria`** `(-5650, +2222)` | Far West (Voidborn flank) | `10` resources (`gold`, `aluminum`, `argon`, `deuterium`); western industrial anchor. |
| **3** | **BUILT** | **`Felis`** `(-2560, +4632)` | South-West Anchor | `7` resources (`energy_crystal`, `null_matter`, `deuterium`); southern flank hub. |
| **4** | **PLAN** | **`Okab`** `(-3936, +4009)` | Deep South-West (`3J` W of `Felis`, `7J` S of `Atria`) | **`5J` clear of ALL rivals** (safest spot in the South-West!), deg `5`, `7` resources (`energy_crystal`, `nebula_gas`), bridges `Felis <-> Atria`. |
| **5** | **PLAN** | **`GSC-0049`** `(-5894, +3073)` *or* **`Marfik`** `(-5582, +2440)` | Far-West Rare Metals (`1--2J` from `Atria`) | `GSC-0049` carries **`platinum_ore` + `iridium_ore`** (`7` res, `3J` clear of rivals); `Marfik` carries `10` res (`titanium_ore`, `energy_crystal`). |
| **6** | **PLAN** | **`GSC-0042`** `(-6201, -71)` *or* **`Avior`** `(-5842, -450)` | Mid-West Corridor (between `Atria` & Outer Rim) | `9--11` resources (`deuterium`, `xenon_gas`, `nebula_gas`), `3J` clear of rivals; steps straight north from `Atria` toward Outer Rim. |
| **7** | **PLAN** | **`Dabih`** `(-6593, -2213)` | Far North-West Rim (West of Outer Rim) | **`11` resources** (`deuterium_ice`, `nebula_gas`, ores/ices) anchoring the far-western rim below/west of Outer Rim (`10J` from `Frontier`). |
| **8** | **PLAN** | **`Ancha`** `(-5224, -4423)` | Top North-West Anchor (West-Northwest of Outer Rim) | Degree `6` super-junction, **`9` resources** (`helium_ice`, `nebula_gas`, `xenon_gas`), `3J` clear of all rivals -- caps the entire Western Sovereign Arc cleanly! |

---

## 4. Live Station #1 (`Collective Resort Ridgecrest`) Operations & Phase-2 Build Plan (2026-11-28)

1. **Station #1 Online (`a2cee88abdcb31db229c04315f0ef6e1` in `ridgecrest`):**
   - **Active Core & Hospitality Stack:** `12` hospitality/resort venues built (`47` max Appeal capacity, `#4` live galaxy Appeal climbing as venues fill), **`Transit Terminal L2`** (`94b7af55d87a489afe350840ec0bb056`, **`60` berths, `+180` tick extension, `0 cr/cycle` rent**) **ONLINE**, **`Refueling Dock`** (`refuel=public`), **`L4 Guild Hall Recruiting`** (`500/500` fleet seated, `0 cr/cycle` rent), and **`Faction Workshop`** (`0 cr/cycle` rent, `0` labor).
   - **Legacy NPC Rent Pruning:** `Nexus Prime` (`central_nexus`) `recruitment_desk` + `faction_lockbox` dismantled (`0` rent saved `-173 cr/cycle`).
2. **Automated Phase-2 Build Ladder (`needs.tsv` + `wallet.py:STATION_BUILD_PRIORITY`, `STATION_BUILD_FLOOR = 200,000 cr`):**
   - **#1 `The Golden Table`** (`700k cr`, L3 Dining `+7` Appeal -> **`54` max = `#1` galaxy** + L3 First-Class `6x` dining multiplier; `100%` construction materials already staged in Ridgecrest storage).
   - **#2 `Fuel Tank Expansion`** (`500k cr`) -> **#3 `Trade Concourse`** (`500k cr`, auto `market=public`) -> **#4 `Repair Slip`** (`500k cr`, auto `repair=public`).
   - *Deferred:* `Transit Concourse L3` (`9M cr`, `150` berths) after Phase-2 + T2 fleet scale-up; `The Leviathan Table` (`1.5M`, boss-drop gated) deferred to late game.
3. **Closed-Loop Supply & On-Site `5A` Kitchen (`craft_net.py`, `haul-policy.json`):**
   - `5A`/`5B` docked at Ridgecrest hand-craft `14+` resort dishes + `fuel_tank` + `repair_kit` straight into faction storage (`deliver_to="faction"`, `0` rent, `0` jumps); empire-facility specialties (`nebula_stellar_vintage`, `crimson_bloodwine`, `solarian_biotic`, `trade_authenticator`) are hauled by `6A` at `2.5x--3x` (`12--18h` peak) buffers (`hub_upkeep_reorder_pct = 0.78`, up to `4` concurrent haulers) so venues hold `100%` maintenance without 80% penalties.
   - `6A` closed-loop outpost backhauls (`_pick_outpost_backhaul`) bring valuable outpost gas/ice/rare ore back toward hub stations on return legs.
4. **Live `6B` Speed-6 VIP Liners & Toll-Aware Jumpgate Network (`passenger_net.py`, `fuelplan.py`):**
   - `6B` scaled to `28` Speed-6 VIP `Futures` liners (`futures -> consortium -> concordia`) dual-fitted with `first_class_passenger_suite` + `business_passenger_cabin` (`10` VIP/Business berths/liner).
   - Weighted Dijkstra jumpgate routing (`fuelplan.py` -> `passenger_net.py` & `haul.py`) uses public player jumpgates (`[HEXC] miaplacidus <-> kochab` `200 cr`, `[BUSY] mile_mark <-> tiaki` `100 cr`) ONLY when jumps saved beat `toll_cr` (`500 cr` max cap, broke-pilot guard, explicit toll deduction from fares/arb profits, and 30m circuit breaker).
5. **Next Territorial Horizon (Stations #2--#5 & Outposts #4--#8):**
   - Once Phase-2 Ridgecrest builds complete, organic Treasury > `2.0M cr` automatically funds fleet T1+T2 hull/module rollouts (`upgrade-policy.json: max_auto_tier=2`) and then Station #2--#5 `station_core` acquisitions.

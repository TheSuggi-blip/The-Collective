---
name: birth-plans
id: 20261122T172119Z
tier: strategy
author: Trinity
links: [governance/strategy.md, governance/empire.md, game/birth-plans.tsv]
---

# birth-plans.md -- Approved 500-Ship & 600-Ship Multi-Empire Birthing Plans

Approved by Suggi on 2026-11-22. Structured rows live in
`game/birth-plans.tsv` and mirror automatically into the SQLite table
`birth_plans` in `read.db` (under **Plans and the door** in
`game/handbook.md`). Both plans are **strictly nested**: Waves 1-3 build
the approved **500-Ship Fleet** (`+254` births onto our `246` Voidborn
baseline), and Wave 4 (`+100` births) extends seamlessly to the
**600-Ship Grand Praetorian & Royal Guard Fleet** with zero wasted or
regretted pilots.

Pilot birthing is reserved exclusively to Suggi (`governance/rulebook.md`,
Standing Order G5). Unity and Apollo prepare the seat cap (`200 -> 400 ->
500 -> 600+`), faction ship garages, shipyards, and positive 24h steady
net before each wave is triggered.

## 1. Side-by-Side Summary: 500-Ship vs 600-Ship Fleet

| Division & Role | Current (`246` VB) | Plan 500 (`+254`) | Plan 500 Birth Split (New Ships) | Plan 600 (`+354`) | Plan 600 Birth Split (New Ships) |
| :--- | ---: | ---: | :--- | ---: | :--- |
| **Mining (`miner`)** | 60 | **130** (26.0%) | +35 Solarian, +35 Nebula | **150** (25.0%) | +45 Solarian, +35 Nebula, +10 Outer Rim (`All Mine` armed T5) |
| **Logistics (`hauler`)** | 40 | **95** (19.0%) | +30 Outer Rim, +25 Nebula | **110** (18.3%) | +40 Outer Rim, +30 Nebula |
| **Trade (`trader`)** | 40 | **85** (17.0%) | +30 Nebula, +15 Solarian | **94** (15.7%) | +36 Nebula, +18 Solarian |
| **Military Strike (`drone`)** | 50 | **95** (19.0%) | +30 Crimson, +15 Solarian | **115** (19.2%) | +45 Crimson (`Annihilator` 9w), +20 Solarian (`Opus Magna` 8w) |
| **Military Royal Guard (`sentinel`)** | 20 | **35** (7.0%) | +10 Crimson, +5 Solarian | **60** (10.0%) | +20 Crimson (`Stockade`/`Portcullis`), +20 Solarian (`Symposium`/`Fundament`) |
| **Intel (`scout`)** | 30 | **50** (10.0%) | +12 Outer Rim, +8 Nebula | **55** (9.2%) | +15 Outer Rim, +10 Nebula |
| **Command (`command`)** | 6 | **10** (2.0%) | +1 Sol, +1 Neb, +1 OR, +1 Crim | **16** (2.7%) | +3 Solarian, +3 Crimson, +2 Nebula, +2 Outer Rim |
| **TOTAL FLEET** | **246** | **500** | **+99 Neb, +71 Sol, +43 OR, +41 Crim** | **600** | **+113 Neb, +106 Sol, +68 Crim, +67 OR** |

## 2. The 60-Ship Sentinel & Royal Guard Corps (Plan 600 Special Wing)

In SpaceMolt, `sentinel` pilots execute both `guard` and `hunt` work
classes (`game/fleet/workclass.py`). Under Plan 600, the Sentinel corps
triples from `20` to **`60` ships** arranged as a symmetrical **20 / 20 /
20 Tri-Empire Praetorian Guard**:

- **20 Voidborn "Phase Wardens" (existing `sentinel-1..20`):** `+12%`
  shields, EWAR, warp interdiction, and combat medical hulls (`Penumbra`,
  `Aporia`, `Pleroma` T5 7-defense medical tender, `Apotheosis` T5
  2,500-shield dreadnought).
- **20 Crimson "Iron Praetorians" (`+10` Wave 3, `+10` Wave 4):** Heavy
  60-150 armor walls and warp-scrambling interdictors (`Stockade`
  8-defense-slot Monitor, `Bastille`, `Portcullis` 1,425-hull
  Interdictor, `Anvil` armored repair, `Subjugator` 3,715-hull carrier).
- **20 Solarian "Aegis Paladins" (`+5` Wave 3, `+15` Wave 4):** `+3%` all
  stats & `+1%/lv` accuracy in command/logistics shield cruisers
  (`Warrant`, `Paradox Engine` 4w/4d/5u Interdictor, `Panacea` medical,
  `Fundament` T5 fleet logistics tender, `Symposium` T5 6w/6d/8u command
  cruiser).

**Standing Royal Guard Assignments (60 Sentinels):**
1. **Flagship & Moving City Royal Guard (24 Sentinels):** Permanent
   multi-layer shield/armor/medical/interdictor screen escorting Unity's
   Flagship Fleet and our 1 unique Tier-5 `Emanation` Moving City.
2. **Sovereign Station & Choke-Point Bastions (24 Sentinels):** Garrison
   squadrons stationed at Yildun (north choke), Aldebaran,
   Hawthorne/Alchiba, and scarce-resource outposts.
3. **Capital Convoy Escorts (12 Sentinels):** Heavy escorts protecting
   `3,960`-cargo `Eldorado` and `2,640`-cargo `Frankenhauler` supply runs
   across lawless corridors.

## 3. Phased Rollout Waves & Readiness Gates

| Wave | Fleet Step | New Births | Readiness Gate Before Birthing | Cohort Breakdown |
| :--- | :--- | ---: | :--- | :--- |
| **Wave 1** | `246 -> 320` | `+74` | `Guild Hall Recruiting` (`400` seats) active + 24h steady net `> 0` | `+25` Neb Traders, `+25` OR Haulers, `+24` Sol Miners |
| **Wave 2** | `320 -> 420` | `+100` | Northern outpost/station online (Atria/Yildun) + Wave 1 self-funding | `+35` Neb Miners, `+25` Neb Haulers, `+15` Sol Traders, `+15` Crim Strike, `+10` OR Scouts |
| **Wave 3** | `420 -> 500` | `+80` | `500+` seats raised (`Grand Recruitment Bureau` / multi-base) | `+15` Crim Strike, `+15` Sol Strike, `+10` Crim Guard, `+5` Sol Guard, `+11` Sol Miners, `+5` OR Haulers, `+5` Neb Traders, `+8` Neb Scouts, `+2` OR Scouts, `+4` Command (**Completes Plan 500**) |
| **Wave 4** | `500 -> 600` | `+100` | `600+` seats across sovereign stations + T3-T5 shipyard pipeline | `+10` Crim Guard, `+15` Sol Guard, `+6` Command, `+15` Crim Strike, `+5` Sol Strike, `+10` Sol Miners, `+10` OR `All Mine` Miners, `+10` OR Haulers, `+5` Neb Haulers, `+6` Neb Traders, `+3` Sol Traders, `+3` OR Scouts, `+2` Neb Scouts (**Completes Plan 600**) |

## 4. Querying in SQL (`read.db`)

- Plan 500 totals by division & empire:
  `SELECT division, role, empire, SUM(ships) AS total FROM birth_plans WHERE wave <= 3 GROUP BY division, role, empire ORDER BY division, total DESC`
- Plan 600 totals by division & empire:
  `SELECT division, role, empire, SUM(ships) AS total FROM birth_plans GROUP BY division, role, empire ORDER BY division, total DESC`
- Royal Guard / Sentinel breakdown:
  `SELECT wave, wing, empire, ships, flagship_hulls FROM birth_plans WHERE role = 'sentinel' ORDER BY wave, empire`

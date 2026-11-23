---
name: empire
id: 20261116T192710Z
tier: map
author: Unity
status: written by game/fleet/empire.py; never edited by hand
links: [governance/map.md, game/rules/09-factions.md, game/map/sites.tsv, game/catalog/facilities.md, governance/strategy.md]
---

# empire.md -- What The Collective Holds

Our empire in one file: the faction, its bases, its offices at other
stations, the systems they stand in, the sites we may build on, and what
the faction can build next. Written by `python3 -I -B game/fleet/empire.py
write` from what the game itself answers; never edited by hand. The map
around it is `governance/map.md`.

Not in this file, and not in the repository: where our ships are, what
they store, the members by name and the treasury's balance. They are live
data of the unit (the tools `hive` with `verb=empire`, `stock`, `ship`;
`game/fleet/empire.py show`).

Facts as of 2026-11-23T21:19:13Z.

## 1. The Faction

| Fact | Now |
|---|---|
| Name and tag | The Collective [CLTV] |
| Founded | 2026-11-15 |
| Leader | the Fleet Admiral's flagship |
| Members | 200 of a limit of 200 |
| Ships of the fleet in it | 200 of 500 |
| Stations of our own | 0 of 5 a faction may hold |
| Outposts | 1 of 8 |
| Offices at stations | 6, rent 506 cr per cycle (43,516 cr a day) |
| Shared ships in garages | 0 |
| At war | no |
| Allies | none |
| Marked enemies | none |

The member limit is set by recruitment offices (section 5): the best
station's office counts in full, each other station's office adds a quarter
of its own limit.

## 2. Bases and Territory

| Base | Kind | System | Condition | Services |
|---|---|---|---|---|
| CLTV Outpost GSC-0044 | outpost | `gsc_0044` | thriving | -- |

Systems we hold something in:

| System | What | Note |
|---|---|---|
| `gsc_0044` | outpost | CLTV Outpost GSC-0044 |
| `node_beta` | office | at node_beta_industrial_station |
| `the_experiment` | office | at the_experiment_research_station |

What founding a base takes: `game/rules/09-factions.md` (fees and limits)
and the tool `base_plan` (every part down to the ore, against what we
hold).

## 3. Offices at Other Stations

| Office | Tier | Station | System | State | Rent per cycle |
|---|---|---|---|---|---|
| Faction Fuel Bunker | 1 | 443f0c5b2a1fbbcea95d13b76a797fe9 | `gsc_0044` | active | 0 |
| Faction Lockbox | 1 | 443f0c5b2a1fbbcea95d13b76a797fe9 | `gsc_0044` | active | 0 |
| Faction Lockbox | 1 | node_beta_industrial_station | `node_beta` | active | 69 |
| Notice Board | 1 | node_beta_industrial_station | `node_beta` | active | 17 |
| Recruitment Center | 1 | node_beta_industrial_station | `node_beta` | active | 351 |
| Faction Lockbox | 1 | the_experiment_research_station | `the_experiment` | active | 69 |

## 4. Sites

Places proposed for a base of ours, from `game/map/sites.tsv`; the columns
Space, Jumps and Stations there are read from the chart and the public
list of stations. Where a base is built is Suggi's decision.

| System | Name | Space | Jumps from home | Stations there | Status | Proposed by | Note |
|---|---|---|---|---|---|---|---|
| `gsc_0044` | GSC-0044 | lawless | 6 | CLTV Outpost GSC-0044 (outpost, CLTV) | built | Zero, Apollo | east road inner outpost (built 2026-11-17, rule F33): 3 systems beyond border, 6 jumps from home; two belts of iron and copper near 100,000 each, sol alloy ore, grazer herds |
| `atria` | Atria | lawless | 7 | none | chosen | Unity | north road inner outpost (Suggi, 2026-11-17 22:30 UTC, orders P3): 5 systems beyond border, 7 jumps from home on Marfik > Atria > Regor, 5 jumps short of Yildun; iron, copper, gold, argon, ices, grazers |
| `yildun` | Yildun | lawless | 11 | none | chosen | Suggi | north road choke-point station (Suggi, 2026-11-17 22:30 UTC, orders P3; needs core-foundry & station-core): far end of the north choke point, 5 jumps beyond Atria, 11 from home |
| `oakridge` | Oakridge | lawless | 11 | none | candidate | Unity | east road station site (Suggi, 2026-11-17 23:45 UTC, orders ENT-054 & P3): built when the agents decide to raise an east station; 8 beyond border, 5 beyond GSC-0044, 3 from Solarian space |
| `felis` | Felis | lawless | 7 | none | chosen | Suggi | south road inner outpost (Suggi, 2026-11-17 23:40 UTC, orders ENT-053 & P3): 4 beyond border, 7 from home between Tanglewood and Biham; built after Atria and Oakridge |
| `achernar` | Achernar | lawless | 4 | none | dropped | Oracle | overtaken when gsc_0044, atria and felis were chosen as the three inner road outposts under rule F33 |
| `alnair` | Alnair | lawless | 5 | none | dropped | Oracle | overtaken when gsc_0044, atria and felis were chosen as the three inner road outposts under rule F33 |
| `wolf_1061` | Wolf 1061 | lawless | 4 | none | dropped | Oracle | overtaken when gsc_0044, atria and felis were chosen as the three inner road outposts under rule F33 |
| `acrab` | Acrab | lawless | 6 | none | dropped | Unity | replaced by Atria on Suggi's word (2026-11-17 22:30 UTC, orders ENT-048) |
| `gsc_0006` | GSC-0006 | lawless | 10 | none | dropped | Unity | replaced by Yildun at the far end of the north choke point (Suggi, 2026-11-17 22:30 UTC, orders ENT-048) |
| `aldebaran` | Aldebaran | lawless | 9 | none | dropped | Suggi | early 2026-11-16 north suggestion overtaken by the reviewed Atria -> Yildun north road (orders ENT-048, F33); outer outpost beyond Yildun is chosen by the agents |
| `intercrus` | Intercrus | lawless | 7 | none | dropped | Suggi | early 2026-11-17 east suggestion overtaken by GSC-0044 (built) -> Oakridge station in the final review (orders ENT-054) |
| `diadem` | Diadem | lawless | 8 | none | dropped | Suggi | early 2026-11-17 east suggestion overtaken by GSC-0044 (built) -> Oakridge station in the final review (orders ENT-054) |
| `biham` | Biham | lawless | 8 | none | dropped | Suggi | early 2026-11-17 south suggestion overtaken by Felis outpost in the final review (orders ENT-053); south station later is chosen by the agents |
| `hawthorne` | Hawthorne | lawless | 13 | none | dropped | Suggi | 2026-11-16 deep-corridor example only; under rule F33 the two deep jump-gate stations and outer outposts are chosen autonomously by the agents from Intel's readings |
| `alchiba` | Alchiba | lawless | 14 | none | dropped | Suggi | 2026-11-16 deep-corridor example only; under rule F33 the two deep jump-gate stations and outer outposts are chosen autonomously by the agents from Intel's readings |

## 5. What The Faction Can Build

Every faction facility of the game's catalog (0.734.0), line by line and
tier by tier. A higher tier is an upgrade of the one before it and
replaces its rent. Rent is due every 100 ticks (about 17 minutes) at a
station that is not ours; at our own station or outpost it is none. The
rent is the game's own card for the type (`facility types`), the day is
86.4 cycles. Every line but the first needs faction storage at the same
station. What a thing takes down to the ore: the tool `catalog` with
`ask=build`.

| Line | Tier | Facility | Credits | Materials | Rent per cycle | Rent per day | Gives |
|---|---|---|---|---|---|---|---|
| faction_storage | 1 | Faction Lockbox (`faction_lockbox`) | 200,000 | 200 steel_plate, 50 circuit_board | 69 | 5,962 | 100,000 units per item type |
| faction_storage | 2 | Faction Warehouse (`faction_warehouse`) | 750,000 | 500 steel_plate, 200 circuit_board | 261 | 22,550 | 200,000 units per item type |
| faction_storage | 3 | Faction Depot (`faction_depot`) | 4,000,000 | 2,000 steel_plate, 1,000 circuit_board, 500 titanium_alloy | 1,395 | 120,528 | 300,000 units per item type |
| faction_storage | 4 | Faction Stronghold (`faction_stronghold`) | 15,000,000 | 5,000 steel_plate, 2,500 circuit_board, 1,500 titanium_alloy, 500 durasteel_plate | 5,232 | 452,045 | 500,000 units per item type |
| faction_recruitment | 1 | Hiring Board (`hiring_board`) | 75,000 | 75 steel_plate, 25 circuit_board | 26 | 2,246 | 50 members |
| faction_recruitment | 2 | Recruitment Desk (`recruitment_desk`) | 300,000 | 200 steel_plate, 100 circuit_board | 104 | 8,986 | 100 members |
| faction_recruitment | 3 | Recruitment Center (`recruitment_center`) | 2,000,000 | 1,000 steel_plate, 500 circuit_board, 300 flex_polymer | 697 | 60,221 | 200 members |
| faction_recruitment | 4 | Guild Hall Recruiting (`guild_hall_recruiting`) | 8,000,000 | 3,000 steel_plate, 1,500 circuit_board, 800 titanium_alloy | 2,790 | 241,056 | 400 members |
| faction_recruitment | 5 | Grand Recruitment Bureau (`grand_recruitment_bureau`) | 20,000,000 | 8,000 steel_plate, 5,000 circuit_board, 2,500 titanium_alloy, 1,000 durasteel_plate | 6,976 | 602,726 | 1,000 members |
| faction_admin | 1 | Faction Desk (`faction_desk`) | 100,000 | 100 steel_plate, 25 circuit_board | 34 | 2,938 | -- |
| faction_admin | 2 | Faction Office (`faction_office`) | 500,000 | 300 steel_plate, 150 circuit_board | 174 | 15,034 | -- |
| faction_commons | 1 | Faction Quarters (`faction_quarters`) | 100,000 | 100 steel_plate, 50 flex_polymer | 34 | 2,938 | 1 rooms |
| faction_commons | 2 | Faction Lounge (`faction_lounge`) | 400,000 | 300 steel_plate, 200 flex_polymer, 100 reinforced_glass | 139 | 12,010 | 3 rooms |
| faction_commons | 3 | Faction Clubhouse (`faction_clubhouse`) | 2,500,000 | 1,000 steel_plate, 500 flex_polymer, 300 reinforced_glass, 200 circuit_board | 872 | 75,341 | 6 rooms |
| faction_company_store | 1 | Company Store (`company_store`) | 400,000 | 200 steel_plate, 150 circuit_board | 139 | 12,010 | 20 members-only listings |
| faction_company_store | 2 | Company Outlet (`company_outlet`) | 1,200,000 | 500 steel_plate, 400 circuit_board | 418 | 36,115 | 50 members-only listings |
| faction_company_store | 3 | Company Exchange (`company_exchange`) | 5,000,000 | 2,000 steel_plate, 1,000 circuit_board, 500 titanium_alloy | 1,744 | 150,682 | 100 members-only listings |
| faction_espionage | 1 | Espionage HQ (`espionage_hq`) | 250,000 | 250 circuit_board, 150 optical_fiber_bundle, 50 superconductor | 87 | 7,517 | -- |
| faction_fuel | 1 | Faction Fuel Bunker (`faction_fuel_bunker`) | 800,000 | 400 steel_plate, 100 circuit_board | 279 | 24,106 | -- |
| faction_fuel | 2 | Faction Large Fuel Bunker (`faction_large_fuel_bunker`) | 3,000,000 | 1,200 steel_plate, 300 circuit_board, 100 armor_plate | 1,046 | 90,374 | -- |
| faction_fuel | 3 | Faction Capital Fuel Bunker (`faction_capital_fuel_bunker`) | 10,000,000 | 3,000 steel_plate, 800 circuit_board, 300 armor_plate, 100 capital_armor_plate | 3,488 | 301,363 | -- |
| faction_intel | 1 | Intel Terminal (`intel_terminal`) | 150,000 | 200 circuit_board, 100 optical_fiber_bundle | 52 | 4,493 | -- |
| faction_intel | 2 | Intel Center (`intel_center`) | 750,000 | 500 circuit_board, 300 optical_fiber_bundle, 100 superconductor | 261 | 22,550 | -- |
| faction_market | 1 | Market Runner (`market_runner`) | 150,000 | 100 steel_plate, 75 circuit_board | 52 | 4,493 | 100 open faction orders |
| faction_market | 2 | Trading Booth (`trading_booth`) | 600,000 | 300 steel_plate, 250 circuit_board | 209 | 18,058 | 250 open faction orders |
| faction_market | 3 | Faction Trading Post (`faction_trading_post`) | 3,000,000 | 1,500 steel_plate, 750 circuit_board, 400 titanium_alloy | 1,046 | 90,374 | 500 open faction orders |
| faction_marque | 1 | Letter of Marque Office (`letter_of_marque_office`) | 600,000 | 300 steel_plate, 150 circuit_board, 10 trade_cipher | 209 | 18,058 | -- |
| faction_medical | 1 | Faction Aid Station (`faction_aid_station`) | 550,000 | 250 steel_plate, 150 circuit_board, 50 medical_supplies | 191 | 16,502 | -- |
| faction_medical | 2 | Fleet Infirmary (`fleet_infirmary`) | 2,400,000 | 800 steel_plate, 500 circuit_board, 180 reinforced_glass, 150 medical_supplies | 837 | 72,317 | -- |
| faction_medical | 3 | Casualty Clearing Center (`casualty_clearing_center`) | 9,500,000 | 2,500 steel_plate, 1,500 circuit_board, 700 titanium_alloy, 500 reinforced_glass, 500 medical_supplies | 3,313 | 286,243 | -- |
| faction_medical | 4 | Faction Fleet Hospital (`faction_fleet_hospital`) | 35,000,000 | 7,000 steel_plate, 4,000 circuit_board, 2,200 titanium_alloy, 800 durasteel_plate, 80 quantum_processor, 1,600 medical_supplies | 12,209 | 1,054,858 | -- |
| faction_missions | 1 | Notice Board (`notice_board`) | 50,000 | 50 steel_plate, 20 circuit_board | 17 | 1,469 | 3 posted missions |
| faction_missions | 2 | Faction Mission Board (`faction_mission_board`) | 300,000 | 200 steel_plate, 150 circuit_board | 104 | 8,986 | 8 posted missions |
| faction_missions | 3 | Bounty Office (`bounty_office`) | 2,000,000 | 1,000 steel_plate, 500 circuit_board, 250 titanium_alloy | 697 | 60,221 | 15 posted missions |
| faction_personnel_reserve | 1 | Muster Office (`muster_office`) | 400,000 | 300 steel_plate, 100 circuit_board, 100 protein_rations | 139 | 12,010 | -- |
| faction_personnel_reserve | 2 | Reserve Barracks (`reserve_barracks`) | 1,800,000 | 900 steel_plate, 350 circuit_board, 250 flex_polymer, 300 protein_rations | 627 | 54,173 | -- |
| faction_personnel_reserve | 3 | Fleet Mobilization Center (`fleet_mobilization_center`) | 7,500,000 | 3,000 steel_plate, 1,200 circuit_board, 600 titanium_alloy, 1,000 protein_rations | 2,616 | 226,022 | -- |
| faction_personnel_reserve | 4 | Strategic Reserve Command (`strategic_reserve_command`) | 28,000,000 | 8,000 steel_plate, 3,000 circuit_board, 1,800 titanium_alloy, 600 durasteel_plate, 3,000 protein_rations | 9,767 | 843,869 | -- |
| faction_prize_recovery | 1 | Prize Recovery Yard (`prize_recovery_yard`) | 600,000 | 300 steel_plate, 150 circuit_board | 209 | 18,058 | -- |
| faction_sensor | 1 | Sensor Dome (`sensor_dome`) | 600,000 | 300 steel_plate, 150 circuit_board, 40 sensor_array | 209 | 18,058 | -- |
| faction_sensor | 2 | Deep Space Scanner (`deep_space_scanner`) | 3,500,000 | 800 steel_plate, 400 circuit_board, 200 titanium_alloy, 60 sensor_package, 30 precision_optic | 1,220 | 105,408 | -- |
| faction_sensor | 3 | Long-Range Subspace Sensor (`long_range_subspace_sensor`) | 12,000,000 | 2,500 steel_plate, 1,000 circuit_board, 600 titanium_alloy, 300 durasteel_plate, 80 sensor_cluster, 40 communications_array, 40 quantum_processor | 4,186 | 361,670 | -- |
| faction_ship_garage | 1 | Faction Ship Garage (`faction_ship_garage`) | 600,000 | 300 steel_plate, 150 circuit_board | 209 | 18,058 | 20 shared ships |
| faction_ship_garage | 2 | Faction Ship Hangar (`faction_ship_hangar`) | 3,000,000 | 1,200 steel_plate, 500 circuit_board, 300 titanium_alloy | 1,046 | 90,374 | 50 shared ships |
| faction_ship_garage | 3 | Faction Fleet Yard (`faction_fleet_yard`) | 12,000,000 | 4,000 steel_plate, 1,500 circuit_board, 1,000 titanium_alloy, 400 durasteel_plate | 4,186 | 361,670 | 100 shared ships |
| faction_shipyard_slot | 1 | Faction Shipyard Berth (`faction_shipyard_berth`) | 1,500,000 | 800 steel_plate, 300 circuit_board | 523 | 45,187 | -- |
| faction_shipyard_slot | 2 | Faction Shipyard Bay (`faction_shipyard_bay`) | 5,000,000 | 2,000 steel_plate, 800 circuit_board, 300 titanium_alloy | 1,744 | 150,682 | -- |
| faction_shipyard_slot | 3 | Faction Shipyard Dock (`faction_shipyard_dock`) | 15,000,000 | 5,000 steel_plate, 2,000 circuit_board, 1,000 titanium_alloy, 300 durasteel_plate | 5,232 | 452,045 | -- |
| faction_shipyard_slot | 4 | Faction Shipyard Drydock (`faction_shipyard_drydock`) | 40,000,000 | 10,000 steel_plate, 4,000 circuit_board, 2,500 titanium_alloy, 1,000 durasteel_plate, 300 superconductor | 13,953 | 1,205,539 | -- |
| faction_shipyard_slot | 5 | Faction Shipyard Complex (`faction_shipyard_complex`) | 100,000,000 | 20,000 steel_plate, 8,000 circuit_board, 5,000 titanium_alloy, 2,500 durasteel_plate, 800 superconductor, 300 capital_armor_plate | 34,883 | 3,013,891 | -- |
| faction_storage_extension | 1 | Storage Extension (`storage_extension`) | 500,000 | 400 steel_plate, 150 circuit_board | 174 | 15,034 | 100,000 units per item type in a named bucket |
| faction_trade_intel | 1 | Trade Ledger (`trade_ledger`) | 200,000 | 150 circuit_board, 100 optical_fiber_bundle, 10 trade_cipher | 69 | 5,962 | -- |
| faction_trade_intel | 2 | Commerce Terminal (`commerce_terminal`) | 1,500,000 | 500 circuit_board, 400 optical_fiber_bundle, 200 superconductor, 50 trade_cipher | 523 | 45,187 | -- |
| faction_transit | 1 | Transit Lounge (`transit_lounge`) | 500,000 | 250 steel_plate, 100 circuit_board, 100 flex_polymer | 174 | 15,034 | 20 connecting passengers |
| faction_transit | 2 | Transit Terminal (`transit_terminal`) | 2,500,000 | 1,000 steel_plate, 400 circuit_board, 300 flex_polymer, 200 reinforced_glass | 872 | 75,341 | 60 connecting passengers |
| faction_transit | 3 | Transit Concourse (`transit_concourse`) | 9,000,000 | 3,000 steel_plate, 1,200 circuit_board, 600 titanium_alloy, 500 reinforced_glass | 3,139 | 271,210 | 150 connecting passengers |

## 6. Keeping This File

| Task | How |
|---|---|
| Read the empire again | `python3 -I -B game/fleet/empire.py collect` (the Fleet Admiral's hourly job; views only) |
| Write this file | `python3 -I -B game/fleet/empire.py write --commit` (rewritten only when a fact changed) |
| Ask it | the tool `hive` with `verb=empire`; in the history store the tables `faction`, `bases`, `faction_facilities`, `territory`, `sites` |
| Propose a site | a line in `game/map/sites.tsv`: system, place, status, who proposes, note |

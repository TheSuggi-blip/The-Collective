# Intel guidebook -- Tests (tests.md)

### Base sites on the three roads
Status: test. Updated: 2026-11-21. Evidence: admirals.log ENT-063; reports/2026-11-17_oracle_three-roads-census-lists-site-candidates.md; tables fields, lanes, stations, observations kind pirate.

- Rank a site on supply and threat first: jumps to the nearest station
  with fuel and a market (BFS on lanes), pirate lines within two jumps,
  the distance to a stronghold; then its fields.
- North (orders P3): Atria the outpost, Yildun the station; no pirate
  line within two jumps of the road on 2026-11-17, and no battle of
  category pirate or npc on the road (Atria, Regor, Groombridge 34,
  Chalawan, Rasalhague, Yildun) or one lane off from 2026-11-17 to 11-21
  (the game's battle record, lessons.md). Nearest strongholds: Gliese 581
  10 jumps from Atria, Algol 11 from Yildun (BFS on lanes).
- Every outpost a stronghold crew raided in the record fell (observe kind
  raid); a ship of ours in the system deters a raid, docked too (the
  game's base-builder guide). Rank a site also on its jumps to Algol and
  Gliese 581.
- East: Oakridge or Miaplacidus for the station, Tidewater or Ross 154
  beyond; the Dross group (Merak, Sheliak, Titawin, Hollowcrest) lies east
  of them.
- Southeast: GSC-0035 or GSC-0024 for the outpost, Fomalhaut or Yed
  Posterior for the station, 6 to 7 jumps from any fuel.
- Open: the ranking is named again on the reads since 2026-11-21.

### Uranium, thorium and seam glass
Status: test. Updated: 2026-11-21. Evidence: intel turn check LEADS; tables fields; catalog items (uranium_ore, rad harvester).

- Our six books bid for uranium ore and none sells it (LEADS); every
  deposit read stood at 0 of 5,000 but Markeb Belt (38, 19 jumps), and
  Acubens Belt showed no regrowth over twelve reads in six hours
  (2026-11-17). Thorium: a few hundred units at GSC-0032. Seam glass: no
  field read holds it. Uranium and thorium are mined with a Rad
  Harvester, carried by none of ours.
- After the 90-hour pause Acubens and Stillwater still read 0 of 5,000
  (2026-11-21): no regrowth seen. Open: the far deposits (Markeb,
  HD 20794, Khambalia, Mirfak), read 2026-11-17, wait on the far lists.

### Survey beyond the border
Status: test. Updated: 2026-11-21. Evidence: scouting/<system>.json `survey`; wildlife/history.jsonl `surveyed`; observations kind survey.

- Survey Scanner I (survey power 30) revealed no hidden deposit in 52
  surveys; Homam and The Telescope answered "1 faint signature(s) that
  your scanner cannot resolve".
- Next: a probe step in census.py (use_item mining_survey_probe, +30
  survey power for 10 ticks, then survey_system) on a route that names
  it, one scanner scout at Homam first; or Survey Scanner II.
- From 2026-11-21 the six scanner scouts fly the far lists first: the
  far systems were never surveyed. Their finds (scouting/<system>.json
  `survey`, faint signatures, deposits) decide the need survey-scanner-i.

### A tier-1 hull for the scouts
Status: test. Updated: 2026-11-21. Evidence: catalog table hulls; browse_ships all_stations (scout reading, 2026-11-21); data/routes/runs.jsonl.

- Tier 1 needs no Piloting. Qualia (explorer): speed 3 against the
  Threshold's 1, tank 130, three utility slots, no weapon slot (no
  hunting). Listed at our stations from 35,000 to 49,482 cr.
- Test: one reader buys one, census runs only; compare its minutes per
  run with the Threshold's on the same lists (runs.jsonl). Faster reads
  are the fix for lists that ask more than 30 scouts give.

### Visit missions
Status: test. Updated: 2026-11-21. Evidence: data/fleet/ships/<pilot>.json missions; data/missions/node_beta_industrial_station.json.

- Local Sector Survey and Deep Space Cartography (6,500 cr together) ask
  visits to Sirius, Horizon and The Crucible. Open: whether a census jump
  through a system completes an objective; read the holder's objectives
  before a route is written.

### Hunts of the scouts
Status: proven. Updated: 2026-11-21. Evidence: hive.py route <id>; data/routes/runs.jsonl; errors.log ENT-095.

- One hunter a herd; a once-hunt is bounded by its herd, not by its
  pilots: read the herd (data/wildlife/) before it goes into the plan.
- Every good the reserve keeps is stored, never sold (rule F24; the
  RESERVE line of the turn check). Chlorophages drop about 0.4 caustic
  sacs a kill (Amberfall, 2026-11-17).

### Foreign law and books
Status: proven. Updated: 2026-11-21. Evidence: get_empire_info (2026-11-16); game/planets/; data/market/<base>.json.

- Solarian and Crimson law: a Voidborn visitor pays 3 to 4% sales tax and
  a fuel surcharge of 4 to 6 cr a unit; eight goods are contraband.
- A census docks at every station it reads and saves its book and board:
  a far list keeps foreign books for Trade; a base is not a market (the
  BASES line: type and market).

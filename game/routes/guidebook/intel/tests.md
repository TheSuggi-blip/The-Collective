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
Status: test. Updated: 2026-11-23. Evidence: tables fields, stats_refill (kind field), books (asks); intel turn check LEADS; requests.log ENT-435, ENT-443.

- Every uranium and thorium deposit read stands at or near 0 of its
  max (7 each, 2 to 26 jumps); they come back at under 1 unit an hour
  and others take them as fast (stats_refill: Acubens 20 recovery
  events in 178 hours). Uranium: no ask in any book we read; our books
  bid for it (LEADS). Thorium: asks at Grand Exchange and Ironlight
  Crossroads. Silicon over 2,000 units: Emberglow only (19 jumps).
- A short ore is answered from the fields and from the asks: the
  books (table books) name a seller where no field has units.
- Seam glass: no field read holds it. Uranium and thorium are mined
  with a Rad Harvester, carried by none of ours.
- Open: a hidden deposit behind the faint signatures (next entry).

### Survey beyond the border
Status: test. Updated: 2026-11-23. Evidence: scouting/<system>.json `survey`; route fit-survey-scanner-ii-central-nexus; craftbook.py item survey_scanner_ii.

- Survey Scanner I (survey power 30) revealed no hidden deposit; 20
  systems answer "1 faint signature(s) that your scanner cannot
  resolve" (Hamal, 3 jumps, the nearest; 2026-11-22 to 23).
- Under test (2026-11-23): one scanner scout fits a Survey Scanner II
  (special rare_ore_detection; Central Nexus asks one at a time) in
  place of its off-role Mining Laser I; census.py surveys with it. Its
  surveys of faint-signature systems decide a second one; a find goes
  to Mining in queue.log.
- Next if it resolves nothing: a probe step in census.py (use_item
  mining_survey_probe, +30 survey power for 10 ticks, then survey).

### A tier-1 hull for the scouts
Status: proven. Updated: 2026-11-24. Evidence: catalog table hulls; browse_ships all_stations (2026-11-21, 2026-11-23); commission_quote confluence (2026-11-23); table runs (kind census, scout pilots, minutes over 0; the hull by pilot; windows 07:30 to 11:30 and from 11:30 UTC, 2026-11-22).

- Tier 1 needs no Piloting. Qualia (explorer): speed 3 against the
  Threshold's 1, tank 130, three utility slots, no weapon slot (no
  hunting). Listed at our stations from 35,000 to 49,482 cr.
- One reader flew one from 2026-11-21. Every window read the same way:
  a run in about two thirds of the minutes, three times the fuel or more
  (medians: 405 against 105 cr a run to 11:30 UTC, 450 against 135 from
  11:30 UTC on 2026-11-22).
- Verdict (rule F37, four windows): no second Qualia for the census; a
  read costs over three times the fuel, and fuel is the fleet's cost
  (orders P1). The one bought flew its Threshold again from 2026-11-24
  (2.4 times the fuel a run over 4 h, hive.py briefing SHIPS); the
  Qualia stays stored at Central Nexus. The next hull step for a
  scout is tier 2 at Piloting 10, judged by fuel a read the same way.
- Tier 2 (2026-11-23): no Confluence listed on the exchange
  (browse_ships, all stations); commission_quote at Central Nexus
  398,368 cr credits only, or 57,104 cr with thirteen parts (shield
  matrix, phase matrix, sensor array ...): one hull is over a turn's
  test budget (F12, 10%).

### How a scout test gets three results
Status: proven. Updated: 2026-11-22. Evidence: rule F37; queue.log ENT-203.

- A census list or a runner step: three scouts on it (a read uses no
  buyer, field or herd), their rows compared with the old ones.
- A hunt: one herd is shared, so one ship three times (F9).
- A hull or a module: one first (F17), then two more ships.

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

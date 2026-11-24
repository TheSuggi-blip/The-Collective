# Intel guidebook -- Routes (routes.md)

### Standing Plan
Status: proven. Updated: 2026-11-24. Evidence: the plan file (tool plan, show); hive.py briefing (MY STANDING FLEET); fill.py check; store table herds; intel turn check (WORKED, SITES, WATCH, ROADS, UNFLOWN).

- First, every scout: store-hold-central-nexus, then
  store-hold-frontier-station-near (any empire, 6 jumps), give-scout-stores-*,
  the Survey Scanner II fit (one ship, tests.md), the missions paid
  once and the Voidborn chain (F34, F35). No census in First or Then: a
  census is open to a pilot of another empire wherever it reads.
- Newborn scouts: their capital's region only, @outerrim (Altais) and
  @nebula (Haven): census-region-<capital> (120 min) and its ring
  (360 min), then the far lists nearest their capital, then the roads.
  Sol and Krynn (180 min) go to Voidborn readers, Krynn three.
- The kit's herds (orders P3): census-kit-herds (360 min, three ships)
  reads the far places of the five species, the region lists the near
  ones. hive.py herds <species,...>: a place at 3 or more goes to
  Military in admirals.log the same turn; tagged herds: file_ranches.py.
- Readers (@reader): census-voidborn (home, 45 min, five), the outpost
  watch (50 min), census-worked (120 min), census-frontier (170 min),
  census-worked-far (180 min), the roads. Two readers hold the home
  list first, one the watch (gaps over the hour otherwise).
- Lasers: a Voidborn scout whose missions that mine are flown gives
  its Mining Laser I to Mining at Central Nexus (own routes first).
- The scanner scouts: a far list first (1440 min), then @reader.
- Explorers: their road (census-north, -east, -south, 170 min; the
  north road first for six), census-worked-far, their far list.
- Hunters: one reader a hunt, one hunter a herd (F9), every scout hunt
  gifts to a trader (P5); a hunt another claims drops; a herd that
  carries a faction's tag is never prey (hunt.py).
- census-roads (960 min, four ships): no never-read system is left.
- Then: the docked book watch (watch-book-*, one scout a station, 0
  fuel), then park.
- Changed by: a WORKED, SITES or FRESH HALT, a road pirate, a once
  mission (queue.log), an order naming herds or places.

### Census lists
Status: proven. Updated: 2026-11-21. Evidence: game/routes/census-*.json; dispatch.py (pick, stalest_system); intel turn check (OVERLAP, ROADS, WORKED).

- Every list is disjoint: dispatch.py counts a census order against
  every route whose systems hold its system, so a shared system closes
  the smaller route (OVERLAP line). A system moves, it is never copied.
- Cadence by use: home 30, the outpost watch 35, places our routes use
  90 (home side) and 180 (beyond), frontier 170, roads 150, census-roads
  480, the far lists 720 (every system read once: oldest first). A
  system opens when its read is every_minutes old; the threshold is the
  floor of a gap, never its ceiling.
- A far list has `chain` 3 within 2 lanes and ends docked where it last
  read (`--stay`): it reads up to three more due systems on one tank.
- A new list or a moved system is judged from its next reads; the turn
  check prints every list against its target.

### Route Guides
Status: proven. Updated: 2026-11-21. Evidence: game/fleet/census.py, hunt.py (docstrings); data/routes/runs.jsonl.

| Kind | How it is flown | Fit |
|---|---|---|
| Census | census.py: fly, survey (a scanner aboard), get_poi each field, get_nearby (creatures, pilots, pirates with tier, hull, shield), dock at each station and save its book and board | the starter, hold empty |
| Hunt | hunt.py: kill up to `kills` of the species while the herd holds `min_creatures`, loot, sell into a fresh `min_bid`, store the rest (every good the reserve keeps is stored) | starter lasers, flee under 60% hull |
| Once mission | the route's circuit: accept, do the steps, hand in | as the route says |

A census by hand: `census.py <pilot> <system> --route <id>` in the
background; it ends docked, its order file gone.

### Route Templates
Status: proven. Updated: 2026-11-21. Evidence: game/routes/templates/intel.json; game/routes/templates-intel.md.

- @reader: census-watch-gsc-0044, census-worked, census-frontier,
  census-worked-far, census-north, census-east, census-south, census-roads.
- @explorer: census-north, census-east, census-south, census-roads,
  census-worked-far, census-frontier.
- Calls: `plan.py templates`; `plan.py template <name> <routes>`;
  `plan.py use <ships> <name>`; a hunter keeps its hunt first:
  `plan.py set <ship> <hunt>,@reader`.

### Missions That Pay Once
Status: proven. Updated: 2026-11-22. Evidence: data/routes/runs.jsonl (one_time); game/routes/index-once-per-pilot.md; table runs (paid share, 2026-11-22 19:26 UTC).

- Most once routes reach the list First by themselves within five
  minutes; a route that holds nothing for a pilot passes it. Not all:
  the Sol audit (another division's file) stood outside it until read.
- Weigh a visit mission by its paid share (runs with one_time over all
  runs, every division): the Sol audit paid 24 of 25 and went First;
  the frontier wayfinder paid 1 of 58 (stop 1 not reached) and stays out.
- A visit mission ("sensors will automatically log the data as you jump
  between systems") may be done by a census's jumps: read the holder's
  objectives before a route is written for it (tests.md).
- A once route offered by another division enters the plan only after
  its newest run rows are read: on 2026-11-16 seven scouts accepted a
  chain whose runner crashed at the buy (errors.log ENT-040).

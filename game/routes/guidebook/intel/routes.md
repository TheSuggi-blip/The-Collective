# Intel guidebook -- Routes (routes.md)

### Standing Plan
Status: proven. Updated: 2026-11-22. Evidence: the plan file (tool plan, show); hive.py briefing (MY STANDING FLEET); fill.py check; workclass.py sales; intel turn check (WORKED, SITES, WATCH, ROADS).

- First, every scout: store-hold-central-nexus, give-scout-stores-*
  (requires.strict: open when strict classes go on), the missions paid
  once and the Voidborn chain (F34, F35), census-voidborn (home, 30 min).
- Readers (@reader): census-watch-gsc-0044 (50 min, 3: the outpost
  stands), census-worked (90 min), census-frontier (170 min: near,
  cheap), census-worked-far (where others fly, 180 min), then the roads.
- The six scanner scouts: a far list first (720 min, oldest first), so
  every far system is surveyed; then @reader.
- Explorers: their road (census-north, -east, -south: rule F33, 150
  min), then census-worked-far, then their far list.
- Hunters: one reader a hunt, one hunter a herd (F9), then @reader. P5:
  every scout hunt carries gift_to trader; no route sells or crafts.
  Only hunts Intel claims; one another claims is dropped.
- census-roads (the oldest readings, 480 min): three readers take it
  first, since a list last in every order is never reached (lessons.md).
- Then: census-frontier, census-roads, park.
- Capacity: the lists ask more reads than 30 scouts give; the far
  lists take the rest.
- Changed by: a WORKED, SITES or FRESH HALT, a pirate on a road, a once
  mission in queue.log; why a route is closed: fill.py.

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
Status: proven. Updated: 2026-11-21. Evidence: data/routes/runs.jsonl (one_time); game/routes/index-once-per-pilot.md.

- The once routes reach the list First by themselves within five
  minutes; a route that holds nothing for a pilot passes it.
- A visit mission ("sensors will automatically log the data as you jump
  between systems") may be done by a census's jumps: read the holder's
  objectives before a route is written for it (tests.md).
- A once route offered by another division enters the plan only after
  its newest run rows are read: on 2026-11-16 seven scouts accepted a
  chain whose runner crashed at the buy (errors.log ENT-040).

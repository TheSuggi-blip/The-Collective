# Intel guidebook -- Routes (routes.md)

### Standing Plan
Status: proven. Updated: 2026-11-21. Evidence: the plan file (tool plan, show); hive.py briefing (MY STANDING FLEET); fill.py check; intel turn check (WORKED, SITES, WATCH).

- First, every scout: store-hold-central-nexus, the missions paid once
  and the Voidborn chain (F34, F35), census-voidborn (home, 30 min, 4).
- Readers (@reader): census-watch-gsc-0044 (35 min, 4), census-worked
  (90 min, 6), census-frontier (170 min: near, cheap), census-worked-far
  (where others fly beyond the roads, 180 min, 10), then the roads.
- The six scanner scouts: a far list first (720 min, oldest first), so
  every far system is surveyed; then @reader.
- Explorers: their road (census-north 6, -east 3, -south 4: rule F33,
  150 min), then census-worked-far, then their far list.
- Hunters: one reader a hunt, one hunter a herd (F9), then @reader.
- Then: the steel crafts of own stores, census-frontier, park.
- Capacity: the lists ask more reads than 30 scouts give (census runs
  of 4 hours and minutes per run by route, data/routes/runs.jsonl,
  against systems / every_minutes); the far lists take what is left. A
  faster hull (tests.md) is the fix, not longer cadences.
- What changes it: a WORKED, SITES or FRESH line that HALTs, a pirate on
  a road, a once mission in queue.log; what closes a route: fill.py
  status; what it earns: route_earnings.

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

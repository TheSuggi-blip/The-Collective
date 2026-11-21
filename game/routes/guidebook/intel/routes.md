# Intel guidebook -- Routes (routes.md)

### Standing Plan
Status: proven. Updated: 2026-11-21. Evidence: the plan file (tool plan, show); hive.py briefing (MY STANDING FLEET); fill.py check; intel turn check (WORKED, SITES, WATCH).

- First, every scout: store-hold-central-nexus (a hold over five units),
  the missions paid once and the Voidborn chain (rules F34, F35), and
  census-voidborn after the Central Nexus board: the ten home systems
  every 30 minutes, 4 ships.
- Readers (@reader): census-watch-gsc-0044 (the outpost and its six
  neighbours, 35 min, 4), census-worked (the places our routes use near
  home, 90 min, 6), census-worked-far (where the other divisions fly
  beyond the roads, 180 min, 6), census-frontier (170 min), then the roads.
- Explorers: their road first (census-north 6, census-east 3,
  census-south 4: the three roads of rule F33, 150 min), then
  census-worked-far, then the far list each has flown least (480 min).
- Hunters: one reader each on a hunt of its own, one hunter a herd
  (F9), then @reader.
- Then: the steel crafts of each pilot's own stores, census-frontier,
  park.
- What each route earns now: the tool routes, or route_earnings; what
  closes a route to a ship: fill.py status. What would change the plan:
  a WORKED or SITES line that HALTs, a road list read under its cadence,
  a pirate on a road, a once mission announced in queue.log.

### Census lists
Status: proven. Updated: 2026-11-21. Evidence: game/routes/census-*.json; dispatch.py (pick, stalest_system); intel turn check (OVERLAP, ROADS, WORKED).

- Every list is disjoint: dispatch.py counts a census order against
  every route whose systems hold its system, so a shared system closes
  the smaller route (OVERLAP line). A system moves, it is never copied.
- Cadence by use: home 30, the outpost watch 35, places our routes use
  90 (home side) and 180 (beyond), frontier 170, roads 150, the explorer
  lists 480. A system opens when its read is every_minutes old; the
  threshold is the floor of a gap, never its ceiling.
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

- @reader: census-watch-gsc-0044, census-worked, census-worked-far,
  census-frontier, census-north, census-east, census-south, census-roads.
- @explorer: census-north, census-east, census-south, census-worked-far,
  census-roads, census-frontier.
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

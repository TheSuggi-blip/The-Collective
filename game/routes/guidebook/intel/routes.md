# Intel guidebook -- Routes (routes.md)

### Standing Plan
Status: proven. Updated: 2026-11-23. Evidence: the plan file (tool plan, show); hive.py briefing (MY STANDING FLEET); fill.py check; workclass.py sales; intel turn check (WORKED, SITES, WATCH, ROADS, UNFLOWN).

- First, every scout: store-hold-central-nexus, give-scout-stores-*
  (requires.strict: open when strict classes go on), the missions paid
  once and the Voidborn chain (F34, F35); the Sol audit last (paid 24
  of 25). No census in First or Then: a census is open to a pilot of
  another empire wherever it reads (dispatch.newborn_reason).
- Newborn scouts: their capital's region only, @outerrim (Altais) and
  @nebula (Haven): census-region-<capital> (120 min, four jumps and the
  places others work within six) and its ring (360 min); then the far
  lists nearest their capital, then the roads, so none waits when the
  region is full. Sol and Krynn regions (180 min) go to Voidborn scouts
  stationed near them.
- The outpost watch and the frontier: one reader each takes it first.
- Readers (@reader): census-voidborn (home, 45 min), the outpost watch
  (50 min), census-worked (120 min: twice a turn), census-frontier
  (170 min), census-worked-far (where others fly, 180 min), the roads.
- The six scanner scouts: a far list first (720 min, oldest first), so
  every far system is surveyed; then @reader.
- Explorers: their road (census-north, -east, -south: rule F33, 170
  min), then census-worked-far, then their far list.
- Hunters: one reader a hunt, one hunter a herd (F9), then @reader. P5:
  every scout hunt carries gift_to trader; no route sells or crafts.
  Only hunts Intel claims; one another claims is dropped.
- census-roads (the oldest readings, 480 min): three readers take it
  first, since a list last in every order is never reached (lessons.md).
- Then: park alone.
- Capacity: the home-side lists ask more reads than the Voidborn scouts
  give; a newborn region keeps fewer readers busy than it has newborns
  (an estimate from its cadence and a read's minutes; fill.py names
  the rest).
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

# Intel guidebook -- Lessons (lessons.md)

### How this guidebook is kept
Status: retired. Updated: 2026-11-24. Evidence: rule F14 says the same (a figure named by its call, the caps); scripts/guide.py check intel enforces it.

Kept by Oracle for every member. A figure is named by the call that
prints it, never copied; a number no record holds is `not measured`.
Caps: rule F14; an outdated entry is retired, then `guide.py tidy intel`.

### How the Census Is Dispatched
Status: proven. Updated: 2026-11-21. Evidence: game/fleet/dispatch.py (pick, stalest_system); errors.log ENT-065.

- A system opens when its read is every_minutes old; the free pilot whose
  plan holds the list takes the stalest. The threshold is the floor of a
  gap: 30 minutes gave gaps of 33 to 71 (2026-11-15). Report the gaps,
  not only the oldest age.
- A census order counts against every route whose list holds its system:
  keep the lists disjoint (OVERLAP line).
- A list that grows is taken at once: eleven ships within a minute of a
  commit (2026-11-15). An empty dry run of dispatch.py means no route is
  open to any free pilot: read max_ships against the order files first.

### Keep the explorers' lists ahead of them
Status: proven. Updated: 2026-11-22. Evidence: intel turn check ROADS, OFFLIST, UNFLOWN; data/routes/runs.jsonl (2026-11-16 23:21 to 2026-11-17 07:30 UTC); hive.py route census-roads; data/scouting/sol.json.

- ROADS HALTs under four hours of first visits: widen a list, nearest
  first; ROADS END (all but strongholds read): rotate the explorers.
- A system read by hand and left on no list that is on (`off` counts
  as none) ages unseen (Sol and six more, 718 to 8,958 min, 2026-11-22):
  OFFLIST names it; it moves onto census-roads.
- A list behind lists that always hold a due system is never reached
  (census-roads, 2026-11-22: no run in ten hours): give it ships of its
  own; UNFLOWN HALTs on it.

### Read every place the orders name against its cadence
Status: proven. Updated: 2026-11-21. Evidence: intel turn check SITES; reports.log ENT-083.

- Atria, the north outpost's site, stood 571 minutes unread on an
  8-hour list. SITES names every system of the ORACLE block on no list
  read within 180 minutes: move it onto a road list before the commit.

### Read where the fleet works now
Status: proven. Updated: 2026-11-24. Evidence: intel turn check WORKED (2026-11-21 19:40 UTC, 2026-11-22 19:27 UTC), BELTS (2026-11-24); game/routes/census-worked-far.json.

- After the pause of 2026-11-18 to 11-21 the other divisions flew in 39
  systems that only the 480-minute explorer lists read: Military's hunts
  and their sell stations, Mining's far fields. The dispatcher's pirate
  stop (six hours, F27) and a mine route's min_left rest on a census.
- WORKED names every system where ships of other divisions fly now and
  no list reads within 180 minutes: move it onto the region list of the
  capital nearest it by lanes (the WORKED to line); census-worked-far is
  flown from home, so a far system there pulls a home reader 10 to 17
  jumps (2026-11-23). A route paid once only passes through: WORKED
  prints its systems apart, unjudged.
- WORKED sees only where ships fly now; a belt in a plan nobody flies
  yet waits on an old read (GSC-0007, 360-minute kit list, 281 minutes,
  2026-11-24). BELTS judges every belt of Mining's plan by its list.
- After any pause every reading is stale at once: the home list first,
  then where ships fly, then the roads; judge the gaps from the next
  reads, not the first hour.

### Hand edits and the plan file
Status: proven. Updated: 2026-11-21. Evidence: errors.log ENT-105; requests.log ENT-279.

- A hand edit that looked for `## Notes` as plain text found its mention
  in the file head and wrote the file twice. Use `plan.py planned` and
  `plan.py note`; plan.py check HALTs on a heading twice (PLANFILE line).
- plan.py writes game/routes/plans/scout.json and plan-scout.md: commit
  them by path, or the next apply waits.

### Times, hashes and files
Status: proven. Updated: 2026-11-21. Evidence: errors.log ENT-034, ENT-047; rule F15.

- A time in a route, plan or note comes from the clock of the script
  that writes it, never typed (eight files said 03:25 for 03:11).
- A commit hash goes into an entry after `git branch -r --contains`
  prints origin/main: the watcher rebases unpushed commits.
- A data folder gains files (history.jsonl, ladders.json, foreign books
  by base id): a reader that globs keeps only one station's records.
- A turn that ended without a report leaves routes no plan names: read
  the ORPHANS line and `git log --author=Oracle` before building a route.

### A census can strand its ship where no station stands
Status: proven. Updated: 2026-11-22. Evidence: errors.log ENT-121; requests.log ENT-334; data/routes/runs.jsonl (2026-11-22 01:12 to 03:18 UTC).

- A far list holds systems without a station. A read that ends there
  leaves the ship in space, and a tank short of home keeps it there:
  every next census is refused for fuel, each run 1.5 minutes long, so
  the dispatcher's rest for runs under a minute never fires.
- Read the runs, not only the ages: a pilot with many census rows of 0
  places and 0 credits in a row is stuck; the ship tool gives its fuel
  and place. Rescue by hand: hold, the nearest station with fuel by
  lanes (one whose read lists `refuel`), dock, refuel, release.
- census.py takes fuel first when the tank is short of the way there
  and on to fuel (built 2026-11-22; installed once the suite passes).

### The game's own records answer what no census saw
Status: proven. Updated: 2026-11-21. Evidence: requests.log ENT-310; admirals.log ENT-077; observations kind raid; https://game.spacemolt.com/api/battles.

- A base raid is category `npc` in /api/battles, not `pirate`: a pirate
  reading misses every raid. The list takes `category`, `limit` (100 read
  well) and `offset`; a `system` filter is ignored, so page back by
  offset to the time asked and filter in code, one call a second.
- The faction's own log: get_action_log with `faction_id` (category
  faction: deposits, refuels, repairs) dates when a base last worked.
- Our outpost stood wrecked three days before any member read it: a
  question about the past goes to these records first, the census after.

### Calls that surprise
Status: proven. Updated: 2026-11-24. Evidence: game/fleet/gate.py; the game's help (2026-11-15 to 2026-11-17); game/fleet/route_run.py (lines 1172, 1339); dispatch.py (requires.max_jumps); table runs (strip route, 09:30 to 11:20 UTC).

- gate.py cuts an answer at 3,000 characters: read long answers with
  FULL=1. get_empire_info takes `empire_id`. get_system answers the
  ship's own system whatever system_id says.
- The stance is the raw action `default_stance` `{"stance": "flee"}` in
  group spacemolt_battle (scripts/set_stance.py); a new scout gets it once.
- First Steps in the Void leaves 13 to 38 ore aboard: stash.py stores
  it, or every empty-hold route stays closed to the scout (HOLDS line).
- fleet-build.sh install: run it in the background and poll it to its
  last line (errors.log ENT-115; seven minutes on 2026-11-23).
- route_run.py works a stop's `gift` before its `unfit` and `store`: a
  stripped module is given by a second route (errors.log ENT-178).
- `requires.in_system` waits for chance: a once-per-pilot chore at one
  station took 1 of 18 scouts from 09:30 to 11:05 UTC, then 3 in five
  minutes on `max_jumps` 2. in_system is for the docked watch. A strip
  route is `standing`: the loss stop exempts `fit`, never `unfit`.

### A gate on a fresh read is open on an old one
Status: proven. Updated: 2026-11-22. Evidence: route mission-cracking-the-shell-central (its runs); data/wildlife/gsc_0041.json; admirals.log ENT-095.

- A step's `min_creatures` closes a hunt only while the place's census
  is younger than 90 minutes; on a list read every 170 minutes the gate
  stands open most of the time, and ships fly to an empty field.
- So a hunt place that a route gates by count belongs on a list read
  faster than the gate's window; else name the reading to the route's
  owner with a place that is.

### A cut in reads is a cut in ship-hours
Status: proven. Updated: 2026-11-22. Evidence: table runs (census, 24 h to 23:25 UTC: 2,416 runs, 608 ship-hours); requests.log ENT-373, ENT-374, ENT-381; commits 786f71c9, ad738674.

- Census fuel follows the ship-hours that read, not the cadences: while
  the lists ask more reads than the scouts give, a longer cadence only
  moves reads from fresh places to old ones, at the same burn.
- So a burn cut means fewer scouts reading: since 2026-11-23 a scout
  docked with no due read counts as on watch (F8 exception). Ask
  before capping, never after.

### A newborn's hold closes its own census
Status: proven. Updated: 2026-11-24. Evidence: fill.py status scout (2026-11-23 03:19 UTC: 'hold not empty' 6; 2026-11-24 05:05 UTC: 2); stash.py (2026-11-23 03:40 UTC); dispatch.py (`goods > 5`); table ship_cargo (2026-11-24 05:07 UTC).

- The region lists carry `requires.empty_hold`; a mission reward or kit
  left aboard (fuel cells, probes) closes every census to its scout, and
  the gate names it waiting. The HOLDS line lists them: store what lies
  aboard (stash.py) the same turn; a ship in space is docked first.
- The gate counts five units as nothing (`goods > 5`). Store routes
  have a reach (empire, max_jumps): Voidborn scouts ending frontier
  missions at Altais (8 units, 17 jumps from Central Nexus) had none;
  store-hold-frontier-station-near, where they end, fixes it by script.
  A store route others plan with is never widened for us.
- A census docked nowhere went home to Central Nexus, across the galaxy
  for a newborn of another empire (a foreign station: `Access denied`);
  with --stay it now ends at the nearest station with fuel (census.py
  end_stop, 2026-11-23).

### A field asked for is answered with the books too
Status: proven. Updated: 2026-11-23. Evidence: requests.log ENT-435, ENT-443; tables fields, stats_refill, books.

- Mining asked for uranium, thorium and silicon fields. Every deposit
  read stood near 0 and regrew under 1 unit an hour, taken as fast by
  others, while the asks named thorium and silicon for sale. Answer a
  request for a field with what is left, what comes back an hour, the
  pirates, and the asks of the same good: buying is Trade's (F23), but
  only Intel reads every book.

### A creature that carries a faction's tag is that faction's livestock
Status: proven. Updated: 2026-11-23. Evidence: observations kind ranch (seven lines, 2026-11-23); public_battles 16:51 UTC; admirals.log ENT-110, ENT-113; commit 930c5cfd; game/fleet/store.py read_wildlife.

A ranch (patch 0.732.1) tames a species at a place; its animals carry
the owner's tag in their name ("[HEXC] Patina-Grazer"). A drone of ours
killed one at a partner's base and the owner's pilot destroyed it.
The census files keep every name with its tag (wildlife/<system>.json),
but the store's table herds keeps one name a place and species, the
first animal's: read the files, not the table, for ranches. A turn
files each tagged herd as kind ranch by script (file_ranches.py of the
intel-turn skill); hunt.py leaves tagged animals alone.

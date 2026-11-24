# Intel guidebook -- Lessons (lessons.md)

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
Status: proven. Updated: 2026-11-24. Evidence: intel turn check ROADS, OFFLIST, UNFLOWN, SITES (2026-11-24 14:18 UTC); fill.py status scout (14:31 UTC); runs.jsonl.

- ROADS HALTs under four hours of first visits: widen a list, nearest
  first; ROADS END (all but strongholds read): rotate the explorers.
- A system read by hand and left on no list that is on (`off` counts
  as none) ages unseen (Sol and six more, 2026-11-22): OFFLIST names it;
  it moves onto census-roads.
- A list behind lists that always hold a due system is never reached
  (census-roads, 2026-11-22: no run in ten hours): give it ships of its
  own; UNFLOWN HALTs on it.
- A road whose explorers fly missions paid once empties: census-north 3
  of 6 ships, 12 of 31 systems over 180 min (2026-11-24). Give it, after
  their own region, the cohort nearest it: the Outer Rim scouts (5 to 13
  jumps by Unknown Edge) filled it to 6 of 6 within minutes.

### Read every place the orders name against its cadence
Status: proven. Updated: 2026-11-21. Evidence: intel turn check SITES; reports.log ENT-083.

- Atria, the north outpost's site, stood 571 minutes unread on an
  8-hour list. SITES names every system of the ORACLE block on no list
  read within 180 minutes: move it onto a road list before the commit.

### Read where the fleet works now
Status: proven. Updated: 2026-11-24. Evidence: intel turn check WORKED (2026-11-21, 2026-11-22, 2026-11-24), BELTS (2026-11-24); game/routes/census-worked-far.json.

- After a pause the other divisions fly where only slow lists read (39
  systems, 2026-11-21); the dispatcher's pirate stop (F27) and a mine
  route's min_left rest on a census.
- WORKED names each system where other divisions fly now and no list
  reads within 180 minutes: move it onto the region list of the capital
  nearest it by lanes (the WORKED to line). census-worked-far is flown
  from home and pulls a reader 10 to 17 jumps. Systems that only routes
  paid once pass through print apart, unjudged.
- WORKED sees only where ships fly now: BELTS judges every belt of
  Mining's plan by its list (GSC-0007 at 281 minutes, 2026-11-24).
- After any pause: the home list first, then where ships fly, then the
  roads; judge the gaps from the next reads, not the first hour.

### Hand edits and the plan file
Status: proven. Updated: 2026-11-21. Evidence: errors.log ENT-105; requests.log ENT-279.

- A hand edit that looked for `## Notes` as plain text found its mention
  in the file head and wrote the file twice. Use `plan.py planned` and
  `plan.py note`; plan.py check HALTs on a heading twice (PLANFILE line).
- plan.py writes game/routes/plans/scout.json and plan-scout.md: commit
  them by path, or the next apply waits.

### Times, hashes and files
Status: proven. Updated: 2026-11-24. Evidence: errors.log ENT-034, ENT-047; rule F15; game/fleet/scorecard.py (playbook caps); guide.py drift intel (2026-11-24 14:34 UTC).

- A time in a route, plan or note comes from the clock of the script
  that writes it, never typed (eight files said 03:25 for 03:11).
- A commit hash goes into an entry after `git branch -r --contains`
  prints origin/main: the watcher rebases unpushed commits.
- A data folder gains files (foreign books by base id): a reader that
  globs keeps only one station's records.
- A turn that ended without a report leaves routes no plan names: read
  the ORPHANS line and `git log --author=Oracle` before building a route.
- The scorecard counts a chapter from its first `###`, headers included
  (lessons 90.5%); guide.py drift counts entries (85.1%): keep a chapter
  under 85% by the scorecard's count.

### A census can strand its ship where no station stands
Status: proven. Updated: 2026-11-22. Evidence: errors.log ENT-121; requests.log ENT-334; data/routes/runs.jsonl (2026-11-22 01:12 to 03:18 UTC).

- A far list holds systems without a station. A read that ends there
  leaves the ship in space, and a tank short of home keeps it there:
  every next census is refused for fuel, each run 1.5 minutes long, so
  the dispatcher's rest for runs under a minute never fires.
- Read the runs, not only the ages: a pilot with many census rows of 0
  places and 0 credits in a row is stuck (STUCK line). Rescue by hand:
  hold, the nearest station whose read lists `refuel`, dock, refuel,
  release. census.py now takes fuel first when the tank is short.

### The game's own records answer what no census saw
Status: proven. Updated: 2026-11-21. Evidence: requests.log ENT-310; admirals.log ENT-077; observations kind raid; https://game.spacemolt.com/api/battles.

- A base raid is category `npc` in /api/battles, not `pirate`: a pirate
  reading misses every raid. It takes `category`, `limit` and `offset`;
  a `system` filter is ignored: page back by offset and filter in code,
  one call a second.
- The faction's own log: get_action_log with `faction_id` (category
  faction: deposits, refuels, repairs) dates when a base last worked.
- Our outpost stood wrecked three days before any member read it: a
  question about the past goes to these records first, the census after.

### Calls that surprise
Status: proven. Updated: 2026-11-24. Evidence: gate.py; the game's help (2026-11-15 to 17); route_run.py (lines 1172, 1339); dispatch.py; table runs (strip route, 2026-11-24).

- gate.py cuts an answer at 3,000 characters: read long answers with
  FULL=1. get_empire_info takes `empire_id`. get_system answers the
  ship's own system whatever system_id says.
- The stance is the raw action `default_stance` `{"stance": "flee"}` in
  group spacemolt_battle (scripts/set_stance.py); a new scout gets it once.
- fleet-build.sh install runs minutes: background it, poll to its last
  line (errors.log ENT-115).
- route_run.py works a stop's `gift` before its `unfit` and `store`: a
  stripped module is given by a second route (errors.log ENT-178).
- `requires.in_system` waits for chance: a once-per-pilot chore at one
  station took 1 of 18 scouts in 95 minutes, then 3 in five minutes on
  `max_jumps` 2. in_system is for the docked watch. A strip route is
  `standing`: the loss stop exempts `fit`, never `unfit`.

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
Status: proven. Updated: 2026-11-24. Evidence: fill.py status scout (2026-11-23, 2026-11-24: 'hold not empty'); stash.py; dispatch.py (`goods > 5`); table ship_cargo; census.py end_stop.

- The region lists carry `requires.empty_hold`; a reward or kit left
  aboard (First Steps ore, fuel cells, probes) closes every census to its
  scout over five units (HOLDS line): store it the same turn (stash.py;
  a ship in space docks first).
- Store routes have a reach (empire, max_jumps): scouts that end
  frontier missions at Altais have store-hold-frontier-station-near. A
  store route others plan with is never widened for us.
- A census docked nowhere went home across the galaxy for a newborn of
  another empire (`Access denied` at a foreign station); census.py now
  ends at the nearest station with fuel (end_stop, 2026-11-23).

### A field asked for is answered with the books too
Status: proven. Updated: 2026-11-23. Evidence: requests.log ENT-435, ENT-443; tables fields, stats_refill, books.

- Mining asked for uranium, thorium and silicon fields. Every deposit
  read stood near 0 and regrew under 1 unit an hour, taken as fast by
  others, while the asks named thorium and silicon for sale. Answer a
  request for a field with what is left, what comes back an hour, the
  pirates, and the asks of the same good: buying is Trade's (F23), but
  only Intel reads every book.

### A creature that carries a faction's tag is that faction's livestock
Status: proven. Updated: 2026-11-23. Evidence: observations kind ranch (2026-11-23); public_battles 16:51 UTC; admirals.log ENT-110, ENT-113; game/fleet/store.py read_wildlife.

A ranch (patch 0.732.1) tames a species at a place; its animals carry
the owner's tag in their name ("[HEXC] Patina-Grazer"). A drone of ours
killed one at a partner's base and the owner's pilot destroyed it. The
census files keep every tagged name (wildlife/<system>.json); the
store's table herds keeps one name a place: file ranches from the files
(file_ranches.py); hunt.py leaves tagged animals alone.

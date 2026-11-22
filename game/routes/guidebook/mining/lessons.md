# Mining guidebook -- Lessons (lessons.md)

### How this guidebook is kept
Status: proven. Updated: 2026-11-16. Evidence: migrated from guidebook/mining.md, the text above its first section.

Kept by Zero; read by every member. What the Mining division
learned about its routes, its levelling and its ships, so that every
ship born later starts where the others stand. Started by the Fleet
Admiral on 2026-11-15 from the runs so far; from here Zero writes it,
at the end of every turn.

- A figure comes from `python3 -B game/fleet/routes.py measure` or from a
  run's RESULT line, and carries its date. A number no record holds is
  written `not measured`. Every earning is in credits per ship-hour
  (orders F19).
- The plan in force is the division's plan file (data/plans/plan-mining.md
  in the unit, the tool plan); `game/routes/plan-miner.md` shows it with
  counts and no names. Every route with its figure: `game/routes/master-index.md`
  and its sub-indexes. The fleet as it flies: `python3 -I -B game/fleet/hive.py
  standing`; the next four hours: the tool hive, verb forecast.

### Size work on what regains
Status: proven. Updated: 2026-11-21. Evidence: errors.log ENT-015; the ice runs of 2026-11-16 (data/routes/runs.jsonl); hive.py refill; data/market/history.jsonl.

- Size every selling station on what its bid regains (hive.py refill),
  never on its standing depth: The Experiment's 15,832 water ice at 36 cr
  was one order, gone in three hours and regaining 10 an hour; 36 runs
  then stored their ice (2026-11-16). The `max_ships` selling there add
  up to no more than regain x 4 / a ship's units in 4 hours.
- A regain is an average over its window (30 h): read the best bid's
  last moves (the tool market) before sizing on it.
- A bid's depth is `best_buy_qty`, never `buy_quantity` (the sum of all
  levels); read the book per level before naming a chain.
- Stored goods are sold before more are mined: divide what is stored by
  what all the bids regain; while that is more hours than the turn,
  nothing of it is mined for sale.
- A STALLED route sold nothing in its last three runs (stalled.py): its
  bid is gone; move its ships and keep one to sell what the bid regains.
- A bid is stale in hours: print it, never recall it.

### Fields, power and the pull
Status: proven. Updated: 2026-11-21. Evidence: spacemolt.com/docs/guides/miner.md (2026-11-15); table readings; chains.py of the skill mining-chains.

- `can_lock = power x F > 20`: a fit of power 20 or less (Mining Laser I
  5, Ice Harvester I 8) never locks, so no deposit refuses it, however
  thin; its rate is capped at remaining / 20 a pull. Screen deposits by
  `supported_power` against the fit, never by share of capacity.
- Energy crystal is taken by a mining laser and lies in nebulae at
  richness 3 to 4; it regrows fast (26 to 68 in 42 minutes at one nebula,
  2026-11-15).
- Regrowth between two census reads is net of other players' mining:
  diff the history store (table readings), and order iron fields by the
  share each gave up between two reads.
- Common ores (carbon, iron, copper, nitrogen ice) are asked at 1 to 4 cr
  at every station: mining them saves nothing unless the reserve lacks
  them; they train.
- Mining XP is one point a unit mined, plus mission XP.

### Runs, holds and the dispatcher
Status: proven. Updated: 2026-11-22. Evidence: errors.log ENT-032; dispatch.py stored_missing; the runners' notes; data/fleet/gifts.jsonl; data/stock/storage.json of 2026-11-21 19:34 UTC.

- More than five units aboard close every `empty_hold` route to a ship:
  read a waiting miner's `cargo` before calling it idle; dock and store,
  never sell under a standing bid elsewhere (F12).
- An engine loop without a runner (busy by hand, no orders file) stores
  and sells nothing: stop it (`gate.py delete /accounts/<pilot>/loop`),
  sell, release.
- A route's loss is read with its notes first: "not docked for the sale"
  and "crashed:" are the runner's, not the field's. A failing new step
  closes a route for up to six hours after three runs: one ship first.
- A run's `delta` is wallet before and after, gifts between our ships
  included: read a route by its median run or take the gifts out.
- A stop file does not free a miner inside a turn; a background script
  ends with the turn's session: a bounded --minutes, its state file read
  at the next turn.
- After a pause the storage book holds only the pilots read since: a gate
  or a chain on stored goods reads short until every pilot is read again
  (89 of 246 pilots and no miner 10 minutes after the resume of
  2026-11-21).
- `requires.stored` names one item, a list all of them: a give route
  gated on iron never sends a miner whose storage holds only ice or
  copper; gate a copy on the station's main other good (2026-11-22).

### Writing to the repository
Status: proven. Updated: 2026-11-21. Evidence: errors.log ENT-021; requests.log ENT-078; the skill mining-chains.

- The logs are public: no entry or commit says which pilot flies which
  route. Before every append or commit: `grep -nE
  '(miner|hauler|trader|scout|drone|sentinel)-[0-9]+' <file>`.
- Times come from a record (`date -u`, the git log, a RESULT line),
  never typed.
- New route files go into the clone before the plan that names them,
  then `routes.py check`, `index`, one commit by path.
- `routes.py measure --write` writes every route file's measured block:
  read `git status`, revert the foreign ones, commit my own.
- `requires.stored` is sized on what one pilot stores, never the fleet's
  total; `requires.module` takes one value.
- The tool fill with write=true adds up to 8 tests: read its dry run
  first and set off any that sells a good the reserve is short of.
- A miner that drops out of the fleet file makes plan.py check HALT on
  its row: take the row out, apply, set it again when it is back.

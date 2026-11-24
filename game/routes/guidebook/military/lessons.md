# Military guidebook -- Lessons (lessons.md)

### How this guidebook is kept
Status: proven. Updated: 2026-11-21. Evidence: rule F14; queue.log ENT-189.

Kept by Apophis, read by every member: what Military learned about its
routes, levelling, ships and the pirates near us. A figure is named by the
call that prints it (`hunt_figures.py`, the tool fleet, `hive.py route`),
with its date where a dated reading is the evidence; a number no record
holds is `not measured`. A reading is never a verdict: what a route earns
now is asked each turn (F22). An outdated entry is retired and tidied
(`scripts/guide.py tidy military`); the store keeps every version. The
turn's procedure is the skill military-turn; its lessons stand here.

### Commits, hashes and times
Status: proven. Updated: 2026-11-21. Evidence: errors.log ENT-049, ENT-068, ENT-110; requests.log ENT-126; queue.log 2026-11-16 18:36 and 19:10 UTC.

- Route files are committed with `route_commit.py` (skill military-turn):
  it parses each file, runs `routes.py index` and `check`, and commits the
  named files and the index only. A `git status` of the folder once took
  another member's line under my name.
- `plan.py` and the fill tool refuse every division while any file under
  game/routes is modified: commit at once, never leave an edit open; wait
  30 to 60 s when another member's file holds it.
- `routes.py measure --write` writes every route file of the fleet: run it
  on a clean tree, `git checkout --` what is not mine, then index.
- The watcher may rebase a commit under a new hash: run `check_refs.py` a
  minute after the last commit, before a report or a log entry names it.
  A time in a log entry is copied from `git log` after the action.

### Holds and hands
Status: proven. Updated: 2026-11-21. Evidence: errors.log 2026-11-16 and 2026-11-17; skill military-turn; queue.log ENT-189.

- By hand only a call's first flight (one ship, ten minutes) and a rescue;
  anything longer runs in the background (`terminal(background=true)`).
- `gate.py hold`, then the script; a runner's order file replaces the hold
  and is removed at its end, and `stash.py` releases at its end: chain the
  hold right after it. Release every ship docked; at the end of a turn
  `grep -l "hand Apophis" data/fleet/orders/*` prints nothing.
- To take a busy drone: loop over the candidates' order files and hold the
  first that is free in the same second.
- A script that takes free drones takes the first to come free, far or
  near: name the candidates or bound them (`--max-jumps`).
- A runner the dispatcher starts in the same seconds may write its order
  over a fresh hold (2026-11-21, requests.log ENT-289): wait one pass
  after a take and keep the pilot only while its order file still reads
  `hand Apophis`; dock again right before a fit.
- A killed background script may leave holds: release each by hand.
- `withdraw` with `target: cargo` is refused by the gate's wall: the plain
  withdraw goes to the own hold; a wall refusal is reported, never worked
  around.

### Reading figures right
Status: proven. Updated: 2026-11-21. Evidence: errors.log 2026-11-15 to 2026-11-17; requests.log ENT-006, ENT-156, ENT-264.

- A kill rate or a payback comes from a measured fight, never from catalog
  damage against hull: the prey's armour is not in that sum.
- A log line is cited with its own run: match the log's time to the run
  row's `started`.
- In the hour of the weekly tax a run's raw `delta` carries the tax:
  `taxes.py` gives it back in the figures; read data/fleet/taxes.json first.
- A herd count taken before the last hunt at the place is stale.
- The route index may count fewer runs than runs.jsonl: name the method.
- A census route counts every census order on its systems, other
  divisions' too, toward its `max_ships`.
- A ship file read right after a dock may predate the repair.
- A wreck list holds older carcasses, ours too: count only new wrecks.
- `observe.py add` refuses a note over 400 characters and writes nothing:
  check its `added` line.

### Hunts, bids and the reserve
Status: proven. Updated: 2026-11-24. Evidence: reserve_hunts.py; loot_bids.py; data/stock/storage.json; errors.log ENT-108; runs.jsonl 2026-11-24 01:20 to 06:30 UTC.

- A money hunt names its loot's bid (`requires.bid` {item, base,
  min_price, min_qty}); a bid gate takes the price at the depth that comes
  and goes, never one run's loot.
- Loot the reserve holds back (curd, carapace, biogas, vials): `min_bid`
  5000 and stored (F24); `reserve_hunts.py` FLAGs a hunt each turn.
- The sale follows the buyer: compare the best book of every station on
  record with the `requires.bid` base of each sale route; a far bid many
  times the home bid gets a sale from where the goods lie (per pilot, per
  station: storage.json), its road read against the pirate record.
- `requires.stored` reads the ledger (about 40 minutes): a sale by hand
  just before sends a pilot on an empty run.
- The fallback never serves a target only a turn reads: 46.5 ship-hours of
  iron after the order ended it (errors.log ENT-108).
- A hunt keeps two animals (F38), so `min_creatures` is at least 3: at 2
  the dispatcher sent hunters to herds they could not touch (12 zero-kill
  runs on four routes in five hours). The dispatcher trusts a census only
  90 minutes; a far herd with an older one is flown blind.

### Plans, fills and claims
Status: proven. Updated: 2026-11-24. Evidence: fill.py; comms.py; requests.log ENT-158; table runs (strip-pulse-laser-central-nexus); dispatch.newborn_reason; 2026-11-17, 2026-11-21 and 2026-11-23 turns.

- The fill gate judges a route by its all-time figure: a hunt whose bid or
  herd is gone gets `status: off` with the record, never put back.
- `fill write=true` may add a route another division claims or work of
  another class (a visit mission, Mining's own craft): read its lines and
  drop those with `fill action=drop`.
- A route another plan holds too is changed by a request to its writer.
- `comms.py append admirals` refuses a claim on a route another division
  claims: leave it out of claim and plan until released.
- The dispatcher may start a route in the minute before a plan commit:
  read data/fleet/orders/ after.
- The loss stop counts a refused accept of a once route until its window
  moves on; a training route takes `requires.skills_below` and is left
  alone by the loss stop.
- Count the holders of each once link each turn: a missing first link kept
  Voidborn Mastery at 0 for every drone.
- The newborn reach (6 jumps) counts from where a ship stands, not from
  its capital: one `far_ok` trip into our corridor (`join-corridor-*`,
  last in the row) opens every home hunt to it. A far ship with a loaded
  hold cannot reach a store route: the trip stores at its end (2026-11-23).
- Another division's strip route (`unfit` of a pulse laser) is fitting,
  open to every class: in the First list it disarmed five hunters, and
  `fill write=true` put it back. Read every route fill adds for an
  `unfit` of a weapon and drop it; rearm by `rearm-pulse-laser-*`.
- The gate passes with ships on `park`: read its `on park` count each turn
  (30 on 2026-11-24, every home herd taken or resting) and write herds
  further out for them (the scratch generator, F23).
- Partner ranches (admirals.log ENT-113): a hunt at a ranch place or in a
  partner's system is `status: off` (F2, F4).

### Battles and stuck ships
Status: proven. Updated: 2026-11-23. Evidence: errors.log 2026-11-16; admirals.log ENT-110; observation kind ranch (aspidiske); stuck_check.py; requests.log ENT-369; table runs 2026-11-23 06:52 to 07:10 UTC (hull_before, hull_after); ship files (ships_lost).

- A ship left in a battle (three runs that never reach stop 1, or
  `in_battle` in its log) is freed with the battle stance flee
  (`spacemolt_battle stance`), then `prepare-at-station`. The combat mode
  flee is not the battle stance.
- A hunt sets the combat mode `external`, which ends the engine's own
  flight. A ship still in a fight from the run before, handed hunt after
  hunt, is shot through runs of two minutes each: two newborns went from
  50 and 34 percent hull to lost in five and three such runs. Read
  `hull_before` of a chain of short zero-kill runs as a ship in a fight.
  The runner fix (flee first, repair under 60 percent) is installed
  (b8b901ae).
- A moving station (table stations, `mobile`) can stand in a system whose
  census predates its arrival: runs to it fail at stop 1 ("It's called a
  Mobile Capital"). The fix (the station list's system, the poi an older
  census named) is installed (2c2604b7).
- A creature named with another faction's tag ("[HEXC] Patina-Grazer") is
  that faction's ranched livestock: its owner joins the fight. A hunter
  that fled such a pilot and came back to the herd was lost (2026-11-23,
  admirals.log ENT-110). hunt.py leaves tagged creatures alone
  (930c5cfd). The fix that ends the hunt at the place when a ship joins
  our fight waits for its install (requests.log ENT-472).
- A ship with an ammunition weapon hunts only with ammunition aboard.
- A fight a drone starts opens at fire whatever its default stance.
- A dry tank where no station stands: the game's tug (`distress_signal`
  tow) docks the ship at the nearest public station; `tow_rescue.py`.
  A hunt whose runs buy no fuel never refuelled at its sell_at
  (`station_fuel_empty`): set it off (errors.log, 2026-11-22).

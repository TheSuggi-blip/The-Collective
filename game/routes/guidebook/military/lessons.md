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
Status: proven. Updated: 2026-11-21. Evidence: reserve_hunts.py; loot_bids.py; data/stock/storage.json; errors.log ENT-108.

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

### Plans, fills and claims
Status: proven. Updated: 2026-11-21. Evidence: fill.py; comms.py; requests.log ENT-158; 2026-11-17 and 2026-11-21 turns.

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

### Battles and stuck ships
Status: proven. Updated: 2026-11-22. Evidence: errors.log 2026-11-16; stuck_check.py; group_hunt.py logs; requests.log ENT-369; tow_rescue.py output 2026-11-22 20:22 UTC.

- A ship left in a battle (three runs that never reach stop 1, or
  `in_battle` in its log) is freed with the battle stance flee
  (`spacemolt_battle stance`), held between two runner passes, then
  `prepare-at-station` and release. The combat mode flee is not the battle
  stance: a drone sat 65 minutes at range 4 with stance fire.
- A ship with an ammunition weapon hunts only with ammunition aboard.
- A fight a drone starts opens at fire whatever its default stance.
- A dry tank where no station stands: the game's tug (`distress_signal`
  tow, 5 minutes, 500 cr) docks the ship at the nearest public station;
  `tow_rescue.py` holds, tows, refuels, releases. A hunt whose runs buy no
  fuel never refuelled at its sell_at (`station_fuel_empty`): set it off
  (errors.log, 2026-11-22: two ships, about three hours stranded).

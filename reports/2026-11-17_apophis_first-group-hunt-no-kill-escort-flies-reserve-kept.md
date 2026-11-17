---
name: first-group-hunt-no-kill-escort-flies-reserve-kept
id: 20261117T205855Z
tier: report
trigger: session-end
author: Apophis
tags: [military, group-hunt, escort, reserve, pirates, sentinels]
links:
  - reports/2026-11-17_apophis_escort-follow-built-far-bids-gone-curd-stored.md
  - reports/2026-11-17_unity_sentinels-to-military-treasury-holds-desk-fee.md
---

# Military -- The First Group Hunt Answered the Fleet's Questions and Made No Kill; the First Escort Flies; Hunts Keep the Reserve's Goods

## Situation

Period: from my report `reports/2026-11-17_apophis_escort-follow-built-far-bids-gone-curd-stored.md` (turn of 16:00
to 16:53 UTC) to the end of my scheduled turn of 20:00 to about 21:00 UTC on 2026-11-17. Orders in force:
`communications/orders.log` ENT-042, replaced at 20:11 UTC by ENT-044 (the same block APOPHIS: hunt one hunter a
herd, guard where our ships gather and the outpost, write the first escort, plan the 20 sentinels until Piloting 20,
one group of three by hand on a pilot whale, no pirate test, group or fight). ENT-045 came at 21:02 UTC, during my
session-end: no guard and no escort in the first ring of outposts and its roads (rule F33), levelling, hunting and
farming meanwhile; my plan follows it since 21:07 UTC (Plans). The plan for my division is in
`reports/2026-11-17_unity_sentinels-to-military-treasury-holds-desk-fee.md`, section Plans.

```
Ships: 70/70 at work (50 drones, 20 sentinels), grounded: 0, lost: 0
Credits: start not measured in this run; end 3,207,385 in the division's wallets; net +69,938 steady and 230,601 paid once by the runs of 16:45 to 20:20 UTC
Output: 170,341 units of 16 reserve items held, +19,291.6 units an hour over 4 hours
Source: fill.py check (20:58 UTC), hive.py fleet (20:21 UTC), the table runs (448 runs, 203.9 ship-hours), hive.py flow (20:21 UTC)
```

The last hour to 20:21 UTC read +25,899 cr net (income 45,023, costs 19,124; `hive.py fleet`). The goal my plan
carried into this turn, steady money above zero, held in the three clean hours of `hive.py history`: +4,767 cr
(16:58), +34,866 (17:58), +4,489 (18:58). The hours of 19:59 and 20:51 read +210,802 and +130,963 while Command read
-166,499 in the first: moves between our own purses bend them, and I do not use them. The forecast (`hive.py
forecast Apophis`, 20:49 UTC): steady 20,904 cr an hour, 299 a ship, 83,618 in 4 hours, 9,110 paid once on the way;
it takes each hunt's figure over all its runs, so the melt hunts read high while no melt bid stands. No stranger
fired at a ship of ours, and no ship is held by hand (`grep "hand Apophis"` over the order files printed nothing).

## Activities

**The group test (D14), by hand, 20:12 to 20:38 UTC.** My new script `group_hunt.py` (skill military-turn) took four
free drones, docked them at Central Nexus, set their battle default stance to fire, made a game fleet and flew it to a
pilot whale of 220 hull at Stellar Siphon in Nexus Prime (the drones' log lines `group_hunt:`; observations kind
`group_hunt`). What the game answered:
- `create` answered max_size 3; the third invite answered `fleet_full` ("3 members + pending invites"): the leader
  counts in the three.
- The leader's flight brought both members to the place, and its `hunt` pulled both into the battle at tick 0.
- The fourth drone, outside the fleet, hunted the same whale and stood on the same side at tick 3: a side is not capped
  at the fleet's three.
- Only the leader fought. At tick 10 it stood at dist 2 with the whale as target, 8 dealt and 106 taken; the three
  others stood at dist 3 with no target, 0 dealt and 0 taken; the whale read 84 percent. The leader's shield (111
  percent) was gone in 8 ticks; the side fled at tick 13 (leader 48 percent hull, 33 after the flight), the whale at
  79 percent. No kill, no loot, no ship lost; all four repaired.

**The first escort route.** `escort-voidborn-conductive-lattice` (commit 9b3c5a9) follows one pilot of ours on the
Node Beta chain, which buys silver beyond the border. The dispatcher started it at 20:33 UTC. Its first run row
(data/routes/runs.jsonl): 23.1 minutes, 7 looks, 6 jumps beside a hauler, 55 strangers seen, hull 100 percent, -169
cr, left "guarded ship gone" when the hauler's run ended. A second run began at 20:57 UTC beside another pilot, before
orders ENT-045 took escorts out of the first ring (Plans).

**The reserve at the sale.** Four hunt runs sold 13 superfluid vials (7,800 cr) the reserve holds back. `hunt.py` now
stores every good `surplus.py` keeps, for every division's hunts (commit d93c033, `fleet-build.sh install`, three new
tests failing first; queue.log ENT-183). The Oxbow and Hassaleh frost-moth hunts store at Node Beta. Stored per hour
over 4 hours: copper piping +627.9, steel plate +587.5, carapace +353.7, biogas +70.3 (`hive.py flow`).

**Pirates (D9 kept).** Intel's census read six Nyx pirates at Violethall Belt (13:16 UTC) and ten Dross raiders at
Hollowcrest Frozen Drift (19:06 UTC). The hunts there and at Alathfar (one lane away) left my plans; `pirate_places.py`,
now over both roles, read PASS. Request ENT-250 asks Unity about the command plan's Violethall hunt.

**Sentinels (D12).** All 20 fly their own far hunts first, then `@hunter`: +16,782 cr in 1,755 hunter-minutes, 574 cr
a hunter-hour from 16:45 to 20:20 UTC (`hunt_figures.py --role sentinel`).

**Hunts, sales, guards.** Melt sales: 12 runs, +55,996 cr while Sirius bid 1,484 to 1,502 (18:04 to 19:44 UTC). Drone
hunts: -174 cr in 4,395 hunter-minutes. Six far tests went out at 20:19 UTC. Guards: 13 runs, 12.4 ship-hours, -983 cr,
no shot; the post at GSC-0044 stood across the outpost's founding (requests ENT-248 closes Apollo's ENT-219).

**Skills.** Drones' medians (ship files, 20:17 UTC): gunnery 4 (2 to 7), weapons 3, tactics 4, xenobiology 4; at
16:16 UTC they read 4, 2.5, 3 and 3 (the guidebook's Class Card then), so tactics and xenobiology rose one level,
weapons half, gunnery held. Sentinels 2, 1, 2, 2. Piloting 5 / 7 / 9, 36 hours to 10 (tool fleet, view levels).

## Problems

- **The group made no kill.** Cause: a member pulled in by the fleet joins with no target and stays a zone back; my
  script set the stance only. Done: the script now sets each member's target and advances it to one zone from the
  prey; it also counts only wrecks that were not there before the fight, because it read six old carcasses as a kill.
- **Reserve goods sold** (errors.log ENT-099). Cause: the rule stood in a route's `min_bid` and a turn check of the
  drone plan; the sentinels joined between turns. Done: the runner keeps them at the sale.
- **Two rows of mine carried a hunt Intel claims** (hunt-titawin-gas-cloud-chlorophage, admirals.log ENT-050). Cause:
  rows inherited from the filler and from the command group were never read against the claims. No ship of mine flew
  it (table runs: only a scout since 12:00 UTC). Done: out of both rows at 20:55 UTC.
- **The filler put a far test in front of a guard drone** whose first route was a sale, not `@guard`: one post stood
  empty from 20:20 UTC for the test. Done: that drone has `@guard` first again.
- **The first install halted** ("the clone was not clean in four minutes": other members' files); the second went in.
- **Not explained:** the leader dealt 8 while the whale lost 16 percent of 220 hull by tick 10.

## Plans

Inside orders ENT-044, my own choices:
- **The second group flight**, by hand with the fixed script, on a pilot whale near home: whether three ships with a
  target kill it, the loot, and what each ship deals and takes. From it I give the Fleet Admiral the steps for the
  dispatcher's `group: N`. A whale took the leader's 111 percent shield in 8 ticks, so the flight flees at 60 percent
  hull as before; a second weapon or a shield fit waits for its record.
- **The escort (orders ENT-045):** read the first RESULT line of `escort-voidborn-conductive-lattice`, whose one run
  started at 20:33 UTC; since 21:07 UTC no drone has it, because its road lies in the first ring. The next escort
  serves beyond the first ring, at the stations and the outposts past it once they stand; before then, the next step
  of `guard.py --follow`, flying to the circuit's next stop instead of trailing a jump behind.
- **The six far tests** of 20:19 UTC (cinder-sylphs at GSC-0035 and GSC-0045, hollow-pilgrims at GSC-0037, GSC-0042,
  Sandrift and Yildun): a test that pays keeps its herd's one hunter; one that leaves for a stranger or loses twice
  rests by D13.
- **Each turn:** `reserve_hunts.py` and `pirate_places.py` over both roles; a pack at a hunt's place, or one lane off,
  takes it out of my plans.
- **Guards (orders ENT-045):** the seven posts (Schedar, the two Ironhollow fields, Garnet, Achernar, Marfik and
  GSC-0044 Belt) stand 2 to 6 jumps out, in the first ring, so the six guard drones fly `@hunter` since 21:07 UTC; the
  runs under way end by their minutes. `@guard` waits for the posts beyond the first ring.
- **Sentinels:** their far hunts first, Piloting toward 20 (now 6 to 8).
- **Goal for the next turn:** Military's steady money above +15,000 cr an hour over the four hours to my next turn
  (`hive.py fleet`), read then.
- **Not now:** a new hull or a fit for groups; no pirate route while the block says no test.

## Suggestions

- **The dispatcher's `group: N` (Unity's to build):** give each member its own `hunt` of the same creature, a
  `target` and an `advance` to the prey's zone; use the game fleet only for the common flight. Reason: the first
  flight's members watched while the leader took all the damage. Cost: a step per member per tick.
- **The filler's guard check (Unity's):** count a ship as a guard when `@guard` stands anywhere in its own routes, not
  only first. Reason: one post stood empty from 20:20 UTC. Cost: one condition in `fill.py`.
- **A claim check of plan rows (Unity's):** `plan.py check` names a ship whose own route another division claims (rule
  F25). Reason: two of my rows held Intel's claimed hunt unseen. Cost: one read of the claims in force.
- **The pirate gate (Unity's):** a pack heavier than any side we field (ten raiders, about 1,370 hull) keeps its system
  closed until a newer read shows it gone, not six hours. Cost: a weight figure in the gate.

## Feedback

- **`fill.py fill drone --write`:** worked; 12 routes in one commit (80f8dab). It offered `hunt-raysheet-nebula-veil-ray`,
  whose curd and carapace the reserve keeps, and two hunts 24 and 25 jumps out; I took those out. The claim gate
  (ENT-241) did not catch Titawin on my rows, since those rows were not its additions.
- **The guard rule of ENT-241:** held for drones with `@guard` first; missed the one with a sale first (above).
- **The dispatcher's escort (requests ENT-237):** worked at first try: `guard escort-voidborn-conductive-lattice`
  started 20:33:46 UTC, "following" the hauler, four looks in 15 minutes.
- **`plan.py set`:** each call printed the same three to fourteen `note` lines about other ships' first routes; one
  summary line would be easier to read. An edit of `## Planned` by hand went into `plan-drone.md` and
  `plan-sentinel.md` at the next `plan.py apply` (commit 2f5bddf), as the skill says.
- **`fleet-build.sh install`:** the gates are good; it waits for other members' uncommitted files and halts after four
  minutes, so I ran it in the background the second time (about nine minutes).
- **`observe.py add`:** refused a note of 850 characters with a clear reason; a script that does not read its answer
  loses the record, so my script now cuts at 400.
- **`hive.py history`:** per-division hours read +210,802 for Military beside -166,499 for Command; a column without
  moves between our own purses would make the hour usable.
- **`hive.py flow`, `forecast`, the tool `stock` and `comms.py append`:** each answered at once and agreed with the
  runs. Not used yet: `hive.py gauges` (queue ENT-181); the next group flight reads it before the start.
- **Built myself:** `group_hunt.py` and the `hunt.py` reserve step; `pirate_places.py` and `reserve_hunts.py` over both
  roles.

## Learnings

From my learning capture of this turn:

- **Joining is not fighting.** The game puts a fleet's members into the leader's battle, but a member with no
  target deals nothing; a ship outside the fleet that hunts the same creature fights on the same side. Record: the
  group test of 20:12 to 20:38 UTC (only the leader dealt damage, 8 of it, and took 106; a fourth ship joined at tick
  3). Military now sets each member's target and closes it in, and counts a side by the ships that fire. For the fleet:
  any convoy, escort or scout group should read each ship's own part in a fight, not the side's. Kept in
  `knowledge/weapons-fits-and-hulls.md`.
- **A rule belongs in the step that acts, not in a check at the turn.** Record: 13 superfluid vials sold by four runs
  between two turns, three on a sentinel hunt my drone-only check never read. Military now keeps the reserve in the
  hunt runner itself and reads both roles each turn. For the fleet: a division that gains ships between turns gains
  rows no turn check has read. Kept in `knowledge/hunting-herds.md`.
- **Confirmed:** a melt bid of depth stands one to two hours and goes to whoever comes first (Sirius 18:04 to 19:44
  UTC; First Step Memorial 1,814 x 99 to 1,794 x 11 in 24 minutes); the sales gated on the bid took +55,996 cr without
  a hand.
- **Open:** why the whale lost more than the leader's damage; which hit trains Shields and Armor (0 on every ship).

Skill: military-turn changed -- the group test step, both roles in the checks, three pitfalls (observe note limit, old
wrecks, a ship file read before its repair)

## Cross-links

- `reports/2026-11-17_apophis_escort-follow-built-far-bids-gone-curd-stored.md` -- my previous report
- `reports/2026-11-17_unity_sentinels-to-military-treasury-holds-desk-fee.md` -- the Fleet Admiral's report in force
- `communications/orders.log` ENT-042, ENT-044 -- the orders of this turn
- `communications/requests.log` ENT-248, ENT-250 -- my answer to Apollo, my request to Unity
- `communications/errors.log` ENT-099 -- reserve goods sold between turns
- `communications/queue.log` ENT-183 -- the hunt runner keeps reserve goods
- `communications/admirals.log` ENT-057, ENT-058 -- my claim and my note
- `game/routes/guidebook/military.md` -- Standing Plan of 20:20 UTC, Group hunts, readings
- `game/routes/escort-voidborn-conductive-lattice.json` -- the first escort route

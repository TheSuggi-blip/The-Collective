---
name: outpost-repaired-itself-repair-stock-kept-atria-asked-for
id: 20261122T002157Z
tier: report
trigger: session-end
author: Apollo
tags: [logistics, outpost, bases, needs, freight, passengers]
links: [reports/2026-11-21_apollo_outpost-wrecked-repair-by-route-every-hauler-at-work.md, reports/2026-11-21_unity_cut-deposit-booked-sweep-writes-ahead-test-round-ends.md, communications/orders.log]
---

# Logistics -- The Outpost Repaired Itself; Its Repair Stock Is Now Kept by Route, and Atria Is Ready to Fund

## Situation

This report covers the scheduled turn from my previous report
(`reports/2026-11-21_apollo_outpost-wrecked-repair-by-route-every-hauler-at-work.md`,
reports.log ENT-088, 2026-11-21 20:42 UTC) to 2026-11-22 00:22 UTC. The orders in
force are orders.log ENT-059 of 2026-11-21 22:51 UTC: Suggi's new standing orders
S2 and S3 (the most dominant fleet; dominate the galaxy), the new goal G5 (a roster
of 500 and the buildings it takes), P1 (steady net above zero over 24 hours), P3
(Atria, then Yildun) and P5 (research the game online and the role). My block:
keep the reserve by its levels and the outpost's bunker by route; prepare Atria's
kit and road and found it once GSC-0044 runs by itself; build the Recruitment
Center when the purse holds its fee; carry and supply beyond our borders too; put
the buildings G5 wants into the needs register.

```
Ships: 40/40 at work, grounded: 0, lost: 0
Credits: start 1,692,277 (briefing, 23:46 UTC), end 1,693,596 (hive.py fleet, 00:21 UTC), net +1,319
Output: GSC-0044's two facilities read ready (faction_owned, 2026-11-21 23:48 UTC); 7 needs registered; 3 routes changed, 1 written
```

The credits figure of the start is the briefing's at the turn's start, since the
wallets between my last report and this turn were read by other members' passes;
the steady change of Logistics per hour in the hour to 00:20 UTC was -7,527 cr
(the tool fleet, view=history) and its costs -18,866 cr an hour against 928 of
income in the last hour (hive.py fleet, 00:21 UTC). The fleet held 10,844,972 cr
in wallets and the treasury 677,210 cr (stats kpi, 23:50 UTC); the fleet's steady
net read +12,236 cr an hour over 24 hours and -21,605 over the last hour (stats
kpi). At the turn's start the fill gate read PASS with 39 of 40 haulers at work
and one by hand; at 00:21 UTC it read 40 at work, 0 waiting.

## Activities

**The outpost (block APOLLO: keep the bunker by route).** The turn opened with the
game's own read of our facilities (`faction_owned` through a docked hauler, a free
read). Both of GSC-0044's facilities, the Fuel Bunker and the Lockbox, read
`ready` at 23:48 UTC: the repair bill delivered last turn (180 steel plate, 60
circuit boards) was taken by the base itself. The faction store there then held 15
circuit boards and no steel plate (empire.json, 23:49 UTC): the repair used 180
plate and 45 boards. The bunker read 4,058 fuel, just over the 4,000 floor of
`supply-bunker-gsc-0044`, whose reserve gate is on since 21:20 UTC (requests.log
ENT-300).

**Its repair stock.** The game's base-builder guide (read this turn) says a wrecked
base starts every repair its own store can pay each cycle. So the bill of the next
raid now stands in the base's store, kept by route:
`supply-repair-gsc-0044-boards` runs under `requires.reserve` below 45 boards at
the outpost (open at 15: a hauler took it at 23:59 UTC), 30 boards a run;
`supply-repair-gsc-0044-plate` carries three more loads of 60 (max_pilots 3 to 6).
Both items are needs of the register (`gsc-0044-repair-plate` 180,
`gsc-0044-repair-boards` 45, priority 1). Commit d5160e92.

**Atria (P3).** GSC-0044 runs by itself again, the condition my block names. I
asked Unity to pay the allocation she gave in ENT-272 (requests.log ENT-314):
150,150 cr into the builder's wallet, kept out of the sweep until the kit is
bought, and the 100,000 cr fee from the treasury. The kit is need
`atria-outpost-kit`; the builder is named in the plan file's Notes.

**G5 and the needs register.** Seven needs of Logistics stand in game/needs.tsv
(commits e496b431 to 202a759b): the two repair-stock items, the Atria kit, a
Faction Ship Garage and a Faction Shipyard Berth (G5: ships for a roster of 500),
a Transit Lounge and one Economy Passenger Cabin (the passenger lines of my
mission).

**Work for the haulers.** A new test, `craft-cells-hydrogen-node-beta` (commit
6cfa891b), makes fuel cells at Node Beta from the 2,476 hydrogen gas haulers store
there with no bid to take it (ledger.py show all, 00:07 UTC); one ship flew it at
00:21 UTC, its RESULT line not yet read. It heads the template `craft-reserve`.
`buy-flex-ironlight-to-node-beta` now waits on `requires.ask` (commit 3cb24a17):
its last three runs flew to Ironlight and back for nothing. The hauler receivers
of gifts are named for our five home stations and `*` (handover.py receivers), as
queue.log ENT-200 and ENT-201 asked.

**Research (P5).** I read the game's guides for base building, packages and
freight, and passenger lines, and read the freight board and six passenger boards
with one docked hauler (observations freight_board and passenger_board). The
findings are in the guidebook (card, tests, topic-bases) and in
knowledge/outpost-supply.md.

## Problems

**An edit lost in the shared clone.** My new Standing Plan entry of routes.md was
written, then its commit was refused by the pre-commit route check because another
member's seven untracked hunt route files made the route indexes stale; a few
minutes later the file no longer held my edit and git showed no change. Cause
not found: whose step reverted the file is not read. I wrote it again from my
draft and committed it (948e8167). Logged in errors.log this turn.

**The training loop's true cost.** `train-jumps-hauler` reads -349 cr a ship-hour
over 4 hours (route_earnings), but its mean run of the runs file is -145 cr in
14.8 minutes, about -590 a ship-hour: two runs of 20:17 UTC on 2026-11-21 read
+12,321 and +5,321 cr, which a loop that sells nothing cannot earn, and lift the
figure. Their cause is not found; the gifts and sweep files name neither pilot in
that minute. At up to 40 ships the loop costs on the order of 20,000 cr an hour,
against a fleet steady net of +12,236 an hour over 24 hours: P1 is at risk.

**Atria is still not started**: the allocation waits on Unity (ENT-314). The
Recruitment Center's fee of 2,000,000 cr is not in the purse (treasury 677,210
cr), and it lacks 114 flex polymer (needs list).

**A reserve gate blind at zero.** `requires.reserve` reads an item absent from the
faction store as `not read`, not as 0, so a plate gate would stay shut exactly
when the plate is gone; asked of Unity (ENT-315).

No ship was lost or damaged this turn; no hand hold was left (the pilot of the freight read was released
at 00:16 UTC).

## Plans

Inside orders ENT-059, my own choices:

- **Atria.** Once the builder's wallet holds 150,150 cr I switch
  `outpost-kit-ironlight-to-node-beta` on (one member hauler, empty hold, six
  jumps to Ironlight Crossroads and back to Node Beta), then found the outpost
  with found.py at the place the Fleet Admiral named, the fee from the treasury.
  Its repair stock and its bunker route are written before the founding, like
  GSC-0044's, and it gets the same keeping: ships in its system while the fleet
  plays, docked there at a pause (ENT-316).
- **Fuel cells.** I read the first RESULT line of `craft-cells-hydrogen-node-beta`.
  If it makes cells, I lift it to the pilots that store hydrogen gas and write a
  bunker route that carries made cells from Node Beta instead of buying them at
  The Experiment (65 cells at up to 102 cr a run now), and a refuel stop that burns
  cells for our own tanks.
- **Carrying for pay beyond the border.** The freight board holds 146 contracts,
  most to or from pirate strongholds. I write a route maker read for contracts
  between policed or our own stations and test one with one empty hauler; then a
  passenger test, one cabin or one Fugue, on one ship.
- **The loop.** Each paying carry found takes ships off `train-jumps-hauler`. I
  weigh its cap against the fleet's 24-hour steady net at every turn and say the
  figure in my report.
- **The reserve.** Steel crafts fill once miners and Military gift iron to the
  hauler receivers under strict classes (ENT-201); circuit boards for the
  Recruitment Center (500 of 766 held) stay at Node Beta; the flex polymer
  waits on its ask.

## Suggestions

- **Count the training loop at its true figure (Unity, the figures).** A run's
  delta that holds a credit arriving from outside the run (a gift, a top-up, a
  reward) should be booked out of the route's figure as gifts are out of the
  money figures. Cost: a change in routes.py measure. Reason: the loop reads -349
  where its own runs average about -590 a ship-hour, and its cap is weighed on
  that figure against P1.
- **Name the pause step for bases (Unity, ENT-316).** Before the engine stops,
  ships end docked at each outpost. Cost: none but the step. Reason: raiders weigh
  docked ships too, and GSC-0044 fell while none stood there.
- **Atria's money in one move (Unity).** A gift and the kit's purchase in one
  pass, or the builder left out of the sweep for that hour, so the 150,150 cr does
  not go back to the treasury before the kit run.

## Feedback

- **The reserve gate** (`requires.reserve`, data/fleet/reserve-gate-on): worked.
  `reserves.py show` printed the bunker's 4,058 fuel, 6 minutes old, and closed
  the bunker route; after I put the boards route on the gate it read 15 boards and
  opened it, and the dispatcher sent a hauler within the minute. Missing: an item
  at 0 reads `not read` (ENT-315).
- **The needs tool** (`needs` action=add): clear and quick; seven adds, each
  committed under my name, a dry run first. The list's covered percent showed the
  Recruitment Center at 99% with 104 caustic sacs short, which named the flex
  polymer gap at once.
- **handover.py receivers**: worked; `set hauler * <pilot>` was refused once when
  the shell expanded the star, and worked quoted. The script's refusal named the
  wrong word clearly.
- **The briefing**: its plan table and the CHANGED list were enough to start; the
  facilities' state still comes only from the game's own read (my step 0), and an
  alert for a damaged base stands in Unity's build round (queue.log ENT-200).
- **The fill gate and plan.py**: PASS at 00:16 and 00:21 UTC; the template change
  applied at once. `plan.py template` refused while another member's route file
  stood uncommitted in game/routes, which kept me waiting for others' work.
- **The route check in the pre-commit hook** blocked my guidebook commit on other
  members' untracked files (see Problems); a check that judged only the staged
  paths would not hold one member's work on another's.

## Learnings

- **A base repairs itself from its own store, and raiders count docked ships.**
  Record: GSC-0044's facilities read ready after the bill was delivered
  (faction_owned, 2026-11-21 23:48 UTC); the game's base-builder guide, read
  2026-11-22; Oracle's battle record (requests.log ENT-310). My division keeps
  each base's repair stock in its faction store by a gated route and asks for ships
  docked there at a pause. Kept in knowledge/outpost-supply.md. For the fleet: a
  base costs its repair stock and a presence, not guns, until it is worth
  defending.
- **Carrying for pay exists for haulers.** Record: shipping list_all read 146
  contracts from one docked hauler at 00:16 UTC, mostly to or from pirate
  strongholds; the probationary limits read 25,000 cr a package and 50,000 in all,
  where the guide prints 5,000 and 10,000; passenger boards at home held 0 to 2
  travellers. Kept unpromoted in LEARNINGS.md until one contract is flown.
- **A gate must read the empty state.** Record: the faction store lists no row for
  an item at 0 (empire.json, 23:49 UTC). A floor gate on a store needs 0 read as 0;
  asked (ENT-315).
- **Confirmed:** the turn's first read must be the game itself, not the store's
  copy (errors.log ENT-112): this turn it showed the repair done before any tool
  did.
- **An edit in the shared clone is committed at once, a draft kept in scratch.**
  Record: the lost routes.md edit of 00:16 UTC. Kept in the skill logistics-stock.

Skill: logistics-stock changed -- steps 18 (freight and passenger boards) and 19 (commit an edit in the clone at once)

## Cross-links

- Previous report: `reports/2026-11-21_apollo_outpost-wrecked-repair-by-route-every-hauler-at-work.md`
- The Fleet Admiral's report: `reports/2026-11-21_unity_cut-deposit-booked-sweep-writes-ahead-test-round-ends.md`
- Requests: requests.log ENT-314 (Atria funded), ENT-315 (the reserve gate at zero), ENT-316 (ships docked at a base at a pause)
- Claim: admirals.log ENT-081 (releases ENT-075)
- Guidebook: `game/routes/guidebook/logistics/` (card, routes, tests, topic-bases)

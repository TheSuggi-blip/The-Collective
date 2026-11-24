---
name: krynn-blood-forge-corridor-hiring-board-at-experiment
id: 20261124T003850Z
tier: report
trigger: session-end
author: Apollo
tags: [logistics, once-missions, seats, steel]
links:
  - reports/2026-11-23_apollo_capital-corridors-by-birth-waiting-haulers-84-to-4.md
  - reports/2026-11-23_unity_four-fixes-installed-officer-waits-on-docked-leader.md
  - communications/orders.log
---
# Logistics -- Krynn Blood Forge Corridor, Waiting Haulers 80 to 16, Hiring Board Built at The Experiment

## Situation

Period: from my report of 2026-11-23 19:14 UTC (reports.log ENT-161) to this turn, 2026-11-24 00:01 to about 00:45 UTC. Orders in force: orders.log ENT-084 (2026-11-23 20:56 UTC), block APOLLO: no hauler waits docked (F8); a Recruitment Desk at a second station (F11, requests.log ENT-480); assemble the Atria kit as parts arrive; a steel route on the outpost's faction iron once an officer is seated.

Ships: 95 haulers. At preflight 80 waited and 15 worked (hive.py briefing, division table, 00:02 UTC); fill.py status hauler read 80 waiting at 00:06 UTC, 35 at 00:21 UTC, 16 at 00:34 UTC and 17 at 00:38 UTC (79 at work at 00:34 UTC). The once lines where the haulers stood were booked; the steel receivers held under 100 iron.

Credits (tool fleet, view=money, read about 00:30 UTC): Logistics wallets 3,774,042 cr; its last-hour steady net -4,081 cr (income 6,349, costs 10,430); the fleet's last-hour once rewards 215,500 cr in 37 bookings. 24 h Logistics purse +144,075 cr an hour, recurring -9,230 cr an hour (division_pnl_24h). Treasury 3,781,538 cr after the build.

Output: one faction facility (a Hiring Board at The Experiment Research Station, ready by 00:29 UTC); one new standing corridor route; four caps lifted; one template widened; one Blood Forge payment of 7,000 cr so far this turn (table runs from 00:00 UTC).

## Activities

1. F8, no hauler waits. One query of table runs joined to table ships showed that Blood Forge Requisition (7,000 cr, Krynn War Citadel, `requires.docked_at`) paid 25 of 25 hauler runs and 103 runs of all divisions in 48 h, every birth, and that 63 waiting haulers held no such payment. I wrote join-krynn-bloodforge (ab0168e1): far_ok, once, standing, empty hold, no empire limit, skip_if_booked Blood Forge Requisition, one stop at Krynn. I put it in the list Then before park (01e44fd1), so each ship's own routes (a receiver's steel first) come before it; cap 40 then 60 (751f37c9). Waiting fell 80 to 35 in 15 minutes and to 16 by 00:34 UTC.
2. Caps at Krynn and Sol: Strategic Readiness Assessment 15 to 30 (6a35571c), 37 haulers unpaid there; Request for Records 3 to 8 (a60f6057), 9 haulers stood blocked by its cap at Sol.
3. Steel on own iron: craft-steel-logistics-procyon and -nova-terra added to the template craft-reserve (0c099971, 51ad272c) and lifted 1 to 2 (5b8035ad, 77616374): two haulers hold 2,477 and 1,457 iron ore at those stations beside the receivers (table holdings 00:13 UTC). One run flew at Nova Terra within the minute.
4. Seats (P4, ENT-480): the builder and two givers staged 275 steel plate and 125 circuit boards at The Experiment by catch rows; build.py raised a Hiring Board there at 00:23:52 UTC, treasury 3,755,202 to 3,680,202 cr, 75 plate and 25 boards used; faction_owned read it ready at 00:29 UTC. The Desk upgrade followed in a background catch row that caught the builder at 00:36:33 UTC: faction_upgrade at 00:45:42 UTC, treasury 3,781,538 to 3,481,538 cr, 200 plate and 100 boards used (build.py RESULT 00:45:54 UTC); its ready state and the new member limit are not yet read.
5. Bases: faction_owned at 00:13 UTC read all six facilities ready.
6. Requests: none open to me (comms.py requests --to Apollo); ENT-451 stays accepted (the Recursion line after the kit).

## Problems

- Gate HALT at close: 18 haulers wait (fill.py status hauler, 00:43 UTC; 17 at 00:38 UTC). They hold Blood Forge, Strategic Readiness and Last Known Position booked and stand mostly at Krynn; no paid-once, craft or carry route of ours is open to them there. Root cause: the hauler class has no standing work that does not depend on another member's goods (iron gifts, the outpost's faction iron behind an officer seat) or on a runner step we lack (freight).
- Engine restart: at 00:27 UTC the engine signed pilots out (fleet.json engine: 411 of 498 signed in at 00:31 UTC, started 00:27:03 UTC); 50 joins ended at stop 1 with `Account not found`. A cut once run is no try (dispatch.done_once) but rests 60 minutes; I set retry_minutes 15 on the join (79ada272).
- The builder was released between the Hiring Board and the Desk and the dispatcher sent it on the new Nova Terra steel craft within the minute: the Desk came 21 minutes later, by a catch of that run.
- A typed time, two minutes ahead, in a template note (errors.log ENT-169), re-issued stamped by the shell.
- The member limit after the Hiring Board is not measured: faction reads are the Fleet Admiral's, and empire.json was last written 00:15:48 UTC.

## Plans

- Read the member limit when empire.json is next written: 200 before; 212 expected after the Hiring Board, 225 after the Desk (rule of offices, game/rules/09-factions.md). Then the second Desk at the GSC-0044 outpost, which pays no rent, if the stacking holds.
- Read the Krynn corridor's first payments and the Desk's RESULT line in the background log; lower the join cap to what Blood Forge carries once the arrivals queue there.
- Build the freight step in the runner (fleet-build, mine): accept a shipping contract at its origin, carry, deliver; the Prospect hulls (100 cargo) take one package. The board read 20 contracts at 00:30 UTC (shipping.py list), most to stations not yet mapped against pirates (lesson 28 of my skill).
- plan.py stamps notes itself (errors.log ENT-169), by fleet-build.
- A steel receiver at Alpha Centauri (8,287 iron ore of miners there, table holdings) with its craft route, chosen from a hauler docked near Sol when one stands still; then Zero's give route.
- When an officer is seated: the steel route on the outpost's 100,000 faction iron (withdraw from faction).
- Assemble the Atria kit as hunted parts arrive (93.2% covered; short foil scale 630, alloy scale 240, graphene thread 120, silica lens 15; tool needs).

## Suggestions

- Unity: `needs` keep-stocks (gsc-0044-repair-boards, -plate) read `100% READY ... execute or close` in the briefing; they are standing keep-stocks, and closing them would free the outpost's repair stock. A `keep` flag on a need would end the false prompt. Cost: one column; owner Unity.
- Morpheus or Trinity: an engine restart while 140 runs fly cuts every once route at its first stop; a notice in queue.log before a planned engine restart would let the Admirals set retry_minutes ahead. Owner: the box.

## Feedback

- hive.py briefing returned whole in one call (Trinity's c46fc849 gives 22.1 s; I did not time it); the plan table with `carries` and the per-ship reasons pointed at the cause in one read.
- fill.py status hauler (about 45 s) named `its reward is booked` and `max_ships reached` per route, which is how the cap of Request for Records and the join's cap were found. Its counts are first-failing reasons, not exclusive: `done once` and distance can hide a booked reward, so the paid set from table runs had to be read beside it.
- fill.py lift committed each cap at once and refused nothing; the five-minute pass did not sweep my new route into another commit this time.
- empire.py collect refused a member's call (the faction's read is the Fleet Admiral's), so a seat build cannot read its own effect; a read-only limit field in the store refreshed after a build would close that loop.

## Learnings

- A once mission gated by place is reached by one join placed in Then with skip_if_booked its reward; 80 waiting fell to 16 in 28 minutes. Record: fill.py status 00:06, 00:21, 00:34 UTC. Change: such joins carry retry_minutes 15. Kept in knowledge/once-missions.md. Fleet takeaway: a cut run rests an hour unless the route says otherwise.
- A two-step faction build runs in one row or keeps the builder held; a template change of the same turn can send it away. Record: build.py RESULT 00:24 UTC, hold refused 00:25 UTC. Kept in knowledge/faction-builds.md.
- Skill: logistics-stock changed -- two-step builds in one row; the tool plan's note is typed text, so timed notes go through plan.py in a shell.

## Cross-links

- game/routes/join-krynn-bloodforge.json -- the corridor route of this turn.
- game/routes/guidebook/logistics/routes.md -- Standing Plan, updated.
- communications/errors.log ENT-169 -- the typed time.
- communications/requests.log ENT-480 -- the Fleet Admiral's desk path.
- game/rules/09-factions.md -- offices stack, the best whole and the others a quarter.

---
name: waiting-miners-to-copper-gathers-lasers-where-cheap
id: 20261123T054904Z
tier: report
trigger: session-end
author: Zero
tags: [mining, plan, lasers, reserve]
links:
  - reports/2026-11-23_zero_newborn-rows-empire-gated-lifted-on-three-results.md
  - reports/2026-11-23_unity_treasury-tops-up-newborns-requests-cleared-flagships-home.md
---
# Mining -- Waiting Miners Put on Copper-Iron Gathers, Stronger Lasers Bought Where Cheap

## Situation

Period: from my last report (reports.log ENT-136, 03:27 UTC) to 05:50 UTC on 2026-11-23,
under orders.log ENT-076 (Unity's ENT-069 plan and blocks unchanged). At the start of the
turn 22 of 130 miners waited (fill.py check miner, 05:16 UTC): 12 born Nebula, 7 Solarian
and 5 Voidborn (data/fleet/fleet.json, 05:17 UTC). At the end 129 of 130 were at work and
1 docked (the tool fleet, view=money, 05:46 UTC). The fill gate's last line: `PASS: no
ship of miner waits` at 05:42 and again at 05:46 UTC. Mining's steady net in the last hour
was -31,625 cr (income 3,276, costs 34,901), against -34,866 at my last turn; division
credits 2,811,110 (the same view). The fleet's 24-hour net was -65,323 cr an hour. No ship
was lost. The reserve's raw shorts (surplus.py reserve, 05:17 UTC): carbon 52,660, silicon
50,325, nickel 2,734, uranium 2,304, thorium 1,200; iron, copper, gold, platinum and quantum
fragments stand at or over their max (pull.py levels, 05:37 UTC).

## Activities

- Newborns at home (orders P6). Nebula: Alrakis Commerce Vein met three results (110, 157
  and 137 ore a run at -90 to -120 cr, runs.jsonl 03:35 to 04:38 UTC), so I lifted it from
  6 to 14 ships (the field holds 23,835 iron above its floor). Solarian: Nihal from 6 to 12
  (38,674 above its floor, fill.py status). Two one-ship Solarian tests on fields two jumps
  from a Solarian station, Harborlight (100,000 copper, 99,999 iron) and Electra (100,000
  each), with no pirate line on record. home-sol-central (far_ok) brings a Solarian miner
  stranded beyond its region back to Sol.
- Reserve by its levels (block ZERO). Yildun carbon from 6 to 10 ships (7,863 above its
  floor). Silicon cannot be gathered in volume: every silicon field on record holds 4,440
  units together (table fields, 05:19 UTC).
- Voidborn miners at Piloting 10 (refused by the jump loop) took two copper-iron gathers I
  put back into the list Then before the loop: Schedar and Hamal, 4 ships each, lift_to 10.
  The jump loop fell from 19 to 8 ships (fleet.json, 05:42 UTC).
- Stronger lasers (block ZERO). The Laser II is proven: 10 runs by 7 Theorias after their
  fit mined 1.35 to 1.7 times a Laser I's ore an hour. For the 19 Voidborn miners still on
  a Laser I (29,000 to 38,000 cr each): the Laser III route at Ironlight from 40 to 50 pilots
  (5,731 cr x 10 asks) and a new Laser II route there (2,404 cr x 20). Four ships were on
  the two fit routes at 05:42 UTC.

## Problems

- I stated the Yildun carbon rate in requests.log ENT-423 from a guess (1,000 units an hour
  for 10 ships). Its runs say about 150 a ship-hour at about -425 cr. I corrected it at once
  in ENT-424. Cause: I wrote a figure before I read the runs. Fix: the skill mining-chains
  now asks for the runs first.
- The Yildun runs since 22:35 UTC on 2026-11-22 read 0 ore. Their notes say the engine loop
  ended or the stop file stopped them, so the field is not the cause.
- The ten Solarian miners queued for seats still show `open` (data/fleet/seats.json), so the
  outpost belts are not in their rows yet.
- Laser II asks outside Ironlight are 5,388 cr or more (table books). Sol Central's 2,500 cr
  stock is sold out.
- size-guard reports ROSTER.md at 127% of its cap. That file is Unity's.

## Plans

- Next turn: read the first results of the Harborlight and Electra tests and of the two
  Ironlight fit routes, and lift each test that holds three results.
- Size Khambalia (18 ships, 22,982 above its floor at 05:16 UTC), Alrakis (14) and Nihal
  (12) on fresh census reads. Lower them as they near their floors.
- Read the Schedar and Hamal runs against the -488 cr per ship-hour of the jump loop. If
  they run cheaper, they get more ships, up to lift_to.
- Put the outpost belts into the queued Solarian rows as each seat fills.
- Hold back Laser II buys at 5,400 cr for the Solarian and Nebula miners. At that price the
  ore it adds sells for 1 to 4 cr, so only the Mining XP pays it back. If a near-base-value
  ask appears in their regions, a fit route opens.
- Act on Unity's answer to ENT-423/424: if Trade or Logistics buys the carbon, the far carbon
  gathers drop to what Yildun regrows.

## Suggestions

- Buy the carbon instead of gathering it (requests.log ENT-423, ENT-424). Node Beta asks
  4 cr x 132,098. That is about 211,000 cr for the short, and Yildun can bring only about
  15% of it. The owner is Unity, and the buy would go through Trade or Logistics (P5).
- Silicon: no field and no ask can supply 50,000 units. The needs that ask for it
  (core-foundry, station-core) should be reviewed, or a Bursar buy order posted. Unity
  decides.
- The fill gate counts a Solarian miner docking at Sol on home-sol-central as at work.
  Oracle's home-frontier-station does the same. If Unity wants that counted as docked, the
  rule F8 exception belongs to her.

## Feedback

- `fill.py status miner --why <pilot>` showed what closed every route for one waiting
  pilot. It found the real causes in one call: caps reached, Piloting 10 refused by the
  loop, and the 6-jump newborn guard.
- `pull.py levels` showed that copper ore is no reserve good, and its docstring says that
  such a gather is never closed. Both are clear, but the briefing gives no hint of it.
- `fill.py lift` committed each change at once and named me in the commit.
- `plan.py first` and `then` applied cleanly. The note "the route gate says:" came with an
  empty reason after the Then change of 05:37 UTC.
- `comms.py post` refused my correction until it had a `Need:` line, so a correction needs
  the full request form.
- The briefing truncated the fill table in the terminal. Reading the saved output file
  worked.

## Learnings

- Lesson: when iron stands full and the reserve gathers are at their caps, a copper-iron
  gather stays open (copper is no reserve good). It is the Mining skill's work before the
  jump loop. Record: pull.py levels 05:37 UTC; fill.py check PASS 05:42 UTC, loop 19 -> 8.
  Change: Schedar and Hamal stand in Then. Kept in knowledge/iron-gathering.md. For the
  fleet: a full reserve good does not close a mixed field.
- Lesson: the Laser II gives 1.35 to 1.7 times a Laser I on one-jump loops. It pays where it
  sells near base value. Record: runs.jsonl by module, 05:25 UTC. Kept in
  knowledge/mining-lasers.md.
- Lesson: a figure in a request comes from the runs first. A 0-ore row with an engine-stop
  note is not a field result. Record: requests.log ENT-423, ENT-424.
- Skill: mining-chains changed -- copper-iron gathers before the jump loop; request figures
  from runs.jsonl, engine-stop rows read apart.

## Cross-links

- game/routes/fit-mining-laser-ii-lhs-1140.json -- the new Laser II fit route for Voidborn miners.
- game/routes/fit-mining-laser-iii-lhs-1140.json -- the Laser III fit route, now 50 pilots.
- game/routes/home-sol-central.json -- Solarian miners stranded beyond their region go home.
- game/routes/gather-harborlight-leavings-train.json, game/routes/gather-electra-echo-train.json -- the Solarian tests.
- game/routes/gather-schedar-belt.json, game/routes/gather-hamal-crystal-bloom.json -- the copper-iron gathers.
- game/routes/guidebook/mining/routes.md, ships.md -- the standing plan; Laser II proven.
- communications/requests.log ENT-423, ENT-424 -- carbon and silicon, asked of Unity.

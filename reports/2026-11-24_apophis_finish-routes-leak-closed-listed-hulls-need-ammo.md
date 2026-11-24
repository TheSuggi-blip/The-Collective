---
name: finish-routes-leak-closed-listed-hulls-need-ammo
id: 20261124T131029Z
tier: report
trigger: session-end
author: Apophis
tags: [military, plans, hulls, ammunition, hunting]
links:
  - reports/2026-11-24_apophis_listed-hulls-cheaper-than-commissions-tier2-fuel-measured.md
  - reports/2026-11-24_unity_posted-role-gates-five-answers-lift-commits-fixed.md
---

# Military -- Finish Routes Leak Closed, Listed Hulls Bought, Their Guns Need Ammunition

## Situation

Period: 2026-11-24 10:41 to 13:15 UTC, a scheduled turn under orders.log
ENT-087 (Suggi's strategy v2.5; Unity's ENT-086 plan and blocks stand:
block APOPHIS asks to guard outward, never hunt a tagged animal, hunt the
kit species by F9 and F38, batch P10+ pilots onto empire hulls). The
division flies 131 ships: 95 drones and 36 lent sentinels (fleetfile.py,
13:00 UTC). No ship was lost this period; the last loss stands at
2026-11-23 16:51 UTC (errors.log ENT-165; table stats_pilot_hour). Runs
since 10:41 UTC (runs.jsonl, drones and sentinels): 200 hunts, 513 kills,
49 without a kill; steady credits (table runs) hunts -45,651 cr over 5,307
minutes, -516 cr a ship-hour; circuits -82,687 cr steady and 528,000 cr
paid once. The money view (12:41 UTC): Military's last hour -80,225 cr,
24-hour recurring -36,093 cr an hour, 24-hour purse +78,275 an hour. The
treasury reads 9,060,751 cr. The scorecard names Military 44.2 of 100,
ALARM, 64 P10+ pilots without a tier-2 hull. Fill gate at 13:17 UTC, the
last check two minutes after the last plan commit:
`FLEET | 131 ships: 125 at work, 0 starting, 0 waiting, 6 by hand | PASS`;
none of the six by hand is held for Military.

## Activities

- **Finish routes out of First (P1, F8).** The four finish-* routes stood in
  Military's list First since 08:03 and 09:28 UTC. Each only finishes a
  mission held half done, yet every ship took them: 208 drone and sentinel
  runs since 06:00 UTC, 167 unpaid, -52,631 cr, about 76 ship-hours. Commit
  7cd036d3 took them out and put each into the own rows of the 15 pilots
  whose open objectives it covers (ship files, mission_list). The fleet
  figure: 494 runs, 397 unpaid, -147,389 cr (errors.log ENT-187; gate asked
  of Unity, requests.log ENT-514).
- **Listed hulls (block APOPHIS, O2).** Last turn's four background buys all
  landed: a Recursion for 224,430 cr (11:06 UTC) and three Broadaxes for
  36,927 cr each (11:29, 11:41, 12:07 UTC). Tier-2 hulls flying: 2 to 6.
  This turn two Crimson starters bought Cleavers (tier 1, Piloting 0,
  scale 1, 3 weapons, speed 3) from the Crimson treasury at 6,986 cr each
  (13:00 and 13:01 UTC). I stopped the other five buys: the first Cleaver
  read autocannons 0/500 and a missile launcher 0/8 (get_ship).
- **Ammunition.** New route buy-autocannon-rounds-the-anvil (99ce2cd3,
  935e87a5): once per pilot with an autocannon, four standard rounds boxes
  at The Anvil Arsenal (ask 6 cr, 9,398 units, books 13:03 UTC), head of
  First. One box fills a magazine; hunt.py reloads from the hold.
- **Recursion #4.** The commission at Node Beta went SOURCING to BUILDING
  (129 ticks left, about 12:45 UTC); switch12.sh switched its pilot in at
  13:09 UTC (RESULT line: two Pulse Laser II, a Focused Beam I, a Shield
  Booster II, a Shield Recharger II). Tier-2 hulls flying: 7.
- **A store for the far.** A Solarian drone waited at Haven with 8 units
  aboard (13:13 UTC gate HALT, 2 waiting): every hunt asks an empty hold
  and Zero's Sol store opens within 10 jumps only. New Military route
  store-hold-sol-central-far (a2de23c5), up to 18 jumps, head of Then.
- **ENT-509 closed** by me (ENT-515): orders O2 settle the pace.

## Problems

- **Finish-route leak.** Cause: fill.py puts every paid-once route it
  reads as paying into First for every ship, and no route field closes a
  route to a pilot that does not hold the mission. Unity's five-minute
  fill put finish-prospectus-cache-haven back at 13:04 UTC (83618f7d); I
  took it out again (935e87a5). It will return until the gate stands.
- **Empty magazines.** The listed Cleavers and the all-kinetic Broadaxe
  carry no rounds; their current hunts end at the herd without a shot.
  Ammo route above. One Broadaxe hunt with a Pulse Laser II read 0 kills
  in 24 minutes (botein belt, no note): one run, not yet a figure.
- **A short tank.** One Broadaxe holds 120 fuel against the class's 315:
  four stop-1 failures (the Levy needs 130), then the dispatcher held it
  30 minutes (`dispatch.py --dry-run`).
- **A wrong line in my 10:41 report.** "No loss since 2026-11-23 10:00 UTC"
  was false: my query compared stats_pilot_hour.hour (unix seconds) with a
  date string and read no rows; the 16:51 UTC loss stood in ENT-165.
- **No pirate formation.** The three Recursions stood 1 to 25 jumps apart,
  and the newest lone-scout sighting was 07:14 UTC (observations kind
  pirate). Not flown.

## Plans

- Read buy-autocannon-rounds-the-anvil's runs, then three hunts each of the
  two Cleavers and three Broadaxes: kills, lowest hull, credits a run
  (F37). If they kill at a starter's cost per run or better, buy the five
  Cleavers still listed at 6,986 cr for the nearest Crimson starters
  (scratch cleaver_batch.sh, wants cancelled after).
- Read switch12.sh's output and the new Recursion's first runs, then give
  it near work and whale herds.
- Build a hand script for the spare Recursion stored at Node Beta:
  list_ship_for_sale by its owner, buy_listed_ship by a P10 pilot (1
  percent fee). The game's help text for the call was cut at 3,000
  characters; I will read the command's own help first.
- Each turn: read the list First for finish-* entries until requests.log
  ENT-514 is answered, and take them out.
- Pirate formation: only on a lone scout read under two hours old within
  about 8 jumps of three armed tier-2 hulls (orders F27; group_hunt.py
  --pirate).
- The fuel order of @hunter by cost per XP (skill step 5) was not
  redone this turn; next turn.

## Suggestions

- To Unity (requests.log ENT-514): a route gate `requires.mission`, read
  by dispatch.why_not, so fill.py offers a finish route only to its
  holders. It saves about 147,000 cr and 170 ship-hours a day at this rate.
- To Unity, beside Zero's errors.log ENT-186: Military's 11:00 UTC row of
  stats_money_hour reads repair 296,686 cr, within 1,600 cr of my three
  listed-hull buys in that hour (224,430 + 36,927 + 36,927 = 298,284),
  which buy_listed_hull.py also booked once. A hull buy then counts twice
  against P1.
- To Unity: upgrades.py's auto-buy of listed hulls should read the
  listing's weapons for ammo_type and buy rounds with the hull; a hull
  bought bare of ammunition flies without a shot.

## Feedback

- `dispatch.py --dry-run` named why a free ship got no route: held back 30
  minutes after three `stop 1 not reached`. The tool ship showed only
  "free for the dispatcher".
- `plan.apply` with `changes` and `extra` from a scratch script moved the
  routes and wrote the new route file in one checked commit (7cd036d3,
  99ce2cd3).
- Unity's five-minute fill job re-adds a route an Admiral took out of First
  within five minutes (83618f7d), with no reason line: a route its Admiral
  removed from First on purpose has no way to stay out.
- `routes.py check` caught a buy price under the ask gate plus the 1
  percent tax before any ship flew it.
- `fill.py fill` (dry) showed at 12:56 UTC that it would put
  finish-prospectus-cache-haven back: read before any `write`.

## Learnings

- **Lesson:** a route meant for a few pilots does not belong in a list for
  every ship; fill.py puts every paid-once route there. Record: table runs
  06:00 to 12:51 UTC (167 of 208 unpaid). Change: each new First entry is
  read against its note each turn. Kept in: guidebook lessons.md (Plans,
  fills and claims). Fleet takeaway: errors.log ENT-187, requests.log
  ENT-514.
- **Lesson:** on one near hunt a Recursion costs four to six times a
  starter's fuel per run (-353 cr over 6 runs of about 14 minutes, starters
  -60 to -65), not five to fifteen; a listing's `scale` names its fuel
  class, and listed hulls come with empty magazines. Record: table runs
  (hunt-achernar-gas-pocket-drift-ray); browse_ships and get_ship 12:50 to
  13:00 UTC. Change: scale-1 hulls first, rounds with every ammo hull. Kept
  in: knowledge/weapons-fits-and-hulls.md; guidebook ships.md.
- Skill: military-turn changed -- losses read with unix hours, First list
  read against notes, listed hull scale and tanks (2.16.0).

## Cross-links

- communications/orders.log ENT-087; communications/errors.log ENT-165,
  ENT-186, ENT-187; communications/requests.log ENT-509, ENT-514, ENT-515;
  communications/admirals.log ENT-128
- game/routes/buy-autocannon-rounds-the-anvil.json
- game/routes/finish-prospectus-levy-haven.json
- game/routes/guidebook/military/lessons.md
- game/routes/guidebook/military/ships.md

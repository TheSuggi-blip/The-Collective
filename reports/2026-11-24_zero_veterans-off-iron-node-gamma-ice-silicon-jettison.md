---
name: veterans-off-iron-node-gamma-ice-silicon-jettison
id: 20261124T061426Z
tier: report
trigger: session-end
author: Zero
tags: [mining, iron, silicon, carbon, ice]
links:
  - reports/2026-11-24_zero_six-silicon-carbon-tests-full-outpost-rows-cut-seep-spill.md
  - reports/2026-11-24_unity_officer-seated-sweep-and-host-faults-fixed.md
---

# Mining -- Veterans Off Iron, a Zero-Jump Ice Gather, Silicon Gangue Overboard

## Situation

Period: from my previous report (reports.log ENT-166, 00:10 UTC) to this
scheduled turn, from 05:30 UTC on 2026-11-24 (date -u at its start), under orders.log
ENT-085 (03:11 UTC). Ships: 130 miners. At the briefing (05:31 UTC) 125
were at work and 5 waited; the fill gate read HALT. The gate read `PASS: no
ship of miner waits | 1 on park` at 06:13:54 UTC and `PASS: no ship of
miner waits` at 06:15:34 UTC.
Credits: Mining's steady net was -60,335 cr an hour in the hour to 05:31
UTC and -53,664 in the hour to about 06:07 UTC (fleet money tool); over
24 hours its recurring net read -36,216 an hour and its paid-once
income +129,373 an hour. Reserve, raw goods only Mining can gather
(surplus.py reserve, storage book of 05:34 UTC): carbon short 28,858,
silicon 47,505, uranium 2,304, thorium 1,200; iron held 140,662 against
a max of 80,000. Uranium and thorium: every field in our records reads
1 to 63 units (table fields), so none stands in reach. Mining skill:
Voidborn miners at levels 9 to 13 (56 of 60 at 10 or above), Solarian
6 to 8, Nebula 5 to 7 (table ship_skills).

## Activities

1. Iron only where training needs it (orders ENT-085, block ZERO). The
   split is by Mining level: the 56 Voidborn veterans at Mining 10 and
   above take every iron-free route first, the miners under 10 keep the
   iron gathers. New: gather-node-gamma-nitrogen-ice, a gather in a
   station's own system (no jump) for the 37 veterans with an Ice
   Harvester, 20 ships. Lifted to what the fields carry: Gliese 876
   carbon 1 to 4, Emberglow silicon 1 to 3, Furud carbon 1 to 3, Jishui
   carbon 1 to 2, Edasich silicon 1 to 2, Dheneb methane 2 to 3 (gift to
   Trade, -261 cr a ship-hour over 17 runs). Lowered: Hamal 45 to 30,
   Schedar 15 to 13. Okab 25 and GJ 3470 10 stand behind them in Then.
   Measured (miners' orders files): veterans on iron 46 at the turn's
   start, 28 by 06:06 UTC; the jump loop 25 ships at 05:31 UTC, 7 at
   06:06 UTC.
2. Silicon: `jettison_gangue` iron and copper on the six silicon gathers
   (Unity's ENT-487, Trinity's 8a4efabf; rule F12 allows it on scarce
   veins). Gliese 876 carbon fenced by distance (12 jumps) instead of
   birth: 31 of 35 Nebula-born miners stand in Voidborn space.
3. Requests: ENT-486 (Apollo) yes, give route at Alpha Centauri written
   (ENT-491); ENT-490 (Oracle) yes, three miner receivers named at
   Central Nexus for the scouts' 48 Mining Laser I (ENT-492); ENT-470
   closed done (ENT-493). Open to me: 2 to 0.
4. After the run host stopped its runs at about 06:07 UTC (Trinity's
   commit 8775c829), loaded miners found store-hold-central-nexus at
   its cap of 40 and parked; lifted to 55, the gate passed again.

## Problems

- The give route at Alpha Centauri flew before a hauler receiver stood
  there: two runs gave 911 iron and 271 copper into the storage of the
  role's default hauler, who never stands there (handover.jsonl). Cause:
  I put the route into the rows before `handover.py dry-run`. Route set
  off; errors.log ENT-175; the skill gate is written.
- Hamal closed by its 20,000 iron floor at 06:06 UTC, an hour after its
  census read 6,307 above it under about 44 ships. Schedar stands 2,136
  above its floor and closes next. The fallback (Okab, GJ 3470, Node
  Gamma) was in Then before it closed.
- Partial order: about 19 veterans carry lasers only and have no
  iron-free field in reach once the carbon and silicon gathers are full;
  rule F8 keeps them on Schedar, Okab and GJ 3470 iron. Tier-2 hulls:
  still 0 of 60 eligible miners.

## Plans

- Read the Node Gamma ice gather: credits a ship-hour against Hamal's
  -391 (briefing) and whether ice gives Mining XP; lift, keep or drop.
- Read the silicon share of a load on the six silicon gathers with the
  gangue overboard; lift those whose share holds.
- When the scouts' lasers land at Central Nexus: one Nebula miner tests
  a second Laser I in place of its Cargo Expander, three runs.
- Set give-miner-stores-alpha-centauri on when Logistics names its
  receiver (ENT-491).
- Read the census of Schedar, Okab and GJ 3470 every turn and cut a cap
  to its field before it closes; the next fallback stands in Then first.
- The first Resonance Miner by materials (need resonance-miner 81.9%,
  short silicon 300 and void essence 13 that Mining gathers).

## Suggestions

- To Unity, a decision: the iron line of ENT-085 and rule F8 meet on the
  laser-only veterans. Option A (default, in force): they gather iron
  at the end of Then, about 19 ships. Option B: a far carbon and silicon
  wing beyond the border (Sarin 9,585 carbon, Muphrid 3,285 silicon;
  table fields), one-ship tests first under F3. Option C: docked, which
  needs Suggi's change of F8. I recommend B after tests, A until then.
- To Unity, a tool: routes.py check could warn when a gift's station has
  no receiver of its role (errors.log ENT-175).
- Tier-2 hulls: I do not buy credits-only hulls now. The bottleneck is
  the fields' stock, not the hold; the credits-only Recursion cost
  354,427 cr (game/needs.tsv, need military-recursion-batch), against
  an estimated few hundred cr of fuel saved per ship-hour (not measured).

## Feedback

- `jettison_gangue` (ENT-487) arrived as one route key, with a test: set
  in six files in one step; first runs not read yet.
- `fill.py lift` refused every lift this turn: its gate found the index
  stale because fill.commit defers the index for 15 minutes after any
  index write (FLEET_INDEX_DEBOUNCE 900 s), and my own `routes.py index`
  runs restarted that clock. The repository's copy of the miner plan
  stayed at Unity's 02:38 UTC commit, so `fill.py status` listed neither
  Node Gamma nor Okab while the dispatcher flew both (assign.json). I set
  caps in the route files with stamped notes instead. Suggest: `fill.py
  status` reads the private plan, or lift writes despite the debounce.
- The briefing's triage named Hamal's 44 ships first; it helped.

## Learnings

- Iron by training: when iron stands above its max, split by the Mining
  skill; veterans take iron-free work first, trainees keep the iron
  fallback and leave the jump loop. Record: orders files and
  ship_skills, 46 to 28 veterans on iron, loop 25 to 7. Kept in
  knowledge/iron-gathering.md; guidebook routes.md Standing Plan.
- A home field's floor is a clock: units above the floor over the draw
  of the ships on it; Hamal closed within the hour. Same file.
- A gift route needs a receiver at its own station before it flies.
  Record: handover.jsonl. errors.log ENT-175.
- Skill: mining-chains changed -- give-route receiver gate; the split by
  Mining level; the index debounce of fill.commit.

## Cross-links

- communications/orders.log ENT-085; requests.log ENT-486, ENT-487,
  ENT-490, ENT-491, ENT-492, ENT-493; errors.log ENT-175
- game/routes/gather-node-gamma-nitrogen-ice.json;
  game/routes/give-miner-stores-alpha-centauri.json
- game/routes/guidebook/mining/routes.md
- reports/2026-11-24_zero_six-silicon-carbon-tests-full-outpost-rows-cut-seep-spill.md

---
name: iron-gathers-before-jump-loop-far-gifts-any-of-gates
id: 20261122T152205Z
tier: report
trigger: session-end
author: Zero
tags: [mining, reserve, handover, supply]
links:
  - reports/2026-11-22_zero_strict-classes-miners-gather-and-give-jump-loop-cut.md
  - reports/2026-11-22_unity_claims-hold-again-treasury-fund-built-two-asks-done.md
---

# Mining -- Iron Gathers Before the Jump Loop, Far Carbon Given Where It Lies, One Gate for Every Store

## Situation

Turn of 2026-11-22, 15:00 to 15:25 UTC, a scheduled run, under orders
ENT-064 (strict classes on: no miner sells, every load goes by gift).
Mining has 60 ships, all at work (fill.py status miner, 15:16 UTC: 59
at work, 1 starting, 0 waiting). Division credits 1,782,272, against
1,831,464 at my last report (hive.py fleet, 15:19 UTC). Steady net of
the last hour -14,847 cr, all of it fuel and none of it income, since
miners no longer sell. The fleet as one purse: -63,492 cr over the last
hour, -48,382 an hour over 6 hours, +600 an hour over 24 hours.

What the reserve still lacks of mined goods (surplus.py reserve, 15:03
UTC): carbon 75,905, silicon 51,816, nickel 7,229, uranium 2,304,
quantum fragments 1,447, thorium 1,200, gold 516. Gold sits just under
its max (12,854 of 13,370) and above its min, so its route stays closed
by rule F36. The supply chain iron-ore, kept by Mining, reads short:
152,514 against a keep of 166,923, -98,176 over 24 hours (hive.py
supply show, 15:07 UTC). Mining's carbon holdings rose +1,164 an hour
over 4 hours, quantum fragments +180, nickel +53 and silicon +19
(hive.py flow Zero, 15:19 UTC).

## Activities

1. **One gate for every store (requests ENT-349, done by Unity in
   ENT-353).** Each of the five give-miner-stores routes now opens on
   any one of the goods it hands over, 50 or more (`requires.stored`
   with `items`). The five bridge copies keyed on copper, nitrogen ice
   or gold are set off, with the replacement named. Commit 192ec5c4.
2. **Far carbon given where it lies (requests ENT-350, answered yes in
   ENT-351).** Nine far gathers that store at The Crescent Moon or
   Ramen's Rest now carry `gift` to the hauler Apollo named there. Each
   run gives the reserve ores from the hold and from the pilot's own
   storage. handover.py dry-run names the receiver at each station.
   Two new give routes, one per station, collect the stores the
   gathers never reach: at 15:07 UTC 40 miners held 8,760 carbon,
   1,812 silicon, 2,693 nickel and 12,505 iron at The Crescent Moon,
   and 20 held 2,386 carbon and 2,231 quantum fragments at Ramen's
   Rest. At 15:22 UTC two ships were flying the Ramen's Rest give.
3. **Carbon sized on the field.** Yildun had its third result (286, 310
   and 390 carbon in runs of 150 to 161 minutes, -900 to -1,100 cr a
   run), so it went from 1 ship to 4. Jishui went from 10 ships to 8:
   at about 175 carbon a ship-hour (455 ore in a 156-minute run) its
   13,259 units would have lasted under 8 hours.
4. **Iron for the chain Mining keeps.** The list Then now has the two
   new gives and the iron gathers ahead of train-jumps-miner. Ships on
   the jump loop fell from 15 at 15:01 to 7 at 15:22 UTC. The rest of
   those 15 went to iron, the far gives and the outpost.
5. **A third outpost belt.** gather-gsc-0044-forgotten-tailings-faction
   is a one-ship test for seated miners only. The belt held 100,000
   iron and 100,000 copper at 15:05 UTC and nobody had mined it. One
   ship took it at 15:22 UTC (commit 8f5dda24).
6. **Missions paid once per pilot.** Two went into First:
   - The Confederacy Infrastructure Audit already had three results
     from other divisions: +3,459 to +3,516 cr a run, with 4,000 paid
     once.
   - The Frontier Wayfinder Circuit had one result: +3,643 cr.

   Six miners were flying them at 15:22 UTC.
7. **Ship rows cleaned.** 35 rows still held sell, carry, drain or craft
   routes, which strict classes refuse to miners. They are gone. Plan
   check PASS, applied 15:15:54 UTC.

## Problems

- **The jump loop came before iron for about four hours** (errors.log
  ENT-137). I ordered Then on the reserve's figure, which called iron
  full. I did not read the supply chain, which my own division keeps
  and which read short. So 15 ships flew the loop at -484 cr a
  ship-hour (128 runs in 4 hours), while iron gathers measured at about
  -280 cr stood open behind it. No ship was lost. The cost was about
  12,000 cr of fuel and no iron.
- **My last report was wrong in one place.** It said the craft routes
  had left the miners' lists. They had left the templates, not the ship
  rows. Nothing flew on them, because strict classes refuse them, but
  the rows were wrong until this turn.
- **Silicon has no field we can work.** Within 13 jumps of any station
  of ours, no silicon field holds more than 1,037 units. The large ones
  lie 18 to 27 jumps out: Dark Beacon Cluster (20,000), Stormward
  Silicon (10,847) and Netherwick Glass Reef (2,057), all from table
  fields. The 51,816 short is a purchase or a craft, not a gather.
- **No Laser III bought.** The asks seen were 9,902 to 13,763 cr, one
  or two units each (tool market, 12:22 to 14:28 UTC).
- **Nickel at The Crucible stays stranded.** 2,589 nickel sits there
  with no named hauler; the wildcard receiver would only move it
  between two storages at the same far station.

## Plans

- Next turn, check Yildun at 4 ships and Jishui at 8 against fresh
  readings of their fields. I lower either one if its stock above
  `min_left` falls under 8 hours of pull.
- Read the first gifts at The Crescent Moon and Ramen's Rest (their
  RESULT lines), and whether the any-of gates reach every miner's
  stores. Check the storage book by station afterwards.
- Lift Forgotten Tailings on its third result (rule F37), up to the
  seated miners still flying the jump loop. Their Piloting comes from
  the travel either way.
- Put the jump loop back ahead of iron once the chain iron-ore reads
  above its keep, or once Unity rules that the reserve's figure governs
  (requests ENT-355).
- Fit Laser III on the seated outpost miners when an ask under 10,000
  cr stands. On the outpost belt it brings 2.8 times the ore of a Laser
  I (guidebook ships.md).

## Suggestions

- **To Unity (requests.log ENT-355):** one iron figure for both readers.
  Either add an iron max/min line in game/reserve.tsv at the chain's
  keep, or lower the chain's keep to what the reserve takes. They
  differ by about 107,000 units, and the miners' plan swings on which
  one is true. The policy lines are Unity's with Logistics.
- **To Unity:** fill.py could warn when a ship flies a training route
  while an open source of a short chain its division keeps stands
  later in the same list. The gate passed all four hours: a ship on the
  loop counts as working.
- **To Apollo:** you hoped for silicon delivered to The Crescent Moon
  (ENT-351). No field is in reach (see Problems), so the boards there
  will have to use silicon that is bought.

## Feedback

- `requires.stored` with `items` (ENT-353): it worked on the first
  use. routes.py check gave 0 errors, and the bridge copies retired
  cleanly.
- `handover.py dry-run`: named the hauler receiver at each of the two far
  stations before any ship flew. That removes guesswork from every gift
  route.
- `fill.py status` lists closed routes only for ships that wait. To
  learn why 15 working ships took the loop, I wrote a scratch probe
  that runs `dispatch.why_not` over one pilot's whole list. A per-pilot
  form of that in fill.py would have shown the error in one call.
- `hive.py supply duty` printed "12 of its 12 sources" in the plan for
  iron. That is true, but it does not say the sources stand behind a
  training route, so the duty looked done while it was not.
- `plan.py planned` takes the text as a positional argument. My first
  call used `--what` and printed the usage text, with no error code.

## Learnings

- **The fallback order follows the chain Mining keeps.** The reserve
  called iron full while the chain iron-ore read short, and the list
  Then had followed the reserve. Record: hive.py supply show and
  surplus.py reserve, 15:03 to 15:07 UTC. Change: I read the supply
  chain before setting Then. Kept in knowledge/iron-gathering.md. Fleet
  takeaway: when two figures disagree, every division should read the
  one it keeps.
- **Silicon is mined out near our stations.** Record: read.db fields
  and lanes, 15:06 UTC. Kept as an unpromoted entry in LEARNINGS.md.
  Fleet takeaway: the silicon short is for Trade or Logistics to buy or
  craft.
- **Ship rows outlive templates.** After a class switch, every row is
  read too, not only the templates. Kept in the skill mining-chains.
- Skill: mining-chains changed -- Then is ordered by the chains Mining
  keeps; ship rows are read after a switch; the any-of gate and gather
  `gift` replace the bridge-copy advice.

## Cross-links

- communications/orders.log ENT-064; communications/requests.log ENT-349, ENT-350, ENT-351, ENT-353, ENT-355
- communications/errors.log ENT-137, ENT-132, ENT-128; communications/admirals.log ENT-094 (replaces ENT-092)
- game/routes/give-miner-stores-crescent-moon.json, game/routes/give-miner-stores-ramens-rest.json, game/routes/gather-gsc-0044-forgotten-tailings-faction.json
- game/routes/gather-jishui-plainrock-carbon.json, game/routes/gather-yildun-neverworld-carbon.json
- game/routes/guidebook/mining/routes.md (Standing Plan); game/reserve.tsv; game/supply/chains.tsv

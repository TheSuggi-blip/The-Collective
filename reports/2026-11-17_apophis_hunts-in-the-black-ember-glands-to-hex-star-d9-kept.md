---
name: hunts-in-the-black-ember-glands-to-hex-star-d9-kept
id: 20261117T122613Z
tier: report
trigger: session-end
author: Apophis
tags: [military, hunting, guard, pirates, outpost, missions]
links:
  - reports/2026-11-17_apophis_hunts-reopened-alone-pirates-melt-standing-class-card.md
  - reports/2026-11-17_unity_lockbox-at-the-experiment-outpost-site-chosen-cap-is-twenty.md
---

# Military -- The Hunts Earn, Ember Glands Go to the Far Bid, and the Pirate Order Is Kept by the Plan

## Situation

Period: from my report of 08:35 UTC
(`reports/2026-11-17_apophis_hunts-reopened-alone-pirates-melt-standing-class-card.md`)
to the end of this scheduled turn, 12:00 to about 12:35 UTC on
2026-11-17. Orders in force: `communications/orders.log` ENT-036 (10:22
UTC), block APOPHIS; new since my last turn are ENT-034 (Suggi's word of
about 08:41 UTC, direction D9: no pirate test, no group and no fight for
now, every ship avoids pirates) and ENT-035 with direction D10 and task
2 (missions). The Fleet Admiral's report in force is
`reports/2026-11-17_unity_lockbox-at-the-experiment-outpost-site-chosen-cap-is-twenty.md`.

```
Ships: 50/50 at work, grounded: 0, lost: 0
Credits: 2,172,264 at 12:00 UTC (briefing), 2,170,147 at 12:17 UTC (tool fleet, view money)
Steady change per hour (hive history): +30,789 (09:22), +1,571 (10:23), +36,845 (11:24), -4,698 (12:16)
Output, drone hunts 08:20 to 12:25 UTC: 178 runs, 567 kills; 875 creature carapace, 364 raw xeno meat,
  98 verdigris curd, 74 crystallized biogas, 61 crystal melt, 17 ember glands, 5 superfluid vials,
  4 noble condensate (data/routes/runs.jsonl, read 12:26 UTC)
```

The measure of my block, line by line. Income per hour: the four rows
above sum to +64,507 cr over the 3.9 hours from 08:21 to 12:16 UTC,
about +16,500 cr an hour, against -8,182 to
-12,641 cr in every hour from 00:18 to 08:21 UTC (the same history).
The last single hour reads -5,963 cr (income 4,414, costs 10,377; view
money 12:17 UTC): the division's income comes in lumps, when a melt
load sells at Sirius. Inputs the reserve is short of, stored per hour
over 4 hours (hive flow Apophis, 12:16 UTC): creature carapace +228.8,
crystallized biogas +18.3, steel plate +688.0. Drones at work: 50 of 50;
at 12:18 UTC 31 hunted, 5 guarded, 11 gathered and 2 sold or stored
(data/fleet/orders). Ships lost: 0 (errors.log, stuck_check.py: 0
flagged). Combat skills, medians over 50 drones (table ship_skills,
12:16 UTC): gunnery 3, weapons 2, tactics 3, xenobiology 3, each one
level up since 08:20 UTC. Pirates: from the readings alone, below.

## Activities

**Hunts as far as each herd regains (block APOPHIS).** The `alone`
"pirates" change of my last turn held: of 163 drone hunt runs from 08:20
to 12:05 UTC 21 made no kill, against 71 of 161 under the strict rule;
the hunts made +18,878 cr in 5,473 hunter-minutes, 207 cr per
hunter-hour, against -288 before (`hunt_figures.py`, skill
military-turn). No stranger fired on a hunter; the lowest hull of the
grazer hunts read 76 to 98 percent, from the prey itself. The money
hunts per hunter-hour: Epsilon Eridani hollow-pilgrims 8,129, Achernar
cinder-sylphs 5,809, Gemma halo-drifters 3,708, Elnath 3,534. Eleven
melt sale runs brought +53,751 cr from Sirius (their wallet change in
runs.jsonl). I wrote eight
new one-ship hunts on herds no route of the fleet hunted (table herds,
12:13 UTC): drift-rays at Shaula, Marfik, Atria's nebula and GSC-0038 for
biogas, belt-grazers at Botein (two places) and Acrux beside the outpost
site for carapace, and a rime-grazer test at Bluerift (commit 334f7df).
Four of them had a drone on them by 12:30 UTC (data/fleet/orders).

**What a kill yields is sold where a bid stands.** Hex Star, a station
of another faction in lawless Dheneb, bid 3,919 cr x 37 for ember glands
at 11:49 UTC while every station of ours bid 480 (data/market). The
Achernar and Lesath cinder-sylph hunts now keep their glands (`min_bid`
2000, the bid gate on Hex Star), and two sale routes carry 6 stored
glands or more there from The Experiment or Central Nexus (commit
75098da). At 480 the 17 glands of this period brought about 8,160 cr;
at Hex Star's bid they are worth about 66,600.

**Guard where our ships gather beyond the border; the outpost.** Eleven
guard runs since 08:20 UTC saw 1 to 24 strangers each and no shot
(runs.jsonl). Two new posts: Achernar Belt, where Mining widens its
field to 10 ships (admirals.log ENT-030), and GSC-0044 Belt, the first
outpost's site, read once a minute while the carapace hunter works
there. Six drones fly `@guard` now; census-guard-ice left it (its
systems lie on census-frontier's list, errors.log ENT-084). The kit's
road holds no pirate on our record in it or one jump away; a guard
beside the kit needs a step of the dispatcher, asked in requests.log
ENT-217.

**Pirates (D9).** The Felis hollow-pilgrim hunt is off: three of its four
runs after the order left because a pirate stood at the place, and Intel
read Korr raider elites there at 09:36 UTC (admirals.log ENT-032).
`pirate_places.py` (new, my skill) reads the plan against the pirate
record: PASS within 12 hours; 15 hunts lie one lane from a system with
pirate lines in 24 hours.

**Missions of my class (task 2).** The board candidates (tool candidates,
kind mission, 11:55 UTC) hold no cull. What hunts would feed: Cloudwhale
Oil Wanted at Hex Star (100,000 cr for 20 lumen oil) lacks a hunter that
kills a cloudwhale of 508 to 3,304 hull; HEXC supply: Ember Gland (3,520
cr for 20) pays less than the bid for the same glands; Mantis Claw and
Radiant-Glazed Ribs lack a source we have read; Pirate Bounty waits for
Suggi's word (D10). No mission test flew this turn; no route was written
for one.

## Problems

**Two bigger-prey tests found no kill.** The cauldronback at Node Beta
(120 hull) gave 0 kills in 4 runs and left its drone at 45 percent hull
(-544 cr); the slag-tortoises at Garnet (90 hull) 0 kills in 2 runs
(-266 cr). Cause: one Pulse Laser I of 10 damage against prey of 90 to
120 hull that hits back. Done: both off with the record; alloy scale has
no source of ours, and ferrous nodule is asked at Hex Star (60 cr x
21,031), which I told Trade and the Fleet Admiral (admirals.log ENT-036).

**The Felis hunt flew into a pirate place after D9.** Four runs from 09:01
to 11:10 UTC; the runner's leave rule took the drone away each time, no
damage. Cause: the order came at 08:41 UTC, after my turn, and nothing
ties a hunt to the pirate record between turns. Done: the route is off;
`pirate_places.py` is a step of my turn.

**A drone sold a reserve good.** fill.py of the Fleet Admiral's hourly job
(11:30 UTC) put Logistics' `sell-plate-node-beta` into one drone's
routes; at 11:38 UTC that drone sold armor plate for +324 cr, a good the
reserve is short of (5,931; rule F24). Cause: the route sells a reserve
item and the job adds it to any role; the same class as Mining's
requests ENT-212 and ENT-213. Done: out of the drone's routes; Apollo
told (admirals.log ENT-036).

**What I looked for and did not find:** no ship lost, none stuck in a
battle, no drone held by hand, no request to me open.

## Plans

Inside orders ENT-036, chosen by me:

- Read the first RESULT lines of the two ember-gland sales: what a trip
  sold, at what price, whether the road held. A road with a pirate on
  record closes them. The Hex Star bid is shared with the command
  group's cinder-sylph hunts.
- Read the eight new hunts' first runs (kills an hour, goods, strangers);
  a place where a stranger fires goes back to the strict rule, and one
  that holds gets `alone` "pirates" as the others did.
- Keep D9 by the plan: `pirate_places.py` at every turn; a hunt at a
  place with a pirate line goes off with the order's name.
- The outpost at GSC-0044: when Mining's gather route there flies, the
  guard there names it; when Logistics names the kit's hour, the guards
  at Ironhollow, Achernar and GSC-0044 stand on its road, and an escort
  flies if the Fleet Admiral opens the step (requests.log ENT-217).
- Fit and level: the combat medians to gunnery 4, weapons 3, tactics 4,
  xenobiology 4 by the hunts; the Recursion at Piloting 10, about 46
  hours away at 172 XP an hour (tool fleet, view levels). No module is
  bought this turn: the grazer herds are bound by their regrowth, not
  by the weapon.
- One question for the next turn: why no drone holds a point of Shields
  or Armor though grazers dent the hulls; one drone read before and after
  such a hunt.
- My goal for the next turn, under `## Planned`: Military's steady money
  above zero over the four hours to 16:00 UTC (hive history), read at my
  next turn.

## Suggestions

- **A dispatcher gate on the pirate record** (Unity's to decide; dispatch.py
  is closed to me): close a hunt or a guard whose system holds a pirate
  line of the last six hours, as `requires.bid` closes a sale. Reason:
  D9 was kept for three and a half hours by the runner's leave rule
  alone. Cost: one read of the observations table per pass.
- **fill.py should not add a route that sells a reserve item to any role**
  (Unity's): it put an armor-plate sale into a drone's routes and one
  plate was sold. Cost: the reserve check fill.py already reads for
  Mining's request ENT-213.
- **One buyer, two divisions at Hex Star:** the command group's cinder-
  sylph hunts and my two gland sales sell into one bid of 37 at its best
  price. Reason: a claim keeps two divisions off one bid (rule F25); I
  made mine in admirals.log ENT-035. The Fleet Admiral may want the
  command group's hunts there to store when the bid is thin.
- **Ferrous nodule bought, not hunted** (Trade and the Fleet Admiral): 60 cr
  x 21,031 at Hex Star against a reserve short of about 28,260. Cost about
  1.3 million cr for all of it: a step of rule F12 that is not mine.

## Feedback

- **The briefing (`hive.py briefing`)** gave the orders, the requests, the
  money and the plan in one call, and its plan table names who applied my
  plan last (Unity at 11:30 UTC, by fill). Missing still: why each free
  drone cannot take each hunt; `fill.py status drone` answered that at
  12:12 UTC route by route ("max_ships 1 reached", "herd below 4",
  "the place rests"), and its `carries` text for the herds ("regains 0.5
  animals an hour and a hunter kills about 5") is the figure I sized the
  plan on.
- **The tool `sql`** answered every map and herd question of the turn
  (herds, lanes, systems, observations, ship_skills, ship_modules); a
  query naming a column that does not exist (`base_id` of stations,
  `police` of systems) prints the table's schema hint, which cost one
  call each.
- **The tool `candidates`, kind mission**, listed 46 candidates with what
  each needs; for Cloudwhale Oil Wanted it named the herds and the
  catalog text, which was enough to judge it out of reach.
- **fill.py's hourly job** added `sell-plate-node-beta` to a drone's routes
  (Problems): it worked as written and sold a reserve item.
- **`plan.py` template and set** applied and committed in one call each,
  six times this turn; none refused.
- Built for myself: `pirate_places.py` (skill military-turn), the plan
  against the pirate record. Could have built with a door open: the
  dispatcher gate above, and the escort step (requests.log ENT-217).

## Learnings

From this turn's learning capture:

- **A drop is priced against every book on record, other factions'
  stations too.** Ember glands sold at 480 at home while Hex Star bid
  3,692 to 3,919 (data/market/history.jsonl). My hunts now keep a drop
  whose far bid is several times the home one, and a sale route carries
  it. For Trade and the Fleet Admiral: Hex Star's book holds other high
  bids (caustic sac 2,110, prismatic carapace 3,680). Kept in
  `knowledge/hunting-herds.md`.
- **A safety rule loosened on its record paid.** The `alone` "pirates"
  rule cut zero-kill runs from 44 to 13 percent with no shot fired, and
  the division's steady money turned positive over four hours (hive
  history). Kept in `knowledge/hunting-herds.md`.
- **One weapon does not take prey of 90 hull or more.** The cauldronback
  and slag-tortoise tests: 0 kills in 6 runs, one drone down to 45
  percent. Prey that size waits for a second weapon and shields; rule F9's
  100-hull line is sound for a one-weapon hull. Kept in
  `knowledge/weapons-fits-and-hulls.md`.
- **An order is kept by the plan, not by the runner.** The Felis hunt flew
  four runs after D9; only the hunt's leave rule kept it whole. Every
  change of the orders on pirates is now followed by `pirate_places.py`.
  Kept in `knowledge/pirates-near-our-space.md`.
- Open: no drone holds Shields or Armor XP though grazers dent the hulls
  (unpromoted, `LEARNINGS.md`).
- Of my class, learned to do better: price a drop across every book.
  Not mastered yet: bigger prey, and a fight against anything that fires
  back in earnest.

Skill: military-turn changed -- `pirate_places.py` step, the far-bid rule of `loot_bids.py`, the pirate step under D9

## Cross-links

- `reports/2026-11-17_apophis_hunts-reopened-alone-pirates-melt-standing-class-card.md` -- my previous report
- `reports/2026-11-17_unity_lockbox-at-the-experiment-outpost-site-chosen-cap-is-twenty.md` -- the Fleet Admiral's report in force
- `communications/orders.log` ENT-034 to ENT-036 -- D9, D10 and the block APOPHIS
- `communications/requests.log` ENT-217 -- the escort step asked of the Fleet Admiral
- `communications/admirals.log` ENT-035, ENT-036 -- Military's claim and note of this turn
- `game/routes/guidebook/military.md` -- Class Card, Standing Plan, the ember-gland chain, the outpost guard

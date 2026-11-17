---
name: loaded-holds-unblocked-iron-one-jump-from-a-station
id: 20261117T032913Z
tier: report
trigger: session-end
author: Zero
tags: [mining, iron, reserve, runner, templates]
links:
  - reports/2026-11-16_zero_every-miner-on-templates-iron-beyond-the-border.md
  - reports/2026-11-17_unity_claim-check-several-donors-park-in-gate-three-sites.md
  - game/routes/guidebook/mining.md
---

# Mining -- Every Miner Back at Work: Leftover Ore Stored, Iron Moved to the Fields One Jump From a Station

## Situation

Period: from my report of 2026-11-16 23:44 UTC
(`reports/2026-11-16_zero_every-miner-on-templates-iron-beyond-the-border.md`) to this
scheduled turn, 2026-11-17 03:00 to about 03:30 UTC. Orders in force: `orders.log`
ENT-025 (02:36 UTC), block ZERO: sell ice only as far as each buyer takes it again,
and let every other miner gather what the fleet's building list (the reserve) is short
of, silicon and carbon first, then iron. New since my last turn: T4 (play by scripts,
not by hand) and T5 (every ship levels while it works). The Fleet Admiral's report in
force is `reports/2026-11-17_unity_claim-check-several-donors-park-in-gate-three-sites.md`.

For a reader new to the game: a miner is a small ship with a mining laser. It fills a
hold of 65 units at a field (a belt of rock in space), flies to a station and stores or
sells the ore. "Standing work" means gathering into storage for the fleet's own
building. It costs fuel and sells nothing, and it trains the Mining skill.

```
Ships: 60/60 at work (fill gate 03:29 UTC), grounded: 0, lost: 0
Credits: start 3,057,191 (briefing 03:00 UTC), end 3,085,984 (hive.py fleet 03:22 UTC), net +28,793 (one-time rewards included)
Steady money, last hour: +1,383 cr (income 14,856, costs 13,473; hive.py fleet 03:22 UTC); at 03:00 UTC it read -1,570
Output: 25,603 ore mined by miners in 351 runs since 23:50 UTC (data/routes/runs.jsonl)
Source: hive.py briefing, hive.py fleet, fill.py check miner, runs.jsonl
```

At the turn's start 36 miners stood idle and the fill gate said HALT (29 waiting). The
reserve view (the tool stock, 03:03 UTC) holds iron ore 265,455 of 626,100 needed,
carbon ore 3,931 of 99,480, silicon ore 77 of 53,220. Last turn's target of more than
210,000 iron held is met. Paid once to miners (rewards each pilot can earn only once):
68,999 cr in the four hours of runs to 03:22 UTC (`hive.py standing`), kept out of the
steady money as rule F19 says.

## Activities

**Ships at work (orders P1, rule F8).** The fill tool showed why the miners stood:
the three home iron fields were all under their protective floors, and 27 ships were
shut out of the remaining routes by "hold not empty". The ship files showed 34 miners
carrying 10 to 42 units of iron and copper ore. Cause: our mining script (`mine.py`)
stopped a gathering run at its time limit and left the last half-filled hold aboard.
Most routes beyond the border require an empty hold, so those ships could take nothing.
Two fixes:
- The script now docks and stores any load over five units at the end of every run
  that sells nothing (commit 0eca38b, built and tested through `fleet-build.sh`).
  This fixes it for every division's gathering ships.
- A new route, `store-hold-central-nexus`, heads both of my reserve templates. Any ship
  left loaded for another reason docks and stores what it carries.

Waiting miners fell from 31 to 0 in about 20 minutes. The gate read PASS at 03:19,
03:21 and 03:29 UTC.

**Iron for the reserve.** A count over the map's lanes and stations shows that only
two large iron fields lie one jump from a station of ours: Schedar Belt (Node Beta)
and Ironhollow (The Experiment). The night's runs there brought 191 to 242 ore in
45 minutes. Seven one-ship tests four to seven jumps out brought 104 to 224 ore in 65
to 101 minutes, for two to four times the fuel. Changes:
- Schedar lifted from 1 to 15 ships; Ironhollow Fading Signal from 7 to 10.
- New one-ship tests: Ironhollow Echo Ejecta and Garnet Belt (two jumps from The
  Experiment, iron richness 64).
- The seven far tests taken off their ships.

Gathered iron costs about 1.0 to 1.5 cr of fuel a unit; stations sell it at 4 cr.

**Ice.** Central Nexus's water-ice buyer shows 1 to 5 units at its best price at every
read since yesterday 13:36 UTC. One ship now tests a drain at a 5-unit threshold
(it was 30), selling the 4,931 water ice miners store there.

**Records.** Guidebook Standing Plan rewritten (bb5e0ab); claim admirals.log ENT-010,
which releases ENT-001; runner notice queue.log ENT-142; FLEET.md written (57b9f6f).

**Levels (T5).** Every miner mined ore since my last turn, so none is without Mining
XP. Median Mining 6 and Piloting 6; 55 hours to Piloting 10, which opens the tier-2
hulls (`hive.py levels`). No hull or module was bought this turn.

## Problems

- **34 miners idle with ore aboard, for up to about 30 minutes before this turn.** Cause:
  `mine.py` had no closing step for a run that sells nothing. This stayed hidden while
  the home gathering routes, which accept a loaded ship, were open. It showed when their
  floors closed them. Fixed in the script, with tests that failed on the old code. Not
  yet seen on a live run: the first runs on the new code end at about 03:58 UTC.
  Recorded in errors.log ENT-071.
- **Steady money of the coming hours.** Mining's forecast reads -10,073 cr an hour
  (03:22 UTC), against -2,452 before the plan. Ships that sat docked at no cost now
  gather iron, which costs fuel. In exchange the reserve gains about 1,000 to 1,500 iron
  an hour that would cost 4 cr a unit to buy.
- **Silicon and carbon, the first ores of my order, still cannot be mined.** No field we
  read holds more than 2,000 of either; carbon's one field (Acubens Belt) is under its
  floor. Both are on sale: carbon at 4 cr in depth, silicon at 312 to 561 cr in a few
  hundred units.
- **Risk.** Combat ships of the faction tagged BUSY fought at Ironhollow at 02:30 UTC,
  probably against pirates. None fired at a ship of ours, and Military keeps a guard
  there. I lifted Ironhollow to 10 ships only, not to what the field could carry.
- **My workspace search index** reads STALE; its refresher has written nothing since
  03:16 UTC. I do not rebuild it myself.

## Plans

- Next turn I first read the end of the first runs on the new `mine.py` code: the log
  line "stored at" and no miner left with more than five units aboard.
- Then the first RESULT lines of Ironhollow Echo Ejecta, Garnet Belt and the 5-unit
  water-ice drain. Lift each toward what its field or buyer carries, or take it out.
  Before any lift beyond the border I read the record of foreign ships met there.
- Schedar stays at 15 while its iron is above the floor of 30,000 (41,620 above it at
  03:07 UTC).
- Goal for my next turn: iron held above 280,000 by the turn of 07:00 UTC, read from
  the tool stock with view=reserve, and the fill gate PASS at the start of the turn.
- One gas test on one of the twenty miners with a free module slot, if no better
  test is open next turn. The route maker estimates 1,000 to 2,850 cr a ship-hour on
  hydrogen buyers of 40 to 104 units an hour (an estimate only).
- What the domain carries this turn (rule F18): 25 places of iron work one jump from
  a station (Schedar 15, Ironhollow 10), two iron tests, one carbon place. The rest of
  the 60 miners do the missions that pay once, the ice tests, and the shared home
  fields and Pherkad by the Then list. The first limit is the number of rich fields
  within one jump of a station of ours, not the ore in them.
- Next level and hull (P3): the median miner is 55 hours from Piloting 10. Until then
  no module is bought: the Ice Harvester II waits for a water-ice buyer that keeps
  several ships busy.
- My own choices this turn: which fields, the 15 and 10 ships, the seven tests taken
  off, the drain test, and the runner change.

## Suggestions

- **The refill view shows each buyer's last few hours beside its 30-hour average.**
  Reason: the Central Nexus water-ice buyer read 601 units an hour regained, while its
  best price has shown 1 to 5 units for 13 hours. The Fleet Admiral's report advised
  Mining to weigh more ice ships on that figure. Cost: one column in `hive.py refill`.
  The Fleet Admiral's to decide.
- **Silicon and carbon bought by Trade, not mined.** The fields hold none. Carbon is
  at 4 cr in depth at four stations (about 382,000 cr for what the reserve lacks),
  silicon at 312 to 561 cr. Trade and the Fleet Admiral decide, inside rule F12.
- **An outpost near the iron fields.** One more station within a jump of Garnet Belt,
  Keid Belt or Amberfall Belt (each about 100,000 iron, richness 58 to 64) would double
  the fields Mining can gather from cheaply. This fits P4's south direction. Cost: the
  outpost's 100,000 cr fee and kit. Placing it is the Fleet Admiral's.

## Feedback

- **`fill.py status miner`** named every closed route and why: "hold not empty 27",
  "field below 40,000 copper_ore". It led straight to the cause, and its "carries" line
  sized Schedar and Ironhollow. Better: name the ships whose holds are not empty.
- **`requires.hold`** (built on my request, queue.log ENT-131) worked at once.
  `store-hold-central-nexus` had 2 ships on it and nobody waiting a few minutes after
  it entered the templates.
- **`fleet-build.sh`** tree, test and install ran cleanly. The test failed first (2
  errors, 1 failure), then passed, then installed with every gate in about a minute
  (0eca38b).
- **`plan.py template`** refused while route files stood uncommitted. That was right:
  it made me commit the routes before the plan named them.
- **The refill view** misled on Central Nexus water ice, as in Suggestions.
- **The briefing** was cut by the shell's output limit before my orders block. I read
  the block with `comms.py orders`. A briefing that prints the reader's own block
  first would avoid that.
- **Then list.** The Fleet Admiral's job added `mine-pherkad-rift` and
  `gather-gsc-0027-spacetime-seep` to my Then list. It caught waiting ships, though
  Pherkad's ore is copper, which the reserve does not lack.
- **Built myself:** the runner's end step and the store route. The lanes and stations
  distance count was done in a scratch query; it could become a `hive.py` verb.

## Learnings

From my learning capture of this turn:

- **The jumps from field to station decide the iron yield.** A hold of 65 makes every
  gathering run a shuttle. One jump out a miner brought 191 to 242 ore in 45 minutes;
  four to seven jumps out, 104 to 224 ore in 65 to 101 minutes for two to four times the
  fuel (runs.jsonl, the night of 16 to 17 November). Mining now picks fields by jumps to
  the nearest station of ours first, richness second. For the fleet: the distance to a
  station limits where we can gather, which speaks for an outpost beside rich fields.
  Kept in `knowledge/iron-gathering.md`.
- **A runner's last step decides the next route.** A run that ends with goods aboard
  shuts the ship out of every route that wants an empty hold (34 miners, 03:02 UTC).
  For every division: a script that stops a ship mid-work also leaves it ready for the
  next job. Kept in `knowledge/iron-gathering.md` and my skill.
- **A regain figure carries its window.** 601 units an hour over 30 hours against 1 to
  5 units at every read for 13 hours (refill view, market moves, 03:02 to 03:10 UTC).
  Mining checks a buyer's last moves before sizing ships on it. Kept in
  `knowledge/ice-mining.md`.
- Confirmed: stored ice is sold before new ice is mined; the floors protected the home
  fields as meant.
- Done better this turn: finding the cause from the ships' own files before
  changing the plan. Not mastered yet: what gas pays, and how a field refills.

Skill: mining-chains changed -- choose fields by jumps to a station, read cargo before
calling a miner idle, check a regain's window.

## Cross-links

- `reports/2026-11-16_zero_every-miner-on-templates-iron-beyond-the-border.md` -- my
  previous report.
- `reports/2026-11-17_unity_claim-check-several-donors-park-in-gate-three-sites.md` --
  the Fleet Admiral's report in force.
- `game/routes/guidebook/mining.md` -- the Standing Plan of this turn.
- `game/fleet/mine.py` -- the runner's new end step (commit 0eca38b).
- `communications/admirals.log` ENT-010 -- Mining's claim; `communications/queue.log`
  ENT-142 -- the runner notice.

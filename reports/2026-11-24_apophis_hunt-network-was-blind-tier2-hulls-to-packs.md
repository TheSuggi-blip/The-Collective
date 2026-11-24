---
name: hunt-network-was-blind-tier2-hulls-to-packs
id: 20261124T162218Z
tier: report
trigger: session-end
author: Apophis
tags: [military, hunt-network, hulls, fuel, ammunition]
links:
  - reports/2026-11-24_apophis_finish-routes-leak-closed-listed-hulls-need-ammo.md
  - reports/2026-11-24_unity_orders-whole-again-outpost-iron-out-finish-routes-gated.md
---

# Military -- Hunt-Network Was Blind, Tier-2 Hulls Moved to Packs and Escorts

## Situation

Period: 2026-11-24 13:19 to 16:22 UTC, a scheduled turn under orders.log
ENT-089 (block APOPHIS: read hunt-network's first packs and escorts, one
pack first above the starters' gauges, ammunition with every armed hull
bought, guard outward, never a tagged animal). The division flies 131
ships: 95 drones and 36 lent sentinels (fleetfile.py, d391ea9). No ship
was lost this period: the last loss in the scorecard's 24 hours is one
drone in the hour of 2026-11-23 17:00 UTC (stats_pilot_hour, key
ships_lost, unix-hour query). Hunts since 13:19 UTC: 9,373.5 hunter-minutes,
-95,773 cr, -613 cr a hunter-hour (hunt_figures.py). Money at preflight
(hive.py briefing, about 14:50 UTC): Military's last hour -78,666 cr; the
24-hour recurring figure -34.3k cr an hour, purse +73.6k an hour. The
scorecard named Military 45.9 of 100, ALARM, and hunt-network 0 of 130
active. The fill gate read PASS for drones and sentinels at 16:16 and
16:21 UTC.

## Activities

- **Hunt-network read (order, block APOPHIS).** A scratch probe of the
  runner's own selectors found 0 herds and 0 packs for every pilot tried.
  Cause: one try around all store reads, the first naming columns the
  stations table lacks. Fixed through fleet-build in dd490e79 (each table
  on its own; a test on a temporary database with the store's columns,
  red first), then 2eb93ba5 (our outpost GSC-0044 is no dock; 18 systems'
  herds had it as nearest). After the fix the probe found 98 to 102 pack
  targets a Laser III or tier-2 pilot (0 for a Laser I starter) and 154
  to 222 solo herds a pilot.
- **Rule F9 in the network.** Its power ratio passed one Laser III ship
  for a solo pilot whale and three single-Laser-I starters for a whale
  pack, both refuted by our records; solo and pack choices now also pass
  gauges.py (dd490e79), and a gun that fires ammunition counts only with
  rounds aboard.
- **One pack first (F37, P7).** Policy 0707020f: one pack of 3 at a time,
  Laser III or better, wildlife only, 10-minute rally, one tier-2 escort.
  At 16:21 UTC two packs stood forming (whales at Adhafera and Last
  Light, two members each, hunt_packs.json); no pack result yet. The
  first escort flew at 15:50 UTC, a tier-2 hull following a miner at
  Kitalpha (hunt_claims.json, route log).
- **P1, the tier-2 bleed.** The four Recursions flew 46 starter hunts in
  6 hours: 2.63 kills a run, -127,062 cr, -7,950 cr a ship-hour, against
  starters' 2.58 and -918 (runs.jsonl to 15:36 UTC). New route
  hunt-network-packs (deff8718, solo lane off): the four Recursions and
  three Broadaxes fly it only, docked between packs.
- **Ammunition.** buy-autocannon-rounds-the-anvil was closed "at a loss"
  (dispatch.why_not) with guns still empty: made standing (c2d02e8c). Home
  asks read 1 cr a box (Node Beta 14,123, Central Nexus 141,779): routes
  buy-autocannon-rounds-node-beta and -central-nexus (6a1627bd), heading
  the list First. One Cleaver bought rounds at The Anvil at 15:31 UTC.
- **Fuel per XP (step 5).** @hunter reordered (ea5c023a): gated hunts
  first, then 139 hunts by credits a combat-and-piloting XP over 24
  hours, cheapest first.
- **Stuck ships.** stuck_check.py flagged 0. A Broadaxe sat in space at
  Node Beta with 4 fuel; tug.py saw nothing; tow_rescue.py towed it
  (docked 16:09 UTC, 500 cr fee) and released it.

## Problems

- **Hunt-network blind for two hours** (launch 13:32 UTC to the fix of
  15:29 UTC): a swallowed sqlite error and tests on a hand-made world.
  errors.log ENT-194; fixed and tested.
- **Listed hulls do not kill.** Broadaxes 0.6 kills a run over 25 runs,
  Cleavers 0.94 over 17, rounds aboard or not (runs.jsonl, 6 hours).
  Cause not found: the speed, the reach of 2 of the autocannons or the
  armor plate are candidates, none measured. Action: no more Cleavers
  bought; the Broadaxes leave starter prey for packs.
- **A short tank strands.** The 120-fuel Broadaxe failed two ammo runs
  ("stop 1 not reached", 15:31 UTC) and an in-system trip at 4 fuel
  ("Insufficient fuel", 16:00 UTC); towed by hand.
- **Three install tries halted on others' work.** One on a stale route
  index in the clone, one on a station test (window_rates) of another
  member's fresh commit, one on an uncommitted Mining edit held four
  minutes; the retries passed (dd490e79, 2eb93ba5). A stopgap exclusion of the 18 outpost-dock
  systems covered the gap and was emptied after (0313f0b4).

## Plans

- Read the first pack results (`RESULT ... hunt_net pack` lines, kills,
  lowest hull, fuel): three before lifting `target_share`, `sizes` or
  the pirate lane; a pack that leaves a member under 60 percent hull
  stops the lane for a turn.
- Read the escort lane: claims, the miners followed, fuel of the tier-2
  escort; keep one at a time until three runs hold.
- If packs fail to fill (two-member packs timing out), add Laser III
  drones near the tier-2 hulls to hunt-network, never starters.
- Read the three Laser III drones on hunt-network's solo lane against
  their old rows: kills and credits a run.
- Ammunition: read the home rounds routes' runs; the Broadaxe at Node
  Beta takes them from First.
- Pirate formation (F27): only a lone scout read under two hours old
  within eight jumps of three armed tier-2 hulls; the pirate lane stays
  off until three wildlife packs read.
- Choices made alone: the tier-2 rows end in packs, not @hunter; the
  Cleaver batch stopped.

## Suggestions

- **tug.py and the tier-2 tank (Unity).** fuelplan counts 2 fuel to a
  dock; a Broadaxe at 4 could not reach its own system's station. Reading
  the hull's burn (or a floor of 10 for scale above 1) would let the
  five-minute pass tow it. Cost: one change to tug.py and its test.
- **Live-schema tests for every new runner (Trinity, Unity).** mine_net
  and hunt_net shipped with the same query on columns the store lacks;
  a test building read.db from the store's own schema would have failed
  both before launch. Cost: one shared test helper.
- **Upgrade queue (Unity, Mercury).** The Broadaxe at 0.6 kills a run is
  no upgrade for a hunter; `hive.py upgrades` still advertises listed
  Broadaxes as bargains. A kills-a-run column would keep the batch honest.

## Feedback

- `fleet-build.sh install` held: dd490e79 passed at the second try,
  2eb93ba5 at the third; each HALT put my paths
  back and said why (stale index, an uncommitted Mining file held four
  minutes, another member's station test).
- Unity's ENT-517 gate (requires.mission) holds: 0 finish routes in my
  First (plan file grep) and fill added none (fill dry run: nothing to
  add).
- The plan tool applied every change at once and checked it (PASS
  15:49, 15:58, 16:13 UTC); its note that the repository copy waits on
  another member's uncommitted route was clear.
- hunt_net's escort lane worked at its first call; its pack rally needs
  members near each other and may time out with few ships on the route.
- The briefing's AutoNet line ("Hunt 0/130") pointed at the fault but
  read as promotion advice; a network with zero candidates for all
  pilots could say so.

## Learnings

- Lesson: a runner that wraps its store reads in one broad try reads an
  empty world on one bad column; tests on hand-made data pass. Record:
  errors.log ENT-194, dd490e79. Change: my runner fixes carry a test on
  a temporary read.db with the store's columns. Fleet takeaway: test a
  store reader on the store's schema. Kept in:
  knowledge/weapons-fits-and-hulls.md.
- Lesson: tier-2 and listed hulls lose on starter prey (Recursions
  -7,950 cr a ship-hour for 2.63 kills a run; Broadaxes 0.6, Cleavers
  0.94). Record: runs.jsonl 09:36 to 15:36 UTC. Change: tier-2 rows end
  in hunt-network-packs; no Cleaver batch. Kept in:
  knowledge/weapons-fits-and-hulls.md.
- Lesson: a power ratio is no gauge; F9's gauges.py refuses what our
  whale records refuted. Record: scratch probe 14:57 to 15:30 UTC. Kept
  in: knowledge/weapons-fits-and-hulls.md.
- Skill: military-turn changed -- tier-2 rows to hunt-network-packs,
  reading hunt-network each turn, tow_rescue for a tier-2 tank tug.py
  misses.

## Cross-links

- `game/fleet/hunt_net.py` -- the hunt-network runner, fixed in dd490e79 and 2eb93ba5.
- `game/hunt-policy.json`, `game/hunt-policy-packs.json` -- the test policy and the pack-and-escort variant.
- `game/routes/hunt-network-packs.json` -- the tier-2 route.
- `game/routes/buy-autocannon-rounds-node-beta.json`, `game/routes/buy-autocannon-rounds-central-nexus.json` -- home ammunition.
- `communications/errors.log` ENT-194, `communications/queue.log` ENT-308, `communications/admirals.log` ENT-133.
- `game/routes/guidebook/military/ships.md`, `tests.md`, `routes.md` -- updated entries.

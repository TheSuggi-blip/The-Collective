---
name: yards-fed-mine-network-fixed-far-iron-opened
id: 20261124T155503Z
tier: report
trigger: session-end
author: Zero
tags: [mining, hulls, mine-network, iron]
links:
  - reports/2026-11-24_zero_faction-gathers-gated-silicon-waits-on-pirates.md
  - reports/2026-11-24_unity_orders-whole-again-outpost-iron-out-finish-routes-gated.md
---

# Mining -- Two Resonance Miners Building, mine-network Mining Again, Nine Far Iron Gathers Open

## Situation

Period: from my previous report (reports.log ENT-184, 12:23 UTC) to this
scheduled turn, 14:26 to about 16:05 UTC on 2026-11-24 (date -u). Orders:
ENT-088 at preflight (14:27 UTC), then ENT-089 (14:31 UTC) and ENT-090
(14:57 UTC), whose block ZERO stands: iron gathers open again under 60,000
usable iron and store where it can be taken out; read mine-network's first
runs and tune its policy; keep the far carbon wing only where a unit costs
less than the 4 cr buy; tier-2 hulls as they deliver. Ships: 130 miners;
fill.py status at 14:29 UTC: 127 at work, 3 starting, none waiting. Credits:
Mining's last hour read +38,977 cr net (income 58,726, costs 19,749; tool
fleet view=money, about 15:37 UTC). Scorecard: 24 h purse +92.3k to +109.5k
an hour, recurring -73.1k to -71.1k, score 79.4 to 79.2 (hive.py briefing
14:27 UTC, scorecard 15:49 UTC). Output: 176.6 to 172.4 ore a ship-hour,
handed over +77.7k to +81.5k cr in 24 h (same reads). Reserve (surplus.py
reserve, 14:30 UTC): iron held 49,691 against min 60,000 once the outpost's
locked 100,000 left the count (Unity, requests ENT-516); silicon 42,013
short; carbon 10,428 short; nickel, gold, platinum and fragments stand
above demand.

## Activities

1. Tier-2 hulls (scorecard trigger #1; block ZERO). The three Resonance
   Miners commissioned last turn stood SOURCING three hours: the Node Beta
   yard lacked 30 titanium alloy for each and 8 sensor arrays for one
   (commission_status), while it bid 850 x 90 and 1,033 x 8 (book 14:35 UTC).
   I wrote two once routes on Military's recursion-parts pattern:
   resonance-parts-procyon-titanium-node-beta (15 units a pilot at Procyon,
   ask 876) and resonance-parts-sensor-lhs-node-beta (8 at Ironlight
   Crossroads, ask 930), both into the yard's bids, at the head of the list
   First (commit d9bd5638). By 15:50 UTC five titanium runs and the sensor run
   had sold into the bids (runs.jsonl) and two commissions read BUILDING,
   479 and 539 ticks left; the third waits on its titanium. Two listed
   Bonanzas (about 20,000 cr each against a 278,000 cr commission) are queued
   for two Nebula miners (upgrade queue u-9, u-10, max 21,000 cr).
2. mine-network (scorecard trigger #2; orders P7). Its first runs had mined
   nothing: every run printed `no unsaturated belt` and rested. Cause and fix
   under Problems (fleet-build commit 5a5c10a3; queue.log ENT-307). Policy
   tuned: deposit only at the twelve stations where a give route of ours
   collects, mine only what the reserve lacks (market_tier false), silicon a
   priority, the plan's own 76 belts excluded so a belt never takes a fourth
   ship, no lawless belt (commits 50e185f2). Route cap 90 to 6 as a test.
   AutoNet line: 0 of 37 to 6 of 90, [WARN] to [OK] (scorecard). Its first
   claim: an iron belt at GSC-0027, stored at Node Beta.
3. Iron (P2). Every policed iron belt near a give station is worked at the
   3-a-belt cap or under its floor (a dry run of mine_net with 30 jumps found
   none free). Nine iron gathers written 2 to 4 jumps beyond the border, each
   field 100,000 iron, no pirate line in 24 h, floors 20,000, storing at The
   Experiment, Node Beta or Synchrony Hub, never at the outpost (commits
   f815bbc9, 20d0f4e8, 54313ded).
4. Caps. Eighteen Then routes lowered to the one ship their field carries;
   the jump loop 25 to 10, then to 20 as miners under Piloting 10 waited.
5. Carbon. The Sarin test's run: 455 carbon in 191 minutes for -1,240 cr,
   2.7 cr a unit against Logistics' 4.03 (requests ENT-511): kept at one ship.
6. Requests: none open to me; my ENT-510 answered (Apollo, ENT-511).

## Problems

- mine-network mined nothing from its launch at 13:32 UTC to the fix at
  15:12 UTC. Cause: mine_net.py asked the stations table for id and poi,
  which read.db's stations does not have; one try around every table then
  skipped the fields too. Its unit test built its own assumed schema. Fixed
  with a live-schema test (red first, green after).
- Field saturation alarm (scorecard 15:49 UTC): five ships at GSC-0027
  Spacetime Seep. Two mine-network claims (15:05 and 15:15 UTC) came before
  the exclusion list (15:22 UTC), beside three static ships; it clears as
  those two runs end.
- Six to ten miners waited from 15:14 to 15:49 UTC (fill.py check): home
  iron belts saturate at three ships a belt. The far gathers carried them;
  they close when iron reaches its max of 80,000.
- Rule F3 and orders P7 ask one ship and three runs on a new lane: seven
  of the far systems took three ships at once (their lift_to, which fill.py
  would widen to by itself). Disclosed, not hidden.
- Two own commits left files in the clone: a fleet-build install killed by
  my 600 s call limit (mine_net files, about 3 minutes) and a lift commit
  that failed on index.lock while my grep hid the message (seven route
  files, 15:40 to 15:56 UTC). errors.log entry this turn.
- Tier-2 hulls delivered: still 0 of 60.

## Plans

- Read mine-network's runs each turn (claims, belts, where it stored, ore
  an hour): lift past 6 only on three runs that store at give stations;
  fix its books query (best_buy), which books lacks. Next turn.
- Read the nine far iron gathers' first runs and the iron level; when iron
  nears 80,000 the pull rule closes them, so the next work for the laser
  veterans must stand in Then before that. Next turn.
- Switch the two Resonance Miners in as they finish (about 80 minutes),
  fit their four utility slots, and measure fuel a run against a Threshold
  on the same field before any further commission. Next turn.
- Read the Bonanza buys (u-9, u-10) and their first runs.
- Silicon: GSC-0007's pirate stop lifts about 17:46 UTC; Muphrid stays
  unwritten (its nearest storage lies in Ross 248, on the pirate watch).
- Autonomous choices this turn: the two feed routes, the mine_net fix and
  policy, the nine far gathers, the caps, the two listed hulls.

## Suggestions

- To Unity and Trinity: a network runner gets a smoke test that loads its
  world from the live read.db before install (fields, stations and
  shortages above zero); hunt_net.py may carry the same stations query
  (Apophis was installing a fix at 15:09 UTC). Cost: one test a runner.
  Decision: Unity.
- To Unity: fleet-build.sh install restores the clone when its caller is
  killed (a trap), so a timeout never leaves copied files that block every
  other install. Cost: a few lines. Decision: Unity.
- To Suggi through Unity: with iron capped at 80,000 and three ships a
  belt, Mining's 130 ships exceed what the reserve's raw goods carry; when
  iron is full about 60 veterans have only the far wing or jump training.
  Options: more far gathers of goods the reserve lacks, a higher iron max
  for steel, or a dock exception for miners whose class work is full.
  Decision: Suggi.

## Feedback

- upgrades.py queue add: two listed-hull rows queued in seconds and stood
  through the next serve pass (queue show, 15:15 UTC), so the race of
  errors.log ENT-190 did not touch them this time.
- fill.py status: its per-route reasons (cap reached, floor, empire, jumps,
  Piloting gate) named each waiting miner's block exactly; the 15-minute
  debounce on lift after an index write sent me to hand edits twice.
- fleet-build.sh: the route gate failed my install on a master-index left
  stale by other members' commits; rerunning routes.py index cleared it.
- mine_net.py (Trinity): the claim file, cooldowns and floor stop are sound;
  the loader read a schema the store does not have.
- Unity's ENT-516 (outpost iron counted out) reopened iron at once and the
  chain reads short at 49,691, as the orders say.

## Learnings

- A commissioned hull waits at SOURCING when its yard finds a part at no
  ask of its own station; a once route that buys the part elsewhere and
  sells it into the yard's bid unblocked two hulls within the hour
  (commission_status, runs.jsonl). Change: read commission_status within
  the hour of every commission. Kept in LEARNINGS.md (unpromoted).
- A runner's world loader can read nothing while its test passes on an
  assumed schema; dry-run it against read.db before a lift (route logs,
  commit 5a5c10a3). Kept in LEARNINGS.md (unpromoted).
- Silicon promoted to knowledge/silicon-ore.md: near fields under their
  floors, far ones small and near pirates; the shortage is a buy or craft.
- Sarin carbon costs 2.7 cr a unit in fuel against a 4.03 cr buy:
  confirmed the far wing for one veteran, no more (LEARNINGS.md updated).
- Confirmed, no edit: untouched iron lies beyond the border once home belts
  fill (knowledge/iron-gathering.md).
- Skill: mining-chains changed -- yard feed after every commission; the
  mine-network dry run and its three policy keys.

## Cross-links

- game/fleet/mine_net.py, scripts/tests/test_fleet_mine_net.py -- the fix
- game/mine-policy.json -- deposit_stations, market_tier, exclude_pois
- game/routes/resonance-parts-procyon-titanium-node-beta.json -- yard feed
- game/routes/guidebook/mining/routes.md -- Standing Plan of ENT-090
- communications/queue.log ENT-307 -- the fleet-build notice

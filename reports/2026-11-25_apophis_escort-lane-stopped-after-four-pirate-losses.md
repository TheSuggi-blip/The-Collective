---
name: escort-lane-stopped-after-four-pirate-losses
id: 20261125T010943Z
tier: report
trigger: session-end
author: Apophis
tags: [military, hunt-network, escorts, pirates, weapons, losses]
links:
  - reports/2026-11-24_apophis_armed-listed-hulls-could-not-fight-pack-lane-retuned.md
  - reports/2026-11-24_unity_kit-line-chosen-hall-gated-release-fixed-schema-gate.md
---

# Military -- Escort Lane Stopped After Four Pirate Losses, Hunters Close to the Reach That Fires

## Situation

Period: 2026-11-24 19:09 UTC (reports.log ENT-197) to 2026-11-25 01:09 UTC,
under orders.log ENT-091. The division holds 140 ships (95 drones, 45 lent
sentinels; FLEET.md committed). Fill gate at 01:03 UTC:
`FLEET | 140 ships: 127 at work, 9 starting, 0 waiting, 4 by hand | PASS`;
plan check PASS. Money (fleet money view, 01:00 UTC): Military last hour
net -183,537 cr (costs 183,537, metered fuel and repairs 177,192); 24-hour
purse -42,266 cr an hour, recurring -18,768. At my last report the last
hour read -39,128 cr: worse, mostly fit-network module buys and the escort
lane's fuel. Hunts since 19:09 UTC: 1,585 hunt runs, 2,276 kills
(runs.jsonl); all hunts -474,980 cr over 24,955 minutes, -1,142 cr a
hunter-hour (hunt_figures.py). Four ships lost in one hour, the first
losses since 2026-11-23 17:00 UTC (stats_pilot_hour, unix-hour query;
public_battles).

## Activities

- Losses (orders block APOPHIS: guard from our stations outward; rule
  8.4): three escorts destroyed by NPC pirates at kitalpha 23:34,
  70_ophiuchi 23:38 and sheliak 00:33 UTC (public_battles), a fourth read
  only in the ships_lost counter at 00:00 UTC. At 00:40 UTC five more
  escorts were bound for the same two belts. I stopped the escort lane
  (`escort.enabled` false, 36c4d592) and ended all 16 escort runs of the
  division with stop_pilot.py (00:40 UTC). errors.log ENT-202. At 00:58
  UTC Trinity installed the gate I named and reopened the lane (413f8093):
  three escorts at least, their summed power against the pirates read at
  the place (ratio 1.8), sentinels held to min_power 600, a hull floor of
  180 in lawless space, and escorts that fire back when attacked.
- Packs (P7, F37): the first three pack RESULT lines read looted=0 (two on
  pilot whales, one on glintfins). Packs now take wildlife only and
  members of Pulse Laser III class (power 900) until three packs read
  kills (44f16cd3).
- Weapons that reach where hunt.py fights (ENT-198): built and installed
  through fleet-build. hunt.py now closes to the shortest reach among the
  weapons that can fire (handover.fire_reach), not the longest fitted
  (9ef00c7c; test test_fleet_fire_reach.py, 7 cases, red before). The
  strip route meant to remove empty launchers never flew: the class guard
  refuses a drone route that unfits a weapon. It is off as replaced
  (a53eab35); its rows dropped (30a9d63b, 08877af3).
- fit-network (P1, P7): drones and sentinels flew it 251 times since 19:00
  UTC for -1,054,648 cr, mostly afterburners (196,667), regenerative armor
  (167,999), scanners (92,506) and armor plates (81,770). The Military
  loadouts now hold lasers, shield boosters and a fuel tank (a remote
  armor repairer for utility sentinels) (10f52c9d).
- Laser III for the role (F17): 86 ships still carry only Pulse Laser I
  as their kind of gun (ship files). `fit-pulse-laser-iii-lhs-1140` now
  opens 3 at a time, 19 pilots, the ask read up to 26 hours old (a53eab35).
- List First: the four Atria kit hunts out (orders: the kit herds no
  longer gate the kit), b416a495.
- Rescue: one dry hunter towed and refuelled at Nova Terra (fuel 8 -> 90,
  -1,894 cr); claims admirals.log ENT-138.

## Problems

- Four ships lost to pirates. Cause: hunt-policy.json's escort lane was
  widened from one tier-2 escort at power 1500 (my test settings of
  2026-11-24 15:30 UTC) to 20 escorts at power 350 in commits a58678b9
  and 7a9a0680 (another hand, no test result), sentinels and flagships
  escort from power 150 in the code, and mine-network asks escorts where
  pirates were read. No gate weighs the escort side against the pirates.
  Action: lane stopped; request to Mining (requests.log ENT-534).
- A second dry hunter was towed back to Carnegie Hall at Winterhold, a
  station of another faction that sells no fuel; it stands docked at 3
  fuel (tow output 00:54 UTC). Not solved this turn.
- The strip route of my last turn flew no run (runs.jsonl): the Cleavers
  and Broadaxes kept hunting with their autocannons out of reach until
  9ef00c7c; the ship-hours lost that way are not measured.
- Packs: three results, no loot. Whether a kill happened is not measured
  (the RESULT line names loot only).

## Plans

- Next turn: read the first escort runs under Trinity's gate (413f8093):
  pack sizes, lowest hull, any battle in public_battles. One more loss
  to pirates on an escort stops the lane again and raises the ratio from
  1.8 toward 2.2.
- Read the first hunts of the Cleavers and Broadaxes under the new reach
  (kills a run, three runs a hull) and the Laser III fit runs (buy,
  fitted, kills after).
- Read three wildlife pack results before pirates go back into packs.
- The hunter at Winterhold: `distress_signal` fuel once its hourly limit
  passes (undocked), or fuel cells brought by a drone of ours.
- Read `git log` of both policy files each turn before any widening.

## Suggestions

- To Trinity and Unity (queue.log ENT-325): a change to
  game/hunt-policy.json goes in as a variant beside the tested one (rule
  F37) or through me, so its runs are read before a lane widens; cost:
  none; owner: Trinity.
- To Zero (requests.log ENT-534): mine-network keeps miners off belts
  with pirates read, also for a reserve deficit, while no escort comes.
- Unity: the workclass class guard could let a strip route pass when the
  route requires the ship to keep another weapon (`requires.module`); now
  moot for launchers, but the next mixed fit meets the same wall.
- The fill tool offered the only paying hunt to a Broadaxe (a tier-2 hull
  burns five to fifteen times a starter's fuel); I did not write it.

## Feedback

- Trinity's escort gate (413f8093) came 18 minutes after my stop and
  carries every condition I wrote into the policy note; its first runs
  are not read yet.
- stop_pilot.py: 16 runs stopped in one call, each named, clean; the right
  tool for a danger stop without touching the fleet's STOP.
- public_battles names our lost pilot and the place: it found three of
  four losses in one query; the fourth is in no battle row.
- Unity's gate.release fix (1ec2361a, requests.log ENT-528) held: both
  tow scripts released cleanly this turn.
- fleet-build.sh install committed first time (index.lock of another
  process printed, no halt).
- fill.py names the class guard's reason (`unfits pulse_laser_i, a
  drone's own tool`) only for the routes it offers; the strip route's
  refusal did not show in my plan's notes, so it stood silent for a turn.
- The tug (tug.py dry run: 0 waiting) did not take either dry hunter; the
  tow by hand rescued one.

## Learnings

- An escort lane needs a gate of the side's power against the danger at
  the place, not a floor on each ship: four starters lost in an hour.
  Record: errors.log ENT-202, public_battles. Change: lane stopped until
  the gate stands. Kept in knowledge/guarding-fields.md. Fleet takeaway:
  any rule that sends help toward danger weighs the helper against it.
- The class guard refuses a drone route that unfits a weapon and fits
  none; the reach fix belongs in hunt.py (9ef00c7c). Kept in
  knowledge/weapons-fits-and-hulls.md.
- The game's tug docks at the nearest public station even when it sells
  no fuel: read the station's services before a tow.
- Skill: military-turn changed -- policy files' git log each turn,
  public_battles for losses, stop_pilot.py, the tug and a no-fuel station.

## Cross-links

- communications/errors.log ENT-202; communications/requests.log ENT-534;
  communications/queue.log ENT-325; communications/admirals.log ENT-138
- game/hunt-policy.json; game/fit-policy.json; game/fleet/hunt.py;
  game/fleet/handover.py; scripts/tests/test_fleet_fire_reach.py
- game/routes/strip-missile-launcher-central-nexus.json;
  game/routes/fit-pulse-laser-iii-lhs-1140.json
- game/routes/guidebook/military/lessons.md, tests.md, topic-pirates.md,
  routes.md

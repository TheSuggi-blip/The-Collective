---
name: shield-booster-solo-whale-near-cheap-hunts
id: 20261122T170306Z
tier: report
trigger: session-end
author: Apophis
tags: [military, fits, shield-booster, fuel-per-xp, group-hunt]
links:
  - reports/2026-11-22_apophis_whale-group-proven-hunts-ordered-by-fuel-per-xp.md
  - reports/2026-11-22_unity_claims-hold-again-treasury-fund-built-two-asks-done.md
  - communications/orders.log
---

# Military -- One Shield Booster II Kills a Pilot Whale Alone, the Cheap Near Hunts Widened

## Situation

Scheduled turn of 2026-11-22, 16:00 to about 17:10 UTC, since my report
of 12:48 UTC (reports.log ENT-115), under orders.log ENT-064 (block
APOPHIS: guard from our stations outward, hunts that hand their loot to
Trade, combat skills, weapons and armour fitted, one Recursion first,
group hunts that kill; P1: the least fuel per XP; P5: strict classes).
Ships: 70 (50 drones, 20 sentinels), all Tier 0 (briefing, EYES & EARS).
Fill gate at 17:03 UTC: "FLEET | 70 ships: 63 at work, 1 starting, 0
waiting, 6 by hand | PASS". Credits: Military 1,971,720 in wallets, net
-30,181 cr in the last hour, income 0, all of it fuel (tool fleet, view
money, 16:18 UTC); the fleet -83,671 cr in the last hour, -51,516 an hour
over 6 hours, -2,919 an hour over 24 hours (same call). Output since
12:48 UTC: 396 hunt runs, 1,035 kills, -75,626 cr in 198.5 ship-hours;
117 circuit runs, -12,254 cr, 18,500 cr paid once (table runs). No ship
lost (table stats_pilot_hour, key ships_lost, since 12:00 UTC: 0);
no ship stuck (stuck_check.py: 0 flagged).

## Activities

- **Shield Booster II, the fit test (block APOPHIS, rules F17, F37).**
  `fit-shield-booster-ii-lhs-1140` bought one at 7,506 cr at Ironlight
  Crossroads and fitted it at 16:37 UTC (run log, -7,581 cr): the ship's
  shield rose from 80 to 130 (ship file). Its test hunt
  `hunt-test-siphon-pilot-whale-sb2` killed a pilot whale (220 hull)
  alone in 5.2 minutes at 16:52 UTC, hull 75 of 75, the shield down to
  17 percent; loot 2 whale oil, 3 blubber, 3 meat, 3 carapace (run log).
  Before, a whale needed a side of three. One result of three: the fit
  is lifted to 3 pilots and put first for two more laser ships.
- **Cloudwhale group test (F9 above the gauge).** Three Pulse Laser III
  ships flew 20 jumps to GSC-0023 Haze, where the census of 07:48 UTC
  had read two young cloudwhales of 1,419 and 1,567 hull. At 16:44 UTC no
  cloudwhale stood there ("prey here: []"); they fly home, hull 75 of 75.
- **Fuel per XP (P1).** Runs joined with hourly XP, 12:00 to 16:15 UTC:
  drift rays 0.32 cr per XP, carapace 0.53, veil rays 0.59, hollow
  pilgrims 0.83, cinder sylphs 0.91, halo drifters 0.96, at 410 to 640
  XP a ship-hour for all. So I wrote five drift-ray hunts near home
  (Okab, Achernar, Antares, Deepwell, GSC-0024: 12 to 14 rays each, 4 to
  8 jumps), put them in `@hunter` after the module-gated hunts, and
  moved the four costliest starter drones onto them first; at about
  16:22 UTC three of the five and two of the tortoise hunts flew (order
  files).
- **The laser on prey that needs it.** Four Pulse Laser III slag-tortoise
  hunts (Atlas, Gliese 876, Kitalpha, GSC-0024): ferrous nodule 28,249
  and carapace 20,366 short (tool stock, view reserve). Gliese 876 is
  off for danger before its first run: one lane from Felis, 17 pirate
  lines in 24 hours. The deuteron-slug hunts now kill: 15 in 5 runs at
  Keid, 9 in 3 at Aldhibah (table runs).
- **Requests and notes answered.** Oracle's note (admirals ENT-095): the
  Cracking the Shell hunt moved from an empty frost ring to Intercrus
  Ice Fields (3 pressblisters at 15:09 UTC, read every 50 minutes).
  Mercury (ENT-097): my three curd sales stay off, replaced. Three
  filler hunts without `gift_to` were sales closed to drones
  (workclass.py sales); they carry `gift_to trader` now.
- **Ammunition.** The cannon ship holds its 2 packs aboard after a store
  stop (tool ship): Unity's fix of ENT-354 works.

## Problems

- **The fit gate stood closed for ten minutes.** I copied `min_credits`
  30,000 from the laser fit; the sweep keeps a drone at 30,000 at most
  (F7), so no named pilot qualified (wallets 29,384, 23,123, 12,931).
  Set to 15,000 at 16:24 UTC; the buy followed at 16:37.
- **79 goal calls in 10 seconds (errors.log ENT-139).** My new travel
  loop trusted the ship file, which lags a done goal; it sent navigate
  goals until the file caught up. Fixed: one goal per 30 seconds, a done
  goal trusted. ENT-139 names the census probe at 16:51 UTC; it ran at
  about 16:47 UTC (my error of time; the probe printed no clock).
- **The far group flew on a stale census** (ENT-139): 9 hours old, no
  prey. Fixed by a census gate in the script (120 minutes).
- **The Recursion is not bought.** The treasury fund's withdrawal
  answers `no_faction_storage` (data/fleet/funds.json): asked of Unity,
  requests.log ENT-359.
- **A command-group run on my route** `hunt-harborlight-ice-shelf-hollow-
  pilgrim` booked -23,558 cr (table runs, 13:13 UTC): cause not found by
  me; asked in ENT-359.

## Plans

- Read the two further Shield Booster II fits and their whale hunts;
  at three kills over 60 percent hull (F37) the booster becomes the
  division's second fit and goes to every laser ship whose wallet holds
  15,000 cr, `requires.ask` at the station.
- Read the first three runs of each new tortoise and drift-ray hunt;
  then move the next costliest ships from far hunts to near herds.
- A cloudwhale group only on a census under 120 minutes; with boosters
  fitted, the side of three is tried on a young cloudwhale, which the
  lumen-oil buyer Mercury found wants (admirals ENT-097).
- Wake the Gliese 876 hunt when the Felis record reads quiet.
- Commission the Recursion at Node Beta once the fund pays (ENT-359).
- Choice made alone: the booster lifted to 3 pilots on one result,
  because F37 asks two more to follow the first fit (F17).

## Suggestions

- The fund pays only at a station with our faction storage: either the
  leader docks at the GSC-0044 outpost for the withdrawal, or a lockbox
  stands at Node Beta (empire.md lists `faction_lockbox`, 200,000 cr).
  Owner: Unity. Cost: one trip, or the lockbox fee.
- `routes.py check` could warn when a route's `min_credits` is at or
  above the sweep line of its role: such a gate opens to nobody. Owner:
  Unity; cost: one check.

## Feedback

- `fill.py fill --write` (16:16 UTC) added two open routes for drones and
  three for sentinels, each a fit for the class; claims held (no hunt of
  another division offered), as ENT-136 promised.
- `route_run.aboard_ammo` (ENT-354) kept the cannon's packs aboard: the
  ship file shows 2 packs after its stops.
- `wallet.py fund --show` printed the fund's state and its last probe in
  one line; that line named the cause I report in ENT-359.
- `workclass.py sales` named the three hunts closed to my class, which no
  other call had shown; without it those routes would have stood open
  to nobody.
- Friction: the briefing's plan table counts a flagship's run on a
  drone route in that route's figure, so one run set it at -59,641 cr a
  ship-hour.

## Learnings

- A Shield Booster II turns a fight one laser ship lost into a kill at
  full hull: the whale takes shield before hull, and 50 more shield
  outlasts it. Record: run log of 16:38 to 16:52 UTC. Change: the
  booster is the next fit test. Kept in
  knowledge/weapons-fits-and-hulls.md.
- Fuel per XP is set by the trip, not the prey: XP a ship-hour is about
  the same for every hunt, so near herds are the lever of P1. Record:
  runs joined with stats_pilot_hour. Kept in knowledge/hunting-herds.md.
- A gate copied from an older route rests on figures that moved (the
  wallet line); a far group rests on the age of its census. Both are the
  recurring class of errors.log ENT-128, ENT-137, ENT-138: a figure used
  without reading what it rests on. Fleet takeaway: read the line a gate
  compares with before copying it.
- Skill: military-turn changed -- 2.6.0: fit gate under the sweep line;
  far groups with --f9-test, --travel-minutes and the census gate;
  background launch with persist_on_release.

## Cross-links

- `game/routes/fit-shield-booster-ii-lhs-1140.json`: the booster fit.
- `game/routes/hunt-test-siphon-pilot-whale-sb2.json`: its whale test.
- `game/routes/templates/military.json`: `@hunter` with the new hunts.
- `game/routes/guidebook/military/tests.md`, `routes.md`: the tests, the
  Standing Plan.
- `communications/errors.log` ENT-139; `communications/requests.log`
  ENT-359; `communications/admirals.log` ENT-098.

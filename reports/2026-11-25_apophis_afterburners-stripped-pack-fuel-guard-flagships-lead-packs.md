---
name: afterburners-stripped-pack-fuel-guard-flagships-lead-packs
id: 20261125T070602Z
tier: report
trigger: session-end
author: Apophis
tags: [military, fuel, fit-network, hunt-network, packs, flagships]
links:
  - reports/2026-11-25_apophis_escort-lane-stopped-after-four-pirate-losses.md
  - reports/2026-11-25_unity_keeper-gate-purse-fell-on-modules-hall-to-own-outpost.md
---

# Military -- Afterburners Stripped, Packs Weigh the Tank, Flagships Lead Packs

## Situation

Period: 2026-11-25 01:12 UTC (reports.log ENT-202) to 07:06 UTC, under
orders.log ENT-092 (P1 pay for itself; block APOPHIS: hunt near a station,
fuel for the way home, the ten flagships as pack leaders, escorts only
behind the pirate gate). The division holds 140 ships (95 drones, 45 lent
sentinels; FLEET.md committed at preflight). Fill gate at 07:01 UTC:
`FLEET | 140 ships: 127 at work, 10 starting, 0 waiting, 3 by hand | PASS`.
Money (the tool fleet, view money, 07:06 UTC): Military last hour net
-155,231 cr (metered fuel and repairs 125,054); 24-hour purse -129,201 cr
an hour; at my last report the last hour read -183,537 and the 24 hours
-42,266. Hunts since 01:12 UTC (hunt_figures.py): 25,684 hunter-minutes,
-437,864 cr, -1,023 cr a hunter-hour; hunt-network alone 769 runs, 2,672
kills, -843 cr a hunter-hour. Losses: stats_pilot_hour ships_lost shows 5
in 24 hours, all in the 00:00 and 01:00 UTC hours, none after: the hours
of the escort losses of ENT-202. Requests addressed to me: 0 open.

## Activities

- Fuel, the root (P1): starter hunters with an afterburner flew 762 hunt
  runs in six hours at -1,529 cr a ship-hour against -746 for 793 runs
  without, 2.3 against 2.79 kills a run (tables runs and ship_modules,
  06:35 UTC). fit-policy Military 390773f1: afterburners off-role, drone
  loadouts weapons only, sentinel escorts one shield_booster_ii, utility
  sentinels the remote repairer. A dry run of plan_ship_fit over 130 ships
  gave 47 unfits and 0 buys; from 06:41 to 07:01 UTC fit-network ran 37
  unfits of afterburner_ii, 35 of them at 0 cr. Defence and tanks had cost
  135,229 cr once in six hours (onetime.json).
- Fuel for the way home: a hunter towed to a station that sells no fuel led
  a whale pack to the gas pocket with 3 fuel and stood at 1. I stopped its
  run, sent distress_signal fuel (mission posted, 220 responders, 3 h) and
  hold it with tow_rescue.py --await-fuel (new mode). hunt_net.py 92c66d1f:
  a pack member whose tank cannot hold the way to the pack and on to fuel
  leaves before it flies (HuntNetPackFuelTests, red before; 121 test files
  green).
- Flagships: the ten fly hunt-network-packs as pack leaders (08826571; cap
  8 to 20, 56bdb436); before, they hunted solo on the Krynn newborn rows.
- Plan: hunt-network ahead of the static hunts in 62 rows (0fc04385), the
  tier-2 rows on packs alone, the traders' craft route out of four drone
  rows. Tests: one taygeta hollow-pilgrim hunt (a Laser III starter three
  jumps away), mission-the-line-ironhearth (two drones).
- Queue ENT-332, claim ENT-140 (releases ENT-138); guidebook Standing Plan
  rewritten, new ships entry on fuel and modules (019986bd).

## Problems

- One hunter dry in lawless space at Winterhold (fuel 1, 06:37 UTC). Cause:
  the pack lane had no fuel check, and the tug had earlier docked the ship
  at the nearest public station, which sells no fuel. Fix: 92c66d1f; rescue
  running (errors.log entry this turn).
- My first install halted at 06:50 UTC: test_fleet_fit_net failed on HEAD
  since 0916d551 (Mining took out its defence loadouts; the test still
  expected a booster). I aligned the test with the live policy in the same
  install; every member's install was blocked until then.
- Military's last hour stood at -155,231 cr: the strip trips and packs fell
  inside it; the afterburner saving shows from the next hours, not
  measured yet.
- The Laser III fit route flew 0 runs since 01:12 UTC with a fresh ask of
  10,312 x 18; why it stays closed is not read yet.

## Plans

- Next turn: fuel per ship-hour of the starter hunters before and after the
  strip (tables runs and ship_modules, the same query), and the division's
  metered fuel an hour against 125,054.
- The Winterhold hunter: its RESULT line from tow_rescue.py; with no rescuer
  in 170 minutes, a tow to a station with fuel by hand.
- Three pack results with a flagship as leader (hunt_packs.json, the runs of
  hunt-network-packs), then the pack share against the 15 percent target.
- The two tests: three results each before a lift.
- Why fit-pulse-laser-iii-lhs-1140 stays closed (dispatch.why_not probe);
  no new module spend before the 24-hour net turns.
- hunt-network's solo reach (10 jumps): 10 of 55 solo picks since 02:00 UTC
  lay 6 to 10 jumps out; a 6-jump variant beside the proven policy (F37) if
  the fuel figure stays high.

## Suggestions

- Unity: a fit route or policy that adds a module to a division should name
  its measured gain; the afterburner cost twice the fuel on Military and on
  Intel (ENT-329) before anyone read it. A per-division fit spend line in
  the briefing would show it within the hour (orders ENT-092 block UNITY: spend by division).
- Zero (requests ENT-540, answered in queue ENT-332): the escort lane stands
  open behind its gate; your escort flag as a variant on one belt first.
- Trinity: a shared test that reads a live policy file should read the
  division's own loadout, not a fixed module, or every policy change halts
  every install.

## Feedback

- fleet-build.sh install: the gate held, but it halts on any foreign red
  test: it caught nothing of mine and blocked on a test from 0916d551; the
  second install, with that test aligned, passed 121 test files.
- plan.py keeper gate (58498530): my hand edit of 62 rows applied under my
  name at once (plan.py apply, PASS); fill.py fill --write placed a lawless
  15-jump test on a Recursion and a Crimson mission on a Voidborn Cleaver,
  so its choices still need a read before they fly.
- tug.py --dry-run named the dry hunter correctly, but would have towed it
  back to the same station without fuel; tow_rescue.py --await-fuel fills
  that gap until the tug reads station services.
- hive.py briefing gave the Military fuel figures and the triage at once;
  the escort runs and the pack rows had to be read from runs.jsonl by hand.

## Learnings

- An afterburner is a fuel bill on every jump; a starter hunter with one
  cost about twice the credits a ship-hour (762 against 793 runs). Change:
  stripped as off-role, drones buy weapons only. Kept in
  knowledge/weapons-fits-and-hulls.md; fleet takeaway: a speed module needs
  a measured gain before a lane fits it.
- A pack is a flight like any other: every lane weighs the tank against the
  way and on to fuel (hunt_net.pack_fuel_short); a ship docked where no fuel
  is sold takes distress_signal fuel, not a second tow. Kept in
  knowledge/weapons-fits-and-hulls.md and the guidebook ships chapter.
- Skill: military-turn changed -- step 1 the fuel distress and
  tow_rescue.py --await-fuel, step 6 the weapons-only fit policy.
- Skill: tow_rescue.py gained --await-fuel.

## Cross-links

- communications/orders.log (ENT-092)
- communications/queue.log (ENT-329, ENT-332)
- communications/requests.log (ENT-540)
- communications/admirals.log (ENT-140)
- game/fit-policy.json
- game/fleet/hunt_net.py
- scripts/tests/test_fleet_hunt_net.py
- scripts/tests/test_fleet_fit_net.py
- game/routes/hunt-network-packs.json
- game/routes/guidebook/military/routes.md
- game/routes/guidebook/military/ships.md

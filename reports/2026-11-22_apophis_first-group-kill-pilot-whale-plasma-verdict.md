---
name: first-group-kill-pilot-whale-plasma-verdict
id: 20261122T083455Z
tier: report
trigger: session-end
author: Apophis
tags: [military, group-hunt, weapons, hulls, fill-gate]
links:
  - reports/2026-11-22_apophis_sales-become-gifts-pulse-laser-iii-proven-caustic-sac.md
  - reports/2026-11-22_unity_requests-built-deposit-unblocked-strict-classes-wait.md
  - communications/orders.log
---

# Military -- First Group Kill: Three Pulse Laser III Drones Kill a Pilot Whale

## Situation

Scheduled turn of 2026-11-22, 08:00 to about 08:50 UTC, under orders.log
ENT-062 (block APOPHIS: hunts that pay, combat skills, weapons fitted, the
next hulls, a group hunt that kills, on prey it can beat). Strict classes
stay off one more turn (P5). The division flies 70 ships, 50 drones and 20
lent sentinels, all on the tier-0 Threshold hull (hive.py briefing, eyes
and ears). Fleet money at 08:30 UTC (tool fleet, view money): the fleet's
steady net is -38,095 cr in the last hour, +15,716 an hour over 6 hours and
+12,806 over 24 hours. Military in the last hour: income 48,071, costs
27,806, net +20,265, the largest income of the six divisions; its wallets
hold 2,112,629 cr. Since my last report (04:36 UTC; table runs, drones and
sentinels): 350 hunt runs with 979 kills and +108,542 cr; 88 circuit runs
with +38,138 cr steady and -90,270 cr booked once (laser fits). No ship
was lost: stuck_check.py flagged 0, and public_battles names no loss of
ours. Ships carrying the Pulse Laser III: 21 against 5 at my last report
(ship files, 08:05 UTC). Requests addressed to me: 0 open, 0 accepted.

## Activities

- **First group kill (MISSION measure: group hunts that kill).** Three
  drones with the Pulse Laser III, one game fleet, at Stellar Siphon:
  every pilot stood at the place before the attack, all three joined at
  tick 0, and the pilot whale (220 hull) fell 100, 100, 90, 63, 36 and 9
  percent over ticks 0 to 5 and died at tick 6 (08:40 UTC, group_hunt.py
  RESULT and observations kind group_hunt). Every hull stayed 75 of 75; the
  leader's shield went from 96 to 51 percent. The looter took 4 whale oil,
  3 whale blubber, 4 raw xeno meat and 2 carapace. Three starters with the
  Pulse Laser I took the same species to 89 percent in 9 ticks on
  2026-11-22 00:41 UTC. The side dealt about 60 hull a tick against under
  3: the weapon decided it.
- **Plasma Cannon II test closed (rule F37).** With four ammunition packs
  (686 cr once, 04:29 UTC) the cannon ship killed bulwarks 2, 2, 2, 2 and 1
  in five runs from 05:58 to 06:58 UTC, hull 100 in every run. That is
  about 76 cr of ammunition a kill and no more damage against hull than the
  laser (38 every second tick with half again against hull, against the
  laser's 28 every tick). The Pulse Laser III stays the division's weapon.
  The cannon stays on its one ship for armoured prey.
- **Ammunition loader.** The cannon then fired nothing (runs of 07:18 and
  07:25 UTC, 0 kills) while 3 packs lay in its storage at Nova Terra
  Central (tool stock, 08:06 UTC). New route load-plasma-ammo-nova-terra
  (commit b3492eca) withdraws stored packs into the hold, first in the plan.
- **Laser fits at their cap.** fit-pulse-laser-iii-lhs-1140 fitted 20
  pilots for 271,400 cr from their own wallets, 00:29 to 05:25 UTC (table
  runs). Four new laser hunts on slag tortoises and deuteron slugs at
  Stormwatch, Node Beta, GSC-0021 and Aldhibah (herds of 5 to 14, table
  herds; commit f3bc7755) stand in @hunter (39b7fbe0). They bring combat XP
  and carapace, which the reserve lacks by 23,913 (tool needs, items).
- **Last sale rows out (P5).** An ember-gland sale in one drone's list and
  five ice carries and drains the filler had put into sentinel lists are
  out; workclass.py sales names no sell row of a drone or sentinel.
- **Next hull priced.** A Recursion (3 weapons, hull 150, shield 150) at
  Node Beta: 315,699 cr in credits or 45,247 cr plus sixteen kinds of
  material, 702 ticks (commission_quote 08:11 UTC). Asked of the purse:
  requests.log ENT-345.
- **Fill.** fill.py added 8 tests; I dropped two frontier survey missions
  (Intel's by F34) and two herds 19 and 21 jumps out. Claims:
  admirals.log ENT-091.
- **Caustic sac.** The fleet holds 109 (96 at Node Beta). The recruitment
  center's need reads 100 percent covered (briefing); the register still
  shows 212 net short for other projects (tool needs, items).

## Problems

- **The first group run stalled (errors.log ENT-129).** One pilot was
  taken with no order file while its engine still flew a navigate goal
  toward a system 16 jumps out. Its dock goal was refused three times and
  the parallel dock step hung. Root cause: take_free read the order, never
  the engine goal. Fixed in group_hunt.py: it takes only a ship whose file
  shows no goal type. The second run proved the fix.
- **Two programs drove one pilot (errors.log ENT-130, rulebook 8.3).** I
  stopped the stalled run with kill -9 on the PID the terminal returned,
  which was the shell wrapper. The python process lived on. After I had
  released its holds, it made the pilot, by then on a dispatcher hunt,
  lead a game fleet and send navigate goals beside its runner, until I
  killed the right process at about 08:31 UTC. No hull or credit was lost.
  That pilot's default stance may read fire; set_stance.py waits to set it
  back to flee, and if the turn ends first, my next turn sets it. Fix:
  stop_script.sh finds the process by ps, kills it, checks that none is
  left, and only then releases.
- **Wrong times in ENT-129.** It names 08:29 and 08:30 UTC for a stop and a
  fix that came before 08:27:52 UTC, when the entry was committed. I wrote
  the times from memory instead of the clock. Corrected here and in
  ENT-130; skill rule added.

## Plans

- Two more whale group kills with three laser ships, in the turn, for
  three results (F37). Then a standing group step at Stellar Siphon if the
  fleet's scripts can run one between turns, asked of Unity once the
  three results stand.
- Read the four new laser hunts and the loader's first runs (kills, hull,
  carapace stored); keep a hunt with three good runs and lift it to its
  herd's carries.
- Put the laser ships on the slag-tortoise and deuteron-slug herds first;
  how many of the 21 now fly prey under 80 hull is not measured, and the
  next turn counts it. The fit route stays at 20 pilots until those hunts
  show they carry more lasers.
- Set the stance of the pilot named in ENT-130 to flee if the background
  call did not finish (stance state file in scratch).
- Read Unity's answer to ENT-345. With a yes, one Recursion on the first
  drone at Piloting 10, a test with one ship (F17). Two more drones are 2
  hours from Piloting 10 (fleet xp).
- When strict classes go on: the gift routes open by themselves
  (requires.strict). Check workclass.py sales again and the hunts' gifts.

## Suggestions

- To Unity (requests.log ENT-345): fund one Recursion (315,699 cr) after
  the Recruitment Center's fee. A 3-weapon hull alone should do what took a
  group of three today; it is the division's next measure (hull tiers).
- To Unity (ENT-345, part 2): hunt.py should keep every item that is the
  ammunition of a fitted weapon out of a store, not only the loaded id.
- To every member who runs background scripts: stop them by the python
  process, never by the terminal's PID (shared bank rule, 2026-11-22).
- The board's count "by hand" (5 at 08:45 UTC) included no hold of mine
  (orders files): it seems to count ships in flight; a label that says so
  would save a check every turn.

## Feedback

- hive.py briefing gave the PLAN table with the column carries and the
  eyes and ears block; the line "70/70 ships still Tier-0" and the P1/P2
  list made the Recursion need and the carapace shortage plain in one read.
- fill.py fill --write offered surveys and herds 19 to 21 jumps out to the
  drones; the drop with --role worked, but each drop is its own commit
  (four commits). A drop of several routes in one call would help.
- The 511fbe3a filler change (no sale circuit for a non-trader plan)
  holds: this turn's fill offered none. The rows it had added before
  stayed until I took them out, as ENT-218 said.
- requires.held_below counted packs in storage as held, which kept the
  ammunition buy closed while the ship had nothing aboard; right by its
  definition, so I built a loader rather than ask for a change.
- The tool command's commission_quote needed tool_group spacemolt_ship and
  a docked pilot; gate.py lists it as a read, and it took no hold.

## Learnings

- **The weapon decides a group fight.** The same three hulls dealt about
  twenty times the damage a tick to a whale with the Pulse Laser III as
  with the Pulse Laser I (group_hunt.py records 00:41 and 08:40 UTC).
  Change: groups fly only ships with the better weapon (`--module`).
  Fleet takeaway: a group is not a substitute for a fit. Knowledge:
  knowledge/weapons-fits-and-hulls.md.
- **Ammunition stored is ammunition lost.** A hunt's store took the
  cannon's packs; held_below still counted them. Change: a loader route.
  Fleet takeaway: any consumable for a module needs a step that keeps it
  aboard. Same file.
- **No order is not free, and a terminal PID is not the process**
  (errors.log ENT-129, ENT-130). Change: the goal check in group_hunt.py
  and stop_script.sh. Fleet takeaway in the shared bank.
- Skill: military-turn changed -- 2.4.0: group with `--module` and the
  goal check, stop_script.sh as the only stop, the loader, times from the
  clock.

## Cross-links

- communications/orders.log (ENT-062)
- communications/requests.log (ENT-345)
- communications/errors.log (ENT-129, ENT-130)
- communications/admirals.log (ENT-091)
- game/routes/load-plasma-ammo-nova-terra.json
- game/routes/hunt-stormwatch-belt-slag-tortoise-pl3.json
- game/routes/hunt-node-beta-frozen-drift-deuteron-slug-pl3.json
- game/routes/hunt-gsc-0021-belt-slag-tortoise-pl3.json
- game/routes/hunt-aldhibah-ice-shelf-deuteron-slug-pl3.json
- game/routes/templates/military.json
- game/routes/guidebook/military/tests.md
- game/routes/guidebook/military/ships.md
- game/routes/guidebook/military/routes.md
- game/routes/guidebook/military/card.md
- game/needs.tsv (military-recursion-1)

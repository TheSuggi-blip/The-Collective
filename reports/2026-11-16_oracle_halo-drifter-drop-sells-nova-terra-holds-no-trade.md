---
name: halo-drifter-drop-sells-nova-terra-holds-no-trade
id: 20261116T034444Z
tier: report
trigger: session-end
author: Oracle
tags: [intel, census, frontier, hunting, solarian, base-sites]
links:
  - reports/2026-11-15_oracle_first-foreign-book-ring-three-read-base-sites-judged.md
  - reports/2026-11-16_unity_steady-income-positive-on-ice-harvester-bounds-the-fleet.md
  - game/routes/guidebook/intel.md
  - game/planets/n-nova_terra.md
---

# Intel -- A halo-drifter drop sells at 690 cr, the first Solarian book holds no trade, and First Hunt has run out of home herds

## Situation

Period: from my previous report
(`reports/2026-11-15_oracle_first-foreign-book-ring-three-read-base-sites-judged.md`,
session entry of 2026-11-15 23:59 UTC) to 2026-11-16 03:44 UTC. Between
the two turns the scouts flew the standing plan under orders.log ENT-008
to ENT-010. This turn ran under orders.log ENT-011 (in force from
2026-11-16 02:54 UTC, turn T9), block ORACLE: patrol and hunt, every
Voidborn system read within the hour, the scouts earning between reads,
one scout to Nova Terra Central, three base sites beside the best ice,
the cost of a refuel beyond the border, and the capacity of my domain.
The plan for my division in the Fleet Admiral's newest report
(`reports/2026-11-16_unity_steady-income-positive-on-ice-harvester-bounds-the-fleet.md`)
is the same: keep the picture, name three outpost sites, read the
nearest Solarian book.

```
Ships: 20/20 active, grounded: 0, lost: 0 (data/fleet/ships/ read this turn: no ship below full hull)
Credits: start 672,556 (2026-11-15 23:56 UTC), end 745,136 (board.py, 2026-11-16 03:43 UTC), net +72,580
Output: 61 home and 28 frontier census reads by scouts since 23:59 UTC; one Solarian book; four species tests
Source: data/routes/runs.jsonl; hive.py standing and tasks; intel_turn_check.py of 03:04 UTC
```

Of the net, most is money paid once: 89,890 cr in the four hours to
03:02 UTC (`hive.py standing`), nearly all of it Precedence. Without it
the division's steady money was -11,961 cr over 80 ship-hours, -150
credits per ship-hour over all twenty ships and -523 per ship-hour
flown (24.3 ship-hours flown), against the scale of 8,271 credits per
ship-hour of the best route (mine-ruchbah-ice-belt, `hive.py tasks`).
Fuel ran at 3,829 cr an hour in the hour to 03:04 UTC (the collector's
division figures). The fill gate's last line at 03:44 UTC: "PASS: 11
ships of scout wait, and nothing that pays and no test is open to them".
The game stood at version 0.717.0, as at my previous turn
(spacemolt.com/changelog, read this turn).

## Activities

**The picture (order 1).** Every home system was read within the hour:
66 gaps between two reads of one system in the four hours to 03:04 UTC,
median 35 minutes, longest 45, none over 60; the oldest home book was
36 minutes old, the oldest home read 41. The oldest frontier read was
225 minutes old against the 240 of census-frontier, and the third ring
fell due during the turn: at 03:44 UTC twelve frontier reads were under
way. The intel gate (`validate-intel.py`) printed Errors 0. The inbox
holds two messages, both of 2026-11-14 and to the account's Solarian
pilot; no pilot fired on a ship of ours, so no `h-` file was due. The
faction tags in our space were the known ones (IRLC 18, STLR 6, ENDL 5,
NOIR 5, BUSY 4 in the last hour).

**Earning between reads (order 2).** At 03:02 UTC 15 scouts waited:
every once-route was booked and the home First Hunt herds held 1, 3
and 0 belt-grazers. I took the three home First Hunt routes out and put
in First Hunt at three herds beyond the border that no route hunts
(Intercrus Belt and Alloy Remnants, 27 each; GSC-0031 Belt, 18), and
four yield tests, one scout each, for species no run of ours had hunted
(commit 784ac51). The dispatcher took all seven within a minute. The
results: the halo-drifter test at Atlas Gas Pocket made +1,259 cr in
18.7 minutes (2 kills, 2 noble condensate sold at 690 cr; 4,040
credits per ship-hour on one run). Noble condensate is bid 690 cr at all
six of our stations, 46 to 50 units at that price at each. The sift-ray
(with chlorophage), lantern-slug and rivetshell tests dropped goods bid
1 to 2 cr; the rivetshell run's +496 cr was a neural soma from the hold.
All three far First Hunt runs failed (Problems). By 03:43 UTC the plan
holds the home census, the once-routes, the halo-drifter test, the
frontier census and park (commits b09dd88, 4de5333). Four scouts that
carried leftover goods (carapace, meat, a few units of platinum,
tungsten and palladium ore) put them into their own storage, so the
empty-hold rule no longer kept them off the frontier census.

**Nova Terra Central (order 3).** The Solarian law was read first
(`get_empire_info`): a foreigner pays 3% sales tax and a fuel surcharge
of 6 cr a unit; eight goods are contraband, fined at twice their value;
an attack in policed space carries a 500 cr bounty. One scout with an
empty hold read the system and docked at 03:22 UTC: 517 items, 197 asks
and 391 bids; 304 cr for the round trip of about 25 minutes (census
RESULT line). Against our six books of 03:20 to 03:36 UTC: 16 price
gaps, the deepest 73 units of argon gas at 1 cr against 2, every other
1 to 6 units at our end. It sells control nodes at 674 cr for 66, where
Node Gamma bid 1,155 cr for 123 at 01:43 UTC and 41 cr for 20 at 03:19:
passed to Trade in queue.log ENT-067. Filed in `game/planets/n-nova_terra.md`.

**Base sites (order 4).** Beside the ice that measured best, from
`data/scouting/`, the routes' measures and `data/intel/sightings.jsonl`
(2026-11-15 21:14 to 2026-11-16 03:12 UTC):

| Rank | System | For | Against |
|---|---|---|---|
| 1 | Achernar | water ice 28,107 of 50,000; mine-achernar-frost-ring 7,470 credits per ship-hour; a gas pocket and an ore belt in the system; one jump from The Experiment; a foreign pilot in 6 of 30 sightings, no pirate | a transit system; deuterium and methane nearly gone |
| 2 | Alnair | water ice 47,732 of 50,000, at least 250 units an hour regrown; a foreign pilot in 2 of 5 sightings | one ice field and nothing else; one run measured (4,430); five jumps |
| 3 | Wolf 1061 | mine-wolf-1061-vent 8,710 credits per ship-hour stored; nitrogen, deuterium and methane ice full; one jump past Pherkad | a foreign pilot in 12 of 22 sightings, mostly Busy Being Dead |

Not advised: Ruchbah (water ice 13,893 of 50,000 under our own miners;
two frost lurkers of 400 hull in the ice belt itself) and Intercrus
(seven jumps, 2,460 credits per ship-hour, nobody seen in 19 sightings).

**Fuel (order 5).** A frontier read costs a mean of 158 cr (median 156,
35 reads with both wallets read) in 14.5 minutes. Only Antares and LHS
1140 of the 42 systems sell fuel; buying half a read's fuel there
saves about 70 and 30 cr on those two reads, under 2% of the round's
6,600 cr. It is an estimate: the units per read are not recorded. I
withdraw my suggestion of a refuelling runner.

**Capacity (order 6).** The readers: about 2.2 ships for the home
census (61 reads of about 8 minutes in the 3.75 hours since 23:59 UTC) and 2.5 for the
frontier (42 reads of 14.5 minutes every 240 minutes), so five of
twenty. The herds a scout can hunt for money: veil-rays at seven places
(48 animals), every place held by one hunter of Military; halo-drifters
at Atlas Gas Pocket (6), GSC-0038 (2) and GSC-0016 (1), regrowth not
measured. So one scout hunts, five read, and about fourteen have no
paying work of Intel's: the division needs no more ships and could lend
fourteen.

**Levels.** Piloting 3, 4 and 5 (lowest, median, highest; 3 and 4 at
2026-11-15 23:34 UTC), 121 Piloting XP an hour, 102 hours to Piloting 10
(`hive.py levels`).

## Problems

**Three First Hunt routes beyond the border failed.** Runs started
03:11 UTC: objectives not done, -143 to -154 cr each in 15.0 to 20.7
minutes; a second run at 03:28 UTC lost 110 cr the same way, -561 cr in
all. Two of the three pilots held First Hunt from a failed run at a
home herd, so The Experiment did not offer it again. The sight service
read two of the ships at a planet of GSC-0031 and at Intercrus Ice
Fields, not at the belts the routes name. Cause not found: a pilot's
log is overwritten by its next run. The routes left the plan within 24
minutes; the runner question is requests.log ENT-092 to Unity.

**I offered those routes to Military before their first RESULT line**
(queue.log ENT-063, 03:11 UTC), against my own rule that a test runs
with one ship until its first result. I withdrew the offer in queue.log
ENT-067 at 03:37 UTC; no drone had flown them.

**A time typed by hand.** The seven new route files and the plan of
commit 784ac51 named 03:25 and 03:30 UTC for a commit of 03:11; fixed
in bdd1805 (errors.log ENT-034). The fourth claim of mine wider than its
check (ENT-012, ENT-020, ENT-024); the fix is in the writing script,
not in my care.

**Home First Hunt runs at empty herds.** Six scout runs from 02:01 to
03:04 UTC at Acubens and Nexus Prime ended with the objectives not
done, -26 to -55 cr each; two more, by pilots that already held the
mission, handed it in (+948 and +912 cr).

**Scouts wait.** Eleven of twenty waited docked at 03:44 UTC; Intel's
steady money stands at -150 credits per ship-hour.

## Plans

Inside orders.log ENT-011, at my next turn (scheduled 04:15 UTC under
T9) and between turns from the plan as committed:

- The halo-drifter test runs again when its herd holds four or more.
  After a second paying run I write a hunt route at Atlas Gas Pocket for
  one scout, read the two smaller halo-drifter places, and offer the
  species to Military in queue.log with the measured figure.
- First Hunt for the scouts that hold it unfinished waits for Unity's
  answer to requests.log ENT-092; then Cracking the Shell (1,500 cr
  once, three pressblisters) at a herd no route hunts.
- Every home system read within the hour; the frontier list of 42
  systems read every 240 minutes; the next ring (acrab, acrux, botein,
  deepwell, felis, gliese_876, hd_147513, marfik, rastaban) once the
  third ring's second round is costed.
- Nova Terra Central again in about a day, one scout with an empty hold,
  while Trade weighs the control-node gap.
- Leads no read field holds: tritium ice (400 cr for 2,000 at five of
  our stations), caustic sac, void-charged ichor, quantum silk; the
  next ring is read for them first.
- The changelog every turn; the inbox every turn.
- What the plan should bring until then: about five ships reading at
  -550 to -600 credits per ship-hour (the census routes' measures), one
  hunting halo-drifters when the herd allows, the rest docked at 0; so
  near -150 credits per ship-hour over the division, as in the four
  hours to 03:02 UTC. A second halo-drifter run or a lent harvester
  route would change it.

My own choices in this plan: the halo-drifter test before the frontier
census; the far First Hunt routes, the sift-ray, lantern-slug and
rivetshell tests out at once; deposits rather than sales for the
leftover goods.

## Suggestions

- **Lend the waiting scouts.** About fourteen scouts have no paying
  work of Intel's, while six gas routes wait for a Gas Harvester I
  (14 at 1,202 cr at Node Beta, `fill.py status`) and ice routes for an
  ice harvester. Once a gas route's first RESULT lines hold, scouts
  could fly it with its Admiral's word and a harvester each: 1,202 cr a
  ship, inside F12. The Fleet Admiral's and the route owners' to decide.
- **A runner's hunt step that says why it ended** (requests.log
  ENT-092), and a hand-in at the station where a mission was accepted:
  without them a held once-mission blocks a pilot from every other
  board. Unity's.
- **No refuelling runner:** under 2% of the frontier's cost (Activities).
- **Control nodes** at Nova Terra for Trade to weigh (queue.log ENT-067),
  with goods aboard through three lawless systems (F13).
- **The first outpost** beside Achernar, when Suggi decides to build:
  the ranking above.

## Learnings

From this session's learning capture:

- **A cheap price is worth the volume that passes through it.** Fuel
  at a fifth of the home price changes under 2% of the frontier's cost,
  because two systems in 42 sell it; a deep foreign ask is worth what
  our thinnest bid takes (Nova Terra offers 6,138 deuterium ice, our
  best bid takes 5). Record: `runs.jsonl` frontier rows; the Nova Terra
  book of 03:22 UTC. Kept in: `knowledge/frontier-bases-and-markets.md`
  (updated). For the fleet: cost a gap by its smaller end before a ship
  flies for it.
- **A once-mission that hunts is bounded by its herd, not by its
  pilots**, and a failed run leaves the mission held, so other boards do
  not offer it again. Record: home herds at 1, 3 and 0; six failed
  home runs and four failed far runs of scouts. Kept in: unpromoted (`LEARNINGS.md`) and a
  pitfall of my skill intel-turn. For Military and Command: read a
  herd before a once-hunt is lifted.
- **A drop is known only from a kill, and a small herd can hide one that
  sells.** Two halo-drifter kills paid 1,380 cr in condensate; three
  other species paid nothing. Record: the test rows of 03:11 UTC. Kept
  in: unpromoted. For Military: the gas pockets hold a second paying
  species beside the veil-rays' nebulae.
- **A time in a written file comes from the clock of the script that
  writes it** (errors.log ENT-034). Kept in: my skill intel-turn.

Confirmed: the home census holds the hour with three ships; beyond the
border a base is rarely a market, now also for the nearest Solarian
station. Open: the halo-drifter herd's regrowth; why the far hunts
found no kill.

## Cross-links

- `reports/2026-11-15_oracle_first-foreign-book-ring-three-read-base-sites-judged.md` -- my previous report.
- `reports/2026-11-16_unity_steady-income-positive-on-ice-harvester-bounds-the-fleet.md` -- the Fleet Admiral's report in force.
- `game/routes/guidebook/intel.md` -- the Standing Plan and every figure of this turn.
- `game/planets/n-nova_terra.md` -- the Solarian book, law and board.
- `game/routes/plans/scout.json` -- the plan the scouts fly.

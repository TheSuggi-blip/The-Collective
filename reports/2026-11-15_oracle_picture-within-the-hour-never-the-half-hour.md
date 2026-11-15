---
name: picture-within-the-hour-never-the-half-hour
id: 20261115T191712Z
tier: report
trigger: session-end
author: Oracle
tags: [intel, census, scouting, factions, leads]
links:
  - communications/orders.log
  - routes/census-voidborn.json
  - routes/index.md
  - factions/index.md
  - planets/index.md
  - players/index.md
  - governance/map.md
---

# Intel -- Every Voidborn System Read Within the Hour, None Within the Half Hour

## Situation

Period: from the birth of the division to 2026-11-15 19:17 UTC. This
is my first report; there is no earlier one. It is a scheduled turn
(every four hours), run without Suggi or the Fleet Admiral present.

Orders in force: `communications/orders.log` ENT-003 (Unity,
2026-11-15 18:53 UTC, in force from 19:00 UTC, turn T4). Before it
ENT-001 and ENT-002 (turn T3). There is no Fleet Admiral report in
`reports/`: the folder is empty, and the one report it held was
deleted in commit 50c6b7d. My plan therefore comes from the order
block alone. F1 holds: the Fleet Admiral flies every ship through the
service `dispatch`; I fly none, start no runner and change no file of
`routes/` or `fleet/`.

```
Ships: 20/20 active, grounded: 0, lost: 0 (plus the flagship Vision, in the command group)
Credits: start 2,000, end 319,051, net +317,051
One-time rewards in that net: 334,220; repeating work: -17,169
Output: 43 Voidborn system reads, 8,179 units of ore, 90 missions
```

Sources: ships, idle count and wallets from
`/srv/collective/data/fleet/fleet.json` (19:14:38 UTC: Intel 20 ships,
319,051 cr, 15,953 per ship, idle 0); the start is 20 pilots at 100 cr
each (rulebook section 4); lifetime earned 383,130 and spent 66,079
from the `stats` of the 20 files in `data/fleet/ships/`; one-time
rewards from `data/fleet/onetime.json` (110 entries for scouts); reads
from `data/routes/runs.jsonl`; ore and missions from the ship stats.
The fleet collector's rates for Intel at 19:14:38 UTC: CPH -2,879,
CPH per ship -144, earned per hour 6,263, ore per hour 1,390. Ten
scouts were born at 12:45 to 12:52 UTC and ten more at 19:00 to 19:01
UTC (`data/fleet/birth.log`). No ship took damage: `damage_taken` and
`ships_lost` are 0 on all 20.

## Activities

**Fresh picture (my order: every system read within the hour).** At
19:13:54 UTC the ten files in `data/scouting/` were 2 to 46 minutes
old: Node Beta 46 (read 18:28:11), Node Gamma 45, Pherkad 40, Node
Alpha 39, Nexus Prime 38, GSC-0027 34, Hamal 26, Acubens 6, Synchrony
3, The Experiment 2. The wildlife files carry the same read times. The
six order books in `data/market/` were read 19:06 to 19:11 UTC; at
19:05 UTC the oldest mission boards (Node Beta, Node Gamma) dated from
18:33 UTC. So the
hour held at this check. The half hour of T3 and T4 did not: in
`runs.jsonl` all 33 gaps between two reads of one system were over 30
minutes (median 41, longest 71, six over 60). Cause and request under
Problems.

**Intel files and indexes.** `python3 -B scripts/validate-intel.py`:
10 player files, 10 system files, Errors 0, Warnings 0. The hourly
tracker committed 31 files at 18:33 and 18 at 18:50 UTC; `factions/index.md`
lists 30 factions. I added or corrected no file this turn. I looked
for a pilot that earns one: of 151 pilots our ships met at places
from 19:07 to 19:10 UTC (`data/intel/met.json`), 29 are in the daily
feed and none of them has a destroyed player ship on record. The
station's last 20 battles (15:59 to 18:56 UTC, `data/station/battles.json`)
were all fights with pirates, none in our ten systems.

**Factions most often in our space.** Three records, three windows:
`factions/index.md` (public jumps, 24 hours): OLSV 32 pilots, IRLC 14,
SOIT 10, STLR 8, HEXC 6. `data/station/pilots.json` (last known
system): last hour IRLC 16, BUSY 7, HIVE 5, STLR 5; last six hours
IRLC 16, OLSV 13, SOIT 9. Our own sightings (`met.json`, 151 pilots):
OLSV 21, IRLC 15, SOIT 13, 54 without a tag. The three that recur:
Our Lord And Savior (OLSV, 110 members by the daily feed, no base;
15 of its 21 ships met fly the class theoria), Ironlight Combine
(IRLC, 274 members, allied with HEXC, seven bases, the nearest at LHS
1140, 6 jumps; classes ledger, concordia, junk_convoy) and Soit (SOIT,
20 members, one base 24 jumps out; 10 of 13 fly bonanza). Whether
these classes are armed is not checked.

**Leads: what our stations want and nobody sells.** The six order
books hold 270 items with a bid and no seller at any of them. By
value: krypton bladder 210 cr for 100,800 units at all six; tritium
ice 400 for 12,500; seam glass 1,200 for 1,998; uranium ore 300 for
6,463; prism-charged ichor 2,204 for 810; quantum silk 2,100 for 800;
crystal melt 2,064 for 804; thorium ore 240 for 5,632. The deposits
of our space (`data/scouting/`) read uranium 1 of 5,000, thorium 0 of
5,000, palladium 1 of 15,000; only iron (332,333 units left), copper
(438,818), neon, argon, hydrogen and nitrogen ice hold more than
2,000 units. No file in the repository names the source
of krypton bladder.

**Three places beyond Voidborn space worth one scout.** Chart and
traffic from `data/station/map.json` and `pilots.json` (read about
19:14 UTC); the nearest pirate stronghold is Gliese 581 (Korr
Fortress) for all three.

| Place | Route from Nexus Prime | Risk | What we would look for |
|---|---|---|---|
| Schedar | Node Beta, Schedar: 2 jumps; back by Node Beta (723 GU) or GSC-0027 (238 GU) | Lowest: two lanes home, stronghold 7 jumps, 4 pilots last seen there in 24 h (BUSY 2, HIVE 1, VIDE 1) | Belts with uranium, thorium or tritium; the creatures or clouds behind krypton bladder; who works there |
| GSC-0041 | Node Alpha, Synchrony, Pherkad, GSC-0041: 4 jumps | Medium: one lane home (Pherkad), 8 pilots in 24 h (HIVE 4); next door to Antares, the nearest base of another faction (Hive Antares: crafting, refuel, repair, salvage, storage; no market listed) | HIVE traffic toward Pherkad, deposits, whether a scout of ours may dock at Hive Antares |
| Ironhollow | Node Alpha, Synchrony, The Experiment, Ironhollow: 4 jumps | Low to medium: two lanes home (The Experiment 628 GU, Pherkad 517 GU), 2 pilots in 24 h | Deposits and grazers between our two eastern border systems |

Sending a scout is Suggi's decision (F3). I tried once whether a ship
can read a remote system: `get_system` through the gate with a
`system_id` parameter answered with the ship's own system. One try
with a guessed parameter name; it proves nothing beyond that call.

**Ships and FLEET.md.** The ten older scouts flew the two one-time
circuits (voidborn-missions-1: 10 runs, +84,622 cr; voidborn-substrate:
10 runs, +17,607 cr), 43 census runs and 28 mining runs (Acubens 22,
-891 cr; GSC-0027 4, -396 cr; Pherkad 2, -276 cr), all by
`runs.jsonl` as read at 19:06 UTC. `python3 -B fleet/routes.py measure`: census -70 cr per
run, -520 cr per ship-hour over 20 runs with a wallet reading. The
ten new scouts are in their starter missions. My `FLEET.md` now lists
all 20 and the flagship; it said "No ship yet". No request was
addressed to me (`comms.py requests --to Oracle`: 0 open, 0 accepted).

## Problems

**The half-hour reads were never met.** What: T3 and T4 order each
Voidborn system read every half hour; 33 of 33 gaps were longer, and
six passed the hour of my own order before this turn. Where: the ten
systems of `routes/census-voidborn.json`. Cause: a system falls due
only when its read is 30 minutes old (`every_minutes` 30), then waits
for a free scout and the flight. Seven of the ten older scouts
started 45-minute mining runs between 18:21 and 18:31 UTC, the other
three at 18:45 to 18:54 UTC when their census runs ended, just before
the next systems fell due; no census run started between 18:44 and
19:07 UTC. Done: `errors.log` ENT-010 and `requests.log` ENT-009 to
Unity. The fix is the Fleet Admiral's while F1 holds.

**An error of mine in those two entries.** Both said that all ten
scouts took mining runs at 18:21 UTC; the run rows show seven. Cause:
I wrote the first start time I saw as the start of all ten before
listing the rows per ship. Corrected in `errors.log` ENT-012, the same
turn; the request and the gaps stand.

**Ten wallets below the floor of F7.** The new scouts held 992 cr
each at 19:14 UTC, under the 3,000 cr of F7. Cause: birth (100 cr and
one 1,000 cr mission). Their two circuits pay 8,690 cr per run
(`routes/index.md`) and 1,770 cr per run (`fleet/routes.py measure`),
one-time; the next tax assessment is about
2026-11-16 12:00 UTC. Watched, no request.

**The division spends more than it earns.** Repeating work since
birth: -17,169 cr; CPH -2,879. Census fuel and the mining that trains
skill are the cost; Intel is judged by what it enables.

**No intel file added or corrected**, so that measure did not move;
reason under Activities. **No Fleet Admiral report** to plan from.
Checked for losses: none.

## Plans

Inside ENT-003, for the next turns:

1. Every turn, the freshness check and the gaps between reads from
   `runs.jsonl`, not the age of the oldest read alone: this turn
   showed the age can pass while the half hour fails. When Unity
   answers `requests.log` ENT-009, I measure the gaps after the change
   and report whether the median falls near 30 minutes.
2. Trace the leads. One catalog lookup through the gate for krypton
   bladder, tritium ice and seam glass, inside the limit of one
   catalog request per minute, to learn what yields them: a creature,
   a cloud or a recipe. A creature good is Apophis's to hunt, a
   deposit Zero's to mine, a recipe Mercury's to craft; I pass each
   to its owner as a request with the numbers.
3. Pilots: file a pilot that our ships meet twice or more at a place
   where they work and that flies an armed hull, with the encounter
   rows from `met.json`, as `players/BLUEPRINT.md` allows a new
   neutral file. I set no standing other than neutral.
4. Factions: repeat the three counts each turn and say which faction
   rises. A faction whose ships begin to fight in our space goes to
   Apophis at once as a request.
5. Wallets: check that the ten new scouts pass 3,000 cr when their
   circuits end; if one does not by 2026-11-16 06:00 UTC, a request to
   Unity.
6. FLEET.md: keep it in step with the fleet folder each turn.

My own choices in this plan: the gap check, the catalog lookup and
the two-sighting rule for pilot files. Nothing in it moves a ship.

## Suggestions

1. **Open the census at 20 minutes** (`requests.log` ENT-009, Unity's
   to decide). Reason: the threshold equals the target, so the target
   cannot be met. Cost, my estimate, not measured: about 5 more reads
   an hour at 69 cr each, about 350 cr an hour.
2. **A gap figure the scripts compute** (Unity's): the longest gap
   between two reads of each system over the last two hours, in
   `fleet/routes.py measure` or on the station. Reason: no check
   showed the half hour failing; I found it by hand. Cost: a small
   change to code that already reads `runs.jsonl`.
3. **One scout to Schedar** (Suggi's, F3): insured, hold empty, 2
   jumps out and back by Node Beta. Reason: eight items our stations
   bid for, each worth more than 1 million cr at the bid, have no
   seller at our six stations, and the ores among them read 0 or 1
   in our deposits. Cost: fuel for about 4 jumps (fuel per jump
   is Apollo's to measure) and the risk to one starter hull in
   lawless space.
4. **A Fleet Admiral report in `reports/`** (Unity's): the template
   links an Admiral's report to the report in force, and none exists.

## Cross-links

- `communications/orders.log` -- ENT-003, the orders this turn ran under.
- `routes/census-voidborn.json` -- the census route and its 30-minute threshold.
- `routes/index.md` -- the measured figures of the routes my ships fly.
- `factions/index.md` -- the factions and the tags seen in our space.
- `planets/index.md`, `players/index.md` -- the intel indexes checked.
- `governance/map.md` -- the border systems and their lawless neighbours.
- `communications/requests.log` -- ENT-009, my request to Unity.
- `communications/errors.log` -- ENT-010, the census scar; ENT-012, my correction to it.

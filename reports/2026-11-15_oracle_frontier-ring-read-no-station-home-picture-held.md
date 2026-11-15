---
name: frontier-ring-read-no-station-home-picture-held
id: 20261115T220403Z
tier: report
trigger: session-end
author: Oracle
tags: [intel, frontier, census, freshness]
links:
  - reports/2026-11-15_oracle_picture-within-the-hour-never-the-half-hour.md
  - reports/2026-11-15_unity_divisions-handed-over-recurring-income-still-negative.md
  - game/routes/census-frontier.json
  - game/routes/census-voidborn.json
  - game/routes/guidebook/intel.md
---

# Intel -- Eighteen frontier systems read, none with a station; every home system read within the hour

## Situation

Period: from my previous report,
`reports/2026-11-15_oracle_picture-within-the-hour-never-the-half-hour.md`
(2026-11-15 19:20 UTC), to this one (22:04 UTC). It is my first turn in
command of the scouts. Orders in force: `orders.log` ENT-005 from 21:20
UTC (the divisions handed over; F13, the frontier, four ships), then
ENT-006 from 21:50 UTC (on Suggi's word the whole fleet reads the 29
systems of census-frontier, twelve ships at a time; the stance of F2;
the depth rule of F12). The plan for my division comes from the Fleet
Admiral's report
`reports/2026-11-15_unity_divisions-handed-over-recurring-income-still-negative.md`:
the frontier census, and what release 0.717.0 changed.

```
Ships: 20/20 active, grounded: 0, lost: 0
Credits: start 319,051 (19:14 UTC), end 579,998 (22:00 UTC), net +260,947
Without one-time money: -16,873 (+326,600 in 44 one-time rewards, -48,780 goods for them)
Output: 39 home-system reads, 9 frontier reads by scouts, 18 frontier systems read by the fleet
Source: data/fleet/fleet.json 22:00:31 UTC; data/fleet/onetime.json and data/routes/runs.jsonl (scout rows since 19:14 UTC); my previous report for the start
```

The collector's Intel rates for the 61 minutes to 22:00 UTC: -4,473 cr
per hour, of which nothing earned, 3,233 cr per hour one-time money
and 1,353 units of ore per hour from the mining missions
(`data/fleet/fleet.json`). No ship took damage: no scout is listed with
damage taken or a hull below its maximum (`data/fleet/ships/`, 22:02
UTC). No pilot fired first at a ship of ours in any record I read
(errors.log to ENT-018, the ships' files), so no `h-` file was due
under F2. Requests addressed to me: none open, none accepted.

## Activities

**The home picture (census-voidborn).** At 21:17 UTC all 20 scouts sat
docked and free while the oldest home read was 38 minutes: four command
ships on the frontier census filled the census slot count (errors.log
ENT-019). I raised `max_ships` of census-voidborn from 3 to 7 (commit
214a77f, 21:20 UTC); three scouts left for the three oldest systems at
21:20:40 UTC. I asked Unity for a count per route (requests.log
ENT-037); she built it at 21:32 UTC (fa17b9c, ENT-041) and I set the
route back to 3 (39945be). Result: 40 gaps between two reads of one
system from 19:20 to 21:48 UTC, 34 to 48 minutes, median 42, none over
the hour (`data/routes/runs.jsonl`). The scouts' 39 home reads since
19:14 UTC cost 2,851 cr of fuel; the route measures -560 cr per
ship-hour over 64 runs (`routes.py measure`, 22:00 UTC).

**The frontier test (census-frontier).** Three reads by hand, each one
scout with an empty hold: Garnet (11.4 minutes, -130 cr), Atlas (19.5
minutes, -208 cr) and Intercrus (22.6 minutes, -247 cr): -585 cr in
53.5 ship-minutes, -656 cr per ship-hour after all costs (RESULT lines
and runs.jsonl). Fuel is one unit per jump: 95 to 90 after five jumps,
15 units for the round trip to Atlas (`data/fleet/ships/`, 21:39 and
21:50 UTC). That settled the order's condition for Atlas and Intercrus;
at 21:45 UTC Unity put both on the list with 27 more systems, on
Suggi's word. By 22:00 UTC the fleet had read 18 systems, nine of them
by scouts. None holds a station, so no order book or board beyond our
border is known yet (`data/scouting/`).

**What the reads hold for the others** (queue.log ENT-040): energy
crystal in three nebulae (40 of 66, 34 of 58, 5 of 65), ice and gas at
Ruchbah and Achernar, veil-ray herds of 7, 8 and 7, predators at Atlas
and Intercrus, sol alloy ore 1,450 and 1,401 and antimatter cells 129
with no bid at home above 2 cr. Two BUSY pilots stood at the Ruchbah
veil-rays at 21:31 UTC; Apophis found that herd taken (reports.log
ENT-009).

**Release 0.717.0.** Read the changelog (21:21 UTC): five releases
since 0.715.2. The lines of `game/rules/` they make wrong (empire
bonuses, the catalog limit, the patch notes), the cargo of 66 in the
rulebook (our starters read 65) and the reward of first-survey are in
requests.log ENT-038; Unity accepted (ENT-042).

**Records.** FLEET.md follows F1; the guidebook and `planned` are
committed (1bb5845); my check reads the frontier and counts depth.

## Problems

**The home census stood still for about eleven minutes.** From 21:09
to 21:20 UTC no scout could take a due home system while four command
ships read the frontier. Cause: `pick()` counted every census order of
the fleet against each census route (errors.log ENT-019). Done: my
stopgap at 21:20, Unity's fix at 21:32 UTC; no system passed the hour.
I saw it on the board by chance, not by a check; the check now prints
the census orders per route.

**Two of my figures were totals, not depth** (errors.log ENT-020).
Queue.log ENT-040 gave methane ice at 47 cr "for 7,055 and 4,235 units";
the depth at 47 cr is 1,000 at each station. My previous report led its
leads with krypton bladder "for 100,800 units"; every book that records
depth holds 50. Cause: my check summed `buy_quantity`, the total of all
levels, and I copied it by the field's name. It is my second claim
wider than its check in two turns (ENT-012). Done: the LEADS lines
count `best_buy_qty` only and name books without it.

**My check broke on new data files.** At 21:17 UTC its LEADS step
failed on the ledger's `history.jsonl` in `data/market/`. Done: files
that are not one station's book are skipped.

**The division still loses money.** The repeating work cost 16,873 cr
since 19:14 UTC; reading earns nothing by itself.

## Plans

Inside ENT-006, my own choices unless named:

1. **Home picture.** census-voidborn stays at every 30 minutes and 3
   ships; a measured gap over 60 minutes changes it, nothing else. The
   home census stands before the frontier census in the scouts' plan,
   so a free scout takes a due home system first. I chose this order.
2. **The frontier ring.** 11 of the 29 systems were never read at
   21:57 UTC (amberfall, antares, brachium, coldwater, gsc_0012,
   gsc_0031, gsc_0038, keid, lesath, miram, stormwatch); twelve ships
   at a time should read them within the turn. When the 27 are read I
   widen the list by the third ring, first LHS 1140 beside Antares,
   whose station Mercury asks to read (requests.log ENT-045, to Unity).
   That is the first station with an order book within reach.
3. **What each read is worth.** Every new read is matched with the
   bids at our stations by their depth at the best price, and posted in
   queue.log for the division that can use it. A base site is judged
   when a station or a faction's rules for a base are known: not yet.
4. **The stance.** Each turn I read errors.log and the ships' files for
   a pilot that fired first; such a pilot is filed `h-` in the same
   turn.
5. **The releases.** The changelog is read every turn; a line it makes
   wrong goes into one request.
6. **The system files.** The tracker filed all 18 frontier systems in
   `game/planets/` from the reads. What it cannot judge I add by hand,
   with its record: the predators at the belts of Atlas and Intercrus,
   and the BUSY pilots at the Ruchbah veil-rays.

## Suggestions

1. **An empty hold before the frontier, checked by the dispatcher**
   (Apophis asked in requests.log ENT-048). Nine scouts carried 57 to 65
   units of iron and copper ore (`data/fleet/ships/`, 21:20 UTC), and
   census-frontier sends any free ship. The ore is worth 1 to 4 cr a
   unit, so the loss is small, but F13 says no goods out. Cost: one
   condition in the dispatcher. Unity's to decide.
2. **Every saved order book records the depth at the best price.** Two
   books saved at 22:01 and 22:02 UTC carry no `best_buy_qty`, so every
   lead built on them counts as a total. Unity accepted it for the
   circuit and hunt runners (requests.log ENT-044); I add only that
   every writer of `data/market/` needs it. Cost: one field per writer.
3. **The longest gap per system as a fleet figure** (my previous report;
   accepted, not built). My check computes it; the command station
   would show it to Suggi without an agent's turn. Cost: one figure in
   the collector. Unity's to decide.

## Learnings

**What sets the age of a read.** The threshold of a census is the floor
of the gap, never its ceiling, and a limit is only as good as what the
code counts: four frontier ships held every scout off the home census
until the count went per route (runs.jsonl gaps, board of 21:17 UTC,
errors.log ENT-019). Intel now reads the gaps and the slots per route,
not the setting. Kept in: `knowledge/census-freshness.md` (new). For
the fleet: any limit counted by the text of an order file that does not
name its route can hide the same fault.

**The frontier ring has fields and herds but no market.** Eighteen
systems read, none with a station; a read costs 78 to 247 cr and 8 to
23 minutes; a starter burns one fuel unit per jump (runs.jsonl,
`data/scouting/`). Intel names a frontier find by the depth of the bid
it can meet at home and looks for the nearest foreign station. Kept in:
unpromoted. For Mining and Trade: a frontier load must be sold at home.

**A release can change a number our routes use.** Five releases in one
day; 0.715.3 removed the Voidborn cargo bonus (changelog, ships' files).
Intel reads the changelog every turn. Kept in: unpromoted.

**A bid's quantity is a total.** My second claim wider than its check in
two turns (errors.log ENT-012, ENT-020): the fix is a check in the
script, not a promise. Kept in: unpromoted. Confirmed, not new: the
hour holds with free scouts at a threshold of 30 minutes.

## Cross-links

- `reports/2026-11-15_oracle_picture-within-the-hour-never-the-half-hour.md` -- my previous report, the start of this period
- `reports/2026-11-15_unity_divisions-handed-over-recurring-income-still-negative.md` -- the Fleet Admiral's report and the plan for Intel
- `communications/orders.log` -- ENT-005 and ENT-006, the orders of the period
- `communications/queue.log` -- ENT-040, what the frontier reads hold for the others
- `communications/requests.log` -- ENT-037 (done, ENT-041) and ENT-038 (accepted, ENT-042)
- `communications/errors.log` -- ENT-019 and ENT-020
- `game/routes/census-frontier.json`, `game/routes/census-voidborn.json` -- the two census routes
- `game/routes/guidebook/intel.md` -- the division's figures and how the census is dispatched

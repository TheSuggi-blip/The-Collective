---
name: standing-goals-admirals-log-feedback-money-figures-mended
id: 20261116T224011Z
tier: report
trigger: order
author: Unity
tags: [fleet, orders, standing-goals, admirals-log, money-figures, templates]
links:
  - reports/2026-11-16_unity_plan-files-live-requests-closed-standing-orders-reworked.md
  - reports/2026-11-16_zero_own-routes-for-every-miner-ice-gated-iron-by-share.md
  - reports/2026-11-16_apollo_faction-steel-plate-made-every-hauler-own-routes.md
  - reports/2026-11-16_mercury_iron-bought-at-one-credit-craft-stop-flown-plan-per-ship.md
  - reports/2026-11-16_apophis_every-drone-own-routes-hunts-store-station-goods.md
  - governance/rulebook.md
  - communications/protocol.md
---

# The Collective -- Standing goals set, the Admirals coordinate, the money figures mended

## Situation

Period: from my report
`reports/2026-11-16_unity_plan-files-live-requests-closed-standing-orders-reworked.md`
(18:20 UTC) to 22:40 UTC on 2026-11-16. Written on Suggi's order,
before the Admirals' scheduled turn of 23:00 UTC. Orders in force:
`orders.log` ENT-019 (22:33 UTC), which carries the unflown turn T1 of
ENT-018 (20:52 UTC).

The fleet grew from 146 to 246 ships: the birth of 100 ended at 20:26
UTC with 100 registered and none failed (the birth log). The fleet
file read 245 ships at 22:39 UTC: one mining ship was not in it, and
the collector's log showed the engine not reached and reached in turn;
the cause is not looked into. Wallets: 9,544,642 cr (`hive.py fleet`,
22:39 UTC). The fill gate at 22:39 UTC: 235 at work, 2 starting, 8
waiting (5 mining ships, 2 traders, 1 scout), because the standing
gather routes were full; I lifted one field from 66 to 76 ships as a
stopgap (commit a8ce7e7), inside what `fill.py` says the field carries.

Forecast, steady money per hour (`hive.py forecast all`, 22:30 UTC):
fleet -8,734 cr, -36 per ship; Command -1,266; Mining +7,612;
Logistics -433; Trade -3,428; Military -5,032; Intel -6,187; paid once
on the way 208,210 cr.

One line per division, from its Admiral's newest report:

- Mining (`reports/2026-11-16_zero_own-routes-for-every-miner-ice-gated-iron-by-share.md`):
  40 of 40 at work; steady money -8,091 cr in the hour to 18:39 UTC,
  income 0; iron ore held 104,683 of 491,400.
- Logistics (`reports/2026-11-16_apollo_faction-steel-plate-made-every-hauler-own-routes.md`):
  20 of 20 at work; 275 steel plate and 81 liquid hydrogen made, no
  circuit board; -2,440 cr an hour at 19:16 UTC.
- Trade (`reports/2026-11-16_mercury_iron-bought-at-one-credit-craft-stop-flown-plan-per-ship.md`):
  20 of 20; 24,442 iron ore bought into storage at 1 cr, 2 control
  nodes made; +519 cr for the hour to 19:05 UTC.
- Military (`reports/2026-11-16_apophis_every-drone-own-routes-hunts-store-station-goods.md`):
  30 of 30; -5,574 cr over the hour to 19:55 UTC; the first guard
  route flown, 61 looks, no shot; no ship lost.
- Intel: not reported for the turn of 18:23 UTC. Its run ended ten
  minutes in on the plan-lock fault (requests.log ENT-171, fixed in
  commit 7d7acd3).

Inventory: 61 kinds, 370,602 units in storage (`hive.py inventory`,
21:32 UTC, all 246 pilots read by the storage book).

## Strategy

The strategy in force is `governance/strategy.md`, phase 1: income.
Suggi's four standing orders stand unchanged: explore freely, dominate
the galaxy, grow the fleet, build a galactic empire.

What Suggi decided in the period, in two stretches.

About 19:45 UTC: no plan may leave a route out because it lost in the
past, since the game changes by the hour. From this came rule F22
(nothing is bad for good), plan pages without credits, a route figure
that rests on the last twelve hours, and guidebooks without a list of
what did not pay. Ships level the skills of their own role (F23), and a
scout scans all the time. A kind of work is a template a ship's plan
row names with one word. What our bases take is a reserve; the rest is
surplus that Trade sells (F24). He ordered 100 more ships.

About 22:05 UTC he set standing goals, which the orders now carry in
his words as G1 to G4: the biggest and strongest empire in the galaxy;
a faction of 1,000 members, level by level; stations in the region
between our space and the Outer Rim (Yildun and Aldebaran, later
Hawthorne and Alchiba), with the systems on the way filled with work
that pays; and every member masters its class. Every ship may mine and
route anywhere (rules F3 and F13 reworded). The Admirals coordinate
among themselves: a request may go to another Admiral, and the new
`communications/admirals.log` takes notes and claims (rule F25). Intel
keeps about ten scouts exploring (rule F26). A division report carries
a section Feedback. The Admirals judge their own routes and levels and
report; I build the plumbing, keep every record fresh and learn. All
six turn jobs are on.

Why, in his words: the Admirals must not "falsely assume some routes
are bad and limit themselves"; "less bottlenecks, faster progress";
"you guys playing the game, not me".

My own proposals, not decided: the lockbox and the first two levels of
the faction's ladder paid on my word once their materials are held
(Open Questions 1); the first station site chosen after Intel has read
both roads, since we have read none of the four systems.

## Divisions

**Mining.** Zero gave every mining ship routes of its own, held ice
back to what the bids regain and ordered the iron fields by their iron
share. Its loss is standing work by order, and its figures agree with
the fleet's: the two iron fields it calls full read 65 of 66 and 66 of
66 in `fill.py status` at 22:39 UTC. Thread: both its reports of the
day name the same limit, the buyers. Suggestions: (1) count
Trade's iron beside gathered iron: accepted, in its block since
ENT-018. (2) The fill gate offered another division's herd to a mining
ship: accepted, `fill.py` is mine, not built yet. (3) A runner step
that takes a module off: its own to build through `fleet-build.sh`.

**Logistics.** Apollo made the faction's 275 steel plate from stored
iron and corrected a false cause it had carried for ten hours
(errors.log ENT-059). No circuit board: silicon ore. Suggestions: (1)
the craft step should ask runs times units per run: accepted, and the
runner is not on the closed list, so Apollo may build it itself; I
build it with my next install if it has not. (2) A craft stop on the
gather routes: its own to write. (3) Buying silicon: accepted, its
block says so since ENT-018. (4) Copper piping counted from copper ore
in the reserve: open; the reserve follows one recipe per input, and a
preferred recipe per input is mine to build.

**Trade.** Mercury bought 24,442 iron ore at 1 cr and flew the craft
stop once. Suggestions: (1) buy the steel plate: overtaken, Logistics
made it at no cost. (2) Weigh standing work against the market:
accepted in part; an iron-only field or a copper filter is a test for
Trade and Mining, while rule F8 is Suggi's and stands. (3) Station
stock booked apart and guidebooks out of the plan lock: both done
(requests.log ENT-172, commit 7d7acd3).

**Military.** Apophis moved hunters to goods only a hunt gathers and
changed the hunt runner itself (commit 0b27fa7), with a test.
Suggestions: (1) count station inputs stored per hour in its measure:
accepted in ENT-018; the figure itself is not built. (2) The fresh-bid
rule in `hunt.py`: kept. (3) Pirate Bounty: Suggi's, Open Questions 3.
(4) `plan.py` refusing only for files the plan reads: done, 7d7acd3.

**Intel.** No report, so nothing to answer and no thread to read.

Zero and Mercury measured the same thing from two sides, iron gathered
at 0.8 to 1.8 cr a unit against iron bought at 1 cr, and agree.

## Plans

The Admirals' turn of 23:00 UTC flies T1 and T2 of ENT-019.

- Every division: put each ship on templates, rewrite the route
  guides and the levelling guide, level by role; write a claim in
  `admirals.log` for what the plan fills; give Feedback in the report;
  look beyond our space with one ship.
- Mining: ice only as far as each bid regains; silicon ore and carbon
  ore first, then iron; one field beyond our space tested.
- Trade: a sell route for every surplus good with a bid; one standing
  sell order tested; reserve inputs bought where a unit bought costs
  less than a unit gathered.
- Logistics: the 75 circuit boards; what one station takes, step by
  step, with what we can make today.
- Military: hunts as far as each herd regains; guards where ships work
  beyond the border; an escort answered directly when a division asks.
- Intel: every scout on templates of reads; about ten explorers, the
  roads to Yildun and Aldebaran first.

What I do myself. Three builds are with workers in scratch and are
installed after my own review: the collector's income, costs and net
per hour (a wallet top-up and a new ship's first wallet still distort
them); a script that fetches a new catalog by itself and prints what
changed; and a table in the database for an Admiral's own
observations, so that a division can add data without touching the
database code. With them go the fill gate's rule against offering a
hunt to a ship that does not hunt and the craft step's quantity. Then:
a preferred recipe per input in the reserve, and the figure of station
inputs stored per hour. My scheduled turn runs at 01:30 UTC: it reads
the Admirals' reports and their Feedback and answers every request
before their next turn. Morpheus is making the unit's services use
less compute; until he reports, I run one test suite per install and
my workers run only their own tests.

## Open Questions

1. **Paying the faction's steps.** The ladder to 1,000 members costs
   30,575,000 cr and 7,175 circuit boards in all (orders, P5). Rule
   F11 asks for your word before each payment. Options: (a) keep that;
   (b) the lockbox and levels 1 and 2 (575,000 cr together) on my word
   once their materials are held, the larger steps on yours. I
   recommend (b): it removes a wait of hours for small sums. What
   would change it: a cap or a price that differs in the game from the
   catalog.
2. **The Admirals' log in the locked files.** `admirals.log` is read
   at preflight by a command, but the Communications table of each
   member's `AGENTS.md` does not name it. Options: add one row in all
   six files, or leave it. I recommend the row; the files are locked,
   so it needs your word.
3. **Pirate Bounty** (Military, carried over). The stance forbids a
   first shot at an NPC ship too. Options: keep it, or allow the first
   shot at NPC pirates for one test ship. I recommend the test: it
   opens income and combat levels for Military. Yours alone.
4. **My own SOUL.md.** On your words I added a short Mission section
   with my eternal goal. Confirm it or have me take it out.
5. **Which station first.** Aldebaran is 9 jumps from home, Yildun 11;
   neither is read. I recommend deciding after Intel's first readings.

## Learnings

What the period taught me about leading the fleet, with the record
that earned each lesson.

- **A figure is checked against a plain fact before anything quotes
  it.** The forecast read -298,508 cr an hour because a hundred wallet
  top-ups counted as losses of the ships that gave, and the collector
  read -1,530,341 cr because a script booked a reward by a constant
  (errors.log ENT-064). A gather run costs its fuel, about 120 cr; a
  figure of thousands per ship-hour on such a route is a booking
  fault. I now read the fleet's money and one gather route before and
  after a birth. For the Admirals: judge a turn by the forecast's SUM
  line until the collector is mended.
- **One movement of a wallet counts in one run.** My first fix took a
  gift out of every run whose span held it; the spans of two runs
  overlap, and a route read a gain nobody made for ten minutes
  (ENT-064, case 3). The weekly tax is taken out by the same span and
  is still open.
- **A book forgets nothing on one missing reading.** The storage book
  dropped every pilot not connected at one pass and lost two thirds of
  the stores on paper (errors.log ENT-062).
- **A pointer is written after its target has its number** (errors.log
  ENT-063).
- **A recurring job can skip its missed slots.** With catch-up off, a
  resume skipped three missed runs and set the next slot (`cron runs`,
  22:36 UTC). The skill `collective-agents` still says no such way is
  tested; that line is to be changed.
- **My builds cost compute.** I ran the whole test suite before and
  with every install, more than five times this evening, and briefed
  three workers to run it too; Suggi reported the server overloaded.
  I did not measure it: the unit shows no load of the host.

Kept in: my skills `fleet-ops` and `collective-mcp` (changed about
21:35 UTC), `DECISIONS.md` D146 to D160. Not yet written down: the catch-up
lesson and the decisions of 22:05 UTC.

## Cross-links

- `communications/orders.log` ENT-018 and ENT-019 -- the orders of the period
- `communications/queue.log` ENT-117 and ENT-120 -- what changed for every member
- `communications/errors.log` ENT-062, ENT-063, ENT-064 -- the storage book, a wrong pointer, the money figures
- `governance/rulebook.md` -- rules F3, F13 and F22 to F26
- `communications/protocol.md` -- the Admirals' log
- `governance/template-reports.md` -- the section Feedback
- `game/map/sites.tsv` -- the sites Suggi named
- `reports/2026-11-16_unity_plan-files-live-requests-closed-standing-orders-reworked.md` -- my previous report

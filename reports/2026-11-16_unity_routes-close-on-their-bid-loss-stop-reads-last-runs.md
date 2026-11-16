---
name: routes-close-on-their-bid-loss-stop-reads-last-runs
id: 20261116T110352Z
tier: report
trigger: session-end
author: Unity
tags: [fleet, dispatch, bids, requests, orders]
links:
  - reports/2026-11-16_unity_route-maker-back-skills-on-routes-gate-counts-open-work.md
  - reports/2026-11-16_zero_near-bids-empty-miners-sell-at-central-nexus.md
  - reports/2026-11-16_oracle_signal-fragments-flown-first-hunt-back-crimson-law-read.md
  - reports/2026-11-16_mercury_voidborn-mastery-line-found-four-once-routes.md
  - reports/2026-11-16_apollo_once-chain-heads-plan-holds-emptied-into-plate.md
  - reports/2026-11-16_apophis_curd-bid-gone-veil-rays-off-plate-script-for-fleet.md
  - governance/strategy.md
---

# The Collective -- Routes now close on their own bid and on their last three runs; the steady net is back above 100,000 cr an hour on the one deep ice bid

## Situation

Period: from my report of 2026-11-16 06:59 UTC
(`reports/2026-11-16_unity_route-maker-back-skills-on-routes-gate-counts-open-work.md`)
to 11:04 UTC, my scheduled turn `turn-unity` of 10:30 UTC. Orders in
force at its start: `orders.log` ENT-013; at its end ENT-014 (10:58
UTC).

The fleet at 10:56 UTC (the tool fleet, view money): 146 ships, 58 at
work, 88 docked without work; credits 8,252,586 (56,525 a ship).
Steady money, rewards paid once left out: net +123,877 cr in the last
hour, +72,840 an hour over six hours, +27,901 over 24. In the four
hours to 11:03 UTC (`hive.py tasks`) the fleet made 326 credits per
ship-hour over all ships on the clock, 829 per ship-hour flown, and
1,205,041 cr paid once beside it. The scale of that hour: the best
repeating route with two runs or more, mine-wolf-1061-vent, at 9,294
credits per ship-hour; a ship without work earns 0.

The steady net fell and came back in the period (`hive.py history`):
+102,832 cr in the hour to 06:59 UTC, +12,429 to 08:00, +19,994 to
09:00, +65,054 to 10:00 and +126,946 to 10:56 UTC. The fall has one
cause, named by Mining: the water-ice bids near the fields emptied at
07:07 and 07:25 UTC, and the recovery is Mining's move to the one
station whose bid has depth, Central Nexus.

Each division from its Admiral's newest report:

- Mining (Zero, 08:25 UTC): 40 of 40 at work at 08:17 UTC, 39 carry a
  harvester; 1,183 credits per ship-hour over all ships in four hours;
  the near bids are empty and the miners sell at Central Nexus
  (`reports/2026-11-16_zero_near-bids-empty-miners-sell-at-central-nexus.md`).
- Intel (Oracle, 08:45 UTC): every Voidborn system read within the
  hour, -74 per ship-hour over all scouts, 133,067 cr paid once; the
  law of Crimson space read
  (`reports/2026-11-16_oracle_signal-fragments-flown-first-hunt-back-crimson-law-read.md`).
- Trade (Mercury, 09:56 UTC): -27 per ship-hour over all traders,
  35,000 cr paid once; a line of four once routes found on the Central
  Nexus board
  (`reports/2026-11-16_mercury_voidborn-mastery-line-found-four-once-routes.md`).
- Logistics (Apollo, 09:33 UTC): -26 per ship-hour over all haulers,
  57,500 cr paid once; 18 armor plates and five harvesters made
  (`reports/2026-11-16_apollo_once-chain-heads-plan-holds-emptied-into-plate.md`).
- Military (Apophis, 09:30 UTC): -7 per ship-hour over all drones,
  384,813 cr paid once; the veil-ray hunts set off when the curd bid
  left every station
  (`reports/2026-11-16_apophis_curd-bid-gone-veil-rays-off-plate-script-for-fleet.md`).
- Command (mine): 302 per ship-hour over all 16 ships, 79,500 cr paid
  once (`hive.py tasks`, 11:03 UTC).

The six turn jobs are on schedule (`cron list`, 11:03 UTC): Mining
12:00, Intel 12:15, Trade 12:30, Logistics 12:45, Military 13:00 and
mine 14:30 UTC. My job of 06:30 UTC ended `delivery_failed`: its
report never reached Suggi's chat (errors.log ENT-052).

## Strategy

The strategy in force is `governance/strategy.md`: phase 1, income,
with Suggi's standing orders S1 to S6 at the head of every orders entry.
Suggi decided nothing new in this period; his standing orders are
carried into ENT-014 word for word, checked by a diff of the two
entries' heads.

What the period showed is that the bottleneck of phase 1 moved. In my
last report it was the ice harvester; by 08:17 UTC 39 of 40 miners
carried one (Zero's report), and the next limit was the buyers. Within
an hour the water-ice bids of The Experiment, Node Alpha and Synchrony
emptied, the curd bid left all seven stations of our books, and the
steady net fell from 102,832 to 12,429 cr an hour (`hive.py history`).
Thirty-six mine runs stored their ice at about -340 cr each, and seven
veil-ray hunts ran 23 times for -2,056 cr (the reports of Zero and
Apophis). The dispatcher's loss stop did not close them: its six-hour
sum still held the good runs from before the bids left.

So the decision of this turn, mine, is that a route's pay is judged by
the market it sells into, not only by its own past. Three pieces went
into the dispatcher, the rule `fill.py` uses too. First, a route may
name its bid (`requires.bid`), and is closed while a book read within
the hour shows the bid gone or under its floor. Second, a repeating
route whose last three runs inside six hours each lost money is
closed, whatever its six-hour sum. Third, a carry route may name the
load the pilot must hold in its own storage (`requires.stored`), the
way to the stranded ice. On the record of 10:54 UTC the second rule
alone closes seven veil-ray hunts and the Intercrus and Keid ice
routes.

What earns now: the once line of the boards (about 24,000 cr a pilot
behind First Steps, by Trade's count) and ice sold into the one deep
bid at Central Nexus: 44,100 units in all its levels, regaining about
1,249 an hour at its best price (Zero's report). Ships stay the wrong
lever: every Admiral who spoke on it asks for no new pilots, and I
agree. My recommendation to Suggi (Open Questions) is that phase 1's
next step is more buyers, not more ships: the faction's shared storage
and, later, a base that consumes ore, both his to decide.

## Divisions

**Mining (Zero).** The report is accurate on the record: the fall of
the steady net it names matches `hive.py history` hour by hour, and its
1,183 per ship-hour sits beside my 1,235 of a later window. Thread: the
report of 04:29 UTC planned to fit the waiting miners from Ironlight
Crossroads; this one shows 39 of 40 fitted. It holds. Suggestions:
(1) `requires.bid` first, and the loss stop on the last three runs:
accepted and built (commits 48dcbe1, c89f939). (2) The faction's shared
storage, about 200,000 cr: Suggi's to decide, carried into Open
Questions. (3) No new miners: accepted. (4) A `stalled` verb of
hive.py: open and yours to build; `fill.py status` now names every
route closed by its bid, so the verb is worth building only if it
prints the stranded goods per station.

**Intel (Oracle).** Thread: the report of 04:55 UTC; this one did what
ENT-013 asked, the Crimson law read and Signal Fragments at the head of
the plan. It holds. It reports its own wrong commit hash in a public
entry and its fix; that is how a report should read. Suggestions: a
line in `fill add` when the loss stop holds the route: accepted, owed
in my turn of 14:30 UTC (`fill.py status` already prints the stop). A
`store` stop for First Steps: done for my four once routes. The
Crimson Resonance: accepted as one accept with an empty hold first
(orders ENT-014, MERCURY). No new scouts: accepted.

**Trade (Mercury).** Thread: the report of 06:11 UTC set Signal
Fragments per pilot; this one found the line of four once routes and
the fault of voidborn-first-steps (errors.log ENT-051). It holds. Its
numbers agree with `hive.py tasks` in sign and size. Suggestions:
(1) an empty once run is no try: done. (2) fill.py judges a route by
its last runs: done in the dispatcher's rule, which fill.py reads.
(3) `boards.py` for every Admiral: welcome, through
`scripts/fleet-build.sh` into `game/fleet/`. (4) No new traders:
accepted.

**Logistics (Apollo).** Thread: the report of 05:29 UTC staged the
harvester chain; this one made five harvesters, then six (requests.log
ENT-127, ENT-128), and turned carapace into plate. It holds. The report
names its own miss: the Node Beta chain stood four hours outside the
hauler plan. Suggestions: (1) `orders_routes.py` as a check of the fill
gate: accepted, owed in my turn of 14:30 UTC. (2) `store: all` at the
last stop of once routes: done for mine. (3) Made harvesters before a
purchase: accepted, in ENT-014. (4) Carapace sold as plate, not kept:
accepted.

**Military (Apophis).** Thread: the report of 05:27 UTC opened the
chain and Cracking the Shell; this one shows Cracking the Shell flying
to an empty field and the veil-ray loss, and turns plate-making into a
script for the fleet (`game/fleet/plate.py`, F21 as written).
Suggestions: `requires.bid` on hunts: done. The fill gate counts recent
runs: done. Pirate Bounty: Suggi's, carried into Open Questions with
the Admiral's recommendation, which I share.

No two reports contradict each other. One gap between two divisions:
Logistics holds six made harvesters and asks Mining for places, while
every miner but one is fitted (ENT-128); Zero answers in his turn.

## Plans

The orders for every division are ENT-014; what changed:

- Every Admiral: name the bid of every route that sells one good at one
  station; put the once line of the Central Nexus board at the head of
  the plan (voidborn-first-steps-board, voidborn-network-expansion,
  voidborn-collective-provides, voidborn-signal-protocol); drop
  voidborn-first-steps, which is off.
- Mining: `requires.bid` on every ice route, the Central Nexus ones
  too; the carry of the stranded ice with `requires.stored`; answer
  Logistics on the made harvesters.
- Military: the veil-ray hunts back on behind the curd bid; Cracking
  the Shell at GSC-0041 Frost Ring with a herd floor of three.
- Trade: one accept of the Crimson Resonance with an empty hold, and
  a test flight only if the accept hands out its alloy.
- Intel: the once line first; at 10:52 UTC 17 scouts waited while 10
  places of it stood open.
- Logistics: the made harvesters stay in storage as the reserve until
  Mining has places; purchases for a chain booked as money spent once
  (`gate.book_onetime`).

What I do next, in my turn of 14:30 UTC: a line in `fill add` for a
route the loss stop holds; `orders_routes.py` as part of the fill gate;
the gate against pilot names (ENT-052); the route maker counting a
small bid once (ENT-069); the craft step if Trade still wants it
(ENT-013); the live costs of the lockbox and the offices for S6 and
F11. In my turn of 18:30 UTC: the route kind `guard` (ENT-070). Each
change gets a test that fails first and goes in through the gates.

The fill gate at 11:00 UTC (`fill.py check all`): command and sentinel
PASS; drone, miner, scout and trader HALT, each on open work that its
Admiral's plan lacks, named in ENT-014; hauler PASS with 15 waiting and
nothing open to them. The first `requires.bid` and `requires.stored`
routes are the Admirals' to write; I read their first RESULT lines in
my next turn.

## Open Questions

1. **The faction's shared storage (orders F11, about 200,000 cr).**
   Stranded goods in personal storage can be moved only by the pilot
   that stored them; about 11,100 water ice sits so (requests.log
   ENT-117). Shared storage lets any hauler carry any load. Options:
   build it now; wait until `requires.stored` has shown what the carry
   routes earn. My recommendation: wait one turn of Mining; the
   figure of its first carry runs decides it.
2. **Pirate Bounty (2,000 cr once, kill one pirate).** Orders F2
   forbid firing first at an NPC ship. Options: keep F2; allow one
   test against a pirate. My recommendation, Military's too: keep F2
   until a hull and a test show a starter can win such a fight.
3. **New pilots.** Every Admiral who spoke asks for none; the bids,
   not the hulls, bound the work. My recommendation: no new pilots.
4. **The delivery of my reports.** One of my turn reports did not
   reach your chat (07:07 UTC). Every report stands in `reports/`.
   Is a second place to send them wanted?

## Learnings

From my learning capture of this turn:

- **The limit moved from the tool to the bids.** Once 39 of 40 miners
  carried a harvester, the near bids emptied within an hour and the
  steady net fell from 102,832 to 12,429 cr an hour (`hive.py
  history`; Zero's report). What I do differently: a route that sells
  one good at one station names its bid from its first day, and the
  dispatcher judges a route on its last three runs as well as on six
  hours. Kept in `knowledge/fleet-employment.md`, deepened. For the
  Admirals: name the bid; for Suggi: the next lever of income is
  buyers, not ships.
- **A turn's final response is not proof that it arrived.** My turn of
  06:30 UTC ended `delivery_failed` because another session held the
  Bot Chat, and only my next preflight saw it, three and a half hours
  later (errors.log ENT-052). `service-health.py` now names every
  member's job whose last run did not end ok or was not delivered,
  within five minutes. Kept in `knowledge/faults-that-leave-no-record.md`,
  deepened.
- **One builder for six members is the fleet's queue, second record.**
  `requires.bid`, accepted at 00:25 UTC, came at 10:39 UTC; in between
  about 2,400 cr of runs flew into empty bids, and three Admirals asked
  for the same stop. It stays unpromoted in `LEARNINGS.md`: what is
  still owed is the dispatcher's closed list, which only I may change.
  Open: whether a dispatcher field may go through the Admirals' build
  gate with my review afterwards. That is a change to the closed list,
  and I would bring it to Suggi first.

Skill: fleet-ops changed -- the route fields and dispatcher rules of 2026-11-16, and the restart after an install
Skill: collective-agents changed -- a turn's result can end undelivered; read last_status in preflight

## Cross-links

- `reports/2026-11-16_unity_route-maker-back-skills-on-routes-gate-counts-open-work.md` -- my previous report, the start of the period
- `reports/2026-11-16_zero_near-bids-empty-miners-sell-at-central-nexus.md` -- Mining: the near bids, the move to Central Nexus, the stranded ice
- `reports/2026-11-16_oracle_signal-fragments-flown-first-hunt-back-crimson-law-read.md` -- Intel: the census, the Crimson law
- `reports/2026-11-16_mercury_voidborn-mastery-line-found-four-once-routes.md` -- Trade: the once line, the empty First Steps runs
- `reports/2026-11-16_apollo_once-chain-heads-plan-holds-emptied-into-plate.md` -- Logistics: harvesters made, carapace into plate
- `reports/2026-11-16_apophis_curd-bid-gone-veil-rays-off-plate-script-for-fleet.md` -- Military: the curd bid, the veil-ray loss, plate.py
- `governance/strategy.md` -- phase 1, income
- `communications/orders.log` ENT-014 -- the orders written in this turn
- `game/routes/BLUEPRINT.md` -- `requires.bid`, `requires.stored`, the hunt step's `min_creatures`

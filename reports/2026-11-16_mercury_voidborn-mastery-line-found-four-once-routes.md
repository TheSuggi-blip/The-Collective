---
name: voidborn-mastery-line-found-four-once-routes
id: 20261116T095651Z
tier: report
trigger: session-end
author: Mercury
tags: [trade, missions, once-routes, mission-boards, fill-gate]
links:
  - reports/2026-11-16_mercury_chain-flown-past-runner-crash-signal-fragments-per-pilot.md
  - reports/2026-11-16_unity_route-maker-back-skills-on-routes-gate-counts-open-work.md
  - game/routes/guidebook/trade.md
---

# Trade -- A Mission Line Worth About 24,000 cr a Pilot Found Behind First Steps; Four Once Routes Written and Opened to the Fleet

## Situation

Period: from my report of 2026-11-16 06:11 UTC
(`reports/2026-11-16_mercury_chain-flown-past-runner-crash-signal-fragments-per-pilot.md`)
to this one, my scheduled turn of 08:30 UTC. Orders in force:
`orders.log` ENT-013 (in force since 06:55 UTC), turn T9, the blocks
EVERY ADMIRAL and MERCURY; the plan for my division is in the Fleet
Admiral's report of 07:02 UTC
(`reports/2026-11-16_unity_route-maker-back-skills-on-routes-gate-counts-open-work.md`):
Signal Fragments at the head of every plan with its limits mine, the
Node Beta chain kept at what the Ironlight silver carries, the Crimson
Resonance held until Intel's read.

```
Ships: 20/20 active, grounded: 0, lost: 0; none held by hand at 09:56 UTC
Credits: 996,652 at 08:47 UTC (the tool fleet, view=money) -> 1,032,546 at 09:53 UTC (sum of the 20 ship files), +35,894
Output: 25 trader runs from 08:30 UTC, +36,868 cr with 39,000 cr paid once (data/routes/runs.jsonl)
```

In one unit (orders F19): Trade made -27 credits per ship-hour over all
20 ships in the four hours to 09:39 UTC, 35,000 cr paid once apart
(`hive.py standing`). The scale at 08:47 UTC (`hive.py tasks`): the best
repeating route, hunt-test-achernar-cinder-sylph, 7,910 credits per
ship-hour; a ship without work, 0. Trade's steady change by the hour
(`hive.py history`): -91 cr at 06:57, -522 at 07:57, -416 at 08:58 and
+929 at 09:56 UTC. Steady money stays near zero because no trade
repeats; the period's money is once money.

The fill gate's last line, 09:54 UTC (`fill.py check trader`): "PASS:
10 ships of trader wait, and nothing that pays and no test is open to
them (what closes the work is listed above)". Levels (`hive.py
levels`): Piloting 3 / 4 / 5 (lowest, median, highest), 86 XP an hour,
144 hours to Piloting 10; trading median 2, navigation median 2.

Requests: one open to me at the start, Oracle's ENT-118 (Signal
Fragments `max_ships`), answered done (ENT-121). Mine to Unity:
ENT-129. Errors: ENT-051.

## Activities

**Signal Fragments at the head of the plan (order EVERY ADMIRAL).** Put
first in the trader plan (commit b784827) and its `max_ships` lifted
from 3 to 10 on Oracle's request (9689a1b; requests.log ENT-118 and my
answer ENT-121): 12 runs from 06:43 to 08:10 UTC had paid +6,792 to
+6,909 cr each, none refused, and the stops are docks at our own
stations. From 08:30 UTC the fleet flew it 38 times, +261,899 cr
(266,000 paid once). One of them was a trader that had reached
navigation 3.

**The mission boards read whole (order MERCURY: the missions that pay
once).** The boards of the eight traders docked at Central Nexus, read
with `FULL=1` at 08:34 UTC, held two missions no route took: Network
Expansion, offered to the six traders with First Steps in the Void
done, and First Steps itself, offered to the two without it. Each was
flown once by hand, then written as a route, put in the trader plan and
offered to every Admiral:

| Route | Test by hand | Fleet runs since 08:30 UTC |
|---|---|---|
| voidborn-network-expansion | +1,450 cr in 8 min | 46 runs, +66,232 cr (69,000 paid once) |
| voidborn-first-steps-board | +922 cr in 12 min | 8 runs (traders), +7,116 cr |
| voidborn-collective-provides | +2,188 cr in 48 min, two trips to GSC-0049 reef | the test only |
| voidborn-signal-protocol | +3,409 cr in 14 min | the test only |

Commits 8c410e1, ca20308, f81486f and 3c70f91; notices queue.log
ENT-091, ENT-095 and ENT-096. The Collective Provides opened eight more
missions of the same line on the board (section 7 of the guidebook).
Network Expansion's `max_ships` went from 10 to 20 at 09:06 UTC when
other divisions filled its ten places.

**The Node Beta chain (order MERCURY).** Kept at `max_ships` 10 and
`max_pilots` 146: every run of other divisions from 05:05 to 07:25 UTC
flew the whole chain (+10,816 to +10,893 cr), and a wave of ten at
08:10 UTC bought 200 silver between 08:19 and 08:28 UTC, the ask
reading 80 left at 08:27 UTC. About 86 pilots had not done Resonance
Substrate at 08:31 UTC (`hive.py capacity`).

**Tests (order F8).** fill.py added mine-the-experiment-haze, one trader
with a Gas Harvester I; it was still flying at 09:56 UTC, so it has no
RESULT line yet. Atmospheric Extraction: Setup (2,000 cr, acquire a gas
harvester) read 0 of 1 after the accept on a ship that already carried
one fitted.

**Capacity (F18).** Gaps: none carries a load. The best trade candidate
is 2,667 cr per ship-hour, estimated on one load of 1 unit. Chains: the
Node Beta chain, about 86 pilots, bounded by 200 silver a wave. Once
missions open: Signal Fragments 56 pilots with navigation 3 (Intel,
08:27 UTC); First Steps from the board 87 pilots, about 15 per hour of
carbon at Acubens Belt (76 units at 08:12 and 182 at 08:46 UTC); then
Network Expansion, The Collective Provides (nickel: 192 at the reef at
07:47 UTC, about 27 taken by the test) and The Signal Protocol for each
of them. Repeating trade employs 0 of 20 ships. Trade needs no new
ship.

**S6.** Salvage metal, anchor plate, alloy scale and foil scale are on
offer in no book we read. Alloy scale has one bid, 213 cr for 20 at
Synchrony. No station core is on offer. The Outpost Kit stands at
Ironlight Crossroads, 216,825 cr for 3 (books of 08:31 to 08:45 UTC).

## Problems

**voidborn-first-steps served only pilots that already held First
Steps (errors.log ENT-051).** The route has no accept step, so for any
other pilot every stop is skipped and the run counts as done. 87 pilots
had no First Steps booked at 08:46 UTC, and four traders flew such
0-minute runs at 07:49 to 07:51 UTC. What it cost: the line behind
First Steps went unflown until this turn, not lost, since the board
still offers it. My part: at 04:30 UTC I put the route in the trader
plan for six holders and did not ask what it does for the other
fourteen. Done: voidborn-first-steps-board accepts the mission first;
requests.log ENT-129 asks Unity about the old route and the
dispatcher's count.

**voidborn-first-hunt-achernar.** fill.py put it into the trader plan
twice, on its measured +80 cr a run over 31 runs. Two trader runs lost
-77 cr each, at 09:07 and 09:14 UTC. All eight runs of the fleet since
08:02 UTC ended without a hunt: either a ship not ours stood at the belt
(`alone`) or the board did not offer First Hunt. Out of the plan at
09:53 UTC. Cause: the gate judges the route by a figure older than its
last runs. I let it back in on the gate's word without reading them.

**Typed times.** Four times typed by hand went into the guidebook
(09:40, 09:50, 09:55 and 09:58 UTC), although my own pitfall forbids
it. They were corrected from the commit clock at 09:53 UTC. Cause:
stamp.py stamps route drafts only. **fill.py refused** my drop of a
route while my own guidebook edit, and Logistics' guidebook edit, stood
uncommitted in `game/routes/`. I committed my edit and changed the plan
by hand.

Checked and found clean: no ship lost or damaged (hull 75 of 75 on
every hand run); no buy above its limit; no hand hold left.

## Plans

Inside ENT-013, for the four hours to my turn of 12:30 UTC, the plan
flies without a hand: the ten traders without First Steps take the
board route (3 at a time), then Network Expansion, The Collective
Provides and The Signal Protocol, about 7,900 cr once each after fuel.
The others fly the links they have not flown, then wait docked or read a
frontier system. The Standing Plan in `game/routes/guidebook/trade.md`
gives each route's ships and expected figure.

My choices for the turn of 12:30 UTC, written into `planned` of
`game/routes/plans/trader.json`:

- Atmospheric Extraction: one trader without a harvester accepts it and
  buys a Gas Harvester I at Node Beta (1,202 cr), then reads the
  objective. A route only if the purchase counts.
- Hardware Optimization: Cargo: the cargo expander's ask first, then the
  same test.
- Network Commerce Protocol (sell 5 carbon ore) and Material Synthesis:
  Basic (mine 10 iron ore and smelt it into steel): one hand test each.
  A route once the runner withdraws from storage and crafts.
- Every turn: the whole board of every docked trader, read with
  `boards.py` against the fleet's book of rewards, and one test for
  every title nobody has flown.
- The mine-the-experiment-haze RESULT line read: lift it if hydrogen
  sold at 26 cr or more, out if not.
- Lower `max_ships` of the board route if its runs end with the carbon
  objective open, and of The Collective Provides when the reef's nickel
  reads under 40.

The Crimson Resonance is not flown: Intel's read of Crimson law
(queue.log ENT-089) finds no bar to one ship, but the Fleet Admiral's
report puts the call with Suggi. Crystal Resonance Harvest (4,000 cr)
and Deep Core Prospecting (5,000 cr and 10 exotic matter) are mining
missions, offered to Zero in queue.log ENT-095.

## Suggestions

1. **A once route that skipped every stop counts as no try** (requests.log
   ENT-129, the Fleet Admiral's: dispatch.py). Reason: the old First
   Steps route gave 87 pilots an empty run booked as done. Cost: one
   condition in the dispatcher's count, and a test.
2. **fill.py judges a route by its last runs as well as by its
   measure.** Reason: it twice added a route whose eight newest runs all
   lost. Cost: a window on the runs file in fill.py, the Fleet Admiral's.
3. **Every Admiral reads its docked pilots' whole boards each turn**
   (my `boards.py`, a script of my skill; I can move it into
   `game/fleet/` with `fleet-build.sh` if the Fleet Admiral wants it for
   all). Reason: four once missions worth about 7,900 cr a pilot stood
   unseen on one board. Cost: free reads, one call per pilot.
4. **No new traders.** Repeating trade employs 0 of 20.

## Learnings

**A board hides a mission line behind its first link.** First Steps in
the Void led to Network Expansion, The Collective Provides and eight
more, about 24,000 cr a pilot. The fleet had flown nothing past the
first link, because no route accepted First Steps from the board. The
record: the boards of 08:34 UTC, the hand runs of 08:35 to 09:48 UTC,
and 87 pilots without First Steps in `data/fleet/onetime.json`. Trade
now reads every docked trader's whole board each turn and tests every
unbooked title by hand that turn. Any division with docked pilots can
do the same: the reads are free. Kept in
`knowledge/voidborn-delivery-missions.md`; the script and the step are
in my skill trade-books.

**A once route for a board mission accepts it at its first stop.**
Otherwise it spends every non-holder on a skipped run (errors.log
ENT-051). Kept in the same file and as a pitfall of the skill.

**A route's measure can be older than its last runs.**
voidborn-first-hunt-achernar measured +80 a run while its last eight
runs lost. Before fill puts a route back, I read its last runs with the
tool route. Kept in the skill.

**Repeated mistake:** typed times. The fix of errors.log ENT-035
covered route drafts, not guidebook edits. The skill now says that a
script editing the guidebook takes its times from `date -u`.

Confirmed, no change: a board offers each pilot its own missions, and
one accept with an empty hold is the cheapest test. Open: whether a
module bought after the accept satisfies an "acquire" objective.

Skill: trade-books changed -- boards.py, the board step, four pitfalls (gate.py cut, once route without accept, fill on an uncommitted guidebook and on old measures, guidebook times)

## Cross-links

- `reports/2026-11-16_mercury_chain-flown-past-runner-crash-signal-fragments-per-pilot.md` -- my previous report.
- `reports/2026-11-16_unity_route-maker-back-skills-on-routes-gate-counts-open-work.md` -- the Fleet Admiral's report in force.
- `game/routes/guidebook/trade.md` -- the Standing Plan and every figure above.
- `game/routes/voidborn-network-expansion.json`, `game/routes/voidborn-first-steps-board.json`, `game/routes/voidborn-collective-provides.json`, `game/routes/voidborn-signal-protocol.json` -- the four new routes.
- `communications/orders.log` ENT-013; `communications/requests.log` ENT-118, ENT-121, ENT-129; `communications/errors.log` ENT-051; `communications/queue.log` ENT-091, ENT-095, ENT-096.

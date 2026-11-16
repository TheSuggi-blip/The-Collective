---
name: steady-income-positive-on-ice-harvester-bounds-the-fleet
id: 20261116T014606Z
tier: report
trigger: session-end
author: Unity
tags: [fleet, economy, capacity, tools, strategy]
links: [reports/2026-11-15_unity_water-ice-pays-routes-write-themselves-steady-income-near-zero.md, reports/2026-11-16_zero_ice-routes-pay-five-thousand-a-run-harvesters-limit.md, reports/2026-11-16_mercury_node-beta-mission-chain-pays-once-gaps-still-one-load.md, reports/2026-11-15_apollo_once-missions-fill-the-plan-stored-soma-sells.md, reports/2026-11-16_apophis_frontier-herds-pay-railgun-no-gain.md, reports/2026-11-15_oracle_first-foreign-book-ring-three-read-base-sites-judged.md, governance/strategy.md]
---

# The Collective -- Steady income turned positive on ice and veil-rays; 120 ships wait for a tool, not for a plan; the fleet's own tools and its strategy are built

## Situation

This report covers 2026-11-15 23:33 UTC, the time of my previous
report
(`reports/2026-11-15_unity_water-ice-pays-routes-write-themselves-steady-income-near-zero.md`),
to 2026-11-16 01:45 UTC. In it the Admirals' third turn, started by
hand at 23:18 UTC under `orders.log` ENT-007, ended, and all five
reported. Each line below is taken from the Admiral's own report.

- Mining (`reports/2026-11-16_zero_ice-routes-pay-five-thousand-a-run-harvesters-limit.md`):
  40 of 40 ships, none lost. Credits 1,376,832 to 1,474,509. Five
  selling ice runs earned +4,644 to +6,730 cr each after fuel; seven
  harvesters were bought; 25 miners stood free at 00:32 UTC because no
  harvester was left on offer at the fitting route's station.
- Trade (`reports/2026-11-16_mercury_node-beta-mission-chain-pays-once-gaps-still-one-load.md`):
  20 of 20 ships. Credits 685,607 to 751,677. Its 27 runs brought
  74,477 cr of rewards paid once and -3,147 cr without them. A chain
  of three missions pays 10,847 cr once per pilot.
- Logistics (`reports/2026-11-15_apollo_once-missions-fill-the-plan-stored-soma-sells.md`):
  20 of 20 ships. Credits 586,889 to 738,040, of it 148,923 paid once
  and +2,228 without. Three stored soma sold for +2,034 cr.
- Military (`reports/2026-11-16_apophis_frontier-herds-pay-railgun-no-gain.md`):
  30 of 30 ships, every hull whole. Credits 884,890 to 1,108,529, of
  it 180,780 paid once. Its 21 hunts made +14,768 cr, 2,007 cr per
  hunter-hour.
- Intel (`reports/2026-11-15_oracle_first-foreign-book-ring-three-read-base-sites-judged.md`):
  20 of 20 ships. Credits 579,998 to 672,556; -6,032 cr without the
  money paid once. It read 41 of 42 frontier systems and found one
  order book beyond the border.
- Command (my own 16 ships): four sentinels flew the ice routes as
  pathfinders; six test runs of my flagships between 01:16 and 01:31
  UTC, five trades and one mission, cost 8,402 cr in sum
  (`data/routes/runs.jsonl`; see Learnings).

Fleet totals, from `data/fleet/fleet.json` through `game/fleet/hive.py
fleet` at 01:43 UTC: 146 ships, none lost, 24 at work and 122 docked
without work; credits 5,803,806. Steady money, the rewards paid once
left out: +55,031 cr in the last hour (income 76,572, costs 21,541, of
them fuel 10,306; the repair meter reads 0 and is not trusted),
+1,892 cr an hour over six hours and -5,588 cr an hour over the 770
minutes on record. It is the first hour above zero. Of that hour
Mining made +54,174 cr with 10 ships at work and Military +11,394 with
5; Command read -8,314, Intel -1,845, Trade -378 and Logistics 0.
`game/fleet/fill.py check all` at 01:43 UTC: 120 ships wait, and the
work open to them is two paying places and one test.

## Strategy

The strategy now stands in one file, `governance/strategy.md`, written
on Suggi's instruction of 2026-11-16 and approved by him. It ranks
beside the constitution; the Precedence section of all six AGENTS.md
names it and preflight reads it. It holds what Suggi wants in his own
words, what real-time strategy, base-building, role-playing and EVE
fleets teach (14 sources), ten principles and four phases, each with a
goalpost. The fleet is in phase 1, income: its goalpost is a steady
net above zero over 24 hours with no ship waiting while paying work
stands open. Against it the record of 01:43 UTC reads -5,588 cr an
hour over the hours on record, +55,031 in the last one, and 120 ships
waiting.

Decided by Suggi in the period, each in the conversation of
2026-11-15 and 2026-11-16:

- His standing orders S1 to S5 head every entry of the orders.
- The scheduled turns stay off: "not yet, we run manual first".
- No ship idle in the four hours between two turns is "extremely
  important": the plumbing comes first. Built: `fill.py` and the fill
  gate, a step of all six turn jobs.
- One MCP for the hivemind's data and one door for fast command.
  Built: `game/fleet/collective_mcp.py`, 17 tools, in all six
  profiles.
- An escort may fire and defend, only after an attack, and then
  escapes too.
- The plans for an outpost and a station belong in the data system.
  Built: `hive.py base outpost|station`.
- Each Admiral reports what its domain carries and how many ships more
  it could employ; I report which knowledge files each wrote.
- Every index that grows is a master index with sub-indexes.

What changed in how the fleet is measured: a fitting's purchase is
money spent once and no longer a running cost, and a route that lost
money over two runs is closed by the dispatcher itself.

My recommendations, none decided yet. The bottleneck of phase 1 is a
tool: 14 ships carry an Ice Harvester I, while five stations bid for
81,695 units of water ice and the fields we read hold 254,347 units
(`hive.py capacity`, 01:30 UTC). I propose to get the harvester by
three ways at once: bought at our stations (14 on offer at 1,413 to
1,738 cr), fetched from the one foreign station (20 on offer at 638
cr) and made by hand from stored ore. I propose no new ship until a
division shows more places than ships, and no outpost before the ice
routes have held a day. Leaving the Voidborn empire I advise against:
it cannot be undone and no phase needs it.

## Divisions

**Mining.** Zero carried out the order as written: the fitting route
and ten ice routes went into the plan, the first RESULT lines were
read and three routes lifted. The thread holds: the turn before he
found water ice, this turn he measured it. His numbers agree with the
fleet's: the paying ice routes read 2,700 to 7,330 cr per ship-hour
in `game/routes/index.md`. His error (a fitting route sized by the
work, not by the asks, `errors.log` ENT-026) had my runner's flaw
beside it: a buy above its limit. Suggestions: where the harvester is
made and who supplies it, accepted, it is the centre of the new
orders; the pathfinders keep flying new routes first, accepted; an
outpost beside the best field, Suggi's, carried to Open Questions;
`measure --write` by route, accepted and done.

**Trade.** Mercury's three reports say the same with more proof each
time: no gap between our stations carries a load. He stayed inside his
orders and corrected two rules of his own (`errors.log` ENT-027,
ENT-028). Suggestions: the empty-hold check by value and
`requires.booked`, both accepted and owed; reading every board again
after a hand-in, accepted, it costs nothing; energy crystals into the
mission that pays 7,000 cr for 15, open: the same crystals make power
cells for harvesters, and one made harvester decides which is worth
more.

**Logistics.** Apollo reversed a finding of his own on the record: the
iron bid does refill. His thread holds, and his two dating slips are
named by himself (`errors.log` ENT-025). Suggestions: First Steps on
again, accepted and done; selling from storage into a standing bid,
accepted and owed; our own 302 soma before any soma is bought,
accepted, the soma trades left my plan; silicon and crystals kept for
circuit boards, accepted, the harvester needs them.

**Military.** Apophis ordered his plan as a standing loop and kept
every hull. His figures agree with the run record. He cited my older
report as the newest, since mine of 23:33 UTC came after his
preflight. Suggestions: `measure --write` for one division, done; an
ammunition check, accepted and owed; more herds for First Hunt,
accepted; credits moved between his own pilots for one better hull,
accepted as one test inside the money limit, since the game allows
gifts between pilots (`governance/rulebook.md`).

**Intel.** Oracle read the frontier ring and named a third claim of
his own that was wider than its check (`errors.log` ENT-024); his fix
is a check that fires by itself. Suggestions: refuelling the census
where fuel is cheap, open until he has measured one read; the map's
outposts marked apart from markets, accepted and owed; the nearest
Solarian order book, accepted earlier (`requests.log` ENT-073).

Two reports stood against each other and are settled: the route maker
offered a soma trade to Trade while Logistics held 302 soma; our own
are sold first.

What each wrote into its own knowledge in the period
(`hive.py learnings`, 01:00 UTC): Mining two files (ice mining, energy
crystal), Logistics three (fuel per hop, station bids that refill,
stored ore), Trade two (delivery missions, order books), Military two
(hunting herds, weapons and hulls), Intel two (census freshness,
frontier bases and markets).

## Plans

The next orders are the next entry of `orders.log` (ENT-010), written
with this report. Its turn tests one thing: whether the divisions earn
for four hours unbroken by themselves.

- Mining puts every miner that can carry a harvester on ice, lifts
  each paying route as far as its share of the bids carries, and buys
  harvesters where they stand, one ship per ask.
- Trade fetches what the foreign station sells cheaper than ours,
  harvesters first, with an empty hold on the way out, and brings the
  fleet its rewards paid once.
- Logistics makes one harvester by hand from stored ore as the test of
  the fleet's first supply chain, and sells the stored soma as the
  bids refill.
- Military keeps one hunter on every herd that paid and one drone in
  every system beyond the border where our miners work.
- Intel keeps the picture, names three sites for a first outpost
  beside the best ice fields, and reads the nearest Solarian book.
- Every Admiral closes the fill gate before its turn ends and states
  the capacity of its domain.

What I do myself. Until 12:00 UTC the nine changes I owe the Admirals:
the craft step, a circuit stop that sells from storage with
`requires.bid`, the route maker counting a small bid once, the
ammunition check, the route kind `guard` with the escort rule, the
gate against pilot names, the census gap figure, the corrections of
`game/rules/` and the empty-hold check by value with
`requires.booked`. The command station is being reworked on Suggi's
words of this morning: the Docs list, the Metrics width, side panels
that fold away and the group chat at the bottom of the map.

Morpheus reviewed the design (`queue.log` ENT-054). Taken at once: an
audit line for every command through the door, the protocol's hints on
the tools, tool purchases booked apart, a HALT line printed once.
Weighed and open: one read tool that answers a division's whole
question in a few lines, a single history store behind the tools so
that no record grows without end, tool lists filtered per profile, and
a market stream in place of polling. A wall per division is work on
the box and his to put to Suggi.

## Open Questions

1. **Start the Admirals' fourth turn?** It is ready: the report, the
   orders and the tools are in place, and `fire_turn.sh` checks all
   three. My recommendation: start it now, by hand. What would change
   it: a word of yours on the orders first.
2. **The first outpost.** Founding one costs 100,000 cr and one
   Outpost Kit. A kit stood on offer for 216,825 cr at the one foreign
   station (one order book, read 01:24 UTC), which is cheaper than the
   facility that makes it (600,000 cr and materials, `hive.py base
   outpost`). Options: buy that kit now, or wait. I recommend waiting
   until the ice routes have held a day and Intel has named three
   sites; the offer may be gone by then, and the 317,000 cr are about
   5% of the fleet's credits.
3. **One line of the constitution.** It calls itself the
   highest-precedence document, and the strategy now ranks beside it.
   I propose one sentence there naming `governance/strategy.md`. The
   file is locked: your word.
4. **More ships.** I recommend none now: 120 of 146 wait. What would
   change it: a division whose places exceed its ships after this
   turn.
5. **The scheduled turns** stay off, as you said. I will ask again
   after two turns by hand have closed their fill gates.
6. **Fleet size by role.** I owe you a plan and propose to give it
   after this turn, from each Admiral's capacity figures.

## Learnings

From this session's learning capture.

**A plan keeps ships at work only where repeating work has places.**
At 01:40 UTC 119 ships waited while the plans had two paying places
and one test left to add (`fill.py check all`); the ships on ice and
veil-rays made the first positive steady hour in the same hour. The
limit was a tool on 14 ships, not the fields and not the bids
(`hive.py capacity`, 01:30 UTC). I now read the limit of the
repeating work before I ask an Admiral for a fuller plan, and order
toward it. Kept in: `knowledge/fleet-employment.md` (new). For the
Admirals: for each waiting ship ask which limit closes the work, and
whether another division holds the key to it.

**A script that fills plans needs a loss stop.** My own filler took a
trade measured on one run for a paying route; two flagships paid 4,635
cr each for plating whose bid is one unit (`data/routes/runs.jsonl`,
01:16 and 01:27 UTC). Three checks now fire by themselves: paying from
two runs, no candidate that buys goods added by a script, and a route
that lost money over two runs closed by the dispatcher. Kept in: the
same file.

**A command in a shared skill is run by every member at once**: three
Admirals reverted other divisions' files after `measure --write`.
**A service can fail every pass while it reads as running**: the route
maker did for nine passes. **A tool's first answer is one recipe, not
the chain**: a draft order of mine would have sent Military hunting
for goods the market sells. **Money spent once on tools read as a
loss**: Mining's figure in the hour it bought its harvesters. Kept in:
unpromoted, `LEARNINGS.md`, each seen once.

Confirmed: orders with a goal, limits and a named record were carried
out as written by all five. Open: how fast a bid refills under our own
sales; what a turn costs in calls, which Morpheus counted and I have
not checked.

## Cross-links

- `reports/2026-11-15_unity_water-ice-pays-routes-write-themselves-steady-income-near-zero.md` -- my previous report.
- `reports/2026-11-16_zero_ice-routes-pay-five-thousand-a-run-harvesters-limit.md` -- Mining.
- `reports/2026-11-16_mercury_node-beta-mission-chain-pays-once-gaps-still-one-load.md` -- Trade.
- `reports/2026-11-15_apollo_once-missions-fill-the-plan-stored-soma-sells.md` -- Logistics.
- `reports/2026-11-16_apophis_frontier-herds-pay-railgun-no-gain.md` -- Military.
- `reports/2026-11-15_oracle_first-foreign-book-ring-three-read-base-sites-judged.md` -- Intel.
- `governance/strategy.md` -- the strategy the fleet plays by.
- `game/fleet/index.md` -- `fill.py`, `hive.py`, `collective_mcp.py`: the tools named above.

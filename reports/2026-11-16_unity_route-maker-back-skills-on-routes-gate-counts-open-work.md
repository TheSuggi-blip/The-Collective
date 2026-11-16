---
name: route-maker-back-skills-on-routes-gate-counts-open-work
id: 20261116T065920Z
tier: report
trigger: session-end
author: Unity
tags: [fleet, services, dispatch, fill-gate, missions]
links:
  - reports/2026-11-16_unity_steady-net-doubles-on-fitted-harvesters-admirals-build-their-own-tools.md
  - reports/2026-11-16_mercury_chain-flown-past-runner-crash-signal-fragments-per-pilot.md
  - reports/2026-11-16_apophis_chain-and-cracking-the-shell-open-yield-tests-spent.md
  - reports/2026-11-16_apollo_harvester-chain-staged-carapace-makes-armor-plate.md
  - reports/2026-11-16_zero_ironlight-harvesters-fit-the-waiting-miners.md
  - reports/2026-11-16_oracle_first-steps-and-atlas-hunt-pay-node-beta-chain-crashes.md
  - governance/strategy.md
---

# The Collective -- The route maker runs again after three silent hours; a route can ask a skill; the fill gate counts only work a ship may take

## Situation

Period: from my report of 2026-11-16 05:02 UTC
(`reports/2026-11-16_unity_steady-net-doubles-on-fitted-harvesters-admirals-build-their-own-tools.md`)
to 06:59 UTC, my first scheduled turn (`turn-unity`, 06:30 UTC). Orders
in force at its start: `orders.log` ENT-012; at its end ENT-013.

The fleet at 06:58 UTC (`hive.py fleet`): 146 ships, 62 at work, 84
docked without work, 0 adrift; credits 6,689,573 (45,819 a ship).
Steady money, rewards paid once left out: net +84,550 cr in the last
hour (income 110,290, costs 25,740, of it fuel 25,717), +80,191 an hour
over six hours, +20,770 an hour over 24. The last hour has fallen
since my last report (+104,094 then); the six-hour figure has risen
(49,065 then). The cause of the hourly fall is not looked into. In one unit
(`hive.py tasks`, four hours to 06:58 UTC): the fleet 519 credits per
ship-hour over all 146 ships and 1,541 per ship-hour flown, 409,667 cr
paid once beside it. The scale: the best repeating route,
mine-ruchbah-ice-belt, 9,689 credits per ship-hour; a ship without work
earns 0.

The divisions, each from its Admiral's newest report and the four-hour
figure of `hive.py tasks` at 06:58 UTC:

- Mining (Zero, 04:29 UTC): harvesters from Ironlight Crossroads at
  half the home price fitted the waiting miners, 20 to 33 of 40 at work;
  1,666 credits per ship-hour over all 40 ships.
- Intel (Oracle, 04:52 UTC): the home hour held, First Steps and a hunt
  at Atlas paid, the frontier grew to 51 systems; -79.
- Trade (Mercury, 05:22 UTC): ten traders flew the Node Beta chain past
  the runner crash, +109,213 cr once; Signal Fragments found at
  navigation 3; -41, no trade repeats.
- Military (Apophis, 05:27 UTC): 24 hunts, 42 kills, 1,829 cr per
  hunter-hour; the yield tests are spent; 162.
- Logistics (Apollo, 05:29 UTC): goods for nine harvesters staged,
  carapace sells as armor plate; -105.
- Command (mine): 549 credits per ship-hour over 16 ships.

The fill gate at 06:58 UTC: PASS for scout, sentinel and trader; HALT
for command (1 test, filled at 06:59), drone (1 paying place), hauler
(1 paying place) and miner (2 tests). Preflight found the route maker
failing since 03:32 UTC: Problems in Divisions and Learnings below.

## Strategy

The strategy in force is `governance/strategy.md`: phase 1, income.
Its goalpost is a steady net above zero over 24 hours and, at every
turn of a day, no ship waiting while paying work stands open. The
first half stands: +20,770 cr an hour over 24 hours. The second does
not: 84 ships wait, and four roles' gates HALT on open work at the end
of this turn. Suggi decided nothing in this period; his standing orders
S1 to S6 and his decisions in my decision log (the newest, D123, the
history store) stand as they were. All six turn jobs read active at
07:00 UTC; their next runs: Zero 08:00, Oracle 08:15, Mercury 08:30,
Apollo 08:45, Apophis 09:00 and mine 10:30 UTC.

What I decided inside them, and why. First, the bottleneck of this
turn was not a field, a bid or a tool but the fleet's own machinery:
the route maker had written no candidate for three hours, so no
division could name a new test; the fill gate's HALT pointed at a
place no ship may take; and two of my own ships flew engine loops that
stored ice for five hours. Principle 3 (find the bottleneck, lift it)
sent the turn there first. Second, the largest sum open to the fleet
this hour is once money, not repeating work: Signal Fragments pays
about 6,900 cr once to every pilot with navigation 3 (46 by Mercury's
count, about 310,000 cr), and the Node Beta chain about 10,893 cr to
every pilot that has not flown it. Both are seed money (principle 1:
it is reinvested into tools and the base reserve), never steady
income, and every figure in this report keeps them apart. Third, the
repeating income is ice: the best repeating route pays 9,689 credits
per ship-hour, and Mining makes 1,666 over all its ships against -105
to 162 in the other divisions. What limits more ice work is the share
of the bids near the fields (Zero: about 30 ice places for 40 miners),
not ships; no division asks for a new ship, and I recommend none.

PROPOSED, for the next turns: the fleet's next repeating income is
the supply chain Logistics has staged (goods for nine more harvesters
made from our own ore, Apollo's report), and the carapace
that Military holds (394 units, about 65 plates at 222 to 380 cr, bids
of 3 to 6 units at four stations). Neither changes the phase; both
serve principle 8 (build the chain inward).

## Divisions

**Mining (Zero).** No report since my last. Its three reports of the
day (00:34, 03:25 and 04:29 UTC) read as one line: ice pays, the
harvester is the limit, the harvester bought at Ironlight Crossroads
fits the waiting miners; I did not check each planned step against the
next report this turn. Its Ruchbah figure agrees with the fleet's
(8,950 by Zero over 16 runs, 9,689 by the tools now). Its suggestion that the loss stop read the notes was
answered last period. Its request ENT-095 is done (requests.log ENT-111),
the second part as asked, the first built differently: a once route
the board refused to every pilot of a role is closed to that role.
ENT-083 (engine loops without an order file) is still owed, moved to
my turn of 10:30 UTC; its only live cases were two of my own ships,
which I stopped by hand at 06:50 UTC.

**Intel (Oracle).** No report since my last. Oracle wrote to me at
04:52 UTC that the route maker had written nothing since 03:22 UTC
(queue.log ENT-076); I read it in my last session and closed without a
fix. That is mine (errors.log ENT-045), and the route maker is fixed
now. Its request ENT-092 is done (ENT-113): the hunt step's last word
and the ship's place go into the run row; the three runs it named
carry no cause in the record.

**Trade (Mercury).** Its thread holds: the chain it opened at 03:36 UTC
was flown for all 20 traders by 05:16 UTC, its figures agree with the
run rows. Suggestions: (1) `requires.skills`: accepted and done
(ENT-110), Signal Fragments now asks navigation 3 and stands at the
head of the command plans. (2) A refused accept as no try on every once
route: declined for now; a mission done once is also "not offered",
so every once route would cost up to three refused runs per pilot, and
the two conditions we know are now fields. (3) No new traders: agreed.
(4) The Crimson Resonance: not flown; Intel reads that empire's law
first (orders ENT-013, ORACLE (7)).

**Military (Apophis).** Its thread holds: the tests it planned at 03:27
UTC were flown and seven of eight dropped by 05:20 UTC, with figures
from the run rows. Suggestions: a herd floor for a circuit's hunt step:
accepted, for my turn of 10:30 UTC; the waiting drones as the reserve
for once missions: agreed; no new drones: agreed. Its request ENT-090
is done (ENT-112) in the circuit runner and the dispatcher; census.py
and mine.py still lack the stance flee.

**Logistics (Apollo).** Its thread holds: one harvester made by hand in
its turn of 03:33 UTC, goods for nine more staged by 05:15 UTC, as it
planned. Suggestions: craft inputs
booked as money spent once: accepted, for 10:30 UTC; every division
crafts its own carapace: accepted into the orders (APOPHIS (6)); the
gate counting only open work: done. Two reports quoted as the hour's
scale a fitting route's one sale (12,564 cr per ship-hour); the scale
now counts only repeating routes.

## Plans

What each division does next stands in orders ENT-013, which changed
three things. Every Admiral puts Signal Fragments at the head of its
plan: the dispatcher sends it only to a pilot with navigation 3. Apophis
turns carapace into armor plate where it lies, no more plates than a
bid's depth. Oracle reads the law of Crimson space before any ship
flies The Crimson Resonance. The rest of ENT-012 stands: Mining keeps
the ice routes at what their bids carry; Logistics makes the ten
harvesters at 08:45 UTC; Trade keeps the chain's limits at what the
silver carries.

What I do myself, in my turn of 10:30 UTC and inside 12:00 UTC: the
dispatcher ends an engine loop that runs without an order file
(ENT-083); a herd floor for a circuit's hunt step; craft inputs booked
as money spent once; the battle stance flee in census.py and mine.py;
then the older owed items: the craft step, a sale from storage and
`requires.bid`, the guard route kind, the gate against pilot names,
the corrections of game/rules/, the empty-hold check by value. I read
every Admiral's commit to the fleet's scripts since 05:02 UTC (one,
Apollo's 0f7a36a: the hunt step hands its run's order to hunt.py, one
line and a test; read) and answer every request before their next
turn. Also behind and mine under F11: the live cost of the faction's
lockbox (listed at 200,000 cr), read from the game before it is paid.
After that, one improvement of the station.

## Open Questions

1. **The Crimson Resonance** (8,500 cr once per pilot, the next link
   of Signal Fragments; a dock at The Rampart Checkpoint and 5 titanium
   alloy delivered at Blood Forge, Crimson space 17 to 20 jumps out,
   Mercury's report). It is yours because it leaves Voidborn space for
   another empire's military installations, and no ship of ours has
   been there. My recommendation: no until Intel has read what that
   empire's law does to a Voidborn ship (ordered in ENT-013); then one
   ship as a test under S1, with an empty hold apart from the alloy.
   What would change it: a law that fines or attacks a visitor, or an
   alloy we cannot make or buy near home.
2. **New ships.** No division asks for one: Mining says ice places,
   not ships, are short (about 30 for 40 miners); Military that its
   herds carry about 9 hunters of 30; Trade and Logistics that their
   repeating work employs few of 20. A waiting ship costs 0. My
   recommendation: no new pilot this day. What would change it: a
   repeating route whose bid carries more ships than the role has.

## Learnings

From this turn's learning capture.

**A fault that leaves no record is found hours late.** The route maker
failed all 19 passes from 03:32 to 06:32 UTC while the shelf read it
running (errors.log ENT-044), the second such failure in a day; the
runner crash without rows and the orphan loops of my own ships had the
same shape. Intel told me at 04:52 UTC and I closed my session without
acting (ENT-045). What I do now: every system that acts by itself gets
a check that speaks on its own clock, tested on the state of its fault;
`service-health.py` in the five-minute job names a failing service in
my chat. For the Admirals: a fault in a service of mine goes to
requests.log, where it stands on my board until answered. Kept in
`knowledge/faults-that-leave-no-record.md` (new; it absorbs two
unpromoted entries).

**A figure that picks a best must be read on the data first.** The
tasks view's scale took a fitting's one sale (88,356 cr per ship-hour)
for the fleet's best work, and two Admirals quoted it. Kept unpromoted
in `LEARNINGS.md`.

Repeated: yes, the class of ENT-030; its fix was a reader, not an
alarm. Open: what an Admiral turn of 104 minutes costs.

Skill: collective-mcp changed -- pitfalls: a figure that picks a best, a service that fails while running

## Cross-links

- `reports/2026-11-16_unity_steady-net-doubles-on-fitted-harvesters-admirals-build-their-own-tools.md` -- my previous report.
- `reports/2026-11-16_mercury_chain-flown-past-runner-crash-signal-fragments-per-pilot.md` -- Trade, 05:22 UTC.
- `reports/2026-11-16_apophis_chain-and-cracking-the-shell-open-yield-tests-spent.md` -- Military, 05:27 UTC.
- `reports/2026-11-16_apollo_harvester-chain-staged-carapace-makes-armor-plate.md` -- Logistics, 05:29 UTC.
- `reports/2026-11-16_zero_ironlight-harvesters-fit-the-waiting-miners.md` -- Mining, 04:29 UTC.
- `reports/2026-11-16_oracle_first-steps-and-atlas-hunt-pay-node-beta-chain-crashes.md` -- Intel, 04:52 UTC.
- `governance/strategy.md` -- the strategy and its phases.
- `communications/orders.log` ENT-013; `communications/requests.log` ENT-110 to ENT-114; `communications/errors.log` ENT-044, ENT-045; `communications/queue.log` ENT-087.

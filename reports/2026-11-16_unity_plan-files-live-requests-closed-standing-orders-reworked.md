---
name: plan-files-live-requests-closed-standing-orders-reworked
id: 20261116T182021Z
tier: report
trigger: order
author: Unity
tags: [fleet, plans, orders, requests, faction, forecast]
links:
  - reports/2026-11-16_unity_routes-close-on-their-bid-loss-stop-reads-last-runs.md
  - reports/2026-11-16_zero_central-nexus-depth-gone-stored-ice-sold-first.md
  - reports/2026-11-16_mercury_spent-reef-dry-crystal-ask-tax-in-runs.md
  - reports/2026-11-16_apollo_stored-gas-into-liquid-hydrogen-haulers-trained-for-signal.md
  - reports/2026-11-16_apophis_curd-bid-back-veil-rays-on-stored-loot-sold.md
  - reports/2026-11-16_oracle_once-line-heads-scout-plan-spent-herd-left.md
  - governance/strategy.md
---

# The Collective -- Every Ship Works and the Fleet Still Loses 15,000 Credits an Hour: Plan Files Are Live, Every Request Is Closed, Suggi Reworked the Standing Orders

## Situation

Period: from my report of 2026-11-16 11:05 UTC
(`reports/2026-11-16_unity_routes-close-on-their-bid-loss-stop-reads-last-runs.md`)
to 18:20 UTC. Orders in force: `orders.log` ENT-017 (18:18 UTC). Suggi
paused the turn jobs at 13:50 UTC, so the Admirals' newest reports are
those of their turn of 12:00 to 14:45 UTC. Each division's line is
taken from that report; the fleet's totals are read from the fleet's
own tools at 18:19 UTC.

- Mining (`reports/2026-11-16_zero_central-nexus-depth-gone-stored-ice-sold-first.md`):
  40 of 40 ships, 2,629,381 cr at 12:31 UTC after the weekly tax; 51
  mine runs made +116,694 cr after fuel; the Central Nexus water ice
  order of 42,635 units was gone within three hours.
- Trade (`reports/2026-11-16_mercury_spent-reef-dry-crystal-ask-tax-in-runs.md`):
  20 of 20 ships, 999,608 cr at 12:58 UTC; 12 trader runs made +20,995
  cr, 22,931 of it paid once; 19 of 20 traders waited docked at 12:30
  UTC.
- Logistics (`reports/2026-11-16_apollo_stored-gas-into-liquid-hydrogen-haulers-trained-for-signal.md`):
  20 of 20 ships, 1,112,747 cr at 14:42 UTC; 75 liquid hydrogen made
  from stored gas and 42 sold; ten haulers trained to navigation 3.
- Military (`reports/2026-11-16_apophis_curd-bid-back-veil-rays-on-stored-loot-sold.md`):
  30 of 30 ships, 1,622,308 cr at 13:36 UTC; 40 stored curd sold for
  13,200 cr; 23 armor plates made, 15 sold; sixteen drones waited.
- Intel (`reports/2026-11-16_oracle_once-line-heads-scout-plan-spent-herd-left.md`):
  20 of 20 ships, 1,039,313 cr at 12:16 UTC; every Voidborn system read
  within the hour; a once hunt flew 13 runs into a spent herd.

Fleet totals (`hive.py fleet`, 18:19 UTC): 146 ships, 146 at work,
8,448,111 cr. Steady money of the last hour: income 14,471, costs
29,518 (fuel), net -15,047 cr an hour; over six hours -10,630 an hour.
Net an hour by division: Command -2,675, Intel -3,933, Logistics
-1,101, Military -7,585, Mining -608, Trade +856. Paid once in the
last hour: 84,500 cr in 22 bookings. The weekly tax of 12:27 UTC took
612,070 cr from 146 pilots and is booked once. The fill gate reads
PASS for every role (`fill.py check all`, 18:19 UTC).

The forecast (`hive.py forecast`, 18:10 UTC) says why: nearly every
ship is on standing work, which gathers and levels and costs its
fuel. If every ship stays where it is, the fleet makes -19,221 cr an
hour, -132 a ship. Only four routes it lists earn: two gas routes of
Trade (310 and 172 cr per ship-hour), one hunt of Military (600) and
one of Intel (2,420), each with one ship.

## Strategy

The strategy in force is `governance/strategy.md`, phase 1: income.
Suggi decided the following in the period; each is his word, built or
written down by me.

1. About 14:00 UTC. Times told to him are in CET. No ship is idle, no
   route is crowded, the orders are short, and each Admiral plans its
   own division. Orders ENT-015 carried it; the standing rules moved
   into the rulebook, section 12.
2. About 15:40 UTC. Each Admiral keeps one plan file with every ship
   and its own routes; a script sends the ships by it; no ship goes
   broke. Built: `game/fleet/plan.py` (commit 78e1f1e) and
   `game/fleet/wallet.py` (commit 0ba8341); orders ENT-016.
3. About 16:45 UTC. He held the Admirals' start: more changes first.
4. Between 17:00 and 17:35 UTC. `FLEET.md` of every member is one
   roster table; `COLLECTIVE.md` is one merged table and, below it,
   each member's own mission; the routes folder gets one index per
   group and one plan per role. Testing is always allowed. His goal:
   "become economically positive earners. We must fill all the supply
   routes, craft, build bases, earn money, level up." Where the fleet
   expands on the map is his. He approved the sentences of three
   locked files that the change made untrue: the constitution
   (version 4) and the six `AGENTS.md`.
5. About 18:10 UTC. He reworked the standing orders: explore freely,
   dominate the galaxy, grow the fleet, build a galactic empire. The
   Fleet Admiral organizes the fleet and instructs the Admirals; the
   faction's treasury, shared storage and every ship in the faction
   are her medium-term goals. Every member is measured by the orders.

What changed in the orders: ENT-017 carries the four standing orders
in his words. What the earlier S2 to S6 named stands in the plan, P1
to P5, which he had approved as it was. P5 now names the faction's
steps with their cost. ENT-017 also corrects ENT-016, which said a
turn was started by hand that he then held.

My own reading, marked as mine: the buyers are the fleet's limit, not
the ships. 146 of 146 ships work and the fleet loses money, because
standing work is what a ship does when no bid, herd or mission takes
it. The lever is demand: goods we craft, stations beyond the six we
sell at, and our own use of what we gather. I propose that the first
thing our supply chain makes is the faction's own offices: the steel
plate and the circuit boards for a Faction Lockbox and a Hiring Board
(275 and 75 units). It is a small, real order that runs through
Mining, Logistics and Intel, and it stands in ENT-017 as Logistics'
order.

## Divisions

**Mining.** Zero reported the Central Nexus order gone and 29 miners
sized on it, a repeat of the morning's fault, with its cause named:
a rule to remember, and a fill hint that counted standing depth. My
judgment: the report is exact and the cause is right; the fix had to
be in the tool. Its thread holds: the report of 09:11 UTC sold at
Central Nexus; this one names why that failed and what replaced it
(`requires.bid` on every ice route, the places cut to seven).
Suggestions: (1) size the fill hint on the regain: accepted and done
(`fill.carries`, commit 9a622e2; `fill.py lift` refuses more). (2) A
refused game command as a runner-fault note: open; not built, it is
next on my list. (3) Shared storage is not needed for the ice:
accepted as a finding; shared storage is now a goal for another
reason, the faction's offices need it first. (4) No new miners, a
search for palladium fields: accepted; it goes to Intel in the plans
below.

**Trade.** Mercury reported the once line stopped at a spent reef and
a dry crystal ask, and the weekly tax read as run losses. Judgment:
honest about its own cause (a chain sized on one ask). Suggestions:
(1) Neural Matrix Delivery under F13: accepted (requests ENT-155).
(2) The tax out of the runs: done (`taxes.py`, commits 9a622e2 and
3d04e0c). (3) A floor for mine steps: done (`min_left`, requests
ENT-157); a floor for a buy step on its ask is open. (4) An outpost:
Suggi's, carried below. (5) No new traders: agreed.

**Logistics.** Apollo reported stored gas sold as liquid hydrogen and
four module missions flown into a refusal, recovered by script.
Judgment: the strongest thread of the five: each turn makes one new
thing from stored goods. Suggestions: (1) keep platinum ore for the
station: accepted; an input of the stations' list is stored, not sold
under its ask. (2) Train every pilot one level short of a board's
gate, and (4) a training field: done (`requires.skills_below`,
standing work, commit 9a622e2). (3) Hand in before a fit: Mercury's
(requests ENT-149). (5) Fill names only allowed work: answered
(requests ENT-160). (6) The craft step: done, not flown (requests
ENT-161).

**Military.** Apophis reported the curd bid back, the stored curd
sold and sixteen drones waiting. Judgment: its numbers agree with the
fleet's; the division earns least per hour today (-7,585) because 27
of 30 drones gather. Suggestions: (1) a level cap and a loss-stop
exemption for training: done, as for Logistics. (2) The tax fix for
runs that start just after the assessment: done (commit 3d04e0c). (3)
A board read for Ghosts in the Cloud: open; the route file carries no
condition yet. (4) Pirate Bounty under F2: Suggi's, carried below.

**Intel.** Oracle reported the once line at the head of the scout
plan and a once hunt flown into a spent herd, with the floor it set.
Judgment: the census is the fleet's measure of what regrows, and it
was kept. Suggestions: (1) an hourly fill of once routes: done every
five minutes (requests ENT-144), and since today the hourly job adds
open paying routes and two tests per role. (2) A herd floor on every
once hunt: accepted, each route's owner. (3) No new scouts: agreed.

All five requests owed to the Admirals are closed (requests ENT-161
to ENT-165): the craft step, the name gate, selling from storage, the
route maker's small bids, the guard route. Craft and guard are tested
on a fake gate only and are not flown.

## Plans

The turn of ENT-017 is started by hand on Suggi's word; it is the
first in which each Admiral writes its own plan file. No ship holds
routes of its own yet; every plan today is the stopgap I set.

- **Mining** sells ice only as far as each bid regains and gathers
  iron first; it reports per ore what a ship gathers in an hour.
- **Trade** finds the trade that repeats, buys the stations' inputs
  where they are cheap, and flies the control-node craft circuit once
  with one trader.
- **Logistics** keeps the stations' list, tests one recipe step, and
  makes the faction's first 275 steel plate and 75 circuit boards.
- **Military** hunts one hunter per herd, guards beyond the border and
  flies the guard route once with one drone.
- **Intel** keeps the census fresh and names sources: the thirteen
  inputs of the stations' list without one, silicon ore and caustic
  sac for the faction's offices, and palladium fields (Zero's
  suggestion: bid at 358 cr, no field read).

What I do myself, in this order:

1. Watch the turn, read every Admiral's plan file and report, and
   give Suggi the forecast per division before and after.
2. Run the learning capture while the turn flies (his word), and
   write its lessons into my knowledge files.
3. Read the rent of a Faction Lockbox from the game with a docked
   flagship before any credit is paid.
4. Build what is open: a refused game command as a runner-fault note
   (Zero); a floor for a buy step (Mercury); a board condition for
   Ghosts in the Cloud (Apophis); the regain measured over the last
   hours only, so the route maker can count it again.
5. Reload the Admirals' tools after the turn, so the tool `fleet`
   offers `view=forecast` (the tool `hive` has it now).
6. The station still shows the figure per ship; Suggi's measure is
   income per hour.

No diplomacy is planned; no word goes to another player.

## Open Questions

1. **The faction's steps (your decision; each payment on your word).**
   The treasury works today. Shared storage is a Faction Lockbox at
   one station: 200,000 cr, 200 steel plate, 50 circuit boards, and a
   rent I have not read yet. For every ship in the faction there are
   two ways. One station up to a Recruitment Center: 2,375,000 cr
   more, 200 members, the builder needs Corporation Management 3, and
   it takes 450 caustic sac, of which we hold none. Or three stations,
   each with a lockbox, a Hiring Board and a Recruitment Desk:
   1,725,000 cr in all, 150 members, Corporation Management 2, shared
   storage at three stations and no caustic sac. I recommend the
   second way, one station at a time, starting when our own plates
   and boards are made. A fleet above 150 ships changes it: then one
   desk becomes a center.
2. **One database (your question).** We have half of it: the history
   store is an SQL database with every run, every market move and
   every reading of a field or herd. The live state, the order
   books, the catalog, the storage book and the intel are files. I
   recommend loading those into the same store and giving every
   member one tool that asks it any question. About a day of work;
   nothing in flight changes.
3. **An outpost (Mercury).** A kit read 74,010 cr plus the 100,000 cr
   fee; it stands only in lawless space. Where is yours. I recommend
   deciding it with the map, not now.
4. **Pirate Bounty (Apophis).** Unflown under the stance. I recommend
   it stays so while the fleet does not earn.
5. **New pilots.** Three Admirals say none. I agree: buyers are the
   limit.
6. **The turn jobs** stay paused; this turn is by hand.

## Learnings

The learning capture runs while the turn flies, on Suggi's word of
about 18:15 UTC; the report after the turn names the knowledge files
it writes. These are the lessons the period's records already hold.

1. **Ships at work is not income.** `hive.py fleet` at 18:19 UTC
   reads 146 of 146 at work and -15,047 cr an hour. I had written
   "no ship idle" as the first step of the plan and built a gate for
   it; the gate is green and the fleet loses money. What I do
   differently: the forecast (`hive.py forecast`) is read beside the
   gate, and each Admiral reports its SUM line before and after it
   plans. For Suggi: PASS means busy, never earning.
2. **A worker's hand-back is a claim.** The worker that fixed the
   route maker built the rule I had briefed and reported that it
   moved 17 ice fields to a bid of two units. The market record
   showed why: the bid's regain is averaged over every reading, and
   the large order had left at 10:37 UTC. I switched that part off
   and compared the candidates on a copy of the live data before the
   install: no estimate per ship-hour moved. What I do differently:
   a brief that says "measured" also says how fresh.
3. **Orders are appended last.** ENT-016 named a turn that Suggi then
   held; ENT-017 had to correct it. The entry is now written right
   before the start, after his last word.
4. **A rule that was broken three times becomes a gate.** Zero asked
   for it (requests ENT-052); `comms.py append` and `routes.py check`
   now refuse a pilot of ours by name.
5. **An index that grows is split before it bloats.** Suggi asked for
   one index per group and one plan per role; the script also removes
   the files it writes no longer, so a renamed group leaves nothing.

Open question: how a bid's regain is measured over the last hours
only, without losing what a quiet bid teaches.

## Cross-links

- `reports/2026-11-16_zero_central-nexus-depth-gone-stored-ice-sold-first.md` -- Mining, turn of 12:00 UTC
- `reports/2026-11-16_mercury_spent-reef-dry-crystal-ask-tax-in-runs.md` -- Trade, turn of 12:30 UTC
- `reports/2026-11-16_apollo_stored-gas-into-liquid-hydrogen-haulers-trained-for-signal.md` -- Logistics, turn of 12:45 UTC
- `reports/2026-11-16_apophis_curd-bid-back-veil-rays-on-stored-loot-sold.md` -- Military, turn of 13:00 UTC
- `reports/2026-11-16_oracle_once-line-heads-scout-plan-spent-herd-left.md` -- Intel, turn of 12:15 UTC
- `communications/orders.log` -- ENT-017, the orders in force
- `governance/strategy.md` -- the strategy, phase 1
- `game/routes/master-index.md` -- the routes and plans, with their sub-indexes

---
name: one-iron-figure-fund-paid-handed-over-worth
id: 20261122T181622Z
tier: report
trigger: session-end
author: Unity
tags: [fleet, iron, treasury, money-figures, strict-classes]
links:
  - reports/2026-11-22_unity_claims-hold-again-treasury-fund-built-two-asks-done.md
  - reports/2026-11-22_zero_iron-gathers-before-jump-loop-far-gifts-any-of-gates.md
  - reports/2026-11-22_oracle_claimed-hunts-dropped-qualia-verdict-claimed-line.md
  - reports/2026-11-22_mercury_curd-standing-bids-nitrogen-crafted-docked-spread-test.md
  - reports/2026-11-22_apollo_boards-from-stored-silicon-crescent-moon-test-opened.md
  - reports/2026-11-22_apophis_shield-booster-solo-whale-near-cheap-hunts.md
---

# The Collective -- One Iron Figure, the Warship Fund Paid, What Hunters and Miners Hand Over Now Counted

## Situation

Period: from my last report (15:19 CET) to 19:16 CET. Orders in force: `orders.log` ENT-065, written this turn (ENT-064 before).

- **The purse** (`hive.py fleet`, 19:14 CET): wallets 8,236,141 cr plus the treasury 1,514,747 cr, 9,750,888 cr in all. At my last report it was 9.76 million, so the purse held level over four hours. 320,000 cr of it moved from the treasury to one Military pilot for its warship (below); that is a move inside our purse, not a loss.
- **Steady money** (`hive.py fleet`, 19:14 CET; fuel in, one-time rewards out): -44,675 cr an hour over the last hour, -56,938 over 6 hours, -7,247 over 24 hours. One-time rewards (missions paid once per pilot) added 99,644 cr in the last hour. Fuel is 104,652 cr an hour. In plain words: the ships burn about 100,000 cr of fuel an hour, and since only traders may sell, most of the fleet shows nothing but that fuel.
- **What is handed over, newly counted** (`hive.py stats contribution`, 19:12 CET, 24 hours): goods given to Trade's and Logistics' receivers would sell for 667,731 cr at today's buy orders, counted only as far as those orders reach (Military 361,194; Intel 167,181; Mining 122,715; Command 9,810; Logistics 6,831). That is about 27,800 cr an hour. Most units lie beyond what the buyers want today: 342,588 of Mining's 379,405 units find no buyer at today's depth.
- **Ships:** 246 of 246 working, none lost; the "never idle" check passed for every role at 19:08 CET (`fill.py check all`).
- **Per division, last hour** (`hive.py fleet` at 18:32 CET): Command -1,576; Intel -24,115; Logistics -17,134; Military -26,970; Mining -12,040; Trade -1,534.
- **Faction seats:** 99 of 200 (briefing). The Recruitment Center stands; seats now fill by moving our ships in.

## Strategy

The standing orders S1 to S5 and the goals G1 to G5 stand as Suggi set them; only he changes them.

New from above me this period: Trinity entered rule F38 (keep two unhurt animals in every herd so it regrows; site bases on scarce resources) and `governance/birth-plans.md`, a plan Suggi approved for growing the fleet from 246 to 500 and then 600 pilots in waves. The first wave (246 to 320 pilots) may only start when two gates hold: 400 seats in the faction, and a steady net above zero over 24 hours. Births stay Suggi's word alone. I took both as written (queue.log ENT-229).

Decided this turn (the Fleet Admiral's own calls):
- **One figure for iron.** Two of our programs disagreed about whether we have enough iron: one said "short" (it wanted 166,923 units), the other said "full" (the buildings we plan need 43,040). The miners' plan followed one of them for four hours. Now both read the same numbers: below 60,000 units the miners gather iron again, at 80,000 they stop, and Trade never sells below 60,000. A check now fails by itself if the two drift apart again. Today we hold 151,657, so iron is full and the miners turn to silicon, carbon, gold and nickel, which the reserve lacks.
- **Orders ENT-065.** P1 ("pay for itself") now names its second purpose: it is the gate of the first birth wave. P4 names 400 seats as the other gate. Military's block now says "buy the warship"; Zero's says iron is full.

My proposal, not decided by anyone above me: the fleet's loss is not mainly a counting problem any more. The goods handed over are worth about 28,000 cr an hour at today's buyers, against a loss of about 57,000 an hour over 6 hours. Even counted, the fleet loses. The cause is fuel spent on training loops and far hunts while buyers for most goods are thin.

## Divisions

- **Mining (Zero, reports.log ENT-117).** He found that his plan put a training loop (jumps for piloting practice) ahead of open iron gathers for four hours, and said so in errors.log ENT-137. 15 ships on the loop fell to 7 within 20 minutes. Suggestions: one iron figure, accepted and done (requests ENT-360). A warning when a ship trains while a short chain's source stands later in its list: open; the iron fix removes today's case, and the new per-pilot view (below) shows the order. A per-pilot "why" view: accepted and built.
- **Intel (Oracle, ENT-118).** He dropped five hunts that Military claims, judged that a second fast scout hull does not pay yet, and asked for the rules at game version 0.732.3 (done, ENT-361). Suggestions: move the Cracking the Shell hunt to a place read more often; Apophis did it this period (Intercrus Ice Fields). Mark one-time routes in the ships table so his check can tell them from standing work: open, small, not built this turn.
- **Trade (Mercury, ENT-119).** 30 of 40 traders flew the training loop because every sell price he had set stood above what the stations pay; he lowered them to the standing bids and the loop fell to 23 ships. His spread test failed twice on a buy limit set without the 1% tax (errors.log ENT-138). Suggestions: a check for that, accepted and built (ENT-362); a per-pilot "why" view, accepted and built.
- **Logistics (Apollo, ENT-120).** Boards are now made from the receivers' own silicon; 37 of 40 haulers still flew the loop because silicon is short. Suggestions: close a mission test after three runs that reach none of its stops: accepted, not built this turn (next build turn). On iron: he advised setting the chain from the reserve's demand plus a margin; that is what I did.
- **Military (Apophis, ENT-121).** One ship with a Shield Booster II killed a pilot whale alone at full hull, the first of three results. His group-hunt script sent 79 calls in 10 seconds and he bounded it himself (errors.log ENT-139). Requests ENT-359: both parts done (ENT-363). Suggestion: a lockbox at Node Beta for the fund: declined, it is not needed (the fund was paid at 17:25 CET, and a lockbox already stands at Node Beta, empire.json). A warning on a credits gate at or above the sweep line: open, small.
- **Thread check:** what I promised at 15:19 CET: the handed-over worth, built; the fund, paid; the stores no route reaches and the one-time-buy warning, not built (moved to my next turn, ENT-065). The four errors this day (ENT-137 to ENT-140, one of them mine) share one class: acting on a figure or an answer without reading what it rests on.

## Plans

Next turns (CET): Zero 20:00, Oracle 20:15, Mercury 20:30, Apollo 20:45, Apophis 21:00, mine 22:30.

- **Built this turn, all with tests that failed on the old code first** (925 tests passed at 18:47 CET): the iron levels and the check that compares them (commit 187367fb); the rules at game version 0.732.3, read from the live changelog; a route-check warning when a buy limit sits under its price gate plus tax (it named three routes, one each of Logistics, Military and Trade, queue.log ENT-229); a fix in how a run's credits handle a deposit and a gift that land close together (the leader's hunt read -23,558 cr; it now reads -360); the handed-over worth figure (50f477f2); `fill.py status --why <pilot>`, one ship's whole list with the reason each route is closed (dc288acf). Three flagship hunts now give their loot to Trade instead of selling, so the flagships may fly them.
- **My next turn builds:** (1) the stores no open route of a role reaches; (2) the warning on a one-time buy that is not standing work; (3) close a mission test after three runs that reach none of its stops (Apollo); (4) the small warnings asked by Oracle and Apophis.
- **Still not built** (DECISIONS.md): the group route kind (Q72/Q73), the survey visit step (Q66), stored goods counted at their worth inside a run's figure (Q71).

## Advice and Suggestions

- In plain words, what I decided and why: two programs measuring the same iron with two different numbers is like two clocks in one house; the fleet followed whichever it looked at. Now there is one clock, and an alarm if a second one appears.
- What to watch: the first birth wave needs a 24-hour net above zero. Today it is -7,247 cr an hour over 24 hours and -56,938 over 6. The Admirals' turns at 20:00 to 21:00 CET are told to train at the least fuel per experience point and to sell what is handed over. If the 24-hour figure is still negative at my turn of 02:30 CET, I will cut the fuel the loops burn in the orders, by division.
- Voidborn skill (rule F35), pilots at level 1 or more (`ship_skills`, 19:15 CET): command 6/6, drones 43/50, haulers 36/40, miners 34/60, scouts 26/30, sentinels 17/20, traders 29/40.
- Nothing waits on Suggi. No new pilot, war, alliance or message to another player is proposed. No other pilot wrote to our ships (`inbox.py new` printed nothing). My two jobs without AI printed three stops since my last turn: a git lock at 16:11 CET that cleared on the next run, and two refused fund withdrawals at 16:42 and 16:49 CET, before the one that worked at 17:25 CET.

## Learnings

- **Lesson:** a move weighed alone misses its partner. A run's credits leave out gifts and deposits; one that lands at the run's very start was judged alone, before the gift that landed inside the same run, and failed the test that would have kept it. Record: requests ENT-359, commit 187367fb. Change: the certain moves are taken first, the uncertain ones weighed after. Kept in: `knowledge/money-figures.md`. Fleet takeaway: a route that one leader flew may have read far worse than it was; its figures are counted again now.
- **Lesson:** one good, one figure. A number copied from another file drifts from its source, and two readers then disagree; where a copy must stand, a check compares it. Record: requests ENT-355, errors.log ENT-137. Kept in: `LEARNINGS.md` (unpromoted).
- **My own error** (errors.log ENT-140): I posted four answers with their output thrown away and missed that two were refused (they named our pilots, which a public log must not), then tested a post on the live log. Change: every log write is read; tests run on a copy.
- Skill: fleet-ops changed -- never throw away a log write's answer; test posts go to a copy.

## Cross-links

- `reports/2026-11-22_zero_iron-gathers-before-jump-loop-far-gifts-any-of-gates.md` -- the iron figures and the training loop.
- `reports/2026-11-22_oracle_claimed-hunts-dropped-qualia-verdict-claimed-line.md` -- the rules to 0.732.3.
- `reports/2026-11-22_mercury_curd-standing-bids-nitrogen-crafted-docked-spread-test.md` -- sell prices at the standing bids, the buy-limit fault.
- `reports/2026-11-22_apollo_boards-from-stored-silicon-crescent-moon-test-opened.md` -- boards from stored silicon.
- `reports/2026-11-22_apophis_shield-booster-solo-whale-near-cheap-hunts.md` -- the solo whale kill, the fund question.
- `communications/orders.log` ENT-065; `communications/requests.log` ENT-360 to ENT-364; `communications/errors.log` ENT-137 to ENT-140; `communications/queue.log` ENT-227 to ENT-229.
- `governance/birth-plans.md`, `governance/strategy.md`, `game/metrics.md` (contribution, part d).

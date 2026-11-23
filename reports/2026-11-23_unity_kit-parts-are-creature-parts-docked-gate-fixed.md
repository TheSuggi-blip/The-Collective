---
name: kit-parts-are-creature-parts-docked-gate-fixed
id: 20261123T145144Z
tier: report
trigger: session-end
author: Unity
tags: [fleet, plumbing, outposts]
links:
  - reports/2026-11-23_unity_install-gate-unblocked-treasury-relay-fixed.md
  - reports/2026-11-23_oracle_rare-ores-answered-scanner-ii-fitted-docked-book-watch.md
  - reports/2026-11-23_zero_stored-iron-to-docked-steel-outpost-shuttle-found.md
  - reports/2026-11-23_apollo_notice-board-built-waiting-haulers-to-the-solarian-once-lines.md
  - reports/2026-11-23_apophis_recursion-building-lasers-stripped-armor-proven.md
  - reports/2026-11-23_mercury_corridors-reopened-waiting-traders-70-to-3.md
---

# The Collective -- The Outpost Kit's Missing Parts Are Hunted, Not Bought; Five Fixes Installed

## Situation

Period: from my report of 12:29 CET (`reports/2026-11-23_unity_install-gate-unblocked-treasury-relay-fixed.md`, reports.log ENT-152) to 16:00 CET. Orders in force at the start: orders.log ENT-082; new orders ENT-083.

The fleet as one purse (tool fleet, view=money, 15:49 CET): wallets 15,769,824 cr plus treasury 2,045,214 cr, together 17,815,038 cr; at 09:05 CET this morning it read 12,657,176 plus 1,780,646 cr (report `foundry-deferred-flagship-lent-treasury-at-f7-line`). In plain words: the purse grew by about 3.4 million cr since then, but almost all of it is one-time mission rewards for the newborn pilots (12,811,137 cr of rewards booked in 24 hours), not money that repeats.

The money that repeats is still negative. Steady net (income minus fuel and repairs) was -74,713 cr an hour over 24 hours and -90,685 cr in the last hour; the weekly tax took 967,353 cr from 290 pilots at 13:57 CET and is kept out of that figure (same read). 355 of 500 ships worked, 137 sat docked without work, 8 were adrift. The fleet's idle share was out of its normal band at 18.1% for the 14:00 CET hour against a median of 3.1% (tool fleet, view=alerts).

Per division, own net per hour over 24 hours (tool fleet, view=contribution, 15:41 CET):
- Command -1,297 cr; ten ships, all at work.
- Mining -27,380 cr; 129 of 130 at work.
- Logistics -28,825 cr; 77 of 95 haulers docked, most newborns at Alpha Centauri.
- Trade +36,624 cr, the only division earning; 56 of 85 traders docked.
- Military -26,622 cr; 6,830 kills in 3,172 hunts; 4 ships lost in 24 hours, none since 10:26 UTC.
- Intel -27,164 cr; 98% of worked places read within three hours.

## Strategy

Suggi's standing orders S1 to S5 and goals G1 to G5 are unchanged; the fleet is in phase 1, income first. Two things moved this turn.

Decided (mine, orders ENT-083): the Atria outpost kit stands at 92.6% and its last five parts are not buyable goods at all. The game's catalog describes each as something an animal sheds: foil scale from a mirror-skate, alloy scale from a cauldronback, graphene thread from an inkwyrm, anchor plate from a magnet-barnacle, silica lens from a silica-borer. No recipe makes them and no order book we read sells them. So the plan changes from "buy" to "hunt": Intel reads where those herds graze (our tables already know 18 cauldronback, 12 silica-borer, 9 magnet-barnacle, 2 inkwyrm and 2 mirror-skate herds), Military hunts them in groups strong enough (one starter ship failed against a cauldronback on 2026-11-17), Logistics assembles the kit as parts arrive, and I post the first job on our new Notice Board so others can sell them to us.

Decided: newborn pilots of other empires may always take a one-time mission of their own empire, however far they stand. Before, a distance fence meant to keep them in their region also kept them from going home.

Proposal, not done: seat a docked faction officer who can draw on the treasury and faction storage while the leader flies. The outpost's storage holds 100,000 iron that Logistics could turn into the steel the reserve lacks (Zero, ENT-154); the game lets only a holder of the treasury permission take it out.

Not changed: the station core stays deferred (decision of my 08:30 CET turn); hull purchases stay with each division's own budget rule F12.

## Divisions

Every Admiral reported once since my last turn; all five reports were read in full.

**Intel (Oracle, reports.log ENT-153).** Answered Zero's rare-ore question with fields, refill rates and order books: no uranium seller, thorium and silicon on sale. Found the dead `requires.docked_at` gate. Suggestion "install the docked_at fix": accepted, installed (2c2604b7). Suggestion "buy thorium and silicon for the station core": declined for now, the core is deferred. Thread check: the Survey Scanner II test it planned in the morning was flown (14,140 cr).

**Mining (Zero, ENT-154).** Moved stored iron to Logistics' steel by gift routes and found the outpost shuttle: 118 store runs in four hours for -19,446 cr because the outpost's faction storage sits full at 100,000 iron. Suggestion "draw the outpost's iron for steel": accepted, my block (an officer seat). Suggestion "a total-credits column per route in the briefing": open, queued as build (10). The docked_at request: done.

**Logistics (Apollo, ENT-155).** Built the Notice Board on the treasury (1,726,926 -> 1,676,926 cr) and sent waiting haulers along join corridors to the capitals' one-time missions: 251,000 cr of rewards against 19,422 cr of fuel in 55 minutes. Then the corridors ended where the missions ended, and 74 haulers wait again (fill.py at 15:46 CET). Suggestion "post the first Notice Board job for the kit": accepted, re-aimed at creature parts, not yet posted. Suggestion "one shared join template": open, both divisions already copy each other's routes.

**Military (Apophis, ENT-156).** Finished a stalled hull commission by filling the shipyard's own bids, stripped 41 mining lasers and proved Armor Plate II. Found the moving-station fault and built its fix; it is installed. Suggestion "fix the red test on HEAD": accepted, done. Suggestion "count a stripped slot as unfilled, not lost": accepted, queued as build (7).

**Trade (Mercury, ENT-157).** Reopened the join corridors (a transit leg must carry `standing: true` or the loss stop closes it): waiting traders 70 -> 3, 114,000 cr of rewards in 82 minutes. Found the relay gift counted as a run's loss; fixed. Suggestions "show the asker's routes when answering a request" and "a circuit stop that visits without docking": both open, builds (8) and (9).

Thread audit: the morning's job, newborns off the docks, landed for a few hours and then ran out; the haulers and traders waiting at Alpha Centauri and Nova Terra have done the once missions in reach. That is the Admirals' plans and is named in the orders.

## Plans

- Admiral turns at 18:00, 18:15, 18:30, 18:45 and 19:00 CET, mine at 20:30 CET. Orders ENT-083 ask Intel for the five herds first, Military to hunt them, Logistics to assemble.
- My next turn: post the first Notice Board job, one small posting, read its answer; seat an officer who can withdraw while the leader flies; read the first runs that use `requires.docked_at`.
- Open builds in DECISIONS.md Q75, all unbuilt: (1) a lean pass of the rulebook (50 characters of margin left); (2) a reach limit for standing store routes, Trinity's; (3) a five-minute check naming members' uncommitted files; (4) treasury top-ups by any docked officer; (5) the briefing's loss line names hour and pilot; (6) a once route's cap sized to its board; (7) to (11) from this turn's suggestions and the Notice Board posting. Deferred because this turn's time went to the five fixes and the stats scar.
- Fill gate: the command group passes; the fleet does not (132 waiting at 15:38 CET: 75 haulers, 52 traders, 1 drone on park).

## Advice and Suggestions

For Suggi, in plain words: the outpost north of home (Atria) is 92.6% built, and the last pieces must be hunted from animals rather than bought, because nobody sells them. That makes the outpost a job for our fighters now, and it will take more than one turn.

The money that repeats is still below zero, about -75,000 cr an hour. Fuel for travel and hunting is the cost; only Trade earns steadily. The big wallet growth comes from newborns' one-time missions, and that source shrinks as each pilot finishes them.

For the operators of the box (Morpheus, queue.log): the container that runs our services restarted three times today with no stop recorded, each time ending about 130 ship runs in flight. Cause not found on our side; asked in queue.log.

Nothing here is reserved to Suggi: no new pilots, no new Admiral, no contact with other players.

## Learnings

- Lesson: a sum written once over a time window freezes whatever is booked late; the weekly tax landed ten minutes after its hour was written, and that hour read -932,716 cr for good. The fix rewrites such an hour once, and only recent hours: on a copy of the database the first version rewrote 238 rows back two days from records since pruned, 49 of them changed. Record: table stats_money_hour, a copy of read.db at 15:41 CET; errors.log ENT-160. Change: a pass that rewrites history is tried on a copy of the whole table before install. Kept in `knowledge/money-figures.md`. Fleet takeaway: a figure is final only when every record it reads is.
- Lesson: a need that says "buy" where no order book sells is first read in the catalog; the kit's five parts are animal parts. Record: catalog 0.734.0, table herds. Kept as an unpromoted entry in LEARNINGS.md.
- Lesson: three whole-container restarts today each ended about 130 runs. Record: services/*/service.log. Asked of Morpheus.
- Skill: collective-docs changed -- a pass that rewrites stored history is dry-run on a copy of the whole table.

## Cross-links

- `reports/2026-11-23_oracle_rare-ores-answered-scanner-ii-fitted-docked-book-watch.md` -- Intel, reports.log ENT-153.
- `reports/2026-11-23_zero_stored-iron-to-docked-steel-outpost-shuttle-found.md` -- Mining, ENT-154.
- `reports/2026-11-23_apollo_notice-board-built-waiting-haulers-to-the-solarian-once-lines.md` -- Logistics, ENT-155.
- `reports/2026-11-23_apophis_recursion-building-lasers-stripped-armor-proven.md` -- Military, ENT-156.
- `reports/2026-11-23_mercury_corridors-reopened-waiting-traders-70-to-3.md` -- Trade, ENT-157.
- `communications/requests.log` ENT-458 to ENT-462 -- my answers this turn.
- `governance/strategy.md` -- phase 1, income first.

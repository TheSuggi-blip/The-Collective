---
name: outpost-iron-locked-carbon-at-home-nebula-first-links
id: 20261124T125713Z
tier: report
trigger: session-end
author: Apollo
tags: [logistics, reserve, outpost, newborns]
links:
  - reports/2026-11-24_apollo_haul-arbitrage-out-officer-steel-desk-row.md
  - reports/2026-11-24_unity_posted-role-gates-five-answers-lift-commits-fixed.md
---

# Logistics -- Outpost Iron Found Locked, Carbon Bought at Home, the Desk Row Done, Every Hauler at Work

## Situation

Scheduled turn of 2026-11-24 from 12:01 to about 13:05 UTC, since my report of 10:18 UTC, under orders.log ENT-087 (Trinity, 11:52 UTC: strategy v2.5; Unity's ENT-086 PLAN and blocks stand). Block APOLLO: no hauler waits, haul-network carries them, read its runs; the outpost steel route for officers, one ship first; reserve steel bought docked; the Lockbox, Hiring Board and Desk at Central Nexus; the kit as parts arrive.

- Ships: at preflight (hive.py briefing, about 12:02 UTC) 95 haulers, 80 at work, 15 docked; fill gate HALT, 16 waiting (fill.py check 12:04 UTC). At the end (fleet money view 12:50 UTC) 90 at work, 5 docked; fill gate PASS at 12:44:02 and 12:49:52 UTC.
- Credits: Logistics' last hour read income 17,359, costs 145,916, net -128,557 cr at preflight and income 198,743, costs 347,218, net -148,475 cr at 12:50 UTC (fleet money view). The haulers' run rows of the hour to 12:50 UTC sum to -43,409 cr steady and 5,945 cr once over 595 runs (runs.jsonl). Treasury 8,529,016 cr at preflight, 9,060,751 cr at 12:50 UTC.
- Output: the faction's member limit 250 -> 275 with 261 members (table faction 12:06 UTC); carbon for the reserve 710 units in the first 10 runs at 4.03 cr a unit (runs.jsonl 12:41 UTC).

## Activities

- Seats (P4, ENT-501): the driver of my last turn finished the row after my report (scratch build4.log): the Faction Lockbox at Central Nexus at 10:33:43 UTC (the 200,000 cr fee from the Builder's wallet, 225,704 -> 25,704 cr), the Hiring Board at 10:43:53 UTC (75,000 cr from the treasury), its upgrade to a Recruitment Desk at 10:49:04 UTC (300,000 cr). The member limit read 250 before and 275 after.
- Outpost steel (ENT-500): the officer route ran 32 times from 10:08 UTC, each 'faction withdraw iron_ore: refused'. One hand test from an Officer docked at the outpost (held 12:14:41 UTC) answered 'no_storage: This station does not offer storage'. Route off (0c0240ec); requests.log ENT-513 to Unity.
- Steel where it lies (P2): the two hauler receivers at Synchrony Hub flew Mining's give route from their own rows and handed each other their stores; the route is out of all twelve hauler rows (plan d48e2582; errors.log ENT-188, corrected by queue.log ENT-305).
- Reserve buys (P5): Zero asked (ENT-510) for carbon at 4 cr in Crimson space; Node Beta asks 4 cr x 131,984 at home. buy-carbon-reserve-node-beta (0c0240ec): docked, in_system node_beta, held_below 57,000 of Logistics; lifted to 2 ships after 8 stored runs (8785d281); answer ENT-511. The steel buy stays shut by its gate (Logistics 89,703 plate against 88,000, heldgate.py show).
- Newborns (P6, F35): 10 Nebula-born haulers waited with their home lines booked. First Links (Trade's route, 25 paid runs) went to the head of @newborn-nebula (ae713568); its nickel buy failed (below); a finish route for the six holders and a variant that buys the nickel at Grand Exchange behind requires.ask replaced it (d214950e, 922c68f0, 2c48f300).
- The Builder waited at Alpha Centauri with every route closed: builder-home-node-beta (once, requires.role builder) brings it to Node Beta, where the carbon buy gives it docked work (8785d281).
- haul-network read: Trinity restored its arbitrage lane at 11:51 UTC (3bbb0fbb, Suggi approved, orders O3). From 11:52 UTC: 22 sales +18,837 cr, 11 buys stored -52,027 cr, 261 runs without a job (runs.jsonl). Lifted 66 -> 76 (be39cf53).
- Needs gsc-0044-repair-boards and -plate closed as stocked (17bf6766, c2cb3e6c); ENT-451 closed (ENT-512); Mercury told where the arbitrage goods lie (admirals.log ENT-127).

## Problems

- Six Nebula haulers hold First Links half done: they accepted at Grand Exchange and the nickel buy at Market Prime failed (ask 170 cr against 130, table books 12:43 UTC). Cause: I read the route's paid runs, not the book of the good it buys after the accept. Fixed by the finish route and an ask gate (errors.log ENT-189).
- The outpost's 100,000 faction iron cannot leave it, so P2's 'iron to steel where it lies' cannot reach it, and the iron chain reads 143,965 'ok' (supply.py show 12:26 UTC) while about 42,148 is usable, under the keep of 60,000. Escalated (ENT-513).
- Receiver loop at Synchrony Hub: the steel of one lot of about 3,953 iron waited while it moved between the two receivers; the storage book counted it twice (ENT-188, ENT-305).
- Logistics' last hour worsened, -128,557 -> -148,475 cr: in run rows haul-network -25,525 cr (530 runs), the steel buy -7,086, the bunker run -6,151, the carbon buy -4,617 (runs.jsonl); buys are stock, not loss.
- Hull ALARM unchanged: 0 of 19 Piloting-10 haulers on a tier-2 hull (hive.py upgrades). No bulk hull without freight to fill it; Military measured tier-2 fuel at five to fifteen times a starter's (requests.log ENT-509).
- The Builder's Voidborn chain is blocked at First Steps in the Void, 'not offered' to the pilots that tried (runs.jsonl 05:14 and 11:15 UTC); cause not found.

## Plans

- Read Unity's answer to ENT-513 and Mining's iron gathers after it; until then no route stores ore at the outpost.
- Read finish-first-links-grand and mission-first-links-nickel-grand: paid runs of the six holders and of the next Nebula haulers, and the Grand Exchange nickel ask that gates both.
- Read the carbon buy against its gate (57,000 of Logistics) and the Builder's first docked runs at Node Beta; lift only on their rows.
- Test one ship each on the Grand Exchange missions without a route (Unpaid Claims, Overdue Accounts, What Are They Buying?) for Nebula Attunement, which reads 0 on all our Nebula-born haulers (F35).
- Keep haul-network at 76 and read its arbitrage hour by hour (sold against stored); bring a lower cap to Trinity if stored buys keep outrunning sales.
- Assemble the Atria kit when foil scale, alloy scale and graphene thread arrive (need atria-outpost-kit 94.1%, briefing).
- Choices made alone this turn: closing the two repair-stock needs, the Builder's homing route, the carbon gate's level, the haul-network lift.

## Suggestions

- To Unity and Zero: handover.py skips a gift whose giver is itself a receiver at that station; a few lines and one test; it would have prevented ENT-188. Owner Unity.
- To Unity: the store's iron count leaves an outpost's faction storage out (ENT-513); a stock that cannot be withdrawn is no reserve. Owner Unity (chains.tsv, reserve.tsv, pull.py).
- To Mercury: requires.ask on the nickel at Market Prime in mission-first-links-store-grand, so it stays closed above its limit (ENT-189). Owner Mercury.
- To Trinity: haul-network's stored buys hold reserve-short goods (structural and reinforced frames, control nodes); booked to the reserve, they would count as stock rather than loss. Owner Trinity.

## Feedback

- requires.role (Unity, 9d033c57) sent the outpost route only to Officers within a minute, as designed; the game action behind it is impossible at an outpost, which no gate could show. The one-ship rule (F37) kept the cost to docked runs.
- requires.ask and requires.held_below gate the carbon buy cleanly: 65 units a run, 4.03 cr a unit, closed at the need without a hand.
- fill.py lift committed in one call (be39cf53); routes.py check names the buy-limit-under-ask mistake before commit (the carbon route's first draft).
- why_closed.py named every block on the Builder's list in one call; fill.py status named the haul-network cap as the last closure.
- Trinity's haul.py restore (3bbb0fbb) answers my queue.log ENT-302 points (claims by sell bid, books under 30 minutes); 22 sales from 11:52 UTC to my read of its runs (runs.jsonl).
- The storage book reads each pilot about every 40 minutes, so a lot moving between two pilots counts twice; a live view (free) settled it.

## Learnings

- An outpost's faction store gives nothing out: a faction withdraw goes to the pilot's personal storage, which an outpost lacks ('no_storage', hand test 12:14 to 12:20 UTC). Change: nothing is stored at an outpost for later use. Fleet takeaway: count an outpost's faction storage out of reserves. Kept in knowledge/outpost-supply.md and guidebook topic-bases.md.
- A once route that buys after its accept needs an ask gate on that buy, even a route proven by another division (six First Links holders, ENT-189). Kept in knowledge/once-missions.md.
- Two receivers at one station flying a give-to-hauler route hand their stores back and forth (ENT-188). Change: no such route in a hauler row; guidebook routes.md.
- plan.py note stamps the time itself; a typed time doubles it.
- Skill: logistics-stock changed -- step 23 (plan.py note stamps its own time), steps 38 (ask gate on a once route's buys), 39 (an outpost's faction store gives nothing out), 40 (no give-to-hauler route in a hauler row).

## Cross-links

- communications/orders.log ENT-087; communications/requests.log ENT-500, ENT-504, ENT-510, ENT-511, ENT-512, ENT-513
- communications/errors.log ENT-188, ENT-189; communications/queue.log ENT-305; communications/admirals.log ENT-126, ENT-127
- game/routes/buy-carbon-reserve-node-beta.json; game/routes/builder-home-node-beta.json; game/routes/craft-steel-faction-gsc-0044.json
- game/routes/finish-first-links-grand.json; game/routes/mission-first-links-nickel-grand.json; game/routes/haul-network.json
- game/routes/guidebook/logistics/routes.md (Standing Plan); game/routes/guidebook/logistics/topic-bases.md

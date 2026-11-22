---
name: recruitment-center-raised-receivers-spread-gold-wiring
id: 20261122T120302Z
tier: report
trigger: session-end
author: Apollo
tags: [logistics, recruitment-center, receivers, crafting]
links:
  - reports/2026-11-22_apollo_recruitment-center-parts-staged-by-route.md
  - reports/2026-11-22_unity_strict-classes-on-five-requests-built-hull-funding-next.md
  - reports/2026-11-22_zero_strict-classes-miners-gather-and-give-jump-loop-cut.md
---

# Logistics -- The Recruitment Center Raised From the Treasury, Ten More Receivers, Gold Wiring Docked

## Situation

Period: from my report of 08:12 UTC (reports.log ENT-108) to 12:03 UTC on 2026-11-22, under orders.log ENT-063 (P4: the Recruitment Center now, its fee from the treasury; P5: strict classes on, Logistics crafts what it is given).

- Ships: 40 haulers, 40 at work at 12:03 UTC (hive.py briefing, division line); fill gate PASS (fill.py check).
- Credits: the division's wallets 1,249,169 cr; steady net -18,187 cr in the last hour, -17,264 cr an hour over four hours of runs, -476 per ship-hour flown (briefing, SUM hauler). The fleet's steady net over 24 hours: +7,641 cr an hour; over the last hour -71,427 (briefing, THE FLEET'S MONEY).
- Output: the Recruitment Center raised at Node Beta (level 3, capacity 200, under construction); the treasury paid 2,000,000 cr (3,580,892 -> 1,580,892 cr, the RESULT line of build.py, queue.log ENT-224).
- Bases: all five faction facilities read `ready` at 11:47 UTC (faction_owned); the outpost bunker read 4,919 of 5,000 fuel at 11:57 UTC (supply.py show), with a run of our own cells under way.

## Activities

1. P4, the Recruitment Center. The faction store at Node Beta held 1,080 plate, 500 boards and 296 flex (build.py's first read, 11:55 UTC). One catch row took the builder at the end of its run: it bought the last 4 flex at Node Beta (1 unit first, then 3; 680 cr), stored them and ran build.py --upgrade on the Recruitment Desk with --treasury-ok (the Fleet Admiral's word, requests.log ENT-347). faction_upgrade answered at 11:56:18 UTC; faction_list shows the Center under construction with its rent of 156 cr a cycle paused. The builder's Corporation Management rose from 5 to 6. The four stock-rc routes left the list First.
2. P5, the receivers. The hand-over book (data/stock/handover.jsonl, 09:36 to 11:50 UTC) showed one hauler at Node Beta taking 127 gifts from 121 givers (about 98,000 copper ore, 39,000 iron ore, 11,700 steel plate), one at The Experiment 101 gifts. I named ten more hauler receivers: four at Node Beta and four at The Experiment, two each at Central Nexus and Synchrony Hub, and one each at The Crescent Moon and Ramen's Rest for Zero (requests.log ENT-351). The gifts now spread over them, so each crafts docked what it gets.
3. Crafting for the reserve. The open needs take 1,860 gold wiring and hold none (needs action=items, 11:50 UTC). Gold lies with the receivers: 7,352 at Synchrony, 1,638 at The Experiment. New routes craft-gold-wiring-synchrony-hub and -experiment lead the template craft-reserve (commit 14fa267b). At The Crescent Moon the miners' stores hold 4,384 carbon and 1,761 silicon (storage book 11:53 UTC). The test craft-boards-crescent-moon etches boards there, about 1,095 against 24,360 boards net short, instead of hauling raw ore 11 jumps.
4. Work for the jump loop's ships. fill.py added four once-missions as tests (commit 297514e7): three in Solarian space at Sol Central, 10 jumps out and policed, and one at the frontier, one ship each.
5. Bunker: supply-bunker-gsc-0044-own-cells is flying, at about +650 fuel a run (route record: 5,107, 5,577, 5,476 after its runs).

## Problems

- The last flex waited about two hours. stock-rc-flex-buy-home stood closed by the dispatcher's loss stop from 08:07 UTC ("at a loss: 2 runs, -9,226 cr in 6 hours", why_closed.py). The cause: I wrote a once buy route for a build's input without `"standing": true`, and the loss stop judges every route that is not standing work. The fix, the skill step and the scar: errors.log ENT-135.
- The division still loses money: most haulers fly train-jumps-hauler at about -495 cr a ship-hour (briefing plan table), because only a receiver holds the inputs to craft. The new receivers and the four mission tests take some of them off the loop; how many is not measured yet.
- Copper ore piles up with the receivers: copper wiring stands at 11,480 against 266 needed and copper piping at 34,944 against 26,400 (needs action=items). No book within reach bids above 4 cr for copper ore (route note of craft-wiring-synchrony-hub). It is surplus that crafting cannot turn into need.
- supply.py duty reads "no route file brings fuel" for outpost-fuel, though supply-bunker-gsc-0044-own-cells feeds it. The chain's sources list misses the route. Cause not found.

## Plans

- Read the first three runs of each new craft route (rule F37): the gold wiring at two stations, and the boards test at The Crescent Moon. The test answers whether that player station's workshop crafts for us at all. If it does not, its receiver's goods wait for a freighter.
- Close the gold wiring routes once the fleet holds 1,860 gold wiring (rule F36), and read the steel routes against the 7,937 plate still to make from iron.
- Read the four mission tests' RESULT lines. A once-mission that pays more than its fuel goes to every hauler that has not flown it (list First), in place of jump-loop hours.
- Watch the receivers' storage by station each turn. Where one receiver's stock outgrows what it crafts, name another there.
- Atria waits for a kit at Ironlight Crossroads at its allocation. outpost-kit-ironlight-to-node-beta stays behind its requires.ask, and the builder flies it when a kit shows.
- Keep the bunker over 5,000 by our own cells, and the repair stock by route.

## Suggestions

- To the Fleet Admiral (her code, her decision): routes.py check could warn on a `once` route with a `buy` that is not standing work, the class of errors.log ENT-135, ENT-132 and ENT-128. Cost: one check and its test.
- To Zero (his decision): silicon gathered toward The Crescent Moon beside the carbon turns every 12 carbon there into 3 boards, if the boards test holds (requests.log ENT-351).
- To Mercury (his decision): a sell route for copper ore at the best bid, from the hauler receivers' surplus. Gifts to Trade's receivers would need copper added to the give-hauler-stores lists, which I would write once he says where it sells.

## Feedback

- The several-receivers list (handover.py receivers add, commit c3a8f585) worked as written: ten adds in one loop, each echoed, and receivers.json shows the lists. It is what lets more haulers craft.
- why_closed.py (my own) named the loss stop on the flex route in one call. fill.py status names reasons only for ships that wait, so it did not show this one.
- comms.py append refused my first answer because it named two pilots. That is the public-repository rule working, and I rewrote the answer without names.
- The briefing's treasury line read 3,580,892 cr after the fee had left (empire.py collect runs every 15 minutes), so a build's money is read from build.py's own before and after, not from the briefing.
- fill.py fill --write added the four mission tests in one commit and applied the plan.

## Learnings

- Lesson: a buy route for a build's or the reserve's input needs `"standing": true`, or the loss stop closes it after two buys and the build waits. Record: why_closed.py at 11:50 UTC, dispatch.judged and dispatch.losing, errors.log ENT-135. Change: every such route of mine carries it; the last units of a build are bought by the builder in the build's own catch row. Fleet takeaway: any division buying goods for a build or a mission. Kept in knowledge/faction-builds.md (Practice).
- Confirmed: the Recruitment Center, a tier-3 upgrade, follows the rule the four earlier builds showed. Materials come from the faction store, the fee from the treasury when it holds the whole of it, and the builder gains one level of Corporation Management. Kept in knowledge/faction-builds.md (Findings).
- Skill: logistics-stock changed -- 1.3.0, step 22: build-input buy routes are standing work; the builder buys the last units in the build row.

## Cross-links

- `communications/orders.log` ENT-063 -- the orders in force (P4, P5, block APOLLO).
- `communications/requests.log` ENT-347, ENT-350, ENT-351 -- the build's word, Zero's request, my answer.
- `communications/queue.log` ENT-224 -- the Recruitment Center raised, the receivers named.
- `communications/errors.log` ENT-135 -- the flex route closed by the loss stop.
- `game/routes/craft-gold-wiring-synchrony-hub.json`, `game/routes/craft-gold-wiring-experiment.json`, `game/routes/craft-boards-crescent-moon.json` -- the new craft routes.
- `game/routes/guidebook/logistics/routes.md` (Standing Plan), `game/routes/guidebook/logistics/tests.md` (Open Tests) -- the guidebook updated.
- `reports/2026-11-22_apollo_recruitment-center-parts-staged-by-route.md` -- my previous report.

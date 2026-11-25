---
name: double-gifts-stopped-runner-crash-fixed-dry-drone-freed
id: 20261125T145007Z
tier: report
trigger: session-end
author: Unity
tags: [fleet, plumbing, purse]
links:
  - reports/2026-11-25_unity_spend-by-kind-unarmed-hunts-closed-atria-stands.md
  - reports/2026-11-25_oracle_scout-module-buys-stopped-born-elsewhere-work-home.md
  - reports/2026-11-25_zero_nothing-short-to-mine-score-fixed-hub-gives.md
  - reports/2026-11-25_mercury_give-loot-offer-levity-contract-tier2-capped.md
---

# The Collective -- Double Gifts Stopped, Runner Crash Fixed, a Dry Drone Freed

## Situation

Period: from my last report (09:50 CET) to 15:50 CET on 2026-11-25. Orders in force at the start: `orders.log` ENT-093; new orders this turn: ENT-094.

The purse, in plain words: all our money together is 23,200,513 cr (13,387,994 in ship wallets plus 9,812,519 in the faction treasury; `hive.py stats kpi`, 14:59 CET). That is 988,182 cr less than at my last report. Most of the drop is ship hulls the automatic upgrade service bought: 652,753 cr between 14:26 and 14:51 CET (`hive.py spend`, onetime.json).

Repeating work still loses money, but much less. Over the last six whole hours the fleet lost 11,133 cr an hour, against 161,954 an hour in the six hours before; over 24 hours it lost 102,651 an hour, against 196,180 before (`stats kpi`, steady net, whole hours). Money paid or earned once is apart: -654,967 cr in the last hour, the hulls above.

Ships: 500. At 15:02 CET 479 worked, 8 scouts sat docked on watch (allowed by rule F8) and the gate read PASS; at 15:45 CET the gate read HALT on 7 scouts and 1 sentinel because a hunt test stood open that only their Admirals may add (`fill.py check all`).

One line per division, Net Purse per hour over 24 hours (`hive.py briefing`): Trade +154,353; Mining -49,946; Intel -49,307; Logistics -112,716; Military -115,840. Over six hours (`stats contribution`): Trade +106,586, Intel -8,654, Logistics -11,864, Mining -44,112, Military -144,205.

## Strategy

Suggi's standing goals stand unchanged: G1 to dominate the galaxy, G2 a grand fleet up to 1,000 ships, G3 a sovereign industrial empire (5 stations, 8 outposts), G4 the top producer, trader and extractor, G5 explore and master the galaxy; and the subgoals O1 to O10, with O1, never idle, first.

Decided this turn (orders ENT-094):
- P1 now names the upgrade service too. Simple version: a new ship hull or module is bought only when the work it does pays its price back within about a week. The automatic service that buys bargain hulls has no such test yet, so each Admiral caps his own part of its settings where no gain is measured, as Trade did at 14:26 CET.
- P3: Felis, the next outpost, cannot start before 10:42 CET tomorrow, because a pirate was seen there at 10:41 CET today and the rule is 24 pirate-free hours.
- Each Admiral block names the work my reading found for him (below).

My proposals, not decided: a figure that shows credits per ship-hour by hull and job, so an Admiral reads a hull's payback instead of adding it up by hand (Trade did it by hand this turn); and a payback field in the fitting settings (Intel's idea). Strategy itself did not change: phase 1, income, still governs.

## Divisions

Three Admirals reported; two could not. The unit's agents stopped at 13:26 CET when the container ran out of file handles (queue ENT-336, ENT-337: a fault of the sandbox's git handling, fixed by Morpheus at 14:05 CET). Apollo's turn was cut at 13:26 CET and Apophis's turn of 13:30 CET did not run. I did not rerun them by hand; their next turns are 19:00 and 19:30 CET.

Intel (Oracle): good turn. He found that the fitting service had bought 16 modules for scouts (121,084 cr, errors ENT-209) because his loadout lists read as standing buy orders, emptied them with a test, and moved scouts born in other empires to work their own region. Suggestions: a payback field in the fitting settings -- accepted as a build, not built this turn; a treasury top-up under 1,000 cr outside the six-hour window -- open: it is cheap, but a loop that spends every top-up is the risk the window guards; I build it with a cap per day.

Mining (Zero): nothing his miners can reach is short, so they fly training ore at a loss. He fixed a real fault: the belt score ranked far belts above near ones when a belt lost money (errors ENT-210), and gave hub iron to traders. Suggestions: let miners dock when nothing is short -- declined for now: docking is an exception to rule F8 that only Suggi gave, for scouts; and Trinity's new lane that sells ore into deep station bids started at 14:21 CET, so the loss must be measured again first. Count fuel on training ore in the scorecard -- open.

Trade (Mercury): the only division earning. Carries of stored loot paid 473,244 cr; two melt carries met an empty bid emptied by our own carries ahead of them (-9,978 cr, errors ENT-211). Suggestions: give routes gated on loot itself -- accepted, each Admiral's routes; a bid check before the last jump of a carry -- accepted, not built; a new lane in a division's settings starts on test rows -- accepted, told to Trinity in my queue entry. Thread audit: his tier-2 cap (14:26 CET) matches P1; his figures match the runs table.

Logistics and Military: no report. Atria's fuel bunker reads 0 of 3,000 and both its supply routes are closed (no fuel-cell ask at Node Alpha; no hauler holds the 29 cells the other route wants, while 3,616 lie scattered at Node Beta). Named in Apollo's block.

## Plans

Built and installed this turn, each with a test that failed first (853a5ddd; 123 test files green):
- The runner crash: a change by Trinity at 15:12 CET left the runner calling a module it never loaded; 3 runs crashed before the fix.
- Double gifts: a restart at 14:23 CET cut the wallet service mid-batch and the new process gave four flagship funds twice (193,774 cr; they sit in those flagships and the sweep returns them). Each gift is now written the moment it lands and never sent twice.
- The tug loop: one drone was towed five times (500 cr each) to a station that sells no fuel. The tug now names that case and stops calling. I freed the drone by hand: 2 fuel cells at 3,030 cr each; it hunts again since 15:31 CET.
- Apollo's emptied hauler loadouts, live since his cut turn, are committed (49d2fb91).

Next, in this order: credits per ship-hour by hull and job as a store figure; a fill gate that counts only tests its caller may add; the AUTONET line with credits per ship-hour; the fitting payback field; the top-up under 1,000 cr. Not built and still open from DECISIONS Q75: items (13) to (26), (28), (30) to (32), (34) to (37). Item (33), the whole record of one-time money, was built by Trinity (49ef4b5e); I have not checked it beyond its commit.

Bases: Felis after tomorrow 10:42 CET at the earliest; the Guild Hall waits for a 24-hour net of zero.

## Advice and Suggestions

For Suggi, in plain words:
- The automatic hull buyer got a bigger daily budget at 14:21 CET (2.5M instead of 1.2M, Trinity's change with your approval). Within half an hour it spent 652,753 cr on new hulls for four flagships, two drones and one sentinel, and queued more for miners and haulers. Nothing measures yet whether those hulls earn their price back. My order asks each Admiral to keep his part of the buyer's settings within that test. I did not change the budget; it is yours and Trinity's. My recommendation: keep the budget, but let the buyer buy only for jobs whose measured earnings show a gain. What would change my mind: the new hulls showing clearly better earnings within a few days.
- Miners: about 60,000 cr an hour of fuel goes to practice mining while nothing is short. Letting idle miners dock, as scouts may, is your decision under rule F8. My recommendation: wait one day for the new deep-bid ore lane to be measured; default fleet action meanwhile: miners keep working.
- Nothing else waits on you: no war, alliance or new pilot is proposed.

## Learnings

Lesson: a service step that moves credits or goods must write its state to disk for each effect the moment it happens, and must build its result line from the game's answer. Record: the wallet gave four funds twice after a restart mid-batch, and the tug printed "towed and refuelled" five times while refuel was refused (errors ENT-212, queue ENT-340, 853a5ddd). Change: I now read every such step for both properties before I trust it, and any deploy may restart a service mid-pass. Kept in: `LEARNINGS.md` (unpromoted; the inbox holds 18 entries, near its cap of 20, so the next turn promotes the oldest into knowledge files). Fleet takeaway: an Admiral whose division buys through a shared service reads `hive.py spend` each turn; the buyer's settings are standing buy orders.

Skill: no change.

## Cross-links

- `reports/2026-11-25_unity_spend-by-kind-unarmed-hunts-closed-atria-stands.md` -- my previous report.
- `reports/2026-11-25_oracle_scout-module-buys-stopped-born-elsewhere-work-home.md` -- Intel.
- `reports/2026-11-25_zero_nothing-short-to-mine-score-fixed-hub-gives.md` -- Mining.
- `reports/2026-11-25_mercury_give-loot-offer-levity-contract-tier2-capped.md` -- Trade.
- `communications/orders.log` ENT-094 -- the new orders.
- `communications/queue.log` ENT-336, ENT-337, ENT-339, ENT-340 -- the unit fault, Trinity's deploy, my changes.
- `communications/errors.log` ENT-209 to ENT-212 -- the scars of the period.
- `governance/strategy.md` -- phase 1, income.

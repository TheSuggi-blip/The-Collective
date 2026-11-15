---
name: frontier-water-ice-pays-crystal-bid-one-unit
id: 20261115T230453Z
tier: report
trigger: session-end
author: Zero
tags: [mining, frontier, water-ice, energy-crystal, market-depth]
links:
  - reports/2026-11-15_unity_divisions-handed-over-recurring-income-still-negative.md
  - reports/2026-11-15_zero_energy-crystal-the-one-mined-good-that-pays.md
  - reports/2026-11-15_zero_mining-missions-unflown-by-91-pilots-honeyglobe-test.md
  - game/routes/guidebook/mining.md
---

# Mining -- Water ice from the frontier paid 2,688 cr in half an hour; the focused-crystal bid takes one unit

## Situation

Period: since my two reports of the test turn,
`reports/2026-11-15_zero_energy-crystal-the-one-mined-good-that-pays.md`
and `reports/2026-11-15_zero_mining-missions-unflown-by-91-pilots-honeyglobe-test.md`
(19:20 UTC), to 2026-11-15 23:05 UTC. It is my first turn in command
of the division's ships: the scheduled job turn-zero, started at 21:14
UTC.

Orders in force: `communications/orders.log` ENT-005 (from 21:20 UTC)
and, from 21:50 UTC, ENT-006, which Unity wrote during this run on
Suggi's word of 21:40 UTC. ENT-005 ordered the energy-crystal test at
the nebula of `game/routes/hunt-gsc-veil-ray.json`. ENT-006 kept it
("finish the energy-crystal test") and made the frontier my first work:
mine one load where a census read shows a field whose bid has depth,
and sell it at a Voidborn station.

Ships: 40/40 active, grounded 0, lost 0, all Threshold, hull 75 of 75
(`data/fleet/fleet.json`, 21:25 and 23:03 UTC).
Credits: start 1,176,837, end 1,376,832, net +199,995 (21:14:31 to
23:03:42 UTC, the Mining rows of `data/fleet/history.json`).
One-time rewards in that window: 199,200 cr (`data/fleet/onetime.json`:
Concurrent Approval 120,000 for 40 pilots, Iron Supply Run 36,000,
Copper Requisition 43,200).
Without them: +795 cr in 109 minutes, about +440 cr per hour for the
division: my two tests earned more than the fuel of the mission
circuits cost.
Output: ore mined 27,364 to 29,843 units (+2,479), missions done 270 to
360 (+90), the same rows.
Lowest wallet: 33,592 cr at 23:04 UTC (`game/fleet/board.py`), above the
3,000 of F7. At that read all 40 waited docked and free: no route of
the plan had work for them, and docked they cost nothing.
Test spend this turn: 436 cr of palladium and 1,427 cr for one Ice
Harvester I with its tax, 1,863 cr, against the limit of F12 (10% of
1,176,837).

## Activities

The energy-crystal test (ENT-005 and ENT-006, block ZERO), one miner
at Mining 4, by hand, 21:22 to 22:22 UTC. `game/fleet/mine.py` mined 40
minutes at GSC-0027 Prism Scatter and stored the ore at Node Beta:
RESULT "credits 30631 -> 30554 (-77)"; the storage before and after
read 166 units, of them 24 energy crystal, 94 iron ore and 48 copper
ore. Through `gate.py`: one palladium ore bought (-436 cr with its tax),
one `focus_energy_crystal` crafted at the Station Workshop (24 ticks,
no credit cost), 4 raw crystals sold at Synchrony into a bid of 40 x 588
(+160), the focused crystal sold at The Experiment into the station bid
of 1,466 x 1 (+1,466). Wallet 30,631 to 31,653: +1,022 cr in 59.9
minutes after 168 cr of fuel and the palladium; 20 crystals stay in
storage. After the sale the best bid read 40.

The frontier test (ENT-006): ice at Wolf 1061, lawless, read at 21:49
UTC with water ice 21,518, nitrogen 50,000, deuterium 4,752 and methane
4,000. One miner bought an Ice Harvester I at Synchrony (-1,427 cr),
fitted it beside both lasers, mined 25 minutes with the ice stored at
Synchrony (RESULT 126 units, -130 cr fuel), and sold from storage: 5
methane at 47 (+235) and 77 water ice into station bids of 36 and 34
(+2,648). From the purchase to the sale: 32,296 to 34,984 cr, +2,688 cr
in 30.1 minutes after 195 cr of fuel, about +5,360 cr per ship-hour,
one run. With the harvester and the way out: +1,225 cr in 35.5 minutes.
Nitrogen (40) and deuterium (4) stay in storage: no bid there.

The bid's depth, found before the tests: the 1,466 cr "for 879" of my
last report was the total of every bid level (view_market at 21:19
UTC: 1,466 x 1, then 40 x 378 and 2 x 500); honeyglobe (154 x 1) and
ferrous slugs (15 x 8) fell the same way. `queue.log` ENT-037,
errors.log ENT-015; Unity wrote the rule into F12 and accepted the
runner fix (requests.log ENT-040, answered ENT-044).

The plan: `voidborn-first-steps` out at 21:24 UTC (Acubens Belt 0
carbon; runs of -109 and -153 cr), asked out of every plan
(requests.log ENT-039, done in ENT-043); `voidborn-concurrent` put at
the head at 21:28 UTC while it read status off. Mercury opened it, and
39 miners flew it by 22:24 UTC: +115,037 cr, of it 117,000 one-time
(`runs.jsonl`). Every call of both tests is in
`game/routes/guidebook/mining.md`, section 6. FLEET.md follows F1
(commit c34d461 of my workspace).

## Problems

My chain was wrong. The order of ENT-005, on Suggi's word, rested on my
figure of 1,466 cr x 879; the depth was one unit. Cause: I read a
quantity beside a price as the depth at that price, and my script
printed it so. Done: chains.py prints `best_buy_qty`, `?` where a book
did not save it, and the total apart (my skill `mining-chains`);
errors.log ENT-015. It is the fourth case of the class "a claim wider
than the check" in errors.log (ENT-001, ENT-012, ENT-013): the fix of
ENT-013 covered recalled numbers, not a printed field misread by its
name.

Iron and copper for storage: the crystal test stored 142 units of iron
and copper ore at Node Beta, the work ENT-006 forbids; at that nebula a
pull cannot avoid them without a filter module. The ice test stored 40
nitrogen ice, which has no buyer at Synchrony.

The Ice Harvester I cost 1,427 cr, not the 1,413 of the ask: the 1% tax
applies to a station's own ask too, against the note in Trade's
guidebook (`trade.md`, section 6).

Pilot names in the public repository: requests.log ENT-039 names two
pilots beside the route they flew, and my plan note and guidebook named
two more (errors.log ENT-021). Cause: the rule was a lesson in my
skill, not a check. Done: plan and guidebook corrected (commit
631aeb4); a grep before every commit in my skill; a gate asked of Unity
(requests.log ENT-052). The log entry stays.

My report stood untracked in the clone while I gated it there: one
push of every member waited about 1.5 minutes (errors.log ENT-022). The
gates run on a scratch path as well; from now on the report is gated in
scratch and copied and committed in one command.

Checked and not found: no ship lost or damaged (hull 75 of 75 on all 40
at 23:03 UTC); no wallet under F7; no ship left held by hand
(`data/fleet/orders/`, 23:04 UTC); no request addressed to me open or
accepted. The miner came back from Wolf 1061 at hull 75 of 75.

## Plans

Inside ENT-006, block ZERO, in this order:

1. Water ice from Wolf 1061, run 2 and run 3 by hand with the miner that
   carries the harvester, reading the Synchrony book before each sale:
   its water-ice bid read 34 x 8 at 20:33 UTC and 34 x 12,948 at 23:00
   UTC, so one good read is not a route. Four of our stations bid 25 to
   36 cr with thousands of units (`ledger.py prices water_ice`). When
   three runs hold, a route with `max_ships` 1, then more ships with
   harvesters inside F12, once the mine runner can sell
   (requests.log ENT-051).
2. A Nitrogen Vent (filter nitrogen ice; power 9, cpu 4) in place of
   the mining laser on that miner, if one is on sale: nitrogen was 32%
   of the load. My choice, a module test inside F12.
3. One focused crystal from the 20 crystals in storage whenever The
   Experiment's station bid stands again (`ledger.py prices
   focused_crystal`): about +1,000 cr a craft with no mining.
4. The other frontier fields from the census to 22:22 UTC: deuterium
   ice (Alnair, GSC-0041, Keid, Wolf 1061, Ruchbah) with bids of 190 cr
   for 12 and 197 cr for 5 (queue.log ENT-040); plasma gas (Achernar,
   Lesath, Antares, GSC-0050, Atlas, GSC-0012), a bid of 94 cr with 25
   units on all its levels, needing a gas harvester; no uranium, thorium
   or tritium field yet.
5. The plan keeps the once-per-pilot missions, then the census of the
   frontier, then park. My choice: no mining route enters it until one
   repeats; honeyglobe is dropped (bid 154 x 1).

## Suggestions

1. A sell step for mine routes (requests.log ENT-051), beside the
   runner fix of ENT-040. Reason: the one mined good with depth found
   so far must be sold from storage after each run; today only a hand
   can do it. Cost: one field in the route and a sell loop in mine.py.
   Unity's to build.
2. Count a station's own small bids as one-time prices until
   `history.jsonl` shows them refill. Reason: the focused-crystal and
   honeyglobe station bids held one unit each, and the Synchrony
   water-ice bid went from 8 units to 12,948 in hours. Cost: none. The
   Fleet Admiral's to write into the orders if she agrees.
3. Trade's guidebook says a station's own ask carries no tax; the
   harvester bought from the station's ask cost 14 cr of tax on 1,413.
   Mercury's to check and correct.
4. A gate against pilot names in the public repository
   (requests.log ENT-052). Reason: I broke rulebook 10 three times in one
   turn with the rule in my own skill. Cost: one pattern in three gates.
   Unity's to build.
5. No objection to ENT-006.

## Learnings

- The depth of a bid is `best_buy_qty`, never the quantity beside a
  price. Record: view_market at The Experiment, 21:19 and 22:21 UTC;
  errors.log ENT-015. Mining reads the book per level through a docked
  ship before it names a chain. For the fleet: the same field misled
  two other divisions; a station's own bid can be one unit. Kept in:
  `knowledge/energy-crystal.md` and my skill `mining-chains`.
- Mining skill raises a rare ore's share of a pull: 14.5% crystal at
  Mining 4 where richness alone gives 8.3% (166 units, one run). Kept
  in: `knowledge/energy-crystal.md`.
- On an ice field the common ice pays, not the rare one: 61% of the
  load was water ice, and water ice had the bids with depth; methane
  was 4%. Record: the Wolf 1061 run, guidebook section 6. Mining now
  costs an ice field by its water-ice share and the water-ice book. Kept
  in: unpromoted (`LEARNINGS.md`), one run only.
- A craft by hand is cheap and fast: 24 ticks, no credits, inputs from
  station storage. This confirms Trade's record.
- A once-only route put at the head of the plan before its owner opens
  it flies by itself once opened: 39 miners in under an hour.
- Repeated mistake: yes, the class of errors.log ENT-001. The fix this
  time is a check that prints the depth, not a rule to remember.
- Open: whether The Experiment's 1,466 cr bid refills, and how the
  water-ice bids move over a day.

## Cross-links

- `reports/2026-11-15_unity_divisions-handed-over-recurring-income-still-negative.md` -- the fleet report that set this turn's plan
- `reports/2026-11-15_zero_energy-crystal-the-one-mined-good-that-pays.md` -- my previous report, the chain this turn corrected
- `reports/2026-11-15_zero_mining-missions-unflown-by-91-pilots-honeyglobe-test.md` -- my previous report, the honeyglobe chain
- `game/routes/guidebook/mining.md` -- every call of the crystal test and the ice test
- `game/routes/plans/miner.json` -- the plan and `planned`
- `communications/orders.log` -- ENT-005 and ENT-006
- `communications/errors.log` -- ENT-015, ENT-021 and ENT-022
- `communications/queue.log` -- ENT-037 and ENT-043
- `communications/requests.log` -- ENT-039, ENT-040, ENT-051, ENT-052

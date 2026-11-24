---
name: faction-gathers-gated-silicon-waits-on-pirates
id: 20261124T122049Z
tier: report
trigger: session-end
author: Zero
tags: [mining, reserve, faction-storage, silicon, carbon]
links:
  - reports/2026-11-24_zero_floors-on-every-belt-sarin-carbon-test-three-t2-hulls.md
  - reports/2026-11-24_unity_posted-role-gates-five-answers-lift-commits-fixed.md
---

# Mining -- Faction Gathers Gated on the Outpost's Iron, Belts Under Their Floors Cut, Silicon Tests Wait on Pirates

## Situation

Period: since `reports/2026-11-24_zero_floors-on-every-belt-sarin-carbon-test-three-t2-hulls.md` (10:04 UTC); this scheduled turn ran 11:31 to about 12:25 UTC. Orders: `orders.log ENT-086` (block ZERO: gather what the reserve lacks; laser-only veterans on the far carbon and silicon wing, one ship first; 3 ships a belt).

Ships: 130 miners; 126 at work at 11:31 UTC (briefing), 129 at work and 1 docked at 12:21 UTC (`hive.py fleet`); none lost. Fill gate: HALT 4 waiting at 11:53 UTC, PASS at 12:08 and 12:12:38 UTC with 2 on park.

Credits: Mining wallets 4,123,924 (briefing 11:31 UTC) to 3,898,077 (12:21 UTC). The three Resonance Miner commissions (834,486 cr, paid 10:59 to 11:28 UTC, `data/fleet/upgrade_queue.json`) sit in the steady figures: the 11:00 hour of `stats_money_hour` reads Mining costs 889,340 and fuel 332,092 cr, against 64,662 and 63,003 the hour before. Without them the hour is about -54,900 cr, in line with the 10:00 hour (-50,552). Last 1h at 12:21 UTC: -339,217 cr, one 277,481 cr commission inside it, metered fuel and repairs 58,356 cr.

Output: 170.6 ore a ship-hour, 52,700 cr handed over in 24 h (scorecard, 12:21 UTC). Reserve shorts that miners can gather: silicon 44,481, carbon 18,590 (tool stock view=reserve, 11:34 UTC); nickel and gold now stand above their max.

## Activities

Order "gather what the reserve lacks" and the far wing:
- Silicon is the one short good worth far work: asks 362 to 452 cr (tool market, 10:46 to 11:36 UTC). The three silicon fields within reach of a station hold 2,155 to 5,110 units (table fields), and all three lie under pirates: GSC-0007 (sightings 10:52, 11:12, 11:46 UTC), Muphrid (four raider elites at the field, admirals ENT-125) and Hadar, whose road runs through Muphrid. The GSC-0007 test ship, empty, was stopped on its way in. The dispatcher's pirate stop keeps the route closed.
- Carbon asks 4 cr at Iron Reach (136,554 units) and The Anvil (357,932), books read 11:33 UTC. Home carbon fields hold about 3,150 units above their floors. Requests ENT-510 asks Logistics to buy the rest; the one-ship Sarin test (23 jumps out, 65 carbon aboard when read this turn) runs to its results.
- Need resonance-miner closed as done (commit 0e8e1b3b): the hull is commissioned with credits, so its materials (300 silicon, 150 nickel and others held for it) go back to the other needs.

Order "3 a belt" and the floors:
- The outpost's faction storage read iron 100,000, its limit (11:39 UTC), while six seated miners flew the two GSC-0044 faction gathers out of the list Then. Those two gathers and Acrux now carry `requires.reserve` (iron under 98,000) and `requires.role` (commits ff755da2, 2fa5711c); the six ships were stopped. fill.py reads them closed by the reserve.
- Belts under their floors: Sidelong (two ships stopped), 82 Eridani 3 to 1 and Guildless 3 to 1 (commits 2aec5a45, 8cd630d9); near-empty Bunda platinum 3 to 1 and Errai fragments 2 to 1 (dc27fd46, 738e6ba7); five more stopped.
- Node Gamma ice floor 30,000 to 7,500, 15% of its 50,000 (commit 620fc8df). It is the cheapest standing work Mining has: -171 cr a ship-hour over 49 runs in 12 h (route_earnings).

Scorecard (Mining): score 78.7 to 79.4, idle 4 to 1 (96.9% to 99.2% at work), belts spread 36 to 31 places (briefing 11:31 UTC, 12:21 UTC).

## Problems

- Six miners worked a store that could not take their iron (errors.log ENT-185). Cause: the 2026-11-23 lesson (`knowledge/iron-gathering.md`) asked a turn to remember to read the store; the routes stood in Then with no gate. Action: self-closing gates on all three faction gathers.
- The far wing reduces to one ship. Silicon fields lie under pirates; carbon is cheaper bought. The laser-only veterans keep the iron fallback the orders allow.
- Two veterans far out took park (fill.py check 12:12 UTC). Every gather in their reach is at its cap or under its floor, and the jump loop refuses Piloting 10. Park measured -1,702 cr a ship-hour over 12 h (route_earnings).
- The money figures carry hull purchases as running cost (errors.log ENT-186). Cause (from the code, not tested): `station/fleet.py` meter() prices a docked wallet drop as fuel or repair, and the commission is not booked as paid once (`bought` 0 in the 11:00 row).
- Module slots (328 empty) and tier-2 hulls (0 of 60 delivered) are not attacked this turn. Extra lasers raise the yield of iron and copper the reserve holds above max. The three hulls are measured first (Apophis, requests ENT-509).

## Plans

- Read the Sarin test's first results (carbon a run, minutes, fuel) against the 4 cr ask, with Apollo's answer to ENT-510. Then end the far carbon wing or keep it at one ship. Next turn.
- Read the Resonance Miners' delivery and switch (`upgrades.py queue show`). Measure their fuel per run against a Threshold on the same field before any further hull. That answers ENT-509 for Mining. Next turn.
- Silicon: each turn read the pirate watch at GSC-0007 and on the Muphrid road, and the census of the three fields. The GSC-0007 test reopens by itself six hours after the last sighting. A ship goes to Muphrid only when the raider elites are gone.
- Read the outpost's faction iron: the gathers open under 98,000 as the outpost's steel crafting draws it (P2). Also read the Node Gamma belt against its 7,500 floor.
- Autonomous choices made this turn: the gates, the caps and the Node Gamma floor (my routes). Fill's eight route-maker tests are not added: two fields are under their floors, the ice tests rest on 322 to 416 units of field, and one silicon field holds 647 units under a 3,000 floor.

## Suggestions

- To Unity (keep the money figures true): the collector books commission and buy_listed_ship payments (`data/fleet/upgrade_queue.json`, `door.jsonl`) as paid once, as capital. meter() skips a pass that holds one. Cost: one change in `station/fleet.py`. Without it P1 is read about 834,000 cr worse for a day from Mining's three hulls alone (errors.log ENT-186). Decision: Unity.
- To Unity and Trinity: `routes.py check` warns on a `deposit: faction` route with no `requires.reserve` on its main good. Decision: Unity.
- To Suggi through Unity: Mining's standing work gathers iron and copper above the reserve's max for Mining XP at about -200 to -600 cr a ship-hour (route_earnings 12 h). A rule exception that lets such miners dock (as F8 allows Intel's scouts) is Suggi's call. I hold the iron fallback until then.

## Feedback

- `requires.reserve` (reserves.py) reads faction storage of any item, not only bunker fuel. It closed the full-store gathers at once with a plain reason in `fill.py status` (`reserve: iron_ore 100,000 ... not under 98,000`). Good tool.
- `fill.py lift` commits again (Unity's 8a4bf667): four lowerings committed in one call each this turn. Last turn the index debounce refused every lift.
- `fill.py lift` refuses while any route file holds an uncommitted change. That is right, but a commit raced the hourly refresh once (index.lock) and needed a second try.
- The pirate stop closes a route to new ships but does not recall a ship already flying to it. I stopped the GSC-0007 ship by hand. A recall of ships in flight would make the stop complete.
- The 15% default floor (Trinity, f9e5d28e) closed my Node Gamma route less than my own 60% floor did; I moved it to the default.

## Learnings

- Faction gathers need a gate on the store's limit, not a reading. Record: table faction_storage 11:39 UTC; commits ff755da2, 2fa5711c. Change: every `deposit: faction` route carries `requires.reserve` and `requires.role`. Kept in `knowledge/iron-gathering.md`. Fleet takeaway: a check a turn must remember fails; a gate fires by itself.
- Read a good's asks before a far gather. Carbon at 4 cr in deep stocks does not pay a 23-jump run; silicon at 362 to 452 cr does where no pirates stand. Record: tool market 10:46 to 11:36 UTC. Change: carbon to home fields and a buy request (ENT-510). Kept unpromoted in LEARNINGS.md until the Sarin results.
- Skill: mining-chains changed -- faction gathers gated on the store's limit; asks read before a far gather; ships in flight to a pirate field are stopped.

## Cross-links

- `communications/orders.log` ENT-086 -- the orders in force.
- `communications/requests.log` ENT-510 -- carbon buy asked of Logistics; ENT-509 -- Apophis on tier-2 fuel.
- `communications/errors.log` ENT-185, ENT-186 -- the full outpost store; hull purchases in the steady money.
- `communications/admirals.log` ENT-125 -- Oracle's pirate reads at Muphrid.
- `game/routes/gather-gsc-0044-belt-faction.json`, `game/routes/gather-gsc-0044-forgotten-tailings-faction.json`, `game/routes/gather-acrux-belt-faction.json` -- the gated faction gathers.
- `game/routes/gather-node-gamma-nitrogen-ice.json` -- the cheapest standing work, floor 7,500.
- `game/routes/guidebook/mining/routes.md` -- Standing Plan of this turn.
- `game/needs.tsv` -- resonance-miner done.

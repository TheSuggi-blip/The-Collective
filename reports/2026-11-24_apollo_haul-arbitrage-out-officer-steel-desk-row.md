---
name: haul-arbitrage-out-officer-steel-desk-row
id: 20261124T101655Z
tier: report
trigger: session-end
author: Apollo
tags: [logistics, haul-engine, steel, recruitment]
links:
  - reports/2026-11-24_apollo_finish-routes-sol-loop-third-desk.md
  - reports/2026-11-24_unity_posted-role-gates-five-answers-lift-commits-fixed.md
---

# Logistics -- Haul Arbitrage Out, Officer Steel and Reserve Steel On, the Desk Row Under Way

## Situation

Scheduled turn of 2026-11-24 from 09:50 to about 10:25 UTC under orders.log ENT-086 (block APOLLO: no hauler waits, haul-network carries them, read its runs; the outpost steel route for officers, one ship first; reserve steel bought docked; the Lockbox, Hiring Board and Desk at Central Nexus with the fund; the kit as parts arrive). At preflight (hive.py briefing, 09:50 UTC) Logistics had 95 ships, 89 on a route and 6 waiting; its last hour stood at income 98,080 cr, costs 377,599 cr, net -279,519 cr; the fill gate read HALT (6 waiting). The faction held 250 of 250 seats and 9,685,239 cr in the treasury (table faction, 09:50 UTC); all eight faction facilities read ready (faction_owned, 09:58 UTC). The newest engine on the haulers, haul-network (queue.log ENT-297), held 60 ships; its 501 runs since 08:50 UTC summed to -239,167 cr (data/routes/runs.jsonl). At 10:14 UTC the fleet money view read Logistics' last hour at income 168,863 cr, costs 346,169 cr, net -177,306 cr, 93 of 95 ships at work.

## Activities

- haul-network read (order: read its runs). Grouped by note: 351 runs 'no eligible job' (+4,429 cr, wallet sweeps only), 18 'arb sold' (+18,714 cr), 40 'arb stored' (-76,167 cr: the bid gone on arrival), the rest bought and failed to sell before the sell tool group was fixed at 09:24 UTC. After the fix, 217 runs: arbitrage sold +16,551 cr, stored -26,123 cr. No run found a freight contract or an internal supply job. The lane is a buy that feeds a sale, Trade's class under P5 and Unity's answer requests.log ENT-504, so I took lane arbitrage out of game/haul-policy.json and gave haul-network `requires.skills_below` corporation_management 7 (commit c26763ce). Since 10:02 UTC its 255 runs read 'no eligible job' at no fuel; it stands as the haulers' freight and supply watch.
- The office row (P4, ENT-501): the Builder held the 200,000 cr fund but the engine had flown it 8 jumps out on an arbitrage buy. fly.py (scratch) caught it at the end of that run at 10:09:44 UTC and flies it home with a keeper loop on the hold; its catch row then builds the Lockbox (fee from the wallet, 225,970 cr read 10:15 UTC), waits active, the Hiring Board and the Desk upgrade. The member limit read before: 250 (table faction).
- Outpost faction iron (ENT-500): craft-steel-faction-gsc-0044 on with `requires.role` officer, max_ships 1 (commit 3b5da68c); one officer took it at 10:08 UTC and flies to the outpost.
- Reserve steel (ENT-504): buy-steel-reserve-central-nexus on, `open_to` hauler, max 20 cr, `held_below` steel 88,000 of Logistics, one ship (commits 3b5da68c, 49c09df1). Three runs stored 195 plate for 3,543 cr; the dispatcher then rests it 30 minutes after three short zero-credit runs, a throttle that keeps it lean.
- Plan: Then reordered to the officer route, the steel buy, the far joins, haul-network, park; the iron-buying steel route left out while iron stands over its max (P2). fill.py added the test mission-the-colonies-crimson; haul-network lifted to 66 (commit 766eae77). Fill gate HALT -> PASS (10:16 UTC).

## Problems

- The arbitrage lane cost 239,167 cr in an hour before this turn read it (errors.log ENT-181): an unproven spread scaled to 60 ships, books up to 180 minutes old, one claim per buy station so several haulers raced one thin bid. Fixed for haulers by the policy; the claim and depth changes are proposed to Trinity (queue.log ENT-302).
- The Builder was taken 8 jumps out with the Lockbox fund in its wallet, which the lane may spend above 6,000 cr: no route in the list Then fenced it. Fixed by the skills_below gate; the office waits on the flight home, not done this turn.
- My first fly.py refreshed the hold only between its own calls, and the gate's goal call returns only when the flight ends: a 20-minute leg would have let the hold go stale. A keeper loop now refreshes it every 30 seconds.
- Pushes were deferred from 09:17 UTC by an untracked empty file named '=' in the clone root, not mine (queue.log ENT-302 to Unity).
- KPI alarm hull upgrades (0 of 19 Piloting-10 haulers on a tier-2 hull) not closed: commission_quote at Node Beta answered achievement_required for the Workhorse and wrong_faction for the Prayer; the Apophenia stands at 433,072 cr (ships.md).

## Plans

- Read build4.log: the Lockbox RESULT line, the Hiring Board and the Desk; read the member limit after (expected above 250) and close the office in the guidebook's bases topic.
- Read the officer route's first RESULT line at the outpost (plate stored into the faction's storage, iron withdrawn); lift it toward the six officers if it holds (rule F37), since 100,000 faction iron lies there against an iron max of 80,000 (P2).
- Keep the steel buy at one ship under its rest throttle; lift the held_below level only on the craft routes' figures.
- Write a give route for the goods left in hauler holds once Mercury names a station (admirals.log ENT-122).
- Hulls: test the Prayer (7,613 cr at Frontier, Outer Rim yards) on the haulers born Outer Rim only where freight or a carry fills 540 units; no batch while the one Prayer flown earns nothing (-11,072 cr in 168 min, briefing 09:50 UTC).
- Assemble the Atria kit when foil scale, alloy scale, graphene thread and silica lens arrive (need atria-outpost-kit, 93%).

## Suggestions

- To Trinity (haul.py, queue.log ENT-302): claim an arbitrage job by its sell bid, ask a bid as deep as the buy and a book read within 30 minutes, and count goods bought and still held at cost in the run row. Owner Trinity with Unity; cost a few lines and a test.
- To Unity: a gate that keeps any new kind of route at one ship until three runs read positive (errors.log ENT-181), so an engine cannot take a division whole before its first figures exist. Owner Unity (dispatch.py or fill.py).
- To Unity: a warning in plan.py check for a route in a list Then without a fence for the faction's Builder.

## Feedback

- requires.role (Unity, 9d033c57) worked at once: craft-steel-faction-gsc-0044 went to an officer within a minute of the Then change, and why_closed.py names its reason. requires.posted is not used by Logistics yet.
- fill.py lift committed in one call (Unity's 8a4bf667); the earlier index debounce did not trouble it.
- The haul and bursar engines (Trinity, ENT-297) arrived wired into every hauler's fallback with a lane that buys to sell; the measured hour says such a lane needs the 1-ship test of rule F37 first. The engine's own design (claims, heartbeat, policy file) made the fix a one-line policy change, which helped.
- The dispatcher's rest after three short zero-credit runs throttles a docked reserve buy without a hand; useful, though not designed for it.
- The pull log line made the '=' file easy to see; a notice to its owner would save every member a push delay.

## Learnings

- A thin station bid read hours ago is no reason to fly, and at scale it costs: the arbitrage lane lost 239,167 cr in 501 runs, 40 of them storing goods where the bid had gone (runs.jsonl 08:50 to 09:55 UTC). Change: lane out of the haulers' policy; fleet takeaway: one claim per bid, not per buy. Kept in knowledge/station-bids-refill.md.
- A docked buy route runs every 30 seconds while held_below reads a 40-minute storage book (runs.jsonl 10:08 to 10:11 UTC). Change: one ship and a level below the need. Unpromoted in LEARNINGS.md; skill logistics-stock step 37.
- The gate's goal call returns only when the flight ends (desk logs, 06:38 caught, 06:44 goal line): a long leg needs a separate keeper loop on the hold.
- Skill: logistics-stock changed -- step 33 extended to engine routes in Then and the fly-home form with a keeper loop; step 37 added (held_below lag on fast buys).

## Cross-links

- communications/orders.log ENT-086; communications/requests.log ENT-500, ENT-501, ENT-504, ENT-505
- communications/queue.log ENT-297, ENT-302; communications/errors.log ENT-181; communications/admirals.log ENT-122
- game/haul-policy.json; game/routes/haul-network.json; game/fleet/haul.py
- game/routes/craft-steel-faction-gsc-0044.json; game/routes/buy-steel-reserve-central-nexus.json
- game/routes/guidebook/logistics/routes.md (Standing Plan); game/routes/guidebook/logistics/ships.md

---
name: scout-module-buys-stopped-born-elsewhere-work-home
id: 20261125T113943Z
tier: report
trigger: session-end
author: Oracle
tags: [intel, fuel, fits, census, regions]
links:
  - reports/2026-11-25_oracle_afterburners-off-scouts-census-refuels-on-the-way.md
  - reports/2026-11-25_unity_spend-by-kind-unarmed-hunts-closed-atria-stands.md
---

# Intel -- Scout Module Buys Stopped, Scouts Born Elsewhere Kept in Their Region, No Hunts Left

## Situation

Period: since `reports/2026-11-25_oracle_afterburners-off-scouts-census-refuels-on-the-way.md` (reports.log ENT-206, 05:50 UTC) to 11:40 UTC. Orders: `orders.log ENT-093` (08:47 UTC), block ORACLE: hunt rows out for unarmed ships, read REFUSED and STUCK after the refuel stops, bring the frontier under its target, keep Felis and the north road read, scouts born elsewhere work their own region.

Ships: 50 scouts, 0 lost in 24 h (table stats_pilot_hour, key ships_lost), 0 grounded; 46 working and 4 free at 11:03 UTC (turn check DIV). Credits: 623,468 cr in scout wallets at 11:03 UTC (fleet.json). Money: Intel's 24-hour purse -39,944 cr an hour, steady -25,696 (briefing 11:00 UTC); its last hour -24,670 cr, all fuel and repairs. Output: 1,593 of 2,325 places read within 3 hours (68.5%, scorecard 11:36 UTC); books under 6 h at 61 of 68 hubs. Division score 67.9 at turn start, 66.7 at 11:36 UTC (scorecard).

## Activities

1. Fuel, the refuel stops (block ORACLE). REFUSED read 16 legs in 2 h, all on one scout; every other scout 0 (turn check 11:04 UTC). That scout is docked at Synchrony with 2 of 130 fuel and 4 cr: its treasury top-up came 5.2 h before and wallet.py tops up a pilot from the treasury once in 6 h (TREASURY_EVERY; funds.json), so it gets one at about 11:55 UTC by itself. Docked, its refused legs burn nothing; no tow is needed.
2. Module spend (P1). Intel bought 131,690 cr of modules once in 6 h, the most of any division (`hive.py spend --hours 6`, 11:08 UTC). In the 7.8 h onetime.json holds, fit-network spent 195,278 cr on scouts: shield boosters III 74,863 (7) and II 37,231 (6), cloaks 34,115 (7), afterburners II 26,849 (10, before 45d42408), one ship scanner III 22,220. None has a measured gain. Commit 34ebb36e (fleet-build, 122 test files green) empties both Intel loadouts: fit-network now only strips off-role modules from scouts. Test red first: the old policy planned a booster III and a cloak, 14,000 cr, for a scout with a free slot. No afterburner stands on a scout (table ship_modules, 11:10 UTC). Need survey-scanner-i dropped (3f87bde6).
3. Hunts (requests ENT-541). Three hunt rows left the plan: Intercrus (-610 cr a ship-hour), Amberfall (-570) and the Titawin test on the one armed scout (2 runs, no kill, -2,795 cr). Seven voidborn-first-hunt circuits left the list First: unarmed scouts flew them 33 times in 24 h and booked none. The Objection left First too (5 runs in 24 h, never offered; it stays on one Outer Rim row, where Deep Range is home).
4. Regions (F35). The 12 systems at the far end of the north road that lie nearer Frontier than Nexus Prime by lanes moved from census-north to census-region-altais, max 6 to 8 (4d5c34dc). Outer Rim rows end @outerrim, census-far-1, home-frontier-station; Nebula rows @nebula, census-far-2 to -4, home-grand-exchange (census-far-2 to -4 lie 17, 8 and 38 of their systems nearest Haven). New watch-book-frontier-station (3fd1d978, zero fuel).
5. Frontier. The turn check judged the frontier against census-frontier's cadence, which sits a trip under the target by design; it now judges the 3-hour target. Oldest frontier read 183 min (Schedar) at 11:27 UTC, 5 of 26 systems past the 155-minute cadence; census-frontier 155 to 145 minutes.
6. Military and Logistics (admirals ENT-142): Felis read a pirate at 09:41:59 UTC (pirate_korr raider elite), so P3's 24 hours without a pirate there end no sooner than 2026-11-26 09:42 UTC. Five places hold 3 or more kit animals. Filed: 24 pirate lines (Ironveil 14, Sheliak 3, GSC-0007 3, Enif 2, Redmarsh 1, Felis 1), 6 ranches, 0 raids, no battle at a base of ours.
7. Checks: game version 0.734.5 (api/stats), no new release; validate-intel Errors 0; envoy: no reply since 2026-11-24 17:39 UTC, the beacon round of 09:26 UTC went out by itself, NOIR rests.

## Problems

- Frontier: 183 min against 180 at 11:27 UTC. Cause: reads come a trip after a system falls due at 155. Action: cadence 145. The old line compared 164 min with the 155-minute cadence at 11:04 UTC; judged against the target, the margin at 11:27 UTC was 183 against 180.
- SITES census-north: Sadalsuud 191 min at 11:27 UTC, a scout was flying to it. The move leaves census-north with 19 systems for the Voidborn readers; its next reads are judged next turn.
- Score fell 67.9 to 66.7 in the turn, idle 3 to 5 while the Outer Rim rows changed and their scouts head home (scorecard 11:36 UTC).
- A scout ran dry of credits (4 cr). Cause: its fit-network runs cost 11,406 cr (6 runs since 2026-11-24 20:30 UTC, table runs) and its hunt test 1,612 cr; the 6-hour treasury top-up window kept it docked. The module cause is closed by 34ebb36e.
- Module slots read 41.5% fit and 0 of 30 eligible scouts on a tier-2 hull. Both alarms are held by P1: no scout module or hull has a measured payback within a week.

## Plans

- Read four hours of census-frontier at 145 min and of census-north and census-region-altais after the move; a list still over the 3-hour target gets 10 min lower, never more ships (plan file Planned).
- Read `hive.py spend` for Intel next turn: modules bought once should read 0; fit-network on scouts should only strip.
- Measure fuel a jump of the four scouts that carry a fuel optimizer against the rest before any module returns to an Intel loadout (P1); the measure decides, not the catalog.
- Envoy: read threads twice a turn; next beacon round 2026-11-26 09:26 UTC by itself; replies go to Unity quoted as data.
- Crystal melt: Intel stores 15 (Sirius 3, The Crucible 12; stock 11:26 UTC). Hex Star's bid stood at 54 cr at 08:57 UTC (it was 3,158); Mercury offers a give stop when it refills (block MERCURY), so no request now.
- Choices made alone: the region split of the north road by nearest capital, the empty loadouts, the dropped need, the First list cuts.

## Suggestions

- To Unity and Trinity: fit-network judges a loadout only by price and free slots. A per-division `payback` field (the measured gain per hour a module must show, read from runs) would make P1 a gate instead of a turn's reading; until then an Admiral keeps a loadout empty. Owner: Unity (fit_net.py is shared). Cost: one field and a test.
- To Unity: wallet.py's six-hour treasury window leaves a pilot docked at 4 cr for up to six hours; a pilot under 1,000 cr could bypass it. Owner: Unity. Cost: one condition; risk: a loop that spends every top-up, which the window guards against.

## Feedback

- `hive.py spend` (b28f7b0d) answered in one call what took a parse of onetime.json last turn: Intel's 131,690 cr of modules in 6 h, beside every division. It made the P1 breach visible at the start of the turn.
- The unarmed-hunt rule (850aee18, ENT-541) closed the hunt routes as answered; the voidborn-first-hunt circuits, kind circuit, stayed open to unarmed scouts as Unity foresaw (33 runs, 0 booked). Taken out of my First list instead of a new request.
- fill.py check passed at 11:04, 11:27, 11:36:30 and 11:40:05 UTC with the docked-watch exception; fill.py status named every closed route with its reason (newborn guard, class, claims), which made the region change checkable.
- fleet-build install ran all gates in about a minute and committed 34ebb36e.

## Learnings

- A fit-policy loadout is a standing buy order: fit-network buys each listed module for every scout with a free slot and the wallet for it. Record: onetime.json (195,278 cr on scouts in 7.8 h), hive.py spend. Change: Intel loadouts empty until a module's gain is measured. Fleet takeaway: every division's loadout list spends without a turn deciding it. Kept in: guidebook `game/routes/guidebook/intel/ships.md`.
- A check judged against a list's cadence HALTs by design, since the cadence sits a trip under the target. Record: turn check 11:04 and 11:27 UTC. Change: FRESH frontier judges 180 min with the cadence printed. Kept in: `knowledge/census-freshness.md` (source 42).
- Skill: intel-turn changed -- FRESH judges the 3-hour target; a SPEND line reads Intel's module buys each turn.

## Cross-links

- `communications/orders.log` ENT-093 -- the orders in force, block ORACLE.
- `communications/requests.log` ENT-541 -- Unity's answer: no hunt for an unarmed ship.
- `communications/admirals.log` ENT-142 -- releases, Felis pirate, kit herds, filings.
- `communications/queue.log` ENT-334 -- this turn's changes and their undo.
- `game/fit-policy.json` -- Intel loadouts emptied (34ebb36e).
- `game/routes/census-region-altais.json`, `game/routes/census-north.json`, `game/routes/census-frontier.json` -- the list changes (4d5c34dc).
- `game/routes/watch-book-frontier-station.json` -- the new docked watch (3fd1d978).
- `game/routes/guidebook/intel/routes.md` -- the Standing Plan (0259f26c).

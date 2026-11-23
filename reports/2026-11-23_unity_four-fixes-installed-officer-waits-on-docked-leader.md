---
name: four-fixes-installed-officer-waits-on-docked-leader
id: 20261123T205640Z
tier: report
trigger: session-end
author: Unity
tags: [fleet, plumbing, empire]
links:
  - reports/2026-11-23_unity_kit-parts-are-creature-parts-docked-gate-fixed.md
  - reports/2026-11-23_oracle_kit-herds-read-ranch-loss-found-hunt-guard.md
  - reports/2026-11-23_zero_iron-handed-at-four-stations-third-laser-yildun-cut.md
  - reports/2026-11-23_apollo_capital-corridors-by-birth-waiting-haulers-84-to-4.md
  - reports/2026-11-23_apophis_recursion-flies-kit-hunts-ranch-loss-rearmed.md
  - reports/2026-11-23_mercury_capital-traders-docked-crafts-blood-forge-station-needs.md
---

# The Collective -- Four Fixes Installed for the Admirals; the Officer and the First Notice Board Post Wait on a Docked Leader

## Situation

Period: from my report of 16:00 CET (`reports/2026-11-23_unity_kit-parts-are-creature-parts-docked-gate-fixed.md`, reports.log ENT-158) to this turn, 20:30 to about 22:00 CET on 2026-11-23. Orders at the start: orders.log ENT-083; new orders ENT-084 (22:00 CET).

The fleet as one purse (tool fleet, view=kpi, 21:53 CET): wallets 19,830,605 cr plus treasury 2,239,907 cr, together 22,070,512 cr; at 15:49 CET it read 17,815,038 cr. In plain words: the purse grew by about 4.3 million cr in six hours, and again almost all of it is one-time money: mission rewards for newly joined pilots, 586,270 cr an hour over 24 hours (same read).

The money that repeats is still below zero and worse than this afternoon. Steady net (what we earn minus fuel and repairs) read -89,200 cr an hour over 24 hours, -140,331 over 6 hours and -144,252 in the last hour; fuel alone was 167,273 cr of the last hour's 196,112 cr of costs. Ships at 21:52 CET: 373 of 500 at work, 72 waiting, 54 held by hand, 1 starting (fill.py check all). The repository's search index stood stale for my whole turn (no `ok` line since 18:35 CET), so I searched by keyword.

One line per division, from each Admiral's report of this evening:
- Mining (Zero, 19:45 CET): 128 of 130 at work; gifts moved 52,163 iron ore and 43,435 copper ore to the haulers who smelt steel; steady net -43,018 cr in its last hour.
- Logistics (Apollo, 20:13 CET): waiting haulers 84 down to 4 by sending newborns to the capitals that pay their birth; at 21:52 CET 61 waited again.
- Military (Apophis, 20:31 CET): its first tier-two hull (a Recursion) flew five kills in 33 minutes; one drone was lost at 17:51 CET to a partner faction's pilot defending its tame herd.
- Trade (Mercury, 20:40 CET): waiting traders 64 down to 0 with crafts at the capitals; a station-need mission paid 32,413 cr for goods the market bid 7,054 cr for.
- Intel (Oracle, 19:51 CET): read the herds of the outpost kit's five species: two of them have only 2 animals in any place we know, too few to hunt.

## Strategy

Suggi's standing goals G1 to G5 and the subgoals O1 to O10 stand unchanged in ENT-084: be the strongest faction in the game, a fleet of up to 1,000 ships, up to 5 stations and 8 outposts, the best income as one enterprise, and the whole galaxy explored.

Decided this turn (my calls as the players' captain):
- The 400-seat building (Guild Hall, 8,000,000 cr) waits. Plain words: it costs more than three times what the treasury holds while the repeating money is negative, and the faction still has 15 free seats of 200 (empire.md 20:51 CET). The game's rules say offices at several stations stack, each extra one counting a quarter; a 300,000 cr Recruitment Desk at a second station should add 25 seats, at 12,000 cr a seat instead of 40,000. Apollo builds one and reads the member limit before and after, which proves or disproves the stacking (requests ENT-480).
- The iron reserve's maximum stays at 80,000. Zero asked whether to raise it; we hold 183,655 iron, so iron is not what steel is short of. Steel is short of smelting where the iron lies; the miners' gifts to the haulers there are the answer.
- Crafts at the capitals may cost up to 500 cr a ship-hour for the crafting experience they buy; dearer ones are cut (Mercury's own line, now in his orders).
- Orders ENT-084 replace ENT-083: the plan lines were shortened to their current state, and each block names its next step.

Proposed and not decided: a Wildlife Corral (750,000 cr, game/catalog/facilities.md) to breed the kit's rare animals, which Apophis suggests. It needs a live wild herd of the species at the place where it is built. I decide it after the first Notice Board job is answered and Oracle's herd census has read the five species a few times.

## Divisions

Mining (Zero). Planned work landed: the iron gifts to the haulers moved 52,163 iron ore by 19:38 CET, matching the plan of the turn before. Suggestions: ENT-465 (a spent far field stays closed) accepted and built, ENT-466 (the filler never adds a route that takes a miner's tools) accepted and built; raising the iron maximum declined (reason above); a receiver hauler at Alpha Centauri is Apollo's call, open. Ten miners had flown 11 jumps to a spent field; the new rule closes such a field until a newer census reads it back.

Logistics (Apollo). The idea of the turn was sound: one database query showed which capital pays which birth, and the waiting haulers fell from 84 to 4. But by 21:52 CET 61 waited again: most routes still open to them want 100 stored iron at their station, and the paid trips are booked (fill.py status hauler). This is the Admiral's plan, and orders ENT-084 name it. Suggestions: the hourly route pass commits only its own files, accepted and done (my scheduled script, tested on a copy); needs.py add refusing his row, not reproduced (the same add passes on a copy of today's register), so I asked for the exact command; lifting caps of once routes at Frontier and Krynn, open: I did not read their owners this turn. His Guild Hall request: declined for now, with the desk path instead.

Military (Apophis). The first Recursion hull flies, and its measured runs now decide a batch. The drone loss came from hunting animals that carried another faction's tag; Oracle's fix refuses such animals for every division, and Apophis's own fix (a ship that joins our fight ends the hunt at that place) is installed. Suggestions: a class guard so strip routes never reach his ships, accepted and built; the dirty clone that blocked his installs, found and fixed; the Corral ranch, open (above).

Trade (Mercury). Waiting traders went from 64 to 0, and the station-need missions are a real find: they pay several times the bid. Suggestions: the sedcards refresh, fixed; a cost line for crafts, decided at his own 500 cr a ship-hour; read station needs before selling, accepted into his orders.

Intel (Oracle). The herd census for the kit's species now runs every six hours. Suggestions: name foil scale and graphene thread first on the Notice Board, accepted into P3; the timing test that failed installs under load, accepted and fixed; the drop per kill, accepted into Military's orders.

Consistency: no division's numbers contradicted another's this evening; the three that crossed (iron handed, hauler waits, kit herds) agree with the store's tables the Admirals cited.

## Plans

- The Admirals' turns start at 00:00 CET; mine at 02:30 CET.
- The officer and the first Notice Board job: both need the leader's flagship docked, and it flew hunts back to back all turn; my attempts to hold it between runs were refused because each new run started within a minute. Next: a queue of leader errands served at its next dock (DECISIONS Q75 (12)), then the officer role (create_role), the promotion, and one small open-to-all posting for the kit's foil scale.
- The new withdraw step (a ship takes goods from the faction's storage, not only its own) is installed but has not flown; it flies first with the officer, on the outpost's 100,000 iron for Logistics' steel.
- The courtesy note to [HEXC] about the drone that hunted their herd is written and passed the airlock's text check, but the airlock's one-message-a-day limit holds it until about 06:00 CET; it goes in my turn of 08:30 CET.
- Still unbuilt from Q75: (1) a lean pass of the rulebook, (3), (5) to (10) the store figures and runner steps listed there, (12) the leader errand queue. Closed this turn: Q56, Q66, Q72 (built or merged).
- Read the hunts' drop per kill as Military reports it, then decide the Corral.

## Advice and Suggestions

For Suggi, in plain words: the fleet earns most of its money right now from one-time rewards, while the repeating money loses about 89,000 cr an hour, almost all of it fuel. That is the cost of moving several hundred new pilots to where their missions pay; it can only last while those missions last. My focus for the next turns is the repeating side: steel made where the iron already lies, crafts that cost less than the experience they give, and ships that wait docked rather than fly empty.

Nothing here needs your decision. Two notes for you or Morpheus: the repository's search index is slow because its embedding helper is unavailable and every update runs the slow way (queue.log ENT-278); and in the evening the box ran heavily loaded, so tests took far longer than usual. No new pilot, no new Admiral, no war and no alliance is proposed. The one message to another faction this turn went to the Ironlight Combine's officer, a polite reply that we will trade with them through the open market as they suggested; no goods and no information were promised.

## Learnings

- A script that writes into the shared repository on a schedule is a writer every member waits on. The hourly sedcards refresh left a file uncommitted when another program held git's lock, and three Admirals' installs failed on it for three hours. Record: requests.log ENT-472 and ENT-473, commit b2b8b16b. Change: every scheduled writer commits through one helper that retries and takes its file back on failure. Kept in knowledge/faults-that-leave-no-record.md. Fleet takeaway: a refused install names a dirty file; the file's writer is fixed, not the install.
- Something read in a help text, a field's name or a test in another process is a guess until it ran once where it acts. Record: errors.log ENT-037 and ENT-081, queue.log ENT-060 and ENT-071. Change: new steps are reported "built, not flown" until one result. New file knowledge/proven-where-it-runs.md, three older inbox entries promoted into it.
- The leader cannot do the faction's paperwork while it hunts. Record: its order file and route log, 21:11 to 21:45 CET. Change: the errand queue (Q75 (12)). Kept unpromoted in LEARNINGS.md.
- Skill: fleet-ops changed -- pitfall: the leader cannot be caught between runs by hand.

## Cross-links

- reports/2026-11-23_zero_iron-handed-at-four-stations-third-laser-yildun-cut.md -- Mining
- reports/2026-11-23_apollo_capital-corridors-by-birth-waiting-haulers-84-to-4.md -- Logistics
- reports/2026-11-23_apophis_recursion-flies-kit-hunts-ranch-loss-rearmed.md -- Military
- reports/2026-11-23_mercury_capital-traders-docked-crafts-blood-forge-station-needs.md -- Trade
- reports/2026-11-23_oracle_kit-herds-read-ranch-loss-found-hunt-guard.md -- Intel
- communications/orders.log ENT-084 -- the new orders
- communications/requests.log ENT-475 to ENT-480 -- my answers
- communications/queue.log ENT-277, ENT-278 -- the installs and the index note
- governance/strategy.md, governance/empire.md -- strategy and the faction's seats

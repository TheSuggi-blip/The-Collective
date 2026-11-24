---
name: officer-seated-sweep-and-host-faults-fixed
id: 20261124T031659Z
tier: report
trigger: session-end
author: Unity
tags: [fleet, plumbing, empire]
links:
  - reports/2026-11-23_unity_four-fixes-installed-officer-waits-on-docked-leader.md
  - reports/2026-11-23_oracle_herds-verb-installed-six-ranches-filed-newborn-book-watch.md
  - reports/2026-11-24_zero_six-silicon-carbon-tests-full-outpost-rows-cut-seep-spill.md
  - reports/2026-11-24_apollo_krynn-blood-forge-corridor-hiring-board-at-experiment.md
  - reports/2026-11-24_apollo_records-corridor-second-desk-at-gsc-0044.md
  - reports/2026-11-24_apophis_far-herds-generator-scar-pirate-formation-flies.md
  - reports/2026-11-24_mercury_bursar-desks-replace-capital-crafts-waiting-48-to-0.md
---

# The Collective -- The Faction Has Its First Officer; Four Faults in the Fleet's Plumbing Fixed, One Stall of the Run Host Rescued

## Situation

Period: from my report of 2026-11-23 21:59 CET (reports.log ENT-164) to this turn, 03:00 to about 04:30 CET. Orders in force: ENT-085, written this turn.

The fleet as one purse (hive.py fleet, 04:12 CET): 25,402,931 cr, made of 22,161,212 cr in the ships' wallets and 3,241,719 cr in the faction's treasury. At 21:53 CET it was 22,070,512 cr, so about 3.33 million more in six hours.

In plain words: almost all of that growth is one-time mission rewards, 627,325 cr an hour over 24 hours and 1,858,500 cr in the last hour alone. The steady side, money that comes in every hour minus fuel and repairs, is still below zero: -93,391 cr an hour over 24 hours, -116,872 over 6 hours and -211,572 in the last hour, when fuel alone cost 285,026 cr. Part of that fuel is the price of the one-time rewards (ships flying to far mission boards), so the steady figure reads worse than the truth; the matched figure that pairs costs with their income reads -63,781 an hour over 24 hours (hive.py stats kpi, 03:08 CET). Ships: 457 of 500 at work, 42 docked without work (27 of them haulers), 1 adrift.

- Command (10 ships, 9 at work): purse +11,331 cr an hour over 24 hours (stats contribution); the faction's first officer seated and its first Notice Board job posted.
- Intel (50, 46 at work): purse +40,960; 92% of the places our routes use read within three hours.
- Logistics (95, 68 at work, 27 docked): purse +145,071; the costliest fuel of the last hour, 88,656 cr.
- Military (130, 124 at work): 9,000 kills and 4 ships lost in 24 hours.
- Mining (130, 127 at work): 122 units of ore a ship-hour; iron 179,545 held against a max of 80,000.
- Trade (85, 83 at work): the only division above zero on the steady side in the last hour, +28,117 cr.

## Strategy

Suggi's standing goals G1 to G5 and his subgoals O1 to O10 stand unchanged at the head of the orders; only he changes them.

Decided this turn (orders ENT-085, which replaces ENT-084):
- The plan's first line now names the steady loss in numbers and adds one rule for every Admiral: at most one install a turn of the scripts the run host runs. Each such change makes the run host hand its work to a fresh copy of itself, and too many at once stopped it this turn (see Divisions and errors.log ENT-174).
- Iron: the reserve's max stays at 80,000 while 179,545 are held and the stock still rose 1,607 an hour over 24 hours (hive.py stats supply). Mining gathers iron only where a ship's training needs it; the stored iron goes to steel where it lies.
- The faction's first officer is one of my flagships. In plain words: until now only the leader's ship could take money out of the treasury, and the leader flies hunts most of the time, so payments waited for hours. An officer has the same right, so either ship can pay. Which ship is chosen does not matter much yet, because the game pays out only to a ship docked at one of our Lockboxes; I read its first payment next turn.
- The first open-to-all Notice Board job went live at 04:32 CET (the game answered `posted`): 50 Foil Scale delivered to Node Beta for 2,500 cr, held in the faction's escrow and paid to the first pilot who completes it, ours or anyone's. Foil scale is a kit part that no market sells and no wild herd we found yields in numbers (Military's herd count), so other players' hunters are the way.

Proposed, not decided: none new. The Guild Hall still waits for a treasury of 8.5 million and a steady net at zero (P4).

## Divisions

Every Admiral reported since my last turn; Apollo twice.

Intel (Oracle, reports.log ENT-165). The herds tool works and Military used it the same night. Suggestion 1, a column in the store's herds table for animals that carry another faction's tag: accepted, my next build of store.py. Suggestion 2, one definition of "working" shared by the scorecard and the fill gate: accepted, open, put to Trinity, who owns the scorecard. The [IRLC] closing line needs no answer; the thread is closed.

Mining (Zero, ENT-166). Suggestion 1, a `jettison_gangue` key: done by Trinity before my turn (8a4efabf, with its test), answered ENT-487. Suggestion 2, the five-minute pass lowers a shared fallback's ship cap to what its field carries: accepted, open; the seep spill it would have stopped cost about 50 ship-runs (errors.log ENT-168). Thread check: Zero cut the outpost's iron rows, yet the iron stock still rose over 24 hours; the new orders say so plainly.

Logistics (Apollo, ENT-167 and ENT-170). A Hiring Board went up at The Experiment and a second Desk is staged at our outpost; the member limit read 225 after the first. Suggestions: a keep flag for standing keep-stock needs, accepted, open (needs.py, mine); a notice before a planned engine restart, passed to the box's owner; a few haulers with a role that may take goods from the faction's storage, accepted in principle: Apollo names up to three in requests.log, and the role and promotions go through my errand queue. Thread check: waiting haulers went 61 (21:52 CET) to 16 (01:34 CET) and back to 24 (04:06 CET), 13 of them Outer Rim-born far from home; not closed, named in his orders block.

Military (Apophis, ENT-168). The generator fault that wrote one place into 36 hunt files was found and fenced in code by Apophis himself (errors.log ENT-170). His request for a way to take a ship by hand at the end of its run is built (`gate.py want`, ENT-488). Suggestions: keep another class's far corridor trips out of combat plans, accepted, open (fill.py); count parked ships in the gate line, accepted, open; the kit's scales from the Notice Board rather than wild herds, agreed and acted on this turn.

Trade (Mercury, ENT-169). Docked Bursar desks replaced the dear capital crafts; waiting traders fell from 48 to 0 and stayed at 0 at 04:05 CET (fill.py check). Both requests done (ENT-489): his fix of the upgrade queue's funding, and the run host's test, which failed in every member's shell and so blocked every Admiral's installs. His suggestion that the sweep prints each failing step: done, in two steps this turn.

## Plans

Next turn 09:00 CET; the Admirals' round starts at 06:00 CET.

- Read the Notice Board job's answer: accepted, delivered, or untouched after 72 hours. If it is answered, the next post is graphene thread; if it sits untouched, the reward is raised once.
- Read the officer's first treasury payment and the first flight of the faction-storage withdraw step (Apollo's steel route on the outpost's 100,000 iron).
- My next dispatch batch, one install: the leader's hold at a station must outlast the sweep's real spacing (passes stood 10 to 17 minutes apart against a hold of 12); the fill pass lowers shared fallback caps to what a field carries; combat plans refuse other classes' far corridor trips; the gate line counts parked ships.
- Store: the tagged-animals column in the herds table. Needs: the keep flag.
- The run host's stall (errors.log ENT-174): proposed to Trinity, who built the handover; he answers in queue.log whether he takes it.
- Still unbuilt from DECISIONS Q75: (1) the rulebook's lean pass, (3) the check for members' files left uncommitted, (5) the hour and pilot of each loss in the briefing, (6) a once route's first cap sized to its board, (7) the scorecard counting off-role modules as unfilled, (8) routes committed since a request in its answer, (9) a circuit stop that visits without docking, (10) a total-credits column per route.
- The courtesy note to the faction whose tame herd we hunted waits for its daily message limit (after 06:00 CET).

## Advice and Suggestions

Nothing here needs your decision, Suggi. Three things worth knowing:

- The money. The purse grows fast, but on one-time rewards: each pilot earns them once per mission, and they will thin out. The steady side, what the fleet earns hour after hour, loses about 64,000 to 93,000 cr an hour depending on how fuel is matched to income. The players' focus stays on the first plan line: cheaper work for the ships that burn fuel without bringing anything home.
- The plumbing. Four faults sat in the fleet's plumbing; three of them in code whose tests were green because each test checked a stand-in rather than the real call. Two of the four ended the treasury's five-minute pass tonight; another blocked every Admiral's installs for hours. All four are fixed, and the lesson went into the fleet's knowledge.
- The run host stopped starting new runs for about eight minutes (03:54 to 04:02 CET) after several code changes landed at once; I freed it by hand, and the rule is now one install a turn. No ship was lost.

Reserved to you and not proposed: no new pilot, no new Admiral, no war, no alliance. One stranger offered our ships chart trades in local chat; nobody answered, because what we know of the map stays ours.

## Learnings

- Lesson: a test is only as true as the call it runs. The errand queue's tests replaced the errand call itself, so the first live errand crashed the sweep; the upgrade queue's stand-in took a call the real function refuses; the run host's test passed only in a shell that names no member. Record: errors.log ENT-171, ENT-173; requests.log ENT-485. Change: a test fakes only the gate, never the step it guards, and a stand-in takes the real function's signature. Kept in: knowledge/proven-where-it-runs.md (the faked-step case). Takeaway for every Admiral: read your test and ask which line of it the live game would answer.
- Lesson: one install of many files is many restarts. Record: errors.log ENT-174, the run host log of 03:54 to 04:02 CET. Change: one install a turn (orders P1). Kept in: my skill's run-host reference.
- Skill: fleet-ops changed -- the errand queue, promote by name and the dispatcher's restart (faction reference); the handover stall and its rescue (run-host reference).

## Cross-links

- `reports/2026-11-23_unity_four-fixes-installed-officer-waits-on-docked-leader.md` -- my previous report.
- `reports/2026-11-23_oracle_herds-verb-installed-six-ranches-filed-newborn-book-watch.md` -- Intel.
- `reports/2026-11-24_zero_six-silicon-carbon-tests-full-outpost-rows-cut-seep-spill.md` -- Mining.
- `reports/2026-11-24_apollo_krynn-blood-forge-corridor-hiring-board-at-experiment.md` and `reports/2026-11-24_apollo_records-corridor-second-desk-at-gsc-0044.md` -- Logistics.
- `reports/2026-11-24_apophis_far-herds-generator-scar-pirate-formation-flies.md` -- Military.
- `reports/2026-11-24_mercury_bursar-desks-replace-capital-crafts-waiting-48-to-0.md` -- Trade.
- `communications/orders.log` ENT-085; `communications/requests.log` ENT-487 to ENT-489; `communications/errors.log` ENT-173, ENT-174; `communications/queue.log` ENT-290.
- `governance/strategy.md`, `governance/rulebook.md` (F8, F11, F12, F15).

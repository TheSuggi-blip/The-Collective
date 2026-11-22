---
name: requests-built-deposit-unblocked-strict-classes-wait
id: 20261122T061715Z
tier: report
trigger: session-end
author: Unity
tags: [fleet, plumbing, purse, strict-classes]
links:
  - reports/2026-11-22_unity_atria-funded-requests-answered-trinity-build-checked.md
  - reports/2026-11-22_zero_laser-iii-proven-sales-become-gifts-iron-at-max.md
  - reports/2026-11-22_oracle_stranded-scout-rescued-fuel-check-built-p5-gifts.md
  - reports/2026-11-22_apollo_atria-kit-behind-its-ask-sales-out-bunker-from-own-cells.md
  - reports/2026-11-22_mercury_every-trader-operating-network-commerce-paid.md
  - reports/2026-11-22_apophis_sales-become-gifts-pulse-laser-iii-proven-caustic-sac.md
---

# The Collective -- Every Request Built, 1.19 Million Freed for the Treasury, Strict Classes Wait One Turn

## Situation

Period: from my report of 03:47 CET to 07:17 CET on 2026-11-22 (all clock times here are CET; the logs keep UTC). Orders in force: `orders.log` ENT-062 (new this turn). "cr" means credits, the game's money.

- **The fleet as one purse** (`hive.py fleet`, 07:17 CET): steady earnings, meaning repeating work after fuel and repairs, were +1,553 cr an hour over the last hour, +9,229 over six hours and +13,174 over 24 hours. Fuel now costs about as much as we earn: 136,045 cr of fuel against 119,814 cr of income in the last hour. The 24-hour figure still holds paused hours and becomes a fair test about 21:30 CET tonight.
- **Paid-once money** (missions a pilot can do only once, and one-off buys such as lasers): -29,636 cr in the last hour, counted apart from the steady figure.
- **Money held:** 8,591,220 cr in the ships and 1,664,273 cr in the faction's shared savings (the treasury) at its last reading, which was taken before this turn's deposit of 1,190,781 cr landed at 07:11 CET (`data/fleet/sweep.jsonl`, state booked). Added up, about 11.45 million cr.
- **Ships:** 246, none lost; 239 at work and none waiting at 07:13 CET (`fill.py check all`: PASS). Six were driven by hand or by an engine goal.
- **Per division** (`hive.py stats contribution`, own net over six hours): Military +33,963 cr an hour, Command +17,007, Mining -936, Trade -6,204, Logistics -18,645, Intel -21,723. Hunting pays for the fleet; scouting and hauling spend fuel, which is their job (reading and carrying), but training loops also burn it.

## Strategy

Suggi's standing orders S1 to S5 and goals G1 to G5 are unchanged; only he changes them. What they ask of this turn, and where we stand:

- **S5, never idle:** met. Every ship had work at 07:13 CET; my two waiting flagships got hunts.
- **P1, an economy that pays for itself:** only just. Six-hour net +9,229 cr an hour. The cause is fuel: since the game resumed the fleet flies far work and training loops, and fuel climbed to about 100,000 cr an hour. Decided this turn: the new orders ask every Admiral to train at the least fuel per experience point, and Trade to put its traders on trade runs and missions that pay their skills before plain jump loops.
- **G2 and P4, the faction's seats:** 99 of 100 seats are filled. The next step is the Recruitment Center (room for 200), whose fee is 2,000,000 cr. With this turn's deposit the treasury holds enough; the fee is paid when Logistics has the parts ready (the needs list still lacks one caustic sac and a batch of flex polymer).
- **G3 and P3, bases north:** Atria (our next small base) waits for an outpost kit at Ironlight Crossroads at its planned price. Decided this turn: the treasury does not pay 999,999 cr for the one kit on sale elsewhere, at Arneb.
- **P5, each class does its own work:** "strict classes" is a switch that makes selling Trade's job alone; the other divisions then hand their goods to named traders and haulers. Decided this turn: it waits one more turn. A dry run showed no ship would stand idle, but Trade has no sell routes yet for the hunting loot at the stations where the hunts would hand it over, and hunting earns most of our money. Switching now would stop that income for hours.
- **Proposed, not decided:** that every member names in the queue log the shared gate files it will change before it changes them (see Advice).

## Divisions

- **Mining (Zero):** proved a stronger mining laser on three runs (about twice the ore per run) and fitted it on seven miners; turned his sales into hand-overs. His fault: the five-minute pass lifted a silicon route to nine ships on a field with no silicon left. Built: a mining route is now sized only by its own ore. Suggestions: the two iron figures (keep 166,923 against the reserve's 108,730) -- open, for a review with Apollo; a cheaper laser test on one ship first -- his to decide, accepted; the board's hourly line shows a sweep inside a run as a loss -- open, not built.
- **Intel (Oracle):** rescued a scout stranded far out with too little fuel after 63 refused runs over two hours. Built for him: a route now rests after three runs that read or reached nothing, however long each took. His own fuel check waits for his turn; the test suite passes again. Suggestions: handbook tests before a new tool lands -- accepted, for Trinity; hand-over routes on with the switch -- done.
- **Logistics (Apollo):** all five faction buildings ready; the outpost's fuel bunker now takes our own fuel cells; his sales left the plan. Suggestions: several hauler receivers per station -- accepted in principle, his to set; the filler should not add sales to other classes -- done; the filler printing why ships at work stand where they are -- open.
- **Trade (Mercury):** all 40 traders at work since 04:51 CET, against 32 waiting yesterday; a new mission paid on its first run. Suggestions: one shared commit wrapper for the guidebook gate -- accepted, open; two survey missions for Intel -- passed to Oracle (rule F34). His request for trade-run missions in the runner was built by Trinity; I closed it.
- **Military (Apophis):** the Pulse Laser III is now the division's weapon after 28 kills at full hull; caustic sac is hunted for the Recruitment Center. His plasma cannon test fired no shot for want of ammunition; he fixed the fit. Suggestions: an ammunition buy counts as fitting, and hunts note an empty magazine -- both accepted, open.
- **Thread check:** my last report promised Apollo founds Atria at his 04:45 CET turn; he did not, because no kit was on sale at the price, and he read the book before flying, which was right. Every Admiral's fill gate passed at its turn, and my own did after this turn's fixes.

## Plans

- **Next turns (CET):** Zero 08:00, Oracle 08:15, Mercury 08:30, Apollo 08:45, Apophis 09:00, mine 10:30.
- **At my 10:30 turn:** switch strict classes on if Trade's sell routes for the hunting loot stand at the receiving stations; read the first hand-overs and the traders' first sales after it. The 21 hand-over routes open by themselves the minute it goes on.
- **Recruitment Center:** pay its 2,000,000 cr fee from the treasury when Apollo reports the parts ready.
- **Still open, mine:** the shared guidebook commit wrapper; ammunition buys counted as fitting; hunts that note an empty magazine; the filler printing reasons for ships at work; the board line for a sweep inside a run; the two iron figures with Apollo. None was built this turn.
- **Done and out of my block:** the base-docking step before a pause stands in the pause procedure (step 3a); my flagships' sales are hand-overs now.

## Advice and Suggestions

- **Plainly, what happened:** the Admirals asked for four tools; three are built and tested, and Trinity had built the fourth. A money pipe was stuck: the ship that pays our savings into the treasury had 1.24 million cr waiting for three hours because its pass always ran out of time first; it now pays first, and 1.19 million moved at 07:11.
- **A risk I found and fixed:** at 05:53 CET a change to a shared check made every Admiral's test of a new build fail. No Admiral had a turn in that hour, so nothing broke; I fixed it before their 08:00 turns.
- **For you, Suggi, informing only:** I propose a simple habit for Trinity, me and the Admirals: before changing a file that checks everyone's work, name it in the queue log. Nothing else needs your word: no new pilot, no war, no message to another player is pending.

## Learnings

- **A switch that moves money between divisions is tested on where the money goes, not only on whether ships stay busy.** Record: the strict-classes dry run (0 ships waiting) against Trade's sell list, which takes no hunting loot. Change: I switch only when the receiving class's routes stand. Kept in `LEARNINGS.md` (unpromoted).
- **A step placed last in a pass with a time limit can starve without a word.** Record: `errors.log` ENT-126 and the sweep log. Change: what matters runs first, and a waiting step prints a line a check reads. Kept in `LEARNINGS.md`, its class in `knowledge/faults-that-leave-no-record.md`.
- **A shared check is tested where its users run it.** Record: `errors.log` ENT-127. For the fleet: a change of an install gate is tried in a member's copy too.
- Skill: collective-docs changed -- two pitfalls: a script that installs itself, and a gate tested where its users run it.

## Cross-links

- `reports/2026-11-22_unity_atria-funded-requests-answered-trinity-build-checked.md` -- my previous fleet report.
- `reports/2026-11-22_zero_laser-iii-proven-sales-become-gifts-iron-at-max.md` -- Mining.
- `reports/2026-11-22_oracle_stranded-scout-rescued-fuel-check-built-p5-gifts.md` -- Intel.
- `reports/2026-11-22_apollo_atria-kit-behind-its-ask-sales-out-bunker-from-own-cells.md` -- Logistics.
- `reports/2026-11-22_mercury_every-trader-operating-network-commerce-paid.md` -- Trade.
- `reports/2026-11-22_apophis_sales-become-gifts-pulse-laser-iii-proven-caustic-sac.md` -- Military.
- `communications/orders.log` ENT-062 -- the new orders; `communications/requests.log` ENT-337 to ENT-342 -- my answers; `communications/errors.log` ENT-126, ENT-127; `communications/queue.log` ENT-218.
- `governance/strategy.md`, `governance/rulebook.md` -- unchanged this turn.

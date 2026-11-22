---
name: jump-loops-capped-hunts-fuel-first-newborns-held-near
id: 20261122T222618Z
tier: report
trigger: session-end
author: Unity
tags: [fleet, fuel, births, requests]
links:
  - reports/2026-11-22_unity_one-iron-figure-fund-paid-handed-over-worth.md
  - reports/2026-11-22_oracle_sol-audit-first-worked-once-apart-galaxy-charted.md
  - reports/2026-11-22_zero_reserve-before-ice-jishui-cut-second-laser-test.md
  - reports/2026-11-22_mercury_docked-gas-crafts-sell-where-it-lies-first-bursar-order.md
  - reports/2026-11-22_apollo_boards-from-stores-proven-jump-loop-put-to-unity.md
  - reports/2026-11-22_apophis_booster-proven-recursion-short-dry-tanks-towed.md
  - governance/birth-plans.md
---

# The Collective -- Empty Jump Loops Capped, Hunts Fuel First, the New Empires' Pilots Kept Near Home

## Situation

Period: since my report of 19:17 CET (`reports/2026-11-22_unity_one-iron-figure-fund-paid-handed-over-worth.md`) to 23:26 CET. Orders now in force: `orders.log ENT-067` (ENT-066 written this turn, then ENT-067 on top of it for the birth wave).

The fleet as one purse (`hive.py stats kpi`, 23:17 CET): 9,936,898 credits (8,096,531 in the ships' wallets, 1,840,367 in the faction's savings). Steady money, meaning what comes in again and again minus what goes out (mostly fuel), reads -75,137 an hour over the last hour, -55,358 over 6 hours and -29,898 over 24 hours. Fuel alone cost 106,654 an hour over 24 hours. Money paid once (mission rewards minus one-off buys) was +46,274 an hour over 24 hours and is counted apart. The fleet still loses money every hour.

Where the fuel goes (view `fuel_sinks`, 22:39 CET, 24 hours): empty training jumps cost 763,525 credits in 1,504 ship-hours and scouting reads (census) 474,488; productive work earned +706,860. The empty jumps alone cost more than the whole daily deficit.

Ships: the fleet had 246 ships at the start. At 23:06 CET a birth wave began, by Suggi's word as Trinity relayed it (queue.log ENT-234): 254 new pilots of four other empires. At 23:26 CET 130 were registered and 3 had failed on the game's connection (`data/fleet/birth.json`). The "never idle" check (`fill.py check all`) passed at about 23:05 CET with 258 ships, then halted at 23:20 CET on one miner whose gathers stood full (Zero's plan), and passed again at 23:26 CET; that last reading counted only 100 of 380 ships while the births rewrote the fleet file, so I trust it less. No ship was lost.

Per division, steady net over 6 hours (`hive.py stats contribution`, 22:35 CET): Command -2,752 an hour; Mining -16,075; Logistics -20,283; Trade +36,620; Military -26,342; Intel -22,755. What the hunters and miners hand to the traders is worth, at today's bids, 279,023 credits (Military), 168,598 (Intel), 136,199 (Mining) over 24 hours; that value is not in the net.

## Strategy

Suggi's standing orders S1 to S5 and goals G1 to G5 stand unchanged, copied word for word into ENT-067. What I decided this turn, in plain words:

- **Stop paying for empty flying.** Rule F8 now says "zero empty burn". Both training loops fly ships in circles with an empty hold, only to grow their Piloting skill. I capped each loop at the pilots nearest the next skill step: 10 traders and 8 haulers. The others move to work that still trains but carries something: loads taken from where goods lie unsold to where they sell or are used, crafting while docked, standing market orders. The gate that keeps ships busy stays as it is. A ship docked with no work still counts as idle, because "never idle" (S5) is Suggi's order and not mine to soften. So each Admiral puts in the cap and the new work in one turn.
- **One new bigger hull at a time.** The warship (Recursion) is the first tier-2 test. I said no, for now, to Mining's 330,000-credit mining ship: the purse is losing money, and its pay-back is weeks, not days.
- **Trade may post standing buy orders up to 100,000 credits held in escrow in all**, each tied to a need or a margin above the 1 percent tax, one unit first (rule F39).
- **The scouts cut their fuel by a third**: they read first what our routes depend on and let older readings age.
- **The new pilots stay in their home regions first** (orders P6). Their empires lie 10 to 21 jumps away, with lawless space in between.

These are decided. The one open proposal is that the newborns' first wave should have waited for 400 seats and a positive 24-hour net, as governance/birth-plans.md had set. Suggi decided otherwise, and the wave runs.

## Divisions

- **Mining (Zero, `reports/2026-11-22_zero_reserve-before-ice-jishui-cut-second-laser-test.md`).** The reserve gathers before ice in every row, and the one iron figure from my last turn holds: Zero reads iron at 146,708 against 60,000, and the supply view and the reserve now agree. Suggestions: the Resonance Miner was declined for now (requests ENT-372; what changes it: the Recursion's three results, a positive 24-hour net, or a quote under 250,000). Seats for miners: open; Zero himself waits until the bunker is kept. A warning when a field will reach its floor before the next turn: accepted, not built this turn.
- **Trade (Mercury, `reports/2026-11-22_mercury_docked-gas-crafts-sell-where-it-lies-first-bursar-order.md`).** Trade is the only division in profit (+36,620 an hour over 6 hours). Suggestions: escrow cap accepted (100,000). The order steps in the runner were accepted, for Mercury to build himself, one order first. The sweep inside a run was already handled: the store reads that run at +3,202, not -8,315 (requests ENT-375). The liquid hydrogen for Apollo is between the two of them.
- **Logistics (Apollo, `reports/2026-11-22_apollo_boards-from-stores-proven-jump-loop-put-to-unity.md`).** Boards are now made from stored silicon. The jump loop question got answer (b), with cargo-carrying loops for the rest (requests ENT-374). The recipe rows of the reserve: open, to decide with Apollo at my next turn. A craft step's notes should list what it made: accepted, not built.
- **Military (Apophis, `reports/2026-11-22_apophis_booster-proven-recursion-short-dry-tanks-towed.md`).** The Shield Booster II is proven. Two hunters ran dry because The Levy station sold no fuel (errors.log ENT-142). Fixes built: hunts now take fuel before they set out and rest after a selling station gave none (requests ENT-376, commit c3184253). The Recursion's fund was topped up by 40,000 credits (requests ENT-371). A fund sized at quote plus 15 percent: declined as a rule; I give a margin case by case. The tug rescue: accepted, for Apophis to install first.
- **Intel (Oracle, `reports/2026-11-22_oracle_sol-audit-first-worked-once-apart-galaxy-charted.md`).** 30 of 30 scouts at work, and 92 percent of the places our routes use were read within 3 hours (stats contribution). Suggestions: pulling the frontier wayfinder out of the plans was not done for command; its 51 runs read 0 credits and it pays once, so I leave it to each plan. A filler line for once routes that pay over half their runs but a plan lacks: accepted, not built.
- **Thread check.** Last turn's iron fix held in Zero's numbers, and the fund paid (Apophis's Feedback). The command group's fill gate stopped once this turn, with 4 flagships waiting on thin herds. I fixed it by adding hand-over routes of their own stores (commit 1c5c1a96 and the next).

## Plans

- **Next turns (CET):** Zero 00:00, Oracle 00:15, Mercury 00:30, Apollo 00:45, Apophis 01:00, mine 02:30. Each Admiral finds orders ENT-067 with the loop caps and P6 for the newborns.
- **Built this turn and running:** hunts check fuel before setting out (`game/fleet/fuelplan.py`, `hunt.py`). The dispatcher rests a hunt whose selling station gave no fuel. A pilot born in another empire is never sent on a Voidborn mission, nor more than 6 jumps from where it stands, unless the route says `far_ok` (commit 8f10b70e). The dispatcher was restarted on the new code twice.
- **My next turn:** read the loop caps and the census cut in the 24-hour net. Put Apophis's tug script into the five-minute pass once I have read its dry run. Read Mercury's order steps. Give the four new flagships routes in their regions as readings come. Seat the newborns as seats open (99 of 200 filled now, briefing).
- **Open builds, not done this turn:** the field-floor warning (Zero); the once-route line (Oracle); a craft step's made-goods note (Apollo); the warning on a station that answered "no fuel" (Apophis); six old test failures that come from one test leaking into another (queue ENT-235); DECISIONS Q56, Q64 to Q73 as listed there.

## Advice and Suggestions

- **The birth wave.** Suggi decided it (via Trinity). It doubles the fleet while the fleet loses about 30,000 credits an hour over 24 hours. The newborns earn their starter rewards first, about 4,000 credits each from the survey mission alone (birth500.py). After that they need work their Admirals have not written yet. Until then the dispatcher keeps them near home and the fill gate will show them waiting. That is the honest state, not a fault.
- **Seats.** The faction has 200 seats and 99 are filled (briefing). 500 ships need 500 seats, so more recruitment buildings come first in Apollo's list.
- **Other players:** one pilot wrote to a flagship of ours in local chat, asking which lanes we fly and offering to swap star charts of Sirius, Sol and Moonshadow (inbox, 21:46 CET). Under rule F4 no pilot of ours answers without Suggi's word. My default is no reply. A chart swap would tell them where we work.
- No other decision waits on Suggi.

## Learnings

- **Lesson:** when the fleet changes what it is (a switch flips, or pilots of a new empire join), every rule that hands out work was written for the old fleet. Record: the dispatcher held 30 Voidborn missions open to one newborn Solarian miner, read at 23:13 CET; the herd-claim failure of this morning came from strict classes (errors.log ENT-131). What changes: before such a change reaches a ship, I list what each reader of the changed fact assumes and guard it in code in the same turn. Kept in `knowledge/fleet-employment.md`.
- **Lesson:** a request about a wrong figure is first replayed through today's code. Mercury's case was already right in the store. Takeaway for the Admirals: a run's figure is in the table `runs`, not on the RESULT line.
- **Lesson:** I wrote a wrong test count into a public answer from memory and corrected it two minutes later (errors.log ENT-143). Counts come from this run's tool output.
- Skill: fleet-ops changed -- pitfalls for newborn pilots, replaying a figure, a baseline for test failures, counts from tool output.
- Skill: fleet-play no change (shared and read-only; the same pitfalls are proposed for it here).

## Cross-links

- `reports/2026-11-22_unity_one-iron-figure-fund-paid-handed-over-worth.md` -- my previous fleet report.
- `reports/2026-11-22_oracle_sol-audit-first-worked-once-apart-galaxy-charted.md` -- Intel.
- `reports/2026-11-22_zero_reserve-before-ice-jishui-cut-second-laser-test.md` -- Mining.
- `reports/2026-11-22_mercury_docked-gas-crafts-sell-where-it-lies-first-bursar-order.md` -- Trade.
- `reports/2026-11-22_apollo_boards-from-stores-proven-jump-loop-put-to-unity.md` -- Logistics.
- `reports/2026-11-22_apophis_booster-proven-recursion-short-dry-tanks-towed.md` -- Military.
- `governance/birth-plans.md` -- the Plan-500 waves and their gates.
- `communications/orders.log` ENT-066, ENT-067; `communications/requests.log` ENT-371 to ENT-377; `communications/queue.log` ENT-234, ENT-235; `communications/errors.log` ENT-143.

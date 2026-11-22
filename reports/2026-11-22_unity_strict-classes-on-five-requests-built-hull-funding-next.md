---
name: strict-classes-on-five-requests-built-hull-funding-next
id: 20261122T100340Z
tier: report
trigger: session-end
author: Unity
tags: [fleet, strict-classes, plumbing, purse]
links:
  - reports/2026-11-22_unity_requests-built-deposit-unblocked-strict-classes-wait.md
  - reports/2026-11-22_zero_laser-iii-lockout-lifted-far-carbon-takes-the-ships.md
  - reports/2026-11-22_oracle_fuel-check-installed-offlist-readings-back-on-lists.md
  - reports/2026-11-22_mercury_loot-sell-routes-stand-for-strict-classes.md
  - reports/2026-11-22_apollo_recruitment-center-parts-staged-by-route.md
  - reports/2026-11-22_apophis_first-group-kill-pilot-whale-plasma-verdict.md
---

# The Collective -- Strict Classes Switched On, Five Asks Built, Hull Funding Next

## Situation

Period: since `reports/2026-11-22_unity_requests-built-deposit-unblocked-strict-classes-wait.md` (06:18 UTC) to 10:05 UTC on 2026-11-22 (07:18 to 11:05 CET). Orders: `orders.log ENT-062` at the start, `ENT-063` from 10:00 UTC.

- **The purse** (`hive.py briefing`, 09:30 UTC): wallets 8,205,469 cr plus the faction's treasury 3,429,412 cr make 11,634,881 cr. Steady net (income minus fuel and repairs, one-time rewards left out) stood at +545 cr an hour over 6 hours and +12,371 over 24 hours.
- **After the switch** (`hive.py stats kpi`, 10:03 UTC): the last hour's steady net is -56,868 cr; 6 hours -2,583; 24 hours +11,128. One-time rewards brought 60,031 cr in that hour. The dip is expected and explained in Divisions: the hunters now give their loot away instead of selling it, and the traders' first sales are still ahead.
- **Ships:** 246, none lost; the "never idle" gate passed at 10:01 UTC (234 at work, 3 starting, 0 waiting, 9 flying an engine goal; `fill.py check all`).
- **Divisions, last hour at 09:30 UTC** (briefing money table): Military +48,577 cr; Command +5,084; Mining +536; Logistics -17,884; Intel -21,139; Trade -25,585.
- **Seats:** 99 of 100 (briefing EYES & EARS); the Recruitment Center (200 more) waits on 4 flex polymer: 296 of 300 at 09:52 UTC (`needs.py show recruitment-center`).
- **The game's own skill (Voidborn) at level 1 or more** (table ship_skills, 10:03 UTC): command 6 of 6, scouts 26 of 30, haulers 32 of 40, sentinels 14 of 20, drones 33 of 50, traders 18 of 40, miners 21 of 60.

## Strategy

Suggi's standing orders S1 to S5 and goals G1 to G5 stand as he wrote them (`orders.log ENT-063`, copied word for word). What changed this turn, decided by me inside my mandate:

- **Strict classes are on (decided, orders P5, decision D244).** Since 09:35:37 UTC only traders sell. Plainly: before, a hunter sold its own loot at the station; now it hands the loot to one of our traders, who sells it. Miners hand ore to haulers, who turn it into parts we build with. Why: Suggi wants each class to do its own job and level its own skills, and crafting trains a hauler about ten times faster than flying empty loops, at no fuel cost (Apollo's figures, `hive.py stats xp`). I held it back one turn until Trade had sell routes at the stations where the loot lands; Mercury built them (queue ENT-222), so the condition I set held.
- **The Recruitment Center gets the treasury's 2,000,000 cr first (decided, P4).** Apollo builds it at his turn as soon as the last flex polymer stands (requests ENT-347).
- **One Recursion for Military after it (decided, F17 one ship first).** A tier-2 fighting hull for about 315,699 cr. The treasury can pay both (3,429,412 minus 2,000,000 leaves 1,429,412), but no script yet moves treasury credits into one pilot's wallet without the sweep taking them back; I build that next turn (requests ENT-348).
- **Not decided, proposal only:** a south-east base. Oracle filed an NPC raid that destroyed another faction's outpost at Fomalhaut (queue ENT-221). North stays first (P3); Fomalhaut needs its raid record read before anyone builds there.

## Divisions

- **Mining (Zero, `reports/2026-11-22_zero_laser-iii-lockout-lifted-far-carbon-takes-the-ships.md`).** Found and fixed why 17 refitted miners flew empty loops for three hours (errors ENT-128). Plainly: routes asked for "the old laser" by its exact name, so a ship with the new laser was turned away. Mining steady +19,342 cr in its hour at 07:17 UTC. Suggestions: a module list in the gate, *accepted and built* (c3a8f585); the two iron figures that disagree, *open* (mine, in the chain review, not done this turn); the filler counting ships on a fallback while their own class's route is closed, *open*. Thread: the far carbon tests he planned last turn were written and taken; his claim of the Laser III fit holds.
- **Intel (Oracle, `reports/2026-11-22_oracle_fuel-check-installed-offlist-readings-back-on-lists.md`).** The scouts now check their fuel before a trip (the cause of last night's stranded scout), and seven systems that no list read for four to six days are back on lists. 30 of 30 at work. Suggestions: a list switched off moves its systems, *accepted* as each Admiral's own practice; weigh the Fomalhaut raid, *done* (queue ENT-223); a count per reason in `fill.py status`, *open*. Thread: matches; his census routes read the outpost every 50 minutes.
- **Trade (Mercury, `reports/2026-11-22_mercury_loot-sell-routes-stand-for-strict-classes.md`).** Summed a day of hunt sales by station and wrote 12 sell routes where the loot lands. Suggestions: switch strict classes on, *accepted and done*; a lower cap on the traders' training loop, *declined for now*: his traders now get sales to fly, and choosing the least fuel per XP is his under P1; `requires.stored` list wording in the blueprint, *open*. Thread: Trade's fuel loss (-25,585 cr an hour) is the training loop; the sales are the test of the switch.
- **Logistics (Apollo, `reports/2026-11-22_apollo_recruitment-center-parts-staged-by-route.md`).** Moved the Recruitment Center's parts into the faction store by routes: plate and boards complete, flex 296 of 300. All three asks *accepted and done* (ENT-347). Thread: his haulers' loss (-17,884 cr an hour) came from waiting on the switch; it is on now.
- **Military (Apophis, `reports/2026-11-22_apophis_first-group-kill-pilot-whale-plasma-verdict.md`).** First group kill: three drones with the better laser killed a pilot whale in six ticks at full hull. 350 hunts, 979 kills, +108,542 cr since 04:36 UTC (his table runs). Two scars (ENT-129, ENT-130), both fixed by his own scripts. Suggestions: the Recursion, *accepted*; ammunition kept aboard, *done*; stop scripts by their python process, *accepted*; a clearer "by hand" label, *open* (it counts ships whose engine flies a goal); several drops in one call, *open*.
- **Command (mine).** Flagships hunted; two routes the filler gave them were Military's claims, and I took them out (errors ENT-131).

## Plans

- **Next turns (CET):** Zero 12:00, Oracle 12:15, Mercury 12:30, Apollo 12:45, Apophis 13:00, mine 14:30.
- **Watch first:** the traders' first sales of handed-over loot and the hauler crafts that open. If sales do not bring the money back within a turn, the switch is weighed again on its record.
- **My next build, in this order:** (1) the treasury-to-pilot funding with a sweep exemption that ends by itself, then the first Recursion funded (ENT-348); (2) why the filler's status and write disagree on a claimed route (errors ENT-131), with a test first; (3) the two iron figures with Apollo.
- **Still open and not built:** the shared guidebook commit wrapper; ammunition buys counted as fitting; the filler printing reasons for ships at work and a count per reason; the board line for a sweep inside a run; the "by hand" label; several drops in one call; the `requires.stored` wording. Older open builds stand in DECISIONS.md Q64 to Q73.
- **Recruitment Center:** Apollo builds it when 300 flex stand; then the member cap rises from 100 to 200 (`governance/empire.md`, the faction ladder) and the first 100 of our 147 ships outside the faction can join.

## Advice and Suggestions

- **Plainly, what happened:** the fleet now works the way Suggi asked on 2026-11-21: each class does its own job and hands its goods to the class that uses them. 100 hand-overs went through in the first 24 minutes (`data/routes/runs.jsonl`), with no ship idle. Money fell in the first hour because the loot is now in the traders' storage, not yet sold; it should come back as their sales run.
- **What I built for the Admirals:** five things they asked for, each with tests that failed first and the whole test suite passing (901 tests): routes can ask for "any of these modules", a warning when a refit would lock ships out, several receivers per station, free reads of the freight board, and hunters keep their ammunition.
- **For Suggi, informing only:** no new pilot, war or message to another player is pending. I committed Trinity's Mobile Base lines into my MISSION.md and ROSTER.md, as the rulebook already holds them.

## Learnings

- **A new warning gate is run on today's live tree before the install, not only on the old fault.** Record: the first draft of the refit warning flagged two refit routes of Military's plan against each other, each the other's alternative; after the rule was added it flagged none (`routes.py check` on the scratch tree, before commit c3a8f585). Change: such flags are read row by row before an install, so warnings stay worth reading. Kept in: skill collective-docs (pitfall on gates). Fleet takeaway: a warning nobody can act on teaches the members to skip warnings.
- **The switch lesson held:** I switched only after the receiving class's routes stood, and no ship waited after it (`LEARNINGS.md`, unpromoted, until the sales confirm it).
- Skill: collective-docs changed -- a new gate is also run on the live tree before the install.

## Cross-links

- `reports/2026-11-22_unity_requests-built-deposit-unblocked-strict-classes-wait.md` -- my previous fleet report.
- `reports/2026-11-22_zero_laser-iii-lockout-lifted-far-carbon-takes-the-ships.md` -- Mining's turn.
- `reports/2026-11-22_oracle_fuel-check-installed-offlist-readings-back-on-lists.md` -- Intel's turn.
- `reports/2026-11-22_mercury_loot-sell-routes-stand-for-strict-classes.md` -- Trade's turn.
- `reports/2026-11-22_apollo_recruitment-center-parts-staged-by-route.md` -- Logistics' turn.
- `reports/2026-11-22_apophis_first-group-kill-pilot-whale-plasma-verdict.md` -- Military's turn.
- `communications/orders.log` ENT-063 -- the orders in force.
- `communications/requests.log` ENT-346, ENT-347, ENT-348 -- my answers.
- `communications/errors.log` ENT-131 -- the claimed routes the filler added.
- `communications/queue.log` ENT-223 -- this turn's notice.
- `governance/strategy.md`, `governance/rulebook.md` (F8, F10, F17, F23, F37) -- the rules this turn worked under.

---
name: cut-deposit-booked-sweep-writes-ahead-test-round-ends
id: 20261121T220647Z
tier: report
trigger: session-end
author: Unity
tags: [fleet, money, treasury, sweep, test-round, orders]
links:
  - reports/2026-11-17_unity_iron-met-make-before-gather-acrab-chosen.md
  - reports/2026-11-21_zero_resume-short-ores-lifted-gathers-first-guidebook-capped.md
  - reports/2026-11-21_apollo_outpost-wrecked-repair-by-route-every-hauler-at-work.md
  - reports/2026-11-21_mercury_silver-to-arneb-paid-once-home-bids-gone-freighter-bought.md
  - reports/2026-11-21_oracle_after-the-pause-far-work-read-every-three-hours.md
  - reports/2026-11-21_apophis_guidebook-capped-laser-iii-fitted-bulwark-group-no-kill.md
---

# The Collective -- The Test Round Ends in the Black: a Cut Deposit Is Booked and the Sweep Writes Ahead

## Situation

Period: from my report `reports/2026-11-17_unity_iron-met-make-before-gather-acrab-chosen.md` (reports.log
ENT-081, 2026-11-17 22:08 UTC) to this turn, 2026-11-21 21:31 to about 22:10 UTC. Inside it: the chat round r21 of
2026-11-18 (DECISIONS D239, orders ENT-054 to ENT-056), the pause of the whole fleet from 2026-11-18 to the resume of
2026-11-21 19:25 UTC (queue.log ENT-192), and Suggi's test round: one turn of each Admiral by hand from about 19:30
UTC, mine last, every schedule paused (queue.log ENT-193). Orders in force at the start: orders.log ENT-057; at the
end ENT-058.

The fleet as one purse (`hive.py stats kpi`, 21:56 UTC). "Steady net" is what the work that repeats earns an hour
after fuel; "paid once" is the reward of a mission a pilot can do only once, kept apart because it ends.

```
Ships: 246, at work 205, waiting 37 (all traders), by hand 4 (fill.py check all, 22:05 UTC); lost: 0
Steady net per hour: +49,212 (1 h), +57,477 (6 h), +14,381 (24 h, mostly paused hours)
Paid once per hour: +126,370 (1 h); net of everything +175,582 (1 h)
Money: wallets 10,955,587 + treasury 544,606 = 11,500,193 cr
```

One line per division, from its Admiral's report of today and the money of the last hour at 22:05 UTC (`hive.py
fleet`):

- Mining (Zero, `reports/2026-11-21_zero_...`): short ores (silicon, gold, nickel, carbon) get the ships first; 60 of
  60 at work; +6,492 cr an hour.
- Logistics (Apollo, `reports/2026-11-21_apollo_...`): our outpost GSC-0044 was found wrecked; its whole repair bill
  stands in its faction storage; 39 of 40 at work; -17,365 cr an hour, mostly fuel of a training loop.
- Trade (Mercury, `reports/2026-11-21_mercury_...`): one far silver trade paid +4,099 cr once; the home bids are gone
  after the pause; 37 of 40 docked; +163 cr an hour.
- Intel (Oracle, `reports/2026-11-21_oracle_...`): every place where other divisions work far out is read every three
  hours; a Sable pirate pack of twenty found; 30 of 30 at work; -19,487 cr an hour, census fuel.
- Military (Apophis, `reports/2026-11-21_apophis_...`): a stronger laser fitted on one drone, a three-ship group fought
  and made no kill; 67 of 70 at work; +51,497 cr an hour.
- Command (mine): six flagships hunting; +618 cr an hour.

## Strategy

What Suggi decided in the period, in his words' sense (DECISIONS D239 to D242):

- 2026-11-18 (D239): every member is measured first by his standing goals, then by the plan, then by its own block of
  the orders; profit is read for the whole fleet, never one division; work that is full at home goes further out,
  never onto another class's work; keeping the system lean is my job.
- 2026-11-21 (D240): a claim of a route stands until its writer releases it; the reports stay as they are.
- 2026-11-21 (D241): yes to the storage book's guard and to the game's records at its new version (both built,
  commit 71ed82cd); every Admiral, at its next turn, researches the game online and its own role and writes it down
  (P5). P5 stays until each Admiral's next turn has run.
- 2026-11-21 (D242): the needs register (what each division needs for its upgrades, `game/needs.tsv`); each division
  decides its own work ("he should find out, do his own research and then make his own decision"); passenger lines
  are Logistics'.

The plan in force (orders ENT-058, unchanged in its parts against ENT-057 but for my block and the watch line): P1 an
economy that pays for itself, steady net above zero over 24 hours with no ship idle; P2 lean supply; P3 the outpost
Atria, then the station Yildun; P4 the faction's ladder, 200 seats, then 400; P5 the research of each role.

Where we stand on them. P1: the last hour and the last six hours are above zero (+49,212 and +57,477 cr an hour);
the 24-hour figure (+14,381) still holds the paused hours and becomes the true test by about 19:30 UTC tomorrow. The
"none idle" half fails: 37 traders wait docked (time view: traders 87 percent docked over 24 hours). P3: Atria waits
for the outpost to run again. P4: the faction holds 99 of 100 seats (table faction); 200 seats need a Recruitment
Center, fee 2,000,000 cr (game/rules/09-factions.md; the official factions guide read today agrees); the treasury
holds 544,606, so about 1,455,000 cr are still to come. G2, the 1,000-member faction, needs the tier-5 office of
20,000,000 cr at one station: the cap is the best office in full plus a quarter of each other office.

My recommendation, a proposal: the treasury is the road to P4 and G2, so its money figures must be true before any
spend is planned on them. That is why this turn put the money record first.

## Divisions

Each division, its thread over its last two reports, and my answer to each suggestion.

**Mining (Zero).** The plan of 2026-11-17 named the steel goal and five tests; today's report reads those tests
(Crystal Resonance 4,000 cr once, Material Synthesis 1,500 once, the outpost belt 342 and 367 ore a run): the thread
holds. Its numbers agree with the fleet's (60 of 60 at work). Suggestions: (1) a gate that opens a mine route only
while our own stored units stand under a number: accepted, open build Q75 (1). (2) the storage book's guard: done
(requests ENT-298, commit 71ed82cd). (3) the filler should not offer tests from an old route-maker list: accepted,
Q75 (2); the route maker runs again since 21:25 UTC (services status).

**Logistics (Apollo).** The plan of 2026-11-18 was the bunker runs, the Center and Atria; the wreck overtook it and
the report says so plainly. Two training runs of +12,321 and +5,321 cr are named with "cause not found"; a wallet
gift landing inside a run is the likeliest cause, not checked. Suggestions: (1) an alert when a base of ours reads
damaged: accepted, Q75 (3), first in line, since our outpost stood wrecked for three days while every tool printed
it active. (2) how an outpost is kept while the fleet is away: his own decision (requests ENT-301, Suggi's D242).
(3) the training loop as fallback: kept; the fleet's steady net carries it now, and his own plan cuts it if the
24-hour net falls under zero.

**Trade (Mercury).** The plan of 2026-11-17 (iron into steel, +5,000 cr an hour) did not survive the pause: the
traders' stores are used and the home bids are gone. The thread breaks for a reason outside the division. He repeated
one mistake (a one-load trade put into the plan) and named it himself. Suggestions: (1) `requires.ask`, a gate on the
buying end: accepted and being built (ENT-305). (2) the traders' standing work: his own decision after his P5
research (ENT-293); his recommendation, docked until the freighter's first carry is read, stands. (3) a failed buy
ends a run: open, Q75 (6).

**Intel (Oracle).** The plan of 2026-11-17 named the probe test; it is "not done" again today, the second report in
a row: the thread breaks there. The rest holds: the roads are read and the far places are now read every three
hours. Suggestions: (1) a census list computed from where ships fly and (2) a books service: open, Q75 (5). (3)
fleet-build.sh puts its files back when stopped: accepted, Q75 (4).

**Military (Apophis).** The plan of 2026-11-18 said the next group takes prey of 100 hull or less; today's group took
a bulwark of 95: the thread holds. No kill, because the members arrived after the fight opened. Suggestions: (1) a
runner that refuses a fresh hand hold: being built (ENT-303). (2) a weapon swap in the fit step: being built
(ENT-304). (3) the filler should skip routes set off for danger, claimed or of another class: accepted, Q75 (2). (4)
fits from the fleet's purse once his test measures: yes, as my answer ENT-271 said; he names the fit and its price.

No two reports contradict each other. Mercury reports the clone's push stopping at about 20:14 UTC and Oracle three
installs refused on a stray file; Morpheus's queue.log ENT-195 records the watcher fixed at 20:37 UTC (it rebases in
a copy of its own now), and the stray file was committed (requests ENT-302).

## Plans

**The divisions** (their own choices, inside ENT-058): Mining reads the storage book whole and lets the pull rule
open or close iron by itself. Logistics finishes the outpost repair and reads the bunker's first result. Trade reads
the freighter's first carry and its research decides the traders' standing work. Intel reads the roads again and the
books from afar. Military finishes the laser test and the next group waits for the group script's two changes. Every
Admiral does P5 at its next turn and adds its needs to the register.

**What I do myself, in this order:**

1. The four builds of the test round (ENT-288 to ENT-290, ENT-297) are written in a scratch copy by the chat
   session's worker (its files of 22:04 UTC; it touches no file of this turn's). Each is installed only after the
   whole test suite passes, and each request is closed with its commit.
2. Q75, the seven builds the Admirals' reports named, after that install, since they touch the same scripts:
   (3) the damaged-base alert and (7) the sweep's gifts written down before their call come first, because a wrecked
   base and a lost record hide from every reader.
3. Atria's money (requests ENT-272) when Apollo names the outpost running by itself.
4. P4: the Recruitment Center's fee from the treasury once it holds it; the treasury's own trend is to be read by the
   store once it holds a reading 24 hours apart (kpi: "purse change: not measured").
5. The turn jobs start again only on Suggi's word.

**The command group.** The six flagships hunt far grazers, one ship to a herd. Prime Directive waited at 22:03 UTC
with six units of loot aboard, which closed every hunt to it ("hold not empty"); the plan's last list now stores a
hold before parking (commit 004c2758). The filler offered it a visit mission in Crimson space; I left it out: it is
Intel's class of work and its board reading dates from 2026-11-18.

## Advice and Suggestions

What the players decided this turn and why:

- **A booking fixed before anything else.** At about 21:08 UTC the five-minute job moved 84,115 cr from Prime
  Directive into the faction's treasury and was cut off by its own time limit before writing it down. The money was
  safe in the treasury, but the fleet's books showed it as 84,115 cr spent: the last hour read a loss of 45,929 cr
  instead of a gain of about 38,000. I booked it once, with its own time, and changed the sweep so that a deposit is
  written down before it is sent and checked at the next pass (commit 92417be2, three tests that fail on the old
  code). Its first live pass at 21:52 UTC wrote and booked 63,721 cr.
- **The traders stay docked for now.** A docked ship costs nothing. 37 traders wait because the home buyers left
  during the pause; Mercury decides their work after his research, as you said.

What I advise you to look at: before the next pause of the fleet, every ship docked first. During the pause of
2026-11-18 the game towed 48 of our drifting ships home for 500 cr each (about 24,000 cr), and our outpost, with no
ship of ours signed in, was wrecked.

Steps that are yours alone: none is asked for now. No new pilot, no war and no word to another player is proposed;
the fleet works inside its orders until you speak.

## Learnings

From the learning capture of this turn:

- **A record written after its call dies with the pass that is cut.** The sweep wrote its deposit down after the
  call and after waiting to see it land; the job's limit of 200 s ended it in between. Record: the treasury 365,083
  to 449,198 cr between 21:06:59 and 21:28:47 UTC with no deposit row (data/fleet/sweep.jsonl, onetime.json,
  empire.json), errors.log ENT-116. What I do differently: a step that moves money writes `sent` before its call and
  the next pass settles it where the money lands; a long step starts only early in a pass. Kept in
  `knowledge/money-figures.md` (updated) and the command guidebook's lessons. For the Admirals: the same shape stands
  in every script of theirs that calls the game and then waits to book.
- **A pause costs money when ships are left in space.** Record: 48 tow messages of the Galactic Salvage Authority to
  our pilots, 2026-11-18 02:03 to 02:06 UTC (`inbox.py show --to-us`), errors.log ENT-112 for the outpost. Kept
  unpromoted in LEARNINGS.md until a second pause shows whether docking first is enough.
- **Confirmed, nothing new:** the official factions guide (read today) agrees with our records on the member cap and
  its offices; the comms gate refused an orders entry over its word limit and named the rule.
- **An apply script's own guard can refuse it.** My first script looked for each edit's new text to stop a second
  run; an edit that deletes has its new text inside the old. Caught before any write.

Skill: collective-docs changed -- an apply script guards on one marker the change adds, not on each edit's new text.

Open questions: whether the sweep's gifts can be cut the same way (Q75 (7)); what wrecked our outpost (requests
ENT-296 to Intel).

## Cross-links

- `reports/2026-11-17_unity_iron-met-make-before-gather-acrab-chosen.md` -- my previous report, the start of the period.
- `reports/2026-11-21_zero_resume-short-ores-lifted-gathers-first-guidebook-capped.md` -- Mining.
- `reports/2026-11-21_apollo_outpost-wrecked-repair-by-route-every-hauler-at-work.md` -- Logistics.
- `reports/2026-11-21_mercury_silver-to-arneb-paid-once-home-bids-gone-freighter-bought.md` -- Trade.
- `reports/2026-11-21_oracle_after-the-pause-far-work-read-every-three-hours.md` -- Intel.
- `reports/2026-11-21_apophis_guidebook-capped-laser-iii-fitted-bulwark-group-no-kill.md` -- Military.
- `communications/orders.log` ENT-058 -- the orders in force.
- `communications/errors.log` ENT-116 -- the cut deposit.
- `communications/requests.log` ENT-302 to ENT-305 -- the four builds accepted.
- `game/fleet/wallet.py` -- the sweep at commit 92417be2.
- `game/rules/09-factions.md` -- the member cap and its offices.

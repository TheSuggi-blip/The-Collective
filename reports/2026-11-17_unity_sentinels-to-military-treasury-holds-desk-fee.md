---
name: sentinels-to-military-treasury-holds-desk-fee
id: 20261117T182424Z
tier: report
trigger: session-end
author: Unity
tags: [fleet, treasury, sentinels, fill, escort, orders]
links:
  - reports/2026-11-17_unity_pirate-gate-treasury-filled-kit-at-base-price.md
  - reports/2026-11-17_zero_waiting-miners-to-deep-core-achernar-silicon-test.md
  - reports/2026-11-17_oracle_survey-step-in-census-exploration-xp-is-per-pilot.md
  - reports/2026-11-17_mercury_collective-provides-six-ships-crystal-craft-off-for-reserve.md
  - reports/2026-11-17_apollo_outpost-kit-route-on-desk-goods-stand-workshop-lifted.md
  - reports/2026-11-17_apophis_escort-follow-built-far-bids-gone-curd-stored.md
---

# The Collective -- The Sentinels Serve Military, the Treasury Holds the Desk's Fee, the Filler Keeps Each Division's Rules

## Situation

Period: from my report `reports/2026-11-17_unity_pirate-gate-treasury-filled-kit-at-base-price.md` (turn of
13:30 UTC) to the end of my scheduled turn of 17:30 to about 18:45 UTC on 2026-11-17. All times here are UTC;
Suggi's are CET, one hour later. All five Admirals reported in their turns of 15:00 to 16:53 UTC; each job's
last run reads `ok` (`hermes cron list`).

Where the fleet stands, in plain words: every one of our 246 ships has work (the fill gate, the check that no
ship sits idle, read PASS at 18:21 UTC: 240 at work, 3 starting, 0 waiting, 3 held by hand). Our first base,
CLTV Outpost GSC-0044, stands since about 16:40 UTC (DECISIONS D224). The money: the ships' wallets hold
10,174,331 cr (`hive.py fleet`, 18:06 UTC) and the faction's shared purse, the treasury, 365,079 cr after this
turn's sweep (the game's view of the faction storage, 18:20 UTC). The steady money, which repeats and leaves out
rewards the game pays only once, is still below zero: -27,458 cr an hour over 6 hours and -18,155 over 24
hours. Rewards paid once (missions each pilot can do once) brought 89,717 cr an hour over 24 hours and carry the
wallets. The last hour read -148,544 cr, but that hour is bent by my sweep: 189,040 cr of gifts were booked
before the receiving wallet showed them, so they read as costs for an hour.

| Division (Admiral) | Ships | At work 18:21 | Steady income per hour, runs of 4 h | Paid once per hour |
|---|---|---|---|---|
| Command (Unity) | 26 -> 6 | all | +19,531 | 14,466 |
| Mining (Zero) | 60 | all | -12,707 | 22,000 |
| Logistics (Apollo) | 40 | all | -5,270 | 487 |
| Trade (Mercury) | 40 | all | -8,078 | 17,375 |
| Military (Apophis) | 50 -> 70 | all | +7,392 | 10,125 |
| Intel (Oracle) | 30 | all | -14,462 | 16,144 |
| Fleet | 246 | 240 + 3 starting | -13,594 | 80,597 |

Source: `hive.py tasks` (runs of the 4 hours to 18:06 UTC) and `fill.py check all` (18:21 UTC). The 20 sentinels
moved from Command to Military at 18:20 UTC; the money column is from before the move.

Each division in one line, from its Admiral's newest report: Mining sent its waiting miners to Deep Core
Prospecting and tested silicon at Achernar, and missed its iron goal; Intel added a survey step to the census and
found that exploration XP is paid per pilot; Trade put six ships on The Collective Provides and switched its
crystal craft off for the reserve; Logistics wrote the outpost kit route, staged the Desk's goods and lifted the
workshop mission; Military built the escort's follow step, saw its far buyers leave and stored curd.

## Strategy

The strategy in force is phase 1, income (`governance/strategy.md`): make the fleet earn more than its fuel,
keep every ship at work, level every ship by its role, and build the faction's ladder and the first bases.

What Suggi decided in this period (from my chat, word for word in DECISIONS D225 to D228; in the orders as
D11 to D14 of `communications/orders.log` ENT-039):

- **Money (D11).** A ship keeps up to 50,000 cr; what it holds above goes into the faction treasury, between
  runs, never the moment it crosses the line. The treasury is the fleet's main purse. The 50 new seats the
  Recruitment Desk brings go to miners first, those working the fields around our outpost first. Every good that
  must never run out (iron, fuel, later food and power) gets a supply chain every member can read.
- **The sentinels (D12).** The 20 sentinels, until now the Fleet Admiral's guard, go to Military: Apophis trains
  them like his drones and hands each back at Piloting 20 (the skill that opens bigger hulls).
- **Rest, not off (D13).** A route that does not pay rests 6, then 24, then 72 hours at most by its record,
  and wakes early when its buyer, field or herd comes back; switched off only for danger or a replacement.
- **Groups (D14).** Military, and scouts when it serves, may hunt in groups of 3 to 20 ships (a game fleet: the
  leader flies and fights for all) to take prey one ship cannot, and later pirates. Pirates stay closed (D9).

What I decided inside that: the treasury was filled by hand this turn, because the Desk's fee had to be held
whole before Logistics' turn (the game pays a faction fee from the treasury only when it holds the whole sum;
otherwise from the builder's wallet, which cannot pay 300,000 cr). The sentinels moved in this turn, not the
next, after I found why the first try failed (below). My recommendation, marked as mine: keep the next turns
on income, the outpost's use and the Desk; nothing bigger is bought until the steady money is above zero.

## Divisions

**Mining (Zero).** Reported the iron goal missed: it measured the fleet's stock, which every division's
crafts draw on; from now on Mining sets goals on its own stored flow. Thread: the miss and its cause are stated
plainly; it holds together. Suggestions: (1) buy carbon instead of gathering it (92,426 short, no field within
7 jumps holds more than 1,357): accepted in principle as Trade's to buy inside rule F12; the purse is open
until the treasury refills after the Desk. (2) A lift pass between turns: accepted, it is open build Q68 (12),
built with D13's rest at my next turn. (3) A hull commission's state in the ship file: accepted, open. (4)
Measure by own flow: accepted; the Measure line names both.

**Intel (Oracle).** Built a survey step into the census; found that exploration XP is paid per pilot for
systems it has never visited. Suggestions: (1) a skill history in the store: accepted, open (it is the backlog's
XP per route). (2) The per-pilot exploration rule: accepted and carried to the fleet here. (3) Treasury
deposits out of run figures: done this turn (requests ENT-239). Its note that `status` read "2 by hand" while
it held nothing is right: engine goals between runs show so; a clearer word is open.

**Trade (Mercury).** Missed its goal of steady money above zero (no bid at our stations for what it carries);
switched its own crystal craft off when it found it used goods the reserve holds back. Suggestions: (1) the
filler counts held-back goods: done (ENT-240). (2) `plan.py check` refuses a plan file with a heading twice:
accepted, open; Military's plan file carries the same fault (an older copy under Notes), so it is real. (3) The
route maker writes a mining contract's route: open. (4) The orders' open once-money figure was stale: taken
out of the orders.

**Logistics (Apollo).** Planned the outpost founded; it was (D224), so its thread holds. Staged 100 boards
and 200 plate for the Desk. Suggestions: (1) a station core on offer at 15,000,000 cr: declined for now, the
fleet holds about 10.5 million cr in all and its steady money is below zero (see Advice). (2) A ship with a
timed job skips the list First: accepted, open (a dispatcher change). (3) The treasury for the Desk: done
(365,079 cr, requests ENT-242).

**Military (Apophis).** Built `guard.py --follow` and flew it once at home (it trails a moving ship by one
jump); its far buyers left (gland bid 4,265 to 480 cr, melt 1,528 to 54 cr within hours), so the hunts store.
Thread: it planned the gland sales; they never flew, and it says why. Suggestions: (1) no tests in front of
guard ships: done (ENT-241). (2) A claim gate on the filler: done. (3) Far bids as a fleet figure: accepted, and
handed back with the door named: a verb of `hive.py` is Military's to build through `fleet-build.sh`.

No two reports contradict each other. I checked the money lines against `hive.py fleet`; they agree.

## Plans

Each division, by orders ENT-039 (`communications/orders.log`):

- **Mining:** gather the fields one jump around the outpost; its miners take the Desk's new seats first, so
  they can dock, store and refuel there; the Liminal hull and Deep Core Prospecting as before.
- **Trade:** sell the surplus, keep the once-missions, and decide on the gather field I lifted for its
  waiting traders (gather-okab-belt 28 to 42 ships at 18:00 UTC; it holds 167,305 units above its floor).
- **Logistics:** build the Recruitment Desk at its turn of 19:45 UTC from the treasury (cap 50 to 100), then
  test with one hauler that a run unloads into the outpost's storage and refuels at its fuel bunker.
- **Military:** plan the 20 sentinels in its own plan file (they stand there since 18:20 UTC, each on the
  hunts it had and Military's hunter template); write the first escort for Logistics' runs to the outpost;
  fly one group of three drones by hand on a pilot whale near home, and record what the game answers.
- **Intel:** about ten scouts explore north and south for the next two sites, 3 or 4 systems out by rule
  F33, and name the candidates; GSC-0044 and its neighbours read every hour.

My own next turn (22:30 CET): the five-minute sweep into the treasury as a script (a ship in a fight refuses
its gift, so it skips such ships and takes them later), a losing route's rest by its record (D13), the
dispatcher's half of a group hunt from Military's test (D14), the sentinels' money under Military on the
station, the duplicate-heading check of plan files, then the supply chains (D11). The turn jobs run next at
20:00 (Zero), 20:15 (Oracle), 20:30 (Mercury), 20:45 (Apollo), 21:00 (Apophis) and 22:30 CET (mine).

## Advice and Suggestions

What we decided and did, in plain words:

- The fleet's shared purse now holds 365,079 cr. I moved the money above 50,000 cr a ship into it, as you
  said (46 ships gave, 4 were in a fight and could not). Logistics builds the Recruitment Desk from it this
  evening: our faction's member limit then rises from 50 to 100, and the new seats go to miners.
- The 20 sentinels now belong to Military, as you said. Apophis plans them from his turn at 21:00 CET.
- Five requests of the Admirals were built and answered: the escort can now follow a ship on a circuit;
  money moved into the treasury no longer shows as a route's loss; the automatic filler no longer puts work in
  front of guard ships, no longer sells goods we keep for building, and leaves routes another division claimed.

What I advise you to look at: the fleet still burns a little more fuel than it earns in an ordinary hour
(-27,458 cr an hour over 6 hours); the one-time mission rewards carry the wallets and they will end. The
Admirals' work this evening is to find buyers that last. The station's headline counts only the wallets, not
the treasury, so a deposit looks like money gone: that change is not built yet (open build Q69 (1), with the sweep script).

A step that is yours: Logistics found a station core on offer for 15,000,000 cr (a station of our own would
cost about 20,000,000 cr this way). My recommendation: not now. We hold about 10.5 million cr in all and earn
below zero steadily; we revisit it when the steady money is positive. Until you say otherwise, nobody buys it.

## Learnings

From my learning capture of this turn:

- **A tool that writes every division's plan breaks each division's own rule until that rule is one of its
  inputs.** Record: three Admirals asked in one day for the filler to stop breaking a rule of theirs, each after
  the harm (requests ENT-213 the reserve, ENT-233 goods held back, ENT-236 guard posts and claims). What I do
  differently: when a division sets a rule about its ships or goods, I check the same turn whether the filler
  reads it. Kept as an unpromoted entry in my `LEARNINGS.md`. For the Admirals: name such a rule in your
  report's Suggestions the turn you set it.
- **Lending a role to another division is one install and one plan pass, and the tests know the role too.**
  Record: the first try of the sentinels' move failed 14 unit tests, because the tests used the command group
  as their example of a division with two roles; changing those fixtures took 25 minutes and the move went in
  (commits c531471, e0b7403). What I do differently: grep the tests for a role before moving it. Kept in my
  skill collective-agents. For Apophis: with two roles, `fill.py add` and `drop` ask for `--role`.
- **The game refuses a credit gift from a ship in a fight.** Record: 4 of 49 gifts of the sweep answered
  `in_battle` (18:00 to 18:20 UTC). The sweep script skips such ships and takes them at a later pass. Kept in my
  skill fleet-ops, its faction reference.
- Confirmed, not new: an hour with many gifts reads the gifts as costs until the receiver's wallet is read
  again (the last hour's -148,544 cr); the six-hour figure is the one to tell (knowledge/money-figures.md).

No knowledge file was created or changed; open question: how far the dispatcher should go in starting a group
hunt by itself before Military's test shows what the game does.

Skill: collective-agents changed -- the pass of lending a role to another division
Skill: fleet-ops changed -- a gift refused in a fight; a sweep's pace and its hour of figures

## Cross-links

- `reports/2026-11-17_unity_pirate-gate-treasury-filled-kit-at-base-price.md` -- my previous report
- `reports/2026-11-17_zero_waiting-miners-to-deep-core-achernar-silicon-test.md` -- Mining
- `reports/2026-11-17_oracle_survey-step-in-census-exploration-xp-is-per-pilot.md` -- Intel
- `reports/2026-11-17_mercury_collective-provides-six-ships-crystal-craft-off-for-reserve.md` -- Trade
- `reports/2026-11-17_apollo_outpost-kit-route-on-desk-goods-stand-workshop-lifted.md` -- Logistics
- `reports/2026-11-17_apophis_escort-follow-built-far-bids-gone-curd-stored.md` -- Military
- `communications/orders.log` ENT-038, ENT-039 -- the orders of this turn
- `communications/requests.log` ENT-237 to ENT-242 -- my answers
- `communications/queue.log` ENT-173, ENT-176 -- the split with my chat, what changed for every division
- `governance/strategy.md` -- phase 1, income

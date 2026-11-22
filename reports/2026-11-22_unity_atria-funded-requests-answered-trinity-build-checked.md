---
name: atria-funded-requests-answered-trinity-build-checked
id: 20261122T022438Z
tier: report
trigger: session-end
author: Unity
tags: [fleet, atria, requests, sweep, orders, trinity]
links:
  - reports/2026-11-21_unity_cut-deposit-booked-sweep-writes-ahead-test-round-ends.md
  - reports/2026-11-21_zero_short-ore-fields-empty-four-far-tests-first-laser-iii.md
  - reports/2026-11-22_oracle_outpost-raid-read-from-the-battle-record-far-work-on-70.md
  - reports/2026-11-22_mercury_far-gaps-sized-from-home-two-far-tests-flying.md
  - reports/2026-11-22_apollo_outpost-repaired-itself-repair-stock-kept-atria-asked-for.md
  - reports/2026-11-22_apophis_weapon-swap-by-route-thermal-test-gate-pass.md
  - governance/system-architecture.md
---

# The Collective -- Atria Funded, Every Request Answered, a New Member's Build Checked

## Situation

This report covers my scheduled turn of 2026-11-22, 01:30 to about
02:40 UTC (02:30 to 03:40 CET), since my report of 2026-11-21 22:10 UTC.
Credits (cr) are the game's money; "steady" money is what repeating work
earns after fuel, and money a mission pays only once per pilot is
counted apart.

The fleet as one purse, read at 02:07 UTC (`hive.py fleet`): 246 ships,
205 at work and 41 docked without work (38 of them traders). Steady net
+4,697 cr an hour over the last hour, +2,674 over six hours and +9,699
over 24 hours; paid once +29,498 in the last hour. Wallets held
10,795,094 cr and the faction treasury (our shared purse) 785,345 cr:
11,580,439 cr in all. No ship was lost. The fill gate (the check that no
ship waits) said HALT for 38 traders, one drone and one sentinel at
02:02 UTC, and PASS for my own command group at 02:05 UTC.

Each division from its Admiral's newest report:

- Mining (Zero, `reports/2026-11-21_zero_...`): 60 of 60 at work; the
  short-ore fields near home ran empty; four far tests and the first
  Mining Laser III fitted.
- Intel (Oracle, `reports/2026-11-22_oracle_...`): the game's battle
  record shows our outpost fell on 2026-11-19 to 16 ships of the Algol
  crew; 70 far systems are now read every 12 hours; one faster hull
  bought as a test.
- Trade (Mercury, `reports/2026-11-22_mercury_...`): far trade gaps
  sized from home, two far buy-and-sell tests flying, 37 traders still
  docked.
- Logistics (Apollo, `reports/2026-11-22_apollo_...`): the outpost
  GSC-0044 repaired itself from its store; its repair stock is now kept
  by route; Atria asked for.
- Military (Apophis, `reports/2026-11-22_apophis_...`): the first
  weapon swap flown by a route, a Plasma Cannon II test started, no ship
  waiting at 01:04 UTC.

Seats: 99 of 100 in the faction (`empire.json`, 02:23 UTC). Our empire's
own skill: 116 of 246 ships hold Voidborn level 1 or more (table
`ship_skills`, 02:08 UTC; 92 a day before).

## Strategy

Suggi's standing orders and goals stand as he set them; this turn changed
none. Standing order S5 (never idle, every ship always kept operating)
came in at 01:20 CET and stood in the orders before the Admirals' turns
read it; rule F37 (a test decides on three independent results, never
on one) came at 01:45 CET. Both are his words, and the code that keeps
them was installed from my chat with him (the fill gate's HALT on a
waiting ship; the filler's tests for up to three ships).

What I decided in this turn, and why:

- Atria, the next outpost on the north road, is funded. The builder
  hauler holds 160,226 cr, above the 155,000 its kit route needs, and
  the treasury pays the founding fee of 100,000 cr. Apollo founds it at
  his turn. Reason: GSC-0044 runs by itself again, the condition I set
  for Atria on 2026-11-18.
- The purse rule, rule F7: Trinity, the Chief Architect you set one
  level above me today (`ROSTER.md`), changed the wallet
  sweep at 02:05 UTC so that working ships keep 30,000 cr instead of
  50,000 (traders and flagships keep 50,000). The rule says the figures
  are mine (Suggi, 2026-11-17), so I judged them on their merits and
  kept them: they move about 2.5 million cr of idle wallet money into
  the treasury (Trinity's dry run), which is what the 200-seat
  Recruitment Center (2,000,000 cr) waits for, and every ship still
  keeps far more than its fuel. I wrote the new lines into F7 and made
  the fleet's tests agree with them (commit 1cefb154; the whole suite
  passed in the clone).
- Strict classes (only traders sell; other divisions give their goods
  to a trader) do not switch on yet: 94 route files still sell for
  another class, 26 of them in plans (`workclass.py sales`, 01:56 UTC),
  ten in my own. The new orders give every Admiral that work first.
- My own proposal, not decided: a way to see who works in the clone
  before a turn builds, so two hands never build the same thing (see
  Learnings).

The strategy file's phase is unchanged: phase 1, income first.

## Divisions

Mining (Zero). Reported the near fields of the ores we lack empty,
lifts on regrown stock lasting under three hours, and seven runs of a
mission into Sargas beside a pirate pack, none lost. His thread holds:
last report he put the short ores first; this one shows them mined out
and the work moved further out. Suggestions: scale tests until Laser III
and tier-2 hulls hold (accepted, his call); a gift's default items should
be the route's sale items (open: his mine routes name their items, which
works now); the pirate stop for circuits (done: it reads every stop and step of a
circuit, requests ENT-329, live since the dispatcher's restart at 02:37
UTC).

Intel (Oracle). Read the battle record that nobody had read for three
days and filed 17 raids on bases. Thread holds: last report named a gang
of about twenty, this one reads sixteen ships of one crew in the
record. Suggestions: a raid alert from the battle list in every briefing
(open: the alert built yesterday reads our facilities, not the battle
list); a ship docked at each base before any pause (accepted, request
ENT-316); a hold that waits for a free ship (open).

Trade (Mercury). Sized far gaps, flew two far tests, and a test looped
18 times in 13 minutes on a buy its wallet could not pay, no credits
lost. Thread breaks on one point: 37 traders docked last report and 38
now. That is his plan's to fix, and the new orders say so under S5.
Suggestions: a road check of pirates for far circuits (in part: the
stops are read now, the road between them is not); a word on S5 for a
class whose routes its books close (given in the orders); the rest after
a refused buy (done, ENT-330, with one difference: a missing ask rests the
route too, 30 minutes); Trade Run
missions for XP (accepted, his plan).

Logistics (Apollo). The outpost repaired itself from its own store; the
reserve gate opened a repair route within the minute. Thread holds: last
report all repair materials sat in storage, this one shows the repair
done. Suggestions: book credits that arrive from outside a run out of
its figure (open: two of his runs of +12,321 and +5,321 cr are not
explained yet); the pause step (accepted); the commit hook checks only
staged route files (done by Trinity's commit).

Military (Apophis). Swapped a weapon by route, started a thermal test,
and flew a fourth group hunt without a kill. Thread holds. Suggestions:
do not judge a hunt that stores its loot by its credits alone (open,
decision Q71); no far test whose sale station is as far as its herd
(open); one weapon bought for the division once its tests hold three
results each (accepted in principle; the purse decides then).

## Plans

Next turns, in CET: Zero 04:00, Oracle 04:15, Mercury 04:30, Apollo 04:45,
Apophis 05:00, my own 06:30. The orders of this turn (`orders.log`
ENT-061) say for each:

- Zero mines what the reserve lacks, then what buyers pay for, and turns
  the sales left in his plan into gifts to Trade's receivers.
- Mercury gets every trader operating under S5: training, carrying the
  fleet's surplus to far buyers or flying the missions that pay their
  skills, instead of docking; and he prepares the sell routes that take
  what other divisions give his receivers.
- Apollo founds Atria and keeps both outposts' bunkers and repair stock
  by route; the Recruitment Center when the treasury holds its fee.
- Apophis keeps hunting and fitting toward a group hunt that kills;
  pirates stay his call, a test first.
- Oracle reads the north road and its choke point, explores further out
  and turns his plan's remaining sales into gifts.

My own next steps:

- Make the dispatcher fast again: the new rest check reads every one of
  the 22,788 run rows for each pilot and route, and a pass now comes
  about every 52 seconds against 43 before
  (`services/dispatch/service.log`, 00:54 and 02:37 UTC). An index read
  once per pass is built in my scratch, not installed.
- Switch strict classes on once no plan holds another class's sale.
- Add the base docking step to the pause procedure (ENT-316).
- Install the gift-answer check (`wallet.py`, built and tested in my
  scratch, not installed) on top of Trinity's version of the file.
- Turn my command group's ten selling hunts into gifts.

## Advice and Suggestions

What the players decided and why: Atria is paid for because our first
outpost runs by itself again; working ships keep 30,000 cr instead of
50,000 so that the money for 200 faction seats reaches the treasury;
strict classes wait until every division has turned its sales into gifts,
so that no ship is left without work when the switch goes on.

What I advise you to look at:

- Trinity, the Chief Architect one level above me (your word of today,
  `ROSTER.md`), changed more than the station page this hour: the
  dispatcher, the wallet sweep, the store, the commit hook and the five
  Admirals' turn instructions (now "act directly within your division's
  mandate; ask Unity only for cross-division conflicts, rule or budget
  exceptions or strategy"). It also shortened the shared skills and the
  report template at 02:27 UTC (queue ENT-209). The changes I checked
  hold up, and I kept them. One did not pass the fleet's full test
  suite: four tests of the sweep failed on the new lines; I fixed the
  tests this turn. Its builds and mine touched the same files at the
  same hour; I propose that a build names its files in the queue log
  before it starts, so that two hands never build the same fix.
- Your word alone: no new pilot, war or word to another player is
  pending this turn.

## Learnings

What this turn taught me about leading the fleet, from my learning
capture:

- Another hand can be building in the shared files while my turn runs.
  This turn I built two fixes that Trinity was building at the same
  time, and I first took its work for my own chat with you. Record: the
  clone's uncommitted edits of 01:43 and 01:49 UTC, Trinity's commit
  c067c15f at 02:05 UTC, my queue note ENT-207. The same lesson stood
  in my list since 2026-11-17 and was never a step, so it came back.
  Now it is a step of my skill collective-docs ("A build in flight"):
  read the clone's state and log first, take whose work it is from its
  commit, never guess. Kept in LEARNINGS.md (the sessions entry).
- A gift whose call times out has usually landed. Two of my six gifts
  for Atria timed out after 90 seconds; both wallets had moved when I
  read them twenty seconds later, so I booked them and gave nothing
  twice. The game's own answer to a gift carries the giver's wallet
  after it, which is proof before the fleet file catches up; that check
  is built and tested, not installed. Confirms knowledge/money-figures.md.
- A change that passes its own tests can still break the fleet's: the
  new sweep passed its author's tests and failed four older ones that
  encoded the old line. The full suite before an install is the gate,
  and it caught this only because I ran it on a copy of the clone.
- My own install looked like a build left behind: it copies files into
  the clone and runs the suite there for about eight minutes, and in
  that window a session committing as Unity committed my files with the
  note "left uncommitted by the turn of 01:30 UTC" (1cefb154, 6319b368).
  The suite passed and the content is the same, so no harm; the fix I
  propose is to run the long suite on the scratch tree and only the
  short gates in the clone. Open, for my next build turn.

Skill: collective-docs changed -- the pitfall "A build in flight".

## Cross-links

- `reports/2026-11-21_unity_cut-deposit-booked-sweep-writes-ahead-test-round-ends.md`: my previous report.
- `reports/2026-11-21_zero_short-ore-fields-empty-four-far-tests-first-laser-iii.md`: Mining.
- `reports/2026-11-22_oracle_outpost-raid-read-from-the-battle-record-far-work-on-70.md`: Intel.
- `reports/2026-11-22_mercury_far-gaps-sized-from-home-two-far-tests-flying.md`: Trade.
- `reports/2026-11-22_apollo_outpost-repaired-itself-repair-stock-kept-atria-asked-for.md`: Logistics.
- `reports/2026-11-22_apophis_weapon-swap-by-route-thermal-test-gate-pass.md`: Military.
- `governance/system-architecture.md`: Trinity's system blueprint, read by its headings.
- `communications/orders.log` ENT-061: the orders of this turn.

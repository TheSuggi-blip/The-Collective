---
name: pirate-gate-treasury-filled-kit-at-base-price
id: 20261117T140449Z
tier: report
trigger: session-end
author: Unity
tags: [fleet, faction, outpost, pirates, fill, requests]
links:
  - reports/2026-11-17_unity_lockbox-at-the-experiment-outpost-site-chosen-cap-is-twenty.md
  - reports/2026-11-17_zero_gold-given-liminal-ordered-class-card-deep-core-test.md
  - reports/2026-11-17_oracle_far-explorers-five-directions-outpost-watch-first-survey.md
  - reports/2026-11-17_mercury_waiting-traders-put-to-crafting-trade-net-above-zero.md
  - reports/2026-11-17_apophis_hunts-in-the-black-ember-glands-to-hex-star-d9-kept.md
  - reports/2026-11-17_apollo_hiring-board-built-kit-price-doubled-piping-craft.md
---

# The Collective -- Pirate Places Closed by the Dispatcher, the Treasury Filled for the Outpost, the Kit Bought at Its Base Price

## Situation

Period: from my report of 10:41 UTC
(`reports/2026-11-17_unity_lockbox-at-the-experiment-outpost-site-chosen-cap-is-twenty.md`)
to the end of my scheduled turn of 13:30 to about 14:10 UTC on 2026-11-17. The Admirals
flew one turn each in it, 11:00 to 12:45 UTC, under orders ENT-036; this turn wrote ENT-037.

The fleet in figures (`hive.py fleet`, read 14:04 UTC): 246 ships, credits 10,045,429.
Steady money, the rewards paid once left out: net +11,325 cr in the last hour (income 92,851,
costs 81,526) and +35,969 cr an hour over six hours; over 24 hours -12,792 an hour (read
13:47 UTC). Paid once in the last hour: -168,223, nearly all of it the 200,000 cr I put into
the faction's treasury (booked as money the Collective keeps, not as a cost). Ships at work:
229 of 246 by the fill gate at 14:04 UTC, 14 waiting (10 haulers, 4 traders), 3 held by my
joining script.

Per division, the last hour (`hive.py fleet`, 14:04 UTC) and each Admiral's newest report:

| Division | Ships | At work | Net per hour | Its report says |
|---|---|---|---|---|
| Command | 26 | 26 | +39,521 | (mine) |
| Military | 50 | 49 | +21,323 | the hunts earn: +64,507 cr over 3.9 hours, glands kept for a far bid |
| Logistics | 40 | 29 | -3,191 | the Hiring Board stands; the outpost kit's price doubled |
| Mining | 60 | 60 | -14,135 | gold given, one Liminal ordered, Class Card, a mining-mission test |
| Trade | 40 | 36 | -11,439 | 33 waiting traders put to crafting; one hour above zero (+1,819 at 11:55 UTC) |
| Intel | 30 | 29 | -20,753 | ten far explorers in five directions; GSC-0044 watched hourly |

Voidborn Mastery, our empire's own skill (rule F35; table `ship_skills`, 13:42 UTC): 14 ships
at level 1, 222 at level 0. The chain stands at The Collective Provides, which Trade now tests
at the nickel of Rotanev. Piloting medians are 7 in every division; tier-2 hulls open at 10,
36 to 54 hours away at today's rates (`hive.py levels`).

## Strategy

The strategy in force is phase 1, income (`governance/strategy.md`), under Suggi's standing
orders S1 to S4 and goals G1 to G4, carried word for word into ENT-037. Nothing of his changed
in the period; no word of his came in it.

What the record of the period says about phase 1: the fleet's best work is still selling into
deep orders that come and go. The two water-ice drains measured 45,333 and 38,951 cr per
ship-hour over the last four hours (`route_earnings`) and fly no ship now, because the deep
order at Central Nexus left at 11:11 UTC (Mining's report); Mining's steady net was +125,601
in the hour to 11:00 UTC and is -14,135 now. Most ships meanwhile do standing work, gathering
into the reserve at -200 to -300 cr a ship-hour (gather-schedar-belt -292, Ironhollow -217).
So the fleet earns in waves. Two things lift the floor between waves: more stations bought
from (Military's ember glands bid 3,919 cr at Hex Star against 480 at home), and crafting what
the reserve lacks from goods nobody bids for (Trade's and Logistics' piping routes, about
break-even and training the class skill).

What I decided in the period, inside the orders:

- The Outpost Kit is bought at up to 150,000 cr. The two at 74,010 cr were gone within two
  hours; the one on offer asks 148,663, about the catalog's 150,000. Waiting for a bargain costs
  the outpost's days and every route that would start from it (requests ENT-227).
- The game spends the faction's treasury on any faction fee it holds whole (the Hiring Board's
  75,000 left the treasury, not the builder's wallet). So I now place every fee: I filled the
  treasury from 6,903 to 206,903 cr (nine wallets above 40,000 gave, each gift booked); it pays
  the outpost's founding fee and about seven days of rent.
- Suggi's order to avoid pirates (D9) is now kept by the dispatcher itself: a hunt, a mine or a
  guard where our readings saw a pirate within six hours does not start. At 13:57 UTC that
  closed nine routes in twelve systems.
- The members ladder: the haulers join up to the Hiring Board's cap of 50 (38 at 14:00 UTC,
  by script).

## Divisions

**Mining (Zero,** `reports/2026-11-17_zero_gold-given-liminal-ordered-class-card-deep-core-test.md`**).**
Gave the 90 gold for the boards, wrote the Class Card, ordered one Liminal for 58,881 cr, and
started the first mining-mission test. Its thread holds: the iron goal of its last report
(above 330,000) is met at 344,892, and its credit fall of 182,077 is explained by 314,823 cr of
gifts to the builder, which `gifts.jsonl` shows. Its three tests that sold reserve ores were a
fault of my tool, now fixed (ENT-212, ENT-213 done). Suggestions: a hull bought for a test
booked as paid once, accepted, not built (open builds). A lift on every dispatcher pass: open;
I have not checked whether the five-minute pass writes lifts, and read it at my next turn.

**Intel (Oracle,** `reports/2026-11-17_oracle_far-explorers-five-directions-outpost-watch-first-survey.md`**).**
Five far census routes by direction, 73 systems read for the first time, GSC-0044 watched
hourly, the first survey read. Thread: of the 97 unread systems of its last turn, 72 were read
(goal 40 met); the exploration median stayed at 2 against a goal of 3, which it says plainly.
Suggestions: caustic sac goes to the reserve first (rule F24): accepted; my command hunts at
Alathfar stop selling sacs at my next turn. A check in `routes.py` for census routes that share
a system: accepted, open. `plan.py template` to refuse in one line while routes are
uncommitted: accepted, open.

**Trade (Mercury,** `reports/2026-11-17_mercury_waiting-traders-put-to-crafting-trade-net-above-zero.md`**).**
Put 33 waiting traders to crafting and selling; crafting XP went from 0 to 3,490 in four hours.
Thread holds for its own figures, but its hour above zero did not last: Trade reads -11,439 in
the hour to 14:04 UTC, and 4 traders wait now with nothing open. Suggestions: lift only a route
that has flown, built (ENT-216 done). A script to pool scattered lead ore (about 33,000 cr):
declined for now; small beside the work, and it crosses every division's ships. The forecast
bounded by bids: open (Q68).

**Logistics (Apollo,** `reports/2026-11-17_apollo_hiring-board-built-kit-price-doubled-piping-craft.md`**).**
Built the Hiring Board, wrote `build.py` with a treasury guard, set haulers crafting piping from
stored plate at no cost. Thread holds: the board its last report planned stands. Its report
named my order's error: ENT-036 said the fee comes from the builder's wallet, and the game took
it from the treasury (errors.log ENT-086). Suggestions: size the treasury for fees too, done;
buy the kit at up to 150,000, accepted (ENT-227); book a gift when it lands, half built (ENT-228).
Now 10 haulers wait: the home fields stand at their floors and Ironhollow carries 52 gatherers
already; four tests stand open for Apollo to take at 15:45 UTC.

**Military (Apophis,** `reports/2026-11-17_apophis_hunts-in-the-black-ember-glands-to-hex-star-d9-kept.md`**).**
The hunts turned the division positive (+64,507 cr over 3.9 hours; +21,323 in the last hour by
my reading, which agrees). Thread holds: the `alone` rule of its last turn cut no-kill runs from
44 to 13 percent with no shot fired. Suggestions: the pirate gate, built (1586add); no reserve
sale from the filler, built; one buyer at Hex Star for two divisions, accepted, my command hunts
store glands when that bid is thin, at my next turn; buying ferrous nodule for 1.3 million cr,
declined: the money goes to the outpost and the members ladder first.

No two reports contradict each other.

## Plans

Each division, inside ENT-037:

- **Logistics** buys the kit at up to 150,000 cr and founds the outpost at GSC-0044, the fee
  from the treasury; then the fuel test into its bunker; then the Recruitment Desk's 100 boards.
- **Mining** switches its pilot into the Liminal and reads its runs, reads the Deep Core test,
  and plans five gather routes around the outpost once its base id is known.
- **Military** guards the kit's road and the outpost, and builds guard.py's `--follow` step
  for an escort (ENT-226).
- **Trade** reads its new gather and mission routes and keeps the floors of its sell routes
  beside the deepest ask.
- **Intel** reads the far routes' first rows (the farthest system in each direction) and
  keeps the outpost site watched.

Mine, at my turn of 18:30 CET (17:30 UTC), in this order: the dispatcher's half of the escort
(a guard that follows a circuit); a run's figure that takes in a gift booked just before its
start (ENT-220); the command hunts store caustic sacs and keep glands for the far bid; then the
rest of Q67 (what each Lockbox holds as a table, the outpost's place and base id, the visit
step for survey missions) and Q68. The members: the joining script ends at the cap of 50; the
Recruitment Desk (300,000 cr) is placed when its boards stand.

The fill gate's last lines at 14:04 UTC: command, drone, miner, scout and sentinel PASS. Hauler
HALT, 10 waiting: the home gather fields stand at their floors, Ironhollow already carries 52
gatherers against the 45 the orders name, and four tests stand open that only Apollo may give
his ships. Trader HALT, 4 waiting, nothing open to them. Both are their Admirals' plans, at
their turns of 15:30 and 15:45 UTC; I lifted nothing further, since that would crowd a field.

## Advice and Suggestions

In plain words, Suggi, what we decided and why:

- **We pay full price for the outpost's kit.** The cheap kits were bought by someone else
  within two hours. The full price (about 150,000 credits) is what the game itself says the kit
  is worth, and every day without the outpost is a day without its storage and fuel stop.
- **The faction's shared purse pays building fees by itself.** We learned that the game takes
  a building fee from the faction's shared purse whenever it holds enough. So I keep that purse
  filled on purpose: it now holds about 207,000 credits, enough for the outpost and a week of
  rent for our three offices.
- **Pirate avoidance is now automatic.** Your order to stay away from pirates was kept only by
  each ship's own retreat rule for five hours; now no ship starts work where pirates were seen
  in the last six hours.

What I advise you to look at: the fleet's money comes in waves. When a big buyer appears
(a large ice order), the fleet earns over 100,000 credits an hour; between waves most ships do
gathering work that costs a little fuel and fills our stores. The steady average over six
hours is about +36,000 credits an hour.

Nothing is waiting for your decision. The steps that stay yours (a new pilot, war or any word
to another player) were not needed this turn.

## Learnings

- **An order that limits ships becomes a check in the same turn.** Record: orders D9 (about
  08:41 UTC) stood in no check for five hours; a hunt flew four runs into a pirate place
  (Military's report) and seven routes of my own plans still lay in such systems at 13:52 UTC.
  The filler broke the reserve rule and the one-ship test rule in three divisions in one round
  (requests ENT-212, ENT-213, ENT-216). What I do differently: a rule or order that limits what
  ships do goes into the dispatcher's rule or the filler with a failing test first, then into
  the orders. Kept in `knowledge/fleet-employment.md` (the filler's eight stops) and the skill
  collective-agents. For the Admirals: a rule a script does not check is broken between turns.
- **The game spends the treasury on a fee it holds whole.** Record: errors.log ENT-086 (82,999 to
  7,723 cr at 12:19 UTC, the wallet unchanged). My order had named the wallet from one build
  seen: a repeat of "a mechanism seen once". What I do differently: an order that names a purse
  quotes the command's help. Kept: unpromoted (`LEARNINGS.md`) and the faction reference of my
  skill fleet-ops.
- Confirmed, not new: a price in the orders goes stale within hours (the kit), so a route's
  ceiling carries the allocation.

Skill: fleet-ops changed -- the purse rule and how the treasury is filled (references/faction.md)
Skill: collective-agents changed -- an order that limits ships becomes a check the same turn

## Cross-links

- `reports/2026-11-17_unity_lockbox-at-the-experiment-outpost-site-chosen-cap-is-twenty.md` -- my previous report
- `reports/2026-11-17_zero_gold-given-liminal-ordered-class-card-deep-core-test.md` -- Mining
- `reports/2026-11-17_oracle_far-explorers-five-directions-outpost-watch-first-survey.md` -- Intel
- `reports/2026-11-17_mercury_waiting-traders-put-to-crafting-trade-net-above-zero.md` -- Trade
- `reports/2026-11-17_apollo_hiring-board-built-kit-price-doubled-piping-craft.md` -- Logistics
- `reports/2026-11-17_apophis_hunts-in-the-black-ember-glands-to-hex-star-d9-kept.md` -- Military
- `communications/orders.log` ENT-037 -- the orders written in this turn
- `communications/requests.log` ENT-222 to ENT-229 -- my answers
- `communications/queue.log` ENT-164 -- what changed for every division
- `governance/strategy.md` -- phase 1, income

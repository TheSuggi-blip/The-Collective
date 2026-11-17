---
name: claim-check-several-donors-park-in-gate-three-sites
id: 20261117T015914Z
tier: report
trigger: session-end
author: Unity
tags: [fleet, requests, tools, money, sites, levels]
links:
  - reports/2026-11-16_unity_standing-goals-admirals-log-feedback-money-figures-mended.md
  - reports/2026-11-16_zero_every-miner-on-templates-iron-beyond-the-border.md
  - reports/2026-11-16_oracle_explorers-on-the-roads-every-scout-on-templates-of-reads.md
  - reports/2026-11-17_mercury_soma-surplus-sold-traders-on-templates-silicon-bought.md
  - reports/2026-11-17_apollo_haulers-on-templates-steel-craft-route-boards-under-way.md
  - reports/2026-11-16_apophis_every-drone-own-routes-hunts-store-station-goods.md
---

# The Collective -- Every Request to the Fleet Admiral Closed, Claims Checked by the Log Itself, Three New Sites on File

## Situation

Period: from my report of 2026-11-16 22:40 UTC
(`reports/2026-11-16_unity_standing-goals-admirals-log-feedback-money-figures-mended.md`)
to this scheduled turn, 2026-11-17 01:30 to about 02:05 UTC. Between the two, the chat
with Suggi wrote orders ENT-021 to ENT-024 (play by scripts, escorts are the Admirals'
call, every ship levels while it works, three more sites); those are the orders in force
(`orders.log` ENT-024).

Fleet, printed by `hive.py fleet` at 01:52 UTC: 246 ships, 240 at work, 6 docked without
work; credits 10,003,228. Steady money (rule F19) in the last hour: net -53,122 cr
(income 13,882, costs 67,004, of it fuel 65,827); over 6 hours -25,750 an hour; over 24
hours +19,447 an hour. Paid once and kept apart: 204,647 cr in the last hour. The
history (`hive.py history`) shows credits rising from 9,847,294 at 00:50 to 9,982,462 at
01:44 UTC (+135,168) while the steady change read -49,804: the rise is rewards the game
pays once, not repeating income.

| Division (Admiral) | Newest report | Its line |
|---|---|---|
| Mining (Zero) | `2026-11-16_zero_every-miner-on-templates-iron-beyond-the-border.md` | 60 miners on templates; iron work moved beyond the border; no silicon field read |
| Intel (Oracle) | `2026-11-16_oracle_explorers-on-the-roads-every-scout-on-templates-of-reads.md` | ten explorers on the roads to the station sites; every scout on a template of reads |
| Trade (Mercury) | `2026-11-17_mercury_soma-surplus-sold-traders-on-templates-silicon-bought.md` | stored soma sold into five bids; 75 silicon ore bought for the boards |
| Logistics (Apollo) | `2026-11-17_apollo_haulers-on-templates-steel-craft-route-boards-under-way.md` | steel plate made by a route; circuit boards under way |
| Military (Apophis) | `2026-11-16_apophis_every-drone-own-routes-hunts-store-station-goods.md` (19:58 UTC) | not reported since: his turn of 00:00 UTC was ended at 01:16 UTC on Suggi's word |

The fill gate (`fill.py check all`) read at 01:55 UTC: 243 at work, 1 waiting; at 01:58
UTC six scouts waited (Intel's plan, Problems of Divisions below). Levels
(`hive.py levels`): the median pilot of every division stands at Piloting 6; hours to
Piloting 10 at the rate since birth: Command 49, Mining 58, Military 61, Logistics 69,
Intel 73, Trade 79.

## Strategy

In force: `governance/strategy.md`, phase 1, income. The bottleneck of this turn is the
same as at my last report: steady money is negative. `hive.py tasks` over four hours
puts it in one table: of 760.8 ship-hours flown, 543.8 were standing work at -176 cr a
ship-hour and 41.7 were census at -625; trade and delivery made 3,485 cr a ship-hour over
142 runs but on 13.1 ship-hours only. The best repeating route with two runs or more
(the scale) is hunt-deepwell-haze-cinder-sylph at 3,854 cr a ship-hour. The paying routes
are thin: methane drain, null matter, soma and plasma each sell into one bid that one
ship empties, and each stood at 0 of 1 ships at 01:58 UTC, closed by an empty store or a
taken bid.

Decided by Suggi in the period (orders ENT-021 to ENT-024, quoted there): the fleet
plays by scripts and a turn sets work up for the hours after it; all of the galaxy is
open and the Admirals judge whether an escort is needed; every ship levels the skills of
its class while it works and earns where it can (T5); Intercrus, Felis and Biham join the
four sites of G3. This turn put the three into `game/map/sites.tsv` (commit 5565dfc).

My recommendation, not decided: steady income comes from buyers that regain, not from
more ships on one-unit bids. `hive.py refill` names the deepest: the water-ice bid at
Central Nexus regained at least 624 units an hour over 29 hours of readings (21,212 cr an
hour at its best price of 34) while our ships took 241 an hour; the methane bids at The
Experiment and Synchrony regain 34 an hour each. A second lead is a buyer without a
seller: `hive.py capacity` reads palladium ore bid at 339 cr for 43,459 units at three
stations, and no field we read holds more than 2 units. I put the first to Mining and the
second to Intel in the orders' next turn, not as a change of orders now. The phase does
not change: the fleet's credits rise on rewards paid once, and those end when every pilot
has flown its missions.

## Divisions

**Mining (Zero).** Reported 60 miners on three templates, Ironhollow lifted to 7 ships
beyond the border and a request for a guard there. Thread: his report of 18:23 UTC planned
own routes per miner, this one shows them grown into templates; his Mining hour of +12,395
cr to 23:35 UTC agrees in sign with the history row of 23:49 UTC (+73,996, methane
drained). Answers: `requires.hold` -- accepted and built (install of 00:17 UTC, d8b1edb).
Shared caps -- accepted in part: fill.py lifts shared standing work in home space as far
as its field carries (Hamal now 120), and the new claim check leaves standing work shared.
Silicon over iron -- accepted, Intel's explorers look for it. Carbon -- Trade's call, as he
says.

**Intel (Oracle).** Reported ten explorers on the roads and disjoint census lists. Thread:
his turn of 18:23 UTC wrote no report (plan-lock fault, fixed in 7d7acd3); this report
names the orphaned route that turn left and his fix. At 01:58 UTC six scouts waited: every
census list read fresh and the shared fields full (requests.log ENT-188). Answers: a census
that reads the next unread system before it turns home -- accepted, his to build through
`fleet-build.sh` with one ship first. census-guard-ice under its hour -- Military's to
weigh, passed on. Ten ships on census-roads -- accepted: each system is read by one ship,
which is the one-ship test rule F13 asks for.

**Trade (Mercury).** Reported soma sold for about 4,200 cr, a focused-crystal craft (+278
cr a run) and a trader left at 298 cr by a hand buy (errors.log ENT-067). Answers: partial
gifts -- done (4712300, ENT-186). A sell route per surplus good written by a script --
accepted, his to build. A sell route's forecast on its bid's regain -- accepted, mine,
not built this turn. His runs that no route explains (navigation loops +3,121) match my
own reading of park below.

**Logistics (Apollo).** Reported no board made, a driver left running, steel plate by a
route. Thread break with Trade: Mercury's note admirals.log ENT-005 says 75 silicon were
deposited for the board crafter at 00:01 UTC; Apollo's report of 00:46 UTC counts 32 and
asks Trade for 18 more (ENT-179). The storage book at about 01:53 UTC: that hauler holds 43
silicon at Central Nexus and 32 at Node Beta, and three haulers hold 29 boards. The silicon
for the first 75 boards is on hand. Answers: claim check -- done (fe80e62). Waiting for a
stopping loop in route_run.py -- accepted, his to build as he offered. A freighter test --
accepted inside rule F12. Feedback: park in the gate -- done (9e62546).

**Military (Apophis).** Not reported since 19:58 UTC. His job's last run reads `cancelled`
(01:16 UTC). The record of the turn: claim ENT-009, the guard route at Ironhollow
(ENT-181), a request to Intel for pirate readings (ENT-182), errors.log ENT-068.

## Plans

The Admirals' next turns, by schedule (CET): Zero 04:00, Oracle 04:15, Mercury 04:30,
Apollo 04:45, Apophis 05:00; mine at 06:30. Each works under orders ENT-024, which this
turn leaves unchanged: T4 (play by scripts) and T5 (level while working) are new to every
Admiral and taken at their next turn.

- Mining: the water-ice bid at Central Nexus regains more than we take; Zero weighs more
  ships on the ice routes against what that bid regains.
- Intel: standing work for scouts whose reads are fresh (ENT-188); the roads to the seven
  sites; a palladium or silicon field.
- Trade: the soma bids' regain read before the routes are lifted; the sell-route
  generator.
- Logistics: 75 boards from the silicon on hand; the lockbox step when plate and boards
  are held (P5).
- Military: the pirate test of orders ENT-024, by script, and the report he could not
  write.

Mine, before the Admirals' slots where I can, else in my turn of 06:30 CET:

1. The park route measured +1,136 cr a ship-hour over 91 runs in four hours: a wallet
   movement no record names. Find it (a mission paid on docking is my first suspect, not
   verified) and give it a record, as the gifts and the tax have.
2. The briefing prints each member's forecast SUM line before its turn (Mercury, Oracle)
   and a short form (Apollo).
3. A fleet-wide fallback: shared standing routes with room join every plan's list Then
   by the five-minute job, behind a switch, after a dry run on live data.
4. The game published 0.723.0 today; the catalog on file is 0.721.1. The hourly refresh
   fetches it; I read that it did.
5. station/ stays with the chat session this hour (queue.log ENT-134).

## Open Questions

1. **How the money is shown to you.** You asked in the chat why the credits rise while the
   divisions show losses. The figures of this turn: credits +135,168 in the hour to 01:44
   UTC, steady -49,804, rewards paid once 267,300 booked in the last hour. Both are true:
   the rise is one-time money. Options: (a) keep rule F19 as it is and show only steady
   money per division; (b) show beside it "all money per hour", one-time included, so the
   rise is visible where you look. My recommendation: (b), with steady money still the
   measure of a route. The chat session is working on this with you; what you decide
   there is built there.
2. **The first site to read.** Seven sites stand in `game/map/sites.tsv`; none is read
   yet except a census of Intercrus and Felis on 2026-11-15. Nothing is yours to decide
   until both roads are read (P4 d); I tell you before any founding.
3. Nothing else is asked: no new pilot, no word to another player and no paid faction
   step was weighed in this turn.

## Learnings

From my learning capture of this turn:

- **Two of my sessions in one hour split the files first.** Suggi asked to change the
  station while my turn ran; the turn took the scripts and the requests and wrote the
  split into `queue.log` ENT-134 before its first build. Record: ENT-134, commits fe80e62,
  4712300, 9e62546. Kept unpromoted in `LEARNINGS.md`. For the Admirals: a turn that
  overlaps another member's names what it touches, as the claims now do.
- **A rule two members race on lives in the command both pass.** The claim of
  admirals.log ENT-006 named routes claimed three minutes before; the check now runs
  under the log's lock (fe80e62). Confirmed of what the skill collective-agents says.
- **A figure built on wallets is wrong by every movement without a record.** Park, which
  earns nothing, measured +1,136 cr a ship-hour (route_earnings, 91 runs); Mercury's
  report names three more. Confirmed of `knowledge/money-figures.md`; the cause is open.
- **A note is not read by the member it names.** Trade's ENT-005 told Logistics of 75
  silicon; Logistics asked for 18 more 40 minutes later. For every Admiral: read the
  holdings table before you ask for goods.

Skill: fleet-ops changed -- the wallet guard now reads the receiver after a gift and gives
from several donors.

## Cross-links

- `reports/2026-11-16_unity_standing-goals-admirals-log-feedback-money-figures-mended.md` -- my previous report.
- `reports/2026-11-16_zero_every-miner-on-templates-iron-beyond-the-border.md` -- Mining.
- `reports/2026-11-16_oracle_explorers-on-the-roads-every-scout-on-templates-of-reads.md` -- Intel.
- `reports/2026-11-17_mercury_soma-surplus-sold-traders-on-templates-silicon-bought.md` -- Trade.
- `reports/2026-11-17_apollo_haulers-on-templates-steel-craft-route-boards-under-way.md` -- Logistics.
- `reports/2026-11-16_apophis_every-drone-own-routes-hunts-store-station-goods.md` -- Military, the last report.
- `communications/orders.log` ENT-024 -- the orders in force; `communications/requests.log` ENT-185 to ENT-188.
- `game/map/sites.tsv` -- the sites, three added this turn.

---
name: lockbox-at-the-experiment-outpost-site-chosen-cap-is-twenty
id: 20261117T103855Z
tier: report
trigger: session-end
author: Unity
tags: [fleet, faction, outpost, lockbox, members, orders]
links:
  - reports/2026-11-17_unity_shared-storage-built-no-ship-waits-station-round-two.md
  - reports/2026-11-17_zero_iron-floors-judged-garnet-named-liminal-found.md
  - reports/2026-11-17_oracle_explorers-on-97-unread-systems-garnet-named-survey-test.md
  - reports/2026-11-17_mercury_palladium-routes-crafting-before-gathering-class-card.md
  - reports/2026-11-17_apophis_hunts-reopened-alone-pirates-melt-standing-class-card.md
  - reports/2026-11-17_apollo_builder-chosen-lockbox-goods-at-the-experiment-outpost-planned.md
---

# The Collective -- The Second Lockbox Stands, the First Outpost's Site Is Chosen, and the Faction Is Full at 20

## Situation

Period: from my report of 2026-11-17 06:27 UTC
(`reports/2026-11-17_unity_shared-storage-built-no-ship-waits-station-round-two.md`)
to the end of this scheduled turn, 09:30 to about 10:50 UTC. Orders in
force at the start: `communications/orders.log` ENT-034; at the end
ENT-036.

The fleet at 10:35 UTC (`hive.py fleet`): 246 ships, 243 at work, and
10,086,168 cr in the wallets. Steady money is what repeats (sales, fuel),
without the rewards the game pays once per pilot:

| Window | Income per hour | Costs per hour | Net per hour |
|---|---|---|---|
| Last hour | 213,293 | 69,318 | +143,975 |
| Last 6 hours | 61,319 | 61,569 | -250 |
| Last 24 hours | 35,369 | 47,814 | -12,445 |

The last hour is high because miners and the command group sold ice
out of storage into the stations' standing bids; the six hours are the
fairer picture: the fleet now breaks even. The fill gate (the check that
no ship waits) read HALT at 10:39 UTC: 238 at work, 8 waiting (4
traders, 2 haulers, 2 scouts), every one because the home gather fields
stand at their floors.

One line per division, from its Admiral's newest report:

- Mining (`reports/2026-11-17_zero_iron-floors-judged-garnet-named-liminal-found.md`):
  60 of 60 at work; floors set by the game's regrowth; 54,470 ore in four
  hours; net -13,544 cr an hour at 07:16 UTC.
- Intel (`reports/2026-11-17_oracle_explorers-on-97-unread-systems-garnet-named-survey-test.md`):
  30 of 30; explorers back on 97 never-read systems; a survey test set up.
- Trade (`reports/2026-11-17_mercury_palladium-routes-crafting-before-gathering-class-card.md`):
  40 of 40; three sell routes; net -5,941 cr an hour against a goal of -2,000.
- Military (`reports/2026-11-17_apophis_hunts-reopened-alone-pirates-melt-standing-class-card.md`):
  50 of 50; the rule that closed 61 of 161 hunts loosened; no ship lost.
- Logistics (`reports/2026-11-17_apollo_builder-chosen-lockbox-goods-at-the-experiment-outpost-planned.md`):
  40 of 40; the builder chosen and the Lockbox's goods in place by 09:30 UTC.

## Strategy

The strategy is `governance/strategy.md`: phase 1, income first. Suggi's
standing orders and goals stand unchanged at the head of every orders
entry. The bottleneck of this period was not ships or skills but two
things we hold: storage near the border, and members in the faction.

What Suggi decided in the period (in my chat with him this morning,
written into the rulebook by that chat): every mission a board offers is
flown when it pays more than it costs (rule F34), and every pilot flies
our own empire's missions to the end of each chain, because only they
train the empire's skill, Voidborn Mastery (rule F35). Orders ENT-035
made them direction D10 and task 2 for every Admiral. Today 11 ships hold
level 1 of that skill and 225 level 0 (table `ship_skills`, 10:34 UTC).

What I decided in this turn, inside the orders:

1. **The second Faction Lockbox** (a shared storage room of the faction
   at a station) stands at The Experiment Research Station. Logistics'
   builder, a hauler, joined the faction and got a role I created for
   it, Builder: it may build and manage facilities, nothing else (no
   treasury, no invites). It built at 09:45 UTC with its own 200 steel
   plate and 50 circuit boards and a fee of 200,000 cr; active at 09:58 UTC.
2. **The first outpost goes to GSC-0044**, three systems beyond our
   border and three jumps from The Experiment, with two untouched belts
   of iron and copper, lanes east toward Intercrus and Diadem, and no
   pirate on our record in it or next to it. Mining and Logistics named
   it; Intel and Military named Garnet, which is only two systems out
   where rule F33 asks three or four. The builder holds 174,940 cr for
   the kit and the fee; Logistics builds it.
3. **The faction's cap is 20, not 50.** The 21st join was refused. The
   field we had read as the cap is the size of a page of the member
   list. The next step is the Hiring Board (cap 50): 75,000 cr, 75 steel
   plate and 25 circuit boards, which we hold.

## Divisions

**Mining (Zero).** Its thread holds: the floors it planned at 03:31 UTC
are set by the game's regrowth rule in the report of 07:27 UTC, and its
storage gains (+7,062 iron an hour) agree with the reserve's figures.
Its suggestions: a Lockbox at The Experiment -- accepted, built; GSC-0044
under rule F33 -- accepted, chosen; one Liminal (a tier-1 mining hull
that asks no Piloting) tested -- accepted, in its block. Its request
ENT-206 (gifts bending run figures) is answered in ENT-210: run figures
already leave out every booked gift; what still bends Schedar is two runs
with losses no record names.

**Intel (Oracle).** Thread holds: it widened the explorers' list and
added a gate (ROADS) after the list ran dry twice -- a fix that fires by
itself. Suggestions: an outpost beyond Pherkad for scout fuel -- open,
the second outpost once the first stands; Garnet -- declined for rule
F33 (GSC-0044 lies two jumps from Garnet and serves it); fill offering a
test by the species' owner -- accepted, my build; a per-ship XP reading
-- accepted, Trade's `xpsnap.py` exists, a verb of `hive.py` is mine to
add.

**Trade (Mercury).** Thread holds on work, not on money: its goal of
-2,000 cr an hour was missed (-5,941), and the last hour read -8,353.
The cause it names is right: thin bids that come and go. Suggestions:
bound a sell route's hour by what its bid regains, not by minutes of
flight -- accepted, my build (the forecast showed +54,942 an hour while
the wallets lost); Homam as a trade hub -- open; buying the kit and fuel
cells -- accepted, the builder holds the credits; boards at Ironlight --
declined, the gold way costs 0 cr (ENT-211).

**Military (Apophis).** Its best work this period: it found that its
safety rule left the hunt whenever any stranger stood near, which closed
61 of 161 hunts, and loosened it by script. Its plan to build a pirate
group was overtaken by Suggi's word at 08:41 UTC (no pirate tests,
ENT-034). Suggestions: Garnet as a hub -- declined (F33), the guard of
GSC-0044 is in its block; one `set_stance.py` for the fleet -- accepted,
open; `comms.py append` refusing a commit hash not on origin/main --
accepted, my build; the briefing naming why a free drone cannot take a
hunt -- accepted, my build.

**Logistics (Apollo).** Thread holds: planned at 08:45 UTC, done at 09:45
UTC. Suggestions: GSC-0044 -- accepted; the gold way for the last boards
-- accepted (ENT-211); facility cards as reads in `gate.py` -- done
(commit 19dfa5c).

No two reports contradict each other on facts; they differ on the
outpost's place, and rule F33 settled it.

## Plans

What each division does next (orders ENT-036, read by the Admirals' turns
from 12:00 CET):

- **Mining**: give 90 gold ore into the builder's storage at The
  Experiment for the last circuit boards; plan gather fields around
  GSC-0044; test one Liminal; read where nickel ore grows back for the
  empire mission The Collective Provides. Its block and Task 1 (its
  Class Card, still missing) stand.
- **Intel**: ten explorers far out on the two turns Suggi set; read
  GSC-0044 and its six neighbours before the founding; the Class Card.
- **Trade**: missions that pay once (about 3.7 million cr open, the
  tool `fleet` view capacity); sell the surplus; answer Intel's request
  ENT-208; close its own fill gate, where 4 traders wait.
- **Military**: the guard of GSC-0044 and of the kit's road; no pirate
  work; read the hunts under the loosened rule.
- **Logistics**: found the outpost at GSC-0044 by routes (kit from
  Ironlight Crossroads, fee, `deploy_outpost`); build the Hiring Board
  at Node Beta as soon as 25 boards and 75 plate stand there.

My own next turn (14:30 CET), from `DECISIONS.md` Q67 and this period:
a site set by one command; what each Lockbox holds as a table; the
outpost's place and base id read from the game; the visit step for the
survey missions; the receiver's wallet read after every gift; the
forecast bounded by a bid's regain; the hash check in `comms.py`; the
fill test by species owner. Then the Hiring Board's fee when the
builder's wallet has given the outpost its share.

## Advice and Suggestions

- **What changed for you to see:** two Lockboxes now (Node Beta and The
  Experiment), and the empire page reads 20 of 20 members. The rent of
  both, 138 cr every 100 game ticks or about 11,900 cr a day, comes from
  the faction's treasury, which five members filled to 83,827 cr (about
  seven days).
- **The member figure was wrong for a day** and is fixed at its root:
  the script now computes the cap from our recruitment offices. No
  credits were lost; we had only planned on joins that did not exist.
- **The money**: the fleet broke even over six hours; the last hour's
  +143,975 cr is ice sold from storage, which ends when the stores do.
  The steady earner is still missing; Trade's and Military's figures are
  the ones to watch.
- **Eight ships waited** at the end of my turn because the home gather
  fields are at their floors. Their Admirals' turns of the next hour
  close it; the outpost at GSC-0044 will open new fields.
- Nothing waits on you: no new pilot, no word to another player, no war.

## Learnings

From this turn's learning capture:

- **A number from the game is planned on by what its field means.** The
  faction's `members_limit` read 50 and went into the orders, my blueprint
  and four scripts; it is a page size, and the cap is 20 (errors.log
  ENT-081). I now read the command's help for every number the orders
  rest on, and a difference from the game's rule (the guide's 20) is a
  question first. Kept: unpromoted, `LEARNINGS.md`. For the Admirals:
  the same holds for every field of an order book or a card.
- **A member builds when the leader gives it a role.** The game's
  custom roles let a hauler build without any other power; one build
  raised its Corporation Management from 0 to 3, which opens the next
  offices. Kept in my skill `fleet-ops` (`references/faction.md`).
- **A live run's order file is its lock.** I deleted one to free my
  flagship; the plan saw the herd as free and sent a second ship, and
  the two met in one fight for 35 minutes (no damage). Kept in
  `fleet-ops` and errors.log ENT-081.
- **Confirmed:** a request can already be answered by what exists
  (ENT-206): run figures had left gifts out since 2026-11-16; what
  bends them is a gift nobody recorded (`knowledge/faults-that-leave-no-record.md`).

Skill: fleet-ops changed -- the faction's cap and `members_limit`, a
member builds by a custom role, invites and joins by script, never
delete a live run's lock.

## Cross-links

- `reports/2026-11-17_unity_shared-storage-built-no-ship-waits-station-round-two.md` -- my previous report
- `reports/2026-11-17_zero_iron-floors-judged-garnet-named-liminal-found.md` -- Mining
- `reports/2026-11-17_oracle_explorers-on-97-unread-systems-garnet-named-survey-test.md` -- Intel
- `reports/2026-11-17_mercury_palladium-routes-crafting-before-gathering-class-card.md` -- Trade
- `reports/2026-11-17_apophis_hunts-reopened-alone-pirates-melt-standing-class-card.md` -- Military
- `reports/2026-11-17_apollo_builder-chosen-lockbox-goods-at-the-experiment-outpost-planned.md` -- Logistics
- `governance/empire.md` -- the faction, its offices and the sites, written by `empire.py`
- `game/map/sites.tsv` -- GSC-0044 chosen
- `communications/orders.log` ENT-035, ENT-036 -- the orders of this turn
- `communications/queue.log` ENT-159, ENT-160; `communications/requests.log` ENT-210, ENT-211; `communications/errors.log` ENT-081

---
name: divisions-handed-over-recurring-income-still-negative
id: 20261115T211312Z
tier: report
trigger: order
author: Unity
tags: [fleet, handover, economy, frontier]
links: [reports/2026-11-15_zero_energy-crystal-the-one-mined-good-that-pays.md, reports/2026-11-15_zero_mining-missions-unflown-by-91-pilots-honeyglobe-test.md, reports/2026-11-15_mercury_no-gap-with-depth-control-nodes-pay-two-loads.md, reports/2026-11-15_apollo_stored-ore-unbid-ferrous-slugs-the-way-out.md, reports/2026-11-15_apophis_veil-rays-pay-no-ship-lost.md, reports/2026-11-15_oracle_picture-within-the-hour-never-the-half-hour.md, governance/rulebook.md, game/routes/BLUEPRINT.md]
---

# The Collective -- The divisions are handed to their Admirals; income that repeats is still negative

## Situation

This is the first fleet report. It covers the time from the first
pilot (2026-11-14) to 2026-11-15 21:15 UTC.

The fleet's live file, read through the command station at 21:11 UTC,
shows 146 ships in six divisions: Mining 40, Military 30, Trade 20,
Logistics 20, Intel 20 and my own division Command 16 (six flagships
and ten guards). The wallets hold 4,258,594 cr, 29,168 cr per ship.
The same file books 4,271,798 cr of rewards that the game pays once
per pilot (the starter missions and three mission circuits). The
wallets stand 13,204 cr below that sum: everything the fleet did
again and again has cost more than it earned. The station's own rate
for the last 60 minutes reads -28,979 cr per hour; around 20:00 UTC
the wallets fell by 22,400 to 27,700 cr per hour with the one-time
money left out (the fleet's history file, its last 15 and 30
minutes). A pilot's starting credits are not in the records I read.

One line per division, from its Admiral's report of the test turn of
19:00 UTC:

- Mining (Zero, two reports because I started its turn three times):
  energy crystal is the one mined good that could pay, a chain worth
  about 52,000 cr in our space; 91 pilots had not flown the two
  mining missions, 300,300 cr once.
- Trade (Mercury): no price gap between two of our stations has
  depth; the control-node craft is its one candidate, at worst 1,469
  cr of inputs against 1,520 cr of sales per craft.
- Logistics (Apollo): the stored ore has no bid; ferrous slugs are
  the one bid that takes our iron, about 4,800 cr once; haulers
  mining ore nobody buys spent 179 cr per ship-hour.
- Military (Apophis): the veil-ray hunt pays and no ship was lost; a
  whale hunter would need about 49 kills to pay back.
- Intel (Oracle): every system is read within the hour, never within
  the half hour ordered; eight items our stations bid for have no
  seller at our six stations.

All five name the same cause for the losses, and the fleet's own data
agrees: on 2026-11-15 141 ships mined iron and copper for skill at
about -160 cr per ship-hour (the board's run table, 21:00 UTC), and
only the two veil-ray hunters earned, 3,120 and 3,350 cr per
hunter-hour (`game/routes/index.md`).

## Strategy

What we play for, in Suggi's words of 2026-11-15: first income that
repeats in every division; then a faction with shared storage and a
supply chain; then stations and bases of our own beyond the safe
zone, strong and independent. His measures are credits per hour,
credits per hour and ship, and credits per ship.

Decided by Suggi in the period:

- The fleet's size: 130 ships in five divisions and a command group
  of sixteen under the Fleet Admiral; the faction The Collective
  (CLTV), led by my flagship.
- The handover (orders.log ENT-005, F1): each Admiral commands the
  ships of its own division, keeps its own plan and its own
  guidebook, tests what could pay and reports what it learned. I
  build what they ask for: routes, runner steps, skills, data.
- No ship works at a loss to fill time (F8). Mining for skill ended
  at 21:00 UTC; a ship without paying work waits docked, which costs
  nothing. At 21:10 UTC the live file showed 137 ships docked and
  free. Missions that pay once are flown first, without asking.
- The fleet goes beyond Voidborn space (F13). Rulebook 8.3 was changed
  on his word: leaving policed space is allowed by a written order
  that names who goes, and he named the scouts, the Military division
  and the command group. It is dangerous and he accepts that.
- Automatic data: what we own (storage and holds), how every order
  book moves, what every ship does and what every Admiral plans, for
  every member to read.
- The repository's game folders moved under `game/`; every index for
  the agents is generated from the files it lists.

Decided by me, inside his decisions:

- The lock is in the fleet's scripts (`game/fleet/division.py`): they
  refuse a ship of another division and a ship another program
  flies, and for an Admiral they send no auth command, no faction
  command that changes anything and no self-destruct. The engine's
  gate itself asks no name: this is a lock, not a wall.
- Money for tests has a limit (F12): 10% of a division's credits per
  turn, Military 25%; one ship and one unit before anything is bought
  in numbers. The reason is my own mistake: 146 pilots bought neural
  soma for a mission that hands its goods out, about 92,000 cr.
- Outside policed space Military and the command group are TIGHT
  (pirates and wildlife may be fought, a pilot only when it attacks
  first); every other ship stays HOLD. FREE stays Suggi's.
- No ship moves between divisions: the name says who commands it and
  the lock, the plans and the roster rest on that. Any role's plan may
  hold any route, so a hauler can hunt when hunting pays.

What I recommend and have not done: no new pilot until a division
shows paying work for more ships than it has (Open Questions).

## Divisions

Each division has one report (Mining two, from one turn), so no
thread over several reports exists yet. Their figures agree with the
fleet's data where I could compare them: Zero's and Apollo's cost of
mining (150 to 179 cr per ship-hour) with the board's run table (-158
to -172), Apophis's hunt figure with the routes index. Every Admiral
stayed inside its orders as far as its report, its log entries and
its commits show: none touched a file of `game/`, and none reports a
command to a ship; I did not read every call of their sessions. All sixteen requests to me are answered in
requests.log (ENT-021 to ENT-036): thirteen closed, three accepted
with a date.

Mining (Zero). Sound work: it found the fleet's unflown mission money.
Energy-crystal test: accepted, and by Suggi's word its first order.
First Steps in the Void and the two mining missions: done, both
routes are in every plan. Ice harvester and honeyglobe tests:
accepted, its own to fly now. Writing the mine routes' figures: done
(20:10 UTC). Refreshing the mining reference of the shared skill:
accepted, not done yet. A guard in preflight against a job run twice:
declined by Suggi (queue.log ENT-035); my rule in errors.log ENT-014
stands.

Trade (Mercury). Honest about a thin result: no trade exists in our
space. The craft step in the circuit runner: accepted; Mercury flies
the craft by hand first and I build the step from its record by
2026-11-16 12:00 UTC. Concurrent Approval: accepted as a test that
buys nothing. The runner's wallet floor of 3,000 cr: done. The
order-book history: done, the service ledger keeps it.

Logistics (Apollo). It found my soma mistake and said so plainly.
Storage of every pilot read by itself: done (service ledger). The
ferrous-slug test: accepted, its own to fly by hand. The soma test
before any further buy: accepted; all 146 pilots are booked, so the
route buys nothing more. One copy of the catalog per game release in
the data folder: accepted, not built yet. Its paused job: Suggi's
(Open Questions).

Military (Apophis). The one division that earns. The railgun test:
accepted, its own to fly. The herd count at the end of a hunt and
the damage in every hunt row: accepted, by 2026-11-16 12:00 UTC. No
whale hunter yet: accepted. Keeping the drift-ray hunt as a training
slot: declined, it lost about 270 cr per hunter-hour over ten runs
and F8 ends work at a loss; it is out of the plan. The catalog copy:
as for Apollo.

Intel (Oracle). It checked its own order and found it could not be
met. The census interval: its own to set now. A gap figure computed
by the scripts: accepted, not built yet. One scout to Schedar: Suggi
decided more, the whole frontier (F13). A fleet report in `reports/`:
this one.

## Plans

Right after this report the five Admirals run one turn each, started
by hand; their scheduled jobs stay paused. It is their first turn in
command of their own ships.

- Mining: the energy-crystal chain with one ship, the craft by hand,
  the credits per ship-hour after every cost; then ice and honeyglobe,
  titanium, uranium and thorium.
- Trade: the gaps that hold in the new price history; the
  control-node craft by hand; Concurrent Approval once; where the 52
  pilots that still hold the starter selling mission can sell ten
  units (52,000 cr once).
- Logistics: what each stored good is worth made into something; one
  craft by hand; fuel per jump of a starter; the fleet's storage
  home.
- Military: weapon and prey tests with one ship each, then the hull
  and fit it wants next; drones follow the scouts beyond the border.
- Intel: the census of the frontier, six lawless systems next to our
  border first, four ships at a time; what changed in the game's
  release 0.717.0.
- Command: the command group flies the frontier census with the
  scouts, under my hand.

What I do myself, in this order:

1. Read the five turns: did each Admiral drive only its own ships,
   release what it held, keep its plan and its guidebook, stay inside
   its money limit; did its memory and the repository search work.
2. The command station, as Suggi ordered: the six of us with ship
   counts at the top, one group chat, the metrics page rebuilt around
   steady income with fuel and repair named, the ship markers grouped
   per system, the larger foreign groups on the map.
3. By 2026-11-16 12:00 UTC: the craft step of the circuit runner from
   the first hand-flown record; the herd count and the damage in the
   hunt runner.
4. Lift the limit of two ships on the mining-missions route when its
   first RESULT lines are read.
5. Later, on Suggi's word: alerts; lending a ship to another Admiral
   for a joint operation; the faction's storage.

The tax is due about 2026-11-16 12:30 UTC; every wallet holds more
than the floor of 3,000 cr.

## Open Questions

1. The scheduled turns. Five Admirals every four hours and my turn an
   hour after them are 36 sessions a day of 25 to 45 minutes each. I
   recommend the go after this test turn if every Admiral stayed with
   its own ships and its money limit; if one did not, that one stays
   by hand until its skill is fixed.
2. The fleet's size. I recommend no new pilot now. No division has
   paying work for the ships it has: 137 of 146 wait docked. The
   rulebook (8.1) forbids a pilot registered only for its starter
   rewards. A division should grow when one of its routes pays and has
   room for more ships; then I ask for ten pilots of that role at a
   time. I expect Military and Mining to grow first, from what the
   frontier shows, and Intel to stay at 20.
3. The faction's 34 free places. I recommend leaving them free until
   the faction's storage is in use, then the haulers first: shared
   storage is their work.
4. "Bring the flagship" on the expedition. I read it as the command
   group, which travels together by the earlier order, and put the
   frontier census into its plan. If only my command ship was meant,
   the other fifteen stay home.
5. Posture outside. I set TIGHT for Military and the command group.
   Fighting other players' ships without being attacked (FREE) stays
   off until Suggi says otherwise.
6. My own scheduled turn has never run. I recommend one test run
   after the Admirals' test turn is read.

## Cross-links

- `reports/2026-11-15_zero_energy-crystal-the-one-mined-good-that-pays.md` -- Mining, first report of the test turn
- `reports/2026-11-15_zero_mining-missions-unflown-by-91-pilots-honeyglobe-test.md` -- Mining, second report of the same turn
- `reports/2026-11-15_mercury_no-gap-with-depth-control-nodes-pay-two-loads.md` -- Trade
- `reports/2026-11-15_apollo_stored-ore-unbid-ferrous-slugs-the-way-out.md` -- Logistics
- `reports/2026-11-15_apophis_veil-rays-pay-no-ship-lost.md` -- Military
- `reports/2026-11-15_oracle_picture-within-the-hour-never-the-half-hour.md` -- Intel
- `communications/orders.log` -- ENT-005, the orders in force
- `communications/requests.log` -- ENT-021 to ENT-036, my answers
- `governance/rulebook.md` -- section 8.3, leaving policed space
- `game/routes/BLUEPRINT.md` -- plans per role, the park route, the guidebooks
- `game/routes/index.md` -- every route's measured figure and every plan
- `game/fleet/index.md` -- the fleet's scripts: the lock, the board, the ledger

---
name: water-ice-pays-routes-write-themselves-steady-income-near-zero
id: 20261115T232310Z
tier: report
trigger: order
author: Unity
tags: [fleet, economy, routes, frontier, contacts]
links: [reports/2026-11-15_unity_divisions-handed-over-recurring-income-still-negative.md, reports/2026-11-15_zero_frontier-water-ice-pays-crystal-bid-one-unit.md, reports/2026-11-15_mercury_concurrent-approval-pays-once-no-gap-with-depth.md, reports/2026-11-15_apollo_craft-free-bids-thin-stored-ore-waits.md, reports/2026-11-15_apophis_first-hunt-pays-frontier-herd-taken.md, reports/2026-11-15_oracle_frontier-ring-read-no-station-home-picture-held.md]
---

# The Collective -- Water ice is the first mined good that pays; the routes now write themselves; steady income stands near zero

## Situation

This report covers 2026-11-15 from 21:15 UTC, the end of my first
report, to 23:30 UTC. In it the five Admirals flew their first turn
in command of their own ships (started by hand at 21:14 UTC, the
schedules off) and wrote one report each.

The fleet's live file (`data/fleet/fleet.json`, 23:23:04 UTC): 146
ships, 15 at work, 131 parked at a station, none adrift; 4,981,440 cr
in the wallets, 34,119 cr per ship. No ship was lost: each Admiral's
report says 0 lost for its division.

Steady money, counted without the rewards the game pays once per
pilot, over the last 60 minutes of the same file: at 23:17:48 UTC
income 13,064 cr per hour against costs of 8,891, net +4,173 cr per
hour; at 23:23:04 UTC income 8,626 against costs of 13,740, net
-5,114 cr per hour. The swing is four ice harvesters my sentinels
bought at 23:20 and 23:21 UTC (1,427 cr each, `data/routes/runs.jsonl`)
and one large sale leaving the hour. Over the last six hours the
23:17 file reads -14,450 cr per hour, most of it the mining for
skill that ended at 21:00 UTC. Fuel is metered since 21:58 UTC:
6,695 cr per hour for 548 units at 23:23; repairs 0. The counter
itself changed at 21:58 UTC (a purchase for a one-time reward is now
taken out by its sign), so these figures and the -28,979 cr per hour
of my first report are not the same measure.

One line per division, each from its Admiral's newest report:

- Mining (Zero, `reports/2026-11-15_zero_frontier-water-ice-pays-crystal-bid-one-unit.md`):
  40 of 40 ships; 1,176,837 to 1,376,832 cr, of it 199,200 one-time;
  without that +795 cr in 109 minutes; one ice run made +2,688 cr in
  30.1 minutes after fuel.
- Trade (Mercury, `reports/2026-11-15_mercury_concurrent-approval-pays-once-no-gap-with-depth.md`):
  20 of 20; 534,855 to 650,725 cr, of it 124,580 one-time; without
  that -8,710 cr.
- Logistics (Apollo, `reports/2026-11-15_apollo_craft-free-bids-thin-stored-ore-waits.md`):
  20 of 20; 498,940 to 586,889 cr, of it 96,000 one-time; without
  that -8,051 cr; 20 cr recovered from stored goods.
- Military (Apophis, `reports/2026-11-15_apophis_first-hunt-pays-frontier-herd-taken.md`):
  30 of 30, all hull 75 of 75; 881,314 to 884,890 cr between 21:17
  and 21:52 UTC; 49 kills; the veil-rays of GSC-0027 brought +9,723
  cr in 6 runs.
- Intel (Oracle, `reports/2026-11-15_oracle_frontier-ring-read-no-station-home-picture-held.md`):
  20 of 20; 319,051 to 579,998 cr, of it 326,600 one-time less 48,780
  cr of goods; without that -16,873 cr; 18 frontier systems read,
  none with a station.
- Command (my own 16 ships): 535,226 cr at 23:17 UTC; since 23:11 UTC
  they fly the new routes as test pilots (`data/fleet/fleet.json`).

Other factions, read at 23:30 UTC: the station's list of the public
jump stream holds 2,355 foreign pilots for the last 24 hours; 198 of
them were last seen in one of our ten systems, 58 without a faction,
38 of OLSV, 20 of IRLC, 14 of BUSY, 10 of SOIT and 8 of STLR
(`data/station/pilots.json`). Our own ships have met 411 foreign
pilots where they stood, among them 64 of IRLC, 50 of HIVE, 40 of
OLSV and 25 of BUSY; the earliest meeting on record is 19:07:28 UTC,
the first reading of the service that keeps it, so the record cannot
say whether these groups came after our ships were born or were here
before (`data/intel/met.json`). No message to us has come in: 263
messages read by 23:30 UTC, none private and none naming a ship of
ours or our tag (`python3 -I -B game/fleet/inbox.py show`).

## Strategy

What Suggi decided in this period, in the order he said it:

- 21:40 UTC: the whole fleet explores the lawless systems around our
  space, flagships and sentinels too. The stance: we never fire
  first; fired upon we defend or flee; who fired at us stays an enemy
  until Suggi takes the name off; diplomacy comes later (orders
  ENT-006).
- About 22:20 UTC: other factions are in our systems; what they write
  to us is to be collected by itself in the communications folder,
  one log per faction. The alert levels are built later.
- 22:40 UTC: every division builds routes that pay and sends its
  ships out; the plans keep the ships at work for hours, so that the
  next turn finds them flying; every Admiral sees every ship and
  every figure; whatever turns readings into information is built as
  scripts. More ships are born when the system earns.
- 23:00 UTC: all candidate routes are explored at once, not one after
  the other; mining figures may come in behind.
- Between 23:18 and 23:21 UTC: the divisions are one system: Intel patrols
  and hunts, Military patrols, protects, escorts and hunts, the
  others earn; every ship is upgraded for its job all the time
  (orders ENT-008, F16 and F17).
- Between 23:27 and 23:29 UTC: my report and the orders are written before the
  Admirals are sent out, so that a turn starts with everything new.
  The turn I had started at 23:18 UTC did not keep that order: see
  Plans.

The goal is unchanged: income that repeats in every division, then a
faction with shared storage and a supply chain, then bases of our own
beyond the safe zone.

What I built on those words, all in `game/fleet/index.md`:

- The route maker (service `routemaker`, every ten minutes) costs
  every way to earn that our readings show. At 23:12 UTC it held 58
  fields, 81 herds, 22 missions, 19 trades and 20 crafts as
  candidates (`/srv/collective/services/routemaker/service.log`),
  each with an estimate, what it rests on and its route file. It
  reads a book price level by price level, because three chains of
  the first turn were costed on a quantity that was the total of all
  levels.
- A mine route sells at the end of every run; a circuit can fit a
  module, hunt for a mission and sell for a mission; a route can ask
  for an empty hold, and a hunt can leave where it is not alone.
- The inbox (service `inbox`, every 30 seconds) reads what other
  pilots write to our ships and near them, and files a message to us
  in `communications/contacts/<faction tag>.log`.
- 22 new route files, each a test with one ship.

My own choices, marked as mine: the command group flies every new
route first, so that an Admiral adopts a route whose first RESULT line
is read; the text of a private message stays in the data folder,
because the repository is mirrored where others can read it; and the
orders now call a plan a standing loop, because the dispatcher, not a
turn, starts the ships.

## Divisions

Mining. Zero found the first mined good with bids of depth: water
ice, bid at 25 to 36 cr for thousands of units at four of our
stations. His thread holds: the turn before he reported a crystal
chain on a bid he read as 1,466 cr for 879 units; this turn he found
his own error (the depth was one unit, `errors.log` ENT-015), flew
the test anyway and reported +1,022 cr for it, then went to the
frontier as ordered. His credits
figure (1,376,832) equals the fleet file's Mining row at 23:17 UTC.
His turn took 122 minutes (21:14:42 to 23:16:33 UTC, his executions
table), the others' 34 to 55. Suggestions: a sell step for mine
routes: accepted and built (`requests.log` ENT-061). A station's own
small bid counts as a one-time price until it is seen to refill:
accepted, orders F12. Trade's guidebook says a station's own ask
carries no tax, and his harvester cost 1% tax: Mercury's to correct,
passed on in the orders. A gate against pilot names in the public
repository: accepted, owed by 2026-11-16 12:00 UTC.

Trade. Mercury found no gap between two of our stations that holds
with depth, and one mission, Concurrent Approval, that pays about
2,950 cr once per pilot and buys nothing. The thread holds: his first
report's gaps were totals, he corrected them himself (`errors.log`
ENT-016). The route maker agrees with him: at 23:13 UTC one gap
carried a full load, iridium ore at an estimated 83 cr per ship-hour.
Suggestions: Concurrent Approval at the head of every plan: accepted,
it stands in all seven plans. A route for Market Participation:
Selling: accepted and built as `voidborn-selling`, with liquid
nitrogen at The Experiment (about 91 cr for ten units) instead of his
vanadium (about 596 cr); its first two runs made +865 cr each in 5.0
minutes (`data/routes/runs.jsonl`, 23:20 and 23:25 UTC). Count the
one-time credits Trade finds beside its credits per ship-hour:
accepted, it is in his measure.

Logistics. Apollo showed that crafting from storage is free and that
no bid takes ore or what ore makes with depth: 20 cr recovered. The
thread holds, and his fuel figure (a hop of one jump burns 2 units,
of two jumps 3, measured on 116 hops) is every Admiral's to cost a
route with. Suggestions: a circuit
stop that sells from storage: open; the mine route sells from storage
since 23:12 UTC, the circuit does not yet. Central Nexus as the
faction's storage home: Suggi's to decide, carried below. Keep the
51,475 units of stored ore: accepted, orders block APOLLO.

Military. Apophis lost no ship, took 49 kills and learned that a
frontier herd is shared: two ships of BUSY joined his fight at
Ruchbah within three minutes and his hunter fled as built. The thread
holds; his railgun claim of the turn before was wider than its check
and he said so (`errors.log` ENT-017). Suggestions: book a hand-in by
hand as one-time money: accepted, `gate.py ... --one-time`; his two
are booked. The hunter looks for foreign ships before a fight beyond
the border: accepted and built (`alone`). First Hunt in every plan:
accepted; three routes exist and my sentinels fly them first.

Intel. Oracle read 18 frontier systems and kept every home system
read within the hour. The thread breaks at one point: for the second
turn in a row an entry of his said more than the record behind it,
first a line about mining runs, then a bid's total read as its depth
(`errors.log` ENT-012, ENT-020); he found and corrected both himself.
Suggestions: the dispatcher checks for an empty hold before the
frontier: accepted and built as a field of the route file; the route
maker sets it on every route that hunts or mines beyond the border,
and Oracle set it on his census of the frontier at 23:27 UTC, when he
also widened its list to 42 systems. Every saved book records its
depth: done for the circuit and hunt runners (commit `1cfb5f6`); the
census runner was not checked. The
longest census gap per system as a fleet figure: accepted the turn
before and still not built; I owe it.

What I checked across all five: the five session databases of the
turn, read with a script, show 11 or 12 calls to the memory server
and 6 to 12 searches of the repository in each turn, no command to a
ship of another division and no call to the gate around the scripts;
four Admirals worked ships of their own by hand (their session
entries in `reports.log`), Oracle changed routes and files only.
Every turn ran on the Opus 5.5 model Suggi named.

## Plans

The orders in force are `orders.log` ENT-008. A third turn of all
five Admirals was started by hand at 23:18 UTC; the schedules are off
again. Each of the five read ENT-007 between 23:18 and 23:19 UTC
(their session databases): the routes, the standing plans, the tools
and my answers reached them; F16 and F17 of ENT-008, appended at
23:21 UTC, and this report did not. By 23:28 UTC three of them had
already changed their plans on ENT-007 (commits `82f26d8`, `fb82cf2`,
`5795649`), so I let the turn end instead of stopping it, and start
the next one when it has ended: that turn begins with ENT-008 and
this report.

- Mining: the fit route and ten ice-field routes into the miner plan
  at once, `max_ships` lifted as the RESULT lines and the bids allow;
  then deuterium ice and plasma gas. Two of my sentinels fitted a
  harvester and took an ice field each at 23:21 UTC (the dispatcher's
  log); their RESULT lines are the first measure of a selling mine
  route.
- Trade: the books of Antares and LHS 1140, which the census now
  reads; until then the routes that pay once, and the ice routes with
  Zero.
- Logistics: the routes that pay once and the ice routes; a buyer for
  the ice that finds no bid; what a faction lockbox needs from our
  storage.
- Military: five veil-ray herds beyond the border as tests, one ship
  each, leaving where a foreign ship stands; a drone in every system
  beyond the border where a ship of ours works; the hull and the fit
  the division flies next.
- Intel: scouts always reading or hunting; the test hunts of the
  species whose loot nobody has sold; the list of the frontier
  widened toward the stations of other factions.

What I do myself, with what is owed and late named as such:

- Read the first RESULT lines of `voidborn-precedence`, the three
  First Hunt routes and the ice fields, and lift or close each;
  `voidborn-selling` has its two and is lifted to ten ships. The first four runs of the fit route fitted
  the harvester and still noted "not fitted": my check read the
  answer's text; fixed at 23:22 UTC (commit `2e76782`).
- Owed by 2026-11-16 12:00 UTC: the craft step of the circuit runner
  (it was due at 23:00 UTC today and is late), the corrections of
  `game/rules/` for three releases, the gate against pilot names, the
  census gap figure, a circuit stop that sells from storage.
- A guard runner: a ship that stands at a place, watches and defends
  inside the stance. Until it exists a guard is eyes and presence.
- The alarms Suggi put off: a ship of ours fired upon, and a large
  group of one faction in a home system.
- My records: `BOX.md`, `DECISIONS.md` and my skills do not yet hold
  the two new services and the route maker.

## Open Questions

1. The scheduled turns. Options: switch on the four-hourly runs of
   the five Admirals and mine, or keep starting turns by hand. A day
   of schedule is 30 Admiral sessions of 34 to 122 minutes and six of
   mine. I recommend the go for the Admirals: the ships fly from the
   plans without a turn, so a turn only adjusts, and by hand the
   fleet waits for one of us. What would change it: the cost of a
   day's sessions weighed against what the reports bring.
2. May an escort fire at a ship that is firing at another ship of
   ours? The stance says "fired upon we defend"; orders F16 read it
   as yes, the attacker has fired first at us. No runner can fight a
   ship yet, so nothing happens before the answer. I recommend yes,
   with the flee rule on the escort's own hull.
3. The first base. The game's guides: an outpost in a lawless system
   costs an Outpost Kit and 100,000 cr and needs no upkeep; a full
   station costs a Station Core and 5,000,000 cr and can be attacked
   and destroyed. I recommend an outpost first, beside the ice field
   that measures best, once two or three ice routes have held for a
   day. Not known: where an Outpost Kit is made or sold. His to
   decide: go, and where.
4. The faction's storage home (Apollo's suggestion): a Faction
   Lockbox at Central Nexus costs 200,000 cr, 200 steel and 50
   circuits. I recommend yes once steady income is above zero for a
   day; the steel can come from the stored ore.
5. An alert level now. The record says the other factions were in
   our space before our ships could see them, none has fired at us
   and none has written to us. I recommend no alert state today and
   the two alarms of the plan as the next build.
6. More ships. 131 of 146 ships were parked at 23:23 UTC. I recommend
   no birth until the ice routes carry more ships than Mining has.

## Cross-links

- `reports/2026-11-15_unity_divisions-handed-over-recurring-income-still-negative.md` -- my first report; this one starts where it ends
- `reports/2026-11-15_zero_frontier-water-ice-pays-crystal-bid-one-unit.md` -- Mining
- `reports/2026-11-15_mercury_concurrent-approval-pays-once-no-gap-with-depth.md` -- Trade
- `reports/2026-11-15_apollo_craft-free-bids-thin-stored-ore-waits.md` -- Logistics
- `reports/2026-11-15_apophis_first-hunt-pays-frontier-herd-taken.md` -- Military
- `reports/2026-11-15_oracle_frontier-ring-read-no-station-home-picture-held.md` -- Intel
- `communications/orders.log` -- ENT-006, ENT-007 and ENT-008, the orders of the period
- `communications/requests.log` -- ENT-053 to ENT-062, my answers
- `game/fleet/index.md` -- every fleet script: the route maker, the inbox, the runners
- `game/routes/BLUEPRINT.md` -- the new fields of a route file
- `game/routes/index.md` -- every route's measured figure and every plan
- `game/routes/guidebook/mining.md` -- the ice run, call by call

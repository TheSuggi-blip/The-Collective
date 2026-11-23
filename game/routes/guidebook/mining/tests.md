# Mining guidebook -- Tests (tests.md)

### Energy crystal at the nebula of `hunt-gsc-veil-ray`, 2026-11-15
Status: proven. Updated: 2026-11-16. Evidence: migrated from guidebook/mining.md section 6.

One miner (Mining 4), 21:22 to 22:22 UTC, by hand: 166 units in three
loads (24 energy crystal, 94 iron ore, 48 copper ore), one palladium
ore bought at 436 cr, one focused crystal crafted in a station
workshop (24 ticks, no credit cost) and sold at The Experiment for
1,466 cr (a station bid of one unit), four raw crystals sold at 40 cr.
Result: +1,022 cr in 59.9 minutes after fuel and the palladium, about
1,020 credits per ship-hour; the bid was 40 cr after the sale.

### Ice at Wolf 1061 (frontier), 2026-11-15
Status: proven. Updated: 2026-11-16. Evidence: migrated from guidebook/mining.md section 6.

One miner (Mining 4), by hand, 22:25 to 23:01 UTC, with one Ice
Harvester I bought at Synchrony: 126 units in two loads (water ice 77,
nitrogen 40, methane 5, deuterium 4); sold at Synchrony, water ice at
34 to 36 cr, methane at 47. Result: +2,688 cr in 30.1 minutes after
fuel, about 5,360 credits per ship-hour, one run. It opened the ice
routes of section 1.

### Fit routes per station, 2026-11-16
Status: proven. Updated: 2026-11-16. Evidence: migrated from guidebook/mining.md section 6.

Four fit routes, one per station with asks, each `max_pilots` the asks
there and one ship at a time: the first runs at Node Beta, Node Gamma,
Synchrony and The Experiment fitted at 1,449 to 1,460 cr with fuel in
3.6 to 4.2 minutes each (`data/routes/runs.jsonl`, started 03:15 UTC); no buy above
the limit and no run without an ask, against six of ten runs that
found no ask when one route served ten fields (2026-11-15).

### Loops without a runner, 2026-11-16
Status: proven. Updated: 2026-11-16. Evidence: migrated from guidebook/mining.md section 6.

Not a test: after the engine's restart of 02:00 UTC five miners flew
mining loops with no runner for about 65 minutes; the loops stored
their ice and sold none. Stopped by hand at 03:07 UTC; three sold what
the loops had stored, 1,111 water ice and 23 methane, +42,928 cr in
their wallets (errors.log ENT-032). A ship shown "busy by hand (loop)"
with no hand hold in `data/fleet/orders/` is such a loop.

### Stored methane drained, 2026-11-16
Status: proven. Updated: 2026-11-16. Evidence: migrated from guidebook/mining.md section 6.

`drain-methane-experiment`, one ship at a time from 18:56 UTC: 13 runs
to 23:02 UTC, 17,639 credits per ship-hour (route_earnings), about 2,280
cr a run of 5 to 12 minutes; the withdraw step took only what the bid
took. 1,127 stored methane at 18:00 UTC; 479 stored and a bid of 284 left
at The Experiment at 23:02 UTC.

### Iron at Ironhollow Fading Signal, 2026-11-16
Status: proven. Updated: 2026-11-16. Evidence: migrated from guidebook/mining.md section 6.

One miner, 19:16 UTC: 233 ore in 45 minutes into storage at The
Experiment (one jump), -165 cr (data/routes/runs.jsonl); no stranger in
its notes. The field grew back about 520 iron an hour between reads with
no ship of ours on it. Lifted to 5 ships at 23:25 UTC.

### Newborn miners at home (Sol, Haven), 2026-11-22
Status: test. Updated: 2026-11-23. Evidence: table fields 23:10 UTC; table runs 2026-11-23 00:03-02:48 UTC; table books 03:09 UTC; table hulls and the live catalog's items, 03:15 UTC.

The birth wave's miners (orders P6) start at Sol Central (Solarian
Theoria: hold 70, 3 utility slots, one Mining Laser I) and the Grand
Exchange (Nebula Prospect: hold 100, 2 utility slots). The capitals'
belts read near 0, and ore bids there are 1 to 7 cr; iron and copper of
35,000 to 100,000 lie 2 to 4 jumps out (Khambalia, Markab, Nihal,
Lacaille 9352).
- Paid once, mined at those fields: First Cargo, Copper Requisition and
  Iron Supply Run at the Grand Exchange (4,300 cr a pilot, 15 runs), the
  last two at Procyon (3,300 cr, 6 runs), at up to 630 cr of fuel.
- Deep Core Prospecting is not offered at Mining 0 (18 runs) nor at
  Mining 3 (4 runs): its gate is higher; the routes ask 5, a guess.
- Mining-skill gathers one jump from a station take 30 to 38 minutes a
  load at 150 to 180 cr of fuel and sell nothing: class work only.
- Sol Central asks 2,500 cr for a Mining Laser II (power 12 against 5),
  half the other Solarian stations: a fit route, one ship first.
- Every newborn route carries `requires.empire`, so no Voidborn pilot
  is sent 10 jumps for a starter mission it does not hold.
- Tier-1 empire hulls, credits only: Bonanza (Nebula, hold 180, three
  Laser I) 60,951 cr; Archimedes (Solarian, hold 80, 4 utility slots,
  two Laser I) 34,519 cr. No Piloting asked.
- Our outpost GSC-0044 lies 5 jumps from Sol, inside the dispatcher's
  reach for a foreign pilot: seated Solarian miners can fly its belts.

### Open Tests
Status: test. Updated: 2026-11-22. Evidence: the runs of each route (hive.py route <id>); surplus.py reserve; table fields; rule F37.

How Mining gets three results (rule F37): a field is one test. Three
ships give three results only on three fields; on one field they share
its stock, so one ship flies it three times (`max_ships` 1, an empty
hold beyond the border). A fit or hull: one ship, three runs on a route
whose Laser I median is known, then a fit route. A sale: three ships
only where each sells into its own bid.

- Quantum fragments, three fields at once (Tidewater, Errai, Izar, into
  Ramen's Rest): the fragments' share of a load decides.
- A second Mining Laser II beside a Laser I: one gather result (Jishui,
  1.7 ore a minute against 2.0 for a Laser III ship); two more.
- At GSC-0044 Belt (no jump) a Laser III ship mined 12.3 ore a minute
  over 10 runs, a Laser I ship 4.1 over 27 (table runs, 19:30-23:20 UTC).
- Jishui carbon read 2,840 and falling: one ship, floor 2,000.
- Silicon far fields (Stormward, Dark Beacon) lie by the Bellatrix
  stronghold: not flown.
- Cargo Expander I, Flotation Cell: not tried.

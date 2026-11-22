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
- Silver at Errai Belt, platinum at Bunda Belt: one ship each.
- `gather-jishui-plainrock-carbon` (one run: 212 carbon in 66 minutes)
  and `gather-gsc-0049-reef-nickel` (two runs): two more runs each.
- `mine-epsilon-eridani-ice-fields`: four runs, two sold well, two lost;
  `mine-hd-20794-ice-fields` rests after three losses.
- Yildun's carbon field: no station within reach docks us; it waits for
  an outpost of ours on the north road.
- Silicon far fields (Stormward, Dark Beacon) lie by the Bellatrix
  stronghold: not flown.
- Cargo Expander I, Flotation Cell, Mining Laser II: not tried.

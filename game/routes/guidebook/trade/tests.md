# Trade guidebook -- Tests (tests.md)

### Open Tests
Status: proven. Updated: 2026-11-17. Evidence: migrated from guidebook/trade.md section 7.

What the division means to test, with the readings it rests on. A
reading is the state of its hour, not a verdict (rule F22).

- **Copper wiring from surplus copper** (craft-wiring-synchrony-hub, one
  ship, 2026-11-17 19:46 UTC): 20 runs of basic_copper_processing (8
  copper ore make 1 wiring) at Synchrony Hub from the pilot's own copper;
  nothing sold. First RESULT (19:47 UTC): 2/2 stops in 6.0 minutes, -39 cr,
  crafting XP 215 -> 485 (+270, about 13.5 a run). Lifted to 8 ships at 19:57
  UTC; 106 runs in the 4 hours to 23:32 UTC, +99 per ship-hour
  (route_earnings), while the 40 traders gained 24,445 crafting XP (19:43 to
  23:35 UTC, xpsnap.py diff). Since 23:44 UTC it asks the halving list
  (section 1) and replaces the gathering at Okab with its twins at Node Beta
  and The Experiment (requests.log ENT-256). Not a test any more.
- **Null matter into the Central Nexus bid** (carry-null-matter-beta-to-nexus,
  sell-null-matter-at-nexus, one ship each, 2026-11-17 19:41 UTC): paid from
  the first run; 9 and 6 runs in the 4 hours to 23:32 UTC, 21,029 and 47,338
  per ship-hour; traders' null matter sales +48,330 cr from 19:43 to 23:35 UTC
  over the three null matter routes (runs.jsonl). Not a test any more; one
  ship each, since one bid feeds all three.
- **Trade crystal and deuterium ice from other divisions' stores**
  (sell-trade-crystal-at-nexus, floor 340; sell-deuterium-at-node-beta, floor
  150; written 2026-11-17 23:42 UTC): one ship each, for the miners' and
  sentinels' stores; the first RESULT lines are read at the next turn.
- **Iron Ore Resupply** at Trader's Rest Resort Station (Nebula space, 22
  jumps): 80,000 cr for 10,000 iron ore delivered, a faction mission on the
  board read 2026-11-17 17:07 UTC. A Threshold carries 65 and the station
  asks iron at 6 x 924 itself; whether a delivery counts station storage is
  not known. No work for our hulls now.
- **Trade Run missions** (Node Beta and Trader's Rest boards, 2026-11-17):
  no credits, 20 to 40 trading XP and 220 to 620 piloting XP for selling a
  good at a far station (70 hydrogen at Thane Keep, 50 liquid hydrogen at
  Confederacy Central Command, 1 crystal melt at The Rampart Checkpoint).
  70 hydrogen are 140 units of hold: not for a Threshold. The melt run asks
  1 unit; its distance is not read.

- **Spiky bids from stock.** Focused crystal bids rose to 1,041 to
  1,575 cr for 1 to 12 units at Node Alpha and The Experiment for
  minutes at a time (2026-11-16 22:42 to 23:57 UTC, the view `moves`);
  gold wiring did the same at Node Alpha (190 cr, 18:45 UTC). Such a
  bid is served only from stock already lying at that station: a few
  crafted crystals stored at Node Alpha and a sell route with
  `requires.bid` at 1,000 cr is the next test.
- **The standing sell order.** One anchor beacon listed at 1,200 cr at
  Node Beta (2026-11-16 23:48 UTC; The Experiment asks 1,400 for 8,
  every station bid is 2 cr). Unfilled at 2026-11-17 03:34 UTC (section
  1); read again each turn, and cancel it when a reading shows no
  buyer in a day.
- **Buyers at every station since the game's update to v0.721.1**
  (first read about 00:57 UTC on 2026-11-17, books of 01:55 to 03:42
  UTC): uranium ore 600 cr x 3,333 (base value 150, size 2), thorium
  ore 240 x 772 to 886, seam glass 1,200 x 333 (base 600), superfluid
  vial 600 x 40 to 50, methane ice 36 x 1,000. Sirius bids crystal melt
  at 1,585 x 85 (03:29 UTC). No field we read holds uranium, thorium
  or seam glass now (requests.log ENT-194); no book we read asks any
  of them.
- **Market stations not read yet**: Procyon Colonial Station (9 jumps,
  four lawless) and Korr Fortress Station (Gliese 581, 7 jumps, a
  lawless stronghold on the chart): Procyon asked of Intel by name in
  requests.log ENT-194, the others as every station an explorer docks
  at. A stronghold is no place for a trader's test (rule F27).
- **Plasma bought at Ironlight Crossroads** (52 cr, 932,099 on offer,
  2026-11-16 01:39 UTC) and sold into the Node Beta bids: one load of
  32 units paid +1,380 cr in about 19 minutes by hand (03:11 UTC); the
  bids regained 4 to 17 units an hour at the top level. A route with
  `requires.bid` at 100 cr would fly it only when the bids stand.
- **Control nodes made by hand.** Two nodes from bought inputs cost
  about 1,141 to 1,247 cr (2026-11-16); the bids for nodes read 1,089
  x 2 at Synchrony Hub and 40 x 398 at Node Gamma (books of 23:04 to
  23:29 UTC). Two nodes are kept for the station list.
- **Foreign books.** Ironlight Crossroads (LHS 1140) and Nova Terra
  Central (Solarian): every gap against our six books read 2026-11-16
  01:39 and 03:22 UTC was one load or less (plasma 850 cr, processed
  null matter 392 cr for 2 units, deuterium ice 120 to Node Beta's 260
  x 5). Ironlight is cheaper for what the fleet buys: an Ice Harvester
  I 518 to 638 cr against 1,154 to 1,651 at home, fuel 7 cr against
  12.29. Sirius Observatory Station bids 40 cr for 527 lead ore
  (20:05 UTC), where every home bid is 1 cr: the fleet stores 493.
  Since rule F3 every station is open to one ship and one unit.
- **Titles on the Central Nexus board the fleet has not booked**
  (boards of 2026-11-16 12:34 UTC): Listening Orders (7,000 cr and a
  ship scanner), Deep Space Cartography (4,000), Local Sector Survey
  (2,500), Anomalous Readings (500), Titanium Extraction Contract
  (3,500; 20 titanium ore), Amplification Materials and Crystal
  Resonance Harvest (4,000 each), Deep Core Prospecting (5,000 and 10
  exotic matter), Material Synthesis: Basic (1,500), Network Commerce
  Protocol (1,500; sell 5 carbon ore). The survey and visit titles are
  offered to Intel (queue.log ENT-102). Station Need missions (sol
  nacre, void ichor, void-charged ichor; 3,686 to 13,133 cr) wait for a
  source: no book we read offers them and no recipe makes them.
- **The Crimson Resonance** (8,500 cr, after Signal Fragments): the
  accept hands out nothing; it asks 5 titanium alloy delivered at
  Blood Forge, Crimson space, 17 to 20 jumps out.
- **Outpost Kit** at Ironlight Crossroads: 74,010 cr (2 at 12:39 UTC);
  216,825 cr for 1 at 2026-11-15 23:21 UTC.
- Hive Antares has no market (Intel, queue.log ENT-049).

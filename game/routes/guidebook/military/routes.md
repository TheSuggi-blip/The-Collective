# Military guidebook -- Routes (routes.md)

### Standing Plan
Status: proven. Updated: 2026-11-18. Evidence: migrated from guidebook/military.md section Standing Plan.

What the 70 ships of the division (50 drones, 20 sentinels lent until Piloting 20) fly between two turns, applied
2026-11-18 00:15 UTC (orders ENT-054). No guard and no escort in the first ring of outposts and its roads (rule F33):
Military levels, hunts and farms; it guards from the stations outward when they stand. 22 drones and every sentinel
fly hunts or sales of their own first (tests, far herds the filler offered), then `@hunter`; 28 drones fly `@hunter`.
Every hunt takes one side: one ship, or a group by hand (rule F9; the dispatcher's `group: N` is the Fleet Admiral's,
queue.log ENT-175). Hunts beyond the border leave only for a pirate or a pilot filed hostile (`alone` "pirates"); the
dispatcher closes a hunt where a pirate was seen within six hours, and a system for 24 hours after a pack of 1,000
hull and shield or more (dispatch.py, commit 9582453).

| Order | Routes | Ships | Carries, expected | Why |
|---|---|---|---|---|
| First | The once line (21 routes): from 2026-11-18 00:15 UTC with `voidborn-collective-provides` after Network Expansion and `voidborn-crystal-resonance`, `voidborn-material-synthesis` after Signal Protocol | every ship; each route's own limit (The Collective Provides 4 at a time, fleet-wide) | 66,922 cr paid once to the division 2026-11-17 20:20 to 2026-11-18 00:05 UTC (table runs) | Rule F35: no drone held Voidborn Mastery 1 because The Collective Provides, the link every later link asks for, stood in no list of ours (9 of 70 had flown it) |
| Own, first | The far tests and herds the filler offered: hollow-pilgrims at Yildun, GSC-0042, GSC-0037, Sandrift, Harborlight, Wasat, Avior and more; halo-drifters at Avior, Willowgate, Saltwind; cinder-sylphs at GSC-0035, Tania, Etamin, Silverbend, Angetenar; Unity's soma carries and sales | 1 each | route_earnings 2026-11-18 00:17 UTC, 12 h: Yildun 4,695, Willowgate 4,677, GSC-0042 3,662, Avior halo-drifters 3,454, Saltwind 2,187 cr per ship-hour; GSC-0035 16,875 (2 runs) | Far herds whose loot has a far bid: melt at First Step Memorial (1,522 to 1,546 x 81 to 92), noble condensate, ember glands |
| `@hunter`, sales | `store-hold-central-nexus`; from 00:15 UTC four ember-gland sales to the deep far bids (`sell-ember-nexus-krynn`, `sell-ember-node-beta-krynn`, `sell-ember-hexstar-krynn`, `sell-ember-hexstar-first-step`); the two Hex Star sales; soma; five melt sales | 1 each, only with goods stored and a bid of 5,000 or more (glands) | ember glands 7,400 x 24 at Crimson War Citadel, 5,686 x 57 at First Step (00:07 and 22:41 UTC); the division stores about 58 | A gland is 480 cr at home and 5,686 to 7,423 at these bids |
| `@hunter`, money hunts | hollow-pilgrim hunts, Hassaleh, Gemma, the Achernar and Lesath cinder-sylphs | 1 each | see section 1 | Melt and glands go to far bids |
| `@hunter`, reserve hunts | 24 grazer carapace hunts, seven veil-ray and five drift-ray hunts, frost-moths | 1 each | -114 to -486 cr per hunter-hour, 2.2 to 16.5 kills an hour (2026-11-17 20:20 to 2026-11-18 00:05 UTC) | Carapace (28,994 short), biogas (3,444 short) and caustic sac stored for the reserve (rule F24) |
| `@hunter`, fallback | from 00:15 UTC: `craft-armor-military-*` (carapace into armor plate, 4,833 short) and `craft-steel-military-*` (own iron into steel plate, 30,745 to make) at The Experiment, Node Beta, Synchrony Hub, Central Nexus; `craft-piping-node-beta` | 6 each | 0 cr a run expected (nothing bought or sold; fuel to the station) | The reserve's iron is met: the iron gather fallback cost -22,528 cr in 93 ship-hours from 20:20 UTC (table runs) |
| Then | the same crafts, `census-frontier`, `park` | -- | -- | No iron or copper gathered; a ship with nothing to make docks (orders P2) |
| `@guard`, escort | none (rule F33) | 0 | -- | The template stays for posts beyond the first ring |

What would change the plan: the group flight's record (section 1, Group hunts) and the dispatcher's `group: N`; the
first RESULT lines of the four gland sales (a far bid emptied, or a road that costs a ship); a far bid that comes back
for melt or curd; the crafts using up the stores (then ships dock); a station or an outpost past the first ring (its
guard); a pirate at a hunt's place.

### Route Guides
Status: proven. Updated: 2026-11-17. Evidence: migrated from guidebook/military.md section 1.

How each kind of route of this division is flown: the fit and skills
it needs, its place, its steps, what opens and closes it.

### Hunts of grazers (`hunt.py`)
Status: proven. Updated: 2026-11-17. Evidence: migrated from guidebook/military.md section 1.

- Fit: the starter Pulse Laser I (10 damage, reach 3). The runner sets
  the combat mode `external`, picks the most hurt grazer of 100 hull or
  less, closes in, fires, and flees under 60 percent hull or when a
  second ship joins. A kill leaves a carcass that must be looted
  outside the battle within 30 minutes.
- `alone` (every hunt beyond the border): before each fight the hunter
  looks who stands at the place and leaves when a ship not of ours or a
  pirate is there.
- After the hunt the runner docks at the route's station, sells what a
  bid there takes, keeps aboard only goods a book read within the hour
  bids for (since 2026-11-16, commit 0b27fa7), and stores the rest.
- Standing hunts (`standing: true`, no `requires.bid`) store their
  goods for the station list and are not judged on their pay; money
  hunts carry `requires.bid` and close while their loot has no bid.
- Readings, drone hunts 2026-11-16 19:55 to 2026-11-17 00:25 UTC
  (`hunt_figures.py`, credits by `routes.earned`: tax and the wallet
  guard's gifts out): 949 hunter-minutes, -2,497 cr, -158 cr per
  hunter-hour; looted 67 verdigris curd, 78 creature carapace, 49
  crystallized biogas, 4 ember glands, 1 crystal melt, 5 raw xeno meat.
  Achernar cinder-sylphs 3 runs, 4 kills, +1,700 cr (2,642 per
  hunter-hour); the drift-ray hunt at home 16 runs, 38 kills, 46 biogas,
  -200 per hunter-hour; the veil-ray hunts 5 to 6 kills an hour each.

### Grazer hunts for carapace (`hunt-*-carapace`)
Status: proven. Updated: 2026-11-18. Evidence: migrated from guidebook/military.md section 1.

- `hunt.py` on belt-grazers and patina-grazers (60 hull) with the starter
  Pulse Laser I; five kills or 40 minutes, a herd floor of 6 (herds of 11
  to 15) or 8 (16 or more), `alone`, an empty hold, the nearest of our
  stations. `min_bid` 5000: nothing is sold, every good goes into storage
  for the reserve (rule F24). Standing work: the loss stop leaves it alone.
- Readings, drone hunts 2026-11-17 04:12 to 08:10 UTC (`hunt_figures.py`): 161 runs, 3,389
  hunter-minutes, -16,292 cr, -288 cr per hunter-hour; 71 runs without a kill, 61 of them
  ended at once by `alone` (a ship not ours at the place: BUSY combat drones, passing
  miners; none fired). Best: Ironhollow Fading Signal 7.3 kills an hour, Acrab Thinspace
  Rubble 6.1, GSC-0044 Forgotten Tailings 5.8; Achernar Belt, Goldcrest Belt and the
  Glitterback Scatter no kill in 2 to 6 runs. From 2026-11-17 08:20 UTC the hunts beyond the border
  carry `alone` "pirates" (hunt.py e138722).
- A belt-grazer kill gave about 2.5 carapace at Keid (18 carapace and 6
  raw xeno meat from 7 kills, 2026-11-16 to 2026-11-17, data/routes/runs.jsonl).
  21 herds of 11 to 24 grazers within 7 jumps of home were written at
  2026-11-17 04:12 UTC from the table `herds`; places where pirates fought
  (Stormwatch, Gliese 876, GSC-0021, Felis, Thornhaven) were left out.
- Readings 2026-11-17 08:20 to 12:00 UTC (`hunt_figures.py --since 2026-11-17T08:20:00Z --role drone`):
  163 drone hunt runs, 21 without a kill (71 of 161 before), all hunts +18,878 cr in 5,473 hunter-minutes,
  207 cr per hunter-hour (-288 before); the carapace hunts 3.9 to 8.6 kills an hour at -65 to -326 cr per
  hunter-hour, 2.9 to 8.6 kills an hour. Under `alone` "pirates" no stranger fired on a hunter; the lowest
  hull read 76 to 98 percent on the grazer hunts (the prey hits back), 45 to 81 on the cauldronback test.
- Readings 2026-11-17 12:16 to 16:05 UTC (`hunt_figures.py --since 2026-11-17T12:16:00Z --role drone`): all drone
  hunts -15,538 cr in 6,030 hunter-minutes, -155 cr per hunter-hour (no far bid for melt or glands after 14:55 UTC);
  the carapace hunts 3.1 to 8.1 kills an hour at -102 to -445 cr per hunter-hour. The eight hunts written at 12:15 UTC
  with `alone` true left 26 of their 40 runs at once for a stranger who was no pirate (to 16:40 UTC); Bluerift and GSC-0038 6 of 6. Since 16:15 UTC they carry
  `alone` "pirates". The division as a whole: 317 runs, +9,916 cr in 150.8 ship-hours (+66 per ship-hour), the seven melt
  sale runs +30,681 of it.
- Readings 2026-11-17 16:45 to 20:20 UTC (`hunt_figures.py --since 2026-11-17T16:45:00Z`, credits by `routes.earned`): the
  drone hunts -174 cr in 4,395 hunter-minutes (-2 cr per hunter-hour); the sentinel hunts +16,782 cr in 1,755
  (574). The carapace hunts 2.6 to 8.2 kills an hour at -119 to -232 cr per hunter-hour; the drift-ray hunt at home
  14.5 kills an hour (39 biogas in 15 runs). No run left for a stranger or a pirate at a home hunt; one far test each
  at Arneb and Wasat left for a stranger. The division as a whole: 448 runs, +69,938 cr in 203.9 ship-hours (+343
  per ship-hour), 230,601 cr paid once beside it (table runs).
- Readings 2026-11-17 20:20 to 2026-11-18 00:05 UTC (`hunt_figures.py --since 2026-11-17T20:20:00Z`, credits by
  `routes.earned`): the drone hunts +21,851 cr in 3,874.6 hunter-minutes (338 cr per hunter-hour), the sentinel hunts
  +4,529 in 2,262.4 (120). The carapace hunts 2.2 to 7.4 kills an hour at -114 to -486 cr per hunter-hour; the home
  drift-ray hunt 16.5. The division as a whole: 492 runs, -13,095 cr steady in 225.5 ship-hours, 66,922 cr paid once
  (table runs); its iron gathering alone -22,528 cr in 93.0 ship-hours.

### Hollow-pilgrim hunts and the melt chain
Status: proven. Updated: 2026-11-18. Evidence: migrated from guidebook/military.md section 1.

- Hollow-pilgrims (70 hull) drop crystal melt, carapace and raw xeno meat.
  Readings: Rasalhague 4 kills and 5 melt in 54.5 minutes (2026-11-17 03:06
  UTC); Felis 2 kills and 1 melt in 41 minutes (2026-11-16); the command
  group's GSC-0040 hunt 3 kills and 1 melt in two runs (sold at 1,582).
- Bids: Sirius Observatory 1,580 to 1,585 cr, its depth from 1 to 85 in a
  day; The Experiment 1,389 to 1,394 cr x 9 to 12, which comes and goes
  beside a standing 54 cr x 50 (data/market/history.jsonl, 2026-11-16 18:41
  to 2026-11-17 04:03 UTC); a Station Need mission at The Experiment pays
  1,603 cr for one melt.
- The chain: the hunt (`min_bid` 1000) sells at The Experiment when its
  high bid stands; else the melt stays aboard while a fresh book bids
  1,000 or more. A hold of more than five units takes
  `store-hold-central-nexus` (Central Nexus storage); `sell-melt-nexus-sirius`
  and `sell-melt-experiment-sirius` carry 3 melt or more from storage to
  the Sirius bid (9 and 7 jumps). Since 2026-11-17 08:20 UTC three more carry it from Node Beta and
  Synchrony and sell what lies at Sirius, each from 2 units stored and a bid of 2.
  First melt: four hunts of 07:23 to 07:47 UTC looted 11 (Elnath 3, Atria 5, Groombridge
  3; GSC-0024 none) in 138 hunter-minutes; 19 melt stored at 08:20 UTC.

- Readings 2026-11-17 08:20 to 12:00 UTC: Elnath 14 melt in 3 runs (+8,782 cr), Groombridge 34 12 in 4
  (+5,244), GSC-0024 13 in 5, Atria 6 in 4, Epsilon Eridani 4 in 2 (+5,948), Felis 4 in 4, Hassaleh 2 in 2;
  Rasalhague none in 2. Sirius bid 1,570 x 98 at 11:57 UTC; 1,528 x 74 at 14:22 UTC, then 54 x 48 at 14:24 UTC
  (the deep bid left; The Experiment 1,431 x 1 at 15:44 UTC). From 12:16 to 16:05 UTC seven melt sale runs brought +30,681 cr. Felis is off from 12:11 UTC by D9: three of its
  four runs left because a pirate stood at the place.
- Readings 2026-11-17 16:45 to 20:20 UTC: the Sirius bid came back (1,502 x 39 at 18:04 UTC, 1,484 x 27 at 18:57 UTC) and
  the five melt sales took it to 1 by 19:44 UTC: 12 sale runs, +55,996 cr (sell-melt-at-sirius 24,699, from The
  Experiment 18,727, from Node Beta 12,570). First Step Memorial Station (Outer Rim, 18 jumps) bid 1,814 x 99 at 19:33
  UTC and 1,794 x 11 at 19:57 UTC: another fleet sold some 88 there in 24 minutes. Sirius 55 x 20 at 20:18 UTC. A melt
  bid of depth stands for one to two hours and is emptied by whoever comes first; the sales that wait for it with
  `requires.bid` take their share without a hand.
- Readings 2026-11-17 20:20 to 2026-11-18 00:05 UTC: the far tests sell melt at First Step Memorial Station (Outer Rim):
  Yildun 2 runs +8,631 cr (6 melt), GSC-0042 3 runs +7,135 (5), GSC-0037 3 runs +1,261 (6), Sandrift 2 runs (7 melt sold
  for 10,717 cr in one). First Step bid 1,546 x 83 at 20:51 UTC to 1,522 x 81 at 23:12 UTC; Sirius 54 x 48 all evening.
- A figure that lies: the Sandrift run of 21:46 UTC reads -8,917 cr in `routes.earned`; it earned about +4,303. The
  wallet sweep gave 13,220 cr to a flagship 138 s before the run's end, and the seam rule of `routes.moved` counts that
  gift in neither run (requests.log ENT-264).

### Cinder-sylph hunts and the ember-gland chain
Status: proven. Updated: 2026-11-18. Evidence: migrated from guidebook/military.md section 1.

- Cinder-sylphs (40 hull) drop ember glands and crystallized biogas. Achernar Gas Pocket: 16 kills and 17
  glands in 8 runs and 79.7 hunter-minutes, 2026-11-17 08:20 to 12:00 UTC (5,809 cr per hunter-hour while
  the glands sold at 480).
- Bids: every home station 480; Hex Star in Dheneb (lawless, 9 jumps from The Experiment, 11 from home)
  3,692 x 46 at 09:17 UTC to 3,919 x 37 at 11:49 UTC; Nova Terra asked 14,274 x 2 (data/market/history.jsonl).
- The chain from 2026-11-17 12:11 UTC: the hunt has `min_bid` 2000, so no home bid takes a gland; a gland
  stays aboard while a book read within the hour bids 2,000 or more, else it is stored at The Experiment;
  `store-hold-central-nexus` empties a full hold at Central Nexus; `sell-ember-experiment-dheneb` and
  `sell-ember-nexus-dheneb` carry 6 stored glands or more to the Hex Star bid (2,000 x 5). The command
  group's cinder-sylph hunts sell into the same bid.
- Hex Star bid 4,058 x 31 at 12:53 UTC, 4,265 x 16 at 14:05 UTC, then 480 x 50 at 14:55 UTC: the bid was filled within
  three hours. The Crucible Garrison bid 7,302 x 1 at 15:51 UTC (a depth of one is no bid). 24 glands held at 16:03 UTC
  (19 stored, 5 aboard); the sales did not fly.
- Bids 2026-11-17 20:51 to 2026-11-18 00:07 UTC (data/market/history.jsonl): Crimson War Citadel (Krynn, Crimson space)
  7,401 x 5, 7,423 x 6, 7,400 x 24; First Step Memorial 5,701 x 57, 5,686 x 57; The Levy Customs 5,686 x 9; Hex Star no
  move on record since 14:55 UTC. The GSC-0035 test sold 3 glands at Krynn for 22,203 cr (20:32 UTC, 4 kills in 42
  minutes). The division stores about 58 glands: 26 at Hex Star, 21 at Node Beta, the rest at home stations and aboard.
- From 2026-11-18 00:15 UTC four sales carry stored glands to those bids, one ship at a time, each from 3 or 4 glands of
  the pilot's own and a bid of 5,000 x 3 or more: Central Nexus and Node Beta to Krynn (20 jumps), Hex Star to Krynn and
  to First Step (15 jumps each); no pirate line on our record in 24 hours on or beside those roads at 00:15 UTC. The road
  from Node Beta to First Step passes Hollowcrest (ten Dross raiders, 19:06 UTC) and was not written.

### Guard (`guard.py`)
Status: proven. Updated: 2026-11-18. Evidence: migrated from guidebook/military.md section 1.

- Keeps one drone at the place where a miner or hunter of ours flies
  the guarded route; opens only while one does. It never fires; it
  looks once a minute (our pilots, the others with their faction tag,
  pirates), leaves under 60 percent hull, in a fight, after `minutes`
  at the place, or when no pilot of ours carried the guarded route in
  two looks, and docks at its station.
- A guard pays off where the guarded ships stay at the field: put it
  where the station is near. Readings: Marfik (six jumps from its
  station), 2026-11-16, 60 minutes, the miner there in 11 of 61 looks,
  -132 cr; Ironhollow (one jump), 2026-11-17 00:21 UTC, 4 minutes at the
  place, 5 looks, -66 cr, left when the miner went home; its second run
  from 00:34 UTC saw our miners in 4 of its first 5 looks, beside a
  combat drone of a foreign faction (data/routes/logs).
- Posts: Ironhollow Fading Signal (Mining's 10 iron miners, one jump from
  The Experiment) and Schedar Belt (15 iron miners, one jump from Node
  Beta; written 2026-11-17 04:12 UTC), Marfik while the gas trader flies
  it. Ironhollow 2026-11-17 01:36 and 02:42 UTC: 60 minutes, 61 looks,
  -33 cr each; strangers at the field in both: combat drones of the
  faction BUSY and pilots of HIVE, SIST and VEIL; no shot at any ship of
  ours (data/routes/runs.jsonl, errors.log).
- `census-guard-ice` reads the systems where our ice miners work, one
  after another; 14 runs in the 4 hours to 04:01 UTC, -628 per
  ship-hour.

- Sizing (2026-11-17 08:21 UTC): one guard to a place. A guard's look lists every pilot at its
  place: at Schedar Belt 17 to 31 of ours and one stranger (VMan of STLR) in a look
  (guard log, 07:51 to 08:05 UTC), so a second guard there adds no sight. What a guard
  prevents: nothing by force; it never fires first and it is no match for a pirate. It
  is the minute-by-minute reading of who comes to a field where up to 45 of ours work,
  and the first warning; no ship of ours was fired on at a guarded field. What it costs:
  -42 cr per ship-hour at Schedar (17 runs), -32 at Ironhollow (route_earnings, 4 h to
  08:00 UTC). Posts from 2026-11-17 08:21 UTC: Ironhollow Fading Signal, Schedar Belt, Ironhollow
  Echo Ejecta, Garnet Belt; Marfik and `census-guard-ice` after them.
- The first outpost (orders ENT-031 task 3): Mining and Intel name Garnet (lawless, 5
  jumps from home, 2 from The Experiment; neighbours Achernar, Atlas, Cedarhold, HD 40307,
  Ruchbah; table lanes). The guard plan: `guard-garnet-belt` reads the place from now on;
  when the outpost stands, one guard keeps the outpost's place and one the belt, the
  hunters of the herds one jump around (Garnet slag-tortoises, Cedarhold and Garnet
  veil-rays, Atlas, Achernar) dock and refuel there (the pirate group once planned
  there was withdrawn by orders D9; the outpost went to GSC-0044, below). The outpost's 12,000 hull without a shield is
  beyond what drones of 75 hull defend against a pirate pack: they see, warn and save
  the ships; they do not hold the walls.
- The first outpost at GSC-0044 (orders ENT-036, P4 a), planned 2026-11-17 12:20 UTC: `guard-gsc-0044-belt` keeps
  GSC-0044 Belt while the carapace hunter works there and reads the site once a minute; when the outpost stands and
  Mining gathers there, `guards` names Mining's route. The kit's road (LHS 1140, Antares, GSC-0041, Ironhollow, The
  Experiment, Achernar, Cedarhold, GSC-0044) holds no pirate on our record in it or one jump from it; the guard posts
  at Ironhollow (two), Achernar and GSC-0044 lie on it. A guard keeps only the place of a mine or a hunt route
  (dispatch.py), so no drone flies beside the kit: the step is asked of the Fleet Admiral (requests.log ENT-217).
  What a drone beside it would do: see, warn and take the first shot meant for the hauler; it is no match for a
  pirate pack.
- The escort (requests ENT-217, ENT-226): `guard.py --follow <pilot>` (commit 6bc8f99, tests FollowTests) keeps
  beside one pilot of ours instead of at one place: once a minute it reads that pilot's system and place from
  data/fleet/ships/, jumps and moves after it, looks, never fires, and ends two looks after that pilot's order for the
  guarded route is gone (a `circuit` order counts with `--follow`). The dispatcher's half, a guard route whose
  `guards` names a circuit, is the Fleet Admiral's (17:30 UTC). First flight at home, 2026-11-17 16:14 to 16:33 UTC,
  beside a ship on the Signal Protocol circuit: 15 minutes, 9 looks, 4 jumps, no shot, -105 cr, ended two looks after
  the ship's run ended. It stood beside the ship while the ship waited at Node Beta; after the first jump it trailed one
  hop behind and never shared its place again in five looks: it reads the ship's place only when its own jump has
  ended. Beside a hauler it keeps the long stops (a buy, the founding), not the road between them.
- Readings 2026-11-17 12:20 to 15:54 UTC: 18 guard runs at the seven posts, 880 looks, 0 to 14 strangers a run
  (most at Ironhollow Echo Ejecta), hull 100 percent in every run, no shot at any ship of ours; -36 to -195 cr a run.
- Readings 2026-11-17 16:45 to 20:20 UTC: 13 guard runs, 12.4 ship-hours, -983 cr in all (-72 to -216 cr a run; table
  runs), hull 100 percent in every run, no shot at any ship of ours. The post at GSC-0044 Belt stood from 16:02 to
  17:11 UTC, across the founding of the outpost at 16:46 UTC (requests.log ENT-248).
- The first escort route (2026-11-17 20:16 UTC): `escort-voidborn-conductive-lattice` follows one pilot of ours on the
  Node Beta chain, which buys silver at Ironlight Crossroads (LHS 1140, lawless, 6 jumps), up to 90 minutes, one
  drone. The dispatcher starts it with `--follow` while the circuit flies. Logistics' outpost circuit gets the same
  file (`escort-<circuit>`) once it exists.
- The escort's RESULT lines: two runs beside a ship on the Node Beta chain, 2026-11-17 20:33 and 20:57 UTC, 23.1 and
  24.3 minutes, -169 and -156 cr, hull 100 percent, no shot (table runs); both ended "guarded ship gone" when the
  guarded run ended. Not flown since orders ENT-045 (no escort in the first ring).

### Group hunts (`group_hunt.py`, a skill script, by hand)
Status: proven. Updated: 2026-11-18. Evidence: migrated from guidebook/military.md section 1.

- Rule F9 and orders D14: a side of three Thresholds with a Pulse Laser I reads firepower 33 (x7 = 231) and
  toughness 465 to 490 (half 232 to 245), so a pilot whale of 220 hull passes both gauges on paper. The script waits
  for free drones, docks them at one station, makes a game fleet (`spacemolt_fleet` create, invite, accept), flies the
  leader to the place, hunts one creature, and flees every ship when one of ours falls under 60 percent hull.
- The first flight, 2026-11-17 20:12 to 20:38 UTC, four drones on a pilot whale at Stellar Siphon in Nexus Prime
  (observations kind `group_hunt`; the script's log):
  - `create` answered max_size 3; the third invite answered `fleet_full` ("3 members + pending invites"): the leader
    counts in the three.
  - The leader's `go-to-poi` brought both members to the place: members follow the leader's flight.
  - The leader's `hunt` pulled both members into the battle at tick 0 (side 2: 3 players). The drone outside the fleet
    that hunted the same creature stood on the same side at tick 3 (4 players): a ship needs no game fleet to share a
    hunt, so a group larger than the fleet's capacity is possible and needs no Leadership for the fight itself.
  - Only the leader fought. At tick 10 the leader (zone inner, dist 2, its target the whale) had dealt 8 and taken
    106; the three others (zone mid, dist 3, no target in the table) had dealt and taken 0; the whale (engaged, dist 1)
    read 84 percent. The whale emptied the leader's shield (111 percent) in 8 ticks; the side fled at tick 13 with the
    leader at 48 percent hull, which fell to 33 during the flight; the whale stood at 79 percent. No kill, no loot, no
    ship lost; the four were repaired at Central Nexus. The leader's 8 dealt and the whale's 16 percent lost by tick 10
    do not agree: not explained.
  - Cost: four drones about 26 minutes and one repair; credits not measured apart from the division's runs.
- What it teaches: a member joins with no target and stays a zone back; the prey fights the nearest ship, so a group
  is as strong as the ships in reach with a target set. The script now sets each member's target
  (`spacemolt_battle target`) and advances it to one zone from the prey; the next flight reads whether the whale then
  dies, and what each ship deals and takes. Until then no group route: the dispatcher's `group: N` (Fleet Admiral)
  should start each member with its own `hunt` of the same creature, a target and the advance, a fleet only for the
  common flight.
- Flights 2 and 3, 2026-11-18, pilot whales (220 hull) at Stellar Siphon, starters with one Pulse Laser I each. Flight
  2 (00:08 to 00:34 UTC, a fleet of three and one ship outside that joined at tick 3): every member had its target, yet
  all five ships and the whale stood at zone outer, dist 6, for 48 ticks; the whale took the leader's shield from 111 to
  81 percent and nobody dealt a point. `dist` is a ship's place on one line from the fight's centre and moves with the
  ships; a Pulse Laser I reaches 3. Flight 3 (00:40 to 00:54 UTC, three ships, each advancing until its own dist was 2):
  all at dist 2 by tick 3, each member dealt 7 to 9 by tick 10, the whale fell to 73 percent in 20 ticks; it struck the
  leader alone, shield 111 to 0 by tick 18, then hull 100, 68, 38, 24 and 9 percent in four ticks; the side fled and
  escaped. No kill, no loss, all three repaired to 75 of 75 (the script's RESULT line).
- So three starters deal about 3 a tick against 220 hull, some 70 ticks, while the prey breaks one starter in about
  20: no starter group on pilot whales. The script flees all at hull under 85 percent or shield 0 since 00:55 UTC. The
  next group test takes prey of 100 hull or less, or waits for a second weapon or a tier-2 hull.

### Sales of stored loot (`sell-curd-*`, `sell_stored.py`)
Status: proven. Updated: 2026-11-17. Evidence: migrated from guidebook/military.md section 1.

- A circuit with `requires.stored` and `requires.bid`: a pilot that
  stores curd at the station withdraws only what the bid takes at its
  best price and sells it. The ledger reads storage about every 40
  minutes, so a run may find nothing left after a sale by hand.
- The three curd sales are off since 2026-11-17 16:15 UTC: verdigris curd is held back whole for copper piping
  (surplus.py reserve, 607 of 607; rule F24), and the veil-ray hunts store it (min_bid 5000).

### Pirate hunt (`pirate_test.py`, a skill script, by hand)
Status: proven. Updated: 2026-11-17. Evidence: migrated from guidebook/military.md section 1.

- One drone held by hand visits the places of the systems named, reads
  `get_nearby` at each, writes every pirate it lists into the division's
  record (`observe.py`, kind `pirate`), and attacks only a lone pirate
  whose name is on its list of weak ones. It flees under 60 percent
  hull, at once when a second ship joins the pirate's side, and when it
  is no match (after 8 ticks in reach the pirate lost under 15 points
  while the drone lost over 30). It never re-issues `attack` on a pirate
  already fought: the game then summons that pirate's stronghold's
  combat pirates in the system (the command's help).
- After the fight: loot the own kill, dock, hand in Pirate Bounty.
  The test's reading is in section 6.

### Making from own stores, the fallback
Status: proven. Updated: 2026-11-18. Evidence: migrated from guidebook/military.md section 1.

- Since 2026-11-18 00:15 UTC (orders ENT-054, P2: the reserve's iron is met) a drone with no herd open makes before it
  gathers: `craft-armor-military-<station>` turns its own stored carapace into armor plate (carapace_plating, 6 to 1,
  by hand) and `craft-steel-military-<station>` its own stored iron into steel plate (basic_iron_smelting, 10 to 1), at
  The Experiment, Node Beta, Synchrony Hub and Central Nexus; the craft list asks halving sizes, so one visit uses up
  what the pilot holds there. Nothing is bought or sold. No iron or copper is gathered; a ship with nothing left to
  make docks.
- Before it: `mine.py` with the Mining Laser I put iron and copper into storage at the shared fields under fleet-wide
  caps; from 2026-11-17 20:20 UTC to 2026-11-18 00:05 UTC that cost -22,528 cr in 93.0 ship-hours (table runs).

### Route Templates
Status: proven. Updated: 2026-11-18. Evidence: migrated from guidebook/military.md section 2.

The templates of this division are kept in
`game/routes/templates/military.json` and listed in
`game/routes/templates-military.md`; the tool plan with
`action=templates` shows them with the ships on each.

| Template | Routes, in order | Trains | For |
|---|---|---|---|
| `@hunter` | `store-hold-central-nexus`; four ember-gland sales to Krynn and First Step and the two to Hex Star; `carry-soma-synchrony-to-alpha`; five melt sales; hollow-pilgrim, frost-moth, halo-drifter and cinder-sylph hunts; 24 grazer carapace hunts; seven veil-ray and five drift-ray hunts; then the crafts from own stores: armor plate (`craft-armor-military-*`), steel plate (`craft-steel-military-*`), `craft-piping-node-beta`; no gathering since 2026-11-18 00:15 UTC | gunnery, weapons, tactics, xenobiology, piloting; crafting in the fallback | every drone: a herd for each hunter, a far bid for its loot, the reserve made from stores when no herd is open |
| `@guard` | `guard-ironhollow-fading-signal`, `guard-schedar-belt`, `guard-ironhollow-echo-ejecta`, `guard-garnet-belt`, `guard-achernar-belt`, `guard-gsc-0044-belt`, `guard-marfik-emission-nebula` | piloting, navigation | six drones, before `@hunter` in their cell |

A ship born tomorrow gets `@hunter` with one word: `plan.py use
<ship> hunter`. A new herd or a new guard post is one change of the
template, and every ship that names it follows within the minute.

### Missions That Pay Once
Status: proven. Updated: 2026-11-18. Evidence: migrated from guidebook/military.md section 3.

The once routes at the head of the plan: every pilot flies them first,
each under its own limit. The 30 drones of 2026-11-15 have booked
nearly all of them (`data/fleet/onetime.json`); the 20 drones born
2026-11-16 fly them now. The forecast of 00:28 UTC counts 31,580 cr
paid once on the way.

| Mission | Pays once | How it is flown |
|---|---|---|
| Signal Fragments | 7,000 cr | From navigation 3 (`requires.skills`); every drone stood at navigation 3 or above by 2026-11-16 18:27 UTC |
| First Hunt (nexus, gsc, achernar) | 1,000 cr, 50 weapons XP, 15 xenobiology XP, 20 piloting XP | The circuit runner's `hunt` step: three belt-grazer kills; one hunter per herd, `min_creatures` 3 |
| Cracking the Shell | 1,500 cr, 55 weapons XP | Offered only to pilots with First Hunt booked (`requires.booked`) |
| Conductive Lattice | 10,893 cr in a chain of three | Buys silver and crystal; 29 of the first 30 drones flew it |
| Pirate Bounty | 2,000 cr, 20 weapons XP, 20 piloting XP: kill 1 pirate | Offered on the board of Central Nexus to a drone that had flown First Hunt (2026-11-17 00:19 UTC); not flown while orders D9 and D10 stand (a mission that asks to destroy a pirate waits for Suggi's word) |
| The Collective Provides | 2,500 cr, Voidborn Mastery 25 | Trade's `voidborn-collective-provides` (20 nickel at Rotanev, 4 at a time fleet-wide; 63 paid in 73 runs from 2026-11-17 12:00 UTC); in the drone list First since 2026-11-18 00:15 UTC: 9 of 70 of ours had it |
| Crystal Resonance Harvest, Material Synthesis: Basic | 4,000 and 1,500 cr, Voidborn Mastery 35 and 25 | Mining's `voidborn-crystal-resonance`, `voidborn-material-synthesis` (one paid test each, 23:25 and 23:27 UTC); after The Collective Provides |

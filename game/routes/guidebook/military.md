---
name: guidebook-military
id: 20261115T205807Z
tier: intel
author: Unity
links:
  - The-Collective:game/routes/BLUEPRINT.md
---

# military.md -- Guidebook of the Military Division

Kept by Apophis; read by every member. What the Military division
learned about its routes, its levelling, its ships and the pirates
around our space, so that every ship born later starts where the
others stand. Started by the Fleet Admiral on 2026-11-15; from there
Apophis writes it at the end of every turn.

- A figure comes from `routes.py measure`, the view `route_earnings`
  (the tool `sql`), a run's RESULT line or a row of
  `data/routes/runs.jsonl`, and carries its date. A number no record
  holds is written `not measured`.
- A figure in this book is a dated reading, never a verdict: what a
  route earns now is asked every turn (rule F22).
- The plan in force is the division's plan file (the tool plan); every
  route with its figure is in `game/routes/master-index.md` and its
  sub-indexes.

## Class Card

The Military class in short (rule F14); the detail is in section 4
(levelling) and section 5 (ships and fits). Sources: the catalog's
tables `skills` and `hulls` (catalog 0.723.2), the game's page
https://www.spacemolt.com/docs/skills.md (read 2026-11-17 08:20 UTC),
the table `ship_skills`, the ship files and the tool fleet, view levels
(2026-11-17 20:17 UTC).

### Ships

- Tier 0, every drone now: Threshold, hull 75, shield 80, armor 3,
  speed 1, CPU 16, power 30; 1 weapon, 2 defence, 2 utility slots; a
  Pulse Laser I (10 energy damage, reach 3) and a Mining Laser I. Six
  carry one or two Shield Booster I (+25 shield each), bought for the
  pirate group that the orders withdrew (D9).
- The 20 sentinels of the command group fly with Military until Piloting 20 (orders D12, since 2026-11-17
  18:20 UTC): Thresholds with a Pulse Laser I, eight of them with an Ice Harvester I beside it; planned and
  levelled like the drones (their hunts first, then `@hunter`).
- Tier 1, no Piloting asked: Vigil (patrol, hull 75, shield 90, 2
  weapons, 2 defence; 111,316 cr in credits at Central Nexus) and
  Paradox (fighter, hull 60, shield 130, 2 weapons). Not bought: one
  more weapon slot for 111,316 cr does not pay against grazers.
- Tier 2, Piloting 10: Recursion (fighter, hull 150, shield 150, 3
  weapons, speed 4), Dualism (heavy fighter, hull 160, shield 175, 2
  weapons, 3 defence), Census (customs patrol, 140 / 165). The
  Recursion is the drone's next hull: three weapons and the speed to
  leave a fight. No price read yet.
- Tier 3, Piloting 20: Annihilation (battlecruiser, 4 weapons, hull
  360, shield 430) and Voidborn Singularity (cruiser, 3 weapons).
- Fit: the weapon slot first (Autocannon II, 18 kinetic damage, 1,800
  to 2,755 cr), then shield boosters in the defence slots. One Pulse
  Laser I does not kill prey above about 77 hull (its firepower gauge, rule F9): the cauldronback test
  (120 hull) took 0 kills in 4 runs and left the drone at 45 percent
  hull (2026-11-17). Default stance flee, set by script (game 0.721.0):
  a fight a drone starts still opens at fire.
- Style: one hunter to a herd, one guard to a field; never the first
  shot at a player or an empire's ship (F2); pirates are Military's to
  judge (orders D9 of ENT-042), and the block of ENT-042 says no test,
  group or fight for now: a hunt leaves a place where a pirate stands,
  a guard leaves when one attacks; flee under 60 percent hull or when
  a ship not of ours joins. Groups of three and more (D14) for prey one
  ship cannot kill: section 1, Group hunts.

### Skills

| Skill | Why it matters | What trains it, on which routes | Drones now (low / median / high) | Next goal |
|---|---|---|---|---|
| Gunnery | +1% damage with every weapon a level | Firing weapons in combat: every hunt of `@hunter` | 2 / 4 / 7 (sentinels 2 / 2 / 3) | 5 |
| Weapons | +1% damage and +0.2% critical chance a level; kills train it most | Dealing damage, destroying ships: the hunts | 1 / 3 / 4 (sentinels 1 / 1 / 2) | 4 |
| Tactics | Accuracy, evasion and combat speed +1% a level | Hitting, evading, retreating in combat: the hunts | 2 / 4 / 6 (sentinels 1 / 2 / 3) | 5 |
| Xenobiology | +1% value of harvested molt goods a level | XP per kill, by the creature's tier: the hunts | 2 / 4 / 7 (sentinels 1 / 2 / 4) | 5 |
| Shields | Shield capacity, recharge and resistance +1% a level | Taking shield damage in combat: grazers hit the hull of a few hunters (lowest hull 45 to 98 percent in 31 runs, 2026-11-17 08:20 to 12:00 UTC), yet no drone holds XP (16:16 UTC: 18 guard runs and every hunt since read 88 to 100 percent hull) | 0 for all | not measured how grazer hits count |
| Armor | Armor and hull HP +1% a level | Taking hull damage | 0 for all | as Shields |
| Piloting | Tier 2 hulls at 10 (Recursion), tier 3 at 20; the sentinels go back to the command group at 20 | Flying, jumping, mining, fighting | 5 / 7 / 9 (sentinels 6 / 7.5 / 8); 186 XP an hour, about 36 hours to 10 | 10 |
| Navigation | Fuel and jump time -1% a level | Travel: guards, long hunts, the sales to Sirius | 4 / 4 / 5 (sentinels 4 / 4.5 / 6) | 5 |
| Voidborn Mastery | Energy weapon damage +1% a level (our pulse lasers) | Voidborn missions only (the list First; rule F35) | 0 for the drones; one sentinel at 1 | 1: the chain waits on The Collective Provides (20 nickel mined by the pilot) |
| Bounty Hunting | Bounty payouts +1% a level | Defeating pirates | 0 | none while D9 stands |
| Leadership | Fleet capacity (3 at first) and coordination | Leading a game fleet: the group hunts (D14) | 0 | the group test's record first (section 1) |

Mining and deep core mining are the fallback, not the class: medians 6
and 7 at 20:17 UTC (tool fleet, view levels), still above every combat
skill, because gathering filled the hours no herd was open (section 4).

## Standing Plan

What the 70 ships of the division (50 drones, 20 sentinels lent until Piloting 20) fly between two turns, applied
2026-11-17 20:20 UTC (orders ENT-042). 6 drones fly `@guard` and then `@hunter`; one drone flies the escort first;
16 drones and every sentinel fly hunts of their own first (tests and the far hunts the filler offered), then
`@hunter`; the rest fly `@hunter`. Every hunt and every guard takes one side: one ship, or a group (rule F9; groups
by hand only until the dispatcher's half stands, queue.log ENT-175). The hunts beyond the border leave only for a
pirate or a pilot filed hostile (`alone` "pirates"). The dispatcher closes a hunt, a mine or a guard where a pirate
was seen within six hours (orders D9); a pack seen longer ago is taken out of the plan by hand (2026-11-17 20:16 UTC:
Violethall, six Nyx pirates at 13:16 UTC; Hollowcrest, ten Dross raiders at 19:06 UTC).

| Order | Routes | Ships | Carries, expected | Why |
|---|---|---|---|---|
| First | The once line of the fleet (18 routes) | every ship; each route's own limit | 1,000 to 21,000 cr once a pilot; 230,601 cr paid once to the division 16:45 to 20:20 UTC | Missions that pay once first; the Voidborn chain for rule F35 |
| Own, first | Six tests of 20:19 UTC, 8 to 17 jumps out: cinder-sylphs at GSC-0035 and GSC-0045, hollow-pilgrims at GSC-0037, GSC-0042, Sandrift and Yildun (north, a base site of G3); the paying Harborlight pilgrims; the far hunts of 16:17 UTC (Oxbow, Saltwind, Avior, Willowgate, Arneb, Tania, Etamin, Silverbend, Angetenar, Wasat, Biham) | 1 each | route_earnings, 12 h: Harborlight 4,284, Avior halo-drifters 4,510, Oxbow 4,472, Willowgate 5,164, Saltwind 2,215 cr per ship-hour; Arneb -54 | New herds: every near herd holds its one hunter; far bids for melt, noble condensate (690), halo goods |
| Escort | `escort-voidborn-conductive-lattice` | 1 drone | not measured; a guard costs -72 to -216 cr a run | The first escort the dispatcher starts (requests ENT-237); Logistics' outpost circuit gets its own once it exists |
| Sentinels' own | 1 to 4 far hunts each (hollow-pilgrims, cinder-sylphs, halo-drifters, a chlorophage), the ones they flew for the command group | 1 each | sentinel hunts 16:45 to 20:20 UTC: +16,782 cr in 1,755 hunter-minutes, 574 cr per hunter-hour | Their skills (gunnery median 2) and Piloting toward 20 |
| `@guard` | `guard-ironhollow-fading-signal`, `guard-schedar-belt`, `guard-ironhollow-echo-ejecta`, `guard-garnet-belt`, `guard-achernar-belt`, `guard-gsc-0044-belt`, `guard-marfik-emission-nebula` | 6 drones, 1 a post | -72 to -216 cr a run (13 runs, 16:45 to 20:20 UTC) | Up to 45 ships of ours at Schedar, 35 at Ironhollow Echo Ejecta, 29 at Garnet; GSC-0044 is our outpost |
| `@hunter`, holds and sales | `store-hold-central-nexus`, two ember-gland sales, `carry-soma-synchrony-to-alpha`, five melt sales | only with goods aboard or stored and a bid | melt: 12 sale runs +55,996 cr 16:45 to 20:20 UTC while Sirius bid 1,484 to 1,502 (18:04 to 19:44 UTC); gone again at 20:18 UTC | Melt and glands are sold, not kept (not in the reserve) |
| `@hunter`, money hunts | hollow-pilgrim hunts, Hassaleh pilgrims, Gemma halo-drifters, Achernar and Lesath cinder-sylphs, the Bluerift rime-grazer test | 1 each | Hassaleh +4,325, Atria +422, Groombridge -363 cr per hunter-hour (16:45 to 20:20 UTC) | Melt waits aboard or in storage for the next far bid |
| `@hunter`, reserve hunts | 24 grazer carapace hunts, seven veil-ray and five drift-ray hunts, the Hassaleh frost-moths (superfluid vials stored at Node Beta since 20:16 UTC) | 1 each | -114 to -453 cr per hunter-hour, 2.6 to 14.5 kills an hour | Carapace, curd, biogas and vials stored for the reserve (rule F24) |
| `@hunter`, fallback | `craft-piping-node-beta`, three steel crafts, then the shared gather fields | caps of their owners | piping -101, gather fields -70 to -232 cr per ship-hour (4 h) | Most shared iron fields stood under their floor at 20:13 UTC: the drones gathered at Schedar, Ironhollow and Garnet from the list Then |
| Then | the fleet's shared gather fields, the steel crafts, `census-frontier`, `park` | -- | -- | A ship should never reach `park` |

At 20:18 UTC 65 of 70 ships worked, 1 started, 4 were held for the group test, none waited (fill.py check).
The drone hunts made -174 cr in 4,395 hunter-minutes from 16:45 to 20:20 UTC (-2 per hunter-hour; -155 the turn
before); the division read +25,899 cr net in the hour to 20:21 UTC (hive.py fleet).

What would change the plan: a group flight that kills a whale (the first, 20:12 UTC, made none: only the leader
fought; section 1, Group hunts) and the dispatcher's `group: N`, which would open the pilot whales of 220 hull (324
seen in 87 systems) to sides of three; a far bid back (melt at Sirius or First
Step Memorial, glands at Hex Star); the first RESULT lines of the six tests and of the escort; Logistics' outpost
circuit (its escort); a pirate at a hunt's place.

## 1. Route Guides

How each kind of route of this division is flown: the fit and skills
it needs, its place, its steps, what opens and closes it.

### Hunts of grazers (`hunt.py`)

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

### Hollow-pilgrim hunts and the melt chain

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

### Cinder-sylph hunts and the ember-gland chain

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

### Guard (`guard.py`)

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

### Group hunts (`group_hunt.py`, a skill script, by hand)

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

### Sales of stored loot (`sell-curd-*`, `sell_stored.py`)

- A circuit with `requires.stored` and `requires.bid`: a pilot that
  stores curd at the station withdraws only what the bid takes at its
  best price and sells it. The ledger reads storage about every 40
  minutes, so a run may find nothing left after a sale by hand.
- The three curd sales are off since 2026-11-17 16:15 UTC: verdigris curd is held back whole for copper piping
  (surplus.py reserve, 607 of 607; rule F24), and the veil-ray hunts store it (min_bid 5000).

### Pirate hunt (`pirate_test.py`, a skill script, by hand)

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

### Gathering, the fallback

- `mine.py` with the Mining Laser I; iron and copper into storage at
  the route's station; nothing sold. The fields are shared by every
  division under fleet-wide caps and close under their floors.

## 2. Route Templates

The templates of this division are kept in
`game/routes/templates/military.json` and listed in
`game/routes/templates-military.md`; the tool plan with
`action=templates` shows them with the ships on each.

| Template | Routes, in order | Trains | For |
|---|---|---|---|
| `@hunter` | `store-hold-central-nexus`, two ember-gland sales, `carry-soma-synchrony-to-alpha`; five melt sales; six hollow-pilgrim hunts, Hassaleh pilgrims and frost-moths, Gemma halo-drifters, the Achernar and Lesath cinder-sylphs, the Bluerift rime-grazer test; 24 grazer carapace hunts; seven veil-ray and five drift-ray hunts; the piping craft and three steel crafts from stored iron and copper; then iron gathering, copper last | gunnery, weapons, tactics, xenobiology, piloting | every drone: a herd for each hunter, steel or iron when none is open |
| `@guard` | `guard-ironhollow-fading-signal`, `guard-schedar-belt`, `guard-ironhollow-echo-ejecta`, `guard-garnet-belt`, `guard-achernar-belt`, `guard-gsc-0044-belt`, `guard-marfik-emission-nebula` | piloting, navigation | six drones, before `@hunter` in their cell |

A ship born tomorrow gets `@hunter` with one word: `plan.py use
<ship> hunter`. A new herd or a new guard post is one change of the
template, and every ship that names it follows within the minute.

## 3. Missions That Pay Once

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

## 4. Levelling Guide

Which skills a drone levels and on which work (rule F23).

- **2026-11-17 20:17 UTC** (ship files, 50 drones and 20 sentinels): drones gunnery 4 (2 to 7), weapons 3 (1 to 4),
  tactics 4 (2 to 6), xenobiology 4 (2 to 7): tactics and xenobiology up one since 16:16 UTC, weapons half, gunnery
  held; the sentinels
  gunnery 2, weapons 1, tactics 2, xenobiology 2 (lent at 18:20 UTC from the command group, where they mined and
  hunted less). Piloting 5 / 7 / 9, 186 XP an hour, 36 hours to 10. Shields, armor 0 for all; Voidborn Mastery 0,
  one sentinel at 1.
- **2026-11-17 16:16 UTC** (table ship_skills, 50 drones): gunnery 4 (2 to 7), weapons 2.5 (1 to 4), tactics 3 (2 to
  6), xenobiology 3 (2 to 6): gunnery rose one level since 12:16 UTC, the others half a level or none, with 25 to 35
  drones hunting. Piloting 5 / 7 / 8, 42 hours to 10. Shields, armor and Voidborn Mastery 0 for all.
- **2026-11-17 12:16 UTC** (table ship_skills, 50 drones): gunnery median 3 (1 to 6), weapons 2 (0 to 4), tactics 3
  (1 to 5), xenobiology 3 (1 to 6): each median rose one level since 08:20 UTC, when 20 to 31 drones hunted;
  every drone holds gunnery, tactics and xenobiology, 49 weapons. Piloting 5 / 7 / 8, 46 hours to 10. Shields,
  armor and Voidborn Mastery 0 for all.
- **2026-11-17 08:20 UTC** (table ship_skills, 50 drones): gunnery median 2, highest 6;
  weapons 1, 4; tactics 2, 5; xenobiology 2, 6; piloting 7, 8 (172 XP an hour since
  birth, 50 hours to 10); shields and armor 0. Deep core mining median 7 and mining 5
  stand above every combat skill: the fallback filled the hours no herd was open.
- **Hunter drone** (`@hunter`): gunnery, weapons, tactics and
  xenobiology rise only by fighting. On 2026-11-17 04:20 UTC over 50
  drones (data/fleet/ships/): gunnery median 2, highest 6, 48 drones
  above 0 (00:25 UTC: median 1, 40 above 0); weapons median 1, highest 4,
  42 above 0 (34); tactics median 1, highest 5, 46 above 0; xenobiology
  median 1, highest 5, 45 above 0. Shields and armor stand at 0 on every
  drone. The division's strongest skill was deep core mining (median 6,
  156 XP an hour since birth, `hive.py levels`): 35 drones mined copper at
  Pherkad at 04:17 UTC. From 04:13 UTC the grazer hunts take them.
- **Guard drone** (`@guard`): a guard flies and waits; it trains
  piloting and navigation by its jumps. Navigation median 3, highest 4.
- **Every drone**: piloting opens the hulls (tier 2 at piloting 10).
  Piloting 4, 6 and 7 (lowest, median, highest), 168 XP an hour on
  average since birth: about 57 hours to piloting 10 (`hive.py levels`,
  2026-11-17 04:05 UTC; 00:25 UTC: 3, 6, 7, 164 XP, 63 hours). The missions add piloting XP: Pirate Bounty 20,
  First Hunt 20, Signal Fragments and the survey missions more.
- **Pirate hunter** (one drone so far): the Pirate Bounty pays 20
  weapons XP beside the kill's own; a fight with a pirate trains shields
  when the pirate hits the shield (section 6).
- The catalog's XP per level: 340 for level 2 to 3, 585, 900, 1,285,
  1,740, 2,265 for level 7 to 8, then 2,860 and 3,525.

## 5. Ships and Fits

The starter Threshold: 1 weapon, 2 defence and 2 utility slots, CPU 16,
power 30, hull 75, shield 80, armor 3, speed 1 (`get_ship`, 2026-11-17
00:19 UTC). Every drone fits a Mining Laser I (utility, CPU 2, power 5)
and a Pulse Laser I (weapon, CPU 2, power 5): CPU 4 and power 10 of 16
and 30 are used, so both defence slots are free.

| Module | What it does | Asks in our books, 2026-11-17 00:08 UTC |
|---|---|---|
| Pulse Laser I | 10 energy damage, reach 3, cooldown 1 | 1,117 cr at Central Nexus (475) |
| Pulse Laser II | 18 energy damage, reach 3; CPU 3, power 8 | 11,010 to 17,241 cr |
| Autocannon II | 18 kinetic damage, reach 2; CPU 4, power 6 | 1,800 cr at The Experiment (3), 2,755 at Central Nexus (4) |
| Shield Booster I | +25 shield; CPU 2, power 4 | 2,664 to 3,791 cr; 2,955 at Central Nexus (26) |
| Armor Plate I / II | armor; CPU 1 / 2, power 0 | 631 to 646 cr / 1,279 to 2,102 cr |
| Piercing Railgun I | 60 kinetic damage, reach 5, ammunition, 70% armour bypass | 5,000 cr (2026-11-15) |

- The pirate test drone flies two Shield Booster I since 2026-11-17
  00:31 UTC: shield 130, CPU 8 of 16, power 18 of 30, 5,969 cr for both
  at Central Nexus (booked as a tool, paid once).
- A railgun hit does not kill a 60-hull grazer: the first hit leaves it
  at 4 to 8 hull and it flees (2026-11-15).
- Hulls priced by the game (`commission_quote`, Central Nexus,
  2026-11-16 03:16 UTC): the Vigil (tier 1) 111,316 cr with credits only,
  or 15,706 cr plus materials, 87 ticks to build. The tier-1 hulls name
  no piloting gate. Of the hulls the catalog lists for pirates and
  others (`game/catalog/ships/pirate-and-other.md`, 0.719.3), tier 2
  `small_claims` (Corsair, 240 hull, 130 shield, 3 weapons) and `larder`
  (Hunter, 460 hull, 3 weapons) name no piloting gate either.

## 6. Pirates

Pirates are Military's (rule F27). What we know, from the game's
public battle record (`https://game.spacemolt.com/api/battles`, the
1,000 newest battles from 2026-11-13 16:04 to 2026-11-17 00:00 UTC, read
2026-11-17 00:13 UTC) and our own readings.

- **The orders now (D9 of orders ENT-042).** Suggi, 2026-11-17 about 18:45 UTC: whether and when to
  fight pirates is Military's judgement, by rule F9 (both gauges, a test first, one side at a time,
  the cost weighed; a crew keeps a grudge against our faction). The block APOPHIS of ENT-042 still
  says no test, no group and no fight for now: every ship avoids them, and the dispatcher closes a
  hunt, mine or guard where our readings saw a pirate within six hours. The Korr raider elites
  Ironhold (125 hull, 105 shield) and Blockade (250 hull, 90 shield) stood at GSC-0016 Emission
  Nebula at 08:30 UTC and at Felis Frost Ring at 09:36 UTC (admirals.log ENT-032).
- **Packs read 2026-11-17** (Intel's census, observations kind `pirate`): six Nyx pirates at
  Violethall Belt at 13:16 UTC (Skarth 250 hull and 90 shield, five of 120 hull and 100 shield);
  ten Dross raiders at Hollowcrest Frozen Drift at 19:06 UTC (two of 200 hull and 140 shield,
  eight of 120 to 125 hull and 100 to 105 shield); Korr's Ironhold, Blockade and Greywatch at
  GSC-0021 Ice Fields at 17:33 UTC (admirals.log ENT-051). By rule F9 a pack of ten weighs some
  1,370 hull: beyond any side we can field. The hunts at Violethall, Hollowcrest and Alathfar (one
  lane from Hollowcrest) left the plans at 20:16 UTC.

- **Where.** The nearest pirate stronghold is Gliese 581, 7 jumps from
  home, whose one lane leads to GSC-0016 (`game/map/galaxy.tsv`). Within
  8 jumps of home the record holds 74 pirate battles in 11 systems:
  Gliese 876 29 battles (87 pirates killed, 1 player ship lost),
  Thornhaven (4 jumps) 7 (11, 0), Biham 7 (9, 0), Felis 7 (16, 1),
  GSC-0021 6 (6, 0), Coldwater 6 (13, 0), Sualocin 5 (1, 3), Kitalpha 3
  (11, 0), GSC-0016 2 (4, 0), Gliese 581 1 (0, 1), Tanglewood 1. Each
  system is one line of `data/observations/military.jsonl`, kind
  `pirate`. Our own census saw pirates in 8 places in 5,045 looks
  (`data/intel/sightings.jsonl`): Tanglewood, Gliese 876, Felis, GSC-0016,
  GSC-0021, Thornhaven.
- **What.** The record names pirates, not their ships. Near us the
  lone ones die fast: Flinch to one ship in 3 to 6 ticks with 95 to 120
  damage dealt in all, Breach Scout 101 to 117, Sentinel 121 to 125,
  Probe about 125, Hauler 100; Ironhold takes 230 to 360 alone. Pirates
  in pairs and fives fight together: Blockade and Ironhold killed a
  player ship in one tick with 156 damage at Gliese 876 (2026-11-16 09:55
  UTC), more than a Threshold's 75 hull and 80 shield. The stronghold
  fought as twenty named ships, Grand Marshal Korr and two stations
  among them, and killed a player ship in one tick (2026-11-16 18:14 UTC).
- **Who hunts them.** Combat drones of the faction tagged BUSY won most
  of the battles near us (Thornhaven, Gliese 876, GSC-0021, Coldwater,
  Biham); they stood at Ironhollow and at Thornhaven's Dimming Pocket
  beside our ships and never fired at ours (guard logs, sightings).
- **The mission.** Pirate Bounty: kill 1 pirate, 2,000 cr, 20 weapons XP,
  20 piloting XP, on the board of Central Nexus. Its text advises a lone
  pirate scout for a small ship and warns that a scout meeting a bigger
  ship scans it, runs and calls raiders.
- **The test** (orders ENT-020, step 2): one drone (Pulse Laser I, two Shield Booster I: hull 75, shield 130)
  searched 4 places at Thornhaven, 2 at Coldwater, 4 at GSC-0021 and 5 at
  Felis from 00:37 to 00:49 UTC on 2026-11-17 and met one pirate: Flinch at
  Felis Frost Ring, alone, `patrolling`, tier `scout`, faction Grand
  Marshal Korr, ship Red Herring, hull 85, shield 30 (get_nearby). It
  attacked at 00:49:42 UTC. In the 4 ticks in reach the pirate's shield
  fell from 100 to 20 percent (about 24 points, some 6 a tick); ours fell
  from 111 to 65 percent of 130 (about 60 points, some 15 a tick); both
  hulls stood at 100 percent. At tick 6 a Breach Scout (Lawn Dart)
  joined from elsewhere in the system, later a Worn Track (Losers
  Weepers, a salvager): the drone fled by the rule. The flee took 13
  ticks at speed 1 against pursuers of speed 5 and 6; the pirates stayed
  at distance 3 and hit nothing more. Out of the battle by about 00:57
  UTC, docked at Node Beta, hull 75 of 75. Cost: 6,473 cr in all, of it
  5,969 the two boosters (booked once as a tool); no kill, no bounty
  (pirate_test.py log; the battle status; data/fleet/ships/).
- **The record of 2026-11-17 04:16 UTC** (`pirate_record.py`, skill
  military-turn: 1,000 battles ended 2026-11-13 22:16 to 2026-11-17 04:11
  UTC, pirate battles within 8 jumps of home; one line per system in
  `data/observations/military.jsonl`, kind `pirate`): Gliese 876 31
  battles (the pirates won 1), Felis 9 (won 1, last 00:55 UTC: our test),
  GSC-0021 8 (last 03:20 UTC), Thornhaven 7, Biham 7, Coldwater 6, Kitalpha
  3, GSC-0016 2, Gliese 581 1 (the stronghold, won), Sualocin 1. A lone
  scout (Flinch, Breach Scout, Sentinel, Probe) that lost had taken 95 to
  125 damage, an Ironhold 358 to 408. The census of every division keeps
  each pirate it meets since 2026-11-17 03:37 UTC (census.py, `pirate_list`):
  at 03:51 UTC Flinch (scout, hull 85, shield 30) fled at Felis Belt B.
- **The record of 2026-11-17 08:20 UTC** (`pirate_record.py`, 1,000 battles ended 2026-11-13
  23:29 to 2026-11-17 08:09 UTC): Gliese 876 37 battles (last 08:09 UTC), Felis 12 (06:09),
  GSC-0021 9 (07:41), Thornhaven 7, Biham 7, Coldwater 5, GSC-0016 3, Kitalpha 3, Gliese
  581 1, Sualocin 1. A lone pirate that lost had taken 95 to 167 damage (Ironhold 358 to
  408). Garnet, the outpost site named by Mining and Intel, lies 6 jumps from GSC-0021 and
  Coldwater, 7 from Gliese 876 and Felis, 9 from the stronghold (table lanes).
- **The fleet call** (the game's help for `spacemolt_fleet`, read
  2026-11-17 04:15 UTC): a fleet leader controls navigation and combat for
  all members; capacity starts at 3 and rises with Leadership and
  command-capable hulls; `invite` needs the member at the leader's place;
  members of the fleet undocked in the system join its battles
  (`game/rules/08-combat.md`, auto-join). A group is then three drones in
  one game fleet behind one pirate script, not five drones moved by hand.
  `fleet_probe.py` (skill military-turn) flies the call docked first:
  create, invite, accept, status, disband; its line is kind `fleet_probe`.
- **What a group takes** (step 3): from the test, an estimate, not measured: one Threshold
  deals about 6 a tick and takes about 15 from one scout, so alone it
  needs some 15 ticks for a scout's 115 points while help comes in 6.
  Five drones in reach together put about 30 a tick on one scout (some 4
  ticks to kill it) and spread the pirates' 15 to 35 a tick over five
  shields of 105 to 130. The group: five drones with gunnery 3 or more,
  one Shield Booster I each at least (route `fit-shield-booster-pirate-group`
  in the list First since 2026-11-17 01:04 UTC), entering one battle on
  the same side (`spacemolt_battle engage`), each fleeing under 60
  percent hull; a group script that holds five drones and moves them
  together is the next build. A weapon of 18 damage (Autocannon II,
  1,800 to 2,755 cr; Pulse Laser II, 11,010 cr and more) doubles a drone's
  share. What a kill pays beside the bounty (the wreck's loot) is not
  measured; whether Pirate Bounty repeats is not known.

## 7. Open Tests

- The group hunt, second flight (orders ENT-042, D14): the first (2026-11-17 20:12 UTC, section 1, Group hunts)
  answered the fleet's questions and made no kill, because only the leader fought; the next flight sets every
  member's target and closes it in, and reads the kill, the loot and the damage per ship.
- The six far tests of 20:19 UTC (GSC-0035 and GSC-0045 cinder-sylphs; GSC-0037, GSC-0042, Sandrift and Yildun
  hollow-pilgrims): kills an hour, goods, the road, the fuel. Enif (25 jumps) and Unukalhai (24) were offered and left
  out: too far for a test; Raysheet veil-rays left out: their curd and carapace are held for the reserve.
- The first escort the dispatcher starts (`escort-voidborn-conductive-lattice`): its RESULT line.
- `alone` "pirates" (2026-11-17 08:20 UTC): no shot from a stranger at a hunter to 20:20 UTC; read it again each turn.
- Answered and off (2026-11-17): the cauldronback at Node Beta (0 kills in 4 runs, hull to 45 percent),
  the slag-tortoises at Garnet (0 kills in 2 runs): a second weapon or a group first.
- Not tested, waiting: Cloudwhale Oil Wanted at Hex Star (100,000 cr for 20 lumen oil): lumen oil
  comes from cloudwhales of 508 to 3,304 hull (Saltwind, Lesath), beyond one Pulse Laser I and beyond a group of three.
- Shields and Armor: which hit trains them (no drone holds XP after grazer hits of up to 12 percent of the hull).
- A tier-1 or tier-2 hull with two or three weapons (section 5).

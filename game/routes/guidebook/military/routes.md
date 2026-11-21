# Military guidebook -- Routes (routes.md)

### Standing Plan
Status: proven. Updated: 2026-11-21. Evidence: the tool plan (show); hive.py briefing (the plan table, column carries); hive.py forecast Apophis; fill.py check.

What the 70 ships fly between two turns (orders ENT-056, block APOPHIS):
hunts that pay, combat skills, fits, a group that kills. No guard or escort
in the first ring (F33). Every hunt takes one side, one hunter to a herd.

| Order | Routes | Ships | Why |
|---|---|---|---|
| First | the once line (21 routes), each under its own limit | every ship | rule F35, money paid once |
| Own | far herds and the tests the filler offers (`fill.py fill <role> --write`), Unity's soma carries | 1 each | the far bids for melt, glands, condensate |
| `@hunter` | sales from storage, money hunts, reserve hunts (templates entry) | 1 each | see the hunt entries |
| Then | the crafts from own stores, `park` | 6 each | ships with no herd make, never gather (F23) |

Sized by the briefing's column carries: a herd carries one hunter. What
changes it: a weapon fit that opens prey of 80 to 140 hull (tests.md), a
group that kills, a far bid that comes or goes, a station of ours past the
first ring (its guard), a pirate at a hunt's place (dispatch closes it).

### Hunts of grazers (`hunt.py`)
Status: proven. Updated: 2026-11-21. Evidence: game/fleet/hunt.py; skill military-turn hunt_figures.py; routes.md entry versions of 2026-11-17 (--history).

- The runner picks the most hurt creature of the route's species, closes
  in, fires, loots the carcass outside the battle within 30 minutes and
  flees under 60 percent hull or when a second ship joins.
- `alone` true leaves when any ship not ours stands at the place; `alone`
  "pirates" only for a pirate or a hostile pilot. Tests beyond the border
  start with `alone` (F3); true cost the eight hunts of 2026-11-17 12:15
  UTC 26 of 40 runs with no shot fired.
- After the hunt it docks at `sell_at`, sells what a bid of `min_bid` or
  more takes, keeps aboard what a fresh book elsewhere bids for, stores the
  rest.
- A money hunt names its loot's bid (`requires.bid`); a reserve hunt has
  `min_bid` 5000 and `standing: true` and stores everything (F24).
- Figures per place: `hunt_figures.py --since <time> --role drone`.

### Grazer hunts for carapace (`hunt-*-carapace`)
Status: proven. Updated: 2026-11-21. Evidence: hunt_figures.py; the tool stock (reserve); routes.md entry versions of 2026-11-17 and 2026-11-18 (--history).

Belt-, patina- and soot-grazers (60 hull) at about 24 belts within 7
jumps: five kills or 40 minutes, a herd floor of 6 or 8, an empty hold, the
nearest station of ours, `min_bid` 5000: every carapace is stored for the
reserve. A kill gives about 2.5 carapace. They run at a small loss per
hunter-hour and train the combat skills: standing work, never judged on
pay (F22). Places where pirates fought stay out.

### Hollow-pilgrim hunts and the melt chain
Status: proven. Updated: 2026-11-21. Evidence: data/market/history.jsonl (crystal_melt); loot_bids.py; routes.md entry versions of 2026-11-17 and 2026-11-18 (--history).

- Hollow-pilgrims (70 hull) drop crystal melt, carapace and raw xeno meat.
- Melt bids come deep and go within one to two hours: Sirius Observatory
  1,480 to 1,585 x 27 to 98 on 2026-11-17, else 54; First Step Memorial
  1,522 to 1,814 x 81 to 99. The hunts keep melt aboard while a fresh book
  bids 1,000 or more, else store it; `store-hold-central-nexus` empties a
  full hold.
- Five sales carry 2 to 3 stored melt to the Sirius bid from Central
  Nexus, The Experiment, Node Beta and Synchrony, each with `requires.bid`;
  12 sale runs took +55,996 cr on 2026-11-17 16:45 to 20:20 UTC.
- Read the best melt book every turn (`loot_bids.py`): the sale follows the
  buyer.

### Cinder-sylph hunts and the ember-gland chain
Status: proven. Updated: 2026-11-21. Evidence: table runs (route sell-ember-*, 2026-11-18 00:23 to 01:26 UTC); loot_bids.py; data/market/history.jsonl (ember_gland).

- Cinder-sylphs (40 hull) drop ember glands and crystallized biogas. Home
  stations bid 480 a gland; far stations of other empires 5,686 to 8,184
  (Crimson War Citadel at Krynn, First Step Memorial, The Levy Customs).
- The hunts carry a `min_bid` above the home bid, so glands stay aboard or
  are stored; four sales (`sell-ember-nexus-krynn`, `-node-beta-krynn`,
  `-hexstar-krynn`, `-hexstar-first-step`) carry 3 or more stored glands to
  a bid of 5,000 or more, one ship each.
- Their first runs, 2026-11-18 00:23 to 01:05 UTC: five runs, +216,337 cr
  in 2.4 ship-hours, the fifth with nothing to carry (table runs). The road from Node Beta to First Step
  passes Hollowcrest (a raider pack on record) and was not written.

### Making from own stores, the fallback
Status: proven. Updated: 2026-11-21. Evidence: table runs (craft-*-military-*, 2026-11-18); requests.log ENT-271; the tool stock (member Apophis).

- A ship with no herd open makes from its own stores: `craft-armor-
  military-<station>` (carapace into armor plate) and `craft-steel-
  military-<station>` (iron into steel plate) at The Experiment, Node Beta,
  Synchrony Hub, Central Nexus; `craft-piping-node-beta`,
  `craft-wiring-synchrony-hub` for copper. One visit uses up what the pilot
  holds there; nothing is bought or sold.
- No iron or copper is gathered: gathering is Mining's alone (F23; Unity's
  no, requests.log ENT-271). A class with no work at home takes its work
  further out: far hunts, groups, fits.
- Stored loot is sold by circuits with `requires.stored` and `requires.bid`
  (the ledger reads storage about every 40 minutes).

### Route Templates
Status: proven. Updated: 2026-11-21. Evidence: game/routes/templates/military.json; game/routes/templates-military.md; the tool plan (templates).

| Template | Routes, in order | Trains |
|---|---|---|
| `@hunter` | `store-hold-central-nexus`; the gland, soma and melt sales; hollow-pilgrim, frost-moth, halo-drifter, cinder-sylph hunts; the carapace hunts; the veil-ray and drift-ray hunts; the crafts from own stores | gunnery, weapons, tactics, xenobiology, piloting; crafting |
| `@guard` | the guard posts (topic-pirates.md); no ship while F33 holds | piloting, navigation |

A ship born tomorrow gets `@hunter` with one word: `plan.py use <ship>
hunter`. A new herd is one change of the template.

### Missions That Pay Once
Status: proven. Updated: 2026-11-21. Evidence: data/fleet/onetime.json; the tool plan (show, First); routes.md entry versions of 2026-11-18 (--history).

The list First of the plan: every pilot flies them first, each under its
own limit; the five-minute job adds a new once route by itself.

| Mission | Pays once | How |
|---|---|---|
| Signal Fragments | 7,000 cr | from navigation 3 |
| First Hunt (three herds) | 1,000 cr, 50 weapons XP | three grazer kills, `min_creatures` 3 |
| Cracking the Shell | 1,500 cr, 55 weapons XP | after First Hunt (`requires.booked`) |
| Conductive Lattice | 10,893 cr in three links | buys silver and crystal |
| The Collective Provides | 2,500 cr, Voidborn Mastery 25 | Trade's route, 4 at a time; the first link of the Voidborn chain |
| Crystal Resonance, Material Synthesis | 4,000 and 1,500 cr, Voidborn Mastery | Mining's routes, after The Collective Provides |
| Pirate Bounty | 2,000 cr | kill a pirate: topic-pirates.md |

Each turn count the holders of each link (onetime.json): a link another
division writes goes into First once its first runs pay.

### Route Guides
Status: retired. Updated: 2026-11-21. Evidence: migrated from guidebook/military.md section 1.

How each kind of route of this division is flown: the fit and skills
it needs, its place, its steps, what opens and closes it.

### Guard (`guard.py`)
Status: retired. Updated: 2026-11-21. Evidence: migrated from guidebook/military.md section 1.

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
Status: retired. Updated: 2026-11-21. Evidence: migrated from guidebook/military.md section 1.

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
Status: retired. Updated: 2026-11-21. Evidence: migrated from guidebook/military.md section 1.

- A circuit with `requires.stored` and `requires.bid`: a pilot that
  stores curd at the station withdraws only what the bid takes at its
  best price and sells it. The ledger reads storage about every 40
  minutes, so a run may find nothing left after a sale by hand.
- The three curd sales are off since 2026-11-17 16:15 UTC: verdigris curd is held back whole for copper piping
  (surplus.py reserve, 607 of 607; rule F24), and the veil-ray hunts store it (min_bid 5000).

### Pirate hunt (`pirate_test.py`, a skill script, by hand)
Status: retired. Updated: 2026-11-21. Evidence: migrated from guidebook/military.md section 1.

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

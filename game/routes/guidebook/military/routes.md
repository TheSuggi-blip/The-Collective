# Military guidebook -- Routes (routes.md)

### Standing Plan
Status: proven. Updated: 2026-11-22. Evidence: the tool plan (show); hive.py briefing (the plan table, column carries); the tool fill (status, check); hive.py forecast Apophis.

What the 70 ships fly between two turns (orders ENT-059, block APOPHIS):
hunts that pay, combat skills, fits, a group that kills. No guard or escort
in the first ring (F33). Every hunt takes one side, one hunter to a herd.

| Order | Routes | Ships | Why |
|---|---|---|---|
| First | the once line (22 routes), each under its own limit | every ship | rule F35, money paid once |
| Own | far herds and the filler's tests (`fill.py fill <role> --write`); the two weapon fits and their bulwark tests | 1 each | far bids; the fit decision |
| `@hunter` | sales from storage, home hunts, then seven patina-grazer herds beyond the border (templates entry) | 1 each | combat XP where the home herds are full |
| Then | the crafts from own stores, `park` | 6 each | until strict classes give crafts to haulers |

Every hunt carries `gift_to: trader`: with strict classes on, the loot goes
to the trader named at its sell station and the hunt is standing work.
Sized by the briefing's column carries: a herd carries one hunter. What
changes it: a weapon that opens prey of 80 to 100 hull (tests.md), a group
that kills, strict classes (no sales, no crafts for drones), a pirate at a
hunt's place (dispatch closes it; a pack sets it off).

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

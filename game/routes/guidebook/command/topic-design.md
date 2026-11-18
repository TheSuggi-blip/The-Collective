# Command guidebook -- Topic: design (topic-design.md)

### Three Layers, Three Speeds
Status: proven. Updated: 2026-11-17. Evidence: migrated from DESIGN.md section 3.1.

| Layer | Who | Decides | Speed |
|---|---|---|---|
| Strategy | Suggi and Unity | Goals, direction, divisions, what the Collective's resources go to | Hours to days |
| Division command | One Admiral per division, an agent with its own profile | Its ships' plans, routes, fits and tests; its guidebook and report | A turn every four hours (section 6); at once when Suggi or Unity speaks to it |
| Execution | Code: the engine behind its gate, our dispatcher, runners and passes (`BOX.md` 7, 9.3, 9.15) | Every action of every ship, the reflexes, the stops | Every tick of 10 s |

Ships are not agents: six agents command 246 ships. The number of
ships is bounded by credits, the faction's limit, courtesy to the
server and the quality of the code, not by attention.

### Accounts and Names
Status: proven. Updated: 2026-11-17. Evidence: migrated from DESIGN.md section 3.2.

- One account per pilot under Suggi's one website account; the key
  and the registration code are in the engine alone. Exactly one
  program drives a ship at a time: the lock of the divisions and the
  order file (`BOX.md` 9.3).
- A name is `<role word>-<number>`, lower case, the numbers counted up
  and never reused: `miner-`, `trader-`, `hauler-`, `drone-`, `scout-`,
  `sentinel-`; the six flagships carry names of their own. A name is
  permanent, and so is the division it states.
- A new pilot is born only on Suggi's word, in waves, by the birth
  script (skill `fleet-ops`, `references/birth.md`).
- The registry is each member's `FLEET.md`, written from the engine's
  data by `fleetfile.py`, never typed; no credential stands in it.

### Divisions
Status: proven. Updated: 2026-11-17. Evidence: migrated from DESIGN.md section 3.3.

| Division | Admiral | Ships | Job (rule F16) | Hull line (Voidborn; catalog of 2026-11-14) | Today | Aimed for |
|---|---|---|---|---|---|---|
| Command | Unity | six flagships, `sentinel-<n>` (lent) | Leads, keeps the faction, chooses the sites | -- | 26 | 51 |
| Mining | Zero | `miner-<n>` | Mines ore, ice and gas | Threshold (T0), Liminal (T1, ore yield +15 percent), Resonance Miner (T2, cargo 180, +25 percent) | 60 | 100 |
| Trade | Mercury | `trader-<n>` | Trades, sells, buys | Any hull: a market pilot works docked | 40 | 80 |
| Logistics | Apollo | `hauler-<n>` | Hauls, crafts, and builds, supplies and keeps our bases | Fugue (T1 courier, speed 4), Apophenia (T2 freighter, cargo 240), Fold Hauler (T3, cargo 635) | 40 | 80 |
| Military | Apophis | `drone-<n>` | Guards, escorts, fights our wars, hunts | Paradox (T1 fighter, shield 130), Recursion (T2 fighter, speed 4), Gestalt (T3 drone carrier) | 50 | 120 |
| Intel | Oracle | `scout-<n>` | Scouts, explores, hunts | Eigenstate (T1 scout, survey scanner), Absence (T1 shuttle, cloak), Interstice (T2 recon), Solipsism (T4 recon, speed 5) | 30 | 60 |
| All | | | | | 246 | 491 |

- How each class builds its ships and levels: its guidebook's card
  (`game/routes/guidebook/<division>/card.md`, rule F14).
- One faction, The Collective (CLTV), led by the command ship;
  divisions are read from a ship's name, not from a faction role.

### Specialists, Not Allrounders
Status: proven. Updated: 2026-11-17. Evidence: migrated from DESIGN.md section 3.4.

- A pilot has one role for life. An allrounder splits its training
  and carries a fit that is best at nothing. Each division flies
  mostly the work of its own class; what `fill.py` lends across
  divisions is the safety net (rule F32).
- The divisions meet at storage: miners deposit, haulers move and
  make, traders sell. Storage is the buffer that lets five Admirals
  work at different hours without waiting for each other.
- Credits are booked where goods are sold, so a division is not
  judged by its own wallet: the measure is the money of the whole
  fleet per hour and ships at work (rules F19 and F31).
- Sizes follow the pipeline, not equal shares.

### Growth
Status: proven. Updated: 2026-11-17. Evidence: migrated from DESIGN.md section 3.5.

- The fleet we aim for is about 500 ships as the territory is
  explored; outposts come first; each wave is born on Suggi's word
  and is gated on the numbers of the last.
- What the first two waves measured (2026-11-15, 5 and 50 ships): the
  starter missions pay a new pilot about 22,000 cr once (later births
  about 6,000); common ore of the home belts has no buyer, so mining
  them pays nothing; an order book is stale within hours and a gap
  read from an old book is gone on arrival; the first income that
  repeated was creature goods, about 3,000 cr per hunter and hour
  while a herd lasts; a kill's goods lie in its wreck and must be
  looted.

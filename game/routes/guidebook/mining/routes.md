# Mining guidebook -- Routes (routes.md)

### Standing Plan
Status: proven. Updated: 2026-11-23. Evidence: the plan file (tool plan, show); fill.py status miner; pull.py levels; table runs; table fields.

Turn of 2026-11-23 05:43 UTC (orders ENT-076). A free miner takes the list
First, its own routes, then the list Then.

| Route | Ships | For |
|---|---|---|
| fit routes: Laser III and Laser II at Ironlight (Voidborn), Laser II at Sol (Solarian) | by asks | the laser |
| `give-miner-stores-<station>`, any one good | 3 each | stores to the receivers |
| once missions (Voidborn, Confederacy, Frontier, Federation) | by route | paid once per pilot |
| seated rows: GSC-0044 Belt, Forgotten Tailings, Acrux | 10, 5, 3 | iron, copper to faction storage |
| newborn rows first: store-hold at Sol Central or the Grand Exchange | 20 each | a loaded hold stored |
| Solarian rows: Welcome, Copper/Iron at Procyon, then Lacaille, Markab, Nihal, Harborlight and Electra (tests) | 3, 6, 6, 6, 12, 1, 1 | paid once, then the Mining skill |
| Nebula rows: First Cargo, A Word in Private, then Bunda, Khambalia, Alrakis | 8, 5, 3, 18, 14 | paid once, then the Mining skill |
| `@reserve-prism` / `@reserve-hamal` | 1 to 10 each | carbon (Yildun 10), nickel, silicon, quantum fragments; gold closed at its max |
| `@ice-sell` with `gift` | 1 to 2 | ice to Trade, overflow only |
| Then | shared | gives, GSC-0027 seep, Pherkad, Schedar and Hamal copper-iron (4 each), home-sol-central, `train-jumps-miner`, park |

Copper ore is no good of the reserve, so a copper-iron gather stays open
while iron stands full (pull.py): the Mining skill's work before the jump
loop. What would change it: the Harborlight and Electra results; a newborn
seated; Deep Core offered (its gate is not read); a silicon field (all
known fields hold 4,440 together); carbon bought at Node Beta (4 cr) in
place of far gathers; a Resonance Miner bought.

### Drains and carries of stored goods (kind `circuit`)
Status: proven. Updated: 2026-11-21. Evidence: drain-methane-experiment and carry-null-matter-synchrony-nexus (hive.py route <id>).

- Fit: none. Trains Piloting and Trading.
- A drain sells where the goods lie: stop 1 stores the hold, withdraws
  the item and sells it into the bid at `min_price` or more; stop 2
  stores the rest. A carry withdraws a load (`qty`), flies it to the
  bid, sells, stores the rest there.
- Opens only for a pilot that stores the item itself (`requires.stored`,
  sized per pilot) while a book read within the hour shows the bid
  (`requires.bid`); first in every list: what is stored is sold before
  more is mined.

### Ice mine routes (kind `mine`, with `sell`)
Status: proven. Updated: 2026-11-21. Evidence: the ice routes' runs of 2026-11-16 (data/routes/runs.jsonl).

- Fit: Ice Harvester I. Trains Mining and Piloting.
- `mine.py` mines for `minutes`, flies to the station, sells the hold
  then the pilot's storage there into every bid level at the floor or
  more, stores the rest.
- Opens only on `requires.bid` (Central Nexus: an order of 300 units at
  its best price). Count the jumps first: one-jump routes measured 7,280
  to 8,950 per ship-hour, four- and five-jump routes 1,210 to 2,990
  (2026-11-16). Methane comes with the water, 3 to 5 percent of a load.

### Standing work for the reserve (kind `mine`, no `sell`)
Status: proven. Updated: 2026-11-21. Evidence: game/rules/13-not-stated.md; table readings; mine.py commit 0eca38b; the gather runs (hive.py route <id>).

- Fit: Mining Laser I. Trains Mining (one XP a unit mined).
- Mines for `minutes`, stores everything at its station, sells nothing;
  closes below its `min_left` floor and opens when the field grows back,
  never judged on its pay (rule F8). The pull rule (F36) closes it while
  every good it brings stands at its max.
- A run ends docked with its hold stored (mine.py `store_last_load`): a
  partial load aboard closes every `empty_hold` route to the ship.
- Choose a field by jumps to the nearest station of ours first, then
  richness: one jump out gave 191 to 260 ore in 45 minutes, four to
  seven jumps 104 to 224 in 65 to 101 (2026-11-16/17). The far short-ore
  fields run 90 minutes: Gold Crest 325 gold a run, Floodlight Flats
  about 420 ore with a third silicon (2026-11-17).
- The game refills a depleted deposit in proportion to its capacity,
  not to what is left; a full field grows nothing. A floor keeps a stock
  and stops flapping, nothing more (iron 20,000 on 100,000).
- Order each list's fields differently so the division is spread; iron
  comes with copper on every field we read.

### Tests beyond the border (kind `mine`, one good sold)
Status: proven. Updated: 2026-11-21. Evidence: rule F3; table met; fill.py.

- A route maker's test or one of mine: one ship with
  `requires.empty_hold` until its first RESULT line (rule F3). Read the
  pilots met at the place before a lift (table `met`): BUSY combat
  drones fought at Ironhollow and Gliese 876 (2026-11-16). A test of a
  reserve good stores, never sells (rule F24).

### Route Templates
Status: proven. Updated: 2026-11-21. Evidence: game/routes/templates/mining.json; plan.py templates.

A kind of work is a named list of routes in
`game/routes/templates/mining.json` (page
`game/routes/templates-mining.md`); a ship's row names it as `@<name>`.

| Template | For | Trains |
|---|---|---|
| `ice-sell` | stored null matter, methane and ice sold where a bid stands, then the water-ice mine routes on a deep order | Mining, Piloting, Trading |
| `reserve-prism` | make, then gather what the reserve lacks: a loaded hold stored, steel plate of the pilot's own iron, then gold, silicon, nickel, carbon | Mining, Crafting, Refining |
| `reserve-hamal` | the same, the short-ore fields in the other order | the same |

Change one: `plan.py template <name> <routes> --title --trains --note`;
put ships on one: `plan.py set <ships> @ice-sell,@reserve-prism`. A
one-ship test stands in front of a ship's templates as a route of its
own. No list of routes that did not pay (rule F22): ask
`route_earnings`.

# Mining guidebook -- Routes (routes.md)

### Standing Plan
Status: proven. Updated: 2026-11-25. Evidence: the plan file (tool plan, show); fill.py check miner; pull.py levels; table fields; mine_net claims in the route logs; dry runs of score_belt_candidates on read.db; handover.py dry-run of the Bursar-hub gives; requests and queue of 2026-11-25.

Turn of orders ENT-093 (iron by deficit only; iron stored at Bursar hubs
given where a receiver stands; P1: fuel only for work that pays or
levels). A free miner takes First, its own routes, then Then.

| Route | Ships | For |
|---|---|---|
| fit and slot routes, `resonance-parts-*`, gives, once missions | by asks | slots, yard parts, stores, paid once |
| `fit-network` (end of First) | all; skips a fitted ship | lasers and expanders only: no defense loadout |
| `mine-network` (end of First and in Then) | up to 130 | deficits, craft demand, market; else training ore, the shortest way first |
| own rows: `@reserve-prism`, `@reserve-hamal`, empire rows | by the pull | silicon; the rest full |
| Then: gives at Crescent Moon, Ramen's Rest and three Bursar hubs with a trader receiver | 2 each; the hubs within a jump | stored goods to the named receiver |
| Then: iron-copper gathers, regional belts | 1 to 3, at most `carries` | training ore (F8) |
| Then: `train-jumps-miner`; park | 20; - | last |

With every reachable good full, nearly all of the division flies
training ore: iron comes with copper at a belt (the game picks common
ores by richness), so iron by deficit only holds for the network's
deficit claims, not for training. Rule F8 keeps every miner flying (the
comms gate refuses a docked watch for non-scouts); the lever left is the
way to the station, which mine-network's score now ranks right. It
stores only at the 12 stations of deposit_stations; lawless deficit
belts are open, every system the dispatcher's pirate stop closes is
closed, and no escort is asked. The outpost's faction gathers stand off.

What would change it: a raw good the reserve lacks within reach (silicon,
uranium, thorium); a bid with depth for a good we hold; an order or a
rule on miners with no work that pays; Military's escort lane open behind
a power gate (the escort flag as a one-belt test).

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

# Trade guidebook -- the Class Card (card.md)

### Class Card
Status: proven. Updated: 2026-11-22. Evidence: the catalog's tables skills and hulls; table ship_skills; browse_ships 2026-11-21.

The trader's class in short (rule F14): what it flies and what it
levels, in that order. Detail: ships.md and levelling.md; the work and
the plan: routes.md. Sources: the catalog's tables `skills` and `hulls`
(0.732.0), the trader ship files (table `ship_skills`).

The role in the game's words (spacemolt.com/docs/guides/trader and
arbitrage, read 2026-11-22): missions first, then arbitrage, then
crafting; cargo over speed; both ends of a gap read on one side of the
book; thin far books pay most. Trade Run missions pay XP for the hauls
the station names. Full notes: Mercury's knowledge file on order books.

### Ships
Status: proven. Updated: 2026-11-21. Evidence: table hulls; browse_ships (all stations, can_fly) through a docked trader, 2026-11-21 19:55 UTC; Logistics' ships.md.

- Tier 0, every trader: Threshold, cargo 65, speed 1, hull 75; a mining
  laser and a pulse laser.
- Tier 1 asks no Piloting, and other empires' tier-1 freighters stand on
  the ship exchange, flyable by our pilots (`browse_ships` with
  `can_fly`, 2026-11-21 19:55 UTC): Prayer (Outer Rim; cargo 540, speed
  3, hull 40, no shield, no slot) ten times at Ironlight Crossroads at
  5,000 cr; Worship (1,100) and Congregation (1,900, speed 1) 18 to 19
  jumps out. The trader's next hull; the first is tried on one ship
  (go-ironlight-trader, rule F17).
- Tier 2, Piloting 10: Apophenia, the Voidborn freighter, cargo 240.
- Style: dock to dock, never fight, stance flee. A freighter without
  slots cannot mine: it carries and trades.

### Skills
Status: proven. Updated: 2026-11-21. Evidence: table ship_skills 2026-11-21 19:51 UTC; the catalog's table skills; xpsnap.py.

In levelling order. Levels: `SELECT skill, level, COUNT(*) FROM
ship_skills WHERE pilot LIKE 'trader-%' GROUP BY skill, level`
(2026-11-21 19:51 UTC); XP a turn: `xpsnap.py diff` (skill trade-books).

| Skill | Why | Trained by | Now (level:ships) | Goal |
|---|---|---|---|---|
| Trading | the class skill; more of `analyze_market` | buying and selling, about 1 XP per 100 cr bought; mission rewards | 3:5, 2:29, 1:6 | 3 for all |
| Crafting | workshop speed with Refining | `@trade-craft` | 6:16, 5:19, 4:4, 10:1 | 6 |
| Refining | workshop speed; smelting | the smelts of `@trade-craft` | 6:6, 5:14, 4:17, 3:2, 10:1 | 5 |
| Navigation | fuel and jump time, -1% a level | every jump | 6:2, 5:17, 4:21 | 6 |
| Piloting | tier-2 hulls at 10, tier 3 at 20 | flying, jumping | 8:20, 7:20 | 10 |
| Engineering | module CPU and power | crafting components | 0 | later |

Trading lags: it rises by credit volume and the home bids are thin; buys
for the fleet and far trades train it.

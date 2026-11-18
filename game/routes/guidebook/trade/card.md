# Trade guidebook -- the Class Card (card.md)

### Class Card
Status: proven. Updated: 2026-11-17. Evidence: migrated from guidebook/trade.md section Class Card.

The trader's class in short (rule F14); the detail is in section 4
(levelling) and section 5 (ships and fits). Sources: the catalog's
tables `skills` and `hulls` (catalog 0.723.2), the game's page
https://www.spacemolt.com/docs/skills.md (read 2026-11-17 07:37 UTC),
the trader ship files (`xpsnap.py`, 2026-11-17 19:43 UTC).

### Ships
Status: proven. Updated: 2026-11-17. Evidence: migrated from guidebook/trade.md section Class Card.

- Tier 0, every trader now: Threshold, cargo 65, fuel 95, hull 75, a
  mining laser and a pulse laser. Three carry a Gas Harvester I, one a
  Cargo Expander I (hold 85).
- Tier 1 (no Piloting asked): no Voidborn freighter; the largest hold
  is the Residuum's 100 (a salvager). Not worth a change for trade.
- Tier 2, Piloting 10: Apophenia, freighter, cargo 240, fuel 300, hull
  140: the trader's next hull. Tier 3, Piloting 20: Fold Hauler, cargo
  635. No price is in the catalog; not read at a shipyard yet.
- Fit: a Cargo Expander I (+20 hold) for carries; no weapon is needed.
  Default stance flee (game 0.721.0), set by script.
- Style: dock to dock. Sell each pilot's stores where a bid stands,
  carry one or two jumps, craft at a station workshop; never fight.

### Skills
Status: proven. Updated: 2026-11-17. Evidence: migrated from guidebook/trade.md section Class Card.

| Skill | Why it matters | What trains it, on which routes | Trade now | Next goal |
|---|---|---|---|---|
| Trading | The class skill. A higher level shows more in `analyze_market` (regional demand, price trends, arbitrage: the game's help); its bonus is not stated in the catalog | Buying and selling at stations or by exchange orders, XP by credit volume (catalog): `@trade-sell`, station stock bought (about 1 XP per 100 cr), mission rewards | 3 for 5, 2 for 26, 1 for 9 | 3 for every trader |
| Crafting | Station workshop speed from x1 at level 0 to x5 at 100 (with Refining); recipes ask it | Crafting at a station: `@trade-craft` (steel plate and copper wiring from all of the pilot's own iron and copper in one visit, copper piping, Logistics' steel crafts) | 6 for 1, 5 for 8, 4 for 29, 3 for 1, 2 for 1 | 5 for every trader |
| Refining | With Crafting, the workshop's speed; smelting asks it | The smelt inside craft-steel-own, craft-piping and craft-steel | 5 for 1, 4 for 16, 3 for 21, 2 for 2 | 4 for every trader |
| Navigation | Fuel, jump fuel and jump time -1% a level; level 3 opens Signal Fragments (7,000 cr once) | Every jump | 6 for 2, 5 for 14, 4 for 24 | 5 |
| Piloting | Tier 2 hulls at 10 (the Apophenia freighter), tier 3 at 20 | Flying, jumping, mining | 8 for 20, 7 for 19, 6 for 1 | 10 |
| Engineering | Module power and CPU, for a fuller fit | Crafting components or modules | 0 | not a goal yet |
| Mining | The fallback only (rule F23) | `@trade-gas`, `@trade-gather`, named by no ship since 2026-11-17 23:42 UTC | -- | -- |

Levels: the trader ship files, 2026-11-17 23:35 UTC (`xpsnap.py save`). XP of the 40 traders
(`xpsnap.py diff`, skill trade-books), four hours each: to 07:37 UTC
crafting 0 and trading 616; 07:37 to 11:41 UTC crafting 3,490, trading
455; 11:41 to 15:37 UTC crafting 10,775, trading 527; 15:37 to 19:43 UTC
deep core mining 34,542, mining 32,581, piloting 32,136, crafting 15,630,
navigation 11,557, refining 8,500, trading 379; 19:43 to 23:35 UTC
piloting 27,151, deep core mining 25,068, crafting 24,445, mining 23,796,
refining 17,350, navigation 10,909, trading 2,164. Every trader gained XP
in each window; crafting stands at 4 or more for 38 of 40. Trading is the
skill that lags: it rises only by credit volume, and the bids carry few
ships. Voidborn Mastery: level 1 for 14 traders, 0 for 26.

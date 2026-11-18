# Trade guidebook -- Levelling (levelling.md)

### Levelling Guide
Status: proven. Updated: 2026-11-17. Evidence: migrated from guidebook/trade.md section 4.

Which skills a ship of this division levels and on which work (rule
F23): the work of its own role first, gathering ore only when none is
open. The levels below are the traders' at 2026-11-17 03:40 UTC (the
table `ship_skills`): trading 2 for 24 ships, 1 for 16; navigation 5
for 1, 4 for 3, 3 for 35, 2 for 1; piloting 7 for 3, 6 for 17, 4 for
19, 3 for 1; crafting 0 for all, 8 of them with XP. The XP of all 40
traders by skill: deep core mining 29,522, piloting 24,111, mining
16,363, navigation 10,687, exploration 4,970, trading 2,753, crafting
120: the standing work trains more than the trade does. At 00:07 UTC
the same table read navigation 2 for 20 traders and crafting XP for 3.

| Kind of ship | Skills it levels | On which work (template) | What the next level opens |
|---|---|---|---|
| A trader born 2026-11-16 evening (navigation 2, trading 0 to 1, piloting 2 to 3) | navigation, then trading | `@trade-train-nav` until navigation 3, `@trade-sell` and `@trade-craft` whenever its own stores and a bid allow | Navigation 3 opens Signal Fragments, 7,000 cr once |
| A trader of the first twenty (navigation 3 to 4, trading 2, piloting 5 to 7) | trading, crafting | `@trade-sell`, `@trade-craft` | Piloting 10 opens the tier-2 hulls; no route trains it faster than flying does |
| A trader with a Gas Harvester I | mining, trading | `@trade-gas`, then the two above | -- |

What raises each skill, as read:

- Trading: a buy gives about 1 XP per 100 cr (24,441 iron ore bought
  for 24,441 cr gave 244 XP, 2026-11-16 18:46 UTC); the 75 silicon ore
  bought for 31,814 cr took its buyer from trading 1 to 2 (159 XP into
  level 2 at 00:07 UTC). Mission rewards give it too: the Node Beta
  chain gives 45 + 30 + 25 (section 3). What a market sale gives is
  not measured.
- Crafting: one hand craft of a focused crystal gave 10 XP
  (2026-11-16 23:50 UTC). A craft's speed grows with the skill and it
  runs only while the pilot stays docked at the workshop (the game's
  `craft` help, 2026-11-15).
- Navigation: about 4 XP a jump on the training loop; level 3 at 340
  XP. The six born traders read at 23:40 UTC stood at 144 to 241 XP.
- Piloting 10, which opens the tier-2 hulls, was about 116 hours away
  at the division's median of 109 piloting XP an hour (`hive.py
  levels`, 2026-11-16 03:25 UTC).

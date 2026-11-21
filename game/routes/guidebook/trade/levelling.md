# Trade guidebook -- Levelling (levelling.md)

### Levelling Guide
Status: proven. Updated: 2026-11-21. Evidence: table ship_skills 2026-11-21; xpsnap.py diff of the turns of 2026-11-17; runs.jsonl.

Which skills a trader levels and on which work (rule F23).

| Kind of ship | Levels | On which work | What the next level opens |
|---|---|---|---|
| A trader under navigation 3 | navigation | `@trade-train-nav` | Signal Fragments, 7,000 cr once |
| Every trader now (navigation 4 to 6, trading 1 to 3, piloting 7 to 8) | trading, crafting, refining | `@trade-sell`, `@trade-craft`, the tests beyond the border | Piloting 10: the Apophenia |
| A trader in a freighter | trading, piloting, navigation | carries beyond the border | -- |

What raises each skill, as read:

- Trading: a buy gives about 1 XP per 100 cr (24,441 iron ore bought for
  24,441 cr gave 244 XP, 2026-11-16 18:46 UTC); mission rewards too (the
  Node Beta chain 45 + 30 + 25). What a sale gives: not measured.
- Crafting: a wiring run about 13.5 XP (craft-wiring-synchrony-hub,
  2026-11-17 19:47 UTC); the 40 traders gained 24,445 crafting XP in the
  four hours to 2026-11-17 23:35 UTC on `@trade-craft`.
- Navigation: about 4 XP a jump; level 3 at 340 XP.
- Piloting: flying and jumping; the hours to the next tier: `hive.py
  levels` (the tool fleet, view=levels).

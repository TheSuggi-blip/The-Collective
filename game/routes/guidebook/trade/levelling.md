# Trade guidebook -- Levelling (levelling.md)

### Levelling Guide
Status: proven. Updated: 2026-11-22. Evidence: table ship_skills; xpsnap.py diff of 2026-11-17; data/missions/*.json rewards (2026-11-22 03:4x UTC).

Which skills a trader levels and on which work (rule F23).

| Kind of ship | Levels | On which work | What the next level opens |
|---|---|---|---|
| A trader under navigation 3 | navigation | `@trade-train-nav` | Signal Fragments, 7,000 cr once |
| Every trader now (navigation 4 to 6, trading 1 to 3, piloting 7 to 9) | trading, piloting, navigation | `@trade-sell`, the far tests, Trade Runs, `train-jumps-trader` when nothing else is open | Piloting 10: the Apophenia |
| A trader in a freighter | trading, piloting, navigation | carries beyond the border | -- |

What raises each skill, as read:

- Trading: about 1 XP per 100 cr of goods bought and as much again per
  100 cr sold (one Trade Run: 30,411 bought and 30,170 sold for 637 XP
  with the mission's 35, level 3 to 4, xpsnap.py diff 2026-11-22 04:2x
  UTC; 24,441 cr of iron ore bought gave 244 XP, 2026-11-16); missions: a
  Trade Run 20 to 40, Network Commerce Protocol 20. A dear good bought
  and sold near one price trains it cheapest.
- Piloting: flying and jumping, and missions: a Trade Run 80 to 580,
  Local Sector Survey 280, Deep Space Cartography 380. A mission's XP by
  skill stands in its board file: `rewards.skill_xp` and `piloting_xp`.
- Crafting: a wiring run about 13.5 XP (craft-wiring-synchrony-hub).
- Navigation: about 4 XP a jump; level 3 at 340 XP.

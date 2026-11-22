# Command guidebook -- Levelling (levelling.md)

### Command Skills and Fleet Tier Readiness
Status: proven. Updated: 2026-11-22. Evidence: rule F10; rule F23; view hull_readiness; view division_playbooks; hive.py levels Unity.

| Skill | Role in Command | How it trains | Live tracking |
|---|---|---|---|
| Piloting | Unlocks Tier 2 hulls at 10, Tier 3 at 20 across every division | Productive travel, mining, combat, missions | `SELECT * FROM hull_readiness` |
| Leadership | Command group bonuses (rule F10) | Leading group operations and missions | `hive.py levels Unity` |
| Tactics | Fleet combat coordination | Combat engagements and patrol support | `hive.py stats xp --member Unity` |
| Navigation | -1% jump fuel and jump time per level | Productive carries and inspections | `hive.py guide command` |

- Fleet-wide rule (F22, F23): pilots train Piloting and class skills on
  productive, fuel-positive or zero-fuel docked work (crafting, Bursar
  books, resource carries) rather than burning fuel on empty jump loops.

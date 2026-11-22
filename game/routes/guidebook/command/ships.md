# Command guidebook -- Ships and Fits (ships.md)

### Command Flagships and Founding Hulls
Status: proven. Updated: 2026-11-22. Evidence: rule F10; rule F33; table ships; view hull_readiness; hive.py stats upgrades --member Unity.

- Unity's flagship leads the faction (CLTV), holds the office deeds and
  executes base founding and facility upgrades once stock covers the
  open need in `game/needs.tsv` (rule F33).
- Live hull classes, fitted modules, Piloting readiness for Tier 2+,
  and empty slots are computed automatically by the Live Division Anchor
  (`hive.py guide command`, SQL view `division_playbooks`, and
  `hive.py stats upgrades --member Unity`) rather than copied here as
  static counts.
- Flagship fit priority: survivability (shield/defense) and range
  (fuel/navigation) first when inspecting frontier outpost candidates or
  station sites; group combat modules when leading the command group.

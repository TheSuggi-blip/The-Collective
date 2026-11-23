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

### Multi-Empire Ship Catalog (All 5 Fleet Empires + Neutral)
Status: proven. Updated: 2026-11-23. Evidence: table hulls; game/catalog/ships/*.md; hive.py guide command.

Command flies flagships across all five empires (Voidborn, Solarian, Nebula, Outer Rim, Crimson) and oversees cross-empire commissioning (`game/catalog/master-index.md` -> `game/catalog/ships/<empire>.md`):

| Empire | Catalog File | T0 Starter (hold / fuel / slots) | Standout T1 / T2 Fleet Hulls |
|---|---|---|---|
| Voidborn | `game/catalog/ships/voidborn.md` | Threshold (65c / 95f / 1W 2D 2U) | T1 Liminal, Qualia, Vigil; T2 Resonance Miner, Recursion, Apophenia, Confluence |
| Solarian | `game/catalog/ships/solarian.md` | Theoria (70c / 100f / 1W 1D 3U) | T1 Archimedes (4U miner), Axiom; T2 Excavation, Meridian Freighter, Theorem, Hypothesis |
| Nebula | `game/catalog/ships/nebula.md` | Prospect (100c / 130f / 1W 1D 2U) | T1 Bonanza (180c miner), Floor Price (400c), Venture; T2 Motherlode, Caravan (540c), Prospectus |
| Crimson | `game/catalog/ships/crimson.md` | Shard (60c / 90f / 2W 1D 1U) | T1 Cleaver (3W), Flail, Mandate; T2 Halberd (4W), Broadaxe (4W), War Wagon (1,200c/8U) |
| Outer Rim | `game/catalog/ships/outerrim.md` | Cobble (75c / 120f / 1W 1D 2U) | T1 Prayer (540c), Worship (1,100c), Congregation (1,900c), Warranty Void; T2 Junk Convoy (850c/6U), Dust Devil |
| Neutral | `game/catalog/ships/pirate-and-other.md` | Secondhand exchange (`browse_ships`) | T1 Ledger (480c), Runner (120c); T2 Workhorse (300c/4U), Lone Star (240c) |

- Every division's Live Anchor (`hive.py guide <division>`) auto-surfaces its active empires' hull ladders directly from `read.db`.

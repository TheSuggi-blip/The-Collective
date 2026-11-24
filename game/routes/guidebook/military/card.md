# Military guidebook -- the Class Card (card.md)

### Class Card
Status: proven. Updated: 2026-11-24. Evidence: governance/strategy.md (v2.5); hive.py upgrades military; read.db tables hulls, ship_listings; MISSION.md.

Military is the fleet's Combat & Security Center across three birth
empires (Voidborn, Crimson, Solarian; live counts in `hive.py upgrades
military`) plus `sentinel-` Royal Guard ships lent until Piloting 20
(rule F10). Core mandate: protect sovereign stations & industrial
lines, fan across PvE herds (`1-2/herd`, 2 left, F9/F38), farm NPC
pirate packs in focused 5-8 ship formations (F27), hold defensive RoE
(F2: never fire first at players/empires), and gift combat loot inward
to Trade/Logistics (P5).

### Ships
Status: proven. Updated: 2026-11-24. Evidence: read.db tables hulls, ship_listings; game/rules/05-galaxy.md; game/fleet/upgrades.py.

- Cross-empire rule (`05-galaxy.md`): flying another empire's hull
  carries **zero penalty** and keeps the pilot's native empire bonus
  (a Voidborn pilot in a Crimson `Broadaxe` keeps +12% shields &
  Voidborn Mastery!). Always pick the best combat hull by role and let
  `upgrades.py queue add` auto-buy cheaper listed ships via
  `ship_listings` (instant delivery, 37-90% below commission).
- Tier 0 starters: Voidborn Threshold (1W/2D/2U), Crimson Shard
  (2W/1D/1U, armor 8), Solarian Theoria (1W/1D/3U). Strip starter
  Mining Laser I (`strip-mining-laser-*`).
- Tier 1 (Piloting 0): Crimson `Cleaver` (3W, 156H), Voidborn
  `Paradox` (2W/2D, 130S), Solarian `Axiom` (2W/1D/2U).
- Tier 2 (Piloting 10): Crimson `Broadaxe` (4W/1D/2U, ~37k listed!)
  & `Halberd` (4W/2D, 339H) for peak DPS; Voidborn `Recursion`
  (3W/2D/2U, spd 4, 150S); Solarian `Theorem` (3W/2D/3U); Crimson
  `Trebuchet` (850H/6D) for tanking.
- Tier 3 (Piloting 20): Solarian `Dialectic` (5W/3D/3U, 520H/280S --
  galactic PvE meta), Crimson `Warmaul` (5W, 680H), Voidborn
  `Annihilation` (4W/4D, 430S), Solarian `Quorum` (4W/3D/4U).
- Fit order: `pulse_laser_iii` first, then `shield_booster_ii/iv` or
  `armor_plate_iii` (watch armor speed penalty). Flee <60% hull.

### Skills
Status: proven. Updated: 2026-11-24. Evidence: catalog table skills; hive.py levels Apophis; hive.py stats xp --member Apophis.

| Skill | Why | What trains it | Next goal |
|---|---|---|---|
| Gunnery, Weapons, Tactics | +1% damage, crit, accuracy/level | firing and kills on every hunt | 6 / 4 / 5+ |
| Xenobiology | +1% molt loot value/level | wildlife kills by tier | 5+ |
| Piloting | T2 at 10, T3 at 20 | flying, fights, missions | 10->20 |
| Empire Mastery (F35) | Voidborn Mastery / Crimson Fury / Solarian Doctrine | own-empire missions (list First) | 1+ |
| Navigation | -1% jump fuel and time/level | far hunts & patrols | 5+ |
| Shields, Armor | tank capacity & resistance | taking hits in combat | 2+ |
| Leadership | fleet group capacity | leading pirate/escort formations | groups |

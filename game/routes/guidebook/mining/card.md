# Mining guidebook -- the Class Card (card.md)

### Class Card
Status: proven. Updated: 2026-11-24. Evidence: governance/strategy.md (v2.5); governance/collective-strategy.md; read.db tables hulls, fields, ship_listings; hive.py levels Zero.

Mining is the fleet's Production Center across three birth empires
(Voidborn, Solarian, Nebula; live counts in `hive.py upgrades mining`).
Core mandate under G4/O3/F23: extract raw ores, ices, and gases into
storage for our manufacturing & reserve chains (`needs.tsv`,
`reserve.tsv`) and high-margin scarce veins (`<=3` ships/belt, `15%`
default `min_left` floor for a 6h buffer; `>=25%` belts for T2/T3
multi-laser rigs to clear the `07-economy.md` sparse-deposit cliff).
Dynamic network: `mine-network` (`game/mine-policy.json`) auto-rotates across unsaturated belts (`>=15%` live floor + instant cooldown, tool-matched, reserve-deficit prioritized, skipping full reserves). Hulls: ships.md; routes: routes.md; calls: topic-scripts.md.

### Ships
Status: proven. Updated: 2026-11-24. Evidence: read.db tables hulls, ship_listings; game/rules/05-galaxy.md; game/fleet/upgrades.py.

- Cross-empire rule (`05-galaxy.md`): flying another empire's hull
  carries **zero penalty** and keeps the pilot's native empire bonus.
  Standardize best hulls by job across all empires; `upgrades.py queue
  add` auto-buys cheaper listed hulls via `ship_listings`.
- Tier 0 starters: Voidborn Threshold (65c, 2U), Solarian Theoria
  (70c, 3U), Nebula Prospect (100c, 2U). Strip starter Pulse Laser I.
- Tier 1 (Piloting 0 -- instant skip): Nebula `Bonanza` (180c with
  half-volume ore compression = ~360 eff. ore, 3U, ~20k listed!),
  Solarian `Archimedes` (80c compressed, 4U), Voidborn `Liminal` (75c
  compressed, 3U).
- Tier 2 (Piloting 10): `Resonance Miner` (Voidborn, 180c, 4U, 160S),
  `Motherlode` (Nebula, 200c, 3U), `Excavation` (Solarian, 200c, 3U);
  ice/gas hulls (`Cold Storage`, `Brain Freeze`, `Hoarfrost`).
- Tier 3+ ladder: `Praxis` (Solarian, 360c, 7U), `Bonanza King`
  (Nebula, 600c, 6U), `Substrate` (Voidborn, 240c, 6U); T5 capitals
  `Tellurian`/`Manifold` (+40% ore yield, 40% volume compression).
- Fit: `mining_laser_iii/iv` (or `ii` where dear), ice/gas harvesters,
  `cargo_expander_ii/iii`. Default stance flee; `<=3/belt`.

### Skills
Status: proven. Updated: 2026-11-24. Evidence: catalog table skills; hive.py levels Zero; hive.py stats xp --member Zero.

| Skill | Why it matters | What trains it | Next goal |
|---|---|---|---|
| Mining | +1% yield/level; richer ore pulls | 1 XP/unit mined; mining missions | 10+ all |
| Deep Core Mining | +5%/level on deep core deposits | mining with power >=3 lasers | 10+ |
| Piloting | T2 at 10, T3 at 20 (P0 hulls skip wait) | flying, jumps, missions | 10->20 |
| Empire Mastery (F35) | Voidborn Mastery / Solarian Doctrine / Nebula Attunement | own-empire missions (list First) | 2+ |
| Navigation | -1% fuel and jump time/level | gather shuttles | 6+ |
| Refining, Crafting | reserve processing when needed | docked smelt/craft routes | 5+ |

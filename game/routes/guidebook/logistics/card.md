# Logistics guidebook -- the Class Card (card.md)

### Class Card
Status: proven. Updated: 2026-11-21. Evidence: catalog tables skills, hulls, facilities (catalog 0.723.2); the help of spacemolt_facility; table ship_skills; orders.log ENT-056.

The hauler's class in short (rule F14): it carries, crafts and builds; gathering is Mining's (rule F23). Levels: the tool fleet, view=levels, member Apollo; XP per ship-hour: hive.py stats xp. Hulls: ships.md; work: routes.md; bases: topic-bases.md.

### Ships
Status: proven. Updated: 2026-11-21. Evidence: table hulls; browse_ships 2026-11-17 00:23 UTC; table faction_members 2026-11-17; ships.md.

- Tier 0, every hauler: Threshold (cargo 65, fuel 95, hull 75), a mining laser, a pulse laser.
- Tier 1, no Piloting asked: Ledger (no empire, cargo 480, hull 150, shield 70, speed 4) is the next hull, for it holds and survives; no listing or quote of it read. Prayer (540, no shield) and Congregation (1,900, speed 1) are Outer Rim hulls on the exchange. No slot: they haul only. None tested.
- Tier 2, Piloting 10: Apophenia, the Voidborn freighter (cargo 240, shield 145, fuel 300).
- Fit: hold first (Cargo Expander I, +20). Stance flee. Only a faction member docks at our outpost.
- Style: dock to dock, every leg with cargo; craft where the goods lie; build where the Fleet Admiral chooses; never fight.

### Skills
Status: proven. Updated: 2026-11-21. Evidence: catalog table skills; table ship_skills; queue.log ENT-159; the tool fleet view=levels.

| Skill | Why | What trains it | Next goal |
|---|---|---|---|
| Crafting, Refining | workshop speed x1 at 0 to x5 at 100 (the higher of the two); not facility jobs | `@craft-reserve`, `craft-boards-*`, the Workshop Production Run | 5; 6 on the builder |
| Corporation Management | a tier N faction facility asks its builder for N (tier 1 none); a station of our own | each faction build or upgrade (Lockbox 0 to 3, Hiring Board to 4, Desk to 5) | 6 on the builder |
| Navigation | -1% fuel, jump fuel and jump time a level | every jump: carries, supply and kit runs | 5 |
| Piloting | tier 2 hulls at 10, tier 3 at 20 | flying; 20 XP a board mission | 10 |
| Voidborn Mastery | our empire's skill (rule F35) | Voidborn missions only (list First) | 1 |
| Engineering | module power and CPU -1% a level | crafting components, modules | 2 on the builder |
| Trading | sales of stored goods | `@stored-goods` | 3 |
| Mining, Deep Core Mining | not the hauler's work: gathering is Mining's alone (rule F23) | -- | not a goal |

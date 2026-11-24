# Intel guidebook -- the Class Card (card.md)

### Class Card
Status: proven. Updated: 2026-11-24. Evidence: governance/strategy.md (v2.5); read.db tables hulls, ship_listings; hive.py levels Oracle; MISSION.md.

Intel is the fleet's Recon & Diplomatic Cost Center across three birth
empires (Voidborn, Outer Rim, Nebula; live counts in `hive.py upgrades
intel`). Core mandate: keep galaxy market books, resource fields,
wildlife herds, rival bases, and wormholes `<3h` fresh in `read.db`
(alongside `ledger.py`'s automatic 15-min `ship_listings` scan), track
rival surges (`rivals.py`), and run Phase-1 diplomatic hails & scout
envoys behind `comms_guard.py` / `diplomacy.py` (F4, O10).

### Ships
Status: proven. Updated: 2026-11-24. Evidence: read.db tables hulls, ship_listings; game/rules/05-galaxy.md; tests.md.

- Cross-empire rule (`05-galaxy.md`): flying another empire's hull
  carries **zero penalty** and keeps the pilot's native empire bonus.
  Judge every scout hull by **fuel per read and speed** (`tests.md`),
  buying listed bargains via `ship_listings` / `upgrades.py` when ROI
  clears.
- Tier 0 starters: Voidborn Threshold (65c, 2U), Outer Rim Cobble,
  Nebula Prospect. Keep starter Mining Laser I only while own-empire
  mining storylines remain open (F35), then strip & gift to Mining.
- Tier 1 (Piloting 0): Crimson `Crimson Stiletto` (spd 6, 2U),
  Solarian `Lemma` (spd 5, 3U), Outer Rim `Warranty Void` (spd 5),
  Nebula `Venture` (80c). (Note: `Qualia` failed fuel test in tests.md.)
- Tier 2 (Piloting 10): Nebula `Prospectus` (spd 5, 80c, 3U),
  Voidborn `Confluence` (120c, 4U), Solarian `Empirica` (125c, 5U).
- Tier 3 (Piloting 20): Nebula `Survey Vessel` (305c, 5U), Solarian
  `Perigee` (270c, 6U), Voidborn `Noumenon` (215c, 5U).
- Fit: `survey_scanner_ii` (every system surveyed on census), Mining
  Survey Probe for faint signatures, `shield_booster_ii`. Empty hold
  beyond the border (F3), never fire first (F2).
- AutoNet feeder (ENT-088): keep `<6h` market books across `60+` safe empire & neutral hubs (feeds `bursar-network` & `haul-network`) and `<3h` `ship_listings` at major shipyards (feeds `upgrades.py` auto-buy); tracked live on `scorecard.py` `AutoNet`.

### Skills
Status: proven. Updated: 2026-11-24. Evidence: catalog table skills; hive.py levels Oracle; table ship_skills.

| Skill | Why | What trains it | Next goal |
|---|---|---|---|
| Exploration | +1% survey power/level | first visits to new systems | median 4+ |
| Navigation | -1% fuel and jump time/level | census jump loops | median 7+ |
| Piloting | hull tiers 10/20/30/50 | routes and missions | 10+ |
| Scanning | +1% scanner effect/level | `survey_system` with scanner fitted | 2+ |
| Empire Mastery (F35) | Voidborn Mastery / Outer Rim Survival / Nebula Attunement | own-empire missions (list First) | 1+ |

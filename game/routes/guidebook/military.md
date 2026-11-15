---
name: guidebook-military
id: 20261115T205807Z
tier: intel
author: Unity
links:
  - The-Collective:game/routes/BLUEPRINT.md
---

# military.md -- Guidebook of the Military Division

Kept by Apophis; read by every member. What the Military division
learned about its routes, its levelling and its ships, so that every
ship born later starts where the others stand. Started by the Fleet
Admiral on 2026-11-15 from the runs so far; from here Apophis writes it,
at the end of every turn.

- A figure comes from `python3 -B game/fleet/routes.py measure` or from a
  run's RESULT line, and carries its date. A number no record holds is
  written `not measured`.
- The plan in force is `game/routes/plans/drone.json`; every route
  with its figure is in `game/routes/index.md`.

## 1. Routes That Pay

| Route | Credits per ship-hour, after all costs | Date | Note |
|---|---|---|---|
| `hunt-gsc-veil-ray` | 3,620 over 16 runs, 24 min a run, 1,620 cr a run (`routes.py measure`) | 2026-11-15 23:58 UTC | 69 kills in 430 hunter-minutes, one run without a kill (the railgun ship out of ammunition). One hunter, ranched: no hunt below four animals, four kills a run. The herd read 6 to 7 from 17:58 to 20:02 UTC, 16 to 18 from 21:58 to 23:06 and 12 at 23:39 UTC while it was hunted (`data/wildlife/history.jsonl`). Trains Weapons and Xenobiology |
| `hunt-hamal-veil-ray` | 2,890 over 10 runs, 27 min a run, 1,150 cr a run (`routes.py measure`) | 2026-11-15 23:58 UTC | 2 of 10 runs without a kill. The herd read 16 at 21:59, 11 at 23:07 and 0 at 23:41 UTC, with 1 to 4 pilots at the place at every read: other players hunt it too. Our run of 23:25 UTC made 2 kills and got 1 carapace, -91 cr |

Both sell verdigris curd at Central Nexus: 330 cr a unit in every sale
of the turn (`runs.jsonl`, `sold`).

## 2. What Did Not Pay

| Route or test | What was measured | Date | Why, and what follows |
|---|---|---|---|
| `hunt-acubens-urchin` | 3 runs, 6 kills, -240 cr per ship-hour | 2026-11-15 | No radiant bile dropped, carapace only. Off |
| `hunt-home-drift-ray` | 11 runs, -260 cr per ship-hour | 2026-11-15 | Crystallized biogas bid 1 to 2 cr. Out of the plan (orders F8) |
| A pilot-whale (220 hull) | Took a starter with a railgun from 73 to 15 hull in one fight | 2026-11-15 | Not for a starter hull with no defence module (orders F9) |
| Piercing Railgun I on veil-rays (`hunt-gsc-veil-ray`, 21:55 to 22:54 UTC) | 3 runs: 4, 4 and 0 kills; the two trips with 4 kills took 21.4 and 24.0 min, the eight pulse-laser trips with 4 kills at the same place 21.7 to 26.8 min (18:20 to 21:28 UTC); +1,915, +1,915 and -65 cr | 2026-11-15 | No gain measured, and the weapon needs ammunition: 8 slug cases bought for 320 cr ran out in the third run, which fled at once. The hunters keep the Pulse Laser I. No hunt route takes a ship with a railgun (`requires.without_module`) until it carries ammunition |
| Yield test: bell-jellies at Nexus Prime Stellar Siphon | 1 run, 2 kills in 6 min at the place, -26 cr | 2026-11-15 23:29 UTC | Drop: 3 crystallized biogas, 1 levity bladder; both bid 1 to 2 cr. Off |
| Yield test: rime-grazers and pressblisters at Node Gamma Ice Belt | 1 run, 3 kills in 16.8 min, -60 cr a run (`routes.py measure`) | 2026-11-15 23:29 UTC | Drop: 3 creature carapace, 2 nitrogen bladder; both bid 1 to 2 cr. Off |
| Yield test: deuteron-slugs at Node Beta Frozen Drift | 1 run, 2 kills in 23.3 min, no goods recorded, -33 cr | 2026-11-15 23:29 UTC | Off |
| `hunt-ruchbah-veil-ray` by hand, hold empty | 1 run: 0 kills, -77 cr, two ships of a faction of 1,249 members joined the fight within three minutes | 2026-11-15 21:26 UTC | The first run of the route (below, section 6) found nobody there |

## 3. Missions That Pay Once

The `once` routes at the head of the plan: every pilot flies them
first. Measured by `routes.py measure`, 2026-11-15 23:58 UTC, all runs of
the fleet:

| Route | Pays once | Measured | Note |
|---|---|---|---|
| `voidborn-precedence` | 4,000 cr | 41 runs, 15 min, 3,890 cr a run | Accept at Node Beta, two docks, nothing bought. Drones from 23:40 UTC |
| `voidborn-first-hunt-nexus`, `-gsc`, `-acubens` | 1,000 cr, 50 Weapons XP, 15 Xenobiology XP, 20 Piloting XP | 1 run each: 970, 930 and 940 cr; 19, 26 and 28 min | The circuit runner's `hunt` step: accept, three belt-grazer kills, hand in. One hunter per herd, so the fleet's pilots queue for three herds |
| `voidborn-first-hunt-schedar` | the same | not measured | A fourth herd one jump beyond GSC-0027 (20 belt-grazers, no pilot, 21:14 UTC), `alone` and an empty hold; a test from 2026-11-15 23:58 UTC |
| `voidborn-selling` | 1,000 cr for the pilots that hold Market Participation: Selling | 40 runs, 5 min, 870 cr a run | 20 drones held the mission (`data/fleet/ships/`, 23:46 UTC) |
| `voidborn-concurrent` | 3,000 cr | every drone has it booked | Flown by all 30 drones on 2026-11-15 |

Belt-grazer goods are creature carapace and raw xeno meat; no station of
ours bids above 1 cr for either. The mission is the pay.

## 4. Levelling

- Piloting opens the hulls: tier 2 needs Piloting 10. The drones stand
  at Piloting 3 (20 drones), 4 (8) and 5 (2) (`data/fleet/ships/`,
  2026-11-15 23:35 UTC). The catalog's XP per level: 900 for level 4 to 5,
  then 1,285, 1,740, 2,265, 2,860 and 3,525 for level 9 to 10. What a hunt
  gives in Piloting is not measured; First Hunt gives 20.
- Weapons stand at 0 to 2, Gunnery at 0 to 3, Tactics at 0 to 3 and
  Xenobiology at 0 to 3 on the eight drones that have hunted; the other
  drones carry none of these skills (same read). First Hunt gives 50
  Weapons XP; what a kill gives is not measured.
- The tier-1 hulls name no Piloting gate: the game's quote for a Vigil
  said "shipyard tier 0 required" (section 5).

## 5. Ships and Fits

The starter Threshold: 1 weapon, 2 defence and 2 utility slots, CPU 16,
power 30 (`get_ship`, 2026-11-15 21:27 UTC). Every drone fits a Mining
Laser I and a Pulse Laser I but one, which fits a Piercing Railgun I; no
drone fits a defence module (`data/fleet/ships/`, 23:35 UTC).

| Module or item | What it does | Price in our books |
|---|---|---|
| Piercing Railgun I | 60 kinetic damage, magazine 7, cooldown 3 ticks, 70% armour bypass | 5,000 cr (Central Nexus, 3) |
| Ferrous Slug Case | Railgun ammunition; one case loads a whole magazine. Recipe: 2 steel plate and 3 iron ore make 5 cases | 52 cr (Central Nexus, 744) |
| Tungsten Slug Case | Railgun ammunition, +40% armour bypass | 40 cr (Central Nexus, 3) |
| Shield Booster I | +25 shield, 2 CPU, 4 power | 2,483 cr (Central Nexus, 26) |
| Pulse Laser I | The starter weapon | 1,385 cr (Central Nexus, 5) |

Catalog and books read 2026-11-15 23:24 to 23:32 UTC.

- A railgun hit does not kill a 60-hull grazer: the first hit leaves it
  at 4 to 8 hull and it flees (hunt logs of 21:30 and 22:52 UTC). On
  veil-rays it was no faster than the pulse laser (section 2).
- Hulls, priced by the game (`commission_quote` at Central Nexus, read
  only, 2026-11-15 23:30 to 23:32 UTC):

| Hull | Tier | Credits only | Credits plus materials | Materials |
|---|---|---|---|---|
| Vigil | 1 | 106,208 cr | 15,040 cr | 8 steel plate, 15 copper wiring, 14 silicate composite, 5 shield emitter, 3 thruster nozzle, 2 sensor array, 2 Pulse Laser I, 2 Shield Booster I |
| Paradox | 1 | 82,690 cr | 12,368 cr | 15 silicate composite, 10 copper wiring, 1 processing core, 2 shield emitter, 4 void nanite suspension, 5 shield matrix, 1 phase matrix, 2 Pulse Laser I, 1 Shield Booster I, 1 Shield Recharger I |

- The exchange lists ships too: `browse_ships` showed 259 listings at the
  stations our pilots have charted, tier-1 hulls from 1,000 cr, all at
  stations of other empires (2026-11-15 23:31 UTC).
- The division flies the Threshold with the Pulse Laser I this week. A
  hunt is bounded by the herd and by other hunters, not by the weapon
  (sections 1 and 2): a hull that kills faster earns more only where a
  herd grows under our ranch. What a Vigil would earn is not measured.

## 6. Open Tests

Every test is one ship, in `game/routes/plans/drone.json`, started
2026-11-15 23:29 UTC:

- Veil-rays beyond our border (`alone`, empty hold): Ruchbah 4 kills,
  +1,243 cr in 25.1 min, no damage, nobody at the place; Garnet and Okab
  left without a fight within minutes, a pilot not of ours at the place,
  -99 cr each; Cedarhold, Achird and Keid had no RESULT line at 23:58 UTC.
  A place rests 30 minutes after a run without a kill.
- Yield tests in our space: patina-grazers at Acubens Shadow Pocket left
  at once, a pilot not of ours at the place (-60 cr); kiln-snails at
  Eltanin Prime Belt had no RESULT line at 23:58 UTC.
- The railgun ship: ammunition from stored iron, then armoured prey of
  100 hull or less.
- A tier-1 hull with two weapons against a home herd, after its cost is
  weighed against the herd's growth.

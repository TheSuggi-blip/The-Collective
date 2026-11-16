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

## Standing Plan

What the drones fly between two turns, in this order (`game/routes/plans/drone.json`,
last committed 2026-11-16 03:25 UTC; `hive.py standing` prints it ship by ship). Every
place holds one hunter (orders F9); every route beyond the border carries `alone`
and an empty hold (F13). Figures: `routes.py measure`, 2026-11-16 03:19 UTC,
credits per ship-hour after fuel, beside the scale of the hour: the best route of
the fleet, mine-ruchbah-ice-belt at 8,271, and 0 for a ship that waits (`hive.py tasks`).

| Order | Routes | Ships | Expected | Why |
|---|---|---|---|---|
| 1 | `voidborn-precedence` | up to 40 | 4,000 cr once per pilot | Every drone has it booked; it passes by itself |
| 2 | First Hunt: `voidborn-first-hunt-nexus`, `-gsc`, `-acubens` (home), `-ironhollow-echo`, `-ironhollow-fading`, `-achernar` (one jump from The Experiment) | 1 each, 6 | 1,000 cr once; 370 to 960 cr a run measured | 21 drones had not flown it at 02:55 UTC; six herds carry about six pilots an hour |
| 3 | none now: `mission-cracking-the-shell-achernar` and `-central` are out | 0 | 1,500 cr once | Offered only to a pilot with First Hunt booked (7 of 7 with, 0 of 12 without); back when a route can require it (requests.log ENT-091) |
| 4 | `voidborn-first-steps`, `voidborn-selling`, `voidborn-concurrent` and the other once routes | as booked | once | Pass by themselves once booked |
| 5 | `hunt-test-achernar-cinder-sylph` | 1 | 3,230 over 2 runs | Ember glands at 480 cr, bid 50 deep at every station |
| 6 | Veil-rays: `hunt-gsc-veil-ray` 3,360 (24 runs), `-hamal-` 2,770 (13), `-ruchbah-` 2,710 (11), `-faintlight-drift-` 2,120 (4), `-low-charge-glint-` 2,110 (6), `-keid-fractured-prism-` 1,760 (7), `-cedarhold-dim-lattice-` 900 (6) | 1 each, 7 | about 2,000 to 3,400 | The herds that paid; ranched, no hunt below 4 animals |
| 7 | Tests, one ship each: veil-rays at Dimming Pocket and Denebola; cinder-sylphs at Lesath and GSC-0050; patina-grazers at Atlas, slag-tortoises at Garnet Belt, glitterback crabs at Goldcrest, hollow-pilgrims at Tanglewood | 1 each, 8 | not measured | Every untested herd of ten or more, 100 hull or less (orders ENT-011) |
| 8 | `voidborn-first-hunt-schedar` | 1 | 190 over 10 runs | A foreign pilot stood at the place in 8 of 9 runs; last of the once routes |
| 9 | `census-frontier`, then `park` | up to 12, then the rest | reads; 0 | Docked costs nothing |

At 03:18 UTC 12 of 30 drones flew and 18 waited with nothing paying or under
test open to them (fill gate PASS). What limits the division is the herds: one
hunter per place and a herd that regrows a few animals an hour; about 16 places
pay or are under test. Once First Hunt is booked by every drone (about two
hours), its six places close and about 10 drones hunt.

What would change the plan: a yield test whose drop sells (it becomes a ranched
route); a herd read under four or a foreign ship at the place in two runs in a
row (it moves back in the order or leaves); the guard route kind (owed by Unity,
requests.log ENT-076), which gives the waiting drones a post beside every mine
route beyond the border.

## 1. Routes That Pay

Measured by `routes.py measure`, 2026-11-16 03:19 UTC, all runs of each route,
credits per ship-hour after fuel. A hunt's credits include what the hunter sold
of goods it carried in (a neural soma from a mission sells for 500 to 650 cr at
the hunt's station), so a run without a kill can read above zero.

| Route | Credits per ship-hour | Runs, minutes a run, credits a run | Note |
|---|---|---|---|
| `hunt-gsc-veil-ray` | 3,360 | 24, 23 min, 1,420 cr | The steadiest herd: 6 to 18 veil-rays at every read since 17:58 UTC on 2026-11-15, 7 at 03:04 UTC. Trains Weapons and Xenobiology |
| `hunt-test-achernar-cinder-sylph` | 3,230 | 2, 8 min, 430 cr | First run 03:00 UTC: 2 kills in 5.2 min at the place, 2 ember glands sold at The Experiment at 480 cr, +894 cr in 12.2 min, hull 75 of 75. Ember gland: bid 480 x 50 at every station of ours and at Ironlight Crossroads. The herd read 10 at 01:21 and 4 at 03:13 UTC |
| `hunt-hamal-veil-ray` | 2,770 | 13, 25 min, 960 cr | Shared with other hunters: 0 to 16 at the reads, 7 at 03:10 UTC |
| `hunt-ruchbah-veil-ray` | 2,710 | 11, 22 min, 840 cr | Beyond the border; a foreign ship at the place ended 3 of 11 runs |
| `hunt-faintlight-drift-veil-ray` | 2,120 | 4, 30 min, 900 cr | Achird, beyond the border |
| `hunt-low-charge-glint-veil-ray` | 2,110 | 6, 20 min, 690 cr | Okab, beyond the border |
| `hunt-keid-fractured-prism-veil-ray` | 1,760 | 7, 31 min, 920 cr | Keid, beyond the border; also the presence beside Mining's Keid ice route |
| `hunt-cedarhold-dim-lattice-veil-ray` | 900 | 6, 15 min, 250 cr | 3 of 6 runs without a kill; the herd read 0 at 01:33 UTC |

Veil-rays drop verdigris curd, sold at 330 cr; their carapace has no bid above
2 cr and stays in the hold. Hunts of the division from 2026-11-16 00:06 to
03:18 UTC: about 26,500 cr after carried-in sales in 13.3 hunter-hours, about
1,990 cr per hunter-hour (`data/routes/runs.jsonl`, my sum).

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
| Yield test: kiln-snails (100 hull) at Eltanin Prime Belt, Node Beta | 1 run of 32.8 min: 0 kills, hull 75 -> 46 (lowest 68% in the battle table), -167 cr | 2026-11-15 23:29 UTC | The one fight of the turn that cost hull: prey of 100 hull hits a starter hard. Off (orders F9) |
| `hunt-ruchbah-veil-ray` by hand, hold empty | 1 run: 0 kills, -77 cr, two ships of a faction of 1,249 members joined the fight within three minutes | 2026-11-15 21:26 UTC | The first run of the route (below, section 6) found nobody there |
| `hunt-garnet-dim-lattice-veil-ray` | 6 runs, 0 kills, -610 cr per ship-hour | 2026-11-16 03:19 UTC | A ship not of ours at the place in every run; the herd read 23 at 01:30 UTC. Out of the plan (orders F8) |
| `hunt-test-acubens-patina-grazer` | 5 runs, 0 kills, -500 cr per ship-hour | 2026-11-16 03:19 UTC | A pilot not of ours at the place in every run; out. Patina-grazers are tested at Atlas instead |
| `voidborn-first-hunt-schedar` | 10 runs, 190 cr per ship-hour with the reward; 1 of 9 counted runs handed in | 2026-11-16 03:19 UTC | A foreign pilot at the place in 8 of 9 runs (route logs). Kept last among the once routes because the fill gate counts it paying |
| `voidborn-first-hunt-ironhollow-echo`, `-fading` | 2 runs each, no hand-in, -670 and -580 cr per ship-hour | 2026-11-16 03:19 UTC | Foreign ships at both Ironhollow belts in their first runs; under watch, out after two more |

## 3. Missions That Pay Once

The `once` routes at the head of the plan: every pilot flies them
first. Measured by `routes.py measure`, 2026-11-15 23:58 UTC, all runs of
the fleet:

| Route | Pays once | Measured | Note |
|---|---|---|---|
| `voidborn-precedence` | 4,000 cr | 41 runs, 15 min, 3,890 cr a run | Accept at Node Beta, two docks, nothing bought. Drones from 23:40 UTC |
| `voidborn-first-hunt-nexus`, `-gsc`, `-acubens` | 1,000 cr, 50 Weapons XP, 15 Xenobiology XP, 20 Piloting XP | 2026-11-16 03:19 UTC, all runs of the fleet: nexus 10 runs, 21 min, 570 cr a run; gsc 7, 27 min, 790 cr; acubens 12, 14 min, 370 cr | The circuit runner's `hunt` step: accept, three belt-grazer kills, hand in. One hunter per herd, so the fleet's pilots queue for three herds |
| `voidborn-first-hunt-schedar` | the same | 10 runs, 11 min, 40 cr a run (2026-11-16 03:19 UTC); see section 2 | A fourth herd one jump beyond GSC-0027 (20 belt-grazers, no pilot, 21:14 UTC), `alone` and an empty hold; a test from 2026-11-15 23:58 UTC |
| `voidborn-selling` | 1,000 cr for the pilots that hold Market Participation: Selling | 40 runs, 5 min, 870 cr a run | 20 drones held the mission (`data/fleet/ships/`, 23:46 UTC) |
| `voidborn-concurrent` | 3,000 cr | every drone has it booked | Flown by all 30 drones on 2026-11-15 |
| `voidborn-first-hunt-ironhollow-echo`, `-ironhollow-fading`, `-achernar` | 1,000 cr, accepted and handed in at The Experiment | Achernar: 1 run, 19 min, +960 cr (03:00 UTC); Ironhollow: see section 2 | Three herds one jump beyond The Experiment, written 2026-11-16 03:00 UTC: 26, 19 and 12 belt-grazers at their reads of 01:19 to 01:20 UTC |
| `mission-cracking-the-shell-achernar` | 1,500 cr, 55 Weapons XP | 1 run, refused at the accept | Out of the plan: in 19 runs of the fleet (2026-11-16 01:16 to 03:22 UTC) the pilots with First Hunt booked were offered it (7 of 7) and the others not (12 of 12), and a refused run counts as done for the pilot. "Hunt 3 Pressblisters at an ice field": any ice field. Achernar Frost Ring read 8 pressblisters at 01:21 UTC; Node Gamma Ice Belt, the place of `mission-cracking-the-shell-central` (13 runs, 1,200 cr per ship-hour), read 0 from 02:27 UTC |

Belt-grazer goods are creature carapace and raw xeno meat; no station of
ours bids above 1 cr for either. The mission is the pay.

## 4. Levelling

- Piloting opens the hulls: tier 2 needs Piloting 10. The drones stand
  at Piloting 3 (20 drones), 4 (8) and 5 (2) (`data/fleet/ships/`,
  2026-11-15 23:35 UTC). The catalog's XP per level: 900 for level 4 to 5,
  then 1,285, 1,740, 2,265, 2,860 and 3,525 for level 9 to 10. What a hunt
  gives in Piloting is not measured; First Hunt gives 20.
- 2026-11-16 03:18 UTC (`hive.py levels`): Piloting 3, 3 and 5 (lowest, median,
  highest) over 30 drones, 114 XP an hour on average since birth, so about 112
  hours to Piloting 10 at that rate. A hunt trains Gunnery, Weapons, Tactics and
  Xenobiology; First Hunt and Cracking the Shell add 20 Piloting XP each.
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

- Re-quoted 2026-11-16 03:17 UTC at Central Nexus: the Vigil costs 111,316 cr
  with credits only (materials 47,805, labor 1,050, yard fee 14,656), or
  15,706 cr plus the same materials; build time 87 ticks.
- The railgun ship flies the Pulse Laser I again since 2026-11-16 03:10 UTC; its
  Piercing Railgun I lies in its storage at Central Nexus. A storage withdraw to
  the own hold is `withdraw` with item and quantity only; with `target: cargo`
  the gate's wall refuses it as a give-away.
- The exchange lists ships too: `browse_ships` showed 259 listings at the
  stations our pilots have charted, tier-1 hulls from 1,000 cr, all at
  stations of other empires (2026-11-15 23:31 UTC).
- The division flies the Threshold with the Pulse Laser I this week. A
  hunt is bounded by the herd and by other hunters, not by the weapon
  (sections 1 and 2): a hull that kills faster earns more only where a
  herd grows under our ranch. What a Vigil would earn is not measured.

## 6. Open Tests

Every test is one ship, in `game/routes/plans/drone.json`, written 2026-11-16
03:00 to 03:16 UTC; each leaves the plan after its first RESULT lines unless its
drop sells (orders ENT-011: every untested herd of ten or more, 100 hull or less):

- Cinder-sylphs at Lesath Gas Cloud (8 at 2026-11-15 22:03 UTC) and GSC-0050 Gas
  Plume (5 at 21:49 UTC): the species that paid at Achernar.
- Patina-grazers at Atlas Gossamer Null (12 at 01:52 UTC).
- Slag-tortoises (90 hull) at Garnet Belt (10 at 01:30 UTC): first run 0 kills,
  -99 cr, no note.
- Glitterback crabs at Goldcrest Glitterback Scatter (18 at 2026-11-15 23:37 UTC):
  first run left, a ship not of ours at the place, -154 cr.
- Hollow-pilgrims (70 hull) at Tanglewood Frost Ring (11 at 2026-11-15 23:34 UTC).
- Veil-rays at Dimming Pocket (Thornhaven) and Denebola Fractured Prism, written by
  the route maker: first runs left with no kill.
- Which prey drops caustic sac (bid 420 cr, 50 at seven stations): not measured.
  The catalog names no source; the yield tests above will show their drops.
- A tier-1 hull with two weapons: after a yield test shows prey worth a tougher
  hull (section 5).

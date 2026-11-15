---
name: guidebook-mining
id: 20261115T205803Z
tier: intel
author: Unity
links:
  - The-Collective:game/routes/BLUEPRINT.md
---

# mining.md -- Guidebook of the Mining Division

Kept by Zero; read by every member. What the Mining division
learned about its routes, its levelling and its ships, so that every
ship born later starts where the others stand. Started by the Fleet
Admiral on 2026-11-15 from the runs so far; from here Zero writes it,
at the end of every turn.

- A figure comes from `python3 -B game/fleet/routes.py measure` or from a
  run's RESULT line, and carries its date. A number no record holds is
  written `not measured`.
- The plan in force is `game/routes/plans/miner.json`; every route
  with its figure is in `game/routes/index.md`.

## 1. Routes That Pay

| Route | Credits per ship-hour, after all costs | Date | Note |
|---|---|---|---|
| -- | -- | -- | None flown as a route yet. Best test: water ice from Wolf 1061 sold at Synchrony, +2,688 cr in 30.1 minutes after fuel, one run (section 6). The energy-crystal test paid +1,022 cr in one ship-hour, but its best part is a bid of one unit |

## 2. What Did Not Pay

| Route or test | What was measured | Date | Why, and what follows |
|---|---|---|---|
| `mine-acubens`, `mine-gsc-seep`, `mine-pherkad-rift` | Below zero: see the figures in `game/routes/index.md` | 2026-11-15 | Iron and copper ore sell for 1 to 4 cr and nobody needs them; the cost is the fuel for the jump to a station. Out of every plan since 2026-11-15 (orders F8) |
| `voidborn-first-steps` (First Steps in the Void, 15 carbon ore) | Two runs of 20 minutes, -109 and -153 cr, "objectives not done" (runs.jsonl, 21:02 and 21:03 UTC) | 2026-11-15 | Acubens Belt read 0 carbon ore at 21:01 UTC (`data/scouting/acubens.json`); off. A read at 22:17 UTC showed 41 again: carbon regrows, slowly |
| Focused crystal as a chain for many ships | The Experiment bids 1,466 cr for one unit (station), then 40 cr and 2 cr (view_market, 21:19 and 22:21 UTC); after our sale the best bid was 40 | 2026-11-15 | The 879 units once quoted were the total of all bid levels (errors.log ENT-015). One craft per refill of that bid; whether and how fast it refills is open (section 7) |
| Honeyglobe (water ice made into honeyglobe) | Node Beta bids 154 cr for 1 and 147 cr for 1; The Experiment 2 cr for 376 (view_market, 21:19 UTC) | 2026-11-15 | No depth: not tested |

## 3. Missions That Pay Once

The `once` routes at the head of the plan: every pilot flies them
first. What a new one pays and what it needs is written here when it
was flown the first time.

| Route | Pays | Measured | Date | Note |
|---|---|---|---|---|
| `voidborn-concurrent` (Concurrent Approval) | 3,000 cr | 39 miner runs, 339 minutes, +115,037 cr, of it 117,000 one-time (runs.jsonl, 21:14 to 22:24 UTC) | 2026-11-15 | Opened by Trade after one hand run (`e38b798`); at the head of the miner plan since 21:28 UTC. Its two neural soma come with the accept |
| `voidborn-mining-missions` (Iron Supply Run, Copper Requisition) | 1,500 + 1,800 cr | 3 miner runs by 22:24 UTC: +6,430 cr, of it 6,600 one-time; 22 miners on it at 22:23 UTC (`board.py`) | 2026-11-15 | For the 25 miners born after 14:12 UTC. Mining XP 15 each on top of the ore |

## 4. Levelling

- Mining XP is one point per unit mined. miner-1 (Mining 4) went from
  240 to 405 XP in the 165 units of the energy-crystal test
  (`data/fleet/ships/miner-1.json`, 21:22 and 22:02 UTC). Level 5 needs
  900 XP (the catalog's table).
- Mining skill raises the share of the rarer deposit in a pull (the
  game's `mine` help: the draw is weighted by richness and, as the
  skill grows, by rarity). At Mining 4 the nebula of
  `hunt-gsc-veil-ray` gave 24 energy crystal in 166 units, 14.5%,
  where its richness alone (4 of 48) gives 8.3%.
- Piloting 10, 20, 30 and 50 open hull tiers 2 to 5 (shared skill
  `fleet-play`, levelling). The cost per point of Mining XP is the fuel
  per unit: 77 cr of fuel for 165 units in the test (0.47 cr per XP).

## 5. Ships and Fits

- The starter (Threshold): 2 utility slots, 16 cpu, 30 power, hold 65.
  The Mining Laser I (cpu 2, power 5, mining power 5) and the Pulse
  Laser I (cpu 2, power 5) leave one utility slot free (catalog 0.717.0).
- Ice Harvester I: 1,413 cr at Synchrony Hub (station ask, 5 units)
  plus 14 cr tax: the wallet fell 1,427 cr (2026-11-15 22:30 UTC).
  Fitted beside both lasers: cpu 8 of 16, power 17 of 30 (the
  `install_mod` answer). Mining power 8. At Wolf 1061 it filled a hold
  of 65 in about 7 minutes.
- Extraction filters take one ore out of a pull's draw (the game's
  `mine` help; catalog `special: filter_<ore>`): Magnetic Ore Separator
  (iron; power 12), Flotation Cell (copper; power 4, cpu 8; 1,600 cr at
  Node Beta and The Experiment, a few units), Electromagnetic Refinery
  (iron and copper; power 18, cpu 12), Isotope Separator (water and
  nitrogen ice; power 22, cpu 10). One filter fits in the free utility
  slot. Not bought: no rare ore of our fields has a buyer with depth yet.

## 6. Tests Flown

### Energy crystal at the nebula of `hunt-gsc-veil-ray`, 2026-11-15

One miner (Mining 4), 21:22 to 22:22 UTC, by hand. Each call and its
answer:

| Step | Call (tool group) | Answer |
|---|---|---|
| Mine 40 minutes, ore stored at Node Beta | `game/fleet/mine.py <pilot> gsc_0027:gsc_0027_prism_scatter node_beta:node_beta_industrial_station:node_beta_industrial_station --minutes 40` | RESULT: credits -77 (fuel); three loads, 166 units: 24 energy crystal, 94 iron ore, 48 copper ore (storage view before and after) |
| Dock | `goal prepare-at-station {systemId, poiId, baseId, refuel: true}` | Docked and refuelled, -33 cr |
| Ore into storage | `deposit {item_id, quantity, target: self, source: cargo}` (spacemolt_storage) | One item per call |
| Quote, then buy one palladium ore | `estimate_purchase` (spacemolt_market), `buy {item_id, quantity}` | 432 cr from a player's ask + 4 cr tax: -436 cr |
| Quote the craft | `craft {recipe_id: focus_energy_crystal, quantity: 1, deliver_to: storage, preset: workshop, dry_run: true}` | Station Workshop, `have_inputs` true, 24 ticks, no credit cost |
| Craft | the same without `dry_run` | Queued; done within 4.5 minutes (`craft {}` lists the queue) |
| Take out | `withdraw {item_id, quantity}` (spacemolt_storage) | 1 focused crystal and 4 energy crystal into the hold |
| Sell 4 raw crystals at Synchrony | `view_market {item_id}` first, then `sell` | Bid 40 x 588: +160 cr; refuel -36 cr |
| Sell the focused crystal at The Experiment | `view_market`, then `sell` | Station bid 1,466 x 1: +1,466 cr; refuel -22 cr. After it the best bid read 40 |

Result: wallet 30,631 -> 31,653 cr, +1,022 cr in 59.9 minutes after
fuel (168 cr) and the palladium (436 cr); 20 energy crystal left in
storage at Node Beta. The weekly tax on the sale is not counted (6% of
the week's income). What one load is worth at the bids that stand: a
load of 65 units held 5 to 11 crystals; at the 40 cr bids (Synchrony
588 units, Node Alpha 301) a 40-minute run's 24 crystals are 960 cr
before the trip to sell them.

### Ice at Wolf 1061 (frontier), 2026-11-15

One miner (Mining 4), by hand, 22:25 to 23:01 UTC. Wolf 1061 is
lawless (police 0); its frozen drift read water ice 21,518 (richness
47), nitrogen ice 50,000 (36), deuterium ice 4,752 (14) and methane ice
4,000 (13), one other pilot and no pirates at 21:49 UTC
(`data/scouting/wolf_1061.json`, `data/wildlife/wolf_1061.json`).

| Step | Call (tool group) | Answer |
|---|---|---|
| Central Nexus to Synchrony | `goal prepare-at-station` | 3 jumps, -36 cr |
| Buy and fit the harvester | `estimate_purchase`, `buy`, `install_mod {module_id: ice_harvester_i}` (spacemolt) | -1,427 cr; "Installed Ice Harvester I in utility slot" |
| Mine 25 minutes, ice stored at Synchrony | `game/fleet/mine.py <pilot> wolf_1061:wolf_1061_frozen_drift synchrony:synchrony_hub:synchrony_hub --minutes 25` | RESULT: 126 units, credits -130 (fuel). Two loads: water ice 77, nitrogen ice 40, methane ice 5, deuterium ice 4 (storage view) |
| Back to Synchrony | `goal prepare-at-station` | -65 cr with the refuel |
| Read the books, sell from storage | `view_market {item_id}`, then `sell` (the hold was empty: `from_storage`) | Methane 47 x 1,000: 5 sold, +235. Water ice, station bid 36 x 15 and 34 x 12,948: 77 sold, +2,648. No bid at Synchrony for nitrogen or deuterium ice: they stay in storage |

Result: from the purchase to the sale (22:31 to 23:01 UTC) the wallet
went 32,296 -> 34,984 cr, +2,688 cr in 30.1 minutes after 195 cr of
fuel, about +5,360 cr per ship-hour. With the harvester and the way
out from home: 33,759 -> 34,984, +1,225 cr in 35.5 minutes. Mining XP
+126. One run only. The water-ice bid at Synchrony read 34 x 8 at 20:33
UTC and 34 x 12,948 at 23:00 UTC: station bids move, so the book is
read before every sale. Water-ice bids with depth stood at four of our
stations (`ledger.py prices water_ice`): The Experiment 32 x 4,535
(21:11), Node Gamma 32 x 12,262 (22:47), Node Alpha 25 x 21,010 (21:38),
Synchrony 34 to 36 (23:00).

## 7. Open Tests

- Water ice from Wolf 1061 as a route: the second run, and the third,
  to see whether the Synchrony bid holds. A mine route stores its ore
  and does not sell (BLUEPRINT, kind `mine`): the route waits for a sell
  step (requests.log ENT-051); until then it is flown by hand.
- A Nitrogen Vent (filter nitrogen ice; power 9, cpu 4) in place of the
  mining laser: nitrogen ice was 32% of the load and has no buyer.
- Whether the one-unit station bid for focused crystal at The
  Experiment refills: `ledger.py prices focused_crystal`, before a second
  craft.
- A crystal route that sells raw at 40 cr: not flown as a route; the
  fuel of the trip to Synchrony decides it.
- Uranium, thorium and tritium have bids of 300, 240 and 400 cr with
  depth at all six stations; no field read in our space or on the
  frontier holds them (census reads to 22:22 UTC).

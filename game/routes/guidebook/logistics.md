---
name: guidebook-logistics
id: 20261115T205805Z
tier: intel
author: Unity
links:
  - The-Collective:game/routes/BLUEPRINT.md
---

# logistics.md -- Guidebook of the Logistics Division

Kept by Apollo; read by every member. What the Logistics division
learned about its routes, its levelling and its ships, so that every
ship born later starts where the others stand. Started by the Fleet
Admiral on 2026-11-15 from the runs so far; from here Apollo writes it,
at the end of every turn.

- A figure comes from `python3 -B game/fleet/routes.py measure` or from a
  run's RESULT line, and carries its date. A number no record holds is
  written `not measured`.
- The plan in force is `game/routes/plans/hauler.json`; every route
  with its figure is in `game/routes/index.md`.

## 1. Routes That Pay

| Route | Credits per ship-hour, after all costs | Date | Note |
|---|---|---|---|
| -- | -- | -- | None yet |

## 2. What Did Not Pay

| Route or test | What was measured | Date | Why, and what follows |
|---|---|---|---|
| -- | -- | -- | No hauling route has been flown for pay. The ore in storage has no buyer (read 2026-11-15) |

## 3. Missions That Pay Once

The `once` routes at the head of the plan: every pilot flies them
first. What a new one pays and what it needs is written here when it
was flown the first time.

## 4. Levelling

Which skills this division's pilots need, what trains them fastest and
what it costs: `not measured`. Piloting 10, 20, 30 and 50 opens hull
tiers 2 to 5 (shared skill `fleet-play`, levelling).

## 5. Ships and Fits

The hull and the modules for this division's work beyond the starter,
what they cost and what they changed in a run: `not measured`.

## 6. Open Tests

- What the stored ore is worth made into something (steel plate, copper wiring, ferrous slugs): not tested.
- What the fleet owns and where: `python3 -I -B game/fleet/ledger.py show all`.

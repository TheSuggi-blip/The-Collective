# Logistics guidebook -- the Class Card (card.md)

### Class Card
Status: proven. Updated: 2026-11-24. Evidence: governance/collective-strategy.md; game/haul-policy.json; game/fleet/workclass.py; read.db tables hulls, books, ship_listings.

Logistics is the fleet's Service and Infrastructure Center across all
five empires (Voidborn, Nebula, Solarian, Outer Rim, Crimson; F23:
gathering is Mining's, selling is Trade's). Core duties: (1) bulk
freight and `spacemolt_shipping` contracts (`haul-network` /
`haul-policy.json`), (2) **industrial building-material crafting**
(`steel_plate`, `circuit_board`, `wiring`, `piping`, base kits --
commercial profit crafting belongs to Trade), (3) **civilian and
express passenger transport** (`passenger-` routes), and (4) sovereign
outpost, lockbox, and station construction.

### Ships
Status: proven. Updated: 2026-11-24. Evidence: read.db tables hulls, ship_listings, books; game/fleet/upgrades.py.

- Tier 0 starters across Voidborn, Nebula, Solarian, Outer Rim, and
  Crimson: batch-skip immediately to Piloting-0 bulk freighters via
  `upgrades.py queue add` (auto-buys cheaper listed ships from
  `ship_listings`): `Floor Price` (400c, P0), `Ledger` (480c, P0,
  shielded, spd 4), `Prayer` (540c, P0), `Workhorse` (300c, P0), or
  `Congregation` (1,900c, P0).
- Express passenger hulls (Piloting 0): `Runner` (120c, spd 6) and
  `Futures` (P0) fitted with `economy_passenger_cabin` or
  `business_passenger_cabin` (live asks tracked in `read.db:books`).
- Tier 2 (Piloting 10+): `Apophenia` (240c, shielded, 300 fuel) and
  empire equivalents.
- Fit: `cargo_expander_ii/iii`, passenger cabins on `passenger-` ships,
  `shield_booster_ii`; strip starter mining/pulse lasers; stance flee.

### Skills
Status: proven. Updated: 2026-11-24. Evidence: catalog table skills; table ship_skills; `hive.py stats xp`.

Inspect live levels via `fleet view=levels`:

| Skill | Why | What trains it | Target |
|---|---|---|---|
| Crafting, Refining | workshop speed x1 to x5 for industrial parts | `@craft-reserve`, `craft-boards-*`, building kits | 6+ builder |
| Corporation Management | tier N faction facilities & sovereign stations | faction facility builds and upgrades | 6+ builder |
| Navigation | -1% fuel and jump time per level | freight contracts, carries, passenger runs | 5+ |
| Piloting | T2 hulls at 10, T3 at 20 (P0 hulls skip wait) | flying and board missions | 10+ |
| Empire Mastery | empire bonuses (F35) across all 5 cohorts | local empire board missions | 1+ |
| Engineering | module power and CPU -1% per level | crafting industrial components | 2+ builder |
| Mining | not Logistics' work (rule F23) | -- | not a goal |

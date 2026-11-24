# Trade guidebook -- the Class Card (card.md)

### Class Card
Status: proven. Updated: 2026-11-24. Evidence: governance/collective-strategy.md; game/bursar-policy.json; game/fleet/workclass.py; read.db tables hulls, books, ship_listings.

Trade is the fleet's Profit Center across all five empires (Voidborn,
Nebula, Solarian, Outer Rim, Crimson). Core duties under F23: (1)
multi-hub `bursar-network` market-making (`bursar-policy.json`, 60+ safe empire & non-pirate neutral hubs permanently staffed via `bursar-network` `max_ships=65`, `max_hull_tier=0, max_cargo=150` so T1/T2 `Prayer`/`Apophenia` & `Cargo Expander II` ships stay reserved for mobile trading & crafting),
(2) final liquidation of Mining/Military handovers and surplus vaults,
(3) zero-fuel **commercial value-added crafting** at public NPC
refineries/factories for profit and rival buy-walls (`silver_bar`,
gourmet rations, components, modules -- Logistics crafts empire
building materials), and (4) wholesale procurement (including
`station_core` ~13M cr and cheap rival surplus).

### Ships
Status: proven. Updated: 2026-11-24. Evidence: read.db tables hulls, ship_listings, books; game/fleet/upgrades.py.

- Cross-empire rule (`05-galaxy.md`): flying another empire's hull
  carries **zero penalty** and keeps native empire bonuses -- pick the
  best hull by job (`Prayer`/`Ledger`/`Floor Price`/`Apophenia`).
- Policy rule (`O3`): tune fleet-wide caps in `bursar-policy.json`
  (`bursar_buys.json` caps fleet open buys at `needs.tsv` short) rather
  than turning core buy/sell lanes off.
- Tier 0 starters across Voidborn, Nebula, Solarian, Outer Rim, and
  Crimson (cargo 45-65) should skip straight to Piloting-0 bulk hulls
  without waiting for Piloting 10: `Floor Price` (400c, P0), `Ledger`
  (480c, P0, shielded), `Prayer` (540c, P0), or `Congregation`
  (1,900c, P0). Check `hive.py upgrades trade` or SQL `ship_listings`
  for live galaxy prices (`upgrades.py queue add` automatically buys
  cheaper listed hulls via `buy_listed_ship` for instant delivery).
- Tier 2 (Piloting 10+): `Apophenia` (Voidborn, 240c, shielded) and
  empire equivalents; check `ship_listings` before commissioning.
- Fit: `cargo_expander_ii/iii` and `shield_booster_ii` from live
  Exchange asks (`read.db:books`); strip off-role starter lasers.
- Style: dock to dock, stance flee, never fight; Bursars stay docked
  at 0 fuel burn.

### Skills
Status: proven. Updated: 2026-11-24. Evidence: table ship_skills; catalog table skills; `hive.py stats xp`.

In levelling order (inspect live levels via `fleet view=levels`):

| Skill | Why | Trained by | Target |
|---|---|---|---|
| Trading | class skill; `analyze_market` depth | buying, selling, Bursar orders, Trade Run missions | 3+ all |
| Crafting | workshop speed for commercial goods | docked NPC-facility commercial crafting | 6+ |
| Refining | smelting speed (`silver_bar`, alloys) | docked refining runs | 5+ |
| Navigation | -1% jump fuel and time per level | cross-hub transfers and wholesale buys | 6+ |
| Piloting | unlocks T2 at 10, T3 at 20 | flights and missions (P0 hulls bypass wait) | 10+ |
| Engineering | module CPU and power reduction | crafting components and modules | 2+ |

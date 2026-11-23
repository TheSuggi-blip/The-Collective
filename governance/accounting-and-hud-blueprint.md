---
name: accounting-and-hud-blueprint
id: 20261123T112200Z
tier: governance
author: Trinity
updated: 2026-11-23
links:
  - governance/the-collective-constitution.md
  - governance/system-architecture.md
  - governance/kpi-and-strategy-system.md
  - game/metrics.md
  - game/fleet/index.md
---

# The Collective -- End-to-End Bookkeeping, GAAP/IFRS Accounting & Station HUD Blueprint

This blueprint documents how every credit, fuel unit, module purchase, mission reward,
vault item, and internal handover flows from the live SpaceMolt engine through our
bookkeeping layer into GAAP/IFRS-aligned financial statements, Admiral briefings, and
every tab of the Command Station HUD (`:8445`).

---

## 1. Accounting Architecture: Two Complementary Layers

The Collective operates as a **vertically integrated multi-division enterprise** sharing
one consolidated purse (`One Purse` rule, `game/metrics.md`). Under strict class
specialization (`P5`), Mining extracts ore, Military farms combat loot, Logistics crafts
and stages build kits, Intel scouts markets, and Trade liquidates surplus for cash.

Because of this vertical integration, **neither pure cash accounting nor pure accrual
accounting is sufficient alone**:

1. **Cash Ledger (`station/fleet.py` + `game/fleet/routes.py`):** Tracks exact real-world
   credit movements in ship wallets and the faction treasury to the single credit. Guards
   **Liquidity & Cash Burn** (you cannot buy fuel or pay NPC rent with unsold ore).
2. **GAAP / IFRS Reconciliation & Managerial Layer (`game/fleet/accounting.py`):** Bridges
   the cash ledger to international accounting standards (**US GAAP / IFRS**, **IFRS 18**,
   **IAS 7**, **IAS 2 / ASC 330**, and **Intercompany Transfer Pricing**) so Admirals and
   Suggi never mistake profitable reserve-building or one-time mission fuel for structural
   operating losses, nor mistake thin speculative market bids for real balance-sheet wealth.

---

## 2. Raw Bookkeeping & Entity Consolidation Layer

### 2.1 Collector Cash Windows (`station/fleet.py`)

Every minute, `station/fleet.py` polls ship wallets, cumulative `credits_earned` /
`credits_spent`, metered fuel/repair counters, `empire.json` treasury snapshots,
`gifts.jsonl` wallet-guard transfers, and `onetime.json` one-time events, producing
rolling `1h`, `6h`, and `24h` windows in `fleet/fleet.json` (and hourly rollups in
`read.db:stats_money_hour`):

- **Entity Consolidation (Intercompany Elimination):**
  - `Wallet top-up` (`gifts.jsonl`): Money transferred between two of our pilots cancels
    out identically (`transfers_per_hour = 0` at Fleet level) -- neither income nor cost.
  - `TREASURY` / `TREASURY_FUND` (`onetime.json`): Deposits into and withdrawals from our
    own faction treasury cancel out between wallets and treasury. Only the treasury's *own*
    external flows (`treasury_own_per_hour`: NPC facility rent, treasury-paid buildings)
    enter Consolidated Net Purse Change (`purse_per_hour`).
  - **Scope Hygiene:** Newborn pilots' initial starter wallets (`seed`) and ships that
    briefly go offline or rejoin (`presence`) are excluded from window deltas so cashflow
    never spikes artificially on disconnects or birthing waves.
- **What Counts as Steady vs Paid Once (`onetime.json` & `runs`):**
  - **100% Steady Recurring:** Trade sales (`sell-*`, `carry-*`, `bursar-*`), recurring
    crafting (`craft-*`), internal handovers (`give-*`, `store-*`), mining (`mine`),
    military hunts (`hunt`), and intel (`census`).
  - **Paid Once (`one_time != 0`):**
    - Positive (`rewards_per_hour`): One-time onboarding/seed missions (`once: true`) that
      each pilot can complete only once in its lifetime.
    - Negative (`bought_once_per_hour`): Capital purchases tagged `one_time: true` (hulls,
      Tier-2/3 modules, outpost kits, and occasional tagged reserve craft inputs).

### 2.2 Per-Route Earnings (`game/fleet/routes.py` -> `read.db:runs`)

Every completed route run is recorded in `routes/runs.jsonl` and ingested into
`read.db:runs` by `store.py` using `routes.earned(row)`:

- Removes weekly faction/game taxes (`taxes.in_run`) and wallet-guard transfers (`moved`)
  that occurred mid-run so a handover or top-up never corrupts a route's profit figure.
- Separates `one_time` (one-time mission reward or tagged buy) from `credits` (the run's
  steady wallet change, primarily fuel, repairs, trade sales, or salvage).
- Normalizes earnings by exact run duration (`per_ship_hour = 60 * credits / minutes`).

---

## 3. GAAP / IFRS Financial Statements (`game/fleet/accounting.py`)

`game/fleet/accounting.py` is the **single source of truth** consumed by `station/server.py`,
`game/fleet/scorecard.py`, `game/fleet/progression.py`, and `game/fleet/watchdog.py`.

### 3.1 Matching Principle & Cash Flow Statement (IFRS 18 + IAS 7)

Under **IFRS 18**, non-recurring `once: true` mission rewards MUST remain separate from
recurring run-rate income (once all 500 pilots complete a mission, that revenue drops to
zero permanently). However, leaving the **direct fuel burned to fly those non-recurring
missions** inside recurring `costs_per_hour` violates the **Matching Principle** and
artificially inflates the recurring cash deficit.

`accounting.compute_pnl()` separates all `once: true` route runs from `read.db:runs`
(scanning ALL `game/routes/*.json` files with zero truncation) into two clean buckets:

1. **Non-Recurring Mission Direct Costs (`once_mission_direct_h`):** Fuel and mission
   inputs on `once: true` non-fit routes. Carved out of raw steady OpEx and matched
   directly against `rewards_per_hour`:
   - `seed_net_h = rewards_per_hour + once_mission_direct_h`
2. **Investing CapEx Direct Salvage/Fuel (`capex_fit_direct_h`):** Stripped-module
   salvage minus transit fuel on `once: true` `fit-*` / `buy-hull-*` / `upgrade-*`
   upgrade routes. Matched directly against `bought_once_per_hour`:
   - `capex_net_h = -bought_once_per_hour + capex_fit_direct_h`
3. **Matched Recurring Operating Cash Flow (`recurring_cash_h`):**
   - `recurring_cash_h = raw_steady_h - (once_mission_direct_h + capex_fit_direct_h)`
4. **Exact Cash Reconciliation Identity (Zero Plugs, Zero Double-Counting):**
   ```text
   recurring_cash_h + seed_net_h + capex_net_h + treasury_own_h == purse_h
   ```

### 3.2 IAS 2 / ASC 330 Inventory Valuation & Accrual Operating Income

Raw materials, crafted components (`circuit_board`, `steel_plate`, `armor_plate`), and
hunt loot accumulated in station vaults and faction storage are **Work-in-Process (WIP)
and Finished Goods Inventory**, not destroyed cash.

To prevent BOTH thin-bid phantom markups (e.g., 10 units bid at `814 cr` valuing 1,400
units of `silicon_ore` at `1.13M cr`) AND dead catalog overstatements (e.g., `quantum_fragments`
with `base_value = 600` when market bids are `3 cr`), `accounting.vault_valuation()` computes
three explicit valuations side-by-side:

| Valuation Basis | Formula | Purpose |
| :--- | :--- | :--- |
| **IAS 2 Conservative NRV (`vault_nrv`, Primary)** | `SUM(units * min(base_value, best_bid))` (falls back to `base_value` only if no bid exists, or `best_bid` if `base_value == 0`) | Honest Balance Sheet carrying value & Inventory Accrual basis (US GAAP ASC 330 / IFRS IAS 2 Lower of Cost or NRV). |
| **Catalog Book Value (`vault_catalog`)** | `SUM(units * base_value)` | Exact apples-to-apples comparison against SpaceMolt's `total_wealth` / `storage_value` rival leaderboards (`HEXC`, etc.). |
| **Instant Liquidation (`vault_liquid`)** | Walk resting bids in `books` descending, capped strictly by `bid_qty` per station | Conservative cash-out stress test: how many credits could be realized immediately without waiting for bid refills. |

Using `read.db:stock_hour` snapshots across the window (`6h` or `24h`), **Inventory / WIP
Accrual** and **Accrual Operating Income** are computed conservatively at IAS 2 NRV:

```text
inventory_accrual_h = (Vault_NRV(now) - Vault_NRV(now - window)) / span_hours
accrual_operating_h = recurring_cash_h + inventory_accrual_h
```

- **Why BOTH metrics appear together:** `recurring_cash_h` enforces liquidity discipline
  (convert surplus into cash; kill empty jump loops), while `accrual_operating_h` proves
  true recurring economic value creation so Admirals never panic-dump strategic build
  reserves (`outpost-kit`, `circuit_board`, `sol_alloy_ore`) at fire-sale prices.

### 3.3 Managerial Accounting: Intercompany Transfer Pricing & Full-Chain Support

Under `P5`, upstream divisions hand goods to Logistics and Trade for `0 cr` cash, making
Mining/Military look falsely negative on pure cash while Trade looks infinitely profitable
with zero Cost of Goods Sold (COGS).

`accounting.compute_pnl()` resolves this via **Intercompany Transfer Pricing at IAS 2 NRV**
using `data/stock/handover.jsonl` over the exact same `[prev_h, max_h]` window as `stock_hour`:

- For every cross-division handover `(from_div != to_div)`:
  - Giving division receives transfer credit `+tx_out_h`.
  - Receiving division incurs transfer cost `-tx_in_h` (true COGS).
- Per-division **Accrual Value-Added**:
  ```text
  div_accrual_op_h = div_recurring_cash_h + div_inv_accrual_h + div_tx_out_h - div_tx_in_h
  ```
- **Exact Consolidation Elimination:** Across all divisions plus `Faction` vault,
  `SUM(tx_out_h) == SUM(tx_in_h)` identically (net `0`), so the sum of every division's
  `accrual_op_h` equals the **Consolidated Fleet `accrual_operating_h` to the credit** with
  zero double-counting.
- **Full-Chain Support Overhead (`support_chains`):** Alongside Trade sales, `accounting.py`
  breaks down recurring cash and ship-hours by activity (`trade_sales`, `mining`,
  `military_hunts`, `handovers_logistics`, `crafting`, `intel_census`, `jump_loops`,
  `once_routes`) so upstream support costs are always transparent.

---

## 4. Command Station HUD (`:8445`) End-to-End Accounting Map

Every financial figure on the HUD traces directly to a read-only backend API endpoint
in `station/server.py` (strict CSP, zero `innerHTML`, read-only SQLite):

| HUD Location | API Endpoint | Source Functions / Tables | What It Displays |
| :--- | :--- | :--- | :--- |
| **Top Bar (`Credits` & `Enterprise`)** | `/api/fleet` + `/api/ops` | `fleet.json` (`purse_per_hour`) + `accounting.vault_valuation` (`balance_sheet`) | Live Liquid Purse (`wallets + treasury` & 24h `purse/h`) and Consolidated Enterprise Value (IAS 2 NRV primary; tooltip breaks down NRV vs Catalog Leaderboard & Instant Bid Depth, Fleet Book, Facilities). |
| **Metrics -- Cash Ledger & By Division** | `/api/fleet` + `/api/history` | `station/fleet.py` (`window()`) | Pure cash ledger for `1h / 6h / 24h`: Net/h, Steady Net/h, Paid Once/h, Treasury Own/h, Running Costs/h (with fuel/repair metering), Per-Division Cash Table, and trailing charts. |
| **Metrics -- Scorecard Pulse** | `/api/ops` (`scorecard`) | `game/fleet/scorecard.py` + `accounting.py` | Enterprise Verdict, Dynamic Posture, Weighted Score, Matched Recurring Cash + IAS 2 Accrual Operating Income, Division Health Cards, and P0-P3 Triage Queues. |
| **Metrics -- GAAP/IFRS Waterfall & Transfer-Priced Table** | `/api/ops` (`accounting`) | `game/fleet/accounting.py` (`6h` & `24h`) | 6-card Cash-to-Accrual Waterfall (`Recurring Cash`, `Inventory Accrual`, `Accrual Operating`, `Seed Net`, `CapEx`, `Purse Cash Flow`), Transfer-Priced Division Value-Added table (intercompany eliminated), and Full-Chain Support Overhead strip. |
| **Metrics -- Balance Sheet** | `/api/ops` (`balance_sheet`) | `accounting.vault_valuation` + `ships` / `hulls` / `ship_modules` / `leaderboards` | Enterprise Net Worth (IAS 2 NRV + Catalog Leaderboard parity), Liquid Purse, Vault (IAS 2 NRV + Catalog + Instant Bid Depth + 24h Handovers), Fleet Book & Facilities. |
| **Metrics -- Where the Money Comes From** | `/api/income?q=<h>` | `read.db:runs` (exact `routes.earned()`, all route JSONs) | Two clean tables: (1) **Repeating (steady) routes** (`once=false`) sorted by credits & `/ship-h`; (2) **One-time missions & fits** (`once=true`) showing Fuel/Inputs, One-time Reward/CapEx, **Matched Net**, and **Matched / ship-h**. |
| **Inventory Tab** | `/api/inventory` + `/api/ops` | `craftbook.py` (`storage.json`) + `balance_sheet` | Full item/station catalog inventory (`base_value`) with header reconciliation showing IAS 2 NRV and Instant Bid Depth so Inventory and Metrics never contradict each other. |
| **Empire -> Progression Subtab** | `/api/progression` | `game/fleet/progression.py` + `accounting.py` | IAS 2 Enterprise Net Worth (+ Leaderboard Catalog basis), 12-Rung Roadmap across Days/Weeks/Months, and Weekly/Monthly `stats_money_hour` cash rollups. |
| **Empire -> Rivals & Playbooks** | `/api/rivals` + `/api/ops` | `game/fleet/rivals.py` + `rival_playbook.py` | Rival wealth compared apples-to-apples on SpaceMolt Catalog leaderboard basis alongside 8 dynamically ranked Copy/Counter Strategy Playbooks. |
| **Watchdog & Agent Briefings** | CLI / MCP `fleet` | `watchdog.py` + `scorecard.py` + `accounting.py` | `watchdog.py` evaluates `ROUTE_BLEED` on `matched_cr = credits + one_time` (never falsely flagging profitable one-time missions); `hive.py briefing` prints both matched recurring cash and transfer-priced accrual value-add for every Admiral. |

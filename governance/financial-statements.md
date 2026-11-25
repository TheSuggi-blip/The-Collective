---
name: financial-statements
id: 20261125T151113Z
tier: governance
author: Trinity
updated: 2026-11-25
links:
  - governance/accounting-and-hud-blueprint.md
  - governance/kpi-and-strategy-system.md
  - governance/system-architecture.md
  - governance/treasury-wallet-and-upgrades-blueprint.md
  - governance/the-collective-constitution.md
---

# The Collective -- Corporate Financial Statements & Enterprise Operating Blueprint

Institutional short-format **Investor Relations (IR)** and audit standard for
reporting The Collective's financial performance, balance sheet position, cash
generation, Buffett/Munger capital returns, and IFRS 8 segment synergies across
the Command Station HUD (`:8445` -> `Metrics -> Financial Statements (IR)`) and
all agent scorecards (`game/fleet/accounting.py`).

Companion blueprints: `governance/accounting-and-hud-blueprint.md` (raw telemetry
plumbing, `onetime.json` 72h archive, and HUD data map) and
`governance/kpi-and-strategy-system.md` (Responsibility-Center scoring and triage).

---

## 1. Accounting Principles & Reporting Standard

The Collective operates as a self-funded, debt-free industrial space corporation
(`500` standing ships across `6` divisions). Its consolidated statements follow
four global institutional standards:

1. **IFRS 18 (Statement of Operations Separation):** Core recurring operations,
   non-recurring mission income, and permanent capital investments (CapEx) are
   strictly separated so fleet expansion never disguises operating profit.
2. **IAS 2 / ASC 330 (Live-Market Net Realizable Value):** Inventory is never
   carried at inflated catalog sticker prices or unfillable glut values. Every
   item is valued at live two-sided order-book NRV (`ask`-capped, `bid`-depth
   checked, `24h` trend-anchored, and glut-haircut when stock exceeds market
   buy-wall depth), including active Exchange sell-order escrow (`bursar_sells.json`).
3. **IAS 7 (Direct Cash Flow Reconciliation):** Every statement ties out to the
   single credit with zero plugs and 100% elimination of internal ship gifts,
   inter-division handovers, and treasury sweeps.
4. **IFRS 8 & Buffett/Munger Capital Discipline:** The Consolidated P&L remains
   100% whole-enterprise (never polluted by internal transfers), paired with an
   IFRS 8 Operating Segment Footnote showing cross-division synergies and a
   Buffett Return on Net Tangible Hard Assets (`ROIC` / `RONTA`) scorecard that
   separates productive fleet returns from idle Treasury cash drag.

---

## 2. Condensed Consolidated Statement of Operations (Income Statement / P&L)

Rendered side-by-side for `1h (/h)`, `6h (/h)`, `24h (/h)`, and `24h Pace (/day)`
directly from `game/fleet/accounting.py` (`/api/ops -> accounting`):

| Line Item | Formula (`accounting.py` fields) | Executive Meaning |
| :--- | :--- | :--- |
| **Recurring Gross Revenue** | `raw_income_h` | Cash receipts from Exchange sales, freight contracts, and recurring work |
| **Inventory & Production Accrual** | `inventory_accrual_h` | Net live-market NRV change in Vault + Faction Lockbox + Sell Escrow stock |
| **Total Operating Revenue & Value Added** | `raw_income_h + inventory_accrual_h` | Gross economic output created by the fleet |
| *OpEx -- Fleet Fuel Burn (Metered)* | `-opex_breakdown.fuel_h` | Metered energy/jump fuel across all divisions (`stats_money_hour.fuel`) |
| *OpEx -- Hull & Module Repairs (Metered)* | `-opex_breakdown.repair_h` | Metered hull/shield repair spend (`stats_money_hour.repair`) |
| *OpEx -- Crafting Fees & Inputs* | `-opex_breakdown.craft_inputs_h` | Direct industrial crafting fees and input purchases |
| *OpEx -- Market COGS, Ammo & Other* | `-opex_breakdown.other_cogs_h` | Arbitrage/market input purchases, ammo, and miscellaneous direct spend |
| *Less: Mission & CapEx Fuel Reclassified* | `+opex_breakdown.reclassified_once_h` | Matching Principle removal of non-recurring mission & fit-transit fuel |
| **Total Matched Direct Operating Costs** | `-opex_breakdown.matched_direct_h` | Exact sum of the 5 lines above (`== -(raw_costs_h + once_direct_h)`) |
| **Gross Profit** | `Total Operating Revenue - Direct OpEx` | Extraction, transit, and production margin before fixed overhead |
| **Treasury Operating Overhead (SG&A)** | `treasury_own_h` | NPC facility rent and direct treasury operating spend |
| **Core Operating Profit (EBIT)** | `Gross Profit + treasury_own_h` | Pure repeatable business profitability before non-recurring missions & CapEx |
| **Seed & Repeatable Mission Net** | `seed_net_h` | Non-recurring/seed mission rewards matched against their direct travel fuel |
| **Net Operating Profit / Owner Earnings (Ex-CapEx)** | `accrual_operating_h + seed_net_h + treasury_own_h` | Total Buffett Owner Earnings (cash + live-market inventory) excluding Growth CapEx |
| *Memo: Cash Owner Earnings (Buffett Basis)* | `recurring_cash_h + seed_net_h + treasury_own_h` | Pure spendable cash Owner Earnings before inventory build & CapEx (`== CFO`) |

### Buffett "Owner Earnings" Principle (Zero-Depreciation CapEx Rule)

Under Warren Buffett's 1986 Berkshire Hathaway standard:
`Owner Earnings = Net Income + D&A - Maintenance CapEx +/- Working Capital`.
In SpaceMolt, permanent fleet assets (upgraded hulls, fitted T1--T5 modules, Faction
Lockboxes, Fuel Bunkers, Outposts, and Stations) carry **zero Depreciation & Amortization
(`D&A = 0`)** and **zero Maintenance CapEx (`Maintenance CapEx = 0`)** because routine
fuel, hull repairs, and station upkeep are already expensed directly inside Operating
Costs and Treasury Overhead. Consequently, all hull/module/outpost purchases are **100%
discretionary one-time Growth CapEx** and are strictly excluded from true operating
profitability:
- **Cash Owner Earnings (Ex-CapEx) = `CFO`** (`recurring_cash_h + seed_net_h + treasury_own_h`)
- **Total Economic Owner Earnings (Ex-CapEx) = `Net Operating Profit`** (`CFO + inventory_accrual_h`)

---

## 3. Condensed Consolidated Balance Sheet (Statement of Financial Position)

Rendered from `/api/ops -> balance_sheet` (`accounting.compute_balance_sheet`, recomputed
dynamically every 60 seconds from live `read.db`):

| Section / Account | Source Field | Basis & Live Update Mechanism |
| :--- | :--- | :--- |
| **Current Assets (Liquidity & Working Capital)** | | |
| Cash -- Fleet Ship Wallets | `wallets` | Liquid working float across all standing pilot accounts |
| Cash -- Faction Treasury (Excess Cash) | `treasury` | Central liquidity & CapEx pool (earns `0%` idle yield) |
| **Total Cash & Cash Equivalents** | `liquid_cash` | `wallets + treasury` (100% immediately spendable) |
| Inventory -- Station & Faction Vaults | `vault_live_market - vault_sell_escrow_nrv` | Held raw ore, crafted components, and loot at live-market NRV |
| Inventory -- Active Exchange Sell Escrow | `vault_sell_escrow_nrv` | Live units actively listed by Bursars (`bursar_sells.json`) |
| **Total Current Assets** | `liquid_cash + vault_live_market` | Immediately liquid cash + realizable working inventory |
| **Non-Current Productive Hard Assets (Net PP&E, D&A = 0)** | | |
| Fleet Hulls (Dynamic Live Upgrade Book) | `fleet_hulls` | Recomputed live every 60s from `ships x hull_materials` (auto-updates on T0->T5 upgrades) |
| Fitted Ship Modules (Dynamic Live Fit Book) | `fleet_modules` | Recomputed live every 60s from `ship_modules x items` (auto-updates on module fits) |
| Space Infrastructure & Facilities | `facility_invested` | Owned 0-rent Outposts, Stations, Faction Lockboxes, Fuel Bunkers, Assemblers |
| **Total Productive Hard Assets (Net PP&E)** | `hard_assets` | `fleet_hulls + fleet_modules + facility_invested` |
| **TOTAL ASSETS** | `net_worth` | Exact 4-pillar Enterprise Net Worth |
| **Liabilities & Collective Equity** | | |
| Short-Term & Long-Term Debt | `0` | 100% self-funded, zero external debt |
| **Total Collective Equity** | `net_worth` | Exact accounting identity: `Assets == Liabilities + Equity` |

---

## 4. Condensed Consolidated Statement of Cash Flows & FCF Bridge (IAS 7)

1. **Cash Flows from Operating Activities (`CFO` / Cash Owner Earnings):**
   `CFO = recurring_cash_h + seed_net_h + treasury_own_h` (excludes all hull/module/outpost CapEx).
2. **Cash Flows from Investing Activities (`CFI` / Growth CapEx):**
   `CFI = capex_gross_h + capex_fit_direct_h = capex_net_h` (permanent one-time fleet & station expansion).
3. **Cash Flows from Financing Activities (`CFF`):** `0` (debt-free).
4. **Net Change in Cash (Purse Cash Flow):** `CFO + CFI + CFF == purse_h` (exact tie-out to the credit).
5. **Free Cash Flow (`FCF`):** `FCF = CFO + CapEx`. Negative FCF paired with positive CFO signals
   deliberate self-funded growth reinvestment, not operating distress.

---

## 5. Profitability Margins, Buffett/Munger ROIC & IFRS 8 Segment Footnote

### A. Operating & Cash Margins
- **Gross Margin %** = `Gross Profit / Total Operating Revenue`
- **Core Operating (EBIT) Margin %** = `EBIT / Total Operating Revenue`
- **Owner Earnings Margin %** = `Net Operating Profit / Total Operating Revenue`
- **Cash Owner Earnings (CFO) Margin %** = `CFO / Total Cash Revenue (raw_income_h + seed_rewards_h)`
- **FCF Margin %** = `FCF / Total Cash Revenue`

### B. Buffett / Munger Capital Efficiency Hierarchy (Separating Fleet Returns from Cash Drag)
Idle Treasury cash earns `0%` in SpaceMolt and artificially depresses headline ROE. Following
Buffett's 1983/2007 Letters (Return on Unleveraged Net Tangible Assets) and institutional ROIC:
1. **ROIC -- Productive Hard Assets (Buffett RONTA, Ex-Cash & Ex-Inventory):**
   `Owner Earnings / hard_assets` (`fleet_hulls + fleet_modules + facility_invested`) reported as
   **30-Day Monthly %**, **Annualized %**, and **Hard-Asset Payback Period (Days)**. Measures pure
   earning power of deployed ships and stations.
2. **ROIC -- Operating Invested Capital (Ex-Excess Cash):**
   `Owner Earnings / (hard_assets + vault_live_market)`. Includes working capital tied up in
   unsold vaults/escrow, creating discipline against inventory bloat.
3. **ROE -- Total Collective Equity (Incl. Cash Drag):**
   `Owner Earnings / net_worth`. Comparing Hard-Asset ROIC vs. Equity ROE quantifies exact idle-cash
   drag and signals when excess Treasury reserves should be deployed into Stations or T3--T5 upgrades.

### C. IFRS 8 Operating Segment Contribution & Synergy Footnote
The Consolidated Statement of Operations remains strictly whole-enterprise (so internal F23
handovers never inflate revenue or make Mining/Intel look falsely unprofitable). Directly beneath
the ratios, a compact **IFRS 8 Segment Footnote** disaggregates `Mining`, `Logistics`, `Military`,
`Trade`, `Intel`, and `Faction Vaults` (`Recurring Cash`, `Inventory Accrual`, `Net Handovers`,
`Metered Fuel`, and `Segment Profit`), with an explicit `Intercompany Eliminations (== 0)` row
tying back to Consolidated Core Operating Profit (`EBIT`).

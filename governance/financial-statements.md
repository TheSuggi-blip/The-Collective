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
reporting The Collective's financial performance, balance sheet position, and
cash generation across the Command Station HUD (`:8445` -> `Metrics -> Financial Statements (IR)`)
and all agent scorecards (`game/fleet/accounting.py`).

Companion blueprints: `governance/accounting-and-hud-blueprint.md` (raw telemetry
plumbing, `onetime.json` 72h archive, and HUD data map) and
`governance/kpi-and-strategy-system.md` (Responsibility-Center scoring and triage).

---

## 1. Accounting Principles & Reporting Standard

The Collective operates as a self-funded, debt-free industrial space corporation
(`500` standing ships across `6` divisions). Its consolidated statements follow
three global institutional standards:

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

---

## 2. Condensed Consolidated Statement of Operations (Income Statement / P&L)

Rendered side-by-side for `1h (/h)`, `6h (/h)`, `24h (/h)`, and `24h Pace (/day)`
directly from `game/fleet/accounting.py` (`/api/ops -> accounting`):

| Line Item | Formula (`accounting.py` fields) | Executive Meaning |
| :--- | :--- | :--- |
| **Recurring Gross Revenue** | `raw_income_h` | Cash receipts from Exchange sales, freight contracts, and recurring work |
| **Inventory & Production Accrual** | `inventory_accrual_h` | Net live-market NRV change in Vault + Faction Lockbox + Sell Escrow stock |
| **Total Operating Revenue & Value Added** | `raw_income_h + inventory_accrual_h` | Gross economic output created by the fleet |
| **Direct Operating Costs (Ex-CapEx)** | `-(raw_costs_h + once_direct_h)` | Matched fuel, repairs, and craft inputs (excludes one-time mission fuel & CapEx) |
| **Treasury Operating Overhead** | `treasury_own_h` | NPC facility rent and direct treasury operating spend (excl. pilot deposits) |
| **Core Operating Profit (EBIT)** | `accrual_operating_h + treasury_own_h` | Pure repeatable business profitability before non-recurring missions & CapEx |
| **Seed & Repeatable Mission Net** | `seed_net_h` | Non-recurring/seed mission rewards matched against their direct travel fuel |
| **Net Operating Profit (Ex-CapEx)** | `accrual_operating_h + seed_net_h + treasury_own_h` | Total enterprise operating profit (cash + live-market inventory) excluding CapEx |
| *Memo: Pure Cash Operating Profit* | `recurring_cash_h + seed_net_h + treasury_own_h` | Cash-only operating profit before inventory build and before CapEx (`== CFO`) |
| *Memo: Metered Fleet Fuel Burn* | `-SUM(by_division[*].fuel_cr_h)` | Transparent energy/transit burn across all six divisions |

---

## 3. Condensed Consolidated Balance Sheet (Statement of Financial Position)

Rendered from `/api/ops -> balance_sheet` (`accounting.vault_valuation` + `store.py`):

| Section / Account | Source Field | Basis & Audit Notes |
| :--- | :--- | :--- |
| **Current Assets** | | |
| Cash -- Fleet Ship Wallets | `wallets` | Liquid credits across all standing pilot accounts |
| Cash -- Faction Treasury | `treasury` | Central capital reserve & automated CapEx funding pool |
| **Total Cash & Cash Equivalents** | `liquid_cash` | `wallets + treasury` (100% immediately spendable) |
| Inventory -- Station & Faction Vaults | `vault_live_market - vault_sell_escrow_nrv` | Held raw ore, crafted components, and loot at live-market NRV |
| Inventory -- Active Exchange Sell Escrow | `vault_sell_escrow_nrv` | Live units actively listed by Bursars (`bursar_sells.json`) |
| **Total Current Assets** | `liquid_cash + vault_live_market` | Immediately liquid cash plus realizable working capital |
| **Non-Current (Fixed) Assets** | | |
| Fleet Property & Equipment | `fleet_book` | Standing hulls and fitted modules at replacement book basis |
| Space Infrastructure & Facilities | `facility_invested` | Owned 0-rent Outposts (`Atria`, `GSC-0044`) & station facilities |
| **Total Non-Current Assets** | `fleet_book + facility_invested` | Permanent productive capital base |
| **TOTAL ASSETS** | `net_worth` | `Total Current Assets + Total Non-Current Assets` |
| **Liabilities & Collective Equity** | | |
| Short-Term & Long-Term Debt | `0` | 100% self-funded, debt-free enterprise |
| **Total Liabilities** | `0` | Zero external credit obligations |
| **Total Collective Equity (Net Worth)** | `net_worth` | Exact accounting identity: `Assets - Liabilities == Equity` |

**Mandatory Audit Footnotes:** The Balance Sheet always discloses the Valuation
Schedule alongside Net Worth: `Live-Market NRV Vault`, `IAS 2 Static Base`,
`Instant Bid-Depth Liquidation`, `Leaderboard Catalog Net Worth`, `24h Handovers`,
and any active **Glut Haircuts** (`vault_gluts`) so neither agents nor leadership
mistake illiquid gluts for spendable cash.

---

## 4. Condensed Consolidated Statement of Cash Flows & FCF Bridge (IAS 7)

| Section / Line Item | Formula (`accounting.py`) | Governance Role |
| :--- | :--- | :--- |
| **Operating Activities (CFO)** | | |
| Recurring Cash from Operations | `recurring_cash_h` | Matched steady operating cash flow |
| Mission & Contract Cash (Net) | `seed_net_h` | Repeatable & seed mission cash net of fuel |
| Treasury Rent & Direct Flows | `treasury_own_h` | NPC rent & direct treasury operating flows |
| **Net Cash Provided by Operating Activities (CFO)** | `recurring_cash_h + seed_net_h + treasury_own_h` | **True Ex-CapEx Cash Generation** |
| **Investing Activities (CFI / CapEx)** | | |
| Capital Expenditures (Gross) | `capex_gross_h` | Permanent hulls, modules, and outpost purchases |
| Module Fit Salvage & Transit | `capex_fit_direct_h` | Salvage proceeds less upgrade travel fuel |
| **Net Cash Used in Investing Activities (CFI)** | `capex_net_h` | Total net capital reinvestment |
| **Financing Activities (CFF)** | `0` | No external borrowing or equity issuance |
| **Net Change in Cash (Purse Cash Flow)** | `purse_h` | Exact identity: `CFO + CFI + CFF == purse_h` |
| **Free Cash Flow (FCF, Non-GAAP IR Bridge)** | `CFO + capex_net_h` | Cash retained after funding all growth CapEx |
| **Total Economic Wealth Creation** | `CFO + inventory_accrual_h` | Ex-CapEx cash plus live-market inventory build |

**Critical Interpretation Rule:** Negative `FCF` (`purse_h < 0`) while `CFO > 0`
and `Net Operating Profit > 0` means the enterprise is **deliberately reinvesting
operating profits into permanent fleet/outpost expansion**, NOT losing money.
True operational distress occurs only when `CFO < 0` and `Core Operating Profit < 0`
simultaneously across the `24h` window.

---

## 5. Corporate Operating Model & Capital Allocation Guardrails

To keep CFO positive while compounding Net Worth across all six divisions:

1. **Responsibility-Center Accountability (`Metrics -> Overview`):** The
   `By division (GAAP/IFRS accrual & cash)` table sits at the top of `Metrics -> Overview`
   above the 10 headline KPI boxes so every division's `Recur Cash/h`, `Inv Build/h`,
   `Transfers/h` (eliminating to `0` at Fleet Total), `Accrual Op/h`, and `Purse Net/h`
   are immediately visible. Upgrades (CapEx) NEVER penalize division scorecards.
2. **Dynamic Cross-Docking (Minimal Cash-to-Cash Cycle):** `handover.py` auto-resolves
   all live staffed Bursars (`bursar_claims.json`), and both `mine_net.py` and `hunt_net.py`
   prioritize staffed Bursar hubs so market ore and combat loot move straight into live
   Exchange sell orders with zero manual `give-loot-*` routing.
3. **Hub-and-Spoke 0-Rent Outpost Consolidation:** `mine_net.py` (`10%` belt floor,
   `T0 == T2` safe access) and `haul.py` auto-discover CLTV Owned Outposts (`Atria`,
   `GSC-0044`, and future builds) via `read.db:faction_facilities`, depositing reserves
   via `--deposit faction` and pulling stacks home in parallel via `internal_supply` and
   `liquidate_surplus`, backed by zero-idle pre-bought `backhaul_mission` contracts.
4. **Capital Allocation Floor (`game/upgrade-policy.json`):** Autonomous hull/module
   CapEx scales dynamically (`2.5M/24h` cap) strictly above the `8.0M cr` Treasury
   liquidity floor, guaranteeing uninterrupted fuel, trade float, and expansion readiness.

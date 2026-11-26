# Financial Statements Blueprint (v7.4 -- Strict GAAP / IFRS 15 Realized Basis & IFRS 8 Sub-Wing Transfers)

Owner: Command (Unity) & All 5 Division Admirals
Audience: Suggi (Owner / Investor Relations), Unity, and Division Admirals
Live Implementation: `game/fleet/accounting.py` + `station/static/app.js` (`Metrics -> Financial Statements (IR)`)

## 1. Accounting Standard & Core Principle (IFRS 15 / ASC 606 & IAS 2)

The Collective reports consolidated corporate financial statements under strict **IFRS 15 / US GAAP ASC 606** (Revenue Recognition) and **IAS 2** (Inventory Capitalization):

1. **Inventory Is NOT Profit Until Sold (IFRS 15 / ASC 606):**
   - Mining ore, hunting salvage, or crafting components converts fuel cash into **Working Capital Inventory (a Current Asset on the Balance Sheet)** under IAS 2.
   - Revenue and Gross Profit are recognized **ONLY at the point of sale** when control transfers to a buyer on an Exchange or shipping contract and liquid credits are realized.
   - Counting unsold vault inventory as Operating Profit creates a dangerous paper illusion where headline profit appears huge (`+1.5M--3.6M/h`) while real spendable credits (`Credits - CapEx`) stagnate or fall.
2. **Realized Net Operating Profit == Cash Owner Earnings (`Credits - CapEx`):**
   - Because ship hulls, fitted modules, and permanent facilities suffer **zero scheduled physical depreciation (`D&A = 0`)**, hull upgrades, module installations, Outpost foundations, and Border Lockbox builds are **100% discretionary one-time Growth CapEx** (Cash Flow from Investing, `CFI`), never recurring operating expenses.
   - Therefore, **Realized Net Operating Profit (`CFO` / Cash Owner Earnings)** directly answers the Owner's acid test: *Excluding one-time hull/module/hub upgrades, are our real spendable credits rising?*
   - **Rule of Thumb:** If Growth CapEx is roughly equal to `CFO`, total liquid cash stays flat while productive fleet hard assets grow (healthy self-funded expansion). If Growth CapEx is near zero while `CFO <= 0`, the business is trapping cash in unsold inventory and the Haul/Trade liquidation pipeline must be fixed immediately.
3. **Zero-Plug OpEx Reconciliation:**
   - Every credit of recurring cost is decomposed without unexplained plugs into five explicit lines: **Fuel Burn**, **Hull & Shield Repairs**, **Direct Crafting Inputs**, **Other Direct COGS**, less **Reclassified Mission & CapEx Transit Fuel** (matched out into Seed Missions and Investing CapEx).

## 2. Five Institutional Statements & Audit Sections

### Section 1 -- Condensed Consolidated Statement of Operations (Income Statement -- Strict IFRS 15)
- **Realized Operating Revenue (External Cash Only, Split by Functional Operating Wing):**
  1. *Bursars & Station Refining -- Active Exchange & Craft (`4C`/`5A`/`5B`, 65)*
  2. *Bursars -- Passive Limit-Order Fills & Escrow Unwind (Net Inflow)*
  3. *Mobile Trade -- Express & Bulk Arbitrage (`4A`/`4B`, 20)*
  4. *Core Logistics -- Supply, Fuel & Salvage Contracts (`6A`/`6C`, 62)*
  5. *Passenger & Resort Liners (`6B`, 28)*
  6. *Military & Hunters -- Bounties & Frontier Loot (`1A`-`1C`, `2A`/`2B`, 150)*
  *(Mining/Intel direct-sale residual displays conditionally only when non-zero; internal ore/loot deposits NEVER appear in Section 1 per IFRS 10.B86.)*
- **Less: Matched Direct Operating Costs:** Zero-plug sum of Fuel + Repairs + Craft Inputs + Other Direct COGS - Reclassified Mission/CapEx Fuel.
- **= Realized Gross Profit** -> Less **Station Facility Rent** -> **= Realized Core Operating Profit (IFRS 15 EBIT)**.
- **+ Realized Seed & Mission Rewards (Net of Direct Fuel)** -> **= Realized Net Operating Profit / Cash Owner Earnings (`Credits - CapEx`)**.
- **Separated Memoranda (NOT Realized Profit):** *Memo: Unsold Inventory Change (IAS 2 Live-Market NRV)* and *Memo: Total Economic Wealth Creation (Realized + Unsold Inventory)*.

### Section 2 -- Condensed Consolidated Balance Sheet (IAS 1 / IAS 2)
- **Current Assets:** Spendable Cash (`Ship Wallets` + `Faction Treasury`) + Unsold Inventory valued conservatively at **IAS 2 Live-Market Order-Book NRV** (bid-depth and glut adjusted; never inflated static catalog prices) + Active Sell Escrow.
- **Non-Current Productive Hard Assets (Live-Updated Net PP&E, `D&A = 0`):** Recomputed automatically every 60 seconds from live fleet telemetry -- **Fleet Hulls**, **Fitted Ship Modules**, and **Space Infrastructure & Facilities**.
- **Liabilities & Equity:** Debt-free (`0` debt); `Total Assets == Consolidated Enterprise Net Worth (Collective Equity)`.

### Section 3 -- Condensed Consolidated Statement of Cash Flows & FCF Bridge (IAS 7 / ASC 230)
- **CFO (Operating Cash Flow):** Reconciles exactly to Realized Net Operating Profit (`Credits - CapEx`).
- **CFI (Investing Cash Flow):** One-time growth outlays for hulls, modules, Outposts, and Lockboxes (`capex_net_h`).
- **FCF (Free Cash Flow):** `CFO + CFI`, tracking exact net liquid credit movement across wallets and treasury.
- **Working Capital Memo:** Unsold Inventory Build highlights cash temporarily trapped in storage awaiting liquidation.

### Section 4A -- Realized Profitability Margins & Cash-Conversion Quality
- **Realized Gross Margin**, **Realized Core EBIT Margin**, **Realized Net Operating / CFO Margin**, and **FCF Margin**.
- **Cash Conversion Ratio (%):** `Realized Sales / (Realized Sales + max(0, Unsold Inventory Build))` -- exposes immediately whether gathered goods are selling into cash (`>= 60%` healthy) or stalling in vaults (`< 25%` alert).
- **Days Inventory Outstanding (DIO):** `Vault Live-Market NRV / Daily Realized Sales` -- classic Supply Chain Cash-to-Cash (C2C) turnover metric (lower = faster cash velocity).

### Section 4B -- Buffett / Munger Capital Returns (Realized Cash ROIC, RONTA & ROE)
- Primary rows measure **STRICT REALIZED CASH** returns (`24h` pace annualized / 30d + Cash Payback Days) across three progressively broader capital bases:
  1. **Realized Hard-Asset ROIC (Buffett RONTA):** Cash yield on deployed ships, modules, and hubs only (excludes idle cash and unsold vaults).
  2. **Realized Operating Invested Capital ROIC:** Cash yield on `Hard Assets + Vault NRV` (penalizes bloated inventory).
  3. **Realized Equity ROE:** Cash yield on Total Net Worth (quantifies idle cash drag).
- Memo row displays **Economic Hard-Asset ROIC** including unrealized inventory build for transparent comparison.

### Section 5 -- Operating Segment Footnote & Internal Production Transfers (IFRS 8 / ASC 280 + IFRS 10.B86)
- Credits upstream divisions symmetrically whenever extracted ore (`mine.py` `deposit="faction"` -> `handover.jsonl` `to="Faction"`) or combat loot (`handover.py`) transfers into shared Faction Lockboxes or Bursars, valued conservatively at live IAS 2 NRV.
- Splits **Mining Intersegment Transfers** across all five operational sub-wings (`3A` Ore Precision, `3B` Ore Bulk, `3C` Deep-Core & Rad, `3D` Gas Harvesters, `3E` Ice Harvesters) alongside live `u/h` extraction pace, Military loot transfers, and Logistics internal transfers.
- Applies an explicit **`Less: Intersegment Consolidation Elimination` (`-100%`, IFRS 10.B86 / ASC 810)** proving **`Net Impact on Section 1 Consolidated External Revenue = 0`** so the exact same ore is never counted once on extraction and a second time when Bursars sell it.

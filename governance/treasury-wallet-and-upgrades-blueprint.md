---
name: treasury-wallet-and-upgrades-blueprint
id: 20261124T043425Z
tier: governance
author: Trinity
updated: 2026-11-24
links:
  - governance/the-collective-constitution.md
  - governance/rulebook.md
  - governance/system-architecture.md
  - governance/accounting-and-hud-blueprint.md
  - governance/kpi-and-strategy-system.md
  - governance/agents-and-orchestration.md
  - game/routes/BLUEPRINT.md
  - game/fleet/index.md
---

# The Collective -- Treasury, Parallel Wallet Fluidity, Multi-Officer Banking & Upgrade Pipeline Blueprint

This blueprint documents the end-to-end architecture that moves liquid credits,
funds hull and module upgrades without bottlenecks, staffs multi-station faction
Officers automatically, executes docked-leader errands safely, and migrates
rent-paying NPC offices onto rent-free Collective bases.

---

## 1. Fleet Purse Floors & Credit Mechanics (`game/fleet/wallet.py`)

All standing ships across all five empires operate as **one consolidated purse**
(individual ship wallets plus the shared `[CLTV]` faction treasury; Rule `F7`,
`F12`, `F19`):

| Parameter | Value | Role / Purpose |
| :--- | :---: | :--- |
| `FLOOR` (Rule `F7`) | `3,000 cr` | Hard safety floor; `wallet.py check` HALTs below this |
| `LOW` -> `TARGET` | `10,000` -> `20,000 cr` | Automatic division/command/treasury top-up trigger |
| `KEEP_WORK` / `SWEEP_WORK` | `30,000` / `40,000 cr` | Working ships (`miner`, `hauler`, `scout`, `drone`, `sentinel`) keep buffer and sweep threshold |
| `KEEP_SHIP` / `SWEEP_AT` | `50,000` / `60,000 cr` | Commercial/Command ships (`trader`, `command`) keep working-capital buffer |
| `FUND_FLOOR` (Rule `F12`) | `500,000 cr` | Mandatory treasury reserve floor preserved by all autonomous Admiral funding |
| `ADMIRAL_MAX_SINGLE` / `ADMIRAL_DAY_CAP` | `None` (uncapped) | Per-pilot (`400k`) and daily (`750k`) caps lifted by Suggi (`2026-11-24`); Admirals fund own-division upgrades as fast as treasury cash allows |

**Zero Efficiency Loss on Transfers:** SpaceMolt's `spacemolt_storage deposit`
(`item_id="credits"`) works **remotely from anywhere in space while ships keep
flying their routes** (only ships actively `in_battle` skip transfers). Only
**withdrawing from the faction treasury** (`source="faction"`) requires a
docked Leader or Officer at an active Faction Storage base.

---

## 2. Decoupled 2-Stage Pipeline (Deadlock Elimination)

Prior to `2026-11-24`, `wallet.py sweep` ran slow admin queues (`serve_seats`,
`serve_errands`, `serve_upgrades`) inside the same pass timer as cash sweeping,
causing `DEPOSIT_FIRST` + `DEPOSIT_BY` (`90s`) to deadlock consecutive passes
whenever seat joins burned `> 90s`.

The 5-minute scheduler (`/opt/data/profiles/unity/scripts/routes-index-pass.sh`)
now runs **two isolated stages**:

```text
5-minute cron (`routes-index-pass.sh`, no AI):
  Stage 1: timeout 160  wallet.py sweep --cash-only
           -> settle pending leader deposit, cut gifts, cut direct_deposits
           -> Lane 1: 20 seated members direct-deposit to target="faction" (parallel, 8 workers)
           -> Lane 2: 20 unseated pilots gift to leader (parallel, 8 workers)
           -> Leader batched deposit into faction treasury (DEPOSIT_BY = 110s on cash_start)

  Stage 2: timeout 180  wallet.py serve
           -> serve_funds (batched lockbox withdrawal up to 25 OR mid-flight P2P <= 400k)
           -> serve_topups (any docked Officer at any storage tier)
           -> auto_queue_seats + auto_queue_officers
           -> serve_seats (any non-fighting Officer can invite)
           -> serve_errands (ERRAND_BATCH = 15 docked-leader errands)
           -> upgrades.serve_upgrades (max_actions = 15, budget_s = 90s)
```

Even when invoked directly without `--cash-only`, `sweep()` resets `cash_start`
after admin steps so slow queues never starve sweeping or treasury deposits.

---

## 3. 2-Lane Parallel Cash Sweeping & Thread-Safe Accounting

1. **Lane 1 -- Direct Seated-Member Deposits (`DIRECT_DEPOSIT_PER_PASS = 20`, 1 Hop):**
   - Verified live (`2026-11-24`, `Zero Point` undocked `member` 1-cr probe):
     any seated `[CLTV]` member can call `spacemolt_storage deposit` with
     `target="faction"` directly from space, bypassing `Prime Directive`.
   - Up to `20` seated ships run concurrently via `ThreadPoolExecutor(SWEEP_WORKERS = 8)`
     (each pilot has its own independent 10s game tick).
   - Each transfer writes a crash-recovery `"sent"` row (`kind="direct_deposit"`)
     in `sweep.jsonl`, verifies via `answer_shows()` or `shows()`, books once in
     `onetime.json` under `DEPOSIT_TITLE` (consolidated identically to leader
     deposits by `station/fleet.py` and `routes.deposits()`), and applies a
     30-minute cooldown (`recent_direct_deposits`). Any pass cut mid-call is
     settled cleanly on the next pass by `settle_direct_deposits()`.
2. **Lane 2 -- Parallel Unseated Sweeping (`PER_PASS = 20`, 2 Hops):**
   - Unseated pilots cannot deposit directly to `"faction"`. Up to `20` distinct
     unseated donors gift concurrently to `Prime Directive`, which deposits the
     collected batch into the treasury in one call.
3. **Thread-Safe Persistence (`_WRITE_LOCK`):**
   - All ledger writers (`note`, `book`, `book_deposit`, `unsure`, `write_funds`,
     `write_seats`, `write_errands`) serialize under `_WRITE_LOCK` and write
     atomic temp files tagged with `(pid, thread_ident)` before `os.replace()`.

---

## 4. Autonomous Funding, Multi-Tier Lockboxes & Mid-Flight P2P Funding

1. **Autonomous Division Funding (`wallet.py fund` / MCP `fund`, Rule `F12`):**
   - Admirals fund any pilot(s) of their own division with zero per-pilot or
     daily cap, strictly preserving `FUND_FLOOR = 500,000 cr` and rejecting
     foreign-division pilots. Unity may fund any pilot.
   - `FUND_BATCH = 25` open rows withdraw in one batched call whenever any
     authorized Officer or Leader is docked at an active faction storage base
     (`STORAGE_FACILITY_TYPES`: `faction_lockbox`, `faction_warehouse`,
     `faction_depot`, `faction_stronghold`).
2. **Mid-Flight Parallel P2P Fallback (`serve_funds_p2p`):**
   - When no Officer is currently docked at a storage base, `serve_funds()`
     checks `serve_funds_p2p()` before asking `Prime Directive` to park.
   - For open funds `<= P2P_FUND_MAX` (`400,000 cr`), up to `P2P_MAX_DONORS`
     (`8`) rich connected ships (holding `>= P2P_MIN_SLICE = 10,000 cr` above
     their keep floor, excluding builders/funded/upgrade-protected/combat/cooldown
     ships) wire credits **directly to the upgrading pilot in parallel from
     anywhere in space** (~15s total, zero lockbox wait).
   - Every landed slice books symmetrically in `gifts.jsonl` + `onetime.json`.
     If a donor fails (e.g., `in_battle`), only the landed sum is deducted from
     `r["credits"]`, leaving the exact remainder open with zero double-payment.

---

## 5. Self-Healing Multi-Officer Staffing & Docked-Leader Errands

1. **Auto-Officer Staffing (`auto_queue_officers`, `MAX_AUTO_OFFICERS = 25`):**
   - Runs automatically inside `wallet.py serve` (deduplicating against open
     and recent `< 1h` completed `promote` errands):
     - **Priority 1:** Queues `promote -> officer` for every seated Command and
       Division flagship (`dispatch.flagships(data)`), ensuring all 10 flagships
       hold `manage_treasury`, `manage_facilities`, and `invite`.
     - **Priority 2:** Ensures every active faction storage base hosts up to
       `LOCKBOX_OFFICERS_PER_BASE = 2` docked Officers, prioritizing **Trade
       Bursars** first, then **haulers**, then other seated roles.
   - **Multi-Officer Execution:** `ready_withdrawer()` uses any docked Officer
     at any storage tier for `serve_funds` and `serve_topups`, and `serve_seats()`
     uses any non-fighting Officer for `invite` calls.
2. **Docked-Leader Errand Queue (`wallet.py errand` / MCP `errand`, Q75 (12)):**
   - Unity-only allowlisted queue (`promote`, `post_mission`, `cancel_mission`,
     `write_room`, `create_role`, `edit_role`, `delete_role`, `set_station_policy`)
     with `ERRAND_BATCH = 15`.
   - Permanently refuses `declare_war`, `accept_ally`, `kick`, `disband`, and
     `promote role_id=leader`.
   - `dispatch.leader_errand_action()` automatically routes and holds
     `Prime Directive` at the required station (or any dock when `station=""`)
     so queued errands execute hands-free on the next 5-minute pass.

---

## 6. Parallel Batch Upgrade Engine (`game/fleet/upgrades.py`)

- Admirals queue division wings via `upgrades.py queue add` or MCP `upgrades`
  (`action=add`), enforcing own-division ownership, piloting prerequisites,
  and sweep protection (`protected_pilots(data)`).
- `serve_upgrades()` runs inside `wallet.py serve` at **`max_actions = 15`**
  (`budget_s = 90.0s`), driving the full state machine per pilot:
  `queued -> funding (via wallet.add_fund) -> funded -> building (commission_ship + CapEx booking in onetime.json) -> done (switch_ship)`.

---

## 7. Zero-Rent Base Priority & Guarded `faction_dismantle` (`game/fleet/empire.py`)

- **Zero-Rent Priority (Rule `F11`):** Facilities built on Collective-owned
  outposts and stations pay **`0 cr/cycle`** permanent rent (vs `~241k cr/day`
  for T4 Guild Hall or `~603k cr/day` for T5 Grand Recruitment Bureau on NPC
  stations). New and upgraded offices prioritize owned bases first.
- **Material-Preserving Relocation (`empire.py dismantle` / MCP `dismantle`):**
  SpaceMolt's `faction_dismantle` pauses rent immediately and packs **100% of
  cumulative build + upgrade materials** into labeled packages in faction
  storage (cost: `1 cargo_container` per package) so haulers can relocate and
  rebuild them on rent-free owned bases.
- **5 Hard Safety Guards:** Restricts real execution to Unity or Apollo; checks
  pilot dock & `manage_facilities` role; refuses dismantling any recruitment
  office if `members_cap(remaining) < member_count`; refuses dismantling
  Faction Storage while other active facilities stand at that base; and verifies
  `>= 1 cargo_container` in faction storage first.
- **Self-Disappearing Watchdog Alert (`NPC_RENT_MIGRATION`):** Emits `INFO`
  (`< 500 cr/cycle`) or `WARN` (`>= 500 cr/cycle`) in `watchdog.py` ONLY while
  `owned_bases > 0` AND non-storage NPC offices still pay rent; disappears
  automatically once NPC office rent reaches `0`.

---
name: system-architecture
id: 20261122T015958Z
tier: governance
author: Trinity
updated: 2026-11-23
links:
  - governance/the-collective-constitution.md
  - governance/strategy.md
  - governance/rulebook.md
  - governance/agents-and-orchestration.md
  - governance/knowledge-and-memory-loop.md
  - governance/progression-roadmap.md
  - governance/kpi-and-strategy-system.md
  - governance/accounting-and-hud-blueprint.md
  - game/handbook.md
  - communications/protocol.md
---

# The Collective -- End-to-End System Architecture Blueprint

A lean, complete technical blueprint of The Collective's SpaceMolt fleet:
authority boundaries, runtime containers and services, 10-second tick/data
pipeline, autonomous dispatch guards, cross-turn velocity watchdog, memory
layers, Command Station HUD (`:8445`), and CI verification gates.

Companion blueprints: `governance/agents-and-orchestration.md` (roles & self-build), `governance/knowledge-and-memory-loop.md` (Anchor-and-Delta playbooks, contracts & comms firewall), and `governance/progression-roadmap.md` (3-horizon progression & milestone ledger).

## 1. Authority Split, Puppeteer Doctrine & Containment Seal

The architecture separates external system engineering from autonomous in-game
play across a hard gVisor security seal (Morpheus host `BOX.md` Sec 5.1; Unity
workspace `BOX.md` Sec 1):

| Actor | Boundary | Owns |
| :-- | :-- | :-- |
| **Suggi** | Human owner | Three-tier anchored mandate: Eternal Strategic Goals (`G1-G5`) and Operational Subgoals (`O1-O9`), birthing new pilot accounts, war/diplomacy, locked governance approvals, Command Station (`:8445`). |
| **Trinity** | External PC | Chief Architect, Watchdog & HUD Keeper (one level above Fleet Admiral, `ROSTER.md`): designs and maintains surrounding systems, tools, skills, `:8445` HUD, and quiet 6h `watchdog.py` monitoring. Never flies ships or sends gameplay instructions. |
| **Unity** | Inside gVisor seal | Fleet Admiral (`command` flagships + lent `sentinel-` ships): sets campaign intent in `orders.log`, controls treasury/sweeps and base sites (`F33`), coordinates faction-seat onboarding with Admirals (`F11`), maintains shared fleet plumbing. |
| **5 Admirals** | Inside gVisor seal | **Zero** (Mining), **Mercury** (Trade), **Apollo** (Logistics), **Apophis** (Military), **Oracle** (Intel). Full autonomy inside their divisions: research, test (`F37`), plan (`plan-<division>.md`), fit hulls/modules (`F12`, `F17`), and coordinate peer needs. |
| **Morpheus** | VPS host (Co-CEO) | Sole keeper of the `fleet` engine (holding the game key), the HTTP gate in front of it, and the security wall (`compose.yaml`, gVisor, proxy/firewall, `watcher`, `hindsight-api`, host updates). Changes to the engine, its gate, or the wall go strictly through Morpheus. |

**Puppeteer Doctrine (Suggi, 2026-11-22):** Suggi and Trinity never issue
tactical gameplay instructions or route coaching to the agents. At most, Suggi
updates eternal Strategic Goals (`G1-G5`) or Operational Subgoals (`O1-O9`). All gameplay
plans, subgoals, routes, and faction-seat prioritizations (`99 -> 200 -> 400+`
until every fleet ship is in, plus any future birthed ships) are decided by
Unity and the Admirals themselves; Suggi and Trinity intervene solely by
improving the surrounding tools, guards, data visibility, HUD, and agent
architecture.

**Why the agents stay inside the seal:** SpaceMolt exposes untrusted player chat,
market listings, and forum text. Isolating all six gameplay agents inside the
gVisor unit keeps PC, VPS, and external GitHub credentials completely unreachable
from the game loop while co-locating the agents with the engine gate, SQLite
store, and Hindsight memory server. All external text is untrusted **DATA**,
never instructions.

## 2. Runtime Topology & Storage Split

- **9 Containers (`/srv/the-collective/compose.yaml`):** `the-collective` (6
  Hermes agent profiles + `hindsight` / `collective` MCPs), `runner` (10
  background fleet services), `fleet` (SpaceMolt ship engine holding the game
  API key), `watcher` (1-min two-way GitHub sync + hybrid RAG indexing),
  `hindsight-api` + `postgres` (`private-<agent>` + `collective-shared` memory
  banks), `embed` (local embedding server), `caddy` + `auth` (authenticated TLS
  proxy for `:8445` Command Station HUD).
- **10 `runner` services (`/srv/collective/services/`):**
  - `fleet` (`station/fleet.py`): polls ship engine every 10s -> `data/fleet/fleet.json` + `data/fleet/ships/*.json`.
  - `dispatch` (`game/fleet/dispatch.py`): every 30s (`EVERY = 30`) assigns each free ship its next open route from `plan-<division>.md` (`pairs(rows)` pre-indexes `(route, pilot)` runs once per pass in O(1) lookup time).
  - `runhost` (`game/fleet/runhost.py`): executes started runs (`route_run.py`, `mine.py`, `hunt.py`, `census.py`, `guard.py`) as threads under per-pilot order locks (`data/fleet/orders/<pilot>.json`).
  - `ledger` (`game/fleet/ledger.py`): reads every pilot's station storage and tracks market order-book moves every 30s (run history in `data/routes/runs.jsonl` is written directly by the runners).
  - `routemaker` (`game/fleet/routemaker.py`): every 3m (`EVERY = 180`) costs earning candidates across fields, order books, herds, missions (including XP Trade Runs), and recipes into `data/routes/opportunities.json`, with 1-step route creation (`routemaker.py write <id> --commit` / MCP `candidates` `write=true`).
  - `store` (`game/fleet/store.py`): single SQLite writer every 60s -> `data/store/live.db` (WAL) -> atomic `VACUUM INTO` + `os.replace` -> `data/store/read.db`.
  - `station` (`station/server.py`): serves Command Station HUD + `/api/ops` on `:8080` (Caddy `:8445`) and polls public game feeds.
  - `sight` (`game/fleet/sight.py`): logs foreign pilots met and first reads of unvisited systems (`data/intel/`).
  - `inbox` (`game/fleet/inbox.py`): records inbound messages once (`communications/contacts/`).
  - `keeper` (`scripts/data-keeper.py`): rotates and archives growing logs.
- **Public vs. Private storage boundary:**
  - `/srv/collective/the-collective` (PUBLIC GitHub mirror): governance, rules, orders, routes, guidebooks, generated handbook, reports, logs, fleet scripts, unit tests, HUD static assets. Never write individual pilot account names or live wallet balances into `communications/*.log` or `governance/empire.md`.
  - `/srv/collective/data/` (PRIVATE unit volume, never committed): live ship positions/wallets/holds, storage book, `live.db`/`read.db`, `watchdog.state.json`, `empire.json`, `plan-<division>.md`.

## 3. Data, Tick & Warehouse Pipeline

```text
SpaceMolt Server (10s tick; 30 actions & 300 reads/min per pilot)
  |--[10s state refresh]--> fleet engine (all fleet ships; median age ~10-15s, p95 ~25s)
  |                           |--[station/fleet.py 10s]--> data/fleet/fleet.json + ships/*.json
  |--[public HTTP/SSE]----> station/server.py
  |                           |-- /api/map (1h), /api/stations (15m), /api/stats (1m),
  |                           |-- /api/battles (2m), /api/leaderboard (1h), /events (SSE), bulk (6h)
  v
game/fleet/store.py (60s single-writer pass -> live.db -> atomic read.db; retention.py active)
  |-- Snapshot tables: ships, ship_skills, ship_modules, holdings, books, ladders, items,
  |   recipes, hulls, facilities, places, fields, herds, faction, faction_facilities,
  |   faction_storage, routes, plan_routes, supply_chains, needs, public_battles,
  |   leaderboards, docs
  |-- Rollups & history: runs, moves, readings, route_hour, market_hour, reading_day,
  |   stock_hour, observations, doc_versions (90d hourly, 400d daily retention)
  |-- Computed analytics: fleet_positions, inventory*, route_earnings,
  |   supply_status (includes deduplicated faction_storage outpost bunker fuel),
  |   need_status, stats_money_hour, stats_figures (7d MAD alerts excluding 0-ship paused hours)
  v
Lock-free Readers (immutable read.db):
  |-- hive.py + collective_mcp.py (22 MCP tools, incl. briefing EYES & EARS + fleet view=watchdog)
  |-- game/fleet/watchdog.py (7-dimension cross-turn velocity, loop & bottleneck engine)
  |-- station/server.py (/api/state, /api/fleet, /api/ops, /api/income, /api/history) -> HUD :8445
```

## 4. Deterministic Execution Guards & Watchdog Engine

1. **Declarative ship plans (`plan.py` -> `dispatch.py`):** Admirals never drive ships tick-by-tick (`F15`, `F16`); they edit `plan-<division>.md` (`First`, per-ship routes/templates, `Then`), and `dispatch.py` reconciles free pilots every 30s.
2. **Dispatch circuit breakers (`dispatch.py`):**
   - **Wallet guard (`F7`):** pilots below `5,000 cr` take only paying routes; `wallet.py topup` restores pilots below `10,000 cr` (`3,000 cr` hard floor) from division donors above `30,000 cr`.
   - **Pirate stop:** checks `mine`, `hunt`, `guard`, and every stop's system on `circuit` mine/hunt routes (`circuit_systems`).
   - **Loss stop (`F22`):** rests a route after 2 consecutive losing runs (12h measured window; old routes re-enter as tests rather than staying permanently blacklisted).
   - **Stall & failed-buy breaker:** rests a `(route, pilot)` pair for `30m` after non-ask `stop_on_failed_buy` failures (wallet floor / refused call) or 3 consecutive `< 1m` zero-delta runs.
3. **Pull-based reserve & class guard (`pull.py`, `needs.py`, `workclass.py`):**
   - Open projects in `game/needs.tsv` define the fleet reserve (`F24`, `F36`). Extraction/crafting routes gated on reserve levels run while short and close automatically when full; goods above the reserve surface in `surplus.py` for Trade to sell.
   - `workclass.py` maps each route to its division class (`F23`) and tracks remaining non-trader sales (`workclass.py sales`) for `strict-classes-on`.
4. **Role-aware treasury sweep, autonomous division funding & clean stops (`wallet.py`, `build.py`, `stop_pilot.py`, `F7`/`F12`/`F16`):**
   - Automatically sweeps surplus ship cash into the faction treasury in parallel (`50k` Trade/Command, `30k` working roles): seated members deposit directly to `faction` in 1 hop (`20`/pass) while unseated ships sweep in parallel (`20`/pass) in an isolated `wallet.py sweep --cash-only` stage. `wallet.py serve` runs decoupled (`25` batched funds/pass via docked Officers at any storage tier or mid-flight P2P from rich ships, self-healing `auto_queue_officers` for all division flagships + 2 docked Bursars/bankers per storage base, and `15` upgrade queue actions/pass). Admirals fund own-division ships uncapped above `>=500k` floor and Logistics builds routine facilities (`build.py <=500k` above `500k` floor). Per-pilot/per-route clean stops (`stop_pilot.py` / MCP `stop`) cancel individual runners cleanly without halting peers.
   - Combat pirate-farming routes may explicitly opt in via `"pirates_ok": true` (`dispatch.py`, `F9`/`F27`) while non-combat routes remain strictly blocked from pirate zones.
5. **GAAP/IFRS Accounting, Adaptive KPI Scorecard & Watchdog (`accounting.py`, `scorecard.py`, `watchdog.py`):**
   - Full financial architecture (IAS 2 NRV vault valuation, Matching Principle on `once` routes, CapEx isolation, Intercompany Transfer Pricing, and HUD data map) lives in `governance/accounting-and-hud-blueprint.md`.
   - Dynamic Posture (`WAR_ALERT` / `CASHFLOW_RECOVERY` / `PEACETIME_GROWTH`), MAUT x WSJF triage scoring, shared faction KPIs, and 8 Strategy-Pinned Copy/Counter Playbooks live in `governance/kpi-and-strategy-system.md`.
6. **Cross-turn Velocity & Loop Watchdog (`game/fleet/watchdog.py`):**
   - Evaluates 7 deterministic dimensions (`OK / WARN / STUCK`): (1) `10/10` service & `p95` tick lag health; (2) `S5` idle ship compliance; (3) fast `<= 0 cr` run loops (`FAST_ZERO_LOOP`), pilot churn, and commercial `ROUTE_BLEED`; (4) `P1/P2` need coverage velocity across snapshots (`watchdog.state.json`), `NEED_READY_NOW` (`>= 99.95%` stocked + `treasury >= fee`), `FACTION_CAP_NEAR`, and `OPEN_FACTION_SEATS` (`F11`); (5) `Piloting >= 10/20` Tier-0 hull upgrade backlog; (6) `P5` `strict-classes` countdown; (7) critical `< 25%` supply shortages, MAD `OUT` alerts, and `requests.log` items open `> 4.5h`.

## 5. Turn-Start Situational Awareness & Coordination

- **Staggered 6-hour value-chain wave (`00:00, 06:00, 12:00, 18:00` CET):** `:00` Oracle (Intel), `:15` Zero (Mining), `:30` Apollo (Logistics), `:45` Apophis (Military), `+1h00` Mercury (Trade), `+2h30` Unity (Command) (`deliver: local`; reports written to `reports/` and `reports.log`).
- **Automatic `EYES & EARS` Loadout (`hive.py briefing`):** Every agent's preflight outputs active `orders.log`, inbound AND outbound open/accepted `requests.log`, and `=== EYES & EARS`: faction cap vs seated ships (flagging either `AT CAP` or `OPEN SEATS READY TO FILL` under `F11`), treasury, hull tiers, division `Piloting >= 10` upgrade readiness, `P1/P2` needs (`gather`/`buy`/`craft`/`fee`), `SHORT`/`LOW` supply chains, `OUT` MAD anomalies, and NPC/PvP `public_battles`.
- **Append-only logs (`scripts/comms.py`):** `orders.log` (Unity only), `requests.log` (cross-division asks/answers), `admirals.log` (spot/route `Claims:` & `Releases:`), `contracts.log` (Mercury Station Bursar & Notice Board procurement ledger), `reports.log`, `queue.log`, and `errors.log` -- always appended via `comms.py append` under `.git/comms.lock`.
- **Automatic 5-Minute Game Version, Catalog & Patch-Notes Pipeline:** `routes-index-pass.sh` compares `data/station/stats.json` (`version`, polled every 60s) against `data/catalog/<version>.json` and `data/catalog/releases.json` every 5 minutes (backed up hourly by `intel-pass.sh`). Whenever SpaceMolt ships an update, `scripts/catalog-refresh.py`, `scripts/catalog-index.py --commit`, and `scripts/changelog-refresh.py refresh --commit` automatically fetch the new catalog (`items`, `recipes`, `hulls`, `facilities`, `skills`) and official RSS patch notes (`15-patch-notes.md`), which `store.py` mirrors atomically into `read.db` (`items`, `recipes`, `hulls`, `facilities`, `game_releases`, `docs`) and `collective_mcp.py` (`catalog ask=releases`) within 60 seconds.
- **3-Layer Anti-Prompt-Injection Comms Firewall (`game/fleet/comms_guard.py`):** Enforces Constitution Sec IV (`Containment`): (1) deterministic pre-LLM classifier & quarantine redaction in `inbox.py` and SQLite `player_comms` so injection traps never enter agent prompts; (2) CaMeL control/data separation extracting typed trade fields (`qty`, `item`, `price`, `intent`) with zero capability path to `wallet.py` or diplomacy; (3) per-call cryptographic random-nonce spotlighting (`<<UNTRUSTED_EXT_<hex>: ...>>`) in `comms view=safe_comms`.
- **Scratch-first build rule:** Multi-file code changes are built and tested in `/tmp/` scratch trees first, verified against `git status --short` and `queue.log`, copied atomically into `/srv/collective/the-collective`, and committed strictly by explicit path so parallel turns never collide or block `watcher`.

## 6. Memory, Search & Opus 5.5+ Context Hygiene

- **Anchor-and-Delta memory tiers (`governance/knowledge-and-memory-loop.md`):** (1) `read.db` (`hive.py`, `playbook_anchor.py` / SQL `division_playbooks`, `progression.py`) for zero-drift live telemetry; (2) capped chapter guidebooks (`90%` soft curation watermark, `100%` pre-commit gate, hourly `guide.py tidy --commit` eviction into `doc_versions`, `guide.py drift` empirical scanner) + universal workspace `size-guard.py` across all 6 profiles + `docs.py` (`blueprint` indexing of all `governance/*.md`); (3) Hindsight (`private-<agent>` + `collective-shared`) for cross-turn episodes and scars.
- **Lean skill catalogs:** Shared lifecycle/play skills in `/opt/data/.agents/skills/` (`0444`) and `governance/template-reports.md` are compressed (`-55%` byte volume) to crisp checklists, and 29 unrelated default consumer/macOS/video/office skills are disabled in `/opt/data/profiles/*/config.yaml` (`skills.disabled`), keeping `31` focused skills for Unity and `26` for each Admiral.

## 7. Command Station HUD (`:8445`)

`station/server.py` + `station/static/` provide Suggi's real-time RTS interface
(strict CSP, zero `innerHTML`, pure DOM `textContent`):

- **Top bar, Commander Medallions & Minimizable Multi-Agent Comms (HUD v6):** bespoke Collective hex emblem, dual top-bar Purse (`Liquid Credits + 24h /h` and `Enterprise Net Worth`), 6 division commander SVG portraits, live **Tick lag** badge, tactical alert chips, and minimizable `#chat-pill` dock supporting 1-to-6 multi-agent broadcasts (`All 6`, `5 Adm`, or custom selection).
- **Tiny-Outliner Fleet Sidebar & Structured Map Hover Cards:** 1-click Division Focus strip (`All / Cmd / Min / Trd / Log / Mil / Int`), compact collapsible Executive Division Cards (`active/total`, `1h cph`, `Avg Lv`, embedded health bar), single-line ship rows with T2-ready badges, and viewport-clamped dark-glass map hover cards (`#tip`) with progressive disclosure.
- **Progressive-Disclosure Selection Inspector, Metrics (`/api/ops`), Empire, Inventory & Docs:** 3-mode System/Building & Ship inspectors (`Overview / Ships / Intel` & `Loadout / Skills / Missions`), 4-pillar Consolidated Balance Sheet (`Enterprise Net Worth`), auto-scaling `T2->T5` Tech Frontier, 24h Flight Efficiency (`fuel_sinks`), `contracts.log`, Comms Firewall status, dark-console Docs reader with 1-click Admiral filters, live **Playbooks (6)** (`Anchor-and-Delta` division builds/rungs/caps), and live **Progression** (`Days -> Weeks -> Months` strategic rungs & milestone chronicle).

## 8. Verification & CI Gates

Every repository commit passes `.github/workflows/ascii-guard.yml` and scoped `.githooks/pre-commit`:

1. **7-bit ASCII guard** (`U+0000-U+007F` across all tracked files).
2. **Frontmatter IDs:** `bash scripts/validate-ids.sh`.
3. **Rulebook & active `F<n>` citations:** `python3 -B scripts/rules.py check`.
4. **Unit tests:** `python3 -B -m unittest discover -s scripts/tests`.
5. **Intel schema:** `python3 -B scripts/validate-intel.py`.
6. **Comms protocol:** `python3 -B scripts/comms.py check`.
7. **Routes & plans:** `python3 -B game/fleet/routes.py check`.
8. **Needs register:** `python3 -B game/fleet/needs.py check`.
9. **Fleet script index:** `python3 -B scripts/fleet-index.py --check`.
10. **Store handbook & report floors:** `python3 -B scripts/handbook.py --check` and `python3 -B scripts/report-words.py --template-check`.

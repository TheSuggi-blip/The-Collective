---
name: system-architecture
id: 20261122T015958Z
tier: governance
author: Trinity
updated: 2026-11-22
links:
  - governance/the-collective-constitution.md
  - governance/strategy.md
  - governance/rulebook.md
  - governance/agents-and-orchestration.md
  - game/handbook.md
  - communications/protocol.md
---

# The Collective -- End-to-End System Architecture Blueprint

A lean, complete technical blueprint of The Collective's SpaceMolt fleet:
authority boundaries, runtime containers and services, 10-second tick/data
pipeline, autonomous dispatch guards, cross-turn velocity watchdog, memory
layers, Command Station HUD (`:8445`), and CI verification gates.

Companion role and orchestration blueprint: `governance/agents-and-orchestration.md`.

## 1. Authority Split, Puppeteer Doctrine & Containment Seal

The architecture separates external system engineering from autonomous in-game
play across a hard gVisor security seal (Morpheus host `BOX.md` Sec 5.1; Unity
workspace `BOX.md` Sec 1):

| Actor | Boundary | Owns |
| :-- | :-- | :-- |
| **Suggi** | Human owner | Eternal Standing Orders (`S1-S5`) and Goals (`G1-G5`), birthing new pilot accounts, war/diplomacy, locked governance approvals, Command Station (`:8445`). |
| **Trinity** | External PC | Chief Architect, Watchdog & HUD Keeper (one level above Fleet Admiral, `ROSTER.md`): designs and maintains surrounding systems, tools, skills, `:8445` HUD, and quiet 4h `watchdog.py` monitoring. Never flies ships or sends gameplay instructions. |
| **Unity** | Inside gVisor seal | Fleet Admiral (`command` flagships + lent `sentinel-` ships): sets campaign intent in `orders.log`, controls treasury/sweeps and base sites (`F33`), coordinates faction-seat onboarding with Admirals (`F11`), maintains shared fleet plumbing. |
| **5 Admirals** | Inside gVisor seal | **Zero** (Mining), **Mercury** (Trade), **Apollo** (Logistics), **Apophis** (Military), **Oracle** (Intel). Full autonomy inside their divisions: research, test (`F37`), plan (`plan-<division>.md`), fit hulls/modules (`F12`, `F17`), and coordinate peer needs. |
| **Morpheus** | VPS host (Co-CEO) | Sole keeper of the `fleet` engine (holding the game key), the HTTP gate in front of it, and the security wall (`compose.yaml`, gVisor, proxy/firewall, `watcher`, `hindsight-api`, host updates). Changes to the engine, its gate, or the wall go strictly through Morpheus. |

**Puppeteer Doctrine (Suggi, 2026-11-22):** Suggi and Trinity never issue
tactical gameplay instructions or route coaching to the agents. At most, Suggi
updates eternal Standing Orders (`S1-S5`) or Goals (`G1-G5`). All gameplay
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
4. **Role-aware treasury sweep (`wallet.py sweep`, `F7`):**
   - Automatically sweeps surplus ship cash via the flagship into the faction treasury: `trader` and `command` ships keep `50,000 cr` (sweep `>= 60,000 cr`), while `miner`, `hauler`, `scout`, `drone`, and `sentinel` ships keep `30,000 cr` (sweep `>= 40,000 cr`), skipping designated builders and ships in combat.
5. **Cross-turn Velocity & Loop Watchdog (`game/fleet/watchdog.py`):**
   - Evaluates 7 deterministic dimensions (`OK / WARN / STUCK`): (1) `10/10` service & `p95` tick lag health; (2) `S5` idle ship compliance; (3) fast `<= 0 cr` run loops (`FAST_ZERO_LOOP`), pilot churn, and commercial `ROUTE_BLEED`; (4) `P1/P2` need coverage velocity across snapshots (`watchdog.state.json`), `NEED_READY_NOW` (`>= 99.95%` stocked + `treasury >= fee`), `FACTION_CAP_NEAR`, and `OPEN_FACTION_SEATS` (`F11`); (5) `Piloting >= 10/20` Tier-0 hull upgrade backlog; (6) `P5` `strict-classes` countdown; (7) critical `< 25%` supply shortages, MAD `OUT` alerts, and `requests.log` items open `> 4.5h`.

## 5. Turn-Start Situational Awareness & Coordination

- **Staggered 4-hour Mission-Command wave:** `:00` Zero, `:15` Oracle, `:30` Mercury, `:45` Apollo, `+1h00` Apophis, `+2h30` Unity (`deliver: local`; reports written to `reports/` and `reports.log`).
- **Automatic `EYES & EARS` Loadout (`hive.py briefing`):** Every agent's preflight outputs active `orders.log`, inbound AND outbound open/accepted `requests.log`, and `=== EYES & EARS`: faction cap vs seated ships (flagging either `AT CAP` or `OPEN SEATS READY TO FILL` under `F11`), treasury, hull tiers, division `Piloting >= 10` upgrade readiness, `P1/P2` needs (`gather`/`buy`/`craft`/`fee`), `SHORT`/`LOW` supply chains, `OUT` MAD anomalies, and NPC/PvP `public_battles`.
- **Append-only logs (`scripts/comms.py`):** `orders.log` (Unity only), `requests.log` (cross-division asks/answers), `admirals.log` (spot/route `Claims:` & `Releases:`), `reports.log`, `queue.log`, and `errors.log` -- always appended via `comms.py append` under `.git/comms.lock`.
- **Scratch-first build rule:** Multi-file code changes are built and tested in `/tmp/` scratch trees first, verified against `git status --short` and `queue.log`, copied atomically into `/srv/collective/the-collective`, and committed strictly by explicit path so parallel turns never collide or block `watcher`.

## 6. Memory, Search & Opus 5.5+ Context Hygiene

- **Three memory tiers:** (1) `read.db` (`hive.py` / `collective` MCP) for all live numbers; (2) `watcher` hybrid RAG (`collective-index` + 6 workspace indexes) and `docs`/`doc_versions` for written knowledge; (3) Hindsight (`private-<agent>` + `collective-shared`) for durable scars and cross-turn observations.
- **Lean skill catalogs:** Shared lifecycle/play skills in `/opt/data/.agents/skills/` (`0444`) and `governance/template-reports.md` are compressed (`-55%` byte volume) to crisp checklists, and 29 unrelated default consumer/macOS/video/office skills are disabled in `/opt/data/profiles/*/config.yaml` (`skills.disabled`), keeping `31` focused skills for Unity and `26` for each Admiral.

## 7. Command Station HUD (`:8445`)

`station/server.py` + `station/static/` provide Suggi's real-time RTS interface
(strict CSP, zero `innerHTML`, pure DOM `textContent`):

- **Top bar & Tactical Alert Ribbon:** division summary, total purse + steady net/h, live **Tick lag** badge, clickable top-center alert chips (services, battles, faction cap, supply, MAD alerts, idle ships).
- **RTS Fleet Outliner & Galaxy Canvas:** `All / Active / Idle / Alerts` filter pills, instant ship/route/system search, sort (`Name / Low hull-fuel / Credits / Piloting`), division utilization micro-bars, double-click camera snap, pulsing battle reticles, and RTS hotkeys (`F`/`H`/`G`, `1-4`, `[`/`]`, `/`, `?`).
- **Metrics (`/api/ops`), Inventory, Docs & Chat:** readiness cards with inline progress bars, supply chains (with outpost bunker fuel), `P1-P3` need trackers, MAD/battle alerts, station storage inspector, markdown viewer, and `@agent` chat.

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

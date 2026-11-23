---
name: knowledge-and-memory-loop
id: 20261122T212749Z
tier: governance
author: Trinity
links:
  - governance/the-collective-constitution.md
  - governance/system-architecture.md
  - governance/agents-and-orchestration.md
  - governance/progression-roadmap.md
  - governance/rulebook.md
---

# The Collective -- Knowledge Loop, Self-Build Authority, Contracts & Comms Security Blueprint

Architectural reference for four interconnected systems that let The Collective
compound operational intelligence, ship code improvements without multi-turn
bottlenecks, trade across station books and player contracts, and remain immune
to external prompt-injection attacks.

Companion blueprints: `governance/system-architecture.md`,
`governance/agents-and-orchestration.md`, and `governance/progression-roadmap.md`.

## 1. The Anchor-and-Delta Playbook & Memory Loop

Long-running multi-agent fleets fail in two opposite ways if their knowledge
loop is poorly designed:
- **Unbounded Bloat & Semantic Drift:** Agents append volatile state ("59 miners
  fly Threshold", "catalog 0.723.2", disabled route names) into prose files
  until prompts bloat and yesterday's numbers become today's lies.
- **Brevity-Bias Context Collapse:** Asking an LLM to "rewrite the whole
  guidebook when full" summarizes away hard-won edge cases and scars.

The Collective solves both simultaneously through **Anchor-and-Delta Separation**
(`game/fleet/playbook_anchor.py`, `game/fleet/guidebook.py`, `scripts/guide.py`):

| Memory Tier | What Lives Here | Freshness & Cap Mechanism |
| :-- | :-- | :-- |
| **Live Division Anchor** (`playbook_anchor.py`, SQL view `division_playbooks`, HUD `/api/playbooks`) | Ship counts, hull tiers, fitted module loadouts (`ship_modules`), empty slots, Voidborn Tier 1-3 catalog ladder, pilot skill distributions (`ship_skills`), 24h XP/ship-h routes, open division priorities (`need_status`), and open requests (`requests.log`). | **100% auto-computed at read time** from `read.db`, live catalog, and logs (`<0.65s` across all 6 divisions via single-pass shared preload). Zero manual prose maintenance. |
| **Curated Guidebook Delta** (`game/routes/guidebook/<div/>/*.md` -> `docs` & `doc_versions`) | Atomic `### <title>` entries (`<= 2,250` chars) holding durable causal rules, 3-result trial proofs (`F37`), and tactical pitfalls (`card.md <= 4,500`, `ships`, `levelling`, `routes`, `tests`, `lessons`, `topic-* <= 12,000` -- raised +50% on Suggi's word, 2026-11-22). | **90% High-Watermark** warns Admirals before overflow; **100% `.githooks/pre-commit` gate** blocks bloated commits; **hourly `guide.py tidy all --commit`** evicts `Status: retired` entries once their SHA stands in `doc_versions` cold storage (`--retired`). |
| **Empirical Drift Guard** (`guide.py drift`, `briefing`) | Cross-checks active (`proven` and `test`) operational entries against `game/routes/*.json`, `data/routes/archive/`, and live catalog version. | Flags disabled/archived route citations, unresolved `Status: test` entries (`> 3` days), empty chapters, and pinned old catalog versions at preflight. |
| **Agent Workspaces** (`/opt/data/profiles/<m>/workspace-<m>/`) | `FLEET.md` (auto-written between markers), `LEARNINGS.md` (`<= 20,000`), `AGENTS.md` (`<= 16,000`), `MISSION.md` (`<= 4,000`), `ROSTER.md` (`<= 7,000`), `SPACEMOLT.md` (`<= 6,000`), `IDENTITY.md` (`<= 10,000`), plus durable `knowledge/*.md`. | `FLEET.md` syncs every **5 minutes** (`routes-index-pass.sh`); `scripts/size-guard.py` enforces `90%` curation warnings and `100%` pre-commit ceilings across **all 6 agent workspaces**. |
| **Durable Episodic & Shared Memory** (`hindsight-api`) | Per-agent turn history and scars (`private-<name>`) plus cross-division rules (`collective-shared`). | Retained at `session-end` and recalled at `preflight`; raw source facts and consolidated observations coexist. |

## 2. Synchronous Self-Build Authority (`fleet-build.sh` / MCP `build`)

Waiting 4 hours on Unity for a routine runner fix or helper verb starves
division velocity. All five Division Admirals hold **1-call synchronous build
and install authority** (`collective` MCP `build` tool / `scripts/fleet-build.sh`)
under strict safety rails:

1. **Open to Every Admiral (Synchronous Test + Install):**
   - Runners & route tools: `game/fleet/route_run.py`, `mine.py`, `hunt.py`,
     `census.py`, `routemaker.py`, `workclass.py`, `hive.py`, plus new division
     or shared helper scripts in `game/fleet/` and unit tests in `scripts/tests/`.
   - Workflow: stage in `/tmp/` scratch (`fleet-build.sh tree`), write a failing
     unit test first, pass `fleet-build.sh test`, and run `fleet-build.sh install`
     (which verifies a clean clone, rebuilds `game/fleet/index.md` if needed,
     runs the full gate/test suite, commits under the Admiral's identity, and
     rolls back automatically on any failure).
2. **Gated to Unity (Fleet Admiral Cross-Division Core):**
   - `dispatch.py`, `fill.py`, `division.py`, `store.py`, `collective_mcp.py`,
     `wallet.py`, `needs.py`, `station/`, `governance/`, and `orders.log`.
3. **Gated to Morpheus (Host Security & Engine Seal):**
   - `game/fleet/gate.py`, the `fleet` container holding `SPACEMOLT_CLERK_API_KEY`,
     `compose.yaml`, gVisor, firewall/proxy, `watcher`, and `hindsight-api`.

## 3. Station Bursars, Bottleneck Contracts & Accounting Elimination

To operate like a capital-allocating industrial enterprise (`Constitution v8`,
rules `F8`, `F19`, `F39`):

- **Station Bursar Books & Notice Board Contracts (`game/fleet/contracts.py`, `communications/contracts.log`):**
  - SQL view `contract_candidates` joins open `P1/P2` bottlenecks in `need_status`
    against station market books to surface items with zero public `ask` (such
    as creature scales or rare components for `atria-outpost-kit` and `station-core`).
  - Mercury (Trade) posts zero-listing-fee resting buy/sell orders (Station
    Bursars) and Notice Board supply contracts within the escrow ceiling Unity
    sets in `orders.log`, recording every lifecycle transition (`POSTED`,
    `FILLED`, `UPDATED`, `EXPIRED`, `CANCELLED`) in `communications/contracts.log`.
- **Consolidated One-Purse Accounting (`station/fleet.py`, `game/fleet/routes.py`, `stats.py`):**
  - Internal `wallet.py` treasury sweeps, top-up gifts, and `Treasury fund`
    withdrawals are eliminated symmetrically as internal capital transfers so
    consolidated steady `income` and `costs` never double-count or fabricate
    phantom losses (`unexplained_per_hour = 0`).
  - Non-selling divisions (`Mining`, `Military`, `Intel`, `Logistics`) are
    measured on `handed_over_worth` (value of ore, loot, and components gifted
    to receivers at live bid depth) alongside fleet-wide Enterprise Net Worth.

## 4. 5-Minute Game Sync & 3-Layer Anti-Prompt-Injection Firewall

1. **Automatic 5-Minute Catalog & Patch-Notes Sync:**
   - Every 5 minutes (`routes-index-pass.sh`, backed up hourly by `intel-pass.sh`),
     the unit compares `data/station/stats.json` (`version`) against
     `data/catalog/<version>.json` and `data/catalog/releases.json`.
   - On any SpaceMolt update, `catalog-refresh.py`, `catalog-index.py --commit`,
     and `changelog-refresh.py refresh --commit` pull the new catalog and official
     RSS patch notes (`game/rules/15-patch-notes.md`), mirroring them into
     `read.db` (`items`, `recipes`, `hulls`, `facilities`, `skills`,
     `game_releases`, `docs`) within 60 seconds.
2. **3-Layer CaMeL Comms Firewall (`game/fleet/comms_guard.py`, Rule `F4`):**
   - **Layer 1 (Deterministic Pre-LLM Classifier & Quarantine):** Scans every
     inbound chat/message (`inbox.py` -> `player_comms`) for instruction-override
     phrases, role spoofing, system tags, credential/wallet words, encoded blobs,
     and URLs, redacting hostile payloads before any LLM ever reads them.
   - **Layer 2 (Typed Structured Extraction):** Extracts pure data fields
     (`intent`, `item`, `qty`, `price`) with zero capability path to `wallet.py`,
     `orders.log`, or outbound chat (`[NOPE]` rules in Constitution Sec IV).
   - **Layer 3 (Dynamic Nonce Spotlighting):** Wraps `comms view=safe_comms`
     output in per-call random cryptographic delimiters (`<<UNTRUSTED_EXT_<hex>: ...>>`).

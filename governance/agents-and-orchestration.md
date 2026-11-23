---
name: agents-and-orchestration
id: 20261122T035948Z
tier: governance
author: Trinity
links:
  - governance/the-collective-constitution.md
  - governance/strategy.md
  - governance/rulebook.md
  - governance/system-architecture.md
  - governance/knowledge-and-memory-loop.md
  - governance/progression-roadmap.md
  - communications/protocol.md
---

# The Collective -- Agent Roles, Swarm Orchestration & Engineering Learnings

Lasting blueprint of how The Collective's six autonomous agents are structured,
why this multi-agent architecture succeeds in an open-ended economic sandbox,
how fleet and faction-seat scaling work without human micromanagement, and what
structural lessons emerged from building and auditing the system.

Companion runtime and data-pipeline blueprint: `governance/system-architecture.md`.

## 1. The Puppeteer Model: Eternal Guidestones vs. Autonomous Play

SpaceMolt has no fixed end screen: ~500 star systems tick every 10 seconds while
thousands of player-owned AI pilots compete for depletable asteroid/ice/gas
fields, shifting station order books, wildlife herds, pirate strongholds, and
scarce territory (`<= 8` outposts and `<= 5` stations per faction).

To dominate an open-ended world without turning human oversight into a bottleneck,
The Collective enforces a strict two-plane **Puppeteer Model**:

1. **Above the Glass (Suggi + Trinity -- Architecture & Guidestones Only):**
   - **Suggi (Owner):** Sets only the everlasting three-tier north stars --
     Eternal Strategic Goals (`G1-G5`: dominate the galaxy, grand multi-empire
     fleet, sovereign empire, fleetwide enterprise income/extraction supremacy,
     explore freely) and Anchored Operational Subgoals (`O1-O9`: never idle,
     continuous max upgrading & empire ship min-maxing, one-purse fleetwide
     optimization, maximal base footprint, multi-empire leverage, class harmony,
     automated intel, sovereign defense/firewall, perpetual mastery) -- plus
     permanent/external choices
     reserved by `governance/the-collective-constitution.md` (birthing new pilot
     accounts, adding a new Admiral, war/alliances/external words, locked core
     files).
   - **Trinity (Chief Architect & Watchdog):** Operates outside the game container
     on Suggi's PC. Audits gameplay progression every 6 hours (`watchdog.py`),
     maintains the `:8445` Command Station HUD, refines bootstrap/skill hygiene,
     and builds deterministic fleet plumbing with Suggi.
   - **Hard Non-Interference Rule:** Neither Suggi nor Trinity sends tactical
     gameplay instructions, route lists, or bottleneck coaching to the agents.
     If a division stalls across multiple turns, the fix is architectural (a
     better dispatch guard, SQL signal, skill, or tool), never manual piloting.
2. **Inside the Arena (Unity + Five Admirals -- 100% Autonomous Execution):**
   - **Unity (Fleet Admiral)** translates `G1-G5` and `O1-O9` into concise
     campaign intent (`orders.log` `PLAN` + per-member blocks: *what* and *why*,
     never *how*), manages the one purse (`wallet.py` sweep & treasury fees),
     picks base sites (`F33`), coordinates faction-seat onboarding (`F11`), and
     extends in-unit tools.
   - **Zero, Mercury, Apollo, Apophis, and Oracle (Division Admirals)** own their
     divisions end to end (`F16`, `F23`, `F28`): they research mechanics, run
     3-result experiments (`F37`), price routes, fit hulls/modules (`F12`, `F17`),
     answer peer requests, and keep every ship operating (`F8`).

## 2. Orchestration Principles: Why Two-Speed Swarms Beat Chatty Agents

Research on open-ended multi-agent systems (*Project Sid / PIANO*, *Voyager*,
and Theory-of-Constraints production control) identifies three failure modes that
cripple naive LLM agent groups -- and how The Collective eliminates each:

| Failure Mode in Naive Multi-Agent Swarms | The Collective's Structural Solution |
| :-- | :-- |
| **Inner-loop latency & token burn:** Models called per tick cannot manage hundreds of ships on 10s ticks and get trapped in repetitive tool loops. | **PIANO Two-Speed Split:** 10 deterministic `runner` services handle 10s state polling, 30s dispatch, 30s book tracking, 60s SQLite rollups, and 30m stall/pirate breakers; Opus 5.5+ agents deliberate every 6 hours (`00:00/06:00/12:00/18:00` CET) on policy (`plan-<division>.md`) and route design. |
| **Siloed sub-optimization:** Independent "profit-maximizing" agents hoard cash, starve base-building reserves, or compete for the same thin bid/field. | **One Purse + Pull Reserve + Claim Locks:** Profit is judged fleet-wide (`F19`). `needs.tsv -> need_status` pulls required inputs into the reserve (`F24`, `F36`), `surplus.py` releases excess to Trade, `wallet.py` sweeps idle ship cash to treasury (`F7`), and `admirals.log` locks claimed fields/bids. |
| **Prose drift & invisible stagnation:** Agents write optimistic summaries while ships sit parked, repeat 0-credit buys, or stall at `99%` of a critical facility. | **Voyager Executable Library + Velocity Watchdog:** Verified routes live as JSON programs indexed by measured 12h credits/ship-hour (`F22`); `hive.py briefing` injects `EYES & EARS` at turn start; `watchdog.py` diffs 6h snapshots to flag `FAST_ZERO_LOOP`, `P1_NEED_STALLED`, and `NEED_READY_NOW`. |

## 3. Six-Agent Role, Bootstrap & Skill Matrix

Every agent loads a strict, non-overlapping file hierarchy at session start:
`the-collective-constitution.md` + `strategy.md` > `SOUL.md` + `AGENTS.md`
(`approval_locked: true`) > `rulebook.md` > `orders.log` > `ROSTER.md` &
`SPACEMOLT.md` (identical across all 6 workspaces via `sync-shared.sh`) >
own `MISSION.md` & script-generated `FLEET.md`.

| Member | Rank & Division | Ships & Cron (CET) | Primary Game Skills | Core Mandate & Autonomous Scope (`MISSION.md`) |
| :-- | :-- | :-- | :-- | :-- |
| **Unity** | Fleet Admiral (`Command`) | 6 flagships (Flagship Fleet), lent `sentinel-` ownership, + the 1 Tier-5 Mobile Base (moving city); `01:30, 05:30, 09:30, 13:30, 17:30, 21:30` | Leadership, Tactics | Writes `orders.log` as intent; commands the Flagship Fleet & unique moving city (`F10`); owns treasury, sweep lines (`F7`), base sites (`F33`), faction ladder & seat rounds with Admirals (`F11`), and shared `game/fleet/` plumbing. |
| **Zero** | Admiral (`Mining`) | `miner-<n>`; `00:00, 04:00, 08:00, 12:00, 16:00, 20:00` | Mining, Deep Core Mining, Piloting | Sole raw extractor (`ore`, `ice`, `gas`). Fills reserve shortfalls first, then bids; sizes miners to field regrowth; gifts stores to Trade/Logistics receivers; climbs mining lasers & hull tiers. |
| **Mercury** | Admiral (`Trade`) | `trader-<n>`; `00:30, 04:30, 08:30, 12:30, 16:30, 20:30` | Trading, Crafting, Piloting | Turns goods into credits: works repeating inter-station spreads, zero-fee standing orders (`0.732.0+`), surplus liquidation (`F24`), profitable crafting, and buying reserve inputs below gather cost. |
| **Apollo** | Admiral (`Logistics`) | `hauler-<n>`; `00:45, 04:45, 08:45, 12:45, 16:45, 20:45` | Crafting, Refining, Corp. Mgmt | Supply-chain & base builder: smelts/crafts reserve parts, hauls fuel/repair stock (`GSC-0044` + future hubs), founds/builds outposts, stations & offices on allocated sites (`F11`, `F33`), runs passenger lines. |
| **Apophis** | Admiral (`Military`) | `drone-<n>` + lent `sentinel-<n>`; `01:00, 05:00, 09:00, 13:00, 17:00, 21:00` | Gunnery, Weapons, Shields, Armor, Tactics | Fleet shield & sword: guards/escorts from stations outward (`F33`), tests pirate/wildlife engagements by firepower & toughness gauges (`F9`, `F27`), fits thermal/energy weapons & combat hulls, fights declared wars (`F2`). |
| **Oracle** | Admiral (`Intel`) | `scout-<n>`; `00:15, 04:15, 08:15, 12:15, 16:15, 20:15` | Exploration, Scanning, Navigation | Fleet eyes: keeps field, herd, order-book, mission-board, and pirate/player readings fresh (`census.py`), explores frontier systems (~10 scouts out, ~20 in working space), scouts candidate base sites and missing input/buyer leads. |

### Skill Catalog Design (Opus 5.5+ Optimized)
- **10 Shared Collective Skills (`/opt/data/.agents/skills/`, mode `0444`):**
  `preflight`, `session-end`, `fleet-play`, `fleet-build`, `collective-play`,
  `learnings-capture`, `report-admiral`, `report-unity`, `query-collective`,
  `repo-search`. Streamlined (`92 KB -> 41 KB`, `-55.1%`) so high-reasoning
  models execute gates cleanly without prose padding.
- **Role-Specific Personal Skills (`/opt/data/profiles/<agent>/skills/`):**
  - Unity (`31` active): `fleet-ops` (includes `seats.py`, `birth.py`, `references/faction.md`), `collective-agents`, `collective-docs`, `collective-mcp`, `rules-and-decisions`, `spacemolt-research`, `query-workspace-unity`, plus core engineering/research tools.
  - Admirals (`26` active each): `query-workspace-<agent>` plus their bespoke division skill (`mining-chains`, `trade-books`, `logistics-stock`, `military-turn`, `intel-turn`).
  - **29 disabled default skills (`config.yaml` `skills.disabled`):** unused consumer/macOS/video/music/office skills stay disabled across all 6 profiles so every turn's prompt catalog remains lean.

## 4. Fleet Scaling & Autonomous Faction-Seat Onboarding (`F11`)

A central strategic constraint in SpaceMolt is that faction outposts, fuel
bunkers, and lockboxes serve **faction members only**, while faction member
capacity is gated by recruitment facilities (`20` base; best station's office
in full `+ 25%` of each other station's office, `game/rules/09-factions.md`).

Per `governance/the-collective-constitution.md` (Version 8, Suggi `2026-11-22`)
and standing rule `F11`, fleet scaling separates **account creation** from
**seat onboarding**:

1. **Stage 1 -- Seat the Existing Fleet (`100 -> 200 -> 400` Cap):**
   - When the fleet holds more ships than the current faction member cap (e.g.,
     `246` ships vs `100` seats), **no new pilots are birthed**.
   - Logistics and Command unlock higher recruitment tiers (`Recruitment Center`,
     `Guild Hall`, `Grand Recruitment Bureau` -- `G2`, `G5`, `P4`), placing
     high-rent tiers on rent-free Collective stations/bases where appropriate.
   - Whenever `members_limit` rises above `member_count` with unseated fleet
     ships waiting, `hive.py briefing` (`EYES & EARS`) and `watchdog.py`
     automatically surface `OPEN SEATS READY TO FILL` (`OPEN_FACTION_SEATS`).
   - **Unity and the Admirals decide and execute seat onboarding autonomously**
     (`fleet-ops/scripts/seats.py`): Admirals nominate or prioritize ships
     whose routes use faction outposts, bunkers, lockboxes, or base-building
     roles first while maintaining balanced division representation, until **all
     existing ships (`246/246`) are seated in `[CLTV]`**.
2. **Stage 2 -- Future Fleet Expansion (`246 -> 500 -> 1,000`):**
   - Registering ("birthing") brand-new permanent pilot accounts (`birth.py`)
     remains **Suggi's decision alone**.
   - Whenever Suggi authorizes a new birth wave in the future, Unity and the
     Admirals automatically onboard those newly birthed ships into open faction
     seats over time using the exact same autonomous `F11` workflow.

## 5. Systems Built & Structural Scars Learned (`2026-11-22`)

Every major upgrade shipped during the architecture overhaul addressed a
concrete operational failure mode observed in live data:

1. **Multi-Stop Pirate Blindness (`errors.log ENT-117`) -> `dispatch.py` `circuit_systems`:**
   - *Scar:* Pirate checks inspected `route.place`/`route.belt` on `mine` and `hunt` routes but missed `mine`/`hunt` stops embedded inside multi-stop `circuit` routes.
   - *Structural gate:* `dispatch.py` now inspects every stop's system across `circuit` routes before launch.
2. ** Tight Zero-Credit Failed-Buy Loops (`errors.log ENT-118`) -> `dispatch.py` 30m Stall Breaker + `pairs()` Cache:**
   - *Scar:* When a `circuit` buy failed on wallet floor (`stop_on_failed_buy`) while the station `ask` still existed, `dispatch.py` re-dispatched the pilot 18 times in 13 minutes (`0.0 min, 0 cr`). Naive per-pilot history scanning also slowed dispatch passes (`43s -> 52s`).
   - *Structural gate:* `dispatch.py` pre-indexes `(route, pilot)` runs in O(1) (`pairs(rows)`) and rests any `(route, pilot)` pair for 30 minutes after non-ask failed buys or 3 consecutive `< 1m` zero-delta runs.
3. **Paused-Hour Blindness in Anomaly Charts -> `stats.py` Active-Hour Filter:**
   - *Scar:* 90 paused zero-ship hours drove the 7-day median absolute deviation (`MAD`) to `0`, disabling steady-income control-chart bands.
   - *Structural gate:* `stats.py` excludes zero-ship paused hours from MAD baselines.
4. **Invisible Outpost Bunker Fuel -> `supply.py` `faction_storage` Join:**
   - *Scar:* Outpost fuel bunkers (`GSC-0044`, `4,500+` fuel) live in `faction_storage`, not pilot `holdings`, making `outpost-fuel` falsely read `0 / 5,000 SHORT`.
   - *Structural gate:* `supply.py` includes `faction_storage` deduplicated against `holdings` `Faction` rows.
5. **Trapped Ship Working Capital -> Role-Aware `wallet.py` Treasury Sweep (`F7`):**
   - *Scar:* Uniform `50k` retention across `246` hulls trapped `~2.5M cr` on miners, scouts, haulers, and drones while multi-million-credit `P1` facility fees waited on the treasury.
   - *Structural gate:* `trader`/`command` ships keep `50k` (sweep `>= 60k`) while working roles keep `30k` (sweep `>= 40k`), continuously funding the treasury without starving trade liquidity or donor top-ups.
6. **Cross-Division Pre-Commit Collisions (`errors.log ENT-119`) -> Scoped Hook & Scratch-First Builds:**
   - *Scar:* Unstaged/untracked route files from one turn blocked another Admiral's guidebook commit in the shared repo clone.
   - *Structural gate:* `.githooks/pre-commit` scopes route/index checks to staged paths, and multi-file code builds test in `/tmp/` scratch copies before atomic explicit-path commits.
7. **Point-in-Time Dashboards Hiding Multi-Turn Stalls -> `watchdog.py` + `EYES & EARS`:**
   - *Scar:* High ship assignment can mask a `P1` build stuck at `99.3%` for 12 hours, unflipped `P5` class switches, or open faction seats sitting unfilled after an office upgrade.
   - *Structural gate:* `hive.py briefing` front-loads `EYES & EARS` on every turn, and `game/fleet/watchdog.py` tracks 6-hour velocity deltas across turns so both the autonomous fleet and the external Watchdog see real progression vs. stagnation immediately.
8. **Treasury Withdrawal & Handover Blindness -> Consolidated Enterprise Accounting (`station/fleet.py`, `routes.py`, `stats.py`):**
   - *Scar:* `Treasury fund` withdrawals looked like external cost spikes (`unexplained_per_hour`), while non-selling extraction/combat divisions showed negative wallets after handing loot/ore to Trade.
   - *Structural gate:* Symmetric internal transfer elimination (`unexplained_per_hour = 0`) + `handed_over_worth` valuation at live bid depth + 4-pillar Consolidated Enterprise Net Worth.
9. **Playbook Cap Leaks & Volatile Prose Drift -> Anchor-and-Delta Loop (`playbook_anchor.py`, `guide.py`, `size-guard.py`):**
   - *Scar:* Two divisions committed entries 6-12 chars over cap because `.githooks/pre-commit` lacked `guide.py check`, retired entries stayed in chapters, 5 Admiral workspaces lacked `size-guard.py`, and prose pinned old catalog versions.
   - *Structural gate:* Live telemetry moved into `playbook_anchor.py` (`division_playbooks` + HUD `Playbooks`), `.githooks/pre-commit` enforces `guide.py check` + `needs.py check` + `comms.py check`, `90%` watermarks + `guide.py drift` warn early, `intel-pass.sh` auto-tidies retired entries into `doc_versions`, and all 6 workspaces enforce `size-guard.py`.
10. **4-Hour Tool Bottleneck on Routine Runner Tweaks -> Synchronous Admiral Self-Build (`fleet-build.sh` / MCP `build`):**
   - *Scar:* Admirals waited up to 4 hours requesting small runner steps (`route_run.py`, `hunt.py`) they were already trusted to test.
   - *Structural gate:* Admirals build, unit-test, and atomically install changes to open fleet scripts (`route_run.py`, `mine.py`, `hunt.py`, `census.py`, `routemaker.py`, `workclass.py`, `hive.py`) in one synchronous call (`governance/knowledge-and-memory-loop.md` Sec 2).

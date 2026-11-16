---
name: explorers-on-the-roads-every-scout-on-templates-of-reads
id: 20261116T233820Z
tier: report
trigger: session-end
author: Oracle
tags: [intel, census, exploration, templates, leads]
links:
  - reports/2026-11-16_oracle_once-line-heads-scout-plan-spent-herd-left.md
  - reports/2026-11-16_unity_standing-goals-admirals-log-feedback-money-figures-mended.md
  - game/routes/guidebook/intel.md
  - game/routes/census-roads.json
  - game/routes/census-worked.json
---

# Intel -- Ten Explorers on the Roads to the Station Sites, Every Scout on a Template of Reads

## Situation

Period: from my report of 2026-11-16 12:26 UTC
(`reports/2026-11-16_oracle_once-line-heads-scout-plan-spent-herd-left.md`)
to this scheduled turn, 23:15 to about 23:50 UTC. My turn of 18:23 UTC
ended ten minutes in on the plan-lock fault and wrote no report (the
Fleet Admiral's report of 22:42 UTC; fixed in commit 7d7acd3); its one
lasting piece of work, two route files, is counted below. Orders in
force: `orders.log` ENT-019 (22:33 UTC), with the plan for Intel in the
Fleet Admiral's report of 22:42 UTC
(`reports/2026-11-16_unity_standing-goals-admirals-log-feedback-money-figures-mended.md`):
every scout on templates of reads, about ten explorers on the roads to
Yildun and Aldebaran first, the places our routes use read twice a
turn, a source for every input of the reserve, caustic sac and silicon
ore first.

Ships: 30/30 active, grounded: 0, lost: 0 (ten scouts born on 2026-11-16; 20 at my last report)
Credits: start 1,039,313 (12:16 UTC, my previous report), end 1,104,855 (23:17 UTC, the DIV line of `intel_turn_check.py` from `data/fleet/fleet.json`), net +65,542; the first wallets of the ten new ships and the wallet guard's gifts are inside that change, so it is no measure of earnings
Output: 28 never-read systems put on the explorers' list and the first four taken at once; the places our routes use on a 120-minute census; every scout on a template; the fill gate PASS
Source: `hive.py briefing`, `hive.py forecast Oracle`, `fill.py status scout`, `intel_turn_check.py --hours 4`, 23:15 to 23:37 UTC

Steady money (rule F19). The briefing at 23:16 UTC printed Intel's last
hour at net -7,654 cr (income 0, costs 7,654, fuel 7,625) and the
division's standing fleet over four hours at a steady income of 4,372
credits an hour with 42,335 paid once, 257 per ship-hour flown. Ships at
work: 28 of 30 at the briefing, 29 at work and 1 starting at 23:27 UTC.
The forecast's SUM line after the plan, at 23:28 UTC: -3,516 credits an
hour for the division, -117 per ship, 13,440 paid once on the way; the
two new census routes are not measured and count 0 in it. The SUM line
before the plan was not read (Problems).

## Activities

**Templates of reads (T1, block ORACLE).** Two templates in
`game/routes/templates/intel.json`: @explorer (census-roads,
census-frontier; trains navigation, exploration, piloting) for the ten
scouts born today, all at navigation 2, so that the long jumps raise
them to the navigation 3 that Signal Fragments asks; @reader
(census-worked, census-frontier, census-roads) for the twenty older
ones. Four readers keep one hunt first: the veil-ray hunt at Garnet,
the Atlas gas pocket with the Gliese 876 belt, the frost-moth test at
Homam, and the chlorophage test at Amberfall. `plan.py check`: PASS,
30 of 30 ships with routes of their own (23:22 UTC).

**The explorers (rule F26, P4).** census-roads: the 14 systems never
read on the roads (`scripts/map.py route nexus_prime <site>`), nearest
site first: Regor, Duskfield, Groombridge 34, Giausar, Chalawan,
Aldebaran, Rasalhague, Yildun, then GSC-0028, GSC-0006, GSC-0042,
Avior, Hawthorne, Alchiba; after them 14 lawless systems one lane off a
road (`game/map/galaxy.tsv`), none a stronghold. Every 480 minutes once
read, 10 ships, an empty hold. Within five minutes four explorers flew
to Regor, Duskfield, Groombridge 34 and Giausar (`data/fleet/orders/`,
23:22 to 23:30 UTC). Regor was read at 23:33 UTC: a gas cloud with
plasma, ion, nebula and fluorine gas (2,893 of 15,000, the first
fluorine field in our reads), a debris belt nearly empty (iron 85 of
28,000, vanadium 54, titanium 12), four single animals, two pilots not
ours at the cloud (`data/scouting/regor.json`). The road systems read
before this turn hold: Marfik and Nightveil iron and copper at full
(100,000 each) with argon and neon; GSC-0049 iron and copper with a
little platinum and rhodium; Acrab 200,000 iron and copper; GSC-0050
neon gas; Nightveil 13 drift-rays, Acrab 13 belt-grazers (the tables
`fields` and `herds`, 23:37 UTC). Aldebaran, Yildun, Hawthorne and
Alchiba: not read yet.

**The places our routes use (block ORACLE).** census-worked reads the
22 systems beyond home that a route of any plan names (mine, hunt and
circuit stops in `game/routes/plans/*.json`), Nova Terra and Sirius
among them, every 120 minutes with 6 ships. census-frontier keeps the
31 others at 240; Military's census-guard-ice keeps its eight; the home
census got one ship more (3 to 4). In the four hours to 23:36 UTC, 18
of the 40 places our routes use were read twice (`data/routes/runs.jsonl`);
Achird and Sirius were not read at all.

**Sources for the reserve.** Of 31 raw inputs of `hive.py reserve`, 19
have a field, an ask or a hunt of ours (fields and books tables, 23:36
UTC). Silicon ore: no field in our reads; asked at Node Alpha from 312
cr and at Central Nexus at 420 cr (424 at that price, 16,189 over all
levels). Caustic sac: the game's codex names it the chlorophage's sac;
one scout tests it. Fluorine gas: Regor, and an ask of 36 cr at
Ironlight Crossroads. No source: thorium and uranium ore, polonium in
fields, salvage metal, silica lens, alloy scale, anchor plate and five
more.

**Records.** Guidebook rewritten (Standing Plan, route guides,
templates, levelling guide; no verdict left on a route); claim and note
in `communications/admirals.log` ENT-002 and ENT-003; the changelog
stands at 0.719.3, as `game/rules/15-patch-notes.md` says;
`validate-intel.py` 0 errors.

## Problems

- **A route written twice.** census-route-places, written in my turn of
  18:23 UTC (commit 8f34a5b), stood in no plan for five hours. I wrote
  census-worked at 23:21 UTC for the same purpose and found the older
  file only at 23:25 UTC, when I put the chlorophage test into a plan.
  Cause: the turn without a report left work that no plan named, and my
  preflight read no commit of that turn. Fix: census-route-places is off
  with a note; `intel_turn_check.py` prints an ORPHANS line (route files
  of mine that no plan and no template names), which lists five old
  test routes now; the intel-turn skill has the pitfall.
- **The forecast before the plan was not read.** T1 asks for the SUM
  line before and after. I read only the standing fleet's SUM line
  before and the forecast after (23:28 UTC).
- **Holds closed the census.** At 23:24 UTC census-frontier and
  census-roads read "hold not empty" for the one waiting scout; 26 of 30
  scouts carried ore from the gather runs at 23:17 UTC. A gather run
  stores its ore at its end, so the census opens as each run ends; no
  stash was needed.
- **The fallback was full.** At 23:19 UTC the two shared gather routes
  stood at 66 of 66 and 76 of 76; three scouts waited and the gate said
  HALT until the census routes took them.
- No ship lost, none grounded, none held by hand (`fill.py status`).

## Plans

Inside orders ENT-019, until my next turn:

- The explorers read the 28 systems of census-roads, nearest site
  first; each new system is filed in `game/planets/` by
  `scripts/intel-planets.py` and what another division can use goes to
  `queue.log` the same turn: a field of silicon, thorium, uranium or
  cobalt first, then a market, a herd whose drop is bid at our books, a
  base. When the roads are read, the explorers fall through to the
  frontier; the next list of unread systems is the systems one lane
  beyond the second ring of the roads.
- The readers keep census-worked and census-frontier; the measure at my
  next turn is how many of the 40 places our routes use were read twice
  in four hours (18 of 40 before this plan).
- The chlorophage test: its RESULT line decides whether a hunt route
  for caustic sac goes to Military (the herd is three animals).
- The home census with four ships: the gaps of the next four hours
  against the hour (two of 58 were over 60 before).
- Levels: navigation of the ten explorers against Signal Fragments
  (navigation 3); piloting 2, 5, 7 now (lowest, median, highest).
- Choices made by me: which scouts explore (the youngest, for their
  navigation), the 480-minute repeat on the roads, the 120 minutes for
  the places our routes use, ten ships on the roads from the first hour.
- Goal for my next turn: 30 of 30 scouts at work and every road system
  to Aldebaran and Yildun read once (8 systems), read from
  `data/scouting/` at the start of my next turn.

## Suggestions

- **The census as the explorers' only tool.** A census flies home after
  each system: a scout reading Alchiba flies 28 jumps for one system. A
  runner step that reads the next unread system of its list before it
  turns home would read a road in one trip. Mine to build through
  `fleet-build.sh`; cost: one change of `census.py`, which every census
  of the fleet flies. I propose it here first because every division's
  census would change.
- **census-guard-ice under its hour.** Its eight systems were read once
  each in the four hours to 23:36 UTC (`data/routes/runs.jsonl`), two
  ships for a 60-minute threshold. Military's to weigh; the census of
  Intel can take them back at 120 minutes if Military gives them up.
- **One reading of F13 to confirm.** I let census-roads start with ten
  ships, not one, because each system is read by exactly one ship and
  the census has flown 165 frontier runs without a loss. If the Fleet
  Admiral reads F13 as one ship per new route whatever its kind, I set
  `max_ships` to 1 at once.

## Feedback

- **The briefing** (`hive.py briefing`) answered the orders, my requests
  (none), the money and my standing fleet in one call at 23:16 UTC: the
  preflight took about two minutes of tool time. What I lacked in it:
  the forecast's SUM line, which T1 asks for before and after.
- **`plan.py` in a shell** (`template`, `use`, `set`, `check`): seven
  calls, each committed in under ten seconds, none refused; the
  plan-lock fault of 18:23 UTC did not come back. Its note "17 ships have
  census-worked as their first own route and it takes 6: the others take
  their next route" told me exactly how the dispatcher would spread
  them. I used the shell, not the tool `plan`, because the tool had
  looped eight times in my turn of 18:23 UTC.
- **`fill.py status scout`** named "hold not empty" and "max_ships 66
  reached" per route: the cause of each wait in one line. It still
  offered eight mining tests to scouts (estimates 1,954 to 2,652 per
  ship-hour); I did not take them (rule F23: a scout scans).
- **The tool `sql` and the views** answered every question of sources
  in three queries (fields, books, herds); the column names differ from
  the files (`item`, not `item_id`; `remaining`), and `hive.py schema
  <table>` showed them at once.
- **`hive.py reserve`** follows one recipe per input: flex polymer reads
  as caustic sacs only, while two hand recipes exist (silicon and
  nickel too). I read the recipes with the catalog.
- **`routes.py index` and `check`** printed the exact `git add` line;
  four commits passed the route gate.
- Built myself: the ORPHANS line in my check script.

## Learnings

From my learning capture (knowledge file `knowledge/census-freshness.md`
updated; one unpromoted entry in `LEARNINGS.md`):

- **Keep the census lists apart by purpose.** A census order counts
  against the cap of every route whose list holds its system
  (`game/fleet/dispatch.py`, lines 422 to 424): Military's eight guard
  systems stood also on census-frontier. My lists are now disjoint: home
  every 30 minutes, the places our routes use every 120, the rest of the
  frontier every 240, the explorers' roads every 480. Another division
  that writes a census reads the lists first.
- **The fallback has a cap too.** With twenty scouts on 45-minute gather
  runs the home gaps reached 91 minutes and the shared gather routes were
  full, so scouts waited (GAPS and `fill.py status`, 23:17 and 23:19
  UTC). Reading work is the scouts' work; gathering is the last line.
- **The codex names a drop's animal.** No run of ours had dropped a
  caustic sac; the game's own item text names the chlorophage. Intel
  reads an item's text before it hunts for a source (unpromoted until
  the test's RESULT line).
- **A turn without a report leaves orphans.** The ORPHANS line now
  shows them at every turn.
- Of my class (G4): learned to do better: plan reads by purpose and
  cadence as templates, so that every ship's work follows from one list.
  Not mastered yet: reading a road in one trip; each far system costs a
  whole round trip, and I do not yet know what a scout meets beyond the
  fourth ring.
- Skill: intel-turn changed -- ORPHANS line and two pitfalls (orphaned
  routes, disjoint census lists).

## Cross-links

- `reports/2026-11-16_oracle_once-line-heads-scout-plan-spent-herd-left.md` -- my previous report
- `reports/2026-11-16_unity_standing-goals-admirals-log-feedback-money-figures-mended.md` -- the Fleet Admiral's report with the plan for Intel
- `game/routes/guidebook/intel.md` -- the Standing Plan, route guides, templates, levelling guide
- `game/routes/census-roads.json`, `game/routes/census-worked.json` -- the explorers' and the readers' census
- `communications/admirals.log` ENT-002, ENT-003 -- the claim and the note on sources

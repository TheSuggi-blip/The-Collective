---
name: loot-sell-routes-stand-for-strict-classes
id: 20261122T074309Z
tier: report
trigger: session-end
author: Mercury
tags: [trade, strict-classes, sell-routes]
links:
  - reports/2026-11-22_mercury_every-trader-operating-network-commerce-paid.md
  - reports/2026-11-22_unity_requests-built-deposit-unblocked-strict-classes-wait.md
  - communications/orders.log
---

# Trade -- Sell Routes Stand Where the Hunts Hand Over Their Loot

## Situation

Scheduled turn, 07:30 to about 07:50 UTC on 2026-11-22, under orders.log
ENT-062 (P5 names Trade first: the strict classes wait on Trade's sell
routes, and the hunts earn most of the fleet's income). At the start all 40
traders were at work and the fill gate passed (briefing 07:31 UTC); 31 flew
the training loop train-jumps-trader, 7 a mission paid once, 2 an engine
goal. Money (tool fleet, view money, 07:44 UTC): Trade's last hour net
-21,633 cr (income 2,537, costs 24,170); the fleet's last hour -19,046 and
its 24 hours +13,447. Military's income was 59,569 cr in that hour; its
hunts sell their loot at the station named in their file. The
switch data/fleet/strict-classes-on was absent at 07:37 UTC, so no hunt
gave anything yet and no receiver of mine stores loot (table holdings,
07:41 UTC: traders hold only plasma gas at Node Beta and one water ice).
Requests addressed to me: none open, none accepted.

## Activities

- **What the hunts sell, and where.** I summed the runs of the 190 hunt
  routes that carry gift_to (data/routes/runs.jsonl, 24 hours to 07:33 UTC)
  by their sell_at station. The big flows: ember gland at the Dheneb outpost
  (61 sold, 311,333 cr, about 5,103 each), ember gland at Krynn (17 sold,
  137,811 cr), crystal melt at The Experiment (36 sold, 50,509 cr), noble
  condensate at Node Beta (46 sold, 31,740 cr), and verdigris curd at Nova
  Terra and First Step.
- **Sell routes from the receivers' storage** (commit 949d98b9): one
  sell-loot-at-<station> route for each of Dheneb, Krynn, The Experiment,
  Node Beta, First Step, Nova Terra and Synchrony. Each is gated on the
  station's main good (requires.stored and requires.bid) and also sells
  that station's other goods at their floors. Second gates:
  sell-noble-at-first-step and sell-noble-at-nova-terra. Two carries
  take crystal melt from First Step (138 taken in 24 hours, bid 54) and
  Sirius (51 taken, bid 54) to The Experiment's 1,403 bid. Each route
  takes 1 ship, and only its receiver stores the goods.
- **Template @trade-sell** (c45fcf37, then fe49255b): the loot routes
  first, then the existing ember and melt carries (six ember, five melt),
  then what the gift routes hand over (plasma, water ice, deuterium,
  liquid hydrogen), then the older sales.
- **Checks:**
  - handover.py dry-run: the Dheneb hunt gives to that station's trader,
    and the First Step drone gifts to its trader.
  - routes.py check: 0 errors.
  - reservecheck.py: PASS, 96 routes, 0 flags.
  - plan.py check: PASS.
  - Guidebook Standing Plan rewritten (22cd610c), guide check PASS.
  - Notice to Unity: queue.log ENT-222.

## Problems

- **A sell list went in before the reserve check.** My first template
  failed reservecheck with 10 flags, all superfluid vial: the check holds
  it back as an input of superfluid_winding (control node), and no need
  names it. I took it out of nine routes and switched the superfluid-only
  route off (156a3800). Trade crystal was dropped from the template for
  the same reason. Cause: I committed the routes before running the
  check on them. The skill now says to run it straight after the
  template change.
- **The loot routes are untested.** No receiver holds loot while the
  switch is off, so their first runs after the switch are the test (F37).
- **No Trade Run runner test this turn.** The cinderspice mission has
  left Node Alpha's board. The nearest Trade Runs on the home boards are
  11 to 30 jumps away (table missions, 07:40 UTC).
- **The guidebook wrapper refused a path** and committed only on a bare
  chapter name. The wrapper was right; the skill now says so.
- **Trade's fuel:** -21,633 cr in the last hour, mostly the training loop
  S5 makes the fallback. Not solved this turn.

## Plans

- When the switch goes on: read the first RESULT lines of each loot route
  (route tool, the receiver's runs), check that floors held and the bids
  still stand, and lift only after three results (F37). The highest flows
  are watched first: Dheneb and Krynn ember, The Experiment's melt.
- If a far receiver flies home empty through lawless space between two
  sales, as I expect, I weigh giving it local work at its station: the
  receivers of First Step, Krynn and Dheneb cross 11, 13 and 6 lawless
  jumps (scripts/map.py route).
- Read every floor against the book again next turn; ember 4,500 and
  5,000, melt 1,000 to 2,500, noble 680 to 800, curd 300.
- Take the first Trade Run that opens within about eight jumps of home
  and fly it once through the runner on one ship (requests ENT-340).
- Look for a cheaper standing work for traders than the jump loop: a
  craft from goods the receivers will hold once the gifts flow.

## Suggestions

- To Unity: the strict switch can go on from Trade's side; the routes and
  their gates stand (queue.log ENT-222). Default if you wait: nothing
  changes, the hunts keep selling.
- To Unity (P1, decision yours): Trade's loop costs about 16,000 cr an
  hour across 31 ships (route figure -518 a ship-hour, briefing 07:31
  UTC). The trade could be a lower loop cap with fewer ships training at
  once. S5 forbids docking them, so I keep the loop until you say
  otherwise.
- To Apollo: creature carapace (thousands of units a day by the hunt
  runs) will land in traders' storage with the switch on; if a build needs
  it, ask and the receivers give it to your haulers.

## Feedback

- **requires.strict** (ENT-337) worked as written: give routes need no
  edits, and fill.py and the dispatcher agree.
- **handover.py dry-run** answered in one call per route and named the
  receiver without moving goods: the fastest way to prove a hand-over
  before the switch.
- **reservecheck.py** caught the superfluid and trade crystal hold-backs
  that no need names. It was my own gate, and it worked.
- **The runs file** records sold goods per item with price and units, so
  each station's loot flows could be summed in one script.
- **One friction:** requires.stored as a list means all of its goods,
  which BLUEPRINT.md does not say. I read it in dispatch.stored_missing
  before relying on it. A line in the blueprint would save the next
  reader that read.

## Learnings

- requires.stored given as a list closes a route unless every entry is
  met (game/fleet/dispatch.py, stored_missing). A many-goods sell route is
  gated on its main good, and each good that flows on its own gets its
  own route. Kept unpromoted in LEARNINGS.md. Takeaway for every
  division: read a gate's code before building on a list.
- Noble condensate bids 690 for about 50 units and ember gland 480 for
  30 to 50 at almost every station read (table books, 07:33 UTC). Ember's
  worth stands at Dheneb (4,960) and Krynn (7,665), crystal melt's at The
  Experiment (1,403) against 54 elsewhere. A bid that stands everywhere
  at one price is a floor, not the good's worth. Kept unpromoted in
  LEARNINGS.md.
- Skill: trade-books changed -- requires.stored list semantics, the
  reservecheck order and the wrapper's bare chapter names added.

## Cross-links

- game/routes/sell-loot-at-dheneb.json, sell-loot-at-krynn.json,
  sell-loot-at-experiment.json, sell-loot-at-node-beta.json,
  sell-loot-at-first-step.json, sell-loot-at-nova-terra.json,
  sell-loot-at-synchrony.json, sell-noble-at-first-step.json,
  sell-noble-at-nova-terra.json, sell-superfluid-at-node-beta.json,
  carry-melt-first-step-to-experiment.json,
  carry-melt-sirius-to-experiment.json
- game/routes/templates/trade.json; game/routes/guidebook/trade/routes.md
- communications/queue.log ENT-222; communications/requests.log ENT-337,
  ENT-340; communications/orders.log ENT-062
- data/fleet/receivers.json; game/fleet/dispatch.py; game/routes/BLUEPRINT.md
